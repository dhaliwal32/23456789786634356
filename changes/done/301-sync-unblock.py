# changes/301-sync-unblock.py - the sync stopped saving on Nov 16: its replay clean-up deleted edge/onice-live.json (its name looks like a replay file) while the live job kept writing it, so every save clashed; the clean-up now leaves the on-ice files alone

OLD = '''    for f in glob.glob(os.path.join(DIR, "*-*.json")):
        if os.path.basename(f)[:-5] not in G:
            os.remove(f)
'''
NEW = '''    for f in glob.glob(os.path.join(DIR, "*-*.json")):
        if os.path.basename(f).startswith("onice"):  # change 301: written by gm_live.py / gm_onice.py, not a replay
            continue
        if os.path.basename(f)[:-5] not in G:
            os.remove(f)
'''

edit("gm_edge.py", lambda t: lit(t, "301: keep the on-ice files", OLD, NEW, "change 301: written by gm_live.py"))
