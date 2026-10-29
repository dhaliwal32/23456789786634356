# changes/131-score-anim-nhl-scores.py - scores animate when they change (count up or down, green when going up, red when going down) on Matchup and the home page; new "NHL scores" panel on Matchup: today's scoreboard (live, final, upcoming), tap a game for its box score (Fantasy / away / home tabs with TOI, G, A, +/-, FPTS and goalies), and a Goal tracker with scorer, time, score and assists, each tagged with the fantasy team that owns him. The sync also saves each fantasy team's ESPN abbreviation for those tags

NEW_CSS = r'''  /* change 131 (install.py) */
  .gx-an131 { display: inline-block; transition: color .5s ease; font-variant-numeric: tabular-nums; }
  .gx-an131.up { color: var(--good) !important; animation: gx131-pop .6s ease-out; }
  .gx-an131.dn { color: var(--bad) !important; animation: gx131-pop .6s ease-out; }
  @keyframes gx131-pop { 0% { transform: scale(1); } 35% { transform: scale(1.06); } 100% { transform: scale(1); } }
  .gx-ns131 { margin-top: 12px; border-radius: 14px; background: var(--card); box-shadow: inset 0 0 0 1px var(--line); overflow: hidden; }
  .gx-ns131 .bar { display: flex; align-items: center; gap: 8px; width: 100%; padding: 12px 14px; font-weight: 600; text-align: left; }
  .gx-ns131 .bar .n { margin-left: auto; font-size: 12px; font-weight: 500; color: var(--mute); }
  .gx-ns131 .bar .lv { color: var(--bad); }
  .gx-ns131 .seg { display: flex; margin: 0 12px 10px; padding: 3px; border-radius: 999px; background: var(--card2, var(--bg)); }
  .gx-ns131 .seg button { flex: 1; padding: 7px 0; border-radius: 999px; font-size: 14px; color: var(--mute); }
  .gx-ns131 .seg button.on { background: var(--ink); color: var(--bg); font-weight: 600; }
  .gx-ns131 .gm { display: grid; grid-template-columns: 1fr auto; align-items: center; gap: 4px 12px; margin: 0 12px 10px; padding: 10px 12px; border-radius: 12px; background: var(--card2, var(--bg)); width: calc(100% - 24px); text-align: left; }
  .gx-ns131 .tm { display: flex; align-items: center; gap: 8px; font-size: 15px; }
  .gx-ns131 .tm b { margin-left: auto; font-size: 17px; font-variant-numeric: tabular-nums; }
  .gx-ns131 .gm .st { grid-row: 1 / span 2; grid-column: 2; padding-left: 12px; border-left: 1px solid var(--line); font-size: 13px; color: var(--mute); min-width: 74px; }
  .gx-ns131 .gm .st.lv { color: var(--bad); }
  .gx-ns131 .hd { display: flex; align-items: center; gap: 10px; padding: 4px 14px 10px; }
  .gx-ns131 .hd .bk { font-size: 22px; color: var(--mute); padding: 0 6px 0 0; }
  .gx-ns131 .tabs { display: flex; gap: 18px; padding: 0 14px; border-bottom: 1px solid var(--line); }
  .gx-ns131 .tabs button { padding: 8px 0; font-size: 13px; font-weight: 600; color: var(--mute); border-bottom: 2px solid transparent; }
  .gx-ns131 .tabs button.on { color: var(--ink); border-color: var(--accent); }
  .gx-ns131 .bx { display: grid; grid-template-columns: minmax(0, 1fr) 46px 26px 26px 34px 46px; gap: 0 4px; padding: 0 14px 10px; font-size: 14px; font-variant-numeric: tabular-nums; }
  .gx-ns131 .bx.g { grid-template-columns: minmax(0, 1fr) 50px 26px 30px 30px 46px; }
  .gx-ns131 .bx > div { padding: 8px 0; border-top: 1px solid var(--line); text-align: right; white-space: nowrap; }
  .gx-ns131 .bx > div.nm { text-align: left; overflow: hidden; text-overflow: ellipsis; }
  .gx-ns131 .bx > div.h { font-size: 11px; font-weight: 700; color: var(--mute); border-top: 0; }
  .gx-ns131 .bx > div.f { font-weight: 600; }
  .gx-ns131 .bx > div.me { box-shadow: inset 3px 0 0 var(--good); padding-left: 8px; }
  .gx-ns131 .own { font-size: 11px; color: var(--mute); margin-left: 4px; }
  .gx-ns131 .gl { margin: 0 12px 10px; padding: 10px 12px; border-radius: 12px; background: var(--card2, var(--bg)); }
  .gx-ns131 .gl .top { display: flex; gap: 10px; align-items: center; }
  .gx-ns131 .gl .top img { width: 46px; height: 46px; border-radius: 999px; object-fit: cover; background: var(--line); flex: none; }
  .gx-ns131 .gl .who { font-weight: 600; }
  .gx-ns131 .gl .when { font-size: 13px; color: var(--mute); }
  .gx-ns131 .gl .as { margin-top: 6px; padding-top: 6px; border-top: 1px solid var(--line); font-size: 13px; display: grid; grid-template-columns: 64px 1fr; color: var(--mute); }
  .gx-ns131 .gl .as span:last-child { color: var(--ink); }
  .gx-ns131 .em { padding: 6px 14px 14px; font-size: 13px; color: var(--mute); }
</style>'''

