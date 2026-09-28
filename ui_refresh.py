#!/usr/bin/env python3
"""UI refresh installer for Fantasy Islands GM.
Changes fantasy-gm.html, lines-tab.js and ask-panel.js: new home screen,
Lines tab in the new theme, no emojis.
Usage: python ui_refresh.py test | live | undo
"""
import pathlib
import re
import sys

FILES = {
    "fantasy-gm.html": ("fantasy-gm-test.html", "fantasy-gm.backup-ui.html"),
    "lines-tab.js": ("lines-tab-test.js", "lines-tab.backup-ui.js"),
    "ask-panel.js": ("ask-panel-test.js", "ask-panel.backup-ui.js"),
}
VS = "\ufe0f?"   # optional emoji variation selector
DOT = "\u25cf"   # small filled circle
STRIP = ("\U0001F3E0\u2694\U0001F501\U0001F3C6\U0001F3D2\U0001F465\u2699\U0001F9EA"
         "\U0001F4CA\U0001F945\U0001F3B2\U0001F525\u2744\u23F1\U0001F4C8\U0001F4F0"
         "\u26D4\u26A0\u2705\u26AA\U0001F4AC\U0001F511\U0001F4E3\U0001F50E")
ARROWS = [("\u2b06" + VS, "\u2191"), ("\u2b07" + VS, "\u2193")]

SCORE_CSS = "  .text-4xl { font-weight: 500 !important; font-size: 2.75rem !important; line-height: 1.1; margin-top: .4rem; margin-bottom: .2rem; letter-spacing: -0.03em; font-variant-numeric: tabular-nums; }"

SETTINGS_DOT = '<span className={ok ? "text-green-700" : "text-slate-400"}>' + DOT + "</span>"

