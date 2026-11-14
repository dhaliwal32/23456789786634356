# changes/266-one-clock-better-tracker.py - one shared game clock (game card, scoreboards and live tracker show the same ticking time) and a richer live tracker (ripple on each play, puck path, shots, recent plays list)

NEW_CSS = r'''  /* change 266 (install.py) */
  .gx-tk264 .sg266 { font-size: 12px; font-weight: 600; color: var(--mute); letter-spacing: 0; font-variant-numeric: tabular-nums; white-space: nowrap; }
  .gx-tk264 .hd264 > span:first-child { white-space: nowrap; }
  .gx-tk264 .rp266 { transform-box: fill-box; transform-origin: center; animation: gx266rp 1.1s ease-out 1 both; }
  @keyframes gx266rp { from { transform: scale(.6); opacity: .95; } to { transform: scale(3.2); opacity: 0; } }
  .gx-tk264 .ls266 { margin-top: 8px; border-top: 1px solid var(--line); }
  .gx-tk264 .ls266 .r266 { display: grid; grid-template-columns: 44px 42px 1fr; align-items: center; gap: 8px; height: 32px; border-bottom: 1px solid var(--line); font-size: 12.5px; }
  .gx-tk264 .ls266 .r266 .tm266 { color: var(--mute); font-variant-numeric: tabular-nums; }
  .gx-tk264 .ls266 .r266 .tg266 { font-size: 11px; font-weight: 800; text-align: center; padding: 2px 0; border-radius: 5px; }
  .gx-tk264 .ls266 .r266 .tx266 { min-width: 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; color: var(--mute); }
  .gx-tk264 .ls266 .r266 .tx266 b { color: var(--ink); font-weight: 700; margin-right: 6px; }
  .gx-tk264 .ls266 .r266.nw266 { animation: gx266in .5s ease-out 1 both; }
  .gx-tk264 .ls266 .r266.gl266 .tx266 b { color: var(--accent); }
  @keyframes gx266in { from { opacity: 0; transform: translateY(-6px); } to { opacity: 1; transform: none; } }
  @media (prefers-reduced-motion: reduce) { .gx-tk264 .rp266, .gx-tk264 .ls266 .r266.nw266 { animation: none; } }
</style>'''

HELPERS = r'''// ---------- change 266: one shared game clock and a richer live tracker (install.py) ----------
// Two ESPN feeds give the clock (scoreboard and game summary) and they lag by different amounts.
// Each feed's last value is kept with the moment it changed; each counts down by itself while it keeps changing (8 s rule from 265),
// and every place shows the feed that is furthest along (later period, then less time left).
window.__CK266 = window.__CK266 || {};
function gxCkIn266(id, src, per, txt) {
  const sec = gxSec265(txt); if (!id || sec == null || !per) return;
  const o = window.__CK266[id] = window.__CK266[id] || {}, s = o[src];
  if (!s || s.raw !== txt || s.per !== per) o[src] = { per, raw: txt, sec, chg: Date.now() };
}
function gxCkFeed266(id) {
  const sm = ((G132.sum || {})[id] || {}).js;
  if (sm) { const st = gxHead132(sm).status || {}; gxCkIn266(id, "sm", st.period || 0, st.displayClock || ""); }
  const g = ((window.__NHLNOW || {}).games || []).find((x) => x.id === id);
  if (g && (g.gameState === "LIVE" || g.gameState === "CRIT")) gxCkIn266(id, "sb", ((g.periodDescriptor || {}).number) || 0, ((g.clock || {}).timeRemaining) || "");
}
function gxCkNow266(id, brk) {
  const o = window.__CK266[id] || {}, now = Date.now();
  let best = null;
  Object.keys(o).forEach((k) => {
    const s = o[k], el = (now - s.chg) / 1000;
    const v = !brk && s.sec > 0 && el < 8 ? Math.max(0, Math.ceil(s.sec - el)) : s.sec;
    if (!best || s.per > best.per || (s.per === best.per && v < best.sec)) best = { per: s.per, sec: v };
  });
  return best;
}
function useTick266(ms) { const [, t] = useState(0); useEffect(() => { const i = setInterval(() => t((x) => x + 1), ms); return () => clearInterval(i); }, [ms]); }
// game card and scoreboard clock ("3rd - 5:39"), live and not in intermission
function GxGClk266({ g }) {
  useTick266(250);
  gxCkFeed266(g.id);
  const b = gxCkNow266(g.id, false);
  return <>{gxPer131(g.periodDescriptor) + " - " + (b && b.per === (((g.periodDescriptor || {}).number) || 0) ? gxMmss132(b.sec) : ((g.clock || {}).timeRemaining || ""))}</>;
}
// tracker clock chip, same shared clock
function GxClk266({ id, per, clk }) {
  useTick266(250);
  gxCkIn266(id, "sm", per, clk);
  gxCkFeed266(id);
  const ty = ((gxHead132(((G132.sum || {})[id] || {}).js).status || {}).type) || {};
  const brk = ty.name === "STATUS_END_PERIOD" || ty.name === "STATUS_INTERMISSION" || /intermission|end of/i.test(ty.detail || "");
  const b = gxCkNow266(id, brk) || { per, sec: gxSec265(clk) };
  if (!b.per) return null;
  const pl = b.per > 3 ? "OT" : "P" + b.per;
  return <span className="ck264" data-gx="266">{brk ? pl + (b.per <= 3 ? " INT" : " END") : pl + " " + (b.sec == null ? clk : gxMmss132(b.sec))}</span>;
}
// a play's time as time left in its period (ESPN play clocks count time played)
const gxPlayLeft266 = (q) => { const s = gxSec265(q.clk); if (s == null) return ""; const L = (q.per > 3 ? 300 : 1200) - s; return L >= 0 ? gxMmss132(L) : q.clk; };
function gxSog266(d, t) { return d.ev.filter((q) => q.t === t && (q.goal || /^(shot|save)/i.test(q.ty))).length; }
function GxTkList266({ d, k, col, A, H }) {
  const seen = React.useRef(null);
  const rows = d.ev.slice(Math.max(0, k - 5), k).reverse();
  const first = seen.current;
  useEffect(() => { seen.current = rows.length ? rows[0].k : null; });
  if (!rows.length) return null;
  return (
    <div className="ls266" data-gx="266l">
      {rows.map((q, j) => {
        const c = col(q.t);
        return (
          <div key={q.k} className={"r266" + (j === 0 && first != null && first !== q.k ? " nw266" : "") + (q.goal ? " gl266" : "")}>
            <span className="tm266">{gxPlayLeft266(q)}</span>
            <span className="tg266" style={{ background: c ? c.f : "var(--line)", color: c ? c.t : "var(--ink)" }}>{q.t === "h" ? H : q.t === "a" ? A : "NHL"}</span>
            <span className="tx266"><b>{q.goal ? "GOAL" : q.ty || "Play"}</b>{q.tx}</span>
          </div>
        );
      })}
    </div>
  );
}
'''

