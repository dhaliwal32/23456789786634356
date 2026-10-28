# changes/110-trades-clean.py - Trades result cleaned up like Simulate: verdict as a small tag, three tiles (your lineup, their lineup, this week), everything else behind More details, no extra writing

NEW_CSS = r'''  /* change 110 (install.py) */
  .gx-vd110 { display: inline-block; font-size: 12px; font-weight: 700; letter-spacing: .04em; text-transform: uppercase; padding: 3px 10px; border-radius: 99px; color: #fff; }
  .gx-tr110 > .gx-stc:not([data-c77="week"]):nth-child(n+3) { display: none; }
  .gx-tr110 > [data-c77="week"] { grid-column: 1 / -1; }
  .gx-tp110 [data-r59="after"] { display: none; }
  .gx-tp110.open [data-r59="after"] { display: block; }
  .gx-tp110 .bg-blue-600 { border-radius: 999px !important; padding: 10px 22px !important; }
  .gx-tp110 .gx-mr110 { font-size: 13px; color: var(--accent); margin-top: 10px; }
</style>'''


def change(t):
    t = lit(t, "110: styles", "</style>", NEW_CSS, "change 110 (install.py)")
    t = lit(t, "110: details state", "function TradeBuilder({ s, initPartner, setS }) {", "function TradeBuilder({ s, initPartner, setS }) {\n  const [det110, setDet110] = useState(false);", "const [det110, setDet110] = useState(false);")
    t = lit(t, "110: result panel", '      {res && vd ? (\n        <div className="gx-pn"><b></b><b></b><b></b><b></b>',
            '      {res && vd ? (\n        <div className={"gx-pn gx-tp110" + (det110 ? " open" : "")}><b></b><b></b><b></b><b></b>', '"gx-pn gx-tp110" + (det110')
    t = lit(t, "110: verdict tag", '            <span className="font-semibold" style={{ color: vd[1] }}>{vd[0]}</span>\n            <span className="text-sm text-slate-500">{vd[2]}</span>',
            '            <span className="gx-vd110" style={{ background: vd[1] }}>{vd[0]}</span>', 'className="gx-vd110"')
    t = lit(t, "110: projection buttons only in details", '{res.mode82 ? <GxTradeModes82 part="pick" res={res} tm={tm82} setTm={setTm82} /> : null}',
            '{det110 && res.mode82 ? <GxTradeModes82 part="pick" res={res} tm={tm82} setTm={setTm82} /> : null}', '{det110 && res.mode82 ? <GxTradeModes82 part="pick"')
    t = lit(t, "110: three tiles", '<div className="gx-stg">\n            <div className="gx-stc"><div className="text-xs text-slate-500 truncate">{gxYou(s, "Your lineup"',
            '<div className={"gx-stg" + (det110 ? "" : " gx-tr110")}>\n            <div className="gx-stc"><div className="text-xs text-slate-500 truncate">{gxYou(s, "Your lineup"', '(det110 ? "" : " gx-tr110")')
    t = lit(t, "110: every projection only in details", '{res.mode82 ? <GxTradeModes82 res={res} cmp={cmp82} tm={tm82} setTm={setTm82} /> : null}',
            '{det110 && res.mode82 ? <GxTradeModes82 res={res} cmp={cmp82} tm={tm82} setTm={setTm82} /> : null}', '{det110 && res.mode82 ? <GxTradeModes82 res={res}')
    t = lit(t, "110: more details button", "{/* gx086-apply */}",
            '<button type="button" className="gx-mr110" onClick={() => setDet110(!det110)}>{det110 ? "Hide details" : "More details"}</button>{/* gx086-apply */}', 'className="gx-mr110"')
    t = lit(t, "110: no apply note", '<span className="text-xs text-slate-500">Shows this trade on every page of the app, through syncs, until you undo it. Nothing changes on ESPN.</span>', "", None)
    return t


edit(APP, change)
