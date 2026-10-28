# changes/103-new-layout.py - new layout: tabs at the top (Roster, Matchup, Players, Lines, Trades, League, Setup); Roster is the first page with the score and week chart on top; Players has Free agents | Goalies | Injuries; games this matchup, around the league and who's carrying you move to Matchup; playoff odds move to League; goalie board removed

NEW_CSS = r'''  /* change 103 (install.py) */
  .gx-tm103 { background: var(--bg); }
  .gx-tm103 .hd { display: flex; align-items: center; gap: 10px; padding: 10px 14px 2px; }
  .gx-tm103 .nm { font-weight: 700; font-size: 18px; color: var(--ink); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .gx-tm103 .dt { width: 7px; height: 7px; border-radius: 99px; flex: none; }
  .gx-tm103 .sr { margin-left: auto; width: 36px; height: 36px; border-radius: 999px; background: var(--card); display: flex; align-items: center; justify-content: center; color: var(--ink); flex: none; }
  .gx-tm103 .sr svg { width: 18px; height: 18px; }
  .gx-tm103 .tb { display: flex; overflow-x: auto; scrollbar-width: none; -webkit-overflow-scrolling: touch; padding: 0 4px; }
  .gx-tm103 .tb::-webkit-scrollbar { display: none; }
  .gx-tm103 .tb a { flex: none; padding: 12px 12px 9px; font-size: 13px; font-weight: 700; letter-spacing: .04em; text-transform: uppercase; color: var(--mute); border-bottom: 3px solid transparent; transition: color .15s, border-color .2s; }
  .gx-tm103 .tb a.on { color: var(--ink); border-bottom-color: var(--accent); }
  .gx-seg103 { display: grid; grid-auto-flow: column; grid-auto-columns: 1fr; border: 1px solid var(--line2); border-radius: 10px; overflow: hidden; }
  .gx-seg103 button { padding: 8px 4px; font-size: 14px; color: var(--mute); border-left: 1px solid var(--line2); transition: background-color .15s, color .15s; }
  .gx-seg103 button:first-child { border-left: 0; }
  .gx-seg103 button.on { background: var(--ink); color: var(--bg); font-weight: 600; }
  .gx-lk103 { display: flex; align-items: center; justify-content: space-between; padding: 12px 2px; border-top: 1px solid var(--line); font-size: 15px; color: var(--ink); }
  .gx-lk103:first-of-type { border-top: 0; }
  .gx-lk103 span { color: var(--mute); }
  @media (max-width: 640px) {
    .gx-bb { display: none !important; }
    body { padding-bottom: 24px !important; }
  }
</style>'''

HELPERS = r'''// ---------- change 103: new layout, tabs at the top (install.py) ----------
const GX_TABS103 = [["roster", "Roster", "myteam", null], ["matchup", "Matchup", "matchup", null], ["players", "Players", "moves", "adddrop"], ["lines", "Lines", "lines", null], ["trades", "Trades", "moves", "trades"], ["league", "League", "league", "power"], ["setup", "Setup", "setup", "settings"]];
const gxTabOn103 = (k, tab) => {
  const sub = (window.__ROUTE || {}).sub;
  return k === "roster" ? tab === "myteam" || tab === "today" : k === "matchup" ? tab === "matchup" : k === "players" ? tab === "moves" && sub !== "trades"
    : k === "trades" ? tab === "moves" && sub === "trades" : k === "lines" ? tab === "lines" : k === "league" ? tab === "league" || tab === "teams" : tab === "setup" || tab === "news";
};
function GxTopM103({ s, tab, go, ageH }) {
  const ref = React.useRef(null);
  const sub = (window.__ROUTE || {}).sub;
  useEffect(() => {
    const n = ref.current, el = n && n.querySelector(".on");
    if (el) { try { n.scrollTo({ left: el.offsetLeft - n.clientWidth / 2 + el.clientWidth / 2, behavior: "smooth" }); } catch (e) {} }
  }, [tab, sub]);
  const dot = !s.lastSync ? "var(--faint)" : ageH !== null && ageH > 2 ? "var(--bad)" : "var(--good)";
  const name = teamName(s, s.me) || "Islands GM";
  return (
    <div className="m-only gx-tm103">
      <div className="hd">
        <span className="gx-badge">{(name[0] || "K").toUpperCase()}</span>
        <span className="nm">{name}</span>
        <span className="dt" style={{ background: dot }} title={s.lastSync ? "Synced " + fmtTime(s.lastSync) : "Not synced yet"}></span>
        <button type="button" className="sr" aria-label="Search" onClick={() => window.dispatchEvent(new Event("gm-search"))}>
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round"><circle cx="11" cy="11" r="7"></circle><path d="M20 20l-3.5-3.5"></path></svg>
        </button>
      </div>
      <nav className="tb" ref={ref} aria-label="Main">
        {GX_TABS103.map(([k, l, t, sb]) => (
          <a key={k} href={gxHash(t, sb || undefined)} className={gxTabOn103(k, tab) ? "on" : ""} onClick={(e) => { if (gxNewTab(e)) return; e.preventDefault(); go(t, sb || undefined); }}>{l}</a>
        ))}
      </nav>
    </div>
  );
}
const GX_PL103 = [["adddrop", "Free agents"], ["goalies", "Goalies"], ["injuries", "Injuries"]];
function GxSubBar103({ tab, sub, go, s, wk }) {
  if (tab === "matchup") return s && wk ? <MatchStrip s={s} wk={wk} /> : null;
  if (tab === "moves" && sub !== "trades") {
    if (sub === "planner" || sub === "advice" || sub === "players") return <div className="mb-3"><button type="button" className="text-sm text-blue-600" onClick={() => go("moves", "adddrop")}>{"\u2039 Back to Free agents"}</button></div>;
    const cur = GX_PL103.some((x) => x[0] === sub) ? sub : "adddrop";
    return <div className="gx-seg103 mb-3">{GX_PL103.map(([k, l]) => <button key={k} type="button" className={cur === k ? "on" : ""} onClick={() => go("moves", k)}>{l}</button>)}</div>;
  }
  const back = tab === "news" || (tab === "setup" && sub && sub !== "settings") ? ["Setup", () => go("setup", "settings")] : tab === "league" && (sub === "playoffs" || sub === "players") ? ["League", () => go("league", "power")] : null;
  return back ? <div className="mb-3"><button type="button" className="text-sm text-blue-600" onClick={back[1]}>{"\u2039 Back to " + back[0]}</button></div> : null;
}
// the boxes that used to sit lower on Today, now under the Matchup
function GxMuMore103({ s, wk }) {
  const K = s.blend, opp = oppOf(wk, s.me) || s.opp;
  const A = useMemo(() => weekLive(s.players.filter((p) => p.ft === s.me), wk, K, s.me), [s.players, wk, K]);
  const B = useMemo(() => weekLive(s.players.filter((p) => p.ft === opp), wk, K, opp), [s.players, wk, K, opp]);
  return <><GxGamesAny s={s} wk={wk} A={A} B={B} /><GxLeagueAny s={s} wk={wk} /><GxCarry s={s} wk={wk} /></>;
}
'''

