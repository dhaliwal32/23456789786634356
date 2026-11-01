# changes/176-matchup-names-live-white.py - Matchup: a player's name is white only while his game is live (grey before and after); his points are white once his game has started, live or final, grey only before he plays (day total white once the day has started)

NEW_CSS = r'''  /* change 176 (install.py) */
  .gx-h2h .gx-pc.gx-lv176 .gx-nm, .gx-h2h .gx-pc.gx-lv176 .gx-nm button { color: var(--ink) !important; }
</style>'''

def change(t):
    t = lit(t, "176: styles", "</style>", NEW_CSS, "change 176 (install.py)")
    t = lit(t, "176: name white while live", '(p.st === "F" ? " gx-fin" : "")', '(p.st === "F" ? " gx-fin" : "") + (p.st === "L" ? " gx-lv176" : "")', '(p.st === "L" ? " gx-lv176" : "")')
    t = lit(t, "176: points white once started", '(p.st === "L" ? " gx-on157" : "")', '(p.st ? " gx-on157" : "") + "" /* gx176 */', '(p.st ? " gx-on157" : "") + "" /* gx176 */')
    t = lit(t, "176: day total white once started", '(state === "live" ? " gx-on157" : "")', '(state !== "projected" ? " gx-on157" : "") + "" /* gx176 */', '(state !== "projected" ? " gx-on157" : "") + "" /* gx176 */')
    return t

edit(APP, change)
