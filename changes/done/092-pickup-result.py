# changes/092-pickup-result.py - Pickups simulate box shows the full result like Trades (season points, league and position ranks, this week and next week, every projection); autopilot note on Today is one short line

NEW_CSS = r'''  /* change 092 (install.py) */
  .gx-pm92 { display: grid; grid-template-columns: minmax(0,1.3fr) repeat(3, minmax(0,1fr)) 54px; gap: 8px; align-items: center; padding: 8px 6px; border-top: 1px solid var(--line); font-size: 13px; font-variant-numeric: tabular-nums; }
  .gx-pm92 > span + span { text-align: right; }
  .gx-pm92.h { font-size: 11px; color: var(--mute); border-top: 0; padding-top: 2px; }
  .gx-pm92.on { outline: 1px solid var(--ink); border-radius: 6px; }
  .gx-pm92 .w { font-weight: 600; color: var(--good); }
  .gx-pm92 .l { font-weight: 600; color: var(--bad); }
  .gx-ap92 { display: flex; align-items: center; gap: 8px; padding: 7px 12px; font-size: 13px; min-width: 0; }
  .gx-ap92 .dot { width: 7px; height: 7px; border-radius: 99px; flex-shrink: 0; }
  @media (max-width: 640px) { .gx-pm92 { grid-template-columns: minmax(0,1.2fr) repeat(2, minmax(0,1fr)) 46px; gap: 6px; padding: 9px 4px; } }
</style>'''

