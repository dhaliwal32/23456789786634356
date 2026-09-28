#!/usr/bin/env python3
"""UI refresh installer for Fantasy Islands GM (round 2: restructure).
Changes fantasy-gm.html, lines-tab.js and ask-panel.js.
Usage: python ui_refresh.py test | live | undo
"""
import pathlib
import re
import sys

FILES = {
    "fantasy-gm.html": ("fantasy-gm-test.html", "fantasy-gm.backup-ui.html"),
    "lines-tab.js": ("lines-tab-test.js", "lines-tab.backup-ui.js"),
    "ask-panel.js": ("ask-panel-test.js", "ask-panel.backup-ui.js"),
}
VS = "\ufe0f?"
DOT = "\u25cf"
STRIP = ("\U0001F3E0\u2694\U0001F501\U0001F3C6\U0001F3D2\U0001F465\u2699\U0001F9EA"
         "\U0001F4CA\U0001F945\U0001F3B2\U0001F525\u2744\u23F1\U0001F4C8\U0001F4F0"
         "\u26D4\u26A0\u2705\u26AA\U0001F4AC\U0001F511\U0001F4E3\U0001F50E")
ARROWS = [("\u2b06" + VS, "\u2191"), ("\u2b07" + VS, "\u2193")]

SCORE_CSS = "  .text-4xl { font-weight: 500 !important; font-size: 2.75rem !important; line-height: 1.1; margin-top: .4rem; margin-bottom: .2rem; letter-spacing: -0.03em; font-variant-numeric: tabular-nums; }"
SETTINGS_DOT = '<span className={ok ? "text-green-700" : "text-slate-400"}>' + DOT + "</span>"

APP = r'''// ---------- App ----------
const NAV = [
  ["today", "Today", null],
  ["myteam", "My Team", null],
  ["matchup", "Matchup", null],
  ["moves", "Moves", [["advice", "Advice"], ["planner", "Planner"], ["adddrop", "Add / Drop"], ["players", "Players"], ["trades", "Trades"], ["playoffs", "Playoffs"]]],
  ["teams", "Teams", null],
  ["lines", "Lines", null],
  ["league", "League", [["power", "Power rankings"], ["standings", "Standings"], ["odds", "Betting lines"]]],
  ["news", "News", null],
  ["setup", "Setup", [["settings", "Settings & backup"], ["sched", "Schedule & weeks"], ["bulk", "Bulk update"], ["inj", "Injury overrides"]]],
];

function App() {
  const [s, setS] = useState(init);
  const [tab, setTab] = useState("today");
  const [subs, setSubs] = useState({ moves: "advice", league: "power", setup: "settings" });
  const [loaded, setLoaded] = useState(false);
  const [status, setStatus] = useState("");
  const [syncMsg, setSyncMsg] = useState("");
  const [teamView, setTeamView] = useState(null);
  const [prevTab, setPrevTab] = useState(null);
  const [player, setPlayer] = useState(null);
  const [tradePartner, setTradePartner] = useState(null);
  const [, tick] = useState(0);
  useEffect(() => {
    let st = init();
    try { const v = JSON.parse(localStorage.getItem(KEY) || "null"); if (v && v.players && v.weeks) st = migrate(v); } catch (e) {}
    const E = window.ESPN_DATA;
    if (E && E.generated && E.generated !== st.lastSync) {
      try { st = applyESPN(st, E); setSyncMsg("Updated"); } catch (e) { setSyncMsg("ESPN file problem: " + e.message); }
    }
    setS(st); setLoaded(true);
  }, []);
  useEffect(() => {
    if (!loaded) return;
    const id = setInterval(() => {
      const sc = document.createElement("script");
      sc.src = "espn-data.js?t=" + Date.now();
      sc.onload = () => {
        sc.remove();
        const E = window.ESPN_DATA;
        tick((x) => x + 1);
        if (!E || !E.generated) return;
        setS((st) => { if (E.generated === st.lastSync) return st; try { const n = applyESPN(st, E); setSyncMsg("Auto-updated " + new Date().toLocaleTimeString([], { hour: "numeric", minute: "2-digit" })); return n; } catch (e) { return st; } });
      };
      sc.onerror = () => sc.remove();
      document.head.appendChild(sc);
    }, 2 * 60 * 1000);
    return () => clearInterval(id);
  }, [loaded]);
  useEffect(() => {
    if (!loaded) return;
    const t = setTimeout(() => { try { localStorage.setItem(KEY, JSON.stringify(s)); setStatus("Saved"); } catch (e) { setStatus("Save failed"); } }, 700);
    return () => clearTimeout(t);
  }, [s, loaded]);
  const E = window.ESPN_DATA;
  window.__MODEL = (E && E.model) || null;
  window.__SIG = (E && E.signals) || null;
  useEffect(() => { fetch("ai/models/ai_proj.json?t=" + Date.now()).then((r) => (r.ok ? r.json() : null)).then((A) => { if (!A || !A.proj || !((Date.now() - Date.parse(A.asof)) / 36e5 < 36)) return; const avg = {}; Object.entries(A.proj).forEach(([id, m]) => { const v = Object.values(m).filter((x) => x != null); if (v.length) avg[id] = v.reduce((a, b) => a + b, 0) / v.length; }); window.__AI = A; window.__AIAVG = avg; setS((st) => ({ ...st, players: [...st.players] })); }).catch(() => {}); }, []);
  window.__PMODE = window.__MODEL ? s.pmode || "blend" : "espn";
  window.__GOALIES = useMemo(() => { const o = {}; Object.entries(s.goalies || {}).forEach(([d, m]) => { o[d] = {}; Object.entries(m || {}).forEach(([n, v]) => { o[d][nrm(n)] = v; }); }); return o; }, [s.goalies]);
  const w0 = s.weeks[s.wk] || s.weeks[0];
  const wk = useMemo(() => deriveWeek(w0, s.autoDone), [w0, s.autoDone]);
  const setWk = (patch) => setS((st) => ({ ...st, weeks: st.weeks.map((w, i) => (i === st.wk ? { ...w, ...(typeof patch === "function" ? patch(w) : patch) } : w)) }));
  const go = (t, sub, extra) => {
    setTab(t); setPlayer(null);
    if (sub) setSubs((x) => ({ ...x, [t]: sub }));
    if (extra && extra.partner) setTradePartner(extra.partner);
    if (t === "teams") setTeamView(null);
    window.scrollTo(0, 0);
  };
  const openTeam = (id) => {
    setPlayer(null);
    if (!id || id === "fa") { go("moves", "adddrop"); return; }
    if (id === s.me) { go("myteam"); return; }
    setPrevTab(tab === "teams" ? null : tab); setTeamView(id); setTab("teams"); window.scrollTo(0, 0);
  };
  const backFromTeam = () => { setTeamView(null); if (prevTab) setTab(prevTab); window.scrollTo(0, 0); };
  window.__NAV = { team: openTeam, player: (p) => { if (p) setPlayer(p); } };
  if (!loaded) return <div className="p-8 text-slate-500">Loading your league…</div>;
  const P = { s, setS, wk, setWk, go };
  const LH = { effAvg, sigOf, Tags, avail, effBack, gStart, teamName, f1, Section, Card, Pills, inp, todayISO, dayLabel, TL };
  const genAt = E && toDate(E.generated);
  const ageH = genAt ? (Date.now() - genAt.getTime()) / 36e5 : null;
  const nav = NAV.find((n) => n[0] === tab);
  const sub = subs[tab];
  let content = null;
  if (tab === "today") content = <Today {...P} />;
  else if (tab === "myteam") content = <MyTeam {...P} />;
  else if (tab === "matchup") content = <Matchup {...P} />;
  else if (tab === "teams") content = teamView ? <TeamPage {...P} id={teamView} back={backFromTeam} /> : <TeamsTab {...P} openTeam={openTeam} />;
  else if (tab === "lines") content = window.LinesTab ? <window.LinesTab {...P} H={LH} /> : <div className="text-slate-400 p-4">The Lines tab could not load (lines-tab.js). Refresh the page; if it keeps happening, check that lines-tab.js is in the repo.</div>;
  else if (tab === "news") content = <NewsView s={s} />;
  else if (tab === "moves") content = sub === "planner" ? <PlannerAll {...P} /> : sub === "adddrop" ? <AddDrop {...P} /> : sub === "players" ? <Players {...P} /> : sub === "trades" ? <TradesPanel key={tradePartner || "none"} {...P} initPartner={tradePartner} /> : sub === "playoffs" ? <PlayoffPlanner {...P} /> : <AdviceAll {...P} />;
  else if (tab === "league") content = sub === "odds" ? <OddsBoard s={s} /> : sub === "standings" ? <League {...P} /> : <PowerRankings {...P} />;
  else if (tab === "setup") content = sub === "sched" ? <Schedule {...P} /> : sub === "bulk" ? <div><Bulk s={s} setS={setS} /><AddOne {...P} /></div> : sub === "inj" ? <InjuryPanel {...P} /> : <Settings {...P} />;
  return (
    <div className="min-h-screen bg-slate-100 text-slate-900">
      <div className="sticky top-0 z-30 bg-slate-900 border-b border-slate-800">
        <div className="max-w-6xl mx-auto px-3 pt-2 pb-1 flex flex-wrap items-center gap-2">
          <div className="font-bold text-lg mr-1 text-white">Fantasy Islands GM</div>
          <select className={inp + " max-w-[210px]"} value={s.wk} onChange={(e) => setS({ ...s, wk: +e.target.value })}>
            {s.weeks.map((w, i) => <option key={i} value={i}>{w.label}</option>)}
          </select>
          <select className={inp} value={window.__PMODE} onChange={(e) => setS({ ...s, pmode: e.target.value, players: [...s.players] })}>
            <option value="espn">Proj: ESPN</option>
            <option value="blend" disabled={!window.__MODEL}>Proj: Blend</option>
            <option value="model" disabled={!window.__MODEL}>Proj: GM model</option><option value="ai" disabled={!window.__MODEL || !window.__AI}>Proj: AI (beta)</option>
          </select>
          <span className={"text-xs px-2 py-1 rounded-full " + (s.lastSync ? (ageH !== null && ageH > 2 ? "bg-red-100 text-red-600" : "bg-green-100 text-green-700") : "bg-slate-200 text-slate-500")}>{s.lastSync ? "● Synced " + fmtTime(s.lastSync) : "Not synced yet"}</span>
          {syncMsg && <span className="text-xs text-green-700 hidden md:inline">{syncMsg}</span>}
          <a href="ai-dashboard.html" className="text-xs text-blue-600 ml-auto">AI Lab</a><span className="text-xs text-slate-500">{status}</span>
        </div>
        <div className="max-w-6xl mx-auto px-2 flex gap-1 overflow-x-auto navscroll">
          {NAV.map(([k, l]) => (
            <button key={k} onClick={() => go(k)} className={"px-3 py-2 text-sm font-medium border-b-2 whitespace-nowrap " + (tab === k ? "border-blue-500 text-white" : "border-transparent text-slate-400 hover:text-white")}>{l}</button>
          ))}
        </div>
      </div>
      {ageH !== null && ageH > 2 && (
        <div className="bg-red-600 text-white text-sm px-4 py-2 text-center">Data is {Math.round(ageH)} hours old — the automatic sync may have stopped. Check GitHub → Actions for a red ✕.</div>
      )}
      <div className="max-w-6xl mx-auto px-3 py-4">
        {nav && nav[2] && <div className="mb-4"><Pills items={nav[2]} value={sub} onChange={(v) => setSubs((x) => ({ ...x, [tab]: v }))} /></div>}
        {content}
        {window.AskPanel ? <window.AskPanel {...P} tab={tab} H={{ effAvg, sigOf, tags, avail, effBack, gStart, teamName, f1, computeMoves, weekProj, oppOf, todayISO }} /> : null}
      </div>
      {player && window.PlayerPopup ? <window.PlayerPopup p={player} s={s} wk={wk} H={LH} onClose={() => setPlayer(null)} /> : null}
    </div>
  );
}

'''

