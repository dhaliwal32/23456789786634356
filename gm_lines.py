"""
gm_lines.py - Lines tab data + roster-change alerts for Fantasy Islands GM.

Every sync (throttled so it stays fast) it:
  1. reads full line combinations for all 32 teams from Daily Faceoff
     (4 forward lines, 3 defence pairs, PP1, PP2, goalies)
  2. reads every team's NHL roster and spots trades, call-ups and send-downs
  3. spots ESPN injury-status changes
  4. downloads NHL standings, the next week of games and every player's season
     fantasy points (your league's scoring)
  5. writes lines-data.js for the app's Lines tab, including a change feed
  6. sends phone alerts (ntfy) for changes that affect your players, or free
     agents who just got a bigger role

It runs as its own step after espn_sync.py and never edits the other files,
so if it fails the sync and the app keep working.

Commands:
  python gm_lines.py              normal run (GitHub Actions does this)
  python gm_lines.py --force      re-read lines and rosters right now
  python gm_lines.py --selftest   offline checks of the change detector
"""
import copy
import hashlib
import json
import os
import re
import sys
import time
import traceback
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

import requests

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from gm_model import norm, ab, stats, SK, GO, THIS, LAST  # noqa: E402

OUT = os.path.join(HERE, "lines-data.js")
STATE = os.path.join(HERE, "lines_state.json")
ESPN_JS = os.path.join(HERE, "espn-data.js")
WEB = "https://api-web.nhle.com/v1"
HDR = {"User-Agent": "Mozilla/5.0"}
UTC = timezone.utc
ET = ZoneInfo("America/New_York")
PT = ZoneInfo("America/Vancouver")

MY_TEAM_ID = 4
READ_EVERY_H = 2           # re-read lines + rosters this often...
READ_EVERY_H_PREGAME = 1   # ...and every hour from 2 PM to 7 PM (lineups get posted)
KEEP_CHANGES = 400
KEEP_DAYS = 21
FA_MIN_OWN = 3.0           # free agents must be this % rostered (or ESPN proj 5+) to trigger an alert
MAX_ALERTS_PER_RUN = 4
ALERT_MAX_AGE_H = 18       # older changes are never alerted
QUIET_START, QUIET_END = 23, 7

NHL_TRI = {"LA": "LAK", "NJ": "NJD", "SJ": "SJS", "TB": "TBL"}
ES = ["F1", "F2", "F3", "F4", "D1", "D2", "D3"]
SLOTS = ES + ["PP1", "PP2", "G"]
RANK = {"F1": 1, "F2": 2, "F3": 3, "F4": 4, "D1": 1, "D2": 2, "D3": 3}
LABEL = {"F1": "1st line", "F2": "2nd line", "F3": "3rd line", "F4": "4th line",
         "D1": "top pair", "D2": "2nd pair", "D3": "3rd pair", "PP1": "PP1", "PP2": "PP2", "G": "goalie"}
ORD = {1: ("1st", "first"), 2: ("2nd", "second"), 3: ("3rd", "third"), 4: ("4th", "fourth")}


def _rx(kind, n):
    o, w = ORD[n]
    if kind == "F":
        pat = rf"^(f ?{n}|forwards? ?{n}|{o} line|{w} line|line ?{n})$"
    elif kind == "D":
        pat = rf"^(d ?{n}|defen[cs]e ?(pair(ing)? ?)?{n}|{o} pair(ing)?|{w} pair(ing)?|pair(ing)? ?{n})$"
    else:
        pat = rf"^(pp ?{n}|powerplay ?{n}|power ?play ?(unit )?{n}|{o} power ?play( unit)?|{w} power ?play( unit)?)$"
    return re.compile(pat, re.I)


GROUPS = ([(f"F{n}", _rx("F", n), 2, 4) for n in (1, 2, 3, 4)]
          + [(f"D{n}", _rx("D", n), 2, 3) for n in (1, 2, 3)]
          + [(f"PP{n}", _rx("P", n), 3, 8) for n in (1, 2)])
