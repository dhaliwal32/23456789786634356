# changes/086-simulate-trades.py - Trades: "Apply here" puts a trade into the app (every page shows it) and keeps it through syncs until you undo it

NEW_CSS = r'''  /* change 086 (install.py) */
  .gx-sim86 { border-left: 3px solid var(--warn); margin-bottom: 12px; padding: 10px 14px; }
  .gx-sim86 .ln { display: flex; align-items: baseline; gap: 10px; padding: 4px 0; font-size: 14px; }
  .gx-sim86 .ln + .ln { border-top: 1px solid var(--line); }
</style>'''

HELPERS = r'''// ---------- change 086: simulated trades that stay on until you undo them (install.py) ----------
const GX_SIM_K = "gm-simtrade";
const gxSimList = () => { try { const v = JSON.parse(localStorage.getItem(GX_SIM_K) || "[]"); return Array.isArray(v) ? v : []; } catch (e) { return []; } };
const gxSimSave = (l) => { try { localStorage.setItem(GX_SIM_K, JSON.stringify(l)); } catch (e) {} window.dispatchEvent(new Event("gx-sim86")); };
// apply each saved trade in order; a player only moves if he is still where the trade expects him
const gxSimPlayers = (players) => {
  const L = gxSimList();
  if (!L.length) return players;
  let P = players, keep = [];
  L.forEach((t) => {
    const at = {}; P.forEach((p) => { at[p.id] = p.ft; });
    const real = t.give.every((id) => at[id] === t.b) && t.get.every((id) => at[id] === t.a);
    if (real) return; // the real trade went through on ESPN, so the what-if is no longer needed
    const mv = {};
    t.give.forEach((id) => { if (at[id] === t.a) mv[id] = t.b; });
    t.get.forEach((id) => { if (at[id] === t.b) mv[id] = t.a; });
    (t.add || []).forEach((id) => { if (at[id] === "fa") mv[id] = t.a; });
    (t.drop || []).forEach((id) => { if (at[id] === t.a) mv[id] = "fa"; });
    if (!Object.keys(mv).length) return;
    keep.push(t);
    P = P.map((p) => (mv[p.id] ? { ...p, ft: mv[p.id], ir: false } : p));
  });
  if (keep.length !== L.length) { try { localStorage.setItem(GX_SIM_K, JSON.stringify(keep)); } catch (e) {} }
  return P;
};
const gxSimReload = (setS) => {
  const E = window.ESPN_DATA;
  setS((st) => { if (E) { try { return applyESPN(st, E); } catch (e) {} } return { ...st, players: gxSimPlayers(st.players) }; });
};
const gxSimAdd = (t, setS) => { gxSimSave(gxSimList().concat([t])); gxSimReload(setS); };
const gxSimDrop = (i, setS) => { gxSimSave(gxSimList().filter((_, k) => k !== i)); gxSimReload(setS); };
function GxSimBar({ s, setS, go }) {
  const [, tick] = useState(0);
  useEffect(() => { const h = () => tick((x) => x + 1); window.addEventListener("gx-sim86", h); return () => window.removeEventListener("gx-sim86", h); }, []);
  const L = gxSimList();
  if (!L.length || !s || !s.players) return null;
  const real = window.__TB_REAL || s.me;
  const nm = (ids) => ids.map((id) => { const p = s.players.find((x) => x.id === id); return p ? p.n : null; }).filter(Boolean).join(", ");
  const who = (id) => (id === real ? "You" : teamName(s, id).trim());
  const line = (t) => {
    const g = t.get.concat(t.add || []);
    return who(t.a) + (t.a === real ? " get " : " gets ") + nm(g) + "; " + (t.b === real ? "you get " : teamName(s, t.b).trim() + " gets ") + nm(t.give) + ((t.drop || []).length ? "; " + (t.a === real ? "you drop " : who(t.a) + " drops ") + nm(t.drop) : "") + ".";
  };
  return (
    <div className="gx-pn gx-sim86"><b></b><b></b><b></b><b></b>
      <div className="text-sm" style={{ display: "flex", alignItems: "baseline", gap: 10, flexWrap: "wrap" }}>
        <span className="font-semibold" style={{ color: "var(--warn)" }}>{L.length === 1 ? "What-if trade is on" : L.length + " what-if trades are on"}</span>
        <span className="text-xs text-slate-500">Every page shows it. Nothing changed on ESPN.</span>
        <span style={{ marginLeft: "auto" }}>{L.length > 1 ? <button type="button" className="text-sm text-blue-600" onClick={() => { gxSimSave([]); gxSimReload(setS); }}>Undo all</button> : null}</span>
      </div>
      {L.map((t, i) => (
        <div key={i} className="ln">
          <span className="min-w-0" style={{ flex: 1 }}>{line(t)}</span>
          <button type="button" className="text-sm text-blue-600 whitespace-nowrap" onClick={() => gxSimDrop(i, setS)}>Undo</button>
        </div>
      ))}
    </div>
  );
}
'''

APPLY_BTN = r'''
          {/* gx086-apply */}<div style={{ display: "flex", flexWrap: "wrap", alignItems: "center", gap: 12, marginTop: 12 }}>
            <button type="button" className="bg-blue-600 rounded-lg px-4 py-1.5 font-semibold" onClick={() => { gxSimAdd({ a: s.me, b: partner, give: Gv.map((p) => p.id), get: Rv.map((p) => p.id), add: picks.filter(Boolean).map((p) => p.id), drop: drops.map((p) => p.id) }, setS); setGive([]); setGet([]); setPick({}); setEdit(-1); setDropSel([]); window.scrollTo(0, 0); }}>Apply here</button>
            <span className="text-xs text-slate-500">Shows this trade on every page of the app, through syncs, until you undo it. Nothing changes on ESPN.</span>
          </div>'''

END_NOTE = '(thOver > 0 ? " " + teamName(s, partner) + " would be over 22 and would have to drop " + thOver + " too." : "")}</div>'

def change(t):
    t = lit(t, "086: styles", "</style>", NEW_CSS, "change 086 (install.py)")
    t = lit(t, "086: helpers", ROOT, HELPERS + ROOT, "change 086: simulated trades")
    t = lit(t, "086: trades keep after a sync",
            "return { ...s, teams, me, opp, players, weeks, wk, lastSync: E.generated,",
            "return { ...s, teams, me, opp, players: gxSimPlayers(players), weeks, wk, lastSync: E.generated,",
            "players: gxSimPlayers(players)")
    t = lit(t, "086: builder can change the app",
            "function TradeBuilder({ s, initPartner }) {",
            "function TradeBuilder({ s, initPartner, setS }) {",
            "function TradeBuilder({ s, initPartner, setS }) {")
    t = lit(t, "086: Apply here button", END_NOTE, END_NOTE + APPLY_BTN, "{/* gx086-apply */}")
    t = lit(t, "086: bar on every page",
            "<SubBar tab={tab} sub={sub} go={go} setSubs={setSubs} nav={nav} s={s} wk={wk} /><GxExtras",
            "<GxSimBar s={s} setS={setS} go={go} />{/* gx086-bar */}<SubBar tab={tab} sub={sub} go={go} setSubs={setSubs} nav={nav} s={s} wk={wk} /><GxExtras",
            "{/* gx086-bar */}")
    return t

edit(APP, change)
