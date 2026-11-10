# changes/252-roster-graph-side.py - Roster box: the Games side becomes a Graph side, projection vs actual for both teams

NEW_CSS = r'''  /* change 252 (install.py) */
  .gx-bx226 .fc.gf252 { display: flex; flex-direction: column; }
  .gf252 .sg252 { display: inline-flex; gap: 2px; padding: 2px; border-radius: 8px; background: var(--card3, var(--hover)); }
  .gf252 .sg252 button { height: 26px; padding: 0 10px; border: 0; border-radius: 6px; background: none; color: var(--mute); font-size: 11.5px; white-space: nowrap; }
  .gf252 .sg252 button.on { background: var(--card); color: var(--ink); font-weight: 600; box-shadow: 0 1px 2px rgba(0,0,0,.25); }
  .gf252 .lg252 { display: flex; gap: 12px; margin-top: 8px; font-size: 11px; color: var(--mute); white-space: nowrap; overflow: hidden; }
  .gf252 .lg252 span { display: inline-flex; align-items: center; gap: 5px; min-width: 0; }
  .gf252 .lg252 i { display: inline-block; width: 14px; height: 9px; border-radius: 2px; flex: none; }
  .gf252 .lg252 em { display: inline-block; width: 14px; border-top: 2px dotted var(--mute); flex: none; }
  .gf252 .ch252 { position: relative; flex: 1 1 auto; min-height: 120px; margin-top: 4px; }
  .gf252 .ch252 svg { position: absolute; inset: 0; width: 100%; height: 100%; display: block; overflow: visible; }
  .gf252 .ch252 .ar252 { transition: d .45s ease; }
  .gf252 .rd252 { display: grid; grid-template-columns: 52px minmax(0,1fr) minmax(0,1fr); gap: 6px; align-items: center; height: 40px; margin-top: 4px; padding-top: 6px; border-top: 1px solid var(--line); font-size: 11px; color: var(--mute); }
  .gf252 .rd252 b { display: block; color: var(--ink); font-size: 13px; font-weight: 600; font-variant-numeric: tabular-nums; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .gf252 .rd252 .op b { color: var(--ink2); }
  .gf252 .rd252 small { color: var(--mute); font-weight: 400; font-size: 11px; }
  .gf252 .rd252 .dn { font-weight: 600; color: var(--ink); font-size: 12px; }
  .gx-bx226 .fc:has(.gl252) { overflow-y: auto; overscroll-behavior: contain; -webkit-overflow-scrolling: touch; }
  @media (prefers-reduced-motion: reduce) { .gf252 .ch252 .ar252 { transition: none; } }
</style>'''

