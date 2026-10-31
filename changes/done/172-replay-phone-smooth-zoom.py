# changes/172-replay-phone-smooth-zoom.py - goal replay: moves the dots directly each screen frame (no full redraw, smooth on phones), and on the phone it zooms to the half of the rink where the goal happened (button to see the full rink)

NEW_EDGE = r'''function GxEdge165({ e, s, x }) {
  /* change 172: dots moved directly (no redraw each frame), phone zooms to the goal half */
  const F = e.F, fr = F.f || [], n = fr.length, gi = Math.max(0, Math.min(F.gi == null ? n - 1 : F.gi, n - 1));
  const D0 = n > 1 ? fr[n - 1][0] : 0, even = !(D0 > 2000 && D0 < 60000);
  const tOf = (k) => (even ? k * 100 : fr[k][0]);
  const T = n ? tOf(n - 1) : 0;
  const [ms, setMs] = useState(0);
  const [play, setPlay] = useState(true);
  const [run, setRun] = useState(0);
  const [ol166, setOl166] = useState(false);
  const [zoom, setZoom] = useState(() => { try { return window.matchMedia("(max-width: 640px)").matches; } catch (er) { return false; } });
  const svg = React.useRef(null), cur = React.useRef(0);
  // every player who appears at any point, with his first spot
  const all = useMemo(() => {
    const m = {}, order = [];
    fr.forEach((f) => (f[1] || []).forEach((o) => { const id = o[0] ? String(o[0]) : "pk"; if (!m[id]) { m[id] = o; order.push(id); } }));
    return order.map((id) => [id, m[id]]);
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
    el.querySelectorAll("[data-p]").forEach((g) => {
      const q = P[g.getAttribute("data-p")];
      if (q) { g.setAttribute("transform", "translate(" + q[0].toFixed(2) + " " + q[1].toFixed(2) + ")"); g.style.display = ""; } else g.style.display = "none";
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
  const teams = [scT].concat([...new Set(gRow.map((o) => o[1]))].filter((t) => t !== scT));
  const C169 = gxPair169(scT, teams[1] || ""); /* gx169 */
  const pk = ((fr[gi] || [0, []])[1]).find((o) => !o[0]);
  const side = pk ? (pk[3] >= 0 ? 1 : -1) : (+x.cx || 0) >= 0 ? 1 : -1;
  const vb = zoom ? (side > 0 ? "-4 -45 106 90" : "-102 -45 106 90") : "-102 -45 204 90";
  const stopAt = (t) => { setPlay(false); cur.current = t; setMs(t); };
  return (
    <div className={"gx-ed165" + (zoom ? " z172" : "")} data-gx="172">
      <svg ref={svg} viewBox={vb} role="img" aria-label="Goal replay with every player on the ice">
        {gxRinkBg165()}
        {all.map(([id, o]) => {
          const q = P0[id], tr = q ? "translate(" + q[0].toFixed(2) + " " + q[1].toFixed(2) + ")" : "translate(0 0)", hide = q ? null : { display: "none" };
          if (id === "pk") return <g key="pk" data-p="pk" transform={tr} style={hide}><circle cx="0" cy="0" r="1.5" className="pk" /></g>;
          const c = o[1] === scT ? C169.sc : C169.ot, sc = F.scorer && id === String(F.scorer);
          return (
            <g key={"p" + id} data-p={id} transform={tr} style={hide}>
              {sc ? <><circle cx="0" cy="0" r="5.6" fill="none" stroke="#111111" strokeWidth="0.35" opacity=".6" /><circle cx="0" cy="0" r="5.2" fill="none" stroke={C169.sc.f} strokeWidth="1" data-gx="170" /></> : null}
              <circle cx="0" cy="0" r="3.7" className="t169" style={gxCol169(c, 0)} />
              <text x="0" y="1.25" textAnchor="middle" fontSize="3.4" className="t169" style={gxCol169(c, 1)}>{o[2]}</text>
            </g>
          );
        })}
      </svg>
      <div className="ct">
        <button type="button" onClick={() => { cur.current = 0; setMs(0); setPlay(true); setRun((r) => r + 1); }} aria-label="Replay">{"↻"}</button>
        <button type="button" onClick={() => { if (play) { stopAt(cur.current); } else { if (cur.current >= T) { cur.current = 0; setMs(0); } setPlay(true); setRun((r) => r + 1); } }}>{play ? "Pause" : "Play"}</button>
        <button type="button" onClick={() => stopAt(tOf(gi))}>Goal moment</button>
        <button type="button" className="zm172" onClick={() => setZoom(!zoom)}>{zoom ? "Full rink" : "Zoom"}</button>
        <span className="lg"><i style={{ background: C169.sc.f, boxShadow: "inset 0 0 0 1.5px " + C169.sc.s }}></i>{scT}<i style={{ background: C169.ot.f, boxShadow: "inset 0 0 0 1.5px " + C169.ot.s }}></i>{teams[1] || ""}</span>
      </div>
      <button type="button" className="dd166" onClick={() => setOl166(!ol166)}>Who was on the ice <i className={ol166 ? "up" : ""}>{"▾"}</i></button>
      <div className="ol" style={ol166 ? null : { display: "none" }}>
        <div className="hd">On the ice at the goal{pp ? " (power play, no plus/minus)" : ""}</div>
        {teams.map((t) => (
          <div key={t} className="tm"><div className="tn">{t + (t === scT ? " (scored)" : "")}</div>
            {gRow.filter((o) => o[1] === t).sort((a, b) => (isG(a) ? 1 : 0) - (isG(b) ? 1 : 0) || a[2] - b[2]).map((o) => {
              const r = ro[o[0]] || [], nm = r[0] || "#" + o[2], p = gxFind131(t, o[2], nm), tag = gxTag131(s, p);
              const pm = isG(o) || pp || code.length !== 4 ? "" : t === scT ? "+1" : "-1";
              return <div key={o[0]} className="pl"><span className="truncate">{"#" + o[2] + " "}{p && window.__NAV ? <button type="button" className="hover:underline" onClick={() => window.__NAV.player(p)}>{shortN(nm)}</button> : shortN(nm)}{isG(o) ? " (G)" : ""}{tag ? <span className="tg">{" (" + tag + ")"}</span> : null}</span><b>{pm}</b></div>;
            })}
          </div>
        ))}
      </div>
    </div>
  );
}
'''

