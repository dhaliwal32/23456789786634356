# changes/093-pickup-projection-pick.py - Pickups result: tap a projection (ESPN, GM model, Blend, AI) to see the whole result with it, like Trades

NEW_CSS = r'''  /* change 093 (install.py) */
  .gx-pm92.r { cursor: pointer; border-radius: 6px; }
  .gx-pm92.r:hover { background: var(--line); }
</style>'''

def change(t):
    t = lit(t, "093: styles", "</style>", NEW_CSS, "change 093 (install.py)")
    # projection for this box only
    t = lit(t, "093: state",
        "  const res = useMemo(() => {\n    const base = calc();\n    const A = new Set(ok.map((x) => x.a.id)), D = new Set(ok.map((x) => x.d.id));",
        "  const [tm93, setTm93] = useState(null); // change 093: projection for this box only\n  const res = useMemo(() => gxWithMode82(tm93, () => {\n    const base = calc();\n    const A = new Set(ok.map((x) => x.a.id)), D = new Set(ok.map((x) => x.d.id));",
        "const [tm93, setTm93] = useState(null);")
    t = lit(t, "093: result uses it",
        "    return { ...base, rb: pos(leagueTable(s)), ra: pos(t2), mode: window.__PMODE };\n  }, [key, s.players, s.wk, window.__PMODE]);",
        "    return { ...base, rb: pos(leagueTable(s)), ra: pos(t2), mode: window.__PMODE };\n  }), [key, s.players, s.wk, window.__PMODE, tm93]);",
        "}), [key, s.players, s.wk, window.__PMODE, tm93]);")
    # picker buttons above the tiles
    t = lit(t, "093: picker",
        "        <span className=\"text-sm text-slate-500\">{vd[2]}</span>\n      </div>\n      <div className=\"gx-stg\">",
        "        <span className=\"text-sm text-slate-500\">{vd[2]}</span>\n      </div>\n"
        "      <div className=\"gx-pmh82\">{/* gx093 */}\n"
        "        <span className=\"text-xs text-slate-500\">Projection</span>\n"
        "        <span className=\"gx-seg\">{GX_PM82.map(([k, l]) => <button key={k} type=\"button\" disabled={!gxCanMode82(k)} className={res.mode === k ? \"on\" : \"\"} onClick={() => setTm93(k === window.__PMODE ? null : k)}>{l}</button>)}</span>\n"
        "        {tm93 && tm93 !== window.__PMODE ? <span className=\"text-xs text-slate-500\">{\"This box only. The rest of the app still uses \" + ((GX_PM82.find((x) => x[0] === window.__PMODE) || [0, \"Best\"])[1]) + \".\"}</span> : null}\n"
        "      </div>\n"
        "      <div className=\"gx-stg\">",
        "{/* gx093 */}")
    # rows can be tapped
    t = lit(t, "093: rows",
        "          <div key={x.k} className={\"gx-pm92\" + (x.k === res.mode ? \" on\" : \"\")}>\n            <span>{x.l}{x.k === res.mode ? <span className=\"text-xs text-slate-500\"> (app)</span> : null}</span>",
        "          <div key={x.k} className={\"gx-pm92 r\" + (x.k === res.mode ? \" on\" : \"\")} role=\"button\" onClick={() => setTm93(x.k === window.__PMODE ? null : x.k)} title=\"Show the pickup with this projection\">\n            <span>{x.l}{x.k === window.__PMODE ? <span className=\"text-xs text-slate-500\"> (app)</span> : null}</span>",
        "title=\"Show the pickup with this projection\"")
    t = lit(t, "093: note",
        "Season is points for the rest of the season. The weeks show the change in your chance to win. Win means your lineup gains points.</div>",
        "Tap a projection to see the result with it. Season is points for the rest of the season. The weeks show the change in your chance to win. Win means your lineup gains points.</div>",
        "Tap a projection to see the result with it.")
    return t

edit(APP, change)
