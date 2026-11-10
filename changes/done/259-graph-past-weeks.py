# changes/259-graph-past-weeks.py - Graph side: past weeks (week arrows) and a Season view; the sync now saves every finished day's lineup points and pregame projection

SYNC_NEW = r'''    data["daily"] = daily
    # ---------- change 259: day by day history for every finished day (install.py) ----------
    # dhist[date][team] = [points scored by lineup players (not bench 7 / IR 8), their pregame projection
    # from ai/joined (None if not saved), lineup players with a projection]; kept in the locked data only
    try:
        def _dh_proj259(dd_):
            try:
                with open(os.path.join(HERE, "ai", "joined", dd_ + ".json"), encoding="utf-8") as f_:
                    recs_ = json.load(f_).get("recs") or []
            except Exception:
                return None
            pj_ = {}
            for r_ in recs_:
                c_ = r_.get("combo")
                if c_ is None:
                    c_ = r_.get("gm") if r_.get("gm") is not None else r_.get("espn")
                if c_ is None:
                    continue
                if r_.get("pos") == "G":
                    sp_g = r_.get("start_p")
                    if sp_g is None:
                        sp_g = r_.get("ai_start_p")
                    c_ = c_ * (sp_g if sp_g is not None else 1)
                pj_[str(r_.get("pid"))] = c_
            return pj_

        def _dh_day259(day_, dd_):
            pj_ = _dh_proj259(dd_)
            out_ = {}
            for t_, tm_ in day_.items():
                a_, p_, g_ = 0.0, 0.0, 0
                for pid_, v_ in tm_.items():
                    if v_[1] in (7, 8):
                        continue
                    if v_[0]:
                        a_ += v_[0]
                    if pj_ and pid_ in pj_:
                        p_ += pj_[pid_]
                        g_ += 1
                out_[t_] = [round(a_, 1), round(p_, 1) if pj_ is not None else None, g_]
            return out_

        def _dh_fetch259(sp_):
            rs_ = get(LEAGUE, params=[("view", "mMatchupScore"), ("view", "mScoreboard"), ("scoringPeriodId", sp_)])
            day_ = {}
            for m_ in rs_.get("schedule", []):
                for side_ in ("home", "away"):
                    ts_ = m_.get(side_) or {}
                    ents_ = (ts_.get("rosterForCurrentScoringPeriod") or {}).get("entries") or []
                    if not ents_:
                        continue
                    tm_ = {}
                    for en_ in ents_:
                        pe_ = en_.get("playerPoolEntry") or {}
                        pts_ = None
                        for st_ in (pe_.get("player") or {}).get("stats") or []:
                            if st_.get("scoringPeriodId") == sp_ and st_.get("statSourceId") == 0:
                                pts_ = st_.get("appliedTotal")
                                break
                        tm_[str(en_.get("playerId"))] = [None if pts_ is None else round(pts_, 2), en_.get("lineupSlotId")]
                    day_[str(ts_.get("teamId"))] = tm_
            return day_

        old_dh_ = {}
        for fn_ in (OUT, os.path.join(HERE, "espn-data.prev.tmp")):  # the last file, or the copy the workflow restored
            try:
                with open(fn_, encoding="utf-8") as f_:
                    raw_ = f_.read()
                old_dh_ = (json.loads(raw_[raw_.index("{"):raw_.rindex("}") + 1]).get("dhist") or {})
            except Exception:
                old_dh_ = {}
            if old_dh_:
                break
        dh_ = {d_: v_ for d_, v_ in old_dh_.items() if isinstance(v_, dict)}
        tday_ = today_et.isoformat()
        for dd_, day_ in daily.items():
            if dd_ < tday_:
                dh_[dd_] = _dh_day259(day_, dd_)
        season_ = sorted({d_ for p_ in periods for d_ in p_["dates"]})
        missing_ = [d_ for d_ in season_ if d_ < tday_ and d_ not in dh_]
        got_ = 0
        for dd_ in missing_[:12]:
            sp_ = (date.fromisoformat(dd_) - day1).days + 1
            try:
                day_ = _dh_fetch259(sp_)
                if day_:
                    dh_[dd_] = _dh_day259(day_, dd_)
                    got_ += 1
            except Exception as ex:
                print(f"(history) {dd_} failed: {ex}")
        data["dhist"] = dh_
        print(f"(history) {len(dh_)} finished days saved, {got_} read from ESPN now, {max(0, len(missing_) - got_)} still to read")
    except Exception as ex:
        print(f"(history) skipped: {type(ex).__name__}: {ex}")
'''

