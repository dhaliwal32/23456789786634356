# changes/325-alerts-lineup-fixes.py - lineup autopilot works again between 9 PM and 1 AM (it was setting tomorrow before ESPN moved to tomorrow, and ESPN refused every change); no autopilot buzz 11 PM - 7 AM (held and sent as one alert at 7 AM); line / injury alerts found overnight now come at 7 AM instead of never; NHL lines read every 30 min (every 15 min from 2 to 7 PM) instead of every 2 hours, so line alerts are not late and bunched; dead phone sign-ups are removed; goal alerts never sent twice after the watcher restarts; the alert time log is no longer deleted by the sync

# ---------- gm_autopilot.py ----------
AP_ROSTER_OLD = '''        team = next((t for t in r.json().get("teams", []) if t.get("id") == my_team_id), None)
        entries = (team or {}).get("roster", {}).get("entries", [])
'''
AP_ROSTER_NEW = '''        # change 325: after midnight Eastern the app is on tomorrow but ESPN stays on today until about 1 AM Pacific;
        # ESPN only takes that day as an upcoming-day change (it refused every "today" change in that window)
        ahead325 = (not future) and bool(cur_sp) and int(sp) > int(cur_sp)
        team = next((t for t in r.json().get("teams", []) if t.get("id") == my_team_id), None)
        entries = (team or {}).get("roster", {}).get("entries", [])
'''
AP_LOCK_OLD = '''"locked": (not future) and bool(pe.get("lineupLocked")),'''
AP_LOCK_NEW = '''"locked": (not future) and not ahead325 and bool(pe.get("lineupLocked")),'''
AP_FOUND_OLD = '''        found.append({"day": day, "sp": sp, "future": future, "moves": moves,'''
AP_FOUND_NEW = '''        found.append({"day": day, "sp": sp, "future": future, "post325": future or ahead325, "moves": moves,'''
AP_POST_OLD = '''        ok, msg = _post(session, url, my_team_id, swid, f["sp"], f["future"], f["moves"])'''
AP_POST_NEW = '''        ok, msg = _post(session, url, my_team_id, swid, f["sp"], f.get("post325", f["future"]), f["moves"])  # change 325'''
AP_NONE_OLD = '''    if not found:
        save_log(b)
        return
'''
AP_NONE_NEW = '''    if not found:
        _held325(st)  # change 325: send what was held overnight
        save_log(b)
        return
'''
AP_NOTE_OLD = '''        else:
            note("Fantasy GM", f"Autopilot set your lineup ({stamp}):\\n" + "\\n".join(lines))
    if fails and not st.get("failed"):
        st["failed"] = 1
        note("Fantasy GM", "Autopilot could not change your lineup. " + "\\n".join(fails) + ". Set it by hand on ESPN.", "high")
    save_log(b)
'''
AP_NOTE_NEW = '''        else:
            _note325(st, note, f"Autopilot set your lineup ({stamp}):\\n" + "\\n".join(lines))
    if fails and not st.get("failed"):
        st["failed"] = 1
        _note325(st, note, "Autopilot could not change your lineup. " + "\\n".join(fails) + ". Set it by hand on ESPN.", "high")
    _held325(st)
    save_log(b)


# ---------- change 325: no autopilot buzz 11 PM - 7 AM Pacific; what it did overnight comes as one alert at 7 AM ----------
def _quiet325():
    h = datetime.now(PT).hour
    return h >= 23 or h < 7


def _note325(st, note, text, prio="default"):
    if _quiet325():
        st["held325"] = (st.get("held325") or [])[-5:] + [text]
        print("(autopilot) quiet hours - alert held for 7 AM")
        return
    _held325(st)  # what was held overnight goes first
    note("Fantasy GM", text, prio)


def _held325(st):
    held = st.get("held325") or []
    if not held or _quiet325():
        return
    try:
        import gm_notify
        if gm_notify.push("Fantasy GM", "Overnight: " + "\\n".join(held), "default"):
            st.pop("held325", None)
    except Exception as ex:
        print(f"(autopilot) overnight alert not sent: {ex}")
'''


def autopilot(t):
    t = lit(t, "325: know when ESPN is still on the day before", AP_ROSTER_OLD, AP_ROSTER_NEW, "ahead325 = (not future)")
    t = lit(t, "325: nobody is locked for that day yet", AP_LOCK_OLD, AP_LOCK_NEW, "not ahead325 and bool(")
    t = lit(t, "325: remember how to send it", AP_FOUND_OLD, AP_FOUND_NEW, '"post325": future or ahead325')
    t = lit(t, "325: send it as an upcoming-day change", AP_POST_OLD, AP_POST_NEW, 'f.get("post325", f["future"])')
    t = lit(t, "325: overnight alert when nothing changes", AP_NONE_OLD, AP_NONE_NEW, "_held325(st)  # change 325")
    t = lit(t, "325: quiet hours for autopilot alerts", AP_NOTE_OLD, AP_NOTE_NEW, "def _note325(st, note, text")
    return t


