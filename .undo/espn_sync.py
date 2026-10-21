"""
espn_sync.py - pulls your ESPN fantasy hockey league into espn-data.js
so fantasy-gm.html (same folder) updates itself.
Run: right-click this file in PyCharm -> Run 'espn_sync'
"""
import json, os, sys
from datetime import datetime, timedelta, date
from zoneinfo import ZoneInfo
import requests

# ---------- YOUR LEAGUE (keep ESPN_S2 and SWID private!) ----------
LEAGUE_ID = 1363781006
SEASON = 2027
MY_TEAM_ID = 4
try:
    from secrets_local import ESPN_S2, SWID
except ImportError:
       ESPN_S2 = os.environ.get("ESPN_S2", "").strip()
       SWID = os.environ.get("SWID", "").strip()
# ------------------------------------------------------------------

BASE = f"https://lm-api-reads.fantasy.espn.com/apis/v3/games/fhl/seasons/{SEASON}"
LEAGUE = f"{BASE}/segments/0/leagues/{LEAGUE_ID}"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "espn-data.js")
DEBUG = "--debug" in sys.argv
ET = ZoneInfo("America/New_York")
NHL = set("ANA BOS BUF CGY CAR CHI COL CBJ DAL DET EDM FLA LA MIN MTL NSH NJ NYI NYR OTT "
          "PHI PIT SJ SEA STL TB TOR UTA VAN VGK WSH WPG".split())
ALIAS = {"LAK": "LA", "NJD": "NJ", "SJS": "SJ", "TBL": "TB", "WAS": "WSH", "UTAH": "UTA", "ARI": "UTA",
         "PHX": "UTA", "CLB": "CBJ", "CLS": "CBJ", "MON": "MTL", "NAS": "NSH", "WIN": "WPG", "VEG": "VGK",
         "TAM": "TB", "CAL": "CGY", "ANH": "ANA"}

if not ESPN_S2 or not SWID or "PASTE" in ESPN_S2:
    sys.exit("First paste your espn_s2 and SWID values at the top of this file.")

session = requests.Session()
session.headers.update({"User-Agent": "Mozilla/5.0"})
session.cookies.update({"espn_s2": ESPN_S2, "SWID": SWID})


def get(url, params=None, fantasy_filter=None):
    headers = {"x-fantasy-filter": json.dumps(fantasy_filter)} if fantasy_filter else {}
    r = session.get(url, params=params, headers=headers, timeout=30)
    if r.status_code in (401, 403):
        sys.exit("ESPN refused access. Copy espn_s2 and SWID again from Chrome and paste them above.")
    r.raise_for_status()
    return r.json()


def dump(name, data):
    if DEBUG:
        with open(os.path.join(HERE, name), "w", encoding="utf-8") as f:
            json.dump(data, f, indent=1)


# 1) NHL team codes + the calendar date of each ESPN scoring day
pro = get(BASE, params={"view": "proTeamsSchedules_wl"})
dump("espn-raw-pro.json", pro)
pro_abbr, period_date = {}, {}
for t in pro.get("settings", {}).get("proTeams", []):
    ab = str(t.get("abbrev", "")).upper()
    pro_abbr[t["id"]] = ALIAS.get(ab, ab)
    for pid, games in (t.get("proGamesByScoringPeriod") or {}).items():
        for g in games:
            if "date" in g:
                d = datetime.fromtimestamp(g["date"] / 1000, ET).date()
                period_date[int(pid)] = min(period_date.get(int(pid), d), d)
first = min(period_date) if period_date else 1
day1 = period_date[first] - timedelta(days=first - 1) if period_date else date(2026, 9, 29)
pdate = lambda pid: (day1 + timedelta(days=int(pid) - 1)).isoformat()

# 2) League teams, matchup weeks and scores
lg = get(LEAGUE, params=[("view", "mTeam"), ("view", "mSettings"), ("view", "mMatchupScore"), ("view", "mStatus")])
dump("espn-raw-league.json", lg)
teams = [{"id": t["id"], "name": (t.get("name") or f"{t.get('location', '')} {t.get('nickname', '')}".strip()
                                  or f"Team {t['id']}")} for t in lg.get("teams", [])]
