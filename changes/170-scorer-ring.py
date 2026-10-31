# changes/170-scorer-ring.py - goal replay: an extra ring around the player who scored

def change(t):
    return lit(t, "170: scorer ring",
               '<circle cx={o[3]} cy={o[4]} r="3.7" className="t169" style={gxCol169(o[1] === scT ? C169.sc : C169.ot, 0)} />',
               '{F.scorer && String(o[0]) === String(F.scorer) ? <><circle cx={o[3]} cy={o[4]} r="5.6" fill="none" stroke="#111111" strokeWidth="0.35" opacity=".6" /><circle cx={o[3]} cy={o[4]} r="5.2" fill="none" stroke={C169.sc.f} strokeWidth="1" data-gx="170" /></> : null}<circle cx={o[3]} cy={o[4]} r="3.7" className="t169" style={gxCol169(o[1] === scT ? C169.sc : C169.ot, 0)} />',
               'data-gx="170"')

edit(APP, change)
