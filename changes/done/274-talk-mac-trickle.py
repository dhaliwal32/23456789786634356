# changes/274-talk-mac-trickle.py - talk_mac.py trickle mode: one Reddit feed per run, launchd every 5 minutes, wait doubles on 429 (max 60 min), uploads at most every 30 minutes (Reddit allows only a trickle without an app key; app keys now need Reddit's review)

MAC = r'''#!/usr/bin/env python3
"""
talk_mac.py - Fantasy Islands GM, Player Talk collector that runs on Kuvar's Mac (change 270).

Reddit refuses GitHub's servers, so this runs on the Mac every 5 minutes (launchd), one feed per run from home internet.
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
DD = [None]


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
    return parse(root)


def parse(root):
    out = []
    for e in root.findall("a:entry", NS):
        g = lambda k: (e.findtext("a:" + k, default="", namespaces=NS) or "").strip()
        ln = e.find("a:link", NS)
        au = e.find("a:author/a:name", NS)
        who = (au.text or "").replace("/u/", "").strip() if au is not None else ""
        url_ = ln.get("href") if ln is not None else ""
        if url_ and re.search(r"daily discussion", g("title"), re.I) and "/comments/" in url_:
            DD[0] = DD[0] or url_  # change 274: remember the newest Daily Discussion thread
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


def slot_url(i, st):
    """change 274: one feed per run. Even turns: r/fantasyhockey (newest comments, then the Daily Discussion thread);
    odd turns: r/fantasyhockey new posts, r/hockey comments, r/hockey new posts, then each team subreddit in turn."""
    if i % 2 == 0:
        if (i // 2) % 2 == 1 and st.get("dd"):
            return "fantasyhockey", st["dd"].rstrip("/") + "/.rss?sort=new", True
        return "fantasyhockey", "https://www.reddit.com/r/fantasyhockey/comments/.rss", False
    rest = [("fantasyhockey", "new"), ("hockey", "comments"), ("hockey", "new")] + [(t, "comments") for t in TEAM_SUBS]
    sub, kind = rest[(i // 2) % len(rest)]
    return sub, f"https://www.reddit.com/r/{sub}/{kind}/.rss", False


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
    """change 274: trickle mode. launchd starts this every 5 minutes; each run reads ONE Reddit feed (Reddit refuses
    more than a trickle without an app key). On 429 the wait doubles (up to 60 min); each success shortens it again.
    Changed subreddit files go up to GitHub at most every 30 minutes."""
    os.makedirs(DATA, exist_ok=True)
    sp = os.path.join(HOME, "state.json")
    try:
        st = json.load(open(sp))
    except Exception:
        st = {}
    now = time.time()
    if now < st.get("next_ok", 0):
        return
    i = st.get("i", 0)
    sub, url, is_dd = slot_url(i, st)
    GAP[0] = 0
    code, body = fetch(url)
    gap = st.get("gap", 5)
    if code == 200:
        items = None
        try:
            root = ET.fromstring(body)
            items = parse(root)
        except Exception as ex:
            log(f"could not read {url}: {ex}")
        if items is not None:
            if is_dd:
                for it in items:
                    it["d"] = 1
            merge(sub, items)
            st.setdefault("dirty", [])
            if sub not in st["dirty"]:
                st["dirty"].append(sub)
            log(f"{sub}: {len(items)} items ({url.split('reddit.com')[-1]})")
        if DD[0] and DD[0] != st.get("dd"):
            st["dd"] = DD[0]
            log("Daily Discussion thread: " + DD[0])
        gap = max(5, gap - 1)
        st["i"] = i + 1
    elif code == 429:
        gap = min(60, gap * 2)
        log(f"429 (Reddit says slow down) on {sub}; next try in {gap} minutes")
    else:
        log(f"{code} {url}")
        st["i"] = i + 1
    st["gap"] = gap
    st["next_ok"] = now + gap * 60 - 30
    if st.get("dirty") and now - st.get("last_up", 0) >= 30 * 60:
        files, meta = {}, {}
        for sb in st["dirty"]:
            try:
                files["talk/raw/" + sb + ".json"] = open(os.path.join(DATA, sb + ".json")).read()
            except Exception:
                pass
        for fn in os.listdir(DATA):
            if fn.endswith(".json"):
                try:
                    d = json.load(open(os.path.join(DATA, fn)))
                    meta[fn[:-5]] = {"n": len(d.get("items", [])), "upd": d.get("upd")}
                except Exception:
                    pass
        files["talk/raw/_meta.json"] = json.dumps({"upd": datetime.now(timezone.utc).isoformat(timespec="seconds"), "from": "mac", "subs": meta}, separators=(",", ":"))
        if upload(files):
            log(f"uploaded {len(files) - 1} subreddit files")
            st["dirty"], st["last_up"] = [], now
    json.dump(st, open(sp, "w"))


if __name__ == "__main__":
    main()
'''

new_file("talk_mac.py", MAC)