G_RE = re.compile(r"^(g ?[12]?|goalies?|goaltenders?|goaltending|starting goalie|backup goalie)$", re.I)


# ----------------------------------------------------------------- helpers
def iso(dt):
    return dt.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def parse(s):
    try:
        return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC)
    except Exception:
        return None


def read_json(path, default):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default


def write_json(path, obj):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, separators=(",", ":"))
    os.replace(tmp, path)


def http_json(url):
    r = requests.get(url, headers=HDR, timeout=30)
    r.raise_for_status()
    return r.json()


def season_label(sid):
    return f"{sid[:4]}-{sid[6:]}"


def pretty(x):
    return str(x or "").replace("_", " ").title()


def load_espn():
    try:
        with open(ESPN_JS, encoding="utf-8") as f:
            body = f.read().split("=", 1)[1].strip()
        return json.loads(body[:-1] if body.endswith(";") else body)
    except Exception as ex:
        print(f"(lines) could not read espn-data.js: {ex}")
        return {}


def chg(now, typ, team, name, text, d="", frm="", to="", g=None):
    key = norm(name)
    cid = hashlib.sha1(f"{typ}|{team}|{key}|{frm}|{to}|{now.date()}".encode()).hexdigest()[:12]
    return {"id": cid, "at": iso(now), "type": typ, "team": team, "name": name, "key": key,
            "dir": d, "from": frm, "to": to, "g": g, "text": text}


# ----------------------------------------------------------------- 1. lines (Daily Faceoff)
def read_team(t):
    from gm_signals import next_data, find_group, SLUGS
    data = next_data(f"https://www.dailyfaceoff.com/teams/{SLUGS[t]}/line-combinations")
    if not data:
        return None
    out, used = {}, set()
    for slot, rx, lo, hi in GROUPS:
        names = set()
        find_group(data, rx, names)
        if slot.startswith("PP"):
            if lo <= len(names) <= hi:
                out[slot] = sorted(names)
            continue
        names = {n for n in names if norm(n) not in used}
        if lo <= len(names) <= hi:
            out[slot] = sorted(names)
            used |= {norm(n) for n in names}
    g = set()
    find_group(data, G_RE, g)
    g = {n for n in g if norm(n) not in used}
    if 1 <= len(g) <= 3:
        out["G"] = sorted(g)
    return out


def complete(g):
    return all(s in (g or {}) for s in ES)


def diff_lines(prev, cur, ok, now):
    out = []
    for t in ok:
        p, c = prev.get(t) or {}, cur.get(t) or {}
        if complete(p) and complete(c):
            pm, cm = {}, {}
            for s in ES:
                for n in p[s]:
                    pm.setdefault(norm(n), (s, n))
                for n in c[s]:
                    cm.setdefault(norm(n), (s, n))
            for k, (s, n) in cm.items():
                if k in pm:
                    ps = pm[k][0]
                    if ps == s:
                        continue
                    if ps[0] == s[0]:
                        up = RANK[s] < RANK[ps]
                        out.append(chg(now, "line", t, n,
                                       f"{n} ({t}) {'promoted' if up else 'moved down'}: {LABEL[ps]} -> {LABEL[s]}",
                                       "up" if up else "down", ps, s, s[0]))
                    else:
                        out.append(chg(now, "line", t, n, f"{n} ({t}) switched from {LABEL[ps]} to {LABEL[s]}",
                                       "", ps, s, s[0]))
                else:
                    out.append(chg(now, "lineup", t, n, f"{n} ({t}) is in the lineup on the {LABEL[s]}",
                                   "in", "", s, s[0]))
            for k, (s, n) in pm.items():
                if k not in cm:
                    out.append(chg(now, "lineup", t, n,
                                   f"{n} ({t}) is no longer in the lineup (was {LABEL[s]}) - scratched, hurt or moved",
                                   "out", s, "", s[0]))
        if p.get("PP1") and c.get("PP1"):
            before, after = {norm(x): x for x in p["PP1"]}, {norm(x): x for x in c["PP1"]}
            for k, n in after.items():
                if k not in before:
                    out.append(chg(now, "pp", t, n, f"{n} ({t}) moved onto PP1", "up", "", "PP1"))
            for k, n in before.items():
                if k not in after:
                    out.append(chg(now, "pp", t, n, f"{n} ({t}) is off PP1", "down", "PP1", ""))
    return out