TODAY = r'''// ---------- Today ----------
function Today({ s, wk, go }) {
  const K = s.blend;
  const opp = oppOf(wk, s.me) || s.opp;
  const done = wk.done || 0;
  const mine = s.players.filter((p) => p.ft === s.me), theirs = s.players.filter((p) => p.ft === opp);
  const A = weekProj(mine, wk, K, done), B = weekProj(theirs, wk, K, done);
  const aA = +((wk.act || {})[s.me]) || 0, aB = +((wk.act || {})[opp]) || 0;
  const fa = aA + A.total, fb = aB + B.total, margin = fa - fb;
  const today = todayISO();
  const dates = wk.dates || [];
  const di = dates.findIndex((d) => d >= today);
  const dday = di >= 0 ? dates[di] : null;
  const L = di >= 0 ? dayLineup(mine, wk, di, K) : null, OL = di >= 0 ? dayLineup(theirs, wk, di, K) : null;
  const checks = [];
  if (L) {
    mine.forEach((p) => { if (!p.ir && (wk.games[p.t] || []).includes(di) && avail(p, dday) === 0) checks.push(["bad", `${p.n} (${p.t}) is out — keep him out of your lineup`]); });
    mine.filter((p) => p.p === "G" && !p.ir && (wk.games[p.t] || []).includes(di)).forEach((p) => {
      const g = gStart(p, dday);
      if (g.l === "not starting") checks.push(["bad", `${p.n} is not starting — use another goalie`]);
      else if (g.l === "✓ confirmed") checks.push(["good", `${p.n} confirmed starting`]);
      else checks.push(["warn", `${p.n}: ${g.l || "starter not announced yet"} — check before lock`]);
    });
    if (L.bench.length) checks.push(["warn", `More players than slots — ${L.bench.map((p) => p.n).join(", ")} would sit`]);
    if (L.empty > 0) checks.push(["warn", `${L.empty} empty slot${L.empty > 1 ? "s" : ""} — a streamer could fill ${L.empty > 1 ? "them" : "it"}`]);
  }
  const outNow = mine.filter((p) => { const b = effBack(p).d; return (b && b > today) || (!b && avail(p, today) === 0); });
  const moves = useMemo(() => computeMoves(s, { H: 1, pool: 40 }).res.filter((r) => r.gain >= (s.minGain ?? 3)).slice(0, 3), [s]);
  const sameDrop = moves.length > 1 && moves.every((r) => r.d.id === moves[0].d.id);
  const trend = s.players.filter((p) => p.ft === "fa" && p.prob > 0 && ((formRatio(p, K) || 0) >= 1.25 || (p.chg || 0) >= 5)).sort((a, b) => (b.chg || 0) - (a.chg || 0)).slice(0, 2);
  const hot = mine.filter((p) => !p.ir && (formRatio(p, K) || 0) >= 1.25);
  const cold = mine.filter((p) => { const r = formRatio(p, K); return !p.ir && r !== null && r <= 0.7; });
  const lastName = (n) => nrm(n).split(" ").pop();
  const allNews = mine.map((p) => { const all = sigOf(p).news || []; return { p, all, items: all.filter((n) => nrm(n.h || "").includes(lastName(p.n))) }; });
  const news = allNews.filter((x) => x.items.length).slice(0, 5);
  const hidden = allNews.reduce((a, x) => a + x.all.length - x.items.length, 0);
  const pct = Math.max(6, Math.min(94, 50 + margin / 2));
  const dot = { bad: "text-red-600", warn: "text-amber-600", good: "text-green-700" };
  const daysLeft = dates.length - done;
  const Row = ({ children }) => <div className="flex items-center gap-3 py-2.5 border-t border-slate-100">{children}</div>;
  return (
    <div className="space-y-4">
      <div className="bg-white rounded-xl border border-slate-200 p-4">
        <div className="flex flex-wrap items-center gap-2 text-xs text-slate-500">
          <span className="uppercase tracking-wide">{wk.label}</span><span>·</span><span>{done >= dates.length ? "Final" : `${daysLeft} day${daysLeft === 1 ? "" : "s"} left`}</span>
          <button className="ml-auto text-blue-600" onClick={() => go("matchup")}>All matchups →</button>
        </div>
        <div className="grid grid-cols-[1fr_auto_1fr] gap-4 items-end mt-4">
          <div className="min-w-0"><div className="text-xs text-slate-500 truncate"><TL s={s} id={s.me} /></div><div className="text-4xl">{f1(fa)}</div><div className="text-xs text-slate-500">{f1(aA)} actual + {f1(A.total)} proj</div></div>
          <div className="text-sm text-slate-400 pb-7">vs</div>
          <div className="min-w-0 text-right"><div className="text-xs text-slate-500 truncate"><TL s={s} id={opp} /></div><div className="text-4xl">{f1(fb)}</div><div className="text-xs text-slate-500">{f1(aB)} actual + {f1(B.total)} proj</div></div>
        </div>
        <div className="h-1.5 rounded-full bg-slate-200 mt-5 overflow-hidden"><div className={"h-full rounded-full " + (margin >= 0 ? "bg-green-500" : "bg-red-500")} style={{ width: pct + "%" }}></div></div>
        <div className="flex flex-wrap items-baseline gap-2 mt-3 text-sm"><span className={"font-semibold " + (margin >= 0 ? "text-green-700" : "text-red-600")}>{margin >= 0 ? "Ahead" : "Behind"} by {f1(Math.abs(margin))}</span><span className="text-slate-500">projected{Math.abs(margin) < 15 ? " · close, every move matters" : ""}</span></div>
      </div>
      <div className="grid md:grid-cols-2 gap-4">
        <Section title={dday ? (dday === today ? "Tonight" : `Next game day · ${dayLabel(dday)}`) : "No games left this week"} sub={L ? `${L.start.length} of your players play · projected ${f1(L.total)} vs ${f1(OL.total)}` : ""} link={["Matchup", () => go("matchup")]}>
          {checks.length ? checks.map(([k, t], i) => <Row key={i}><span className={dot[k]}>●</span><span className="text-slate-700">{t}</span></Row>) : <div className="text-green-700">Lineup looks good.</div>}
        </Section>
        <Section title="Best moves this week" sub={sameDrop ? `All free up ${moves[0].d.n}'s spot` : ""} link={["All moves", () => go("moves", "adddrop")]}>
          {moves.length ? moves.map((r) => { const sd = effAvg(r.f, K) - effAvg(r.d, K); const [v, c] = verdict(r.gain, sd); return (
            <Row key={r.f.id}><span className={"text-xs px-2 py-0.5 rounded whitespace-nowrap " + c}>{v}</span><span className="flex-1">Add <PN p={r.f} className="font-semibold" /> <span className="text-xs text-slate-400">{r.f.p} · {r.f.t}</span>{sameDrop ? null : <> · drop <PN p={r.d} className="font-semibold" /></>}</span><span className="text-green-700 font-semibold">+{f1(r.gain)}</span></Row>
          ); }) : <div className="text-slate-400">No move worth an acquisition right now.</div>}
        </Section>
      </div>
      {L && (
        <Section title={`Your lineup · ${dday === today ? "tonight" : dayLabel(dday)}`} sub={`${L.start.length} starting · ${L.bench.length} would sit · ${L.empty} empty slot${L.empty === 1 ? "" : "s"}`} link={["My Team", () => go("myteam")]}>
          <div className="flex flex-wrap gap-2 mt-1">{L.start.map((p) => <span key={p.id} className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg border border-slate-200 text-sm"><span className="text-xs text-slate-400">{p.slot}</span><PN p={p} className="" /><span className="text-xs text-slate-500">{f1(p.x)}</span></span>)}</div>
          {hot.length || cold.length ? (
            <div className="text-sm mt-3 flex flex-wrap gap-x-6 gap-y-1">
              {hot.length ? <span><span className="text-orange-600 font-medium">Hot</span> {hot.map((p, i) => <span key={p.id}>{i ? ", " : " "}<PN p={p} className="" /></span>)}</span> : null}
              {cold.length ? <span><span className="text-sky-600 font-medium">Cold</span> {cold.map((p, i) => <span key={p.id}>{i ? ", " : " "}<PN p={p} className="" /></span>)}</span> : null}
            </div>
          ) : <div className="text-xs text-slate-400 mt-3">Hot and cold streaks show up once players have 3+ games.</div>}
        </Section>
      )}
      {window.LinesSummary ? <window.LinesSummary s={s} wk={wk} go={go} trend={trend} H={{ Section, teamName, f1, TL }} /> : null}
      <div className="grid md:grid-cols-2 gap-4">
        <Section title="Injuries" link={["My Team", () => go("myteam")]}>
          {outNow.length ? outNow.map((p) => { const b = effBack(p); const soon = b.d && dates.length && b.d <= dates[dates.length - 1]; return (
            <Row key={p.id}><PN p={p} /><span className="text-xs text-slate-400">{p.p} · {p.t}{p.ir ? " · IR" : ""}</span><span className={"ml-auto text-xs " + (soon ? "text-green-700 font-semibold" : "text-slate-500")}>{b.d ? "Back " + mdL(b.d) : "No return date"}</span></Row>
          ); }) : <div className="text-green-700">Everyone healthy.</div>}
        </Section>
        <Section title="News on your players" link={["All news", () => go("news")]}>
          {news.length ? news.map(({ p, items }) => (
            <div key={p.id} className="py-2.5 border-t border-slate-100">
              <div><PN p={p} /> <span className="text-xs text-slate-400">{p.p} · {p.t}</span></div>
              {items.slice(0, 2).map((n, i) => <a key={i} href={n.u} target="_blank" rel="noreferrer" className={"block text-sm mt-0.5 hover:underline " + (n.tone === "-" ? "text-red-600" : "text-slate-600")}>{n.h}</a>)}
            </div>
          )) : <div className="text-slate-400">No headlines about your players right now.</div>}
          {hidden > 0 && <div className="text-xs text-slate-400 mt-2">{hidden} general headline{hidden === 1 ? "" : "s"} hidden (they don't mention the player)</div>}
        </Section>
      </div>
    </div>
  );
}

'''

