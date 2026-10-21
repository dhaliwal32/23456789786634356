# changes/090-autopilot-days-ahead.py - Autopilot: choose how many days ahead to set lineups (set once, then only on the day or when you tap Redo); mode and days can be changed in the app

AUTOPILOT_PY = r'''"""
gm_autopilot.py - change 089: sets your ESPN lineup for today by itself.

Runs at the end of every sync (espn_sync.py calls run()). It works out the best
legal lineup for today from the app's projections and Daily Faceoff's starting
goalies, then either:
  mode "test" - only writes what it WOULD do to autopilot_log.json and sends a phone note
  mode "on"   - makes the change on ESPN, logs it and sends a phone note
  mode "off"  - does nothing
The switch lives in autopilot.json (edit it on GitHub). It starts in "test".

Safety rules:
  - only ever touches your own team (MY_TEAM_ID) and only today's scoring day
  - never moves a player whose game has started (ESPN locks him) or anyone in an IR slot
  - one all-or-nothing request per day it changes
  - days after today (autopilot.json "days_ahead") are set once, then only changed again on the day itself
    or when you tap "Redo upcoming days" in the app (it writes "redo_at")
  - changes only when the new lineup is worth at least min_gain more points today
"""
import json
import os
import re
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

HERE = os.path.dirname(os.path.abspath(__file__))
CONF = os.path.join(HERE, "autopilot.json")
LOG = os.path.join(HERE, "autopilot_log.json")
ET = ZoneInfo("America/New_York")
PT = ZoneInfo("America/Vancouver")
WRITES = "https://lm-api-writes.fantasy.espn.com/apis/v3/games/fhl/seasons/{season}/segments/0/leagues/{league}/transactions/"
DEFAULT_CONF = {"mode": "test", "days_ahead": 0, "redo_at": "", "min_gain": 0.5, "goalies": True, "skaters": True,
                "notes": "mode: test = only tell me, on = change my ESPN lineup, off = do nothing. days_ahead: 0 = today only, 1-14 = that many days after today, week = through Sunday"}
SLOT_F, SLOT_D, SLOT_G, SLOT_U, SLOT_BENCH, SLOT_IR = 3, 4, 5, 6, 7, 8
CAP = {SLOT_F: 9, SLOT_D: 5, SLOT_U: 1, SLOT_G: 2}
ACTIVE = (SLOT_F, SLOT_D, SLOT_U, SLOT_G)
STICK = 0.75          # a player already starting keeps his spot unless someone is this much better
OUTS = ("OUT", "INJURY_RESERVE", "SUSPENSION")
MAX_NOTES_TEST = 4    # test mode: at most this many phone notes a day


def _read_js(name):
    p = os.path.join(HERE, name)
    if not os.path.exists(p):
        return {}
    t = open(p, encoding="utf-8").read()
    return json.loads(t[t.index("{"):t.rindex("}") + 1])


def conf():
    c = dict(DEFAULT_CONF)
    try:
        with open(CONF, encoding="utf-8") as f:
            c.update(json.load(f) or {})
    except FileNotFoundError:
        with open(CONF, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_CONF, f, indent=2)
        print("(autopilot) created autopilot.json in test mode")
    except Exception as ex:
        print(f"(autopilot) autopilot.json could not be read ({ex}), staying off")
        c["mode"] = "off"
    c["mode"] = str(c.get("mode", "test")).strip().lower()
    return c


def load_log():
    try:
        with open(LOG, encoding="utf-8") as f:
            b = json.load(f)
        if isinstance(b, dict):
            b.setdefault("entries", [])
            b.setdefault("state", {})
            return b
    except Exception:
        pass
    return {"entries": [], "state": {}}


def save_log(b):
    b["entries"] = b["entries"][-60:]
    with open(LOG, "w", encoding="utf-8") as f:
        json.dump(b, f, indent=1)


def _nrm(s):
    import unicodedata
    s = unicodedata.normalize("NFD", s or "")
    return "".join(c for c in s if unicodedata.category(c) != "Mn").lower().strip()


def start_chance(p, day, E):
    """Same rules as the app: Daily Faceoff confirmed 100%, likely 85%, unconfirmed 50%,
    another goalie named for his team means he sits; otherwise his recent start share."""
    g = (E.get("goalies") or {}).get(day) or {}
    names = {_nrm(k): v for k, v in g.items()}
    me = names.get(_nrm(p["n"]))
    lvl = lambda st: 1.0 if ("confirm" in st and "un" not in st) else 0.85 if re.search(r"likely|expected|project", st) else 0.5
    if me:
        return lvl((me.get("status") or "").lower()), "Daily Faceoff"
    mate = next((v for v in g.values() if v.get("team") == p["t"]), None)
    if mate:
        return 1 - lvl((mate.get("status") or "").lower()), "Daily Faceoff"
    gs = ((E.get("signals") or {}).get("gstart") or {}).get(str(p["id"])) or {}
    return float(gs.get("share", 0.5)), "start share"


def value(p, day, E):
    """Expected fantasy points today, before the game: projection x start chance x healthy."""
    base = p.get("pavg") or p.get("avg") or 0
    v = (base * 10 + (p.get("tot") or 0)) / (10 + p["gp"]) if p.get("gp") else base
    mv = (((E.get("model") or {}).get("proj") or {}).get(str(p["id"])) or {}).get(day)
    if mv is not None:
        v = (v + mv) / 2
    inj = ((E.get("signals") or {}).get("injuries") or {}).get(str(p["id"])) or {}
    st = (p.get("status") or "ACTIVE").upper()
    ist = (inj.get("status") or "").lower()
    if st in OUTS or "out" in ist or "reserve" in ist or "suspen" in ist:
        if not (inj.get("back") and inj["back"] <= day):
            return 0.0, "out"
    why = ""
    if p["p"] == "G":
        sc, src = start_chance(p, day, E)
        v *= sc
        why = f"{round(sc * 100)}% to start"
    if st == "DAY_TO_DAY" or "day-to-day" in ist:
        v *= 0.8
        why = (why + ", " if why else "") + "day-to-day"
    return v, why


def plan(roster, day, games, E, c):
    """roster: list of dicts {id, n, t, p, slot, locked, elig, ...espn-data fields}.
    Returns (moves, before, after, notes)."""
    cap = dict(CAP)
    for r in roster:
        if r["locked"] and r["slot"] in ACTIVE:
            cap[r["slot"]] -= 1
    free = [r for r in roster if not r["locked"] and r["slot"] != SLOT_IR]
    for r in roster:
        has = r["t"] in games
        v, why = value(r, day, E) if has else (0.0, "no game")
        r["v"], r["why"] = round(v, 2), why
    sc = lambda r: r["v"] + (STICK if r["slot"] in ACTIVE and r["v"] > 0 else 0)
    want = {}
    if not c.get("goalies", True):
        for r in free:
            if r["p"] == "G":
                want[r["id"]] = r["slot"]
                if r["slot"] == SLOT_G:
                    cap[SLOT_G] -= 1
    if not c.get("skaters", True):
        for r in free:
            if r["p"] != "G":
                want[r["id"]] = r["slot"]
                if r["slot"] in ACTIVE:
                    cap[r["slot"]] -= 1
    left = [r for r in free if r["id"] not in want]

    def take(pos, slot):
        pool = sorted([r for r in left if r["p"] == pos and r["v"] > 0 and r["id"] not in want], key=sc, reverse=True)
        for r in pool[:max(0, cap[slot])]:
            want[r["id"]] = slot
    take("G", SLOT_G)
    take("D", SLOT_D)
    take("F", SLOT_F)
    util = sorted([r for r in left if r["p"] in ("F", "D") and r["v"] > 0 and r["id"] not in want
                   and (not r["elig"] or SLOT_U in r["elig"])], key=sc, reverse=True)
    for r in util[:max(0, cap[SLOT_U])]:
        want[r["id"]] = SLOT_U
    for r in left:
        want.setdefault(r["id"], SLOT_BENCH)
    # keep starters in the starting spot they already have (F slot vs UTIL) so nothing moves for nothing
    for r in left:
        a = want[r["id"]]
        if a in (SLOT_F, SLOT_U, SLOT_D) and r["slot"] in (SLOT_F, SLOT_U, SLOT_D) and r["slot"] != a:
            mate = next((q for q in left if want[q["id"]] == r["slot"] and q["slot"] == a and q["p"] == r["p"]), None)
            if mate:
                want[r["id"]], want[mate["id"]] = r["slot"], a
    moves = [{"r": r, "from": r["slot"], "to": want[r["id"]]} for r in left if want[r["id"]] != r["slot"]]
    total = lambda f: sum(r["v"] for r in roster if f(r) in ACTIVE)
    before = total(lambda r: r["slot"])
    after = total(lambda r: want.get(r["id"], r["slot"]))
    return moves, round(before, 1), round(after, 1)


def describe(moves):
    ins = [m["r"] for m in moves if m["to"] in ACTIVE and m["from"] not in ACTIVE]
    outs = [m["r"] for m in moves if m["from"] in ACTIVE and m["to"] not in ACTIVE]
    def names(rs, why):
        out = [r["n"].split(" ")[-1] + (" (" + r["why"] + ")" if why and r["p"] == "G" and r.get("why") else "") for r in rs[:4]]
        return ", ".join(out) + (f" +{len(rs) - 4} more" if len(rs) > 4 else "")
    parts = []
    if ins:
        parts.append("start " + names(ins, True))
    if outs:
        nog = all(r.get("why") == "no game" for r in outs)
        parts.append("bench " + names(outs, False) + (" (no game)" if nog else ""))
    if not parts and moves:
        parts.append("move " + names([m["r"] for m in moves], False) + " between starting spots")
    s = "; ".join(parts)
    return s[:1].upper() + s[1:] + "."


def _when(x):
    try:
        return datetime.fromisoformat(str(x).replace("Z", "+00:00"))
    except Exception:
        return None


def days_ahead(c, today):
    """How many days after today to set. "week" = through Sunday, the end of the matchup week."""
    v = c.get("days_ahead", 0)
    if str(v).lower() == "week":
        return 6 - today.weekday()
    try:
        return max(0, min(14, int(v)))
    except Exception:
        return 0


def _post(session, url, my_team_id, swid, sp, future, moves):
    body = {"isLeagueManager": False, "teamId": my_team_id, "type": "FUTURE_ROSTER" if future else "ROSTER", "memberId": swid,
            "scoringPeriodId": sp, "executionType": "EXECUTE",
            "items": [{"playerId": m["r"]["id"], "type": "LINEUP", "fromLineupSlotId": m["from"], "toLineupSlotId": m["to"]} for m in moves]}
    try:
        w = session.post(url, json=body, headers={"Content-Type": "application/json"}, timeout=30)
        try:
            js = w.json()
        except Exception:
            js = {}
        if w.status_code < 300:
            return True, js.get("status") or "EXECUTED"
        msg = ", ".join(str(x.get("message") or x.get("type") or x) for x in (js.get("details") or js.get("messages") or [])) or w.text[:200]
        return False, msg
    except Exception as ex:
        return False, f"{type(ex).__name__}: {ex}"


def run(session, league_url, my_team_id, swid, season, league_id):
    c = conf()
    if c["mode"] == "off":
        print("(autopilot) off")
        return
    E = _read_js("espn-data.js")
    G = _read_js("games-data.js")
    now_et = datetime.now(ET)
    today = now_et.date()
    n_ahead = days_ahead(c, today)
    b = load_log()
    st = b["state"]
    if st.get("day") != today.isoformat():
        st.update({"day": today.isoformat(), "notes": 0, "sent": []})
        st.pop("failed", None)
    planned = {d: v for d, v in (st.get("planned") or {}).items() if d > today.isoformat()}
    st["planned"] = planned
    redo = _when(c.get("redo_at"))
    byid = {p["id"]: p for p in E.get("players") or []}
    url = WRITES.format(season=season, league=league_id)
    min_gain = float(c.get("min_gain", 0.5))
    stamp = datetime.now(PT).strftime("%-I:%M %p")
    found = []
    for k in range(n_ahead + 1):
        dd = today + timedelta(days=k)
        day = dd.isoformat()
        future = k > 0
        if future:
            last = _when(planned.get(day))
            if last and not (redo and redo > last):
                continue          # already set: only the day itself or a redo changes it again
        sp = next((p["id"] for p in (E.get("periods") or []) if day in (p.get("dates") or [])), None)
        games = (G.get("games") or {}).get(day) or {}
        if not sp or not games:
            if future:
                planned[day] = datetime.now(PT).isoformat(timespec="seconds")
            continue
        r = session.get(league_url, params=[("view", "mRoster"), ("forTeamId", my_team_id), ("scoringPeriodId", sp)], timeout=30)
        r.raise_for_status()
        team = next((t for t in r.json().get("teams", []) if t.get("id") == my_team_id), None)
        entries = (team or {}).get("roster", {}).get("entries", [])
        if len(entries) < 15:
            print(f"(autopilot) {day}: your roster came back with {len(entries)} players, so nothing was changed")
            continue
        roster = []
        for en in entries:
            pe = en.get("playerPoolEntry") or {}
            pl = pe.get("player") or {}
            base = byid.get(en.get("playerId"))
            if base:
                roster.append({**base, "slot": en.get("lineupSlotId"), "locked": (not future) and bool(pe.get("lineupLocked")),
                               "elig": pl.get("eligibleSlots") or []})
        moves, before, after = plan(roster, day, games, E, c)
        gain = round(after - before, 1)
        if future:
            planned[day] = datetime.now(PT).isoformat(timespec="seconds")
        if not moves or gain < min_gain:
            print(f"(autopilot) {day}: lineup is already the best (projected {before})")
            continue
        found.append({"day": day, "sp": sp, "future": future, "moves": moves, "before": before, "after": after, "gain": gain, "text": describe(moves)})
    if not found:
        save_log(b)
        return
    try:
        import gm_notify
        note = gm_notify.push
    except Exception:
        note = lambda *a, **k: False
    dname = lambda d: "today" if d == today.isoformat() else datetime.fromisoformat(d).strftime("%a %b %-d")
    lines, fails = [], []
    for f in found:
        entry = {"at": datetime.now(PT).isoformat(timespec="seconds"), "day": f["day"], "mode": c["mode"], "text": f["text"],
                 "gain": f["gain"], "before": f["before"], "after": f["after"],
                 "moves": [{"id": m["r"]["id"], "n": m["r"]["n"], "from": m["from"], "to": m["to"], "why": m["r"].get("why", "")} for m in f["moves"]]}
        if c["mode"] != "on":
            sig = f["day"] + "|" + "|".join(sorted(f"{m['r']['id']}:{m['to']}" for m in f["moves"]))
            if sig in st["sent"]:
                continue
            st["sent"].append(sig)
            entry["result"] = "test only"
            b["entries"].append(entry)
            lines.append(f"{dname(f['day'])}: {f['text']} +{f['gain']}")
            print(f"(autopilot) test {f['day']}: would {f['text']} (+{f['gain']})")
            continue
        ok, msg = _post(session, url, my_team_id, swid, f["sp"], f["future"], f["moves"])
        entry["result"] = "done" if ok else "failed: " + str(msg)[:200]
        b["entries"].append(entry)
        if ok:
            lines.append(f"{dname(f['day'])}: {f['text']} +{f['gain']}")
            print(f"(autopilot) changed {f['day']}: {f['text']} (+{f['gain']})")
        else:
            fails.append(f"{dname(f['day'])}: ESPN said {msg}")
            if f["future"]:
                planned.pop(f["day"], None)   # try that day again next sync
            print(f"(autopilot) ESPN refused the change for {f['day']}: {msg}")
    if lines:
        if c["mode"] != "on":
            if st["notes"] < MAX_NOTES_TEST:
                st["notes"] += 1
                note("Autopilot test", f"Would change your lineup ({stamp}):\n" + "\n".join(lines) + "\nNothing was changed on ESPN.")
        else:
            note("Autopilot", f"Changed your lineup ({stamp}):\n" + "\n".join(lines))
    if fails and not st.get("failed"):
        st["failed"] = 1
        note("Autopilot could not change your lineup", "\n".join(fails) + ". Set it by hand on ESPN.", "high")
    save_log(b)
'''

