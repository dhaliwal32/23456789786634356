# changes/274-remove-talk-tab.py - Talk tab taken out of the player screen (Kuvar, Nov 14: "no more talk"); Reddit refuses the collector without an app key

def change(t):
    t = lit(t, "274: Talk tab button off",
            'const tabs = [["ov", "Overview"], ["log", "Game log"], ["news", "News" + (news.length ? " (" + news.length + ")" : "")], ["talk", "Talk"], ["lines", "Lines"]];',
            'const tabs = [["ov", "Overview"], ["log", "Game log"], ["news", "News" + (news.length ? " (" + news.length + ")" : "")], ["lines", "Lines"]]; /* 274: Talk tab removed */',
            "274: Talk tab removed")
    t = lit(t, "274: Talk tab body off", '          {tab === "talk" ? <GxTalk270 p={p} s={s} /> : null}\n', "          {/* 274: Talk tab body removed */}\n", "274: Talk tab body removed")
    return t

edit(APP, change)
