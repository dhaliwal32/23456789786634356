# changes/293-live-first-watchlist-trade-ideas.py - live tracker shows the newest play the moment ESPN has it (no stepping, the puck goes straight to the real spot and stays near it); scores are checked every 20 seconds between games; the watchlist is hidden until you pick Watchlist in Filters; Trades shows trade ideas (one-for-one swaps that make both lineups stronger) in the empty space

NEW_CSS = r'''  /* change 293 (install.py) */
  .gx-ti293 .hd { display: flex; align-items: baseline; justify-content: space-between; gap: 10px; }
  .gx-ti293 .hd small { font-size: 12px; color: var(--mute); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .gx-ti293 .rw { display: grid; grid-template-columns: minmax(0,1fr) auto; align-items: center; gap: 12px; width: 100%; height: 64px; border-top: 1px solid var(--line); color: var(--ink); text-align: left; font-variant-numeric: tabular-nums; }
  .gx-ti293 .rw:first-of-type { border-top: 0; }
  .gx-ti293 .sw { min-width: 0; display: grid; grid-template-columns: 40px auto minmax(0,1fr); align-items: center; gap: 2px 8px; }
  .gx-ti293 .sw small { font-size: 11.5px; color: var(--mute); }
  .gx-ti293 .sw b { font-size: 14px; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .gx-ti293 .nm { text-align: right; font-size: 12px; color: var(--mute); white-space: nowrap; }
  .gx-ti293 .nm b { display: block; font-size: 14px; font-weight: 600; color: var(--ink); }
  .gx-ti293 .em { font-size: 13.5px; color: var(--mute); padding: 8px 0 2px; }
</style>'''

HELPERS = r'''// ---------- change 293: trade ideas, watchlist behind Filters (install.py) ----------
// one-for-one swaps that the trade builder itself scores as good for both teams (points, rest of season)
// step 1: a quick look at every swap with every team to pick the 36 most promising; step 2: score those the builder's way, a few at a time
function gxIdeas293(s, done) {
  const K = s.blend, today = todayISO(), N = { F: 10, D: 5, G: 2 }, nR = s.weeks.length - s.wk;
  const val = (p) => effAvg(p, K) * (p.p === "G" ? p.prob : 1);
  const ok = (p) => !p.ir && avail(p, today) > 0;
  const str = (r) => ["F", "D", "G"].reduce((t, k) => t + r.filter((p) => p.p === k && ok(p)).map(val).sort((a, b) => b - a).slice(0, N[k]).reduce((a, b) => a + b, 0), 0);
  const A = s.players.filter((p) => p.ft === s.me), a0 = str(A), cand = [], teams = {};
  s.teams.filter((t) => t.id !== s.me).forEach((tm) => {
    const B = s.players.filter((p) => p.ft === tm.id), b0 = str(B);
    teams[tm.id] = B;
    A.filter((p) => ok(p) && !p.keep).forEach((x) => B.filter(ok).forEach((y) => {
      const da = str(A.filter((p) => p.id !== x.id).concat([y])) - a0, db = str(B.filter((p) => p.id !== y.id).concat([x])) - b0;
      if (da > -0.3 && db > -0.3) cand.push({ x, y, tm: tm.id, q: Math.min(da, db) + (da + db) / 4 });
    }));
  });
  cand.sort((u, v) => v.q - u.q);
  const top = cand.slice(0, 36), tD = gxTradeDay(), live = (r) => r.map((p) => (p.ir ? { ...p, ir: false } : p));
  const base = {}, tot = (id, r) => (base[id] != null ? base[id] : (base[id] = horizonTotal(live(r), s, nR)));
  const good = [];
  let i = 0, dead = false;
  const step = () => {
    if (dead) return;
    const end = Math.min(top.length, i + 4);
    for (; i < end; i++) {
      const o = top[i], B = teams[o.tm];
      try {
        const my = horizonTotal(live(gxTimed(A, A.filter((p) => p.id !== o.x.id).concat([{ ...o.y, ft: s.me }]), tD)), s, nR) - tot(s.me, A);
        const th = horizonTotal(live(gxTimed(B, B.filter((p) => p.id !== o.y.id).concat([{ ...o.x, ft: o.tm }]), tD)), s, nR) - tot(o.tm, B);
        if (my >= 2 && th >= 2) good.push({ x: o.x, y: o.y, tm: o.tm, my, th });
      } catch (e) {}
    }
    if (i < top.length) { setTimeout(step, 0); return; }
    good.sort((u, v) => v.my - u.my);
    const out = [], ux = {}, uy = {};
    good.forEach((o) => { if (out.length >= 5 || ux[o.x.id] || uy[o.y.id]) return; ux[o.x.id] = uy[o.y.id] = 1; out.push(o); });
    done(out);
  };
  setTimeout(step, 0);
  return () => { dead = true; };
}
function GxIdeas293({ s, onPick }) {
  const [list, setList] = useState(() => (window.__TI293 && window.__TI293.k === s.players ? window.__TI293.v : null));
  useEffect(() => {
    if (window.__TI293 && window.__TI293.k === s.players) { setList(window.__TI293.v); return undefined; }
    let stop = null, dead = false;
    setList(null);
    const id = setTimeout(() => { try { stop = gxIdeas293(s, (v) => { window.__TI293 = { k: s.players, v }; if (!dead) setList(v); }); } catch (e) { if (!dead) setList([]); } }, 400);
    return () => { dead = true; clearTimeout(id); if (stop) stop(); };
  }, [s.players, s.me, s.blend, window.__PMODE]);
  const sg = (v) => "+" + Math.round(v);
  return (
    <div className="gx-pn gx-ti293" data-gx="293">
      <div className="hd"><span className="gx-tag">Trade ideas</span><small>swaps that help both teams</small></div>
      {!list ? <div className="em">Looking through every team...</div> : list.length ? list.map((o) => (
        <button key={o.x.id + "|" + o.y.id} type="button" className="rw" onClick={() => onPick(o.x.id, o.y.id, o.tm)}>
          <span className="sw"><small>Give</small><GxFace p={o.x} size={14} /><b>{o.x.n}</b><small>Get</small><GxFace p={o.y} size={14} /><b>{o.y.n + " \u00b7 " + (gxTag131(s, o.y) || teamName(s, o.tm))}</b></span>
          <span className="nm"><b>{"You " + sg(o.my)}</b>{"Them " + sg(o.th)}</span>
        </button>
      )) : <div className="em">No one-for-one swap helps both teams right now.</div>}
      {list && list.length ? <div className="em" style={{ fontSize: 12 }}>Points over the rest of the season, scored the same way as the result below. Tap an idea to load it.</div> : null}
    </div>
  );
}
'''

