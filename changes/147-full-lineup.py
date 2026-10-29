# changes/147-full-lineup.py - Matchup day box shows every player like ESPN (phone and laptop): all lineup spots, players with no game faded, then bench and IR; the day total moved to the top of the box. Laptop scoreboard: no TV channel, betting lines always filled in (ESPN's line, or the app's own odds when ESPN has none)

NEW_CSS = r'''  /* change 147 (install.py) */
  .gx-idle147 { opacity: .42; }
  .gx-h2h.gx-tt147 { border-top: 0 !important; border-bottom: 2px solid var(--line2, var(--line)); margin-bottom: 2px; }
  .gx-h2h.gx-be147 { border-top: 2px solid var(--line2, var(--line)); }
  .gx-h2h .gx-sv147 { color: var(--faint, var(--mute)); }
</style>'''

ROWS_OLD = r'''  const rows = [];
  ["F", "D", "UTIL", "G"].forEach((sl) => {'''
ROWS_NEW = r'''  /* gx147: every player, like ESPN */
  const full147 = (id, l) => {
    const N = { F: 9, D: 5, UTIL: 1, G: 2 }, out = { F: [], D: [], UTIL: [], G: [], BE: [], IR: [] }, dt = dates[d];
    const used = new Set((l.start || []).map((p) => p.id));
    (l.start || []).forEach((p) => (out[p.slot] || out.BE).push(p));
    const bn = (l.bench || []).filter((p) => !used.has(p.id)).map((p) => ({ ...p, bench147: true, dt }));
    bn.forEach((p) => used.add(p.id));
    const rest = s.players.filter((p) => p.ft === id && !used.has(p.id));
    const idle = rest.filter((p) => !p.ir).map((p) => ({ ...p, idle147: true, dt }));
    const take = (sl, ok) => { while (out[sl].length < N[sl]) { const i = idle.findIndex(ok); if (i < 0) break; out[sl].push(idle.splice(i, 1)[0]); } };
    take("F", (p) => p.p === "F"); take("D", (p) => p.p === "D"); take("G", (p) => p.p === "G"); take("UTIL", (p) => p.p !== "G");
    out.BE = [...bn, ...idle];
    out.IR = rest.filter((p) => p.ir).map((p) => ({ ...p, idle147: true, dt }));
    return out;
  };
  const fa147 = full147(a, x), fb147 = full147(b, y);
  const rows = [];
  ["BE", "IR"].forEach((sl) => { for (let i = 0; i < Math.max(fa147[sl].length, fb147[sl].length); i++) rows.push([sl, fa147[sl][i] || null, fb147[sl][i] || null]); });
  const tail147 = rows.splice(0, rows.length);
  ["F", "D", "UTIL", "G"].forEach((sl) => { for (let i = 0; i < Math.max(fa147[sl].length, fb147[sl].length); i++) rows.push([sl, fa147[sl][i] || null, fb147[sl][i] || null]); });
  rows.push(...tail147);
  if (false) ["F", "D", "UTIL", "G"].forEach((sl) => {'''

CELL_OLD = r'''    if (!p) return <div className={"text-sm text-slate-500" + (right ? " text-right" : "")}>empty</div>;'''
CELL_NEW = CELL_OLD + r'''
    if (p.idle147 || p.bench147) { /* gx147: no game or on the bench */
      const sub = p.bench147 ? mGame(p) : "";
      return (
        <div className={"min-w-0 gx-pc" + (p.idle147 ? " gx-idle147" : "")} style={{ flexDirection: right ? "row-reverse" : "row" }}><span className="gx-fw" style={{ display: "inline-flex" }}><GxFace p={p} size={30} /></span><div className={"min-w-0" + (right ? " text-right" : "")} style={{ flex: 1 }}>
          <div className="truncate gx-nm"><button type="button" className="hover:underline text-left" onClick={(e) => { e.stopPropagation(); if (window.__NAV) window.__NAV.player(p); }}><span className="m-hide">{p.n}</span><span className="m-inl">{shortN(p.n)}</span></button><span className="gx-tl98"><TeamLogo t={p.t} size={15} /></span>{p.ir ? <span style={{ color: "var(--bad)", fontWeight: 600, fontSize: 12, marginLeft: 4 }}>IR</span> : null}</div>
          <div className="text-xs text-slate-500 truncate">{sub || "\u00a0"}</div></div>
        </div>
      );
    }'''

NUM_OLD = r'''    if (v == null) return <div className={"text-slate-500" + (right ? "" : " text-right")}>{"\u2013"}</div>;'''
NUM_NEW = r'''    if (p && (p.idle147 || p.bench147)) return <div className={"gx-sv147" + (right ? "" : " text-right")}>{"\u2013"}</div>;
''' + NUM_OLD


