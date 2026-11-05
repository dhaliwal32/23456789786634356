# changes/204-all-players-sort-place.py - Players > All players: a second number on the left, the player's place in the list as it is sorted now (FPTS, Avg, G...), beside his rank

NEW_CSS = r'''  /* change 204 (install.py) */
  .gx-sc99.gx-rk106 > .gx-rk > .gx-n204 { flex-direction: row !important; justify-content: flex-start !important; align-items: center; gap: 0; padding-left: 4px !important; overflow: hidden; white-space: nowrap; font-variant-numeric: tabular-nums; }
  .gx-n204 > b { width: 32px; color: var(--ink); font-weight: 600; }
  .gx-n204 > i { width: 30px; font-style: normal; color: var(--mute); font-size: 12px; }
  .gx-sc99.gx-rk106 > .gx-rk { grid-template-columns: 70px 44px 200px 170px 40px 62px 64px 70px 40px 40px 42px 46px 46px 46px 48px 44px 56px; }
  .gx-sc99.gx-rk106 > .gx-rk > :nth-child(2) { left: 70px; }
  .gx-sc99.gx-rk106 > .gx-rk > :nth-child(3) { left: 114px; }
  @media (max-width: 640px) {
    .gx-sc99.gx-rk106 > .gx-rk { grid-template-columns: 58px 36px 130px 34px 56px 50px 56px 34px 34px 36px 40px 40px 42px 44px 40px 52px; }
    .gx-sc99.gx-rk106 > .gx-rk > :nth-child(2) { left: 58px; }
    .gx-sc99.gx-rk106 > .gx-rk > :nth-child(3) { left: 94px; }
    .gx-sc99.gx-rk106 > .gx-rk > .gx-n204 { padding-left: 2px !important; }
    .gx-n204 > b { width: 28px; font-size: 13px; }
    .gx-n204 > i { width: 28px; font-size: 11px; }
  }
</style>'''

def change(t):
    t = lit(t, "204: styles", "</style>", NEW_CSS, "change 204 (install.py)")
    t = lit(t, "204: index", '{shown.map(({ p, rk, e, sf }) => {', '{shown.map(({ p, rk, e, sf }, i204) => {', '}, i204) => {')
    t = lit(t, "204: two numbers", '<span className="text-slate-500" style={{ paddingLeft: 4 }}>{rk}</span>',
            '<span className="text-slate-500 gx-n204" title="Place in this list, then rank"><b>{i204 + 1}</b><i>{rk}</i></span>', 'gx-n204" title=')
    t = lit(t, "204: heading", '<span>#</span><span></span><span>Player</span><span className="m-hide">Fantasy team</span>',
            '<span className="gx-n204"><b style={{ fontWeight: 400, color: "var(--mute)" }}>#</b><i>Rk</i></span><span></span><span>Player</span><span className="m-hide">Fantasy team</span>', '<i>Rk</i></span>')
    return t

edit(APP, change)
