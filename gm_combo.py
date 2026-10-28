"""
gm_combo.py - the Combined projection: one number per player per game, built from ESPN, the GM model and the AI.

Every night it re-tests every way of combining them on all graded games so far (ai/joined), using only
games from before each test day (walk-forward, no peeking), and keeps whatever has the smallest average
miss per game (the same measure the AI Lab uses), separately for forwards, defence and goalies:
  - "ai", "gm", "espn": one model alone
  - "half": AI and GM model averaged
  - "mix":  learned weights for ESPN, GM and AI (weights add up to 1, no correction, so it stays fair)
The mix has to beat the best of the others by more than 1 standard error, so it can't win by luck.
When a player has no number from the chosen model, the app falls back AI -> GM -> ESPN.
It also learns how often a goalie Daily Faceoff lists as unconfirmed (and his backup) really starts,
and re-tunes the AI's goalie start chances (they come out too low for likely starters) and only
switches that on when the walk-forward test shows it clearly helps.
Writes ai/combo.json, which the app and ai_engine.py read.

Run: python gm_combo.py          (needs numpy)
     python gm_combo.py --selftest
"""
import glob
import json
import math
import os
import sys
from datetime import datetime, timezone

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "ai", "combo.json")
VERSION = "combo-v1"
GROUPS = ("F", "D", "G")
MIN_TRAIN_DAYS = 6
MIN_ROWS = 300
DEFAULT_W = {"espn": 0.0, "gm": 0.5, "ai": 0.5}
STEP = 0.05


def group_of(r):
    if r.get("pos") == "G":
        return "G" if (r.get("gs") or 0) >= 1 and r.get("played") else None
    if r.get("pos") in ("F", "D"):
        return r["pos"] if r.get("played") else None
    return None


def three(r):
    """espn, gm, ai with the same fallbacks the app uses when one is missing"""
    e, g, a = r.get("espn"), r.get("gm"), r.get("ai")
    if a is None:
        a = g if g is not None else e
    if g is None:
        g = a
    if e is None:
        e = g
    if a is None or g is None or e is None:
        return None
    return float(e), float(g), float(a)


def fit_mix(B, y):
    """best weights on a 5% grid (ESPN, GM, AI add up to 1), by the smallest average miss"""
    best = None
    grid = np.round(np.arange(0, 1 + 1e-9, STEP), 2)
    for wa in grid:
        for wg in grid:
            if wa + wg > 1 + 1e-9:
                continue
            w = np.array([1 - wa - wg, wg, wa])
            m = float(np.mean(np.abs(B @ w - y)))
            if best is None or m < best[0]:
                best = (m, w)
    return best[1], 0.0


def family_preds(B, w_mix, bias):
    return {"half": (B[:, 1] + B[:, 2]) / 2, "ai": B[:, 2], "gm": B[:, 1], "espn": B[:, 0], "mix": B @ w_mix + bias}


def weights_of(fam, w_mix=None, bias=0.0):
    if fam == "half":
        return dict(DEFAULT_W), 0.0
    if fam in ("ai", "gm", "espn"):
        return {k: 1.0 if k == fam else 0.0 for k in ("espn", "gm", "ai")}, 0.0
    return {"espn": round(float(w_mix[0]), 2), "gm": round(float(w_mix[1]), 2), "ai": round(float(w_mix[2]), 2)}, round(float(bias), 3)


def learn(recs):
    rows = [r for r in recs if group_of(r) and r.get("fp") is not None and three(r)]
    days = sorted({r["date"] for r in rows})
    out = {}
    for G in GROUPS:
        gr = [r for r in rows if group_of(r) == G]
        by_day = {}
        for r in gr:
            by_day.setdefault(r["date"], []).append(r)
        err = {f: [] for f in ("half", "ai", "gm", "espn", "mix")}
        ys, preds = [], {f: [] for f in err}
        for i, d in enumerate(days):
            te = by_day.get(d) or []
            tr = [r for dd in days[:i] for r in by_day.get(dd, [])]
            if i < MIN_TRAIN_DAYS or not te or len(tr) < 100:
                continue
            Btr = np.array([three(r) for r in tr]); ytr = np.array([r["fp"] for r in tr], float)
            w, b = fit_mix(Btr, ytr)
            Bte = np.array([three(r) for r in te]); yte = np.array([r["fp"] for r in te], float)
            P = family_preds(Bte, w, b)
            for f in err:
                err[f].extend(list(np.abs(P[f] - yte)))
                preds[f].extend(list(P[f]))
            ys.extend(list(yte))
        n = len(ys)
        tests = {}
        y = np.array(ys, float)
        for f in err:
            if n:
                p = np.array(preds[f], float)
                tests[f] = {"n": n, "mae": round(float(np.mean(np.abs(p - y))), 3), "rmse": round(float(np.sqrt(np.mean((p - y) ** 2))), 3),
                            "bias": round(float(np.mean(p - y)), 3)}
        pick, why = "half", "starting choice"
        if n >= MIN_ROWS:
            single = {f: float(np.mean(err[f])) for f in ("ai", "gm", "espn", "half")}
            pick = min(single, key=single.get)
            why = f"smallest average miss per game ({single[pick]:.3f} pts)"
            dlt = np.array(err["mix"]) - np.array(err[pick])
            se = float(np.std(dlt, ddof=1) / math.sqrt(len(dlt))) if len(dlt) > 1 else 1e9
            if float(np.mean(dlt)) < -se:
                pick, why = "mix", f"learned mix beats {pick} by {-np.mean(dlt):.3f} pts per game (SE {se:.3f})"
        else:
            why = f"only {n} test games so far - using the AI+GM average"
        w_all, b_all = (fit_mix(np.array([three(r) for r in gr]), np.array([r["fp"] for r in gr], float)) if len(gr) >= 50 else (np.array([0, .5, .5]), 0.0))
        wts, bias = weights_of(pick, w_all, b_all)
        out[G] = {"pick": pick, "why": why, "w": wts, "bias": bias, "games": len(gr), "tests": tests}
    return out, (days[0] if days else None), (days[-1] if days else None)


