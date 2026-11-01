# changes/179-phone-scores-espn.py - Phone NHL Scores list like the ESPN app: Watch button on each live game, team records and betting line before puck drop

NEW_CSS = r'''  /* change 179 (install.py) */
  .gx-gc140 .cd.c179 { display: block; padding: 0; cursor: pointer; }
  .gx-gc140 .c179 .tp { display: flex; align-items: center; padding: 12px 14px; }
  .gx-gc140 .c179 .tr .rc { font-size: 12px; color: var(--mute); font-variant-numeric: tabular-nums; }
  .gx-gc140 .c179 .st { display: flex; flex-direction: column; justify-content: center; gap: 8px; }
  .gx-gc140 .c179 .wt179 { display: inline-flex; align-items: center; justify-content: center; height: 32px; border-radius: 999px; background: #5b7cf0; color: #fff; font-size: 15px; font-weight: 600; text-decoration: none; }
  .gx-gc140 .c179 .wt179:active { transform: scale(.97); }
  .gx-gc140 .c179 .od { margin: 0 12px 12px; border-radius: 6px; box-shadow: inset 0 0 0 1px var(--line); font-size: 13px; }
  .gx-gc140 .c179 .od > button { display: flex; align-items: center; justify-content: center; gap: 6px; width: 100%; padding: 10px 30px 10px 12px; position: relative; white-space: nowrap; }
  .gx-gc140 .c179 .od > button .c { position: absolute; right: 12px; transition: transform .25s ease; }
  .gx-gc140 .c179 .od > button .c.up { transform: rotate(180deg); }
  .gx-gc140 .c179 .od .k { color: var(--mute); }
  .gx-gc140 .c179 .od .x { overflow: hidden; max-height: 0; transition: max-height .28s ease; }
  .gx-gc140 .c179 .od .x.on { max-height: 60px; }
  .gx-gc140 .c179 .od .x > div { padding: 0 12px 10px; text-align: center; color: var(--mute); }
</style>'''

OLD_FEED = r'''abbrev: gxAb132(tm.abbreviation), score: x.score == null || ty.state === "pre" ? undefined : +x.score, logo: tm.logo || "" };'''
NEW_FEED = r'''abbrev: gxAb132(tm.abbreviation), score: x.score == null || ty.state === "pre" ? undefined : +x.score, logo: tm.logo || "", rec179: ((x.records || [])[0] || {}).summary || "" };'''

OLD_LIST = r'''          <button key={g.id} type="button" className="cd" onClick={() => openGame(g.id)}><div className="tms">{rows2(g)}</div><div className={"st" + (live(g) ? " lv" : pre(g) ? " pr" : "")}>{status(g)}</div></button>'''
NEW_LIST = r'''          (() => { /* change 179: game cards like the ESPN app */
            const p0 = pre(g), ta = gxAb131((g.awayTeam || {}).abbrev), th = gxAb131((g.homeTeam || {}).abbrev);
            const rw = (T) => <div className="tr"><TeamLogo t={gxAb131(T.abbrev)} size={24} /><span className="nm">{gxNick141(T.abbrev)}</span><span className="rc">{T.rec179 || ""}</span></div>;
            return (
              <div key={g.id} role="button" tabIndex={0} className="cd c179" onClick={() => openGame(g.id)}>
                <div className="tp">
                  <div className="tms">{p0 ? [rw(g.awayTeam || {}), rw(g.homeTeam || {})] : rows2(g)}</div>
                  <div className={"st" + (live(g) ? " lv" : p0 ? " pr" : "")}><span>{status(g)}</span>{live(g) ? <a className="wt179" href={gxWatchUrl175(g, g.id)} target="_blank" rel="noopener noreferrer" onClick={(e) => e.stopPropagation()}>Watch</a> : null}</div>
                </div>
                {p0 && g.ml && (g.ml.a != null || g.ou != null) ? (
                  <div className="od" onClick={(e) => e.stopPropagation()}>
                    <button type="button" onClick={() => setOx146((o) => ({ ...o, [g.id]: !o[g.id] }))}><span className="k">ML:</span> <b>{ta + " " + ml146(gxML147(g.ml.a, ta))}</b> <span className="k">@</span> <b>{th + " " + ml146(gxML147(g.ml.h, th))}</b>{g.ou != null ? <><span className="k">{" \u00b7 Total:"}</span> <b>{g.ou}</b></> : null}<span className={"c" + (ox146[g.id] ? " up" : "")}>{"\u2304"}</span></button>
                    <div className={"x" + (ox146[g.id] ? " on" : "")}><div>{g.sp ? "Line: " + g.sp : "No puck line yet."}</div></div>
                  </div>
                ) : null}
              </div>
            );
          })()'''

OLD_WATCH = r'''        <a className="gx-wt174" href={gxWatchUrl175(g, gid)} target="_blank" rel="noopener noreferrer"><svg viewBox="0 0 10 10" aria-hidden="true"><path d="M2 1 L9 5 L2 9 Z" /></svg>Watch</a>
'''
NEW_WATCH = r'''        {/* change 179: Watch moved onto the live game cards in the scoreboard */}
'''


def change(t):
    t = lit(t, "179: styles", "</style>", NEW_CSS, "change 179 (install.py)")
    t = lit(t, "179: team records from ESPN", OLD_FEED, NEW_FEED, "rec179:")
    t = lit(t, "179: phone game cards", OLD_LIST, NEW_LIST, "change 179: game cards like the ESPN app")
    t = lit(t, "179: Watch moved", OLD_WATCH, NEW_WATCH, "change 179: Watch moved onto the live game cards")
    return t


edit(APP, change)