mp = lg.get("settings", {}).get("scheduleSettings", {}).get("matchupPeriods", {})
periods = [{"id": int(k), "dates": [pdate(x) for x in mp[k]]} for k in sorted(mp, key=int)]
matchups = []
for m in lg.get("schedule", []):
    h, a = m.get("home") or {}, m.get("away") or {}
    if not h or not a:
        continue
    pts = lambda x: x.get("totalPointsLive", x.get("totalPoints")) or 0
    matchups.append({"period": m.get("matchupPeriodId"), "home": h.get("teamId"), "away": a.get("teamId"),
                     "hs": round(pts(h), 2), "as": round(pts(a), 2)})
current = lg.get("status", {}).get("currentMatchupPeriod") or 1

# 3) Players: everyone rostered + top free agents / waivers
ESPN_TEAM_IDS = {1: "BOS", 2: "BUF", 3: "CGY", 4: "CHI", 5: "DET", 6: "EDM", 7: "CAR", 8: "LA",
                 9: "DAL", 10: "MTL", 11: "NJ", 12: "NYI", 13: "NYR", 14: "OTT", 15: "PHI", 16: "PIT",
                 17: "COL", 18: "SJ", 19: "STL", 20: "TB", 21: "TOR", 22: "VAN", 23: "WSH", 24: "UTA",
                 25: "ANA", 26: "FLA", 27: "NSH", 28: "WPG", 29: "CBJ", 30: "MIN", 37: "VGK",
                 124292: "SEA", 129764: "UTA"}
for k, v in ESPN_TEAM_IDS.items():
    pro_abbr[k] = v
raw = []
for statuses in (["ONTEAM"], ["FREEAGENT", "WAIVERS"]):
    filt = {"players": {"filterStatus": {"value": statuses}, "limit": 1000,
                        "sortPercOwned": {"sortPriority": 1, "sortAsc": False}}}
    pl = get(LEAGUE, params={"view": "kona_player_info"}, fantasy_filter=filt)
    raw += pl.get("players", []) if isinstance(pl, dict) else []
if not any(e.get("onTeamId") for e in raw):  # backup: rosters straight from the league
    rl = get(LEAGUE, params={"view": "mRoster"})
    for t in rl.get("teams", []):
        for en in (t.get("roster") or {}).get("entries", []):
            pe = en.get("playerPoolEntry") or {}
            raw.append({"player": pe.get("player") or {}, "onTeamId": t.get("id")})
dump("espn-raw-players.json", raw)
print(f"(check) raw players from ESPN: {len(raw)}  |  NHL teams known: {len(pro_abbr)}")
players, seen, skipped = [], set(), {}
for e in raw:
    p = e.get("player") or {}
    if not p or p.get("id") in seen:
        continue
    seen.add(p.get("id"))
    ab = pro_abbr.get(p.get("proTeamId"))
    if ab not in NHL:
        skipped[p.get("proTeamId")] = skipped.get(p.get("proTeamId"), 0) + 1
        continue
    tot = avg = pavg = None
    for st in p.get("stats") or []:
        if st.get("seasonId") != SEASON or st.get("statSplitTypeId") != 0:
            continue
        if st.get("statSourceId") == 0:
            tot, avg = st.get("appliedTotal"), st.get("appliedAverage")
        elif st.get("statSourceId") == 1:
            pavg = st.get("appliedAverage")
    players.append({"id": p.get("id"), "n": p.get("fullName"), "t": ab,
                    "p": {4: "D", 5: "G"}.get(p.get("defaultPositionId"), "F"),
                    "ft": e.get("onTeamId", 0) or 0, "status": p.get("injuryStatus") or "ACTIVE",
                    "gp": round(tot / avg) if tot and avg else 0, "tot": round(tot or 0, 1),
                    "avg": round(avg or 0, 2), "pavg": round(pavg or 0, 2),
                    "own": round((p.get("ownership") or {}).get("percentOwned") or 0, 1),
                    "chg": round((p.get("ownership") or {}).get("percentChange") or 0, 1), "wv": 1 if e.get("status") == "WAIVERS" else 0})