def change(t):
    t = lit(t, "147: styles", "</style>", NEW_CSS, "change 147 (install.py)")
    t = lit(t, "147: every player", ROWS_OLD, ROWS_NEW, "gx147: every player, like ESPN")
    t = lit(t, "147: faded cells", CELL_OLD + "\n", CELL_NEW + "\n", "gx147: no game or on the bench")
    t = lit(t, "147: no points for them", NUM_OLD, NUM_NEW, 'p && (p.idle147 || p.bench147)) return <div className={"gx-sv147"')
    # bench line gets a divider above the first BE row
    t = lit(t, "147: bench divider",
            '          <div className="gx-h2h" style={i ? null : { borderTop: 0 }}>',
            '          <div className={"gx-h2h" + (sl === "BE" && (!rows[i - 1] || rows[i - 1][0] !== "BE") ? " gx-be147" : "")} style={i ? null : { borderTop: 0 }}>',
            '" gx-be147" : "")}')
    # day total at the top of the day box
    if "gx-tt114 gx-tt147" not in t:
        k = t.find('{rows.length ? <div className="gx-h2h gx-tt114">')
        if k < 0 or t.count('{rows.length ? <div className="gx-h2h gx-tt114">') != 1:
            fail("147: day total row not found once")
        line_start = t.rfind("\n", 0, k) + 1
        line_end = t.index("\n", k)
        line = t[line_start:line_end]
        if not line.strip().startswith("{rows.length ? <div className=\"gx-h2h gx-tt114\">") or not line.rstrip().endswith("null}"):
            fail("147: day total row is not on its own line")
        t = t[:line_start] + t[line_end + 1:]
        anchor = '        {rows.length ? rows.map(([sl, p, q], i) => ('
        if t.count(anchor) != 1:
            fail("147: day rows anchor not found once")
        t = t.replace(anchor, line.replace('<div className="gx-h2h gx-tt114">', '<div className="gx-h2h gx-tt114 gx-tt147">') + "\n" + anchor)
        print("(install) 147: day total at the top: updated")
    # laptop scoreboard: no TV channel; betting lines from ESPN in any of its shapes, else from the app's odds
    if '<small>{g.tv || "\\u00a0"}</small>' in t:
        t = t.replace('<small>{g.tv || "\\u00a0"}</small>', '', 1)
        print("(install) 147: TV channel removed")
    t = lit(t, "147: ESPN line shapes",
            'const v = q.moneyLine != null ? q.moneyLine : ((((q.current || {}).moneyLine) || {}).american);',
            'let v = q.moneyLine != null ? q.moneyLine : ((((q.current || {}).moneyLine) || {}).american); if (v == null) v = ((q.close || {}).odds) != null ? q.close.odds : (q.open || {}).odds; if (v != null && isNaN(+v)) v = String(v).toUpperCase() === "EVEN" ? 100 : null;',
            'String(v).toUpperCase() === "EVEN"')
    t = lit(t, "147: ESPN moneyline block",
            'g.ml = { a: ml(od.awayTeamOdds), h: ml(od.homeTeamOdds) };',
            'g.ml = { a: ml(od.awayTeamOdds), h: ml(od.homeTeamOdds) }; if (g.ml.a == null && od.moneyline) g.ml = { a: ml(od.moneyline.away), h: ml(od.moneyline.home) };',
            'if (g.ml.a == null && od.moneyline)')
    t = lit(t, "147: away line", '{ta + " " + ml146(g.ml.a)}', '{ta + " " + ml146(gxML147(g.ml.a, ta))}', 'ml146(gxML147(g.ml.a, ta))')
    t = lit(t, "147: home line", '{th + " " + ml146(g.ml.h)}', '{th + " " + ml146(gxML147(g.ml.h, th))}', 'ml146(gxML147(g.ml.h, th))')
    t = lit(t, "147: line helper", ROOT,
            '// ---------- change 147: betting line from the app\'s odds when ESPN has none (install.py) ----------\n'
            'function gxML147(v, t) {\n'
            '  if (v != null && !isNaN(+v)) return +v;\n'
            '  const o = ((((window.ESPN_DATA || {}).model || {}).odds) || {})[todayISO()] || {}, w = o[t] && o[t].win;\n'
            '  if (w == null || w <= 0 || w >= 1) return null;\n'
            '  const m = w >= 0.5 ? -100 * w / (1 - w) : 100 * (1 - w) / w;\n'
            '  return Math.round(m / 5) * 5;\n'
            '}\n' + ROOT,
            'change 147: betting line from the app')
    return t


edit(APP, change)
