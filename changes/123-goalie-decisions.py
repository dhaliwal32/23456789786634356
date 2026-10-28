# changes/123-goalie-decisions.py - goalie games now show W, L or OTL even when the NHL left the decision blank: the goalie who played most of the game gets it (win, overtime loss if the game went past 60 minutes, otherwise loss); fixes the saved game history, future syncs, and the app

import glob
import json as _json123

SYNC_FN = r'''    # change 123: when the NHL leaves a goalie's decision blank, the goalie who played most of the game gets it
    def _mins123(s):
        try:
            a, b = str(s or "0:0").split(":")[:2]
            return int(a) + int(b) / 60
        except Exception:
            return 0

    def _fill_dec123(P):
        by = {}
        for x in P.values():
            if "sv" in x:
                by.setdefault((x.get("t"), x.get("o")), []).append(x)
        for gl in by.values():
            if any(x.get("dec") for x in gl):
                continue
            x = max(gl, key=lambda y: _mins123(y.get("toi")))
            my, op = x.get("my"), x.get("op")
            if my is None or op is None or my == op or _mins123(x.get("toi")) < 30:
                continue
            x["dec"] = "W" if my > op else ("O" if sum(_mins123(y.get("toi")) for y in gl) > 60.02 else "L")

    # 3e) box-score history for the player pop-up'''


def _mins(s):
    try:
        a, b = str(s or "0:0").split(":")[:2]
        return int(a) + int(b) / 60
    except Exception:
        return 0


def fix_box(t):
    try:
        d = _json123.loads(t)
    except Exception:
        return t
    P = d.get("p") or {}
    by, n = {}, 0
    for x in P.values():
        if isinstance(x, dict) and "sv" in x:
            by.setdefault((x.get("t"), x.get("o")), []).append(x)
    for gl in by.values():
        if any(x.get("dec") for x in gl):
            continue
        x = max(gl, key=lambda y: _mins(y.get("toi")))
        my, op = x.get("my"), x.get("op")
        if my is None or op is None or my == op or _mins(x.get("toi")) < 30:
            continue
        x["dec"] = "W" if my > op else ("O" if sum(_mins(y.get("toi")) for y in gl) > 60.02 else "L")
        n += 1
    return _json123.dumps(d, separators=(",", ":")) if n else t


APP_FN = r'''// ---------- change 123: fill a blank goalie decision (most minutes gets it) (install.py) ----------
const gxMins123 = (s) => { const m = String(s || "0:0").split(":"); return (+m[0] || 0) + (+m[1] || 0) / 60; };
function gxFillDec123(P) {
  if (!P) return P;
  const by = {};
  Object.values(P).forEach((x) => { if (x && x.sv != null) (by[x.t + "|" + x.o] = by[x.t + "|" + x.o] || []).push(x); });
  Object.values(by).forEach((gl) => {
    if (gl.some((x) => x.dec)) return;
    const x = gl.reduce((a, b) => (gxMins123(b.toi) > gxMins123(a.toi) ? b : a));
    if (x.my == null || x.op == null || x.my === x.op || gxMins123(x.toi) < 30) return;
    x.dec = x.my > x.op ? "W" : gl.reduce((s, y) => s + gxMins123(y.toi), 0) > 60.02 ? "O" : "L";
  });
  return P;
}
// a single day's line from the sync (no score saved with it): use the final score of his team's game
function gxDecP123(p, dt, x) {
  if (!x || x.sv == null || x.dec || !p || !dt || gxMins123(x.toi) < 50) return x;
  if (gState(p.t, dt).s !== "F") return x;
  const g = gScore(p.t, dt);
  if (!g || g.my == null || g.op == null || g.my === g.op) return x;
  return { ...x, dec: g.my > g.op ? "W" : gxMins123(x.toi) > 60.02 ? "O" : "L" };
}
'''


def change_sync(t):
    t = lit(t, "123: goalie decision helper", "    # 3e) box-score history for the player pop-up", SYNC_FN, "change 123: when the NHL leaves")
    w = '                with open(os.path.join(bdir31_, dd31_ + ".json"), "w", encoding="utf-8") as f31_:'
    t = lit(t, "123: fill decisions before saving", w, "                _fill_dec123(out31_)\n" + w, "_fill_dec123(out31_)\n")
    return t


def change(t):
    t = lit(t, "123: helpers", ROOT, APP_FN + ROOT, "change 123: fill a blank goalie decision")
    t = lit(t, "123: saved history",
            'return fetch("box/" + d + ".json").then((r) => (r.ok ? r.json() : null)).then((j) => { if (j && j.p) B.days[d] = j.p; return (j && j.p) || null; }).catch(() => null);',
            'return fetch("box/" + d + ".json").then((r) => (r.ok ? r.json() : null)).then((j) => { if (j && j.p) B.days[d] = gxFillDec123(j.p); return (j && j.p) || null; }).catch(() => null);',
            "B.days[d] = gxFillDec123(j.p)")
    t = lit(t, "123: day lines", "return L || E0; /* gx120 */", "return L || gxDecP123(p, dt, E0); /* gx120 */", "gxDecP123(p, dt, E0)")
    return t


edit("espn_sync.py", change_sync)
edit(APP, change)
for _f in sorted(glob.glob("box/20*.json")):
    edit(_f, fix_box)
