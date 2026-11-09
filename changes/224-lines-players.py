# changes/224-lines-players.py - Lines: players stand on the rink (back to you, team colours, name and number); tap one to zoom into a big model you can spin, with all his stats, and swipe or use arrows to move between players

NEW_CSS = r'''  /* change 224 (install.py): Lines players on the rink and the zoomed player view */
  .gx-rk111 .row { --gp224: 6px; gap: var(--gp224); }
  @media (max-width: 640px) { .gx-rk111 .row { --gp224: 4px; } }
  .gx-rk111 .row.c112 { grid-template-columns: 22px repeat(var(--n), calc((100% - 22px - 3 * var(--gp224)) / 3)); justify-content: center; }
  .gx-rk111 .row { margin: 2px 0; }
  .gx-fg224 { display: flex; flex-direction: column; align-items: center; min-width: 0; padding: 4px 0 6px; background: none; border: 0; cursor: pointer; transition: transform .15s ease; -webkit-tap-highlight-color: transparent; }
  .gx-fg224:active { transform: scale(.95); }
  .gx-fg224 .md { position: relative; width: 66px; }
  .gx-fg224 .md svg { position: relative; z-index: 1; display: block; width: 100%; height: auto; filter: drop-shadow(0 3px 3px rgba(0,0,0,.35)); }
  .gx-fg224 .rg { position: absolute; left: 50%; bottom: -3px; width: 78%; height: 12px; transform: translateX(-50%); border-radius: 50%; background: rgba(0,0,0,.28); }
  .gx-fg224 .rg.me { background: none; border: 2.5px solid var(--accent); box-shadow: 0 0 8px var(--accent); }
  .gx-fg224 .rg.fa { background: none; border: 2.5px solid var(--good); box-shadow: 0 0 8px var(--good); }
  .gx-fg224 .nm { margin-top: 6px; font-size: 12.5px; font-weight: 700; color: var(--ink); max-width: 100%; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .gx-fg224.empty .md { height: 92px; }
  @media (max-width: 640px) { .gx-fg224 .md { width: 54px; } .gx-fg224 .nm { font-size: 11.5px; } .gx-fg224.empty .md { height: 76px; } }

  .gx-lz224 { z-index: 60; display: flex; align-items: center; justify-content: center; background: rgba(4,5,7,.74); -webkit-backdrop-filter: blur(6px); backdrop-filter: blur(6px); animation: gx224-fade .22s ease-out; overscroll-behavior: contain; }
  .gx-lz224.out { animation: gx224-fadeout .22s ease-in forwards; }
  @keyframes gx224-fade { from { opacity: 0; } to { opacity: 1; } }
  @keyframes gx224-fadeout { to { opacity: 0; } }
  .gx-lz224 .pn { position: relative; width: min(460px, 100%); max-height: 100%; overflow-y: auto; overscroll-behavior: contain; background: var(--bg); border: 1px solid var(--line); border-radius: 22px; padding: 0 0 16px; }
  @media (max-width: 640px) { .gx-lz224 .pn { width: 100%; height: 100%; border-radius: 0; border: 0; padding-bottom: calc(16px + env(safe-area-inset-bottom)); } }
  .gx-lz224 .x { position: absolute; top: 10px; right: 10px; z-index: 3; width: 40px; height: 40px; border-radius: 99px; background: rgba(0,0,0,.35); color: #fff; font-size: 22px; line-height: 1; }
  .gx-lz224 .st { position: relative; height: 310px; perspective: 900px; display: flex; align-items: flex-end; justify-content: center; padding-bottom: 16px; touch-action: pan-y; cursor: grab; overflow: hidden; }
  .gx-lz224 .st .fl { position: absolute; left: 50%; bottom: 10px; width: 190px; height: 30px; transform: translateX(-50%); border-radius: 50%; background: radial-gradient(ellipse, rgba(0,0,0,.55), transparent 70%); }
  .gx-lz224 .sp { position: relative; width: 170px; height: 272px; transform-style: preserve-3d; will-change: transform; }
  .gx-lz224 .sp > svg { position: absolute; inset: 0; width: 100%; height: 100%; -webkit-backface-visibility: hidden; backface-visibility: hidden; }
  .gx-lz224 .sp > svg.fr { transform: rotateY(180deg); }
  .gx-lz224 .zm { transition: transform .32s cubic-bezier(.2,.8,.2,1), opacity .32s; transform-origin: 50% 100%; }
  .gx-lz224 .hint { position: absolute; left: 0; right: 0; top: 12px; text-align: center; font-size: 11px; color: rgba(255,255,255,.6); pointer-events: none; }
  .gx-lz224 .ar { position: absolute; top: 140px; z-index: 2; width: 42px; height: 42px; border-radius: 99px; background: rgba(0,0,0,.35); color: #fff; font-size: 26px; line-height: 1; display: flex; align-items: center; justify-content: center; }
  .gx-lz224 .ar.l { left: 10px; } .gx-lz224 .ar.r { right: 10px; }
  .gx-lz224 .ar:disabled { opacity: .25; }
  .gx-lz224 .inf { padding: 0 16px; touch-action: pan-y; }
  .gx-lz224 .hd { text-align: center; }
  .gx-lz224 .hd b { display: block; font-size: 22px; font-weight: 800; color: var(--ink); }
  .gx-lz224 .hd small { display: block; font-size: 13px; color: var(--mute); margin-top: 2px; }
  .gx-lz224 .tg { display: inline-block; margin-top: 6px; padding: 2px 10px; border-radius: 99px; font-size: 12px; font-weight: 700; border: 1px solid var(--line2); color: var(--ink2, var(--ink)); }
  .gx-lz224 .tg.me { border-color: var(--accent); color: var(--accent); } .gx-lz224 .tg.fa { border-color: var(--good); color: var(--good); }
  .gx-lz224 .ln { margin-top: 8px; text-align: center; font-size: 12.5px; color: var(--mute); }
  .gx-lz224 .tl { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 6px; margin-top: 14px; }
  .gx-lz224 .tl > div, .gx-lz224 .gs > div { background: var(--card); border-radius: 10px; padding: 8px 4px; text-align: center; min-width: 0; }
  .gx-lz224 .tl small, .gx-lz224 .gs small { display: block; font-size: 10.5px; color: var(--mute); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .gx-lz224 .tl b { display: block; font-size: 17px; font-weight: 700; color: var(--ink); font-variant-numeric: tabular-nums; }
  .gx-lz224 .sh { margin: 14px 0 6px; font-size: 12px; color: var(--mute); letter-spacing: .06em; }
  .gx-lz224 .gs { display: grid; grid-template-columns: repeat(5, minmax(0, 1fr)); gap: 6px; }
  .gx-lz224 .gs b { display: block; font-size: 15px; font-weight: 600; color: var(--ink); font-variant-numeric: tabular-nums; white-space: nowrap; }
  .gx-lz224 .bt { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 8px; margin-top: 16px; }
  .gx-lz224 .bt button { padding: 11px 6px; border-radius: 12px; border: 1px solid var(--line2); font-size: 14px; font-weight: 600; color: var(--ink); }
  .gx-lz224 .bt button.pr { background: var(--ink); border-color: var(--ink); color: var(--bg); }
  .gx-lz224 .dots { display: flex; justify-content: center; gap: 5px; margin-top: 14px; }
  .gx-lz224 .dots i { width: 6px; height: 6px; border-radius: 99px; background: var(--line2); }
  .gx-lz224 .dots i.on { background: var(--ink); }
  .gx-lz224 .sw.r { animation: gx224-r .26s cubic-bezier(.2,.8,.2,1); } .gx-lz224 .sw.l { animation: gx224-l .26s cubic-bezier(.2,.8,.2,1); }
  @keyframes gx224-r { from { opacity: 0; transform: translate3d(40px,0,0); } to { opacity: 1; transform: none; } }
  @keyframes gx224-l { from { opacity: 0; transform: translate3d(-40px,0,0); } to { opacity: 1; transform: none; } }
  @media (prefers-reduced-motion: reduce) { .gx-lz224, .gx-lz224 .sw.r, .gx-lz224 .sw.l { animation: none !important; } .gx-lz224 .zm { transition: none !important; } }
</style>'''

