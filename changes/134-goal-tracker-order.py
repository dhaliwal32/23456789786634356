# changes/134-goal-tracker-order.py - the goal tracker lists goals by the real time they were scored, newest first, across all games (it was grouped by game and sorted the clock as text)

def change(t):
    t = lit(t, "134: keep when each goal happened",
            'timeInPeriod: (e.clock || {}).displayValue || "", awayScore',
            'timeInPeriod: (e.clock || {}).displayValue || "", wc: e.wallclock || "", awayScore',
            'wc: e.wallclock || ""')
    t = lit(t, "134: newest goal first",
            'all.sort((a, b) => String(b.g.startTimeUTC).localeCompare(String(a.g.startTimeUTC)) || ((b.x.periodDescriptor || {}).number || 0) - ((a.x.periodDescriptor || {}).number || 0) || String(b.x.timeInPeriod).localeCompare(String(a.x.timeInPeriod)));',
            'const gw134 = ({ g, x }) => { const w = Date.parse(x.wc || ""); if (!isNaN(w)) return w; const m = String(x.timeInPeriod || "0:0").split(":"), n = ((x.periodDescriptor || {}).number || 1) - 1; return (Date.parse(g.startTimeUTC || "") || 0) + (n * 1200 + (+m[0] || 0) * 60 + (+m[1] || 0)) * 1600 + n * 1080e3; };\n    all.sort((a, b) => gw134(b) - gw134(a)); /* change 134 */',
            '/* change 134 */')
    return t


edit(APP, change)
