# changes/138-matchup-nhl-cleanup.py - Matchup: NHL scores panel moved to the very bottom, cleaner one-line scoreboard, goal tracker with goal counters at the top (All / Rostered / Yours, tap to filter) and short one-line goal rows

NEW_CSS = r'''  /* change 138 (install.py) */
  .gx-ns131.gx138 { margin-top: 18px; }
  .gx-ns131 .gx-sb138 { margin: 0 12px 10px; }
  .gx-ns131 .gx-sb138 .r { display: grid; grid-template-columns: minmax(0, 1fr) 26px minmax(86px, auto) 26px minmax(0, 1fr); align-items: center; gap: 6px; width: 100%; padding: 9px 2px; border-top: 1px solid var(--line); font-size: 14px; }
  .gx-ns131 .gx-sb138 .r:first-child { border-top: 0; }
  .gx-ns131 .gx-sb138 .t { display: flex; align-items: center; gap: 6px; min-width: 0; font-weight: 600; }
  .gx-ns131 .gx-sb138 .t.h { justify-content: flex-end; }
  .gx-ns131 .gx-sb138 b { font-size: 16px; font-variant-numeric: tabular-nums; text-align: center; color: var(--mute); font-weight: 600; }
  .gx-ns131 .gx-sb138 b.w { color: var(--ink); font-weight: 700; }
  .gx-ns131 .gx-sb138 .st { text-align: center; font-size: 12px; color: var(--mute); white-space: nowrap; }
  .gx-ns131 .gx-sb138 .st.lv { color: var(--bad); font-weight: 600; }
  .gx-ns131 .gx-gc138 { display: flex; gap: 8px; margin: 0 12px 10px; }
  .gx-ns131 .gx-gc138 button { flex: 1; padding: 8px 0 7px; border-radius: 12px; background: var(--card2, var(--bg)); text-align: center; box-shadow: inset 0 0 0 1px transparent; }
  .gx-ns131 .gx-gc138 button.on { box-shadow: inset 0 0 0 1.5px var(--accent); }
  .gx-ns131 .gx-gc138 b { display: block; font-size: 20px; line-height: 1.1; font-variant-numeric: tabular-nums; }
  .gx-ns131 .gx-gc138 small { font-size: 11px; color: var(--mute); }
  .gx-ns131 .gx-gr138 { margin: 0 12px 10px; }
  .gx-ns131 .gx-gr138 .r { display: grid; grid-template-columns: 22px minmax(0, 1fr) auto; align-items: center; gap: 10px; padding: 8px 2px; border-top: 1px solid var(--line); }
  .gx-ns131 .gx-gr138 .r:first-child { border-top: 0; }
  .gx-ns131 .gx-gr138 .r.me { box-shadow: inset 3px 0 0 var(--accent); padding-left: 8px; }
  .gx-ns131 .gx-gr138 .who { font-weight: 600; font-size: 14px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .gx-ns131 .gx-gr138 .as { font-size: 12px; color: var(--mute); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .gx-ns131 .gx-gr138 .tc { text-align: right; font-size: 12px; color: var(--mute); white-space: nowrap; font-variant-numeric: tabular-nums; }
  .gx-ns131 .gx-gr138 .tc .sc { color: var(--ink); font-weight: 600; }
</style>'''

SB_START = '  } else if (tab === "sb") {'
SB_END = '  } else {\n    const all = [];'
SB_NEW = r'''  } else if (tab === "sb") {
    /* gx138: one-line scoreboard */
    body = games.length ? <div className="gx-sb138">{games.map((g) => {
      const A = g.awayTeam || {}, H = g.homeTeam || {}, pre = !(live(g) || fin(g)), aw = !pre && +A.score >= +H.score, hw = !pre && +H.score >= +A.score;
      return (
        <button key={g.id} type="button" className="r" onClick={() => { setGid(g.id); setSide("fan"); }}>
          <span className="t"><TeamLogo t={gxAb131(A.abbrev)} size={20} /><span className="truncate">{gxAb131(A.abbrev)}</span></span>
          <b className={aw ? "w" : ""}>{pre || A.score == null ? "" : A.score}</b>
          <span className={"st" + (live(g) ? " lv" : "")}>{status(g)}</span>
          <b className={hw ? "w" : ""}>{pre || H.score == null ? "" : H.score}</b>
          <span className="t h"><span className="truncate">{gxAb131(H.abbrev)}</span><TeamLogo t={gxAb131(H.abbrev)} size={20} /></span>
        </button>
      );
    })}</div> : <div className="em">No NHL games today.</div>;
'''

