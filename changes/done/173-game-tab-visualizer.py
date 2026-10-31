# changes/173-game-tab-visualizer.py - NHL scores game view, GAME tab: a Goal Visualizer dropdown under every goal (same rink and replay as the Goal Tracker)

NEW_CSS = r'''  /* change 173 (install.py) */
  .gx-sc141 .gw173 { border-bottom: 1px solid var(--line); }
  .gx-sc141 .gw173 > .gr { border-bottom: 0; }
  .gx-sc141 .gv173 { display: flex; align-items: center; gap: 6px; margin: -4px 16px 10px 72px; padding: 0; background: none; color: var(--accent); font-size: 13px; font-weight: 600; }
  .gx-sc141 .gv173 i { font-style: normal; display: inline-block; transition: transform .25s ease; }
  .gx-sc141 .gv173 i.up { transform: rotate(180deg); }
  .gx-sc141 .gvb173 { padding: 0 16px 14px; max-width: 640px; margin: 0 auto; animation: gx173in .25s ease; }
  @keyframes gx173in { from { opacity: 0; transform: translateY(-8px); } to { opacity: 1; transform: none; } }
  @media (prefers-reduced-motion: reduce) { .gx-sc141 .gvb173 { animation: none; } }
  @media (max-width: 640px) { .gx-sc141 .gv173 { margin-left: 72px; } .gx-sc141 .gvb173 { padding: 0 12px 12px; } }
</style>'''

OLD_START = '{per[k].map((r) => <div key={r.i} className="gr">'
NEW_START = '{per[k].map((r) => <div key={r.i} className="gw173"><div className="gr">'

OLD_END = '<span>{r.x.awayScore}</span><span>{r.x.homeScore}</span></div>)}'
NEW_END = ('<span>{r.x.awayScore}</span><span>{r.x.homeScore}</span></div>'
           '{r.x.cx != null ? (() => { const k173 = "G" + r.g.id + "-" + r.i, on = !!gv163[k173]; return <>'
           '<button type="button" className="gv173" onClick={(e) => { e.stopPropagation(); setGv163((o) => ({ ...o, [k173]: !on })); }}>Goal Visualizer <i className={on ? "up" : ""}>{"\\u25be"}</i></button>'
           '{on ? <div className="gvb173"><GxRink163 x={r.x} g={r.g} tm={r.tm} s={s} /></div> : null}'
           '</>; })() : null}</div>)}')

def change(t):
    t = lit(t, "173: styles", "</style>", NEW_CSS, "change 173 (install.py)")
    t = lit(t, "173: goal row wrapper", OLD_START, NEW_START, 'className="gw173"><div className="gr">')
    t = lit(t, "173: visualizer under each goal", OLD_END, NEW_END, 'const k173 = "G"')
    return t

edit(APP, change)
