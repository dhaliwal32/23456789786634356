# changes/105-cleanup-slide.py - swipes slide (week chart, matchups, matchup days, goalie days); roster drops Last 5, So far becomes Avg, goalies show start % instead of Avg; game log shows dashes for games he missed; Players: Free agents | All players; Matchup drops Games this matchup, Around the league and Who's carrying you; injuries rows lose the links and news text; less extra writing; lineup games in the week chart (two styles to choose from)

NEW_CSS = r'''  /* change 105 (install.py) */
  @keyframes gx105-r { from { opacity: .2; transform: translateX(44px); } to { opacity: 1; transform: none; } }
  @keyframes gx105-l { from { opacity: .2; transform: translateX(-44px); } to { opacity: 1; transform: none; } }
  .gx-sl105.r { animation: gx105-r .28s cubic-bezier(.2,.8,.2,1); }
  .gx-sl105.l { animation: gx105-l .28s cubic-bezier(.2,.8,.2,1); }
  .gx-sc99 .gx-ro > :nth-child(5) { display: none !important; }
  .gx-sc99 .gx-ro { grid-template-columns: 44px 200px 108px 50px 62px 42px 56px 60px 66px 64px 40px 40px 40px 42px 46px 46px 46px 48px 44px 56px 62px 52px; }
  .gx-fa105 { margin-bottom: 4px; }
  @media (max-width: 640px) {
    .gx-sc99 .gx-ro { grid-template-columns: 36px 142px 88px 46px 58px 40px 54px 50px 60px 56px 34px 34px 34px 36px 40px 40px 42px 44px 40px 52px 56px 46px; }
  }
  @media (prefers-reduced-motion: reduce) { .gx-sl105.r, .gx-sl105.l { animation: none; } }
</style>'''

HELPERS = r'''// ---------- change 105: slide on swipe, all players, chart games (install.py) ----------
// returns "r" or "l" when the key moves forward or back, so the new content slides in from that side
function useSlide105(k) {
  const r = React.useRef({ k, c: "" });
  if (r.current.k !== k) r.current = { k, c: k > r.current.k ? "r" : "l" };
  return r.current.c;
}
// lineup games in the week chart: "text" (under each day) or "bars" (behind each day)
const gxGopt105 = () => { const v = uiGet().gxGopt105; return v === "bars" ? "bars" : "text"; };
const GX_DNP105 = { dec: "-", sv: "-", ga: "-", svp: null, toi: "-", g: "-", a: "-", pm: "-", pim: "-", sog: "-" };
function GxFaToggle105({ cur, go }) {
  return (
    <div className="gx-seg gx-fa105">
      <button type="button" className={cur !== "allp" ? "on" : ""} onClick={() => go("moves", "adddrop")}>Free agents</button>
      <button type="button" className={cur === "allp" ? "on" : ""} onClick={() => go("moves", "allp")}>All players</button>
    </div>
  );
}
'''


