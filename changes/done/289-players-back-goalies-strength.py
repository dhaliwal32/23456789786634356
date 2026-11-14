# changes/289-players-back-goalies-strength.py - Players is the Free agents page again (no row of pages on top): Filters has a Show choice (Free agents, All players, Injured) and a strip of every week sits above the list; Goalies tonight is a tidy card at the top of Matchup; the Roster page shows where your team ranks in strength, tap it for every team; the League row at the bottom of Matchup is gone

NEW_CSS = r'''  /* change 289 (install.py) */
  .gx-ws289 { display: flex; gap: 8px; overflow-x: auto; padding: 2px 0 4px; scrollbar-width: none; -webkit-overflow-scrolling: touch; overscroll-behavior-x: contain; }
  .gx-ws289::-webkit-scrollbar { display: none; }
  .gx-ws289 button { flex: 0 0 auto; min-width: 86px; padding: 7px 12px; border-radius: 12px; border: 1px solid var(--line2); color: var(--mute); text-align: left; transition: background-color .15s, color .15s, border-color .15s; }
  .gx-ws289 button b { display: block; font-size: 13px; font-weight: 600; color: var(--ink2); white-space: nowrap; }
  .gx-ws289 button small { display: block; font-size: 11px; white-space: nowrap; }
  .gx-ws289 button.on { background: var(--seg277); border-color: var(--seg277); }
  .gx-ws289 button.on b { color: var(--ink); }
  .gx-go289 { border-radius: 16px; background: var(--card); overflow: hidden; }
  .gx-go289 > .hd { display: flex; align-items: center; gap: 10px; width: 100%; min-height: 52px; padding: 8px 16px; color: var(--ink); text-align: left; }
  .gx-go289 > .hd > span:first-child { flex: 1; min-width: 0; }
  .gx-go289 > .hd b { display: block; font-weight: 600; font-size: 15px; }
  .gx-go289 > .hd small { display: block; font-size: 12px; color: var(--mute); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .gx-go289 > .bd { padding: 0 16px 12px; animation: gx288-in .26s cubic-bezier(.2,.8,.2,1); }
  .gx-go289 .sc { font-size: 12px; color: var(--mute); letter-spacing: .04em; padding: 10px 0 2px; border-top: 1px solid var(--line); margin-top: 4px; }
  .gx-go289 .sc:first-child { border-top: 0; margin-top: 0; }
  .gx-go289 .rw { display: grid; grid-template-columns: auto minmax(0,1fr) auto 40px; align-items: center; gap: 10px; width: 100%; height: 48px; color: var(--ink); text-align: left; font-variant-numeric: tabular-nums; }
  .gx-go289 .rw .nn { min-width: 0; }
  .gx-go289 .rw .nn b { display: block; font-size: 14px; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .gx-go289 .rw .nn small { display: block; font-size: 11.5px; color: var(--mute); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .gx-go289 .rw .st { font-size: 12.5px; color: var(--mute); white-space: nowrap; }
  .gx-go289 .rw .st.ok { color: var(--good); }
  .gx-go289 .rw .st.mb { color: var(--warn); }
  .gx-go289 .rw .xp { text-align: right; font-weight: 600; font-size: 14px; }
  .gx-go289 .em { font-size: 13px; color: var(--mute); height: 40px; display: flex; align-items: center; }
  .gx-go289 .al { width: 100%; height: 40px; margin-top: 8px; border: 1px solid var(--line2); border-radius: 10px; font-size: 13.5px; color: var(--ink); }
  .gx-sr289 { display: flex; align-items: center; gap: 12px; width: 100%; min-height: 60px; padding: 10px 16px; border-radius: 16px; background: var(--card); color: var(--ink); text-align: left; }
  .gx-sr289 .rk { font-size: 24px; font-weight: 600; letter-spacing: -.02em; line-height: 1; white-space: nowrap; }
  .gx-sr289 .rk small { font-size: 12px; font-weight: 400; color: var(--mute); margin-left: 4px; letter-spacing: 0; }
  .gx-sr289 .tx { flex: 1; min-width: 0; }
  .gx-sr289 .tx b { display: block; font-size: 14px; font-weight: 600; }
  .gx-sr289 .tx small { display: block; font-size: 12px; color: var(--mute); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .gx-sx289 { z-index: 70; display: flex; align-items: center; justify-content: center; background: rgba(0,0,0,.6); animation: gx101-fade .2s ease-out; transition: opacity .18s ease-in; }
  .gx-sx289.out { opacity: 0; }
  .gx-sx289 .pn { width: min(560px, calc(100% - 24px)); max-height: calc(100% - 48px); overflow-y: auto; overscroll-behavior: contain; background: var(--card); border: 1px solid var(--line2); border-radius: 18px; padding: 16px; animation: gx101-pop .26s cubic-bezier(.2,.8,.2,1); transition: transform .18s ease-in; }
  .gx-sx289.out .pn { transform: translateY(24px); }
  .gx-sx289 .tt { display: flex; align-items: baseline; justify-content: space-between; gap: 10px; margin-bottom: 4px; }
  .gx-sx289 .tt b { font-size: 17px; font-weight: 600; }
  .gx-sx289 .tt button { font-size: 22px; line-height: 1; color: var(--mute); padding: 4px 8px; }
  .gx-sx289 .nt { font-size: 12px; color: var(--mute); margin-bottom: 8px; }
  .gx-sx289 .r { display: grid; grid-template-columns: 26px minmax(0,1fr) 56px 34px 34px 34px; align-items: center; gap: 6px; height: 44px; border-top: 1px solid var(--line); font-size: 14px; font-variant-numeric: tabular-nums; }
  .gx-sx289 .r > :nth-child(n+3) { text-align: right; }
  .gx-sx289 .r > :nth-child(2) { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .gx-sx289 .r.h { height: 30px; border-top: 0; font-size: 11.5px; color: var(--mute); }
  .gx-sx289 .r.me { font-weight: 600; background: var(--accentSoft); margin: 0 -8px; padding: 0 8px; border-radius: 10px; border-top-color: transparent; }
  .gx-sx289 .r .lo { color: var(--mute); }
  .gx-sx289 .al { width: 100%; height: 40px; margin-top: 12px; border: 1px solid var(--line2); border-radius: 10px; font-size: 13.5px; color: var(--ink); }
  @media (max-width: 640px) {
    .gx-go289, .gx-sr289 { border-radius: 14px; }
    .gx-go289 > .hd { padding: 8px 14px; } .gx-go289 > .bd { padding: 0 14px 12px; }
    .gx-sx289 { align-items: flex-end; }
    .gx-sx289 .pn { width: 100%; max-height: calc(100% - 52px); border-radius: 18px 18px 0 0; border: 0; padding: 16px 14px calc(18px + env(safe-area-inset-bottom)); animation: gx101-up .3s cubic-bezier(.2,.8,.2,1); }
    .gx-sx289.out .pn { transform: translateY(60vh); }
  }
</style>'''

