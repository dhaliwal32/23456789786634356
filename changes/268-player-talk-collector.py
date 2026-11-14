# changes/268-player-talk-collector.py - Player Talk step 1: gm_talk.py collects recent Reddit posts and comments about your players (free, public RSS) into talk/<id>.json every 3 hours, run from gm_notify.py

TALK = r'''"""
gm_talk.py - change 268: Player Talk (free, no AI).

For each player on your fantasy team, collects recent public Reddit posts and comments that mention him,
from Reddit's public RSS feeds (r/fantasyhockey incl. the Daily Discussion thread, r/hockey, his team's subreddit),
and saves talk/<ESPN id>.json for the app's Talk tab. Runs from gm_notify.py on every sync, but only does work
every 3 hours (talk/_state.json). Each item keeps a short piece of the post (max 240 characters) and a link to it.
Run by hand: python gm_talk.py --force
"""
import html
import json
import os
import re
import sys
import time
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone

import requests

HERE = os.path.dirname(os.path.abspath(__file__))
ESPN_JS = os.path.join(HERE, "espn-data.js")
OUT = os.path.join(HERE, "talk")
STATE = os.path.join(OUT, "_state.json")
EVERY_H = 3
KEEP_DAYS = 7
MAX_ITEMS = 25
BUDGET_S = 75
UA = "FantasyIslandsGM/1.0 (personal fantasy hockey app; github.com/dhaliwal32)"
NS = {"a": "http://www.w3.org/2005/Atom"}

SUBS = {"ANA": "AnaheimDucks", "BOS": "BostonBruins", "BUF": "sabres", "CAR": "canes", "CBJ": "BlueJackets", "CGY": "CalgaryFlames",
        "CHI": "hawks", "COL": "ColoradoAvalanche", "DAL": "DallasStars", "DET": "DetroitRedWings", "EDM": "EdmontonOilers",
        "FLA": "FloridaPanthers", "LA": "losangeleskings", "MIN": "wildhockey", "MTL": "Habs", "NJ": "devils", "NSH": "Predators",
        "NYI": "NewYorkIslanders", "NYR": "rangers", "OTT": "OttawaSenators", "PHI": "Flyers", "PIT": "penguins", "SEA": "SeattleKraken",
        "SJ": "SanJoseSharks", "STL": "stlouisblues", "TB": "TampaBayLightning", "TOR": "leafs", "UTA": "UtahHockeyClub",
        "VAN": "canucks", "VGK": "goldenknights", "WPG": "winnipegjets", "WSH": "caps"}
BOTS = {"automoderator", "sportsbot", "nhl_bot", "[deleted]"}
BAD = re.compile(r"\b(retard\w*|f[a@]g\w*|n[i1]gg\w*|kys)\b", re.I)


def log(m):
    print(f"(talk) {m}")


def now():
    return datetime.now(timezone.utc)


def load_espn():
    try:
        with open(ESPN_JS, encoding="utf-8") as f:
            body = f.read().split("=", 1)[1].strip()
        return json.loads(body[:-1] if body.endswith(";") else body)
    except Exception as ex:
        log(f"could not read espn-data.js: {ex}")
        return {}


def plain(s):
    s = re.sub(r"<[^>]+>", " ", html.unescape(s or ""))
    s = html.unescape(s)
    s = re.sub(r"submitted by\s+/u/\S+.*$", "", s, flags=re.S)
    s = re.sub(r"\[link\]|\[comments\]", "", s)
    return re.sub(r"\s+", " ", s).strip()


def norm(s):
    import unicodedata
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9 ]", " ", s.lower())


def cut(s, n=240):
    if len(s) <= n:
        return s
    s = s[:n].rsplit(" ", 1)[0]
    return s.rstrip(",.;:-") + "..."


class Feed:
    def __init__(self):
        self.s = requests.Session()
        self.s.headers["User-Agent"] = UA
        self.n = 0
        self.fails = 0
        self.t0 = time.time()

    def left(self):
        return BUDGET_S - (time.time() - self.t0)

    def get(self, url):
        if self.left() <= 0 or self.fails >= 4:
            return []
        if self.n:
            time.sleep(1.3)
        self.n += 1
        try:
            r = self.s.get(url, timeout=15)
            if r.status_code != 200:
                self.fails += 1
                log(f"{r.status_code} {url}")
                return []
            root = ET.fromstring(r.content)
        except Exception as ex:
            self.fails += 1
            log(f"failed {url}: {ex}")
            return []
        out = []
        for e in root.findall("a:entry", NS):
            g = lambda k: (e.findtext("a:" + k, default="", namespaces=NS) or "").strip()
            ln = e.find("a:link", NS)
            au = e.find("a:author/a:name", NS)
            cat = e.find("a:category", NS)
            out.append({"title": g("title"), "url": ln.get("href") if ln is not None else "", "t": g("updated") or g("published"),
                        "who": (au.text or "").replace("/u/", "").strip() if au is not None else "",
                        "sub": (cat.get("term") or "").replace("r/", "") if cat is not None else "", "body": plain(g("content"))})
        return out


def mentions(text, full, last, last_ok):
    t = " " + norm(text) + " "
    if " " + norm(full) + " " in t:
        return True
    return last_ok and (" " + norm(last) + " ") in t


def item(e, kind, src):
    who = (e.get("who") or "").lower()
    if who in BOTS:
        return None
    body = e.get("body") or ""
    title = e.get("title") or ""
    is_comment = "/comments/" in e.get("url", "") and re.search(r"/comments/\w+/[^/]*/\w+/?$", e.get("url", "")) is not None
    text = body if is_comment or not title else (title + (". " + body if body and body != title else ""))
    text = plain(text)
    if len(text) < 25 or BAD.search(text) or (text.upper() == text and len(text) > 30):
        return None
    return {"src": src, "kind": kind, "t": e.get("t", ""), "url": e.get("url", ""), "who": e.get("who", ""),
            "text": cut(text), "type": "comment" if is_comment else "post"}


def run(force=False):
    os.makedirs(OUT, exist_ok=True)
    try:
        st = json.load(open(STATE))
    except Exception:
        st = {}
    last = st.get("last")
    if not force and last and now() - datetime.fromisoformat(last) < timedelta(hours=EVERY_H):
        return
    D = load_espn()
    me = D.get("myTeamId")
    allp = D.get("players") or []
    mine = [p for p in allp if p.get("ft") == me and p.get("n")]
    if not mine:
        log("no roster players found")
        return
    # a last name alone counts only if no other NHL player in the data shares it (on his team for team subs)
    lasts = {}
    for p in allp:
        lasts.setdefault(norm(p["n"].split(" ", 1)[-1]).strip(), set()).add((p.get("t"), p["id"]))
    F = Feed()
    found = {p["id"]: [] for p in mine}
    # 1) r/fantasyhockey Daily Discussion thread comments (newest thread)
    th = F.get("https://www.reddit.com/r/fantasyhockey/search.rss?q=title%3A%22Daily%20Discussion%22&restrict_sr=on&sort=new&t=week")
    dd = []
    if th:
        u = th[0]["url"].rstrip("/")
        dd = F.get(u + "/.rss?limit=100&sort=new")
    # 2) each roster team's subreddit, newest comments
    team_c = {}
    for t in sorted({p.get("t") for p in mine}):
        if SUBS.get(t):
            team_c[t] = F.get(f"https://www.reddit.com/r/{SUBS[t]}/comments/.rss?limit=100")
    # 3) a search per player across r/fantasyhockey, r/hockey and his team's subreddit
    for p in mine:
        full, ln, t = p["n"], p["n"].split(" ", 1)[-1], p.get("t")
        uniq = len(lasts.get(norm(ln).strip(), ())) == 1
        uniq_team = len([x for x in lasts.get(norm(ln).strip(), ()) if x[0] == t]) == 1
        subs = "fantasyhockey+hockey" + ("+" + SUBS[t] if SUBS.get(t) else "")
        q = requests.utils.quote('"' + full + '"')
        for e in F.get(f"https://www.reddit.com/r/{subs}/search.rss?q={q}&restrict_sr=on&sort=new&t=week"):
            sub = e.get("sub") or ""
            it = item(e, "fan", "Reddit r/" + (sub or "hockey"))
            if it: found[p["id"]].append(it)
        for e in dd:
            if mentions(e["title"] + " " + e["body"], full, ln, uniq):
                it = item(e, "fan", "Reddit r/fantasyhockey Daily Discussion")
                if it: found[p["id"]].append(it)
        for e in team_c.get(t, []):
            if mentions(e["body"], full, ln, uniq_team):
                it = item(e, "fan", "Reddit r/" + SUBS[t])
                if it: found[p["id"]].append(it)
    if F.n and F.fails >= F.n:
        log(f"every Reddit request failed ({F.n}); keeping old files")
        return
    cutoff = now() - timedelta(days=KEEP_DAYS)
    for p in mine:
        path = os.path.join(OUT, f"{p['id']}.json")
        try:
            old = json.load(open(path)).get("items", [])
        except Exception:
            old = []
        seen, items = set(), []
        for it in found[p["id"]] + old:
            k1, k2 = it["url"], norm(it["text"])[:120]
            if k1 in seen or k2 in seen:
                continue
            try:
                if datetime.fromisoformat(it["t"].replace("Z", "+00:00")) < cutoff:
                    continue
            except Exception:
                continue
            seen.update((k1, k2))
            items.append(it)
        items.sort(key=lambda x: x["t"], reverse=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"id": p["id"], "n": p["n"], "upd": now().isoformat(timespec="seconds"), "items": items[:MAX_ITEMS]}, f, ensure_ascii=False, separators=(",", ":"))
    st["last"] = now().isoformat(timespec="seconds")
    st["req"], st["fails"] = F.n, F.fails
    json.dump(st, open(STATE, "w"))
    log(f"{len(mine)} players, {F.n} Reddit requests ({F.fails} failed), {sum(len(v) for v in found.values())} new items, {int(time.time() - F.t0)} s")


if __name__ == "__main__":
    run(force="--force" in sys.argv)
'''

def hook(t):
    return lit(t, "268: run gm_talk from the sync", "            gm_edge.run()\n        except Exception as ex:\n            print(f\"(edge probe) WARNING: {ex}\")\n",
               "            gm_edge.run()\n        except Exception as ex:\n            print(f\"(edge probe) WARNING: {ex}\")\n        try:  # change 268: player talk from Reddit\n            import gm_talk\n            gm_talk.run()\n        except Exception as ex:\n            print(f\"(talk) WARNING: {ex}\")\n",
               "change 268: player talk")

new_file("gm_talk.py", TALK)
edit("gm_notify.py", hook)
