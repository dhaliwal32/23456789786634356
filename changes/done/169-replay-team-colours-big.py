# changes/169-replay-team-colours-big.py - goal replay circles in each team's own colour (the other team goes white with its colour as the ring when the two colours look alike), and on the laptop the Goal Visualizer opens big in the middle of the screen

HELP = r'''// ---------- change 169: team colours for the replay, big replay window on the laptop (install.py) ----------
function gxHex169(h) { const m = String(h || "").replace("#", ""); return [parseInt(m.slice(0, 2), 16) || 0, parseInt(m.slice(2, 4), 16) || 0, parseInt(m.slice(4, 6), 16) || 0]; }
function gxLum169(h) { const c = gxHex169(h); return (0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2]) / 255; }
function gxPair169(a, b) {
  const ca = gxTC101(a), cb = gxTC101(b), x = gxHex169(ca), y = gxHex169(cb);
  const dist = Math.sqrt((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2 + (x[2] - y[2]) ** 2);
  const solid = (c) => ({ f: c, t: gxLum169(c) > 0.55 ? "#111111" : "#ffffff", s: gxLum169(c) > 0.55 ? "#111111" : "#ffffff" });
  const ring = (c) => ({ f: "#ffffff", t: gxLum169(c) > 0.75 ? "#111111" : c, s: gxLum169(c) > 0.75 ? "#111111" : c });
  return { sc: solid(ca), ot: dist < 130 ? ring(cb) : solid(cb) };
}
const gxCol169 = (c, txt) => (txt ? { fill: c.t, fontWeight: 700 } : { fill: c.f, stroke: c.s, strokeWidth: c.f === "#ffffff" ? 0.9 : 0.5 });
function GxGvModal169({ title, onClose, children }) {
  useEffect(() => { const k = (e) => { if (e.key === "Escape") onClose(); }; window.addEventListener("keydown", k); return () => window.removeEventListener("keydown", k); }, []);
  return ReactDOM.createPortal(
    <div className="fixed inset-0 gx-gv169" onClick={onClose} role="dialog" aria-label="Goal Visualizer">
      <div className="bx" onClick={(e) => e.stopPropagation()}>
        <div className="hd"><span>{title}</span><button type="button" className="xx" aria-label="Close" onClick={onClose}>{"×"}</button></div>
        {children}
      </div>
    </div>, document.body);
}
'''

NEW_CSS = r'''  /* change 169 (install.py) */
  .gx-gv169 { z-index: 70; background: rgba(0,0,0,.6); display: flex; align-items: center; justify-content: center; padding: 24px; animation: gx101-fade .18s ease-out; }
  .gx-gv169 .bx { width: min(980px, 100%); max-height: calc(100vh - 48px); overflow-y: auto; overscroll-behavior: contain; background: var(--card); border-radius: 16px; box-shadow: 0 20px 60px rgba(0,0,0,.45); padding: 18px 22px 22px; animation: gx101-pop .22s cubic-bezier(.2,.8,.2,1); }
  .gx-gv169 .hd { display: flex; align-items: center; gap: 12px; font-size: 18px; font-weight: 600; margin-bottom: 8px; }
  .gx-gv169 .hd .xx { margin-left: auto; font-size: 28px; line-height: 1; color: var(--mute); width: 36px; height: 36px; border-radius: 99px; }
  .gx-gv169 .hd .xx:hover { background: var(--card2, var(--bg)); color: var(--ink); }
  .gx-gv169 .gx-rk163 { margin-top: 4px; }
  .gx-gv169 .gx-rk163 .tl b { font-size: 17px; }
  .gx-gv169 .gx-rk163 .tl small { font-size: 12px; }
  .gx-gv169 .gx-ed165 .ct button { font-size: 14px; padding: 7px 14px; }
  .gx-gv169 .gx-ed165 .ol { font-size: 14px; }
</style>'''


def app(t):
    t = lit(t, "169: styles", "</style>", NEW_CSS, "change 169 (install.py)")
    t = lit(t, "169: helpers", ROOT, HELP + ROOT, "change 169: team colours for the replay")
    t = lit(t, "169: colours ready",
            '  const teams = [scT].concat([...new Set(gRow.map((o) => o[1]))].filter((t) => t !== scT));\n  return (\n    <div className="gx-ed165" data-gx="168">',
            '  const teams = [scT].concat([...new Set(gRow.map((o) => o[1]))].filter((t) => t !== scT));\n  const C169 = gxPair169(scT, teams[1] || ""); /* gx169 */\n  return (\n    <div className="gx-ed165" data-gx="168">',
            "const C169 = gxPair169(scT")
    t = lit(t, "169: circle colours",
            '<circle cx={o[3]} cy={o[4]} r="3.7" className={o[1] === scT ? "sc" : "ot"} />',
            '<circle cx={o[3]} cy={o[4]} r="3.7" className="t169" style={gxCol169(o[1] === scT ? C169.sc : C169.ot, 0)} />',
            'className="t169" style={gxCol169(o[1] === scT ? C169.sc : C169.ot, 0)}')
    t = lit(t, "169: number colours",
            'className={o[1] === scT ? "sc" : "ot"}>{o[2]}</text>',
            'className="t169" style={gxCol169(o[1] === scT ? C169.sc : C169.ot, 1)}>{o[2]}</text>',
            'style={gxCol169(o[1] === scT ? C169.sc : C169.ot, 1)}>')
    t = lit(t, "169: key colours",
            '<span className="lg"><i className="sc"></i>{scT}<i className="ot"></i>{teams[1] || ""}</span>',
            '<span className="lg"><i style={{ background: C169.sc.f, boxShadow: "inset 0 0 0 1.5px " + C169.sc.s }}></i>{scT}<i style={{ background: C169.ot.f, boxShadow: "inset 0 0 0 1.5px " + C169.ot.s }}></i>{teams[1] || ""}</span>',
            'background: C169.sc.f')
    t = lit(t, "169: laptop opens big",
            '{on ? <GxRink163 x={r.x} g={r.g} tm={r.tm} s={s} /> : null}</>; })() : null}',
            '{on ? <GxGvModal169 title={shortN(r.n) + " \\u00b7 " + r.tm + " \\u00b7 " + (r.x.timeInPeriod || "") + " " + gxPer131(r.x.periodDescriptor)} onClose={() => setGv163((o) => ({ ...o, [k167]: false }))}><GxRink163 x={r.x} g={r.g} tm={r.tm} s={s} /></GxGvModal169> : null}</>; })() : null}',
            "<GxGvModal169 title=")
    return t


edit(APP, app)