def step_lines(state, now):
    from gm_signals import SLUGS
    prev = state.get("lines") or {}
    cur, ok, counts = {}, [], {s: 0 for s in SLOTS}
    for t in SLUGS:
        g = None
        try:
            g = read_team(t)
        except Exception as ex:
            print(f"(lines) {t}: Daily Faceoff read failed ({type(ex).__name__})")
        if g and "F1" in g and "D1" in g:
            cur[t] = g
            ok.append(t)
            for s in g:
                counts[s] += 1
        else:
            cur[t] = prev.get(t) or {}
        time.sleep(0.15)
    print(f"(lines) Daily Faceoff: {len(ok)}/32 teams read | groups found: "
          + ", ".join(f"{s} {counts[s]}" for s in SLOTS))
    changes = diff_lines(prev, cur, ok, now) if prev else []
    if not prev:
        print("(lines) first read saved - line changes are reported from the next read")
    state["lines"] = cur
    if ok:
        state["lines_at"] = iso(now)
    return changes


# ----------------------------------------------------------------- 2. NHL rosters
def read_rosters():
    from gm_signals import SLUGS
    out = {}
    for t in SLUGS:
        try:
            js = http_json(f"{WEB}/roster/{NHL_TRI.get(t, t)}/current")
            pl = {}
            for grp, pos in (("forwards", "F"), ("defensemen", "D"), ("goalies", "G")):
                for x in js.get(grp) or []:
                    n = f"{(x.get('firstName') or {}).get('default', '')} {(x.get('lastName') or {}).get('default', '')}".strip()
                    if x.get("id") and n:
                        pl[str(x["id"])] = {"n": n, "p": pos}
            if len(pl) >= 15:
                out[t] = pl
        except Exception as ex:
            print(f"(lines) {t}: NHL roster read failed ({type(ex).__name__})")
        time.sleep(0.1)
    return out


def diff_rosters(prev, cur, now):
    if not prev:
        return []
    where_p = {pid: t for t, pl in prev.items() for pid in pl}
    where_c = {pid: t for t, pl in cur.items() for pid in pl}
    out = []
    for pid, tc in where_c.items():
        tp = where_p.get(pid)
        x = cur[tc][pid]
        if tp == tc:
            continue
        if tp and tp in cur:
            out.append(chg(now, "move", tc, x["n"], f"{x['n']} moved {tp} -> {tc} (trade or waiver claim)",
                           "in", tp, tc, x["p"]))
        elif tp is None and tc in prev:
            out.append(chg(now, "move", tc, x["n"], f"{x['n']} added to {tc}'s NHL roster (call-up, signing or claim)",
                           "in", "", tc, x["p"]))
    for pid, tp in where_p.items():
        if pid in where_c or tp not in cur:
            continue
        x = prev[tp][pid]
        out.append(chg(now, "move", tp, x["n"],
                       f"{x['n']} removed from {tp}'s NHL roster (sent down, waived, released or retired)",
                       "out", tp, "", x["p"]))
    return out


def step_rosters(state, now):
    prev = state.get("rosters") or {}
    cur = read_rosters()
    good = {t: pl for t, pl in cur.items() if not (t in prev and len(pl) < 0.5 * len(prev[t]))}
    print(f"(lines) NHL rosters: {len(good)}/32 teams read, {sum(len(v) for v in good.values())} players")
    changes = diff_rosters(prev, good, now) if prev else []
    if not prev:
        print("(lines) first roster read saved - moves are reported from the next read")
    state["rosters"] = {**prev, **good}
    if good:
        state["rosters_at"] = iso(now)
    return changes


