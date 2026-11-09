# changes/220-tab-bar-fits.py - on the phone all seven tabs fit across the top, nothing cut off at the edges

NEW_CSS = r'''  /* change 220 (install.py): all seven phone tabs fit the width */
  @media (max-width: 640px) {
    .gx-tm103 .tb { overflow-x: hidden; padding: 0 2px; justify-content: space-between; }
    .gx-tm103 .tb a { flex: 1 1 auto; min-width: 0; text-align: center; white-space: nowrap; padding: 12px 1px 9px; font-size: clamp(10px, 2.95vw, 13px); letter-spacing: 0; }
  }
</style>'''

def change(t):
    t = lit(t, "220: styles", "</style>", NEW_CSS, "change 220 (install.py)")
    return t

edit(APP, change)
