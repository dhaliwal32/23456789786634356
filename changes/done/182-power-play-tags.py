# changes/182-power-play-tags.py - Live power play / penalty kill tags: on Matchup player rows ("PP 1:24" / "PK 1:24", stronger for that team's PP1 / PK1 players) and on the NHL Scores game cards ("PHI PP 1:24"), worked out from the penalties in ESPN's live game feed

NEW_CSS = r'''  /* change 182 (install.py) */
  .gx-pp182 { display: inline-block; margin-right: 6px; padding: 0 5px; border-radius: 4px; font-size: 10.5px; line-height: 15px; font-weight: 600; color: var(--mute); box-shadow: inset 0 0 0 1px var(--line2); font-variant-numeric: tabular-nums; vertical-align: 1px; }
  .gx-pp182.on.pp { background: var(--warn); color: #111; box-shadow: none; }
  .gx-pp182.on.pk { color: var(--warn); box-shadow: inset 0 0 0 1px var(--warn); }
  .gx-ppg182 { display: block; font-size: 12px; font-weight: 600; color: var(--warn); white-space: nowrap; font-variant-numeric: tabular-nums; }
</style>'''

HELPERS = r'''// ---------- change 182: live power plays from the penalties in ESPN's game feed (install.py) ----------
const GX_PPW182 = new WeakMap();
function gxPen182(sm) {
  if (!sm || typeof sm !== "object") return null;
  if (GX_PPW182.has(sm)) return GX_PPW182.get(sm);
  const hc = gxHead132(sm), ab = {};
  (hc.competitors || []).forEach((x) => { ab[String((x.team || {}).id)] = gxAb131(gxAb132((x.team || {}).abbreviation)); });
  const sec = (e) => { const n = (e.period || {}).number || 1, m = String((e.clock || {}).displayValue || "0:0").split(":"); return (n - 1) * 1200 + (+m[0] || 0) * 60 + (+m[1] || 0); };
  const pens = [], goals = [];
  ((sm || {}).plays || []).forEach((e) => {
    const ty = String((e.type || {}).text || ""), tx = String(e.text || ""), tm = ab[String((e.team || {}).id)];
    if (!tm || ((e.period || {}).number || 1) >= 5) return;
    if (e.scoringPlay) { goals.push({ t: tm, at: sec(e) }); return; }
    if (!/penalt/i.test(ty) || /penalty shot/i.test(ty + " " + tx)) return;
    let m = +e.penaltyMinutes || +((e.penalty || {}).minutes) || 0;
    if (!m) { const r = tx.match(/(\d+)\s*(?:min|minutes)\b/i) || tx.match(/\((\d+)\)/); m = r ? +r[1] : /major|fighting/i.test(tx) ? 5 : 2; }
    if (m >= 10 || (/misconduct/i.test(ty + " " + tx) && m !== 2 && m !== 4 && m !== 5)) return;
    const at = sec(e);
    pens.push({ t: tm, at, m, end: at + m * 60 });
  });
  // penalties to both teams at the same moment with the same length cancel out
  pens.forEach((p) => { if (p.x) return; const q = pens.find((q) => !q.x && q !== p && q.t !== p.t && q.at === p.at && q.m === p.m); if (q) { p.x = 1; q.x = 1; } });
  const live = pens.filter((p) => !p.x);
  // a power play goal ends the short team's first minor (or half of a double minor)
  goals.sort((a, b) => a.at - b.at).forEach((gl) => {
    const on = (f) => live.filter((p) => f(p.t) && p.at <= gl.at && gl.at < p.end);
    const opp = on((t) => t !== gl.t), mine = on((t) => t === gl.t);
    if (opp.length <= mine.length) return;
    const mn = opp.filter((p) => p.m === 2 || p.m === 4).sort((a, b) => a.end - b.end)[0];
    if (!mn) return;
    mn.end = mn.m === 4 && mn.end - gl.at > 120 ? gl.at + 120 : gl.at;
  });
  GX_PPW182.set(sm, live);
  return live;
}
// { pp: team on the power play, sh: team short, left: seconds } for a live scoreboard game, or null
function gxPPNow182(g) {
  try {
    if (!g || g.gameState !== "LIVE" || (g.clock || {}).inIntermission) return null;
    const c = G132.sum[g.id], L = gxPen182(c && c.js);
    if (!L || !L.length) return null;
    const n = (g.periodDescriptor || {}).number || 1;
    if (n >= 5) return null;
    const m = String((g.clock || {}).timeRemaining || "").split(":");
    if (m.length < 2) return null;
    const now = (n - 1) * 1200 + (n <= 3 ? 1200 : 300) - ((+m[0] || 0) * 60 + (+m[1] || 0));
    const A = gxAb131((g.awayTeam || {}).abbrev), H = gxAb131((g.homeTeam || {}).abbrev);
    const act = (t) => L.filter((p) => p.t === t && p.at <= now && now < p.end);
    const a = Math.min(2, act(A).length), h = Math.min(2, act(H).length);
    if (a === h) return null;
    const sh = a > h ? A : H, pp = a > h ? H : A;
    return { pp, sh, left: Math.max(0, Math.min(...act(sh).map((p) => p.end)) - now) };
  } catch (e) { return null; }
}
function gxPPTeam182(t) {
  const g = Object.values(G132.ev || {}).find((x) => x && x.gameState === "LIVE" && (gxAb131((x.homeTeam || {}).abbrev) === t || gxAb131((x.awayTeam || {}).abbrev) === t));
  return g ? gxPPNow182(g) : null;
}
// Matchup row tag; stronger for that team's PP1 (power play) or PK1 (penalty kill) players
function GxPP182({ t, n, st }) {
  if (st !== "L" || !t) return null;
  const r = gxPPTeam182(t);
  if (!r) return null;
  const isPP = r.pp === t, ln = ((((window.LINES_DATA || {}).teams || {})[t] || {}).lines) || {};
  const on = (ln[isPP ? "PP1" : "PK1"] || []).some((x) => nrm(x) === nrm(n || ""));
  return <span className={"gx-pp182 " + (isPP ? "pp" : "pk") + (on ? " on" : "")} data-gx="182">{(isPP ? "PP " : "PK ") + gxMmss132(r.left)}</span>;
}
// NHL Scores game card line, e.g. "PHI PP 1:24"
function GxPPg182({ g }) {
  const r = gxPPNow182(g);
  return r ? <span className="gx-ppg182">{r.pp + " PP " + gxMmss132(r.left)}</span> : null;
}
'''