# ----------------------------------------------------------------- 3. ESPN injury status
def step_status(state, players, now):
    prev = state.get("status") or {}
    cur = {str(p["id"]): (p.get("status") or "ACTIVE") for p in players}
    out = []
    if prev and cur:
        by = {str(p["id"]): p for p in players}
        for pid, s in cur.items():
            o = prev.get(pid)
            if not o or o == s:
                continue
            p = by[pid]
            if not (p.get("ft") or (p.get("own") or 0) >= FA_MIN_OWN or (p.get("pavg") or 0) >= 5):
                continue
            c = chg(now, "status", p["t"], p["n"], f"{p['n']} ({p['t']}) injury status: {pretty(o)} -> {pretty(s)}",
                    "up" if s == "ACTIVE" else "down", o, s, p.get("p"))
            c["e"] = pid
            out.append(c)
    if cur:
        state["status"] = cur
    return out


# ----------------------------------------------------------------- 4. standings, fantasy points, schedule
def parse_standings(js):
    out = {}
    for r in (js or {}).get("standings") or []:
        t = ab((r.get("teamAbbrev") or {}).get("default"))
        if not t:
            continue
        out[t] = {"pts": r.get("points") or 0, "gp": r.get("gamesPlayed") or 0, "w": r.get("wins") or 0,
                  "l": r.get("losses") or 0, "otl": r.get("otLosses") or 0,
                  "pct": round(r.get("pointPctg") or 0, 3), "gf": r.get("goalFor") or 0, "ga": r.get("goalAgainst") or 0,
                  "name": (r.get("teamName") or {}).get("default") or t, "season": r.get("seasonId"),
                  "streak": f"{r.get('streakCode') or ''}{r.get('streakCount') or ''}"}
    return out


def read_standings(state):
    rows = {}
    try:
        rows = parse_standings(http_json(f"{WEB}/standings/now"))
    except Exception as ex:
        print(f"(lines) standings/now failed: {ex}")
    if rows and any(v.get("season") == int(THIS) and v["gp"] > 0 for v in rows.values()):
        return rows, season_label(THIS)
    last = state.get("last_st")
    if not last:
        end = "2026-04-16"
        try:
            for s in http_json(f"{WEB}/standings-season").get("seasons") or []:
                if s.get("id") == int(LAST) and s.get("standingsEnd"):
                    end = s["standingsEnd"]
        except Exception as ex:
            print(f"(lines) standings-season lookup failed: {ex}")
        try:
            last = parse_standings(http_json(f"{WEB}/standings/{end}"))
        except Exception as ex:
            print(f"(lines) last-season standings failed: {ex}")
            last = {}
        if last:
            state["last_st"] = last
    return (last or rows), f"{season_label(LAST)} final"


def season_fp(season):
    sk, out = {}, {}
    for r in stats("skater/summary", season):
        k = f"{norm(r.get('skaterFullName'))}|{'D' if r.get('positionCode') == 'D' else 'F'}"
        sk[k] = {"gp": r.get("gamesPlayed") or 0,
                 "fp": SK["G"] * (r.get("goals") or 0) + SK["A"] * (r.get("assists") or 0)
                 + SK["PM"] * (r.get("plusMinus") or 0) + SK["PPP"] * (r.get("ppPoints") or 0)
                 + SK["SHP"] * (r.get("shPoints") or 0) + SK["SOG"] * (r.get("shots") or 0)}
    for r in stats("skater/realtime", season):
        k = f"{norm(r.get('skaterFullName'))}|{'D' if r.get('positionCode') == 'D' else 'F'}"
        if k in sk:
            sk[k]["fp"] += SK["HIT"] * (r.get("hits") or 0) + SK["BLK"] * (r.get("blockedShots") or 0)
    for k, v in sk.items():
        out[k] = [round(v["fp"], 1), v["gp"]]
    for r in stats("goalie/summary", season):
        fp = (GO["W"] * (r.get("wins") or 0) + GO["GA"] * (r.get("goalsAgainst") or 0)
              + GO["SV"] * (r.get("saves") or 0) + GO["SO"] * (r.get("shutouts") or 0)
              + GO["OTL"] * (r.get("otLosses") or 0))
        out[f"{norm(r.get('goalieFullName'))}|G"] = [round(fp, 1), r.get("gamesPlayed") or 0]
    return out


