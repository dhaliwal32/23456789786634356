# changes/248-lines-hot-cold-numbers.py - Lines: warm soft spotlight on available players; hot players get trophies in their stall, cold players get cobwebs and spiders (more the hotter or colder); numbers found even when the name has accents (Lekkerimaki); name on dark jerseys moved below the shoulder band so it can be read (Oilers)

NEW_CSS = r'''  /* change 248 (install.py): spotlight, hot and cold stalls */
  .gx-fg224.gx-lt227.st246.fa::after { display: block !important; content: "" !important; position: absolute !important; left: 0 !important; right: 0 !important; top: 0 !important; bottom: auto !important; height: 100cqw !important; z-index: 0 !important; pointer-events: none; clip-path: none !important; border-radius: 0 !important; mix-blend-mode: screen; opacity: 1;
    background: radial-gradient(ellipse 16cqw 3.5cqw at 50% 0, rgba(255,252,238,.95), transparent 75%), linear-gradient(180deg, rgba(255,236,196,.5), rgba(255,226,180,.2) 65%, rgba(255,220,170,.06)) !important;
    -webkit-mask: var(--bm248) center / 100% 100% no-repeat; mask: var(--bm248) center / 100% 100% no-repeat; }
  .gx-fg224.gx-lt227.st246.fa .md.jr231 svg { filter: brightness(1.12) drop-shadow(0 0 2cqw rgba(255,226,160,.5)) drop-shadow(0 1.5cqw 2cqw rgba(0,0,0,.55)) !important; }
  .gx-fg224.gx-lt227.st246 .hc248 { position: absolute; left: 0; top: 0; width: 100%; height: 100cqw; pointer-events: none; z-index: 2; }
  .gx-fg224.gx-lt227.st246 .hc248 svg { position: absolute !important; left: 0 !important; top: 0 !important; width: 100% !important; height: 100% !important; aspect-ratio: auto !important; filter: none !important; }
  .gx-fg224.gx-lt227.st246.h2 .md.jr231 svg, .gx-fg224.gx-lt227.st246.h3 .md.jr231 svg { filter: drop-shadow(0 0 2.4cqw rgba(255,200,80,.55)) drop-shadow(0 1.5cqw 2cqw rgba(0,0,0,.55)) !important; }
  .gx-fg224.gx-lt227.st246.c2 .md.jr231 svg { filter: saturate(.75) drop-shadow(0 1.5cqw 2cqw rgba(0,0,0,.55)) !important; }
  .gx-fg224.gx-lt227.st246.c3 .md.jr231 svg { filter: saturate(.5) brightness(.85) drop-shadow(0 1.5cqw 2cqw rgba(0,0,0,.55)) !important; }
  .gx-fg224.gx-lt227.st246.c3 .hc248 { background: linear-gradient(180deg, rgba(150,155,160,.16), rgba(90,95,100,.22)); }
  @keyframes gx-sp248 { 0% { transform: translateY(0); } 50% { transform: translateY(2.2px); } 100% { transform: translateY(0); } }
  .gx-fg224.gx-lt227.st246 .hc248 .sp { animation: gx-sp248 3.2s ease-in-out infinite; transform-box: fill-box; }
  @keyframes gx-tw248 { 0%, 100% { opacity: .2; } 50% { opacity: 1; } }
  .gx-fg224.gx-lt227.st246 .hc248 .tw { animation: gx-tw248 2.2s ease-in-out infinite; }
  @media (prefers-reduced-motion: reduce) { .gx-fg224.gx-lt227.st246 .hc248 .sp, .gx-fg224.gx-lt227.st246 .hc248 .tw { animation: none; } }
</style>'''

