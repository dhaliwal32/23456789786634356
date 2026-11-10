# changes/254-box-tap-zoom.py - Roster box: no full screen button, double tap the box to grow it in place; stall logos no longer cut off on the phone

NEW_CSS = r'''  /* change 254 (install.py) */
  .gx-bx225 .hd .fs { display: none !important; }
  .gx-zm254 { position: relative; }
  .gx-zm254 .zx254 { display: none; }
  .gx-zm254.on { z-index: 62; background: var(--card); border: 1px solid var(--line2); border-radius: 16px; padding: 46px 10px 10px; box-shadow: 0 24px 60px rgba(0,0,0,.55); display: flex; flex-direction: column; overflow: hidden; }
  .gx-zm254.an { transition: top .32s cubic-bezier(.2,.8,.2,1), left .32s cubic-bezier(.2,.8,.2,1), width .32s cubic-bezier(.2,.8,.2,1), height .32s cubic-bezier(.2,.8,.2,1), padding .32s ease; }
  .gx-zm254.on .zx254 { display: flex; position: absolute; top: 8px; right: 8px; width: 32px; height: 32px; align-items: center; justify-content: center; border-radius: 999px; border: 1px solid var(--line2); background: var(--card2); color: var(--ink); font-size: 18px; line-height: 1; }
  .gx-zm254.on .zt254 { display: block; position: absolute; top: 15px; left: 14px; font-size: 12px; color: var(--mute); }
  .gx-zm254 .zt254 { display: none; }
  .gx-zm254.on .stg { flex: 1 1 auto; height: auto !important; aspect-ratio: auto !important; max-height: none !important; min-height: 0; }
  .gx-zm254.on .tb { flex: none; }
  .gx-zb254 { position: fixed; inset: 0; z-index: 61; background: rgba(0,0,0,.55); opacity: 0; transition: opacity .32s ease; }
  .gx-zb254.in { opacity: 1; }
  @media (prefers-reduced-motion: reduce) { .gx-zm254.an { transition: none; } .gx-zb254 { transition: none; } }
  @media (max-width: 640px) {
    .gx-fg224.gx-lt227.st246 { padding-top: 119% !important; }
    .gx-fg224.gx-lt227.st246 > .md.jr231 { height: 119cqw !important; }
  }
</style>'''