# ---------- gm_notify.py ----------
NT_OLD = '''def flush(now=None):
    print("(notify) summaries are off")
'''
NT_NEW = '''def flush(now=None):
    print("(notify) summaries are off")
    try:
        _morning325(now)
    except Exception as ex:
        print(f"(notify) WARNING overnight alerts: {ex}")


def _morning325(now=None):
    """change 325: alerts found 11 PM - 7 AM were held for a summary, but summaries are off, so they were never sent.
    Now the ones from the last 10 hours go out after 7 AM (newest 5); older ones are dropped."""
    now = now or datetime.now(UTC)
    if quiet(now):
        return
    box = _load()
    held = [i for i in box["items"] if not i.get("sent") and i.get("urgent") and i.get("title") == ONLY_TITLE]
    if not held:
        return
    cut = now - timedelta(hours=10)
    fresh = [i for i in held if (_parse(i.get("at", "")) or now) >= cut]
    for i in held:
        if i not in fresh[-5:]:
            i.update(sent=True, via="expired325", sent_at=_iso(now))
    for i in fresh[-5:]:
        if push(ONLY_TITLE, i["text"], "high"):
            i.update(sent=True, via="morning325", sent_at=_iso(now))
    _save(box)
    print(f"(notify) {len(fresh[-5:])} overnight alert(s) sent, {len(held) - len(fresh[-5:])} too old")
'''


def notify(t):
    return lit(t, "325: send overnight alerts in the morning", NT_OLD, NT_NEW, "def _morning325(now=None):")


# ---------- gm_lines.py ----------
LN_OLD = '''READ_EVERY_H = 2           # re-read lines + rosters this often...
READ_EVERY_H_PREGAME = 1   # ...and every hour from 2 PM to 7 PM (lineups get posted)
'''
LN_NEW = '''READ_EVERY_H = 0.5         # re-read lines + rosters this often... (change 325: was 2 hours, alerts came late and in bunches)
READ_EVERY_H_PREGAME = 0.25  # ...and every 15 minutes from 2 PM to 7 PM (lineups get posted) (change 325: was 1 hour)
'''


def lines(t):
    return lit(t, "325: read lines more often", LN_OLD, LN_NEW, "change 325: was 2 hours")


# ---------- gm_push.py ----------
PU_LOOP_OLD = '''        ok = 0
        for x in subs:
'''
PU_LOOP_NEW = '''        ok, dead325 = 0, []
        for x in subs:
'''
PU_GONE_OLD = '''                else:
                    print(f"(push) a device refused the alert ({r.status_code}): {r.text[:120]}")
'''
PU_GONE_NEW = '''                else:
                    print(f"(push) a device refused the alert ({r.status_code}): {r.text[:120]}")
                    if r.status_code in (404, 410):
                        dead325.append(x["endpoint"])
'''
PU_END_OLD = '''        print(f"(push) app alert sent to {ok} of {len(subs)} device(s)")
        return ok
'''
PU_END_NEW = '''        print(f"(push) app alert sent to {ok} of {len(subs)} device(s)")
        if dead325:
            _drop325(dead325)
        return ok
'''
PU_HELP_OLD = '''if __name__ == "__main__":
'''
PU_HELP_NEW = '''def _drop325(dead):
    """change 325: a phone sign-up Apple says no longer exists is removed (only the sync saves this file)"""
    if os.environ.get("GITHUB_WORKFLOW") != "Fantasy sync":
        return
    try:
        with open(SUBS, encoding="utf-8") as f:
            d = json.load(f)
        keep = [x for x in d.get("subs", []) if x.get("endpoint") not in set(dead)]
        if len(keep) < len(d.get("subs", [])):
            d["subs"] = keep
            with open(SUBS, "w", encoding="utf-8") as f:
                json.dump(d, f, indent=1)
                f.write("\\n")
            print(f"(push) removed {len(dead)} device(s) that no longer exist")
    except Exception as ex:
        print(f"(push) could not remove old devices: {ex}")


if __name__ == "__main__":
'''


def pushf(t):
    t = lit(t, "325: note dead devices", PU_LOOP_OLD, PU_LOOP_NEW, "ok, dead325 = 0, []")
    t = lit(t, "325: which device is gone", PU_GONE_OLD, PU_GONE_NEW, "dead325.append(")
    t = lit(t, "325: remove them", PU_END_OLD, PU_END_NEW, "_drop325(dead325)")
    t = lit(t, "325: remover", PU_HELP_OLD, PU_HELP_NEW, "def _drop325(dead):")
    return t


# ---------- gm_edge.py ----------
ED_OLD = '''        if os.path.basename(f).startswith("onice"):  # change 301: written by gm_live.py / gm_onice.py, not a replay'''
ED_NEW = '''        if os.path.basename(f).startswith(("onice", "alert-times")):  # change 301: written by gm_live.py / gm_onice.py, not a replay (change 325: alert-times too)'''


def edge(t):
    return lit(t, "325: keep the alert time log", ED_OLD, ED_NEW, '"alert-times")):')


# ---------- gm_live.py ----------
LV_STOP_OLD = '''                log("no game live and none left today - stopping")
                return
'''
LV_STOP_NEW = '''                log("no game live and none left today - stopping")
                push_onice()  # change 325: save the last alerts sent, so a restart never sends them again
                return
'''
LV_END_OLD = '''        time.sleep(20)


# ---------- change 302'''
LV_END_NEW = '''        time.sleep(20)
    push_onice()  # change 325: out of time (GitHub allows 6 hours): save, and ask live-alerts.yml to start the next watcher now
    try:
        open(os.path.join(HERE, ".gx-restart325"), "w").write("1")
    except Exception:
        pass
    log("out of time - asking for the next watcher")


# ---------- change 302'''


def live(t):
    t = lit(t, "325: save before stopping", LV_STOP_OLD, LV_STOP_NEW, "push_onice()  # change 325: save the last")
    t = lit(t, "325: restart right away when out of time", LV_END_OLD, LV_END_NEW, ".gx-restart325")
    return t


edit("gm_autopilot.py", autopilot)
edit("gm_notify.py", notify)
edit("gm_lines.py", lines)
edit("gm_push.py", pushf)
edit("gm_edge.py", edge)
edit("gm_live.py", live)
