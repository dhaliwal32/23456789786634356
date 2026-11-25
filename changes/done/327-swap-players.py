# changes/327-swap-players.py - swap players yourself (Kuvar, Nov 25: "when autopilot is on i want to swap players on the app, saved, and autopilot to change it and remember the change"): Roster page > Swap players, tap a bench player then the starter he replaces; the swap is saved in lineup_holds.json, autopilot sets it on ESPN at the next sync and keeps it for that day only; autopilot notes say "tomorrow" instead of "today" late at night

# ---------- the app ----------
NEW_CSS = r'''  /* change 327 (install.py) */
  .gx-sw327 { margin-bottom: 12px; }
  .gx-sw327 > .ls em { font-style: normal; color: var(--mute); }
  .gx-sw327s .rw { grid-template-columns: auto minmax(0,1fr) 44px; padding: 0 8px; margin: 0 -8px; width: calc(100% + 16px); border-radius: 10px; transition: background .18s ease, opacity .18s ease; }
  .gx-sw327s .rw.on { background: var(--line2); }
  .gx-sw327s .rw.no { opacity: .35; }
  .gx-sw327s .hl { border: 1px solid var(--line2); border-radius: 12px; padding: 2px 12px; margin-bottom: 10px; }
  .gx-sw327s .hl .hr { display: flex; align-items: center; gap: 10px; height: 44px; font-size: 13.5px; }
  .gx-sw327s .hl .hr + .hr { border-top: 1px solid var(--line); }
  .gx-sw327s .hl .hr > span { flex: 1; min-width: 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .gx-sw327s .hl .hr button { font-size: 13px; color: var(--mute); padding: 6px 2px 6px 10px; flex-shrink: 0; }
  .gx-sw327s .cf { position: sticky; bottom: -16px; margin: 8px -16px -16px; padding: 12px 16px 16px; background: var(--card); border-top: 1px solid var(--line2); display: flex; align-items: center; gap: 12px; animation: gx101-pop .26s cubic-bezier(.2,.8,.2,1); }
  .gx-sw327s .cf > span { flex: 1; min-width: 0; font-size: 14px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .gx-sw327s .cf button { flex-shrink: 0; height: 40px; padding: 0 16px; border-radius: 10px; background: var(--ink); color: var(--card); font-size: 14px; font-weight: 600; }
  .gx-sw327s .cf button:disabled { opacity: .5; }
  .gx-sw327s .ms { font-size: 13px; color: var(--good); padding: 0 0 10px; animation: gx288-in .26s cubic-bezier(.2,.8,.2,1); }
</style>'''

