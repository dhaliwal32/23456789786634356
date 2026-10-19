# changes/084-head-start-80.py - Pickups for next week: comes up by itself at 80% (or 20%), and you can turn it on yourself any week you have moves left

OLD_RULES = '''const gxHsOff = (s) => !!uiGet()[gxHsKey(s)];
const gxHsSet = (s, off) => { uiSet(gxHsKey(s), off); window.dispatchEvent(new Event("gx-hs83")); };
const gxHsCan = (s, base, ml) => !!nextWkS(s) && ml > 0 && base != null && (base >= GX_HS_SURE || base <= 1 - GX_HS_SURE);'''

NEW_RULES = '''const gxHsMode = (s) => { const v = uiGet()[gxHsKey(s)]; return v === "on" ? "on" : v === "off" || v === true ? "off" : ""; }; /* change 084 */
const gxHsAuto = (base) => base != null && (base >= GX_HS_SURE || base <= 1 - GX_HS_SURE);
const gxHsOff = (s) => gxHsMode(s) === "off";
const gxHsSet = (s, v) => { uiSet(gxHsKey(s), v); window.dispatchEvent(new Event("gx-hs83")); };
const gxHsCan = (s, base, ml) => !!nextWkS(s) && ml > 0 && base != null;
const gxHsOn = (s, base, ml) => gxHsCan(s, base, ml) && (gxHsMode(s) === "on" || (gxHsMode(s) === "" && gxHsAuto(base)));'''

OLD_LINE = '''  if (gxHsOff(s)) return <span>{" "}<button type="button" className="text-blue-600 text-sm" style={btn} onClick={() => gxHsSet(s, false)}>Use them for next week instead</button></span>;
  return (
    <span className="text-slate-500">
      {" " + (base >= GX_HS_SURE ? "You're " + wpTxt(base) + " to win this week" : "This week looks lost (" + wpTxt(base) + ")") + ", so they're aimed at next week."}
      <button type="button" className="text-blue-600 text-sm" style={btn} onClick={() => gxHsSet(s, true)}>Keep them for this week</button>'''

NEW_LINE = '''  if (!gxHsOn(s, base, ml)) return <span>{" "}<button type="button" className="text-blue-600 text-sm" style={btn} onClick={() => gxHsSet(s, "on")}>Use them for next week instead</button></span>;
  const why084 = base >= GX_HS_SURE ? "You're " + wpTxt(base) + " to win this week, so they're aimed at next week." : base <= 1 - GX_HS_SURE ? "This week looks lost (" + wpTxt(base) + "), so they're aimed at next week." : "Aimed at next week by you (" + wpTxt(base) + " to win this week).";
  return (
    <span className="text-slate-500">
      {" " + why084}
      <button type="button" className="text-blue-600 text-sm" style={btn} onClick={() => gxHsSet(s, "off")}>Keep them for this week</button>'''

def change(t):
    t = lit(t, "084: 80% cutoff", "const GX_HS_SURE = 0.85;", "const GX_HS_SURE = 0.80;", "const GX_HS_SURE = 0.80;")
    t = lit(t, "084: on/off rules", OLD_RULES, NEW_RULES, "/* change 084 */")
    t = lit(t, "084: top line", OLD_LINE, NEW_LINE, "const why084")
    t = lit(t, "084: box follows the choice",
            "  const on = gxHsCan(s, base, ml) && !gxHsOff(s);",
            "  const on = gxHsOn(s, base, ml);",
            "  const on = gxHsOn(s, base, ml);")
    t = lit(t, "084: protect this week",
            "      if (base >= GX_HS_SURE && now < Math.min(base, GX_HS_SURE) - 0.03) return;",
            "      if (base >= 0.5 && now < (gxHsAuto(base) ? Math.min(base, GX_HS_SURE) : base) - 0.03) return;",
            "(gxHsAuto(base) ? Math.min(base, GX_HS_SURE) : base) - 0.03")
    return t

edit(APP, change)
