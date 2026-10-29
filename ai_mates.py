"""
ai_mates.py - research: linemates for the AI.

  --download   reads the NHL's shift charts for every game in the saved history (2010-11 on) and keeps,
               for each player, the teammates he shared the most ice time with: ai/mates/<season>.json.gz
  --test       re-runs the AI's walk-forward test with and without linemate inputs:
                 mate_now  - how good the 2 teammates he played the most with in this game are
                             (in the app this would come from Daily Faceoff's lines before the game)
                 mate_prev - the same, averaged over his recent games (no peeking at all)
               writes ai/research/mates_exp.json
Nothing here changes the live AI.
"""
import copy
import gzip
import json
import math
import os
import sys
import time
import warnings
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone

import numpy as np

import ai_engine as E
import ai_learn as L

warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
MDIR = os.path.join(HERE, "ai", "mates")
FIRST_SEASON = os.environ.get("MATES_FROM", "20102011")
TOP = 6


def log(*a):
    print(datetime.now(timezone.utc).strftime("%H:%M:%S"), *a, flush=True)


def rd(p):
    try:
        with gzip.open(p, "rt", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError, EOFError):
        return None


def wr(p, obj):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    tmp = p + ".tmp"
    with gzip.open(tmp, "wt", encoding="utf-8") as f:
        json.dump(obj, f, separators=(",", ":"))
    os.replace(tmp, p)


def history_rows():
    return L.load_history(HERE)


def secs(t):
    try:
        m, s = str(t).split(":")
        return int(m) * 60 + int(s)
    except Exception:
        return None


def mates_of(data, skaters):
    """{pid: [[mate, shared seconds], ...]} for skaters, from one game's shift chart rows"""
    iv = {}
    for r in data:
        if r.get("typeCode") == 505 or r.get("detailCode") not in (0, None):
            continue
        pid, per = r.get("playerId"), r.get("period") or 0
        a, b = secs(r.get("startTime")), secs(r.get("endTime"))
        if pid is None or a is None or b is None or b <= a or pid not in skaters:
            continue
        iv.setdefault(pid, []).append((per * 10000 + a, per * 10000 + b, r.get("teamAbbrev") or r.get("teamId")))
    for v in iv.values():
        v.sort()
    team = {p: v[0][2] for p, v in iv.items()}
    out = {}
    pids = list(iv)
    for i, p in enumerate(pids):
        for q in pids[i + 1:]:
            if team[p] != team[q]:
                continue
            s, A, B, i2, j2 = 0, iv[p], iv[q], 0, 0
            while i2 < len(A) and j2 < len(B):
                o = min(A[i2][1], B[j2][1]) - max(A[i2][0], B[j2][0])
                if o > 0:
                    s += o
                if A[i2][1] < B[j2][1]:
                    i2 += 1
                else:
                    j2 += 1
            if s >= 30:
                out.setdefault(p, []).append([q, s])
                out.setdefault(q, []).append([p, s])
    return {str(p): sorted(v, key=lambda x: -x[1])[:TOP] for p, v in out.items()}


def download():
    rows = history_rows()
    games, sk = {}, {}
    for r in rows:
        if r.get("season", "") >= FIRST_SEASON and r.get("g"):
            games.setdefault(r["season"], {})[r["g"]] = r["d"]
            if r["pos"] != "G":
                sk.setdefault(r["g"], set()).add(r["p"])
    s = __import__("requests").Session()
    s.headers.update(E.HDR)

    def one(gid):
        for attempt in range(3):
            try:
                r = s.get(f"{E.STATS}/shiftcharts", params={"cayenneExp": f"gameId={gid}"}, timeout=40)
                r.raise_for_status()
                return gid, mates_of(r.json().get("data") or [], sk.get(gid, set()))
            except Exception:
                time.sleep(2 + attempt * 3)
        return gid, False

    for season in sorted(games):
        path = os.path.join(MDIR, f"{season}.json.gz")
        have = rd(path) or {}
        todo = [g for g in games[season] if str(g) not in have or games[season][g] >= "2026-09-01"]
        if not todo:
            continue
        log(f"{season}: {len(todo)} games to read ({len(have)} saved)")
        t0, bad, empty = time.time(), 0, 0
        with ThreadPoolExecutor(max_workers=8) as ex:
            for gid, m in ex.map(one, todo):
                if m is False:
                    bad += 1
                    continue
                empty += 0 if m else 1
                have[str(gid)] = m
        wr(path, have)
        log(f"{season}: saved {len(have)} games ({bad} failed, {empty} without shifts) in {time.time() - t0:.0f}s")


# ---------------------------------------------------------------- test
MATES = {}


def q_of(st, pid, pos):
    """a teammate's pre-game fantasy points per game (long memory, pulled toward average)"""
    p = st.pl.get(pid)
    if not p:
        return None
    n = p["N"]["l"]
    v = {k: (p["S"]["l"][k] + L.K_PRIOR * st.lmean(pos, k)) / (n + L.K_PRIOR) for k in L.SK_STATS}
    return sum(E.SK[k] * v[k] for k in L.SK_STATS)


