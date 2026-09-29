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
    t = sub_once(t, "bigger logos in News", r'<div className="pt-0\.5"><TeamLogo t=\{p\.t\} size=\{\d+\} /></div>',
                 '<div className="pt-0.5"><TeamLogo t={p.t} size={36} /></div>', '<TeamLogo t={p.t} size={36} /></div>')
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
    for f, fn in PY_FIXES.items():
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


if __name__ == "__main__":
    main()
