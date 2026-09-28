"""
gm_alerts.py - lineup checks for Fantasy Islands GM (phone alerts through ntfy).
Checks your ESPN lineup every sync and hands what it finds to gm_notify.py,
which decides whether your phone buzzes right away or the item waits for the next summary.
 URGENT (sent right away, only before that game starts):
 - an active player ruled OUT with a game today
 - a goalie in your lineup who is NOT the starter tonight (Daily Faceoff)
 - a starter missing from tonight's Daily Faceoff lineup (possible scratch; 2-8 PM)
 - a bench player with a game while a starter at his position has none (within 3 hours of the game)
 SUMMARY (morning / pre-game):
 - that same bench swap earlier in the day
 - free agents newly on PP1, with an ice-time jump, or being grabbed fast
 - your players losing ice time
Test it: right-click this file -> Run 'gm_alerts' (sends a test message).
"""
import hashlib
import re
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import requests
from gm_model import norm, ab
import gm_notify

NTFY_TOPIC = gm_notify.NTFY_TOPIC
SCRATCH_FROM, SCRATCH_TO = 14, 20      # check tonight's lineups for scratches between 2 PM and 8 PM
SWAP_URGENT_H = 3                      # bench/starter swap becomes urgent this many hours before the game
TRENDING_PCT = 10

LOCAL = ZoneInfo("America/Vancouver")
ET = ZoneInfo("America/New_York")
HDR = {"User-Agent": "Mozilla/5.0"}
BENCH, IR, UTIL = 7, 8, 6
OUT_WORDS = ("OUT", "INJURY_RESERVE", "INJURED_RESERVE", "SUSPEN")
LINEUP_RE = re.compile(r"^(f ?[1-4]|forwards? ?[1-4]|(1st|2nd|3rd|4th|first|second|third|fourth) (line|pair(ing)?)|line ?[1-4]"
                       r"|d ?[1-3]|defen[cs]e ?(pair(ing)? ?)?[1-3]|pair(ing)? ?[1-3])$", re.I)


def send(title, msg, prio="default", tags=""):
    """Send straight to the phone (used for the test message)."""
    return gm_notify.push(title, msg, prio, tags)


def games_today():
    d = datetime.now(ET).date().isoformat()
    r = requests.get(f"https://api-web.nhle.com/v1/schedule/{d}", headers=HDR, timeout=30)
    r.raise_for_status()
    out = {}
    for day in r.json().get("gameWeek", []):
        if day.get("date") != d:
            continue
        for g in day.get("games", []):
            if g.get("gameType") != 2:
                continue
            t = datetime.fromisoformat(g["startTimeUTC"].replace("Z", "+00:00")).astimezone(LOCAL)
            label = t.strftime("%I:%M %p").lstrip("0")
            for side in ("homeTeam", "awayTeam"):
                out[ab(g[side]["abbrev"])] = (label, t)
    return d, out


def lineup_names(team):
    """All forwards + defensemen in a team's current Daily Faceoff lineup (fresh read)."""
    from gm_signals import next_data, find_group, SLUGS
    data = next_data(f"https://www.dailyfaceoff.com/teams/{SLUGS[team]}/line-combinations")
    names = set()
    if data:
        find_group(data, LINEUP_RE, names)
    return {norm(n) for n in names}


