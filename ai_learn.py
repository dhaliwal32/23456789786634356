"""
ai_learn.py  -  Fantasy Islands GM learning engine, STAGE 2 (learn -> validate -> promote -> predict)

Runs once a day in its own GitHub Actions workflow (ai-train.yml). It never touches
espn-data.js, espn_sync.py or the app; it only writes inside the ai/ folder.

  1. HISTORY   downloads every regular-season player-game since 2024-25 from the NHL,
               stored as small weekly compressed files so the repo grows slowly.
  2. FEATURES  replays the seasons day by day. Inputs for a game are built ONLY from
               games played on earlier dates (no peeking at the future).
  3. LEARN     trains several model types for forwards, defensemen and goalies.
  4. VALIDATE  walk-forward: train on everything before a month, test on that month,
               repeat for the latest months. Every score comes from games the model never saw.
  5. PROMOTE   a new model replaces the live one only if it is clearly better
               (more than 2 standard errors AND at least 0.5% better AND not worse in the
               most recent month). A live model that falls behind the simple baseline is
               rolled back automatically. Every decision is logged in ai/models/registry.json.
  6. PREDICT   writes AI projections for the next 7 days to ai/models/ai_proj.json.

Commands:
  python ai_learn.py --daily            normal daily run (retrains on Mondays or when needed)
  python ai_learn.py --daily --train    force a retrain today
  python ai_learn.py --selftest         offline tests on synthetic data
  python ai_learn.py --livetest         read-only check of the historical NHL download
"""
import gzip
import hashlib
import json
import math
import os
import pickle
import platform
import random
import shutil
import sys
import tempfile
import time
import traceback
from array import array
from datetime import date, datetime, timedelta

import numpy as np

import ai_engine as E

VERSION = "ai-stage2-v1"
HERE = E.HERE
SEASONS = [("20242025", "2024-10-01", "2025-04-20"),
           ("20252026", "2025-10-01", "2026-04-20"),
           ("20262027", "2026-09-25", "2027-04-25")]
SK_STATS = ["G", "A", "PM", "PPP", "SHP", "SOG", "HIT", "BLK"]
USAGE = ["toi", "pptoi"]
G_STATS = ["W", "OTL", "GA", "SV", "SO"]
DECAYS = (("s", 0.75), ("m", 0.93), ("l", 0.985))   # memory ~2, ~10, ~45 games
K_PRIOR = 5.0          # shrink small samples toward the league average (partial pooling)
TEAM_K = ("gf", "ga", "sf", "sa")
TEAM_DECAY = 0.9
SHARE_DECAY = 0.85
GOALIE_WINDOW = 45
DEFAULT = {"F": {"G": .16, "A": .24, "PM": 0.0, "PPP": .08, "SHP": .006, "SOG": 1.9, "HIT": 1.2, "BLK": .55,
                 "toi": 15.0, "pptoi": 1.4},
           "D": {"G": .05, "A": .21, "PM": 0.0, "PPP": .06, "SHP": .004, "SOG": 1.3, "HIT": 1.3, "BLK": 1.4,
                 "toi": 20.0, "pptoi": 0.9}}
TEAM_DEFAULT = {"gf": 3.0, "ga": 3.0, "sf": 28.5, "sa": 28.5}
SV_DEFAULT = 0.900
CFG = {"folds": 6, "min_test": 1500, "min_train": 5000, "promote_se": 2.0, "min_gain": 0.005, "keep_models": 3}

SK_FEATS = ([f"{k}_{dn}" for dn, _ in DECAYS for k in SK_STATS + USAGE] + [f"n_{dn}" for dn, _ in DECAYS]
            + ["gp_log", "sgp_log", "sh_pct", "rest", "b2b", "home", "own_gf", "own_sf",
               "opp_ga", "opp_sa", "opp_sf", "opp_gf", "opp_b2b"])
GO_FEATS = ["share", "share_n", "prev_start", "sv", "sv_n", "gp_log", "rest", "b2b", "home",
            "own_sa", "own_gf", "opp_sf", "opp_gf", "opp_ga", "opp_b2b", "n_cands"]
SK_T = SK_STATS + ["fp"]
GC_T = G_STATS + ["SA", "fp"]
IDX = {n: i for i, n in enumerate(SK_FEATS)}
GIDX = {n: i for i, n in enumerate(GO_FEATS)}
FEATURE_HASH = hashlib.sha1(json.dumps([VERSION, SK_FEATS, GO_FEATS]).encode()).hexdigest()[:10]


def H(root, *parts):
    return os.path.join(root, "ai", *parts)


def r4(x):
    return None if x is None or x != x else round(float(x), 4)


def season_for(d):
    ds = d.isoformat()
    cur = SEASONS[0][0]
    for s, a, _ in SEASONS:
        if a <= ds:
            cur = s
    return cur


def minutes(x):
    if x is None:
        return None
    if isinstance(x, str):
        if ":" in x:
            m, s = x.split(":", 1)
            try:
                return int(m) + int(s) / 60.0
            except ValueError:
                return None
        try:
            x = float(x)
        except ValueError:
            return None
    return float(x) / 60.0


def group(rows, key):
    out = {}
    for r in rows:
        out.setdefault(r[key], []).append(r)
    return out


def shots_against(r):
    sa = r.get("SA")
    return float(sa) if sa is not None else float((r.get("SV") or 0) + (r.get("GA") or 0))


def starter_of(grs, t):
    return next((r["p"] for r in grs if r["pos"] == "G" and r["t"] == t and (r.get("GS") or 0) >= 1), None)


# ----------------------------------------------------------------- 1. HISTORY
def save_gz(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "wb") as raw:
        with gzip.GzipFile(fileobj=raw, mode="wb", mtime=0) as gz:
            gz.write(json.dumps(obj, separators=(",", ":"), sort_keys=True).encode("utf-8"))
    os.replace(tmp, path)


def load_gz(path, default=None):
    try:
        with gzip.open(path, "rt", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError, EOFError):
        return default


def stats_query(kind, start, end):
    exp = f'gameDate<="{end} 23:59:59" and gameDate>="{start}" and gameTypeId=2'
    js = E.http_json(f"{E.STATS}/{kind}", {"isAggregate": "false", "isGame": "true", "limit": -1, "cayenneExp": exp})
    data = js.get("data") or []
    total = js.get("total")
    if isinstance(total, int) and total > len(data):
        raise OverflowError(f"{kind} {start}..{end}: got {len(data)} of {total} rows")
    return data


def _num(r, *keys):
    for k in keys:
        if r.get(k) is not None:
            return r.get(k)
    return None


