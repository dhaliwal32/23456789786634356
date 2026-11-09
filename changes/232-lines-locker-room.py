# changes/232-lines-locker-room.py - Lines as a locker room: jerseys with fabric, folds and stitched numbers hang in wooden stalls, names always fit, no borders

NEW_CSS = r'''  /* change 232 (install.py): Lines locker room */
  .gx-rk111 { border: 0; border-radius: 14px; padding: 12px 8px 10px; background: linear-gradient(180deg, #17191d, #101214); }
  html[data-theme="light"] .gx-rk111 { background: linear-gradient(180deg, #e7e2da, #d9d2c6); }
  .gx-rk111 .logo { opacity: .04; }
  .gx-rk111 .row { margin: 0 0 10px; }
  .gx-fg224.gx-lt227, .gx-fg224.gx-lt227.me, .gx-fg224.gx-lt227.fa { border: 0; box-shadow: inset 0 10px 14px -10px rgba(0,0,0,.6), inset 6px 0 8px -6px rgba(0,0,0,.55), inset -6px 0 8px -6px rgba(0,0,0,.55); border-radius: 6px 6px 3px 3px; padding: 6px 3px 7px;
    background: repeating-linear-gradient(90deg, rgba(255,255,255,.025) 0 2px, rgba(0,0,0,.035) 2px 5px, rgba(255,255,255,0) 5px 9px), linear-gradient(180deg, #4a3423, #36261a 60%, #2b1f15); }
  html[data-theme="light"] .gx-fg224.gx-lt227 { background: repeating-linear-gradient(90deg, rgba(255,255,255,.06) 0 2px, rgba(0,0,0,.04) 2px 5px, rgba(255,255,255,0) 5px 9px), linear-gradient(180deg, #c99e6f, #b3875b 60%, #a37950); box-shadow: inset 0 10px 14px -10px rgba(0,0,0,.35), inset 6px 0 8px -6px rgba(0,0,0,.3), inset -6px 0 8px -6px rgba(0,0,0,.3); }
  .gx-fg224.gx-lt227.empty { background: rgba(0,0,0,.18); border: 0; box-shadow: none; }
  .gx-fg224.gx-lt227 .md.jr231 { max-width: 112px; aspect-ratio: 120 / 140; }
  .gx-fg224.gx-lt227 .pl232 { display: block; max-width: 92%; margin: 0 auto 2px; padding: 2px 6px; border-radius: 3px; font-size: 9.5px; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
    color: #2a2218; background: linear-gradient(180deg, #f1e6c8, #d8c79c); box-shadow: 0 1px 0 rgba(255,255,255,.25) inset, 0 1px 2px rgba(0,0,0,.45); }
  .gx-fg224.gx-lt227 .sb227, .gx-fg224.gx-lt227 .ow227 { color: rgba(255,255,255,.72); }
  .gx-fg224.gx-lt227 .ow227 b { color: #fff; }
  html[data-theme="light"] .gx-fg224.gx-lt227 .sb227, html[data-theme="light"] .gx-fg224.gx-lt227 .ow227 { color: rgba(30,20,10,.75); }
  html[data-theme="light"] .gx-fg224.gx-lt227 .ow227 b { color: #1d150d; }
  .gx-fg224.gx-lt227.me .ow227 span:first-child { color: #fff; background: rgba(0,0,0,.45); padding: 1px 5px; border-radius: 4px; }
  html[data-theme="light"] .gx-fg224.gx-lt227.me .ow227 span:first-child { color: #fff; background: #1d150d; }
  .gx-fg224.gx-lt227.fa .ow227 span:first-child { color: #7fe0a3; }
  html[data-theme="light"] .gx-fg224.gx-lt227.fa .ow227 span:first-child { color: #0f6b34; }
</style>'''

