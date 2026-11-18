# changes/317-no-lead-alerts.py - no more "You lead" / "they lead" phone alerts (Kuvar, Nov 17); goal and assist alerts stay. To bring them back, delete the "if True:" lines this adds.

def go(t):
    t = lit(t, "317: lead alerts off",
            '''                if side > 0:
                    push("Fantasy GM", f"You lead {a:.1f} to {b:.1f}")''',
            '''                if True:  # change 317: lead alerts off (Kuvar, Nov 17); delete this line and the "pass" under it, and change the next "elif" to "if", to bring them back
                    pass
                elif side > 0:
                    push("Fantasy GM", f"You lead {a:.1f} to {b:.1f}")''',
            'change 317: lead alerts off')
    py_ok("gm_live.py", t)
    return t


edit("gm_live.py", go)
