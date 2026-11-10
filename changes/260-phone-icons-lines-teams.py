# changes/260-phone-icons-lines-teams.py - phone player screen: icon buttons (Simulate, Trade, ESPN, Watch, Hide, Injury alerts), no Simulate on rostered players; phone Lines: all-teams grid opens and closes

NEW_CSS = r'''  /* change 260 (install.py) */
  .gx-pdm .ic260 { display: none; }
  @media (max-width: 640px) {
    .gx-pdm .bt { display: none !important; }
    .gx-pdm .ic260 { position: relative; display: flex; gap: 6px; margin: 12px 0 2px; }
    .gx-pdm .ic260 button { flex: 1 1 0; min-width: 0; max-width: 76px; height: 54px; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 4px; border-radius: 12px; background: rgba(0,0,0,.5); border: 1px solid rgba(255,255,255,.22); color: #fff; font-size: 10.5px; font-weight: 600; line-height: 1; white-space: nowrap; }
    .gx-pdm .ic260 button svg { width: 20px; height: 20px; flex: none; }
    .gx-pdm .ic260 button.pr { background: #fff; color: #111; border-color: #fff; }
    .gx-pdm .ic260 button.on { background: rgba(255,255,255,.2); border-color: rgba(255,255,255,.6); }
    .gx-ln111 .tg260 { display: flex; align-items: center; gap: 8px; width: 100%; height: 40px; padding: 0 12px; margin-bottom: 8px; border-radius: 10px; border: 1px solid var(--line); background: var(--card); color: var(--ink); font-size: 13.5px; font-weight: 600; }
    .gx-ln111 .tg260 .sp { flex: 1; }
    .gx-ln111 .tg260 .cv { color: var(--mute); font-size: 12px; transition: transform .2s ease; }
    .gx-ln111 .tg260.op .cv { transform: rotate(180deg); }
    .gx-ln111 .at237.cl260 { display: none; }
    .gx-ln111 .at237.op260 { animation: gx260in .2s ease; }
    @keyframes gx260in { from { opacity: 0; transform: translateY(-6px); } to { opacity: 1; transform: none; } }
  }
  .gx-ln111 .tg260 { display: none; }
  @media (max-width: 640px) { .gx-ln111 .tg260 { display: flex; } }
  @media (prefers-reduced-motion: reduce) { .gx-ln111 .at237.op260 { animation: none; } .gx-ln111 .tg260 .cv { transition: none; } }
</style>'''

