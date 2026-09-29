#!/usr/bin/env python3
"""News clean-up, team logos and game times for Fantasy Islands GM.
Changes fantasy-gm.html only (same safe style as ui_refresh.py) and writes games-data.js.
Usage: python news_logos.py test | live | undo | games
"""
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import urllib.request
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

SRC, TEST, BAK = "fantasy-gm.html", "fantasy-gm-test.html", "fantasy-gm.backup-news.html"
GAMES = "games-data.js"
BABEL = "/tmp/babel/node_modules/@babel/standalone"
ALIAS = {"LAK": "LA", "NJD": "NJ", "SJS": "SJ", "TBL": "TB", "ARI": "UTA", "UTAH": "UTA"}
DONE = "function TeamLogo("
ROOT = 'ReactDOM.createRoot(document.getElementById("root")).render(<App />);'

GAMES_TAG = r'''<script>window.GAMES_DATA = null; document.write('<script src="games-data.js?t=' + Date.now() + '"><\/script>');</script>''' + "\n"

TAG_NEW = r'''{ const nw = newsOf(p)[0]; if (nw) out.push({ t: (nw.label ? nw.label + ": " : "") + (nw.h || "").slice(0, 60), c: NEWS_CLS[nw.kind] || "text-slate-500", u: nw.u }); }'''

TODAY_OLD = r'''const allNews = mine.map((p) => { const all = sigOf(p).news || []; return { p, all, items: all.filter((n) => nrm(n.h || "").includes(lastName(p.n))) }; });'''
TODAY_NEW = r'''const allNews = mine.map((p) => { const all = sigOf(p).news || []; return { p, all, items: newsOf(p) }; }).sort((a, b) => (a.items.length ? NEWS_RANK[a.items[0].kind] : 9) - (b.items.length ? NEWS_RANK[b.items[0].kind] : 9));'''

TODAY_ITEM_OLD = r'''{items.slice(0, 2).map((n, i) => <a key={i} href={n.u} target="_blank" rel="noreferrer" className={"block text-sm mt-0.5 hover:underline " + (n.tone === "-" ? "text-red-600" : "text-slate-600")}>{n.h}</a>)}'''
TODAY_ITEM_NEW = r'''{items.slice(0, 2).map((n, i) => <NewsItem key={i} n={n} />)}'''

HIDDEN_OLD = r'''{hidden} general headline{hidden === 1 ? "" : "s"} hidden (they don't mention the player)'''
HIDDEN_NEW = r'''{hidden} old or minor headline{hidden === 1 ? "" : "s"} hidden'''

TEAMNEWS_OLD = r'''const news = roster.filter((p) => (sigOf(p).news || []).length).slice(0, 6);'''
TEAMNEWS_NEW = r'''const news = roster.filter((p) => newsOf(p).length).slice(0, 6);'''

NEWSTAB_OLD = r'''else if (tab === "news") content = <div className="space-y-4"><PhoneFeed /><NewsView s={s} /></div>;'''
NEWSTAB_NEW = r'''else if (tab === "news") content = <div className="space-y-4"><NewsView s={s} wk={wk} /><PhoneFeed /></div>;'''

ODDS_OLD = r'''<td className="px-3 py-2 font-medium whitespace-nowrap">{v.opp} @ {home}</td>'''
ODDS_NEW = r'''<td className="px-3 py-2 font-medium whitespace-nowrap"><span className="inline-flex items-center gap-1.5"><TeamLogo t={v.opp} size={18} />{v.opp} @ <TeamLogo t={home} size={18} />{home}</span></td>'''

SCHED_OLD = r'''<td className="px-2 py-1 font-medium">{t}</td>'''
SCHED_NEW = r'''<td className="px-2 py-1 font-medium whitespace-nowrap"><span className="inline-flex items-center gap-1.5"><TeamLogo t={t} size={16} />{t}</span></td>'''

PO_OLD = r'''<td className="px-2 py-1.5 font-medium">{r.t}</td>'''
PO_NEW = r'''<td className="px-2 py-1.5 font-medium whitespace-nowrap"><span className="inline-flex items-center gap-1.5"><TeamLogo t={r.t} size={16} />{r.t}</span></td>'''

