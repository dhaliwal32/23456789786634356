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
    ESPN_S2 = os.environ.get("ESPN_S2", "")
    SWID = os.environ.get("SWID", "")
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
                    "chg": round((p.get("ownership") or {}).get("percentChange") or 0, 1)})
if skipped:
    print(f"(check) players skipped, unknown NHL team id: {skipped}")
if players:
    x = players[0]
    print(f"(check) example: {x['n']} {x['t']} {x['p']}  team={x['ft']}  proj avg={x['pavg']}")

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
        "periods": periods, "matchups": matchups}
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
for off in (0, 1):
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