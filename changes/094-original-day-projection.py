# changes/094-original-day-projection.py - Today and Matchup also show each day's original projection (before games started), not only the updated one

def change(t):
    # Today, This week box, today's details: "Projected" becomes "Projected now", plus an "Original" row
    t = lit(t, "094: today original row",
        r'''<span className="l">Projected</span><span>{f1(me[d0]) + " "}<span style={mc(m0)}>{(m0 >= 0 ? "ahead by " : "behind by ") + f1(Math.abs(m0))}</span></span><span>{f1(th[d0])}</span></> : null}
        {k0 === "p" ?''',
        r'''<span className="l">Projected now</span><span>{f1(me[d0]) + " "}<span style={mc(m0)}>{(m0 >= 0 ? "ahead by " : "behind by ") + f1(Math.abs(m0))}</span></span><span>{f1(th[d0])}</span>
          <span className="l">Original</span><span>{f1(exp(X, d0)) + " "}<span style={mc(exp(X, d0) - exp(Y, d0))}>{(exp(X, d0) - exp(Y, d0) >= 0 ? "ahead by " : "behind by ") + f1(Math.abs(exp(X, d0) - exp(Y, d0)))}</span></span><span>{f1(exp(Y, d0))}</span></> : null /* gx094 */}
        {k0 === "p" ?''',
        "/* gx094 */")
    # Today, This week box, a finished day: show the original projection above "Vs expected"
    t = lit(t, "094: finished day original row",
        r'''<span className="l">Vs expected</span>''',
        r'''<span className="l">Original</span><span>{f1(exp(X, d0))}</span><span>{f1(exp(Y, d0))}</span>
          <span className="l">Vs expected</span>''',
        r'''<span className="l">Original</span><span>{f1(exp(X, d0))}</span><span>{f1(exp(Y, d0))}</span>''')
    # Matchup page: day header gets an "Original projection" line once games have started
    t = lit(t, "094: matchup day original line",
        r'''{(dayTot >= 0 ? "+" : "") + f1(dayTot)}</span>
          </span>
        </div>''',
        r'''{(dayTot >= 0 ? "+" : "") + f1(dayTot)}</span>
          </span>
        </div>
        {state !== "projected" && x.proj != null && y.proj != null ? <div className="text-xs text-slate-500" style={{ textAlign: "right", marginTop: -4, marginBottom: 6, fontVariantNumeric: "tabular-nums" }} data-gx="094">{"Original projection " + f1(x.proj) + " to " + f1(y.proj) + " (" + (x.proj - y.proj >= 0 ? "+" : "") + f1(x.proj - y.proj) + ")"}</div> : null}''',
        'data-gx="094"')
    # Matchup page: under each started player's points, his original projection in small grey
    t = lit(t, "094: matchup player original",
        r''': f1(v)}</div>;''',
        r''': f1(v)}{p.st && p.x0 != null ? <div className="text-xs" style={{ color: "var(--faint)", fontWeight: 400 }} data-gx="094p"><span className="m-hide">proj </span>{f1(p.x0)}</div> : null}</div>;''',
        'data-gx="094p"')
    return t

edit(APP, change)
