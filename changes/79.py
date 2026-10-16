# changes/079-tap-to-sort.py - tap any column heading to sort that list highest first (Pickups, rosters, League table, Player rankings, Playoff targets)

NEW_CSS = r'''  /* change 079 (install.py) */
  .gx-sh { color: inherit; text-align: right; cursor: pointer; white-space: nowrap; }
  .gx-sh:hover { color: var(--ink); }
  .gx-sh.on { color: var(--ink); font-weight: 600; text-decoration: underline; text-underline-offset: 3px; }
  th .gx-sh { text-align: left; text-transform: inherit; letter-spacing: inherit; font-weight: inherit; }
  th .gx-sh.on { font-weight: 600; }
</style>'''

HELPERS = r'''// ---------- change 079: tap a heading to sort (install.py) ----------
// first tap: highest first; tap the same heading again: back to the normal order
const GxSH = ({ k, cur, set, def, cls, children }) => (
  <button type="button" className={"n gx-sh " + (cls || "") + (cur === k ? " on" : "")} title="Tap to sort, highest first" onClick={(e) => { e.stopPropagation(); set(cur === k ? def : k); }}>{children}</button>
);
const gxL5v = (h) => { const a = (h || []).map((x) => (typeof x === "number" ? x : x && x.v)).filter((x) => x != null); return a.length ? a.reduce((s, x) => s + x, 0) / a.length : -99; };
'''

# ---- Pickups ----
OLD_PK_ROWS = '''  const all = q ? M.res : M.res.filter((r) => r.gain >= minGain);
  const rows = all.slice(0, limit);'''
NEW_PK_ROWS = '''  const all = q ? M.res : M.res.filter((r) => r.gain >= minGain);
  // change 079: sort the whole list by any heading before it is cut to the first rows
  const [srt79, setSrt79] = useState("add");
  const wAll79 = useMemo(() => { const o = {}; if (srt79 !== "win" || base == null) return o; all.slice(0, 150).forEach((r) => { o[r.f.id] = winChance(sP, afterMove(sP, r.f, r.d)); }); return o; }, [M, srt79, base]);
  const key79 = { l5: (r) => gxL5v(hist[String(r.f.id).slice(1)]), g: (r) => M.gamesIn(r.f), x: (r) => effAvg(r.f, K), win: (r) => (wAll79[r.f.id] != null ? wAll79[r.f.id] : -1) }[srt79];
  const rows = (key79 ? [...all].sort((a, b) => key79(b) - key79(a) || b.gain - a.gain) : all).slice(0, limit);'''
OLD_PK_DEPS = '''  }, [M, limit, base]);
  const ids = rows.map((r) => String(r.f.id).slice(1)).join(",");'''
NEW_PK_DEPS = '''  }, [M, limit, base, srt79, wAll79]);
  const ids = (srt79 === "l5" ? all.slice(0, 150) : rows).map((r) => String(r.f.id).slice(1)).join(",");'''
OLD_PK_HEAD = '''<span className="n m-hide">Last 5</span><span className="n m-hide">Games</span><span className="n m-hide">Expected</span><span className="n">Adds</span><span className="n">Win</span>'''
NEW_PK_HEAD = '''<GxSH k="l5" cur={srt79} set={(v) => { setSrt79(v); setLimit(25); }} def="add" cls="m-hide">Last 5</GxSH><GxSH k="g" cur={srt79} set={(v) => { setSrt79(v); setLimit(25); }} def="add" cls="m-hide">Games</GxSH><GxSH k="x" cur={srt79} set={(v) => { setSrt79(v); setLimit(25); }} def="add" cls="m-hide">Expected</GxSH><GxSH k="add" cur={srt79} set={(v) => { setSrt79(v); setLimit(25); }} def="add">Adds</GxSH><GxSH k="win" cur={srt79} set={(v) => { setSrt79(v); setLimit(25); }} def="add">Win</GxSH>'''

# ---- My Team roster and other teams' roster pages (same code in both) ----
OLD_KEY = '''  const keyFn = { mu: (p) => mu[p.id] || 0, left, next: nextG, sea: (p) => (p.gp ? p.tot / p.gp : -99), pg: pv, rk: (p) => -(rankOf[p.id] || 9999) }[sort];'''
NEW_KEY = '''  const keyFn = { mu: (p) => mu[p.id] || 0, left, next: nextG, sea: (p) => (p.gp ? p.tot / p.gp : -99), pg: pv, rk: (p) => -(rankOf[p.id] || 9999), l5: (p) => gxL5v(hist[String(p.id).slice(1)]) }[sort]; // change 079: Last 5 sorts too'''

# ---- League table ----
OLD_LT_LIST = '''  const list = by === "st" ? stand : T.rows;'''
NEW_LT_LIST = '''  // change 079: Points and Playoffs headings sort too
  const list = by === "st" ? stand : by === "pf" ? [...T.rows].sort((a, b) => b.rec.pf - a.rec.pf || b.strength - a.strength) : by === "po" ? [...T.rows].sort((a, b) => ((sim && sim.odds[b.t.id]) || 0) - ((sim && sim.odds[a.t.id]) || 0) || b.strength - a.strength) : T.rows;'''
