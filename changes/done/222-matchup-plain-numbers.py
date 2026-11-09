# changes/222-matchup-plain-numbers.py - Matchup margin line, day +/- and week Summary margin in plain colours, no green or red

def change(t):
    t = lit(t, "222: margin line", 'color: !mine ? "var(--ink2, var(--ink))" : margin >= 0 ? "var(--good)" : "var(--bad)"',
            'color: "var(--ink2, var(--ink))" /* change 222: plain */', 'color: "var(--ink2, var(--ink))" /* change 222: plain */')
    t = lit(t, "222: day menu", 'const col = (v) => ({ color: !mine || Math.abs(v) < 0.05 ? "var(--mute)" : v > 0 ? "var(--good)" : "var(--bad)" });',
            'const col = (v) => ({ color: "var(--mute)" }); /* change 222: plain */', 'const col = (v) => ({ color: "var(--mute)" }); /* change 222: plain */')
    t = lit(t, "222: week summary", '<div className="text-right" style={{ color: !mine || Math.abs(dw) < 0.05 ? "var(--mute)" : dw > 0 ? "var(--good)" : "var(--bad)" }}>',
            '<div className="text-right" style={{ color: "var(--mute)" /* change 222: plain */ }}>', '<div className="text-right" style={{ color: "var(--mute)" /* change 222: plain */ }}>')
    return t

edit(APP, change)
