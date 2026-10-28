# changes/108-rosters-sort-filters.py - rosters drop Today, Pts, Matchup, Left, Next wk; tap any stat heading to sort (best first, tap again worst first); Matchup shows one date with arrows instead of every day; players below their projection in red; nothing shows behind the player when sliding; Pickups filters behind one button, no Last 5, every stat for every view

NEW_CSS = r'''  /* change 108 (install.py) */
  /* rosters: face, name, FPTS, Avg, Expected, Rank, then stats */
  .gx-sc99 .gx-ro > :nth-child(3), .gx-sc99 .gx-ro > :nth-child(4), .gx-sc99 .gx-ro > :nth-child(6), .gx-sc99 .gx-ro > :nth-child(7), .gx-sc99 .gx-ro > :nth-child(8) { display: none !important; }
  .gx-sc99 .gx-ro { grid-template-columns: 44px 200px 62px 72px 70px 64px 40px 40px 40px 42px 46px 46px 46px 48px 44px 56px; }
  /* pickups: no Last 5, every stat */
  .gx-sc99 .gx-pk > :nth-child(3) { display: none !important; }
  .gx-sc99 .gx-pk.full, .gx-sc99 .gx-pk.cm { grid-template-columns: 44px 220px 62px 56px 70px 66px 58px 62px 56px 40px 40px 40px 42px 46px 46px 46px 48px 44px 56px; }
  /* nothing behind the player while sliding */
  .gx-sc99.gx-rk106 > .gx-rk > :nth-child(2) { box-shadow: 12px 0 0 var(--card); }
  .gx-sc99.gx-rk106 > .gx-rk.me > :nth-child(2) { box-shadow: 12px 0 0 var(--card3, var(--card)); }
  /* sortable stat headings */
  .gx-sh108 { color: inherit; font: inherit; white-space: nowrap; }
  .gx-sh108.on { color: var(--ink); font-weight: 700; }
  .gx-sh108 i { font-style: normal; font-size: 9px; margin-left: 2px; }
  /* matchup: one date with arrows */
  .gx-dn108 { display: flex; align-items: center; justify-content: center; gap: 14px; margin-top: 14px; }
  .gx-dn108 .dt { min-width: 150px; text-align: center; font-weight: 600; font-size: 16px; }
  .gx-dn108 .dt small { display: block; font-weight: 400; font-size: 12px; }
  /* pickups filter button */
  .gx-ft108 > button.tg { display: flex; align-items: center; gap: 8px; width: 100%; padding: 10px 12px; border: 1px solid var(--line2); border-radius: 12px; font-size: 14px; color: var(--ink); text-align: left; }
  .gx-ft108 > button.tg span { color: var(--mute); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  .gx-ft108 > button.tg b { margin-left: auto; font-weight: 400; color: var(--mute); transition: transform .2s; }
  .gx-ft108.open > button.tg b { transform: rotate(180deg); }
  .gx-ft108 .pnl { margin-top: 8px; padding: 12px; border: 1px solid var(--line); border-radius: 12px; display: flex; flex-direction: column; gap: 10px; animation: gx101-in .2s ease-out; }
  .gx-ft108 .pnl .gx-rs100 { justify-content: flex-start; margin: 0; }
  @media (max-width: 640px) {
    .gx-sc99 .gx-ro { grid-template-columns: 36px 142px 56px 62px 60px 54px 34px 34px 34px 36px 40px 40px 42px 44px 40px 52px; }
    .gx-sc99 .gx-pk.full, .gx-sc99 .gx-pk.cm { grid-template-columns: 36px 150px 56px 52px 64px 60px 52px 58px 52px 34px 34px 34px 36px 40px 40px 42px 44px 40px 52px; }
  }
</style>'''

