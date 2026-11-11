# changes/262-box-open-close-graph-zoom.py - Roster box: double tap opens, only X or outside closes; Graph zooms (pinch / scroll) and moves (drag); tapping the graph never switches to the Day side

NEW_CSS = r'''  /* change 262 (install.py) */
  .gf252 .ch252 svg.zm262 { touch-action: none; cursor: crosshair; }
  .gf252 .ch252.on262 svg.zm262 { cursor: grab; }
  .gf252 .ch252.dg262 svg.zm262 { cursor: grabbing; }
  .gf252 .ch252.on262 .ar252, .gf252 .ch252.dg262 .ar252 { transition: none; }
  .gf252 .ch252 .rz262 { position: absolute; top: 2px; right: 6px; z-index: 2; height: 26px; padding: 0 10px; border-radius: 999px; border: 1px solid var(--line2); background: var(--card2); color: var(--ink); font-size: 12px; }
  .gf252 .ch252 .ht262 { position: absolute; top: 4px; right: 8px; z-index: 1; font-size: 10.5px; color: var(--faint); pointer-events: none; }
</style>'''

def cut(t, label, start, end, new, marker):
    if marker in t:
        print("(install) " + label + ": already done")
        return t
    if t.count(start) != 1:
        fail(label + ": start text found " + str(t.count(start)) + " times")
    i = t.index(start)
    j = t.find(end, i)
    if j < 0:
        fail(label + ": end text not found")
    print("(install) " + label + ": updated")
    return t[:i] + new + t[j:]