NEWSVIEW = r'''function NewsView({ s, wk }) {
  const [f, setF] = useState("all");
  const [open, setOpen] = useState({});
  const opp = wk ? oppOf(wk, s.me) : null;
  const pass = (n) => f === "all" || (f === "inj" ? NEWS_OUT.has(n.kind) : f === "moves" ? n.kind === "trade" || n.kind === "roster" : n.kind === "hot");
  const rows = s.players.map((p) => ({ p, items: newsOf(p).filter(pass) })).filter((x) => x.items.length)
    .sort((a, b) => NEWS_RANK[a.items[0].kind] - NEWS_RANK[b.items[0].kind] || a.items[0].age - b.items[0].age);
  const only = (list, keep) => list.map((x) => ({ ...x, items: x.items.filter(keep) })).filter((x) => x.items.length);
  const groups = [
    ["mine", "Your players", "Regular news shows for a day, hot streaks for 3 days, and injuries, scratches, trades and roster moves for a week.", rows.filter((x) => x.p.ft === s.me), true],
    ["opp", opp ? "Your opponent · " + teamName(s, opp) : "", "Everything current on the team you play this week.", opp ? rows.filter((x) => x.p.ft === opp) : [], false],
    ["league", "Around your league", "Other fantasy teams: important news and hot streaks only.", only(rows.filter((x) => x.p.ft !== s.me && x.p.ft !== opp && x.p.ft !== "fa"), (n) => n.kind !== "news"), false],
    ["fa", "Free agents", "Only important news: injuries, scratches, trades and roster moves.", only(rows.filter((x) => x.p.ft === "fa"), (n) => NEWS_BIG.has(n.kind)), false],
  ];
  return (
    <div className="space-y-4">
      <Pills items={[["all", "All"], ["inj", "Injuries & scratches"], ["moves", "Trades & roster moves"], ["hot", "Hot"]]} value={f} onChange={setF} />
      {!window.__SIG && <div className={box + " text-slate-400"}>No news loaded yet.</div>}
      {groups.filter((g) => g[4] || g[3].length).map(([k, title, sub, list]) => {
        const shown = open[k] ? list : list.slice(0, 8);
        return (
          <Section key={k} title={title + " (" + list.length + ")"} sub={sub}>
            {shown.length ? shown.map(({ p, items }) => (
              <div key={p.id} className="flex gap-3 py-2.5 border-t border-slate-100">
                <div className="pt-0.5"><TeamLogo t={p.t} size={22} /></div>
                <div className="min-w-0 flex-1">
                  <div className="flex flex-wrap items-baseline gap-2"><PN p={p} /><span className="text-xs text-slate-400">{p.p} · <TL s={s} id={p.ft} /></span></div>
                  {items.slice(0, 2).map((n, i) => <NewsItem key={i} n={n} />)}
                </div>
              </div>
            )) : <div className="text-slate-400 text-xs">Nothing current.</div>}
            {list.length > shown.length && <button className="text-sm text-blue-600 mt-2" onClick={() => setOpen({ ...open, [k]: true })}>Show all {list.length}</button>}
          </Section>
        );
      })}
    </div>
  );
}

'''

