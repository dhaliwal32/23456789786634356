# changes/258-injury-watch-alerts.py - injury alerts for watched players (McCann, Marchand): return date moves, status, back in lineup, news; Injury alerts button on the player screen

# ---------- the list: McCann and Marchand (Terry off) ----------
def prefs(t):
    t = lit(t, "258: watch list", '"pickup_bigger_role": true\n}', '"pickup_bigger_role": true,\n  "return_watch": ["Jared McCann", "Brad Marchand"]\n}', '"return_watch": ["Jared McCann", "Brad Marchand"]')
    return t

edit("alert_prefs.json", prefs)

# ---------- gm_lines: the app's list (settings.json "rwatch") comes first ----------
LINES_OLD = '''def _watch121():
    try:
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "alert_prefs.json"), encoding="utf-8") as f:'''
LINES_NEW = '''def _watch121():
    try:  # change 258: the list saved from the app's Injury alerts button
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "settings.json"), encoding="utf-8") as f:
            w = json.load(f).get("rwatch")
        if isinstance(w, list):
            return {norm(x) for x in w if isinstance(x, str)}
    except Exception:
        pass
    try:
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "alert_prefs.json"), encoding="utf-8") as f:'''

def lines(t):
    t = lit(t, "258: gm_lines watch list", LINES_OLD, LINES_NEW, "# change 258: the list saved from the app's Injury alerts button")
    return t

edit("gm_lines.py", lines)

# ---------- gm_signals: return date moves, injury news, and one first alert per newly watched player ----------
SIG_HELP = r'''# ---------- change 258: injury alerts for watched players (install.py) ----------
RW_STATE258 = os.path.join(HERE, "rw_state.json")


def _rw_names258():
    for fn, key in (("settings.json", "rwatch"), ("alert_prefs.json", "return_watch")):
        try:
            with open(os.path.join(HERE, fn), encoding="utf-8") as f:
                w = json.load(f).get(key)
            if isinstance(w, list):
                return [x for x in w if isinstance(x, str)]
        except Exception:
            pass
    return ["Troy Terry"]


def _md258(d):
    try:
        x = datetime.strptime(str(d)[:10], "%Y-%m-%d")
        return x.strftime("%b ") + str(x.day)
    except Exception:
        return str(d or "?")


def rw_alerts258(ev, cur, players):
    """a few words each, titled Fantasy GM: first alert when a player is added, then every time his return date
    or ESPN's injury note changes. Status changes and back-in-lineup alerts come from gm_lines.py (change 121)."""
    try:
        import gm_notify
    except Exception as ex:
        print(f"(signals) injury alerts unavailable: {ex}")
        return ev
    try:
        import hashlib
        names = {norm(n): n for n in _rw_names258()}
        try:
            with open(RW_STATE258, encoding="utf-8") as f:
                st = json.load(f)
        except Exception:
            st = {}
        hello = set(st.get("hello") or []) & set(names)
        seen = st.get("seen") or {}
        sent = 0
        for p in players or []:
            k = norm(p.get("n") or "")
            if k not in names:
                continue
            pid, last = str(p.get("id")), str(p.get("n") or "").split()[-1]
            x = (cur or {}).get(pid)
            if k not in hello:
                if x:
                    msg = f"{last} back around {_md258(x['back'])}" if x.get("back") else f"{last} out, no return date yet"
                else:
                    msg = f"{last} is not on the injury list"
                gm_notify.add(f"rw258|hello|{pid}", "Fantasy GM", msg, "mine", urgent=True)
                hello.add(k)
                sent += 1
                if x:
                    seen[pid] = {"back": x.get("back") or "", "note": x.get("note") or ""}
                continue
            if not x:
                continue
            o = seen.get(pid) or {}
            b, ob, note = x.get("back") or "", o.get("back") or "", x.get("note") or ""
            dated = False
            if b and ob and b != ob:
                gm_notify.add(f"rw258|date|{pid}|{ob}|{b}", "Fantasy GM", f"{last} return moved to {_md258(b)} (was {_md258(ob)})", "mine", urgent=True)
                dated = True
                sent += 1
            if len(note) > 15 and note != (o.get("note") or "") and o and not dated:
                h = hashlib.md5(note.encode("utf-8")).hexdigest()[:10]
                gm_notify.add(f"rw258|news|{pid}|{h}", "Fantasy GM", f"{last} injury news", "mine", urgent=True)
                sent += 1
            seen[pid] = {"back": b or ob, "note": note or o.get("note") or ""}
        seen = {k2: v for k2, v in seen.items() if any(str(q.get("id")) == k2 and norm(q.get("n") or "") in names for q in players or [])}
        with open(RW_STATE258, "w", encoding="utf-8") as f:
            json.dump({"hello": sorted(hello), "seen": seen}, f, indent=0, sort_keys=True)
        print(f"(signals) injury alerts: watching {len(names)}, {sent} handed to notifications")
    except Exception as ex:
        print(f"(signals) injury alerts failed: {type(ex).__name__}: {ex}")
    return ev


def build(players):'''

def signals(t):
    t = lit(t, "258: signals helper", "def build(players):", SIG_HELP, "# ---------- change 258: injury alerts for watched players")
    t = lit(t, "258: signals step",
            '("injmoves", lambda: inj_moves(out.get("injuries"))),',
            '("injmoves", lambda: rw_alerts258(inj_moves(out.get("injuries")), out.get("injuries"), players)),',
            "rw_alerts258(inj_moves(")
    return t

