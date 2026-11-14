# changes/264-live-puck-tracker.py - NHL scores game view: live tracker like bet365, the puck glides to each new ESPN play on the rink (live games); finished games keep the 263 shot map

NEW_CSS = r'''  /* change 264 (install.py) */
  .gx-tk264 { padding: 4px 16px 10px; }
  .gx-tk264 .hd264 { display: flex; justify-content: space-between; align-items: center; gap: 10px; font-size: 13px; font-weight: 700; letter-spacing: .04em; padding: 10px 0 8px; }
  .gx-tk264 .ck264 { font-size: 13px; font-weight: 700; font-variant-numeric: tabular-nums; padding: 3px 9px; border-radius: 7px; background: var(--card2, #1d1f24); color: var(--ink); letter-spacing: 0; }
  .gx-tk264 .rw264 { border-radius: 12px; overflow: hidden; }
  .gx-tk264 .rw264 svg { width: 100%; height: auto; display: block; }
  .gx-tk264 .pk264 { transition: transform .75s cubic-bezier(.4, 0, .2, 1); }
  .gx-tk264 .zn264 { transition: opacity .5s; }
  .gx-tk264 .ev264 { display: flex; align-items: center; gap: 10px; min-height: 46px; padding: 8px 2px 0; }
  .gx-tk264 .tg264 { flex: 0 0 auto; min-width: 42px; text-align: center; font-size: 12px; font-weight: 800; padding: 4px 6px; border-radius: 6px; }
  .gx-tk264 .tx264 { min-width: 0; flex: 1 1 auto; }
  .gx-tk264 .tx264 b { display: block; font-size: 14px; color: var(--ink); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .gx-tk264 .tx264 span { display: block; font-size: 12px; color: var(--mute); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; height: 16px; }
  @media (prefers-reduced-motion: reduce) { .gx-tk264 .pk264 { transition: none; } }
</style>'''