def sync(t):
    t = lit(t, "259: day history in the sync", '    data["daily"] = daily\n', SYNC_NEW, "# ---------- change 259: day by day history")
    return t

edit("espn_sync.py", sync)

NEW_CSS = r'''  /* change 259 (install.py) */
  .gf252 .gw259 { display: flex; align-items: center; gap: 6px; height: 32px; margin: -2px 0 6px; }
  .gf252 .gw259 .ar { width: 30px; height: 30px; flex: none; border-radius: 999px; border: 1px solid var(--line); background: var(--card); color: var(--ink); font-size: 16px; line-height: 1; display: inline-flex; align-items: center; justify-content: center; }
  .gf252 .gw259 .ar:disabled { opacity: .35; }
  .gf252 .gw259 .wl { min-width: 0; font-size: 13px; font-weight: 600; color: var(--ink); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .gf252 .gw259 .wl small { margin-left: 6px; font-size: 11.5px; font-weight: 400; color: var(--mute); }
  .gf252 .gw259 .sp { flex: 1; }
  .gf252 .gw259 .sb { flex: none; height: 28px; padding: 0 11px; border-radius: 8px; border: 1px solid var(--line); background: var(--card); color: var(--ink); font-size: 12px; font-weight: 600; }
  .gf252 .gw259 .sb.on { background: var(--card3, var(--hover)); }
  .gf252 .nt259 { font-size: 12px; color: var(--mute); margin-top: 6px; }
  .gx-pn.gx-bx226 .fc.fin259 { position: relative; inset: auto; margin-top: 12px; height: 340px; display: flex; flex-direction: column; overflow: hidden; backface-visibility: visible; -webkit-backface-visibility: visible; }
  @media (max-width: 640px) { .gx-pn.gx-bx226 .fc.fin259 { height: 330px; } }
</style>'''

