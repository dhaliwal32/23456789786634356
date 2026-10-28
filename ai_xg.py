"""
ai_xg.py - research: expected goals (xG) for the AI.

  --download   reads every game's play-by-play from the NHL (games listed in the saved history),
               keeps only the shots (where, what kind, rebound, rush, strength) in ai/xg/shots/<season>.json.gz
  --fit        trains a shot-quality model on older seasons (before TEST_FROM, so the test stays fair)
               and writes per player-game and per team-game xG to ai/xg/agg.json.gz
  --test       re-runs the AI's walk-forward test with and without xG inputs (same months, same history)
               and writes ai/research/xg_exp.json
Nothing here changes the live AI.
"""
import gzip
import json
import math
import os
import pickle
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
XDIR = os.path.join(HERE, "ai", "xg")
SDIR = os.path.join(XDIR, "shots")
OLDER_ROOT = os.path.join(HERE, "ai", "older")
TEST_FROM = "2025-10-01"
FIRST_SEASON = "20102011"
AL = {"LAK": "LA", "NJD": "NJ", "SJS": "SJ", "TBL": "TB", "UTAH": "UTA", "ARI": "UTA", "PHX": "UTA", "ATL": "WPG"}
KINDS = {"goal": 1, "shot-on-goal": 2, "missed-shot": 3}
STYPES = ["wrist", "snap", "slap", "backhand", "tip-in", "deflected", "wrap-around", "poke", "bat", "between-legs", "cradle"]


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
    seen = {}
    for root in (OLDER_ROOT, HERE):
        for r in L.load_history(root):
            seen[(r.get("g"), r.get("p"))] = r
    return sorted(seen.values(), key=lambda r: (r["d"], r["g"] or 0))


def secs(t):
    try:
        m, s = str(t).split(":")
        return int(m) * 60 + int(s)
    except Exception:
        return 0


def shots_of(js):
    """compact unblocked shot attempts: [period, sec, team, shooter, dist, angle, kind, stype, rebound, rush, strength, empty_net, goal]"""
    home, away = js.get("homeTeam") or {}, js.get("awayTeam") or {}
    tid = {home.get("id"): (AL.get(home.get("abbrev"), home.get("abbrev")), True), away.get("id"): (AL.get(away.get("abbrev"), away.get("abbrev")), False)}
    out, prev = [], None
    for p in js.get("plays") or []:
        pd = p.get("periodDescriptor") or {}
        if pd.get("periodType") == "SO":
            continue
        d = p.get("details") or {}
        k = p.get("typeDescKey")
        per, sec = pd.get("number") or 0, secs(p.get("timeInPeriod"))
        if k in KINDS and d.get("xCoord") is not None and d.get("yCoord") is not None and d.get("eventOwnerTeamId") in tid:
            team, is_home = tid[d["eventOwnerTeamId"]]
            x, y = float(d["xCoord"]), float(d["yCoord"])
            side = p.get("homeTeamDefendingSide")
            if side in ("left", "right"):
                home_net = -89.0 if side == "left" else 89.0
                net = -home_net if is_home else home_net
            else:
                net = 89.0 if x >= 0 else -89.0
            dx = abs(net - x)
            dist, ang = math.hypot(dx, y), abs(math.degrees(math.atan2(y, dx)))
            sc = str(p.get("situationCode") or "1551")
            ag, ask, hsk, hg = (int(c) for c in sc) if len(sc) == 4 and sc.isdigit() else (1, 5, 5, 1)
            my, op, opg = (hsk, ask, ag) if is_home else (ask, hsk, hg)
            strength = 1 if my > op else -1 if my < op else 0
            st = d.get("shotType") or ""
            reb = rush = 0
            if prev and prev[0] == per and 0 <= sec - prev[1] <= 3 and (prev[2] in KINDS or prev[2] == "blocked-shot") and prev[3] == team:
                reb = 1
            if prev and prev[0] == per and 0 <= sec - prev[1] <= 4 and prev[4] in ("N", "D") and prev[3] == team:
                rush = 1
            shooter = d.get("shootingPlayerId") or d.get("scoringPlayerId")
            out.append([per, sec, team, shooter, round(dist, 1), round(ang, 1), KINDS[k],
                        STYPES.index(st) if st in STYPES else -1, reb, rush, strength, 1 if opg == 0 else 0, 1 if k == "goal" else 0])
        if k:
            own = tid.get(d.get("eventOwnerTeamId"), (None, None))[0]
            prev = (per, sec, k, own, d.get("zoneCode"))
    return out


