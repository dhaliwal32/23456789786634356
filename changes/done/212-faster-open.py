# changes/212-faster-open.py - the app remembers day names and each week's games once, so it is ready sooner after opening

OLD_DL = 'const dayLabel = (x) => fromIso(x).toLocaleDateString("en-US", { weekday: "short", month: "numeric", day: "numeric" });'
NEW_DL = ('/* change 212: date words worked out once per date */ const GX_DL212 = new Map(), GX_MD212 = new Map();\n'
          'const dayLabel = (x) => { let v = GX_DL212.get(x); if (v === undefined) { v = fromIso(x).toLocaleDateString("en-US", { weekday: "short", month: "numeric", day: "numeric" }); GX_DL212.set(x, v); } return v; };')
OLD_MD = 'const mdL = (x) => fromIso(x).toLocaleDateString("en-US", { month: "short", day: "numeric" });'
NEW_MD = 'const mdL = (x) => { let v = GX_MD212.get(x); if (v === undefined) { v = fromIso(x).toLocaleDateString("en-US", { month: "short", day: "numeric" }); GX_MD212.set(x, v); } return v; };'
OLD_WG = 'const wkGames = (dates) => {'
NEW_WG = 'const GX_WG212 = new Map(); /* change 212: each week\'s games worked out once */\nconst wkGames = (dates) => { const k212 = dates.join(","); let v212 = GX_WG212.get(k212); if (!v212) { v212 = gxWkGames212(dates); GX_WG212.set(k212, v212); } return v212; };\nconst gxWkGames212 = (dates) => {'

def change(t):
    t = lit(t, "212: day names", OLD_DL, NEW_DL, "change 212: date words worked out once per date")
    t = lit(t, "212: month-day", OLD_MD, NEW_MD, "GX_MD212.set(x, v)")
    t = lit(t, "212: week games", OLD_WG, NEW_WG, "change 212: each week's games worked out once")
    return t

edit(APP, change)
