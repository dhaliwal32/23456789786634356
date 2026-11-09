# changes/228-roster-jumbotron.py - Roster box: Kuvar's 3D scoreboard model, its four screens show Today, Win, Games and Players

NEW_CSS = r'''  /* change 228 (install.py): 3D scoreboard in the Roster box */
  .gx-bx226 .jb228 { position: relative; aspect-ratio: 1 / 1; max-height: 540px; }
  .gx-bx226 .jb228 .gl228 { position: absolute; inset: 0; }
  .gx-bx226 .jb228 .gl228 canvas { border-radius: 14px; }
  .gx-bx226 .jb228.on .stg { visibility: hidden; }
  .gx-bx226 .jb228 .stg { position: absolute; inset: 0; }
  .gx-bx225.gx-bx226.full .jb228 { max-height: 62vh; margin: 0 auto; }
</style>'''

HELPERS = r'''// ---------- change 228: 3D scoreboard in the Roster box (install.py) ----------
// loads the 3D library and the scoreboard only when the box is shown; the flat box stays as the fallback
const GX228 = (window.__GX228 = window.__GX228 || { p: null });
function gxLoad228() {
  if (window.gxJumbo) return Promise.resolve(true);
  if (GX228.p) return GX228.p;
  const add = (src) => new Promise((ok, no) => { const sc = document.createElement("script"); sc.src = src; sc.onload = ok; sc.onerror = no; document.head.appendChild(sc); });
  GX228.p = (window.GX3D ? Promise.resolve() : add("vendor/gx3d.js?v=228")).then(() => add("vendor/gx3d-jumbo.js?v=228")).then(() => !!window.gxJumbo);
  GX228.p.catch(() => { GX228.p = null; });
  return GX228.p;
}
function GxJumbo228({ J, k, setK, onTap, fb }) {
  const box = React.useRef(null), ctl = React.useRef(null), tapR = React.useRef(onTap);
  const [on, setOn] = useState(false);
  tapR.current = onTap;
  useEffect(() => {
    let dead = false;
    const ok = (() => { try { const c = document.createElement("canvas"); return !!(c.getContext("webgl2") || c.getContext("webgl")); } catch (e) { return false; } })();
    if (!ok) return undefined;
    gxLoad228().then((y) => {
      if (dead || !y || !box.current) return;
      ctl.current = window.gxJumbo.mount(box.current, { base: "models3d/", onFace: (f) => setK(f), onTap: (id) => tapR.current && tapR.current(id), onReady: () => { if (!dead) setOn(true); }, onError: () => { if (!dead) setOn(false); } });
      if (J) ctl.current.set(J);
      ctl.current.turn(k);
    }).catch(() => {});
    return () => { dead = true; if (ctl.current) { ctl.current.destroy(); ctl.current = null; } };
  }, []);
  const key = JSON.stringify(J);
  useEffect(() => { if (ctl.current && J) ctl.current.set(J); }, [key]);
  useEffect(() => { if (ctl.current) ctl.current.turn(k); }, [k]);
  return (
    <div className={"jb228" + (on ? " on" : "")}>
      {fb}
      <div ref={box} className="gl228" style={on ? null : { visibility: "hidden" }}></div>
    </div>
  );
}
'''

