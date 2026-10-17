# changes/082-trade-projections.py - Trades: pick which projection the trade result uses (ESPN, GM model, Blend, AI) and see win or lose under every projection at once

NEW_CSS = r'''  /* change 082 (install.py) */
  .gx-pm82 { display: grid; grid-template-columns: minmax(0,1.3fr) repeat(4, minmax(0,1fr)) 54px; gap: 8px; align-items: center; padding: 8px 6px; border-top: 1px solid var(--line); font-size: 13px; font-variant-numeric: tabular-nums; }
  .gx-pm82 > span + span { text-align: right; }
  .gx-pm82.h { font-size: 11px; color: var(--mute); border-top: 0; padding-top: 2px; }
  .gx-pm82.r { cursor: pointer; border-radius: 6px; }
  .gx-pm82.r:hover { background: var(--line); }
  .gx-pm82.on { outline: 1px solid var(--ink); }
  .gx-pm82 .w { font-weight: 600; color: var(--good); }
  .gx-pm82 .l { font-weight: 600; color: var(--bad); }
  .gx-pmh82 { display: flex; align-items: center; gap: 10px; flex-wrap: wrap; margin: 10px 0 2px; }
  @media (max-width: 640px) {
    .gx-pm82 { grid-template-columns: minmax(0,1.2fr) repeat(2, minmax(0,1fr)) 46px; gap: 6px; padding: 9px 4px; }
  }
</style>'''

HELPERS = r'''// ---------- change 082: trade result under each projection (install.py) ----------
const GX_PM82 = [["espn", "ESPN"], ["model", "GM model"], ["blend", "Blend"], ["ai", "AI"]];
const gxCanMode82 = (k) => k === "espn" || (!!window.__MODEL && (k !== "ai" || !!window.__AI));
// run fn with a different projection, then put the app's projection back
const gxWithMode82 = (m, fn) => {
  const prev = window.__PMODE;
  if (!m || m === prev || !gxCanMode82(m)) return fn();
  window.__PMODE = m;
  try { return fn(); } finally { window.__PMODE = prev; }
};
const gxPct82 = (b, a) => { if (b == null || a == null) return "–"; const d = Math.round(a * 100) - Math.round(b * 100); return (d > 0 ? "+" : "") + d + "%"; };
function GxTradeModes82({ res, cmp, tm, setTm, part }) {
  const app = window.__PMODE, cur = res.mode82, lbl = (k) => (GX_PM82.find((x) => x[0] === k) || [k, k])[1];
  const sg = (v) => (v >= 0 ? "+" : "") + Math.round(v);
  if (part === "pick") return (
      <div className="gx-pmh82">
        <span className="text-xs text-slate-500">Projection</span>
        <span className="gx-seg">{GX_PM82.map(([k, l]) => <button key={k} type="button" disabled={!gxCanMode82(k)} className={cur === k ? "on" : ""} onClick={() => setTm(k === app ? null : k)}>{l}</button>)}</span>
        {tm && tm !== app ? <span className="text-xs text-slate-500">Trades only. The rest of the app still uses {lbl(app)}.</span> : null}
      </div>
  );
  return (
      <div style={{ marginTop: 12 }}>
        <div className="gx-tag" style={{ marginBottom: 4 }}>Every projection</div>
        <div className="gx-pm82 h"><span>Projection</span><span>You</span><span className="m-hide">Them</span><span className="m-hide">This week</span><span>Next week</span><span>Result</span></div>
        {!cmp ? <div className="text-xs text-slate-500" style={{ padding: "8px 6px" }}>Working out every projection...</div> : cmp.map((x) => (
          <div key={x.k} className={"gx-pm82 r" + (x.k === cur ? " on" : "")} onClick={() => setTm(x.k === app ? null : x.k)} title="Show the trade with this projection">
            <span>{x.l}{x.k === app ? <span className="text-xs text-slate-500"> (app)</span> : null}</span>
            <span style={{ color: x.my >= 0 ? "var(--good)" : "var(--bad)" }}>{sg(x.my)}</span>
            <span className="m-hide" style={{ color: x.th >= 0 ? "var(--good)" : "var(--bad)" }}>{sg(x.th)}</span>
            <span className="m-hide">{gxPct82(x.tb, x.ta)}</span>
            <span>{gxPct82(x.wb, x.wa)}</span>
            <span className={x.my > 0 ? "w" : "l"}>{x.my > 0 ? "Win" : "Lose"}</span>
          </div>
        ))}
        <div className="text-xs text-slate-500" style={{ marginTop: 6 }}>Points are for the rest of the season. The weeks show the change in your chance to win. Win means your lineup gains points.</div>
      </div>
  );
}
'''


