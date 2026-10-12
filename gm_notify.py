"""
gm_notify.py - decides when your phone buzzes (ntfy) for Fantasy Islands GM.

URGENT alerts (things that cost you points tonight if you don't act) go out
right away. Everything else is collected and sent as one summary:
  - Morning summary at 8:00 AM Pacific (first sync after 8)
  - Pre-game summary about 60 minutes before your first player's game,
    only if something new came in since the morning
Nothing is sent 11 PM - 7 AM; anything that arrives then waits for the morning.
Everything is kept in notify_outbox.json, which the app's News tab shows.

Other scripts call:  gm_notify.add(key, title, text, section, urgent=False)
The sync runs `python gm_notify.py` at the end to send any summary that is due.

Commands:
  python gm_notify.py            send a summary if one is due (GitHub Actions does this)
  python gm_notify.py --preview  show what the next summary would say (sends nothing)
  python gm_notify.py --test     send a test message to your phone now
"""
import json
import os
import sys
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

import requests

try:
    from secrets_local import NTFY_TOPIC
except ImportError:
    NTFY_TOPIC = os.environ.get("NTFY_TOPIC", "PASTE-YOUR-TOPIC-NAME").strip()
try:
    from gm_model import ab
except Exception:
    def ab(x):
        return x

HERE = os.path.dirname(os.path.abspath(__file__))
OUTBOX = os.path.join(HERE, "notify_outbox.json")
ESPN_JS = os.path.join(HERE, "espn-data.js")
APP_URL = "https://dhaliwal32.github.io/23456789786634356/fantasy-gm.html"
PT = ZoneInfo("America/Vancouver")
ET = ZoneInfo("America/New_York")
UTC = timezone.utc
HDR = {"User-Agent": "Mozilla/5.0"}

QUIET_START, QUIET_END = 23, 7      # nothing sent between 11 PM and 7 AM Pacific
MORNING = (8, 0)                    # morning summary time (Pacific)
PREGAME_MIN = 60                    # pre-game summary this many minutes before your first game
MAX_PER_SECTION = 6
KEEP_DAYS = 7                       # history kept for the app's News tab
KEEP_LOG = 40                       # summaries kept for the app's News tab
SECTIONS = [("lineup", "LINEUP"), ("mine", "YOUR PLAYERS"), ("pickup", "PICKUP IDEAS"), ("other", "OTHER")]


def _iso(dt):
    return dt.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def _parse(s):
    try:
        return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC)
    except Exception:
        return None


def _load():
    try:
        with open(OUTBOX, encoding="utf-8") as f:
            box = json.load(f)
    except Exception:
        box = {}
    box.setdefault("items", [])
    box.setdefault("sent", {})
    box.setdefault("log", [])
    return box


def _save(box):
    now = datetime.now(UTC)
    cut = now - timedelta(days=KEEP_DAYS)
    box["items"] = [i for i in box["items"] if (_parse(i.get("at", "")) or now) >= cut]
    box["log"] = box["log"][-KEEP_LOG:]
    for k in sorted(box["sent"])[:-5]:
        del box["sent"][k]
    tmp = OUTBOX + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(box, f, indent=1)
    os.replace(tmp, OUTBOX)


def _day(now):
    return now.astimezone(PT).date().isoformat()


def quiet(now):
    h = now.astimezone(PT).hour
    return h >= QUIET_START or h < QUIET_END


def _clock(dt):
    return dt.astimezone(PT).strftime("%I:%M %p").lstrip("0")


def push(title, msg, prio="default", tags=""):
    """Send one message to the phone right now. Returns True if sent."""
    if not NTFY_TOPIC or "PASTE" in NTFY_TOPIC:
        print("(notify) off - no ntfy topic")
        return False
    headers = {"Title": title, "Priority": prio, "Click": APP_URL}
    if tags:
        headers["Tags"] = tags
    r = requests.post(f"https://ntfy.sh/{NTFY_TOPIC}", data=msg.encode("utf-8"), headers=headers, timeout=20)
    return r.ok


