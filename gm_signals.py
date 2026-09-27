"""
gm_signals.py - hot/cold form (last 14 days, NHL stats), PP1 units (Daily Faceoff, checked once a day),
team power-play ranking (NHL stats) and news (ESPN). Called by espn_sync.py.
"""
import json
import os
import re
from datetime import datetime, timedelta
import requests
from gm_model import norm, SK, GO, THIS, LAST, stats, team_code, ab

HERE = os.path.dirname(os.path.abspath(__file__))
PP_CACHE = os.path.join(HERE, "pp1_cache.json")
HDR = {"User-Agent": "Mozilla/5.0"}
STATS = "https://api.nhle.com/stats/rest/en"
DAYS = 14
PP_PRIOR = 5   # 2025-26 counts like this many games once 2026-27 starts (0 = this season only)
SLUGS = {"ANA": "anaheim-ducks", "BOS": "boston-bruins", "BUF": "buffalo-sabres", "CGY": "calgary-flames",
         "CAR": "carolina-hurricanes", "CHI": "chicago-blackhawks", "COL": "colorado-avalanche",
         "CBJ": "columbus-blue-jackets", "DAL": "dallas-stars", "DET": "detroit-red-wings", "EDM": "edmonton-oilers",
         "FLA": "florida-panthers", "LA": "los-angeles-kings", "MIN": "minnesota-wild", "MTL": "montreal-canadiens",
         "NSH": "nashville-predators", "NJ": "new-jersey-devils", "NYI": "new-york-islanders",
         "NYR": "new-york-rangers", "OTT": "ottawa-senators", "PHI": "philadelphia-flyers",
         "PIT": "pittsburgh-penguins", "SJ": "san-jose-sharks", "SEA": "seattle-kraken", "STL": "st-louis-blues",
         "TB": "tampa-bay-lightning", "TOR": "toronto-maple-leafs", "UTA": "utah-mammoth",
         "VAN": "vancouver-canucks", "VGK": "vegas-golden-knights", "WSH": "washington-capitals", "WPG": "winnipeg-jets"}
POS = ["hot streak", "streak", "promot", "top line", "top-line", "first line", "power play", "pp1", "career-high",
       "multi-point", "hat trick", "returns", "activated", "back in the lineup", "strong start"]
NEG = ["injur", "out for", "out indefinitely", "scratch", "day-to-day", "surgery", "demot", "suspend",
       "sidelined", "placed on ir", "week-to-week", "month-to-month"]


# ---------- recent form ----------
def get_stats(kind, start, end):
    exp = f'seasonId={THIS} and gameTypeId=2 and gameDate<="{end} 23:59:59" and gameDate>="{start}"'
    r = requests.get(f"{STATS}/{kind}", params={"limit": -1, "cayenneExp": exp}, headers=HDR, timeout=60)
    r.raise_for_status()
    return r.json().get("data", [])


def recent(players):
    end = datetime.now().date()
    start = end - timedelta(days=DAYS)
    sk = {}
    for r in get_stats("skater/summary", start, end):
        grp = "D" if r.get("positionCode") == "D" else "F"
        sk[(norm(r.get("skaterFullName")), grp)] = {
            "gp": r.get("gamesPlayed") or 0,
            "pts": SK["G"] * (r.get("goals") or 0) + SK["A"] * (r.get("assists") or 0)
            + SK["PM"] * (r.get("plusMinus") or 0) + SK["PPP"] * (r.get("ppPoints") or 0)
            + SK["SHP"] * (r.get("shPoints") or 0) + SK["SOG"] * (r.get("shots") or 0)}
    for r in get_stats("skater/realtime", start, end):
        grp = "D" if r.get("positionCode") == "D" else "F"
        k = (norm(r.get("skaterFullName")), grp)
        if k in sk:
            sk[k]["pts"] += SK["HIT"] * (r.get("hits") or 0) + SK["BLK"] * (r.get("blockedShots") or 0)
    go = {}
    for r in get_stats("goalie/summary", start, end):
        go[norm(r.get("goalieFullName"))] = {
            "gp": r.get("gamesStarted") or r.get("gamesPlayed") or 0,
            "pts": GO["W"] * (r.get("wins") or 0) + GO["GA"] * (r.get("goalsAgainst") or 0)
            + GO["SV"] * (r.get("saves") or 0) + GO["SO"] * (r.get("shutouts") or 0)
            + GO["OTL"] * (r.get("otLosses") or 0)}
    out = {}
    for p in players:
        key = norm(p["n"])
        x = go.get(key) if p["p"] == "G" else sk.get((key, "D" if p["p"] == "D" else "F"))
        if x and x["gp"]:
            out[str(p["id"])] = {"gp": x["gp"], "ppg": round(x["pts"] / x["gp"], 2)}
    print(f"(signals) recent form: {len(out)} players with games in the last {DAYS} days")
    return out


