# changes/152-matchup-espn-order-live.py - Matchup in ESPN's lineup order, no LIVE/FINAL tags, players wait for puck drop, live scores keep updating, even spacing, GP before FPTS, grey numbers, sort fixes, trackpad scroll on the player page

NEW_CSS = r'''  /* change 152 (install.py) */
  .gx-h2h [data-gx="094p"], .gx-h2h [data-gx="135n"] > div { white-space: nowrap; }
  .gx-pd, .gx-pd-bd { overscroll-behavior: auto; }
  .gx-sd141 .gm .tr b, .gx-ns131 .tr b { flex: none; width: 24px; text-align: right; font-variant-numeric: tabular-nums; }
  .gx-sd141 .gm .tr i, .gx-ns131 .tr i { flex: none; }
  .gx-sd141 .gm .tr i:not(.ar), .gx-ns131 .tr i:not(.ar) { width: 6px; }
  .gx-sd141 .gm .tms { width: 160px; }
  .gx-face.gx-fb152 { display: inline-flex; align-items: center; justify-content: center; }
  .gx-sc99 .gx-ro:not(.gx-roh) > .n:not([style]), .gx-sc99 .gx-ro:not(.gx-roh) > .n > div:not([style]),
  .gx-sc99 .gx-pk:not(.text-xs) > .n:not([style]), .gx-sc99 .gx-rk:not(.gx-rkh) > .n,
  .gx-sc99 .gx-ro > :nth-child(12), .gx-sc99 .gx-pk > :nth-child(10), .gx-sc99.gx-rk106 > .gx-rk > :nth-child(8) { color: var(--mute) !important; font-weight: 400 !important; }
  .gx-sc99 .gx-roh > .on, .gx-sc99 .gx-pk.text-xs > .on, .gx-sc99 .gx-rkh > .on { color: var(--ink) !important; }
  .gx-sc99 .gx-ro > :nth-child(13) { order: 1; }
  .gx-sc99 .gx-ro { grid-template-columns: 44px 200px 40px 62px 72px 70px 40px 40px 42px 46px 46px 46px 48px 44px 56px; }
  .gx-sc99 .gx-pk > :nth-child(11) { order: 1; }
  .gx-sc99 .gx-pk.full { grid-template-columns: 44px 220px 40px 62px 56px 70px 66px 58px 62px 56px 40px 40px 42px 46px 46px 46px 48px 44px 56px; }
  .gx-sc99.gx-rk106 > .gx-rk > :nth-child(4), .gx-sc99.gx-rk106 > .gx-rk > :nth-child(8), .gx-sc99.gx-rk106 > .gx-rk > :nth-child(9) { order: 1; }
  .gx-sc99.gx-rk106 > .gx-rk > :nth-child(5) { display: none !important; }
  .gx-sc99.gx-rk106 > .gx-rk { grid-template-columns: 38px 44px 200px 170px 40px 62px 64px 70px 40px 40px 42px 46px 46px 46px 48px 44px 56px; }
  @media (max-width: 640px) {
    .gx-sc99 .gx-ro { grid-template-columns: 36px 142px 34px 56px 62px 60px 34px 34px 36px 40px 40px 42px 44px 40px 52px; }
    .gx-sc99 .gx-pk.full { grid-template-columns: 36px 150px 34px 56px 52px 64px 60px 52px 58px 52px 34px 34px 36px 40px 40px 42px 44px 40px 52px; }
    .gx-sc99.gx-rk106 > .gx-rk { grid-template-columns: 30px 36px 142px 34px 56px 50px 56px 34px 34px 36px 40px 40px 42px 44px 40px 52px; }
  }
</style>'''

