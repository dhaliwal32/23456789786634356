# changes/209-matchup-day-picker-summary.py - Matchup: tap the day name to pick any day of the week or Summary (every player's points this week)

NEW_CSS = r'''  /* change 209 (install.py) */
  .gx-dp209 { position: relative; }
  .gx-dp209 > .bt { display: block; width: 100%; background: none; border: 0; color: inherit; font: inherit; cursor: pointer; padding: 2px 6px; border-radius: 8px; }
  .gx-dp209 > .bt:hover { background: var(--accentSoft); }
  .gx-dp209 .cv { font-size: 11px; color: var(--mute); margin-left: 6px; display: inline-block; transition: transform .18s ease; }
  .gx-dp209 .cv.up { transform: rotate(180deg); }
  .gx-dp209 .mn209 { position: absolute; top: calc(100% + 6px); left: 50%; transform: translateX(-50%); width: 230px; z-index: 40; background: var(--card); border: 1px solid var(--line2); border-radius: 12px; box-shadow: 0 10px 30px rgba(0,0,0,.35); padding: 6px; text-align: left; animation: gxDp209 .16s ease; }
  @keyframes gxDp209 { from { opacity: 0; transform: translate(-50%, -6px); } to { opacity: 1; transform: translate(-50%, 0); } }
  .gx-dp209 .rw { display: grid; grid-template-columns: minmax(0,1fr) 64px; align-items: center; height: 40px; width: 100%; padding: 0 10px; border: 0; background: none; color: var(--ink); font-size: 14px; font-weight: 500; border-radius: 8px; cursor: pointer; }
  .gx-dp209 .rw span:first-child { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; text-align: left; }
  .gx-dp209 .rw span:last-child { text-align: right; font-size: 13px; font-variant-numeric: tabular-nums; }
  .gx-dp209 .rw.on { background: var(--accentSoft); }
  .gx-dp209 .rw:hover { background: var(--accentSoft); }
  .gx-dp209 .sep { height: 1px; background: var(--line); margin: 4px 6px; }
  .gx-ws209 .gx-gd209 { font-size: 11px; letter-spacing: .06em; color: var(--mute); padding: 10px 0 4px; border-top: 2px solid var(--line2, var(--line)); text-align: center; }
  .gx-ws209 .gx-sub209 { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .gx-ws209 .gx-h2h > .gx-pc { min-height: 48px !important; }
  @media (max-width: 640px) { .gx-ws209 .gx-h2h > .gx-pc { min-height: 40px !important; } }
  .gx-ws209 .gx-dr209 { font-size: 11px; color: var(--bad); margin-left: 6px; font-weight: 400; }
</style>'''

