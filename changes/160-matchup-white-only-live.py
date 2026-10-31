# changes/160-matchup-white-only-live.py - Matchup: every player name grey; a player's points are white only while his game is being played, grey before and after it ends (day total white only while live)

NEW_CSS = r'''  /* change 160 (install.py) */
  .gx-h2h .gx-pc .gx-nm, .gx-h2h .gx-pc .gx-nm button { color: var(--mute) !important; }
</style>'''

def change(t):
    t = lit(t, "160: styles", "</style>", NEW_CSS, "change 160 (install.py)")
    t = lit(t, "160: white only while live", '(p.st ? " gx-on157" : "")', '(p.st === "L" ? " gx-on157" : "")', '(p.st === "L" ? " gx-on157" : "")')
    t = lit(t, "160: day total white only while live", '(state !== "projected" ? " gx-on157" : "")', '(state === "live" ? " gx-on157" : "")', '(state === "live" ? " gx-on157" : "")')
    return t

edit(APP, change)