# ---------- PP1 units ----------
PP_RE = re.compile(r"^(pp ?1|powerplay ?1|power ?play ?(unit )?1|1st power ?play( unit)?|first power ?play( unit)?)$", re.I)
NAME_KEYS = ("playerName", "name", "fullName", "player_name")


def names_in(obj, out):
    if isinstance(obj, dict):
        for k in NAME_KEYS:
            if isinstance(obj.get(k), str) and " " in obj[k]:
                out.add(obj[k])
                break
        for v in obj.values():
            if isinstance(v, (dict, list)):
                names_in(v, out)
    elif isinstance(obj, list):
        for v in obj:
            names_in(v, out)


def find_pp1(obj, out):
    if isinstance(obj, dict):
        if any(isinstance(v, str) and PP_RE.match(v.strip()) for v in obj.values()):
            names_in(obj, out)
        for v in obj.values():
            find_pp1(v, out)
    elif isinstance(obj, list):
        for v in obj:
            find_pp1(v, out)


def pp1(players):
    today = datetime.now().date().isoformat()
    cache = {}
    if os.path.exists(PP_CACHE):
        with open(PP_CACHE, encoding="utf-8") as f:
            cache = json.load(f)
    if cache.get("date") != today:
        units = {}
        for t, slug in SLUGS.items():
            try:
                html = requests.get(f"https://www.dailyfaceoff.com/teams/{slug}/line-combinations",
                                    headers=HDR, timeout=30).text
                m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html, re.S)
                names = set()
                if m:
                    find_pp1(json.loads(m.group(1)), names)
                units[t] = sorted(names) if 3 <= len(names) <= 8 else cache.get("units", {}).get(t, [])
            except Exception:
                units[t] = cache.get("units", {}).get(t, [])
        cache = {"date": today, "prev": cache.get("units", {}), "units": units}
        with open(PP_CACHE, "w", encoding="utf-8") as f:
            json.dump(cache, f)
    units, prev = cache.get("units", {}), cache.get("prev", {})
    by = {norm(p["n"]): str(p["id"]) for p in players}
    on, chg = {}, {}
    for t, names in units.items():
        before = set(prev.get(t, []))
        for n in names:
            pid = by.get(norm(n))
            if pid:
                on[pid] = True
                if before and n not in before:
                    chg[pid] = "added"
        if before:
            for n in before - set(names):
                pid = by.get(norm(n))
                if pid:
                    chg[pid] = "removed"
    teams_ok = sum(1 for v in units.values() if v)
    print(f"(signals) PP1: {teams_ok}/32 teams read, {len(on)} players on PP1, {len(chg)} changes vs last day")
    return {"asof": cache.get("date"), "on": on, "changes": chg, "units": units}


# ---------- team power-play ranking ----------
def team_pp():
    def season(sid):
        pts, gp, pct = {}, {}, {}
        for r in stats("skater/summary", sid):
            t = ab((r.get("teamAbbrevs") or "").split(",")[-1].strip())
            pts[t] = pts.get(t, 0) + (r.get("ppPoints") or 0)
        for r in stats("team/summary", sid):
            c = team_code(r.get("teamFullName"))
            if c:
                gp[c] = r.get("gamesPlayed") or 0
                v = r.get("powerPlayPct") or 0
                pct[c] = v * 100 if v <= 1 else v
        return pts, gp, pct

    lpts, lgp, lpct = season(LAST)
    tpts, tgp, tpct = season(THIS)
    print(f"(signals) team PP check: {len(lgp)} teams found for 2025-26, {len(tgp)} for 2026-27")
    out = {}
    for t in set(lgp) | set(tgp):
        g = tgp.get(t, 0)
        last_rate = lpts.get(t, 0) / max(1, lgp.get(t, 82))
        this_rate = tpts.get(t, 0) / g if g else 0
        w = PP_PRIOR if g else 1
        rate = (last_rate * w + this_rate * g) / (w + g)
        pct = (lpct.get(t, 0) * w + tpct.get(t, 0) * g) / (w + g)
        out[t] = {"pct": round(pct, 1), "rate": round(rate, 2), "gp": g,
                  "lastPct": round(lpct.get(t, 0), 1), "thisPct": round(tpct.get(t, 0), 1)}
    best = sorted(out.items(), key=lambda kv: -kv[1]["pct"])[:3]
    src = "2026-27 (blended)" if any(v["gp"] for v in out.values()) else "2025-26"
    print(f"(signals) team PP ranking from {src}: best {[(t, str(v['pct']) + '%') for t, v in best]}")
    return out


