"""Fantasy Islands adaptive-learning orchestrator.

Install as an additional module, never replacing the existing GM baseline.
Called in espn_sync.py AFTER model and signals have been built, BEFORE writing JS.
Writes only PUBLIC fantasy predictions and outcomes; no tokens, cookies or secrets.
"""
from __future__ import annotations

from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo
import json
import os
import tempfile

import gm_learning_core as core
import gm_learning_nhl as nhl

HERE = Path(__file__).resolve().parent
ROOT = HERE / "learning_data"
SNAPS = ROOT / "snapshots"
OUTCOMES = ROOT / "outcomes"
MODELS = ROOT / "models"
REPORT = ROOT / "report.json"
MODEL_META = ROOT / "model_meta.json"
ET = ZoneInfo("America/New_York")


def read_json(p, fallback=None):
    try:
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return fallback


def write_json(path, item):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(item, indent=1, sort_keys=True, ensure_ascii=False, allow_nan=False) + "\n"
    if path.exists() and path.read_text(encoding="utf-8") == text:
        return
    fd, temp = tempfile.mkstemp(prefix="tmp-learning-", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(text)
        os.replace(temp, path)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)


def board_cached(day, cache):
    if day not in cache:
        cache[day] = nhl.board(day)
    return cache[day]


def pending_days(today):
    return sorted(d.stem for d in SNAPS.glob("????-??-??.json") if
                  d.stem < today and not (OUTCOMES / f"{d.stem}.json").exists())


def settle_completed(cache, today):
    result = {"days_labeled": [], "pending_days": [], "warnings": []}
    # Process a few days per run; if the official NHL API has no data, retry later.
    for day in pending_days(today)[:14]:
        snapshots = read_json(SNAPS / f"{day}.json", [])
        if not snapshots:
            continue
        try:
            games = board_cached(day, cache)
            needed = {s["team"] for s in snapshots}
            if not all(games.get(t, {}).get("finished") for t in needed):
                result["pending_days"].append(day)
                continue
            official = nhl.fantasy_scores(day)
            labels = nhl.labels_for_snapshots(snapshots, games, official)
            if not labels or not any(r.get("played") for r in labels.values()):
                raise ValueError("No matching player stats; review name/team mapping or NHL response")
            # Do not accept unusually sparse labels after a likely API schema change.
            skaters = [s for s in snapshots if s["position"] != "G"]
            matched = sum(1 for s in skaters if labels.get(s["player_id"], {}).get("played"))
            if skaters and matched / len(skaters) < .55:
                raise ValueError(f"Only {matched}/{len(skaters)} skaters matched; possible API schema drift")
            write_json(OUTCOMES / f"{day}.json", labels)
            result["days_labeled"].append(day)
            print(f"(learning) final {day}: {sum(bool(x.get('played')) for x in labels.values())} appearances labeled")
        except Exception as e:
            result["warnings"].append(f"{day}: {e}")
            result["pending_days"].append(day)
            print(f"(learning) outcomes delayed {day}: {e}")
    stale = [day for day in pending_days(today) if day < (date.fromisoformat(today) - timedelta(days=7)).isoformat()]
    if stale:
        result["warnings"].append(f"Stale unlabeled prediction days: {', '.join(stale[:5])}")
    return result


def sample_rows():
    result = []
    for p in sorted(OUTCOMES.glob("????-??-??.json")):
        day = p.stem
        snaps = read_json(SNAPS / f"{day}.json", [])
        outcomes = read_json(p, {})
        for snap in snaps:
            label = outcomes.get(snap["player_id"])
            if label is None:
                continue
            result.append({**snap, **label})
    return result


def update_models(rows):
    import joblib
    meta = read_json(MODEL_META, {"groups": {}, "start": {}, "last_train_key": ""})
    fingerprint = f"{len(rows)}:{max((r['date'] for r in rows), default='')}"
    if fingerprint == meta.get("last_train_key"):
        return meta, read_json(REPORT, {}).get("training", {})
    training = {}
    for group in ("F", "D", "G"):
        old = meta.get("groups", {}).get(group)
        report, bundle = core.train_group(rows, group, str(MODELS), old)
        training[group] = report
        if bundle:
            MODELS.mkdir(parents=True, exist_ok=True)
            temp = MODELS / f".{group}.tmp.joblib"
            joblib.dump(bundle, temp)
            temp.replace(MODELS / f"{group}.joblib")
            meta.setdefault("groups", {})[group] = {
                k: v for k, v in bundle.items() if k != "model" and k != "features"}
            print(f"(learning) PROMOTED {group} {bundle['kind']}/{bundle['family']}")
    start_report, start_bundle = core.learn_start(rows, str(MODELS), meta.get("start"))
    training["start_probability"] = start_report
    if start_bundle:
        MODELS.mkdir(parents=True, exist_ok=True)
        temp = MODELS / ".start.tmp.joblib"
        joblib.dump(start_bundle, temp)
        temp.replace(MODELS / "start.joblib")
        meta["start"] = {k: v for k, v in start_bundle.items() if k not in ("model", "features")}
        print("(learning) PROMOTED goalie start probability")
    meta["last_train_key"] = fingerprint
    write_json(MODEL_META, meta)
    return meta, training


