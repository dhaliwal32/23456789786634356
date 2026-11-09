# changes/229-flat-box-lines-profile.py - Roster box back to the flat box (no 3D scoreboard); Lines: tapping a player opens his profile

JB_OLD = '''          <GxJumbo228 J={J228} k={k} setK={setK} onTap={(id) => openP(s.players.find((p) => p.id === id))} fb={(
            <div ref={stg} className="stg" onPointerDown={pDown} onPointerMove={pMove} onPointerUp={pUp} onPointerCancel={pUp}>
              <div ref={pr} className="pr">{fToday}{fWin}{fGames}{fPlayers}</div>
            </div>
          )} />'''
JB_NEW = '''          {/* change 229: flat box again */}<div ref={stg} className="stg" data-gx="229" onPointerDown={pDown} onPointerMove={pMove} onPointerUp={pUp} onPointerCancel={pUp}>
            <div ref={pr} className="pr">{fToday}{fWin}{fGames}{fPlayers}</div>
          </div>'''

TAP_OLD = '''onClick={(e) => { const md = e.currentTarget.querySelector(".md"); setZoom224({ n, from: md ? md.getBoundingClientRect() : null }); }}'''
TAP_NEW = '''onClick={() => { if (p && window.__NAV) window.__NAV.player(p); }} data-gx="229t"'''

def change(t):
    t = lit(t, "229: flat box", JB_OLD, JB_NEW, 'data-gx="229"')
    t = lit(t, "229: Lines tap opens the profile", TAP_OLD, TAP_NEW, 'data-gx="229t"')
    return t

edit(APP, change)
