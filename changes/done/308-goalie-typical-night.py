# changes/308-goalie-typical-night.py - new choice for the AI's goalie points: aims at a goalie's typical night (team strength, home, back-to-backs) instead of the average one; the AI only switches to it if it clearly wins its fair test

OLD = '''FAMILIES = {
    "F": {"baseline": SkBaseline, "ridge_fp": SkRidgeFP, "poisson_stats": SkPoissonStats,
          "gbm_fp": SkGBMFP, "gbm_stats": SkGBMStats},
    "D": {"baseline": SkBaseline, "ridge_fp": SkRidgeFP, "poisson_stats": SkPoissonStats,
          "gbm_fp": SkGBMFP, "gbm_stats": SkGBMStats},
    "G_start": {"baseline": StBaseline, "logit": StLogit, "gbm": StGBM},
    "G_cond": {"baseline": GcBaseline, "gbm_stats": GcGBM},
}'''

NEW = '''# change 308: goalie nights are all or nothing (a win is worth 5), so the smallest average miss comes from
# aiming at the typical night, not the average one. A small median (quantile) model on the baseline's own
# number plus team strength. Walk-forward test on Nov 16 2026: 6.646 vs baseline 6.680 (-0.5%, 2.5 SE).
GC308_FEATS = ["own_gf", "opp_ga", "opp_gf", "own_sa", "opp_sf", "home", "b2b", "opp_b2b", "sv", "sv_n"]


class GcMedLin:
    def _z(self, X, b):
        return np.column_stack([X[:, [GIDX[k] for k in GC308_FEATS]], b])

    def fit(self, X, Y):
        from sklearn.linear_model import QuantileRegressor
        self.base = GcBaseline().fit(X, Y)
        self.m = _scaled(QuantileRegressor(quantile=0.5, alpha=0.01, solver="highs")).fit(
            self._z(X, self.base.predict(X)["fp"]), Y[:, -1])
        return self

    def predict(self, X):
        out = self.base.predict(X)
        out["fp"] = self.m.predict(self._z(X, out["fp"]))
        return out


FAMILIES = {
    "F": {"baseline": SkBaseline, "ridge_fp": SkRidgeFP, "poisson_stats": SkPoissonStats,
          "gbm_fp": SkGBMFP, "gbm_stats": SkGBMStats},
    "D": {"baseline": SkBaseline, "ridge_fp": SkRidgeFP, "poisson_stats": SkPoissonStats,
          "gbm_fp": SkGBMFP, "gbm_stats": SkGBMStats},
    "G_start": {"baseline": StBaseline, "logit": StLogit, "gbm": StGBM},
    "G_cond": {"baseline": GcBaseline, "gbm_stats": GcGBM, "median_lin": GcMedLin},  # change 308
}'''


def go(t):
    t = lit(t, "308: goalie typical-night model", OLD, NEW, "change 308: goalie nights")
    py_ok("ai_learn.py", t)
    return t


edit("ai_learn.py", go)
