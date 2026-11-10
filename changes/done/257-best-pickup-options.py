# changes/257-best-pickup-options.py - Roster Best pickup now: top 10 pickups by this week's win chance, arrows and swipe to flip, tap "for X" to drop someone else

NEW_CSS = r'''  /* change 257 (install.py) */
  .gx-bx226 .bp257 .ft { display: flex; align-items: center; gap: 8px; }
  .gx-bx226 .bp257 .nv257 { margin-left: auto; display: inline-flex; align-items: center; gap: 6px; font-size: 12px; color: var(--mute); font-variant-numeric: tabular-nums; white-space: nowrap; }
  .gx-bx226 .bp257 .nv257 button { width: 32px; height: 32px; border-radius: 999px; border: 1px solid var(--line); background: var(--card); color: var(--ink); font-size: 17px; line-height: 1; display: inline-flex; align-items: center; justify-content: center; }
  .gx-bx226 .bp257 .nv257 button:disabled { opacity: .35; }
  .gx-bx226 .bp257 .gn257 { display: flex; align-items: center; justify-content: space-between; gap: 10px; font-size: 12px; color: var(--mute); margin-top: 8px; height: 32px; white-space: nowrap; }
  .gx-bx226 .bp257 .gn257 span { overflow: hidden; text-overflow: ellipsis; }
  .gx-bx226 .bp257 .row230 { touch-action: pan-y; }
  .gx-bx226 .bp257 .dr257 { flex: none; height: 32px; padding: 0 12px; border-radius: 8px; border: 1px solid var(--line); background: var(--card); color: var(--ink); font-size: 12.5px; font-weight: 600; }
  .gx-bx226 .bp257 .dl257 { margin-top: 10px; border-top: 1px solid var(--line); }
  .gx-bx226 .bp257 .dl257 .hd257 { font-size: 11px; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; color: var(--mute); padding: 10px 0 4px; }
  .gx-bx226 .bp257 .dl257 button.r { display: grid; grid-template-columns: 30px minmax(0,1fr) 62px 52px; gap: 8px; align-items: center; width: 100%; min-height: 44px; padding: 0 6px; border: 0; border-top: 1px solid var(--line); background: none; color: var(--ink); text-align: left; font-size: 13px; }
  @media (min-width: 641px) { .gx-bx226 .bp257 .dl257 button.r { grid-template-columns: 46px minmax(0,1fr) 70px 56px; } }
  .gx-bx226 .bp257 .dl257 button.r.on { background: var(--hover); border-radius: 8px; box-shadow: inset 0 0 0 1px var(--line2); }
  .gx-bx226 .bp257 .dl257 .nn { min-width: 0; }
  .gx-bx226 .bp257 .dl257 .nn b { display: block; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .gx-bx226 .bp257 .dl257 .nn small { display: block; font-size: 11px; color: var(--mute); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .gx-bx226 .bp257 .dl257 .n { text-align: right; font-variant-numeric: tabular-nums; white-space: nowrap; }
  .gx-bx226 .bp257 .dl257 .n small { display: block; font-size: 10.5px; color: var(--mute); }
</style>'''

