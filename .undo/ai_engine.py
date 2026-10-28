"""
ai_engine.py  -  Fantasy Islands GM learning engine, STAGE 1 + 2b (record -> grade -> report)

Runs right AFTER espn_sync.py in GitHub Actions. It only READS espn-data.js (and the AI
projections written by ai_learn.py) and writes into the ai/ folder, so your existing app
keeps working even if this file fails.

Each run it:
  1. PREDICT  - saves a permanent, timestamped copy of the pregame projections
                (ESPN, GM model, Blend and AI) for games that have not started yet.
                Rows are append-only and are never written after a game starts.
  2. OBSERVE  - once NHL games are officially final ("OFF"), downloads the real stats
                and scores them with your league's exact scoring.
  3. DIAGNOSE - compares the official pregame predictions with reality and writes
                ai/report.json (and ai/report.js for the dashboard).

Commands:
  python ai_engine.py              normal run (GitHub Actions does this)
  python ai_engine.py --selftest   offline tests in a temporary folder
  python ai_engine.py --livetest   read-only check that the NHL APIs answer as expected
"""
import hashlib
import json
import math
import os
import shutil
import sys
import tempfile
import unicodedata
from datetime import date, datetime, timedelta, timezone
from zoneinfo import ZoneInfo

VERSION = "ai-stage2b-v1"
HERE = os.path.dirname(os.path.abspath(__file__))
UTC = timezone.utc
ET = ZoneInfo("America/New_York")
PT = ZoneInfo("America/Vancouver")
WEB = "https://api-web.nhle.com/v1"
STATS = "https://api.nhle.com/stats/rest/en"
HDR = {"User-Agent": "Mozilla/5.0"}

# League scoring - must equal gm_model.SK / gm_model.GO (the self-test checks this)
SK = {"G": 6, "A": 4, "PM": 2, "PPP": 2, "SHP": 3, "SOG": 1, "HIT": 0.1, "BLK": 1}
GO = {"W": 5, "GA": -3, "SV": 0.6, "SO": 5, "OTL": 1}

ESPN_K = 10                # app default "ESPN projection weight"
MAX_INPUT_AGE_MIN = 25     # espn-data.js must have been generated this recently
AI_MAX_AGE_H = 36          # AI projections older than this are not used
MIN_LEAD_MIN = 2           # never record a prediction within 2 min of puck drop
CORRECTION_HOURS = 72      # keep re-checking final stats this long (NHL corrections)
RELABEL_EVERY_H = 3        # how often to re-check days that are already final
FINAL_STATES = ("OFF",)    # NHL "official final"
DEAD_SCHED = ("PPD", "CNCL", "SUSP")
DF_START = [("unconfirmed", 0.60), ("confirmed", 1.00), ("likely", 0.85)]  # order matters
ALIAS = {"LAK": "LA", "NJD": "NJ", "SJS": "SJ", "TBL": "TB", "ARI": "UTA", "UTAH": "UTA", "WAS": "WSH"}
MODELS = ("espn", "gm", "blend", "ai")
HASH_SKIP = ("v", "ts", "data_ts", "lead_min", "ai_meta")


# ----------------------------------------------------------------- small helpers
def clamp(x, lo, hi):
    return max(lo, min(hi, x))


def norm(n):  # identical to gm_model.norm so names match the same way
    n = unicodedata.normalize("NFD", n or "").encode("ascii", "ignore").decode()
    return n.lower().replace(".", "").replace("-", " ").strip()


def last_name(n):
    parts = norm(n).split()
    return parts[-1] if parts else ""


def ab(x):
    x = (x or "").upper()
    return ALIAS.get(x, x)


def iso(dt):
    return dt.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_utc(s):
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC)


def P(root, *parts):
    return os.path.join(root, "ai", *parts)


def read_json(path, default):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return default


def write_json(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, separators=(",", ":"))
    os.replace(tmp, path)


def append_rows(path, rows):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, separators=(",", ":")) + "\n")


def read_rows(path):
    out = []
    try:
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        out.append(json.loads(line))
                    except ValueError:
                        pass
    except OSError:
        pass
    return out


def memo(fn):
    cache = {}

    def inner(day):
        if day not in cache:
            cache[day] = fn(day)
        return [dict(g) for g in cache[day]]
    return inner


def http_json(url, params=None):
    import requests
    r = requests.get(url, params=params, headers=HDR, timeout=30)
    r.raise_for_status()
    return r.json()


# ----------------------------------------------------------------- inputs
def load_espn_data(root):
    with open(os.path.join(root, "espn-data.js"), encoding="utf-8") as f:
        txt = f.read()
    body = txt.split("=", 1)[1].strip()
    if body.endswith(";"):
        body = body[:-1]
    return json.loads(body)


def data_time(data):
    try:
        dt = datetime.fromisoformat(str(data.get("generated")))
    except ValueError:
        return None
    if dt.tzinfo is None:  # espn_sync writes naive local time (UTC on GitHub runners)
        dt = dt.replace(tzinfo=UTC if os.environ.get("GITHUB_ACTIONS") else PT)
    return dt.astimezone(UTC)


def load_ai(root, now):
    """AI projections from ai_learn.py - only used if made recently (and therefore before the games)."""
    ai = read_json(P(root, "models", "ai_proj.json"), {})
    try:
        age = (now - parse_utc(ai["asof"])).total_seconds() / 3600
    except (KeyError, TypeError, ValueError):
        return {}
    if age > AI_MAX_AGE_H or age < -1:
        print(f"(ai) AI projections are {round(age)} h old - not used for new predictions")
        return {}
    return ai


def fetch_day(day):
    """Regular-season NHL games on one Eastern-time date, with id, start time and state."""
    js = http_json(f"{WEB}/schedule/{day}")
    out = []
    for d in js.get("gameWeek") or []:
        if d.get("date") != day:
            continue
        for g in d.get("games") or []:
            if g.get("gameType") != 2:
                continue
            out.append({"gid": g.get("id"), "date": day, "start": g.get("startTimeUTC"),
                        "state": g.get("gameState"), "sched": g.get("gameScheduleState"),
                        "home": ab((g.get("homeTeam") or {}).get("abbrev")),
                        "away": ab((g.get("awayTeam") or {}).get("abbrev"))})
    return out