HELPERS = r'''// ---------- change 224: Lines players standing on the rink, tap to zoom (install.py) ----------
// body, trim, number colour per team: a plain jersey in team colours, not a copy of a real design
const GX_JC224 = { ANA: ["#1c1c1f", "#F47A38", "#F47A38"], BOS: ["#1c1c1f", "#FFB81C", "#FFB81C"], BUF: ["#003087", "#FFB81C", "#FFFFFF"], CGY: ["#C8102E", "#F1BE48", "#FFFFFF"],
  CAR: ["#CE1126", "#1c1c1f", "#FFFFFF"], CHI: ["#CF0A2C", "#1c1c1f", "#FFFFFF"], COL: ["#6F263D", "#236192", "#FFFFFF"], CBJ: ["#002654", "#CE1126", "#FFFFFF"],
  DAL: ["#006847", "#1c1c1f", "#FFFFFF"], DET: ["#CE1126", "#FFFFFF", "#FFFFFF"], EDM: ["#041E42", "#FF4C00", "#FF4C00"], FLA: ["#C8102E", "#041E42", "#FFFFFF"],
  LA: ["#1c1c1f", "#A2AAAD", "#FFFFFF"], MIN: ["#154734", "#A6192E", "#EAAA00"], MTL: ["#AF1E2D", "#192168", "#FFFFFF"], NSH: ["#FFB81C", "#041E42", "#041E42"],
  NJ: ["#CE1126", "#1c1c1f", "#FFFFFF"], NYI: ["#00539B", "#F47D30", "#FFFFFF"], NYR: ["#0038A8", "#CE1126", "#FFFFFF"], OTT: ["#1c1c1f", "#C52032", "#FFFFFF"],
  PHI: ["#F74902", "#1c1c1f", "#FFFFFF"], PIT: ["#1c1c1f", "#FCB514", "#FCB514"], SJ: ["#006D75", "#EA7200", "#FFFFFF"], SEA: ["#001628", "#99D9D9", "#99D9D9"],
  STL: ["#002F87", "#FCB514", "#FFFFFF"], TB: ["#002868", "#FFFFFF", "#FFFFFF"], TOR: ["#00205B", "#FFFFFF", "#FFFFFF"], UTA: ["#1c1c1f", "#6CACE4", "#FFFFFF"],
  VAN: ["#00205B", "#00843D", "#FFFFFF"], VGK: ["#333F48", "#B4975A", "#B4975A"], WSH: ["#C8102E", "#041E42", "#FFFFFF"], WPG: ["#041E42", "#AC162C", "#FFFFFF"] };
const gxJc224 = (t) => GX_JC224[t] || GX_JC224[typeof gxAb131 === "function" ? gxAb131(t) : t] || ["#3a3d44", "#9aa0a8", "#FFFFFF"];
let gxSkN224 = 0;
// a whole skater (or goalie) seen from behind ("back") or the front ("front"), viewBox 100 x 160
function GxSkater224({ t, name, no, side, goalie, className }) {
  const [bd, tr, nc] = gxJc224(t);
  const id = React.useMemo(() => "sk224_" + (++gxSkN224), []);
  const nm = String(name || "").toUpperCase().slice(0, 14), num = no == null || no === "" ? "" : String(no), front = side === "front";
  const hel = bd.toUpperCase() === "#FFFFFF" ? "#1c1c1f" : bd;
  const shade = "url(#" + id + ")";
  const torso = goalie
    ? "M30 34 Q50 28 70 34 L88 41 Q97 45 98 56 L99 78 L86 81 L81 60 L82 100 L18 100 L19 60 L14 81 L1 78 L2 56 Q3 45 12 41 Z"
    : "M32 34 Q50 29 68 34 L85 41 Q94 45 95 55 L96 74 L84 76 L80 58 L79 98 L21 98 L20 58 L16 76 L4 74 L5 55 Q6 45 15 41 Z";
  return (
    <svg className={className} viewBox="0 0 100 160" aria-hidden="true">
      <defs>
        <linearGradient id={id} x1="0" x2="1" y1="0" y2="0">
          <stop offset="0" stopColor="#000" stopOpacity=".42" /><stop offset=".24" stopColor="#000" stopOpacity="0" />
          <stop offset=".5" stopColor="#fff" stopOpacity=".12" /><stop offset=".76" stopColor="#000" stopOpacity="0" /><stop offset="1" stopColor="#000" stopOpacity=".42" />
        </linearGradient>
      </defs>
      {/* skates */}
      <path d="M30 146 L29 154 L46 154 L45 146 Z M55 146 L54 154 L71 154 L70 146 Z" fill="#202227" />
      <path d="M26 156.5 H48 M52 156.5 H74" stroke="#d6dade" strokeWidth="2.4" strokeLinecap="round" />
      {/* socks with stripes */}
      <path d={goalie ? "M24 112 L46 112 L46 147 L28 147 Z M54 112 L76 112 L72 147 L54 147 Z" : "M31 112 L45 112 L45 147 L31 147 Z M55 112 L69 112 L69 147 L55 147 Z"} fill={goalie ? "#e9eaec" : bd} />
      {goalie ? <path d="M24 112 L46 112 L46 147 L28 147 Z M54 112 L76 112 L72 147 L54 147 Z" fill="none" stroke={tr} strokeWidth="2" /> : <path d="M31 124 H45 M31 129 H45 M55 124 H69 M55 129 H69" stroke={tr} strokeWidth="2.4" />}
      {/* pants */}
      <path d="M22 94 L78 94 L76 115 L54 115 L50 106 L46 115 L24 115 Z" fill="#1d1f24" />
      <path d="M23 99 H77" stroke={tr} strokeWidth="2.6" opacity=".9" />
      {/* stick */}
      {goalie ? <path d="M86 84 L80 150 L60 154" stroke="#c9a56b" strokeWidth="5" fill="none" strokeLinecap="round" strokeLinejoin="round" />
        : <path d="M90 76 L84 150 L72 154" stroke="#c9a56b" strokeWidth="3.2" fill="none" strokeLinecap="round" strokeLinejoin="round" />}
      {/* jersey */}
      <path d={torso} fill={bd} />
      <path d={goalie ? "M1.6 66 L15.5 68 M1.4 71 L15 73 M98.4 66 L84.5 68 M98.6 71 L85 73" : "M4.6 64 L17.5 66 M4.5 68.5 L17 70.5 M95.4 64 L82.5 66 M95.5 68.5 L83 70.5"} stroke={tr} strokeWidth="2.6" />
      <path d="M21 86 H79 M21 91 H79" stroke={tr} strokeWidth="2.6" />
      <path d={torso} fill={shade} />
      {/* gloves (a blocker and catcher for goalies) */}
      {goalie ? <><rect x="-1" y="76" width="17" height="14" rx="4" fill="#e9eaec" stroke={tr} strokeWidth="1.5" /><ellipse cx="92" cy="84" rx="10" ry="9" fill="#e9eaec" stroke={tr} strokeWidth="1.5" /></>
        : <><rect x="3" y="73" width="14" height="12" rx="4" fill="#26282d" /><rect x="83" y="73" width="14" height="12" rx="4" fill="#26282d" /></>}
      {front ? (
        <>
          <path d="M40 33 L50 44 L60 33" stroke={tr} strokeWidth="2.6" fill="none" />
          {num ? <text x="50" y="66" textAnchor="middle" fontSize="15" fontWeight="900" fill={nc} stroke={tr === nc ? "#000" : tr} strokeOpacity={tr === nc ? 0.35 : 1} strokeWidth="1" paintOrder="stroke" style={{ fontFamily: "Arial Black, Arial, Helvetica, sans-serif" }}>{num}</text> : null}
          <ellipse cx="50" cy="20" rx="13" ry="13.5" fill={hel} />
          <ellipse cx="50" cy="20" rx="13" ry="13.5" fill={shade} />
          <path d="M40.5 18 Q50 15 59.5 18 L58 30 Q50 34 42 30 Z" fill="#e2b48c" />
          {goalie ? <path d="M40 17 H60 M40 21 H60 M40 25 H60 M44 15 V31 M50 15 V33 M56 15 V31" stroke="#cfd3d8" strokeWidth="1.1" /> : <path d="M39.5 17.5 Q50 14 60.5 17.5 L60 21.5 Q50 18.5 40 21.5 Z" fill="#20232a" opacity=".85" />}
          <circle cx="45.5" cy="23.5" r="1" fill="#2a1d14" /><circle cx="54.5" cy="23.5" r="1" fill="#2a1d14" />
        </>
      ) : (
        <>
          <path d="M41 33 Q50 38 59 33" stroke={tr} strokeWidth="2.4" fill="none" />
          <ellipse cx="50" cy="20" rx="13" ry="13.5" fill={hel} />
          <ellipse cx="50" cy="20" rx="13" ry="13.5" fill={shade} />
          <path d="M38 23 Q50 27 62 23" stroke="#000" strokeOpacity=".35" strokeWidth="1.4" fill="none" />
          {nm ? <text x="50" y="47" textAnchor="middle" fontSize="8.4" fontWeight="800" letterSpacing=".6" fill={nc} textLength={nm.length > 8 ? 46 : undefined} lengthAdjust="spacingAndGlyphs" style={{ fontFamily: "Arial, Helvetica, sans-serif" }}>{nm}</text> : null}
          {num ? <text x="50" y="77" textAnchor="middle" fontSize="27" fontWeight="900" fill={nc} stroke={tr === nc ? "#000" : tr} strokeOpacity={tr === nc ? 0.35 : 1} strokeWidth="1.3" paintOrder="stroke" style={{ fontFamily: "Arial Black, Arial, Helvetica, sans-serif" }}>{num}</text> : null}
        </>
      )}
    </svg>
  );
}
// which lines and units a player is on, e.g. "Line 1 \u00b7 PP1 \u00b7 PK2"
function gxLnOf224(ln, n) {
  const L = { F1: "Line 1", F2: "Line 2", F3: "Line 3", F4: "Line 4", D1: "Pair 1", D2: "Pair 2", D3: "Pair 3", G: "Goalie", PP1: "PP1", PP2: "PP2", PK1: "PK1", PK2: "PK2" };
  return Object.keys(L).filter((k) => (ln[k] || []).includes(n)).map((k) => L[k]).join(" \u00b7 ") || "Not in the lineup";
}
// the zoomed view: big model you can spin, stats, swipe or arrows to move, tap outside to close
function GxLnZoom224({ s, t, T, list, i0, from, byName, onClose }) {
  const [i, setI] = useState(i0);
  const [out, setOut] = useState(false);
  const [dir, setDir] = useState("");
  const zm = React.useRef(null), sp = React.useRef(null), ang = React.useRef(0), drag = React.useRef(null), sw = React.useRef(null);
  gxUse100();
  useEffect(() => { gxLoad100("sea"); }, []);
  const n = list[i], p = byName[nrm(n)] || null, ln = (T && T.lines) || {}, no = ((T && T.no) || {})[n];
  const last = n.split(" ").slice(1).join(" ") || n, isG = (ln.G || []).includes(n) || (p && p.p === "G");
  const K = s.blend;
  const rank = React.useMemo(() => {
    if (!p) return null;
    const pv = (q) => effAvg(q, K) * (q.p === "G" ? q.prob : 1);
    const L2 = s.players.filter((q) => q.p === p.p && q.prob > 0 && (q.proj !== false || q.gp > 0)).sort((a, b) => pv(b) - pv(a));
    const k = L2.findIndex((q) => q.id === p.id);
    return k < 0 ? null : k + 1;
  }, [p ? p.id : null, s.players, K]);
  // zoom in from the tapped player
  React.useLayoutEffect(() => {
    const el = zm.current;
    if (!el || !from) return;
    const r = el.getBoundingClientRect();
    if (!r.width) return;
    const sc = from.width / r.width, dx = from.left + from.width / 2 - (r.left + r.width / 2), dy = from.bottom - r.bottom;
    el.style.transition = "none"; el.style.transform = "translate(" + dx + "px," + dy + "px) scale(" + sc + ")"; el.style.opacity = ".6";
    requestAnimationFrame(() => requestAnimationFrame(() => { el.style.transition = ""; el.style.transform = ""; el.style.opacity = ""; }));
  }, []);
  const close = () => {
    if (out) return;
    setOut(true);
    const el = zm.current;
    if (el && from) { const r = el.getBoundingClientRect(); const sc = from.width / (r.width || 1); el.style.transform = "translate(" + (from.left + from.width / 2 - (r.left + r.width / 2)) + "px," + (from.bottom - r.bottom) + "px) scale(" + sc + ")"; el.style.opacity = ".4"; }
    setTimeout(onClose, 230);
  };
  const go = (d) => { const j = i + d; if (j < 0 || j >= list.length) return; setDir(d > 0 ? "r" : "l"); setI(j); ang.current = 0; if (sp.current) { sp.current.style.transition = "none"; sp.current.style.transform = "rotateY(0deg)"; } };
  useEffect(() => { const k = (e) => { if (e.key === "Escape") close(); if (e.key === "ArrowRight") go(1); if (e.key === "ArrowLeft") go(-1); }; window.addEventListener("keydown", k); return () => window.removeEventListener("keydown", k); });
  // drag on the player spins him
  const sDown = (e) => { drag.current = { x: e.clientX, a: ang.current }; if (sp.current) sp.current.style.transition = "none"; try { e.currentTarget.setPointerCapture(e.pointerId); } catch (x) {} };
  const sMove = (e) => { const d = drag.current; if (!d) return; ang.current = d.a + (e.clientX - d.x) * 0.9; if (sp.current) sp.current.style.transform = "rotateY(" + ang.current + "deg)"; };
  const sUp = () => { drag.current = null; };
  // swipe on the stats moves to the next or previous player
  const iDown = (e) => { sw.current = { x: e.clientX, y: e.clientY }; };
  const iUp = (e) => { const d = sw.current; sw.current = null; if (!d) return; const dx = e.clientX - d.x, dy = e.clientY - d.y; if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy) * 1.5) go(dx < 0 ? 1 : -1); };
  const eid = p ? String(p.id || "").replace(/^e/, "") : null, D = GX100.data.sea;
  const v = p && D ? gxAgg104(D[eid], isG, s.sc || {}) : null;
  const SK = [["GP", 0], ["G", 1], ["A", 2], ["PTS", 3], ["+/-", 4], ["PIM", 5], ["SOG", 6], ["HIT", 7], ["BLK", 8], ["TOI", 9]];
  const GO = [["GP", 0], ["W", 1], ["L", 2], ["OTL", 3], ["SV%", 6], ["GAA", 7], ["SV", 5], ["GA", 4], ["SO", 8], ["TOI", 9]];
  const mine = p && p.ft === s.me, fa = p && p.ft === "fa";
  const tag = !p ? "" : mine ? "Yours" : fa ? (p.wv ? "Waivers" : "Free agent") : teamName(s, p.ft);
  const Q = window.__QA || {};
  const act = (f) => () => { if (!p || !f) return; onClose(); setTimeout(() => f(p), 30); };
  const [bd] = gxJc224(p ? p.t : t);
  const box = (
    <div className={"fixed inset-0 gx-lz224" + (out ? " out" : "")} onClick={close} role="dialog" aria-label={n}>
      <div className="pn" onClick={(e) => e.stopPropagation()}>
        <button type="button" className="x" aria-label="Close" onClick={close}>{"\u00d7"}</button>
        <div className="st" style={{ background: "radial-gradient(ellipse at 50% 92%, " + bd + "aa, transparent 62%), linear-gradient(180deg, #0b0c0f, #15171b)" }}
          onPointerDown={sDown} onPointerMove={sMove} onPointerUp={sUp} onPointerCancel={sUp}>
          <div className="hint">Drag to spin</div>
          <button type="button" className="ar l" aria-label="Previous player" disabled={i === 0} onPointerDown={(e) => e.stopPropagation()} onClick={() => go(-1)}>{"\u2039"}</button>
          <button type="button" className="ar r" aria-label="Next player" disabled={i === list.length - 1} onPointerDown={(e) => e.stopPropagation()} onClick={() => go(1)}>{"\u203a"}</button>
          <div className="fl"></div>
          <div ref={zm} className="zm">
            <div key={n} className={"sw " + dir}>
              <div ref={sp} className="sp">
                <GxSkater224 t={p ? p.t : t} name={last} no={no} side="back" goalie={isG} />
                <GxSkater224 t={p ? p.t : t} name={last} no={no} side="front" goalie={isG} className="fr" />
              </div>
            </div>
          </div>
        </div>
        <div key={"i" + n} className={"inf sw " + dir} onPointerDown={iDown} onPointerUp={iUp}>
          <div className="hd">
            <b>{n}</b>
            <small>{(no != null ? "#" + no + " \u00b7 " : "") + (isG ? "G" : p ? p.p : "") + " \u00b7 " + (p ? p.t : t)}</small>
            {tag ? <span className={"tg" + (mine ? " me" : fa ? " fa" : "")}>{tag}</span> : null}
          </div>
          <div className="ln">{gxLnOf224(ln, n)}</div>
          {p ? (
            <>
              <div className="tl">
                <div><small>Pts/g</small><b>{f1(gxPgAvg(p, K))}</b></div>
                <div><small>Projected</small><b>{f1(effAvg(p, K))}</b></div>
                <div><small>{(isG ? "G" : p.p) + " rank"}</small><b>{rank ? "#" + rank : "-"}</b></div>
                <div><small>Season FPTS</small><b>{f1(p.tot || 0)}</b></div>
              </div>
              <div className="sh">{"SEASON"}</div>
              <div className="gs">{(isG ? GO : SK).map(([l, k]) => <div key={l}><small>{l}</small><b>{v ? v[k] : "..."}</b></div>)}</div>
              <div className="bt">
                <button type="button" className="pr" onClick={act(Q.sim)}>Simulate</button>
                {Q.tradeable && Q.tradeable(p) ? <button type="button" onClick={act(Q.trade)}>Trade</button> : <button type="button" disabled style={{ opacity: 0.4 }}>Trade</button>}
                <button type="button" onClick={() => { onClose(); setTimeout(() => { if (window.__NAV) window.__NAV.player(p); }, 30); }}>Full profile</button>
              </div>
            </>
          ) : <div className="ln" style={{ marginTop: 14 }}>No fantasy numbers for this player yet.</div>}
          <div className="dots">{list.length <= 24 ? list.map((x, k) => <i key={x + k} className={k === i ? "on" : ""}></i>) : null}</div>
        </div>
      </div>
    </div>
  );
  return ReactDOM.createPortal(box, document.body);
}
'''

