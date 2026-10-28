# changes/098-phone-matchup-espn.py - phone player photo lines up with Status; finished players faded in Matchup; phone Matchup in ESPN's layout (no face: name and team logo, opponent and score, stat line)

NEW_CSS = r'''  /* change 098 (install.py) */
  .gx-h2h .gx-fin { opacity: .5; }
  .gx-tl98 { display: none; }
  .gx-sl98 { display: none; }
  @media (max-width: 640px) {
    .gx-pd-ph { width: 138px; height: 100%; aspect-ratio: auto; align-self: stretch; }
    .gx-pd-hd { grid-template-columns: 138px 1fr; }
    .gx-h2h .gx-fw { display: none !important; }
    .gx-h2h .gx-tl98 { display: inline-block; vertical-align: -2px; margin: 0 4px; }
    .gx-h2h .gx-tl98 img { width: 15px !important; height: 15px !important; }
    .gx-h2h .gx-sl98 { display: block; font-size: 11px; color: var(--mute); line-height: 1.3; white-space: normal; }
    .gx-h2h .gx-st98 { display: none; }
    .gx-h2h { align-items: start; }
  }
</style>'''

OLD_FACE = '<div className="min-w-0 gx-pc" style={{ flexDirection: right ? "row-reverse" : "row" }}><GxFace p={p} size={30} />'
NEW_FACE = '<div className={"min-w-0 gx-pc" + (p.st === "F" ? " gx-fin" : "")} style={{ flexDirection: right ? "row-reverse" : "row" }}><span className="gx-fw" style={{ display: "inline-flex" }}><GxFace p={p} size={30} /></span>'

OLD_NAME = '<span className="m-hide">{p.n}</span><span className="m-inl">{shortN(p.n)}</span></button></div>'
NEW_NAME = ('<span className="m-hide">{p.n}</span><span className="m-inl">{shortN(p.n)}</span></button>'
            '<span className="gx-tl98"><TeamLogo t={p.t} size={15} /></span></div>')

OLD_LINE = '<div className="text-xs text-slate-500 truncate">{p.st ? <><LiveTag st={p.st} t={p.t} dt={p.dt} />{line ? " " + line : ""}</> : <>{mGame(p)}{st ? " \\u00b7 " + st.toLowerCase() : ""}</>}</div></div>'
NEW_LINE = ('<div className="text-xs text-slate-500 truncate">{p.st ? <>{gxOpp98(p)}<LiveTag st={p.st} t={p.t} dt={p.dt} />'
            '{p.st === "F" ? <span className="m-inl"> Final</span> : null}<span className="gx-st98">{line ? " " + line : ""}</span></> : <>{mGame(p)}{st ? " \\u00b7 " + st.toLowerCase() : ""}</>}</div>'
            '{p.st && line ? <div className="gx-sl98">{line}</div> : null}</div>')

HELPERS = r'''// ---------- change 098: phone Matchup in ESPN's layout (install.py) ----------
// opponent before the score on the phone, e.g. "@WPG"
function gxOpp98(p) {
  const g = gameOf(p.t, p.dt);
  return g ? <span className="m-inl">{(g.h ? "" : "@") + g.o + " "}</span> : null;
}
'''


def change(t):
    t = lit(t, "098: styles", "</style>", NEW_CSS, "change 098 (install.py)")
    t = lit(t, "098: helpers", ROOT, HELPERS + ROOT, "change 098: phone Matchup in ESPN's layout")
    t = lit(t, "098: fade finished, face laptop only", OLD_FACE, NEW_FACE, '(p.st === "F" ? " gx-fin" : "")')
    t = lit(t, "098: team logo after name", OLD_NAME, NEW_NAME, '<span className="gx-tl98">')
    t = lit(t, "098: opponent and stat line", OLD_LINE, NEW_LINE, '<div className="gx-sl98">{line}</div>')
    return t


edit(APP, change)
