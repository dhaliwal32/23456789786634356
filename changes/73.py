# changes/073-settings-sync.py - keeps settings the same on every device through settings.json in the repo

SYNC = r'''// ---------- change 073: settings sync between devices (install.py) ----------
const GX_SYNC_K = "gm-sync-key", GX_SYNC_AT = "gm-sync-at";
const GX_SYNC_API = "https://api.github.com/repos/dhaliwal32/23456789786634356/contents/settings.json";
const GX_SYNC_SET = ["pmode", "pbest", "minGain", "protectTop", "minF", "minD", "minGo", "blend", "autoDone", "autoGoalie", "gw", "poStart", "poWeeks"];
const gxSyncKey = () => { try { return localStorage.getItem(GX_SYNC_K) || ""; } catch (e) { return ""; } };
const gxSyncNote = (t) => { window.__SYNC_ST = t; window.dispatchEvent(new Event("gx-sync")); };
const gxSyncPick = (s) => {
  const set = {}, keep = [], back = {};
  GX_SYNC_SET.forEach((k) => { if (s[k] !== undefined) set[k] = s[k]; });
  if (s.pbest) delete set.pmode;
  (s.players || []).forEach((p) => {
    if (p.keep) keep.push(p.id);
    if (p.back && p.back !== (DEFAULT_BACK[p.n] || "")) back[p.id] = p.back;
  });
  let watch = [];
  try { watch = JSON.parse(localStorage.getItem("gm-watch") || "[]") || []; } catch (e) {}
  return { set, keep, back, watch, theme: window.__themePref ? window.__themePref() : "auto" };
};
const gxSyncSig = (P) => {
  const srt = (o) => { const x = {}; Object.keys(o || {}).sort().forEach((k) => (x[k] = o[k])); return x; };
  return JSON.stringify([srt(P.set), (P.keep || []).slice().sort(), srt(P.back), (P.watch || []).slice().sort(), P.theme || "auto"]);
};
const gxSyncApply = (st, R) => {
  const next = { ...st }, keep = new Set(R.keep || []), back = R.back || {};
  GX_SYNC_SET.forEach((k) => { if (R.set && R.set[k] !== undefined) next[k] = R.set[k]; });
  next.players = (st.players || []).map((p) => {
    const def = DEFAULT_BACK[p.n] || "";
    const b = back[p.id] != null ? back[p.id] : p.back && p.back !== def ? def : p.back;
    const k = keep.has(p.id);
    return !!p.keep === k && b === p.back ? p : { ...p, keep: k, back: b };
  });
  return next;
};
const gxB64 = (str) => btoa(unescape(encodeURIComponent(str)));
const gxUnB64 = (b) => decodeURIComponent(escape(atob(String(b || "").replace(/\s/g, ""))));
function GxSync({ s, setS }) {
  const [, tick] = useState(0);
  const sha = React.useRef(null), last = React.useRef(null), timer = React.useRef(null), ready = React.useRef(false), sRef = React.useRef(s);
  sRef.current = s;
  useEffect(() => {
    const h = () => tick((x) => x + 1);
    window.addEventListener("gm-watch", h); window.addEventListener("gm-theme", h);
    return () => { window.removeEventListener("gm-watch", h); window.removeEventListener("gm-theme", h); };
  }, []);
  const hdr = (key) => ({ Authorization: "Bearer " + key, Accept: "application/vnd.github+json" });
  const pull = () => {
    const key = gxSyncKey();
    const req = key
      ? fetch(GX_SYNC_API + "?ref=main&t=" + Date.now(), { headers: hdr(key), cache: "no-store" }).then((r) => {
          if (r.status === 404) { sha.current = null; return null; }
          if (r.status === 401 || r.status === 403) throw new Error("key");
          if (!r.ok) throw new Error("net");
          return r.json().then((j) => { sha.current = j.sha; return JSON.parse(gxUnB64(j.content)); });
        })
      : fetch("settings.json?t=" + Date.now(), { cache: "no-store" }).then((r) => (r.ok ? r.json() : null));
    return req.then((R) => {
      if (!R || !R.at) { if (key) gxSyncNote("On \u00b7 nothing saved yet"); return false; }
      let seen = "";
      try { seen = localStorage.getItem(GX_SYNC_AT) || ""; } catch (e) {}
      last.current = gxSyncSig(R);
      if (key) gxSyncNote("On \u00b7 last change " + gxWhen(R.at));
      if (R.at <= seen) return false;
      try { localStorage.setItem(GX_SYNC_AT, R.at); } catch (e) {}
      setS((st) => gxSyncApply(st, R));
      if (Array.isArray(R.watch)) { try { localStorage.setItem("gm-watch", JSON.stringify(R.watch)); } catch (e) {} window.dispatchEvent(new Event("gm-watch")); }
      if (R.theme && window.__themePref && window.__setTheme && window.__themePref() !== R.theme) window.__setTheme(R.theme);
      return true;
    }).catch((e) => { if (key) gxSyncNote(e && e.message === "key" ? "GitHub refused the key. It needs Contents: Read and write on this repo." : "Could not reach GitHub. Trying again in 2 minutes."); return true; });
  };
  const push = () => {
    const key = gxSyncKey();
    if (!key || !ready.current) return;
    const P = gxSyncPick(sRef.current), sig = gxSyncSig(P);
    if (sig === last.current) return;
    const body = { ...P, at: new Date().toISOString() };
    const put = (again) => fetch(GX_SYNC_API, {
      method: "PUT", headers: { ...hdr(key), "Content-Type": "application/json" },
      body: JSON.stringify({ message: "Settings saved from the app", content: gxB64(JSON.stringify(body, null, 1) + "\n"), branch: "main", ...(sha.current ? { sha: sha.current } : {}) }),
    }).then((r) => {
      if ((r.status === 409 || r.status === 422) && again) {
        return fetch(GX_SYNC_API + "?ref=main&t=" + Date.now(), { headers: hdr(key), cache: "no-store" }).then((g) => (g.ok ? g.json() : null)).then((j) => { sha.current = j ? j.sha : null; return put(false); });
      }
      if (!r.ok) { gxSyncNote(r.status === 401 || r.status === 403 ? "GitHub refused the key. It needs Contents: Read and write on this repo." : "Saving failed (" + r.status + "). Trying again in 2 minutes."); return; }
      return r.json().then((j) => {
        sha.current = j && j.content ? j.content.sha : null;
        last.current = sig;
        try { localStorage.setItem(GX_SYNC_AT, body.at); } catch (e) {}
        gxSyncNote("On \u00b7 saved " + gxWhen(body.at));
      });
    });
    return put(true).catch(() => gxSyncNote("Could not reach GitHub. Trying again in 2 minutes."));
  };
  useEffect(() => {
    let busy = false;
    const cycle = () => {
      if (busy) return;
      busy = true;
      pull().then((applied) => { ready.current = true; busy = false; if (!applied) push(); });
    };
    cycle();
    const id = setInterval(cycle, 2 * 60 * 1000);
    const vis = () => { if (document.visibilityState === "visible") cycle(); };
    document.addEventListener("visibilitychange", vis);
    window.addEventListener("gx-sync-now", cycle);
    return () => { clearInterval(id); document.removeEventListener("visibilitychange", vis); window.removeEventListener("gx-sync-now", cycle); };
  }, []);
  const sig = gxSyncSig(gxSyncPick(s));
  useEffect(() => {
    if (!ready.current || !gxSyncKey() || sig === last.current) return;
    clearTimeout(timer.current);
    timer.current = setTimeout(push, 4000);
    return () => clearTimeout(timer.current);
  }, [sig]);
  return null;
}
function GxSyncRow() {
  const [, tick] = useState(0);
  const [key, setKey] = useState("");
  const [edit, setEdit] = useState(false);
  useEffect(() => { const h = () => tick((x) => x + 1); window.addEventListener("gx-sync", h); return () => window.removeEventListener("gx-sync", h); }, []);
  const has = !!gxSyncKey(), st = window.__SYNC_ST || "";
  const btn = "border border-slate-300 rounded-lg px-3 py-1 text-sm";
  const save = () => { const v = key.trim(); if (!v) return; try { localStorage.setItem(GX_SYNC_K, v); } catch (e) {} setKey(""); setEdit(false); gxSyncNote("Key saved. Syncing..."); window.dispatchEvent(new Event("gx-sync-now")); };
  const off = () => { try { localStorage.removeItem(GX_SYNC_K); } catch (e) {} gxSyncNote(""); };
  return (
    <div className="gx-sr">
      <span className="min-w-0"><span className="block">Sync between devices</span><span className="block text-xs text-slate-500">{has ? st || "On" : "Off on this device. Turn on and paste your GitHub key."}</span></span>
      {edit ? (
        <span className="flex gap-2 items-center">
          <input type="password" autoComplete="off" className={inp + " text-sm"} style={{ width: 170 }} placeholder="Paste the key" value={key} onChange={(e) => setKey(e.target.value)} />
          <button type="button" className={btn} onClick={save}>Save</button>
        </span>
      ) : (
        <span className="flex gap-2 items-center">
          {has ? <button type="button" className={btn} onClick={() => window.dispatchEvent(new Event("gx-sync-now"))}>Sync now</button> : null}
          <button type="button" className={btn} onClick={() => (has ? off() : setEdit(true))}>{has ? "Turn off" : "Turn on"}</button>
        </span>
      )}
    </div>
  );
}

'''


def change(t):
    t = lit(t, "073: sync code", ROOT, SYNC + ROOT, "change 073: settings sync")
    t = lit(t, "073: sync in app", "<GxBest s={s} setS={setS} />", "<GxBest s={s} setS={setS} /><GxSync s={s} setS={setS} />{/* gx073-app */}", "gx073-app")
    t = lit(t, "073: setup row", '<div className="gx-sr"><span>Week on screen</span>', '<GxSyncRow />{/* gx073-row */}<div className="gx-sr"><span>Week on screen</span>', "gx073-row")
    for must in ("function App(", "function Today(", "function SetupPage(", "function GxSync("):
        if must not in t:
            fail("fantasy-gm.html looks damaged after change 073 (" + must + ").")
    return t


edit(APP, change)
