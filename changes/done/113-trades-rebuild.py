# changes/113-trades-rebuild.py - Trades rebuilt like Simulate: team chips instead of drop-downs, "+ Add players" opens a clean picker, no long roster list; on a laptop an analysis section (week-by-week chart, player comparison) and details open by default

NEW_CSS = r'''  /* change 113 (install.py) */
  .gx-tw113 { display: flex; gap: 8px; overflow-x: auto; scrollbar-width: none; padding: 2px 0 4px; }
  .gx-tw113::-webkit-scrollbar { display: none; }
  .gx-tw113 button { flex: none; display: flex; align-items: center; gap: 8px; padding: 7px 12px 7px 7px; border: 1px solid var(--line2); border-radius: 999px; font-size: 13px; color: var(--ink); white-space: nowrap; }
  .gx-tw113 button .b { width: 24px; height: 24px; border-radius: 99px; background: var(--card3, var(--line)); display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: 700; }
  .gx-tw113 button.on { background: var(--ink); color: var(--bg); border-color: var(--ink); }
  .gx-tw113 button.on .b { background: var(--bg); color: var(--ink); }
  .gx-th113 { display: flex; align-items: center; gap: 8px; margin-bottom: 8px; font-size: 13px; color: var(--mute); }
  .gx-th113 button { color: var(--accent); }
  .gx-add113 { display: block; width: 100%; margin-top: 8px; padding: 9px; border: 1px dashed var(--line2); border-radius: 10px; font-size: 14px; color: var(--ink); }
  .gx-pk113 .lst { max-height: 60vh; overflow-y: auto; margin-top: 8px; }
  .gx-pk113 .it { display: flex; align-items: center; gap: 10px; width: 100%; padding: 9px 4px; border-top: 1px solid var(--line); text-align: left; }
  .gx-pk113 .it .ck { width: 22px; height: 22px; border-radius: 99px; border: 1.5px solid var(--line2); margin-left: auto; display: flex; align-items: center; justify-content: center; font-size: 13px; flex: none; }
  .gx-pk113 .it.on .ck { background: var(--accent); border-color: var(--accent); color: var(--on, #fff); }
  .gx-pk113 .it .v { font-size: 13px; color: var(--mute); font-variant-numeric: tabular-nums; }
  .gx-lab113 .gx-pd-t th, .gx-lab113 .gx-pd-t td { padding: 6px 6px; }
  .gx-lab113 .lg { display: flex; gap: 14px; font-size: 12px; color: var(--mute); margin-top: 6px; }
  .gx-lab113 .lg i { display: inline-block; width: 12px; height: 3px; vertical-align: middle; margin-right: 6px; }
</style>'''

