# changes/178-box-ppp-shp.py - Matchup score pop-up: Power Play Points (+2) and Shorthanded Points (+3) get their own rows instead of "Other"

OLD = r'''    let left = real != null ? real - est : (x.ppg || 0) * (sc.PPP || 0), ppp = x.ppg || 0;
    if (real != null && sc.PPP) { const k = Math.round(left / sc.PPP); if (k > 0 && Math.abs(left - k * sc.PPP) < 0.05) { ppp = k; } }
    if (ppp && sc.PPP) { add("Power Play Points", sc.PPP, ppp); est += ppp * sc.PPP; left = real != null ? real - est : 0; }'''

NEW = r'''    // change 178: power play and shorthanded points both counted; ESPN's total decides the split when it is known
    const wP = +sc.PPP || 0, wS = +sc.SHP || 0;
    const p0 = x.ppp != null ? x.ppp : x.ppg || 0, s0 = x.shp != null ? x.shp : x.shg || 0;
    let ppp = p0, shp = s0;
    if (real != null && (wP || wS)) {
      const left = real - est;
      let best = null;
      for (let a = 0; a <= 8; a++) for (let b = 0; b <= 6; b++) {
        if ((!wP && a) || (!wS && b)) continue;
        if (Math.abs(left - a * wP - b * wS) >= 0.05) continue;
        const d = Math.abs(a - p0) + Math.abs(b - s0);
        if (!best || d < best[2]) best = [a, b, d];
      }
      if (best) { ppp = best[0]; shp = best[1]; }
    }
    if (ppp && wP) { add("Power Play Points", wP, ppp); est += ppp * wP; }
    if (shp && wS) { add("Shorthanded Points", wS, shp); est += shp * wS; }'''


def change(t):
    t = lit(t, "178: box power play and shorthanded points", OLD, NEW, "change 178: power play and shorthanded points")
    return t


edit(APP, change)
