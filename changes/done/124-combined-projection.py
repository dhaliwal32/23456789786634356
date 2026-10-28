# changes/124-combined-projection.py - one Combined projection everywhere instead of choosing ESPN / GM model / Blend / AI / Best. gm_combo.py re-tests every model and mix every night on every graded game (walk-forward, no peeking) and uses whatever has the smallest average miss per game, separately for forwards, defence and goalies; missing numbers fall back AI -> GM -> ESPN; goalie start chance uses confirmations first, then the AI. ai_engine.py now records and grades the Combined number too. The projection choices are gone; the AI Lab still shows how each model does

GM_COMBO = r'''"""
gm_combo.py - the Combined projection: one number per player per game, built from ESPN, the GM model and the AI.

Every night it re-tests every way of combining them on all graded games so far (ai/joined), using only
games from before each test day (walk-forward, no peeking), and keeps whatever has the smallest average
miss per game (the same measure the AI Lab uses), separately for forwards, defence and goalies:
  - "ai", "gm", "espn": one model alone
  - "half": AI and GM model averaged
  - "mix":  learned weights for ESPN, GM and AI (weights add up to 1, no correction, so it stays fair)
The mix has to beat the best of the others by more than 1 standard error, so it can't win by luck.
When a player has no number from the chosen model, the app falls back AI -> GM -> ESPN.
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
          "data": {"from": d0, "to": d1, "records": len(recs)}, "groups": groups}
    with open(os.path.join(root, "ai", "combo.json"), "w", encoding="utf-8") as fh:
        json.dump(js, fh, indent=1)
    for G, x in groups.items():
        t = x["tests"]
        line = ", ".join(f"{k} {v['mae']}" for k, v in t.items())
        print(f"(combo) {G}: using {x['pick']} {x['w']} bias {x['bias']} - {x['why']} | test MAE: {line}")


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
'''

COMBO_JSON = r'''{
 "version": "combo-v1",
 "asof": "2026-10-28T09:52:40Z",
 "data": {
  "from": "2026-09-29",
  "to": "2026-10-27",
  "records": 14686
 },
 "groups": {
  "F": {
   "pick": "ai",
   "why": "smallest average miss per game (4.597 pts)",
   "w": {
    "espn": 0.0,
    "gm": 0.0,
    "ai": 1.0
   },
   "bias": 0.0,
   "games": 4652,
   "tests": {
    "half": {
     "n": 3730,
     "mae": 4.606,
     "rmse": 6.058,
     "bias": -0.073
    },
    "ai": {
     "n": 3730,
     "mae": 4.597,
     "rmse": 6.057,
     "bias": -0.071
    },
    "gm": {
     "n": 3730,
     "mae": 4.627,
     "rmse": 6.081,
     "bias": -0.075
    },
    "espn": {
     "n": 3730,
     "mae": 4.831,
     "rmse": 6.3,
     "bias": 0.125
    },
    "mix": {
     "n": 3730,
     "mae": 4.602,
     "rmse": 6.055,
     "bias": -0.069
    }
   }
  },
  "D": {
   "pick": "ai",
   "why": "smallest average miss per game (3.592 pts)",
   "w": {
    "espn": 0.0,
    "gm": 0.0,
    "ai": 1.0
   },
   "bias": 0.0,
   "games": 2390,
   "tests": {
    "half": {
     "n": 1925,
     "mae": 3.616,
     "rmse": 4.816,
     "bias": 0.032
    },
    "ai": {
     "n": 1925,
     "mae": 3.592,
     "rmse": 4.808,
     "bias": 0.014
    },
    "gm": {
     "n": 1925,
     "mae": 3.661,
     "rmse": 4.854,
     "bias": 0.05
    },
    "espn": {
     "n": 1925,
     "mae": 3.918,
     "rmse": 5.131,
     "bias": 0.14
    },
    "mix": {
     "n": 1925,
     "mae": 3.592,
     "rmse": 4.808,
     "bias": 0.015
    }
   }
  },
  "G": {
   "pick": "half",
   "why": "only 291 test games so far - using the AI+GM average",
   "w": {
    "espn": 0.0,
    "gm": 0.5,
    "ai": 0.5
   },
   "bias": 0.0,
   "games": 394,
   "tests": {
    "half": {
     "n": 291,
     "mae": 6.547,
     "rmse": 8.231,
     "bias": 0.278
    },
    "ai": {
     "n": 291,
     "mae": 6.545,
     "rmse": 8.238,
     "bias": 0.402
    },
    "gm": {
     "n": 291,
     "mae": 6.581,
     "rmse": 8.252,
     "bias": 0.154
    },
    "espn": {
     "n": 291,
     "mae": 6.974,
     "rmse": 8.682,
     "bias": 0.312
    },
    "mix": {
     "n": 291,
     "mae": 6.57,
     "rmse": 8.242,
     "bias": 0.171
    }
   }
  }
 }
}'''

