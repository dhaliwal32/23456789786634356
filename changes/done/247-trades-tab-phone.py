# changes/247-trades-tab-phone.py - phone top menu: Roster, Matchup, Players, Lines, Trades as tabs; League and Setup in More

NEW_CSS = r'''  /* change 247 (install.py) */
  @media (max-width: 640px) {
    .gx-tm103 .tb a, .gx-tm103 .tb .mr241 { padding: 14px 2px 11px; font-size: clamp(10.5px, 3.05vw, 13px); }
    .gx-tm103 .tb .mr241 svg { width: 10px; height: 10px; }
  }
</style>'''

def change(t):
    t = lit(t, "247: trades on the main tabs",
            'const GX_MAIN241 = ["roster", "matchup", "players", "lines"];',
            'const GX_MAIN241 = ["roster", "matchup", "players", "lines", "trades"]; // change 247',
            '"trades"]; // change 247')
    t = lit(t, "247: styles", "</style>", NEW_CSS, "change 247 (install.py)")
    return t

edit(APP, change)