def add(key, title, text, section="other", urgent=False, tags=""):
    """Hand over one alert. Urgent ones are sent now; the rest wait for the next summary."""
    now = datetime.now(UTC)
    box = _load()
    k = f"{_day(now)}|{key}"
    if any(i.get("k") == k for i in box["items"]):
        return "duplicate"
    item = {"k": k, "at": _iso(now), "title": title, "text": text,
            "section": section if section in dict(SECTIONS) else "other", "urgent": bool(urgent), "sent": False}
    status = "queued for the next summary"
    if urgent and not quiet(now):
        try:
            ok = push(title, text, "high", tags or "warning")
        except Exception as ex:
            print(f"(notify) urgent send failed: {ex}")
            ok = False
        if ok:
            item.update(sent=True, via="urgent", sent_at=_iso(now))
            status = "sent right away"
            for i in box["items"]:
                if i.get("text") == text and not i.get("sent"):
                    i.update(sent=True, via="urgent", sent_at=_iso(now))
    box["items"].append(item)
    _save(box)
    print(f"(notify) {'URGENT ' if urgent else ''}{status}: {title}")
    return status


def _load_espn():
    try:
        with open(ESPN_JS, encoding="utf-8") as f:
            body = f.read().split("=", 1)[1].strip()
        return json.loads(body[:-1] if body.endswith(";") else body)
    except Exception:
        return {}


def _today(now):
    """How many of your players play today, and when the first one starts."""
    try:
        E = _load_espn()
        me = E.get("myTeamId") or 4
        mine = [p for p in E.get("players") or [] if p.get("ft") == me and not p.get("ir")]
        d = now.astimezone(ET).date().isoformat()
        js = requests.get(f"https://api-web.nhle.com/v1/schedule/{d}", headers=HDR, timeout=30).json()
        start = {}
        for day in js.get("gameWeek") or []:
            if day.get("date") != d:
                continue
            for g in day.get("games") or []:
                if g.get("gameType") != 2:
                    continue
                st = datetime.fromisoformat(g["startTimeUTC"].replace("Z", "+00:00"))
                for side in ("homeTeam", "awayTeam"):
                    start[ab(g[side]["abbrev"])] = st
        playing = [p for p in mine if p.get("t") in start]
        first = min((start[p["t"]] for p in playing), default=None)
        return {"n": len(playing), "first": first}
    except Exception as ex:
        print(f"(notify) could not read today's schedule: {ex}")
        return None


def build(items, foot=""):
    lines = []
    for sec, label in SECTIONS:
        xs = [i for i in items if i.get("section") == sec]
        if not xs:
            continue
        lines.append(label)
        for i in xs[:MAX_PER_SECTION]:
            lines.append(("[!] " if i.get("urgent") else "- ") + i["text"])
        if len(xs) > MAX_PER_SECTION:
            lines.append(f"  + {len(xs) - MAX_PER_SECTION} more in the app")
        lines.append("")
    if foot:
        lines.append(foot)
    return "\n".join(lines).strip()


def _foot(info):
    if not info:
        return ""
    if not info["n"]:
        return "None of your players play today."
    return f"Today: {info['n']} of your players play, first puck drop {_clock(info['first'])}."


