# changes/135-live-first.py - once games start, Matchup puts live scores first: players whose game has not started show a dash with a small grey projection (no green or red), the day total row and the day's +/- under the date show points actually scored (projected total small underneath), and the week box at the bottom shows the live week score with the projection small underneath while games are on

LV = r'''    if (v == null) return <div className={"text-slate-500" + (right ? "" : " text-right")}>{"\u2013"}</div>;
    if (state === "live" && !p.st) return <div className={right ? "" : "text-right"} data-gx="135n"><span style={{ color: "var(--faint)" }}>{"\u2013"}</span><div className="text-xs" style={{ color: "var(--faint)", fontWeight: 400 }}><span className="m-hide">proj </span>{f1(v)}</div></div>;
    const win = state === "live" ? !!(q && q.st) && v - o >= 0.05 : o == null || v - o >= 0.05;'''


def change(t):
    t = lit(t, "135: unstarted players show projection small",
            '    if (v == null) return <div className={"text-slate-500" + (right ? "" : " text-right")}>{"\\u2013"}</div>;\n    const win = o == null || v - o >= 0.05;',
            LV, 'data-gx="135n"')
    t = lit(t, "135: day total counts real points while live",
            "  const dayTot = x.act + x.total - (y.act + y.total);",
            "  const lv135 = (l) => (l.start || []).reduce((t, p) => t + (p.st ? +(p.a || 0) : 0), 0);\n  const dayTot = state === \"live\" ? lv135(x) - lv135(y) : x.act + x.total - (y.act + y.total); /* change 135 */\n  const dvD135 = state === \"live\" ? dayTot : dvOf(d);\n  const wkLive135 = Object.values((window.__LIVESC || {})[today] || {}).some((g) => g && g.s === \"L\");",
            "const dvD135")
    t = lit(t, "135: date +/- uses real points while live",
            '<small style={{ color: Math.abs(dvOf(d)) < 0.05 ? "var(--mute)" : dvOf(d) > 0 ? "var(--good)" : "var(--bad)" }}>{(dvOf(d) > 0 ? "+" : "") + f1(dvOf(d))}</small>',
            '<small style={{ color: Math.abs(dvD135) < 0.05 ? "var(--mute)" : dvD135 > 0 ? "var(--good)" : "var(--bad)" }}>{(dvD135 > 0 ? "+" : "") + f1(dvD135)}</small>',
            "f1(dvD135)")
    t = lit(t, "135: live total row",
            '<div className="text-right">{f1(x.act + x.total)}</div><div></div><div>{f1(y.act + y.total)}</div>',
            '<div className="text-right">{state === "live" ? <>{f1(lv135(x))}<div className="text-xs" style={{ color: "var(--faint)", fontWeight: 400, whiteSpace: "nowrap" }}>proj {f1(x.act + x.total)}</div></> : f1(x.act + x.total)}</div><div></div><div>{state === "live" ? <>{f1(lv135(y))}<div className="text-xs" style={{ color: "var(--faint)", fontWeight: 400, whiteSpace: "nowrap" }}>proj {f1(y.act + y.total)}</div></> : f1(y.act + y.total)}</div>',
            "f1(lv135(x))")
    t = lit(t, "135: week box shows live score during games",
            '<div className="gx-wt114"><div><small>{over ? "Week final" : "Week projected"}</small><b>{Math.round(fa)}</b></div><div className="r"><small>{over ? "Week final" : "Week projected"}</small><b>{Math.round(fb)}</b></div></div>',
            '<div className="gx-wt114">{wkLive135 && !over ? <><div><small>Week live</small><b><GxAnimNum131 v={aA} /></b><small>{"proj " + Math.round(fa)}</small></div><div className="r"><small>Week live</small><b><GxAnimNum131 v={aB} /></b><small>{"proj " + Math.round(fb)}</small></div></> : <><div><small>{over ? "Week final" : "Week projected"}</small><b>{Math.round(fa)}</b></div><div className="r"><small>{over ? "Week final" : "Week projected"}</small><b>{Math.round(fb)}</b></div></>}</div>',
            "<small>Week live</small>")
    return t


edit(APP, change)