def step_fp(state, now, due):
    if state.get("last_fp_for") != LAST or not state.get("last_fp"):
        lf = season_fp(LAST)
        if lf:
            state["last_fp"], state["last_fp_for"] = lf, LAST
    fat = parse(state.get("fp_at") or "")
    if due or not fat or now - fat >= timedelta(hours=1):
        state["fp_this"], state["fp_at"] = season_fp(THIS), iso(now)
    return state.get("fp_this") or {}, state.get("last_fp") or {}


def read_schedule(now):
    day = now.astimezone(ET).date().isoformat()
    out = {}
    for d in http_json(f"{WEB}/schedule/{day}").get("gameWeek") or []:
        for g in d.get("games") or []:
            if g.get("gameType") != 2:
                continue
            h, a = ab(g["homeTeam"]["abbrev"]), ab(g["awayTeam"]["abbrev"])
            out.setdefault(h, []).append({"d": d["date"], "o": a, "h": True, "s": g.get("startTimeUTC")})
            out.setdefault(a, []).append({"d": d["date"], "o": h, "h": False, "s": g.get("startTimeUTC")})
    return out


def team_fp(ln, fp):
    tot = 0.0
    for s in ES + ["G"]:
        grp = "G" if s == "G" else s[0]
        for n in (ln or {}).get(s, []):
            tot += (fp.get(f"{norm(n)}|{grp}") or [0])[0]
    return round(tot, 1)


# ----------------------------------------------------------------- 5. alerts
def relevance(ch, p):
    if not p:
        return None
    ft = p.get("ft") or 0
    if ft == MY_TEAM_ID:
        return "mine"
    if ft:
        return None
    if not ((p.get("own") or 0) >= FA_MIN_OWN or (p.get("pavg") or 0) >= 5):
        return None
    if ch["type"] in ("line", "lineup") and ch["dir"] in ("up", "in") and ch["to"] in ("F1", "F2", "D1"):
        return "fa"
    if ch["type"] == "move" and ch["dir"] == "in":
        return "fa"
    return None


def alert_for(c):
    bad = c["dir"] in ("down", "out")
    if c["who"] == "mine":
        title = {"line": "Your player's line changed", "lineup": "Your player: lineup change",
                 "pp": "Your player: power-play change", "move": "Your player: roster move",
                 "status": "Your player: injury update"}.get(c["type"], "Your player")
        prio = "high" if bad and c["type"] in ("lineup", "move", "status") else "default"
    else:
        title, prio = "Pickup idea: bigger role", "default"
    return title, c["text"], prio, "arrow_down" if bad else "arrow_up"


def send_alerts(state, now):
    try:
        import gm_alerts
    except Exception as ex:
        print(f"(lines) alerts unavailable: {ex}")
        return
    if not gm_alerts.NTFY_TOPIC or "PASTE" in gm_alerts.NTFY_TOPIC:
        print("(lines) alerts off - no ntfy topic")
        return
    h = now.astimezone(PT).hour
    if h >= QUIET_START or h < QUIET_END:
        print("(lines) quiet hours - alerts wait until 7 AM")
        return
    pending = [c for c in state.get("changes") or [] if c.get("who") and not c.get("alerted")
               and parse(c["at"]) and now - parse(c["at"]) < timedelta(hours=ALERT_MAX_AGE_H)]
    if not pending:
        return
    pending.sort(key=lambda c: (c["who"] != "mine", c["at"]))
    first = pending if len(pending) <= MAX_ALERTS_PER_RUN else pending[:MAX_ALERTS_PER_RUN - 1]
    rest = pending[len(first):]
    for c in first:
        gm_alerts.send(*alert_for(c))
        c["alerted"] = True
    if rest:
        msg = "; ".join(c["text"] for c in rest[:6]) + (" ..." if len(rest) > 6 else "") + " - see the Lines tab."
        gm_alerts.send(f"{len(rest)} more roster/line changes", msg, "low", "clipboard")
        for c in rest:
            c["alerted"] = True
    print(f"(lines) phone alerts sent: {len(first)}{' + 1 summary' if rest else ''}")