def download():
    rows = history_rows()
    games = {}
    for r in rows:
        if r.get("season", "") >= FIRST_SEASON and r.get("g"):
            games.setdefault(r["season"], {})[r["g"]] = r["d"]
    s = __import__("requests").Session()
    s.headers.update(E.HDR)

    def one(gid):
        for attempt in range(3):
            try:
                r = s.get(f"https://api-web.nhle.com/v1/gamecenter/{gid}/play-by-play", timeout=30)
                if r.status_code == 404:
                    return gid, None
                r.raise_for_status()
                return gid, shots_of(r.json())
            except Exception:
                time.sleep(2 + attempt * 3)
        return gid, False

    for season in sorted(games):
        path = os.path.join(SDIR, f"{season}.json.gz")
        have = rd(path) or {}
        todo = [g for g in games[season] if str(g) not in have or (games[season][g] >= "2026-09-01")]
        if not todo:
            continue
        log(f"{season}: {len(todo)} games to read ({len(have)} saved)")
        t0, bad = time.time(), 0
        with ThreadPoolExecutor(max_workers=8) as ex:
            for gid, sh in ex.map(one, todo):
                if sh is False:
                    bad += 1
                    continue
                have[str(gid)] = {"d": games[season][gid], "s": sh or []}
        wr(path, have)
        log(f"{season}: saved {len(have)} games ({bad} failed) in {time.time() - t0:.0f}s")


def shot_X(s):
    per, sec, team, shooter, dist, ang, kind, stype, reb, rush, strength, en, goal = s
    oh = [1.0 if stype == i else 0.0 for i in range(len(STYPES))]
    return [dist, ang, math.log1p(dist), dist * ang / 90.0, float(reb), float(rush), float(strength == 1), float(strength == -1), float(en),
            float(per >= 4), float(kind == 3)] + oh


def fit():
    from sklearn.ensemble import HistGradientBoostingClassifier
    X, Y = [], []
    allg = {}
    for f in sorted(os.listdir(SDIR)) if os.path.isdir(SDIR) else []:
        G = rd(os.path.join(SDIR, f)) or {}
        allg.update(G)
        for gid, g in G.items():
            if g["d"] < TEST_FROM:
                for s in g["s"]:
                    X.append(shot_X(s)); Y.append(s[12])
    log(f"xG training shots: {len(Y)} (goals {int(sum(Y))})")
    m = HistGradientBoostingClassifier(max_iter=300, learning_rate=0.05, max_leaf_nodes=31, min_samples_leaf=200, random_state=0)
    m.fit(np.array(X), np.array(Y))
    with open(os.path.join(XDIR, "xg_model.pkl"), "wb") as fh:
        pickle.dump(m, fh)
    # check: log loss on the test months versus a distance-only rate
    Xt, Yt = [], []
    for gid, g in allg.items():
        if g["d"] >= TEST_FROM:
            for s in g["s"]:
                Xt.append(shot_X(s)); Yt.append(s[12])
    if Yt:
        p = np.clip(m.predict_proba(np.array(Xt))[:, 1], 1e-4, 1 - 1e-4); y = np.array(Yt)
        base = np.clip(np.full(len(y), np.mean(Y)), 1e-4, 1 - 1e-4)
        ll = lambda q: float(-np.mean(y * np.log(q) + (1 - y) * np.log(1 - q)))
        log(f"xG check on unseen months: log loss {ll(p):.4f} vs league rate {ll(base):.4f}; xG {p.sum():.0f} vs goals {y.sum():.0f}")
    agg = {}
    gids = list(allg)
    for i in range(0, len(gids), 2000):
        chunk = gids[i:i + 2000]
        S = [(gid, s) for gid in chunk for s in allg[gid]["s"]]
        if not S:
            continue
        pr = m.predict_proba(np.array([shot_X(s) for _, s in S]))[:, 1]
        for (gid, s), q in zip(S, pr):
            a = agg.setdefault(gid, {"p": {}, "t": {}})
            if s[3]:
                v = a["p"].setdefault(str(s[3]), [0.0, 0])
                v[0] += float(q); v[1] += 1
            t = a["t"].setdefault(s[2], [0.0, 0.0])
            t[0] += float(q)
            if s[10] == 1:
                t[1] += float(q)
    for a in agg.values():
        for v in a["p"].values():
            v[0] = round(v[0], 4)
        for v in a["t"].values():
            v[0], v[1] = round(v[0], 3), round(v[1], 3)
    wr(os.path.join(XDIR, "agg.json.gz"), agg)
    log(f"xG totals saved for {len(agg)} games")


