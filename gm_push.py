"""
gm_push.py - change 278: phone alerts straight from the Fantasy Islands GM home-screen app (web push).
The app saves each device that turned alerts on in push_subs.json. This file sends a message to every
one of them. It needs no new secret: its signing key is worked out from the SWID and NTFY_TOPIC secrets,
and only the public half is saved, in push_key.json, for the app to read.
Other scripts call:  gm_push.send(title, text, url="#matchup")
Commands:
  python gm_push.py          make sure push_key.json is there
  python gm_push.py --test   send a test alert to every device
"""
import base64
import hashlib
import hmac
import json
import os
import sys
import time
from urllib.parse import urlparse

HERE = os.path.dirname(os.path.abspath(__file__))
SUBS = os.path.join(HERE, "push_subs.json")
KEYF = os.path.join(HERE, "push_key.json")
SITE = "https://dhaliwal32.github.io/23456789786634356/"
ORDER = 0xFFFFFFFF00000000FFFFFFFFFFFFFFFFBCE6FAADA7179E84F3B9CAC2FC632551


def _b64(b):
    return base64.urlsafe_b64encode(b).rstrip(b"=").decode()


def _unb64(s):
    s = str(s or "").strip()
    return base64.urlsafe_b64decode(s + "=" * (-len(s) % 4))


def _private():
    from cryptography.hazmat.primitives.asymmetric import ec
    seed = os.environ.get("SWID", "").strip() + "|" + os.environ.get("NTFY_TOPIC", "").strip()
    if len(seed) < 12:
        return None
    d = int.from_bytes(hmac.new(seed.encode("utf-8"), b"fantasy-gm-webpush-v1", hashlib.sha256).digest(), "big")
    return ec.derive_private_key(d % (ORDER - 1) + 1, ec.SECP256R1())


def _point(pub):
    from cryptography.hazmat.primitives import serialization as ser
    return pub.public_bytes(ser.Encoding.X962, ser.PublicFormat.UncompressedPoint)


def public_key():
    k = _private()
    return _b64(_point(k.public_key())) if k else None


def ensure_key():
    """Save the public key for the app (push_key.json). Returns it, or None when the secrets are missing."""
    pk = public_key()
    if not pk:
        return None
    try:
        with open(KEYF, encoding="utf-8") as f:
            if json.load(f).get("key") == pk:
                return pk
    except Exception:
        pass
    with open(KEYF, "w", encoding="utf-8") as f:
        json.dump({"key": pk}, f)
        f.write("\n")
    print("(push) saved push_key.json")
    return pk


def _hkdf(salt, ikm, info, n):
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.hkdf import HKDF
    return HKDF(algorithm=hashes.SHA256(), length=n, salt=salt, info=info).derive(ikm)


def encrypt(data, p256dh, auth):
    """RFC 8291 (aes128gcm) body for one device."""
    from cryptography.hazmat.primitives.asymmetric import ec
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    ua = _unb64(p256dh)
    eph = ec.generate_private_key(ec.SECP256R1())
    mine = _point(eph.public_key())
    shared = eph.exchange(ec.ECDH(), ec.EllipticCurvePublicKey.from_encoded_point(ec.SECP256R1(), ua))
    ikm = _hkdf(_unb64(auth), shared, b"WebPush: info\x00" + ua + mine, 32)
    salt = os.urandom(16)
    cek = _hkdf(salt, ikm, b"Content-Encoding: aes128gcm\x00", 16)
    nonce = _hkdf(salt, ikm, b"Content-Encoding: nonce\x00", 12)
    body = AESGCM(cek).encrypt(nonce, data + b"\x02", None)
    return salt + (4096).to_bytes(4, "big") + bytes([len(mine)]) + mine + body


def _vapid(endpoint, key):
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric import ec
    from cryptography.hazmat.primitives.asymmetric.utils import decode_dss_signature
    u = urlparse(endpoint)
    head = _b64(json.dumps({"typ": "JWT", "alg": "ES256"}, separators=(",", ":")).encode())
    body = _b64(json.dumps({"aud": u.scheme + "://" + u.netloc, "exp": int(time.time()) + 12 * 3600, "sub": SITE}, separators=(",", ":")).encode())
    r, s = decode_dss_signature(key.sign((head + "." + body).encode(), ec.ECDSA(hashes.SHA256())))
    jwt = head + "." + body + "." + _b64(r.to_bytes(32, "big") + s.to_bytes(32, "big"))
    return "vapid t=" + jwt + ", k=" + _b64(_point(key.public_key()))


def _subs():
    try:
        with open(SUBS, encoding="utf-8") as f:
            return [x for x in json.load(f).get("subs", []) if x.get("endpoint") and x.get("p256dh") and x.get("auth")]
    except Exception:
        return []


def send(title, text, url="#matchup"):
    """Send one alert to every device that turned app alerts on. Returns how many accepted it. Never raises."""
    try:
        import requests
        key = _private()
        subs = _subs()
        if not key or not subs:
            return 0
        data = json.dumps({"title": str(title), "body": str(text), "url": url}).encode("utf-8")
        ok = 0
        for x in subs:
            try:
                r = requests.post(x["endpoint"], data=encrypt(data, x["p256dh"], x["auth"]), timeout=20, headers={
                    "Authorization": _vapid(x["endpoint"], key), "Content-Encoding": "aes128gcm",
                    "Content-Type": "application/octet-stream", "TTL": "3600", "Urgency": "high"})
                if r.status_code in (200, 201, 202):
                    ok += 1
                else:
                    print(f"(push) a device refused the alert ({r.status_code}): {r.text[:120]}")
            except Exception as ex:
                print(f"(push) could not reach a device: {ex}")
        print(f"(push) app alert sent to {ok} of {len(subs)} device(s)")
        return ok
    except Exception as ex:
        print(f"(push) off: {ex}")
        return 0


if __name__ == "__main__":
    try:
        print("(push) key ready" if ensure_key() else "(push) no key: SWID and NTFY_TOPIC secrets are missing")
    except Exception as ex:
        print(f"(push) could not make the key: {ex}")
    if "--test" in sys.argv:
        n = send("Fantasy GM", "Test - alerts from the app are working.", "#matchup")
        print(f"(push) test sent to {n} device(s)")
