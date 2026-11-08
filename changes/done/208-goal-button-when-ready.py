# changes/208-goal-button-when-ready.py - Goal button shows only once the replay or the video is in; one On ice (the pill inside the visualizer is gone)

HELPERS = r'''// ---------- change 208: goal button only when the replay or video is ready (install.py) ----------
function GxGv208({ x, g, tm, children }) {
  const e = useEdge165(x, g, tm);
  if (!x || !(e || x.vid185)) return null;
  return children(e && x.vid185 ? "Video and Visualizer" : x.vid185 ? "Video" : "Goal Visualizer");
}
'''

OLD_LBL = '{r.x.vid185 ? "Video and Visualizer" : "Goal Visualizer"}'


def gate(t, label, start, end):
    """Wrap one goal button: from `start` to the first `end` after it."""
    if "GxGv208 x={r.x} g={r.g} tm={r.tm}>{(lb208) => { const " + label in t:
        print("208: " + label + " already done")
        return t
    if t.count(start) != 1:
        fail("208: start for " + label + " found " + str(t.count(start)) + " times")
    i = t.find(start)
    j = t.find(end, i)
    if j < 0:
        fail("208: end for " + label + " not found")
    seg = t[i:j + len(end)]
    if seg.count(OLD_LBL) != 1:
        fail("208: label for " + label + " found " + str(seg.count(OLD_LBL)) + " times")
    new = seg.replace(start, "{<GxGv208 x={r.x} g={r.g} tm={r.tm}>{(lb208) => { const " + label, 1)
    new = new.replace(OLD_LBL, "{lb208}", 1)
    new = new[: -len(end)] + end.replace("})() : null}", "}}</GxGv208>}", 1)
    return t[:i] + new + t[j + len(end):]


def change(t):
    t = lit(t, "208: helpers", ROOT, HELPERS + ROOT, "change 208: goal button only when")
    # laptop Goal Tracker
    t = gate(t, "k167", "{r.x.cx != null || r.x.vid185 ? (() => { const k167",
             '</GxGvModal169> : null}</>; })() : null}<GxOi205 x={r.x} g={r.g} tm={r.tm} s={s} cls="gv167" />')
    # game view GAME tab
    t = gate(t, "k173", "{r.x.cx != null || r.x.vid185 ? (() => { const k173",
             '</div> : null}</>; })() : null}<GxOi205 x={r.x} g={r.g} tm={r.tm} s={s} cls="gv173" />')
    # phone Goal Tracker cards
    t = gate(t, "k163", "{r.x.cx != null || r.x.vid185 ? (() => { const k163",
             '</div> : null}</>; })() : null}<GxOi205 x={r.x} g={r.g} tm={r.tm} s={s} cls="gv163" />')
    # inside the box: Visualizer only means the real replay, not the still picture
    t = lit(t, "208: switch only with both",
            '{x.vid185 ? <div className="sg185" data-gx="185">',
            '{x.vid185 && e165 ? <div className="sg185" data-gx="185" data-gx208="1">',
            'data-gx208="1"')
    t = lit(t, "208: video first when no replay",
            'const vw = x.vid185 ? vw185 || ((isNaN(cx) || isNaN(cy)) && !e165 ? "v" : "z") : "z";',
            'const vw = x.vid185 ? (e165 ? vw185 || "z" : "v") : "z"; /* change 208 */',
            '(e165 ? vw185 || "z" : "v") : "z"; /* change 208 */')
    # one On ice: remove the pill inside the visualizer (the drop-down under the button stays)
    t = lit(t, "208: no On ice pill in the visualizer",
            '        <button type="button" className="oi184" onClick={() => setOl166(!ol166)}>On ice <i className={ol166 ? "up" : ""}>{"\\u25be"}</i></button>\n',
            '        {/* change 208: On ice pill removed */}\n',
            "change 208: On ice pill removed")
    return t


edit(APP, change)
