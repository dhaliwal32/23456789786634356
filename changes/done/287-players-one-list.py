# changes/287-players-one-list.py - Players is one page: a single list of every player with a switch on top (All, Free agents, Injured, Advice), positions, search, and the two team lists tucked behind More filters; the old row of four pages is gone (Advice is the old Free agents page with the watchlist and win chances)

NEW_CSS = r'''  /* change 287 (install.py) */
  .gx-pl287 > .gx-seg103 { margin-bottom: 12px; }
  .gx-mf287 { border: 1px solid var(--line2); border-radius: 8px; padding: 6px 12px; font-size: 14px; color: var(--ink); white-space: nowrap; }
  .gx-mf287.on { background: var(--accentSoft); }
</style>'''

HELPERS = r'''// ---------- change 287: Players as one list (install.py) ----------
const GX_PL287 = [["all", "All"], ["fa", "Free agents"], ["inj", "Injured"], ["adv", "Advice"]];
function GxPlayers287(P) {
  const { sub } = P;
  const [v, setV] = useState(() => { const u = uiGet().pl287; return sub === "allp" ? "all" : sub === "injuries" ? "inj" : GX_PL287.some((x) => x[0] === u) ? u : "fa"; });
  const pick = (k) => { setV(k); uiSet("pl287", k); };
  return (
    <div className="gx-pl287" data-gx="287">
      <div className="gx-seg103">{GX_PL287.map(([k, l]) => <button key={k} type="button" className={v === k ? "on" : ""} onClick={() => pick(k)}>{l}</button>)}</div>
      {v === "adv" ? <Pickups {...P} /> : <GxRankings s={P.s} st287={v} />}
    </div>
  );
}
'''

ROUTE_OLD = r'''  else if (tab === "moves") content = sub === "allp" ? <div className="space-y-3"><GxFaToggle105 cur="allp" go={go} /><GxRankings {...P} /></div> : '''
ROUTE_NEW = r'''  else if (tab === "moves") content = sub === "allp" || sub === "injuries" || sub === "adddrop" || !sub ? <GxPlayers287 {...P} sub={sub} /> : sub === "allp" ? <div className="space-y-3"><GxFaToggle105 cur="allp" go={go} /><GxRankings {...P} /></div> : '''

BAR_OLD = r'''    const cur = GX_PL103.some((x) => x[0] === sub) ? sub : "adddrop";
    return <div className="gx-seg103 mb-3">{GX_PL103.map(([k, l]) => <button key={k} type="button" className={cur === k ? "on" : ""} onClick={() => go("moves", k)}>{l}</button>)}</div>;'''
BAR_NEW = r'''    if (sub === "goalies") return <div className="mb-3"><button type="button" className="text-sm text-blue-600" onClick={() => go("moves", "adddrop")}>{"\u2039 Back to Players"}</button></div>;
    return null; /* change 287: one Players page, no row of pages */'''

SIG_OLD = r'''function GxRankings({ s }) {'''
SIG_NEW = r'''function GxRankings({ s, st287 }) {'''

ST_OLD = r'''  const [nhl203, setNhl203] = useState(rk217.nhl);'''
ST_NEW = ST_OLD + r'''
  const [more287, setMore287] = useState(() => rk217.own !== "all" || rk217.nhl !== "all"); /* change 287: team lists behind More filters */
  const inj287 = (p) => !!(p.ir || (p.status && p.status !== "ACTIVE"));'''

F_OLD = r'''    .filter((p) => (pos === "A" || p.p === pos) && rank[p.id] && (nhl203 === "all" || p.t === nhl203) && '''
F_NEW = r'''    .filter((p) => (pos === "A" || p.p === pos) && (st287 === "inj" ? inj287(p) : rank[p.id]) && (st287 !== "fa" || p.ft === "fa") && (nhl203 === "all" || p.t === nhl203) && '''

