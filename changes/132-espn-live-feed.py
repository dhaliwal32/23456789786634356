# changes/132-espn-live-feed.py - the NHL's own live feed blocks phones and browsers, so live scores, live fantasy points, the NHL scores panel and the goal tracker never filled in ("no games today"). They now read ESPN's live scoreboard and game summaries, which browsers are allowed to read. One ESPN summary per game gives the box score, power play points and goals

HELPERS = r'''// ---------- change 132: live NHL data from ESPN (install.py) ----------
// The NHL site does not let browsers read its feed, so the app's old NHL calls are answered from ESPN here, in the same shape as before.
const GX_AL132 = { LAK: "LA", NJD: "NJ", SJS: "SJ", TBL: "TB", WAS: "WSH", UTAH: "UTA", ARI: "UTA", PHX: "UTA", CLB: "CBJ", CLS: "CBJ", MON: "MTL", NAS: "NSH", WIN: "WPG", VEG: "VGK" };
const gxAb132 = (x) => GX_AL132[x] || x;
const GX_E132 = "https://site.api.espn.com/apis/site/v2/sports/hockey/nhl/";
const G132 = { sum: {}, ev: {} };
const gxEtDay132 = (iso) => { try { return new Date(iso).toLocaleDateString("en-CA", { timeZone: "America/New_York" }); } catch (e) { return String(iso || "").slice(0, 10); } };
const gxPd132 = (n) => ({ number: n || 1, periodType: n === 4 ? "OT" : n >= 5 ? "SO" : "REG" });
const gxMmss132 = (sec) => { const s = Math.max(0, Math.round(+sec || 0)); return Math.floor(s / 60) + ":" + String(s % 60).padStart(2, "0"); };
function gxNow132(js) {
  const games = [];
  ((js || {}).events || []).forEach((e) => {
    const c = ((e.competitions || [])[0]) || {}, st = c.status || e.status || {}, ty = st.type || {};
    const T = (side) => { const x = (c.competitors || []).find((q) => q.homeAway === side) || {}, tm = x.team || {}; return { id: +tm.id || tm.id, abbrev: gxAb132(tm.abbreviation), score: x.score == null || ty.state === "pre" ? undefined : +x.score, logo: tm.logo || "" }; };
    const state = ty.state === "in" ? "LIVE" : ty.state === "post" ? "FINAL" : "FUT";
    const n = st.period || 0, intm = ty.name === "STATUS_END_PERIOD" || ty.name === "STATUS_INTERMISSION" || /intermission|end of/i.test(ty.detail || "");
    const g = { id: String(e.id), gameDate: gxEtDay132(e.date), startTimeUTC: e.date, gameState: state, periodDescriptor: gxPd132(n), homeTeam: T("home"), awayTeam: T("away"),
      clock: { secondsRemaining: state === "LIVE" ? +st.clock || 0 : 1200, timeRemaining: st.displayClock || "", inIntermission: state === "LIVE" && intm } };
    G132.ev[g.id] = g;
    games.push(g);
  });
  return { games };
}
// one ESPN game summary, shared by the box score, power play and goal readers (kept 10 seconds)
function gxSum132(id) {
  const c = G132.sum[id];
  if (c && (c.p || Date.now() - c.at < 10000)) return c.p ? c.p : Promise.resolve(c.js);
  const p = fetch(GX_E132 + "summary?event=" + id).then((r) => (r.ok ? r.json() : null)).catch(() => null).then((js) => { G132.sum[id] = { js, at: Date.now() }; return js; });
  G132.sum[id] = { p, at: Date.now(), js: c && c.js };
  return p;
}
const gxHead132 = (sm) => (((sm || {}).header || {}).competitions || [])[0] || {};
function gxBox132(sm) {
  const hc = gxHead132(sm), out = { awayTeam: {}, homeTeam: {}, playerByGameStats: { awayTeam: { forwards: [], defense: [], goalies: [] }, homeTeam: { forwards: [], defense: [], goalies: [] } } };
  const side = {}, done = ((hc.status || {}).type || {}).state === "post", per = (hc.status || {}).period || 3;
  (hc.competitors || []).forEach((x) => { const k = x.homeAway === "home" ? "homeTeam" : "awayTeam", tm = x.team || {}; side[String(tm.id)] = k; out[k] = { id: +tm.id || tm.id, abbrev: gxAb132(tm.abbreviation), score: +x.score || 0, win: !!x.winner }; });
  (((sm || {}).boxscore || {}).players || []).forEach((tp) => {
    const k = side[String((tp.team || {}).id)]; if (!k) return;
    const P = out.playerByGameStats[k];
    (tp.statistics || []).forEach((grp) => {
      const L = grp.labels || [], ix = (l) => L.indexOf(l), nm = grp.name;
      if (nm !== "forwards" && nm !== "defenses" && nm !== "goalies") return;
      (grp.athletes || []).forEach((a) => {
        const s = a.stats || [], v = (l) => { const i = ix(l); return i < 0 ? null : s[i]; }, n = (l) => +(v(l) || 0) || 0, at = a.athlete || {};
        const base = { playerId: +at.id || at.id, sweaterNumber: at.jersey != null && at.jersey !== "" ? +at.jersey : null, name: { default: at.shortName || at.displayName || "" }, headshot: (at.headshot || {}).href || "", toi: v("TOI") || "" };
        if (nm === "goalies") {
          if (!base.toi || base.toi === "0:00" || base.toi === "00:00") return;
          P.goalies.push({ ...base, saves: n("SV"), shotsAgainst: n("SA"), goalsAgainst: n("GA") });
        } else {
          (nm === "forwards" ? P.forwards : P.defense).push({ ...base, goals: n("G"), assists: n("A"), plusMinus: n("+/-"), sog: n("SOG"), pim: n("PIM"), hits: n("HT"), blockedShots: n("BS"), shifts: n("SHFT"), giveaways: n("GV"), takeaways: n("TK"), faceoffWinningPctg: n("FO%") });
        }
      });
    });
  });
  // goalie decisions once the game is over: the goalie who played most for each side
  if (done) ["awayTeam", "homeTeam"].forEach((k) => {
    const G = out.playerByGameStats[k].goalies, toi = (x) => { const m = String(x.toi).split(":"); return (+m[0] || 0) * 60 + (+m[1] || 0); };
    if (!G.length) return;
    const top = G.slice().sort((a, b) => toi(b) - toi(a))[0];
    top.decision = out[k].win ? "W" : per > 3 ? "O" : "L";
  });
  return out;
}
// goals in the NHL play-by-play shape (power play and short-handed points are worked out from these)
function gxPbp132(sm) {
  const hc = gxHead132(sm), home = (hc.competitors || []).find((x) => x.homeAway === "home") || {}, hid = +((home.team || {}).id) || (home.team || {}).id;
  const plays = [];
  ((sm || {}).plays || []).forEach((e) => {
    if (!e.scoringPlay) return;
    const tid = +((e.team || {}).id) || (e.team || {}).id, st = ((e.strength || {}).abbreviation) || "", isH = tid === hid;
    const sc = st.indexOf("power") >= 0 ? "pp" : st.indexOf("short") >= 0 ? "sh" : "ev";
    const code = sc === "ev" ? "1551" : (sc === "pp") === isH ? "1451" : "1541";
    const ps = e.participants || [], sco = ps.find((p) => p.type === "scorer"), as = ps.filter((p) => p.type === "assister");
    const id = (p) => (p && p.athlete ? +p.athlete.id || p.athlete.id : null);
    plays.push({ typeDescKey: "goal", situationCode: code, details: { eventOwnerTeamId: tid, scoringPlayerId: id(sco), assist1PlayerId: id(as[0]), assist2PlayerId: id(as[1]) } });
  });
  return { homeTeam: { id: hid }, plays };
}
// goals in the NHL game summary shape, for the goal tracker
function gxLanding132(sm) {
  const hc = gxHead132(sm), ab = {};
  (hc.competitors || []).forEach((x) => { ab[String((x.team || {}).id)] = gxAb132((x.team || {}).abbreviation); });
  const by = {};
  ((sm || {}).plays || []).forEach((e) => {
    if (!e.scoringPlay) return;
    const n = (e.period || {}).number || 1, ps = e.participants || [], sco = ps.find((p) => p.type === "scorer") || {}, at = sco.athlete || {};
    const st = ((e.strength || {}).abbreviation) || "";
    (by[n] = by[n] || { periodDescriptor: gxPd132(n), goals: [] }).goals.push({
      name: { default: at.displayName || "" }, teamAbbrev: { default: ab[String((e.team || {}).id)] || "" }, headshot: (at.headshot || {}).href || "",
      timeInPeriod: (e.clock || {}).displayValue || "", awayScore: e.awayScore, homeScore: e.homeScore, strength: st.indexOf("power") >= 0 ? "PP" : st.indexOf("short") >= 0 ? "SH" : "",
      assists: ps.filter((p) => p.type === "assister").map((p) => ({ name: { default: (p.athlete || {}).displayName || "" } })) });
  });
  return { summary: { scoring: Object.keys(by).sort((a, b) => a - b).map((k) => by[k]) } };
}
(function () {
  if (window.__GXF132) return;
  const nf = window.fetch.bind(window);
  window.__GXF132 = nf;
  const ok = (obj) => (obj ? { ok: true, status: 200, json: () => Promise.resolve(obj) } : { ok: false, status: 502, json: () => Promise.resolve(null) });
  window.fetch = function (u, o) {
    const s = typeof u === "string" ? u : (u && u.url) || "";
    if (s.indexOf("https://api-web.nhle.com/v1/") !== 0) return nf(u, o);
    const path = s.slice(28).split("?")[0];
    if (path === "score/now") return nf(GX_E132 + "scoreboard").then((r) => (r.ok ? r.json() : null)).then((js) => ok(js ? gxNow132(js) : null)).catch(() => ok(null));
    const m = path.match(/^gamecenter\/([^/]+)\/(boxscore|play-by-play|landing)$/);
    if (!m) return nf(u, o);
    return gxSum132(m[1]).then((sm) => ok(sm ? (m[2] === "boxscore" ? gxBox132(sm) : m[2] === "play-by-play" ? gxPbp132(sm) : gxLanding132(sm)) : null));
  };
})();
'''


def change(t):
    t = lit(t, "132: read live NHL data from ESPN", ROOT, HELPERS + ROOT, "change 132: live NHL data from ESPN")
    return t


edit(APP, change)
