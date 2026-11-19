# changes/320-late-assists.py - late assists alert within about 30 seconds: the NHL feed often adds assists minutes after the goal, so every live game is re-read every 30 seconds (and every 5 seconds for 4 minutes after a score change), not only right after a goal

def go(t):
    t = lit(t, "320: re-read live games",
            '''        if _boot318["done"] and now > _hot318.get(gid, 0):
            continue''',
            '''        live320 = g.get("gameState") in ("LIVE", "CRIT")
        if _boot318["done"] and now > _hot318.get(gid, 0) and not (live320 and now - _read320.get(gid, 0) >= 30):
            continue  # change 320: a live game is still re-read every 30 s, so a late assist is never stuck until the next goal
        _read320[gid] = now''',
            'change 320: a live game is still re-read every 30 s')
    t = lit(t, "320: read times",
            '_tot318, _hot318, _boot318 = {}, {}, {"done": False}',
            '_tot318, _hot318, _boot318 = {}, {}, {"done": False}\n_read320 = {}  # change 320: when each game was last read',
            '_read320 = {}  # change 320')
    py_ok("gm_live.py", t)
    return t


edit("gm_live.py", go)