def change(t):
    t = lit(t, "105: styles", "</style>", NEW_CSS, "change 105 (install.py)")
    t = lit(t, "105: helpers", ROOT, HELPERS + ROOT, "change 105: slide on swipe")

    # --- week chart: slide when the week changes, and lineup games per day
    t = lit(t, "105: chart slide key",
            "  const act = (id) => +((w.act || {})[id]) || 0;\n  const sa = up ? 0 : act(s.me), sb = up || !opp ? 0 : act(opp);",
            "  const sl105 = useSlide105(i);\n  const act = (id) => +((w.act || {})[id]) || 0;\n  const sa = up ? 0 : act(s.me), sb = up || !opp ? 0 : act(opp);",
            "const sl105 = useSlide105(i);")
    t = lit(t, "105: chart slides", '<svg viewBox={"0 0 " + W + " " + Hh} width="100%" className="gx-svg" style={{ display: "block", marginTop: 8 }}',
            '<svg key={"w105-" + i} viewBox={"0 0 " + W + " " + Hh} width="100%" className={"gx-svg gx-sl105 " + sl105} style={{ display: "block", marginTop: 8 }}',
            'key={"w105-" + i} viewBox=')
    t = lit(t, "105: chart taller for games", "const base = 172, yy = (v) => base - (v / topV) * 158, Hh = narrow ? 230 : 214;",
            'const base = 172, yy = (v) => base - (v / topV) * 158, Hh = (narrow ? 230 : 214) + (gxGopt105() === "text" ? 18 : 0);',
            '(gxGopt105() === "text" ? 18 : 0)')
    t = lit(t, "105: games bars", "        {segs}\n",
            '        {segs}\n        {gxGopt105() === "bars" ? dates.map((_, d) => { const ga = gms(X, d), gb = gms(Y, d); return <g key={"gb" + d}><rect x={cx(d) - 9} y={base - ga * 4} width={7} height={ga * 4} rx={1.5} style={{ fill: "var(--accent)", opacity: 0.3 }} /><rect x={cx(d) + 2} y={base - gb * 4} width={7} height={gb * 4} rx={1.5} style={{ fill: "var(--mute)", opacity: 0.3 }} /></g>; }) : null}\n',
            '{gxGopt105() === "bars" ? dates.map((_, d)')
    t = lit(t, "105: games text",
            '              <rect x={cx(d) - cw / 2} y={0} width={cw} height={Hh} style={{ fill: "transparent", cursor: "pointer" }} onClick={() => setSel(d)} />',
            '              {gxGopt105() === "text" ? <text x={cx(d)} y={Hh - 4} textAnchor="middle" style={{ fontSize: fs - 1, fill: "var(--mute)" }}>{gms(X, d) + "\\u2013" + gms(Y, d)}</text> : null}\n'
            '              <rect x={cx(d) - cw / 2} y={0} width={cw} height={Hh} style={{ fill: "transparent", cursor: "pointer" }} onClick={() => setSel(d)} />',
            '+ gms(Y, d)}</text> : null}')

    # --- matchup: slide when the matchup or the day changes
    t = lit(t, "105: matchup slide keys", "  const d = Math.max(0, Math.min(n - 1, day != null ? day : first >= 0 ? first : n - 1));",
            "  const d = Math.max(0, Math.min(n - 1, day != null ? day : first >= 0 ? first : n - 1));\n  const sl105a = useSlide105(sel), sl105b = useSlide105(sel * 100 + d);",
            "const sl105a = useSlide105(sel)")
    t = lit(t, "105: matchup score slides",
            '      <div onTouchStart={onStart} onTouchEnd={onEnd} style={{ touchAction: "pan-y" }}>\n        <div style={{ display: "flex", alignItems: "center", gap: 8 }}>',
            '      <div onTouchStart={onStart} onTouchEnd={onEnd} style={{ touchAction: "pan-y" }}>\n        <div key={"m105-" + sel} className={"gx-sl105 " + sl105a} style={{ display: "flex", alignItems: "center", gap: 8 }}>',
            'key={"m105-" + sel}')
    t = lit(t, "105: matchup day slides",
            '      <div className="gx-pn" style={{ marginTop: 12 }}><b></b><b></b><b></b><b></b>\n        <div style={{ display: "flex", alignItems: "baseline", marginBottom: 6 }}>',
            '      <div key={"d105-" + sel + "-" + d} className={"gx-pn gx-sl105 " + sl105b} style={{ marginTop: 12 }}><b></b><b></b><b></b><b></b>\n        <div style={{ display: "flex", alignItems: "baseline", marginBottom: 6 }}>',
            'key={"d105-" + sel + "-" + d}')
    # --- goalie days slide
    t = lit(t, "105: goalie day slides", '      <div className="gx-pn" data-r65="goalies">', '      <GxGoSl105 day={day}><div className="gx-pn" data-r65="goalies">', '<GxGoSl105 day={day}>')
    t = lit(t, "105: goalie day slides end",
            '"No NHL games this day."}</div>}\n      </div>\n',
            '"No NHL games this day."}</div>}\n      </div></GxGoSl105>\n',
            "</div></GxGoSl105>")

    # --- matchup: the three boxes go
    t = lit(t, "105: matchup boxes removed", "<GxMuMore103 s={s} wk={wk} />", "{/* gx105: games, league and carrying boxes removed */}", "gx105: games, league and carrying boxes removed")

    # --- roster: So far becomes Avg (no ESPN gap), goalies show start % at the end
    for k in range(2):
        pass
    if '{HB("sea", "Avg", "m-hide")}' not in t:
        if t.count('{HB("sea", "So far", "m-hide")}') != 2:
            fail("105: So far heading: expected 2 places")
        t = t.replace('{HB("sea", "So far", "m-hide")}', '{HB("sea", "Avg", "m-hide")}')
        gap = '{sea == null ? "\\u2013" : <>{f1(sea)}{gap != null ? <span className="text-xs" style={{ marginLeft: 6, color: gap >= 0 ? "var(--good)" : "var(--bad)" }}>{(gap >= 0 ? "+" : "") + f1(gap)}</span> : null}</>}'
        if t.count(gap) != 2:
            fail("105: So far cells: expected 2 places")
        t = t.replace(gap, '{sea == null ? "\\u2013" : f1(sea)}')
        print("(install) 105: So far is now Avg: updated (2)")
    else:
        print("(install) 105: So far is now Avg: already done")
    t = lit(t, "105: goalie start % heading", 'const GX_GO104 = ["GP", "W", "L", "OTL", "GA", "SV", "SV%", "GAA", "SO", "TOI", "FPTS", "Avg"];',
            'const GX_GO104 = ["GP", "W", "L", "OTL", "GA", "SV", "SV%", "GAA", "SO", "TOI", "FPTS", "GS%"];', '"FPTS", "GS%"];')
    t = lit(t, "105: goalie start % cells", '  return v.map((c, i) => <div key={"c104" + i}',
            '  if (isG) v = [...v.slice(0, 11), p.prob != null ? Math.round(p.prob * 100) + "%" : "-"];\n  return v.map((c, i) => <div key={"c104" + i}',
            'Math.round(p.prob * 100) + "%" : "-"];')

    # --- game log: dashes for games he missed
    t = lit(t, "105: game log keeps missed games", "      setLog(list.filter((r) => r.x).map((r) => {",
            '      setLog(list.filter((r) => r.x || !(r.d === today && gState(p.t, r.d).s === "P")).map((r) => {\n        if (!r.x) { const tm = r.day ? Object.values(r.day).find((v) => v && v.t === p.t) : null; return { ...r, x: tm ? { ...GX_DNP105, o: tm.o, h: tm.h } : GX_DNP105, dnp: true, fp: null, est: false, st: "F" }; }',
            "x: GX_DNP105, dnp: true")
    t = lit(t, "105: keep the box day for missed games",
            "return has.has(d) ? gxBoxDay(d).then((day) => ({ d, x: (day && day[eid]) || live })) :",
            "return has.has(d) ? gxBoxDay(d).then((day) => ({ d, x: (day && day[eid]) || live, day })) :",
            "x: (day && day[eid]) || live, day }))")
    t = lit(t, "105: stats skip missed games", "const done = rows;", "const done = rows.filter((r) => !r.dnp);", "rows.filter((r) => !r.dnp)")
    t = lit(t, "105: missed game points (1)", '<td className="b">{f1(r.fp)}{r.est ? "*" : ""}</td>', '<td className="b">{r.dnp ? "-" : f1(r.fp)}{r.est ? "*" : ""}</td>', '{r.dnp ? "-" : f1(r.fp)}{r.est')
    t = lit(t, "105: missed game points (2)", '<td className="b">{f1(r.fp)}</td>', '<td className="b">{r.dnp ? "-" : f1(r.fp)}</td>', '<td className="b">{r.dnp ? "-" : f1(r.fp)}</td>')

    # --- Players: Free agents | All players
    t = lit(t, "105: all players page", 'else if (tab === "moves") content = sub === "planner"',
            'else if (tab === "moves") content = sub === "allp" ? <div className="space-y-3"><GxFaToggle105 cur="allp" go={go} /><GxRankings {...P} /></div> : sub === "planner"',
            'sub === "allp" ? <div className="space-y-3"><GxFaToggle105')
    t = lit(t, "105: free agents toggle", '<div className="space-y-3">\n      <div className="text-sm">\n        <span className="font-semibold">{ml === 0 ?',
            '<div className="space-y-3">\n      <GxFaToggle105 cur="adddrop" go={(t, k) => { window.location.hash = gxHash(t, k); }} />\n      <div className="text-sm">\n        <span className="font-semibold">{ml === 0 ?',
            '<GxFaToggle105 cur="adddrop"')

    # --- injuries: no links, no news text, shorter lines
    t = lit(t, "105: injuries no news text",
            '{note && (upd || openN[nk]) ? <div className={"text-xs text-slate-500 nt" + (openN[nk] ? " open" : "")} role="button" onClick={() => setOpenN((x) => ({ ...x, [nk]: !x[nk] }))}>{note}</div> : null}',
            '{/* gx105: news text removed */}', "gx105: news text removed")
    t = lit(t, "105: injuries no links",
            '{!upd && note && !openN[nk] ? <span><button type="button" className="text-blue-600" onClick={() => setOpenN((x) => ({ ...x, [nk]: true }))}>Latest news</button>{r.p.ft === "fa" ? " \u00b7 " : ""}</span> : null}',
            '{/* gx105: links removed */}', "gx105: links removed")
    t = lit(t, "105: injuries no watch/espn",
            '{r.p.ft === "fa" ? <span><button type="button" className="text-blue-600" onClick={() => gxWatch.toggle(r.p.id)}>{gxWatch.has(r.p.id) ? "Watching" : "Watch"}</button>{" \u00b7 "}<button type="button" className="text-blue-600" onClick={() => { if (window.__QA) window.__QA.espn(r.p); }}>Add on ESPN</button></span> : null}',
            "", None)
    t = lit(t, "105: injuries shorter filter line",
            '{allP ? "Showing every injured player. " : "Showing good players only: better than your weakest at their position once healthy. "}',
            '{allP ? "Every injured player \\u00b7 " : "Good players only \\u00b7 "}', '"Good players only \\u00b7 "')

    # --- less extra writing
    t = lit(t, "105: pickups footnote",
            '{rows.length ? <div className="text-xs text-slate-500" style={{ marginTop: 10 }}>Adds is the extra points in your lineup for {hLabel}. Tap a player to try the swap or change who you drop.</div> : null}',
            "{/* gx105: footnote removed */}", "gx105: footnote removed")
    t = lit(t, "105: rankings footnote", 'style={{ paddingTop: 10, marginTop: 10, borderTop: "1px solid var(--line)" }}>\n          Rank is each',
            'style={{ display: "none" }}>\n          Rank is each', 'style={{ display: "none" }}>\n          Rank is each')
    t = lit(t, "105: weakest spots subtitle", ' right="First to drop or include in a trade"', "", None)
    t = lit(t, "105: buy low subtitle", ' sub="Good players on other teams who are cold, unlucky or underrated."', "", None)
    return t


GOALIE_SL = r'''// ---------- change 105: goalie days slide ----------
function GxGoSl105({ day, children }) {
  const c = useSlide105(day);
  return <div key={"g105-" + day} className={"gx-sl105 " + c}>{children}</div>;
}
'''


def change2(t):
    return lit(t, "105: goalie slide helper", ROOT, GOALIE_SL + ROOT, "change 105: goalie days slide")


edit(APP, change)
edit(APP, change2)
