# changes/207-watch-link-la.py - Watch link uses "la" for the Kings instead of "lak" (e.g. live/nhl/2026-11-07/la-vgk)

OLD = r'''const GX_NHL175 = { LA: "lak", NJ: "nj", SJ: "sj", TB: "tb", UTAH: "uta" };'''
NEW = r'''const GX_NHL175 = { LA: "la", NJ: "nj", SJ: "sj", TB: "tb", UTAH: "uta" }; /* change 207 */'''


def change(t):
    t = lit(t, "207: Kings code la", OLD, NEW, "change 207 */")
    return t


edit(APP, change)
