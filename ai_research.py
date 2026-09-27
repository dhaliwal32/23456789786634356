"""
ai_research.py  -  Fantasy Islands GM automated research loop (STAGE 5)

On retraining days (Mondays, or when you force a retrain) this runs BEFORE ai_learn.py:

  1. REVIEW    measures the live skater model's errors on past months it never saw and
               ranks candidate ideas by how strongly they line up with those errors.
  2. SCREEN    tests the most promising ideas on "research" months (walk-forward).
  3. CONFIRM   ideas that clearly help are re-tested on the two most recent months,
               which the screening step never used. Only ideas that hold up there too
               are adopted.
  4. COMPETE   adopted ideas become a challenger model ("...+research"). It only goes
               live if it wins ai_learn.py's normal weekly competition.
  5. LOG       every experiment, adopted or rejected, is written in plain English to
               ai/research/log.json (shown in the AI Lab's Research section).

It never edits code. Ideas are combinations of inputs the system already collects.

Commands:
  python ai_research.py --daily [--train]   what GitHub Actions runs (research if due, then ai_learn)
  python ai_research.py --selftest          offline tests on synthetic data
"""
import json
import math
import os
import pickle
import shutil
import sys
import tempfile
import time
import traceback
from datetime import date, datetime, timedelta

import numpy as np

import ai_engine as E
import ai_learn as L

VERSION = "ai-research-v1"
I = L.IDX
MIN_REL = 0.003          # an idea must improve accuracy by at least 0.3% on held-out months
RETEST_DAYS = 28         # rejected ideas wait this long before being tested again...
RETEST_GROWTH = 1.25     # ...unless the data has grown by 25%
MAX_PER_GROUP = 4        # ideas tested per group per week (keeps the run short)
GROUPS = {"F": "forwards", "D": "defensemen"}


def _fp_rate(X, d):
    return sum(E.SK[k] * X[:, I[f"{k}_{d}"]] for k in L.SK_STATS)


# name: (plain-English description, function of the existing inputs or None for training ideas)
CANDIDATES = {
    "toi_trend": ("Ice time rising or falling (last few games vs long run)",
                  lambda X: X[:, I["toi_s"]] - X[:, I["toi_l"]]),
    "pp_trend": ("Power-play time rising or falling",
                 lambda X: X[:, I["pptoi_s"]] - X[:, I["pptoi_l"]]),
    "pp_share": ("Share of his ice time spent on the power play",
                 lambda X: X[:, I["pptoi_m"]] / np.maximum(X[:, I["toi_m"]], 1.0)),
    "shot_luck": ("Goals above what his shots normally produce (luck that should even out)",
                  lambda X: X[:, I["G_l"]] - X[:, I["sh_pct"]] * X[:, I["SOG_l"]]),
    "form_gap": ("Hot or cold streak: recent fantasy rate minus long-run rate",
                 lambda X: _fp_rate(X, "s") - _fp_rate(X, "l")),
    "matchup_off": ("His team's scoring combined with the opponent's goals allowed",
                    lambda X: X[:, I["own_gf"]] * X[:, I["opp_ga"]]),
    "shot_env": ("His team's shot volume combined with the opponent's shots allowed",
                 lambda X: X[:, I["own_sf"]] * X[:, I["opp_sa"]]),
    "fatigue": ("Back-to-back games combined with heavy minutes (tired legs)",
                lambda X: X[:, I["b2b"]] * X[:, I["toi_m"]]),
    "small_sample": ("Very few NHL games so far (unproven player)",
                     lambda X: (X[:, I["n_l"]] < 10).astype(float)),
    "recent_training": ("Train only on the most recent ~60% of games (newer seasons matter more)", None),
}

BASE = {g: dict(f) for g, f in L.FAMILIES.items()}   # original model families, before any research


