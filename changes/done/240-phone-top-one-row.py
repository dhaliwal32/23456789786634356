# changes/240-phone-top-one-row.py - Phone top bar in one row: team picture (tap to check for new data, sync dot on it) then the tabs; name row and search button gone; less empty space above the page

NEW_CSS = r'''  /* change 240 (install.py): phone top bar in one row */
  @media (max-width: 640px) {
    .gx-tm103 .hd { display: none; }
    .gx-tm103 .tb { align-items: stretch; padding: 0 2px 0 6px; }
    .gx-tm103 .tb .me240 { flex: none; position: relative; display: flex; align-items: center; justify-content: center; width: 32px; margin-right: 2px; border-bottom: 3px solid transparent; }
    .gx-tm103 .tb .me240 .pc { display: block; width: 26px; height: 26px; border-radius: 99px; overflow: hidden; }
    .gx-tm103 .tb .me240 .pc.sp240 { animation: gx-sp240 .8s ease-in-out; }
    .gx-tm103 .tb .me240 .dt240 { position: absolute; right: 1px; top: 50%; margin-top: 4px; width: 8px; height: 8px; border-radius: 99px; box-shadow: 0 0 0 2px var(--bg); }
    .gx-tm103 .tb a { padding: 13px 1px 10px; font-size: clamp(9.5px, 2.7vw, 12.5px); }
    .max-w-6xl.mx-auto.px-3.py-4 { padding-top: 8px; }
    .gx-bx226 { margin-top: 0 !important; }
  }
  @keyframes gx-sp240 { 0% { transform: rotate(0); } 100% { transform: rotate(360deg); } }
</style>'''

def change(t):
    t = lit(t, "240: styles", "</style>", NEW_CSS, "change 240 (install.py)")
    t = lit(t, "240: team picture at the start of the tabs",
            '      <nav className="tb" ref={ref} aria-label="Main">\n',
            '      <nav className="tb" ref={ref} aria-label="Main">\n'
            '        <button type="button" className="me240" data-gx="240" aria-label={name + ", check for new data"} title={s.lastSync ? "Synced " + fmtTime(s.lastSync) + ". Tap to check for new data" : "Not synced yet"} onClick={(e) => { const pc = e.currentTarget.querySelector(".pc"); if (pc) { pc.classList.remove("sp240"); void pc.offsetWidth; pc.classList.add("sp240"); } if (window.__gxPoll129) window.__gxPoll129(); }}><span className="pc"><GxFtPic114 id={s.me} size={26} /></span><span className="dt240" style={{ background: dot }}></span></button>\n',
            'className="me240" data-gx="240"')
    return t

edit(APP, change)
