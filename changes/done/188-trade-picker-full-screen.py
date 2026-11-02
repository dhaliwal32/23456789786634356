# changes/188-trade-picker-full-screen.py - Trades "+ Add players" sheet on the phone fills the whole screen: the player list grows to fill it and Done sits at the very bottom (above the iPhone home bar)

NEW_CSS = r'''  /* change 188 (install.py) */
  @media (max-width: 640px) {
    .gx-so107 > .gx-sim107.gx-pk113 { display: flex; flex-direction: column; height: 100%; min-height: 100%; padding-bottom: calc(12px + env(safe-area-inset-bottom, 0px)); }
    .gx-pk113 .hd, .gx-pk113 .sr, .gx-pk113 .act { flex: none; }
    .gx-pk113 .lst { max-height: none; flex: 1 1 auto; min-height: 0; overscroll-behavior: contain; }
    .gx-pk113 .act { margin-top: 10px; }
  }
</style>'''


def change(t):
    t = lit(t, "188: styles", "</style>", NEW_CSS, "change 188 (install.py)")
    return t


edit(APP, change)