if skipped:
    print(f"(check) players skipped, unknown NHL team id: {skipped}")
if players:
    x = players[0]
    print(f"(check) example: {x['n']} {x['t']} {x['p']}  team={x['ft']}  proj avg={x['pavg']}")

print(f"(check) players on waivers: {sum(1 for x_ in players if x_.get('wv'))}")
slots = {}
try:
    rl = get(LEAGUE, params={"view": "mRoster"})
    for t in rl.get("teams", []):
        for en in (t.get("roster") or {}).get("entries", []):
            slots[en.get("playerId")] = en.get("lineupSlotId")
except Exception:
    pass
for p in players:
    p["ir"] = slots.get(p["id"]) == 8
print(f"(check) players in IR slots: {[p['n'] for p in players if p['ir']]}")
data = {"generated": datetime.now().isoformat(timespec="seconds"),
        "leagueName": lg.get("settings", {}).get("name", ""), "myTeamId": MY_TEAM_ID,
        "currentPeriod": current, "teams": teams, "players": players,
        "periods": periods, "matchups": matchups, "slots": {str(k): v for k, v in slots.items()}, "acq": ({str(t.get("id")): ((t.get("transactionCounter") or {}).get("matchupAcquisitionTotals") or {}) for t in lg.get("teams", [])} if any("transactionCounter" in t for t in lg.get("teams", [])) else None)}
