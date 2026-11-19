# changes/322-alerts-own-track.py - goal / assist alerts run on their own track, so saving who was on the ice (which took 4 minutes after the Suzuki goal on Nov 18) can never hold an alert back

THREAD = r'''# ---------- change 322: the alert checks run on their own track ----------
_opp322 = [None]
_run322 = [False]


def _loop322():
    while True:
        try:
            if _opp322[0]:
                fast318(_opp322[0], 0)  # one look at both feeds
        except Exception as e:
            log("alert track error", e)
        time.sleep(2)


def alerts322(opp):
    """hand the alert track the current opponent; start the track the first time"""
    if opp:
        _opp322[0] = opp
    if not _run322[0] and _opp322[0]:
        import threading
        threading.Thread(target=_loop322, daemon=True).start()
        _run322[0] = True
        log("alert track started")


if __name__ == "__main__":'''


def go(t):
    t = lit(t, "322: main loop hands off",
            '''        fast318(sc[2] if sc else None, 30)  # change 318: NHL feed every 5 seconds (replaces the ESPN goal check, goal_alerts302)''',
            '''        alerts322(sc[2] if sc else None)  # change 322: goal alerts run on their own track (every 2 s), never held up by the steps above
        time.sleep(20)''',
            'alerts322(sc[2] if sc else None)')
    t = lit(t, "322: on ice first, alerts first",
            '''        push_onice()  # change 205''',
            '''        alerts322(sc[2] if sc else None)  # change 322: start the alert track before the slow on-ice step
        push_onice()  # change 205''',
            'start the alert track before the slow on-ice step')
    t = lit(t, "322: alert track", 'if __name__ == "__main__":', THREAD, "change 322: the alert checks run on their own track")
    py_ok("gm_live.py", t)
    return t


edit("gm_live.py", go)
