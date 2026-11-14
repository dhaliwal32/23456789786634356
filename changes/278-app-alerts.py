# changes/278-app-alerts.py - alerts from the app itself: turn them on in Setup > Phone alerts and the home-screen app gets the same alerts as ntfy, and tapping one opens the right page (ntfy keeps working too)

NEW_CSS = r'''  /* change 278 (install.py) */
  .gx-ps278 { display: flex; align-items: center; gap: 10px; flex-wrap: wrap; }
  .gx-ps278 .tx { flex: 1; min-width: 180px; }
  .gx-ps278 .bt { display: flex; gap: 8px; flex-wrap: wrap; }
  .gx-ps278 .bt button { border: 1px solid var(--line2); border-radius: 10px; padding: 7px 14px; font-size: 14px; color: var(--ink); min-height: 36px; }
  .gx-ps278 .bt button:disabled { opacity: .5; }
  .gx-ps278 .ms { flex-basis: 100%; font-size: 12.5px; color: var(--mute); }
</style>'''

HELPERS = r'''// ---------- change 278: alerts from the app itself (install.py) ----------
const GX_PUSH_API278 = "https://api.github.com/repos/dhaliwal32/23456789786634356/contents/push_subs.json";
const GX_PUSH_RUN278 = "https://api.github.com/repos/dhaliwal32/23456789786634356/actions/workflows/push-test.yml/dispatches";
const gxPushOk278 = () => { try { return "serviceWorker" in navigator && "PushManager" in window && "Notification" in window; } catch (e) { return false; } };
const gxPushBytes278 = (str) => { const b = atob(String(str || "").replace(/-/g, "+").replace(/_/g, "/")), u = new Uint8Array(b.length); for (let i = 0; i < b.length; i++) u[i] = b.charCodeAt(i); return u; };
const gxPushStr278 = (buf) => { const u = new Uint8Array(buf || []); let x = ""; for (let i = 0; i < u.length; i++) x += String.fromCharCode(u[i]); return btoa(x).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, ""); };
// read push_subs.json on GitHub, change the list with fn, save it (same key as Sync between devices)
const gxPushSave278 = (fn) => {
  const key = gxSyncKey();
  if (!key) return Promise.reject(new Error("nokey"));
  const hdr = { Authorization: "Bearer " + key, Accept: "application/vnd.github+json" };
  const once = (again) => fetch(GX_PUSH_API278 + "?ref=main&t=" + Date.now(), { headers: hdr, cache: "no-store" })
    .then((r) => { if (r.status === 404) return null; if (r.status === 401 || r.status === 403) throw new Error("key"); if (!r.ok) throw new Error("read " + r.status); return r.json(); })
    .then((j) => {
      let cur = [];
      try { cur = (JSON.parse(gxUnB64(j.content)).subs) || []; } catch (e) {}
      const body = { message: "App alerts: devices", content: gxB64(JSON.stringify({ subs: fn(cur) }, null, 1) + "\n"), branch: "main" };
      if (j && j.sha) body.sha = j.sha;
      return fetch(GX_PUSH_API278, { method: "PUT", headers: { ...hdr, "Content-Type": "application/json" }, body: JSON.stringify(body) })
        .then((r) => { if ((r.status === 409 || r.status === 422) && again) return once(false); if (!r.ok) throw new Error(r.status === 401 || r.status === 403 ? "key" : "save " + r.status); return true; });
    });
  return once(true);
};
// tapping an alert: the helper file (sw.js) tells the open app which page to show
(function gxPushBoot278() {
  try {
    if (window.__gxPush278 || !gxPushOk278()) return;
    window.__gxPush278 = 1;
    navigator.serviceWorker.addEventListener("message", (e) => { const h = e.data && e.data.gxGo278; if (h && typeof h === "string" && h[0] === "#") window.location.hash = h; });
    if (Notification.permission === "granted") navigator.serviceWorker.register("sw.js").catch(() => {});
  } catch (e) {}
})();
function GxPush278() {
  const [st, setSt] = useState("load"); // load, none, off, on
  const [msg, setMsg] = useState("");
  const [busy, setBusy] = useState(false);
  const ios = /iPhone|iPad|iPod/.test(navigator.userAgent || "");
  useEffect(() => {
    let dead = false;
    if (!gxPushOk278()) { setSt("none"); return undefined; }
    navigator.serviceWorker.getRegistration().then((reg) => (reg ? reg.pushManager.getSubscription() : null))
      .then((sub) => { if (!dead) setSt(sub && Notification.permission === "granted" ? "on" : "off"); })
      .catch(() => { if (!dead) setSt("off"); });
    return () => { dead = true; };
  }, []);
  const why = (e) => { const m = (e && e.message) || ""; return m === "nokey" ? "First turn on Sync between devices on this device (Setup, More, Data and backup), then come back here." : m === "key" ? "GitHub refused the key saved on this device." : "That did not work (" + (m || "unknown") + "). Try again."; };
  const turnOn = () => {
    if (!gxSyncKey()) { setMsg(why(new Error("nokey"))); return; }
    setBusy(true); setMsg("");
    let P;
    try { P = Promise.resolve(Notification.requestPermission()); } catch (e) { P = Promise.resolve("denied"); } // asked straight from the tap, as the iPhone requires
    P.then((perm) => {
      if (perm !== "granted") throw new Error("blocked");
      return fetch("push_key.json?t=" + Date.now(), { cache: "no-store" }).then((r) => { if (!r.ok) throw new Error("notready"); return r.json(); });
    }).then((k) => navigator.serviceWorker.register("sw.js").then(() => navigator.serviceWorker.ready).then((reg) => reg.pushManager.getSubscription()
      .then((old) => (old ? old.unsubscribe().catch(() => {}) : null))
      .then(() => reg.pushManager.subscribe({ userVisibleOnly: true, applicationServerKey: gxPushBytes278(k.key) }))))
      .then((sub) => {
        const row = { endpoint: sub.endpoint, p256dh: gxPushStr278(sub.getKey("p256dh")), auth: gxPushStr278(sub.getKey("auth")), name: ios ? "iPhone" : "Computer", at: new Date().toISOString() };
        return gxPushSave278((cur) => cur.filter((x) => x.endpoint !== row.endpoint).concat([row]).slice(-6));
      })
      .then(() => { setSt("on"); setMsg("On. Tap Send a test to try it."); })
      .catch((e) => {
        const m = (e && e.message) || "";
        setMsg(m === "blocked" ? "Alerts are blocked for this app. Allow them in " + (ios ? "iPhone Settings, Notifications, Islands GM." : "your browser's site settings.") : m === "notready" ? "Not ready yet. Try again in 10 minutes." : why(e));
      })
      .then(() => setBusy(false));
  };
  const turnOff = () => {
    setBusy(true); setMsg("");
    navigator.serviceWorker.getRegistration().then((reg) => (reg ? reg.pushManager.getSubscription() : null))
      .then((sub) => { if (!sub) return null; const ep = sub.endpoint; return sub.unsubscribe().catch(() => {}).then(() => gxPushSave278((cur) => cur.filter((x) => x.endpoint !== ep)).catch(() => {})); })
      .then(() => { setSt("off"); setMsg("Off on this device."); }).catch((e) => setMsg(why(e))).then(() => setBusy(false));
  };
  const test = () => {
    const key = gxSyncKey();
    if (!key) { setMsg(why(new Error("nokey"))); return; }
    setBusy(true); setMsg("");
    fetch(GX_PUSH_RUN278, { method: "POST", headers: { Authorization: "Bearer " + key, Accept: "application/vnd.github+json", "Content-Type": "application/json" }, body: JSON.stringify({ ref: "main" }) })
      .then((r) => setMsg(r.status === 204 ? "Test sent. It should arrive in about a minute." : "Could not start the test (" + r.status + ")."))
      .catch(() => setMsg("Could not reach GitHub. Try again.")).then(() => setBusy(false));
  };
  const sub = st === "load" ? "Checking..." : st === "on" ? "On for this device. Tapping an alert opens the app on the right page."
    : st === "none" ? (ios ? "Open the app from its home screen icon. If you already did, delete the icon, add it again from Safari (Share, Add to Home Screen), and come back here." : "This browser cannot show alerts from the app.")
    : "Get alerts from the app itself, without the ntfy app.";
  return (
    <div className="gx-pn gx-ps278" data-gx="278">
      <span className="tx"><span className="block">Alerts from this app</span><span className="block text-xs text-slate-500">{sub}</span></span>
      {st === "off" ? <span className="bt"><button type="button" disabled={busy} onClick={turnOn}>{busy ? "Working..." : "Turn on"}</button></span> : null}
      {st === "on" ? <span className="bt"><button type="button" disabled={busy} onClick={test}>Send a test</button><button type="button" disabled={busy} onClick={turnOff}>Turn off</button></span> : null}
      {msg ? <span className="ms">{msg}</span> : null}
    </div>
  );
}
'''