def load_champions():
    import joblib
    active = {}
    for group in ("F", "D", "G", "start"):
        path = MODELS / f"{group}.joblib"
        if path.exists():
            try:
                obj = joblib.load(path)  # Load ONLY files from your own trusted repository.
                if isinstance(obj, dict) and "model" in obj and "features" in obj:
                    active[group] = obj
            except Exception as e:
                print(f"(learning) corrupt {group} model, using legacy baseline: {e}")
    return active


def predict(champion, row):
    # Consistent with training: prediction = frozen blend baseline + learned residual.
    import numpy as np
    X = core.matrix([row], champion["features"])
    return round(float(max(0, row["features"]["blend_proj"] +
                           champion["model"].predict(X)[0])), 3)


def start_chance(champions, row):
    start_model = champions.get("start")
    fallback = core.num(row["features"].get("start_base"))
    if fallback is None:
        return None
    if start_model:
        try:
            val = start_model["model"].predict_proba(core.matrix([row], start_model["features"]))[0, 1]
            return round(core.clip(float(val), .01, .99), 3)
        except Exception:
            pass
    return round(fallback, 3)


def make_feature_row(data, p, dt, game, now=None):
    feats = core.features_for(data, p, dt, game)
    if feats is None:
        return None
    return {"date": dt, "player_id": str(p["id"]), "name": p["n"], "team": p["t"],
            "position": p["p"], "pregame_utc": (now or datetime.now(timezone.utc)).isoformat(),
            "game_id": game["id"], "features": feats}


def freeze_predictions(data, boards, champions, now):
    taken = 0
    today, tomorrow = now.astimezone(ET).date(), now.astimezone(ET).date() + timedelta(days=1)
    for day in (today, tomorrow):
        dt = day.isoformat()
        games = boards.get(dt) or {}
        if not games:
            continue
        file = SNAPS / f"{dt}.json"
        snapshots = read_json(file, [])
        by_id = {s["player_id"]: s for s in snapshots}
        for p in data.get("players", []):
            pid = str(p.get("id"))
            game = games.get(p.get("t"))
            if not game or pid in by_id or p.get("p") not in ("F", "D", "G"):
                continue
            horizon = (game["start_utc"] - now).total_seconds() / 3600
            # Same pregame horizon across training and deployment. Never record after puck drop.
            if not (1.5 <= horizon <= 3.5):
                continue
            prior_date = (day - timedelta(days=1)).isoformat()
            was_yesterday = p["t"] in (boards.get(prior_date) or {})
            frow = make_feature_row(data, p, dt, {**game, "b2b": int(was_yesterday)}, now)
            if not frow:
                continue
            champion = champions.get(p["p"])
            if champion:
                try:
                    frow["champion_prediction"] = predict(champion, frow)
                except Exception as exc:
                    print(f"(learning) could not snapshot champion for {p['n']}: {exc}")
            if p["p"] == "G":
                frow["start_probability_snapshot"] = start_chance(champions, frow)
            by_id[pid] = frow
            taken += 1
        if len(by_id) != len(snapshots):
            write_json(file, sorted(by_id.values(), key=lambda s: s["player_id"]))
    return taken


def apply_to_upcoming(data, boards, champions, now):
    # Preserve unmodified GM output for complete transparency and easy rollback.
    original = data.get("model") or {}
    raw_proj = original.get("proj") or {}
    changes = {"F": 0, "D": 0, "G": 0}
    start_prob = {}
    new_proj = {pid: dict(days) for pid, days in raw_proj.items()}
    today = now.astimezone(ET).date()
    for offset in range(2):
        day = today + timedelta(days=offset)
        dt = day.isoformat()
        games = boards.get(dt) or {}
        for p in data.get("players", []):
            pid = str(p.get("id"))
            group = p.get("p")
            if pid not in new_proj or dt not in new_proj[pid] or p.get("t") not in games:
                continue
            game = games[p["t"]]
            if (game["start_utc"] - now).total_seconds() < 60 * 5:
                continue  # Never retroactively revise already-started game predictions.
            prior = boards.get((day - timedelta(days=1)).isoformat()) or {}
            row = make_feature_row(data, p, dt, {**game, "b2b": int(p["t"] in prior)}, now)
            if not row:
                continue
            if group in champions:
                try:
                    value = predict(champions[group], row)
                    # Breaker: do not let a noisy retraining result produce outlandish changes.
                    baseline = row["features"]["gm_proj"]
                    if value <= max(15, baseline * 3) and value >= 0:
                        new_proj[pid][dt] = value
                        changes[group] += 1
                except Exception as exc:
                    print(f"(learning) projection fallback {p['n']}: {exc}")
            if group == "G":
                chance = start_chance(champions, row)
                if chance is not None:
                    start_prob.setdefault(pid, {})[dt] = chance
    if sum(changes.values()):
        original["legacyProj"] = raw_proj
        original["proj"] = new_proj
    return changes, start_prob


