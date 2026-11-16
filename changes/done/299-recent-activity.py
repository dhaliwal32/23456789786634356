# changes/299-recent-activity.py - Setup: League activity section with every pickup, drop and trade in the last 7 days; tap one for its effect (win chance this week before and after, points added this week and rest of season, points scored since the move, strength rank before and after) and, for trades, each team's vote

NEW_CSS = r'''  /* change 299 (install.py) */
  .gx-ac299 .hd { display: flex; align-items: center; justify-content: space-between; gap: 10px; margin-bottom: 4px; }
  .gx-ac299 .rw { display: grid; grid-template-columns: auto minmax(0,1fr) auto; align-items: center; gap: 10px; width: 100%; min-height: 58px; padding: 6px 0; border-top: 1px solid var(--line); color: var(--ink); text-align: left; }
  .gx-ac299 .rw:first-of-type { border-top: 0; }
  .gx-ac299 .rw .tx { min-width: 0; }
  .gx-ac299 .rw .tx b { display: block; font-size: 14px; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .gx-ac299 .rw .tx small { display: block; font-size: 12px; color: var(--mute); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .gx-ac299 .rw .wh { font-size: 12px; color: var(--mute); white-space: nowrap; text-align: right; }
  .gx-ac299 .ad, .gx-ad299 .ad { color: var(--good); } .gx-ac299 .dr, .gx-ad299 .dr { color: var(--bad); }
  .gx-ac299 .mr { width: 100%; height: 40px; margin-top: 8px; border: 1px solid var(--line2); border-radius: 10px; font-size: 13.5px; color: var(--ink); }
  .gx-ac299 .em { font-size: 13.5px; color: var(--mute); padding: 8px 0; }
  .gx-ad299 .sc { font-size: 12px; color: var(--mute); letter-spacing: .04em; padding: 14px 0 4px; }
  .gx-ad299 .pr { display: grid; grid-template-columns: auto minmax(0,1fr) auto; align-items: center; gap: 10px; height: 50px; width: 100%; text-align: left; color: var(--ink); }
  .gx-ad299 .pr b { display: block; font-size: 14px; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .gx-ad299 .pr small { display: block; font-size: 12px; color: var(--mute); }
  .gx-ad299 .gr { display: grid; grid-template-columns: minmax(0,1fr) minmax(0,1fr); gap: 8px; }
  .gx-ad299 .tl { background: var(--card2); border-radius: 12px; padding: 10px 12px; min-width: 0; }
  .gx-ad299 .tl small { display: block; font-size: 12px; color: var(--mute); }
  .gx-ad299 .tl b { display: block; font-size: 17px; font-weight: 600; margin-top: 2px; font-variant-numeric: tabular-nums; white-space: nowrap; }
  .gx-ad299 .tl i { font-style: normal; font-size: 12px; color: var(--mute); font-weight: 400; }
  .gx-ad299 .vt { display: flex; align-items: center; gap: 10px; height: 40px; border-top: 1px solid var(--line); font-size: 14px; }
  .gx-ad299 .vt span { flex: 1; min-width: 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .gx-ad299 .vt em { font-style: normal; font-size: 13px; }
</style>'''

