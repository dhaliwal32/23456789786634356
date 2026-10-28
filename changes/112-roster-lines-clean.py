# changes/112-roster-lines-clean.py - roster page: no Weakest spots, player updates, injuries/protected, day by day or Rank; no Buy low; Lines: power play 3 on top and 2 below, penalty kill 2 and 2, cleaner player boxes, favourite team asked once (opens every time, changeable in Setup > Display)

NEW_CSS = r'''  /* change 112 (install.py) */
  .gx-sc99 .gx-ro > :nth-child(11) { display: none !important; }
  .gx-sc99 .gx-ro { grid-template-columns: 44px 200px 62px 72px 70px 40px 40px 40px 42px 46px 46px 46px 48px 44px 56px; }
  @media (max-width: 640px) { .gx-sc99 .gx-ro { grid-template-columns: 36px 142px 56px 62px 60px 34px 34px 34px 36px 40px 40px 42px 44px 40px 52px; } }
  /* lines: cleaner boxes, narrower rows of two centred */
  .gx-rk111 .row.c112 { grid-template-columns: 22px repeat(var(--n), minmax(0, 118px)); justify-content: center; }
  .gx-pc111 { border: 0 !important; box-shadow: 0 1px 2px rgba(0,0,0,.08); background: var(--card) !important; border-radius: 12px; }
  .gx-pc111.me { box-shadow: 0 0 0 2px var(--accent) !important; }
  .gx-pc111.fa { box-shadow: 0 1px 2px rgba(0,0,0,.08) !important; }
  .gx-pc111 .o { font-size: 9px; }
  .gx-fav112 { margin-top: 14px; }
  .gx-fav112 .g { display: grid; grid-template-columns: repeat(auto-fill, minmax(64px, 1fr)); gap: 8px; margin-top: 10px; }
  .gx-fav112 .g button { display: flex; flex-direction: column; align-items: center; gap: 4px; padding: 8px 2px; border: 1px solid var(--line); border-radius: 12px; font-size: 12px; }
  .gx-ln111 .fv { margin-left: auto; font-size: 12px; color: var(--mute); }
</style>'''

HELPERS = r'''// ---------- change 112: favourite team for Lines (install.py) ----------
function GxFavPick112({ onPick }) {
  const L = window.LINES_DATA || { teams: {} };
  const teams = Object.keys(L.teams || {}).filter((t) => ((L.teams[t] || {}).lines || {}).F1).sort();
  return (
    <div className="gx-pn gx-fav112">
      <div className="font-semibold">Pick your favourite team</div>
      <div className="text-xs text-slate-500">It opens here every time. Change it in Setup, Display.</div>
      <div className="g">{teams.map((c) => <button key={c} type="button" onClick={() => onPick(c)}><TeamLogo t={c} size={30} />{c}</button>)}</div>
    </div>
  );
}
function GxFavSel112() {
  const L = window.LINES_DATA || { teams: {} };
  const teams = Object.keys(L.teams || {}).filter((t) => ((L.teams[t] || {}).lines || {}).F1).sort();
  const [v, setV] = useState(uiGet().ln111fav || "");
  return (
    <select className={inp} value={v} onChange={(e) => { setV(e.target.value); uiSet("ln111fav", e.target.value); uiSet("ln111", e.target.value); }}>
      <option value="">None</option>
      {teams.map((c) => <option key={c} value={c}>{((L.teams[c] || {}).st || {}).name || c}</option>)}
    </select>
  );
}
'''

