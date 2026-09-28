// lines-tab.js - the "🏒 Lines" tab for Fantasy Islands GM (loaded by fantasy-gm.html).
// Data: window.LINES_DATA from lines-data.js (written by gm_lines.py every sync).
// Projections come from the app's own functions (passed in as H), so numbers match every other tab.
(function () {
  const { useState, useEffect, useMemo } = React;
  const ES_F = ["F1", "F2", "F3", "F4"], ES_D = ["D1", "D2", "D3"];
  const LBL = { F1: "1st line", F2: "2nd line", F3: "3rd line", F4: "4th line", D1: "top pair", D2: "2nd pair", D3: "3rd pair", PP1: "PP1", PP2: "PP2", G: "goalie" };
  const SHORT = { F1: "L1", F2: "L2", F3: "L3", F4: "L4", D1: "D1", D2: "D2", D3: "D3", PP1: "PP1", PP2: "PP2", G: "G" };
  const MODE = { espn: "ESPN", blend: "Blend", model: "GM model", ai: "AI" };
  const nk = (x) => (x || "").normalize("NFD").replace(/[\u0300-\u036f]/g, "").replace(/[^\x00-\x7f]/g, "").toLowerCase().replace(/\./g, "").replace(/-/g, " ").trim();
  const grpOf = (sl) => (sl === "G" ? "G" : sl && sl[0] !== "P" ? sl[0] : null);
  const ago = (iso) => {
    if (!iso) return "never";
    const m = (Date.now() - Date.parse(iso)) / 6e4;
    if (m < 1) return "just now";
    if (m < 60) return Math.round(m) + " min ago";
    if (m < 2880) return Math.round(m / 60) + " h ago";
    return Math.round(m / 1440) + " days ago";
  };

  function build(s, L) {
    const byKey = {}, byName = {}, byId = {};
    s.players.forEach((p) => {
      const k = nk(p.n);
      byKey[k + "|" + p.p] = byKey[k + "|" + p.p] || p;
      byName[k] = byName[k] || p;
      if (typeof p.id === "string" && p.id[0] === "e") byId[p.id.slice(1)] = p;
    });
    const teams = (L && L.teams) || {};
    const where = {};
    Object.entries(teams).forEach(([t, T]) => {
      const ln = T.lines || {};
      [...ES_F, ...ES_D, "G"].forEach((sl) => (ln[sl] || []).forEach((n) => { const id = nk(n) + "|" + t; where[id] = where[id] || { t, name: n }; if (!where[id].es) where[id].es = sl; }));
      ["PP1", "PP2"].forEach((sl) => (ln[sl] || []).forEach((n) => { const id = nk(n) + "|" + t; where[id] = where[id] || { t, name: n }; if (!where[id].pp) where[id].pp = sl; }));
    });
    const fpOf = (k, g) => {
      for (const x of g ? [g] : ["F", "D"]) {
        const a = ((L && L.fp) || {})[k + "|" + x], b = ((L && L.fpl) || {})[k + "|" + x];
        if (a || b) return { cur: a || null, last: b || null };
      }
      return { cur: null, last: null };
    };
    const pOf = (k, g) => (g && byKey[k + "|" + g]) || byName[k] || null;
    const recent = {}, cutoff = Date.now() - 48 * 36e5;
    ((L && L.changes) || []).forEach((c) => {
      if (Date.parse(c.at) < cutoff || !["line", "lineup", "pp"].includes(c.type)) return;
      const id = c.key + "|" + c.team;
      if (!recent[id]) recent[id] = c.dir === "up" || c.dir === "in" ? "up" : c.dir === "down" || c.dir === "out" ? "down" : "";
    });
    const items = [], seen = new Set();
    s.players.forEach((p) => { const k = nk(p.n), id = k + "|" + p.t; if (seen.has(id)) return; seen.add(id); items.push({ name: p.n, key: k, t: p.t, g: p.p, p }); });
    Object.entries(teams).forEach(([t, T]) => Object.entries(T.lines || {}).forEach(([sl, arr]) => (arr || []).forEach((n) => {
      const k = nk(n), id = k + "|" + t; if (seen.has(id)) return; seen.add(id);
      items.push({ name: n, key: k, t, g: grpOf(sl) || "F", p: pOf(k, grpOf(sl)) });
    })));
    return { byId, where, fpOf, pOf, recent, items, useThis: L && L.fp_use === "this" };
  }

  function Chip({ n, t, g, ctx, s, H, onPick }) {
    const k = nk(n), p = ctx.pOf(k, g);
    const mine = p && p.ft === s.me, fa = p && p.ft === "fa";
    const f = ctx.fpOf(k, g), v = ctx.useThis ? f.cur : f.last;
    const hurt = p && p.status && p.status !== "ACTIVE";
    const ch = ctx.recent[k + "|" + t];
    return (
      <button onClick={() => onPick({ name: n, key: k, t, g: g || (p ? p.p : "F"), p })}
        className={"text-left text-xs px-1.5 py-0.5 rounded border " + (mine ? "bg-blue-50 border-slate-300" : fa ? "bg-green-50 border-green-300" : "border-slate-200")}>
        <span className={mine ? "text-blue-700 font-semibold" : fa ? "text-green-700" : ""}>{n}</span>
        {hurt ? <span className="text-red-600 ml-1" title={p.status}>✚</span> : null}
        {ch ? <span className={"ml-1 " + (ch === "up" ? "text-green-700" : "text-red-600")}>{ch === "up" ? "⬆" : "⬇"}</span> : null}
        <span className="text-slate-400 ml-1">{v ? H.f1(v[0]) : "–"}</span>
      </button>
    );
  }

  function TeamCard({ t, T, rank, sort, ctx, s, H, L, onPick }) {
    const ln = T.lines || {}, st = T.st || {};
    const val = (n, g) => { const f = ctx.fpOf(nk(n), g), v = ctx.useThis ? f.cur : f.last; return v ? v[0] : -1; };
    const row = (sl) => {
      const g = grpOf(sl), arr = [...(ln[sl] || [])].sort((a, b) => val(b, g) - val(a, g));
      if (!arr.length) return null;
      return (
        <div key={sl} className="flex items-start gap-2 py-0.5">
          <span className="text-xs text-slate-500 w-8 shrink-0 pt-0.5">{SHORT[sl]}</span>
          <div className="flex flex-wrap gap-1">{arr.map((n) => <Chip key={n} n={n} t={t} g={g} ctx={ctx} s={s} H={H} onPick={onPick} />)}</div>
        </div>
      );
    };
    const today = H.todayISO();
    const ng = ((L.sched || {})[t] || []).find((x) => x.d >= today);
    return (
      <div className="bg-white rounded-xl border border-slate-200 p-3 text-sm">
        <div className="flex items-baseline gap-2 mb-1">
          <span className="text-lg font-bold">#{rank}</span>
          <span className="font-semibold">{st.name || t}</span>
          <span className="ml-auto text-xs text-slate-500 text-right">
            {sort === "fp" ? `${H.f1(T.fp || 0)} FP` : st.gp ? `${st.pts} pts · ${st.w}-${st.l}-${st.otl}` : "–"}
          </span>
        </div>
        <div className="text-xs text-slate-400 mb-1">
          {sort === "fp" ? (st.gp ? `${st.pts} pts · ${st.w}-${st.l}-${st.otl}` : "") : `${H.f1(T.fp || 0)} fantasy pts in lineup`}
          {ng ? ` · next: ${H.dayLabel(ng.d)} ${ng.h ? "vs" : "@"} ${ng.o}` : ""}
        </div>
        {ES_F.map(row)}{ES_D.map(row)}
        <div className="border-t border-slate-100 mt-1 pt-1">{row("PP1")}{row("PP2")}{row("G")}</div>
        {!ln.F1 && <div className="text-xs text-slate-400">Lines not available yet.</div>}
      </div>
    );
  }

  function PlayerCard({ it, s, wk, H, L, ctx, onClose, onPick }) {
    const K = s.blend, today = H.todayISO(), p = it.p;
    const hasId = !!(p && typeof p.id === "string" && p.id[0] === "e");
    const isG = it.g === "G";
    const w = ctx.where[it.key + "|" + it.t] || null;
    const ln = ((L.teams || {})[it.t] || {}).lines || {};
    const mates = w && w.es && w.es !== "G" ? (ln[w.es] || []).filter((n) => nk(n) !== it.key) : [];
    const f = ctx.fpOf(it.key, it.g);
    const per = (d) => { if (!hasId) return null; const g = isG ? H.gStart(p, d) : null; return { x: H.effAvg(p, K, d) * (g ? g.v : p.prob) * H.avail(p, d), g }; };
    const games = ((L.sched || {})[it.t] || []).filter((x) => x.d >= today).slice(0, 6);
    const wkIdx = hasId ? (wk.games[p.t] || []).filter((i) => ((wk.dates || [])[i] || "") >= today) : [];
    const wkPts = wkIdx.reduce((a, i) => a + ((per(wk.dates[i]) || {}).x || 0), 0);
    const back = hasId ? H.effBack(p) : { d: "" };
    const inj = hasId ? (((window.__SIG || {}).injuries) || {})[p.id.slice(1)] : null;
    const news = hasId ? (H.sigOf(p).news || []) : [];
    const hist = (L.changes || []).filter((c) => c.key === it.key && (c.team === it.t || c.from === it.t || c.to === it.t)).slice(0, 6);
    const fmt = (v) => (v ? `${v[1]} GP · ${H.f1(v[1] ? v[0] / v[1] : 0)}/game` : "no games");
    const hurt = hasId && ((p.status && p.status !== "ACTIVE") || (back.d && back.d > today));
    return (
      <div className="mt-3 border border-slate-200 rounded-xl p-3 bg-slate-50">
        <div className="flex items-start gap-2">
          <div>
            <div className="text-lg font-bold">{it.name}</div>
            <div className="text-xs text-slate-500">
              {isG ? "Goalie" : it.g === "D" ? "Defence" : "Forward"} · {it.t} · {p ? H.teamName(s, p.ft) : "not in your league's ESPN player list"}
              {p && p.own ? ` · ${H.f1(p.own)}% rostered` : ""}{p && p.chg ? ` (${p.chg > 0 ? "+" : ""}${H.f1(p.chg)}%)` : ""}
            </div>
          </div>
          <button className="ml-auto text-xs text-slate-500" onClick={onClose}>✕ close</button>
        </div>
        <div className="mt-2 text-sm">
          {w && w.es ? (
            <span>{isG ? `Goalie for ${it.t}` : `${LBL[w.es]} for ${it.t}`}{mates.length ? " with " : ""}
              {mates.map((n, i) => <span key={n}>{i ? " & " : ""}<button className="underline" onClick={() => onPick({ name: n, key: nk(n), t: it.t, g: grpOf(w.es), p: ctx.pOf(nk(n), grpOf(w.es)) })}>{n}</button></span>)}
            </span>
          ) : <span className="text-amber-600">Not in {it.t}'s current Daily Faceoff lineup (scratched, injured, in the minors, or not read yet)</span>}
          {!isG && <span className="text-slate-500"> · {w && w.pp ? `on ${w.pp}` : "no power-play unit"}</span>}
        </div>
        {hurt && <div className="text-sm text-red-600 mt-1">✚ {String(p.status || "").replace(/_/g, " ")}{back.d ? ` · back around ${H.dayLabel(back.d)} (${back.src})` : ""}{inj && inj.note ? ` — ${inj.note}` : ""}</div>}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-2 mt-3">
          <H.Card label={`${L.season} fantasy pts`} value={f.cur ? H.f1(f.cur[0]) : "–"} sub={fmt(f.cur)} />
          <H.Card label="Last season" value={f.last ? H.f1(f.last[0]) : "–"} sub={fmt(f.last)} />
          <H.Card label="Projection / game" value={hasId ? H.f1(H.effAvg(p, K)) : "–"} sub={hasId ? `${MODE[window.__PMODE] || ""} mode · ESPN ${H.f1(p.pavg)}` : "no projection"} />
          <H.Card label="Rest of this week" value={hasId ? H.f1(wkPts) : "–"} sub={`${wkIdx.length} game${wkIdx.length === 1 ? "" : "s"} left`} />
        </div>
        {games.length > 0 && (
          <div className="mt-3">
            <div className="font-medium text-sm mb-1">Next games</div>
            <table className="w-full text-sm"><tbody>
              {games.map((g) => { const r = per(g.d); return (
                <tr key={g.d} className="border-t border-slate-100">
                  <td className="py-1 pr-2 whitespace-nowrap">{H.dayLabel(g.d)}</td>
                  <td className="py-1 pr-2">{g.h ? "vs" : "@"} {g.o}</td>
                  <td className="py-1 pr-2 text-xs text-slate-500">{r && r.g ? r.g.l || `${Math.round(r.g.v * 100)}% start chance` : ""}</td>
                  <td className="py-1 text-right font-semibold">{r ? H.f1(r.x) : ""}</td>
                </tr>); })}
            </tbody></table>
          </div>
        )}
        {hasId && <div className="mt-2"><H.Tags p={p} K={K} /></div>}
        {news.length > 0 && <div className="mt-3"><div className="font-medium text-sm mb-1">News</div>
          {news.map((n, i) => <div key={i} className="text-xs"><span className="text-slate-400 mr-2">{n.d}</span><a href={n.u} target="_blank" rel="noreferrer" className={"underline " + (n.tone === "-" ? "text-red-600" : "text-slate-600")}>{n.h}</a></div>)}</div>}
        {hist.length > 0 && <div className="mt-3"><div className="font-medium text-sm mb-1">Recent changes</div>
          {hist.map((c) => <div key={c.id} className="text-xs"><span className="text-slate-400 mr-2">{ago(c.at)}</span>{c.text}</div>)}</div>}
      </div>
    );
  }

  function LinesTab({ s, wk, H }) {
    const [, tick] = useState(0);
    const [sel, setSel] = useState(null);
    const [q, setQ] = useState("");
    const [sort, setSort] = useState("standings");
    const [team, setTeam] = useState("all");
    const [onlyMine, setOnlyMine] = useState(false);
    const [feed, setFeed] = useState("all");
    useEffect(() => {
      const id = setInterval(() => {
        const sc = document.createElement("script");
        sc.src = "lines-data.js?t=" + Date.now();
        sc.onload = () => { sc.remove(); tick((x) => x + 1); };
        sc.onerror = () => sc.remove();
        document.head.appendChild(sc);
      }, 3 * 60 * 1000);
      return () => clearInterval(id);
    }, []);
    const L = window.LINES_DATA;
    const ctx = useMemo(() => build(s, L), [s.players, L && L.generated]);
    if (!L) return <H.Section title="🏒 Lines">No line data yet. It appears after the next sync once gm_lines.py is set up.</H.Section>;
    const pick = (it) => { setSel(it); window.scrollTo({ top: 0, behavior: "smooth" }); };
    const qq = nk(q);
    const results = qq.length < 2 ? [] : ctx.items.filter((i) => i.key.includes(qq))
      .sort((a, b) => (b.key.startsWith(qq) - a.key.startsWith(qq)) || ((b.p ? b.p.own : 0) - (a.p ? a.p.own : 0))).slice(0, 8);
    const feedList = (L.changes || []).filter((c) => {
      const p = c.e ? ctx.byId[c.e] : null;
      if (feed === "mine") return p && p.ft === s.me;
      if (feed === "fa") return p && p.ft === "fa";
      if (feed === "lines") return ["line", "lineup", "pp"].includes(c.type);
      if (feed === "moves") return c.type === "move" || c.type === "status";
      return true;
    }).slice(0, 80);
    const icon = { line: "", lineup: "↪", pp: "PP", move: "🔁", status: "✚" };
    const all = Object.entries(L.teams || {}).map(([t, T]) => ({ t, T }));
    const st = (x) => x.T.st || {};
    all.sort(sort === "fp" ? (a, b) => (b.T.fp || 0) - (a.T.fp || 0)
      : (a, b) => (st(b).pts || 0) - (st(a).pts || 0) || (st(b).pct || 0) - (st(a).pct || 0) || ((st(b).gf || 0) - (st(b).ga || 0)) - ((st(a).gf || 0) - (st(a).ga || 0)));
    all.forEach((x, i) => (x.rank = i + 1));
    const myTeams = new Set(s.players.filter((p) => p.ft === s.me).map((p) => p.t));
    const shown = all.filter((x) => (team === "all" || x.t === team) && (!onlyMine || myTeams.has(x.t)));
    return (
      <div className="space-y-4">
        <H.Section title="🔎 Ask about a player" sub="Type any NHL player's name to see his line, power-play unit, season fantasy points, projections, schedule, injury and news in one place.">
          <input className={H.inp + " w-full"} placeholder="Player name, e.g. MacKinnon" value={q} onChange={(e) => setQ(e.target.value)} />
          {results.length > 0 && <div className="flex flex-wrap gap-2 mt-2">{results.map((it) => (
            <button key={it.key + it.t} onClick={() => { setSel(it); setQ(""); }} className="px-2 py-1 rounded-lg border border-slate-300 text-xs">
              {it.name} <span className="text-slate-400">{it.g} · {it.t}{it.p ? " · " + H.teamName(s, it.p.ft) : ""}</span>
            </button>))}</div>}
          {qq.length >= 2 && !results.length && <div className="text-xs text-slate-400 mt-2">No player matches "{q}".</div>}
          {sel && <PlayerCard it={sel} s={s} wk={wk} H={H} L={L} ctx={ctx} onClose={() => setSel(null)} onPick={pick} />}
        </H.Section>
        <H.Section title="📣 Roster & line changes" sub={`Lines and NHL rosters checked ${ago(L.lines_at)}. Your phone gets alerts for your players and for free agents who move into a top role.`}>
          <div className="mb-2"><H.Pills items={[["all", "All"], ["mine", "My players"], ["fa", "Free agents"], ["lines", "Lines & PP"], ["moves", "Trades, call-ups & injuries"]]} value={feed} onChange={setFeed} /></div>
          {feedList.length ? feedList.map((c) => {
            const p = c.e ? ctx.byId[c.e] : null, up = c.dir === "up" || c.dir === "in", down = c.dir === "down" || c.dir === "out";
            return (
              <div key={c.id} className="flex flex-wrap items-baseline gap-2 border-t border-slate-100 py-1.5 text-sm">
                <span className="text-xs text-slate-400 w-20 shrink-0">{ago(c.at)}</span>
                <span className={"text-xs w-6 " + (up ? "text-green-700" : down ? "text-red-600" : "text-slate-500")}>{icon[c.type] || ""}{c.type === "line" ? (up ? "⬆" : down ? "⬇" : "↔") : ""}</span>
                <button className="text-left hover:underline flex-1" onClick={() => pick({ name: c.name, key: c.key, t: c.to && c.type === "move" && c.dir === "in" ? c.to : c.team, g: c.g || (p ? p.p : "F"), p: p || ctx.pOf(c.key, c.g) })}>{c.text}</button>
                {p && p.ft === s.me ? <span className="text-xs text-blue-700 font-semibold">yours</span> : p && p.ft === "fa" ? <span className="text-xs text-green-700">FA</span> : p ? <span className="text-xs text-slate-400">{H.teamName(s, p.ft)}</span> : null}
              </div>);
          }) : <div className="text-slate-400 text-xs">No changes yet. The first read saves a starting point, and changes show up after the next read (every 1–2 hours).</div>}
        </H.Section>
        <H.Section title="🏒 Lines — all 32 teams"
          sub={`Daily Faceoff lines, checked ${ago(L.lines_at)}. ${sort === "fp" ? `Teams sorted by the ${L.fp_season} fantasy points of their current lineup` : `Teams sorted by NHL standings (${L.st_src})`}; players in each line sorted by ${L.fp_season} fantasy points (your scoring). Blue = yours · green = free agent · ✚ = injured · ⬆⬇ = moved in the last 48 h.`}>
          <div className="flex flex-wrap gap-2 items-center">
            <H.Pills items={[["standings", "NHL standings"], ["fp", "Fantasy points"]]} value={sort} onChange={setSort} />
            <select className={H.inp} value={team} onChange={(e) => setTeam(e.target.value)}>
              <option value="all">All teams</option>{all.map((x) => x.t).sort().map((t) => <option key={t} value={t}>{t}</option>)}
            </select>
            <label className="flex items-center gap-1 text-xs"><input type="checkbox" checked={onlyMine} onChange={(e) => setOnlyMine(e.target.checked)} /> Only teams with my players</label>
          </div>
        </H.Section>
        <div className="grid md:grid-cols-2 xl:grid-cols-3 gap-3">
          {shown.map((x) => <TeamCard key={x.t} t={x.t} T={x.T} rank={x.rank} sort={sort} ctx={ctx} s={s} H={H} L={L} onPick={pick} />)}
        </div>
      </div>
    );
  }

  window.LinesTab = LinesTab;
})();
