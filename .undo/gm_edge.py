"""gm_edge.py - change 165: saves the NHL EDGE tracking (where every player and the puck are) for each goal of today's games,
so the app can replay it and list who was on the ice at the goal (plus/minus).

Runs at the end of every sync (from gm_notify.py). Writes edge/index.json and one small file per goal (edge/<game>-<event>.json).
The NHL only sends these files to requests that come from nhl.com, so the browser cannot read them itself; this script fetches them.
Keeps 3 days.
"""
import json, os, time, glob
from datetime import datetime, timedelta, timezone
import requests

HERE = os.path.dirname(os.path.abspath(__file__))
DIR = os.path.join(HERE, "edge")
IDX = os.path.join(DIR, "index.json")
UA = {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"}
NHL = dict(UA, Referer="https://www.nhl.com/", Origin="https://www.nhl.com")
AL = {"LAK": "LA", "NJD": "NJ", "SJS": "SJ", "TBL": "TB", "UTAH": "UTA", "ARI": "UTA"}
KEEP_DAYS = 3
BUDGET_S = 50


def ab(x):
    x = str(x or "").upper()
    return AL.get(x, x)


def getj(url, hdr=None):
    r = requests.get(url, headers=hdr or UA, timeout=20)
    r.raise_for_status()
    return r.json()


def pack(frames):
    """frames -> [[ms, [[pid, team, num, x, y], ...]], ...] with x, y in feet from centre ice (x -100..100, y -42.5..42.5)"""
    out, t0 = [], None
    for f in frames:
        ts = f.get("timeStamp") or 0
        if t0 is None:
            t0 = ts
        row = []
        for o in (f.get("onIce") or {}).values():
            try:
                x, y = round(float(o["x"]) / 12 - 100, 1), round(float(o["y"]) / 12 - 42.5, 1)
            except Exception:
                continue
            pid = o.get("playerId") or 0
            row.append([pid if pid != "" else 0, ab(o.get("teamAbbrev")), o.get("sweaterNumber") or 0, x, y])
        out.append([round((ts - t0) / 10), row])  # timeStamp is in 1/10000 s
    return out


def goal_frame(fr):
    """index of the frame where the puck is closest to either net (the goal); last frame if no puck"""
    best, bi = None, len(fr) - 1
    for i, (_, row) in enumerate(fr):
        for o in row:
            if o[0] == 0:
                d = min((o[3] - 89) ** 2 + o[4] ** 2, (o[3] + 89) ** 2 + o[4] ** 2)
                if best is None or d < best - 0.01:
                    best, bi = d, i
    return bi


def run():
    os.makedirs(DIR, exist_ok=True)
    try:
        idx = json.load(open(IDX))
    except Exception:
        idx = {"goals": {}}
    G = idx.setdefault("goals", {})
    t0, new = time.time(), 0
    days = set()
    try:
        now = getj("https://api-web.nhle.com/v1/score/now")
    except Exception as ex:
        print(f"(edge) score/now failed: {ex}")
        return
    for g in now.get("games") or []:
        if g.get("gameState") not in ("LIVE", "CRIT", "FINAL", "OFF") or not g.get("id"):
            continue
        gid, day = g["id"], g.get("gameDate") or ""
        days.add(day)
        if time.time() - t0 > BUDGET_S:
            break
        try:
            pbp = getj(f"https://api-web.nhle.com/v1/gamecenter/{gid}/play-by-play")
        except Exception as ex:
            print(f"(edge) play-by-play {gid} failed: {ex}")
            continue
        tid = {}
        for side in ("homeTeam", "awayTeam"):
            T = pbp.get(side) or {}
            tid[T.get("id")] = ab(T.get("abbrev"))
        ro = {}
        for r in pbp.get("rosterSpots") or []:
            nm = (((r.get("firstName") or {}).get("default") or "") + " " + ((r.get("lastName") or {}).get("default") or "")).strip()
            ro[str(r.get("playerId"))] = [nm, r.get("positionCode") or "", r.get("sweaterNumber"), tid.get(r.get("teamId"), "")]
        for p in pbp.get("plays") or []:
            if p.get("typeDescKey") != "goal" or not p.get("pptReplayUrl"):
                continue
            key = f"{gid}-{p.get('eventId')}"
            old = G.get(key) or {}
            if old.get("ok") or (old.get("tries", 0) >= 6) or time.time() - old.get("at", 0) < 240:
                continue
            if time.time() - t0 > BUDGET_S:
                break
            d = p.get("details") or {}
            ent = {"d": day, "g": gid, "ev": p.get("eventId"), "per": (p.get("periodDescriptor") or {}).get("number"),
                   "t": p.get("timeInPeriod"), "tr": p.get("timeRemaining"), "team": tid.get(d.get("eventOwnerTeamId"), ""),
                   "sc": p.get("situationCode"), "home": tid.get((pbp.get("homeTeam") or {}).get("id"), ""),
                   "at": time.time(), "tries": old.get("tries", 0) + 1, "ok": False}
            try:
                r = requests.get(p["pptReplayUrl"], headers=NHL, timeout=20)
                fr = r.json() if r.status_code == 200 else None
            except Exception:
                fr = None
            if isinstance(fr, list) and fr:
                P = pack(fr)
                gi = goal_frame(P)
                ids = set(str(o[0]) for f in P for o in f[1] if o[0])
                with open(os.path.join(DIR, key + ".json"), "w") as f:
                    json.dump({"f": P, "gi": gi, "ro": {k: ro[k] for k in ids if k in ro}, "home": ent["home"], "team": ent["team"],
                               "sc": ent["sc"], "goalie": d.get("goalieInNetId"), "scorer": d.get("scoringPlayerId"),
                               "a1": d.get("assist1PlayerId"), "a2": d.get("assist2PlayerId")}, f, separators=(",", ":"))
                ent["ok"] = True
                new += 1
            G[key] = ent
    # keep 3 days
    cut = (datetime.now(timezone.utc) - timedelta(days=KEEP_DAYS)).strftime("%Y-%m-%d")
    for k in [k for k, v in G.items() if (v.get("d") or "") < cut]:
        G.pop(k, None)
        try:
            os.remove(os.path.join(DIR, k + ".json"))
        except Exception:
            pass
    for f in glob.glob(os.path.join(DIR, "*-*.json")):
        if os.path.basename(f)[:-5] not in G:
            os.remove(f)
    idx["updated"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    with open(IDX, "w") as f:
        json.dump(idx, f, separators=(",", ":"))
    print(f"(edge) {new} new goal replay(s), {sum(1 for v in G.values() if v.get('ok'))} saved")


if __name__ == "__main__":
    run()
