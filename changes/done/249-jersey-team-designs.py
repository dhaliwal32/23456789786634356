# changes/249-jersey-team-designs.py - Lines jerseys use Kuvar's chosen jersey colours and stripe patterns per team (body, shoulder yoke, lower sleeves, sleeve and hem stripes, number and name colours); no logos

HELPERS = r'''// ---------- change 249: per-team jersey colours and stripes from Kuvar's jersey sheet (install.py) ----------
// b body, y shoulder yoke, ys stripes under the yoke, sl lower sleeves, st sleeve and hem stripes (top to bottom), hm below the hem stripes, col collar, n number, o number outline, nm name
const GX_JD249 = {
  ANA: { b: "#1e8a4c", col: "#4b2a7b", sl: "#4b2a7b", st: ["#f2c230", "#4b2a7b", "#f2c230"], hm: "#4b2a7b", n: "#f2c230", o: "#4b2a7b", nm: "#f2c230" },
  BOS: { b: "#5a3a22", st: ["#f2c230", "#5a3a22", "#f2c230"], n: "#f2c230", o: "#2e1c10", nm: "#f2c230" },
  BUF: { b: "#1f4fae", st: ["#ffffff", "#c9a227", "#ffffff"], hm: "#1f4fae", n: "#ffffff", o: "#0f2a66", nm: "#ffffff" },
  CAR: { b: "#3a3b3f", st: ["#c8102e", "#9a9da3", "#c8102e"], hm: "#3a3b3f", n: "#f2f2f2", o: "#1c1c1f", nm: "#f2f2f2" },
  CBJ: { b: "#a7aab0", y: "#2f6fcf", sl: "#2f6fcf", st: ["#0f1e3d", "#2f6fcf", "#0f1e3d"], hm: "#0f1e3d", n: "#1a2238", o: "#a7aab0", nm: "#1a2238" },
  CGY: { b: "#c8102e", st: ["#e8c45a", "#ffffff", "#e8c45a"], hm: "#d6ad3e", n: "#ffffff", o: "#c9952a", nm: "#f1c75a" },
  CHI: { b: "#1e8a3c", st: ["#111111", "#f3efe0", "#111111", "#f3efe0", "#111111"], hm: "#f3efe0", n: "#ffffff", o: "#111111", nm: "#ffffff" },
  COL: { b: "#f2f4f7", y: "#7fb3e0", sl: "#7fb3e0", st: ["#1f3b66", "#9aa3ad"], hm: "#9aa3ad", n: "#7fb3e0", o: "#1f3b66", nm: "#2a4a7a" },
  DAL: { b: "#f4f5f2", st: ["#111111", "#39d35a", "#111111"], hm: "#111111", n: "#111111", o: "#39d35a", nm: "#111111" },
  DET: { b: "#d2192f", sl: "#d2192f", st: ["#ffffff", "#ffffff"], hm: "#ffffff", n: "#ffffff", o: "#9e1022", nm: "#ffffff" },
  EDM: { b: "#141518", st: ["#ff6a13", "#141518", "#ff6a13"], hm: "#141518", n: "#141518", o: "#ff6a13", nm: "#ff6a13" },
  FLA: { b: "#f25d63", y: "#162447", ys: ["#f7d031", "#f28c1e", "#e2373b"], sl: "#162447", st: ["#f7d031", "#f28c1e"], hm: "#162447", n: "#f7d031", o: "#162447", nm: "#162447" },
  LA: { b: "#5b2a86", st: ["#f2c230", "#111111", "#f2c230"], hm: "#111111", n: "#111111", o: "#f2c230", nm: "#f2c230" },
  MIN: { b: "#141414", st: ["#1f7a3a", "#ffffff", "#1f7a3a"], hm: "#141414", n: "#141414", o: "#2fa04f", nm: "#ffffff" },
  MTL: { b: "#f4f4f4", st: ["#c8102e", "#1f3a8a", "#c8102e"], hm: "#f4f4f4", n: "#c8102e", o: "#f4f4f4", nm: "#c8102e" },
  NJ: { b: "#141414", st: ["#c8102e", "#141414", "#c8102e"], hm: "#c8102e", n: "#c8102e", o: "#141414", nm: "#c8102e" },
  NSH: { b: "#0f1f3d", st: ["#f2b81c", "#0f1f3d", "#f2b81c"], hm: "#0f1f3d", n: "#f2b81c", o: "#0f1f3d", nm: "#f2b81c" },
  NYI: { b: "#f4f4f4", y: "#132a52", sl: "#132a52", st: ["#9cc3e6", "#f47d30"], hm: "#132a52", n: "#132a52", o: "#f47d30", nm: "#132a52" },
  NYR: { b: "#14234a", st: ["#c8102e", "#ffffff", "#c8102e"], hm: "#14234a", n: "#c8102e", o: "#ffffff", nm: "#ffffff" },
  OTT: { b: "#141414", st: ["#c9a227", "#c8102e", "#c9a227"], hm: "#141414", n: "#e8b04a", o: "#7a1020", nm: "#e8b04a" },
  PHI: { b: "#6b6c70", st: ["#f47a20", "#111111", "#f47a20", "#111111", "#f47a20"], hm: "#6b6c70", n: "#f47a20", o: "#111111", nm: "#111111" },
  PIT: { b: "#141e3a", y: "#9fc6ea", st: ["#9fc6ea", "#f2c230", "#9fc6ea"], hm: "#9fc6ea", n: "#c9a227", o: "#141e3a", nm: "#f2c230" },
  SEA: { b: "#0f1c33", st: ["#e6dfc8", "#7fd0d6", "#e6dfc8"], hm: "#e6dfc8", n: "#d8d2bd", o: "#0f1c33", nm: "#ffffff" },
  SJ: { b: "#1fb2c2", sl: "#111111", st: ["#ffffff", "#9aa0a6"], hm: "#111111", n: "#ffffff", o: "#111111", nm: "#ffffff" },
  STL: { b: "#141414", st: ["#2a6fd6", "#9fc6ea", "#2a6fd6"], hm: "#141414", n: "#ffffff", o: "#2a6fd6", nm: "#ffffff" },
  TB: { b: "#151515", sl: "#6b6e73", st: ["#7fb3e0", "#7fb3e0"], hm: "#7fb3e0", n: "#7fb3e0", o: "#151515", nm: "#7fb3e0" },
  TOR: { b: "#ece6d4", st: ["#1b2b56", "#ece6d4", "#1b2b56"], hm: "#1b2b56", n: "#1b2b56", o: "#ece6d4", nm: "#1b2b56" },
  UTA: { b: "#8ec3ea", sl: "#111111", st: ["#ffffff", "#111111"], hm: "#111111", n: "#111111", o: "#8ec3ea", nm: "#111111" },
  VAN: { b: "#0f1f3d", st: ["#2a6fd6", "#0f1f3d", "#2a6fd6"], hm: "#0f1f3d", n: "#2a6fd6", o: "#0f1f3d", nm: "#2a6fd6" },
  VGK: { b: "#141414", ys: ["#1e6b4a", "#c9a227"], st: ["#1e6b4a", "#c9a227", "#c8102e", "#c9a227"], hm: "#141414", n: "#d4b25c", o: "#141414", nm: "#d4b25c" },
  WPG: { b: "#0d1a33", st: ["#41c8e6", "#0d1a33", "#41c8e6"], hm: "#0d1a33", n: "#0d1a33", o: "#41c8e6", nm: "#41c8e6" },
  WSH: { b: "#2a5fb0", y: "#f4f4f4", st: ["#ffffff", "#c9a227", "#ffffff"], hm: "#2a5fb0", n: "#ffffff", o: "#c9a227", nm: "#ffffff" },
};
'''

