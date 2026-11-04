# changes/199-watch-tb-code.py - Watch link uses "tb" for Tampa Bay instead of "tbl"

def change(t):
    t = lit(t, "199: Tampa Bay code", 'TB: "tbl", UTAH', 'TB: "tb", UTAH', 'TB: "tb", UTAH')
    return t

edit(APP, change)
