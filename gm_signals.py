"""
gm_signals.py - recent form, PP1 units + even-strength lines (Daily Faceoff, daily), team PP ranking,
news + injuries (ESPN, Daily Faceoff backup), ice-time trends and the luck detector (NHL stats).
Called by espn_sync.py.
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
BROWSER = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36",
           "Accept": "application/json, text/html, */*", "Accept-Language": "en-US,en;q=0.9",
           "Referer": "https://www.espn.com/", "Origin": "https://www.espn.com"}
STATS = "https://api.nhle.com/stats/rest/en"
PREV2 = "20242025"
DAYS = 14
PP_PRIOR = 5
TOI_DAYS, TOI_MIN_GP, TOI_PRIOR = 10, 3, 10
LUCK_MIN_SHOTS, LUCK_MIN_SA = 25, 150
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
       "sidelined", "placed on ir", "week-to-week", "month-to-month", "will miss", "expected to miss"]
WORDS = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "ten": 10, "twelve": 12}
UNIT = {"day": 1, "week": 7, "month": 30}
DUR = re.compile(r"(\d+|one|two|three|four|five|six|seven|eight|ten|twelve)(?:\s*(?:-|to)\s*(\d+|two|three|four|five|six|eight|ten|twelve))?\s*(day|week|month)s?", re.I)
PP_RE = re.compile(r"^(pp ?1|powerplay ?1|power ?play ?(unit )?1|1st power ?play( unit)?|first power ?play( unit)?)$", re.I)
LINE_RES = [("F1", re.compile(r"^(f ?1|forwards? ?1|1st line|first line|line ?1)$", re.I)),
            ("F2", re.compile(r"^(f ?2|forwards? ?2|2nd line|second line|line ?2)$", re.I)),
            ("D1", re.compile(r"^(d ?1|defen[cs]e ?(pair(ing)? ?)?1|1st pair(ing)?|first pair(ing)?|pair(ing)? ?1)$", re.I)),
            ("D2", re.compile(r"^(d ?2|defen[cs]e ?(pair(ing)? ?)?2|2nd pair(ing)?|second pair(ing)?|pair(ing)? ?2)$", re.I))]
NAME_KEYS = ("playerName", "name", "fullName", "player_name")


# ---------- helpers ----------
def next_data(url):
    html = requests.get(url, headers=BROWSER, timeout=30).text
    m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html, re.S)
    return json.loads(m.group(1)) if m else None


def first_json(urls):
    last = None
    for u in urls:
        try:
            r = requests.get(u, headers=BROWSER, timeout=30)
            r.raise_for_status()
            return r.json()
        except Exception as ex:
            last = ex
    raise last or RuntimeError("no source")


def duration_back(text, start):
    m = DUR.search(text or "")
    if not m:
        return ""
    lo = WORDS.get(m.group(1).lower()) or int(m.group(1))
    hi = m.group(2)
    hi = (WORDS.get(hi.lower()) or int(hi)) if hi else lo
    days = round((lo + hi) / 2 * UNIT[m.group(3).lower()])
    try:
        base = datetime.fromisoformat((start or "")[:10])
    except Exception:
        base = datetime.now()
    return (base + timedelta(days=days)).date().isoformat()


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


def find_group(obj, rx, out):
    if isinstance(obj, dict):
        if any(isinstance(v, str) and rx.match(v.strip()) for v in obj.values()):
            names_in(obj, out)
        for v in obj.values():
            find_group(v, rx, out)
    elif isinstance(obj, list):
        for v in obj:
            find_group(v, rx, out)


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


# ---------- Daily Faceoff: PP1 units + even-strength lines (read once a day) ----------
def df_lines(players):
    today = datetime.now().date().isoformat()
    cache = {}
    if os.path.exists(PP_CACHE):
        with open(PP_CACHE, encoding="utf-8") as f:
            cache = json.load(f)
    if cache.get("date") != today or "lines" not in cache:
        new_day = cache.get("date") != today
        units, lines = {}, {}
        for t, slug in SLUGS.items():
            try:
                data = next_data(f"https://www.dailyfaceoff.com/teams/{slug}/line-combinations")
                pp, grp = set(), {}
                if data:
                    find_group(data, PP_RE, pp)
                    for lab, rx in LINE_RES:
                        names = set()
                        find_group(data, rx, names)
                        ok = (2 <= len(names) <= 4) if lab[0] == "F" else (2 <= len(names) <= 3)
                        if ok:
                            grp[lab] = sorted(names)
                units[t] = sorted(pp) if 3 <= len(pp) <= 8 else cache.get("units", {}).get(t, [])
                lines[t] = grp or cache.get("lines", {}).get(t, {})
            except Exception:
                units[t] = cache.get("units", {}).get(t, [])
                lines[t] = cache.get("lines", {}).get(t, {})
        cache = {"date": today,
                 "prev": cache.get("units", {}) if new_day else cache.get("prev", {}),
                 "units": units,
                 "prev_lines": cache.get("lines", {}) if new_day else cache.get("prev_lines", {}),
                 "lines": lines}
        with open(PP_CACHE, "w", encoding="utf-8") as f:
            json.dump(cache, f)
    return cache


def pp1(players, cache):
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
    print(f"(signals) PP1: {sum(1 for v in units.values() if v)}/32 teams read, {len(on)} players on PP1, {len(chg)} changes vs last day")
    return {"asof": cache.get("date"), "on": on, "changes": chg, "units": units}


def lines(players, cache):
    cur, prev = cache.get("lines", {}), cache.get("prev_lines", {})
    by = {norm(p["n"]): p for p in players}
    top, chg = {}, {}
    for t, groups in cur.items():
        now_top = {norm(n): lab for lab, names in groups.items() for n in names}
        pg = prev.get(t) or {}
        before_top = {norm(n) for names in pg.values() for n in names}
        for n, lab in now_top.items():
            p = by.get(n)
            if p:
                top[str(p["id"])] = lab
                if pg and n not in before_top:
                    chg[str(p["id"])] = "up"
        if pg:
            for n in before_top - set(now_top):
                p = by.get(n)
                if p and p["t"] == t and (p.get("status") or "ACTIVE") in ("ACTIVE", ""):
                    chg[str(p["id"])] = "down"
    teams_ok = sum(1 for g in cur.values() if g)
    ups = sum(1 for v in chg.values() if v == "up")
    print(f"(signals) lines: {teams_ok}/32 teams read, {len(top)} top-6 F / top-4 D players, {ups} promoted, {len(chg) - ups} demoted vs last day")
    return {"asof": cache.get("date"), "top": top, "changes": chg}


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
    out = {}
    for t in set(lgp) | set(tgp):
        g = tgp.get(t, 0)
        last_rate = lpts.get(t, 0) / max(1, lgp.get(t, 82))
        this_rate = tpts.get(t, 0) / g if g else 0
        w = PP_PRIOR if g else 1
        out[t] = {"pct": round((lpct.get(t, 0) * w + tpct.get(t, 0) * g) / (w + g), 1),
                  "rate": round((last_rate * w + this_rate * g) / (w + g), 2), "gp": g,
                  "lastPct": round(lpct.get(t, 0), 1), "thisPct": round(tpct.get(t, 0), 1)}
    best = sorted(out.items(), key=lambda kv: -kv[1]["pct"])[:3]
    src = "2026-27 (blended)" if any(v["gp"] for v in out.values()) else "2025-26"
    print(f"(signals) team PP ranking from {src}: best {[(t, str(v['pct']) + '%') for t, v in best]}")
    return out


# ---------- news (ESPN, backup: Daily Faceoff player news) ----------
def _df_items():
    data = next_data("https://www.dailyfaceoff.com/hockey-player-news")
    items = []

    def walk(o):
        if isinstance(o, dict):
            title = next((v for k, v in o.items() if isinstance(v, str) and any(w in k.lower() for w in ("title", "headline"))), None)
            if title and len(title) > 15:
                body = " ".join(v for k, v in o.items() if isinstance(v, str) and any(w in k.lower() for w in ("detail", "description", "summary", "content", "body", "news")))
                date = next((v for k, v in o.items() if isinstance(v, str) and any(w in k.lower() for w in ("date", "created", "published"))), "")
                slug = next((v for k, v in o.items() if isinstance(v, str) and k.lower() in ("slug", "url", "link")), "")
                url = slug if slug.startswith("http") else (f"https://www.dailyfaceoff.com/hockey-player-news/{slug}" if slug else "https://www.dailyfaceoff.com/hockey-player-news")
                items.append({"title": title, "text": title + " " + re.sub(r"<[^>]+>", " ", body), "date": date[:10], "url": url})
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    if data:
        walk(data)
    return items


def news(players):
    names = [(norm(p["n"]), str(p["id"])) for p in players if len(p["n"]) > 6]
    out, src = {}, "ESPN"
    try:
        js = first_json(["https://site.api.espn.com/apis/site/v2/sports/hockey/nhl/news?limit=100",
                         "https://site.web.api.espn.com/apis/site/v2/sports/hockey/nhl/news?limit=100",
                         "https://now.core.api.espn.com/v1/sports/news?sport=hockey&league=nhl&limit=100"])
        arts = js.get("articles") or js.get("headlines") or []
        items = [{"title": a.get("headline") or "", "text": (a.get("headline") or "") + " " + (a.get("description") or ""),
                  "date": (a.get("published") or "")[:10], "url": ((a.get("links") or {}).get("web") or {}).get("href", ""),
                  "cats": {norm(c.get("description")) for c in a.get("categories", []) if c.get("type") == "athlete"}} for a in arts]
    except Exception:
        src = "Daily Faceoff"
        items = [dict(i, cats=set()) for i in _df_items()]
    for it in items:
        text = " " + norm(it["text"]) + " "
        tone = "-" if any(w in text for w in NEG) else "+" if any(w in text for w in POS) else ""
        for n, pid in names:
            if n in it["cats"] or f" {n} " in text:
                out.setdefault(pid, []).append({"h": it["title"], "d": it["date"], "u": it["url"], "tone": tone})
    for pid in out:
        out[pid] = out[pid][:3]
    print(f"(signals) news from {src}: {len(items)} items, {len(out)} players mentioned")
    return out


# ---------- injuries & return dates ----------
def injuries(players):
    by = {norm(p["n"]): str(p["id"]) for p in players}
    out, n_espn, n_parsed, src = {}, 0, 0, "ESPN"
    try:
        js = first_json(["https://site.api.espn.com/apis/site/v2/sports/hockey/nhl/injuries",
                         "https://site.web.api.espn.com/apis/site/v2/sports/hockey/nhl/injuries"])
        for team in js.get("injuries", []):
            for inj in team.get("injuries", []):
                pid = by.get(norm((inj.get("athlete") or {}).get("displayName") or ""))
                if not pid:
                    continue
                det = inj.get("details") or {}
                note = inj.get("shortComment") or inj.get("longComment") or ""
                back, how = (det.get("returnDate") or "")[:10], "espn"
                if not back:
                    back, how = duration_back(note, inj.get("date")), "parsed"
                n_espn += bool(back) and how == "espn"
                n_parsed += bool(back) and how == "parsed"
                out[pid] = {"status": inj.get("status") or "", "back": back, "src": how, "type": det.get("type") or "", "note": note[:160]}
    except Exception:
        src = "Daily Faceoff news"
        for it in _df_items():
            text = " " + norm(it["text"]) + " "
            if not any(w in text for w in NEG):
                continue
            for n, pid in by.items():
                if len(n) > 6 and f" {n} " in text and pid not in out:
                    back = duration_back(it["text"], it["date"])
                    n_parsed += bool(back)
                    out[pid] = {"status": "", "back": back, "src": "parsed", "type": "", "note": it["title"][:160]}
    print(f"(signals) injuries from {src}: {len(out)} players, return dates: {n_espn} from ESPN, {n_parsed} from news text")
    return out


# ---------- ice time trends ----------
def toi_rows(exp):
    r = requests.get(f"{STATS}/skater/timeonice", params={"limit": -1, "cayenneExp": exp}, headers=HDR, timeout=60)
    r.raise_for_status()
    out = {}
    for x in r.json().get("data", []):
        grp = "D" if x.get("positionCode") == "D" else "F"
        out[(norm(x.get("skaterFullName")), grp)] = {"gp": x.get("gamesPlayed") or 0,
                                                     "toi": x.get("timeOnIcePerGame") or 0,
                                                     "pp": x.get("ppTimeOnIcePerGame") or 0}
    return out


def toi(players):
    end = datetime.now().date()
    start = end - timedelta(days=TOI_DAYS)
    rec = toi_rows(f'seasonId={THIS} and gameTypeId=2 and gameDate<="{end} 23:59:59" and gameDate>="{start}"')
    cur = toi_rows(f"seasonId={THIS} and gameTypeId=2")
    last = toi_rows(f"seasonId={LAST} and gameTypeId=2")
    out, ups, downs = {}, 0, 0
    for p in players:
        if p["p"] == "G":
            continue
        k = (norm(p["n"]), "D" if p["p"] == "D" else "F")
        r = rec.get(k)
        if not r or r["gp"] < TOI_MIN_GP:
            continue
        c = cur.get(k, {"gp": 0, "toi": 0, "pp": 0})
        l = last.get(k)
        before = c["gp"] - r["gp"]
        tb = (c["toi"] * c["gp"] - r["toi"] * r["gp"]) / before if before > 0 else 0
        pb = (c["pp"] * c["gp"] - r["pp"] * r["gp"]) / before if before > 0 else 0
        w = TOI_PRIOR if l and l["gp"] else 0
        if w + before == 0:
            continue
        base = ((l["toi"] if l else 0) * w + tb * before) / (w + before)
        pbase = ((l["pp"] if l else 0) * w + pb * before) / (w + before)
        d, pd = r["toi"] - base, r["pp"] - pbase
        out[str(p["id"])] = {"r": round(r["toi"]), "b": round(base), "d": round(d),
                             "pr": round(r["pp"]), "pb": round(pbase), "pd": round(pd), "gp": r["gp"]}
        ups += d >= 120
        downs += d <= -120
    print(f"(signals) ice time: {len(out)} players tracked, {ups} up 2+ min, {downs} down 2+ min (last {TOI_DAYS} days)")
    return out


# ---------- luck detector ----------
def luck(players):
    def sk(season):
        out = {}
        for r in stats("skater/summary", season):
            grp = "D" if r.get("positionCode") == "D" else "F"
            out[(norm(r.get("skaterFullName")), grp)] = (r.get("goals") or 0, r.get("shots") or 0)
        return out

    def go(season):
        return {norm(r.get("goalieFullName")): (r.get("saves") or 0, r.get("shotsAgainst") or 0) for r in stats("goalie/summary", season)}

    cur, l1, l2 = sk(THIS), sk(LAST), sk(PREV2)
    gc, g1, g2 = go(THIS), go(LAST), go(PREV2)
    out = {}
    for p in players:
        key = norm(p["n"])
        if p["p"] == "G":
            c = gc.get(key)
            if not c or c[1] < LUCK_MIN_SA:
                continue
            sv = sum(x.get(key, (0, 0))[0] for x in (g1, g2))
            sa = sum(x.get(key, (0, 0))[1] for x in (g1, g2))
            career = (sv + 0.900 * 1500) / (sa + 1500)
            out[str(p["id"])] = {"t": "g", "sv": round(c[0] / c[1], 3), "csv": round(career, 3),
                                 "d": round(c[0] - career * c[1], 1), "sa": c[1]}
        else:
            k = (key, "D" if p["p"] == "D" else "F")
            c = cur.get(k)
            if not c or c[1] < LUCK_MIN_SHOTS:
                continue
            g = sum(x.get(k, (0, 0))[0] for x in (l1, l2))
            s = sum(x.get(k, (0, 0))[1] for x in (l1, l2))
            prior = 0.045 if p["p"] == "D" else 0.105
            career = (g + prior * 100) / (s + 100)
            out[str(p["id"])] = {"t": "s", "g": c[0], "sh": c[1], "pct": round(100 * c[0] / c[1], 1),
                                 "cpct": round(100 * career, 1), "xg": round(career * c[1], 1),
                                 "d": round(c[0] - career * c[1], 1)}
    hi = sum(1 for v in out.values() if v["d"] >= (2 if v["t"] == "s" else 4))
    lo = sum(1 for v in out.values() if v["d"] <= (-2 if v["t"] == "s" else -4))
    print(f"(signals) luck: {len(out)} players with enough shots, {hi} running lucky, {lo} running unlucky")
    return out
# ---------- automatic goalie start share ----------
GS_DAYS = 21      # about the last 10 team games
GS_PRIOR = 6      # last season's share counts like 6 games


def gstart(players):
    end = datetime.now().date()
    start = end - timedelta(days=GS_DAYS)
    exp = f'seasonId={THIS} and gameTypeId=2 and gameDate<="{end} 23:59:59" and gameDate>="{start}"'
    r = requests.get(f"{STATS}/team/summary", params={"limit": -1, "cayenneExp": exp}, headers=HDR, timeout=60)
    r.raise_for_status()
    team_g = {}
    for x in r.json().get("data", []):
        c = team_code(x.get("teamFullName"))
        if c:
            team_g[c] = x.get("gamesPlayed") or 0
    recent_st = {}
    for x in get_stats("goalie/summary", start, end):
        recent_st[norm(x.get("goalieFullName"))] = (x.get("gamesStarted") or 0, ab((x.get("teamAbbrevs") or "").split(",")[-1].strip()))
    last = {norm(x.get("goalieFullName")): (x.get("gamesStarted") or 0, ab((x.get("teamAbbrevs") or "").split(",")[-1].strip()))
            for x in stats("goalie/summary", LAST)}
    last_gp = {}
    for x in stats("team/summary", LAST):
        c = team_code(x.get("teamFullName"))
        if c:
            last_gp[c] = x.get("gamesPlayed") or 82
    out, flags = {}, 0
    for p in players:
        if p["p"] != "G":
            continue
        key, t = norm(p["n"]), p["t"]
        g = team_g.get(t, 0)
        if g < 3:                                   # wait until the team has played 3 games
            continue
        st, st_team = recent_st.get(key, (0, t))
        starts = st if st_team == t else 0
        l = last.get(key)
        prior = l[0] / max(1, last_gp.get(l[1], 82)) if l and l[1] == t else None
        pr = prior if prior is not None else 0.5
        share = max(0.05, min(0.95, (starts + pr * GS_PRIOR) / (g + GS_PRIOR)))
        flag = g >= 5 and abs(starts / g - pr) >= 0.25
        flags += flag
        out[str(p["id"])] = {"share": round(share, 2), "rs": starts, "rg": g, "prior": round(pr, 2), "flag": flag}
    print(f"(signals) goalie starts: {len(out)} goalies with an automatic start %, {flags} with a big change in who starts")
    return out

def build(players):
    out = {}
    try:
        cache = df_lines(players)
    except Exception as ex:
        print(f"(signals) Daily Faceoff lines failed: {type(ex).__name__}: {ex}")
        cache = {}
    steps = (("recent", lambda: recent(players)), ("pp1", lambda: pp1(players, cache)), ("lines", lambda: lines(players, cache)),
             ("news", lambda: news(players)), ("teampp", team_pp), ("injuries", lambda: injuries(players)),
             ("toi", lambda: toi(players)), ("luck", lambda: luck(players)), ("gstart", lambda: gstart(players)))
    for name, fn in steps:
        try:
            out[name] = fn()
        except Exception as ex:
            print(f"(signals) {name} failed: {type(ex).__name__}: {ex}")
    print(f"(signals) saved: {list(out.keys())}")
    return out
