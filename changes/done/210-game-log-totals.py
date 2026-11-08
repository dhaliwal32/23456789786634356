# changes/210-game-log-totals.py - Player screen Game log: totals line (goals, assists, points for skaters; record for goalies)

NEW_CSS = r'''  /* change 210 (install.py) */
  .gx-tt210 { display: flex; gap: 8px; margin: 0 0 10px; }
  .gx-tt210 > div { flex: 1 1 0; min-width: 0; height: 52px; border: 1px solid var(--line); border-radius: 10px; display: flex; flex-direction: column; align-items: center; justify-content: center; }
  .gx-tt210 b { font-size: 18px; font-weight: 700; color: var(--ink); font-variant-numeric: tabular-nums; line-height: 1.1; }
  .gx-tt210 small { font-size: 11px; letter-spacing: .06em; color: var(--mute); margin-top: 2px; }
</style>'''

HELPERS = r'''// ---------- change 210: game log totals (install.py) ----------
function GxLogTot210({ log, isG }) {
  if (!log || !log.length) return null;
  const q = log.filter((r) => !r.dnp && r.st !== "P" && r.x);
  if (!q.length) return null;
  const n = (k) => q.reduce((t, r) => t + (+(r.x[k] || 0) || 0), 0);
  let T;
  if (isG) {
    const c = (v) => q.filter((r) => r.x.dec === v).length;
    T = [["W", c("W")], ["L", c("L")], ["OTL", c("O")], ["GP", q.length]];
  } else {
    const g = n("g"), a = n("a");
    T = [["G", g], ["A", a], ["PTS", g + a], ["GP", q.length]];
  }
  return <div className="gx-tt210" data-gx="210">{T.map(([k, v]) => <div key={k}><b>{v}</b><small>{k}</small></div>)}</div>;
}
'''

def change(t):
    t = lit(t, "210: styles", "</style>", NEW_CSS, "change 210 (install.py)")
    t = lit(t, "210: helpers", ROOT, HELPERS + ROOT, "change 210: game log totals")
    old = '''              {log === null ? <div className="text-sm text-slate-500">Loading games...</div>
                : !log.length ? <div className="text-sm text-slate-500">No games saved yet.</div> : (<>'''
    new = '''              <GxLogTot210 log={log} isG={isG} />
              {log === null ? <div className="text-sm text-slate-500">Loading games...</div>
                : !log.length ? <div className="text-sm text-slate-500">No games saved yet.</div> : (<>'''
    t = lit(t, "210: show totals", old, new, "<GxLogTot210 log={log}")
    return t

edit(APP, change)