HELPERS = r'''// ---------- change 299: League activity in Setup (install.py) ----------
const gxTm299 = (s, n) => { const t = s.teams.find((x) => String(x.id).replace(/^t/, "") === String(n)); return t ? t.id : null; };
const gxPl299 = (s, id) => s.players.find((p) => String(p.id).replace(/^e/, "") === String(id)) || null;
const GX_ST299 = { EXECUTED: "Done", PENDING: "Waiting for votes", VETOED: "Vetoed", CANCELED: "Cancelled", FAILED_INVALIDPLAYERSOURCE: "Failed", FAILED_ROSTERLIMIT: "Failed" };
// every pickup, drop and trade in the last 7 days, newest first
function gxAct299(s) {
  const tx = ((window.ESPN_DATA || {}).tx) || [], cut = Date.now() - 7 * 864e5, out = [], votes = {};
  tx.forEach((t) => { if (/^TRADE_(UPHOLD|VETO)/.test(t.ty) && t.rel) (votes[t.rel] = votes[t.rel] || []).push({ tm: gxTm299(s, t.tm), up: /UPHOLD/.test(t.ty), at: t.at }); });
  const byId = {}; tx.forEach((t) => (byId[t.id] = t));
  const seenTrade = {};
  tx.forEach((t) => {
    if (!t.at || t.at < cut) return;
    if ((t.ty === "FREEAGENT" || t.ty === "WAIVER") && t.st === "EXECUTED") {
      const add = (t.it || []).find((i) => i[1] === "ADD"), drop = (t.it || []).find((i) => i[1] === "DROP");
      out.push({ k: t.id, kind: "move", at: t.at, tm: gxTm299(s, t.tm), add: add ? gxPl299(s, add[0]) : null, drop: drop ? gxPl299(s, drop[0]) : null, waiver: t.ty === "WAIVER" });
    } else if (t.ty === "TRADE_ACCEPT" || (t.ty === "TRADE_PROPOSAL" && /EXECUTED|VETOED|PENDING/.test(String(t.st || "")) && (votes[t.id] || []).length)) {
      const root = t.ty === "TRADE_ACCEPT" && t.rel && byId[t.rel] ? byId[t.rel] : t;
      if (seenTrade[root.id]) return;
      seenTrade[root.id] = 1;
      const items = (root.it && root.it.length ? root.it : t.it) || [];
      const sides = {};
      items.forEach((i) => { if (i[1] !== "TRADE" && i[1] !== "ADD") return; const to = gxTm299(s, i[3]); if (!to) return; (sides[to] = sides[to] || []).push(gxPl299(s, i[0])); });
      const v = [...(votes[root.id] || []), ...(t.id !== root.id ? votes[t.id] || [] : [])];
      out.push({ k: root.id, kind: "trade", at: t.at, st: t.ty === "TRADE_ACCEPT" ? t.st || "PENDING" : root.st, sides, votes: v }); /* ESPN leaves an accepted trade's status empty while votes are open */
    }
  });
  out.sort((a, b) => b.at - a.at);
  return out;
}
// what a move did for that team (worked out when you tap it)
function gxMoveFx299(s, m) {
  const T = m.tm, sT = { ...s, me: T, opp: null }, nR = s.weeks.length - s.wk;
  const after = s.players, before = s.players.map((p) => (m.add && p.id === m.add.id ? { ...p, ft: "fa" } : m.drop && p.id === m.drop.id ? { ...p, ft: T } : p));
  const rA = after.filter((p) => p.ft === T), rB = before.filter((p) => p.ft === T);
  const out = {};
  try { out.wb = winChance(sT, rB); out.wa = winChance(sT, rA); } catch (e) {}
  try { out.wk = horizonTotal(rA, sT, 1) - horizonTotal(rB, sT, 1); out.ros = horizonTotal(rA, sT, nR) - horizonTotal(rB, sT, nR); } catch (e) {}
  try { const rk = (pl) => { const L = leagueTable({ ...s, players: pl }).rows || []; return L.findIndex((x) => x.t.id === T) + 1; }; out.rb = rk(before); out.ra = rk(after); } catch (e) {}
  return out;
}
function gxTradeFx299(s, m) {
  const nR = s.weeks.length - s.wk, ids = Object.keys(m.sides), out = {};
  if (ids.length !== 2) return out;
  const moved = {}; ids.forEach((to) => (m.sides[to] || []).forEach((p) => { if (p) moved[p.id] = to; }));
  const from = {}; ids.forEach((to) => (m.sides[to] || []).forEach((p) => { if (p) from[p.id] = ids.find((x) => x !== to); }));
  const before = s.players.map((p) => (from[p.id] ? { ...p, ft: from[p.id] } : p));
  ids.forEach((T) => { try { const sT = { ...s, me: T, opp: null }; out[T] = horizonTotal(s.players.filter((p) => p.ft === T), sT, nR) - horizonTotal(before.filter((p) => p.ft === T), sT, nR); } catch (e) {} });
  return out;
}
// fantasy points a player has scored since a day (box scores, one file a day)
function gxSince299(s, p, fromIso) {
  if (!p) return Promise.resolve(null);
  const id = String(p.id).replace(/^e/, "");
  return gxBoxIdx().then((ds) => Promise.all((ds || []).filter((d) => d >= fromIso).map((d) => gxBoxDay(d)))).then((days) => {
    let pts = 0, gp = 0;
    days.forEach((m) => { const x = m && m[id]; if (x) { pts += x.fp != null ? x.fp : gxEst(x, s.sc || {}); gp++; } });
    return { pts, gp };
  }).catch(() => null);
}
const gxDay299 = (ms) => { try { const d = new Date(ms); return gxWhen(d.toISOString()); } catch (e) { return ""; } };
function GxActSheet299({ s, m, onClose }) {
  const [out, setOut] = useState(false);
  const [fx, setFx] = useState(null);
  const [since, setSince] = useState(null);
  const close = () => { if (out) return; setOut(true); setTimeout(onClose, 180); };
  useEffect(() => { const k = (e) => { if (e.key === "Escape") close(); }; window.addEventListener("keydown", k); return () => window.removeEventListener("keydown", k); }, [out]);
  useEffect(() => {
    const id = setTimeout(() => { try { setFx(m.kind === "move" ? gxMoveFx299(s, m) : gxTradeFx299(s, m)); } catch (e) { setFx({}); } }, 60);
    if (m.kind === "move") { const d0 = iso(new Date(m.at)); Promise.all([gxSince299(s, m.add, d0), gxSince299(s, m.drop, d0)]).then((v) => setSince(v)); }
    return () => clearTimeout(id);
  }, [m.k]);
  const sg = (v) => (v == null || isNaN(v) ? "\u2013" : (v >= 0 ? "+" : "\u2212") + f1(Math.abs(v)));
  const pr = (p, tag) => p ? (
    <button type="button" className="pr" onClick={() => { if (window.__NAV) { try { document.documentElement.classList.add("gx-pt281"); } catch (e) {} window.__NAV.player(p); } }}>
      <GxFace p={p} size={24} /><span style={{ minWidth: 0 }}><b>{p.n}</b><small>{p.t + " \u00b7 " + p.p + " \u00b7 " + f1(gxPgAvg(p, s.blend)) + " a game"}</small></span><span className={tag === "Added" ? "ad" : "dr"} style={{ fontSize: 13 }}>{tag}</span>
    </button>
  ) : null;
  const body = m.kind === "move" ? (
    <>
      <div className="sc">THE MOVE</div>{pr(m.add, "Added")}{pr(m.drop, "Dropped")}
      <div className="sc">WHAT IT DID FOR {String(teamName(s, m.tm)).toUpperCase()}</div>
      {!fx ? <div className="tl"><small>Working it out...</small></div> : (
        <div className="gr">
          <div className="tl"><small>Win chance this week</small><b>{fx.wb == null ? "\u2013" : wpTxt(fx.wb) + " \u2192 " + wpTxt(fx.wa)}</b></div>
          <div className="tl"><small>Strength rank</small><b>{fx.rb ? ordN(fx.rb) + " \u2192 " + ordN(fx.ra) : "\u2013"}</b></div>
          <div className="tl"><small>Points this week</small><b>{sg(fx.wk)}</b></div>
          <div className="tl"><small>Points rest of season</small><b>{sg(fx.ros)}</b></div>
        </div>
      )}
      <div className="sc">SINCE THE MOVE</div>
      <div className="gr">
        <div className="tl"><small>{m.add ? lastN(m.add.n) + " (added)" : "Added"}</small><b>{since && since[0] ? f1(since[0].pts) : "\u2013"} <i>{since && since[0] ? since[0].gp + " GP" : ""}</i></b></div>
        <div className="tl"><small>{m.drop ? lastN(m.drop.n) + " (dropped)" : "Dropped"}</small><b>{since && since[1] ? f1(since[1].pts) : "\u2013"} <i>{since && since[1] ? since[1].gp + " GP" : ""}</i></b></div>
      </div>
    </>
  ) : (
    <>
      {Object.keys(m.sides).map((T) => (
        <React.Fragment key={T}>
          <div className="sc">{String(teamName(s, T)).toUpperCase() + " GETS"}</div>
          {(m.sides[T] || []).map((p, j) => (p ? <React.Fragment key={j}>{pr(p, "Added")}</React.Fragment> : null))}
          <div className="tl" style={{ marginTop: 4 }}><small>Points rest of season</small><b>{fx ? sg(fx[T]) : "\u2026"}</b></div>
        </React.Fragment>
      ))}
      <div className="sc">{"VOTES \u00b7 " + (GX_ST299[m.st] || m.st || "")}</div>
      {m.votes.length ? m.votes.map((v, j) => <div key={j} className="vt"><GxFtPic114 id={v.tm} size={22} /><span>{teamName(s, v.tm)}</span><em className={v.up ? "ad" : "dr"}>{v.up ? "Uphold" : "Veto"}</em></div>)
        : <div className="tl"><small>No votes ESPN shows yet. If the league hides who voted, only the result appears here.</small></div>}
    </>
  );
  return ReactDOM.createPortal(
    <div className={"gx-sx289 gx-ad299 fixed inset-0" + (out ? " out" : "")} onClick={close}>
      <div className="pn" onClick={(e) => e.stopPropagation()}>
        <div className="tt"><b>{m.kind === "move" ? teamName(s, m.tm) : "Trade"}</b><button type="button" aria-label="Close" onClick={close}>{"\u00d7"}</button></div>
        <div className="nt">{gxDay299(m.at) + (m.waiver ? " \u00b7 waiver claim" : "")}</div>
        {body}
      </div>
    </div>, document.body);
}
function GxAct299({ s }) {
  const [mine, setMine] = useState(false);
  const [n, setN] = useState(5);
  const [sel, setSel] = useState(null);
  const gen = (window.ESPN_DATA || {}).generated;
  const all = useMemo(() => { try { return gxAct299(s); } catch (e) { return []; } }, [gen, s.players]);
  const has = !!((window.ESPN_DATA || {}).tx);
  const list = mine ? all.filter((m) => m.tm === s.me || (m.sides && m.sides[s.me])) : all;
  const nm = (p) => (p ? p.n : "someone");
  return (
    <>
      <div className="gx-tag gx-st275">League activity</div>
      <div className="gx-pn gx-ac299" data-gx="299">
        <div className="hd"><span className="text-xs text-slate-500">Last 7 days</span><span className="gx-seg">{[[false, "All teams"], [true, "Mine"]].map(([k, l]) => <button key={l} type="button" className={mine === k ? "on" : ""} onClick={() => { setMine(k); setN(5); }}>{l}</button>)}</span></div>
        {!has ? <div className="em">Shows after the next sync.</div> : !list.length ? <div className="em">No pickups, drops or trades in the last 7 days.</div> : list.slice(0, n).map((m) => (
          <button key={m.k} type="button" className="rw" onClick={() => setSel(m)}>
            {m.kind === "move" ? <GxFtPic114 id={m.tm} size={30} /> : <span style={{ width: 30, height: 30, borderRadius: 8, background: "var(--card3)", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 15 }}>{"\u21c4"}</span>}
            <span className="tx">
              {m.kind === "move" ? <><b>{m.add ? <><span className="ad">+</span>{" " + m.add.n}</> : <><span className="dr">{"\u2212"}</span>{" " + nm(m.drop)}</>}</b><small>{teamName(s, m.tm) + (m.add && m.drop ? " \u00b7 dropped " + m.drop.n : "")}</small></>
                : <><b>{Object.keys(m.sides).map((T) => teamName(s, T)).join(" \u21c4 ")}</b><small>{(GX_ST299[m.st] || m.st || "Trade") + (m.votes.length ? " \u00b7 " + m.votes.filter((v) => v.up).length + " uphold, " + m.votes.filter((v) => !v.up).length + " veto" : "")}</small></>}
            </span>
            <span className="wh">{gxDay299(m.at)}</span>
          </button>
        ))}
        {list.length > n ? <button type="button" className="mr" onClick={() => setN(n + 10)}>{"Show more (" + (list.length - n) + ")"}</button> : null}
      </div>
      {sel ? <GxActSheet299 s={s} m={sel} onClose={() => setSel(null)} /> : null}
    </>
  );
}
'''

POS_OLD = r'''      {/* change 295: My team and Favourite team are in More */}'''
POS_NEW = r'''      <GxAct299 s={s} />{/* change 299 */}
''' + POS_OLD


def change(t):
    t = lit(t, "299: styles", "</style>", NEW_CSS, "change 299 (install.py)")
    t = lit(t, "299: helpers", ROOT, HELPERS + ROOT, "change 299: League activity in Setup")
    t = lit(t, "299: on the Setup page", POS_OLD, POS_NEW, "<GxAct299 s={s} />")
    return t

edit(APP, change)
