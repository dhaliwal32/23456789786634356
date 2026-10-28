# changes/129-auto-refresh.py - the app refreshes itself: it checks for new ESPN data every minute (was 2), checks right away whenever you come back to it, and if it was in the background for 5 minutes or more it reloads fully (same as Setup > Refresh) so scores, matchup and AI projections are all fresh. It stays on the page you were on


def change(t):
    t = lit(t, "129: name the data check",
            '    const id = setInterval(() => {\n      const sc = document.createElement("script");\n      sc.src = "espn-data.js?t=" + Date.now();',
            '    const poll129 = () => {\n      const sc = document.createElement("script");\n      sc.src = "espn-data.js?t=" + Date.now();',
            "const poll129 = () => {")
    t = lit(t, "129: check every minute",
            '    }, 2 * 60 * 1000);\n    return () => clearInterval(id);\n  }, [loaded]);',
            '''    };
    window.__gxPoll129 = poll129; /* gx129 */
    const id = setInterval(() => { if (!document.hidden) poll129(); }, 60 * 1000);
    return () => clearInterval(id);
  }, [loaded]);
  useEffect(() => {
    // change 129: coming back to the app - reload fully after 5+ minutes away, otherwise check for new data now
    let hid = document.hidden ? Date.now() : 0;
    const fresh = () => { try { window.location.replace(window.location.pathname + "?v=" + Date.now() + window.location.hash); } catch (e) { window.location.reload(); } };
    const vis = () => {
      if (document.hidden) { hid = Date.now(); return; }
      if (hid && Date.now() - hid >= 5 * 60 * 1000) fresh(); else if (window.__gxPoll129) window.__gxPoll129();
      hid = 0;
    };
    const show = (e) => { if (e.persisted) fresh(); };
    document.addEventListener("visibilitychange", vis);
    window.addEventListener("pageshow", show);
    return () => { document.removeEventListener("visibilitychange", vis); window.removeEventListener("pageshow", show); };
  }, []);''',
            "change 129: coming back to the app")
    return t


edit(APP, change)
