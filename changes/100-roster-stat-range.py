# changes/100-roster-stat-range.py - roster stats picker at top right (Today, Last 7/15/30 days, Season, Next 7/30 days and Rest of season projected); full stat totals; headings line up when sliding on the phone

NEW_CSS = r'''  /* change 100 (install.py) */
  .gx-sc99 > div { width: max-content; min-width: 100%; }
  .gx-sc99 .gx-roh > :nth-child(2) { visibility: visible; }
  .gx-sc99 .gx-tag { display: inline-block; }
  .gx-rs100 { display: flex; justify-content: flex-end; align-items: center; gap: 8px; margin-bottom: 8px; }
  .gx-rs100 select { font-size: 13px; padding: 4px 8px; }
  .gx-sc99 .gx-ro { grid-template-columns: 44px 200px 108px 50px 64px 62px 42px 56px 96px 66px 64px 40px 40px 40px 46px 44px 46px 44px 44px 56px 36px 44px 40px 52px 62px 52px; }
  @media (max-width: 640px) {
    .gx-sc99 .gx-ro { grid-template-columns: 36px 142px 88px 46px 60px 58px 40px 54px 84px 60px 56px 34px 34px 34px 42px 38px 42px 40px 40px 52px 32px 40px 36px 48px 56px 46px; }
  }
</style>'''

HELPERS = r'''// ---------- change 100: stats range picker for rosters (install.py) ----------
const GX_RNG100 = [["today", "Today"], ["l7", "Last 7 days"], ["l15", "Last 15 days"], ["l30", "Last 30 days"], ["sea", "Season"], ["n7", "Next 7 days (projected)"], ["n30", "Next 30 days (projected)"], ["ros", "Rest of season (projected)"]];
const GX_C100 = ["GP", "G", "A", "+/-", "PIM", "SOG", "HIT", "BLK", "TOI", "W", "SV", "GA", "SV%", "FPTS", "Avg"];
const gxRng100 = () => { const v = uiGet().gxRng100; return GX_RNG100.some((r) => r[0] === v) ? v : "sea"; };
const gxProjR100 = (r) => r === "n7" || r === "n30" || r === "ros";
const GX100 = (window.__GX100 = window.__GX100 || { data: {}, busy: {} });
// past ranges: every saved box score day in the range (plus today's and yesterday's live lines)
function gxLoad100(rng) {
  if (gxProjR100(rng) || GX100.data[rng] || GX100.busy[rng]) return;
  GX100.busy[rng] = true;
  const td = todayISO(), from = rng === "today" ? td : rng === "sea" ? "0000" : addDays(td, -({ l7: 6, l15: 14, l30: 29 }[rng]));
  const P = (window.ESPN_DATA || {}).pstat || {};
  gxBoxIdx().then((idx) => {
    const ds = (idx || []).filter((d) => d >= from && d <= td);
    return Promise.all(ds.map((d) => gxBoxDay(d).then((day) => [d, day || {}]))).then((list) => {
      const have = new Set(ds);
      Object.keys(P).forEach((d) => { if (d >= from && d <= td && !have.has(d)) list.push([d, P[d] || {}]); });
      return list;
    });
  }).then((list) => {
    const o = {};
    list.forEach(([d, day]) => Object.keys(day).forEach((id) => { if (day[id]) (o[id] = o[id] || []).push(day[id]); }));
    GX100.data[rng] = o;
  }).catch(() => { GX100.data[rng] = {}; }).then(() => { GX100.busy[rng] = false; window.dispatchEvent(new Event("gx-rng100")); });
}
function gxAgg100(list, isG, sc) {
  if (!list || !list.length) return GX_C100.map((h, i) => (i === 0 ? 0 : "-"));
  const n = list.length, S = (f) => list.reduce((a, x) => a + (+f(x) || 0), 0);
  const fp = S((x) => (x.fp != null ? x.fp : gxEst(x, sc)));
  const ts = list.map((x) => gxPdSec(x.toi)).filter((v) => v != null);
  const toi = ts.length ? gxPdMS(ts.reduce((a, v) => a + v, 0) / ts.length) : "-";
  if (isG) {
    const sv = S((x) => x.sv), sa = S((x) => (x.sa != null ? x.sa : (x.sv || 0) + (x.ga || 0)));
    return [n, "-", "-", "-", "-", "-", "-", "-", toi, list.filter((x) => x.dec === "W").length, sv, S((x) => x.ga), sa ? (sv / sa).toFixed(3).replace(/^0/, "") : "-", f1(fp), f1(fp / n)];
  }
  return [n, S((x) => x.g), S((x) => x.a), gxPdSigned(S((x) => x.pm)), S((x) => x.pim), S((x) => x.sog), Math.round(S((x) => x.hit)), S((x) => x.blk), toi, "-", "-", "-", "-", f1(fp), f1(fp / n)];
}
// projected ranges: games left and projected fantasy points (the app does not project goals or shots)
function gxProj100(p, s, rng) {
  const td = todayISO(), K = s.blend, S = SCHED[p.t];
  if (!S || p.ir) return GX_C100.map((h, i) => (i === 0 ? 0 : "-"));
  const end = rng === "n7" ? addDays(td, 6) : rng === "n30" ? addDays(td, 29) : "9999";
  let n = 0, x = 0;
  [...S].sort().forEach((d) => {
    if (d < td || d > end || (d === td && gState(p.t, d).s !== "P")) return;
    const av = avail(p, d);
    if (!(av > 0)) return;
    const g = p.p === "G" ? gStart(p, d) : null;
    n += 1;
    x += effAvg(p, K, d) * (g ? g.v : 1) * av;
  });
  return [n, "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", f1(x), n ? f1(x / n) : "-"];
}
const gxUse100 = () => {
  const [, tick] = useState(0);
  useEffect(() => { const f = () => tick((x) => x + 1); window.addEventListener("gx-rng100", f); return () => window.removeEventListener("gx-rng100", f); }, []);
  return gxRng100();
};
function GxSC100({ p, s }) {
  const rng = gxUse100();
  useEffect(() => { gxLoad100(rng); });
  const eid = String(p.id || "").replace(/^e/, "");
  let v;
  if (gxProjR100(rng)) v = gxProj100(p, s, rng);
  else { const D = GX100.data[rng]; v = D ? gxAgg100(D[eid], p.p === "G", s.sc || {}) : GX_C100.map(() => "..."); }
  return v.map((c, i) => <div key={"c100" + i} className={"n " + (i >= 13 ? "font-semibold" : "text-slate-500")}>{c}</div>);
}
function GxSH100() {
  const rng = gxUse100();
  return GX_C100.map((h, i) => <span key={h} className="n">{gxProjR100(rng) && i === 0 ? "Gms" : h}</span>);
}
function GxRngSel100() {
  const rng = gxUse100();
  return (
    <div className="gx-rs100">
      <span className="text-xs text-slate-500">Stats</span>
      <select className={inp} value={rng} onChange={(e) => { uiSet("gxRng100", e.target.value); window.dispatchEvent(new Event("gx-rng100")); }}>
        {GX_RNG100.map(([k, l]) => <option key={k} value={k}>{l}</option>)}
      </select>
    </div>
  );
}
'''