def fetch_range(start, end):
    """Every regular-season player-game between two dates (inclusive), in history format."""
    try:
        parts = {k: stats_query(k, start, end)
                 for k in ("skater/summary", "skater/realtime", "skater/timeonice", "goalie/summary")}
    except OverflowError:
        d0, d1 = date.fromisoformat(start), date.fromisoformat(end)
        if d0 >= d1:
            raise
        mid = d0 + (d1 - d0) // 2
        return fetch_range(start, mid.isoformat()) + fetch_range((mid + timedelta(days=1)).isoformat(), end)
    sk = {}
    for r in parts["skater/summary"]:
        k = (r.get("gameId"), r.get("playerId"))
        sk[k] = {"g": r.get("gameId"), "d": str(r.get("gameDate"))[:10], "p": r.get("playerId"),
                 "n": r.get("skaterFullName"), "t": E.ab(r.get("teamAbbrev")),
                 "o": E.ab(r.get("opponentTeamAbbrev")) or None, "h": {"H": 1, "R": 0}.get(r.get("homeRoad")),
                 "pos": "D" if r.get("positionCode") == "D" else "F",
                 "G": r.get("goals") or 0, "A": r.get("assists") or 0, "PM": r.get("plusMinus") or 0,
                 "PPP": r.get("ppPoints") or 0, "SHP": r.get("shPoints") or 0, "SOG": r.get("shots") or 0,
                 "HIT": 0, "BLK": 0, "toi": r.get("timeOnIcePerGame"), "pptoi": None}
    for r in parts["skater/realtime"]:
        k = (r.get("gameId"), r.get("playerId"))
        if k in sk:
            sk[k]["HIT"] = r.get("hits") or 0
            sk[k]["BLK"] = r.get("blockedShots") or 0
    for r in parts["skater/timeonice"]:
        k = (r.get("gameId"), r.get("playerId"))
        if k in sk:
            sk[k]["pptoi"] = _num(r, "ppTimeOnIce", "ppTimeOnIcePerGame")
            if sk[k]["toi"] is None:
                sk[k]["toi"] = _num(r, "timeOnIce", "timeOnIcePerGame")
    go = []
    for r in parts["goalie/summary"]:
        go.append({"g": r.get("gameId"), "d": str(r.get("gameDate"))[:10], "p": r.get("playerId"),
                   "n": r.get("goalieFullName"), "t": E.ab(r.get("teamAbbrev")),
                   "o": E.ab(r.get("opponentTeamAbbrev")) or None, "h": {"H": 1, "R": 0}.get(r.get("homeRoad")),
                   "pos": "G", "GS": r.get("gamesStarted") or 0, "W": r.get("wins") or 0,
                   "OTL": r.get("otLosses") or 0, "GA": r.get("goalsAgainst") or 0, "SV": r.get("saves") or 0,
                   "SA": r.get("shotsAgainst"), "SO": r.get("shutouts") or 0, "toi": r.get("timeOnIce")})
    rows = list(sk.values()) + go
    teams = {}
    for r in rows:
        teams.setdefault(r["g"], set()).add(r["t"])
    for r in rows:
        if not r.get("o"):
            other = [t for t in teams.get(r["g"], ()) if t != r["t"]]
            r["o"] = other[0] if len(other) == 1 else None
    return rows


def update_history(root, today, fetch, log=print, pause=0.2):
    ipath = H(root, "history", "index.json")
    idx = E.read_json(ipath, {})
    n = 0
    for season, s, e in SEASONS:
        last_day, d0 = date.fromisoformat(e), date.fromisoformat(s)
        while d0 <= last_day and d0 < today:
            d1 = min(d0 + timedelta(days=6), last_day)
            key = f"{season}/{d0.isoformat()}"
            if not idx.get(key, {}).get("complete"):
                end = min(d1, today - timedelta(days=1))
                try:
                    rows = fetch(d0.isoformat(), end.isoformat())
                    save_gz(H(root, "history", season, f"{d0.isoformat()}.json.gz"), rows)
                    idx[key] = {"rows": len(rows), "through": end.isoformat(),
                                "complete": d1 <= today - timedelta(days=4)}
                    n += 1
                    if pause:
                        time.sleep(pause)
                except Exception as ex:
                    log(f"(learn) could not download {key}: {type(ex).__name__}: {ex}")
            d0 += timedelta(days=7)
    E.write_json(ipath, idx)
    if n:
        log(f"(learn) history: refreshed {n} weekly files")
    return n


def load_history(root):
    idx = E.read_json(H(root, "history", "index.json"), {})
    seen = {}
    for key in sorted(idx):
        season, d0 = key.split("/")
        for r in load_gz(H(root, "history", season, f"{d0}.json.gz"), []) or []:
            r["season"] = season
            seen[(r.get("g"), r.get("p"))] = r
    return sorted((r for r in seen.values() if r.get("d") and r.get("t")), key=lambda r: (r["d"], r["g"] or 0))


