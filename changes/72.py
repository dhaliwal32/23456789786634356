# changes/072-page-addresses.py - every page and player pop-up gets its own address, so links open in new tabs and Back works

HELPERS = r'''// ---------- change 072: page addresses and links that open in a new tab (install.py) ----------
const GX_RT = ["today", "matchup", "myteam", "moves", "lines", "league", "teams", "news", "setup"];
const GX_RDEF = { moves: "adddrop", league: "power", setup: "settings" };
const GX_TEAM_HREF = { roster: "#myteam", pickups: "#moves", plan: "#moves/planner", trades: "#moves/trades", lines: "#lines" };
const gxHash = (tab, sub, team, pid) => {
  const t = GX_RT.indexOf(tab) >= 0 ? tab : "today";
  let h = "#" + t;
  if (GX_RDEF[t] && sub && sub !== GX_RDEF[t]) h += "/" + sub;
  if (t === "teams" && team) h += "/" + team;
  if (pid) h += "&p=" + encodeURIComponent(pid);
  return h;
};
const gxParseHash = (h) => {
  const m = String(h || "").replace(/^#\/?/, "").split("&p=");
  const parts = m[0].split("/").filter(Boolean), tab = parts[0];
  if (!tab || GX_RT.indexOf(tab) < 0) return null;
  const r = { tab, sub: null, team: null, pid: m[1] ? decodeURIComponent(m[1]) : null };
  if (tab === "teams") r.team = parts[1] || null;
  else if (GX_RDEF[tab]) r.sub = parts[1] || GX_RDEF[tab];
  return r;
};
const gxNewTab = (e) => !!(e && (e.metaKey || e.ctrlKey || e.shiftKey || e.button === 1));
const gxPHref = (p) => { const R = window.__ROUTE || {}; return gxHash(R.tab, R.sub, R.team, p && p.id); };

'''

OLD_APP = r'''  window.__PMODE = window.__MODEL ? s.pmode || "blend" : "espn";'''

APP_HOOKS = r'''  // change 072 (gx072-app): keep the address bar in step with the page, and follow Back and Forward
  window.__ROUTE = { tab, sub: subs[tab], team: tab === "teams" ? teamView : null };
  const gxWant = React.useRef(null);
  useEffect(() => {
    if (!loaded) return;
    const apply = () => {
      const r = gxParseHash(window.location.hash);
      if (!r) return;
      const pl = r.pid ? (window.__PLAYERS || []).find((p) => p.id === r.pid) || null : null;
      const want = gxHash(r.tab, r.sub, r.team, pl ? pl.id : null);
      gxWant.current = want;
      setTimeout(() => { if (gxWant.current === want) gxWant.current = null; }, 1500);
      setTab(r.tab);
      if (r.sub) setSubs((x) => ({ ...x, [r.tab]: r.sub }));
      setTeamView(r.tab === "teams" ? r.team : null);
      setPlayer(pl);
    };
    apply();
    window.addEventListener("popstate", apply);
    return () => window.removeEventListener("popstate", apply);
  }, [loaded]);
  useEffect(() => {
    if (!loaded) return;
    const h = gxHash(tab, subs[tab], tab === "teams" ? teamView : null, player ? player.id : null);
    if (gxWant.current) { if (h === gxWant.current) gxWant.current = null; return; }
    if (window.location.hash === h) return;
    try { if (!window.location.hash) window.history.replaceState(null, "", h); else window.history.pushState(null, "", h); } catch (e) {}
  }, [loaded, tab, subs[tab], teamView, player ? player.id : null]);
'''

OLD_PN = r'''<button type="button" className={"hover:underline text-left " + (className === undefined ? "font-medium" : className)} onClick={(e) => { e.stopPropagation(); if (window.__NAV) window.__NAV.player(p); }}>{p.n}</button>'''
NEW_PN = r'''<a href={gxPHref(p)} className={"hover:underline text-left " + (className === undefined ? "font-medium" : className)} onClick={(e) => { /* gx072-pn */ e.stopPropagation(); if (gxNewTab(e)) return; e.preventDefault(); if (window.__NAV) window.__NAV.player(p); }}>{p.n}</a>'''

OLD_TL = r'''<button type="button" className={"hover:underline text-left " + (className || "")} onClick={(e) => { e.stopPropagation(); if (window.__NAV) window.__NAV.team(id); }}>{nm}</button>'''
NEW_TL = r'''<a href={id === s.me ? "#myteam" : gxHash("teams", null, id)} className={"hover:underline text-left " + (className || "")} onClick={(e) => { /* gx072-tl */ e.stopPropagation(); if (gxNewTab(e)) return; e.preventDefault(); if (window.__NAV) window.__NAV.team(id); }}>{nm}</a>'''

