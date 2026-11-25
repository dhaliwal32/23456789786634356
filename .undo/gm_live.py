"""
gm_live.py - watches your matchup during NHL games: goal and assist alerts for the other team's players
(from the NHL live feed, change 318) and who was on the ice for each goal. Runs on GitHub (live-alerts.yml)
and stops by itself after the day's last game. Lead-change alerts are off (change 317).
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
APP_URL = "https://dhaliwal32.github.io/23456789786634356/fantasy-gm.html#matchup"
LEAGUE = f"https://lm-api-reads.fantasy.espn.com/apis/v3/games/fhl/seasons/{SEASON}/segments/0/leagues/{LEAGUE_ID}"
HERE = os.path.dirname(os.path.abspath(__file__))
MAX_RUN = 5.6 * 3600  # GitHub stops a job after 6 hours

s = requests.Session()
s.headers.update({"User-Agent": "Mozilla/5.0"})
s.cookies.update({"espn_s2": ESPN_S2, "SWID": SWID})


def log(*a):
    print(datetime.now(timezone.utc).strftime("%H:%M:%S"), *a, flush=True)


def push(title, msg):
    try:  # change 278: the same alert also goes to the home-screen app
        import gm_push
        gm_push.send(msg, "", "#matchup")  # change 315: two lines, message on top then "from <app>" (Kuvar picked this; iOS always needs a top line)
    except Exception as e:
        log("app alert failed", e)


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
        if not gm_onice.update("edge/onice-live.json", 20, live_only=True) and not _dirty321[0]:
            return
        _dirty321[0] = False
        run = lambda *a: subprocess.run(["git", *a], cwd=HERE, capture_output=True, text=True)
        run("config", "user.name", "fantasy-bot")
        run("config", "user.email", "fantasy-bot@users.noreply.github.com")
        run("add", "edge/onice-live.json")
        run("add", "edge/onice-sent311.json")  # change 311: goal alerts already sent
        run("add", "edge/alert-times.json")  # change 321: when every alert went out
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
            if nxt is None:  # change 312: stay on between games (GitHub's schedule can start it hours late); stop after the last one
                log("no game live and none left today - stopping")
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
                if True:  # change 317: lead alerts off (Kuvar, Nov 17); delete this line and the "pass" under it, and change the next "elif" to "if", to bring them back
                    pass
                elif side > 0:
                    push("Fantasy GM", f"You lead {a:.1f} to {b:.1f}")
                else:
                    push("Fantasy GM", f"{them} lead {b:.1f} to {a:.1f}")
                log("lead change", a, b)
                last = side
            elif side != 0:
                last = side
        alerts322(sc[2] if sc else None)  # change 322: start the alert track before the slow on-ice step
        push_onice()  # change 205
        alerts322(sc[2] if sc else None)  # change 322: goal alerts run on their own track (every 2 s), never held up by the steps above
        time.sleep(20)


# ---------- change 302: a phone alert for every goal and assist by your opponent's players ----------
_opp302 = {"id": None, "ids": set(), "at": 0}  # the opponent's roster (change 302, names added in 318)


def _opp_ids302(opp):
    """the opponent's player ids, read again every 20 minutes"""
    if opp != _opp302["id"] or time.time() - _opp302["at"] > 1200:
        try:
            r = s.get(LEAGUE, params=[("view", "mRoster"), ("forTeamId", opp)], timeout=30).json()
            t = next((x for x in r.get("teams", []) if x.get("id") == opp), {})
            ents = (t.get("roster") or {}).get("entries", [])
            _opp302.update({"id": opp, "ids": {e.get("playerId") for e in ents}, "at": time.time(),  # change 318: names too, to match the NHL feed
                            "names": {e.get("playerId"): (((e.get("playerPoolEntry") or {}).get("player") or {}).get("fullName") or "") for e in ents}})
        except Exception as e:
            log("opponent roster failed", e)
    return _opp302["ids"]


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


_order321 = []  # change 321: sent keys in the order they happened


def _mark311(key):
    k = _sent311()
    if not _order321:
        try:
            with open(SENT311) as f:
                _order321.extend(json.load(f).get("keys", []))
        except Exception:
            pass
    k.add(key)
    if key not in _order321:
        _order321.append(key)
    try:
        with open(SENT311, "w") as f:
            json.dump({"keys": [x for x in _order321[-3000:] if x in k] or sorted(k)[-3000:]}, f)  # change 321: newest 3000 kept
    except Exception as e:
        log("could not save sent alerts", e)


