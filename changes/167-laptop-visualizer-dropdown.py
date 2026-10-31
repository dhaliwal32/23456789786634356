# changes/167-laptop-visualizer-dropdown.py - laptop Goal Tracker: Goal Visualizer is a drop-down like on the phone, and the goal card text is cleaned up (sizes, spacing, assists lined up under the name)

NEW_CSS = r'''  /* change 167 (install.py) */
  .gx-sd141 .gs { align-items: flex-start; padding: 14px 10px 14px 6px; }
  .gx-sd141 .gs .ar { margin-top: 10px; }
  .gx-sd141 .gs .tp { align-items: center; gap: 12px; }
  .gx-sd141 .gs .nm { color: var(--ink); font-size: 15px; font-weight: 600; line-height: 1.3; }
  .gx-sd141 .gs .nm button { color: inherit; }
  .gx-sd141 .gs .sm { font-size: 12.5px; color: var(--mute); line-height: 1.45; }
  .gx-sd141 .gs .mb { align-self: center; }
  .gx-sd141 .gs .asl { font-size: 13px; line-height: 1.45; margin-top: 10px; padding-left: 58px; }
  .gx-sd141 .gs .asl button { color: var(--ink); }
  .gx-sd141 .gv167 { display: flex; align-items: center; justify-content: center; gap: 6px; width: 100%; margin-top: 12px; padding: 9px; border-radius: 8px; background: var(--card2, var(--bg)); color: var(--ink); font-size: 13px; font-weight: 600; }
  .gx-sd141 .gv167 i { font-style: normal; display: inline-block; transition: transform .25s ease; }
  .gx-sd141 .gv167 i.up { transform: rotate(180deg); }
  .gx-sd141 .gs .gx-rk163 { margin-top: 10px; }
</style>'''

def change(t):
    t = lit(t, "167: styles", "</style>", NEW_CSS, "change 167 (install.py)")
    t = lit(t, "167: laptop drop-down",
            '{r.x.cx != null ? <GxRink163 x={r.x} g={r.g} tm={r.tm} s={s} /> : null}',
            '{r.x.cx != null ? (() => { const k167 = "L" + r.g.id + "-" + r.i, on = !!gv163[k167]; return <><button type="button" className="gv167" onClick={() => setGv163((o) => ({ ...o, [k167]: !on }))}>Goal Visualizer <i className={on ? "up" : ""}>{"\\u25be"}</i></button>{on ? <GxRink163 x={r.x} g={r.g} tm={r.tm} s={s} /> : null}</>; })() : null}',
            'className="gv167"')
    return t

edit(APP, change)
