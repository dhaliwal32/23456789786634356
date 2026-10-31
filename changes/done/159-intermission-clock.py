# changes/159-intermission-clock.py - during an intermission, show a clock counting down to the next period ("1st INT 09:23"), like NHL.com, on Matchup rows and the NHL scores

HELPERS = r'''// ---------- change 159: intermission countdown (install.py) ----------
const GX_INT159 = 18 * 60; /* NHL intermissions are 18 minutes */
function gxIntEnd159(g) {
  const n = ((g || {}).periodDescriptor || {}).number || 1, key = "gx159:" + g.id + ":" + n;
  const c = (typeof G132 !== "undefined" && G132.sum[g.id]) || null, js = c && c.js;
  let end = 0;
  ((js && js.plays) || []).forEach((p) => { if (((p.period || {}).number || 0) === n) { const w = Date.parse(p.wallclock || ""); if (!isNaN(w) && w > end) end = w; } });
  let seen = 0;
  try { seen = +localStorage.getItem(key) || 0; if (!seen) { seen = Date.now(); localStorage.setItem(key, String(seen)); } } catch (e) { seen = (window.__INT159 = window.__INT159 || {})[key] || (window.__INT159[key] = Date.now()); }
  return end && end <= seen + 60e3 ? end : seen;
}
function gxIntLeft159(g) {
  if (!g || !(g.clock || {}).inIntermission) return null;
  return Math.max(0, GX_INT159 - Math.floor((Date.now() - gxIntEnd159(g)) / 1000));
}
const gxIntFmt159 = (sec) => String(Math.floor(sec / 60)).padStart(2, "0") + ":" + String(sec % 60).padStart(2, "0");
function gxIntG159(g) {
  const per = gxPer131(g.periodDescriptor), left = gxIntLeft159(g);
  return per + " INT" + (left ? " " + gxIntFmt159(left) : "");
}
function gxIntT159(team, per) {
  const g = (((window.__NHLNOW || {}).games) || []).find((x) => (x.clock || {}).inIntermission && (gxAb131((x.homeTeam || {}).abbrev) === team || gxAb131((x.awayTeam || {}).abbrev) === team));
  return g ? gxIntG159(g) : per + " INT";
}
// redraws every second while "on" (an intermission clock is showing)
function useTick159(on) {
  const [, t] = useState(0);
  useEffect(() => { if (!on) return undefined; const id = setInterval(() => t((x) => x + 1), 1000); return () => clearInterval(id); }, [on]);
}
const gxAnyInt159 = () => (((window.__NHLNOW || {}).games) || []).some((g) => (g.clock || {}).inIntermission);
'''

NEW_CSS = r'''  /* change 159 (install.py) */
  .gx-sd141 .gm .st { width: 96px; }
</style>'''

def change(t):
    t = lit(t, "159: styles", "</style>", NEW_CSS, "change 159 (install.py)")
    t = lit(t, "159: helpers", ROOT, HELPERS + ROOT, "change 159: intermission countdown")
    t = lit(t, "159: matchup rows tick",
            "const LiveTag = ({ st, t, dt, e157 }) => {",
            "const LiveTag = ({ st, t, dt, e157 }) => {\n  useTick159(st === \"L\" && !!(t && dt && (gScore(t, dt) || {}).int)); /* gx159 */",
            "useTick159(st === \"L\" && !!(t && dt")
    t = lit(t, "159: matchup rows text",
            'sc.int ? " · " + sc.per + " int."',
            'sc.int ? " · " + gxIntT159(t, sc.per)',
            "gxIntT159(t, sc.per)")
    t = lit(t, "159: scoreboards text",
            'gxPer131(g.periodDescriptor) + " int."',
            'gxIntG159(g)',
            None, count=2)
    t = lit(t, "159: scores tick",
            "function GxNhl141({ s, a, b, tA, tB, side }) {\n  const [open, setOpen] = useState(false);",
            "function GxNhl141({ s, a, b, tA, tB, side }) {\n  useTick159(gxAnyInt159()); /* gx159 */\n  const [open, setOpen] = useState(false);",
            "useTick159(gxAnyInt159()); /* gx159 */")
    return t

edit(APP, change)
