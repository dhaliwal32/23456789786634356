# changes/115-home-week-side.py - home page week chart: the empty space on the right now shows games left (or games this week), days won (or days ahead) and a Week column with both totals and total lineup games, lined up with the day columns

SIDE = r'''        {/* gx115: right side of the week chart */}
        {(() => { const sy = Math.max(ya, yb) + 26, gx = lx + (W - lx) / 2 - 4, lab = { fontSize: fs - 1, fill: "var(--mute)" }, val = { fontSize: fs, fill: "var(--ink)", fontWeight: 600 };
          return (<g>
            {sy + 50 < base ? <><text x={lx} y={sy} style={lab}>{up ? "Games" : "Games left"}</text>
            <text x={lx} y={sy + 15} style={val}>{(up ? totG(X) : X.used) + "–" + (up ? totG(Y) : Y.used)}</text>
            <text x={lx} y={sy + 36} style={lab}>{done ? "Days won" : "Days ahead"}</text>
            <text x={lx} y={sy + 51} style={val}>{won + " of " + (done || n)}</text></> : null}
            <text x={gx} y={192} textAnchor="middle" style={{ fontSize: fs, fill: "var(--ink)", fontWeight: 600 }}>Week</text>
            {narrow ? <text x={gx} y={208} textAnchor="middle" style={{ fontSize: fs, fill: CA[n - 1] > CB[n - 1] ? "var(--good)" : "var(--ink2)", fontWeight: 600 }}>{Math.round(CA[n - 1])}</text> : <text x={gx} y={209} textAnchor="middle" style={{ fontSize: fs, fill: CA[n - 1] > CB[n - 1] ? "var(--good)" : "var(--ink2)", fontWeight: 600 }}>{Math.round(CA[n - 1]) + "–" + Math.round(CB[n - 1])}</text>}
            {narrow ? <text x={gx} y={223} textAnchor="middle" style={{ fontSize: fs, fill: "var(--mute)", fontWeight: 600 }}>{Math.round(CB[n - 1])}</text> : null}
            {gxGopt105() === "text" ? <text x={gx} y={Hh - 4} textAnchor="middle" style={{ fontSize: fs - 1, fill: "var(--mute)" }}>{totG(X) + "–" + totG(Y)}</text> : null}
          </g>); })()}
'''


def change(t):
    old = '''        <text x={lx} y={yb} style={{ fontSize: fs, fill: "var(--mute)" }}>{nm + " " + Math.round(CB[n - 1])}</text>
'''
    return lit(t, "115: week chart right side", old, old + SIDE, "gx115: right side of the week chart")


edit(APP, change)
