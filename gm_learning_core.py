"""Feature engineering + safely gated adaptive residual learning (no network)."""
from __future__ import annotations

from datetime import date
import math
import os
import warnings

FEATURE_GROUPS = {
    "base": ["gm_proj", "espn_proj", "blend_proj", "season_avg", "season_gp"],
    "context": ["gm_proj", "espn_proj", "blend_proj", "season_avg", "season_gp",
                "gm_matchup_ratio", "home", "back_to_back", "odds_win", "odds_gf", "odds_ga"],
    "signals": ["gm_proj", "espn_proj", "blend_proj", "season_avg", "season_gp",
                "gm_matchup_ratio", "home", "back_to_back", "odds_win", "odds_gf", "odds_ga",
                "recent_fpg", "toi_last", "toi_delta", "pp_toi_last", "pp_toi_delta",
                "goalie_start_share", "goalie_confirmed", "goalie_other_confirmed",
                "team_pp", "ownership", "ownership_change"],
}
START_FEATURES = ["goalie_start_share", "goalie_confirmed", "goalie_other_confirmed",
                  "home", "back_to_back", "odds_win", "season_gp"]
MIN_EXAMPLES = {"F": 240, "D": 120, "G": 90}
MIN_DATES = 12


def num(x, default=None):
    try:
        if isinstance(x, bool):
            return float(x)
        v = float(x)
        return v if math.isfinite(v) else default
    except (TypeError, ValueError):
        return default


def clip(v, lo, hi):
    return max(lo, min(hi, v))


def get_signal(signals, group, player, default=None):
    """Supports keyed ESPN IDs, names, or (where appropriate) team keys."""
    bucket = (signals or {}).get(group) or {}
    if not isinstance(bucket, dict):
        return default
    for key in (str(player.get("id")), player.get("id"), player.get("n"),
                (player.get("n") or "").lower()):
        if key in bucket:
            return bucket[key]
    if group == "teampp":
        return bucket.get(player.get("t"), default)
    return default


def nested_num(obj, *names):
    if isinstance(obj, (int, float)):
        return num(obj)
    if not isinstance(obj, dict):
        return None
    for k in names:
        if k in obj and num(obj[k]) is not None:
            return num(obj[k])
    return None


def goalie_start_features(goalies, day, player, share=None):
    team_starters = (goalies or {}).get(day) or {}
    if not isinstance(team_starters, dict):
        team_starters = {}
    import unicodedata
    def n(s):
        return unicodedata.normalize("NFKD", str(s or "")).encode("ascii", "ignore").decode().casefold().replace(".", "").strip()
    mine, other = None, False
    for name, row in team_starters.items():
        if not isinstance(row, dict) or row.get("team") != player.get("t"):
            continue
        status = str(row.get("status", "")).lower()
        if n(name) == n(player.get("n")):
            mine = status
        elif "confirm" in status and "unconfirm" not in status:
            other = True
    confirmed = (mine is not None and "confirm" in mine and "unconfirm" not in mine)
    base = .99 if confirmed else (.02 if other else (.85 if mine and any(
        w in mine for w in ("likely", "expected", "probable")) else (num(share) if num(share) is not None else .5)))
    share = num(share)
    if share is not None and 1 < share <= 100:
        share /= 100.0  # Accept either 0-1 or 0-100 input for historical start share.
    if not confirmed and not other and share is not None and (mine is None or not any(
            w in mine for w in ("likely", "expected", "probable"))):
        base = share
    return {"goalie_start_share": share, "goalie_confirmed": float(confirmed),
            "goalie_other_confirmed": float(other), "start_base": clip(base, .01, .99)}


