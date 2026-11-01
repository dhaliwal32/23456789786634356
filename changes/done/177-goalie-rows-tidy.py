# changes/177-goalie-rows-tidy.py - Goalies page: photo in its own column on the outside edge, four fixed lines per goalie so both sides line up

NEW_CSS = r'''  /* change 177 (install.py) */
  .gx-gs.gx-g177 { display: grid; grid-template-columns: calc(30px * var(--gx-fs, 1)) minmax(0,1fr); column-gap: 8px; align-items: start; }
  .gx-gs.r.gx-g177 { grid-template-columns: minmax(0,1fr) calc(30px * var(--gx-fs, 1)); }
  .gx-g177 .fc { display: flex; justify-content: center; padding-top: 1px; }
  .gx-g177 .fc .gx-fb152 { border-radius: 6px; background: var(--card2); }
  .gx-g177 .tx { min-width: 0; }
  .gx-g177 .ln { height: 18px; line-height: 18px; font-size: 12px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; color: var(--mute); }
  .gx-g177 .ln.n { display: flex; gap: 5px; align-items: baseline; height: 20px; line-height: 20px; font-size: 14px; color: var(--ink); }
  .gx-g177.r .ln.n { justify-content: flex-end; }
  .gx-g177 .ln.n .nm { min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  .gx-g177 .ln.n .tc { flex: none; font-size: 11px; color: var(--mute); }
  .gx-g177 .ln .gx-pill { font-size: 10.5px; padding: 0 6px; line-height: 16px; display: inline-block; }
  .gx-g177 .ln.sw button { font-size: 12px; }
  @media (max-width: 640px) {
    .gx-gm2.gx-r177 { grid-template-columns: minmax(0,1fr) 50px minmax(0,1fr); gap: 4px; }
    .gx-gm2.gx-r177 .md { font-size: 11.5px; }
    .gx-gs.gx-g177 { grid-template-columns: calc(26px * var(--gx-fs, 1)) minmax(0,1fr); column-gap: 6px; padding: 5px 4px; }
    .gx-gs.r.gx-g177 { grid-template-columns: minmax(0,1fr) calc(26px * var(--gx-fs, 1)); }
    .gx-g177 .ln.n { font-size: 13.5px; }
  }
  .gx-gm2.gx-r177 .md { align-self: center; font-size: 12px; color: var(--mute); text-align: center; line-height: 18px; white-space: nowrap; }
</style>'''

OLD_CELL = r'''      <div className={"gx-gs" + (r ? " r" : "") + (me ? " me" : "")}>
        <div className="truncate" style={{ fontWeight: me ? 600 : 400 }}>
          {r ? null : <span style={{ marginRight: 6 }}><GxFace p={x.p} t={x.t} size={18} /></span>}{nm} <span className="text-xs text-slate-500">{x.t}</span>{r ? <span style={{ marginLeft: 6 }}><GxFace p={x.p} t={x.t} size={18} /></span> : null}
        </div>
        <div className="gx-gl2">
          <span style={{ color: x.col }}>{x.status}</span>{tag(x.p)}{x.val ? <span className="text-slate-500">{x.val}</span> : null}
          {dr ? <button type="button" className="text-blue-600" onClick={(e) => { e.stopPropagation(); setSim({ add: x.p.id, drop: dr.id }); }}>{"swap for " + lastN(dr.n)}</button> : null}
        </div>
      </div>'''

NEW_CELL = r'''      <div className={"gx-gs gx-g177" + (r ? " r" : "") + (me ? " me" : "")}>
        {/* change 177: photo column on the outside, four fixed lines */}
        {r ? null : <div className="fc"><GxFace p={x.p} t={x.t} size={30} /></div>}
        <div className="tx">
          <div className="ln n" style={{ fontWeight: me ? 600 : 400 }}><span className="nm"><span className="m-hide" style={{ display: "inline" }}>{nm}</span><span className="m-inl">{sn177}</span></span></div>
          <div className="ln" style={{ color: x.col }}>{x.status || "\u00a0"}</div>
          <div className="ln">{tag(x.p) || "\u00a0"}</div>
          <div className="ln">{[x.t, x.val].filter(Boolean).join(" \u00b7 ")}</div>
          {dr ? <div className="ln sw"><button type="button" className="text-blue-600" onClick={(e) => { e.stopPropagation(); setSim({ add: x.p.id, drop: dr.id }); }}>{"swap for " + lastN(dr.n)}</button></div> : null}
        </div>
        {r ? <div className="fc"><GxFace p={x.p} t={x.t} size={30} /></div> : null}
      </div>'''

OLD_ROW = r'''          <div key={gm.home + i} className="gx-gm2" style={i ? null : { borderTop: 0 }}>
            {cell(gm.a, false)}
            <div className="text-xs text-slate-500 text-center" style={{ alignSelf: "center" }}>{mid(gm)}</div>'''

NEW_ROW = r'''          <div key={gm.home + i} className="gx-gm2 gx-r177" style={i ? null : { borderTop: 0 }}>
            {cell(gm.a, false)}
            <div className="md">{mid(gm)}</div>'''


OLD_NM = r'''    const nm = x.p ? <PN p={x.p} className="" /> : x.name ?'''
NEW_NM = r'''    // change 177: short name for the phone, e.g. "A. Soderblom", still opens the player
    const fn177 = x.p ? x.p.n : x.name || "", sp177 = fn177.indexOf(" ");
    const sx177 = sp177 > 0 ? fn177[0] + ". " + fn177.slice(sp177 + 1) : fn177;
    const sn177 = x.p ? <a href={gxPHref(x.p)} onClick={(e) => { e.stopPropagation(); if (gxNewTab(e)) return; e.preventDefault(); if (window.__NAV) window.__NAV.player(x.p); }}>{sx177}</a> : sx177 ? <span>{sx177}</span> : <span className="text-slate-500">{"-"}</span>;
    const nm = x.p ? <PN p={x.p} className="" /> : x.name ?'''


def change(t):
    t = lit(t, "177: styles", "</style>", NEW_CSS, "change 177 (install.py)")
    t = lit(t, "177: saves as SV", '(x.sv || 0) + " saves"', '(x.sv || 0) + " SV"', '(x.sv || 0) + " SV"')
    t = lit(t, "177: short name", OLD_NM, NEW_NM, "change 177: short name for the phone")
    t = lit(t, "177: goalie cell", OLD_CELL, NEW_CELL, "change 177: photo column on the outside")
    t = lit(t, "177: goalie row", OLD_ROW, NEW_ROW, "gx-gm2 gx-r177")
    return t


edit(APP, change)