OLD_CHIP = '''  const chip = (n, i) => {
    if (!n) return <div key={"e" + i} className="gx-pc111 empty"><span className="n">{"-"}</span></div>;'''
NEW_CHIP = '''  const chip = (n, i) => {
    /* change 224: players standing on the rink; tap to zoom */
    if (!n) return <div key={"e" + i} className="gx-fg224 empty"><div className="md"></div></div>;
    { const p = byName[nrm(n)], mine = p && p.ft === s.me, fa = p && p.ft === "fa", last = n.split(" ").slice(1).join(" ") || n;
      const isG = (ln.G || []).includes(n) || (p && p.p === "G");
      return (
        <button key={n + i} type="button" className="gx-fg224" aria-label={n} onClick={(e) => { const md = e.currentTarget.querySelector(".md"); setZoom224({ n, from: md ? md.getBoundingClientRect() : null }); }}>
          <div className="md"><GxSkater224 t={p ? p.t : t} name={last} no={((T && T.no) || {})[n]} side="back" goalie={isG} /><span className={"rg" + (mine ? " me" : fa ? " fa" : "")}></span></div>
          <span className="nm">{last}</span>
        </button>
      ); }'''

OLD_ORD = '  const ord = (arr) => [...(arr || [])].sort((a, b) => (GX_ORD111[df[a]] ?? 9) - (GX_ORD111[df[b]] ?? 9));'
NEW_ORD = '''  const ord = (arr) => [...(arr || [])].sort((a, b) => (GX_ORD111[df[a]] ?? 9) - (GX_ORD111[df[b]] ?? 9));
  const [zoom224, setZoom224] = useState(null); /* change 224: the zoomed player */'''