def features_for(data, player, dt, game):
    """All information must come from a *pregame* version of data, never later."""
    model = data.get("model") or {}
    pid = str(player.get("id"))
    gm = num((model.get("proj") or {}).get(pid, {}).get(dt))
    if gm is None:  # No GM prediction => no supervised baseline to improve safely.
        return None
    base = num((model.get("base") or {}).get(pid))
    espn = num(player.get("pavg"))
    if espn is not None and espn <= 0:
        espn = None  # Missing ESPN projection must not count as an actual zero forecast.
    adjusted = (espn * clip(gm / base, .5, 1.6)) if espn is not None and base and base > 0 else espn
    blend = ((gm + adjusted) / 2) if adjusted is not None and adjusted > 0 else gm
    odds = ((model.get("odds") or {}).get(dt) or {}).get(player.get("t")) or {}
    signals = data.get("signals") or {}
    recent = get_signal(signals, "recent", player)
    toi = get_signal(signals, "toi", player)
    teampp = get_signal(signals, "teampp", player)
    gs = get_signal(signals, "gstart", player)
    share = nested_num(gs, "share", "s")
    st = goalie_start_features(data.get("goalies"), dt, player, share) if player.get("p") == "G" else {}
    f = {
        "gm_proj": gm, "espn_proj": adjusted, "espn_raw_proj": espn, "blend_proj": blend,
        "season_avg": num(player.get("avg")), "season_gp": num(player.get("gp")),
        "gm_matchup_ratio": clip(gm / base, .5, 1.6) if base and base > 0 else None,
        "home": num(game.get("home")), "back_to_back": num(game.get("b2b")),
        "odds_win": num(odds.get("win")), "odds_gf": num(odds.get("gf")),
        "odds_ga": num(odds.get("ga")),
        "recent_fpg": nested_num(recent, "fpg", "avg", "pts", "fp"),
        "toi_last": nested_num(toi, "r", "recent"), "toi_delta": nested_num(toi, "d", "delta"),
        "pp_toi_last": nested_num(toi, "pr", "pp_recent"), "pp_toi_delta": nested_num(toi, "pd", "pp_delta"),
        "team_pp": nested_num(teampp, "pct", "pp", "ppPct", "pp_percent"),
        "ownership": num(player.get("own")), "ownership_change": num(player.get("chg")),
        "goalie_start_share": st.get("goalie_start_share"),
        "goalie_confirmed": st.get("goalie_confirmed"),
        "goalie_other_confirmed": st.get("goalie_other_confirmed"),
        "start_base": st.get("start_base"),
    }
    return f


def matrix(rows, features):
    import numpy as np
    return np.asarray([[num(row.get("features", {}).get(k), float("nan"))
                        for k in features] for row in rows], dtype=float)


def mae(actual, pred):
    return sum(abs(a - b) for a, b in zip(actual, pred)) / max(len(actual), 1)


def score_baselines(rows):
    labels = [r["actual"] for r in rows]
    candidates = {}
    for col in ("gm_proj", "blend_proj", "espn_raw_proj", "espn_proj"):
        usable = [r for r in rows if num(r.get("features", {}).get(col)) is not None]
        if len(usable) >= len(rows) * .95:
            candidates[col] = round(mae([r["actual"] for r in usable],
                                         [r["features"][col] for r in usable]), 4)
    return candidates


def _dates_split(rows):
    dates = sorted({r["date"] for r in rows})
    if len(dates) < MIN_DATES:
        return None
    # Date-grouped training, tuning and untouched latest holdout.
    tr_end = max(5, int(len(dates) * .60))
    tune_end = max(tr_end + 2, int(len(dates) * .80))
    if len(dates) - tune_end < 2:
        return None
    return ([r for r in rows if r["date"] < dates[tr_end]],
            [r for r in rows if dates[tr_end] <= r["date"] < dates[tune_end]],
            [r for r in rows if r["date"] >= dates[tune_end]])


def _candidate(kind, strength=1):
    from sklearn.pipeline import make_pipeline
    from sklearn.impute import SimpleImputer
    from sklearn.preprocessing import StandardScaler
    from sklearn.linear_model import Ridge
    from sklearn.ensemble import HistGradientBoostingRegressor
    if kind == "ridge":
        return make_pipeline(SimpleImputer(strategy="median", keep_empty_features=True),
                             StandardScaler(), Ridge(alpha=80 * strength))
    return HistGradientBoostingRegressor(max_iter=130, learning_rate=.045,
                                         max_leaf_nodes=8, min_samples_leaf=36,
                                         l2_regularization=12, random_state=19)