SIDE = r'''function Side({ l, s, id }) {
  return (
    <div className="p-3">
      <div className="flex justify-between font-semibold mb-1"><TL s={s} id={id} className="truncate" /><span>{f1(l.total)}</span></div>
      <table className="w-full text-sm"><tbody>
        {l.start.map((p) => {
          const g = gameOf(p.t, p.dt), o = oddsFor(p.t, p.dt);
          const gc = p.gs ? (p.gs.includes("confirmed") && !p.gs.includes("un") ? "text-green-700 font-semibold" : p.gs === "not starting" ? "text-red-600" : "text-amber-600") : "";
          return (
            <tr key={p.id} className="border-t border-slate-100">
              <td className="py-2 pr-2 text-xs text-slate-500 w-10 align-top">{p.slot}</td>
              <td className="py-2">
                <div className="flex items-center gap-2 min-w-0">
                  <TeamLogo t={p.t} size={20} />
                  <PN p={p} className="truncate" />
                  {!p.gs && p.prob < 1 ? <span className="text-xs text-slate-400">{Math.round(p.prob * 100)}%</span> : null}
                  {p.gs ? <span className={"text-xs " + gc}>{p.gs}</span> : null}
                </div>
                {g ? <div className="text-xs text-slate-500 mt-0.5" style={{ paddingLeft: 28 }}>{(g.h ? "vs " : "@") + g.o} · {gameTime(g)}</div> : null}
              </td>
              <td className="py-2 text-right whitespace-nowrap align-top">
                {o && window.__PMODE !== "espn" ? (p.p === "G"
                  ? <span className={"text-xs mr-2 " + (o.win >= 0.55 ? "text-green-700" : o.win <= 0.45 ? "text-red-600" : "text-slate-500")} title="Win chance from betting odds">W {Math.round(o.win * 100)}%</span>
                  : <span className={"text-xs mr-2 " + (o.gf >= 3.3 ? "text-green-700" : o.gf <= 2.7 ? "text-red-600" : "text-slate-400")} title="Team expected goals from betting odds">xG {o.gf.toFixed(1)}</span>) : null}
                {f1(p.x)}
              </td>
            </tr>
          );
        })}
        {l.start.length === 0 && <tr><td className="text-slate-400 py-1">No games</td></tr>}
      </tbody></table>
      {l.bench.length > 0 && <div className="text-xs text-red-600 mt-1">Would sit (no slot): {l.bench.map((p) => p.n).join(", ")}</div>}
      {l.empty > 0 && <div className="text-xs text-slate-500 mt-1">Empty slots: {l.empty}</div>}
    </div>
  );
}
'''

