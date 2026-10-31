# changes/163-goal-visualizer.py - Goal visualizer: a rink showing where each goal was shot from (ESPN's live shot location), with Score / Time / Shot tiles, in the laptop Goal Tracker and under each goal card on the phone ("Goal Visualizer" button)

NEW_CSS = r'''  /* change 163 (install.py) */
  .gx-rk163 { margin-top: 10px; }
  .gx-rk163 svg { display: block; width: 100%; height: auto; }
  .gx-rk163 .tl { display: grid; grid-template-columns: repeat(3, minmax(0,1fr)); gap: 6px; margin-top: 8px; }
  .gx-rk163 .tl > div { background: var(--card2, var(--bg)); border-radius: 8px; padding: 6px 4px; text-align: center; min-width: 0; }
  .gx-rk163 .tl b { display: block; font-size: 14px; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .gx-rk163 .tl small { display: block; font-size: 11px; color: var(--mute); }
  .gx-gt141 .gv163 { display: flex; align-items: center; justify-content: center; gap: 6px; width: 100%; padding: 10px; border-top: 1px solid var(--line); color: var(--accent); font-size: 14px; font-weight: 600; }
  .gx-gt141 .gv163 i { display: inline-block; transition: transform .25s ease; font-style: normal; }
  .gx-gt141 .gv163 i.up { transform: rotate(180deg); }
  .gx-gt141 .gvb163 { padding: 0 12px 12px; }
</style>'''

HELPERS = r'''// ---------- change 163: goal visualizer (install.py) ----------
// rink in feet: x -100..100 (nets at +/-89), y -42.5..42.5; ESPN gives the shot spot as coordinate {x, y}
function GxRink163({ x, g, tm }) {
  const cx = +x.cx, cy = +x.cy;
  if (isNaN(cx) || isNaN(cy)) return null;
  const side = cx >= 0 ? 1 : -1, nx = side * 89;
  const A = gxAb131((g.awayTeam || {}).abbrev), H = gxAb131((g.homeTeam || {}).abbrev), as = +x.awayScore, hs = +x.homeScore;
  const score = isNaN(as) || isNaN(hs) ? "" : as === hs ? as + "-" + hs + " Tied" : Math.max(as, hs) + "-" + Math.min(as, hs) + " " + (as > hs ? A : H);
  const red = "#d64545", blue = "#3d73d9", ln = "var(--line2, var(--line))";
  const circ = (px, py, k) => <circle key={k} cx={px} cy={py} r="15" fill="none" stroke={red} strokeWidth="0.6" opacity=".7" />;
  const dot = (px, py, k) => <circle key={k} cx={px} cy={py} r="0.9" fill={red} opacity=".8" />;
  return (
    <div className="gx-rk163" data-gx="163">
      <svg viewBox="-102 -45 204 90" role="img" aria-label={"Goal by " + (x.name && x.name.default ? x.name.default : "") + " from the spot shown"}>
        <rect x="-100" y="-42.5" width="200" height="85" rx="28" fill="var(--card2, var(--bg))" stroke={ln} strokeWidth="1" />
        <line x1="0" y1="-42.5" x2="0" y2="42.5" stroke={red} strokeWidth="1" strokeDasharray="2 1.5" />
        <line x1="-25" y1="-42.5" x2="-25" y2="42.5" stroke={blue} strokeWidth="1.2" />
        <line x1="25" y1="-42.5" x2="25" y2="42.5" stroke={blue} strokeWidth="1.2" />
        <line x1="-89" y1="-38.5" x2="-89" y2="38.5" stroke={red} strokeWidth="0.5" />
        <line x1="89" y1="-38.5" x2="89" y2="38.5" stroke={red} strokeWidth="0.5" />
        <circle cx="0" cy="0" r="15" fill="none" stroke={blue} strokeWidth="0.6" opacity=".7" />
        {[[-69, -22], [-69, 22], [69, -22], [69, 22]].map(([a, b], i) => circ(a, b, "c" + i))}
        {[[-69, -22], [-69, 22], [69, -22], [69, 22], [-20, -22], [-20, 22], [20, -22], [20, 22]].map(([a, b], i) => dot(a, b, "d" + i))}
        <path d="M -89 -4 A 6 6 0 0 0 -83 0 A 6 6 0 0 0 -89 4 Z" fill="rgba(61,115,217,.18)" stroke={red} strokeWidth="0.5" />
        <path d="M 89 -4 A 6 6 0 0 1 83 0 A 6 6 0 0 1 89 4 Z" fill="rgba(61,115,217,.18)" stroke={red} strokeWidth="0.5" />
        <rect x="-92.3" y="-3" width="3.3" height="6" fill="none" stroke={red} strokeWidth="0.6" />
        <rect x="89" y="-3" width="3.3" height="6" fill="none" stroke={red} strokeWidth="0.6" />
        <line x1={cx} y1={-cy} x2={nx} y2="0" stroke="var(--ink)" strokeWidth="0.7" strokeDasharray="1.6 1.2" opacity=".8" />
        <circle cx={cx} cy={-cy} r="3.4" fill="var(--accent)" stroke="var(--ink)" strokeWidth="0.7" />
        <text x={side > 0 ? -60 : 60} y="2.5" textAnchor="middle" fontSize="7" fill="var(--mute)" fontWeight="600">{tm}</text>
      </svg>
      <div className="tl">
        <div><b>{score || "-"}</b><small>Score</small></div>
        <div><b>{(x.timeInPeriod || "") + " " + gxPer131(x.periodDescriptor)}</b><small>Time</small></div>
        <div><b>{x.shot ? String(x.shot).replace(/\s*Shot$/i, "") : "-"}</b><small>Shot</small></div>
      </div>
    </div>
  );
}
'''

