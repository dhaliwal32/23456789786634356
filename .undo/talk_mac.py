#!/usr/bin/env python3
"""
talk_mac.py - Fantasy Islands GM, Player Talk collector that runs on Kuvar's Mac (change 270).

Reddit refuses GitHub's servers, so this runs on the Mac every hour (launchd) from home internet.
It reads Reddit's public RSS feeds (newest comments and posts of all 32 team subreddits, r/fantasyhockey with the
Daily Discussion thread, and r/hockey), keeps the last 3 days, and uploads talk/raw/<subreddit>.json to the repo
in one commit through the GitHub API. It needs no roster: the app picks out the posts about each player itself.

The GitHub key is read from the Mac Keychain (service "fantasy-gm-talk", account "talk"); it is never in a file.
Change 273: plain requests only (short name, no limit=, Reddit gives 25 items each); refused otherwise. Runs every hour.
Change 271: one request every 7 s or slower (Reddit gave 429 at 1.5 s), team subreddits comments only (about 37 requests, 5 minutes).
Only Python's own modules are used, so nothing has to be installed.
Run by hand:  python3 ~/FantasyTalk/talk_mac.py
"""
import base64
import hashlib
import html
import json
import os
import re
import subprocess
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone

REPO = "dhaliwal32/23456789786634356"
BRANCH = "main"
HOME = os.path.join(os.path.expanduser("~"), "FantasyTalk")
DATA = os.path.join(HOME, "data")
UA = "FantasyIslandsGM/1.0"  # change 273: Reddit refuses longer names (tested on the Mac)
KEEP_DAYS = 3
MAX_ITEMS = 400
GAP_S = 5  # change 271: Reddit allows only a few requests a minute without an account
NS = {"a": "http://www.w3.org/2005/Atom"}
TEAM_SUBS = ["AnaheimDucks", "BostonBruins", "sabres", "canes", "BlueJackets", "CalgaryFlames", "hawks", "ColoradoAvalanche",
             "DallasStars", "DetroitRedWings", "EdmontonOilers", "FloridaPanthers", "losangeleskings", "wildhockey", "Habs",
             "devils", "Predators", "NewYorkIslanders", "rangers", "OttawaSenators", "Flyers", "penguins", "SeattleKraken",
             "SanJoseSharks", "stlouisblues", "TampaBayLightning", "leafs", "UtahHockeyClub", "canucks", "goldenknights",
             "winnipegjets", "caps"]
BOTS = {"automoderator", "sportsbot", "nhl_bot", "[deleted]", "gdt_bot", "nhl_gdt"}
BAD = re.compile(r"\b(retard\w*|f[a@]gg?\w*|n[i1]gg\w*|kys)\b", re.I)


def log(m):
    print(datetime.now().strftime("%Y-%m-%d %H:%M"), m, flush=True)


def plain(s):
    s = re.sub(r"<[^>]+>", " ", html.unescape(s or ""))
    s = html.unescape(s)
    s = re.sub(r"submitted by\s+/u/\S+.*$", "", s, flags=re.S)
    s = re.sub(r"\[link\]|\[comments\]", "", s)
    return re.sub(r"\s+", " ", s).strip()


def cut(s, n=300):
    if len(s) <= n:
        return s
    return s[:n].rsplit(" ", 1)[0].rstrip(",.;:-") + "..."


FAILS = [0]
GAP = [GAP_S]


def fetch(url):
    """Change 272: fetch with macOS curl. Reddit answers curl from the Mac but answers Python's own urllib with 429."""
    r = subprocess.run(["curl", "-s", "-L", "--max-time", "20", "-A", UA,
                        "-w", "\\n%{http_code}", url], capture_output=True)
    body, _, code = r.stdout.rpartition(b"\n")
    try:
        code = int(code.decode().strip() or 0)
    except ValueError:
        code = 0
    return code, body


def feed(url):
    """Reads one Reddit feed. Waits GAP seconds before each request; on "too many requests" (429) waits a minute,
    tries again and slows down for the rest of the run. Gives up on the run after 4 failures in a row."""
    if FAILS[0] >= 4:
        return None
    root = None
    for attempt in (1, 2):
        time.sleep(GAP[0] if attempt == 1 else 60)
        code, body = fetch(url)
        if code == 200:
            try:
                root = ET.fromstring(body)
                FAILS[0] = 0
            except Exception as ex:
                log(f"could not read {url}: {ex}")
            break
        if code == 429:
            GAP[0] = min(30, GAP[0] * 1.5)
            log(f"429 (Reddit says slow down), waiting a minute; now {GAP[0]:.0f} s between requests")
            continue
        log(f"{code} {url}")
        break
    if root is None:
        FAILS[0] += 1
        return None
    out = []
    for e in root.findall("a:entry", NS):
        g = lambda k: (e.findtext("a:" + k, default="", namespaces=NS) or "").strip()
        ln = e.find("a:link", NS)
        au = e.find("a:author/a:name", NS)
        who = (au.text or "").replace("/u/", "").strip() if au is not None else ""
        url_ = ln.get("href") if ln is not None else ""
        if not url_ or who.lower() in BOTS:
            continue
        title = plain(g("title"))
        body = plain(g("content"))
        is_c = re.search(r"/comments/\w+/[^/]*/\w+/?$", url_) is not None
        if is_c:
            text, head = body, re.sub(r"^/?u/\S+ on ", "", title)
        else:
            text, head = title + (". " + body if body and body != title else ""), ""
        if len(text) < 20 or BAD.search(text) or (text.upper() == text and len(text) > 30):
            continue
        out.append({"u": url_, "t": g("updated") or g("published"), "w": who, "k": "c" if is_c else "p", "h": cut(head, 120), "x": cut(text)})
    return out


