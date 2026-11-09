# changes/214-player-screen-smooth.py - the player screen slides in first, then loads the game log and past seasons

OLD_ST = '''  const [tab, setTab] = useState("ov");
  const [log, setLog] = useState(null);'''
NEW_ST = '''  const [tab, setTab] = useState("ov");
  /* change 214: wait for the slide-in to finish before the heavy loading starts */
  const [rd214, setRd214] = useState(false);
  useEffect(() => { setRd214(false); const t214 = setTimeout(() => setRd214(true), 260); return () => clearTimeout(t214); }, [p0.id]);
  const [log, setLog] = useState(null);'''

OLD_H1 = '''    let dead = false;
    setSea191("cur"); setPrev191(null);'''
NEW_H1 = '''    let dead = false;
    setSea191("cur"); setPrev191(null);
    if (!rd214) return undefined; /* change 214 */'''
OLD_H2 = '''      else setPrev191([]);
    });
    return () => { dead = true; };
  }, [p.id]);'''
NEW_H2 = '''      else setPrev191([]);
    });
    return () => { dead = true; };
  }, [p.id, rd214]);'''

OLD_L1 = '''    let dead = false;
    setLog(null);
    if (!eid) { setLog([]); return; }'''
NEW_L1 = '''    let dead = false;
    setLog(null);
    if (!rd214) return undefined; /* change 214: game log after the slide-in */
    if (!eid) { setLog([]); return; }'''
OLD_L2 = '''    }).catch(() => { if (!dead) setLog([]); });
    return () => { dead = true; };
  }, [p.id]);'''
NEW_L2 = '''    }).catch(() => { if (!dead) setLog([]); });
    return () => { dead = true; };
  }, [p.id, rd214]);'''

def change(t):
    t = lit(t, "214: ready state", OLD_ST, NEW_ST, "change 214: wait for the slide-in")
    t = lit(t, "214: seasons wait", OLD_H1, NEW_H1, "if (!rd214) return undefined; /* change 214 */")
    t = lit(t, "214: seasons deps", OLD_H2, NEW_H2, "      else setPrev191([]);\n    });\n    return () => { dead = true; };\n  }, [p.id, rd214]);")
    t = lit(t, "214: log wait", OLD_L1, NEW_L1, "change 214: game log after the slide-in")
    t = lit(t, "214: log deps", OLD_L2, NEW_L2, "    }).catch(() => { if (!dead) setLog([]); });\n    return () => { dead = true; };\n  }, [p.id, rd214]);")
    return t

edit(APP, change)
