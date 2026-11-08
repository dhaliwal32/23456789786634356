# changes/211-watch-opens-safari.py - Watch buttons open in real Safari when the app runs from the home screen

HELPERS = r'''// ---------- change 211: Watch opens in Safari from the home screen app (install.py) ----------
function gxHome211() {
  try {
    const ios = /iPhone|iPad|iPod/.test(navigator.userAgent || "") || (navigator.platform === "MacIntel" && navigator.maxTouchPoints > 1);
    const st = window.navigator.standalone === true || (window.matchMedia && window.matchMedia("(display-mode: standalone)").matches);
    return ios && st;
  } catch (e) { return false; }
}
function gxWatchGo211(e) {
  e.stopPropagation();
  if (!gxHome211()) return;
  const u = String((e.currentTarget && e.currentTarget.href) || "");
  if (!/^https?:\/\//i.test(u)) return;
  e.preventDefault();
  window.location.href = "x-safari-" + u;
}
'''

OLD179 = 'className="wt179" href={gxWatchUrl175(g, g.id)} target="_blank" rel="noopener noreferrer" onClick={(e) => e.stopPropagation()}'
NEW179 = 'className="wt179" href={gxWatchUrl175(g, g.id)} target="_blank" rel="noopener noreferrer" onClick={gxWatchGo211}'
OLD181 = 'className="wt181" href={gxWatchUrl175(g, g.id)} target="_blank" rel="noopener noreferrer" onClick={(e) => e.stopPropagation()}'
NEW181 = 'className="wt181" href={gxWatchUrl175(g, g.id)} target="_blank" rel="noopener noreferrer" onClick={gxWatchGo211}'

def change(t):
    t = lit(t, "211: helpers", ROOT, HELPERS + ROOT, "change 211: Watch opens in Safari")
    t = lit(t, "211: phone Watch", OLD179, NEW179, 'className="wt179" href={gxWatchUrl175(g, g.id)} target="_blank" rel="noopener noreferrer" onClick={gxWatchGo211}')
    t = lit(t, "211: laptop Watch", OLD181, NEW181, 'className="wt181" href={gxWatchUrl175(g, g.id)} target="_blank" rel="noopener noreferrer" onClick={gxWatchGo211}')
    return t

edit(APP, change)
