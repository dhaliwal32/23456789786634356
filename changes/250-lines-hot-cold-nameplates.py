# changes/250-lines-phone-zoom-badges.py - Lines on the phone: stall zoomed in so the jersey and nameplate are bigger; hot and cold shown on the nameplate (hot: clean gold plate in a fancy engraved font, cold: cheap tape label in scrawled marker), trophies and cobwebs removed

NEW_CSS = r'''  /* change 250 (install.py): phone stall zoom, hot and cold nameplates */
  @font-face { font-family: "GxFancy250"; src: url(fonts/cinzel-700.woff2) format("woff2"); font-weight: 700; font-display: swap; }
  @font-face { font-family: "GxMarker250"; src: url(fonts/marker-400.woff2) format("woff2"); font-weight: 400; font-display: swap; }
  @media (max-width: 640px) {
    .gx-fg224.gx-lt227.st246 { background-image: none !important; background-color: #0c0c0e !important; }
    .gx-fg224.gx-lt227.st246 > .md.jr231 { background: var(--st) 50% -13.5cqw / 135% auto no-repeat; overflow: hidden !important; }
    .gx-fg224.gx-lt227.st246 .md.jr231 .pl232 { top: 12.8cqw; max-width: 66cqw; font-size: clamp(7.5px, 4.4cqw, 13px); padding: .8cqw 2cqw; }
    .gx-fg224.gx-lt227.st246 .md.jr231 svg { left: 21.6cqw; top: 21.6cqw; width: 56.8cqw !important; }
  }
  .gx-fg224.gx-lt227.st246 .hc248 { display: none !important; }
  /* hot: polished gold plate, engraved serif capitals; more shine and glow the hotter */
  .gx-fg224.gx-lt227.st246.h1 .md.jr231 .pl232, .gx-fg224.gx-lt227.st246.h2 .md.jr231 .pl232, .gx-fg224.gx-lt227.st246.h3 .md.jr231 .pl232 {
    font-family: "GxFancy250", "Didot", "Bodoni 72", Georgia, serif; font-weight: 700; letter-spacing: .12em; color: #3a2704; border-radius: 2px;
    text-shadow: 0 1px 0 rgba(255,246,200,.75), 0 -1px 0 rgba(90,60,0,.35);
    background: linear-gradient(180deg, #fff2b8 0%, #e9c45a 28%, #c6952a 55%, #f3d277 78%, #b98a22 100%);
    box-shadow: 0 0 0 1px #7a5a12, inset 0 1px 0 rgba(255,255,255,.7), inset 0 -1px 0 rgba(0,0,0,.25), 0 2px 4px rgba(0,0,0,.6); }
  .gx-fg224.gx-lt227.st246.h2 .md.jr231 .pl232 { box-shadow: 0 0 0 1px #7a5a12, inset 0 1px 0 rgba(255,255,255,.8), 0 0 8px rgba(255,200,80,.55), 0 2px 4px rgba(0,0,0,.6); }
  .gx-fg224.gx-lt227.st246.h3 .md.jr231 .pl232 { overflow: hidden; box-shadow: 0 0 0 1px #8a6510, inset 0 1px 0 rgba(255,255,255,.9), 0 0 14px rgba(255,205,90,.85), 0 0 3px rgba(255,240,180,.9), 0 2px 4px rgba(0,0,0,.6); }
  .gx-fg224.gx-lt227.st246.h3 .md.jr231 .pl232::after { content: ""; position: absolute; top: 0; bottom: 0; left: -60%; width: 40%; background: linear-gradient(100deg, transparent, rgba(255,255,255,.75), transparent); animation: gx-sh250 2.8s ease-in-out infinite; }
  @keyframes gx-sh250 { 0% { left: -60%; } 55%, 100% { left: 120%; } }
  /* cold: cheap masking tape label, scrawled marker; more crooked and worn the colder */
  .gx-fg224.gx-lt227.st246.c1 .md.jr231 .pl232, .gx-fg224.gx-lt227.st246.c2 .md.jr231 .pl232, .gx-fg224.gx-lt227.st246.c3 .md.jr231 .pl232 {
    font-family: "GxMarker250", "Marker Felt", "Chalkboard SE", "Comic Sans MS", cursive; font-weight: 400; letter-spacing: .02em; text-transform: none; color: #2b2b2b; border-radius: 0;
    background: linear-gradient(180deg, rgba(232,222,190,.97), rgba(214,203,168,.97)); box-shadow: 0 1px 2px rgba(0,0,0,.45); text-shadow: none;
    clip-path: polygon(0 8%, 6% 0, 14% 6%, 24% 0, 38% 5%, 52% 0, 66% 6%, 80% 0, 92% 5%, 100% 0, 98% 92%, 90% 100%, 78% 94%, 62% 100%, 48% 95%, 32% 100%, 18% 94%, 6% 100%, 0 93%); }
  .gx-fg224.gx-lt227.st246.c1 .md.jr231 .pl232 { transform: translate(-50%, -50%) rotate(-2deg); }
  .gx-fg224.gx-lt227.st246.c2 .md.jr231 .pl232 { transform: translate(-50%, -50%) rotate(-5deg); color: #3a3a3a; background: linear-gradient(180deg, rgba(220,210,178,.95), rgba(196,186,150,.95)); }
  .gx-fg224.gx-lt227.st246.c3 .md.jr231 .pl232 { transform: translate(-47%, -40%) rotate(8deg); color: #4a4a4a; opacity: .9; background: linear-gradient(180deg, rgba(205,196,165,.92), rgba(176,166,130,.92)); text-decoration: line-through; text-decoration-color: rgba(160,20,20,.75); text-decoration-thickness: 1.5px; }
  @media (prefers-reduced-motion: reduce) { .gx-fg224.gx-lt227.st246.h3 .md.jr231 .pl232::after { animation: none; display: none; } }
</style>'''

def change(t):
    t = lit(t, "250: styles", "</style>", NEW_CSS, "change 250 (install.py)")
    t = lit(t, "250: no trophies or cobwebs",
            '''<GxJersey232 t={p ? p.t : t} name={last} no={gxNo248(T, n)} goalie={isG} /></div><GxHC248 k={gxHC248(p, h248, s)} />''',
            '''<GxJersey232 t={p ? p.t : t} name={last} no={gxNo248(T, n)} goalie={isG} /></div>{/* change 250: hot and cold shown on the nameplate */}''',
            "change 250: hot and cold shown on the nameplate")
    return t

edit(APP, change)
