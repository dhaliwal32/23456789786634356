# changes/133-espn-shots-fix.py - live shots on goal were read from the wrong ESPN column (ESPN's "SOG" column is shootout goals; shots are "S"), so live points were missing 1 point per shot. Columns are now read by ESPN's own stat names

def change(t):
    t = lit(t, "133: read ESPN columns by name",
            'const s = a.stats || [], v = (l) => { const i = ix(l); return i < 0 ? null : s[i]; }',
            'const s = a.stats || [], KY = grp.keys || [], KM = { "S": "shotsTotal", "SOG": "shotsTotal", "BS": "blockedShots", "HT": "hits", "TK": "takeaways", "+/-": "plusMinus", "TOI": "timeOnIce", "SHFT": "shifts", "G": "goals", "A": "assists", "GV": "giveaways", "PIM": "penaltyMinutes", "FO%": "faceoffPercent", "SV": "saves", "SA": "shotsAgainst", "GA": "goalsAgainst" }, v = (l) => { const k = KY.indexOf(KM[l]); const i = k >= 0 && !(l === "SV" || l === "SA" || l === "GA") ? k : ix(l === "SOG" ? "S" : l); return i < 0 ? null : s[i]; }',
            'KM = { "S": "shotsTotal"')
    return t


edit(APP, change)
