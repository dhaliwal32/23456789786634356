# changes/155-matchup-team-like-espn.py - Matchup rows like ESPN FantasyCast: team code and position after each name (laptop), and the opponent before the game score on laptop too ("WPG W 5-2")

NEW_CSS = r'''  /* change 155 (install.py) */
  .gx-h2h .gx-tp155 { font-size: 12px; color: var(--mute); margin-left: 6px; font-weight: 400; white-space: nowrap; }
  .gx-h2h .gx-pc .text-xs .m-inl { display: inline !important; }
  @media (max-width: 640px) { .gx-h2h .gx-tp155 { display: none; } }
</style>'''

def change(t):
    t = lit(t, "155: styles", "</style>", NEW_CSS, "change 155 (install.py)")
    t = lit(t, "155: team after name",
            '<span className="gx-tl98"><TeamLogo t={p.t} size={15} /></span>',
            '<span className="gx-tl98"><TeamLogo t={p.t} size={15} /></span><span className="gx-tp155">{p.t + " " + p.p}</span>',
            'className="gx-tp155"', count=2)
    return t

edit(APP, change)
