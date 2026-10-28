# changes/128-star-line-alert.py - phone alert when a free agent moves onto a superstar's line, e.g. "Holloway joined McDavid's line (EDM)". Superstars are the 30 forwards with the highest ESPN projection per game


def change(t):
    t = lit(t, "128: find free agents on a star's line",
            '        c["who"] = relevance(c, p)\n    old = state.get("changes") or []\n',
            '''        c["who"] = relevance(c, p)
    # change 128: a free agent who moves onto a superstar's line
    try:
        fw = [p for p in players if p.get("p") == "F"]
        stars = {norm(p["n"]): p["n"] for p in sorted(fw, key=lambda p: -(p.get("pavg") or 0))[:30]}
        lines_now = state.get("lines") or {}
        for c in new:
            if c["type"] not in ("line", "lineup") or c["dir"] not in ("up", "in", "") or not str(c.get("to") or "").startswith("F"):
                continue
            p = by_id.get(c.get("e") or "")
            if not p or p.get("ft"):
                continue
            mates = (lines_now.get(c["team"]) or {}).get(c["to"]) or []
            star = [stars[norm(m)] for m in mates if norm(m) != c["key"] and norm(m) in stars]
            if star:
                c["who"], c["star"] = "star", star[0]
    except Exception:
        print(f"(lines) WARNING star line check failed:\\n{traceback.format_exc()}")
    old = state.get("changes") or []
''', "change 128: a free agent who moves onto a superstar's line")
    t = lit(t, "128: short star line alert",
            "    last = str(c.get(\"name\") or \"\").split()[-1] if c.get(\"name\") else \"\"\n",
            "    last = str(c.get(\"name\") or \"\").split()[-1] if c.get(\"name\") else \"\"\n"
            "    if c.get(\"who\") == \"star\" and c.get(\"star\"):\n"
            "        return \"Fantasy GM\", f\"{last} joined {str(c['star']).split()[-1]}'s line ({c['team']})\"\n",
            "if c.get(\"who\") == \"star\" and c.get(\"star\"):")
    return t


edit("gm_lines.py", change)
