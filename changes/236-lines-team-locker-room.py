# changes/236-lines-team-locker-room.py - Lines: each team gets its own drawn locker room (team colours, ceiling lights, lit stalls, carpet with logo, 4 room styles)

NEW_CSS = r'''  /* change 236 (install.py): team locker room */
  .gx-rk111.rm236 { padding: 44px 8px 92px; border-radius: 14px; overflow: hidden; isolation: isolate;
    background: repeating-linear-gradient(90deg, rgba(255,255,255,.035) 0 1px, rgba(0,0,0,0) 1px 64px), linear-gradient(180deg, color-mix(in srgb, var(--rb) 38%, #07080a) 0%, color-mix(in srgb, var(--rb) 52%, #0b0c0f) 55%, color-mix(in srgb, var(--rb) 30%, #050607) 100%); }
  html[data-theme="light"] .gx-rk111.rm236 { background: repeating-linear-gradient(90deg, rgba(255,255,255,.035) 0 1px, rgba(0,0,0,0) 1px 64px), linear-gradient(180deg, color-mix(in srgb, var(--rb) 38%, #07080a) 0%, color-mix(in srgb, var(--rb) 52%, #0b0c0f) 55%, color-mix(in srgb, var(--rb) 30%, #050607) 100%); }
  .gx-rk111.rm236 > .logo { display: none; }
  .gx-rk111.rm236 .row { z-index: 2; }
  .gx-rk111.rm236 .row .lb { color: rgba(255,255,255,.62); }
  .rm236 .rr236 { position: absolute; inset: 0; pointer-events: none; z-index: 0; }
  .rm236 .cl236 { position: absolute; left: 0; right: 0; top: 0; height: 26px; background: linear-gradient(180deg, #0a0b0d, #16181c); box-shadow: 0 2px 6px rgba(0,0,0,.6); display: flex; justify-content: space-around; align-items: center; padding: 0 6%; }
  .rm236 .cl236 i { width: 34px; height: 7px; border-radius: 4px; background: var(--lc); box-shadow: 0 0 10px 2px var(--lc), 0 0 26px 6px color-mix(in srgb, var(--lc) 45%, transparent); }
  .rm236 .bm236 { position: absolute; top: 26px; width: 30%; height: 72%; transform: translateX(-50%); background: linear-gradient(180deg, color-mix(in srgb, var(--lc) 16%, transparent), transparent 85%); clip-path: polygon(38% 0, 62% 0, 100% 100%, 0 100%); }
  .rm236 .sr236 { position: absolute; left: 0; right: 0; top: 30px; height: 5px; background: var(--rt); box-shadow: 0 0 8px color-mix(in srgb, var(--rg) 50%, transparent); }
  .rm236 .sr236::after { content: ""; position: absolute; left: 0; right: 0; top: 7px; height: 2px; background: var(--rn); opacity: .7; }
  .rm236 .fl236 { position: absolute; left: 0; right: 0; bottom: 0; height: 84px; overflow: hidden;
    background: repeating-linear-gradient(45deg, rgba(255,255,255,.025) 0 2px, rgba(0,0,0,.03) 2px 4px), radial-gradient(ellipse at 50% 0%, color-mix(in srgb, var(--rb) 85%, #fff 8%), color-mix(in srgb, var(--rb) 70%, #000) 75%);
    box-shadow: inset 0 10px 14px -6px rgba(0,0,0,.7); border-top: 3px solid color-mix(in srgb, var(--rt) 80%, #000); }
  .rm236 .fl236 .lg236 { position: absolute; left: 50%; top: 50%; transform: translate(-50%, -48%) perspective(300px) rotateX(58deg); opacity: .55; filter: drop-shadow(0 0 1px rgba(0,0,0,.4)); }
  .rm236 .fl236 .lg236 img { display: block; }
  .rm236 .gx-fg224.gx-lt227, .rm236 .gx-fg224.gx-lt227.me, .rm236 .gx-fg224.gx-lt227.fa, html[data-theme="light"] .rm236 .gx-fg224.gx-lt227 { position: relative; padding-top: 10px;
    background: radial-gradient(ellipse at 50% 0%, color-mix(in srgb, var(--rg) 22%, transparent), transparent 55%), repeating-linear-gradient(90deg, rgba(255,255,255,.03) 0 2px, rgba(0,0,0,.04) 2px 5px, rgba(255,255,255,0) 5px 9px), linear-gradient(180deg, var(--w1), var(--w2) 60%, var(--w3));
    box-shadow: inset 0 10px 14px -10px rgba(0,0,0,.6), inset 6px 0 8px -6px rgba(0,0,0,.55), inset -6px 0 8px -6px rgba(0,0,0,.55), 0 4px 8px rgba(0,0,0,.35); }
  .rm236 .gx-fg224.gx-lt227::before { content: ""; position: absolute; left: 10%; right: 10%; top: 3px; height: 3px; border-radius: 2px; background: var(--rg); box-shadow: 0 0 6px 1px var(--rg), 0 4px 14px 2px color-mix(in srgb, var(--rg) 40%, transparent); }
  .rm236 .gx-fg224.gx-lt227.empty { background: rgba(0,0,0,.25); box-shadow: inset 0 0 10px rgba(0,0,0,.5); }
  .rm236 .gx-fg224.gx-lt227.empty::before { opacity: .25; }
  .rm236 .gx-fg224.gx-lt227 .pl232 { color: var(--rn); background: var(--rb); box-shadow: 0 0 0 1px var(--rt) inset, 0 1px 2px rgba(0,0,0,.5); }
  .rm236 .gx-fg224.gx-lt227 .sb227, .rm236 .gx-fg224.gx-lt227 .ow227, html[data-theme="light"] .rm236 .gx-fg224.gx-lt227 .sb227, html[data-theme="light"] .rm236 .gx-fg224.gx-lt227 .ow227 { color: var(--tx); }
  .rm236 .gx-fg224.gx-lt227 .ow227 b, html[data-theme="light"] .rm236 .gx-fg224.gx-lt227 .ow227 b { color: var(--tb); }
  .rm236 .gx-fg224.gx-lt227.me .ow227 span:first-child, html[data-theme="light"] .rm236 .gx-fg224.gx-lt227.me .ow227 span:first-child { color: #fff; background: rgba(0,0,0,.55); }
  .rm236 .gx-fg224.gx-lt227.fa .ow227 span:first-child, html[data-theme="light"] .rm236 .gx-fg224.gx-lt227.fa .ow227 span:first-child { color: var(--fa); }
  .rm236.walnut { --w1: #4a3423; --w2: #36261a; --w3: #2b1f15; --tx: rgba(255,255,255,.74); --tb: #fff; --fa: #7fe0a3; }
  .rm236.oak { --w1: #c99e6f; --w2: #b3875b; --w3: #a37950; --tx: rgba(30,20,10,.78); --tb: #1d150d; --fa: #0f6b34; }
  .rm236.white { --w1: #eceded; --w2: #dadbdd; --w3: #c8c9cc; --tx: rgba(20,22,26,.72); --tb: #111; --fa: #0f6b34; }
  .rm236.carbon { --w1: #33363d; --w2: #282b31; --w3: #1e2025; --tx: rgba(255,255,255,.74); --tb: #fff; --fa: #7fe0a3; }
  .rm236.white .gx-fg224.gx-lt227 { background: radial-gradient(ellipse at 50% 0%, color-mix(in srgb, var(--rg) 22%, transparent), transparent 55%), linear-gradient(180deg, var(--w1), var(--w2) 60%, var(--w3)); }
  .rm236.carbon .gx-fg224.gx-lt227 { background: radial-gradient(ellipse at 50% 0%, color-mix(in srgb, var(--rg) 22%, transparent), transparent 55%), repeating-linear-gradient(45deg, rgba(255,255,255,.035) 0 2px, rgba(0,0,0,0) 2px 4px), linear-gradient(180deg, var(--w1), var(--w2) 60%, var(--w3)); }
  @media (max-width: 640px) { .gx-rk111.rm236 { padding: 40px 5px 80px; } .rm236 .fl236 { height: 72px; } .rm236 .cl236 i { width: 24px; } }
</style>'''

