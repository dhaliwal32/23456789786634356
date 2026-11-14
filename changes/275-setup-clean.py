# changes/275-setup-clean.py - Setup cleaned up: one short page (your team, favourite team, watch link, alerts, autopilot, protected players, AI), everything rarely used moved under More

NEW_CSS = r'''  /* change 275 (install.py) */
  .gx-st275 { display: block; margin: 18px 4px 6px; }
</style>'''

OLD_START = r'''      <div className="gx-pn" style={{ paddingTop: 2, paddingBottom: 2 }}>
        {row("display", "Display", themeTxt'''
OLD_END = r'''{row("history", "Prediction history", "Every projection and what happened", () => window.open("ai-history.html", "_blank"), 7)}'''

NEW_LIST = r'''      {/* change 275: short Setup */}
      <div className="gx-tag gx-st275">App</div>
      <div className="gx-pn" style={{ paddingTop: 2, paddingBottom: 2 }}>
        <div className="gx-sr" style={{ borderTop: 0 }}><span>My team</span><GxMeSel241 s={s} /></div>
        <div className="gx-sr"><span>Favourite team</span><GxFavSel112 /></div>
        <div className="gx-sr"><span>Watch link</span><GxWatchSel174 /></div>
      </div>
      <div className="gx-tag gx-st275">Alerts and lineup</div>
      <div className="gx-pn" style={{ paddingTop: 2, paddingBottom: 2 }}>
        {row("alerts", "Phone alerts", alertTxt, () => go("setup", "alerts"), 0)}<GxAutoRow row={row} go={go} />{/* gx089-row */}
        {row("rules", "Protected players", (top + kept.length) + " players the app will never tell you to drop", () => go("setup", "rules"), 1)}
      </div>
      <div className="gx-tag gx-st275">AI</div>
      <div className="gx-pn" style={{ paddingTop: 2, paddingBottom: 2 }}>
        {row("ailab", "AI Lab", "How each projection is doing", () => window.open("ai-dashboard.html", "_blank"), 0)}
        {row("history", "Prediction history", "Every projection and what happened", () => window.open("ai-history.html", "_blank"), 1)}
      </div>
      <div className="gx-tag gx-st275">Rarely used</div>
      <div className="gx-pn" style={{ paddingTop: 2, paddingBottom: 2 }}>
        {row("more", "More", "Injury dates, edit players, betting lines, schedule, backup", () => go("setup", "more"), 0)}'''

OLD_PLAYERS = r'''  if (sub === "players") return page("Players and injuries", <>'''
NEW_MORE = r'''  if (sub === "more") return page("More", <>
    <div className="gx-sr" style={{ borderTop: 0 }}><span>Theme</span>{seg([["auto", "Automatic"], ["light", "Light"], ["dark", "Dark"]], theme, (k) => window.__setTheme && window.__setTheme(k))}</div>
    {row("inj", "Injury return dates", outN ? outN + " of your players hurt or on IR" : "Everyone on your team is healthy", () => go("setup", "inj"), 1)}
    {row("bulk", "Edit players", "Projections, play %, fantasy team", () => go("setup", "bulk"), 2)}
    {row("news", "News", newsN ? newsN + " of your players in the news" : "Nothing new on your players", () => go("news"), 3)}
    {row("odds", "Betting lines", "Win chances and expected goals for each game", () => go("setup", "odds"), 4)}
    {row("sched", "Schedule", "Games per NHL team this week", () => go("setup", "sched"), 5)}
    {row("data", "Data and backup", (bad.length ? "Not working: " + bad.join(", ") : "All " + src.length + " data sources working") + " \u00b7 backup \u00b7 advanced", () => go("setup", "data"), 6)}
  </>); /* change 275: More page */
''' + OLD_PLAYERS


def change(t):
    t = lit(t, "275: styles", "</style>", NEW_CSS, "change 275 (install.py)")
    if "change 275: short Setup" not in t:
        a, b = t.find(OLD_START), t.find(OLD_END)
        if t.count(OLD_START) != 1 or t.count(OLD_END) != 1 or b < a:
            fail("275: could not find the Setup list")
        t = t[:a] + NEW_LIST + t[b + len(OLD_END):]
        print("(install) 275: setup list: updated")
    t = lit(t, "275: more page", OLD_PLAYERS, NEW_MORE, "change 275: More page")
    return t

edit(APP, change)
