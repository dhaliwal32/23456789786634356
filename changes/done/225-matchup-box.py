# changes/225-matchup-box.py - Roster page: the week chart becomes a four-sided box you spin (Score, Win, Games, Players)

NEW_CSS = r'''  /* change 225 (install.py): matchup box on the Roster page */
  .gx-bx225 { min-width: 0; }
  .gx-bx225 .hd { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }
  .gx-bx225 .hd .sp { flex: 1; }
  .gx-bx225 .mu { height: 30px; max-width: 170px; border-radius: 8px; border: 1px solid var(--line); background: var(--card); color: var(--ink); font-size: 12.5px; padding: 0 6px; }
  .gx-bx225 .fs { width: 30px; height: 30px; border-radius: 8px; border: 1px solid var(--line); background: var(--card); color: var(--ink); display: inline-flex; align-items: center; justify-content: center; }
  .gx-bx225 .stg { position: relative; height: 288px; margin-top: 10px; perspective: 1100px; touch-action: pan-y; user-select: none; -webkit-user-select: none; }
  .gx-bx225 .pr { position: absolute; inset: 0; transform-style: preserve-3d; will-change: transform; }
  .gx-bx225 .pr.an { transition: transform .55s cubic-bezier(.2,.8,.2,1); }
  .gx-bx225 .fc { position: absolute; inset: 0; box-sizing: border-box; padding: 14px; border-radius: 14px; background: var(--card2); border: 1px solid var(--line); backface-visibility: hidden; -webkit-backface-visibility: hidden; overflow: hidden; }
  .gx-bx225 .fc::after { content: ""; position: absolute; inset: 0; border-radius: 14px; pointer-events: none; background: #000; opacity: var(--sh, 0); }
  html[data-theme="light"] .gx-bx225 .fc::after { opacity: calc(var(--sh, 0) * .45); }
  .gx-bx225 .ft { display: flex; justify-content: space-between; align-items: center; }
  .gx-bx225 .sc { display: grid; grid-template-columns: minmax(0,1fr) 64px minmax(0,1fr); align-items: center; gap: 6px; margin-top: 8px; }
  .gx-bx225 .sc .r { text-align: right; }
  .gx-bx225 .bg { font-size: clamp(26px, 7vw, 34px); font-weight: 600; font-variant-numeric: tabular-nums; line-height: 1.1; }
  .gx-bx225 .shr { display: flex; height: 4px; gap: 3px; margin: 10px 0 8px; }
  .gx-bx225 .dys { display: grid; grid-template-columns: repeat(7, minmax(0,1fr)); gap: 4px; margin-top: 8px; }
  .gx-bx225 .dy { border: 0; border-radius: 8px; background: var(--card3, var(--card)); padding: 6px 0; text-align: center; font-variant-numeric: tabular-nums; color: var(--ink); }
  .gx-bx225 .dy small { display: block; font-size: 10px; color: var(--mute); }
  .gx-bx225 .dy b { display: block; font-size: 12.5px; font-weight: 600; margin-top: 2px; }
  .gx-bx225 .dy i { display: block; font-style: normal; font-size: 12.5px; color: var(--mute); }
  .gx-bx225 .dy.td { box-shadow: inset 0 0 0 1px var(--ink); }
  .gx-bx225 .dy.on { background: var(--accentSoft); }
  .gx-bx225 .dy.pj b, .gx-bx225 .dy.pj i { color: var(--faint); font-weight: 400; }
  .gx-bx225 .fx { display: grid; grid-template-columns: repeat(3, minmax(0,1fr)); gap: 6px; margin-top: 10px; }
  .gx-bx225 .fx div { font-size: 12px; color: var(--mute); }
  .gx-bx225 .fx b { display: block; color: var(--ink); font-size: 14px; font-weight: 600; font-variant-numeric: tabular-nums; }
  .gx-bx225 .wn { display: flex; align-items: center; gap: 14px; margin-top: 6px; }
  .gx-bx225 .gr { display: grid; grid-template-columns: 54px repeat(7, minmax(0,1fr)) 40px; gap: 4px; align-items: center; margin-top: 10px; font-variant-numeric: tabular-nums; }
  .gx-bx225 .gr .h { font-size: 10px; color: var(--mute); text-align: center; }
  .gx-bx225 .gr .n { font-size: 12px; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .gx-bx225 .gr .c { height: 26px; border-radius: 6px; display: flex; align-items: center; justify-content: center; font-size: 12.5px; }
  .gx-bx225 .gr .t { text-align: right; font-size: 13px; font-weight: 600; }
  .gx-bx225 .kp { display: grid; grid-template-columns: minmax(0,1fr) minmax(0,1fr); gap: 12px; margin-top: 6px; }
  .gx-bx225 .pl { display: grid; grid-template-columns: auto minmax(0,1fr) auto; align-items: center; gap: 6px; height: 40px; border-bottom: 1px solid var(--line); background: none; border-left: 0; border-right: 0; border-top: 0; padding: 0; color: var(--ink); text-align: left; width: 100%; }
  .gx-bx225 .pl .nm { min-width: 0; }
  .gx-bx225 .pl .nm b { display: block; font-size: 12.5px; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .gx-bx225 .pl .nm span { display: block; font-size: 10.5px; color: var(--mute); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .gx-bx225 .pl .pt { font-size: 13px; font-weight: 600; font-variant-numeric: tabular-nums; }
  .gx-bx225 .tb { display: flex; justify-content: center; gap: 4px; margin-top: 10px; }
  .gx-bx225 .tb button { height: 30px; padding: 0 12px; border-radius: 8px; border: 0; background: none; color: var(--mute); font-size: 12.5px; }
  .gx-bx225 .tb button.on { background: var(--accentSoft); color: var(--ink); font-weight: 600; }
  .gx-bx225 .dt { margin-top: 10px; border-top: 1px solid var(--line); padding-top: 10px; }
  .gx-bx225 .dt .cols { display: grid; grid-template-columns: minmax(0,1fr) minmax(0,1fr); gap: 12px; }
  .gx-bx225 .dt .rw { display: flex; justify-content: space-between; gap: 6px; height: 28px; align-items: center; font-size: 12.5px; border-bottom: 1px solid var(--line); }
  .gx-bx225 .dt .rw span:first-child { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; min-width: 0; }
  .gx-bx225 .dt .rw b { font-weight: 600; font-variant-numeric: tabular-nums; }
  .gx-bx225.full { position: fixed; inset: 0; z-index: 60; background: var(--bg); overflow-y: auto; padding: calc(env(safe-area-inset-top) + 14px) 14px calc(env(safe-area-inset-bottom) + 20px); }
  .gx-bx225.full .stg { height: min(62vh, 520px); }
  .gx-bx225.full .dys .dy { padding: 9px 0; }
  @media (min-width: 641px) { .gx-bx225 .stg { height: 250px; } .gx-bx225 .stg { perspective: 2200px; } }
  @media (prefers-reduced-motion: reduce) { .gx-bx225 .pr.an { transition: none; } }
</style>'''

