# changes/200-watch-nj-code.py - Watch link uses "nj" for New Jersey instead of "njd"

def change(t):
    t = lit(t, "200: New Jersey code", 'NJ: "njd", SJ', 'NJ: "nj", SJ', 'NJ: "nj", SJ')
    return t

edit(APP, change)
