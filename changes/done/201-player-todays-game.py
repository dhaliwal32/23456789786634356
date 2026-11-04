# changes/201-player-todays-game.py - player screen: today's live or final game card that opens the NHL scores game view

NEW_CSS = r'''  /* change 201 (install.py) */
  .gx-tg201 { display: grid; grid-template-columns: minmax(0, 1fr) 112px 14px; align-items: center; column-gap: 10px; width: 100%; padding: 10px 14px; margin-bottom: 12px; border: 1px solid var(--line); border-radius: 12px; background: var(--card); text-align: left; cursor: pointer; transition: transform .12s ease; }
  .gx-tg201:active { transform: scale(.985); }
  .gx-tg201 .k { grid-column: 1 / -1; font-size: 11px; letter-spacing: .08em; text-transform: uppercase; color: var(--mute); margin-bottom: 6px; }
  .gx-tg201 .tms { display: flex; flex-direction: column; gap: 6px; min-width: 0; }
  .gx-tg201 .tr { display: grid; grid-template-columns: 24px minmax(0, 1fr) 30px; align-items: center; column-gap: 8px; height: 26px; }
  .gx-tg201 .tr .nm { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; font-size: 15px; color: var(--ink); }
  .gx-tg201 .tr b { text-align: right; font-size: 17px; font-variant-numeric: tabular-nums; color: var(--ink); }
  .gx-tg201 .tr.lo .nm, .gx-tg201 .tr.lo b { color: var(--mute); }
  .gx-tg201 .tr.me .nm { font-weight: 600; }
  .gx-tg201 .st { font-size: 13px; color: var(--mute); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; border-left: 1px solid var(--line); padding-left: 10px; height: 58px; display: flex; align-items: center; }
  .gx-tg201 .st.lv { color: #e5484d; }
  .gx-tg201 .cv { color: var(--mute); font-size: 18px; text-align: right; }
  .gx-pd-t tr.go201 { cursor: pointer; }
</style>'''

HELPERS = r'''// ---------- change 201: today's game on the player screen opens the NHL scores game view (install.py) ----------
function gxGame201(t) {
  const J = window.__NHLNOW || {};
  return (J.games || []).find((g) => gxAb131((g.awayTeam || {}).abbrev) === t || gxAb131((g.homeTeam || {}).abbrev) === t) || null;
}
function gxGs201(g) {
  const st = g ? g.gameState : "";
  return st === "LIVE" || st === "CRIT" ? "L" : st === "FINAL" || st === "OFF" ? "F" : "P";
}
function gxOpen201(id) { try { window.dispatchEvent(new CustomEvent("gx-game201", { detail: { id } })); } catch (e) {} }
function GxTg201({ t }) {
  const [, bump] = useState(0);
  useEffect(() => { const id = setInterval(() => bump((x) => x + 1), 2000); return () => clearInterval(id); }, []);
  useTick159(gxAnyInt159());
  const g = gxGame201(t), k = gxGs201(g);
  if (!g || k === "P") return null;
  const A = g.awayTeam || {}, H = g.homeTeam || {}, aw = +A.score > +H.score, hw = +H.score > +A.score, fin = k === "F";
  const st = k === "L" ? ((g.clock || {}).inIntermission ? gxIntG159(g) : gxPer131(g.periodDescriptor) + " - " + ((g.clock || {}).timeRemaining || "")) : "Final" + (((g.periodDescriptor || {}).periodType || "REG") !== "REG" ? "/" + gxPer131(g.periodDescriptor) : "");
  const row = (T, win, lose) => <div className={"tr" + (fin && lose ? " lo" : "") + (gxAb131(T.abbrev) === t ? " me" : "")}><TeamLogo t={gxAb131(T.abbrev)} size={24} /><span className="nm">{gxNick141(T.abbrev)}</span><b>{T.score == null ? "" : T.score}</b></div>;
  return (
    <button type="button" className="gx-tg201" onClick={() => gxOpen201(g.id)} aria-label="Open this game in NHL scores">
      <div className="k">{k === "L" ? "Today's game, live" : "Today's game"}</div>
      <div className="tms">{row(A, aw, hw)}{row(H, hw, aw)}</div>
      <div className={"st" + (k === "L" ? " lv" : "")}>{st}</div>
      <div className="cv">{"\u203a"}</div>
    </button>
  );
}
'''

ONLY_HOOKS = r'''  // change 201: the copy kept on every page only opens a game from the player screen
  useEffect(() => {
    if (!only201) return undefined;
    const h = (e) => { const id = e && e.detail && e.detail.id; if (!id) return; setGid(id); setGt("game"); setOut(false); setDm144(""); setOpen(true); };
    window.addEventListener("gx-game201", h);
    return () => window.removeEventListener("gx-game201", h);
  }, [only201]);
  useEffect(() => {
    if (!only201 || !open) return undefined;
    const id = setInterval(() => bump((x) => x + 1), 2000);
    return () => clearInterval(id);
  }, [only201, open]);
  if (only201) return open ? GX_SHEET141() : null;
  // ---------- laptop column ----------'''

def change(t):
    t = lit(t, "201: styles", "</style>", NEW_CSS, "change 201 (install.py)")
    t = lit(t, "201: helpers", ROOT, HELPERS + ROOT, "change 201: today's game on the player screen")
    t = lit(t, "201: sheet prop", "function GxNhl141({ s, a, b, tA, tB, side }) {", "function GxNhl141({ s, a, b, tA, tB, side, only201 }) {", "tB, side, only201 })")
    t = lit(t, "201: sheet only", "  // ---------- laptop column ----------", ONLY_HOOKS, "change 201: the copy kept on every page")
    t = lit(t, "201: mount",
            "{player ? <GxPdSafe key={player.id} p={player} s={s} wk={wk} H={LH} onClose={() => setPlayer(null)} /> : null}",
            "{player ? <GxPdSafe key={player.id} p={player} s={s} wk={wk} H={LH} onClose={() => setPlayer(null)} /> : null}<GxNhl141 s={s} a={s.me} b={(wk && oppOf(wk, s.me)) || s.opp} only201 />",
            "only201 />")
    t = lit(t, "201: card", '          {tab === "ov" ? (<>', '          {tab === "ov" ? (<>\n            <GxTg201 t={p.t} />', "<GxTg201 t={p.t} />")
    t = lit(t, "201: today row",
            '<tr key={g.d} className={lv ? "lv" : ""}>',
            '<tr key={g.d} className={(lv ? "lv" : "") + (lv && g.d === todayISO() && gxGame201(p.t) ? " go201" : "")} onClick={lv && g.d === todayISO() && gxGame201(p.t) ? () => gxOpen201(gxGame201(p.t).id) : undefined}>',
            '" go201" : ""')
    return t

edit(APP, change)
