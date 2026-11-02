# changes/194-simulate-win-by-week.py - Simulate a pickup (from Players) shows "Win chance by week": every remaining week as a card with your chance to win now and after the swap (green up, red down); the weeks counted in the points are highlighted, and tapping a week adds or removes it from the weeks counted (same as the Filters week picker)

OLD_SIG = r'''function GxSim107({ s, setS, wk, M, H, hLabel, init, wBase, onClose }) {'''
NEW_SIG = r'''function GxSim107({ s, setS, wk, M, H, hLabel, init, wBase, onClose, w194, onW194 }) {'''

OLD_DN = r'''  const DN = (dt) => (dt === today ? "Today" : dayLabel(dt).split(",")[0]);'''
NEW_DN = r'''  const DN = (dt) => (dt === today ? "Today" : dayLabel(dt).split(",")[0]);
  /* change 194: win chance by week, now and after the swap */
  const wb194 = useMemo(() => (w194 ? gxWkWins194(s, null) : []), [s, !!w194]);
  const wa194 = useMemo(() => (w194 && a && d && pick ? gxWkWins194(s, rosterOn(pick)) : []), [s, addId, dropId, pick, !!w194]);'''

OLD_DET = r'''                <button type="button" className="lk bt150" onClick={() => setDet(!det)}>{det ? "Hide details" : "More details"}</button>'''
NEW_DET = r'''                {w194 && wb194.length ? <GxSimWeeks194 s={s} before={wb194} after={wa194} sel={w194} onW={onW194} /> : null}
                <button type="button" className="lk bt150" onClick={() => setDet(!det)}>{det ? "Hide details" : "More details"}</button>'''

OLD_CALL = r'''      {sim ? <GxSim107 s={sP} setS={setS} wk={wkP} M={M} H={wks193'''
NEW_CALL = r'''      {sim ? <GxSim107 w194={gxSelW194(sP, wm193, wks193)} onW194={(arr) => { setWm193("pick"); setWks193(arr); setLimit(40); }} s={sP} setS={setS} wk={wkP} M={M} H={wks193'''

HELPERS = r'''// ---------- change 194: win chance by week in the Simulate box (install.py) ----------
function gxSelW194(sP, mode, wks) {
  const all = [];
  for (let i = sP.wk; i < sP.weeks.length; i++) all.push(i);
  return mode === "h1" ? [sP.wk] : mode === "h4" ? all.slice(0, 4) : mode === "h0" ? all : wks || [sP.wk];
}
// every remaining week: { i, wl, opp, wc } for my roster (or a changed roster)
function gxWkWins194(sP, roster) {
  const out = [];
  for (let i = sP.wk; i < sP.weeks.length; i++) {
    const w = sP.weeks[i] || {}, opp = oppOf(w, sP.me);
    if (!opp) continue;
    let wc = null;
    try { wc = winChance({ ...sP, wk: i }, roster || undefined); } catch (e) {}
    out.push({ i, wl: String(w.label || "Week " + (i + 1)).split(" \u00b7 ")[0], opp, wc });
  }
  return out;
}
function GxSimWeeks194({ s, before, after, sel, onW }) {
  const A = {};
  (after || []).forEach((x) => { A[x.i] = x.wc; });
  const S = new Set(sel || []);
  const tog = (i) => { const n = new Set(S); if (n.has(i)) n.delete(i); else n.add(i); const arr = [...n].sort((x, y) => x - y); if (arr.length && onW) onW(arr); };
  return (
    <div className="gx-sw194">
      <div className="sec">Win chance by week</div>
      <div className="gr">
        {before.map((x) => {
          const n = A[x.i], dl = n != null && x.wc != null ? Math.round(n * 100) - Math.round(x.wc * 100) : 0;
          return (
            <button key={x.i} type="button" className={"wc" + (S.has(x.i) ? " on" : "")} onClick={() => tog(x.i)} aria-pressed={S.has(x.i)}>
              <span className="l">{x.wl}</span>
              <span className="o"><GxFtPic114 id={x.opp} size={14} /><span>{gxTag131(s, { ft: x.opp }) || teamName(s, x.opp)}</span></span>
              <span className="w"><span className="b">{x.wc == null ? "-" : wpTxt(x.wc)}</span><span className="ar">{"\u2192"}</span><b style={{ color: dl > 0 ? "var(--good)" : dl < 0 ? "var(--bad)" : "var(--ink)" }}>{n == null ? "-" : wpTxt(n)}</b></span>
            </button>
          );
        })}
      </div>
      <div className="nt">Highlighted weeks count in the points above. Tap a week to add or remove it.</div>
    </div>
  );
}
'''

NEW_CSS = r'''  /* change 194 (install.py) */
  .gx-sw194 { margin-top: 4px; }
  .gx-sw194 .gr { display: grid; grid-template-columns: repeat(auto-fill, minmax(118px, 1fr)); gap: 8px; max-height: 262px; overflow-y: auto; overscroll-behavior: contain; padding: 2px; }
  .gx-sw194 .wc { display: grid; grid-template-rows: 18px 20px 22px; align-items: center; height: 76px; padding: 6px 10px; border: 1px solid var(--line2); border-radius: 10px; text-align: left; min-width: 0; transition: background .15s ease, border-color .15s ease; }
  .gx-sw194 .wc > * { min-width: 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .gx-sw194 .wc .l { font-size: 13px; font-weight: 600; }
  .gx-sw194 .wc .o { display: flex; align-items: center; gap: 5px; font-size: 12.5px; color: var(--mute); }
  .gx-sw194 .wc .w { display: flex; align-items: baseline; gap: 4px; font-variant-numeric: tabular-nums; }
  .gx-sw194 .wc .w .b { font-size: 12.5px; color: var(--mute); }
  .gx-sw194 .wc .w .ar { font-size: 11px; color: var(--mute); }
  .gx-sw194 .wc .w b { font-size: 15px; }
  .gx-sw194 .wc.on { border-color: var(--accent); box-shadow: inset 0 0 0 1px var(--accent); background: var(--accentSoft); }
  .gx-sw194 .nt { font-size: 12px; color: var(--mute); margin-top: 6px; }
  @media (max-width: 640px) { .gx-sw194 .gr { grid-template-columns: repeat(3, minmax(0, 1fr)); } .gx-sw194 .wc { padding: 6px 8px; } }
</style>'''


def change(t):
    t = lit(t, "194: styles", "</style>", NEW_CSS, "change 194 (install.py)")
    t = lit(t, "194: helpers", ROOT, HELPERS + ROOT, "change 194: win chance by week")
    t = lit(t, "194: Simulate takes the weeks", OLD_SIG, NEW_SIG, "onClose, w194, onW194 })")
    t = lit(t, "194: win chances now and after", OLD_DN, NEW_DN, "change 194: win chance by week, now and after")
    t = lit(t, "194: show the weeks", OLD_DET, NEW_DET, "<GxSimWeeks194 s={s}")
    t = lit(t, "194: points follow the weeks", "  }, [addId, dropId, pick]);", "  }, [addId, dropId, pick, M]); /* change 194 */", "[addId, dropId, pick, M]")
    t = lit(t, "194: Players passes its weeks", OLD_CALL, NEW_CALL, "w194={gxSelW194(sP, wm193, wks193)}")
    return t


edit(APP, change)
