# changes/095-player-screen.py - new ESPN-style player screen: photo, number, position, rank, averages, and tabs (Overview, Game log, News, Lines)

NEW_CSS = r'''  /* change 095 (install.py) */
  .gx-pd-ov { position: fixed; inset: 0; z-index: 50; overflow-y: auto; background: rgba(0,0,0,.65); }
  .gx-pd { max-width: 680px; margin: 28px auto; background: var(--bg); border: 1px solid var(--line); border-radius: 14px; overflow: hidden; position: relative; }
  .gx-pd-x { position: absolute; top: 8px; right: 10px; z-index: 2; font-size: 22px; line-height: 1; color: var(--mute); padding: 6px; }
  .gx-pd-hd { display: grid; grid-template-columns: 132px 1fr 170px; gap: 14px; padding: 16px 16px 12px; background: var(--card); border-bottom: 1px solid var(--line); }
  .gx-pd-ph { position: relative; width: 132px; height: 112px; border-radius: 10px; overflow: hidden; background: var(--card2); display: flex; align-items: flex-end; justify-content: center; }
  .gx-pd-ph .lg { position: absolute; left: 6px; top: 6px; opacity: .35; }
  .gx-pd-ph img { position: relative; height: 104px; width: auto; object-fit: contain; }
  .gx-pd-ph .ini { position: relative; margin-bottom: 30px; font-size: 30px; font-weight: 600; color: var(--faint); }
  .gx-pd-nm { display: flex; align-items: flex-start; gap: 8px; padding-right: 24px; }
  .gx-pd-no { font-size: 38px; line-height: 1; font-weight: 300; color: var(--faint); font-variant-numeric: tabular-nums; }
  .gx-pd-nm .f { font-size: 17px; line-height: 1.15; }
  .gx-pd-nm .l { font-size: 21px; line-height: 1.15; font-weight: 700; }
  .gx-pd-tm { font-size: 13px; color: var(--mute); margin-top: 2px; }
  .gx-pd-kv { display: grid; grid-template-columns: 74px 1fr; row-gap: 3px; margin-top: 10px; font-size: 13px; }
  .gx-pd-kv .k { color: var(--mute); font-size: 11px; letter-spacing: .06em; text-transform: uppercase; padding-top: 2px; }
  .gx-pd-dot { display: inline-block; width: 8px; height: 8px; border-radius: 50%; margin-left: 6px; vertical-align: 1px; }
  .gx-pd-st { border-left: 1px solid var(--line); padding-left: 14px; display: flex; flex-direction: column; gap: 9px; padding-right: 22px; }
  .gx-pd-st .k { color: var(--mute); font-size: 11px; letter-spacing: .06em; text-transform: uppercase; }
  .gx-pd-st .v { font-size: 20px; font-weight: 700; line-height: 1.1; font-variant-numeric: tabular-nums; }
  .gx-pd-st .v small { font-size: 12px; font-weight: 400; color: var(--mute); margin-left: 4px; }
  .gx-pd-ac { display: flex; flex-wrap: wrap; gap: 8px; padding: 12px 16px; background: var(--card); border-bottom: 1px solid var(--line); }
  .gx-pd-ac button { padding: 7px 14px; border-radius: 999px; border: 1px solid var(--line2); font-size: 13px; color: var(--ink); }
  .gx-pd-ac button.pr { background: var(--accent); border-color: var(--accent); color: var(--on, #fff); font-weight: 600; }
  .gx-pd-tb { display: flex; border-bottom: 1px solid var(--line); background: var(--card); overflow-x: auto; }
  .gx-pd-tb button { flex: 1; padding: 11px 6px 9px; font-size: 14px; color: var(--mute); border-bottom: 2px solid transparent; white-space: nowrap; }
  .gx-pd-tb button.on { color: var(--ink); border-bottom-color: var(--accent); font-weight: 600; }
  .gx-pd-bd { padding: 12px; display: flex; flex-direction: column; gap: 12px; }
  .gx-pd-pn { background: var(--card); border: 1px solid var(--line); border-radius: 12px; padding: 12px 14px; }
  .gx-pd-h { font-weight: 600; font-size: 15px; margin-bottom: 8px; display: flex; align-items: baseline; gap: 8px; }
  .gx-pd-h .r { margin-left: auto; font-weight: 400; font-size: 12px; color: var(--mute); }
  .gx-pd-t { width: 100%; border-collapse: collapse; font-size: 13px; font-variant-numeric: tabular-nums; }
  .gx-pd-t th { font-size: 11px; font-weight: 600; color: var(--mute); text-align: right; padding: 6px 4px; border-bottom: 1px solid var(--line2); white-space: nowrap; }
  .gx-pd-t td { text-align: right; padding: 7px 4px; border-top: 1px solid var(--line); white-space: nowrap; }
  .gx-pd-t th:first-child, .gx-pd-t td:first-child { text-align: left; }
  .gx-pd-t td.b { font-weight: 600; }
  .gx-pd-t tr.lv td { background: var(--accentSoft); }
  .gx-pd-tl { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; }
  .gx-pd-tl > div { border: 1px solid var(--line); border-radius: 10px; padding: 8px 10px; }
  .gx-pd-tl .k { font-size: 11px; color: var(--mute); }
  .gx-pd-tl .v { font-size: 18px; font-weight: 700; font-variant-numeric: tabular-nums; }
  .gx-pd-tl .s { font-size: 11px; color: var(--mute); }
  .gx-pd-nw { padding: 8px 0; border-top: 1px solid var(--line); font-size: 13px; }
  .gx-pd-nw:first-of-type { border-top: 0; }
  .gx-pd-nw .d { font-size: 11px; color: var(--mute); text-transform: uppercase; letter-spacing: .04em; margin-bottom: 2px; }
  .gx-pd-mt { display: inline-block; margin: 2px 6px 2px 0; padding: 4px 10px; border: 1px solid var(--line2); border-radius: 999px; font-size: 13px; }
  .gx-pd-more { display: block; width: 100%; text-align: center; padding-top: 10px; font-size: 14px; color: var(--accent); }
  @media (max-width: 640px) {
    .gx-pd-ov { background: var(--bg); }
    .gx-pd { margin: 0; border: 0; border-radius: 0; min-height: 100%; }
    .gx-pd-hd { grid-template-columns: 96px 1fr; gap: 12px; padding: 14px 12px 12px; }
    .gx-pd-ph { width: 96px; height: 96px; }
    .gx-pd-ph img { height: 90px; }
    .gx-pd-no { font-size: 30px; }
    .gx-pd-nm .l { font-size: 19px; }
    .gx-pd-kv { grid-template-columns: 64px 1fr; margin-top: 6px; }
    .gx-pd-st { grid-column: 1 / -1; border-left: 0; padding: 10px 0 0; border-top: 1px solid var(--line); flex-direction: row; justify-content: space-between; gap: 6px; }
    .gx-pd-st .k { font-size: 10px; letter-spacing: .03em; }
    .gx-pd-st .v { font-size: 18px; }
    .gx-pd-ac { padding: 10px 12px; }
    .gx-pd-bd { padding: 10px 8px; }
    .gx-pd-pn { padding: 10px; }
    .gx-pd-t { font-size: 12px; }
    .gx-pd-t th, .gx-pd-t td { padding-left: 2px; padding-right: 2px; }
  }
</style>'''