HELPERS = r'''// ---------- team logos, game times and news filter (news_logos.py) ----------
const NHL_LOGO = { LA: "LAK", NJ: "NJD", SJ: "SJS", TB: "TBL" };
function TeamLogo({ t, size }) {
  const [bad, setBad] = useState(false);
  if (!t) return null;
  const z = size || 16;
  if (bad) return <span>{t}</span>;
  return <img src={"https://assets.nhle.com/logos/nhl/svg/" + (NHL_LOGO[t] || t) + "_dark.svg"} alt={t} title={t} loading="lazy" onError={() => setBad(true)} style={{ width: z, height: z, objectFit: "contain", display: "inline-block", verticalAlign: "middle" }} />;
}
const gameOf = (t, dt) => { const G = (window.GAMES_DATA || {}).games || {}; return dt && G[dt] ? G[dt][t] || null : null; };
const gameTime = (g) => { const d = g && g.st ? new Date(g.st) : null; return d && !isNaN(d) ? d.toLocaleTimeString([], { hour: "numeric", minute: "2-digit" }) : "time TBD"; };
const NEWS_JUNK = /highlights|draft board|rankings|mailbag|podcast|give me a reason|league-winners|sleepers|\bbusts\b|best bets|predictions|betting|\bodds\b|takeaways|\bgrades\b|cheat sheet|start.?sit|waiver wire|what we learned/i;
const NEWS_KINDS = [
  ["trade", "Trade", /\btrade|traded|acquir|deal sends/i],
  ["scratch", "Scratched", /scratch/i],
  ["susp", "Suspended", /suspen/i],
  ["injury", "Injury", /injur|\bIR\b|surgery|day-to-day|week-to-week|month-to-month|out for|out indefinitely|will miss|expected to miss|sidelined|concussion|upper-body|lower-body|leaves game|left the game|ruled out|won't play|will not play|questionable|doubtful/i],
  ["roster", "Roster move", /waive|claimed|recall|reassign|sent down|assigned to|loaned|signs|signed|extension|contract|released|buyout|activated|returns|back in the lineup|cleared/i],
  ["hot", "Hot", /streak|hat trick|multi-point|career-high|promot|top line|top-line|first line|pp1|two goals|three points|four points|scores twice|milestone|\brecord\b/i],
];
const NEWS_DAYS = { trade: 7, scratch: 7, susp: 7, injury: 7, roster: 7, hot: 3, news: 1 };
const NEWS_RANK = { injury: 0, scratch: 0, susp: 0, trade: 1, roster: 2, hot: 3, news: 4 };
const NEWS_BIG = new Set(["trade", "scratch", "susp", "injury", "roster"]);
const NEWS_OUT = new Set(["injury", "scratch", "susp"]);
const NEWS_CLS = { injury: "text-red-600", scratch: "text-red-600", susp: "text-red-600", trade: "text-blue-600", roster: "text-blue-600", hot: "text-orange-600" };
const NEWS_BADGE = { injury: "bg-red-100 text-red-600", scratch: "bg-red-100 text-red-600", susp: "bg-red-100 text-red-600", trade: "bg-blue-50 text-blue-600", roster: "bg-slate-200 text-slate-600", hot: "bg-amber-100 text-orange-600" };
const newsAge = (d) => { if (!d) return 0; const a = Math.round((fromIso(todayISO()) - fromIso(String(d).slice(0, 10))) / 864e5); return isNaN(a) ? 0 : Math.max(0, a); };
const newsOf = (p) => {
  const last = nrm(p.n).split(" ").pop();
  return (sigOf(p).news || []).map((n) => {
    const h = n.h || "";
    if (!h || NEWS_JUNK.test(h) || !nrm(h).includes(last)) return null;
    const k = NEWS_KINDS.find((x) => x[2].test(h));
    const kind = k ? k[0] : "news", age = newsAge(n.d);
    return age < NEWS_DAYS[kind] ? { ...n, kind, label: k ? k[1] : "", age } : null;
  }).filter(Boolean).sort((a, b) => NEWS_RANK[a.kind] - NEWS_RANK[b.kind] || a.age - b.age);
};
const NewsItem = ({ n }) => (
  <div className="flex flex-wrap items-baseline gap-x-2 mt-1 text-sm">
    {n.label ? <span className={"text-xs px-1.5 py-0.5 rounded " + (NEWS_BADGE[n.kind] || "")}>{n.label}</span> : null}
    <a href={n.u} target="_blank" rel="noreferrer" className="hover:underline text-slate-700">{n.h}</a>
    <span className="text-xs text-slate-400">{n.age <= 0 ? "today" : n.age === 1 ? "yesterday" : n.age + " days ago"}</span>
  </div>
);

'''

TEAM_PAT = r"(?<!\$)\{([A-Za-z_][\w.]*)\.p\}( · | )\{\1\.t\}"


def fail(msg):
    print("STOPPED - nothing was changed: " + msg)
    sys.exit(1)


def sub_once(text, name, pat, rep, done=None, flags=0, count=1):
    if done and done in text:
        print(f"(news) {name}: already done")
        return text
    new, n = re.subn(pat, lambda m: rep, text, flags=flags)
    if n != count:
        fail(f"'{name}' matched {n} times (expected {count}). Send this log to the AI helper.")
    print(f"(news) {name}: updated")
    return new


def lit(text, name, old, new, done=None, count=1):
    return sub_once(text, name, re.escape(old), new, done, 0, count)


def block(text, name, start, end, rep, done):
    pat = re.escape(start) + r"\r?\n.*?(?=" + re.escape(end) + ")"
    return sub_once(text, name, pat, rep, done, re.S)


def logos(t):
    if "<TeamLogo t={p.t} />" in t:
        print("(news) logos next to players: already done")
        return t
    t, n = re.subn(TEAM_PAT, lambda m: "{%s.p}%s<TeamLogo t={%s.t} />" % (m.group(1), m.group(2), m.group(1)), t)
    if n < 15:
        fail(f"logos: only found {n} places (expected 15 or more). Send this log to the AI helper.")
    print(f"(news) logos next to players: {n} places")
    return t