HELPERS = r'''// ---------- change 108: tap a stat heading to sort, pickup filters (install.py) ----------
// one sort for every stat table: key = heading, dir 1 = best first, -1 = worst first
const GX108 = (window.__GX108 = window.__GX108 || { k: null, dir: 1 });
const GX_LOW108 = { GA: 1, GAA: 1, L: 1, OTL: 1 };
function gxSet108(k) {
  if (GX108.k === k) GX108.dir = -GX108.dir; else { GX108.k = k; GX108.dir = 1; }
  window.dispatchEvent(new Event("gx-sort108"));
}
const gxUseSort108 = () => { const [, t] = useState(0); useEffect(() => { const f = () => t((x) => x + 1); window.addEventListener("gx-sort108", f); return () => window.removeEventListener("gx-sort108", f); }, []); return GX108; };
const gxNum108 = (v) => {
  if (v == null) return -Infinity;
  const x = String(v);
  if (/^\d+:\d\d$/.test(x)) return gxPdSec(x);
  const n = parseFloat(x.replace("%", "").replace("+", ""));
  return isNaN(n) ? -Infinity : x.indexOf("%") > 0 && n > 1 ? n / 100 : n;
};
function gxSort108(list, s, get) {
  const k = GX108.k;
  if (!k) return list;
  const rng = gxRng100(), g = get || ((x) => x), K = s.blend;
  const val = (p) => {
    if (k === "Avg") return p.gp ? p.tot / p.gp : -Infinity;
    if (k === "Exp" || k === "Rank") return gxPgAvg(p, K);
    const H = p.p === "G" ? GX_GO106 : GX_SK106, i = H.indexOf(k);
    if (i < 0) return -Infinity;
    const v = gxNum108(gxVals106(p, s, rng)[i]);
    return GX_LOW108[k] && v !== -Infinity ? -v : v;
  };
  return [...list].map((x) => [x, val(g(x))]).sort((a, b) => (b[1] - a[1]) * GX108.dir).map((x) => x[0]);
}
function GxHB108({ k, l }) {
  const S = gxUseSort108();
  return <button type="button" className={"n gx-sh108" + (S.k === k ? " on" : "")} onClick={() => gxSet108(k)}>{l || k}{S.k === k ? <i>{S.dir > 0 ? "\u25bc" : "\u25b2"}</i> : null}</button>;
}
function GxFlt108({ label, children }) {
  const [open, setOpen] = useState(false);
  return (
    <div className={"gx-ft108" + (open ? " open" : "")}>
      <button type="button" className="tg" onClick={() => setOpen(!open)}>Filters <span>{label}</span><b>{"\u25be"}</b></button>
      {open ? <div className="pnl">{children}</div> : null}
    </div>
  );
}
const gxRngLbl108 = () => ((GX_RNG100.find((r) => r[0] === gxRng100()) || [0, "Season"])[1]).replace(" (projected)", " proj.");
'''

DAYNAV = '''<div className="gx-dn108">
        <button type="button" className="gx-arw" aria-label="Earlier day" disabled={d <= 0} onClick={() => setDay(d - 1)}>{"\\u2039"}</button>
        <div className="dt">{dates[d] === today ? "Today" : dates[d] ? dayLabel(dates[d]) : ""}<small style={{ color: Math.abs(dvOf(d)) < 0.05 ? "var(--mute)" : dvOf(d) > 0 ? "var(--good)" : "var(--bad)" }}>{(dvOf(d) > 0 ? "+" : "") + f1(dvOf(d))}</small></div>
        <button type="button" className="gx-arw" aria-label="Later day" disabled={d >= n - 1} onClick={() => setDay(d + 1)}>{"\\u203a"}</button>
      </div>
'''


