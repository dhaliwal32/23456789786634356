# changes/099-slide-tables.py - rosters and pickups slide sideways (player stays on the left, every column available); rosters get today's game, points and stat line columns like ESPN

NEW_CSS = r'''  /* change 099 (install.py) */
  .gx-sc99 { overflow-x: auto; -webkit-overflow-scrolling: touch; overscroll-behavior-x: contain; }
  .gx-sc99 .gx-tag { position: sticky; left: 0; }
  .gx-sc99 .gx-ro, .gx-sc99 .gx-pk { width: max-content; min-width: 100%; column-gap: 0; }
  .gx-sc99 .gx-ro > *, .gx-sc99 .gx-pk > * { display: block !important; }
  .gx-sc99 .gx-ro > .gx-sp, .gx-sc99 .gx-pk > .gx-sp { display: flex !important; }
  .gx-sc99 .gx-ro > * + *, .gx-sc99 .gx-pk > * + * { padding-left: 10px; }
  .gx-sc99 .gx-ro > :nth-child(1), .gx-sc99 .gx-ro > :nth-child(2),
  .gx-sc99 .gx-pk > :nth-child(1), .gx-sc99 .gx-pk > :nth-child(2) { position: sticky; z-index: 2; background: var(--card); align-self: stretch; display: flex !important; flex-direction: column; justify-content: center; }
  .gx-sc99 .gx-ro > :nth-child(1), .gx-sc99 .gx-pk > :nth-child(1) { left: 0; box-shadow: 14px 0 0 var(--card); }
  .gx-sc99 .gx-ro > :nth-child(2), .gx-sc99 .gx-pk > :nth-child(2) { left: 44px; box-shadow: 8px 0 8px -8px rgba(0,0,0,.45); padding-right: 6px; }
  .gx-sc99 .gx-ro > :nth-child(7) span { display: inline; }
  .gx-fc99 { display: flex; align-items: center; }
  .gx-sc99 .gx-op99 { line-height: 1.25; white-space: nowrap; }
  .gx-sc99 .gx-ro { grid-template-columns: 44px 200px 108px 50px 64px 62px 42px 56px 96px 66px 64px repeat(9, 42px); }
  .gx-sc99 .gx-pk { grid-template-columns: 44px 300px 64px 56px 70px 66px 58px 62px 56px; }
  @media (max-width: 640px) {
    .gx-sc99 .gx-ro > :nth-child(2), .gx-sc99 .gx-pk > :nth-child(2) { left: 36px; }
    .gx-sc99 .gx-ro > * + *, .gx-sc99 .gx-pk > * + * { padding-left: 8px; }
    .gx-sc99 .gx-ro { grid-template-columns: 36px 142px 88px 46px 60px 58px 40px 54px 84px 60px 56px repeat(9, 38px); }
    .gx-sc99 .gx-pk { grid-template-columns: 36px 168px 62px 52px 64px 60px 52px 58px 52px; }
  }
</style>'''

HELPERS = r'''// ---------- change 099: today's game and stat line columns for rosters (install.py) ----------
const GX_ST99 = ["G", "A", "+/-", "SOG", "HIT", "BLK", "SV", "GA", "TOI"];
function gxToday99(p) {
  const td = todayISO(), g = p.ir ? null : gameOf(p.t, td), st = g ? gState(p.t, td).s : null, sc = g && st !== "P" ? gScore(p.t, td) : null;
  let opp = "-", res = "";
  if (g) {
    opp = (g.h ? "" : "@") + g.o;
    res = st === "P" ? gameTime(g) : sc && sc.my != null ? sc.my + "-" + sc.op + (st === "F" ? " Final" : sc.per ? " " + sc.per : "") : st === "F" ? "Final" : "Live";
  }
  const a = st && st !== "P" ? gxPdReal(p, td) : null;
  return [
    <div key="t99a" className="gx-op99"><div>{opp}</div>{res ? <div className="text-xs text-slate-500">{res}</div> : null}</div>,
    <div key="t99b" className="n font-semibold">{a == null ? "-" : f1(a)}</div>,
  ];
}
function gxStats99(p) {
  const td = todayISO(), x = gState(p.t, td).s !== "P" ? pStat(p, td) : null, d = "-";
  const v = !x ? GX_ST99.map(() => d)
    : p.p === "G" ? [d, d, d, d, d, d, x.sv != null ? x.sv : d, x.ga != null ? x.ga : d, x.toi || d]
    : [x.g || 0, x.a || 0, gxPdSigned(x.pm), x.sog || 0, x.hit || 0, x.blk || 0, d, d, x.toi || d];
  return v.map((c, i) => <div key={"s99" + i} className="n text-slate-500">{c}</div>);
}
'''


def rep(t, label, pat, new, n, marker):
    if marker in t:
        print("(install) " + label + ": already done")
        return t
    t2, k = re.subn(pat, (lambda m: m.expand(new)) if ("\\1" in new) else (lambda m: new), t)
    if k != n:
        fail(label + ": expected " + str(n) + " places, found " + str(k) + "; nothing changed")
    print("(install) " + label + ": updated (" + str(k) + ")")
    return t2