# 3b) actual points per player per day + NHL game states (news_logos.py round 16)
try:
    today_et = datetime.now(ET).date()
    sp_of = {d_.isoformat(): pid_ for pid_, d_ in period_date.items()}
    # 3c) per-player points from ESPN box scores (news_logos.py round 17)
    cur_sp_ = lg.get("scoringPeriodId") or (lg.get("status") or {}).get("latestScoringPeriod")
    if cur_sp_:
        span_ = [(pdate(x_), x_) for x_ in range(max(1, int(cur_sp_) - 6), int(cur_sp_) + 1)]
    else:
        span_ = [(dd_, sp_of.get(dd_)) for dd_ in ((today_et - timedelta(days=b_)).isoformat() for b_ in range(6, -1, -1))]
    daily = {}
    for dd_, sp_ in span_:
        if not sp_:
            continue
        day_ = {}
        try:
            rs_ = get(LEAGUE, params=[("view", "mMatchupScore"), ("view", "mScoreboard"), ("scoringPeriodId", sp_)])
            dump(f"espn-raw-daily-{dd_}.json", rs_)
            for m_ in rs_.get("schedule", []):
                for side_ in ("home", "away"):
                    ts_ = m_.get(side_) or {}
                    ents_ = (ts_.get("rosterForCurrentScoringPeriod") or {}).get("entries") or []
                    if not ents_:
                        continue
                    tm_ = {}
                    for en_ in ents_:
                        pe_ = en_.get("playerPoolEntry") or {}
                        pts_ = None
                        for st_ in (pe_.get("player") or {}).get("stats") or []:
                            if st_.get("scoringPeriodId") == sp_ and st_.get("statSourceId") == 0:
                                pts_ = st_.get("appliedTotal")
                                break
                        if pts_ is None:
                            pts_ = pe_.get("appliedStatTotal")
                        tm_[str(en_.get("playerId"))] = [None if pts_ is None else round(pts_, 2), en_.get("lineupSlotId")]
                    day_[str(ts_.get("teamId"))] = tm_
        except Exception as ex:
            print(f"(daily) ESPN box scores for {dd_} failed: {ex}")
        mine_n_ = sum(1 for v in day_.get(str(MY_TEAM_ID), {}).values() if v[0])
        print(f"(daily) {dd_} (scoring period {sp_}): {len(day_)} teams, {mine_n_} of your players with points")
        if day_:
            daily[dd_] = day_
    import unicodedata as ud_

    def _toks(n):
        n = ud_.normalize("NFD", n or "").encode("ascii", "ignore").decode().lower().replace(".", " ").replace("-", " ").replace("'", "")
        return n.split()

    def _nk(n):
        p = _toks(n)
        return (p[0][0] + " " + " ".join(p[1:])) if len(p) > 1 else " ".join(p)

    def _nk2(n):
        p = _toks(n)
        return (p[0][0] + " " + p[-1]) if len(p) > 1 else " ".join(p)

    _pidx = {}
    _pidx3 = {}
    for p_ in players:
        if p_.get("n"):
            for k_ in {_nk(p_["n"]), _nk2(p_["n"])}:
                _pidx.setdefault((k_, p_["t"]), p_["id"])
                _pidx3.setdefault((k_, p_["t"], p_["p"]), p_["id"])
    gstate = {}
    pstat = {}
    for back_ in (1, 0):
        dd_ = (today_et - timedelta(days=back_)).isoformat()
        try:
            js_ = requests.get(f"https://api-web.nhle.com/v1/score/{dd_}", headers={"User-Agent": "Mozilla/5.0"}, timeout=20).json()
        except Exception as ex:
            print(f"(daily) NHL scores for {dd_} failed: {ex}")
            continue
        gs_ = {}
        for g_ in js_.get("games", []):
            s_ = str(g_.get("gameState") or "")
            s_ = "F" if s_ in ("FINAL", "OFF") else "L" if s_ in ("LIVE", "CRIT") else "P"
            per_ = (g_.get("periodDescriptor") or {}).get("number") or 1
            rem_ = (g_.get("clock") or {}).get("secondsRemaining")
            rem_ = 1200 if rem_ is None else rem_
            f_ = 1.0 if s_ == "F" else 0.0 if s_ == "P" else min(0.99, ((per_ - 1) * 1200 + (1200 - rem_)) / 3600)
            pd_ = g_.get("periodDescriptor") or {}
            ck_ = g_.get("clock") or {}
            pdl_ = "OT" if pd_.get("periodType") == "OT" else "SO" if pd_.get("periodType") == "SO" else {1: "1st", 2: "2nd", 3: "3rd"}.get(per_, str(per_))
            hs_, as_ = (g_.get("homeTeam") or {}).get("score"), (g_.get("awayTeam") or {}).get("score")
            for side_, me_, op_ in (("homeTeam", hs_, as_), ("awayTeam", as_, hs_)):
                ab_ = str((g_.get(side_) or {}).get("abbrev") or "").upper()
                gs_[ALIAS.get(ab_, ab_)] = {"s": s_, "f": round(f_, 2), "my": me_, "op": op_, "per": pdl_,
                                            "clk": ck_.get("timeRemaining") or "", "int": bool(ck_.get("inIntermission"))}
        pst_ = {}
        for g_ in js_.get("games", []):  # 3d) player box scores (news_logos.py round 22)
            if str(g_.get("gameState") or "") not in ("LIVE", "CRIT", "FINAL", "OFF") or not g_.get("id"):
                continue
            try:
                bx_ = requests.get(f"https://api-web.nhle.com/v1/gamecenter/{g_['id']}/boxscore", headers={"User-Agent": "Mozilla/5.0"}, timeout=20).json()
            except Exception as ex:
                print(f"(daily) box score {g_.get('id')} failed: {ex}")
                continue
            pbg_ = bx_.get("playerByGameStats") or {}
            for side_ in ("homeTeam", "awayTeam"):
                tab_ = str((bx_.get(side_) or g_.get(side_) or {}).get("abbrev") or "").upper()
                tab_ = ALIAS.get(tab_, tab_)
                grp_ = pbg_.get(side_) or {}
                for x_, gp_ in [(y_, "F") for y_ in (grp_.get("forwards") or [])] + [(y_, "D") for y_ in (grp_.get("defense") or [])] + [(y_, "G") for y_ in (grp_.get("goalies") or [])]:
                    nm_ = (x_.get("name") or {}).get("default") or ""
                    pid_ = _pidx3.get((_nk(nm_), tab_, gp_)) or _pidx3.get((_nk2(nm_), tab_, gp_))
                    if not pid_:
                        continue
                    if "saves" in x_ or "goalsAgainst" in x_ or "saveShotsAgainst" in x_:
                        if not x_.get("toi") or x_.get("toi") == "00:00":
                            continue
                        pst_[str(pid_)] = {"sv": x_.get("saves") or 0, "ga": x_.get("goalsAgainst") or 0,
                                           "dec": x_.get("decision") or "", "toi": x_.get("toi") or "", "sa": x_.get("shotsAgainst"), "svp": x_.get("savePctg"), "es": x_.get("evenStrengthShotsAgainst") or "", "pp": x_.get("powerPlayShotsAgainst") or "", "sh": x_.get("shorthandedShotsAgainst") or ""}
                    else:
                        pst_[str(pid_)] = {"g": x_.get("goals") or 0, "a": x_.get("assists") or 0, "pm": x_.get("plusMinus") or 0,
                                           "sog": x_.get("sog") or 0, "pim": x_.get("pim") or 0, "hit": x_.get("hits") or 0,
                                           "blk": x_.get("blockedShots") or 0, "toi": x_.get("toi") or "", "ppg": x_.get("powerPlayGoals") or 0, "fo": x_.get("faceoffWinningPctg"), "shf": x_.get("shifts"), "gv": x_.get("giveaways") or 0, "tk": x_.get("takeaways") or 0}
        pstat[dd_] = pst_
        print(f"(daily) {dd_}: box-score lines for {len(pst_)} league players")
        gstate[dd_] = gs_
    data["daily"] = daily
    data["gstate"] = gstate
    data["pstat"] = pstat
    # 3e) box-score history for the player pop-up: one small file per finished day (news_logos.py round 31)
    try:
        bdir31_ = os.path.join(HERE, "box")
        os.makedirs(bdir31_, exist_ok=True)
        ipath31_ = os.path.join(bdir31_, "index.json")
        try:
            with open(ipath31_, encoding="utf-8") as f31_:
                idx31_ = json.load(f31_)
        except Exception:
            idx31_ = {}
        if idx31_.get("v") != 2:
            idx31_ = {"none": idx31_.get("none") or []}
        have31_, none31_ = set(idx31_.get("dates") or []), set(idx31_.get("none") or [])
        d31_ = min(period_date.values()) if period_date else day1
        todo31_ = []
        while d31_ <= today_et:
            if d31_.isoformat() not in have31_ and d31_.isoformat() not in none31_:
                todo31_.append(d31_.isoformat())
            d31_ += timedelta(days=1)
        new31_ = 0
        for dd31_ in todo31_[:12]:
            try:
                sj31_ = requests.get(f"https://api-web.nhle.com/v1/score/{dd31_}", headers={"User-Agent": "Mozilla/5.0"}, timeout=20).json()
                gms31_ = [g31_ for g31_ in sj31_.get("games", []) if g31_.get("gameType", 2) == 2 and str(g31_.get("gameScheduleState") or "OK") == "OK"]
                if not gms31_:
                    if dd31_ < today_et.isoformat():
                        none31_.add(dd31_)
                    continue
                if not all(str(g31_.get("gameState") or "") in ("FINAL", "OFF") for g31_ in gms31_):
                    continue
                fp31_ = {}
                for tm31_ in (daily.get(dd31_) or {}).values():
                    for pid31_, v31_ in tm31_.items():
                        if v31_ and v31_[0] is not None:
                            fp31_[str(pid31_)] = v31_[0]
                out31_ = {}
                for g31_ in gms31_:
                    bx31_ = requests.get(f"https://api-web.nhle.com/v1/gamecenter/{g31_['id']}/boxscore", headers={"User-Agent": "Mozilla/5.0"}, timeout=20).json()
                    pbg31_ = bx31_.get("playerByGameStats") or {}
                    sc31_ = {s31_: (bx31_.get(s31_) or g31_.get(s31_) or {}) for s31_ in ("homeTeam", "awayTeam")}
                    ab31_ = {}
                    for s31_ in ("homeTeam", "awayTeam"):
                        a31_ = str(sc31_[s31_].get("abbrev") or "").upper()
                        ab31_[s31_] = ALIAS.get(a31_, a31_)
                    for s31_, o31_ in (("homeTeam", "awayTeam"), ("awayTeam", "homeTeam")):
                        grp31_ = pbg31_.get(s31_) or {}
                        base31_ = {"t": ab31_[s31_], "o": ab31_[o31_], "h": 1 if s31_ == "homeTeam" else 0,
                                   "my": sc31_[s31_].get("score"), "op": sc31_[o31_].get("score")}
                        for x31_, gp31_ in [(y31_, "F") for y31_ in (grp31_.get("forwards") or [])] + [(y31_, "D") for y31_ in (grp31_.get("defense") or [])] + [(y31_, "G") for y31_ in (grp31_.get("goalies") or [])]:
                            nm31_ = (x31_.get("name") or {}).get("default") or ""
                            pid31_ = _pidx3.get((_nk(nm31_), ab31_[s31_], gp31_)) or _pidx3.get((_nk2(nm31_), ab31_[s31_], gp31_))
                            if not pid31_:
                                continue
                            if "saves" in x31_ or "goalsAgainst" in x31_ or "saveShotsAgainst" in x31_:
                                if not x31_.get("toi") or x31_.get("toi") == "00:00":
                                    continue
                                ln31_ = {"sv": x31_.get("saves") or 0, "ga": x31_.get("goalsAgainst") or 0, "dec": x31_.get("decision") or "",
                                         "toi": x31_.get("toi") or "", "sa": x31_.get("shotsAgainst"), "svp": x31_.get("savePctg")}
                            else:
                                ln31_ = {"g": x31_.get("goals") or 0, "a": x31_.get("assists") or 0, "pm": x31_.get("plusMinus") or 0,
                                         "sog": x31_.get("sog") or 0, "pim": x31_.get("pim") or 0, "hit": x31_.get("hits") or 0,
                                         "blk": x31_.get("blockedShots") or 0, "toi": x31_.get("toi") or "", "ppg": x31_.get("powerPlayGoals") or 0,
                                         "fo": x31_.get("faceoffWinningPctg"), "shf": x31_.get("shifts"), "gv": x31_.get("giveaways") or 0, "tk": x31_.get("takeaways") or 0}
                            ln31_.update(base31_)
                            if str(pid31_) in fp31_:
                                ln31_["fp"] = fp31_[str(pid31_)]
                            out31_[str(pid31_)] = ln31_
                try:
                    with open(os.path.join(bdir31_, dd31_ + ".json"), encoding="utf-8") as f31_:
                        old41_ = (json.load(f31_) or {}).get("p") or {}
                    for k41_, v41_ in out31_.items():
                        if "fp" not in v41_ and "fp" in (old41_.get(k41_) or {}):
                            v41_["fp"] = old41_[k41_]["fp"]
                except Exception:
                    pass
                with open(os.path.join(bdir31_, dd31_ + ".json"), "w", encoding="utf-8") as f31_:
                    json.dump({"d": dd31_, "p": out31_}, f31_, separators=(",", ":"))
                have31_.add(dd31_)
                new31_ += 1
            except Exception as ex31_:
                print(f"(box) history for {dd31_} failed: {ex31_}")
        with open(ipath31_, "w", encoding="utf-8") as f31_:
            json.dump({"v": 2, "dates": sorted(have31_), "none": sorted(none31_)}, f31_, separators=(",", ":"))
        print(f"(box) history: {new31_} new day(s), {len(have31_)} saved in total")
    except Exception as ex31_:
        print(f"(box) history failed: {ex31_}")
    mine_ = str(MY_TEAM_ID)
    for dd_, day_ in daily.items():
        tot_ = sum((v[0] or 0) for v in day_.get(mine_, {}).values() if v[1] in (3, 4, 5, 6))
        print(f"(daily) {dd_}: your active players scored {round(tot_, 1)}")
    for m_ in matchups:
        if m_["period"] == current and MY_TEAM_ID in (m_["home"], m_["away"]):
            print(f"(daily) ESPN week score for you: {m_['hs'] if m_['home'] == MY_TEAM_ID else m_['as']}")
    print("(daily) NHL game states:", {k_: sorted(set(v["s"] for v in g2_.values())) for k_, g2_ in gstate.items()})
