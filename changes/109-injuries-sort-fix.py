# changes/109-injuries-sort-fix.py - tapping a stat heading sorts right away (the lists now listen for it); Pickups stat headings show; new clean Injuries page (filters behind one button, best players first or by return date); Week plan / Advice links and League's Player rankings link removed

NEW_CSS = r'''  /* change 109 (install.py) */
  .gx-ij109 { display: grid; grid-template-columns: 36px minmax(0,1fr) auto; gap: 10px; align-items: center; padding: 10px 0; border-top: 1px solid var(--line); }
  .gx-ij109:first-child { border-top: 0; }
  .gx-ij109 .l2 { font-size: 12px; color: var(--mute); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .gx-ij109 .ev { font-size: 12px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .gx-ij109 .ev.up { color: var(--good); } .gx-ij109 .ev.wn { color: var(--warn); } .gx-ij109 .ev.dn { color: var(--bad); }
  .gx-ij109 .v { text-align: right; font-weight: 600; font-variant-numeric: tabular-nums; }
  .gx-ij109 .v small { display: block; font-size: 11px; font-weight: 400; color: var(--mute); }
</style>'''

HELPERS = r'''// ---------- change 109: clean Injuries page (install.py) ----------
function GxInj109({ s }) {
  const ea = gxPgAvg, K = s.blend;
  const [who, setWho] = useState(() => uiGet()["ij85:who"] || "fa");
  const [pos, setPos] = useState("all");
  const [by, setBy] = useState(() => uiGet().ij109by || "best");
  const [nU, setNU] = useState(5);
  const [nL, setNL] = useState(15);
  const D = useMemo(() => {
    const EV = ((window.__SIG || {}).injmoves) || {}, list = [], ups = [];
    s.players.forEach((p) => {
      const id = typeof p.id === "string" && p.id[0] === "e" ? p.id.slice(1) : null;
      const inj = autoInj(p), e = id ? EV[id] : null;
      if (!inj && !(e && e.k === "back")) return;
      const r = { p, v: ea(p, K), inj, e, back: inj ? effBack(p).d : "" };
      if (inj) list.push(r);
      if (e) ups.push(r);
    });
    return { list, ups };
  }, [s]);
  const keep = (r) => (who === "fa" ? r.p.ft === "fa" : who === "mine" ? r.p.ft === s.me : true) && (pos === "all" || r.p.p === pos);
  const best = (a, b) => b.v - a.v;
  const ups = D.ups.filter(keep).sort(by === "best" ? best : (a, b) => gxIjLast(b.e).localeCompare(gxIjLast(a.e)) || best(a, b));
  const list = D.list.filter(keep).sort(by === "best" ? best : (a, b) => (a.back || "9").localeCompare(b.back || "9") || best(a, b));
  const ev = (e) => (e.k === "back" ? ["up", "Off the injury list"] : e.k === "sooner" ? ["up", "Back sooner, now " + mdL(e.now)] : e.k === "dtd" ? ["up", "Now day-to-day"]
    : e.k === "later" ? ["wn", "Pushed back to " + mdL(e.now)] : e.k === "new" ? ["dn", "New injury" + (e.now ? ", back " + mdL(e.now) : "")] : ["", "New news"]);
  const own = (p) => (p.ft === "fa" ? "" : p.ft === s.me ? "Yours · " : teamName(s, p.ft) + " · ");
  const row = (r, upd) => {
    const st = r.inj ? (r.inj.status || "Out").replace("Injured Reserve", "IR") + (r.back ? " · back " + mdL(r.back) : "") : "Healthy";
    const x = upd && r.e ? ev(r.e) : null;
    return (
      <div key={(upd ? "u" : "l") + r.p.id} className="gx-ij109">
        <GxFace p={r.p} size={28} />
        <div className="min-w-0">
          <div className="truncate"><PN p={r.p} className="" /> <span className="text-xs text-slate-500">{r.p.p}</span></div>
          <div className="l2">{(who === "fa" ? "" : own(r.p)) + st}</div>
          {x ? <div className={"ev " + x[0]}>{x[1]}</div> : null}
        </div>
        <div className="v">{f1(r.v)}<small>pts/g</small></div>
      </div>
    );
  };
  const lbl = ({ fa: "Free agents", mine: "My team", all: "All teams" })[who] + " · " + ({ all: "All", F: "Forwards", D: "Defence", G: "Goalies" })[pos] + " · " + (by === "best" ? "Best first" : "By date");
  return (
    <div className="space-y-3">
      <GxFlt108 label={lbl}>
        <Pills items={[["fa", "Free agents"], ["mine", "My team"], ["all", "All teams"]]} value={who} onChange={(v) => { setWho(v); uiSet("ij85:who", v); }} />
        <Pills items={[["all", "All"], ["F", "Forwards"], ["D", "Defence"], ["G", "Goalies"]]} value={pos} onChange={setPos} />
        <Pills items={[["best", "Best first"], ["date", "By date"]]} value={by} onChange={(v) => { setBy(v); uiSet("ij109by", v); }} />
      </GxFlt108>
      {ups.length ? (
        <GxPanel title="Updates" right="last 7 days">
          {ups.slice(0, nU).map((r) => row(r, true))}
          {ups.length > nU ? <button type="button" className="text-sm text-blue-600" style={{ marginTop: 8 }} onClick={() => setNU(nU + 10)}>Show more</button> : null}
        </GxPanel>
      ) : null}
      <GxPanel title="Injured" right={list.length + ""}>
        {list.length ? list.slice(0, nL).map((r) => row(r, false)) : <div className="text-sm text-slate-500">None</div>}
        {list.length > nL ? <button type="button" className="text-sm text-blue-600" style={{ marginTop: 8 }} onClick={() => setNL(nL + 20)}>Show more</button> : null}
      </GxPanel>
    </div>
  );
}
'''


