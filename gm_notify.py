"""
gm_notify.py - decides when your phone buzzes (ntfy) for Fantasy Islands GM.

URGENT alerts (things that cost you points tonight if you don't act) go out
right away. Everything else is collected and sent as one summary:
  - Morning summary at 8:00 AM Pacific (first sync after 8)
  - Pre-game summary about 60 minutes before your first player's game,
    only if something new came in since the morning
Nothing is sent 11 PM - 7 AM; anything that arrives then waits for the morning.

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
KEEP_DAYS = 3
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
    return box


def _save(box):
    now = datetime.now(UTC)
    cut = now - timedelta(days=KEEP_DAYS)
    box["items"] = [i for i in box["items"] if (_parse(i.get("at", "")) or now) >= cut]
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
            item["sent"] = True
            status = "sent right away"
            for i in box["items"]:
                if i.get("text") == text:
                    i["sent"] = True
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
            i["sent"] = True
        done.append(kind)
        print(f"(notify) {kind} summary sent with {len(pend)} update(s)")
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