HELPERS = r'''// ---------- change 131: animated scores and the NHL scores panel (install.py) ----------
function GxAnimNum131({ v, d }) {
  const dd = d == null ? 1 : d;
  const [shown, setShown] = useState(v);
  const [fl, setFl] = useState("");
  const prev = React.useRef(v), raf = React.useRef(0);
  useEffect(() => {
    const a = prev.current, b = v;
    prev.current = v;
    if (a == null || b == null || Math.abs(b - a) < 0.05) { setShown(b); return undefined; }
    setFl(b > a ? "up" : "dn");
    const t0 = performance.now(), dur = 900;
    cancelAnimationFrame(raf.current);
    const step = (t) => { const k = Math.min(1, (t - t0) / dur), e = 1 - Math.pow(1 - k, 3); setShown(a + (b - a) * e); if (k < 1) raf.current = requestAnimationFrame(step); };
    raf.current = requestAnimationFrame(step);
    const to = setTimeout(() => setFl(""), 1800);
    return () => { cancelAnimationFrame(raf.current); clearTimeout(to); };
  }, [v]);
  return <span className={"gx-an131 " + fl}>{shown == null ? "" : Number(shown).toFixed(dd)}</span>;
}
const GX_AL131 = { LAK: "LA", NJD: "NJ", SJS: "SJ", TBL: "TB", UTAH: "UTA", ARI: "UTA" };
const gxAb131 = (x) => GX_AL131[x] || x;
const gxPer131 = (pd) => { const n = (pd || {}).number || 1, ty = (pd || {}).periodType; return ty === "SO" ? "SO" : ty === "OT" ? "OT" : ["", "1st", "2nd", "3rd"][n] || n + "th"; };
// who owns an NHL player in your league: team + sweater number, else team + first initial + last name
function gxOwnerMap131() {
  const P = window.__PLAYERS || [], key = (P.length || 0) + "|" + ((window.ESPN_DATA || {}).generated || "");
  if (window.__OWN131 && window.__OWN131.k === key) return window.__OWN131.m;
  const m = {};
  P.forEach((p) => {
    const no = typeof gxPdNo === "function" ? gxPdNo(p) : null;
    if (no != null) m[p.t + "#" + no] = p;
    const parts = String(p.n || "").split(" ");
    m[p.t + ":" + nrm(p.n).charAt(0) + ":" + nrm(parts.slice(1).join(" "))] = p;
  });
  window.__OWN131 = { k: key, m };
  return m;
}
function gxFind131(team, no, name) {
  const m = gxOwnerMap131(), t = gxAb131(team);
  if (no != null && m[t + "#" + no]) return m[t + "#" + no];
  const nm = String(name || ""), i = nm.indexOf(". "), last = i > 0 ? nm.slice(i + 2) : nm.split(" ").slice(1).join(" ");
  return m[t + ":" + nrm(nm).charAt(0) + ":" + nrm(last)] || null;
}
function gxTag131(s, p) {
  if (!p || !p.ft || p.ft === "fa") return "";
  const T = ((window.ESPN_DATA || {}).teams || []).find((x) => "t" + x.id === p.ft || String(x.id) === String(p.ft).replace(/^t/, "")) || {};
  if (T.abbrev) return T.abbrev;
  return String(teamName(s, p.ft) || "").replace(/[^A-Za-z0-9 ]/g, " ").trim().split(/\s+/).map((w) => w[0] || "").join("").slice(0, 4).toUpperCase();
}
function gxBoxRows131(bx, gid) {
  const pp = (typeof G120 !== "undefined" && G120.pp[gid]) || {}, P = (bx || {}).playerByGameStats || {}, out = [];
  ["awayTeam", "homeTeam"].forEach((k) => {
    const T = (bx || {})[k] || {}, ab = gxAb131(T.abbrev);
    [...(P[k] || {}).forwards || [], ...(P[k] || {}).defense || []].forEach((pl) => {
      const q = pp[pl.playerId] || {};
      const x = { g: pl.goals || 0, a: pl.assists || 0, pm: pl.plusMinus || 0, sog: (pl.sog != null ? pl.sog : pl.shots) || 0, pim: pl.pim || 0, hit: pl.hits || 0, blk: (pl.blockedShots != null ? pl.blockedShots : pl.blocked) || 0, ppp: q.ppp || 0, shp: q.shp || 0 };
      out.push({ side: k, t: ab, g: false, id: pl.playerId, no: pl.sweaterNumber, n: (pl.name || {}).default || "", toi: pl.toi || "", x, fp: typeof gxFp120 === "function" ? gxFp120(x) : 0 });
    });
    ((P[k] || {}).goalies || []).forEach((pl) => {
      if (!pl.toi || pl.toi === "00:00") return;
      let sv = pl.saves, sa = pl.shotsAgainst;
      if (sv == null && pl.saveShotsAgainst) { const m = String(pl.saveShotsAgainst).split("/"); sv = +m[0]; sa = +m[1]; }
      const x = { sv: sv || 0, ga: pl.goalsAgainst || 0, sa: sa || 0, dec: pl.decision || "" };
      out.push({ side: k, t: ab, g: true, id: pl.playerId, no: pl.sweaterNumber, n: (pl.name || {}).default || "", toi: pl.toi || "", x, fp: typeof gxFp120 === "function" ? gxFp120(x) : 0 });
    });
  });
  return out;
}
function GxNhl131({ s }) {
  const [open, setOpen] = useState(() => !!uiGet().ns131);
  const [tab, setTab] = useState("sb");
  const [gid, setGid] = useState(null);
  const [side, setSide] = useState("fan");
  const [, bump] = useState(0);
  const J = window.__NHLNOW || {}, games = (J.games || []).slice();
  const live = (g) => g.gameState === "LIVE" || g.gameState === "CRIT", fin = (g) => g.gameState === "FINAL" || g.gameState === "OFF";
  const B = (window.__BX131 = window.__BX131 || {}), L = (window.__LD131 = window.__LD131 || {});
  const box = (id) => (typeof G120 !== "undefined" && G120.box[id] && G120.box[id].bx) || (B[id] && B[id].bx) || null;
  useEffect(() => {
    if (!open || !gid) return undefined;
    const g = games.find((x) => x.id === gid);
    const need = !box(gid) || (g && live(g) && (!B[gid] || Date.now() - B[gid].at > 30000) && !(typeof G120 !== "undefined" && G120.box[gid]));
    if (!need || (g && g.gameState === "FUT")) return undefined;
    let dead = false;
    fetch("https://api-web.nhle.com/v1/gamecenter/" + gid + "/boxscore").then((r) => (r.ok ? r.json() : null)).then((bx) => { if (bx && !dead) { B[gid] = { bx, at: Date.now() }; bump((x) => x + 1); } }).catch(() => {});
    return () => { dead = true; };
  }, [open, gid, J]);
  // goals: from the scoreboard feed, or each game's summary when the feed has none
  useEffect(() => {
    if (!open || tab !== "gt") return undefined;
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
  }, [open, tab, J]);
  const nick = (ab) => (typeof GX_NICK119 !== "undefined" && GX_NICK119[gxAb131(ab)]) || ab;
  const nLive = games.filter(live).length;
  const toggle = () => { const v = !open; setOpen(v); uiSet("ns131", v ? 1 : 0); };
  const status = (g) => (live(g) ? ((g.clock || {}).inIntermission ? gxPer131(g.periodDescriptor) + " int." : gxPer131(g.periodDescriptor) + " - " + ((g.clock || {}).timeRemaining || "")) : fin(g) ? "Final" + (((g.periodDescriptor || {}).periodType || "REG") !== "REG" ? "/" + gxPer131(g.periodDescriptor) : "") : g.startTimeUTC ? new Date(g.startTimeUTC).toLocaleTimeString([], { hour: "numeric", minute: "2-digit" }) : "");
  const order = (g) => (live(g) ? 0 : g.gameState === "FUT" || g.gameState === "PRE" ? 1 : 2);
  games.sort((a, b) => order(a) - order(b) || String(a.startTimeUTC).localeCompare(String(b.startTimeUTC)));
  const teamRow = (T) => <div className="tm"><TeamLogo t={gxAb131(T.abbrev)} size={22} /><span>{nick(T.abbrev)}</span><b>{T.score != null ? T.score : ""}</b></div>;
  let body = null;
  if (gid) {
    const g = games.find((x) => x.id === gid) || {}, bx = box(gid), rows = bx ? gxBoxRows131(bx, gid) : [];
    rows.forEach((r) => { r.p = gxFind131(r.t, r.no, r.n); r.tag = gxTag131(s, r.p); r.me = r.p && r.p.ft === s.me; });
    const aw = gxAb131((g.awayTeam || {}).abbrev), hm = gxAb131((g.homeTeam || {}).abbrev);
    const list = side === "fan" ? rows.filter((r) => r.tag).sort((a, b) => b.fp - a.fp) : rows.filter((r) => r.side === side);
    const sk = list.filter((r) => !r.g), gl = list.filter((r) => r.g);
    const nm = (r) => <div className={"nm" + (r.me ? " me" : "")} key={"n" + r.id}><button type="button" className="hover:underline" onClick={() => { if (r.p && window.__NAV) window.__NAV.player(r.p); }}>{r.n}</button>{r.tag ? <span className="own">{r.tag}</span> : null}</div>;
    body = (
      <>
        <div className="hd"><button type="button" className="bk" aria-label="Back" onClick={() => setGid(null)}>{"‹"}</button>
          <div style={{ flex: 1 }}>{teamRow(g.awayTeam || {})}{teamRow(g.homeTeam || {})}</div>
          <div className={"st" + (live(g) ? " lv" : "")} style={{ fontSize: 13, color: live(g) ? "var(--bad)" : "var(--mute)", minWidth: 70, textAlign: "right" }}>{status(g)}</div></div>
        <div className="tabs">{[["fan", "Fantasy"], ["awayTeam", aw], ["homeTeam", hm]].map(([k, l]) => <button key={k} type="button" className={side === k ? "on" : ""} onClick={() => setSide(k)}>{l}</button>)}</div>
        {!bx ? <div className="em">{g.gameState === "FUT" || g.gameState === "PRE" ? "Not started yet." : "Loading..."}</div> : (
          <>
            {sk.length ? <div className="bx"><div className="h nm">Skaters</div><div className="h">TOI</div><div className="h">G</div><div className="h">A</div><div className="h">+/-</div><div className="h">FPTS</div>
              {sk.map((r) => [nm(r), <div key={"t" + r.id}>{r.toi}</div>, <div key={"g" + r.id}>{r.x.g}</div>, <div key={"a" + r.id}>{r.x.a}</div>, <div key={"p" + r.id}>{r.x.pm > 0 ? "+" + r.x.pm : r.x.pm}</div>, <div key={"f" + r.id} className="f">{f1(r.fp)}</div>])}</div> : side === "fan" ? <div className="em">No fantasy-rostered players in this game.</div> : null}
            {gl.length ? <div className="bx g"><div className="h nm">Goalies</div><div className="h">MIN</div><div className="h">W</div><div className="h">GA</div><div className="h">SV</div><div className="h">FPTS</div>
              {gl.map((r) => [nm(r), <div key={"t" + r.id}>{r.toi}</div>, <div key={"w" + r.id}>{r.x.dec === "W" ? 1 : 0}</div>, <div key={"ga" + r.id}>{r.x.ga}</div>, <div key={"sv" + r.id}>{r.x.sv}</div>, <div key={"f" + r.id} className="f">{f1(r.fp)}</div>])}</div> : null}
          </>
        )}
      </>
    );
  } else if (tab === "sb") {
    body = games.length ? games.map((g) => (
      <button key={g.id} type="button" className="gm" onClick={() => { setGid(g.id); setSide("fan"); }}>
        {teamRow(g.awayTeam || {})}<div className={"st" + (live(g) ? " lv" : "")}>{status(g)}</div>{teamRow(g.homeTeam || {})}
      </button>
    )) : <div className="em">No NHL games today.</div>;
  } else {
    const all = [];
    games.forEach((g) => (g.goals || (L[g.id] || {}).goals || []).forEach((x) => all.push({ g, x })));
    all.sort((a, b) => String(b.g.startTimeUTC).localeCompare(String(a.g.startTimeUTC)) || ((b.x.periodDescriptor || {}).number || 0) - ((a.x.periodDescriptor || {}).number || 0) || String(b.x.timeInPeriod).localeCompare(String(a.x.timeInPeriod)));
    body = all.length ? all.map(({ g, x }, i) => {
      const tm = gxAb131(x.teamAbbrev && x.teamAbbrev.default ? x.teamAbbrev.default : x.teamAbbrev), who = (x.name && x.name.default) || [((x.firstName || {}).default || ""), ((x.lastName || {}).default || "")].join(" ").trim();
      const p = gxFind131(tm, null, who), tag = gxTag131(s, p);
      const sc = gxAb131((g.awayTeam || {}).abbrev) + " " + (x.awayScore != null ? x.awayScore : "") + ", " + gxAb131((g.homeTeam || {}).abbrev) + " " + (x.homeScore != null ? x.homeScore : "");
      return (
        <div key={g.id + "-" + i} className="gl">
          <div className="top">{x.headshot || x.mugshot ? <img src={x.headshot || x.mugshot} alt="" /> : <TeamLogo t={tm} size={46} />}
            <div className="min-w-0"><div className="who">{who + ", " + tm}{tag ? <span className="own">{"(" + tag + ")"}</span> : null}</div><div className="when">{x.timeInPeriod + " " + gxPer131(x.periodDescriptor) + " Period · " + sc}</div></div></div>
          {(x.assists || []).length ? <div className="as"><span>Assists:</span><span>{(x.assists || []).map((a) => { const an = (a.name && a.name.default) || [((a.firstName || {}).default || ""), ((a.lastName || {}).default || "")].join(" ").trim(), ap = gxFind131(tm, null, an), at = gxTag131(s, ap); return an + (at ? " (" + at + ")" : ""); }).join(", ")}</span></div> : <div className="as"><span>Assists:</span><span>Unassisted</span></div>}
        </div>
      );
    }) : <div className="em">No goals yet today.</div>;
  }
  return (
    <div className="gx-ns131">
      <button type="button" className="bar" onClick={toggle}><span>NHL scores</span><span className="n">{nLive ? <span className="lv">{nLive + " live"}</span> : games.length ? games.length + " games" : ""}</span><span className={"sec-chev" + (open ? "" : " shut")} style={{ marginLeft: 8 }}></span></button>
      {open ? <>{!gid ? <div className="seg"><button type="button" className={tab === "sb" ? "on" : ""} onClick={() => setTab("sb")}>Scoreboard</button><button type="button" className={tab === "gt" ? "on" : ""} onClick={() => setTab("gt")}>Goal tracker</button></div> : null}{body}</> : null}
    </div>
  );
}
'''


