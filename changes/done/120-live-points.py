# changes/120-live-points.py - live fantasy points during games: while the app is open it reads the NHL's live box scores every 15 seconds and works out everyone's points with your league's scoring (power play points from the NHL's goal log); ESPN's numbers take over once the sync confirms them. Also adds gm_live.py (lead-change alerts from GitHub while the app is closed) and removes the Ask button

GM_LIVE = r'''"""
gm_live.py - watches your matchup during NHL games and buzzes your phone (ntfy) when the lead changes.

Runs on GitHub (live-alerts.yml). It checks ESPN's live matchup score about every 30 seconds while
games are on, and stops by itself when no game is live and none starts in the next 75 minutes.
"""
import json
import os
import re
import sys
import time
from datetime import datetime, timezone

import requests

LEAGUE_ID = 1363781006
SEASON = 2027
MY_TEAM_ID = 4
ESPN_S2 = os.environ.get("ESPN_S2", "").strip()
SWID = os.environ.get("SWID", "").strip()
NTFY_TOPIC = os.environ.get("NTFY_TOPIC", "").strip()
APP_URL = "https://dhaliwal32.github.io/23456789786634356/fantasy-gm.html#matchup"
LEAGUE = f"https://lm-api-reads.fantasy.espn.com/apis/v3/games/fhl/seasons/{SEASON}/segments/0/leagues/{LEAGUE_ID}"
HERE = os.path.dirname(os.path.abspath(__file__))
EVERY = 30          # seconds between checks while games are on
MAX_RUN = 5.6 * 3600  # GitHub stops a job after 6 hours

s = requests.Session()
s.headers.update({"User-Agent": "Mozilla/5.0"})
s.cookies.update({"espn_s2": ESPN_S2, "SWID": SWID})


def log(*a):
    print(datetime.now(timezone.utc).strftime("%H:%M:%S"), *a, flush=True)


def push(title, msg):
    if not NTFY_TOPIC:
        log("(no ntfy topic)", title, msg)
        return
    try:
        requests.post(f"https://ntfy.sh/{NTFY_TOPIC}", data=msg.encode("utf-8"),
                      headers={"Title": title, "Priority": "high", "Tags": "ice_hockey", "Click": APP_URL}, timeout=20)
    except Exception as e:
        log("ntfy failed", e)


def games_now():
    """(any game live, minutes until the next one starts or None)"""
    js = requests.get("https://api-web.nhle.com/v1/score/now", timeout=20).json()
    now = datetime.now(timezone.utc)
    live, nxt = False, None
    for g in js.get("games", []):
        st = g.get("gameState")
        if st in ("LIVE", "CRIT"):
            live = True
        elif st in ("FUT", "PRE") and g.get("startTimeUTC"):
            t = datetime.fromisoformat(g["startTimeUTC"].replace("Z", "+00:00"))
            m = (t - now).total_seconds() / 60
            if m > -30 and (nxt is None or m < nxt):
                nxt = m
    return live, nxt


def my_id():
    try:
        txt = open(os.path.join(HERE, "espn-data.js"), encoding="utf-8").read()
        m = re.search(r'"myTeamId":\s*(\d+)', txt)
        return int(m.group(1)) if m else MY_TEAM_ID
    except Exception:
        return MY_TEAM_ID


def names():
    try:
        r = s.get(LEAGUE, params=[("view", "mTeam")], timeout=30).json()
        return {t["id"]: (t.get("name") or f"Team {t['id']}").strip() for t in r.get("teams", [])}
    except Exception:
        return {}


def score(me):
    r = s.get(LEAGUE, params=[("view", "mMatchupScore"), ("view", "mStatus")], timeout=30)
    r.raise_for_status()
    js = r.json()
    cur = (js.get("status") or {}).get("currentMatchupPeriod")
    for m in js.get("schedule", []):
        if m.get("matchupPeriodId") != cur:
            continue
        h, a = m.get("home") or {}, m.get("away") or {}
        pts = lambda x: x.get("totalPointsLive", x.get("totalPoints")) or 0
        if h.get("teamId") == me:
            return pts(h), pts(a), a.get("teamId")
        if a.get("teamId") == me:
            return pts(a), pts(h), h.get("teamId")
    return None


def main():
    if not ESPN_S2 or not SWID:
        sys.exit("ESPN_S2 and SWID are missing")
    start, me, nm, last, quiet = time.time(), my_id(), names(), None, 0
    while time.time() - start < MAX_RUN:
        try:
            live, nxt = games_now()
        except Exception as e:
            log("NHL check failed", e)
            live, nxt = True, None
        if not live:
            if nxt is None or nxt > 75:
                log("no game live and none soon - stopping")
                return
            time.sleep(min(300, max(30, (nxt - 2) * 60)))
            continue
        try:
            sc = score(me)
        except Exception as e:
            log("ESPN check failed", e)
            sc = None
        if sc:
            a, b, opp = sc
            d = round(a - b, 1)
            side = 1 if d > 0 else -1 if d < 0 else 0
            them = nm.get(opp, "Your opponent")
            if last is None:
                log(f"start: {a:.1f} to {b:.1f}")
                last = side
            elif side != 0 and side != last:
                if side > 0:
                    push("You took the lead", f"{a:.1f} to {b:.1f} vs {them}")
                else:
                    push(f"{them} took the lead", f"{b:.1f} to {a:.1f}. You trail by {abs(d):.1f}")
                log("lead change", a, b)
                last = side
            elif side != 0:
                last = side
        time.sleep(EVERY)


if __name__ == "__main__":
    main()
'''

