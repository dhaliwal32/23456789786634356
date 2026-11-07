# changes/205-goal-power-play-on-ice.py - Goal Tracker says Power play / Shorthanded / Empty net, and shows who was on the ice as soon as NHL's shift data has the goal

import pathlib as _pl205

ONICE_PY = r'''"""gm_onice.py - change 205: who was on the ice for each goal of today's NHL games, from NHL's shift charts.

The app shows this under each goal in the Goal Tracker right away, without waiting for the goal's tracking file.
The browser cannot read NHL's feeds itself, so this runs on GitHub:
  - from gm_edge.py at the end of every sync, writing edge/onice.json
  - from gm_live.py every 30 seconds while games are live, writing edge/onice-live.json (committed only when a new goal is filled)
Each goal: d (game day), g, ev, per, t (time in period), tr (time left), team (scoring team), home, sc (situation code),
on = [[playerId, team, number, name, position], ...] for both teams at the moment of the goal. Keeps 3 days.
"""
import json, os, time
from datetime import datetime, timedelta, timezone
import requests

HERE = os.path.dirname(os.path.abspath(__file__))
UA = {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"}
NHL = dict(UA, Referer="https://www.nhl.com/", Origin="https://www.nhl.com")
AL = {"LAK": "LA", "NJD": "NJ", "SJS": "SJ", "TBL": "TB", "UTAH": "UTA", "ARI": "UTA"}
KEEP_DAYS = 3
SHIFT_GAP = 45  # seconds between shift chart reads for the same game


def ab(x):
    x = str(x or "").upper()
    return AL.get(x, x)


def sec(t):
    try:
        m, s = str(t or "0:0").split(":")[:2]
        return int(m) * 60 + int(s)
    except Exception:
        return -1


def getj(url, hdr=None):
    r = requests.get(url, headers=hdr or UA, timeout=20)
    r.raise_for_status()
    return r.json()


def on_ice(shifts, per, t, ro):
    """players whose shift covers the goal: started before it and ended at it or later. None if the shifts don't reach it yet."""
    T = sec(t)
    rows, last = {}, -1
    for s in shifts:
        if s.get("typeCode") != 517 or s.get("period") != per:
            continue
        a, b = sec(s.get("startTime")), sec(s.get("endTime"))
        if a < 0 or b < 0:
            continue
        last = max(last, b)
        if a < T <= b:
            pid = s.get("playerId")
            r = ro.get(str(pid)) or []
            nm = r[0] if r else ((s.get("firstName") or "") + " " + (s.get("lastName") or "")).strip()
            rows[pid] = [pid, r[3] if len(r) > 3 and r[3] else ab(s.get("teamAbbrev")), r[2] if len(r) > 2 else None, nm, r[1] if len(r) > 1 else ""]
    if last < T:
        return None
    on = list(rows.values())
    teams = {}
    for o in on:
        teams[o[1]] = teams.get(o[1], 0) + 1
    if len(teams) != 2 or min(teams.values()) < 3 or len(on) > 14:
        return None
    return on


def update(out="edge/onice.json", budget=25, live_only=False):
    """fills on-ice lists for today's goals; returns True when the file changed"""
    path = os.path.join(HERE, out)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    try:
        data = json.load(open(path))
    except Exception:
        data = {"goals": {}}
    G = data.setdefault("goals", {})
    seen = data.setdefault("shiftAt", {})
    t0, changed = time.time(), False
    try:
        now = getj("https://api-web.nhle.com/v1/score/now")
    except Exception as ex:
        print(f"(onice) score/now failed: {ex}")
        return False
    for g in now.get("games") or []:
        st = g.get("gameState")
        if not g.get("id") or st not in (("LIVE", "CRIT") if live_only else ("LIVE", "CRIT", "FINAL", "OFF")):
            continue
        if time.time() - t0 > budget:
            break
        gid, day = g["id"], g.get("gameDate") or ""
        n_goals = sum(int((g.get(x) or {}).get("score") or 0) for x in ("homeTeam", "awayTeam"))
        if n_goals and sum(1 for k, v in G.items() if v.get("g") == gid and v.get("on")) >= n_goals:
            continue  # every goal of this game already done
        try:
            pbp = getj(f"https://api-web.nhle.com/v1/gamecenter/{gid}/play-by-play")
        except Exception as ex:
            print(f"(onice) play-by-play {gid} failed: {ex}")
            continue
        tid = {}
        for side in ("homeTeam", "awayTeam"):
            T = pbp.get(side) or {}
            tid[T.get("id")] = ab(T.get("abbrev"))
        home = tid.get((pbp.get("homeTeam") or {}).get("id"), "")
        ro = {}
        for r in pbp.get("rosterSpots") or []:
            nm = (((r.get("firstName") or {}).get("default") or "") + " " + ((r.get("lastName") or {}).get("default") or "")).strip()
            ro[str(r.get("playerId"))] = [nm, r.get("positionCode") or "", r.get("sweaterNumber"), tid.get(r.get("teamId"), "")]
        todo = []
        for p in pbp.get("plays") or []:
            pd = p.get("periodDescriptor") or {}
            if p.get("typeDescKey") != "goal" or pd.get("periodType") == "SO":
                continue
            key = f"{gid}-{p.get('eventId')}"
            if (G.get(key) or {}).get("on"):
                continue
            d = p.get("details") or {}
            todo.append((key, {"d": day, "g": gid, "ev": p.get("eventId"), "per": pd.get("number"), "t": p.get("timeInPeriod"),
                               "tr": p.get("timeRemaining"), "team": tid.get(d.get("eventOwnerTeamId"), ""), "sc": p.get("situationCode"),
                               "home": home, "scorer": d.get("scoringPlayerId")}))
        if not todo or time.time() - seen.get(str(gid), 0) < SHIFT_GAP:
            continue
        seen[str(gid)] = time.time()
        try:
            shifts = (getj(f"https://api.nhle.com/stats/rest/en/shiftcharts?cayenneExp=gameId={gid}", NHL) or {}).get("data") or []
        except Exception as ex:
            print(f"(onice) shift chart {gid} failed: {ex}")
            continue
        for key, ent in todo:
            on = on_ice(shifts, ent["per"], ent["t"], ro)
            if on:
                ent["on"], ent["ok"], ent["at"] = on, True, time.time()
                G[key] = ent
                changed = True
    cut = (datetime.now(timezone.utc) - timedelta(days=KEEP_DAYS)).strftime("%Y-%m-%d")
    for k in [k for k, v in G.items() if (v.get("d") or "") < cut]:
        G.pop(k, None)
        changed = True
    for k in [k for k, v in seen.items() if time.time() - v > 86400]:
        seen.pop(k, None)
    if changed or not os.path.exists(path):
        data["updated"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        with open(path, "w") as f:
            json.dump(data, f, separators=(",", ":"))
    print(f"(onice) {sum(1 for v in G.values() if v.get('on'))} goal(s) with players on the ice" + (" (new)" if changed else ""))
    return changed


if __name__ == "__main__":
    update()
'''

