# changes/142-slides.py - NHL scores: everything that moves sideways slides. Laptop goal tracker slides to the next or earlier goal; in the scores sheet, Scoreboard / Goal Tracker, opening a game and going back, and the Game / Fantasy / team tabs all slide left or right

NEW_CSS = r'''  /* change 142 (install.py) */
  .gx-sh141 .bd, .gx-sd141 .bx { overflow-x: hidden; }
</style>'''


def change(t):
    t = lit(t, "142: styles", "</style>", NEW_CSS, "change 142 (install.py)")
    t = lit(t, "142: sheet slide position",
            '  const dragY = React.useRef(null);',
            '  const dragY = React.useRef(null);\n  const pos142 = gid ? 10 + ({ game: 0, fan: 1, awayTeam: 2, homeTeam: 3 }[gt] || 0) : tab === "sb" ? 0 : 1, sl142 = useSlide105(pos142);',
            'sl142 = useSlide105(pos142)')
    t = lit(t, "142: goal slide position",
            '  // ---------- laptop column ----------',
            '  const gi142 = goals.length ? (gi == null || gi >= goals.length ? goals.length - 1 : gi) : -1, slg142 = useSlide105(gi142);\n  // ---------- laptop column ----------',
            'slg142 = useSlide105(gi142)')
    t = lit(t, "142: goal slides",
            '              <div className="md">',
            '              <div key={"gi" + gi142} className={"md gx-sl105 " + slg142}>',
            'className={"md gx-sl105 " + slg142}')
    t = lit(t, "142: sheet pages slide",
            '          <div className="bd">{body}</div>',
            '          <div className="bd"><div key={"p" + pos142} className={"gx-sl105 " + sl142}>{body}</div></div>',
            'className={"gx-sl105 " + sl142}')
    return t


edit(APP, change)