def stats_rows(kind, day):
    exp = f'gameDate<="{day} 23:59:59" and gameDate>="{day}" and gameTypeId=2'
    js = http_json(f"{STATS}/{kind}", {"isAggregate": "false", "isGame": "true",
                                       "limit": -1, "cayenneExp": exp})
    return js.get("data") or []


def fetch_stats(day):
    """Per-game NHL stats for every player on one date, in the engine's label format."""
    sk = {}
    for r in stats_rows("skater/summary", day):
        k = (r.get("gameId"), r.get("playerId"))
        sk[k] = {"gid": r.get("gameId"), "nhl_id": r.get("playerId"), "name": r.get("skaterFullName"),
                 "team": ab(r.get("teamAbbrev")), "pos": "D" if r.get("positionCode") == "D" else "F",
                 "G": r.get("goals") or 0, "A": r.get("assists") or 0, "PM": r.get("plusMinus") or 0,
                 "PPP": r.get("ppPoints") or 0, "SHP": r.get("shPoints") or 0, "SOG": r.get("shots") or 0,
                 "HIT": 0, "BLK": 0, "toi": r.get("timeOnIcePerGame")}
    matched = 0
    for r in stats_rows("skater/realtime", day):
        k = (r.get("gameId"), r.get("playerId"))
        if k in sk:
            sk[k]["HIT"] = r.get("hits") or 0
            sk[k]["BLK"] = r.get("blockedShots") or 0
            matched += 1
    if sk and not matched:
        raise RuntimeError(f"hits/blocks for {day} not available yet - will retry")
    go = []
    for r in stats_rows("goalie/summary", day):
        go.append({"gid": r.get("gameId"), "nhl_id": r.get("playerId"), "name": r.get("goalieFullName"),
                   "team": ab(r.get("teamAbbrev")), "pos": "G", "GS": r.get("gamesStarted") or 0,
                   "W": r.get("wins") or 0, "OTL": r.get("otLosses") or 0, "GA": r.get("goalsAgainst") or 0,
                   "SV": r.get("saves") or 0, "SO": r.get("shutouts") or 0, "toi": r.get("timeOnIce")})
    return list(sk.values()) + go


def fantasy_points(s):
    table = GO if s.get("pos") == "G" else SK
    return round(sum(w * (s.get(k) or 0) for k, w in table.items()), 2)


# ----------------------------------------------------------------- stage 1: PREDICT
def espn_eff(p):
    """App's ESPN per-game number: (proj avg x K + season pts) / (K + games)."""
    pavg, tot, gp = p.get("pavg") or 0, p.get("tot") or 0, p.get("gp") or 0
    if pavg > 0:
        return round((pavg * ESPN_K + tot) / (ESPN_K + gp), 3)
    if gp > 0:
        return round(tot / gp, 3)
    return None


def blend_of(espn, gm, base):
    """App's Blend: ESPN half scaled by the model's matchup ratio, 50/50 with GM."""
    if espn is None or gm is None:
        return None
    ratio = clamp(gm / base, 0.5, 1.6) if base else 1.0
    return round(0.5 * espn * ratio + 0.5 * gm, 3)


def _contains(c, keys, depth=0):
    if isinstance(c, dict):
        if any(k in c for k in keys):
            return True
        return depth < 1 and any(_contains(v, keys, depth + 1) for v in c.values())
    if isinstance(c, (list, tuple, set)):
        if any(k in c for k in keys if not isinstance(k, dict)):
            return True
        return depth < 1 and any(_contains(v, keys, depth + 1) for v in c if isinstance(v, (list, dict)))
    return False


def signals_for(sig, p):
    """This player's pregame signals, using the exact shapes gm_signals.py writes."""
    pid = str(p.get("id"))
    keys = (p.get("id"), pid, p.get("n"), norm(p.get("n")))
    out = {}
    for k, v in (sig or {}).items():
        if not isinstance(v, dict) or k in ("pp1", "lines", "teampp"):
            continue
        hit = next((v[x] for x in keys if x is not None and x in v), None)
        if hit is None:
            continue
        if k == "news":
            items = hit if isinstance(hit, list) else [hit]
            out["news_n"] = len(items)
            out["news_tone"] = "".join(str(i.get("tone") or "") for i in items if isinstance(i, dict))
        elif len(json.dumps(hit, default=str)) <= 300:
            out[k] = hit
    pp = sig.get("pp1") if isinstance((sig or {}).get("pp1"), dict) else {}
    if isinstance(pp.get("on"), (dict, list)):
        out["pp1_on"] = _contains(pp["on"], keys)
        ch = pp.get("changes")
        if isinstance(ch, dict) and pid in ch:
            out["pp1_chg"] = ch[pid]
    ln = sig.get("lines") if isinstance((sig or {}).get("lines"), dict) else {}
    if isinstance(ln.get("top"), (dict, list)):
        out["lines_top"] = _contains(ln["top"], keys)
        if isinstance(ln["top"], dict) and ln["top"].get(pid):
            out["line"] = ln["top"][pid]
        ch = ln.get("changes")
        if isinstance(ch, dict) and pid in ch:
            out["line_chg"] = ch[pid]
    tp = (sig or {}).get("teampp")
    if isinstance(tp, dict) and isinstance(tp.get(p.get("t")), dict):
        out["teampp"] = {k: tp[p["t"]].get(k) for k in ("pct", "rate", "gp")}
    return out


def goalie_start(p, day_map, sig):
    """Same rule as the app: Daily Faceoff status first, else recent start share."""
    for nm, info in (day_map or {}).items():
        if norm(nm) == norm(p.get("n")):
            st = str((info or {}).get("status") or "").lower()
            for word, prob in DF_START:
                if word in st:
                    return prob, "DF " + word
            return 0.60, "DF " + (st or "unknown")
    if any((i or {}).get("team") == p.get("t") for i in (day_map or {}).values()):
        return 0.05, "DF other goalie named"
    gs = sig.get("gstart")
    share = gs.get("share") if isinstance(gs, dict) else None
    if isinstance(share, (int, float)):
        share = share / 100 if share > 1 else share
        return round(clamp(share, 0, 1), 3), "recent start share"
    return None, "unknown"


