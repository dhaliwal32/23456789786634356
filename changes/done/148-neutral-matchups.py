# changes/148-neutral-matchups.py - other teams' matchups use plain colours: no green or red for the margin, day +/- , day total or win ring, and the NHL scores mark the two teams in white and grey instead of green and blue (your own matchup keeps its colours)

NEW_CSS = r'''  /* change 148 (install.py) */
  .gx-nc148 .gx-gt141 .cd.me { border-left-color: var(--ink); }
  .gx-nc148 .gx-gt141 .cd.op { border-left-color: var(--mute); }
  .gx-nc148 .gx-bt141 .t > div.n.me { box-shadow: inset 4px 0 0 var(--ink); }
  .gx-nc148 .gx-bt141 .t > div.n.op { box-shadow: inset 4px 0 0 var(--mute); }
  .gx-nc148 .gx-lg141 .me, .gx-nc148 .gx-lg141 .op, .gx-nc148.gx-sd141 .lg .me, .gx-nc148.gx-sd141 .lg .op { color: var(--ink); }
  .gx-nc148 i.me { background: var(--ink) !important; }
  .gx-nc148 i.op { background: var(--mute) !important; }
</style>'''


def change(t):
    t = lit(t, "148: styles", "</style>", NEW_CSS, "change 148 (install.py)")
    t = lit(t, "148: margin line",
            'color: margin >= 0 ? "var(--good)" : "var(--bad)"',
            'color: !mine ? "var(--ink2, var(--ink))" : margin >= 0 ? "var(--good)" : "var(--bad)"',
            'color: !mine ? "var(--ink2, var(--ink))" : margin >= 0')
    t = lit(t, "148: day +/-",
            'color: Math.abs(dvD135) < 0.05 ? "var(--mute)" : dvD135 > 0 ? "var(--good)" : "var(--bad)"',
            'color: !mine || Math.abs(dvD135) < 0.05 ? "var(--mute)" : dvD135 > 0 ? "var(--good)" : "var(--bad)"',
            'color: !mine || Math.abs(dvD135) < 0.05')
    t = lit(t, "148: day total",
            'color: Math.abs(dayTot) < 0.05 ? "var(--mute)" : dayTot > 0 ? "var(--good)" : "var(--bad)"',
            'color: !mine || Math.abs(dayTot) < 0.05 ? "var(--mute)" : dayTot > 0 ? "var(--good)" : "var(--bad)"',
            'color: !mine || Math.abs(dayTot) < 0.05')
    t = lit(t, "148: plain ring", "const GxRing = ({ v, big }) => {", "const GxRing = ({ v, big, plain }) => {", "const GxRing = ({ v, big, plain }) => {")
    t = lit(t, "148: plain ring colour",
            '  const col = v == null ? "var(--faint)" : v >= 0.5 ? "var(--good)" : "var(--bad)";',
            '  const col = v == null ? "var(--faint)" : plain ? "var(--ink2, var(--ink))" : v >= 0.5 ? "var(--good)" : "var(--bad)";',
            'plain ? "var(--ink2, var(--ink))"')
    t = lit(t, "148: Matchup ring", "<GxRing v={winProb(A, B, aA, aB)} />", "<GxRing v={winProb(A, B, aA, aB)} plain={!mine} />", "plain={!mine} />")
    t = lit(t, "148: scores column plain", '<div className="gx-sd141">', '<div className={"gx-sd141" + (a !== s.me ? " gx-nc148" : "")}>', '(a !== s.me ? " gx-nc148" : "")}>')
    t = lit(t, "148: scores sheet plain",
            'ref={sh143} className={"gx-sh141" + (out ? " out" : "") + (drag143 ? " dg" : "")}',
            'ref={sh143} className={"gx-sh141" + (out ? " out" : "") + (drag143 ? " dg" : "") + (a !== s.me ? " gx-nc148" : "")}',
            '(drag143 ? " dg" : "") + (a !== s.me ? " gx-nc148" : "")}')
    return t


edit(APP, change)