HELPERS = r'''// ---------- change 259: Graph side for past weeks and the season (install.py) ----------
// finished days come from E.dhist[date][team] = [lineup points, pregame projection, lineup players with a projection]
function gxWkDh259(s, j, me) {
  const H = (window.ESPN_DATA || {}).dhist || {}, wk = s.weeks[j] || {}, dates = wk.dates || [];
  const opp = oppOf(wk, me);
  const row = (t, d) => { const x = (H[d] || {})[String(t).replace(/\D/g, "")]; return x || null; };
  const A = dates.map((d) => { const x = row(me, d); return x ? x[0] : null; });
  const B = dates.map((d) => { const x = opp ? row(opp, d) : null; return x ? x[0] : null; });
  const PA = dates.map((d) => { const x = row(me, d); return x && x[1] != null ? x[1] : null; });
  const PB = dates.map((d) => { const x = opp ? row(opp, d) : null; return x && x[1] != null ? x[1] : null; });
  const have = dates.filter((d) => H[d]).length;
  return { dates, opp, A, B, PA, PB, have, n: dates.length };
}
function GxGraphWrap259({ s, i, go, me, cur, nmA, nmB, plain, today }) {
  const [sea, setSea] = useState(() => uiGet().gr259 === "s");
  const setS = (v) => { setSea(v); uiSet("gr259", v ? "s" : ""); };
  const gen = (window.ESPN_DATA || {}).generated;
  const lab = (j) => String((s.weeks[j] || {}).label || "Week " + (j + 1)).split(" \u00b7 ");
  const season = useMemo(() => {
    const out = [];
    for (let j = 0; j < s.weeks.length; j++) {
      const ds = (s.weeks[j] || {}).dates || [];
      if (!ds.length || ds[ds.length - 1] >= today) continue;
      const g = gxWkDh259(s, j, me);
      if (!g.opp || !g.have) continue;
      const sum = (a) => a.reduce((t, v) => t + (v || 0), 0);
      const pOk = (a) => a.every((v, d) => v != null || !g.A[d]);
      out.push({ j, a: sum(g.A), b: sum(g.B), pa: pOk(g.PA) ? sum(g.PA) : null, pb: pOk(g.PB) ? sum(g.PB) : null, full: g.have === g.n, opp: g.opp });
    }
    return out;
  }, [s.weeks, me, gen, today]);
  const W = (j) => lab(j)[0].replace(/^Week\s*/i, "W");
  const head = (
    <div className="gw259" onPointerDown={(e) => e.stopPropagation()}>
      {sea ? <span className="wl">Season</span> : (
        <>
          <button type="button" className="ar" aria-label="Earlier week" disabled={i <= 0} onClick={() => go(i - 1)}>{"\u2039"}</button>
          <span className="wl">{lab(i)[0]}<small>{lab(i)[1] || ""}</small></span>
          <button type="button" className="ar" aria-label="Next week" disabled={i >= s.weeks.length - 1} onClick={() => go(i + 1)}>{"\u203a"}</button>
        </>
      )}
      <span className="sp"></span>
      <button type="button" className={"sb" + (sea ? " on" : "")} onClick={() => setS(!sea)}>{sea ? "Back to week" : "Season"}</button>
    </div>
  );
  if (sea) {
    if (!season.length) return <>{head}<div className="nt259">No finished weeks saved yet. The sync reads past days from ESPN a few at a time, so this fills in over the next hour.</div></>;
    const L = season.map((x) => W(x.j));
    const res = (k) => { const x = season[k]; if (!x) return ""; return x.a > x.b ? "Won" : x.a < x.b ? "Lost" : "Tied"; };
    return (
      <>{head}
        <GxGraph252 key="sea" dates={L} today={null} DN={(d) => L[d]} nmA={nmA} nmB={nmB} plain={plain} onDay={(d) => { setS(false); go(season[d].j); }}
          lab={["Season total", "By week"]} sub={["season so far", "that week"]} res={res}
          A={season.map((x) => x.a)} B={season.map((x) => x.b)} PA={season.map((x) => x.pa)} PB={season.map((x) => x.pb)}
          NA={season.map(() => 0)} NB={season.map(() => 0)} />
        {season.some((x) => !x.full) ? <div className="nt259">Some past days are still loading from ESPN.</div> : null}
      </>
    );
  }
  if (cur) return <>{head}<GxGraph252 key={"c" + i} {...cur} /></>;
  const g = gxWkDh259(s, i, me);
  const ds = g.dates;
  if (!ds.length || ds[0] > today) return <>{head}<div className="nt259">This week hasn't started yet.</div></>;
  if (!g.opp) return <>{head}<div className="nt259">No matchup this week.</div></>;
  if (!g.have) return <>{head}<div className="nt259">This week's days are still loading from ESPN. The sync reads a few past days at a time, so it fills in over the next hour.</div></>;
  const DN = (d) => dayLabel(ds[d]).split(",")[0].slice(0, 3);
  return (
    <>{head}
      <GxGraph252 key={"p" + i} dates={ds} today={today} DN={DN} nmA={nmA} nmB={g.opp ? teamName(s, g.opp) : nmB} plain={plain} onDay={null}
        A={g.A} B={g.B} PA={g.PA.map((v, d) => (v == null && g.A[d] != null ? null : v))} PB={g.PB} NA={ds.map(() => 0)} NB={ds.map(() => 0)} />
      {g.have < g.n ? <div className="nt259">Some days of this week are still loading from ESPN.</div> : null}
    </>
  );
}
'''

FIN_OLD = """        {fin ? <div className="text-xs text-slate-500" style={{ marginTop: 6 }}>Day by day scores are only kept for the current week.</div> : null}
      </div>
    );
  }
  const X = R[0], Y = R[1];"""