except Exception as ex:
    print(f"(check) daily actual points failed: {ex}")
# 4) Starting goalies from Daily Faceoff (today + tomorrow)
import re
TEAM_WORDS = [("blue jackets", "CBJ"), ("red wings", "DET"), ("maple leafs", "TOR"), ("golden knights", "VGK"),
              ("ducks", "ANA"), ("bruins", "BOS"), ("sabres", "BUF"), ("flames", "CGY"), ("hurricanes", "CAR"),
              ("blackhawks", "CHI"), ("avalanche", "COL"), ("stars", "DAL"), ("oilers", "EDM"), ("panthers", "FLA"),
              ("kings", "LA"), ("wild", "MIN"), ("canadiens", "MTL"), ("predators", "NSH"), ("devils", "NJ"),
              ("islanders", "NYI"), ("rangers", "NYR"), ("senators", "OTT"), ("flyers", "PHI"), ("penguins", "PIT"),
              ("sharks", "SJ"), ("kraken", "SEA"), ("blues", "STL"), ("lightning", "TB"), ("mammoth", "UTA"),
              ("utah", "UTA"), ("canucks", "VAN"), ("capitals", "WSH"), ("jets", "WPG")]


def team_code(txt):
    t = (txt or "").lower().replace("-", " ")
    for w, c in TEAM_WORDS:
        if w in t:
            return c
    return None


