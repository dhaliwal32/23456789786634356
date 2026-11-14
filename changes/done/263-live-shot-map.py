# changes/263-live-shot-map.py - NHL scores game view: a live shot map on a rink (every shot, goal and miss from ESPN, updates every 2 s while the game is live)

NEW_CSS = r'''  /* change 263 (install.py) */
  .gx-sm263 { padding: 4px 16px 10px; }
  .gx-sm263 .hd263 { display: flex; justify-content: space-between; align-items: baseline; gap: 10px; font-size: 13px; font-weight: 700; letter-spacing: .04em; padding: 10px 0 8px; }
  .gx-sm263 .hd263 small { font-size: 12px; font-weight: 500; color: var(--mute); letter-spacing: 0; }
  .gx-sm263 .rw263 { border-radius: 12px; overflow: hidden; }
  .gx-sm263 .rw263 svg { width: 100%; height: auto; display: block; }
  .gx-sm263 .lg263 { display: flex; flex-wrap: wrap; gap: 6px 14px; font-size: 12px; color: var(--mute); padding: 8px 2px 0; }
  .gx-sm263 .lg263 i { display: inline-block; width: 9px; height: 9px; border-radius: 50%; margin-right: 5px; vertical-align: 0; }
  .gx-sm263 .em263 { font-size: 13px; color: var(--mute); padding: 6px 0 4px; }
</style>'''

HELPERS = r'''// ---------- change 263: live shot map on the NHL game view (install.py) ----------
// shots, goals and misses with ESPN's spot on the rink, from the game summary plays (same feed as the goal tracker)
function gxShots263(sm) {
  const hc = gxHead132(sm), A = { id: "", ab: "" }, H = { id: "", ab: "" };
  (hc.competitors || []).forEach((x) => {
    const o = x.homeAway === "home" ? H : A, tm = x.team || {};
    o.id = String(tm.id || ""); o.ab = gxAb131(gxAb132(tm.abbreviation));
  });
  const pts = [];
  ((sm || {}).plays || []).forEach((e) => {
    const c = e.coordinate; if (!c || c.x == null || c.y == null || isNaN(+c.x) || isNaN(+c.y)) return;
    const ty = String((e.type || {}).text || e.text || "");
    let k = "";
    if (e.scoringPlay || /^goal/i.test(ty)) k = "goal";
    else if (/blocked/i.test(ty)) k = "blk";
    else if (/missed/i.test(ty)) k = "miss";
    else if (/shot|save/i.test(ty)) k = "sog";
    if (!k) return;
    const tid = String(((e.team || {}).id) || "");
    pts.push({ k, t: tid && tid === H.id ? "h" : tid && tid === A.id ? "a" : "", x: +c.x, y: +c.y });
  });
  return { pts, A: A.ab, H: H.ab };
}
function GxShotMap263({ id, g }) {
  const [d, setD] = useState(null);
  const live = !!(g && g.gameState === "LIVE");
  useEffect(() => {
    let on = true, t = 0;
    const pull = () => gxSum132(id).then((sm) => { if (on && sm) setD(gxShots263(sm)); }).catch(() => {});
    pull();
    if (live) t = setInterval(pull, 2000);
    return () => { on = false; if (t) clearInterval(t); };
  }, [id, live]);
  if (!d) return null;
  const A = d.A || "AWAY", H = d.H || "HOME";
  const cA = gxCols184(A, H).sc, cH = gxCols184(H, A).sc;
  const colr = (t) => (t === "h" ? cH.f : cA.f);
  const n = (t, k) => d.pts.filter((p) => p.t === t && (p.k === "sog" || p.k === "goal")).length;
  const sA = n("a"), sH = n("h");
  const dots = d.pts.map((p, i) => {
    const tr = "translate(" + p.x + " " + -p.y + ")";
    if (p.k === "blk") return <g key={i} transform={tr}><circle r="1.1" fill="#8a8a8a" /></g>;
    if (p.k === "miss") return <g key={i} transform={tr}><circle r="1.5" fill="none" stroke={colr(p.t)} strokeWidth="0.45" /></g>;
    if (p.k === "goal") return <g key={i} transform={tr}><circle r="3.4" fill={colr(p.t)} stroke="#ffffff" strokeWidth="0.45" /></g>;
    return <g key={i} transform={tr}><circle r="1.9" fill={colr(p.t)} /></g>;
  });
  return (
    <div className="gx-sm263" data-gx="263">
      <div className="hd263"><span>Shot map</span><small>{A} {sA} · {H} {sH} shots on goal</small></div>
      {d.pts.length ? (
        <div className="rw263">
          <svg viewBox="-106.25 -48.75 212.5 97.5" role="img" aria-label="Shot map">
            {gxRink184({ L: A, R: H, H, id: "sm263" + id })}
            {dots}
          </svg>
        </div>
      ) : <div className="em263">{live ? "Shots will appear here as ESPN posts their spot." : "No shot locations for this game."}</div>}
      {d.pts.length ? (
        <div className="lg263">
          <span><i style={{ background: cA.f }}></i>{A} shot</span>
          <span><i style={{ background: cH.f }}></i>{H} shot</span>
          <span><i style={{ background: "#ffffff", border: "2px solid #121212", boxSizing: "border-box" }}></i>Goal (bigger dot)</span>
          <span><i style={{ background: "#8a8a8a" }}></i>Blocked</span>
        </div>
      ) : null}
    </div>
  );
}
'''

def change(t):
    t = lit(t, "263: styles", "</style>", NEW_CSS, "change 263 (install.py)")
    t = lit(t, "263: helpers", ROOT, HELPERS + ROOT, "change 263: live shot map")
    t = lit(t, "263: show the map above the scoring",
            'body = gs.length ? <div className="gx-sc141"><div className="h1">SCORING</div>',
            'body = <>{/* change 263 */}<GxShotMap263 id={gid} g={g} />{gs.length ? <div className="gx-sc141"><div className="h1">SCORING</div>',
            "<GxShotMap263 id={gid} g={g} />")
    t = lit(t, "263: close the fragment",
            '{pre(g) ? "Not started yet." : "No goals yet."}</div>;',
            '{pre(g) ? "Not started yet." : "No goals yet."}</div>}</>;',
            "No goals yet.\"}</div>}</>;")
    return t

edit(APP, change)
