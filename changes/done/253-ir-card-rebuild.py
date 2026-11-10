# changes/253-ir-card-rebuild.py - Back from IR card rebuilt: one clear best move, drops picked by rest of season, tap any option, ESPN steps

NEW_CSS = r'''  /* change 253 (install.py) */
  .gx-ir253 { margin-top: 12px; }
  .gx-ir253 .pl { display: flex; align-items: center; gap: 10px; min-height: 52px; border-top: 1px solid var(--line); }
  .gx-ir253 .pl:first-of-type { border-top: 0; }
  .gx-ir253 .pl .nm { flex: 1; min-width: 0; }
  .gx-ir253 .pl .nm b { display: block; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .gx-ir253 .pl .nm small { display: block; font-size: 12px; color: var(--mute); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .gx-ir253 .bt { flex: none; min-height: 38px; padding: 0 14px; border-radius: 10px; border: 1px solid var(--line2); background: var(--card3, var(--card2)); color: var(--ink); font-weight: 600; font-size: 14px; }
  .gx-ir253 .op { padding: 2px 0 10px; max-width: 640px; }
  .gx-ir253 .plan { margin-top: 6px; padding: 12px; border-radius: 12px; background: var(--card3, var(--hover)); border: 1px solid var(--line2); }
  .gx-ir253 .plan .k { font-size: 11px; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; color: var(--mute); }
  .gx-ir253 .plan .t { margin-top: 4px; font-size: 16px; font-weight: 600; color: var(--ink); }
  .gx-ir253 .plan .nums { display: grid; grid-template-columns: repeat(2, minmax(0,1fr)); gap: 8px; margin-top: 10px; }
  .gx-ir253 .plan .nums div { font-size: 11px; color: var(--mute); min-width: 0; }
  .gx-ir253 .plan .nums b { display: block; font-size: 14px; font-weight: 600; color: var(--ink); font-variant-numeric: tabular-nums; white-space: nowrap; }
  .gx-ir253 .plan ol { list-style: decimal; margin: 10px 0 0; padding: 0 0 0 20px; font-size: 13px; color: var(--ink2); line-height: 1.45; }
  .gx-ir253 .plan ol li + li { margin-top: 3px; }
  .gx-ir253 .plan .bts { display: flex; gap: 8px; margin-top: 12px; }
  .gx-ir253 .plan .bts .bt { flex: 1; }
  .gx-ir253 .gt { font-size: 11px; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; color: var(--mute); margin: 14px 0 2px; }
  .gx-ir253 .r { display: grid; grid-template-columns: 34px minmax(0,1fr) 64px 56px; gap: 8px; align-items: center; width: 100%; min-height: 48px; padding: 0 6px; border: 0; border-top: 1px solid var(--line); background: none; color: var(--ink); text-align: left; font-size: 13px; }
  .gx-ir253 .r.on { background: var(--hover); border-radius: 8px; box-shadow: inset 0 0 0 1px var(--line2); }
  .gx-ir253 .r .nn { min-width: 0; }
  .gx-ir253 .r .nn b { display: block; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .gx-ir253 .r .nn small { display: block; font-size: 11.5px; color: var(--mute); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .gx-ir253 .r .n { text-align: right; font-variant-numeric: tabular-nums; white-space: nowrap; }
  .gx-ir253 .r .n small { display: block; font-size: 10.5px; color: var(--mute); }
  .gx-ir253 .nt { font-size: 12px; color: var(--mute); margin: 4px 0 2px; }
  .gx-ir253 .mo253 { display: block; width: 100%; margin-top: 12px; }
  .gx-ir253 .cp { font-size: 12px; color: var(--mute); margin-top: 8px; }
</style>'''

