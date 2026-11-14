# changes/267-tracker-live-motion.py - live tracker like bet365: puck keeps moving around the attacking zone between plays, attack labels, pressure bar, goal celebration, power play tag, Watch button, rink stays pinned at the top while scrolling

NEW_CSS = r'''  /* change 267 (install.py) */
  .gx-tk264 { display: contents; }
  .gx-tk264 .pn267 { position: sticky; top: 0; z-index: 6; background: var(--bg); padding: 4px 16px 6px; box-shadow: 0 8px 12px -10px rgba(0,0,0,.6); }
  .gx-tk264 .ls266 { margin: 4px 16px 10px; }
  .gx-tk264 .hd264 .rt267 { display: flex; align-items: center; gap: 8px; flex: 0 0 auto; }
  .gx-tk264 .wt267 { font-size: 12px; font-weight: 700; padding: 4px 10px; border-radius: 7px; background: var(--card3, #2a2c31); color: var(--ink); border: 1px solid var(--line2, #3a3c42); text-decoration: none; letter-spacing: 0; }
  .gx-tk264 .pb267 { display: grid; grid-template-columns: 38px 1fr 38px; align-items: center; gap: 8px; padding: 8px 2px 0; font-size: 11px; font-weight: 800; }
  .gx-tk264 .pb267 .br267 { position: relative; height: 8px; border-radius: 4px; overflow: hidden; background: var(--line); }
  .gx-tk264 .pb267 .br267 i { position: absolute; top: 0; bottom: 0; transition: width .8s ease, left .8s ease; }
  .gx-tk264 .pb267 .br267 em { position: absolute; left: 50%; top: -2px; bottom: -2px; width: 2px; margin-left: -1px; background: var(--bg); }
  .gx-tk264 .pb267 span:last-child { text-align: right; }
  .gx-tk264 .pb267 small { grid-column: 1 / -1; text-align: center; font-size: 10.5px; font-weight: 500; color: var(--mute); margin-top: -2px; }
  .gx-tk264 .lb267 { transition: opacity .4s; }
  .gx-tk264 .cl267 { animation: gx267fl .9s ease-in-out 0s 3 alternate both; }
  @keyframes gx267fl { from { opacity: .25; } to { opacity: .7; } }
  .gx-tk264 .ct267 { transform-box: fill-box; transform-origin: center; animation: gx267pop .5s cubic-bezier(.2, 1.4, .4, 1) 1 both; }
  @keyframes gx267pop { from { transform: scale(.3); opacity: 0; } to { transform: scale(1); opacity: 1; } }
  @media (prefers-reduced-motion: reduce) { .gx-tk264 .cl267, .gx-tk264 .ct267 { animation: none; } }
</style>'''