MATCHUP = r'''// ---------- Matchup ----------
function LiveBar({ s, wk, setWk, ids }) {
  const setAct = (id, v) => setWk((w) => ({ act: { ...(w.act || {}), [id]: v } }));
  const auto = s.autoDone && wk.dates && wk.dates.length;
  return (
    <div className="flex flex-wrap gap-3 items-center text-xs text-slate-500 mb-3">
      {auto ? <span>Days completed: <b className="text-slate-700">{wk.done}</b> of {wk.days.length}</span> : (
        <label>Days completed <select className={inp + " ml-1"} value={wk.done} onChange={(e) => setWk({ done: +e.target.value })}><option value={0}>None</option>{wk.days.map((d, i) => <option key={i} value={i + 1}>Through {d}</option>)}</select></label>
      )}
      {ids.map((id) => <label key={id}>{teamName(s, id)} actual <input type="number" step="0.1" className={inp + " w-20 ml-1"} value={(wk.act || {})[id] ?? ""} onChange={(e) => setAct(id, e.target.value)} /></label>)}
      <span>Actual scores fill in from ESPN automatically.</span>
    </div>
  );
}
function Side({ l, s, id }) {
  return (
    <div className="p-3">
      <div className="flex justify-between font-semibold mb-1"><TL s={s} id={id} className="truncate" /><span>{f1(l.total)}</span></div>
      <table className="w-full text-sm"><tbody>
        {l.start.map((p) => (
          <tr key={p.id} className="border-t border-slate-100">
            <td className="py-1.5 pr-2 text-xs text-slate-500 w-10">{p.slot}</td>
            <td className="py-1.5"><PN p={p} className="" /><span className="text-xs text-slate-400 ml-1">{p.t}{p.gs ? "" : p.prob < 1 ? " · " + Math.round(p.prob * 100) + "%" : ""}</span>{p.gs ? <span className={"text-xs ml-1 " + (p.gs.includes("confirmed") && !p.gs.includes("un") ? "text-green-700 font-semibold" : p.gs === "not starting" ? "text-red-600" : "text-amber-600")}>{p.gs}</span> : ""}</td>
            <td className="py-1.5 text-right whitespace-nowrap">{(() => { const o = oddsFor(p.t, p.dt); if (!o || window.__PMODE === "espn") return null; return p.p === "G" ? <span className={"text-xs mr-2 " + (o.win >= 0.55 ? "text-green-700" : o.win <= 0.45 ? "text-red-600" : "text-slate-500")} title="Win chance from betting odds">W {Math.round(o.win * 100)}%</span> : <span className={"text-xs mr-2 " + (o.gf >= 3.3 ? "text-green-700" : o.gf <= 2.7 ? "text-red-600" : "text-slate-400")} title="Team expected goals from betting odds">xG {o.gf.toFixed(1)}</span>; })()}{f1(p.x)}</td>
          </tr>
        ))}
        {l.start.length === 0 && <tr><td className="text-slate-400 py-1">No games</td></tr>}
      </tbody></table>
      {l.bench.length > 0 && <div className="text-xs text-red-600 mt-1">Would sit (no slot): {l.bench.map((p) => p.n).join(", ")}</div>}
      {l.empty > 0 && <div className="text-xs text-slate-500 mt-1">Empty slots: {l.empty}</div>}
    </div>
  );
}
function MatchCard({ s, a, b, P, on, mine, onSel }) {
  const X = P[a], Y = P[b];
  const fx = X.act + X.r.total, fy = Y.act + Y.r.total;
  const pct = Math.max(6, Math.min(94, 50 + (fx - fy) / 2));
  return (
    <div role="button" onClick={onSel} className={"rounded-xl border p-3 cursor-pointer text-sm " + (on ? "border-blue-500 bg-blue-50" : "bg-white border-slate-200")}>
      <div className="text-xs uppercase tracking-wide text-slate-500 mb-1">{mine ? "Your matchup" : "Matchup"}</div>
      <div className="flex justify-between gap-2"><TL s={s} id={a} className={"truncate " + (fx >= fy ? "font-semibold" : "text-slate-500")} /><span className="font-semibold">{f1(fx)}</span></div>
      <div className="flex justify-between gap-2 mt-1"><TL s={s} id={b} className={"truncate " + (fy > fx ? "font-semibold" : "text-slate-500")} /><span className="font-semibold">{f1(fy)}</span></div>
      <div className="h-1 rounded-full bg-slate-200 mt-2 overflow-hidden"><div className="h-full bg-green-500" style={{ width: pct + "%" }}></div></div>
      {X.act || Y.act ? <div className="text-xs text-slate-500 mt-1">Actual so far {f1(X.act)} – {f1(Y.act)}</div> : null}
    </div>
  );
}
function Matchup({ s, setS, wk, setWk }) {
  const K = s.blend, done = wk.done || 0;
  const pairOpp = oppOf(wk, s.me);
  const myPair = [s.me, pairOpp || s.opp];
  const others = (wk.pairs || []).filter((p) => p[0] && p[1] && p[0] !== s.me && p[1] !== s.me);
  const all = [myPair, ...others];
  const [sel, setSel] = useState(0);
  const cur = all[Math.min(sel, all.length - 1)];
  const P = useMemo(() => {
    const o = {};
    all.forEach((pr) => pr.forEach((id) => { if (!id || o[id]) return; o[id] = { r: weekProj(s.players.filter((p) => p.ft === id), wk, K, done), act: +((wk.act || {})[id]) || 0 }; }));
    return o;
  }, [s.players, wk, K, done, s.opp]);
  const [a, b] = cur;
  const A = P[a].r, B = P[b].r, aA = P[a].act, aB = P[b].act;
  const fa = aA + A.total, fb = aB + B.total, margin = fa - fb;
  const final = done >= wk.days.length;
  let run = aA - aB;
  return (
    <div>
      {all.length > 1 && <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3 mb-4">{all.map(([x, y], i) => <MatchCard key={x + "-" + y} s={s} a={x} b={y} P={P} on={i === sel} mine={i === 0} onSel={() => setSel(i)} />)}</div>}
      <div className="flex flex-wrap gap-2 items-center mb-3 text-sm">
        <TL s={s} id={a} className="font-semibold" /><span className="text-slate-500">vs</span>
        {sel === 0 && !pairOpp ? <select className={inp} value={s.opp} onChange={(e) => setS({ ...s, opp: e.target.value })}>{s.teams.filter((t) => t.id !== s.me).map((t) => <option key={t.id} value={t.id}>{t.name}</option>)}</select> : <TL s={s} id={b} className="font-semibold" />}
      </div>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-3">
        <Card label={teamName(s, a)} value={f1(fa)} sub={`${f1(aA)} actual + ${f1(A.total)} proj`} />
        <Card label={teamName(s, b)} value={f1(fb)} sub={`${f1(aB)} actual + ${f1(B.total)} proj`} />
        <Card label={final ? "Final margin" : "Projected margin"} value={(margin >= 0 ? "+" : "") + f1(margin)} tone={margin >= 0 ? "bg-green-50 border-green-200" : "bg-red-50 border-red-200"} />
        <Card label={"Lean · " + teamName(s, a)} value={final ? (margin > 0 ? "WIN" : margin < 0 ? "LOSS" : "TIE") : Math.abs(margin) < 15 ? "Coin flip" : margin > 0 ? (margin > 45 ? "Strong fav" : "Favoured") : margin < -45 ? "Big underdog" : "Underdog"} sub={final ? "Week complete" : `${wk.days.length - done} day(s) left · ${A.wasted} games wasted`} />
      </div>
      <LiveBar s={s} wk={wk} setWk={setWk} ids={[a, b]} />
      {wk.days.map((dl, d) => {
        if (d < done) return <div key={d} className="bg-slate-200 rounded-lg px-3 py-2 mb-2 text-sm text-slate-500">{dl} — completed</div>;
        const x = A.days[d], y = B.days[d]; run += x.total - y.total;
        return (
          <div key={d} className="bg-white rounded-xl border border-slate-200 mb-3">
            <div className="flex justify-between items-center px-3 py-2 border-b border-slate-200 text-sm">
              <span className="font-semibold">{dl}</span>
              <span>{f1(x.total)} – {f1(y.total)} · <span className={run >= 0 ? "text-green-700 font-semibold" : "text-red-700 font-semibold"}>running {run >= 0 ? "+" : ""}{f1(run)}</span></span>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 divide-y md:divide-y-0 md:divide-x divide-slate-200">
              <Side l={x} s={s} id={a} /><Side l={y} s={s} id={b} />
            </div>
          </div>
        );
      })}
      <div className="text-xs text-slate-500">Lineups auto-optimized (9 F, 5 D, 1 UTIL, 2 G). W % / xG = betting line for that game. Tap any matchup above to switch.</div>
    </div>
  );
}

'''