TODAY = r'''// ---------- Today ----------
function Today({ s, wk, go }) {
  const K = s.blend;
  const opp = oppOf(wk, s.me) || s.opp;
  const done = wk.done || 0;
  const mine = s.players.filter((p) => p.ft === s.me), theirs = s.players.filter((p) => p.ft === opp);
  const A = weekProj(mine, wk, K, done), B = weekProj(theirs, wk, K, done);
  const aA = +((wk.act || {})[s.me]) || 0, aB = +((wk.act || {})[opp]) || 0;
  const fa = aA + A.total, fb = aB + B.total, margin = fa - fb;
  const today = todayISO();
  const dates = wk.dates || [];
  const di = dates.findIndex((d) => d >= today);
  const dday = di >= 0 ? dates[di] : null;
  const L = di >= 0 ? dayLineup(mine, wk, di, K) : null, OL = di >= 0 ? dayLineup(theirs, wk, di, K) : null;
  const checks = [];
  if (L) {
    mine.forEach((p) => { if (!p.ir && (wk.games[p.t] || []).includes(di) && avail(p, dday) === 0) checks.push(["bad", `${p.n} (${p.t}) is out — keep him out of your lineup`]); });
    mine.filter((p) => p.p === "G" && !p.ir && (wk.games[p.t] || []).includes(di)).forEach((p) => {
      const g = gStart(p, dday);
      if (g.l === "not starting") checks.push(["bad", `${p.n} is not starting — use another goalie`]);
      else if (g.l === "✓ confirmed") checks.push(["good", `${p.n} confirmed starting`]);
      else checks.push(["warn", `${p.n}: ${g.l || "starter not announced yet"} — check before lock`]);
    });
    if (L.bench.length) checks.push(["warn", `More players than slots — ${L.bench.map((p) => p.n).join(", ")} would sit`]);
    if (L.empty > 0) checks.push(["warn", `${L.empty} empty slot${L.empty > 1 ? "s" : ""} — a streamer could fill ${L.empty > 1 ? "them" : "it"}`]);
  }
  const outNow = mine.filter((p) => { const b = effBack(p).d; return (b && b > today) || (!b && avail(p, today) === 0); });
  const moves = useMemo(() => computeMoves(s, { H: 1, pool: 40 }).res.filter((r) => r.gain >= (s.minGain ?? 3)).slice(0, 3), [s]);
  const sameDrop = moves.length > 1 && moves.every((r) => r.d.id === moves[0].d.id);
  const trend = s.players.filter((p) => p.ft === "fa" && p.prob > 0 && ((formRatio(p, K) || 0) >= 1.25 || (p.chg || 0) >= 5)).sort((a, b) => (b.chg || 0) - (a.chg || 0)).slice(0, 2);
  const lastName = (n) => nrm(n).split(" ").pop();
  const allNews = mine.map((p) => { const all = sigOf(p).news || []; return { p, all, items: all.filter((n) => nrm(n.h || "").includes(lastName(p.n))) }; });
  const news = allNews.filter((x) => x.items.length).slice(0, 5);
  const hidden = allNews.reduce((a, x) => a + x.all.length - x.items.length, 0);
  const pct = Math.max(6, Math.min(94, 50 + margin / 2));
  const dot = { bad: "text-red-600", warn: "text-amber-600", good: "text-green-700" };
  const daysLeft = dates.length - done;
  const Row = ({ children }) => <div className="flex items-center gap-3 py-2.5 border-t border-slate-100">{children}</div>;
  return (
    <div className="space-y-4">
      <div className="bg-white rounded-xl border border-slate-200 p-4">
        <div className="flex flex-wrap items-center gap-2 text-xs text-slate-500">
          <span className="uppercase tracking-wide">{wk.label}</span><span>·</span><span>{done >= dates.length ? "Final" : `${daysLeft} day${daysLeft === 1 ? "" : "s"} left`}</span>
          <button className="ml-auto text-blue-600" onClick={() => go("matchup")}>Full matchup →</button>
        </div>
        <div className="grid grid-cols-[1fr_auto_1fr] gap-4 items-end mt-4">
          <div className="min-w-0"><div className="text-xs uppercase tracking-wide text-slate-500 truncate">{teamName(s, s.me)}</div><div className="text-4xl">{f1(fa)}</div><div className="text-xs text-slate-500">{f1(aA)} actual + {f1(A.total)} proj</div></div>
          <div className="text-sm text-slate-400 pb-7">vs</div>
          <div className="min-w-0 text-right"><div className="text-xs uppercase tracking-wide text-slate-500 truncate">{teamName(s, opp)}</div><div className="text-4xl">{f1(fb)}</div><div className="text-xs text-slate-500">{f1(aB)} actual + {f1(B.total)} proj</div></div>
        </div>
        <div className="h-1.5 rounded-full bg-slate-200 mt-5 overflow-hidden"><div className={"h-full rounded-full " + (margin >= 0 ? "bg-green-500" : "bg-red-500")} style={{ width: pct + "%" }}></div></div>
        <div className="flex flex-wrap items-baseline gap-2 mt-3 text-sm"><span className={"font-semibold " + (margin >= 0 ? "text-green-700" : "text-red-600")}>{margin >= 0 ? "Ahead" : "Behind"} by {f1(Math.abs(margin))}</span><span className="text-slate-500">projected{Math.abs(margin) < 15 ? " · close, every move matters" : ""}</span></div>
      </div>
      <div className="grid md:grid-cols-2 gap-4">
        <Section title={dday ? (dday === today ? "Tonight" : `Next game day · ${dayLabel(dday)}`) : "No games left this week"} sub={L ? `${L.start.length} of your players play · projected ${f1(L.total)} vs ${f1(OL.total)}` : ""} link={["Matchup", () => go("matchup")]}>
          {checks.length ? checks.map(([k, t], i) => <Row key={i}><span className={dot[k]}>●</span><span className="text-slate-700">{t}</span></Row>) : <div className="text-green-700">Lineup looks good.</div>}
        </Section>
        <Section title="Best moves this week" sub={sameDrop ? `All free up ${moves[0].d.n}'s spot` : ""} link={["All moves", () => go("moves", "adddrop")]}>
          {moves.length ? moves.map((r) => { const sd = effAvg(r.f, K) - effAvg(r.d, K); const [v, c] = verdict(r.gain, sd); return (
            <Row key={r.f.id}><span className={"text-xs px-2 py-0.5 rounded whitespace-nowrap " + c}>{v}</span><span className="flex-1">Add <b>{r.f.n}</b> <span className="text-xs text-slate-400">{r.f.p} · {r.f.t}</span>{sameDrop ? null : <> · drop <b>{r.d.n}</b></>}</span><span className="text-green-700 font-semibold">+{f1(r.gain)}</span></Row>
          ); }) : <div className="text-slate-400">No move worth an acquisition right now.</div>}
        </Section>
      </div>
      {window.LinesSummary ? <window.LinesSummary s={s} wk={wk} go={go} trend={trend} H={{ Section, teamName, f1 }} /> : null}
      <div className="grid md:grid-cols-2 gap-4">
        <Section title="Injuries" link={["Manage", () => go("setup", "inj")]}>
          {outNow.length ? outNow.map((p) => { const b = effBack(p); const soon = b.d && dates.length && b.d <= dates[dates.length - 1]; return (
            <Row key={p.id}><span className="font-medium">{p.n}</span><span className="text-xs text-slate-400">{p.p} · {p.t}{p.ir ? " · IR" : ""}</span><span className={"ml-auto text-xs " + (soon ? "text-green-700 font-semibold" : "text-slate-500")}>{b.d ? "Back " + mdL(b.d) : "No return date"}</span></Row>
          ); }) : <div className="text-green-700">Everyone healthy.</div>}
        </Section>
        <Section title="News on your players" link={["All news", () => go("league", "news")]}>
          {news.length ? news.map(({ p, items }) => (
            <div key={p.id} className="py-2.5 border-t border-slate-100">
              <div><span className="font-medium">{p.n}</span> <span className="text-xs text-slate-400">{p.p} · {p.t}</span></div>
              {items.slice(0, 2).map((n, i) => <a key={i} href={n.u} target="_blank" rel="noreferrer" className={"block text-sm mt-0.5 hover:underline " + (n.tone === "-" ? "text-red-600" : "text-slate-600")}>{n.h}</a>)}
            </div>
          )) : <div className="text-slate-400">No headlines about your players right now.</div>}
          {hidden > 0 && <div className="text-xs text-slate-400 mt-2">{hidden} general headline{hidden === 1 ? "" : "s"} hidden (they don't mention the player)</div>}
        </Section>
      </div>
    </div>
  );
}

'''

