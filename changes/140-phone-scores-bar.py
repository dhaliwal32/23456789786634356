# changes/140-phone-scores-bar.py - phone Matchup: NHL Scores bar always at the bottom of the screen (score ticker on the right that changes game every few seconds), tap or swipe up to open the sheet; scoreboard as ESPN-style game cards (laptop keeps the bar at the end of the page)

NEW_CSS = r'''  /* change 140 (install.py) */
  .gx-fb140, .gx-sp140 { display: none; }
  @keyframes gx140-tk { from { opacity: 0; transform: translateY(6px); } }
  @media (max-width: 640px) {
    .gx-ns131.gx138 { display: none !important; }
    .gx-sp140 { display: block; height: 90px; }
    .gx-fb140 { display: block; position: fixed; left: 0; right: 0; bottom: 0; z-index: 60; background: var(--card); color: var(--ink); border-radius: 16px 16px 0 0; box-shadow: 0 -1px 0 var(--line), 0 -10px 28px rgba(0,0,0,.28); padding: 6px 16px calc(16px + env(safe-area-inset-bottom)); animation: gx139-up .28s cubic-bezier(.2, .8, .2, 1); -webkit-tap-highlight-color: transparent; }
    .gx-fb140 .grab { width: 40px; height: 5px; border-radius: 9px; background: var(--line2, var(--line)); margin: 0 auto; }
    .gx-fb140 .rw { display: flex; align-items: center; gap: 10px; margin-top: 12px; min-width: 0; }
    .gx-fb140 .rw svg { flex: none; }
    .gx-fb140 .rw > b { font-size: 18px; font-weight: 700; white-space: nowrap; }
    .gx-tk140 { margin-left: auto; min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; font-size: 14px; font-variant-numeric: tabular-nums; animation: gx140-tk .45s ease; }
    .gx-tk140 small { font-size: 14px; color: var(--mute); margin-left: 10px; }
    .gx-tk140 small.lv { color: var(--bad); }
    .gx-sh139 .gx-ns131.sh { height: 92vh; max-height: 92vh; }
  }
  .gx-gc140 { display: flex; flex-direction: column; gap: 10px; padding: 0 12px 8px; }
  .gx-gc140 .cd { display: flex; align-items: center; width: 100%; padding: 12px 14px; border-radius: 14px; background: var(--card2, var(--bg)); text-align: left; }
  .gx-gc140 .tms { flex: 1; min-width: 0; display: flex; flex-direction: column; gap: 8px; padding-right: 12px; border-right: 1px solid var(--line); }
  .gx-gc140 .tr { display: flex; align-items: center; gap: 10px; font-size: 17px; }
  .gx-gc140 .tr .nm { flex: 1; min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  .gx-gc140 .tr b { font-weight: 500; min-width: 20px; text-align: right; font-variant-numeric: tabular-nums; }
  .gx-gc140 .tr i { display: block; width: 7px; height: 10px; flex: none; }
  .gx-gc140 .tr i.ar { width: 0; height: 0; border-top: 5px solid transparent; border-bottom: 5px solid transparent; border-right: 7px solid var(--ink); }
  .gx-gc140 .tr.lo .nm, .gx-gc140 .tr.lo b { color: var(--mute); }
  .gx-gc140 .st { width: 96px; flex: none; padding-left: 14px; font-size: 14px; }
  .gx-gc140 .st.lv { color: var(--bad); font-weight: 600; }
  .gx-gc140 .st.pr { color: var(--mute); }
</style>'''

HELPERS = r'''// ---------- change 140: phone NHL Scores bar ticker (install.py) ----------
const GX_IC140 = <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><path d="M4 3l7.5 13.5" /><path d="M11.5 16.5H19a2 2 0 0 1 0 4H10a2 2 0 0 1-1.7-1L6 15.5" /><circle cx="18" cy="11" r="1.6" /></svg>;
function GxTick140({ games, live, fin, status }) {
  const [i, setI] = useState(0);
  useEffect(() => { if (games.length < 2) return undefined; const id = setInterval(() => setI((x) => x + 1), 4000); return () => clearInterval(id); }, [games.length]);
  if (!games.length) return <span className="gx-tk140"><small>No games today</small></span>;
  const g = games[i % games.length], A = g.awayTeam || {}, H = g.homeTeam || {}, pre = !(live(g) || fin(g));
  const a = gxAb131(A.abbrev), h = gxAb131(H.abbrev);
  return <span key={g.id + "-" + (i % games.length)} className="gx-tk140">{pre ? a + " - " + h : a + " " + (A.score != null ? A.score : 0) + " - " + h + " " + (H.score != null ? H.score : 0)}<small className={live(g) ? "lv" : ""}>{status(g)}</small></span>;
}
'''

