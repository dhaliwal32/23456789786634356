# changes/193-pickups-pick-weeks.py - Players (free agents): the "Pickups for next week" box and its "aimed at next week" line are gone; Filters now let you pick exactly which weeks count: This week, Next 4 weeks, Rest of season, Losing weeks (every week you're under 50% to win), or tap any weeks you want, each shown with its dates, opponent and your chance to win

OLD_HZ = '''  const n = H === 0 ? s.weeks.length - s.wk : H;
  const horizon = s.weeks.slice(s.wk, s.wk + n).map((w, i) => { const dw = deriveWeek(w, s.autoDone); return { wk: dw, from: i === 0 ? dw.done : 0 }; });
  const lineupAware = H !== 0;'''
NEW_HZ = '''  const n = H === 0 ? s.weeks.length - s.wk : H;
  const W193 = Array.isArray(o.wks) && o.wks.length ? [...new Set(o.wks)].filter((i) => i >= s.wk && i < s.weeks.length).sort((a, b) => a - b) : null; /* change 193: chosen weeks */
  const horizon = W193 ? W193.map((wi) => { const dw = deriveWeek(s.weeks[wi], s.autoDone); return { wk: dw, from: wi === s.wk ? dw.done : 0 }; }) : s.weeks.slice(s.wk, s.wk + n).map((w, i) => { const dw = deriveWeek(w, s.autoDone); return { wk: dw, from: i === 0 ? dw.done : 0 }; });
  const lineupAware = W193 ? W193.length <= 4 : H !== 0;'''

OLD_KEY = '''  const key = [o.H, o.pos, o.q, window.__PMODE, [...gxHideSet()].sort().join(",")].join("|");'''
NEW_KEY = '''  const key = [o.H, o.pos, o.q, window.__PMODE, [...gxHideSet()].sort().join(","), (o.wks || []).join(".")].join("|"); /* change 193 */'''

OLD_ST = '''  const [H, setH] = useState(1);
  const [pos, setPos]'''
NEW_ST = '''  const [H, setH] = useState(1);
  const [wm193, setWm193] = useState("h1"); /* change 193: h1, h4, h0, lose or pick */
  const [wks193, setWks193] = useState(null);
  const [pos, setPos]'''

OLD_M = '''  const M = useMemo(() => gxMoves102(s, sP, { H, pos, q }), [sP, H, pos, q, gxHideV]);'''
NEW_M = '''  const M = useMemo(() => gxMoves102(s, sP, wks193 ? { H, pos, q, wks: wks193 } : { H, pos, q }), [sP, H, pos, q, gxHideV, wks193]);'''

OLD_HSL = '''{!plan ? <GxHsLine s={s} base={base} ml={ml} /> : null}{/* gx083-h */}'''
NEW_HSL = '''{/* change 193: next-week line removed */}'''
OLD_HS = '''{!plan ? <GxHeadStart s={s} base={base} ml={ml} /> : null}{/* gx083 */}'''
NEW_HS = '''{/* change 193: Pickups for next week removed */}'''

OLD_FL = '''<GxFlt108 label={({ all: "All", F: "Forwards", D: "Defence", G: "Goalies" })[pos] + " \\u00b7 " + ({ 1: plan ? "Next week" : "This week", 4: "Next 4 weeks", 0: "Rest of season" })[H] + " \\u00b7 " + gxRngLbl108()}>'''
NEW_FL = '''<GxFlt108 label={({ all: "All", F: "Forwards", D: "Defence", G: "Goalies" })[pos] + " \\u00b7 " + (wks193 ? (wm193 === "lose" ? "Losing weeks (" + wks193.length + ")" : wks193.length === 1 ? gxWkShort193(sP, wks193[0]) : wks193.length + " weeks") : ({ 1: plan ? "Next week" : "This week", 4: "Next 4 weeks", 0: "Rest of season" })[H]) + " \\u00b7 " + gxRngLbl108()}>'''

OLD_PL = '''        <Pills items={[[1, plan ? "Next week" : "This week"], [4, "Next 4 weeks"], [0, "Rest of season"]]} value={H} onChange={(v) => { setH(v); setLimit(40); }} />
      </div><GxRngSel100 /></GxFlt108>'''
NEW_PL = '''      </div><GxWkPick193 s={s} sP={sP} plan={plan} mode={wm193} wks={wks193} onPick={(m, a) => { setWm193(m); setLimit(40); if (m === "h1" || m === "h4" || m === "h0") { setWks193(null); setH(m === "h1" ? 1 : m === "h4" ? 4 : 0); } else setWks193(a); }} /><GxRngSel100 /></GxFlt108>'''

OLD_SIM = '''<GxSim107 s={sP} setS={setS} wk={wkP} M={M} H={H} hLabel={hLabel}'''
NEW_SIM = '''<GxSim107 s={sP} setS={setS} wk={wkP} M={M} H={wks193 ? (wks193.length === 1 && wks193[0] === sP.wk ? 1 : 2) : H} hLabel={wks193 ? (wks193.length === 1 ? gxWkShort193(sP, wks193[0]).toLowerCase() : "the " + wks193.length + " weeks you picked") : hLabel}'''

