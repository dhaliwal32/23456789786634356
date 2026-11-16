# changes/309-calmer-tonight-say.py - calmer "data is old" warning, laptop shows the same 5 tabs as the phone plus a Setup gear, Matchup rows compact before games start, a one-line state of the matchup on the Roster box, and a "Tonight" card with only what needs doing before puck drop

NEW_CSS = r'''  /* change 309 (install.py) */
  .gx-say309 { font-size: 14px; line-height: 1.45; color: var(--ink2, var(--ink)); margin: 10px 0 2px; }
  .gxg309 { display: flex; align-items: flex-end; }
  .gxg309 a { display: flex; align-items: center; padding: 6px 8px 12px; color: var(--mute); border-bottom: 2px solid transparent; }
  .gxg309 a.on { color: var(--ink); border-bottom-color: var(--accent); }
  .gxg309 svg { width: 18px; height: 18px; }
  .gx-tn309 .pl .tg { flex: none; font-size: 12px; color: var(--mute); white-space: nowrap; }
  .gx-tn309 .ok { padding: 4px 0 2px; font-size: 14px; color: var(--mute); }
  /* rows are only tall once a game has started and they carry a stat line; before that they stay compact */
  .gx-h2h > .gx-pc { min-height: 44px; }
  *:has(> .gx-h2h .gx-sl98) > .gx-h2h > .gx-pc { min-height: 72px; }
  @media (max-width: 640px) {
    .gx-h2h > .gx-pc { min-height: 40px; }
    *:has(> .gx-h2h .gx-sl98) > .gx-h2h > .gx-pc { min-height: 64px; }
  }
</style>'''

