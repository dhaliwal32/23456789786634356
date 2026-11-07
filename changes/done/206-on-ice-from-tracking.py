# changes/206-on-ice-from-tracking.py - On ice shows a minute or two after a goal: the 30-second live job also reads the goal's tracking file, not only NHL's shift charts (which NHL posts only after each period); shift charts replace it once posted

TRACK_FN = r'''

def from_track(url, ro):
    """change 206: players on the ice at the goal moment of the goal's NHL tracking file (posted a few minutes after the goal)"""
    try:
        import gm_edge
        r = requests.get(url, headers=NHL, timeout=20)
        fr = r.json() if r.status_code == 200 else None
        if not isinstance(fr, list) or not fr:
            return None
        P = gm_edge.pack(fr)
        row = P[gm_edge.goal_frame(P)][1]
        on = []
        for o in row:
            if not o[0]:
                continue
            r0 = ro.get(str(o[0])) or []
            on.append([o[0], r0[3] if len(r0) > 3 and r0[3] else o[1], r0[2] if len(r0) > 2 and r0[2] is not None else o[2],
                       r0[0] if r0 else "", r0[1] if len(r0) > 1 else ""])
        teams = {}
        for o in on:
            teams[o[1]] = teams.get(o[1], 0) + 1
        if len(teams) != 2 or min(teams.values()) < 3 or len(on) > 14:
            return None
        return on
    except Exception as ex:
        print(f"(onice) tracking failed: {ex}")
        return None


def update('''

USE_OLD = '''            on = on_ice(shifts, ent["per"], ent["t"], ro)
            if on:
                ent["on"], ent["ok"], ent["at"] = on, True, time.time()
'''
USE_NEW = '''            on, src206 = on_ice(shifts, ent["per"], ent["t"], ro), "s"
            if not on and rp206.get(key) and not (G.get(key) or {}).get("on"):  # change 206: NHL posts shifts only after each period
                on, src206 = from_track(rp206[key], ro), "t"
            if on:
                ent["on"], ent["ok"], ent["at"], ent["src"] = on, True, time.time(), src206
'''


def change(t):
    t = lit(t, "206: tracking reader", "\n\ndef update(", TRACK_FN, "change 206: players on the ice at the goal moment")
    t = lit(t, "206: list of tracking links", "        todo = []\n", "        todo, rp206 = [], {}\n", "todo, rp206 = [], {}")
    t = lit(t, "206: remember the tracking link",
            '"home": home, "scorer": d.get("scoringPlayerId")}))',
            '"home": home, "scorer": d.get("scoringPlayerId")}))\n            rp206[key] = p.get("pptReplayUrl")',
            'rp206[key] = p.get("pptReplayUrl")')
    t = lit(t, "206: keep going without shift charts",
            '            print(f"(onice) shift chart {gid} failed: {ex}")\n            continue\n',
            '            print(f"(onice) shift chart {gid} failed: {ex}")\n            shifts = []\n',
            'failed: {ex}")\n            shifts = []\n')
    t = lit(t, "206: shift charts replace the tracking list later",
            '            if (G.get(key) or {}).get("on"):\n',
            '            if (G.get(key) or {}).get("on") and (G.get(key) or {}).get("src") != "t":\n',
            '(G.get(key) or {}).get("src") != "t":')
    t = lit(t, "206: games with tracking-only goals keep being checked",
            'if v.get("g") == gid and v.get("on")) >= n_goals:',
            'if v.get("g") == gid and v.get("on") and v.get("src") != "t") >= n_goals:',
            'v.get("on") and v.get("src") != "t") >= n_goals:')
    t = lit(t, "206: use tracking when shifts are not there yet", USE_OLD, USE_NEW, "src206 = from_track(rp206[key], ro)")
    return t


edit("gm_onice.py", change)
