# changes/314-alert-no-top-line.py - phone alerts drop the bold top line (Kuvar marked it out, Nov 17): the title is an invisible character, so only "from <app name>" and the message show (an empty title makes the iPhone put the app name back)

T0 = '"\\U0001F3D2 Fantasy Islands"'
T1 = '"\\u200b"'


def live(t):
    t = lit(t, "314: lead alerts, no top line",
            'gm_push.send(' + T0 + ', msg, "#matchup")  # change 313: like ESPN, bold name on top, message under it',
            'gm_push.send(' + T1 + ', msg, "#matchup")  # change 314: invisible title, no top line (Kuvar, Nov 17)',
            'change 314: invisible title, no top line')
    t = lit(t, "314: goal alerts, no top line",
            'gm_push.send(' + T0 + ', msg, "#matchup")  # change 313: like ESPN (Kuvar picked this, Nov 17)',
            'gm_push.send(' + T1 + ', msg, "#matchup")  # change 314: invisible title; only "from <app>" and the message show',
            'only "from <app>" and the message show')
    py_ok("gm_live.py", t)
    return t


def push(t):
    t = lit(t, "314: test alert, no top line",
            'n = send(' + T0 + ', "Test - alerts from the app are working.", "#matchup")  # change 311',
            'n = send(' + T1 + ', "Test - alerts from the app are working.", "#matchup")  # change 314: same look as real alerts',
            'change 314: same look as real alerts')
    py_ok("gm_push.py", t)
    return t


edit("gm_live.py", live)
edit("gm_push.py", push)