HELPERS = r'''// ---------- change 090: autopilot controls in the app, lineups set days ahead (install.py) ----------
const GX_AP_API = "https://api.github.com/repos/dhaliwal32/23456789786634356/contents/autopilot.json";
const GX_AP_RUN = "https://api.github.com/repos/dhaliwal32/23456789786634356/actions/workflows/sync.yml/dispatches";
const gxApSave = (patch) => {
  const key = gxSyncKey();
  if (!key) return Promise.reject(new Error("nokey"));
  const hdr = { Authorization: "Bearer " + key, Accept: "application/vnd.github+json" };
  const once = (again) => fetch(GX_AP_API + "?ref=main&t=" + Date.now(), { headers: hdr, cache: "no-store" })
    .then((r) => { if (r.status === 401 || r.status === 403) throw new Error("key"); if (!r.ok) throw new Error("read " + r.status); return r.json(); })
    .then((j) => {
      let cur = {};
      try { cur = JSON.parse(decodeURIComponent(escape(atob(String(j.content || "").replace(/\n/g, ""))))); } catch (e) {}
      const next = { ...cur, ...patch };
      return fetch(GX_AP_API, { method: "PUT", headers: { ...hdr, "Content-Type": "application/json" },
        body: JSON.stringify({ message: "Autopilot settings from the app", content: gxB64(JSON.stringify(next, null, 2) + "\n"), branch: "main", sha: j.sha }) })
        .then((r) => {
          if ((r.status === 409 || r.status === 422) && again) return once(false);
          if (!r.ok) throw new Error(r.status === 401 || r.status === 403 ? "key" : "save " + r.status);
          return next;
        });
    });
  return once(true).then((next) => fetch(GX_AP_RUN, { method: "POST", headers: { ...hdr, "Content-Type": "application/json" }, body: JSON.stringify({ ref: "main" }) })
    .then((r) => ({ next, ran: r.status === 204 })).catch(() => ({ next, ran: false })));
};
const GX_AP_AHEAD = [["0", "Today only"], ["1", "+1 day"], ["3", "+3 days"], ["week", "Rest of week"], ["7", "+7 days"]];
const gxApDayName = (d) => { try { return d === todayISO() ? "today" : fromIso(d).toLocaleDateString([], { weekday: "short", month: "short", day: "numeric" }); } catch (e) { return d || ""; } };
function GxAutoPage2({ s, go }) {
  const v = gxUseAp();
  const [cfg, setCfg] = useState(null);
  const [busy, setBusy] = useState(false);
  const [msg, setMsg] = useState("");
  const c = cfg || (v && v.c) || null;
  const m = c ? String(c.mode || "test").toLowerCase() : null, M = GX_AP_MODE[m] || null;
  const ahead = c ? String(c.days_ahead == null ? 0 : c.days_ahead) : "0";
  const has = !!gxSyncKey();
  const list = v && v.b ? [...(v.b.entries || [])].reverse().slice(0, 25) : [];
  const save = (patch, done) => {
    if (busy) return;
    setBusy(true); setMsg("Saving…");
    gxApSave(patch).then(({ next, ran }) => {
      setCfg(next); __gxAP = null;
      setMsg((done || "Saved.") + (ran ? " Running now; give it about 2 minutes." : " It takes effect at the next sync (every 6 to 30 minutes)."));
    }).catch((e) => setMsg(e && e.message === "key" ? "GitHub refused the key. It needs Contents: Read and write on this repo." : e && e.message === "nokey" ? "Turn on Sync between devices first." : "Could not reach GitHub. Try again."))
      .finally(() => setBusy(false));
  };
  const seg = (items, val, pick) => <span className="gx-seg">{items.map(([k, l]) => <button key={k} type="button" disabled={busy || !has} className={val === k ? "on" : ""} onClick={() => pick(k)}>{l}</button>)}</span>;
  const pickMode = (k) => {
    if (k === m) return;
    if (k === "on" && !window.confirm("Let the app change your real ESPN lineup by itself?")) return;
    save({ mode: k }, "Mode set to " + GX_AP_MODE[k][0] + ".");
  };
  return (
    <div className="space-y-3">
      <div className="font-semibold" style={{ fontSize: 17 }}>Lineup autopilot</div>
      <div className="gx-pn"><b></b><b></b><b></b><b></b>
        <div className="gx-sr" style={{ borderTop: 0 }}><span>Mode</span>{c ? seg([["off", "Off"], ["test", "Test"], ["on", "On"]], m, pickMode) : <span className="text-sm text-slate-500">{v ? "Starts after the next sync" : "Checking…"}</span>}</div>
        {M ? <div className="text-sm text-slate-500" style={{ padding: "2px 0 8px" }}>{M[2]}</div> : null}
        <div className="gx-sr"><span>Set lineups</span>{seg(GX_AP_AHEAD, ahead, (k) => save({ days_ahead: k === "week" ? "week" : +k }, "Lineups will be set " + ({ "0": "for today only.", "1": "for today and tomorrow.", "3": "for today and the next 3 days.", week: "through Sunday.", "7": "for today and the next 7 days." }[k] || ".")))}</div>
        <div className="text-xs text-slate-500" style={{ paddingTop: 6 }}>Days after today are set once. After that they only change on the day itself, when starting goalies are confirmed, or when you tap Redo.</div>
        <div className="gx-sr">
          <span>Upcoming days</span>
          <button type="button" className="border border-slate-300 rounded-lg px-3 py-1 text-sm" disabled={busy || !has || ahead === "0"} onClick={() => save({ redo_at: new Date().toISOString() }, "Upcoming days will be set again.")}>Redo upcoming days</button>
        </div>
        {msg ? <div className="text-xs" style={{ paddingTop: 6, color: /refused|Could not|first/.test(msg) ? "var(--bad)" : "var(--good)" }}>{msg}</div> : null}
        {!has ? <div className="text-xs text-slate-500" style={{ paddingTop: 8 }}>To change these here, turn on Sync between devices in Setup, Data and backup. Or <a className="text-blue-600" href={GX_AP_EDIT} target="_blank" rel="noopener">edit autopilot.json on GitHub</a>.</div> : null}
      </div>
      <div className="gx-pn"><b></b><b></b><b></b><b></b>
        <div className="gx-tag" style={{ marginBottom: 6 }}>What it does</div>
        <div className="text-sm" style={{ lineHeight: 1.6 }}>
          <div>{"• Every sync it works out the best lineup for today and for the days you chose."}</div>
          <div>{"• Starts players who have a game, benches players who don't, and swaps in the goalie who is actually starting."}</div>
          <div>{"• Never moves a player once his game has started, never touches IR, and only changes things when it adds at least " + ((c && c.min_gain) || 0.5) + " points."}</div>
          <div>{"• Sends a phone note every time, and shows it on Today."}</div>
        </div>
      </div>
      <GxPanel title="History" right={list.length ? "newest first" : ""}>
        {list.length ? list.map((e, i) => {
          const fail = String(e.result || "").indexOf("failed") === 0, test = e.mode !== "on";
          return (
            <div key={i} className="gx-row" style={{ display: "block", ...(i ? {} : { borderTop: 0 }) }}>
              <div className="text-xs text-slate-500">{"For " + gxApDayName(e.day) + " · " + gxApDay(e.at) + " " + gxApTime(e.at) + " · "}<span style={{ color: fail ? "var(--bad)" : test ? "var(--warn)" : "var(--good)" }}>{fail ? "ESPN refused" : test ? "test only" : "done"}</span>{e.gain ? " · +" + e.gain + " pts" : ""}</div>
              <div className="text-sm">{e.text}</div>
              {fail ? <div className="text-xs" style={{ color: "var(--bad)" }}>{String(e.result).replace(/^failed: /, "")}</div> : null}
            </div>
          );
        }) : <div className="text-sm text-slate-500">Nothing yet. The first suggestion shows up here when a lineup can be improved.</div>}
      </GxPanel>
    </div>
  );
}
'''

new_file("gm_autopilot.py", AUTOPILOT_PY)

def change(t):
    t = lit(t, "090: helpers", ROOT, HELPERS + ROOT, "change 090: autopilot controls")
    t = lit(t, "090: new autopilot page",
            'sub === "autopilot" ? <GxAutoPage {...P} /> :',
            'sub === "autopilot" ? <GxAutoPage2 {...P} /> :',
            '<GxAutoPage2 {...P} />')
    t = lit(t, "090: Today note says which day",
            '<div className="text-sm" style={{ marginTop: 2 }}>{(test && !fail ? "Would: " : "") + e.text + (e.gain ? " +" + e.gain + " points today." : "")}</div>',
            '<div className="text-sm" style={{ marginTop: 2 }}>{(e.day && e.day !== todayISO() ? "For " + gxApDayName(e.day) + ": " : "") + (test && !fail ? "Would: " : "") + e.text + (e.gain ? " +" + e.gain + " points." : "")}</div>{/* gx090-today */}',
            "{/* gx090-today */}")
    return t

edit(APP, change)