HELPERS = r'''// ---------- change 113: Trades rebuilt (install.py) ----------
function GxPick113({ title, list, sel, onToggle, onClose, pg }) {
  const [q, setQ] = useState("");
  const [out, setOut] = useState(false);
  const close = () => { if (out) return; setOut(true); setTimeout(onClose, 160); };
  const qq = nrm(q), ord = { F: 0, D: 1, G: 2 };
  const rows = list.filter((p) => !qq || nrm(p.n).includes(qq)).sort((a, b) => (a.ir ? 1 : 0) - (b.ir ? 1 : 0) || ord[a.p] - ord[b.p] || pg(b) - pg(a));
  return (
    <div className={"gx-so107" + (out ? " out" : "")} onClick={close}>
      <div className="gx-sim107 gx-pk113" onClick={(e) => e.stopPropagation()}>
        <div className="hd"><span className="t">{title}</span><span className="m">{sel.length ? sel.length + " picked" : ""}</span><button type="button" className="x" aria-label="Close" onClick={close}>{"×"}</button></div>
        <input className={inp + " sr"} placeholder="Search" value={q} onChange={(e) => setQ(e.target.value)} />
        <div className="lst">
          {rows.map((p) => {
            const on = sel.includes(p.id);
            return (
              <button key={p.id} type="button" className={"it" + (on ? " on" : "")} onClick={() => onToggle(p.id)}>
                <GxFace p={p} size={26} />
                <span className="min-w-0"><span className="block truncate">{p.n}</span><span className="text-xs text-slate-500">{p.p + " · " + p.t + (p.ir ? " · IR" : "")}</span></span>
                <span className="v" style={{ marginLeft: "auto" }}>{f1(pg(p))}</span>
                <span className="ck" style={{ marginLeft: 10 }}>{on ? "✓" : ""}</span>
              </button>
            );
          })}
        </div>
        <div className="act"><button type="button" className="pr" onClick={close}>Done</button></div>
      </div>
    </div>
  );
}
// laptop only: week-by-week chart and player comparison
function GxTradeLab113({ s, res, Gv, Rv, pg, gl }) {
  const K = s.blend;
  const rng = gxUse100();
  useEffect(() => { gxLoad100("sea"); gxLoad100("l15"); }, []);
  const W = useMemo(() => {
    if (!res || !res.myL || !res.meL) return [];
    const out = [];
    for (let i = s.wk; i < s.weeks.length; i++) {
      const dw = deriveWeek(s.weeks[i], s.autoDone), from = i === s.wk ? dw.done || 0 : 0;
      out.push({ i, b: weekProj(res.meL, dw, K, from).total, a: weekProj(res.myL, dw, K, from).total });
    }
    return out;
  }, [res]);
  const n = W.length, w = 640, h = 180, pad = 30;
  const mx = Math.max(1, ...W.map((x) => Math.max(x.a, x.b))) * 1.08;
  const X = (k) => pad + (n <= 1 ? 0 : (k * (w - pad - 10)) / (n - 1)), Y = (v) => h - 22 - (v / mx) * (h - 34);
  const line = (key) => W.map((x, k) => X(k).toFixed(1) + "," + Y(x[key]).toFixed(1)).join(" ");
  const tot = W.reduce((t, x) => t + x.a - x.b, 0);
  const st = (p, r) => { const v = gxVals106(p, s, r); const gp = gxNum108(v[1]); return gp > 0 ? f1(gxNum108(v[0]) / gp) : "-"; };
  const row = (p, side) => {
    const v = gxVals106(p, s, "sea");
    return (
      <tr key={side + p.id}>
        <td><span className="inline-flex items-center gap-2"><GxFace p={p} size={20} />{p.n}</span></td>
        <td>{side === "g" ? "Give" : "Get"}</td><td>{p.p}</td><td>{p.t}</td><td>{v[1]}</td><td>{v[0]}</td><td>{st(p, "sea")}</td><td>{st(p, "l15")}</td><td className="b">{f1(pg(p))}</td><td>{gl(p)}</td>
      </tr>
    );
  };
  return (
    <div className="gx-lab113 m-hide space-y-3">
      <div className="gx-pn">
        <div className="gx-pd-h">Week by week<span className="r">{"Your projected points, rest of season · " + (tot >= 0 ? "+" : "") + Math.round(tot)}</span></div>
        {n > 1 ? (
          <svg viewBox={"0 0 " + w + " " + h} width="100%" style={{ display: "block" }}>
            <line x1={pad} x2={w - 10} y1={h - 22} y2={h - 22} style={{ stroke: "var(--line)" }} />
            <polyline points={line("b")} style={{ fill: "none", stroke: "var(--mute)", strokeWidth: 2, strokeDasharray: "4 4" }} />
            <polyline points={line("a")} style={{ fill: "none", stroke: "var(--accent)", strokeWidth: 2.5 }} />
            {W.map((x, k) => (k % Math.max(1, Math.ceil(n / 12)) === 0 ? <text key={k} x={X(k)} y={h - 6} textAnchor="middle" style={{ fontSize: 11, fill: "var(--mute)" }}>{"W" + (x.i + 1)}</text> : null))}
          </svg>
        ) : <div className="text-sm text-slate-500">Not enough weeks left.</div>}
        <div className="lg"><span><i style={{ background: "var(--accent)" }}></i>After the trade</span><span><i style={{ background: "var(--mute)" }}></i>Now</span></div>
      </div>
      <div className="gx-pn">
        <div className="gx-pd-h">Player comparison</div>
        <table className="gx-pd-t">
          <thead><tr><th>Player</th><th>Side</th><th>Pos</th><th>Team</th><th>GP</th><th>FPTS</th><th>Avg</th><th>Last 15</th><th>Proj/g</th><th>Games left</th></tr></thead>
          <tbody>{Gv.map((p) => row(p, "g"))}{Rv.map((p) => row(p, "r"))}</tbody>
        </table>
      </div>
    </div>
  );
}
'''

PARTNER = '''      <div className="gx-tw113">
        {others.map((t) => <button key={t.id} type="button" className={partner === t.id ? "on" : ""} onClick={() => { setPartner(t.id); setGet([]); setPick({}); setEdit(-1); }}><span className="b">{(String(t.name || "?").replace(/[^A-Za-z0-9 ]/g, "").trim()[0] || "?").toUpperCase()}</span>{t.name}</button>)}
      </div>
      {give.length || get.length ? <div style={{ textAlign: "right" }}><button className="text-xs text-slate-500 underline" onClick={() => { setGive([]); setGet([]); setPick({}); setEdit(-1); }}>Clear</button></div> : null}
'''


