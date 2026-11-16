# changes/303-trade-players.py - trades in League activity find their players: when ESPN does not link the accepted trade to its offer, the offer is found by the team that accepted it (the nearest offer before it that sends players to or from that team)

OLD = '''  if (!Object.keys(sides).length) {
    const A = gxTm299(s, root.tm), B = gxTm299(s, t.tm !== root.tm ? t.tm : null);'''
NEW = '''  if (!Object.keys(sides).length) { /* change 303: find the offer by the team that accepted it */
    const who = String(t.tm), at = t.at || 0;
    const offer = tx.filter((x) => x.ty === "TRADE_PROPOSAL" && (x.it || []).some((i) => String(i[2]) === who || String(i[3]) === who) && (x.pr || x.at || 0) <= at + 6e4)
      .sort((u, v) => (v.pr || v.at || 0) - (u.pr || u.at || 0))[0];
    if (offer) (offer.it || []).forEach((i) => { if (i[1] === "LINEUP" || i[1] === "DROP") return; const to = gxTm299(s, i[3]); const p = gxPl299(s, i[0]); if (!to || !p || (sides[to] || []).some((q) => q.id === p.id)) return; (sides[to] = sides[to] || []).push(p); });
  }
  if (!Object.keys(sides).length) {
    const A = gxTm299(s, root.tm), B = gxTm299(s, t.tm !== root.tm ? t.tm : null);'''


def change(t):
    t = lit(t, "303: find the offer", OLD, NEW, "change 303: find the offer by the team that accepted it")
    return t

edit(APP, change)