OLD_ROWS_END = '''       pair112("D1", ln.D1), pair112("D2", ln.D2), pair112("D3", ln.D3), <div key="s2" className="sp"></div>, pair112("G", ln.G)];'''
NEW_ROWS_END = '''       pair112("D1", ln.D1), pair112("D2", ln.D2), pair112("D3", ln.D3), <div key="s2" className="sp"></div>, pair112("G", ln.G)];
  /* change 224: everyone in the order shown, for moving between players in the zoomed view */
  const order224 = (mode === "pp" ? ["PP1", "PP2"] : mode === "pk" ? ["PK1", "PK2"] : ["F1", "F2", "F3", "F4", "D1", "D2", "D3", "G"]).flatMap((k) => ord(ln[k]).filter(Boolean)).filter((x, k, a) => a.indexOf(x) === k);
  const zoomEl224 = zoom224 && order224.includes(zoom224.n) ? <GxLnZoom224 key={zoom224.n + "|" + t} s={s} t={t} T={T} list={order224} i0={order224.indexOf(zoom224.n)} from={zoom224.from} byName={byName} onClose={() => setZoom224(null)} /> : null;'''

OLD_RINK = '<div key={t + mode} className="gx-rk111">'
NEW_RINK = '{zoomEl224}<div key={t + mode} className="gx-rk111">'

def change(t):
    t = lit(t, "224: styles", "</style>", NEW_CSS, "change 224 (install.py)")
    t = lit(t, "224: helpers", ROOT, HELPERS + ROOT, "change 224: Lines players standing on the rink")
    t = lit(t, "224: zoom state", OLD_ORD, NEW_ORD, "change 224: the zoomed player")
    t = lit(t, "224: players on the rink", OLD_CHIP, NEW_CHIP, "change 224: players standing on the rink; tap to zoom")
    t = lit(t, "224: order", OLD_ROWS_END, NEW_ROWS_END, "change 224: everyone in the order shown")
    t = lit(t, "224: show zoom", OLD_RINK, NEW_RINK, "{zoomEl224}<div key={t + mode}")
    return t

edit(APP, change)