SUMMARY = r'''  // ---------- compact summary for the Today screen ----------
  function LinesSummary({ s, wk, go, trend, H }) {
    const L = window.LINES_DATA;
    const pr = (wk.pairs || []).find((x) => x[0] && x[1] && (x[0] === s.me || x[1] === s.me));
    const opp = pr ? (pr[0] === s.me ? pr[1] : pr[0]) : s.opp;
    const ctx = useMemo(() => build(s, L), [s.players, L && L.generated]);
    const items = useMemo(() => enrich(L, ctx, s, opp), [ctx, opp, L && L.generated]);
    if (!L) return null;
    const imp = items.filter((x) => x.s >= TH);
    const mine = imp.filter((x) => x.ok === "me" || (x.ok !== "fa" && x.mates.length > 0)).slice(0, 4);
    const tr = (trend || []).slice(0, 2);
    const fa = imp.filter((x) => x.ok === "fa").slice(0, Math.max(2, 4 - tr.length));
    const open = () => go("lines");
    const head = (t) => <div className="text-xs uppercase tracking-wide text-slate-400 mb-1">{t}</div>;
    return (
      <H.Section title="Line changes" sub={`Checked ${ago(L.lines_at)} · ${imp.length} of ${items.length} changes matter to you`} link={["Open Lines", open]}>
        <div className="grid md:grid-cols-2 gap-x-8 gap-y-4">
          <div>
            {head("Your team")}
            {mine.length ? mine.map((x) => <Row key={x.c.id} x={x} s={s} H={H} onPick={open} />) : <div className="lt-msg">No changes for your players.</div>}
          </div>
          <div>
            {head("Pickup targets")}
            {fa.map((x) => <Row key={x.c.id} x={x} s={s} H={H} onPick={open} />)}
            {tr.map((p) => (
              <div key={p.id} className="lt-it" onClick={() => go("moves", "adddrop")}>
                <span className="lt-ic lt-up">↗</span>
                <div style={{ minWidth: 0 }}>
                  <div className="text-sm"><b>{p.n}</b> <span className="lt-tm">{p.t} · {p.p}</span> trending</div>
                  <div className="lt-why">{(p.chg || 0) >= 5 ? `+${H.f1(p.chg)}% rostered this week` : "Hot over the last 14 days"}</div>
                </div>
                <span className="lt-own fa">FA</span>
              </div>
            ))}
            {!fa.length && !tr.length && <div className="lt-msg">No free agents moving up right now.</div>}
          </div>
        </div>
        <div className="lt-bar"><span>{items.length - imp.length} minor changes hidden</span><button className="lt-link" style={{ padding: 0 }} onClick={open}>See all {items.length} in Lines →</button></div>
      </H.Section>
    );
  }

  window.LinesSummary = LinesSummary;
  window.LinesTab = LinesTab;'''

COLORS = [
    ("#1a2438", "#292929"), ("#22304a", "#292929"), ("#0e1628", "#161616"), ("#3b4b6b", "#4a4a4a"),
    ("#15203a", "#1f1f1f"), ("#e6edf7", "#fafafa"), ("#cbd5e1", "#d4d4d4"), ("#2c3b58", "#363636"),
    ("#c9d6e8", "#bdbdbd"), ("#1c2a44", "#202020"), ("#111a2e", "#1a1a1a"), ("#56627a", "#4d4d4d"),
    ("#c4a7ff", "#8b7cff"), ("#60a5fa", "#8b7cff"), ("#4ade80", "#5fd08a"), ("#f87171", "#f06a6a"),
    ("#8b98ad", "#8f8f8f"), ("rgba(96,165,250,", "rgba(139,124,255,"),
]


def fail(msg):
    print("STOPPED - nothing was changed: " + msg)
    sys.exit(1)


