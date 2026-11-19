# changes/321-race-feeds-timing.py - goal / assist alerts race the NHL feed and ESPN's feed and send from whichever shows the goal first (never twice), check every 2 seconds, and write down the time of every alert in edge/alert-times.json so delays can be measured

ESPN_BLOCK = r'''# ---------- change 321: race ESPN's feed against the NHL feed; write down when every alert went out ----------
SB321 = "https://site.api.espn.com/apis/site/v2/sports/hockey/nhl/"
TIMES321 = os.path.join(HERE, "edge", "alert-times.json")
SEED321 = "zz-espn321"  # in the sent file: goals already on the board when the ESPN racer first ran were alerted before
_etot321, _ehot321, _eread321, _eboot321 = {}, {}, {}, {"done": False}
_dirty321 = [False]


def _secs321(t):
    try:
        m, s = str(t).split(":")[:2]
        return int(m) * 60 + int(s)
    except Exception:
        return None


def _dup321(pid, kind, per, t):
    """the same player, same kind, same period, within 60 seconds of game clock = the same goal"""
    s = _secs321(t)
    if s is None:
        return False
    pre = f"d|{pid}|{kind}|{per}|"
    return any(k.startswith(pre) and abs(int(k[len(pre):]) - s) <= 60 for k in _sent311() if k[len(pre):].isdigit())


def _send321(key, pid, kind, per, t, msg, src, wall=None):
    """send one alert unless either feed already sent it; remember it under both names"""
    if key in _sent311() or _dup321(pid, kind, per, t):
        return
    try:
        import gm_push
        gm_push.send(msg, "", "#matchup")  # change 315's look: the message, then "from <app>"
        log("goal alert:", msg, "(" + src + ")")
    except Exception as e:
        log("goal alert failed", e)
        return
    _mark311(key)
    s = _secs321(t)
    if s is not None:
        _mark311(f"d|{pid}|{kind}|{per}|{s}")
    try:
        try:
            with open(TIMES321) as f:
                L = json.load(f)
        except Exception:
            L = []
        L.append({"sent": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "msg": msg, "from": src,
                  "goal": wall, "period": per, "clock": t})
        with open(TIMES321, "w") as f:
            json.dump(L[-300:], f, indent=0)
        _dirty321[0] = True
    except Exception as e:
        log("could not save alert time", e)


def espn_goals321(opp):
    """one look at ESPN's feed: the same alerts as the NHL check, from whichever feed has the goal first"""
    ids = _opp_ids302(opp)
    names = {pid: nm for pid, nm in (_opp302.get("names") or {}).items() if pid in ids and nm}
    if not names:
        return
    sb = requests.get(SB321 + "scoreboard", headers=UA318, timeout=10).json()
    seed, now = SEED321 not in _sent311(), time.time()
    for ev in sb.get("events", []):
        st = (((ev.get("status") or {}).get("type")) or {}).get("state")
        if st not in ("in", "post"):
            continue
        eid = ev.get("id")
        comp = (ev.get("competitions") or [{}])[0]
        tot = sum(int(c.get("score") or 0) for c in comp.get("competitors") or [])
        if tot != _etot321.get(eid):
            _etot321[eid] = tot
            _ehot321[eid] = now + 240
        if _eboot321["done"] and now > _ehot321.get(eid, 0) and not (st == "in" and now - _eread321.get(eid, 0) >= 30):
            continue
        _eread321[eid] = now
        try:
            sm = requests.get(SB321 + "summary", params={"event": eid}, headers=UA318, timeout=10).json()
        except Exception as e:
            log("ESPN game read failed", eid, e)
            continue
        for p in sm.get("plays") or []:
            per = (p.get("period") or {}).get("number") or 0
            if not p.get("scoringPlay") or per >= 5:
                continue  # shootout goals do not count
            t = (p.get("clock") or {}).get("displayValue")
            text = p.get("text") or ""
            for q in p.get("participants") or []:
                kind = {"scorer": "Goal", "assister": "Assist"}.get(q.get("type"))
                a = q.get("athlete") or {}
                try:
                    pid = int(a.get("id"))
                except Exception:
                    continue
                if not kind or pid not in names:
                    continue
                key = f"e|{eid}|{p.get('id')}|{pid}|{kind}"
                if seed:
                    if key not in _sent311():
                        _mark311(key)
                    continue
                nm = a.get("displayName") or names[pid]
                m = re.search(r"Goal \((\d+)\)", text) if kind == "Goal" else re.search(re.escape(nm) + r" \((\d+)\)", text)
                _send321(key, pid, kind, per, t, f"{kind} by {names[pid]}" + (f" ({m.group(1)})" if m else ""), "ESPN", p.get("wallclock"))
    if seed:
        _mark311(SEED321)
    _eboot321["done"] = True


if __name__ == "__main__":'''