OLD_TOP = r'''<button key={k} onClick={() => go(k, k === "setup" ? "settings" : k === "league" ? "power" : undefined)} className={"gx-tab" + (grp.indexOf(tab) >= 0 ? " on" : "")}>{l}{W[k] ? <i className="gx-wd" title="Needs a look"></i> : null}</button>'''
NEW_TOP = r'''<a key={k} href={gxHash(k)} onClick={(e) => { /* gx072-top */ if (gxNewTab(e)) return; e.preventDefault(); go(k, k === "setup" ? "settings" : k === "league" ? "power" : undefined); }} className={"gx-tab" + (grp.indexOf(tab) >= 0 ? " on" : "")}>{l}{W[k] ? <i className="gx-wd" title="Needs a look"></i> : null}</a>'''

OLD_SUB = r'''<Pills items={TEAM_SUBS} value={cur} onChange={to} />'''
NEW_SUB = r'''<div className="flex gap-2 overflow-x-auto navscroll pb-1">{/* gx072-sub */}{TEAM_SUBS.map(([k, l]) => <a key={k} href={GX_TEAM_HREF[k]} onClick={(e) => { if (gxNewTab(e)) return; e.preventDefault(); to(k); }} className={"px-3 py-1.5 rounded-full text-sm border whitespace-nowrap " + (cur === k ? "bg-blue-600 text-white border-blue-600" : "bg-white border-slate-300 text-slate-600")}>{l}</a>)}</div>'''

OLD_PICK = r'''<button key={k} type="button" onClick={() => go("moves", k)} className={"whitespace-nowrap " + (sub === k || (k === "adddrop" && !inPick) ? "font-semibold" : "text-slate-500")}>{l}</button>'''
NEW_PICK = r'''<a key={k} href={gxHash("moves", k)} onClick={(e) => { /* gx072-pick */ if (gxNewTab(e)) return; e.preventDefault(); go("moves", k); }} className={"whitespace-nowrap " + (sub === k || (k === "adddrop" && !inPick) ? "font-semibold" : "text-slate-500")}>{l}</a>'''

OLD_ROW = r'''  const row = (k, title, sumTxt, fn, i) => (
    <button key={k} type="button" className="gx-lk" style={i ? null : { borderTop: 0 }} onClick={fn}>
      <span className="min-w-0" style={{ flex: 1 }}><span className="block">{title}</span>{sumTxt ? <span className="block text-xs text-slate-500 truncate">{sumTxt}</span> : null}</span>
      <span className="sec-chev shut" style={{ margin: "0 4px 0 12px" }}></span>
    </button>
  );'''
NEW_ROW = r'''  const row = (k, title, sumTxt, fn, i) => { /* gx072-row */
    const ext = k === "ailab" ? "ai-dashboard.html" : k === "history" ? "ai-history.html" : "";
    const href = ext || (k === "news" ? "#news" : gxHash("setup", k));
    return (
      <a key={k} href={href} target={ext ? "_blank" : undefined} rel={ext ? "noopener" : undefined} className="gx-lk" style={i ? null : { borderTop: 0 }} onClick={(e) => { if (ext || gxNewTab(e)) return; e.preventDefault(); fn(e); }}>
        <span className="min-w-0" style={{ flex: 1 }}><span className="block">{title}</span>{sumTxt ? <span className="block text-xs text-slate-500 truncate">{sumTxt}</span> : null}</span>
        <span className="sec-chev shut" style={{ margin: "0 4px 0 12px" }}></span>
      </a>
    );
  };'''


def change(t):
    t = lit(t, "072: helpers", ROOT, HELPERS + ROOT, "change 072: page addresses")
    t = lit(t, "072: app hooks", OLD_APP, APP_HOOKS + OLD_APP, "gx072-app")
    t = lit(t, "072: player names", OLD_PN, NEW_PN, "gx072-pn")
    t = lit(t, "072: team names", OLD_TL, NEW_TL, "gx072-tl")
    t = lit(t, "072: top bar", OLD_TOP, NEW_TOP, "gx072-top")
    t = lit(t, "072: team sub-tabs", OLD_SUB, NEW_SUB, "gx072-sub")
    t = lit(t, "072: pickup sub-tabs", OLD_PICK, NEW_PICK, "gx072-pick")
    t = lit(t, "072: setup rows", OLD_ROW, NEW_ROW, "gx072-row")
    for must in ("function App(", "function Today(", "function SetupPage(", "gxParseHash(window.location.hash)"):
        if must not in t:
            fail("fantasy-gm.html looks damaged after change 072 (" + must + ").")
    return t


edit(APP, change)