# ----------------------------------------------------------------- main
def run(force=False):
    now = datetime.now(UTC)
    state = read_json(STATE, {})
    espn = load_espn()
    players = espn.get("players") or []
    by_ng, by_n = {}, {}
    for p in players:
        by_ng.setdefault((norm(p["n"]), p.get("p")), p)
        by_n.setdefault(norm(p["n"]), p)
    by_id = {str(p["id"]): p for p in players}

    every = READ_EVERY_H_PREGAME if 14 <= now.astimezone(PT).hour < 19 else READ_EVERY_H
    last = parse(state.get("read_at") or "")
    due = force or not last or now - last >= timedelta(hours=every)
    new = []
    if due:
        for name, fn in (("lines", step_lines), ("rosters", step_rosters)):
            try:
                new += fn(state, now)
            except Exception:
                print(f"(lines) WARNING {name} step failed:\n{traceback.format_exc()}")
        state["read_at"] = iso(now)
    else:
        print(f"(lines) lines + rosters read {int((now - last).total_seconds() // 60)} min ago - next read within {every} h")
    try:
        new += step_status(state, players, now)
    except Exception:
        print(f"(lines) WARNING status step failed:\n{traceback.format_exc()}")

    for c in new:
        p = by_id.get(c.get("e") or "") or by_ng.get((c["key"], c.get("g"))) or by_n.get(c["key"])
        c["e"] = str(p["id"]) if p else None
        c["who"] = relevance(c, p)
    old = state.get("changes") or []
    ids = {c["id"] for c in old}
    fresh = [c for c in new if c["id"] not in ids]
    cut = now - timedelta(days=KEEP_DAYS)
    state["changes"] = [c for c in fresh + old if (parse(c["at"]) or now) >= cut][:KEEP_CHANGES]
    print(f"(lines) {len(fresh)} new change(s) ({sum(1 for c in fresh if c.get('who'))} worth a phone alert)")

    st, st_src = {}, ""
    try:
        st, st_src = read_standings(state)
        print(f"(lines) standings: {len(st)} teams ({st_src})")
    except Exception as ex:
        print(f"(lines) WARNING standings failed: {ex}")
    fp_this, fp_last = {}, {}
    try:
        fp_this, fp_last = step_fp(state, now, due)
        print(f"(lines) season fantasy points: {len(fp_this)} players {season_label(THIS)}, {len(fp_last)} players {season_label(LAST)}")
    except Exception as ex:
        print(f"(lines) WARNING fantasy points failed: {ex}")
    sched = {}
    try:
        sched = read_schedule(now)
    except Exception as ex:
        print(f"(lines) WARNING schedule failed: {ex}")
    try:
        send_alerts(state, now)
    except Exception as ex:
        print(f"(lines) WARNING alerts failed: {ex}")

    use_this = any(v[1] > 0 for v in fp_this.values())
    lines = state.get("lines") or {}
    rosters = state.get("rosters") or {}
    teams = {}
    for t in sorted(set(lines) | set(st) | set(rosters)):
        teams[t] = {"lines": lines.get(t) or {}, "st": st.get(t) or {},
                    "fp": team_fp(lines.get(t), fp_this if use_this else fp_last),
                    "roster": len(rosters.get(t) or {})}
    data = {"generated": iso(now), "lines_at": state.get("lines_at"), "rosters_at": state.get("rosters_at"),
            "season": season_label(THIS), "fp_use": "this" if use_this else "last",
            "fp_season": season_label(THIS if use_this else LAST), "st_src": st_src,
            "teams": teams, "fp": fp_this, "fpl": fp_last, "sched": sched,
            "changes": [{k: v for k, v in c.items() if k != "alerted"} for c in state["changes"][:200]]}
    write_json(STATE, state)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("window.LINES_DATA = " + json.dumps(data, separators=(",", ":")) + ";\n")
    print(f"(lines) wrote lines-data.js: {len(teams)} teams, {len(data['changes'])} changes in the feed")
    return 0