HELPERS = r'''// ---------- change 092: full result for a pickup, like Trades (install.py) ----------
function GxPickRes92({ s, myR, ok }) {
  const key = ok.map((x) => x.a.id + ">" + x.d.id).join(",");
  const calc = () => {
    const nR = s.weeks.length - s.wk;
    const timed = timedMove(myR, s.me, ok.map((x) => ({ add: x.a, drop: x.d })));
    const my = horizonTotal(timed, s, nR) - horizonTotal(myR, s, nR);
    const w = deriveWeek(s.weeks[s.wk] || s.weeks[0], s.autoDone), on = oppOf(w, s.me) && (w.done || 0) < (w.dates || []).length;
    const tb = on ? winChance(s) : null, ta = on ? winChance(s, timed) : null;
    const sN = nextWkS(s), ho = sN && oppOf(sN.weeks[sN.wk] || {}, s.me);
    const wb = ho ? winChance(sN) : null, wa = ho ? winChance(sN, timed) : null;
    return { my, tb, ta, wb, wa };
  };
  const res = useMemo(() => {
    const base = calc();
    const A = new Set(ok.map((x) => x.a.id)), D = new Set(ok.map((x) => x.d.id));
    const players = s.players.map((p) => (A.has(p.id) ? { ...p, ft: s.me } : D.has(p.id) ? { ...p, ft: "fa", ir: false } : p));
    const pos = (t) => ({ o: t.rows.findIndex((x) => x.t.id === s.me) + 1, ...(t.grpRank[s.me] || {}) });
    const keep = __LT, t2 = leagueTable({ ...s, players });
    __LT = keep;
    return { ...base, rb: pos(leagueTable(s)), ra: pos(t2), mode: window.__PMODE };
  }, [key, s.players, s.wk, window.__PMODE]);
  const [cmp, setCmp] = useState(null);
  useEffect(() => {
    setCmp(null);
    const id = setTimeout(() => setCmp(GX_PM82.filter(([k]) => gxCanMode82(k)).map(([k, l]) => ({ k, l, ...(k === res.mode ? res : gxWithMode82(k, calc)) }))), 60);
    return () => clearTimeout(id);
  }, [res]);
  const GN = { F: "Forwards", D: "Defence", G: "Goalies" };
  const sg = (v) => (v >= 0 ? "+" : "") + Math.round(v);
  const arrow = (b, a, fmt, up) => <><span>{fmt(b)}</span><span className="text-slate-500" style={{ fontSize: 14, margin: "0 6px" }}>{"→"}</span><span style={{ color: up > 0 ? "var(--good)" : up < 0 ? "var(--bad)" : "var(--ink)" }}>{fmt(a)}</span></>;
  const wkUp = res.ta != null && res.tb != null ? Math.round(res.ta * 100) - Math.round(res.tb * 100) : 0;
  const vd = res.my > 0.5 ? ["Good pickup", "var(--good)", "Your lineup gains points for the rest of the season."]
    : wkUp > 0 ? ["Stream only", "var(--warn)", "Helps this week, but costs you points over the season. Fine if you swap him back later."]
    : ["Bad for you", "var(--bad)", "Your lineup gets worse."];
  return (
    <div style={{ marginTop: 14 }}>
      <div style={{ display: "flex", alignItems: "baseline", gap: 10, flexWrap: "wrap" }}>
        <span className="font-semibold" style={{ color: vd[1] }}>{vd[0]}</span>
        <span className="text-sm text-slate-500">{vd[2]}</span>
      </div>
      <div className="gx-stg">
        <div className="gx-stc"><div className="text-xs text-slate-500">Your lineup</div><div className="gx-stv" style={{ color: res.my >= 0 ? "var(--good)" : "var(--bad)" }}>{sg(res.my)}</div><div className="text-xs text-slate-500">points, rest of season</div></div>
        <div className="gx-stc"><div className="text-xs text-slate-500">Your league rank</div><div className="gx-stv">{arrow(res.rb.o, res.ra.o, ordN, res.rb.o - res.ra.o)}</div><div className="text-xs text-slate-500">by team strength</div></div>
        <div className="gx-stc"><div className="text-xs text-slate-500">Position ranks</div>
          {["F", "D", "G"].map((k) => { const b = res.rb[k], a = res.ra[k], f = (v) => (v ? ordN(v) : "–"); return (
            <div key={k} style={{ display: "flex", alignItems: "baseline", gap: 6, fontSize: 15, fontWeight: 600, fontVariantNumeric: "tabular-nums", marginTop: 2 }}>
              <span className="text-xs text-slate-500" style={{ width: 74, flexShrink: 0, fontWeight: 400 }}>{GN[k]}</span>
              {b === a ? <><span>{f(b)}</span><span className="text-xs text-slate-500" style={{ fontWeight: 400 }}>same</span></> : <span>{arrow(b, a, f, (b || 0) - (a || 0))}</span>}
            </div>
          ); })}
        </div>
        {res.tb != null && res.ta != null ? <div className="gx-stc"><div className="text-xs text-slate-500">This week</div><div className="gx-stv">{arrow(res.tb, res.ta, wpTxt, wkUp)}</div><div className="text-xs text-slate-500">chance to win</div></div> : null}
        {res.wb != null && res.wa != null ? <div className="gx-stc"><div className="text-xs text-slate-500">Next week</div><div className="gx-stv">{arrow(res.wb, res.wa, wpTxt, Math.round(res.wa * 100) - Math.round(res.wb * 100))}</div><div className="text-xs text-slate-500">chance to win</div></div> : null}
      </div>
      <div style={{ marginTop: 12 }}>
        <div className="gx-tag" style={{ marginBottom: 4 }}>Every projection</div>
        <div className="gx-pm92 h"><span>Projection</span><span>Season</span><span className="m-hide">This week</span><span>Next week</span><span>Result</span></div>
        {!cmp ? <div className="text-xs text-slate-500" style={{ padding: "8px 6px" }}>Working out every projection...</div> : cmp.map((x) => (
          <div key={x.k} className={"gx-pm92" + (x.k === res.mode ? " on" : "")}>
            <span>{x.l}{x.k === res.mode ? <span className="text-xs text-slate-500"> (app)</span> : null}</span>
            <span style={{ color: x.my >= 0 ? "var(--good)" : "var(--bad)" }}>{sg(x.my)}</span>
            <span className="m-hide">{gxPct82(x.tb, x.ta)}</span>
            <span>{gxPct82(x.wb, x.wa)}</span>
            <span className={x.my > 0 ? "w" : "l"}>{x.my > 0 ? "Win" : "Lose"}</span>
          </div>
        ))}
        <div className="text-xs text-slate-500" style={{ marginTop: 6 }}>Season is points for the rest of the season. The weeks show the change in your chance to win. Win means your lineup gains points.</div>
      </div>
    </div>
  );
}
// ---------- change 092: autopilot note on Today is one short line (install.py) ----------
function GxAutoToday2({ go }) {
  const v = gxUseAp();
  if (!v || !v.b) return null;
  const today = todayISO();
  const e = [...(v.b.entries || [])].reverse().find((x) => String(x.at || "").slice(0, 10) === today);
  if (!e) return null;
  const fail = String(e.result || "").indexOf("failed") === 0, test = e.mode !== "on";
  const col = fail ? "var(--bad)" : test ? "var(--warn)" : "var(--good)";
  const day = e.day && e.day !== today ? gxApDayName(e.day) + "'s" : "today's";
  const txt = fail ? "Autopilot could not set your lineup. Set it on ESPN." : (test ? "Autopilot test: would change " : "Autopilot set ") + day + " lineup" + (e.gain ? " (+" + e.gain + ")" : "");
  return (
    <div className="gx-pn gx-ap92" role="button" onClick={() => go("setup", "autopilot")} title={e.text}>
      <span className="dot" style={{ background: col }}></span>
      <span className="truncate" style={{ flex: 1, minWidth: 0 }}>{txt}</span>
      <span className="text-xs text-slate-500" style={{ flexShrink: 0 }}>{gxApTime(e.at)}</span>
    </div>
  );
}
'''

def change(t):
    t = lit(t, "092: styles", "</style>", NEW_CSS, "change 092 (install.py)")
    t = lit(t, "092: helpers", ROOT, HELPERS + ROOT, "change 092: full result for a pickup")
    t = lit(t, "092: result in the simulate box",
            '{R.short.length ? <div className="text-sm text-red-600 mt-2">Below your minimum at {R.short.join(", ")}. Pick a different drop.</div> : null}',
            '<GxPickRes92 s={s} myR={myR} ok={R.ok} />{/* gx092-res */}{R.short.length ? <div className="text-sm text-red-600 mt-2">Below your minimum at {R.short.join(", ")}. Pick a different drop.</div> : null}',
            "{/* gx092-res */}")
    t = lit(t, "092: short autopilot line",
            "<GxAutoToday go={go} />{/* gx089-today */}",
            "<GxAutoToday2 go={go} />{/* gx089-today */}{/* gx092-today */}",
            "{/* gx092-today */}")
    return t

edit(APP, change)
