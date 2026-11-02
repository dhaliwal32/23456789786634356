# changes/195-more-details.py - More details in Simulate and Trades is more useful: points gained This week / Next 4 weeks / Rest of season / Playoffs, a points-by-week bar strip (green gain, red loss) for every remaining week, a players in vs out table (expected per game, season average, last 15 days average, games this week / next 4 weeks / rest of season, status), and in Trades the same win-chance-by-week cards as Simulate

HELPERS = r'''// ---------- change 195: more useful More details for Simulate and Trades (install.py) ----------
function gxGms195(s, p, a, b) {
  let g = 0;
  for (let i = a; i < b && i < s.weeks.length; i++) {
    const w = deriveWeek(s.weeks[i], s.autoDone), st = i === s.wk ? w.done || 0 : 0;
    (w.games[p.t] || []).forEach((d) => { const dt = w.dates ? w.dates[d] : null; if (d >= st && !p.ir && avail(p, dt) > 0) g++; });
  }
  return g;
}
function gxAvg195(p, s, rng) {
  const v = gxVals106(p, s, rng), fp = parseFloat(v[0]), gp = parseFloat(v[1]);
  return !isNaN(fp) && gp > 0 ? f1(fp / gp) : gp === 0 ? "-" : "...";
}
function GxMore195({ s, before, after, ins, outs, weeks }) {
  gxUse100();
  useEffect(() => { gxLoad100("l15"); gxLoad100("sea"); }, []);
  const K = s.blend, end = s.weeks.length;
  const pw = useMemo(() => {
    const out = [];
    for (let i = s.wk; i < end; i++) {
      const w = deriveWeek(s.weeks[i], s.autoDone), fr = i === s.wk ? w.done || 0 : 0;
      let d = 0;
      try { d = weekProj(after, w, K, fr).total - weekProj(before, w, K, fr).total; } catch (e) {}
      out.push({ i, opp: oppOf(s.weeks[i] || {}, s.me), d, wl: String((s.weeks[i] || {}).label || "Week " + (i + 1)).split(" \u00b7 ")[0].replace("Week ", "W") });
    }
    return out;
  }, [s, before, after]);
  const lastReg = pw.reduce((m, x) => (x.opp ? x.i : m), -1);
  const sum = (L) => L.reduce((t, x) => t + x.d, 0);
  const po = pw.filter((x) => x.i > lastReg && !x.opp);
  const tiles = [["This week", sum(pw.slice(0, 1))], ["Next 4 weeks", sum(pw.slice(0, 4))], ["Rest of season", sum(pw)]].concat(po.length ? [["Playoffs", sum(po)]] : []);
  const mx = Math.max(1, ...pw.map((x) => Math.abs(x.d)));
  const wb = useMemo(() => (weeks ? gxWkWins194(s, before) : []), [s, before, !!weeks]);
  const wa = useMemo(() => (weeks ? gxWkWins194(s, after) : []), [s, after, !!weeks]);
  const sg = (v) => (v >= 0 ? "+" : "") + f1(v);
  const row = (p, kind) => {
    const st = p.ir ? "IR" : p.status && p.status !== "ACTIVE" ? M_ST[p.status] || String(p.status).replace(/_/g, " ") : "";
    return (
      <div key={kind + p.id} className="tr195">
        <span className="pc195"><i className={kind}>{kind === "in" ? "IN" : "OUT"}</i><GxFace p={p} size={22} /><span className="nm">{p.n}<small>{p.p + " \u00b7 " + p.t}</small></span></span>
        <span className="n b">{f1(gxPgAvg(p, K))}</span>
        <span className="n">{p.gp ? f1(p.tot / p.gp) : "-"}</span>
        <span className="n">{gxAvg195(p, s, "l15")}</span>
        <span className="n">{gxGms195(s, p, s.wk, s.wk + 1)}</span>
        <span className="n">{gxGms195(s, p, s.wk, s.wk + 4)}</span>
        <span className="n">{gxGms195(s, p, s.wk, end)}</span>
        <span className="n st" style={{ color: st ? "var(--bad)" : "var(--mute)" }}>{st || "OK"}</span>
      </div>
    );
  };
  return (
    <div className="gx-mo195">
      <div className="sec195">Points you gain</div>
      <div className="tl195">
        {tiles.map(([l, v]) => <div key={l}><small>{l}</small><b style={{ color: v > 0.05 ? "var(--good)" : v < -0.05 ? "var(--bad)" : "var(--ink)" }}>{sg(v)}</b></div>)}
      </div>
      <div className="sec195">Points by week</div>
      <div className="br195">
        {pw.map((x) => (
          <div key={x.i} className={"c" + (x.opp ? "" : " po")} title={x.wl + ": " + sg(x.d)}>
            <span className="v" style={{ color: x.d > 0.05 ? "var(--good)" : x.d < -0.05 ? "var(--bad)" : "var(--mute)" }}>{Math.abs(x.d) < 0.05 ? "0" : sg(x.d)}</span>
            <span className="bx"><i style={{ height: Math.max(2, Math.round((Math.abs(x.d) / mx) * 44)) + "px", background: x.d >= 0 ? "var(--good)" : "var(--bad)", opacity: Math.abs(x.d) < 0.05 ? 0.25 : 1 }}></i></span>
            <span className="w">{x.wl}</span>
          </div>
        ))}
      </div>
      {po.length ? <div className="nt195">Shaded weeks are playoff weeks.</div> : null}
      <div className="sec195">Players in and out</div>
      <div className="tb195">
        <div className="tr195 hd"><span className="pc195">Player</span><span className="n">Exp</span><span className="n">Avg</span><span className="n">L15</span><span className="n">This wk</span><span className="n">Next 4</span><span className="n">Rest</span><span className="n st">Status</span></div>
        {(ins || []).filter(Boolean).map((p) => row(p, "in"))}
        {(outs || []).filter(Boolean).map((p) => row(p, "out"))}
      </div>
      <div className="nt195">Exp = expected points a game. Avg = season average, L15 = last 15 days. Games columns count games left.</div>
      {weeks && wb.length ? <div className="gx-sw194 ro195"><GxSimWeeks194 s={s} before={wb} after={wa} sel={[]} onW={null} /></div> : null}
    </div>
  );
}
'''

