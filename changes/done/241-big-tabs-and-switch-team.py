# changes/241-big-tabs-and-switch-team.py - Phone: 4 big main tabs plus a More menu (Trades, League, Setup); Setup > Display: view the app as any fantasy team

NEW_CSS = r'''  /* change 241 (install.py): big phone tabs, More menu, view as another team */
  .gx-tm103 .mr241 { display: none; }
  @media (max-width: 640px) {
    .gx-tm103 .tb a.sd241 { display: none; }
    .gx-tm103 .tb a, .gx-tm103 .tb .mr241 { flex: 1 1 auto; padding: 14px 3px 11px; font-size: clamp(12px, 3.5vw, 14px); letter-spacing: 0; }
    .gx-tm103 .tb .mr241 { display: flex; align-items: center; justify-content: center; gap: 3px; font-weight: 700; text-transform: uppercase; color: var(--mute); border-bottom: 3px solid transparent; white-space: nowrap; }
    .gx-tm103 .tb .mr241.on { color: var(--ink); border-bottom-color: var(--accent); }
    .gx-tm103 .tb .mr241 svg { width: 12px; height: 12px; flex: none; }
  }
  .gx-mm241 { position: fixed; inset: 0; z-index: 80; }
  .gx-mm241 .bg { position: absolute; inset: 0; background: rgba(0,0,0,.35); }
  .gx-mm241 .pn { position: absolute; right: 8px; min-width: 200px; background: var(--card); border: 1px solid var(--line2); border-radius: 14px; padding: 6px; box-shadow: 0 12px 30px rgba(0,0,0,.5); animation: gx-mm241 .16s ease-out; }
  .gx-mm241 .pn a { display: flex; align-items: center; min-height: 48px; padding: 0 14px; border-radius: 10px; font-size: 16px; font-weight: 600; color: var(--ink); }
  .gx-mm241 .pn a.on { background: var(--card3, var(--card2)); }
  .gx-mm241 .pn a:active { background: var(--hover); }
  @keyframes gx-mm241 { from { opacity: 0; transform: translateY(-6px); } to { opacity: 1; transform: none; } }
  .gx-as241 { display: flex; align-items: center; gap: 10px; margin-bottom: 10px; padding: 8px 12px; border-radius: 12px; background: var(--card); border: 1px solid var(--line2); font-size: 13px; color: var(--ink2); }
  .gx-as241 b { color: var(--ink); }
  .gx-as241 button { margin-left: auto; flex: none; padding: 6px 12px; border-radius: 9px; border: 1px solid var(--line2); background: var(--card3, var(--card2)); color: var(--ink); font-weight: 600; font-size: 13px; }
</style>'''

