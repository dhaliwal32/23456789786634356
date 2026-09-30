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

SIDE2 = r'''function Side({ l, s, id }) {
  // matchup row layout v4: big logo beside name + opponent/time, same font for totals
  return (
    <div className="p-3 flex flex-col h-full">
      <div className="flex justify-between font-semibold mb-1"><TL s={s} id={id} className="truncate" /><span>{f1(l.total)}</span></div>
      <table className="w-full text-sm"><tbody>
        {l.start.map((p) => {
          const g = gameOf(p.t, p.dt), o = oddsFor(p.t, p.dt);
          const gc = p.gs ? (p.gs.includes("confirmed") && !p.gs.includes("un") ? "text-green-700 font-semibold" : p.gs === "not starting" ? "text-red-600" : "text-amber-600") : "";
          return (
            <tr key={p.id} className="border-t border-slate-100">
              <td className="py-2 pr-2 text-xs text-slate-500 w-10 align-middle">{p.slot}</td>
              <td className="py-2 align-middle">
                <div className="flex items-center gap-3 min-w-0">
                  <TeamLogo t={p.t} size={36} />
                  <div className="min-w-0">
                    <div className="flex items-center gap-2 min-w-0">
                      <PN p={p} className="truncate" />
                      {!p.gs && p.prob < 1 ? <span className="text-xs text-slate-400">{Math.round(p.prob * 100)}%</span> : null}
                      {p.gs ? <span className={"text-xs " + gc}>{p.gs}</span> : null}
                    </div>
                    {g ? <div className="text-xs text-slate-500 mt-0.5">{(g.h ? "vs " : "@") + g.o} · {gameTime(g)}</div> : null}
                  </div>
                </div>
              </td>
              <td className="py-2 text-right whitespace-nowrap align-middle">
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
      <div className="mt-auto pt-3"><div className="flex justify-between font-semibold border-t border-slate-200 pt-2"><span>Projected today</span><span>{f1(l.total)}</span></div></div>
    </div>
  );
}
'''

WIN_HELPERS = r'''// ---------- win probability (news_logos.py) ----------
const normCdf = (z) => { const t = 1 / (1 + 0.2316419 * Math.abs(z)); const d = 0.3989423 * Math.exp(-z * z / 2); const p = d * t * (0.3193815 + t * (-0.3565638 + t * (1.781478 + t * (-1.821256 + t * 1.330274)))); return z > 0 ? 1 - p : p; };
// spread of a team's remaining points: game-to-game swings of every lineup player-game + 10% projection error
const projVar = (R) => { let v = (0.1 * R.total) ** 2; R.days.forEach((L) => { if (L) L.start.forEach((p) => { const sd = p.p === "G" ? 3 + 0.8 * p.x : 1.5 + 0.6 * p.x; v += sd * sd; }); }); return v; };
const winProb = (A, B, aA, aB) => { const m = aA + A.total - (aB + B.total); const sd = Math.sqrt(projVar(A) + projVar(B)); return sd > 0 ? normCdf(m / sd) : m > 0 ? 1 : m < 0 ? 0 : 0.5; };
const wpTxt = (v) => Math.round(Math.max(0.01, Math.min(0.99, v)) * 100) + "%";
function winChance(s, roster) {
  const w = deriveWeek(s.weeks[s.wk] || s.weeks[0], s.autoDone);
  const opp = oppOf(w, s.me) || s.opp;
  if (!opp) return null;
  const K = s.blend, done = w.done || 0;
  const A = weekProj(roster || s.players.filter((p) => p.ft === s.me), w, K, done);
  const B = weekProj(s.players.filter((p) => p.ft === opp), w, K, done);
  return winProb(A, B, +((w.act || {})[s.me]) || 0, +((w.act || {})[opp]) || 0);
}
const afterMove = (s, add, drop) => s.players.filter((p) => p.ft === s.me && p.id !== drop.id).concat([{ ...add, ft: s.me }]);
const WinDelta = ({ s, add, drop, base }) => {
  const b = base === undefined ? winChance(s) : base;
  const n = winChance(s, afterMove(s, add, drop));
  if (b == null || n == null) return null;
  const d = Math.round(n * 100) - Math.round(b * 100);
  return <span className={"text-xs whitespace-nowrap " + (d > 0 ? "text-green-700" : d < 0 ? "text-red-600" : "text-slate-500")} title="Chance to win this week's matchup, before and after the move">win {wpTxt(b)} → {wpTxt(n)}</span>;
};

'''

R6_HELPERS = r'''// ---------- round 6: moves left, fill slots, ESPN lineup check, goalie streams, strategy (news_logos.py) ----------
const movesLeft = (s, tid, w) => {
  const E = window.ESPN_DATA || {};
  if (E.acq && w && w.period != null) { const a = E.acq[String(tid).replace(/^t/, "")]; if (a) return Math.max(0, 3 - (+a[String(w.period)] || 0)); }
  return tid === s.me ? Math.max(0, 3 - (((s.movesUsed || {})[s.wk]) || 0)) : null;
};
const gamesMoves = (s, tid, w, R) => { const m = movesLeft(s, tid, w); return R.used + " games left" + (m != null ? " · " + m + " move" + (m === 1 ? "" : "s") + " left" : ""); };
const dropFor = (s, add) => {
  const K = s.blend, mine = s.players.filter((p) => p.ft === s.me && !p.ir);
  const prot = new Set([...mine].sort((a, b) => effAvg(b, K) - effAvg(a, K)).slice(0, s.protectTop ?? 8).map((p) => p.id));
  const mins = { F: s.minF ?? 10, D: s.minD ?? 5, G: s.minGo ?? 2 };
  const cnt = { F: 0, D: 0, G: 0 }; mine.forEach((p) => { cnt[p.p]++; });
  const pv = (p) => effAvg(p, K) * (p.p === "G" ? p.prob : 1);
  return mine.filter((p) => !prot.has(p.id) && !p.keep && (p.p === add.p || cnt[p.p] - 1 >= mins[p.p])).sort((a, b) => pv(a) - pv(b))[0] || null;
};
const strategy = (p) => (p == null ? null : p >= 0.75 ? ["Play it safe", "You're a clear favourite. Keep steady skaters in, skip risky goalie streams and save moves for injuries."]
  : p >= 0.55 ? ["Protect the edge", "Slight favourite. Take sure points: stream skaters with extra games before goalies."]
  : p >= 0.4 ? ["Toss-up", "Every game counts. Fill every empty slot and use all your moves."]
  : ["Swing big", "You're the underdog. Chase upside: confirmed goalies with good win odds and players on hot power plays."]);
const StrategyLine = ({ p }) => { const t = strategy(p); return t ? <div className="text-sm mt-2"><span className="font-semibold">{t[0]}</span><span className="text-slate-500"> · {t[1]}</span></div> : null; };
function FillSlot({ l, s, wk, d }) {
  const K = s.blend, dt = wk.dates ? wk.dates[d] : null;
  if (!dt || dt < todayISO() || l.empty <= 0) return null;
  const c = { F: 0, D: 0, UTIL: 0, G: 0 }; l.start.forEach((p) => { c[p.slot] = (c[p.slot] || 0) + 1; });
  const open = { F: 9 - c.F, D: 5 - c.D, U: 1 - c.UTIL, G: 2 - c.G };
  const fits = (p) => (p.p === "G" ? open.G > 0 : open[p.p] > 0 || open.U > 0);
  const val = (p) => effAvg(p, K, dt) * (p.p === "G" ? gStart(p, dt).v : p.prob) * avail(p, dt);
  const best = s.players.filter((p) => p.ft === "fa" && p.prob > 0 && (p.proj !== false || p.gp > 0) && (wk.games[p.t] || []).includes(d) && fits(p))
    .map((p) => ({ p, v: val(p) })).filter((x) => x.v > 0).sort((a, b) => b.v - a.v).slice(0, 2);
  if (!best.length) return null;
  const ml = movesLeft(s, s.me, wk);
  return (
    <div className="mt-3 rounded-lg border border-slate-200 px-3 py-2">
      <div className="text-xs uppercase tracking-wide text-slate-500">Fill an empty spot{ml != null ? " · " + ml + " move" + (ml === 1 ? "" : "s") + " left" : ""}</div>
      {best.map(({ p, v }) => { const dr = dropFor(s, p), g = gameOf(p.t, dt); return (
        <div key={p.id} className="flex items-center gap-3 py-2">
          <TeamLogo t={p.t} size={28} />
          <div className="min-w-0 flex-1">
            <div className="flex items-center gap-2"><PN p={p} className="truncate" /><span className="text-xs text-slate-400">{p.p}</span></div>
            <div className="text-xs text-slate-500 mt-0.5">{[g ? (g.h ? "vs " : "@") + g.o + " · " + gameTime(g) : null, dr ? "drop " + dr.n : null].filter(Boolean).join(" · ")}</div>
          </div>
          <div className="text-right whitespace-nowrap"><div className="font-semibold text-green-700">+{f1(v)}</div>{dr ? <WinDelta s={s} add={p} drop={dr} /> : null}</div>
        </div>
      ); })}
    </div>
  );
}
function espnLineupChecks(mine, L, wk, di, dday, today) {
  const SL = (window.ESPN_DATA || {}).slots;
  if (!SL || !L || dday !== today) return [];
  const sid = (p) => SL[String(p.id).slice(1)];
  if (!mine.some((p) => sid(p) != null)) return [];
  const act = (p) => { const v = sid(p); return v != null && v !== 7 && v !== 8; };
  const locked = (p) => { const g = gameOf(p.t, dday); return !!(g && g.st && new Date(g.st) <= new Date()); };
  const plays = (p) => (wk.games[p.t] || []).includes(di);
  const best = new Set(L.start.map((p) => p.id));
  const toStart = L.start.filter((p) => !act(p) && !locked(p));
  if (!toStart.length) return [["good", "Your ESPN lineup is already the best one for today"]];
  const out = mine.filter((p) => act(p) && !best.has(p.id) && !locked(p)).sort((a, b) => (plays(a) ? 1 : 0) - (plays(b) ? 1 : 0)).slice(0, toStart.length);
  return [["bad", "On ESPN, start " + toStart.map((p) => p.n).join(", ") + (out.length ? " and bench " + out.map((p) => p.n).join(", ") : "")]];
}
const startTag = (gs) => ((gs.l || "").includes("confirmed") && !(gs.l || "").includes("un") ? ["Confirmed", "bg-green-100 text-green-700"]
  : gs.v >= 0.85 ? ["Likely starter", "bg-amber-100 text-amber-800"] : [Math.round(gs.v * 100) + "% to start", "bg-slate-200 text-slate-600"]);
function GoalieStreams({ s, wk }) {
  const K = s.blend, today = todayISO(), dates = wk.dates || [];
  const base = useMemo(() => winChance(s), [s]);
  const st = strategy(base);
  const days = dates.map((dt, d) => ({ dt, d })).filter((x) => x.dt >= today).map(({ dt, d }) => ({ dt, list: s.players
    .filter((p) => p.ft === "fa" && p.p === "G" && (wk.games[p.t] || []).includes(d) && avail(p, dt) > 0)
    .map((p) => { const gs = gStart(p, dt); return { p, gs, o: oddsFor(p.t, dt), g: gameOf(p.t, dt), v: effAvg(p, K, dt) * gs.v }; })
    .filter((x) => x.gs.v >= 0.4).sort((a, b) => b.v - a.v).slice(0, 3) }));
  return (
    <Section title="Goalie streams" sub="Free-agent goalies for each day left this week, best first. Start status from Daily Faceoff, win chance from betting odds.">
      {st ? <div className="text-sm mb-2"><span className="font-semibold">{st[0]}</span><span className="text-slate-500"> · You're {wpTxt(base)} to win this week. {base >= 0.75 ? "Only stream a confirmed starter with a good win chance." : base < 0.4 ? "A good goalie stream is your best upside." : "Stream when a confirmed starter has a good matchup."}</span></div> : null}
      {days.length ? days.map(({ dt, list }) => (
        <div key={dt} className="mt-4">
          <div className="text-xs uppercase tracking-wide text-slate-500 mb-1">{dt === today ? "Today" : dayLabel(dt)}</div>
          {list.length ? list.map(({ p, gs, o, g, v }) => { const tg = startTag(gs), dr = dropFor(s, p); return (
            <div key={p.id} className="flex items-center gap-3 py-2.5 border-t border-slate-100">
              <TeamLogo t={p.t} size={30} />
              <div className="min-w-0 flex-1">
                <div className="flex flex-wrap items-center gap-2"><PN p={p} /><span className={"text-xs px-1.5 py-0.5 rounded " + tg[1]}>{tg[0]}</span></div>
                <div className="text-xs text-slate-500 mt-0.5">{[g ? (g.h ? "vs " : "@") + g.o + " · " + gameTime(g) : null, o ? "W " + Math.round(o.win * 100) + "%" : null, dr ? "drop " + dr.n : null].filter(Boolean).join(" · ")}</div>
              </div>
              <div className="text-right whitespace-nowrap"><div className="font-semibold">{f1(v)}</div>{dr ? <WinDelta s={s} add={p} drop={dr} base={base} /> : null}</div>
            </div>
          ); }) : <div className="text-sm text-slate-400 py-2 border-t border-slate-100">No free-agent starters play.</div>}
        </div>
      )) : <div className="text-slate-400">No days left this week.</div>}
    </Section>
  );
}

'''

CARD_A_OLD = r'''<Card label={teamName(s, a)} value={f1(fa)} sub={`${f1(aA)} actual + ${f1(A.total)} proj`} />'''
CARD_A_NEW = r'''<Card label={teamName(s, a)} value={f1(fa)} sub={<>{f1(aA)} actual + {f1(A.total)} proj<br />{gamesMoves(s, a, wk, A)}</>} />'''
CARD_B_OLD = r'''<Card label={teamName(s, b)} value={f1(fb)} sub={`${f1(aB)} actual + ${f1(B.total)} proj`} />'''
CARD_B_NEW = r'''<Card label={teamName(s, b)} value={f1(fb)} sub={<>{f1(aB)} actual + {f1(B.total)} proj<br />{gamesMoves(s, b, wk, B)}</>} />'''
BAR_OLD = r'''<div className="h-1 rounded-full bg-slate-200 mt-2 overflow-hidden"><div className="h-full bg-green-500" style={{ width: pct + "%" }}></div></div>'''
BAR_NEW = r'''<div className="h-1 rounded-full bg-slate-200 mt-2 overflow-hidden"><div className="h-full bg-green-500" style={{ width: Math.round(winProb(X.r, Y.r, X.act, Y.act) * 100) + "%" }}></div></div><div className="flex justify-between text-xs text-slate-500 mt-1.5"><span>{wpTxt(winProb(X.r, Y.r, X.act, Y.act))} to win</span><span>{wpTxt(1 - winProb(X.r, Y.r, X.act, Y.act))}</span></div>'''
EMPTY_OLD = r'''{l.empty > 0 && <div className="text-xs text-slate-500 mt-1">Empty slots: {l.empty}</div>}'''

# ---------- Python files (applied in live mode only, checked for errors first) ----------
SYNC, ALERTS = "espn_sync.py", "gm_alerts.py"
PY_BAK = {SYNC: "espn_sync.backup-news.py", ALERTS: "gm_alerts.backup-news.py"}
PY_DONE = {SYNC: '"slots": {str(k)', ALERTS: "(news_logos.py)"}
SYNC_OLD = '"periods": periods, "matchups": matchups}'
SYNC_NEW = ('"periods": periods, "matchups": matchups, "slots": {str(k): v for k, v in slots.items()}, '
            '"acq": ({str(t.get("id")): ((t.get("transactionCounter") or {}).get("matchupAcquisitionTotals") or {}) '
            'for t in lg.get("teams", [])} if any("transactionCounter" in t for t in lg.get("teams", [])) else None)}')
GOALIE_BLOCK = r'''for p in active:  # 2b) goalie still not confirmed close to puck drop (news_logos.py)
    if p["p"] != "G" or not upcoming(p["t"]) or games[p["t"]][1] - now > timedelta(minutes=75):
        continue
    gst = next(((v.get("status") or "").lower() for k, v in gday.items() if norm(k) == norm(p["n"])), "")
    if "confirm" in gst and "un" not in gst:
        continue
    if any(v.get("team") == p["t"] and "confirm" in (v.get("status") or "").lower() and "un" not in (v.get("status") or "").lower() for k, v in gday.items() if norm(k) != norm(p["n"])):
        continue
    alerts.append(("Goalie not confirmed yet", f"{p['n']} ({p['t']}, {lbl(p['t'])}) still isn't confirmed as tonight's starter. Check before puck drop and have a backup ready.", "lineup", True, "warning"))'''


def py_ok(name, src):
    try:
        compile(src, name, "exec")
    except SyntaxError as ex:
        fail(f"{name} would have a Python error after the change (line {ex.lineno}): {ex.msg}")


def fix_sync(t):
    t = lit(t, "sync: save ESPN lineup slots and moves used", SYNC_OLD, SYNC_NEW, '"slots": {str(k)')
    py_ok(SYNC, t)
    return t


def fix_alerts(t):
    t = sub_once(t, "alerts: scratch check near each game", r"if SCRATCH_FROM <= now\.hour < SCRATCH_TO:",
                 "if True:  # scratch check runs within 3 hours of each game (news_logos.py)", "scratch check runs within 3 hours")
    t = sub_once(t, "alerts: scratch timing", r'if p\["p"\] == "G" or not upcoming\(p\["t"\]\) or is_out\(p\):',
                 'if p["p"] == "G" or not upcoming(p["t"]) or is_out(p) or games[p["t"]][1] - now > timedelta(hours=3):',
                 'or games[p["t"]][1] - now > timedelta(hours=3)')
    if "2b) goalie still not confirmed" in t:
        print("(news) alerts: unconfirmed goalie warning: already done")
    else:
        m = list(re.finditer(r"^([ \t]*)if True:  # scratch check runs", t, re.M))
        if len(m) != 1:
            fail("alerts: could not find where to add the goalie warning. Send this log to the AI helper.")
        ind = m[0].group(1)
        t = t[:m[0].start()] + "".join(ind + ln + "\n" for ln in GOALIE_BLOCK.splitlines()) + t[m[0].start():]
        print("(news) alerts: unconfirmed goalie warning: updated")
    py_ok(ALERTS, t)
    return t


PY_FIXES = {SYNC: fix_sync, ALERTS: fix_alerts}

# ---------- lines-tab.js: logos next to team names only (applied in live mode) ----------
LINES = "lines-tab.js"
PY_BAK[LINES] = "lines-tab.backup-news.js"
PY_DONE[LINES] = "H.TeamLogo t={x.t} size={32}"


def babel_ok(code, name):
    if not shutil.which("node") or not os.path.exists(BABEL):
        print(f"(news) {name}: syntax check skipped (checker not installed)")
        return
    pathlib.Path("/tmp/check.jsx").write_text(code, encoding="utf-8")
    js = ("const B=require(%r);const fs=require('fs');try{B.transform(fs.readFileSync('/tmp/check.jsx','utf8'),"
          "{presets:['react']});console.log('ok')}catch(e){console.log(e.message);process.exit(1)}") % BABEL
    r = subprocess.run(["node", "-e", js], capture_output=True, text=True)
    if r.returncode:
        fail(f"{name} would have a syntax error: " + (r.stdout or r.stderr)[:600])
    print(f"(news) {name}: syntax check ok")


def fix_lines_tab(t):
    t = lit(t, "lines: logo on each team row", '<div className="lt-tmain">',
            '{H.TeamLogo ? <div style={{ flexShrink: 0 }}><H.TeamLogo t={x.t} size={32} /></div> : null}<div className="lt-tmain">',
            "H.TeamLogo t={x.t} size={32}")
    t = lit(t, "lines: logo in grouped changes", "<b>{nm}</b>",
            "{H.TeamLogo ? <H.TeamLogo t={t} size={22} /> : null}<b>{nm}</b>", "H.TeamLogo t={t} size={22}")
    babel_ok(t, LINES)
    return t


JS_FIXES = {LINES: fix_lines_tab}

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