HELPERS = r'''// ---------- change 289: Players page back with a Show filter, week strip, Goalies tonight, strength rank (install.py) ----------
const GX_SHOW289 = [["fa", "Free agents"], ["all", "All players"], ["inj", "Injured"]];
function GxPlayers289(P) {
  const { sub } = P;
  const [v, setV] = useState(() => { const u = uiGet().pl289; return sub === "allp" ? "all" : sub === "injuries" ? "inj" : GX_SHOW289.some((x) => x[0] === u) ? u : "fa"; });
  const pick = (k) => { setV(k); uiSet("pl289", k); };
  if (v === "fa") return <Pickups {...P} show289={v} onShow289={pick} />;
  return (
    <div className="space-y-3" data-gx="289">
      <GxFlt108 label={v === "all" ? "All players" : "Injured"}><div className="flex flex-wrap gap-2 items-center"><Pills items={GX_SHOW289} value={v} onChange={pick} /></div></GxFlt108>
      <GxRankings s={P.s} st287={v} />
    </div>
  );
}
// every week left, one tap each, above the free agent list
function GxWkStrip289({ s, sP, plan, mode, wks, onPick }) {
  const list = [];
  for (let i = sP.wk; i < sP.weeks.length; i++) { const w = sP.weeks[i] || {}, opp = oppOf(w, sP.me), L = String(w.label || "Week " + (i + 1)).split(" \u00b7 "); list.push({ i, wl: L[0], opp }); }
  const sel = new Set(mode === "h1" ? [sP.wk] : mode === "h4" ? list.slice(0, 4).map((x) => x.i) : mode === "h0" ? list.map((x) => x.i) : wks || []);
  if (list.length < 2) return null;
  return (
    <div className="gx-ws289" data-gx="289w">
      {list.map((x, j) => (
        <button key={x.i} type="button" className={sel.has(x.i) ? "on" : ""} aria-pressed={sel.has(x.i)} onClick={() => (x.i === sP.wk ? onPick("h1", null) : onPick("pick", [x.i]))}>
          <b>{j === 0 ? (plan ? "Next week" : "This week") : x.wl}</b>
          <small>{x.opp ? "v " + (gxTag131(s, { ft: x.opp }) || teamName(s, x.opp)) : "no matchup"}</small>
        </button>
      ))}
    </div>
  );
}
function gxGoals289(s, wk, today) {
  const E = window.ESPN_DATA || {}, K = s.blend, D = ((E.goalies || s.goalies || {})[today]) || {};
  const G = s.players.filter((p) => p.p === "G"), byN = {};
  G.forEach((p) => (byN[nrm(p.n)] = p));
  const word = (st) => { const x = String(st || "").toLowerCase(); return x.includes("confirm") && !x.includes("un") ? ["Confirmed", "ok"] : /likely|expected|project/.test(x) ? ["Likely", "mb"] : ["Not confirmed", ""]; };
  const starts = Object.keys(D).filter((n) => D[n]).map((n) => ({ n, t: D[n].team, w: word(D[n].status), p: byN[nrm(n)] || null }));
  const plays = (t) => !!gameOf(t, today) || starts.some((x) => x.t === t);
  const game = (t) => { const g = gameOf(t, today); return g ? (g.h ? "v " : "@ ") + g.o + " \u00b7 " + gameTime(g) : ""; };
  const row = (p) => {
    const me = starts.find((x) => x.p && x.p.id === p.id), other = me ? null : starts.find((x) => x.t === p.t);
    const w = me ? me.w : other ? ["Backup", ""] : [String(gStart(p, today).l || "Not known").replace(/^[^A-Za-z]+/, "").replace(/^./, (c) => c.toUpperCase()), ""];
    return { p, w, sub: p.t + (game(p.t) ? " " + game(p.t) : ""), x: effAvg(p, K, today), sits: !me && !!other };
  };
  const team = (id) => G.filter((p) => p.ft === id && !p.ir && plays(p.t)).map(row).sort((a, b) => (a.sits ? 1 : 0) - (b.sits ? 1 : 0) || b.x - a.x);
  const opp = oppOf(wk, s.me) || s.opp;
  const free = starts.filter((x) => x.p && x.p.ft === "fa").map((x) => row(x.p)).sort((a, b) => b.x - a.x).slice(0, 5);
  return { mine: team(s.me), opp, theirs: opp ? team(opp) : [], free, known: starts.length };
}
function GxGoal289(P) {
  const { s, wk, go } = P, today = todayISO(), gen = (window.ESPN_DATA || {}).generated;
  const [open, setOpen] = useState(() => uiGet().go289 === "o");
  const flip = () => { const v = !open; setOpen(v); uiSet("go289", v ? "o" : "c"); };
  const d = useMemo(() => { try { return gxGoals289(s, wk, today); } catch (e) { return null; } }, [s.players, wk, today, gen]);
  if (!d) return null;
  const sum = d.mine.length ? d.mine.map((r) => lastN(r.p.n) + " " + r.w[0].toLowerCase()).join(" \u00b7 ") : "None of your goalies play today";
  const rows = (list, none) => (list.length ? list.map((r) => (
    <button key={r.p.id} type="button" className="rw" onClick={() => { if (window.__NAV) window.__NAV.player(r.p); }}>
      <GxFace p={r.p} size={22} />
      <span className="nn"><b>{r.p.n}</b><small>{r.sub}</small></span>
      <span className={"st " + r.w[1]}>{r.w[0]}</span>
      <span className="xp">{r.sits ? "\u2013" : f1(r.x)}</span>
    </button>
  )) : <div className="em">{none}</div>);
  return (
    <div className="gx-go289" data-gx="289g">
      <button type="button" className="hd" aria-expanded={open} onClick={flip}>
        <span><b>Goalies tonight</b><small>{sum}</small></span>
        <span className={"sec-chev" + (open ? "" : " shut")} style={{ margin: "0 4px 0 0" }}></span>
      </button>
      {open ? (
        <div className="bd">
          <div className="sc">Yours</div>{rows(d.mine, "None play today.")}
          {d.opp ? <><div className="sc">{teamName(s, d.opp)}</div>{rows(d.theirs, "None play today.")}</> : null}
          <div className="sc">Free agents starting</div>{rows(d.free, d.known ? "No free agent is starting tonight." : "Starters are not posted yet.")}
          <button type="button" className="al" onClick={() => go("moves", "goalies")}>Every goalie, any day</button>
        </div>
      ) : null}
    </div>
  );
}
// where my team ranks in strength; tap for every team
function GxStr289({ s }) {
  const [open, setOpen] = useState(false);
  const [out, setOut] = useState(false);
  const close = () => { if (out) return; setOut(true); setTimeout(() => { setOut(false); setOpen(false); }, 180); };
  useEffect(() => { if (!open) return undefined; const k = (e) => { if (e.key === "Escape") close(); }; window.addEventListener("keydown", k); return () => window.removeEventListener("keydown", k); }, [open, out]);
  const T = leagueTable(s), rows = T.rows || [], i = rows.findIndex((x) => x.t.id === s.me), me = i >= 0 ? rows[i] : null, g = (T.grpRank || {})[s.me] || {};
  if (!me) return null;
  const gap = i > 0 ? f1(rows[i - 1].strength - me.strength) + " behind " + teamName(s, rows[i - 1].t.id) : rows[1] ? f1(me.strength - rows[1].strength) + " ahead of " + teamName(s, rows[1].t.id) : "";
  return (
    <>
      <button type="button" className="gx-sr289" data-gx="289s" onClick={() => setOpen(true)}>
        <span className="rk">{ordN(i + 1)}<small>{"of " + rows.length}</small></span>
        <span className="tx"><b>{"Strength " + f1(me.strength) + " a week"}</b><small>{"Forwards " + (g.F ? ordN(g.F) : "\u2013") + " \u00b7 Defence " + (g.D ? ordN(g.D) : "\u2013") + " \u00b7 Goalies " + (g.G ? ordN(g.G) : "\u2013")}</small></span>
        <span className="sec-chev shut" style={{ margin: "0 4px 0 0" }}></span>
      </button>
      {open ? ReactDOM.createPortal(
        <div className={"gx-sx289 fixed inset-0" + (out ? " out" : "")} onClick={close}>
          <div className="pn" onClick={(e) => e.stopPropagation()}>
            <div className="tt"><b>League strength</b><button type="button" aria-label="Close" onClick={close}>{"\u00d7"}</button></div>
            <div className="nt">{"Projected points a week from here on" + (gap ? ". You are " + gap + "." : ".")}</div>
            <div className="r h"><span>#</span><span>Team</span><span>A week</span><span>F</span><span>D</span><span>G</span></div>
            {rows.map((x, j) => { const r = (T.grpRank || {})[x.t.id] || {}; return (
              <div key={x.t.id} className={"r" + (x.t.id === s.me ? " me" : "")}>
                <span className="lo">{j + 1}</span><span>{x.t.name}</span><span>{f1(x.strength)}</span><span className="lo">{r.F || "\u2013"}</span><span className="lo">{r.D || "\u2013"}</span><span className="lo">{r.G || "\u2013"}</span>
              </div>
            ); })}
            <button type="button" className="al" onClick={() => { close(); window.location.hash = gxHash("league", "power"); }}>Standings and playoff odds</button>
          </div>
        </div>, document.body) : null}
    </>
  );
}
'''

