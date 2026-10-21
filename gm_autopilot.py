"""
gm_autopilot.py - change 089: sets your ESPN lineup for today by itself.

Runs at the end of every sync (espn_sync.py calls run()). It works out the best
legal lineup for today from the app's projections and Daily Faceoff's starting
goalies, then either:
  mode "test" - only writes what it WOULD do to autopilot_log.json and sends a phone note
  mode "on"   - makes the change on ESPN, logs it and sends a phone note
  mode "off"  - does nothing
The switch lives in autopilot.json (edit it on GitHub). It starts in "test".

Safety rules:
  - only ever touches your own team (MY_TEAM_ID) and only today's scoring day
  - never moves a player whose game has started (ESPN locks him) or anyone in an IR slot
  - one all-or-nothing request per change; at most one change per run
  - changes only when the new lineup is worth at least min_gain more points today
"""
import json
import os
import re
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

HERE = os.path.dirname(os.path.abspath(__file__))
CONF = os.path.join(HERE, "autopilot.json")
LOG = os.path.join(HERE, "autopilot_log.json")
ET = ZoneInfo("America/New_York")
PT = ZoneInfo("America/Vancouver")
WRITES = "https://lm-api-writes.fantasy.espn.com/apis/v3/games/fhl/seasons/{season}/segments/0/leagues/{league}/transactions/"
DEFAULT_CONF = {"mode": "test", "min_gain": 0.5, "goalies": True, "skaters": True,
                "notes": "mode: test = only tell me, on = change my ESPN lineup, off = do nothing"}
SLOT_F, SLOT_D, SLOT_G, SLOT_U, SLOT_BENCH, SLOT_IR = 3, 4, 5, 6, 7, 8
CAP = {SLOT_F: 9, SLOT_D: 5, SLOT_U: 1, SLOT_G: 2}
ACTIVE = (SLOT_F, SLOT_D, SLOT_U, SLOT_G)
STICK = 0.75          # a player already starting keeps his spot unless someone is this much better
OUTS = ("OUT", "INJURY_RESERVE", "SUSPENSION")
MAX_NOTES_TEST = 4    # test mode: at most this many phone notes a day


def _read_js(name):
    p = os.path.join(HERE, name)
    if not os.path.exists(p):
        return {}
    t = open(p, encoding="utf-8").read()
    return json.loads(t[t.index("{"):t.rindex("}") + 1])


def conf():
    c = dict(DEFAULT_CONF)
    try:
        with open(CONF, encoding="utf-8") as f:
            c.update(json.load(f) or {})
    except FileNotFoundError:
        with open(CONF, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_CONF, f, indent=2)
        print("(autopilot) created autopilot.json in test mode")
    except Exception as ex:
        print(f"(autopilot) autopilot.json could not be read ({ex}), staying off")
        c["mode"] = "off"
    c["mode"] = str(c.get("mode", "test")).strip().lower()
    return c


def load_log():
    try:
        with open(LOG, encoding="utf-8") as f:
            b = json.load(f)
        if isinstance(b, dict):
            b.setdefault("entries", [])
            b.setdefault("state", {})
            return b
    except Exception:
        pass
    return {"entries": [], "state": {}}


def save_log(b):
    b["entries"] = b["entries"][-60:]
    with open(LOG, "w", encoding="utf-8") as f:
        json.dump(b, f, indent=1)


def _nrm(s):
    import unicodedata
    s = unicodedata.normalize("NFD", s or "")
    return "".join(c for c in s if unicodedata.category(c) != "Mn").lower().strip()


def start_chance(p, day, E):
    """Same rules as the app: Daily Faceoff confirmed 100%, likely 85%, unconfirmed 50%,
    another goalie named for his team means he sits; otherwise his recent start share."""
    g = (E.get("goalies") or {}).get(day) or {}
    names = {_nrm(k): v for k, v in g.items()}
    me = names.get(_nrm(p["n"]))
    lvl = lambda st: 1.0 if ("confirm" in st and "un" not in st) else 0.85 if re.search(r"likely|expected|project", st) else 0.5
    if me:
        return lvl((me.get("status") or "").lower()), "Daily Faceoff"
    mate = next((v for v in g.values() if v.get("team") == p["t"]), None)
    if mate:
        return 1 - lvl((mate.get("status") or "").lower()), "Daily Faceoff"
    gs = ((E.get("signals") or {}).get("gstart") or {}).get(str(p["id"])) or {}
    return float(gs.get("share", 0.5)), "start share"