def learn_gstart(recs):
    """re-tune the AI's goalie start chances (they come out too low for likely starters); test walk-forward"""
    G = [r for r in recs if r.get("pos") == "G" and r.get("ai_start_p") is not None]
    for r in G:
        r["_y"] = 1.0 if (r.get("gs") or 0) >= 1 else 0.0
    days = sorted({r["date"] for r in G})
    lg = lambda p: math.log(min(1 - 1e-4, max(1e-4, p)) / (1 - min(1 - 1e-4, max(1e-4, p))))

    def fit(rows):
        x = np.array([lg(r["ai_start_p"]) for r in rows]); y = np.array([r["_y"] for r in rows]); a, b = 1.0, 0.0
        for _ in range(300):
            p = 1 / (1 + np.exp(-(a * x + b)))
            a -= 0.5 * float(np.mean((p - y) * x)); b -= 0.5 * float(np.mean(p - y))
        return a, b

    def apply(rows, a, b):
        out, grp = {}, {}
        for r in rows:
            grp.setdefault((r.get("gid"), r.get("team")), []).append(r)
        for g in grp.values():
            q = [1 / (1 + math.exp(-(a * lg(r["ai_start_p"]) + b))) for r in g]
            s = sum(q)
            for r, v in zip(g, q):
                out[id(r)] = v / s if len(g) > 1 and s > 0 else v
        return out

    raw, new, ys = [], [], []
    for i, d in enumerate(days):
        if i < MIN_TRAIN_DAYS:
            continue
        tr = [r for r in G if r["date"] < d]; te = [r for r in G if r["date"] == d]
        if len(tr) < 200 or not te:
            continue
        a, b = fit(tr)
        q = apply(te, a, b)
        for r in te:
            raw.append(r["ai_start_p"]); new.append(q[id(r)]); ys.append(r["_y"])
    res = {"use": False, "a": 1.0, "b": 0.0, "n": len(ys)}
    if len(ys) >= 300:
        R, N, Y = np.array(raw), np.array(new), np.array(ys)
        d = (N - Y) ** 2 - (R - Y) ** 2
        se = float(np.std(d, ddof=1) / math.sqrt(len(d)))
        a, b = fit(G)
        res.update({"a": round(a, 4), "b": round(b, 4), "brier_ai": round(float(np.mean((R - Y) ** 2)), 4),
                    "brier_new": round(float(np.mean((N - Y) ** 2)), 4), "se": round(se, 4),
                    "use": bool(float(np.mean(d)) < -2 * se)})
    return res