HELPERS = r'''// ---------- change 267: live tracker motion, attack labels, pressure, goal celebration, power play, Watch (install.py) ----------
const gxG267 = (id) => ((window.__NHLNOW || {}).games || []).find((x) => x.id === id) || null;
// which end a team attacks this period: where its shots were, else home attacks the right end
function gxSide267(d, t, per) {
  const sh = (ps) => d.ev.filter((q) => q.t === t && q.x != null && Math.abs(q.x) > 25 && (q.goal || /shot|save/i.test(q.ty)) && ps(q));
  let L = sh((q) => q.per === per); if (!L.length) L = sh(() => true);
  if (L.length) { const s = L.reduce((a, q) => a + Math.sign(q.x), 0); if (s) return s > 0 ? 1 : -1; }
  return t === "h" ? 1 : -1;
}
const gxOth267 = (t) => (t === "h" ? "a" : t === "a" ? "h" : "");
// who is attacking at a play: the play's team if it is in that team's attacking zone, the other team if in its own end
function gxWho267(d, q, per) {
  if (!q || !q.t) return { t: "", zs: 0 };
  if (q.x == null || Math.abs(q.x) <= 25) return { t: q.t, zs: 0 };
  const s = gxSide267(d, q.t, per);
  if (Math.sign(q.x) === s) return { t: q.t, zs: s };
  const o = gxOth267(q.t); return { t: o, zs: o ? gxSide267(d, o, per) : 0 };
}
const gxStop267 = (e) => !e || e.goal || /stoppage|penalty|faceoff|period|game|shootout|challenge|timeout/i.test(e.ty);
function gxAtk267(d, k, e, p) {
  const per = (e && e.per) || d.per || 1, w = gxWho267(d, p, per);
  let lab = "";
  if (e) {
    if (e.goal) lab = "GOAL";
    else if (/stoppage|penalty|faceoff/i.test(e.ty)) lab = e.ty;
    else if (/shot/i.test(e.ty)) lab = e.ty;
    else if (!w.zs) lab = "In possession";
    else lab = p && Math.abs(p.x) >= 64 ? "Dangerous attack" : "Attack";
  }
  const lt = e && (e.goal || /shot/i.test(e.ty)) ? e.t : w.t;
  return { t: w.t, zs: w.zs, lab, lt, hold: gxStop267(e) };
}
// pressure: last 12 plays, shots count most; plays in a team's own end count for the other team
function gxPress267(d, k) {
  const per = d.per || 1; let a = 0, h = 0;
  d.ev.slice(Math.max(0, k - 11), k + 1).forEach((q) => {
    if (!q.t) return;
    let w = 0.3, who = q.t;
    if (q.goal) w = 4; else if (/^(shot|save)/i.test(q.ty)) w = 3; else if (/missed/i.test(q.ty)) w = 2; else if (/blocked/i.test(q.ty)) w = 1.5;
    else { if (/takeaway/i.test(q.ty)) w = 1; else if (/hit/i.test(q.ty)) w = 0.7; else if (/faceoff/i.test(q.ty)) w = 0.5; else if (/giveaway/i.test(q.ty)) { w = 1; who = gxOth267(q.t); }
      const z = gxWho267(d, q, q.per || per); if (z.zs && z.t) who = z.t; }
    if (who === "a") a += w; else if (who === "h") h += w;
  });
  return a + h > 0 ? a / (a + h) : 0.5;
}
// the puck: glides to each real play, then keeps moving around the attacking zone until the next one (stops at whistles, faceoffs and goals)
function GxPuck267({ x, y, k, hold, zs, fill }) {
  const g = React.useRef(null), S = React.useRef(null);
  React.useLayoutEffect(() => {
    const el = g.current; if (!el) return;
    const cur = S.current || (S.current = { x, y: -y });
    const paint = () => el.setAttribute("transform", "translate(" + cur.x.toFixed(2) + " " + cur.y.toFixed(2) + ")");
    const still = hold || (window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches);
    const ease = (u) => (u < 0.5 ? 2 * u * u : 1 - Math.pow(-2 * u + 2, 2) / 2);
    const cl = (v, m) => Math.max(-m, Math.min(m, v));
    let leg = { fx: cur.x, fy: cur.y, tx: x, ty: -y, t0: performance.now(), dur: 650 }, raf = 0, on = true, first = true;
    const next = (now) => {
      let tx, ty;
      if (zs) { tx = zs * (30 + Math.random() * 58); ty = -34 + Math.random() * 68; }
      else { tx = x + (Math.random() * 20 - 10); ty = -y + (Math.random() * 20 - 10); }
      leg = { fx: cur.x, fy: cur.y, tx: cl(tx, 95), ty: cl(ty, 38), t0: now + (first ? 1100 : Math.random() < 0.3 ? 250 + Math.random() * 450 : 0), dur: 900 + Math.random() * 900 };
      first = false;
    };
    const frame = (now) => {
      if (!on) return;
      const u = Math.max(0, Math.min(1, (now - leg.t0) / leg.dur)), v = ease(u);
      cur.x = leg.fx + (leg.tx - leg.fx) * v; cur.y = leg.fy + (leg.ty - leg.fy) * v; paint();
      if (u >= 1) { if (still) return; next(now); }
      raf = requestAnimationFrame(frame);
    };
    paint(); raf = requestAnimationFrame(frame);
    return () => { on = false; cancelAnimationFrame(raf); };
  }, [k, hold, zs]);
  return (
    <g ref={g} data-gx="267">
      <circle r="3.2" fill={fill || "#888"} opacity="0.35" />
      <circle r="1.7" fill="#111" stroke="#fff" strokeWidth="0.55" />
    </g>
  );
}
// goal: rink flashes in the scoring team's colour with GOAL for 6 seconds after the goal shows up
function GxCel267({ e, c, tm }) {
  const [until, setU] = useState(0), last = React.useRef(null);
  useEffect(() => {
    if (!e || !e.goal || last.current === e.k) return;
    const first = last.current === null; last.current = e.k;
    if (first) return; // a goal that was already there when the game opened doesn't celebrate
    const u = Date.now() + 6000; setU(u);
    const t = setTimeout(() => setU(0), 6100); return () => clearTimeout(t);
  }, [e && e.k]);
  useEffect(() => { if (last.current === null) last.current = e ? e.k : ""; }, []);
  if (!until || !e || !e.goal) return null;
  const nm = String(e.tx || "").replace(/^Goal\s*\(\d+\)\s*[^,]*,\s*/i, "").slice(0, 34);
  return (
    <g data-gx="267g" pointerEvents="none">
      <rect className="cl267" x="-100" y="-42.5" width="200" height="85" rx="28" ry="28" fill={c ? c.f : "#2563eb"} />
      <g className="ct267">
        <text x="0" y="-2" textAnchor="middle" fontSize="22" fontWeight="900" fill="#fff" stroke="rgba(0,0,0,.45)" strokeWidth="0.8" paintOrder="stroke" letterSpacing="2">GOAL</text>
        <text x="0" y="12" textAnchor="middle" fontSize="7" fontWeight="800" fill="#fff" stroke="rgba(0,0,0,.45)" strokeWidth="0.5" paintOrder="stroke">{tm}{nm ? "  " + nm : ""}</text>
      </g>
    </g>
  );
}
'''

