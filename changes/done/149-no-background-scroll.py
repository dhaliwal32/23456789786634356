# changes/149-no-background-scroll.py - whenever anything opens on top (player screen, box score, NHL scores, simulate, search, any pop-up), the page behind it stays completely still; only the page you opened scrolls

NEW_CSS = r'''  /* change 149 (install.py) */
  .gx-so, .gx-pd-ov, .gx-so107, .gx-bm119, .gx-sh139, .gx-sh141, .fixed.inset-0, .gx-pd, .gx-pd-bd, .gx-sh141 .bd { overscroll-behavior: contain; }
</style>'''

HELPER = r'''// ---------- change 149: the page behind any pop-up never scrolls (install.py) ----------
(function () {
  if (window.__GX149) return;
  window.__GX149 = 1;
  const SEL = ".gx-so, .gx-pd-ov, .gx-so107, .gx-bm119, .gx-sh139, .gx-sh141:not(.gx-nl149), .fixed.inset-0, .gx-pd";
  let locked = false, y = 0, q = 0;
  const set = (on) => {
    if (on === locked) return;
    locked = on;
    const b = document.body;
    if (on) { y = window.scrollY || 0; b.style.position = "fixed"; b.style.top = -y + "px"; b.style.left = "0"; b.style.right = "0"; b.style.width = "100%"; b.style.overflow = "hidden"; }
    else { b.style.position = ""; b.style.top = ""; b.style.left = ""; b.style.right = ""; b.style.width = ""; b.style.overflow = ""; window.scrollTo(0, y); }
  };
  const check = () => { q = 0; let on = false; document.querySelectorAll(SEL).forEach((el) => { if (!on && getComputedStyle(el).display !== "none") on = true; }); set(on); };
  const soon = () => { if (!q) q = requestAnimationFrame(check); };
  const start = () => { new MutationObserver(soon).observe(document.body, { childList: true, subtree: true, attributes: true, attributeFilter: ["class"] }); check(); };
  if (document.body) start(); else document.addEventListener("DOMContentLoaded", start);
})();
'''


def change(t):
    t = lit(t, "149: styles", "</style>", NEW_CSS, "change 149 (install.py)")
    t = lit(t, "149: one page-wide lock", ROOT, HELPER + ROOT, "change 149: the page behind any pop-up never scrolls")
    t = lit(t, "149: old sheet lock handed over", "function gxLock141(on) {", "function gxLock141(on) { return; /* gx149: the page-wide lock does this now */", "gx149: the page-wide lock does this now")
    t = lit(t, "149: no lock while dragging the sheet up",
            '(drag143 ? " dg" : "") + (a !== s.me ? " gx-nc148" : "")}',
            '(drag143 ? " dg" : "") + (a !== s.me ? " gx-nc148" : "") + (dragNow144 ? " gx-nl149" : "")}',
            '(dragNow144 ? " gx-nl149" : "")}')
    return t


edit(APP, change)