def change(t):
    t = lit(t, "109: styles", "</style>", NEW_CSS, "change 109 (install.py)")
    t = lit(t, "109: helpers", ROOT, HELPERS + ROOT, "change 109: clean Injuries page")
    # lists redraw when a heading is tapped
    for name, sig in (("roster", "function MyTeam({ s, setS, wk, go }) {"), ("other rosters", "function GxRosterTable({ s, wk, tid }) {"),
                      ("pickups", "function Pickups({ s, setS, wk }) {"), ("all players", "function GxRankings({ s }) {")):
        t = lit(t, "109: " + name + " listens for sorting", sig, sig + "\n  gxUseSort108(); /* gx109 */", sig + "\n  gxUseSort108(); /* gx109 */")
    # pickups stat headings
    t = lit(t, "109: pickups stat headings", '<GxSH106 mode={pos === "G" ? "go" : pos === "all" ? "cm" : "sk"} />', '<GxSH106 mode={pos === "G" ? "go" : "sk"} />{/* gx109h */}', "{/* gx109h */}")
    t = lit(t, "109: pickups heading text", '{base == null ? "Free agents, best first" : "Win chance now " + wpTxt(base)}', '{"Player"}', None)
    # injuries page
    t = lit(t, "109: injuries page", 'sub === "injuries" ? <GxInjPage {...P} />', 'sub === "injuries" ? <GxInj109 {...P} />', 'sub === "injuries" ? <GxInj109')
    # no Week plan / Advice links
    i = t.find('      <div className="gx-pn" data-gx="103more">')
    if i >= 0:
        j = t.find("      </div>\n", i) + len("      </div>\n")
        t = t[:i] + t[j:]
        print("(install) 109: plan and advice links removed: updated")
    # no Player rankings link on League
    i = t.find('      <button type="button" className="gx-lk" data-c78="link" onClick={() => go("league", "players")}>')
    if i >= 0:
        j = t.find("      </button>\n", i) + len("      </button>\n")
        t = t[:i] + t[j:]
        print("(install) 109: player rankings link removed: updated")
    return t


edit(APP, change)
