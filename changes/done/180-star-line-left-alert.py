# changes/180-star-line-left-alert.py - Phone alert when your player or a free agent is no longer on a superstar's line ("Boldy left Kaprizov's line (MIN)"), the opposite of change 128

HELPER = r'''def star_left180(prev, cur, players, now, new):
    """change 180: your player or a free agent who was on a top-30 forward's line and no longer is"""
    fw = [p for p in players if p.get("p") == "F"]
    stars = {norm(p["n"]): p["n"] for p in sorted(fw, key=lambda p: -(p.get("pavg") or 0))[:30]}
    pl = {}
    for p in players:
        if p.get("p") == "F":
            pl.setdefault(norm(p["n"]), p)
    byk = {(c["team"], c["key"]): c for c in new if c.get("type") in ("line", "lineup")}
    out = []
    for t, pv in (prev or {}).items():
        cv = (cur or {}).get(t) or {}
        if pv == cv or not (complete(pv) and complete(cv)):
            continue
        slot_now = {}
        for s in ES:
            if s.startswith("F"):
                for n in cv.get(s) or []:
                    slot_now[norm(n)] = s
        for s in ES:
            if not s.startswith("F"):
                continue
            names = pv.get(s) or []
            had = [x for x in names if norm(x) in stars]
            for n in names:
                k = norm(n)
                if k in stars:
                    continue
                p = pl.get(k)
                if not p or not ((p.get("ft") or 0) == MY_TEAM_ID or not p.get("ft")):
                    continue
                sk = slot_now.get(k)
                gone = [x for x in had if sk is None or slot_now.get(norm(x)) != sk]
                if not gone:
                    continue
                star = stars[norm(gone[0])]
                c = byk.get((t, k))
                if c:
                    if c.get("who") != "star":
                        c["who"], c["star"] = "starleft", star
                    continue
                c = chg(now, "line", t, n, f"{n} ({t}) is no longer on {star}'s line", "", s, s, "F")
                c["who"], c["star"], c["e"] = "starleft", star, str(p["id"])
                out.append(c)
    return out


def alert_for(c):
'''

ALERT_OLD = r'''        return "Fantasy GM", f"{last} joined {str(c['star']).split()[-1]}'s line ({c['team']})"
'''
ALERT_NEW = r'''        return "Fantasy GM", f"{last} joined {str(c['star']).split()[-1]}'s line ({c['team']})"
    if c.get("who") == "starleft" and c.get("star"):  # change 180
        return "Fantasy GM", f"{last} left {str(c['star']).split()[-1]}'s line ({c['team']})"
'''

PREV_OLD = r'''    new = []
    if due:'''
PREV_NEW = r'''    prev180 = copy.deepcopy(state.get("lines") or {})  # change 180: lines before this read
    new = []
    if due:'''

CALL_OLD = r'''        print(f"(lines) WARNING star line check failed:\n{traceback.format_exc()}")
'''
CALL_NEW = r'''        print(f"(lines) WARNING star line check failed:\n{traceback.format_exc()}")
    # change 180: your player or a free agent leaving a superstar's line
    try:
        new += star_left180(prev180, state.get("lines") or {}, players, now, new)
    except Exception:
        print(f"(lines) WARNING star line left check failed:\n{traceback.format_exc()}")
'''

TEST_OLD = r'''    print("INFO  " + txt[:300])'''
TEST_NEW = r'''    # change 180 checks
    pls = [{"id": "e1", "n": "Aa One", "p": "F", "pavg": 9, "ft": 7}, {"id": "e2", "n": "Bb One", "p": "F", "pavg": 2, "ft": MY_TEAM_ID},
           {"id": "e3", "n": "Cc One", "p": "F", "pavg": 2, "ft": 0}, {"id": "e4", "n": "Dd Two", "p": "F", "pavg": 2, "ft": 5}]
    pls += [{"id": "x%d" % i, "n": "Star Number%d" % i, "p": "F", "pavg": 8, "ft": 6} for i in range(29)]
    b180 = copy.deepcopy(base)
    c180 = copy.deepcopy(base)
    c180["F1"] = ["Aa One", "Dd Two", "Ee Two"]
    c180["F2"] = ["Bb One", "Cc One", "Ff Two"]
    left = star_left180({"TOR": b180}, {"TOR": c180}, pls, now, [])
    check("your player off a star's line is found", any(c["name"] == "Bb One" and c["who"] == "starleft" and c["star"] == "Aa One" for c in left))
    check("free agent off a star's line is found", any(c["name"] == "Cc One" for c in left))
    check("other team's player is not", not any(c["name"] == "Dd Two" for c in left))
    check("left alert text", alert_for(left[0]) == ("Fantasy GM", left[0]["name"].split()[-1] + " left One's line (TOR)"))
    check("no change, no alert", not star_left180({"TOR": b180}, {"TOR": copy.deepcopy(b180)}, pls, now, []))
    print("INFO  " + txt[:300])'''


def change(t):
    t = lit(t, "180: helper", "def alert_for(c):\n", HELPER, "def star_left180(")
    t = lit(t, "180: alert text", ALERT_OLD, ALERT_NEW, "change 180\n")
    t = lit(t, "180: keep lines before the read", PREV_OLD, PREV_NEW, "prev180 = copy.deepcopy")
    t = lit(t, "180: run the check", CALL_OLD, CALL_NEW, "new += star_left180(")
    t = lit(t, "180: self test", TEST_OLD, TEST_NEW, "# change 180 checks")
    return t


edit("gm_lines.py", change)