# ---------- round 9: phone layout (only screens 640 px wide or less; desktop unchanged) ----------
R9_CSS = r'''  /* round 9 mobile (news_logos.py) */
  .m-only { display: none !important; }
  .m-tab { padding: 11px 2px 9px; font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: .03em; border-bottom: 3px solid transparent; white-space: nowrap; text-align: center; }
  .m-icon { width: 34px; height: 34px; border-radius: 999px; background: #202020; color: var(--ink); font-size: 18px; line-height: 1; flex-shrink: 0; }
  .m-wk { font-size: 16px; padding: 4px 8px; max-width: 190px; border: 1px solid var(--line2); }
  .m-h2h-head { display: grid; grid-template-columns: minmax(0,1fr) 40px minmax(0,1fr); align-items: end; padding: 10px 12px; border-bottom: 1px solid var(--line); }
  .m-big { font-size: 26px; font-weight: 700; letter-spacing: -.02em; font-variant-numeric: tabular-nums; line-height: 1.1; }
  .m-row { display: grid; grid-template-columns: minmax(0,1fr) 24px minmax(0,1fr); border-bottom: 1px solid var(--line); }
  .m-cell { display: flex; align-items: center; gap: 6px; padding: 8px; min-width: 0; min-height: 54px; }
  .m-slot { display: flex; align-items: center; justify-content: center; background: #151515; font-size: 11px; font-weight: 700; color: var(--mute); }
  .m-pts { font-weight: 600; font-size: 14px; font-variant-numeric: tabular-nums; flex-shrink: 0; min-width: 30px; text-align: center; }
  .m-ghead, .m-rrow { display: grid; gap: 8px; align-items: center; }
  .m-ghead { grid-template-columns: minmax(0,1fr) 42px 34px 46px; font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: .08em; color: var(--mute); padding: 10px 2px 6px; }
  .m-rrow { grid-template-columns: 28px minmax(0,1fr) 42px 34px 46px; padding: 9px 2px; border-top: 1px solid var(--line); cursor: pointer; }
  .m-ghead span + span, .m-num { text-align: right; font-variant-numeric: tabular-nums; }
  @media (max-width: 640px) {
    .m-only { display: block !important; }
    .m-hide { display: none !important; }
    body { overflow-x: hidden; }
    input:not([type=checkbox]), select, textarea { font-size: 16px !important; }
    .max-w-6xl.mx-auto.px-3.py-4 { padding: 12px 10px 90px !important; }
    .bg-white.rounded-xl.p-4 { padding: 1rem .9rem !important; }
    .font-semibold.text-base, .font-bold.text-lg { font-family: Inter, ui-sans-serif, system-ui, -apple-system, sans-serif; font-weight: 700 !important; font-size: 1.05rem !important; }
    .text-4xl { font-size: 2.1rem !important; }
    .overflow-x-auto > table th:first-child, .overflow-x-auto > table td:first-child { position: sticky; left: 0; z-index: 1; background: var(--card); }
    .lg\:grid-cols-5.gap-3.mb-4 { display: flex !important; overflow-x: auto; scroll-snap-type: x mandatory; -webkit-overflow-scrolling: touch; padding-bottom: 4px; }
    .lg\:grid-cols-5.gap-3.mb-4 > * { flex: 0 0 72%; scroll-snap-align: start; }
    .fixed.bottom-5.right-5.rounded-full { bottom: 14px !important; right: 12px !important; padding: 8px 16px !important; font-size: 13px !important; }
    .lt-pills { flex-direction: column !important; align-items: flex-end !important; gap: 4px !important; }
    .lt-rk { width: auto !important; min-width: 26px; font-size: 13px; }
    .lt-tn { font-size: 15px; }
  }
'''

R9_HELPERS = r'''// ---------- round 9: phone layout (news_logos.py) ----------
const M_TABS = [["today", "Today"], ["matchup", "Matchup"], ["myteam", "My Team"], ["moves", "Moves"]];
const M_MORE = [["teams", "Teams"], ["lines", "Lines"], ["league", "League"], ["news", "News"], ["setup", "Setup"]];
const M_MODES = [["espn", "ESPN"], ["blend", "Blend"], ["model", "GM model"], ["ai", "AI (beta)"]];
const M_ST = { DAY_TO_DAY: "DTD", OUT: "Out", INJURY_RESERVE: "IR", SUSPENSION: "Susp." };
const shortN = (n) => { const x = String(n || "").split(" "); return x.length > 1 ? x[0][0] + ". " + x.slice(1).join(" ") : x[0]; };
const mGame = (p) => { const g = gameOf(p.t, p.dt); return g ? (g.h ? "vs " : "@") + g.o + " " + gameTime(g) : ""; };
const mStart = (gs) => (!gs ? "" : gs.includes("confirmed") && !gs.includes("un") ? "Confirmed" : /not starting|rests|backup/.test(gs) ? "May sit" : /likely/.test(gs) ? "Likely" : "Unconfirmed");
function MobileHeader({ s, setS, tab, go, ageH }) {
  const [menu, setMenu] = useState(false);
  const [opts, setOpts] = useState(false);
  const more = M_MORE.find(([k]) => k === tab);
  const pick = (k) => { setMenu(false); setOpts(false); go(k); };
  const dot = !s.lastSync ? "var(--faint)" : ageH !== null && ageH > 2 ? "var(--bad)" : "var(--good)";
  const can = (k) => k === "espn" || (!!window.__MODEL && (k !== "ai" || !!window.__AI));
  const tabBtn = (k, l, on, fn) => (
    <button key={k} onClick={fn} className="m-tab" style={{ color: on ? "var(--ink)" : "var(--mute)", borderBottomColor: on ? "var(--accent)" : "transparent" }}>{l}</button>
  );
  return (
    <div className="m-only">
      <div className="flex items-center gap-2 px-3 pt-2">
        <span className="font-semibold text-white truncate" style={{ fontSize: 18 }}>{teamName(s, s.me) || "Islands GM"}</span>
        <span title={s.lastSync ? "Synced " + fmtTime(s.lastSync) : "Not synced yet"} style={{ width: 7, height: 7, borderRadius: 99, background: dot, flexShrink: 0 }}></span>
        <select className="m-wk ml-auto" value={s.wk} onChange={(e) => setS({ ...s, wk: +e.target.value })}>
          {s.weeks.map((w, i) => <option key={i} value={i}>{(w.label || "").replace(/^Week /, "Wk ")}</option>)}
        </select>
        <button className="m-icon" aria-label="Options" onClick={() => { setOpts(!opts); setMenu(false); }}>⋯</button>
      </div>
      {opts && (
        <div className="px-3 pt-2 pb-1">
          <div className="text-xs text-slate-500 mb-1">Projections</div>
          <div className="flex gap-2 overflow-x-auto navscroll">
            {M_MODES.map(([k, l]) => <button key={k} disabled={!can(k)} onClick={() => setS({ ...s, pmode: k, players: [...s.players] })} className={"px-3 py-1 rounded-full text-sm border whitespace-nowrap " + (window.__PMODE === k ? "bg-blue-600 border-blue-600" : "border-slate-300 text-slate-600") + (can(k) ? "" : " opacity-40")}>{l}</button>)}
          </div>
          <div className="flex items-center gap-3 text-xs text-slate-500 mt-2">
            <span>{s.lastSync ? "Synced " + fmtTime(s.lastSync) : "Not synced yet"}</span>
            <a href="ai-dashboard.html" className="text-blue-600 ml-auto">AI Lab</a>
          </div>
        </div>
      )}
      <div className="grid grid-cols-5 mt-1">
        {M_TABS.map(([k, l]) => tabBtn(k, l, tab === k && !menu, () => pick(k)))}
        {tabBtn("more", more ? more[1] : "More", !!more || menu, () => { setMenu(!menu); setOpts(false); })}
      </div>
      {menu && (
        <div className="border-t border-slate-800">
          {M_MORE.map(([k, l]) => <button key={k} onClick={() => pick(k)} className="block w-full text-left px-4 py-3 border-b border-slate-800" style={{ color: tab === k ? "var(--accent)" : "var(--ink)" }}>{l}</button>)}
        </div>
      )}
    </div>
  );
}
function MSide({ p, right }) {
  const al = right ? "flex-end" : "flex-start";
  if (!p) return <div className="m-cell" style={{ justifyContent: al }}><span className="text-sm text-slate-400">Empty</span></div>;
  const st = p.p === "G" ? mStart(p.gs) : "";
  const stc = st === "Confirmed" ? "text-green-700" : st === "May sit" ? "text-red-600" : "text-amber-600";
  const inj = p.status && p.status !== "ACTIVE" ? M_ST[p.status] || "" : "";
  const info = (
    <div className="min-w-0" style={{ flex: 1, textAlign: right ? "right" : "left" }}>
      <div className="flex items-center gap-1 min-w-0" style={{ justifyContent: al }}>
        <button type="button" className="truncate font-medium" style={{ minWidth: 0 }} onClick={() => window.__NAV && window.__NAV.player(p)}>{shortN(p.n)}</button>
        <span style={{ flexShrink: 0, lineHeight: 0 }}><TeamLogo t={p.t} size={16} /></span>
        {inj ? <span className="text-xs text-red-600" style={{ flexShrink: 0 }}>{inj}</span> : null}
      </div>
      <div className="text-xs text-slate-500 truncate">{st ? <span className={stc}>{st} · </span> : null}{mGame(p)}</div>
    </div>
  );
  const pts = <div className="m-pts">{f1(p.x)}</div>;
  return <div className="m-cell">{right ? pts : info}{right ? info : pts}</div>;
}
function H2H({ x, y, s, a, b, wk, d }) {
  const rows = [];
  ["F", "D", "UTIL", "G"].forEach((sl) => {
    const A = x.start.filter((p) => p.slot === sl), B = y.start.filter((p) => p.slot === sl);
    for (let i = 0; i < Math.max(A.length, B.length); i++) rows.push([sl, A[i] || null, B[i] || null]);
  });
  const sit = (l, id) => (l.bench.length ? <div className="text-xs text-slate-500 px-3 pt-2">{teamName(s, id)} would sit: {l.bench.map((p) => shortN(p.n)).join(", ")}</div> : null);
  return (
    <div>
      <div className="m-h2h-head">
        <div className="min-w-0"><div className="text-xs text-slate-500 truncate">{teamName(s, a)}</div><div className="m-big">{f1(x.total)}</div></div>
        <div className="text-xs text-slate-500 text-center pb-1">vs</div>
        <div className="min-w-0 text-right"><div className="text-xs text-slate-500 truncate">{teamName(s, b)}</div><div className="m-big">{f1(y.total)}</div></div>
      </div>
      {rows.length ? rows.map(([sl, p, q], i) => (
        <div key={i} className="m-row"><MSide p={p} /><div className="m-slot">{sl === "UTIL" ? "U" : sl}</div><MSide p={q} right /></div>
      )) : <div className="text-sm text-slate-400 px-3 py-3">No games for either team.</div>}
      {sit(x, a)}{sit(y, b)}
      {x.empty || y.empty ? <div className="text-xs text-slate-500 px-3 pt-2">Empty slots: {teamName(s, a)} {x.empty} · {teamName(s, b)} {y.empty}</div> : null}
      {a === s.me ? <div className="px-3"><FillSlot l={x} s={s} wk={wk} d={d} /></div> : null}
      <div className="h-2"></div>
    </div>
  );
}

'''

ROSTERVIEW = r'''function RosterView({ s, wk, team }) {
  // roster view v9: no Signals column, phone list by position (news_logos.py)
  const K = s.blend, done = wk.done || 0;
  const roster = s.players.filter((p) => p.ft === team);
  const order = { F: 0, D: 1, G: 2 };
  const sorted = [...roster].sort((a, b) => (a.ir ? 1 : 0) - (b.ir ? 1 : 0) || order[a.p] - order[b.p] || effAvg(b, K) - effAvg(a, K));
  const Ls = wk.days.map((_, d) => (d < done ? null : dayLineup(roster, wk, d, K)));
  const wkPts = (p) => Ls.reduce((a, L) => { if (!L) return a; const x = L.start.find((y) => y.id === p.id); return a + (x ? x.x : 0); }, 0);
  const left = (p) => (wk.games[p.t] || []).filter((d) => d >= done).length;
  const stTag = (p) => (p.ir ? "IR" : p.status && p.status !== "ACTIVE" ? M_ST[p.status] || p.status.replace(/_/g, " ") : "");
  const groups = [["Forwards", sorted.filter((p) => !p.ir && p.p === "F")], ["Defence", sorted.filter((p) => !p.ir && p.p === "D")], ["Goalies", sorted.filter((p) => !p.ir && p.p === "G")], ["Injured reserve", sorted.filter((p) => p.ir)]].filter((g) => g[1].length);
  return (
    <div>
      <div className="m-hide overflow-x-auto">
        <table className="w-full text-sm">
          <thead className="text-left"><tr>{["Player", "", "Proj / game", "Games left", "Week pts"].map((h, i) => <th key={i} className="px-2 py-2">{h}</th>)}</tr></thead>
          <tbody>{sorted.map((p) => (
            <tr key={p.id} className="border-t border-slate-100 align-top">
              <td className="px-2 py-2 whitespace-nowrap"><PN p={p} />{p.ir ? <span className="text-red-600 text-xs ml-1">IR</span> : p.status && p.status !== "ACTIVE" ? <span className="text-red-600 text-xs ml-1">{p.status.replace(/_/g, " ")}</span> : null}</td>
              <td className="px-2 py-2 text-xs text-slate-500 whitespace-nowrap">{p.p} · <TeamLogo t={p.t} /></td>
              <td className="px-2 py-2">{f1(effAvg(p, K))}</td>
              <td className="px-2 py-2">{p.ir ? "–" : left(p)}</td>
              <td className="px-2 py-2 font-semibold">{p.ir ? "–" : f1(wkPts(p))}</td>
            </tr>
          ))}</tbody>
        </table>
      </div>
      <div className="m-only">
        {groups.map(([title, list]) => (
          <div key={title} className="mb-2">
            <div className="m-ghead"><span>{title}</span><span>Proj</span><span>Gms</span><span>Week</span></div>
            {list.map((p) => { const tg = stTag(p); return (
              <div key={p.id} className="m-rrow" role="button" onClick={() => window.__NAV && window.__NAV.player(p)}>
                <TeamLogo t={p.t} size={26} />
                <div className="min-w-0">
                  <div className="truncate font-medium">{p.n}</div>
                  <div className="text-xs text-slate-500">{p.p}{tg ? <span className="text-red-600"> · {tg}</span> : null}</div>
                </div>
                <span className="m-num">{f1(effAvg(p, K))}</span>
                <span className="m-num">{p.ir ? "–" : left(p)}</span>
                <span className="m-num font-semibold">{p.ir ? "–" : f1(wkPts(p))}</span>
              </div>
            ); })}
          </div>
        ))}
      </div>
    </div>
  );
}

'''

# ---------- round 10: Lines tab on phones, cleaner Players list, one trade builder ----------
R10_CSS = r'''  /* round 10 trades (news_logos.py) */
  .tb-grid { display: grid; grid-template-columns: minmax(0,1fr) minmax(0,1fr); gap: 12px; }
  .tb-p { display: flex; align-items: center; gap: 8px; width: 100%; text-align: left; padding: 8px; border: 1px solid var(--line); border-radius: 10px; margin-bottom: 6px; background: transparent; color: var(--ink); }
  .tb-p.on { border-color: var(--accent); background: var(--accentSoft); }
  .tb-p.ir { opacity: .5; }
  .tb-chk { width: 22px; height: 22px; border-radius: 999px; border: 1px solid var(--line2); display: flex; align-items: center; justify-content: center; font-size: 13px; flex-shrink: 0; color: var(--mute); }
  .tb-p.on .tb-chk { background: var(--accent); border-color: var(--accent); color: #111; }
  .tb-sel { min-height: 70px; border: 1px dashed var(--line2); border-radius: 12px; padding: 10px; min-width: 0; }
  .tb-chip { display: flex; align-items: center; gap: 6px; padding: 4px 0; font-size: 14px; min-width: 0; }
  .tb-x { margin-left: auto; color: var(--mute); padding: 0 4px; font-size: 16px; }
  .tb-tiles { display: grid; grid-template-columns: repeat(2, minmax(0,1fr)); gap: 10px; }
  .tb-pk { border: 1px solid var(--line); border-radius: 12px; padding: 10px 12px; }
  .m-inl { display: none !important; }
  @media (min-width: 768px) { .tb-tiles { grid-template-columns: repeat(4, minmax(0,1fr)); } }
  @media (max-width: 640px) {
    .m-inl { display: inline !important; }
    .m-tab { font-size: 11px; letter-spacing: .01em; }
    .tb-grid { gap: 8px; }
    .tb-p { padding: 7px 6px; gap: 6px; }
  }
'''