class Augmented:
    """A model family plus extra inputs (appended after the originals, so nothing else shifts)."""

    def __init__(self, grp, base, extras=()):
        self.grp, self.base, self.extras = grp, base, list(extras)
        self.keep_frac = 0.6 if "recent_training" in self.extras else 1.0

    def _x(self, X):
        cols = [CANDIDATES[e][1](X) for e in self.extras if e in CANDIDATES and CANDIDATES[e][1] is not None]
        return np.column_stack([X] + cols) if cols else X

    def fit(self, X, Y):
        k = int(len(X) * (1 - self.keep_frac))
        self.m = BASE[self.grp][self.base]().fit(self._x(X[k:]), Y[k:])
        return self

    def predict(self, X):
        return self.m.predict(self._x(X))


def register(adopted):
    """Make adopted ideas available to ai_learn's weekly competition as '<base>+research'."""
    for g, info in (adopted or {}).items():
        base, extras = (info or {}).get("base"), (info or {}).get("extras") or []
        if extras and base in BASE.get(g, {}):
            L.FAMILIES[g][f"{base}+research"] = (lambda g=g, b=base, ex=tuple(extras): Augmented(g, b, ex))


def wf(X, Y, dates, folds, maker):
    preds, acts = [], []
    for a, b in folds:
        tr = dates < a
        te = (dates >= a) & (dates < b)
        m = maker().fit(X[tr], Y[tr])
        preds.append(np.asarray(m.predict(X[te])["fp"], dtype=float))
        acts.append(Y[te, -1])
    if not preds:
        return np.zeros(0), np.zeros(0)
    return np.concatenate(preds), np.concatenate(acts)


def test_mask(dates, folds):
    k = np.zeros(len(dates), dtype=bool)
    for a, b in folds:
        k |= (dates >= a) & (dates < b)
    return k


def corr(a, b):
    a, b = np.asarray(a, dtype=float), np.asarray(b, dtype=float)
    if len(a) < 3 or a.std() == 0 or b.std() == 0 or not np.isfinite(a).all():
        return 0.0
    return float(np.corrcoef(a, b)[0, 1])


def judge(lb, lc):
    """Paired comparison on the same games. Returns (mean change in miss, its SE, relative gain)."""
    m, se = L.mean_se(lc - lb)
    base = float(lb.mean()) if len(lb) else float("nan")
    rel = -m / base if base else 0.0
    return m, se, rel


def screen_ok(m, se):
    return se == se and m < 0 and m < -se


def confirm_ok(m, se, rel, min_rel=MIN_REL):
    return se == se and m < -2 * se and rel >= min_rel