def snapshot(root, state, data, now, day_fetch, ai=None):
    ai = ai or {}
    dts = data_time(data)
    age = (now - dts).total_seconds() / 60 if dts else None
    if age is None or age > MAX_INPUT_AGE_MIN or age < -10:
        print(f"(ai) snapshot skipped: espn-data.js is not fresh (age: {None if age is None else round(age)} min)")
        return 0
    today = now.astimezone(ET).date()
    days = [(today + timedelta(days=k)).isoformat() for k in (-1, 0, 1)]
    games = [g for d in days for g in day_fetch(d)]
    played = {(g[s], g["date"]) for g in games for s in ("home", "away")}
    open_games = {}
    for g in games:
        if g["date"] == days[0] or not g.get("gid") or not g.get("start"):
            continue
        if g.get("sched") in DEAD_SCHED or g.get("state") not in ("FUT", "PRE"):
            continue
        lead = (parse_utc(g["start"]) - now).total_seconds() / 60
        if lead < MIN_LEAD_MIN:
            continue
        open_games.setdefault(g["home"], []).append((g, g["away"], True, lead))
        open_games.setdefault(g["away"], []).append((g, g["home"], False, lead))

    model = data.get("model") or {}
    proj, base, odds = model.get("proj") or {}, model.get("base") or {}, model.get("odds") or {}
    sig_all, goalies = data.get("signals") or {}, data.get("goalies") or {}
    ai_proj, ai_gs, ai_rng = ai.get("proj") or {}, ai.get("gstart") or {}, ai.get("range") or {}
    ai_ver = ai.get("versions") or {}
    last = state.setdefault("last", {})
    new_rows = {}
    n_ai = 0
    for p in data.get("players") or []:
        for g, opp, home, lead in open_games.get(p.get("t"), []):
            pid, day = str(p.get("id")), g["date"]
            gm = (proj.get(pid) or {}).get(day)
            espn = espn_eff(p)
            aiv = (ai_proj.get(pid) or {}).get(day)
            if gm is None and espn is None and aiv is None:
                continue  # nothing real to record - never invent a number
            prev_day = (date.fromisoformat(day) - timedelta(days=1)).isoformat()
            sig = signals_for(sig_all, p)
            row = {"v": VERSION, "ts": iso(now), "data_ts": iso(dts), "gid": g["gid"], "date": day,
                   "start": g["start"], "lead_min": round(lead), "pid": pid, "name": p.get("n"),
                   "team": p.get("t"), "pos": p.get("p"), "opp": opp, "home": home,
                   "b2b": (p.get("t"), prev_day) in played, "ft": p.get("ft", 0),
                   "status": p.get("status"), "ir": bool(p.get("ir")),
                   "espn_raw": {k: p.get(k) for k in ("pavg", "avg", "tot", "gp", "own", "chg")},
                   "pred": {"espn": espn, "gm": gm, "blend": blend_of(espn, gm, base.get(pid)), "ai": aiv},
                   "gm_base": base.get(pid), "odds": (odds.get(day) or {}).get(p.get("t")), "sig": sig}
            if aiv is not None:
                n_ai += 1
                grp = "G_cond" if p.get("p") == "G" else ("D" if p.get("p") == "D" else "F")
                row["ai_meta"] = {"asof": ai.get("asof"), "version": ai_ver.get(grp),
                                  "range": (ai_rng.get(pid) or {}).get(day)}
            if p.get("p") == "G":
                sp, why = goalie_start(p, goalies.get(day), sig)
                row["goalie"] = {"start_p": sp, "source": why, "ai_start_p": (ai_gs.get(pid) or {}).get(day)}
            core = {k: v for k, v in row.items() if k not in HASH_SKIP}
            h = hashlib.sha1(json.dumps(core, sort_keys=True, default=str).encode()).hexdigest()[:12]
            key = f"{g['gid']}|{pid}"
            if last.get(key, {}).get("h") == h:
                last[key]["seen"] = iso(now)
                continue
            last[key] = {"h": h, "seen": iso(now), "date": day}
            new_rows.setdefault(day, []).append(row)
    for day, rows in new_rows.items():
        append_rows(P(root, "predictions", f"{day}.jsonl"), rows)
    cutoff = (today - timedelta(days=2)).isoformat()
    state["last"] = {k: v for k, v in last.items() if v.get("date", "") >= cutoff}
    n = sum(len(r) for r in new_rows.values())
    n_games = len({g["gid"] for lst in open_games.values() for g, *_ in lst})
    print(f"(ai) snapshot: {n} new/changed prediction rows ({n_ai} with AI projections) | "
          f"{n_games} upcoming games open for predictions")
    return n


# ----------------------------------------------------------------- stage 2: OBSERVE
def label(root, state, now, day_fetch, stats_fetch):
    lstate = state.setdefault("labels", {})
    pred_dir = P(root, "predictions")
    if not os.path.isdir(pred_dir):
        return []
    today = now.astimezone(ET).date().isoformat()
    done = []
    for fn in sorted(os.listdir(pred_dir)):
        if not fn.endswith(".jsonl"):
            continue
        day = fn[:-6]
        ls = lstate.get(day, {})
        if day > today or ls.get("frozen"):
            continue
        if ls.get("all_final") and ls.get("last") and now - parse_utc(ls["last"]) < timedelta(hours=RELABEL_EVERY_H):
            continue
        games = day_fetch(day)
        if games and all(g.get("sched") in DEAD_SCHED for g in games):
            lstate[day] = {"last": iso(now), "all_final": True, "frozen": True, "games": len(games), "complete": 0}
            continue
        final_ids = {g["gid"] for g in games if g.get("state") in FINAL_STATES and g.get("sched") not in DEAD_SCHED}
        if not final_ids:
            continue
        rows = [r for r in stats_fetch(day) if r.get("gid") in final_ids]
        sk_games = {r["gid"] for r in rows if r["pos"] != "G"}
        g_games = {r["gid"] for r in rows if r["pos"] == "G"}
        complete = {gid for gid in final_ids if gid in sk_games and gid in g_games}
        for r in rows:
            r["fp"] = fantasy_points(r)
        gmap = {str(g["gid"]): {"state": g.get("state"), "sched": g.get("sched"), "home": g.get("home"),
                                "away": g.get("away"), "complete": g["gid"] in complete} for g in games}
        write_json(P(root, "labels", f"{day}.json"),
                   {"date": day, "fetched": iso(now), "games": gmap,
                    "rows": [r for r in rows if r["gid"] in complete]})
        settled = bool(games) and all(g["gid"] in complete or g.get("sched") in DEAD_SCHED for g in games)
        first = ls.get("first_final") or (iso(now) if settled else None)
        frozen = bool(settled and first and now - parse_utc(first) >= timedelta(hours=CORRECTION_HOURS))
        lstate[day] = {"last": iso(now), "all_final": settled, "first_final": first, "frozen": frozen,
                       "games": len(games), "complete": len(complete)}
        done.append(day)
        print(f"(ai) results {day}: {len(complete)}/{len(games)} games final & graded"
              + (" (locked)" if frozen else ""))
    return done