R10_HELPERS = r'''// ---------- round 10: one trade builder (analyzer + 2-for-1 + best waiver pickup) (news_logos.py) ----------
const Dlt = ({ v }) => <span className={"font-semibold " + (v >= 0 ? "text-green-700" : "text-red-600")}>{v >= 0 ? "+" : ""}{f1(v)}</span>;
const tbFlags = (p, K) => {
  const f = [], g = sigOf(p), l = g.luck, id = typeof p.id === "string" && p.id[0] === "e" ? p.id.slice(1) : null;
  const mb = window.__MODEL && id ? (window.__MODEL.base || {})[id] : null;
  if (mb != null && p.proj && p.avg > 0) {
    if (mb / p.avg <= 0.85 && p.avg - mb >= 1) f.push({ t: "ESPN overrates", sell: true });
    else if (mb / p.avg >= 1.15 && mb - p.avg >= 1) f.push({ t: "underrated", sell: false });
  }
  if (l && ((l.t === "s" && l.d >= 2) || (l.t === "g" && l.d >= 4))) f.push({ t: "lucky", sell: true });
  if (l && ((l.t === "s" && l.d <= -2) || (l.t === "g" && l.d <= -4))) f.push({ t: "unlucky", sell: false });
  if ((formRatio(p, K) || 0) >= 1.25) f.push({ t: "hot", sell: true });
  return f;
};
function TradeBuilder({ s, initPartner }) {
  const K = s.blend, today = todayISO();
  const others = s.teams.filter((t) => t.id !== s.me);
  const [partner, setPartner] = useState(initPartner || (others[0] || {}).id || "");
  const [give, setGive] = useState([]);
  const [get, setGet] = useState([]);
  const [pick, setPick] = useState({});
  const [busy, setBusy] = useState("");
  const [ideas, setIdeas] = useState(null);
  const nR = s.weeks.length - s.wk;
  const mins = { F: s.minF ?? 10, D: s.minD ?? 5, G: s.minGo ?? 2 };
  const order = { F: 0, D: 1, G: 2 };
  const mine = s.players.filter((p) => p.ft === s.me);
  const theirs = s.players.filter((p) => p.ft === partner);
  const pg = (p) => effAvg(p, K) * (p.p === "G" ? p.prob : 1);
  const vv = (p) => effAvg0(p, K) * (p.p === "G" ? p.prob : 1);
  const gl = (p) => [...(SCHED[p.t] || [])].filter((d) => d >= today && avail(p, d) > 0).length;
  const cnt = (r) => { const c = { F: 0, D: 0, G: 0 }; r.forEach((p) => { if (!p.ir) c[p.p]++; }); return c; };
  const tv = useMemo(() => { const o = {}; s.players.forEach((p) => { if (p.ft !== "fa" || p.proj !== false || p.gp > 0) o[p.id] = rosRaw(p, K); }); return o; }, [s.players, K, window.__PMODE]);
  const fas = useMemo(() => s.players.filter((p) => p.ft === "fa" && p.prob > 0 && tv[p.id] > 0).sort((a, b) => tv[b.id] - tv[a.id]).slice(0, 60), [tv]);
  const rep = useMemo(() => { const o = {}; ["F", "D", "G"].forEach((k) => { const l = s.players.filter((p) => p.ft === "fa" && p.p === k && p.prob > 0 && (p.proj !== false || p.gp > 0)).map(vv).sort((a, b) => b - a).slice(0, 5); o[k] = l.length ? l.reduce((a, b) => a + b, 0) / l.length : 0; }); return o; }, [s.players, K]);
  const pe = (p) => Math.max(0, vv(p) - (rep[p.p] || 0)) * gl(p);
  const Gv = mine.filter((p) => give.includes(p.id)), Rv = theirs.filter((p) => get.includes(p.id));
  const extra = Math.max(0, Gv.length - Rv.length), need = Math.max(0, Rv.length - Gv.length);
  const ready = Gv.length > 0 && Rv.length > 0;
  const picks = [...Array(extra)].map((_, k) => fas.find((f) => f.id === pick[k]) || null);
  const myAfter0 = mine.filter((p) => !give.includes(p.id)).concat(Rv.map((p) => ({ ...p, ft: s.me })));
  const base = useMemo(() => (ready ? { r: horizonTotal(mine, s, nR), w4: horizonTotal(mine, s, 4), th: horizonTotal(theirs, s, nR) } : null), [ready, partner, s.players, s.wk, K]);
  const res = useMemo(() => {
    if (!ready || !base) return null;
    const got = picks.filter(Boolean).map((f) => ({ ...f, ft: s.me }));
    const after = myAfter0.concat(got);
    const thAfter = theirs.filter((p) => !get.includes(p.id)).concat(Gv.map((p) => ({ ...p, ft: partner })));
    const my = horizonTotal(after, s, nR) - base.r;
    return { my, my4: horizonTotal(after, s, 4) - base.w4, noPick: got.length ? horizonTotal(myAfter0, s, nR) - base.r : my, th: horizonTotal(thAfter, s, nR) - base.th, after };
  }, [base, give.join(), get.join(), JSON.stringify(pick)]);
  const toggle = (sel, set, id) => { set(sel.includes(id) ? sel.filter((x) => x !== id) : [...sel, id]); setPick({}); };
  const findPickup = (k) => {
    setBusy("pick" + k);
    setTimeout(() => {
      const cur = myAfter0.concat(picks.filter((f, i) => f && i !== k).map((f) => ({ ...f, ft: s.me })));
      const c = cnt(cur), short = ["F", "D", "G"].filter((x) => c[x] < mins[x]);
      const used = new Set(picks.filter(Boolean).map((f) => f.id));
      const cands = fas.filter((f) => !used.has(f.id) && (!short.length || short.includes(f.p))).slice(0, 15);
      let best = null;
      cands.forEach((f) => { const v = horizonTotal(cur.concat([{ ...f, ft: s.me }]), s, nR); if (!best || v > best.v) best = { f, v }; });
      setPick((x) => ({ ...x, [k]: best ? best.f.id : undefined }));
      setBusy("");
    }, 30);
  };
  const findIdeas = () => {
    setBusy("ideas");
    setTimeout(() => {
      const mineR = mine.filter((p) => !p.ir);
      const keep = new Set([...mineR].sort((a, b) => (tv[b.id] || 0) - (tv[a.id] || 0)).slice(0, 2).map((p) => p.id));
      const bestFA = {}; ["F", "D", "G"].forEach((k) => (bestFA[k] = fas.find((f) => f.p === k)));
      const cands = [];
      others.forEach((t) => {
        s.players.filter((p) => p.ft === t.id && !p.ir).sort((a, b) => (tv[b.id] || 0) - (tv[a.id] || 0)).slice(0, 4).forEach((T) => {
          const pool = mineR.filter((p) => !keep.has(p.id) && (tv[p.id] || 0) < (tv[T.id] || 0));
          for (let i = 0; i < pool.length; i++) for (let j = i + 1; j < pool.length; j++) {
            const A = pool[i], B = pool[j];
            if (pe(T) <= 0 || pe(A) + pe(B) < 0.95 * pe(T) || Math.max(vv(A), vv(B)) < 0.75 * vv(T)) continue;
            const c = cnt(mineR); c[A.p]--; c[B.p]--; c[T.p]++;
            const short = ["F", "D", "G"].filter((k) => c[k] < mins[k]);
            if (short.length > 1) continue;
            const fa = short.length ? bestFA[short[0]] : ["F", "D", "G"].map((k) => bestFA[k]).filter(Boolean).sort((a, b) => tv[b.id] - tv[a.id])[0];
            if (!fa) continue;
            const pre = (tv[T.id] || 0) + tv[fa.id] - (tv[A.id] || 0) - (tv[B.id] || 0);
            if (pre > 0) cands.push({ t, T, A, B, fa, pre });
          }
        });
      });
      cands.sort((a, b) => b.pre - a.pre);
      const seen = new Set(), top = [];
      for (const c of cands) { if (seen.has(c.T.id)) continue; seen.add(c.T.id); top.push(c); if (top.length >= 12) break; }
      const b0 = horizonTotal(mine, s, nR);
      const out = top.map((c) => {
        const after = mine.filter((p) => p.id !== c.A.id && p.id !== c.B.id).concat([{ ...c.T, ft: s.me }, { ...c.fa, ft: s.me }]);
        return { ...c, myR: horizonTotal(after, s, nR) - b0, perc: (pe(c.A) + pe(c.B) - pe(c.T)) / Math.max(1, pe(c.T)) };
      }).filter((x) => x.myR > 0).sort((a, b) => b.myR - a.myR).slice(0, 6);
      setIdeas(out); setBusy("");
    }, 30);
  };
  const load = (x) => { setPartner(x.t.id); setGive([x.A.id, x.B.id]); setGet([x.T.id]); setPick({ 0: x.fa.id }); window.scrollTo(0, 0); };
  const sum = (l, f) => l.reduce((a, p) => a + f(p), 0);
  const vGive = sum(Gv, (p) => tv[p.id] || 0), vGet = sum(Rv, (p) => tv[p.id] || 0);
  const peG = sum(Gv, pe), peR = sum(Rv, pe);
  const theyThink = peR > 0 ? (peG - peR) / peR : 0;
  const edge = vGive > 0 ? (vGet - vGive) / vGive : 0;
  const hasPick = picks.some(Boolean);
  const vd = !res ? null : res.my <= 0 ? ["Bad for you", "bg-red-100 text-red-600", "Your lineup gets worse" + (extra && !hasPick ? ". Try adding the best waiver pickup." : ".")]
    : theyThink >= -0.05 ? ["Good trade", "bg-green-100 text-green-700", "You gain, and by ESPN's numbers it looks fair or better to them."]
    : ["Good for you, hard sell", "bg-amber-100 text-amber-800", "You gain, but by ESPN's numbers they lose. Expect a counter-offer."];
  const drops = need ? myAfter0.filter((p) => !p.ir && !get.includes(p.id)).sort((a, b) => pg(a) - pg(b)).slice(0, need) : [];
  const rows = (list, sel, set) => [...list].sort((a, b) => (a.ir ? 1 : 0) - (b.ir ? 1 : 0) || order[a.p] - order[b.p] || pg(b) - pg(a)).map((p) => {
    const on = sel.includes(p.id), fl = tbFlags(p, K)[0];
    return (
      <button key={p.id} type="button" className={"tb-p" + (on ? " on" : "") + (p.ir ? " ir" : "")} onClick={() => toggle(sel, set, p.id)}>
        <TeamLogo t={p.t} size={22} />
        <div className="min-w-0" style={{ flex: 1 }}>
          <div className="truncate font-medium"><span className="m-hide">{p.n}</span><span className="m-inl">{shortN(p.n)}</span></div>
          <div className="text-xs text-slate-500 truncate">{p.p} · {f1(pg(p))}/g{p.ir ? " · IR" : ""}{fl ? <span className={fl.sell ? "text-amber-600" : "text-green-700"}> · {fl.t}</span> : null}</div>
        </div>
        <span className="tb-chk">{on ? "✓" : "+"}</span>
      </button>
    );
  });
  const sideBox = (lab, list, sel, set) => (
    <div className="tb-sel">
      <div className="text-xs uppercase tracking-wide text-slate-500">{lab}</div>
      {list.length ? list.map((p) => (
        <div key={p.id} className="tb-chip"><TeamLogo t={p.t} size={18} /><span className="truncate">{shortN(p.n)}</span><span className="text-xs text-slate-500">{p.p}</span><button type="button" className="tb-x" onClick={() => toggle(sel, set, p.id)}>×</button></div>
      )) : <div className="text-sm text-slate-400 mt-1">Tap players below</div>}
      {list.length ? <div className="text-xs text-slate-500 mt-1 pt-1 border-t border-slate-100">{f1(sum(list, pg))}/g · {f1(sum(list, (p) => tv[p.id] || 0))} pts rest of season</div> : null}
    </div>
  );
  return (
    <div className="space-y-4">
      <Section title="Trade builder" sub="Pick a team, then tap players in the rosters below. Lineup numbers are rest-of-season points in your best daily lineups.">
        <div className="flex items-center gap-2">
          <span className="text-sm text-slate-500 whitespace-nowrap">Trade with</span>
          <select className={inp + " flex-1"} value={partner} onChange={(e) => { setPartner(e.target.value); setGet([]); setPick({}); }}>{others.map((t) => <option key={t.id} value={t.id}>{t.name}</option>)}</select>
          {give.length || get.length ? <button className="text-xs text-slate-500 underline whitespace-nowrap" onClick={() => { setGive([]); setGet([]); setPick({}); }}>Clear</button> : null}
        </div>
        <div className="tb-grid mt-3">
          {sideBox("You give", Gv, give, setGive)}
          {sideBox("You get", Rv, get, setGet)}
        </div>
        {res && vd ? (
          <div className="mt-4">
            <div className="flex flex-wrap items-center gap-2 mb-3"><span className={"px-3 py-1 rounded-full font-semibold text-sm " + vd[1]}>{vd[0]}</span><span className="text-sm text-slate-500">{vd[2]}</span></div>
            <div className="tb-tiles">
              <Card label="Your lineup" value={<Dlt v={res.my} />} sub={<>rest of season{hasPick ? " incl. pickup" : ""} · next 4 wks <Dlt v={res.my4} /></>} />
              <Card label="Their lineup" value={<Dlt v={res.th} />} sub="rest of season" />
              <Card label="How they see it" value={(theyThink >= 0 ? "+" : "") + Math.round(theyThink * 100) + "%"} sub={theyThink >= -0.05 ? "a win or even for them (ESPN view)" : "looks like a loss to them"} />
              <Card label="Raw value" value={f1(vGive) + " → " + f1(vGet)} sub={edge > 0.25 ? "lopsided: veto risk (4 votes)" : Math.abs(edge) <= 0.1 ? "fair for a league vote" : edge > 0 ? "slightly in your favour" : "you give more value"} />
            </div>
            {(() => { const a = cnt(res.after), b = cnt(mine); return (
              <div className="text-xs text-slate-500 mt-3">Your roster after: {["F", "D", "G"].map((k) => <span key={k} className={"mr-3 " + (a[k] < mins[k] ? "text-red-600 font-semibold" : "")}>{k} {b[k]}→{a[k]}</span>)}{res.after.filter((p) => !p.ir).length}/22 active</div>
            ); })()}
            {drops.length ? <div className="text-sm text-amber-600 mt-2">You'd be over 22 players. Likely drop{drops.length > 1 ? "s" : ""}: {drops.map((p) => p.n).join(", ")} (your lowest projected).</div> : null}
          </div>
        ) : null}
        {ready && extra > 0 ? (
          <div className="tb-pk mt-4">
            <div className="font-semibold">You free {extra} roster spot{extra > 1 ? "s" : ""}</div>
            <div className="text-xs text-slate-500">Fill {extra > 1 ? "them" : "it"} from waivers and see how much it adds.</div>
            {[...Array(extra)].map((_, k) => { const f = picks[k]; return (
              <div key={k} className="mt-3">
                {f ? (
                  <div className="flex items-center gap-2"><TeamLogo t={f.t} size={24} /><PN p={f} /><span className="text-xs text-slate-500">{f.p} · {f1(pg(f))}/g</span><button className="text-xs text-slate-500 ml-auto" onClick={() => setPick((x) => ({ ...x, [k]: undefined }))}>Remove</button></div>
                ) : (
                  <button className="bg-blue-600 rounded-lg px-3 py-1.5 text-sm font-semibold" disabled={!!busy} onClick={() => findPickup(k)}>{busy === "pick" + k ? "Searching…" : "Find best waiver pickup"}</button>
                )}
                <select className={inp + " w-full mt-2"} value={pick[k] || ""} onChange={(e) => { const v = e.target.value; setPick((x) => ({ ...x, [k]: v || undefined })); }}>
                  <option value="">Or choose a free agent…</option>
                  {fas.map((x) => <option key={x.id} value={x.id}>{x.n} ({x.p}, {x.t}) · {f1(pg(x))}/g</option>)}
                </select>
              </div>
            ); })}
            {hasPick && res ? (
              <div className="grid grid-cols-3 gap-2 mt-3 text-center">
                <div><div className="text-xs text-slate-500">Without pickup</div><div className="text-lg"><Dlt v={res.noPick} /></div></div>
                <div><div className="text-xs text-slate-500">With pickup</div><div className="text-lg"><Dlt v={res.my} /></div></div>
                <div><div className="text-xs text-slate-500">Pickup adds</div><div className="text-lg"><Dlt v={res.my - res.noPick} /></div></div>
              </div>
            ) : null}
          </div>
        ) : null}
      </Section>
      <Section title="Trade ideas" sub="2-for-1 offers: give two players, get one better one, then fill the open spot from waivers. Picked so they look fair by ESPN's numbers, which is how most managers judge trades.">
        <button className="bg-blue-600 rounded-lg px-4 py-1.5 text-sm font-semibold" disabled={!!busy} onClick={findIdeas}>{busy === "ideas" ? "Searching…" : "Find 2-for-1 trades"}</button>
        {ideas && (ideas.length ? ideas.map((x, i) => (
          <div key={i} className="py-3 border-t border-slate-100 mt-2">
            <div className="tb-grid">
              <div className="min-w-0"><div className="text-xs text-slate-500">You give</div><div className="truncate">{shortN(x.A.n)}</div><div className="truncate">{shortN(x.B.n)}</div></div>
              <div className="min-w-0"><div className="text-xs text-slate-500">You get · {x.t.name}</div><div className="truncate font-semibold">{shortN(x.T.n)}</div><div className="truncate text-slate-500 text-sm">+ pick up {shortN(x.fa.n)}</div></div>
            </div>
            <div className="flex items-center gap-3 mt-2 text-sm">
              <span>You <Dlt v={x.myR} /></span>
              <span className={"text-xs " + (x.perc >= 0.05 ? "text-green-700" : "text-amber-600")}>{x.perc >= 0.05 ? "Likely accepted" : "About even for them"}</span>
              <button className="text-blue-600 ml-auto" onClick={() => load(x)}>Load</button>
            </div>
          </div>
        )) : <div className="text-sm text-slate-400 mt-2">No 2-for-1 trade helps you right now while still looking fair to the other side.</div>)}
      </Section>
      <Section title="Rosters" sub="Tap to add or remove. Amber tags are sell-high signs, green are buy-low signs.">
        <div className="tb-grid">
          <div className="min-w-0"><div className="text-xs uppercase tracking-wide text-slate-500 mb-2 truncate">{teamName(s, s.me)}</div>{rows(mine, give, setGive)}</div>
          <div className="min-w-0"><div className="text-xs uppercase tracking-wide text-slate-500 mb-2 truncate">{teamName(s, partner)}</div>{rows(theirs, get, setGet)}</div>
        </div>
      </Section>
    </div>
  );
}

'''

TRADES_PANEL = r'''function TradesPanel(props) {
  // trades v10: analyzer and 2-for-1 merged into one builder (news_logos.py)
  return <TradeBuilder {...props} />;
}

'''

