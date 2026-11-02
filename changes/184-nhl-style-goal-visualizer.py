# changes/184-nhl-style-goal-visualizer.py - Goal Visualizer drawn like NHL.com's EDGE Goal Visualizer, inside the app: full rink with ice, all markings, home logo at centre ice, team codes at each end, NHL-style player circles, grey control buttons, and the scorer card with photo, goal and assist totals, Score / Time / Shot tiles and a blue replay button

NEW_CSS = r'''  /* change 184 (install.py) */
  .gx-v184 { margin-top: 10px; background: #eeeeee; color: #121212; border-radius: 12px; overflow: hidden; box-shadow: inset 0 0 0 1px #dddddd; font-family: Inter, -apple-system, "Segoe UI", Roboto, Arial, sans-serif; }
  .gx-v184 .hd184 { text-align: center; padding: 10px 12px 2px; line-height: 1.25; }
  .gx-v184 .hd184 b { display: block; font-size: 14px; font-weight: 700; color: #121212; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .gx-v184 .hd184 small { display: block; font-size: 12px; color: #666666; }
  .gx-v184 .rw184 svg { display: block; width: 100%; height: auto; }
  .gx-v184 .gx-ed165 svg { display: block; width: 100%; height: auto; }
  .gx-v184 .ct184 { display: flex; align-items: center; gap: 8px; padding: 2px 10px 10px; }
  .gx-v184 .ct184 .ib { width: 34px; height: 34px; flex: none; display: inline-flex; align-items: center; justify-content: center; border-radius: 8px; background: #c4c4c4; color: #ffffff; transition: background .15s ease; }
  .gx-v184 .ct184 .ib:hover { background: #b2b2b2; }
  .gx-v184 .ct184 .ib svg { width: 16px; height: 16px; display: block; }
  .gx-v184 .ct184 .oi184 { margin-left: auto; height: 34px; padding: 0 14px; border-radius: 8px; background: #c4c4c4; color: #ffffff; font-size: 14px; font-weight: 700; display: inline-flex; align-items: center; gap: 6px; }
  .gx-v184 .ct184 .oi184 i { font-style: normal; display: inline-block; transition: transform .25s ease; }
  .gx-v184 .ct184 .oi184 i.up { transform: rotate(180deg); }
  .gx-v184 .cd184 { background: #ffffff; display: grid; grid-template-columns: 56px minmax(0,1fr) auto 36px; align-items: center; gap: 10px 12px; padding: 12px 14px; }
  .gx-v184 .cd184.st184 { grid-template-columns: 56px minmax(0,1fr) auto; }
  .gx-v184 .fc184 { width: 56px; height: 56px; border-radius: 99px; overflow: hidden; display: flex; align-items: flex-end; justify-content: center; }
  .gx-v184 .fc184 img { width: 100%; height: 100%; object-fit: cover; object-position: center top; display: block; }
  .gx-v184 .fc184 span { width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; color: #ffffff; font-weight: 800; font-size: 18px; }
  .gx-v184 .in184 { min-width: 0; }
  .gx-v184 .nm184 { display: flex; align-items: center; gap: 8px; min-width: 0; height: 26px; }
  .gx-v184 .nm184 .bg { width: 22px; height: 22px; flex: none; border-radius: 99px; display: inline-flex; align-items: center; justify-content: center; font-size: 10.5px; font-weight: 900; }
  .gx-v184 .nm184 .tx { min-width: 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; font-size: 15px; font-weight: 700; color: #121212; }
  .gx-v184 .nm184 .tx button { color: inherit; font-weight: inherit; }
  .gx-v184 .nm184 .tx small { font-size: 15px; font-weight: 400; color: #666666; }
  .gx-v184 .as184 { display: flex; align-items: center; gap: 8px; min-width: 0; height: 24px; margin-top: 2px; }
  .gx-v184 .as184 img { width: 22px; height: 22px; flex: none; object-fit: contain; }
  .gx-v184 .as184 span { min-width: 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; font-size: 13px; color: #333333; }
  .gx-v184 .tl184 { display: grid; grid-template-columns: 84px 96px 84px; gap: 6px; }
  .gx-v184 .tl184 > div { background: #eeeeee; border-radius: 4px; padding: 8px 4px; text-align: center; min-width: 0; }
  .gx-v184 .tl184 b { display: block; font-size: 14px; font-weight: 700; color: #121212; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .gx-v184 .tl184 small { display: block; font-size: 12px; color: #666666; margin-top: 1px; }
  .gx-v184 .pb184 { width: 36px; height: 36px; border-radius: 99px; background: #2152d9; color: #ffffff; display: inline-flex; align-items: center; justify-content: center; }
  .gx-v184 .pb184 svg { width: 16px; height: 16px; margin-left: 2px; }
  .gx-v184 .ol184 { background: #ffffff; border-top: 1px solid #eeeeee; padding: 2px 14px 12px; overflow: hidden; animation: gx184-dn .22s ease-out; }
  .gx-v184 .ol184 .ol { margin-top: 8px; display: grid; grid-template-columns: minmax(0,1fr) minmax(0,1fr); gap: 4px 12px; font-size: 13px; color: #121212; }
  .gx-v184 .ol184 .ol .hd { grid-column: 1 / -1; color: #666666; font-size: 12px; padding: 0; margin: 0; border: 0; background: none; }
  .gx-v184 .ol184 .ol .tm { min-width: 0; }
  .gx-v184 .ol184 .ol .tn { font-weight: 700; margin-bottom: 2px; }
  .gx-v184 .ol184 .ol .pl { display: flex; align-items: center; gap: 6px; line-height: 1.6; min-width: 0; }
  .gx-v184 .ol184 .ol .pl > span { flex: 1; min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  .gx-v184 .ol184 .ol .pl button { color: inherit; }
  .gx-v184 .ol184 .ol .pl .tg { color: #666666; }
  .gx-v184 .ol184 .ol .pl b { font-weight: 700; width: 22px; text-align: right; flex: none; }
  @keyframes gx184-dn { from { opacity: 0; transform: translateY(-6px); } to { opacity: 1; transform: none; } }
  @media (max-width: 640px) {
    .gx-v184 .cd184 { grid-template-columns: 56px minmax(0,1fr) 36px; gap: 10px 8px; padding: 12px 10px; }
    .gx-v184 .cd184 .in184 { grid-column: 2 / 4; }
    .gx-v184 .cd184 .tl184 { grid-column: 1 / 3; grid-template-columns: repeat(3, minmax(0,1fr)); gap: 5px; }
    .gx-v184 .tl184 > div { padding: 8px 2px; }
    .gx-v184 .tl184 b { font-size: 13px; letter-spacing: -0.2px; }
    .gx-v184 .cd184.st184 { grid-template-columns: 56px minmax(0,1fr); }
    .gx-v184 .cd184.st184 .in184 { grid-column: 2 / 3; }
    .gx-v184 .cd184.st184 .tl184 { grid-column: 1 / -1; }
    .gx-v184 .ct184 { padding: 0 8px 8px; }
  }
  .gx-gv169 .gx-v184 { margin-top: 2px; }
</style>'''

