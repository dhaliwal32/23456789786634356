# changes/107-simulate-clean.py - new Simulate a pickup: the player, pick who to drop from your weakest players, best day to add him (points each day), two result numbers, details only when asked

NEW_CSS = r'''  /* change 107 (install.py) */
  .gx-so107 { position: fixed; inset: 0; z-index: 55; background: rgba(0,0,0,.6); overflow-y: auto; display: flex; justify-content: center; align-items: flex-start; animation: gx101-fade .2s ease-out; transition: opacity .18s; }
  .gx-so107.out { opacity: 0; }
  .gx-sim107 { width: 100%; max-width: 560px; margin: 40px 12px; background: var(--card); border: 1px solid var(--line2); border-radius: 16px; padding: 16px; animation: gx101-pop .26s cubic-bezier(.2,.8,.2,1); transition: transform .18s; }
  .gx-so107.out .gx-sim107 { transform: translateY(30px); }
  .gx-sim107 .hd { display: flex; align-items: center; gap: 8px; margin-bottom: 12px; }
  .gx-sim107 .hd .t { font-weight: 700; font-size: 17px; }
  .gx-sim107 .hd .m { font-size: 12px; color: var(--mute); }
  .gx-sim107 .hd .x { margin-left: auto; font-size: 24px; line-height: 1; color: var(--mute); padding: 2px 6px; }
  .gx-sim107 .pl { display: flex; align-items: center; gap: 12px; padding: 10px; border: 1px solid var(--line); border-radius: 12px; }
  .gx-sim107 .pl .nm { font-weight: 600; font-size: 16px; }
  .gx-sim107 .pl .sb { font-size: 13px; color: var(--mute); }
  .gx-sim107 .lk { font-size: 13px; color: var(--accent); }
  .gx-sim107 .sec { font-size: 12px; letter-spacing: .06em; text-transform: uppercase; color: var(--mute); margin: 16px 0 8px; }
  .gx-sim107 .chips { display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 8px; }
  .gx-sim107 .dc { display: flex; align-items: center; gap: 8px; padding: 8px; border: 1px solid var(--line2); border-radius: 10px; text-align: left; position: relative; }
  .gx-sim107 .dc.on { border-color: var(--accent); box-shadow: inset 0 0 0 1px var(--accent); background: var(--accentSoft); }
  .gx-sim107 .dc .n { display: block; font-size: 14px; font-weight: 500; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .gx-sim107 .dc .v { display: block; font-size: 12px; color: var(--mute); }
  .gx-sim107 .dc i { position: absolute; top: -8px; right: 8px; font-style: normal; font-size: 10px; font-weight: 700; letter-spacing: .04em; background: var(--good); color: #fff; padding: 1px 6px; border-radius: 99px; }
  .gx-sim107 .days { display: flex; gap: 6px; overflow-x: auto; scrollbar-width: none; padding-top: 10px; }
  .gx-sim107 .dy { flex: 1 0 64px; border: 1px solid var(--line2); border-radius: 10px; padding: 8px 4px; text-align: center; position: relative; }
  .gx-sim107 .dy span { display: block; font-size: 12px; color: var(--mute); }
  .gx-sim107 .dy b { display: block; font-size: 15px; font-variant-numeric: tabular-nums; }
  .gx-sim107 .dy.on { border-color: var(--accent); background: var(--accentSoft); }
  .gx-sim107 .dy.best::after { content: "BEST"; position: absolute; top: -8px; left: 50%; transform: translateX(-50%); font-size: 10px; font-weight: 700; background: var(--good); color: #fff; padding: 1px 6px; border-radius: 99px; }
  .gx-sim107 .res { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-top: 16px; }
  .gx-sim107 .res > div { border: 1px solid var(--line); border-radius: 12px; padding: 10px 12px; }
  .gx-sim107 .res small { display: block; font-size: 12px; color: var(--mute); }
  .gx-sim107 .res b { display: block; font-size: 22px; font-variant-numeric: tabular-nums; margin-top: 2px; }
  .gx-sim107 .act { display: flex; gap: 8px; margin-top: 14px; }
  .gx-sim107 .act button { flex: 1; padding: 10px; border-radius: 999px; font-weight: 600; font-size: 14px; border: 1px solid var(--line2); }
  .gx-sim107 .act button.pr { background: var(--ink); color: var(--bg); border-color: var(--ink); }
  .gx-sim107 .sr { width: 100%; }
  .gx-sim107 .opt { display: flex; align-items: center; gap: 10px; width: 100%; padding: 8px 4px; border-top: 1px solid var(--line); text-align: left; }
  .gx-sim107 .opt .v { margin-left: auto; font-size: 13px; color: var(--mute); }
  @media (max-width: 640px) {
    .gx-so107 { background: var(--bg); }
    .gx-sim107 { margin: 0; border: 0; border-radius: 0; min-height: 100%; padding: 16px 14px 40px; animation: gx101-up .3s cubic-bezier(.2,.8,.2,1); }
    .gx-sim107 .chips { grid-template-columns: 1fr 1fr; }
  }
</style>'''

