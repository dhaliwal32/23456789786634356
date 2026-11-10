# changes/251-lines-plates-fabric.py - Lines nameplates look like real plates (brushed metal with screws and engraved letters; gold for hot; real masking tape torn only at the ends for cold) and the jersey gets a fabric grain and soft spotlight

NEW_CSS = r'''  /* change 251 (install.py): real nameplates */
  .gx-fg224.gx-lt227.st246 .md.jr231 .pl232 {
    padding: .7cqw 4.2cqw; border-radius: 1.5px; letter-spacing: .1em; color: #24262a;
    text-shadow: 0 1px 0 rgba(255,255,255,.65), 0 -1px 0 rgba(0,0,0,.28);
    background:
      radial-gradient(circle at 2.1cqw 50%, #3c3f44 0 .45cqw, #e9ebee .55cqw .75cqw, rgba(0,0,0,.35) .8cqw, transparent .95cqw),
      radial-gradient(circle at calc(100% - 2.1cqw) 50%, #3c3f44 0 .45cqw, #e9ebee .55cqw .75cqw, rgba(0,0,0,.35) .8cqw, transparent .95cqw),
      repeating-linear-gradient(90deg, rgba(255,255,255,.10) 0 1px, rgba(0,0,0,.05) 1px 2px, rgba(255,255,255,0) 2px 3px),
      linear-gradient(180deg, #f6f7f9 0%, #d3d6db 42%, #b2b6bd 58%, #e6e8eb 100%);
    box-shadow: 0 0 0 1px rgba(0,0,0,.6), inset 0 1px 0 rgba(255,255,255,.85), inset 0 -1px 0 rgba(0,0,0,.25), 0 2px 3px rgba(0,0,0,.65); }
  .gx-fg224.gx-lt227.st246.h1 .md.jr231 .pl232, .gx-fg224.gx-lt227.st246.h2 .md.jr231 .pl232, .gx-fg224.gx-lt227.st246.h3 .md.jr231 .pl232 {
    color: #3b2804; text-shadow: 0 1px 0 rgba(255,244,200,.8), 0 -1px 0 rgba(80,52,0,.35); letter-spacing: .12em;
    background:
      radial-gradient(circle at 2.1cqw 50%, #5a3f0c 0 .45cqw, #fff0b8 .55cqw .75cqw, rgba(60,40,0,.4) .8cqw, transparent .95cqw),
      radial-gradient(circle at calc(100% - 2.1cqw) 50%, #5a3f0c 0 .45cqw, #fff0b8 .55cqw .75cqw, rgba(60,40,0,.4) .8cqw, transparent .95cqw),
      repeating-linear-gradient(90deg, rgba(255,255,255,.12) 0 1px, rgba(120,80,0,.06) 1px 2px, rgba(255,255,255,0) 2px 3px),
      linear-gradient(180deg, #fff4c4 0%, #e8c25a 40%, #bd8f2b 58%, #f2d47c 100%); }
  .gx-fg224.gx-lt227.st246.h1 .md.jr231 .pl232 { box-shadow: 0 0 0 1px #6f500e, inset 0 1px 0 rgba(255,255,255,.85), inset 0 -1px 0 rgba(0,0,0,.25), 0 2px 3px rgba(0,0,0,.65); }
  .gx-fg224.gx-lt227.st246.c1 .md.jr231 .pl232, .gx-fg224.gx-lt227.st246.c2 .md.jr231 .pl232, .gx-fg224.gx-lt227.st246.c3 .md.jr231 .pl232 {
    padding: .9cqw 4cqw; font-size: clamp(8px, 4.6cqw, 14px); letter-spacing: .03em; color: #161616; text-shadow: none; box-shadow: none; border-radius: 0;
    background:
      linear-gradient(180deg, rgba(255,255,255,.35), rgba(255,255,255,0) 30%, rgba(0,0,0,0) 70%, rgba(0,0,0,.10)),
      repeating-linear-gradient(0deg, rgba(90,70,30,.05) 0 1px, rgba(255,255,255,0) 1px 3px),
      repeating-linear-gradient(90deg, rgba(90,70,30,.035) 0 1px, rgba(255,255,255,0) 1px 4px),
      linear-gradient(180deg, #f1e9cf, #e3d7b2);
    clip-path: polygon(2.5% 0, 97.5% 0, 100% 14%, 97% 30%, 99.5% 47%, 97% 64%, 100% 82%, 97.5% 100%, 2.5% 100%, 0 84%, 3% 68%, 0.5% 50%, 3% 34%, 0 17%); }
  .gx-fg224.gx-lt227.st246.c2 .md.jr231 .pl232 { color: #262626; background: linear-gradient(180deg, rgba(255,255,255,.25), rgba(0,0,0,0) 35%, rgba(60,40,10,.14)), repeating-linear-gradient(0deg, rgba(90,70,30,.06) 0 1px, rgba(255,255,255,0) 1px 3px), radial-gradient(ellipse at 70% 60%, rgba(110,85,40,.22), transparent 55%), linear-gradient(180deg, #e8dcb8, #d4c69c); }
  .gx-fg224.gx-lt227.st246.c3 .md.jr231 .pl232 { color: #333; background: linear-gradient(180deg, rgba(255,255,255,.2), rgba(0,0,0,0) 35%, rgba(60,40,10,.2)), repeating-linear-gradient(0deg, rgba(90,70,30,.07) 0 1px, rgba(255,255,255,0) 1px 3px), radial-gradient(ellipse at 25% 40%, rgba(110,85,40,.28), transparent 50%), radial-gradient(ellipse at 80% 70%, rgba(110,85,40,.24), transparent 45%), linear-gradient(180deg, #dccfa8, #c4b48a); }
  /* available players: a clean soft light behind the jersey and a thin light under the shelf */
  .gx-fg224.gx-lt227.st246.fa::after { display: none !important; }
  .gx-fg224.gx-lt227.st246 .md.jr231 > svg { z-index: 2; }
  .gx-fg224.gx-lt227.st246 .md.jr231 .pl232 { z-index: 3; }
  .gx-fg224.gx-lt227.st246.fa .md.jr231::after { content: ""; position: absolute; inset: 0; z-index: 1; pointer-events: none; mix-blend-mode: screen;
    background: radial-gradient(ellipse 30cqw 3cqw at 50% 25cqw, rgba(255,246,222,.9), rgba(255,240,210,0) 100%), radial-gradient(ellipse 34cqw 30cqw at 50% 48cqw, rgba(255,236,200,.42), rgba(255,226,180,.12) 55%, rgba(255,220,170,0) 80%); }
  @media (max-width: 640px) { .gx-fg224.gx-lt227.st246.fa .md.jr231::after { background: radial-gradient(ellipse 40cqw 3.6cqw at 50% 20cqw, rgba(255,246,222,.9), rgba(255,240,210,0) 100%), radial-gradient(ellipse 44cqw 38cqw at 50% 48cqw, rgba(255,236,200,.42), rgba(255,226,180,.12) 55%, rgba(255,220,170,0) 80%); } }
  .gx-fg224.gx-lt227.st246.fa .md.jr231 svg { filter: brightness(1.08) drop-shadow(0 0 1.6cqw rgba(255,228,170,.35)) drop-shadow(0 1.5cqw 2cqw rgba(0,0,0,.55)) !important; }
</style>'''