def run(players, slots, goalies, signals, my_team_id):
    if not NTFY_TOPIC or "PASTE" in NTFY_TOPIC:
        print("(alerts) off - put your ntfy topic name in the NTFY_TOPIC secret to turn on phone alerts")
        return
    now = datetime.now(LOCAL)
    day, games = games_today()
    signals = signals or {}
    inj = signals.get("injuries", {})
    gday = (goalies or {}).get(day, {})
    mine = [p for p in players if p["ft"] == my_team_id]
    counts = {}
    for p in mine:
        counts[slots.get(p["id"])] = counts.get(slots.get(p["id"]), 0) + 1
    print(f"(alerts) your lineup slots today: {counts}  (7 = bench, 8 = IR)  |  NHL teams playing today: {len(games)}")

    def is_out(p):
        st = (inj.get(str(p["id"]), {}).get("status") or p.get("status") or "").upper().replace("-", "_").replace(" ", "_")
        return any(w in st for w in OUT_WORDS)

    def upcoming(t):
        return t in games and games[t][1] > now

    def lbl(t):
        return games[t][0]

    active = [p for p in mine if slots.get(p["id"]) not in (BENCH, IR, None)]
    bench = [p for p in mine if slots.get(p["id"]) == BENCH]
    alerts = []   # (title, message, section, urgent, tags)

    for p in active:                       # 1) injured starters
        if upcoming(p["t"]) and is_out(p):
            alerts.append(("Lineup: starter is OUT", f"{p['n']} ({p['t']}, {lbl(p['t'])}) is listed OUT but is in your active lineup. Bench him and start someone who plays today.", "lineup", True, "warning"))

    for p in active:                       # 2) goalies not starting
        if p["p"] != "G" or not upcoming(p["t"]):
            continue
        if norm(p["n"]) in {norm(k) for k in gday}:
            continue
        other = next(((k, v) for k, v in gday.items() if v.get("team") == p["t"] and "confirm" in (v.get("status") or "").lower() and "un" not in (v.get("status") or "").lower()), None)
        if other:
            alerts.append(("Goalie not starting tonight", f"{p['n']} ({p['t']}, {lbl(p['t'])}): Daily Faceoff lists {other[0]} ({other[1].get('status') or 'starter'}). Swap in a goalie who is starting.", "lineup", True, "warning"))

    if SCRATCH_FROM <= now.hour < SCRATCH_TO:   # 3) possible scratches (morning skate / warmups)
        checked = {}
        for p in active:
            if p["p"] == "G" or not upcoming(p["t"]) or is_out(p):
                continue
            if p["t"] not in checked:
                try:
                    checked[p["t"]] = lineup_names(p["t"])
                except Exception:
                    checked[p["t"]] = set()
            names = checked[p["t"]]
            if len(names) >= 15 and norm(p["n"]) not in names:
                alerts.append(("Possible scratch tonight", f"{p['n']} ({p['t']}, {lbl(p['t'])}) is not in tonight's lineup on Daily Faceoff - he may be scratched or hurt. Check and swap him out before puck drop.", "lineup", True, "warning"))
        print(f"(alerts) scratch check: {len(checked)} teams' lineups read")

    for b in bench:                        # 4) bench player with a game vs idle starter
        if not upcoming(b["t"]) or is_out(b):
            continue
        idle = [a for a in active if a["t"] not in games and (a["p"] == b["p"] or (b["p"] != "G" and slots.get(a["id"]) == UTIL))]
        if idle:
            a = idle[0]
            soon = games[b["t"]][1] - now <= timedelta(hours=SWAP_URGENT_H)
            alerts.append(("Lineup: bench player has a game", f"{b['n']} ({b['t']}, {lbl(b['t'])}) is on your bench with a game today, while {a['n']} ({a['t']}) is starting with no game. Swap them.", "lineup", soon, "arrows_counterclockwise"))

    ppc = (signals.get("pp1") or {}).get("changes", {})
    toi = signals.get("toi") or {}
    for p in players:                      # 5) free-agent opportunities + your players' ice time
        t = toi.get(str(p["id"]))
        if p["ft"] == my_team_id and t and t["d"] <= -180:
            alerts.append(("Your player is losing ice time", f"{p['n']} ({p['t']}) is down {abs(t['d']) / 60:.1f} min per game lately ({t['r'] / 60:.1f} vs {t['b'] / 60:.1f}). Possible demotion - watch his role.", "mine", False, ""))
        if p["ft"]:
            continue
        if ppc.get(str(p["id"])) == "added":
            alerts.append(("Pickup: new PP1 free agent", f"{p['n']} ({p['p']}, {p['t']}) was just moved onto his team's top power-play unit and is a free agent.", "pickup", False, ""))
        elif t and (t["d"] >= 180 or t["pd"] >= 90):
            alerts.append(("Pickup: ice time jump", f"{p['n']} ({p['p']}, {p['t']}) is playing {t['r'] / 60:.1f} min per game lately, up {t['d'] / 60:+.1f} (PP {t['pd'] / 60:+.1f}). Likely promoted - free agent.", "pickup", False, ""))
        elif (p.get("chg") or 0) >= TRENDING_PCT:
            alerts.append(("Pickup: trending free agent", f"{p['n']} ({p['p']}, {p['t']}) ownership is up {p['chg']}% - other managers are grabbing him.", "pickup", False, ""))

    new = 0
    for title, msg, section, urgent, tags in alerts:
        key = hashlib.md5((msg + ("!" if urgent else "")).encode("utf-8")).hexdigest()[:12]
        if gm_notify.add(key, title, msg, section, urgent=urgent, tags=tags) != "duplicate":
            new += 1
    print(f"(alerts) {len(alerts)} alert(s) found ({sum(1 for a in alerts if a[3])} urgent), {new} new")


if __name__ == "__main__":
    if not NTFY_TOPIC or "PASTE" in NTFY_TOPIC:
        print("Put your ntfy topic name in NTFY_TOPIC first.")
    else:
        send("Fantasy Islands GM", "Test alert - phone alerts are working!", "default")
        print("Test alert sent - check your phone.")
