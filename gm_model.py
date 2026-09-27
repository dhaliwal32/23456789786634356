"""
gm_model.py - GM projection model for Fantasy Islands.
Per-game fantasy projections from free NHL stats: role/usage rates, shooting % pulled
toward normal, opponent strength, home/away, back-to-backs - and, when available,
betting odds (win probability + expected goals) via gm_odds.py.
Called by espn_sync.py.
"""
import math
import unicodedata
from datetime import datetime, timedelta, date
from zoneinfo import ZoneInfo
import requests

SK = {"G": 6, "A": 4, "PM": 2, "PPP": 2, "SHP": 3, "SOG": 1, "HIT": 0.1, "BLK": 1}
GO = {"W": 5, "GA": -3, "SV": 0.6, "SO": 5, "OTL": 1}

LAST, THIS = "20252026", "20262027"
PRIOR_GAMES = 20
TEAM_PRIOR = 15
DAYS_AHEAD = 35
ET = ZoneInfo("America/New_York")
STATS = "https://api.nhle.com/stats/rest/en"
WEB = "https://api-web.nhle.com/v1"
HDR = {"User-Agent": "Mozilla/5.0"}
ALIAS = {"LAK": "LA", "NJD": "NJ", "SJS": "SJ", "TBL": "TB", "ARI": "UTA", "UTAH": "UTA"}
TEAM_WORDS = [("blue jackets", "CBJ"), ("red wings", "DET"), ("maple leafs", "TOR"), ("golden knights", "VGK"),
              ("ducks", "ANA"), ("bruins", "BOS"), ("sabres", "BUF"), ("flames", "CGY"), ("hurricanes", "CAR"),
              ("blackhawks", "CHI"), ("avalanche", "COL"), ("stars", "DAL"), ("oilers", "EDM"), ("panthers", "FLA"),
              ("kings", "LA"), ("wild", "MIN"), ("canadiens", "MTL"), ("predators", "NSH"), ("devils", "NJ"),
              ("islanders", "NYI"), ("rangers", "NYR"), ("senators", "OTT"), ("flyers", "PHI"), ("penguins", "PIT"),
              ("sharks", "SJ"), ("kraken", "SEA"), ("blues", "STL"), ("lightning", "TB"), ("mammoth", "UTA"),
              ("utah", "UTA"), ("canucks", "VAN"), ("capitals", "WSH"), ("jets", "WPG")]


def clamp(x, lo, hi):
    return max(lo, min(hi, x))


def norm(n):
    n = unicodedata.normalize("NFD", n or "").encode("ascii", "ignore").decode()
    return n.lower().replace(".", "").replace("-", " ").strip()


def ab(x):
    x = (x or "").upper()
    return ALIAS.get(x, x)


def team_code(txt):
    t = unicodedata.normalize("NFD", txt or "").encode("ascii", "ignore").decode().lower()
    for w, c in TEAM_WORDS:
        if w in t:
            return c
    return None


def stats(kind, season):
    try:
        r = requests.get(f"{STATS}/{kind}", headers=HDR, timeout=60,
                         params={"limit": -1, "cayenneExp": f"seasonId={season} and gameTypeId=2"})
        r.raise_for_status()
        return r.json().get("data", [])
    except Exception as ex:
        print(f"(model) could not load {kind} {season}: {ex}")
        return []


def skater_table(season):
    out = {}
    for r in stats("skater/summary", season):
        grp = "D" if r.get("positionCode") == "D" else "F"
        out[(norm(r.get("skaterFullName")), grp)] = {
            "gp": r.get("gamesPlayed") or 0, "G": r.get("goals") or 0, "A": r.get("assists") or 0,
            "PM": r.get("plusMinus") or 0, "PPP": r.get("ppPoints") or 0, "SHP": r.get("shPoints") or 0,
            "SOG": r.get("shots") or 0, "HIT": 0, "BLK": 0}
    for r in stats("skater/realtime", season):
        grp = "D" if r.get("positionCode") == "D" else "F"
        k = (norm(r.get("skaterFullName")), grp)
        if k in out:
            out[k]["HIT"] = r.get("hits") or 0
            out[k]["BLK"] = r.get("blockedShots") or 0
    return out


