# changes/196-pickups-win-follows-weeks.py - Players list: the Win column now follows the weeks picked in Filters (it always showed this week before). One week picked: that week's chance to win after the swap, heading "Win W8". Several weeks: the average chance over those weeks, heading "Win avg". Coloured green/red against your chance for those same weeks without the move

OLD_BASE = r'''  const base = useMemo(() => planBase(s, sP), [sP]);'''
NEW_BASE = r'''  const base = useMemo(() => planBase(s, sP), [sP]);
  /* change 196: Win column follows the picked weeks */
  const ww196 = gxSelW194(sP, wm193, wks193), wk196 = ww196.join(".");
  const base196 = useMemo(() => (base == null && ww196.length === 1 && ww196[0] === sP.wk ? null : gxWinW196(sP, null, ww196)), [sP, wk196, base]);'''

OLD_W = r'''o[r.f.id] = winChance(sP, afterMove(sP, r.f, r.d));'''
NEW_W = r'''o[r.f.id] = gxWinW196(sP, afterMove(sP, r.f, r.d), ww196);'''

OLD_D1 = r'''}, [M, srt79, base]);'''
NEW_D1 = r'''}, [M, srt79, base, wk196]);'''
OLD_D2 = r'''}, [M, limit, base, srt79, wAll79]);'''
NEW_D2 = r'''}, [M, limit, base, srt79, wAll79, wk196]);'''

OLD_C = r'''<div className="n" style={w != null && base != null ? { color: w > base + 0.004 ? "var(--good)" : w < base - 0.004 ? "var(--bad)" : "var(--ink)" } : null}>'''
NEW_C = r'''<div className="n" title={base196 != null && w != null ? "Now " + wpTxt(base196) + ", after " + wpTxt(w) : ""} style={w != null && base196 != null ? { color: w > base196 + 0.004 ? "var(--good)" : w < base196 - 0.004 ? "var(--bad)" : "var(--ink)" } : null}>'''

OLD_H = r'''<GxSH k="win" cur={srt79} set={(v) => { setSrt79(v); setLimit(40); }} def="add">Win</GxSH>'''
NEW_H = r'''<GxSH k="win" cur={srt79} set={(v) => { setSrt79(v); setLimit(40); }} def="add">{ww196.length === 1 ? (ww196[0] === sP.wk ? "Win" : "Win " + gxWkShort193(sP, ww196[0]).replace("Week ", "W")) : "Win avg"}</GxSH>'''

HELPERS = r'''// ---------- change 196: chance to win over the picked weeks (install.py) ----------
// one week: that week's chance; several: the average over the weeks that have a matchup
function gxWinW196(sP, roster, wks) {
  const L = (wks && wks.length ? wks : [sP.wk]).filter((i) => oppOf(sP.weeks[i] || {}, sP.me));
  if (!L.length) return null;
  let t = 0, n = 0;
  L.forEach((i) => { let v = null; try { v = winChance(i === sP.wk ? sP : { ...sP, wk: i }, roster || undefined); } catch (e) {} if (v != null) { t += v; n++; } });
  return n ? t / n : null;
}
'''


def change(t):
    t = lit(t, "196: helpers", ROOT, HELPERS + ROOT, "change 196: chance to win over the picked weeks")
    t = lit(t, "196: base for the picked weeks", OLD_BASE, NEW_BASE, "change 196: Win column follows the picked weeks")
    t = lit(t, "196: win after the move for the picked weeks", OLD_W, NEW_W, "gxWinW196(sP, afterMove(sP, r.f, r.d), ww196)", count=2)
    t = lit(t, "196: sort list redo", OLD_D1, NEW_D1, "[M, srt79, base, wk196]")
    t = lit(t, "196: visible rows redo", OLD_D2, NEW_D2, "wAll79, wk196]")
    t = lit(t, "196: colour against the same weeks", OLD_C, NEW_C, "base196 + 0.004")
    t = lit(t, "196: heading names the weeks", OLD_H, NEW_H, '"Win avg"}</GxSH>')
    return t


edit(APP, change)