HELPERS = r'''// ---------- change 152: Matchup rows in ESPN's own lineup order (install.py) ----------
// ESPN's daily lineup (slot per player, in ESPN's order) for a team on a day, shaped like full147's output; null when ESPN has no lineup for that day
function gxOrd152(s, id, l, dt, K) {
  const AD = dt ? actDay(id, dt) : null;
  if (!AD || !Object.keys(AD).length) return null;
  const SL = { 3: "F", 4: "D", 6: "UTIL", 5: "G", 7: "BE", 8: "IR" };
  const by = {}; s.players.forEach((p) => (by[p.id] = p));
  const st = {}, bn = {};
  (l.start || []).forEach((p) => (st[p.id] = p)); (l.bench || []).forEach((p) => (bn[p.id] = p));
  const out = { F: [], D: [], UTIL: [], G: [], BE: [], IR: [] };
  const ord = ((((window.ESPN_DATA || {}).dorder || {})[dt]) || {})[String(id).replace(/^t/, "")];
  (ord && ord.length ? ord.filter((k) => AD[k]) : Object.keys(AD)).forEach((pid) => {
    const v = AD[pid], sl = SL[v && v[1]], p0 = by["e" + pid];
    if (!sl || !p0) return;
    const g = gameOf(p0.t, dt);
    if (sl === "BE" || sl === "IR") { const o = Object.assign({}, st[p0.id] || bn[p0.id] || p0, { slot: sl, dt }); if (g && sl === "BE") o.bench147 = true; else o.idle147 = true; out[sl].push(o); return; }
    if (st[p0.id]) { out[sl].push(Object.assign({}, st[p0.id], { slot: sl })); return; }
    if (!g) { out[sl].push(Object.assign({}, p0, { slot: sl, dt, idle147: true })); return; }
    const gs = gState(p0.t, dt), isG = p0.p === "G", gst = isG ? gStart(p0, dt) : null;
    const x0 = effAvg(p0, K, dt) * (isG ? (gst ? gst.v : p0.prob) : p0.prob) * avail(p0, dt);
    const on = gs.s !== "P";
    out[sl].push(Object.assign({}, p0, { slot: sl, dt, st: on ? gs.s : "", a: on ? gxLiveA120(p0, dt, v[0]) : null, x0, x: on ? 0 : x0, gs: gst ? gst.l : "" }));
  });
  return out;
}
// ---------- change 152: live data never gets stuck (install.py) ----------
// a feed call that hangs (phone asleep, slow network) gives up after 12 seconds, so the next pull can run
(function () {
  if (window.__GXF152) return;
  const f0 = window.fetch;
  window.__GXF152 = f0;
  window.fetch = function (u, o) {
    const s = typeof u === "string" ? u : (u && u.url) || "";
    if (s.indexOf("site.api.espn.com") < 0 && s.indexOf("api-web.nhle.com") < 0) return f0.call(window, u, o);
    return new Promise((res, rej) => {
      const t = setTimeout(() => rej(new Error("timeout")), 12000);
      f0.call(window, u, o).then((r) => { clearTimeout(t); res(r); }, (e) => { clearTimeout(t); rej(e); });
    });
  };
})();
'''