def change(t):
    t = lit(t, "249: helpers", ROOT, HELPERS + ROOT, "change 249: per-team jersey colours")
    t = lit(t, "249: read the team's design",
            "  const three = num.toLowerCase() !== trim.toLowerCase() && num.toLowerCase() !== body.toLowerCase(), dark = gxLum232(body) < 70;",
            '''  const D = GX_JD249[String(t || "").toUpperCase()] || null; /* change 249 */
  const ST = D ? D.st : null, NF = D ? D.n : num, NO = D ? D.o : trim, NM = D ? D.nm : num, NMO = D ? (D.o.toLowerCase() === D.nm.toLowerCase() ? "rgba(0,0,0,.45)" : D.o) : trim;
  const bandD = (y, x, w) => ST.map((c, i) => <rect key={"d" + y + x + i} x={x} y={y + i * 3.4} width={w} height="3.4" style={{ fill: c }} />);
  const three = num.toLowerCase() !== trim.toLowerCase() && num.toLowerCase() !== body.toLowerCase(), dark = D ? !!D.y : gxLum232(body) < 70;''',
            "const D = GX_JD249[String(t || \"\").toUpperCase()] || null; /* change 249 */")
    t = lit(t, "249: body colour", "<path d={shirt} style={{ fill: body }} />", "<path d={shirt} style={{ fill: D ? D.b : body }} />", "fill: D ? D.b : body")
    t = lit(t, "249: yoke and lower sleeves",
            '''        {dark ? <path d="M0 18 L120 18 L120 40 Q60 47 0 40 Z" style={{ fill: trim, opacity: 0.9 }} /> : null}''',
            '''        {D ? <>
          {D.sl ? <><rect x="0" y="86" width="23.6" height="40" style={{ fill: D.sl }} /><rect x="96.4" y="86" width="23.6" height="40" style={{ fill: D.sl }} /></> : null}
          {D.y ? <path d="M0 18 L120 18 L120 40 Q60 47 0 40 Z" style={{ fill: D.y }} /> : null}
          {(D.ys || []).map((c, i) => <path key={"ys" + i} d={"M0 " + (41.2 + i * 2.6) + " Q60 " + (48.2 + i * 2.6) + " 120 " + (41.2 + i * 2.6)} style={{ fill: "none", stroke: c, strokeWidth: 2.6 }} />)}
        </> : dark ? <path d="M0 18 L120 18 L120 40 Q60 47 0 40 Z" style={{ fill: trim, opacity: 0.9 }} /> : null}''',
            '''{D.sl ? <><rect x="0" y="86" width="23.6"''')
    t = lit(t, "249: stripes",
            "        {band(80, 0, 26)}{band(80, 94, 26)}{band(108, 24, 72)}",
            '''        {D ? <>{bandD(76, 0, 26)}{bandD(76, 94, 26)}{bandD(108, 24, 72)}{D.hm ? <rect x="24" y={108 + ST.length * 3.4} width="72" height="40" style={{ fill: D.hm }} /> : null}</> : <>{band(80, 0, 26)}{band(80, 94, 26)}{band(108, 24, 72)}</>}''',
            "{bandD(76, 0, 26)}")
    t = lit(t, "249: collar",
            '''        <path d="M44 20 Q60 29 76 20 L79 24 Q60 34 41 24 Z" style={{ fill: trim }} />''',
            '''        <path d="M44 20 Q60 29 76 20 L79 24 Q60 34 41 24 Z" style={{ fill: D ? (D.col || D.y || ST[0]) : trim }} />''',
            "fill: D ? (D.col || D.y || ST[0]) : trim")
    t = lit(t, "249: cuffs",
            '''        <path d="M0 104 L19 109 L18 117 L0 112 Z M120 104 L101 109 L102 117 L120 112 Z" style={{ fill: trim }} />''',
            '''        <path d="M0 104 L19 109 L18 117 L0 112 Z M120 104 L101 109 L102 117 L120 112 Z" style={{ fill: D ? (D.hm || ST[0]) : trim }} />''',
            "fill: D ? (D.hm || ST[0]) : trim")
    t = lit(t, "249: twill colours (outer)",
            '''    <text key="o2" {...props} style={{ ...props.style, fill: num, stroke: gxLum232(trim) > 140 ? "rgba(0,0,0,.55)" : "rgba(255,255,255,.35)", strokeWidth: props.sw + 1.6, paintOrder: "stroke", strokeLinejoin: "round" }}>{kids}</text>,''',
            '''    <text key="o2" {...props} style={{ ...props.style, fill: props.f || num, stroke: gxLum232(props.k || trim) > 140 ? "rgba(0,0,0,.55)" : "rgba(255,255,255,.35)", strokeWidth: props.sw + 1.6, paintOrder: "stroke", strokeLinejoin: "round" }}>{kids}</text>,''',
            "fill: props.f || num, stroke: gxLum232(props.k || trim)")
    t = lit(t, "249: twill colours (inner)",
            '''    <text key="o1" {...props} style={{ ...props.style, fill: num, stroke: trim, strokeWidth: props.sw, paintOrder: "stroke", strokeLinejoin: "round" }}>{kids}</text>,''',
            '''    <text key="o1" {...props} style={{ ...props.style, fill: props.f || num, stroke: props.k || trim, strokeWidth: props.sw, paintOrder: "stroke", strokeLinejoin: "round" }}>{kids}</text>,''',
            "fill: props.f || num, stroke: props.k || trim, strokeWidth: props.sw")
    t = lit(t, "249: stitch line colour",
            '''    <text key="st" {...props} style={{ ...props.style, fill: "none", stroke: gxLum232(num) > 140 ? "rgba(0,0,0,.28)" : "rgba(255,255,255,.4)", strokeWidth: 0.35, strokeDasharray: "0.9 0.9" }}>{kids}</text>,''',
            '''    <text key="st" {...props} style={{ ...props.style, fill: "none", stroke: gxLum232(props.f || num) > 140 ? "rgba(0,0,0,.28)" : "rgba(255,255,255,.4)", strokeWidth: 0.35, strokeDasharray: "0.9 0.9" }}>{kids}</text>,''',
            "gxLum232(props.f || num) > 140")
    t = lit(t, "249: name colours",
            '''      {twill({ className: "nm231", textAnchor: "middle", style: { fontSize: nmSize }, sw: 1.2 }''',
            '''      {twill({ className: "nm231", textAnchor: "middle", style: { fontSize: nmSize }, sw: 1.2, f: NM, k: NMO }''',
            "sw: 1.2, f: NM, k: NMO")
    t = lit(t, "249: number colours",
            '''      {twill({ className: "no231", x: 60, y: 95, textAnchor: "middle", style: { fontSize: nTxt.length > 1 ? 40 : 44 }, sw: 3 }, nTxt)}''',
            '''      {twill({ className: "no231", x: 60, y: 95, textAnchor: "middle", style: { fontSize: nTxt.length > 1 ? 40 : 44 }, sw: 3, f: NF, k: NO }, nTxt)}''',
            "sw: 3, f: NF, k: NO }, nTxt)}")
    return t

edit(APP, change)