PLAYERS10 = r'''function Players({ s, wk }) {
  // players v10: no Signals column, phone list (news_logos.py)
  const K = s.blend;
  const [ft, setFt] = useState("all"); const [pos, setPos] = useState("all"); const [q, setQ] = useState(""); const [sort, setSort] = useState("week");
  const rows = s.players
    .filter((p) => (ft === "all" || p.ft === ft) && (pos === "all" || p.p === pos) && p.n.toLowerCase().includes(q.toLowerCase()))
    .map((p) => { const g = (wk.games[p.t] || []).filter((d) => !p.ir && avail(p, wk.dates ? wk.dates[d] : null)).length; const r = sigOf(p).rec; return { ...p, g, ea: effAvg(p, K), wkp: g * effAvg(p, K) * p.prob, rp: r ? r.ppg : null, rg: r ? r.gp : 0 }; })
    .sort((a, b) => (sort === "week" ? b.wkp - a.wkp : sort === "avg" ? b.ea - a.ea : sort === "hot" ? (b.rp || 0) - (a.rp || 0) : b.tot - a.tot)).slice(0, 300);
  const stTag = (p) => (p.ir ? "IR" : p.status && p.status !== "ACTIVE" ? M_ST[p.status] || p.status.replace(/_/g, " ") : "");
  return (
    <div className="space-y-3">
      <div className="flex flex-wrap gap-2">
        <input className={inp + " flex-1 min-w-[160px]"} placeholder="Search player" value={q} onChange={(e) => setQ(e.target.value)} />
        <select className={inp} value={ft} onChange={(e) => setFt(e.target.value)}><option value="all">All teams</option><option value="fa">Free agents</option>{s.teams.map((t) => <option key={t.id} value={t.id}>{t.name}</option>)}</select>
        <select className={inp} value={pos} onChange={(e) => setPos(e.target.value)}><option value="all">All positions</option><option>F</option><option>D</option><option>G</option></select>
        <select className={inp} value={sort} onChange={(e) => setSort(e.target.value)}><option value="week">Sort: this week</option><option value="avg">Sort: projected avg</option><option value="hot">Sort: last 14 days</option><option value="tot">Sort: season total</option></select>
      </div>
      <div className="m-hide bg-white rounded-xl border border-slate-200 overflow-x-auto">
        <table className="w-full text-sm">
          <thead className="text-left"><tr>{["Player", "", "Team", "Gms", "Avg", "Last 14d", "Season", "Week"].map((h, i) => <th key={i} className="px-3 py-2">{h}</th>)}</tr></thead>
          <tbody>
            {rows.map((p) => (
              <tr key={p.id} className={"border-t border-slate-100 " + (p.ft === s.me ? "bg-blue-50" : "")}>
                <td className="px-3 py-2"><PN p={p} />{stTag(p) ? <span className="text-red-600 text-xs ml-1">{stTag(p)}</span> : null}</td>
                <td className="px-3 py-2 text-xs text-slate-500 whitespace-nowrap">{p.p} · <TeamLogo t={p.t} /></td>
                <td className="px-3 py-2 text-xs text-slate-500"><TL s={s} id={p.ft} /></td>
                <td className="px-3 py-2">{p.g}</td><td className="px-3 py-2 font-semibold">{f1(p.ea)}</td>
                <td className="px-3 py-2">{p.rp !== null ? `${f1(p.rp)} (${p.rg})` : "–"}</td>
                <td className="px-3 py-2">{p.gp ? `${f1(p.tot)} (${p.gp})` : "–"}</td>
                <td className="px-3 py-2 font-semibold">{f1(p.wkp)}</td>
              </tr>
            ))}
          </tbody>
        </table>
        <div className="text-xs text-slate-500 p-3">Up to 300 shown — use the filters to narrow down.</div>
      </div>
      <div className="m-only bg-white rounded-xl border border-slate-200 px-3">
        <div className="m-ghead"><span>Player</span><span>Gms</span><span>Avg</span><span>Week</span></div>
        {rows.slice(0, 100).map((p) => { const tg = stTag(p); return (
          <div key={p.id} className="m-rrow" role="button" onClick={() => window.__NAV && window.__NAV.player(p)}>
            <TeamLogo t={p.t} size={26} />
            <div className="min-w-0">
              <div className={"truncate font-medium" + (p.ft === s.me ? " text-blue-600" : "")}>{p.n}</div>
              <div className="text-xs text-slate-500 truncate">{p.p} · {teamName(s, p.ft)}{tg ? <span className="text-red-600"> · {tg}</span> : null}</div>
            </div>
            <span className="m-num">{p.g}</span>
            <span className="m-num">{f1(p.ea)}</span>
            <span className="m-num font-semibold">{f1(p.wkp)}</span>
          </div>
        ); })}
        <div className="text-xs text-slate-500 py-3">Up to 100 shown — use the filters to narrow down.</div>
      </div>
    </div>
  );
}

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
    # --- round 3: big logos in Matchup and News ---
    t = block(t, "matchup rows with big logos", "function Side({ l, s, id }) {", "function MatchCard(", SIDE2, "matchup row layout v4")
    t = sub_once(t, "cleaner day difference",
                 re.escape('<div className="flex flex-wrap justify-between items-center gap-2 px-3 py-2.5 border-t border-slate-200 text-sm">') + r'.*?" ahead"\}</span>\s*</div>',
                 r'''<div data-v="daydiff2" className="flex justify-between items-center gap-3 px-3 py-3 border-t border-slate-200 font-semibold">
              <span>Difference</span>
              <span className="flex items-center gap-2">
                {x.total !== y.total ? <span className="text-sm text-slate-500 font-normal">{teamName(s, x.total > y.total ? a : b)} ahead</span> : null}
                <span className={"px-2.5 py-0.5 rounded-md " + (x.total - y.total >= 0 ? "bg-green-100 text-green-700" : "bg-red-100 text-red-600")}>{x.total - y.total >= 0 ? "+" : ""}{f1(x.total - y.total)}</span>
              </span>
            </div>''',
                 'data-v="daydiff2"', re.S)
    t = sub_once(t, "remove running total from day header",
                 r'<span>\{f1\(x\.total\)\} . \{f1\(y\.total\)\} . <span className=\{run >= 0[^\n]*?</span></span>',
                 "{/* day header: running total removed */}", "day header: running total removed")
    # --- round 4: win probability + how each move changes it ---
    t = lit(t, "win probability helpers", ROOT, WIN_HELPERS + ROOT, "function winChance(")
    t = sub_once(t, "matchup: win chance instead of Favoured/Coin flip",
                 r'<Card label=\{"Lean . " \+ teamName\(s, a\)\} value=\{[^\n]*?"Underdog"\}',
                 '<Card label={"Win chance · " + teamName(s, a)} value={final ? (margin > 0 ? "WIN" : margin < 0 ? "LOSS" : "TIE") : wpTxt(winProb(A, B, aA, aB))}',
                 'label={"Win chance · "')
    t = sub_once(t, "home: win chance",
                 r'projected\{Math\.abs\(margin\) < 15 \? "\s*.\s*close, every move matters" : ""\}',
                 "projected · {wpTxt(winProb(A, B, aA, aB))} chance to win", "chance to win</span>")
    t = lit(t, "home: moves change win chance",
            '<span className="text-green-700 font-semibold">+{f1(r.gain)}</span></Row>',
            '<WinDelta s={s} add={r.f} drop={r.d} /><span className="text-green-700 font-semibold">+{f1(r.gain)}</span></Row>',
            "<WinDelta s={s} add={r.f} drop={r.d} /><span")
    t = sub_once(t, "advice: moves change win chance",
                 r'<span className="text-green-700 font-semibold">\+\{f1\(r\.gain\)\}</span>(?=\s*<span className=\{"text-xs " \+ \(sd >= 0)',
                 '<WinDelta s={s} add={r.f} drop={r.d} advice={1} /><span className="text-green-700 font-semibold">+{f1(r.gain)}</span>',
                 "advice={1}")
    t = lit(t, "add/drop: win chance baseline",
            "const M = useMemo(() => computeMoves(s, { H, pos, q }), [s, H, pos, q]);",
            "const M = useMemo(() => computeMoves(s, { H, pos, q }), [s, H, pos, q]);\n  const wBase = useMemo(() => winChance(s), [s]);",
            "const wBase")
    t = lit(t, "add/drop: win column header",
            '{["Add", "", "Gms", "Avg", "Drop", "Gain", "Δ/game", "Advice", ""].map(',
            '{["Add", "", "Gms", "Avg", "Drop", "Gain", "Win this week", "Δ/game", "Advice", ""].map(',
            '"Gain", "Win this week"')
    t = lit(t, "add/drop: win column",
            '<td className={"px-3 py-2 font-semibold " + (r.gain > 0 ? "text-green-700" : "text-red-700")}>{r.gain >= 0 ? "+" : ""}{f1(r.gain)}</td>',
            '<td className={"px-3 py-2 font-semibold " + (r.gain > 0 ? "text-green-700" : "text-red-700")}>{r.gain >= 0 ? "+" : ""}{f1(r.gain)}</td><td className="px-3 py-2"><WinDelta s={s} add={r.f} drop={r.d} base={wBase} /></td>',
            "base={wBase} /></td>")
    t = lit(t, "add/drop: empty row width", "colSpan={9}>No moves clear", "colSpan={10}>No moves clear", "colSpan={10}>No moves clear")
    t = lit(t, "add/drop: simulator win chance", "{simBreaks && <span",
            "{A && D ? <WinDelta s={s} add={A} drop={D} base={wBase} /> : null}{simBreaks && <span", "base={wBase} /> : null}")
    # --- round 5: one clean footer per day: day difference + running total ---
    t = sub_once(t, "matchup: clean day footer",
                 r'<Side l=\{x\} s=\{s\} id=\{a\} /><Side l=\{y\} s=\{s\} id=\{b\} />.*?data-v="daydiff2".*?</span>\s*</span>\s*</div>',
                 r'''<Side l={x} s={s} id={a} /><Side l={y} s={s} id={b} />
            </div>
            <div data-v="daydiff2" data-w="daydiff3" className="border-t border-slate-200 px-3 py-2">
              {[["Day difference", x.total - y.total], ["Total so far", run]].map(([lab, v]) => (
                <div key={lab} className="flex justify-between items-center py-1.5 font-semibold">
                  <span>{lab}</span>
                  <span className="flex items-center gap-3">
                    <span className="text-sm text-slate-500 font-normal">{Math.abs(v) < 0.05 ? "even" : (v > 0 ? teamName(s, a) : teamName(s, b)) + " ahead"}</span>
                    <span className={"min-w-[64px] text-center px-2.5 py-0.5 rounded-md " + (v >= 0 ? "bg-green-100 text-green-700" : "bg-red-100 text-red-600")}>{v >= 0 ? "+" : ""}{f1(v)}</span>
                  </span>
                </div>
              ))}
            </div>''',
                 'data-w="daydiff3"', re.S)
    # --- round 6: games/moves left, win chance on every card, fill empty spots, ESPN lineup check, goalie streams, strategy ---
    t = lit(t, "round 6 helpers", ROOT, R6_HELPERS + ROOT, "function GoalieStreams(")
    t = lit(t, "matchup: games and moves left (you)", CARD_A_OLD, CARD_A_NEW, "gamesMoves(s, a, wk, A)")
    t = lit(t, "matchup: games and moves left (them)", CARD_B_OLD, CARD_B_NEW, "gamesMoves(s, b, wk, B)")
    t = lit(t, "matchup cards: win chance", BAR_OLD, BAR_NEW, "to win</span><span>")
    t = lit(t, "matchup: pass the day to each side", "<Side l={x} s={s} id={a} /><Side l={y} s={s} id={b} />",
            "<Side l={x} s={s} id={a} wk={wk} d={d} /><Side l={y} s={s} id={b} wk={wk} d={d} />", "wk={wk} d={d} />")
    t = lit(t, "matchup: side knows the day", "function Side({ l, s, id }) {", "function Side({ l, s, id, wk, d }) {", "function Side({ l, s, id, wk, d })")
    t = lit(t, "matchup: fill empty spots", EMPTY_OLD, EMPTY_OLD + "\n      {wk && id === s.me ? <FillSlot l={l} s={s} wk={wk} d={d} /> : null}", "<FillSlot")
    t = sub_once(t, "home: ESPN lineup check", r'(?<=a streamer could fill \$\{L\.empty > 1 \? "them" : "it"\}`\]\);)',
                 ' espnLineupChecks(mine, L, wk, di, dday, today).forEach((c) => (c[0] === "bad" ? checks.unshift(c) : checks.push(c)));',
                 "espnLineupChecks(mine")
    t = lit(t, "home: safe or risky advice", "chance to win</span></div>",
            "chance to win</span></div>{done < dates.length ? <StrategyLine p={winProb(A, B, aA, aB)} /> : null}", "<StrategyLine")
    t = lit(t, "moves: goalie streams tab", '["planner", "Planner"], ["adddrop", "Add / Drop"]',
            '["planner", "Planner"], ["goalies", "Goalie streams"], ["adddrop", "Add / Drop"]', '["goalies", "Goalie streams"]')
    t = lit(t, "moves: goalie streams page", 'sub === "planner" ? <PlannerAll {...P} /> :',
            'sub === "planner" ? <PlannerAll {...P} /> : sub === "goalies" ? <GoalieStreams {...P} /> :', "<GoalieStreams {...P} />")
    # --- round 7: moves used filled in from ESPN ---
    t = lit(t, "moves used from ESPN (helper)", ROOT,
            r'''// ---------- moves used from ESPN (news_logos.py) ----------
function movesUsedESPN(s, w) {
  const E = window.ESPN_DATA || {};
  if (!E.acq || !w || w.period == null) return null;
  const a = E.acq[String(s.me).replace(/^t/, "")];
  return a ? (+a[String(w.period)] || 0) : null;
}