def _fit(rows, features, kind):
    import numpy as np
    # Fit residuals, preserving the current prediction as a strong prior.
    y = np.asarray([r["actual"] - r["features"]["blend_proj"] for r in rows])
    X = matrix(rows, features)
    if kind == "tree":
        model = _candidate(kind)
    else:
        model = _candidate("ridge")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        model.fit(X, y)
    return model


def predictions(model, rows, features):
    import numpy as np
    raw = np.asarray([r["features"]["blend_proj"] for r in rows])
    return np.maximum(0, raw + model.predict(matrix(rows, features)))


def feature_impact(model, tune, keys):
    """Descriptive permutation impact; associations are not causal claims."""
    import numpy as np
    if not tune:
        return []
    x = matrix(tune, keys)
    actual = np.asarray([r["actual"] for r in tune])
    base = np.asarray([r["features"]["blend_proj"] for r in tune])
    baseline_error = mae(actual, np.maximum(0, base + model.predict(x)))
    rng = np.random.default_rng(24)
    result = []
    for index, feature in enumerate(keys):
        observed = x[:, index]
        if np.sum(np.isfinite(observed)) < len(observed) * .2:
            continue
        errors = []
        for _ in range(3):
            z = x.copy()
            z[:, index] = rng.permutation(z[:, index])
            errors.append(mae(actual, np.maximum(0, base + model.predict(z))))
        delta = sum(errors) / len(errors) - baseline_error
        if delta > .01:
            result.append({"feature": feature, "permutation_mae_increase": round(float(delta), 3)})
    return sorted(result, key=lambda x: -x["permutation_mae_increase"])[:7]


def train_group(rows, group, model_dir, current_meta):
    """Train and promote only when the most recent chronological holdout beats baselines.

    Old deployed predictions stored BEFORE actual results are the comparison when available.
    """
    rows = sorted([r for r in rows if r.get("position") == group and
                   r.get("played") and num(r.get("actual")) is not None and
                   num(r.get("features", {}).get("blend_proj")) is not None],
                  key=lambda r: (r["date"], str(r.get("player_id"))))
    report = {"examples": len(rows), "dates": len({r["date"] for r in rows}),
              "status": "collecting", "current": current_meta or {}}
    if len(rows) < MIN_EXAMPLES[group]:
        report["need_examples"] = MIN_EXAMPLES[group]
        return report, None
    split = _dates_split(rows)
    if split is None:
        report["need_dates"] = MIN_DATES
        return report, None
    train, tune, hold = split
    if len(train) < 40 or len(tune) < 10 or len(hold) < 12:
        return report, None
    target = [r["actual"] for r in hold]
    baselines = score_baselines(hold)
    if not baselines:
        return report, None
    best_base = min(baselines.values())
    report.update({"baseline_mae": baselines, "holdout_examples": len(hold),
                   "holdout_dates": sorted({r["date"] for r in hold}),
                   "status": "tested"})
    choices = []
    for family, keys in FEATURE_GROUPS.items():
        informative = sum(1 for key in keys if any(
            num(r.get("features", {}).get(key)) is not None for r in train))
        if informative < 3:
            continue
        for kind in ("ridge", "tree"):
            if kind == "tree" and len(train) < 350:
                continue
            try:
                est = _fit(train, keys, kind)
                err = mae([r["actual"] for r in tune], predictions(est, tune, keys))
                choices.append((err, kind, family, keys))
            except Exception as exc:
                print(f"(learning) {group} {kind} {family} skipped: {exc}")
    if not choices:
        return report, None
    tune_err, kind, family, keys = min(choices, key=lambda x: x[0])
    try:
        selected = _fit(train + tune, keys, kind)
        predict = predictions(selected, hold, keys)
    except Exception as exc:
        print(f"(learning) {group} failed after tuning: {exc}")
        return report, None
    hold_error = mae(target, predict)
    # Compare to *genuinely pregame* forecasts made by any deployed champion.
    deployed = [r for r in hold if num(r.get("champion_prediction")) is not None]
    old_live_error = mae([r["actual"] for r in deployed],
                         [r["champion_prediction"] for r in deployed]) if len(deployed) >= len(hold)*.8 else None
    # When a previous champion is active, compare on exactly the same player-games.
    same_rows_challenger = mae([r["actual"] for r in deployed],
                               predictions(selected, deployed, keys)) if old_live_error is not None else hold_error
    reference = old_live_error if old_live_error is not None else best_base
    valid = bool(same_rows_challenger <= reference * .97 and
                 (reference - same_rows_challenger) >= .08 and
                 hold_error <= best_base * 1.01)
    report.update({"selected": f"{kind}/{family}", "tuning_mae": round(tune_err, 3),
                   "holdout_mae": round(hold_error, 3), "reference_mae": round(reference, 3),
                   "promotion_passed": valid})
    if not valid:
        report["status"] = "existing model retained" if current_meta else "baseline retained"
        return report, None
    # Only after a successful, out-of-time test can all known finished games train the model.
    try:
        champion = _fit(rows, keys, kind)
        report["feature_drivers"] = feature_impact(selected, hold, keys)
        report["status"] = "promoted"
        return report, {"model": champion, "features": keys, "group": group,
                        "kind": kind, "family": family, "trained_through": rows[-1]["date"],
                        "validation_mae": round(hold_error, 3), "validation_baseline_mae": best_base,
                        "feature_drivers": report["feature_drivers"]}
    except Exception as exc:
        print(f"(learning) {group} full fit failed: {exc}")
        report["status"] = "training error; old model retained"
        return report, None


