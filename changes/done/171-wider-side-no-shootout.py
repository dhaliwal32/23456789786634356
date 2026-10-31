# changes/171-wider-side-no-shootout.py - laptop: the right column (Goal Tracker, NHL Scoreboard) is wider so nothing wraps, assists stay on one line; shootout goals no longer show in the Goal Tracker or get replays

NEW_CSS = r'''  /* change 171 (install.py) */
  @media (min-width: 1300px) {
    .gx-mu141 { grid-template-columns: minmax(0, 1fr) 450px; gap: 22px; }
  }
  .gx-sd141 .gs .asl { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .gx-sd141 .gs .tp .min-w-0 > div { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
</style>'''

def change(t):
    t = lit(t, "171: styles", "</style>", NEW_CSS, "change 171 (install.py)")
    t = lit(t, "171: no shootout goals",
            '    const st = ((e.strength || {}).abbreviation) || "";\n    (by[n] = by[n] || { periodDescriptor: gxPd132(n), goals: [] }).goals.push({',
            '    if (n >= 5 || /shootout/i.test(String((e.type || {}).text || "") + " " + String(((e.period || {}).displayValue) || ""))) return; /* gx171: shootout goals do not count */\n    const st = ((e.strength || {}).abbreviation) || "";\n    (by[n] = by[n] || { periodDescriptor: gxPd132(n), goals: [] }).goals.push({',
            "gx171: shootout goals do not count")
    return t


def edge(t):
    return lit(t, "171: no shootout replays",
               '            if p.get("typeDescKey") != "goal" or not p.get("pptReplayUrl"):',
               '            if p.get("typeDescKey") != "goal" or not p.get("pptReplayUrl") or (p.get("periodDescriptor") or {}).get("periodType") == "SO":  # change 171',
               "# change 171")


edit(APP, change)
edit("gm_edge.py", edge)
