# changes/235-jersey-long-sleeves.py - Lines jerseys: long sleeves, names always fit (Firefox too), number and details under the jersey no longer covered

NEW_CSS = r'''  /* change 235 (install.py): jersey fixes */
  .gx-fg224.gx-lt227 .md.jr231 { aspect-ratio: auto; height: auto; }
  .gx-fg224.gx-lt227 .md.jr231 svg { height: auto; aspect-ratio: 120 / 140; }
  .gx-fg224.gx-lt227 .sb227 { position: relative; z-index: 2; margin-top: 3px; }
</style>'''

R = [
  ("235: long sleeves",
   'const shirt = "M44 20 Q60 29 76 20 L100 26 Q112 31 116 43 L119 78 L102 83 L96 58 L96 128 Q60 134 24 128 L24 58 L18 83 L1 78 L4 43 Q8 31 20 26 Z";',
   'const shirt = "M44 20 Q60 29 76 20 L100 26 Q112 31 115 42 L120 112 L103 117 L96 62 L96 128 Q60 134 24 128 L24 62 L17 117 L0 112 L5 42 Q8 31 20 26 Z"; /* change 235 */',
   "L120 112 L103 117 L96 62"),
  ("235: stripes on long sleeves",
   "{band(60, 0, 24)}{band(60, 96, 24)}{band(108, 0, 120)}",
   "{band(80, 0, 26)}{band(80, 94, 26)}{band(108, 24, 72)}",
   "{band(80, 0, 26)}"),
  ("235: cuffs at the wrists",
   '<path d="M0 74 L22 80 L22 86 L0 80 Z M120 74 L98 80 L98 86 L120 80 Z" style={{ fill: trim }} />',
   '<path d="M0 104 L19 109 L18 117 L0 112 Z M120 104 L101 109 L102 117 L120 112 Z" style={{ fill: trim }} />',
   "M0 104 L19 109 L18 117"),
  ("235: names fit by size",
   "const nmSize = 9.5, nmW = nm.length * nmSize * 0.8, NMMAX = 58;",
   "const nmSize = Math.min(9.5, 60 / Math.max(1, nm.length * 0.86)), nmW = 0, NMMAX = 58;",
   "60 / Math.max(1, nm.length * 0.86)"),
]

def change(t):
    t = lit(t, "235: styles", "</style>", NEW_CSS, "change 235 (install.py): jersey fixes")
    for label, old, new, mark in R:
        t = lit(t, label, old, new, mark)
    return t

edit(APP, change)
