# changes/102-speed.py - smoother app: Pickups remembers its list until the next sync (and works it out in the background after load), the 2-minute data check only redraws when there is new data, no repeating page scans for the Ask button, no blur behind the top bar

NEW_CSS = r'''  /* change 102 (install.py) */
  .sticky.top-0.bg-slate-900 { backdrop-filter: none !important; -webkit-backdrop-filter: none !important; background-color: var(--bg) !important; }
  button.fixed.bottom-5.right-5 { bottom: calc(16px + env(safe-area-inset-bottom)) !important; }
  .gx-sc99 { will-change: scroll-position; }
</style>'''

HELPERS = r'''// ---------- change 102: Pickups list remembered until the next sync (install.py) ----------
const GX102 = new WeakMap();
function gxMoves102(s, sP, o) {
  let m = GX102.get(s);
  if (!m) { m = new Map(); GX102.set(s, m); }
  const key = [o.H, o.pos, o.q, window.__PMODE, [...gxHideSet()].sort().join(",")].join("|");
  if (!m.has(key)) m.set(key, computeMoves(sP, o));
  return m.get(key);
}
// work out the default Pickups list quietly after the app has loaded, so the first visit is quick
function gxPrewarm102(s) {
  const run = () => { try { gxMoves102(s, planS(s), { H: 1, pos: "all", q: "" }); } catch (e) {} };
  if (window.requestIdleCallback) window.requestIdleCallback(run, { timeout: 4000 }); else setTimeout(run, 1500);
}
'''


def change(t):
    t = lit(t, "102: styles", "</style>", NEW_CSS, "change 102 (install.py)")
    t = lit(t, "102: helpers", ROOT, HELPERS + ROOT, "change 102: Pickups list remembered")
    t = lit(t, "102: pickups uses the remembered list",
            "  const M = useMemo(() => computeMoves(sP, { H, pos, q }), [sP, H, pos, q, gxHideV]);",
            "  const M = useMemo(() => gxMoves102(s, sP, { H, pos, q }), [sP, H, pos, q, gxHideV]);",
            "gxMoves102(s, sP, { H, pos, q })")
    t = lit(t, "102: prewarm after load", "function GxQA({ s, go }) {\n",
            "function GxQA({ s, go }) {\n  useEffect(() => { const id = setTimeout(() => gxPrewarm102(s), 2500); return () => clearTimeout(id); }, [s]);\n",
            "gxPrewarm102(s), 2500)")
    t = lit(t, "102: redraw only on new data",
            "        tick((x) => x + 1);\n        if (!E || !E.generated) return;",
            "        if (!E || !E.generated || E.generated === window.__GX102G) return;\n        window.__GX102G = E.generated;\n        tick((x) => x + 1);",
            "E.generated === window.__GX102G")
    t = lit(t, "102: no repeating Ask scan (1)", "    fix();\n    const id = setInterval(fix, 2000);", "    const id = 0; /* gx102: no repeating scan */", "const id = 0; /* gx102")
    t = lit(t, "102: no repeating Ask scan (2)", '  setTimeout(run, 300);\n  setInterval(run, 1500);\n  window.addEventListener("resize", run);',
            "  /* gx102: the Ask button is placed by CSS now */", "/* gx102: the Ask button is placed by CSS now */")
    return t


edit(APP, change)
