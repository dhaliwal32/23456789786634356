# changes/305-alerts-no-title.py - goal / assist alerts and the test alert are sent with no title, so the iPhone shows only the home screen app's name (name it "\U0001F3D2 Fantasy Islands") and the line underneath, like ESPN's

SW_OLD = '''showNotification(d.title || "Fantasy GM", {'''
SW_NEW = '''showNotification(d.title != null ? d.title : "Fantasy GM", { /* change 305: an empty title stays empty */'''
LV_OLD = '''gm_push.send("\\U0001F3D2 Fantasy Islands", msg, "#matchup")'''
LV_NEW = '''gm_push.send("", msg, "#matchup")  # change 305: no title, the app's name shows instead'''
PS_OLD = '''send("Fantasy GM", "Test - alerts from the app are working.", "#matchup")'''
PS_NEW = '''send("", "Test - alerts from the app are working.", "#matchup")  # change 305'''

edit("sw.js", lambda t: lit(t, "305: empty title allowed", SW_OLD, SW_NEW, "change 305: an empty title stays empty"))
edit("gm_live.py", lambda t: lit(t, "305: goal alerts with no title", LV_OLD, LV_NEW, "change 305: no title"))
edit("gm_push.py", lambda t: lit(t, "305: test alert with no title", PS_OLD, PS_NEW, "# change 305"))
