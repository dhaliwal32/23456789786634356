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


def write_enc(path, text, name="ESPN_ENC"):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write("window." + name + " = " + json.dumps(seal(text)) + ";\n")
    os.replace(tmp, path)
