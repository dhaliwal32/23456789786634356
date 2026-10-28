"""
ai_history_exp.py - research: does the AI get more accurate with older seasons of NHL history?

Downloads older regular seasons into ai/history (same format as ai_learn.py), then re-runs the AI's
own walk-forward test with the live model types, each time starting the history one season earlier.
The test months are the same for every option, so the numbers compare fairly.
Writes ai/research/history_exp.json. It does not change the live AI.

Run: python ai_history_exp.py            (download + test)
     python ai_history_exp.py --no-download
"""
import json
import math
import os
import sys
import time
import warnings
from datetime import datetime, timezone

import numpy as np

import ai_engine as E
import ai_learn as L

warnings.filterwarnings("ignore")
ORIG_FOLDS = L.folds_for
HERE = os.path.dirname(os.path.abspath(__file__))
OLDER = [("20232024", "2023-10-01", "2024-04-25"), ("20222023", "2022-10-01", "2023-04-20"),
         ("20212022", "2021-10-01", "2022-05-05"), ("20202021", "2021-01-10", "2021-05-25"),
         ("20192020", "2019-09-28", "2020-03-15"), ("20182019", "2018-09-28", "2019-04-10"),
         ("20172018", "2017-09-28", "2018-04-10")]
OUT = os.path.join(HERE, "ai", "research", "history_exp.json")


def log(*a):
    print(datetime.now(timezone.utc).strftime("%H:%M:%S"), *a, flush=True)


def main():
    # older seasons are kept apart (ai/older/...) so the live AI does not start using them by itself
    XROOT = os.path.join(HERE, "ai", "older")
    if "--no-download" not in sys.argv:
        live = L.SEASONS
        L.SEASONS = sorted(OLDER, key=lambda s: s[1])
        try:
            n = L.update_history(XROOT, datetime.now(E.ET).date(), L.fetch_range, log, 0.3)
        finally:
            L.SEASONS = live
        log(f"downloaded {n} weekly files")
    seen = {}
    for r in L.load_history(XROOT) + L.load_history(HERE):
        seen[(r.get("g"), r.get("p"))] = r
    rows_all = sorted(seen.values(), key=lambda r: (r["d"], r["g"] or 0))
    seasons = sorted({r["season"] for r in rows_all})
    log("seasons on hand:", seasons, "rows:", len(rows_all))
    current_start = "20242025"
    starts = [s for s in sorted(seasons, reverse=True) if s <= current_start]
    prod = (E.read_json(os.path.join(HERE, "ai", "models", "registry.json"), {}).get("production") or {})
    fam = {g: (prod.get(g) or {}).get("family") or ("gbm_stats" if g == "F" else "poisson_stats" if g == "D" else "gbm" if g == "G_start" else "baseline") for g in L.FAMILIES}
    log("live model types:", fam)
    fixed = {}
    res = {"asof": E.iso(datetime.now(timezone.utc)), "families": fam, "options": {}, "rows": {}}
    base_loss = {}
    for s0 in starts:
        rows = [r for r in rows_all if r["season"] >= s0]
        t0 = time.time()
        st, SX, GS, GC = L.build_dataset(rows)
        data = L.datasets(SX, GS, GC)
        res["rows"][s0] = len(rows)
        out = {}
        for grp in L.FAMILIES:
            X, Y, dates, keys = data[grp]
            gcfg = dict(L.CFG, **{k: min(L.CFG[k], v) for k, v in L.GROUP_CFG.get(grp, {}).items()})
            if grp not in fixed:
                fixed[grp] = ORIG_FOLDS(dates, gcfg)
            L.folds_for = (lambda f: (lambda d, c: f))(fixed[grp])
            keep = L.FAMILIES[grp]
            L.FAMILIES[grp] = {fam[grp]: keep[fam[grp]]}
            try:
                wf = L.walk_forward(grp, X, Y, dates, keys, gcfg)
            finally:
                L.FAMILIES[grp] = keep
            loss = wf["losses"][fam[grp]]
            o = {"n": int(len(loss)), "loss": round(float(loss.mean()), 4)}
            if s0 == current_start:
                base_loss[grp] = loss
            elif grp in base_loss and len(base_loss[grp]) == len(loss):
                d = loss - base_loss[grp]
                o["vs_current"] = round(float(d.mean()), 4)
                o["se"] = round(float(d.std(ddof=1) / math.sqrt(len(d))), 4)
                o["pct"] = round(float(-d.mean() / base_loss[grp].mean() * 100), 2)
            out[grp] = o
            log(s0, grp, o)
        res["options"][s0] = out
        log(f"history from {s0}: {len(rows)} rows, {time.time() - t0:.0f}s")
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        with open(OUT, "w", encoding="utf-8") as f:
            json.dump(res, f, indent=1)


if __name__ == "__main__":
    main()
