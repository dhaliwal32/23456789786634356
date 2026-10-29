# changes/139-nhl-sheet.py - Matchup NHL scores open as a sheet that slides up (tap outside to slide it down), goal tracker back to the cards with faces and lined up evenly, counters Goals today / Mine / Opponent's, game scores (W 5-2, L 2-5) and scoreboard scores all one colour

NEW_CSS = r'''  /* change 139 (install.py) */
  .gx-sh139 { position: fixed; inset: 0; z-index: 75; background: rgba(0,0,0,.55); display: flex; align-items: flex-end; justify-content: center; animation: gx139-in .22s ease; }
  .gx-sh139 .gx-ns131.sh { width: min(760px, 100%); max-height: 88vh; margin: 0; display: flex; flex-direction: column; border-radius: 18px 18px 0 0; padding-bottom: env(safe-area-inset-bottom); animation: gx139-up .28s cubic-bezier(.2, .8, .2, 1); }
  .gx-sh139 .grab { width: 40px; height: 5px; border-radius: 9px; background: var(--line2, var(--line)); margin: 8px auto 0; flex: none; }
  .gx-sh139 .hd139 { display: flex; align-items: center; gap: 8px; padding: 10px 14px 12px; font-weight: 600; flex: none; }
  .gx-sh139 .hd139 .n { margin-left: auto; font-size: 12px; font-weight: 500; color: var(--mute); }
  .gx-sh139 .hd139 .n .lv { color: var(--bad); }
  .gx-sh139 .hd139 .xx { font-size: 24px; line-height: 1; color: var(--mute); padding: 0 2px 0 8px; }
  .gx-sh139 .seg { flex: none; }
  .gx-sh139 .bd139 { overflow-y: auto; -webkit-overflow-scrolling: touch; overscroll-behavior: contain; padding-bottom: 14px; }
  .gx-sh139.out { animation: gx139-out .22s ease forwards; }
  .gx-sh139.out .gx-ns131.sh { animation: gx139-down .22s ease-in forwards; }
  @keyframes gx139-in { from { opacity: 0; } }
  @keyframes gx139-out { to { opacity: 0; } }
  @keyframes gx139-up { from { transform: translateY(100%); } to { transform: none; } }
  @keyframes gx139-down { from { transform: none; } to { transform: translateY(100%); } }
  @media (prefers-reduced-motion: reduce) { .gx-sh139, .gx-sh139 .gx-ns131.sh { animation: none !important; } }
  .gx-ns131 .gx-sb138 b, .gx-ns131 .gx-sb138 b.w { color: var(--ink); font-weight: 600; }
  .gx-ns131 .gl .top { min-height: 46px; }
  .gx-ns131 .gl .top .ph139 { width: 46px; height: 46px; border-radius: 999px; overflow: hidden; background: var(--line); flex: none; display: flex; align-items: center; justify-content: center; }
  .gx-ns131 .gl .top .ph139 img { width: 100%; height: 100%; object-fit: cover; }
  .gx-ns131 .gl .who { font-size: 15px; }
</style>'''

STATE_OLD = '  const [gf138, setGf138] = useState("all");'
STATE_NEW = r'''  const [gf138, setGf138] = useState("all");
  const [cl139, setCl139] = useState(false);
  const close139 = () => { setCl139(true); setTimeout(() => { setCl139(false); setOpen(false); setGid(null); }, 220); };
  useEffect(() => {
    if (!open) return undefined;
    const k = (e) => { if (e.key === "Escape") close139(); };
    window.addEventListener("keydown", k);
    const ov = document.body.style.overflow; document.body.style.overflow = "hidden";
    return () => { window.removeEventListener("keydown", k); document.body.style.overflow = ov; };
  }, [open]);'''

