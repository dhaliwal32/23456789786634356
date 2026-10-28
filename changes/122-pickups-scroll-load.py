# changes/122-pickups-scroll-load.py - Pickups: shows the first 40 free agents and quietly loads 40 more each time you scroll near the bottom (no Show more button), so the page opens fast

HELPERS = r'''// ---------- change 122: load more of a list when you scroll near its end (install.py) ----------
function GxMore122({ onMore }) {
  const ref = React.useRef(null);
  useEffect(() => {
    const el = ref.current;
    if (!el || typeof IntersectionObserver === "undefined") { onMore(); return; }
    const io = new IntersectionObserver((es) => { if (es.some((e) => e.isIntersecting)) onMore(); }, { rootMargin: "800px 0px" });
    io.observe(el);
    return () => io.disconnect();
  });
  return <div ref={ref} style={{ height: 1 }} aria-hidden="true"></div>;
}
'''


def change(t):
    t = lit(t, "122: helpers", ROOT, HELPERS + ROOT, "change 122: load more of a list")
    t = lit(t, "122: start with 40", "  const [limit, setLimit] = useState(100000); /* gx118: show all */", "  const [limit, setLimit] = useState(40); /* gx122: 40 then more on scroll */", "gx122: 40 then more on scroll")
    t = t.replace("setLimit(100000)", "setLimit(40)")
    t = lit(t, "122: load more on scroll",
            '</div>{all.length > rows.length ? <button type="button" className="text-sm text-blue-600" style={{ marginTop: 10 }} onClick={() => setLimit(limit + 25)}>Show {Math.min(25, all.length - rows.length)} more</button> : null}',
            '</div>{all.length > rows.length ? <GxMore122 onMore={() => setLimit((v) => (v < all.length ? v + 40 : v))} /> : null}',
            "<GxMore122 onMore=")
    return t


edit(APP, change)
