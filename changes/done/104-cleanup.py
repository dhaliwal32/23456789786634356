# changes/104-cleanup.py - skaters and goalies get their own stat columns on rosters; simple pickup rows (Add on ESPN and Hide move to the player screen); tidy Buy low rows on Trades

NEW_CSS = r'''  /* change 104 (install.py) */
  .gx-sc99 .gx-ro { grid-template-columns: 44px 200px 108px 50px 64px 62px 42px 56px 96px 66px 64px 40px 40px 40px 42px 46px 46px 46px 48px 44px 56px 62px 52px; }
  .gx-gh104 { border-top: 0; padding-top: 2px; }
  .gx-sc99 .gx-ro > :nth-child(2) > div, .gx-sc99 .gx-pk > :nth-child(2) > div { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 100%; }
  .gx-bl104 { display: grid; grid-template-columns: 34px minmax(0,1fr) auto auto; gap: 10px; align-items: center; padding: 10px 0; border-top: 1px solid var(--line); }
  .gx-bl104 .why { font-size: 12px; color: var(--mute); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .gx-bl104 .pg { text-align: right; font-weight: 600; font-variant-numeric: tabular-nums; }
  .gx-bl104 .pg span { display: block; font-size: 11px; font-weight: 400; color: var(--mute); }
  .gx-bl104 .tr { font-size: 13px; padding: 5px 10px; border: 1px solid var(--line2); border-radius: 999px; color: var(--ink); white-space: nowrap; }
  @media (max-width: 640px) {
    .gx-sc99 .gx-ro { grid-template-columns: 36px 142px 88px 46px 60px 58px 40px 54px 84px 60px 56px 34px 34px 34px 36px 40px 40px 42px 44px 40px 52px 56px 46px; }
  }
</style>'''

HELPERS = r'''// ---------- change 104: separate skater and goalie stat columns (install.py) ----------
const GX_SK104 = ["GP", "G", "A", "PTS", "+/-", "PIM", "SOG", "HIT", "BLK", "TOI", "FPTS", "Avg"];
const GX_GO104 = ["GP", "W", "L", "OTL", "GA", "SV", "SV%", "GAA", "SO", "TOI", "FPTS", "Avg"];
function gxAgg104(list, isG, sc) {
  const C = isG ? GX_GO104 : GX_SK104;
  if (!list || !list.length) return C.map((h, i) => (i === 0 ? 0 : "-"));
  const n = list.length, S = (f) => list.reduce((a, x) => a + (+f(x) || 0), 0);
  const fp = S((x) => (x.fp != null ? x.fp : gxEst(x, sc)));
  const ts = list.map((x) => gxPdSec(x.toi)).filter((v) => v != null), tot = ts.reduce((a, v) => a + v, 0);
  const toi = ts.length ? gxPdMS(tot / ts.length) : "-";
  if (isG) {
    const sv = S((x) => x.sv), ga = S((x) => x.ga), sa = S((x) => (x.sa != null ? x.sa : (x.sv || 0) + (x.ga || 0)));
    return [n, list.filter((x) => x.dec === "W").length, list.filter((x) => x.dec === "L").length, list.filter((x) => x.dec === "O").length, ga, sv,
      sa ? (sv / sa).toFixed(3).replace(/^0/, "") : "-", tot ? (ga * 3600 / tot).toFixed(2) : "-", list.filter((x) => x.dec === "W" && !x.ga).length, toi, f1(fp), f1(fp / n)];
  }
  const g = S((x) => x.g), a = S((x) => x.a);
  return [n, g, a, g + a, gxPdSigned(S((x) => x.pm)), S((x) => x.pim), S((x) => x.sog), Math.round(S((x) => x.hit)), S((x) => x.blk), toi, f1(fp), f1(fp / n)];
}
function GxSC104({ p, s }) {
  const rng = gxUse100();
  useEffect(() => { gxLoad100(rng); });
  const eid = String(p.id || "").replace(/^e/, ""), isG = p.p === "G";
  let v;
  if (gxProjR100(rng)) { const pr = gxProj100(p, s, rng); v = [pr[0], "-", "-", "-", "-", "-", "-", "-", "-", "-", pr[13], pr[14]]; }
  else { const D = GX100.data[rng]; v = D ? gxAgg104(D[eid], isG, s.sc || {}) : GX_SK104.map(() => "..."); }
  return v.map((c, i) => <div key={"c104" + i} className={"n " + (i >= 10 ? "font-semibold" : "text-slate-500")}>{c}</div>);
}
function GxSH104({ g }) {
  const rng = gxUse100();
  return (g ? GX_GO104 : GX_SK104).map((h, i) => <span key={h + i} className="n">{gxProjR100(rng) && i === 0 ? "Gms" : h}</span>);
}
// heading row for the goalie group (11 blank cells under the roster columns, then the goalie stats)
function GxGH104() {
  return <div className="gx-ro gx-roh gx-gh104">{Array.from({ length: 11 }, (_, i) => <span key={i}></span>)}<GxSH104 g /></div>;
}
// ---------- change 104: tidy Buy low row ----------
function GxBL104({ s, p, r, onPick }) {
  return (
    <div className="gx-bl104">
      <GxFace p={p} size={26} />
      <div className="min-w-0">
        <div className="truncate"><PN p={p} className="font-medium" /> <span className="text-xs text-slate-500">{p.p}</span></div>
        <div className="why"><TL s={s} id={p.ft} />{" · " + r.join(", ")}</div>
      </div>
      <div className="pg">{f1(effAvg(p, s.blend))}<span>pts/g</span></div>
      <button type="button" className="tr" onClick={() => onPick(p)}>+ Trade</button>
    </div>
  );
}
'''

