# changes/310-tall-screen.py - tall (portrait) monitors: the Matchup page keeps its Goal Tracker and Scoreboard column from 1000 px wide (so a 1080 px portrait screen works at 100% zoom with bigger text), the column follows down the screen, and the empty space under the Scoreboard shows every goal tonight, newest first

NEW_CSS = r'''  /* change 310 (install.py): tall screens */
  .gx-gl310 { display: none; }
  @media (orientation: portrait) and (min-width: 1000px) and (max-width: 1099.98px) {
    .gx-mu141 { display: grid; grid-template-columns: minmax(0, 1fr) 360px; gap: 16px; align-items: start; }
    .gx-mu141 > .sd { display: block; position: sticky; top: 72px; max-height: calc(100vh - 84px); overflow-y: auto; }
    .gx-ib141 { display: none !important; }
  }
  @media (orientation: portrait) and (min-width: 1000px) {
    .gx-gl310 { display: block; }
  }
  .gx-gl310 .g { display: flex; align-items: center; gap: 10px; width: 100%; padding: 8px 14px 8px 10px; border-top: 1px solid var(--line); font-size: 13px; cursor: pointer; }
  .gx-gl310 .bh + .g { border-top: 0; }
  .gx-gl310 .g:hover { background: var(--card2, var(--line)); }
  .gx-gl310 .g.on { background: var(--accentSoft); }
  .gx-gl310 .g > i { flex: none; width: 3px; align-self: stretch; border-radius: 2px; background: var(--line); }
  .gx-gl310 .g > i.me { background: #8bd450; }
  .gx-gl310 .g > i.op { background: #8fb6e6; }
  .gx-gl310 .f { flex: none; width: 32px; height: 32px; border-radius: 999px; overflow: hidden; background: var(--line); }
  .gx-gl310 .f img { width: 100%; height: 100%; object-fit: cover; }
  .gx-gl310 .w { flex: 1; min-width: 0; line-height: 1.3; }
  .gx-gl310 .w b { display: block; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .gx-gl310 .w small, .gx-gl310 .sc { font-size: 12px; color: var(--mute); }
  .gx-gl310 .sc { flex: none; text-align: right; font-variant-numeric: tabular-nums; line-height: 1.3; }
</style>'''

OLD = '''          }) : <div style={{ padding: 14, color: "var(--mute)", fontSize: 13 }}>No NHL games today.</div>}
        </div>
        {open ? GX_SHEET141() : null}'''

NEW = '''          }) : <div style={{ padding: 14, color: "var(--mute)", fontSize: 13 }}>No NHL games today.</div>}
        </div>
        {/* change 310: on a tall screen, every goal tonight under the scoreboard; tap one to show it in the Goal Tracker */}
        {n > 1 ? (
          <div className="bx gx-gl310" data-gx="310">
            <div className="bh"><span>Every goal tonight</span><span className="r">{n}</span></div>
            {goals.map((q, j) => [q, j]).reverse().map(([q, j]) => {
              const aw = gxAb131((q.g.awayTeam || {}).abbrev), hm = gxAb131((q.g.homeTeam || {}).abbrev), hs = gxHs141(q.x, q.p);
              return (
                <div key={"g310" + q.g.id + "-" + q.i} role="button" tabIndex={0} className={"g" + (j === idx ? " on" : "")} onClick={() => setGi(j >= n - 1 ? null : j)}>
                  <i className={q.mk}></i>
                  <span className="f">{hs ? <img src={hs} alt="" onError={(e) => { e.currentTarget.style.display = "none"; }} /> : null}</span>
                  <div className="w"><b>{shortN(q.n)}</b><small>{q.tm + " \\u00b7 " + (q.x.timeInPeriod || "") + " " + gxPer131(q.x.periodDescriptor)}</small></div>
                  <div className="sc">{aw + " " + q.x.awayScore}<br />{hm + " " + q.x.homeScore}</div>
                </div>
              );
            })}
          </div>
        ) : null}
        {open ? GX_SHEET141() : null}'''


def change(t):
    t = lit(t, "310: styles", "</style>", NEW_CSS, "change 310 (install.py): tall screens")
    t = lit(t, "310: every goal tonight", OLD, NEW, "change 310: on a tall screen")
    return t


edit(APP, change)