ROUTE_OLD = r'''<GxPlayers287 {...P} sub={sub} />'''
ROUTE_NEW = r'''<GxPlayers289 {...P} sub={sub} />'''

SIG_OLD = r'''function Pickups({ s, setS, wk }) {'''
SIG_NEW = r'''function Pickups({ s, setS, wk, show289, onShow289 }) {'''

LBL_OLD = r'''<GxFlt108 label={({ all: "All", F: "Forwards", D: "Defence", G: "Goalies" })[pos] + '''
LBL_NEW = r'''<GxFlt108 label={(onShow289 ? "Free agents \u00b7 " : "") + ({ all: "All", F: "Forwards", D: "Defence", G: "Goalies" })[pos] + '''

IN_OLD = r'''gxRngLbl108()}><div className="flex flex-wrap gap-2 items-center">'''
IN_NEW = r'''gxRngLbl108()}>{onShow289 ? <div className="flex flex-wrap gap-2 items-center" style={{ marginBottom: 10 }}><Pills items={GX_SHOW289} value={show289} onChange={onShow289} /></div> : null}<div className="flex flex-wrap gap-2 items-center">'''

WK_OLD = r'''<GxRngSel100 /></GxFlt108>'''
WK_NEW = r'''<GxRngSel100 /></GxFlt108>
      <GxWkStrip289 s={s} sP={sP} plan={plan} mode={wm193} wks={wks193} onPick={(m, a) => { setWm193(m); setLimit(40); if (m === "h1" || m === "h4" || m === "h0") { setWks193(null); setH(m === "h1" ? 1 : m === "h4" ? 4 : 0); } else setWks193(a); }} />'''