HELPERS = r'''// ---------- change 309: state of the matchup line, Tonight card, laptop gear (install.py) ----------
// one plain line under the Roster box score: where it stands now, who has more games left, and the move that helps most
// (the projected margin is already on the line above, so it is not repeated)
function GxSay309({ sa, sb, la, lb, over, up, ml }) {
  const [bp, setBp] = useState(() => window.__BP309 || null);
  useEffect(() => { const f = () => setBp(window.__BP309 || null); window.addEventListener("gx-bp309", f); return () => window.removeEventListener("gx-bp309", f); }, []);
  if (over) return null;
  const pl = (n) => n + " game" + (n === 1 ? "" : "s"), more = (n) => n + " more game" + (n === 1 ? "" : "s");
  const d = sa - sb;
  const a = up ? "Your week hasn't started yet." : Math.abs(d) < 0.05 ? "You're tied right now." : d > 0 ? "You lead by " + f1(d) + " right now." : "You trail by " + f1(-d) + " right now.";
  const g = la === lb ? " You both have " + pl(la) + " left." : la > lb ? " You have " + more(la - lb) + " left than them." : " They have " + more(lb - la) + " left than you.";
  const o = bp && bp.top;
  const t = ml !== 0 && o && o.a != null && bp.b != null && o.a - bp.b >= 0.02 && o.f && o.d ? " Adding " + o.f.n + " for " + lastN(o.d.n) + " takes you from " + wpTxt(bp.b) + " to " + wpTxt(o.a) + "." : "";
  return <div className="gx-say309" data-gx="309s">{a + g + t}</div>;
}
// only what needs doing before puck drop tonight; says so plainly when there is nothing
function GxTonight309({ s, wk }) {
  const today = todayISO(), gen = (window.ESPN_DATA || {}).generated;
  const v = useMemo(() => {
    try {
      const dates = (wk && wk.dates) || [], di = dates.indexOf(today);
      const mine = s.players.filter((p) => p.ft === s.me && !p.ir);
      const plays = (p) => SCHED[p.t] && SCHED[p.t].has(today);
      const pre = (p) => gState(p.t, today).s === "P";
      const tonight = mine.filter(plays);
      if (!tonight.length) return null;
      const byId = {}; s.players.forEach((p) => (byId[p.id] = p));
      const L = di >= 0 ? weekLive(mine, wk, s.blend, s.me, { detail: true }) : null;
      const day = L && L.days ? L.days[di] : null;
      const inLine = new Set(((day && day.start) || []).map((q) => q.id));
      const when = (p) => { const g = gameOf(p.t, today); return g ? (g.h ? "v " : "@ ") + g.o + " \u00b7 " + gameTime(g) : ""; };
      const out = [];
      if (day && day.empty > 0 && tonight.some(pre) && movesLeft(s, s.me, wk) !== 0) out.push({ k: "empty", t: day.empty + " empty lineup spot" + (day.empty === 1 ? "" : "s") + " tonight", sub: "A pickup with a game tonight would fill it", act: "Find one" });
      tonight.filter(pre).forEach((p) => {
        const stt = String(p.status || "").toUpperCase();
        if (OUTS.includes(stt)) { out.push({ k: "out", p, t: p.n, sub: "Listed " + (stt === "INJURY_RESERVE" ? "on IR" : stt.toLowerCase()) + " \u00b7 keep him out of your lineup", tag: when(p) }); return; }
        if (p.p !== "G") return;
        const g = gStart(p, today), l = String(g.l || "").toLowerCase(), conf = l.includes("confirm") && !l.includes("un");
        if (inLine.has(p.id) && g.v < 0.5) out.push({ k: "g", p, t: p.n, sub: "In your lineup but probably not starting (" + Math.round(g.v * 100) + "%)", tag: when(p) });
        else if (g.v >= 0.5 && !conf) out.push({ k: "g", p, t: p.n, sub: "Expected to start, not confirmed yet", tag: when(p) });
      });
      return { out, n: tonight.length };
    } catch (e) { return null; }
  }, [s.players, wk, today, gen, s.blend]);
  if (!v) return null;
  const openP = (p) => { if (p && window.__NAV) window.__NAV.player(byIdP(s, p.id) || p); };
  return (
    <div className="gx-pn gx-ir253 gx-tn309" data-gx="309t">
      <div className="gx-tag" style={{ marginBottom: 6 }}>Tonight</div>
      {!v.out.length ? <div className="ok">{"Nothing to do tonight. " + v.n + " of your players have a game."}</div> : v.out.map((x, j) => (
        <div key={j} className="pl">
          {x.p ? <GxFace p={x.p} size={30} /> : null}
          <button type="button" className="nm text-left" onClick={() => (x.p ? openP(x.p) : (window.location.hash = gxHash("moves", "adddrop")))}><b>{x.t}</b><small>{x.sub}</small></button>
          {x.act ? <button type="button" className="bt" onClick={() => (window.location.hash = gxHash("moves", "adddrop"))}>{x.act}</button> : <span className="tg">{x.tag}</span>}
        </div>
      ))}
    </div>
  );
}
const byIdP = (s, id) => s.players.find((q) => q.id === id) || null;
'''