NEW_ROWS = '''const unit112 = (lb, arr, a, b) => { const o = ord(arr), r = (k, l, xs, n, c) => { const z = [...xs]; while (z.length < n) z.push(""); return <div key={k} className={"row" + (c ? " c112" : "")} style={{ "--n": n }}><span className="lb">{l}</span>{z.slice(0, n).map(chip)}</div>; }; return [r(lb + "a", lb, o.slice(0, a), a, a < 3), r(lb + "b", "", o.slice(a), b, true)]; };
  const pair112 = (lb, arr) => { const o = ord(arr); while (o.length < 2) o.push(""); return <div key={lb} className="row c112" style={{ "--n": 2 }}><span className="lb">{lb}</span>{o.slice(0, 2).map(chip)}</div>; };
  const rows = mode === "pp" ? [...unit112("PP1", ln.PP1, 3, 2), <div key="s1" className="sp"></div>, ...unit112("PP2", ln.PP2, 3, 2)]
    : mode === "pk" ? [...unit112("PK1", ln.PK1, 2, 2), <div key="s1" className="sp"></div>, ...unit112("PK2", ln.PK2, 2, 2)]
    : [row("L1", ln.F1, 3), row("L2", ln.F2, 3), row("L3", ln.F3, 3), row("L4", ln.F4, 3), <div key="s1" className="sp"></div>,
       pair112("D1", ln.D1), pair112("D2", ln.D2), pair112("D3", ln.D3), <div key="s2" className="sp"></div>, pair112("G", ln.G)];'''


def change(t):
    t = lit(t, "112: styles", "</style>", NEW_CSS, "change 112 (install.py)")
    t = lit(t, "112: helpers", ROOT, HELPERS + ROOT, "change 112: favourite team for Lines")
    # roster page: remove the boxes under the roster
    i = t.find('      <GxPanel title="Weakest spots">')
    if i >= 0:
        j = t.find("      </Section>\n", i)
        if j < 0:
            fail("112: end of the day by day box not found")
        t = t[:i] + "      {/* gx112: weakest spots, updates, injuries, protected, day by day removed */}\n" + t[j + len("      </Section>\n"):]
        print("(install) 112: roster boxes removed: updated")
    elif "gx112: weakest spots" not in t:
        fail("112: Weakest spots box not found")
    # trades: no Buy low
    i = t.find("      <TradeAdvice s={s} onPick=")
    if i >= 0:
        j = t.find("\n", i) + 1
        t = t[:i] + t[j:]
        print("(install) 112: buy low removed: updated")
    # lines: power play and penalty kill units, favourite team
    t = lit(t, "112: lines units",
            'const rows = mode === "pp" ? [row("PP1", ln.PP1, 5), <div key="s1" className="sp"></div>, row("PP2", ln.PP2, 5)]\n    : mode === "pk" ? [row("PK1", ln.PK1, 4), <div key="s1" className="sp"></div>, row("PK2", ln.PK2, 4)]\n    : [row("L1", ln.F1, 3), row("L2", ln.F2, 3), row("L3", ln.F3, 3), row("L4", ln.F4, 3), <div key="s1" className="sp"></div>,\n       row("D1", ln.D1, 2), row("D2", ln.D2, 2), row("D3", ln.D3, 2), <div key="s2" className="sp"></div>, row("G", ln.G, 2)];',
            NEW_ROWS, "const unit112 =")
    t = lit(t, "112: favourite opens first", '  const [t, setT] = useState(() => window.__LINES_TEAM || uiGet().ln111 || "");',
            '  const [t, setT] = useState(() => window.__LINES_TEAM || uiGet().ln111fav || uiGet().ln111 || "");\n  const [fav112, setFav112] = useState(() => uiGet().ln111fav || "");',
            "const [fav112, setFav112] = useState(")
    t = lit(t, "112: ask for favourite", '      ) : <div className="text-sm text-slate-500" style={{ marginTop: 14 }}>Search a team to see its lines.</div>}',
            '      ) : null}\n      {!fav112 ? <GxFavPick112 onPick={(c) => { uiSet("ln111fav", c); setFav112(c); pick(c); }} /> : null}',
            "<GxFavPick112 onPick=")
    # setup > display: favourite team
    t = lit(t, "112: setup favourite team",
            '    <div className="text-xs text-slate-500" style={{ paddingTop: 8 }}>Best switches each day to whichever projection has been most accurate in the AI Lab.</div>\n  </>);',
            '    <div className="gx-sr"><span>Favourite team (Lines)</span><GxFavSel112 /></div>\n    <div className="text-xs text-slate-500" style={{ paddingTop: 8 }}>Best switches each day to whichever projection has been most accurate in the AI Lab.</div>\n  </>);',
            "<GxFavSel112 />")
    return t


edit(APP, change)
