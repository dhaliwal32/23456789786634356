# changes/219-players-one-row.py - Players has one row of buttons: Free agents, All players, Goalies, Injuries

OLD_PL = 'const GX_PL103 = [["adddrop", "Free agents"], ["goalies", "Goalies"], ["injuries", "Injuries"]];'
NEW_PL = 'const GX_PL103 = [["adddrop", "Free agents"], ["allp", "All players"], ["goalies", "Goalies"], ["injuries", "Injuries"]]; /* change 219: one row */'
OLD_FA = 'function GxFaToggle105({ cur, go }) {\n  return ('
NEW_FA = 'function GxFaToggle105({ cur, go }) {\n  if (true) return null; /* change 219: All players moved into the Players row */\n  return ('

def change(t):
    t = lit(t, "219: Players row", OLD_PL, NEW_PL, "change 219: one row */")
    t = lit(t, "219: old toggle off", OLD_FA, NEW_FA, "change 219: All players moved into the Players row")
    return t

edit(APP, change)