def flush(now=None):
    now = now or datetime.now(UTC)
    box = _load()
    done = box["sent"].setdefault(_day(now), [])
    local = now.astimezone(PT)
    pend = [i for i in box["items"] if not i.get("sent")]
    if quiet(now):
        print(f"(notify) quiet hours - {len(pend)} update(s) waiting for the morning summary")
        _save(box)
        return
    info = _today(now) if ("morning" not in done or "pregame" not in done) else None
    kind = None
    if "morning" not in done and (local.hour, local.minute) >= MORNING:
        kind = "morning"
    elif "morning" in done and "pregame" not in done and info and info["first"]:
        if now >= info["first"]:
            done.append("pregame")
        elif now >= info["first"] - timedelta(minutes=PREGAME_MIN) and pend:
            kind = "pregame"
    if not kind:
        _save(box)
        print(f"(notify) no summary due right now - {len(pend)} update(s) waiting")
        return
    if kind == "morning":
        if not pend and not (info and info["n"]):
            done.append("morning")
            _save(box)
            print("(notify) morning: nothing to say today - skipped")
            return
        title = f"Morning summary - {local.strftime('%a %b')} {local.day}"
        body = build(pend, _foot(info)) if pend else _foot(info) + "\nNo new changes since yesterday."
    else:
        title = f"Before puck drop - first game {_clock(info['first'])}"
        body = build(pend)
    if pend:
        title += f" ({len(pend)} update{'s' if len(pend) != 1 else ''})"
    ok = False
    try:
        ok = push(title, body, "default")
    except Exception as ex:
        print(f"(notify) summary send failed: {ex}")
    if ok:
        for i in pend:
            i.update(sent=True, via=kind, sent_at=_iso(now))
        done.append(kind)
        box["log"].append({"at": _iso(now), "kind": kind, "title": title, "body": body})
        print(f"(notify) {kind} summary sent with {len(pend)} update(s)")
    _save(box)


# ---------- alert switches and a full log of what is sent (news_logos.py round 66) ----------
KEEP_LOG = 300
PREFS = os.path.join(HERE, "alert_prefs.json")
GROUP_OF = {
    "starter_is_out": "injuries", "possible_scratch": "injuries", "your_player_injury_update": "injuries",
    "your_player_line_change": "lines", "your_player_lineup_change": "lines", "your_player_power_play_change": "lines",
    "your_player_roster_move": "lines", "more_line_changes": "lines", "your_player_losing_ice_time": "lines",
    "goalie_not_starting": "goalies", "goalie_not_confirmed": "goalies",
    "pickup_new_pp1": "pickups", "pickup_ice_time_jump": "pickups", "pickup_trending": "pickups", "pickup_bigger_role": "pickups",
}
TITLE_KIND = [
    ("Lineup: starter is OUT", "starter_is_out"), ("Possible scratch tonight", "possible_scratch"),
    ("Your player: injury update", "your_player_injury_update"), ("Lineup: bench player has a game", "bench_player_has_a_game"),
    ("Goalie not starting tonight", "goalie_not_starting"), ("Goalie not confirmed yet", "goalie_not_confirmed"),
    ("Your player's line changed", "your_player_line_change"), ("Your player: lineup change", "your_player_lineup_change"),
    ("Your player: power-play change", "your_player_power_play_change"), ("Your player: roster move", "your_player_roster_move"),
    ("Your player is losing ice time", "your_player_losing_ice_time"), ("Pickup: new PP1 free agent", "pickup_new_pp1"),
    ("Pickup: ice time jump", "pickup_ice_time_jump"), ("Pickup: trending free agent", "pickup_trending"),
    ("Pickup idea: bigger role", "pickup_bigger_role"), ("Morning summary", "morning_summary"), ("Before puck drop", "pregame_summary"),
]
ORDER = ["injuries", "lines", "goalies", "pickups", "morning_summary", "pregame_summary", "bench_player_has_a_game"] + list(GROUP_OF)
DEFAULTS = {k: True for k in ORDER}
DEFAULTS["bench_player_has_a_game"] = False
OFF_TXT, STALE_TXT = "Not sent (switched off)", "Not sent (no longer true)"
_PREFS = {}
_VIA = {"v": None, "blocked": False}


def kind_of(title):
    t = str(title or "")
    if "roster/line changes" in t:
        return "more_line_changes"
    for start, k in TITLE_KIND:
        if t.startswith(start):
            return k
    return None


def prefs():
    if "p" in _PREFS:
        return _PREFS["p"]
    p, ok = {}, True
    if os.path.exists(PREFS):
        try:
            with open(PREFS, encoding="utf-8") as f:
                p = json.load(f)
            if not isinstance(p, dict):
                p, ok = {}, False
        except Exception:
            p, ok = {}, False
    if not ok:
        print("(notify) alert_prefs.json could not be read - using the standard switches until it is fixed")
    elif any(k not in p for k in ORDER):
        out = {k: p.get(k, DEFAULTS[k]) for k in ORDER}
        out.update({k: v for k, v in p.items() if k not in out})
        try:
            with open(PREFS, "w", encoding="utf-8") as f:
                json.dump(out, f, indent=2)
            print("(notify) alert_prefs.json now lists every alert, each with its own switch")
        except Exception as ex:
            print(f"(notify) could not update alert_prefs.json: {ex}")
        p = out
    _PREFS["p"] = p
    return p