# ----------------------------------------------------------------- stage 3: DIAGNOSE
def official(rows):
    """The official pregame prediction = latest row stamped before puck drop."""
    best, leaked = {}, 0
    for r in rows:
        if not r.get("ts") or not r.get("start") or r["ts"] >= r["start"]:
            leaked += 1
            continue
        k = (r["gid"], r["pid"])
        if k not in best or r["ts"] > best[k]["ts"]:
            best[k] = r
    return best, leaked


def join_day(preds, lab):
    rows = lab.get("rows") or []
    by_nt, by_n, by_lt = {}, {}, {}
    for a in rows:
        by_nt[(a["gid"], norm(a["name"]), a["team"])] = a
        by_n.setdefault((a["gid"], norm(a["name"])), []).append(a)
        by_lt.setdefault((a["gid"], last_name(a["name"]), a["team"], a["pos"] == "G"), []).append(a)
    out, void = [], 0
    for (gid, pid), p in preds.items():
        gi = (lab.get("games") or {}).get(str(gid))
        if not gi:
            continue
        if gi.get("sched") in DEAD_SCHED:
            void += 1
            continue
        if not gi.get("complete"):
            continue
        nm = norm(p.get("name"))
        a, how = by_nt.get((gid, nm, p.get("team"))), "name+team"
        if a is None:
            c = by_n.get((gid, nm), [])
            a, how = (c[0], "name") if len(c) == 1 else (None, None)
        if a is None:
            c = [x for x in by_lt.get((gid, last_name(p.get("name")), p.get("team"), p.get("pos") == "G"), [])
                 if norm(x["name"])[:1] == nm[:1]]
            a, how = (c[0], "last+team") if len(c) == 1 else (None, None)
        pr, gl, sig = p.get("pred") or {}, p.get("goalie") or {}, p.get("sig") or {}
        rng = (p.get("ai_meta") or {}).get("range") or [None, None]
        out.append({"date": p["date"], "gid": gid, "pid": pid, "name": p.get("name"), "team": p.get("team"),
                    "pos": p.get("pos"), "opp": p.get("opp"), "home": p.get("home"), "b2b": p.get("b2b"),
                    "status": p.get("status"), "ft": p.get("ft", 0), "pp1": sig.get("pp1_on"),
                    "pp1_chg": sig.get("pp1_chg"), "top": sig.get("lines_top"), "line": sig.get("line"),
                    "line_chg": sig.get("line_chg"), "lead": p.get("lead_min"),
                    "espn": pr.get("espn"), "gm": pr.get("gm"), "blend": pr.get("blend"), "ai": pr.get("ai"),
                    "ai_lo": rng[0], "ai_hi": rng[1],
                    "start_p": gl.get("start_p"), "ai_start_p": gl.get("ai_start_p"),
                    "played": a is not None, "match": how,
                    "fp": a["fp"] if a else None, "gs": (a or {}).get("GS"), "toi": (a or {}).get("toi"),
                    "nhl_id": (a or {}).get("nhl_id")})
    return out, void


def task_pairs(recs, task, model):
    """(record, error) pairs; error = prediction - actual (positive = over-projected)."""
    out = []
    for r in recs:
        v = r.get(model)
        if v is None:
            continue
        if task == "skater":
            if r["pos"] == "G" or not r["played"]:
                continue
            out.append((r, v - r["fp"]))
        elif task == "goalie_if_start":
            if r["pos"] != "G" or (r.get("gs") or 0) < 1:
                continue
            out.append((r, v - r["fp"]))
        elif task == "goalie_expected":
            if r["pos"] != "G" or r.get("start_p") is None:
                continue
            out.append((r, r["start_p"] * v - (r["fp"] or 0)))
    return out


def summarize(errs):
    n = len(errs)
    if not n:
        return None
    ae = [abs(e) for e in errs]
    mae, bias = sum(ae) / n, sum(errs) / n
    sd_ae = math.sqrt(sum((x - mae) ** 2 for x in ae) / (n - 1)) if n > 1 else 0.0
    sd_e = math.sqrt(sum((x - bias) ** 2 for x in errs) / (n - 1)) if n > 1 else 0.0
    return {"n": n, "mae": round(mae, 3), "mae_se": round(sd_ae / math.sqrt(n), 3),
            "rmse": round(math.sqrt(sum(e * e for e in errs) / n), 3),
            "bias": round(bias, 3), "bias_se": round(sd_e / math.sqrt(n), 3)}


def paired(recs, task, a, b):
    """Same games, two models: mean(|err a| - |err b|). Negative = a is more accurate."""
    ea = {(r["gid"], r["pid"]): e for r, e in task_pairs(recs, task, a)}
    eb = {(r["gid"], r["pid"]): e for r, e in task_pairs(recs, task, b)}
    d = [abs(ea[k]) - abs(eb[k]) for k in ea if k in eb]
    n = len(d)
    if n < 2:
        return None
    m = sum(d) / n
    se = math.sqrt(sum((x - m) ** 2 for x in d) / (n - 1)) / math.sqrt(n)
    if n < 200:
        verdict = "too few games to judge"
    elif m < -2 * se:
        verdict = f"{a} more accurate"
    elif m > 2 * se:
        verdict = f"{b} more accurate"
    else:
        verdict = "no clear difference yet"
    return {"n": n, "diff": round(m, 3), "se": round(se, 3), "verdict": verdict}


