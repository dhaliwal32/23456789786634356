# changes/261-alert-tap-opens-ntfy.py - phone alerts no longer carry a website link, so tapping one opens the ntfy app instead of Safari

def notify(t):
    t = lit(t, "261: gm_notify no click link",
            'headers = {"Title": title, "Priority": prio, "Click": APP_URL}',
            'headers = {"Title": title, "Priority": prio}  # change 261: no Click link, tapping opens ntfy',
            "# change 261: no Click link")
    return t

edit("gm_notify.py", notify)


def live(t):
    t = lit(t, "261: gm_live no click link",
            'headers={"Title": title, "Priority": "default", "Click": APP_URL}, timeout=20)',
            'headers={"Title": title, "Priority": "default"}, timeout=20)  # change 261: no Click link, tapping opens ntfy',
            "# change 261: no Click link")
    return t

edit("gm_live.py", live)
