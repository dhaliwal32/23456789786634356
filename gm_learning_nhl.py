"""Public NHL API adapters. Official stat rows are required before adding a label.

This layer intentionally does not reconstruct old predictions from current player stats:
training forecasts must have been captured before puck drop.
"""
from __future__ import annotations

from datetime import date, datetime
from zoneinfo import ZoneInfo
import unicodedata
import requests

WEB = "https://api-web.nhle.com/v1"
STATS = "https://api.nhle.com/stats/rest/en"
SEASON = "20262027"
HEADERS = {"User-Agent": "Fantasy-Islands-Projection-Research/1.0"}
ET = ZoneInfo("America/New_York")
ALIASES = {"LAK": "LA", "NJD": "NJ", "SJS": "SJ", "TBL": "TB", "WAS": "WSH",
           "ARI": "UTA", "UTAH": "UTA", "CLB": "CBJ"}


def norm(name):
    val = unicodedata.normalize("NFKD", str(name or "")).encode("ascii", "ignore").decode().lower()
    return " ".join(val.replace(".", "").replace("-", " ").split())


def code(v):
    return ALIASES.get(str(v or "").upper(), str(v or "").upper())


def board(day, session=None):
    s = session or requests
    r = s.get(f"{WEB}/score/{day}", headers=HEADERS, timeout=25)
    r.raise_for_status()
    obj = r.json()
    out = {}
    for g in obj.get("games") or []:
        if g.get("gameType") != 2:  # Only regular-season games, not pre-season or playoffs.
            continue
        try:
            start = datetime.fromisoformat(g["startTimeUTC"].replace("Z", "+00:00"))
        except (ValueError, TypeError, KeyError):
            continue
        home = code((g.get("homeTeam") or {}).get("abbrev"))
        away = code((g.get("awayTeam") or {}).get("abbrev"))
        if not home or not away:
            continue
        finished = g.get("gameState") in ("FINAL", "OFF")
        one = {"id": g.get("id"), "start_utc": start, "finished": finished,
               "game_state": g.get("gameState")}
        out[home] = {**one, "home": 1, "opponent": away}
        out[away] = {**one, "home": 0, "opponent": home}
    return out


def _report(kind, day, session=None):
    s = session or requests
    # The documented isGame=true mode returns per-player, per-game rows.
    params = {"isAggregate": "false", "isGame": "true", "limit": -1,
              "cayenneExp": f'gameDate>="{day}" and gameDate<="{day}" and gameTypeId=2'}
    r = s.get(f"{STATS}/{kind}", headers=HEADERS, params=params, timeout=50)
    r.raise_for_status()
    obj = r.json()
    if not isinstance(obj, dict) or not isinstance(obj.get("data"), list):
        raise ValueError(f"Malformed NHL stats {kind} on {day}; refuse to write outcomes")
    return obj["data"]


def _key(row, name_field):
    """Prefer NHL id; does not depend on ESPN's different player-id namespace."""
    return (str(row.get("playerId", "")), str(row.get("gameId", ""))) if row.get("playerId") else (
        norm(row.get(name_field)), str(row.get("gameId", "")))


def fantasy_scores(day, session=None):
    """Return keyed per-game stats from NHL official summary + realtime reports.

    Fail closed if realtime data is missing: hits and blocks matter in this league.
    """
    from gm_learning_core import num
    skaters = _report("skater/summary", day, session)
    realtime = _report("skater/realtime", day, session)
    goalies = _report("goalie/summary", day, session)
    if not skaters or not realtime or not goalies:
        raise ValueError(f"Incomplete official stats on {day}; will retry on next sync")
    # There must be per-game rows, never accidentally collect season aggregates.
    for sample in (skaters[0], realtime[0], goalies[0]):
        if "gameId" not in sample:
            raise ValueError("NHL response lacks gameId; refusing possible season-total leakage")
    rt = {_key(r, "skaterFullName"): r for r in realtime}
    result = {}
    for r in skaters:
        extra = rt.get(_key(r, "skaterFullName"))
        if extra is None:
            continue  # Unknown hits/blocks must NOT quietly become zero.
        keys = ("goals", "assists", "plusMinus", "ppPoints", "shPoints", "shots")
        if any(num(r.get(k)) is None for k in keys):
            continue
        hits = num(extra.get("hits"))
        blocks = num(extra.get("blockedShots"), num(extra.get("blockedShotAttempts")))
        if hits is None or blocks is None:
            continue
        pts = (6*r["goals"] + 4*r["assists"] + 2*r["plusMinus"] +
               2*r["ppPoints"] + 3*r["shPoints"] + r["shots"] + .1*hits + blocks)
        result[(norm(r.get("skaterFullName")), code(r.get("teamAbbrevs")))] = {
            "actual": round(float(pts), 2), "played": 1,
            "nhl_player_id": r.get("playerId"), "game_id": r.get("gameId")}
    for r in goalies:
        fields = ("saves", "goalsAgainst", "wins", "otLosses", "shutouts")
        if any(num(r.get(k)) is None for k in fields):
            continue
        pts = (5*r["wins"] - 3*r["goalsAgainst"] + .6*r["saves"] +
               5*r["shutouts"] + r["otLosses"])
        started = num(r.get("gamesStarted"))
        result[(norm(r.get("goalieFullName")), code(r.get("teamAbbrevs")))] = {
            "actual": round(float(pts), 2), "played": 1,
            "started": int(started > 0) if started is not None else None,
            "nhl_player_id": r.get("playerId"), "game_id": r.get("gameId")}
    if not result:
        raise ValueError(f"Official rows on {day} did not resolve to fantasy scores")
    return result


def labels_for_snapshots(snapshots, games, official):
    """Labels only final team games. No nonappearance zeros in points-if-playing model."""
    outcome = {}
    for row in snapshots:
        game = games.get(row["team"])
        if not game or not game["finished"]:
            continue
        raw = official.get((norm(row["name"]), code(row["team"])))
        label = {"date": row["date"], "player_id": row["player_id"],
                 "game_id": game["id"], "played": 0}
        if raw is not None and (raw.get("game_id") is None or
                                str(raw["game_id"]) == str(game["id"])):
            label.update(raw)
        # Non-starter goalie is a real 0 for start-probability, not points-per-appearance.
        if row["position"] == "G" and game["finished"]:
            if label.get("started") is None and not label["played"]:
                label["started"] = 0
        outcome[row["player_id"]] = label
    return outcome


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python3 gm_learning_nhl.py YYYY-MM-DD (finished NHL regular-season date)")
    day = sys.argv[1]
    date.fromisoformat(day)
    try:
        board_rows = board(day)
        scores = fantasy_scores(day)
        print(f"(learning-check) {day}: {len(board_rows)//2} NHL games, "
              f"{sum(g['finished'] for g in board_rows.values())//2} final; "
              f"{len(scores)} player-game rows with exact Fantasy Islands scoring fields")
        print("(learning-check) Data schema verified for this date. Compare a few results with ESPN.")
    except Exception as exc:
        raise SystemExit(f"(learning-check) NHL adapter requires review: {exc}")
