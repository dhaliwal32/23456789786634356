# changes/217-players-filters-saved.py - Players remembers your filters (position, weeks, sort, teams) on this device

HELPERS = r'''// ---------- change 217: Players filters remembered on this device (install.py) ----------
function gxPkSaved217(s) {
  let v = {};
  try { v = uiGet().gxPk217 || {}; } catch (e) {}
  const cur = (s && s.wk) || 0;
  let wm = ["h1", "h4", "h0", "lose", "pick"].includes(v.wm) ? v.wm : "h1";
  let wks = Array.isArray(v.wks) ? v.wks.filter((i) => typeof i === "number" && i >= cur) : null;
  if ((wm === "pick" || wm === "lose") && !(wks && wks.length)) { wm = "h1"; wks = null; }
  if (wm !== "pick" && wm !== "lose") wks = null;
  const H = wm === "h4" ? 4 : wm === "h0" ? 0 : 1;
  return { wm, wks, H, pos: ["all", "F", "D", "G"].includes(v.pos) ? v.pos : "all", srt: typeof v.srt === "string" ? v.srt : "add" };
}
function gxRkSaved217() {
  let v = {};
  try { v = uiGet().gxRk217 || {}; } catch (e) {}
  return { pos: ["A", "F", "D", "G"].includes(v.pos) ? v.pos : "A", own: typeof v.own === "string" ? v.own : "all", nhl: typeof v.nhl === "string" ? v.nhl : "all", sort: typeof v.sort === "string" ? v.sort : "exp" };
}
'''

OLD_PK = '''  const [H, setH] = useState(1);
  const [wm193, setWm193] = useState("h1"); /* change 193: h1, h4, h0, lose or pick */
  const [wks193, setWks193] = useState(null);'''
NEW_PK = '''  const sv217 = useMemo(() => gxPkSaved217(s), []); /* change 217: start from the saved filters */
  const [H, setH] = useState(sv217.H);
  const [wm193, setWm193] = useState(sv217.wm); /* change 193: h1, h4, h0, lose or pick */
  const [wks193, setWks193] = useState(sv217.wks);'''
OLD_POS = 'const [pos, setPos] = useState(() => { const v = window.__PICK_POS || "all"; window.__PICK_POS = ""; return v; });'
NEW_POS = 'const [pos, setPos] = useState(() => { const v = window.__PICK_POS || sv217.pos; window.__PICK_POS = ""; return v; });'
OLD_SRT = 'const [srt79, setSrt79] = useState("add");'
NEW_SRT = '''const [srt79, setSrt79] = useState(sv217.srt);
  useEffect(() => { try { uiSet("gxPk217", Object.assign({}, uiGet().gxPk217 || {}, { wm: wm193, wks: wks193, srt: srt79 })); } catch (e) {} }, [wm193, wks193, srt79]); /* change 217 */'''
OLD_PILL = '<Pills items={[["all", "All"], ["F", "Forwards"], ["D", "Defence"], ["G", "Goalies"]]} value={pos} onChange={(v) => { setPos(v); setLimit(40); }} />'
NEW_PILL = '<Pills items={[["all", "All"], ["F", "Forwards"], ["D", "Defence"], ["G", "Goalies"]]} value={pos} onChange={(v) => { setPos(v); setLimit(40); try { uiSet("gxPk217", Object.assign({}, uiGet().gxPk217 || {}, { pos: v })); } catch (e) {} }} />'

OLD_RK = '''  const [pos, setPos] = useState("A"); /* gx202 */
  const [own, setOwn] = useState("all");
  const [nhl203, setNhl203] = useState("all");
  const [q, setQ] = useState("");
  const [sort, setSort] = useState("exp");'''
NEW_RK = '''  const rk217 = useMemo(() => gxRkSaved217(), []); /* change 217: start from the saved filters */
  const [pos, setPos] = useState(rk217.pos); /* gx202 */
  const [own, setOwn] = useState(rk217.own);
  const [nhl203, setNhl203] = useState(rk217.nhl);
  const [q, setQ] = useState("");
  const [sort, setSort] = useState(rk217.sort);
  useEffect(() => { try { uiSet("gxRk217", { pos, own, nhl: nhl203, sort }); } catch (e) {} }, [pos, own, nhl203, sort]); /* change 217 */'''

def change(t):
    t = lit(t, "217: helpers", ROOT, HELPERS + ROOT, "change 217: Players filters remembered")
    t = lit(t, "217: free agent filters", OLD_PK, NEW_PK, "change 217: start from the saved filters */\n  const [H, setH]")
    t = lit(t, "217: position", OLD_POS, NEW_POS, "window.__PICK_POS || sv217.pos")
    t = lit(t, "217: sort", OLD_SRT, NEW_SRT, "const [srt79, setSrt79] = useState(sv217.srt);")
    t = lit(t, "217: position pills", OLD_PILL, NEW_PILL, '{ pos: v })); } catch (e) {} }} />')
    t = lit(t, "217: all players", OLD_RK, NEW_RK, 'uiSet("gxRk217"')
    return t

edit(APP, change)