def diagnostics(rows):
    # Purely pregame forecasts vs postgame labels, with live promoted forecasts isolated.
    played = [r for r in rows if r.get("played") and core.num(r.get("actual")) is not None]
    result = {}
    for group in ("F", "D", "G"):
        part = [r for r in played if r["position"] == group]
        if not part:
            continue
        result[group] = {"games": len(part), "baseline_mae": core.score_baselines(part)}
        frozen = [r for r in part if core.num(r.get("champion_prediction")) is not None]
        if frozen:
            result[group]["deployed_mae"] = round(core.mae(
                [r["actual"] for r in frozen], [r["champion_prediction"] for r in frozen]), 3)
            result[group]["deployed_examples"] = len(frozen)
        for key in ("home", "back_to_back", "goalie_confirmed"):
            eligible = [r for r in part if r["features"].get(key) is not None]
            if len(eligible) < 30:
                continue
            by = {}
            for flag in (0, 1):
                examples = [r for r in eligible if int(r["features"][key]) == flag]
                if len(examples) >= 12:
                    by[str(flag)] = {"n": len(examples), "gm_mae": round(core.mae(
                        [r["actual"] for r in examples], [r["features"]["gm_proj"] for r in examples]), 3)}
            if by:
                result[group].setdefault("slices", {})[key] = by
    return result



def research_queue(rows):
    """Automatically propose *testable hypotheses*, never claim causal discoveries.

    A suggested new source still needs a genuine pregame adapter before it can be trained.
    """
    played = [r for r in rows if r.get("played") and core.num(r.get("actual")) is not None]
    if len(played) < 60:
        return [{"topic": "Accumulate unbiased pregame data",
                 "evidence": f"{len(played)} completed player-games captured so far",
                 "next_test": "Continue collecting forecasts before game start; never backfill past ESPN predictions from today's values."}]
    recent_days = sorted({r["date"] for r in played})[-21:]
    recent = [r for r in played if r["date"] in recent_days]
    ideas = []
    def add(topic, evidence, next_test):
        ideas.append({"topic": topic, "evidence": evidence, "next_test": next_test})
    for feature, topic, suggestion in [
        ("recent_fpg", "Recent-form data coverage", "Verify the recent-points mapping in gm_signals and freeze it before puck drop."),
        ("toi_last", "Player usage / ice time", "Check TOI extraction; consider separate even-strength and PP ice time if available pregame."),
        ("odds_win", "Pregame betting odds completeness", "Compare models with and without opening/near-start odds; monitor monthly API quotas.")]:
        missing = sum(core.num(r["features"].get(feature)) is None for r in recent)
        if recent and missing/len(recent) >= .45:
            add(topic, f"Missing for {missing}/{len(recent)} recent completed appearances",
                suggestion)
    for pos in ("F", "D", "G"):
        part = [r for r in recent if r["position"] == pos]
        if len(part) < 50:
            continue
        for feature, label, new_signal in [
            ("back_to_back", "Rest and fatigue", "Capture the exact days since last game, opponent rest and travel; test on future pregame snapshots."),
            ("home", "Home/away context", "Test referee, last-change / matchups or opponent effects as separately timestamped inputs.")]:
            left = [r for r in part if r["features"].get(feature) == 0]
            right = [r for r in part if r["features"].get(feature) == 1]
            if min(len(left),len(right)) < 20:
                continue
            err = lambda rs: core.mae([r["actual"] for r in rs], [r["features"]["gm_proj"] for r in rs])
            a,b = err(left),err(right)
            if abs(a-b) >= .75:
                add(f"{label} ({pos})", f"Historical GM errors by flag: {a:.2f} vs {b:.2f} fantasy points",
                    new_signal)
    if not ideas:
        add("Candidate features", "No sufficiently large error or completeness gap currently isolated",
            "Collect pregame power-play deployment, opponent penalty kill, linemates and confirmed goalie information when reliable; let the chronological tests decide if they help.")
    return ideas[:7]