HELPERS = r'''// ---------- change 254: double tap the Roster box to grow it in place (install.py) ----------
// single taps inside the box wait a moment so a double tap can't open a player first; the side buttons are never delayed
function GxZm254({ children }) {
  const wrap = React.useRef(null), ph = React.useRef(null), last = React.useRef(null), pend = React.useRef(null), pass = React.useRef(false), pt = React.useRef(null);
  const [z, setZ] = useState(0); // 0 closed, 1 open, 2 closing
  const [bg, setBg] = useState(false);
  const box = () => wrap.current && wrap.current.getBoundingClientRect();
  const put = (el, r) => { el.style.top = r.top + "px"; el.style.left = r.left + "px"; el.style.width = r.width + "px"; el.style.height = r.height + "px"; };
  const target = (r0) => {
    const vw = window.innerWidth, vh = window.innerHeight;
    const w = Math.min(vw - 16, 760), h = Math.min(vh - 32, Math.max(r0.height + 60, vh * 0.86));
    return { left: (vw - w) / 2, top: Math.max(16, (vh - h) / 2), width: w, height: h };
  };
  const open = () => {
    const el = wrap.current; if (!el || z) return;
    const r = box();
    ph.current.style.height = r.height + "px";
    el.classList.add("on"); el.style.position = "fixed"; put(el, r);
    setZ(1); setBg(true);
    requestAnimationFrame(() => requestAnimationFrame(() => { el.classList.add("an"); put(el, target(r)); }));
  };
  const close = () => {
    const el = wrap.current; if (!el || z !== 1) return;
    setZ(2); setBg(false);
    const r = ph.current.getBoundingClientRect();
    el.classList.add("an"); el.style.padding = "0px"; put(el, { top: r.top, left: r.left, width: r.width, height: r.height });
    const done = () => {
      el.classList.remove("an", "on"); ["position", "top", "left", "width", "height", "padding"].forEach((k) => (el.style[k] = ""));
      ph.current.style.height = ""; setZ(0);
    };
    let fin = false; const f = () => { if (fin) return; fin = true; done(); };
    el.addEventListener("transitionend", function te(e) { if (e.target === el) { el.removeEventListener("transitionend", te); f(); } });
    setTimeout(f, 420);
  };
  useEffect(() => {
    if (z !== 1) return undefined;
    const kd = (e) => { if (e.key === "Escape") close(); };
    const rs = () => { const el = wrap.current; if (el) put(el, target(ph.current.getBoundingClientRect())); };
    window.addEventListener("keydown", kd); window.addEventListener("resize", rs);
    return () => { window.removeEventListener("keydown", kd); window.removeEventListener("resize", rs); };
  }, [z]);
  useEffect(() => () => clearTimeout(pend.current && pend.current.t), []);
  const dn = (e) => { pt.current = { x: e.clientX, y: e.clientY, t: Date.now() }; };
  const clickCap = (e) => {
    if (pass.current) { pass.current = false; return; }
    if (!e.detail) return; // keyboard
    if (e.target.closest && (e.target.closest(".tb") || e.target.closest(".zx254"))) return;
    const p = pt.current; if (p && (Math.abs(e.clientX - p.x) > 12 || Math.abs(e.clientY - p.y) > 12)) return;
    const now = Date.now(), l = last.current;
    e.stopPropagation(); e.preventDefault();
    if (l && now - l.t < 320 && Math.abs(e.clientX - l.x) < 40 && Math.abs(e.clientY - l.y) < 40) {
      last.current = null; if (pend.current) { clearTimeout(pend.current.t); pend.current = null; }
      if (z === 1) close(); else if (!z) open();
      return;
    }
    last.current = { t: now, x: e.clientX, y: e.clientY };
    const tg = e.target, cx = e.clientX, cy = e.clientY;
    if (pend.current) clearTimeout(pend.current.t);
    pend.current = { t: setTimeout(() => { pend.current = null; pass.current = true; try { tg.dispatchEvent(new MouseEvent("click", { bubbles: true, cancelable: true, clientX: cx, clientY: cy, view: window })); } catch (x) {} pass.current = false; }, 300) };
  };
  return (
    <div ref={ph} className="min-w-0" data-gx="254">
      {bg || z ? ReactDOM.createPortal(<div className={"gx-zb254 fixed inset-0" + (bg ? " in" : "")} onClick={close}></div>, document.body) : null}
      <div ref={wrap} className="gx-zm254" onPointerDownCapture={dn} onClickCapture={clickCap}>
        <span className="zt254">Tap twice to shrink</span>
        <button type="button" className="zx254" aria-label="Shrink the box" onClick={close}>{"\u00d7"}</button>
        {children}
      </div>
    </div>
  );
}
'''

OLD_COL = '''        <div className="min-w-0">
          {/* change 229: flat box again */}<div ref={stg} className="stg" data-gx="229" onPointerDown={pDown} onPointerMove={pMove} onPointerUp={pUp} onPointerCancel={pUp}>
            <div ref={pr} className="pr">{fToday}{fWin}<div className="fc gf252">'''
NEW_COL = '''        <GxZm254>
          {/* change 229: flat box again */}<div ref={stg} className="stg" data-gx="229" onPointerDown={pDown} onPointerMove={pMove} onPointerUp={pUp} onPointerCancel={pUp}>
            <div ref={pr} className="pr">{fToday}{fWin}<div className="fc gf252">'''
OLD_END = '''          <div className="tb">{NAMES.map((t, j) => <button key={t} type="button" className={k === j ? "on" : ""} onClick={() => turn(j)}>{t}</button>)}</div>
        </div>
      </div>
    </div>
  );
}
// ---------- change 231'''
NEW_END = '''          <div className="tb">{NAMES.map((t, j) => <button key={t} type="button" className={k === j ? "on" : ""} onClick={() => turn(j)}>{t}</button>)}</div>
        </GxZm254>{/* change 254 */}
      </div>
    </div>
  );
}
// ---------- change 231'''

def change(t):
    t = lit(t, "254: styles", "</style>", NEW_CSS, "change 254 (install.py)")
    t = lit(t, "254: helpers", ROOT, HELPERS + ROOT, "change 254: double tap the Roster box")
    t = lit(t, "254: wrap the box", OLD_COL, NEW_COL, "        <GxZm254>\n")
    t = lit(t, "254: end of wrap", OLD_END, NEW_END, "</GxZm254>{/* change 254 */}")
    return t

edit(APP, change)