HELPERS = r'''// ---------- change 184: Goal Visualizer drawn like NHL.com's EDGE Goal Visualizer (install.py) ----------
const GX_RED184 = "#cc3333", GX_BLUE184 = "#3366cc";
const gxBig184 = () => { try { return window.matchMedia("(max-width: 640px)").matches; } catch (e) { return false; } };
let GX_ICE184 = null;
function gxIce184() {
  // faint skate marks on white, made once and kept
  if (GX_ICE184 !== null) return GX_ICE184;
  try {
    const c = document.createElement("canvas"); c.width = 1000; c.height = 425;
    const x = c.getContext("2d");
    x.fillStyle = "#fbfbfb"; x.fillRect(0, 0, 1000, 425);
    let sd = 7;
    const rnd = () => { sd = (sd * 16807) % 2147483647; return sd / 2147483647; };
    for (let i = 0; i < 900; i++) {
      const a = rnd() * 1000, b = rnd() * 425, r = 20 + rnd() * 160, s = rnd() * 6.3, l = 0.15 + rnd() * 0.6;
      x.strokeStyle = "rgba(120,130,140," + (0.025 + rnd() * 0.05).toFixed(3) + ")";
      x.lineWidth = 0.5 + rnd() * 0.9;
      x.beginPath(); x.arc(a, b, r, s, s + l); x.stroke();
    }
    GX_ICE184 = c.toDataURL("image/jpeg", 0.8);
  } catch (e) { GX_ICE184 = ""; }
  return GX_ICE184;
}
const gxLogo184 = (t) => "https://assets.nhle.com/logos/nhl/svg/" + (NHL_LOGO[gxAb131(t)] || gxAb131(t)) + "_light.svg";
// the rink in feet (x -100..100, y -42.5..42.5); L / R = team code at each end, H = home team for centre ice
function gxRink184({ L, R, H, id }) {
  const red = GX_RED184, blue = GX_BLUE184, cp = "gxb184" + id, ice = gxIce184(), out = [];
  out.push(<defs key="df"><clipPath id={cp}><rect x="-100" y="-42.5" width="200" height="85" rx="28" ry="28" /></clipPath></defs>);
  out.push(<rect key="ice" x="-100" y="-42.5" width="200" height="85" rx="28" ry="28" fill="#fbfbfb" />);
  const g = [];
  if (ice) g.push(<image key="im" href={ice} x="-100" y="-42.5" width="200" height="85" preserveAspectRatio="none" />);
  // trapezoids behind the nets and the goal lines
  [-1, 1].forEach((s) => {
    g.push(<path key={"tz" + s} d={"M " + s * 89 + " -11 L " + s * 100 + " -14 M " + s * 89 + " 11 L " + s * 100 + " 14"} stroke={red} strokeWidth="0.25" fill="none" />);
    g.push(<line key={"gl" + s} x1={s * 89} y1="-42.5" x2={s * 89} y2="42.5" stroke={red} strokeWidth="0.25" />);
    g.push(<path key={"cr" + s} d={"M " + s * 89 + " -4 L " + s * 84.5 + " -4 A 4.5 4.5 0 0 " + (s > 0 ? 0 : 1) + " " + s * 84.5 + " 4 L " + s * 89 + " 4 Z"} fill="rgba(51,102,204,.16)" stroke={red} strokeWidth="0.25" />);
    g.push(<path key={"nt" + s} d={"M " + s * 89 + " -3 L " + s * 91.5 + " -3 Q " + s * 93.3 + " -3 " + s * 93.3 + " -1.2 L " + s * 93.3 + " 1.2 Q " + s * 93.3 + " 3 " + s * 91.5 + " 3 L " + s * 89 + " 3"} fill="#ffffff" stroke={red} strokeWidth="0.35" />);
    g.push(<rect key={"bl" + s} x={s * 25 - 0.5} y="-42.5" width="1" height="85" fill={blue} />);
  });
  // centre red line (dashed), centre circle, referee crease
  g.push(<rect key="rl" x="-0.5" y="-42.5" width="1" height="85" fill={red} />);
  for (let y = -41; y < 42; y += 3.4) g.push(<rect key={"rd" + y} x="-0.2" y={y} width="0.4" height="1.5" fill="#ffffff" />);
  g.push(<path key="rc" d="M -10 42.5 A 10 10 0 0 1 10 42.5" fill="none" stroke={red} strokeWidth="0.25" />);
  // end-zone faceoff circles with hash marks and the L marks around each dot
  [[-69, -22], [-69, 22], [69, -22], [69, 22]].forEach(([a, b], i) => {
    const k = "fo" + i, hm = [];
    [-1, 1].forEach((v) => [-1, 1].forEach((h) => {
      hm.push("M " + (a + h * 2.875) + " " + (b + v * 14.7) + " L " + (a + h * 2.875) + " " + (b + v * 16.7));
      hm.push("M " + (a + h * 2) + " " + (b + v * 0.75) + " L " + (a + h * 6) + " " + (b + v * 0.75) + " M " + (a + h * 2) + " " + (b + v * 0.75) + " L " + (a + h * 2) + " " + (b + v * 3.75));
    }));
    g.push(<circle key={k + "c"} cx={a} cy={b} r="15" fill="none" stroke={red} strokeWidth="0.25" />);
    g.push(<path key={k + "h"} d={hm.join(" ")} fill="none" stroke={red} strokeWidth="0.25" />);
    g.push(<circle key={k + "d"} cx={a} cy={b} r="1" fill={red} />);
  });
  [[-20, -22], [-20, 22], [20, -22], [20, 22]].forEach(([a, b], i) => g.push(<circle key={"nz" + i} cx={a} cy={b} r="1" fill={red} />));
  // centre ice: home logo, then the blue circle and dot on top
  if (H) g.push(<image key="lg" href={gxLogo184(H)} x="-16.7" y="-16.7" width="33.4" height="33.4" preserveAspectRatio="xMidYMid meet" />);
  g.push(<circle key="cc" cx="0" cy="0" r="15" fill="none" stroke={blue} strokeWidth="0.25" />);
  g.push(<circle key="cd" cx="0" cy="0" r="0.5" fill={blue} />);
  // which team defends each end
  if (L) g.push(<text key="tl" transform="translate(-95.2 0) rotate(90)" textAnchor="middle" dominantBaseline="central" fontSize="5.3" fontWeight="700" fill="#121212">{L}</text>);
  if (R) g.push(<text key="tr" transform="translate(95.2 0) rotate(-90)" textAnchor="middle" dominantBaseline="central" fontSize="5.3" fontWeight="700" fill="#121212">{R}</text>);
  out.push(<g key="cl" clipPath={"url(#" + cp + ")"}>{g}</g>);
  out.push(<rect key="bd" x="-100" y="-42.5" width="200" height="85" rx="28" ry="28" fill="none" stroke="#c5c5c7" strokeWidth="0.3" />);
  return out;
}
// player circle colours: scoring team filled with its colour, the other team white with its colour as ring and number
function gxCols184(sc, ot) {
  const a = gxTC101(gxAb131(sc)) || "#2152d9", b = gxTC101(gxAb131(ot)) || "#121212";
  const la = gxLum169(a), lb = gxLum169(b);
  return { sc: { f: a, s: la > 0.8 ? "#121212" : a, t: la > 0.62 ? "#121212" : "#ffffff" }, ot: { f: "#ffffff", s: lb > 0.75 ? "#121212" : b, t: lb > 0.75 ? "#121212" : b } };
}
const GX_IC184 = {
  rep: <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><path d="M3.2 8a4.8 4.8 0 1 0 1.5-3.5" /><path d="M3 2.5v2.6h2.6" /></svg>,
  pau: <svg viewBox="0 0 16 16" fill="currentColor" aria-hidden="true"><rect x="4" y="3" width="2.6" height="10" rx="0.8" /><rect x="9.4" y="3" width="2.6" height="10" rx="0.8" /></svg>,
  ply: <svg viewBox="0 0 16 16" fill="currentColor" aria-hidden="true"><path d="M4.5 2.8v10.4c0 .6.6.9 1.1.6l8-5.2c.5-.3.5-.9 0-1.2l-8-5.2c-.5-.3-1.1 0-1.1.6z" /></svg>,
  gol: <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.6" aria-hidden="true"><circle cx="8" cy="8" r="5.2" /><circle cx="8" cy="8" r="1.6" fill="currentColor" stroke="none" /></svg>,
};
const gxT184 = (t) => { const m = String(t || "").split(":"); return m.length === 2 ? (m[0].length < 2 ? "0" : "") + m[0] + ":" + m[1] : String(t || ""); };
function gxDate184(d) {
  const m = String(d || "").match(/^(\d{4})-(\d{2})-(\d{2})/);
  if (!m) return "";
  try { return new Date(+m[1], +m[2] - 1, +m[3]).toLocaleDateString("en-US", { month: "long", day: "numeric", year: "numeric" }); } catch (e) { return ""; }
}
// the white card under the rink: photo, number, name (goals), team logo and assists (assists), Score / Time / Shot, blue replay button
function GxGvCard184({ x, g, tm, no, onPlay }) {
  const nm = (x.name && x.name.default) || "", p = gxFind131(tm, no, nm);
  const col = gxTC101(gxAb131(tm)) || "#2152d9", hs = gxHs141(x, p);
  const [bad, setBad] = useState(false);
  const A = gxAb131((g.awayTeam || {}).abbrev), H = gxAb131((g.homeTeam || {}).abbrev), as = +x.awayScore, hsc = +x.homeScore;
  const score = isNaN(as) || isNaN(hsc) ? "-" : as === hsc ? as + "-" + hsc + " Tied" : Math.max(as, hsc) + "-" + Math.min(as, hsc) + " " + (as > hsc ? A : H);
  const gN = x.gN184 != null ? x.gN184 : ((String(x.text184 || "").match(/Goal \((\d+)\)/) || [])[1]);
  const ast = (x.assists || []).map((q) => shortN((q.name && q.name.default) || "") + (q.n184 != null ? " (" + q.n184 + ")" : "")).join(", ");
  const lb = gxLum169(col);
  const shot = x.shot ? String(x.shot).replace(/\s*Shot$/i, "") : "-";
  return (
    <div className={"cd184" + (onPlay ? "" : " st184")}>
      <div className="fc184" style={{ background: col }}>{hs && !bad ? <img src={hs} alt="" loading="lazy" onError={() => setBad(true)} /> : <span>{(nm.split(" ").map((w) => w[0] || "").join("") || "?").slice(0, 2)}</span>}</div>
      <div className="in184">
        <div className="nm184">
          {no != null ? <span className="bg" style={{ background: col, color: lb > 0.62 ? "#121212" : "#ffffff", boxShadow: "0 0 0 1.5px #ffffff, 0 0 0 3px " + col }}>{no}</span> : null}
          <span className="tx">{p && window.__NAV ? <button type="button" onClick={() => window.__NAV.player(p)}>{nm}</button> : nm}{no != null ? " #" + no : ""}{gN != null ? <small>{" (" + gN + ")"}</small> : null}</span>
        </div>
        <div className="as184"><img src={gxLogo184(tm)} alt={gxAb131(tm)} loading="lazy" /><span>{ast || "Unassisted"}</span></div>
      </div>
      <div className="tl184">
        <div><b>{score}</b><small>Score</small></div>
        <div><b>{gxT184(x.timeInPeriod) + " (" + gxPer131(x.periodDescriptor) + ")"}</b><small>Time</small></div>
        <div><b>{shot || "-"}</b><small>Shot</small></div>
      </div>
      {onPlay ? <button type="button" className="pb184" aria-label="Play the goal again" onClick={onPlay}>{GX_IC184.ply}</button> : null}
    </div>
  );
}
'''

