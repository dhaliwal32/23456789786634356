# changes/226-matchup-box-more.py - Roster: the score at the top goes (the box has it), the box gets a Today side and more on every side

NEW_CSS = r'''  /* change 226 (install.py): fuller matchup box */
  .gx-bx226 .lay { display: grid; grid-template-columns: minmax(0,1fr); gap: 14px; margin-top: 10px; }
  @media (min-width: 900px) { .gx-bx226 .lay { grid-template-columns: minmax(0,1fr) minmax(0,1fr); gap: 18px; align-items: start; } }
  .gx-bx226 .sbd .tg2 { font-size: 12px; color: var(--mute); }
  .gx-bx226 .sbd .row2 { display: grid; grid-template-columns: minmax(0,1fr) 104px minmax(0,1fr); align-items: center; margin-top: 6px; }
  .gx-bx226 .sbd .big { font-size: clamp(28px, 7vw, 40px); font-weight: 600; font-variant-numeric: tabular-nums; line-height: 1.1; }
  .gx-bx226 .stg { height: auto; aspect-ratio: 1 / 1; max-height: 540px; margin-top: 0; }
  .gx-bx226 .wbig { font-size: 19px; font-weight: 600; margin-top: 8px; }
  .gx-bx226 .fc { padding: 13px 13px 12px; }
  .gx-bx226 .fx2 { display: grid; grid-template-columns: repeat(3, minmax(0,1fr)); gap: 6px; margin-top: 9px; padding-top: 9px; border-top: 1px solid var(--line); }
  .gx-bx226 .fx2 div { font-size: 11px; color: var(--mute); min-width: 0; }
  .gx-bx226 .fx2 b { display: block; color: var(--ink); font-size: 13.5px; font-weight: 600; font-variant-numeric: tabular-nums; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .gx-bx226 .fx2 b i { font-style: normal; color: var(--mute); font-weight: 400; }
  .gx-bx226 .tdc { display: grid; grid-template-columns: minmax(0,1fr) minmax(0,1fr); gap: 12px; margin-top: 6px; }
  .gx-bx226 .tr { display: grid; grid-template-columns: minmax(0,1fr) auto; align-items: center; gap: 6px; height: 27px; border-bottom: 1px solid var(--line); font-size: 12px; background: none; border-left: 0; border-right: 0; border-top: 0; padding: 0; color: var(--ink); text-align: left; width: 100%; }
  .gx-bx226 .tr .nm { min-width: 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .gx-bx226 .tr .nm small { color: var(--mute); font-size: 10.5px; margin-left: 4px; }
  .gx-bx226 .tr b { font-weight: 600; font-variant-numeric: tabular-nums; }
  .gx-bx226 .tr b.pj { color: var(--faint); font-weight: 400; }
  .gx-bx226 .tot { display: flex; justify-content: space-between; align-items: baseline; font-size: 12px; margin-bottom: 2px; }
  .gx-bx226 .tot b { font-size: 16px; font-weight: 600; font-variant-numeric: tabular-nums; }
  .gx-bx226 .lf { margin-top: 8px; }
  .gx-bx226 .lf .rw2 { display: flex; justify-content: space-between; font-size: 11.5px; height: 22px; align-items: center; gap: 6px; }
  .gx-bx226 .lf .rw2 span { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; min-width: 0; }
  .gx-bx226 .lf .rw2 b { font-weight: 600; font-variant-numeric: tabular-nums; }
  .gx-bx226 .pl { height: 36px; }
  .gx-bx226 .tb button { padding: 0 9px; }
  .gx-bx225.gx-bx226.full .stg { max-height: 62vh; margin: 0 auto; }
  @media (min-width: 641px) { .gx-bx226 .stg { perspective: 1800px; } }
  .gx-bx226 .fx2 { margin-top: 12px; }
</style>'''