# ----------------------------------------------------------------- 2. FEATURES (point-in-time)
class State:
    """Everything known about players and teams BEFORE the day being processed."""

    def __init__(self):
        self.pl, self.gl, self.tm, self.share = {}, {}, {}, {}
        self.lg = {"F": {}, "D": {}}
        self.lgt = {k: [0.0, 0.0] for k in TEAM_K}
        self.lsv = [0.0, 0.0]
        self.team_days, self.team_goalies, self.prev_starter, self.names = {}, {}, {}, {}
        self.season = None

    def lmean(self, pos, k):
        s, n = self.lg[pos].get(k, (0.0, 0.0))
        return (s + 200 * DEFAULT[pos][k]) / (n + 200)

    def tmean(self, k):
        s, n = self.lgt[k]
        return (s + 50 * TEAM_DEFAULT[k]) / (n + 50)

    def trel(self, t, k):
        ts = self.tm.get(t) if t else None
        m = self.tmean(k)
        if not ts:
            return 1.0
        return ((ts["S"][k] + 5 * m) / (ts["N"] + 5)) / m

    def sv_mean(self):
        return (self.lsv[0] + 5000 * SV_DEFAULT) / (self.lsv[1] + 5000)

    def played(self, t, day):
        return 1.0 if t and day in self.team_days.get(t, ()) else 0.0

    def candidates(self, t, day):
        return sorted(g for g, last in self.team_goalies.get(t, {}).items()
                      if last < day and (day - last).days <= GOALIE_WINDOW)

    def skater_x(self, pid, pos, t, o, h, day, last=None):
        p = self.pl.get(pid) if pid is not None else None
        x = []
        for dn, _ in DECAYS:
            n = p["N"][dn] if p else 0.0
            for k in SK_STATS + USAGE:
                s = p["S"][dn][k] if p else 0.0
                x.append((s + K_PRIOR * self.lmean(pos, k)) / (n + K_PRIOR))
        for dn, _ in DECAYS:
            x.append(p["N"][dn] if p else 0.0)
        gp = p["gp"] if p else 0
        sgp = p["sgp"] if p and p["season"] == self.season else 0
        prior_pct = self.lmean(pos, "G") / max(self.lmean(pos, "SOG"), 1e-6)
        g_l = p["S"]["l"]["G"] if p else 0.0
        s_l = p["S"]["l"]["SOG"] if p else 0.0
        last = last or (p["last"] if p else None)
        rest = min(10, (day - last).days) if last else 5
        yday = day - timedelta(days=1)
        x += [math.log1p(gp), math.log1p(sgp), (g_l + 50 * prior_pct) / (s_l + 50), float(rest),
              1.0 if rest == 1 else 0.0, 0.5 if h is None else float(h),
              self.trel(t, "gf"), self.trel(t, "sf"), self.trel(o, "ga"), self.trel(o, "sa"),
              self.trel(o, "sf"), self.trel(o, "gf"), self.played(o, yday)]
        return x

    def goalie_x(self, gid, t, o, h, day, n_cands):
        g = self.gl.get(gid) if gid is not None else None
        sh = self.share.get((gid, t)) if gid is not None else None
        svm = self.sv_mean()
        last = g["last"] if g else None
        rest = min(10, (day - last).days) if last else 5
        yday = day - timedelta(days=1)
        return [(sh[0] + 1.0) / (sh[1] + 2.0) if sh else 0.35, sh[1] if sh else 0.0,
                1.0 if gid is not None and self.prev_starter.get(t) == gid else 0.0,
                (g["sv"] + 600 * svm) / (g["sa"] + 600) if g else svm, g["sa"] if g else 0.0,
                math.log1p(g["gp"] if g else 0), float(rest), self.played(t, yday), 0.5 if h is None else float(h),
                self.trel(t, "sa"), self.trel(t, "gf"), self.trel(o, "sf"), self.trel(o, "gf"), self.trel(o, "ga"),
                self.played(o, yday), float(n_cands)]

    def update(self, day, rows):
        for _, grs in group(rows, "g").items():
            tot = {}
            for r in grs:
                x = tot.setdefault(r["t"], {"gf": 0.0, "ga": 0.0, "sf": 0.0, "sa": 0.0})
                if r["pos"] == "G":
                    x["ga"] += r.get("GA") or 0
                    x["sa"] += shots_against(r)
                else:
                    x["gf"] += r.get("G") or 0
                    x["sf"] += r.get("SOG") or 0
            for t, x in tot.items():
                if not t:
                    continue
                ts = self.tm.setdefault(t, {"S": {k: 0.0 for k in TEAM_K}, "N": 0.0})
                for k in TEAM_K:
                    ts["S"][k] = ts["S"][k] * TEAM_DECAY + x[k]
                    self.lgt[k][0] += x[k]
                    self.lgt[k][1] += 1
                ts["N"] = ts["N"] * TEAM_DECAY + 1.0
                self.team_days.setdefault(t, set()).add(day)
                starter = starter_of(grs, t)
                cands = set(self.candidates(t, day)) | {r["p"] for r in grs if r["pos"] == "G" and r["t"] == t}
                for g in cands:
                    s = self.share.setdefault((g, t), [0.0, 0.0])
                    s[0] = s[0] * SHARE_DECAY + (1.0 if g == starter else 0.0)
                    s[1] = s[1] * SHARE_DECAY + 1.0
                if starter is not None:
                    self.prev_starter[t] = starter
            for r in grs:
                self.names[r["p"]] = (r.get("n"), r["pos"], r["t"], day)
                if r["pos"] == "G":
                    g = self.gl.setdefault(r["p"], {"sv": 0.0, "sa": 0.0, "gp": 0, "last": None})
                    sa, sv = shots_against(r), float(r.get("SV") or 0)
                    g["sv"] = g["sv"] * 0.98 + sv
                    g["sa"] = g["sa"] * 0.98 + sa
                    g["gp"] += 1
                    g["last"] = day
                    self.team_goalies.setdefault(r["t"], {})[r["p"]] = day
                    self.lsv[0] += sv
                    self.lsv[1] += sa
                else:
                    self._update_skater(r, day)

    def _update_skater(self, r, day):
        pos = r["pos"]
        p = self.pl.get(r["p"])
        if p is None:
            p = self.pl[r["p"]] = {"S": {dn: {k: 0.0 for k in SK_STATS + USAGE} for dn, _ in DECAYS},
                                   "N": {dn: 0.0 for dn, _ in DECAYS}, "gp": 0, "sgp": 0,
                                   "season": self.season, "last": None}
        if p["season"] != self.season:
            p["season"], p["sgp"] = self.season, 0
        vals = {k: float(r.get(k) or 0) for k in SK_STATS}
        for k in USAGE:
            m = minutes(r.get(k))
            vals[k] = m if m is not None else self.lmean(pos, k)
        for dn, dec in DECAYS:
            S = p["S"][dn]
            for k, v in vals.items():
                S[k] = S[k] * dec + v
            p["N"][dn] = p["N"][dn] * dec + 1.0
        p["gp"] += 1
        p["sgp"] += 1
        p["last"] = day
        for k, v in vals.items():
            a = self.lg[pos].setdefault(k, [0.0, 0.0])
            a[0] += v
            a[1] += 1


class Coll:
    def __init__(self, feats, targets):
        self.feats, self.targets = feats, targets
        self.X, self.Y, self.meta = array("d"), array("d"), []

    def add(self, x, y, meta):
        if len(x) != len(self.feats):
            raise ValueError(f"feature length {len(x)} != {len(self.feats)}")
        self.X.extend(x)
        self.Y.extend(y)
        self.meta.append(meta)

    def arrays(self):
        n = len(self.meta)
        if not n:
            return np.zeros((0, len(self.feats))), np.zeros((0, len(self.targets)))
        return (np.array(self.X, dtype=float).reshape(n, len(self.feats)),
                np.array(self.Y, dtype=float).reshape(n, len(self.targets)))


def game_info(grs):
    teams = sorted({r["t"] for r in grs if r.get("t")})
    info = {}
    for t in teams:
        r0 = next((r for r in grs if r["t"] == t), {})
        o = r0.get("o") or next((x for x in teams if x != t), None)
        info[t] = (o, r0.get("h"))
    return info


def build_dataset(rows):
    st = State()
    SX, GS, GC = Coll(SK_FEATS, SK_T), Coll(GO_FEATS, ["start"]), Coll(GO_FEATS, GC_T)
    for ds, drows in sorted(group(rows, "d").items()):
        day = date.fromisoformat(ds)
        st.season = drows[0].get("season") or season_for(day)
        for gid, grs in group(drows, "g").items():
            info = game_info(grs)
            for r in grs:
                if r["pos"] == "G":
                    continue
                o, h = info.get(r["t"], (None, None))
                SX.add(st.skater_x(r["p"], r["pos"], r["t"], o, h, day),
                       [float(r.get(k) or 0) for k in SK_STATS] + [E.fantasy_points(r)],
                       (ds, gid, r["p"], r["pos"], st.season))
            for t, (o, h) in info.items():
                cands = st.candidates(t, day)
                starter = starter_of(grs, t)
                for g in cands:
                    GS.add(st.goalie_x(g, t, o, h, day, len(cands)), [1.0 if g == starter else 0.0],
                           (ds, gid, g, t, st.season))
                for r in grs:
                    if r["pos"] == "G" and r["t"] == t and (r.get("GS") or 0) >= 1:
                        GC.add(st.goalie_x(r["p"], t, o, h, day, len(cands)),
                               [float(r.get(k) or 0) for k in G_STATS] + [shots_against(r), E.fantasy_points(r)],
                               (ds, gid, r["p"], t, st.season))
        st.update(day, drows)
    return st, SX, GS, GC


def datasets(SX, GS, GC):
    out = {}
    Xs, Ys = SX.arrays()
    ds = np.array([m[0] for m in SX.meta], dtype="U10")
    pos = np.array([m[3] for m in SX.meta], dtype="U1")
    for g in ("F", "D"):
        k = pos == g
        out[g] = (Xs[k], Ys[k], ds[k], None)
    Xg, Yg = GS.arrays()
    out["G_start"] = (Xg, Yg, np.array([m[0] for m in GS.meta], dtype="U10"), [(m[0], m[3]) for m in GS.meta])
    Xc, Yc = GC.arrays()
    out["G_cond"] = (Xc, Yc, np.array([m[0] for m in GC.meta], dtype="U10"), None)
    return out


