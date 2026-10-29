# changes/145-midnight-scores.py - at midnight (your time) the NHL scores switch to the new day's games and Matchup moves to the new day by itself; the scores feed always asks ESPN for today's date

def change(t):
    t = lit(t, "145: scores feed asks for today",
            'if (path === "score/now") return nf(GX_E132 + "scoreboard?_=" + Math.floor(Date.now() / 5000))',
            'if (path === "score/now") return nf(GX_E132 + "scoreboard?dates=" + todayISO().replace(/-/g, "") + "&_=" + Math.floor(Date.now() / 5000))',
            'scoreboard?dates=" + todayISO().replace(/-/g, "")')
    t = lit(t, "145: midnight refresh",
            '  useEffect(() => { const h32 = () => tick((x) => x + 1); window.addEventListener("gm-theme", h32); return () => window.removeEventListener("gm-theme", h32); }, []);\n',
            '  useEffect(() => { const h32 = () => tick((x) => x + 1); window.addEventListener("gm-theme", h32); return () => window.removeEventListener("gm-theme", h32); }, []);\n'
            '  useEffect(() => { /* gx145: new day at midnight */\n'
            '    let id = 0, day = todayISO();\n'
            '    const arm = () => { const n = new Date(), m = new Date(n.getFullYear(), n.getMonth(), n.getDate() + 1, 0, 0, 2); id = setTimeout(fire, Math.max(1000, m - n)); };\n'
            '    const fire = () => { if (todayISO() !== day) { day = todayISO(); window.__LP120 = 0; window.__NHLNOW = { games: [] }; tick((x) => x + 1); } arm(); };\n'
            '    const vis = () => { if (!document.hidden && todayISO() !== day) { clearTimeout(id); fire(); } };\n'
            '    arm(); document.addEventListener("visibilitychange", vis);\n'
            '    return () => { clearTimeout(id); document.removeEventListener("visibilitychange", vis); };\n'
            '  }, []);\n',
            'gx145: new day at midnight')
    return t


edit(APP, change)
