# changes/218-waivers-dot.py - players on waivers get a small yellow dot by their name instead of the word "waivers"

NEW_CSS = r'''  /* change 218 (install.py): yellow dot for players on waivers */
  .gx-wv218 { display: inline-block; width: 7px; height: 7px; border-radius: 99px; background: var(--warn); margin-left: 6px; vertical-align: middle; flex: none; }
</style>'''

OLD_F = '{r.f.wv ? <span className="text-xs" style={{ color: "var(--warn)", marginLeft: 6 }}>on waivers</span> : null}'
NEW_F = '{r.f.wv ? <i className="gx-wv218" title="On waivers" /> : null}'
OLD_P = '{r.p.wv ? <span className="text-xs" style={{ color: "var(--warn)", marginLeft: 6 }}>on waivers</span> : null}'
NEW_P = '{r.p.wv ? <i className="gx-wv218" title="On waivers" /> : null}'
OLD_OWN = '''const owner = (p) => (p.ft === "fa" ? <span className="text-slate-500">{p.wv ? "Waivers" : "Free agent"}</span> : <TL s={s} id={p.ft} className={p.ft === s.me ? "font-semibold" : ""} />);'''
NEW_OWN = '''const owner = (p) => (p.ft === "fa" ? <span className="text-slate-500">Free agent</span> : <TL s={s} id={p.ft} className={p.ft === s.me ? "font-semibold" : ""} />); /* change 218: waivers shown as a dot by the name */'''
OLD_NM = '''<div className="truncate"><PN p={p} className={me ? "font-semibold" : ""} />{st ? <span'''
NEW_NM = '''<div className="truncate"><PN p={p} className={me ? "font-semibold" : ""} />{p.wv && p.ft === "fa" ? <i className="gx-wv218" title="On waivers" /> : null}{st ? <span'''

def change(t):
    t = lit(t, "218: styles", "</style>", NEW_CSS, "change 218 (install.py)")
    if NEW_F not in t:
        if t.count(OLD_F) != 2:
            fail("218: expected the waivers text twice in the free agent lists")
        t = t.replace(OLD_F, NEW_F)
    t = lit(t, "218: injuries list", OLD_P, NEW_P, '{r.p.wv ? <i className="gx-wv218"')
    t = lit(t, "218: all players owner", OLD_OWN, NEW_OWN, "change 218: waivers shown as a dot by the name")
    t = lit(t, "218: all players name", OLD_NM, NEW_NM, '{p.wv && p.ft === "fa" ? <i className="gx-wv218"')
    return t

edit(APP, change)
