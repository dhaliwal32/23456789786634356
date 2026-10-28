# changes/097-espn-faces.py - player faces like ESPN: bigger square head-and-shoulders photo, no circle, no logo badge; jersey numbers read right away

NEW_CSS = r'''  /* change 097 (install.py) */
  :root { --gx-fs: 1.6; }
  @media (max-width: 640px) { :root { --gx-fs: 1.3; } }
  .gx-face > .c { border-radius: 6px; background: transparent; box-shadow: none; }
  .gx-face > .c > img { object-fit: cover; object-position: center bottom; transform: none; }
  .gx-face > .bd { display: none; }
  /* make room for the bigger photos in each list */
  .adv-head, .adv-row { grid-template-columns: 44px minmax(0,1fr) 60px 74px 36px; }
  .gx-ro { grid-template-columns: 44px minmax(0,1fr) 62px 60px 40px 54px 96px 62px 64px; }
  .gx-pk { grid-template-columns: 44px minmax(0,1fr) 52px 46px 66px 58px 56px; }
  .gx-gl { grid-template-columns: 42px minmax(0,1fr) 104px 44px 60px; }
  .gx-lt { grid-template-columns: 40px minmax(0,1fr) 52px 60px 68px 100px; }
  .gx-rk { grid-template-columns: 38px 42px minmax(0,1fr) 170px 40px 64px 70px; }
  .gx-hs83 { grid-template-columns: 42px minmax(0,1fr) 58px 58px; }
  .gx-ij85 { grid-template-columns: 42px minmax(0,1fr) 48px; }
  @media (max-width: 640px) {
    .m-rrow { grid-template-columns: 36px minmax(0,1fr) 42px 34px 46px; }
    .adv-head, .adv-row { grid-template-columns: 34px minmax(0,1fr) 46px 64px 18px; }
    .gx-ro { grid-template-columns: 30px minmax(0,1fr) 36px 44px 42px 46px; }
    .gx-pk { grid-template-columns: 34px minmax(0,1fr) 52px 46px; }
    .gx-gl { grid-template-columns: 32px minmax(0,1fr) 92px 52px; }
    .gx-lt { grid-template-columns: 28px minmax(0,1fr) 44px 88px; }
    .gx-rk { grid-template-columns: 30px 30px minmax(0,1fr) 50px 56px; }
    .gx-hs83 { grid-template-columns: 34px minmax(0,1fr) 58px 58px; }
    .gx-ij85 { grid-template-columns: 34px minmax(0,1fr) 48px; }
    .gx-h2h .gx-face > .c > img { width: 100% !important; height: 100% !important; }
  }
</style>'''

OLD_BOX = '<span className="gx-face" style={{ width: z, height: z }} title={(p.n || "") + " (" + tm + ")"}>'
NEW_BOX = '<span className="gx-face" style={{ width: "calc(" + z + "px * var(--gx-fs, 1))", height: "calc(" + z + "px * var(--gx-fs, 1))" }} title={(p.n || "") + " (" + tm + ")"}>'


def change(t):
    t = lit(t, "097: styles", "</style>", NEW_CSS, "change 097 (install.py)")
    t = lit(t, "097: bigger photo box", OLD_BOX, NEW_BOX, 'var(--gx-fs, 1))", height:')
    return t


edit(APP, change)


# read the NHL rosters on the next sync if no jersey numbers are saved yet (instead of waiting up to 2 hours)
def lines(t):
    t = lit(t, "097: read rosters now for jersey numbers",
            "    due = force or not last or now - last >= timedelta(hours=every)\n",
            "    due = force or not last or now - last >= timedelta(hours=every)\n"
            "    if not due and not any(\"no\" in v for pl in (state.get(\"rosters\") or {}).values() for v in pl.values()):\n"
            "        print(\"(lines) no jersey numbers saved yet - reading rosters now\")\n"
            "        due = True\n",
            "no jersey numbers saved yet - reading rosters now")
    return t


edit("gm_lines.py", lines)