GT_START = '    /* gx138: goal counters and short goal rows */'
GT_END = '  return (\n    <div className="gx-ns131 gx138">'
GT_NEW = r'''    /* gx139: goal counters and goal cards with faces */
    const nmOf = (q) => (q.name && q.name.default) || [((q.firstName || {}).default || ""), ((q.lastName || {}).default || "")].join(" ").trim();
    const G138 = all.map(({ g, x }, i) => {
      const tm = gxAb131(x.teamAbbrev && x.teamAbbrev.default ? x.teamAbbrev.default : x.teamAbbrev), who = nmOf(x), p = gxFind131(tm, null, who), tag = gxTag131(s, p);
      const as = (x.assists || []).map((a) => { const an = nmOf(a), ap = gxFind131(tm, null, an); return { an, ap, at: gxTag131(s, ap) }; });
      const by = (ft) => !!ft && ((p && p.ft === ft) || as.some((a) => a.ap && a.ap.ft === ft));
      return { g, x, i, tm, who, p, tag, as, me: by(s.me), op: by(opp) };
    });
    const nM = G138.filter((r) => r.me).length, nO = G138.filter((r) => r.op).length;
    const list = G138.filter((r) => (gf138 === "me" ? r.me : gf138 === "op" ? r.op : true));
    const pBtn = (pl, label, k) => (pl ? <button key={k} type="button" className="hover:underline text-left" style={{ fontWeight: "inherit" }} onClick={() => { close139(); if (window.__NAV) window.__NAV.player(pl); }}>{label}</button> : <React.Fragment key={k}>{label}</React.Fragment>);
    const face = (r) => {
      const src = r.x.headshot || r.x.mugshot || (r.p && String(r.p.id || "")[0] === "e" ? "https://a.espncdn.com/i/headshots/nhl/players/full/" + String(r.p.id).slice(1) + ".png" : "");
      return <span className="ph139">{src ? <img src={src} alt="" onError={(e) => { e.currentTarget.style.display = "none"; }} /> : <TeamLogo t={r.tm} size={30} />}</span>;
    };
    body = (
      <>
        <div className="gx-gc138">{[["all", "Goals today", G138.length], ["me", "Mine", nM], ["op", "Opponent's", nO]].map(([k, l, c]) => <button key={k} type="button" className={gf138 === k ? "on" : ""} onClick={() => setGf138(k)}><b>{c}</b><small>{l}</small></button>)}</div>
        {list.length ? list.map((r) => {
          const sc = gxAb131((r.g.awayTeam || {}).abbrev) + " " + (r.x.awayScore != null ? r.x.awayScore : "") + ", " + gxAb131((r.g.homeTeam || {}).abbrev) + " " + (r.x.homeScore != null ? r.x.homeScore : "");
          return (
            <div key={r.g.id + "-" + r.i} className="gl">
              <div className="top">{face(r)}
                <div className="min-w-0"><div className="who">{pBtn(r.p, r.who, "s")}{", " + r.tm}{r.tag ? <span className="own">{"(" + r.tag + ")"}</span> : null}</div><div className="when">{(r.x.timeInPeriod || "") + " " + gxPer131(r.x.periodDescriptor) + " Period \u00b7 " + sc}</div></div></div>
              <div className="as"><span>Assists:</span><span>{r.as.length ? r.as.map((a, k) => <React.Fragment key={k}>{k ? ", " : ""}{pBtn(a.ap, a.an, "a")}{a.at ? " (" + a.at + ")" : ""}</React.Fragment>) : "Unassisted"}</span></div>
            </div>
          );
        }) : <div className="em">{G138.length ? (gf138 === "me" ? "No goals or assists by your players yet." : "No goals or assists by your opponent's players yet.") : "No goals yet today."}</div>}
      </>
    );
  }
'''

RET_START = '  return (\n    <div className="gx-ns131 gx138">'
RET_END = '\n// ---------- change 132: live NHL data from ESPN'
RET_NEW = r'''  /* gx139: sheet */
  const gl139 = games.filter((g) => live(g) || fin(g)).reduce((a, g) => a + (+((g.awayTeam || {}).score) || 0) + (+((g.homeTeam || {}).score) || 0), 0);
  const cnt139 = <>{nLive ? <span className="lv">{nLive + " live"}</span> : games.length ? games.length + " games" : ""}{gl139 ? " \u00b7 " + gl139 + " goals" : ""}</>;
  const seg139 = <div className="seg"><button type="button" className={tab === "sb" ? "on" : ""} onClick={() => setTab("sb")}>Scoreboard</button><button type="button" className={tab === "gt" ? "on" : ""} onClick={() => setTab("gt")}>Goal tracker</button></div>;
  return (
    <div className="gx-ns131 gx138">
      <button type="button" className="bar" onClick={toggle}><span>NHL scores</span><span className="n">{cnt139}</span><span className="sec-chev shut" style={{ marginLeft: 8 }}></span></button>
      {open ? ReactDOM.createPortal(
        <div className={"gx-sh139" + (cl139 ? " out" : "")} onClick={close139} role="dialog" aria-label="NHL scores">
          <div className="gx-ns131 sh" onClick={(e) => e.stopPropagation()}>
            <div className="grab"></div>
            <div className="hd139"><span>NHL scores</span><span className="n">{cnt139}</span><button type="button" className="xx" aria-label="Close" onClick={close139}>{"\u00d7"}</button></div>
            {!gid ? seg139 : null}
            <div className="bd139">{body}</div>
          </div>
        </div>, document.body) : null}
    </div>
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
    t = lit(t, "139: styles", "</style>", NEW_CSS, "change 139 (install.py)")
    t = lit(t, "139: opponent passed in", "function GxNhl131({ s })", "function GxNhl131({ s, opp })", "function GxNhl131({ s, opp })")
    t = lit(t, "139: Matchup gives the opponent", "<GxNhl131 s={s} />", "<GxNhl131 s={s} opp={pairOpp || s.opp} />", "<GxNhl131 s={s} opp={pairOpp || s.opp} />")
    t = lit(t, "139: starts closed", "useState(() => !!uiGet().ns131)", "useState(false) /* gx139 */", "useState(false) /* gx139 */")
    t = lit(t, "139: sheet state", STATE_OLD, STATE_NEW, "const [cl139, setCl139]")
    t = lit(t, "139: tap opens the sheet",
            'const toggle = () => { const v = !open; setOpen(v); uiSet("ns131", v ? 1 : 0); };',
            'const toggle = () => { setGid(null); setOpen(true); }; /* gx139 */',
            'setOpen(true); }; /* gx139 */')
    t = cut(t, "139: goal tracker cards", GT_START, GT_END, GT_NEW, "gx139: goal counters")
    t = cut(t, "139: sheet", RET_START, RET_END, RET_NEW, "gx139: sheet")
    # game scores beside players (W 5-2, L 2-5) in one colour
    t = lit(t, "139: game scores one colour",
            '(res === "W" ? "text-green-700" : res === "L" ? "text-red-600" : "text-slate-700")',
            '("text-slate-700" /* gx139 */)',
            '("text-slate-700" /* gx139 */)')
    return t


edit(APP, change)
