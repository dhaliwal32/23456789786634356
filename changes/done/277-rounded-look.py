# changes/277-rounded-look.py - cleaner look everywhere: every card has soft rounded corners, and the switches (Table / My team, Standings / Strength, Theme...) become soft grey sliders like on the iPhone

NEW_CSS = r'''  /* change 277 (install.py) */
  :root { --seg277: #3a3c43; }
  html[data-theme="light"] { --seg277: #ffffff; }
  html { -webkit-tap-highlight-color: transparent; }
  .gx-pn { border-radius: 16px; }
  .gx-pn.full { border-radius: 0; }
  @media (max-width: 640px) { .gx-pn { border-radius: 14px; } }
  .gx-seg, .gx-seg103 { border: 0; border-radius: 10px; padding: 2px; gap: 2px; background: var(--accentSoft); overflow: visible; }
  .gx-seg button, .gx-seg103 button { border-left: 0; border-radius: 8px; }
  .gx-seg button.on, .gx-seg103 button.on { background: var(--seg277); color: var(--ink); font-weight: 600; box-shadow: 0 1px 3px rgba(0,0,0,.28); }
</style>'''


def change(t):
    t = lit(t, "277: styles", "</style>", NEW_CSS, "change 277 (install.py)")
    return t

edit(APP, change)
