# changes/075-hide-pickups.py - Hide button on pickups, and free agents not in their team's lineup are left out of suggestions

HELPERS = r'''// ---------- change 075: hide players from pickup suggestions (install.py) ----------
let __GXH = { raw: null, set: new Set() };
const gxHideSet = () => {
  let raw = "[]";
  try { raw = localStorage.getItem("gm-hide") || "[]"; } catch (e) {}
  if (raw !== __GXH.raw) { let a = []; try { a = JSON.parse(raw) || []; } catch (e) {} __GXH = { raw, set: new Set(a) }; }
  return __GXH.set;
};
const gxHide = {
  list: () => [...gxHideSet()],
  set: (l) => {
    const raw = JSON.stringify((l || []).slice().sort());
    let old = "[]";
    try { old = localStorage.getItem("gm-hide") || "[]"; } catch (e) {}
    if (raw === old) return;
    try { localStorage.setItem("gm-hide", raw); } catch (e) {}
    window.dispatchEvent(new Event("gm-hide"));
  },
  toggle: (id) => { const l = gxHide.list(), i = l.indexOf(id); if (i >= 0) l.splice(i, 1); else l.push(id); gxHide.set(l); },
};
function gxUseHide() {
  const [v, setV] = useState(0);
  useEffect(() => { const h = () => setV((x) => x + 1); window.addEventListener("gm-hide", h); return () => window.removeEventListener("gm-hide", h); }, []);
  return v;
}
// skaters who are healthy but not in their team's current lineup (Daily Faceoff), only when the full lineup is known
const gxLK = (x) => nrm(x).replace(/[.'\u2019]/g, "").replace(/-/g, " ").replace(/\s+/g, " ").trim();
let __GXL = { L: null, m: null };
const gxLineupSets = () => {
  const L = window.LINES_DATA;
  if (!L || !L.teams) return null;
  if (__GXL.L === L && __GXL.m) return __GXL.m;
  const m = {};
  Object.entries(L.teams).forEach(([t, x]) => {
    const ln = (x || {}).lines || {}, names = [];
    ["F1", "F2", "F3", "F4", "D1", "D2", "D3"].forEach((sl) => (ln[sl] || []).forEach((n) => names.push(gxLK(n))));
    if (names.length >= 15) m[t] = new Set(names);
  });
  __GXL = { L, m };
  return m;
};
const gxScratch = (p) => {
  if (!p || p.p === "G" || p.ir) return false;
  const m = gxLineupSets(), set = m && m[p.t];
  if (!set) return false;
  if (avail(p, todayISO()) === 0) return false;
  return !set.has(gxLK(p.n));
};
const goalieOut = (p) => gxGoalieOut0(p) || (!!p && (gxHideSet().has(p.id) || gxScratch(p)));
function GxHiddenPanel({ s }) {
  gxUseHide();
  const [open, setOpen] = useState(false);
  const K = s.blend;
  const list = gxHide.list().map((id) => s.players.find((p) => p.id === id)).filter(Boolean);
  if (!list.length) return null;
  return (
    <div className="gx-pn">
      <button type="button" className="text-sm text-slate-500" onClick={() => setOpen(!open)}>
        {list.length + " player" + (list.length === 1 ? "" : "s") + " hidden from suggestions \u00b7 "}<span className="text-blue-600">{open ? "Close" : "Show"}</span>
      </button>
      {open ? list.map((p) => (
        <div key={p.id} className="gx-row">
          <TeamLogo t={p.t} size={22} />
          <span className="min-w-0 truncate" style={{ flex: 1 }}><PN p={p} className="" /> <span className="text-xs text-slate-500">{p.p + (p.ft !== "fa" ? " \u00b7 " + teamName(s, p.ft) : "")}</span></span>
          <span style={{ fontVariantNumeric: "tabular-nums" }}>{f1(effAvg(p, K))}</span>
          <button type="button" className="text-sm text-blue-600" style={{ marginLeft: 8 }} onClick={() => gxHide.toggle(p.id)}>Show again</button>
        </div>
      )) : null}
      {open ? <div className="text-xs text-slate-500" style={{ marginTop: 8 }}>Hidden players also stay out of the Plan, Advice and trade ideas. Searching a name still finds them.</div> : null}
    </div>
  );
}

'''


def change(t):
    # the old goalie check keeps working under a new name; the new goalieOut adds hidden and not-in-lineup players
    t = lit(t, "075: rename goalie check", "const goalieOut = (p) => {",
            "const gxGoalieOut0 = (p) => { /* gx075-g */", "gx075-g")
    t = lit(t, "075: helpers", ROOT, HELPERS + ROOT, "change 075: hide players")
    # Pickups recomputes when the hidden list changes
    t = lit(t, "075: pickups refresh",
            "const M = useMemo(() => computeMoves(sP, { H, pos, q }), [sP, H, pos, q]);",
            "const gxHideV = gxUseHide(); /* gx075-m */\n  const M = useMemo(() => computeMoves(sP, { H, pos, q }), [sP, H, pos, q, gxHideV]);",
            "gx075-m")
    # Hide link on each pickup row
    t = lit(t, "075: hide link",
            "if (window.__QA) window.__QA.espn(r.f); }}>Add on ESPN</button>",
            r'''if (window.__QA) window.__QA.espn(r.f); }}>Add on ESPN</button>{" \u00b7 "}<button type="button" className="text-blue-600" onClick={(e) => { e.stopPropagation(); gxHide.toggle(r.f.id); }}>{gxHideSet().has(r.f.id) ? "Show again" : "Hide" /* gx075-row */}</button>{gxScratch(r.f) ? <span style={{ color: "var(--warn)" }}>{" \u00b7 not in lineup"}</span> : null}''',
            "gx075-row")
    # hidden list under the watchlist
    t = lit(t, "075: hidden panel", "<GxWatchPanel s={s} />",
            "<GxWatchPanel s={s} /><GxHiddenPanel s={s} />{/* gx075-p */}", "gx075-p")
    # the hidden list syncs between devices
    t = lit(t, "075: sync pick", "return { set, keep, back, watch, theme:",
            "return { set, keep, back, watch, hide: gxHide.list() /* gx075-s1 */, theme:", "gx075-s1")
    t = lit(t, "075: sync sig", '(P.watch || []).slice().sort(), P.theme || "auto"]',
            '(P.watch || []).slice().sort(), (P.hide || []).slice().sort() /* gx075-s2 */, P.theme || "auto"]', "gx075-s2")
    t = lit(t, "075: sync apply", "if (Array.isArray(R.watch)) {",
            "if (Array.isArray(R.hide)) gxHide.set(R.hide); /* gx075-s3 */ if (Array.isArray(R.watch)) {", "gx075-s3")
    t = lit(t, "075: sync listen",
            'window.addEventListener("gm-watch", h); window.addEventListener("gm-theme", h);',
            'window.addEventListener("gm-watch", h); window.addEventListener("gm-theme", h); window.addEventListener("gm-hide", h); /* gx075-s4 */',
            "gx075-s4")
    for must in ("function Today(", "function Pickups(", "const goalieOut = (p) =>", "function GxHiddenPanel("):
        if must not in t:
            fail("fantasy-gm.html looks damaged after change 075 (" + must + ").")
    return t


edit(APP, change)