# ----------------------------------------------------------------- 3. MODELS
def _hgb_reg(loss):
    from sklearn.ensemble import HistGradientBoostingRegressor
    return HistGradientBoostingRegressor(loss=loss, max_iter=150, learning_rate=0.05, max_leaf_nodes=15,
                                         min_samples_leaf=100, l2_regularization=1.0, early_stopping=False,
                                         random_state=0)


def _hgb_clf():
    from sklearn.ensemble import HistGradientBoostingClassifier
    return HistGradientBoostingClassifier(max_iter=150, learning_rate=0.05, max_leaf_nodes=15,
                                          min_samples_leaf=100, l2_regularization=1.0, early_stopping=False,
                                          random_state=0)


def _scaled(model):
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler
    return make_pipeline(StandardScaler(), model)


class Const:
    def __init__(self, v):
        self.v = float(v)

    def predict(self, X):
        return np.full(len(X), self.v)

    def predict_proba(self, X):
        p = np.full(len(X), self.v)
        return np.column_stack([1 - p, p])


def fp_sk(d):
    return sum(E.SK[k] * d[k] for k in SK_STATS)


def fp_go(d):
    return sum(E.GO[k] * d[k] for k in G_STATS)


class SkBaseline:
    """No learning: recent-form rates (about the last 10 games, shrunk to league average)."""

    def fit(self, X, Y):
        return self

    def predict(self, X):
        out = {k: X[:, IDX[k + "_m"]] for k in SK_STATS}
        out["fp"] = fp_sk(out)
        return out


class SkRidgeFP:
    def fit(self, X, Y):
        from sklearn.linear_model import Ridge
        self.m = _scaled(Ridge(alpha=10.0)).fit(X, Y[:, -1])
        return self

    def predict(self, X):
        return {"fp": self.m.predict(X)}


class SkPoissonStats:
    def fit(self, X, Y):
        from sklearn.linear_model import PoissonRegressor, Ridge
        self.m = {}
        for j, k in enumerate(SK_STATS):
            y = Y[:, j]
            if k == "PM":
                self.m[k] = _scaled(Ridge(alpha=10.0)).fit(X, y)
            elif len(y) and y.sum() > 0 and y.min() >= 0:
                self.m[k] = _scaled(PoissonRegressor(alpha=0.01, max_iter=300)).fit(X, y)
            else:
                self.m[k] = Const(y.mean() if len(y) else 0.0)
        return self

    def predict(self, X):
        out = {k: m.predict(X) for k, m in self.m.items()}
        out["fp"] = fp_sk(out)
        return out


class SkGBMFP:
    def fit(self, X, Y):
        self.m = _hgb_reg("squared_error").fit(X, Y[:, -1])
        return self

    def predict(self, X):
        return {"fp": self.m.predict(X)}


class SkGBMStats:
    def fit(self, X, Y):
        self.m = {}
        for j, k in enumerate(SK_STATS):
            y = Y[:, j]
            if k == "PM":
                self.m[k] = _hgb_reg("squared_error").fit(X, y)
            elif len(y) and y.sum() > 0 and y.min() >= 0:
                self.m[k] = _hgb_reg("poisson").fit(X, y)
            else:
                self.m[k] = Const(y.mean() if len(y) else 0.0)
        return self

    def predict(self, X):
        out = {k: (m.predict(X) if k == "PM" else np.clip(m.predict(X), 0, None)) for k, m in self.m.items()}
        out["fp"] = fp_sk(out)
        return out


class StBaseline:
    """No learning: each goalie's recent share of his team's starts."""

    def fit(self, X, Y):
        return self

    def predict(self, X):
        return X[:, GIDX["share"]]


class StLogit:
    def fit(self, X, Y):
        from sklearn.linear_model import LogisticRegression
        y = Y[:, 0].astype(int)
        self.m = _scaled(LogisticRegression(C=1.0, max_iter=1000)).fit(X, y) if len(set(y.tolist())) > 1 \
            else Const(y.mean() if len(y) else 0.5)
        return self

    def predict(self, X):
        return self.m.predict_proba(X)[:, 1]


class StGBM:
    def fit(self, X, Y):
        y = Y[:, 0].astype(int)
        self.m = _hgb_clf().fit(X, y) if len(set(y.tolist())) > 1 else Const(y.mean() if len(y) else 0.5)
        return self

    def predict(self, X):
        return self.m.predict_proba(X)[:, 1]


class GcBaseline:
    """No learning: expected shots x the goalie's shrunk save %, league-average win/SO/OTL rates."""

    def fit(self, X, Y):
        self.mean = {k: float(Y[:, j].mean()) if len(Y) else 0.0 for j, k in enumerate(GC_T)}
        return self

    def predict(self, X):
        sa = self.mean["SA"] * (X[:, GIDX["own_sa"]] + X[:, GIDX["opp_sf"]]) / 2.0
        sv = X[:, GIDX["sv"]]
        n = len(X)
        out = {"SV": sa * sv, "GA": sa * (1 - sv), "W": np.full(n, self.mean["W"]),
               "SO": np.full(n, self.mean["SO"]), "OTL": np.full(n, self.mean["OTL"])}
        out["fp"] = fp_go(out)
        return out


class GcGBM:
    def fit(self, X, Y):
        self.m = {}
        for j, k in enumerate(G_STATS):
            y = Y[:, j]
            if k in ("GA", "SV"):
                self.m[k] = _hgb_reg("poisson").fit(X, y) if len(y) and y.sum() > 0 else Const(y.mean() if len(y) else 0)
            else:
                yi = y.astype(int)
                self.m[k] = _hgb_clf().fit(X, yi) if len(set(yi.tolist())) > 1 else Const(y.mean() if len(y) else 0)
        return self

    def predict(self, X):
        out = {}
        for k, m in self.m.items():
            out[k] = np.clip(m.predict(X), 0, None) if k in ("GA", "SV") else m.predict_proba(X)[:, 1]
        out["fp"] = fp_go(out)
        return out


FAMILIES = {
    "F": {"baseline": SkBaseline, "ridge_fp": SkRidgeFP, "poisson_stats": SkPoissonStats,
          "gbm_fp": SkGBMFP, "gbm_stats": SkGBMStats},
    "D": {"baseline": SkBaseline, "ridge_fp": SkRidgeFP, "poisson_stats": SkPoissonStats,
          "gbm_fp": SkGBMFP, "gbm_stats": SkGBMStats},
    "G_start": {"baseline": StBaseline, "logit": StLogit, "gbm": StGBM},
    "G_cond": {"baseline": GcBaseline, "gbm_stats": GcGBM},
}
GROUP_NAMES = {"F": "forwards", "D": "defensemen", "G_start": "goalie start chance",
               "G_cond": "goalie points if he starts"}


def normalize(p, keys):
    tot = {}
    for v, k in zip(p, keys):
        tot[k] = tot.get(k, 0.0) + v
    return np.array([v / tot[k] if tot[k] > 0 else v for v, k in zip(p, keys)])


def main_pred(grp, model, X, keys=None):
    if grp == "G_start":
        p = np.clip(np.asarray(model.predict(X), dtype=float), 1e-3, 1.0)
        return normalize(p, keys) if keys is not None else p
    return np.asarray(model.predict(X)["fp"], dtype=float)