HELPERS = r'''// ---------- change 095: ESPN-style player screen (install.py) ----------
const GXPD_DOT = " " + String.fromCharCode(183) + " ";
const gxPdSec = (t) => { const m = String(t || "").split(":"); return m.length === 2 ? (+m[0]) * 60 + (+m[1]) : null; };
const gxPdMS = (v) => (v == null ? "-" : Math.floor(v / 60) + ":" + String(Math.round(v % 60)).padStart(2, "0"));
const gxPdReal = (p, d) => {
  const D = (((window.ESPN_DATA || {}).daily) || {})[d] || {}, id = String(p.id || "").replace(/^e/, "");
  for (const tm of Object.values(D)) { const v = (tm || {})[id]; if (v && v[0] != null) return v[0]; }
  return null;
};
const gxPdTeam = (t) => (((window.LINES_DATA || {}).teams || {})[t]) || {};
// jersey number from the NHL roster (saved by gm_lines.py from change 095 on)
const gxPdNo = (p) => { const m = gxPdTeam(p.t).no; if (!m) return null; const k = nrm(p.n); for (const n in m) if (nrm(n) === k) return m[n]; return null; };
// NHL position code and shoots (C, LW, RW, D; L or R)
const gxPdNhlPos = (p) => { const m = (gxPdTeam(p.t).pos || {}).nhl || {}, k = nrm(p.n); for (const n in m) if (nrm(n) === k) return m[n]; return ""; };
const gxPdSigned = (v) => (v > 0 ? "+" + v : String(v || 0));
// one row of totals for a set of games
const gxPdSum = (rows, isG) => {
  const n = rows.length, sum = (f) => rows.reduce((a, r) => a + (f(r) || 0), 0);
  if (isG) {
    const sv = sum((r) => r.x.sv), sa = sum((r) => (r.x.sa != null ? r.x.sa : (r.x.sv || 0) + (r.x.ga || 0)));
    return { gp: n, w: rows.filter((r) => r.x.dec === "W").length, l: rows.filter((r) => r.x.dec === "L" || r.x.dec === "O").length, ga: sum((r) => r.x.ga), sv, svp: sa ? sv / sa : null, fp: sum((r) => r.fp) };
  }
  const ts = rows.map((r) => gxPdSec(r.x.toi)).filter((v) => v != null);
  return { gp: n, toi: ts.length ? ts.reduce((a, v) => a + v, 0) / ts.length : null, g: sum((r) => r.x.g), a: sum((r) => r.x.a), pm: sum((r) => r.x.pm), pim: sum((r) => r.x.pim), sog: sum((r) => r.x.sog), fp: sum((r) => r.fp) };
};
const GX_PD_SLOT = { F1: "1st line", F2: "2nd line", F3: "3rd line", F4: "4th line", D1: "Top pair", D2: "2nd pair", D3: "3rd pair", PP1: "Power play 1", PP2: "Power play 2", PK1: "Penalty kill 1", PK2: "Penalty kill 2", G: "Goalies" };

function GxPlayerDetail({ p: p0, s, wk, onClose }) {
  const K = s.blend, today = todayISO(), sc = s.sc || {};
  const p = s.players.find((q) => q.id === p0.id) || p0;
  const eid = typeof p.id === "string" && p.id[0] === "e" ? p.id.slice(1) : null;
  const isG = p.p === "G";
  const [tab, setTab] = useState("ov");
  const [log, setLog] = useState(null);
  const [nLog, setNLog] = useState(10);
  const [img, setImg] = useState(true);
  const rank = useMemo(() => {
    const o = {}, pv = (q) => effAvg(q, K) * (q.p === "G" ? q.prob : 1);
    ["F", "D", "G"].forEach((k) => {
      s.players.filter((q) => q.p === k && q.prob > 0 && (q.proj !== false || q.gp > 0)).map((q) => [q.id, pv(q)]).sort((a, b) => b[1] - a[1]).forEach((x, i) => (o[x[0]] = i + 1));
    });
    return o;
  }, [s.players, K, window.__PMODE]);
  useEffect(() => { setTab("ov"); setNLog(10); setImg(true); }, [p.id]);
  useEffect(() => { const k = (e) => { if (e.key === "Escape") onClose(); }; window.addEventListener("keydown", k); return () => window.removeEventListener("keydown", k); }, []);
  useEffect(() => {
    let dead = false;
    setLog(null);
    if (!eid) { setLog([]); return; }
    const past = [...((SCHED && SCHED[p.t]) || [])].filter((d) => d <= today).sort().reverse();
    gxBoxIdx().then((idx) => {
      const has = new Set(idx || []);
      return Promise.all(past.map((d) => {
        const live = pStat(p, d);
        return has.has(d) ? gxBoxDay(d).then((day) => ({ d, x: (day && day[eid]) || live })) : Promise.resolve({ d, x: live });
      }));
    }).then((list) => {
      if (dead) return;
      setLog(list.filter((r) => r.x).map((r) => {
        const a = r.x.fp != null ? r.x.fp : gxPdReal(p, r.d);
        return { ...r, fp: a != null ? a : gxEst(r.x, sc), est: a == null, st: gState(p.t, r.d).s };
      }));
    }).catch(() => { if (!dead) setLog([]); });
    return () => { dead = true; };
  }, [p.id]);

  // header facts
  const sp = String(p.n || "").indexOf(" "), first = sp > 0 ? p.n.slice(0, sp) : "", last = sp > 0 ? p.n.slice(sp + 1) : p.n;
  const no = gxPdNo(p), nhlPos = gxPdNhlPos(p);
  const T = gxPdTeam(p.t), tName = (T.st || {}).name || p.t;
  const back = eid ? effBack(p) : { d: "" };
  const hurt = !!(p.ir || (p.status && p.status !== "ACTIVE") || (back.d && back.d > today));
  const stTxt = !hurt ? "Healthy" : p.ir ? "Injured reserve" : p.status === "DAY_TO_DAY" ? "Day to day" : p.status === "OUT" ? "Out" : p.status === "SUSPENSION" ? "Suspended" : p.status === "INJURY_RESERVE" ? "Injured reserve" : "Not playing";
  const stCol = !hurt ? "var(--good)" : p.status === "DAY_TO_DAY" ? "var(--warn)" : "var(--bad)";
  const posWord = isG ? "G" : p.p === "D" ? "D" : "F";
  const elig = posWord + (nhlPos && nhlPos[0] !== posWord ? " (" + nhlPos.replace(/[LR]$/, "") + ")" : "");
  const rk = rank[p.id];
  const avgSoFar = p.gp ? p.tot / p.gp : null;
  const proj = eid ? effAvg(p, K) : null;
  const inj = eid ? (((window.__SIG || {}).injuries) || {})[eid] : null;
  const news = eid ? (sigOf(p).news || []) : [];

  // this week and next games
  const per = (d) => { if (!eid) return null; const g = isG ? gStart(p, d) : null; return { x: effAvg(p, K, d) * (g ? g.v : (p.prob != null ? p.prob : 1)) * avail(p, d), g }; };
  const wkIdx = eid && wk && wk.games ? (wk.games[p.t] || []).filter((i) => ((wk.dates || [])[i] || "") >= today && gState(p.t, wk.dates[i]).s === "P") : [];
  const wkPts = wkIdx.reduce((a, i) => a + ((per(wk.dates[i]) || {}).x || 0), 0);
  const L = window.LINES_DATA || {};
  const nextG = ((L.sched || {})[p.t] || []).filter((x) => x.d >= today).slice(0, 5);

  // stats rows
  const rows = log || [];
  const done = rows;
  const since = (n) => done.filter((r) => r.d >= addDays(today, -(n - 1)));
  const statRows = [["Season", gxPdSum(done, isG)], ["Last 7 days", gxPdSum(since(7), isG)], ["Last 15 days", gxPdSum(since(15), isG)]];
  const SH = isG ? ["GP", "W", "L", "GA", "SV", "SV%", "FPTS"] : ["GP", "ATOI", "G", "A", "+/-", "PIM", "SOG", "FPTS"];
  const svp = (v) => (v == null ? "-" : v.toFixed(3).replace(/^0/, ""));
  const statCells = (r) => (isG ? [r.gp, r.w, r.l, r.ga, r.sv, svp(r.svp), f1(r.fp)] : [r.gp, gxPdMS(r.toi), r.g, r.a, gxPdSigned(r.pm), r.pim, r.sog, f1(r.fp)]);

  // lines
  const ln = T.lines || {}, me = nrm(p.n);
  const slots = Object.keys(ln).filter((k) => (ln[k] || []).some((n) => nrm(n) === me));
  const mateP = (n) => s.players.find((q) => nrm(q.n) === nrm(n) && q.t === p.t) || s.players.find((q) => nrm(q.n) === nrm(n));
  const chg = ((L.changes || []).filter((c) => nrm(c.name) === me && (c.team === p.t || c.from === p.t || c.to === p.t))).slice(0, 6);

  const Q = window.__QA;
  const act = (fn) => () => { onClose(); fn(p); };
  const owner = p.ft === "fa" ? (p.wv ? "Waivers" : "Free agent") : <TL s={s} id={p.ft} />;
  const tabs = [["ov", "Overview"], ["log", "Game log"], ["news", "News" + (news.length ? " (" + news.length + ")" : "")], ["lines", "Lines"]];

  return (
    <div className="gx-pd-ov" onClick={onClose}>
      <div className="gx-pd" data-gx="095" onClick={(e) => e.stopPropagation()}>
        <button type="button" className="gx-pd-x" aria-label="Close" onClick={onClose}>{String.fromCharCode(215)}</button>
        <div className="gx-pd-hd">
          <div className="gx-pd-ph">
            <span className="lg"><TeamLogo t={p.t} size={44} /></span>
            {eid && img ? <img alt={p.n} src={"https://a.espncdn.com/i/headshots/nhl/players/full/" + eid + ".png"} onError={() => setImg(false)} />
              : <span className="ini">{(first[0] || "") + (last[0] || "")}</span>}
          </div>
          <div className="min-w-0">
            <div className="gx-pd-nm">
              {no != null ? <span className="gx-pd-no">{"#" + no}</span> : null}
              <div className="min-w-0"><div className="f truncate">{first}</div><div className="l truncate">{last}</div></div>
            </div>
            <div className="gx-pd-tm truncate">{tName}</div>
            <div className="gx-pd-kv">
              <span className="k">Elig</span><span>{elig}</span>
              <span className="k">Manager</span><span className="truncate">{owner}</span>
              <span className="k">Status</span><span>{stTxt}<span className="gx-pd-dot" style={{ background: stCol }}></span></span>
            </div>
          </div>
          <div className="gx-pd-st">
            <div><div className="k">Position rank</div><div className="v">{rk || "-"}<small>{rk ? posWord : ""}</small></div></div>
            <div><div className="k">Average points</div><div className="v">{avgSoFar == null ? "-" : f1(avgSoFar)}</div></div>
            <div><div className="k">Projected</div><div className="v">{proj == null ? "-" : f1(proj)}</div></div>
            <div><div className="k">% rostered</div><div className="v">{p.own != null ? f1(p.own) : "-"}<small>{p.chg ? "(" + (p.chg > 0 ? "+" : "") + f1(p.chg) + ")" : "(+0)"}</small></div></div>
          </div>
        </div>
        {Q ? (
          <div className="gx-pd-ac">
            <button type="button" className="pr" onClick={act(Q.swap)}>{Q.mine(p) ? "Find a replacement" : "Find a swap"}</button>
            {Q.tradeable(p) ? <button type="button" onClick={act(Q.trade)}>Add to a trade</button> : null}
            <button type="button" onClick={() => Q.espn(p)}>{Q.fa(p) ? "Add on ESPN" : "Open on ESPN"}</button>
            {Q.fa(p) ? <GxPdWatch p={p} Q={Q} /> : null}
          </div>
        ) : null}
        <div className="gx-pd-tb">
          {tabs.map(([k, l]) => <button key={k} type="button" className={tab === k ? "on" : ""} onClick={() => setTab(k)}>{l}</button>)}
        </div>
        <div className="gx-pd-bd">
          {hurt && tab === "ov" ? (
            <div className="gx-pd-pn" style={{ color: "var(--bad)", fontSize: 14 }}>
              {stTxt}{back.d ? GXPD_DOT + "back around " + dayLabel(back.d) : ""}{inj && inj.note ? GXPD_DOT + inj.note : ""}
            </div>
          ) : null}

          {tab === "ov" ? (<>
            <div className="gx-pd-pn">
              <div className="gx-pd-h">Stats<span className="r">fantasy points (FPTS) by your league's scoring</span></div>
              {log === null ? <div className="text-sm text-slate-500">Loading games...</div> : (
                <table className="gx-pd-t"><thead><tr><th></th>{SH.map((h) => <th key={h}>{h}</th>)}</tr></thead>
                  <tbody>{statRows.map(([l, r]) => <tr key={l}><td>{l}</td>{statCells(r).map((v, i) => <td key={i} className={i === SH.length - 1 ? "b" : ""}>{r.gp ? v : i ? "-" : 0}</td>)}</tr>)}</tbody>
                </table>
              )}
            </div>
            <div className="gx-pd-pn">
              <div className="gx-pd-h">This week</div>
              <div className="gx-pd-tl">
                <div><div className="k">Per game</div><div className="v">{proj == null ? "-" : f1(proj)}</div><div className="s">{isG ? "if he starts" : "ESPN " + f1(p.avg || 0)}</div></div>
                <div><div className="k">Rest of this week</div><div className="v">{eid ? f1(wkPts) : "-"}</div><div className="s">{wkIdx.length + " game" + (wkIdx.length === 1 ? "" : "s") + " left"}</div></div>
                <div><div className="k">Season points</div><div className="v">{f1(p.tot || 0)}</div><div className="s">{(p.gp || 0) + " GP"}</div></div>
              </div>
              {nextG.length ? (
                <table className="gx-pd-t" style={{ marginTop: 10 }}><thead><tr><th>Next games</th><th>Opp</th><th>{isG ? "Start" : ""}</th><th>Proj</th></tr></thead>
                  <tbody>{nextG.map((g) => { const r = per(g.d), lv = gState(p.t, g.d).s !== "P", a = lv ? gxPdReal(p, g.d) : null; return (
                    <tr key={g.d} className={lv ? "lv" : ""}>
                      <td>{dayLabel(g.d)}</td>
                      <td><span className="inline-flex items-center gap-1 justify-end">{g.h ? "vs" : "@"} <TeamLogo t={g.o} size={16} /> {g.o}</span></td>
                      <td className="text-slate-500">{isG && r && r.g ? Math.round(r.g.v * 100) + "%" : ""}</td>
                      <td className="b">{lv ? <>{a == null ? "-" : f1(a)} <LiveTag st={gState(p.t, g.d).s} t={p.t} dt={g.d} /></> : r ? f1(r.x) : ""}</td>
                    </tr>); })}</tbody>
                </table>
              ) : null}
              {eid ? <div style={{ marginTop: 8 }}><Tags p={p} K={K} /></div> : null}
            </div>
            {news.length ? (
              <div className="gx-pd-pn">
                <div className="gx-pd-h">Latest news<button type="button" className="r text-blue-600" onClick={() => setTab("news")}>All news</button></div>
                <GxPdNews items={news.slice(0, 1)} />
              </div>
            ) : null}
          </>) : null}

          {tab === "log" ? (
            <div className="gx-pd-pn">
              <div className="gx-pd-h">Game log<span className="r">{log && log.length ? log.length + " games" : ""}</span></div>
              {log === null ? <div className="text-sm text-slate-500">Loading games...</div>
                : !log.length ? <div className="text-sm text-slate-500">No games saved yet.</div> : (<>
                <table className="gx-pd-t">
                  <thead><tr><th>Date</th><th>Opp</th>{isG ? <><th>Dec</th><th>SV</th><th>GA</th><th className="m-hide">SV%</th></> : <><th className="m-hide">TOI</th><th>G</th><th>A</th><th>+/-</th><th className="m-hide">PIM</th><th>SOG</th></>}<th>FPTS</th></tr></thead>
                  <tbody>{log.slice(0, nLog).map((r) => { const x = r.x, gm = ((((window.GAMES_DATA || {}).games || {})[r.d]) || {})[p.t] || null, o = x.o || (gm ? gm.o : ""), h = x.o ? x.h : gm ? gm.h : null; return (
                    <tr key={r.d} className={r.st === "L" ? "lv" : ""}>
                      <td>{r.d.slice(5).replace("-", "/")}</td>
                      <td>{o ? (h ? "" : "@") + o : ""}</td>
                      {isG ? <><td>{x.dec === "O" ? "OTL" : x.dec || "-"}</td><td>{x.sv || 0}</td><td>{x.ga || 0}</td><td className="m-hide">{x.svp != null ? svp(Number(x.svp)) : "-"}</td></>
                        : <><td className="m-hide">{x.toi || "-"}</td><td>{x.g || 0}</td><td>{x.a || 0}</td><td>{gxPdSigned(x.pm)}</td><td className="m-hide">{x.pim || 0}</td><td>{x.sog || 0}</td></>}
                      <td className="b">{f1(r.fp)}{r.est ? "*" : ""}</td>
                    </tr>); })}</tbody>
                </table>
                {log.length > nLog ? <button type="button" className="gx-pd-more" onClick={() => setNLog(nLog + 20)}>Show more</button> : null}
                {log.some((r) => r.est) ? <div className="text-xs text-slate-500" style={{ marginTop: 8 }}>* worked out from the box score, without power-play or shorthanded points.</div> : null}
              </>)}
            </div>
          ) : null}

          {tab === "news" ? (
            <div className="gx-pd-pn">
              <div className="gx-pd-h">Recent news</div>
              {inj && inj.note ? <div className="gx-pd-nw"><div className="d">Injury</div><div style={{ color: "var(--bad)" }}>{inj.note}</div></div> : null}
              {news.length ? <GxPdNews items={news} /> : !(inj && inj.note) ? <div className="text-sm text-slate-500">No news for him in the last few days.</div> : null}
            </div>
          ) : null}

          {tab === "lines" ? (<>
            <div className="gx-pd-pn">
              <div className="gx-pd-h">{"Where he plays for " + p.t}<button type="button" className="r text-blue-600" onClick={act(() => window.__NAV && window.__NAV.lines(p.t))}>All team lines</button></div>
              {!slots.length ? <div className="text-sm" style={{ color: "var(--warn)" }}>{"Not in " + p.t + "'s current Daily Faceoff lineup (scratched, injured, in the minors, or not read yet)."}</div>
                : slots.sort().map((k) => (
                  <div key={k} className="gx-pd-nw">
                    <div className="d">{GX_PD_SLOT[k] || k}</div>
                    <div>{(ln[k] || []).filter((n) => nrm(n) !== me).map((n) => { const q = mateP(n); return q ? <button key={n} type="button" className="gx-pd-mt" onClick={() => window.__NAV && window.__NAV.player(q)}>{n}</button> : <span key={n} className="gx-pd-mt text-slate-500">{n}</span>; })}</div>
                  </div>
                ))}
              {!isG && slots.length && !slots.some((k) => k[0] === "P") ? <div className="text-xs text-slate-500" style={{ marginTop: 6 }}>Not on a power-play or penalty-kill unit.</div> : null}
            </div>
            {chg.length ? (
              <div className="gx-pd-pn">
                <div className="gx-pd-h">Recent changes</div>
                {chg.map((c) => <div key={c.id} className="gx-pd-nw"><div className="d">{dayLabel(String(c.at || "").slice(0, 10))}</div><div>{c.text}</div></div>)}
              </div>
            ) : null}
          </>) : null}
        </div>
      </div>
    </div>
  );
}
function GxPdNews({ items }) {
  return items.map((n, i) => (
    <div key={i} className="gx-pd-nw">
      <div className="d">{n.d}</div>
      <a href={n.u} target="_blank" rel="noreferrer" style={{ color: n.tone === "-" ? "var(--bad)" : "var(--ink)" }}>{n.h}</a>
    </div>
  ));
}
function GxPdWatch({ p, Q }) {
  const [, tick] = useState(0);
  return <button type="button" onClick={() => { Q.star(p); tick((x) => x + 1); }}>{Q.starred(p) ? "Watching" : "Watch"}</button>;
}
// if the new screen ever breaks, fall back to the old pop-up
class GxPdSafe extends React.Component {
  constructor(props) { super(props); this.state = { bad: false }; }
  static getDerivedStateFromError() { return { bad: true }; }
  componentDidCatch(e) { try { console.error("player screen (095)", e); } catch (x) {} }
  render() {
    const P = this.props;
    if (this.state.bad) return window.PlayerPopup ? <window.PlayerPopup p={P.p} s={P.s} wk={P.wk} H={P.H} onClose={P.onClose} /> : null;
    return <GxPlayerDetail p={P.p} s={P.s} wk={P.wk} onClose={P.onClose} />;
  }
}
'''