OLD_SIM = r'''{det ? <GxPickRes92 s={s} myR={myR} ok={[{ a, d }]} /> : null}'''
NEW_SIM = r'''{det ? <GxMore195 s={s} before={myR} after={rosterOn(pick)} ins={[a]} outs={[d]} /> : null}{det ? <GxPickRes92 s={s} myR={myR} ok={[{ a, d }]} /> : null}'''

OLD_TR = r'''          {det110 && res.mode82 ? <GxTradeModes82 res={res} cmp={cmp82} tm={tm82} setTm={setTm82} /> : null}'''
NEW_TR = r'''          {det110 && res.mode82 ? <GxTradeModes82 res={res} cmp={cmp82} tm={tm82} setTm={setTm82} /> : null}
          {det110 && res.meL && res.myL ? <GxMore195 s={s} before={res.meL} after={res.myL} ins={[...Rv, ...picks.filter(Boolean)]} outs={[...Gv, ...drops]} weeks /> : null}'''

NEW_CSS = r'''  /* change 195 (install.py) */
  .gx-mo195 { margin-top: 14px; }
  .gx-mo195 .sec195 { font-size: 12px; letter-spacing: .06em; text-transform: uppercase; color: var(--mute); margin: 14px 0 8px; }
  .gx-mo195 .tl195 { display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 8px; }
  .gx-mo195 .tl195 > div { border: 1px solid var(--line); border-radius: 12px; padding: 10px 12px; height: 66px; min-width: 0; }
  .gx-mo195 .tl195 small { display: block; font-size: 12px; color: var(--mute); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .gx-mo195 .tl195 b { display: block; font-size: 22px; font-variant-numeric: tabular-nums; margin-top: 2px; }
  .gx-mo195 .br195 { display: flex; gap: 4px; overflow-x: auto; padding-bottom: 4px; overscroll-behavior-x: contain; }
  .gx-mo195 .br195 .c { flex: 0 0 40px; display: grid; grid-template-rows: 16px 48px 16px; justify-items: center; border-radius: 6px; padding: 4px 0; }
  .gx-mo195 .br195 .c.po { background: var(--card3, var(--card2)); }
  .gx-mo195 .br195 .v { font-size: 10.5px; font-variant-numeric: tabular-nums; white-space: nowrap; }
  .gx-mo195 .br195 .bx { display: flex; align-items: flex-end; height: 48px; }
  .gx-mo195 .br195 .bx i { display: block; width: 14px; border-radius: 3px 3px 0 0; }
  .gx-mo195 .br195 .w { font-size: 11px; color: var(--mute); }
  .gx-mo195 .nt195 { font-size: 12px; color: var(--mute); margin-top: 6px; }
  .gx-mo195 .tb195 { overflow-x: auto; overscroll-behavior-x: contain; }
  .gx-mo195 .tr195 { display: grid; grid-template-columns: 220px repeat(6, 56px) 64px; align-items: center; min-width: max-content; height: 48px; border-top: 1px solid var(--line); }
  .gx-mo195 .tr195.hd { height: 30px; border-top: 0; font-size: 12px; color: var(--mute); }
  .gx-mo195 .tr195 .pc195 { display: flex; align-items: center; gap: 8px; min-width: 0; overflow: hidden; position: sticky; left: 0; background: var(--card); height: 100%; z-index: 1; }
  .gx-mo195 .tr195 .pc195 i { flex: none; font-style: normal; font-size: 10px; font-weight: 700; width: 32px; text-align: center; border-radius: 99px; padding: 1px 0; color: #fff; }
  .gx-mo195 .tr195 .pc195 i.in { background: var(--good); }
  .gx-mo195 .tr195 .pc195 i.out { background: var(--bad); }
  .gx-mo195 .tr195 .nm { min-width: 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; font-size: 14px; }
  .gx-mo195 .tr195 .nm small { margin-left: 6px; font-size: 12px; color: var(--mute); }
  .gx-mo195 .tr195 .n { text-align: right; padding-right: 8px; font-size: 13px; font-variant-numeric: tabular-nums; white-space: nowrap; color: var(--mute); }
  .gx-mo195 .tr195 .n.b { color: var(--ink); font-weight: 600; }
  .gx-mo195 .tr195.hd .n { color: var(--mute); font-weight: 400; }
  .gx-mo195 .tr195 .n.st { text-align: right; }
  .gx-mo195 .ro195 .sec { font-size: 12px; letter-spacing: .06em; text-transform: uppercase; color: var(--mute); margin: 14px 0 8px; font-weight: 400; }
  .gx-mo195 .ro195 .wc { cursor: default; }
  .gx-mo195 .ro195 .nt { display: none; }
  @media (max-width: 640px) {
    .gx-mo195 .tr195 { grid-template-columns: 176px repeat(6, 46px) 54px; }
    .gx-mo195 .tr195 .pc195 { gap: 6px; }
    .gx-mo195 .tr195 .pc195 i { width: 30px; }
    .gx-mo195 .tr195 .nm small { display: none; }
  }
</style>'''


def change(t):
    t = lit(t, "195: styles", "</style>", NEW_CSS, "change 195 (install.py)")
    t = lit(t, "195: helpers", ROOT, HELPERS + ROOT, "change 195: more useful More details")
    t = lit(t, "195: Simulate details", OLD_SIM, NEW_SIM, "<GxMore195 s={s} before={myR}")
    t = lit(t, "195: Trades details", OLD_TR, NEW_TR, "<GxMore195 s={s} before={res.meL}")
    return t


edit(APP, change)