# ----------------------------------------------------------------- 4. VALIDATE (walk-forward)
def folds_for(dates, cfg):
    out = []
    for m in sorted(set(d[:7] for d in dates.tolist())):
        y, mo = int(m[:4]), int(m[5:7])
        a = m + "-01"
        b = f"{y + (mo == 12):04d}-{mo % 12 + 1:02d}-01"
        n_tr = int((dates < a).sum())
        n_te = int(((dates >= a) & (dates < b)).sum())
        if n_tr >= cfg["min_train"] and n_te >= cfg["min_test"]:
            out.append((a, b))
    return out[-cfg["folds"]:]


def loss_of(grp, pred, actual):
    return np.square(pred - actual) if grp == "G_start" else np.abs(pred - actual)


def walk_forward(grp, X, Y, dates, keys, cfg):
    fams = FAMILIES[grp]
    folds = folds_for(dates, cfg)
    n = len(dates)
    pred = {f: np.full(n, np.nan) for f in fams}
    fold_id = np.full(n, -1)
    for i, (a, b) in enumerate(folds):
        tr = dates < a
        te = (dates >= a) & (dates < b)
        kte = [keys[j] for j in np.flatnonzero(te)] if keys is not None else None
        for f, cls in fams.items():
            pred[f][te] = main_pred(grp, cls().fit(X[tr], Y[tr]), X[te], kte)
        fold_id[te] = i
    t = fold_id >= 0
    actual = Y[t, 0] if grp == "G_start" else Y[t, -1]
    fid = fold_id[t]
    return {"folds": folds, "actual": actual, "fold_id": fid,
            "preds": {f: pred[f][t] for f in fams},
            "losses": {f: loss_of(grp, pred[f][t], actual) for f in fams},
            "recent": fid == (len(folds) - 1)}


def mean_se(a):
    n = len(a)
    if not n:
        return float("nan"), float("nan")
    return float(a.mean()), (float(a.std(ddof=1)) / math.sqrt(n) if n > 1 else float("nan"))


def decide(losses, prod, cfg, recent):
    """Returns (family, event, reason). Conservative: the live model stays unless beaten clearly."""
    base = "baseline"
    avg = {f: float(l.mean()) for f, l in losses.items()}
    best = min(avg, key=avg.get)

    def clearly_better(a, b):
        m, se = mean_se(losses[a] - losses[b])
        rel = -m / avg[b] if avg[b] else 0.0
        rec = float((losses[a][recent] - losses[b][recent]).mean()) if recent.any() else 0.0
        ok = m < -cfg["promote_se"] * se and rel >= cfg["min_gain"] and rec <= 0
        return ok, m, se, rel

    if prod not in losses:
        prod = None
    if prod is None:
        if best != base:
            ok, m, se, rel = clearly_better(best, base)
            if ok:
                return best, "promote", f"first model: {best} beats the baseline by {rel:.1%} (±{2 * se:.3f})"
        return base, "promote", "first model: no learned model clearly beat the simple baseline yet"
    if prod != base:
        ok, m, se, rel = clearly_better(base, prod)
        if ok:
            return base, "rollback", f"live model {prod} fell {rel:.1%} behind the baseline on recent unseen games"
    if best != prod:
        ok, m, se, rel = clearly_better(best, prod)
        if ok:
            return best, "promote", f"{best} beats live model {prod} by {rel:.1%} (±{2 * se:.3f})"
        return prod, "keep", f"{best} scored slightly better than {prod}, but not clearly enough to switch"
    return prod, "keep", f"{prod} is still the most accurate"


def summarize_wf(grp, wf):
    L = wf["losses"]
    out = {"what": GROUP_NAMES[grp],
           "loss": "Brier score (lower is better)" if grp == "G_start" else "average miss in fantasy points (lower is better)",
           "families": {}, "folds": []}
    for f, l in L.items():
        m, se = mean_se(l)
        d, dse = mean_se(l - L["baseline"])
        out["families"][f] = {"n": int(len(l)), "loss": r4(m), "se": r4(se), "vs_baseline": r4(d), "vs_baseline_se": r4(dse)}
    for i, (a, b) in enumerate(wf["folds"]):
        k = wf["fold_id"] == i
        out["folds"].append({"from": a, "to": b, "n": int(k.sum()),
                             "loss": {f: r4(float(l[k].mean())) for f, l in L.items()}})
    return out


def intervals(pred, actual, fold_id):
    """80% ranges learned from earlier test months, checked on the latest month."""
    if len(pred) < 200:
        return None
    last = int(fold_id.max())
    cal, chk = fold_id < last, fold_id == last
    honest = True
    if cal.sum() < 100 or chk.sum() < 50:
        cal = chk = np.ones(len(pred), dtype=bool)
        honest = False
    edges = np.quantile(pred[cal], np.linspace(0, 1, 11)[1:-1])
    bc, ac = np.searchsorted(edges, pred[cal]), actual[cal]
    q = []
    for i in range(10):
        a = ac[bc == i]
        q.append([float(np.quantile(a, 0.1)), float(np.quantile(a, 0.9))] if len(a) else [0.0, 0.0])
    bk = np.searchsorted(edges, pred[chk])
    lo = np.array([q[i][0] for i in bk])
    hi = np.array([q[i][1] for i in bk])
    cov = float(((actual[chk] >= lo) & (actual[chk] <= hi)).mean())
    return {"edges": [round(float(e), 3) for e in edges], "q": [[round(a, 2), round(b, 2)] for a, b in q],
            "coverage_80": round(cov, 3), "checked_on": int(chk.sum()), "honest_check": honest}


def calib(p, y):
    out = []
    for lo, hi in ((0, .2), (.2, .5), (.5, .8), (.8, 1.01)):
        k = (p >= lo) & (p < hi)
        if k.any():
            out.append({"range": f"{int(lo * 100)}-{int(min(hi, 1) * 100)}%", "n": int(k.sum()),
                        "predicted": round(float(p[k].mean()), 3), "actual": round(float(y[k].mean()), 3)})
    return out


# ----------------------------------------------------------------- 5. TRAIN + PROMOTE
def prune(root, grp, keep, current):
    d = H(root, "models")
    files = sorted((f for f in os.listdir(d) if f.startswith(grp + "-") and f.endswith(".pkl")),
                   key=lambda f: f[:-4].rsplit("-", 1)[-1])
    for f in files[:-keep]:
        if f != current:
            os.remove(os.path.join(d, f))


