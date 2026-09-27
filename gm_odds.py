"""
gm_odds.py - NHL betting odds (The Odds API) -> win probability and expected goals
for each team in each game. Cached for 4 hours to stay inside the free plan
(500 credits/month; each download costs 2 credits).
"""
import json
import os
from datetime import datetime, timezone, timedelta
from statistics import median
from zoneinfo import ZoneInfo
import requests

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "odds_cache.json")
REFRESH_HOURS = 4
ET = ZoneInfo("America/New_York")
URL = "https://api.the-odds-api.com/v4/sports/icehockey_nhl/odds/"


def _key():
    k = os.environ.get("ODDS_API_KEY", "").strip()
    if not k:
        try:
            from secrets_local import ODDS_API_KEY
            k = ODDS_API_KEY.strip()
        except Exception:
            pass
    return k


def _parse(events, team_code):
    out = {}
    for ev in events:
        h, a = team_code(ev.get("home_team")), team_code(ev.get("away_team"))
        if not h or not a:
            continue
        day = datetime.fromisoformat(ev["commence_time"].replace("Z", "+00:00")).astimezone(ET).date().isoformat()
        wins, totals = [], []
        for bk in ev.get("bookmakers", []):
            for m in bk.get("markets", []):
                outs = m.get("outcomes", [])
                if m.get("key") == "h2h":
                    pr = {o.get("name"): o.get("price") for o in outs}
                    hp, ap = pr.get(ev["home_team"]), pr.get(ev["away_team"])
                    if hp and ap:
                        ih, ia = 1 / hp, 1 / ap
                        wins.append(ih / (ih + ia))           # remove the bookmaker's margin
                elif m.get("key") == "totals":
                    ov = next((o for o in outs if o.get("name") == "Over"), None)
                    un = next((o for o in outs if o.get("name") == "Under"), None)
                    if ov and un and ov.get("point") is not None:
                        io, iu = 1 / ov["price"], 1 / un["price"]
                        totals.append(ov["point"] + (io / (io + iu) - 0.5) * 1.2)
        if not wins:
            continue
        pw = median(wins)
        total = median(totals) if totals else 6.0
        share = 0.5 + (pw - 0.5) * 0.55                     # stronger team gets more of the goals
        gh, gaw = total * share, total * (1 - share)
        out.setdefault(day, {})[h] = {"win": round(pw, 3), "gf": round(gh, 2), "ga": round(gaw, 2), "opp": a, "home": True}
        out.setdefault(day, {})[a] = {"win": round(1 - pw, 3), "gf": round(gaw, 2), "ga": round(gh, 2), "opp": h, "home": False}
    return out


def get_odds(team_code):
    cache = {}
    if os.path.exists(CACHE):
        try:
            with open(CACHE, encoding="utf-8") as f:
                cache = json.load(f)
        except Exception:
            cache = {}
    now = datetime.now(timezone.utc)
    fresh = cache.get("fetched") and now - datetime.fromisoformat(cache["fetched"]) < timedelta(hours=REFRESH_HOURS)
    if not fresh:
        key = _key()
        if not key:
            print("(odds) no ODDS_API_KEY - using team-strength estimates instead")
            return cache.get("games", {})
        try:
            r = requests.get(URL, params={"apiKey": key, "regions": "us", "markets": "h2h,totals",
                                          "oddsFormat": "decimal"}, timeout=30)
            r.raise_for_status()
            games = _parse(r.json(), team_code)
            today = datetime.now(ET).date().isoformat()
            games = {d: v for d, v in games.items() if d >= today}
            cache = {"fetched": now.isoformat(), "games": games}
            with open(CACHE, "w", encoding="utf-8") as f:
                json.dump(cache, f)
            n = sum(len(v) for v in games.values()) // 2
            print(f"(odds) downloaded odds for {n} games - API credits left this month: {r.headers.get('x-requests-remaining')}")
        except Exception as ex:
            print(f"(odds) download failed: {ex}")
            return cache.get("games", {})
    else:
        n = sum(len(v) for v in cache.get("games", {}).values()) // 2
        print(f"(odds) using saved odds from {cache['fetched'][:16]} UTC ({n} games)")
    return cache.get("games", {})