# the Goal Visualizer box: header, then the replay (or the still rink) and the card
NEW_RINK = r'''function GxRink163({ x, g, tm, s }) {
  /* change 184: drawn like NHL.com's Goal Visualizer */
  const e165 = useEdge165(x, g, tm); /* gx165 */
  const cx = +x.cx, cy = +x.cy;
  if ((isNaN(cx) || isNaN(cy)) && !e165) return null;
  const A = gxAb131((g.awayTeam || {}).abbrev), H = gxAb131((g.homeTeam || {}).abbrev), T = gxAb131(tm), O = T === H ? A : H;
  const nm = (x.name && x.name.default) || "";
  const head = <div className="hd184"><b>{gxNick141(A) + " @ " + gxNick141(H)}</b><small>{gxDate184(g.gameDate)}</small></div>;
  if (e165) return <div className="gx-rk163 gx-v184" data-gx="184">{head}<GxEdge165 key={e165.k} e={e165} s={s} x={x} g={g} tm={tm} /></div>;
  // still picture when NHL tracking is not saved for this goal: the scorer at the shot spot and the puck's path to the net
  const side = cx >= 0 ? 1 : -1, nx = side * 89, px = cx, py = -cy, no = gxPdNo({ t: T, n: nm });
  const C = gxCols184(T, O);
  return (
    <div className="gx-rk163 gx-v184" data-gx="184">
      {head}
      <div className="rw184">
        <svg viewBox="-106.25 -48.75 212.5 97.5" role="img" aria-label={"Goal by " + nm + " from the spot shown"}>
          {gxRink184({ L: side < 0 ? O : T, R: side > 0 ? O : T, H, id: "s" + (g.id || "") + (x.timeInPeriod || "") })}
          <line x1={px} y1={py} x2={nx} y2="0" stroke="#121212" strokeWidth="0.35" strokeDasharray="1.2 1" />
          <circle cx={nx} cy="0" r="1" fill="#121212" />
          <g transform={"translate(" + px + " " + py + ") scale(" + (gxBig184() ? 1.6 : 1) + ")"}>
            <circle r="4.17" fill="none" stroke={C.sc.f} strokeWidth="0.5" />
            <circle r="3.17" fill={C.sc.f} stroke={C.sc.s} strokeWidth="0.25" />
            <text y="0.1" textAnchor="middle" dominantBaseline="central" fontSize="3.33" fontWeight="900" fill={C.sc.t}>{no != null ? no : ""}</text>
          </g>
        </svg>
      </div>
      <GxGvCard184 x={x} g={g} tm={tm} no={no} onPlay={null} />
    </div>
  );
}
'''

