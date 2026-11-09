# changes/215-players-list-smooth.py - Players remembers each free agent's win chance, so the list opens and scrolls without a hitch

HELPERS = r'''// ---------- change 215: win chance after each pickup worked out once per sync (install.py) ----------
const GX_WN215 = new WeakMap();
function gxWinC215(s, sP, f, d, wks) {
  let m = GX_WN215.get(s);
  if (!m) { m = new Map(); GX_WN215.set(s, m); }
  const k = [sP.wk, (wks || []).join("."), f && f.id, d ? d.id : "", Math.floor(Date.now() / 120000)].join("|");
  if (!m.has(k)) m.set(k, gxWinW196(sP, afterMove(sP, f, d), wks));
  return m.get(k);
}
'''

OLD_A = 'all.slice(0, 150).forEach((r) => { o[r.f.id] = gxWinW196(sP, afterMove(sP, r.f, r.d), ww196); });'
NEW_A = 'all.slice(0, 150).forEach((r) => { o[r.f.id] = gxWinC215(s, sP, r.f, r.d, ww196); });'
OLD_B = 'rows.forEach((r) => { o[r.f.id] = gxWinW196(sP, afterMove(sP, r.f, r.d), ww196); });'
NEW_B = 'rows.forEach((r) => { o[r.f.id] = gxWinC215(s, sP, r.f, r.d, ww196); });'

def change(t):
    t = lit(t, "215: helpers", ROOT, HELPERS + ROOT, "change 215: win chance after each pickup")
    t = lit(t, "215: sort list", OLD_A, NEW_A, "all.slice(0, 150).forEach((r) => { o[r.f.id] = gxWinC215(")
    t = lit(t, "215: shown rows", OLD_B, NEW_B, "rows.forEach((r) => { o[r.f.id] = gxWinC215(")
    return t

edit(APP, change)