def research(root, data, now, cfg, log=print, max_per_group=MAX_PER_GROUP):
    import warnings
    warnings.filterwarnings("ignore")
    path = L.H(root, "research", "log.json")
    rlog = E.read_json(path, {})
    rlog.setdefault("experiments", [])
    rlog.setdefault("tested", {})
    rlog.setdefault("adopted", {})
    reg = E.read_json(L.H(root, "models", "registry.json"), {})
    n_new = 0
    for grp, gname in GROUPS.items():
        X, Y, dates, _ = data[grp]
        folds = L.folds_for(dates, cfg)
        if len(folds) < 3:
            log(f"(research) {gname}: not enough months of data yet")
            continue
        rf, cf = folds[:-2], folds[-2:]
        prod = ((reg.get("production") or {}).get(grp) or {}).get("family") or "gbm_stats"
        base = prod.split("+")[0]
        if base == "baseline" or base not in BASE[grp]:
            base = "gbm_stats"
        ad = rlog["adopted"].get(grp) or {}
        cur = list(ad.get("extras") or []) if ad.get("base") == base else []

        def mk(ex):
            return lambda: Augmented(grp, base, tuple(ex))

        tested = rlog["tested"].setdefault(grp, {})
        todo = []
        for c in CANDIDATES:
            if c in cur:
                continue
            t = tested.get(c)
            if t and now - E.parse_utc(t["at"]) < timedelta(days=RETEST_DAYS) and len(dates) < t.get("n", 0) * RETEST_GROWTH:
                continue
            todo.append(c)
        if not todo:
            log(f"(research) {gname}: every idea was tested recently - nothing new to test")
            continue
        t0 = time.time()
        bp, act = wf(X, Y, dates, rf, mk(cur))
        resid = bp - act
        lb = np.abs(resid)
        Xt = X[test_mask(dates, rf)]
        ranked = sorted(((abs(corr(CANDIDATES[c][1](Xt), resid)) if CANDIDATES[c][1] else 0.02, c) for c in todo),
                        reverse=True)[:max_per_group]
        lb2 = None
        for score, c in ranked:
            desc = CANDIDATES[c][0]
            cp, _ = wf(X, Y, dates, rf, mk(cur + [c]))
            m, se, rel = judge(lb, np.abs(cp - act))
            hold = None
            if not screen_ok(m, se):
                status = "rejected"
                summary = (f"{desc}: {gname} projections changed by {rel:+.1%} on research months "
                           f"(±{2 * se / max(lb.mean(), 1e-9):.1%}) - not a clear improvement, so it was rejected.")
            else:
                if lb2 is None:
                    bp2, act2 = wf(X, Y, dates, cf, mk(cur))
                    lb2 = np.abs(bp2 - act2)
                cp2, act2 = wf(X, Y, dates, cf, mk(cur + [c]))
                m2, se2, rel2 = judge(lb2, np.abs(cp2 - act2))
                hold = {"n": int(len(lb2)), "gain": round(rel2, 4), "pm": round(2 * se2 / max(lb2.mean(), 1e-9), 4)}
                if confirm_ok(m2, se2, rel2):
                    status = "adopted"
                    cur.append(c)
                    rlog["adopted"][grp] = {"base": base, "extras": list(cur), "at": E.iso(now)}
                    summary = (f"{desc}: improved {gname} accuracy by {rel:.1%} on research months and {rel2:.1%} "
                               f"on the two held-out months - added to a challenger model, which goes live only if "
                               f"it wins the weekly competition.")
                else:
                    status = "not confirmed"
                    summary = (f"{desc}: looked {rel:.1%} better on research months but changed by {rel2:+.1%} on the "
                               f"held-out months - it did not hold up, so it was not adopted.")
            tested[c] = {"at": E.iso(now), "n": int(len(dates)), "status": status}
            rlog["experiments"].append({"at": E.iso(now), "group": gname, "key": c, "name": desc, "status": status,
                                        "base": base, "priority": round(score, 4),
                                        "research": {"n": int(len(lb)), "gain": round(rel, 4),
                                                     "pm": round(2 * se / max(lb.mean(), 1e-9), 4)},
                                        "holdout": hold, "summary": summary})
            n_new += 1
            log(f"(research) {gname}: {status.upper():13s} {c} | {summary}")
            if status == "adopted":
                break   # one adoption per group per week, so every test compares against the current model
        log(f"(research) {gname}: {len(ranked)} idea(s) tested in {time.time() - t0:.0f}s")
    rep = E.read_json(os.path.join(root, "ai", "report.json"), {})
    rlog["clues"] = (rep.get("flags") or [])[:10]
    rlog["experiments"] = rlog["experiments"][-300:]
    rlog["version"] = VERSION
    rlog["last_run"] = E.iso(now)
    E.write_json(path, rlog)
    register(rlog["adopted"])
    return n_new


def daily_main(force=False, root=None, now=None):
    root = root or L.HERE
    now = now or datetime.now(E.UTC)
    rlog = E.read_json(L.H(root, "research", "log.json"), {})
    register(rlog.get("adopted"))
    reg = E.read_json(L.H(root, "models", "registry.json"), {})
    due = (force or reg.get("feature_hash") != L.FEATURE_HASH or not reg.get("production")
           or (now.weekday() == 0 and not str(reg.get("last_train", "")).startswith(E.iso(now)[:10])))
    if due:
        try:
            rows = L.load_history(root)
            if rows:
                _, SX, GS, GC = L.build_dataset(rows)
                research(root, L.datasets(SX, GS, GC), now, L.CFG)
            else:
                print("(research) no history yet - research starts after the first training run")
        except Exception:
            print("(research) WARNING research step failed - training continues without it")
            print(traceback.format_exc())
    else:
        print("(research) not a research day (Mondays) - skipping")
    return L.daily(root, now, force)


