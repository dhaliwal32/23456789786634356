# changes/213-tabs-slide.py - tabs answer the tap at once, the new page slides in from the side, each page keeps its place, and the phone tab bar stays at the top

NEW_CSS = r'''  /* change 213 (install.py): tabs slide in from the side they are on */
  @keyframes gx213-r { from { opacity: 0; transform: translate3d(28px, 0, 0); } to { opacity: 1; transform: none; } }
  @keyframes gx213-l { from { opacity: 0; transform: translate3d(-28px, 0, 0); } to { opacity: 1; transform: none; } }
  .gx-pg101.gx-in213r { animation: gx213-r .24s cubic-bezier(.2, .8, .2, 1); }
  .gx-pg101.gx-in213l { animation: gx213-l .24s cubic-bezier(.2, .8, .2, 1); }
  @media (prefers-reduced-motion: reduce) { .gx-pg101.gx-in213r, .gx-pg101.gx-in213l { animation: none !important; } }
  /* change 213: "hidden" here stopped the phone top bar from staying at the top; "clip" cuts the same sideways overflow without that */
  @media (max-width: 640px) { html, body { overflow-x: clip; } }
</style>'''

HELPERS = r'''// ---------- change 213: tabs answer at once, slide, and remember where you were (install.py) ----------
window.__GX213Y = window.__GX213Y || {};
const gxTabIdx213 = (tab) => { const i = GX_TABS103.findIndex((x) => gxTabOn103(x[0], tab)); return i < 0 ? 99 : i; };
'''

OLD_GO = '''  const go = (t, sub, extra) => {
    setTab(t); setPlayer(null);
    if (sub) setSubs((x) => ({ ...x, [t]: sub }));
    if (extra && extra.partner) setTradePartner(extra.partner);
    if (t === "teams") setTeamView(null);
    window.scrollTo(0, 0);
  };'''
NEW_GO = '''  const go = (t, sub, extra) => {
    /* change 213: remember this page's place, then switch in the background so the tap shows at once */
    const from213 = tab + "/" + (subs[tab] || ""), to213 = t + "/" + (sub || subs[t] || "");
    if (from213 === to213) { window.__GX213Y[to213] = 0; setPlayer(null); try { window.scrollTo({ top: 0, behavior: "smooth" }); } catch (e) { window.scrollTo(0, 0); } return; }
    window.__GX213Y[from213] = window.scrollY;
    window.__GX213GO = to213;
    React.startTransition(() => {
      setTab(t); setPlayer(null);
      if (sub) setSubs((x) => ({ ...x, [t]: sub }));
      if (extra && extra.partner) setTradePartner(extra.partner);
      if (t === "teams") setTeamView(null);
    });
  };
  const key213 = tab + "/" + (subs[tab] || "");
  const prev213 = React.useRef({ k: key213, i: 0 });
  const idx213 = gxTabIdx213(tab);
  const dir213 = prev213.current.k === key213 ? "" : idx213 > prev213.current.i ? " gx-in213r" : idx213 < prev213.current.i ? " gx-in213l" : "";
  React.useLayoutEffect(() => {
    const was = prev213.current.k;
    prev213.current = { k: key213, i: idx213 };
    if (was === key213) return;
    const y = window.__GX213GO === key213 ? window.__GX213Y[key213] || 0 : 0;
    window.__GX213GO = null;
    window.scrollTo(0, y);
  }, [key213]);'''

OLD_PG = '<div key={tab + "/" + (sub || "")} className="gx-pg101">{content}</div>'
NEW_PG = '<div key={tab + "/" + (sub || "")} className={"gx-pg101" + dir213}>{content}</div>'

OLD_TOP = '''function GxTopM103({ s, tab, go, ageH }) {
  const ref = React.useRef(null);'''
NEW_TOP = '''function GxTopM103({ s, tab, go, ageH }) {
  const ref = React.useRef(null);
  const [pend213, setPend213] = useState(null); /* change 213: the tapped tab lights up at once */
  useEffect(() => { setPend213(null); }, [tab, (window.__ROUTE || {}).sub]);'''
OLD_A = 'className={gxTabOn103(k, tab) ? "on" : ""} onClick={(e) => { if (gxNewTab(e)) return; e.preventDefault(); go(t, sb || undefined); }}'
NEW_A = 'className={(pend213 ? pend213 === k : gxTabOn103(k, tab)) ? "on" : ""} onClick={(e) => { if (gxNewTab(e)) return; e.preventDefault(); setPend213(k); go(t, sb || undefined); }}'

def change(t):
    t = lit(t, "213: styles", "</style>", NEW_CSS, "change 213 (install.py)")
    t = lit(t, "213: helpers", ROOT, HELPERS + ROOT, "change 213: tabs answer at once")
    t = lit(t, "213: go", OLD_GO, NEW_GO, "change 213: remember this page's place")
    t = lit(t, "213: page slide", OLD_PG, NEW_PG, 'className={"gx-pg101" + dir213}')
    t = lit(t, "213: tab bar state", OLD_TOP, NEW_TOP, "change 213: the tapped tab lights up at once")
    t = lit(t, "213: tab bar tap", OLD_A, NEW_A, "setPend213(k); go(t, sb || undefined)")
    return t

edit(APP, change)
