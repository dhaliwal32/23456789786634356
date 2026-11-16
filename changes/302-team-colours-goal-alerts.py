# changes/302-team-colours-goal-alerts.py - live tracker and shot map: when both teams wear nearly the same colour (Oilers and Flyers), the home team is shown in light grey so the two sides are easy to tell apart; phone alerts for every goal and assist by your opponent's players, in ESPN's format ("Goal by ... (9)", "Assist by ... (12)")

HELPERS = r'''// ---------- change 302: two teams in nearly the same colour (install.py) ----------
function gxPair302(A, H) {
  const a = gxCols184(A, H).sc, h = gxCols184(H, A).sc;
  try {
    const x = gxHex169(a.f), y = gxHex169(h.f), d = Math.sqrt((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2 + (x[2] - y[2]) ** 2);
    if (d < 100) return [a, { f: "#e6e6e6", s: "#121212", t: "#121212" }];
  } catch (e) {}
  return [a, h];
}
'''

C_OLD = r'''  const cA = gxCols184(A, H).sc, cH = gxCols184(H, A).sc;'''
C_NEW = r'''  const [cA, cH] = gxPair302(A, H); /* change 302 */'''


def change(t):
    t = lit(t, "302: helpers", ROOT, HELPERS + ROOT, "change 302: two teams in nearly the same colour")
    t = lit(t, "302: colours in the shot map and tracker", C_OLD, C_NEW, "change 302 */", 2)
    return t


GOALS = r'''

# ---------- change 302: a phone alert for every goal and assist by your opponent's players ----------
SB302 = "https://site.api.espn.com/apis/site/v2/sports/hockey/nhl/"
_seen302, _primed302, _opp302 = set(), False, {"id": None, "ids": set(), "at": 0}


def _opp_ids302(opp):
    """the opponent's player ids, read again every 20 minutes"""
    if opp != _opp302["id"] or time.time() - _opp302["at"] > 1200:
        try:
            r = s.get(LEAGUE, params=[("view", "mRoster"), ("forTeamId", opp)], timeout=30).json()
            t = next((x for x in r.get("teams", []) if x.get("id") == opp), {})
            _opp302.update({"id": opp, "ids": {e.get("playerId") for e in (t.get("roster") or {}).get("entries", [])}, "at": time.time()})
        except Exception as e:
            log("opponent roster failed", e)
    return _opp302["ids"]


def _count302(text, name, goal):
    import re as _re
    if goal:
        m = _re.search(r"Goal \((\d+)\)", text or "")
    else:
        m = _re.search(_re.escape(name) + r" \((\d+)\)", text or "")
    return f" ({m.group(1)})" if m else ""


def goal_alerts302(opp):
    global _primed302
    if not opp:
        return
    ids = _opp_ids302(opp)
    if not ids:
        return
    try:
        sb = requests.get(SB302 + "scoreboard", timeout=20).json()
    except Exception as e:
        log("goal check failed", e)
        return
    for ev in sb.get("events", []):
        st = (((ev.get("status") or {}).get("type")) or {}).get("state")
        if st not in ("in", "post"):
            continue
        try:
            sm = requests.get(SB302 + "summary", params={"event": ev.get("id")}, timeout=20).json()
        except Exception:
            continue
        for p in sm.get("plays") or []:
            if not p.get("scoringPlay") or ((p.get("period") or {}).get("number") or 0) >= 5:
                continue          # shootout goals do not count
            for q in p.get("participants") or []:
                a = q.get("athlete") or {}
                try:
                    pid = int(a.get("id"))
                except Exception:
                    continue
                kind = q.get("type")
                if pid not in ids or kind not in ("scorer", "assister"):
                    continue
                key = f"{p.get('id')}|{pid}"
                if key in _seen302:
                    continue
                _seen302.add(key)
                if not _primed302:
                    continue          # goals from before this run started: no alert
                name = a.get("displayName") or a.get("fullName") or ""
                goal = kind == "scorer"
                msg = ("Goal by " if goal else "Assist by ") + name + _count302(p.get("text"), name, goal)
                try:
                    import gm_push
                    gm_push.send("\U0001F3D2 Fantasy Islands", msg, "#matchup")
                except Exception as e:
                    log("goal alert failed", e)
                log("goal alert:", msg)
    _primed302 = True
'''

M_OLD = '''        push_onice()  # change 205
'''
M_NEW = '''        push_onice()  # change 205
        try:
            goal_alerts302(sc[2] if sc else None)  # change 302
        except Exception as e:
            log("goal alerts failed", e)
'''
END_OLD = '''

if __name__ == "__main__":
    main()'''


def live(t):
    t = lit(t, "302: goal alert code", END_OLD, GOALS + END_OLD, "change 302: a phone alert for every goal")
    t = lit(t, "302: check goals each loop", M_OLD, M_NEW, "goal_alerts302(sc[2]")
    return t


edit(APP, change)
edit("gm_live.py", live)