# ----------------------------------------------------------------- tests
def selftest():
    import warnings
    warnings.filterwarnings("ignore")
    results = []

    def check(name, cond):
        results.append(bool(cond))
        print(("PASS  " if cond else "FAIL  ") + name)

    tmp = tempfile.mkdtemp()
    try:
        rows = L.synth()
        for r in rows:
            r["season"] = L.season_for(date.fromisoformat(r["d"]))
        _, SX, GS, GC = L.build_dataset(rows)
        data = L.datasets(SX, GS, GC)
        X, Y, d, _ = data["F"]
        ok = all(fn is None or (len(fn(X)) == len(X) and np.isfinite(fn(X)).all()) for _, fn in CANDIDATES.values())
        check("every idea produces one valid number per game", ok)
        a = Augmented("F", "baseline", ["toi_trend", "pp_share"]).fit(X[:500], Y[:500]).predict(X[:20])["fp"]
        b = L.SkBaseline().predict(X[:20])["fp"]
        check("added inputs never disturb the original ones", np.allclose(a, b))
        check("'recent training' idea trains on the newest 60% only",
              Augmented("F", "gbm_fp", ["recent_training"]).keep_frac == 0.6)
        m = Augmented("F", "gbm_fp", ["form_gap"]).fit(X[:1500], Y[:1500])
        m2 = pickle.loads(pickle.dumps(m))
        check("research models save and reload correctly",
              np.allclose(m.predict(X[:30])["fp"], m2.predict(X[:30])["fp"]) and type(m2).__module__ == "ai_research")

        rng = np.random.default_rng(1)
        lb = np.abs(rng.normal(0, 5, 4000))
        mm, se, rel = judge(lb, lb - 0.3)
        check("a clearly better idea passes screening and confirmation", screen_ok(mm, se) and confirm_ok(mm, se, rel))
        mm, se, rel = judge(lb, lb + rng.normal(0, 0.05, 4000))
        check("a pure-noise idea is not confirmed", not confirm_ok(mm, se, rel))
        mm, se, rel = judge(lb, lb - 0.004)
        check("a real but tiny (<0.3%) gain is not adopted", not confirm_ok(mm, se, rel))

        register({"F": {"base": "gbm_fp", "extras": ["toi_trend"]}})
        fam = L.FAMILIES["F"].get("gbm_fp+research")
        check("adopted ideas enter the weekly competition as a challenger",
              fam is not None and isinstance(fam(), Augmented) and fam().extras == ["toi_trend"])
        L.FAMILIES["F"].pop("gbm_fp+research", None)

        tcfg = dict(L.CFG, folds=5, min_test=50, min_train=300)
        now = datetime(2027, 1, 4, 12, 0, tzinfo=E.UTC)
        n = research(tmp, data, now, tcfg, max_per_group=3)
        rl = E.read_json(L.H(tmp, "research", "log.json"), {})
        exps = rl.get("experiments", [])
        check("experiments run and are logged", n > 0 and len(exps) == n)
        check("every experiment has a result and a plain-English explanation",
              all(e["status"] in ("adopted", "rejected", "not confirmed") and len(e["summary"]) > 40 for e in exps))
        check("confirmation only uses held-out months when screening passed",
              all((e["holdout"] is None) == (e["status"] == "rejected") for e in exps))
        n2 = research(tmp, data, now + timedelta(days=1), tcfg, max_per_group=3)
        again = {e["key"] for e in E.read_json(L.H(tmp, "research", "log.json"), {})["experiments"][n:]}
        check("ideas are not re-tested within 4 weeks on the same data", not again & {e["key"] for e in exps})
        for g in L.FAMILIES:
            for k in [k for k in L.FAMILIES[g] if k.endswith("+research")]:
                L.FAMILIES[g].pop(k)
    except Exception:
        traceback.print_exc()
        results.append(False)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    ok = all(results)
    print(f"\n{sum(results)}/{len(results)} checks passed" + ("" if ok else "  <-- SOMETHING FAILED"))
    return 0 if ok else 1


def main(argv):
    if "--selftest" in argv:
        return selftest()
    if "--daily" in argv:
        return 1 if daily_main(force="--train" in argv) else 0
    print(__doc__)
    return 0


if __name__ == "__main__":
    import ai_research  # run from the module so saved research models reload as ai_research.* classes
    sys.exit(ai_research.main(sys.argv[1:]))
