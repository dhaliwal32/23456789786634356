# changes/085-injuries-tab.py - Team > Pickups > Injuries: every injured player, when he's back, who is good, and every injury update from the last 7 days

# ---------- the sync remembers injuries between runs (gm_signals.py) ----------
PY_FN = r'''

# ---------- change 085: injury updates (install.py) ----------
INJ_HIST = os.path.join(HERE, "inj_hist.json")
INJ_KEEP_DAYS = 7

def inj_moves(cur):
    """Remember every injured player's return date, status and news note between syncs.
    Report, for 7 days: newly injured, return date moved earlier or later, out to day-to-day,
    off the injury list, and new injury news ("nd" = date of the newest news)."""
    cur = cur or {}
    now = datetime.utcnow() - timedelta(hours=8)
    today = now.strftime("%Y-%m-%d")
    cutoff = (now - timedelta(days=INJ_KEEP_DAYS)).strftime("%Y-%m-%d")
    try:
        with open(INJ_HIST, encoding="utf-8") as f:
            h = json.load(f)
    except Exception:
        h = {}
    last, ev = h.get("last") or {}, h.get("ev") or {}
    fresh = lambda e: max(e.get("d", ""), e.get("nd", "")) >= cutoff
    # a broken or partial injury read must not look like everyone got healthy
    trusted = len(cur) >= 20 and any(x.get("src") == "espn" for x in cur.values()) and len(cur) >= 0.6 * len(last)
    if not trusted:
        print(f"(signals) injury updates: skipped, injury list looks incomplete ({len(cur)} players)")
        return {k: v for k, v in ev.items() if fresh(v)}
    first = not last
    out_words = ("injured reserve", "out", "suspen")
    for pid, x in cur.items():
        o = last.get(pid)
        b, st, note = x.get("back") or "", (x.get("status") or "").lower(), x.get("note") or ""
        old = ev.get(pid) if ev.get(pid) and fresh(ev[pid]) else None
        if o is None:
            if old and old.get("k") == "back":
                ev.pop(pid, None)          # he came back onto the list; the earlier "back" was a blip
            elif not first:
                ev[pid] = {"k": "new", "d": today, "now": b}
            continue
        ob, ost = o.get("back") or "", (o.get("status") or "").lower()
        e = None
        if b and ob and b != ob:
            was = old["was"] if old and old.get("k") in ("sooner", "later") and old.get("was") else ob
            if b != was:
                e = {"k": "sooner" if b < was else "later", "d": today, "was": was, "now": b}
            elif old and old.get("k") in ("sooner", "later"):
                ev.pop(pid, None)
                old = None
        elif "day-to-day" in st and any(w in ost for w in out_words):
            e = {"k": "dtd", "d": today, "was": o.get("status") or "", "now": b}
        if e:
            if old and old.get("nd"):
                e["nd"] = old["nd"]
            ev[pid] = e
            old = e
        if len(note) > 15 and note != (o.get("note") or ""):
            e = old or {"k": "news", "d": today}
            e["nd"] = today
            ev[pid] = e
    for pid, o in last.items():
        if pid not in cur:
            ev[pid] = {"k": "back", "d": today, "was": o.get("back") or ""}
    ev = {k: v for k, v in ev.items() if fresh(v)}
    h = {"last": {pid: {"back": x.get("back") or "", "status": x.get("status") or "", "note": x.get("note") or ""} for pid, x in cur.items()}, "ev": ev}
    with open(INJ_HIST, "w", encoding="utf-8") as f:
        json.dump(h, f, indent=0, sort_keys=True)
    print(f"(signals) injury updates: {len(ev)} in the last {INJ_KEEP_DAYS} days")
    return ev
'''

def change_py(t):
    t = lit(t, "085: injury updates function", "\n\n# ---------- ice time trends ----------", PY_FN + "\n\n# ---------- ice time trends ----------", "change 085: injury updates")
    t = lit(t, "085: run it after injuries",
            '("toi", lambda: toi(players)),',
            '("injmoves", lambda: inj_moves(out.get("injuries"))), ("toi", lambda: toi(players)),',
            '("injmoves", lambda: inj_moves(out.get("injuries")))')
    return t

edit("gm_signals.py", change_py)

# ---------- the Injuries page (fantasy-gm.html) ----------
NEW_CSS = r'''  /* change 085 (install.py) */
  .gx-ij85 { display: grid; grid-template-columns: 26px minmax(0,1fr) 48px; gap: 10px; align-items: center; padding: 9px 0; border-top: 1px solid var(--line); font-size: 14px; }
  .gx-ij85.first { border-top: 0; }
  .gx-ij85 .n { text-align: right; font-variant-numeric: tabular-nums; }
  .gx-ij85 .up { color: var(--good); }
  .gx-ij85 .dn { color: var(--bad); }
  .gx-ij85 .wn { color: var(--warn); }
  .gx-ij85 .nt { display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
  .gx-ij85 .nt.open { -webkit-line-clamp: unset; }
  .gx-ij85 .good { font-size: 11px; color: var(--good); border: 1px solid var(--good); border-radius: 999px; padding: 0 6px; margin-left: 6px; }
</style>'''