LAPTOP_TABS = ('{GX_TABS103.map(([k, l, t, sb]) => <a key={k} href={gxHash(t, sb || undefined)} onClick={(e) => { if (gxNewTab(e)) return; e.preventDefault(); go(t, sb || undefined); }} '
               'className={"gx-tab" + (gxTabOn103(k, tab) ? " on" : "")}>{l}</a>)}\n')

MORE = '''      <div className="gx-pn" data-gx="103more">
        <a className="gx-lk103" href={gxHash("moves", "planner")}>Week plan<span>{"\\u203a"}</span></a>
        <a className="gx-lk103" href={gxHash("moves", "advice")}>Advice<span>{"\\u203a"}</span></a>
      </div>
      {sim ? <MoveSim s={sP}'''


def change(t):
    t = lit(t, "103: styles", "</style>", NEW_CSS, "change 103 (install.py)")
    t = lit(t, "103: helpers", ROOT, HELPERS + ROOT, "change 103: new layout")
    # Roster is the first page
    t = lit(t, "103: start on Roster", 'const [tab, setTab] = useState("today");', 'const [tab, setTab] = useState("myteam");', 'useState("myteam");')
    t = lit(t, "103: phone tabs at the top", "<MobileHeader s={s} setS={setS} tab={tab} go={go} ageH={ageH} />", "<GxTopM103 s={s} tab={tab} go={go} ageH={ageH} />", "<GxTopM103 s={s}")
    t = lit(t, "103: one row of choices", "<SubBar tab={tab} sub={sub} go={go} setSubs={setSubs} nav={nav} s={s} wk={wk} />", "<GxSubBar103 tab={tab} sub={sub} go={go} s={s} wk={wk} />", "<GxSubBar103 tab={tab}")
    # laptop tabs match the phone
    if "GX_TABS103.map(([k, l, t, sb]) => <a key={k} href={gxHash(t, sb || undefined)} onClick" in t:
        print("(install) 103: laptop tabs: already done")
    else:
        t2, k = re.subn(r"\{TABS\.map\(\(\[k, l, grp\]\) => <a key=\{k\} href=\{gxHash\(k\)\}[^\n]*\n", lambda m: LAPTOP_TABS, t)
        if k != 1:
            fail("103: laptop tabs: expected 1 place, found " + str(k))
        t = t2
        print("(install) 103: laptop tabs: updated")
    # Roster page = score and week chart, then the roster
    t = lit(t, "103: Today can show just its top", "function Today({ s, wk, go }) {", "function Today({ s, wk, go, top103 }) {", "function Today({ s, wk, go, top103 })")
    t = lit(t, "103: Today top only", "      <GxHome s={s} wk={wk} A={A} B={B} />\n", "      {top103 ? null : <GxHome s={s} wk={wk} A={A} B={B} />}\n", "{top103 ? null : <GxHome")
    t = lit(t, "103: roster page", '  if (tab === "today") content = <Today {...P} />;',
            '  if (tab === "today" || tab === "myteam") content = <div className="space-y-4"><Today {...P} top103 /><MyTeam {...P} /></div>;',
            '<Today {...P} top103 /><MyTeam {...P} />')
    t = lit(t, "103: matchup extras", '  else if (tab === "matchup") content = <Matchup {...P} />;',
            '  else if (tab === "matchup") content = <div className="space-y-4"><Matchup {...P} /><GxMuMore103 s={s} wk={wk} /></div>;',
            "<GxMuMore103 s={s} wk={wk} />")
    t = lit(t, "103: playoff odds on League", ": <LeaguePage {...P} />;", ': <div className="space-y-4"><LeaguePage {...P} /><GxPlayoff s={s} /></div>;', "<LeaguePage {...P} /><GxPlayoff s={s} />")
    t = lit(t, "103: plan and advice links", "      {sim ? <MoveSim s={sP}", MORE, 'data-gx="103more"')
    return t


edit(APP, change)
