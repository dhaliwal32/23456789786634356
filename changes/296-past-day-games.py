# changes/296-past-day-games.py - Matchup: pick an earlier day and the NHL scores (phone sheet and laptop column) show that day's games, with box scores, scoring, team stats and, for the last 3 days, goal replays and who was on the ice

J_OLD = r'''  }, [open, dragNow144]);
  const J = window.__NHLNOW || {}, games = (J.games || []).slice();'''
J_NEW = r'''  }, [open, dragNow144]);
  /* change 296: an earlier day picked on Matchup shows that day's games (read once from ESPN, kept while the app is open) */
  const past296 = !!day296 && day296 < todayISO(), D296 = (window.__NHLDAY296 = window.__NHLDAY296 || {});
  useEffect(() => {
    if (!past296 || D296[day296]) return undefined;
    let dead = false;
    (window.__GXF132 || window.fetch)(GX_E132 + "scoreboard?dates=" + day296.replace(/-/g, "")).then((r) => (r.ok ? r.json() : null)).then((js) => { if (!js) return; D296[day296] = gxNow132(js); if (!dead) bump((x) => x + 1); }).catch(() => {});
    return () => { dead = true; };
  }, [day296, past296]);
  useEffect(() => { setGid(null); }, [day296]);
  const J = past296 ? D296[day296] || { games: [] } : window.__NHLNOW || {}, games = (J.games || []).slice();'''

SIG_OLD = r'''function GxNhl141({ s, a, b, tA, tB, side, only201 }) {'''
SIG_NEW = r'''function GxNhl141({ s, a, b, tA, tB, side, only201, day296 }) {'''

USE_OLD = r'''      <GxNhl141 s={s} a={a} b={b} tA={tA141} tB={tB141} />
    </div>
    <div className="sd"><GxNhl141 s={s} a={a} b={b} tA={tA141} tB={tB141} side /></div>'''
USE_NEW = r'''      <GxNhl141 s={s} a={a} b={b} tA={dates[d] < today ? A.days[d] : tA141} tB={dates[d] < today ? B.days[d] : tB141} day296={dates[d]} />
    </div>
    <div className="sd"><GxNhl141 s={s} a={a} b={b} tA={dates[d] < today ? A.days[d] : tA141} tB={dates[d] < today ? B.days[d] : tB141} day296={dates[d]} side /></div>'''

DL_OLD = r'''const dl = (() => { try { return new Date().toLocaleDateString([], { weekday: "long", month: "long", day: "numeric" }); } catch (e) { return ""; } })();'''
DL_NEW = r'''const dl = (() => { try { return (past296 ? fromIso(day296) : new Date()).toLocaleDateString([], { weekday: "long", month: "long", day: "numeric" }); } catch (e) { return ""; } })();'''


def change(t):
    t = lit(t, "296: panel takes a day", SIG_OLD, SIG_NEW, "only201, day296 })")
    t = lit(t, "296: that day's games", J_OLD, J_NEW, "change 296: an earlier day picked on Matchup")
    t = lit(t, "296: Matchup passes its day", USE_OLD, USE_NEW, "day296={dates[d]} side />")
    t = lit(t, "296: the date shown", DL_OLD, DL_NEW, "(past296 ? fromIso(day296) : new Date())")
    return t

edit(APP, change)