def patch():
    PREV = "--prev-only" in sys.argv  # fair version: only linemates from his earlier games
    L.SK_FEATS = list(L.SK_FEATS) + (["mate_prev"] if PREV else ["mate_now", "mate_n", "mate_prev"])
    L.IDX = {n: i for i, n in enumerate(L.SK_FEATS)}
    old_x, old_sk = L.State.skater_x, L.State._update_skater
    POS = {}

    def skater_x(self, pid, pos, t, o, h, day, last=None):
        x = old_x(self, pid, pos, t, o, h, day, last)
        g = self._cur_g
        ms = (MATES.get(str(g)) or {}).get(str(pid)) or []
        qs = [q_of(self, m, POS.get(m, "F")) for m, s in ms[:2]]
        qs = [q for q in qs if q is not None]
        now = sum(qs) / len(qs) if qs else 4.0
        p = self.pl.get(pid)
        prev = p.get("mq", 4.0) if p else 4.0
        return x + ([prev] if PREV else [now, float(len(qs)), prev])

    def upd_sk(self, r, day):
        POS[r["p"]] = r["pos"]
        old_sk(self, r, day)
        ms = (MATES.get(str(r.get("g"))) or {}).get(str(r["p"])) or []
        qs = [q_of(self, m, POS.get(m, "F")) for m, s in ms[:2]]
        qs = [q for q in qs if q is not None]
        if qs:
            p = self.pl[r["p"]]
            p["mq"] = 0.8 * p.get("mq", 4.0) + 0.2 * (sum(qs) / len(qs))

    L.State.skater_x, L.State._update_skater = skater_x, upd_sk
    orig_build = L.build_dataset

    def build(rows):
        st = L.State()
        st._cur_g = None
        SX, GS, GC = L.Coll(L.SK_FEATS, L.SK_T), L.Coll(L.GO_FEATS, ["start"]), L.Coll(L.GO_FEATS, L.GC_T)
        from datetime import date
        for ds, drows in sorted(L.group(rows, "d").items()):
            day = date.fromisoformat(ds)
            st.season = drows[0].get("season") or L.season_for(day)
            for gid, grs in L.group(drows, "g").items():
                st._cur_g = gid
                info = L.game_info(grs)
                for r in grs:
                    if r["pos"] == "G":
                        continue
                    o, h = info.get(r["t"], (None, None))
                    SX.add(st.skater_x(r["p"], r["pos"], r["t"], o, h, day),
                           [float(r.get(k) or 0) for k in L.SK_STATS] + [E.fantasy_points(r)],
                           (ds, gid, r["p"], r["pos"], st.season))
            st.update(day, drows)
        return st, SX, GS, GC
    return build


def test():
    rows0 = [r for r in history_rows() if r.get("season", "") >= os.environ.get("TEST_FROM_SEASON", "20082009")]
    for f in sorted(os.listdir(MDIR)) if os.path.isdir(MDIR) else []:
        MATES.update(rd(os.path.join(MDIR, f)) or {})
    log(f"linemates known for {len(MATES)} games")
    prod = (E.read_json(os.path.join(HERE, "ai", "models", "registry.json"), {}).get("production") or {})
    fam = {g: (prod.get(g) or {}).get("family") or {"F": "gbm_stats", "D": "poisson_stats"}[g] for g in ("F", "D")}
    out = {"asof": E.iso(datetime.now(timezone.utc)), "families": fam, "games_with_mates": len(MATES), "groups": {}}
    losses, folds = {}, {}
    orig_folds = L.folds_for
    for arm in os.environ.get("MATES_ARMS", "current,with_mates").split(","):
        rows = copy.deepcopy(rows0)
        if arm == "with_mates":
            build = patch()
            st, SX, GS, GC = build(rows)
        else:
            st, SX, GS, GC = L.build_dataset(rows)
        data = L.datasets(SX, GS, GC)
        for grp in ("F", "D"):
            X, Y, dates, keys = data[grp]
            cut = getattr(L, "TRAIN_FROM", {}).get(grp)
            if cut:
                m = dates >= cut
                X, Y, dates = X[m], Y[m], dates[m]
            if grp not in folds:
                folds[grp] = orig_folds(dates, L.CFG)
            L.folds_for = (lambda f: (lambda d, c: f))(folds[grp])
            keep = L.FAMILIES[grp]
            L.FAMILIES[grp] = {fam[grp]: keep[fam[grp]]}
            try:
                wf = L.walk_forward(grp, X, Y, dates, keys, L.CFG)
            finally:
                L.FAMILIES[grp] = keep
            losses[(arm, grp)] = wf["losses"][fam[grp]]
            log(arm, grp, "MAE", round(float(losses[(arm, grp)].mean()), 4))
            if arm == "with_mates" and ("current", grp) in losses:
                b, e = losses[("current", grp)], losses[(arm, grp)]
                d = e - b
                out["groups"][grp] = {"n": int(len(d)), "current": round(float(b.mean()), 4), "with_mates": round(float(e.mean()), 4),
                                      "diff": round(float(d.mean()), 4), "se": round(float(d.std(ddof=1) / math.sqrt(len(d))), 4),
                                      "pct": round(float(-d.mean() / b.mean() * 100), 2), "recent_diff": round(float(d[wf["recent"]].mean()), 4)}
        del data, SX, st
    os.makedirs(os.path.join(HERE, "ai", "research"), exist_ok=True)
    out["arms"] = "mate_prev only" if "--prev-only" in sys.argv else "mate_now + mate_n + mate_prev"
    with open(os.path.join(HERE, "ai", "research", "mates_exp_prev.json" if "--prev-only" in sys.argv else "mates_exp.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1)
    log(json.dumps(out))


if __name__ == "__main__":
    if "--download" in sys.argv:
        download()
    if "--test" in sys.argv:
        test()
