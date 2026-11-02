# changes/197-league-draft.py - League page gets a Draft section: the draft order (team pictures, pick 1 to 10) and every pick going down in order with the player's stats beside him (games, fantasy points, average, expected, rank this season, value = how far he beat or missed his draft spot, who has him now); pick a team to see only its picks. espn_sync.py now saves ESPN's draft (draft order and picks) into the league data

SYNC_OLD = '''# 3b) actual points per player per day + NHL game states (news_logos.py round 16)'''
SYNC_NEW = '''# change 197: draft order and every pick (players no longer in the player list get a short line of their own)
try:
    _dr = get(LEAGUE, params=[("view", "mDraftDetail"), ("view", "mSettings")])
    _dd = _dr.get("draftDetail") or {}
    _ds = (_dr.get("settings") or {}).get("draftSettings") or {}
    _picks = [{"o": x.get("overallPickNumber"), "r": x.get("roundId"), "rp": x.get("roundPickNumber"), "t": x.get("teamId"),
               "p": x.get("playerId"), "k": 1 if x.get("keeper") else 0} for x in (_dd.get("picks") or []) if x.get("playerId")]
    _known = {p_["id"] for p_ in players}
    _miss = [x["p"] for x in _picks if x["p"] not in _known]
    _extra = []
    if _miss:
        try:
            _pl = get(LEAGUE, params={"view": "kona_player_info"}, fantasy_filter={"players": {"filterIds": {"value": _miss}, "limit": len(_miss)}})
            for _e in (_pl.get("players", []) if isinstance(_pl, dict) else []):
                _p = _e.get("player") or {}
                _tot = _avg = _pav = None
                for _st in _p.get("stats") or []:
                    if _st.get("seasonId") != SEASON or _st.get("statSplitTypeId") != 0:
                        continue
                    if _st.get("statSourceId") == 0:
                        _tot, _avg = _st.get("appliedTotal"), _st.get("appliedAverage")
                    elif _st.get("statSourceId") == 1:
                        _pav = _st.get("appliedAverage")
                _extra.append({"id": _p.get("id"), "n": _p.get("fullName"), "t": pro_abbr.get(_p.get("proTeamId")) or "",
                               "p": {4: "D", 5: "G"}.get(_p.get("defaultPositionId"), "F"), "ft": _e.get("onTeamId", 0) or 0,
                               "gp": round(_tot / _avg) if _tot and _avg else 0, "tot": round(_tot or 0, 1), "pavg": round(_pav or 0, 2)})
        except Exception as _ex:
            print("(draft) missing players not read:", _ex)
    data["draft"] = {"order": _ds.get("pickOrder") or [], "type": _ds.get("type") or "", "date": _ds.get("date"),
                     "done": bool(_dd.get("drafted")), "picks": _picks, "extra": _extra}
    print(f"(draft) {len(_picks)} picks, order {data['draft']['order']}, {len(_extra)} players read separately")
except Exception as _ex:
    print("(draft) skipped:", _ex)
# 3b) actual points per player per day + NHL game states (news_logos.py round 16)'''

