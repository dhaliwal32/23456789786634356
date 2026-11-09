# changes/221-all-players-filters-block.py - All players filters as one neat block on the phone: positions, then both team lists side by side, then search

NEW_CSS = r'''  /* change 221 (install.py): All players filters in one block on the phone */
  @media (max-width: 640px) {
    [data-c78="rank"] > div:first-child { display: grid !important; grid-template-columns: 1fr 1fr; gap: 8px; }
    [data-c78="rank"] > div:first-child > .gx-seg { grid-column: 1 / -1; display: grid; grid-auto-flow: column; grid-auto-columns: 1fr; }
    [data-c78="rank"] > div:first-child > .gx-seg button { text-align: center; }
    [data-c78="rank"] > div:first-child > select { width: 100%; min-width: 0; }
    [data-c78="rank"] > div:first-child > input { grid-column: 1 / -1; width: 100%; min-width: 0; }
  }
</style>'''

def change(t):
    t = lit(t, "221: styles", "</style>", NEW_CSS, "change 221 (install.py)")
    return t

edit(APP, change)
