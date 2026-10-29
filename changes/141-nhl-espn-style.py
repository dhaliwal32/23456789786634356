# changes/141-nhl-espn-style.py - NHL scores like ESPN. Phone: sheet with goal cards (square faces, assists one per line, green bar for the left team's players, blue for the right team's), no counters, background stays still while the sheet scrolls, tap only opens it. Game view: Game (scoring by period), Fantasy (only the two teams in the matchup on screen), each NHL team (forwards, then defence, then goalies). Laptop: goal tracker (one goal at a time with arrows) and NHL scoreboard with both teams' fantasy points per game in a column beside Matchup.

NEW_CSS = r'''  /* change 141 (install.py) */
  .gx-sh141 { position: fixed; inset: 0; z-index: 75; background: rgba(0,0,0,.55); display: flex; align-items: flex-end; justify-content: center; animation: gx139-in .22s ease; }
  .gx-sh141 .pn { width: min(760px, 100%); height: 92vh; display: flex; flex-direction: column; background: var(--bg); color: var(--ink); border-radius: 18px 18px 0 0; overflow: hidden; padding-bottom: env(safe-area-inset-bottom); animation: gx139-up .28s cubic-bezier(.2, .8, .2, 1); }
  .gx-sh141.out { animation: gx139-out .22s ease forwards; }
  .gx-sh141.out .pn { animation: gx139-down .22s ease-in forwards; }
  .gx-sh141 .grab { width: 40px; height: 5px; border-radius: 9px; background: var(--line2, var(--line)); margin: 8px auto 0; flex: none; }
  .gx-sh141 .hd { display: flex; align-items: center; gap: 10px; padding: 12px 16px; border-bottom: 1px solid var(--line); flex: none; touch-action: none; }
  .gx-sh141 .hd .tt { display: flex; align-items: center; gap: 10px; font-size: 18px; font-weight: 700; }
  .gx-sh141 .hd.c .tt { flex: 1; justify-content: center; }
  .gx-sh141 .hd .ic { font-size: 30px; line-height: 1; color: var(--ink); width: 28px; text-align: left; }
  .gx-sh141 .hd .xx { margin-left: auto; font-size: 30px; line-height: 1; color: var(--ink); width: 28px; text-align: right; }
  .gx-sh141 .seg2 { display: flex; margin: 12px 16px; padding: 3px; border-radius: 999px; background: var(--card2, var(--card)); flex: none; }
  .gx-sh141 .seg2 button { flex: 1; padding: 8px 0; border-radius: 999px; font-size: 15px; font-weight: 600; color: var(--mute); }
  .gx-sh141 .seg2 button.on { background: var(--card); color: var(--ink); box-shadow: 0 1px 3px rgba(0,0,0,.25); }
  .gx-sh141 .bd { flex: 1; overflow-y: auto; -webkit-overflow-scrolling: touch; overscroll-behavior: contain; touch-action: pan-y; padding-bottom: 20px; }
  .gx-gt141 { display: flex; flex-direction: column; gap: 12px; padding: 0 12px; }
  .gx-gt141 .cd { background: var(--card); border-radius: 12px; overflow: hidden; border-left: 4px solid transparent; }
  .gx-gt141 .cd.me { border-left-color: #8bd450; }
  .gx-gt141 .cd.op { border-left-color: #8fb6e6; }
  .gx-gt141 .top { display: flex; align-items: flex-end; gap: 12px; padding: 6px 14px 0 10px; border-bottom: 1px solid var(--line); }
  .gx-gt141 .ph { width: 64px; height: 50px; flex: none; overflow: hidden; display: flex; align-items: flex-end; justify-content: center; }
  .gx-gt141 .ph img { width: 64px; height: auto; display: block; }
  .gx-gt141 .tx { padding: 6px 0 10px; min-width: 0; }
  .gx-gt141 .who { font-size: 15px; font-weight: 600; }
  .gx-gt141 .when { font-size: 13px; color: var(--mute); margin-top: 2px; }
  .gx-gt141 .as { display: grid; grid-template-columns: 76px 1fr; gap: 4px 0; padding: 10px 14px 12px 10px; font-size: 14px; }
  .gx-gt141 .as > span:first-child { color: var(--mute); }
  .gx-gt141 .as .ls > div + div { margin-top: 4px; }
  .gx-gv141 { display: flex; align-items: center; justify-content: center; gap: 0; padding: 14px 16px; border-bottom: 1px solid var(--line); flex: none; }
  .gx-gv141 .tms { display: flex; flex-direction: column; gap: 6px; padding-right: 14px; border-right: 1px solid var(--line); min-width: 190px; }
  .gx-gv141 .tr { display: flex; align-items: center; gap: 10px; font-size: 17px; }
  .gx-gv141 .tr .nm { flex: 1; }
  .gx-gv141 .tr b { font-weight: 500; min-width: 20px; text-align: right; }
  .gx-gv141 .tr i { display: block; width: 7px; height: 10px; }
  .gx-gv141 .tr i.ar { width: 0; height: 0; border-top: 5px solid transparent; border-bottom: 5px solid transparent; border-right: 7px solid var(--ink); }
  .gx-gv141 .tr.lo .nm, .gx-gv141 .tr.lo b { color: var(--mute); }
  .gx-gv141 .st { padding-left: 14px; font-size: 14px; min-width: 80px; }
  .gx-gv141 .st.lv { color: var(--bad); font-weight: 600; }
  .gx-tb141 { display: flex; justify-content: center; gap: 28px; border-bottom: 1px solid var(--line); flex: none; }
  .gx-tb141 button { padding: 12px 2px 10px; font-size: 14px; font-weight: 600; letter-spacing: .04em; color: var(--mute); border-bottom: 3px solid transparent; }
  .gx-tb141 button.on { color: var(--ink); border-color: var(--accent); }
  .gx-sc141 { padding: 6px 0 8px; }
  .gx-sc141 .h1 { padding: 16px 16px 8px; font-size: 13px; font-weight: 700; letter-spacing: .04em; }
  .gx-sc141 .ph { display: grid; grid-template-columns: 1fr 56px 56px; padding: 10px 16px 8px; font-size: 12px; font-weight: 700; letter-spacing: .04em; border-bottom: 1px solid var(--line); }
  .gx-sc141 .ph span + span, .gx-sc141 .gr > span:nth-child(n+3) { text-align: center; }
  .gx-sc141 .gr { display: grid; grid-template-columns: 56px 1fr 56px 56px; align-items: center; padding: 12px 16px; border-bottom: 1px solid var(--line); font-size: 15px; }
  .gx-sc141 .gr small { display: block; color: var(--mute); font-size: 14px; }
  .gx-sc141 .gr .as { color: var(--mute); }
  .gx-bt141 { padding: 0 12px; }
  .gx-bt141 .tn { display: flex; align-items: center; gap: 10px; padding: 16px 4px 10px; font-size: 18px; font-weight: 600; }
  .gx-bt141 .t { display: grid; grid-template-columns: minmax(0, 1fr) 52px 28px 28px 34px 50px; font-size: 15px; font-variant-numeric: tabular-nums; background: var(--card); border-radius: 10px; overflow: hidden; margin-bottom: 14px; }
  .gx-bt141 .t.g { grid-template-columns: minmax(0, 1fr) 56px 28px 32px 32px 50px; }
  .gx-bt141 .t > div { padding: 9px 6px; border-top: 1px solid var(--line); text-align: right; white-space: nowrap; }
  .gx-bt141 .t > div.n { text-align: left; padding-left: 14px; overflow: hidden; text-overflow: ellipsis; font-weight: 500; }
  .gx-bt141 .t > div.h { border-top: 0; font-size: 12px; font-weight: 700; letter-spacing: .03em; color: var(--ink); }
  .gx-bt141 .t > div.m { color: var(--mute); }
  .gx-bt141 .t > div.f { font-weight: 700; padding-right: 14px; }
  .gx-bt141 .t > div.n.me { box-shadow: inset 4px 0 0 #8bd450; }
  .gx-bt141 .t > div.n.op { box-shadow: inset 4px 0 0 #8fb6e6; }
  .gx-bt141 .t .ow { font-size: 11px; color: var(--mute); margin-left: 6px; font-weight: 500; }
  .gx-lg141 { display: flex; justify-content: center; gap: 14px; padding: 6px 0 10px; font-size: 13px; }
  .gx-lg141 span { display: inline-flex; align-items: center; gap: 5px; }
  .gx-lg141 i, .gx-sd141 .lg i, .gx-sd141 .fp i { display: inline-block; width: 11px; height: 11px; }
  .gx-lg141 .me, .gx-sd141 .me { color: #8bd450; }
  .gx-lg141 .op, .gx-sd141 .op { color: #8fb6e6; }
  .gx-lg141 i.me, .gx-sd141 i.me { background: #8bd450; }
  .gx-lg141 i.op, .gx-sd141 i.op { background: #8fb6e6; }
  .gx-sd141 .bx { background: var(--card); border-radius: 12px; box-shadow: inset 0 0 0 1px var(--line); margin-bottom: 14px; overflow: hidden; }
  .gx-sd141 .bh { display: flex; align-items: center; gap: 10px; padding: 12px 14px; border-bottom: 1px solid var(--line); font-size: 17px; }
  .gx-sd141 .bh .r { margin-left: auto; font-size: 13px; color: var(--ink); }
  .gx-sd141 .lg { margin-left: auto; display: flex; gap: 12px; font-size: 12px; color: var(--ink) !important; }
  .gx-sd141 .lg span { display: inline-flex; align-items: center; gap: 5px; }
  .gx-sd141 .gs { display: flex; align-items: center; gap: 6px; padding: 12px 8px 12px 4px; }
  .gx-sd141 .gs .ar { font-size: 24px; color: var(--accent); width: 22px; text-align: center; }
  .gx-sd141 .gs .ar:disabled { color: var(--line2, var(--line)); }
  .gx-sd141 .gs .md { flex: 1; min-width: 0; }
  .gx-sd141 .gs .tp { display: flex; align-items: center; gap: 10px; }
  .gx-sd141 .gs .fc { width: 46px; height: 46px; border-radius: 999px; overflow: hidden; background: var(--line); flex: none; }
  .gx-sd141 .gs .fc img { width: 100%; height: 100%; object-fit: cover; }
  .gx-sd141 .gs .nm { color: var(--accent); font-size: 14px; }
  .gx-sd141 .gs .sm { font-size: 12px; color: var(--mute); line-height: 1.3; }
  .gx-sd141 .gs .mb { margin-left: auto; background: var(--card2, var(--bg)); border-radius: 6px; padding: 5px 10px; font-size: 13px; display: grid; grid-template-columns: 18px 34px 18px; gap: 2px 4px; align-items: center; }
  .gx-sd141 .gs .mb b { font-weight: 500; text-align: right; }
  .gx-sd141 .gs .asl { font-size: 13px; color: var(--mute); margin-top: 8px; }
  .gx-sd141 .gs .asl button { color: var(--accent); }
  .gx-sd141 .dt { padding: 12px 14px 6px; font-weight: 600; }
  .gx-sd141 .gm { display: flex; align-items: center; width: 100%; text-align: left; padding: 10px 14px; border-top: 1px solid var(--line); }
  .gx-sd141 .gm .tms { width: 150px; flex: none; display: flex; flex-direction: column; gap: 6px; padding-right: 10px; border-right: 1px solid var(--line); }
  .gx-sd141 .gm .tr { display: flex; align-items: center; gap: 8px; font-size: 15px; }
  .gx-sd141 .gm .tr .nm { flex: 1; min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  .gx-sd141 .gm .tr i { display: block; width: 6px; height: 9px; }
  .gx-sd141 .gm .tr i.ar { width: 0; height: 0; border-top: 4.5px solid transparent; border-bottom: 4.5px solid transparent; border-right: 6px solid var(--ink); }
  .gx-sd141 .gm .tr.lo .nm, .gx-sd141 .gm .tr.lo b { color: var(--mute); }
  .gx-sd141 .gm .st { width: 64px; flex: none; padding-left: 10px; font-size: 12px; font-weight: 600; }
  .gx-sd141 .gm .st.lv { color: var(--bad); }
  .gx-sd141 .gm .fp { flex: 1; min-width: 0; padding-left: 10px; border-left: 1px solid var(--line); font-size: 12px; line-height: 1.7; }
  .gx-sd141 .gm .fp b { font-weight: 700; }
  .gx-mu141 > .sd { display: none; }
  @media (min-width: 1100px) {
    .gx-mu141 { display: grid; grid-template-columns: minmax(0, 1fr) 370px; gap: 18px; align-items: start; }
    .gx-mu141 > .sd { display: block; position: sticky; top: 72px; max-height: calc(100vh - 84px); overflow-y: auto; }
    .gx-ib141 { display: none !important; }
  }
  @media (max-width: 640px) {
    .gx-ib141 { display: none !important; }
    .gx-sh141 .pn { width: 100%; }
  }
</style>'''