ROW_OLD = r'''{p.st ? <>{gxOpp98(p)}<LiveTag st={p.st} t={p.t} dt={p.dt} e157 />{null /* gx152 */}'''
ROW_NEW = r'''{p.st ? <><GxPP182 t={p.t} n={p.n} st={p.st} />{gxOpp98(p)}<LiveTag st={p.st} t={p.t} dt={p.dt} e157 />{null /* gx152 */}'''

PH_OLD = r'''<span>{status(g)}</span>{live(g) ? <a className="wt179"'''
PH_NEW = r'''<span>{status(g)}</span><GxPPg182 g={g} />{live(g) ? <a className="wt179"'''

LP_OLD = r'''<span>{status(g)}</span>{live(g) ? <a className="wt181"'''
LP_NEW = r'''<span>{status(g)}</span><GxPPg182 g={g} />{live(g) ? <a className="wt181"'''


def change(t):
    t = lit(t, "182: styles", "</style>", NEW_CSS, "change 182 (install.py)")
    t = lit(t, "182: helpers", ROOT, HELPERS + ROOT, "change 182: live power plays")
    t = lit(t, "182: Matchup rows", ROW_OLD, ROW_NEW, "<GxPP182 t={p.t}")
    t = lit(t, "182: phone game cards", PH_OLD, PH_NEW, '<GxPPg182 g={g} />{live(g) ? <a className="wt179"')
    t = lit(t, "182: laptop game cards", LP_OLD, LP_NEW, '<GxPPg182 g={g} />{live(g) ? <a className="wt181"')
    return t


edit(APP, change)
