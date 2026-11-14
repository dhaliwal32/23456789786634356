# changes/279-game-preview.py - tap a game before it starts: full preview (odds, records, where, goalies, season series, scoring leaders, team stats side by side, injuries, last 5 games); Fantasy tab shows your and their players in the game with projections plus the best free agents; team tabs show every player's season

NEW_CSS = r'''  /* change 279 (install.py) */
  .gx-pv279 { padding: 4px 12px 24px; font-variant-numeric: tabular-nums; }
  .gx-pv279 .h { padding: 16px 4px 8px; font-size: 13px; font-weight: 700; letter-spacing: .04em; display: flex; justify-content: space-between; gap: 10px; }
  .gx-pv279 .h small { font-weight: 400; letter-spacing: 0; color: var(--mute); font-size: 12px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .gx-pv279 .cd { background: var(--card); border-radius: 12px; overflow: hidden; }
  .gx-pv279 .c3 { display: grid; grid-template-columns: minmax(0,1fr) 132px minmax(0,1fr); align-items: center; gap: 6px; min-height: 40px; padding: 6px 12px; border-top: 1px solid var(--line); font-size: 14px; }
  .gx-pv279 .c3:first-child, .gx-pv279 .rw:first-child { border-top: 0; }
  .gx-pv279 .c3 > :nth-child(2) { text-align: center; font-size: 12px; color: var(--mute); }
  .gx-pv279 .c3 > :nth-child(3) { text-align: right; }
  .gx-pv279 .c3 > * { min-width: 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .gx-pv279 .c3 b { font-weight: 600; }
  .gx-pv279 .c3 .lo { color: var(--mute); }
  .gx-pv279 .c3.tm { font-weight: 600; min-height: 44px; }
  .gx-pv279 .c3.tm span { display: inline-flex; align-items: center; gap: 6px; }
  .gx-pv279 .c3 small { display: block; font-size: 11.5px; color: var(--mute); overflow: hidden; text-overflow: ellipsis; }
  .gx-pv279 .rw { display: grid; grid-template-columns: minmax(0,1fr) auto; align-items: center; gap: 10px; min-height: 40px; padding: 6px 12px; border-top: 1px solid var(--line); font-size: 14px; }
  .gx-pv279 .rw > :first-child { min-width: 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .gx-pv279 .rw small { color: var(--mute); font-size: 12px; }
  .gx-pv279 .rw em { font-style: normal; color: var(--mute); font-size: 13px; white-space: nowrap; }
  .gx-pv279 .sub { display: flex; align-items: center; gap: 6px; padding: 10px 12px 4px; font-size: 13px; font-weight: 600; }
  .gx-pv279 .l5 { display: grid; grid-template-columns: minmax(0,1fr) minmax(0,1fr); gap: 10px; }
  .gx-pv279 .l5 .g { display: grid; grid-template-columns: 40px minmax(0,1fr) auto; gap: 6px; align-items: center; min-height: 34px; padding: 4px 10px; border-top: 1px solid var(--line); font-size: 13px; }
  .gx-pv279 .l5 .g > :nth-child(1) { color: var(--mute); font-size: 12px; }
  .gx-pv279 .l5 .g > :nth-child(2) { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .gx-pv279 .l5 .g b { font-weight: 600; }
  .gx-pv279 .pl { display: grid; grid-template-columns: auto minmax(0,1fr) 44px; align-items: center; gap: 10px; min-height: 46px; padding: 5px 12px; border-top: 1px solid var(--line); font-size: 14px; }
  .gx-pv279 .pl:first-child { border-top: 0; }
  .gx-pv279 .pl > :nth-child(2) { min-width: 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .gx-pv279 .pl small { display: block; font-size: 11.5px; color: var(--mute); }
  .gx-pv279 .pl > :nth-child(3) { text-align: right; font-weight: 600; }
  .gx-pv279 .tb { display: grid; grid-template-columns: minmax(0,1fr) 34px 52px 44px 44px; font-size: 14px; }
  .gx-pv279 .tb > div { min-height: 38px; display: flex; align-items: center; justify-content: flex-end; padding: 4px 6px; border-top: 1px solid var(--line); min-width: 0; }
  .gx-pv279 .tb > .n { justify-content: flex-start; padding-left: 12px; gap: 6px; white-space: nowrap; overflow: hidden; }
  .gx-pv279 .tb > .n button, .gx-pv279 .tb > .n span.x { overflow: hidden; text-overflow: ellipsis; }
  .gx-pv279 .tb > .n i { font-style: normal; font-size: 10.5px; color: var(--mute); border: 1px solid var(--line2); border-radius: 5px; padding: 0 4px; flex-shrink: 0; }
  .gx-pv279 .tb > .hh { font-size: 11.5px; color: var(--mute); border-top: 0; min-height: 32px; }
  .gx-pv279 .tb > .f { font-weight: 600; padding-right: 12px; }
  .gx-pv279 .em { padding: 14px 12px; color: var(--mute); font-size: 13.5px; }
  @media (max-width: 640px) { .gx-pv279 .c3 { grid-template-columns: minmax(0,1fr) 112px minmax(0,1fr); padding: 6px 10px; } .gx-pv279 .l5 { gap: 8px; } .gx-pv279 .l5 .g { grid-template-columns: 34px minmax(0,1fr) auto; padding: 4px 8px; font-size: 12.5px; } }
</style>'''