def value(p, day, E):
    """Expected fantasy points today, before the game: projection x start chance x healthy."""
    base = p.get("pavg") or p.get("avg") or 0
    v = (base * 10 + (p.get("tot") or 0)) / (10 + p["gp"]) if p.get("gp") else base
    mv = (((E.get("model") or {}).get("proj") or {}).get(str(p["id"])) or {}).get(day)
    if mv is not None:
        v = (v + mv) / 2
    inj = ((E.get("signals") or {}).get("injuries") or {}).get(str(p["id"])) or {}
    st = (p.get("status") or "ACTIVE").upper()
    ist = (inj.get("status") or "").lower()
    if st in OUTS or "out" in ist or "reserve" in ist or "suspen" in ist:
        if not (inj.get("back") and inj["back"] <= day):
            return 0.0, "out"
    why = ""
    if p["p"] == "G":
        sc, src = start_chance(p, day, E)
        v *= sc
        why = f"{round(sc * 100)}% to start"
    if st == "DAY_TO_DAY" or "day-to-day" in ist:
        v *= 0.8
        why = (why + ", " if why else "") + "day-to-day"
    return v, why


def plan(roster, day, games, E, c):
    """roster: list of dicts {id, n, t, p, slot, locked, elig, ...espn-data fields}.
    Returns (moves, before, after, notes)."""
    cap = dict(CAP)
    for r in roster:
        if r["locked"] and r["slot"] in ACTIVE:
            cap[r["slot"]] -= 1
    free = [r for r in roster if not r["locked"] and r["slot"] != SLOT_IR]
    for r in roster:
        has = r["t"] in games
        v, why = value(r, day, E) if has else (0.0, "no game")
        r["v"], r["why"] = round(v, 2), why
    sc = lambda r: r["v"] + (STICK if r["slot"] in ACTIVE and r["v"] > 0 else 0)
    want = {}
    if not c.get("goalies", True):
        for r in free:
            if r["p"] == "G":
                want[r["id"]] = r["slot"]
                if r["slot"] == SLOT_G:
                    cap[SLOT_G] -= 1
    if not c.get("skaters", True):
        for r in free:
            if r["p"] != "G":
                want[r["id"]] = r["slot"]
                if r["slot"] in ACTIVE:
                    cap[r["slot"]] -= 1
    left = [r for r in free if r["id"] not in want]

    def take(pos, slot):
        pool = sorted([r for r in left if r["p"] == pos and r["v"] > 0 and r["id"] not in want], key=sc, reverse=True)
        for r in pool[:max(0, cap[slot])]:
            want[r["id"]] = slot
    take("G", SLOT_G)
    take("D", SLOT_D)
    take("F", SLOT_F)
    util = sorted([r for r in left if r["p"] in ("F", "D") and r["v"] > 0 and r["id"] not in want
                   and (not r["elig"] or SLOT_U in r["elig"])], key=sc, reverse=True)
    for r in util[:max(0, cap[SLOT_U])]:
        want[r["id"]] = SLOT_U
    for r in left:
        want.setdefault(r["id"], SLOT_BENCH)
    # keep starters in the starting spot they already have (F slot vs UTIL) so nothing moves for nothing
    for r in left:
        a = want[r["id"]]
        if a in (SLOT_F, SLOT_U, SLOT_D) and r["slot"] in (SLOT_F, SLOT_U, SLOT_D) and r["slot"] != a:
            mate = next((q for q in left if want[q["id"]] == r["slot"] and q["slot"] == a and q["p"] == r["p"]), None)
            if mate:
                want[r["id"]], want[mate["id"]] = r["slot"], a
    moves = [{"r": r, "from": r["slot"], "to": want[r["id"]]} for r in left if want[r["id"]] != r["slot"]]
    total = lambda f: sum(r["v"] for r in roster if f(r) in ACTIVE)
    before = total(lambda r: r["slot"])
    after = total(lambda r: want.get(r["id"], r["slot"]))
    return moves, round(before, 1), round(after, 1)


def describe(moves):
    ins = [m["r"] for m in moves if m["to"] in ACTIVE and m["from"] not in ACTIVE]
    outs = [m["r"] for m in moves if m["from"] in ACTIVE and m["to"] not in ACTIVE]
    short = lambda r: r["n"].split(" ")[-1] + (" (" + r["why"] + ")" if r.get("why") else "")
    parts = []
    if ins:
        parts.append("Start " + ", ".join(short(r) for r in ins))
    if outs:
        parts.append("bench " + ", ".join(short(r) for r in outs))
    if not parts and moves:
        parts.append("move " + ", ".join(m["r"]["n"].split(" ")[-1] for m in moves) + " between starting spots")
    return "; ".join(parts) + "."


