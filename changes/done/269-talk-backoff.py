# changes/269-talk-backoff.py - Player Talk: when Reddit refuses every request, wait the normal 3 hours before trying again (it was retrying on every sync)

OLD = '''        log(f"every Reddit request failed ({F.n}); keeping old files")
        return'''
NEW = '''        log(f"every Reddit request failed ({F.n}); keeping old files, next try in {EVERY_H} hours")
        st["last"] = now().isoformat(timespec="seconds"); st["req"], st["fails"] = F.n, F.fails  # change 269: back off
        json.dump(st, open(STATE, "w"))
        return'''

def fix(t):
    return lit(t, "269: back off after a refused run", OLD, NEW, "change 269: back off")

edit("gm_talk.py", fix)