def fix(t):
    t = logos(t)
    t = lit(t, "load game times", "<script>window.LINES_DATA = null;", GAMES_TAG + "<script>window.LINES_DATA = null;", "games-data.js")
    t = sub_once(t, "news tag next to players", r"if \(g\.news && g\.news\.length\) out\.push\(\{[^\n]*?u: g\.news\[0\]\.u \}\);", TAG_NEW, "newsOf(p)[0]")
    t = lit(t, "home: news on your players", TODAY_OLD, TODAY_NEW, "items: newsOf(p)")
    t = lit(t, "home: news headlines", TODAY_ITEM_OLD, TODAY_ITEM_NEW, "<NewsItem key={i} n={n} />")
    t = lit(t, "home: hidden count", HIDDEN_OLD, HIDDEN_NEW, "old or minor headline")
    t = lit(t, "team page news", TEAMNEWS_OLD, TEAMNEWS_NEW, "roster.filter((p) => newsOf(p).length)")
    t = lit(t, "news tab order", NEWSTAB_OLD, NEWSTAB_NEW, "<NewsView s={s} wk={wk} />")
    t = lit(t, "phone feed shorter", "const [show, setShow] = useState(12);", "const [show, setShow] = useState(5);", "const [show, setShow] = useState(5);")
    t = block(t, "news tab", "function NewsView({ s }) {", "// ---------- PP1 ----------", NEWSVIEW, "function NewsView({ s, wk })")
    t = block(t, "matchup rows (logo, opponent, time)", "function Side({ l, s, id }) {", "function MatchCard(", SIDE, "gameOf(p.t, p.dt)")
    t = lit(t, "betting lines logos", ODDS_OLD, ODDS_NEW, "<TeamLogo t={v.opp}")
    t = lit(t, "schedule logos", SCHED_OLD, SCHED_NEW, "<TeamLogo t={t} size={16} />")
    t = lit(t, "playoff schedule logos", PO_OLD, PO_NEW, "<TeamLogo t={r.t}")
    t = lit(t, "logo, game time and news helpers", ROOT, HELPERS + ROOT, DONE)
    # --- round 2: bigger logos, day totals and difference in Matchup ---
    t = sub_once(t, "bigger logos", r"const z = size \|\| \d+;", "const z = size || 28;", "const z = size || 28;")
    t = sub_once(t, "matchup: both sides same height",
                 r'<div className="p-3">(?=\r?\n[ \t]*<div className="flex justify-between font-semibold mb-1"><TL s=\{s\} id=\{id\})',
                 '<div className="p-3 flex flex-col h-full">', 'className="p-3 flex flex-col h-full"')
    t = lit(t, "matchup: projected total at the bottom",
            r'''{l.empty > 0 && <div className="text-xs text-slate-500 mt-1">Empty slots: {l.empty}</div>}''',
            r'''{l.empty > 0 && <div className="text-xs text-slate-500 mt-1">Empty slots: {l.empty}</div>}
      <div className="mt-auto pt-3"><div className="flex justify-between items-baseline border-t border-slate-200 pt-2"><span className="text-xs uppercase tracking-wide text-slate-500">Projected today</span><span className="font-semibold text-base">{f1(l.total)}</span></div></div>''',
            "Projected today")
    t = sub_once(t, "matchup: day difference",
                 re.escape("<Side l={x} s={s} id={a} /><Side l={y} s={s} id={b} />") + r"\r?\n[ \t]*</div>",
                 r'''<Side l={x} s={s} id={a} /><Side l={y} s={s} id={b} />
            </div>
            <div className="flex flex-wrap justify-between items-center gap-2 px-3 py-2.5 border-t border-slate-200 text-sm">
              <span className="text-xs uppercase tracking-wide text-slate-500">Day difference</span>
              <span className={"font-semibold " + (x.total - y.total >= 0 ? "text-green-700" : "text-red-600")}>{x.total - y.total >= 0 ? "+" : ""}{f1(x.total - y.total)} · {x.total === y.total ? "even" : teamName(s, x.total > y.total ? a : b) + " ahead"}</span>
            </div>''',
                 "Day difference")
    for must in (ROOT, "const SR = {", DONE, "function Side(", "function NewsView({ s, wk })", "function Matchup(", "function Today("):
        if must not in t:
            fail("fantasy-gm.html looks damaged after the changes (" + must + ").")
    return t


