# changes/323-news-alerts-two-lines.py - line, lineup and injury alerts use the same two lines as goal alerts (Kuvar, Nov 19): the news on top, then "from <app>"; no more "Fantasy GM" line

def go(t):
    t = lit(t, "323: news alerts, two lines",
            '        app_ok = gm_push.send(title, msg, "#myteam") > 0',
            '        app_ok = gm_push.send(msg, "", "#myteam") > 0  # change 323: two lines like goal alerts (change 315), no "Fantasy GM" title',
            'change 323: two lines like goal alerts')
    py_ok("gm_notify.py", t)
    return t


edit("gm_notify.py", go)
