# changes/146-pregame-board.py - same spacing everywhere on Matchup (phone player lines never wrap, every row the same height); laptop NHL Scoreboard before games start, like ESPN: date, start time and TV channel, how many players each matchup team has in that game, and a betting line (moneyline and total) that opens to the puck line; games switch to scores once they start. The blinking LIVE light is gone everywhere

NEW_CSS = r'''  /* change 146 (install.py) */
  .gm-dot { display: none !important; animation: none !important; }
  .gx-sd141 .gm .st.pg { font-weight: 400; line-height: 1.35; }
  .gx-sd141 .gm .st.pg b { display: block; font-weight: 700; font-size: 13px; }
  .gx-sd141 .gm .st.pg small { display: block; color: var(--mute); font-size: 12px; }
  .gx-sd141 .od { margin: 0 12px 12px; border-radius: 6px; box-shadow: inset 0 0 0 1px var(--line); background: var(--card2, var(--bg)); font-size: 13px; }
  .gx-sd141 .od > button { display: flex; align-items: center; justify-content: center; gap: 6px; width: 100%; padding: 10px 12px; position: relative; }
  .gx-sd141 .od > button .c { position: absolute; right: 12px; transition: transform .25s ease; }
  .gx-sd141 .od > button .c.up { transform: rotate(180deg); }
  .gx-sd141 .od .k { color: var(--mute); }
  .gx-sd141 .od .x { overflow: hidden; max-height: 0; transition: max-height .28s ease; }
  .gx-sd141 .od .x.on { max-height: 60px; }
  .gx-sd141 .od .x > div { padding: 0 12px 10px; text-align: center; color: var(--mute); }
  .gx-sd141 .gm .fp > div { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .gx-sd141 .gm .st { white-space: nowrap; width: 80px; }
  @media (max-width: 640px) {
    .gx-h2h .gx-sl98 { white-space: nowrap !important; overflow: hidden; text-overflow: ellipsis; }
    .gx-h2h > .gx-pc { min-height: 52px; }
    .gx-h2h > .gx-pc .gx-nm { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  }
</style>'''

ODDS = r'''    G132.ev[g.id] = g;'''
ODDS_NEW = r'''    try { /* gx146: betting line and TV */
      const od = (c.odds || [])[0] || {}, ml = (q) => { if (!q) return null; const v = q.moneyLine != null ? q.moneyLine : ((((q.current || {}).moneyLine) || {}).american); return v == null || v === "" ? null : +v; };
      g.ml = { a: ml(od.awayTeamOdds), h: ml(od.homeTeamOdds) }; g.ou = od.overUnder != null ? od.overUnder : null; g.sp = od.details || "";
      const b0 = (c.broadcasts || [])[0], gb = (c.geoBroadcasts || [])[0];
      g.tv = b0 && b0.names && b0.names.length ? b0.names.join("/") : gb && gb.media ? gb.media.shortName || "" : "";
    } catch (e) {}
    G132.ev[g.id] = g;'''

ROW_OLD = r'''              <button key={g.id} type="button" className="gm" onClick={() => openGame(g.id)}>
                <div className="tms">{rows2(g)}</div>
                <div className={"st" + (live(g) ? " lv" : "")}>{status(g)}</div>
                <div className="fp"><div><b>{abA}:</b> {f1(fpOf(tA, ta) + fpOf(tA, th))} FPTS</div><div><b>{abB}:</b> {f1(fpOf(tB, ta) + fpOf(tB, th))} FPTS</div></div>
              </button>'''
ROW_NEW = r'''              <React.Fragment key={g.id}>
              <button type="button" className="gm" onClick={() => openGame(g.id)}>
                <div className="tms">{rows2(g)}</div>
                {pre(g) ? (() => { const d = g.startTimeUTC ? new Date(g.startTimeUTC) : null; return <div className="st pg">{d ? (d.getMonth() + 1) + "/" + d.getDate() : ""}<b>{status(g)}</b><small>{g.tv || "\u00a0"}</small></div>; })() : <div className={"st" + (live(g) ? " lv" : "")}>{status(g)}</div>}
                {pre(g)
                  ? <div className="fp"><div><b>{abA}:</b> {nOf146(tA, ta, th)} Players</div><div><b>{abB}:</b> {nOf146(tB, ta, th)} Players</div></div>
                  : <div className="fp"><div><b>{abA}:</b> {f1(fpOf(tA, ta) + fpOf(tA, th))} FPTS</div><div><b>{abB}:</b> {f1(fpOf(tB, ta) + fpOf(tB, th))} FPTS</div></div>}
              </button>
              {pre(g) && g.ml && (g.ml.a != null || g.ou != null) ? (
                <div className="od">
                  <button type="button" onClick={() => setOx146((o) => ({ ...o, [g.id]: !o[g.id] }))}><span className="k">ML:</span> <b>{ta + " " + ml146(g.ml.a)}</b> <span className="k">@</span> <b>{th + " " + ml146(g.ml.h)}</b>{g.ou != null ? <><span className="k">{" \u00b7 Total:"}</span> <b>{g.ou}</b></> : null}<span className={"c" + (ox146[g.id] ? " up" : "")}>{"\u2304"}</span></button>
                  <div className={"x" + (ox146[g.id] ? " on" : "")}><div>{g.sp ? "Line: " + g.sp : "No puck line yet."}</div></div>
                </div>
              ) : null}
              </React.Fragment>'''


def change(t):
    t = lit(t, "146: styles", "</style>", NEW_CSS, "change 146 (install.py)")
    t = lit(t, "146: betting line and TV from ESPN", ODDS, ODDS_NEW, "gx146: betting line and TV")
    t = lit(t, "146: open line state",
            '  const [gi, setGi] = useState(null);',
            '  const [gi, setGi] = useState(null);\n  const [ox146, setOx146] = useState({});\n  const nOf146 = (day, x, y) => ((day && day.start) || []).filter((p) => p.t === x || p.t === y).length;\n  const ml146 = (v) => (v == null ? "-" : v > 0 ? "+" + v : String(v));',
            'const [ox146, setOx146] = useState({});')
    t = lit(t, "146: pregame rows", ROW_OLD, ROW_NEW, 'nOf146(tA, ta, th)} Players')
    return t


edit(APP, change)