# ---------- change 318: goal / assist alerts from the NHL's own live feed (faster than ESPN) ----------
NHL318 = "https://api-web.nhle.com/v1/"
UA318 = {"User-Agent": "Mozilla/5.0"}
SEED318 = "zz-nhl318"  # in the sent file: goals already on the board when the NHL feed first ran were alerted by the old ESPN path
_tot318, _hot318, _boot318 = {}, {}, {"done": False}
_read320 = {}  # change 320: when each game was last read


def _norm318(x):
    import unicodedata
    x = unicodedata.normalize("NFKD", str(x or "")).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z ]", "", x).strip()


def _match318(full, names):
    """ESPN player id for an NHL name: the same full name, or the same first letter and last name if only one player fits"""
    n = _norm318(full)
    if not n:
        return None
    hit = [pid for pid, nm in names.items() if _norm318(nm) == n]
    if len(hit) == 1:
        return hit[0]
    last = n.split()[-1]
    hit = [pid for pid, nm in names.items() if _norm318(nm).split()[-1:] == [last] and _norm318(nm)[:1] == n[:1]]
    return hit[0] if len(hit) == 1 else None


def nhl_goals318(opp):
    """one look at the NHL feed: alert each new goal or assist by the opponent's players"""
    ids = _opp_ids302(opp)
    names = {pid: nm for pid, nm in (_opp302.get("names") or {}).items() if pid in ids and nm}
    if not names:
        return
    sc = requests.get(NHL318 + "score/now", headers=UA318, timeout=10).json()
    seed, now = SEED318 not in _sent311(), time.time()
    for g in sc.get("games", []):
        if g.get("gameState") not in ("LIVE", "CRIT", "OFF", "FINAL"):
            continue
        gid = g.get("id")
        tot = ((g.get("awayTeam") or {}).get("score") or 0) + ((g.get("homeTeam") or {}).get("score") or 0)
        if tot != _tot318.get(gid):
            _tot318[gid] = tot
            _hot318[gid] = now + 240  # a new goal: read this game every pass for 4 minutes (assists are often added late)
        live320 = g.get("gameState") in ("LIVE", "CRIT")
        if _boot318["done"] and now > _hot318.get(gid, 0) and not (live320 and now - _read320.get(gid, 0) >= 30):
            continue  # change 320: a live game is still re-read every 30 s, so a late assist is never stuck until the next goal
        _read320[gid] = now
        try:
            pbp = requests.get(f"{NHL318}gamecenter/{gid}/play-by-play", headers=UA318, timeout=10).json()
        except Exception as e:
            log("NHL game read failed", gid, e)
            continue
        who = {r.get("playerId"): ((r.get("firstName") or {}).get("default", "") + " " + (r.get("lastName") or {}).get("default", "")).strip()
               for r in pbp.get("rosterSpots") or []}
        for p in pbp.get("plays") or []:
            if p.get("typeDescKey") != "goal" or (p.get("periodDescriptor") or {}).get("periodType") == "SO":
                continue  # shootout goals do not count
            d = p.get("details") or {}
            for f, kind in (("scoringPlayer", "Goal"), ("assist1Player", "Assist"), ("assist2Player", "Assist")):
                nid = d.get(f + "Id")
                pid = _match318(who.get(nid, ""), names) if nid else None
                if pid is None:
                    continue
                key = f"n|{gid}|{p.get('eventId')}|{nid}|{kind}"
                if key in _sent311():
                    continue
                if seed:
                    _mark311(key)
                    s321 = _secs321(p.get("timeInPeriod"))
                    if s321 is not None:
                        _mark311(f"d|{pid}|{kind}|{(p.get('periodDescriptor') or {}).get('number') or 0}|{s321}")  # change 321
                    continue
                n = d.get(f + "Total")
                msg = f"{kind} by {names[pid]}" + (f" ({n})" if n else "")
                _send321(key, pid, kind, (p.get("periodDescriptor") or {}).get("number") or 0, p.get("timeInPeriod"), msg, "NHL")  # change 321
    if seed:
        _mark311(SEED318)
    _boot318["done"] = True


def fast318(opp, secs):
    """check the NHL feed every 5 seconds for secs seconds"""
    end = time.time() + secs
    while True:
        if opp:
            try:
                nhl_goals318(opp)
            except Exception as e:
                log("NHL goal check failed", e)
            try:
                espn_goals321(opp)  # change 321: whichever feed has the goal first sends it
            except Exception as e:
                log("ESPN goal check failed", e)
        if time.time() >= end:
            return
        time.sleep(2)  # change 321: was 5


# ---------- change 321: race ESPN's feed against the NHL feed; write down when every alert went out ----------
SB321 = "https://site.api.espn.com/apis/site/v2/sports/hockey/nhl/"
TIMES321 = os.path.join(HERE, "edge", "alert-times.json")
SEED321 = "zz-espn321"  # in the sent file: goals already on the board when the ESPN racer first ran were alerted before
_etot321, _ehot321, _eread321, _eboot321 = {}, {}, {}, {"done": False}
_dirty321 = [False]


