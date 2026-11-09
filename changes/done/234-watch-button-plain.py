# changes/234-watch-button-plain.py - Watch buttons in the app's own button style instead of blue

NEW_CSS = r'''  /* change 234 (install.py): Watch buttons match the app */
  .gx-gc140 .c179 .wt179, .gx-sd141 .gm .wt181 { background: var(--card3, var(--card2)); color: var(--ink); border: 1px solid var(--line2); }
  .gx-gc140 .c179 .wt179:active, .gx-sd141 .gm .wt181:active { background: var(--hover); }
  .gx-sd141 .gm .wt181:hover { filter: none; border-color: var(--mute); }
</style>'''

def change(t):
    t = lit(t, "234: styles", "</style>", NEW_CSS, "change 234 (install.py)")
    return t

edit(APP, change)
