# changes/189-trade-picker-stats.py - Trades "+ Add players" sheet shows every stat for each player, like Pickups: skaters (GP FPTS G A PTS +/- PIM SOG HIT BLK TOI) and goalies (GP FPTS W L OTL GA SV SV% GAA SO TOI) in their own groups, points per game first, a Stats range picker (Season, Last 7/15/30 days, projected), tap any heading to sort; the name stays put while the stats slide sideways; wider window on the laptop

NEW_PICK = r'''function GxPick113({ title, list, sel, onToggle, onClose, pg, s }) {
  /* change 189: every stat in the trade player picker */
  const [q, setQ] = useState("");
  const [out, setOut] = useState(false);
  const rng = gxUse100();
  useEffect(() => { gxLoad100(rng); });
  const S = gxUseSort108();
  const close = () => { if (out) return; setOut(true); setTimeout(onClose, 160); };
  const qq = nrm(q), ord = { F: 0, D: 1, G: 2 };
  const rows = list.filter((p) => !qq || nrm(p.n).includes(qq)).sort((a, b) => (a.ir ? 1 : 0) - (b.ir ? 1 : 0) || ord[a.p] - ord[b.p] || pg(b) - pg(a));
  const srt = (L) => (s && S.k ? gxSort108(L, s, null, { PG: (p) => pg(p) }) : L);
  const sk = srt(rows.filter((p) => p.p !== "G")), go = srt(rows.filter((p) => p.p === "G"));
  const row = (p) => {
    const on = sel.includes(p.id);
    return (
      <button key={p.id} type="button" className={"it r189" + (on ? " on" : "")} onClick={() => onToggle(p.id)}>
        <span className="lf"><span className="ck">{on ? "\u2713" : ""}</span><GxFace p={p} size={26} /><span className="min-w-0"><span className="block truncate">{p.n}</span><span className="block truncate text-xs text-slate-500">{p.p + " \u00b7 " + p.t + (p.ir ? " \u00b7 IR" : "")}</span></span></span>
        <span className="n pg">{f1(pg(p))}</span>
        {s ? <GxSC106 p={p} s={s} mode={p.p === "G" ? "go" : "sk"} /> : null}
      </button>
    );
  };
  const head = (lbl, mode) => <div className="hr189"><span className="lf">{lbl}</span><GxHB108 k="PG" l="P/G" />{s ? <GxSH106 mode={mode} /> : null}</div>;
  return (
    <div className={"gx-so107" + (out ? " out" : "")} onClick={close}>
      <div className="gx-sim107 gx-pk113 gx-pk189" onClick={(e) => e.stopPropagation()}>
        <div className="hd"><span className="t">{title}</span><span className="m">{sel.length ? sel.length + " picked" : ""}</span><button type="button" className="x" aria-label="Close" onClick={close}>{"\u00d7"}</button></div>
        <div className="tp189"><input className={inp + " sr"} placeholder="Search" value={q} onChange={(e) => setQ(e.target.value)} /><GxRngSel100 /></div>
        <div className="lst">
          {sk.length ? <>{head("Skaters", "sk")}{sk.map(row)}</> : null}
          {go.length ? <>{head("Goalies", "go")}{go.map(row)}</> : null}
        </div>
        <div className="act"><button type="button" className="pr" onClick={close}>Done</button></div>
      </div>
    </div>
  );
}
'''

OLD_CALL = r'''pg={pg} onToggle={(id) => (pk113 === "give" ? toggle(give, setGive, id) : toggle(get, setGet, id))} onClose={() => setPk113(null)} />'''
NEW_CALL = r'''pg={pg} s={s} onToggle={(id) => (pk113 === "give" ? toggle(give, setGive, id) : toggle(get, setGet, id))} onClose={() => setPk113(null)} />'''

NEW_CSS = r'''  /* change 189 (install.py) */
  .gx-sim107.gx-pk189 { max-width: 980px; }
  .gx-pk189 .tp189 { display: flex; gap: 8px; align-items: center; }
  .gx-pk189 .tp189 .sr { flex: 1; min-width: 0; }
  .gx-pk189 .tp189 .gx-rs100 { flex: none; display: flex; align-items: center; gap: 6px; }
  .gx-pk189 .tp189 .gx-rs100 select { width: auto; max-width: 170px; }
  .gx-pk189 .lst { overflow: auto; }
  .gx-pk189 .hr189, .gx-pk189 .it.r189 { display: grid; grid-template-columns: minmax(230px, 1fr) 56px repeat(11, 60px); align-items: center; min-width: max-content; width: 100%; gap: 0; padding: 0; }
  .gx-pk189 .it.r189 { height: 52px; border-top: 1px solid var(--line); }
  .gx-pk189 .hr189 { position: sticky; top: 0; z-index: 2; background: var(--card); height: 34px; border-top: 1px solid var(--line); font-size: 12px; color: var(--mute); }
  .gx-pk189 .hr189 .lf { font-weight: 600; letter-spacing: .04em; text-transform: uppercase; z-index: 3; }
  .gx-pk189 .lf { position: sticky; left: 0; z-index: 1; background: var(--card); display: flex; align-items: center; gap: 8px; height: 100%; min-width: 0; padding: 0 8px 0 2px; }
  .gx-pk189 .it.r189.on .lf { background: var(--card); }
  .gx-pk189 .it .ck { margin-left: 0 !important; }
  .gx-pk189 .n { text-align: right; padding-right: 8px; font-size: 13px; font-variant-numeric: tabular-nums; white-space: nowrap; }
  .gx-pk189 .hr189 .n { font-size: 12px; }
  .gx-pk189 .n.pg { color: var(--ink); }
  @media (max-width: 640px) {
    .gx-pk189 .hr189, .gx-pk189 .it.r189 { grid-template-columns: 172px 46px repeat(11, 46px); width: auto; }
    .gx-pk189 .tp189 .gx-rs100 select { max-width: 132px; }
    .gx-pk189 .lf { gap: 6px; }
    .gx-pk189 .tp189 .gx-rs100 > span { display: none; }
  }
</style>'''


def cut(t, label, start, end, new, done):
    if done in t:
        print("(install) " + label + ": already done")
        return t
    i = t.find(start)
    if i < 0 or t.find(start, i + 1) >= 0:
        fail(label + ": start text not found exactly once")
    j = t.find(end, i)
    if j < 0:
        fail(label + ": end text not found")
    print("(install) " + label + ": updated")
    return t[:i] + new + t[j:]


def change(t):
    t = lit(t, "189: styles", "</style>", NEW_CSS, "change 189 (install.py)")
    t = cut(t, "189: picker with stats", "function GxPick113({ title, list, sel, onToggle, onClose, pg", "// laptop only: week-by-week chart and player comparison", NEW_PICK, "change 189: every stat in the trade player picker")
    t = lit(t, "189: pass the app state", OLD_CALL, NEW_CALL, "pg={pg} s={s} onToggle")
    return t


edit(APP, change)