def change(t):
    t = lit(t, "099: styles", "</style>", NEW_CSS, "change 099 (install.py)")
    t = lit(t, "099: helpers", ROOT, HELPERS + ROOT, "change 099: today's game and stat line columns")
    # rosters (your team and other teams): scroll box around the table
    t = rep(t, "099: roster scroll box open", r'(<div className="gx-pn"><b></b><b></b><b></b><b></b>)(\s*<div className="gx-ro gx-roh">)',
            r'\1<div className="gx-sc99">\2', 2, '<div className="gx-sc99">\n')
    t = rep(t, "099: roster scroll box close", r'(\{list\.map\(row\)\}\s*</div>\s*\)\)\})', r'\1</div>', 2, "{list.map(row)}\n          </div>\n        ))}</div>")
    # roster headings
    t = rep(t, "099: roster headings", re.escape('<span></span><span>Tap a heading to sort</span>'),
            '<span></span><span>Player</span><span>Today</span><span className="n">Pts</span>', 2, '<span>Player</span><span>Today</span>')
    t = rep(t, "099: roster stat headings", re.escape('{HB("rk", "Rank", "m-hide")}'),
            '{HB("rk", "Rank", "m-hide")}{GX_ST99.map((h) => <span key={h} className="n">{h}</span>)}', 2, "{GX_ST99.map((h) =>")
    # roster rows
    t = rep(t, "099: roster today cells", re.escape('{sub ? <div className="text-xs text-slate-500 truncate">{sub}</div> : null}\n        </div>'),
            '{sub ? <div className="text-xs text-slate-500 truncate">{sub}</div> : null}\n        </div>{gxToday99(p)}', 2, "</div>{gxToday99(p)}")
    t = rep(t, "099: roster stat cells", re.escape('<div className="n text-xs text-slate-500 m-hide">{rk ? p.p + " " + ordN(rk) : "\\u2013"}</div>'),
            '<div className="n text-xs text-slate-500 m-hide">{rk ? p.p + " " + ordN(rk) : "\\u2013"}</div>{gxStats99(p)}', 2, "</div>{gxStats99(p)}")
    # face in its own full-height cell, so nothing slides out from under it
    t = rep(t, "099: roster face cell", re.escape('<div key={p.id} className="gx-ro">\n        <GxFace p={p} size={26} />'),
            '<div key={p.id} className="gx-ro">\n        <div className="gx-fc99"><GxFace p={p} size={26} /></div>', 2, '<div className="gx-fc99"><GxFace p={p} size={26} /></div>')
    t = lit(t, "099: pickups face cell", '<div key={r.f.id} className="gx-pk row" role="button" onClick={() => setSim({ add: r.f.id, drop: r.d.id })}>\n              <GxFace p={r.f} size={26} />', '<div key={r.f.id} className="gx-pk row" role="button" onClick={() => setSim({ add: r.f.id, drop: r.d.id })}>\n              <div className="gx-fc99"><GxFace p={r.f} size={26} /></div>', '<div className="gx-fc99"><GxFace p={r.f} size={26} /></div>')
    # pickups
    t = lit(t, "099: pickups scroll box open",
            '      <div className="gx-pn"><b></b><b></b><b></b><b></b>\n        <div className="gx-pk text-xs text-slate-500" style={{ borderTop: 0, paddingTop: 0 }}>',
            '      <div className="gx-pn"><b></b><b></b><b></b><b></b><div className="gx-sc99">\n        <div className="gx-pk text-xs text-slate-500" style={{ borderTop: 0, paddingTop: 0 }}>',
            '<b></b><div className="gx-sc99">\n        <div className="gx-pk text-xs')
    t = lit(t, "099: pickups scroll box close",
            '{all.length > rows.length ? <button type="button" className="text-sm text-blue-600" style={{ marginTop: 10 }} onClick={() => setLimit(limit + 25)}>',
            '</div>{all.length > rows.length ? <button type="button" className="text-sm text-blue-600" style={{ marginTop: 10 }} onClick={() => setLimit(limit + 25)}>',
            '</div>{all.length > rows.length ? <button')
    t = lit(t, "099: pickups headings", 'def="add">Win</GxSH>',
            'def="add">Win</GxSH><span className="n">So far</span><span className="n">Rost</span>',
            '<span className="n">So far</span><span className="n">Rost</span>')
    t = lit(t, "099: pickups cells",
            '{w == null ? "\\u2013" : wpTxt(w)}</div>\n            </div>',
            '{w == null ? "\\u2013" : wpTxt(w)}</div>\n              <div className="n text-slate-500">{r.f.gp ? f1(r.f.tot / r.f.gp) : "-"}</div>\n              <div className="n text-slate-500">{r.f.own != null ? Math.round(r.f.own) + "%" : "-"}</div>\n            </div>',
            '{r.f.gp ? f1(r.f.tot / r.f.gp) : "-"}</div>')
    return t


edit(APP, change)
