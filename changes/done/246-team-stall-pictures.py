# changes/246-team-stall-pictures.py - Lines and My team: each stall uses Kuvar's own picture of that team's locker stall (stalls/TEAM.jpg), name on the plaque, jersey on the hanger

NEW_CSS = r'''  /* change 246 (install.py): team stall pictures */
  .gx-fg224.gx-lt227.st246 { container-type: inline-size; position: relative; overflow: hidden; justify-content: flex-start; padding: 100% 3px 7px !important; border-radius: 6px !important;
    background: #0c0c0e var(--st) center top / 100% auto no-repeat !important; box-shadow: 0 4px 10px rgba(0,0,0,.45) !important; }
  .gx-fg224.gx-lt227.st246::before { display: none !important; }
  .gx-fg224.gx-lt227.st246:not(.fa)::after { display: none !important; }
  .gx-fg224.gx-lt227.st246.fa::after { bottom: auto !important; height: 100cqw; }
  .gx-fg224.gx-lt227.st246 > .md.jr231 { position: absolute !important; left: 0; top: 0; width: 100% !important; max-width: none !important; height: 100cqw !important; aspect-ratio: auto !important; margin: 0 !important; z-index: 1; overflow: visible; }
  .gx-fg224.gx-lt227.st246 .md.jr231 .pl232 { position: absolute; left: 50%; top: 19.5cqw; transform: translate(-50%, -50%); max-width: 44cqw; margin: 0; padding: .6cqw 1.4cqw; font-size: clamp(6.5px, 2.9cqw, 12px); letter-spacing: .06em; border-radius: 2px;
    color: #17171a; background: linear-gradient(180deg, #eeebe4, #bdb8ad); box-shadow: 0 1px 2px rgba(0,0,0,.6), 0 0 0 1px rgba(0,0,0,.25); }
  .gx-fg224.gx-lt227.st246 .md.jr231 svg { position: absolute; left: 29cqw; top: 26cqw; width: 42cqw !important; height: auto !important; aspect-ratio: 120 / 140; filter: drop-shadow(0 1.5cqw 2cqw rgba(0,0,0,.55)); }
  .gx-fg224.gx-lt227.st246 .sb227 { margin-top: 6px; }
  .gx-fg224.gx-lt227.st246 .sb227, .gx-fg224.gx-lt227.st246 .ow227, html[data-theme="light"] .gx-fg224.gx-lt227.st246 .sb227, html[data-theme="light"] .gx-fg224.gx-lt227.st246 .ow227 { color: rgba(255,255,255,.74) !important; }
  .gx-fg224.gx-lt227.st246 .ow227 b, html[data-theme="light"] .gx-fg224.gx-lt227.st246 .ow227 b { color: #fff !important; }
  .gx-fg224.gx-lt227.st246.fa .ow227 span:first-child { color: #7fe0a3 !important; }
</style>'''

HELPERS = r'''// ---------- change 246: Kuvar's team stall pictures (install.py) ----------
const GX_ST246 = new Set(["ANA", "BOS", "BUF", "CAR", "CBJ", "CGY", "CHI", "COL", "DAL", "DET", "EDM", "FLA", "LA", "MIN", "MTL", "NJ", "NSH", "NYI", "NYR", "OTT", "PHI", "PIT", "SEA", "SJ", "STL", "TB", "TOR", "UTA", "VAN", "VGK", "WPG", "WSH"]);
const gxSt246c = (t) => (GX_ST246.has(String(t || "").toUpperCase()) ? " st246" : "");
const gxSt246s = (t) => { const T = String(t || "").toUpperCase(); return GX_ST246.has(T) ? { "--st": "url(stalls/" + T + ".jpg?v=1)" } : undefined; };
'''

def change(t):
    t = lit(t, "246: styles", "</style>", NEW_CSS, "change 246 (install.py)")
    t = lit(t, "246: helpers", ROOT, HELPERS + ROOT, "change 246: Kuvar's team stall pictures")
    t = lit(t, "246: Lines stalls",
            '''className={"gx-fg224 gx-lt227" + (mine ? " me" : fa ? " fa" : "")} aria-label={n}''',
            '''className={"gx-fg224 gx-lt227" + (mine ? " me" : fa ? " fa" : "") + gxSt246c(t)} style={gxSt246s(t)} aria-label={n}''',
            "gxSt246c(t)} style={gxSt246s(t)}")
    t = lit(t, "246: My team stalls",
            '''className={"gx-fg224 gx-lt227 " + tn.k} aria-label={p.n}''',
            '''className={"gx-fg224 gx-lt227 " + tn.k + gxSt246c(p.t)} style={gxSt246s(p.t)} aria-label={p.n}''',
            "gxSt246c(p.t)} style={gxSt246s(p.t)}")
    return t

edit(APP, change)