def goalie_table(season):
    return {norm(r.get("goalieFullName")): {"SA": r.get("shotsAgainst") or 0, "SV": r.get("saves") or 0}
            for r in stats("goalie/summary", season)}


def team_table():
    def rows(season):
        out = {}
        for r in stats("team/summary", season):
            c = team_code(r.get("teamFullName"))
            if c:
                out[c] = {"gp": r.get("gamesPlayed") or 0, "gf": r.get("goalsForPerGame") or 0,
                          "ga": r.get("goalsAgainstPerGame") or 0, "sf": r.get("shotsForPerGame") or 0,
                          "sa": r.get("shotsAgainstPerGame") or 0, "pp": r.get("pointPct") or 0.5}
        return out
    last, this = rows(LAST), rows(THIS)
    keys = ("gf", "ga", "sf", "sa", "pp")
    T = {}
    for c in set(last) | set(this):
        a, b = last.get(c), this.get(c)
        if a and b and b["gp"]:
            T[c] = {k: (a[k] * TEAM_PRIOR + b[k] * b["gp"]) / (TEAM_PRIOR + b["gp"]) for k in keys}
        else:
            T[c] = {k: (a or b)[k] for k in keys}
    L = {k: sum(t[k] for t in T.values()) / max(1, len(T)) for k in keys}
    return T, L


def schedule():
    games = {}
    cur = datetime.now(ET).date()
    end = cur + timedelta(days=DAYS_AHEAD)
    while cur <= end:
        try:
            r = requests.get(f"{WEB}/schedule/{cur.isoformat()}", headers=HDR, timeout=30)
            r.raise_for_status()
            for day in r.json().get("gameWeek", []):
                for g in day.get("games", []):
                    if g.get("gameType") != 2:
                        continue
                    h, a = ab(g["homeTeam"]["abbrev"]), ab(g["awayTeam"]["abbrev"])
                    games.setdefault(h, {})[day["date"]] = (a, True)
                    games.setdefault(a, {})[day["date"]] = (h, False)
        except Exception as ex:
            print(f"(model) schedule lookup failed for {cur}: {ex}")
        cur += timedelta(days=7)
    return games


def rates(grp, ls, ts):
    lgp, tgp = (ls or {}).get("gp", 0), (ts or {}).get("gp", 0)
    if lgp + tgp < 5:
        return None
    w = min(lgp, PRIOR_GAMES)
    r = {}
    for k in ("A", "PM", "PPP", "SHP", "SOG", "HIT", "BLK"):
        lr = (ls[k] / lgp) if lgp else 0
        r[k] = (lr * w + (ts or {}).get(k, 0)) / (w + tgp)
    prior = 0.045 if grp == "D" else 0.105
    g = (ls or {}).get("G", 0) + (ts or {}).get("G", 0)
    s = (ls or {}).get("SOG", 0) + (ts or {}).get("SOG", 0)
    r["G"] = r["SOG"] * (g + prior * 150) / (s + 150)
    r["PM"] *= 0.3
    return r


def skater_pts(r, T, L, opp=None, home=None, b2b=False, od=None):
    o = T.get(opp) if opp else None
    if od:                                   # betting market: expected goals for his team
        m_off = clamp(od["gf"] / L["gf"], 0.75, 1.3)
        hf = 0.97 if b2b else 1.0
    else:
        m_off = clamp(o["ga"] / L["ga"], 0.85, 1.2) if o else 1.0
        hf = 1.0 if home is None else (1.03 if home else 0.98)
        if b2b:
            hf *= 0.96
    m_sog = clamp(o["sa"] / L["sa"], 0.88, 1.15) if o else 1.0
    m_blk = clamp(o["sf"] / L["sf"], 0.88, 1.15) if o else 1.0
    return (SK["G"] * r["G"] * m_off * hf + SK["A"] * r["A"] * m_off * hf + SK["PPP"] * r["PPP"] * m_off * hf
            + SK["SHP"] * r["SHP"] + SK["SOG"] * r["SOG"] * m_sog * hf + SK["HIT"] * r["HIT"]
            + SK["BLK"] * r["BLK"] * m_blk + SK["PM"] * r["PM"])


