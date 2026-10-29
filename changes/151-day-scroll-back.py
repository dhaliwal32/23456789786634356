# changes/151-day-scroll-back.py - simulate box: Best day to add slides sideways again like before 150 (everything else from 150 stays); tapping a player in the Pickups list opens his page instead of the simulate box (Simulate is on his page)

NEW_CSS = r'''  /* change 151 (install.py) */
  .gx-sim107 .days { overflow-x: auto !important; -webkit-overflow-scrolling: touch; }
  .gx-sim107 .dy { flex: 1 0 64px !important; padding: 8px 4px !important; }
  .gx-sim107 .dy b { font-size: 15px !important; }
  @media (max-width: 640px) { .gx-sim107 .dy span { font-size: 12px !important; } }
</style>'''


def change(t):
    t = lit(t, "151: styles", "</style>", NEW_CSS, "change 151 (install.py)")
    t = lit(t, "151: pickup row opens the player",
            'role="button" onClick={() => setSim({ add: r.f.id, drop: r.d.id })}>',
            'role="button" onClick={() => { if (window.__NAV) window.__NAV.player(r.f); }} data-gx="151">',
            'data-gx="151">')
    return t


edit(APP, change)