HELPERS = r'''// ---------- change 209: Matchup day picker and week Summary (install.py) ----------
function GxDayPick209({ dates, d, sum, today, onDay, onSum, dv, wkDv, mine }) {
  const [op, setOp] = useState(false);
  const ref = React.useRef(null);
  useEffect(() => {
    if (!op) return;
    const f = (e) => { if (ref.current && !ref.current.contains(e.target)) setOp(false); };
    const k = (e) => { if (e.key === "Escape") setOp(false); };
    document.addEventListener("pointerdown", f); window.addEventListener("keydown", k);
    return () => { document.removeEventListener("pointerdown", f); window.removeEventListener("keydown", k); };
  }, [op]);
  const col = (v) => ({ color: !mine || Math.abs(v) < 0.05 ? "var(--mute)" : v > 0 ? "var(--good)" : "var(--bad)" });
  const sg = (v) => (v > 0 ? "+" : "") + f1(v);
  const lb = (x) => (x === today ? "Today" : x ? dayLabel(x) : "");
  const cur = sum ? wkDv : dv(d);
  return (
    <div className="dt gx-dp209" ref={ref} data-gx="209">
      <button type="button" className="bt" aria-expanded={op} onClick={() => setOp(!op)}>
        {sum ? "Summary" : lb(dates[d])}<span className={"cv" + (op ? " up" : "")}>{"\u25be"}</span>
        <small style={col(cur)}>{sg(cur)}</small>
      </button>
      {op ? (
        <div className="mn209">
          <button type="button" className={"rw" + (sum ? " on" : "")} onClick={() => { onSum(); setOp(false); }}><span>Summary (week)</span><span style={col(wkDv)}>{sg(wkDv)}</span></button>
          <div className="sep"></div>
          {dates.map((x, i) => {
            const v = dv(i), fut = x > today;
            return <button key={x} type="button" className={"rw" + (!sum && i === d ? " on" : "")} onClick={() => { onDay(i); setOp(false); }}><span>{lb(x)}</span><span style={fut ? { color: "var(--mute)" } : col(v)}>{(fut ? "proj " : "") + sg(v)}</span></button>;
          })}
        </div>
      ) : null}
    </div>
  );
}
const gxSum209 = (s, id, R) => {
  const m = {};
  const add = (p) => { if (!m[p.id]) m[p.id] = { p, pts: 0, gp: 0, left: 0, rem: 0, live: false }; return m[p.id]; };
  s.players.filter((p) => p.ft === id).forEach(add);
  ((R && R.days) || []).forEach((dy) => (dy.start || []).forEach((q) => {
    const o = add(q);
    if (q.st === "L" || q.st === "F") {
      if (q.a != null) o.pts += +q.a || 0;
      o.gp++;
      if (q.st === "L") { o.live = true; o.rem += q.x || 0; }
    } else { o.left++; o.rem += q.x || 0; }
  }));
  const G = { F: [], D: [], G: [] };
  Object.values(m).forEach((o) => G[o.p.p === "G" ? "G" : o.p.p === "D" ? "D" : "F"].push(o));
  Object.values(G).forEach((l) => l.sort((u, v) => v.pts - u.pts || v.rem - u.rem || (u.p.n < v.p.n ? -1 : 1)));
  return G;
};
function GxWkSum209({ s, a, b, A, B, aA, aB, fa, fb, mine }) {
  const SA = gxSum209(s, a, A), SB = gxSum209(s, b, B);
  const dw = aA - aB;
  const nm = { F: "FORWARDS", D: "DEFENCE", G: "GOALIES" };
  const cell = (o, right, id) => {
    if (!o) return <div></div>;
    const p = o.p, gone = p.ft !== id;
    const sub = o.gp + " GP" + (o.left ? " \u00b7 " + o.left + " left" : "") + (o.live ? " \u00b7 live" : "");
    return (
      <div className={"min-w-0 gx-pc" + (o.live ? " gx-lv176" : "")} style={{ flexDirection: right ? "row-reverse" : "row" }} onClick={() => { if (window.__NAV) window.__NAV.player(p); }}>
        <span className="gx-fw" style={{ display: "inline-flex" }}><GxFace p={p} size={30} /></span>
        <div className={"min-w-0" + (right ? " text-right" : "")} style={{ flex: 1 }}>
          <div className="truncate gx-nm"><button type="button" className="hover:underline text-left"><span className="m-hide">{p.n}</span><span className="m-inl">{shortN(p.n)}</span></button><span className="gx-tl98"><TeamLogo t={p.t} size={15} /></span><span className="gx-tp155">{p.t + " " + p.p}</span>{gone ? <span className="gx-dr209">dropped</span> : null}</div>
          <div className="text-xs text-slate-500 gx-sub209">{sub}</div>
        </div>
      </div>
    );
  };
  const num = (o, right) => {
    if (!o) return <div></div>;
    const proj = o.rem > 0.05 ? o.pts + o.rem : null;
    return <div className={(right ? "" : "text-right") + (o.gp ? " gx-on157" : "")} data-gx="138pts">{o.gp ? f1(o.pts) : "\u2013"}{proj != null ? <div className="text-xs" style={{ fontWeight: 400, whiteSpace: "nowrap" }}>{f1(proj)}</div> : null}</div>;
  };
  return (
    <div className="gx-ws209">
      <div className="gx-h2h gx-tt114 gx-tt147 gx-on157">
        <div>Week</div>
        <div className="text-right">{f1(aA)}<div className="text-xs" style={{ fontWeight: 400, whiteSpace: "nowrap" }}><span className="m-hide">proj </span>{f1(fa)}</div></div>
        <div></div>
        <div>{f1(aB)}<div className="text-xs" style={{ fontWeight: 400, whiteSpace: "nowrap" }}><span className="m-hide">proj </span>{f1(fb)}</div></div>
        <div className="text-right" style={{ color: !mine || Math.abs(dw) < 0.05 ? "var(--mute)" : dw > 0 ? "var(--good)" : "var(--bad)" }}>{(dw > 0 ? "+" : "") + f1(dw)}</div>
      </div>
      {["F", "D", "G"].map((g) => {
        const L = SA[g], R = SB[g], n = Math.max(L.length, R.length);
        if (!n) return null;
        const out = [<div key={g + "h"} className="gx-gd209">{nm[g]}</div>];
        for (let i = 0; i < n; i++) out.push(
          <div key={g + i} className="gx-h2h" style={i ? null : { borderTop: 0 }}>
            {cell(L[i], false, a)}{num(L[i], false)}
            <div className="text-xs text-center" style={{ color: "var(--faint)" }}>{g}</div>
            {num(R[i], true)}{cell(R[i], true, b)}
          </div>
        );
        return out;
      })}
    </div>
  );
}
'''