def change_sync(t):
    return lit(t, "131: save team abbreviations",
               '"logo": str(t.get("logo") or "")} for t in lg.get("teams", [])]  # change 114: team pictures',
               '"logo": str(t.get("logo") or ""), "abbrev": str(t.get("abbrev") or "")} for t in lg.get("teams", [])]  # change 114: team pictures (abbrev: change 131)',
               '"abbrev": str(t.get("abbrev") or "")}')


def change(t):
    t = lit(t, "131: styles", "</style>", NEW_CSS, "change 131 (install.py)")
    t = lit(t, "131: helpers", ROOT, HELPERS + ROOT, "change 131: animated scores")
    t = lit(t, "131: keep today's NHL feed", "window.__LP120 = Date.now();", "window.__NHLNOW = js; window.__LP120 = Date.now();", "window.__NHLNOW = js;")
    t = lit(t, "131: home score you", '<div className="gx-num" style={big}>{f1(aA)}</div>', '<div className="gx-num" style={big}><GxAnimNum131 v={aA} /></div>', "<GxAnimNum131 v={aA} /></div>\n")
    t = lit(t, "131: home score them", '<div className="gx-num" style={{ ...big, color: "var(--ink2)" }}>{f1(aB)}</div>', '<div className="gx-num" style={{ ...big, color: "var(--ink2)" }}><GxAnimNum131 v={aB} /></div>', 'style={{ ...big, color: "var(--ink2)" }}><GxAnimNum131')
    t = lit(t, "131: matchup score you", '<div className="gx-num" style={{ fontSize: 28 }}>{f1(aA)}</div>', '<div className="gx-num" style={{ fontSize: 28 }}><GxAnimNum131 v={aA} /></div>', 'style={{ fontSize: 28 }}><GxAnimNum131 v={aA} />')
    t = lit(t, "131: matchup score them", '<div className="gx-num" style={{ fontSize: 28, color: "var(--ink2)" }}>{f1(aB)}</div>', '<div className="gx-num" style={{ fontSize: 28, color: "var(--ink2)" }}><GxAnimNum131 v={aB} /></div>', 'style={{ fontSize: 28, color: "var(--ink2)" }}><GxAnimNum131')
    t = lit(t, "131: NHL scores panel on Matchup", '        </div>\n      </div>\n      <div className="gx-dn108">', '        </div>\n      </div>\n      <GxNhl131 s={s} />\n      <div className="gx-dn108">', "<GxNhl131 s={s} />")
    return t


edit("espn_sync.py", change_sync)
edit(APP, change)
