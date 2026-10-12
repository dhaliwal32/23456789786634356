# changes/070-score-race.py - This week box becomes a score race for any week; best move moves into it
NEW_CSS = r'''  /* change 070 (install.py) */
  .gx-rf { display: grid; grid-template-columns: repeat(3, minmax(0,1fr)); border-top: 1px solid var(--line); margin-top: 6px; }
  .gx-rf > div { padding: 10px 0 2px; min-width: 0; }
  .gx-rf > div + div { padding-left: 12px; border-left: 1px solid var(--line); }
  .gx-rf small { display: block; font-size: 12px; color: var(--mute); }
  .gx-rf b { font-weight: 600; font-size: 16px; font-variant-numeric: tabular-nums; }
  .gx-rt { display: grid; grid-template-columns: 96px minmax(0,1fr) minmax(0,1fr); row-gap: 5px; column-gap: 8px; font-size: 13px; border-top: 1px solid var(--line); margin-top: 10px; padding-top: 10px; font-variant-numeric: tabular-nums; }
  .gx-rt .l { color: var(--mute); }
  @media (max-width: 640px) { .gx-rf b { font-size: 15px; } .gx-rf > div + div { padding-left: 8px; } .gx-rt { grid-template-columns: 70px minmax(0,1fr) minmax(0,1fr); } }
'''