GRAPH = r'''function GxGraph252({ dates, today, DN, A, B, PA, PB, NA, NB, nmA, nmB, plain, onDay, lab, sub, tag, res }) { /* change 259 */ /* change 262: zoom and move */
  const [md, setMd] = useState(() => (uiGet().gr252 === "day" ? "day" : "run"));
  const n = dates.length;
  const lastReal = (() => { let j = -1; for (let d = 0; d < n; d++) if (A[d] != null) j = d; return j; })();
  const [pk, setPk] = useState(null);
  const [sz, setSz] = useState([300, 150]);
  const box = React.useRef(null), svgR = React.useRef(null);
  // zoom window as parts of the whole graph: [left, right, bottom, top], each 0 to 1
  const Z0 = [0, 1, 0, 1];
  const [zm, setZm] = useState(Z0);
  const [dg, setDg] = useState(false);
  const zr = React.useRef(zm); zr.current = zm;
  const ptr = React.useRef(new Map()), ges = React.useRef(null), moved = React.useRef(false), raf = React.useRef(0), want = React.useRef(null);
  useEffect(() => {
    const el = box.current;
    if (!el) return undefined;
    const m = () => { const w = Math.round(el.clientWidth), h = Math.round(el.clientHeight); if (w > 40 && h > 40) setSz((o) => (o[0] === w && o[1] === h ? o : [w, h])); };
    m();
    if (!window.ResizeObserver) return undefined;
    const ro = new ResizeObserver(m); ro.observe(el);
    return () => ro.disconnect();
  }, []);
  useEffect(() => { setZm(Z0); }, [md, n, dates[0]]);
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
  const stepV0 = nice(top / 3), yMax = Math.ceil(top / stepV0) * stepV0;
  const W = sz[0], H = sz[1], L0 = 26, R0 = 8, T0 = 14, B0 = 18, PW = Math.max(10, W - L0 - R0), PH = Math.max(10, H - T0 - B0);
  const zoomed = zm[1] - zm[0] < 0.999 || zm[3] - zm[2] < 0.999;
  const fxOf = (d) => (n > 1 ? d / (n - 1) : 0.5);
  const x = (d) => L0 + PW * (fxOf(d) - zm[0]) / (zm[1] - zm[0]);
  const y = (v) => T0 + PH * (1 - (v / yMax - zm[2]) / (zm[3] - zm[2]));
  const pts = (arr) => arr.map((v, d) => (v == null ? null : [x(d), y(v)])).filter(Boolean);
  const line = (arr) => { const p = pts(arr); return p.length ? "M" + p.map((q) => q[0].toFixed(1) + " " + q[1].toFixed(1)).join(" L") : ""; };
  const area = (arr) => { const p = pts(arr); if (!p.length) return ""; const b = y(0).toFixed(1); return "M" + p[0][0].toFixed(1) + " " + b + " L" + p.map((q) => q[0].toFixed(1) + " " + q[1].toFixed(1)).join(" L") + " L" + p[p.length - 1][0].toFixed(1) + " " + b + " Z"; };
  const cA = plain ? "var(--ink2)" : "var(--accent)", cB = "var(--mute)";
  // grid lines for the part on screen
  const lo = zm[2] * yMax, hi = zm[3] * yMax, stepV = nice(Math.max(0.05, (hi - lo) / 3));
  const grid = []; for (let v = Math.ceil(lo / stepV - 1e-9) * stepV; v <= hi + 1e-6 && grid.length < 12; v += stepV) grid.push(+v.toFixed(4));
  const fmt = (v) => (v >= 100 ? String(Math.round(v)) : f1(v));
  const gid = "g252" + (plain ? "p" : "m");
  // ---- zoom helpers (window math stays between 0 and 1)
  const minX = n > 1 ? Math.min(1, 1.2 / (n - 1)) : 1, minY = 0.08;
  const fit = (a, w, mn) => { w = Math.max(mn, Math.min(1, w)); a = Math.max(0, Math.min(1 - w, a)); return [a, a + w]; };
  const zAt = (z, px, py, f) => {
    const u = Math.max(0, Math.min(1, (px - L0) / PW)), v = Math.max(0, Math.min(1, 1 - (py - T0) / PH));
    const dx = z[0] + u * (z[1] - z[0]), dy = z[2] + v * (z[3] - z[2]);
    const w = (z[1] - z[0]) / f, h = (z[3] - z[2]) / f;
    const X = fit(dx - u * Math.max(minX, Math.min(1, w)), w, minX), Y = fit(dy - v * Math.max(minY, Math.min(1, h)), h, minY);
    return [X[0], X[1], Y[0], Y[1]];
  };
  const zPan = (z, ddx, ddy) => {
    const X = fit(z[0] - (ddx / PW) * (z[1] - z[0]), z[1] - z[0], minX), Y = fit(z[2] + (ddy / PH) * (z[3] - z[2]), z[3] - z[2], minY);
    return [X[0], X[1], Y[0], Y[1]];
  };
  const isZ = (z) => z[1] - z[0] < 0.999 || z[3] - z[2] < 0.999;
  const put = (z) => { want.current = z; if (!raf.current) raf.current = requestAnimationFrame(() => { raf.current = 0; if (want.current) setZm(want.current); }); };
  useEffect(() => () => cancelAnimationFrame(raf.current), []);
  const toSvg = (cx, cy) => { const el = svgR.current; if (!el) return [0, 0]; const r = el.getBoundingClientRect(); return [((cx - r.left) / (r.width || 1)) * W, ((cy - r.top) / (r.height || 1)) * H]; };
  const mid2 = () => { const a = [...ptr.current.values()]; return { x: (a[0].x + a[1].x) / 2, y: (a[0].y + a[1].y) / 2, d: Math.hypot(a[0].x - a[1].x, a[0].y - a[1].y) || 1 }; };
  const startPan = () => { const a = [...ptr.current.values()][0]; ges.current = { k: "pan", x: a.x, y: a.y, z: zr.current }; };
  const pDown = (e) => {
    if (e.pointerType === "mouse" && e.button !== 0) return;
    ptr.current.set(e.pointerId, { x: e.clientX, y: e.clientY });
    if (ptr.current.size === 1) moved.current = false;
    if (ptr.current.size >= 2) {
      const m = mid2(); ges.current = { k: "pinch", m, z: zr.current };
      e.stopPropagation(); setDg(true);
      try { e.currentTarget.setPointerCapture(e.pointerId); } catch (x2) {}
    } else if (isZ(zr.current)) {
      startPan(); e.stopPropagation(); setDg(true);
      try { e.currentTarget.setPointerCapture(e.pointerId); } catch (x2) {}
    } else ges.current = null; // not zoomed: one finger still spins the box
  };
  const pMove = (e) => {
    if (!ptr.current.has(e.pointerId)) return;
    ptr.current.set(e.pointerId, { x: e.clientX, y: e.clientY });
    const g = ges.current;
    if (!g) return;
    e.stopPropagation();
    if (g.k === "pinch" && ptr.current.size >= 2) {
      const m = mid2(), [sx, sy] = toSvg(g.m.x, g.m.y), [nx, ny] = toSvg(m.x, m.y);
      let z = zAt(g.z, sx, sy, m.d / g.m.d);
      z = zPan(z, nx - sx, ny - sy);
      moved.current = true; put(z);
    } else if (g.k === "pan") {
      const a = ptr.current.get(e.pointerId), r = svgR.current.getBoundingClientRect();
      const ddx = ((a.x - g.x) / (r.width || 1)) * W, ddy = ((a.y - g.y) / (r.height || 1)) * H;
      if (Math.abs(a.x - g.x) + Math.abs(a.y - g.y) > 4) moved.current = true;
      put(zPan(g.z, ddx, ddy));
    }
  };
  const pUp = (e) => {
    if (!ptr.current.has(e.pointerId)) return;
    ptr.current.delete(e.pointerId);
    const g = ges.current;
    if (g) e.stopPropagation();
    if (ptr.current.size === 1 && g && g.k === "pinch") { if (want.current) zr.current = want.current; startPan(); }
    else if (!ptr.current.size) { ges.current = null; setDg(false); }
  };
  // laptop: scroll wheel or trackpad pinch zooms where the mouse is; sideways scroll moves
  useEffect(() => {
    const el = svgR.current;
    if (!el) return undefined;
    const wh = (e) => {
      const z = want.current && raf.current ? want.current : zr.current;
      const side = !e.ctrlKey && Math.abs(e.deltaX) > Math.abs(e.deltaY);
      if (!e.ctrlKey && !side && e.deltaY > 0 && !isZ(z)) return; // fully out: let the page scroll
      e.preventDefault();
      const r = el.getBoundingClientRect(), px = ((e.clientX - r.left) / (r.width || 1)) * W, py = ((e.clientY - r.top) / (r.height || 1)) * H;
      if (side) { put(zPan(z, -e.deltaX, 0)); return; }
      const dy = e.deltaMode === 1 ? e.deltaY * 16 : e.deltaY;
      put(zAt(z, px, py, Math.exp(-dy * (e.ctrlKey ? 0.01 : 0.0022))));
    };
    el.addEventListener("wheel", wh, { passive: false });
    return () => el.removeEventListener("wheel", wh);
  }, [W, H, n]);
  const tap = (e) => {
    if (moved.current) { moved.current = false; return; }
    const [px] = toSvg(e.clientX, e.clientY);
    let b = -1; for (let d = 0; d < n; d++) { const xd = x(d); if (xd < L0 - 2 || xd > W - R0 + 2) continue; if (b < 0 || Math.abs(xd - px) < Math.abs(x(b) - px)) b = d; }
    if (b >= 0) setPk(b); // just picks the day (Kuvar, Nov 10: never switch to the Day side)
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
  const clip = gid + "c";
  const inX = (d) => { const xd = x(d); return xd >= L0 - 2 && xd <= W - R0 + 2; };
  return (
    <>
      <div className="ft">
        <span className="gx-tag">{tag || "Projection vs actual"}</span>
        <span className="sg252" onPointerDown={(e) => e.stopPropagation()}>
          <button type="button" className={run ? "on" : ""} onClick={() => setM("run")}>{(lab || [])[0] || "Running total"}</button>
          <button type="button" className={!run ? "on" : ""} onClick={() => setM("day")}>{(lab || [])[1] || "By day"}</button>
        </span>
      </div>
      <div className="lg252">
        <span><i style={{ background: cA, opacity: 0.55 }}></i><span className="truncate">{nmA}</span></span>
        <span><i style={{ background: cB, opacity: 0.45 }}></i><span className="truncate">{nmB}</span></span>
        <span><em></em>Projected</span>
      </div>
      <div className={"ch252" + (zoomed ? " on262" : "") + (dg ? " dg262" : "")} data-gx="252" ref={box}>
        {zoomed ? <button type="button" className="rz262" data-gx="262" onPointerDown={(e) => e.stopPropagation()} onClick={(e) => { e.stopPropagation(); setZm(Z0); }}>Reset zoom</button> : <span className="ht262">Pinch or scroll to zoom</span>}
        <svg ref={svgR} className="zm262" viewBox={"0 0 " + W + " " + H} role="img" aria-label={"Projection vs actual, " + (run ? "running total" : "by day")} onClick={tap}
          onPointerDown={pDown} onPointerMove={pMove} onPointerUp={pUp} onPointerCancel={pUp} onDragStart={(e) => e.preventDefault()}>
          <defs>
            <linearGradient id={gid + "a"} x1="0" y1="0" x2="0" y2="1"><stop offset="0" style={{ stopColor: cA, stopOpacity: 0.42 }} /><stop offset="1" style={{ stopColor: cA, stopOpacity: 0.03 }} /></linearGradient>
            <linearGradient id={gid + "b"} x1="0" y1="0" x2="0" y2="1"><stop offset="0" style={{ stopColor: cB, stopOpacity: 0.32 }} /><stop offset="1" style={{ stopColor: cB, stopOpacity: 0.02 }} /></linearGradient>
            <clipPath id={clip}><rect x={L0} y={T0 - 8} width={PW} height={PH + 8} /></clipPath>
          </defs>
          <rect x={0} y={0} width={W} height={H} style={{ fill: "transparent" }} />
          {grid.map((v) => <g key={v}><line x1={L0} x2={W - R0} y1={y(v)} y2={y(v)} style={{ stroke: "var(--line)", strokeWidth: 1 }} /><text x={L0 - 4} y={y(v) + 3} textAnchor="end" style={{ fontSize: 8.5, fill: "var(--faint)" }}>{stepV >= 1 ? String(Math.round(v)) : f1(v)}</text></g>)}
          {dates.map((dt, d) => (inX(d) ? <text key={dt} x={x(d)} y={H - 4} textAnchor="middle" style={{ fontSize: 9, fill: d === sel ? "var(--ink)" : "var(--mute)", fontWeight: dt === today ? 700 : 400 }}>{DN(d)}</text> : null))}
          <g clipPath={"url(#" + clip + ")"}>
            {inX(sel) ? <line x1={x(sel)} x2={x(sel)} y1={T0 - 6} y2={H - B0} style={{ stroke: "var(--line2, var(--line))", strokeWidth: 1 }} /> : null}
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
          </g>
        </svg>
      </div>
      <div className="rd252">
        <div className="dn">{dates[sel] === today ? "Today" : DN(sel)}<small style={{ display: "block" }}>{res ? res(sel) : run ? (sub || [])[0] || "so far" : (sub || [])[1] || "that day"}</small></div>
        {cell(nmA, aR, aP, aN, "")}
        {cell(nmB, bR, bP, bN, "op")}
      </div>
    </>
  );
}
'''

def change(t):
    t = lit(t, "262: styles", "</style>", NEW_CSS, "change 262 (install.py)")
    t = lit(t, "262: open box ignores double taps",
            "    if (!e.detail) return; // keyboard\n",
            "    if (!e.detail) return; // keyboard\n    if (z) return; /* change 262: once open, taps go straight through; only X or outside closes */\n",
            "change 262: once open, taps go straight through")
    t = lit(t, "262: open box label", '<span className="zt254">Tap twice to shrink</span>', '<span className="zt254">Tap outside or X to close</span>', "Tap outside or X to close")
    t = cut(t, "262: graph zoom", "function GxGraph252(", "// ---------- change 253:", GRAPH, "change 262: zoom and move")
    return t

edit(APP, change)
