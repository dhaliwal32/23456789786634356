# changes/244-day-all-and-ir-back.py - Roster box Day side lists every player (no "+N more", scrolls inside the box); Roster page "Back from IR" card: when an IR player is ready or coming back, shows who to move to IR or who to drop, with win chance after each

NEW_CSS = r'''  /* change 244 (install.py): Day side shows all, Back from IR card */
  .gx-bx226 .fc.dy244 { overflow-y: auto; overscroll-behavior: contain; -webkit-overflow-scrolling: touch; }
  .gx-ir244 { margin-top: 12px; }
  .gx-ir244 .hd { display: flex; align-items: center; justify-content: space-between; gap: 8px; margin-bottom: 6px; }
  .gx-ir244 .pl { display: flex; align-items: center; gap: 10px; min-height: 52px; border-top: 1px solid var(--line); }
  .gx-ir244 .pl:first-of-type { border-top: 0; }
  .gx-ir244 .pl .nm { flex: 1; min-width: 0; }
  .gx-ir244 .pl .nm b { display: block; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .gx-ir244 .pl .nm small { display: block; font-size: 12px; color: var(--mute); }
  .gx-ir244 .bt { flex: none; min-height: 38px; padding: 0 14px; border-radius: 10px; border: 1px solid var(--line2); background: var(--card3, var(--card2)); color: var(--ink); font-weight: 600; font-size: 14px; }
  .gx-ir244 .op { padding: 4px 0 10px; max-width: 720px; }
  .gx-ir244 .op .gt { font-size: 11px; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; color: var(--mute); margin: 10px 0 2px; }
  .gx-ir244 .op .r { display: grid; grid-template-columns: auto minmax(0,1fr) 54px 64px; gap: 8px; align-items: center; min-height: 46px; border-top: 1px solid var(--line); font-size: 13px; }
  .gx-ir244 .op .r .nn { min-width: 0; }
  .gx-ir244 .op .r .nn b { display: block; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .gx-ir244 .op .r .nn small { display: block; font-size: 11.5px; color: var(--mute); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .gx-ir244 .op .r .n { text-align: right; font-variant-numeric: tabular-nums; }
  .gx-ir244 .op .r .n small { display: block; font-size: 10.5px; color: var(--mute); }
  .gx-ir244 .op .r.best { background: var(--hover); border-radius: 8px; }
  .gx-ir244 .op .ft { display: flex; align-items: center; justify-content: space-between; gap: 10px; margin-top: 10px; font-size: 13px; color: var(--mute); }
</style>'''