HELPERS = r'''// ---------- change 253: Back from IR card rebuilt (install.py) ----------
// drops ranked by rest-of-season points first (never protected players, keeps position minimums),
// this week's win chance breaks ties between players within 10 points; tap any option to make it the plan
function GxIrBack253({ s }) {
  const today = todayISO(), gen = (window.ESPN_DATA || {}).generated;
  const mine = useMemo(() => s.players.filter((p) => p.ft === s.me), [s.players, s.me]);
  const back = mine.map((p) => ({ p, w: gxSoon244(p, today) })).filter((x) => x.w);
  const [open, setOpen] = useState(null);
  const [calc, setCalc] = useState(null);
  const [pick, setPick] = useState(null);
  const [cp, setCp] = useState("");
  const [more, setMore] = useState(false);
  useEffect(() => {
    setCalc(null); setPick(null); setCp(""); setMore(false);
    if (!open) return undefined;
    const P = mine.find((p) => p.id === open);
    if (!P) return undefined;
    let dead = false;
    const id = setTimeout(() => {
      try {
        const M = computeMoves(s, { H: 0, q: "\u0000" });
        const ros = (q) => M.rawPts(q);
        const on = mine.map((q) => (q.id === P.id ? { ...q, ir: false } : q));
        const base = winChance(s);
        const irOpts = mine.filter((q) => !q.ir && q.id !== P.id && OUTS.includes(String(q.status || "").toUpperCase()))
          .map((q) => ({ k: "ir", q, ros: ros(q), w: winChance(s, on.map((r) => (r.id === q.id ? { ...r, ir: true } : r))) }))
          .sort((a, b) => (b.w || 0) - (a.w || 0));
        const okMin = (q) => q.p === P.p || M.cnt[q.p] - 1 >= M.mins[q.p];
        const cand = mine.filter((q) => !q.ir && q.id !== P.id && !irOpts.some((o) => o.q.id === q.id) && !M.protectedIds.has(q.id) && okMin(q))
          .map((q) => ({ q, ros: ros(q) })).sort((a, b) => a.ros - b.ros).slice(0, 6)
          .map((o) => ({ k: "drop", ...o, w: winChance(s, on.filter((r) => r.id !== o.q.id)) }));
        const drops = cand.sort((a, b) => Math.floor(a.ros / 10) - Math.floor(b.ros / 10) || (b.w || 0) - (a.w || 0)).slice(0, 3);
        const stash = irOpts.length ? [] : s.players.filter((q) => q.ft === "fa" && ["OUT", "INJURY_RESERVE"].includes(String(q.status || "").toUpperCase()))
          .sort((a, b) => gxPgAvg(b, s.blend) - gxPgAvg(a, s.blend)).slice(0, 4);
        if (!dead) setCalc({ P, base, rosP: ros({ ...P, ir: false }), irOpts, drops, stash });
      } catch (e) { if (!dead) setCalc({ err: true }); }
    }, 60);
    return () => { dead = true; clearTimeout(id); };
  }, [open, gen, mine]);
  if (!back.length) return null;
  const wp = (x) => (x == null ? "\u2013" : Math.round(x * 100) + "%");
  const col = () => ""; /* plain colours (Kuvar, Nov 9) */
  const openP = (p) => { if (window.__NAV) window.__NAV.player(p); };
  const lid = (window.ESPN_DATA || {}).leagueId || 1363781006, tid = String(s.me).replace(/\D/g, "");
  const goEspn = (add, name) => {
    let ok = false;
    try { if (name && navigator.clipboard) { navigator.clipboard.writeText(name); ok = true; } } catch (e) {}
    setCp(name && ok ? name + "'s name is copied. Paste it in ESPN's search." : "");
    window.open(add ? "https://fantasy.espn.com/hockey/players/add?leagueId=" + lid + "&teamId=" + tid : "https://fantasy.espn.com/hockey/team?leagueId=" + lid + "&teamId=" + tid, "_blank");
  };
  const body = (P) => {
    if (!calc) return <div className="text-xs text-slate-500" style={{ padding: "8px 0" }}>Working out your options...</div>;
    if (calc.err) return <div className="text-xs text-slate-500" style={{ padding: "8px 0" }}>Could not work this out right now.</div>;
    const all = [...calc.irOpts, ...calc.drops];
    const best = all[0];
    const plan = pick ? (pick.k === "stash" ? { ...pick, d: pick.d || calc.drops[0] } : pick) : best;
    if (!plan) return <div className="text-sm text-slate-500" style={{ padding: "8px 0" }}>Every player you could drop is protected or needed for your minimums. Change Pickup rules in Setup to free someone up.</div>;
    const ln = lastN(P.n);
    const dq = plan.k === "stash" ? plan.d.q : plan.q;
    const title = plan.k === "ir" ? "Move " + plan.q.n + " to IR" : plan.k === "drop" ? "Drop " + plan.q.n : "Drop " + dq.n + ", stash " + plan.f.n;
    const steps = plan.k === "ir"
      ? ["Move " + plan.q.n + " to the IR spot.", "Move " + ln + " from IR to your bench or lineup."]
      : plan.k === "drop"
        ? ["Drop " + plan.q.n + ".", "Move " + ln + " from IR to your bench or lineup."]
        : ["Drop " + dq.n + ".", "Move " + ln + " from IR to your bench or lineup.", "Add " + plan.f.n + " from free agents.", "Move " + lastN(plan.f.n) + " to the IR spot."];
    const w = plan.k === "stash" ? plan.d.w : plan.w;
    const lose = plan.k === "ir" ? 0 : plan.k === "stash" ? plan.d.ros : plan.ros;
    const isBest = plan === best;
    const row = (o, sub) => (
      <button key={o.k + o.q.id} type="button" className={"r" + (plan.k === o.k && plan.q && plan.q.id === o.q.id ? " on" : "")} onClick={() => { setPick(o); setCp(""); }}>
        <GxFace p={o.q} size={26} />
        <span className="nn"><b>{o.q.n}</b><small>{sub}</small></span>
        <span className="n">{o.k === "ir" ? "none" : "\u2212" + Math.round(o.ros)}<small>season pts</small></span>
        <span className="n" style={{ color: col(o.w, calc.base) }}>{wp(o.w)}<small>win wk</small></span>
      </button>
    );
    return (
      <>
        <div className="plan">
          <div className="k">{isBest ? "Best move" : "Your pick"}</div>
          <div className="t">{title}</div>
          <div className="nums">
            <div>Win this week<b><span style={{ color: "var(--mute)", fontWeight: 400 }}>{wp(calc.base) + " \u2192 "}</span><span style={{ color: col(w, calc.base) }}>{wp(w)}</span></b></div>
            <div>Rest of season you give up<b>{plan.k === "ir" ? "Nothing" : Math.round(lose) + " pts"}</b></div>
          </div>
          <ol>{steps.map((t, i) => <li key={i}>{t}</li>)}</ol>
          <div className="bts">
            <button type="button" className="bt" onClick={() => goEspn(false, plan.k === "stash" ? null : (plan.q || {}).n)}>Open my ESPN team</button>
            {plan.k === "stash" ? <button type="button" className="bt" onClick={() => goEspn(true, plan.f.n)}>Open ESPN free agents</button> : null}
          </div>
          {cp ? <div className="cp">{cp}</div> : null}
        </div>
        {!more ? <button type="button" className="bt mo253" onClick={() => setMore(true)}>Show other options</button> : <>
        {calc.irOpts.length ? <div className="gt">Move to IR instead (no drop)</div> : null}
        {calc.irOpts.map((o) => row(o, o.q.t + " \u00b7 " + o.q.p + " \u00b7 " + String(o.q.status || "").replace(/_/g, " ").toLowerCase() + (o.q.back ? " \u00b7 back " + dayLabel(o.q.back) : "")))}
        {calc.drops.length ? <div className="gt">{calc.irOpts.length ? "Or drop" : "Drop one"}</div> : null}
        {calc.drops.map((o) => row(o, o.q.t + " \u00b7 " + o.q.p + " \u00b7 " + f1(gxPgAvg(o.q, s.blend)) + " pts/g"))}
        {calc.stash.length && calc.drops.length ? (
          <>
            <div className="gt">Or stash an injured free agent</div>
            <div className="nt">{"Drop " + (pick && pick.k === "drop" ? pick.q.n : calc.drops[0].q.n) + " and put one of these in the IR spot " + ln + " leaves."}</div>
            {calc.stash.map((f) => {
              const d = pick && pick.k === "drop" ? pick : pick && pick.k === "stash" ? pick.d : calc.drops[0];
              const o = { k: "stash", q: f, f, d };
              return (
                <button key={"s" + f.id} type="button" className={"r" + (plan.k === "stash" && plan.f.id === f.id ? " on" : "")} onClick={() => { setPick(o); setCp(""); }}>
                  <GxFace p={f} size={26} />
                  <span className="nn"><b>{f.n}</b><small>{f.t + " \u00b7 " + f.p + " \u00b7 " + (String(f.status || "").toUpperCase() === "OUT" ? "out" : "IR") + (f.back && f.back >= today ? " \u00b7 back " + dayLabel(f.back) : "")}</small></span>
                  <span className="n">{f1(gxPgAvg(f, s.blend))}<small>pts/g</small></span>
                  <span className="n" style={{ color: col(d.w, calc.base) }}>{wp(d.w)}<small>win wk</small></span>
                </button>
              );
            })}
          </>
        ) : null}
        <button type="button" className="bt mo253" onClick={() => setMore(false)}>Hide other options</button>
        </>}
      </>
    );
  };
  return (
    <div className="gx-pn gx-ir253" data-gx="253">
      <div className="gx-tag" style={{ marginBottom: 6 }}>Back from IR</div>
      {back.map(({ p, w }) => (
        <React.Fragment key={p.id}>
          <div className="pl">
            <GxFace p={p} size={30} />
            <button type="button" className="nm text-left" onClick={() => openP(p)}><b>{p.n}</b><small>{p.t + " \u00b7 " + p.p + " \u00b7 " + (w.now ? "Ready to come back" : "Back around " + dayLabel(w.d)) + " \u00b7 " + f1(gxPgAvg(p, s.blend)) + " pts/g"}</small></button>
            <button type="button" className="bt" onClick={() => setOpen(open === p.id ? null : p.id)}>{open === p.id ? "Close" : "Make room"}</button>
          </div>
          {open === p.id ? <div className="op">{body(p)}</div> : null}
        </React.Fragment>
      ))}
    </div>
  );
}
'''

def change(t):
    t = lit(t, "253: styles", "</style>", NEW_CSS, "change 253 (install.py)")
    t = lit(t, "253: helpers", ROOT, HELPERS + ROOT, "change 253: Back from IR card rebuilt")
    t = lit(t, "253: use it", "{top103 ? <GxIrBack244 s={s} /> : null}", "{top103 ? <GxIrBack253 s={s} /> : null}", "<GxIrBack253 s={s} />")
    return t

edit(APP, change)