edit("gm_signals.py", signals)

# ---------- app: Injury alerts button on the player screen, list kept on the device and synced ----------
NEW_CSS = r'''  /* change 258 (install.py) */
  .gx-pd-ac button.rw258.on, .gx-pdm .bt button.rw258.on { border-color: var(--ink2); }
  .gx-pdm .bt button.rw258 { white-space: nowrap; }
</style>'''

HELPERS = r'''// ---------- change 258: Injury alerts list (install.py) ----------
// names, kept on this device ("gx-rw258") and in settings.json ("rwatch") when sync is on; the GitHub side reads it every sync
const GX_RW258 = "gx-rw258";
const gxRw258 = {
  get: () => { try { const r = localStorage.getItem(GX_RW258); if (r == null) return null; const a = JSON.parse(r); return Array.isArray(a) ? a : []; } catch (e) { return null; } },
  set: (l) => {
    const a = [...new Set((l || []).filter((x) => typeof x === "string"))].sort();
    const raw = JSON.stringify(a);
    let old = null;
    try { old = localStorage.getItem(GX_RW258); } catch (e) {}
    if (raw === old) return;
    try { localStorage.setItem(GX_RW258, raw); } catch (e) {}
    window.dispatchEvent(new Event("gx-rw258"));
  },
  has: (p) => (gxRw258.get() || window.__RW258 || []).some((n) => nrm(n) === nrm(p && p.n)),
  toggle: (p) => {
    const l = (gxRw258.get() || window.__RW258 || []).slice();
    const i = l.findIndex((n) => nrm(n) === nrm(p.n));
    if (i >= 0) l.splice(i, 1); else l.push(p.n);
    gxRw258.set(l);
  },
};
// first time on a device: start from the list the GitHub side uses (alert_prefs.json)
(function gxRwSeed258() {
  try {
    if (gxRw258.get() != null) return;
    fetch("alert_prefs.json?t=" + Date.now(), { cache: "no-store" }).then((r) => (r.ok ? r.json() : null)).then((j) => {
      if (gxRw258.get() != null) return;
      const l = j && Array.isArray(j.return_watch) ? j.return_watch : [];
      window.__RW258 = l;
      gxRw258.set(l);
    }).catch(() => {});
  } catch (e) {}
})();
function GxRwBtn258({ p }) {
  const [, tick] = useState(0);
  useEffect(() => { const h = () => tick((x) => x + 1); window.addEventListener("gx-rw258", h); return () => window.removeEventListener("gx-rw258", h); }, []);
  if (!p) return null;
  const on = gxRw258.has(p);
  const hurt = p.status && String(p.status).toUpperCase() !== "ACTIVE";
  if (!on && !hurt) return null;
  return <button type="button" className={"rw258" + (on ? " on" : "")} data-gx="258" onClick={() => gxRw258.toggle(p)}>{on ? "Injury alerts on" : "Injury alerts"}</button>;
}
'''

def change(t):
    t = lit(t, "258: styles", "</style>", NEW_CSS, "change 258 (install.py)")
    t = lit(t, "258: helpers", ROOT, HELPERS + ROOT, "change 258: Injury alerts list")
    t = lit(t, "258: sync sends the list",
            'hide: gxHide.list() /* gx075-s1 */, theme:',
            'hide: gxHide.list() /* gx075-s1 */, ...(gxRw258.get() ? { rwatch: gxRw258.get() } : {}) /* gx258 */, theme:',
            '{ rwatch: gxRw258.get() } : {}) /* gx258 */')
    t = lit(t, "258: sync compares the list",
            'P.theme || "auto"]);',
            'P.theme || "auto", Array.isArray(P.rwatch) ? P.rwatch.slice().sort() : null /* gx258 */]);',
            'P.rwatch.slice().sort() : null /* gx258 */')
    t = lit(t, "258: sync reads the list",
            'if (Array.isArray(R.hide)) gxHide.set(R.hide); /* gx075-s3 */',
            'if (Array.isArray(R.hide)) gxHide.set(R.hide); /* gx075-s3 */ if (Array.isArray(R.rwatch)) gxRw258.set(R.rwatch); /* gx258 */',
            'gxRw258.set(R.rwatch); /* gx258 */')
    t = lit(t, "258: sync notices changes",
            'window.addEventListener("gm-hide", h); /* gx075-s4 */',
            'window.addEventListener("gm-hide", h); /* gx075-s4 */ window.addEventListener("gx-rw258", h); /* gx258 */',
            'window.addEventListener("gx-rw258", h); /* gx258 */')
    t = lit(t, "258: phone button",
            '''<button type="button" onClick={() => { gxHide.toggle(p.id); close101(); }}>{gxHideSet().has(p.id) ? "Show" : "Hide"}</button></>}
                </div>''',
            '''<button type="button" onClick={() => { gxHide.toggle(p.id); close101(); }}>{gxHideSet().has(p.id) ? "Show" : "Hide"}</button></>}
                  <GxRwBtn258 p={p} />
                </div>''',
            '                  <GxRwBtn258 p={p} />\n')
    t = lit(t, "258: laptop button",
            '''{Q.fa(p) ? <GxPdWatch p={p} Q={Q} /> : null}''',
            '''<GxRwBtn258 p={p} />{Q.fa(p) ? <GxPdWatch p={p} Q={Q} /> : null}''',
            '<GxRwBtn258 p={p} />{Q.fa(p)')
    return t

edit(APP, change)