HELPERS = r'''// ---------- change 248: hot and cold stalls on Lines (install.py) ----------
// soft cone of light for the available-player spotlight (blurred trapezoid used as a mask)
(function () { try { const s = "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100' preserveAspectRatio='none'><defs><filter id='b' x='-20%' y='-20%' width='140%' height='140%'><feGaussianBlur stdDeviation='3.2'/></filter></defs><polygon points='40,0 60,0 88,100 12,100' fill='white' filter='url(#b)'/></svg>"; document.documentElement.style.setProperty("--bm248", "url(\"data:image/svg+xml," + encodeURIComponent(s) + "\")"); } catch (e) {} })();
// jersey number by name, ignoring accents (Lekkerimaki / Lekkerimäki)
function gxNo248(T, n) { const m = (T && T.no) || {}; if (m[n] != null) return m[n]; const k = nrm(n); for (const x in m) if (nrm(x) === k) return m[x]; return null; }
// last 5 games against what he is expected to score: h1..h3 hot, c1..c3 cold, "" normal
function gxHC248(p, hist, s) {
  if (!p) return "";
  const a = (hist || {})[String(p.id).slice(1)];
  if (!a || a.length < 4) return "";
  const exp = effAvg(p, s.blend);
  if (!(exp > 0.5)) return "";
  const r = a.reduce((t, v) => t + v, 0) / a.length / exp - 1;
  return r >= 1 ? "h3" : r >= 0.7 ? "h2" : r >= 0.4 ? "h1" : r <= -0.8 ? "c3" : r <= -0.6 ? "c2" : r <= -0.4 ? "c1" : "";
}
function gxCup248(x, y, h, k) {
  const w = h * 0.62, s = h / 10;
  return (
    <g key={k} transform={"translate(" + x + " " + y + ") scale(" + s + ")"}>
      <ellipse cx="0" cy="0.2" rx="4.2" ry="0.7" fill="rgba(0,0,0,.45)" />
      <path d="M-3 0 h6 v-1.4 h-6 Z" fill="#5a3b12" />
      <path d="M-1.9 -1.4 h3.8 l-0.5 -1.1 h-2.8 Z" fill="#b8860b" />
      <path d="M-0.55 -2.5 h1.1 v-2.1 h-1.1 Z" fill="#c9971a" />
      <path d="M-3.1 -9.6 h6.2 q0 4.6 -3.1 5.1 q-3.1 -0.5 -3.1 -5.1 Z" fill="#e0aa1e" stroke="#7a560c" strokeWidth="0.18" />
      <path d="M-3.1 -8.9 q-2 0 -1.9 1.5 q0.2 1.4 2.1 1.3 M3.1 -8.9 q2 0 1.9 1.5 q-0.2 1.4 -2.1 1.3" fill="none" stroke="#d29c19" strokeWidth="0.45" />
      <path d="M-2.2 -9.2 q-0.1 3.4 1.2 4.2" fill="none" stroke="#fff1b0" strokeWidth="0.45" opacity=".8" />
      <circle className="tw" cx="1.6" cy="-8.6" r="0.35" fill="#fff" />
    </g>
  );
}
function gxWeb248(cx, cy, r, ang0, k) {
  const sp = [], n = 6, a1 = ang0, a2 = ang0 + 90;
  const pt = (a, rr) => [cx + Math.cos(a * Math.PI / 180) * rr, cy + Math.sin(a * Math.PI / 180) * rr];
  for (let i = 0; i <= n; i++) { const a = a1 + (a2 - a1) * i / n, [x, y] = pt(a, r); sp.push(<line key={"l" + i} x1={cx} y1={cy} x2={x} y2={y} />); }
  for (let j = 1; j <= 4; j++) {
    const rr = r * j / 4.4; let d = "";
    for (let i = 0; i <= n; i++) { const a = a1 + (a2 - a1) * i / n, [x, y] = pt(a, rr); d += (i ? " Q" + pt(a - (a2 - a1) / n / 2, rr * 0.86).map((v) => v.toFixed(2)).join(" ") + " " : "M") + x.toFixed(2) + " " + y.toFixed(2); }
    sp.push(<path key={"r" + j} d={d} fill="none" />);
  }
  return <g key={k} stroke="rgba(235,240,245,.6)" strokeWidth="0.32">{sp}</g>;
}
function gxSpider248(x, y, top, s, k) {
  const legs = [];
  for (let i = 0; i < 4; i++) { const yy = -0.9 + i * 0.6; legs.push(<path key={"a" + i} d={"M-0.6 " + yy + " q-1.6 -0.8 -2.4 " + (0.9 + i * 0.5)} />, <path key={"b" + i} d={"M0.6 " + yy + " q1.6 -0.8 2.4 " + (0.9 + i * 0.5)} />); }
  return (
    <g key={k}>
      <line x1={x} y1={top} x2={x} y2={y - 1.6 * s} stroke="rgba(235,240,245,.55)" strokeWidth="0.22" />
      <g className="sp" transform={"translate(" + x + " " + y + ") scale(" + s + ")"}>
        <g fill="none" stroke="#111" strokeWidth="0.32" strokeLinecap="round">{legs}</g>
        <ellipse cx="0" cy="0.5" rx="1.1" ry="1.4" fill="#141414" stroke="#3a3a3a" strokeWidth="0.15" />
        <circle cx="0" cy="-1" r="0.7" fill="#1c1c1c" />
        <circle cx="-0.25" cy="-1.15" r="0.13" fill="#c33" /><circle cx="0.25" cy="-1.15" r="0.13" fill="#c33" />
      </g>
    </g>
  );
}
function GxHC248({ k }) {
  if (!k) return null;
  const g = [];
  if (k === "h1") g.push(gxCup248(84, 95, 9, "a"));
  if (k === "h2") g.push(gxCup248(16, 95, 9, "a"), gxCup248(84, 95, 11, "b"));
  if (k === "h3") g.push(gxCup248(10, 95, 8, "a"), gxCup248(21, 95.5, 12, "b"), gxCup248(79, 95.5, 12, "c"), gxCup248(90, 95, 8, "d"));
  if (k === "c1") g.push(gxWeb248(0, 0, 18, 0, "w1"));
  if (k === "c2") g.push(gxWeb248(0, 0, 22, 0, "w1"), gxWeb248(100, 0, 18, 90, "w2"), gxSpider248(80, 30, 0, 1.2, "s1"));
  if (k === "c3") g.push(gxWeb248(0, 0, 28, 0, "w1"), gxWeb248(100, 0, 26, 90, "w2"), gxWeb248(0, 100, 16, 270, "w3"), gxWeb248(100, 100, 16, 180, "w4"), gxSpider248(18, 38, 0, 1.3, "s1"), gxSpider248(84, 24, 0, 1, "s2"), gxSpider248(70, 52, 0, 0.9, "s3"));
  return <span className={"hc248"} aria-hidden="true"><svg viewBox="0 0 100 100" preserveAspectRatio="none">{g}</svg></span>;
}
'''