# ---------- news ----------
def news(players):
    r = requests.get("https://site.api.espn.com/apis/site/v2/sports/hockey/nhl/news",
                     params={"limit": 100}, headers=HDR, timeout=30)
    r.raise_for_status()
    arts = r.json().get("articles", [])
    names = [(norm(p["n"]), str(p["id"])) for p in players if len(p["n"]) > 6]
    out = {}
    for a in arts:
        text = " " + norm((a.get("headline") or "") + " " + (a.get("description") or "")) + " "
        cats = {norm(c.get("description")) for c in a.get("categories", []) if c.get("type") == "athlete"}
        tone = "-" if any(w in text for w in NEG) else "+" if any(w in text for w in POS) else ""
        link = ((a.get("links") or {}).get("web") or {}).get("href", "")
        for n, pid in names:
            if n in cats or f" {n} " in text:
                out.setdefault(pid, []).append({"h": a.get("headline"), "d": (a.get("published") or "")[:10], "u": link, "tone": tone})
    for pid in out:
        out[pid] = out[pid][:3]
    print(f"(signals) news: {len(arts)} articles, {len(out)} players mentioned")
    return out


# ---------- injuries & return dates ----------
WORDS = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "ten": 10, "twelve": 12}
UNIT = {"day": 1, "week": 7, "month": 30}
DUR = re.compile(r"(\d+|one|two|three|four|five|six|seven|eight|ten|twelve)(?:\s*(?:-|to)\s*(\d+|two|three|four|five|six|eight|ten|twelve))?\s*(day|week|month)s?", re.I)


def injuries(players):
    r = requests.get("https://site.api.espn.com/apis/site/v2/sports/hockey/nhl/injuries", headers=HDR, timeout=30)
    r.raise_for_status()
    by = {norm(p["n"]): str(p["id"]) for p in players}
    out, n_espn, n_parsed = {}, 0, 0
    for team in r.json().get("injuries", []):
        for inj in team.get("injuries", []):
            name = ((inj.get("athlete") or {}).get("displayName") or "")
            pid = by.get(norm(name))
            if not pid:
                continue
            det = inj.get("details") or {}
            note = inj.get("shortComment") or inj.get("longComment") or ""
            back, src = (det.get("returnDate") or "")[:10], "espn"
            if not back:
                m = DUR.search(note)
                if m:
                    lo = WORDS.get(m.group(1).lower(), None) or int(m.group(1))
                    hi = m.group(2)
                    hi = (WORDS.get(hi.lower(), None) or int(hi)) if hi else lo
                    days = round((lo + hi) / 2 * UNIT[m.group(3).lower()])
                    start = (inj.get("date") or "")[:10] or datetime.now().date().isoformat()
                    back = (datetime.fromisoformat(start) + timedelta(days=days)).date().isoformat()
                    src = "parsed"
            if back:
                n_espn += src == "espn"
                n_parsed += src == "parsed"
            out[pid] = {"status": inj.get("status") or "", "back": back, "src": src,
                        "type": det.get("type") or "", "note": note[:160]}
    print(f"(signals) injuries: {len(out)} of your league's players listed, return dates: {n_espn} from ESPN, {n_parsed} from news text")
    return out

def build(players):
    out = {}
    steps = (("recent", lambda: recent(players)), ("pp1", lambda: pp1(players)), ("news", lambda: news(players)),
             ("teampp", team_pp), ("injuries", lambda: injuries(players)))
    for name, fn in steps:
        try:
            out[name] = fn()
        except Exception as ex:
            print(f"(signals) {name} failed: {type(ex).__name__}: {ex}")
    print(f"(signals) saved: {list(out.keys())}")
    return out