def change(t):
    t = lit(t, "108: styles", "</style>", NEW_CSS, "change 108 (install.py)")
    t = lit(t, "108: helpers", ROOT, HELPERS + ROOT, "change 108: tap a stat heading to sort")

    # --- rosters: sortable headings, rows sorted
    t = sub_once(t, "108: roster headings", re.escape('{HB("mu", "Matchup")}{HB("left", "Left")}{HB("next", "Next wk", "m-hide")}{HB("sea", "Avg", "m-hide")}{HB("pg", "Expected")}{HB("rk", "Rank", "m-hide")}'),
                 '{HB("mu", "Matchup")}{HB("left", "Left")}{HB("next", "Next wk", "m-hide")}<GxHB108 k="Avg" /><GxHB108 k="Exp" l="Expected" /><GxHB108 k="Rank" />', '<GxHB108 k="Avg" /><GxHB108 k="Exp"', 0, 2)
    t = sub_once(t, "108: roster rows sorted", re.escape("{list.map(row)}"), "{gxSort108(list, s).map(row)}", "{gxSort108(list, s).map(row)}", 0, 2)
    # --- sortable stat headings everywhere
    t = lit(t, "108: stat headings sortable", '  return H.map((h, i) => <span key={h + i} className="n">{gxProjR100(rng) && h === "GP" ? "Gms" : h}</span>);',
            '  const S = gxUseSort108();\n  return H.map((h, i) => <button type="button" key={h + i} className={"n gx-sh108" + (S.k === h ? " on" : "")} onClick={() => gxSet108(h)}>{gxProjR100(rng) && h === "GP" ? "Gms" : h}{S.k === h ? <i>{S.dir > 0 ? "\\u25bc" : "\\u25b2"}</i> : null}</button>);',
            "const S = gxUseSort108();\n  return H.map")
    # --- pickups: every stat in every view, rows sorted, filters behind a button
    t = lit(t, "108: mixed list keeps skater columns", "  const v = gxVals106(p, s, rng), out = mode === \"cm\" ? v.slice(0, 1) : v;",
            '  const v0 = gxVals106(p, s, rng), v = mode === "mx" && p.p === "G" ? [v0[0], v0[1], "-", "-", "-", "-", "-", "-", "-", "-", v0[10]] : v0, out = mode === "cm" ? v.slice(0, 1) : v;',
            'mode === "mx" && p.p === "G"')
    t = lit(t, "108: pickups full columns always", 'const gxPkMode106 = (pos) => (pos === "G" ? "full go" : pos === "F" || pos === "D" ? "full sk" : "cm");',
            'const gxPkMode106 = (pos) => (pos === "G" ? "full go" : "full sk");', 'const gxPkMode106 = (pos) => (pos === "G" ? "full go" : "full sk");')
    t = lit(t, "108: pickups cells", 'mode={pos === "all" ? "cm" : "full"}', 'mode={pos === "G" ? "full" : "mx"}', 'mode={pos === "G" ? "full" : "mx"}')
    t = lit(t, "108: pickups headings", '<GxSH106 mode={pos === "G" ? "go" : pos === "all" ? "cm" : "sk"} />', '<GxSH106 mode={pos === "G" ? "go" : "sk"} />', '<GxSH106 mode={pos === "G" ? "go" : "sk"} />')
    t = lit(t, "108: pickups rows sorted", "{rows.length ? rows.map((r) => {", "{rows.length ? gxSort108(rows, s, (r) => r.f).map((r) => {", "gxSort108(rows, s, (r) => r.f)")
    t = lit(t, "108: all players rows sorted", "const shown = rows.slice(0, n);", "const shown = gxSort108(rows, s, (x) => x.p).slice(0, n);", "gxSort108(rows, s, (x) => x.p).slice(0, n)")
    i = t.find('<div className="flex flex-wrap gap-2 items-center">\n        <Pills items={[["all", "All"], ["F", "Forwards"], ["D", "Defence"], ["G", "Goalies"]]} value={pos}')
    if "<GxFlt108 label=" in t:
        print("(install) 108: pickup filters: already done")
    else:
        if i < 0:
            fail("108: pickup filters: start not found")
        j = t.find("</div>", i) + len("</div>")
        inner = t[i:j]
        lab = '{({ all: "All", F: "Forwards", D: "Defence", G: "Goalies" })[pos] + " \\u00b7 " + ({ 1: plan ? "Next week" : "This week", 4: "Next 4 weeks", 0: "Rest of season" })[H] + " \\u00b7 " + gxRngLbl108()}'
        t = t[:i] + "<GxFlt108 label=" + lab + ">" + inner + "<GxRngSel100 /></GxFlt108>" + t[j:]
        print("(install) 108: pickup filters: updated")
    OLDP = '<b></b><GxRngSel100 /><div className="gx-sc99">\n        <div className={"gx-pk text-xs'
    if t.count(OLDP) == 1:
        t = t.replace(OLDP, '<b></b><div className="gx-sc99">\n        <div className={"gx-pk text-xs')
        print("(install) 108: pickups picker moved into filters: updated")

    # --- matchup: one date with arrows, below-projection in red
    i = t.find('<div style={{ display: "grid", gridTemplateColumns: "repeat(" + Math.max(1, n) + ", minmax(0,1fr))", gap: 6, marginTop: 14 }}>')
    if 'className="gx-dn108"' in t:
        print("(install) 108: matchup date: already done")
    else:
        if i < 0:
            fail("108: matchup day buttons not found")
        j = t.find("        })}\n      </div>\n", i) + len("        })}\n      </div>\n")
        t = t[:i] + DAYNAV + t[j:]
        print("(install) 108: matchup date: updated")
    t = lit(t, "108: below projection in red", 'return <div className={right ? "" : "text-right"} style={win ? { color: "var(--good)", fontWeight: 600 } : null}>',
            'return <div className={right ? "" : "text-right"} style={win ? { color: "var(--good)", fontWeight: 600 } : p.st && p.x0 != null && v < p.x0 - 0.05 ? { color: "var(--bad)" } : null}>',
            'v < p.x0 - 0.05 ? { color: "var(--bad)" }')
    return t


edit(APP, change)
