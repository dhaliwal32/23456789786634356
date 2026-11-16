"""
gm_tx.py - change 298: the league's recent moves from ESPN (pickups, drops, waiver claims, trades, trade votes).
Called by espn_sync.py. Returns a short list that goes into espn-data.js as "tx" (newest first).
Each item: {id, ty, st, tm, at, rel, it: [[playerId, ADD/DROP/TRADE, fromTeam, toTeam], ...], bid}
"""
import collections


def read(session, league_url, cur_sp, days=8):
    seen, out, types = set(), [], collections.Counter()
    try:
        cur = int(cur_sp or 0)
    except Exception:
        cur = 0
    if cur < 1:
        print("(tx) skipped: no current day number from ESPN")
        return []
    for sp in range(max(1, cur - days + 1), cur + 1):
        try:
            r = session.get(league_url, params=[("view", "mTransactions2"), ("scoringPeriodId", sp)], timeout=30)
            if r.status_code != 200:
                print(f"(tx) day {sp}: ESPN answered {r.status_code}")
                continue
            js = r.json() or {}
        except Exception as ex:
            print(f"(tx) day {sp}: {type(ex).__name__}")
            continue
        for t in js.get("transactions") or []:
            k = t.get("id")
            if not k or k in seen:
                continue
            seen.add(k)
            ty = str(t.get("type") or "")
            types[ty + "/" + str(t.get("status") or "")] += 1
            items = [[i.get("playerId"), i.get("type"), i.get("fromTeamId"), i.get("toTeamId")] for i in (t.get("items") or [])]
            out.append({"id": k, "ty": ty, "st": t.get("status"), "tm": t.get("teamId"), "at": t.get("processDate") or t.get("proposedDate"),
                        "pr": t.get("proposedDate"), "rel": t.get("relatedTransactionId"), "it": items, "bid": t.get("bidAmount")})
    out.sort(key=lambda x: x.get("at") or 0, reverse=True)
    print(f"(tx) {len(out)} moves in the last {days} days: " + ", ".join(f"{k} {v}" for k, v in sorted(types.items())))
    return out[:400]
