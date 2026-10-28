# changes/119-box-score-popup.py - Matchup: tapping a player opens an ESPN-style pop-up (face, name, date and opponent, then Scoring category / Pts per / # / Score and a Total) instead of the box under the row; tap the name to open the profile

NEW_CSS = r'''  /* change 119 (install.py) */
  .gx-bm119 { position: fixed; inset: 0; z-index: 70; background: rgba(0,0,0,.6); display: flex; align-items: center; justify-content: center; padding: 70px 16px 24px; animation: gx101-fade .18s ease-out; }
  .gx-bm119 .cd { position: relative; width: min(420px, 100%); background: var(--card); color: var(--ink); border-radius: 16px; padding-top: 60px; box-shadow: 0 12px 40px rgba(0,0,0,.35); animation: gx119-pop .2s ease-out; }
  @keyframes gx119-pop { from { opacity: 0; transform: scale(.94); } to { opacity: 1; transform: none; } }
  .gx-bm119 .fc { position: absolute; top: -50px; left: 50%; transform: translateX(-50%); width: 100px; height: 100px; border-radius: 999px; overflow: hidden; background: var(--card2, var(--bg)); border: 3px solid var(--card); display: flex; align-items: flex-end; justify-content: center; }
  .gx-bm119 .fc img { width: 100%; height: 100%; object-fit: cover; border-radius: 0 !important; }
  .gx-bm119 .xx { position: absolute; top: 12px; right: 14px; font-size: 26px; line-height: 1; color: var(--mute); padding: 4px; }
  .gx-bm119 .nm { display: block; margin: 0 auto; font-size: 20px; font-weight: 700; text-align: center; }
  .gx-bm119 .sb { text-align: center; font-size: 14px; color: var(--mute); margin: 4px 0 14px; }
  .gx-bm119 .tb { display: grid; grid-template-columns: minmax(0, 1fr) 64px 40px 64px; font-variant-numeric: tabular-nums; }
  .gx-bm119 .tb > div { padding: 12px 6px; border-top: 1px solid var(--line); font-size: 15px; }
  .gx-bm119 .tb > div:nth-child(4n+1) { padding-left: 18px; }
  .gx-bm119 .tb > div:nth-child(4n) { padding-right: 18px; text-align: right; font-weight: 600; }
  .gx-bm119 .tb > div:nth-child(4n+2), .gx-bm119 .tb > div:nth-child(4n+3) { text-align: center; color: var(--ink2); }
  .gx-bm119 .tb .h { font-size: 11px; font-weight: 700; letter-spacing: .04em; text-transform: uppercase; color: var(--ink) !important; }
  .gx-bm119 .tb .t { font-weight: 700; background: var(--card2, var(--bg)); }
  .gx-bm119 .tb .t:nth-child(4n+1) { border-bottom-left-radius: 16px; }
  .gx-bm119 .tb .t:nth-child(4n) { border-bottom-right-radius: 16px; }
  .gx-bm119 .em { padding: 14px 18px 18px; text-align: center; color: var(--mute); font-size: 14px; border-top: 1px solid var(--line); }
</style>'''