DATA = r'''  // change 228: what the four screens of the 3D scoreboard show
  const J228 = {
    nmA, nmB,
    today: ti < 0 ? { none: "Today is not part of this week.", right: "" } : {
      right: tA.filter((x) => x.g.s === "L").length + tB.filter((x) => x.g.s === "L").length + " playing now",
      a: tA.map(({ q, v, real, g }) => ({ n: lastN(q.n), st: g.s === "L" ? "LIVE" : g.s === "F" ? "FINAL" : gameTime(gameOf(q.t, today)), live: g.s === "L", v, real, id: q.id })),
      b: tB.map(({ q, v, real, g }) => ({ n: lastN(q.n), st: g.s === "L" ? "LIVE" : g.s === "F" ? "FINAL" : gameTime(gameOf(q.t, today)), live: g.s === "L", v, real, id: q.id })),
      ta: tSum(tA), tb: tSum(tB), pa: tProj(tA), pb: tProj(tB),
    },
    win: {
      right: over ? "Final" : "Now",
      line: over ? (sa >= sb ? "Won by " + f1(sa - sb) : "Lost by " + f1(sb - sa)) : (fa >= fb ? "On pace to win by " : "On pace to lose by ") + f1(Math.abs(fa - fb)),
      sub: over ? "" : "They should finish near " + f1(fb) + ". You need " + f1(Math.max(0, need)) + " more" + (leftA ? ", " + f1(perG) + " a game left." : "."),
      hist: wHist.map((v, j) => ({ v, d: DN(fdays[j]) })),
      cells: [["If you add 10", over ? "\u2013" : wpTxt(swing(10))], ["If they add 10", over ? "\u2013" : wpTxt(swing(-10))], ["Need a game", over || !leftA ? "\u2013" : f1(perG)], ["Your pace", f1(fa)], ["Their pace", f1(fb)], ["Spread", "\u00b1" + f1(sdNow)]],
    },
    games: {
      right: up ? "Projected" : "Left " + leftA + " v " + leftB, leftLab: up ? "All" : "Left",
      days: dates.map((_, d) => DN(d)), ti, a: dates.map((_, d) => gms(X, d)), b: dates.map((_, d) => gms(Y, d)), fut: dates.map((_, d) => st(d) === "p"),
      la: up ? totG(X) : leftA, lb: up ? totG(Y) : leftB,
      cells: [["All week", totG(X) + " v " + totG(Y)], ["Played", gpA + " v " + gpB], ["Today", gToday(X) + " v " + gToday(Y)], ["Bench with a game", (X.wasted || 0) + " v " + (Y.wasted || 0)], ["Empty spots", (X.empty || 0) + " v " + (Y.empty || 0)], ["Vs projection", done ? sg(vsA) + " v " + sg(vsB) : "\u2013"]],
    },
    players: {
      a: top(SA, 5).map((o) => ({ n: lastN(o.p.n), sub: o.p.t + " \u00b7 " + o.gp + " GP", v: o.pts, id: o.p.id })),
      b: top(SB, 5).map((o) => ({ n: lastN(o.p.n), sub: o.p.t + " \u00b7 " + o.gp + " GP", v: o.pts, id: o.p.id })),
      la: lefts(SA).map((o) => ({ n: lastN(o.p.n) + " \u00b7 " + o.left + (o.live ? " live" : " left"), v: "+" + f1(o.rem), id: o.p.id })),
      lb: lefts(SB).map((o) => ({ n: lastN(o.p.n) + " \u00b7 " + o.left + (o.live ? " live" : " left"), v: "+" + f1(o.rem), id: o.p.id })),
    },
  };
'''

RET_OLD = '''  return (
    <div className={cls}>
      {head}
      <div className="lay">'''

STG_OLD = '''          <div ref={stg} className="stg" onPointerDown={pDown} onPointerMove={pMove} onPointerUp={pUp} onPointerCancel={pUp}>
            <div ref={pr} className="pr">{fToday}{fWin}{fGames}{fPlayers}</div>
          </div>'''
STG_NEW = '''          <GxJumbo228 J={J228} k={k} setK={setK} onTap={(id) => openP(s.players.find((p) => p.id === id))} fb={(
            <div ref={stg} className="stg" onPointerDown={pDown} onPointerMove={pMove} onPointerUp={pUp} onPointerCancel={pUp}>
              <div ref={pr} className="pr">{fToday}{fWin}{fGames}{fPlayers}</div>
            </div>
          )} />'''

def change(t):
    t = lit(t, "228: styles", "</style>", NEW_CSS, "change 228 (install.py): 3D scoreboard")
    t = lit(t, "228: helpers", ROOT, HELPERS + ROOT, "change 228: 3D scoreboard in the Roster box")
    t = lit(t, "228: screen data", RET_OLD, DATA + RET_OLD, "change 228: what the four screens")
    t = lit(t, "228: scoreboard in the box", STG_OLD, STG_NEW, "<GxJumbo228 J={J228}")
    return t

edit(APP, change)
