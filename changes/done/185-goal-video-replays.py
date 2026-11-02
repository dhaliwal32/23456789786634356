# changes/185-goal-video-replays.py - Goal video replays inside the app: ESPN's game summary lists a video clip for most goals (plain mp4); each goal gets its clip, the goal button says "Video and Visualizer", and the Goal Visualizer box has Visualizer / Video buttons at the top with the video playing right there

NEW_CSS = r'''  /* change 185 (install.py) */
  .gx-v184 .sg185 { display: flex; justify-content: center; gap: 4px; margin: 8px auto 2px; padding: 3px; width: max-content; border-radius: 99px; background: #dcdcdc; }
  .gx-v184 .sg185 button { height: 30px; padding: 0 16px; border-radius: 99px; font-size: 13px; font-weight: 700; color: #555555; display: inline-flex; align-items: center; gap: 6px; transition: background .15s ease, color .15s ease; }
  .gx-v184 .sg185 button.on { background: #ffffff; color: #121212; box-shadow: 0 1px 2px rgba(0,0,0,.15); }
  .gx-v184 .sg185 button svg { width: 12px; height: 12px; }
  .gx-v184 .vd185 { padding: 8px 10px 10px; animation: gx184-dn .22s ease-out; }
  .gx-v184 .vd185 video { display: block; width: 100%; aspect-ratio: 16 / 9; background: #000000; border-radius: 8px; }
  .gx-v184 .vd185 small { display: block; margin-top: 6px; font-size: 12px; color: #666666; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
</style>'''

OLD_RET = r'''  return { summary: { scoring: Object.keys(by).sort((a, b) => a - b).map((k) => by[k]) } };'''
NEW_RET = r'''  try { /* change 185: the video clip for each goal, from ESPN's list of game videos */
    const vs = (((sm || {}).videos) || []).map((v) => ({ h: String(v.headline || ""), u: (((v.links || {}).source) || {}).href || "", p: (typeof v.thumbnail === "string" ? v.thumbnail : (v.thumbnail || {}).href) || "", d: +v.duration || 0 })).filter((v) => v.u && /\.mp4(\?|$)/i.test(v.u));
    const used = {};
    const esc = (w) => w.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    Object.keys(by).sort((a, b) => a - b).forEach((k) => by[k].goals.forEach((q) => {
      const nm = (q.name || {}).default || "", last = nm.split(" ").slice(1).join(" ");
      let i = nm ? vs.findIndex((v, j) => !used[j] && v.h.indexOf(nm) >= 0) : -1;
      if (i < 0 && last) i = vs.findIndex((v, j) => !used[j] && new RegExp("\\b" + esc(last) + "\\b").test(v.h));
      if (i >= 0) { used[i] = 1; q.vid185 = vs[i]; }
    }));
  } catch (er) {}
  return { summary: { scoring: Object.keys(by).sort((a, b) => a - b).map((k) => by[k]) } };'''

OLD_HOOK = r'''  const e165 = useEdge165(x, g, tm); /* gx165 */
  const cx = +x.cx, cy = +x.cy;
  if ((isNaN(cx) || isNaN(cy)) && !e165) return null;'''
NEW_HOOK = r'''  const e165 = useEdge165(x, g, tm); /* gx165 */
  const [vw185, setVw185] = useState(null); /* change 185: Visualizer or Video */
  const cx = +x.cx, cy = +x.cy;
  if ((isNaN(cx) || isNaN(cy)) && !e165 && !x.vid185) return null;
  const vw = x.vid185 ? vw185 || ((isNaN(cx) || isNaN(cy)) && !e165 ? "v" : "z") : "z";'''

OLD_HEAD = r'''  const head = <div className="hd184"><b>{gxNick141(A) + " @ " + gxNick141(H)}</b><small>{gxDate184(g.gameDate)}</small></div>;'''
NEW_HEAD = r'''  const head = <><div className="hd184"><b>{gxNick141(A) + " @ " + gxNick141(H)}</b><small>{gxDate184(g.gameDate)}</small></div>
    {x.vid185 ? <div className="sg185" data-gx="185">
      <button type="button" className={vw === "z" ? "on" : ""} disabled={(isNaN(cx) || isNaN(cy)) && !e165} onClick={() => setVw185("z")}>Visualizer</button>
      <button type="button" className={vw === "v" ? "on" : ""} onClick={() => setVw185("v")}>{GX_IC184.ply}Video</button>
    </div> : null}</>;
  if (vw === "v") return (
    <div className="gx-rk163 gx-v184" data-gx="184">
      {head}
      <div className="vd185"><video key={x.vid185.u} src={x.vid185.u} poster={x.vid185.p || undefined} controls playsInline autoPlay preload="metadata" />{x.vid185.h ? <small>{x.vid185.h}</small> : null}</div>
      <GxGvCard184 x={x} g={g} tm={tm} no={gxPdNo({ t: T, n: nm })} onPlay={null} />
    </div>
  );'''


def change(t):
    t = lit(t, "185: styles", "</style>", NEW_CSS, "change 185 (install.py)")
    t = lit(t, "185: match a video to each goal", OLD_RET, NEW_RET, "change 185: the video clip for each goal")
    t = lit(t, "185: Visualizer or Video", OLD_HOOK, NEW_HOOK, "change 185: Visualizer or Video")
    t = lit(t, "185: Video button and player", OLD_HEAD, NEW_HEAD, 'data-gx="185"')
    t = lit(t, "185: goal buttons show for video-only goals", "{r.x.cx != null ? (() =>", "{r.x.cx != null || r.x.vid185 ? (() =>", "r.x.cx != null || r.x.vid185", count=3)
    t = lit(t, "185: goal button label", ">Goal Visualizer <i className", ">{r.x.vid185 ? \"Video and Visualizer\" : \"Goal Visualizer\"} <i className", "Video and Visualizer", count=3)
    return t


edit(APP, change)
