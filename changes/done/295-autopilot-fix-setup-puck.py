# changes/295-autopilot-fix-setup-puck.py - lineup autopilot works again (it had been skipping every day since Oct 25 because it could not find ESPN's number for the day) and now says why whenever it skips; its notes reach the phone; Setup main page is only alerts, autopilot and AI (My team, Favourite team and Protected players moved to More); the live puck moves around the zone again and the dashed lines behind it are gone

AP_FN_OLD = '''def run(session, league_url, my_team_id, swid, season, league_id):
'''
AP_FN_NEW = '''def _sp_for(E, dd):
    """ESPN's number for a day (its scoringPeriodId). change 295: espn-data "periods" only lists the first weeks of the
    season, but the numbers simply run one a day from opening day, so count from the first one."""
    try:
        ps = [p for p in (E.get("periods") or []) if p.get("dates")]
        first = min(ps, key=lambda p: int(p["id"]))
        d0 = datetime.fromisoformat(first["dates"][0]).date()
        n = int(first["id"]) + (dd - d0).days
        return n if n >= 1 else None
    except Exception:
        return None


def run(session, league_url, my_team_id, swid, season, league_id):
'''

SP_OLD = '''        sp = next((p["id"] for p in (E.get("periods") or []) if day in (p.get("dates") or [])), None)
'''
SP_NEW = '''        sp = _sp_for(E, dd)
'''

SKIP_OLD = '''        if not sp or not games:
            if future:
'''
SKIP_NEW = '''        if not sp or not games:
            print(f"(autopilot) {day}: skipped, " + ("no NHL games that day" if sp else "could not work out ESPN's number for the day"))
            if future:
'''

CHK_OLD = '''        r.raise_for_status()
        team = next((t for t in r.json().get("teams", []) if t.get("id") == my_team_id), None)
'''
CHK_NEW = '''        r.raise_for_status()
        cur_sp = r.json().get("scoringPeriodId")
        if not future and cur_sp and abs(int(cur_sp) - int(sp)) > 1:
            print(f"(autopilot) {day}: ESPN says today is day {cur_sp} but the app worked out day {sp}, so nothing was changed")
            continue
        team = next((t for t in r.json().get("teams", []) if t.get("id") == my_team_id), None)
'''

N1_OLD = '''            note("Autopilot", f"Changed your lineup ({stamp}):\\n" + "\\n".join(lines))
'''
N1_NEW = '''            note("Fantasy GM", f"Autopilot set your lineup ({stamp}):\\n" + "\\n".join(lines))
'''
N2_OLD = '''        note("Autopilot could not change your lineup", "\\n".join(fails) + ". Set it by hand on ESPN.", "high")
'''
N2_NEW = '''        note("Fantasy GM", "Autopilot could not change your lineup. " + "\\n".join(fails) + ". Set it by hand on ESPN.", "high")
'''

APP_START = r'''      <div className="gx-tag gx-st275">App</div>
'''
APP_END = r'''      <div className="gx-tag gx-st275">Alerts and lineup</div>
'''
APP_NEW = r'''      {/* change 295: My team and Favourite team are in More */}
      <div className="gx-tag gx-st275">Alerts and lineup</div>
'''
PR_OLD = r'''        {row("rules", "Protected players", (top + kept.length) + " players the app will never tell you to drop", () => go("setup", "rules"), 1)}
'''
MORE_OLD = r'''    <div className="gx-sr"><span>Watch link</span><GxWatchSel174 /></div>{/* change 291 */}
'''
MORE_NEW = r'''    <div className="gx-sr"><span>My team</span><GxMeSel241 s={s} /></div>
    <div className="gx-sr"><span>Favourite team</span><GxFavSel112 /></div>
    <div className="gx-sr"><span>Watch link</span><GxWatchSel174 /></div>{/* change 291 */}
    {row("rules", "Protected players", (top + kept.length) + " players the app will never tell you to drop", () => go("setup", "rules"), 1)}{/* change 295 */}
'''
SUM_OLD = r'''{row("more", "More", "Injury dates, edit players, betting lines, schedule, backup", () => go("setup", "more"), 0)}'''
SUM_NEW = r'''{row("more", "More", "Your team, protected players, injury dates, backup", () => go("setup", "more"), 0)}'''

PK_OLD = r'''      tx = x + (Math.random() * 8 - 4); ty = -y + (Math.random() * 8 - 4); /* change 293: stays by the real spot */'''
PK_NEW = r'''      if (zs) { tx = zs * (30 + Math.random() * 58); ty = -34 + Math.random() * 68; } /* change 295: moves around the zone again */
      else { tx = x + (Math.random() * 20 - 10); ty = -y + (Math.random() * 20 - 10); }'''

TR_START = r'''          {p && trail.length ? <polyline points='''
TR_END = r'''data-gx="266p" /> : null}
'''
TR_NEW = r'''          {/* change 295: no dashed path behind the puck */}
'''


def cut(t, name, start, end, new, done):
    if done in t:
        print(f"(install) {name}: already done")
        return t
    if t.count(start) != 1:
        fail(f"'{name}' start matched {t.count(start)} times")
    a = t.find(start)
    b = t.find(end, a)
    if b < 0:
        fail(f"'{name}' end not found")
    print(f"(install) {name}: updated")
    return t[:a] + new + t[b + len(end):]


def change(t):
    t = cut(t, "295: App group off the main Setup page", APP_START, APP_END, APP_NEW, "change 295: My team and Favourite team are in More")
    t = lit(t, "295: protected players off the main page", PR_OLD, "")
    t = lit(t, "295: into More", MORE_OLD, MORE_NEW, "{/* change 295 */}")
    t = lit(t, "295: More summary", SUM_OLD, SUM_NEW)
    t = lit(t, "295: puck moves around again", PK_OLD, PK_NEW, "change 295: moves around the zone again")
    t = cut(t, "295: no dashed path", TR_START, TR_END, TR_NEW, "change 295: no dashed path behind the puck")
    return t


def autopilot(t):
    t = lit(t, "295: day number helper", AP_FN_OLD, AP_FN_NEW, "def _sp_for(E, dd):")
    t = lit(t, "295: day number", SP_OLD, SP_NEW, "sp = _sp_for(E, dd)")
    t = lit(t, "295: say why it skipped", SKIP_OLD, SKIP_NEW, "(autopilot) {day}: skipped, ")
    t = lit(t, "295: check the day with ESPN", CHK_OLD, CHK_NEW, "cur_sp = r.json().get")
    t = lit(t, "295: note title", N1_OLD, N1_NEW, "Autopilot set your lineup")
    t = lit(t, "295: failure note title", N2_OLD, N2_NEW, '"Autopilot could not change your lineup. "')
    return t


edit(APP, change)
edit("gm_autopilot.py", autopilot)