HELPERS = r'''// ---------- change 327: swap players yourself; autopilot sets it on ESPN and keeps it that day (install.py) ----------
const GX_HOLD_API327 = "https://api.github.com/repos/dhaliwal32/23456789786634356/contents/lineup_holds.json";
const GX_HOLD_LS327 = "gx-holds327";
const GX_SLOT327 = { 3: "F", 4: "D", 5: "G", 6: "UTIL" };
let __gxH327 = null;
function gxHoldsGet327() {
  if (!__gxH327) __gxH327 = fetch("lineup_holds.json?t=" + Date.now(), { cache: "no-store" }).then((r) => (r.ok ? r.json() : null)).then((j) => (j && Array.isArray(j.holds) ? j.holds : [])).catch(() => []);
  return __gxH327.then((list) => {
    let L = null;
    try { L = JSON.parse(localStorage.getItem(GX_HOLD_LS327) || "null"); } catch (e) {}
    return L && Date.now() - (L.t || 0) < 15 * 60 * 1000 ? L.holds || [] : list; // just saved: the site can take a few minutes to show the new file
  });
}
// read lineup_holds.json on GitHub, change the list with fn, save it (same key as Sync between devices)
function gxHoldsSave327(fn) {
  const key = gxSyncKey();
  if (!key) return Promise.reject(new Error("nokey"));
  const hdr = { Authorization: "Bearer " + key, Accept: "application/vnd.github+json" };
  const once = (again) => fetch(GX_HOLD_API327 + "?ref=main&t=" + Date.now(), { headers: hdr, cache: "no-store" })
    .then((r) => { if (r.status === 404) return null; if (r.status === 401 || r.status === 403) throw new Error("key"); if (!r.ok) throw new Error("read " + r.status); return r.json(); })
    .then((j) => {
      let cur = [];
      try { cur = (JSON.parse(gxUnB64(j.content)).holds) || []; } catch (e) {}
      const next = fn(cur);
      const body = { message: "Lineup swap from the app", content: gxB64(JSON.stringify({ holds: next }, null, 1) + "\n"), branch: "main" };
      if (j && j.sha) body.sha = j.sha;
      return fetch(GX_HOLD_API327, { method: "PUT", headers: { ...hdr, "Content-Type": "application/json" }, body: JSON.stringify(body) })
        .then((r) => { if ((r.status === 409 || r.status === 422) && again) return once(false); if (!r.ok) throw new Error(r.status === 401 || r.status === 403 ? "key" : "save " + r.status); return next; });
    });
  return once(true).then((next) => { try { localStorage.setItem(GX_HOLD_LS327, JSON.stringify({ t: Date.now(), holds: next })); } catch (e) {} __gxH327 = null; return next; });
}
// the lineup day: today while one of your games has not started, otherwise the next day you have a game
function gxSwapDay327(s, today) {
  const mine = s.players.filter((p) => p.ft === s.me && !p.ir);
  for (let i = 0; i < 8; i++) {
    const dt = addDays(today, i);
    if (mine.some((p) => SCHED[p.t] && SCHED[p.t].has(dt) && (i > 0 || gState(p.t, dt).s === "P"))) return dt;
  }
  return null;
}
// your players with their ESPN spot (newest ESPN lineup up to that day), with saved swaps for that day applied
function gxSwapRows327(s, dt, today, holds) {
  const tid = String(s.me).replace(/^t/, ""), D = (window.ESPN_DATA || {}).daily || {};
  const ks = Object.keys(D).filter((d) => d <= dt && D[d] && D[d][tid]).sort();
  const AD = ks.length ? D[ks[ks.length - 1]][tid] : {};
  const rows = s.players.filter((p) => p.ft === s.me && !p.ir).map((p) => {
    const pid = String(p.id).replace(/^e/, ""), v = AD[pid], slot = v ? v[1] : 7;
    const plays = !!(SCHED[p.t] && SCHED[p.t].has(dt));
    return { p, pid, slot, on: !!GX_SLOT327[slot], plays, gm: plays ? gameOf(p.t, dt) : null,
      lock: plays && dt === today && gState(p.t, dt).s !== "P",
      x: plays ? effAvg(p, s.blend) * (p.p === "G" ? (p.prob != null ? p.prob : 1) : 1) : 0 };
  }).filter((r) => r.slot !== 8);
  const by = Object.fromEntries(rows.map((r) => [r.pid, r]));
  const mine = (holds || []).filter((h) => h.day === dt && by[String(h.in)] && by[String(h.out)]);
  mine.forEach((h) => {
    const a = by[String(h.in)], b = by[String(h.out)];
    if (!a.on && b.on) { a.on = true; a.slot = b.slot; b.on = false; b.slot = 7; }
    a.held = b.held = true;
  });
  return { rows, holds: mine, by };
}
// can bench player b take starter a's spot? goalie for goalie, F for F, D for D, F or D into UTIL
const gxCan327 = (b, a) => (a.slot === 5 ? b.p.p === "G" : b.p.p !== "G" && (a.slot === 6 || b.p.p === a.p.p));
const GX_PO327 = { F: 0, D: 1, G: 2 };
function GxSwap327({ P }) {
  const { s } = P, today = todayISO(), gen = (window.ESPN_DATA || {}).generated;
  const ap = gxUseAp();
  const [holds, setHolds] = useState(null);
  const [open, setOpen] = useState(false);
  const [out, setOut] = useState(false);
  const [pick, setPick] = useState(null);
  const [busy, setBusy] = useState(false);
  const [msg, setMsg] = useState("");
  useEffect(() => { let dead = false; gxHoldsGet327().then((h) => { if (!dead) setHolds(h); }); return () => { dead = true; }; }, [gen]);
  const close = () => { if (out) return; setOut(true); setTimeout(() => { setOut(false); setOpen(false); setPick(null); setMsg(""); }, 180); };
  useEffect(() => { if (!open) return undefined; const k = (e) => { if (e.key === "Escape") close(); }; window.addEventListener("keydown", k); return () => window.removeEventListener("keydown", k); }, [open, out]);
  const dt = useMemo(() => { try { return gxSwapDay327(s, today); } catch (e) { return null; } }, [s.players, today, gen]);
  const D = useMemo(() => { try { return dt ? gxSwapRows327(s, dt, today, holds) : null; } catch (e) { return null; } }, [s.players, s.blend, dt, today, holds, gen]);
  if (gxApMode(ap) !== "on" || !window.ESPN_DATA || s.me !== gxReal241() || !dt || !D) return null;
  const dn = dt === today ? "Today" : dt === addDays(today, 1) ? "Tomorrow" : dayLabel(dt).split(",")[0];
  const ord = (a, b) => (GX_PO327[a.p.p] - GX_PO327[b.p.p]) || (b.x - a.x);
  const st = D.rows.filter((r) => r.on).sort(ord), bn = D.rows.filter((r) => !r.on).sort(ord);
  const [sel1, sel2] = String(pick || "").split(">");
  const A = sel1 ? D.by[sel1] : null, B = sel2 ? D.by[sel2] : null;
  const swap = A && B ? (A.on ? { in: B, out: A } : { in: A, out: B }) : null;
  const fits = (r) => {
    if (r.lock) return false;
    if (!A || B || A === r || A.on === r.on) return true;
    return A.on ? gxCan327(r, A) : gxCan327(A, r);
  };
  const tap = (r) => {
    if (busy || !fits(r)) return;
    setMsg("");
    if (!A || B) { setPick(r.pid); return; }
    if (A === r) { setPick(null); return; }
    if (A.on === r.on) { setPick(r.pid); return; }
    setPick(A.pid + ">" + r.pid);
  };
  const fail = (e) => setMsg(e && (e.message === "nokey" || e.message === "key")
    ? "Could not save. First turn on Sync between devices on this device (Setup, More, Data and backup)."
    : "Could not save. Check your connection and try again.");
  const save = () => {
    if (!swap || busy) return;
    setBusy(true);
    const h = { day: dt, in: swap.in.pid, out: swap.out.pid, at: new Date().toISOString() };
    gxHoldsSave327((cur) => [...cur.filter((x) => x.day >= today && !(x.day === dt && [String(x.in), String(x.out)].some((y) => y === h.in || y === h.out))), h])
      .then((next) => { setHolds(next); setPick(null); setMsg("Saved. Autopilot sets it on ESPN within about 6 minutes and keeps it for " + dn.toLowerCase() + "."); })
      .catch(fail).then(() => setBusy(false));
  };
  const undo = (h) => {
    if (busy) return;
    setBusy(true);
    gxHoldsSave327((cur) => cur.filter((x) => x.day >= today && !(x.day === h.day && String(x.in) === String(h.in) && String(x.out) === String(h.out))))
      .then((next) => { setHolds(next); setPick(null); setMsg("Swap removed. Autopilot picks that spot by itself again."); })
      .catch(fail).then(() => setBusy(false));
  };
  const rw = (r) => {
    const on = A === r || B === r, ok = fits(r);
    const sub = [r.on ? GX_SLOT327[r.slot] : r.p.p, r.gm ? (r.gm.h ? "vs " : "@ ") + r.gm.o : "no game", r.lock ? "game started" : r.held ? "your swap" : ""].filter(Boolean).join(" \u00b7 ");
    return (
      <button key={r.pid} type="button" className={"rw" + (on ? " on" : "") + (ok ? "" : " no")} disabled={!ok} onClick={() => tap(r)}>
        <GxFace p={r.p} size={26} />
        <span className="nn"><b>{r.p.n}</b><small>{sub}</small></span>
        <span className="xp">{r.plays ? f1(r.x) : "\u2013"}</span>
      </button>
    );
  };
  const nm = (pid) => lastN((D.by[String(pid)] || { p: { n: "" } }).p.n);
  return (
    <>
      <button type="button" className="gx-gp291 gx-sw327" data-gx="327" onClick={() => setOpen(true)}>
        <b>Swap players</b>
        <span className="ls">{D.holds.length ? D.holds.map((h) => <span key={h.in + ">" + h.out}>{"Start " + nm(h.in) + ", sit " + nm(h.out)}</span>) : <em>{dn + " \u00b7 choose who starts"}</em>}</span>
        <span className="sec-chev shut" style={{ margin: "0 2px 0 0" }}></span>
      </button>
      {open ? ReactDOM.createPortal(
        <div className={"gx-sx289 fixed inset-0" + (out ? " out" : "")} onClick={close}>
          <div className="pn gx-sw327s" onClick={(e) => e.stopPropagation()}>
            <div className="tt"><b>{"Swap players \u00b7 " + dn}</b><button type="button" aria-label="Close" onClick={close}>{"\u00d7"}</button></div>
            <div className="nt">Tap a bench player, then the starter he replaces. Autopilot sets it on ESPN and keeps your swap for the day. The number is his projected points.</div>
            {msg ? <div className="ms">{msg}</div> : null}
            {D.holds.length ? (
              <div className="hl">
                {D.holds.map((h) => (
                  <div key={h.in + ">" + h.out} className="hr">
                    <span>{"Your swap: start "}<b>{nm(h.in)}</b>{", sit "}<b>{nm(h.out)}</b></span>
                    <button type="button" disabled={busy} onClick={() => undo(h)}>Undo</button>
                  </div>
                ))}
              </div>
            ) : null}
            <div className="gx-go289"><div className="bd">
              <div className="sc">Starting</div>{st.length ? st.map(rw) : <div className="em">Nobody is starting yet.</div>}
              <div className="sc">Bench</div>{bn.length ? bn.map(rw) : <div className="em">Nobody on the bench.</div>}
            </div></div>
            {swap ? (
              <div className="cf">
                <span>{"Start "}<b>{lastN(swap.in.p.n)}</b>{", sit "}<b>{lastN(swap.out.p.n)}</b></span>
                <button type="button" disabled={busy} onClick={save}>{busy ? "Saving..." : "Save swap"}</button>
              </div>
            ) : null}
          </div>
        </div>, document.body) : null}
    </>
  );
}
'''