def goalie_pts(sv, team, T, L, opp=None, home=None, b2b=False, od=None):
    own = T.get(team, L)
    o = T.get(opp, L) if opp else L
    sa = 0.5 * o["sf"] + 0.5 * own["sa"]
    ga = sa * (1 - sv)
    if od:                                   # betting market: win chance + expected goals against
        ga = 0.5 * ga + 0.5 * od["ga"]
        pw = clamp(od["win"], 0.1, 0.9)
    else:
        edge = 0 if home is None else (0.03 if home else -0.03)
        pw = clamp(0.5 + 0.9 * (own["pp"] - o["pp"]) + edge - (0.04 if b2b else 0), 0.25, 0.75)
    potl = (1 - pw) * 0.22
    pso = pw * 0.9 * math.exp(-ga)
    return GO["W"] * pw + GO["OTL"] * potl + GO["SV"] * (sa - ga) + GO["GA"] * ga + GO["SO"] * pso


def build(players):
    print("(model) downloading NHL stats…")
    SL, ST = skater_table(LAST), skater_table(THIS)
    GL, GT = goalie_table(LAST), goalie_table(THIS)
    T, L = team_table()
    sched = schedule()
    try:
        import gm_odds
        ODDS = gm_odds.get_odds(team_code)
    except Exception as ex:
        print(f"(model) odds unavailable: {ex}")
        ODDS = {}
    base, proj = {}, {}
    ns = ng = with_odds = 0
    for p in players:
        pid, tm, key = str(p["id"]), p["t"], norm(p["n"])
        games = sched.get(tm, {})
        if p["p"] == "G":
            gl, gt = GL.get(key), GT.get(key)
            if not gl and not gt:
                continue
            sa = (gl or {}).get("SA", 0) + (gt or {}).get("SA", 0)
            sv = ((gl or {}).get("SV", 0) + (gt or {}).get("SV", 0) + 0.900 * 1500) / (sa + 1500)
            base[pid] = round(goalie_pts(sv, tm, T, L), 2)
            for dt, (opp, home) in games.items():
                b2b = (date.fromisoformat(dt) - timedelta(days=1)).isoformat() in games
                od = ODDS.get(dt, {}).get(tm)
                with_odds += bool(od)
                proj.setdefault(pid, {})[dt] = round(goalie_pts(sv, tm, T, L, opp, home, b2b, od), 2)
            ng += 1
        else:
            grp = "D" if p["p"] == "D" else "F"
            r = rates(grp, SL.get((key, grp)), ST.get((key, grp)))
            if not r:
                continue
            base[pid] = round(skater_pts(r, T, L), 2)
            for dt, (opp, home) in games.items():
                b2b = (date.fromisoformat(dt) - timedelta(days=1)).isoformat() in games
                od = ODDS.get(dt, {}).get(tm)
                with_odds += bool(od)
                proj.setdefault(pid, {})[dt] = round(skater_pts(r, T, L, opp, home, b2b, od), 2)
            ns += 1
    days = len({d for g in sched.values() for d in g})
    print(f"(model) projected {ns} skaters + {ng} goalies over {days} game days  |  teams rated: {len(T)}  |  player-games using betting odds: {with_odds}")
    ex = next((p for p in players if str(p["id"]) in base and p["ft"]), None)
    if ex:
        print(f"(model) example: {ex['n']}  base {base[str(ex['id'])]}  next games: {list(proj.get(str(ex['id']), {}).items())[:3]}")
    return {"asof": datetime.now().isoformat(timespec="seconds"), "base": base, "proj": proj, "odds": ODDS}
