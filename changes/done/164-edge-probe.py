# changes/164-edge-probe.py - one-time test: can GitHub download the NHL's player-tracking (EDGE) data and shift charts? Writes ai/research/edge_probe.json, nothing in the app changes

PROBE = r'''"""gm_edge_probe.py - change 164: checks once whether NHL EDGE tracking (where every player is at the goal) and shift charts can be read.
Writes ai/research/edge_probe.json. Runs at most every 20 minutes until it has tested at least one goal, then stops by itself.
"""
import json, os, time
import requests

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "ai", "research", "edge_probe.json")
UA = {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"}


def get(url, hdr=None):
    r = {"url": url}
    try:
        x = requests.get(url, headers={**UA, **(hdr or {})}, timeout=20)
        r.update(status=x.status_code, bytes=len(x.content), ctype=x.headers.get("content-type"), cors=x.headers.get("access-control-allow-origin"), head=x.text[:1500])
        try:
            r["json"] = x.json()
        except Exception:
            pass
    except Exception as ex:
        r["error"] = str(ex)[:300]
    return r


def run():
    old = {}
    try:
        old = json.load(open(OUT))
    except Exception:
        pass
    if old.get("done") or time.time() - old.get("at", 0) < 1200:
        return
    out = {"at": time.time(), "when": time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime()), "done": False, "tests": []}
    now = get("https://api-web.nhle.com/v1/score/now")
    games = [g for g in ((now.get("json") or {}).get("games") or []) if g.get("gameState") in ("LIVE", "CRIT", "FINAL", "OFF")]
    out["games_seen"] = len(games)
    for g in games[:3]:
        gid = g.get("id")
        land = get(f"https://api-web.nhle.com/v1/gamecenter/{gid}/landing")
        urls = []
        for per in (((land.get("json") or {}).get("summary") or {}).get("scoring") or []):
            for goal in per.get("goals") or []:
                for k, v in goal.items():
                    if isinstance(v, str) and ("sprites" in v or "ppt" in k.lower() or "replay" in k.lower()):
                        urls.append([k, v])
        pbp = get(f"https://api-web.nhle.com/v1/gamecenter/{gid}/play-by-play")
        gplay = [p for p in ((pbp.get("json") or {}).get("plays") or []) if p.get("typeDescKey") == "goal"]
        keys = sorted(set(k for p in gplay for k in p)) if gplay else []
        t = {"game": gid, "landing_status": land.get("status"), "replay_fields": urls[:6], "pbp_goal_keys": keys,
             "pbp_goal_sample": json.dumps(gplay[0])[:1500] if gplay else ""}
        if gplay:
            ev = gplay[0].get("eventId")
            season = str(g.get("season") or "")
            for u in [x[1] for x in urls[:1]] + [f"https://wsr.nhle.com/sprites/{season}/{gid}/ev{ev}.json"]:
                for hdr in ({}, {"Referer": "https://www.nhl.com/", "Origin": "https://www.nhl.com"}):
                    r = get(u, hdr)
                    j = r.pop("json", None)
                    if isinstance(j, list) and j:
                        r["frames"] = len(j)
                        r["frame0"] = json.dumps(j[0])[:1500]
                    r["with_referer"] = bool(hdr)
                    t.setdefault("tracking", []).append(r)
        sh = get(f"https://api.nhle.com/stats/rest/en/shiftcharts?cayenneExp=gameId={gid}")
        sj = sh.pop("json", None)
        t["shifts_status"] = sh.get("status")
        t["shifts_count"] = len((sj or {}).get("data") or []) if isinstance(sj, dict) else None
        t["shifts_sample"] = json.dumps(((sj or {}).get("data") or [None])[0])[:600] if isinstance(sj, dict) else ""
        t["shifts_cors"] = sh.get("cors")
        out["tests"].append(t)
        if gplay:
            out["done"] = True
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1)
    print("(edge probe) wrote", OUT, "done" if out["done"] else "no goals yet")


if __name__ == "__main__":
    run()
'''

new_file("gm_edge_probe.py", PROBE)


def notify(t):
    return lit(t, "164: run the probe",
               "        try:  # change 130: Monday note\n",
               "        try:  # change 164: one-time EDGE tracking test\n            import gm_edge_probe\n            gm_edge_probe.run()\n        except Exception as ex:\n            print(f\"(edge probe) WARNING: {ex}\")\n        try:  # change 130: Monday note\n",
               "change 164: one-time EDGE tracking test")


edit("gm_notify.py", notify)