RK_OLD = r'''.map((p) => ({ p, rk: pos === "A" ? rankA202[p.id] : rank[p.id], e: pv(p), sf: p.gp ? p.tot / p.gp : null }))'''
RK_NEW = r'''.map((p) => ({ p, rk: (pos === "A" ? rankA202[p.id] : rank[p.id]) || 9999, e: pv(p), sf: p.gp ? p.tot / p.gp : null }))'''

RKV_OLD = r'''<b>{i204 + 1}</b><i>{rk}</i></span>'''
RKV_NEW = r'''<b>{i204 + 1}</b><i>{rk === 9999 ? "\u2013" : rk}</i></span>'''

SEL_START = r'''        <select className={inp} value={own} onChange={(e) => { setOwn(e.target.value); setN(50); }}>'''
SEL_END = r'''        <input className={inp + " flex-1 min-w-[140px]"} placeholder="Search a player" value={q} onChange={(e) => { setQ(e.target.value); setN(50); }} />'''
SEL_NEW = r'''        <input className={inp + " flex-1 min-w-[140px]"} placeholder="Search a player" value={q} onChange={(e) => { setQ(e.target.value); setN(50); }} />
        <button type="button" className={"gx-mf287" + (more287 ? " on" : "")} aria-expanded={more287} onClick={() => { if (more287) { setOwn("all"); setNhl203("all"); setN(50); } setMore287(!more287); }}>{more287 ? "Fewer filters" : "More filters"}</button>
        {more287 && st287 !== "fa" ? (
        <select className={inp} value={own} onChange={(e) => { setOwn(e.target.value); setN(50); }}>
          <option value="all">Every fantasy team</option>
          <option value="rost">On a fantasy team</option>
          <option value="fa">Free agents</option>
          {s.teams.map((t) => <option key={t.id} value={t.id}>{t.name}{t.id === s.me ? " (you)" : ""}</option>)}
        </select>) : null}
        {more287 ? (
        <select className={inp} value={nhl203} onChange={(e) => { setNhl203(e.target.value); setN(50); }} data-gx="203">
          <option value="all">All NHL teams</option>
          {[...new Set(s.players.map((p) => p.t).filter((x) => x && x !== "FA"))].sort().map((x) => <option key={x} value={x}>{x}</option>)}
        </select>) : null}{/* change 287 */}'''


def cut(t, name, start, end, new, done):
    if done in t:
        print(f"(install) {name}: already done")
        return t
    if t.count(start) != 1:
        fail(f"'{name}' start matched {t.count(start)} times")
    a = t.find(start)
    b = t.find(end, a)
    if b < 0:
        fail(f"'{name}' end not found")
    print(f"(install) {name}: updated")
    return t[:a] + new + t[b + len(end):]


def change(t):
    t = lit(t, "287: styles", "</style>", NEW_CSS, "change 287 (install.py)")
    t = lit(t, "287: helpers", ROOT, HELPERS + ROOT, "change 287: Players as one list")
    t = lit(t, "287: route", ROUTE_OLD, ROUTE_NEW, "<GxPlayers287 {...P}")
    t = lit(t, "287: no row of pages", BAR_OLD, BAR_NEW, "change 287: one Players page")
    t = lit(t, "287: list takes a status", SIG_OLD, SIG_NEW, "function GxRankings({ s, st287 })")
    t = lit(t, "287: state", ST_OLD, ST_NEW, "const [more287, setMore287]")
    t = lit(t, "287: status filter", F_OLD, F_NEW, 'st287 === "inj" ? inj287(p)')
    t = lit(t, "287: rank for unranked", RK_OLD, RK_NEW, "|| 9999, e: pv(p)")
    t = lit(t, "287: rank shown", RKV_OLD, RKV_NEW, "rk === 9999 ?")
    t = cut(t, "287: filters row", SEL_START, SEL_END, SEL_NEW, "{/* change 287 */}")
    return t

edit(APP, change)