SHOW_OLD = '''      <MyTeam {...P} />{/* change 285: table only */}'''
SHOW_NEW = '''      <GxSwap327 P={P} />{/* change 327 */}
      <MyTeam {...P} />{/* change 285: table only */}'''


def app(t):
    t = lit(t, "327: styles", "</style>", NEW_CSS, "change 327 (install.py)")
    t = lit(t, "327: helpers", ROOT, HELPERS + ROOT, "change 327: swap players yourself")
    t = lit(t, "327: Swap players on the Roster page", SHOW_OLD, SHOW_NEW, "<GxSwap327 P={P} />")
    return t


# ---------- gm_autopilot.py ----------
PL_OLD = '''    left = [r for r in free if r["id"] not in want]
'''
PL_NEW = '''    left = [r for r in free if r["id"] not in want]

    # change 327: swaps Kuvar made in the app for this day: the player he put in starts, the one he sat stays on the bench
    forced327 = set()
    home327 = {"F": SLOT_F, "D": SLOT_D, "G": SLOT_G}
    for pin, pout in c.get("holds327") or []:
        a = next((r for r in left if str(r["id"]) == pin and r["id"] not in want), None)
        o = next((r for r in roster if str(r["id"]) == pout), None)
        if not a or not o or a["p"] not in home327 or (o["locked"] and o["slot"] in ACTIVE):
            continue  # one of the two is locked (game started) or not on the team any more
        if o in left and o["id"] not in want:
            want[o["id"]] = SLOT_BENCH
            forced327.add(o["id"])
        if a["slot"] in ACTIVE:
            slot = a["slot"]
        elif o["slot"] in (home327[a["p"]], SLOT_U) and (a["p"] != "G") == (o["slot"] != SLOT_G) and (o["slot"] != SLOT_U or not a["elig"] or SLOT_U in a["elig"]):
            slot = o["slot"]
        else:
            slot = home327[a["p"]]
        if cap[slot] <= 0 and a["p"] != "G" and (not a["elig"] or SLOT_U in a["elig"]) and cap[SLOT_U] > 0:
            slot = SLOT_U
        if cap[slot] <= 0:
            continue
        want[a["id"]] = slot
        cap[slot] -= 1
        forced327.add(a["id"])
'''
FILL_OLD = '''        room = cap[slot] - sum(1 for r in left if want.get(r["id"]) == slot)
'''
FILL_NEW = '''        room = cap[slot] - sum(1 for r in left if want.get(r["id"]) == slot and r["id"] not in forced327)  # change 327: swaps already took their spot from cap
'''
FOUND_OLD = '''    found = []
'''
FOUND_NEW = '''    found = []
    holds327 = _holds327(today)  # change 327: swaps saved in the app, by day
    n_ahead = max(n_ahead, min(14, max(((datetime.fromisoformat(d).date() - today).days for d in holds327), default=0)))
'''
SKIP_OLD = '''            if last and not (redo and redo > last):
'''
SKIP_NEW = '''            if last and not (redo and redo > last) and day not in holds327:  # change 327: a day with a swap is always checked
'''
PLAN_OLD = '''        moves, before, after = plan(roster, day, games, E, c)
'''
PLAN_NEW = '''        moves, before, after = plan(roster, day, games, E, {**c, "holds327": holds327.get(day, [])})  # change 327
        held327 = {x for pr in holds327.get(day, []) for x in pr}
'''
GAIN_OLD = '''        if not moves or (gain < min_gain and fills <= 0):
'''
GAIN_NEW = '''        swap327 = any(str(m["r"]["id"]) in held327 for m in moves)  # change 327: a swap from the app is made even if it adds no points
        if not moves or (gain < min_gain and fills <= 0 and not swap327):
'''
TEXT_OLD = '''"gain": gain, "text": describe(moves)})'''
TEXT_NEW = '''"gain": gain, "text": ("Your swap: " if swap327 else "") + describe(moves)})'''
DNAME_OLD = '''    dname = lambda d: "today" if d == today.isoformat() else datetime.fromisoformat(d).strftime("%a %b %-d")
'''
DNAME_NEW = '''    pt327 = datetime.now(PT).date()  # change 327: named by the Pacific day, so a late-night change for tomorrow says "tomorrow"
    dname = lambda d: "today" if d == pt327.isoformat() else "tomorrow" if d == (pt327 + timedelta(days=1)).isoformat() else datetime.fromisoformat(d).strftime("%a %b %-d")
'''
HELP_OLD = '''# ---------- change 326: the day ESPN is on right now'''
HELP_NEW = '''# ---------- change 327: swaps saved from the app (lineup_holds.json, written by the app only) ----------
def _holds327(today):
    """{day: [(player in, player out), ...]} for today and later, ESPN ids as text"""
    try:
        with open(os.path.join(HERE, "lineup_holds.json"), encoding="utf-8") as f:
            d = json.load(f)
    except Exception:
        return {}
    out = {}
    for h in (d or {}).get("holds") or []:
        day = str(h.get("day") or "")
        if day >= today.isoformat() and h.get("in") and h.get("out"):
            out.setdefault(day, []).append((str(h["in"]).lstrip("e"), str(h["out"]).lstrip("e")))
    return out


# ---------- change 326: the day ESPN is on right now'''