def change(t):
    t = lit(t, "113: styles", "</style>", NEW_CSS, "change 113 (install.py)")
    t = lit(t, "113: helpers", ROOT, HELPERS + ROOT, "change 113: Trades rebuilt")
    # state
    t = lit(t, "113: picker state, details open on a laptop", "  const [det110, setDet110] = useState(false);",
            "  const [det110, setDet110] = useState(() => window.innerWidth > 640);\n  const [pk113, setPk113] = useState(null);", "const [pk113, setPk113] = useState(null);")
    # result keeps the rosters for the analysis
    t = lit(t, "113: rosters for the analysis", "return { my, th, rb, ra, wb, wa, tb, ta, q82, mode82, short: [",
            "return { myL: live59(myT), meL: live59(mine), my, th, rb, ra, wb, wa, tb, ta, q82, mode82, short: [", "return { myL: live59(myT), meL: live59(mine),")
    # team chips
    i = t.find('      <div className="flex items-center gap-2">\n        <span className="text-sm text-slate-500 whitespace-nowrap">Trade with</span>')
    if 'className="gx-tw113"' in t:
        print("(install) 113: team chips: already done")
    else:
        if i < 0:
            fail("113: Trade with row not found")
        j = t.find("      </div>\n", i) + len("      </div>\n")
        t = t[:i] + PARTNER + t[j:]
        print("(install) 113: team chips: updated")
    # add players buttons
    t = lit(t, "113: add players (give)", '{Gv.length ? Gv.map((p, i) => offerRow(p, i, () => toggle(give, setGive, p.id))) : <div className="text-sm text-slate-500">Tap your players below</div>}',
            '{Gv.map((p, i) => offerRow(p, i, () => toggle(give, setGive, p.id)))}<button type="button" className="gx-add113" onClick={() => setPk113("give")}>+ Add players</button>', 'onClick={() => setPk113("give")}')
    t = lit(t, "113: add players (get)", '{Rv.length ? Rv.map((p, i) => offerRow(p, i, () => toggle(get, setGet, p.id))) : <div className="text-sm text-slate-500">Tap their players below</div>}',
            '{Rv.map((p, i) => offerRow(p, i, () => toggle(get, setGet, p.id)))}<button type="button" className="gx-add113" onClick={() => setPk113("get")}>+ Add players</button>', 'onClick={() => setPk113("get")}')
    # no long roster list; picker and laptop analysis instead
    t = lit(t, "113: roster list replaced",
            '      <div className="gx-pn"><b></b><b></b><b></b><b></b>\n        <div style={{ display: "flex", alignItems: "baseline", marginBottom: 6 }}>\n          <span className="gx-tag">Rosters</span>',
            '      {res && vd ? <GxTradeLab113 s={s} res={res} Gv={Gv} Rv={Rv} pg={pg} gl={gl} /> : null}\n'
            '      {pk113 ? <GxPick113 title={pk113 === "give" ? gxYou(s, "You give", teamName(s, s.me) + " gives") : teamName(s, partner)} list={pk113 === "give" ? mine : theirs} sel={pk113 === "give" ? give : get} pg={pg} onToggle={(id) => (pk113 === "give" ? toggle(give, setGive, id) : toggle(get, setGet, id))} onClose={() => setPk113(null)} /> : null}\n'
            '      <div className="gx-pn" style={{ display: "none" }}><b></b><b></b><b></b><b></b>\n        <div style={{ display: "flex", alignItems: "baseline", marginBottom: 6 }}>\n          <span className="gx-tag">Rosters</span>',
            "<GxTradeLab113 s={s}")
    # trading for another team: tucked away
    t = lit(t, "113: other side state", "  const [side, setSide] = useState(s.me);\n  window.__TB_REAL = s.me;",
            "  const [side, setSide] = useState(s.me);\n  const [from113, setFrom113] = useState(false);\n  window.__TB_REAL = s.me;", "const [from113, setFrom113] = useState(false);")
    i = t.find('      <div className="flex items-center gap-2" style={{ marginBottom: 12 }} data-c78="side">')
    if '"Trading as you"' in t:
        print("(install) 113: trade from: already done")
    else:
        if i < 0:
            fail("113: Trade from row not found")
        j = t.find("      </div>\n", i) + len("      </div>\n")
        new = ('      <div className="gx-th113" data-c78="side">{a === s.me ? "Trading as you" : "Trading as " + teamName(s, a)}'
               '<button type="button" onClick={() => setFrom113(!from113)}>{from113 ? "Done" : "Change"}</button>{a !== s.me ? <button type="button" onClick={() => setSide(s.me)}>Back to mine</button> : null}</div>\n'
               '      {from113 ? <select className={inp + " w-full"} style={{ marginBottom: 12 }} value={a} onChange={(e) => { setSide(e.target.value); setFrom113(false); }}>{s.teams.map((t) => <option key={t.id} value={t.id}>{t.name}{t.id === s.me ? " (you)" : ""}</option>)}</select> : null}\n')
        t = t[:i] + new + t[j:]
        print("(install) 113: trade from: updated")
    return t


edit(APP, change)
