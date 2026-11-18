# changes/316-matchup-espn-sides.py - the Matchup page puts teams on the same sides as ESPN: away team on the left, home team on the right (so some weeks you are on the right); your win chance, margins and colours still read from your side

HELP = r'''// ---------- change 316: ESPN's sides on the Matchup page (away left, home right) ----------
// wk.pairs are stored [home, away]; your own matchup stays first in the list
function gxSides316(wk, me, opp) {
  const P = (wk.pairs || []).filter((p) => p[0] && p[1]);
  const mp = P.find((p) => p[0] === me || p[1] === me);
  return [mp ? [mp[1], mp[0]] : [me, opp], ...P.filter((p) => p !== mp).map((p) => [p[1], p[0]])];
}
'''


def change(t):
    t = lit(t, "316: helper", ROOT, HELP + ROOT, "change 316: ESPN's sides")
    t = lit(t, "316: matchup order",
            '''  const pairOpp = oppOf(wk, s.me);
  const myPair = [s.me, pairOpp || s.opp];
  const others = (wk.pairs || []).filter((p) => p[0] && p[1] && p[0] !== s.me && p[1] !== s.me);
  const all = [myPair, ...others];''',
            '''  const all = gxSides316(wk, s.me, s.opp); /* change 316: ESPN's sides */''',
            'const all = gxSides316(wk, s.me, s.opp); /* change 316')
    t = lit(t, "316: mine either side",
            '  const mine = a === s.me;\n',
            '  const mine = a === s.me || b === s.me, sg316 = b === s.me ? -1 : 1; /* change 316: you may be on the right */\n',
            'sg316 = b === s.me ? -1 : 1;')
    t = lit(t, "316: left name",
            '<div className="text-sm font-semibold gx-nm114" style={mine ? { color: "var(--accent)" } : null}>',
            '<div className={"text-sm gx-nm114" + (b === s.me ? " text-slate-500" : " font-semibold")} style={a === s.me ? { color: "var(--accent)" } : null}>',
            '(b === s.me ? " text-slate-500" : " font-semibold")} style={a === s.me ?')
    t = lit(t, "316: right name",
            '<div className="text-sm text-slate-500 gx-nm114 r">',
            '<div className={"text-sm gx-nm114 r" + (b === s.me ? " font-semibold" : " text-slate-500")} style={b === s.me ? { color: "var(--accent)" } : null}>',
            '"text-sm gx-nm114 r" + (b === s.me')
    t = lit(t, "316: ring shows your chance",
            '<GxRing v={winProb(A, B, aA, aB)} plain={!mine} />',
            '<GxRing v={sg316 < 0 ? 1 - winProb(A, B, aA, aB) : winProb(A, B, aA, aB)} plain={!mine} />',
            'v={sg316 < 0 ? 1 - winProb(A, B, aA, aB)')
    t = lit(t, "316: projected line",
            '{mine ? (margin >= 0 ? "Projected to win by " : "Projected to lose by ")',
            '{mine ? (margin * sg316 >= 0 ? "Projected to win by " : "Projected to lose by ")',
            'margin * sg316 >= 0 ?')
    t = lit(t, "316: day picker from your side",
            'dv={(i) => (i === d ? dvD135 : dvOf(i))} wkDv={aA - aB}',
            'dv={(i) => sg316 * (i === d ? dvD135 : dvOf(i))} wkDv={sg316 * (aA - aB)}',
            'wkDv={sg316 * (aA - aB)}')
    t = lit(t, "316: day total from your side",
            'style={{ color: !mine || Math.abs(dayTot) < 0.05 ? "var(--mute)" : dayTot > 0 ? "var(--good)" : "var(--bad)" }}>{(dayTot > 0 ? "+" : "") + f1(dayTot)}</div>',
            'style={{ color: !mine || Math.abs(dayTot) < 0.05 ? "var(--mute)" : sg316 * dayTot > 0 ? "var(--good)" : "var(--bad)" }}>{(sg316 * dayTot > 0 ? "+" : "") + f1(sg316 * dayTot)}</div>',
            'f1(sg316 * dayTot)')
    t = lit(t, "316: week summary from your side",
            '  const dw = aA - aB;\n',
            '  const dw = (b === s.me ? -1 : 1) * (aA - aB); /* change 316 */\n',
            'const dw = (b === s.me ? -1 : 1) * (aA - aB);')
    # the scores column always gets you as "My Team"
    t = lit(t, "316: scores column, phone",
            '<GxNhl141 s={s} a={a} b={b} tA={dates[d] < today ? A.days[d] : tA141} tB={dates[d] < today ? B.days[d] : tB141} day296={dates[d]} />',
            '<GxNhl141 s={s} a={sg316 < 0 ? b : a} b={sg316 < 0 ? a : b} tA={sg316 < 0 ? (dates[d] < today ? B.days[d] : tB141) : (dates[d] < today ? A.days[d] : tA141)} tB={sg316 < 0 ? (dates[d] < today ? A.days[d] : tA141) : (dates[d] < today ? B.days[d] : tB141)} day296={dates[d]} />',
            'a={sg316 < 0 ? b : a} b={sg316 < 0 ? a : b} tA={sg316 < 0 ? (dates[d] < today ? B.days[d] : tB141) : (dates[d] < today ? A.days[d] : tA141)} tB={sg316 < 0 ? (dates[d] < today ? A.days[d] : tA141) : (dates[d] < today ? B.days[d] : tB141)} day296={dates[d]} />')
    t = lit(t, "316: scores column, laptop",
            '<GxNhl141 s={s} a={a} b={b} tA={dates[d] < today ? A.days[d] : tA141} tB={dates[d] < today ? B.days[d] : tB141} day296={dates[d]} side />',
            '<GxNhl141 s={s} a={sg316 < 0 ? b : a} b={sg316 < 0 ? a : b} tA={sg316 < 0 ? (dates[d] < today ? B.days[d] : tB141) : (dates[d] < today ? A.days[d] : tA141)} tB={sg316 < 0 ? (dates[d] < today ? A.days[d] : tA141) : (dates[d] < today ? B.days[d] : tB141)} day296={dates[d]} side />',
            '<GxNhl141 s={s} a={sg316 < 0 ? b : a} b={sg316 < 0 ? a : b} tA={sg316 < 0 ? (dates[d] < today ? B.days[d] : tB141) : (dates[d] < today ? A.days[d] : tA141)} tB={sg316 < 0 ? (dates[d] < today ? A.days[d] : tA141) : (dates[d] < today ? B.days[d] : tB141)} day296={dates[d]} side />')
    # the score chips on top use the same sides
    t = lit(t, "316: chips",
            '  const all = [[s.me, myOpp || s.opp]].concat((wk.pairs || []).filter((p) => p[0] && p[1] && p[0] !== s.me && p[1] !== s.me)).filter((p) => p[0] && p[1]);\n  if (all.length < 2) return null;\n  const sc = (id) =>',
            '  const all = gxSides316(wk, s.me, myOpp || s.opp).filter((p) => p[0] && p[1]); /* change 316 */\n  if (all.length < 2) return null;\n  const sc = (id) =>',
            'const all = gxSides316(wk, s.me, myOpp || s.opp)')
    return t


edit(APP, change)
