# changes/292-rink-scrolls.py - live game view: the rink no longer stays stuck at the top while you scroll; the whole game page scrolls together

NEW_CSS = r'''  /* change 292 (install.py) */
  .gx-tk264 .pn267 { position: static; box-shadow: none; }
</style>'''


def change(t):
    t = lit(t, "292: styles", "</style>", NEW_CSS, "change 292 (install.py)")
    return t

edit(APP, change)
