"""gm_lock.py - change 156: writes a scrambled copy of the league data (espn-data.enc.js) that only the app password can open.

No secret is needed here: the data is locked with a public key, and only the app (after the password) holds the matching private key.
Scheme: zlib, then ChaCha20 (RFC 8439) with a fresh random key; that key is sealed with RSA-OAEP (SHA-256).
"""
import base64, hashlib, json, os, struct, zlib

N = 26556585423764321684251125016358737272256729561016144732895830262800914560717610824670402253629983328321588315646674339293680356551465829442616221782204772322531694264381316545539343192463074743521541005282355568695634357507522741253969134735672935538611915400680250897878642929437660768118035666649029880684604956947347033270877237090232264355549119125165500347567999510777088886127736726886645328204989203183498266393086750900579505444069684994429714885609853379795286102282304315849200073730371054958018566149228464852283480630711129821499914048669935860038468643849754881278150633258416296779524202969228419094779
E = 65537


def _mgf1(seed, n):
    out, c = b"", 0
    while len(out) < n:
        out += hashlib.sha256(seed + c.to_bytes(4, "big")).digest()
        c += 1
    return out[:n]


def _oaep(m):
    k = (N.bit_length() + 7) // 8
    h = hashlib.sha256(b"").digest()
    db = h + b"\x00" * (k - len(m) - 66) + b"\x01" + m
    seed = os.urandom(32)
    mdb = bytes(a ^ b for a, b in zip(db, _mgf1(seed, k - 33)))
    ms = bytes(a ^ b for a, b in zip(seed, _mgf1(mdb, 32)))
    em = int.from_bytes(b"\x00" + ms + mdb, "big")
    return pow(em, E, N).to_bytes(k, "big")


def _rotl(v, c):
    return ((v << c) & 0xffffffff) | (v >> (32 - c))


def _block(key_w, ctr, nonce_w):
    s = [0x61707865, 0x3320646e, 0x79622d32, 0x6b206574] + key_w + [ctr] + nonce_w
    x = s[:]
    def qr(a, b, c, d):
        x[a] = (x[a] + x[b]) & 0xffffffff; x[d] = _rotl(x[d] ^ x[a], 16)
        x[c] = (x[c] + x[d]) & 0xffffffff; x[b] = _rotl(x[b] ^ x[c], 12)
        x[a] = (x[a] + x[b]) & 0xffffffff; x[d] = _rotl(x[d] ^ x[a], 8)
        x[c] = (x[c] + x[d]) & 0xffffffff; x[b] = _rotl(x[b] ^ x[c], 7)
    for _ in range(10):
        qr(0, 4, 8, 12); qr(1, 5, 9, 13); qr(2, 6, 10, 14); qr(3, 7, 11, 15)
        qr(0, 5, 10, 15); qr(1, 6, 11, 12); qr(2, 7, 8, 13); qr(3, 4, 9, 14)
    return struct.pack("<16I", *[(x[i] + s[i]) & 0xffffffff for i in range(16)])


def chacha20(key, nonce, data):
    kw, nw = list(struct.unpack("<8I", key)), list(struct.unpack("<3I", nonce))
    out = bytearray(len(data))
    for i in range(0, len(data), 64):
        ks = _block(kw, 1 + i // 64, nw)
        ch = data[i:i + 64]
        out[i:i + len(ch)] = bytes(a ^ b for a, b in zip(ch, ks))
    return bytes(out)


def seal(text):
    key, nonce = os.urandom(32), os.urandom(12)
    c = chacha20(key, nonce, zlib.compress(text.encode("utf-8"), 9))
    b = lambda x: base64.b64encode(x).decode()
    return {"v": 1, "k": b(_oaep(key)), "n": b(nonce), "c": b(c)}


# ---------- change 307: steady pieces, so the repo stops growing ~200 MB a week ----------
# v1 used a fresh random key every sync, so every saved copy was completely different and git could not
# store it efficiently. v2 cuts the data into pieces at points chosen by the content itself, and locks each
# piece with one steady key and a nonce made from the piece (the "synthetic IV" method). A piece that did not
# change comes out byte for byte the same, and git stores it once. Someone without the password can only
# tell which pieces stayed the same between syncs, not what is in them.
import hmac
import random as _random

_RND = _random.Random(307)
_GEAR = [_RND.getrandbits(32) for _ in range(256)]
# maps looked up by id that come out in a different order each sync for no reason (the app never lists them in stored order)
STEADY = (("model", "proj"), ("model", "base"), ("signals", "teampp"))


def _steady(text):
    try:
        d = json.loads(text)
        for a, b in STEADY:
            x = d.get(a)
            x = x.get(b) if isinstance(x, dict) else None
            if isinstance(x, dict):
                d[a][b] = {k: x[k] for k in sorted(x)}
        return json.dumps(d)
    except Exception:
        return text


def _pieces(b, bits=12, low=1024, high=65536):
    mask, out, st, h, g = ((1 << bits) - 1) << (32 - bits), [], 0, 0, _GEAR  # top bits: they depend on the last 32 bytes
    for i in range(len(b)):
        h = ((h << 1) + g[b[i]]) & 0xffffffff
        n = i - st
        if (n >= low and not (h & mask)) or n >= high:
            out.append(b[st:i + 1])
            st, h = i + 1, 0
    if st < len(b):
        out.append(b[st:])
    return out


def _master():
    s = os.environ.get("ESPN_S2", "").strip()
    if not s:
        return os.urandom(32)  # no steady secret: still locked, just no saving
    return hmac.new(s.encode("utf-8"), b"gx-lock-v2 307", hashlib.sha256).digest()


def seal2(text):
    m = _master()
    key = hmac.new(m, b"enc", hashlib.sha256).digest()
    ivk = hmac.new(m, b"iv", hashlib.sha256).digest()
    b = lambda x: base64.b64encode(x).decode()
    out = []
    for p in _pieces(_steady(text).encode("utf-8")):
        z = zlib.compress(p, 9)
        n = hmac.new(ivk, z, hashlib.sha256).digest()[:12]
        out.append(b(n + chacha20(key, n, z)))
    return {"v": 2, "k": b(_oaep(key)), "c": out}


def write_enc(path, text, name="ESPN_ENC"):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        try:
            e = seal2(text)
            head = json.dumps({"v": 2, "k": e["k"]})[:-1]
            f.write("window." + name + " = " + head + ', "c": [\n' + ",\n".join(json.dumps(c) for c in e["c"]) + "\n]};\n")
        except Exception as ex:  # never lose a sync over this: fall back to the old kind
            print(f"(lock) steady pieces failed, using the old kind: {type(ex).__name__}: {ex}")
            f.seek(0)
            f.truncate()
            f.write("window." + name + " = " + json.dumps(seal(text)) + ";\n")
    os.replace(tmp, path)