def pause_models_on_drift(rows, meta):
    """Disable a deployed champion if *later live* forecasts substantially lag baselines."""
    paused = []
    for group, n_min in (("F", 90), ("D", 45), ("G", 24)):
        champion = (meta.get("groups") or {}).get(group)
        if not champion:
            continue
        since = champion.get("trained_through", "")
        seen = [r for r in rows if r.get("position") == group and r.get("played") and
                r["date"] > since and core.num(r.get("champion_prediction")) is not None]
        last_dates = sorted({r["date"] for r in seen})[-7:]
        recent = [r for r in seen if r["date"] in last_dates]
        if len(last_dates) < 5 or len(recent) < n_min:
            continue
        champion_mae = core.mae([r["actual"] for r in recent],
                                [r["champion_prediction"] for r in recent])
        reference = min(core.score_baselines(recent).values())
        if champion_mae > reference * 1.15 and champion_mae - reference >= .40:
            if not champion.get("paused"):
                champion["paused"] = True
                champion["pause_reason"] = (f"Live post-promotion error {champion_mae:.2f} vs "
                                            f"strongest baseline {reference:.2f} across {len(recent)} games")
                paused.append(group)
    if paused:
        write_json(MODEL_META, meta)
    return paused


def write_dashboard_report(report):
    write_json(REPORT, report)
    path = HERE / "learning-report.js"
    text = "window.LEARNING_REPORT = " + json.dumps(report, separators=(",", ":"), allow_nan=False) + ";\n"
    if not path.exists() or path.read_text(encoding="utf-8") != text:
        path.write_text(text, encoding="utf-8")


def run(data):
    """Fail-safe integration: returns the existing data augmented with learning results.

    A source failure never changes the old model; a supervised model is not used
    until it passes held-out chronological evaluation.
    """
    now = datetime.now(timezone.utc)
    today = now.astimezone(ET).date().isoformat()
    cache = {}
    health = {"boards": [], "warnings": []}
    # Today, tomorrow, and yesterday are needed to detect back-to-backs.
    for i in (-1, 0, 1):
        day = (date.fromisoformat(today) + timedelta(days=i)).isoformat()
        try:
            board_cached(day, cache)
            health["boards"].append(day)
        except Exception as exc:
            health["warnings"].append(f"NHL scoreboard {day}: {exc}")
    settled = settle_completed(cache, today)
    health["warnings"].extend(settled["warnings"])
    rows = sample_rows()
    try:
        meta, training = update_models(rows)
    except Exception as exc:
        meta, training = read_json(MODEL_META, {}), {}
        health["warnings"].append(f"Training failed: {exc}; existing models retained")
    paused = pause_models_on_drift(rows, meta)
    active = load_champions()
    # A paused scorer falls back to the tested original baseline; keep its model for audit.
    for group in paused + [g for g in ("F", "D", "G") if (meta.get("groups") or {}).get(g, {}).get("paused")]:
        active.pop(group, None)
    taken = freeze_predictions(data, cache, active, now)
    changes, goalie_starts = apply_to_upcoming(data, cache, active, now)
    report = {"version": "1.0", "asof": now.isoformat(), "snapshots": sum(
                len(read_json(p, [])) for p in SNAPS.glob("????-??-??.json")),
              "labeled_appearances": sum(bool(r.get("played")) for r in rows),
              "new_snapshots": taken, "outcomes_added": settled["days_labeled"],
              "pending_outcomes": settled["pending_days"], "health": health,
              "trained": {g: meta.get("groups", {}).get(g) for g in ("F", "D", "G")},
              "start_model": meta.get("start", {}), "training": training,
              "accuracy": diagnostics(rows), "drift_paused": paused,
              "research_queue": research_queue(rows),
              "applied_today_tomorrow": changes,
              "notes": ["Models predict points GIVEN an NHL appearance; goalie starting chance is separate.",
                        "Only game-day, genuinely pregame snapshots become supervised training records.",
                        "Betting odds and signals are trained only when present at snapshot time."]}
    write_dashboard_report(report)
    data["learning"] = {"asof": now.isoformat(), "snapshot_count": report["snapshots"],
                        "training_examples": report["labeled_appearances"],
                        "champions": report["trained"], "applied": changes,
                        "goalieStartProb": goalie_starts, "warnings": health["warnings"][:5]}
    print(f"(learning) pregame snapshots={report['snapshots']} new={taken} labeled={report['labeled_appearances']} applied={changes}")
    return data


if __name__ == "__main__":
    rows = sample_rows()
    print(json.dumps({"snapshots": sum(len(read_json(p, [])) for p in SNAPS.glob("*.json")),
                      "rows": len(rows), "accuracy": diagnostics(rows)}, indent=2))
