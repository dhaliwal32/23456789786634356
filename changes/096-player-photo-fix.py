# changes/096-player-photo-fix.py - player screen: bigger clean photo frame, ice time never shows ":60"; player faces (with a small team logo) everywhere a team logo sat beside a player

def change(t):
    # laptop: frame is the photo's own shape (350 x 254), sized so its bottom lines up with the Status row
    t = lit(t, "096: header width",
            "  .gx-pd-hd { display: grid; grid-template-columns: 132px 1fr 170px;",
            "  .gx-pd-hd { display: grid; grid-template-columns: 193px 1fr 170px;",
            "grid-template-columns: 193px 1fr 170px;")
    t = lit(t, "096: photo frame",
            "  .gx-pd-ph { position: relative; width: 132px; height: 112px; border-radius: 10px; overflow: hidden; background: var(--card2); display: flex; align-items: flex-end; justify-content: center; }",
            "  .gx-pd-ph { position: relative; width: 193px; aspect-ratio: 350 / 254; height: auto; border-radius: 10px; overflow: hidden; background: var(--card2); border: 1px solid var(--line); display: flex; align-items: flex-end; justify-content: center; } /* gx096 */",
            "/* gx096 */")
    t = lit(t, "096: photo fill",
            "  .gx-pd-ph img { position: relative; height: 104px; width: auto; object-fit: contain; }",
            "  .gx-pd-ph img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; object-position: center bottom; display: block; }",
            "object-position: center bottom; display: block;")
    # phone: same shape, a little smaller
    t = lit(t, "096: phone header",
            "    .gx-pd-hd { grid-template-columns: 96px 1fr;",
            "    .gx-pd-hd { grid-template-columns: 112px 1fr;",
            "grid-template-columns: 112px 1fr;")
    t = lit(t, "096: phone frame",
            "    .gx-pd-ph { width: 96px; height: 96px; }",
            "    .gx-pd-ph { width: 112px; height: auto; }",
            ".gx-pd-ph { width: 112px; height: auto; }")
    t = lit(t, "096: phone photo",
            "    .gx-pd-ph img { height: 90px; }",
            "    .gx-pd-ph img { height: 100%; }",
            ".gx-pd-ph img { height: 100%; }")
    # 18:60 becomes 19:00
    t = lit(t, "096: ice time rounding",
            'const gxPdMS = (v) => (v == null ? "-" : Math.floor(v / 60) + ":" + String(Math.round(v % 60)).padStart(2, "0"));',
            'const gxPdMS = (v) => { if (v == null) return "-"; const r = Math.round(v); return Math.floor(r / 60) + ":" + String(r % 60).padStart(2, "0"); };',
            "const r = Math.round(v); return Math.floor(r / 60)")
    return t


edit(APP, change)


FACE_CSS = r"""  /* change 096 faces (install.py) */
  .gx-face { position: relative; display: inline-block; flex: none; vertical-align: middle; }
  .gx-face > .c { position: absolute; inset: 0; border-radius: 50%; overflow: hidden; background: var(--card2); box-shadow: inset 0 0 0 1px var(--line); }
  .gx-face > .c > img { width: 100%; height: 100%; object-fit: cover; transform: scale(1.45); transform-origin: 50% 22%; display: block; }
  .gx-face > .bd { position: absolute; right: -1px; bottom: -1px; border-radius: 50%; background: var(--card); box-shadow: 0 0 0 1px var(--line); display: flex; align-items: center; justify-content: center; overflow: hidden; }
</style>"""

FACE_JS = r"""// ---------- change 096: player faces beside names (install.py) ----------
// a round ESPN headshot with a small team logo badge; the plain team logo if there is no photo
function GxFace({ p, t, size }) {
  const [bad, setBad] = useState(false);
  const tm = (p && p.t) || t, z = size || 28;
  const eid = p && typeof p.id === "string" && p.id[0] === "e" ? p.id.slice(1) : null;
  if (!eid || bad) return <TeamLogo t={tm} size={size} />;
  const b = Math.max(11, Math.round(z * 0.5));
  return (
    <span className="gx-face" style={{ width: z, height: z }} title={(p.n || "") + " (" + tm + ")"}>
      <span className="c"><img src={"https://a.espncdn.com/i/headshots/nhl/players/full/" + eid + ".png"} alt="" loading="lazy" onError={() => setBad(true)} /></span>
      <span className="bd" style={{ width: b, height: b }}><TeamLogo t={tm} size={b - 2} /></span>
    </span>
  );
}
"""


def faces(t):
    t = lit(t, "096: face styles", "</style>", FACE_CSS, "change 096 faces (install.py)")
    t = lit(t, "096: face helper", ROOT, FACE_JS + ROOT, "change 096: player faces beside names")
    if "<GxFace p={" in t.split("function GxFace")[0] or t.count("<GxFace p={") > 2:
        print("(install) 096: faces in lists: already done")
        return t
    # goalie board: the goalie may be missing, so pass his team too
    old_g = "<TeamLogo t={x.t} size={18} />"
    if t.count(old_g) != 2:
        fail("096: goalie board logos: expected 2, found " + str(t.count(old_g)))
    t = t.replace(old_g, "<GxFace p={x.p} t={x.t} size={18} />")
    # every other logo drawn from a player's own team (not the 095 photo watermark, size 44)
    pat = re.compile(r"<TeamLogo t=\{(p|a|r\.f|r\.p|x\.p)\.t\}( size=\{(\d+)\})? />")
    n = [0]
    def rep(m):
        if m.group(3) == "44":
            return m.group(0)
        n[0] += 1
        return "<GxFace p={" + m.group(1) + "}" + (m.group(2) or "") + " />"
    t = pat.sub(rep, t)
    if n[0] != 36:
        fail("096: expected 36 player logos, found " + str(n[0]) + "; nothing changed")
    print("(install) 096: faces in lists: updated (38 places)")
    return t


edit(APP, faces)
