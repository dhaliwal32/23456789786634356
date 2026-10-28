# changes/106-drag-stats-clean.py - week chart and matchup days follow your finger; matchups only change from the top strip; FPTS right after the name on rosters, pickups and all players (with every roster stat and the stats picker); end Avg gone; goalie start share (games started so far) beside his average; home page chart without the extra boxes and "behind by" lines; less writing on Pickups

NEW_CSS = r'''  /* change 106 (install.py) */
  .gx-dr106 { touch-action: pan-y; will-change: transform; }
  /* rosters: FPTS right after the name, no Avg at the end */
  .gx-sc99 .gx-ro > * { order: 2; }
  .gx-sc99 .gx-ro > :nth-child(1), .gx-sc99 .gx-ro > :nth-child(2) { order: 0; }
  .gx-sc99 .gx-ro > :nth-child(12) { order: 1; font-weight: 600; color: var(--ink) !important; }
  .gx-sc99 .gx-ro > :nth-child(23) { display: none !important; }
  .gx-sc99 .gx-ro { grid-template-columns: 44px 200px 62px 108px 50px 62px 42px 56px 78px 66px 64px 40px 40px 40px 42px 46px 46px 46px 48px 44px 56px; }
  .gx-gs106 { font-size: 11px; color: var(--mute); margin-left: 4px; font-weight: 400; }
  /* pickups: FPTS after the name, every stat */
  .gx-sc99 .gx-pk > * { order: 2; }
  .gx-sc99 .gx-pk > :nth-child(1), .gx-sc99 .gx-pk > :nth-child(2) { order: 0; }
  .gx-sc99 .gx-pk > :nth-child(10) { order: 1; font-weight: 600; color: var(--ink) !important; }
  .gx-sc99 .gx-pk.full { grid-template-columns: 44px 260px 62px 64px 56px 70px 66px 58px 62px 56px 40px 40px 40px 42px 46px 46px 46px 48px 44px 56px; }
  .gx-sc99 .gx-pk.cm { grid-template-columns: 44px 260px 62px 64px 56px 70px 66px 58px 62px 56px; }
  /* all players: FPTS after the name, every stat */
  .gx-sc99.gx-rk106 > .gx-rk { width: max-content; min-width: 100%; column-gap: 0; grid-template-columns: 38px 44px 200px 62px 170px 40px 64px 70px 40px 40px 40px 42px 46px 46px 46px 48px 44px 56px; }
  .gx-sc99.gx-rk106 > .gx-rk > * { order: 2; padding-left: 8px; }
  .gx-sc99.gx-rk106 > .gx-rk > :nth-child(-n+3) { order: 0; position: sticky; z-index: 2; background: var(--card); align-self: stretch; display: flex; flex-direction: column; justify-content: center; }
  .gx-sc99.gx-rk106 > .gx-rk > :nth-child(1) { left: 0; }
  .gx-sc99.gx-rk106 > .gx-rk > :nth-child(2) { left: 38px; }
  .gx-sc99.gx-rk106 > .gx-rk > :nth-child(3) { left: 82px; box-shadow: 8px 0 8px -8px rgba(0,0,0,.45); }
  .gx-sc99.gx-rk106 > .gx-rk > :nth-child(8) { order: 1; font-weight: 600; }
  .gx-sc99.gx-rk106 > .gx-rk.me > * { background: var(--card3, var(--card)); }
  @media (max-width: 640px) {
    .gx-sc99 .gx-ro { grid-template-columns: 36px 142px 56px 88px 46px 58px 40px 54px 70px 60px 56px 34px 34px 34px 36px 40px 40px 42px 44px 40px 52px; }
    .gx-sc99 .gx-pk.full { grid-template-columns: 36px 160px 56px 62px 52px 64px 60px 52px 58px 52px 34px 34px 34px 36px 40px 40px 42px 44px 40px 52px; }
    .gx-sc99 .gx-pk.cm { grid-template-columns: 36px 160px 56px 62px 52px 64px 60px 52px 58px 52px; }
    .gx-sc99.gx-rk106 > .gx-rk { grid-template-columns: 30px 36px 142px 56px 50px 56px 34px 34px 34px 36px 40px 40px 42px 44px 40px 52px; }
    .gx-sc99.gx-rk106 > .gx-rk > :nth-child(2) { left: 30px; }
    .gx-sc99.gx-rk106 > .gx-rk > :nth-child(3) { left: 66px; }
  }
</style>'''