HELPERS = r'''// ---------- change 279: game preview before puck drop (install.py) ----------
// [ESPN stat name, label, 1 = higher is better, -1 = lower is better, 0 = neither]
const GX_ST279 = [["avgGoals", "Goals a game", 1], ["avgGoalsAgainst", "Goals against a game", -1], ["avgShots", "Shots a game", 1], ["avgShotsAgainst", "Shots against a game", -1], ["powerPlayPct", "Power play %", 1], ["penaltyKillPct", "Penalty kill %", 1], ["powerPlayGoals", "Power play goals", 1], ["powerPlayGoalsAgainst", "PP goals against", -1], ["shortHandedGoals", "Shorthanded goals", 1], ["penaltyMinutes", "Penalty minutes", 0]];
const gxMD279 = (x) => { const d = new Date(x); return isNaN(d) ? "" : (d.getMonth() + 1) + "/" + d.getDate(); };
const gxDay279 = (x) => { const d = /^\d{4}-\d\d-\d\d$/.test(String(x)) ? fromIso(x) : new Date(x); return isNaN(d) ? "" : d.toLocaleDateString("en-US", { month: "short", day: "numeric" }); };
const gxGmDate279 = (g) => { const d = g && g.startTimeUTC ? new Date(g.startTimeUTC) : null; return d && !isNaN(d) ? iso(d) : todayISO(); };
const gxProj279 = (p, K, dt) => effAvg(p, K, dt) * (p.p === "G" ? gStart(p, dt).v : p.prob == null ? 1 : p.prob) * avail(p, dt);
function gxUsePre279(id) {
  const [sm, setSm] = useState(null);
  useEffect(() => {
    let dead = false;
    const load = () => gxSum132(id).then((js) => { if (!dead && js) setSm(js); });
    setSm(null); load();
    const t = setInterval(load, 60000);
    return () => { dead = true; clearInterval(t); };
  }, [id]);
  return sm;
}
function GxPre279({ id, g, pBtn }) {
  const sm = gxUsePre279(id);
  const aw = gxAb131((g.awayTeam || {}).abbrev), hm = gxAb131((g.homeTeam || {}).abbrev);
  if (!sm) return <div className="gx-pv279"><div className="em">Loading the preview...</div></div>;
  const P = pby(), dt = gxGmDate279(g);
  const of = (list, ab) => (list || []).find((x) => gxAb131(((x || {}).team || {}).abbreviation) === ab) || {};
  const comp = (ab) => ((gxHead132(sm).competitors) || []).find((c) => gxAb131((c.team || {}).abbreviation) === ab) || {};
  const rec = (ab, ty) => { const r = (comp(ab).record || []).find((x) => ty.indexOf(x.type) >= 0); return r ? r.summary : ""; };
  const stat = (ab, nm) => { const x = ((of((sm.boxscore || {}).teams, ab).statistics) || []).find((q) => q.name === nm); return x ? x.displayValue : null; };
  const pk = (sm.pickcenter || [])[0] || {}, vn = (sm.gameInfo || {}).venue || {};
  const tv = [...new Set((sm.broadcasts || []).map((x) => (x.media || {}).shortName || x.station).filter(Boolean))].slice(0, 3).join(", ");
  const ser = (sm.seasonseries || [])[0];
  const ld = (ab, nm) => { const c = ((of(sm.leaders, ab).leaders) || []).find((x) => x.name === nm), l = c && (c.leaders || [])[0]; return l && l.athlete ? l : null; };
  const who = (l, right) => {
    if (!l) return <span></span>;
    const p = P["e" + l.athlete.id], line = (l.statistics || []).map((x) => x.displayValue + " " + x.abbreviation).join(", ");
    return <span>{pBtn(p, l.athlete.shortName || l.athlete.displayName, "x")}<small>{line}</small></span>;
  };
  const cmp = (a, b, dir) => { const x = parseFloat(a), y = parseFloat(b); if (!dir || isNaN(x) || isNaN(y) || x === y) return [false, false]; const aw2 = dir > 0 ? x > y : x < y; return [!aw2, aw2]; };
  const gl = (ab) => { const D = (window.__GOALIES || {})[dt] || {}; return Object.keys(D).filter((n) => D[n] && D[n].team === ab).map((n) => ({ n: n.replace(/\b\w/g, (c) => c.toUpperCase()), st: D[n].status || "" })); };
  const glA = gl(aw), glH = gl(hm);
  const inj = (ab) => (of(sm.injuries, ab).injuries) || [];
  const l5 = (ab) => (of(sm.lastFiveGames, ab).events) || [];
  const head = <div className="c3 tm"><span><TeamLogo t={aw} size={22} />{aw}</span><span></span><span style={{ justifyContent: "flex-end" }}>{hm}<TeamLogo t={hm} size={22} /></span></div>;
  const facts = [["Line", pk.details], ["Total goals", pk.overUnder != null ? String(pk.overUnder) : ""], ["Where", [vn.fullName, (vn.address || {}).city].filter(Boolean).join(", ")], ["TV", tv]].filter((x) => x[1]);
  return (
    <div className="gx-pv279" data-gx="279">
      <div className="h"><span>MATCHUP</span></div>
      <div className="cd">
        {head}
        <div className="c3"><b>{rec(aw, ["total"])}</b><span>Record</span><b>{rec(hm, ["total"])}</b></div>
        {rec(aw, ["road", "away"]) || rec(hm, ["home"]) ? <div className="c3"><span>{rec(aw, ["road", "away"])}</span><span>Away / Home</span><span>{rec(hm, ["home"])}</span></div> : null}
        {glA.length || glH.length ? <div className="c3"><span>{glA[0] ? glA[0].n : "\u2013"}<small>{glA[0] ? glA[0].st : ""}</small></span><span>Goalie</span><span>{glH[0] ? glH[0].n : "\u2013"}<small>{glH[0] ? glH[0].st : ""}</small></span></div> : null}
        {facts.map(([k, v]) => <div key={k} className="rw"><small>{k}</small><span>{v}</span></div>)}
      </div>
      {ser ? <>
        <div className="h"><span>SEASON SERIES</span><small>{ser.summary || ""}</small></div>
        <div className="cd">{(ser.events || []).map((e) => {
          const cs = e.competitors || [], a2 = cs.find((c) => c.homeAway === "away") || cs[0] || {}, h2 = cs.find((c) => c.homeAway === "home") || cs[1] || {}, fin = (e.statusType || {}).completed;
          const nm = (c) => gxAb131(((c.team || {}).abbreviation) || "");
          return <div key={e.id} className="rw"><span>{fin ? <>{a2.winner ? <b>{nm(a2) + " " + a2.score}</b> : nm(a2) + " " + a2.score}{", "}{h2.winner ? <b>{nm(h2) + " " + h2.score}</b> : nm(h2) + " " + h2.score}</> : nm(a2) + " at " + nm(h2)}</span><em>{gxDay279(e.date) + (fin ? " \u00b7 Final" : "")}</em></div>;
        })}</div>
      </> : null}
      {["points", "goals", "assists"].some((k) => ld(aw, k) || ld(hm, k)) ? <>
        <div className="h"><span>SCORING LEADERS</span></div>
        <div className="cd">{head}{[["points", "Points"], ["goals", "Goals"], ["assists", "Assists"]].map(([k, l]) => <div key={k} className="c3">{who(ld(aw, k))}<span>{l}</span>{who(ld(hm, k), true)}</div>)}</div>
      </> : null}
      {GX_ST279.some(([k]) => stat(aw, k) != null) ? <>
        <div className="h"><span>TEAM STATS</span><small>this season, better side in bold</small></div>
        <div className="cd">{head}{GX_ST279.map(([k, l, dir]) => { const a = stat(aw, k), b = stat(hm, k); if (a == null && b == null) return null; const w = cmp(a, b, dir); return <div key={k} className="c3">{w[1] ? <b>{a}</b> : <span className={w[0] ? "lo" : ""}>{a}</span>}<span>{l}</span>{w[0] ? <b>{b}</b> : <span className={w[1] ? "lo" : ""}>{b}</span>}</div>; })}</div>
      </> : null}
      <div className="h"><span>INJURIES</span></div>
      <div className="cd">{[aw, hm].map((ab) => (
        <React.Fragment key={ab}>
          <div className="sub" style={ab === hm ? { borderTop: "1px solid var(--line)" } : null}><TeamLogo t={ab} size={20} />{gxFull141(ab)}</div>
          {inj(ab).length ? inj(ab).map((x, j) => { const at = x.athlete || {}, dd = x.details || {}; return <div key={j} className="rw" style={{ borderTop: 0, minHeight: 34 }}><span>{pBtn(P["e" + at.id], at.displayName, "i")} <small>{[((at.position || {}).abbreviation), dd.type].filter(Boolean).join(" \u00b7 ")}</small></span><em>{[((x.type || {}).abbreviation) || x.status, dd.returnDate ? "back " + gxDay279(dd.returnDate) : ""].filter(Boolean).join(" \u00b7 ")}</em></div>; }) : <div className="em" style={{ paddingTop: 4 }}>Nobody listed.</div>}
        </React.Fragment>
      ))}</div>
      {l5(aw).length || l5(hm).length ? <>
        <div className="h"><span>LAST 5 GAMES</span></div>
        <div className="l5">{[aw, hm].map((ab) => (
          <div key={ab} className="cd">
            <div className="sub"><TeamLogo t={ab} size={20} />{ab}</div>
            {l5(ab).slice().sort((x, y) => String(y.gameDate).localeCompare(String(x.gameDate))).map((e) => <div key={e.id} className="g"><span>{gxMD279(e.gameDate)}</span><span>{(e.atVs || "") + " " + gxAb131(((e.opponent || {}).abbreviation) || "")}</span><span>{e.gameResult === "W" ? <b>{"W " + e.score}</b> : (e.gameResult || "") + " " + (e.score || "")}</span></div>)}
          </div>
        ))}</div>
      </> : null}
    </div>
  );
}
// Fantasy and team tabs before the game starts
function GxPreTab279({ s, g, gt, a, b, pBtn }) {
  const K = s.blend, dt = gxGmDate279(g);
  const aw = gxAb131((g.awayTeam || {}).abbrev), hm = gxAb131((g.homeTeam || {}).abbrev);
  const inGame = s.players.filter((p) => p.t === aw || p.t === hm).map((p) => ({ p, x: gxProj279(p, K, dt) }));
  const row = ({ p, x }) => <div key={p.id} className="pl"><GxFace p={p} size={20} /><span>{pBtn(p, p.n, "p")}<small>{p.t + " \u00b7 " + p.p + (p.ir ? " \u00b7 IR" : "") + " \u00b7 " + f1(p.avg || 0) + " a game"}</small></span><span>{p.ir ? "\u2013" : f1(x)}</span></div>;
  const list = (rows, none) => <div className="cd">{rows.length ? rows.map(row) : <div className="em">{none}</div>}</div>;
  if (gt === "fan") {
    const mine = (id) => inGame.filter((o) => o.p.ft === id).sort((u, v) => v.x - u.x);
    const fa = inGame.filter((o) => o.p.ft === "fa" && !o.p.ir && o.x > 0).sort((u, v) => v.x - u.x).slice(0, 6);
    const sum = (rows) => f1(rows.reduce((t, o) => t + (o.p.ir ? 0 : o.x), 0));
    return (
      <div className="gx-pv279" data-gx="279">
        {[a, b].filter(Boolean).map((id) => <React.Fragment key={id}><div className="h"><span>{(id === s.me ? "YOUR PLAYERS" : String(teamName(s, id)).toUpperCase())}</span><small>{"projected " + sum(mine(id))}</small></div>{list(mine(id), "Nobody in this game.")}</React.Fragment>)}
        <div className="h"><span>BEST FREE AGENTS IN THIS GAME</span><small>projected</small></div>
        {list(fa, "No free agents worth a look.")}
      </div>
    );
  }
  const T = gt === "awayTeam" ? aw : hm;
  const rows = inGame.filter((o) => o.p.t === T && (o.p.gp || 0) > 0).sort((u, v) => (v.p.tot || 0) - (u.p.tot || 0)).slice(0, 24);
  return (
    <div className="gx-pv279" data-gx="279">
      <div className="h"><span>{String(gxFull141(T)).toUpperCase()}</span><small>season and tonight</small></div>
      <div className="cd"><div className="tb">
        <div className="hh n">PLAYER</div><div className="hh">GP</div><div className="hh">FPTS</div><div className="hh">AVG</div><div className="hh f">PROJ</div>
        {rows.map(({ p, x }) => [
          <div key={"n" + p.id} className="n">{pBtn(p, shortN(p.n), "p")}<small style={{ color: "var(--mute)", fontSize: 11.5 }}>{p.p}</small>{gxTag131(s, p) ? <i>{gxTag131(s, p)}</i> : null}</div>,
          <div key={"g" + p.id}>{p.gp}</div>, <div key={"t" + p.id}>{f1(p.tot || 0)}</div>, <div key={"a" + p.id}>{f1(p.avg || 0)}</div>, <div key={"x" + p.id} className="f">{p.ir ? "\u2013" : f1(x)}</div>,
        ])}
      </div>{rows.length ? null : <div className="em">No players found for this team.</div>}</div>
    </div>
  );
}
'''

OLD_GAME = r'''body = <>{/* change 263 */}<GxTrack264 id={gid} g={g} />{gs.length ?'''
NEW_GAME = r'''body = pre(g) ? <GxPre279 id={gid} g={g} pBtn={pBtn} /> : <>{/* change 263 */}<GxTrack264 id={gid} g={g} />{gs.length ?'''

OLD_TAB = r'''      } else if (!bx) {
        body = <div style={{ padding: 16, color: "var(--mute)" }}>{pre(g) ? "Not started yet." : "Loading..."}</div>;'''
NEW_TAB = r'''      } else if (pre(g)) {
        body = <GxPreTab279 s={s} g={g} gt={gt} a={a} b={b} pBtn={pBtn} />;
''' + OLD_TAB


def change(t):
    t = lit(t, "279: styles", "</style>", NEW_CSS, "change 279 (install.py)")
    t = lit(t, "279: helpers", ROOT, HELPERS + ROOT, "change 279: game preview before puck drop")
    t = lit(t, "279: game tab", OLD_GAME, NEW_GAME, "<GxPre279 id={gid}")
    t = lit(t, "279: other tabs", OLD_TAB, NEW_TAB, "<GxPreTab279 s={s}")
    return t

edit(APP, change)