HELPERS = r'''// ---------- change 197: League > Draft (install.py) ----------
function GxDraft197({ s }) {
  const E = window.ESPN_DATA || {}, D = E.draft || null, K = s.blend;
  const [tm, setTm] = useState("all");
  const [lim, setLim] = useState(40);
  const rows = useMemo(() => {
    if (!D || !(D.picks || []).length) return [];
    const ex = {};
    (D.extra || []).forEach((p) => { ex[String(p.id)] = p; });
    const L = [...D.picks].sort((a, b) => a.o - b.o).map((x) => {
      const p = s.players.find((q) => q.id === "e" + x.p);
      const e = ex[String(x.p)];
      const pl = p || (e ? { id: "e" + e.id, n: e.n, t: e.t, p: e.p, ft: e.ft ? "t" + e.ft : "fa", gp: e.gp, tot: e.tot, avg: e.pavg, prob: 1, x197: true } : null);
      return { ...x, pl, by: "t" + x.t };
    });
    const ranked = L.filter((r) => r.pl).sort((a, b) => (b.pl.tot || 0) - (a.pl.tot || 0));
    ranked.forEach((r, i) => { r.rk = i + 1; r.val = r.o - (i + 1); });
    return L;
  }, [D, s.players]);
  if (!D) return null;
  const ord = (D.order || []).map((t) => "t" + t);
  const shown = tm === "all" ? rows : rows.filter((r) => r.by === tm);
  const ab = (id) => gxTag131(s, { ft: id }) || teamName(s, id);
  return (
    <div className="gx-pn gx-dr197"><b></b><b></b><b></b><b></b>
      <div className="hd197"><span className="gx-st">Draft</span><span className="sb">{rows.length ? rows.length + " picks" + (D.done ? "" : " so far") : "No draft yet"}</span></div>
      {ord.length ? (
        <>
          <div className="sec197">Draft order</div>
          <div className="or197">
            {ord.map((t, i) => (
              <button key={t + i} type="button" className={"oc" + (tm === t ? " on" : "")} onClick={() => { setTm(tm === t ? "all" : t); setLim(40); }} title={teamName(s, t)}>
                <span className="n">{i + 1}</span><GxFtPic114 id={t} size={30} /><span className="a">{ab(t)}</span>
              </button>
            ))}
          </div>
        </>
      ) : null}
      {rows.length ? (
        <>
          <div className="sec197">{tm === "all" ? "Every pick" : ab(tm) + "'s picks"}{tm !== "all" ? <button type="button" className="cl" onClick={() => setTm("all")}>Show all teams</button> : null}</div>
          <div className="tb197">
            <div className="tr197 hd"><span className="pk">Pick</span><span className="pc">Player</span><span>By</span><span>Now</span><span className="n">GP</span><span className="n">FPTS</span><span className="n">Avg</span><span className="n">Exp</span><span className="n">Rank</span><span className="n">Value</span></div>
            {shown.slice(0, lim).map((r) => {
              const p = r.pl, now = p ? (p.ft === "fa" ? "FA" : p.ft === r.by ? "Same" : ab(p.ft)) : "";
              return (
                <div key={r.o} className={"tr197" + (p && !p.x197 ? " go" : "")} role={p && !p.x197 ? "button" : undefined} onClick={() => { if (p && !p.x197 && window.__NAV) window.__NAV.player(p); }}>
                  <span className="pk"><b>{r.o}</b><small>{r.r + "." + r.rp}</small></span>
                  <span className="pc">{p ? <GxFace p={p} size={24} /> : <span className="gx-face"></span>}<span className="nm"><span className="t">{p ? p.n : "Player " + r.p}</span><small>{p ? p.p + " \u00b7 " + p.t : ""}{r.k ? " \u00b7 keeper" : ""}</small></span></span>
                  <span className="tm"><GxFtPic114 id={r.by} size={18} /><span>{ab(r.by)}</span></span>
                  <span className="nw" style={{ color: now === "FA" ? "var(--bad)" : now === "Same" ? "var(--mute)" : "var(--ink)" }}>{now}</span>
                  <span className="n">{p ? p.gp || 0 : "-"}</span>
                  <span className="n b">{p ? f1(p.tot || 0) : "-"}</span>
                  <span className="n">{p && p.gp ? f1(p.tot / p.gp) : "-"}</span>
                  <span className="n">{p && !p.x197 ? f1(gxPgAvg(p, K)) : p ? f1(p.avg || 0) : "-"}</span>
                  <span className="n">{r.rk ? ordN(r.rk) : "-"}</span>
                  <span className="n b" style={{ color: r.val == null ? "var(--mute)" : r.val > 0 ? "var(--good)" : r.val < 0 ? "var(--bad)" : "var(--ink)" }}>{r.val == null ? "-" : (r.val > 0 ? "+" : "") + r.val}</span>
                </div>
              );
            })}
          </div>
          {shown.length > lim ? <GxMore122 onMore={() => setLim((v) => v + 40)} /> : null}
          <div className="nt197">Rank = place among drafted players by fantasy points this season. Value = draft spot minus that rank (green beat his spot, red missed it). Now = who has him today.</div>
        </>
      ) : <div className="text-sm text-slate-500" style={{ marginTop: 8 }}>ESPN hasn't listed any picks yet.</div>}
    </div>
  );
}
'''

OLD_LG = '''<LeaguePage {...P} /><GxPlayoff s={s} /></div>;'''
NEW_LG = '''<LeaguePage {...P} /><GxPlayoff s={s} /><GxDraft197 s={s} /></div>;'''