HELPERS = r'''// ---------- change 106: drag to swipe, stats everywhere, goalie start share (install.py) ----------
// follow the finger; past about a quarter of the width it moves on, otherwise it springs back
function useDrag106(prev, next) {
  const ref = React.useRef(null), st = React.useRef(null);
  const set = (el, tr, x, op) => { el.style.transition = tr; el.style.transform = x; el.style.opacity = op; };
  const h = {
    onTouchStart: (e) => { const t = e.touches[0]; st.current = { x: t.clientX, y: t.clientY, dx: 0, lock: null }; },
    onTouchMove: (e) => {
      const s = st.current, el = ref.current;
      if (!s || !el) return;
      const t = e.touches[0], dx = t.clientX - s.x, dy = t.clientY - s.y;
      if (s.lock == null) { if (Math.abs(dx) < 8 && Math.abs(dy) < 8) return; s.lock = Math.abs(dx) > Math.abs(dy) ? "x" : "y"; }
      if (s.lock !== "x") return;
      const can = dx < 0 ? !!next : !!prev;
      s.dx = can ? dx : dx / 4;
      set(el, "none", "translateX(" + s.dx + "px)", String(1 - Math.min(0.5, Math.abs(s.dx) / 700)));
    },
    onTouchEnd: () => {
      const s = st.current, el = ref.current;
      st.current = null;
      if (!s || !el || s.lock !== "x") return;
      const w = el.offsetWidth || 320, fn = Math.abs(s.dx) > w * 0.22 ? (s.dx < 0 ? next : prev) : null;
      if (fn) {
        set(el, "transform .15s ease-in, opacity .15s", "translateX(" + (s.dx < 0 ? -w : w) * 0.6 + "px)", "0");
        setTimeout(() => { set(el, "none", "", ""); fn(); }, 140);
      } else set(el, "transform .22s cubic-bezier(.2,.8,.2,1), opacity .22s", "", "");
    },
  };
  h.onTouchCancel = h.onTouchEnd;
  return [ref, h];
}
// how often a goalie has started: games played out of his team's games so far
function gxGS106(p) {
  const S = SCHED[p.t], td = todayISO();
  if (!S || p.p !== "G") return null;
  let tg = 0;
  S.forEach((d) => { if (d < td || (d === td && gState(p.t, d).s === "F")) tg += 1; });
  if (!tg) return null;
  const n = Math.min(p.gp || 0, tg);
  return { n, tg, pct: Math.round((n / tg) * 100) + "%" };
}
const gxGsTxt106 = (p) => { const g = gxGS106(p); return g ? "started " + g.n + " of " + g.tg : ""; };
// stat values in display order: FPTS first, no average at the end
const GX_SK106 = ["FPTS", "GP", "G", "A", "PTS", "+/-", "PIM", "SOG", "HIT", "BLK", "TOI"];
const GX_GO106 = ["FPTS", "GP", "W", "L", "OTL", "GA", "SV", "SV%", "GAA", "SO", "TOI"];
const GX_CM106 = ["FPTS"];
function gxVals106(p, s, rng) {
  const eid = String(p.id || "").replace(/^e/, ""), isG = p.p === "G";
  let v;
  if (gxProjR100(rng)) { const pr = gxProj100(p, s, rng); v = [pr[0], "-", "-", "-", "-", "-", "-", "-", "-", "-", pr[13], pr[14]]; }
  else { const D = GX100.data[rng]; v = D ? gxAgg104(D[eid], isG, s.sc || {}) : GX_SK104.map(() => "..."); }
  return [v[10], ...v.slice(0, 10)];
}
function GxSC106({ p, s, mode }) {
  const rng = gxUse100();
  useEffect(() => { gxLoad100(rng); });
  const v = gxVals106(p, s, rng), out = mode === "cm" ? v.slice(0, 1) : v;
  return out.map((c, i) => <div key={"c106" + i} className={"n " + (i === 0 ? "font-semibold" : "text-slate-500")}>{c}</div>);
}
function GxSH106({ mode }) {
  const rng = gxUse100();
  const H = mode === "go" ? GX_GO106 : mode === "cm" ? GX_CM106 : GX_SK106;
  return H.map((h, i) => <span key={h + i} className="n">{gxProjR100(rng) && h === "GP" ? "Gms" : h}</span>);
}
const gxPkMode106 = (pos) => (pos === "G" ? "full go" : pos === "F" || pos === "D" ? "full sk" : "cm");
'''