HELPERS = r'''// ---------- change 119: box score pop-up for one player on one day (install.py) ----------
const GX_NICK119 = { ANA: "Ducks", BOS: "Bruins", BUF: "Sabres", CAR: "Hurricanes", CBJ: "Blue Jackets", CGY: "Flames", CHI: "Blackhawks", COL: "Avalanche", DAL: "Stars", DET: "Red Wings", EDM: "Oilers", FLA: "Panthers", LA: "Kings", LAK: "Kings", MIN: "Wild", MTL: "Canadiens", NJ: "Devils", NJD: "Devils", NSH: "Predators", NYI: "Islanders", NYR: "Rangers", OTT: "Senators", PHI: "Flyers", PIT: "Penguins", SEA: "Kraken", SJ: "Sharks", SJS: "Sharks", STL: "Blues", TB: "Lightning", TBL: "Lightning", TOR: "Maple Leafs", UTA: "Mammoth", VAN: "Canucks", VGK: "Golden Knights", WPG: "Jets", WSH: "Capitals" };
function GxBox119({ s, p, onClose }) {
  useEffect(() => { const k = (e) => { if (e.key === "Escape") onClose(); }; window.addEventListener("keydown", k); return () => window.removeEventListener("keydown", k); }, []);
  const sc = Object.assign({}, typeof SC0 === "object" ? SC0 : {}, (s && s.sc) || {});
  const x = typeof pStat === "function" ? pStat(p, p.dt) : null;
  const g = gameOf(p.t, p.dt);
  const sub = dayLabel(p.dt).replace(",", "") + (g ? (g.h ? " vs. " : " @ ") + (GX_NICK119[g.o] || g.o) : "");
  const rows = [];
  const add = (l, w, n) => { if (n && w) rows.push([l, w, n, n * w]); };
  let est = 0;
  if (x && x.sv != null) {
    const w = x.dec === "W" ? 1 : 0, o = x.dec === "O" ? 1 : 0, so = w && x.ga === 0 ? 1 : 0;
    add("Wins", sc.W, w); add("Overtime losses", sc.OTL, o); add("Saves", sc.SV, x.sv || 0); add("Goals against", sc.GA, x.ga || 0); add("Shutouts", sc.SO, so);
  } else if (x) {
    add("Goals", sc.G, x.g || 0); add("Assists", sc.A, x.a || 0); add("Plus/minus", sc.PM, x.pm || 0); add("Shots on goal", sc.SOG, x.sog || 0);
    add("Hits", sc.HIT, x.hit || 0); add("Blocked shots", sc.BLK, x.blk || 0);
  }
  rows.forEach((r) => { est += r[3]; });
  const real = p.st && p.a != null ? p.a : null;
  if (x && x.sv == null) {
    // ESPN counts power play points; the box score only has power play goals, so the rest comes from ESPN's total
    let left = real != null ? real - est : (x.ppg || 0) * (sc.PPP || 0), ppp = x.ppg || 0;
    if (real != null && sc.PPP) { const k = Math.round(left / sc.PPP); if (k > 0 && Math.abs(left - k * sc.PPP) < 0.05) { ppp = k; } }
    if (ppp && sc.PPP) { add("Power Play Points", sc.PPP, ppp); est += ppp * sc.PPP; left = real != null ? real - est : 0; }
    if (real != null && Math.abs(real - est) >= 0.05) rows.push(["Other", null, null, real - est]);
  } else if (x && real != null && Math.abs(real - est) >= 0.05) rows.push(["Other", null, null, real - est]);
  const total = real != null ? real : x ? est : null;
  const num = (v) => (Math.round(v * 10) / 10).toString();
  const box = (
    <div className="gx-bm119" onClick={onClose} role="dialog" aria-label={p.n + " box score"}>
      <div className="cd" onClick={(e) => e.stopPropagation()}>
        <div className="fc"><GxFace p={p} size={100} /></div>
        <button type="button" className="xx" aria-label="Close" onClick={onClose}>{"×"}</button>
        <button type="button" className="nm hover:underline" onClick={() => { onClose(); if (window.__NAV) window.__NAV.player(p); }}>{p.n}</button>
        <div className="sb">{sub}</div>
        {p.st && x ? (
          <div className="tb">
            <div className="h">Scoring category</div><div className="h">Pts per</div><div className="h">#</div><div className="h">Score</div>
            {rows.map((r, i) => <React.Fragment key={i}><div>{r[0]}</div><div>{r[1] == null ? "" : num(r[1])}</div><div>{r[2] == null ? "" : r[2]}</div><div>{f1(r[3])}</div></React.Fragment>)}
            {!rows.length ? <><div style={{ color: "var(--mute)" }}>No points this game</div><div></div><div></div><div></div></> : null}
            <div className="t">{p.st === "F" ? "Total" : "Total so far"}</div><div className="t"></div><div className="t"></div><div className="t">{f1(total || 0)}</div>
          </div>
        ) : (
          <div className="em">{p.st ? "No stats yet for this game." : "Has not played yet."}<div style={{ marginTop: 6, color: "var(--ink)", fontWeight: 600 }}>{"Projected " + f1(p.x || 0) + " FPTS"}</div></div>
        )}
      </div>
    </div>
  );
  return ReactDOM.createPortal(box, document.body);
}
'''


def change(t):
    t = lit(t, "119: styles", "</style>", NEW_CSS, "change 119 (install.py)")
    t = lit(t, "119: helpers", ROOT, HELPERS + ROOT, "change 119: box score pop-up")
    # no box under the row any more
    t = lit(t, "119: no box under the row",
            '          {[p, q].filter((z) => z && bx118 === z.id + "|" + z.dt).map((z) => <GxBox118 key={"bx" + z.id} p={z} />)}\n',
            "", "gx119-popup")
    # pop-up for the tapped player
    t = lit(t, "119: pop-up", "        {sit(x, a)}{sit(y, b)}\n",
            '        {sit(x, a)}{sit(y, b)}\n        {(() => { /* gx119-popup */ const z = bx118 ? rows.map((r) => [r[1], r[2]]).flat().find((v) => v && v.id + "|" + v.dt === bx118) : null; return z ? <GxBox119 s={s} p={z} onClose={() => setBx118("")} /> : null; })()}\n',
            "gx119-popup")
    return t


edit(APP, change)