def learn_start(rows, model_dir, current_meta):
    """Separate calibrated P(start) model; never multiply player performance twice."""
    import numpy as np
    from sklearn.pipeline import make_pipeline
    from sklearn.impute import SimpleImputer
    from sklearn.preprocessing import StandardScaler
    from sklearn.linear_model import LogisticRegression
    rows = sorted([r for r in rows if r.get("position") == "G" and r.get("started") in (0, 1)
                   and num(r.get("features", {}).get("start_base")) is not None], key=lambda r: r["date"])
    report = {"examples": len(rows), "status": "collecting"}
    if len(rows) < 180:
        return report, None
    split = _dates_split(rows)
    if not split:
        return report, None
    tr, tune, hold = split
    if len(set(r["started"] for r in tr)) < 2 or len(set(r["started"] for r in hold)) < 2:
        return report, None
    clf = make_pipeline(SimpleImputer(strategy="median", keep_empty_features=True),
                        StandardScaler(), LogisticRegression(C=.1, max_iter=1000, random_state=19))
    clf.fit(matrix(tr + tune, START_FEATURES), [r["started"] for r in tr + tune])
    def brier(y, p):
        return float(np.mean((np.asarray(y) - np.asarray(p)) ** 2))
    y = [r["started"] for r in hold]
    estimated = clf.predict_proba(matrix(hold, START_FEATURES))[:, 1]
    baseline = [r["features"]["start_base"] for r in hold]
    b0, b1 = brier(y, baseline), brier(y, estimated)
    frozen = [r for r in hold if num(r.get("start_probability_snapshot")) is not None]
    old_live = brier([r["started"] for r in frozen],
                     [r["start_probability_snapshot"] for r in frozen]) if len(frozen) >= .8*len(hold) else None
    reference = old_live if old_live is not None else b0
    on_same_rows = brier([r["started"] for r in frozen],
                         clf.predict_proba(matrix(frozen, START_FEATURES))[:, 1]) if old_live is not None else b1
    promoted = on_same_rows < reference * .95 and (reference - on_same_rows) >= .003 and b1 <= b0 * 1.01
    report.update({"status": "promoted" if promoted else "baseline retained",
                   "baseline_brier": round(b0, 4), "model_brier": round(b1, 4),
                   "reference_brier": round(reference, 4),
                   "promotion_passed": promoted})
    if not promoted:
        return report, None
    clf.fit(matrix(rows, START_FEATURES), [r["started"] for r in rows])
    return report, {"model": clf, "features": START_FEATURES,
                    "trained_through": rows[-1]["date"], "validation_brier": b1}