HELPERS = r'''// ---------- change 085: Injuries page under Team > Pickups (install.py) ----------
const gxIjDays = (d) => Math.round((fromIso(d) - fromIso(todayISO())) / 864e5);
const gxIjWhen = (d) => { const n = gxIjDays(d); return n < 0 ? "any day now" : n === 0 ? "today" : n === 1 ? "tomorrow" : "in " + n + " days"; };
const gxIjAgo = (d) => { const n = -gxIjDays(d); return n <= 0 ? "today" : n === 1 ? "yesterday" : mdL(d); };
const gxIjLast = (e) => (e.nd && e.nd > e.d ? e.nd : e.d);
const gxIjNote = (n) => (n && n.length > 15 ? n : "");
function GxInjPage({ s }) {
  const [, tick] = useState(0);
  useEffect(() => { const h = () => tick((x) => x + 1); window.addEventListener("gm-watch", h); return () => window.removeEventListener("gm-watch", h); }, []);
  const [who, setWho] = useState(() => uiGet()["ij85:who"] || "fa");
  const [pos, setPos] = useState("all");
  const [allP, setAllP] = useState(false);
  const [moreU, setMoreU] = useState(false);
  const [moreL, setMoreL] = useState(false);
  const [openN, setOpenN] = useState({});
  const K = s.blend;
  const pick = (v) => { setWho(v); uiSet("ij85:who", v); };
  const D = useMemo(() => {
    const S = window.__SIG || {}, EV = S.injmoves || {};
    const val = (p) => effAvg(p, K) * (p.p === "G" ? p.prob || 0.5 : 1);
    const mine = s.players.filter((p) => p.ft === s.me && !p.ir);
    const bar = {};
    ["F", "D", "G"].forEach((g) => { const v = mine.filter((p) => p.p === g).map(val); bar[g] = v.length ? Math.min(...v) : 0; });
    const list = [], ups = [];
    s.players.forEach((p) => {
      const id = typeof p.id === "string" && p.id[0] === "e" ? p.id.slice(1) : null;
      const inj = autoInj(p), e = id ? EV[id] : null;
      if (!inj && !(e && e.k === "back")) return;
      const v = val(p), good = v > 0 && v >= bar[p.p];
      const r = { p, v, good, inj, e, back: inj ? effBack(p).d : "" };
      if (inj) list.push(r);
      if (e) ups.push(r);
    });
    return { list, ups };
  }, [s]);
  const inWho = (r) => (who === "fa" ? r.p.ft === "fa" : who === "mine" ? r.p.ft === s.me : true);
  const keep = (r) => inWho(r) && (pos === "all" || r.p.p === pos) && (allP || who === "mine" || r.good);
  const ups = D.ups.filter(keep).sort((a, b) => gxIjLast(b.e).localeCompare(gxIjLast(a.e)) || b.v - a.v);
  const list = D.list.filter(keep).sort((a, b) => (a.back || "9").localeCompare(b.back || "9") || b.v - a.v);
  const groups = [
    ["Back within a week", list.filter((r) => r.back && gxIjDays(r.back) <= 7)],
    ["Back in 1 to 4 weeks", list.filter((r) => r.back && gxIjDays(r.back) > 7 && gxIjDays(r.back) <= 30)],
    ["Out longer", list.filter((r) => r.back && gxIjDays(r.back) > 30)],
    ["No return date", list.filter((r) => !r.back)],
  ];
  const evTxt = (e) => {
    if (e.k === "back") return <span className="up">{"Off the injury list"}</span>;
    if (e.k === "sooner") return <span className="up">{"Back sooner: was " + mdL(e.was) + ", now " + mdL(e.now)}</span>;
    if (e.k === "dtd") return <span className="up">{"Now day-to-day (was " + (e.was || "out").replace("Injured Reserve", "IR") + ")"}</span>;
    if (e.k === "later") return <span className="wn">{"Pushed back: was " + mdL(e.was) + ", now " + mdL(e.now)}</span>;
    if (e.k === "new") return <span className="dn">{"Newly injured" + (e.now ? ", back about " + mdL(e.now) : "")}</span>;
    return <span>{"New injury news"}</span>;
  };
  const owner = (p) => (p.ft === "fa" ? "Free agent" : p.ft === s.me ? "Your team" : teamName(s, p.ft));
  const row = (r, i, upd) => {
    const st = r.inj ? (r.inj.status || "Out").replace("Injured Reserve", "IR") + (r.inj.type ? " · " + r.inj.type : "") + (r.back ? " · back " + mdL(r.back) + " (" + gxIjWhen(r.back) + ")" : "") : "Healthy now";
    const note = r.inj ? gxIjNote(r.inj.note) : "", nk = (upd ? "u" : "l") + r.p.id;
    return (
      <div key={nk} className={"gx-ij85" + (i ? "" : " first")}>
        <TeamLogo t={r.p.t} size={26} />
        <div className="min-w-0">
          <div className="truncate"><PN p={r.p} className="" /> <span className="text-xs text-slate-500">{r.p.p}</span>{r.good && allP && who !== "mine" ? <span className="good">Good</span> : null}{r.p.wv ? <span className="text-xs" style={{ color: "var(--warn)", marginLeft: 6 }}>on waivers</span> : null}</div>
          <div className="text-xs text-slate-500">{(who === "fa" ? "" : owner(r.p) + " · ") + st}</div>
          {upd && r.e ? <div className="text-xs">{evTxt(r.e)}<span className="text-slate-500">{" · " + gxIjAgo(gxIjLast(r.e))}</span></div> : !upd && r.e && r.e.k !== "news" ? <div className="text-xs">{evTxt(r.e)}</div> : null}
          {note && (upd || openN[nk]) ? <div className={"text-xs text-slate-500 nt" + (openN[nk] ? " open" : "")} role="button" onClick={() => setOpenN((x) => ({ ...x, [nk]: !x[nk] }))}>{note}</div> : null}
          <div className="text-xs text-slate-500">
            {!upd && note && !openN[nk] ? <span><button type="button" className="text-blue-600" onClick={() => setOpenN((x) => ({ ...x, [nk]: true }))}>Latest news</button>{r.p.ft === "fa" ? " · " : ""}</span> : null}
            {r.p.ft === "fa" ? <span><button type="button" className="text-blue-600" onClick={() => gxWatch.toggle(r.p.id)}>{gxWatch.has(r.p.id) ? "Watching" : "Watch"}</button>{" · "}<button type="button" className="text-blue-600" onClick={() => { if (window.__QA) window.__QA.espn(r.p); }}>Add on ESPN</button></span> : null}
          </div>
        </div>
        <div className="n"><div className="font-semibold">{f1(effAvg(r.p, K))}</div><div className="text-xs text-slate-500">pts/g</div></div>
      </div>
    );
  };
  const upsShown = moreU ? ups : ups.slice(0, 5);
  return (
    <div className="space-y-3">
      <div className="flex flex-wrap gap-2 items-center">
        <Pills items={[["fa", "Free agents"], ["mine", "My team"], ["all", "All teams"]]} value={who} onChange={pick} />
        <Pills items={[["all", "All"], ["F", "Forwards"], ["D", "Defence"], ["G", "Goalies"]]} value={pos} onChange={setPos} />
      </div>
      {who !== "mine" ? <div className="text-xs text-slate-500">{allP ? "Showing every injured player. " : "Showing good players only: better than your weakest at their position once healthy. "}<button type="button" className="text-blue-600" onClick={() => setAllP(!allP)}>{allP ? "Good players only" : "Show everyone"}</button></div> : null}
      <GxPanel title="Updates" right="last 7 days">
        {ups.length ? upsShown.map((r, i) => row(r, i, true)) : <div className="text-sm text-slate-500" style={{ padding: "4px 0" }}>No injury updates in the last 7 days{who === "fa" ? " for these free agents" : ""}. New return dates, day-to-day moves and fresh news show up here.</div>}
        {ups.length > 5 ? <button type="button" className="text-sm text-blue-600" style={{ marginTop: 8 }} onClick={() => setMoreU(!moreU)}>{moreU ? "Show fewer" : "Show all " + ups.length + " updates"}</button> : null}
      </GxPanel>
      {groups.map(([title, g]) => {
        if (!g.length) return null;
        const longer = title === "Out longer" || title === "No return date";
        const shown = longer && !moreL ? g.slice(0, 3) : g;
        return (
          <GxPanel key={title} title={title} right={g.length + (g.length === 1 ? " player" : " players")}>
            {shown.map((r, i) => row(r, i, false))}
            {shown.length < g.length ? <button type="button" className="text-sm text-blue-600" style={{ marginTop: 8 }} onClick={() => setMoreL(true)}>{"Show " + (g.length - shown.length) + " more"}</button> : null}
          </GxPanel>
        );
      })}
      {!list.length ? <div className="text-sm text-slate-500">No injured players match.</div> : null}
    </div>
  );
}
'''

def change(t):
    t = lit(t, "085: styles", "</style>", NEW_CSS, "change 085 (install.py)")
    t = lit(t, "085: helpers", ROOT, HELPERS + ROOT, "change 085: Injuries page")
    t = lit(t, "085: Injuries tab name",
            'const PICK_SUBS = [["adddrop", "Pickups"], ["advice", "Advice"], ["goalies", "Goalies"]];',
            'const PICK_SUBS = [["adddrop", "Pickups"], ["advice", "Advice"], ["goalies", "Goalies"], ["injuries", "Injuries"]];',
            '["injuries", "Injuries"]];')
    t = lit(t, "085: Injuries page route",
            'sub === "goalies" ? <GoalieStreams {...P} /> :',
            'sub === "goalies" ? <GoalieStreams {...P} /> : sub === "injuries" ? <GxInjPage {...P} /> :',
            'sub === "injuries" ? <GxInjPage {...P} /> :')
    return t

edit(APP, change)
