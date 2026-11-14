# changes/286-lines-photo-cards.py - Lines: clean photo cards instead of jerseys and locker stalls (photo, name, number and position, points a game, who owns him; your players outlined, free agents marked Free, small Hot / Cold mark)

NEW_CSS = r'''  /* change 286 (install.py) */
  .gx-bd286 { margin-top: 12px; }
  .gx-bd286 .row { display: grid; grid-template-columns: 30px repeat(6, minmax(0, 1fr)); gap: 8px; align-items: stretch; margin-bottom: 8px; }
  .gx-bd286 .row > .lb { align-self: center; font-size: 12px; font-weight: 700; letter-spacing: .04em; color: var(--mute); }
  .gx-bd286 .row > .gx-cd286 { grid-column: span 2; }
  .gx-bd286 .row.c112 > .gx-cd286 { grid-column: span 3; }
  .gx-bd286 .sp { height: 10px; }
  .gx-cd286 { position: relative; display: flex; flex-direction: column; align-items: center; justify-content: flex-start; gap: 2px; min-width: 0; height: 132px; padding: 12px 6px 8px; border-radius: 14px; background: var(--card); border: 1px solid var(--line); color: var(--ink); text-align: center; transition: transform .12s ease, border-color .15s ease, background-color .15s ease; }
  .gx-cd286:hover { background: var(--card3); }
  .gx-cd286.me { border-color: var(--accent); }
  .gx-cd286.empty { background: none; border-style: dashed; }
  .gx-cd286 .ph { width: 46px; height: 46px; display: flex; align-items: center; justify-content: center; flex: none; }
  .gx-cd286 .ph .no { width: 44px; height: 44px; border-radius: 12px; background: var(--card3); color: var(--mute); display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 15px; }
  .gx-cd286 .nm { max-width: 100%; margin-top: 4px; font-size: 13.5px; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .gx-cd286 .sb { font-size: 11px; color: var(--mute); white-space: nowrap; }
  .gx-cd286 .bt { margin-top: auto; display: flex; align-items: baseline; justify-content: center; gap: 6px; max-width: 100%; font-size: 11px; color: var(--mute); white-space: nowrap; font-variant-numeric: tabular-nums; }
  .gx-cd286 .bt b { font-size: 13px; font-weight: 600; color: var(--ink); }
  .gx-cd286 .bt .ow { overflow: hidden; text-overflow: ellipsis; }
  .gx-cd286 .bt .fa { color: var(--good); font-weight: 600; }
  .gx-cd286 .hc { position: absolute; top: 6px; right: 7px; font-size: 9.5px; font-weight: 700; letter-spacing: .05em; }
  .gx-cd286 .hc.h { color: var(--warn); }
  .gx-cd286 .hc.c { color: #7fa8d8; }
  @media (max-width: 640px) {
    .gx-bd286 .row { grid-template-columns: 22px repeat(6, minmax(0, 1fr)); gap: 6px; margin-bottom: 6px; }
    .gx-bd286 .row > .lb { font-size: 11px; }
    .gx-cd286 { height: 126px; padding: 10px 4px 7px; border-radius: 12px; }
    .gx-cd286 .nm { font-size: 12.5px; }
  }
</style>'''

EMPTY_OLD = r'''    if (!n) return <div key={"e" + i} className="gx-fg224 gx-lt227 empty"></div>;'''
EMPTY_NEW = r'''    if (!n) return <div key={"e" + i} className="gx-cd286 empty"></div>;'''

CHIP_START = r'''    { const p = byName[nrm(n)], mine = p && p.ft === s.me, fa = p && p.ft === "fa", last = n.split(" ").slice(1).join(" ") || n;'''
CHIP_END = r'''      ); }
'''
CHIP_NEW = r'''    { /* change 286: clean photo card */
      const p = byName[nrm(n)], mine = p && p.ft === s.me, fa = p && p.ft === "fa", last = n.split(" ").slice(1).join(" ") || n;
      const isG = (ln.G || []).includes(n) || (p && p.p === "G"), no = gxNo248(T, n), hc = gxHC248(p, h248, s);
      const pos = isG ? "G" : String(df[n] || (p ? p.p : "")).replace(/[0-9]/g, "").toUpperCase();
      const own = !p ? "" : mine ? "Yours" : fa ? (p.wv ? "Waivers" : "Free") : ((teamName(s, p.ft) || "").replace(/[^A-Za-z0-9' ]/g, " ").trim().split(/\s+/)[0] || "").slice(0, 9);
      return (
        <button key={n + i} type="button" className={"gx-cd286" + (mine ? " me" : "")} aria-label={n} data-gx="286" onClick={() => { if (p && window.__NAV) window.__NAV.player(p); }}>
          {hc ? <span className={"hc " + hc.charAt(0)}>{hc.charAt(0) === "h" ? "HOT" : "COLD"}</span> : null}
          <span className="ph">{p ? <GxFace p={p} size={28} /> : <span className="no">{no != null ? no : last.charAt(0)}</span>}</span>
          <span className="nm">{last}</span>
          <span className="sb">{(no != null ? "#" + no + " \u00b7 " : "") + pos}</span>
          <span className="bt">{p ? <><b>{f1(gxPgAvg(p, s.blend))}</b><span className={"ow" + (fa ? " fa" : "")}>{own}</span></> : null}</span>
        </button>
      ); }
'''

BOARD_START = r'''<div key={t + mode} className={"gx-rk111 rm236 " + gxRoom236(t).cls} style={gxRoom236(t).style} data-gx="236">'''
BOARD_END = r'''            {rows}
          </div>'''
BOARD_NEW = r'''<div key={t + mode} className="gx-bd286" data-gx="286b">
            {rows}
          </div>'''


def cut(t, name, start, end, new, done):
    if done in t:
        print(f"(install) {name}: already done")
        return t
    if t.count(start) != 1:
        fail(f"'{name}' start matched {t.count(start)} times")
    a = t.find(start)
    b = t.find(end, a)
    if b < 0:
        fail(f"'{name}' end not found")
    print(f"(install) {name}: updated")
    return t[:a] + new + t[b + len(end):]


def change(t):
    t = lit(t, "286: styles", "</style>", NEW_CSS, "change 286 (install.py)")
    t = lit(t, "286: empty spot", EMPTY_OLD, EMPTY_NEW, 'className="gx-cd286 empty"')
    t = cut(t, "286: photo card", CHIP_START, CHIP_END, CHIP_NEW, "change 286: clean photo card")
    t = cut(t, "286: plain board", BOARD_START, BOARD_END, BOARD_NEW, 'data-gx="286b"')
    return t

edit(APP, change)