PTS_OLD = '''lines.append(f"{dname(f['day'])}: {f['text']} +{f['gain']}")'''
PTS_NEW = '''lines.append(f"{dname(f['day'])}: {f['text']} {f['gain']:+}")  # change 327: -2.0, not +-2.0'''


def autopilot(t):
    t = lit(t, "327: keep swaps from the app", PL_OLD, PL_NEW, "forced327 = set()")
    t = lit(t, "327: swaps already counted", FILL_OLD, FILL_NEW, "and r[\"id\"] not in forced327)")
    t = lit(t, "327: read swaps", FOUND_OLD, FOUND_NEW, "holds327 = _holds327(today)")
    t = lit(t, "327: days with swaps are checked", SKIP_OLD, SKIP_NEW, "and day not in holds327:")
    t = lit(t, "327: hand swaps to the plan", PLAN_OLD, PLAN_NEW, '"holds327": holds327.get(day, [])')
    t = lit(t, "327: swaps go through", GAIN_OLD, GAIN_NEW, "swap327 = any(")
    t = lit(t, "327: note says your swap", TEXT_OLD, TEXT_NEW, '("Your swap: " if swap327 else "")')
    t = lit(t, "327: today or tomorrow by Pacific day", DNAME_OLD, DNAME_NEW, "pt327 = datetime.now(PT).date()")
    t = lit(t, "327: swap reader", HELP_OLD, HELP_NEW, "def _holds327(today):")
    t = lit(t, "327: points sign", PTS_OLD, PTS_NEW, "# change 327: -2.0, not +-2.0", count=2)
    return t


edit(APP, app)
edit("gm_autopilot.py", autopilot)