NEW_CSS = r'''  /* change 205 (install.py) */
  .gx-pp205 { display: inline-block; margin-left: 6px; padding: 1px 6px; border-radius: 4px; font-size: 11px; font-weight: 700; line-height: 16px; vertical-align: 1px; white-space: nowrap; background: var(--warn); color: #111111; }
  .gx-pp205.sh, .gx-pp205.en { background: none; color: var(--mute); box-shadow: inset 0 0 0 1px var(--line2, var(--line)); }
  .gx-sc141 .gr small .gx-pp205 { font-size: 10px; }
  .ol205 { padding: 4px 12px 12px; animation: gx173in .25s ease; }
  .gx-sd141 .ol205 { padding: 10px 2px 0; }
  .gx-sc141 .ol205 { margin: -4px 16px 12px 72px; padding: 0; max-width: 560px; }
  .ol205 .hd205 { color: var(--mute); font-size: 12px; margin-bottom: 6px; }
  .ol205 .tg205 { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); gap: 4px 14px; }
  .ol205 .tn205 { font-weight: 700; font-size: 13px; color: var(--ink); margin-bottom: 2px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .ol205 .pl205 { display: grid; grid-template-columns: 32px minmax(0, 1fr) 24px; align-items: center; height: 22px; font-size: 13px; font-weight: 400; line-height: 22px; color: var(--ink); }
  .ol205 .pl205 .no205 { color: var(--mute); font-variant-numeric: tabular-nums; }
  .ol205 .pl205 .nm205 { min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  .ol205 .pl205 .nm205 button { color: inherit; font: inherit; }
  .ol205 .pl205 .nm205 .t205 { color: var(--mute); }
  .ol205 .pl205 .pm205 { text-align: right; font-weight: 600; font-variant-numeric: tabular-nums; color: var(--mute); }
  .ol205 .em205 { color: var(--mute); font-size: 13px; }
  .gx-sc141 .gv173 + .gv173.oi205 { margin-top: -2px; }
  .gx-gt141 .ph { position: relative; }
  .gx-gt141 .ph .gx-pp205 { position: absolute; right: 1px; bottom: 2px; margin: 0; padding: 0 4px; font-size: 10px; line-height: 15px; }
  .gx-gt141 .ph .gx-pp205.sh, .gx-gt141 .ph .gx-pp205.en { background: var(--card, #1c1d21); color: var(--ink); }
  @media (max-width: 640px) { .gx-sc141 .ol205 { margin-left: 72px; margin-right: 12px; } }
  @media (prefers-reduced-motion: reduce) { .ol205 { animation: none; } }
</style>'''

