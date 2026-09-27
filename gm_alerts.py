"""
gm_alerts.py - phone alerts through the free ntfy app.
Checks your ESPN lineup every sync and pings your phone about:
 - an active player ruled OUT with a game today
 - a goalie in your lineup who is NOT the starter tonight (Daily Faceoff)
 - a starter missing from tonight's Daily Faceoff lineup (possible scratch; 2-8 PM)
 - a bench player with a game while a starter at his position has none
 - free agents newly on PP1, with an ice-time jump, or being grabbed fast
 - your players losing ice time
Each alert is sent once per day. Test it: right-click this file -> Run 'gm_alerts'.
"""
import hashlib
import json
import os
import re
from datetime import datetime
from zoneinfo import ZoneInfo
import requests
from gm_model import norm, ab

try:
    from secrets_local import NTFY_TOPIC
except ImportError:
    NTFY_TOPIC = os.environ.get("NTFY_TOPIC", "PASTE-YOUR-TOPIC-NAME").strip()
QUIET_START, QUIET_END = 23, 7         # no alerts between 11 PM and 7 AM (your time)
SCRATCH_FROM, SCRATCH_TO = 14, 20      # check tonight's lineups for scratches between 2 PM and 8 PM
TRENDING_PCT = 10

HERE = os.path.dirname(os.path.abspath(__file__))
SENT = os.path.join(HERE, "alerts_sent.json")
LOCAL = ZoneInfo("America/Vancouver")
ET = ZoneInfo("America/New_York")
HDR = {"User-Agent": "Mozilla/5.0"}
BENCH, IR, UTIL = 7, 8, 6
OUT_WORDS = ("OUT", "INJURY_RESERVE", "INJURED_RESERVE", "SUSPEN")
LINEUP_RE = re.compile(r"^(f ?[1-4]|forwards? ?[1-4]|(1st|2nd|3rd|4th|first|second|third|fourth) (line|pair(ing)?)|line ?[1-4]"
                       r"|d ?[1-3]|defen[cs]e ?(pair(ing)? ?)?[1-3]|pair(ing)? ?[1-3])$", re.I)


def send(title, msg, prio="default", tags=""):
    requests.post(f"https://ntfy.sh/{NTFY_TOPIC}", data=msg.encode("utf-8"),
                  headers={"Title": title, "Priority": prio, "Tags": tags}, timeout=20)


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
                out[ab(g[side]["abbrev"])] = label
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
    if "PASTE" in NTFY_TOPIC:
        print("(alerts) off - put your ntfy topic name in gm_alerts.py to turn on phone alerts")
        return
    now = datetime.now(LOCAL)
    if now.hour >= QUIET_START or now.hour < QUIET_END:
        print("(alerts) quiet hours - nothing sent")
        return
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

    active = [p for p in mine if slots.get(p["id"]) not in (BENCH, IR, None)]
    bench = [p for p in mine if slots.get(p["id"]) == BENCH]
    alerts = []

    for p in active:                       # 1) injured starters
        if p["t"] in games and is_out(p):
            alerts.append(("Lineup: starter is OUT", f"{p['n']} ({p['t']}, {games[p['t']]}) is listed OUT but is in your active lineup. Bench him and start someone who plays today.", "high", "warning"))

    for p in active:                       # 2) goalies not starting
        if p["p"] != "G" or p["t"] not in games:
            continue
        if norm(p["n"]) in {norm(k) for k in gday}:
            continue
        other = next(((k, v) for k, v in gday.items() if v.get("team") == p["t"]), None)
        if other:
            alerts.append(("Goalie not starting tonight", f"{p['n']} ({p['t']}, {games[p['t']]}): Daily Faceoff lists {other[0]} ({other[1].get('status') or 'starter'}). Swap in a goalie who is starting.", "high", "goal_net"))

    if SCRATCH_FROM <= now.hour < SCRATCH_TO:   # 3) possible scratches (morning skate / warmups)
        checked = {}
        for p in active:
            if p["p"] == "G" or p["t"] not in games or is_out(p):
                continue
            if p["t"] not in checked:
                try:
                    checked[p["t"]] = lineup_names(p["t"])
                except Exception:
                    checked[p["t"]] = set()
            names = checked[p["t"]]
            if len(names) >= 15 and norm(p["n"]) not in names:
                alerts.append(("Possible scratch tonight", f"{p['n']} ({p['t']}, {games[p['t']]}) is not in tonight's lineup on Daily Faceoff - he may be scratched or hurt. Check and swap him out before puck drop.", "high", "rotating_light"))
        print(f"(alerts) scratch check: {len(checked)} teams' lineups read")

    for b in bench:                        # 4) bench player with a game vs idle starter
        if b["t"] not in games or is_out(b):
            continue
        idle = [a for a in active if a["t"] not in games and (a["p"] == b["p"] or (b["p"] != "G" and slots.get(a["id"]) == UTIL))]
        if idle:
            a = idle[0]
            alerts.append(("Lineup: bench player has a game", f"{b['n']} ({b['t']}, {games[b['t']]}) is on your bench with a game today, while {a['n']} ({a['t']}) is starting with no game. Swap them.", "default", "arrows_counterclockwise"))

    ppc = (signals.get("pp1") or {}).get("changes", {})
    toi = signals.get("toi") or {}
    for p in players:                      # 5) free-agent opportunities + your players' ice time
        t = toi.get(str(p["id"]))
        if p["ft"] == my_team_id and t and t["d"] <= -180:
            alerts.append(("Your player is losing ice time", f"{p['n']} ({p['t']}) is down {abs(t['d']) / 60:.1f} min per game lately ({t['r'] / 60:.1f} vs {t['b'] / 60:.1f}). Possible demotion - watch his role.", "default", "arrow_down"))
        if p["ft"]:
            continue
        if ppc.get(str(p["id"])) == "added":
            alerts.append(("Pickup: new PP1 free agent", f"{p['n']} ({p['p']}, {p['t']}) was just moved onto his team's top power-play unit and is a free agent.", "default", "chart_with_upwards_trend"))
        elif t and (t["d"] >= 180 or t["pd"] >= 90):
            alerts.append(("Pickup: ice time jump", f"{p['n']} ({p['p']}, {p['t']}) is playing {t['r'] / 60:.1f} min per game lately, up {t['d'] / 60:+.1f} (PP {t['pd'] / 60:+.1f}). Likely promoted - free agent.", "default", "stopwatch"))
        elif (p.get("chg") or 0) >= TRENDING_PCT:
            alerts.append(("Pickup: trending free agent", f"{p['n']} ({p['p']}, {p['t']}) ownership is up {p['chg']}% - other managers are grabbing him.", "low", "fire"))

    sent = {}
    if os.path.exists(SENT):
        with open(SENT, encoding="utf-8") as f:
            sent = json.load(f)
    today = sent.get(day, [])
    new = 0
    for title, msg, prio, tags in alerts:
        h = hashlib.md5(msg.encode("utf-8")).hexdigest()[:12]
        if h in today:
            continue
        send(title, msg, prio, tags)
        today.append(h)
        new += 1
    with open(SENT, "w", encoding="utf-8") as f:
        json.dump({day: today}, f)
    print(f"(alerts) {len(alerts)} alert(s) found, {new} new sent to your phone")


if __name__ == "__main__":
    if "PASTE" in NTFY_TOPIC:
        print("Put your ntfy topic name in NTFY_TOPIC first.")
    else:
        send("Fantasy Islands GM", "Test alert - phone alerts are working!", "default", "white_check_mark")
        print("Test alert sent - check your phone.")
