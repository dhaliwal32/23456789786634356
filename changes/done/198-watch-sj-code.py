# changes/198-watch-sj-code.py - Watch link uses "sj" for San Jose instead of "sjs"

def change(t):
    t = lit(t, "198: San Jose code", 'SJ: "sjs", TB: "tbl"', 'SJ: "sj", TB: "tbl"', 'SJ: "sj", TB: "tbl"')
    return t

edit(APP, change)
