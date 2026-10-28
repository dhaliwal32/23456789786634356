# changes/118-show-all-box-score.py - Pickups: every free agent shows, no "Show more"; player screen: the Game log tab always shows every game; Matchup: tap a player (not the name) and his full box score for that day opens right under him, tap the name to open his profile

NEW_CSS = r'''  /* change 118 (install.py) */
  .gx-h2h .gx-pc { cursor: pointer; }
  .gx-bx118 { margin: 0 0 8px; padding: 12px; border-radius: 12px; background: var(--card2, var(--bg)); box-shadow: inset 0 0 0 1px var(--line); transform-origin: top center; animation: gx118-open .2s ease-out; }
  @keyframes gx118-open { from { opacity: 0; transform: scaleY(.85); } to { opacity: 1; transform: none; } }
  .gx-bx118 .hd { display: flex; align-items: baseline; gap: 8px; margin-bottom: 10px; }
  .gx-bx118 .hd .n { font-weight: 600; }
  .gx-bx118 .hd .o { font-size: 12px; color: var(--mute); }
  .gx-bx118 .hd .x { margin-left: auto; font-size: 13px; color: var(--accent); }
  .gx-bx118 .g { display: grid; grid-template-columns: repeat(auto-fill, minmax(52px, 1fr)); gap: 8px 4px; }
  .gx-bx118 .g > div { text-align: center; }
  .gx-bx118 .g small { display: block; font-size: 11px; color: var(--mute); }
  .gx-bx118 .g b { font-size: 16px; font-weight: 600; font-variant-numeric: tabular-nums; }
  .gx-bx118 .g .f b { color: var(--accent); }
  .gx-bx118 .e { font-size: 13px; color: var(--mute); }
</style>'''

HELPERS = r'''// ---------- change 118: one player's box score for one day, opened from Matchup (install.py) ----------
function GxBox118({ p }) {
  const x = typeof pStat === "function" ? pStat(p, p.dt) : null;
  const pts = p.st ? (p.a == null ? 0 : p.a) : p.x;
  const opp = p.st && typeof gxOpp98 === "function" ? gxOpp98(p) : mGame(p);
  const t = (k, l, v, f) => <div key={k} className={f ? "f" : ""}><small>{l}</small><b>{v}</b></div>;
  let cells = [];
  if (x && x.sv != null) {
    cells = [t("f", "FPTS", f1(pts || 0), 1), t("dec", "Result", ({ W: "Win", L: "Loss", O: "OT loss" })[x.dec] || "–"), t("sv", "Saves", x.sv), t("ga", "Goals against", x.ga),
      t("sa", "Shots", x.sa != null ? x.sa : x.sv + x.ga), t("svp", "Save %", x.sv + x.ga ? (x.sv / (x.sv + x.ga)).toFixed(3).replace(/^0/, "") : "–"), t("so", "Shutout", x.ga === 0 && x.dec === "W" ? "Yes" : "No"), t("toi", "TOI", x.toi || "–")];
  } else if (x) {
    const pm = x.pm || 0;
    cells = [t("f", "FPTS", f1(pts || 0), 1), t("g", "G", x.g || 0), t("a", "A", x.a || 0), t("pts", "PTS", (x.g || 0) + (x.a || 0)), t("pm", "+/-", (pm > 0 ? "+" : "") + pm),
      t("sog", "SOG", x.sog || 0), t("ppg", "PPG", x.ppg || 0), t("pim", "PIM", x.pim || 0), t("hit", "HIT", x.hit || 0), t("blk", "BLK", x.blk || 0),
      t("tk", "TK", x.tk || 0), t("gv", "GV", x.gv || 0), x.fo ? t("fo", "FO%", Math.round(x.fo * 100) + "%") : null, t("shf", "Shifts", x.shf || 0), t("toi", "TOI", x.toi || "–")].filter(Boolean);
  }
  return (
    <div className="gx-bx118">
      <div className="hd">
        <span className="n">{p.n}</span><span className="o">{opp}</span>
        <button type="button" className="x" onClick={(e) => { e.stopPropagation(); if (window.__NAV) window.__NAV.player(p); }}>Profile</button>
      </div>
      {cells.length ? <div className="g">{cells}</div>
        : <div className="e">{p.st ? "No stats yet for this game." : "Has not played yet. Projected " + f1(p.x || 0) + " FPTS."}</div>}
    </div>
  );
}
'''


def change(t):
    t = lit(t, "118: styles", "</style>", NEW_CSS, "change 118 (install.py)")
    t = lit(t, "118: helpers", ROOT, HELPERS + ROOT, "change 118: one player's box score")
    # pickups: every free agent, no Show more
    t = lit(t, "118: pickups show all", "  const [limit, setLimit] = useState(25);", "  const [limit, setLimit] = useState(100000); /* gx118: show all */", "gx118: show all")
    t = t.replace("setLimit(25)", "setLimit(100000)")
    # player screen: full game log
    t = lit(t, "118: full game log", "  const [nLog, setNLog] = useState(10);", "  const [nLog, setNLog] = useState(100000); /* gx118: full log */", "gx118: full log")
    t = lit(t, "118: full game log on new player", "useEffect(() => { setTab(\"ov\"); setNLog(10); setImg(true); }, [p.id]);",
            "useEffect(() => { setTab(\"ov\"); setNLog(100000); setImg(true); }, [p.id]);", "setNLog(100000); setImg(true)")
    # matchup: tap a player for his box score
    t = lit(t, "118: matchup box state", "  const sl105a = useSlide105(sel), sl105b = useSlide105(sel * 100 + d);",
            "  const sl105a = useSlide105(sel), sl105b = useSlide105(sel * 100 + d);\n  const [bx118, setBx118] = useState(\"\");",
            "const [bx118, setBx118] = useState(")
    t = lit(t, "118: matchup tap player",
            '      <div className={"min-w-0 gx-pc" + (p.st === "F" ? " gx-fin" : "")} style={{ flexDirection: right ? "row-reverse" : "row" }}>',
            '      <div className={"min-w-0 gx-pc" + (p.st === "F" ? " gx-fin" : "")} style={{ flexDirection: right ? "row-reverse" : "row" }} onClick={() => setBx118(bx118 === p.id + "|" + p.dt ? "" : p.id + "|" + p.dt)}>',
            'onClick={() => setBx118(bx118 === p.id')
    t = lit(t, "118: matchup box under the row",
            '''        {rows.length ? rows.map(([sl, p, q], i) => (
          <div key={i} className="gx-h2h" style={i ? null : { borderTop: 0 }}>
            {cell(p, false)}{num(p, q, false)}
            <div className="text-xs text-center" style={{ color: "var(--faint)" }}>{sl === "UTIL" ? "U" : sl}</div>
            {num(q, p, true)}{cell(q, true)}
          </div>
        )) : ''',
            '''        {rows.length ? rows.map(([sl, p, q], i) => (
          <React.Fragment key={i}>
          <div className="gx-h2h" style={i ? null : { borderTop: 0 }}>
            {cell(p, false)}{num(p, q, false)}
            <div className="text-xs text-center" style={{ color: "var(--faint)" }}>{sl === "UTIL" ? "U" : sl}</div>
            {num(q, p, true)}{cell(q, true)}
          </div>
          {[p, q].filter((z) => z && bx118 === z.id + "|" + z.dt).map((z) => <GxBox118 key={"bx" + z.id} p={z} />)}
          </React.Fragment>
        )) : ''',
            "<GxBox118 key=")
    return t


edit(APP, change)