def change(t):
    t = lit(t, "209: styles", "</style>", NEW_CSS, "change 209 (install.py)")
    t = lit(t, "209: helpers", ROOT, HELPERS + ROOT, "change 209: Matchup day picker")
    t = lit(t, "209: summary state",
            "  const [day, setDay] = useState(null);\n  const touch = React.useRef(null);",
            "  const [day, setDay] = useState(null);\n  const [sum209, setSum209] = useState(false); /* gx209 */\n  const touch = React.useRef(null);",
            "const [sum209, setSum209]")
    old_dt = '''        <button type="button" className="gx-arw" aria-label="Earlier day" disabled={d <= 0} onClick={() => setDay(d - 1)}>{"\\u2039"}</button>
        <div className="dt">{dates[d] === today ? "Today" : dates[d] ? dayLabel(dates[d]) : ""}<small style={{ color: !mine || Math.abs(dvD135) < 0.05 ? "var(--mute)" : dvD135 > 0 ? "var(--good)" : "var(--bad)" }}>{(dvD135 > 0 ? "+" : "") + f1(dvD135)}</small></div>
        <button type="button" className="gx-arw" aria-label="Later day" disabled={d >= n - 1} onClick={() => setDay(d + 1)}>{"\\u203a"}</button>'''
    new_dt = '''        <button type="button" className="gx-arw" aria-label="Earlier day" disabled={!sum209 && d <= 0} onClick={() => { if (sum209) setSum209(false); else setDay(d - 1); }}>{"\\u2039"}</button>
        <GxDayPick209 dates={dates} d={d} sum={sum209} today={today} mine={mine} dv={(i) => (i === d ? dvD135 : dvOf(i))} wkDv={aA - aB} onDay={(i) => { setSum209(false); setDay(i); }} onSum={() => setSum209(true)} />
        <button type="button" className="gx-arw" aria-label="Later day" disabled={!sum209 && d >= n - 1} onClick={() => { if (sum209) setSum209(false); else setDay(d + 1); }}>{"\\u203a"}</button>'''
    t = lit(t, "209: day picker", old_dt, new_dt, "<GxDayPick209 dates={dates}")
    old_box = '''      <div key={"d105-" + sel + "-" + d} ref={dr106} {...dh106} className={"gx-pn gx-dr106 gx-sl105 " + sl105b} style={{ marginTop: 12 }}>'''
    new_box = '''      {sum209 ? <div key={"s209-" + sel} className="gx-pn gx-sl105" style={{ marginTop: 12 }}><GxWkSum209 s={s} a={a} b={b} A={A} B={B} aA={aA} aB={aB} fa={fa} fb={fb} mine={mine} /></div> : null}
      <div key={"d105-" + sel + "-" + d} ref={dr106} {...dh106} className={"gx-pn gx-dr106 gx-sl105 " + sl105b} style={sum209 ? { display: "none" } : { marginTop: 12 }}>'''
    t = lit(t, "209: summary box", old_box, new_box, "<GxWkSum209 s={s}")
    return t

edit(APP, change)
