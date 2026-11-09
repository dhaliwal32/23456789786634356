# changes/242-tap-team-to-switch.py - Tap your team picture (phone) or team name (laptop) at the top to switch which team the app shows

NEW_CSS = r'''  /* change 242 (install.py): team menu from the top bar */
  .gx-tw242 { display: flex; align-items: flex-end; gap: 0; padding: 0; background: none; border: 0; color: inherit; text-align: left; cursor: pointer; border-radius: 10px; }
  .gx-tw242:hover .nm242 { text-decoration: underline; text-underline-offset: 3px; }
  .gx-tm242 { position: fixed; inset: 0; z-index: 85; }
  .gx-tm242 .bg { position: absolute; inset: 0; background: rgba(0,0,0,.4); }
  .gx-tm242 .pn { position: absolute; width: min(320px, calc(100vw - 16px)); max-height: calc(100vh - 90px); overflow-y: auto; overscroll-behavior: contain; background: var(--card); border: 1px solid var(--line2); border-radius: 14px; padding: 6px; box-shadow: 0 14px 34px rgba(0,0,0,.55); animation: gx-mm241 .16s ease-out; }
  .gx-tm242 .hd { padding: 8px 12px 6px; font-size: 11px; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; color: var(--mute); }
  .gx-tm242 .it { display: flex; align-items: center; gap: 12px; width: 100%; min-height: 50px; padding: 0 12px; border-radius: 10px; font-size: 15px; font-weight: 600; color: var(--ink); text-align: left; }
  .gx-tm242 .it:active, .gx-tm242 .it:hover { background: var(--hover); }
  .gx-tm242 .it.on { background: var(--card3, var(--card2)); }
  .gx-tm242 .it .tn { flex: 1; min-width: 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .gx-tm242 .it small { flex: none; font-size: 11px; font-weight: 600; color: var(--mute); }
  .gx-tm242 .it svg { width: 16px; height: 16px; flex: none; }
  .gx-tm242 .sep { height: 1px; background: var(--line2); margin: 6px 8px; }
</style>'''

HELPERS = r'''// ---------- change 242: tap the team at the top to switch teams (install.py) ----------
function gxOpenTeams242(e) { const r = e && e.currentTarget ? e.currentTarget.getBoundingClientRect() : null; window.dispatchEvent(new CustomEvent("gx-teams242", { detail: r ? { left: r.left, bottom: r.bottom } : null })); }
function GxTeamMenu242({ s }) {
  const [at, setAt] = useState(null);
  useEffect(() => {
    const h = (e) => setAt(e.detail || { left: 8, bottom: 56 });
    const k = (e) => { if (e.key === "Escape") setAt(null); };
    window.addEventListener("gx-teams242", h); window.addEventListener("keydown", k);
    return () => { window.removeEventListener("gx-teams242", h); window.removeEventListener("keydown", k); };
  }, []);
  if (!at) return null;
  const real = gxReal241();
  const list = [...(s.teams || [])].sort((a, b) => (a.id === real ? -1 : b.id === real ? 1 : String(a.name).localeCompare(String(b.name))));
  const left = Math.max(8, Math.min(at.left, window.innerWidth - Math.min(320, window.innerWidth - 16) - 8));
  const refresh = () => { setAt(null); if (window.__gxPoll129) window.__gxPoll129(); };
  return ReactDOM.createPortal(
    <div className="gx-tm242" data-gx="242">
      <div className="bg" onClick={() => setAt(null)}></div>
      <div className="pn" style={{ top: at.bottom + 6, left }}>
        <div className="hd">View the app as</div>
        {list.map((t) => (
          <button key={t.id} type="button" className={"it" + (t.id === s.me ? " on" : "")} onClick={() => { if (t.id === s.me) { setAt(null); return; } setAt(null); gxSetMe241(t.id); }}>
            <GxFtPic114 id={t.id} size={28} />
            <span className="tn">{t.name}</span>
            {t.id === real ? <small>yours</small> : null}
            {t.id === s.me ? <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M3.5 8.5l3 3 6-7"></path></svg> : null}
          </button>
        ))}
        <div className="sep"></div>
        <button type="button" className="it" onClick={refresh}>
          <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round"><path d="M13 8a5 5 0 1 1-1.5-3.6M13 2.5v2.8h-2.8"></path></svg>
          <span className="tn">Refresh</span>
          <small>{s.lastSync ? fmtTime(s.lastSync) : ""}</small>
        </button>
      </div>
    </div>, document.body);
}
'''

PHONE_OLD = '''onClick={(e) => { const pc = e.currentTarget.querySelector(".pc"); if (pc) { pc.classList.remove("sp240"); void pc.offsetWidth; pc.classList.add("sp240"); } if (window.__gxPoll129) window.__gxPoll129(); }}><span className="pc">'''
PHONE_NEW = '''onClick={gxOpenTeams242} data-gx242="1"><span className="pc">'''

LAP_A = '''    <div className="m-hide max-w-6xl mx-auto px-3 flex items-end gap-1" style={{ paddingTop: 10 }}>
      <span className="gx-badge gx-bp121"><GxFtPic114 id={s.me} size={30} /></span>
      <span style={{ margin: "0 14px 10px 8px", lineHeight: 1.2, minWidth: 0 }}>
        <span className="block font-semibold truncate" style={{ maxWidth: 180 }}>{name}</span>'''
LAP_A2 = '''    <div className="m-hide max-w-6xl mx-auto px-3 flex items-end gap-1" style={{ paddingTop: 10 }}>
      <button type="button" className="gx-tw242" title="Switch team" onClick={gxOpenTeams242} data-gx="242l">
      <span className="gx-badge gx-bp121"><GxFtPic114 id={s.me} size={30} /></span>
      <span style={{ margin: "0 14px 10px 8px", lineHeight: 1.2, minWidth: 0 }}>
        <span className="block font-semibold truncate nm242" style={{ maxWidth: 180 }}>{name}</span>'''
LAP_B = '''        <span className="block text-xs text-slate-500">{rank ? ordN(rank[0]) + " of " + rank[1] : s.league || "\\u00a0"}</span>
      </span>'''
LAP_B2 = LAP_B + '''
      </button>'''

def change(t):
    t = lit(t, "242: styles", "</style>", NEW_CSS, "change 242 (install.py)")
    t = lit(t, "242: helpers", ROOT, HELPERS + ROOT, "change 242: tap the team at the top")
    t = lit(t, "242: phone picture opens the team menu", PHONE_OLD, PHONE_NEW, 'onClick={gxOpenTeams242} data-gx242="1"')
    t = lit(t, "242: laptop name opens the team menu (start)", LAP_A, LAP_A2, 'data-gx="242l"')
    t = lit(t, "242: laptop name opens the team menu (end)", LAP_B, LAP_B2, LAP_B + '\n      </button>')
    t = lit(t, "242: menu mounted", '<GxAsBar241 s={s} />', '<GxAsBar241 s={s} /><GxTeamMenu242 s={s} />', '<GxTeamMenu242 s={s} />')
    return t

edit(APP, change)
