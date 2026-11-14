# changes/288-goalies-on-matchup.py - Goalie starts live on the Matchup page: a Goalie starts card (one line on your goalies today, tap to open the full list for any day) instead of a page under Players

NEW_CSS = r'''  /* change 288 (install.py) */
  .gx-gc288 { border-radius: 16px; background: var(--card); overflow: hidden; }
  .gx-gc288 > .hd288 { display: flex; align-items: center; gap: 10px; width: 100%; min-height: 56px; padding: 10px 16px; color: var(--ink); text-align: left; }
  .gx-gc288 > .hd288 > span:first-child { flex: 1; min-width: 0; }
  .gx-gc288 > .hd288 b { display: block; font-weight: 600; font-size: 15px; }
  .gx-gc288 > .hd288 small { display: block; font-size: 12px; color: var(--mute); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .gx-gc288 > .hd288 .sec-chev { transition: transform .2s ease; }
  .gx-gc288 > .bd288 { padding: 0 12px 14px; animation: gx288-in .26s cubic-bezier(.2,.8,.2,1); }
  @keyframes gx288-in { from { opacity: 0; transform: translateY(-8px); } to { opacity: 1; transform: none; } }
  @media (max-width: 640px) { .gx-gc288 { border-radius: 14px; } .gx-gc288 > .hd288 { padding: 10px 14px; } .gx-gc288 > .bd288 { padding: 0 6px 12px; } }
</style>'''

HELPERS = r'''// ---------- change 288: Goalie starts card on Matchup (install.py) ----------
function GxGoalCard288(P) {
  const { s } = P, today = todayISO();
  const [open, setOpen] = useState(() => uiGet().gc288 === "o");
  const flip = () => { const v = !open; setOpen(v); uiSet("gc288", v ? "o" : "c"); };
  let sum = "";
  try {
    const DF = (((window.ESPN_DATA || {}).goalies) || {})[today] || {};
    const plays = (p) => !!gameOf(p.t, today) || Object.values(DF).some((v) => v && v.team === p.t);
    const mine = s.players.filter((p) => p.ft === s.me && p.p === "G" && !p.ir && plays(p));
    sum = mine.length ? mine.map((p) => lastN(p.n) + ": " + String(gStart(p, today).l || "").replace(/^[^A-Za-z]+/, "")).join(" \u00b7 ") : "None of your goalies play today";
  } catch (e) { sum = ""; }
  return (
    <div className="gx-gc288" data-gx="288">
      <button type="button" className="hd288" aria-expanded={open} onClick={flip}>
        <span><b>Goalie starts</b><small>{sum}</small></span>
        <span className={"sec-chev" + (open ? "" : " shut")} style={{ margin: "0 4px 0 0" }}></span>
      </button>
      {open ? <div className="bd288"><GoalieStreams {...P} /></div> : null}
    </div>
  );
}
'''

MU_OLD = r'''<Matchup {...P} /><GxLgLink285 go={P.go} />'''
MU_NEW = r'''<Matchup {...P} /><GxGoalCard288 {...P} /><GxLgLink285 go={P.go} />'''


def change(t):
    t = lit(t, "288: styles", "</style>", NEW_CSS, "change 288 (install.py)")
    t = lit(t, "288: helpers", ROOT, HELPERS + ROOT, "change 288: Goalie starts card")
    t = lit(t, "288: on Matchup", MU_OLD, MU_NEW, "<GxGoalCard288 {...P} />")
    return t

edit(APP, change)
