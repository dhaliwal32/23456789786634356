# changes/166-on-ice-dropdown.py - goal replay: just the circles with numbers; the "On the ice" list with plus/minus is hidden behind a drop-down, closed by default

NEW_CSS = r'''  /* change 166 (install.py) */
  .gx-ed165 .dd166 { display: flex; align-items: center; justify-content: center; gap: 6px; width: 100%; margin-top: 8px; padding: 8px; border-radius: 8px; background: var(--card2, var(--bg)); color: var(--mute); font-size: 13px; }
  .gx-ed165 .dd166 i { font-style: normal; display: inline-block; transition: transform .25s ease; }
  .gx-ed165 .dd166 i.up { transform: rotate(180deg); }
</style>'''

def change(t):
    t = lit(t, "166: styles", "</style>", NEW_CSS, "change 166 (install.py)")
    t = lit(t, "166: closed by default", "  const [run, setRun] = useState(0);\n", "  const [run, setRun] = useState(0);\n  const [ol166, setOl166] = useState(false);\n", "const [ol166, setOl166] = useState(false);")
    t = lit(t, "166: drop-down",
            '      <div className="ol">\n        <div className="hd">',
            '      <button type="button" className="dd166" onClick={() => setOl166(!ol166)}>Who was on the ice <i className={ol166 ? "up" : ""}>{"\\u25be"}</i></button>\n      <div className="ol" style={ol166 ? null : { display: "none" }}>\n        <div className="hd">',
            'className="dd166"')
    return t

edit(APP, change)
