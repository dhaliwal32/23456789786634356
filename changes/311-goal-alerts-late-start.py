# changes/311-goal-alerts-late-start.py - opponent goal / assist alerts: title back to "\U0001F3D2 Fantasy Islands" (no title showed the name twice), and goals scored before the watcher starts (in the last 3 hours) are no longer skipped; sent alerts are remembered in edge/onice-sent311.json so a restart never repeats one

LV1_OLD = '''gm_push.send("", msg, "#matchup")  # change 305: no title, the app's name shows instead'''
LV1_NEW = '''gm_push.send("\\U0001F3D2 Fantasy Islands", msg, "#matchup")  # change 311: title back (no title showed the name twice)
                    _mark311(key)'''
LV2_OLD = '''                if not _primed302:
                    continue          # goals from before this run started: no alert'''
LV2_NEW = '''                if not _primed302 and (key in _sent311() or not _recent311(p.get("wallclock"))):
                    continue          # change 311: before this run started, only goals from the last 3 hours not already sent'''
LV3_OLD = '''        run("add", "edge/onice-live.json")'''
LV3_NEW = '''        run("add", "edge/onice-live.json")
        run("add", "edge/onice-sent311.json")  # change 311: goal alerts already sent'''
LV4_OLD = '''def goal_alerts302(opp):'''
LV4_NEW = '''# ---------- change 311: remember sent goal alerts, catch goals scored before the watcher started ----------
SENT311 = os.path.join(HERE, "edge", "onice-sent311.json")
_sent_cache311 = None


def _sent311():
    global _sent_cache311
    if _sent_cache311 is None:
        try:
            with open(SENT311) as f:
                _sent_cache311 = set(json.load(f).get("keys", []))
        except Exception:
            _sent_cache311 = set()
    return _sent_cache311


def _mark311(key):
    k = _sent311()
    k.add(key)
    try:
        with open(SENT311, "w") as f:
            json.dump({"keys": sorted(k)[-400:]}, f)
    except Exception as e:
        log("could not save sent alerts", e)


def _recent311(wc):
    try:
        t = datetime.strptime(str(wc)[:19], "%Y-%m-%dT%H:%M:%S").replace(tzinfo=timezone.utc)
        return (datetime.now(timezone.utc) - t).total_seconds() < 3 * 3600
    except Exception:
        return False


def goal_alerts302(opp):'''
LV5_OLD = '''    ids = _opp_ids302(opp)
    if not ids:
        return'''
LV5_NEW = '''    ids = _opp_ids302(opp)
    if not _primed302:
        log(f"goal alerts: opponent {opp}, {len(ids)} players")  # change 311
    if not ids:
        return'''
PS_OLD = '''send("", "Test - alerts from the app are working.", "#matchup")  # change 305'''
PS_NEW = '''send("\\U0001F3D2 Fantasy Islands", "Test - alerts from the app are working.", "#matchup")  # change 311'''


def _lv(t):
    t = lit(t, "311: title back", LV1_OLD, LV1_NEW, "change 311: title back")
    t = lit(t, "311: catch earlier goals", LV2_OLD, LV2_NEW, "change 311: before this run started")
    t = lit(t, "311: commit sent list", LV3_OLD, LV3_NEW, "change 311: goal alerts already sent")
    t = lit(t, "311: helpers", LV4_OLD, LV4_NEW, "change 311: remember sent goal alerts")
    t = lit(t, "311: log roster size", LV5_OLD, LV5_NEW, "# change 311\n")
    return t


edit("gm_live.py", _lv)
edit("gm_push.py", lambda t: lit(t, "311: test alert title back", PS_OLD, PS_NEW, "# change 311"))
