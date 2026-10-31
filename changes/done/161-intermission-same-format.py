# changes/161-intermission-same-format.py - intermission clock in the same format as the game clock: "1st INT - 1:05" on the scoreboards like "2nd - 17:43", "1st INT 1:05" on Matchup rows like "2nd 17:43", always on one line

NEW_CSS = r'''  /* change 161 (install.py) */
  .gx-gc140 .st { width: 124px; white-space: nowrap; }
  .gx-sd141 .gm .st { width: 100px; white-space: nowrap; letter-spacing: -0.2px; }
</style>'''

def change(t):
    t = lit(t, "161: styles", "</style>", NEW_CSS, "change 161 (install.py)")
    t = lit(t, "161: scoreboard format",
            'return per + " INT" + (left ? " " + gxIntFmt159(left) : "");',
            'return per + " INT" + (left ? " - " + gxMmss132(left) : ""); /* gx161 */',
            '" - " + gxMmss132(left) : ""); /* gx161 */')
    t = lit(t, "161: row format",
            'return g ? gxIntG159(g) : per + " INT";',
            'const L161 = g ? gxIntLeft159(g) : null; return per + " INT" + (L161 ? " " + gxMmss132(L161) : ""); /* gx161 */',
            "const L161 = g ? gxIntLeft159(g) : null;")
    return t

edit(APP, change)