''' + ROOT, "function movesUsedESPN(")
    t = lit(t, "planner: moves used from ESPN", "const used = ((s.movesUsed || {})[s.wk]) || 0;",
            "const espnUsed = movesUsedESPN(s, wk); const used = espnUsed != null ? espnUsed : ((s.movesUsed || {})[s.wk]) || 0;",
            "const espnUsed = movesUsedESPN(s, wk);")
    t = lit(t, "planner: show ESPN count instead of the menu",
            r'''<label>Moves already used this week <select className={inp} value={used} onChange={(e) => setUsed(+e.target.value)}>{[0, 1, 2, 3].map((n) => <option key={n} value={n}>{n}</option>)}</select></label>''',
            r'''{espnUsed != null ? <span>Moves used this week: <b>{used} of 3</b> <span className="text-xs text-slate-500">from ESPN</span></span> : <label>Moves already used this week <select className={inp} value={used} onChange={(e) => setUsed(+e.target.value)}>{[0, 1, 2, 3].map((n) => <option key={n} value={n}>{n}</option>)}</select></label>}''',
            "{espnUsed != null ? <span>Moves used this week")
    t = lit(t, "planner: note under the plan", 'Set "moves already used" after each one.',
            '''{espnUsed != null ? "Your moves count updates from ESPN at the next sync." : 'Set "moves already used" after each one.'}''',
            "Your moves count updates from ESPN at the next sync.")
    # --- round 8: give the Lines tab access to team logos ---
    t = lit(t, "lines tab can use logos", "todayISO, dayLabel, TL };", "todayISO, dayLabel, TL, TeamLogo };", "dayLabel, TL, TeamLogo };")
    t = sub_once(t, "bigger logos in News", r'<div className="pt-0\.5"><TeamLogo t=\{p\.t\} size=\{\d+\} /></div>',
                 '<div className="pt-0.5"><TeamLogo t={p.t} size={36} /></div>', '<TeamLogo t={p.t} size={36} /></div>')
    # --- round 9: phone layout (ESPN-style header and tabs, head-to-head Matchup, clean rosters, no Signals column) ---
    t = lit(t, "phone: styles", "</style>", R9_CSS + "</style>", "round 9 mobile")
    t = lit(t, "phone: helpers", ROOT, R9_HELPERS + ROOT, "function MobileHeader(")
    t = lit(t, "phone: header", '<div className="max-w-6xl mx-auto px-3 pt-2 pb-1 flex flex-wrap items-center gap-2">',
            '<MobileHeader s={s} setS={setS} tab={tab} go={go} ageH={ageH} />\n        <div className="m-hide max-w-6xl mx-auto px-3 pt-2 pb-1 flex flex-wrap items-center gap-2">',
            "<MobileHeader s={s}")
    t = lit(t, "phone: hide desktop tabs", '<div className="max-w-6xl mx-auto px-2 flex gap-1 overflow-x-auto navscroll">',
            '<div className="m-hide max-w-6xl mx-auto px-2 flex gap-1 overflow-x-auto navscroll">', "m-hide max-w-6xl mx-auto px-2")
    t = lit(t, "phone: head-to-head matchup", '<div className="grid grid-cols-1 md:grid-cols-2 divide-y md:divide-y-0 md:divide-x divide-slate-200">',
            '<div className="m-only"><H2H x={x} y={y} s={s} a={a} b={b} wk={wk} d={d} /></div>\n            <div className="m-hide grid grid-cols-1 md:grid-cols-2 divide-y md:divide-y-0 md:divide-x divide-slate-200">',
            "<H2H x={x}")
    t = block(t, "rosters: no Signals column + phone list", "function RosterView({ s, wk, team }) {", "function MyTeam(", ROSTERVIEW, "roster view v9")
    # --- round 10: Lines gets its own phone tab, cleaner Players list, one trade builder ---
    t = lit(t, "phone: Lines tab", 'const M_TABS = [["today", "Today"], ["matchup", "Matchup"], ["myteam", "My Team"], ["moves", "Moves"]];',
            'const M_TABS = [["today", "Today"], ["matchup", "Matchup"], ["myteam", "My Team"], ["moves", "Moves"], ["lines", "Lines"]];', '["lines", "Lines"]];')
    t = lit(t, "phone: Lines out of More", 'const M_MORE = [["teams", "Teams"], ["lines", "Lines"], ["league", "League"], ["news", "News"], ["setup", "Setup"]];',
            'const M_MORE = [["teams", "Teams"], ["league", "League"], ["news", "News"], ["setup", "Setup"]];', 'const M_MORE = [["teams", "Teams"], ["league"')
    t = lit(t, "phone: six tabs", '<div className="grid grid-cols-5 mt-1">', '<div className="grid grid-cols-6 mt-1">', "grid grid-cols-6 mt-1")
    t = lit(t, "trade builder styles", "</style>", R10_CSS + "</style>", "round 10 trades")
    t = lit(t, "trade builder", ROOT, R10_HELPERS + ROOT, "function TradeBuilder(")
    t = block(t, "trades: one builder", "function TradesPanel(props) {", "// ---------- Phone notifications feed", TRADES_PANEL, "trades v10")
    t = block(t, "players: no Signals column + phone list", "function Players({ s, wk }) {", "// ---------- Setup ----------", PLAYERS10, "players v10")
    for must in (ROOT, "const SR = {", DONE, "function Side(", "function NewsView({ s, wk })", "function Matchup(", "function Today(", "function MobileHeader(", "function RosterView(", "function TradeBuilder("):
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
        for f, bk in PY_BAK.items():
            if pathlib.Path(bk).exists():
                pathlib.Path(f).write_text(pathlib.Path(bk).read_text(encoding="utf-8"), encoding="utf-8")
                print(f"(news) restored {f} from {bk}")
        return
    if mode not in ("test", "live"):
        fail("mode must be test, live, undo or games")
    p = pathlib.Path(SRC)
    if not p.exists():
        fail(f"{SRC} is missing from the repo")
    old = p.read_text(encoding="utf-8")
    new = fix(old)
    jsx_check(new)
    py = {}
    for f, fn in {**PY_FIXES, **JS_FIXES}.items():
        fp = pathlib.Path(f)
        if not fp.exists():
            print(f"(news) {f} not found - skipped")
            continue
        print(f"--- {f}")
        before = fp.read_text(encoding="utf-8")
        py[f] = (before, fn(before))
    if mode == "test":
        pathlib.Path(TEST).write_text(new, encoding="utf-8")
        print(f"(news) test copy written - open {TEST} to check")
        print("(news) Python changes checked (no errors) - they are only applied in live mode")
    else:
        if DONE not in old:
            pathlib.Path(BAK).write_text(old, encoding="utf-8")
            print(f"(news) backup saved: {BAK}")
        p.write_text(new, encoding="utf-8")
        print("(news) live app updated")
        for f, (before, after) in py.items():
            if after == before:
                continue
            if PY_DONE[f] not in before:
                pathlib.Path(PY_BAK[f]).write_text(before, encoding="utf-8")
                print(f"(news) backup saved: {PY_BAK[f]}")
            pathlib.Path(f).write_text(after, encoding="utf-8")
            print(f"(news) {f} updated")


# ---------- round 11: cleaner Add / Drop with a pop-up move simulator ----------
R11_CSS = r'''  /* round 11 add/drop (news_logos.py) */
  .ms-card { background: var(--card); border: 1px solid var(--line2); border-radius: 14px; width: 100%; max-width: 680px; padding: 18px; margin: auto 0; }
  .ms-move { border: 1px solid var(--line); border-radius: 12px; padding: 12px; margin-bottom: 10px; }
  .ms-pick { display: flex; align-items: center; gap: 10px; border: 1px solid var(--line2); border-radius: 8px; padding: 6px 10px; min-height: 42px; }
  .ms-list { position: absolute; left: 0; right: 0; top: calc(100% + 4px); z-index: 60; background: #202020; border: 1px solid var(--line2); border-radius: 10px; padding: 4px; max-height: 300px; overflow-y: auto; }
  .ms-opt { display: flex; align-items: center; gap: 8px; width: 100%; padding: 8px; border-radius: 8px; color: var(--ink); }
  .ms-opt:hover { background: var(--accentSoft); }
  .ms-res { border-top: 1px solid var(--line); margin-top: 14px; padding-top: 14px; }
  @media (max-width: 640px) { .ms-card { padding: 14px; } .ms-move .tb-grid { grid-template-columns: minmax(0,1fr); } }
'''

ADDDROP11 = r'''const shortTag = (p, K) => { const t = tags(p, K)[0]; if (!t) return null; const x = t.u ? t.t.split(":")[0] : t.t; return { t: x.length > 20 ? x.slice(0, 19) + "…" : x, c: t.c }; };
const cntOf = (r) => { const c = { F: 0, D: 0, G: 0 }; r.forEach((p) => { if (!p.ir) c[p.p]++; }); return c; };
const WinCell = ({ s, add, drop, base }) => {
  if (base == null) return null;
  const n = winChance(s, afterMove(s, add, drop));
  if (n == null) return null;
  const d = Math.round(n * 100) - Math.round(base * 100);
  return <span className="whitespace-nowrap"><span className="font-medium">{wpTxt(n)}</span> <span className={"text-xs " + (d > 0 ? "text-green-700" : d < 0 ? "text-red-600" : "text-slate-500")}>{d > 0 ? "+" : ""}{d}</span></span>;
};
function AddDrop({ s, setS, wk }) {
  // add/drop v11: one drop on top, cleaner rows, pop-up simulator (news_logos.py)
  const [H, setH] = useState(1);
  const [pos, setPos] = useState("sk"); const [q, setQ] = useState(""); const [limit, setLimit] = useState(25);
  const [dropSel, setDropSel] = useState("");
  const [sim, setSim] = useState(null);
  const [showSet, setShowSet] = useState(false);
  const M = useMemo(() => computeMoves(s, { H, pos, q }), [s, H, pos, q]);
  const wBase = useMemo(() => winChance(s), [s]);
  const { res, total, gamesIn, rawPts, autoProt, protectedIds, cnt, mins, keepsMins, lineupAware, myR, K, gw, protectTop } = M;
  const minGain = s.minGain ?? 3;
  const num = (k, v, fb) => setS((st) => ({ ...st, [k]: isNaN(parseFloat(v)) ? fb : parseFloat(v) }));
  const hLabel = { 1: "rest of this week", 2: "this week + next", 4: "next 4 weeks", 0: "rest of season" }[H];
  const forced = myR.find((p) => p.id === dropSel && !p.ir) || null;
  const rows = useMemo(() => {
    if (!forced) return res;
    const base = lineupAware ? total(myR) : 0;
    return res.filter((r) => keepsMins(forced, r.f)).map((r) => ({ ...r, d: forced, gain: lineupAware ? total(myR.filter((x) => x.id !== forced.id).concat([{ ...r.f, ft: s.me }])) - base : rawPts(r.f) - rawPts(forced) })).sort((a, b) => b.gain - a.gain);
  }, [M, dropSel]);
  const worth = rows.filter((r) => r.gain >= minGain);
  const shown = worth.slice(0, limit === 0 ? 9999 : limit);
  const tally = {}; shown.forEach((r) => { tally[r.d.id] = (tally[r.d.id] || 0) + 1; });
  const topId = Object.keys(tally).sort((a, b) => tally[b] - tally[a])[0];
  const common = forced || myR.find((p) => p.id === topId) || null;
  const mixed = !forced && Object.keys(tally).length > 1;
  const dropList = myR.filter((p) => !p.ir).sort((a, b) => effAvg(a, K) - effAvg(b, K));
  const toggleKeep = (id, v) => setS((st) => ({ ...st, players: st.players.map((p) => (p.id === id ? { ...p, keep: v } : p)) }));
  const stOf = (p) => (p.status && p.status !== "ACTIVE" ? M_ST[p.status] || p.status.replace(/_/g, " ") : "");
  const tabs = [["sk", "All skaters"], ["F", "Forwards"], ["D", "Defense"], ["G", "Goalies"], ["pp1", "On PP1"], ["all", "Everyone"]];
  return (
    <div className="space-y-4">
      <Section title="Add / Drop" sub={`${worth.length} pickups worth ${minGain}+ pts · ${lineupAware ? "lineup-aware" : "quick estimate"}`} link={[showSet ? "Hide settings" : "Settings & protected players", () => setShowSet(!showSet)]}>
        <div className="flex flex-wrap gap-2 items-center">
          <select className={inp} value={H} onChange={(e) => setH(+e.target.value)}><option value={1}>Rest of this week</option><option value={2}>This week + next</option><option value={4}>Next 4 weeks</option><option value={0}>Rest of season</option></select>
          <input className={inp + " flex-1 min-w-[140px]"} placeholder="Search free agents" value={q} onChange={(e) => setQ(e.target.value)} />
          <select className={inp} value={limit} onChange={(e) => setLimit(+e.target.value)}><option value={25}>Show 25</option><option value={50}>Show 50</option><option value={100}>Show 100</option><option value={0}>Show all</option></select>
          <button className="bg-blue-600 rounded-lg px-4 py-1.5 font-semibold" onClick={() => setSim({})}>Build a move</button>
        </div>
        {showSet && (
          <div className="mt-3 pt-3 border-t border-slate-200 space-y-3">
            <div className="flex flex-wrap gap-3 items-center">
              <span className="font-medium">Minimums</span>
              <label>F <input type="number" className={inp + " w-14"} value={mins.F} onChange={(e) => num("minF", e.target.value, 10)} /></label>
              <label>D <input type="number" className={inp + " w-14"} value={mins.D} onChange={(e) => num("minD", e.target.value, 5)} /></label>
              <label>G <input type="number" className={inp + " w-14"} value={mins.G} onChange={(e) => num("minGo", e.target.value, 2)} /></label>
              <span className={"text-xs " + (cnt.F < mins.F || cnt.D < mins.D || cnt.G < mins.G ? "text-red-600 font-semibold" : "text-slate-500")}>You have F {cnt.F} · D {cnt.D} · G {cnt.G}</span>
            </div>
            <div className="flex flex-wrap gap-3 items-center">
              <label>Goalie value × <input type="number" step="0.1" className={inp + " w-16"} value={gw} onChange={(e) => num("gw", e.target.value, 1.3)} /></label>
              <label>Auto-protect top <input type="number" className={inp + " w-14"} value={protectTop} onChange={(e) => num("protectTop", e.target.value, 8)} /></label>
              <label>Min gain <input type="number" step="0.5" className={inp + " w-16"} value={minGain} onChange={(e) => num("minGain", e.target.value, 3)} /> pts</label>
            </div>
            <div>
              <div className="text-xs text-slate-500 mb-1">Protected players (never suggested as drops):</div>
              <div className="flex flex-wrap gap-2">
                {myR.map((p) => { const auto = autoProt.has(p.id), prot = protectedIds.has(p.id); return (
                  <label key={p.id} className={"flex items-center gap-1 px-2 py-1 rounded-full border text-xs " + (p.ir ? "text-slate-400 border-slate-200" : prot ? "bg-green-50 border-green-300" : "border-slate-300")}>
                    <input type="checkbox" disabled={p.ir || auto} checked={p.ir || prot} onChange={(e) => toggleKeep(p.id, e.target.checked)} />{p.n}{p.ir ? " (IR)" : auto ? " (auto)" : ""}
                  </label>
                ); })}
              </div>
            </div>
          </div>
        )}
      </Section>
      <div className="bg-white rounded-xl border border-slate-200 overflow-x-auto">
        <div className="p-3 border-b border-slate-200"><Pills items={tabs} value={pos} onChange={setPos} /></div>
        <div className="flex flex-wrap items-center gap-2 px-3 py-2.5 border-b border-slate-200 text-sm">
          <span className="text-slate-500">Dropping</span>
          {common ? <span className="inline-flex items-center gap-1.5 font-semibold"><TeamLogo t={common.t} size={22} />{common.n}<span className="text-xs text-slate-500 font-normal">{common.p}</span></span> : <span className="text-slate-400">nobody yet</span>}
          <span className="text-xs text-slate-500">{forced ? "your choice" : mixed ? "for most pickups, others shown on the row" : "suggested"}</span>
          <select className={inp + " ml-auto"} value={dropSel} onChange={(e) => setDropSel(e.target.value)}>
            <option value="">Change drop: best for each (auto)</option>
            {dropList.map((p) => <option key={p.id} value={p.id}>Drop {p.n} ({p.p}) · {f1(effAvg(p, K))}/g{protectedIds.has(p.id) ? " · protected" : ""}</option>)}
          </select>
        </div>
        <table className="w-full text-sm">
          <thead className="text-left"><tr>
            <th className="px-3 py-2">Add</th>
            <th className="px-3 py-2 m-hide">Gms</th>
            <th className="px-3 py-2 m-hide">Avg</th>
            <th className="px-3 py-2">Gain</th>
            <th className="px-3 py-2 whitespace-nowrap">Win · now {wBase == null ? "–" : wpTxt(wBase)}</th>
            <th className="px-3 py-2">Advice</th>
            <th className="px-3 py-2"></th>
          </tr></thead>
          <tbody>
            {shown.map((r) => { const sd = effAvg(r.f, K) - effAvg(r.d, K); const [v, c] = verdict(r.gain, sd); const tg = shortTag(r.f, K); const st = stOf(r.f); return (
              <tr key={r.f.id} className="border-t border-slate-100">
                <td className="px-3 py-2.5">
                  <div className="flex items-center gap-2.5">
                    <TeamLogo t={r.f.t} size={26} />
                    <div className="min-w-0">
                      <div className="flex items-center gap-2 whitespace-nowrap"><PN p={r.f} /><span className="text-xs text-slate-500">{r.f.p}</span>{st ? <span className="text-xs text-red-600">{st}</span> : null}</div>
                      {common && r.d.id !== common.id ? <div className="text-xs text-slate-500">drops {r.d.n}</div> : null}
                    </div>
                  </div>
                </td>
                <td className="px-3 py-2.5 m-hide">{gamesIn(r.f)}</td>
                <td className="px-3 py-2.5 m-hide">{f1(effAvg(r.f, K))}</td>
                <td className={"px-3 py-2.5 font-semibold " + (r.gain > 0 ? "text-green-700" : "text-red-600")}>{r.gain >= 0 ? "+" : ""}{f1(r.gain)}</td>
                <td className="px-3 py-2.5"><WinCell s={s} add={r.f} drop={r.d} base={wBase} /></td>
                <td className="px-3 py-2.5 whitespace-nowrap"><span className={"text-xs px-2 py-0.5 rounded " + c}>{v}</span>{tg ? <span className={"text-xs ml-2 " + tg.c}>{tg.t}</span> : null}</td>
                <td className="px-3 py-2.5 text-right"><button className="text-blue-600 text-sm" onClick={() => setSim({ add: r.f.id, drop: r.d.id })}>Simulate</button></td>
              </tr>
            ); })}
            {shown.length === 0 && <tr><td className="px-3 py-4 text-slate-400" colSpan={7}>No pickups clear your minimum gain for this position and window{forced ? " with this drop" : ""}.</td></tr>}
          </tbody>
        </table>
      </div>
      <div className="text-xs text-slate-500">Gain = extra projected points in your daily lineups ({hLabel}). Win = your chance to win this week after the move, with the change next to it. Stream only = helps now but is a worse player long-term.</div>
      {sim ? <MoveSim s={s} setS={setS} wk={wk} M={M} H={H} hLabel={hLabel} init={sim} wBase={wBase} onClose={() => setSim(null)} /> : null}
    </div>
  );
}
function MoveSim({ s, setS, wk, M, H, hLabel, init, wBase, onClose }) {
  const { total, rawPts, gamesIn, protectedIds, mins, lineupAware, myR, fas, K } = M;
  const left = movesLeft(s, s.me, wk);
  const cap = Math.max(1, left == null ? 3 : left);
  const [moves, setMoves] = useState([{ add: init.add || "", drop: init.drop || "", sug: init.drop || "" }]);
  const [qs, setQs] = useState({});
  const [openI, setOpenI] = useState(init.add ? -1 : 0);
  const [focus, setFocus] = useState(0);
  useEffect(() => {
    const k = (e) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", k); document.body.style.overflow = "hidden";
    return () => { window.removeEventListener("keydown", k); document.body.style.overflow = ""; };
  }, []);
  const byId = (id) => (id ? s.players.find((p) => p.id === id) || null : null);
  const rosterBefore = (i, ms) => { let r = myR; (ms || moves).slice(0, i).forEach((m) => { const a = byId(m.add); if (a && r.some((x) => x.id === m.drop)) r = r.filter((x) => x.id !== m.drop).concat([{ ...a, ft: s.me }]); }); return r; };
  const suggestDrop = (i, f, ms) => {
    const r = rosterBefore(i, ms), c = cntOf(r);
    const ok = (d) => !d.ir && (d.p === f.p || c[d.p] - 1 >= mins[d.p]);
    let cands = r.filter((d) => ok(d) && !protectedIds.has(d.id));
    if (!cands.length) cands = r.filter(ok);
    const b = lineupAware ? total(r) : 0;
    let best = null;
    cands.forEach((d) => { const g = lineupAware ? total(r.filter((x) => x.id !== d.id).concat([{ ...f, ft: s.me }])) - b : rawPts(f) - rawPts(d); if (!best || g > best.g) best = { d, g }; });
    return best ? best.d.id : "";
  };
  const setAdd = (i, id) => {
    const f = byId(id);
    setMoves((ms) => ms.map((m, k) => { if (k !== i) return m; const sug = f ? suggestDrop(i, f, ms) : ""; return { add: id, drop: sug, sug }; }));
    setQs((x) => ({ ...x, [i]: "" })); setOpenI(-1); setFocus(i);
  };
  const setDrop = (i, id) => setMoves((ms) => ms.map((m, k) => (k === i ? { ...m, drop: id } : m)));
  const addMove = () => { const n = moves.length; setMoves((ms) => ms.concat([{ add: "", drop: "", sug: "" }])); setOpenI(n); setFocus(n); };
  const removeMove = (i) => { setMoves((ms) => ms.filter((_, k) => k !== i)); setFocus(0); setOpenI(-1); };
  const matches = (i) => {
    const q = nrm(qs[i] || ""), used = new Set(moves.filter((_, k) => k !== i).map((m) => m.add));
    if (!q) return M.res.filter((r) => !used.has(r.f.id)).slice(0, 6).map((r) => r.f);
    return fas.filter((p) => p.prob > 0 && !used.has(p.id) && nrm(p.n).includes(q)).sort((a, b) => effAvg(b, K) - effAvg(a, K)).slice(0, 8);
  };
  const key = JSON.stringify(moves.map((m) => [m.add, m.drop]));
  const R = useMemo(() => {
    const list = moves.map((m, i) => { const a = byId(m.add), r = rosterBefore(i); const d = r.find((x) => x.id === m.drop) || null; return a && d ? { a, d } : null; });
    const ok = list.filter(Boolean);
    if (!ok.length) return { list, ok };
    const after = rosterBefore(moves.length);
    const gain = lineupAware ? total(after) - total(myR) : ok.reduce((t, x) => t + rawPts(x.a) - rawPts(x.d), 0);
    const c = cntOf(after);
    return { list, ok, after, gain, c, win: winChance(s, after), short: ["F", "D", "G"].filter((k) => c[k] < mins[k]) };
  }, [key]);
  const addF = byId((moves[focus] || {}).add);
  const alts = useMemo(() => (addF ? computeMoves(s, { H, pos: addF.p, pool: 40 }).res.filter((r) => r.f.id !== addF.id && !moves.some((m) => m.add === r.f.id)).slice(0, 3) : []), [addF ? addF.id : "", H]);
  const apply = () => {
    const drops = new Set(R.ok.map((x) => x.d.id)), adds = new Set(R.ok.map((x) => x.a.id));
    setS((st) => ({ ...st, players: st.players.map((p) => (drops.has(p.id) ? { ...p, ft: "fa", ir: false } : adds.has(p.id) ? { ...p, ft: st.me } : p)) }));
    onClose();
  };
  const before = cntOf(myR);
  const posName = { F: "forwards", D: "defencemen", G: "goalies" };
  return (
    <div className="fixed inset-0 z-50 flex items-start justify-center p-3 sm:p-6 overflow-y-auto" style={{ background: "rgba(0,0,0,.65)" }} onClick={onClose}>
      <div className="ms-card" onClick={(e) => e.stopPropagation()}>
        <div className="flex items-start gap-3 mb-3">
          <div>
            <div className="font-semibold text-base">Simulate a move</div>
            <div className="text-xs text-slate-500">Points: {hLabel} · win chance: this week{left != null ? ` · ${left} move${left === 1 ? "" : "s"} left this week` : ""}</div>
          </div>
          <button className="ml-auto text-2xl leading-none text-slate-500" aria-label="Close" onClick={onClose}>×</button>
        </div>
        {moves.map((m, i) => {
          const a = byId(m.add), r = rosterBefore(i), it = R.list[i];
          const drops = r.filter((p) => !p.ir).sort((x, y) => effAvg(x, K) - effAvg(y, K));
          const sd = it ? effAvg(it.a, K) - effAvg(it.d, K) : 0;
          const ml = openI === i ? matches(i) : [];
          return (
            <div key={i} className="ms-move" onClick={() => setFocus(i)}>
              {moves.length > 1 ? <div className="flex items-center mb-2"><span className="text-xs uppercase tracking-wide text-slate-500">Move {i + 1}</span><button className="ml-auto text-xs text-slate-500" onClick={(e) => { e.stopPropagation(); removeMove(i); }}>Remove</button></div> : null}
              <div className="tb-grid">
                <div className="min-w-0">
                  <div className="text-xs text-slate-500 mb-1">Add</div>
                  {a && openI !== i ? (
                    <div className="ms-pick">
                      <TeamLogo t={a.t} size={26} />
                      <div className="min-w-0 flex-1"><div className="truncate font-medium">{a.n}</div><div className="text-xs text-slate-500">{a.p} · {gamesIn(a)} gms · {f1(effAvg(a, K))}/g</div></div>
                      <button className="text-xs text-blue-600" onClick={() => setOpenI(i)}>Change</button>
                    </div>
                  ) : (
                    <div className="relative">
                      <input className={inp + " w-full"} autoFocus={openI === i} placeholder="Type a free agent's name" value={qs[i] || ""}
                        onChange={(e) => { setQs({ ...qs, [i]: e.target.value }); setOpenI(i); }} onFocus={() => setOpenI(i)}
                        onBlur={() => setTimeout(() => setOpenI((x) => (x === i ? -1 : x)), 150)} />
                      {openI === i ? (
                        <div className="ms-list">
                          {!(qs[i] || "").trim() ? <div className="text-xs text-slate-500 px-2 pt-1 pb-1">Top pickups</div> : null}
                          {ml.map((p) => (
                            <button key={p.id} type="button" className="ms-opt" onMouseDown={(e) => e.preventDefault()} onClick={() => setAdd(i, p.id)}>
                              <TeamLogo t={p.t} size={22} />
                              <span className="truncate flex-1 text-left">{p.n} <span className="text-xs text-slate-500">{p.p}</span></span>
                              <span className="text-xs text-slate-500 whitespace-nowrap">{gamesIn(p)} gms · {f1(effAvg(p, K))}</span>
                            </button>
                          ))}
                          {ml.length === 0 ? <div className="text-sm text-slate-400 px-2 py-2">No free agent matches.</div> : null}
                          {a ? <button type="button" className="text-xs text-slate-500 px-2 py-1" onMouseDown={(e) => e.preventDefault()} onClick={() => setOpenI(-1)}>Keep {a.n}</button> : null}
                        </div>
                      ) : null}
                    </div>
                  )}
                </div>
                <div className="min-w-0">
                  <div className="text-xs text-slate-500 mb-1">Drop{m.drop && m.drop === m.sug ? " · suggested" : ""}</div>
                  <select className={inp + " w-full"} value={m.drop} onChange={(e) => setDrop(i, e.target.value)}>
                    <option value="">Choose who to drop</option>
                    {drops.map((p) => <option key={p.id} value={p.id}>{p.n} ({p.p}) · {f1(effAvg(p, K))}/g{protectedIds.has(p.id) ? " · protected" : ""}</option>)}
                  </select>
                </div>
              </div>
              {it ? (
                <div className={"text-xs mt-2 " + (sd >= 0 ? "text-green-700" : "text-amber-600")}>
                  {sd >= 0 ? `Keeper: ${f1(sd)}/game better than ${it.d.n} long-term` : `Stream only: ${f1(-sd)}/game worse than ${it.d.n} long-term`}{protectedIds.has(it.d.id) ? ` · ${it.d.n} is protected` : ""}
                </div>
              ) : a && m.drop && !r.some((x) => x.id === m.drop) ? <div className="text-xs mt-2 text-red-600">That player is already dropped in an earlier move. Choose another drop.</div> : null}
            </div>
          );
        })}
        {addF && alts.length ? (
          <div className="mt-3">
            <div className="text-xs uppercase tracking-wide text-slate-500 mb-1">Other {posName[addF.p]} to consider</div>
            {alts.map((r) => (
              <div key={r.f.id} className="flex items-center gap-2.5 py-2 border-t border-slate-100">
                <TeamLogo t={r.f.t} size={22} />
                <div className="min-w-0 flex-1"><div className="truncate">{r.f.n}</div><div className="text-xs text-slate-500">{gamesIn(r.f)} gms · {f1(effAvg(r.f, K))}/g · drop {r.d.n}</div></div>
                <span className="text-green-700 font-semibold text-sm">+{f1(r.gain)}</span>
                <button className="text-xs text-blue-600" onClick={() => setAdd(focus, r.f.id)}>Use</button>
              </div>
            ))}
          </div>
        ) : null}
        {moves.length < cap ? <button className="text-sm text-blue-600 mt-3" onClick={addMove}>+ Add another move</button>
          : <div className="text-xs text-slate-500 mt-3">{left === 0 ? "No moves left this week on ESPN, so this is only a what-if." : `That's all ${cap} of your moves left this week.`}</div>}
        <div className="ms-res">
          {R.ok.length ? (
            <div>
              <div className="grid grid-cols-3 gap-2 text-center">
                <div><div className="text-xs text-slate-500">Points</div><div className="text-xl"><Dlt v={R.gain} /></div><div className="text-xs text-slate-500">{hLabel}</div></div>
                <div><div className="text-xs text-slate-500">Win this week</div><div className={"text-xl font-semibold " + (R.win != null && wBase != null ? (R.win > wBase ? "text-green-700" : R.win < wBase ? "text-red-600" : "") : "")}>{R.win == null ? "–" : wpTxt(R.win)}</div><div className="text-xs text-slate-500">now {wBase == null ? "–" : wpTxt(wBase)}</div></div>
                <div><div className="text-xs text-slate-500">Roster after</div><div className="text-sm font-semibold mt-1">F {R.c.F} · D {R.c.D} · G {R.c.G}</div><div className="text-xs text-slate-500">was F {before.F} · D {before.D} · G {before.G}</div></div>
              </div>
              {R.short.length ? <div className="text-sm text-red-600 mt-2">Below your minimum at {R.short.join(", ")}. Pick a different drop.</div> : null}
              <div className="flex flex-wrap items-center gap-3 mt-3">
                <button className="bg-blue-600 rounded-lg px-4 py-1.5 font-semibold" onClick={apply}>Apply here</button>
                <span className="text-xs text-slate-500">Updates this app only. Make the real move on ESPN; the next sync confirms it.</span>
              </div>
            </div>
          ) : <div className="text-sm text-slate-400">Pick a player to add and one to drop to see the result.</div>}
        </div>
      </div>
    </div>
  );
}

'''


def round11(t):
    t = lit(t, "add/drop styles", "</style>", R11_CSS + "</style>", "round 11 add/drop")
    t = block(t, "add/drop: cleaner table + pop-up simulator", "function AddDrop({ s, setS }) {",
              "// ---------- Players ----------", ADDDROP11, "add/drop v11")
    for must in ("function MoveSim(", "function AddDrop({ s, setS, wk })", "// ---------- Players ----------"):
        if must not in t:
            fail("fantasy-gm.html looks damaged after round 11 (" + must + ").")
    return t


_fix_before_r11 = fix


def fix(t):
    return round11(_fix_before_r11(t))

# ---------- round 12: short colour dot instead of the advice pill ----------
R12_DOT = 'style={{ display: "inline-block", width: 10, height: 10, borderRadius: 99, marginRight: 5, background: "%s" }}'
R12_CELL_OLD = r'''<td className="px-3 py-2.5 whitespace-nowrap"><span className={"text-xs px-2 py-0.5 rounded " + c}>{v}</span>{tg ? <span className={"text-xs ml-2 " + tg.c}>{tg.t}</span> : null}</td>'''
R12_CELL_NEW = r'''<td className="px-3 py-2.5" data-keep="dot"><span title={v} style={{ display: "inline-block", width: 12, height: 12, borderRadius: 99, background: v === "Add & keep" ? "var(--good)" : v === "Stream only" ? "var(--warn)" : "var(--bad)" }}></span></td>'''
R12_NAME_OLD = r'''<span className="text-xs text-slate-500">{r.f.p}</span>{st ? <span className="text-xs text-red-600">{st}</span> : null}</div>'''
R12_NAME_NEW = r'''<span className="text-xs text-slate-500">{r.f.p}</span>{st ? <span className="text-xs text-red-600">{st}</span> : null}{tg ? <span className={"text-xs " + tg.c}>{tg.t}</span> : null}</div>'''
R12_FOOT_OLD = r'''Stream only = helps now but is a worse player long-term.</div>'''
R12_FOOT_NEW = ('<span data-keep="legend">Keep: </span>'
                '<span className="whitespace-nowrap"><span ' + R12_DOT % "var(--good)" + '></span>add and keep</span> · '
                '<span className="whitespace-nowrap"><span ' + R12_DOT % "var(--warn)" + '></span>stream this week, then drop</span> · '
                '<span className="whitespace-nowrap"><span ' + R12_DOT % "var(--bad)" + '></span>not worth a move</span></div>')


def round12(t):
    t = lit(t, "add/drop: short Keep header", '<th className="px-3 py-2">Advice</th>',
            '<th className="px-3 py-2" title="Green: add and keep · Yellow: stream this week only · Red: pass">Keep</th>',
            'title="Green: add and keep')
    t = lit(t, "add/drop: colour dot", R12_CELL_OLD, R12_CELL_NEW, 'data-keep="dot"')
    t = lit(t, "add/drop: label next to name", R12_NAME_OLD, R12_NAME_NEW, '{tg ? <span className={"text-xs " + tg.c}>{tg.t}</span> : null}</div>')
    t = lit(t, "add/drop: colour legend", R12_FOOT_OLD, R12_FOOT_NEW, 'data-keep="legend"')
    return t


_fix_before_r12 = fix


def fix(t):
    return round12(_fix_before_r12(t))

# ---------- keep older rounds' "already done" markers after round 11 ----------
OLD_MARKS = '  // older rounds already done: "Gain", "Win this week" · colSpan={10}>No moves clear · base={wBase} /> : null}\n'
_fix_before_marks = fix


def fix(t):
    if "add/drop v11" in t and "older rounds already done" not in t:
        t = t.replace("  // add/drop v11:", OLD_MARKS + "  // add/drop v11:", 1)
    return _fix_before_marks(t)

# ---------- round 13: plain win % header, only green and red ----------
R13_WIN_OLD = '<span className="whitespace-nowrap"><span className="font-medium">{wpTxt(n)}</span>'
R13_WIN_NEW = '<span className="whitespace-nowrap" data-win="col"><span className={"font-medium " + (d > 0 ? "text-green-700" : d < 0 ? "text-red-600" : "")}>{wpTxt(n)}</span>'
R13_LEG_OLD = (R12_DOT % "var(--warn)" + '></span>stream this week, then drop</span> · <span className="whitespace-nowrap"><span '
               + R12_DOT % "var(--bad)" + '></span>not worth a move</span>')
R13_LEG_NEW = R12_DOT % "var(--bad)" + '></span>stream only or not worth a move</span>'


def round13(t):
    t = lit(t, "add/drop: header shows just the win %", '<th className="px-3 py-2 whitespace-nowrap">Win · now {wBase',
            '<th className="px-3 py-2 whitespace-nowrap" data-win="now" title="Your chance to win this week right now">{wBase',
            'data-win="now"')
    t = lit(t, "add/drop: win % green or red", R13_WIN_OLD, R13_WIN_NEW, 'data-win="col"')
    t = lit(t, "add/drop: yellow dot becomes red",
            'background: v === "Add & keep" ? "var(--good)" : v === "Stream only" ? "var(--warn)" : "var(--bad)"',
            'background: v === "Add & keep" ? "var(--good)" : "var(--bad)"',
            'v === "Add & keep" ? "var(--good)" : "var(--bad)"')
    t = lit(t, "add/drop: keep hover text", 'title="Green: add and keep · Yellow: stream this week only · Red: pass"',
            'title="Green: add and keep · Red: stream only or pass"', "Red: stream only or pass")
    t = lit(t, "add/drop: legend green and red only", R13_LEG_OLD, R13_LEG_NEW, "stream only or not worth a move")
    return t


_fix_before_r13 = fix


def fix(t):
    return round13(_fix_before_r13(t))

# ---------- round 14: cleaner injuries + protected players on My Team ----------
R14_START = '<Section title="Injuries & settings" sub="Return dates fill in from ESPN automatically; pick a date to override. Protected players are never suggested as drops.">'
R14_CALL = '<MyInjProt s={s} setS={setS} wk={wk} />\n    </div>\n  );\n}\n\n'
R14_HELPERS = r'''// ---------- round 14: My Team injuries + protected players (news_logos.py) ----------
function MyInjProt({ s, setS, wk }) {
  const K = s.blend, today = todayISO();
  const [edit, setEdit] = useState(null);
  const [adv, setAdv] = useState(false);
  const roster = s.players.filter((p) => p.ft === s.me);
  const upd = (id, patch) => setS((st) => ({ ...st, players: st.players.map((p) => (p.id === id ? { ...p, ...patch } : p)) }));
  const out = roster.filter((p) => { const b = effBack(p).d; return p.ir || (b && b > today) || (!b && avail(p, today) === 0) || (p.status && p.status !== "ACTIVE"); })
    .sort((a, b) => ((effBack(a).d || "9999") < (effBack(b).d || "9999") ? -1 : 1));
  const top = s.protectTop ?? 8;
  const healthy = roster.filter((p) => !p.ir).sort((a, b) => effAvg(b, K) - effAvg(a, K));
  const auto = healthy.slice(0, top), autoIds = new Set(auto.map((p) => p.id));
  const mine = healthy.filter((p) => p.keep && !autoIds.has(p.id));
  const addable = healthy.filter((p) => !autoIds.has(p.id) && !p.keep);
  const ST = { DAY_TO_DAY: "Day-to-day", OUT: "Out", INJURY_RESERVE: "IR", SUSPENSION: "Suspended" };
  const stTxt = (p) => (p.ir ? "IR" : ST[p.status] || (p.status || "Out").replace(/_/g, " "));
  const SRC = { you: "your date", ESPN: "from ESPN", news: "from injury news", estimate: "estimate" };
  const chip = "inline-flex items-center gap-1.5 pl-1.5 pr-2.5 py-1 rounded-full border text-sm ";
  const backTxt = (p, b) => {
    if (!b) return "No return date yet";
    if (b <= today) return "Available now";
    const n = Math.round((fromIso(b) - fromIso(today)) / 864e5);
    const miss = (wk.dates || []).filter((d, i) => d >= today && d < b && (wk.games[p.t] || []).includes(i)).length;
    return "Back " + mdL(b) + " (" + n + " day" + (n === 1 ? "" : "s") + ")" + (miss ? " · misses " + miss + " game" + (miss === 1 ? "" : "s") + " this week" : "");
  };
  return (
    <div className="space-y-4">
      <div className="grid md:grid-cols-2 gap-4 items-start">
        <Section title="Injuries" sub="Return dates come from ESPN. Change one only if you know better.">
          {out.length ? out.map((p) => { const eb = effBack(p); return (
            <div key={p.id} className="flex items-center gap-3 py-3 border-t border-slate-100">
              <TeamLogo t={p.t} size={30} />
              <div className="min-w-0 flex-1">
                <div className="flex items-center gap-2"><PN p={p} /><span className="text-xs text-slate-500">{p.p}</span><span className="text-xs px-1.5 py-0.5 rounded bg-red-100 text-red-600">{stTxt(p)}</span></div>
                <div className="text-xs text-slate-500 mt-0.5">{backTxt(p, eb.d)}{eb.d && eb.src ? " · " + SRC[eb.src] : ""}{eb.src === "you" ? <button className="text-blue-600 ml-2" onClick={() => upd(p.id, { back: DEFAULT_BACK[p.n] || "" })}>Reset</button> : null}</div>
                {edit === p.id ? <div className="flex items-center gap-2 mt-2"><input type="date" className={inp} value={eb.d} onChange={(e) => upd(p.id, { back: e.target.value })} /><button className="text-sm text-blue-600" onClick={() => setEdit(null)}>Done</button></div> : null}
              </div>
              {edit === p.id ? null : <button className="text-sm text-blue-600 whitespace-nowrap" onClick={() => setEdit(p.id)}>Change</button>}
            </div>
          ); }) : <div className="text-green-700">Everyone is healthy.</div>}
        </Section>
        <Section title="Protected players" sub="Never suggested as drops anywhere in the app. Players on IR are never dropped.">
          <label className="flex flex-wrap items-center gap-2 text-sm"><span>Always protect my top</span>
            <select className={inp} value={top} onChange={(e) => setS((st) => ({ ...st, protectTop: +e.target.value }))}>{[...Array(13)].map((_, n) => <option key={n} value={n}>{n}</option>)}</select>
            <span>players</span></label>
          {auto.length ? (
            <div className="mt-3 flex flex-wrap gap-2">{auto.map((p) => <span key={p.id} className={chip + "border-slate-200 text-slate-600"}><TeamLogo t={p.t} size={18} />{p.n}</span>)}</div>
          ) : null}
          <div className="text-xs uppercase tracking-wide text-slate-500 mt-4 mb-2">Also protect</div>
          <div className="flex flex-wrap gap-2 items-center">
            {mine.map((p) => <span key={p.id} className={chip + "border-green-300 bg-green-50"}><TeamLogo t={p.t} size={18} />{p.n}<button className="text-slate-500 ml-1 text-base leading-none" aria-label={"Unprotect " + p.n} onClick={() => upd(p.id, { keep: false })}>×</button></span>)}
            {addable.length ? <select className={inp} value="" onChange={(e) => { if (e.target.value) upd(e.target.value, { keep: true }); }}><option value="">+ Add a player</option>{addable.map((p) => <option key={p.id} value={p.id}>{p.n} ({p.p})</option>)}</select> : null}
          </div>
        </Section>
      </div>
      <div className="px-1">
        <button className="text-sm text-blue-600" onClick={() => setAdv(!adv)}>{adv ? "Hide the full editor" : "Edit every player: projections, play %, IR"}</button>
        {adv ? <div className="mt-3"><RosterTable s={s} setS={setS} wk={wk} team={s.me} /></div> : null}
      </div>
    </div>
  );
}

'''


def round14(t):
    t = block(t, "my team: cleaner injuries and protected players", R14_START, "function TeamsTab(", R14_CALL, "<MyInjProt s={s}")
    t = lit(t, "my team: injuries and protected helper", ROOT, R14_HELPERS + ROOT, "function MyInjProt(")
    return t


_fix_before_r14 = fix


def fix(t):
    return round14(_fix_before_r14(t))

# ---------- round 15: clean Advice page and player lines ----------
R15_CSS = r'''  /* round 15 advice (news_logos.py) */
  .adv-head, .adv-row { display: grid; grid-template-columns: 28px minmax(0,1fr) 60px 74px 36px; gap: 12px; align-items: center; }
  .adv-head { font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: .08em; color: var(--mute); padding: 4px 0 8px; }
  .adv-row { padding: 10px 0; border-top: 1px solid var(--line); }
  .adv-num { text-align: right; font-variant-numeric: tabular-nums; white-space: nowrap; }
  @media (max-width: 640px) { .adv-head, .adv-row { grid-template-columns: 26px minmax(0,1fr) 46px 64px 18px; gap: 8px; } }
'''

R15_PLAYERLINE = r'''const PlayerLine = ({ s, p, extra }) => {
  // player line v15: logo, name, one short note (news_logos.py)
  const tg = shortTag(p, s.blend);
  return (
    <div className="flex items-center gap-3 py-2.5 border-t border-slate-100 text-sm">
      <TeamLogo t={p.t} size={26} />
      <div className="min-w-0 flex-1">
        <div className="flex items-center gap-2 min-w-0"><PN p={p} className="truncate font-medium" /><span className="text-xs text-slate-500">{p.p}</span>{tg ? <span className={"text-xs truncate " + tg.c}>{tg.t}</span> : null}</div>
        <div className="text-xs text-slate-500 flex flex-wrap items-baseline gap-x-2 mt-0.5"><TL s={s} id={p.ft} />{extra}</div>
      </div>
      <div className="text-right whitespace-nowrap"><div className="font-semibold">{f1(effAvg(p, s.blend))}</div><div className="text-xs text-slate-500">pts/g</div></div>
    </div>
  );
};
'''

R15_ADVICE = r'''const advDot = (k, z) => ({ display: "inline-block", width: z || 10, height: z || 10, borderRadius: 99, margin: z ? 0 : "0 5px 0 6px", background: k ? "var(--good)" : "var(--bad)" });
const KeepLegend = () => <div className="text-xs text-slate-500 mt-3">Keep:<span style={advDot(true)}></span>add and keep ·<span style={advDot(false)}></span>stream this week, then drop</div>;
const AdvMove = ({ s, r, K, showDrop, base }) => {
  const sd = effAvg(r.f, K) - effAvg(r.d, K), keep = r.gain > 0 && sd >= 0, tg = shortTag(r.f, K);
  return (
    <div className="adv-row">
      <TeamLogo t={r.f.t} size={28} />
      <div className="min-w-0">
        <div className="flex items-center gap-2 min-w-0"><PN p={r.f} className="truncate font-medium" /><span className="text-xs text-slate-500">{r.f.p}</span>{tg ? <span className={"text-xs truncate m-hide " + tg.c}>{tg.t}</span> : null}</div>
        <div className="text-xs text-slate-500 truncate">{showDrop ? "drop " + r.d.n + " · " : ""}{sd >= 0 ? "+" : ""}{f1(sd)}/g long-term</div>
      </div>
      <div className="adv-num font-semibold text-green-700">+{f1(r.gain)}</div>
      <div className="adv-num"><WinCell s={s} add={r.f} drop={r.d} base={base} /></div>
      <div className="adv-num"><span title={keep ? "Add and keep" : "Stream this week, then drop"} style={advDot(keep, 12)}></span></div>
    </div>
  );
};
function AdvicePanel({ s }) {
  // advice v15: clean rows (news_logos.py) · older marker kept: advice={1}
  const K = s.blend;
  const minGain = s.minGain ?? 3;
  const now = useMemo(() => computeMoves(s, { H: 1, pool: 60 }), [s]);
  const later = useMemo(() => computeMoves(s, { H: 4, pool: 40 }), [s]);
  const base = useMemo(() => winChance(s), [s]);
  const sdOf = (r) => effAvg(r.f, K) - effAvg(r.d, K);
  const topNow = now.res.filter((r) => r.gain >= minGain).slice(0, 5);
  const topLong = later.res.filter((r) => r.gain >= minGain && sdOf(r) >= 0).slice(0, 5);
  const mine = s.players.filter((p) => p.ft === s.me && !p.ir);
  const why = (p) => {
    const g = sigOf(p), r = [], fr = formRatio(p, K), t = g.toi;
    if (g.ppChg === "added") r.push("new on PP1");
    if (fr !== null && fr >= 1.25) r.push(f1(g.rec.ppg) + "/g last 14 days");
    if (t && t.d >= 90) r.push(mm(t.d) + " ice time");
    if (t && t.pd >= 45) r.push("PP " + mm(t.pd));
    if ((p.chg || 0) >= 5) r.push("+" + f1(p.chg) + "% rostered");
    return r.join(" · ");
  };
  const watch = s.players.filter((p) => p.ft === "fa" && p.prob > 0 && why(p)).sort((a, b) => effAvg(b, K) - effAvg(a, K)).slice(0, 8);
  const form = mine.map((p) => {
    const fr = formRatio(p, K), t = toiOf(p), rec = sigOf(p).rec;
    if (fr !== null && fr >= 1.3) return { p, n: "Hot: " + f1(rec.ppg) + "/g lately. Start him every game.", c: "text-orange-600" };
    if (fr !== null && fr <= 0.7) return { p, n: "Cold: " + f1(rec.ppg) + "/g lately. Check his role before dropping.", c: "text-sky-600" };
    if (t && (t.d <= -90 || t.pd <= -45)) return { p, n: "Losing minutes (" + mm(t.d) + " a game). Watch closely.", c: "text-red-600" };
    if (t && (t.d >= 90 || t.pd >= 45)) return { p, n: "Bigger role (" + mm(t.d) + " a game).", c: "text-green-700" };
    return null;
  }).filter(Boolean);
  const buyLow = s.players.filter((p) => p.ft !== s.me && p.ft !== "fa" && effAvg(p, K) >= 7 && (formRatio(p, K) ?? 9) <= 0.75).sort((a, b) => effAvg(b, K) - effAvg(a, K)).slice(0, 5);
  const T = leagueTable(s), g = T.grpRank[s.me] || {};
  const posName = { F: "forwards", D: "defence", G: "goalies" }, need = { F: 10, D: 5, G: 2 };
  const by = ["F", "D", "G"].sort((a, b) => (g[b] || 0) - (g[a] || 0)), weak = by[0], strong = by[2];
  const spare = mine.filter((p) => p.p === strong).sort((a, b) => effAvg(b, K) - effAvg(a, K)).slice(need[strong]);
  const oneDrop = (l) => (l.length > 1 && l.every((r) => r.d.id === l[0].d.id) ? l[0].d : null);
  const moves = (list, label, empty) => {
    const d1 = oneDrop(list);
    if (!list.length) return <div className="text-slate-400">{empty}</div>;
    return (
      <div>
        {d1 ? <div className="text-sm mb-2"><span className="text-slate-500">Drop for each: </span><PN p={d1} /></div> : null}
        <div className="adv-head"><span></span><span>Pickup</span><span className="adv-num">{label}</span><span className="adv-num" title="Your chance to win this week right now">{base == null ? "Win" : wpTxt(base)}</span><span className="adv-num">Keep</span></div>
        {list.map((r) => <AdvMove key={r.f.id} s={s} r={r} K={K} showDrop={!d1} base={base} />)}
      </div>
    );
  };
  return (
    <div className="space-y-4">
      {!window.__SIG ? <div className="text-sm text-slate-500">Form, PP1 and news signals appear after the next sync.</div> : null}
      <Section title="Best moves this week" sub="Most extra points in your daily lineups for the rest of this week.">
        {moves(topNow, "Gain", `No move adds ${minGain}+ points this week. Save your moves.`)}
        {topNow.length ? <KeepLegend /> : null}
      </Section>
      <Section title="Long-term upgrades" sub="Better per game, and more points over the next 4 weeks.">
        {moves(topLong, "4 wks", "No free agent is a clear long-term upgrade right now.")}
      </Section>
      {watch.length ? (
        <Section title="Free agents to watch" sub="Hot lately, new on PP1, more ice time, or gaining owners fast.">
          {watch.map((p) => <PlayerLine key={p.id} s={s} p={p} extra={<span>· {why(p)}</span>} />)}
        </Section>
      ) : null}
      <Section title="Your players" sub="Recent form and ice time compared with their projection.">
        {form.length ? form.map(({ p, n, c }) => <PlayerLine key={p.id} s={s} p={p} extra={<span className={c}>· {n}</span>} />) : <div className="text-slate-400">Everyone is playing close to projection.</div>}
      </Section>
      <Section title="Trade advice" sub={`Your ranks: forwards #${g.F || "–"}, defence #${g.D || "–"}, goalies #${g.G || "–"} of ${T.rows.length}.`}>
        <div>{weak !== strong && g[weak] > g[strong] ? <>Trade from your <b>{posName[strong]}</b> to improve your <b>{posName[weak]}</b>.{spare.length ? <span className="text-slate-500"> Spare: {spare.map((p) => p.n).join(", ")}.</span> : null}</> : "Your roster is balanced. Trade only for clear upgrades."}</div>
        {buyLow.length ? <div className="mt-3"><div className="text-xs uppercase tracking-wide text-slate-500 mb-1">Buy low: good players in a slump</div>{buyLow.map((p) => <PlayerLine key={p.id} s={s} p={p} />)}</div> : null}
      </Section>
    </div>
  );
}

'''

R15_EDGES = r'''function EdgesPanel({ s }) {
  // edges v15: only groups with players, 5 each (news_logos.py)
  const K = s.blend, S = window.__SIG || {}, M = window.__MODEL;
  const pid = (p) => (typeof p.id === "string" && p.id[0] === "e" ? p.id.slice(1) : null);
  const top5 = (l) => l.slice(0, 5);
  const byAvg = (a, b) => effAvg(b, K) - effAvg(a, K);
  const ln = (p) => sigOf(p).lines || {};
  const promoFA = top5(s.players.filter((p) => p.ft === "fa" && ln(p).chg === "up").sort(byAvg));
  const promoOther = top5(s.players.filter((p) => p.ft !== "fa" && p.ft !== s.me && ln(p).chg === "up").sort(byAvg));
  const mineChg = s.players.filter((p) => p.ft === s.me && ln(p).chg);
  const lk = (p) => sigOf(p).luck;
  const lucky = (p) => { const l = lk(p); return l && (l.t === "s" ? l.d >= 2 : l.d >= 4); };
  const unlucky = (p) => { const l = lk(p); return l && (l.t === "s" ? l.d <= -2 : l.d <= -4); };
  const byLuck = (a, b) => Math.abs(lk(b).d) - Math.abs(lk(a).d);
  const sellHigh = top5(s.players.filter((p) => p.ft === s.me && lucky(p)).sort(byLuck));
  const myUnlucky = top5(s.players.filter((p) => p.ft === s.me && unlucky(p)).sort(byLuck));
  const buyLow = top5(s.players.filter((p) => p.ft !== s.me && p.ft !== "fa" && unlucky(p) && effAvg(p, K) >= 5).sort(byLuck));
  const buyFA = top5(s.players.filter((p) => p.ft === "fa" && unlucky(p)).sort(byLuck));
  const luckInfo = (p) => { const l = lk(p); return <span>· {l.t === "s" ? `${l.g} G on ${l.sh} shots, ${l.pct}% vs ${l.cpct}% career` : `SV% ${l.sv.toFixed(3)} vs ${l.csv.toFixed(3)} career`}</span>; };
  const mv = (p) => { const id = pid(p); const mb = M && id ? (M.base || {})[id] : null; return mb != null && p.proj && p.avg > 0 ? { mb, e: p.avg, d: mb - p.avg, r: mb / p.avg } : null; };
  const under = (p) => { const x = mv(p); return x && x.d >= 1 && x.r >= 1.15; };
  const over = (p) => { const x = mv(p); return x && x.d <= -1 && x.r <= 0.85; };
  const uFA = top5(s.players.filter((p) => p.ft === "fa" && under(p)).sort((a, b) => mv(b).d - mv(a).d));
  const uOther = top5(s.players.filter((p) => p.ft !== "fa" && p.ft !== s.me && under(p)).sort((a, b) => mv(b).d - mv(a).d));
  const oMine = top5(s.players.filter((p) => p.ft === s.me && over(p)).sort((a, b) => mv(a).d - mv(b).d));
  const uMine = top5(s.players.filter((p) => p.ft === s.me && under(p)));
  const mvInfo = (p) => { const x = mv(p); return <span className={x.d > 0 ? "text-green-700" : "text-red-600"}>· model {f1(x.mb)} vs ESPN {f1(x.e)} pts/g</span>; };
  const lineNote = (p) => <span className={ln(p).chg === "up" ? "text-green-700" : "text-red-600"}>· {ln(p).chg === "up" ? "moved up to " + (LBL[ln(p).grp] || "a bigger role") : "moved down the lineup"}</span>;
  const None = ({ t }) => <div className="text-slate-400">{t}</div>;
  const Grp = ({ t, list, note }) => (list.length ? (
    <div className="mt-3"><div className="text-xs uppercase tracking-wide text-slate-500 mb-1">{t}</div>{list.map((p) => <PlayerLine key={p.id} s={s} p={p} extra={note ? note(p) : null} />)}</div>
  ) : null);
  const promoAny = promoFA.length + promoOther.length + mineChg.length;
  const luckAny = sellHigh.length + myUnlucky.length + buyLow.length + buyFA.length;
  const mvAny = uFA.length + uOther.length + oMine.length + uMine.length;
  return (
    <div className="space-y-4">
      <Section title="Line promotions" sub="Top-6 forwards and top-4 D get more minutes. Points usually follow within a week.">
        {!S.lines ? <None t="Line data appears after the next sync." /> : promoAny ? (<>
          <Grp t="Free agents: pickup targets" list={promoFA} note={lineNote} />
          <Grp t="Your players" list={mineChg} note={lineNote} />
          <Grp t="Other teams: trade targets" list={promoOther} note={lineNote} />
        </>) : <None t="No line changes since yesterday." />}
      </Section>
      <Section title="Luck" sub="Shooting % and save % this season vs career. Luck evens out, so trade on it.">
        {!S.luck || !Object.keys(S.luck).length ? <None t="Fills in once players have enough shots, usually by late October." /> : luckAny ? (<>
          <Grp t="Sell high: your lucky players" list={sellHigh} note={luckInfo} />
          <Grp t="Buy low: unlucky players on other teams" list={buyLow} note={luckInfo} />
          <Grp t="Unlucky free agents" list={buyFA} note={luckInfo} />
          <Grp t="Your unlucky players: don't sell low" list={myUnlucky} note={luckInfo} />
        </>) : <None t="Nobody is running unusually lucky or unlucky." />}
      </Section>
      <Section title="Model vs ESPN" sub="Where your GM model and ESPN disagree by 15% or more. Most managers only see ESPN's number.">
        {!M ? <None t="Needs the GM model in the sync." /> : mvAny ? (<>
          <Grp t="Undervalued free agents" list={uFA} note={mvInfo} />
          <Grp t="Undervalued on other teams: trade targets" list={uOther} note={mvInfo} />
          <Grp t="Yours that ESPN overrates: sell" list={oMine} note={mvInfo} />
          <Grp t="Yours that ESPN underrates: keep" list={uMine} note={mvInfo} />
          <div className="text-xs text-slate-500 mt-3">Early in the season the model leans on last year's stats, so check why before acting.</div>
        </>) : <None t="The model and ESPN agree on everyone right now." />}
      </Section>
    </div>
  );
}

'''


def round15(t):
    t = lit(t, "advice styles", "</style>", R15_CSS + "</style>", "round 15 advice")
    t = block(t, "player lines: cleaner layout", "const PlayerLine = ({ s, p, extra }) => (", "const Section = (", R15_PLAYERLINE, "player line v15")
    t = block(t, "advice: clean page", "function AdvicePanel({ s }) {", "function NewsView(", R15_ADVICE, "advice v15")
    t = block(t, "edges: only groups with players", "function EdgesPanel({ s }) {", "// ---------- Bench fixer ----------", R15_EDGES, "edges v15")
    return t


_fix_before_r15 = fix


def fix(t):
    return round15(_fix_before_r15(t))

# ---------- round 16: real ESPN points once a game starts, projection for the rest ----------
# espn_sync.py: saves each rostered player's actual points per day (last 7 days) + NHL game states.
# fantasy-gm.html: Matchup / Today / league cards show actual on top, what's still projected under it,
# LIVE / FINAL on each player, projected vs actual per day, and a win chance built from banked points
# plus a small nudge (10% of how far off each player has been per game, capped at 15%).

SYNC16_ANCHOR = "# 4) Starting goalies from Daily Faceoff (today + tomorrow)"
SYNC16_BLOCK = r'''# 3b) actual points per player per day + NHL game states (news_logos.py round 16)
try:
    today_et = datetime.now(ET).date()
    sp_of = {d_.isoformat(): pid_ for pid_, d_ in period_date.items()}
    daily = {}
    for back_ in range(6, -1, -1):
        dd_ = (today_et - timedelta(days=back_)).isoformat()
        sp_ = sp_of.get(dd_)
        if not sp_:
            continue
        try:
            rs_ = get(LEAGUE, params={"view": "mRoster", "scoringPeriodId": sp_})
        except Exception as ex:
            print(f"(daily) ESPN rosters for {dd_} failed: {ex}")
            continue
        dump(f"espn-raw-daily-{dd_}.json", rs_)
        day_ = {}
        for tt_ in rs_.get("teams", []):
            tm_ = {}
            for en_ in (tt_.get("roster") or {}).get("entries", []):
                pl_ = (en_.get("playerPoolEntry") or {}).get("player") or {}
                pts_ = None
                for st_ in pl_.get("stats") or []:
                    if st_.get("scoringPeriodId") == sp_ and st_.get("statSourceId") == 0:
                        pts_ = round(st_.get("appliedTotal") or 0, 2)
                        break
                tm_[str(en_.get("playerId"))] = [pts_, en_.get("lineupSlotId")]
            day_[str(tt_.get("id"))] = tm_
        daily[dd_] = day_
    gstate = {}
    for back_ in (1, 0):
        dd_ = (today_et - timedelta(days=back_)).isoformat()
        try:
            js_ = requests.get(f"https://api-web.nhle.com/v1/score/{dd_}", headers={"User-Agent": "Mozilla/5.0"}, timeout=20).json()
        except Exception as ex:
            print(f"(daily) NHL scores for {dd_} failed: {ex}")
            continue
        gs_ = {}
        for g_ in js_.get("games", []):
            s_ = str(g_.get("gameState") or "")
            s_ = "F" if s_ in ("FINAL", "OFF") else "L" if s_ in ("LIVE", "CRIT") else "P"
            per_ = (g_.get("periodDescriptor") or {}).get("number") or 1
            rem_ = (g_.get("clock") or {}).get("secondsRemaining")
            rem_ = 1200 if rem_ is None else rem_
            f_ = 1.0 if s_ == "F" else 0.0 if s_ == "P" else min(0.99, ((per_ - 1) * 1200 + (1200 - rem_)) / 3600)
            for side_ in ("homeTeam", "awayTeam"):
                ab_ = str((g_.get(side_) or {}).get("abbrev") or "").upper()
                gs_[ALIAS.get(ab_, ab_)] = {"s": s_, "f": round(f_, 2)}
        gstate[dd_] = gs_
    data["daily"] = daily
    data["gstate"] = gstate
    mine_ = str(MY_TEAM_ID)
    for dd_, day_ in daily.items():
        tot_ = sum((v[0] or 0) for v in day_.get(mine_, {}).values() if v[1] in (3, 4, 5, 6))
        print(f"(daily) {dd_}: your active players scored {round(tot_, 1)}")
    for m_ in matchups:
        if m_["period"] == current and MY_TEAM_ID in (m_["home"], m_["away"]):
            print(f"(daily) ESPN week score for you: {m_['hs'] if m_['home'] == MY_TEAM_ID else m_['as']}")
    print("(daily) NHL game states:", {k_: sorted(set(v["s"] for v in g2_.values())) for k_, g2_ in gstate.items()})
except Exception as ex:
    print(f"(check) daily actual points failed: {ex}")
'''

_fix_sync_before_r16 = PY_FIXES[SYNC]


def fix_sync16(t):
    t = _fix_sync_before_r16(t)
    t = lit(t, "sync: actual points per day", SYNC16_ANCHOR, SYNC16_BLOCK + SYNC16_ANCHOR, "# 3b) actual points per player per day")
    py_ok(SYNC, t)
    return t


PY_FIXES[SYNC] = fix_sync16

R16_DAYLINEUP = r'''function dayLineup(roster, wk, d, K, cap) {
  const c = cap || { F: 9, D: 5, U: 1, G: 2 };
  const dt = wk.dates ? wk.dates[d] : null;
  const pl = roster.filter((p) => !p.ir && p.prob > 0 && avail(p, dt) > 0 && (wk.games[p.t] || []).includes(d)).map((p) => { const g = p.p === "G" ? gStart(p, dt) : null; return { ...p, x: effAvg(p, K, dt) * (g ? g.v : p.prob) * avail(p, dt), gs: g ? g.l : "", dt }; });
  const by = (a, b) => b.x - a.x;
  const F = pl.filter((p) => p.p === "F").sort(by), D = pl.filter((p) => p.p === "D").sort(by), G = pl.filter((p) => p.p === "G").sort(by);
  const fs = F.slice(0, c.F), ds = D.slice(0, c.D);
  const rest = [...F.slice(c.F), ...D.slice(c.D)].sort(by);
  const u = rest.slice(0, c.U), gs = G.slice(0, c.G);
  const bench = [...rest.slice(c.U), ...G.slice(c.G)];
  const start = [...fs.map((p) => ({ ...p, slot: "F" })), ...ds.map((p) => ({ ...p, slot: "D" })), ...u.map((p) => ({ ...p, slot: "UTIL" })), ...gs.map((p) => ({ ...p, slot: "G" }))];
  return { start, bench, total: start.reduce((s, p) => s + p.x, 0), empty: c.F - fs.length + (c.D - ds.length) + (c.U - u.length) + (c.G - gs.length), sched: pl.length };
}
'''

R16_HELPERS = r'''// ---------- round 16: live and final points from ESPN (news_logos.py) ----------
const ESLOT = { 3: "F", 4: "D", 6: "UTIL", 5: "G" };
const CAPK = { F: "F", D: "D", UTIL: "U", G: "G" };
let __PB = null, __NG = null;
const pby = () => { const L = window.__PLAYERS || []; if (!__PB || __PB.k !== L) __PB = { k: L, m: Object.fromEntries(L.map((p) => [p.id, p])) }; return __PB.m; };
const actDay = (tid, dt) => { const D = ((window.ESPN_DATA || {}).daily || {})[dt]; return D ? D[String(tid).replace(/^t/, "")] || null : null; };
const gState = (t, dt) => {
  const x = ((((window.ESPN_DATA || {}).gstate || {})[dt]) || {})[t];
  if (x && x.s === "F") return { s: "F", f: 1 };
  if (x && x.s === "L") return { s: "L", f: x.f || 0 };
  const g = gameOf(t, dt), st = g && g.st ? Date.parse(g.st) : NaN;
  if (!isNaN(st)) { const el = (Date.now() - st) / 36e5; return el < 0 ? { s: "P", f: 0 } : el > 3.5 ? { s: "F", f: 1 } : { s: "L", f: Math.min(0.95, el / 2.6) }; }
  return dt && dt < todayISO() ? { s: "F", f: 1 } : { s: "P", f: 0 };
};
const LiveTag = ({ st }) => (st === "L" ? <span className="text-xs font-semibold text-red-600">LIVE</span> : st === "F" ? <span className="text-xs text-slate-500">FINAL</span> : null);
// players who beat or missed their projection get 10% of the average miss per game, capped at 15%
function liveNudges(K) {
  const E = window.ESPN_DATA || {}, key = [E.generated, K, window.__PMODE, window.__PLAYERS];
  if (__NG && __NG.k.every((v, i) => v === key[i])) return __NG.m;
  const P = pby(), acc = {};
  Object.entries(E.daily || {}).forEach(([dt, T]) => Object.values(T || {}).forEach((tm) => Object.entries(tm || {}).forEach(([pid, v]) => {
    const p = P["e" + pid];
    if (!p || !v || v[0] == null || gState(p.t, dt).s !== "F") return;
    const a = (acc[p.id] = acc[p.id] || { s: 0, n: 0, seen: {} });
    if (a.seen[dt]) return;
    a.seen[dt] = 1; a.s += v[0] - effAvg(p, K, dt); a.n++;
  })));
  const m = {};
  Object.entries(acc).forEach(([id, a]) => { const b = effAvg(P[id], K); if (!(b > 0) || !a.n) return; const adj = Math.max(-0.15, Math.min(0.15, (0.1 * a.s / a.n) / b)); if (Math.abs(adj) >= 0.005) m[id] = 1 + adj; });
  __NG = { k: key, m };
  return m;
}
function weekLive(roster, wk, K, tid, opt) {
  // live week v16: real points for games that started (ESPN lineup), projection for everything still to come
  const dates = wk.dates || [], ng = liveNudges(K), P = pby(), today = todayISO();
  const r = roster.map((p) => (ng[p.id] ? { ...p, gwMul: (p.gwMul || 1) * ng[p.id] } : p));
  const byId = {}; r.forEach((p) => (byId[p.id] = p));
  let actSoFar = 0, projSoFar = 0;
  const days = wk.days.map((_, d) => {
    const dt = dates[d];
    const plays = (p) => (wk.games[p.t] || []).includes(d);
    const lk = (p) => !!dt && plays(p) && gState(p.t, dt).s !== "P";
    const full = opt && opt.detail ? dayLineup(roster, wk, d, K).total : null;
    const AD = dt ? actDay(tid, dt) : null;
    const adAct = AD ? Object.entries(AD).filter(([, v]) => v && ESLOT[v[1]]) : [];
    if (!dt || (!r.some(lk) && !adAct.some(([, v]) => v[0] != null))) {
      const L = dayLineup(r, wk, d, K);
      return { ...L, act: 0, proj: full != null ? full : L.total, locked: 0, liveN: 0, openN: L.start.length, allDone: !!dt && dt < today, benchAct: [], empty: dt && dt < today ? 0 : L.empty };
    }
    const cap = { F: 9, D: 5, U: 1, G: 2 }, rows = [], done = new Set();
    let act = 0;
    const take = (p, pp, slot, a, assume) => {
      const g = gState(p.t, dt), gs = p.p === "G" ? gStart(p, dt) : null;
      const base = (q) => effAvg(q, K, dt) * (a != null ? 1 : (gs ? gs.v : p.prob) * avail(p, dt));
      const x0 = base(pp), playing = assume || a != null || (g.s === "L" && g.f < 0.3);
      const vf = g.s === "L" && playing ? 1 - g.f : 0;
      rows.push({ ...pp, slot, st: g.s, a, x0, x: x0 * vf, vf, dt, gs: gs ? gs.l : "" });
      if (a != null) { act += a; actSoFar += a; projSoFar += base(p) * (g.s === "F" ? 1 : g.f); }
      done.add(p.id);
      if (CAPK[slot]) cap[CAPK[slot]]--;
    };
    if (AD) {
      adAct.forEach(([pid, v]) => {
        const p = P["e" + pid];
        if (!p) { if (v[0] != null) { act += v[0]; actSoFar += v[0]; } return; }
        if (plays(p) ? gState(p.t, dt).s === "P" : v[0] == null) return;
        take(p, byId[p.id] || p, ESLOT[v[1]], v[0], false);
      });
    } else {
      dayLineup(r, wk, d, K).start.filter(lk).forEach((q) => { const raw = roster.find((x) => x.id === q.id) || q; take(raw, byId[q.id] || raw, q.slot, null, true); });
    }
    const benchAct = AD ? Object.entries(AD).filter(([, v]) => v && v[1] === 7 && v[0]).map(([pid, v]) => ({ p: P["e" + pid], a: v[0] })).filter((x) => x.p && gState(x.p.t, dt).s !== "P") : [];
    Object.keys(cap).forEach((k) => (cap[k] = Math.max(0, cap[k])));
    const L = dayLineup(r.filter((p) => !done.has(p.id) && !lk(p)), wk, d, K, cap);
    const liveN = rows.filter((x) => x.vf > 0).length;
    return { start: [...rows, ...L.start], bench: L.bench, total: rows.reduce((s2, x) => s2 + x.x, 0) + L.total, act, proj: full, locked: rows.length, liveN, openN: L.start.length, allDone: !rows.some((x) => x.st === "L") && !L.start.length, benchAct, empty: dt < today ? 0 : L.empty, sched: L.sched + liveN };
  });
  const sum = (f) => days.reduce((a, x) => a + f(x), 0);
  return { days, total: sum((x) => x.total), act: sum((x) => x.act), actSoFar, projSoFar, used: sum((x) => x.openN + x.liveN), wasted: sum((x) => x.bench.length), empty: sum((x) => x.empty), sched: sum((x) => x.sched) };
}

'''

R16_SIDE = r'''function Side({ l, s, id, wk, d }) {
  // matchup row layout v4: big logo beside name + opponent/time, same font for totals
  // matchup row v16: real ESPN points once a game starts (news_logos.py)
  const locked = (l.locked || 0) > 0;
  return (
    <div className="p-3 flex flex-col h-full">
      <div className="flex justify-between font-semibold mb-1"><TL s={s} id={id} className="truncate" /><span>{f1((l.act || 0) + l.total)}</span></div>
      <table className="w-full text-sm"><tbody>
        {l.start.map((p) => {
          const g = gameOf(p.t, p.dt), o = oddsFor(p.t, p.dt);
          const gc = p.gs ? (p.gs.includes("confirmed") && !p.gs.includes("un") ? "text-green-700 font-semibold" : p.gs === "not starting" ? "text-red-600" : "text-amber-600") : "";
          return (
            <tr key={p.id} className="border-t border-slate-100">
              <td className="py-2 pr-2 text-xs text-slate-500 w-10 align-middle">{p.slot}</td>
              <td className="py-2 align-middle">
                <div className="flex items-center gap-3 min-w-0">
                  <TeamLogo t={p.t} size={36} />
                  <div className="min-w-0">
                    <div className="flex items-center gap-2 min-w-0">
                      <PN p={p} className="truncate" />
                      {!p.st && !p.gs && p.prob < 1 ? <span className="text-xs text-slate-400">{Math.round(p.prob * 100)}%</span> : null}
                      {!p.st && p.gs ? <span className={"text-xs " + gc}>{p.gs}</span> : null}
                    </div>
                    {g || p.st ? <div className="text-xs text-slate-500 mt-0.5">{g ? (g.h ? "vs " : "@") + g.o + " · " : ""}{p.st ? <LiveTag st={p.st} /> : gameTime(g)}</div> : null}
                  </div>
                </div>
              </td>
              <td className="py-2 text-right whitespace-nowrap align-middle">
                {p.st ? (
                  <div>
                    <div className="font-semibold">{p.a == null ? (p.st === "F" ? <span className="text-xs text-slate-400 font-normal">DNP</span> : "–") : f1(p.a)}</div>
                    {p.st === "L" ? <div className="text-xs text-slate-400">proj {f1(p.x0)}</div> : null}
                  </div>
                ) : (<>
                  {o && window.__PMODE !== "espn" ? (p.p === "G"
                    ? <span className={"text-xs mr-2 " + (o.win >= 0.55 ? "text-green-700" : o.win <= 0.45 ? "text-red-600" : "text-slate-500")} title="Win chance from betting odds">W {Math.round(o.win * 100)}%</span>
                    : <span className={"text-xs mr-2 " + (o.gf >= 3.3 ? "text-green-700" : o.gf <= 2.7 ? "text-red-600" : "text-slate-400")} title="Team expected goals from betting odds">xG {o.gf.toFixed(1)}</span>) : null}
                  {f1(p.x)}
                </>)}
              </td>
            </tr>
          );
        })}
        {l.start.length === 0 && <tr><td className="text-slate-400 py-1">No games</td></tr>}
      </tbody></table>
      {l.benchAct && l.benchAct.length ? <div className="text-xs text-slate-500 mt-1">On the ESPN bench (not counted): {l.benchAct.map((x) => x.p.n + " " + f1(x.a)).join(", ")}</div> : null}
      {l.bench.length > 0 && <div className="text-xs text-red-600 mt-1">Would sit (no slot): {l.bench.map((p) => p.n).join(", ")}</div>}
      {l.empty > 0 && <div className="text-xs text-slate-500 mt-1">Empty slots: {l.empty}</div>}
      {wk && id === s.me ? <FillSlot l={l} s={s} wk={wk} d={d} /> : null}
      <div className="mt-auto pt-3"><div className="border-t border-slate-200 pt-2 space-y-1">
        {locked && l.allDone ? (<>
          <div className="flex justify-between text-sm text-slate-500"><span>Projected</span><span>{l.proj != null ? f1(l.proj) : "–"}</span></div>
          <div className="flex justify-between font-semibold"><span>Actual</span><span>{f1(l.act)}</span></div>
        </>) : locked ? (<>
          <div className="flex justify-between font-semibold"><span>Actual so far</span><span>{f1(l.act)}</span></div>
          <div className="flex justify-between text-sm text-slate-500"><span>Still projected</span><span>{f1(l.total)}</span></div>
        </>) : <div className="flex justify-between font-semibold"><span>Projected today</span><span>{f1(l.total)}</span></div>}
      </div></div>
    </div>
  );
}
'''

R16_MATCHUP = r'''function Matchup({ s, setS, wk, setWk }) {
  // matchup v16: actual points on top, what's still projected underneath (news_logos.py)
  const K = s.blend, done = wk.done || 0;
  const pairOpp = oppOf(wk, s.me);
  const myPair = [s.me, pairOpp || s.opp];
  const others = (wk.pairs || []).filter((p) => p[0] && p[1] && p[0] !== s.me && p[1] !== s.me);
  const all = [myPair, ...others];
  const [sel, setSel] = useState(0);
  const cur = all[Math.min(sel, all.length - 1)];
  const gen = (window.ESPN_DATA || {}).generated;
  const P = useMemo(() => {
    const o = {};
    all.forEach((pr) => pr.forEach((id) => { if (!id || o[id]) return; o[id] = { r: weekLive(s.players.filter((p) => p.ft === id), wk, K, id, { detail: true }), act: +((wk.act || {})[id]) || 0 }; }));
    return o;
  }, [s.players, wk, K, done, s.opp, gen]);
  const [a, b] = cur;
  const A = P[a].r, B = P[b].r, aA = P[a].act, aB = P[b].act;
  const fa = aA + A.total, fb = aB + B.total, margin = fa - fb;
  const final = done >= wk.days.length;
  const vsP = (R) => { if (!(R.projSoFar > 0 || R.actSoFar > 0)) return null; const v = R.actSoFar - R.projSoFar; return <><br /><span className={v >= 0 ? "text-green-700" : "text-red-600"}>{(v >= 0 ? "+" : "") + f1(v)} vs projected so far</span></>; };
  let run = (aA - aB) - (A.act - B.act);
  return (
    <div>
      {all.length > 1 && <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3 mb-4">{all.map(([x, y], i) => <MatchCard key={x + "-" + y} s={s} a={x} b={y} P={P} on={i === sel} mine={i === 0} onSel={() => setSel(i)} />)}</div>}
      <div className="flex flex-wrap gap-2 items-center mb-3 text-sm">
        <TL s={s} id={a} className="font-semibold" /><span className="text-slate-500">vs</span>
        {sel === 0 && !pairOpp ? <select className={inp} value={s.opp} onChange={(e) => setS({ ...s, opp: e.target.value })}>{s.teams.filter((t) => t.id !== s.me).map((t) => <option key={t.id} value={t.id}>{t.name}</option>)}</select> : <TL s={s} id={b} className="font-semibold" />}
      </div>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-3">
        <Card label={teamName(s, a)} value={f1(aA)} sub={<>+ {f1(A.total)} still projected · {f1(fa)} final est.{vsP(A)}<br />{gamesMoves(s, a, wk, A)}</>} />
        <Card label={teamName(s, b)} value={f1(aB)} sub={<>+ {f1(B.total)} still projected · {f1(fb)} final est.{vsP(B)}<br />{gamesMoves(s, b, wk, B)}</>} />
        <Card label={final ? "Final margin" : "Projected margin"} value={(margin >= 0 ? "+" : "") + f1(margin)} tone={margin >= 0 ? "bg-green-50 border-green-200" : "bg-red-50 border-red-200"} />
        <Card label={"Win chance · " + teamName(s, a)} value={final ? (margin > 0 ? "WIN" : margin < 0 ? "LOSS" : "TIE") : wpTxt(winProb(A, B, aA, aB))} sub={final ? "Week complete" : `${wk.days.length - done} day(s) left · ${A.wasted} games wasted`} />
      </div>
      <LiveBar s={s} wk={wk} setWk={setWk} ids={[a, b]} />
      {wk.days.map((dl, d) => {
        const x = A.days[d], y = B.days[d];
        const dv = x.act + x.total - (y.act + y.total); run += dv;
        const tag = x.locked || y.locked ? (x.allDone && y.allDone ? "FINAL" : "LIVE") : "";
        return (
          <div key={d} className="bg-white rounded-xl border border-slate-200 mb-3">
            <div className="flex justify-between items-center px-3 py-2 border-b border-slate-200 text-sm">
              <span className="font-semibold">{dl}</span>
              {/* day header: running total removed */}
              {tag ? <span className={"text-xs font-semibold " + (tag === "LIVE" ? "text-red-600" : "text-slate-500")}>{tag}</span> : null}
            </div>
            <div className="m-only"><H2H x={x} y={y} s={s} a={a} b={b} wk={wk} d={d} /></div>
            <div className="m-hide grid grid-cols-1 md:grid-cols-2 divide-y md:divide-y-0 md:divide-x divide-slate-200">
              <Side l={x} s={s} id={a} wk={wk} d={d} /><Side l={y} s={s} id={b} wk={wk} d={d} />
            </div>
            <div data-v="daydiff2" data-w="daydiff3" className="border-t border-slate-200 px-3 py-2">
              {[["Day difference", dv], ["Total so far", run]].map(([lab, v]) => (
                <div key={lab} className="flex justify-between items-center py-1.5 font-semibold">
                  <span>{lab}</span>
                  <span className="flex items-center gap-3">
                    <span className="text-sm text-slate-500 font-normal">{Math.abs(v) < 0.05 ? "even" : (v > 0 ? teamName(s, a) : teamName(s, b)) + " ahead"}</span>
                    <span className={"min-w-[64px] text-center px-2.5 py-0.5 rounded-md " + (v >= 0 ? "bg-green-100 text-green-700" : "bg-red-100 text-red-600")}>{v >= 0 ? "+" : ""}{f1(v)}</span>
                  </span>
                </div>
              ))}
            </div>
          </div>
        );
      })}
      <div className="text-xs text-slate-500">Games that have started show real ESPN points (LIVE, then FINAL). Everything still to come is projected, with lineups auto-optimized (9 F, 5 D, 1 UTIL, 2 G). W % / xG = betting line for that game. Tap any matchup above to switch.</div>
    </div>
  );
}

'''

R16_MSIDE = r'''function MSide({ p, right }) {
  // msside v16: real ESPN points once a game starts (news_logos.py)
  const al = right ? "flex-end" : "flex-start";
  if (!p) return <div className="m-cell" style={{ justifyContent: al }}><span className="text-sm text-slate-400">Empty</span></div>;
  const st = p.p === "G" && !p.st ? mStart(p.gs) : "";
  const stc = st === "Confirmed" ? "text-green-700" : st === "May sit" ? "text-red-600" : "text-amber-600";
  const inj = p.status && p.status !== "ACTIVE" ? M_ST[p.status] || "" : "";
  const info = (
    <div className="min-w-0" style={{ flex: 1, textAlign: right ? "right" : "left" }}>
      <div className="flex items-center gap-1 min-w-0" style={{ justifyContent: al }}>
        <button type="button" className="truncate font-medium" style={{ minWidth: 0 }} onClick={() => window.__NAV && window.__NAV.player(p)}>{shortN(p.n)}</button>
        <span style={{ flexShrink: 0, lineHeight: 0 }}><TeamLogo t={p.t} size={16} /></span>
        {inj ? <span className="text-xs text-red-600" style={{ flexShrink: 0 }}>{inj}</span> : null}
      </div>
      <div className="text-xs text-slate-500 truncate">{p.st ? <><LiveTag st={p.st} />{p.st === "L" ? " · proj " + f1(p.x0) : ""}</> : <>{st ? <span className={stc}>{st} · </span> : null}{mGame(p)}</>}</div>
    </div>
  );
  const pts = <div className="m-pts">{p.st ? (p.a == null ? "–" : f1(p.a)) : f1(p.x)}</div>;
  return <div className="m-cell">{right ? pts : info}{right ? info : pts}</div>;
}
function H2H({ x, y, s, a, b, wk, d }) {
  const rows = [];
  ["F", "D", "UTIL", "G"].forEach((sl) => {
    const A = x.start.filter((p) => p.slot === sl), B = y.start.filter((p) => p.slot === sl);
    for (let i = 0; i < Math.max(A.length, B.length); i++) rows.push([sl, A[i] || null, B[i] || null]);
  });
  const sit = (l, id) => (l.bench.length ? <div className="text-xs text-slate-500 px-3 pt-2">{teamName(s, id)} would sit: {l.bench.map((p) => shortN(p.n)).join(", ")}</div> : null);
  const line = (l) => (l.locked ? "actual " + f1(l.act) + (l.allDone ? (l.proj != null ? " (projected " + f1(l.proj) + ")" : "") : " + " + f1(l.total) + " to come") : "projected " + f1(l.total));
  return (
    <div>
      <div className="m-h2h-head">
        <div className="min-w-0"><div className="text-xs text-slate-500 truncate">{teamName(s, a)}</div><div className="m-big">{f1((x.act || 0) + x.total)}</div></div>
        <div className="text-xs text-slate-500 text-center pb-1">vs</div>
        <div className="min-w-0 text-right"><div className="text-xs text-slate-500 truncate">{teamName(s, b)}</div><div className="m-big">{f1((y.act || 0) + y.total)}</div></div>
      </div>
      {rows.length ? rows.map(([sl, p, q], i) => (
        <div key={i} className="m-row"><MSide p={p} /><div className="m-slot">{sl === "UTIL" ? "U" : sl}</div><MSide p={q} right /></div>
      )) : <div className="text-sm text-slate-400 px-3 py-3">No games for either team.</div>}
      {sit(x, a)}{sit(y, b)}
      {x.empty || y.empty ? <div className="text-xs text-slate-500 px-3 pt-2">Empty slots: {teamName(s, a)} {x.empty} · {teamName(s, b)} {y.empty}</div> : null}
      {x.locked || y.locked ? <div className="text-xs text-slate-500 px-3 pt-2">{teamName(s, a)}: {line(x)} · {teamName(s, b)}: {line(y)}</div> : null}
      {a === s.me ? <div className="px-3"><FillSlot l={x} s={s} wk={wk} d={d} /></div> : null}
      <div className="h-2"></div>
    </div>
  );
}

'''

R16_PROJVAR_OLD = r'''const projVar = (R) => { let v = (0.1 * R.total) ** 2; R.days.forEach((L) => { if (L) L.start.forEach((p) => { const sd = p.p === "G" ? 3 + 0.8 * p.x : 1.5 + 0.6 * p.x; v += sd * sd; }); }); return v; };'''
R16_PROJVAR_NEW = r'''const projVar = (R) => { let v = (0.1 * R.total) ** 2; R.days.forEach((L) => { if (L) L.start.forEach((p) => { const z = p.x0 != null ? p.x0 : p.x, sd = p.p === "G" ? 3 + 0.8 * z : 1.5 + 0.6 * z; v += sd * sd * (p.vf != null ? p.vf : 1); }); }); return v; };'''


def round16(t):
    t = block(t, "live: lineup with open slots", "function dayLineup(roster, wk, d, K) {", "function weekProj(", R16_DAYLINEUP, "dayLineup(roster, wk, d, K, cap)")
    t = lit(t, "live: win chance spread", R16_PROJVAR_OLD, R16_PROJVAR_NEW, "p.vf != null")
    t = lit(t, "live: player list", "window.__SIG = (E && E.signals) || null; livePP1(E);",
            "window.__SIG = (E && E.signals) || null; livePP1(E); window.__PLAYERS = s.players;", "window.__PLAYERS = s.players")
    t = lit(t, "live: win chance (you)", "const A = weekProj(roster || s.players.filter((p) => p.ft === s.me), w, K, done);",
            "const A = weekLive(roster || s.players.filter((p) => p.ft === s.me), w, K, s.me);", "weekLive(roster || s.players")
    t = lit(t, "live: win chance (them)", "const B = weekProj(s.players.filter((p) => p.ft === opp), w, K, done);",
            "const B = weekLive(s.players.filter((p) => p.ft === opp), w, K, opp);", "w, K, opp);")
    t = lit(t, "home: live week", "const A = weekProj(mine, wk, K, done), B = weekProj(theirs, wk, K, done);",
            "const A = weekLive(mine, wk, K, s.me), B = weekLive(theirs, wk, K, opp);", "weekLive(mine, wk, K, s.me)")
    t = lit(t, "home: actual on top (you)",
            '<div className="text-4xl">{f1(fa)}</div><div className="text-xs text-slate-500">{f1(aA)} actual + {f1(A.total)} proj</div>',
            '<div className="text-4xl">{f1(aA)}</div><div className="text-xs text-slate-500">+ {f1(A.total)} still projected · {f1(fa)} final est.</div>',
            "still projected · {f1(fa)} final est.</div>")
    t = lit(t, "home: actual on top (them)",
            '<div className="text-4xl">{f1(fb)}</div><div className="text-xs text-slate-500">{f1(aB)} actual + {f1(B.total)} proj</div>',
            '<div className="text-4xl">{f1(aB)}</div><div className="text-xs text-slate-500">+ {f1(B.total)} still projected · {f1(fb)} final est.</div>',
            "still projected · {f1(fb)} final est.</div>")
    t = lit(t, "league cards: actual (1)", '<span className="font-semibold">{f1(fx)}</span></div>',
            '<span className="font-semibold">{f1(X.act)}</span></div>', "{f1(X.act)}</span></div>")
    t = lit(t, "league cards: actual (2)", '<span className="font-semibold">{f1(fy)}</span></div>',
            '<span className="font-semibold">{f1(Y.act)}</span></div>', "{f1(Y.act)}</span></div>")
    t = lit(t, "league cards: projected final",
            '{X.act || Y.act ? <div className="text-xs text-slate-500 mt-1">Actual so far {f1(X.act)} – {f1(Y.act)}</div> : null}',
            '<div className="text-xs text-slate-500 mt-1">Projected final {f1(fx)} – {f1(fy)}</div>', "Projected final {f1(fx)}")
    t = block(t, "matchup rows: real points", "function Side({ l, s, id, wk, d }) {", "function MatchCard(", R16_SIDE, "matchup row v16")
    t = block(t, "matchup: live week", "function Matchup({ s, setS, wk, setWk }) {", "// ---------- Power rankings ----------", R16_MATCHUP, "// matchup v16:")
    t = block(t, "phone matchup: real points", "function MSide({ p, right }) {", "// ---------- round 10: one trade builder", R16_MSIDE, "msside v16")
    t = lit(t, "fill a spot: only games not started", "(wk.games[p.t] || []).includes(d) && fits(p))",
            '(wk.games[p.t] || []).includes(d) && fits(p) && gState(p.t, dt).s === "P")', 'fits(p) && gState(p.t, dt).s === "P"')
    t = lit(t, "goalie streams: only games not started", 'p.p === "G" && (wk.games[p.t] || []).includes(d) && avail(p, dt) > 0)',
            'p.p === "G" && (wk.games[p.t] || []).includes(d) && avail(p, dt) > 0 && gState(p.t, dt).s === "P")', 'avail(p, dt) > 0 && gState(p.t, dt).s === "P"')
    t = lit(t, "league table: live week", "const r = weekProj(s.players.filter((p) => p.ft === t.id), wk, K, done);",
            "const r = weekLive(s.players.filter((p) => p.ft === t.id), wk, K, t.id);", "weekLive(s.players.filter((p) => p.ft === t.id), wk, K, t.id)")
    t = lit(t, "team page: live week", "const mine = weekProj(roster, wk, K, done), theirs = o ? weekProj(s.players.filter((p) => p.ft === o), wk, K, done) : null;",
            "const mine = weekLive(roster, wk, K, id), theirs = o ? weekLive(s.players.filter((p) => p.ft === o), wk, K, o) : null;", "weekLive(roster, wk, K, id)")
    t = lit(t, "live: helpers", ROOT, R16_HELPERS + ROOT, "function weekLive(")
    for must in ("function weekLive(", "function Side(", "function Matchup(", "function H2H(", "dayLineup(roster, wk, d, K, cap)"):
        if must not in t:
            fail("fantasy-gm.html looks damaged after round 16 (" + must + ").")
    return t


_fix_before_r16 = fix


def fix(t):
    return round16(_fix_before_r16(t))

if __name__ == "__main__":
    main()