def find_games(obj, out):
    if isinstance(obj, dict):
        keys = [k.lower() for k in obj]
        if any("home" in k and "goalie" in k for k in keys) and any("away" in k and "goalie" in k for k in keys):
            out.append(obj)
        for v in obj.values():
            find_games(v, out)
    elif isinstance(obj, list):
        for v in obj:
            find_games(v, out)


def pick(d, side, *needles):
    for k, v in d.items():
        kl = k.lower()
        if kl.startswith(side) and all(n in kl for n in needles) and isinstance(v, str) and v.strip():
            return v.strip()
    return None


goalies = {}
for off in range(8):
    day = (datetime.now(ET) + timedelta(days=off)).date().isoformat()
    try:
        html = requests.get(f"https://www.dailyfaceoff.com/starting-goalies/{day}",
                            headers={"User-Agent": "Mozilla/5.0"}, timeout=30).text
        m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html, re.S)
        games = []
        if m:
            find_games(json.loads(m.group(1)), games)
        day_map = {}
        for g in games:
            for side in ("home", "away"):
                name = pick(g, side, "goalie", "name")
                if not name:
                    continue
                status = pick(g, side, "strength") or pick(g, side, "status") or "Unconfirmed"
                team = team_code(pick(g, side, "team", "name") or pick(g, side, "team", "slug") or pick(g, side, "team"))
                day_map[name] = {"status": status, "team": team}
        goalies[day] = day_map
        print(f"(check) starting goalies {day}: {len(day_map)} found, e.g. {list(day_map.items())[:2]}")
    except Exception as ex:
        print(f"(check) goalie lookup failed for {day}: {ex}")
