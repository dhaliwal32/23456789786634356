# changes/237-lines-spotlight.py - Lines: available players (free agents and waivers) get a spotlight on their stall instead of the FA / WAIVERS word; every team shown at the top

NEW_CSS = r'''  /* change 237 (install.py): spotlight on available players */
  .rm236 .gx-fg224.gx-lt227.fa { box-shadow: inset 0 10px 14px -10px rgba(0,0,0,.4), 0 0 0 1px rgba(255,246,214,.35), 0 0 22px 2px rgba(255,240,200,.28), 0 4px 8px rgba(0,0,0,.35); }
  .rm236 .gx-fg224.gx-lt227.fa::before { background: #fff8e6; box-shadow: 0 0 8px 2px #fff3d1, 0 0 20px 6px rgba(255,240,200,.55); }
  .rm236 .gx-fg224.gx-lt227::after { content: ""; position: absolute; inset: 0; border-radius: inherit; pointer-events: none; z-index: 0; background: rgba(0,0,0,.22); }
  .rm236 .gx-fg224.gx-lt227.fa::after { background: radial-gradient(ellipse 62% 20% at 50% 93%, rgba(255,244,214,.55), transparent 72%), linear-gradient(180deg, rgba(255,244,214,.6), rgba(255,244,214,.18) 70%, rgba(255,244,214,.08));
    clip-path: polygon(30% 0, 70% 0, 100% 100%, 0 100%); }
  .rm236 .gx-fg224.gx-lt227 > * { position: relative; z-index: 1; }
  .rm236 .gx-fg224.gx-lt227.fa .ow227 span:first-child:empty { display: none; }
  .rm236 .gx-fg224.gx-lt227 .ow227 .gx-wv218 { margin: 0 2px 0 0; }
  .gx-ln111 .at237 { display: grid; grid-template-columns: repeat(16, minmax(0, 1fr)); gap: 4px; margin-top: 10px; }
  .gx-ln111 .at237 button { display: flex; flex-direction: column; align-items: center; gap: 2px; padding: 5px 0 4px; border-radius: 10px; font-size: 9.5px; font-weight: 600; color: var(--mute); letter-spacing: .02em; }
  .gx-ln111 .at237 button.on { background: var(--card2); color: var(--ink); box-shadow: inset 0 0 0 1px var(--line2); }
  @media (max-width: 640px) { .gx-ln111 .at237 { grid-template-columns: repeat(8, minmax(0, 1fr)); gap: 3px; } }
</style>'''

def change(t):
    t = lit(t, "237: styles", "</style>", NEW_CSS, "change 237 (install.py): spotlight")
    t = lit(t, "237: no FA word on Lines",
            'fa ? (p.wv ? "WAIVERS" : "FA") : ((teamName(s, p.ft)',
            'fa ? (p.wv ? <i className="gx-wv218" title="On waivers" data-gx="237" /> : "") : ((teamName(s, p.ft)',
            'title="On waivers" data-gx="237"')
    t = lit(t, "237: all teams at the top",
            '{recent.length ? <div className="rec">{recent.map((c) => <button key={c} type="button" onClick={() => pick(c)}><TeamLogo t={c} size={18} />{c}</button>)}</div> : null}',
            '<div className="at237" data-gx="237a">{teams.map((c) => <button key={c} type="button" className={c === t ? "on" : ""} aria-label={nameOf(c)} onClick={() => pick(c)}><TeamLogo t={c} size={26} />{c}</button>)}</div>',
            'data-gx="237a"')
    return t

edit(APP, change)