HELPERS = r'''// ---------- change 232: Lines locker room jerseys (install.py) ----------
// one jersey shape for every team (no team's real design), coloured from GX_JC224, with fabric, folds and stitched name and number
function gxLum232(hex) { const h = String(hex || "#777").replace("#", ""); const v = parseInt(h.length === 3 ? h.split("").map((x) => x + x).join("") : h, 16); return 0.299 * ((v >> 16) & 255) + 0.587 * ((v >> 8) & 255) + 0.114 * (v & 255); }
function GxJersey232({ t, name, no, goalie }) {
  const c = GX_JC224[t] || GX_JC224[String(t || "").toUpperCase()] || ["#3a3d44", "#9aa0a8", "#ffffff"];
  const body = c[0], trim = c[1], num = c[2] || "#ffffff";
  const id = "j232" + String(t || "x") + String(no == null ? "" : no) + String(name || "").replace(/[^A-Za-z]/g, "");
  const nm = String(name || "").toUpperCase(), nTxt = no == null ? "" : String(no);
  const three = num.toLowerCase() !== trim.toLowerCase() && num.toLowerCase() !== body.toLowerCase(), dark = gxLum232(body) < 70;
  const nmSize = 9.5, nmW = nm.length * nmSize * 0.8, NMMAX = 58;
  const shirt = "M44 20 Q60 29 76 20 L100 26 Q112 31 116 43 L119 78 L102 83 L96 58 L96 128 Q60 134 24 128 L24 58 L18 83 L1 78 L4 43 Q8 31 20 26 Z";
  // stripes: three colours get trim / number / trim bands, two colours get two trim bands
  const band = (y, x, w) => three
    ? [<rect key={"a" + y + x} x={x} y={y} width={w} height="5" style={{ fill: trim }} />, <rect key={"b" + y + x} x={x} y={y + 6.2} width={w} height="2.4" style={{ fill: num }} />, <rect key={"c" + y + x} x={x} y={y + 9.8} width={w} height="5" style={{ fill: trim }} />]
    : [<rect key={"a" + y + x} x={x} y={y} width={w} height="4.6" style={{ fill: trim }} />, <rect key={"c" + y + x} x={x} y={y + 7.4} width={w} height="4.6" style={{ fill: trim }} />];
  const twill = (props, kids) => [
    <text key="sh" {...props} transform="translate(0.7 1.3)" style={{ ...props.style, fill: "rgba(0,0,0,.4)", stroke: "rgba(0,0,0,.4)", strokeWidth: props.sw + 1.6 }}>{kids}</text>,
    <text key="o2" {...props} style={{ ...props.style, fill: num, stroke: gxLum232(trim) > 140 ? "rgba(0,0,0,.55)" : "rgba(255,255,255,.35)", strokeWidth: props.sw + 1.6, paintOrder: "stroke", strokeLinejoin: "round" }}>{kids}</text>,
    <text key="o1" {...props} style={{ ...props.style, fill: num, stroke: trim, strokeWidth: props.sw, paintOrder: "stroke", strokeLinejoin: "round" }}>{kids}</text>,
    <text key="st" {...props} style={{ ...props.style, fill: "none", stroke: gxLum232(num) > 140 ? "rgba(0,0,0,.28)" : "rgba(255,255,255,.4)", strokeWidth: 0.35, strokeDasharray: "0.9 0.9" }}>{kids}</text>,
  ];
  return (
    <svg viewBox="0 0 120 140" role="img" aria-label={(name || "") + (nTxt ? " number " + nTxt : "")}>
      <defs>
        <clipPath id={id + "c"}><path d={shirt} /></clipPath>
        <pattern id={id + "m"} width="2.2" height="2.2" patternUnits="userSpaceOnUse"><circle cx="0.55" cy="0.55" r="0.42" fill="rgba(0,0,0,.16)" /><circle cx="1.65" cy="1.65" r="0.42" fill="rgba(255,255,255,.06)" /></pattern>
        <linearGradient id={id + "s"} x1="0" x2="1" y1="0" y2="0"><stop offset="0" stopColor="#000" stopOpacity=".42" /><stop offset=".2" stopColor="#000" stopOpacity=".1" /><stop offset=".5" stopColor="#fff" stopOpacity=".08" /><stop offset=".8" stopColor="#000" stopOpacity=".1" /><stop offset="1" stopColor="#000" stopOpacity=".42" /></linearGradient>
        <linearGradient id={id + "v"} x1="0" x2="0" y1="0" y2="1"><stop offset="0" stopColor="#fff" stopOpacity=".1" /><stop offset=".35" stopColor="#fff" stopOpacity="0" /><stop offset="1" stopColor="#000" stopOpacity=".3" /></linearGradient>
        <path id={id + "a"} d="M27 47 Q60 37 93 47" fill="none" />
      </defs>
      <path d="M60 3 Q66 3 66 8 Q66 12 61 13 L60 19" style={{ fill: "none", stroke: "#b9bcc2", strokeWidth: 2.2, strokeLinecap: "round" }} />
      <path d="M24 26 Q60 14 96 26" style={{ fill: "none", stroke: "#8e6a45", strokeWidth: 4, strokeLinecap: "round" }} />
      <path d={shirt} transform="translate(1.5 2.5)" style={{ fill: "rgba(0,0,0,.35)" }} />
      <path d={shirt} style={{ fill: body }} />
      <g clipPath={"url(#" + id + "c)"}>
        {dark ? <path d="M0 18 L120 18 L120 40 Q60 47 0 40 Z" style={{ fill: trim, opacity: 0.9 }} /> : null}
        {band(60, 0, 24)}{band(60, 96, 24)}{band(108, 0, 120)}
        <path d="M44 20 Q60 29 76 20 L79 24 Q60 34 41 24 Z" style={{ fill: trim }} />
        <path d="M0 74 L22 80 L22 86 L0 80 Z M120 74 L98 80 L98 86 L120 80 Z" style={{ fill: trim }} />
        {goalie ? <rect x="0" y="122" width="120" height="4" style={{ fill: num }} /> : null}
        <rect x="0" y="0" width="120" height="140" style={{ fill: "url(#" + id + "m)" }} />
        <rect x="0" y="0" width="120" height="140" style={{ fill: "url(#" + id + "s)" }} />
        <rect x="0" y="0" width="120" height="140" style={{ fill: "url(#" + id + "v)" }} />
        <path d="M24 60 Q30 66 27 80 M96 60 Q90 66 93 80 M36 120 Q44 114 52 121 M70 121 Q78 114 86 120 M30 98 Q34 90 31 82 M90 98 Q86 90 89 82" style={{ fill: "none", stroke: "rgba(0,0,0,.2)", strokeWidth: 1.3, strokeLinecap: "round" }} />
        <path d="M25 61 Q31 67 28 80 M95 61 Q89 67 92 80" style={{ fill: "none", stroke: "rgba(255,255,255,.07)", strokeWidth: 1, strokeLinecap: "round" }} />
        <path d="M45 22 Q34 36 24 58 M75 22 Q86 36 96 58" style={{ fill: "none", stroke: "rgba(0,0,0,.28)", strokeWidth: 0.6, strokeDasharray: "1.4 1.2" }} />
      </g>
      {twill({ className: "nm231", textAnchor: "middle", style: { fontSize: nmSize }, sw: 1.2 }, <textPath href={"#" + id + "a"} startOffset="50%" {...(nmW > NMMAX ? { textLength: NMMAX, lengthAdjust: "spacingAndGlyphs" } : {})}>{nm}</textPath>)}
      {twill({ className: "no231", x: 60, y: 95, textAnchor: "middle", style: { fontSize: nTxt.length > 1 ? 40 : 44 }, sw: 3 }, nTxt)}
    </svg>
  );
}
'''

OLD = '''<div className="md jr231"><GxJersey231 t={p ? p.t : t} name={last} no={((T && T.no) || {})[n]} goalie={isG} /></div>'''
NEW = '''<div className="md jr231"><span className="pl232">{last}</span><GxJersey232 t={p ? p.t : t} name={last} no={((T && T.no) || {})[n]} goalie={isG} /></div>'''

def change(t):
    t = lit(t, "232: styles", "</style>", NEW_CSS, "change 232 (install.py): Lines locker room")
    t = lit(t, "232: helpers", ROOT, HELPERS + ROOT, "change 232: Lines locker room jerseys")
    t = lit(t, "232: card", OLD, NEW, "<GxJersey232 t={p ? p.t : t}")
    return t

edit(APP, change)
