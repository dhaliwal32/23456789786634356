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
    if not NTFY_TOPIC:
        log("(no ntfy topic)", title, msg)
        return
    try:
        requests.post(f"https://ntfy.sh/{NTFY_TOPIC}", data=msg.encode("utf-8"),
                      headers={"Title": title, "Priority": "default", "Click": APP_URL}, timeout=20)
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
        time.sleep(EVERY)


if __name__ == "__main__":
    main()