def sub_once(text, name, pat, rep, done=None, flags=0):
    if done and done in text:
        print(f"(ui) {name}: already done")
        return text
    new, n = re.subn(pat, lambda m: rep, text, flags=flags)
    if n != 1:
        fail(f"'{name}' matched {n} times (expected exactly 1). Send this log to the AI helper.")
    print(f"(ui) {name}: updated")
    return new


def common(text):
    for pat, rep in ARROWS:
        text, n = re.subn(pat, rep, text)
        if n:
            print(f"(ui) arrows {rep}: {n} replaced")
    text, n = re.subn("[" + STRIP + "]" + VS + " ?", "", text)
    print(f"(ui) emojis removed: {n}")
    left = [c for c in STRIP if c in text]
    if left:
        fail("some emojis are still there: " + " ".join(left))
    return text


def fix_app(t):
    t = sub_once(t, "home score font", r"^[ \t]*\.text-4xl \{[^\n]*\}[ \t]*$", SCORE_CSS, None, re.M)
    t = sub_once(t, "home screen", r"// ---------- Today ----------\r?\n.*?(?=// ---------- Advice ----------)", TODAY, "window.LinesSummary ?", re.S)
    t = sub_once(t, "data source status icons", r'\{ok \? "' + "\u2705" + VS + r'" : "' + "\u26aa" + VS + r'"\}', SETTINGS_DOT, '"text-slate-400"}>' + DOT)
    t = common(t)
    if "ReactDOM.createRoot" not in t or "const SR = {" not in t:
        fail("fantasy-gm.html looks damaged after the changes.")
    return t


def fix_lines(t):
    total = 0
    for a, b in COLORS:
        total += t.count(a)
        t = t.replace(a, b)
    print(f"(ui) Lines tab colours changed: {total}")
    if total == 0 and "#8b7cff" not in t:
        fail("lines-tab.js doesn't have the colours I expected.")
    t = sub_once(t, "home line-changes card", r"^[ \t]*window\.LinesTab = LinesTab;[ \t]*$", SUMMARY, "window.LinesSummary = LinesSummary", re.M)
    t = common(t)
    if "window.LinesTab = LinesTab" not in t:
        fail("lines-tab.js looks damaged after the changes.")
    return t


def fix_ask(t):
    t = sub_once(t, "news tag filter",
                 r'\(H\.tags\(p, K\) \|\| \[\]\)\.map\(\(x\) => x\.t\)\.filter\(\(t\) => t && !t\.startsWith\("' + "\U0001F4F0" + VS + r'"\)\)',
                 "(H.tags(p, K) || []).filter((x) => x.t && !x.u).map((x) => x.t)",
                 ".filter((x) => x.t && !x.u)")
    t = common(t)
    if "window.AskPanel = AskPanel" not in t:
        fail("ask-panel.js looks damaged after the changes.")
    return t


FIX = {"fantasy-gm.html": fix_app, "lines-tab.js": fix_lines, "ask-panel.js": fix_ask}


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "test"
    if mode == "undo":
        n = 0
        for src, (_, bak) in FILES.items():
            b = pathlib.Path(bak)
            if b.exists():
                pathlib.Path(src).write_text(b.read_text(encoding="utf-8"), encoding="utf-8")
                print(f"(ui) restored {src}")
                n += 1
        if not n:
            fail("no backups found - live mode has never been run.")
        return
    if mode not in ("test", "live"):
        fail("mode must be test, live or undo")
    out = {}
    for src in FILES:
        p = pathlib.Path(src)
        if not p.exists():
            fail(f"{src} is missing from the repo")
        print(f"--- {src}")
        old = p.read_text(encoding="utf-8")
        out[src] = (old, FIX[src](old))
    if mode == "test":
        html = out["fantasy-gm.html"][1]
        html = sub_once(html, "test page loads test Lines tab", r'src="lines-tab\.js\?t=', 'src="lines-tab-test.js?t=')
        html = sub_once(html, "test page loads test Ask panel", r'src="ask-panel\.js\?t=', 'src="ask-panel-test.js?t=')
        out["fantasy-gm.html"] = (out["fantasy-gm.html"][0], html)
        for src, (test, _) in FILES.items():
            pathlib.Path(test).write_text(out[src][1], encoding="utf-8")
        print("(ui) test copies written - open fantasy-gm-test.html to check")
    else:
        for src, (_, bak) in FILES.items():
            b = pathlib.Path(bak)
            if not b.exists():
                b.write_text(out[src][0], encoding="utf-8")
                print(f"(ui) backup saved: {bak}")
            pathlib.Path(src).write_text(out[src][1], encoding="utf-8")
        print("(ui) live files updated")


if __name__ == "__main__":
    main()