HELPERS = r'''// ---------- change 107: Simulate a pickup, cleaned up (install.py) ----------
function GxSim107({ s, setS, wk, M, H, hLabel, init, wBase, onClose }) {
  const ea = gxPgAvg, K = M.K, myR = M.myR, today = todayISO();
  const byId = (id) => (id ? s.players.find((p) => p.id === id) || null : null);
  const [addId, setAddId] = useState(init.add || "");
  const [chg, setChg] = useState(!init.add);
  const [q, setQ] = useState("");
  const [dropId, setDropId] = useState(init.drop || "");
  const [day, setDay] = useState(null);
  const [allD, setAllD] = useState(false);
  const [det, setDet] = useState(false);
  const [out, setOut] = useState(false);
  const close = () => { if (out) return; setOut(true); setTimeout(onClose, 170); };
  useEffect(() => {
    const k = (e) => { if (e.key === "Escape") close(); };
    window.addEventListener("keydown", k); document.body.style.overflow = "hidden";
    return () => { window.removeEventListener("keydown", k); document.body.style.overflow = ""; };
  }, []);
  const a = byId(addId), d = byId(dropId);
  const left = movesLeft(s, s.me, wk);
  const dates = wk.dates || [], from = wk.done || 0;
  const a0 = a ? pickStart(a) : today;
  const cands = useMemo(() => myR.filter((p) => !p.ir).sort((x, y) => ea(x, K) - ea(y, K)), [myR, K]);
  const weak = cands.filter((p) => !M.protectedIds.has(p.id)).slice(0, 6);
  const sug = useMemo(() => {
    if (!a) return "";
    const c = cntOf(myR), ok = (x) => x.p === a.p || c[x.p] - 1 >= M.mins[x.p], b = M.total(myR);
    let best = null;
    (weak.length ? weak : cands).filter(ok).forEach((x) => { const g = M.total(timedMove(myR, s.me, [{ add: a, drop: x }])) - b; if (!best || g > best.g) best = { x, g }; });
    return best ? best.x.id : "";
  }, [addId]);
  useEffect(() => { if (sug && (!dropId || !init.drop)) setDropId(sug); }, [sug]);
  const rosterOn = (dt) => myR.map((p) => (d && p.id === d.id ? { ...p, untilD: dt } : p)).concat(a ? [{ ...a, ft: s.me, fromD: dt }] : []);
  const dayG = useMemo(() => {
    if (!a || !d) return [];
    const b = weekProj(myR, wk, K, from).total;
    return dates.map((dt, i) => ({ dt, i })).filter((x) => x.i >= from && x.dt >= a0).map((x) => ({ ...x, g: weekProj(rosterOn(x.dt), wk, K, from).total - b }));
  }, [addId, dropId, wk]);
  const best = dayG.reduce((b, x) => (!b || x.g > b.g + 0.05 ? x : b), null);
  const pick = day != null && dayG.some((x) => x.dt === day) ? day : best ? best.dt : null;
  const R = useMemo(() => {
    if (!a || !d || !pick) return null;
    const r = rosterOn(pick);
    const dg = dayG.find((x) => x.dt === pick);
    return { gain: H === 1 && dg ? dg.g : M.total(r) - M.total(myR), win: winChance(s, r) };
  }, [addId, dropId, pick]);
  const qq = nrm(q);
  const opts = !chg ? [] : qq ? M.fas.filter((p) => p.prob > 0 && nrm(p.n).includes(qq)).sort((x, y) => ea(y, K) - ea(x, K)).slice(0, 8) : M.res.slice(0, 8).map((r) => r.f);
  const apply = () => {
    if (!a || !d) return;
    setS((st) => ({ ...st, players: st.players.map((p) => (p.id === d.id ? { ...p, ft: "fa", ir: false } : p.id === a.id ? { ...p, ft: st.me } : p)) }));
    close();
  };
  const DN = (dt) => (dt === today ? "Today" : dayLabel(dt).split(",")[0]);
  const sg = (v) => (v >= 0 ? "+" : "") + f1(v);
  return (
    <div className={"gx-so107" + (out ? " out" : "")} onClick={close}>
      <div className="gx-sim107" onClick={(e) => e.stopPropagation()}>
        <div className="hd">
          <span className="t">Simulate a pickup</span>
          {left != null ? <span className="m">{left + " move" + (left === 1 ? "" : "s") + " left"}</span> : null}
          <button type="button" className="x" aria-label="Close" onClick={close}>{"×"}</button>
        </div>
        {a && !chg ? (
          <div className="pl">
            <GxFace p={a} size={44} />
            <div className="min-w-0" style={{ flex: 1 }}>
              <div className="nm truncate">{a.n}</div>
              <div className="sb">{a.p + " · " + a.t + " · " + f1(ea(a, K)) + "/g · " + M.gamesIn(a) + " games"}</div>
            </div>
            <button type="button" className="lk" onClick={() => { setChg(true); setQ(""); }}>Change</button>
          </div>
        ) : (
          <div>
            <input className={inp + " sr"} autoFocus placeholder="Search a free agent" value={q} onChange={(e) => setQ(e.target.value)} />
            {opts.map((p) => (
              <button key={p.id} type="button" className="opt" onClick={() => { setAddId(p.id); setDropId(""); setDay(null); setChg(false); }}>
                <GxFace p={p} size={26} /><span className="truncate">{p.n} <span className="text-xs text-slate-500">{p.p}</span></span><span className="v">{f1(ea(p, K))}</span>
              </button>
            ))}
          </div>
        )}
        {a && !chg ? (
          <>
            <div className="sec">Drop</div>
            <div className="chips">
              {(allD ? cands : weak).map((p) => (
                <button key={p.id} type="button" className={"dc" + (p.id === dropId ? " on" : "")} onClick={() => { setDropId(p.id); setDay(null); }}>
                  <GxFace p={p} size={28} />
                  <span className="min-w-0"><span className="n">{shortN(p.n)}</span><span className="v">{p.p + " · " + f1(ea(p, K))}</span></span>
                  {p.id === sug ? <i>BEST</i> : null}
                </button>
              ))}
            </div>
            <button type="button" className="lk" style={{ marginTop: 8 }} onClick={() => setAllD(!allD)}>{allD ? "Weakest only" : "Whole roster"}</button>
            {dayG.length ? (
              <>
                <div className="sec">Best day to add</div>
                <div className="days">
                  {dayG.map((x) => (
                    <button key={x.dt} type="button" className={"dy" + (x.dt === pick ? " on" : "") + (best && x.dt === best.dt && dayG.length > 1 ? " best" : "")} onClick={() => setDay(x.dt)}>
                      <span>{DN(x.dt)}</span><b style={{ color: x.g >= 0 ? "var(--good)" : "var(--bad)" }}>{sg(x.g)}</b>
                    </button>
                  ))}
                </div>
              </>
            ) : null}
            {R ? (
              <>
                <div className="res">
                  <div><small>{"Points, " + hLabel}</small><b style={{ color: R.gain >= 0 ? "var(--good)" : "var(--bad)" }}>{sg(R.gain)}</b></div>
                  <div><small>{"Win " + (String(hLabel).indexOf("next week") === 0 ? "next week" : "this week")}</small><b>{(wBase != null ? wpTxt(wBase) + " → " : "") + (R.win == null ? "-" : wpTxt(R.win))}</b></div>
                </div>
                <button type="button" className="lk" style={{ marginTop: 10 }} onClick={() => setDet(!det)}>{det ? "Hide details" : "More details"}</button>
                {det ? <GxPickRes92 s={s} myR={myR} ok={[{ a, d }]} /> : null}
                <div className="act">
                  <button type="button" className="pr" onClick={() => { if (window.__QA) window.__QA.espn(a); }}>Add on ESPN</button>
                  <button type="button" onClick={apply}>Try it here</button>
                </div>
              </>
            ) : null}
          </>
        ) : null}
      </div>
    </div>
  );
}
'''


def change(t):
    t = lit(t, "107: styles", "</style>", NEW_CSS, "change 107 (install.py)")
    t = lit(t, "107: helpers", ROOT, HELPERS + ROOT, "change 107: Simulate a pickup, cleaned up")
    t = sub_once(t, "107: use the new simulate box", re.escape("<MoveSim "), "<GxSim107 ", "<GxSim107 s={", 0, 3)
    return t


edit(APP, change)
