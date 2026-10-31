# changes/162-live-every-2s.py - while a game is live and the app is open, check scores and player stats every 2 seconds (was 10), with no reused copies older than 2 seconds

def change(t):
    t = lit(t, "162: pull every 2 s",
            "> 59000) pull(); }, 10 * 1000); /* gx120 */",
            "> 59000) pull(); }, 2 * 1000); /* gx120 gx162 */",
            "}, 2 * 1000); /* gx120 gx162 */")
    t = lit(t, "162: summary kept 2 s",
            "if (c && (c.p || Date.now() - c.at < 10000)) return",
            "if (c && (c.p || Date.now() - c.at < 2000)) return",
            "Date.now() - c.at < 2000)) return")
    t = lit(t, "162: fresh summary",
            '"summary?event=" + id + "&_=" + Math.floor(Date.now() / 5000)',
            '"summary?event=" + id + "&_=" + Math.floor(Date.now() / 2000)',
            '"&_=" + Math.floor(Date.now() / 2000)).then')
    t = lit(t, "162: fresh scoreboard",
            '.replace(/-/g, "") + "&_=" + Math.floor(Date.now() / 5000)',
            '.replace(/-/g, "") + "&_=" + Math.floor(Date.now() / 2000)',
            '.replace(/-/g, "") + "&_=" + Math.floor(Date.now() / 2000)')
    return t

edit(APP, change)