CARD_OLD = '''<div className="md jr231"><span className="pl232">{last}</span><GxJersey232 t={p ? p.t : t} name={last} no={((T && T.no) || {})[n]} goalie={isG} /></div>'''
CARD_NEW = '''<div className="md jr231"><span className="pl232">{last}</span><GxJersey232 t={p ? p.t : t} name={last} no={gxNo248(T, n)} goalie={isG} /></div><GxHC248 k={gxHC248(p, h248, s)} />'''

def change(t):
    t = lit(t, "248: styles", "</style>", NEW_CSS, "change 248 (install.py)")
    t = lit(t, "248: helpers", ROOT, HELPERS + ROOT, "change 248: hot and cold stalls")
    t = lit(t, "248: last 5 games for the team on screen",
            "  const [zoom224, setZoom224] = useState(null); /* change 224: the zoomed player */",
            '''  const [zoom224, setZoom224] = useState(null); /* change 224: the zoomed player */
  const [h248, setH248] = useState({}); /* change 248: last 5 games for hot and cold stalls */
  const ids248 = useMemo(() => { const out = new Set(); Object.values(ln || {}).forEach((a) => { if (Array.isArray(a)) a.forEach((n) => { const p = n && byName[nrm(n)]; if (p) out.add(String(p.id).slice(1)); }); }); return [...out].join(","); }, [ln, byName]);
  useEffect(() => { let dead = false; if (!ids248) return undefined; gxLast5(ids248.split(","), s.sc || {}).then((h) => { if (!dead) setH248(h || {}); }); return () => { dead = true; }; }, [ids248]);''',
            "change 248: last 5 games for hot and cold stalls")
    t = lit(t, "248: card number and hot/cold", CARD_OLD, CARD_NEW, "<GxHC248 k={gxHC248(p, h248, s)} />")
    t = lit(t, "248: number line",
            '''<span className="sb227">{(((T && T.no) || {})[n] != null ? "#" + ((T && T.no) || {})[n] + " \\u00b7 " : "")''',
            '''<span className="sb227">{(gxNo248(T, n) != null ? "#" + gxNo248(T, n) + " \\u00b7 " : "")''',
            '''"#" + gxNo248(T, n) + " \\u00b7 "''')
    t = lit(t, "248: hot/cold class on the stall",
            '''className={"gx-fg224 gx-lt227" + (mine ? " me" : fa ? " fa" : "") + gxSt246c(t)}''',
            '''className={"gx-fg224 gx-lt227" + (mine ? " me" : fa ? " fa" : "") + gxSt246c(t) + (gxSt246c(t) && gxHC248(p, h248, s) ? " " + gxHC248(p, h248, s) : "")}''',
            '''(gxSt246c(t) && gxHC248(p, h248, s)''')
    t = lit(t, "248: name below the shoulder band on dark jerseys",
            '''<path id={id + "a"} d="M27 47 Q60 37 93 47" fill="none" />''',
            '''<path id={id + "a"} d={dark ? "M27 57 Q60 47 93 57" : "M27 47 Q60 37 93 47"} fill="none" />''',
            '''d={dark ? "M27 57 Q60 47 93 57"''')
    return t

edit(APP, change)
