# changes/154-matchup-one-colour.py - Matchup day box: every score in exactly the same grey as the stat lines (same colour, same fade for finished games), nothing white or bold

NEW_CSS = r'''  /* change 154 (install.py) */
  .gx-h2h.gx-tt147 > div:nth-child(2), .gx-h2h.gx-tt147 > div:nth-child(4),
  .gx-h2h.gx-tt147 > div:nth-child(2) *, .gx-h2h.gx-tt147 > div:nth-child(4) *,
  .gx-h2h [data-gx="138pts"], .gx-h2h [data-gx="138pts"] *, .gx-h2h [data-gx="135n"], .gx-h2h [data-gx="135n"] *,
  .gx-h2h .gx-sv147, .gx-h2h .text-slate-700, .gx-h2h .text-slate-700 *, .gx-h2h .gx-sl98, .gx-h2h .gx-pc .text-xs, .gx-h2h .gx-pc .text-xs * { color: var(--mute) !important; font-weight: 400 !important; }
  .gx-h2h > .gx-fin + div, .gx-h2h > div:has(+ .gx-fin) { opacity: .5; }
</style>'''

def change(t):
    return lit(t, "154: styles", "</style>", NEW_CSS, "change 154 (install.py)")

edit(APP, change)
