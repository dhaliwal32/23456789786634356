# changes/078-rankings-and-any-trade.py - League > Player rankings page (every player ranked by position), and Trades can be built between any two teams

NEW_CSS = r'''  /* change 078 (install.py) */
  .gx-rk { display: grid; grid-template-columns: 38px 26px minmax(0,1fr) 170px 40px 64px 70px; gap: 8px; align-items: center; padding: 8px 0; border-top: 1px solid var(--line); font-variant-numeric: tabular-nums; }
  .gx-rk .n { text-align: right; }
  .gx-rk.me { background: var(--accentSoft); }
  .gx-rkh { font-size: 12px; color: var(--mute); border-top: 0; padding: 0 0 6px; }
  .gx-rkh button { color: var(--mute); text-align: right; }
  .gx-rkh button.on { color: var(--ink); font-weight: 600; text-decoration: underline; text-underline-offset: 3px; }
  @media (max-width: 640px) { .gx-rk { grid-template-columns: 30px 22px minmax(0,1fr) 50px 56px; gap: 6px; } }
</style>'''

HELPERS = r'''// ---------- change 078: player rankings for the whole league, and trades between any two teams (install.py) ----------
const gxYou = (s, you, other) => (!window.__TB_REAL || s.me === window.__TB_REAL ? you : other);
function GxRankings({ s }) {
  const K = s.blend;
  const [pos, setPos] = useState("F");
  const [own, setOwn] = useState("all");
  const [q, setQ] = useState("");
  const [sort, setSort] = useState("exp");
  const [n, setN] = useState(50);
  const pv = (p) => effAvg(p, K) * (p.p === "G" ? p.prob : 1);
  const rank = useMemo(() => {
    const o = {};
    ["F", "D", "G"].forEach((k) => {
      s.players.filter((p) => p.p === k && p.prob > 0 && (p.proj !== false || p.gp > 0)).map((p) => [p.id, pv(p)]).sort((a, b) => b[1] - a[1]).forEach((x, i) => (o[x[0]] = i + 1));
    });
    return o;
  }, [s.players, K, window.__PMODE]);
  const qq = nrm(q);
  const rows = s.players
    .filter((p) => p.p === pos && rank[p.id] && (own === "all" || (own === "rost" ? p.ft !== "fa" : own === "fa" ? p.ft === "fa" : p.ft === own)) && (!qq || nrm(p.n).includes(qq)))
    .map((p) => ({ p, rk: rank[p.id], e: pv(p), sf: p.gp ? p.tot / p.gp : null }))
    .sort((a, b) => (sort === "exp" ? a.rk - b.rk : sort === "sf" ? (b.sf == null ? -99 : b.sf) - (a.sf == null ? -99 : a.sf) : (b.p.tot || 0) - (a.p.tot || 0)));
  const shown = rows.slice(0, n);
  const stTag = (p) => (p.ir ? "IR" : p.status && p.status !== "ACTIVE" ? M_ST[p.status] || p.status.replace(/_/g, " ") : "");
  const owner = (p) => (p.ft === "fa" ? <span className="text-slate-500">{p.wv ? "Waivers" : "Free agent"}</span> : <TL s={s} id={p.ft} className={p.ft === s.me ? "font-semibold" : ""} />);
  const HB = (k, l, cls) => <button type="button" className={"n " + (cls || "") + (sort === k ? " on" : "")} onClick={() => { setSort(k); setN(50); }}>{l}</button>;
  const PN78 = { F: "forwards", D: "defencemen", G: "goalies" };
  return (
    <div className="space-y-3" data-c78="rank">
      <div className="flex flex-wrap items-center gap-2">
        <span className="gx-seg">{[["F", "Forwards"], ["D", "Defence"], ["G", "Goalies"]].map(([k, l]) => <button key={k} type="button" className={pos === k ? "on" : ""} onClick={() => { setPos(k); setN(50); }}>{l}</button>)}</span>
        <select className={inp} value={own} onChange={(e) => { setOwn(e.target.value); setN(50); }}>
          <option value="all">Every player</option>
          <option value="rost">On a fantasy team</option>
          <option value="fa">Free agents</option>
          {s.teams.map((t) => <option key={t.id} value={t.id}>{t.name}{t.id === s.me ? " (you)" : ""}</option>)}
        </select>
        <input className={inp + " flex-1 min-w-[140px]"} placeholder="Search a player" value={q} onChange={(e) => { setQ(e.target.value); setN(50); }} />
      </div>
      <div className="gx-pn"><b></b><b></b><b></b><b></b>
        <div className="gx-rk gx-rkh">
          <span>Rank</span><span></span><span>Player</span><span className="m-hide">Fantasy team</span>
          <span className="n m-hide">GP</span>{HB("sf", "So far")}{HB("exp", "Expected")}
        </div>
        {shown.map(({ p, rk, e, sf }) => {
          const me = p.ft === s.me, st = stTag(p);
          return (
            <div key={p.id} className={"gx-rk" + (me ? " me" : "")}>
              <span className="text-slate-500" style={{ paddingLeft: 4 }}>{rk}</span>
              <TeamLogo t={p.t} size={22} />
              <div className="min-w-0">
                <div className="truncate"><PN p={p} className={me ? "font-semibold" : ""} />{st ? <span className="text-xs" style={{ color: "var(--bad)", marginLeft: 8 }}>{st}</span> : null}</div>
                <div className="text-xs text-slate-500 truncate"><span className="m-inl">{owner(p)}{" · "}</span>{p.t}{sort === "tot" ? " · " + f1(p.tot) + " pts" : ""}</div>
              </div>
              <span className="truncate text-sm m-hide">{owner(p)}</span>
              <span className="n text-slate-500 m-hide">{p.gp || "–"}</span>
              <span className="n">{sf == null ? "–" : f1(sf)}</span>
              <span className="n font-semibold">{f1(e)}</span>
            </div>
          );
        })}
        {!shown.length ? <div className="text-sm text-slate-500" style={{ padding: "10px 0" }}>No {PN78[pos]} match.</div> : null}
        {rows.length > shown.length ? <button type="button" className="text-sm text-blue-600" style={{ marginTop: 10 }} onClick={() => setN(n + 50)}>{"Show 50 more (" + (rows.length - shown.length) + " left)"}</button> : null}
        <div className="text-xs text-slate-500" style={{ paddingTop: 10, marginTop: 10, borderTop: "1px solid var(--line)" }}>
          Rank is each player's place among all {PN78[pos]} by expected points a game{pos === "G" ? ", weighted by how often he starts" : ""}, the same rank shown on team pages. So far is his average this season. <button type="button" className="text-blue-600" onClick={() => { setSort(sort === "tot" ? "exp" : "tot"); setN(50); }}>{sort === "tot" ? "Back to rank order" : "Sort by season total"}</button>
        </div>
      </div>
    </div>
  );
}
'''