def calibration(recs, key):
    gl = [r for r in recs if r["pos"] == "G" and r.get(key) is not None]
    cal = {"n": len(gl)}
    if gl:
        started = [1 if (r.get("gs") or 0) >= 1 else 0 for r in gl]
        cal["brier"] = round(sum((r[key] - s) ** 2 for r, s in zip(gl, started)) / len(gl), 4)
        cal["bins"] = []
        for lo, hi in ((0, 0.2), (0.2, 0.5), (0.5, 0.8), (0.8, 1.01)):
            b = [(r[key], s) for r, s in zip(gl, started) if lo <= r[key] < hi]
            if b:
                cal["bins"].append({"range": f"{lo:.0%}-{min(hi, 1):.0%}", "n": len(b),
                                    "predicted": round(sum(x for x, _ in b) / len(b), 3),
                                    "actual": round(sum(y for _, y in b) / len(b), 3)})
    return cal


SEGMENTS = {
    "position": lambda r: {"D": "defense"}.get(r["pos"], "forward"),
    "venue": lambda r: "home" if r.get("home") else "away",
    "rest": lambda r: "back-to-back" if r.get("b2b") else "rested",
    "injury status": lambda r: "active" if (r.get("status") or "ACTIVE") == "ACTIVE" else "listed " + str(r.get("status")),
    "power play": lambda r: {True: "on PP1", False: "not on PP1"}.get(r.get("pp1"), "unknown"),
    "PP1 change": lambda r: {"added": "just added to PP1", "removed": "just removed from PP1"}.get(r.get("pp1_chg"), "no change"),
    "line": lambda r: r.get("line") or {True: "top line/pair", False: "lower lines"}.get(r.get("top"), "unknown"),
    "line change": lambda r: {"up": "just promoted", "down": "just demoted"}.get(r.get("line_chg"), "no change"),
    "ownership": lambda r: "on a fantasy team" if r.get("ft") else "free agent",
    "team": lambda r: r.get("team"),
    "opponent": lambda r: r.get("opp"),
}


def report(root, state, now):
    lstate = state.get("labels", {})
    pred_dir = P(root, "predictions")
    days = sorted(fn[:-6] for fn in os.listdir(pred_dir) if fn.endswith(".jsonl")) if os.path.isdir(pred_dir) else []
    recs = []
    counts = {"prediction_rows_graded": 0, "official": 0, "leak_blocked": 0, "void": 0,
              "graded_days": 0, "days_waiting": 0}
    for day in days:
        lab_path = P(root, "labels", f"{day}.json")
        if not os.path.exists(lab_path):
            counts["days_waiting"] += 1
            continue
        cache = P(root, "joined", f"{day}.json")
        j = read_json(cache, None) if lstate.get(day, {}).get("frozen") else None
        if j is None or j.get("v") != VERSION:
            rows = read_rows(os.path.join(pred_dir, f"{day}.jsonl"))
            best, leaked = official(rows)
            rs, void = join_day(best, read_json(lab_path, {}))
            j = {"v": VERSION, "day": day, "rows": len(rows), "official": len(best), "leaked": leaked,
                 "void": void, "recs": rs}
            write_json(cache, j)
        recs += j["recs"]
        counts["prediction_rows_graded"] += j["rows"]
        counts["official"] += j["official"]
        counts["leak_blocked"] += j["leaked"]
        counts["void"] += j["void"]
        counts["graded_days"] += 1

    tasks, pairs, segs, flags, best = {}, {}, {}, [], {}
    for task in ("skater", "goalie_if_start", "goalie_expected"):
        tasks[task] = {m: summarize([e for _, e in task_pairs(recs, task, m)]) for m in MODELS}
        pairs[task] = {f"{a}_vs_{b}": paired(recs, task, a, b)
                       for a, b in (("gm", "espn"), ("blend", "espn"), ("blend", "gm"),
                                    ("ai", "espn"), ("ai", "gm"), ("ai", "blend"))}
        ranked = sorted([(m, s) for m, s in tasks[task].items() if s and s["n"] >= 200], key=lambda x: x[1]["mae"])
        if not ranked:
            best[task] = {"model": None, "note": "not enough finished games yet (needs 200+)"}
        else:
            top = ranked[0][0]
            cmp = paired(recs, task, top, ranked[1][0]) if len(ranked) > 1 else None
            clear = bool(cmp and cmp["verdict"].endswith("more accurate"))
            best[task] = {"model": top, "vs": ranked[1][0] if len(ranked) > 1 else None, "detail": cmp,
                          "note": "clearly best" if clear else "lowest error so far, but not clearly better yet"}
    for seg, fn in SEGMENTS.items():
        segs[seg] = {}
        for m in MODELS:
            groups = {}
            for r, e in task_pairs(recs, "skater", m):
                groups.setdefault(fn(r), []).append(e)
            for val, errs in groups.items():
                s = summarize(errs)
                segs[seg].setdefault(val, {})[m] = s
                if s["n"] >= 100 and s["bias_se"] > 0 and abs(s["bias"]) > 2.5 * s["bias_se"]:
                    flags.append({"segment": f"{seg}: {val}", "model": m, "n": s["n"], "bias": s["bias"],
                                  "text": f"{m.upper()} {'over' if s['bias'] > 0 else 'under'}-projects "
                                          f"{val} by {abs(s['bias']):.2f} pts/game ({s['n']} games)",
                                  "status": "exploratory - not yet validated"})

    cov = [r["ai_lo"] <= r["fp"] <= r["ai_hi"] for r in recs
           if r["pos"] != "G" and r["played"] and r.get("ai_lo") is not None and r.get("ai_hi") is not None]
    daily = {}
    for m in MODELS:
        for r, e in task_pairs(recs, "skater", m):
            daily.setdefault(r["date"], {}).setdefault(m, []).append(e)
    daily_out = [dict({"date": d}, **{m: summarize(v) for m, v in sorted(ms.items())}) for d, ms in sorted(daily.items())]

    players = {}
    for r in sorted(recs, key=lambda x: x["date"]):
        if r.get("ft"):
            pl = players.setdefault(r["pid"], {"name": r["name"], "pos": r["pos"], "team": r["team"], "games": []})
            pl["games"].append({k: r.get(k) for k in ("date", "opp", "home", "b2b", "line", "espn", "gm", "blend",
                                                      "ai", "ai_lo", "ai_hi", "start_p", "ai_start_p", "played", "fp")})
    for pl in players.values():
        pl["games"] = pl["games"][-30:]

    reg = read_json(P(root, "models", "registry.json"), {})
    not_played = [r for r in recs if not r["played"] and r["pos"] != "G"]
    rep = {"version": VERSION, "generated": iso(now), "counts": counts,
           "not_played": {"n": len(not_played),
                          "rostered_examples": sorted({r["name"] for r in not_played if r.get("ft")})[:20],
                          "note": "scratched/injured, or a name the engine could not match - check this list"},
           "tasks": tasks, "paired": pairs, "best": best, "segments": segs, "flags": flags,
           "calibration": calibration(recs, "start_p"), "calibration_ai": calibration(recs, "ai_start_p"),
           "ai_range": {"n": len(cov), "coverage": round(sum(cov) / len(cov), 3) if cov else None, "target": 0.8},
           "ai_models": {"production": reg.get("production"), "last_train": reg.get("last_train"),
                         "recent_decisions": (reg.get("history") or [])[-8:],
                         "status": read_json(P(root, "models", "status.json"), {})},
           "daily": daily_out, "players": players, "health": state.get("health", {}),
           "labels": {d: v for d, v in sorted(lstate.items())[-10:]}}
    write_json(P(root, "report.json"), rep)
    with open(P(root, "report.js"), "w", encoding="utf-8") as f:
        f.write("window.AI_REPORT = " + json.dumps(rep, separators=(",", ":")) + ";\n")
    s = tasks["skater"]
    print("(ai) accuracy so far (skaters, avg error pts/game): "
          + ", ".join(f"{m} {s[m]['mae']} (n={s[m]['n']})" for m in MODELS if s.get(m))
          if any(s.values()) else "(ai) accuracy: no finished games graded yet")
    return rep