def change(t):
    t = lit(t, "163: styles", "</style>", NEW_CSS, "change 163 (install.py)")
    t = lit(t, "163: helpers", ROOT, HELPERS + ROOT, "change 163: goal visualizer")
    t = lit(t, "163: shot spot from ESPN",
            'strength: st.indexOf("power") >= 0 ? "PP" : st.indexOf("short") >= 0 ? "SH" : "",',
            'strength: st.indexOf("power") >= 0 ? "PP" : st.indexOf("short") >= 0 ? "SH" : "", cx: e.coordinate ? e.coordinate.x : null, cy: e.coordinate ? e.coordinate.y : null, shot: ((String(e.text || "").match(/Goal \\(\\d+\\)\\s*([^,]+)/) || [])[1] || "").trim(), /* gx163 */',
            "cx: e.coordinate ? e.coordinate.x : null")
    t = lit(t, "163: open state",
            "useTick159(gxAnyInt159()); /* gx159 */",
            "useTick159(gxAnyInt159()); /* gx159 */\n  const [gv163, setGv163] = useState({});",
            "const [gv163, setGv163] = useState({});")
    t = lit(t, "163: laptop rink",
            '<div className="asl">Assists: {r.as.length ? r.as.map((q, k) => <React.Fragment key={k}>{k ? ", " : ""}{pBtn(q.ap, shortN(q.an), "a")}{q.at ? " (" + q.at + ")" : ""}</React.Fragment>) : "Unassisted"}</div>',
            '<div className="asl">Assists: {r.as.length ? r.as.map((q, k) => <React.Fragment key={k}>{k ? ", " : ""}{pBtn(q.ap, shortN(q.an), "a")}{q.at ? " (" + q.at + ")" : ""}</React.Fragment>) : "Unassisted"}</div>{r.x.cx != null ? <GxRink163 x={r.x} g={r.g} tm={r.tm} /> : null}',
            "<GxRink163 x={r.x} g={r.g} tm={r.tm} /> : null}")
    t = lit(t, "163: phone button and rink",
            '<div className="as"><span>Assists:</span><div className="ls">{r.as.length ? r.as.map((q, k) => <div key={k}>{pBtn(q.ap, q.an, "a")}{q.at ? " (" + q.at + ")" : ""}</div>) : <div>Unassisted</div>}</div></div>',
            '<div className="as"><span>Assists:</span><div className="ls">{r.as.length ? r.as.map((q, k) => <div key={k}>{pBtn(q.ap, q.an, "a")}{q.at ? " (" + q.at + ")" : ""}</div>) : <div>Unassisted</div>}</div></div>'
            '{r.x.cx != null ? (() => { const k163 = r.g.id + "-" + r.i, on = !!gv163[k163]; return <><button type="button" className="gv163" onClick={(e) => { e.stopPropagation(); setGv163((o) => ({ ...o, [k163]: !on })); }}>Goal Visualizer <i className={on ? "up" : ""}>{"\\u25be"}</i></button>{on ? <div className="gvb163"><GxRink163 x={r.x} g={r.g} tm={r.tm} /></div> : null}</>; })() : null}',
            'className="gv163"')
    return t

edit(APP, change)