NEW_CSS = r'''  /* change 197 (install.py) */
  .gx-dr197 .hd197 { display: flex; align-items: baseline; gap: 10px; }
  .gx-dr197 .hd197 .sb { font-size: 12px; color: var(--mute); }
  .gx-dr197 .sec197 { display: flex; align-items: center; gap: 10px; font-size: 12px; letter-spacing: .06em; text-transform: uppercase; color: var(--mute); margin: 14px 0 8px; }
  .gx-dr197 .sec197 .cl { margin-left: auto; text-transform: none; letter-spacing: 0; font-size: 12px; color: var(--ink); text-decoration: underline; }
  .gx-dr197 .or197 { display: flex; gap: 8px; overflow-x: auto; padding: 2px 2px 6px; overscroll-behavior-x: contain; }
  .gx-dr197 .or197 .oc { flex: 0 0 74px; height: 86px; display: grid; grid-template-rows: 16px 34px 18px; justify-items: center; align-items: center; border: 1px solid var(--line2); border-radius: 10px; padding: 6px 4px; transition: background .15s ease, border-color .15s ease; }
  .gx-dr197 .or197 .oc .n { font-size: 12px; font-weight: 700; color: var(--mute); }
  .gx-dr197 .or197 .oc .a { font-size: 12px; max-width: 64px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .gx-dr197 .or197 .oc.on { border-color: var(--accent); box-shadow: inset 0 0 0 1px var(--accent); background: var(--accentSoft); }
  .gx-dr197 .tb197 { overflow-x: auto; overscroll-behavior-x: contain; }
  .gx-dr197 .tr197 { display: grid; grid-template-columns: 56px 280px 96px 72px 52px 70px 58px 58px 64px 64px; align-items: center; height: 50px; border-top: 1px solid var(--line); width: max-content; min-width: 100%; }
  .gx-dr197 .tr197.hd { height: 30px; border-top: 0; font-size: 12px; color: var(--mute); }
  .gx-dr197 .tr197.go { cursor: pointer; }
  .gx-dr197 .tr197.go:hover { background: var(--hover, rgba(255,255,255,.03)); }
  .gx-dr197 .tr197 > span { min-width: 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .gx-dr197 .tr197 .pk { display: flex; flex-direction: column; line-height: 1.15; padding-left: 4px; position: sticky; left: 0; background: var(--card); height: 100%; justify-content: center; z-index: 1; }
  .gx-dr197 .tr197 .pk b { font-size: 14px; font-variant-numeric: tabular-nums; }
  .gx-dr197 .tr197 .pk small { font-size: 11px; color: var(--mute); }
  .gx-dr197 .tr197 .pc { display: flex; align-items: center; gap: 8px; position: sticky; left: 56px; background: var(--card); height: 100%; z-index: 1; padding-right: 8px; }
  .gx-dr197 .tr197 .pc .gx-face { flex: none; }
  .gx-dr197 .tr197 .nm { display: flex; flex-direction: column; min-width: 0; line-height: 1.2; font-size: 14px; }
  .gx-dr197 .tr197 .nm .t, .gx-dr197 .tr197 .nm small { display: block; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .gx-dr197 .tr197 .nm small { font-size: 11.5px; color: var(--mute); }
  .gx-dr197 .tr197 .tm { display: flex; align-items: center; gap: 5px; font-size: 13px; }
  .gx-dr197 .tr197 .tm .gx-fp114 { flex: none; }
  .gx-dr197 .tr197 .nw { font-size: 13px; }
  .gx-dr197 .tr197 .n { text-align: right; padding-right: 8px; font-size: 13px; font-variant-numeric: tabular-nums; color: var(--mute); }
  .gx-dr197 .tr197 .n.b { color: var(--ink); font-weight: 600; }
  .gx-dr197 .tr197.hd .n { font-weight: 400; color: var(--mute); }
  .gx-dr197 .nt197 { font-size: 12px; color: var(--mute); margin-top: 8px; }
  @media (max-width: 640px) {
    .gx-dr197 .tr197 { grid-template-columns: 44px 150px 70px 56px 38px 56px 44px 44px 48px 52px; }
    .gx-dr197 .tr197 .pc { left: 44px; gap: 6px; }
    .gx-dr197 .or197 .oc { flex-basis: 66px; }
  }
</style>'''


def change(t):
    t = lit(t, "197: styles", "</style>", NEW_CSS, "change 197 (install.py)")
    t = lit(t, "197: helpers", ROOT, HELPERS + ROOT, "change 197: League > Draft")
    t = lit(t, "197: Draft on the League page", OLD_LG, NEW_LG, "<GxDraft197 s={s} />")
    return t


def change_sync(t):
    t = lit(t, "197: save the draft", SYNC_OLD, SYNC_NEW, "change 197: draft order and every pick")
    return t


edit(APP, change)
edit("espn_sync.py", change_sync)