HELPERS = r'''// ---------- change 236: each team's own locker room on Lines (install.py) ----------
const GX_RS236 = ["walnut", "carbon", "oak", "white"];
function gxRoom236(t) {
  const c = GX_JC224[t] || GX_JC224[String(t || "").toUpperCase()] || ["#3a3d44", "#9aa0a8", "#ffffff"];
  const body = c[0], trim = c[1], num = c[2] || "#ffffff";
  let gl = gxLum232(trim) >= gxLum232(num) ? trim : num;
  if (gxLum232(gl) < 60) gl = "#ffffff";
  const keys = Object.keys(GX_JC224).sort();
  const i = Math.max(0, keys.indexOf(String(t || "").toUpperCase()));
  const warm = i % 2 === 0;
  return { cls: GX_RS236[i % 4], style: { "--rb": body, "--rt": trim, "--rn": num, "--rg": gl, "--lc": warm ? "#ffe6b8" : "#e6f1ff" } };
}
function GxRoom236({ t }) {
  return (
    <div className="rr236" aria-hidden="true">
      {[12, 38, 62, 88].map((x) => <span key={x} className="bm236" style={{ left: x + "%" }} />)}
      <div className="cl236"><i /><i /><i /><i /><i /></div>
      <div className="sr236" />
      <div className="fl236"><span className="lg236"><TeamLogo t={t} size={150} /></span></div>
    </div>
  );
}
'''

def change(t):
    t = lit(t, "236: styles", "</style>", NEW_CSS, "change 236 (install.py): team locker room")
    t = lit(t, "236: helpers", ROOT, HELPERS + ROOT, "change 236: each team's own locker room")
    t = lit(t, "236: room on Lines",
            '{zoomEl224}<div key={t + mode} className="gx-rk111">\n            <GxRinkLines111 teamCode={t} />',
            '{zoomEl224}<div key={t + mode} className={"gx-rk111 rm236 " + gxRoom236(t).cls} style={gxRoom236(t).style} data-gx="236">\n            <GxRoom236 t={t} />\n            <GxRinkLines111 teamCode={t} />',
            'data-gx="236"')
    return t

edit(APP, change)