HELPERS = r'''// ---------- change 226: fuller matchup box (install.py) ----------
function GxBox226({ s, wk }) {
  const K = s.blend, today = todayISO(), gen = (window.ESPN_DATA || {}).generated;
  const NF = 4, STEP = 360 / NF, NAMES = ["Today", "Win", "Games", "Players"];
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
  // five sides around the middle of the box; the box turns
  const paint = (a, anim) => {
    const el = pr.current, box = stg.current;
    if (!el || !box) return;
    const z = box.clientWidth / 2 / Math.tan(Math.PI / NF);
    el.classList.toggle("an", !!anim);
    el.style.transform = "translateZ(" + -z + "px) rotateY(" + -a + "deg)";
    [...el.children].forEach((f, j) => {
      f.style.transform = "rotateY(" + j * STEP + "deg) translateZ(" + z + "px)";
      const d = Math.abs((((j * STEP - a) % 360) + 540) % 360 - 180);
      f.style.setProperty("--sh", String(Math.min(0.8, d / 90)));
    });
  };
  const turn = (j) => { const a0 = ang.current; let t = Math.round(a0 / 360) * 360 + j * STEP; while (t - a0 > 180) t -= 360; while (a0 - t > 180) t += 360; ang.current = t; paint(t, true); setK(((j % NF) + NF) % NF); };
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
    ang.current = d.a - dx * 0.36; paint(ang.current, false);
  };
  const pUp = () => {
    const d = drag.current; drag.current = null;
    if (!d || !d.on) return;
    const moved = ang.current - d.a, j = Math.round(d.a / STEP) + (Math.abs(moved) > 20 ? Math.sign(moved) : 0);
    turn(j);
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
  const cls = "gx-pn gx-bx225 gx-bx226" + (full ? " full fixed inset-0" : "");
  const act = (id) => +(gxAct120(w)[id]) || 0;
  const sa = up ? 0 : act(me), sb = up || !opp ? 0 : act(opp);
  const nmA = me === s.me ? "You" : teamName(s, me), nmB = opp ? teamName(s, opp) : "";
  if (fin || !R) {
    return (
      <div className={cls}>{head}
        {fin && opp && (sa || sb) ? (
          <div style={{ paddingTop: 10 }}>
            <div className="sc"><div className="min-w-0"><div className="text-sm font-semibold truncate">{nmA}</div><div className="bg">{f1(sa)}</div></div><div></div><div className="min-w-0 r"><div className="text-sm text-slate-500 truncate">{nmB}</div><div className="bg" style={{ color: "var(--ink2)" }}>{f1(sb)}</div></div></div>
            <div className="text-sm text-slate-500" style={{ marginTop: 6 }}>{sa > sb ? "Won by " + f1(sa - sb) : sa < sb ? "Lost by " + f1(sb - sa) : "Tied"}</div>
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
  const fdays = dates.map((_, d) => d).filter((d) => st(d) === "f"), done = fdays.length, ti = dates.indexOf(today);
  const wp = winProb(X, Y, sa, sb), fa = sa + X.total, fb = sb + Y.total, over = done >= n;
  const DN = (d) => (dates[d] === today ? "Today" : dayLabel(dates[d]).split(",")[0].slice(0, 3));
  const gms = (L, d) => gxGmN(L.days[d]);
  const totG = (L) => dates.reduce((t, _, d) => t + gms(L, d), 0);
  const playedG = (L) => dates.reduce((t, _, d) => t + (st(d) === "p" ? 0 : ((L.days[d] || {}).start || []).filter((q) => q.st === "L" || q.st === "F").length), 0);
  const won = fdays.filter((d) => A7[d] > B7[d]).length, lost = fdays.filter((d) => A7[d] < B7[d]).length;
  const vsA = fdays.reduce((t, d) => t + A7[d] - exp(X, d), 0), vsB = fdays.reduce((t, d) => t + B7[d] - exp(Y, d), 0);
  const sg = (v) => (v >= 0 ? "+" : "\u2212") + f1(Math.abs(v));
  const best = (a7) => fdays.reduce((b, d) => (b == null || a7[d] > a7[b] ? d : b), null);
  const bA = best(A7), bB = best(B7);
  const gpA = playedG(X), gpB = playedG(Y);
  const sdNow = Math.sqrt(projVar(X) + projVar(Y)), remNow = Math.max(1, X.total + Y.total);
  const wHist = fdays.map((d) => {
    let a = 0, b = 0, ra = 0, rb = 0;
    for (let j = 0; j < n; j++) { if (j <= d) { a += A7[j]; b += B7[j]; } else { ra += exp(X, j); rb += exp(Y, j); } }
    const sd = sdNow * Math.sqrt(Math.max(0.05, (ra + rb) / remNow)), m = a + ra - (b + rb);
    return sd > 0 ? normCdf(m / sd) : m > 0 ? 1 : m < 0 ? 0 : 0.5;
  });
  const leftA = X.used, leftB = Y.used, need = fb - sa, perG = leftA ? Math.max(0, need) / leftA : 0;
  // what a swing of 10 points would do to the win chance
  const swing = (v) => { const m = fa + v - fb; return sdNow > 0 ? normCdf(m / sdNow) : m > 0 ? 1 : 0; };
  const SA = gxSum209(s, me, X), SB = gxSum209(s, opp, Y);
  const all = (G) => [...G.F, ...G.D, ...G.G];
  const top = (G, m) => all(G).filter((o) => o.gp || o.left).sort((u, v) => v.pts - u.pts || v.rem - u.rem).slice(0, m);
  const lefts = (G) => all(G).filter((o) => o.left || o.live).sort((u, v) => v.rem - u.rem).slice(0, 3);
  const grpPts = (G, g) => G[g].reduce((t, o) => t + o.pts, 0);
  const openP = (p) => { if (p && window.__NAV) window.__NAV.player(p); };
  const faceTitle = (a, b) => <div className="ft"><span className="gx-tag">{a}</span><span className="text-xs text-slate-500">{b}</span></div>;
  const two = (a, b) => <>{a}<i>{" v " + b}</i></>;
  const dayCell = (d) => (
    <button key={d} type="button" className={"dy" + (dates[d] === today ? " td" : "") + (st(d) === "p" ? " pj" : "") + (sel === d ? " on" : "")} onClick={() => setSel(sel === d ? null : d)}>
      <small>{DN(d)}</small><b>{f1(A7[d])}</b><i>{f1(B7[d])}</i>
    </button>
  );
  const tag = "Week " + (i + 1) + (!n ? "" : up ? " \u00b7 starts " + dayLabel(dates[0]) : over ? " \u00b7 final" : " \u00b7 day " + Math.min(n, done + 1) + " of " + n);
  const mineMu = me === s.me;
  const board = (
    <div className="sbd">
      <div className="tg2">{tag}</div>
      <div className="row2">
        <div className="min-w-0"><div className="text-sm font-semibold truncate">{mineMu ? teamName(s, s.me) : nmA}</div><div className="big"><GxAnimNum131 v={sa} /></div></div>
        <div style={{ display: "flex", justifyContent: "center" }}><GxRing v={wp} big plain={!mineMu} /></div>
        <div className="min-w-0 text-right"><div className="text-sm text-slate-500 truncate">{nmB}</div><div className="big" style={{ color: "var(--ink2)" }}><GxAnimNum131 v={sb} /></div></div>
      </div>
      <div className="shr"><div style={{ width: (sa + sb > 0 ? Math.max(4, Math.min(96, (sa / (sa + sb)) * 100)) : 50) + "%", background: "var(--accent)" }}></div><div style={{ flex: 1, background: "var(--track)" }}></div></div>
      <div className="text-xs text-slate-500" style={{ display: "flex" }}><span>{(over ? "Final " : "Projected ") + f1(fa)}</span><span style={{ margin: "0 auto" }}>{(fa >= fb ? "Ahead by " : "Behind by ") + f1(Math.abs(fa - fb))}</span><span>{f1(fb)}</span></div>
      <div className="dys">{dates.map((_, d) => dayCell(d))}</div>
      <div className="fx2">
        <div>Per game<b>{two(gpA ? f1(sa / gpA) : "\u2013", gpB ? f1(sb / gpB) : "\u2013")}</b></div>
        <div>Days won<b>{done ? two(won, lost) : "\u2013"}</b></div>
        <div>Best day<b>{bA != null ? two(f1(A7[bA]), f1(B7[bB])) : "\u2013"}</b></div>
        <div>Forwards<b>{two(f1(grpPts(SA, "F")), f1(grpPts(SB, "F")))}</b></div>
        <div>Defence<b>{two(f1(grpPts(SA, "D")), f1(grpPts(SB, "D")))}</b></div>
        <div>Goalies<b>{two(f1(grpPts(SA, "G")), f1(grpPts(SB, "G")))}</b></div>
        <div>Points left<b>{two(f1(X.total), f1(Y.total))}</b></div>
        <div>Games left<b>{two(leftA, leftB)}</b></div>
        <div>Vs projection<b>{done ? two(sg(vsA), sg(vsB)) : "\u2013"}</b></div>
      </div>
    </div>
  );
  // today: everyone in today's lineup for both teams, live points or projection
  const tRows = (L) => ti < 0 ? [] : ((L.days[ti] || {}).start || []).map((q) => ({ q, v: q.a != null ? q.a : q.x0 != null ? q.x0 : q.x || 0, real: q.a != null, g: gState(q.t, today) })).sort((u, v) => (u.real === v.real ? v.v - u.v : u.real ? -1 : 1));
  const tA = tRows(X), tB = tRows(Y), tSum = (r) => r.filter((x) => x.real).reduce((t, x) => t + x.v, 0), tProj = (r) => r.reduce((t, x) => t + x.v, 0);
  const tCol = (rows, nm, dim) => (
    <div className="min-w-0">
      <div className="tot"><span className={dim ? "text-slate-500" : "font-semibold"}>{nm}</span><b>{f1(tSum(rows))}<span className="text-xs text-slate-500" style={{ fontWeight: 400 }}>{" / " + f1(tProj(rows))}</span></b></div>
      {rows.slice(0, 9).map(({ q, v, real, g }) => (
        <button key={q.id} type="button" className="tr" onClick={() => openP(q)}>
          <span className="nm">{lastN(q.n)}<small>{g.s === "L" ? "live" : g.s === "F" ? "final" : gameTime(gameOf(q.t, today))}</small></span>
          <b className={real ? "" : "pj"}>{f1(v)}</b>
        </button>
      ))}
      {rows.length > 9 ? <div className="text-xs text-slate-500" style={{ marginTop: 4 }}>{"+" + (rows.length - 9) + " more"}</div> : null}
      {!rows.length ? <div className="text-xs text-slate-500" style={{ marginTop: 6 }}>No games today</div> : null}
    </div>
  );
  const fToday = (
    <div className="fc">
      {faceTitle("Today", ti < 0 ? "Not in this week" : tA.filter((x) => x.g.s === "L").length + tB.filter((x) => x.g.s === "L").length + " playing now")}
      {ti < 0 ? <div className="text-sm text-slate-500" style={{ marginTop: 10 }}>Today is not part of this week. Tap a day on the Score side to see its lineups.</div> : (
        <>
          <div className="text-xs text-slate-500" style={{ marginTop: 4 }}>{"Lineup games " + tA.length + " v " + tB.length + " \u00b7 points so far / with projection"}</div>
          <div className="tdc">{tCol(tA, nmA, false)}{tCol(tB, nmB, true)}</div>
        </>
      )}
    </div>
  );
  const W0 = 300, H0 = 80, px = (j) => 14 + (W0 - 28) * (wHist.length > 1 ? j / (wHist.length - 1) : 0.5), py = (v) => 8 + (1 - v) * (H0 - 26);
  const fWin = (
    <div className="fc">
      {faceTitle("Win chance", over ? "Final" : "Now")}
      <div className="wbig">{over ? (sa >= sb ? "Won by " + f1(sa - sb) : "Lost by " + f1(sb - sa)) : (fa >= fb ? "On pace to win by " : "On pace to lose by ") + f1(Math.abs(fa - fb))}</div>
      {over ? null : <div className="text-xs text-slate-500" style={{ marginTop: 4 }}>{"They should finish near " + f1(fb) + ". You need " + f1(Math.max(0, need)) + " more" + (leftA ? ", " + f1(perG) + " a game left." : ".")}</div>}
      <div className="gx-tag" style={{ marginTop: 12 }}>After each day</div>
      {wHist.length ? (
        <svg viewBox={"0 0 " + W0 + " " + H0} width="100%" height={H0} className="gx-svg" style={{ display: "block", marginTop: 2 }} role="img" aria-label="Win chance after each day">
          <line x1={0} x2={W0} y1={py(0.5)} y2={py(0.5)} style={{ stroke: "var(--line2, var(--line))", strokeDasharray: "3 4" }} />
          {wHist.length > 1 ? <polyline points={wHist.map((v, j) => px(j).toFixed(1) + "," + py(v).toFixed(1)).join(" ")} style={{ fill: "none", stroke: "var(--accent)", strokeWidth: 2, strokeLinejoin: "round" }} /> : null}
          {wHist.map((v, j) => <g key={j}><circle cx={px(j)} cy={py(v)} r={3} style={{ fill: "var(--accent)" }} /><text x={px(j)} y={py(v) - 7} textAnchor="middle" style={{ fontSize: 10, fill: "var(--ink2)" }}>{Math.round(v * 100)}</text><text x={px(j)} y={H0 - 2} textAnchor="middle" style={{ fontSize: 10, fill: "var(--mute)" }}>{DN(fdays[j])}</text></g>)}
        </svg>
      ) : <div className="text-xs text-slate-500" style={{ marginTop: 8 }}>Shows once the first day is over.</div>}
      <div className="fx2">
        <div>If you add 10<b>{over ? "\u2013" : wpTxt(swing(10))}</b></div>
        <div>If they add 10<b>{over ? "\u2013" : wpTxt(swing(-10))}</b></div>
        <div>Need a game<b>{over || !leftA ? "\u2013" : f1(perG)}</b></div>
        <div>Their pace<b>{f1(fb)}</b></div>
        <div>Your pace<b>{f1(fa)}</b></div>
        <div>Spread<b>{"\u00b1" + f1(sdNow)}</b></div>
      </div>
    </div>
  );
  const maxG = Math.max(1, ...dates.map((_, d) => Math.max(gms(X, d), gms(Y, d))));
  const gCell = (L, d, mine) => { const g = gms(L, d), fut = st(d) === "p"; return <div key={d} className="c" style={{ background: fut ? "transparent" : mine ? "rgba(127,127,127," + (0.08 + 0.32 * g / maxG) + ")" : "rgba(127,127,127," + (0.05 + 0.18 * g / maxG) + ")", border: fut ? "1px dashed var(--line)" : "0", color: fut ? "var(--faint)" : mine ? "var(--ink)" : "var(--ink2)" }}>{g}</div>; };
  const gToday = (L) => ti < 0 ? 0 : gms(L, ti);
  const fGames = (
    <div className="fc">
      {faceTitle("Lineup games", up ? "Projected" : "Left " + leftA + " v " + leftB)}
      <div className="gr">
        <div></div>{dates.map((_, d) => <div key={d} className="h" style={dates[d] === today ? { color: "var(--ink)", fontWeight: 600 } : null}>{DN(d)}</div>)}<div className="h">{up ? "All" : "Left"}</div>
        <div className="n">{nmA}</div>{dates.map((_, d) => gCell(X, d, true))}<div className="t">{up ? totG(X) : leftA}</div>
        <div className="n text-slate-500">{nmB}</div>{dates.map((_, d) => gCell(Y, d, false))}<div className="t text-slate-500">{up ? totG(Y) : leftB}</div>
      </div>
      <div className="fx2" style={{ marginTop: 14 }}>
        <div>All week<b>{two(totG(X), totG(Y))}</b></div>
        <div>Played<b>{two(gpA, gpB)}</b></div>
        <div>Today<b>{two(gToday(X), gToday(Y))}</b></div>
        <div>Bench with a game<b>{two(X.wasted || 0, Y.wasted || 0)}</b></div>
        <div>Empty spots<b>{two(X.empty || 0, Y.empty || 0)}</b></div>
        <div>Vs projection<b>{done ? two(sg(vsA), sg(vsB)) : "\u2013"}</b></div>
      </div>
    </div>
  );
  const pCol = (G, nm, dim) => (
    <div className="min-w-0">
      <div className={"text-xs truncate" + (dim ? " text-slate-500" : " font-semibold")} style={{ marginBottom: 2 }}>{nm}</div>
      {top(G, 5).map((o) => (
        <button key={o.p.id} type="button" className="pl" onClick={() => openP(o.p)}>
          <GxFace p={o.p} size={20} />
          <span className="nm"><b>{lastN(o.p.n)}</b><span>{o.p.t + " \u00b7 " + o.gp + " GP" + (o.left ? " \u00b7 " + o.left + " left" : "")}</span></span>
          <span className="pt" style={dim ? { color: "var(--ink2)" } : null}>{f1(o.pts)}</span>
        </button>
      ))}
      <div className="lf"><div className="gx-tag">Most left to give</div>
        {lefts(G).map((o) => <div key={o.p.id} className="rw2"><span>{lastN(o.p.n) + " \u00b7 " + o.left + (o.live ? " live" : " left")}</span><b>{"+" + f1(o.rem)}</b></div>)}
        {!lefts(G).length ? <div className="text-xs text-slate-500">No games left</div> : null}
      </div>
    </div>
  );
  const fPlayers = (
    <div className="fc">
      {faceTitle("Players", "Points this week")}
      <div className="kp">{pCol(SA, nmA, false)}{pCol(SB, nmB, true)}</div>
    </div>
  );
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
      <div className="lay">
        <div className="min-w-0">{board}{det}</div>
        <div className="min-w-0">
          <div ref={stg} className="stg" onPointerDown={pDown} onPointerMove={pMove} onPointerUp={pUp} onPointerCancel={pUp}>
            <div ref={pr} className="pr">{fToday}{fWin}{fGames}{fPlayers}</div>
          </div>
          <div className="tb">{NAMES.map((t, j) => <button key={t} type="button" className={k === j ? "on" : ""} onClick={() => turn(j)}>{t}</button>)}</div>
        </div>
      </div>
    </div>
  );
}
'''

