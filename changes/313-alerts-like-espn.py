# changes/313-alerts-like-espn.py - phone alerts copy ESPN's look: bold "Fantasy Islands" on top, the message in normal text under it (the iPhone adds its "from" line in between for home screen apps)

def go(t):
    t = lit(t, "313: lead alerts like ESPN",
            '        gm_push.send(msg, "", "#matchup")  # change 312: the message is the title, so only the app name shows above it',
            '        gm_push.send("\\U0001F3D2 Fantasy Islands", msg, "#matchup")  # change 313: like ESPN, bold name on top, message under it',
            'change 313: like ESPN, bold name on top')
    t = lit(t, "313: goal alerts like ESPN",
            'gm_push.send(msg, "", "#matchup")  # change 312: the message is the title (Kuvar wants only the app name above it, not a second name)',
            'gm_push.send("\\U0001F3D2 Fantasy Islands", msg, "#matchup")  # change 313: like ESPN (Kuvar picked this, Nov 17)',
            'change 313: like ESPN (Kuvar')
    py_ok("gm_live.py", t)
    return t


edit("gm_live.py", go)