NEW_JS = r'''// ---------- change 070: This week box as a score race, any week (install.py) ----------
function GxRace({ s, wk }) {
  const K = s.blend, today = todayISO(), gen = (window.ESPN_DATA || {}).generated;
  const [pick, setPick] = useState(null);
  const [sel, setSel] = useState(null);
  const [W, setW] = useState(620);
  const box = React.useRef(null);
  const touch = React.useRef(null);
  useEffect(() => {
    const el = box.current;
    if (!el) return;
    const fit = () => setW(Math.max(290, Math.round(el.clientWidth - 28)));
    fit();
    if (window.ResizeObserver) { const ro = new ResizeObserver(fit); ro.observe(el); return () => ro.disconnect(); }
    window.addEventListener("resize", fit);
    return () => window.removeEventListener("resize", fit);
  }, []);
  useEffect(() => {
    const h = () => { setPick(Math.min(s.weeks.length - 1, s.wk + 1)); setSel(null); if (box.current) box.current.scrollIntoView({ behavior: "smooth", block: "start" }); };
    window.addEventListener("gx-race-next", h);
    return () => window.removeEventListener("gx-race-next", h);
  }, [s.wk, s.weeks.length]);
  const i = gxWkAt61(s, pick), cur = i === s.wk;
  const go = (k) => { setPick(Math.max(0, Math.min(s.weeks.length - 1, k))); setSel(null); };
  const w = useMemo(() => (cur ? wk : deriveWeek(s.weeks[i], s.autoDone)), [cur, wk, s.weeks, i, s.autoDone]);
  const dates = w.dates || [], n = dates.length;
  const opp = oppOf(w, s.me) || (cur ? s.opp : null);
  const up = !(n > 0 && dates[0] <= today), fin = !cur && n > 0 && dates[n - 1] < today;
  const R = useMemo(() => {
    if (!opp || !n || fin) return null;
    const run = (id) => weekLive(s.players.filter((p) => p.ft === id), w, K, id, { detail: true });
    return [run(s.me), run(opp)];
  }, [w, opp, fin, s.players, K, gen, window.__PMODE]);
  const mv = useMemo(() => {
    if (!up || !opp || !R) return null;
    try {
      const sW = { ...s, wk: i };
      const r = computeMoves(sW, { H: 1, pool: 40 }).res.filter((x) => x.gain >= (s.minGain ?? 3))[0];
      if (!r) return { none: true };
      return { r, b: winChance(sW), a: winChance(sW, afterMove(sW, r.f, r.d)) };
    } catch (e) { return null; }
  }, [up, i, opp, R]);
  const act = (id) => +((w.act || {})[id]) || 0;
  const sa = up ? 0 : act(s.me), sb = up || !opp ? 0 : act(opp);
  const nm0 = opp ? (teamName(s, opp) || "").split(" ")[0] : "", nm = nm0.length > 10 ? nm0.slice(0, 9) + "\u2026" : nm0;
  const title = cur ? "This week" : up && i === s.wk + 1 ? "Next week" : "Week " + (i + 1);
  const head = (
    <div style={{ display: "flex", alignItems: "center", gap: 8, flexWrap: "wrap" }}>
      <span className="gx-tag">{title}{opp ? " \u00b7 vs " + teamName(s, opp) : ""}</span>
      <GxWkPick s={s} i={i} go={go} />
    </div>
  );
  const wrapP = { className: "gx-pn", ref: box, style: { minWidth: 0, touchAction: "pan-y" }, ...gxSwipe61(touch, i, go) };
  if (fin || !R) {
    return (
      <div {...wrapP}>{head}
        {fin && opp && (sa || sb) ? (
          <div style={{ display: "flex", alignItems: "baseline", gap: 10, paddingTop: 10, fontVariantNumeric: "tabular-nums" }}>
            <span className="gx-stv">{f1(sa)}</span><span className="text-slate-500">to {f1(sb)}</span>
            <span style={{ color: sa > sb ? "var(--good)" : sa < sb ? "var(--bad)" : "var(--mute)" }}>{sa > sb ? "Won by " + f1(sa - sb) : sa < sb ? "Lost by " + f1(sb - sa) : "Tied"}</span>
          </div>
        ) : <div className="text-sm text-slate-500" style={{ paddingTop: 10 }}>{fin ? "No result saved for this week." : "The matchup for this week is not set yet."}</div>}
        {fin ? <div className="text-xs text-slate-500" style={{ marginTop: 6 }}>Day by day scores are only kept for the current week.</div> : null}
      </div>
    );
  }
  const X = R[0], Y = R[1];
  const st = (d) => (dates[d] < today ? "f" : dates[d] === today ? "t" : "p");
  const pts = (L, d) => { const x = L.days[d] || {}, k = st(d); return k === "f" ? x.act || 0 : k === "t" ? (x.act || 0) + (x.total || 0) : x.total || 0; };
  const exp = (L, d) => { const x = L.days[d] || {}; return x.proj != null ? x.proj : x.total || 0; };
  const me = dates.map((_, d) => pts(X, d)), th = dates.map((_, d) => pts(Y, d));
  const cum = (a) => { let t = 0; return a.map((v) => (t += v)); };
  const CA = cum(me), CB = cum(th);
  const fdays = dates.map((_, d) => d).filter((d) => st(d) === "f"), done = fdays.length;
  const EA = cum(dates.map((_, d) => exp(X, d))), EB = cum(dates.map((_, d) => exp(Y, d)));
  const wp = winProb(X, Y, sa, sb), fa = sa + X.total, fb = sb + Y.total;
  const ti = dates.indexOf(today), d0 = sel != null && sel < n ? sel : ti >= 0 ? ti : up ? 0 : n - 1;
  const narrow = W < 480, gut = narrow ? 80 : 108, L0 = 4, R0 = W - gut, cw = (R0 - L0) / n, cx = (d) => L0 + cw * (d + 0.5);
  const topV = Math.max(CA[n - 1], CB[n - 1], done ? Math.max(EA[done - 1], EB[done - 1]) : 0, 1) * 1.06;
  const base = 172, yy = (v) => base - (v / topV) * 158, Hh = narrow ? 230 : 214;
  const P = (a, from, to) => a.slice(from, to + 1).map((v, k) => cx(from + k).toFixed(1) + "," + yy(v).toFixed(1)).join(" ");
  const ln = (col, dash, wdt, op) => ({ fill: "none", stroke: col, strokeWidth: wdt || 2, strokeDasharray: dash || "none", strokeLinejoin: "round", strokeLinecap: "round", opacity: op || 1 });
  const segs = [];
  for (let k = 0; k < n - 1; k++) {
    const ah = CA[k + 1] >= CB[k + 1];
    segs.push(<polygon key={"g" + k} points={[cx(k) + "," + yy(CA[k]), cx(k + 1) + "," + yy(CA[k + 1]), cx(k + 1) + "," + yy(CB[k + 1]), cx(k) + "," + yy(CB[k])].join(" ")} style={{ fill: ah ? "var(--good)" : "var(--bad)", opacity: 0.1 }} />);
  }
  let ya = yy(CA[n - 1]) + 4, yb = yy(CB[n - 1]) + 4;
  if (Math.abs(ya - yb) < 15) { const m = (ya + yb) / 2, sg1 = ya <= yb ? -1 : 1; ya = m + sg1 * 7.5; yb = m - sg1 * 7.5; }
  ya = Math.max(12, ya); yb = Math.max(12, yb);
  const lx = cx(n - 1) + 12, fs = narrow ? 11 : 12;
  const sg = (v) => (v >= 0 ? "+" : "\u2212") + Math.round(Math.abs(v));
  const DN = (d) => (dates[d] === today ? "Today" : dayLabel(dates[d]).split(",")[0]);
  const rng = up || !done ? dates.map((_, d) => d) : fdays;
  const won = rng.filter((d) => me[d] > th[d]).length;
  const bD = rng.reduce((b, d) => (b == null || me[d] - th[d] > me[b] - th[b] ? d : b), null);
  const bestTxt = bD != null && me[bD] > th[bD] ? "best " + DN(bD) + " " + sg(me[bD] - th[bD]) : "";
  const vsA = fdays.reduce((t, d) => t + me[d] - exp(X, d), 0), vsB = fdays.reduce((t, d) => t + th[d] - exp(Y, d), 0);
  const gms = (L, d) => ((L.days[d] || {}).start || []).length;
  const totG = (L) => dates.reduce((t, _, d) => t + gms(L, d), 0);
  const topOf = (L) => { const t = ((L || {}).start || []).filter((p) => p.x > 0).sort((a, b) => b.x - a.x)[0]; return t ? shortN(t.n) + " " + f1(t.x) : "\u2013"; };
  const fact = (key, label, big, sub, col) => (<div key={key}><small>{label}</small><b style={col ? { color: col } : null}>{big}</b>{sub ? <span className="text-sm text-slate-500">{" " + sub}</span> : null}</div>);
  const facts = up ? [
    fact("g", "Lineup games", totG(X), "them " + totG(Y)),
    fact("d", "Days favoured", won + " of " + n, bestTxt),
    fact("m", "Best move", mv ? (mv.none ? "None worth it" : lastN(mv.r.f.n) + " in") : "\u2026", mv && !mv.none ? lastN(mv.r.d.n) + " out" + (mv.a != null && mv.b != null ? " \u00b7 " + wpTxt(mv.b).replace("%", "") + " \u2192 " + wpTxt(mv.a) : "") : ""),
  ] : [
    done ? fact("v", "Against projection", sg(vsA), "them " + sg(vsB), vsA >= 0 ? "var(--good)" : "var(--bad)") : fact("g", "Lineup games", totG(X), "them " + totG(Y)),
    fact("l", "Lineup games left", X.used, "them " + Y.used),
    done ? fact("w", "Days won", won + " of " + done, bestTxt) : fact("d", "Days favoured", won + " of " + n, bestTxt),
  ];
  const k0 = st(d0), m0 = me[d0] - th[d0], x0 = X.days[d0] || {}, y0 = Y.days[d0] || {};
  const mc = (v) => ({ color: v >= 0 ? "var(--good)" : "var(--bad)" });
  return (
    <div {...wrapP}>
      {head}
      <div className="text-xs text-slate-500" style={{ marginTop: 4 }}>
        {(done >= n ? "Final " : "Projected ") + Math.round(fa) + " \u2013 " + Math.round(fb) + " \u00b7 "}<span style={{ color: wp >= 0.5 ? "var(--good)" : "var(--bad)" }}>{wpTxt(wp) + " to win"}</span>
      </div>
      <svg viewBox={"0 0 " + W + " " + Hh} width="100%" className="gx-svg" style={{ display: "block", marginTop: 8 }} role="img" aria-label="Running total for both teams through the week">
        <rect x={cx(d0) - cw / 2 + 2} y={4} width={cw - 4} height={Hh - 6} rx={6} style={{ fill: "var(--accentSoft)" }} />
        <line x1={L0} x2={R0} y1={base} y2={base} style={{ stroke: "var(--line)" }} />
        {segs}
        {done >= 2 ? <polyline points={P(EB, 0, done - 1)} style={ln("var(--mute)", "2 4", 1, 0.6)} /> : null}
        {done >= 2 ? <polyline points={P(EA, 0, done - 1)} style={ln("var(--accent)", "2 4", 1, 0.45)} /> : null}
        {done < n ? <polyline points={P(CB, Math.max(0, done - 1), n - 1)} style={ln("var(--mute)", "5 4")} /> : null}
        {done < n ? <polyline points={P(CA, Math.max(0, done - 1), n - 1)} style={ln("var(--accent)", "5 4")} /> : null}
        {done >= 2 ? <polyline points={P(CB, 0, done - 1)} style={ln("var(--mute)")} /> : null}
        {done >= 2 ? <polyline points={P(CA, 0, done - 1)} style={ln("var(--accent)")} /> : null}
        {fdays.map((d) => <g key={"f" + d}><circle cx={cx(d)} cy={yy(CB[d])} r={2.5} style={{ fill: "var(--mute)" }} /><circle cx={cx(d)} cy={yy(CA[d])} r={2.5} style={{ fill: "var(--accent)" }} /></g>)}
        <circle cx={cx(d0)} cy={yy(CB[d0])} r={4.5} style={k0 === "f" ? { fill: "var(--mute)", stroke: "var(--card)", strokeWidth: 2 } : { fill: "var(--card)", stroke: "var(--mute)", strokeWidth: 2 }} />
        <circle cx={cx(d0)} cy={yy(CA[d0])} r={4.5} style={k0 === "f" ? { fill: "var(--accent)", stroke: "var(--card)", strokeWidth: 2 } : { fill: "var(--card)", stroke: "var(--accent)", strokeWidth: 2 }} />
        <text x={lx} y={ya} style={{ fontSize: fs, fill: "var(--accent)", fontWeight: 600 }}>{"You " + Math.round(CA[n - 1])}</text>
        <text x={lx} y={yb} style={{ fontSize: fs, fill: "var(--mute)" }}>{nm + " " + Math.round(CB[n - 1])}</text>
        {dates.map((dt, d) => {
          const on = d === d0, win = me[d] > th[d] + 0.05;
          return (
            <g key={dt}>
              <text x={cx(d)} y={192} textAnchor="middle" style={{ fontSize: fs, fill: on ? "var(--ink)" : "var(--mute)", fontWeight: on ? 600 : 400 }}>{DN(d)}</text>
              {narrow ? <text x={cx(d)} y={208} textAnchor="middle" style={{ fontSize: fs, fill: win ? "var(--good)" : "var(--ink2)" }}>{Math.round(me[d])}</text> : <text x={cx(d)} y={209} textAnchor="middle" style={{ fontSize: fs, fill: win ? "var(--good)" : "var(--ink2)" }}>{Math.round(me[d]) + "\u2013" + Math.round(th[d])}</text>}
              {narrow ? <text x={cx(d)} y={223} textAnchor="middle" style={{ fontSize: fs, fill: "var(--mute)" }}>{Math.round(th[d])}</text> : null}
              <rect x={cx(d) - cw / 2} y={0} width={cw} height={Hh} style={{ fill: "transparent", cursor: "pointer" }} onClick={() => setSel(d)} />
            </g>
          );
        })}
      </svg>
      <div className="gx-rf">{facts}</div>
      <div className="gx-rt">
        <span className="l">{dayLabel(dates[d0])}</span><span style={{ color: "var(--accent)", fontWeight: 600 }}>You</span><span className="text-slate-500 truncate">{teamName(s, opp)}</span>
        {k0 === "f" ? <><span className="l">Points</span><span>{f1(me[d0]) + " "}<span style={mc(m0)}>{(m0 >= 0 ? "won by " : "lost by ") + f1(Math.abs(m0))}</span></span><span>{f1(th[d0])}</span>
          <span className="l">Vs expected</span><span style={mc(me[d0] - exp(X, d0))}>{sg(me[d0] - exp(X, d0))}</span><span style={mc(th[d0] - exp(Y, d0))}>{sg(th[d0] - exp(Y, d0))}</span></> : null}
        {k0 === "t" ? <><span className="l">So far</span><span>{f1(x0.act || 0)}</span><span>{f1(y0.act || 0)}</span>
          <span className="l">Projected</span><span>{f1(me[d0]) + " "}<span style={mc(m0)}>{(m0 >= 0 ? "ahead by " : "behind by ") + f1(Math.abs(m0))}</span></span><span>{f1(th[d0])}</span></> : null}
        {k0 === "p" ? <><span className="l">Projected</span><span>{f1(me[d0]) + " "}<span style={mc(m0)}>{(m0 >= 0 ? "ahead by " : "behind by ") + f1(Math.abs(m0))}</span></span><span>{f1(th[d0])}</span></> : null}
        <span className="l">Lineup games</span><span>{gms(X, d0)}</span><span>{gms(Y, d0)}</span>
        {k0 === "p" ? <><span className="l">Top pick</span><span className="truncate">{topOf(x0)}</span><span className="truncate">{topOf(y0)}</span></> : null}
      </div>
    </div>
  );
}

'''