FABRIC = r'''
        <rect x="0" y="0" width="120" height="140" filter={"url(#" + id + "g)"} style={{ opacity: 0.22, mixBlendMode: "overlay" }} />{/* change 251: fabric grain */}
        <rect x="0" y="0" width="120" height="140" style={{ fill: "url(#" + id + "l)" }} />'''

def change(t):
    t = lit(t, "251: styles", "</style>", NEW_CSS, "change 251 (install.py): real nameplates")
    t = lit(t, "251: grain and light definitions",
            '<clipPath id={id + "c"}><path d={shirt} /></clipPath>',
            '<clipPath id={id + "c"}><path d={shirt} /></clipPath>\n        <filter id={id + "g"} x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="7" /><feColorMatrix type="saturate" values="0" /></filter>\n        <radialGradient id={id + "l"} cx="50%" cy="10%" r="75%"><stop offset="0" stopColor="#fff3dc" stopOpacity=".26" /><stop offset=".55" stopColor="#fff3dc" stopOpacity=".05" /><stop offset="1" stopColor="#000" stopOpacity=".22" /></radialGradient>',
            '<filter id={id + "g"} x="0" y="0" width="100%" height="100%"><feTurbulence')
    t = lit(t, "251: grain and light on the jersey",
            '''        <path d="M45 22 Q34 36 24 58 M75 22 Q86 36 96 58" style={{ fill: "none", stroke: "rgba(0,0,0,.28)", strokeWidth: 0.6, strokeDasharray: "1.4 1.2" }} />''',
            '''        <path d="M45 22 Q34 36 24 58 M75 22 Q86 36 96 58" style={{ fill: "none", stroke: "rgba(0,0,0,.28)", strokeWidth: 0.6, strokeDasharray: "1.4 1.2" }} />''' + FABRIC,
            "change 251: fabric grain")
    return t

edit(APP, change)