HELPERS = r'''// ---------- change 252: Graph side of the Roster box, projection vs actual (install.py) ----------
// A[d] / B[d] = real points that day (null when the day hasn't started), PA[d] / PB[d] = that day's original projection,
// NA[d] / NB[d] = what's still projected for a day (today's rest, later days)
// games still to come in the lineup for one position group (F = forwards, D, G), same as the old Games side
function gxGl252(L, P0, dates, st) {
  return dates.reduce((t, _, d) => t + (st(d) === "f" ? 0 : ((L.days[d] || {}).start || []).filter((q) => q.st !== "F" && (P0 === "F" ? q.p !== "D" && q.p !== "G" : q.p === P0) && gxGPlays(q)).length), 0);
}
// a day counts as real once it is over, or once any game in either lineup has started
function gxOn252(X, Y, d, st) {
  if (st(d) === "f") return true;
  if (st(d) === "p") return false;
  const on = (L) => ((L.days[d] || {}).start || []).some((q) => q.st === "L" || q.st === "F");
  return on(X) || on(Y);
}
function GxGraph252({ dates, today, DN, A, B, PA, PB, NA, NB, nmA, nmB, plain, onDay }) {
  const [md, setMd] = useState(() => (uiGet().gr252 === "day" ? "day" : "run"));
  const n = dates.length;
  const lastReal = (() => { let j = -1; for (let d = 0; d < n; d++) if (A[d] != null) j = d; return j; })();
  const [pk, setPk] = useState(null);
  const [sz, setSz] = useState([300, 150]);
  const box = React.useRef(null);
  useEffect(() => {
    const el = box.current;
    if (!el) return undefined;
    const m = () => { const w = Math.round(el.clientWidth), h = Math.round(el.clientHeight); if (w > 40 && h > 40) setSz((o) => (o[0] === w && o[1] === h ? o : [w, h])); };
    m();
    if (!window.ResizeObserver) return undefined;
    const ro = new ResizeObserver(m); ro.observe(el);
    return () => ro.disconnect();
  }, []);
  const sel = pk != null && pk < n ? pk : lastReal >= 0 ? lastReal : 0;
  const setM = (m) => { setMd(m); uiSet("gr252", m); };
  const cum = (arr) => { let t = 0; return arr.map((v) => (v == null ? null : (t += v))); };
  const run = md === "run";
  // the numbers each line draws
  const aR = run ? cum(A) : A, bR = run ? cum(B) : B;
  const aP = run ? cum(PA) : PA, bP = run ? cum(PB) : PB;
  // projected-now continuation: from the last real point, adding what's still projected
  const ahead = (real, rest) => {
    if (lastReal < 0 || lastReal >= n - 1) return null;
    const out = dates.map(() => null);
    out[lastReal] = real[lastReal];
    let t = real[lastReal] + (rest[lastReal] || 0);
    for (let d = lastReal + 1; d < n; d++) { if (run) { t += rest[d] || 0; out[d] = t; } else out[d] = rest[d] || 0; }
    return out;
  };
  const aN = ahead(aR, NA), bN = ahead(bR, NB);
  const vals = [...aR, ...bR, ...aP, ...bP, ...(aN || []), ...(bN || [])].filter((v) => v != null);
  const top = Math.max(5, ...vals);
  const nice = (v) => { const p = Math.pow(10, Math.floor(Math.log10(v))); const m = v / p; return (m <= 1 ? 1 : m <= 2 ? 2 : m <= 2.5 ? 2.5 : m <= 5 ? 5 : 10) * p; };
  const stepV = nice(top / 3), yMax = Math.ceil(top / stepV) * stepV;
  const W = sz[0], H = sz[1], L0 = 26, R0 = 8, T0 = 14, B0 = 18;
  const x = (d) => L0 + (W - L0 - R0) * (n > 1 ? d / (n - 1) : 0.5);
  const y = (v) => T0 + (H - T0 - B0) * (1 - v / yMax);
  const pts = (arr) => arr.map((v, d) => (v == null ? null : [x(d), y(v)])).filter(Boolean);
  const line = (arr) => { const p = pts(arr); return p.length ? "M" + p.map((q) => q[0].toFixed(1) + " " + q[1].toFixed(1)).join(" L") : ""; };
  const area = (arr) => { const p = pts(arr); if (!p.length) return ""; const b = y(0).toFixed(1); return "M" + p[0][0].toFixed(1) + " " + b + " L" + p.map((q) => q[0].toFixed(1) + " " + q[1].toFixed(1)).join(" L") + " L" + p[p.length - 1][0].toFixed(1) + " " + b + " Z"; };
  const cA = plain ? "var(--ink2)" : "var(--accent)", cB = "var(--mute)";
  const grid = []; for (let v = 0; v <= yMax + 0.001; v += stepV) grid.push(v);
  const fmt = (v) => (v >= 100 ? String(Math.round(v)) : f1(v));
  const gid = "g252" + (plain ? "p" : "m");
  const tap = (e) => {
    const r = e.currentTarget.getBoundingClientRect(); const px = ((e.clientX - r.left) / r.width) * W;
    let b = 0; for (let d = 1; d < n; d++) if (Math.abs(x(d) - px) < Math.abs(x(b) - px)) b = d;
    if (b === sel && pk != null && onDay) onDay(b); else setPk(b);
  };
  const real = A[sel] != null;
  const diff = (v, p) => { const m = v - p; return (m >= 0 ? "+" : "\u2212") + f1(Math.abs(m)); };
  const cell = (nm, aArr, pArr, nArr, cls) => {
    const v = aArr[sel], p = pArr[sel];
    const now = nArr ? nArr[sel] : null;
    return (
      <div className={"min-w-0 " + cls}>
        <div className="truncate">{nm}</div>
        {v != null ? <b>{fmt(v)}<small>{" proj " + fmt(p) + " \u00b7 " + diff(v, p)}</small></b> : <b style={{ color: "var(--mute)", fontWeight: 400 }}>{(now != null ? fmt(now) : "\u2013")}<small>{" proj " + fmt(p)}</small></b>}
      </div>
    );
  };
  return (
    <>
      <div className="ft">
        <span className="gx-tag">Projection vs actual</span>
        <span className="sg252" onPointerDown={(e) => e.stopPropagation()}>
          <button type="button" className={run ? "on" : ""} onClick={() => setM("run")}>Running total</button>
          <button type="button" className={!run ? "on" : ""} onClick={() => setM("day")}>By day</button>
        </span>
      </div>
      <div className="lg252">
        <span><i style={{ background: cA, opacity: 0.55 }}></i><span className="truncate">{nmA}</span></span>
        <span><i style={{ background: cB, opacity: 0.45 }}></i><span className="truncate">{nmB}</span></span>
        <span><em></em>Projected</span>
      </div>
      <div className="ch252" data-gx="252" ref={box}>
        <svg viewBox={"0 0 " + W + " " + H} role="img" aria-label={"Projection vs actual, " + (run ? "running total" : "by day")} onClick={tap} style={{ cursor: "pointer" }}>
          <defs>
            <linearGradient id={gid + "a"} x1="0" y1="0" x2="0" y2="1"><stop offset="0" style={{ stopColor: cA, stopOpacity: 0.42 }} /><stop offset="1" style={{ stopColor: cA, stopOpacity: 0.03 }} /></linearGradient>
            <linearGradient id={gid + "b"} x1="0" y1="0" x2="0" y2="1"><stop offset="0" style={{ stopColor: cB, stopOpacity: 0.32 }} /><stop offset="1" style={{ stopColor: cB, stopOpacity: 0.02 }} /></linearGradient>
          </defs>
          {grid.map((v) => <g key={v}><line x1={L0} x2={W - R0} y1={y(v)} y2={y(v)} style={{ stroke: "var(--line)", strokeWidth: 1 }} /><text x={L0 - 4} y={y(v) + 3} textAnchor="end" style={{ fontSize: 8.5, fill: "var(--faint)" }}>{stepV >= 1 ? String(Math.round(v)) : f1(v)}</text></g>)}
          {dates.map((dt, d) => <text key={dt} x={x(d)} y={H - 4} textAnchor="middle" style={{ fontSize: 9, fill: d === sel ? "var(--ink)" : "var(--mute)", fontWeight: dt === today ? 700 : 400 }}>{DN(d)}</text>)}
          <line x1={x(sel)} x2={x(sel)} y1={T0 - 6} y2={H - B0} style={{ stroke: "var(--line2, var(--line))", strokeWidth: 1 }} />
          <path className="ar252" d={area(bR)} style={{ fill: "url(#" + gid + "b)" }} />
          <path className="ar252" d={area(aR)} style={{ fill: "url(#" + gid + "a)" }} />
          <path className="ar252" d={line(bP)} style={{ fill: "none", stroke: cB, strokeWidth: 1.6, strokeDasharray: "1 4", strokeLinecap: "round" }} />
          <path className="ar252" d={line(aP)} style={{ fill: "none", stroke: cA, strokeWidth: 2, strokeDasharray: "1 4", strokeLinecap: "round", opacity: 0.9 }} />
          {bN ? <path className="ar252" d={line(bN)} style={{ fill: "none", stroke: cB, strokeWidth: 1.2, strokeDasharray: "5 4", opacity: 0.6 }} /> : null}
          {aN ? <path className="ar252" d={line(aN)} style={{ fill: "none", stroke: cA, strokeWidth: 1.4, strokeDasharray: "5 4", opacity: 0.6 }} /> : null}
          <path className="ar252" d={line(bR)} style={{ fill: "none", stroke: cB, strokeWidth: 1.8, strokeLinejoin: "round" }} />
          <path className="ar252" d={line(aR)} style={{ fill: "none", stroke: cA, strokeWidth: 2.4, strokeLinejoin: "round" }} />
          {real ? <circle cx={x(sel)} cy={y(bR[sel])} r={2.6} style={{ fill: cB }} /> : null}
          {real ? <circle cx={x(sel)} cy={y(aR[sel])} r={3.2} style={{ fill: cA, stroke: "var(--card2)", strokeWidth: 1.5 }} /> : null}
        </svg>
      </div>
      <div className="rd252">
        <div className="dn">{dates[sel] === today ? "Today" : DN(sel)}<small style={{ display: "block" }}>{run ? "so far" : "that day"}</small></div>
        {cell(nmA, aR, aP, aN, "")}
        {cell(nmB, bR, bP, bN, "op")}
      </div>
    </>
  );
}
'''