SB_START = '    /* gx138: one-line scoreboard */'
SB_END = '  } else {\n    const all = [];'
SB_NEW = r'''    /* gx140: ESPN-style game cards */
    body = games.length ? <div className="gx-gc140">{games.map((g) => {
      const A = g.awayTeam || {}, H = g.homeTeam || {}, pre = !(live(g) || fin(g)), done = fin(g);
      const aw = !pre && +A.score > +H.score, hw = !pre && +H.score > +A.score;
      const row = (T, win, lose) => <div className={"tr" + (done && lose ? " lo" : "")}><TeamLogo t={gxAb131(T.abbrev)} size={24} /><span className="nm">{nick(T.abbrev)}</span><b>{pre || T.score == null ? "" : T.score}</b><i className={done && win ? "ar" : ""}></i></div>;
      return (
        <button key={g.id} type="button" className="cd" onClick={() => { setGid(g.id); setSide("fan"); }}>
          <div className="tms">{row(A, aw, hw)}{row(H, hw, aw)}</div>
          <div className={"st" + (live(g) ? " lv" : pre ? " pr" : "")}>{status(g)}</div>
        </button>
      );
    })}</div> : <div className="em">No NHL games today.</div>;
'''

FB = r'''  /* gx139: sheet */
  /* gx140: phone bar */
  const tsY140 = React.useRef(null);
  const fb140 = (
    <div className="gx-fb140" role="button" aria-label="Open NHL scores" onClick={toggle}
      onTouchStart={(e) => { tsY140.current = e.touches[0].clientY; }}
      onTouchEnd={(e) => { const y0 = tsY140.current; tsY140.current = null; if (y0 != null && e.changedTouches[0].clientY - y0 < -25) toggle(); }}>
      <div className="grab"></div>
      <div className="rw">{GX_IC140}<b>NHL Scores</b><GxTick140 games={games} live={live} fin={fin} status={status} /></div>
    </div>
  );'''


def change(t):
    t = lit(t, "140: styles", "</style>", NEW_CSS, "change 140 (install.py)")
    t = lit(t, "140: helpers", ROOT, HELPERS + ROOT, "change 140: phone NHL Scores bar ticker")
    if "gx140: ESPN-style game cards" not in t:
        if t.count(SB_START) != 1:
            fail("140: scoreboard start not found once")
        i = t.index(SB_START)
        j = t.find(SB_END, i)
        if j < 0:
            fail("140: scoreboard end not found")
        t = t[:i] + SB_NEW + t[j:]
        print("(install) 140: scoreboard cards: updated")
    t = lit(t, "140: bar code", "  /* gx139: sheet */", FB, "gx140: phone bar")
    t = lit(t, "140: bar on screen",
            '    <div className="gx-ns131 gx138">\n      <button type="button" className="bar" onClick={toggle}>',
            '    <>\n    {!open ? ReactDOM.createPortal(fb140, document.body) : null}<div className="gx-sp140"></div>\n    <div className="gx-ns131 gx138">\n      <button type="button" className="bar" onClick={toggle}>',
            '{!open ? ReactDOM.createPortal(fb140, document.body) : null}')
    t = lit(t, "140: close the fragment",
            '        </div>, document.body) : null}\n    </div>\n  );\n}',
            '        </div>, document.body) : null}\n    </div>\n    </>\n  );\n}',
            '    </div>\n    </>\n  );\n}')
    t = lit(t, "140: sheet title", '<div className="hd139"><span>NHL scores</span>', '<div className="hd139">{GX_IC140}<span>NHL Scores</span>', '<div className="hd139">{GX_IC140}')
    return t


edit(APP, change)
