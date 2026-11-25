# changes/326-autopilot-espn-day.py - lineup autopilot reads ESPN's real current day (the roster read only repeats back the day it asked for), so change 325's "ESPN is still on today" fix works between 9 PM and 1 AM

CUR_OLD = '''        cur_sp = r.json().get("scoringPeriodId")
'''
CUR_NEW = '''        cur_sp = _espn_day326(session, league_url) or r.json().get("scoringPeriodId")  # change 326: ESPN's real day
'''
HELP_OLD = '''# ---------- change 325: no autopilot buzz 11 PM - 7 AM Pacific;'''
HELP_NEW = '''# ---------- change 326: the day ESPN is on right now (a roster read for a day only repeats that day back) ----------
_day326 = {}


def _espn_day326(session, league_url):
    if "v" not in _day326:
        try:
            js = session.get(league_url, params=[("view", "mStatus")], timeout=30).json()
            _day326["v"] = js.get("scoringPeriodId") or (js.get("status") or {}).get("latestScoringPeriod")
        except Exception as ex:
            print(f"(autopilot) could not read ESPN's current day: {ex}")
            _day326["v"] = None
    return _day326["v"]


# ---------- change 325: no autopilot buzz 11 PM - 7 AM Pacific;'''


def autopilot(t):
    t = lit(t, "326: read ESPN's real day", CUR_OLD, CUR_NEW, "_espn_day326(session, league_url) or")
    t = lit(t, "326: helper", HELP_OLD, HELP_NEW, "def _espn_day326(session, league_url):")
    return t


edit("gm_autopilot.py", autopilot)