def change(t):
    t = lit(t, "267: styles", "</style>", NEW_CSS, "change 267 (install.py)")
    t = lit(t, "267: helpers", ROOT, HELPERS + ROOT, "change 267: live tracker motion")
    t = lit(t, "267: attacking side",
            'const zs = p && p.t && Math.abs(p.x) > 25 ? (p.x > 0 ? 1 : -1) : 0, zc = p ? col(p.t) : null;',
            'const S267 = gxAtk267(d, k, e, p), zs = S267.zs, zc = col(S267.t) || (p ? col(p.t) : null), g267 = gxG267(id), pp267 = g267 ? gxPPNow182(g267) : null, pr267 = gxPress267(d, k), lc267 = col(S267.lt);',
            "const S267 = gxAtk267(d, k, e, p)")
    t = lit(t, "267: pinned top part", '<div className="gx-tk264" data-gx="264">\n      <div className="hd264">',
            '<div className="gx-tk264" data-gx="264">\n      <div className="pn267">\n      <div className="hd264">', '<div className="pn267">')
    t = lit(t, "267: watch next to the clock", '<GxClk266 id={id} per={d.per} clk={d.clk} /></div>',
            '<span className="rt267"><GxClk266 id={id} per={d.per} clk={d.clk} />{g267 ? <a className="wt267" data-gx="267w" href={gxWatchUrl175(g267, id)} target="_blank" rel="noopener" onClick={gxWatchGo211}>Watch</a> : null}</span></div>',
            'data-gx="267w"')
    old_pk = '''          {p ? (
            <g className="pk264" style={{ transform: "translate(" + p.x + "px, " + -p.y + "px)" }}>
              {e && e.goal ? <circle r="6" fill="none" stroke={ec ? ec.f : "#fff"} strokeWidth="0.8" opacity="0.8" /> : null}
              <circle r="3.2" fill={zc ? zc.f : "#888"} opacity="0.35" />
              <circle r="1.7" fill="#111" stroke="#fff" strokeWidth="0.55" />
            </g>
          ) : null}
        </svg>
      </div>
'''
    new_pk = '''          {p ? <GxPuck267 x={p.x} y={p.y} k={p.k} hold={S267.hold} zs={zs} fill={zc ? zc.f : null} /> : null}
          {S267.lab && !(e && e.goal) ? <g className="lb267" data-gx="267l" pointerEvents="none"><text x={zs ? zs * 62 : 0} y="-33" textAnchor="middle" fontSize="6.4" fontWeight="900" fill={lc267 ? lc267.f : "#e8e8e8"} stroke="rgba(0,0,0,.55)" strokeWidth="0.9" paintOrder="stroke">{(S267.lt === "h" ? H : S267.lt === "a" ? A : "") + (S267.lt ? " " : "") + S267.lab.toUpperCase()}</text></g> : null}
          {pp267 ? <g data-gx="267pp" pointerEvents="none"><rect x="-34" y="31.5" width="68" height="8.6" rx="4.3" fill="#f5a524" /><text x="0" y="37.4" textAnchor="middle" fontSize="4.8" fontWeight="800" fill="#121212">{pp267.pp + " POWER PLAY " + gxMmss132(pp267.left)}</text></g> : null}
          <GxCel267 e={e} c={ec} tm={e ? (e.t === "h" ? H : e.t === "a" ? A : "") : ""} />
        </svg>
      </div>
      <div className="pb267" data-gx="267b">
        <span style={{ color: cA.f }}>{A}</span>
        <div className="br267"><i style={{ left: 0, width: Math.round(pr267 * 100) + "%", background: cA.f }}></i><i style={{ left: Math.round(pr267 * 100) + "%", width: (100 - Math.round(pr267 * 100)) + "%", background: cH.f }}></i><em></em></div>
        <span style={{ color: cH.f }}>{H}</span>
        <small>Pressure, last 12 plays</small>
      </div>
'''
    t = lit(t, "267: moving puck and overlays", old_pk, new_pk, "<GxPuck267 x={p.x}")
    t = lit(t, "267: end of pinned part", "      <GxTkList266 d={d} k={k} col={col} A={A} H={H} />",
            "      </div>{/* 267 pinned end */}\n      <GxTkList266 d={d} k={k} col={col} A={A} H={H} />", "267 pinned end")
    return t

edit(APP, change)