OLD_SUB = '<div className="text-xs text-slate-500 truncate">{"Swap for " + r.d.n + " \\u00b7 " + (keep ? "keep" : H === 1 ? "one week only" : "short-term") + (tg ? " \\u00b7 " + tg.t : "")}{" \\u00b7 "}<button type="button" className="text-blue-600" onClick={(e) => { e.stopPropagation(); if (window.__QA) window.__QA.espn(r.f); }}>Add on ESPN</button>{" \\u00b7 "}<button type="button" className="text-blue-600" onClick={(e) => { e.stopPropagation(); gxHide.toggle(r.f.id); }}>{gxHideSet().has(r.f.id) ? "Show again" : "Hide" /* gx075-row */}</button>{gxScratch(r.f) ? <span style={{ color: "var(--warn)" }}>{" \\u00b7 not in lineup"}</span> : null}</div>'
NEW_SUB = '<div className="text-xs text-slate-500 truncate">{"for " + r.d.n + (keep ? "" : H === 1 ? " \\u00b7 this week" : " \\u00b7 short-term") + (tg ? " \\u00b7 " + tg.t : "") /* gx104-row */}{gxScratch(r.f) ? <span style={{ color: "var(--warn)" }}>{" \\u00b7 not in lineup"}</span> : null}</div>'

HIDE_BTN = '{Q.fa(p) ? <GxPdWatch p={p} Q={Q} /> : null}{Q.fa(p) ? <button type="button" onClick={() => { gxHide.toggle(p.id); onClose(); }}>{gxHideSet().has(p.id) ? "Show in pickups" : "Hide from pickups"}</button> : null}'


def rep(t, label, old, new, n, marker):
    if marker in t:
        print("(install) " + label + ": already done")
        return t
    k = t.count(old)
    if k != n:
        fail(label + ": expected " + str(n) + " places, found " + str(k) + "; nothing changed")
    print("(install) " + label + ": updated (" + str(k) + ")")
    return t.replace(old, new)


def change(t):
    t = lit(t, "104: styles", "</style>", NEW_CSS, "change 104 (install.py)")
    t = lit(t, "104: helpers", ROOT, HELPERS + ROOT, "change 104: separate skater and goalie")
    t = rep(t, "104: skater cells", "<GxSC100 p={p} s={s} />", "<GxSC104 p={p} s={s} />", 2, "<GxSC104 p={p} s={s} />")
    t = rep(t, "104: skater headings", "<GxSH100 />", "<GxSH104 />", 2, "<GxSH104 />")
    t = rep(t, "104: goalie heading row", '<div className="gx-tag" style={{ padding: "8px 0 4px" }}>{title}</div>',
            '<div className="gx-tag" style={{ padding: "8px 0 4px" }}>{title}</div>{title === "Goalies" ? <GxGH104 /> : null}', 2, '{title === "Goalies" ? <GxGH104 /> : null}')
    t = lit(t, "104: simple pickup rows", OLD_SUB, NEW_SUB, "/* gx104-row */")
    t = lit(t, "104: hide from the player screen", '{Q.fa(p) ? <GxPdWatch p={p} Q={Q} /> : null}', HIDE_BTN, '"Hide from pickups"')
    t = lit(t, "104: buy low heading", '<div className="text-xs uppercase tracking-wide text-slate-500">Buy low ({list.length}): good players who are cold, unlucky or underrated</div>',
            '<div className="text-xs text-slate-500">{list.length + " players"}</div>', '{list.length + " players"}')
    t = lit(t, "104: buy low rows",
            '<PlayerLine key={p.id} s={s} p={p} extra={<><span className="text-sky-600">{"\\u00b7 " + r.join(", ")}</span><button type="button" className="text-blue-600" onClick={() => onPick(p)}>Add to trade</button></>} />',
            '<GxBL104 key={p.id} s={s} p={p} r={r} onPick={onPick} />', "<GxBL104 key={p.id}")
    t = lit(t, "104: hide on the phone header",
            ': <button type="button" onClick={() => Q.espn(p)}>Add on ESPN</button>}',
            ': <><button type="button" onClick={() => Q.espn(p)}>Add on ESPN</button><button type="button" onClick={() => { gxHide.toggle(p.id); close101(); }}>{gxHideSet().has(p.id) ? "Show" : "Hide"}</button></>}',
            '{gxHideSet().has(p.id) ? "Show" : "Hide"}')
    return t


edit(APP, change)
