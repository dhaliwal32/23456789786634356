"""
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
    try:  # change 278: the same alert also goes to the home-screen app
        import gm_push
        gm_push.send(title, msg, "#matchup")
    except Exception as e:
        log("app alert failed", e)
    if True:  # change 284: ntfy switched off (Kuvar, Nov 14, 2026); alerts go only to the app. Delete these two lines to bring ntfy back.
        return
    if not NTFY_TOPIC:
        log("(no ntfy topic)", title, msg)
        return
    try:
        requests.post(f"https://ntfy.sh/{NTFY_TOPIC}", data=msg.encode("utf-8"),
                      headers={"Title": title, "Priority": "default"}, timeout=20)  # change 261: no Click link, tapping opens ntfy
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


def push_onice():
    """change 205: fill who was on the ice for new goals and commit it, so the app shows it within a minute or two"""
    try:
        import subprocess
        import gm_onice
        if not gm_onice.update("edge/onice-live.json", 20, live_only=True):
            return
        run = lambda *a: subprocess.run(["git", *a], cwd=HERE, capture_output=True, text=True)
        run("config", "user.name", "fantasy-bot")
        run("config", "user.email", "fantasy-bot@users.noreply.github.com")
        run("add", "edge/onice-live.json")
        run("add", "edge/onice-sent311.json")  # change 311: goal alerts already sent
        if run("diff", "--cached", "--quiet").returncode == 0:
            return
        run("commit", "-q", "-m", "on ice " + datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ"))
        for _ in range(4):
            if run("pull", "-q", "--rebase", "-X", "theirs").returncode == 0 and run("push", "-q").returncode == 0:
                log("on ice saved")
                return
            run("rebase", "--abort")
            time.sleep(5)
        log("on ice: push failed (does live-alerts.yml have contents: write?)")
        run("reset", "-q", "--hard", "origin/main")
    except Exception as e:
        log("on ice failed", e)


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
                    push("Fantasy GM", f"You lead {a:.1f} to {b:.1f}")
                else:
                    push("Fantasy GM", f"{them} lead {b:.1f} to {a:.1f}")
                log("lead change", a, b)
                last = side
            elif side != 0:
                last = side
        push_onice()  # change 205
        try:
            goal_alerts302(sc[2] if sc else None)  # change 302
        except Exception as e:
            log("goal alerts failed", e)
        time.sleep(EVERY)


# ---------- change 302: a phone alert for every goal and assist by your opponent's players ----------
SB302 = "https://site.api.espn.com/apis/site/v2/sports/hockey/nhl/"
_seen302, _primed302, _opp302 = set(), False, {"id": None, "ids": set(), "at": 0}


def _opp_ids302(opp):
    """the opponent's player ids, read again every 20 minutes"""
    if opp != _opp302["id"] or time.time() - _opp302["at"] > 1200:
        try:
            r = s.get(LEAGUE, params=[("view", "mRoster"), ("forTeamId", opp)], timeout=30).json()
            t = next((x for x in r.get("teams", []) if x.get("id") == opp), {})
            _opp302.update({"id": opp, "ids": {e.get("playerId") for e in (t.get("roster") or {}).get("entries", [])}, "at": time.time()})
        except Exception as e:
            log("opponent roster failed", e)
    return _opp302["ids"]


def _count302(text, name, goal):
    import re as _re
    if goal:
        m = _re.search(r"Goal \((\d+)\)", text or "")
    else:
        m = _re.search(_re.escape(name) + r" \((\d+)\)", text or "")
    return f" ({m.group(1)})" if m else ""


# ---------- change 311: remember sent goal alerts, catch goals scored before the watcher started ----------
SENT311 = os.path.join(HERE, "edge", "onice-sent311.json")
_sent_cache311 = None


def _sent311():
    global _sent_cache311
    if _sent_cache311 is None:
        try:
            with open(SENT311) as f:
                _sent_cache311 = set(json.load(f).get("keys", []))
        except Exception:
            _sent_cache311 = set()
    return _sent_cache311


def _mark311(key):
    k = _sent311()
    k.add(key)
    try:
        with open(SENT311, "w") as f:
            json.dump({"keys": sorted(k)[-400:]}, f)
    except Exception as e:
        log("could not save sent alerts", e)


def _recent311(wc):
    try:
        t = datetime.strptime(str(wc)[:19], "%Y-%m-%dT%H:%M:%S").replace(tzinfo=timezone.utc)
        return (datetime.now(timezone.utc) - t).total_seconds() < 3 * 3600
    except Exception:
        return False


def goal_alerts302(opp):
    global _primed302
    if not opp:
        return
    ids = _opp_ids302(opp)
    if not _primed302:
        log(f"goal alerts: opponent {opp}, {len(ids)} players")  # change 311
    if not ids:
        return
    try:
        sb = requests.get(SB302 + "scoreboard", timeout=20).json()
    except Exception as e:
        log("goal check failed", e)
        return
    for ev in sb.get("events", []):
        st = (((ev.get("status") or {}).get("type")) or {}).get("state")
        if st not in ("in", "post"):
            continue
        try:
            sm = requests.get(SB302 + "summary", params={"event": ev.get("id")}, timeout=20).json()
        except Exception:
            continue
        for p in sm.get("plays") or []:
            if not p.get("scoringPlay") or ((p.get("period") or {}).get("number") or 0) >= 5:
                continue          # shootout goals do not count
            for q in p.get("participants") or []:
                a = q.get("athlete") or {}
                try:
                    pid = int(a.get("id"))
                except Exception:
                    continue
                kind = q.get("type")
                if pid not in ids or kind not in ("scorer", "assister"):
                    continue
                key = f"{p.get('id')}|{pid}"
                if key in _seen302:
                    continue
                _seen302.add(key)
                if not _primed302 and (key in _sent311() or not _recent311(p.get("wallclock"))):
                    continue          # change 311: before this run started, only goals from the last 3 hours not already sent
                name = a.get("displayName") or a.get("fullName") or ""
                goal = kind == "scorer"
                msg = ("Goal by " if goal else "Assist by ") + name + _count302(p.get("text"), name, goal)
                try:
                    import gm_push
                    gm_push.send("\U0001F3D2 Fantasy Islands", msg, "#matchup")  # change 311: title back (no title showed the name twice)
                    _mark311(key)
                except Exception as e:
                    log("goal alert failed", e)
                log("goal alert:", msg)
    _primed302 = True


if __name__ == "__main__":
    main()
