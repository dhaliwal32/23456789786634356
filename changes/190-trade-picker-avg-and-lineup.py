# changes/190-trade-picker-avg-and-lineup.py - Trades "+ Add players" sheet: adds Avg (fantasy points per game played in the chosen stats range) and renames P/G to Exp (expected points per game); every column has a fixed width so all rows line up no matter how long a name is; long names end in "..." instead of covering the next column

OLD_ROW = r'''        <span className="n pg">{f1(pg(p))}</span>'''
NEW_ROW = r'''        <span className="n pg">{gxAvg190(p, s)}</span><span className="n">{f1(pg(p))}</span>'''

OLD_HEAD = r'''<GxHB108 k="PG" l="P/G" />'''
NEW_HEAD = r'''<GxHB108 k="A190" l="Avg" /><GxHB108 k="PG" l="Exp" />'''

OLD_SORT = r'''{ PG: (p) => pg(p) }'''
NEW_SORT = r'''{ PG: (p) => pg(p), A190: (p) => { const a = parseFloat(gxAvg190(p, s)); return isNaN(a) ? -Infinity : a; } }'''

OLD_NAME = r'''<span className="min-w-0"><span className="block truncate">{p.n}</span>'''
NEW_NAME = r'''<span className="min-w-0 nm190"><span className="block truncate">{p.n}</span>'''

HELPERS = r'''// ---------- change 190: average points per game played in the chosen stats range (install.py) ----------
function gxAvg190(p, s) {
  if (!s) return "-";
  const v = gxVals106(p, s, gxRng100()), fp = parseFloat(v[0]), gp = parseFloat(v[1]);
  return !isNaN(fp) && gp > 0 ? f1(fp / gp) : "-";
}
'''

NEW_CSS = r'''  /* change 190 (install.py) */
  .gx-sim107.gx-pk189 { max-width: 1100px; }
  .gx-pk189 .hr189, .gx-pk189 .it.r189 { grid-template-columns: 250px 58px 58px repeat(11, 60px) !important; width: max-content !important; min-width: max-content; }
  .gx-pk189 .lf { overflow: hidden; }
  .gx-pk189 .lf .nm190 { flex: 1 1 auto; min-width: 0; overflow: hidden; }
  .gx-pk189 .lf .ck, .gx-pk189 .lf .gx-face, .gx-pk189 .lf img { flex: none; }
  .gx-pk189 .n { overflow: hidden; text-overflow: clip; }
  @media (max-width: 640px) {
    .gx-pk189 .hr189, .gx-pk189 .it.r189 { grid-template-columns: 172px 46px 46px repeat(11, 46px) !important; }
  }
</style>'''


def change(t):
    t = lit(t, "190: styles", "</style>", NEW_CSS, "change 190 (install.py)")
    t = lit(t, "190: helpers", ROOT, HELPERS + ROOT, "change 190: average points per game")
    t = lit(t, "190: Avg and Exp in each row", OLD_ROW, NEW_ROW, "{gxAvg190(p, s)}</span>")
    t = lit(t, "190: Avg and Exp headings", OLD_HEAD, NEW_HEAD, 'k="A190" l="Avg"')
    t = lit(t, "190: sort by Avg", OLD_SORT, NEW_SORT, "A190: (p) =>")
    t = lit(t, "190: names cut with dots", OLD_NAME, NEW_NAME, "min-w-0 nm190")
    return t


edit(APP, change)
