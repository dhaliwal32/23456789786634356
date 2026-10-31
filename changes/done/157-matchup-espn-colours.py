# changes/157-matchup-espn-colours.py - Matchup like the ESPN app: points white once a player's game has started (live or over), grey dash before; finished games say "5-2 Final" (no W/L) and are no longer faded

NEW_CSS = r'''  /* change 157 (install.py) */
  .gx-h2h .gx-on157[data-gx="138pts"] { color: var(--ink) !important; }
  .gx-h2h.gx-tt147.gx-on157 > div:nth-child(2), .gx-h2h.gx-tt147.gx-on157 > div:nth-child(4) { color: var(--ink) !important; }
  .gx-h2h .gx-fin, .gx-h2h > .gx-fin + div, .gx-h2h > div:has(+ .gx-fin) { opacity: 1 !important; }
</style>'''

def change(t):
    t = lit(t, "157: styles", "</style>", NEW_CSS, "change 157 (install.py)")
    t = lit(t, "157: LiveTag option", "const LiveTag = ({ st, t, dt }) => {", "const LiveTag = ({ st, t, dt, e157 }) => {", "dt, e157 }) => {")
    t = lit(t, "157: no W/L", '{res ? res + " " : ""}{sc.my}', '{res && !e157 ? res + " " : ""}{sc.my}', "res && !e157 ?")
    t = lit(t, "157: Final word",
            '<span className="font-normal text-slate-500">{tail}</span>',
            '<span className="font-normal text-slate-500">{tail}{e157 && st === "F" ? " Final" : ""}</span>',
            'e157 && st === "F" ? " Final"')
    t = lit(t, "157: matchup uses it", "<LiveTag st={p.st} t={p.t} dt={p.dt} />", "<LiveTag st={p.st} t={p.t} dt={p.dt} e157 />", "dt={p.dt} e157 />")
    t = lit(t, "157: white when started",
            '<div className={right ? "" : "text-right"} style={null} data-gx="138pts">',
            '<div className={(right ? "" : "text-right") + (p.st ? " gx-on157" : "")} style={null} data-gx="138pts">',
            '(p.st ? " gx-on157" : "")')
    t = lit(t, "157: day total white once games start",
            '{rows.length ? <div className="gx-h2h gx-tt114 gx-tt147">',
            '{rows.length ? <div className={"gx-h2h gx-tt114 gx-tt147" + (state !== "projected" ? " gx-on157" : "")}>',
            '"gx-h2h gx-tt114 gx-tt147" + (state !== "projected"')
    return t

edit(APP, change)
