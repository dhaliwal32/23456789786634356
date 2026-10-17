# changes/081-trade-3-day-delay.py - Trades take 3 days to go through: both teams keep their players until then, so the trade numbers (points, this week, next week) only count days after that

HELPERS = r'''// ---------- change 081: trades take 3 days to go through (install.py) ----------
const GX_TRADE_DAYS = 3;
const gxTradeDay = () => addDays(todayISO(), GX_TRADE_DAYS);
// a roster that keeps its old players until the trade day and has the new ones from that day on
const gxTimed = (before, after, day) => {
  const was = new Set(before.map((p) => p.id)), now = new Set(after.map((p) => p.id));
  return before.filter((p) => !now.has(p.id)).map((p) => ({ ...p, untilD: day }))
    .concat(after.map((p) => (was.has(p.id) ? p : { ...p, fromD: day })));
};
'''


def change(t):
    t = lit(t, "081: helpers", ROOT, HELPERS + ROOT, "change 081: trades take 3 days")
    t = lit(t, "081: rest of season counts from the trade day",
            "const my = horizonTotal(live59(after), s, nR) - horizonTotal(live59(mine), s, nR), th = horizonTotal(live59(thAfter), s, nR) - horizonTotal(live59(theirs), s, nR);",
            "const tD81 = gxTradeDay(), myT = gxTimed(mine, after, tD81), thT = gxTimed(theirs, thAfter, tD81); // change 081\n"
            "    const my = horizonTotal(live59(myT), s, nR) - horizonTotal(live59(mine), s, nR), th = horizonTotal(live59(thT), s, nR) - horizonTotal(live59(theirs), s, nR);",
            "myT = gxTimed(mine, after, tD81)")
    t = lit(t, "081: next week uses the timed roster",
            "wa = hasOpp ? winChance(sN, after) : null;",
            "wa = hasOpp ? winChance(sN, myT) : null; /* change 081 */",
            "winChance(sN, myT) : null; /* change 081 */")
    t = lit(t, "081: this week uses the timed roster",
            "ta = on77 ? winChance(s, after) : null;",
            "ta = on77 ? winChance(s, myT) : null; /* change 081 */",
            "winChance(s, myT) : null; /* change 081 */")
    t = lit(t, "081: say when it goes through",
            '" of 22 active." + (irIn.length',
            '" of 22 active. Trades take " + GX_TRADE_DAYS + " days, so it goes through " + dayLabel(gxTradeDay()) + "; until then both teams keep their players, and the numbers above count that." + (irIn.length',
            "Trades take \" + GX_TRADE_DAYS")
    return t


edit(APP, change)
