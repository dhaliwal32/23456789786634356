# changes/143-drag-sheet.py - phone: the NHL Scores sheet follows your finger (drag the bar up to pull it open, drag the top of the sheet down to put it away); smaller, cleaner bottom bar; no date arrows on Matchup (swipe the day box instead)

NEW_CSS = r'''  /* change 143 (install.py) */
  .gx-fb140 { touch-action: none; }
  .gx-sh141.dg, .gx-sh141.dg .pn { animation: none !important; }
  .gx-sh141 .grab, .gx-sh141 .hd, .gx-sh141 .seg2, .gx-sh141 .gx-gv141, .gx-sh141 .gx-tb141 { touch-action: none; }
  @media (max-width: 640px) {
    .gx-sp140 { height: 72px; }
    .gx-fb140 { padding: 6px 18px calc(12px + env(safe-area-inset-bottom)); }
    .gx-fb140 .grab { width: 34px; height: 4px; }
    .gx-fb140 .rw { margin-top: 9px; gap: 8px; }
    .gx-fb140 .rw svg { width: 17px; height: 17px; }
    .gx-fb140 .rw > b { font-size: 15px; font-weight: 600; }
    .gx-tk140 { font-size: 13px; color: var(--ink); }
    .gx-tk140 small { font-size: 12px; margin-left: 8px; }
    .gx-dn108 .gx-arw { display: none !important; }
  }
</style>'''

STATE = r'''  const [drag143, setDrag143] = useState(false);
  const pn143 = React.useRef(null), dz143 = React.useRef(null), sh143 = React.useRef(null);
  const ease143 = "transform .26s cubic-bezier(.2, .8, .2, 1)";
  const setY143 = (y, anim) => { const p = pn143.current; if (!p) return; p.style.transition = anim ? ease143 : "none"; p.style.transform = "translateY(" + Math.max(0, y) + "px)"; const o = sh143.current; if (o) { const H = p.offsetHeight || 1; o.style.transition = anim ? "background .26s ease" : "none"; o.style.background = "rgba(0,0,0," + (0.55 * Math.max(0, Math.min(1, 1 - y / H))).toFixed(3) + ")"; } };
  const end143 = () => { setDrag143(false); setOpen(false); setGid(null); };
  // drag the bar up: the sheet comes up under the finger
  const barDown143 = (e) => { dz143.current = { y: e.touches[0].clientY, dy: 0, on: false, up: true }; };
  const barMove143 = (e) => {
    const z = dz143.current; if (!z || !z.up) return;
    z.dy = z.y - e.touches[0].clientY;
    if (!z.on && z.dy > 6) { z.on = true; setGid(null); setDrag143(true); setOpen(true); }
    if (z.on) { const p = pn143.current; if (p) setY143((p.offsetHeight || 600) - z.dy, false); }
  };
  const barUp143 = () => {
    const z = dz143.current; dz143.current = null;
    if (!z || !z.on) return;
    const p = pn143.current, H = (p && p.offsetHeight) || 600;
    if (z.dy > H * 0.18) { setY143(0, true); setTimeout(() => setDrag143(false), 270); }
    else { setY143(H, true); setTimeout(end143, 260); }
  };
  // drag the top of the sheet down: it follows, and goes away past a short distance
  const shDown143 = (e) => { if (e.target.closest && e.target.closest(".bd")) return; dz143.current = { y: e.touches[0].clientY, dy: 0, on: true, up: false }; };
  const shMove143 = (e) => { const z = dz143.current; if (!z || z.up) return; z.dy = e.touches[0].clientY - z.y; setY143(z.dy, false); };
  const shUp143 = () => {
    const z = dz143.current; dz143.current = null;
    if (!z || z.up) return;
    const p = pn143.current, H = (p && p.offsetHeight) || 600;
    if (z.dy > 90) { setY143(H, true); setTimeout(end143, 260); } else setY143(0, true);
  };'''

OLD_HD = ' onTouchStart={(e) => { dragY.current = e.touches[0].clientY; }} onTouchEnd={(e) => { const y0 = dragY.current; dragY.current = null; if (y0 != null && e.changedTouches[0].clientY - y0 > 70) close(); }}'


def change(t):
    t = lit(t, "143: styles", "</style>", NEW_CSS, "change 143 (install.py)")
    t = lit(t, "143: drag state", "  const dragY = React.useRef(null);\n", "  const dragY = React.useRef(null);\n" + STATE + "\n", "const [drag143, setDrag143]")
    if OLD_HD in t:
        if t.count(OLD_HD) != 2:
            fail("143: old header swipe found " + str(t.count(OLD_HD)) + " times")
        t = t.replace(OLD_HD, "")
        print("(install) 143: old header swipe removed")
    t = lit(t, "143: bar drags",
            '<div className="gx-fb140" role="button" aria-label="Open NHL scores" onClick={() => { setGid(null); setOpen(true); }}>',
            '<div className="gx-fb140" role="button" aria-label="Open NHL scores" onClick={() => { if (!drag143) { setGid(null); setOpen(true); } }} onTouchStart={barDown143} onTouchMove={barMove143} onTouchEnd={barUp143} onTouchCancel={barUp143}>',
            'onTouchStart={barDown143}')
    t = lit(t, "143: bar stays while dragging",
            '      {!open ? ReactDOM.createPortal(fb, document.body) : null}',
            '      {!open || drag143 ? ReactDOM.createPortal(fb, document.body) : null}',
            '{!open || drag143 ? ReactDOM.createPortal(fb')
    t = lit(t, "143: sheet backdrop",
            '      <div className={"gx-sh141" + (out ? " out" : "")} onClick={close} role="dialog" aria-label="NHL scores">',
            '      <div ref={sh143} className={"gx-sh141" + (out ? " out" : "") + (drag143 ? " dg" : "")} style={drag143 ? { background: "rgba(0,0,0,0)" } : null} onClick={close} role="dialog" aria-label="NHL scores">',
            'ref={sh143} className={"gx-sh141"')
    t = lit(t, "143: sheet follows the finger",
            '        <div className="pn" onClick={(e) => e.stopPropagation()}>',
            '        <div className="pn" ref={pn143} style={drag143 ? { transform: "translateY(100%)" } : null} onClick={(e) => e.stopPropagation()} onTouchStart={shDown143} onTouchMove={shMove143} onTouchEnd={shUp143} onTouchCancel={shUp143}>',
            'ref={pn143}')
    return t


edit(APP, change)