def go(t):
    # NHL alerts go through the shared sender, so the two feeds never both send the same goal
    t = lit(t, "321: NHL alerts through the shared sender",
            '''                n = d.get(f + "Total")
                msg = f"{kind} by {names[pid]}" + (f" ({n})" if n else "")
                try:
                    import gm_push
                    gm_push.send(msg, "", "#matchup")  # change 315's look: the message, then "from <app>"
                    _mark311(key)
                    log("goal alert:", msg)
                except Exception as e:
                    log("goal alert failed", e)''',
            '''                n = d.get(f + "Total")
                msg = f"{kind} by {names[pid]}" + (f" ({n})" if n else "")
                _send321(key, pid, kind, (p.get("periodDescriptor") or {}).get("number") or 0, p.get("timeInPeriod"), msg, "NHL")  # change 321''',
            '"NHL")  # change 321')
    t = lit(t, "321: first NHL pass remembers goals under both names",
            '''                if seed:
                    _mark311(key)
                    continue
                n = d.get(f + "Total")''',
            '''                if seed:
                    _mark311(key)
                    s321 = _secs321(p.get("timeInPeriod"))
                    if s321 is not None:
                        _mark311(f"d|{pid}|{kind}|{(p.get('periodDescriptor') or {}).get('number') or 0}|{s321}")  # change 321
                    continue
                n = d.get(f + "Total")''',
            's321 = _secs321(p.get("timeInPeriod"))')
    t = lit(t, "321: both feeds every 2 seconds",
            '''            try:
                nhl_goals318(opp)
            except Exception as e:
                log("NHL goal check failed", e)
        if time.time() >= end:
            return
        time.sleep(5)''',
            '''            try:
                nhl_goals318(opp)
            except Exception as e:
                log("NHL goal check failed", e)
            try:
                espn_goals321(opp)  # change 321: whichever feed has the goal first sends it
            except Exception as e:
                log("ESPN goal check failed", e)
        if time.time() >= end:
            return
        time.sleep(2)  # change 321: was 5''',
            'time.sleep(2)  # change 321: was 5')
    # keep the sent list in the order things happened (sorting dropped the wrong keys once it was full)
    t = lit(t, "321: sent list in order",
            '''def _mark311(key):
    k = _sent311()
    k.add(key)
    try:
        with open(SENT311, "w") as f:
            json.dump({"keys": sorted(k)[-400:]}, f)''',
            '''_order321 = []  # change 321: sent keys in the order they happened


def _mark311(key):
    k = _sent311()
    if not _order321:
        try:
            with open(SENT311) as f:
                _order321.extend(json.load(f).get("keys", []))
        except Exception:
            pass
    k.add(key)
    if key not in _order321:
        _order321.append(key)
    try:
        with open(SENT311, "w") as f:
            json.dump({"keys": [x for x in _order321[-3000:] if x in k] or sorted(k)[-3000:]}, f)  # change 321: newest 3000 kept''',
            'change 321: newest 3000 kept')
    # the alert times file is saved with the on-ice file, and on its own when only it changed
    t = lit(t, "321: save alert times",
            '''        if not gm_onice.update("edge/onice-live.json", 20, live_only=True):
            return''',
            '''        if not gm_onice.update("edge/onice-live.json", 20, live_only=True) and not _dirty321[0]:
            return
        _dirty321[0] = False''',
            'and not _dirty321[0]:')
    t = lit(t, "321: add alert times file",
            '''        run("add", "edge/onice-sent311.json")  # change 311: goal alerts already sent''',
            '''        run("add", "edge/onice-sent311.json")  # change 311: goal alerts already sent
        run("add", "edge/alert-times.json")  # change 321: when every alert went out''',
            'run("add", "edge/alert-times.json")')
    t = lit(t, "321: ESPN racer", 'if __name__ == "__main__":', ESPN_BLOCK, "change 321: race ESPN's feed")
    py_ok("gm_live.py", t)
    return t


edit("gm_live.py", go)
