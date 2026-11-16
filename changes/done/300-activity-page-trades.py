# changes/300-activity-page-trades.py - League activity moves off the main Setup page into its own page (one row to open it); trades show both teams and their players even when ESPN splits the trade over several records; each move and trade shows win chance for every week left, before and after; no vote text unless ESPN gives the votes

HELPERS = r'''// ---------- change 300: League activity page, trade sides, win chance by week (install.py) ----------
const gxActSum300 = (s) => { try { const L = gxAct299(s), td = iso(new Date()); const n = L.filter((m) => iso(new Date(m.at)) === td).length; return L.length ? (n ? n + " move" + (n === 1 ? "" : "s") + " today \u00b7 " : "") + L.length + " in the last 7 days" : "Pickups, drops and trades"; } catch (e) { return "Pickups, drops and trades"; } };
// both sides of a trade, from every ESPN record that belongs to it
function gxSides300(s, root, t) {
  const tx = ((window.ESPN_DATA || {}).tx) || [], recs = tx.filter((x) => x.id === root.id || x.id === t.id || x.rel === root.id || x.rel === t.id || (t.rel && (x.id === t.rel || x.rel === t.rel)));
  const sides = {};
  recs.forEach((x) => (x.it || []).forEach((i) => { if (i[1] === "LINEUP" || i[1] === "DROP") return; const to = gxTm299(s, i[3]); const p = gxPl299(s, i[0]); if (!to || !p || (sides[to] || []).some((q) => q.id === p.id)) return; (sides[to] = sides[to] || []).push(p); }));
  if (!Object.keys(sides).length) {
    const A = gxTm299(s, root.tm), B = gxTm299(s, t.tm !== root.tm ? t.tm : null);
    recs.forEach((x) => (x.it || []).forEach((i) => { const p = gxPl299(s, i[0]); if (!p) return; const to = p.ft === A ? B : p.ft === B ? A : null; if (to && !(sides[to] || []).some((q) => q.id === p.id)) (sides[to] = sides[to] || []).push(p); }));
    if (A && !sides[A]) sides[A] = []; if (B && !sides[B]) sides[B] = [];
  }
  return sides;
}
// win chance in every week left for a team, before and after a move
function GxWeeks300({ s, T, before, after }) {
  const [v, setV] = useState(null);
  useEffect(() => {
    const id = setTimeout(() => { try { const sT = { ...s, me: T, opp: null }; setV({ b: gxWkWins194(sT, before), a: gxWkWins194(sT, after) }); } catch (e) { setV({ b: [], a: [] }); } }, 120);
    return () => clearTimeout(id);
  }, [T]);
  if (!v) return <div className="tl"><small>Working out every week left...</small></div>;
  if (!v.b.length) return null;
  return <GxSimWeeks194 s={s} before={v.b} after={v.a} sel={[]} onW={null} />;
}
'''

ROW_OLD = '''      <GxAct299 s={s} />{/* change 299 */}
'''
ROW_NEW = '''      <div className="gx-pn" style={{ paddingTop: 2, paddingBottom: 2 }}>{row("activity", "League activity", gxActSum300(s), () => go("setup", "activity"), 0)}</div>{/* change 300 */}
'''
PG_OLD = '''  if (sub === "more") return page("More", <>'''
PG_NEW = '''  if (sub === "activity") return <div className="space-y-3"><GxAct299 s={s} /></div>; /* change 300 */
''' + PG_OLD

SD_OLD = '''      const items = (root.it && root.it.length ? root.it : t.it) || [];
      const sides = {};
      items.forEach((i) => { if (i[1] !== "TRADE" && i[1] !== "ADD") return; const to = gxTm299(s, i[3]); if (!to) return; (sides[to] = sides[to] || []).push(gxPl299(s, i[0])); });'''
SD_NEW = '''      const sides = gxSides300(s, root, t); /* change 300 */'''

VT_OLD = '''        : <div className="tl"><small>No votes ESPN shows yet. If the league hides who voted, only the result appears here.</small></div>}'''
VT_NEW = '''        : null}'''

MW_OLD = '''      <div className="sc">SINCE THE MOVE</div>'''
MW_NEW = '''      <GxWeeks300 s={s} T={m.tm} before={s.players.map((p) => (m.add && p.id === m.add.id ? { ...p, ft: "fa" } : m.drop && p.id === m.drop.id ? { ...p, ft: m.tm } : p)).filter((p) => p.ft === m.tm)} after={s.players.filter((p) => p.ft === m.tm)} />
''' + MW_OLD

