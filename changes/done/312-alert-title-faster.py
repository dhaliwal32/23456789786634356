# changes/312-alert-title-faster.py - phone alerts show only the message under the app's name (no "Fantasy Islands" line on top), and goal / assist alerts come faster: checks every 15 seconds, finished games are not re-read, and the watcher stays on between games instead of waiting for GitHub's late schedule

def go(t):
    t = lit(t, "312: every 15 seconds",
            'EVERY = 30          # seconds between checks while games are on',
            'EVERY = 15          # seconds between checks while games are on (change 312: was 30)',
            'EVERY = 15  ')
    t = lit(t, "312: lead alerts, message as the title",
            '        gm_push.send(title, msg, "#matchup")',
            '        gm_push.send(msg, "", "#matchup")  # change 312: the message is the title, so only the app name shows above it',
            'gm_push.send(msg, "", "#matchup")  # change 312')
    t = lit(t, "312: goal alerts, message as the title",
            'gm_push.send("\\U0001F3D2 Fantasy Islands", msg, "#matchup")  # change 311: title back (no title showed the name twice)',
            'gm_push.send(msg, "", "#matchup")  # change 312: the message is the title (Kuvar wants only the app name above it, not a second name)',
            'only the app name above it, not a second name')
    t = lit(t, "312: skip finished games",
            '''        if st not in ("in", "post"):
            continue''',
            '''        if st not in ("in", "post") or ev.get("id") in _fin312:
            continue
        if st == "post" and _primed302:
            _fin312.add(ev.get("id"))  # change 312: read a finished game one last time, then skip it''',
            '_fin312.add(ev.get("id"))')
    t = lit(t, "312: finished set",
            '_seen302, _primed302, _opp302 = set(), False, {"id": None, "ids": set(), "at": 0}',
            '_seen302, _primed302, _opp302 = set(), False, {"id": None, "ids": set(), "at": 0}\n_fin312 = set()  # change 312: finished games already read',
            '_fin312 = set()  # change 312')
    t = lit(t, "312: stay on until the last game",
            """            if nxt is None or nxt > 75:
                log("no game live and none soon - stopping")""",
            """            if nxt is None:  # change 312: stay on between games (GitHub's schedule can start it hours late); stop after the last one
                log("no game live and none left today - stopping")""",
            "none left today - stopping")
    py_ok("gm_live.py", t)
    return t


edit("gm_live.py", go)
