# changes/238-roster-locker-room.py - Roster page: your own fantasy team as a locker room under the roster table

NEW_CSS = r'''  /* change 238 (install.py): your team's locker room on Roster */
  .gx-mr238 { margin-top: 4px; }
  .gx-mr238 .wn238 { position: relative; z-index: 2; display: flex; align-items: center; justify-content: center; gap: 10px; margin: 0 0 14px; padding: 0 10px; }
  .gx-mr238 .wn238 b { font-family: "Arial Black", "Helvetica Neue", Arial, sans-serif; font-weight: 900; font-size: 20px; letter-spacing: .1em; text-transform: uppercase; color: #fff; text-shadow: 0 0 10px rgba(255,255,255,.35), 0 2px 0 rgba(0,0,0,.6); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; min-width: 0; }
  .gx-mr238 .wn238 small { display: block; font-size: 10.5px; letter-spacing: .14em; color: rgba(255,255,255,.6); text-transform: uppercase; font-weight: 700; }
  .gx-mr238 .gx-fg224.gx-lt227.off { opacity: .55; }
  .gx-mr238 .gx-fg224.gx-lt227.lv { box-shadow: inset 0 10px 14px -10px rgba(0,0,0,.4), 0 0 0 1px color-mix(in srgb, var(--good) 70%, transparent), 0 0 18px 2px color-mix(in srgb, var(--good) 35%, transparent); }
  .gx-mr238 .gx-fg224.gx-lt227.lv::before { background: var(--good); box-shadow: 0 0 8px 2px var(--good); }
  .gx-mr238 .gx-fg224.gx-lt227 .ow227 { justify-content: center; }
  .gx-mr238 .gx-fg224.gx-lt227 .ow227 span { font-weight: 600; }
  .gx-mr238 .fl236 .lg236 img, .gx-mr238 .fl236 .lg236 > * { border-radius: 8px; }
  @media (max-width: 640px) { .gx-mr238 .wn238 b { font-size: 16px; } }
</style>'''

HELPERS = r'''// ---------- change 238: your own team's locker room on Roster (install.py) ----------
function gxNo238(p) {
  const L = window.LINES_DATA || { teams: {} }, T = (L.teams || {})[p.t] || {}, no = T.no || {};
  if (no[p.n] != null) return no[p.n];
  const k = nrm(p.n); for (const n in no) if (nrm(n) === k) return no[n];
  return null;
}
function gxTn238(p) {
  const td = todayISO(), g = p.ir ? null : gameOf(p.t, td);
  if (!g) return { k: "off", txt: p.ir ? "IR" : "No game" };
  const st = gState(p.t, td).s, opp = (g.h ? "v " : "@ ") + g.o;
  if (st === "P") return { k: "", txt: opp + " " + gameTime(g) };
  const sc = gScore(p.t, td), a = gxPdReal(p, td);
  const scr = sc && sc.my != null ? " " + sc.my + "-" + sc.op : "";
  return { k: st === "F" ? "" : "lv", txt: opp + scr + (st === "F" ? " F" : ""), pts: a };
}
function GxMyRoom238({ s }) {
  const mine = (s.players || []).filter((p) => p.ft === s.me);
  if (!mine.length) return null;
  const val = (p) => gxPgAvg(p, s.blend) || 0;
  const by = (f) => mine.filter(f).sort((a, b) => val(b) - val(a));
  const groups = [["F", by((p) => !p.ir && p.p !== "D" && p.p !== "G")], ["D", by((p) => !p.ir && p.p === "D")], ["G", by((p) => !p.ir && p.p === "G")], ["IR", by((p) => p.ir)]].filter((g) => g[1].length);
  const name = teamName(s, s.me) || "My team";
  const st = { "--rb": "#1b2330", "--rt": "var(--accent)", "--rn": "#ffffff", "--rg": "#ffffff", "--lc": "#e6f1ff" };
  const card = (p) => {
    const last = p.n.split(" ").slice(1).join(" ") || p.n, no = gxNo238(p), tn = gxTn238(p), isG = p.p === "G";
    return (
      <button key={p.id} type="button" className={"gx-fg224 gx-lt227 " + tn.k} aria-label={p.n} onClick={() => { if (window.__NAV) window.__NAV.player(p); }}>
        <div className="md jr231"><span className="pl232">{last}</span><GxJersey232 t={p.t} name={last} no={no} goalie={isG} /></div>
        <span className="sb227">{(no != null ? "#" + no + " \u00b7 " : "") + p.p + " \u00b7 " + p.t}</span>
        <span className="ow227"><span>{tn.txt}</span><b>{tn.pts != null ? f1(tn.pts) : f1(val(p))}</b></span>
      </button>
    );
  };
  const rows = [];
  groups.forEach(([lb, list]) => {
    for (let i = 0; i < list.length; i += 3) {
      const part = list.slice(i, i + 3);
      rows.push(<div key={lb + i} className={"row" + (part.length < 3 ? " c112" : "")} style={{ "--n": part.length }}><span className="lb">{i === 0 ? lb : ""}</span>{part.map(card)}</div>);
    }
  });
  return (
    <div className="gx-rk111 rm236 carbon gx-mr238" style={st} data-gx="238">
      <div className="rr236" aria-hidden="true">
        {[12, 38, 62, 88].map((x) => <span key={x} className="bm236" style={{ left: x + "%" }} />)}
        <div className="cl236"><i /><i /><i /><i /><i /></div>
        <div className="sr236" />
        <div className="fl236"><span className="lg236"><GxFtPic114 id={s.me} size={110} /></span></div>
      </div>
      <div className="wn238"><GxFtPic114 id={s.me} size={34} /><div className="min-w-0"><small>Your locker room</small><b>{name}</b></div></div>
      {rows}
    </div>
  );
}
'''

def change(t):
    t = lit(t, "238: styles", "</style>", NEW_CSS, "change 238 (install.py): your team's locker room")
    t = lit(t, "238: helpers", ROOT, HELPERS + ROOT, "change 238: your own team's locker room")
    t = lit(t, "238: show it on Roster",
            '<Today {...P} top103 /><MyTeam {...P} /></div>',
            '<Today {...P} top103 /><MyTeam {...P} /><GxMyRoom238 s={s} /></div>',
            '<GxMyRoom238 s={s} />')
    return t

edit(APP, change)
