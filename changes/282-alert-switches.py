# changes/282-alert-switches.py - Phone alerts: every alert has a real on/off switch you tap in the app (saved to GitHub with the key on the device); the GitHub link and the master switches are gone

NEW_CSS = r'''  /* change 282 (install.py) */
  button.gx-sw282 { min-height: 28px !important; min-width: 46px !important; padding: 0 !important; }
  .gx-sw282::after { content: ""; position: absolute; inset: -9px -6px; }
  .gx-sw282 { position: relative; width: 46px; height: 28px; border-radius: 99px; background: var(--line2); flex-shrink: 0; transition: background-color .2s ease; }
  .gx-sw282.on { background: var(--good); }
  .gx-sw282 i { position: absolute; top: 2px; left: 2px; width: 24px; height: 24px; border-radius: 99px; background: #ffffff; box-shadow: 0 1px 3px rgba(0,0,0,.35); transition: transform .2s cubic-bezier(.2,.8,.2,1); }
  .gx-sw282.on i { transform: translateX(18px); }
  .gx-sw282:active { transform: none; }
</style>'''

HELPERS = r'''// ---------- change 282: alert switches you tap in the app (install.py) ----------
const GX_AL_API282 = "https://api.github.com/repos/dhaliwal32/23456789786634356/contents/alert_prefs.json";
// read alert_prefs.json on GitHub, put the changed lines in, save it
const gxAlSave282 = (patch) => {
  const key = gxSyncKey();
  if (!key) return Promise.reject(new Error("nokey"));
  const hdr = { Authorization: "Bearer " + key, Accept: "application/vnd.github+json" };
  const once = (again) => fetch(GX_AL_API282 + "?ref=main&t=" + Date.now(), { headers: hdr, cache: "no-store" })
    .then((r) => { if (r.status === 401 || r.status === 403) throw new Error("key"); if (!r.ok) throw new Error("read " + r.status); return r.json(); })
    .then((j) => {
      let cur = {};
      try { cur = JSON.parse(gxUnB64(j.content)); } catch (e) {}
      return fetch(GX_AL_API282, { method: "PUT", headers: { ...hdr, "Content-Type": "application/json" },
        body: JSON.stringify({ message: "Alert switches from the app", content: gxB64(JSON.stringify({ ...cur, ...patch }, null, 2) + "\n"), branch: "main", sha: j.sha }) })
        .then((r) => { if ((r.status === 409 || r.status === 422) && again) return once(false); if (!r.ok) throw new Error(r.status === 401 || r.status === 403 ? "key" : "save " + r.status); return true; });
    });
  return once(true);
};
// what to save when one switch is tapped; if its whole group was switched off, the group comes back on and its other alerts stay off
const gxAlPatch282 = (p, x) => {
  const row = GX_AL.find((r) => r[1] === x.k) || [], g = row[4], patch = { [x.k]: !x.on };
  if (!x.on && g && p && p[g] === false) {
    patch[g] = true;
    GX_AL.forEach((r) => { if (r[4] === g && r[1] !== x.k) patch[r[1]] = false; });
  }
  return patch;
};
function GxSw282({ on, label, onTap }) {
  return <button type="button" role="switch" aria-checked={!!on} aria-label={label} className={"gx-sw282" + (on ? " on" : "")} onClick={onTap}><i></i></button>;
}
'''

HOOK_OLD = r'''  // alerts page v67 (news_logos.py)
  const [d, setD] = useState(null);'''
HOOK_NEW = HOOK_OLD + r'''
  const [ov282, setOv282] = useState({}); /* change 282: switches tapped here, shown at once */
  const [er282, setEr282] = useState("");'''

ST_OLD = r'''  const st = gxAlertState(d.p), log = gxAlertLog(d.b);'''
ST_NEW = r'''  const P282 = { ...(d.p || {}), ...ov282 };
  const st = gxAlertState(P282), log = gxAlertLog(d.b);
  const flip282 = (x) => {
    const patch = gxAlPatch282(P282, x), back = {};
    Object.keys(patch).forEach((k) => (back[k] = P282[k]));
    setEr282(""); setOv282((o) => ({ ...o, ...patch }));
    gxAlSave282(patch).catch((e) => {
      setOv282((o) => ({ ...o, ...back }));
      const m = (e && e.message) || "";
      setEr282(m === "nokey" ? "To change switches here, first turn on Sync between devices on this device (Setup, More, Data and backup)." : m === "key" ? "GitHub refused the key saved on this device." : "Could not save that. Try again.");
    });
  };'''

LINK_OLD_A = r'''          <a className="text-sm text-blue-600" style={{ marginLeft: "auto" }} href={GX_PREFS_URL} target="_blank" rel="noopener">Change</a>
        </div>
        <div className="text-xs text-slate-500" style={{ marginTop: 2 }}>'''
LINK_END = r'''Nothing is sent from 11 p.m. to 7 a.m.</div>'''
LINK_NEW = r'''        </div>
        <div className="text-xs text-slate-500" style={{ marginTop: 2 }}>Tap a switch to change it. It applies at the next sync, within 30 minutes. Nothing is sent from 11 p.m. to 7 a.m.</div>
        {er282 ? <div className="text-xs" style={{ color: "var(--bad)", marginTop: 6 }}>{er282}</div> : null}{/* change 282 */}'''

ROW_OLD = r'''<span className="text-sm" style={{ color: x.on ? "var(--good)" : "var(--mute)" }}>{x.on ? "On" : "Off"}</span>'''
ROW_NEW = r'''<GxSw282 on={x.on} label={x.label} onTap={() => flip282(x)} />'''

WHY_OLD = r'''" in the last 7 days" + (x.why ? " \u00b7 " + x.why : "")}'''
WHY_NEW = r'''" in the last 7 days"}'''

MASTER_START = r'''        <div className="text-xs text-slate-500" style={{ margin: "12px 0 2px", letterSpacing: ".04em" }}>Master switches</div>'''
MASTER_END = r'''            <span className="text-sm" style={{ color: on ? "var(--good)" : "var(--mute)" }}>{on ? "On" : "Off"}</span>
          </div>
        ); })}
'''


def cut(t, name, start, end, new, done):
    if done in t:
        print(f"(install) {name}: already done")
        return t
    if t.count(start) != 1:
        fail(f"'{name}' start matched {t.count(start)} times")
    a = t.find(start)
    b = t.find(end, a)
    if b < 0:
        fail(f"'{name}' end not found")
    print(f"(install) {name}: updated")
    return t[:a] + new + t[b + len(end):]


def change(t):
    t = lit(t, "282: styles", "</style>", NEW_CSS, "change 282 (install.py)")
    t = lit(t, "282: helpers", ROOT, HELPERS + ROOT, "change 282: alert switches you tap in the app")
    t = lit(t, "282: state", HOOK_OLD, HOOK_NEW, "const [ov282, setOv282]")
    t = lit(t, "282: flip", ST_OLD, ST_NEW, "const flip282 = ")
    t = cut(t, "282: no link", LINK_OLD_A, LINK_END, LINK_NEW, "{er282 ? <div")
    t = lit(t, "282: switch in each row", ROW_OLD, ROW_NEW, "<GxSw282 on={x.on}")
    t = lit(t, "282: no master note", WHY_OLD, WHY_NEW)
    t = cut(t, "282: no master switches", MASTER_START, MASTER_END, "", "change 282: no master switches") if MASTER_START in t else t
    return t

edit(APP, change)