HELPERS = r'''// ---------- change 205: power play tag and players on the ice for each goal (install.py) ----------
function GxStr205({ x, short }) {
  const k = (x || {}).strength;
  if (!k) return null;
  return <span title={k === "PP" ? "Power play goal" : k === "SH" ? "Shorthanded goal" : "Empty net goal"} className={"gx-pp205 " + k.toLowerCase()} data-gx="205">{short ? k : k === "PP" ? "Power play" : k === "SH" ? "Shorthanded" : "Empty net"}</span>;
}
const E205 = { at: 0, busy: false, m: {} };
function gxOiLoad205() {
  if (E205.busy || Date.now() - E205.at < 25000) return;
  E205.busy = true;
  const one = (f) => fetch("edge/" + f + "?t=" + Date.now()).then((r) => (r.ok ? r.json() : null)).catch(() => null);
  Promise.all([one("onice.json"), one("onice-live.json")]).then((js) => {
    E205.busy = false; E205.at = Date.now();
    const m = {};
    js.forEach((j) => Object.entries((j && j.goals) || {}).forEach(([k, v]) => { if (v && v.on && v.on.length && !m[k]) m[k] = v; }));
    E205.m = m; window.dispatchEvent(new Event("gx-oi205"));
  });
}
function gxOiFind205(x, g, tm) {
  if (!x) return null;
  const per = (x.periodDescriptor || {}).number || 1, s0 = gxSec165(x.timeInPeriod), day = (g || {}).gameDate;
  let best = null;
  Object.values(E205.m).forEach((v) => {
    if (v.team !== tm || v.per !== per || (day && v.d && v.d !== day)) return;
    const d = Math.min(Math.abs(gxSec165(v.t) - s0), Math.abs(gxSec165(v.tr) - s0));
    if (d <= 3 && (!best || d < best.d)) best = { v, d };
  });
  return best ? best.v : null;
}
// plus/minus counts unless the scoring team had more skaters (situation code: away goalie, away skaters, home skaters, home goalie)
function gxPmOk205(code, scT, home) {
  const c = String(code || "");
  if (c.length !== 4) return false;
  const hs = home === scT, mine = +(hs ? c[2] : c[1]), them = +(hs ? c[1] : c[2]);
  return !(mine > them);
}
function GxOiList205({ x, g, tm, s }) {
  const v = gxOiFind205(x, g, tm);
  const e = useEdge165(v ? null : x, g, tm);
  let rows = [], home = "", code = "";
  if (v) {
    rows = v.on.map((o) => ({ id: o[0], t: o[1], no: o[2], n: o[3] || "", gl: o[4] === "G" }));
    home = v.home; code = v.sc;
  } else if (e) {
    const F = e.F || {}, fr = F.f || [], n = fr.length, gi = Math.max(0, Math.min(F.gi == null ? n - 1 : F.gi, n - 1)), ro = F.ro || {};
    rows = ((fr[gi] || [0, []])[1] || []).filter((o) => o[0]).map((o) => { const r = ro[o[0]] || []; return { id: o[0], t: o[1], no: o[2], n: r[0] || "", gl: r[1] === "G" }; });
    home = F.home; code = F.sc;
  }
  if (!rows.length) return <div className="em205">Loading...</div>;
  const pm = gxPmOk205(code, tm, home);
  const teams = [tm].concat([...new Set(rows.map((r) => r.t))].filter((t) => t !== tm)).filter((t) => rows.some((r) => r.t === t));
  return (
    <>
      <div className="hd205">{"On the ice at the goal" + (pm ? "" : " (power play goal, no plus/minus)")}</div>
      <div className="tg205">
        {teams.map((t) => (
          <div key={t} className="min-w-0"><div className="tn205">{t + (t === tm ? " (scored)" : "")}</div>
            {rows.filter((r) => r.t === t).sort((a, b) => (a.gl ? 1 : 0) - (b.gl ? 1 : 0) || (+a.no || 0) - (+b.no || 0)).map((r) => {
              const p = gxFind131(t, r.no, r.n), tag = gxTag131(s, p), nm = r.n ? shortN(r.n) : "#" + r.no;
              return <div key={r.id} className="pl205"><span className="no205">{r.no != null ? "#" + r.no : ""}</span><span className="nm205">{p && window.__NAV ? <button type="button" className="hover:underline" onClick={(ev) => { ev.stopPropagation(); window.__NAV.player(p); }}>{nm}</button> : nm}{tag ? <span className="t205">{" (" + tag + ")"}</span> : null}</span><span className="pm205">{r.gl ? "G" : pm ? (t === tm ? "+1" : "-1") : ""}</span></div>;
            })}
          </div>
        ))}
      </div>
    </>
  );
}
function GxOi205({ x, g, tm, s, cls }) {
  const [, tk] = useState(0);
  const [on, setOn] = useState(false);
  useEffect(() => {
    const f = () => tk((n) => n + 1);
    window.addEventListener("gx-oi205", f); window.addEventListener("gx-edge165", f);
    gxOiLoad205(); gxEdgeLoad165();
    const id = setInterval(() => { gxOiLoad205(); gxEdgeLoad165(); }, 30000);
    return () => { window.removeEventListener("gx-oi205", f); window.removeEventListener("gx-edge165", f); clearInterval(id); };
  }, []);
  if (!x || !(gxOiFind205(x, g, tm) || gxEdgeFind165(x, g, tm))) return null;
  return (
    <>
      <button type="button" className={cls + " oi205"} onClick={(e) => { e.stopPropagation(); setOn(!on); }}>On ice <i className={on ? "up" : ""}>{"\u25be"}</i></button>
      {on ? <div className="ol205" onClick={(e) => e.stopPropagation()}><GxOiList205 x={x} g={g} tm={tm} s={s} /></div> : null}
    </>
  );
}
'''


