# changes/227-lines-cards.py - Lines: clean player cards with photos instead of the drawn players, plain board instead of the drawn rink

NEW_CSS = r'''  /* change 227 (install.py): Lines player cards */
  .gx-rk111 { border-radius: 16px; border: 1px solid var(--line); background: var(--card); padding: 12px 10px 10px; }
  .gx-rk111 .ice { display: none; }
  .gx-rk111 .logo { opacity: .05; }
  .gx-rk111 .row { margin: 0 0 8px; }
  .gx-rk111 .sp { height: 6px; }
  .gx-rk111 .row .lb { font-size: 10.5px; }
  .gx-fg224.gx-lt227 { padding: 8px 4px 7px; border-radius: 12px; border: 1px solid var(--line); background: var(--card2); justify-content: flex-start; gap: 0; }
  .gx-fg224.gx-lt227.me { border-color: var(--accent); box-shadow: inset 0 0 0 1px var(--accent); }
  .gx-fg224.gx-lt227.fa { border-color: var(--good); }
  .gx-fg224.gx-lt227 .md { width: 54px; height: 54px; border-radius: 10px; overflow: hidden; background: var(--card3, var(--card)); display: flex; align-items: flex-end; justify-content: center; }
  .gx-fg224.gx-lt227 .md img { width: 100%; height: 100%; object-fit: cover; object-position: 50% 10%; display: block; }
  .gx-fg224.gx-lt227 .md .no227 { align-self: center; font-size: 22px; font-weight: 700; color: var(--mute); font-variant-numeric: tabular-nums; }
  .gx-fg224.gx-lt227 .nm { margin-top: 6px; font-size: 12.5px; font-weight: 600; }
  .gx-fg224.gx-lt227 .sb227 { font-size: 10.5px; color: var(--mute); margin-top: 1px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 100%; }
  .gx-fg224.gx-lt227 .ow227 { margin-top: 4px; height: 16px; display: flex; align-items: center; gap: 4px; font-size: 10px; font-weight: 600; color: var(--mute); letter-spacing: .02em; white-space: nowrap; overflow: hidden; max-width: 100%; }
  .gx-fg224.gx-lt227 .ow227 b { color: var(--ink); font-weight: 600; font-variant-numeric: tabular-nums; }
  .gx-fg224.gx-lt227.me .ow227 { color: var(--ink); }
  .gx-fg224.gx-lt227.fa .ow227 { color: var(--good); }
  .gx-fg224.gx-lt227.empty { border-style: dashed; background: none; min-height: 112px; }
  @media (max-width: 640px) { .gx-fg224.gx-lt227 .md { width: 48px; height: 48px; } .gx-fg224.gx-lt227 .nm { font-size: 12px; } }
  /* the zoomed player shows his photo, no spinning */
  .gx-lz224 .hint { display: none; }
  .gx-lz224 .sp.ph227 { transform: none !important; transition: none !important; display: flex; align-items: flex-end; justify-content: center; height: 100%; }
  .gx-lz224 .sp.ph227 img { height: 100%; max-height: 230px; width: auto; display: block; filter: drop-shadow(0 8px 18px rgba(0,0,0,.45)); }
  .gx-lz224 .sp.ph227 .no227 { font-size: 96px; font-weight: 700; color: rgba(255,255,255,.9); line-height: 1; margin-bottom: 40px; }
</style>'''

HELPERS = r'''// ---------- change 227: Lines player cards with photos (install.py) ----------
function GxLnPic227({ p, no, big }) {
  const [bad, setBad] = useState(false);
  const id = p ? String(p.id || "").replace(/^e/, "") : "";
  if (!id || bad) return <span className="no227">{no != null ? no : "\u2013"}</span>;
  return <img src={"https://a.espncdn.com/i/headshots/nhl/players/full/" + id + ".png"} alt="" loading="lazy" onError={() => setBad(true)} />;
}
'''

CARD_OLD = '''<div className="md"><GxSkater224 t={p ? p.t : t} name={last} no={((T && T.no) || {})[n]} side="back" goalie={isG} /><span className={"rg" + (mine ? " me" : fa ? " fa" : "")}></span></div>
          <span className="nm">{last}</span>'''
CARD_NEW = '''<div className="md"><GxLnPic227 p={p} no={((T && T.no) || {})[n]} /></div>
          <span className="nm">{last}</span>
          <span className="sb227">{(((T && T.no) || {})[n] != null ? "#" + ((T && T.no) || {})[n] + " \\u00b7 " : "") + (isG ? "G" : String(df[n] || (p ? p.p : "")).replace(/[0-9]/g, "").toUpperCase())}</span>
          <span className="ow227">{p ? <><span>{mine ? "YOURS" : fa ? (p.wv ? "WAIVERS" : "FA") : ((teamName(s, p.ft) || "").replace(/[^A-Za-z0-9' ]/g, " ").trim().split(/\\s+/)[0] || "").slice(0, 9)}</span><b>{f1(gxPgAvg(p, s.blend))}</b></> : null}</span>'''

ZOOM_OLD = '''              <div ref={sp} className="sp">
                <GxSkater224 t={p ? p.t : t} name={last} no={no} side="back" goalie={isG} />
                <GxSkater224 t={p ? p.t : t} name={last} no={no} side="front" goalie={isG} className="fr" />
              </div>'''
ZOOM_NEW = '''              <div ref={sp} className="sp ph227"><GxLnPic227 p={p} no={no} big /></div>'''

def change(t):
    t = lit(t, "227: styles", "</style>", NEW_CSS, "change 227 (install.py): Lines player cards")
    t = lit(t, "227: helpers", ROOT, HELPERS + ROOT, "change 227: Lines player cards with photos")
    t = lit(t, "227: card", CARD_OLD, CARD_NEW, '<GxLnPic227 p={p} no={((T && T.no) || {})[n]} />')
    t = lit(t, "227: card class", '<button key={n + i} type="button" className="gx-fg224" aria-label={n}', '<button key={n + i} type="button" className={"gx-fg224 gx-lt227" + (mine ? " me" : fa ? " fa" : "")} aria-label={n}', '"gx-fg224 gx-lt227"')
    t = lit(t, "227: empty card", '<div key={"e" + i} className="gx-fg224 empty"><div className="md"></div></div>', '<div key={"e" + i} className="gx-fg224 gx-lt227 empty"></div>', 'className="gx-fg224 gx-lt227 empty"')
    t = lit(t, "227: zoom photo", ZOOM_OLD, ZOOM_NEW, 'className="sp ph227"')
    return t

edit(APP, change)