def change(t):
    t = lit(t, "252: styles", "</style>", NEW_CSS, "change 252 (install.py)")
    t = lit(t, "252: helpers", ROOT, HELPERS + ROOT, "change 252: Graph side of the Roster box")
    t = lit(t, "252: button name",
            'const NF = 4, STEP = 360 / NF, NAMES = ["Day", "Win", "Games", "Players"];',
            'const NF = 4, STEP = 360 / NF, NAMES = ["Day", "Win", "Graph", "Players"]; /* change 252 */',
            'NAMES = ["Day", "Win", "Graph", "Players"]; /* change 252 */')
    t = lit(t, "252: graph side",
            '{fToday}{fWin}{fGames}{fPlayers}</div>\n          </div>\n          <div className="tb">{NAMES.map((t, j) => <button key={t} type="button" className={k === j ? "on" : ""} onClick={() => turn(j)}>{t}</button>)}</div>\n        </div>\n      </div>\n    </div>\n  );\n}\n// ---------- change 231',
            '{fToday}{fWin}<div className="fc gf252"><GxGraph252 dates={dates} today={today} DN={DN} nmA={nmA} nmB={nmB} plain={!mineMu} onDay={showDay}'
            ' A={dates.map((_, d) => (gxOn252(X, Y, d, st) ? (X.days[d] || {}).act || 0 : null))} B={dates.map((_, d) => (gxOn252(X, Y, d, st) ? (Y.days[d] || {}).act || 0 : null))}'
            ' PA={dates.map((_, d) => exp(X, d))} PB={dates.map((_, d) => exp(Y, d))}'
            ' NA={dates.map((_, d) => (st(d) === "f" ? 0 : (X.days[d] || {}).total || 0))} NB={dates.map((_, d) => (st(d) === "f" ? 0 : (Y.days[d] || {}).total || 0))} /></div>{fPlayers}</div>\n          </div>\n          <div className="tb">{NAMES.map((t, j) => <button key={t} type="button" className={k === j ? "on" : ""} onClick={() => turn(j)}>{t}</button>)}</div>\n        </div>\n      </div>\n    </div>\n  );\n}\n// ---------- change 231',
            '<div className="fc gf252"><GxGraph252')
    t = lit(t, "252: games facts on the Win side",
            '        <div>Their pace<b>{f1(fb)}</b></div>\n        <div>Your pace<b>{f1(fa)}</b></div>\n        <div>Spread<b>{"\\u00b1" + f1(sdNow)}</b></div>\n      </div>\n    </div>\n  );\n  const maxG = Math.max(1, ...dates.map((_, d) => Math.max(gms(X, d), gms(Y, d))));\n  const gCell = (L, d, mine) => { const g = gms(L, d), fut = st(d) === "p"; return <div key={d} className="c" style={{ background: fut ? "transparent" : mine ? "rgba(127,127,127," + (0.08 + 0.32 * g / maxG) + ")" : "rgba(127,127,127," + (0.05 + 0.18 * g / maxG) + ")", border: fut ? "1px dashed var(--line)" : "0", color: fut ? "var(--faint)" : mine ? "var(--ink)" : "var(--ink2)" }}>{g}</div>; };\n  const gLeftP',
            '        <div>Spread<b>{"\\u00b1" + f1(sdNow)}</b></div>\n'
            '        <div className="gl252">Games left<b>{two(leftA, leftB)}</b></div>\n'
            '        <div>Goalie starts left<b>{two(gxGl252(X, "G", dates, st), gxGl252(Y, "G", dates, st))}</b></div>\n'
            '        <div>Bench with a game<b>{two(X.wasted || 0, Y.wasted || 0)}</b></div>\n'
            '      </div>\n    </div>\n  );\n  const maxG = Math.max(1, ...dates.map((_, d) => Math.max(gms(X, d), gms(Y, d))));\n  const gCell = (L, d, mine) => { const g = gms(L, d), fut = st(d) === "p"; return <div key={d} className="c" style={{ background: fut ? "transparent" : mine ? "rgba(127,127,127," + (0.08 + 0.32 * g / maxG) + ")" : "rgba(127,127,127," + (0.05 + 0.18 * g / maxG) + ")", border: fut ? "1px dashed var(--line)" : "0", color: fut ? "var(--faint)" : mine ? "var(--ink)" : "var(--ink2)" }}>{g}</div>; };\n  const gLeftP',
            '<div className="gl252">Games left')
    return t

edit(APP, change)