def allowed(title):
    k = kind_of(title)
    if not k:
        return True
    p = prefs()
    if p.get(k, DEFAULTS.get(k, True)) is False:
        return False
    g = GROUP_OF.get(k)
    return not (g and p.get(g, True) is False)


def _log(box, now, kind, title, body):
    box["log"].append({"at": _iso(now), "kind": kind, "title": title, "body": body})


_push0, _add0, _flush0 = push, add, flush


def push(title, msg, prio="default", tags=""):
    via = _VIA["v"]
    if via == "summary" and not allowed(title):
        _VIA["blocked"] = True
        print(f"(notify) {title}: switched off, not sent")
        return True
    if via:
        return _push0(title, msg, prio, tags)
    now = datetime.now(UTC)
    if not allowed(title):
        box = _load()
        _log(box, now, OFF_TXT, title, msg)
        _save(box)
        print(f"(notify) switched off, not sent: {title}")
        return False
    ok = _push0(title, msg, prio, tags)
    if ok:
        box = _load()
        _log(box, now, "urgent", title, msg)
        _save(box)
    return ok


def add(key, title, text, section="other", urgent=False, tags=""):
    now = datetime.now(UTC)
    k = f"{_day(now)}|{key}"
    if not allowed(title):
        box = _load()
        if not any(i.get("k") == k for i in box["items"]):
            box["items"].append({"k": k, "at": _iso(now), "title": title, "text": text,
                                 "section": section if section in dict(SECTIONS) else "other", "urgent": bool(urgent),
                                 "sent": True, "via": "off", "sent_at": _iso(now)})
            _log(box, now, OFF_TXT, title, text)
            _save(box)
            print(f"(notify) switched off, not sent: {title}")
        return "switched off"
    _VIA["v"] = "item"
    try:
        res = _add0(key, title, text, section, urgent, tags)
    finally:
        _VIA["v"] = None
    box = _load()
    for i in box["items"]:
        if i.get("k") == k:
            i["seen"] = _iso(now)
    _save(box)
    return res


def flush(now=None):
    now = now or datetime.now(UTC)
    box = _load()
    cut, n = now - timedelta(minutes=50), 0
    for i in box["items"]:
        if i.get("sent"):
            continue
        if not allowed(i.get("title")):
            i.update(sent=True, via="off", sent_at=_iso(now))
            _log(box, now, OFF_TXT, i.get("title"), i.get("text"))
            n += 1
        elif i.get("section") == "lineup":
            seen = _parse(i.get("seen") or i.get("at") or "")
            if seen and seen < cut:
                i.update(sent=True, via="stale", sent_at=_iso(now))
                _log(box, now, STALE_TXT, i.get("title"), i.get("text"))
                n += 1
    if n:
        _save(box)
        print(f"(notify) {n} waiting update(s) removed: switched off, or the lineup problem is no longer there")
    _VIA["v"], _VIA["blocked"] = "summary", False
    try:
        _flush0(now)
    finally:
        _VIA["v"] = None
    if _VIA["blocked"]:
        box = _load()
        if box["log"]:
            box["log"][-1]["kind"] = OFF_TXT
        _save(box)


if __name__ == "__main__":
    if "--preview" in sys.argv:
        b = _load()
        p = [i for i in b["items"] if not i.get("sent")]
        print(f"{len(p)} update(s) waiting:\n")
        print(build(p) or "(nothing)")
    elif "--test" in sys.argv:
        print("sent" if push("Fantasy Islands GM", "Test - phone notifications are working.") else "not sent")
    else:
        try:
            flush()
        except Exception as ex:
            print(f"(notify) WARNING: {ex}")
