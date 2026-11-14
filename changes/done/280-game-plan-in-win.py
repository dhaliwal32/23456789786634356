# changes/280-game-plan-in-win.py - Roster box: Game plan moves inside the Win side (who starts over who and goalies, under the win numbers); the card on the left is gone and its sentence is not repeated

NEW_CSS = r'''  /* change 280 (install.py) */
  .gx-bx226 .gp276.in280 { margin-top: 14px; padding-top: 12px; border-top: 1px solid var(--line); }
  .gx-bx226 .gp276.in280 .dd276 { border-top: 0; padding-top: 0; margin-top: 6px; }
</style>'''

LEFT_OLD = r'''<div className="min-w-0">{board}{me !== s.me || !cur || over ? null : <GxPlan276 s={s} w={w} sa={sa} sb={sb} fa={fa} fb={fb} leftA={leftA} leftB={leftB} up={up} openP={openP} />}{me !== s.me || !cur ? null : <GxBp257 s={s} openP={openP} />}</div>'''
LEFT_NEW = r'''<div className="min-w-0">{board}{me !== s.me || !cur ? null : <GxBp257 s={s} openP={openP} />}</div>'''

WIN_OLD = r'''        <div>Goalie starts left<b>{two(gxGl252(X, "G", dates, st), gxGl252(Y, "G", dates, st))}</b></div>
        <div>Bench with a game<b>{two(X.wasted || 0, Y.wasted || 0)}</b></div>
      </div>
'''
WIN_NEW = WIN_OLD + r'''      {me !== s.me || !cur || over ? null : <GxPlan276 inWin s={s} w={w} sa={sa} sb={sb} fa={fa} fb={fb} leftA={leftA} leftB={leftB} up={up} openP={openP} />}{/* change 280 */}
'''

SIG_OLD = r'''function GxPlan276({ s, w, sa, sb, fa, fb, leftA, leftB, up, openP }) {'''
SIG_NEW = r'''function GxPlan276({ s, w, sa, sb, fa, fb, leftA, leftB, up, openP, inWin }) {'''
BOX_OLD = r'''    <div className="bp230 gp276" data-gx="276">
      <div className="ft"><span className="gx-tag">Game plan</span></div>
      <div className="say">{say} <span>{say2}</span></div>'''
BOX_NEW = r'''    <div className={inWin ? "gp276 in280" : "bp230 gp276"} data-gx="276">
      <div className="ft"><span className="gx-tag">Game plan</span></div>
      {inWin ? null : <div className="say">{say} <span>{say2}</span></div>}'''


def change(t):
    t = lit(t, "280: styles", "</style>", NEW_CSS, "change 280 (install.py)")
    t = lit(t, "280: off the left side", LEFT_OLD, LEFT_NEW)
    t = lit(t, "280: plan takes inWin", SIG_OLD, SIG_NEW, "openP, inWin })")
    t = lit(t, "280: plan without its card", BOX_OLD, BOX_NEW, '"gp276 in280"')
    t = lit(t, "280: into the Win side", WIN_OLD, WIN_NEW, "<GxPlan276 inWin")
    return t

edit(APP, change)
