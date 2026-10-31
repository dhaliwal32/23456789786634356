# changes/153-matchup-readable-stats.py - Matchup player scores in the same grey as the other numbers, full stat lines readable, every player row the same fixed height

NEW_CSS = r'''  /* change 153 (install.py) */
  .gx-h2h:not(.gx-tt147) [data-gx="138pts"] { color: var(--mute) !important; }
  .gx-h2h .gx-sl98 { display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; font-size: 12px; color: var(--mute); line-height: 16px; max-height: 32px; white-space: normal; overflow: hidden; }
  .gx-h2h .gx-st98 { display: none; }
  .gx-h2h > .gx-pc { min-height: 72px; }
  @media (max-width: 640px) {
    .gx-h2h .gx-sl98 { font-size: 11px; line-height: 14px; height: 28px; white-space: normal !important; overflow: hidden; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; text-overflow: clip; word-break: normal; }
    .gx-h2h > .gx-pc { min-height: 64px; align-items: flex-start; }
    .gx-h2h { grid-template-columns: minmax(0,1fr) 36px 12px 36px minmax(0,1fr); gap: 4px; }
  }
</style>'''

def change(t):
    return lit(t, "153: styles", "</style>", NEW_CSS, "change 153 (install.py)")

edit(APP, change)