def change(t):
    t = lit(t, "106: styles", "</style>", NEW_CSS, "change 106 (install.py)")
    t = lit(t, "106: helpers", ROOT, HELPERS + ROOT, "change 106: drag to swipe")

    # --- week chart follows the finger
    t = lit(t, "106: chart drag hook", "  const sl105 = useSlide105(i);",
            "  const sl105 = useSlide105(i);\n  const [dr106, dh106] = useDrag106(i > 0 ? () => go(i - 1) : null, i < s.weeks.length - 1 ? () => go(i + 1) : null);",
            "const [dr106, dh106] = useDrag106(")
    t = lit(t, "106: chart no release-only swipe", '  const wrapP = { className: "gx-pn", ref: box, style: { minWidth: 0, touchAction: "pan-y" }, ...gxSwipe61(touch, i, go) };',
            '  const wrapP = { className: "gx-pn", ref: box, style: { minWidth: 0, touchAction: "pan-y" } };', 'style: { minWidth: 0, touchAction: "pan-y" } };')
    t = lit(t, "106: chart drags", 'key={"w105-" + i} viewBox=', 'key={"w105-" + i} ref={dr106} {...dh106} viewBox=', "ref={dr106} {...dh106} viewBox=")
    t = lit(t, "106: chart drag class", 'className={"gx-svg gx-sl105 " + sl105}', 'className={"gx-svg gx-dr106 gx-sl105 " + sl105}', '"gx-svg gx-dr106 gx-sl105 "')
    # home page: no extra boxes or "behind by" lines
    t = lit(t, "106: chart sub line hidden", '<div className="text-xs text-slate-500" style={{ marginTop: 4 }}>\n        {(done >= n ? "Final " : "Projected ")',
            '<div className="text-xs text-slate-500" style={{ display: "none" }}>\n        {(done >= n ? "Final " : "Projected ")', 'style={{ display: "none" }}>\n        {(done >= n')
    t = lit(t, "106: chart boxes hidden", '<div className="gx-rf">{facts}</div>\n      <div className="gx-rt">',
            '<div className="gx-rf" style={{ display: "none" }}>{facts}</div>\n      <div className="gx-rt" style={{ display: "none" }}>', '<div className="gx-rf" style={{ display: "none" }}>')
    t = lit(t, "106: no behind by on top", '<span style={{ margin: "0 auto", color: ahead ? "var(--good)" : "var(--bad)" }}>{(ahead ? "Ahead by " : "Behind by ") + f1(Math.abs(margin))}</span>',
            '<span style={{ margin: "0 auto" }}></span>', None)

    # --- matchup: no swipe between matchups; days follow the finger
    t = lit(t, "106: no matchup swipe", '      <div onTouchStart={onStart} onTouchEnd={onEnd} style={{ touchAction: "pan-y" }}>', "      <div>", None)
    t = lit(t, "106: day drag hook", "  const sl105a = useSlide105(sel), sl105b = useSlide105(sel * 100 + d);",
            "  const sl105a = useSlide105(sel), sl105b = useSlide105(sel * 100 + d);\n  const [dr106, dh106] = useDrag106(d > 0 ? () => setDay(d - 1) : null, d < n - 1 ? () => setDay(d + 1) : null);",
            "const [dr106, dh106] = useDrag106(d > 0")
    t = lit(t, "106: day panel drags", 'key={"d105-" + sel + "-" + d} className={"gx-pn gx-sl105 " + sl105b}',
            'key={"d105-" + sel + "-" + d} ref={dr106} {...dh106} className={"gx-pn gx-dr106 gx-sl105 " + sl105b}', "ref={dr106} {...dh106} className={\"gx-pn gx-dr106")
    t = lit(t, "106: old page-wide day swipe off", '    ok = !(e.target.closest && e.target.closest(".gx-ms, .navscroll, .overflow-x-auto, .gx-so, .gx-bb, input, select"));',
            '    ok = false; /* gx106: swipes are handled where they happen */', "gx106: swipes are handled where they happen")

    t = sub_once(t, "106: roster cells", re.escape("<GxSC104 p={p} s={s} />"), '<GxSC106 p={p} s={s} mode="full" />', '<GxSC106 p={p} s={s} mode="full" />', 0, 2)
    t = sub_once(t, "106: roster headings", re.escape("<GxSH104 />"), '<GxSH106 mode="sk" />', '<GxSH106 mode="sk" />', 0, 2)
    t = lit(t, "106: goalie headings", "<GxSH104 g />", '<GxSH106 mode="go" />', '<GxSH106 mode="go" />')
    # --- rosters: goalie start share
    if "gxGsTxt106(p)" not in t:
        old = 'if (p.p === "G") return Math.round(p.prob * 100) + "% of starts";'
        if t.count(old) != 2:
            fail("106: goalie role line: expected 2")
        t = t.replace(old, 'if (p.p === "G") return gxGsTxt106(p);')
        old = '{sea == null ? "\\u2013" : f1(sea)}'
        if t.count(old) != 2:
            fail("106: roster Avg cells: expected 2")
        t = t.replace(old, '{sea == null ? "\\u2013" : f1(sea)}{p.p === "G" && gxGS106(p) ? <span className="gx-gs106">{gxGS106(p).pct}</span> : null}')
        print("(install) 106: goalie start share on rosters: updated")

    # --- player screen: start share beside the name line, no 50% start column
    t = lit(t, "106: phone header start share", '<span>{p.t + " · " + posWord + (no != null ? " · #" + no : "")}</span>',
            '<span>{p.t + " · " + posWord + (no != null ? " · #" + no : "") + (gxGS106(p) ? " · starts " + gxGS106(p).pct : "")}</span>', '" · starts " + gxGS106(p).pct')
    t = lit(t, "106: laptop header start share", '<div className="gx-pd-tm truncate">{tName}</div>',
            '<div className="gx-pd-tm truncate">{tName}{gxGS106(p) ? " \\u00b7 " + gxGsTxt106(p) + " (" + gxGS106(p).pct + ")" : ""}</div>', '{tName}{gxGS106(p) ?')
    t = lit(t, "106: no start column heading", '<th>{isG ? "Start" : ""}</th>', "", None)
    t = lit(t, "106: no start column cells", '<td className="text-slate-500">{isG && r && r.g ? Math.round(r.g.v * 100) + "%" : ""}</td>', "", None)
    t = lit(t, "106: per game note", '{isG ? "if he starts" : "ESPN " + f1(p.avg || 0)}', '{isG ? (gxGS106(p) ? "starts " + gxGS106(p).pct : "") : "ESPN " + f1(p.avg || 0)}', '"starts " + gxGS106(p).pct : "")')

    # --- pickups: less writing, every stat, FPTS after the name
    t = lit(t, "106: pickups top line",
            '{ml === 0 ? "No moves left this week." : ml == null ? "" : ml + " move" + (ml === 1 ? "" : "s") + " left this week."}',
            '{ml === 0 ? "No moves left" : ml == null ? "" : ml + " move" + (ml === 1 ? "" : "s") + " left"}', '"No moves left" : ml == null')
    t = lit(t, "106: pickups next week line",
            '{plan ? <span className="text-slate-500"> Showing {pw.label || "next week"}.{d0 ? " Moves reset " + dayLabel(d0) + "." : ""}</span> : null}',
            '{plan ? <span className="text-slate-500">{" \\u00b7 showing next week"}</span> : null}', '" \\u00b7 showing next week"')
    t = lit(t, "106: pickups no text under the player",
            '<div className="text-xs text-slate-500 truncate">{"for " + r.d.n + (keep ? "" : H === 1 ? " \\u00b7 this week" : " \\u00b7 short-term") + (tg ? " \\u00b7 " + tg.t : "") /* gx104-row */}{gxScratch(r.f) ? <span style={{ color: "var(--warn)" }}>{" \\u00b7 not in lineup"}</span> : null}</div>',
            "{/* gx106: no text under the player */}", "gx106: no text under the player")
    t = lit(t, "106: pickups stats picker", '<b></b><div className="gx-sc99">\n        <div className="gx-pk', '<b></b><GxRngSel100 /><div className="gx-sc99">\n        <div className="gx-pk', '<b></b><GxRngSel100 /><div className="gx-sc99">\n        <div className="gx-pk')
    t = lit(t, "106: pickups heading mode", '<div className="gx-pk text-xs text-slate-500" style={{ borderTop: 0, paddingTop: 0 }}>',
            '<div className={"gx-pk text-xs text-slate-500 " + gxPkMode106(pos)} style={{ borderTop: 0, paddingTop: 0 }}>', '"gx-pk text-xs text-slate-500 " + gxPkMode106(pos)')
    t = lit(t, "106: pickups row mode", 'className="gx-pk row"', 'className={"gx-pk row " + gxPkMode106(pos)}', '"gx-pk row " + gxPkMode106(pos)')
    t = lit(t, "106: pickups stat headings", '<span className="n">So far</span><span className="n">Rost</span>',
            '<span className="n">Avg</span><span className="n">Rost</span><GxSH106 mode={pos === "G" ? "go" : pos === "all" ? "cm" : "sk"} />', '<GxSH106 mode={pos === "G"')
    t = lit(t, "106: pickups stat cells", '{r.f.own != null ? Math.round(r.f.own) + "%" : "-"}</div>',
            '{r.f.own != null ? Math.round(r.f.own) + "%" : "-"}</div>\n              <GxSC106 p={r.f} s={s} mode={pos === "all" ? "cm" : "full"} />', '<GxSC106 p={r.f} s={s} mode={pos === "all"')

    # --- all players: every stat, FPTS after the name
    t = lit(t, "106: all players scroll box", '<div className="gx-rk gx-rkh">', '<GxRngSel100 /><div className="gx-sc99 gx-rk106">\n        <div className="gx-rk gx-rkh">', '<div className="gx-sc99 gx-rk106">')
    t = lit(t, "106: all players headings", '{HB("sf", "So far")}{HB("exp", "Expected")}', '{HB("sf", "Avg")}{HB("exp", "Expected")}<GxSH106 mode={pos === "G" ? "go" : "sk"} />', '<GxSH106 mode={pos === "G" ? "go" : "sk"} />')
    t = lit(t, "106: all players cells", '<span className="n font-semibold">{f1(e)}</span>', '<span className="n font-semibold">{f1(e)}</span><GxSC106 p={p} s={s} mode="full" />', '{f1(e)}</span><GxSC106')
    t = lit(t, "106: all players scroll box end",
            '{rows.length > shown.length ? <button type="button" className="text-sm text-blue-600" style={{ marginTop: 10 }} onClick={() => setN(n + 50)}>',
            '</div>{rows.length > shown.length ? <button type="button" className="text-sm text-blue-600" style={{ marginTop: 10 }} onClick={() => setN(n + 50)}>', '</div>{rows.length > shown.length ? <button')
    t = lit(t, "106: rank heading", "<span>Rank</span><span></span><span>Player</span>", "<span>#</span><span></span><span>Player</span>", "<span>#</span><span></span><span>Player</span>")
    return t


edit(APP, change)