def rep(t, label, pat, new, n, marker):
    if marker in t:
        print("(install) " + label + ": already done")
        return t
    t2, k = re.subn(pat, (lambda m: m.expand(new)) if ("\\1" in new) else (lambda m: new), t)
    if k != n:
        fail(label + ": expected " + str(n) + " places, found " + str(k) + "; nothing changed")
    print("(install) " + label + ": updated (" + str(k) + ")")
    return t2


def change(t):
    t = lit(t, "100: styles", "</style>", NEW_CSS, "change 100 (install.py)")
    t = lit(t, "100: helpers", ROOT, HELPERS + ROOT, "change 100: stats range picker")
    t = rep(t, "100: picker above the roster", r'<b></b><div className="gx-sc99">(\s*<div className="gx-ro gx-roh">)',
            r'<b></b><GxRngSel100 /><div className="gx-sc99">\1', 2, "<GxRngSel100 />")
    t = rep(t, "100: stat headings", re.escape('{GX_ST99.map((h) => <span key={h} className="n">{h}</span>)}'), "<GxSH100 />", 2, "<GxSH100 />")
    t = rep(t, "100: stat cells", re.escape("{gxStats99(p)}"), "<GxSC100 p={p} s={s} />", 2, "<GxSC100 p={p} s={s} />")
    return t


edit(APP, change)