FIN_NEW = """        {fin && opp ? <div className="fc gf252 fin259"><GxGraphWrap259 s={s} i={i} go={(j) => { setPick(Math.max(0, Math.min(s.weeks.length - 1, j))); setSel(null); }} me={me} cur={null} nmA={nmA} nmB={nmB} plain={me !== s.me} today={today} /></div> : null}{/* change 259 */}
      </div>
    );
  }
  const X = R[0], Y = R[1];"""

def in230(t, label, old, new, done):
    if done in t:
        print(f"(install) {label}: already done")
        return t
    a = t.index("function GxBox230(")
    j = t.find(old, a)
    if j < 0:
        fail(f"{label}: text not found inside GxBox230")
    return t[:j] + new + t[j + len(old):]

def change(t):
    t = lit(t, "259: styles", "</style>", NEW_CSS, "change 259 (install.py)")
    t = lit(t, "259: helpers", ROOT, HELPERS + ROOT, "change 259: Graph side for past weeks")
    t = lit(t, "259: graph props", "function GxGraph252({ dates, today, DN, A, B, PA, PB, NA, NB, nmA, nmB, plain, onDay }) {",
            "function GxGraph252({ dates, today, DN, A, B, PA, PB, NA, NB, nmA, nmB, plain, onDay, lab, sub, tag, res }) { /* change 259 */",
            "plain, onDay, lab, sub, tag, res }) { /* change 259 */")
    t = lit(t, "259: graph title", '<span className="gx-tag">Projection vs actual</span>', '<span className="gx-tag">{tag || "Projection vs actual"}</span>', '{tag || "Projection vs actual"}')
    t = lit(t, "259: run label", ">Running total</button>", ">{(lab || [])[0] || \"Running total\"}</button>", "(lab || [])[0] || \"Running total\"")
    t = lit(t, "259: day label", ">By day</button>", ">{(lab || [])[1] || \"By day\"}</button>", "(lab || [])[1] || \"By day\"")
    t = lit(t, "259: readout words", '{run ? "so far" : "that day"}', '{res ? res(sel) : run ? (sub || [])[0] || "so far" : (sub || [])[1] || "that day"}', '{res ? res(sel) : run ?')
    t = lit(t, "259: current week graph",
            '<div className="fc gf252"><GxGraph252 dates={dates} today={today} DN={DN} nmA={nmA} nmB={nmB} plain={!mineMu} onDay={showDay} A={dates.map((_, d) => (gxOn252(X, Y, d, st) ? (X.days[d] || {}).act || 0 : null))} B={dates.map((_, d) => (gxOn252(X, Y, d, st) ? (Y.days[d] || {}).act || 0 : null))} PA={dates.map((_, d) => exp(X, d))} PB={dates.map((_, d) => exp(Y, d))} NA={dates.map((_, d) => (st(d) === "f" ? 0 : (X.days[d] || {}).total || 0))} NB={dates.map((_, d) => (st(d) === "f" ? 0 : (Y.days[d] || {}).total || 0))} /></div>{fPlayers}',
            '<div className="fc gf252"><GxGraphWrap259 s={s} i={i} go={(j) => { setPick(Math.max(0, Math.min(s.weeks.length - 1, j))); setSel(null); }} me={me} nmA={nmA} nmB={nmB} plain={!mineMu} today={today} cur={{ dates, today, DN, nmA, nmB, plain: !mineMu, onDay: showDay, A: dates.map((_, d) => (gxOn252(X, Y, d, st) ? (X.days[d] || {}).act || 0 : null)), B: dates.map((_, d) => (gxOn252(X, Y, d, st) ? (Y.days[d] || {}).act || 0 : null)), PA: dates.map((_, d) => exp(X, d)), PB: dates.map((_, d) => exp(Y, d)), NA: dates.map((_, d) => (st(d) === "f" ? 0 : (X.days[d] || {}).total || 0)), NB: dates.map((_, d) => (st(d) === "f" ? 0 : (Y.days[d] || {}).total || 0)) }} /></div>{fPlayers}',
            "<GxGraphWrap259 s={s} i={i} go=")
    t = in230(t, "259: finished week graph", FIN_OLD, FIN_NEW, "{/* change 259 */}")
    return t

edit(APP, change)