LEAGUE = r'''// ---------- League ----------
// (this week's matchups moved to the Matchup tab)
function League({ s, wk }) {
  const K = s.blend, done = wk.done || 0;
  const P = {};
  s.teams.forEach((t) => { const r = weekProj(s.players.filter((p) => p.ft === t.id), wk, K, done); const a = +((wk.act || {})[t.id]) || 0; P[t.id] = { ...r, a, fin: a + r.total }; });
  const rec = {}; s.teams.forEach((t) => (rec[t.id] = { w: 0, l: 0, ties: 0, pf: 0 }));
  s.weeks.forEach((w) => {
    const len = (w.dates || w.days || []).length;
    if (!len || effDone(w, s.autoDone) < len) return;
    (w.pairs || []).forEach(([a, b]) => {
      if (!rec[a] || !rec[b]) return;
      const x = +((w.act || {})[a]) || 0, y = +((w.act || {})[b]) || 0;
      if (!x && !y) return;
      rec[a].pf += x; rec[b].pf += y;
      if (x > y) { rec[a].w++; rec[b].l++; } else if (y > x) { rec[b].w++; rec[a].l++; } else { rec[a].ties++; rec[b].ties++; }
    });
  });
  const stand = s.teams.map((t) => ({ team: t, ...rec[t.id] })).sort((a, b) => b.w - a.w || b.pf - a.pf);
  return (
    <div className="space-y-4">
      <Section title="Standings" sub="Completed weeks. Top 6 make the playoffs. This week's matchups are on the Matchup tab.">
        <div className="overflow-x-auto"><table className="w-full text-sm">
          <thead className="text-left"><tr>{["#", "Team", "W", "L", "T", "PF"].map((h) => <th key={h} className="px-2 py-2">{h}</th>)}</tr></thead>
          <tbody>{stand.map((r, i) => (
            <tr key={r.team.id} className={"border-t border-slate-100 " + (r.team.id === s.me ? "bg-blue-50 font-semibold" : "") + (i === 5 ? " border-b-2 border-b-slate-400" : "")}>
              <td className="px-2 py-2">{i + 1}</td><td className="px-2 py-2"><TL s={s} id={r.team.id} /></td><td className="px-2 py-2">{r.w}</td><td className="px-2 py-2">{r.l}</td><td className="px-2 py-2">{r.ties}</td><td className="px-2 py-2">{f1(r.pf)}</td>
            </tr>
          ))}</tbody>
        </table></div>
      </Section>
      <Section title="All teams this week" sub="Actual + projected for the remaining days.">
        <div className="overflow-x-auto"><table className="w-full text-sm">
          <thead className="text-left"><tr>{["Team", "Actual", "Remaining", "Projected final", "Games left", "Wasted"].map((h) => <th key={h} className="px-2 py-2">{h}</th>)}</tr></thead>
          <tbody>{s.teams.map((t) => ({ team: t, ...P[t.id] })).sort((a, b) => b.fin - a.fin).map((r) => (
            <tr key={r.team.id} className={"border-t border-slate-100 " + (r.team.id === s.me ? "bg-blue-50 font-semibold" : "")}>
              <td className="px-2 py-2"><TL s={s} id={r.team.id} /></td><td className="px-2 py-2">{f1(r.a)}</td><td className="px-2 py-2">{f1(r.total)}</td><td className="px-2 py-2">{f1(r.fin)}</td><td className="px-2 py-2">{r.used}</td><td className="px-2 py-2">{r.wasted}</td>
            </tr>
          ))}</tbody>
        </table></div>
      </Section>
    </div>
  );
}

'''

PLAYERLINE = r'''const PlayerLine = ({ s, p, extra }) => (
  <div className="flex flex-wrap items-baseline gap-2 border-t border-slate-100 py-2 text-sm">
    <PN p={p} /><span className="text-xs text-slate-400">{p.p} · {p.t} · <TL s={s} id={p.ft} /></span>
    <span className="text-xs text-slate-500">avg {f1(effAvg(p, s.blend))}</span>{extra}<Tags p={p} K={s.blend} />
  </div>
);
'''