def change(t):
    t = lit(t, "205: styles", "</style>", NEW_CSS, "change 205 (install.py)")
    t = lit(t, "205: helpers", ROOT, HELPERS + ROOT, "change 205: power play tag and players")
    t = lit(t, "205: empty net goals",
            'strength: st.indexOf("power") >= 0 ? "PP" : st.indexOf("short") >= 0 ? "SH" : "",',
            'strength: st.indexOf("power") >= 0 ? "PP" : st.indexOf("short") >= 0 ? "SH" : st.indexOf("empty") >= 0 ? "EN" : "",',
            'st.indexOf("empty") >= 0 ? "EN"')
    # laptop Goal Tracker
    t = lit(t, "205: laptop tag",
            '<div className="sm">{(r.x.timeInPeriod || "") + " - " + gxPer131(r.x.periodDescriptor)}</div>',
            '<div className="sm">{(r.x.timeInPeriod || "") + " - " + gxPer131(r.x.periodDescriptor)}<GxStr205 x={r.x} /></div>',
            'gxPer131(r.x.periodDescriptor)}<GxStr205 x={r.x} /></div>')
    t = lit(t, "205: laptop on ice",
            '<GxRink163 x={r.x} g={r.g} tm={r.tm} s={s} /></GxGvModal169> : null}</>; })() : null}',
            '<GxRink163 x={r.x} g={r.g} tm={r.tm} s={s} /></GxGvModal169> : null}</>; })() : null}<GxOi205 x={r.x} g={r.g} tm={r.tm} s={s} cls="gv167" />',
            '<GxOi205 x={r.x} g={r.g} tm={r.tm} s={s} cls="gv167" />')
    # phone Goal Tracker
    t = lit(t, "205: phone tag",
            'e.currentTarget.style.visibility = "hidden"; }} /> : <TeamLogo t={r.tm} size={34} />}</span>',
            'e.currentTarget.style.visibility = "hidden"; }} /> : <TeamLogo t={r.tm} size={34} />}<GxStr205 x={r.x} short /></span>',
            '<GxStr205 x={r.x} short /></span>')
    t = lit(t, "205: phone on ice",
            '<div className="gvb163"><GxRink163 x={r.x} g={r.g} tm={r.tm} s={s} /></div> : null}</>; })() : null}',
            '<div className="gvb163"><GxRink163 x={r.x} g={r.g} tm={r.tm} s={s} /></div> : null}</>; })() : null}<GxOi205 x={r.x} g={r.g} tm={r.tm} s={s} cls="gv163" />',
            '<GxOi205 x={r.x} g={r.g} tm={r.tm} s={s} cls="gv163" />')
    # game view, GAME tab
    t = lit(t, "205: game tab tag",
            '<small>{r.x.timeInPeriod}</small>Goal:',
            '<small>{r.x.timeInPeriod}<GxStr205 x={r.x} /></small>Goal:',
            '<small>{r.x.timeInPeriod}<GxStr205 x={r.x} /></small>')
    t = lit(t, "205: game tab on ice",
            '<div className="gvb173"><GxRink163 x={r.x} g={r.g} tm={r.tm} s={s} /></div> : null}</>; })() : null}',
            '<div className="gvb173"><GxRink163 x={r.x} g={r.g} tm={r.tm} s={s} /></div> : null}</>; })() : null}<GxOi205 x={r.x} g={r.g} tm={r.tm} s={s} cls="gv173" />',
            '<GxOi205 x={r.x} g={r.g} tm={r.tm} s={s} cls="gv173" />')
    return t


