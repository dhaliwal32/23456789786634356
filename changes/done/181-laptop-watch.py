# changes/181-laptop-watch.py - Laptop NHL Scoreboard: Watch button under the clock of every live game (it left the game view in 179)

NEW_CSS = r'''  /* change 181 (install.py) */
  .gx-sd141 .gm.c181 { cursor: pointer; }
  .gx-sd141 .gm .st.w181 { display: flex; flex-direction: column; align-items: flex-start; gap: 6px; }
  .gx-sd141 .gm .wt181 { display: inline-flex; align-items: center; justify-content: center; height: 24px; padding: 0 12px; border-radius: 999px; background: #5b7cf0; color: #fff; font-size: 12px; font-weight: 600; text-decoration: none; }
  .gx-sd141 .gm .wt181:hover { filter: brightness(1.1); }
</style>'''

OLD_OPEN = r'''<button type="button" className="gm" onClick={() => openGame(g.id)}>'''
NEW_OPEN = r'''<div role="button" tabIndex={0} className="gm c181" onClick={() => openGame(g.id)}>'''

OLD_ST = r''' : <div className={"st" + (live(g) ? " lv" : "")}>{status(g)}</div>}
'''
NEW_ST = r''' : <div className={"st" + (live(g) ? " lv w181" : "")}><span>{status(g)}</span>{live(g) ? <a className="wt181" href={gxWatchUrl175(g, g.id)} target="_blank" rel="noopener noreferrer" onClick={(e) => e.stopPropagation()}>Watch</a> : null}</div>}
'''

OLD_CLOSE = r'''                  : <div className="fp"><div><b>{abA}:</b> {f1(fpOf(tA, ta) + fpOf(tA, th))} FPTS</div><div><b>{abB}:</b> {f1(fpOf(tB, ta) + fpOf(tB, th))} FPTS</div></div>}
              </button>'''
NEW_CLOSE = r'''                  : <div className="fp"><div><b>{abA}:</b> {f1(fpOf(tA, ta) + fpOf(tA, th))} FPTS</div><div><b>{abB}:</b> {f1(fpOf(tB, ta) + fpOf(tB, th))} FPTS</div></div>}
              </div>'''


def change(t):
    t = lit(t, "181: styles", "</style>", NEW_CSS, "change 181 (install.py)")
    t = lit(t, "181: card can hold a link", OLD_OPEN, NEW_OPEN, 'className="gm c181"')
    t = lit(t, "181: Watch under the clock", OLD_ST, NEW_ST, 'className="wt181"')
    t = lit(t, "181: card end", OLD_CLOSE, NEW_CLOSE, "FPTS</div></div>}\n              </div>")
    return t


edit(APP, change)