HELPERS = r'''// ---------- change 264: live puck tracker on the NHL game view (install.py) ----------
// like bet365's tracker: ESPN play-by-play events in order, the puck glides from one event spot to the next
function gxTk264(sm) {
  const hc = gxHead132(sm), A = { id: "", ab: "" }, H = { id: "", ab: "" };
  (hc.competitors || []).forEach((x) => {
    const o = x.homeAway === "home" ? H : A, tm = x.team || {};
    o.id = String(tm.id || ""); o.ab = gxAb131(gxAb132(tm.abbreviation));
  });
  const st = hc.status || {}, ev = [];
  ((sm || {}).plays || []).forEach((e) => {
    const c = e.coordinate, ok = c && c.x != null && c.y != null && !isNaN(+c.x) && !isNaN(+c.y);
    const tid = String(((e.team || {}).id) || "");
    ev.push({ k: String(e.id || ev.length), ty: String((e.type || {}).text || ""), tx: String(e.text || ""), t: tid && tid === H.id ? "h" : tid && tid === A.id ? "a" : "",
      x: ok ? +c.x : null, y: ok ? +c.y : null, goal: !!e.scoringPlay || /^goal/i.test(String((e.type || {}).text || "")),
      per: ((e.period || {}).number) || 0, clk: ((e.clock || {}).displayValue) || "" });
  });
  return { ev, A: A.ab, H: H.ab, per: st.period || 0, clk: st.displayClock || "" };
}
function GxTrack264({ id, g }) {
  const live = !!(g && (g.gameState === "LIVE" || g.gameState === "CRIT"));
  if (!live) return <GxShotMap263 id={id} g={g} />;
  return <GxTkLive264 id={id} />;
}
function GxTkLive264({ id }) {
  const [d, setD] = useState(null);
  const [i, setI] = useState(-1);
  useEffect(() => {
    let on = true;
    const pull = () => gxSum132(id).then((sm) => { if (on && sm) setD(gxTk264(sm)); }).catch(() => {});
    pull();
    const t = setInterval(pull, 2000);
    return () => { on = false; clearInterval(t); };
  }, [id]);
  const n = d ? d.ev.length : 0;
  // step through new events one at a time (0.9 s each); if far behind, skip ahead to the last 5
  useEffect(() => {
    if (!n) return;
    if (i < 0 || i < n - 6) { setI(Math.max(0, n - 1 - (i < 0 ? 0 : 5))); return; }
    if (i >= n - 1) return;
    const t = setTimeout(() => setI((v) => Math.min(n - 1, v + 1)), 900);
    return () => clearTimeout(t);
  }, [n, i]);
  if (!d) return null;
  const A = d.A || "AWAY", H = d.H || "HOME";
  const cA = gxCols184(A, H).sc, cH = gxCols184(H, A).sc;
  const col = (t) => (t === "h" ? cH : t === "a" ? cA : null);
  const k = Math.min(Math.max(i, 0), n - 1), e = n ? d.ev[k] : null;
  // puck: spot of the latest event up to now that has one
  let p = null; const trail = [];
  for (let j = k; j >= 0 && (!p || trail.length < 4); j--) {
    const q = d.ev[j];
    if (q.x == null) continue;
    if (!p) p = q; else trail.push(q);
  }
  // attacking zone: the team of the latest event with a spot, in the end where it happened
  const zs = p && p.t && Math.abs(p.x) > 25 ? (p.x > 0 ? 1 : -1) : 0, zc = p ? col(p.t) : null;
  const cp = "url(#gxb184tk264" + id + (gxDk186() ? "d" : "") + ")";
  const ec = e ? col(e.t) : null;
  const clock = d.per ? (d.per > 3 ? "OT" : "P" + d.per) + " " + d.clk : "";
  return (
    <div className="gx-tk264" data-gx="264">
      <div className="hd264"><span>Live tracker</span>{clock ? <span className="ck264">{clock}</span> : null}</div>
      <div className="rw264">
        <svg viewBox="-106.25 -48.75 212.5 97.5" role="img" aria-label="Live tracker">
          {gxRink184({ L: A, R: H, H, id: "tk264" + id })}
          <g clipPath={cp}><rect className="zn264" x={zs > 0 ? 25 : -100} y="-42.5" width="75" height="85" fill={zc ? zc.f : "#888"} opacity={zs && zc ? 0.22 : 0} /></g>
          {trail.map((q, j) => <circle key={q.k} cx={q.x} cy={-q.y} r={1.3} fill={col(q.t) ? col(q.t).f : "#9a9a9a"} opacity={0.55 - j * 0.12} />)}
          {p ? (
            <g className="pk264" style={{ transform: "translate(" + p.x + "px, " + -p.y + "px)" }}>
              {e && e.goal ? <circle r="6" fill="none" stroke={ec ? ec.f : "#fff"} strokeWidth="0.8" opacity="0.8" /> : null}
              <circle r="3.2" fill={zc ? zc.f : "#888"} opacity="0.35" />
              <circle r="1.7" fill="#111" stroke="#fff" strokeWidth="0.55" />
            </g>
          ) : null}
        </svg>
      </div>
      <div className="ev264">
        {e ? <span className="tg264" style={{ background: ec ? ec.f : "var(--line)", color: ec ? ec.t : "var(--ink)" }}>{e.t === "h" ? H : e.t === "a" ? A : "NHL"}</span> : null}
        <div className="tx264">
          <b>{e ? (e.goal ? "GOAL" : e.ty || "Play") : "Waiting for the first play"}</b>
          <span>{e ? e.tx : ""}</span>
        </div>
      </div>
    </div>
  );
}
'''

def change(t):
    t = lit(t, "264: styles", "</style>", NEW_CSS, "change 264 (install.py)")
    t = lit(t, "264: helpers", ROOT, HELPERS + ROOT, "change 264: live puck tracker")
    t = lit(t, "264: tracker in the game view", "<GxShotMap263 id={gid} g={g} />", "<GxTrack264 id={gid} g={g} />", "<GxTrack264 id={gid} g={g} />")
    return t

edit(APP, change)