data["goalies"] = goalies
try:
    import gm_model
    data["model"] = gm_model.build(players)
except Exception as ex:
    print(f"(check) GM model failed: {ex}")
try:
    import gm_signals
    data["signals"] = gm_signals.build(players)
except Exception as ex:
    print(f"(check) signals failed: {ex}")
try:
    
    import gm_alerts
    gm_alerts.run(players, globals().get("slots", {}), data.get("goalies", {}), data.get("signals", {}), MY_TEAM_ID)
except Exception as ex:
    print(f"(check) alerts failed: {ex}")

with open(OUT, "w", encoding="utf-8") as f:
    f.write("window.ESPN_DATA = " + json.dumps(data) + ";\n")

rostered = sum(1 for p in players if p["ft"])
print(f"League: {data['leagueName']}  |  current week: {current}")
print(f"Teams: {len(teams)}  |  players: {len(players)} ({rostered} rostered, {len(players) - rostered} free agents)")
print(f"With ESPN projections: {sum(1 for p in players if p['pavg'])}  |  with season stats: {sum(1 for p in players if p['gp'])}")
print(f"Your team: {next((t['name'] for t in teams if t['id'] == MY_TEAM_ID), '?')}")
print(f"Saved {OUT} - now refresh fantasy-gm.html")

# locked-in 57 (news_logos.py)
