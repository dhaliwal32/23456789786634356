# changes/130-weekly-note.py - one short phone note every Monday morning: last week's score and how close the app's projections were for your players, e.g. "Week 4: you 406, Gems 426 (lost by 20). App was 15% off on your players."

WEEKLY = r'''"""
gm_weekly.py - one short phone note every Monday morning (8 to 11 am Pacific):
    "Week 4: you 461, Sarm 470 (lost by 9). App was 4% off on your players."
The score is ESPN's final for last week; "off" compares the app's projection (Combined, else AI, else GM model)
for your players' games last week with the points they really scored (from ai/joined).
Called from gm_notify.py on every sync; sends once per week.
"""
import glob
import json
import os
import re
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

HERE = os.path.dirname(os.path.abspath(__file__))
PT = ZoneInfo("America/Vancouver")


def espn():
    with open(os.path.join(HERE, "espn-data.js"), encoding="utf-8") as f:
        t = f.read()
    return json.loads(t[t.index("{"):t.rindex("}") + 1])


def accuracy(me, d0, d1):
    pred = act = 0.0
    n = 0
    for f in sorted(glob.glob(os.path.join(HERE, "ai", "joined", "*.json"))):
        day = os.path.basename(f)[:10]
        if not (d0 <= day <= d1):
            continue
        try:
            with open(f, encoding="utf-8") as fh:
                recs = (json.load(fh) or {}).get("recs") or []
        except Exception:
            continue
        for r in recs:
            if r.get("ft") != me or not r.get("played") or r.get("fp") is None:
                continue
            p = next((r.get(k) for k in ("combo", "ai", "gm", "espn") if r.get(k) is not None), None)
            if p is None:
                continue
            if r.get("pos") == "G" and (r.get("gs") or 0) < 1:
                continue
            pred += p
            act += r["fp"]
            n += 1
    return (abs(act - pred) / act * 100 if act > 0 else None), n


def message(now=None):
    now = (now or datetime.now(PT)).astimezone(PT)
    if now.weekday() != 0 or not (8 <= now.hour < 12):
        return None, None
    E = espn()
    me, cur = E.get("myTeamId"), E.get("currentPeriod") or 1
    wk = cur - 1 if cur > 1 else None
    if not wk:
        return None, None
    m = next((x for x in E.get("matchups") or [] if x.get("period") == wk and me in (x.get("home"), x.get("away"))), None)
    if not m:
        return None, None
    home = m["home"] == me
    a, b = (m["hs"], m["as"]) if home else (m["as"], m["hs"])
    opp = m["away"] if home else m["home"]
    names = {t["id"]: t["name"] for t in E.get("teams") or []}
    them = (names.get(opp) or "Them").split()[0]
    res = f"won by {a - b:.0f}" if a > b else f"lost by {b - a:.0f}" if b > a else "tied"
    end = (now - timedelta(days=1)).date()
    pct, n = accuracy(me, (end - timedelta(days=6)).isoformat(), end.isoformat())
    msg = f"Week {wk}: you {a:.0f}, {them} {b:.0f} ({res})."
    if pct is not None and n >= 5:
        msg += f" App was {pct:.0f}% off on your players."
    return f"weekly-{wk}", msg


def run():
    key, msg = message()
    if not msg:
        return
    import gm_notify
    gm_notify.add(key, "Fantasy GM", msg, "mine", urgent=True)
    print(f"(weekly) {msg}")


if __name__ == "__main__":
    import sys
    if "--preview" in sys.argv:
        print(message(datetime(2026, 10, 26, 9, 0, tzinfo=PT)))
    else:
        run()
'''


def change_notify(t):
    return lit(t, "130: weekly note", "        try:\n            flush()\n        except Exception as ex:\n            print(f\"(notify) WARNING: {ex}\")",
               "        try:\n            flush()\n        except Exception as ex:\n            print(f\"(notify) WARNING: {ex}\")\n        try:  # change 130: Monday note\n            import gm_weekly\n            gm_weekly.run()\n        except Exception as ex:\n            print(f\"(weekly) WARNING: {ex}\")",
               "change 130: Monday note")


new_file("gm_weekly.py", WEEKLY)
edit("gm_notify.py", change_notify)