TOP_OLD = '''    <div className="space-y-3">
      <div>
        <div className="gx-tag">{tag}</div>'''
TOP_NEW = '''    <div className="space-y-3">
      <div style={top103 ? { display: "none" } : null} data-gx="226top">
        <div className="gx-tag">{tag}</div>'''

SORT_HELP = r'''// ---------- change 226: Players list headings use one sort at a time (install.py) ----------
function gxClr226() { if (GX108.k) { GX108.k = null; GX108.dir = 1; window.dispatchEvent(new Event("gx-sort108")); } }
'''

def fix_sort(t):
    i = t.index('<GxSH k="l5" cur={srt79}')
    j = t.index('{/* gx109h */}', i)
    seg = t[i:j]
    if 'gxClr226' in seg:
        return t
    seg2 = seg.replace('cur={srt79}', 'cur={GX108.k ? "" : srt79}').replace('set={(v) => { setSrt79(v); setLimit(40); }}', 'set={(v) => { gxClr226(); setSrt79(v); setLimit(40); }}')
    seg2 = seg2.replace('<span className="n">Avg</span>', '<GxHB108 k="Avg" />', 1)
    if seg2 == seg or 'gxClr226' not in seg2 or 'GxHB108 k="Avg"' not in seg2:
        fail("226: Players headings not found as expected")
    return t[:i] + seg2 + t[j:]

def change(t):
    t = lit(t, "226: styles", "</style>", NEW_CSS, "change 226 (install.py): fuller matchup box")
    t = lit(t, "226: helpers", ROOT, HELPERS + ROOT, "change 226: fuller matchup box")
    t = lit(t, "226: use it", "{top103 ? <GxBox225 s={s} wk={wk} /> : <GxRace s={s} wk={wk} />}", "{top103 ? <GxBox226 s={s} wk={wk} /> : <GxRace s={s} wk={wk} />}", "<GxBox226 s={s} wk={wk} />")
    t = lit(t, "226: top score hidden on Roster", TOP_OLD, TOP_NEW, 'data-gx="226top"')
    t = lit(t, "226: sort helper", ROOT, SORT_HELP + ROOT, "change 226: Players list headings use one sort")
    t = fix_sort(t)
    return t

edit(APP, change)
