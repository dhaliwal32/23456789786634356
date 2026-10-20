# changes/087-goalie-games.py - Lineup games counts skip goalies who are not starting (backups, goalies told they sit, goalies who did not play)

HELPERS = r'''// ---------- change 087: a goalie only counts as a lineup game if he starts (install.py) ----------
const gxGPlays = (p) => {
  if (!p || p.p !== "G") return true;
  if (p.a != null) return p.a !== 0;             // game played: real points tell us he was in net
  const g = p.dt ? gStart(p, p.dt) : null;
  return (g ? g.v : p.prob || 0) >= 0.5;          // still to come: count him if he is more likely than not to start
};
const gxGmN = (L) => ((L || {}).start || []).filter(gxGPlays).length;
const gxGmLeft = (days) => { const today = todayISO(); return (days || []).reduce((t, x) => t + (x ? (x.start || []).filter((p) => (!p.dt || p.dt >= today) && (!p.st || (p.st === "L" && p.vf > 0)) && gxGPlays(p)).length : 0), 0); };
'''

def change(t):
    t = lit(t, "087: helpers", ROOT, HELPERS + ROOT, "change 087: a goalie only counts")
    t = lit(t, "087: games left (week)", "used: sum((x) => x.openN + x.liveN)", "used: gxGmLeft(days) /* gx087 */", "used: gxGmLeft(days) /* gx087 */")
    t = lit(t, "087: games left (plan)", "used: sum((x) => x.start.length)", "used: sum((x) => x.start.filter(gxGPlays).length)", "x.start.filter(gxGPlays).length")
    t = lit(t, "087: games this matchup",
            "a: ((X.days[d] || {}).start || []).length, b: ((Y.days[d] || {}).start || []).length",
            "a: gxGmN(X.days[d]), b: gxGmN(Y.days[d])",
            "a: gxGmN(X.days[d]), b: gxGmN(Y.days[d])")
    t = lit(t, "087: score race days",
            "const gms = (L, d) => ((L.days[d] || {}).start || []).length;",
            "const gms = (L, d) => gxGmN(L.days[d]);",
            "const gms = (L, d) => gxGmN(L.days[d]);")
    return t

edit(APP, change)