HELPERS = r'''// ---------- change 260: phone player screen icon buttons (install.py) ----------
const GX_IC260 = {
  sim: <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M7 7h11l-3-3M17 17H6l3 3" /></svg>,
  trade: <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M4 9h13M13 5l4 4-4 4M20 15H7M11 11l-4 4 4 4" /></svg>,
  add: <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round"><circle cx="12" cy="12" r="9" /><path d="M12 8v8M8 12h8" /></svg>,
  open: <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M14 4h6v6M20 4l-9 9M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5" /></svg>,
  star: (on) => <svg viewBox="0 0 24 24" fill={on ? "currentColor" : "none"} stroke="currentColor" strokeWidth="2" strokeLinejoin="round"><path d="M12 3.5l2.6 5.3 5.8.8-4.2 4.1 1 5.8L12 16.8l-5.2 2.7 1-5.8-4.2-4.1 5.8-.8z" /></svg>,
  hide: (on) => on
    ? <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round"><path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12z" /><circle cx="12" cy="12" r="3" /></svg>
    : <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round"><path d="M3 3l18 18M10.6 5.1A9.7 9.7 0 0 1 12 5c6.4 0 10 7 10 7a17 17 0 0 1-3.3 4.2M6.6 6.6C3.8 8.4 2 12 2 12s3.6 7 10 7a9.4 9.4 0 0 0 4.4-1.1M9.9 9.9a3 3 0 0 0 4.2 4.2" /></svg>,
  bell: (on) => <svg viewBox="0 0 24 24" fill={on ? "currentColor" : "none"} stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M18 16V11a6 6 0 0 0-12 0v5l-2 2h16zM10 21h4" /></svg>,
};
function GxPdIcons260({ p, Q, act, close101 }) {
  const [, tick] = useState(0);
  useEffect(() => { const h = () => tick((x) => x + 1); window.addEventListener("gx-rw258", h); window.addEventListener("gm-watch", h); return () => { window.removeEventListener("gx-rw258", h); window.removeEventListener("gm-watch", h); }; }, []);
  if (!Q || !p) return null;
  const fa = Q.fa(p), other = !fa && !Q.mine(p);
  const rw = gxRw258.has(p), hurt = p.status && String(p.status).toUpperCase() !== "ACTIVE";
  const wt = Q.starred(p), hid = gxHideSet().has(p.id);
  const B = (k, ic, label, fn, cls) => <button key={k} type="button" className={cls || ""} aria-label={label} onClick={fn}>{ic}<span>{label}</span></button>;
  const list = [];
  if (fa) list.push(B("sim", GX_IC260.sim, "Simulate", act(Q.sim), "pr"));
  if (!fa) list.push(B("trade", GX_IC260.trade, "Trade", act(Q.trade), "pr")); /* own players too (Kuvar) */
  list.push(B("espn", fa ? GX_IC260.add : GX_IC260.open, fa ? "Add" : "ESPN", () => Q.espn(p)));
  if (fa) list.push(B("watch", GX_IC260.star(wt), wt ? "Watching" : "Watch", () => { Q.star(p); tick((x) => x + 1); }, wt ? "on" : ""));
  if (fa) list.push(B("hide", GX_IC260.hide(hid), hid ? "Show" : "Hide", () => { gxHide.toggle(p.id); close101(); }));
  if (rw || hurt) list.push(B("inj", GX_IC260.bell(rw), rw ? "Alerts on" : "Injury", () => gxRw258.toggle(p), rw ? "on" : ""));
  return <div className="ic260" data-gx="260">{list}</div>;
}
// ---------- change 260: phone Lines, open and close the all-teams grid (remembered on the device) ----------
function GxTeamsTog260({ t, open, set }) {
  return (
    <button type="button" className={"tg260" + (open ? " op" : "")} data-gx="260l" aria-expanded={open} onClick={() => set(!open)}>
      {t ? <TeamLogo t={t} size={22} /> : null}<span>{open ? "Hide teams" : "All teams"}</span><span className="sp"></span><span className="cv">{"\u25be"}</span>
    </button>
  );
}
'''

def change(t):
    t = lit(t, "260: styles", "</style>", NEW_CSS, "change 260 (install.py)")
    t = lit(t, "260: helpers", ROOT, HELPERS + ROOT, "change 260: phone player screen icon buttons")
    t = lit(t, "260: icons row", '          <div className="strip">', '          <GxPdIcons260 p={p} Q={Q} act={act} close101={close101} />\n          <div className="strip">', "<GxPdIcons260 p={p} Q={Q} act={act} close101={close101} />")
    t = lit(t, "260: lines toggle",
            '      <div className="at237" data-gx="237a">',
            '      <div className={"at237" + (tg260 ? " op260" : " cl260")} data-gx="237a">',
            '<GxTeamsTog260 t={t} open={tg260}')
    t = lit(t, "260: teams button above search",
            '    <div className="gx-ln111">\n      <div className="srch">',
            '    <div className="gx-ln111">\n      <GxTeamsTog260 t={t} open={tg260} set={(v) => { setTg260(v); uiSet("ln260", v ? "o" : "c"); }} />\n      <div className="srch">',
            '<GxTeamsTog260 t={t} open={tg260} set=')
    t = lit(t, "260: lines toggle state",
            '  const [t, setT] = useState(() => window.__LINES_TEAM || uiGet().ln111fav || uiGet().ln111 || "");\n',
            '  const [t, setT] = useState(() => window.__LINES_TEAM || uiGet().ln111fav || uiGet().ln111 || "");\n  const [tg260, setTg260] = useState(() => uiGet().ln260 === "o"); /* change 260: teams grid open */\n',
            "/* change 260: teams grid open */")
    return t

edit(APP, change)
