# changes/285-roster-table-phone-menu.py - Roster page shows the table only (the Table / My team switch and the jersey room are gone); phone top menu is Roster, Matchup, Players, Lines, Trades and a gear for Setup (no More button); League opens from a Standings row at the bottom of Matchup on the phone

NEW_CSS = r'''  /* change 285 (install.py) */
  .gx-ll285 { display: none; }
  @media (max-width: 640px) {
    .gx-tm103 .tb .mr241.gr285 { flex: 0 0 44px; padding-left: 0; padding-right: 0; }
    .gx-tm103 .tb .mr241.gr285 svg { width: 19px; height: 19px; }
    .gx-ll285 { display: flex; align-items: center; gap: 10px; width: 100%; min-height: 56px; padding: 10px 14px; border-radius: 14px; background: var(--card); color: var(--ink); text-align: left; }
    .gx-ll285 > span:first-child { flex: 1; min-width: 0; }
    .gx-ll285 b { display: block; font-weight: 600; font-size: 15px; }
    .gx-ll285 small { display: block; font-size: 12px; color: var(--mute); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  }
</style>'''

RV_OLD = r'''      <div className="gx-seg103">{[["table", "Table"], ["team", "My team"]].map(([k, l]) => <button key={k} type="button" className={v === k ? "on" : ""} onClick={() => pick(k)}>{l}</button>)}</div>
      {v === "team" ? <GxMyRoom238 s={P.s} /> : <MyTeam {...P} />}'''
RV_NEW = r'''      <MyTeam {...P} />{/* change 285: table only */}'''

MORE_OLD = r'''        <GxMore241 tab={tab} go={go} />
      </nav>'''
MORE_NEW = r'''        <GxGear285 tab={tab} go={go} />
      </nav>'''

MU_OLD = r'''<Matchup {...P} />{/* gx105: games, league and carrying boxes removed */}'''
MU_NEW = r'''<Matchup {...P} /><GxLgLink285 go={P.go} />{/* gx105: games, league and carrying boxes removed */}'''

HELPERS = r'''// ---------- change 285: phone menu gear, League row on Matchup (install.py) ----------
function GxGear285({ tab, go }) {
  const on = tab === "setup" || tab === "news";
  return (
    <a href={gxHash("setup", "settings")} className={"mr241 gr285" + (on ? " on" : "")} data-gx="285" aria-label="Setup" onClick={(e) => { if (gxNewTab(e)) return; e.preventDefault(); go("setup", "settings"); }}>
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="3.2"></circle><path d="M19.4 13.5a1.6 1.6 0 0 0 .3 1.8l.1.1a2 2 0 1 1-2.8 2.8l-.1-.1a1.6 1.6 0 0 0-1.8-.3 1.6 1.6 0 0 0-1 1.5V19.5a2 2 0 1 1-4 0v-.1a1.6 1.6 0 0 0-1-1.5 1.6 1.6 0 0 0-1.8.3l-.1.1a2 2 0 1 1-2.8-2.8l.1-.1a1.6 1.6 0 0 0 .3-1.8 1.6 1.6 0 0 0-1.5-1H3.5a2 2 0 1 1 0-4h.1a1.6 1.6 0 0 0 1.5-1 1.6 1.6 0 0 0-.3-1.8l-.1-.1a2 2 0 1 1 2.8-2.8l.1.1a1.6 1.6 0 0 0 1.8.3h.1a1.6 1.6 0 0 0 1-1.5V3.5a2 2 0 1 1 4 0v.1a1.6 1.6 0 0 0 1 1.5 1.6 1.6 0 0 0 1.8-.3l.1-.1a2 2 0 1 1 2.8 2.8l-.1.1a1.6 1.6 0 0 0-.3 1.8v.1a1.6 1.6 0 0 0 1.5 1h.2a2 2 0 1 1 0 4h-.1a1.6 1.6 0 0 0-1.5 1z"></path></svg>
    </a>
  );
}
function GxLgLink285({ go }) {
  return (
    <a href={gxHash("league", "power")} className="gx-ll285" data-gx="285" onClick={(e) => { if (gxNewTab(e)) return; e.preventDefault(); go("league", "power"); }}>
      <span><b>League</b><small>Standings, every matchup this week, playoff odds</small></span>
      <span className="sec-chev shut" style={{ margin: "0 4px 0 0" }}></span>
    </a>
  );
}
'''


def change(t):
    t = lit(t, "285: styles", "</style>", NEW_CSS, "change 285 (install.py)")
    t = lit(t, "285: helpers", ROOT, HELPERS + ROOT, "change 285: phone menu gear")
    t = lit(t, "285: roster table only", RV_OLD, RV_NEW, "change 285: table only")
    t = lit(t, "285: gear instead of More", MORE_OLD, MORE_NEW, "<GxGear285 tab={tab}")
    t = lit(t, "285: League row on Matchup", MU_OLD, MU_NEW, "<GxLgLink285 go={P.go}")
    return t

edit(APP, change)