APP_FN = r'''// ---------- change 124: the Combined projection (install.py) ----------
// weights come from ai/combo.json (re-learned every night by gm_combo.py); missing numbers fall back AI -> GM -> ESPN
function gxCombo124(p, K, dt) {
  const e = effAvg0(p, K), id = typeof p.id === "string" && p.id[0] === "e" ? p.id.slice(1) : null;
  let g = null, a = null;
  if (id) {
    const M = window.__MODEL;
    if (M) { const pr = (M.proj || {})[id], mv = dt && pr && pr[dt] != null ? pr[dt] : (M.base || {})[id]; if (mv != null) g = mv; }
    const A = window.__AI;
    if (A) { const ap = (A.proj || {})[id], av = ap ? (dt && ap[dt] != null ? ap[dt] : (window.__AIAVG || {})[id]) : null; if (av != null) a = av; }
  }
  const grp = p.p === "G" ? "G" : p.p === "D" ? "D" : "F", C = (((window.__COMBO || {}).groups) || {})[grp] || {};
  const W = C.w || { espn: 0, gm: 0.5, ai: 0.5 };
  let s = 0, t = 0;
  if (a != null && W.ai) { s += W.ai * a; t += W.ai; }
  if (g != null && W.gm) { s += W.gm * g; t += W.gm; }
  if (W.espn) { s += W.espn * e; t += W.espn; }
  const v = t > 1e-9 ? s / t + (C.bias || 0) : a != null ? a : g != null ? g : e;
  return Math.max(0, v) * (p.gwMul || 1);
}
'''

ENGINE_COMBO = r'''

def combo_of(espn, gm, aiv, pos, C):
    """change 124: the app's Combined projection (ai/combo.json weights; falls back AI -> GM -> ESPN)"""
    g = ((C or {}).get("groups") or {}).get("G" if pos == "G" else "D" if pos == "D" else "F") or {}
    W = g.get("w") or {"espn": 0.0, "gm": 0.5, "ai": 0.5}
    s = t = 0.0
    for k, v in (("ai", aiv), ("gm", gm), ("espn", espn)):
        if v is not None and W.get(k):
            s += W[k] * v
            t += W[k]
    if t <= 1e-9:
        v = aiv if aiv is not None else gm if gm is not None else espn
        return None if v is None else round(v, 3)
    return round(max(0.0, s / t + (g.get("bias") or 0.0)), 3)
'''

CSS = r'''  /* change 124 (install.py) */
  .gx-pmh82, .gx-ep124 { display: none !important; }
</style>'''


