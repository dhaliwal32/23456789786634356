# changes/318-fast-goal-alerts.py - goal / assist alerts come from the NHL's own live feed (usually 10 to 30 seconds after the goal, ESPN is often a minute or more), checked every 5 seconds; a game is only read in full when its score changes

NEW_BLOCK = r'''# ---------- change 318: goal / assist alerts from the NHL's own live feed (faster than ESPN) ----------
NHL318 = "https://api-web.nhle.com/v1/"
UA318 = {"User-Agent": "Mozilla/5.0"}
SEED318 = "zz-nhl318"  # in the sent file: goals already on the board when the NHL feed first ran were alerted by the old ESPN path
_tot318, _hot318, _boot318 = {}, {}, {"done": False}


def _norm318(x):
    import unicodedata
    x = unicodedata.normalize("NFKD", str(x or "")).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z ]", "", x).strip()


def _match318(full, names):
    """ESPN player id for an NHL name: the same full name, or the same first letter and last name if only one player fits"""
    n = _norm318(full)
    if not n:
        return None
    hit = [pid for pid, nm in names.items() if _norm318(nm) == n]
    if len(hit) == 1:
        return hit[0]
    last = n.split()[-1]
    hit = [pid for pid, nm in names.items() if _norm318(nm).split()[-1:] == [last] and _norm318(nm)[:1] == n[:1]]
    return hit[0] if len(hit) == 1 else None


def nhl_goals318(opp):
    """one look at the NHL feed: alert each new goal or assist by the opponent's players"""
    ids = _opp_ids302(opp)
    names = {pid: nm for pid, nm in (_opp302.get("names") or {}).items() if pid in ids and nm}
    if not names:
        return
    sc = requests.get(NHL318 + "score/now", headers=UA318, timeout=10).json()
    seed, now = SEED318 not in _sent311(), time.time()
    for g in sc.get("games", []):
        if g.get("gameState") not in ("LIVE", "CRIT", "OFF", "FINAL"):
            continue
        gid = g.get("id")
        tot = ((g.get("awayTeam") or {}).get("score") or 0) + ((g.get("homeTeam") or {}).get("score") or 0)
        if tot != _tot318.get(gid):
            _tot318[gid] = tot
            _hot318[gid] = now + 240  # a new goal: read this game every pass for 4 minutes (assists are often added late)
        if _boot318["done"] and now > _hot318.get(gid, 0):
            continue
        try:
            pbp = requests.get(f"{NHL318}gamecenter/{gid}/play-by-play", headers=UA318, timeout=10).json()
        except Exception as e:
            log("NHL game read failed", gid, e)
            continue
        who = {r.get("playerId"): ((r.get("firstName") or {}).get("default", "") + " " + (r.get("lastName") or {}).get("default", "")).strip()
               for r in pbp.get("rosterSpots") or []}
        for p in pbp.get("plays") or []:
            if p.get("typeDescKey") != "goal" or (p.get("periodDescriptor") or {}).get("periodType") == "SO":
                continue  # shootout goals do not count
            d = p.get("details") or {}
            for f, kind in (("scoringPlayer", "Goal"), ("assist1Player", "Assist"), ("assist2Player", "Assist")):
                nid = d.get(f + "Id")
                pid = _match318(who.get(nid, ""), names) if nid else None
                if pid is None:
                    continue
                key = f"n|{gid}|{p.get('eventId')}|{nid}|{kind}"
                if key in _sent311():
                    continue
                if seed:
                    _mark311(key)
                    continue
                n = d.get(f + "Total")
                msg = f"{kind} by {names[pid]}" + (f" ({n})" if n else "")
                try:
                    import gm_push
                    gm_push.send(msg, "", "#matchup")  # change 315's look: the message, then "from <app>"
                    _mark311(key)
                    log("goal alert:", msg)
                except Exception as e:
                    log("goal alert failed", e)
    if seed:
        _mark311(SEED318)
    _boot318["done"] = True


def fast318(opp, secs):
    """check the NHL feed every 5 seconds for secs seconds"""
    end = time.time() + secs
    while True:
        if opp:
            try:
                nhl_goals318(opp)
            except Exception as e:
                log("NHL goal check failed", e)
        if time.time() >= end:
            return
        time.sleep(5)


if __name__ == "__main__":'''


def go(t):
    t = lit(t, "318: opponent names",
            '''            _opp302.update({"id": opp, "ids": {e.get("playerId") for e in (t.get("roster") or {}).get("entries", [])}, "at": time.time()})''',
            '''            ents = (t.get("roster") or {}).get("entries", [])
            _opp302.update({"id": opp, "ids": {e.get("playerId") for e in ents}, "at": time.time(),  # change 318: names too, to match the NHL feed
                            "names": {e.get("playerId"): (((e.get("playerPoolEntry") or {}).get("player") or {}).get("fullName") or "") for e in ents}})''',
            'change 318: names too')
    t = lit(t, "318: main loop",
            '''        push_onice()  # change 205
        try:
            goal_alerts302(sc[2] if sc else None)  # change 302
        except Exception as e:
            log("goal alerts failed", e)
        time.sleep(EVERY)''',
            '''        push_onice()  # change 205
        fast318(sc[2] if sc else None, 30)  # change 318: NHL feed every 5 seconds (replaces the ESPN goal check, goal_alerts302)''',
            'fast318(sc[2] if sc else None, 30)')
    t = lit(t, "318: new block", 'if __name__ == "__main__":', NEW_BLOCK, "change 318: goal / assist alerts from the NHL")
    py_ok("gm_live.py", t)
    return t


edit("gm_live.py", go)