def train(root, reg, data, now, cfg, log=print):
    import warnings
    import sklearn
    warnings.filterwarnings("ignore")
    if reg.get("feature_hash") != FEATURE_HASH:
        if reg.get("production"):
            log("(learn) model inputs changed since the last version - choosing models from scratch")
        reg["production"] = {}
        reg["feature_hash"] = FEATURE_HASH
    prod_all = reg.setdefault("production", {})
    val = E.read_json(H(root, "models", "validation.json"), {})
    val.setdefault("groups", {})
    for grp in FAMILIES:
        X, Y, dates, keys = data[grp]
        if len(dates) < cfg["min_train"]:
            log(f"(learn) {grp}: only {len(dates)} examples - not enough to train yet")
            continue
        t0 = time.time()
        wf = walk_forward(grp, X, Y, dates, keys, cfg)
        if not wf["folds"]:
            log(f"(learn) {grp}: not enough months of data to test fairly yet")
            continue
        prod = (prod_all.get(grp) or {}).get("family")
        choice, event, why = decide(wf["losses"], prod, cfg, wf["recent"])
        model = FAMILIES[grp][choice]().fit(X, Y)
        fn = f"{grp}-{choice}-{now.strftime('%Y%m%d')}.pkl"
        os.makedirs(H(root, "models"), exist_ok=True)
        with open(H(root, "models", fn), "wb") as f:
            pickle.dump(model, f)
        prune(root, grp, cfg["keep_models"], fn)
        prod_all[grp] = {"version": fn[:-4], "family": choice, "file": fn, "trained": E.iso(now),
                         "examples": int(len(dates)), "data_through": str(dates.max())}
        g = summarize_wf(grp, wf)
        g["decision"] = {"event": event, "family": choice, "previous": prod, "reason": why}
        if grp == "G_start":
            g["calibration"] = calib(wf["preds"][choice], wf["actual"])
        else:
            g["intervals"] = intervals(wf["preds"][choice], wf["actual"], wf["fold_id"])
        g["seconds"] = round(time.time() - t0, 1)
        g["trained"] = E.iso(now)
        val["groups"][grp] = g
        reg.setdefault("history", []).append({"at": E.iso(now), "group": grp, "event": event,
                                              "family": choice, "previous": prod, "reason": why})
        reg.setdefault("runs", []).append({"at": E.iso(now), "group": grp, "live": choice,
                                           "live_loss": g["families"][choice]["loss"],
                                           "baseline_loss": g["families"]["baseline"]["loss"],
                                           "months_tested": len(wf["folds"])})
        log(f"(learn) {GROUP_NAMES[grp]}: {event.upper()} {choice} | {why} | {g['seconds']}s")
    reg["history"] = reg.get("history", [])[-300:]
    reg["runs"] = reg.get("runs", [])[-600:]
    reg["last_train"] = E.iso(now)
    reg["code"] = VERSION
    reg["env"] = {"python": platform.python_version(), "numpy": np.__version__, "sklearn": sklearn.__version__}
    val["version"] = VERSION
    val["trained"] = E.iso(now)
    E.write_json(H(root, "models", "registry.json"), reg)
    E.write_json(H(root, "models", "validation.json"), val)
    with open(H(root, "models", "validation.js"), "w", encoding="utf-8") as f:
        f.write("window.AI_VALIDATION = " + json.dumps(val, separators=(",", ":")) + ";\n")
    return val


def load_production(root, reg, log=print):
    out = {}
    for grp, info in (reg.get("production") or {}).items():
        try:
            with open(H(root, "models", info["file"]), "rb") as f:
                out[grp] = pickle.load(f)
        except Exception as ex:
            log(f"(learn) could not load {grp} model {info.get('file')}: {type(ex).__name__}: {ex}")
    return out


# ----------------------------------------------------------------- 6. PREDICT
def predict_upcoming(root, st, models, reg, val, espn, now, day_fetch, days=7, log=print):
    today = now.astimezone(E.ET).date()
    games = []
    for k in range(days):
        ds = (today + timedelta(days=k)).isoformat()
        try:
            games += [g for g in day_fetch(ds) if g.get("sched") not in E.DEAD_SCHED]
        except Exception as ex:
            log(f"(learn) schedule {ds} unavailable: {ex}")
    sched = {}
    for g in games:
        d = date.fromisoformat(g["date"])
        for t, o, h in ((g["home"], g["away"], 1), (g["away"], g["home"], 0)):
            sched.setdefault(t, []).append((g["date"], o, h))
            st.team_days.setdefault(t, set()).add(d)
    st.season = season_for(today)
    idx = {}
    for pid, (n, pos, t, last) in st.names.items():
        idx.setdefault((E.norm(n), pos), []).append((last, t or "", pid))

    def match(p):
        grp = p.get("p")
        c = idx.get((E.norm(p.get("n")), grp), [])
        if not c and grp in ("F", "D"):
            c = idx.get((E.norm(p.get("n")), "D" if grp == "F" else "F"), [])
        if not c:
            return None
        same = [x for x in c if x[1] == p.get("t")]
        return max(same or c)[2]

    out = {"asof": E.iso(now), "code": VERSION,
           "versions": {g: ((reg.get("production") or {}).get(g) or {}).get("version") for g in FAMILIES},
           "note": "skaters: expected fantasy points if he plays; goalies: points if he starts, plus start chance",
           "proj": {}, "gstart": {}, "range": {}, "detail": {}, "unmatched": []}
    players = [p for p in (espn or {}).get("players", []) if p.get("t") in sched]
    batch = {"F": [], "D": []}
    for p in players:
        if p.get("p") == "G":
            continue
        pid = match(p)
        if pid is None:
            out["unmatched"].append(p.get("n"))
        pos = "D" if p.get("p") == "D" else "F"
        tg = sorted(sched[p["t"]])
        pl_last = st.pl[pid]["last"] if pid in st.pl else None
        for i, (ds, opp, home) in enumerate(tg):
            cands = [d for d in (pl_last, date.fromisoformat(tg[i - 1][0]) if i else None) if d]
            batch[pos].append((st.skater_x(pid, pos, p["t"], opp, home, date.fromisoformat(ds),
                                           last=max(cands) if cands else None), str(p["id"]), ds))
    near = {(today + timedelta(days=k)).isoformat() for k in range(2)}
    for pos, items in batch.items():
        m = models.get(pos)
        if m is None or not items:
            continue
        pr = m.predict(np.array([x for x, _, _ in items]))
        iv = ((val.get("groups") or {}).get(pos) or {}).get("intervals")
        for i, (_, eid, ds) in enumerate(items):
            fp = float(pr["fp"][i])
            out["proj"].setdefault(eid, {})[ds] = round(fp, 2)
            if iv:
                b = int(np.searchsorted(iv["edges"], fp))
                out["range"].setdefault(eid, {})[ds] = [iv["q"][b][0], iv["q"][b][1]]
            if ds in near and all(k in pr for k in SK_STATS):
                out["detail"].setdefault(eid, {})[ds] = {k: round(float(pr[k][i]), 3) for k in SK_STATS}
    ms, mc = models.get("G_start"), models.get("G_cond")
    goalies = {}
    for p in players:
        if p.get("p") == "G" and not p.get("ir"):
            goalies.setdefault(p["t"], []).append(p)
    if ms is not None and mc is not None:
        for t, gl in goalies.items():
            ids = [match(p) for p in gl]
            for ds, opp, home in sorted(sched[t]):
                X = np.array([st.goalie_x(gid, t, opp, home, date.fromisoformat(ds), len(gl)) for gid in ids])
                ps = main_pred("G_start", ms, X, [(ds, t)] * len(gl))
                fc = mc.predict(X)["fp"]
                for p, sp, f in zip(gl, ps, fc):
                    eid = str(p["id"])
                    out["gstart"].setdefault(eid, {})[ds] = round(float(sp), 3)
                    out["proj"].setdefault(eid, {})[ds] = round(float(f), 2)
    E.write_json(H(root, "models", "ai_proj.json"), out)
    log(f"(learn) AI projections written: {len(out['proj'])} players, {len(games)} games in the next {days} days, "
        f"{len(out['unmatched'])} players without NHL history (league-average start)")
    return out