def change_engine(t):
    t = lit(t, "124: Combined in the model list", 'MODELS = ("espn", "gm", "blend", "ai")', 'MODELS = ("espn", "gm", "blend", "ai", "combo")', 'MODELS = ("espn", "gm", "blend", "ai", "combo")')
    t = lit(t, "124: combo formula", "\n\ndef blend_of(espn, gm, base):", ENGINE_COMBO + "\n\ndef blend_of(espn, gm, base):", "def combo_of(espn, gm, aiv, pos, C):")
    t = lit(t, "124: read combo weights", "    ai_ver = ai.get(\"versions\") or {}\n",
            "    ai_ver = ai.get(\"versions\") or {}\n    combo_w = read_json(P(root, \"combo.json\"), {})  # change 124\n", "combo_w = read_json(P(root, \"combo.json\"), {})")
    t = lit(t, "124: record the Combined number",
            '"pred": {"espn": espn, "gm": gm, "blend": blend_of(espn, gm, base.get(pid)), "ai": aiv},',
            '"pred": {"espn": espn, "gm": gm, "blend": blend_of(espn, gm, base.get(pid)), "ai": aiv,\n                            "combo": combo_of(espn, gm if gm is not None else base.get(pid), aiv, p.get("p"), combo_w)},',
            '"combo": combo_of(espn, gm if gm is not None else base.get(pid)')
    t = lit(t, "124: keep it when grading",
            '"espn": pr.get("espn"), "gm": pr.get("gm"), "blend": pr.get("blend"), "ai": pr.get("ai"),',
            '"espn": pr.get("espn"), "gm": pr.get("gm"), "blend": pr.get("blend"), "ai": pr.get("ai"), "combo": pr.get("combo"),',
            '"ai": pr.get("ai"), "combo": pr.get("combo"),')
    t = lit(t, "124: player history",
            '"ai", "ai_lo", "ai_hi", "start_p", "ai_start_p", "played", "fp")})',
            '"ai", "combo", "ai_lo", "ai_hi", "start_p", "ai_start_p", "played", "fp")})',
            '"ai", "combo", "ai_lo"')
    t = lit(t, "124: compare it with the others",
            '                       for a, b in (("gm", "espn"), ("blend", "espn"), ("blend", "gm"),',
            '                       for a, b in (("combo", "ai"), ("combo", "gm"), ("combo", "espn"), ("gm", "espn"), ("blend", "espn"), ("blend", "gm"),',
            '(("combo", "ai"), ("combo", "gm"), ("combo", "espn"),')
    return t


def change_lab(t):
    t = lit(t, "124: AI Lab models", 'const M = ["espn", "gm", "blend", "ai"];', 'const M = ["espn", "gm", "blend", "ai", "combo"];', '"ai", "combo"];')
    t = lit(t, "124: AI Lab names", 'const NAME = {espn: "ESPN", gm: "GM model", blend: "Blend", ai: "AI"};', 'const NAME = {espn: "ESPN", gm: "GM model", blend: "Blend", ai: "AI", combo: "Combined (app)"};', 'combo: "Combined (app)"')
    t = lit(t, "124: AI Lab colours", 'const COL = {espn: "#f87171", gm: "#60a5fa", blend: "#a78bfa", ai: "#34d399"};', 'const COL = {espn: "#f87171", gm: "#60a5fa", blend: "#a78bfa", ai: "#34d399", combo: "#fbbf24"};', 'combo: "#fbbf24"')
    return t


