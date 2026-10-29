# changes/144-smooth-drag.py - phone NHL Scores sheet: smooth dragging (moves once per screen frame on the graphics chip, page lock and backdrop fade only after you let go) and no second animation after it opens

NEW_CSS = r'''  /* change 144 (install.py) */
  .gx-sh141 .pn { will-change: transform; backface-visibility: hidden; }
  .gx-sh141.dg.out { animation: gx139-out .22s ease forwards !important; }
  .gx-sh141.dg.out .pn { animation: gx139-down .22s ease-in forwards !important; }
</style>'''

D_START = '  const [drag143, setDrag143] = useState(false);'
D_END = '  const pos142 ='
D_NEW = r'''  const [dm144, setDm144] = useState("");
  const drag143 = dm144 !== "", dragNow144 = dm144 === "drag";
  const pn143 = React.useRef(null), dz143 = React.useRef(null), sh143 = React.useRef(null), raf144 = React.useRef(0);
  const ease144 = "transform .3s cubic-bezier(.2, .8, .2, 1)";
  const bg144 = (on) => { const o = sh143.current; if (!o) return; o.style.transition = "background .3s ease"; o.style.background = on ? "rgba(0,0,0,.55)" : "rgba(0,0,0,0)"; };
  const setY143 = (y, anim) => {
    const p = pn143.current; if (!p) return;
    cancelAnimationFrame(raf144.current);
    const v = "translate3d(0," + Math.max(0, Math.round(y)) + "px,0)";
    if (anim) { p.style.transition = ease144; p.style.transform = v; return; }
    raf144.current = requestAnimationFrame(() => { p.style.transition = "none"; p.style.transform = v; });
  };
  const end143 = () => { setDm144(""); setOpen(false); setGid(null); };
  // drag the bar up: the sheet comes up under the finger
  const barDown143 = (e) => { dz143.current = { y: e.touches[0].clientY, dy: 0, on: false, up: true, H: 0 }; };
  const barMove143 = (e) => {
    const z = dz143.current; if (!z || !z.up) return;
    z.dy = z.y - e.touches[0].clientY;
    if (!z.on && z.dy > 6) { z.on = true; setGid(null); setDm144("drag"); setOpen(true); }
    if (z.on) { const p = pn143.current; if (p) { if (!z.H) z.H = p.offsetHeight || 600; setY143(z.H - z.dy, false); } }
  };
  const barUp143 = () => {
    const z = dz143.current; dz143.current = null;
    if (!z || !z.on) return;
    const p = pn143.current, H = z.H || (p && p.offsetHeight) || 600;
    if (z.dy > H * 0.18) { setY143(0, true); bg144(true); setTimeout(() => setDm144("held"), 310); }
    else { setY143(H, true); setTimeout(end143, 310); }
  };
  // drag the top of the sheet down: it follows, and goes away past a short distance
  const shDown143 = (e) => { if (e.target.closest && e.target.closest(".bd")) return; const p = pn143.current; dz143.current = { y: e.touches[0].clientY, dy: 0, on: true, up: false, H: (p && p.offsetHeight) || 600 }; };
  const shMove143 = (e) => { const z = dz143.current; if (!z || z.up) return; z.dy = e.touches[0].clientY - z.y; setY143(z.dy, false); };
  const shUp143 = () => {
    const z = dz143.current; dz143.current = null;
    if (!z || z.up) return;
    if (z.dy > 90) { setY143(z.H, true); bg144(false); setTimeout(end143, 310); } else setY143(0, true);
  };
'''

SLIDE_AFTER = '  const pos142 = gid ? 10 + ({ game: 0, fan: 1, awayTeam: 2, homeTeam: 3 }[gt] || 0) : tab === "sb" ? 0 : 1, sl142 = useSlide105(pos142);'
SLIDE_NEW = SLIDE_AFTER + r'''
  // slide only when the page changes while the sheet is open (not again when it opens)
  const pp144 = React.useRef({ open: false, pos: pos142, c: "" });
  if (!open) pp144.current = { open: false, pos: pos142, c: "" };
  else if (!pp144.current.open) pp144.current = { open: true, pos: pos142, c: "" };
  else if (pp144.current.pos !== pos142) pp144.current = { open: true, pos: pos142, c: pos142 > pp144.current.pos ? "r" : "l" };
  const slc144 = pp144.current.c;'''


def change(t):
    t = lit(t, "144: styles", "</style>", NEW_CSS, "change 144 (install.py)")
    if "const [dm144, setDm144]" not in t:
        if t.count(D_START) != 1:
            fail("144: drag code start not found once")
        i = t.index(D_START)
        j = t.find(D_END, i)
        if j < 0:
            fail("144: drag code end not found")
        t = t[:i] + D_NEW + t[j:]
        print("(install) 144: drag code: updated")
    t = lit(t, "144: slide only inside the sheet", SLIDE_AFTER + "\n", SLIDE_NEW + "\n", "const slc144 = pp144.current.c;")
    t = lit(t, "144: page class", 'className={"gx-sl105 " + sl142}', 'className={"gx-sl105 " + slc144}', 'className={"gx-sl105 " + slc144}')
    t = lit(t, "144: lock after letting go",
            '    if (!open) return undefined;\n    const k = (e) => { if (e.key === "Escape") close(); };\n    window.addEventListener("keydown", k);\n    gxLock141(true);\n    return () => { window.removeEventListener("keydown", k); gxLock141(false); };\n  }, [open]);',
            '    if (!open || dragNow144) return undefined;\n    const k = (e) => { if (e.key === "Escape") close(); };\n    window.addEventListener("keydown", k);\n    gxLock141(true);\n    return () => { window.removeEventListener("keydown", k); gxLock141(false); };\n  }, [open, dragNow144]);',
            '  }, [open, dragNow144]);')
    t = lit(t, "144: backdrop starts clear only while dragging",
            'style={drag143 ? { background: "rgba(0,0,0,0)" } : null} onClick={close}',
            'style={dragNow144 ? { background: "rgba(0,0,0,0)" } : null} onClick={close}',
            'style={dragNow144 ? { background: "rgba(0,0,0,0)" } : null}')
    t = lit(t, "144: sheet starts low only while dragging",
            'style={drag143 ? { transform: "translateY(100%)" } : null}',
            'style={dragNow144 ? { transform: "translate3d(0,100%,0)" } : null}',
            'style={dragNow144 ? { transform: "translate3d(0,100%,0)" } : null}')
    t = lit(t, "144: bar only while dragging",
            '      {!open || drag143 ? ReactDOM.createPortal(fb, document.body) : null}',
            '      {!open || dragNow144 ? ReactDOM.createPortal(fb, document.body) : null}',
            '{!open || dragNow144 ? ReactDOM.createPortal(fb')
    t = lit(t, "144: closing resets the drag state",
            '  const close = () => { setOut(true); setTimeout(() => { setOut(false); setOpen(false); setGid(null); }, 220); };\n  useEffect(() => {\n    if (!open || dragNow144)',
            '  const close = () => { setOut(true); setTimeout(() => { setOut(false); setOpen(false); setGid(null); setDm144(""); }, 220); };\n  useEffect(() => {\n    if (!open || dragNow144)',
            'setGid(null); setDm144(""); }, 220); };')
    return t


edit(APP, change)