HELPERS = r'''// ---------- change 120: live fantasy points from the NHL's box scores (install.py) ----------
const G120 = { box: {}, pp: {}, goals: {}, fin: {}, busy: false };
const GX_AL120 = { LAK: "LA", NJD: "NJ", SJS: "SJ", TBL: "TB", UTAH: "UTA", ARI: "UTA" };
const gxSc120 = () => Object.assign({}, typeof SC0 === "object" ? SC0 : {}, window.__SC120 || {});
function gxPP120(pb) {
  const hid = (pb.homeTeam || {}).id, out = {};
  (pb.plays || []).forEach((e) => {
    if (e.typeDescKey !== "goal") return;
    const d = e.details || {}, c = String(e.situationCode || "");
    if (c.length !== 4) return;
    const ag = +c[0], as = +c[1], hs = +c[2], hg = +c[3], home = d.eventOwnerTeamId === hid;
    const my = home ? hs : as, op = home ? as : hs, myG = home ? hg : ag, opG = home ? ag : hg;
    const pp = my > op && (myG === 1 || my - op >= 2), sh = my < op && (opG === 1 || op - my >= 2);
    if (!pp && !sh) return;
    [d.scoringPlayerId, d.assist1PlayerId, d.assist2PlayerId].forEach((id) => { if (!id) return; const o = (out[id] = out[id] || { ppp: 0, shp: 0 }); if (pp) o.ppp++; else o.shp++; });
  });
  return out;
}
function gxFp120(x) {
  const sc = gxSc120(), w = (k) => +sc[k] || 0;
  if (x.sv != null) return (x.dec === "W" ? w("W") : 0) + (x.dec === "O" ? w("OTL") : 0) + x.sv * w("SV") + x.ga * w("GA") + (x.dec === "W" && x.ga === 0 ? w("SO") : 0);
  return x.g * w("G") + x.a * w("A") + x.pm * w("PM") + x.sog * w("SOG") + x.hit * w("HIT") + x.blk * w("BLK") + x.ppp * w("PPP") + x.shp * w("SHP") + x.pim * w("PIM");
}
function gxRebuild120() {
  const out = {};
  Object.entries(G120.box).forEach(([gid, B]) => {
    const bx = B.bx || {}, pbg = bx.playerByGameStats || {}, pp = G120.pp[gid] || {}, D = (out[B.d] = out[B.d] || {});
    ["awayTeam", "homeTeam"].forEach((k) => {
      const T = bx[k] || {}, ab = GX_AL120[T.abbrev] || T.abbrev, P = pbg[k] || {};
      const put = (pl, x) => {
        x.fp = Math.round(gxFp120(x) * 100) / 100; x.fin = B.fin || 0; x.gs = B.start || "";
        if (pl.sweaterNumber != null) D[ab + "#" + pl.sweaterNumber] = x;
        const nm = String((pl.name || {}).default || ""), i = nm.indexOf(". "), ln = nrm(i > 0 ? nm.slice(i + 2) : nm.split(" ").slice(1).join(" "));
        if (ln) D[ab + ":" + nrm(nm).charAt(0) + ":" + ln] = x;
      };
      [...(P.forwards || []), ...(P.defense || [])].forEach((pl) => { const q = pp[pl.playerId] || {};
        put(pl, { g: pl.goals || 0, a: pl.assists || 0, pm: pl.plusMinus || 0, sog: (pl.sog != null ? pl.sog : pl.shots) || 0, pim: pl.pim || 0, hit: pl.hits || 0, blk: (pl.blockedShots != null ? pl.blockedShots : pl.blocked) || 0, ppg: pl.powerPlayGoals || 0, ppp: q.ppp || 0, shp: q.shp || 0, toi: pl.toi || "", fo: pl.faceoffWinningPctg || 0, shf: pl.shifts || 0, gv: pl.giveaways || 0, tk: pl.takeaways || 0 }); });
      (P.goalies || []).forEach((pl) => {
        if (!pl.toi || pl.toi === "00:00") return;
        let sv = pl.saves, sa = pl.shotsAgainst;
        if (sv == null && pl.saveShotsAgainst) { const m = String(pl.saveShotsAgainst).split("/"); sv = +m[0]; sa = +m[1]; }
        put(pl, { sv: sv || 0, ga: pl.goalsAgainst || 0, sa: sa || 0, dec: pl.decision || "", toi: pl.toi });
      });
    });
  });
  const sg = JSON.stringify(out);
  if (sg === window.__LPSG120) return false;
  window.__LPSG120 = sg; window.__LIVEPTS = out; window.__LIVEV120 = (window.__LIVEV120 || 0) + 1;
  return true;
}
window.gxLive120 = (js, done) => {
  if (G120.busy || !js || !js.games) return;
  const isF = (g) => g.gameState === "FINAL" || g.gameState === "OFF";
  const games = js.games.filter((g) => g.id && (g.gameState === "LIVE" || g.gameState === "CRIT" || (isF(g) && !G120.fin[g.id])));
  if (!games.length) return;
  G120.busy = true;
  const U = "https://api-web.nhle.com/v1/gamecenter/";
  Promise.all(games.map((g) => fetch(U + g.id + "/boxscore").then((r) => (r.ok ? r.json() : null)).catch(() => null).then((bx) => {
    if (!bx) return null;
    const goals = ((g.homeTeam || {}).score || 0) + ((g.awayTeam || {}).score || 0), needP = goals > 0 && G120.goals[g.id] !== goals;
    return (needP ? fetch(U + g.id + "/play-by-play").then((r) => (r.ok ? r.json() : null)).catch(() => null) : Promise.resolve(null)).then((pb) => {
      if (pb) { G120.pp[g.id] = gxPP120(pb); G120.goals[g.id] = goals; }
      const old = G120.box[g.id];
      G120.box[g.id] = { bx, d: g.gameDate, start: g.startTimeUTC || "", fin: isF(g) ? (old && old.fin) || (old ? Date.now() : (Date.parse(g.startTimeUTC || "") || 0) + 3 * 36e5) : 0 };
      if (isF(g) && (!needP || pb)) G120.fin[g.id] = 1;
      return null;
    });
  }))).then(() => { G120.busy = false; if (gxRebuild120() && done) done(); }, () => { G120.busy = false; });
};
// the live box score line for one player on one day (from the NHL), or null
function gxLiveStat120(p, dt) {
  const D = (window.__LIVEPTS || {})[dt];
  if (!D || !p) return null;
  const no = typeof gxPdNo === "function" ? gxPdNo(p) : null;
  let x = no != null ? D[p.t + "#" + no] : null;
  if (!x) { const ln = nrm(String(p.n || "").split(" ").slice(1).join(" ")); x = ln ? D[p.t + ":" + nrm(p.n).charAt(0) + ":" + ln] : null; }
  return x || null;
}
// live numbers count while the game is on, and after it ends until an ESPN sync from after the final confirms them
function gxUseLive120(p, dt, a) {
  const L = gxLiveStat120(p, dt);
  if (!L) return null;
  const g = gState(p.t, dt);
  if (g.s === "L") return L;
  if (g.s !== "F") return null;
  if (a == null) return L;
  const gen = Date.parse(String((window.ESPN_DATA || {}).generated || "") + "Z"), fin = L.fin || (L.gs ? Date.parse(L.gs) + 3 * 36e5 : 0);
  return !isNaN(gen) && fin && gen > fin + 5 * 60e3 ? null : L;
}
const gxLiveA120 = (p, dt, a) => { const L = p && dt ? gxUseLive120(p, dt, a) : null; return L ? L.fp : a; };
// team scores with today's live points in place of the last sync's
const W120 = new WeakMap();
function gxAct120(w) {
  const A = (w && w.act) || {}, today = todayISO();
  if (!w || !window.__LIVEPTS || !(w.dates || []).includes(today)) return A;
  const c = W120.get(w), k = (window.__LIVEV120 || 0) + "|" + ((window.ESPN_DATA || {}).generated || "");
  if (c && c.k === k && c.A === A) return c.v;
  const v = { ...A }, P = pby();
  Object.keys(A).forEach((tid) => {
    const AD = actDay(tid, today);
    if (!AD) return;
    let d = 0;
    Object.entries(AD).forEach(([pid, x]) => { if (!x || !ESLOT[x[1]]) return; const p = P["e" + pid]; if (!p) return; const a2 = gxLiveA120(p, today, x[0]); if (a2 != null) d += a2 - (x[0] || 0); });
    v[tid] = (+A[tid] || 0) + d;
  });
  W120.set(w, { k, A, v });
  return v;
}
'''