edit(APP, change)

# new script: on-ice lists from NHL shift charts
new_file("gm_onice.py", ONICE_PY)


def edge205(t):
    return lit(t, "205: on ice after each sync",
               '    print(f"(edge) {new} new goal replay(s), {sum(1 for v in G.values() if v.get(\'ok\'))} saved")\n',
               '    print(f"(edge) {new} new goal replay(s), {sum(1 for v in G.values() if v.get(\'ok\'))} saved")\n'
               '    try:  # change 205: who was on the ice for every goal, from shift charts\n'
               '        import gm_onice\n'
               '        gm_onice.update("edge/onice.json", 25)\n'
               '    except Exception as ex:\n'
               '        print(f"(onice) WARNING: {ex}")\n',
               "change 205: who was on the ice")


edit("gm_edge.py", edge205)

LIVE_FN = r'''

def push_onice():
    """change 205: fill who was on the ice for new goals and commit it, so the app shows it within a minute or two"""
    try:
        import subprocess
        import gm_onice
        if not gm_onice.update("edge/onice-live.json", 20, live_only=True):
            return
        run = lambda *a: subprocess.run(["git", *a], cwd=HERE, capture_output=True, text=True)
        run("config", "user.name", "fantasy-bot")
        run("config", "user.email", "fantasy-bot@users.noreply.github.com")
        run("add", "edge/onice-live.json")
        if run("diff", "--cached", "--quiet").returncode == 0:
            return
        run("commit", "-q", "-m", "on ice " + datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ"))
        for _ in range(4):
            if run("pull", "-q", "--rebase", "-X", "theirs").returncode == 0 and run("push", "-q").returncode == 0:
                log("on ice saved")
                return
            run("rebase", "--abort")
            time.sleep(5)
        log("on ice: push failed (does live-alerts.yml have contents: write?)")
        run("reset", "-q", "--hard", "origin/main")
    except Exception as e:
        log("on ice failed", e)


def main():'''


def live205(t):
    t = lit(t, "205: live on ice function", "\n\ndef main():", LIVE_FN, "change 205: fill who was on the ice")
    t = lit(t, "205: live on ice call",
            "            elif side != 0:\n                last = side\n        time.sleep(EVERY)",
            "            elif side != 0:\n                last = side\n        push_onice()  # change 205\n        time.sleep(EVERY)",
            "push_onice()  # change 205")
    return t


edit("gm_live.py", live205)