def selftest():
    ok = []

    def check(name, cond):
        ok.append(bool(cond))
        print(("PASS  " if cond else "FAIL  ") + name)

    now = datetime(2026, 10, 10, 18, 0, tzinfo=UTC)
    base = {"F1": ["Aa One", "Bb One", "Cc One"], "F2": ["Dd Two", "Ee Two", "Ff Two"],
            "F3": ["Gg Three", "Hh Three", "Ii Three"], "F4": ["Jj Four", "Kk Four", "Ll Four"],
            "D1": ["Mm Dee", "Nn Dee"], "D2": ["Oo Dee", "Pp Dee"], "D3": ["Qq Dee", "Rr Dee"],
            "PP1": ["Aa One", "Bb One", "Cc One", "Dd Two", "Mm Dee"]}
    cur = copy.deepcopy(base)
    cur["F1"] = ["Aa One", "Bb One", "Dd Two"]
    cur["F2"] = ["Cc One", "Ee Two", "Ff Two"]
    cur["F4"] = ["Jj Four", "Kk Four", "Zz New"]
    cur["PP1"] = ["Aa One", "Bb One", "Cc One", "Ee Two", "Mm Dee"]
    ch = diff_lines({"TOR": base}, {"TOR": cur}, ["TOR"], now)
    txt = " | ".join(c["text"] for c in ch)
    check("promotion found", any(c["name"] == "Dd Two" and c["dir"] == "up" for c in ch))
    check("demotion found", any(c["name"] == "Cc One" and c["dir"] == "down" for c in ch))
    check("player out of lineup found", any(c["name"] == "Ll Four" and c["dir"] == "out" for c in ch))
    check("player into lineup found", any(c["name"] == "Zz New" and c["dir"] == "in" for c in ch))
    check("PP1 change found", any(c["type"] == "pp" and c["name"] == "Ee Two" for c in ch))
    part = copy.deepcopy(cur)
    del part["F4"]
    check("incomplete read is ignored for lines", not [c for c in diff_lines({"TOR": base}, {"TOR": part}, ["TOR"], now)
                                                       if c["type"] != "pp"])
    prev_r = {"TOR": {"1": {"n": "Aa One", "p": "F"}, "2": {"n": "Bb Two", "p": "D"}}, "MTL": {"3": {"n": "Cc Three", "p": "F"}}}
    cur_r = {"TOR": {"1": {"n": "Aa One", "p": "F"}}, "MTL": {"3": {"n": "Cc Three", "p": "F"}, "2": {"n": "Bb Two", "p": "D"},
                                                             "4": {"n": "Dd Four", "p": "F"}}}
    mv = diff_rosters(prev_r, cur_r, now)
    check("trade found", any(c["name"] == "Bb Two" and c["from"] == "TOR" and c["to"] == "MTL" for c in mv))
    check("call-up found", any(c["name"] == "Dd Four" and c["dir"] == "in" for c in mv))
    mv2 = diff_rosters(prev_r, {"TOR": {"1": {"n": "Aa One", "p": "F"}}}, now)
    check("send-down found", any(c["name"] == "Bb Two" and c["dir"] == "out" for c in mv2))
    check("unread team is not reported", not any(c["team"] == "MTL" for c in mv2))
    p_mine = {"ft": MY_TEAM_ID, "own": 50}
    p_fa = {"ft": 0, "own": 10, "pavg": 4}
    check("my player is alert-worthy", relevance({"type": "line", "dir": "down", "to": "F3"}, p_mine) == "mine")
    check("free agent promoted to F2 is alert-worthy", relevance({"type": "line", "dir": "up", "to": "F2"}, p_fa) == "fa")
    check("free agent moved to F3 is not", relevance({"type": "line", "dir": "up", "to": "F3"}, p_fa) is None)
    print("INFO  " + txt[:300])
    print(f"\n{sum(ok)}/{len(ok)} checks passed" + ("" if all(ok) else "  <-- SOMETHING FAILED"))
    return 0 if all(ok) else 1


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    sys.exit(run(force="--force" in sys.argv))
