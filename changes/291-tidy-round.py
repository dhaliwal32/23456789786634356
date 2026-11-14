# changes/291-tidy-round.py - Game plan shows only when the ESPN lineup needs a change; Best pickup loads in smoothly; Matchup rows: goalie status is a green / yellow / red dot and the power play tag is short on the phone; Goalies tonight is one slim line that slides a sheet up; week strip on Players adds and removes weeks; no Hot / Cold on Lines; Watch link moved to Setup > More

NEW_CSS = r'''  /* change 291 (install.py) */
  .gd291 { display: inline-block; width: 8px; height: 8px; border-radius: 99px; margin-left: 6px; vertical-align: middle; flex: none; background: var(--warn); }
  .gd291.ok291 { background: var(--good); }
  .gd291.no291 { background: var(--bad); }
  @media (max-width: 640px) { .gx-h2h .gx-pp182 .t291 { display: none; } }
  .gx-gp291 { display: flex; align-items: center; gap: 10px; width: 100%; height: 44px; padding: 0 14px; border-radius: 14px; background: var(--card); color: var(--ink); text-align: left; font-size: 14px; }
  .gx-gp291 > b { font-weight: 600; white-space: nowrap; }
  .gx-gp291 > .ls { flex: 1; min-width: 0; display: flex; align-items: center; gap: 12px; overflow: hidden; color: var(--ink2); white-space: nowrap; font-size: 13px; }
  .gx-gp291 > .ls span { display: inline-flex; align-items: center; gap: 6px; }
  .gx-gp291 > .ls .gd291 { margin-left: 0; }
  .gx-gp291 > .ls em { font-style: normal; color: var(--mute); }
  .gx-sx289 .gx-go289 { background: none; border-radius: 0; }
  .gx-sx289 .gx-go289 > .bd { padding: 0; animation: none; }
  .gx-go289 .rw .st .gd291 { margin: 0 6px 0 0; }
  .gx-bx226 .bp257 { min-height: 150px; }
  .gx-bx226 .bp257 .row230:not(.r):not(.l), .gx-bx226 .bp257 .gn257 { animation: gx291-in .4s cubic-bezier(.2,.8,.2,1) both; }
  @keyframes gx291-in { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: none; } }
  .gx-bx226 .bp257 .sk291 { display: grid; grid-template-columns: 42px minmax(0,1fr) 84px; align-items: center; gap: 10px; margin-top: 8px; height: 44px; }
  .gx-bx226 .bp257 .sk291 i, .gx-bx226 .bp257 .sk291 b, .gx-bx226 .bp257 .sk291 em, .gx-bx226 .bp257 .sk291 u { display: block; border-radius: 8px; background: var(--card3); animation: gx291-pulse 1.2s ease-in-out infinite; }
  .gx-bx226 .bp257 .sk291 i { width: 42px; height: 42px; border-radius: 10px; }
  .gx-bx226 .bp257 .sk291 b { height: 12px; width: 60%; }
  .gx-bx226 .bp257 .sk291 em { height: 10px; width: 40%; margin-top: 8px; }
  .gx-bx226 .bp257 .sk291 u { height: 32px; }
  @keyframes gx291-pulse { 0%, 100% { opacity: .55; } 50% { opacity: 1; } }
  @media (prefers-reduced-motion: reduce) { .gx-bx226 .bp257 .row230, .gx-bx226 .bp257 .gn257, .gx-bx226 .bp257 .sk291 * { animation: none !important; } }
</style>'''

HELPERS = r'''// ---------- change 291: goalie dots, Goalies tonight as a slim line with a sheet (install.py) ----------
// green confirmed, yellow likely or not confirmed yet, red not starting
const gxGd291 = (word) => { const w = String(word || "").toLowerCase(); return /^confirmed/.test(w) ? "ok291" : /sit|backup|not starting|rest/.test(w) ? "no291" : "mid291"; };
function GxGoal291(P) {
  const { s, wk, go } = P, today = todayISO(), gen = (window.ESPN_DATA || {}).generated;
  const [open, setOpen] = useState(false);
  const [out, setOut] = useState(false);
  const close = () => { if (out) return; setOut(true); setTimeout(() => { setOut(false); setOpen(false); }, 180); };
  useEffect(() => { if (!open) return undefined; const k = (e) => { if (e.key === "Escape") close(); }; window.addEventListener("keydown", k); return () => window.removeEventListener("keydown", k); }, [open, out]);
  const d = useMemo(() => { try { return gxGoals289(s, wk, today); } catch (e) { return null; } }, [s.players, wk, today, gen]);
  if (!d) return null;
  const rows = (list, none) => (list.length ? list.map((r) => (
    <button key={r.p.id} type="button" className="rw" onClick={() => { if (window.__NAV) { try { document.documentElement.classList.add("gx-pt281"); } catch (e) {} window.__NAV.player(r.p); } }}>
      <GxFace p={r.p} size={22} />
      <span className="nn"><b>{r.p.n}</b><small>{r.sub}</small></span>
      <span className="st"><i className={"gd291 " + gxGd291(r.w[0])}></i>{r.w[0]}</span>
      <span className="xp">{r.sits ? "\u2013" : f1(r.x)}</span>
    </button>
  )) : <div className="em">{none}</div>);
  return (
    <>
      <button type="button" className="gx-gp291" data-gx="291g" onClick={() => setOpen(true)}>
        <b>Goalies tonight</b>
        <span className="ls">{d.mine.length ? d.mine.map((r) => <span key={r.p.id}><i className={"gd291 " + gxGd291(r.w[0])}></i>{lastN(r.p.n)}</span>) : <em>none of yours play</em>}</span>
        <span className="sec-chev shut" style={{ margin: "0 2px 0 0" }}></span>
      </button>
      {open ? ReactDOM.createPortal(
        <div className={"gx-sx289 fixed inset-0" + (out ? " out" : "")} onClick={close}>
          <div className="pn" onClick={(e) => e.stopPropagation()}>
            <div className="tt"><b>Goalies tonight</b><button type="button" aria-label="Close" onClick={close}>{"\u00d7"}</button></div>
            <div className="nt">Green is confirmed, yellow is likely or not confirmed yet, red is not starting. The number is his points if he starts.</div>
            <div className="gx-go289"><div className="bd">
              <div className="sc">Yours</div>{rows(d.mine, "None play today.")}
              {d.opp ? <><div className="sc">{teamName(s, d.opp)}</div>{rows(d.theirs, "None play today.")}</> : null}
              <div className="sc">Free agents starting</div>{rows(d.free, d.known ? "No free agent is starting tonight." : "Starters are not posted yet.")}
            </div></div>
            <button type="button" className="al" onClick={() => { close(); go("moves", "goalies"); }}>Every goalie, any day</button>
          </div>
        </div>, document.body) : null}
    </>
  );
}
'''