HELPERS = r'''// ---------- change 241: More menu for the phone tabs, view as another team (install.py) ----------
const GX_MAIN241 = ["roster", "matchup", "players", "lines"];
function GxMore241({ tab, go }) {
  const [open, setOpen] = useState(false);
  const [top, setTop] = useState(60);
  const ref = React.useRef(null);
  const side = GX_TABS103.filter((x) => !GX_MAIN241.includes(x[0]));
  const cur = side.find((x) => gxTabOn103(x[0], tab));
  useEffect(() => { setOpen(false); }, [tab, (window.__ROUTE || {}).sub]);
  useEffect(() => { if (!open) return undefined; const k = (e) => { if (e.key === "Escape") setOpen(false); }; window.addEventListener("keydown", k); return () => window.removeEventListener("keydown", k); }, [open]);
  const tap = () => { const r = ref.current && ref.current.getBoundingClientRect(); if (r) setTop(r.bottom + 6); setOpen((o) => !o); };
  return (
    <>
      <button ref={ref} type="button" className={"mr241" + (cur ? " on" : "")} data-gx="241" aria-expanded={open} onClick={tap}>
        {cur ? cur[1] : "More"}
        <svg viewBox="0 0 12 12" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round"><path d="M3 4.5l3 3 3-3"></path></svg>
      </button>
      {open ? ReactDOM.createPortal(
        <div className="gx-mm241">
          <div className="bg" onClick={() => setOpen(false)}></div>
          <div className="pn" style={{ top }}>
            {side.map(([k, l, t, sb]) => <a key={k} href={gxHash(t, sb || undefined)} className={cur && cur[0] === k ? "on" : ""} onClick={(e) => { if (gxNewTab(e)) return; e.preventDefault(); setOpen(false); go(t, sb || undefined); }}>{l}</a>)}
          </div>
        </div>, document.body) : null}
    </>
  );
}
function gxMe241(teams, real) {
  const v = uiGet().me241;
  return v && v !== real && (teams || []).some((t) => t.id === v) ? v : real;
}
function gxReal241() { const E = window.ESPN_DATA; return E && E.myTeamId != null ? "t" + E.myTeamId : null; }
function gxSetMe241(id) {
  const real = gxReal241();
  uiSet("me241", !id || id === real ? "" : id);
  try { const v = JSON.parse(localStorage.getItem(KEY) || "null"); if (v) { v.lastSync = null; localStorage.setItem(KEY, JSON.stringify(v)); } } catch (e) {}
  try { location.replace(location.pathname + "?v=" + Date.now() + "#myteam"); } catch (e) { location.reload(); }
}
function GxMeSel241({ s }) {
  const real = gxReal241();
  return (
    <select className={inp} value={s.me} onChange={(e) => gxSetMe241(e.target.value)} data-gx="241s">
      {(s.teams || []).map((t) => <option key={t.id} value={t.id}>{t.name + (t.id === real ? " (yours)" : "")}</option>)}
    </select>
  );
}
function GxAsBar241({ s }) {
  const real = gxReal241();
  if (!real || s.me === real) return null;
  return <div className="gx-as241" data-gx="241b"><span>Viewing as <b>{teamName(s, s.me)}</b></span><button type="button" onClick={() => gxSetMe241(real)}>Back to mine</button></div>;
}
'''

def change(t):
    t = lit(t, "241: styles", "</style>", NEW_CSS, "change 241 (install.py)")
    t = lit(t, "241: helpers", ROOT, HELPERS + ROOT, "change 241: More menu for the phone tabs")
    t = lit(t, "241: side tabs marked, More button",
            '''        {GX_TABS103.map(([k, l, t, sb]) => (
          <a key={k} href={gxHash(t, sb || undefined)} className={(pend213 ? pend213 === k : gxTabOn103(k, tab)) ? "on" : ""} onClick={(e) => { if (gxNewTab(e)) return; e.preventDefault(); setPend213(k); go(t, sb || undefined); }}>{l}</a>
        ))}
''',
            '''        {GX_TABS103.map(([k, l, t, sb]) => (
          <a key={k} href={gxHash(t, sb || undefined)} className={((pend213 ? pend213 === k : gxTabOn103(k, tab)) ? "on" : "") + (GX_MAIN241.includes(k) ? "" : " sd241")} onClick={(e) => { if (gxNewTab(e)) return; e.preventDefault(); setPend213(k); go(t, sb || undefined); }}>{l}</a>
        ))}
        <GxMore241 tab={tab} go={go} />
''',
            '<GxMore241 tab={tab} go={go} />')
    t = lit(t, "241: chosen team used", 'const me = "t" + E.myTeamId;', 'const me = gxMe241(teams, "t" + E.myTeamId); /* change 241 */', 'gxMe241(teams, "t" + E.myTeamId)')
    t = lit(t, "241: Setup row",
            '<div className="gx-sr"><span>Favourite team (Lines)</span><GxFavSel112 /></div>',
            '<div className="gx-sr"><span>My team (view the app as)</span><GxMeSel241 s={s} /></div>\n    <div className="gx-sr"><span>Favourite team (Lines)</span><GxFavSel112 /></div>',
            '<GxMeSel241 s={s} />')
    t = lit(t, "241: viewing-as bar", '<GxSimBar s={s} setS={setS} go={go} />{/* gx086-bar */}', '<GxAsBar241 s={s} /><GxSimBar s={s} setS={setS} go={go} />{/* gx086-bar */}', '<GxAsBar241 s={s} />')
    return t

edit(APP, change)