def learn_gs_df(root, recs):
    """goalie start chance when Daily Faceoff has a goalie listed but not confirmed:
    learned from every saved pre-game snapshot (ai/predictions) and who actually started"""
    Y = {}
    for r in recs:
        if r.get("pos") == "G":
            Y[(r.get("gid"), r.get("pid"))] = 1.0 if (r.get("gs") or 0) >= 1 else 0.0
    lg = lambda p: math.log(min(1 - 1e-4, max(1e-4, p)) / (1 - min(1 - 1e-4, max(1e-4, p))))
    rows = []
    for f in sorted(glob.glob(os.path.join(root, "ai", "predictions", "*.jsonl"))):
        try:
            with open(f, encoding="utf-8") as fh:
                for ln in fh:
                    if '"pos":"G"' not in ln and '"pos": "G"' not in ln:
                        continue
                    x = json.loads(ln)
                    g, k = x.get("goalie") or {}, (x.get("gid"), x.get("pid"))
                    s = str(g.get("source") or "").lower()
                    c = "unc" if "unconfirmed" in s else "other" if "other goalie" in s else "likely" if "likely" in s else "conf" if "confirmed" in s else None
                    if k in Y and g.get("ai_start_p") is not None and c:
                        rows.append((c, lg(g["ai_start_p"]), 1.0 if (x.get("lead_min") or 0) < 720 else 0.0, Y[k], x.get("date")))
        except Exception as ex:
            print(f"(combo) could not read {f}: {ex}")
    days = sorted({r[4] for r in rows})

    def X(rs):
        return np.array([[1.0, r[1], r[2], r[1] * r[2]] for r in rs])

    def fit(rs):
        A, y, w = X(rs), np.array([r[3] for r in rs]), np.zeros(4)
        for _ in range(400):
            p = 1 / (1 + np.exp(-A @ w))
            w -= 0.3 * (A.T @ (p - y)) / len(y)
        return w

    old = {"conf": 1.0, "likely": 0.85, "unc": 0.5, "other": 0.5}
    e_new, e_old = [], []
    for i, d in enumerate(days):
        if i < MIN_TRAIN_DAYS:
            continue
        tr = [r for r in rows if r[4] < d]
        te = [r for r in rows if r[4] == d]
        W = {c: fit([r for r in tr if r[0] == c]) for c in ("unc", "other") if sum(1 for r in tr if r[0] == c) > 100}
        for r in te:
            if r[0] in ("conf", "likely"):
                p = 0.99
            elif r[0] in W:
                p = float(1 / (1 + math.exp(-X([r])[0] @ W[r[0]])))
            else:
                p = old[r[0]]
            e_new.append((p - r[3]) ** 2)
            e_old.append((old[r[0]] - r[3]) ** 2)
    res = {"use": False, "rows": len(rows), "n": len(e_new)}
    if len(e_new) >= 1000:
        d = np.array(e_new) - np.array(e_old)
        se = float(np.std(d, ddof=1) / math.sqrt(len(d)))
        res.update({"brier_old": round(float(np.mean(e_old)), 4), "brier_new": round(float(np.mean(e_new)), 4), "se": round(se, 4),
                    "use": bool(float(np.mean(d)) < -2 * se), "likely": 0.99,
                    "unc": [round(float(v), 4) for v in fit([r for r in rows if r[0] == "unc"])],
                    "other": [round(float(v), 4) for v in fit([r for r in rows if r[0] == "other"])]})
    return res


def load(root):
    recs = []
    for f in sorted(glob.glob(os.path.join(root, "ai", "joined", "*.json"))):
        try:
            with open(f, encoding="utf-8") as fh:
                recs += (json.load(fh) or {}).get("recs") or []
        except Exception as ex:
            print(f"(combo) could not read {f}: {ex}")
    return recs


def main(root=HERE):
    recs = load(root)
    groups, d0, d1 = learn(recs)
    js = {"version": VERSION, "asof": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
          "data": {"from": d0, "to": d1, "records": len(recs)}, "groups": groups, "gstart": learn_gstart(recs), "gs_df": learn_gs_df(root, recs)}
    with open(os.path.join(root, "ai", "combo.json"), "w", encoding="utf-8") as fh:
        json.dump(js, fh, indent=1)
    for G, x in groups.items():
        t = x["tests"]
        line = ", ".join(f"{k} {v['mae']}" for k, v in t.items())
        print(f"(combo) {G}: using {x['pick']} {x['w']} bias {x['bias']} - {x['why']} | test MAE: {line}")
    print(f"(combo) goalie start chances: {js['gstart']}")
    print(f"(combo) Daily Faceoff listed goalies: {js['gs_df']}")


def selftest():
    import random
    random.seed(1)
    recs = []
    for d in range(20):
        day = f"2026-10-{d + 1:02d}"
        for i in range(120):
            mu = random.uniform(2, 10)
            fp = max(0.0, random.gauss(mu, 3))
            recs.append({"date": day, "pos": "F", "played": True, "fp": fp,
                         "espn": mu + random.gauss(0, 3), "gm": mu + random.gauss(0, 1.0), "ai": mu + random.gauss(0, 1.0)})
    g, _, _ = learn(recs)
    ok1 = g["F"]["pick"] in ("half", "mix")
    print(("PASS" if ok1 else "FAIL") + "  two equally good models with separate errors get combined: " + g["F"]["pick"] + " " + str(g["F"]["w"]))
    for r in recs:
        r["gm"] = r["fp"] + random.gauss(0, 0.3)
    g2, _, _ = learn(recs)
    ok2 = g2["F"]["pick"] in ("gm", "mix") and g2["F"]["w"]["gm"] >= 0.8
    print(("PASS" if ok2 else "FAIL") + "  a clearly better model takes over: " + g2["F"]["pick"] + " " + str(g2["F"]["w"]))
    ok3 = g["D"]["pick"] == "half"
    print(("PASS" if ok3 else "FAIL") + "  no data for a group keeps the AI+GM average")
    return ok1 and ok2 and ok3


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(0 if selftest() else 1)
    main()
