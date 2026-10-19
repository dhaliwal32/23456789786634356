# changes/083-head-start.py - Pickups: when this week is already decided (85%+ or 15%- to win) and moves are left, suggest pickups that help most next week; can be turned off for the week

NEW_CSS = r'''  /* change 083 (install.py) */
  .gx-hs83 { display: grid; grid-template-columns: 26px minmax(0,1fr) 58px 58px; gap: 10px; align-items: center; padding: 9px 0; border-top: 1px solid var(--line); font-size: 14px; font-variant-numeric: tabular-nums; }
  .gx-hs83 .n { text-align: right; }
  .gx-hs83.hd { border-top: 0; padding-top: 2px; font-size: 12px; color: var(--mute); }
</style>'''

HELPERS = r'''// ---------- change 083: head start on next week when this week is decided (install.py) ----------
const GX_HS_SURE = 0.85;
const gxHsKey = (s) => "hs83:" + (((s.weeks || [])[s.wk] || {}).label || s.wk);
const gxHsOff = (s) => !!uiGet()[gxHsKey(s)];
const gxHsSet = (s, off) => { uiSet(gxHsKey(s), off); window.dispatchEvent(new Event("gx-hs83")); };
const gxHsCan = (s, base, ml) => !!nextWkS(s) && ml > 0 && base != null && (base >= GX_HS_SURE || base <= 1 - GX_HS_SURE);
function gxUseHs() {
  const [n, setN] = useState(0);
  useEffect(() => { const h = () => setN((x) => x + 1); window.addEventListener("gx-hs83", h); return () => window.removeEventListener("gx-hs83", h); }, []);
  return n;
}
function GxHsLine({ s, base, ml }) {
  gxUseHs();
  if (!gxHsCan(s, base, ml)) return null;
  const btn = { marginLeft: 6 };
  if (gxHsOff(s)) return <span>{" "}<button type="button" className="text-blue-600 text-sm" style={btn} onClick={() => gxHsSet(s, false)}>Use them for next week instead</button></span>;
  return (
    <span className="text-slate-500">
      {" " + (base >= GX_HS_SURE ? "You're " + wpTxt(base) + " to win this week" : "This week looks lost (" + wpTxt(base) + ")") + ", so they're aimed at next week."}
      <button type="button" className="text-blue-600 text-sm" style={btn} onClick={() => gxHsSet(s, true)}>Keep them for this week</button>
    </span>
  );
}
function GxHeadStart({ s, base, ml }) {
  const hsV = gxUseHs();
  const gxHideV = gxUseHide();
  const sN = nextWkS(s);
  const on = gxHsCan(s, base, ml) && !gxHsOff(s);
  const baseN = useMemo(() => (on ? winChance(sN) : null), [on, s]);
  const rows = useMemo(() => {
    if (!on || baseN == null) return [];
    const M = computeMoves(s, { H: 2, pos: "all", pool: 60 });
    const out = [];
    M.res.slice(0, 30).forEach((r) => {
      if (gxHideSet().has(r.f.id) || gxScratch(r.f)) return;
      const R = afterMove(s, r.f, r.d), now = winChance(s, R), nx = winChance(sN, R);
      if (now == null || nx == null || nx <= baseN + 0.004) return;
      if (base >= GX_HS_SURE && now < Math.min(base, GX_HS_SURE) - 0.03) return;
      out.push({ ...r, now, nx });
    });
    return out.sort((a, b) => b.nx - a.nx || b.gain - a.gain).slice(0, 5);
  }, [on, s, baseN, gxHideV, hsV]);
  if (!on || baseN == null) return null;
  const wN = deriveWeek(sN.weeks[sN.wk], sN.autoDone), opp = oppOf(wN, s.me);
  return (
    <div className="gx-pn"><b></b><b></b><b></b><b></b>
      <div className="gx-st">Pickups for next week</div>
      <div className="text-xs text-slate-500" style={{ marginTop: 2, marginBottom: 6 }}>
        {"Best adds for next week" + (opp ? " against " + teamName(s, opp) : "") + " (" + wpTxt(baseN) + " now). You still get 3 new moves next week."}
      </div>
      {rows.length ? (
        <div>
          <div className="gx-hs83 hd"><span></span><span></span><span className="n">This wk</span><span className="n">Next wk</span></div>
          {rows.map((r) => (
            <div key={r.f.id} className="gx-hs83">
              <TeamLogo t={r.f.t} size={26} />
              <div className="min-w-0">
                <div className="truncate"><PN p={r.f} className="" /> <span className="text-xs text-slate-500">{r.f.p}</span>{r.f.wv ? <span className="text-xs" style={{ color: "var(--warn)", marginLeft: 6 }}>on waivers</span> : null}</div>
                <div className="text-xs text-slate-500">{"Swap for " + r.d.n + " · "}<button type="button" className="text-blue-600" onClick={(e) => { e.stopPropagation(); if (window.__QA) window.__QA.espn(r.f); }}>Add on ESPN</button>{" · "}<button type="button" className="text-blue-600" onClick={(e) => { e.stopPropagation(); gxHide.toggle(r.f.id); }}>Hide</button></div>
              </div>
              <div className="n" style={{ color: r.now < base - 0.004 ? "var(--bad)" : "var(--ink)" }}>{wpTxt(r.now)}</div>
              <div className="n font-semibold" style={{ color: "var(--good)" }}>{wpTxt(r.nx)}</div>
            </div>
          ))}
        </div>
      ) : <div className="text-sm text-slate-500" style={{ padding: "6px 0" }}>No free agent raises next week's win chance right now.</div>}
    </div>
  );
}
'''

HEAD_OLD = '<span className="font-semibold">{ml === 0 ? "No moves left this week." : ml == null ? "" : ml + " move" + (ml === 1 ? "" : "s") + " left this week."}</span>'

def change(t):
    t = lit(t, "083: styles", "</style>", NEW_CSS, "change 083 (install.py)")
    t = lit(t, "083: helpers", ROOT, HELPERS + ROOT, "change 083: head start on next week")
    t = lit(t, "083: top line on Pickups", HEAD_OLD,
            HEAD_OLD + "{!plan ? <GxHsLine s={s} base={base} ml={ml} /> : null}{/* gx083-h */}",
            "{/* gx083-h */}")
    t = lit(t, "083: box on Pickups",
            "<GxWatchPanel s={s} /><GxHiddenPanel s={s} />{/* gx075-p */}",
            "{!plan ? <GxHeadStart s={s} base={base} ml={ml} /> : null}{/* gx083 */}<GxWatchPanel s={s} /><GxHiddenPanel s={s} />{/* gx075-p */}",
            "{/* gx083 */}")
    return t

edit(APP, change)