OLD_TITLE = r'''<div className="font-semibold" style={{ fontSize: 17 }}>Phone alerts</div>'''
NEW_TITLE = OLD_TITLE + r'''
      <GxPush278 />{/* change 278 */}'''

OLD_HEAD = r'''<!-- round 50 home-screen app -->'''
NEW_HEAD = OLD_HEAD + r'''
<link rel="manifest" href="manifest.webmanifest">'''

MANIFEST = r'''{
 "name": "Fantasy Islands GM",
 "short_name": "Islands GM",
 "start_url": "fantasy-gm.html",
 "scope": "./",
 "display": "standalone",
 "background_color": "#0c0d0f",
 "theme_color": "#0c0d0f",
 "icons": [{ "src": "icon.png", "sizes": "512x512", "type": "image/png" }]
}
'''

SW = r'''/* sw.js - change 278: shows alerts sent to the home-screen app and opens the right page when one is tapped. It stores nothing and never touches how the app loads. */
self.addEventListener("install", function () { self.skipWaiting(); });
self.addEventListener("activate", function (e) { e.waitUntil(self.clients.claim()); });
self.addEventListener("push", function (e) {
  var d = {};
  try { d = e.data ? e.data.json() : {}; } catch (x) { d = { body: e.data ? e.data.text() : "" }; }
  e.waitUntil(self.registration.showNotification(d.title || "Fantasy GM", { body: d.body || "", icon: "icon.png", data: { url: d.url || "#matchup" } }));
});
self.addEventListener("notificationclick", function (e) {
  e.notification.close();
  var hash = (e.notification.data && e.notification.data.url) || "#matchup";
  e.waitUntil(self.clients.matchAll({ type: "window", includeUncontrolled: true }).then(function (list) {
    for (var i = 0; i < list.length; i++) {
      if (list[i].url.indexOf("fantasy-gm.html") >= 0) { list[i].postMessage({ gxGo278: hash }); return list[i].focus(); }
    }
    return self.clients.openWindow("fantasy-gm.html" + hash);
  }));
});
'''