APP_END = 'ReactDOM.createRoot(document.getElementById("root")).render(<App />);'
PAT_BOX = r'<div className="gx-pn"><b></b><b></b><b></b><b></b>\s*<div style=\{\{ display: "flex", alignItems: "baseline" \}\}>\s*<span className="gx-tag">This week</span>.*?<GxWeek wk=\{wk\} A=\{A\} B=\{B\} aA=\{aA\} aB=\{aB\} />\s*</div>'
PAT_BEST = r'\{best \? \(\s*<button type="button" className="w-full text-left".*?No move worth making right now\.</div>\}'
PAT_CALC = r'const best = useMemo\(\(\) => \{\s*const r = computeMoves\(sP, \{ H: 1, pool: 40 \}\).*?\}, \[sP\]\);'
NEXT_LINK = r'''<button type="button" className="text-sm text-blue-600" style={{ marginTop: 8 }} onClick={() => window.dispatchEvent(new Event("gx-race-next"))}>See next week's forecast</button>'''


def one(t, label, pat, repl):
    found = re.findall(pat, t, flags=re.S)
    if len(found) != 1:
        fail("070: " + label + " was found " + str(len(found)) + " times, expected once.")
    return re.sub(pat, lambda m: repl, t, count=1, flags=re.S)


def change(t):
    if "function GxRace(" in t:
        print("070: already done")
        return t
    t = lit(t, "070: styles", "</style>", NEW_CSS + "</style>", "change 070 (install.py)")
    t = one(t, "the This week box on Today", PAT_BOX, "<GxRace s={s} wk={wk} />")
    t = one(t, "the best move on the Next week panel", PAT_BEST, NEXT_LINK)
    t = one(t, "the best move calculation on Today", PAT_CALC, "")
    if t.count(APP_END) != 1:
        fail("070: could not find the last line of the app.")
    t = t.replace(APP_END, NEW_JS + APP_END, 1)
    for must in ("function Today(", "function GxRace(", "<GxRace s={s} wk={wk} />", "gx-race-next"):
        if must not in t:
            fail("fantasy-gm.html looks damaged after change 070 (" + must + ").")
    return t


edit(APP, change)
