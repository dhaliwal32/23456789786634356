# changes/232-box-names-fit.py - Roster box: long team names shrink to fit on one line, both names the same size

NEW_CSS = r'''  /* change 232 (install.py): team names shrink to fit */
  .gx-bx226 .ft232 { display: block; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; min-width: 0; }
  .gx-bx226 .tot:has(.ft232) { flex-wrap: wrap; }
  .gx-bx226 .tot .ft232 { flex: 1 0 100%; line-height: 16px; height: 16px; }
  .gx-bx226 .tot b { flex: 0 0 auto; white-space: nowrap; }
</style>'''

HELPERS = r'''// ---------- change 232: team names shrink to fit, same size on both sides (install.py) ----------
function gxFit232(el) {
  if (!el || el.__ft232) return;
  el.__ft232 = 1;
  let raf = 0;
  const run = () => {
    raf = 0;
    const L = el.querySelectorAll(".ft232");
    if (!L.length) return;
    let k = 1;
    L.forEach((n) => { n.style.fontSize = (+n.dataset.fx) + "px"; });
    L.forEach((n) => { const cw = n.clientWidth, sw = n.scrollWidth; if (cw > 0 && sw > cw + 0.5) k = Math.min(k, cw / sw); });
    L.forEach((n) => { n.style.fontSize = Math.max(8, (k < 1 ? Math.floor(+n.dataset.fx * k * 0.97 * 10) / 10 : +n.dataset.fx)) + "px"; });
  };
  const go = () => { if (!raf) raf = requestAnimationFrame(run); };
  run();
  try { new ResizeObserver(go).observe(el); } catch (e) {}
  try { new MutationObserver(go).observe(el, { subtree: true, characterData: true, childList: true }); } catch (e) {}
}
'''

def change(t):
    t = lit(t, "232: styles", "</style>", NEW_CSS, "change 232 (install.py)")
    t = lit(t, "232: helpers", ROOT, HELPERS + ROOT, "change 232: team names shrink")
    if "ft232\" data-fx" in t:
        return t
    a = t.find("function GxBox230(")
    if a < 0:
        fail("232: GxBox230 not found")
    b = t.find("\nfunction ", a + 10)
    seg = t[a:b]
    reps = [
        ('<div className="row2">', '<div className="row2" ref={gxFit232}>', 1),
        ('<div className="sc">', '<div className="sc" ref={gxFit232}>', 1),
        ('<div className="text-sm font-semibold truncate">{mineMu ? teamName(s, s.me) : nmA}</div>',
         '<div className="text-sm font-semibold ft232" data-fx="14">{mineMu ? teamName(s, s.me) : nmA}</div>', 1),
        ('<div className="text-sm font-semibold truncate">{nmA}</div>',
         '<div className="text-sm font-semibold ft232" data-fx="14">{nmA}</div>', 1),
        ('<div className="text-sm text-slate-500 truncate">{nmB}</div>',
         '<div className="text-sm text-slate-500 ft232" data-fx="14">{nmB}</div>', 2),
        ('<div className="tdc">', '<div className="tdc" ref={gxFit232}>', 1),
        ('<span className={dim ? "text-slate-500" : "font-semibold"}>{nm}</span>',
         '<span className={"ft232" + (dim ? " text-slate-500" : " font-semibold")} data-fx="12">{nm}</span>', 1),
    ]
    for old, new, n in reps:
        if seg.count(old) != n:
            fail("232: expected %d in GxBox230: %s" % (n, old[:50]))
        seg = seg.replace(old, new)
    return t[:a] + seg + t[b:]

edit(APP, change)