OLD_LT_HEAD = '''<span className="n">Record</span><span className="n m-hide">Points</span><span className="n m-hide">Strength</span><span className="n">Playoffs</span></div>'''
NEW_LT_HEAD = '''<GxSH k="st" cur={by} set={setBy} def="st">Record</GxSH><GxSH k="pf" cur={by} set={setBy} def="st" cls="m-hide">Points</GxSH><GxSH k="pw" cur={by} set={setBy} def="st" cls="m-hide">Strength</GxSH><GxSH k="po" cur={by} set={setBy} def="st">Playoffs</GxSH></div>'''

# ---- Player rankings: GP sorts too ----
OLD_RK_SORT = '''    .sort((a, b) => (sort === "exp" ? a.rk - b.rk : sort === "sf" ?'''
NEW_RK_SORT = '''    .sort((a, b) => (sort === "exp" ? a.rk - b.rk : sort === "gp" ? (b.p.gp || 0) - (a.p.gp || 0) || a.rk - b.rk : sort === "sf" ?'''
OLD_RK_HEAD = '''<span className="n m-hide">GP</span>{HB("sf", "So far")}'''
NEW_RK_HEAD = '''{HB("gp", "GP", "m-hide")}{HB("sf", "So far")}'''

# ---- Playoff targets table ----
OLD_PO_ROWS = '''  const rows = useMemo(() => s.players'''
NEW_PO_ROWS = '''  const [sp79, setSp79] = useState("v"); // change 079: tap a heading to sort
  const pk79 = (x) => (sp79[0] === "w" ? x.per[+sp79.slice(1)] || 0 : sp79 === "avg" ? effAvg(x.p, K) : x[sp79] || 0);
  const rows = useMemo(() => s.players'''
OLD_PO_SORT = '''    .sort((a, b) => b.v - a.v).slice(0, 100), [s.players, who, pos, q, st, nW, K]);'''
NEW_PO_SORT = '''    .sort((a, b) => pk79(b) - pk79(a) || b.v - a.v).slice(0, 100), [s.players, who, pos, q, st, nW, K, sp79]);'''
OLD_PO_HEAD = '''"Games", "Light", "Avg", "Playoff pts", "Sched bonus"].map((h, i) => <th key={i} className="px-2 py-2">{h}</th>)}'''
NEW_PO_HEAD = '''"Games", "Light", "Avg", "Playoff pts", "Sched bonus"].map((h, i) => { const k = i < 3 ? null : i < 3 + weeks.length ? "w" + (i - 3) : ["g", "off", "avg", "v", "bonus"][i - 3 - weeks.length]; return <th key={i} className="px-2 py-2">{k ? <GxSH k={k} cur={sp79} set={setSp79} def="v">{h}</GxSH> : h}</th>; })}'''


def change(t):
    t = lit(t, "079: styles", "</style>", NEW_CSS, "change 079 (install.py)")
    t = lit(t, "079: helpers", ROOT, HELPERS + ROOT, "change 079: tap a heading to sort")
    t = lit(t, "079: pickups sort", OLD_PK_ROWS, NEW_PK_ROWS, "change 079: sort the whole list")
    t = lit(t, "079: pickups win chances follow the sort", OLD_PK_DEPS, NEW_PK_DEPS, "[M, limit, base, srt79, wAll79]")
    t = lit(t, "079: pickups headings", OLD_PK_HEAD, NEW_PK_HEAD, '<GxSH k="l5" cur={srt79}')
    t = lit(t, "079: roster Last 5 sort", OLD_KEY, NEW_KEY, "change 079: Last 5 sorts too", count=2)
    t = lit(t, "079: roster Last 5 heading", '<span className="n m-hide">Last 5</span>', '{HB("l5", "Last 5", "m-hide")}', 'HB("l5", "Last 5"', count=2)
    t = lit(t, "079: league table sort", OLD_LT_LIST, NEW_LT_LIST, "change 079: Points and Playoffs headings")
    t = lit(t, "079: league table headings", OLD_LT_HEAD, NEW_LT_HEAD, '<GxSH k="st" cur={by}')
    t = lit(t, "079: rankings GP sort", OLD_RK_SORT, NEW_RK_SORT, 'sort === "gp" ? (b.p.gp')
    t = lit(t, "079: rankings GP heading", OLD_RK_HEAD, NEW_RK_HEAD, 'HB("gp", "GP"')
    t = lit(t, "079: playoff targets sort state", OLD_PO_ROWS, NEW_PO_ROWS, "const [sp79, setSp79]")
    t = lit(t, "079: playoff targets sort", OLD_PO_SORT, NEW_PO_SORT, "pk79(b) - pk79(a)")
    t = lit(t, "079: playoff targets headings", OLD_PO_HEAD, NEW_PO_HEAD, "<GxSH k={k} cur={sp79}")
    return t


edit(APP, change)
