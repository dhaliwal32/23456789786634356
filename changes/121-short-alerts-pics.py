# changes/121-short-alerts-pics.py - phone alerts: only power play joins (your players and free agents), Troy Terry getting close to returning, your goalies confirmed / not starting / not confirmed, and lead changes, all in a few words; no summaries or other alerts. Box score pop-up photo fills the circle like ESPN; the K in the top corner is your team picture

NOTIFY_GATE = r'''

# ---------- change 121: only the alerts Kuvar asked for, all titled "Fantasy GM"; no summaries ----------
ONLY_TITLE = "Fantasy GM"
_push121, _add121 = push, add


def push(title, msg, prio="default", tags=""):
    if title != ONLY_TITLE and not str(msg).startswith("Test"):
        print(f"(notify) not sent (only short Fantasy GM alerts are on): {title}")
        return False
    return _push121(title, msg, prio, tags)


def add(key, title, text, section="other", urgent=False, tags=""):
    if title != ONLY_TITLE:
        print(f"(notify) not sent (only short Fantasy GM alerts are on): {title}")
        return "switched off"
    return _add121(key, title, text, section, True, "")


def flush(now=None):
    print("(notify) summaries are off")

'''

ALERTS_NEW = r'''    # change 121: only short goalie alerts for your goalies with a game today
    alerts = []
    for p in mine:
        if p["p"] != "G" or slots.get(p["id"]) == IR or not upcoming(p["t"]) or is_out(p):
            continue
        last = p["n"].split()[-1]
        ok = lambda v: "confirm" in (v.get("status") or "").lower() and "un" not in (v.get("status") or "").lower()
        conf = any(ok(v) for k, v in gday.items() if norm(k) == norm(p["n"]))
        other = any(v.get("team") == p["t"] and ok(v) for k, v in gday.items() if norm(k) != norm(p["n"]))
        if conf:
            alerts.append(("Fantasy GM", f"{last} confirmed", "lineup", True, ""))
        elif other:
            alerts.append(("Fantasy GM", f"{last} not starting", "lineup", True, ""))
        elif games[p["t"]][1] - now <= timedelta(minutes=75):
            alerts.append(("Fantasy GM", f"{last} not confirmed", "lineup", True, ""))

    new = 0
    for title, msg, section, urgent, tags in alerts:'''

WATCH = r'''
# change 121: players to watch for a return from injury (alert_prefs.json "return_watch")
def _watch121():
    try:
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "alert_prefs.json"), encoding="utf-8") as f:
            w = json.load(f).get("return_watch")
        if isinstance(w, list):
            return {norm(x) for x in w}
    except Exception:
        pass
    return {norm("Troy Terry")}


WATCH121 = _watch121()


def relevance(ch, p):'''

ALERT_FOR = r'''def alert_for(c):
    # change 121: a few words only, and only power play joins and watched players coming back
    last = str(c.get("name") or "").split()[-1] if c.get("name") else ""
    if c["type"] == "pp" and c["dir"] == "up" and c.get("who") in ("mine", "fa"):
        return "Fantasy GM", f"{last} joined {c['team']} PP1"
    if c.get("who") == "watch":
        to, frm = str(c.get("to") or "").upper(), str(c.get("from") or "").upper()
        if c["type"] == "status" and to != frm and ("DAY" in to or to == "ACTIVE"):
            return "Fantasy GM", (f"{last} back to active" if to == "ACTIVE" else f"{last} close to returning ({pretty(to)})")
        if c["type"] == "lineup" and c["dir"] == "in":
            return "Fantasy GM", f"{last} back in the {c['team']} lineup"
        if c["type"] == "move" and c["dir"] == "in":
            return "Fantasy GM", f"{last} activated"
    return None


def _alert_for_old('''

CSS = r'''  /* change 121 (install.py) */
  .gx-bm119 .fc { background: #e8e8ea; }
  .gx-bm119 .fc .hs { position: absolute; bottom: 0; left: 50%; height: 100%; width: auto; max-width: none; transform: translateX(-50%); }
  .gx-bp121 { border: 0 !important; overflow: hidden; }
  .gx-bp121 .gx-fp114 { width: 100% !important; height: 100% !important; border-radius: 999px !important; object-fit: cover; }
</style>'''