ROUTE_OLD = r'''<GxGoal289 {...P} /><Matchup {...P} />'''
ROUTE_NEW = r'''<GxGoal291 {...P} /><Matchup {...P} />'''

ROW_OLD = r'''<span className="gx-tp155">{p.t + " " + p.p}</span></div>
        <div className="text-xs text-slate-500 truncate">{p.st ? <><GxPP182'''
ROW_NEW = r'''<span className="gx-tp155">{p.t + " " + p.p}</span>{st ? <i className={"gd291 " + gxGd291(st)} title={st} data-gx="291d"></i> : null}</div>
        <div className="text-xs text-slate-500 truncate">{p.st ? <><GxPP182'''
GS_OLD = r'''<>{mGame(p)}{st ? " \u00b7 " + st.toLowerCase() : ""}</>'''
GS_NEW = r'''<>{mGame(p)}</>'''

PP_OLD = r'''{(isPP ? "PP " : "PK ") + gxMmss132(r.left)}</span>;'''
PP_NEW = r'''{isPP ? "PP" : "PK"}<span className="t291">{" " + gxMmss132(r.left)}</span></span>;'''

PL_OLD = r'''  const rows = P ? P.rows : [], show = all ? rows : rows.slice(0, 3), fixN = rows.filter((r) => r.fix).length;'''
PL_NEW = r'''  const rows = P ? P.rows.filter((r) => r.fix) : [], show = all ? rows : rows.slice(0, 3), fixN = rows.length; /* change 291: only what needs changing on ESPN */
  if (!rows.length) return null;'''
GL_OLD = r'''          {P.gl.map((q) => ('''
GL_NEW = r'''          {[].map((q) => ('''

HC_OLD = r'''          {hc ? <span className={"hc " + hc.charAt(0)}>{hc.charAt(0) === "h" ? "HOT" : "COLD"}</span> : null}
'''

WK_OLD = r'''onClick={() => (x.i === sP.wk ? onPick("h1", null) : onPick("pick", [x.i]))}>'''
WK_NEW = r'''onClick={() => { const n = new Set(sel); if (n.has(x.i)) n.delete(x.i); else n.add(x.i); const a = [...n].sort((u, v) => u - v); if (!a.length) return; if (a.length === 1 && a[0] === sP.wk) onPick("h1", null); else onPick("pick", a); }}>{/* change 291: taps add up */}'''

W1_OLD = r'''        <div className="gx-sr"><span>Watch link</span><GxWatchSel174 /></div>
      </div>
      <div className="gx-tag gx-st275">Alerts and lineup</div>'''
W1_NEW = r'''      </div>
      <div className="gx-tag gx-st275">Alerts and lineup</div>'''
W2_OLD = r'''    {row("inj", "Injury return dates", outN ? outN + " of your players hurt or on IR" : "Everyone on your team is healthy", () => go("setup", "inj"), 1)}'''
W2_NEW = r'''    <div className="gx-sr"><span>Watch link</span><GxWatchSel174 /></div>{/* change 291 */}
''' + W2_OLD

SK_OLD = r'''{!L ? <div className="text-xs text-slate-500" style={{ marginTop: 8 }}>Working it out...</div> :'''
SK_NEW = r'''{!L ? <div className="sk291" aria-label="Working it out"><i></i><span><b></b><em></em></span><u></u></div> :'''


def change(t):
    t = lit(t, "291: styles", "</style>", NEW_CSS, "change 291 (install.py)")
    t = lit(t, "291: helpers", ROOT, HELPERS + ROOT, "change 291: goalie dots")
    t = lit(t, "291: goalies line", ROUTE_OLD, ROUTE_NEW, "<GxGoal291 {...P} />")
    t = lit(t, "291: goalie dot in the row", ROW_OLD, ROW_NEW, 'data-gx="291d"')
    t = lit(t, "291: no goalie words", GS_OLD, GS_NEW)
    t = lit(t, "291: short power play tag", PP_OLD, PP_NEW, 'className="t291"')
    t = lit(t, "291: plan only when needed", PL_OLD, PL_NEW, "change 291: only what needs changing")
    t = lit(t, "291: plan without goalies", GL_OLD, GL_NEW)
    t = lit(t, "291: no hot or cold", HC_OLD, "")
    t = lit(t, "291: weeks add up", WK_OLD, WK_NEW, "change 291: taps add up")
    t = lit(t, "291: watch link off the main list", W1_OLD, W1_NEW)
    t = lit(t, "291: watch link in More", W2_OLD, W2_NEW, "{/* change 291 */}")
    t = lit(t, "291: pickup placeholder", SK_OLD, SK_NEW, 'className="sk291"')
    return t

edit(APP, change)