GT_START = '    body = all.length ? all.map(({ g, x }, i) => {'
GT_END = '  return (\n    <div className="gx-ns131">'
GT_NEW = r'''    /* gx138: goal counters and short goal rows */
    const nmOf = (q) => (q.name && q.name.default) || [((q.firstName || {}).default || ""), ((q.lastName || {}).default || "")].join(" ").trim();
    const G138 = all.map(({ g, x }, i) => {
      const tm = gxAb131(x.teamAbbrev && x.teamAbbrev.default ? x.teamAbbrev.default : x.teamAbbrev), who = nmOf(x), p = gxFind131(tm, null, who), tag = gxTag131(s, p);
      const as = (x.assists || []).map((a) => { const an = nmOf(a), ap = gxFind131(tm, null, an); return { an, ap, at: gxTag131(s, ap) }; });
      const ros = !!tag || as.some((a) => a.at), me = (p && p.ft === s.me) || as.some((a) => a.ap && a.ap.ft === s.me);
      return { g, x, i, tm, who, p, tag, as, ros, me };
    });
    const nR = G138.filter((r) => r.ros).length, nM = G138.filter((r) => r.me).length;
    const list = G138.filter((r) => (gf138 === "me" ? r.me : gf138 === "ros" ? r.ros : true));
    const pBtn = (pl, label, k) => (pl ? <button key={k} type="button" className="hover:underline text-left" style={{ fontWeight: "inherit" }} onClick={() => { if (window.__NAV) window.__NAV.player(pl); }}>{label}</button> : <React.Fragment key={k}>{label}</React.Fragment>);
    body = (
      <>
        <div className="gx-gc138">{[["all", "Goals today", G138.length], ["ros", "Rostered", nR], ["me", "Yours", nM]].map(([k, l, c]) => <button key={k} type="button" className={gf138 === k ? "on" : ""} onClick={() => setGf138(k)}><b>{c}</b><small>{l}</small></button>)}</div>
        {list.length ? <div className="gx-gr138">{list.map((r) => {
          const ab = gxAb131((r.g.awayTeam || {}).abbrev), hb = gxAb131((r.g.homeTeam || {}).abbrev);
          return (
            <div key={r.g.id + "-" + r.i} className={"r" + (r.me ? " me" : "")}>
              <TeamLogo t={r.tm} size={22} />
              <div className="min-w-0">
                <div className="who">{pBtn(r.p, r.who, "s")}{r.tag ? <span className="own">{r.tag}</span> : null}</div>
                <div className="as">{r.as.length ? r.as.map((a, k) => <React.Fragment key={k}>{k ? ", " : ""}{pBtn(a.ap, a.an, "a")}{a.at ? " (" + a.at + ")" : ""}</React.Fragment>) : "Unassisted"}</div>
              </div>
              <div className="tc"><div className="sc">{ab + " " + (r.x.awayScore != null ? r.x.awayScore : "") + "-" + (r.x.homeScore != null ? r.x.homeScore : "") + " " + hb}</div><div>{gxPer131(r.x.periodDescriptor) + " " + (r.x.timeInPeriod || "")}</div></div>
            </div>
          );
        })}</div> : <div className="em">{G138.length ? (gf138 === "me" ? "No goals or assists by your players yet." : "No goals by rostered players yet.") : "No goals yet today."}</div>}
      </>
    );
  }
'''


def cut(t, label, start, end, new, marker):
    if marker in t:
        print("(install) " + label + ": already done")
        return t
    if t.count(start) != 1:
        fail(label + ": start text found " + str(t.count(start)) + " times")
    i = t.index(start)
    j = t.find(end, i)
    if j < 0:
        fail(label + ": end text not found")
    print("(install) " + label + ": updated")
    return t[:i] + new + t[j:]