HELPERS = r'''// ---------- change 193: pick which weeks count for pickups (install.py) ----------
const gxWkShort193 = (s, i) => String(((s.weeks || [])[i] || {}).label || "Week " + (i + 1)).split(" \u00b7 ")[0];
function GxWkPick193({ s, sP, plan, mode, wks, onPick }) {
  const list = useMemo(() => {
    const out = [];
    for (let i = sP.wk; i < sP.weeks.length; i++) {
      const w = sP.weeks[i] || {}, opp = oppOf(w, sP.me);
      let wc = null;
      try { wc = opp ? winChance({ ...sP, wk: i }) : null; } catch (e) {}
      const L = String(w.label || "Week " + (i + 1)).split(" \u00b7 ");
      out.push({ i, wl: L[0], dl: L[1] || "", opp, wc });
    }
    return out;
  }, [sP]);
  const sel = new Set(mode === "h1" ? [sP.wk] : mode === "h4" ? list.slice(0, 4).map((x) => x.i) : mode === "h0" ? list.map((x) => x.i) : wks || []);
  const lose = list.filter((x) => x.wc != null && x.wc < 0.5).map((x) => x.i);
  const tog = (i) => { const n = new Set(sel); if (n.has(i)) n.delete(i); else n.add(i); const a = [...n].sort((x, y) => x - y); if (a.length) onPick("pick", a); };
  return (
    <div className="gx-wk193">
      <div className="qk"><Pills items={[["h1", plan ? "Next week" : "This week"], ["h4", "Next 4 weeks"], ["h0", "Rest of season"], ["lose", "Losing weeks" + (lose.length ? " (" + lose.length + ")" : "")]]} value={mode} onChange={(v) => { if (v === "lose") { if (lose.length) onPick("lose", lose); } else onPick(v, null); }} /></div>
      <div className="tp">Or tap the weeks you want</div>
      <div className="gr">
        {list.map((x) => (
          <button key={x.i} type="button" className={"wc" + (sel.has(x.i) ? " on" : "")} onClick={() => tog(x.i)} aria-pressed={sel.has(x.i)}>
            <span className="l">{x.wl}</span>
            <span className="d">{x.dl}</span>
            <span className="o">{x.opp ? <><GxFtPic114 id={x.opp} size={14} /><span>{gxTag131(s, { ft: x.opp }) || teamName(s, x.opp)}</span></> : <span>No matchup</span>}</span>
            <b style={{ color: x.wc == null ? "var(--mute)" : x.wc >= 0.5 ? "var(--good)" : "var(--bad)" }}>{x.wc == null ? "-" : wpTxt(x.wc)}</b>
          </button>
        ))}
      </div>
    </div>
  );
}
'''

NEW_CSS = r'''  /* change 193 (install.py) */
  .gx-wk193 { width: 100%; margin-top: 10px; }
  .gx-wk193 .qk > div { flex-wrap: wrap; overflow: visible; }
  .gx-wk193 .tp { font-size: 12px; color: var(--mute); margin: 10px 0 6px; }
  .gx-wk193 .gr { display: grid; grid-template-columns: repeat(auto-fill, minmax(124px, 1fr)); gap: 8px; max-height: 300px; overflow-y: auto; overscroll-behavior: contain; padding: 2px; }
  .gx-wk193 .wc { display: grid; grid-template-rows: 18px 16px 20px 20px; align-items: center; height: 88px; padding: 6px 10px; border: 1px solid var(--line2); border-radius: 10px; text-align: left; min-width: 0; transition: background .15s ease, border-color .15s ease; }
  .gx-wk193 .wc > * { min-width: 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .gx-wk193 .wc .l { font-size: 13px; font-weight: 600; }
  .gx-wk193 .wc .d { font-size: 11.5px; color: var(--mute); }
  .gx-wk193 .wc .o { display: flex; align-items: center; gap: 5px; font-size: 12.5px; color: var(--ink2, var(--ink)); }
  .gx-wk193 .wc .o img, .gx-wk193 .wc .o .gx-fp114 { flex: none; }
  .gx-wk193 .wc b { font-size: 14px; font-variant-numeric: tabular-nums; }
  .gx-wk193 .wc.on { border-color: var(--accent); box-shadow: inset 0 0 0 1px var(--accent); background: var(--accentSoft); }
  @media (max-width: 640px) { .gx-wk193 .gr { grid-template-columns: repeat(3, minmax(0, 1fr)); } .gx-wk193 .wc { padding: 6px 8px; } }
</style>'''


def change(t):
    t = lit(t, "193: styles", "</style>", NEW_CSS, "change 193 (install.py)")
    t = lit(t, "193: helpers", ROOT, HELPERS + ROOT, "change 193: pick which weeks count")
    t = lit(t, "193: chosen weeks in the pickup maths", OLD_HZ, NEW_HZ, "change 193: chosen weeks")
    t = lit(t, "193: remember lists per week choice", OLD_KEY, NEW_KEY, '(o.wks || []).join(".")')
    t = lit(t, "193: week choice state", OLD_ST, NEW_ST, "change 193: h1, h4, h0, lose or pick")
    t = lit(t, "193: use the chosen weeks", OLD_M, NEW_M, "{ H, pos, q, wks: wks193 }")
    t = lit(t, "193: remove next-week line", OLD_HSL, NEW_HSL, "change 193: next-week line removed")
    t = lit(t, "193: remove Pickups for next week", OLD_HS, NEW_HS, "change 193: Pickups for next week removed")
    t = lit(t, "193: filter label", OLD_FL, NEW_FL, 'wm193 === "lose" ? "Losing weeks (')
    t = lit(t, "193: week picker in Filters", OLD_PL, NEW_PL, "<GxWkPick193 s={s}")
    t = lit(t, "193: simulate box window", OLD_SIM, NEW_SIM, 'weeks you picked")')
    return t


edit(APP, change)