NEWBLOCK = r'''// ---------- Clickable names, team pages, My Team (UI refresh) ----------
const TL = ({ s, id, className }) => {
  if (!id) return null;
  const nm = teamName(s, id);
  if (id === "fa") return <span className={className || ""}>{nm}</span>;
  return <button type="button" className={"hover:underline text-left " + (className || "")} onClick={(e) => { e.stopPropagation(); if (window.__NAV) window.__NAV.team(id); }}>{nm}</button>;
};
const PN = ({ p, className }) => (
  <button type="button" className={"hover:underline text-left " + (className === undefined ? "font-medium" : className)} onClick={(e) => { e.stopPropagation(); if (window.__NAV) window.__NAV.player(p); }}>{p.n}</button>
);

let __LT = null;
function leagueTable(s) {
  const key = [s.players, s.weeks, s.wk, s.blend, s.autoDone, window.__PMODE];
  if (__LT && __LT.key.every((v, i) => v === key[i])) return __LT.v;
  const K = s.blend, today = todayISO();
  const rows = s.teams.map((t) => {
    const r = s.players.filter((p) => p.ft === t.id);
    let ros = 0, n4 = 0, days = 0;
    s.weeks.slice(s.wk).forEach((w, i) => { const dw = deriveWeek(w, s.autoDone); const from = i === 0 ? dw.done : 0; const v = weekProj(r, dw, K, from).total; ros += v; if (i < 4) n4 += v; days += Math.max(0, dw.days.length - from); });
    const perGame = (pos, n) => r.filter((p) => p.p === pos && !p.ir && avail(p, today) > 0).map((p) => effAvg(p, K) * (pos === "G" ? p.prob : 1)).sort((a, b) => b - a).slice(0, n).reduce((a, b) => a + b, 0);
    const grp = { F: perGame("F", 10), D: perGame("D", 5), G: perGame("G", 2) };
    const out = r.filter((p) => p.ir || avail(p, today) === 0).length;
    return { t, ros, n4, strength: days ? (ros / days) * 7 : 0, grp, out };
  });
  const rec = {}; s.teams.forEach((t) => (rec[t.id] = { w: 0, l: 0, t: 0, pf: 0, n: 0 }));
  s.weeks.forEach((w) => {
    const len = (w.dates || []).length;
    if (!len || effDone(w, s.autoDone) < len) return;
    (w.pairs || []).forEach(([a, b]) => {
      if (!rec[a] || !rec[b]) return;
      const x = +((w.act || {})[a]) || 0, y = +((w.act || {})[b]) || 0;
      if (!x && !y) return;
      rec[a].pf += x; rec[b].pf += y; rec[a].n++; rec[b].n++;
      if (x > y) { rec[a].w++; rec[b].l++; } else if (y > x) { rec[b].w++; rec[a].l++; } else { rec[a].t++; rec[b].t++; }
    });
  });
  rows.forEach((x) => (x.rec = rec[x.t.id]));
  rows.sort((a, b) => b.strength - a.strength);
  const grpRank = {};
  ["F", "D", "G"].forEach((k) => { [...rows].sort((a, b) => b.grp[k] - a.grp[k]).forEach((x, i) => { grpRank[x.t.id] = { ...(grpRank[x.t.id] || {}), [k]: i + 1 }; }); });
  const v = { rows, grpRank };
  __LT = { key, v };
  return v;
}
const recTxt = (r) => (r && r.n ? `${r.w}-${r.l}${r.t ? "-" + r.t : ""}` : "–");
const RankSpans = ({ g }) => <span>{["F", "D", "G"].map((k) => <span key={k} className={"mr-2 " + (g[k] <= 3 ? "text-green-700" : g[k] >= 8 ? "text-red-600" : "")}>{k} #{g[k]}</span>)}</span>;

function RosterView({ s, wk, team }) {
  const K = s.blend, done = wk.done || 0;
  const roster = s.players.filter((p) => p.ft === team);
  const order = { F: 0, D: 1, G: 2 };
  const sorted = [...roster].sort((a, b) => (a.ir ? 1 : 0) - (b.ir ? 1 : 0) || order[a.p] - order[b.p] || effAvg(b, K) - effAvg(a, K));
  const Ls = wk.days.map((_, d) => (d < done ? null : dayLineup(roster, wk, d, K)));
  const wkPts = (p) => Ls.reduce((a, L) => { if (!L) return a; const x = L.start.find((y) => y.id === p.id); return a + (x ? x.x : 0); }, 0);
  const left = (p) => (wk.games[p.t] || []).filter((d) => d >= done).length;
  return (
    <div className="overflow-x-auto">
      <table className="w-full text-sm">
        <thead className="text-left"><tr>{["Player", "", "Proj / game", "Games left", "Week pts", "Signals"].map((h, i) => <th key={i} className="px-2 py-2">{h}</th>)}</tr></thead>
        <tbody>{sorted.map((p) => (
          <tr key={p.id} className="border-t border-slate-100 align-top">
            <td className="px-2 py-2 whitespace-nowrap"><PN p={p} />{p.ir ? <span className="text-red-600 text-xs ml-1">IR</span> : p.status && p.status !== "ACTIVE" ? <span className="text-red-600 text-xs ml-1">{p.status.replace(/_/g, " ")}</span> : null}</td>
            <td className="px-2 py-2 text-xs text-slate-500 whitespace-nowrap">{p.p} · {p.t}</td>
            <td className="px-2 py-2">{f1(effAvg(p, K))}</td>
            <td className="px-2 py-2">{p.ir ? "–" : left(p)}</td>
            <td className="px-2 py-2 font-semibold">{p.ir ? "–" : f1(wkPts(p))}</td>
            <td className="px-2 py-2 min-w-[160px]"><Tags p={p} K={K} /></td>
          </tr>
        ))}</tbody>
      </table>
    </div>
  );
}

function MyTeam({ s, setS, wk, go }) {
  const K = s.blend, today = todayISO();
  const T = leagueTable(s);
  const meRow = T.rows.find((r) => r.t.id === s.me);
  const rank = meRow ? T.rows.indexOf(meRow) + 1 : null;
  const g = T.grpRank[s.me] || {};
  const posName = { F: "forwards", D: "defence", G: "goalies" };
  const need = { F: 10, D: 5, G: 2 };
  const by = ["F", "D", "G"].sort((a, b) => (g[b] || 0) - (g[a] || 0));
  const weak = by[0], strong = by[2];
  const pv = (p) => effAvg(p, K) * (p.p === "G" ? p.prob : 1);
  const roster = s.players.filter((p) => p.ft === s.me);
  const chips = roster.filter((p) => !p.ir && p.p === strong).sort((a, b) => pv(b) - pv(a)).slice(need[strong]);
  const order = { F: 0, D: 1, G: 2 };
  const sorted = [...roster].sort((a, b) => (a.ir ? 1 : 0) - (b.ir ? 1 : 0) || order[a.p] - order[b.p] || effAvg(b, K) - effAvg(a, K));
  const done = wk.done || 0;
  const Ls = wk.days.map((_, d) => (d < done ? null : dayLineup(roster, wk, d, K)));
  const cell = (p, d) => { if (p.ir || !(wk.games[p.t] || []).includes(d)) return "none"; const L = Ls[d]; if (!L) return "past"; if (L.start.some((x) => x.id === p.id)) return "start"; if (L.bench.some((x) => x.id === p.id)) return "sit"; return "out"; };
  const CELL = { start: "bg-green-500", sit: "bg-amber-500", out: "bg-red-500", past: "bg-slate-200" };
  const tot = Ls.reduce((a, L) => a + (L ? L.total : 0), 0);
  const sits = Ls.reduce((a, L) => a + (L ? L.bench.length : 0), 0);
  const cnt = { F: 0, D: 0, G: 0 }; roster.forEach((p) => { if (!p.ir) cnt[p.p]++; });
  const irN = roster.filter((p) => p.ir).length;
  const outList = roster.filter((p) => { const b = effBack(p).d; return p.ir || (b && b > today) || (!b && avail(p, today) === 0) || (p.status && p.status !== "ACTIVE"); });
  const upd = (id, patch) => setS((st) => ({ ...st, players: st.players.map((p) => (p.id === id ? { ...p, ...patch } : p)) }));
  const protectTop = s.protectTop ?? 8;
  const auto = new Set(roster.filter((p) => !p.ir).sort((a, b) => effAvg(b, K) - effAvg(a, K)).slice(0, protectTop).map((p) => p.id));
  return (
    <div className="space-y-4">
      <div className="bg-white rounded-xl border border-slate-200 p-4">
        <div className="text-xs uppercase tracking-wide text-slate-500">{rank ? `Power rank #${rank} of ${T.rows.length}` : "My team"}</div>
        <div className="text-2xl font-bold mt-1">{teamName(s, s.me)}</div>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mt-4">
          <Card label="Strength" value={meRow ? f1(meRow.strength) : "–"} sub="projected pts per week" />
          <Card label="Group ranks" value={<RankSpans g={g} />} sub={`Weakest: ${posName[weak]}`} />
          <Card label="This week" value={f1(tot)} sub={`projected in your lineup · ${sits} game${sits === 1 ? "" : "s"} would sit`} />
          <Card label="Roster" value={`${roster.length - irN}/22`} sub={`F ${cnt.F} · D ${cnt.D} · G ${cnt.G}${irN ? ` · ${irN} IR` : ""}`} />
        </div>
        <div className="text-sm text-slate-600 mt-3">{weak !== strong && chips.length ? <>Trade chips from your {posName[strong]}: {chips.map((p, i) => <span key={p.id}>{i ? ", " : ""}<PN p={p} className="" /></span>)}. Use them to upgrade your {posName[weak]}.</> : `Your weakest group is ${posName[weak]}. Look for upgrades in Moves.`} <button className="text-blue-600 ml-1" onClick={() => go("moves", "trades")}>Open Trades →</button></div>
      </div>
      <Section title="Roster" sub="Lineup order: forwards, defence, goalies, then IR. Week pts = projected points in your daily lineup for the rest of this week. Tap a player for details.">
        <RosterView s={s} wk={wk} team={s.me} />
      </Section>
      <Section title="This week, day by day" sub="Violet = in your lineup · amber = plays but would sit (no open slot) · red = out · grey = already played.">
        <div className="overflow-x-auto">
          <table className="text-sm w-full">
            <thead><tr><th className="px-2 py-2 text-left">Player</th>{wk.days.map((d, i) => <th key={i} className="px-1 py-2 text-center">{d.split(",")[0]}</th>)}</tr></thead>
            <tbody>
              {sorted.filter((p) => !p.ir).map((p) => (
                <tr key={p.id} className="border-t border-slate-100">
                  <td className="px-2 py-1 whitespace-nowrap"><PN p={p} className="" /> <span className="text-xs text-slate-400">{p.p}</span></td>
                  {wk.days.map((_, d) => { const c = cell(p, d); return <td key={d} className="px-1 py-1 text-center">{c === "none" ? <span className="text-slate-400">·</span> : <span className={"inline-block w-6 h-3 rounded " + CELL[c]}></span>}</td>; })}
                </tr>
              ))}
              <tr className="border-t-2 border-slate-300">
                <td className="px-2 py-2 text-xs text-slate-500">Lineup filled</td>
                {Ls.map((L, d) => <td key={d} className={"text-center text-xs py-2 " + (L && L.bench.length ? "text-amber-600 font-semibold" : "text-slate-500")}>{L ? `${L.start.length}/17` : "done"}{L && L.bench.length ? ` · ${L.bench.length} sit` : ""}</td>)}
              </tr>
            </tbody>
          </table>
        </div>
      </Section>
      <Section title="Injuries & settings" sub="Return dates fill in from ESPN automatically; pick a date to override. Protected players are never suggested as drops.">
        {outList.length ? outList.map((p) => { const eb = effBack(p); return (
          <div key={p.id} className="flex flex-wrap items-center gap-2 py-2 border-t border-slate-100">
            <PN p={p} /><span className="text-xs text-slate-400">{p.p} · {p.t}{p.ir ? " · IR" : ""}</span>
            <span className="text-xs text-red-600">{(p.status || "").replace(/_/g, " ")}</span>
            <span className="ml-auto flex items-center gap-2">
              <input type="date" className={inp} value={eb.d} onChange={(e) => upd(p.id, { back: e.target.value })} />
              <span className="text-xs text-slate-500">{eb.src ? (eb.src === "you" ? "set by you" : "auto: " + eb.src) : ""}</span>
              {p.back ? <button className="text-xs text-red-600" onClick={() => upd(p.id, { back: "" })}>Clear</button> : null}
            </span>
          </div>
        ); }) : <div className="text-green-700">Everyone healthy.</div>}
        <div className="font-medium mt-4 mb-2">Protected players</div>
        <div className="flex flex-wrap gap-2">
          {roster.map((p) => { const a = auto.has(p.id), on = p.ir || a || p.keep; return (
            <label key={p.id} className={"flex items-center gap-1 px-2 py-1 rounded-full border text-xs " + (p.ir ? "text-slate-400 border-slate-200" : on ? "bg-green-50 border-green-300" : "border-slate-300")}>
              <input type="checkbox" disabled={p.ir || a} checked={!!on} onChange={(e) => upd(p.id, { keep: e.target.checked })} />{p.n}{p.ir ? " (IR)" : a ? " (auto)" : ""}
            </label>
          ); })}
        </div>
        <div className="text-xs text-slate-500 mt-1">Your top {protectTop} are protected automatically (change the number in Moves → Add / Drop → Settings).</div>
        <details className="mt-4"><summary className="cursor-pointer text-sm text-blue-600">Edit projections, play %, IR and return dates for every player</summary><div className="mt-3"><RosterTable s={s} setS={setS} wk={wk} team={s.me} /></div></details>
      </Section>
    </div>
  );
}

function TeamsTab({ s, wk, openTeam }) {
  const T = leagueTable(s);
  return (
    <Section title="Teams" sub="Every team in your league, ordered by power ranking. Tap a team to see its roster, its week and how it fits with yours for trades.">
      <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-3 mt-2">
        {T.rows.map((x, i) => { const g = T.grpRank[x.t.id] || {}; const o = oppOf(wk, x.t.id); const me = x.t.id === s.me; return (
          <div key={x.t.id} role="button" onClick={() => openTeam(x.t.id)} className={"rounded-xl border p-4 cursor-pointer hover:border-slate-400 " + (me ? "border-blue-500 bg-blue-50" : "border-slate-200 bg-slate-50")}>
            <div className="flex items-baseline gap-2"><span className="text-slate-400 text-sm">#{i + 1}</span><span className="font-semibold truncate">{x.t.name}</span>{me && <span className="text-xs text-blue-600 ml-auto">You</span>}</div>
            <div className="text-xs text-slate-500 mt-1">{x.rec && x.rec.n ? `${recTxt(x.rec)} · ${f1(x.rec.pf)} PF · ` : ""}{f1(x.strength)} pts/wk projected</div>
            <div className="text-xs mt-2"><RankSpans g={g} /></div>
            <div className="text-xs text-slate-500 mt-2">{o ? `This week vs ${teamName(s, o)}` : "No matchup loaded"}{x.out ? ` · ${x.out} out` : ""}</div>
          </div>
        ); })}
      </div>
    </Section>
  );
}

function TeamPage({ s, wk, id, back, go }) {
  const K = s.blend;
  const T = leagueTable(s);
  const x = T.rows.find((r) => r.t.id === id);
  if (!x) return <Section title="Team not found"><button className="text-blue-600" onClick={back}>← Back</button></Section>;
  const rank = T.rows.indexOf(x) + 1, g = T.grpRank[id] || {}, mg = T.grpRank[s.me] || {};
  const roster = s.players.filter((p) => p.ft === id);
  const done = wk.done || 0, o = oppOf(wk, id);
  const act = (t) => +((wk.act || {})[t]) || 0;
  const mine = weekProj(roster, wk, K, done), theirs = o ? weekProj(s.players.filter((p) => p.ft === o), wk, K, done) : null;
  const posName = { F: "forwards", D: "defence", G: "goalies" };
  const need = { F: 10, D: 5, G: 2 };
  const myWeak = ["F", "D", "G"].sort((a, b) => (mg[b] || 0) - (mg[a] || 0))[0];
  const theyStrong = ["F", "D", "G"].filter((k) => g[k] < mg[k]);
  const pv = (p) => effAvg(p, K) * (p.p === "G" ? p.prob : 1);
  const myAt = s.players.filter((p) => p.ft === s.me && !p.ir && p.p === myWeak).map(pv).sort((a, b) => b - a);
  const bar = myAt.length ? myAt[Math.min(need[myWeak], myAt.length) - 1] : 0;
  const targets = roster.filter((p) => !p.ir && p.p === myWeak && pv(p) > bar).sort((a, b) => pv(b) - pv(a)).slice(0, 4);
  const news = roster.filter((p) => (sigOf(p).news || []).length).slice(0, 6);
  return (
    <div className="space-y-4">
      <button className="text-sm text-blue-600" onClick={back}>← Back</button>
      <div className="bg-white rounded-xl border border-slate-200 p-4">
        <div className="text-xs uppercase tracking-wide text-slate-500">Power rank #{rank} of {T.rows.length}</div>
        <div className="text-2xl font-bold mt-1">{x.t.name}</div>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mt-4">
          <Card label="Record" value={recTxt(x.rec)} sub={x.rec && x.rec.n ? `${f1(x.rec.pf)} points for` : "no completed weeks yet"} />
          <Card label="Strength" value={f1(x.strength)} sub="projected pts per week" />
          <Card label="Group ranks" value={<RankSpans g={g} />} sub={`among ${T.rows.length} teams`} />
          <Card label="Players out" value={x.out} sub="injured or on IR" />
        </div>
      </div>
      <div className="grid md:grid-cols-2 gap-4">
        <Section title="Their week" sub={wk.label} link={["All matchups", () => go("matchup")]}>
          {o ? (
            <div>
              <div className="flex justify-between py-2"><span className="font-medium">{x.t.name}</span><span className="font-semibold">{f1(act(id) + mine.total)}</span></div>
              <div className="flex justify-between py-2 border-t border-slate-100"><TL s={s} id={o} /><span className="font-semibold">{f1(act(o) + theirs.total)}</span></div>
              <div className="text-xs text-slate-500 mt-1">{mine.used} lineup games left · {mine.wasted} would sit · {mine.empty} empty slots</div>
            </div>
          ) : <div className="text-slate-400">No matchup loaded for this week.</div>}
        </Section>
        <Section title="Trade fit with you" sub={`Your weakest group: ${posName[myWeak]} (#${mg[myWeak]}). Theirs: F #${g.F} · D #${g.D} · G #${g.G}.`}>
          {theyStrong.length ? <div className="mb-2">They're stronger than you at <b>{theyStrong.map((k) => posName[k]).join(" and ")}</b>.</div> : <div className="mb-2 text-slate-500">They're not stronger than you anywhere, so trade only for specific players.</div>}
          <div className="font-medium mt-2 mb-1">Players who'd upgrade your {posName[myWeak]}</div>
          {targets.length ? targets.map((p) => <div key={p.id} className="flex gap-2 py-1.5 border-t border-slate-100"><PN p={p} /><span className="text-xs text-slate-400">{p.p} · {p.t}</span><span className="ml-auto text-xs text-slate-500">{f1(pv(p))}/game</span></div>) : <div className="text-xs text-slate-400">None of their {posName[myWeak]} beat your current starters.</div>}
          <button className="bg-blue-600 rounded-lg px-3 py-1.5 mt-3 text-sm font-semibold" onClick={() => go("moves", "trades", { partner: id })}>Trade with them</button>
        </Section>
      </div>
      <Section title="Roster" sub="Lineup order: forwards, defence, goalies, then IR. Tap a player for details.">
        <RosterView s={s} wk={wk} team={id} />
      </Section>
      {news.length > 0 && <Section title="News">{news.map((p) => <PlayerLine key={p.id} s={s} p={p} />)}</Section>}
    </div>
  );
}

function AdviceAll({ s }) {
  return <div className="space-y-4"><AdvicePanel s={s} /><EdgesPanel s={s} /></div>;
}
function PlannerAll(props) {
  return <div className="space-y-4"><AcqPlanner {...props} /><BenchFixer {...props} /></div>;
}
function TradesPanel(props) {
  const [m, setM] = useState("build");
  return (
    <div className="space-y-4">
      <Pills items={[["build", "Trade analyzer"], ["two", "2-for-1 builder"]]} value={m} onChange={setM} />
      {m === "build" ? <TradeAnalyzer {...props} /> : <TwoForOne {...props} />}
    </div>
  );
}

'''

