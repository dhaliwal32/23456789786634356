# changes/276-game-plan.py - Roster box: Game plan card (where the matchup stands in one line, then who to start over who when more players have a game than there are spots, lineup fixes for ESPN, goalies not confirmed)

NEW_CSS = r'''  /* change 276 (install.py) */
  .gx-bx226 .gp276 .say { font-size: 14px; line-height: 1.4; color: var(--ink); margin-top: 8px; }
  .gx-bx226 .gp276 .say span { color: var(--mute); }
  .gx-bx226 .gp276 .dd276 { font-size: 12px; color: var(--mute); margin-top: 12px; padding-top: 10px; border-top: 1px solid var(--line); display: flex; justify-content: space-between; gap: 10px; white-space: nowrap; }
  .gx-bx226 .gp276 .rw { display: grid; grid-template-columns: 8px minmax(0,1fr) auto; align-items: center; gap: 10px; height: 44px; width: 100%; background: none; border: 0; padding: 0; color: var(--ink); text-align: left; }
  .gx-bx226 .gp276 .rw + .rw { border-top: 1px solid var(--line); }
  .gx-bx226 .gp276 .rw i { width: 8px; height: 8px; border-radius: 99px; background: var(--line2); }
  .gx-bx226 .gp276 .rw i.do { background: var(--warn); }
  .gx-bx226 .gp276 .rw b { display: block; font-size: 13.5px; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .gx-bx226 .gp276 .rw small { display: block; font-size: 11px; color: var(--mute); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .gx-bx226 .gp276 .rw em { font-style: normal; font-size: 12px; color: var(--mute); font-variant-numeric: tabular-nums; white-space: nowrap; }
  .gx-bx226 .gp276 .ok { font-size: 13px; color: var(--mute); height: 44px; display: flex; align-items: center; }
  .gx-bx226 .gp276 .mr { width: 100%; height: 36px; margin-top: 4px; border: 1px solid var(--line2); border-radius: 10px; background: none; color: var(--ink); font-size: 13px; }
</style>'''