GM_PUSH = r'''"""
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
'''

NOTIFY_OLD = '''    """Send one message to the phone right now. Returns True if sent."""'''
NOTIFY_NEW = NOTIFY_OLD + '''
    try:  # change 278: the same alert also goes to the home-screen app
        import gm_push
        gm_push.send(title, msg, "#myteam")
    except Exception as ex:
        print(f"(notify) app alert not sent: {ex}")'''
MAIN_OLD = '''    else:
        try:
            flush()
'''
MAIN_NEW = '''    else:
        try:  # change 278: keep push_key.json there for the app
            import gm_push
            gm_push.ensure_key()
        except Exception as ex:
            print(f"(notify) push key: {ex}")
        try:
            flush()
'''
LIVE_OLD = '''def push(title, msg):
    if not NTFY_TOPIC:
'''
LIVE_NEW = '''def push(title, msg):
    try:  # change 278: the same alert also goes to the home-screen app
        import gm_push
        gm_push.send(title, msg, "#matchup")
    except Exception as e:
        log("app alert failed", e)
    if not NTFY_TOPIC:
'''


def change(t):
    t = lit(t, "278: styles", "</style>", NEW_CSS, "change 278 (install.py)")
    t = lit(t, "278: manifest link", OLD_HEAD, NEW_HEAD, 'rel="manifest"')
    t = lit(t, "278: helpers", ROOT, HELPERS + ROOT, "change 278: alerts from the app itself")
    t = lit(t, "278: show it", OLD_TITLE, NEW_TITLE, "<GxPush278 />")
    return t


def notify(t):
    t = lit(t, "278: notify send", NOTIFY_OLD, NOTIFY_NEW, "gm_push.send(title, msg")
    t = lit(t, "278: notify key", MAIN_OLD, MAIN_NEW, "gm_push.ensure_key()")
    return t


edit(APP, change)
edit("gm_notify.py", notify)
edit("gm_live.py", lambda t: lit(t, "278: live send", LIVE_OLD, LIVE_NEW, "gm_push.send(title, msg"))
new_file("gm_push.py", GM_PUSH)
new_file("sw.js", SW)
new_file("manifest.webmanifest", MANIFEST)