MU_OLD = r'''<Matchup {...P} /><GxGoalCard288 {...P} /><GxLgLink285 go={P.go} />'''
MU_NEW = r'''<GxGoal289 {...P} /><Matchup {...P} />'''

STR_START = r'''      <div className="text-sm" style={{ display: "flex", flexWrap: "wrap", gap: "6px 18px" }}>
        <span><span className="text-slate-500">Strength</span> {meRow ? f1(meRow.strength) : "\u2013"} a week</span>'''
STR_END = r'''        <span><span className="text-slate-500">Goalies</span> <span style={rkc(g.G)}>{g.G ? ordN(g.G) : "\u2013"}</span></span>
      </div>'''
STR_NEW = r'''      <GxStr289 s={s} />{/* change 289 */}'''


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
    t = lit(t, "289: styles", "</style>", NEW_CSS, "change 289 (install.py)")
    t = lit(t, "289: helpers", ROOT, HELPERS + ROOT, "change 289: Players page back")
    t = lit(t, "289: route", ROUTE_OLD, ROUTE_NEW, "<GxPlayers289 {...P}")
    t = lit(t, "289: pickups take show", SIG_OLD, SIG_NEW, "show289, onShow289 })")
    t = lit(t, "289: filter label", LBL_OLD, LBL_NEW, '(onShow289 ? "Free agents')
    t = lit(t, "289: show inside filters", IN_OLD, IN_NEW, "<Pills items={GX_SHOW289} value={show289}")
    t = lit(t, "289: week strip", WK_OLD, WK_NEW, "<GxWkStrip289 s={s}")
    t = lit(t, "289: goalies on top of Matchup", MU_OLD, MU_NEW, "<GxGoal289 {...P} /><Matchup")
    t = cut(t, "289: strength rank", STR_START, STR_END, STR_NEW, "<GxStr289 s={s} />")
    return t

edit(APP, change)
