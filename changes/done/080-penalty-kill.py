# changes/080-penalty-kill.py - Lines: each team now shows Penalty kill 1 and Penalty kill 2 under the power plays (from Daily Faceoff)

# 1. The sync (gm_lines.py) saves the two penalty-kill units it already reads from Daily Faceoff.
def lines_py(t):
    t = lit(t, "080: count PK slots",
            'SLOTS = ES + ["PP1", "PP2", "G"]',
            'SLOTS = ES + ["PP1", "PP2", "PK1", "PK2", "G"]  # change 080: penalty kill',
            "change 080: penalty kill")
    t = lit(t, "080: save PK units",
            "        out[\"G\"] = sorted(g)\n    return out\n",
            "        out[\"G\"] = sorted(g)\n"
            "    # change 080: penalty-kill units (pk1, pk2) from the same Daily Faceoff page\n"
            "    try:\n"
            "        for gi in (\"pk1\", \"pk2\"):\n"
            "            m = (DFPOS.get(t) or {}).get(gi) or {}\n"
            "            if 3 <= len(m) <= 6:\n"
            "                out[gi.upper()] = sorted(m)\n"
            "    except Exception:\n"
            "        pass\n"
            "    return out\n",
            "change 080: penalty-kill units")
    return t


edit("gm_lines.py", lines_py)


# 2. The Lines page (lines-tab.js) shows them under the power plays.
def lines_tab(t):
    t = lit(t, "080: PK cards skip line tags",
            'const w = ctx.where[k + "|" + t] || {}, ch = mode === "pp" ? null : ctx.latestES[k + "|" + t];\n    const bits = [];\n    if (mode !== "pp" && w.pp) bits.push(w.pp);',
            'const w = ctx.where[k + "|" + t] || {}, ch = mode !== "es" ? null : ctx.latestES[k + "|" + t]; /* change 080 */\n    const bits = [];\n    if (mode === "es" && w.pp) bits.push(w.pp);',
            'mode !== "es" ? null : ctx.latestES[k + "|" + t]; /* change 080 */')
    t = lit(t, "080: PK unit layout",
            "    return (\n      <div>\n        <div className=\"lt-rink\">",
            "    // change 080: a penalty-kill unit, forwards on top and defence below\n"
            "    const pkUnit = (sl) => {\n"
            "      const arr = ln[sl] || [];\n"
            "      if (!arr.length) return <div className=\"lt-msg\">Not available.</div>;\n"
            "      const fw = arr.filter((n) => gOf(n) !== \"D\").sort((a, b) => val(b, \"F\") - val(a, \"F\")), df = arr.filter((n) => gOf(n) === \"D\").sort((a, b) => val(b, \"D\") - val(a, \"D\"));\n"
            "      const pkc = (n) => card(n, gOf(n), gOf(n) === \"D\" ? \"D\" : \"F\", \"pk\", sl + n);\n"
            "      return <div>{fw.length ? <div className=\"lt-ppd\" style={{ marginTop: 0 }}>{fw.map(pkc)}</div> : null}{df.length ? <div className=\"lt-ppd\">{df.map(pkc)}</div> : null}</div>;\n"
            "    };\n"
            "    const hasPK = (ln.PK1 || []).length || (ln.PK2 || []).length;\n"
            "    return (\n      <div>\n        <div className=\"lt-rink\">",
            "change 080: a penalty-kill unit")
    t = lit(t, "080: show PK sections",
            "        <div className=\"lt-sec\">Power play 2</div>\n        {unit(\"PP2\")}\n",
            "        <div className=\"lt-sec\">Power play 2</div>\n        {unit(\"PP2\")}\n"
            "        {hasPK ? <React.Fragment><div className=\"lt-sec\">Penalty kill 1</div>{pkUnit(\"PK1\")}<div className=\"lt-sec\">Penalty kill 2</div>{pkUnit(\"PK2\")}</React.Fragment> : null}\n",
            "Penalty kill 1")
    return t


edit("lines-tab.js", lines_tab)