HELPERS = r'''// ---------- change 141: NHL scores like ESPN (install.py) ----------
const GX_CITY141 = { ANA: "Anaheim", BOS: "Boston", BUF: "Buffalo", CAR: "Carolina", CBJ: "Columbus", CGY: "Calgary", CHI: "Chicago", COL: "Colorado", DAL: "Dallas", DET: "Detroit", EDM: "Edmonton", FLA: "Florida", LA: "Los Angeles", MIN: "Minnesota", MTL: "Montreal", NJ: "New Jersey", NSH: "Nashville", NYI: "New York", NYR: "New York", OTT: "Ottawa", PHI: "Philadelphia", PIT: "Pittsburgh", SEA: "Seattle", SJ: "San Jose", STL: "St. Louis", TB: "Tampa Bay", TOR: "Toronto", UTA: "Utah", VAN: "Vancouver", VGK: "Vegas", WPG: "Winnipeg", WSH: "Washington" };
const GX_PER141 = { 1: "FIRST PERIOD", 2: "SECOND PERIOD", 3: "THIRD PERIOD" };
const gxNick141 = (ab) => (typeof GX_NICK119 !== "undefined" && GX_NICK119[gxAb131(ab)]) || gxAb131(ab);
const gxFull141 = (ab) => { const t = gxAb131(ab); return (GX_CITY141[t] ? GX_CITY141[t] + " " : "") + gxNick141(t); };
const gxNm141 = (q) => (q && q.name && q.name.default) || [(((q || {}).firstName || {}).default || ""), (((q || {}).lastName || {}).default || "")].join(" ").trim();
const gxFtAb141 = (s, id) => (id ? gxTag131(s, { ft: id }) : "");
const gxHs141 = (x, p) => (x && (x.headshot || x.mugshot)) || (p && String(p.id || "")[0] === "e" ? "https://a.espncdn.com/i/headshots/nhl/players/full/" + String(p.id).slice(1) + ".png" : "");
// a page-wide lock that keeps the page behind the sheet still on phones
function gxLock141(on) {
  const b = document.body;
  if (on) { const y = window.scrollY || 0; b.dataset.gx141 = String(y); b.style.position = "fixed"; b.style.top = -y + "px"; b.style.left = "0"; b.style.right = "0"; b.style.width = "100%"; b.style.overflow = "hidden"; }
  else if (b.dataset.gx141 != null) { const y = +b.dataset.gx141 || 0; delete b.dataset.gx141; b.style.position = ""; b.style.top = ""; b.style.left = ""; b.style.right = ""; b.style.width = ""; b.style.overflow = ""; window.scrollTo(0, y); }
}
function GxNhl141({ s, a, b, tA, tB, side }) {
  const [open, setOpen] = useState(false);
  const [out, setOut] = useState(false);
  const [tab, setTab] = useState("sb");
  const [gid, setGid] = useState(null);
  const [gt, setGt] = useState("game");
  const [gi, setGi] = useState(null);
  const [, bump] = useState(0);
  const dragY = React.useRef(null);
  useEffect(() => { const id = setInterval(() => bump((x) => x + 1), 15000); return () => clearInterval(id); }, []);
  const close = () => { setOut(true); setTimeout(() => { setOut(false); setOpen(false); setGid(null); }, 220); };
  useEffect(() => {
    if (!open) return undefined;
    const k = (e) => { if (e.key === "Escape") close(); };
    window.addEventListener("keydown", k);
    gxLock141(true);
    return () => { window.removeEventListener("keydown", k); gxLock141(false); };
  }, [open]);
  const J = window.__NHLNOW || {}, games = (J.games || []).slice();
  const live = (g) => g.gameState === "LIVE" || g.gameState === "CRIT", fin = (g) => g.gameState === "FINAL" || g.gameState === "OFF", pre = (g) => !(live(g) || fin(g));
  const BX = (window.__BX131 = window.__BX131 || {}), L = (window.__LD131 = window.__LD131 || {});
  const box = (id) => (typeof G120 !== "undefined" && G120.box[id] && G120.box[id].bx) || (BX[id] && BX[id].bx) || null;
  useEffect(() => {
    if (!open || !gid) return undefined;
    const g = games.find((x) => x.id === gid);
    const need = !box(gid) || (g && live(g) && (!BX[gid] || Date.now() - BX[gid].at > 30000) && !(typeof G120 !== "undefined" && G120.box[gid]));
    if (!need || (g && pre(g))) return undefined;
    let dead = false;
    fetch("https://api-web.nhle.com/v1/gamecenter/" + gid + "/boxscore").then((r) => (r.ok ? r.json() : null)).then((bx) => { if (bx && !dead) { BX[gid] = { bx, at: Date.now() }; bump((x) => x + 1); } }).catch(() => {});
    return () => { dead = true; };
  }, [open, gid, J]);
  const wantGoals = side || (open && (tab === "gt" || gid));
  useEffect(() => {
    if (!wantGoals) return undefined;
    let dead = false;
    games.filter((g) => (live(g) || fin(g)) && !g.goals).forEach((g) => {
      const c = L[g.id];
      if (c && (fin(g) || Date.now() - c.at < 45000)) return;
      fetch("https://api-web.nhle.com/v1/gamecenter/" + g.id + "/landing").then((r) => (r.ok ? r.json() : null)).then((js) => {
        if (!js || dead) return;
        const goals = [];
        (((js.summary || {}).scoring) || []).forEach((p) => (p.goals || []).forEach((x) => goals.push({ ...x, periodDescriptor: p.periodDescriptor })));
        L[g.id] = { at: Date.now(), goals }; bump((x) => x + 1);
      }).catch(() => {});
    });
    return () => { dead = true; };
  }, [wantGoals, J]);
  const status = (g) => (live(g) ? ((g.clock || {}).inIntermission ? gxPer131(g.periodDescriptor) + " int." : gxPer131(g.periodDescriptor) + " - " + ((g.clock || {}).timeRemaining || "")) : fin(g) ? "Final" + (((g.periodDescriptor || {}).periodType || "REG") !== "REG" ? "/" + gxPer131(g.periodDescriptor) : "") : g.startTimeUTC ? new Date(g.startTimeUTC).toLocaleTimeString([], { hour: "numeric", minute: "2-digit" }) : "");
  const order = (g) => (live(g) ? 0 : pre(g) ? 1 : 2);
  games.sort((x, y) => order(x) - order(y) || String(x.startTimeUTC).localeCompare(String(y.startTimeUTC)));
  const who = (p) => (p && p.ft === a ? "me" : p && p.ft === b ? "op" : "");
  const go = (p) => { if (p && window.__NAV) { if (open) close(); window.__NAV.player(p); } };
  const pBtn = (p, label, k, cls) => (p ? <button key={k} type="button" className={"hover:underline text-left " + (cls || "")} style={{ fontWeight: "inherit" }} onClick={(e) => { e.stopPropagation(); go(p); }}>{label}</button> : <React.Fragment key={k}>{label}</React.Fragment>);
  // every goal today, with who scored and assisted
  const goals = [];
  games.forEach((g) => (g.goals || (L[g.id] || {}).goals || []).forEach((x, i) => {
    const tm = gxAb131(x.teamAbbrev && x.teamAbbrev.default ? x.teamAbbrev.default : x.teamAbbrev), n = gxNm141(x), p = gxFind131(tm, null, n);
    const as = (x.assists || []).map((q) => { const an = gxNm141(q), ap = gxFind131(tm, null, an); return { an, ap, at: gxTag131(s, ap) }; });
    const w = Date.parse(x.wc || ""), m = String(x.timeInPeriod || "0:0").split(":"), pn = ((x.periodDescriptor || {}).number || 1) - 1;
    const at = !isNaN(w) ? w : (Date.parse(g.startTimeUTC || "") || 0) + (pn * 1200 + (+m[0] || 0) * 60 + (+m[1] || 0)) * 1600 + pn * 1080e3;
    const k = [who(p)].concat(as.map((q) => who(q.ap)));
    goals.push({ g, x, i, tm, n, p, tag: gxTag131(s, p), as, at, mk: k.indexOf("me") >= 0 ? "me" : k.indexOf("op") >= 0 ? "op" : "" });
  }));
  goals.sort((x, y) => x.at - y.at);
  const sc = (r) => gxAb131((r.g.awayTeam || {}).abbrev) + " " + (r.x.awayScore != null ? r.x.awayScore : "") + ", " + gxAb131((r.g.homeTeam || {}).abbrev) + " " + (r.x.homeScore != null ? r.x.homeScore : "");
  const teamRow = (T, win, lose, done) => <div className={"tr" + (done && lose ? " lo" : "")}><TeamLogo t={gxAb131(T.abbrev)} size={side ? 20 : 24} /><span className="nm">{gxNick141(T.abbrev)}</span><b>{T.score == null ? "" : T.score}</b><i className={done && win ? "ar" : ""}></i></div>;
  const rows2 = (g) => { const A = g.awayTeam || {}, H = g.homeTeam || {}, p0 = pre(g), done = fin(g), aw = !p0 && +A.score > +H.score, hw = !p0 && +H.score > +A.score; return [teamRow(p0 ? { ...A, score: null } : A, aw, hw, done), teamRow(p0 ? { ...H, score: null } : H, hw, aw, done)]; };
  const fpOf = (day, t) => ((day && day.start) || []).reduce((z, p) => z + (p.t === t && p.st ? +(p.a || 0) : 0), 0);
  const openGame = (id) => { setGid(id); setGt("game"); setOpen(true); };

  // ---------- laptop column ----------
  if (side) {
    const n = goals.length, idx = gi == null || gi >= n ? n - 1 : gi, r = n ? goals[idx] : null;
    const pos = r && r.p ? r.p.p : "";
    const dl = (() => { try { return new Date().toLocaleDateString([], { weekday: "long", month: "long", day: "numeric" }); } catch (e) { return ""; } })();
    const abA = gxFtAb141(s, a), abB = gxFtAb141(s, b);
    return (
      <div className="gx-sd141">
        <div className="bx">
          <div className="bh"><span>Goal Tracker</span><span className="r">{n ? "Goal " + (idx + 1) + " of " + n : ""}</span></div>
          {r ? (
            <div className="gs">
              <button type="button" className="ar" aria-label="Earlier goal" disabled={idx <= 0} onClick={() => setGi(idx - 1)}>{"\u2039"}</button>
              <div className="md">
                <div className="tp">
                  <span className="fc">{gxHs141(r.x, r.p) ? <img src={gxHs141(r.x, r.p)} alt="" onError={(e) => { e.currentTarget.style.display = "none"; }} /> : null}</span>
                  <div className="min-w-0"><div className="nm">{pBtn(r.p, shortN(r.n), "s")}</div><div className="sm">{r.tm + (pos ? " " + pos : "")}</div><div className="sm">{(r.x.timeInPeriod || "") + " - " + gxPer131(r.x.periodDescriptor)}</div></div>
                  <div className="mb"><TeamLogo t={gxAb131((r.g.awayTeam || {}).abbrev)} size={16} /><span>{gxAb131((r.g.awayTeam || {}).abbrev)}</span><b>{r.x.awayScore}</b><TeamLogo t={gxAb131((r.g.homeTeam || {}).abbrev)} size={16} /><span>{gxAb131((r.g.homeTeam || {}).abbrev)}</span><b>{r.x.homeScore}</b></div>
                </div>
                <div className="asl">Assists: {r.as.length ? r.as.map((q, k) => <React.Fragment key={k}>{k ? ", " : ""}{pBtn(q.ap, shortN(q.an), "a")}{q.at ? " (" + q.at + ")" : ""}</React.Fragment>) : "Unassisted"}</div>
              </div>
              <button type="button" className="ar" aria-label="Later goal" disabled={idx >= n - 1} onClick={() => setGi(idx + 1 >= n - 1 ? null : idx + 1)}>{"\u203a"}</button>
            </div>
          ) : <div className="em" style={{ padding: 14, color: "var(--mute)", fontSize: 13 }}>No goals yet today.</div>}
        </div>
        <div className="bx">
          <div className="bh"><span>NHL Scoreboard</span><span className="lg"><span><i className="me"></i>{teamName(s, a) && a === s.me ? "My Team" : abA}</span><span><i className="op"></i>{a === s.me ? "Opp Team" : abB}</span></span></div>
          <div className="dt">{dl}</div>
          {games.length ? games.map((g) => {
            const ta = gxAb131((g.awayTeam || {}).abbrev), th = gxAb131((g.homeTeam || {}).abbrev);
            return (
              <button key={g.id} type="button" className="gm" onClick={() => openGame(g.id)}>
                <div className="tms">{rows2(g)}</div>
                <div className={"st" + (live(g) ? " lv" : "")}>{status(g)}</div>
                <div className="fp"><div><b>{abA}:</b> {f1(fpOf(tA, ta) + fpOf(tA, th))} FPTS</div><div><b>{abB}:</b> {f1(fpOf(tB, ta) + fpOf(tB, th))} FPTS</div></div>
              </button>
            );
          }) : <div style={{ padding: 14, color: "var(--mute)", fontSize: 13 }}>No NHL games today.</div>}
        </div>
        {open ? GX_SHEET141() : null}
      </div>
    );
  }

  // ---------- the sheet (phone, and the game view from the laptop column) ----------
  function GX_SHEET141() {
    let body = null, head = null, extra = null;
    if (gid) {
      const g = games.find((x) => x.id === gid) || {}, bx = box(gid), rows = bx ? gxBoxRows131(bx, gid) : [];
      rows.forEach((q) => { q.p = gxFind131(q.t, q.no, q.n); q.tag = gxTag131(s, q.p); q.k = who(q.p); });
      const aw = gxAb131((g.awayTeam || {}).abbrev), hm = gxAb131((g.homeTeam || {}).abbrev);
      extra = <>
        <div className="gx-gv141"><div className="tms">{rows2(g)}</div><div className={"st" + (live(g) ? " lv" : "")}>{status(g)}</div></div>
        <div className="gx-tb141">{[["game", "GAME"], ["fan", "FANTASY"], ["awayTeam", aw], ["homeTeam", hm]].map(([k, l]) => <button key={k} type="button" className={gt === k ? "on" : ""} onClick={() => setGt(k)}>{l}</button>)}</div>
      </>;
      const table = (list, gl) => {
        if (!list.length) return null;
        const nm = (q) => <div key={"n" + q.id} className={"n " + q.k}>{pBtn(q.p, shortN(q.n), "p")}{gt === "fan" && q.tag ? <span className="ow">{q.tag}</span> : null}</div>;
        return gl ? (
          <div className="t g"><div className="h n">GOALIES</div><div className="h">MIN</div><div className="h">W</div><div className="h">GA</div><div className="h">SV</div><div className="h f">FPTS</div>
            {list.map((q) => [nm(q), <div key={"t" + q.id} className="m">{q.toi}</div>, <div key={"w" + q.id} className="m">{q.x.dec === "W" ? 1 : 0}</div>, <div key={"ga" + q.id} className="m">{q.x.ga}</div>, <div key={"sv" + q.id} className="m">{q.x.sv}</div>, <div key={"f" + q.id} className="f">{f1(q.fp)}</div>])}</div>
        ) : (
          <div className="t"><div className="h n">SKATERS</div><div className="h">TOI</div><div className="h">G</div><div className="h">A</div><div className="h">+/-</div><div className="h f">FPTS</div>
            {list.map((q) => [nm(q), <div key={"t" + q.id} className="m">{q.toi}</div>, <div key={"g" + q.id} className="m">{q.x.g}</div>, <div key={"a" + q.id} className="m">{q.x.a}</div>, <div key={"pm" + q.id} className="m">{q.x.pm}</div>, <div key={"f" + q.id} className="f">{f1(q.fp)}</div>])}</div>
        );
      };
      const legend = <div className="gx-lg141"><span className="me"><i className="me"></i>{a === s.me ? "My Player" : gxFtAb141(s, a)}</span><span className="op"><i className="op"></i>{a === s.me ? "Opponent's Player" : gxFtAb141(s, b)}</span></div>;
      if (gt === "game") {
        const gs = goals.filter((r) => r.g.id === gid), per = {};
        gs.forEach((r) => { const pd = r.x.periodDescriptor || {}, key = pd.periodType === "SO" ? 5 : pd.periodType === "OT" ? 4 : pd.number || 1; (per[key] = per[key] || []).push(r); });
        body = gs.length ? <div className="gx-sc141"><div className="h1">SCORING</div>{Object.keys(per).sort((x, y) => x - y).map((k) => (
          <React.Fragment key={k}>
            <div className="ph"><span>{GX_PER141[k] || (+k === 4 ? "OVERTIME" : "SHOOTOUT")}</span><span>{aw}</span><span>{hm}</span></div>
            {per[k].map((r) => <div key={r.i} className="gr"><span><TeamLogo t={r.tm} size={26} /></span><span><small>{r.x.timeInPeriod}</small>Goal: {pBtn(r.p, shortN(r.n), "s")}<small className="as">{r.as.length ? "(" : ""}{r.as.map((q, j) => <React.Fragment key={j}>{j ? ", " : ""}{pBtn(q.ap, shortN(q.an), "a")}</React.Fragment>)}{r.as.length ? ")" : "Unassisted"}</small></span><span>{r.x.awayScore}</span><span>{r.x.homeScore}</span></div>)}
          </React.Fragment>
        ))}</div> : <div className="em" style={{ padding: 16, color: "var(--mute)" }}>{pre(g) ? "Not started yet." : "No goals yet."}</div>;
      } else if (!bx) {
        body = <div style={{ padding: 16, color: "var(--mute)" }}>{pre(g) ? "Not started yet." : "Loading..."}</div>;
      } else if (gt === "fan") {
        const list = rows.filter((q) => q.k).sort((x, y) => (x.k === y.k ? y.fp - x.fp : x.k === "me" ? -1 : 1));
        body = <div className="gx-bt141">{list.length ? <>{table(list.filter((q) => !q.g), false)}{table(list.filter((q) => q.g), true)}</> : <div style={{ padding: 16, color: "var(--mute)" }}>No players from this matchup in this game.</div>}{legend}</div>;
      } else {
        const list = rows.filter((q) => q.side === gt), T = gt === "awayTeam" ? aw : hm;
        body = <div className="gx-bt141"><div className="tn"><TeamLogo t={T} size={26} />{gxFull141(T)}</div>{table(list.filter((q) => !q.g), false)}{table(list.filter((q) => q.g), true)}{legend}</div>;
      }
      head = <div className="hd c" onTouchStart={(e) => { dragY.current = e.touches[0].clientY; }} onTouchEnd={(e) => { const y0 = dragY.current; dragY.current = null; if (y0 != null && e.changedTouches[0].clientY - y0 > 70) close(); }}><button type="button" className="ic" aria-label="Back" onClick={() => setGid(null)}>{"\u2039"}</button><span className="tt">{GX_IC140}NHL Scores</span><button type="button" className="xx" aria-label="Close" onClick={close}>{"\u00d7"}</button></div>;
    } else {
      head = <div className="hd" onTouchStart={(e) => { dragY.current = e.touches[0].clientY; }} onTouchEnd={(e) => { const y0 = dragY.current; dragY.current = null; if (y0 != null && e.changedTouches[0].clientY - y0 > 70) close(); }}><span className="tt">{GX_IC140}NHL Scores</span><button type="button" className="xx" aria-label="Close" onClick={close}>{"\u00d7"}</button></div>;
      extra = <div className="seg2"><button type="button" className={tab === "sb" ? "on" : ""} onClick={() => setTab("sb")}>Scoreboard</button><button type="button" className={tab === "gt" ? "on" : ""} onClick={() => setTab("gt")}>Goal Tracker</button></div>;
      if (tab === "sb") {
        body = games.length ? <div className="gx-gc140">{games.map((g) => (
          <button key={g.id} type="button" className="cd" onClick={() => openGame(g.id)}><div className="tms">{rows2(g)}</div><div className={"st" + (live(g) ? " lv" : pre(g) ? " pr" : "")}>{status(g)}</div></button>
        ))}</div> : <div style={{ padding: 16, color: "var(--mute)" }}>No NHL games today.</div>;
      } else {
        const list = goals.slice().reverse();
        body = list.length ? <div className="gx-gt141">{list.map((r) => (
          <div key={r.g.id + "-" + r.i} className={"cd " + r.mk}>
            <div className="top"><span className="ph">{gxHs141(r.x, r.p) ? <img src={gxHs141(r.x, r.p)} alt="" onError={(e) => { e.currentTarget.style.visibility = "hidden"; }} /> : <TeamLogo t={r.tm} size={34} />}</span>
              <div className="tx"><div className="who">{pBtn(r.p, r.n, "s")}{", " + r.tm}{r.tag ? " (" + r.tag + ")" : ""}</div><div className="when">{(r.x.timeInPeriod || "") + " " + gxPer131(r.x.periodDescriptor) + " Period - " + sc(r)}</div></div></div>
            <div className="as"><span>Assists:</span><div className="ls">{r.as.length ? r.as.map((q, k) => <div key={k}>{pBtn(q.ap, q.an, "a")}{q.at ? " (" + q.at + ")" : ""}</div>) : <div>Unassisted</div>}</div></div>
          </div>
        ))}</div> : <div style={{ padding: 16, color: "var(--mute)" }}>No goals yet today.</div>;
      }
    }
    return ReactDOM.createPortal(
      <div className={"gx-sh141" + (out ? " out" : "")} onClick={close} role="dialog" aria-label="NHL scores">
        <div className="pn" onClick={(e) => e.stopPropagation()}>
          <div className="grab"></div>
          {head}{extra}
          <div className="bd">{body}</div>
        </div>
      </div>, document.body);
  }

  // ---------- phone bar and the in-page bar (between phone and laptop widths) ----------
  const fb = (
    <div className="gx-fb140" role="button" aria-label="Open NHL scores" onClick={() => { setGid(null); setOpen(true); }}>
      <div className="grab"></div>
      <div className="rw">{GX_IC140}<b>NHL Scores</b><GxTick140 games={games} live={live} fin={fin} status={status} /></div>
    </div>
  );
  return (
    <>
      {!open ? ReactDOM.createPortal(fb, document.body) : null}
      <div className="gx-sp140"></div>
      <div className="gx-ns131 gx-ib141" style={{ marginTop: 18 }}>
        <button type="button" className="bar" onClick={() => { setGid(null); setOpen(true); }}><span>NHL Scores</span><span className="n">{games.length ? games.length + " games" : ""}</span><span className="sec-chev shut" style={{ marginLeft: 8 }}></span></button>
      </div>
      {open ? GX_SHEET141() : null}
    </>
  );
}
'''


def change(t):
    t = lit(t, "141: styles", "</style>", NEW_CSS, "change 141 (install.py)")
    t = lit(t, "141: helpers", ROOT, HELPERS + ROOT, "change 141: NHL scores like ESPN")
    t = lit(t, "141: today's lineups for the column",
            '  const mine = a === s.me;\n  return (\n    <div>\n',
            '  const mine = a === s.me;\n  const tI141 = dates.indexOf(today), tA141 = tI141 >= 0 ? A.days[tI141] : null, tB141 = tI141 >= 0 ? B.days[tI141] : null;\n  return (\n    <div className="gx-mu141"><div className="mn">\n',
            'const tI141 = dates.indexOf(today)')
    t = lit(t, "141: new scores in Matchup",
            '      <GxNhl131 s={s} opp={pairOpp || s.opp} />\n    </div>\n  );\n}',
            '      <GxNhl141 s={s} a={a} b={b} tA={tA141} tB={tB141} />\n    </div>\n    <div className="sd"><GxNhl141 s={s} a={a} b={b} tA={tA141} tB={tB141} side /></div>\n    </div>\n  );\n}',
            '<GxNhl141 s={s} a={a} b={b} tA={tA141} tB={tB141} side />')
    return t


edit(APP, change)