# ----------------------------------------------------------------- main run
def run(root=HERE, now=None, day_fetch=None, stats_fetch=None):
    now = now or datetime.now(UTC)
    state = read_json(P(root, "state.json"), {})
    health = state.setdefault("health", {})
    errs = []
    dfetch = memo(day_fetch or fetch_day)
    try:
        n = snapshot(root, state, load_espn_data(root), now, dfetch, load_ai(root, now))
        health["last_snapshot_check"] = iso(now)
        if n:
            health["last_snapshot_written"] = iso(now)
    except Exception as ex:
        errs.append(f"snapshot: {type(ex).__name__}: {ex}")
    try:
        if label(root, state, now, dfetch, stats_fetch or fetch_stats):
            health["last_results_graded"] = iso(now)
    except Exception as ex:
        errs.append(f"results: {type(ex).__name__}: {ex}")
    health["last_run"] = iso(now)
    health["recent_errors"] = ([{"at": iso(now), "error": e} for e in errs] + health.get("recent_errors", []))[:20]
    try:
        report(root, state, now)
    except Exception as ex:
        errs.append(f"report: {type(ex).__name__}: {ex}")
    write_json(P(root, "state.json"), state)
    for e in errs:
        print(f"(ai) WARNING {e}")
    return errs


# ----------------------------------------------------------------- tests
def selftest():
    os.environ["GITHUB_ACTIONS"] = "true"
    tmp = tempfile.mkdtemp()
    results = []

    def check(name, cond):
        results.append(bool(cond))
        print(("PASS  " if cond else "FAIL  ") + name)

    try:
        check("skater scoring (1G 2A +1 1PPP 4SOG 1HIT = 22.1)",
              fantasy_points({"pos": "F", "G": 1, "A": 2, "PM": 1, "PPP": 1, "SOG": 4, "HIT": 1}) == 22.1)
        check("goalie scoring (W, 2GA, 28SV = 15.8)",
              fantasy_points({"pos": "G", "W": 1, "GA": 2, "SV": 28}) == 15.8)
        check("goalie shutout scoring (W, 30SV, SO = 28)",
              fantasy_points({"pos": "G", "W": 1, "GA": 0, "SV": 30, "SO": 1}) == 28.0)
        check("OT-loss goalie (OTL, 3GA, 30SV = 10)",
              fantasy_points({"pos": "G", "OTL": 1, "GA": 3, "SV": 30}) == 10.0)
        try:
            sys.path.insert(0, HERE)
            import gm_model
            check("scoring identical to gm_model.py", gm_model.SK == SK and gm_model.GO == GO)
            check("name matching identical to gm_model.py", gm_model.norm("Tim Stützle") == norm("Tim Stützle"))
        except ImportError as ex:
            print(f"SKIP  gm_model comparison ({ex})")

        D = "2026-10-10"
        g1 = {"gid": 1, "date": D, "start": "2026-10-10T23:00:00Z", "state": "FUT", "sched": "OK",
              "home": "VAN", "away": "COL"}
        g2 = {"gid": 2, "date": D, "start": "2026-10-10T17:00:00Z", "state": "LIVE", "sched": "OK",
              "home": "TOR", "away": "MTL"}
        g3 = {"gid": 3, "date": "2026-10-11", "start": "2026-10-11T23:00:00Z", "state": "FUT", "sched": "PPD",
              "home": "EDM", "away": "CGY"}
        world = {D: [g1, g2], "2026-10-11": [g3]}

        def fetch(d):
            return [dict(g) for g in world.get(d, [])]

        def pl(i, n, t, p, pavg, ft=0):
            return {"id": i, "n": n, "t": t, "p": p, "ft": ft, "status": "ACTIVE", "gp": 0, "tot": 0,
                    "avg": 0, "pavg": pavg, "own": 50, "chg": 0}
        players = [pl(1, "Nathan MacKinnon", "COL", "F", 5.0, 4), pl(2, "Quinn Hughes", "VAN", "D", 4.0),
                   pl(3, "Kevin Lankinen", "VAN", "G", 6.0, 4), pl(4, "Auston Matthews", "TOR", "F", 5.0),
                   pl(5, "Thatcher Demko", "VAN", "G", 5.5), pl(6, "Connor McDavid", "EDM", "F", 6.0)]
        now = datetime(2026, 10, 10, 18, 0, tzinfo=UTC)
        data = {"generated": (now - timedelta(minutes=5)).replace(tzinfo=None).isoformat(timespec="seconds"),
                "players": players,
                "model": {"base": {"1": 4.0, "2": 3.0, "3": 6.0, "4": 5.0, "5": 5.5, "6": 5.0},
                          "proj": {"1": {D: 4.5}, "2": {D: 3.0}, "3": {D: 6.0}, "4": {D: 5.0}, "5": {D: 5.5},
                                   "6": {"2026-10-11": 5.0}},
                          "odds": {D: {"VAN": {"win": 0.55, "gf": 3.1, "ga": 2.7}}}},
                "goalies": {D: {"Kevin Lankinen": {"status": "Confirmed", "team": "VAN"}}},
                "signals": {"pp1": {"asof": "x", "on": {"1": True}, "changes": {"1": "added"}, "units": {}},
                            "lines": {"asof": "x", "top": {"1": "F1", "2": "D1"}, "changes": {"2": "up"}},
                            "teampp": {"COL": {"pct": 25.0, "rate": 0.9, "gp": 0, "lastPct": 25.0}},
                            "news": {"1": [{"h": "x", "tone": "+"}]}}}
        write_json(P(tmp, "models", "ai_proj.json"),
                   {"asof": iso(now - timedelta(hours=2)), "versions": {"F": "F-gbm_stats-20261005"},
                    "proj": {"1": {D: 6.1}, "3": {D: 7.0}, "5": {D: 6.5}},
                    "gstart": {"3": {D: 0.7}, "5": {D: 0.3}}, "range": {"1": {D: [0.0, 14.0]}}})
        ai = load_ai(tmp, now)
        check("fresh AI projections are loaded", ai.get("proj", {}).get("1", {}).get(D) == 6.1)
        check("stale AI projections are ignored", load_ai(tmp, now + timedelta(days=3)) == {})

        def write_data():
            with open(os.path.join(tmp, "espn-data.js"), "w", encoding="utf-8") as f:
                f.write("window.ESPN_DATA = " + json.dumps(data) + ";\n")
        write_data()
        state = {}
        snapshot(tmp, state, load_espn_data(tmp), now, fetch, ai)
        rows = read_rows(P(tmp, "predictions", D + ".jsonl"))
        check("records only games that have not started", sorted(r["pid"] for r in rows) == ["1", "2", "3", "5"])
        check("postponed games are not recorded", not os.path.exists(P(tmp, "predictions", "2026-10-11.jsonl")))
        mac = next(r for r in rows if r["pid"] == "1")
        lank = next(r for r in rows if r["pid"] == "3")
        demko = next(r for r in rows if r["pid"] == "5")
        hughes = next(r for r in rows if r["pid"] == "2")
        check("ESPN per-game formula", abs(mac["pred"]["espn"] - 5.0) < 1e-9)
        check("Blend formula", abs(mac["pred"]["blend"] - 5.0625) < 0.001)
        check("AI projection recorded next to ESPN/GM/Blend", mac["pred"]["ai"] == 6.1)
        check("AI range and model version recorded", mac["ai_meta"]["range"] == [0.0, 14.0]
              and mac["ai_meta"]["version"] == "F-gbm_stats-20261005")
        check("player without an AI projection gets none (never invented)", hughes["pred"]["ai"] is None)
        check("PP1 signal and PP1 change attached", mac["sig"].get("pp1_on") is True and mac["sig"].get("pp1_chg") == "added")
        check("exact line (F1/D1) and line change attached", mac["sig"].get("line") == "F1"
              and hughes["sig"].get("line") == "D1" and hughes["sig"].get("line_chg") == "up")
        check("team power-play strength attached", (mac["sig"].get("teampp") or {}).get("pct") == 25.0)
        check("news tone attached", mac["sig"].get("news_tone") == "+")
        check("confirmed goalie = 100% start", lank["goalie"]["start_p"] == 1.0)
        check("other goalie confirmed = 5% start", demko["goalie"]["start_p"] == 0.05)
        check("AI goalie start chance recorded separately", lank["goalie"]["ai_start_p"] == 0.7)
        check("betting odds attached", (hughes.get("odds") or {}).get("win") == 0.55)
        check("timestamp is before puck drop", all(r["ts"] < r["start"] for r in rows))
        check("no duplicate rows when nothing changed",
              snapshot(tmp, state, load_espn_data(tmp), now + timedelta(minutes=10), fetch, ai) == 0)
        data["model"]["proj"]["1"][D] = 5.2
        write_data()
        check("changed projection adds a new timestamped row",
              snapshot(tmp, state, load_espn_data(tmp), now + timedelta(minutes=20), fetch, ai) == 1)
        check("stale espn-data.js is ignored",
              snapshot(tmp, state, load_espn_data(tmp), now + timedelta(hours=3), fetch, ai) == 0)
        data["generated"] = "2026-10-10T23:01:00"
        data["model"]["proj"]["1"][D] = 9.9
        write_data()
        check("nothing recorded after puck drop (even if NHL still says FUT)",
              snapshot(tmp, state, load_espn_data(tmp), datetime(2026, 10, 10, 23, 5, tzinfo=UTC), fetch, ai) == 0)
        mac = [r for r in read_rows(P(tmp, "predictions", D + ".jsonl")) if r["pid"] == "1"][-1]
        bad = dict(mac, ts="2026-10-10T23:30:00Z", pred={"espn": 99, "gm": 99, "blend": 99, "ai": 99})
        append_rows(P(tmp, "predictions", D + ".jsonl"), [bad])
        best, leaked = official(read_rows(P(tmp, "predictions", D + ".jsonl")))
        check("post-start row rejected; official = last pregame row",
              leaked == 1 and best[(1, "1")]["pred"]["gm"] == 5.2 and best[(1, "1")]["pred"]["ai"] == 6.1)

        g1["state"] = "OFF"
        stats = [dict(gid=1, nhl_id=11, name="Nathan MacKinnon", team="COL", pos="F", G=1, A=2, PM=1, PPP=1,
                      SHP=0, SOG=4, HIT=1, BLK=0, toi=1260),
                 dict(gid=1, nhl_id=12, name="Quinn Hughes", team="VAN", pos="D", G=0, A=0, PM=-1, PPP=0,
                      SHP=0, SOG=2, HIT=0, BLK=2, toi=1500),
                 dict(gid=1, nhl_id=13, name="Kevin Lankinen", team="VAN", pos="G", GS=1, W=1, OTL=0, GA=2,
                      SV=28, SO=0, toi=3600),
                 dict(gid=2, nhl_id=14, name="Auston Matthews", team="TOR", pos="F", G=2, A=0, PM=2, PPP=0,
                      SHP=0, SOG=6, HIT=0, BLK=0, toi=1200),
                 dict(gid=2, nhl_id=15, name="Joseph Woll", team="TOR", pos="G", GS=1, W=1, GA=1, SV=25)]
        later = datetime(2026, 10, 11, 12, 0, tzinfo=UTC)
        label(tmp, state, later, fetch, lambda d: [dict(r) for r in stats])
        lab = read_json(P(tmp, "labels", D + ".json"), {})
        check("only officially final games are graded", {r["gid"] for r in lab.get("rows", [])} == {1})
        rep = report(tmp, state, later)
        recs = read_json(P(tmp, "joined", D + ".json"), {}).get("recs", [])
        r1 = next((r for r in recs if r["pid"] == "1"), {})
        r5 = next((r for r in recs if r["pid"] == "5"), {})
        check("actual points joined to the pregame prediction", r1.get("fp") == 22.1 and r1.get("gm") == 5.2)
        check("goalie who did not play is marked as not played", r5.get("played") is False)
        check("skater accuracy computed", rep["tasks"]["skater"]["gm"]["n"] == 2)
        check("AI graded on the same games (only where it made a projection)", rep["tasks"]["skater"]["ai"]["n"] == 1)
        check("AI range coverage measured on real results", rep["ai_range"]["n"] == 1)
        check("goalie start calibration computed (app rule and AI)",
              rep["calibration"]["n"] == 2 and rep["calibration_ai"]["n"] == 2)
        check("exact line used in error breakdown", "F1" in rep["segments"]["line"])
        g2["state"] = "OFF"
        label(tmp, state, later + timedelta(hours=1), fetch, lambda d: [dict(r) for r in stats])
        check("day not locked before correction window ends", not state["labels"][D]["frozen"])
        label(tmp, state, later + timedelta(hours=75), fetch, lambda d: [dict(r) for r in stats])
        check("day locked after 72-hour correction window", state["labels"][D]["frozen"])
        errs = run(tmp, later + timedelta(hours=76), fetch, lambda d: [dict(r) for r in stats])
        check("full run completes without errors", errs == [] and os.path.exists(P(tmp, "report.js")))

        real = os.path.join(HERE, "espn-data.js")
        if os.path.exists(real):
            d = load_espn_data(HERE)
            pls = d.get("players") or []
            check("your real espn-data.js loads and has players", len(pls) > 100)
            proj = (d.get("model") or {}).get("proj") or {}
            if proj:
                check("your GM projections are keyed by ESPN player id",
                      any(str(p.get("id")) in proj for p in pls))
            else:
                print("NOTE  real espn-data.js has no GM projections yet")
            sig = d.get("signals") or {}
            print(f"INFO  signal groups in your data: {sorted(sig)}")
            ex = next((p for p in pls if p.get("ft") == 4), None)
            if ex:
                s = signals_for(sig, ex)
                print(f"INFO  signals found for {ex.get('n')}: {sorted(s)} | line: {s.get('line')} | "
                      f"team PP: {s.get('teampp')}")
                print(f"INFO  ESPN per-game for {ex.get('n')}: {espn_eff(ex)}")
            aip = read_json(os.path.join(HERE, "ai", "models", "ai_proj.json"), {})
            if aip:
                ids = {str(p.get("id")) for p in pls}
                print(f"INFO  your AI projections: made {aip.get('asof')}, {len(aip.get('proj', {}))} players, "
                      f"{len(ids & set(aip.get('proj', {})))} match ESPN players")
            else:
                print("NOTE  no AI projections in the repo yet (they appear after the first AI training run)")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    ok = all(results)
    print(f"\n{sum(results)}/{len(results)} checks passed" + ("" if ok else "  <-- SOMETHING FAILED"))
    return 0 if ok else 1


