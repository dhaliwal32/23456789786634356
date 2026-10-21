# changes/091-autopilot-page-back.py - Autopilot page goes back to the simple version (no in-app buttons, no GitHub key needed); explains days_ahead in autopilot.json

def change(t):
    t = lit(t, "091: simple autopilot page",
            'sub === "autopilot" ? <GxAutoPage2 {...P} /> :',
            'sub === "autopilot" ? <GxAutoPage {...P} /> : /* gx091 */',
            'sub === "autopilot" ? <GxAutoPage {...P} /> : /* gx091 */')
    t = lit(t, "091: days ahead how-to",
            'then Commit changes. It takes effect at the next sync.</div>',
            'then Commit changes. It takes effect at the next sync. To set lineups ahead, change the number after "days_ahead": 0 is today only, 3 is the next 3 days too, 7 is a week. Days after today are set once, then only changed again on the day itself.</div>{/* gx091-ahead */}',
            '{/* gx091-ahead */}')
    return t

edit(APP, change)
