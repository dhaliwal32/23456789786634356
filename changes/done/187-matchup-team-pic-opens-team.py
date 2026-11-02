# changes/187-matchup-team-pic-opens-team.py - Matchup: tapping either team's picture opens that team's page (your own picture opens your Roster), the same as tapping the team name

OLD_A = r'''<div className="text-sm font-semibold gx-nm114" style={mine ? { color: "var(--accent)" } : null}><GxFtPic114 id={a} size={22} /><TL s={s} id={a} /></div>'''
NEW_A = r'''<div className="text-sm font-semibold gx-nm114" style={mine ? { color: "var(--accent)" } : null}><button type="button" className="gx-tp187" aria-label={"Open " + teamName(s, a)} onClick={(e) => { e.stopPropagation(); if (window.__NAV) window.__NAV.team(a); }}><GxFtPic114 id={a} size={22} /></button><TL s={s} id={a} /></div>'''
OLD_B = r'''<div className="text-sm text-slate-500 gx-nm114 r"><TL s={s} id={b} /><GxFtPic114 id={b} size={22} /></div>'''
NEW_B = r'''<div className="text-sm text-slate-500 gx-nm114 r"><TL s={s} id={b} /><button type="button" className="gx-tp187" aria-label={"Open " + teamName(s, b)} onClick={(e) => { e.stopPropagation(); if (window.__NAV) window.__NAV.team(b); }}><GxFtPic114 id={b} size={22} /></button></div>'''

NEW_CSS = r'''  /* change 187 (install.py) */
  .gx-tp187 { display: inline-flex; flex: none; padding: 0; border-radius: 7px; transition: transform .12s ease, opacity .12s ease; }
  .gx-tp187:hover { opacity: .85; }
  .gx-tp187:active { transform: scale(.94); }
</style>'''


def change(t):
    t = lit(t, "187: styles", "</style>", NEW_CSS, "change 187 (install.py)")
    t = lit(t, "187: left team picture", OLD_A, NEW_A, 'aria-label={"Open " + teamName(s, a)}')
    t = lit(t, "187: right team picture", OLD_B, NEW_B, 'aria-label={"Open " + teamName(s, b)}')
    return t


edit(APP, change)