SUMMARY = r'''  // ---------- compact summary for the Today screen ----------
  function LinesSummary({ s, wk, go, trend, H }) {
    const L = window.LINES_DATA;
    const pr = (wk.pairs || []).find((x) => x[0] && x[1] && (x[0] === s.me || x[1] === s.me));
    const opp = pr ? (pr[0] === s.me ? pr[1] : pr[0]) : s.opp;
    const ctx = useMemo(() => build(s, L), [s.players, L && L.generated]);
    const items = useMemo(() => enrich(L, ctx, s, opp), [ctx, opp, L && L.generated]);
    if (!L) return null;
    const imp = items.filter((x) => x.s >= TH);
    const mine = imp.filter((x) => x.ok === "me" || (x.ok !== "fa" && x.mates.length > 0)).slice(0, 4);
    const tr = (trend || []).slice(0, 2);
    const fa = imp.filter((x) => x.ok === "fa").slice(0, Math.max(2, 4 - tr.length));
    const open = () => go("lines");
    const head = (t) => <div className="text-xs uppercase tracking-wide text-slate-400 mb-1">{t}</div>;
    return (
      <H.Section title="Line changes" sub={`Checked ${ago(L.lines_at)} · ${imp.length} of ${items.length} changes matter to you`} link={["Open Lines", open]}>
        <div className="grid md:grid-cols-2 gap-x-8 gap-y-4">
          <div>
            {head("Your team")}
            {mine.length ? mine.map((x) => <Row key={x.c.id} x={x} s={s} H={H} onPick={open} />) : <div className="lt-msg">No changes for your players.</div>}
          </div>
          <div>
            {head("Pickup targets")}
            {fa.map((x) => <Row key={x.c.id} x={x} s={s} H={H} onPick={open} />)}
            {tr.map((p) => (
              <div key={p.id} className="lt-it" onClick={() => go("moves", "adddrop")}>
                <span className="lt-ic lt-up">↗</span>
                <div style={{ minWidth: 0 }}>
                  <div className="text-sm"><b>{p.n}</b> <span className="lt-tm">{p.t} · {p.p}</span> trending</div>
                  <div className="lt-why">{(p.chg || 0) >= 5 ? `+${H.f1(p.chg)}% rostered this week` : "Hot over the last 14 days"}</div>
                </div>
                <span className="lt-own fa">FA</span>
              </div>
            ))}
            {!fa.length && !tr.length && <div className="lt-msg">No free agents moving up right now.</div>}
          </div>
        </div>
        <div className="lt-bar"><span>{items.length - imp.length} minor changes hidden</span><button className="lt-link" style={{ padding: 0 }} onClick={open}>See all {items.length} in Lines →</button></div>
      </H.Section>
    );
  }

  // ---------- player pop-up used everywhere in the app ----------
  function PlayerPopup({ p, s, wk, H, onClose }) {
    const L = window.LINES_DATA || { teams: {}, changes: [], sched: {}, season: "This season" };
    const ctx = useMemo(() => build(s, L), [s.players, L && L.generated]);
    const [it, setIt] = useState(null);
    useEffect(() => { setIt(null); }, [p && p.id]);
    useEffect(() => { const k = (e) => { if (e.key === "Escape") onClose(); }; window.addEventListener("keydown", k); return () => window.removeEventListener("keydown", k); }, []);
    const real = s.players.find((q) => q.id === p.id) || p;
    const cur = it || { name: real.n, key: nk(real.n), t: real.t, g: real.p, p: real };
    return (
      <div className="fixed inset-0 z-50 overflow-y-auto" style={{ background: "rgba(0,0,0,.65)" }} onClick={onClose}>
        <div className="max-w-2xl mx-auto my-10 px-3" onClick={(e) => e.stopPropagation()}>
          <PlayerCard it={cur} s={s} wk={wk} H={H} L={L} ctx={ctx} onClose={onClose} onPick={setIt} />
        </div>
      </div>
    );
  }

  window.PlayerPopup = PlayerPopup;
  window.LinesSummary = LinesSummary;
  window.LinesTab = LinesTab;'''