# ---------------------------------------------------------------- test: the AI with xG inputs
def patch_xg():
    """the AI's code with xG inputs added (same as the change that would put it live)"""
    L.USAGE = ["toi", "pptoi", "ixg", "iff"]
    L.DEFAULT["F"].update({"ixg": 0.24, "iff": 2.4})
    L.DEFAULT["D"].update({"ixg": 0.08, "iff": 1.5})
    L.TEAM_DEFAULT.update({"xgf": 2.9, "xga": 2.9})
    L.SK_FEATS = ([f"{k}_{dn}" for dn, _ in L.DECAYS for k in L.SK_STATS + L.USAGE] + [f"n_{dn}" for dn, _ in L.DECAYS]
                  + ["gp_log", "sgp_log", "sh_pct", "rest", "b2b", "home", "own_gf", "own_sf",
                     "opp_ga", "opp_sa", "opp_sf", "opp_gf", "opp_b2b", "own_xgf", "opp_xga", "ixg_finish"])
    L.IDX = {n: i for i, n in enumerate(L.SK_FEATS)}
    old_init, old_x, old_upd, old_sk = L.State.__init__, L.State.skater_x, L.State.update, L.State._update_skater

    def init(self):
        old_init(self)
        self.lgt["xgf"], self.lgt["xga"] = [0.0, 0.0], [0.0, 0.0]

    def skater_x(self, pid, pos, t, o, h, day, last=None):
        x = old_x(self, pid, pos, t, o, h, day, last)
        p = self.pl.get(pid) if pid is not None else None
        g_l = p["S"]["l"]["G"] if p else 0.0
        xg_l = p["S"]["l"].get("ixg", 0.0) if p else 0.0
        return x + [self.trel(t, "xgf"), self.trel(o, "xga"), (g_l + 3.0) / (xg_l + 3.0)]

    def upd_sk(self, r, day):
        for k in ("ixg", "iff"):
            if r.get(k) is not None:
                r[k] = float(r[k]) * 60.0  # minutes() divides plain numbers by 60
        old_sk(self, r, day)

    L.State.__init__, L.State.skater_x, L.State._update_skater = init, skater_x, upd_sk

    orig_update = old_upd

    def team_update(self, day, rows):
        orig_update(self, day, rows)
        for gid, grs in L.group(rows, "g").items():
            T = grs[0].get("_xgt")
            if not T:
                continue
            teams = list(T)
            for t in teams:
                o = next((u for u in teams if u != t), None)
                if o is None or t not in self.tm:
                    continue
                ts = self.tm[t]
                for k, v in (("xgf", T[t]), ("xga", T[o])):
                    ts["S"].setdefault(k, 0.0)
                    ts["S"][k] = ts["S"][k] * L.TEAM_DECAY + v
                    self.lgt[k][0] += v
                    self.lgt[k][1] += 1
    L.State.update = team_update

    def trel(self, t, k):
        ts = self.tm.get(t) if t else None
        m = self.tmean(k)
        if not ts or k not in ts["S"]:
            return 1.0
        return ((ts["S"][k] + 5 * m) / (ts["N"] + 5)) / m
    L.State.trel = trel


def attach(rows):
    agg = rd(os.path.join(XDIR, "agg.json.gz")) or {}
    n = 0
    for r in rows:
        a = agg.get(str(r.get("g")))
        if not a:
            continue
        if r["pos"] != "G":
            v = a["p"].get(str(r.get("p")))
            r["ixg"], r["iff"] = (v[0], v[1]) if v else (0.0, 0)
            n += 1
        r["_xgt"] = {t: v[0] for t, v in a["t"].items()}
    log(f"xG attached to {n} skater-games")
    return rows


def test():
    import copy
    rows0 = [r for r in history_rows() if r.get("season", "") >= FIRST_SEASON]
    prod = (E.read_json(os.path.join(HERE, "ai", "models", "registry.json"), {}).get("production") or {})
    fam = {g: (prod.get(g) or {}).get("family") or {"F": "gbm_stats", "D": "poisson_stats"}[g] for g in ("F", "D")}
    out = {"asof": E.iso(datetime.now(timezone.utc)), "families": fam, "history_from": FIRST_SEASON, "groups": {}}
    losses, folds = {}, {}
    orig_folds = L.folds_for
    for arm in ("current", "with_xg"):
        rows = copy.deepcopy(rows0)
        if arm == "with_xg":
            patch_xg()
            rows = attach(rows)
        st, SX, GS, GC = L.build_dataset(rows)
        data = L.datasets(SX, GS, GC)
        for grp in ("F", "D"):
            X, Y, dates, keys = data[grp]
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
            recent = wf["recent"]
            log(arm, grp, "MAE", round(float(losses[(arm, grp)].mean()), 4))
            if arm == "with_xg":
                b, e = losses[("current", grp)], losses[(arm, grp)]
                d = e - b
                out["groups"][grp] = {"n": int(len(d)), "current": round(float(b.mean()), 4), "with_xg": round(float(e.mean()), 4),
                                      "diff": round(float(d.mean()), 4), "se": round(float(d.std(ddof=1) / math.sqrt(len(d))), 4),
                                      "pct": round(float(-d.mean() / b.mean() * 100), 2), "recent_diff": round(float(d[recent].mean()), 4)}
    os.makedirs(os.path.join(HERE, "ai", "research"), exist_ok=True)
    with open(os.path.join(HERE, "ai", "research", "xg_exp.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1)
    log(json.dumps(out))


if __name__ == "__main__":
    if "--download" in sys.argv:
        download()
    if "--fit" in sys.argv:
        fit()
    if "--test" in sys.argv:
        test()
