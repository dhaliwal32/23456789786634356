# changes/281-player-over-game.py - tapping a player inside an NHL game opens him on top of the game, so closing him puts you back exactly where you were (pre-game preview included); the Send a test button for app alerts works with the key the phone already has

NEW_CSS = r'''  /* change 281 (install.py) */
  html.gx-pt281 .gx-pd-ov { z-index: 80; }
</style>'''

GO_OLD = r'''  const go = (p) => { if (p && window.__NAV) { if (open) close(); window.__NAV.player(p); } };'''
GO_NEW = r'''  const go = (p) => { if (p && window.__NAV) { try { document.documentElement.classList.add("gx-pt281"); } catch (e) {} window.__NAV.player(p); } }; /* change 281: the game stays open underneath */'''

HELPERS = r'''// ---------- change 281: player on top of an open game; app alert test through a file (install.py) ----------
// a game opened from the player screen must still come out on top of him
(function gxTop281() {
  if (window.__gxTop281) return;
  window.__gxTop281 = 1;
  window.addEventListener("gx-game201", () => { try { document.documentElement.classList.remove("gx-pt281"); } catch (e) {} });
})();
// saving push_test.json starts the App alert test job (the phone's key may save files but not start jobs)
const gxPushPing281 = (key) => {
  const api = "https://api.github.com/repos/dhaliwal32/23456789786634356/contents/push_test.json";
  const hdr = { Authorization: "Bearer " + key, Accept: "application/vnd.github+json" };
  return fetch(api + "?ref=main&t=" + Date.now(), { headers: hdr, cache: "no-store" }).then((r) => (r.ok ? r.json() : null)).then((j) => {
    const body = { message: "App alert test", content: gxB64(JSON.stringify({ at: new Date().toISOString() }) + "\n"), branch: "main" };
    if (j && j.sha) body.sha = j.sha;
    return fetch(api, { method: "PUT", headers: { ...hdr, "Content-Type": "application/json" }, body: JSON.stringify(body) });
  });
};
'''

TEST_OLD = r'''    fetch(GX_PUSH_RUN278, { method: "POST", headers: { Authorization: "Bearer " + key, Accept: "application/vnd.github+json", "Content-Type": "application/json" }, body: JSON.stringify({ ref: "main" }) })
      .then((r) => setMsg(r.status === 204 ? "Test sent. It should arrive in about a minute." : "Could not start the test (" + r.status + ")."))'''
TEST_NEW = r'''    gxPushPing281(key)
      .then((r) => setMsg(r.ok ? "Test sent. It should arrive in about a minute." : "Could not start the test (" + r.status + ")."))'''


def change(t):
    t = lit(t, "281: styles", "</style>", NEW_CSS, "change 281 (install.py)")
    t = lit(t, "281: game stays open", GO_OLD, GO_NEW, "change 281: the game stays open underneath")
    t = lit(t, "281: test button", TEST_OLD, TEST_NEW, "gxPushPing281(key)\n")
    t = lit(t, "281: helpers", "// ---------- change 278: alerts from the app itself (install.py) ----------", HELPERS + "// ---------- change 278: alerts from the app itself (install.py) ----------", "change 281: player on top of an open game")
    return t

edit(APP, change)