TW_OLD = '''          <div className="tl" style={{ marginTop: 4 }}><small>Points rest of season</small><b>{fx ? sg(fx[T]) : "\\u2026"}</b></div>'''
TW_NEW = TW_OLD + '''
          {(() => { const from = {}; Object.keys(m.sides).forEach((X) => (m.sides[X] || []).forEach((p) => { if (p) from[p.id] = Object.keys(m.sides).find((Y) => Y !== X); })); const done = Object.keys(m.sides).every((X) => (m.sides[X] || []).every((p) => !p || p.ft === X)); const bef = s.players.map((p) => (done && from[p.id] ? { ...p, ft: from[p.id] } : p)), aft = s.players.map((p) => (!done && from[p.id] !== undefined ? { ...p, ft: Object.keys(m.sides).find((X) => (m.sides[X] || []).some((q) => q && q.id === p.id)) } : p)); return <GxWeeks300 s={s} T={T} before={bef.filter((p) => p.ft === T)} after={aft.filter((p) => p.ft === T)} />; })()}{/* change 300 */}'''

TT_OLD = ''': <><b>{Object.keys(m.sides).map((T) => teamName(s, T)).join(" \\u21c4 ")}</b>'''
TT_NEW = ''': <><b>{Object.keys(m.sides).length ? Object.keys(m.sides).map((T) => teamName(s, T)).join(" \\u21c4 ") : "Trade"}</b>'''

FX_OLD = r'''  const before = s.players.map((p) => (from[p.id] ? { ...p, ft: from[p.id] } : p));
  ids.forEach((T) => { try { const sT = { ...s, me: T, opp: null }; out[T] = horizonTotal(s.players.filter((p) => p.ft === T), sT, nR) - horizonTotal(before.filter((p) => p.ft === T), sT, nR); } catch (e) {} });'''
FX_NEW = r'''  const done = ids.every((X) => (m.sides[X] || []).every((p) => !p || p.ft === X)); /* change 300: a trade still waiting for votes has not moved anyone yet */
  const before = done ? s.players.map((p) => (from[p.id] ? { ...p, ft: from[p.id] } : p)) : s.players, after = done ? s.players : s.players.map((p) => (moved[p.id] ? { ...p, ft: moved[p.id] } : p));
  ids.forEach((T) => { try { const sT = { ...s, me: T, opp: null }; out[T] = horizonTotal(after.filter((p) => p.ft === T), sT, nR) - horizonTotal(before.filter((p) => p.ft === T), sT, nR); } catch (e) {} });'''

NEW_CSS = r'''  /* change 300 (install.py) */
  .gx-ad299 .gx-sw194 { margin-top: 10px; }
  .gx-ad299 .gx-sw194 .sec { font-size: 12px; color: var(--mute); letter-spacing: .04em; text-transform: uppercase; padding: 4px 0; }
  .gx-ad299 .gx-sw194 .nt { display: none; }
  .gx-ad299 .gx-sw194 .wc { cursor: default; }
</style>'''


def change(t):
    t = lit(t, "300: styles", "</style>", NEW_CSS, "change 300 (install.py)")
    t = lit(t, "300: helpers", ROOT, HELPERS + ROOT, "change 300: League activity page")
    t = lit(t, "300: one row on Setup", ROW_OLD, ROW_NEW, '{row("activity", "League activity"')
    t = lit(t, "300: its own page", PG_OLD, PG_NEW, 'if (sub === "activity") return')
    t = lit(t, "300: trade sides", SD_OLD, SD_NEW, "const sides = gxSides300(s, root, t);")
    t = lit(t, "300: no vote text", VT_OLD, VT_NEW)
    t = lit(t, "300: weeks for a move", MW_OLD, MW_NEW, "<GxWeeks300 s={s} T={m.tm}")
    t = lit(t, "300: weeks for a trade", TW_OLD, TW_NEW, "return <GxWeeks300 s={s} T={T}")
    t = lit(t, "300: trade title", TT_OLD, TT_NEW, ': "Trade"}</b>')
    t = lit(t, "300: pending trade points", FX_OLD, FX_NEW, "change 300: a trade still waiting for votes")
    return t


TX_OLD = '''    print(f"(tx) {len(out)} moves in the last {days} days: " + ", ".join(f"{k} {v}" for k, v in sorted(types.items())))'''
TX_NEW = TX_OLD + '''
    for x in out:  # change 300: how ESPN links the parts of a trade (ids shortened, no names)
        if x["ty"].startswith("TRADE"):
            print("(tx) trade part:", x["ty"], x["st"], "id", str(x["id"])[:8], "rel", str(x.get("rel"))[:8], "team", x["tm"], "items", [(i[1], i[2], i[3]) for i in x["it"]])'''

edit(APP, change)
edit("gm_tx.py", lambda t: lit(t, "300: log trade parts", TX_OLD, TX_NEW, "change 300: how ESPN links"))