# ----------------------------------------------------------------- daily run
def daily(root=HERE, now=None, force=False, fetch=None, day_fetch=None, cfg=None, log=print, pause=0.2):
    now = now or datetime.now(E.UTC)
    cfg = cfg or CFG
    today = now.astimezone(E.ET).date()
    errs = []
    status = {"run": E.iso(now), "code": VERSION, "trained": False}
    try:
        status["weekly_files_refreshed"] = update_history(root, today, fetch or fetch_range, log, pause)
    except Exception as ex:
        errs.append(f"history: {type(ex).__name__}: {ex}")
    rows = load_history(root)
    status["history_rows"] = len(rows)
    if not rows:
        errs.append("history: no games downloaded yet")
    else:
        t0 = time.time()
        st, SX, GS, GC = build_dataset(rows)
        data = datasets(SX, GS, GC)
        log(f"(learn) replayed {len(rows)} player-games in {time.time() - t0:.0f}s -> "
            f"{len(SX.meta)} skater, {len(GS.meta)} goalie-start and {len(GC.meta)} goalie-game examples")
        reg = E.read_json(H(root, "models", "registry.json"), {})
        due = (force or reg.get("feature_hash") != FEATURE_HASH or not reg.get("production")
               or (now.weekday() == 0 and not str(reg.get("last_train", "")).startswith(E.iso(now)[:10])))
        if due:
            try:
                train(root, reg, data, now, cfg, log)
                status["trained"] = True
            except Exception as ex:
                errs.append(f"training: {type(ex).__name__}: {ex}")
                log(traceback.format_exc())
        else:
            log("(learn) not a retraining day (Mondays) - using the current models")
        try:
            models = load_production(root, reg, log)
            if models:
                predict_upcoming(root, st, models, reg, E.read_json(H(root, "models", "validation.json"), {}),
                                 E.load_espn_data(root), now, day_fetch or E.fetch_day, log=log)
            else:
                log("(learn) no live models yet - projections skipped")
        except Exception as ex:
            errs.append(f"predict: {type(ex).__name__}: {ex}")
            log(traceback.format_exc())
    status["errors"] = errs
    E.write_json(H(root, "models", "status.json"), status)
    for e in errs:
        log(f"(learn) WARNING {e}")
    return errs


# ----------------------------------------------------------------- tests
def _pois(rng, lam):
    L, k, p = math.exp(-lam), 0, 1.0
    while True:
        p *= rng.random()
        if p <= L:
            return k
        k += 1


def synth(seed=1, ndays=90):
    """Fake but realistic-shaped league: 6 teams, 3 seasons, known player skill levels."""
    rng = random.Random(seed)
    teams = ["AAA", "BBB", "CCC", "DDD", "EEE", "FFF"]
    rosters, pid = {}, 1000
    for t in teams:
        sk = []
        for j in range(12):
            sk.append({"p": pid, "n": f"{t} Skater{j}", "pos": "D" if j >= 8 else "F", "skill": rng.uniform(0.5, 1.6)})
            pid += 1
        rosters[t] = (sk, [{"p": pid, "n": f"{t} GoalieA"}, {"p": pid + 1, "n": f"{t} GoalieB"}])
        pid += 2
    strength = {t: rng.uniform(0.8, 1.2) for t in teams}
    rows, gid = [], 1
    for start in ("2024-10-05", "2025-10-05", "2026-10-01"):
        d0 = date.fromisoformat(start)
        for k in range(0, ndays, 2):
            day = (d0 + timedelta(days=k)).isoformat()
            order = teams[:]
            rng.shuffle(order)
            for i in range(0, len(order), 2):
                h, a = order[i], order[i + 1]
                tot = {}
                for t, o, home in ((h, a, 1), (a, h, 0)):
                    tg = tsog = 0
                    for pl in rosters[t][0]:
                        mult = strength[t] / strength[o]
                        sog = _pois(rng, (2.2 if pl["pos"] == "F" else 1.3) * pl["skill"] * mult)
                        g = sum(1 for _ in range(sog) if rng.random() < 0.1)
                        ast = _pois(rng, 0.25 * pl["skill"] * mult)
                        rows.append({"g": gid, "d": day, "p": pl["p"], "n": pl["n"], "t": t, "o": o, "h": home,
                                     "pos": pl["pos"], "G": g, "A": ast, "PM": rng.choice([-1, 0, 0, 1]),
                                     "PPP": sum(1 for _ in range(g + ast) if rng.random() < 0.3), "SHP": 0,
                                     "SOG": sog, "HIT": _pois(rng, 1.0),
                                     "BLK": _pois(rng, 1.5 if pl["pos"] == "D" else 0.5),
                                     "toi": int(900 * pl["skill"]), "pptoi": int(60 * pl["skill"])})
                        tg += g
                        tsog += sog
                    tot[t] = (tg, tsog)
                ot = tot[h][0] == tot[a][0]
                win = rng.choice([h, a]) if ot else (h if tot[h][0] > tot[a][0] else a)
                for t, o in ((h, a), (a, h)):
                    gk = rosters[t][1][0] if rng.random() < 0.75 else rosters[t][1][1]
                    ga, sa = tot[o]
                    rows.append({"g": gid, "d": day, "p": gk["p"], "n": gk["n"], "t": t, "o": o,
                                 "h": 1 if t == h else 0, "pos": "G", "GS": 1, "W": int(win == t),
                                 "OTL": int(ot and win != t), "GA": ga, "SV": sa - ga, "SA": sa,
                                 "SO": int(ga == 0), "toi": 3600})
                gid += 1
    return rows


