# changes/137-goal-tracker-links.py - in the goal tracker, tap the scorer's or an assist's name to open that player's page (when the app knows the player)

def change(t):
    t = lit(t, "137: scorer name opens player",
            '<div className="who">{who + ", " + tm}',
            '<div className="who">{p ? <button type="button" className="hover:underline text-left" style={{ fontWeight: "inherit" }} onClick={() => { if (window.__NAV) window.__NAV.player(p); }}>{who}</button> : who}{", " + tm}',
            '{p ? <button type="button" className="hover:underline text-left" style={{ fontWeight: "inherit" }}')
    t = lit(t, "137: assist names open player",
            '{(x.assists || []).map((a) => { const an = (a.name && a.name.default) || [((a.firstName || {}).default || ""), ((a.lastName || {}).default || "")].join(" ").trim(), ap = gxFind131(tm, null, an), at = gxTag131(s, ap); return an + (at ? " (" + at + ")" : ""); }).join(", ")}',
            '{(x.assists || []).map((a, k) => { const an = (a.name && a.name.default) || [((a.firstName || {}).default || ""), ((a.lastName || {}).default || "")].join(" ").trim(), ap = gxFind131(tm, null, an), at = gxTag131(s, ap); return <React.Fragment key={k}>{k ? ", " : ""}{ap ? <button type="button" className="hover:underline text-left" onClick={() => { if (window.__NAV) window.__NAV.player(ap); }}>{an}</button> : an}{at ? " (" + at + ")" : ""}</React.Fragment>; })}',
            'return <React.Fragment key={k}>{k ? ", " : ""}{ap ?')
    return t


edit(APP, change)