def change(t):
    t = lit(t, "309: styles", "</style>", NEW_CSS, "change 309 (install.py)")
    t = lit(t, "309: helpers", ROOT, HELPERS + ROOT, "change 309: state of the matchup line")
    # 2. calmer warning: only after half a day, and in plain words
    t = lit(t, "309: warning after 12 hours", "{ageH !== null && ageH > 2 && (", "{ageH !== null && ageH > 12 && (", "ageH > 12 && (")
    t = lit(t, "309: warning words",
            "Data is {Math.round(ageH)} hours old \u2014 the automatic sync may have stopped. Check GitHub \u2192 Actions for a red \u2715.",
            "No new data for {Math.round(ageH)} hours. The automatic sync may have stopped.",
            "No new data for {Math.round(ageH)} hours")
    t = lit(t, "309: laptop dot",
            'background: !s.lastSync ? "var(--faint)" : ageH !== null && ageH > 2 ? "var(--bad)" : "var(--good)" }}></span>',
            'background: !s.lastSync ? "var(--faint)" : ageH !== null && ageH > 12 ? "var(--bad)" : ageH !== null && ageH > 2 ? "var(--faint)" : "var(--good)" }}></span>',
            'ageH > 12 ? "var(--bad)" : ageH !== null && ageH > 2 ? "var(--faint)" : "var(--good)" }}></span>')
    t = lit(t, "309: laptop updated time",
            '{sync ? "Synced " + sync.toLocaleTimeString([], { hour: "numeric", minute: "2-digit" }) : "Not synced yet"}',
            '{sync ? (ageH !== null && ageH > 2 ? "Updated " + Math.round(ageH) + " h ago" : "Synced " + sync.toLocaleTimeString([], { hour: "numeric", minute: "2-digit" })) : "Not synced yet"}',
            '"Updated " + Math.round(ageH) + " h ago"')
    t = lit(t, "309: phone dot",
            'const dot = !s.lastSync ? "var(--faint)" : ageH !== null && ageH > 2 ? "var(--bad)" : "var(--good)";',
            'const dot = !s.lastSync ? "var(--faint)" : ageH !== null && ageH > 12 ? "var(--bad)" : ageH !== null && ageH > 2 ? "var(--faint)" : "var(--good)";',
            'const dot = !s.lastSync ? "var(--faint)" : ageH !== null && ageH > 12')
    # 3. laptop: the phone's 5 tabs, Search, and a gear for Setup (League opens from the strength card, AI Lab from Setup)
    t = lit(t, "309: laptop tabs",
            '{GX_TABS103.map(([k, l, t, sb]) => <a key={k} href={gxHash(t, sb || undefined)} onClick={(e) => { if (gxNewTab(e)) return; e.preventDefault(); go(t, sb || undefined); }} className={"gx-tab" + (gxTabOn103(k, tab) ? " on" : "")}>{l}</a>)}',
            '{GX_TABS103.filter((x) => GX_MAIN241.includes(x[0])).map(([k, l, t, sb]) => <a key={k} href={gxHash(t, sb || undefined)} onClick={(e) => { if (gxNewTab(e)) return; e.preventDefault(); go(t, sb || undefined); }} className={"gx-tab" + (gxTabOn103(k, tab) ? " on" : "")}>{l}</a>)}',
            'GX_TABS103.filter((x) => GX_MAIN241.includes(x[0])).map(([k, l, t, sb]) => <a key={k} href={gxHash(t, sb || undefined)} onClick')
    t = lit(t, "309: no AI Lab tab",
            '      <a className="gx-tab" href="ai-dashboard.html" target="_blank" rel="noopener" data-r63="ailab">AI Lab</a>\n',
            '', None)
    t = lit(t, "309: laptop gear",
            '      <button type="button" className="ml-auto gx-tab" onClick={() => window.dispatchEvent(new Event("gm-search"))}>Search</button>\n',
            '      <button type="button" className="ml-auto gx-tab" onClick={() => window.dispatchEvent(new Event("gm-search"))}>Search</button>\n      <span className="gxg309" data-gx="309g"><GxGear285 tab={tab} go={go} /></span>\n',
            'className="gxg309"')
    # 4. the state of the matchup line, and the best pickup shares its answer with it
    t = lit(t, "309: matchup line",
            '<span>{f1(fb)}</span></div>\n      <div className="dys">',
            '<span>{f1(fb)}</span></div>\n      {mineMu ? <GxSay309 sa={sa} sb={sb} la={leftA} lb={leftB} over={over} up={up} ml={movesLeft(s, s.me, w)} /> : null}\n      <div className="dys">',
            '<GxSay309 sa={sa}')
    t = lit(t, "309: share best pickup",
            '        if (!dead) { setL({ b, opts }); setIx(0); }',
            '        if (!dead) { setL({ b, opts }); setIx(0); window.__BP309 = { b, top: opts[0] || null }; window.dispatchEvent(new Event("gx-bp309")); }',
            'window.__BP309 = { b, top')
    # 5. Tonight card under the Roster box
    t = lit(t, "309: tonight card",
            '{top103 ? <GxIrBack253 s={s} /> : null}',
            '{top103 ? <GxTonight309 s={s} wk={wk} /> : null}{top103 ? <GxIrBack253 s={s} /> : null}',
            '<GxTonight309 s={s} wk={wk} />')
    return t


edit(APP, change)