def change(t):
    t = lit(t, "152: styles", "</style>", NEW_CSS, "change 152 (install.py)")
    t = lit(t, "152: helpers", ROOT, HELPERS + ROOT, "change 152: Matchup rows in ESPN")
    # Matchup: ESPN's own order and slots for days ESPN has a lineup
    t = lit(t, "152: ESPN order",
            "const fa147 = full147(a, x), fb147 = full147(b, y);",
            "const fa147 = gxOrd152(s, a, x, dates[d], K) || full147(a, x), fb147 = gxOrd152(s, b, y, dates[d], K) || full147(b, y); /* gx152 */",
            "gxOrd152(s, a, x, dates[d], K)")
    # no "Today - live" line, no Final word on phone rows
    t = lit(t, "152: day tag",
            '<div style={{ display: "flex", alignItems: "baseline", marginBottom: 6 }}>\n          <span className="gx-tag">{(dates[d] === today',
            '<div style={{ display: "none" }} data-gx="152t">\n          <span className="gx-tag">{(dates[d] === today',
            'data-gx="152t"')
    t = lit(t, "152: total label",
            '<div>{state === "final" ? "Final" : state === "live" ? "Live" : "Projected"}</div>',
            '<div>{state === "final" ? "Final" : state === "live" ? "Today" : "Projected"}</div>',
            'state === "live" ? "Today" : "Projected"')
    t = lit(t, "152: no Final word",
            '{p.st === "F" ? <span className="m-inl"> Final</span> : null}',
            '{null /* gx152 */}',
            '{null /* gx152 */}')
    # LIVE and FINAL pills gone everywhere; the score and clock stay
    t = sub_once(t, "152: no pills",
            r'      \{st === "L" \? <span className="gm-pill[^\n]*\n',
            '      {null /* gx152 pills */}\n',
            "gx152 pills")
    # a player counts as started only once the puck drops
    t = lit(t, "152: puck drop",
            "  const x = ((window.__LIVESC || {})[dt] || {})[t] || ((((window.ESPN_DATA || {}).gstate || {})[dt]) || {})[t];",
            "  const x = ((window.__LIVESC || {})[dt] || {})[t] || ((((window.ESPN_DATA || {}).gstate || {})[dt]) || {})[t];\n"
            "  const lv152 = ((window.__LIVESC || {})[dt] || {})[t]; /* gx152: wait for puck drop */\n"
            "  if (lv152 && (lv152.s === \"P\" || (lv152.s === \"L\" && !lv152.f && !lv152.my && !lv152.op && lv152.per === \"1st\" && !lv152.int))) return { s: \"P\", f: 0 };",
            "gx152: wait for puck drop")
    # live pulls: every 10 s, right away when the page comes back, never stuck busy
    t = lit(t, "152: pull timer",
            "    const id = setInterval(() => { if (document.hidden) return; if (window.__LIVEANY120 || Date.now() - (window.__LP120 || 0) > 59000) pull(); }, 15 * 1000); /* gx120 */\n    return () => { dead = true; clearInterval(id); };",
            "    const id = setInterval(() => { if (document.hidden) return; if (window.__LIVEANY120 || Date.now() - (window.__LP120 || 0) > 59000) pull(); }, 10 * 1000); /* gx120 */\n"
            "    const vis152 = () => { if (!document.hidden) { G120.busy = false; pull(); } }; /* gx152 */\n"
            "    document.addEventListener(\"visibilitychange\", vis152); window.addEventListener(\"focus\", vis152);\n"
            "    return () => { dead = true; clearInterval(id); document.removeEventListener(\"visibilitychange\", vis152); window.removeEventListener(\"focus\", vis152); };",
            "const vis152 = () =>")
    t = lit(t, "152: busy timeout",
            "if (G120.busy || !js || !js.games) return;",
            "if ((G120.busy && Date.now() - (G120.bt || 0) < 20000) || !js || !js.games) return; /* gx152 */",
            "Date.now() - (G120.bt || 0) < 20000")
    t = lit(t, "152: busy time", "  G120.busy = true;\n", "  G120.busy = true; G120.bt = Date.now();\n", "G120.bt = Date.now();")
    # faces: a missing photo keeps the same size box (team logo inside)
    t = lit(t, "152: face box",
            "if (!eid || bad) return <TeamLogo t={tm} size={size} />;",
            'if (!eid || bad) return <span className="gx-face gx-fb152" style={{ width: "calc(" + z + "px * var(--gx-fs, 1))", height: "calc(" + z + "px * var(--gx-fs, 1))" }}><TeamLogo t={tm} size={Math.round(z * 0.8)} /></span>;',
            "gx-face gx-fb152")
    # GP before FPTS in every stat table
    t = lit(t, "152: GP first values",
            'v = mode === "mx" && p.p === "G" ? [v0[0], v0[1], "-", "-", "-", "-", "-", "-", "-", "-", v0[10]] : v0, out = mode === "cm" ? v.slice(0, 1) : v;',
            'v1 = mode === "mx" && p.p === "G" ? [v0[0], v0[1], "-", "-", "-", "-", "-", "-", "-", "-", v0[10]] : v0, v = [v1[1], v1[0], ...v1.slice(2)] /* gx152 */, out = mode === "cm" ? v1.slice(0, 1) : v;',
            "v = [v1[1], v1[0], ...v1.slice(2)] /* gx152 */")
    t = lit(t, "152: GP first headings",
            '  const H = mode === "go" ? GX_GO106 : mode === "cm" ? GX_CM106 : GX_SK106;',
            '  const H0 = mode === "go" ? GX_GO106 : mode === "cm" ? GX_CM106 : GX_SK106, H = H0.length > 1 ? [H0[1], H0[0], ...H0.slice(2)] : H0; /* gx152 */',
            "H = H0.length > 1 ? [H0[1], H0[0], ...H0.slice(2)] : H0; /* gx152 */")
    t = lit(t, "152: one colour",
            'className={"n " + (i === 0 ? "font-semibold" : "text-slate-500")}',
            'className={"n text-slate-500" /* gx152 */}',
            '"n text-slate-500" /* gx152 */')
    # sorting: Avg and Expected sort by exactly what is shown
    t = lit(t, "152: sort override",
            "function gxSort108(list, s, get) {",
            "function gxSort108(list, s, get, ov152) {",
            "function gxSort108(list, s, get, ov152) {")
    t = lit(t, "152: sort values",
            'if (k === "Exp" || k === "Rank") return gxPgAvg(p, K);',
            'if (ov152 && ov152[k]) return ov152[k](p); /* gx152 */\n    if (k === "Exp") return effAvg(p, K);\n    if (k === "Rank") return gxPgAvg(p, K);',
            "if (ov152 && ov152[k]) return ov152[k](p); /* gx152 */")
    t = lit(t, "152: rankings headings",
            '{HB("gp", "GP", "m-hide")}{HB("sf", "Avg")}{HB("exp", "Expected")}',
            '<span className="n m-hide">GP</span><GxHB108 k="Avg" /><GxHB108 k="Exp" l="Expected" />{/* gx152 */}',
            '<GxHB108 k="Avg" /><GxHB108 k="Exp" l="Expected" />{/* gx152 */}')
    t = lit(t, "152: rankings sort",
            "const shown = gxSort108(rows, s, (x) => x.p).slice(0, n);",
            "const shown = gxSort108(rows, s, (x) => x.p, { Avg: (p) => (p.gp ? p.tot / p.gp : -Infinity), Exp: pv }).slice(0, n); /* gx152 */",
            "Exp: pv }).slice(0, n); /* gx152 */")
    return t

edit(APP, change)


# the sync saves ESPN's own player order for each team and day (the browser loses it when reading numbers as keys)
def sync(t):
    return lit(t, "152: ESPN order in sync",
               '    data["daily"] = daily\n',
               '    data["daily"] = daily\n    data["dorder"] = {d_: {t_: list(v_.keys()) for t_, v_ in dy_.items()} for d_, dy_ in daily.items()}  # change 152\n',
               "change 152")

edit("espn_sync.py", sync)