COLORS = [
    ("#1a2438", "#292929"), ("#22304a", "#292929"), ("#0e1628", "#161616"), ("#3b4b6b", "#4a4a4a"),
    ("#15203a", "#1f1f1f"), ("#e6edf7", "#fafafa"), ("#cbd5e1", "#d4d4d4"), ("#2c3b58", "#363636"),
    ("#c9d6e8", "#bdbdbd"), ("#1c2a44", "#202020"), ("#111a2e", "#1a1a1a"), ("#56627a", "#4d4d4d"),
    ("#c4a7ff", "#8b7cff"), ("#60a5fa", "#8b7cff"), ("#4ade80", "#5fd08a"), ("#f87171", "#f06a6a"),
    ("#8b98ad", "#8f8f8f"), ("rgba(96,165,250,", "rgba(139,124,255,"),
]


def fail(msg):
    print("STOPPED - nothing was changed: " + msg)
    sys.exit(1)


def sub_once(text, name, pat, rep, done=None, flags=0, count=1):
    if done and done in text:
        print(f"(ui) {name}: already done")
        return text
    new, n = re.subn(pat, lambda m: rep, text, flags=flags)
    if n != count:
        fail(f"'{name}' matched {n} times (expected {count}). Send this log to the AI helper.")
    print(f"(ui) {name}: updated")
    return new


def lit(text, name, old, new, done=None, count=1):
    return sub_once(text, name, re.escape(old), new, done, 0, count)


def block(text, name, start, end, rep, done):
    pat = re.escape(start) + r"\r?\n.*?(?=" + re.escape(end) + ")"
    return sub_once(text, name, pat, rep, done, re.S)