OLD_TP = '''function TradesPanel(props) {
  // trades v10: analyzer and 2-for-1 merged into one builder (news_logos.py)
  return <TradeBuilder {...props} />;
}'''
NEW_TP = '''function TradesPanel(props) {
  // trades v10: analyzer and 2-for-1 merged into one builder (news_logos.py)
  // change 078: build a trade from any team's side, not only yours
  const s = props.s;
  const [side, setSide] = useState(s.me);
  window.__TB_REAL = s.me;
  const a = s.teams.some((t) => t.id === side) ? side : s.me;
  const s2 = a === s.me ? s : { ...s, me: a, opp: null };
  const ip = props.initPartner && props.initPartner !== a ? props.initPartner : null;
  return (
    <div>
      <div className="flex items-center gap-2" style={{ marginBottom: 12 }} data-c78="side">
        <span className="text-sm text-slate-500 whitespace-nowrap">Trade from</span>
        <select className={inp + " flex-1"} value={a} onChange={(e) => setSide(e.target.value)}>{s.teams.map((t) => <option key={t.id} value={t.id}>{t.name}{t.id === s.me ? " (you)" : ""}</option>)}</select>
        {a !== s.me ? <button type="button" className="text-xs text-slate-500 underline whitespace-nowrap" onClick={() => setSide(s.me)}>Back to mine</button> : null}
      </div>
      {a !== s.me ? <div className="text-xs text-slate-500" style={{ margin: "-4px 0 12px" }}>{"Showing the trade from " + teamName(s, a).trim() + "'s side. Pick who they trade with below."}</div> : null}
      <TradeBuilder key={a} {...props} s={s2} initPartner={ip} />
    </div>
  );
}'''