def _secs321(t):
    try:
        m, s = str(t).split(":")[:2]
        return int(m) * 60 + int(s)
    except Exception:
        return None


def _dup321(pid, kind, per, t):
    """the same player, same kind, same period, within 60 seconds of game clock = the same goal"""
    s = _secs321(t)
    if s is None:
        return False
    pre = f"d|{pid}|{kind}|{per}|"
    return any(k.startswith(pre) and abs(int(k[len(pre):]) - s) <= 60 for k in _sent311() if k[len(pre):].isdigit())


def _send321(key, pid, kind, per, t, msg, src, wall=None):
    """send one alert unless either feed already sent it; remember it under both names"""
    if key in _sent311() or _dup321(pid, kind, per, t):
        return
    try:
        import gm_push
        gm_push.send(msg, "", "#matchup")  # change 315's look: the message, then "from <app>"
        log("goal alert:", msg, "(" + src + ")")
    except Exception as e:
        log("goal alert failed", e)
        return
    _mark311(key)
    s = _secs321(t)
    if s is not None:
        _mark311(f"d|{pid}|{kind}|{per}|{s}")
    try:
        try:
            with open(TIMES321) as f:
                L = json.load(f)
        except Exception:
            L = []
        L.append({"sent": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "msg": msg, "from": src,
                  "goal": wall, "period": per, "clock": t})
        with open(TIMES321, "w") as f:
            json.dump(L[-300:], f, indent=0)
        _dirty321[0] = True
    except Exception as e:
        log("could not save alert time", e)


def espn_goals321(opp):
    """one look at ESPN's feed: the same alerts as the NHL check, from whichever feed has the goal first"""
    ids = _opp_ids302(opp)
    names = {pid: nm for pid, nm in (_opp302.get("names") or {}).items() if pid in ids and nm}
    if not names:
        return
    sb = requests.get(SB321 + "scoreboard", headers=UA318, timeout=10).json()
    seed, now = SEED321 not in _sent311(), time.time()
    for ev in sb.get("events", []):
        st = (((ev.get("status") or {}).get("type")) or {}).get("state")
        if st not in ("in", "post"):
            continue
        eid = ev.get("id")
        comp = (ev.get("competitions") or [{}])[0]
        tot = sum(int(c.get("score") or 0) for c in comp.get("competitors") or [])
        if tot != _etot321.get(eid):
            _etot321[eid] = tot
            _ehot321[eid] = now + 240
        if _eboot321["done"] and now > _ehot321.get(eid, 0) and not (st == "in" and now - _eread321.get(eid, 0) >= 30):
            continue
        _eread321[eid] = now
        try:
            sm = requests.get(SB321 + "summary", params={"event": eid}, headers=UA318, timeout=10).json()
        except Exception as e:
            log("ESPN game read failed", eid, e)
            continue
        for p in sm.get("plays") or []:
            per = (p.get("period") or {}).get("number") or 0
            if not p.get("scoringPlay") or per >= 5:
                continue  # shootout goals do not count
            t = (p.get("clock") or {}).get("displayValue")
            text = p.get("text") or ""
            for q in p.get("participants") or []:
                kind = {"scorer": "Goal", "assister": "Assist"}.get(q.get("type"))
                a = q.get("athlete") or {}
                try:
                    pid = int(a.get("id"))
                except Exception:
                    continue
                if not kind or pid not in names:
                    continue
                key = f"e|{eid}|{p.get('id')}|{pid}|{kind}"
                if seed:
                    if key not in _sent311():
                        _mark311(key)
                    continue
                nm = a.get("displayName") or names[pid]
                m = re.search(r"Goal \((\d+)\)", text) if kind == "Goal" else re.search(re.escape(nm) + r" \((\d+)\)", text)
                _send321(key, pid, kind, per, t, f"{kind} by {names[pid]}" + (f" ({m.group(1)})" if m else ""), "ESPN", p.get("wallclock"))
    if seed:
        _mark311(SEED321)
    _eboot321["done"] = True


# ---------- change 322: the alert checks run on their own track ----------
_opp322 = [None]
_run322 = [False]


def _loop322():
    while True:
        try:
            if _opp322[0]:
                fast318(_opp322[0], 0)  # one look at both feeds
        except Exception as e:
            log("alert track error", e)
        time.sleep(2)


def alerts322(opp):
    """hand the alert track the current opponent; start the track the first time"""
    if opp:
        _opp322[0] = opp
    if not _run322[0] and _opp322[0]:
        import threading
        threading.Thread(target=_loop322, daemon=True).start()
        _run322[0] = True
        log("alert track started")


if __name__ == "__main__":
    main()
