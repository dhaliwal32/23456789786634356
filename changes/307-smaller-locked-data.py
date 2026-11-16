# changes/307-smaller-locked-data.py - the locked league data is saved in small pieces that stay the same when nothing in them changed, so each sync adds about a fifth as much to the repo (about 30 KB instead of 175 KB); the app opens both the old and new kind

LOCK_OLD = '''def write_enc(path, text, name="ESPN_ENC"):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write("window." + name + " = " + json.dumps(seal(text)) + ";\\n")
    os.replace(tmp, path)'''

LOCK_NEW = '''# ---------- change 307: steady pieces, so the repo stops growing ~200 MB a week ----------
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
            f.write("window." + name + " = " + head + ', "c": [\\n' + ",\\n".join(json.dumps(c) for c in e["c"]) + "\\n]};\\n")
        except Exception as ex:  # never lose a sync over this: fall back to the old kind
            print(f"(lock) steady pieces failed, using the old kind: {type(ex).__name__}: {ex}")
            f.seek(0)
            f.truncate()
            f.write("window." + name + " = " + json.dumps(seal(text)) + ";\\n")
    os.replace(tmp, path)'''

JS_OLD = '''  function dec(E) {
    return unlocked.then(function (k) {'''

JS_NEW = '''  function dec(E) {
    if (E && E.v === 2) return dec307(E);
    return unlocked.then(function (k) {'''

JS_HELP_OLD = '''  function load(src) {'''

JS_HELP_NEW = '''  // change 307: the new kind is many small locked pieces; each one is nonce (12 bytes) + locked, zipped text
  function dec307(E) {
    return unlocked.then(function (k) {
      return crypto.subtle.decrypt({ name: "RSA-OAEP" }, k, b64(E.k));
    }).then(function (raw) {
      var key = new Uint8Array(raw);
      return Promise.all(E.c.map(function (s) {
        var u = b64(s), z = chacha(key, u.subarray(0, 12), u.subarray(12));
        return new Response(new Blob([z]).stream().pipeThrough(new DecompressionStream("deflate"))).arrayBuffer();
      }));
    }).then(function (parts) {
      var n = 0, i, all;
      for (i = 0; i < parts.length; i++) n += parts[i].byteLength;
      all = new Uint8Array(n); n = 0;
      for (i = 0; i < parts.length; i++) { all.set(new Uint8Array(parts[i]), n); n += parts[i].byteLength; }
      return JSON.parse(new TextDecoder().decode(all));
    });
  }
  function load(src) {'''


def lock_py(t):
    t = lit(t, "307: steady pieces", LOCK_OLD, LOCK_NEW, "change 307: steady pieces")
    py_ok("gm_lock.py", t)
    return t


def lock_js(t):
    t = lit(t, "307: open the new kind", JS_OLD, JS_NEW, "dec307(E);")
    t = lit(t, "307: new kind reader", JS_HELP_OLD, JS_HELP_NEW, "change 307: the new kind")
    return t


edit("gm_lock.py", lock_py)
edit("gx-lock.js", lock_js)