OLD_POP = '{player && window.PlayerPopup ? <window.PlayerPopup p={player} s={s} wk={wk} H={LH} onClose={() => setPlayer(null)} /> : null}'
NEW_POP = '{player ? <GxPdSafe key={player.id} p={player} s={s} wk={wk} H={LH} onClose={() => setPlayer(null)} /> : null}'


def change(t):
    t = lit(t, "095: styles", "</style>", NEW_CSS, "change 095 (install.py)")
    t = lit(t, "095: helpers", ROOT, HELPERS + ROOT, "change 095: ESPN-style player screen")
    t = lit(t, "095: open the new screen", OLD_POP, NEW_POP, "<GxPdSafe key={player.id}")
    return t


edit(APP, change)


# save each player's jersey number with the NHL roster, and pass it to the app
def lines(t):
    t = lit(t, "095: jersey number",
            'pl[str(x["id"])] = {"n": n, "p": pos, "pc": x.get("positionCode") or "", "sh": x.get("shootsCatches") or ""}',
            'pl[str(x["id"])] = {"n": n, "p": pos, "pc": x.get("positionCode") or "", "sh": x.get("shootsCatches") or "", "no": x.get("sweaterNumber")}',
            '"no": x.get("sweaterNumber")')
    t = lit(t, "095: numbers to the app",
            '"roster": len(rosters.get(t) or {}), "pos": team_pos(t, state, rosters)}',
            '"roster": len(rosters.get(t) or {}), "pos": team_pos(t, state, rosters),\n                    "no": {v["n"]: v["no"] for v in (rosters.get(t) or {}).values() if v.get("no") is not None}}',
            '"no": {v["n"]: v["no"] for v in')
    return t


edit("gm_lines.py", lines)
