# changes/304-only-processed-trades.py - League activity shows only trades ESPN has processed (both teams and all their players known); trades still waiting for votes are left out

OLD = '''    } else if (t.ty === "TRADE_ACCEPT" || (t.ty === "TRADE_PROPOSAL" && /EXECUTED|VETOED|PENDING/.test(String(t.st || "")) && (votes[t.id] || []).length)) {'''
NEW = '''    } else if ((t.ty === "TRADE_ACCEPT" || t.ty === "TRADE_PROPOSAL") && t.st === "EXECUTED") { /* change 304: processed trades only */'''

PUSH_OLD = '''      out.push({ k: root.id, kind: "trade", at: t.at,'''
PUSH_NEW = '''      if (Object.keys(sides).length !== 2 || Object.keys(sides).some((X) => !(sides[X] || []).length)) return; /* change 304: both sides with players, or not shown */
      const sig304 = Object.keys(sides).map((X) => sides[X].map((p) => p.id).sort().join(",")).sort().join("|");
      if (seenTrade["s" + sig304]) return; /* change 304: one row per trade, however ESPN splits it */
      seenTrade["s" + sig304] = 1;
''' + PUSH_OLD


def change(t):
    t = lit(t, "304: processed trades only", OLD, NEW, "change 304: processed trades only")
    t = lit(t, "304: both sides known", PUSH_OLD, PUSH_NEW, "change 304: both sides with players")
    return t

edit(APP, change)
