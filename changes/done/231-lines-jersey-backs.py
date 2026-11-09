# changes/231-lines-jersey-backs.py - Lines: every player card shows the back of a jersey in his team's colours with his name and number

NEW_CSS = r'''  /* change 231 (install.py): jersey backs on Lines */
  .gx-fg224.gx-lt227 .md.jr231 { width: 100%; max-width: 104px; height: auto; aspect-ratio: 120 / 112; background: none; border-radius: 0; overflow: visible; display: block; }
  .gx-fg224.gx-lt227 .md.jr231 svg { width: 100%; height: 100%; display: block; overflow: visible; }
  .gx-fg224.gx-lt227 .jr231 .nm231 { font-family: "Arial Black", "Helvetica Neue", Arial, sans-serif; font-weight: 900; letter-spacing: .04em; }
  .gx-fg224.gx-lt227 .jr231 .no231 { font-family: "Arial Black", "Helvetica Neue", Arial, sans-serif; font-weight: 900; }
  .gx-fg224.gx-lt227 .nm { display: none; }
  .gx-fg224.gx-lt227 .sb227 { margin-top: 4px; }
</style>'''

HELPERS = r'''// ---------- change 231: jersey backs on Lines (install.py) ----------
// a plain jersey seen from behind in the team's colours (GX_JC224: body, trim, numbers), name arched over a big number
function GxJersey231({ t, name, no, goalie }) {
  const c = GX_JC224[t] || GX_JC224[String(t || "").toUpperCase()] || ["#3a3d44", "#9aa0a8", "#ffffff"];
  const body = c[0], trim = c[1], num = c[2] || "#ffffff";
  const id = "j231" + String(t || "x") + String(no == null ? "" : no) + String(name || "").replace(/[^A-Za-z]/g, "");
  const nm = String(name || "").toUpperCase();
  const nmSize = Math.max(6.2, Math.min(10.5, 92 / Math.max(5, nm.length)));
  const nTxt = no == null ? "" : String(no);
  const outline = (hex) => { const h = String(hex).replace("#", ""); const v = parseInt(h.length === 3 ? h.split("").map((x) => x + x).join("") : h, 16); const r = (v >> 16) & 255, g = (v >> 8) & 255, b = v & 255; return 0.299 * r + 0.587 * g + 0.114 * b > 150 ? "rgba(0,0,0,.35)" : "rgba(255,255,255,.18)"; };
  const shirt = "M42 6 Q60 14 78 6 L98 12 Q108 16 112 26 L119 58 L101 64 L95 44 L94 106 Q60 111 26 106 L25 44 L19 64 L1 58 L8 26 Q12 16 22 12 Z";
  return (
    <svg viewBox="0 0 120 112" role="img" aria-label={(name || "") + (nTxt ? " number " + nTxt : "")}>
      <defs><clipPath id={id}><path d={shirt} /></clipPath></defs>
      <path d={shirt} style={{ fill: body, stroke: outline(body), strokeWidth: 1 }} />
      <g clipPath={"url(#" + id + ")"}>
        <rect x="0" y="45" width="30" height="5.5" style={{ fill: trim }} /><rect x="0" y="52.5" width="30" height="2.4" style={{ fill: num }} /><rect x="0" y="56.8" width="30" height="5.5" style={{ fill: trim }} />
        <rect x="90" y="45" width="30" height="5.5" style={{ fill: trim }} /><rect x="90" y="52.5" width="30" height="2.4" style={{ fill: num }} /><rect x="90" y="56.8" width="30" height="5.5" style={{ fill: trim }} />
        <rect x="0" y="88" width="120" height="5.5" style={{ fill: trim }} /><rect x="0" y="95.5" width="120" height="2.4" style={{ fill: num }} />
        {goalie ? <rect x="0" y="99.5" width="120" height="5" style={{ fill: trim }} /> : null}
        <path d="M42 6 Q60 14 78 6 L80 9 Q60 18 40 9 Z" style={{ fill: trim }} />
        <path d="M25 44 L25 104" style={{ stroke: "rgba(0,0,0,.18)", strokeWidth: 1 }} /><path d="M95 44 L95 104" style={{ stroke: "rgba(0,0,0,.18)", strokeWidth: 1 }} />
      </g>
      <path id={id + "a"} d="M30 33 Q60 25 90 33" fill="none" />
      <text className="nm231" style={{ fontSize: nmSize, fill: num, stroke: trim, strokeWidth: 0.9, paintOrder: "stroke" }} textAnchor="middle"><textPath href={"#" + id + "a"} startOffset="50%">{nm}</textPath></text>
      <text className="no231" x="60" y="79" textAnchor="middle" style={{ fontSize: nTxt.length > 1 ? 40 : 44, fill: num, stroke: trim, strokeWidth: 2.4, paintOrder: "stroke", strokeLinejoin: "round" }}>{nTxt}</text>
    </svg>
  );
}
'''

OLD = '''<div className="md"><GxLnPic227 p={p} no={((T && T.no) || {})[n]} /></div>'''
NEW = '''<div className="md jr231"><GxJersey231 t={p ? p.t : t} name={last} no={((T && T.no) || {})[n]} goalie={isG} /></div>'''

def change(t):
    t = lit(t, "231: styles", "</style>", NEW_CSS, "change 231 (install.py): jersey backs on Lines")
    t = lit(t, "231: helpers", ROOT, HELPERS + ROOT, "change 231: jersey backs on Lines")
    t = lit(t, "231: card", OLD, NEW, "<GxJersey231 t={p ? p.t : t}")
    return t

edit(APP, change)
