# changes/319-tidy-alert-code.py - removes alert code nothing runs any more: the switched-off ntfy sender, and the old ESPN goal check that change 318 replaced (alerts work exactly the same)

OLD, NEW = [], []

OLD.append('    if True:  # change 284: ntfy switched off (Kuvar, Nov 14, 2026); alerts go only to the app. Delete these two lines to bring ntfy back.\n        return\n    if not NTFY_TOPIC:\n        log("(no ntfy topic)", title, msg)\n        return\n    try:\n        requests.post(f"https://ntfy.sh/{NTFY_TOPIC}", data=msg.encode("utf-8"),\n                      headers={"Title": title, "Priority": "default"}, timeout=20)  # change 261: no Click link, tapping opens ntfy\n    except Exception as e:\n        log("ntfy failed", e)\n')
NEW.append('')
OLD.append('NTFY_TOPIC = os.environ.get("NTFY_TOPIC", "").strip()\n')
NEW.append('')
OLD.append('EVERY = 15          # seconds between checks while games are on (change 312: was 30)\n')
NEW.append('')
OLD.append('SB302 = "https://site.api.espn.com/apis/site/v2/sports/hockey/nhl/"\n_seen302, _primed302, _opp302 = set(), False, {"id": None, "ids": set(), "at": 0}\n_fin312 = set()  # change 312: finished games already read\n\n\n')
NEW.append('_opp302 = {"id": None, "ids": set(), "at": 0}  # the opponent\'s roster (change 302, names added in 318)\n\n\n')
OLD.append('def _count302(text, name, goal):\n    import re as _re\n    if goal:\n        m = _re.search(r"Goal \\((\\d+)\\)", text or "")\n    else:\n        m = _re.search(_re.escape(name) + r" \\((\\d+)\\)", text or "")\n    return f" ({m.group(1)})" if m else ""\n\n\n')
NEW.append('')
OLD.append('def _recent311(wc):\n    try:\n        t = datetime.strptime(str(wc)[:19], "%Y-%m-%dT%H:%M:%S").replace(tzinfo=timezone.utc)\n        return (datetime.now(timezone.utc) - t).total_seconds() < 3 * 3600\n    except Exception:\n        return False\n\n\ndef goal_alerts302(opp):\n    global _primed302\n    if not opp:\n        return\n    ids = _opp_ids302(opp)\n    if not _primed302:\n        log(f"goal alerts: opponent {opp}, {len(ids)} players")  # change 311\n    if not ids:\n        return\n    try:\n        sb = requests.get(SB302 + "scoreboard", timeout=20).json()\n    except Exception as e:\n        log("goal check failed", e)\n        return\n    for ev in sb.get("events", []):\n        st = (((ev.get("status") or {}).get("type")) or {}).get("state")\n        if st not in ("in", "post") or ev.get("id") in _fin312:\n            continue\n        if st == "post" and _primed302:\n            _fin312.add(ev.get("id"))  # change 312: read a finished game one last time, then skip it\n        try:\n            sm = requests.get(SB302 + "summary", params={"event": ev.get("id")}, timeout=20).json()\n        except Exception:\n            continue\n        for p in sm.get("plays") or []:\n            if not p.get("scoringPlay") or ((p.get("period") or {}).get("number") or 0) >= 5:\n                continue          # shootout goals do not count\n            for q in p.get("participants") or []:\n                a = q.get("athlete") or {}\n                try:\n                    pid = int(a.get("id"))\n                except Exception:\n                    continue\n                kind = q.get("type")\n                if pid not in ids or kind not in ("scorer", "assister"):\n                    continue\n                key = f"{p.get(\'id\')}|{pid}"\n                if key in _seen302:\n                    continue\n                _seen302.add(key)\n                if not _primed302 and (key in _sent311() or not _recent311(p.get("wallclock"))):\n                    continue          # change 311: before this run started, only goals from the last 3 hours not already sent\n                name = a.get("displayName") or a.get("fullName") or ""\n                goal = kind == "scorer"\n                msg = ("Goal by " if goal else "Assist by ") + name + _count302(p.get("text"), name, goal)\n                try:\n                    import gm_push\n                    gm_push.send(msg, "", "#matchup")  # change 315: two lines (Kuvar picked this, Nov 17); do not change again without asking\n                    _mark311(key)\n                except Exception as e:\n                    log("goal alert failed", e)\n                log("goal alert:", msg)\n    _primed302 = True\n\n\n')
NEW.append('')
OLD.append("gm_live.py - watches your matchup during NHL games and buzzes your phone (ntfy) when the lead changes.\n\nRuns on GitHub (live-alerts.yml). It checks ESPN's live matchup score about every 30 seconds while\ngames are on, and stops by itself when no game is live and none starts in the next 75 minutes.\n")
NEW.append("gm_live.py - watches your matchup during NHL games: goal and assist alerts for the other team's players\n(from the NHL live feed, change 318) and who was on the ice for each goal. Runs on GitHub (live-alerts.yml)\nand stops by itself after the day's last game. Lead-change alerts are off (change 317).\n")
NAMES = ['319: ntfy code gone', '319: ntfy setting gone', '319: unused EVERY', '319: old ESPN goal state', '319: old ESPN goal count', '319: old ESPN goal check', '319: file note']


def go(t):
    for nm, o, n in zip(NAMES, OLD, NEW):
        t = lit(t, nm, o, n, None)
    for gone in ('def goal_alerts302', 'def _count302', 'SB302 =', 'ntfy.sh', 'def _recent311', 'EVERY ='):
        if gone in t:
            fail('319: ' + gone + ' is still used somewhere')
    py_ok('gm_live.py', t)
    return t


edit('gm_live.py', go)