def run(session, league_url, my_team_id, swid, season, league_id):
    c = conf()
    if c["mode"] == "off":
        print("(autopilot) off")
        return
    E = _read_js("espn-data.js")
    G = _read_js("games-data.js")
    now_et = datetime.now(ET)
    day = now_et.date().isoformat()
    sp = next((p["id"] for p in (E.get("periods") or []) if day in (p.get("dates") or [])), None)
    games = (G.get("games") or {}).get(day) or {}
    if not sp or not games:
        print(f"(autopilot) nothing to do today ({day}): {'no NHL games' if not games else 'no ESPN scoring day'}")
        return
    r = session.get(league_url, params=[("view", "mRoster"), ("forTeamId", my_team_id), ("scoringPeriodId", sp)], timeout=30)
    r.raise_for_status()
    team = next((t for t in r.json().get("teams", []) if t.get("id") == my_team_id), None)
    entries = (team or {}).get("roster", {}).get("entries", [])
    if len(entries) < 15:
        print(f"(autopilot) your roster came back with {len(entries)} players, so nothing was changed")
        return
    byid = {p["id"]: p for p in E.get("players") or []}
    roster = []
    for en in entries:
        pe = en.get("playerPoolEntry") or {}
        pl = pe.get("player") or {}
        base = byid.get(en.get("playerId"))
        if not base:
            continue
        roster.append({**base, "slot": en.get("lineupSlotId"), "locked": bool(pe.get("lineupLocked")),
                       "elig": pl.get("eligibleSlots") or []})
    moves, before, after = plan(roster, day, games, E, c)
    gain = round(after - before, 1)
    b = load_log()
    st = b["state"] if b["state"].get("day") == day else {"day": day, "notes": 0, "sent": []}
    b["state"] = st
    if not moves or gain < float(c.get("min_gain", 0.5)):
        print(f"(autopilot) lineup is already the best for {day} (projected {before})")
        save_log(b)
        return
    text = describe(moves)
    sig = "|".join(sorted(f"{m['r']['id']}:{m['to']}" for m in moves))
    stamp = datetime.now(PT).strftime("%-I:%M %p")
    entry = {"at": datetime.now(PT).isoformat(timespec="seconds"), "day": day, "mode": c["mode"], "text": text,
             "gain": gain, "before": before, "after": after,
             "moves": [{"id": m["r"]["id"], "n": m["r"]["n"], "from": m["from"], "to": m["to"], "why": m["r"].get("why", "")} for m in moves]}
    try:
        import gm_notify
        note = gm_notify.push
    except Exception:
        note = lambda *a, **k: False
    if c["mode"] != "on":
        if sig in st["sent"]:
            print(f"(autopilot) test: same suggestion as before for {day}: {text}")
            save_log(b)
            return
        entry["result"] = "test only"
        b["entries"].append(entry)
        st["sent"].append(sig)
        if st["notes"] < MAX_NOTES_TEST:
            st["notes"] += 1
            note("Autopilot test", f"Would change your lineup ({stamp}): {text} +{gain} points today. Nothing was changed on ESPN.")
        print(f"(autopilot) test: would {text} (+{gain})")
        save_log(b)
        return
    body = {"isLeagueManager": False, "teamId": my_team_id, "type": "ROSTER", "memberId": swid,
            "scoringPeriodId": sp, "executionType": "EXECUTE",
            "items": [{"playerId": m["r"]["id"], "type": "LINEUP", "fromLineupSlotId": m["from"], "toLineupSlotId": m["to"]} for m in moves]}
    url = WRITES.format(season=season, league=league_id)
    try:
        w = session.post(url, json=body, headers={"Content-Type": "application/json"}, timeout=30)
        ok = w.status_code < 300
        try:
            js = w.json()
        except Exception:
            js = {}
        msg = js.get("status") or ""
        if not ok:
            msg = ", ".join(str(x.get("message") or x.get("type") or x) for x in (js.get("details") or js.get("messages") or [])) or w.text[:200]
    except Exception as ex:
        ok, msg = False, f"{type(ex).__name__}: {ex}"
    entry["result"] = "done" if ok else "failed: " + str(msg)[:200]
    b["entries"].append(entry)
    if ok:
        note("Autopilot", f"Changed your lineup ({stamp}): {text} +{gain} points today.")
        print(f"(autopilot) changed lineup: {text} (+{gain})")
    else:
        if "failed" not in st:
            st["failed"] = 1
            note("Autopilot could not change your lineup", f"{text} ESPN said: {msg}. Set it by hand on ESPN today.", "high")
        print(f"(autopilot) ESPN refused the change: {msg}")
    save_log(b)
