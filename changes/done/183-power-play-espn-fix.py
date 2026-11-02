# changes/183-power-play-espn-fix.py - Power play tags (182) now find ESPN's penalties: ESPN names the play after the infraction ("Tripping") and keeps the length on type.penaltyMinutes / type.penaltyType

OLD1 = r'''    if (!/penalt/i.test(ty) || /penalty shot/i.test(ty + " " + tx)) return;
    let m = +e.penaltyMinutes || +((e.penalty || {}).minutes) || 0;'''
NEW1 = r'''    const T183 = e.type || {}, pt183 = String(T183.penaltyType || ""); /* change 183: ESPN penalty plays */
    if (!(T183.penaltyMinutes != null || pt183 || /penalt/i.test(ty)) || /penalty shot/i.test(ty + " " + tx + " " + pt183)) return;
    let m = +T183.penaltyMinutes || +e.penaltyMinutes || +((e.penalty || {}).minutes) || 0;'''

OLD2 = r'''    if (m >= 10 || (/misconduct/i.test(ty + " " + tx) && m !== 2 && m !== 4 && m !== 5)) return;'''
NEW2 = r'''    if (m >= 10 || /misconduct/i.test(pt183) || (/misconduct/i.test(ty + " " + tx) && m !== 2 && m !== 4 && m !== 5)) return;'''


def change(t):
    t = lit(t, "183: read ESPN penalty plays", OLD1, NEW1, "change 183: ESPN penalty plays")
    t = lit(t, "183: skip misconducts", OLD2, NEW2, "/misconduct/i.test(pt183)")
    return t


edit(APP, change)
