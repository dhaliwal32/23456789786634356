# changes/136-live-fixes.py - live fixes from game night: player scores below their projection are no longer red (plain text again); live ESPN data is fetched fresh every 5 seconds instead of possibly getting a cached copy (it was running about 40 seconds behind ESPN, so the top score briefly dropped a point when ESPN's sync had a stat the live feed did not yet); the line under the scores now says "Projected to win by" / "Projected to lose by", since it is the week projection, not the current score

def change(t):
    t = lit(t, "136: no red player scores",
            ' : p.st && p.x0 != null && v < p.x0 - 0.05 ? { color: "var(--bad)" } : null}>{p.st && p.a == null',
            ' : null}>{p.st && p.a == null',
            'style={win ? { color: "var(--good)", fontWeight: 600 } : null}>{p.st && p.a == null')
    t = lit(t, "136: fresh game summaries",
            'fetch(GX_E132 + "summary?event=" + id)',
            'fetch(GX_E132 + "summary?event=" + id + "&_=" + Math.floor(Date.now() / 5000))',
            '"summary?event=" + id + "&_="')
    t = lit(t, "136: fresh scoreboard",
            'nf(GX_E132 + "scoreboard")',
            'nf(GX_E132 + "scoreboard?_=" + Math.floor(Date.now() / 5000))',
            '"scoreboard?_="')
    t = lit(t, "136: margin line says projected",
            '{mine ? (margin >= 0 ? "Ahead by " : "Behind by ") + f1(Math.abs(margin)) : teamName(s, margin >= 0 ? a : b) + " ahead by " + f1(Math.abs(margin))}',
            '{mine ? (margin >= 0 ? "Projected to win by " : "Projected to lose by ") + f1(Math.abs(margin)) : teamName(s, margin >= 0 ? a : b) + " projected to win by " + f1(Math.abs(margin))}',
            '"Projected to win by "')
    return t


edit(APP, change)