NEW_EDGE = r'''function GxEdge165({ e, s, x, g, tm }) {
  /* change 184: NHL.com look; dots still moved directly each screen frame (172) */
  const F = e.F, fr = F.f || [], n = fr.length, gi = Math.max(0, Math.min(F.gi == null ? n - 1 : F.gi, n - 1));
  const D0 = n > 1 ? fr[n - 1][0] : 0, even = !(D0 > 2000 && D0 < 60000);
  const tOf = (k) => (even ? k * 100 : fr[k][0]);
  const T = n ? tOf(n - 1) : 0;
  const [ms, setMs] = useState(0);
  const [play, setPlay] = useState(true);
  const [run, setRun] = useState(0);
  const [ol166, setOl166] = useState(false);
  const [big, setBig] = useState(() => gxBig184());
  useEffect(() => { const f = () => setBig(gxBig184()); window.addEventListener("resize", f); return () => window.removeEventListener("resize", f); }, []);
  const k = big ? 1.6 : 1;
  const svg = React.useRef(null), cur = React.useRef(0);
  // every player who appears at any point, with his first spot
  const all = useMemo(() => {
    const m = {}, order = [];
    fr.forEach((f) => (f[1] || []).forEach((o) => { const id = o[0] ? String(o[0]) : "pk"; if (!m[id]) { m[id] = o; order.push(id); } }));
    // puck drawn last so it sits on top
    return order.filter((id) => id !== "pk").concat(m.pk ? ["pk"] : []).map((id) => [id, m[id]]);
  }, [F]);
  // where everyone is at a time (blended between the two nearest frames)
  const at = (t) => {
    let k = 0;
    while (k < n - 1 && tOf(k + 1) <= t) k++;
    const k2 = Math.min(n - 1, k + 1), span = tOf(k2) - tOf(k), fq = span > 0 ? Math.max(0, Math.min(1, (t - tOf(k)) / span)) : 0;
    const nx = {}, out = {};
    ((fr[k2] || [0, []])[1]).forEach((o) => { nx[o[0] ? String(o[0]) : "pk"] = o; });
    ((fr[k] || [0, []])[1]).forEach((o) => { const id = o[0] ? String(o[0]) : "pk", b = nx[id]; out[id] = b ? [o[3] + (b[3] - o[3]) * fq, o[4] + (b[4] - o[4]) * fq] : [o[3], o[4]]; });
    return out;
  };
  const paint = (t) => {
    const el = svg.current;
    if (!el) return;
    const P = at(t);
    el.querySelectorAll("[data-p]").forEach((q) => {
      const v = P[q.getAttribute("data-p")];
      if (v) { q.setAttribute("transform", "translate(" + v[0].toFixed(2) + " " + v[1].toFixed(2) + ")"); q.style.display = ""; } else q.style.display = "none";
    });
  };
  useEffect(() => { cur.current = ms; paint(ms); }, [ms, F]);
  useEffect(() => {
    if (!play || n < 2) return undefined;
    let raf = 0;
    const t0 = performance.now() - cur.current;
    const step = (now) => {
      const m = Math.min(T, now - t0);
      cur.current = m;
      paint(m);
      if (m >= T) { setMs(T); setPlay(false); return; }
      raf = requestAnimationFrame(step);
    };
    raf = requestAnimationFrame(step);
    return () => { cancelAnimationFrame(raf); };
  }, [play, run]);
  if (!n) return null;
  const P0 = at(ms);
  const scT = e.v.team || F.team, ro = F.ro || {};
  const gRow = ((fr[gi] || [0, []])[1]).filter((o) => o[0]);
  const code = String(F.sc || e.v.sc || ""), scHome = scT === (F.home || e.v.home);
  const mySk = +(scHome ? code[2] : code[1]), opSk = +(scHome ? code[1] : code[2]);
  const pp = code.length === 4 && mySk > opSk;
  const isG = (o) => ((ro[o[0]] || [])[1] || "") === "G";
  const gA = gxAb131(((g || {}).awayTeam || {}).abbrev), gH = gxAb131(((g || {}).homeTeam || {}).abbrev);
  const otT = [...new Set(gRow.map((o) => o[1]))].find((t) => t !== scT) || (scT === gH ? gA : gH);
  const teams = [scT, otT].filter(Boolean);
  const C = gxCols184(scT, otT);
  const pk = ((fr[gi] || [0, []])[1]).find((o) => !o[0]);
  const side = pk ? (pk[3] >= 0 ? 1 : -1) : (+x.cx || 0) >= 0 ? 1 : -1;
  const stopAt = (t) => { setPlay(false); cur.current = t; setMs(t); };
  const replay = () => { cur.current = 0; setMs(0); setPlay(true); setRun((r) => r + 1); };
  const scNo = F.scorer && ro[F.scorer] ? ro[F.scorer][2] : gxPdNo({ t: scT, n: (x.name && x.name.default) || "" });
  return (
    <div className="gx-ed165" data-gx="172">
      <svg ref={svg} viewBox="-106.25 -48.75 212.5 97.5" role="img" aria-label="Goal replay with every player on the ice">
        {gxRink184({ L: side < 0 ? otT : scT, R: side > 0 ? otT : scT, H: gH || F.home, id: e.k })}
        {all.map(([id, o]) => {
          const q = P0[id], tr = q ? "translate(" + q[0].toFixed(2) + " " + q[1].toFixed(2) + ")" : "translate(0 0)", hide = q ? null : { display: "none" };
          if (id === "pk") return <g key="pk" data-p="pk" transform={tr} style={hide}><circle r={1 * k} fill="#121212" stroke="#121212" strokeWidth="0.25" /></g>;
          const c = o[1] === scT ? C.sc : C.ot, sc = F.scorer && id === String(F.scorer);
          return (
            <g key={"p" + id} data-p={id} transform={tr} style={hide}><g transform={"scale(" + k + ")"}>
              {sc ? <circle r="4.17" fill="none" stroke={C.sc.f} strokeWidth="0.5" data-gx="170" /> : null}
              <circle r="3.17" fill={c.f} stroke={c.s} strokeWidth="0.25" />
              <text y="0.1" textAnchor="middle" dominantBaseline="central" fontSize="3.33" fontWeight="900" fill={c.t}>{o[2]}</text>
            </g></g>
          );
        })}
      </svg>
      <div className="ct184">
        <button type="button" className="ib" onClick={replay} aria-label="Replay" title="Replay">{GX_IC184.rep}</button>
        <button type="button" className="ib" onClick={() => { if (play) { stopAt(cur.current); } else { if (cur.current >= T) { cur.current = 0; setMs(0); } setPlay(true); setRun((r) => r + 1); } }} aria-label={play ? "Pause" : "Play"} title={play ? "Pause" : "Play"}>{play ? GX_IC184.pau : GX_IC184.ply}</button>
        <button type="button" className="ib" onClick={() => stopAt(tOf(gi))} aria-label="Goal moment" title="Goal moment">{GX_IC184.gol}</button>
        <button type="button" className="oi184" onClick={() => setOl166(!ol166)}>On ice <i className={ol166 ? "up" : ""}>{"\u25be"}</i></button>
      </div>
      <GxGvCard184 x={x} g={g || {}} tm={tm || scT} no={scNo} onPlay={replay} />
      {ol166 ? <div className="ol184"><div className="ol">
        <div className="hd">On the ice at the goal{pp ? " (power play, no plus/minus)" : ""}</div>
        {teams.map((t) => (
          <div key={t} className="tm"><div className="tn">{t + (t === scT ? " (scored)" : "")}</div>
            {gRow.filter((o) => o[1] === t).sort((a, b) => (isG(a) ? 1 : 0) - (isG(b) ? 1 : 0) || a[2] - b[2]).map((o) => {
              const r = ro[o[0]] || [], nm = r[0] || "#" + o[2], p = gxFind131(t, o[2], nm), tag = gxTag131(s, p);
              const pm = isG(o) || pp || code.length !== 4 ? "" : t === scT ? "+1" : "-1";
              return <div key={o[0]} className="pl"><span>{"#" + o[2] + " "}{p && window.__NAV ? <button type="button" className="hover:underline" onClick={() => window.__NAV.player(p)}>{shortN(nm)}</button> : shortN(nm)}{isG(o) ? " (G)" : ""}{tag ? <span className="tg">{" (" + tag + ")"}</span> : null}</span><b>{pm}</b></div>;
            })}
          </div>
        ))}
      </div></div> : null}
    </div>
  );
}
'''