OLD_ST = 'gxPer131(g.periodDescriptor) + " - " + ((g.clock || {}).timeRemaining || "")'
NEW_ST = '<GxGClk266 g={g} />'

def change(t):
    t = lit(t, "266: styles", "</style>", NEW_CSS, "change 266 (install.py)")
    t = lit(t, "266: helpers", ROOT, HELPERS + ROOT, "change 266: one shared game clock")
    # every live clock on the scoreboards, game card and player screen game card uses the shared clock
    if NEW_ST not in t:
        n = t.count(OLD_ST)
        if n != 3: fail("266: expected 3 game clocks, found %d" % n)
        t = t.replace(OLD_ST, NEW_ST)
    t = lit(t, "266: tracker clock", "<GxClk265 id={id} per={d.per} clk={d.clk} />", "<GxClk266 id={id} per={d.per} clk={d.clk} />", "<GxClk266 id={id} per={d.per} clk={d.clk} />")
    t = lit(t, "266: shots on goal in the header", '<div className="hd264"><span>Live tracker</span>',
            '<div className="hd264"><span>Live tracker</span><small className="sg266" data-gx="266s">{A} {gxSog266(d, "a")} SOG {gxSog266(d, "h")} {H}</small>', 'data-gx="266s"')
    t = lit(t, "266: puck path and ripple", "          {trail.map((q, j) => <circle",
            '          {p && trail.length ? <polyline points={[...trail].reverse().concat([p]).map((q) => q.x + "," + -q.y).join(" ")} fill="none" stroke={zc ? zc.f : "#9a9a9a"} strokeWidth="0.5" strokeDasharray="1.2 1.4" opacity="0.6" data-gx="266p" /> : null}\n'
            '          {p ? <g key={"rp" + p.k} transform={"translate(" + p.x + " " + -p.y + ")"}><circle className="rp266" r="3" fill="none" stroke={zc ? zc.f : "#ffffff"} strokeWidth="0.7" /></g> : null}\n'
            "          {trail.map((q, j) => <circle", 'data-gx="266p"')
    t = lit(t, "266: play time on the card", '<span>{e ? e.tx : ""}</span>', '<span>{e ? (gxPlayLeft266(e) ? gxPlayLeft266(e) + "  " : "") + e.tx : ""}</span>', "gxPlayLeft266(e) + ")
    t = lit(t, "266: recent plays list", '          <span>{e ? (gxPlayLeft266(e) ? gxPlayLeft266(e) + "  " : "") + e.tx : ""}</span>\n        </div>\n      </div>\n',
            '          <span>{e ? (gxPlayLeft266(e) ? gxPlayLeft266(e) + "  " : "") + e.tx : ""}</span>\n        </div>\n      </div>\n      <GxTkList266 d={d} k={k} col={col} A={A} H={H} />\n',
            "<GxTkList266 d={d} k={k} col={col} A={A} H={H} />")
    return t

edit(APP, change)