def selftest():
    import warnings
    warnings.filterwarnings("ignore")
    os.environ["GITHUB_ACTIONS"] = "true"
    results = []

    def check(name, cond):
        results.append(bool(cond))
        print(("PASS  " if cond else "FAIL  ") + name)

    tmp = tempfile.mkdtemp()
    try:
        rows = synth()
        for r in rows:
            r["season"] = season_for(date.fromisoformat(r["d"]))
        st, SX, GS, GC = build_dataset([dict(r) for r in rows])
        check("feature counts match the model inputs",
              SX.arrays()[0].shape[1] == len(SK_FEATS) and GS.arrays()[0].shape[1] == len(GO_FEATS))
        check("training examples built for skaters, goalie starts and goalie games",
              len(SX.meta) > 5000 and len(GC.meta) > 300 and len(GS.meta) > len(GC.meta))

        cut = sorted({r["d"] for r in rows})[len({r["d"] for r in rows}) // 2]
        rows2 = [dict(r) for r in rows]
        for r in rows2:
            if r["d"] == cut:
                for k in ("G", "A", "SOG", "HIT", "BLK", "GA", "SV", "SA", "GS"):
                    if k in r and k != "GS":
                        r[k] = (r[k] or 0) * 5 + 3
        _, SX2, GS2, _ = build_dataset(rows2)
        d1 = np.array([m[0] for m in SX.meta])
        up = d1 <= cut
        X1, X2 = SX.arrays()[0], SX2.arrays()[0]
        check("NO FUTURE LEAKAGE: changing one day's results leaves all inputs up to that day identical",
              np.array_equal(X1[up], X2[up]))
        check("...and inputs after that day do change (so the leak test is real)", not np.array_equal(X1[~up], X2[~up]))
        g1 = np.array([m[0] for m in GS.meta]) <= cut
        check("NO FUTURE LEAKAGE for goalie-start inputs", np.array_equal(GS.arrays()[0][g1], GS2.arrays()[0][g1]))

        rng = np.random.default_rng(0)
        base = np.abs(rng.normal(0, 5, 3000))
        recent = np.zeros(3000, dtype=bool)
        recent[-500:] = True
        c, ev, _ = decide({"baseline": base, "good": base - 0.4}, None, CFG, recent)
        check("a clearly better model is promoted", c == "good" and ev == "promote")
        c, ev, _ = decide({"baseline": base, "noise": base + rng.normal(0, 0.05, 3000)}, None, CFG, recent)
        check("a model that is not clearly better is NOT promoted", c == "baseline")
        c, ev, _ = decide({"baseline": base, "bad": base + 0.4}, "bad", CFG, recent)
        check("a live model that falls behind the baseline is rolled back", c == "baseline" and ev == "rollback")
        c, ev, _ = decide({"baseline": base, "good": base - 0.4, "good2": base - 0.41}, "good", CFG, recent)
        check("a tiny improvement does not replace the live model", c == "good" and ev == "keep")
        late = base - 0.4
        late[recent] += 1.0
        c, ev, _ = decide({"baseline": base, "fading": late}, None, CFG, recent)
        check("a model that is worse in the most recent month is not promoted", c == "baseline")

        X, Y, _, _ = datasets(SX, GS, GC)["F"]
        a = SkGBMStats().fit(X[:2000], Y[:2000]).predict(X[:50])["fp"]
        b = SkGBMStats().fit(X[:2000], Y[:2000]).predict(X[:50])["fp"]
        check("training is reproducible (same data -> same model)", np.allclose(a, b))

        def fake_fetch(s, e):
            return [{k: v for k, v in r.items() if k != "season"} for r in rows if s <= r["d"] <= e]

        eplayers, eid = [], 1
        for pid, n, t, pos in sorted({(r["p"], r["n"], r["t"], r["pos"]) for r in rows if r["t"] in ("AAA", "BBB")}):
            eplayers.append({"id": eid, "n": n, "t": t, "p": pos, "ft": 0})
            eid += 1
        eplayers.append({"id": 999, "n": "Rookie Newguy", "t": "AAA", "p": "F", "ft": 0})
        with open(os.path.join(tmp, "espn-data.js"), "w", encoding="utf-8") as f:
            f.write("window.ESPN_DATA = " + json.dumps({"generated": "2027-01-05T12:00:00", "players": eplayers}) + ";\n")

        def fake_day(ds):
            if ds != "2027-01-06":
                return []
            return [{"gid": 5000, "date": ds, "start": ds + "T23:00:00Z", "state": "FUT", "sched": "OK",
                     "home": "AAA", "away": "BBB"}]

        tcfg = dict(CFG, folds=2, min_test=50, min_train=300)
        now = datetime(2027, 1, 5, 12, 0, tzinfo=E.UTC)
        errs = daily(tmp, now, fetch=fake_fetch, day_fetch=fake_day, cfg=tcfg, pause=0)
        check("full daily run (download -> replay -> train -> validate -> predict) has no errors", errs == [])
        reg = E.read_json(H(tmp, "models", "registry.json"), {})
        check("a live model chosen for forwards, defense, goalie starts and goalie scoring",
              set(reg.get("production", {})) == set(FAMILIES))
        ok = True
        for grp, info in reg.get("production", {}).items():
            with open(H(tmp, "models", info["file"]), "rb") as f:
                ok = ok and type(pickle.load(f)).__module__ == "ai_learn"
        check("saved models reload correctly", ok)
        val = E.read_json(H(tmp, "models", "validation.json"), {})
        check("walk-forward validation ran on months the models never saw",
              len(val.get("groups", {}).get("F", {}).get("folds", [])) >= 1)
        proj = E.read_json(H(tmp, "models", "ai_proj.json"), {})
        fwd = next(p for p in eplayers if p["t"] == "AAA" and p["p"] == "F")
        v = proj.get("proj", {}).get(str(fwd["id"]), {}).get("2027-01-06")
        check("AI projection written for a forward (keyed by ESPN id)", isinstance(v, (int, float)) and 0 < v < 40)
        gks = [p for p in eplayers if p["t"] == "AAA" and p["p"] == "G"]
        s = sum(proj.get("gstart", {}).get(str(p["id"]), {}).get("2027-01-06", 0) for p in gks)
        check("goalie start chances for one team add up to 100%", abs(s - 1) < 0.01)
        check("a player with no NHL history still gets a cautious projection",
              "999" in proj.get("proj", {}) and "Rookie Newguy" in proj.get("unmatched", []))
        last = reg.get("last_train")
        daily(tmp, now + timedelta(days=1), fetch=fake_fetch, day_fetch=fake_day, cfg=tcfg, pause=0)
        reg2 = E.read_json(H(tmp, "models", "registry.json"), {})
        check("no retraining on a non-Monday once models exist", reg2.get("last_train") == last)
    except Exception:
        traceback.print_exc()
        results.append(False)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    ok = all(results)
    print(f"\n{sum(results)}/{len(results)} checks passed" + ("" if ok else "  <-- SOMETHING FAILED"))
    return 0 if ok else 1


def livetest():
    results = []

    def check(name, cond):
        results.append(bool(cond))
        print(("PASS  " if cond else "FAIL  ") + name)

    rows = fetch_range("2026-04-06", "2026-04-12")
    sk = [r for r in rows if r["pos"] != "G"]
    go = [r for r in rows if r["pos"] == "G"]
    games = {r["g"] for r in rows}
    print(f"INFO  week of 2026-04-06: {len(games)} games, {len(sk)} skater rows, {len(go)} goalie rows")
    check("a week of past games downloads", len(games) >= 20 and len(sk) > 30 * len(games))
    check("hits and blocks merged", sum(r["HIT"] for r in sk) > 0 and sum(r["BLK"] for r in sk) > 0)
    check("power-play points present", sum(r["PPP"] for r in sk) > 0)
    check("two starting goalies per game", sum(r["GS"] for r in go) == 2 * len(games))
    check("every game has exactly two teams", all(len({r["t"] for r in rows if r["g"] == g}) == 2 for g in games))
    for field, label in (("o", "opponent"), ("h", "home/away"), ("toi", "ice time"), ("pptoi", "power-play ice time")):
        share = sum(1 for r in sk if r.get(field) is not None) / max(1, len(sk))
        print(("PASS  " if share > 0.95 else "WARN  ") + f"{label} available for {share:.0%} of rows"
              + ("" if share > 0.95 else " (the engine falls back safely, but tell Claude)"))
    ex = sk[0] if sk else {}
    print(f"INFO  example row: {ex}")
    ok = all(results)
    print(f"\n{sum(results)}/{len(results)} live checks passed" + ("" if ok else "  <-- SOMETHING FAILED"))
    return 0 if ok else 1


def main(argv):
    if "--selftest" in argv:
        return selftest()
    if "--livetest" in argv:
        return livetest()
    if "--daily" in argv:
        return 1 if daily(force="--train" in argv) else 0
    print(__doc__)
    return 0


if __name__ == "__main__":
    import ai_learn  # run from the module so saved models reload as ai_learn.* classes
    sys.exit(ai_learn.main(sys.argv[1:]))