HELPERS = r'''// ---------- change 244: Back from IR, who to move or drop (install.py) ----------
function gxSoon244(p, today) {
  if (!p.ir) return null;
  const st = String(p.status || "").toUpperCase();
  if (!st || st === "ACTIVE" || st === "DAY_TO_DAY") return { now: true };
  if (p.back && p.back <= addDays(today, 7)) return { now: p.back <= today, d: p.back };
  return null;
}
function GxIrBack244({ s }) {
  const today = todayISO(), gen = (window.ESPN_DATA || {}).generated;
  const mine = useMemo(() => s.players.filter((p) => p.ft === s.me), [s.players, s.me]);
  const back = mine.map((p) => ({ p, w: gxSoon244(p, today) })).filter((x) => x.w);
  const [open, setOpen] = useState(null);
  const [calc, setCalc] = useState(null);
  useEffect(() => {
    setCalc(null);
    if (!open) return undefined;
    const P = mine.find((p) => p.id === open);
    if (!P) return undefined;
    let dead = false;
    const id = setTimeout(() => {
      try {
        const on = mine.map((q) => (q.id === P.id ? { ...q, ir: false } : q));
        const pct = (x) => (x == null ? null : x);
        const base = pct(winChance(s));
        const irOpts = mine.filter((q) => !q.ir && q.id !== P.id && OUTS.includes(String(q.status || "").toUpperCase()))
          .map((q) => ({ q, w: pct(winChance(s, on.map((r) => (r.id === q.id ? { ...r, ir: true } : r)))) }));
        const pool = mine.filter((q) => !q.ir && q.id !== P.id && !irOpts.some((o) => o.q.id === q.id)).sort((a, b) => gxPgAvg(a, s.blend) - gxPgAvg(b, s.blend)).slice(0, 8);
        const drops = pool.map((q) => ({ q, v: gxPgAvg(q, s.blend), w: pct(winChance(s, on.filter((r) => r.id !== q.id))) }))
          .sort((a, b) => (b.w || 0) - (a.w || 0) || a.v - b.v).slice(0, 5);
        if (!dead) setCalc({ base, irOpts, drops });
      } catch (e) { if (!dead) setCalc({ err: true }); }
    }, 60);
    return () => { dead = true; clearTimeout(id); };
  }, [open, gen, mine]);
  if (!back.length) return null;
  const wp = (x) => (x == null ? "\u2013" : Math.round(x * 100) + "%");
  const col = (x, b) => (x == null || b == null ? "" : x > b + 0.005 ? "var(--good)" : x < b - 0.005 ? "var(--bad)" : "");
  const openP = (p) => { if (window.__NAV) window.__NAV.player(p); };
  const row = (o, sub, best) => (
    <div key={o.q.id} className={"r" + (best ? " best" : "")}>
      <GxFace p={o.q} size={26} />
      <button type="button" className="nn text-left" onClick={() => openP(o.q)}><b>{o.q.n}</b><small>{sub}</small></button>
      <span className="n">{f1(gxPgAvg(o.q, s.blend))}<small>pts/g</small></span>
      <span className="n" style={{ color: col(o.w, calc && calc.base) }}>{wp(o.w)}<small>win after</small></span>
    </div>
  );
  return (
    <div className="gx-pn gx-ir244" data-gx="244">
      <div className="hd"><span className="gx-tag">Back from IR</span></div>
      {back.map(({ p, w }) => (
        <React.Fragment key={p.id}>
          <div className="pl">
            <GxFace p={p} size={30} />
            <button type="button" className="nm text-left" onClick={() => openP(p)}><b>{p.n}</b><small>{p.t + " \u00b7 " + p.p + " \u00b7 " + (w.now ? "Ready to come back" : "Back around " + dayLabel(w.d)) + " \u00b7 " + f1(gxPgAvg(p, s.blend)) + " pts/g"}</small></button>
            <button type="button" className="bt" onClick={() => setOpen(open === p.id ? null : p.id)}>{open === p.id ? "Close" : "Make room"}</button>
          </div>
          {open === p.id ? (
            <div className="op">
              {!calc ? <div className="text-xs text-slate-500" style={{ padding: "8px 0" }}>Working out your options...</div> : calc.err ? <div className="text-xs text-slate-500">Could not work this out right now.</div> : (
                <>
                  {calc.irOpts.length ? <><div className="gt">Move to IR instead (no drop)</div>{calc.irOpts.map((o, i) => row(o, o.q.t + " \u00b7 " + String(o.q.status || "").replace(/_/g, " ").toLowerCase() + (o.q.back ? " \u00b7 back " + dayLabel(o.q.back) : ""), i === 0))}</> : null}
                  <div className="gt">{calc.irOpts.length ? "Or drop" : "Drop one to make room"}</div>
                  {calc.drops.map((o, i) => row(o, o.q.t + " \u00b7 " + o.q.p, !calc.irOpts.length && i === 0))}
                  <div className="ft"><span>{"Your win chance this week now: " + wp(calc.base)}</span><button type="button" className="bt" onClick={() => window.__QA && window.__QA.espn && window.__QA.espn(p)}>Do it on ESPN</button></div>
                </>
              )}
            </div>
          ) : null}
        </React.Fragment>
      ))}
    </div>
  );
}
'''

def change(t):
    t = lit(t, "244: styles", "</style>", NEW_CSS, "change 244 (install.py)")
    t = lit(t, "244: helpers", ROOT, HELPERS + ROOT, "change 244: Back from IR")
    t = lit(t, "244: Day side scrolls", '  const fToday = (\n    <div className="fc">\n      <div className="ft">\n        <span className="dn230">', '  const fToday = (\n    <div className="fc dy244">\n      <div className="ft">\n        <span className="dn230">', '<div className="fc dy244">')
    t = lit(t, "244: no +N more", '''      {rows.length > 10 ? <div className="text-xs text-slate-500" style={{ marginTop: 4 }}>{"+" + (rows.length - 10) + " more"}</div> : null}\n''', "", '/* change 244: everyone */')
    t = lit(t, "244: Day side shows everyone", "      {rows.slice(0, 10).map(({ q, v, real, g }) => (", "      {rows.map(({ q, v, real, g }) => ( /* change 244: everyone */", "/* change 244: everyone */")
    t = lit(t, "244: card on Roster", "{top103 ? <GxBox230 s={s} wk={wk} /> : <GxRace s={s} wk={wk} />}", "{top103 ? <GxBox230 s={s} wk={wk} /> : <GxRace s={s} wk={wk} />}{top103 ? <GxIrBack244 s={s} /> : null}", "<GxIrBack244 s={s} />")
    return t

edit(APP, change)
