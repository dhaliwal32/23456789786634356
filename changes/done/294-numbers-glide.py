# changes/294-numbers-glide.py - any number that changes by itself (scores, points, win chance, stats) now counts smoothly from the old value to the new one instead of jumping

HELPERS = r'''// ---------- change 294: numbers that change by themselves count smoothly to the new value (install.py) ----------
// Watches every piece of text on the page. When a number is replaced by another number of the same kind
// (same sign, same unit) and nobody just tapped anything, it counts from the old value to the new one.
// Left alone: clocks, anything already animating itself (changing many times a second), and big redraws.
(function gxNum294() {
  if (window.__gxNum294 || !window.MutationObserver) return;
  window.__gxNum294 = 1;
  const RX = /^([^\d:]{0,4})(\d{1,6}(?:\.\d{1,2})?)([^\d:]{0,6})$/;
  const mine = new WeakMap(), seen = new WeakMap(), run = new WeakMap(), own = new WeakSet();
  let lastIn = 0;
  ["pointerdown", "keydown", "change", "input"].forEach((k) => window.addEventListener(k, () => { lastIn = performance.now(); }, true));
  const still = () => { try { return window.matchMedia("(prefers-reduced-motion: reduce)").matches; } catch (e) { return false; } };
  const stop = (node) => { const r = run.get(node); if (r) { cancelAnimationFrame(r.raf); run.delete(node); } };
  const glide = (node, a, b) => {
    const x0 = +a[2], x1 = +b[2], dec = (b[2].split(".")[1] || "").length, end = b[1] + b[2] + b[3], t0 = performance.now(), dur = 550;
    stop(node);
    const r = { raf: 0 };
    const put = (txt) => { mine.set(node, txt); node.nodeValue = txt; };
    const step = (t) => {
      if (!node.isConnected) { run.delete(node); return; }
      const k = Math.min(1, (t - t0) / dur), e = 1 - Math.pow(1 - k, 3);
      if (k >= 1) { put(end); run.delete(node); return; }
      put(b[1] + (x0 + (x1 - x0) * e).toFixed(dec) + b[3]);
      r.raf = requestAnimationFrame(step);
    };
    run.set(node, r);
    put(a[1] + a[2] + a[3]);
    r.raf = requestAnimationFrame(step);
  };
  const seeAll = (muts) => {
    const now = performance.now(), last = new Map();
    muts.forEach((m) => { if (m.type === "characterData" && !last.has(m.target)) last.set(m.target, m.oldValue); });
    const todo = [];
    last.forEach((old, node) => {
      const cur = node.nodeValue;
      if (mine.get(node) === cur) return; // my own step
      const before = seen.get(node) || 0;
      seen.set(node, now);
      if (now - before < 200) { own.add(node); stop(node); return; } // it animates itself, leave it alone
      if (own.has(node)) return;
      todo.push([node, old, cur]);
    });
    if (!todo.length || now - lastIn < 700 || document.hidden || todo.length > 80 || still()) { todo.forEach((x) => stop(x[0])); return; }
    todo.forEach(([node, old, cur]) => {
      const a = RX.exec(String(old == null ? "" : old)), b = RX.exec(String(cur));
      if (!a || !b || a[1] !== b[1] || a[3] !== b[3] || +a[2] === +b[2]) { stop(node); return; }
      const el = node.parentElement;
      if (!el || !el.getClientRects().length) return;
      glide(node, a, b);
    });
  };
  const start = () => new MutationObserver(seeAll).observe(document.body, { characterData: true, characterDataOldValue: true, subtree: true });
  if (document.body) start(); else document.addEventListener("DOMContentLoaded", start);
})();
'''


def change(t):
    t = lit(t, "294: helpers", ROOT, HELPERS + ROOT, "change 294: numbers that change by themselves")
    return t

edit(APP, change)
