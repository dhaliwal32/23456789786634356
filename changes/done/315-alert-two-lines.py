# changes/315-alert-two-lines.py - phone alerts are two lines (Kuvar picked this, Nov 17): the message on top, then the iPhone's "from <app name>" line; no body text

T1 = '"\\u200b"'


def live(t):
    t = lit(t, "315: lead alerts, two lines",
            'gm_push.send(' + T1 + ', msg, "#matchup")  # change 314: invisible title, no top line (Kuvar, Nov 17)',
            'gm_push.send(msg, "", "#matchup")  # change 315: two lines, message on top then "from <app>" (Kuvar picked this; iOS always needs a top line)',
            'change 315: two lines, message on top')
    t = lit(t, "315: goal alerts, two lines",
            'gm_push.send(' + T1 + ', msg, "#matchup")  # change 314: invisible title; only "from <app>" and the message show',
            'gm_push.send(msg, "", "#matchup")  # change 315: two lines (Kuvar picked this, Nov 17); do not change again without asking',
            'change 315: two lines (Kuvar picked')
    py_ok("gm_live.py", t)
    return t


def push(t):
    t = lit(t, "315: test alert, two lines",
            'n = send(' + T1 + ', "Test - alerts from the app are working.", "#matchup")  # change 314: same look as real alerts',
            'n = send("Test - alerts from the app are working.", "", "#matchup")  # change 315: same look as real alerts',
            'change 315: same look as real alerts')
    py_ok("gm_push.py", t)
    return t


edit("gm_live.py", live)
edit("gm_push.py", push)