HELPERS = r'''// ---------- change 225: matchup box on the Roster page (install.py) ----------
function GxBox225({ s, wk }) {
  const K = s.blend, today = todayISO(), gen = (window.ESPN_DATA || {}).generated;
  const [pick, setPick] = useState(null);
  const [who, setWho] = useState(null);
  const [k, setK] = useState(0);
  const [sel, setSel] = useState(null);
  const [full, setFull] = useState(false);
  const stg = React.useRef(null), pr = React.useRef(null), ang = React.useRef(0), drag = React.useRef(null);
  const i = gxWkAt61(s, pick), cur = i === s.wk;
  const w = useMemo(() => (cur ? wk : deriveWeek(s.weeks[i], s.autoDone)), [cur, wk, s.weeks, i, s.autoDone]);
  const me = who && (w.pairs || []).some((p) => p[0] === who || p[1] === who) ? who : s.me;
  const dates = w.dates || [], n = dates.length;
  const opp = oppOf(w, me) || (cur && me === s.me ? s.opp : null);
  const up = !(n > 0 && dates[0] <= today), fin = !cur && n > 0 && dates[n - 1] < today;
  const R = useMemo(() => {
    if (!opp || !n || fin) return null;
    const run = (id) => weekLive(s.players.filter((p) => p.ft === id), w, K, id, { detail: true });
    return [run(me), run(opp)];
  }, [w, me, opp, fin, s.players, K, gen, window.__PMODE, window.__LIVEV120]);
  useEffect(() => {
    const h = () => { setPick(Math.min(s.weeks.length - 1, s.wk + 1)); setSel(null); };
    window.addEventListener("gx-race-next", h);
    return () => window.removeEventListener("gx-race-next", h);
  }, [s.wk, s.weeks.length]);
  useEffect(() => { if (!full) return undefined; const kd = (e) => { if (e.key === "Escape") setFull(false); }; window.addEventListener("keydown", kd); return () => window.removeEventListener("keydown", kd); }, [full]);
  // spinning: the four sides are placed around the middle of the box and the box turns
  const paint = (a, anim) => {
    const el = pr.current, box = stg.current;
    if (!el || !box) return;
    const z = box.clientWidth / 2;
    el.classList.toggle("an", !!anim);
    el.style.transform = "translateZ(" + -z + "px) rotateY(" + -a + "deg)";
    [...el.children].forEach((f, j) => {
      f.style.transform = "rotateY(" + j * 90 + "deg) translateZ(" + z + "px)";
      const d = Math.abs((((j * 90 - a) % 360) + 540) % 360 - 180);
      f.style.setProperty("--sh", String(Math.min(0.75, d / 120)));
    });
  };
  const turn = (j) => { const a0 = ang.current, base = Math.round(a0 / 360) * 360; let t = base + j * 90; while (t - a0 > 180) t -= 360; while (a0 - t > 180) t += 360; ang.current = t; paint(t, true); setK(((j % 4) + 4) % 4); };
  React.useLayoutEffect(() => { paint(ang.current, false); });
  useEffect(() => {
    const box = stg.current;
    if (!box || !window.ResizeObserver) return undefined;
    const ro = new ResizeObserver(() => paint(ang.current, false)); ro.observe(box);
    return () => ro.disconnect();
  }, [full, R ? 1 : 0]);
  const pDown = (e) => { drag.current = { x: e.clientX, y: e.clientY, a: ang.current, on: false }; };
  const pMove = (e) => {
    const d = drag.current;
    if (!d) return;
    const dx = e.clientX - d.x, dy = e.clientY - d.y;
    if (!d.on) { if (Math.abs(dx) > 8 && Math.abs(dx) > Math.abs(dy)) { d.on = true; try { stg.current.setPointerCapture(e.pointerId); } catch (x) {} } else return; }
    ang.current = d.a - dx * 0.42; paint(ang.current, false);
  };
  const pUp = () => {
    const d = drag.current; drag.current = null;
    if (!d || !d.on) return;
    const moved = ang.current - d.a, j = Math.round(d.a / 90) + (Math.abs(moved) > 25 ? Math.sign(moved) : 0);
    ang.current = d.a + moved; turn(j);
  };
  const pairs = (w.pairs || []).filter((p) => p[0] && p[1]);
  const title = cur ? "This week" : up && i === s.wk + 1 ? "Next week" : "Week " + (i + 1);
  const muSel = pairs.length ? (
    <select className="mu" aria-label="Choose a matchup" value={me} onChange={(e) => { setWho(e.target.value); setSel(null); }}>
      {pairs.map((p) => { const a = p[0] === s.me || p[1] === s.me ? s.me : p[0], b = a === p[0] ? p[1] : p[0]; return <option key={a + b} value={a}>{(a === s.me ? "You" : teamName(s, a)) + " v " + teamName(s, b)}</option>; })}
    </select>
  ) : null;
  const head = (
    <div className="hd">
      <span className="gx-tag">{title}</span>
      <GxWkPick s={s} i={i} go={(j) => { setPick(Math.max(0, Math.min(s.weeks.length - 1, j))); setSel(null); }} />
      <span className="sp"></span>
      {muSel}
      <button type="button" className="fs" aria-label={full ? "Close full screen" : "Full screen"} onClick={() => setFull(!full)}>{full ? "\u00d7" : "\u2922"}</button>
    </div>
  );
  const cls = "gx-pn gx-bx225" + (full ? " full fixed inset-0" : "");
  const act = (id) => +(gxAct120(w)[id]) || 0;
  const sa = up ? 0 : act(me), sb = up || !opp ? 0 : act(opp);
  if (fin || !R) {
    return (
      <div className={cls}>{head}
        {fin && opp && (sa || sb) ? (
          <div style={{ display: "flex", alignItems: "baseline", gap: 10, paddingTop: 10, fontVariantNumeric: "tabular-nums" }}>
            <span className="gx-stv">{f1(sa)}</span><span className="text-slate-500">to {f1(sb)}</span>
            <span className="text-slate-500">{sa > sb ? "Won by " + f1(sa - sb) : sa < sb ? "Lost by " + f1(sb - sa) : "Tied"}</span>
          </div>
        ) : <div className="text-sm text-slate-500" style={{ paddingTop: 10 }}>{fin ? "No result saved for this week." : "The matchup for this week is not set yet."}</div>}
        {fin ? <div className="text-xs text-slate-500" style={{ marginTop: 6 }}>Day by day scores are only kept for the current week.</div> : null}
      </div>
    );
  }
  const X = R[0], Y = R[1];
  const st = (d) => (dates[d] < today ? "f" : dates[d] === today ? "t" : "p");
  const pts = (L, d) => { const x = L.days[d] || {}, kk = st(d); return kk === "f" ? x.act || 0 : kk === "t" ? (x.act || 0) + (x.total || 0) : x.total || 0; };
  const exp = (L, d) => { const x = L.days[d] || {}; return x.proj != null ? x.proj : x.total || 0; };
  const A7 = dates.map((_, d) => pts(X, d)), B7 = dates.map((_, d) => pts(Y, d));
  const fdays = dates.map((_, d) => d).filter((d) => st(d) === "f"), done = fdays.length;
  const wp = winProb(X, Y, sa, sb), fa = sa + X.total, fb = sb + Y.total, over = done >= n;
  const nmA = me === s.me ? "You" : teamName(s, me), nmB = teamName(s, opp);
  const DN = (d) => (dates[d] === today ? "Today" : dayLabel(dates[d]).split(",")[0].slice(0, 3));
  const gms = (L, d) => gxGmN(L.days[d]);
  const totG = (L) => dates.reduce((t, _, d) => t + gms(L, d), 0);
  const won = fdays.filter((d) => A7[d] > B7[d]).length;
  const vsA = fdays.reduce((t, d) => t + A7[d] - exp(X, d), 0), vsB = fdays.reduce((t, d) => t + B7[d] - exp(Y, d), 0);
  const sg = (v) => (v >= 0 ? "+" : "\u2212") + f1(Math.abs(v));
  // win chance at the end of each finished day: points so far plus the original projection for the days after it
  const sdNow = Math.sqrt(projVar(X) + projVar(Y)), remNow = Math.max(1, X.total + Y.total);
  const wHist = fdays.map((d) => {
    let a = 0, b = 0, ra = 0, rb = 0;
    for (let j = 0; j < n; j++) { if (j <= d) { a += A7[j]; b += B7[j]; } else { ra += exp(X, j); rb += exp(Y, j); } }
    const sd = sdNow * Math.sqrt(Math.max(0.05, (ra + rb) / remNow));
    const m = a + ra - (b + rb);
    return sd > 0 ? normCdf(m / sd) : m > 0 ? 1 : m < 0 ? 0 : 0.5;
  });
  const leftA = X.used, leftB = Y.used;
  const need = fb - sa, perG = leftA ? Math.max(0, need) / leftA : 0;
  const SA = gxSum209(s, me, X), SB = gxSum209(s, opp, Y);
  const top = (G) => [...G.F, ...G.D, ...G.G].filter((o) => o.gp || o.left).sort((u, v) => v.pts - u.pts || v.rem - u.rem).slice(0, 5);
  const openP = (p) => { if (p && window.__NAV) window.__NAV.player(p); };
  const faceTitle = (a, b) => <div className="ft"><span className="gx-tag">{a}</span><span className="text-xs text-slate-500">{b}</span></div>;
  const dayCell = (d) => {
    const k0 = st(d), a = A7[d], b = B7[d], pj = k0 === "p";
    return (
      <button key={d} type="button" className={"dy" + (dates[d] === today ? " td" : "") + (pj ? " pj" : "") + (sel === d ? " on" : "")} onClick={() => setSel(sel === d ? null : d)}>
        <small>{DN(d)}</small><b>{f1(a)}</b><i>{f1(b)}</i>
      </button>
    );
  };
  // the four sides
  const fScore = (
    <div className="fc">
      {faceTitle("Score", over ? "Final" : "Day " + Math.min(n, done + 1) + " of " + n)}
      <div className="sc">
        <div className="min-w-0"><div className="text-sm font-semibold truncate">{nmA}</div><div className="bg"><GxAnimNum131 v={sa} /></div></div>
        <GxRing v={wp} plain />
        <div className="min-w-0 r"><div className="text-sm text-slate-500 truncate">{nmB}</div><div className="bg" style={{ color: "var(--ink2)" }}><GxAnimNum131 v={sb} /></div></div>
      </div>
      <div className="shr"><div style={{ width: (sa + sb > 0 ? Math.max(4, Math.min(96, (sa / (sa + sb)) * 100)) : 50) + "%", background: "var(--accent)" }}></div><div style={{ flex: 1, background: "var(--track)" }}></div></div>
      <div className="text-xs text-slate-500" style={{ display: "flex" }}><span>{(over ? "Final " : "Projected ") + f1(fa)}</span><span style={{ margin: "0 auto" }}>{(fa >= fb ? "Ahead by " : "Behind by ") + f1(Math.abs(fa - fb))}</span><span>{f1(fb)}</span></div>
      <div className="dys">{dates.map((_, d) => dayCell(d))}</div>
    </div>
  );
  const W0 = 300, H0 = 86, px = (j) => 14 + (W0 - 28) * (wHist.length > 1 ? j / (wHist.length - 1) : 0.5), py = (v) => 8 + (1 - v) * (H0 - 26);
  const fWin = (
    <div className="fc">
      {faceTitle("Win chance", over ? "Final" : "Now")}
      <div className="wn">
        <GxRing v={wp} big plain />
        <div className="min-w-0">
          <div className="text-sm">{over ? (sa >= sb ? "Won by " + f1(sa - sb) : "Lost by " + f1(sb - sa)) : (fa >= fb ? "On pace to win by " : "On pace to lose by ") + f1(Math.abs(fa - fb))}</div>
          {over ? null : <div className="text-xs text-slate-500" style={{ marginTop: 4 }}>{"They should finish near " + f1(fb)}</div>}
          {over ? null : <div className="text-xs text-slate-500" style={{ marginTop: 2 }}>{"You need " + f1(Math.max(0, need)) + " more" + (leftA ? ", " + f1(perG) + " a game left" : "")}</div>}
        </div>
      </div>
      <div className="gx-tag" style={{ marginTop: 12 }}>After each day</div>
      {wHist.length ? (
        <svg viewBox={"0 0 " + W0 + " " + H0} width="100%" height={H0} className="gx-svg" style={{ display: "block", marginTop: 4 }} role="img" aria-label="Win chance after each day">
          <line x1={0} x2={W0} y1={py(0.5)} y2={py(0.5)} style={{ stroke: "var(--line2, var(--line))", strokeDasharray: "3 4" }} />
          {wHist.length > 1 ? <polyline points={wHist.map((v, j) => px(j).toFixed(1) + "," + py(v).toFixed(1)).join(" ")} style={{ fill: "none", stroke: "var(--accent)", strokeWidth: 2, strokeLinejoin: "round" }} /> : null}
          {wHist.map((v, j) => <g key={j}><circle cx={px(j)} cy={py(v)} r={3} style={{ fill: "var(--accent)" }} /><text x={px(j)} y={py(v) - 7} textAnchor="middle" style={{ fontSize: 10, fill: "var(--ink2)" }}>{Math.round(v * 100)}</text><text x={px(j)} y={H0 - 2} textAnchor="middle" style={{ fontSize: 10, fill: "var(--mute)" }}>{DN(fdays[j])}</text></g>)}
        </svg>
      ) : <div className="text-xs text-slate-500" style={{ marginTop: 8 }}>Shows once the first day is over.</div>}
    </div>
  );
  const maxG = Math.max(1, ...dates.map((_, d) => Math.max(gms(X, d), gms(Y, d))));
  const gCell = (L, d, mine) => { const g = gms(L, d), fut = st(d) === "p"; return <div key={d} className="c" style={{ background: fut ? "transparent" : mine ? "rgba(127,127,127," + (0.08 + 0.32 * g / maxG) + ")" : "rgba(127,127,127," + (0.05 + 0.18 * g / maxG) + ")", border: fut ? "1px dashed var(--line)" : "0", color: fut ? "var(--faint)" : mine ? "var(--ink)" : "var(--ink2)" }}>{g}</div>; };
  const fGames = (
    <div className="fc">
      {faceTitle("Lineup games", up ? "Projected" : "Left " + leftA + " v " + leftB)}
      <div className="gr">
        <div></div>{dates.map((_, d) => <div key={d} className="h" style={dates[d] === today ? { color: "var(--ink)", fontWeight: 600 } : null}>{DN(d)}</div>)}<div className="h">{up ? "All" : "Left"}</div>
        <div className="n">{nmA}</div>{dates.map((_, d) => gCell(X, d, true))}<div className="t">{up ? totG(X) : leftA}</div>
        <div className="n text-slate-500">{nmB}</div>{dates.map((_, d) => gCell(Y, d, false))}<div className="t text-slate-500">{up ? totG(Y) : leftB}</div>
      </div>
      <div className="fx" style={{ marginTop: 14 }}>
        <div>Games all week<b>{totG(X) + " v " + totG(Y)}</b></div>
        <div>{done ? "Days won" : "Days"}<b>{done ? won + " of " + done : n}</b></div>
        <div>Vs projection<b>{done ? sg(vsA) + " v " + sg(vsB) : "\u2013"}</b></div>
      </div>
    </div>
  );
  const pCol = (G, nm, dim) => (
    <div className="min-w-0">
      <div className={"text-xs truncate" + (dim ? " text-slate-500" : " font-semibold")} style={{ marginBottom: 2 }}>{nm}</div>
      {top(G).map((o) => (
        <button key={o.p.id} type="button" className="pl" onClick={() => openP(o.p)}>
          <GxFace p={o.p} size={22} />
          <span className="nm"><b>{lastN(o.p.n)}</b><span>{o.p.t + " \u00b7 " + o.gp + " GP" + (o.left ? " \u00b7 " + o.left + " left" : "")}</span></span>
          <span className="pt" style={dim ? { color: "var(--ink2)" } : null}>{f1(o.pts)}</span>
        </button>
      ))}
    </div>
  );
  const fPlayers = (
    <div className="fc">
      {faceTitle("Who's carrying", "Points this week")}
      <div className="kp">{pCol(SA, nmA, false)}{pCol(SB, nmB, true)}</div>
    </div>
  );
  // details under the box for a tapped day
  const dayRows = (L, d) => ((L.days[d] || {}).start || []).map((q) => ({ q, v: q.a != null ? q.a : q.x0 != null ? q.x0 : q.x || 0, real: q.a != null })).sort((u, v) => v.v - u.v);
  const det = sel != null && sel < n ? (
    <div className="dt">
      <div className="ft"><span className="gx-tag">{dayLabel(dates[sel])}</span><button type="button" className="text-xs text-slate-500" onClick={() => setSel(null)}>Close</button></div>
      <div className="cols" style={{ marginTop: 6 }}>
        {[[X, nmA], [Y, nmB]].map(([L, nm], c) => (
          <div key={c} className="min-w-0">
            <div className={"text-xs" + (c ? " text-slate-500" : " font-semibold")}>{nm + " \u00b7 " + f1(c ? B7[sel] : A7[sel])}</div>
            {dayRows(L, sel).map(({ q, v, real }) => <div key={q.id} className="rw"><span>{shortN(q.n)}</span><b style={real ? null : { color: "var(--faint)", fontWeight: 400 }}>{f1(v)}</b></div>)}
            {!dayRows(L, sel).length ? <div className="text-xs text-slate-500" style={{ marginTop: 6 }}>No games</div> : null}
          </div>
        ))}
      </div>
      <div className="text-xs text-slate-500" style={{ marginTop: 6 }}>Grey numbers are projections.</div>
    </div>
  ) : null;
  return (
    <div className={cls}>
      {head}
      <div ref={stg} className="stg" onPointerDown={pDown} onPointerMove={pMove} onPointerUp={pUp} onPointerCancel={pUp}>
        <div ref={pr} className="pr">{fScore}{fWin}{fGames}{fPlayers}</div>
      </div>
      <div className="tb">{["Score", "Win", "Games", "Players"].map((t, j) => <button key={t} type="button" className={k === j ? "on" : ""} onClick={() => turn(j)}>{t}</button>)}</div>
      {det}
    </div>
  );
}
'''

def change(t):
    t = lit(t, "225: styles", "</style>", NEW_CSS, "change 225 (install.py): matchup box")
    t = lit(t, "225: helpers", ROOT, HELPERS + ROOT, "change 225: matchup box on the Roster page")
    t = lit(t, "225: show it", "<GxAutoToday2 go={go} />{/* gx089-today */}{/* gx092-today */}<GxRace s={s} wk={wk} />",
            "<GxAutoToday2 go={go} />{/* gx089-today */}{/* gx092-today */}{top103 ? <GxBox225 s={s} wk={wk} /> : <GxRace s={s} wk={wk} />}",
            "<GxBox225 s={s} wk={wk} />")
    return t

edit(APP, change)
