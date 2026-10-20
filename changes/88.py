# changes/088-goalie-per-game.py - Pickups: goalies show points per team game (points if he starts x start chance), same as Trades, so they compare fairly with skaters

HELPERS = r'''// ---------- change 088: goalies per team game, like Trades (install.py) ----------
const gxPgAvg = (p, K, dt) => effAvg(p, K, dt) * (p && p.p === "G" ? (p.prob != null ? p.prob : 0.5) : 1);
'''

OPT_OLD = '{drops.map((p) => <option key={p.id} value={p.id}>{p.n} ({p.p}) · {f1(effAvg(p, K))}/g{protectedIds.has(p.id) ? " · protected" : ""}</option>)}'
OPT_NEW = '{drops.map((p) => <option key={p.id} value={p.id}>{p.n} ({p.p}) · {f1(effAvg(p, K))}/g{p.p === "G" ? " · starts " + Math.round((p.prob || 0) * 100) + "%" : ""}{protectedIds.has(p.id) ? " · protected" : ""}</option>)}{/* gx088-opt */}'

def change(t):
    t = lit(t, "088: helpers", ROOT, HELPERS + ROOT, "change 088: goalies per team game")
    t = lit(t, "088: protect by per-game value",
            "const ranked = myR.filter((p) => !p.ir).sort((a, b) => effAvg(wt(b), K) - effAvg(wt(a), K));",
            "const ranked = myR.filter((p) => !p.ir).sort((a, b) => gxPgAvg(wt(b), K) - gxPgAvg(wt(a), K)); /* gx088 */",
            "gxPgAvg(wt(b), K) - gxPgAvg(wt(a), K)); /* gx088 */")
    t = lit(t, "088: simulate box",
            "function MoveSim({ s, setS, wk, M, H, hLabel, init, wBase, onClose }) {\n",
            "function MoveSim({ s, setS, wk, M, H, hLabel, init, wBase, onClose }) {\n  const effAvg = gxPgAvg; /* gx088-sim */\n",
            "/* gx088-sim */")
    t = lit(t, "088: drop list shows start chance", OPT_OLD, OPT_NEW, "{/* gx088-opt */}")
    t = lit(t, "088: Pickups list",
            "function Pickups({ s, setS, wk }) {\n  const K = s.blend;",
            "function Pickups({ s, setS, wk }) {\n  const effAvg = gxPgAvg; /* gx088-pk */\n  const K = s.blend;",
            "/* gx088-pk */")
    t = lit(t, "088: watchlist",
            "function GxWatchPanel({ s }) {\n",
            "function GxWatchPanel({ s }) {\n  const effAvg = gxPgAvg; /* gx088-w */\n",
            "/* gx088-w */")
    t = lit(t, "088: injuries page",
            "function GxInjPage({ s }) {\n",
            "function GxInjPage({ s }) {\n  const effAvg = gxPgAvg; /* gx088-i */\n",
            "/* gx088-i */")
    t = lit(t, "088: injuries page counts goalies once",
            'const val = (p) => effAvg(p, K) * (p.p === "G" ? p.prob || 0.5 : 1);',
            'const val = (p) => effAvg(p, K); /* gx088-iv */',
            "/* gx088-iv */")
    t = lit(t, "088: advice protect ranking",
            "const ranked = myR.filter((p) => !p.ir).sort((a, b) => effAvg(b, K) - effAvg(a, K));",
            "const ranked = myR.filter((p) => !p.ir).sort((a, b) => gxPgAvg(b, K) - gxPgAvg(a, K)); /* gx088-a */",
            "/* gx088-a */")
    old_r = "const healthy = roster.filter((p) => !p.ir).sort((a, b) => effAvg(b, K) - effAvg(a, K));"
    if "/* gx088-r */" not in t:
        if t.count(old_r) != 2:
            fail("088: roster protect ranking: expected 2 matches, found " + str(t.count(old_r)))
        t = t.replace(old_r, "const healthy = roster.filter((p) => !p.ir).sort((a, b) => gxPgAvg(b, K) - gxPgAvg(a, K)); /* gx088-r */")
    return t

edit(APP, change)