OLD_LAND = r'''cy: e.coordinate ? e.coordinate.y : null, shot:'''
NEW_LAND = r'''cy: e.coordinate ? e.coordinate.y : null, gN184: sco.ytdGoals != null ? sco.ytdGoals : ((String(e.text || "").match(/Goal \((\d+)\)/) || [])[1]), shot:'''
OLD_AST = r'''.map((p) => ({ name: { default: (p.athlete || {}).displayName || "" } })) });'''
NEW_AST = r'''.map((p) => ({ name: { default: (p.athlete || {}).displayName || "" }, n184: p.ytdAssists != null ? p.ytdAssists : gxAstN184(e.text, (p.athlete || {}).displayName) })) });'''
AST_FN = r'''const gxAstN184 = (tx, nm) => { const i = String(tx || "").indexOf(String(nm || "") + " ("); if (!nm || i < 0) return null; const m = String(tx).slice(i + String(nm).length).match(/^ \((\d+)\)/); return m ? +m[1] : null; }; /* change 184 */
function gxLanding132(sm) {'''


def cut(t, label, start, end, new, done):
    if done in t:
        print("(install) " + label + ": already done")
        return t
    i = t.find(start)
    if i < 0 or t.find(start, i + 1) >= 0:
        fail(label + ": start text not found exactly once")
    j = t.find(end, i)
    if j < 0:
        fail(label + ": end text not found")
    print("(install) " + label + ": updated")
    return t[:i] + new + t[j:]


def change(t):
    t = lit(t, "184: styles", "</style>", NEW_CSS, "change 184 (install.py)")
    t = lit(t, "184: helpers", ROOT, HELPERS + ROOT, "change 184: Goal Visualizer drawn like")
    t = lit(t, "184: goal totals", OLD_LAND, NEW_LAND, "gN184: sco.ytdGoals")
    t = lit(t, "184: assist totals", OLD_AST, NEW_AST, "n184: p.ytdAssists")
    t = lit(t, "184: assist totals from text", "function gxLanding132(sm) {", AST_FN, "const gxAstN184 =")
    t = cut(t, "184: visualizer box", "function GxRink163({ x, g, tm, s }) {", "// ---------- change 165:", NEW_RINK, "change 184: drawn like NHL.com")
    t = cut(t, "184: replay", "function GxEdge165({ e, s, x", "// ---------- change 169:", NEW_EDGE, "change 184: NHL.com look")
    return t


edit(APP, change)
