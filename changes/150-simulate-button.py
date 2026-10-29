# changes/150-simulate-button.py - simulate box always fits the screen (no sideways sliding, all seven days in one row, details in two even columns) with big Whole roster / More details buttons; player screen: "Find a swap" / "Find a replacement" becomes "Simulate". A free agent opens the simulate box with him added (best drop picked); your own player opens it with him dropped so you pick who to add; another team's player opens a trade with him

NEW_CSS = r'''  /* change 150 (install.py) */
  .gx-so107 { overflow-x: hidden; }
  .gx-sim107 { box-sizing: border-box; min-width: 0; overflow-x: hidden; }
  .gx-sim107 * { box-sizing: border-box; }
  .gx-sim107 .days { overflow-x: visible; gap: 6px; }
  .gx-sim107 .dy { flex: 1 1 0; min-width: 0; padding: 8px 2px; }
  .gx-sim107 .dy b { font-size: 14px; white-space: nowrap; }
  .gx-sim107 .dy.best::after { font-size: 9px; padding: 1px 5px; }
  .gx-sim107 .gx-stg { grid-template-columns: 1fr 1fr; border-radius: 12px; overflow: hidden; }
  .gx-sim107 .gx-stg > .gx-stc:nth-child(3) { grid-column: 1 / -1; }
  .gx-sim107 .gx-stc { overflow: hidden; }
  .gx-sim107 .bt150 { display: block; width: 100%; margin-top: 12px !important; padding: 13px 0; border-radius: 12px; border: 1px solid var(--line2); background: var(--card2, var(--bg)); color: var(--ink); font-size: 15px; font-weight: 600; text-align: center; }
  @media (max-width: 640px) { .gx-sim107 .res b { font-size: 20px; } .gx-sim107 .dy span { font-size: 11px; } }
</style>'''


def change(t):
    t = lit(t, "150: styles", "</style>", NEW_CSS, "change 150 (install.py)")
    t = lit(t, "150: big Whole roster button", '<button type="button" className="lk" style={{ marginTop: 8 }} onClick={() => setAllD(!allD)}>', '<button type="button" className="lk bt150" onClick={() => setAllD(!allD)}>', 'className="lk bt150" onClick={() => setAllD(!allD)}>')
    t = lit(t, "150: big details button", '<button type="button" className="lk" style={{ marginTop: 10 }} onClick={() => setDet(!det)}>', '<button type="button" className="lk bt150" onClick={() => setDet(!det)}>', 'className="lk bt150" onClick={() => setDet(!det)}>')
    t = lit(t, "150: simulate action",
            '    trade: (p) => { window.__TRADE_P = { id: p.id, ft: p.ft };',
            '    sim: (p) => { if (p.ft !== "fa" && p.ft !== s.me) { window.__QA.trade(p); return; } window.__PICK_SIM = p.ft === "fa" ? { add: p.id } : { drop: p.id }; go("moves", "adddrop"); setTimeout(() => window.dispatchEvent(new Event("gm-pick")), 50); }, /* gx150 */\n    trade: (p) => { window.__TRADE_P = { id: p.id, ft: p.ft };',
            '/* gx150 */')
    t = lit(t, "150: Pickups opens the simulate box",
            '    window.addEventListener("gm-pick", h);\n    return () => window.removeEventListener("gm-pick", h);\n  }, []);\n  const [sim, setSim] = useState(null);',
            '    window.addEventListener("gm-pick", h);\n    const h150 = () => { if (window.__PICK_SIM) { const v = window.__PICK_SIM; window.__PICK_SIM = null; setSim(v); } };\n    window.addEventListener("gm-pick", h150);\n    return () => { window.removeEventListener("gm-pick", h); window.removeEventListener("gm-pick", h150); };\n  }, []);\n  const [sim, setSim] = useState(() => { const v = window.__PICK_SIM || null; window.__PICK_SIM = null; return v; });',
            'const h150 = () => { if (window.__PICK_SIM)')
    old = '<button type="button" className="pr" onClick={act(Q.swap)}>{Q.mine(p) ? "Find a replacement" : "Find a swap"}</button>'
    if old in t:
        if t.count(old) != 2:
            fail("150: button found " + str(t.count(old)) + " times")
        t = t.replace(old, '<button type="button" className="pr" onClick={act(Q.sim)}>Simulate</button>')
        print("(install) 150: buttons renamed: updated")
    return t


edit(APP, change)
