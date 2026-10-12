# changes/074-fast-app.py - the app loads the copy built on GitHub instead of translating itself on the phone

OLD_BABEL = '<script src="https://unpkg.com/@babel/standalone@7/babel.min.js"></script>'
NEW_BABEL = '<!-- change 074 (gx074-head): Babel loads only when needed, see the loader at the end of the page -->'

LOADER = r'''<script>/* change 074 (gx074-loader): use the copy built on GitHub when it matches this page; otherwise translate in the browser like before */
(function () {
  var started = false;
  function slow() {
    if (started) return;
    started = true;
    var s = document.createElement("script");
    s.src = "https://unpkg.com/@babel/standalone@7/babel.min.js";
    s.onload = function () { if (document.readyState === "loading") return; try { window.Babel.transformScriptTags(); } catch (e) { console.error(e); } };
    document.head.appendChild(s);
  }
  try {
    var el = document.querySelector('script[type="text/babel"]:not([src])');
    var m = document.querySelector('meta[name="gx-build"]');
    var c = m ? String(m.getAttribute("content") || "").split(".") : [];
    if (!el || c.length !== 2 || /[?&]slow\b/.test(location.search)) { slow(); return; }
    var t = el.textContent, h = 0x811c9dc5;
    for (var i = 0; i < t.length; i++) { h ^= t.charCodeAt(i); h = Math.imul(h, 0x01000193); }
    if ((h >>> 0).toString(36) !== c[0]) { slow(); return; }
    window.__GX_FAST = c[1];
    ["build/lines-tab.js", "build/ask-panel.js", m.getAttribute("data-file") || "build/app.js"].forEach(function (f) {
      var b = document.createElement("script");
      b.src = f + "?v=" + c[1];
      b.async = false;
      b.onerror = slow;
      document.body.appendChild(b);
    });
  } catch (e) { slow(); }
})();
</script>
'''


def change(t):
    t = lit(t, "074: stop loading Babel up front", OLD_BABEL, NEW_BABEL, "gx074-head")
    t = lit(t, "074: fast loader", "</body>", LOADER + "</body>", "gx074-loader")
    for must in ("function App(", "function Today(", "gx074-loader", "gx074-head"):
        if must not in t:
            fail("fantasy-gm.html looks damaged after change 074 (" + must + ").")
    return t


edit(APP, change)