def jsx_check(html):
    m = re.search(r'<script type="text/babel">(.*?)</script>', html, re.S)
    if not m:
        fail("could not find the app code in fantasy-gm.html")
    if not shutil.which("node") or not os.path.exists(BABEL):
        print("(news) syntax check skipped (checker not installed) - test the page before going live")
        return
    pathlib.Path("/tmp/app.jsx").write_text(m.group(1), encoding="utf-8")
    js = ("const B=require(%r);const fs=require('fs');try{B.transform(fs.readFileSync('/tmp/app.jsx','utf8'),"
          "{presets:['react']});console.log('ok')}catch(e){console.log(e.message);process.exit(1)}") % BABEL
    r = subprocess.run(["node", "-e", js], capture_output=True, text=True)
    if r.returncode:
        fail("the new app code has a syntax error: " + (r.stdout or r.stderr)[:600])
    print("(news) app code syntax check: ok")


def ab(x):
    x = (x or "").upper()
    return ALIAS.get(x, x)


def games():
    start = datetime.now(ZoneInfo("America/New_York")).date() - timedelta(days=3)
    out, ok = {}, 0
    for k in range(6):
        d = (start + timedelta(days=7 * k)).isoformat()
        try:
            req = urllib.request.Request(f"https://api-web.nhle.com/v1/schedule/{d}", headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=30) as r:
                js = json.load(r)
            ok += 1
        except Exception as ex:
            print(f"(games) week of {d} failed: {type(ex).__name__}: {ex}")
            continue
        for day in js.get("gameWeek", []):
            for g in day.get("games", []):
                if g.get("gameType") != 2:
                    continue
                h, a = ab(g["homeTeam"]["abbrev"]), ab(g["awayTeam"]["abbrev"])
                st = g.get("startTimeUTC") or ""
                dd = out.setdefault(day["date"], {})
                dd[h] = {"o": a, "h": 1, "st": st}
                dd[a] = {"o": h, "h": 0, "st": st}
    n = sum(len(v) for v in out.values()) // 2
    if not n:
        fail(f"no games downloaded ({ok}/6 weeks reached the NHL). The old games-data.js is kept.")
    p = pathlib.Path(GAMES)
    if p.exists():
        try:
            old = json.loads(p.read_text(encoding="utf-8").split("=", 1)[1].strip().rstrip(";"))
            if old.get("games") == out:
                print(f"(games) {n} games, no changes since last time")
                return
        except Exception:
            pass
    data = {"generated": datetime.now(timezone.utc).isoformat(timespec="seconds"), "games": out}
    p.write_text("window.GAMES_DATA = " + json.dumps(data, separators=(",", ":")) + ";\n", encoding="utf-8")
    print(f"(games) wrote {GAMES}: {n} games over {len(out)} days")


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "test"
    if mode == "games":
        games()
        return
    if mode == "undo":
        b = pathlib.Path(BAK)
        if not b.exists():
            fail("no backup found - live mode has never been run.")
        pathlib.Path(SRC).write_text(b.read_text(encoding="utf-8"), encoding="utf-8")
        print(f"(news) restored {SRC} from {BAK}")
        return
    if mode not in ("test", "live"):
        fail("mode must be test, live, undo or games")
    p = pathlib.Path(SRC)
    if not p.exists():
        fail(f"{SRC} is missing from the repo")
    old = p.read_text(encoding="utf-8")
    new = fix(old)
    jsx_check(new)
    if mode == "test":
        pathlib.Path(TEST).write_text(new, encoding="utf-8")
        print(f"(news) test copy written - open {TEST} to check")
    else:
        if DONE not in old:
            pathlib.Path(BAK).write_text(old, encoding="utf-8")
            print(f"(news) backup saved: {BAK}")
        p.write_text(new, encoding="utf-8")
        print("(news) live app updated")


if __name__ == "__main__":
    main()