def collect():
    got = {}
    def add(sub, items):
        if items is not None:
            got.setdefault(sub, []).extend(items)
    for s in ["fantasyhockey", "hockey"] + TEAM_SUBS:
        add(s, feed(f"https://www.reddit.com/r/{s}/comments/.rss"))
        if s in ("fantasyhockey", "hockey"):
            add(s, feed(f"https://www.reddit.com/r/{s}/new/.rss"))
    # newest Daily Discussion thread in r/fantasyhockey: its comments too
    q = urllib.parse.quote('title:"Daily Discussion"')
    th = feed(f"https://www.reddit.com/r/fantasyhockey/search.rss?q={q}&restrict_sr=on&sort=new&t=week") or []
    if th:
        dd = feed(th[0]["u"].rstrip("/") + "/.rss?sort=new")
        if dd:
            for it in dd:
                it["d"] = 1
            add("fantasyhockey", dd)
    return got


def merge(sub, new):
    path = os.path.join(DATA, sub + ".json")
    try:
        old = json.load(open(path)).get("items", [])
    except Exception:
        old = []
    cutoff = datetime.now(timezone.utc) - timedelta(days=KEEP_DAYS)
    seen, items = set(), []
    for it in new + old:
        key = it["u"]
        if key in seen:
            continue
        try:
            if datetime.fromisoformat(it["t"].replace("Z", "+00:00")) < cutoff:
                continue
        except Exception:
            continue
        seen.add(key)
        items.append(it)
    items.sort(key=lambda x: x["t"], reverse=True)
    body = {"sub": sub, "upd": datetime.now(timezone.utc).isoformat(timespec="seconds"), "items": items[:MAX_ITEMS]}
    json.dump(body, open(path, "w"), ensure_ascii=False, separators=(",", ":"))
    return body


def token():
    try:
        return subprocess.run(["security", "find-generic-password", "-s", "fantasy-gm-talk", "-a", "talk", "-w"],
                              capture_output=True, text=True, check=True).stdout.strip()
    except Exception:
        log("no GitHub key in the Keychain (service fantasy-gm-talk); see the setup steps")
        return ""


def gh(tok, method, path, body=None):
    req = urllib.request.Request("https://api.github.com/repos/" + REPO + path, method=method,
                                 data=json.dumps(body).encode() if body is not None else None,
                                 headers={"Authorization": "Bearer " + tok, "Accept": "application/vnd.github+json",
                                          "User-Agent": UA, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read() or b"{}")


def upload(files):
    tok = token()
    if not tok or not files:
        return False
    for attempt in range(4):
        try:
            head = gh(tok, "GET", f"/git/ref/heads/{BRANCH}")["object"]["sha"]
            base = gh(tok, "GET", f"/git/commits/{head}")["tree"]["sha"]
            tree = gh(tok, "POST", "/git/trees", {"base_tree": base, "tree": [
                {"path": p, "mode": "100644", "type": "blob", "content": c} for p, c in files.items()]})["sha"]
            com = gh(tok, "POST", "/git/commits", {"message": "talk " + datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ"),
                                                    "tree": tree, "parents": [head]})["sha"]
            gh(tok, "PATCH", f"/git/refs/heads/{BRANCH}", {"sha": com})
            return True
        except urllib.error.HTTPError as ex:
            log(f"GitHub upload try {attempt + 1}: {ex.code} {ex.read()[:200]!r}")
            if ex.code in (401, 403, 404):
                return False
            time.sleep(5)
        except Exception as ex:
            log(f"GitHub upload try {attempt + 1}: {ex}")
            time.sleep(5)
    return False


def main():
    os.makedirs(DATA, exist_ok=True)
    t0 = time.time()
    got = collect()
    if not got:
        log("Reddit gave nothing this time; nothing uploaded")
        return
    sent = {}
    try:
        sent = json.load(open(os.path.join(HOME, "sent.json")))
    except Exception:
        pass
    files, meta = {}, {}
    for sub, new in got.items():
        body = merge(sub, new)
        txt = json.dumps(body, ensure_ascii=False, separators=(",", ":"))
        h = hashlib.sha1(json.dumps(body["items"]).encode()).hexdigest()
        meta[sub] = {"n": len(body["items"]), "upd": body["upd"]}
        if sent.get(sub) != h:
            files["talk/raw/" + sub + ".json"] = txt
            sent[sub] = h
    files["talk/raw/_meta.json"] = json.dumps({"upd": datetime.now(timezone.utc).isoformat(timespec="seconds"), "from": "mac", "subs": meta}, separators=(",", ":"))
    ok = upload(files)
    if ok:
        json.dump(sent, open(os.path.join(HOME, "sent.json"), "w"))
    log(f"{len(got)} subreddits, {sum(len(v) for v in got.values())} new items, {len(files)} files {'uploaded' if ok else 'NOT uploaded'}, {int(time.time() - t0)} s")


if __name__ == "__main__":
    main()