def change_notify(t):
    if "change 121: only the alerts" in t:
        print("(install) 121: alert gate: already done")
        return t
    i = t.rfind('\nif __name__ == "__main__":')
    if i < 0:
        fail("121: end of gm_notify.py not found")
    print("(install) 121: alert gate: updated")
    return t[:i] + NOTIFY_GATE + t[i:]


def change_alerts(t):
    return lit(t, "121: short goalie alerts", "    new = 0\n    for title, msg, section, urgent, tags in alerts:", ALERTS_NEW, "change 121: only short goalie alerts")


def change_lines(t):
    t = lit(t, "121: return watch list", "\ndef relevance(ch, p):", WATCH, "WATCH121 = _watch121()")
    t = lit(t, "121: watched player first", "def relevance(ch, p):\n    if not p:\n        return None\n",
            "def relevance(ch, p):\n    if not p:\n        return None\n    if norm(p.get(\"n\") or ch.get(\"name\") or \"\") in WATCH121 and ch[\"type\"] in (\"status\", \"lineup\", \"move\"):\n        return \"watch\"\n",
            'return "watch"')
    t = lit(t, "121: free agent power play joins", '    if ch["type"] == "move" and ch["dir"] == "in":\n        return "fa"\n',
            '    if ch["type"] == "pp" and ch["dir"] == "up":\n        return "fa"\n    if ch["type"] == "move" and ch["dir"] == "in":\n        return "fa"\n',
            'if ch["type"] == "pp" and ch["dir"] == "up":\n        return "fa"')
    t = lit(t, "121: short line alerts", "def alert_for(c):", ALERT_FOR + "c):", "change 121: a few words only")
    i = t.find("        title, text, prio, tags = alert_for(c)\n")
    if i >= 0:
        j = t.find("        c[\"alerted\"] = True\n", i)
        if j < 0:
            fail("121: line alert loop not found")
        t = t[:i] + "        a121 = alert_for(c)\n        urgent = bool(a121)\n        if a121:\n            gm_notify.add(c[\"id\"], a121[0], a121[1], \"mine\", urgent=True, tags=\"\")\n" + t[j:]
        print("(install) 121: line alert loop: updated")
    elif "a121 = alert_for(c)" not in t:
        fail("121: line alert loop not found")
    return t


def change_live(t):
    t = lit(t, "121: short lead alert (you)", 'push("You took the lead", f"{a:.1f} to {b:.1f} vs {them}")', 'push("Fantasy GM", f"You lead {a:.1f} to {b:.1f}")', 'f"You lead {a:.1f} to {b:.1f}"')
    t = lit(t, "121: short lead alert (them)", 'push(f"{them} took the lead", f"{b:.1f} to {a:.1f}. You trail by {abs(d):.1f}")', 'push("Fantasy GM", f"{them} lead {b:.1f} to {a:.1f}")', 'f"{them} lead {b:.1f} to {a:.1f}"')
    t = lit(t, "121: alert style", 'headers={"Title": title, "Priority": "high", "Tags": "ice_hockey", "Click": APP_URL}', 'headers={"Title": title, "Priority": "default", "Click": APP_URL}', '"Priority": "default", "Click": APP_URL}')
    return t


def change(t):
    t = lit(t, "121: styles", "</style>", CSS, "change 121 (install.py)")
    t = lit(t, "121: pop-up photo", '<div className="fc"><GxFace p={p} size={100} /></div>',
            '<div className="fc">{String(p.id || "")[0] === "e" ? <img className="hs" src={"https://a.espncdn.com/i/headshots/nhl/players/full/" + String(p.id).slice(1) + ".png"} alt="" onError={(e) => { e.currentTarget.style.display = "none"; }} /> : <TeamLogo t={p.t} size={60} />}</div>',
            '<img className="hs" src={"https://a.espncdn.com/i/headshots/nhl/players/full/"')
    n = t.count('<span className="gx-badge">{(name[0] || "K").toUpperCase()}</span>')
    if n:
        t = t.replace('<span className="gx-badge">{(name[0] || "K").toUpperCase()}</span>', '<span className="gx-badge gx-bp121"><GxFtPic114 id={s.me} size={30} /></span>')
        print("(install) 121: team picture in the corner (%d places): updated" % n)
    elif "gx-badge gx-bp121" not in t:
        fail("121: K badge not found")
    return t


edit("gm_notify.py", change_notify)
edit("gm_alerts.py", change_alerts)
edit("gm_lines.py", change_lines)
edit("gm_live.py", change_live)
edit(APP, change)