DEPS = ['}, [s.players, wk, K, done, a, b, gen]);', '}), [s.players, wk, K, gen, s.opp]);', '}, [cur, fin, opp, w, s.players, K, window.__PMODE]);',
        '}), [s.players, w, fin, K, gen, window.__PMODE]);', '}, [w, opp, fin, s.players, K, gen, window.__PMODE]);',
        'wk, K, s.me), [s.players, wk, K]);', 'wk, K, opp), [s.players, wk, K, opp]);']


def change(t):
    t = lit(t, "120: helpers", ROOT, HELPERS + ROOT, "change 120: live fantasy points")
    if "gxAct120(wk)" not in t:
        n = 0
        for o, nw in [("(wk.act || {})", "gxAct120(wk)"), ("(w.act || {})", "gxAct120(w)"), ("(live.act || {})", "gxAct120(live)")]:
            n += t.count(o)
            t = t.replace(o, nw)
        if n < 20:
            fail("120: expected about 23 score reads, found %d" % n)
        print("(install) 120: live team scores (%d places): updated" % n)
    else:
        print("(install) 120: live team scores: already done")
    for d in DEPS:
        nd = d.replace("]);", ", window.__LIVEV120]);")
        t = lit(t, "120: refresh " + d[:30], d, nd, nd)
    t = lit(t, "120: live points in the week", "  const take = (p, pp, slot, a, assume) => {\n",
            "  const take = (p, pp, slot, a, assume) => {\n    a = gxLiveA120(p, dt, a); /* gx120 */\n", "a = gxLiveA120(p, dt, a); /* gx120 */")
    t = lit(t, "120: live box score lines",
            'const pStat = (p, dt) => { const id = String((p && p.id) || "").replace(/^e/, ""); return ((((window.ESPN_DATA || {}).pstat || {})[dt]) || {})[id] || null; };',
            'const pStat = (p, dt) => { const id = String((p && p.id) || "").replace(/^e/, ""); const E0 = ((((window.ESPN_DATA || {}).pstat || {})[dt]) || {})[id] || null; const L = p && dt && typeof gxUseLive120 === "function" ? gxUseLive120(p, dt, gxPdReal(p, dt)) : null; return L || E0; /* gx120 */ };',
            "return L || E0; /* gx120 */")
    t = lit(t, "120: league scoring for live points", "  const P = { s, setS, wk, setWk, go };", "  window.__SC120 = s.sc; const P = { s, setS, wk, setWk, go };", "window.__SC120 = s.sc;")
    t = lit(t, "120: check every 15 seconds during games", "const id = setInterval(pull, 60 * 1000);",
            "const id = setInterval(() => { if (document.hidden) return; if (window.__LIVEANY120 || Date.now() - (window.__LP120 || 0) > 59000) pull(); }, 15 * 1000); /* gx120 */",
            "15 * 1000); /* gx120 */")
    t = lit(t, "120: live box scores after the scores", "      window.__LIVESC = out; tick((x) => x + 1);",
            '      window.__LP120 = Date.now(); window.__LIVEANY120 = js.games.some((g) => g.gameState === "LIVE" || g.gameState === "CRIT" || ((g.gameState === "FUT" || g.gameState === "PRE") && g.startTimeUTC && Date.parse(g.startTimeUTC) - Date.now() < 15 * 60e3));\n'
            '      const sg120 = JSON.stringify(out); window.__LIVESC = out; if (sg120 !== window.__LSG120) { window.__LSG120 = sg120; tick((x) => x + 1); }\n'
            '      if (window.gxLive120) window.gxLive120(js, () => tick((x) => x + 1));',
            "window.gxLive120(js, () => tick")
    # no Ask button
    t = lit(t, "120: no Ask button", "{window.AskPanel ? <window.AskPanel {...P}", "{false && window.AskPanel ? <window.AskPanel {...P}", "{false && window.AskPanel")
    return t


edit(APP, change)
new_file("gm_live.py", GM_LIVE)
