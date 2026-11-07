"""gm_onice.py - change 205: who was on the ice for each goal of today's NHL games, from NHL's shift charts.

The app shows this under each goal in the Goal Tracker right away, without waiting for the goal's tracking file.
The browser cannot read NHL's feeds itself, so this runs on GitHub:
  - from gm_edge.py at the end of every sync, writing edge/onice.json
  - from gm_live.py every 30 seconds while games are live, writing edge/onice-live.json (committed only when a new goal is filled)
Each goal: d (game day), g, ev, per, t (time in period), tr (time left), team (scoring team), home, sc (situation code),
on = [[playerId, team, number, name, position], ...] for both teams at the moment of the goal. Keeps 3 days.
"""
import json, os, time
from datetime import datetime, timedelta, timezone
import requests

HERE = os.path.dirname(os.path.abspath(__file__))
UA = {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"}
NHL = dict(UA, Referer="https://www.nhl.com/", Origin="https://www.nhl.com")
AL = {"LAK": "LA", "NJD": "NJ", "SJS": "SJ", "TBL": "TB", "UTAH": "UTA", "ARI": "UTA"}
KEEP_DAYS = 3
SHIFT_GAP = 45  # seconds between shift chart reads for the same game


def ab(x):
    x = str(x or "").upper()
    return AL.get(x, x)


def sec(t):
    try:
        m, s = str(t or "0:0").split(":")[:2]
        return int(m) * 60 + int(s)
    except Exception:
        return -1


def getj(url, hdr=None):
    r = requests.get(url, headers=hdr or UA, timeout=20)
    r.raise_for_status()
    return r.json()


def on_ice(shifts, per, t, ro):
    """players whose shift covers the goal: started before it and ended at it or later. None if the shifts don't reach it yet."""
    T = sec(t)
    rows, last = {}, -1
    for s in shifts:
        if s.get("typeCode") != 517 or s.get("period") != per:
            continue
        a, b = sec(s.get("startTime")), sec(s.get("endTime"))
        if a < 0 or b < 0:
            continue
        last = max(last, b)
        if a < T <= b:
            pid = s.get("playerId")
            r = ro.get(str(pid)) or []
            nm = r[0] if r else ((s.get("firstName") or "") + " " + (s.get("lastName") or "")).strip()
            rows[pid] = [pid, r[3] if len(r) > 3 and r[3] else ab(s.get("teamAbbrev")), r[2] if len(r) > 2 else None, nm, r[1] if len(r) > 1 else ""]
    if last < T:
        return None
    on = list(rows.values())
    teams = {}
    for o in on:
        teams[o[1]] = teams.get(o[1], 0) + 1
    if len(teams) != 2 or min(teams.values()) < 3 or len(on) > 14:
        return None
    return on


def update(out="edge/onice.json", budget=25, live_only=False):
    """fills on-ice lists for today's goals; returns True when the file changed"""
    path = os.path.join(HERE, out)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    try:
        data = json.load(open(path))
    except Exception:
        data = {"goals": {}}
    G = data.setdefault("goals", {})
    seen = data.setdefault("shiftAt", {})
    t0, changed = time.time(), False
    try:
        now = getj("https://api-web.nhle.com/v1/score/now")
    except Exception as ex:
        print(f"(onice) score/now failed: {ex}")
        return False
    for g in now.get("games") or []:
        st = g.get("gameState")
        if not g.get("id") or st not in (("LIVE", "CRIT") if live_only else ("LIVE", "CRIT", "FINAL", "OFF")):
            continue
        if time.time() - t0 > budget:
            break
        gid, day = g["id"], g.get("gameDate") or ""
        n_goals = sum(int((g.get(x) or {}).get("score") or 0) for x in ("homeTeam", "awayTeam"))
        if n_goals and sum(1 for k, v in G.items() if v.get("g") == gid and v.get("on")) >= n_goals:
            continue  # every goal of this game already done
        try:
            pbp = getj(f"https://api-web.nhle.com/v1/gamecenter/{gid}/play-by-play")
        except Exception as ex:
            print(f"(onice) play-by-play {gid} failed: {ex}")
            continue
        tid = {}
        for side in ("homeTeam", "awayTeam"):
            T = pbp.get(side) or {}
            tid[T.get("id")] = ab(T.get("abbrev"))
        home = tid.get((pbp.get("homeTeam") or {}).get("id"), "")
        ro = {}
        for r in pbp.get("rosterSpots") or []:
            nm = (((r.get("firstName") or {}).get("default") or "") + " " + ((r.get("lastName") or {}).get("default") or "")).strip()
            ro[str(r.get("playerId"))] = [nm, r.get("positionCode") or "", r.get("sweaterNumber"), tid.get(r.get("teamId"), "")]
        todo = []
        for p in pbp.get("plays") or []:
            pd = p.get("periodDescriptor") or {}
            if p.get("typeDescKey") != "goal" or pd.get("periodType") == "SO":
                continue
            key = f"{gid}-{p.get('eventId')}"
            if (G.get(key) or {}).get("on"):
                continue
            d = p.get("details") or {}
            todo.append((key, {"d": day, "g": gid, "ev": p.get("eventId"), "per": pd.get("number"), "t": p.get("timeInPeriod"),
                               "tr": p.get("timeRemaining"), "team": tid.get(d.get("eventOwnerTeamId"), ""), "sc": p.get("situationCode"),
                               "home": home, "scorer": d.get("scoringPlayerId")}))
        if not todo or time.time() - seen.get(str(gid), 0) < SHIFT_GAP:
            continue
        seen[str(gid)] = time.time()
        try:
            shifts = (getj(f"https://api.nhle.com/stats/rest/en/shiftcharts?cayenneExp=gameId={gid}", NHL) or {}).get("data") or []
        except Exception as ex:
            print(f"(onice) shift chart {gid} failed: {ex}")
            continue
        for key, ent in todo:
            on = on_ice(shifts, ent["per"], ent["t"], ro)
            if on:
                ent["on"], ent["ok"], ent["at"] = on, True, time.time()
                G[key] = ent
                changed = True
    cut = (datetime.now(timezone.utc) - timedelta(days=KEEP_DAYS)).strftime("%Y-%m-%d")
    for k in [k for k, v in G.items() if (v.get("d") or "") < cut]:
        G.pop(k, None)
        changed = True
    for k in [k for k, v in seen.items() if time.time() - v > 86400]:
        seen.pop(k, None)
    if changed or not os.path.exists(path):
        data["updated"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        with open(path, "w") as f:
            json.dump(data, f, separators=(",", ":"))
    print(f"(onice) {sum(1 for v in G.values() if v.get('on'))} goal(s) with players on the ice" + (" (new)" if changed else ""))
    return changed


if __name__ == "__main__":
    update()
