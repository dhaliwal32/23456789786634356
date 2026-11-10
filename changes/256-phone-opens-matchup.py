# changes/256-phone-opens-matchup.py - on the phone, a fresh start of the app opens on Matchup (a refresh keeps the page you were on)

HELPERS = r'''// ---------- change 256: phone opens on Matchup (install.py) ----------
// runs once when the page loads, before the app reads the address; sessionStorage is empty only on a fresh start
// (home screen icon after the app was closed, or a new tab), so a refresh or the app's own reloads keep the page
(function gxStart256() {
  try {
    if (!(window.matchMedia && window.matchMedia("(max-width: 640px)").matches)) return;
    if (sessionStorage.getItem("gx256")) return;
    sessionStorage.setItem("gx256", "1");
    if (String(window.location.hash || "").indexOf("&p=") >= 0) return; // a link to a player opens that player
    window.history.replaceState(null, "", window.location.pathname + window.location.search + "#matchup");
  } catch (e) {}
})();
'''

def change(t):
    t = lit(t, "256: start on Matchup", ROOT, HELPERS + ROOT, "change 256: phone opens on Matchup")
    return t

edit(APP, change)
