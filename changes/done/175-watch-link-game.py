# changes/175-watch-link-game.py - Watch button adds the game to your Watch link: <your link>/live/nhl/<date>/<away>-<home>, e.g. live/nhl/2026-10-31/pit-mtl

HELPERS = r'''// ---------- change 175: Watch link with the game added (install.py) ----------
const GX_NHL175 = { LA: "lak", NJ: "njd", SJ: "sjs", TB: "tbl", UTAH: "uta" };
function gxWatchUrl175(g, id) {
  let u = "";
  try { u = String(uiGet().gxWatch174 || "").trim(); } catch (e) {}
  if (!u) return gxWatchUrl174(id);
  if (!/^https?:\/\//i.test(u)) u = "https://" + u;
  const c = (t) => { const a = String(gxAb131((t || {}).abbrev) || "").toUpperCase(); return GX_NHL175[a] || a.toLowerCase(); };
  const d = g && (g.gameDate || gxEtDay132(g.startTimeUTC));
  const aw = c(g && g.awayTeam), hm = c(g && g.homeTeam);
  if (!d || !aw || !hm) return u;
  return u.replace(/\/+$/, "") + "/live/nhl/" + d + "/" + aw + "-" + hm;
}
'''

def change(t):
    t = lit(t, "175: helpers", ROOT, HELPERS + ROOT, "change 175: Watch link with the game added")
    t = lit(t, "175: watch button", 'href={gxWatchUrl174(gid)}', 'href={gxWatchUrl175(g, gid)}', 'gxWatchUrl175(g, gid)')
    return t

edit(APP, change)