STEP_OLD = r'''    if (i < 0 || i < n - 6) { setI(Math.max(0, n - 1 - (i < 0 ? 0 : 5))); return; }
    if (i >= n - 1) return;
    const t = setTimeout(() => setI((v) => Math.min(n - 1, v + 1)), 900);
    return () => clearTimeout(t);'''
STEP_NEW = r'''    if (i !== n - 1) setI(n - 1); /* change 293: always the newest play, at once */'''

PK_OLD = r'''      if (zs) { tx = zs * (30 + Math.random() * 58); ty = -34 + Math.random() * 68; }
      else { tx = x + (Math.random() * 20 - 10); ty = -y + (Math.random() * 20 - 10); }'''
PK_NEW = r'''      tx = x + (Math.random() * 8 - 4); ty = -y + (Math.random() * 8 - 4); /* change 293: stays by the real spot */'''
DUR_OLD = r'''let leg = { fx: cur.x, fy: cur.y, tx: x, ty: -y, t0: performance.now(), dur: 650 }'''
DUR_NEW = r'''let leg = { fx: cur.x, fy: cur.y, tx: x, ty: -y, t0: performance.now(), dur: 320 }'''

POLL_OLD = r'''Date.now() - (window.__LP120 || 0) > 59000) pull(); }, 2 * 1000);'''
POLL_NEW = r'''Date.now() - (window.__LP120 || 0) > 20000) pull(); }, 2 * 1000);'''

SHOW_OLD = r'''const GX_SHOW289 = [["fa", "Free agents"], ["all", "All players"], ["inj", "Injured"]];'''
SHOW_NEW = r'''const GX_SHOW289 = [["fa", "Free agents"], ["all", "All players"], ["inj", "Injured"], ["watch", "Watchlist"]];'''
LB_OLD = r'''<GxFlt108 label={v === "all" ? "All players" : "Injured"}>'''
LB_NEW = r'''<GxFlt108 label={v === "all" ? "All players" : v === "watch" ? "Watchlist" : "Injured"}>'''
RK_OLD = r'''      <GxRankings s={P.s} st287={v} />
    </div>
  );
}
// every week left, one tap each, above the free agent list'''
RK_NEW = r'''      {v === "watch" ? (gxWatch.list().length ? <GxWatchPanel s={P.s} /> : <div className="gx-pn text-sm text-slate-500">Your watchlist is empty.</div>) : <GxRankings s={P.s} st287={v} />}
    </div>
  );
}
// every week left, one tap each, above the free agent list'''
WP_OLD = r'''<GxWatchPanel s={s} /><GxHiddenPanel s={s} />{/* gx075-p */}'''
WP_NEW = r'''{onShow289 ? null : <GxWatchPanel s={s} />}<GxHiddenPanel s={s} />{/* gx075-p */}'''

TI_OLD = r'''<div className="text-sm text-slate-500">Pick at least one player on each side to see the result.</div>}'''
TI_NEW = r'''<GxIdeas293 s={s} onPick={(g, r, tm) => { setPartner(tm); setGive([g]); setGet([r]); }} />}'''


def change(t):
    t = lit(t, "293: styles", "</style>", NEW_CSS, "change 293 (install.py)")
    t = lit(t, "293: helpers", ROOT, HELPERS + ROOT, "change 293: trade ideas")
    t = lit(t, "293: newest play at once", STEP_OLD, STEP_NEW, "change 293: always the newest play")
    t = lit(t, "293: puck stays by the spot", PK_OLD, PK_NEW, "change 293: stays by the real spot")
    t = lit(t, "293: puck gets there faster", DUR_OLD, DUR_NEW)
    t = lit(t, "293: check scores every 20 s", POLL_OLD, POLL_NEW)
    t = lit(t, "293: watchlist in Show", SHOW_OLD, SHOW_NEW, '["watch", "Watchlist"]')
    t = lit(t, "293: watchlist label", LB_OLD, LB_NEW, 'v === "watch" ? "Watchlist"')
    t = lit(t, "293: watchlist view", RK_OLD, RK_NEW, "Your watchlist is empty.")
    t = lit(t, "293: watchlist off the page", WP_OLD, WP_NEW, "{onShow289 ? null : <GxWatchPanel s={s} />}")
    t = lit(t, "293: trade ideas", TI_OLD, TI_NEW, "<GxIdeas293 s={s} onPick")
    return t

edit(APP, change)
