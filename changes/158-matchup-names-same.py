# changes/158-matchup-names-same.py - Matchup: every player name the same colour like ESPN; players with no game today are no longer faded (their dash stays grey)

NEW_CSS = r'''  /* change 158 (install.py) */
  .gx-h2h .gx-idle147 { opacity: 1 !important; }
  .gx-h2h .gx-pc .gx-nm, .gx-h2h .gx-pc .gx-nm button { color: var(--ink) !important; }
</style>'''

def change(t):
    return lit(t, "158: styles", "</style>", NEW_CSS, "change 158 (install.py)")

edit(APP, change)