def change(t):
    t = lit(t, "138: styles", "</style>", NEW_CSS, "change 138 (install.py)")
    t = lit(t, "138: goal filter state",
            '  const [side, setSide] = useState("fan");\n  const [, bump] = useState(0);',
            '  const [side, setSide] = useState("fan");\n  const [gf138, setGf138] = useState("all");\n  const [, bump] = useState(0);',
            'const [gf138, setGf138]')
    t = cut(t, "138: scoreboard rows", SB_START, SB_END, SB_NEW, "gx138: one-line scoreboard")
    t = cut(t, "138: goal tracker", GT_START, GT_END, GT_NEW, "gx138: goal counters")
    # header: live count and total goals today
    t = lit(t, "138: header counts",
            '<span className="n">{nLive ? <span className="lv">{nLive + " live"}</span> : games.length ? games.length + " games" : ""}</span>',
            '<span className="n">{(() => { const gl138 = games.filter((g) => live(g) || fin(g)).reduce((a, g) => a + (+((g.awayTeam || {}).score) || 0) + (+((g.homeTeam || {}).score) || 0), 0); return <>{nLive ? <span className="lv">{nLive + " live"}</span> : games.length ? games.length + " games" : ""}{gl138 ? " \\u00b7 " + gl138 + " goals" : ""}</>; })()}</span>',
            'const gl138 = games.filter')
    t = lit(t, "138: panel class", '    <div className="gx-ns131">', '    <div className="gx-ns131 gx138">', '<div className="gx-ns131 gx138">')
    # move the panel from above the day box to the very bottom of Matchup
    t = lit(t, "138: take panel off the top",
            '      <GxNhl131 s={s} />\n      <div className="gx-dn108">',
            '      <div className="gx-dn108" data-gx="138top">',
            'data-gx="138top"')
    t = lit(t, "138: panel at the bottom",
            '        <span>{gamesMoves(s, a, wk, A)}</span><span style={{ marginLeft: "auto" }}>{gamesMoves(s, b, wk, B)}</span>\n      </div>\n    </div>',
            '        <span>{gamesMoves(s, a, wk, A)}</span><span style={{ marginLeft: "auto" }}>{gamesMoves(s, b, wk, B)}</span>\n      </div>\n      <GxNhl131 s={s} />\n    </div>',
            '{gamesMoves(s, b, wk, B)}</span>\n      </div>\n      <GxNhl131 s={s} />')
    # player points all one colour (no green for the higher one)
    t = lit(t, "138: player points one colour",
            'style={win ? { color: "var(--good)", fontWeight: 600 } : null}',
            'style={null} data-gx="138pts"',
            'data-gx="138pts"')
    # both big scores the same colour
    t = lit(t, "138: scores one colour",
            '<div className="gx-num" style={{ fontSize: 28, color: "var(--ink2)" }}>',
            '<div className="gx-num" style={{ fontSize: 28 }} data-gx="138sc">',
            'data-gx="138sc"')
    # smoother live scores: no green or red flash, quicker count, and a drop waits 20 s
    # (live and ESPN numbers can disagree for a moment, which made the score jump down and back up)
    t = lit(t, "138: smoother score count",
            '''  const [fl, setFl] = useState("");
  const prev = React.useRef(v), raf = React.useRef(0);
  useEffect(() => {
    const a = prev.current, b = v;
    prev.current = v;
    if (a == null || b == null || Math.abs(b - a) < 0.05) { setShown(b); return undefined; }
    setFl(b > a ? "up" : "dn");
    const t0 = performance.now(), dur = 900;
    cancelAnimationFrame(raf.current);
    const step = (t) => { const k = Math.min(1, (t - t0) / dur), e = 1 - Math.pow(1 - k, 3); setShown(a + (b - a) * e); if (k < 1) raf.current = requestAnimationFrame(step); };
    raf.current = requestAnimationFrame(step);
    const to = setTimeout(() => setFl(""), 1800);
    return () => { cancelAnimationFrame(raf.current); clearTimeout(to); };
  }, [v]);
  return <span className={"gx-an131 " + fl}>''',
            '''  const cur = React.useRef(v), raf = React.useRef(0); /* gx138 smooth */
  useEffect(() => {
    const b = v;
    if (b == null || cur.current == null) { cur.current = b; setShown(b); return undefined; }
    const a = cur.current;
    if (Math.abs(b - a) < 0.05) return undefined;
    const go = () => {
      const t0 = performance.now(), dur = 600;
      cancelAnimationFrame(raf.current);
      const step = (t) => { const k = Math.min(1, (t - t0) / dur), e = 1 - Math.pow(1 - k, 3), x = k < 1 ? a + (b - a) * e : b; cur.current = x; setShown(x); if (k < 1) raf.current = requestAnimationFrame(step); };
      raf.current = requestAnimationFrame(step);
    };
    let to = 0;
    if (b < a) to = setTimeout(go, 20000); else go();
    return () => { cancelAnimationFrame(raf.current); clearTimeout(to); };
  }, [v]);
  return <span className="gx-an131">''',
            'gx138 smooth')
    return t


edit(APP, change)
