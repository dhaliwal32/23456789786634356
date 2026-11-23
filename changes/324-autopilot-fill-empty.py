# changes/324-autopilot-fill-empty.py - lineup autopilot never leaves a starting spot empty (Kuvar, Nov 23: "add all active and then for those empty still fit a player in"): everyone with a game starts first, then any spot still open keeps or gets a player with no game today instead of sitting empty; a lineup with empty spots is fixed even when it adds no points

FILL_OLD = '''    for r in util[:max(0, cap[SLOT_U])]:
        want[r["id"]] = SLOT_U
    for r in left:
        want.setdefault(r["id"], SLOT_BENCH)
'''
FILL_NEW = '''    for r in util[:max(0, cap[SLOT_U])]:
        want[r["id"]] = SLOT_U

    # change 324: players with a game start first (above); any starting spot still open gets a player with no game
    # today instead of staying empty. A player already in that spot stays put, healthy players before injured ones.
    def fill324(slot, ok):
        room = cap[slot] - sum(1 for r in left if want.get(r["id"]) == slot)
        if room <= 0:
            return
        pool = sorted([r for r in left if r["id"] not in want and ok(r)],
                      key=lambda r: (r["slot"] != slot, r["slot"] not in ACTIVE, r["why"] == "out",
                                     -(r.get("pavg") or r.get("avg") or 0)))
        for r in pool[:room]:
            want[r["id"]] = slot
    fill324(SLOT_G, lambda r: r["p"] == "G")
    fill324(SLOT_D, lambda r: r["p"] == "D")
    fill324(SLOT_F, lambda r: r["p"] == "F")
    fill324(SLOT_U, lambda r: r["p"] in ("F", "D") and (not r["elig"] or SLOT_U in r["elig"]))
    for r in left:
        want.setdefault(r["id"], SLOT_BENCH)
'''

GAIN_OLD = '''        if not moves or gain < min_gain:
'''
GAIN_NEW = '''        fills = sum(m["to"] in ACTIVE for m in moves) - sum(m["from"] in ACTIVE for m in moves)  # change 324: empty spots filled
        if not moves or (gain < min_gain and fills <= 0):
'''

DESC_OLD = '''    ins = [m["r"] for m in moves if m["to"] in ACTIVE and m["from"] not in ACTIVE]
'''
DESC_NEW = '''    ins = [m["r"] for m in moves if m["to"] in ACTIVE and m["from"] not in ACTIVE and m["r"].get("v", 0) > 0]
    fill = [m["r"] for m in moves if m["to"] in ACTIVE and m["from"] not in ACTIVE and not m["r"].get("v", 0) > 0]  # change 324
'''
DESC2_OLD = '''    if not parts and moves:
'''
DESC2_NEW = '''    if fill:
        parts.append("fill empty spots with " + names(fill, False) + " (no game)")
    if not parts and moves:
'''


def autopilot(t):
    t = lit(t, "324: fill empty starting spots", FILL_OLD, FILL_NEW, "def fill324(slot, ok):")
    t = lit(t, "324: fix empty spots even with no points gained", GAIN_OLD, GAIN_NEW, "# change 324: empty spots filled")
    t = lit(t, "324: note lists the fill-ins", DESC_OLD, DESC_NEW, "fill = [m[\"r\"] for m in moves")
    t = lit(t, "324: note line for fill-ins", DESC2_OLD, DESC2_NEW, '"fill empty spots with "')
    return t


edit("gm_autopilot.py", autopilot)
