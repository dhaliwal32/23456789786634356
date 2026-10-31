# changes/174-watch-button.py - Watch button on every game (NHL scores game view); link set in Setup > Display, blank = that game's ESPN Gamecast

NEW_CSS = r'''  /* change 174 (install.py) */
  .gx-wt174 { display: flex; align-items: center; justify-content: center; gap: 8px; margin: 0 16px 10px; padding: 10px; border-radius: 10px; background: var(--card2, var(--bg)); border: 1px solid var(--line); color: var(--ink); font-size: 14px; font-weight: 600; text-decoration: none; }
  .gx-wt174 svg { width: 14px; height: 14px; fill: currentColor; }
  .gx-wt174:active { transform: scale(.98); }
  .gx-wi174 { flex: 1 1 220px; min-width: 0; }
</style>'''

HELPERS = r'''// ---------- change 174: Watch button link (install.py) ----------
function gxWatchUrl174(id) {
  let u = "";
  try { u = String(uiGet().gxWatch174 || "").trim(); } catch (e) {}
  if (u && !/^https?:\/\//i.test(u)) u = "https://" + u;
  return u || "https://www.espn.com/nhl/game/_/gameId/" + id;
}
function GxWatchSel174() {
  const [v, setV] = useState(() => { try { return uiGet().gxWatch174 || ""; } catch (e) { return ""; } });
  return <input type="url" inputMode="url" className={inp + " gx-wi174"} placeholder="Blank = ESPN Gamecast for that game" value={v} onChange={(e) => { setV(e.target.value); uiSet("gxWatch174", e.target.value.trim()); }} />;
}
'''

OLD_SET = '<div className="gx-sr"><span>Favourite team (Lines)</span><GxFavSel112 /></div>'
NEW_SET = OLD_SET + '\n    <div className="gx-sr"><span>Watch link</span><GxWatchSel174 /></div>'

OLD_GV = '<div className="gx-gv141"><div className="tms">{rows2(g)}</div><div className={"st" + (live(g) ? " lv" : "")}>{status(g)}</div></div>'
NEW_GV = OLD_GV + '\n        <a className="gx-wt174" href={gxWatchUrl174(gid)} target="_blank" rel="noopener noreferrer"><svg viewBox="0 0 10 10" aria-hidden="true"><path d="M2 1 L9 5 L2 9 Z" /></svg>Watch</a>'

def change(t):
    t = lit(t, "174: styles", "</style>", NEW_CSS, "change 174 (install.py)")
    t = lit(t, "174: helpers", ROOT, HELPERS + ROOT, "change 174: Watch button link")
    t = lit(t, "174: setup row", OLD_SET, NEW_SET, "<GxWatchSel174 />")
    t = lit(t, "174: watch button", OLD_GV, NEW_GV, 'className="gx-wt174"')
    return t

edit(APP, change)