NEW_CSS = r'''  /* change 172 (install.py) */
  .gx-ed165 svg { overflow: hidden; }
  .gx-ed165 svg g[data-p] { will-change: transform; }
  .gx-ed165 .ct .zm172 { display: none; }
  @media (max-width: 640px) {
    .gx-ed165 .ct .zm172 { display: inline-block; }
    .gx-ed165 .ct { gap: 5px; }
    .gx-ed165 .ct button { padding: 6px 9px; font-size: 13px; }
    .gx-ed165 .ct .lg { width: 100%; justify-content: flex-end; margin-left: 0; }
  }
</style>'''


def cut(t, label, start, end, new, done):
    if done in t:
        print("(install) " + label + ": already done")
        return t
    a = t.find(start)
    if a < 0 or t.count(start) != 1:
        fail(label + ": start text not found exactly once")
    b = t.find(end, a)
    if b < 0:
        fail(label + ": end text not found")
    print("(install) " + label + ": updated")
    return t[:a] + new + t[b + len(end):]


def app(t):
    t = lit(t, "172: styles", "</style>", NEW_CSS, "change 172 (install.py)")
    t = cut(t, "172: smooth replay", "function GxEdge165({ e, s, x }) {\n", "\n  );\n}\n", NEW_EDGE, "change 172: dots moved directly")
    return t


edit(APP, app)