def change(t):
    t = lit(t, "124: styles", "</style>", CSS, "change 124 (install.py)")
    t = lit(t, "124: helpers", ROOT, APP_FN + ROOT, "change 124: the Combined projection")
    t = lit(t, "124: Combined for every number", "const effAvg = (p, K, dt) => {\n  const base = effAvg0(p, K);",
            "const effAvg = (p, K, dt) => {\n  if ((window.__PMODE || \"combo\") === \"combo\") return gxCombo124(p, K, dt); /* gx124 */\n  const base = effAvg0(p, K);",
            "return gxCombo124(p, K, dt); /* gx124 */")
    t = lit(t, "124: always Combined", 'window.__PMODE = window.__MODEL ? s.pmode || "blend" : "espn";', 'window.__PMODE = "combo"; /* gx124 */', 'window.__PMODE = "combo"; /* gx124 */')
    t = lit(t, "124: AI goalie start chance", 'const aiG = window.__PMODE === "ai" && dt &&', 'const aiG = (window.__PMODE === "ai" || window.__PMODE === "combo") && dt &&', '(window.__PMODE === "ai" || window.__PMODE === "combo") && dt &&')
    t = lit(t, "124: load the weights", '  useEffect(() => { fetch("ai/models/ai_proj.json?t=" + Date.now())',
            '  useEffect(() => { fetch("ai/combo.json?t=" + Date.now()).then((r) => (r.ok ? r.json() : null)).then((C) => { if (C && C.groups) { window.__COMBO = C; setS((st) => ({ ...st, players: [...st.players] })); } }).catch(() => {}); }, []); /* gx124 */\n  useEffect(() => { fetch("ai/models/ai_proj.json?t=" + Date.now())',
            '  useEffect(() => { fetch("ai/combo.json?t="')
    # no more choosing
    t = lit(t, "124: phone menu choices", "{M_MODES.map(([k, l]) =>", "{[].map(([k, l]) =>", "{[].map(([k, l]) =>")
    t = lit(t, "124: phone menu label", '<div className="text-xs text-slate-500 mb-1">Projections</div>', '<div className="text-xs text-slate-500 mb-1">Projections: Combined</div>', "Projections: Combined</div>")
    t = lit(t, "124: setup label", 'const projTxt = s.pbest ? "Best projection (" + (PM[window.__PMODE] || "ESPN") + ")" : (PM[window.__PMODE] || "ESPN") + " projections";',
            'const projTxt = "Combined projection";', 'const projTxt = "Combined projection";')
    i = t.find('    <div className="gx-sr"><span>Projections</span>{seg([["best"')
    if i >= 0:
        j = t.find("\n", i)
        t = t[:i] + '    <div className="gx-sr"><span>Projections</span><span className="text-sm">Combined</span></div>' + t[j:]
        print("(install) 124: setup choice removed: updated")
    elif '<span>Projections</span><span className="text-sm">Combined</span>' not in t:
        fail("124: setup projection row not found")
    t = lit(t, "124: setup note", "Best switches each day to whichever projection has been most accurate in the AI Lab.",
            "One projection built from ESPN, the GM model and the AI, re-tested every night on every game played. The AI Lab shows how each one is doing.",
            "One projection built from ESPN, the GM model and the AI")
    t = lit(t, "124: Best switching off", "    if (!s.pbest) return;\n    let dead = false;\n    const MAP = { espn:", "    if (true) return; /* gx124: Combined replaces Best */\n    let dead = false;\n    const MAP = { espn:", "if (true) return; /* gx124")
    t = lit(t, "124: no side by side projections", "const gxCanMode82 = (k) => k === \"espn\" || (!!window.__MODEL && (k !== \"ai\" || !!window.__AI));",
            "const gxCanMode82 = (k) => false; /* gx124: one Combined projection */", "const gxCanMode82 = (k) => false; /* gx124")
    n = t.count('      <div style={{ marginTop: 12 }}>\n        <div className="gx-tag" style={{ marginBottom: 4 }}>Every projection</div>')
    if n:
        t = t.replace('      <div style={{ marginTop: 12 }}>\n        <div className="gx-tag" style={{ marginBottom: 4 }}>Every projection</div>', '      <div style={{ marginTop: 12 }} className="gx-ep124">\n        <div className="gx-tag" style={{ marginBottom: 4 }}>Every projection</div>')
        print("(install) 124: every-projection tables hidden (%d): updated" % n)
    return t


new_file("gm_combo.py", GM_COMBO)
new_file("ai/combo.json", COMBO_JSON)
edit("ai_engine.py", change_engine)
edit("ai-dashboard.html", change_lab)
edit(APP, change)
