# changes/192-smaller-matchup-faces-laptop.py - Matchup on the laptop: player photos smaller (about 33 px instead of 48) and rows a bit shorter (56 px instead of 72), so the list is tighter; phone unchanged

NEW_CSS = r'''  /* change 192 (install.py) */
  @media (min-width: 641px) {
    .gx-h2h { --gx-fs: 1.1; }
    .gx-h2h > .gx-pc { min-height: 56px; }
  }
</style>'''


def change(t):
    t = lit(t, "192: styles", "</style>", NEW_CSS, "change 192 (install.py)")
    return t


edit(APP, change)
