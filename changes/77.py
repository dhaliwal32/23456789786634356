# changes/077-trade-ranks-this-week.py - trade result: all three position ranks (forwards, defence, goalies) and this week's win chance

OLD_CALC = '''    const wb = hasOpp ? winChance(sN) : null, wa = hasOpp ? winChance(sN, after) : null;
    const c = cnt(after);
    return { my, th, rb, ra, wb, wa, short: ["F", "D", "G"].filter((k) => c[k] < mins[k]) };'''
NEW_CALC = '''    const wb = hasOpp ? winChance(sN) : null, wa = hasOpp ? winChance(sN, after) : null;
    // change 077: this week's win chance too, while the week still has days to play
    const w77 = deriveWeek(s.weeks[s.wk] || s.weeks[0], s.autoDone), on77 = oppOf(w77, s.me) && (w77.done || 0) < (w77.dates || []).length;
    const tb = on77 ? winChance(s) : null, ta = on77 ? winChance(s, after) : null;
    const c = cnt(after);
    return { my, th, rb, ra, wb, wa, tb, ta, short: ["F", "D", "G"].filter((k) => c[k] < mins[k]) };'''

OLD_TILES = '''<div className="text-xs text-slate-500">{grp && grp[1] ? GN[grp[0]] + " " + ordN(res.rb[grp[0]]) + " \\u2192 " + ordN(res.ra[grp[0]]) : "position ranks unchanged"}</div></div>
            {res.wb != null && res.wa != null ? <div className="gx-stc"><div className="text-xs text-slate-500">Next week</div>'''
NEW_TILES = '''<div className="text-xs text-slate-500">by team strength</div></div>
            <div className="gx-stc" data-c77="pos"><div className="text-xs text-slate-500">Position ranks</div>
              {["F", "D", "G"].map((k) => { const b = res.rb[k], a = res.ra[k], f = (v) => (v ? ordN(v) : "\\u2013"); return (
                <div key={k} style={{ display: "flex", alignItems: "baseline", gap: 6, fontSize: 15, fontWeight: 600, fontVariantNumeric: "tabular-nums", marginTop: 2 }}>
                  <span className="text-xs text-slate-500" style={{ width: 74, flexShrink: 0, fontWeight: 400 }}>{GN[k][0].toUpperCase() + GN[k].slice(1)}</span>
                  {b === a ? <><span>{f(b)}</span><span className="text-xs text-slate-500" style={{ fontWeight: 400 }}>same</span></> : <span>{arrow(b, a, f, (b || 0) - (a || 0))}</span>}
                </div>
              ); })}
            </div>
            {res.tb != null && res.ta != null ? <div className="gx-stc" data-c77="week"><div className="text-xs text-slate-500">This week</div><div className="gx-stv">{arrow(res.tb, res.ta, wpTxt, Math.round(res.ta * 100) - Math.round(res.tb * 100))}</div><div className="text-xs text-slate-500">chance to win</div></div> : null}
            {res.wb != null && res.wa != null ? <div className="gx-stc"><div className="text-xs text-slate-500">Next week</div>'''


def change(t):
    t = lit(t, "077: this week's win chance", OLD_CALC, NEW_CALC, "change 077: this week's win chance")
    t = lit(t, "077: position ranks and this week tiles", OLD_TILES, NEW_TILES, 'data-c77="pos"')
    return t


edit(APP, change)