def common(text):
    for pat, rep in ARROWS:
        text, n = re.subn(pat, rep, text)
        if n:
            print(f"(ui) arrows {rep}: {n} replaced")
    text, n = re.subn("[" + STRIP + "]" + VS + " ?", "", text)
    print(f"(ui) emojis removed: {n}")
    left = [c for c in STRIP if c in text]
    if left:
        fail("some emojis are still there: " + " ".join(left))
    return text


def fix_app(t):
    t = sub_once(t, "home score font", r"^[ \t]*\.text-4xl \{[^\n]*\}[ \t]*$", SCORE_CSS, None, re.M)
    t = block(t, "tabs and navigation", "// ---------- App ----------", "// ---------- Today ----------", APP, '["myteam", "My Team", null]')
    t = block(t, "home screen", "// ---------- Today ----------", "// ---------- Advice ----------", TODAY, "Your lineup · ")
    t = block(t, "matchup tab (all matchups)", "// ---------- Matchup ----------", "// ---------- Power rankings ----------", MATCHUP, "function MatchCard")
    t = block(t, "league standings", "// ---------- League ----------", "// ---------- Add / Drop ----------", LEAGUE, "(this week's matchups moved to the Matchup tab)")
    t = sub_once(t, "clickable names in player rows", r"const PlayerLine = \(\{ s, p, extra \}\) => \(\r?\n.*?\r?\n\);\r?\n", PLAYERLINE, "<PN p={p} /><span className=\"text-xs text-slate-400\">{p.p} · {p.t} · <TL", re.S)
    t = lit(t, "clickable names in news", '<span className="font-medium">{p.n}</span><span className="text-xs text-slate-400">{p.p} · {p.t} · {teamName(s, p.ft)}</span>',
            '<PN p={p} /> <span className="text-xs text-slate-400">{p.p} · {p.t} · <TL s={s} id={p.ft} /></span>', "<PN p={p} /> <span")
    t = lit(t, "clickable names in power rankings", '<div className="whitespace-nowrap">{x.t.name}</div>', '<div className="whitespace-nowrap"><TL s={s} id={x.t.id} /></div>', "<TL s={s} id={x.t.id} /></div>")
    t = lit(t, "clickable names in climb panel", "<b>{x.t.name}</b>", '<TL s={s} id={x.t.id} className="font-semibold" />', 'id={x.t.id} className="font-semibold"')
    t = lit(t, "clickable player names in Players", '<td className="px-3 py-2 font-medium">{p.n}{p.ir', '<td className="px-3 py-2"><PN p={p} />{p.ir', '<td className="px-3 py-2"><PN p={p} />{p.ir')
    t = lit(t, "clickable team names in Players", '<td className="px-3 py-2 text-xs text-slate-500">{teamName(s, p.ft)}</td>', '<td className="px-3 py-2 text-xs text-slate-500"><TL s={s} id={p.ft} /></td>', "<TL s={s} id={p.ft} /></td>")
    t = lit(t, "PP1 filter in Add / Drop (tabs)", '["G", "Goalies"], ["all", "Everyone"]];', '["G", "Goalies"], ["pp1", "On PP1"], ["all", "Everyone"]];', '["pp1", "On PP1"]')
    t = lit(t, "PP1 filter in Add / Drop (logic)", 'const inTab = (f) => pos === "all" || (pos === "sk" ? f.p !== "G" : f.p === pos);',
            'const inTab = (f) => pos === "all" || (pos === "pp1" ? !!sigOf(f).pp1 : pos === "sk" ? f.p !== "G" : f.p === pos);', 'pos === "pp1" ? !!sigOf(f).pp1')
    t = lit(t, "clickable names in Add / Drop", '<td className="px-3 py-2 font-medium">{r.f.n}', '<td className="px-3 py-2"><PN p={r.f} />', "<PN p={r.f} />")
    t = lit(t, "trade analyzer partner", "function TradeAnalyzer({ s }) {", "function TradeAnalyzer({ s, initPartner }) {", "function TradeAnalyzer({ s, initPartner })")
    t = lit(t, "2-for-1 partner", "function TwoForOne({ s }) {", "function TwoForOne({ s, initPartner }) {", "function TwoForOne({ s, initPartner })")
    t = lit(t, "trade partner pre-select", 'const [partner, setPartner] = useState((others[0] || {}).id || "");',
            'const [partner, setPartner] = useState(initPartner || (others[0] || {}).id || "");', "useState(initPartner ||", count=2)
    t = sub_once(t, "data source status icons", r'\{ok \? "' + "\u2705" + VS + r'" : "' + "\u26aa" + VS + r'"\}', SETTINGS_DOT, '"text-slate-400"}>' + DOT)
    t = lit(t, "team pages and My Team", 'ReactDOM.createRoot(document.getElementById("root")).render(<App />);',
            NEWBLOCK + 'ReactDOM.createRoot(document.getElementById("root")).render(<App />);', "function TeamPage(")
    t = common(t)
    for must in ("ReactDOM.createRoot", "const SR = {", "function MyTeam(", "function TeamPage(", "function Matchup(", "function Today("):
        if must not in t:
            fail("fantasy-gm.html looks damaged after the changes (" + must + ").")
    return t


def fix_lines(t):
    total = 0
    for a, b in COLORS:
        total += t.count(a)
        t = t.replace(a, b)
    print(f"(ui) Lines tab colours changed: {total}")
    if total == 0 and "#8b7cff" not in t:
        fail("lines-tab.js doesn't have the colours I expected.")
    t = lit(t, "clickable owners in Lines", '<span className="lt-own">{x.p ? H.teamName(s, x.p.ft) : ""}</span>',
            '<span className="lt-own">{x.p ? (H.TL ? <H.TL s={s} id={x.p.ft} /> : H.teamName(s, x.p.ft)) : ""}</span>', "<H.TL s={s} id={x.p.ft} />")
    t = lit(t, "clickable owner in player card", "{p ? H.teamName(s, p.ft) : \"not in your league's ESPN player list\"}",
            "{p ? (H.TL ? <H.TL s={s} id={p.ft} /> : H.teamName(s, p.ft)) : \"not in your league's ESPN player list\"}", "<H.TL s={s} id={p.ft} />")
    t = sub_once(t, "home card and player pop-up",
                 r"(?:^[ \t]*// ---------- compact summary for the Today screen ----------.*?)?^[ \t]*window\.LinesTab = LinesTab;[ \t]*$",
                 SUMMARY, "window.PlayerPopup = PlayerPopup", re.S | re.M)
    t = common(t)
    if "window.LinesTab = LinesTab" not in t:
        fail("lines-tab.js looks damaged after the changes.")
    return t


def fix_ask(t):
    t = sub_once(t, "news tag filter",
                 r'\(H\.tags\(p, K\) \|\| \[\]\)\.map\(\(x\) => x\.t\)\.filter\(\(t\) => t && !t\.startsWith\("' + "\U0001F4F0" + VS + r'"\)\)',
                 "(H.tags(p, K) || []).filter((x) => x.t && !x.u).map((x) => x.t)", ".filter((x) => x.t && !x.u)")
    t = common(t)
    if "window.AskPanel = AskPanel" not in t:
        fail("ask-panel.js looks damaged after the changes.")
    return t


FIX = {"fantasy-gm.html": fix_app, "lines-tab.js": fix_lines, "ask-panel.js": fix_ask}


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "test"
    if mode == "undo":
        n = 0
        for src, (_, bak) in FILES.items():
            b = pathlib.Path(bak)
            if b.exists():
                pathlib.Path(src).write_text(b.read_text(encoding="utf-8"), encoding="utf-8")
                print(f"(ui) restored {src}")
                n += 1
        if not n:
            fail("no backups found - live mode has never been run.")
        return
    if mode not in ("test", "live"):
        fail("mode must be test, live or undo")
    out = {}
    for src in FILES:
        p = pathlib.Path(src)
        if not p.exists():
            fail(f"{src} is missing from the repo")
        print(f"--- {src}")
        old = p.read_text(encoding="utf-8")
        out[src] = (old, FIX[src](old))
    if mode == "test":
        html = out["fantasy-gm.html"][1]
        html = sub_once(html, "test page loads test Lines tab", r'src="lines-tab\.js\?t=', 'src="lines-tab-test.js?t=')
        html = sub_once(html, "test page loads test Ask panel", r'src="ask-panel\.js\?t=', 'src="ask-panel-test.js?t=')
        out["fantasy-gm.html"] = (out["fantasy-gm.html"][0], html)
        for src, (test, _) in FILES.items():
            pathlib.Path(test).write_text(out[src][1], encoding="utf-8")
        print("(ui) test copies written - open fantasy-gm-test.html to check")
    else:
        for src, (_, bak) in FILES.items():
            b = pathlib.Path(bak)
            if not b.exists():
                b.write_text(out[src][0], encoding="utf-8")
                print(f"(ui) backup saved: {bak}")
            pathlib.Path(src).write_text(out[src][1], encoding="utf-8")
        print("(ui) live files updated")


if __name__ == "__main__":
    main()