def change(t):
    t = lit(t, "078: styles", "</style>", NEW_CSS, "change 078 (install.py)")
    t = lit(t, "078: rankings page and helpers", ROOT, HELPERS + ROOT, "change 078: player rankings for the whole league")
    t = lit(t, "078: League sub-page route",
            'else if (tab === "league") content = sub === "playoffs" ? <PlayoffPlanner {...P} /> : <LeaguePage {...P} />;',
            'else if (tab === "league") content = sub === "playoffs" ? <PlayoffPlanner {...P} /> : sub === "players" ? <GxRankings {...P} /> : <LeaguePage {...P} />;',
            'sub === "players" ? <GxRankings')
    t = lit(t, "078: back to League from rankings",
            'tab === "league" && sub === "playoffs" ? ["League"',
            'tab === "league" && (sub === "playoffs" || sub === "players") ? ["League"',
            '(sub === "playoffs" || sub === "players")')
    t = lit(t, "078: rankings link on League",
            '<button type="button" className="gx-lk" onClick={() => go("league", "playoffs")}>',
            '''<button type="button" className="gx-lk" data-c78="link" onClick={() => go("league", "players")}>
        <span>Player rankings</span><span className="text-sm text-slate-500" style={{ marginLeft: 8 }}>every player by position, and who owns him</span>
        <span className="sec-chev shut" style={{ margin: "0 4px 0 auto" }}></span>
      </button>
      <button type="button" className="gx-lk" onClick={() => go("league", "playoffs")}>''',
            'data-c78="link"')
    t = lit(t, "078: trade from any team", OLD_TP, NEW_TP, "change 078: build a trade from any team's side")
    t = lit(t, "078: label You give", '<div className="gx-tag" style={{ marginBottom: 4 }}>You give</div>',
            '<div className="gx-tag" style={{ marginBottom: 4 }}>{gxYou(s, "You give", teamName(s, s.me) + " gives")}</div>', 'gxYou(s, "You give"')
    t = lit(t, "078: label You get", '<div className="gx-tag" style={{ marginBottom: 4 }}>You get</div>',
            '<div className="gx-tag" style={{ marginBottom: 4 }}>{gxYou(s, "You get", teamName(s, s.me) + " gets")}</div>', 'gxYou(s, "You get"')
    t = lit(t, "078: label Your lineup", '<div className="text-xs text-slate-500">Your lineup</div>',
            '<div className="text-xs text-slate-500 truncate">{gxYou(s, "Your lineup", teamName(s, s.me))}</div>', 'gxYou(s, "Your lineup"')
    t = lit(t, "078: label league rank", 'Your league rank</div>', '{gxYou(s, "Your league rank", "League rank")}</div>', 'gxYou(s, "Your league rank"')
    t = lit(t, "078: label roster after", '"Your roster after: "', 'gxYou(s, "Your roster after: ", teamName(s, s.me) + " after: ")', 'gxYou(s, "Your roster after')
    t = lit(t, "078: label short at", '>This leaves you short at {res.short', '>{gxYou(s, "This leaves you", "This leaves " + teamName(s, s.me).trim())} short at {res.short', 'gxYou(s, "This leaves you"')
    return t


edit(APP, change)