HELPERS = r'''// ---------- change 276: Game plan card in the Roster box (install.py) ----------
// the lineup day to plan: today while a game has not started yet, otherwise the next day with games
function gxPlan276(s, w, today) {
  const K = s.blend, dates = w.dates || [], ti = dates.indexOf(today);
  const ng = liveNudges(K); // same small live adjustments the box uses, so the numbers match the Day side
  const mine = s.players.filter((p) => p.ft === s.me && !p.ir).map((p) => (ng[p.id] ? { ...p, gwMul: (p.gwMul || 1) * ng[p.id] } : p));
  const plays = (p, d) => (w.games[p.t] || []).includes(d);
  let d = -1;
  for (let j = Math.max(0, ti); j < dates.length; j++) {
    if (dates[j] < today) continue;
    if (mine.some((p) => plays(p, j) && (dates[j] !== today || gState(p.t, today).s === "P"))) { d = j; break; }
  }
  if (d < 0) return null;
  const dt = dates[d], isT = dt === today;
  const AD = actDay(s.me, dt), has = !!AD && Object.keys(AD).length > 0;
  const slotOf = (p) => { const v = has ? AD[String(p.id).replace(/^e/, "")] : null; return v ? v[1] : null; };
  const cap = { F: 9, D: 5, U: 1, G: 2 };
  const open = mine.filter((p) => plays(p, d) && (!isT || gState(p.t, dt).s === "P"));
  if (isT) mine.forEach((p) => { const k = CAPK[ESLOT[slotOf(p)]]; if (k && plays(p, d) && gState(p.t, dt).s !== "P") cap[k] = Math.max(0, cap[k] - 1); });
  const L = dayLineup(open, w, d, K, cap);
  const bench = [...L.bench].sort((a, b) => b.x - a.x);
  const used = new Set(), rows = [];
  // every player who sits is paired with the weakest starter he could have replaced
  bench.forEach((b) => {
    const c = L.start.filter((q) => !used.has(q.id) && (b.p === "G" ? q.slot === "G" : q.slot !== "G" && (q.p === b.p || q.slot === "UTIL"))).sort((x, y) => x.x - y.x)[0];
    if (!c) return;
    used.add(c.id);
    const fix = has && isT && ESLOT[slotOf(b)] && !ESLOT[slotOf(c)];
    rows.push({ a: c, b, fix, k: c.id + b.id });
  });
  // starters ESPN still has on the bench with nobody to sit for them
  if (has && isT) L.start.filter((q) => !used.has(q.id) && slotOf(q) === 7).forEach((q) => rows.push({ a: q, b: null, fix: true, k: q.id }));
  rows.sort((x, y) => (y.fix ? 1 : 0) - (x.fix ? 1 : 0));
  const gl = L.start.filter((q) => q.slot === "G" && q.gs && !/confirmed/.test(q.gs.replace("unconfirmed", "")));
  return { d, dt, isT, rows, gl, n: open.length, st: L.start.length, empty: L.empty };
}
function GxPlan276({ s, w, sa, sb, fa, fb, leftA, leftB, up, openP }) {
  const today = todayISO(), gen = (window.ESPN_DATA || {}).generated;
  const [all, setAll] = useState(false);
  const ap = gxUseAp();
  const P = useMemo(() => { try { return gxPlan276(s, w, today); } catch (e) { return null; } }, [s.players, w, today, gen, s.blend, window.__LIVEV120]);
  const lead = sa - sb, m = fa - fb, apOn = gxApMode(ap) === "on";
  const say = up ? "Projected to " + (m >= 0 ? "win" : "lose") + " by " + f1(Math.abs(m)) + "."
    : (Math.abs(lead) < 0.05 ? "Tied" : (lead > 0 ? "You lead by " : "You trail by ") + f1(Math.abs(lead))) + ", on pace to " + (m >= 0 ? "win" : "lose") + " by " + f1(Math.abs(m)) + ".";
  const say2 = leftA + " games left, they have " + leftB + "." + (m < 0 && leftA && !up ? " You need " + f1(Math.max(0, fb - sa) / leftA) + " a game." : "");
  const rows = P ? P.rows : [], show = all ? rows : rows.slice(0, 3), fixN = rows.filter((r) => r.fix).length;
  const dn = P ? (P.isT ? "Today" : dayLabel(P.dt).split(",")[0]) : "";
  return (
    <div className="bp230 gp276" data-gx="276">
      <div className="ft"><span className="gx-tag">Game plan</span></div>
      <div className="say">{say} <span>{say2}</span></div>
      {!P ? null : (
        <>
          <div className="dd276"><span>{dn + " \u00b7 " + P.n + " with a game, " + P.st + " start"}</span><span>{fixN ? (apOn ? "Autopilot will fix " + fixN : fixN + " to change on ESPN") : rows.length ? "who starts over who" : ""}</span></div>
          {!rows.length ? <div className="ok">{P.empty ? "Everyone with a game starts. " + P.empty + " empty spot" + (P.empty === 1 ? "" : "s") + "." : "Everyone with a game starts."}</div> : null}
          {show.map((r) => (
            <button key={r.k} type="button" className="rw" onClick={() => openP(r.b || r.a)}>
              <i className={r.fix ? "do" : ""}></i>
              <span className="min-w-0"><b>{r.b ? "Start " + lastN(r.a.n) + " over " + lastN(r.b.n) : "Start " + lastN(r.a.n)}</b><small>{r.b ? (r.fix ? "ESPN has them the other way round" : lastN(r.b.n) + " sits, lowest " + (r.b.p === "G" ? "goalie" : r.b.p === "D" ? "defenceman" : "forward") + " left over") : "On your bench with an open spot"}</small></span>
              <em>{r.b ? f1(r.a.x) + " v " + f1(r.b.x) : "+" + f1(r.a.x)}</em>
            </button>
          ))}
          {rows.length > 3 ? <button type="button" className="mr" onClick={() => setAll(!all)}>{all ? "Show less" : "Show all " + rows.length}</button> : null}
          {P.gl.map((q) => (
            <button key={"g" + q.id} type="button" className="rw" style={{ borderTop: "1px solid var(--line)" }} onClick={() => openP(q)}>
              <i></i>
              <span className="min-w-0"><b>{lastN(q.n) + " in goal"}</b><small>{q.gs}</small></span>
              <em>{f1(q.x)}</em>
            </button>
          ))}
        </>
      )}
    </div>
  );
}
'''

OLD_SHOW = r'''<div className="min-w-0">{board}{me !== s.me || !cur ? null : <GxBp257 s={s} openP={openP} />}</div>'''
NEW_SHOW = r'''<div className="min-w-0">{board}{me !== s.me || !cur || over ? null : <GxPlan276 s={s} w={w} sa={sa} sb={sb} fa={fa} fb={fb} leftA={leftA} leftB={leftB} up={up} openP={openP} />}{me !== s.me || !cur ? null : <GxBp257 s={s} openP={openP} />}</div>'''


def change(t):
    t = lit(t, "276: styles", "</style>", NEW_CSS, "change 276 (install.py)")
    t = lit(t, "276: helpers", ROOT, HELPERS + ROOT, "change 276: Game plan card")
    t = lit(t, "276: show it", OLD_SHOW, NEW_SHOW, "<GxPlan276 s={s}")
    return t

edit(APP, change)
