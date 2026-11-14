# changes/265-tracker-clock-ticks.py - live tracker clock counts down every second between ESPN updates, and stops at whistles and intermissions

HELPERS = r'''// ---------- change 265: live tracker clock that ticks every second (install.py) ----------
// ESPN's clock only changes every few seconds. Between updates the app counts down by itself from the last value.
// If ESPN's clock has not moved for 8 s, the clock is stopped (whistle), so the app shows ESPN's value and stops counting.
const gxSec265 = (c) => { const m = String(c || "").match(/^(\d+):(\d{1,2})/); return m ? +m[1] * 60 + +m[2] : null; };
function GxClk265({ id, per, clk }) {
  const r = React.useRef({ v: null, sec: null, chg: 0 });
  const [, tick] = useState(0);
  const now = Date.now();
  if (clk !== r.current.v) r.current = { v: clk, sec: gxSec265(clk), chg: now };
  useEffect(() => { const t = setInterval(() => tick((x) => x + 1), 250); return () => clearInterval(t); }, []);
  const ty = ((gxHead132(((G132.sum || {})[id] || {}).js).status || {}).type) || {};
  const brk = ty.name === "STATUS_END_PERIOD" || ty.name === "STATUS_INTERMISSION" || /intermission|end of/i.test(ty.detail || "");
  const R = r.current, el = (now - R.chg) / 1000;
  let sec = R.sec;
  if (sec != null && !brk && sec > 0 && el < 8) sec = Math.max(0, Math.ceil(sec - el));
  if (!per) return null;
  const pl = per > 3 ? "OT" : "P" + per;
  const txt = brk ? (per <= 3 ? pl + " INT" : pl + " END") : sec == null ? pl + " " + (clk || "") : pl + " " + gxMmss132(sec);
  return <span className="ck264" data-gx="265">{txt}</span>;
}
'''

def change(t):
    t = lit(t, "265: helpers", ROOT, HELPERS + ROOT, "change 265: live tracker clock")
    t = lit(t, "265: use it", '{clock ? <span className="ck264">{clock}</span> : null}', '<GxClk265 id={id} per={d.per} clk={d.clk} />', "<GxClk265 id={id} per={d.per} clk={d.clk} />")
    return t

edit(APP, change)