def change(t):
    t = lit(t, "082: styles", "</style>", NEW_CSS, "change 082 (install.py)")
    t = lit(t, "082: helpers", ROOT, HELPERS + ROOT, "change 082: trade result under each projection")
    t = lit(t, "082: trade-only projection",
            "const [dropAll, setDropAll] = useState(false);",
            "const [dropAll, setDropAll] = useState(false);\n  const [tm82, setTm82] = useState(null); // change 082: projection for this page only",
            "const [tm82, setTm82] = useState(null);")
    t = lit(t, "082: result uses the chosen projection",
            "  const res = useMemo(() => {\n    if (!ready) return null;",
            "  const res = useMemo(() => gxWithMode82(tm82, () => { // change 082\n    if (!ready) return null;",
            "useMemo(() => gxWithMode82(tm82, () => { // change 082")
    t = lit(t, "082: result recomputes when the projection changes",
            "  }, [key, s.players, s.wk, K, window.__PMODE]);",
            "  }), [key, s.players, s.wk, K, window.__PMODE, tm82]);",
            "window.__PMODE, tm82]);")
    t = lit(t, "082: numbers under every projection",
            "    const c = cnt(after);\n    return { my, th, rb, ra, wb, wa, tb, ta, short:",
            "    // change 082: the same numbers under every projection\n"
            "    const q82 = () => {\n"
            "      const sN2 = nextWkS(s), ho = sN2 && oppOf(sN2.weeks[sN2.wk] || {}, s.me);\n"
            "      return { my: horizonTotal(live59(myT), s, nR) - horizonTotal(live59(mine), s, nR), th: horizonTotal(live59(thT), s, nR) - horizonTotal(live59(theirs), s, nR),\n"
            "        tb: on77 ? winChance(s) : null, ta: on77 ? winChance(s, myT) : null, wb: ho ? winChance(sN2) : null, wa: ho ? winChance(sN2, myT) : null };\n"
            "    };\n"
            "    const mode82 = window.__PMODE;\n"
            "    const c = cnt(after);\n    return { my, th, rb, ra, wb, wa, tb, ta, q82, mode82, short:",
            "return { my, th, rb, ra, wb, wa, tb, ta, q82, mode82, short:")
    t = lit(t, "082: work out every projection just after the result shows",
            "window.__PMODE, tm82]);\n",
            "window.__PMODE, tm82]);\n"
            "  const [cmp82, setCmp82] = useState(null); // change 082: every projection, filled in a moment after the main result\n"
            "  useEffect(() => {\n"
            "    setCmp82(null);\n"
            "    if (!res || !res.q82) return;\n"
            "    const id = setTimeout(() => setCmp82(GX_PM82.filter(([k]) => gxCanMode82(k)).map(([k, l]) => ({ k, l, ...(k === res.mode82 ? { my: res.my, th: res.th, tb: res.tb, ta: res.ta, wb: res.wb, wa: res.wa } : gxWithMode82(k, res.q82)) }))), 60);\n"
            "    return () => clearTimeout(id);\n"
            "  }, [res]);\n",
            "const [cmp82, setCmp82] = useState(null);")
    t = lit(t, "082: picker under the verdict",
            "            <span className=\"text-sm text-slate-500\">{vd[2]}</span>\n          </div>",
            "            <span className=\"text-sm text-slate-500\">{vd[2]}</span>\n          </div>\n          {res.mode82 ? <GxTradeModes82 part=\"pick\" res={res} tm={tm82} setTm={setTm82} /> : null}",
            "{res.mode82 ? <GxTradeModes82 part=\"pick\" res={res} tm={tm82} setTm={setTm82} /> : null}")
    t = lit(t, "082: every projection table",
            "          {res.short.length ? <div className=\"text-sm\" style={{ marginTop: 10, color: \"var(--bad)\" }}>",
            "          {res.mode82 ? <GxTradeModes82 res={res} cmp={cmp82} tm={tm82} setTm={setTm82} /> : null}\n"
            "          {res.short.length ? <div className=\"text-sm\" style={{ marginTop: 10, color: \"var(--bad)\" }}>",
            "<GxTradeModes82 res={res}")
    return t


edit(APP, change)
