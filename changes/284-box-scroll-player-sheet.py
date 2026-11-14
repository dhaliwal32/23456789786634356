# changes/284-box-scroll-player-sheet.py - Roster box: every side scrolls with your finger (the side facing you lies flat once the box stops turning, which the iPhone needs); phone player screen is a sheet with a dark strip on top, tap the strip to close; ntfy switched off, alerts come only from the app

NEW_CSS = r'''  /* change 284 (install.py) */
  .gx-bx225 .pr.rs284 { transform: none !important; transform-style: flat !important; will-change: auto; }
  .gx-bx225 .pr.rs284 > .fc { transform: none !important; visibility: hidden; }
  .gx-bx225 .pr.rs284 > .fc.fr284 { visibility: visible; }
  .gx-bx225 .pr.rs284 > .fc.fr284:not(.gf252) { overflow-y: auto; overscroll-behavior: contain; -webkit-overflow-scrolling: touch; touch-action: pan-y; }
  @media (max-width: 640px) {
    .gx-pd-ov { background: rgba(0,0,0,.6); }
    .gx-pd { margin: 52px 0 0; min-height: calc(100% - 52px); border-radius: 18px 18px 0 0; }
    .gx-pd::before { content: ""; position: absolute; top: 7px; left: 50%; width: 40px; height: 5px; margin-left: -20px; border-radius: 99px; background: rgba(255,255,255,.45); z-index: 4; pointer-events: none; }
    .gx-pd-ov.out .gx-pd { transform: translateY(60vh); }
  }
</style>'''

FX_OLD = r'''  useEffect(() => { try { if (uiGet().bx255 !== k) uiSet("bx255", k); } catch (e) {} }, [k]);'''
FX_NEW = FX_OLD + r'''
  /* change 284: once the box has stopped turning, the side facing you lies flat so it scrolls on the iPhone; a sideways drag or a turn stands the box up again */
  useEffect(() => {
    const el = pr.current, box = stg.current;
    if (!el || !box) return;
    const rest = () => { el.__t284 = 0; el.__rest284 = el.style.transform; [...el.children].forEach((f, j) => f.classList.toggle("fr284", j === el.__k284)); el.classList.add("rs284"); };
    const wake = (turning) => {
      clearTimeout(el.__t284); el.__t284 = 0;
      if (!el.classList.contains("rs284")) return;
      // stand the box up exactly where it was resting first, so a turn starts from the right place
      const to = el.style.transform;
      el.classList.remove("an"); el.style.transform = el.__rest284 || to; el.classList.remove("rs284");
      void el.offsetWidth;
      if (turning) el.classList.add("an");
      el.style.transform = to;
      void el.offsetWidth;
    };
    const later = () => { clearTimeout(el.__t284); el.__t284 = setTimeout(rest, 640); };
    if (!el.__on284) {
      el.__on284 = 1;
      let p0 = null;
      box.addEventListener("pointerdown", (e) => { p0 = { x: e.clientX, y: e.clientY }; }, true);
      box.addEventListener("pointermove", (e) => { if (!p0) return; const dx = e.clientX - p0.x, dy = e.clientY - p0.y; if (Math.abs(dx) > 8 && Math.abs(dx) > Math.abs(dy)) { p0 = null; wake(false); } }, true);
      const up = () => { p0 = null; later(); };
      box.addEventListener("pointerup", up, true); box.addEventListener("pointercancel", up, true);
    }
    if (el.__k284 !== k) { const first = el.__k284 == null; el.__k284 = k; wake(!first); later(); }
  });'''

N_OLD = '''    try:  # change 278: the same alert also goes to the home-screen app
        import gm_push
        gm_push.send(title, msg, "#myteam")
    except Exception as ex:
        print(f"(notify) app alert not sent: {ex}")
'''
N_NEW = '''    app_ok = False
    try:  # change 278: the alert goes to the home-screen app
        import gm_push
        app_ok = gm_push.send(title, msg, "#myteam") > 0
    except Exception as ex:
        print(f"(notify) app alert not sent: {ex}")
    if not NTFY_ON:  # change 284
        return app_ok
'''
Q_OLD = '''def quiet(now):
'''
Q_NEW = '''NTFY_ON = False  # change 284: ntfy switched off (Kuvar, Nov 14, 2026); alerts go only to the app. True brings ntfy back.


def quiet(now):
'''
L_OLD = '''    if not NTFY_TOPIC:
        log("(no ntfy topic)", title, msg)
        return
'''
L_NEW = '''    if True:  # change 284: ntfy switched off (Kuvar, Nov 14, 2026); alerts go only to the app. Delete these two lines to bring ntfy back.
        return
    if not NTFY_TOPIC:
        log("(no ntfy topic)", title, msg)
        return
'''


def change(t):
    t = lit(t, "284: styles", "</style>", NEW_CSS, "change 284 (install.py)")
    t = lit(t, "284: flat side", FX_OLD, FX_NEW, "change 284: once the box has stopped turning")
    return t


def notify(t):
    t = lit(t, "284: notify, ntfy off", N_OLD, N_NEW, "if not NTFY_ON:")
    t = lit(t, "284: notify switch", Q_OLD, Q_NEW, "NTFY_ON = False")
    return t


edit(APP, change)
edit("gm_notify.py", notify)
edit("gm_live.py", lambda t: lit(t, "284: live, ntfy off", L_OLD, L_NEW, "change 284: ntfy switched off"))
