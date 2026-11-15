# changes/297-trade-targets.py - Trades: the ideas box becomes "Players to trade for": up to 10 players on other teams, best for you first, each with the one-for-one offer that also helps the other team; tap one to load the trade

NEW_CSS = r'''  /* change 297 (install.py) */
  .gx-ti293 .tg297 { min-width: 0; display: grid; grid-template-columns: auto minmax(0,1fr); align-items: center; gap: 10px; }
  .gx-ti293 .tg297 b { display: block; font-size: 14.5px; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .gx-ti293 .tg297 small { display: block; font-size: 12px; color: var(--mute); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .gx-ti293 .rw { height: 58px; }
</style>'''

TOP_OLD = r'''  const top = cand.slice(0, 36), tD = gxTradeDay(),'''
TOP_NEW = r'''  const top = (() => { const n = {}; return cand.filter((o) => (n[o.y.id] = (n[o.y.id] || 0) + 1) <= 3).slice(0, 90); })(), tD = gxTradeDay(), /* change 297: 3 offers per player at most */'''

DD_OLD = r'''    good.forEach((o) => { if (out.length >= 5 || ux[o.x.id] || uy[o.y.id]) return; ux[o.x.id] = uy[o.y.id] = 1; out.push(o); });
    done(out);'''
DD_NEW = r'''    good.forEach((o) => { if (out.length >= 10 || uy[o.y.id]) return; uy[o.y.id] = 1; out.push(o); }); /* change 297: one row per player to trade for */
    done(out);'''

HD_OLD = r'''<div className="hd"><span className="gx-tag">Trade ideas</span><small>swaps that help both teams</small></div>'''
HD_NEW = r'''<div className="hd"><span className="gx-tag">Players to trade for</span><small>with an offer that helps them too</small></div>'''

RW_OLD = r'''          <span className="sw"><small>Give</small><GxFace p={o.x} size={14} /><b>{o.x.n}</b><small>Get</small><GxFace p={o.y} size={14} /><b>{o.y.n + " \u00b7 " + (gxTag131(s, o.y) || teamName(s, o.tm))}</b></span>'''
RW_NEW = r'''          <span className="tg297"><GxFace p={o.y} size={22} /><span><b>{o.y.n}</b><small>{o.y.t + " \u00b7 " + o.y.p + " \u00b7 " + (gxTag131(s, o.y) || teamName(s, o.tm)) + " \u00b7 offer " + lastN(o.x.n)}</small></span></span>'''

EM_OLD = r'''<div className="em">No one-for-one swap helps both teams right now.</div>'''
EM_NEW = r'''<div className="em">Nobody on another team can be had right now in a one-for-one that helps both sides.</div>'''

GD_OLD = r'''        if (my >= 2 && th >= 2) good.push({ x: o.x, y: o.y, tm: o.tm, my, th });'''
GD_NEW = r'''        if (my >= 2 && th >= 0) good.push({ x: o.x, y: o.y, tm: o.tm, my, th }); /* change 297: they must not lose, you must gain */'''

QK_OLD = r'''if (da > -0.3 && db > -0.3) cand.push({ x, y, tm: tm.id, q: Math.min(da, db) + (da + db) / 4 });'''
QK_NEW = r'''if (da > 0.1 && db > -1.5) cand.push({ x, y, tm: tm.id, q: da + Math.min(0, db) }); /* change 297 */'''


def change(t):
    t = lit(t, "297: styles", "</style>", NEW_CSS, "change 297 (install.py)")
    t = lit(t, "297: look at more swaps", TOP_OLD, TOP_NEW)
    t = lit(t, "297: more targets", GD_OLD, GD_NEW, "change 297: they must not lose")
    t = lit(t, "297: wider first look", QK_OLD, QK_NEW, "q: da + Math.min(0, db) }); /* change 297 */")
    t = lit(t, "297: one row per target", DD_OLD, DD_NEW, "change 297: one row per player to trade for")
    t = lit(t, "297: title", HD_OLD, HD_NEW)
    t = lit(t, "297: target first", RW_OLD, RW_NEW, 'className="tg297"')
    t = lit(t, "297: empty note", EM_OLD, EM_NEW)
    return t

edit(APP, change)