def livetest():
    """Read-only: prove the NHL endpoints return what the engine expects."""
    results = []

    def check(name, cond):
        results.append(bool(cond))
        print(("PASS  " if cond else "FAIL  ") + name)

    today = datetime.now(ET).date().isoformat()
    print(f"INFO  regular-season games today ({today}): {len(fetch_day(today))}")
    day, games = None, []
    for k in range(1, 15):  # a known stretch of last regular season
        d = (date(2026, 4, 1) + timedelta(days=k)).isoformat()
        games = fetch_day(d)
        if games and all(g["state"] in FINAL_STATES for g in games):
            day = d
            break
    check("found a finished regular-season day to test with", day is not None)
    if day:
        rows = fetch_stats(day)
        sk = [r for r in rows if r["pos"] != "G"]
        gl = [r for r in rows if r["pos"] == "G"]
        print(f"INFO  {day}: {len(games)} games, {len(sk)} skater rows, {len(gl)} goalie rows")
        check("skater rows returned", len(sk) > 20 * len(games))
        check("hits/blocks merged", sum(r["HIT"] for r in sk) > 0 and sum(r["BLK"] for r in sk) > 0)
        check("power-play points present", sum(r["PPP"] for r in sk) > 0)
        check("two starting goalies per game", sum(r["GS"] for r in gl) == 2 * len(games))
        check("stats game ids match schedule game ids",
              {r["gid"] for r in rows} == {g["gid"] for g in games})
        top = max(sk, key=lambda r: fantasy_points(r))
        print(f"INFO  best skater that day: {top['name']} ({top['team']}) = {fantasy_points(top)} fantasy pts")
    ok = all(results)
    print(f"\n{sum(results)}/{len(results)} live checks passed" + ("" if ok else "  <-- SOMETHING FAILED"))
    return 0 if ok else 1


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    if "--livetest" in sys.argv:
        sys.exit(livetest())
    run()
    sys.exit(0)