HELPERS = r'''// ---------- change 257: Best pickup now with 10 options and a choice of drop (install.py) ----------
// options = the 20 best adds this week by points (each with its best drop), ranked by win chance this week after the move, top 10
function GxBp257({ s, openP }) {
  const gen = (window.ESPN_DATA || {}).generated;
  const [L, setL] = useState(null);
  const [ix, setIx] = useState(0);
  const [dd, setDd] = useState({}); // chosen drop per add: f.id -> { d, gain, a }
  const [dl, setDl] = useState(null); // drop list for the shown add
  const sw = React.useRef(null), M = React.useRef(null);
  useEffect(() => {
    let dead = false;
    setL(null); setDd({}); setDl(null);
    const id = setTimeout(() => {
      try {
        const m = computeMoves(s, { H: 1, pool: 40 });
        M.current = m;
        const b = winChance(s);
        const opts = m.res.filter((x) => x.gain >= (s.minGain ?? 3)).slice(0, 20)
          .map((r) => ({ ...r, a: winChance(s, afterMove(s, r.f, r.d)) }))
          .sort((x, y) => Math.round((y.a || 0) * 100) - Math.round((x.a || 0) * 100) || y.gain - x.gain).slice(0, 10);
        if (!dead) { setL({ b, opts }); setIx(0); }
      } catch (e) { if (!dead) setL({ err: true }); }
    }, 900);
    return () => { dead = true; clearTimeout(id); };
  }, [gen, s.players, s.wk]);
  const sl = useSlide105(ix);
  const n = L && L.opts ? L.opts.length : 0;
  const go = (j) => { if (j < 0 || j >= n) return; setIx(j); setDl(null); };
  const o0 = n ? L.opts[Math.min(ix, n - 1)] : null;
  const o = o0 && dd[o0.f.id] ? { ...o0, ...dd[o0.f.id] } : o0;
  const openDrops = () => {
    if (dl) { setDl(null); return; }
    const m = M.current; if (!m || !o) return;
    try {
      const base = m.total(m.myR);
      const rows = m.myR.filter((d) => !d.ir && !m.protectedIds.has(d.id) && m.keepsMins(d, o.f))
        .map((d) => ({ d, gain: m.total(timedMove(m.myR, s.me, [{ add: o.f, drop: d }])) - base }))
        .sort((x, y) => y.gain - x.gain).slice(0, 8)
        .map((r) => ({ ...r, a: winChance(s, afterMove(s, o.f, r.d)) }));
      setDl({ f: o.f.id, rows });
    } catch (e) { setDl(null); }
  };
  const pickDrop = (r) => { setDd((x) => ({ ...x, [o.f.id]: { d: r.d, gain: r.gain, a: r.a } })); setDl(null); };
  const tDown = (e) => { sw.current = { x: e.clientX, y: e.clientY }; };
  const tUp = (e) => { const p = sw.current; sw.current = null; if (!p) return; const dx = e.clientX - p.x, dy = e.clientY - p.y; if (Math.abs(dx) > 40 && Math.abs(dx) > Math.abs(dy) * 1.5) go(ix + (dx < 0 ? 1 : -1)); };
  return (
    <div className="bp230 bp257" data-gx="257">
      <div className="ft">
        <span className="gx-tag">Best pickup now</span>
        {n > 1 ? (
          <span className="nv257">
            <button type="button" aria-label="Better option" disabled={ix <= 0} onClick={() => go(ix - 1)}>{"\u2039"}</button>
            <span>{(ix + 1) + " of " + n}</span>
            <button type="button" aria-label="Next option" disabled={ix >= n - 1} onClick={() => go(ix + 1)}>{"\u203a"}</button>
          </span>
        ) : null}
      </div>
      {!L ? <div className="text-xs text-slate-500" style={{ marginTop: 8 }}>Working it out...</div> : L.err ? <div className="text-xs text-slate-500" style={{ marginTop: 8 }}>Could not work this out right now.</div> : !n ? <div className="text-sm text-slate-500" style={{ marginTop: 8 }}>No pickup is worth a move right now.</div> : (
        <>
          <div key={"o" + ix} className={"row230 gx-sl105 " + sl} onPointerDown={tDown} onPointerUp={tUp} onPointerCancel={() => (sw.current = null)}>
            <span className="pp230">
              <button type="button" style={{ background: "none", border: 0, padding: 0 }} onClick={() => openP(o.f)}><GxFace p={o.f} size={26} /></button>
              <span className="min-w-0">
                <button type="button" style={{ background: "none", border: 0, padding: 0, color: "inherit", textAlign: "left", maxWidth: "100%" }} onClick={() => openP(o.f)}><b>{o.f.n}</b></button>
                <small>{o.f.t + " \u00b7 " + o.f.p + " \u00b7 for " + lastN(o.d.n)}</small>
              </span>
            </span>
            <span className="wc230">{wpTxt(L.b) + " \u2192 "}<b>{wpTxt(o.a)}</b></span>
            <button type="button" className="sm230" onClick={() => { if (!window.__QA) return; window.__QA.sim(o.f); window.__PICK_SIM = { add: o.f.id, drop: o.d.id }; }}>Simulate</button>
          </div>
          <div className="gn257"><button type="button" className="dr257" onClick={openDrops}>{(dl && dl.f === o.f.id ? "Close" : "Drop someone else") + " \u25be"}</button><span>{(o.gain >= 0 ? "+" : "\u2212") + f1(Math.abs(o.gain)) + " points this week"}</span></div>
          {dl && dl.f === o.f.id ? (
            <div className="dl257">
              <div className="hd257">{"Drop for " + o.f.n}</div>
              {dl.rows.map((r) => (
                <button key={r.d.id} type="button" className={"r" + (r.d.id === o.d.id ? " on" : "")} onClick={() => pickDrop(r)}>
                  <GxFace p={r.d} size={24} />
                  <span className="nn"><b>{r.d.n}</b><small>{r.d.t + " \u00b7 " + r.d.p + " \u00b7 " + f1(gxPgAvg(r.d, s.blend)) + " pts/g"}</small></span>
                  <span className="n">{(r.gain >= 0 ? "+" : "\u2212") + f1(Math.abs(r.gain))}<small>pts wk</small></span>
                  <span className="n">{wpTxt(r.a)}<small>win</small></span>
                </button>
              ))}
            </div>
          ) : null}
        </>
      )}
    </div>
  );
}
'''

def change(t):
    t = lit(t, "257: styles", "</style>", NEW_CSS, "change 257 (install.py)")
    t = lit(t, "257: helpers", ROOT, HELPERS + ROOT, "change 257: Best pickup now with 10 options")
    t = lit(t, "257: old pickup work off",
            "if (!cur || me !== s.me) { setBp(null); return undefined; }",
            "{ setBp(null); return undefined; } /* change 257: GxBp257 does this now */",
            "/* change 257: GxBp257 does this now */")
    t = lit(t, "257: show it",
            '<div className="min-w-0">{board}{bpCard}</div>',
            '<div className="min-w-0">{board}{me !== s.me || !cur ? null : <GxBp257 s={s} openP={openP} />}</div>',
            "<GxBp257 s={s} openP={openP} />")
    return t

edit(APP, change)
