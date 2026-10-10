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


# ---------- round 17: player points from ESPN box scores (same numbers as FantasyCast), no "DNP" ----------

SYNC17_START = "    sp_of = {d_.isoformat(): pid_ for pid_, d_ in period_date.items()}\n"
SYNC17_END = "        daily[dd_] = day_\n"
SYNC17_NEW = r'''    sp_of = {d_.isoformat(): pid_ for pid_, d_ in period_date.items()}
    # 3c) per-player points from ESPN box scores (news_logos.py round 17)
    cur_sp_ = lg.get("scoringPeriodId") or (lg.get("status") or {}).get("latestScoringPeriod")
    if cur_sp_:
        span_ = [(pdate(x_), x_) for x_ in range(max(1, int(cur_sp_) - 6), int(cur_sp_) + 1)]
    else:
        span_ = [(dd_, sp_of.get(dd_)) for dd_ in ((today_et - timedelta(days=b_)).isoformat() for b_ in range(6, -1, -1))]
    daily = {}
    for dd_, sp_ in span_:
        if not sp_:
            continue
        day_ = {}
        try:
            rs_ = get(LEAGUE, params=[("view", "mMatchupScore"), ("view", "mScoreboard"), ("scoringPeriodId", sp_)])
            dump(f"espn-raw-daily-{dd_}.json", rs_)
            for m_ in rs_.get("schedule", []):
                for side_ in ("home", "away"):
                    ts_ = m_.get(side_) or {}
                    ents_ = (ts_.get("rosterForCurrentScoringPeriod") or {}).get("entries") or []
                    if not ents_:
                        continue
                    tm_ = {}
                    for en_ in ents_:
                        pe_ = en_.get("playerPoolEntry") or {}
                        pts_ = None
                        for st_ in (pe_.get("player") or {}).get("stats") or []:
                            if st_.get("scoringPeriodId") == sp_ and st_.get("statSourceId") == 0:
                                pts_ = st_.get("appliedTotal")
                                break
                        if pts_ is None:
                            pts_ = pe_.get("appliedStatTotal")
                        tm_[str(en_.get("playerId"))] = [None if pts_ is None else round(pts_, 2), en_.get("lineupSlotId")]
                    day_[str(ts_.get("teamId"))] = tm_
        except Exception as ex:
            print(f"(daily) ESPN box scores for {dd_} failed: {ex}")
        mine_n_ = sum(1 for v in day_.get(str(MY_TEAM_ID), {}).values() if v[0])
        print(f"(daily) {dd_} (scoring period {sp_}): {len(day_)} teams, {mine_n_} of your players with points")
        if day_:
            daily[dd_] = day_
'''

_fix_sync_before_r17 = PY_FIXES[SYNC]


def fix_sync17(t):
    t = _fix_sync_before_r17(t)
    t = sub_once(t, "sync: player points from ESPN box scores", re.escape(SYNC17_START) + r".*?" + re.escape(SYNC17_END),
                 SYNC17_NEW, "# 3c) per-player points from ESPN box scores", re.S)
    py_ok(SYNC, t)
    return t


PY_FIXES[SYNC] = fix_sync17


def round17(t):
    t = lit(t, "matchup rows: no DNP",
            '<div className="font-semibold">{p.a == null ? (p.st === "F" ? <span className="text-xs text-slate-400 font-normal">DNP</span> : "–") : f1(p.a)}</div>',
            '<div className="font-semibold">{p.a == null ? "–" : f1(p.a)}</div>',
            '<div className="font-semibold">{p.a == null ? "–" : f1(p.a)}</div>')
    return t


_fix_before_r17 = fix


def fix(t):
    return round17(_fix_before_r17(t))

def fix(t):
    return round16(_fix_before_r16(t))

# ---------- round 18: only players whose team plays that day, sorted F / D / UTIL / G ----------

def round18(t):
    t = lit(t, "matchup: skip players with no game",
            'if (plays(p) ? gState(p.t, dt).s === "P" : v[0] == null) return;',
            'if (plays(p) ? gState(p.t, dt).s === "P" : !v[0]) return;',
            ': !v[0]) return;')
    t = lit(t, "matchup: sort rows by slot",
            "return { start: [...rows, ...L.start], bench: L.bench,",
            "return { start: [...rows, ...L.start].sort((a, b) => ({ F: 0, D: 1, UTIL: 2, G: 3 }[a.slot] ?? 4) - ({ F: 0, D: 1, UTIL: 2, G: 3 }[b.slot] ?? 4)), bench: L.bench,",
            "UTIL: 2, G: 3 }[a.slot]")
    t = lit(t, "nudges: only real games",
            'if (!p || !v || v[0] == null || gState(p.t, dt).s !== "F") return;',
            'if (!p || !v || v[0] == null || !(SCHED[p.t] && SCHED[p.t].has(dt)) || gState(p.t, dt).s !== "F") return;',
            "SCHED[p.t].has(dt)) || gState")
    return t


_fix_before_r18 = fix


def fix(t):
    return round18(_fix_before_r18(t))

# ---------- round 19: player pop-up uses real ESPN points (season total, tonight, games already played) ----------

LT19_ANCHOR = "  // ---------- styles (dark, matches the app) ----------"
LT19_HELPER = r'''  // real ESPN points for one player on one day (news_logos.py round 19)
  const realPts = (p, d) => {
    const D = (((window.ESPN_DATA || {}).daily) || {})[d] || {}, id = String(p.id || "").replace(/^e/, "");
    for (const tm of Object.values(D)) { const v = (tm || {})[id]; if (v && v[0] != null) return v[0]; }
    return null;
  };

'''

_fix_lines_before_r19 = JS_FIXES[LINES]


def fix_lines19(t):
    t = _fix_lines_before_r19(t)
    t = lit(t, "pop-up: real points helper", LT19_ANCHOR, LT19_HELPER + LT19_ANCHOR, "const realPts =")
    t = lit(t, "pop-up: rest of week skips games already started",
            'const wkIdx = hasId ? (wk.games[p.t] || []).filter((i) => ((wk.dates || [])[i] || "") >= today) : [];',
            'const wkIdx = hasId ? (wk.games[p.t] || []).filter((i) => ((wk.dates || [])[i] || "") >= today && !(H.gState && H.gState(p.t, wk.dates[i]).s !== "P")) : [];',
            "H.gState(p.t, wk.dates[i]).s")
    t = lit(t, "pop-up: tonight's game",
            'const hurt = hasId && ((p.status && p.status !== "ACTIVE") || (back.d && back.d > today));',
            'const hurt = hasId && ((p.status && p.status !== "ACTIVE") || (back.d && back.d > today));\n'
            '    const LT = H.LiveTag || (() => null), started = (d) => !!(H.gState && H.gState(it.t, d).s !== "P"), tn = hasId && started(today) ? { a: realPts(p, today), st: H.gState(it.t, today).s } : null;',
            "const LT = H.LiveTag")
    t = lit(t, "pop-up: season points from ESPN",
            '<H.Card label={`${L.season} fantasy pts`} value={f.cur ? H.f1(f.cur[0]) : "–"} sub={fmt(f.cur)} />',
            '<H.Card label={`${L.season} fantasy pts`} value={hasId ? H.f1(p.tot || 0) : f.cur ? H.f1(f.cur[0]) : "–"} sub={hasId ? <>{p.gp ? `${p.gp} GP · ${H.f1(p.tot / p.gp)}/game` : "no games yet"}{tn ? <> · tonight {tn.a == null ? "–" : H.f1(tn.a)} <LT st={tn.st} /></> : null}</> : fmt(f.cur)} />',
            "tonight {tn.a")
    t = lit(t, "pop-up: projection shows how it moved",
            '<H.Card label="Projection / game" value={hasId ? H.f1(H.effAvg(p, K)) : "–"} sub={hasId ? `${MODE[window.__PMODE] || ""} mode · ESPN ${H.f1(p.pavg)}` : "no projection"} />',
            '<H.Card label="Projection / game" value={hasId ? H.f1(H.effAvg(p, K)) : "–"} sub={hasId ? `${MODE[window.__PMODE] || ""} mode · ESPN ${H.f1(p.avg)}${p.gp ? ` · was ${H.f1(H.effAvg({ ...p, gp: 0, tot: 0 }, K))} before ${p.gp} game${p.gp === 1 ? "" : "s"}` : ""}` : "no projection"} />',
            "before ${p.gp} game")
    t = lit(t, "pop-up: real points for games already played",
            '<td className="py-1 text-right font-semibold">{r ? H.f1(r.x) : ""}</td>',
            '<td className="py-1 text-right font-semibold">{hasId && started(g.d) ? <>{realPts(p, g.d) == null ? "–" : H.f1(realPts(p, g.d))} <LT st={H.gState(it.t, g.d).s} /></> : r ? H.f1(r.x) : ""}</td>',
            "realPts(p, g.d) == null")
    babel_ok(t, LINES)
    return t


JS_FIXES[LINES] = fix_lines19


def round19(t):
    t = lit(t, "pop-up gets live helpers", "const LH = { effAvg,", "const LH = { gState, actDay, LiveTag, effAvg,", "const LH = { gState, actDay, LiveTag,")
    return t


_fix_before_r19 = fix


def fix(t):
    return round19(_fix_before_r19(t))

# ---------- round 20: Goalie streams lists every game's Daily Faceoff starting goalies ----------

R20_GOALIES = r'''function GoalieStreams({ s, wk }) {
  // goalie streams v20: every game's Daily Faceoff starters, then the best free agents (news_logos.py)
  const K = s.blend, today = todayISO(), dates = wk.dates || [];
  const base = useMemo(() => winChance(s), [s]);
  const st = strategy(base);
  const byName = useMemo(() => { const o = {}; s.players.forEach((p) => { if (p.p === "G") o[nrm(p.n)] = p; }); return o; }, [s.players]);
  const raw = (window.ESPN_DATA || {}).goalies || s.goalies || {};
  const GD = (window.GAMES_DATA || {}).games || {};
  const tagOf = (status) => { const x = (status || "").toLowerCase(); return x.includes("confirm") && !x.includes("un") ? ["Confirmed", "bg-green-100 text-green-700"] : /likely|expected|project/.test(x) ? ["Likely", "bg-amber-100 text-amber-800"] : ["Unconfirmed", "bg-slate-200 text-slate-600"]; };
  const starters = (dt) => {
    const day = raw[dt] || {}, g = GD[dt] || {};
    const side = (t) => { const e = Object.entries(day).find(([, x]) => x && x.team === t); return { t, name: e ? e[0] : null, status: e ? e[1].status : "", p: e ? byName[nrm(e[0])] || null : null, o: oddsFor(t, dt) }; };
    return Object.entries(g).filter(([, v]) => v.h === 1).map(([home, v]) => ({ away: side(v.o), home: side(home), st: v.st, dt }))
      .sort((a, b) => String(a.st || "").localeCompare(String(b.st || "")));
  };
  const days = dates.map((dt, d) => ({ dt, d })).filter((x) => x.dt >= today).map(({ dt, d }) => ({ dt, games: starters(dt), list: s.players
    .filter((p) => p.ft === "fa" && p.p === "G" && (wk.games[p.t] || []).includes(d) && avail(p, dt) > 0 && gState(p.t, dt).s === "P")
    .map((p) => { const gs = gStart(p, dt); return { p, gs, o: oddsFor(p.t, dt), g: gameOf(p.t, dt), v: effAvg(p, K, dt) * gs.v }; })
    .filter((x) => x.gs.v >= 0.4).sort((a, b) => b.v - a.v).slice(0, 3) }));
  const own = (p) => (!p ? null : p.ft === s.me ? <span className="text-blue-600 font-semibold">yours</span> : p.ft === "fa" ? <span className="text-green-700 font-semibold">FA</span> : <span>{teamName(s, p.ft)}</span>);
  const Gl = ({ x, right }) => {
    const tg = x.name ? tagOf(x.status) : null;
    const bits = [own(x.p), x.o ? "W " + Math.round(x.o.win * 100) + "%" : null].filter(Boolean);
    return (
      <div className={"flex items-center gap-2 min-w-0 flex-1" + (right ? " flex-row-reverse text-right" : "")}>
        <TeamLogo t={x.t} size={28} />
        <div className="min-w-0">
          <div className={"flex flex-wrap items-center gap-x-2 gap-y-0.5" + (right ? " justify-end" : "")}>
            {x.name ? (x.p ? <PN p={x.p} className="truncate font-medium" /> : <span className="font-medium truncate">{x.name}</span>) : <span className="text-slate-400">Not announced</span>}
            {tg ? <span className={"text-xs px-1.5 py-0.5 rounded " + tg[1]}>{tg[0]}</span> : null}
          </div>
          {bits.length ? <div className="text-xs text-slate-500">{bits.map((b, i) => <span key={i}>{i ? " · " : ""}{b}</span>)}</div> : null}
        </div>
      </div>
    );
  };
  const head = (t) => <div className="text-xs uppercase tracking-wide text-slate-500 mt-3 mb-1">{t}</div>;
  return (
    <Section title="Goalie streams" sub="Every game's starting goalies from Daily Faceoff, then the best free-agent goalies for each day left this week. Win chance from betting odds.">
      {st ? <div className="text-sm mb-2"><span className="font-semibold">{st[0]}</span><span className="text-slate-500"> · You're {wpTxt(base)} to win this week. {base >= 0.75 ? "Only stream a confirmed starter with a good win chance." : base < 0.4 ? "A good goalie stream is your best upside." : "Stream when a confirmed starter has a good matchup."}</span></div> : null}
      {days.length ? days.map(({ dt, games, list }) => (
        <div key={dt} className="mt-5">
          <div className="font-semibold">{dt === today ? "Today" : dayLabel(dt)}</div>
          {head("Starting goalies (Daily Faceoff)")}
          {games.length ? games.map((gm, i) => { const gs = gState(gm.home.t, dt); return (
            <div key={i} className="flex items-center gap-3 py-2.5 border-t border-slate-100">
              <Gl x={gm.away} />
              <div className="text-xs text-slate-500 text-center whitespace-nowrap" style={{ minWidth: 60 }}>{gs.s !== "P" ? <LiveTag st={gs.s} /> : gameTime({ st: gm.st })}<div className="text-slate-400">@</div></div>
              <Gl x={gm.home} right />
            </div>
          ); }) : <div className="text-sm text-slate-400 py-2 border-t border-slate-100">No game times loaded for this day.</div>}
          {head("Free agents to stream")}
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


def round20(t):
    t = block(t, "goalie streams: every game's starting goalies", "function GoalieStreams({ s, wk }) {",
              "// ---------- moves used from ESPN", R20_GOALIES, "goalie streams v20")
    return t


_fix_before_r20 = fix


def fix(t):
    return round20(_fix_before_r20(t))

# ---------- round 21: live game scores, nicer LIVE / FINAL tags ----------

# --- espn_sync.py: keep each game's score, period and clock with the game state ---
SYNC21_OLD = '''            for side_ in ("homeTeam", "awayTeam"):
                ab_ = str((g_.get(side_) or {}).get("abbrev") or "").upper()
                gs_[ALIAS.get(ab_, ab_)] = {"s": s_, "f": round(f_, 2)}
'''
SYNC21_NEW = '''            pd_ = g_.get("periodDescriptor") or {}
            ck_ = g_.get("clock") or {}
            pdl_ = "OT" if pd_.get("periodType") == "OT" else "SO" if pd_.get("periodType") == "SO" else {1: "1st", 2: "2nd", 3: "3rd"}.get(per_, str(per_))
            hs_, as_ = (g_.get("homeTeam") or {}).get("score"), (g_.get("awayTeam") or {}).get("score")
            for side_, me_, op_ in (("homeTeam", hs_, as_), ("awayTeam", as_, hs_)):
                ab_ = str((g_.get(side_) or {}).get("abbrev") or "").upper()
                gs_[ALIAS.get(ab_, ab_)] = {"s": s_, "f": round(f_, 2), "my": me_, "op": op_, "per": pdl_,
                                            "clk": ck_.get("timeRemaining") or "", "int": bool(ck_.get("inIntermission"))}
'''

_fix_sync_before_r21 = PY_FIXES[SYNC]


def fix_sync21(t):
    t = _fix_sync_before_r21(t)
    t = lit(t, "sync: game scores and clock", SYNC21_OLD, SYNC21_NEW, '"my": me_')
    py_ok(SYNC, t)
    return t


PY_FIXES[SYNC] = fix_sync21

# --- lines-tab.js: pop-up tags show the score too ---
_fix_lines_before_r21 = JS_FIXES[LINES]


def fix_lines21(t):
    t = _fix_lines_before_r21(t)
    t = lit(t, "pop-up: score on tonight's tag", "<LT st={tn.st} />", "<LT st={tn.st} t={it.t} dt={today} />", "<LT st={tn.st} t={it.t}")
    t = lit(t, "pop-up: score on played games", "<LT st={H.gState(it.t, g.d).s} />",
            "<LT st={H.gState(it.t, g.d).s} t={it.t} dt={g.d} />", "<LT st={H.gState(it.t, g.d).s} t={it.t}")
    babel_ok(t, LINES)
    return t


JS_FIXES[LINES] = fix_lines21

# --- fantasy-gm.html ---
R21_CSS = r'''  /* round 21 live (news_logos.py) */
  .gm-dot { width: 6px; height: 6px; border-radius: 99px; background: var(--bad); display: inline-block; animation: gmPulse 1.4s ease-in-out infinite; }
  @keyframes gmPulse { 0%, 100% { opacity: 1; } 50% { opacity: .25; } }
  .gm-pill { font-size: 10px; font-weight: 700; letter-spacing: .06em; padding: 2px 6px; border-radius: 5px; line-height: 1.3; }
'''

R21_TAG_OLD = r'''const LiveTag = ({ st }) => (st === "L" ? <span className="text-xs font-semibold text-red-600">LIVE</span> : st === "F" ? <span className="text-xs text-slate-500">FINAL</span> : null);'''
R21_TAG_NEW = r'''const gScore = (t, dt) => { const L = ((window.__LIVESC || {})[dt] || {})[t]; return L || ((((window.ESPN_DATA || {}).gstate || {})[dt]) || {})[t] || null; };
const LiveTag = ({ st, t, dt }) => {
  // live tag v21: pill + score from the player's team's side (news_logos.py)
  if (st !== "L" && st !== "F") return null;
  const sc = t && dt ? gScore(t, dt) : null;
  const has = !!(sc && sc.my != null && sc.op != null);
  const res = has && st === "F" ? (sc.my > sc.op ? "W" : sc.my < sc.op ? "L" : "") : "";
  const tail = !sc ? "" : st === "F" ? (sc.per === "OT" || sc.per === "SO" ? " " + sc.per : "") : sc.int ? " · " + sc.per + " int." : sc.per ? " · " + sc.per + (sc.clk ? " " + sc.clk : "") : "";
  return (
    <span className="inline-flex items-center gap-1.5 whitespace-nowrap align-middle">
      {st === "L" ? <span className="gm-pill inline-flex items-center gap-1 bg-red-100 text-red-600"><span className="gm-dot"></span>LIVE</span> : <span className="gm-pill bg-slate-200 text-slate-500">FINAL</span>}
      {has ? <span className={"text-xs font-semibold " + (res === "W" ? "text-green-700" : res === "L" ? "text-red-600" : "text-slate-700")}>{res ? res + " " : ""}{sc.my}–{sc.op}<span className="font-normal text-slate-500">{tail}</span></span> : null}
    </span>
  );
};'''

R21_POLL = r'''const [, tick] = useState(0);
  useEffect(() => {
    // round 21: live NHL scores straight from the NHL every minute (falls back to the sync's copy if blocked)
    let dead = false;
    const AL = { LAK: "LA", NJD: "NJ", SJS: "SJ", TBL: "TB", UTAH: "UTA", ARI: "UTA" };
    const pull = () => fetch("https://api-web.nhle.com/v1/score/now").then((r) => (r.ok ? r.json() : null)).then((js) => {
      if (dead || !js || !js.games) return;
      const out = {};
      js.games.forEach((g) => {
        const d = g.gameDate; if (!d) return;
        const st = g.gameState, s = st === "FINAL" || st === "OFF" ? "F" : st === "LIVE" || st === "CRIT" ? "L" : "P";
        const pd = g.periodDescriptor || {}, n = pd.number || 1, ck = g.clock || {};
        const rem = ck.secondsRemaining == null ? 1200 : ck.secondsRemaining;
        const f = s === "F" ? 1 : s === "P" ? 0 : Math.min(0.99, ((n - 1) * 1200 + 1200 - rem) / 3600);
        const per = pd.periodType === "OT" ? "OT" : pd.periodType === "SO" ? "SO" : ["", "1st", "2nd", "3rd"][n] || String(n);
        const hs = (g.homeTeam || {}).score, as = (g.awayTeam || {}).score;
        out[d] = out[d] || {};
        [[g.homeTeam, hs, as], [g.awayTeam, as, hs]].forEach(([T, my, op]) => { const a = T && (AL[T.abbrev] || T.abbrev); if (a) out[d][a] = { s, f, my, op, per, clk: ck.timeRemaining || "", int: !!ck.inIntermission }; });
      });
      window.__LIVESC = out; tick((x) => x + 1);
    }).catch(() => {});
    pull();
    const id = setInterval(pull, 60 * 1000);
    return () => { dead = true; clearInterval(id); };
  }, []);'''


def round21(t):
    t = lit(t, "live: styles", "</style>", R21_CSS + "</style>", "round 21 live")
    t = lit(t, "live: tag with score", R21_TAG_OLD, R21_TAG_NEW, "live tag v21")
    t = lit(t, "live: newest game state first",
            "const x = ((((window.ESPN_DATA || {}).gstate || {})[dt]) || {})[t];",
            "const x = ((window.__LIVESC || {})[dt] || {})[t] || ((((window.ESPN_DATA || {}).gstate || {})[dt]) || {})[t];",
            "(window.__LIVESC || {})[dt] || {})[t] ||")
    t = lit(t, "live: scores every minute", "const [, tick] = useState(0);", R21_POLL, "round 21: live NHL scores")
    t = lit(t, "matchup rows: score on tag", "{p.st ? <LiveTag st={p.st} /> : gameTime(g)}",
            "{p.st ? <LiveTag st={p.st} t={p.t} dt={p.dt} /> : gameTime(g)}", "<LiveTag st={p.st} t={p.t} dt={p.dt} /> : gameTime(g)")
    t = lit(t, "phone matchup: score on tag", '<><LiveTag st={p.st} />{p.st === "L"',
            '<><LiveTag st={p.st} t={p.t} dt={p.dt} />{p.st === "L"', '<LiveTag st={p.st} t={p.t} dt={p.dt} />{p.st === "L"')
    t = lit(t, "matchup day header: tag",
            '{tag ? <span className={"text-xs font-semibold " + (tag === "LIVE" ? "text-red-600" : "text-slate-500")}>{tag}</span> : null}',
            '{tag ? <LiveTag st={tag === "LIVE" ? "L" : "F"} /> : null}', '<LiveTag st={tag === "LIVE" ? "L" : "F"} />')
    t = lit(t, "goalie streams: game score",
            '{gs.s !== "P" ? <LiveTag st={gs.s} /> : gameTime({ st: gm.st })}',
            '{gs.s !== "P" ? <><LiveTag st={gs.s} />{(() => { const sc = gScore(gm.home.t, dt); return sc && sc.my != null ? <div className="text-sm font-semibold text-slate-700 mt-0.5">{sc.op} – {sc.my}{sc.s === "L" && sc.per ? <div className="text-xs text-slate-500 font-normal">{sc.int ? sc.per + " int." : sc.per + " " + (sc.clk || "")}</div> : null}</div> : null; })()}</> : gameTime({ st: gm.st })}',
            "gScore(gm.home.t, dt)")
    return t


_fix_before_r21 = fix


def fix(t):
    return round21(_fix_before_r21(t))

# ---------- round 22: NHL box-score stat line under each player (G, A, +/-, SOG, PIM, HIT, BLK, TOI / goalie W, SV, GA) ----------

# --- espn_sync.py: download box scores for games that started today / yesterday and match them to league players ---
SYNC22_DEFS_OLD = "    gstate = {}\n"
SYNC22_DEFS_NEW = '''    import unicodedata as ud_

    def _toks(n):
        n = ud_.normalize("NFD", n or "").encode("ascii", "ignore").decode().lower().replace(".", " ").replace("-", " ").replace("'", "")
        return n.split()

    def _nk(n):
        p = _toks(n)
        return (p[0][0] + " " + " ".join(p[1:])) if len(p) > 1 else " ".join(p)

    def _nk2(n):
        p = _toks(n)
        return (p[0][0] + " " + p[-1]) if len(p) > 1 else " ".join(p)

    _pidx = {}
    for p_ in players:
        if p_.get("n"):
            for k_ in {_nk(p_["n"]), _nk2(p_["n"])}:
                _pidx.setdefault((k_, p_["t"]), p_["id"])
    gstate = {}
    pstat = {}
'''

SYNC22_BOX_OLD = "        gstate[dd_] = gs_\n"
SYNC22_BOX_NEW = '''        pst_ = {}
        for g_ in js_.get("games", []):  # 3d) player box scores (news_logos.py round 22)
            if str(g_.get("gameState") or "") not in ("LIVE", "CRIT", "FINAL", "OFF") or not g_.get("id"):
                continue
            try:
                bx_ = requests.get(f"https://api-web.nhle.com/v1/gamecenter/{g_['id']}/boxscore", headers={"User-Agent": "Mozilla/5.0"}, timeout=20).json()
            except Exception as ex:
                print(f"(daily) box score {g_.get('id')} failed: {ex}")
                continue
            pbg_ = bx_.get("playerByGameStats") or {}
            for side_ in ("homeTeam", "awayTeam"):
                tab_ = str((bx_.get(side_) or g_.get(side_) or {}).get("abbrev") or "").upper()
                tab_ = ALIAS.get(tab_, tab_)
                grp_ = pbg_.get(side_) or {}
                for x_ in (grp_.get("forwards") or []) + (grp_.get("defense") or []) + (grp_.get("goalies") or []):
                    nm_ = (x_.get("name") or {}).get("default") or ""
                    pid_ = _pidx.get((_nk(nm_), tab_)) or _pidx.get((_nk2(nm_), tab_))
                    if not pid_:
                        continue
                    if "saves" in x_ or "goalsAgainst" in x_ or "saveShotsAgainst" in x_:
                        if not x_.get("toi") or x_.get("toi") == "00:00":
                            continue
                        pst_[str(pid_)] = {"sv": x_.get("saves") or 0, "ga": x_.get("goalsAgainst") or 0,
                                           "dec": x_.get("decision") or "", "toi": x_.get("toi") or ""}
                    else:
                        pst_[str(pid_)] = {"g": x_.get("goals") or 0, "a": x_.get("assists") or 0, "pm": x_.get("plusMinus") or 0,
                                           "sog": x_.get("sog") or 0, "pim": x_.get("pim") or 0, "hit": x_.get("hits") or 0,
                                           "blk": x_.get("blockedShots") or 0, "toi": x_.get("toi") or ""}
        pstat[dd_] = pst_
        print(f"(daily) {dd_}: box-score lines for {len(pst_)} league players")
        gstate[dd_] = gs_
'''

SYNC22_SAVE_OLD = '    data["gstate"] = gstate\n'
SYNC22_SAVE_NEW = '    data["gstate"] = gstate\n    data["pstat"] = pstat\n'

_fix_sync_before_r22 = PY_FIXES[SYNC]


def fix_sync22(t):
    t = _fix_sync_before_r22(t)
    t = lit(t, "sync: name matching for box scores", SYNC22_DEFS_OLD, SYNC22_DEFS_NEW, "def _nk(")
    t = lit(t, "sync: player box scores", SYNC22_BOX_OLD, SYNC22_BOX_NEW, "3d) player box scores")
    t = lit(t, "sync: save box scores", SYNC22_SAVE_OLD, SYNC22_SAVE_NEW, 'data["pstat"] = pstat')
    py_ok(SYNC, t)
    return t


PY_FIXES[SYNC] = fix_sync22

# --- fantasy-gm.html: stat line under each player whose game has started ---
R22_HELPERS = r'''// ---------- round 22: NHL box-score stat lines (news_logos.py) ----------
const pStat = (p, dt) => { const id = String((p && p.id) || "").replace(/^e/, ""); return ((((window.ESPN_DATA || {}).pstat || {})[dt]) || {})[id] || null; };
const statLine = (x) => {
  if (!x) return "";
  if (x.sv != null) return [x.dec || null, x.sv + " SV", x.ga + " GA", x.toi ? x.toi + " TOI" : null].filter(Boolean).join(", ");
  const n = (v, l) => (v ? (v > 1 ? v + " " + l : l) : null);
  return [n(x.g, "G"), n(x.a, "A"), (x.pm > 0 ? "+" : "") + (x.pm || 0), n(x.sog, "SOG"), n(x.pim, "PIM"), n(x.hit, "HIT"), n(x.blk, "BLK"), x.toi ? x.toi + " TOI" : null].filter(Boolean).join(", ");
};

'''


def round22(t):
    t = lit(t, "stat lines: helpers", ROOT, R22_HELPERS + ROOT, "const statLine =")
    t = lit(t, "matchup rows: stat line",
            "{p.st ? <LiveTag st={p.st} t={p.t} dt={p.dt} /> : gameTime(g)}</div> : null}",
            '{p.st ? <LiveTag st={p.st} t={p.t} dt={p.dt} /> : gameTime(g)}</div> : null}\n'
            '                    {p.st && statLine(pStat(p, p.dt)) ? <div className="text-xs text-slate-400 mt-0.5">{statLine(pStat(p, p.dt))}</div> : null}',
            '<div className="text-xs text-slate-400 mt-0.5">{statLine(pStat(p, p.dt))}</div>')
    t = lit(t, "phone matchup: stat line", "{mGame(p)}</>}</div>",
            '{mGame(p)}</>}</div>{p.st && statLine(pStat(p, p.dt)) ? <div className="text-xs text-slate-400 truncate">{statLine(pStat(p, p.dt))}</div> : null}',
            '<div className="text-xs text-slate-400 truncate">{statLine(')
    return t


_fix_before_r22 = fix


def fix(t):
    return round22(_fix_before_r22(t))

# ---------- round 23: full game box score in the player pop-up ----------

# --- espn_sync.py: keep the rest of the box-score stats ---
_fix_sync_before_r23 = PY_FIXES[SYNC]


def fix_sync23(t):
    t = _fix_sync_before_r23(t)
    t = lit(t, "sync: full skater box score",
            '"blk": x_.get("blockedShots") or 0, "toi": x_.get("toi") or ""}',
            '"blk": x_.get("blockedShots") or 0, "toi": x_.get("toi") or "", "ppg": x_.get("powerPlayGoals") or 0, '
            '"fo": x_.get("faceoffWinningPctg"), "shf": x_.get("shifts"), "gv": x_.get("giveaways") or 0, "tk": x_.get("takeaways") or 0}',
            '"ppg": x_.get("powerPlayGoals")')
    t = lit(t, "sync: full goalie box score",
            '"dec": x_.get("decision") or "", "toi": x_.get("toi") or ""}',
            '"dec": x_.get("decision") or "", "toi": x_.get("toi") or "", "sa": x_.get("shotsAgainst"), "svp": x_.get("savePctg"), '
            '"es": x_.get("evenStrengthShotsAgainst") or "", "pp": x_.get("powerPlayShotsAgainst") or "", "sh": x_.get("shorthandedShotsAgainst") or ""}',
            '"svp": x_.get("savePctg")')
    py_ok(SYNC, t)
    return t


PY_FIXES[SYNC] = fix_sync23

# --- lines-tab.js: box-score section in the pop-up, for the day you tapped on ---
LT23_BOX = r'''        {(() => {
          // game box score v23 (news_logos.py)
          const gd = it.gd || today, gst = hasId && H.gState ? H.gState(it.t, gd) : null;
          if (!gst || gst.s === "P" || !H.pStat) return null;
          const x = H.pStat(p, gd), fp = realPts(p, gd), sc = s.sc || {};
          const tile = (l, v, hl) => <div key={l} className="rounded-lg border border-slate-200 px-2 py-1.5 text-center"><div className="text-[10px] uppercase tracking-wide text-slate-500">{l}</div><div className={"font-semibold " + (hl ? "text-green-700" : "")}>{v}</div></div>;
          let tiles = [], rows = [];
          if (x && x.sv != null) {
            tiles = [tile("Decision", x.dec || "–", x.dec === "W"), tile("Saves", x.sa != null ? x.sv + "/" + x.sa : x.sv), tile("SV%", x.svp != null ? Number(x.svp).toFixed(3).replace(/^0/, "") : "–"), tile("GA", x.ga), tile("TOI", x.toi || "–"), tile("EV shots", x.es || "–"), tile("PP shots", x.pp || "–"), tile("SH shots", x.sh || "–")];
            rows = [["Win", x.dec === "W" ? 1 : 0, sc.W ?? 5], ["OT loss", x.dec === "O" ? 1 : 0, sc.OTL ?? 1], ["Saves", x.sv, sc.SV ?? 0.6], ["Goals against", x.ga, sc.GA ?? -3]];
          } else if (x) {
            tiles = [tile("G", x.g, x.g > 0), tile("A", x.a, x.a > 0), tile("PTS", (x.g || 0) + (x.a || 0), (x.g || 0) + (x.a || 0) > 0), tile("+/-", (x.pm > 0 ? "+" : "") + (x.pm || 0), x.pm > 0), tile("SOG", x.sog), tile("PPG", x.ppg ?? 0), tile("PIM", x.pim), tile("HIT", x.hit), tile("BLK", x.blk), tile("FO%", x.fo ? Math.round(x.fo * 100) + "%" : "–"), tile("Takeaways", x.tk ?? 0), tile("Giveaways", x.gv ?? 0), tile("Shifts", x.shf ?? "–"), tile("TOI", x.toi || "–")];
            rows = [["Goals", x.g, sc.G ?? 6], ["Assists", x.a, sc.A ?? 4], ["+/-", x.pm, sc.PM ?? 2], ["Shots", x.sog, sc.SOG ?? 1], ["Hits", x.hit, sc.HIT ?? 0.1], ["Blocks", x.blk, sc.BLK ?? 1]];
          }
          const est = rows.reduce((a, r) => a + (r[1] || 0) * r[2], 0);
          const parts = rows.filter((r) => r[1]).map((r) => `${r[0]} ${r[1]} × ${r[2]} = ${H.f1(r[1] * r[2])}`);
          if (fp != null && rows.length && Math.abs(fp - est) >= 0.05) parts.push(`other (power play, shorthanded, shutout) ${fp - est > 0 ? "+" : ""}${H.f1(fp - est)}`);
          return (
            <div className="mt-4">
              <div className="flex flex-wrap items-center gap-2 mb-2">
                <div className="font-medium text-sm">Game box score · {H.dayLabel(gd)}</div>
                {H.LiveTag ? <H.LiveTag st={gst.s} t={it.t} dt={gd} /> : null}
                <span className="ml-auto font-semibold">{fp == null ? "–" : H.f1(fp)} <span className="text-xs text-slate-500 font-normal">fantasy pts</span></span>
              </div>
              {x ? <div className="grid grid-cols-4 md:grid-cols-7 gap-2">{tiles}</div> : <div className="text-xs text-slate-400">The box score appears after the next sync (every 10 minutes during games).</div>}
              {parts.length ? <div className="mt-2 text-xs text-slate-500">{parts.join(" · ")}</div> : null}
            </div>
          );
        })()}
'''

_fix_lines_before_r23 = JS_FIXES[LINES]


def fix_lines23(t):
    t = _fix_lines_before_r23(t)
    t = lit(t, "pop-up: remember the game day you tapped",
            "const cur = it || { name: real.n, key: nk(real.n), t: real.t, g: real.p, p: real };",
            "const cur = it || { name: real.n, key: nk(real.n), t: real.t, g: real.p, p: real, gd: p.dt };",
            "gd: p.dt")
    t = lit(t, "pop-up: game box score", "        {games.length > 0 && (", LT23_BOX + "        {games.length > 0 && (", "game box score v23")
    babel_ok(t, LINES)
    return t


JS_FIXES[LINES] = fix_lines23


# --- fantasy-gm.html: give the pop-up the box-score helpers ---
def round23(t):
    t = lit(t, "pop-up gets box-score helpers", "const LH = { gState, actDay, LiveTag, effAvg,",
            "const LH = { gState, actDay, LiveTag, pStat, gScore, effAvg,", "LiveTag, pStat, gScore,")
    return t


_fix_before_r23 = fix


def fix(t):
    return round23(_fix_before_r23(t))

# ---------- round 24: a player only counts on a day if ESPN has him on that day's roster ----------
R24_HELPER = r'''// ---------- round 24: a player counts on a day only if ESPN has him on that day's roster (news_logos.py) ----------
const onEspnDay = (AD, p) => !AD || !Object.keys(AD).length || AD[String(p.id).replace(/^e/, "")] != null;

'''


def round24(t):
    t = lit(t, "roster check: helper", ROOT, R24_HELPER + ROOT, "const onEspnDay =")
    t = lit(t, "roster check: projected day total",
            "const full = opt && opt.detail ? dayLineup(roster, wk, d, K).total : null;",
            "const full = opt && opt.detail ? dayLineup(roster.filter((p) => onEspnDay(dt ? actDay(tid, dt) : null, p)), wk, d, K).total : null;",
            "dayLineup(roster.filter((p) => onEspnDay(")
    t = lit(t, "roster check: days with no games started",
            "const L = dayLineup(r, wk, d, K);",
            "const L = dayLineup(r.filter((p) => onEspnDay(AD, p)), wk, d, K);",
            "dayLineup(r.filter((p) => onEspnDay(AD, p)), wk, d, K);")
    t = lit(t, "roster check: rest of a live day",
            "dayLineup(r.filter((p) => !done.has(p.id) && !lk(p)), wk, d, K, cap)",
            "dayLineup(r.filter((p) => onEspnDay(AD, p) && !done.has(p.id) && !lk(p)), wk, d, K, cap)",
            "onEspnDay(AD, p) && !done.has(p.id)")
    t = lit(t, "roster check: ESPN lineup check",
            "const toStart = L.start.filter((p) => !act(p) && !locked(p));",
            "const toStart = L.start.filter((p) => sid(p) != null && !act(p) && !locked(p));",
            "sid(p) != null && !act(p)")
    return t


_fix_before_r24 = fix


def fix(t):
    return round24(_fix_before_r24(t))

# ---------- round 25: pickups start after the daily lock + waivers (news_logos.py) ----------
# ESPN locks the whole day at the first puck drop: anyone added after that plays from tomorrow,
# even if his team plays later. Players on waivers (1-day waivers) play from tomorrow at the earliest.

# --- espn_sync.py: mark players on waivers ---
SYNC25_WV_OLD = '"chg": round((p.get("ownership") or {}).get("percentChange") or 0, 1)})'
SYNC25_WV_NEW = '"chg": round((p.get("ownership") or {}).get("percentChange") or 0, 1), "wv": 1 if e.get("status") == "WAIVERS" else 0})'
SYNC25_LOG_OLD = "\nslots = {}\ntry:\n"
SYNC25_LOG_NEW = "\nprint(f\"(check) players on waivers: {sum(1 for x_ in players if x_.get('wv'))}\")\nslots = {}\ntry:\n"

_fix_sync_before_r25 = PY_FIXES[SYNC]


def fix_sync25(t):
    t = _fix_sync_before_r25(t)
    t = lit(t, "sync: mark players on waivers", SYNC25_WV_OLD, SYNC25_WV_NEW, '"wv": 1 if e.get("status")')
    t = lit(t, "sync: count players on waivers", SYNC25_LOG_OLD, SYNC25_LOG_NEW, "players on waivers")
    py_ok(SYNC, t)
    return t


PY_FIXES[SYNC] = fix_sync25

# --- fantasy-gm.html ---
R25_HELPERS = r'''// ---------- round 25: pickups start after the daily lock (news_logos.py) ----------
// ESPN locks the whole day at the first puck drop, so anyone added after that plays from tomorrow.
// Players on waivers (1-day waivers) can play from tomorrow at the earliest.
let __LK = null;
const lockedToday = () => {
  const today = todayISO(), k = today + ":" + Math.floor(Date.now() / 30000);
  if (__LK && __LK.k === k) return __LK.v;
  const G = ((window.GAMES_DATA || {}).games || {})[today] || {};
  const first = Object.values(G).reduce((m, g) => { const t = g && g.st ? Date.parse(g.st) : NaN; return isNaN(t) ? m : Math.min(m, t); }, Infinity);
  const live = Object.values((window.__LIVESC || {})[today] || {}).some((x) => x && x.s && x.s !== "P");
  const espn = Object.values((((window.ESPN_DATA || {}).gstate || {})[today]) || {}).some((x) => x && x.s && x.s !== "P");
  const v = live || espn || first <= Date.now();
  __LK = { k, v };
  return v;
};
const pickStart = (p) => ((p && p.wv) || lockedToday() ? addDays(todayISO(), 1) : todayISO());
const onDay = (p, dt) => !dt || ((!p.fromD || dt >= p.fromD) && (!p.untilD || dt < p.untilD));
const timedMove = (roster, me, moves) => {
  let r = roster;
  moves.forEach(({ add, drop }) => { const a = pickStart(add); r = r.map((p) => (drop && p.id === drop.id ? { ...p, untilD: a } : p)).concat([{ ...add, ft: me, fromD: a }]); });
  return r;
};
const PickNote = () => { const a = pickStart(null); return a === todayISO() ? null : <div className="w-full text-xs text-amber-600 mt-1">Today's first game has started, so anyone you add now plays from {dayLabel(a)}. Players on waivers show a Waivers tag and can't play before tomorrow.</div>; };

'''


def round25(t):
    t = lit(t, "lock: helpers", ROOT, R25_HELPERS + ROOT, "const pickStart =")
    t = lit(t, "lock: lineups respect pickup and drop days",
            "const pl = roster.filter((p) => !p.ir && p.prob > 0 && avail(p, dt) > 0",
            "const pl = roster.filter((p) => !p.ir && p.prob > 0 && onDay(p, dt) && avail(p, dt) > 0",
            "p.prob > 0 && onDay(p, dt)")
    t = lit(t, "lock: games left for a pickup",
            "const gamesIn = (p) => { let g = 0; horizon.forEach((h) => (h.wk.games[p.t] || []).forEach((d) => { if (d >= h.from && !p.ir && avail(p, h.wk.dates ? h.wk.dates[d] : null)) g++; })); return g; };",
            "const gamesIn = (p) => { const a = pickStart(p); let g = 0; horizon.forEach((h) => (h.wk.games[p.t] || []).forEach((d) => { const dt = h.wk.dates ? h.wk.dates[d] : null; if (d >= h.from && (!dt || dt >= a) && !p.ir && avail(p, dt)) g++; })); return g; };",
            "const gamesIn = (p) => { const a = pickStart(p);")
    t = lit(t, "lock: points for a pickup",
            "const rawPts = (p) => { let t = 0; horizon.forEach((h) => (h.wk.games[p.t] || []).forEach((d) => { const dt = h.wk.dates ? h.wk.dates[d] : null; if (d >= h.from && !p.ir && avail(p, dt)) t += effAvg(wt(p), K, dt) * p.prob; })); return t; };",
            "const rawPts = (p, ref) => { const a = pickStart(ref || p); let t = 0; horizon.forEach((h) => (h.wk.games[p.t] || []).forEach((d) => { const dt = h.wk.dates ? h.wk.dates[d] : null; if (d >= h.from && (!dt || dt >= a) && !p.ir && avail(p, dt)) t += effAvg(wt(p), K, dt) * p.prob; })); return t; };",
            "const rawPts = (p, ref) =>")
    t = lit(t, "lock: move gain",
            "const gain = lineupAware ? total([...myR.filter((x) => x.id !== d.id), { ...f, ft: s.me }]) - base : raw - rawPts(d);",
            "const gain = lineupAware ? total(timedMove(myR, s.me, [{ add: f, drop: d }])) - base : raw - rawPts(d, f);",
            "total(timedMove(myR, s.me, [{ add: f, drop: d }]))")
    t = lit(t, "lock: add/drop with your chosen drop",
            "gain: lineupAware ? total(myR.filter((x) => x.id !== forced.id).concat([{ ...r.f, ft: s.me }])) - base : rawPts(r.f) - rawPts(forced) }",
            "gain: lineupAware ? total(timedMove(myR, s.me, [{ add: r.f, drop: forced }])) - base : rawPts(r.f) - rawPts(forced, r.f) }",
            "[{ add: r.f, drop: forced }]")
    t = lit(t, "lock: simulator suggested drop",
            "const g = lineupAware ? total(r.filter((x) => x.id !== d.id).concat([{ ...f, ft: s.me }])) - b : rawPts(f) - rawPts(d);",
            "const g = lineupAware ? total(timedMove(r, s.me, [{ add: f, drop: d }])) - b : rawPts(f) - rawPts(d, f);",
            "total(timedMove(r, s.me")
    t = lit(t, "lock: simulator points",
            "const gain = lineupAware ? total(after) - total(myR) : ok.reduce((t, x) => t + rawPts(x.a) - rawPts(x.d), 0);",
            "const timed = timedMove(myR, s.me, ok.map((x) => ({ add: x.a, drop: x.d })));\n    const gain = lineupAware ? total(timed) - total(myR) : ok.reduce((t, x) => t + rawPts(x.a) - rawPts(x.d, x.a), 0);",
            "const timed = timedMove(myR")
    t = lit(t, "lock: simulator win chance", "win: winChance(s, after)", "win: winChance(s, timed)", "winChance(s, timed)")
    t = lit(t, "lock: win change per move",
            "const afterMove = (s, add, drop) => s.players.filter((p) => p.ft === s.me && p.id !== drop.id).concat([{ ...add, ft: s.me }]);",
            "const afterMove = (s, add, drop) => timedMove(s.players.filter((p) => p.ft === s.me), s.me, [{ add, drop }]);",
            "timedMove(s.players.filter((p) => p.ft === s.me), s.me")
    t = lit(t, "lock: bench fixer",
            "const r2 = [...mine.filter((x) => x.id !== d.id), { ...f, ft: s.me }];",
            "const r2 = timedMove(mine, s.me, [{ add: f, drop: d }]);",
            "timedMove(mine, s.me")
    t = lit(t, "lock: planner starts tomorrow by itself",
            "const [fromTomorrow, setFT] = useState(false);",
            "const [fromTomorrow, setFT] = useState(() => lockedToday());",
            "useState(() => lockedToday())")
    t = lit(t, "lock: planner label",
            "Start from tomorrow (today's games already started)",
            "Start from tomorrow (today's first game has started, so adds play tomorrow)",
            "so adds play tomorrow")
    t = lit(t, "lock: planner skips days a pickup can't play",
            "if (usedFA.has(f.id) || !(wk.games[f.t] || []).includes(d)) continue;",
            "if (usedFA.has(f.id) || !(wk.games[f.t] || []).includes(d) || wk.dates[d] < pickStart(f)) continue;",
            "wk.dates[d] < pickStart(f)")
    t = lit(t, "lock: fill an empty spot",
            'fits(p) && gState(p.t, dt).s === "P")',
            'fits(p) && gState(p.t, dt).s === "P" && dt >= pickStart(p))',
            'fits(p) && gState(p.t, dt).s === "P" && dt >= pickStart')
    t = lit(t, "lock: goalie streams",
            'avail(p, dt) > 0 && gState(p.t, dt).s === "P")',
            'avail(p, dt) > 0 && gState(p.t, dt).s === "P" && dt >= pickStart(p))',
            'avail(p, dt) > 0 && gState(p.t, dt).s === "P" && dt >= pickStart')
    t = lit(t, "lock: note on Advice",
            'sub="Most extra points in your daily lineups for the rest of this week.">',
            'sub="Most extra points in your daily lineups for the rest of this week."><PickNote where="adv" />',
            'PickNote where="adv"')
    t = lit(t, "lock: note on Add / Drop",
            "onClick={() => setSim({})}>Build a move</button>",
            'onClick={() => setSim({})}>Build a move</button><PickNote where="ad" />',
            'PickNote where="ad"')
    t = lit(t, "lock: note on Today",
            "{moves.length ? moves.map((r) => { const sd = effAvg(r.f, K)",
            '<PickNote where="today" />{moves.length ? moves.map((r) => { const sd = effAvg(r.f, K)',
            'PickNote where="today"')
    t = lit(t, "waivers: keep the flag from ESPN",
            "own: p.own || 0, chg: p.chg || 0 };",
            "own: p.own || 0, chg: p.chg || 0, wv: !!p.wv };",
            "wv: !!p.wv")
    t = lit(t, "waivers: tag in Add / Drop",
            '<PN p={r.f} /><span className="text-xs text-slate-500">{r.f.p}</span>{st ?',
            '<PN p={r.f} /><span className="text-xs text-slate-500">{r.f.p}</span>{r.f.wv ? <span className="text-xs text-amber-600">Waivers</span> : null}{st ?',
            '{r.f.wv ? <span className="text-xs text-amber-600">Waivers</span>')
    t = lit(t, "waivers: tag in Advice",
            '<PN p={r.f} className="truncate font-medium" /><span className="text-xs text-slate-500">{r.f.p}</span>',
            '<PN p={r.f} className="truncate font-medium" /><span className="text-xs text-slate-500">{r.f.p}</span>{r.f.wv ? <span className="text-xs text-amber-600 whitespace-nowrap">Waivers</span> : null}',
            'text-amber-600 whitespace-nowrap">Waivers')
    for must in ("const pickStart =", "function computeMoves(", "function MoveSim(", "function AddDrop(", "function buildPlan("):
        if must not in t:
            fail("fantasy-gm.html looks damaged after round 25 (" + must + ").")
    return t


_fix_before_r25 = fix


def fix(t):
    return round25(_fix_before_r25(t))

# ---------- round 26: planner never drops the same player twice + win chance per step (news_logos.py) ----------
R26_HELPERS = r'''// ---------- round 26: planner win chance (news_logos.py) ----------
const planRoster = (s, wk, steps) => {
  let r = s.players.filter((p) => p.ft === s.me);
  steps.forEach((st) => { const a = wk.dates[st.day]; r = r.map((p) => (p.id === st.drop.id ? { ...p, untilD: a } : p)).concat([{ ...st.add, ft: s.me, fromD: a }]); });
  return r;
};
const PlanWin = ({ a, b }) => {
  if (a == null || b == null) return null;
  const d = Math.round(b * 100) - Math.round(a * 100);
  return <span className={"text-sm whitespace-nowrap " + (d > 0 ? "text-green-700" : d < 0 ? "text-red-600" : "text-slate-500")} title="Your chance to win this week before and after this move">win {wpTxt(a)} → {wpTxt(b)} <span className="font-semibold">{d > 0 ? "+" : ""}{d}%</span></span>;
};

'''


def round26(t):
    t = lit(t, "planner: never drop the same player twice",
            "const drops = active.filter((x) => !x.p.ir && x.from < d + (x.orig ? 1 : 0)",
            "const drops = active.filter((x) => !x.p.ir && x.to === nD - 1 && x.from < d + (x.orig ? 1 : 0)",
            "x.to === nD - 1 &&")
    t = lit(t, "planner: win chance helpers", ROOT, R26_HELPERS + ROOT, "const planRoster =")
    t = lit(t, "planner: work out win chance after each step",
            "const run = () => { setBusy(true); setTimeout(() => { setPlan(buildPlan(s, wk, d0, left)); setBusy(false); }, 30); };",
            "const run = () => { setBusy(true); setTimeout(() => { setPlan(buildPlan(s, wk, d0, left)); setBusy(false); }, 30); };\n"
            "  const wins = useMemo(() => (plan ? { b: winChance(s), after: plan.steps.map((_, i) => winChance(s, planRoster(s, wk, plan.steps.slice(0, i + 1)))) } : null), [plan]);",
            "const wins = useMemo(")
    t = lit(t, "planner: win chance on each step",
            '<span className="text-green-700 font-semibold ml-auto">+{f1(st.gain)}</span>',
            '<span className="ml-auto flex items-baseline gap-3">{wins ? <PlanWin a={i ? wins.after[i - 1] : wins.b} b={wins.after[i]} /> : null}<span className="text-green-700 font-semibold">+{f1(st.gain)}</span></span>',
            "<PlanWin")
    t = lit(t, "planner: win chance for the whole plan",
            "${f1(aA + plan.final - aB - oppProj)}`}>",
            "${f1(aA + plan.final - aB - oppProj)}${wins && wins.after.length ? ` · win chance ${wpTxt(wins.b)} → ${wpTxt(wins.after[wins.after.length - 1])}` : \"\"}`}>",
            "win chance ${wpTxt(wins.b)}")
    for must in ("function buildPlan(", "function AcqPlanner(", "const planRoster ="):
        if must not in t:
            fail("fantasy-gm.html looks damaged after round 26 (" + must + ").")
    return t


_fix_before_r26 = fix


def fix(t):
    return round26(_fix_before_r26(t))

# ---------- round 27: no moves left this week -> no pickup or drop suggestions, plan next week instead ----------
R27_HELPERS = r'''// ---------- round 27: no moves left this week, so plan next week instead (news_logos.py) ----------
const noMovesWk = (s, w) => !!w && movesLeft(s, s.me, w) === 0;
const outOfMoves = (s) => noMovesWk(s, s.weeks[s.wk]);
const nextWkS = (s) => (s.wk + 1 < s.weeks.length ? { ...s, wk: s.wk + 1 } : null);
const planS = (s) => (outOfMoves(s) && nextWkS(s)) || s;
const planBase = (s, sP) => (sP !== s && !oppOf(sP.weeks[sP.wk] || {}, sP.me) ? null : winChance(sP));
const planNote = (sP) => { const w = sP.weeks[sP.wk] || {}, d = (w.dates || [])[0]; return "No moves left this week. These are for " + (w.label || "next week") + (d ? ", once your moves reset on " + dayLabel(d) : "") + "."; };
const PlanNote = ({ sP }) => <div className="w-full text-xs text-amber-600 mt-1 mb-1">{planNote(sP)}</div>;

'''

R27_TODAY_OLD = r'''const moves = useMemo(() => computeMoves(s, { H: 1, pool: 40 }).res.filter((r) => r.gain >= (s.minGain ?? 3)).slice(0, 3), [s]);'''
R27_TODAY_NEW = r'''const sP = useMemo(() => planS(s), [s]); // round 27, older marker kept: <WinDelta s={s} add={r.f} drop={r.d} /><span
  const pBase = useMemo(() => (sP !== s ? planBase(s, sP) : undefined), [sP]);
  const moves = useMemo(() => computeMoves(sP, { H: 1, pool: 40 }).res.filter((r) => r.gain >= (s.minGain ?? 3)).slice(0, 3), [sP]);'''

R27_ADV_OLD = r'''<Section title="Best moves this week" sub="Most extra points in your daily lineups for the rest of this week."><PickNote where="adv" />'''
R27_ADV_NEW = r'''<Section title={sP !== s ? "Plan for next week" : "Best moves this week"} sub={sP !== s ? "Most extra points in next week's daily lineups." : "Most extra points in your daily lineups for the rest of this week."}>{sP !== s ? <PlanNote sP={sP} /> : <PickNote where="adv" />}'''

R27_LONG_OLD = r'''<Section title="Long-term upgrades" sub="Better per game, and more points over the next 4 weeks.">'''
R27_LONG_NEW = r'''<Section title="Long-term upgrades" sub={sP !== s ? "Better per game, and more points over the 4 weeks starting next week. Win shows next week's matchup." : "Better per game, and more points over the next 4 weeks."}>'''

R27_PLANNER_NEW = r'''function AcqPlanner({ s: s0, setS, wk: wk0 }) {
  // round 27: with no moves left this week, the planner plans next week
  // older marker kept: {espnUsed != null ? <span>Moves used this week
  const s = planS(s0), wk = s === s0 ? wk0 : deriveWeek(s.weeks[s.wk], s.autoDone), tw = s === s0 ? "this week" : "next week";'''

R27_USED_OLD = r'''{espnUsed != null ? <span>Moves used this week: <b>{used} of 3</b>'''
R27_USED_NEW = r'''{s !== s0 ? <div className="w-full text-sm text-amber-600">No moves left this week, so this plans next week: {wk.label}.</div> : null}{espnUsed != null ? <span>Moves used {tw}: <b>{used} of 3</b>'''

R27_TITLE_OLD = r'''`Your plan: +${f1(plan.gain)} points this week` : "No move is worth it this week"}'''
R27_TITLE_NEW = r'''`Your plan: +${f1(plan.gain)} points ${tw}` : "No move is worth it " + tw}'''

R27_GNOTE_OLD = r'''{st ? <div className="text-sm mb-2"><span className="font-semibold">{st[0]}</span>'''
R27_GNOTE_NEW = r'''{noMovesWk(s, wk) ? <div className="text-sm text-amber-600 mb-2">No moves left this week, so no free-agent streams are shown. Next week's best pickups, goalies included, are on Advice, and the Planner builds the full plan.</div> : st ? <div className="text-sm mb-2"><span className="font-semibold">{st[0]}</span>'''

R27_GEMPTY_OLD = r'''<div className="text-sm text-slate-400 py-2 border-t border-slate-100">No free-agent starters play.</div>'''
R27_GEMPTY_NEW = r'''(noMovesWk(s, wk) ? null : <div className="text-sm text-slate-400 py-2 border-t border-slate-100">No free-agent starters play.</div>)'''

R27_AD_NEW = r'''{outOfMoves(s) ? <div className="w-full text-xs text-amber-600 mt-1">No moves left this week, so this list is only a what-if until your moves reset. Next week's plan is on Advice and in the Planner.</div> : <PickNote where="ad" />}'''


def round27(t):
    t = lit(t, "no moves: helpers", ROOT, R27_HELPERS + ROOT, "const outOfMoves =")
    # Today
    t = lit(t, "no moves: Today uses next week", R27_TODAY_OLD, R27_TODAY_NEW, "computeMoves(sP, { H: 1, pool: 40 })")
    t = lit(t, "no moves: Today card title", '<Section title="Best moves this week" sub={sameDrop ?',
            '<Section title={sP !== s ? "Best moves for next week" : "Best moves this week"} sub={sameDrop ?',
            '"Best moves for next week" : "Best moves this week"} sub={sameDrop ?')
    t = lit(t, "no moves: Today note", '<PickNote where="today" />',
            '{sP !== s ? <PlanNote sP={sP} /> : <PickNote where="today" />}',
            '<PlanNote sP={sP} /> : <PickNote where="today" />')
    t = lit(t, "no moves: Today win chance",
            '<WinDelta s={s} add={r.f} drop={r.d} /><span className="text-green-700 font-semibold">+{f1(r.gain)}</span></Row>',
            '<WinDelta s={sP} add={r.f} drop={r.d} base={pBase} /><span className="text-green-700 font-semibold">+{f1(r.gain)}</span></Row>',
            "<WinDelta s={sP} add={r.f} drop={r.d} base={pBase} />")
    # Advice
    t = lit(t, "no moves: Advice uses next week", "const now = useMemo(() => computeMoves(s, { H: 1, pool: 60 }), [s]);",
            "const sP = useMemo(() => planS(s), [s]);\n  const now = useMemo(() => computeMoves(sP, { H: 1, pool: 60 }), [sP]);",
            "computeMoves(sP, { H: 1, pool: 60 })")
    t = sub_once(t, "no moves: Advice long-term list and win chance",
                 re.escape("const later = useMemo(() => computeMoves(s, { H: 4, pool: 40 }), [s]);") + r"\s*"
                 + re.escape("const base = useMemo(() => winChance(s), [s]);"),
                 "const later = useMemo(() => computeMoves(sP, { H: 4, pool: 40 }), [sP]);\n  const base = useMemo(() => planBase(s, sP), [sP]);",
                 "computeMoves(sP, { H: 4, pool: 40 })")
    t = lit(t, "no moves: Advice rows", "<AdvMove key={r.f.id} s={s} r={r} K={K} showDrop={!d1} base={base} />",
            "<AdvMove key={r.f.id} s={sP} r={r} K={K} showDrop={!d1} base={base} />", "<AdvMove key={r.f.id} s={sP}")
    t = lit(t, "no moves: Advice plan for next week", R27_ADV_OLD, R27_ADV_NEW, '<PlanNote sP={sP} /> : <PickNote where="adv" />')
    t = lit(t, "no moves: Advice empty text", "No move adds ${minGain}+ points this week. Save your moves.",
            'No move adds ${minGain}+ points ${sP !== s ? "next week" : "this week"}. Save your moves.',
            'points ${sP !== s ? "next week" : "this week"}. Save your moves.')
    t = lit(t, "no moves: Advice long-term text", R27_LONG_OLD, R27_LONG_NEW, "over the 4 weeks starting next week")
    # Matchup: fill an empty spot
    t = lit(t, "no moves: hide fill an empty spot", "if (!dt || dt < todayISO() || l.empty <= 0) return null;",
            "if (!dt || dt < todayISO() || l.empty <= 0 || noMovesWk(s, wk)) return null;", "l.empty <= 0 || noMovesWk(s, wk)")
    # Goalie streams
    t = lit(t, "no moves: goalie streams list", ".filter((x) => x.gs.v >= 0.4).sort((a, b) => b.v - a.v).slice(0, 3) }));",
            ".filter((x) => x.gs.v >= 0.4).sort((a, b) => b.v - a.v).slice(0, noMovesWk(s, wk) ? 0 : 3) }));",
            ".slice(0, noMovesWk(s, wk) ? 0 : 3)")
    t = lit(t, "no moves: goalie streams heading", '{head("Free agents to stream")}',
            '{noMovesWk(s, wk) ? null : head("Free agents to stream")}', 'noMovesWk(s, wk) ? null : head("Free agents to stream")')
    t = lit(t, "no moves: goalie streams empty text", R27_GEMPTY_OLD, R27_GEMPTY_NEW, "(noMovesWk(s, wk) ? null : <div")
    t = lit(t, "no moves: goalie streams note", R27_GNOTE_OLD, R27_GNOTE_NEW, "so no free-agent streams are shown")
    # Bench fixer
    t = lit(t, "no moves: bench fixer", "{w.fix ? (",
            '{i === 0 && w.fix && outOfMoves(s) ? <div className="text-xs text-slate-500 mt-1">No moves left this week, so no swap is suggested for it.</div> : w.fix ? (',
            "i === 0 && w.fix && outOfMoves(s)")
    # Planner
    t = lit(t, "no moves: planner plans next week", "function AcqPlanner({ s, setS, wk }) {", R27_PLANNER_NEW,
            "function AcqPlanner({ s: s0, setS, wk: wk0 })")
    t = lit(t, "no moves: planner start day", "+ (fromTomorrow ? 1 : 0));", "+ (fromTomorrow && ti >= 0 ? 1 : 0));", "fromTomorrow && ti >= 0")
    t = lit(t, "no moves: planner tomorrow box", '<label className="flex items-center gap-1"><input type="checkbox" checked={fromTomorrow}',
            '<label className="flex items-center gap-1" style={{ display: ti >= 0 ? "" : "none" }}><input type="checkbox" checked={fromTomorrow}',
            'style={{ display: ti >= 0 ? "" : "none" }}')
    t = lit(t, "no moves: planner banner", R27_USED_OLD, R27_USED_NEW, "<span>Moves used {tw}: <b>")
    t = lit(t, "no moves: planner title", R27_TITLE_OLD, R27_TITLE_NEW, "points ${tw}`")
    # Add / Drop
    t = lit(t, "no moves: add/drop note", '<PickNote where="ad" />', R27_AD_NEW, "this list is only a what-if")
    for must in ("const outOfMoves =", "function Today(", "function AdvicePanel(", "function AcqPlanner(", "function GoalieStreams(", "function FillSlot(",
                 "<WinDelta s={s} add={r.f} drop={r.d} /><span", "{espnUsed != null ? <span>Moves used this week", 'PickNote where="adv"', 'PickNote where="ad"', 'PickNote where="today"'):
        if must not in t:
            fail("fantasy-gm.html looks damaged after round 27 (" + must + ").")
    return t


_fix_before_r27 = fix


def fix(t):
    return round27(_fix_before_r27(t))

# ---------- round 28: clean-up. Boxes open and close, simpler Today and Matchup, player updates on My Team, goalies must be playing ----------
R28_CSS = r'''  /* round 28 clean-up (news_logos.py) */
  .sec-chev { width: 8px; height: 8px; border-right: 2px solid var(--mute); border-bottom: 2px solid var(--mute); transform: rotate(45deg); transition: transform .15s ease; flex-shrink: 0; display: inline-block; margin: 6px 6px 0 10px; }
  .sec-chev.shut { transform: rotate(-45deg); }
  .sec-head { flex: 1; min-width: 0; text-align: left; cursor: pointer; }
'''

R28_SECTION = r'''// round 28: every box opens and closes; the choice is remembered on this device (news_logos.py)
const UIKEY = "fantasy-islands-gm-ui";
let __UI = null;
const uiGet = () => { if (!__UI) { try { __UI = JSON.parse(localStorage.getItem(UIKEY) || "{}") || {}; } catch (e) { __UI = {}; } } return __UI; };
const uiSet = (k, v) => { const u = uiGet(); u[k] = v; try { localStorage.setItem(UIKEY, JSON.stringify(u)); } catch (e) {} };
const secKey = (t) => (typeof t === "string" ? t.toLowerCase().replace(/[^a-z ]/g, " ").replace(/\s+/g, " ").trim().slice(0, 40) : "box");
// boxes that start closed: "tab:start of the title"
const SEC_SHUT = ["today:your lineup", "today:injuries", "today:news on your players",
  "myteam:this week day by day", "myteam:player updates", "myteam:injuries", "myteam:protected players",
  "moves/advice:free agents to watch", "moves/advice:trade advice", "moves/advice:line promotions", "moves/advice:luck", "moves/advice:model vs espn",
  "moves/planner:week ", "moves/planner:chronic bench players", "moves/trades:trade ideas",
  "teams:news", "league/power:how to climb the rankings", "league/standings:all teams this week",
  "news:your opponent", "news:around your league", "news:free agents", "news:phone notifications", "setup/settings:team names"];
const Section = ({ title, sub, link, children, closed, id }) => {
  const [k] = useState(() => "sec:" + (window.__TAB || "") + ":" + (id || secKey(title)));
  const [open, setOpen] = useState(() => { const v = uiGet()[k]; return v == null ? !(closed || SEC_SHUT.some((x) => k.indexOf("sec:" + x) === 0)) : !!v; });
  const flip = () => { uiSet(k, !open); setOpen(!open); };
  const onKey = (e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); flip(); } };
  return (
    <div className={"bg-white rounded-xl border border-slate-200 p-4 text-sm" + (open ? "" : " self-start")}>
      <div className={"flex items-start gap-2" + (open ? " mb-2" : "")}>
        <div role="button" tabIndex={0} aria-expanded={open} className="sec-head" onClick={flip} onKeyDown={onKey}>
          <div className="font-semibold text-base">{title}</div>{open && sub ? <div className="text-xs text-slate-500">{sub}</div> : null}
        </div>
        {open && link ? <button className="text-xs text-blue-600 whitespace-nowrap" onClick={link[1]}>{link[0] + " \u2192"}</button> : null}
        <button type="button" onClick={flip} aria-label={open ? "Close this box" : "Open this box"} style={{ lineHeight: 0, padding: "2px 0" }}><span className={"sec-chev" + (open ? "" : " shut")}></span></button>
      </div>
      {open ? children : null}
    </div>
  );
};
const SectionShut = (p) => <Section {...p} closed />;
const DayFold = ({ id, open0, head, right, children }) => {
  const k = "day:" + id;
  const [open, setOpen] = useState(() => { const v = uiGet()[k]; return v == null ? !!open0 : !!v; });
  const flip = () => { uiSet(k, !open); setOpen(!open); };
  const onKey = (e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); flip(); } };
  return (
    <div className="bg-white rounded-xl border border-slate-200 mb-3">
      <div role="button" tabIndex={0} aria-expanded={open} onClick={flip} onKeyDown={onKey} className={"flex items-center gap-3 px-3 py-2 text-sm cursor-pointer" + (open ? " border-b border-slate-200" : "")}>
        <span className="font-semibold">{head}</span>
        <span className="ml-auto flex items-center gap-3">{right}</span>
        <span className={"sec-chev" + (open ? "" : " shut")} style={{ margin: "0 4px 2px 2px" }}></span>
      </div>
      {open ? children : null}
    </div>
  );
};

'''

R28_HELPERS = r'''// ---------- round 28: goalies must be playing, player updates for My Team (news_logos.py) ----------
// a goalie is "not playing" if he started fewer than 2 of his team's last 5 games, or is out right now
const goalieOut = (p) => {
  if (!p || p.p !== "G") return false;
  const today = todayISO();
  if (avail(p, today) === 0) return true;
  const g = sigOf(p).gs;
  if (g && g.rg >= 3) return g.rs * 5 < g.rg * 2;
  const played = [...(SCHED[p.t] || [])].filter((d) => d < today).length;
  return played >= 4 && !(p.gp > 0);
};
function MyForm({ s }) {
  const K = s.blend;
  const rows = s.players.filter((p) => p.ft === s.me && !p.ir).map((p) => {
    const fr = formRatio(p, K), t = toiOf(p), rec = sigOf(p).rec;
    if (fr !== null && fr >= 1.3) return { p, n: "Hot: " + f1(rec.ppg) + "/g lately. Start him every game.", c: "text-orange-600" };
    if (fr !== null && fr <= 0.7) return { p, n: "Cold: " + f1(rec.ppg) + "/g lately. Check his role before dropping.", c: "text-sky-600" };
    if (t && (t.d <= -90 || t.pd <= -45)) return { p, n: "Losing minutes (" + (t.d <= -90 ? mm(t.d) + " a game" : "power play " + mm(t.pd)) + "). Watch closely.", c: "text-red-600" };
    if (t && (t.d >= 90 || t.pd >= 45)) return { p, n: "Bigger role (" + (t.d >= 90 ? mm(t.d) + " a game" : "power play " + mm(t.pd)) + ").", c: "text-green-700" };
    return null;
  }).filter(Boolean);
  return (
    <Section title={"Player updates" + (rows.length ? " (" + rows.length + ")" : "")} sub="Hot and cold streaks and ice-time changes, compared with each player's projection.">
      {rows.length ? rows.map(({ p, n, c }) => <PlayerLine key={p.id} s={s} p={p} extra={<span className={c}>{"\u00b7 " + n}</span>} />) : <div className="text-slate-400">Everyone is playing close to projection.</div>}
    </Section>
  );
}

'''

R28_DAY_PAT = r"\s*".join(re.escape(x) for x in (
    '<div key={d} className="bg-white rounded-xl border border-slate-200 mb-3">',
    '<div className="flex justify-between items-center px-3 py-2 border-b border-slate-200 text-sm">',
    '<span className="font-semibold">{dl}</span>',
    '{/* day header: running total removed */}',
    '{tag ? <LiveTag st={tag === "LIVE" ? "L" : "F"} /> : null}',
    '</div>',
))
R28_DAY_NEW = r'''<DayFold key={(wk.dates || [])[d] || d} id={(wk.dates || [])[d] || "d" + d} open0={d === openDay} head={dl} right={<>{/* day header: running total removed */}{tag ? <LiveTag st={tag === "LIVE" ? "L" : "F"} /> : null}<span className="text-slate-500">{f1(x.act + x.total) + " \u2013 " + f1(y.act + y.total)}</span><span className={"min-w-[56px] text-center px-2 py-0.5 rounded-md font-semibold " + (dv >= 0 ? "bg-green-100 text-green-700" : "bg-red-100 text-red-600")}>{dv >= 0 ? "+" : ""}{f1(dv)}</span></>}>'''
R28_TAIL_OLD = '<div className="text-xs text-slate-500">Games that have started'
R28_TAIL_PAT = re.escape("</div>") + r"\s*" + re.escape(");") + r"\s*" + re.escape("})}") + r"\s*" + re.escape(R28_TAIL_OLD)
R28_TAIL_NEW = "</DayFold>\n        );\n      })}\n      " + R28_TAIL_OLD

R28_EMPTY_OLD = r'''{l.empty > 0 && <div className="text-xs text-slate-500 mt-1">Empty slots: {l.empty}</div>}'''
R28_EMPTY_NEW = r'''{l.empty > 0 && !(wk && id === s.me && noMovesWk(s, wk)) && <div className="text-xs text-slate-500 mt-1">Empty slots: {l.empty}</div>}'''


def round28(t):
    t = lit(t, "clean-up: styles", "</style>", R28_CSS + "</style>", "round 28 clean-up")
    t = block(t, "clean-up: boxes open and close", "const Section = ({ title, sub, link, children }) => (",
              "// ---------- App ----------", R28_SECTION, "const SEC_SHUT =")
    t = lit(t, "clean-up: helpers", ROOT, R28_HELPERS + ROOT, "const goalieOut =")
    t = lit(t, "clean-up: boxes know their tab", "window.__NAV = { team: openTeam, player: (p) => { if (p) setPlayer(p); } };",
            'window.__NAV = { team: openTeam, player: (p) => { if (p) setPlayer(p); } }; window.__TAB = tab + (subs[tab] ? "/" + subs[tab] : "");',
            "window.__TAB = tab")
    # Today
    t = lit(t, "clean-up: Today score line (you)", '<div className="text-xs text-slate-500">+ {f1(A.total)} still projected',
            '<div className="hidden">+ {f1(A.total)} still projected', '<div className="hidden">+ {f1(A.total)} still projected')
    t = lit(t, "clean-up: Today score line (them)", '<div className="text-xs text-slate-500">+ {f1(B.total)} still projected',
            '<div className="hidden">+ {f1(B.total)} still projected', '<div className="hidden">+ {f1(B.total)} still projected')
    t = lit(t, "clean-up: Today advice sentence", "{done < dates.length ? <StrategyLine p={winProb(A, B, aA, aB)} /> : null}",
            "{/* round 28: advice sentence removed (older marker kept: <StrategyLine) */}", "round 28: advice sentence removed")
    t = lit(t, "clean-up: Today empty slots line", "if (L.empty > 0) checks.push(", "if (L.empty > 0 && !outOfMoves(s)) checks.push(",
            "L.empty > 0 && !outOfMoves(s)")
    t = lit(t, "clean-up: Today injuries count", '<Section title="Injuries" link={["My Team", () => go("myteam")]}>',
            '<Section title={"Injuries" + (outNow.length ? " (" + outNow.length + ")" : "")} link={["My Team", () => go("myteam")]}>',
            '"Injuries" + (outNow.length')
    t = lit(t, "clean-up: Today news count", '<Section title="News on your players" link={["All news", () => go("news")]}>',
            '<Section title={"News on your players" + (news.length ? " (" + news.length + ")" : "")} link={["All news", () => go("news")]}>',
            '"News on your players" + (news.length')
    t = lit(t, "clean-up: Today line changes start closed", "H={{ Section, teamName, f1, TL }}",
            "H={{ Section: SectionShut, teamName, f1, TL }}", "Section: SectionShut")
    # Matchup
    t = lit(t, "clean-up: Matchup actual row", "<LiveBar s={s} wk={wk} setWk={setWk} ids={[a, b]} />",
            "{/* round 28: actual-score row removed */}", "round 28: actual-score row removed")
    t = lit(t, "clean-up: Matchup day to open", "let run = (aA - aB) - (A.act - B.act);",
            "let run = (aA - aB) - (A.act - B.act);\n  const openDay = (wk.dates || []).findIndex((x) => x >= todayISO());", "const openDay =")
    t = sub_once(t, "clean-up: Matchup day bars (top)", R28_DAY_PAT, R28_DAY_NEW, "<DayFold key=")
    t = sub_once(t, "clean-up: Matchup day bars (bottom)", R28_TAIL_PAT, R28_TAIL_NEW, "</DayFold>")
    t = lit(t, "clean-up: Matchup empty slots count", R28_EMPTY_OLD, R28_EMPTY_NEW, "l.empty > 0 && !(wk && id === s.me && noMovesWk(s, wk))")
    t = lit(t, "clean-up: phone Matchup empty slots count", '{x.empty || y.empty ? <div className="text-xs text-slate-500 px-3 pt-2">Empty slots:',
            '{(x.empty || y.empty) && !(a === s.me && noMovesWk(s, wk)) ? <div className="text-xs text-slate-500 px-3 pt-2">Empty slots:',
            "(x.empty || y.empty) && !(a === s.me")
    # Advice and My Team
    t = sub_once(t, "clean-up: player updates leave Advice",
                 re.escape('<Section title="Your players" sub="Recent form and ice time compared with their projection.">') + r".*?" + re.escape("</Section>"),
                 "{/* round 28: player updates moved to My Team */}", "round 28: player updates moved to My Team", re.S)
    t = lit(t, "clean-up: player updates on My Team", "<MyInjProt s={s} setS={setS} wk={wk} />",
            "<MyForm s={s} />\n      <MyInjProt s={s} setS={setS} wk={wk} />", "<MyForm s={s} />")
    # goalies must be playing
    t = lit(t, "clean-up: goalies in pickup lists", ".filter((f) => f.prob > 0 && (f.proj !== false || f.gp > 0) && inTab(f) && f.n.toLowerCase().includes(q))",
            ".filter((f) => f.prob > 0 && (f.proj !== false || f.gp > 0) && inTab(f) && f.n.toLowerCase().includes(q) && (!!q || !goalieOut(f)))",
            "(!!q || !goalieOut(f))")
    t = lit(t, "clean-up: goalies in Model vs ESPN", "const under = (p) => { const x = mv(p); return x && x.d >= 1 && x.r >= 1.15; };",
            "const under = (p) => { const x = mv(p); return x && x.d >= 1 && x.r >= 1.15 && !goalieOut(p); };", "x.r >= 1.15 && !goalieOut(p)")
    t = lit(t, "clean-up: goalies in free agents to watch", 'const watch = s.players.filter((p) => p.ft === "fa" && p.prob > 0 && why(p))',
            'const watch = s.players.filter((p) => p.ft === "fa" && p.prob > 0 && why(p) && !goalieOut(p))', "why(p) && !goalieOut(p)")
    t = lit(t, "clean-up: goalies in trade pickups",
            's.players.filter((p) => p.ft === "fa" && p.prob > 0 && tv[p.id] > 0).sort((a, b) => tv[b.id] - tv[a.id]).slice(0, 60)',
            's.players.filter((p) => p.ft === "fa" && p.prob > 0 && tv[p.id] > 0 && !goalieOut(p)).sort((a, b) => tv[b.id] - tv[a.id]).slice(0, 60)',
            "tv[p.id] > 0 && !goalieOut(p)")
    t = lit(t, "clean-up: goalies in the planner", 'const fas = s.players.filter((p) => p.ft === "fa" && p.prob > 0 && (p.proj !== false || p.gp > 0))',
            'const fas = s.players.filter((p) => p.ft === "fa" && p.prob > 0 && (p.proj !== false || p.gp > 0) && !goalieOut(p))',
            "(p.proj !== false || p.gp > 0) && !goalieOut(p))")
    for must in ("const SEC_SHUT =", "const Section = (", "function MyForm(", "const goalieOut =", "<DayFold key=", "</DayFold>", "function Matchup(", "function Today(",
                 "<StrategyLine", "day header: running total removed", '<LiveTag st={tag === "LIVE" ? "L" : "F"} />', "<MyInjProt s={s}", "<FillSlot", "Projected today"):
        if must not in t:
            fail("fantasy-gm.html looks damaged after round 28 (" + must + ").")
    return t


_fix_before_r28 = fix


def fix(t):
    return round28(_fix_before_r28(t))

# ---------- round 29: trades. Trade advice with a league-wide buy-low list, no 2-for-1 box, searchable pickup, two result tiles ----------
R29_HELPERS = r'''// ---------- round 29: trade advice with buy-low list, free-agent search (news_logos.py) ----------
function TradeAdvice({ s, onPick }) {
  const K = s.blend;
  const [team, setTeam] = useState("all");
  const [more, setMore] = useState(false);
  const T = leagueTable(s), g = T.grpRank[s.me] || {};
  const posName = { F: "forwards", D: "defence", G: "goalies" }, need = { F: 10, D: 5, G: 2 };
  const by = ["F", "D", "G"].sort((a, b) => (g[b] || 0) - (g[a] || 0)), weak = by[0], strong = by[2];
  const pg = (p) => effAvg(p, K) * (p.p === "G" ? p.prob : 1);
  const mine = s.players.filter((p) => p.ft === s.me && !p.ir);
  const spare = mine.filter((p) => p.p === strong).sort((a, b) => pg(b) - pg(a)).slice(need[strong]);
  const sell = mine.filter((p) => tbFlags(p, K).some((f) => f.sell)).sort((a, b) => pg(b) - pg(a)).slice(0, 6);
  const all = useMemo(() => {
    const why = (p) => {
      const r = [], fr = formRatio(p, K), sg = sigOf(p), rec = sg.rec, l = sg.luck;
      const id = typeof p.id === "string" && p.id[0] === "e" ? p.id.slice(1) : null;
      const mb = window.__MODEL && id ? (window.__MODEL.base || {})[id] : null;
      if (fr !== null && fr <= 0.75 && rec) r.push("cold: " + f1(rec.ppg) + "/g last 14 days");
      if (mb != null && p.proj && p.avg > 0 && mb / p.avg >= 1.15 && mb - p.avg >= 1) r.push("model " + f1(mb) + " vs ESPN " + f1(p.avg));
      if (l && ((l.t === "s" && l.d <= -2) || (l.t === "g" && l.d <= -4))) r.push("unlucky");
      return r;
    };
    return s.players.filter((p) => p.ft !== s.me && p.ft !== "fa" && !p.ir && pg(p) >= 6 && !goalieOut(p))
      .map((p) => ({ p, r: why(p) })).filter((x) => x.r.length).sort((a, b) => pg(b.p) - pg(a.p));
  }, [s.players, K, window.__PMODE]);
  const list = all.filter((x) => team === "all" || x.p.ft === team);
  const shown = list.slice(0, more ? 20 : 8);
  return (
    <Section title="Trade advice" sub={"Your ranks: forwards #" + (g.F || "-") + ", defence #" + (g.D || "-") + ", goalies #" + (g.G || "-") + " of " + T.rows.length + "."}>
      <div>{weak !== strong && g[weak] > g[strong] ? <>Trade from your <b>{posName[strong]}</b> to improve your <b>{posName[weak]}</b>.{spare.length ? <span className="text-slate-500"> Spare: {spare.map((p) => p.n).join(", ")}.</span> : null}</> : "Your roster is balanced. Trade only for clear upgrades."}</div>
      {sell.length ? <div className="mt-1 text-slate-500">Sell high: {sell.map((p) => p.n).join(", ")}.</div> : null}
      <div className="flex flex-wrap items-center gap-2 mt-4 mb-1">
        <div className="text-xs uppercase tracking-wide text-slate-500">Buy low ({list.length}): good players who are cold, unlucky or underrated</div>
        <select className={inp + " ml-auto"} value={team} onChange={(e) => { setTeam(e.target.value); setMore(false); }}>
          <option value="all">All teams</option>
          {s.teams.filter((t) => t.id !== s.me).map((t) => <option key={t.id} value={t.id}>{t.name}</option>)}
        </select>
      </div>
      {shown.length ? shown.map(({ p, r }) => (
        <PlayerLine key={p.id} s={s} p={p} extra={<><span className="text-sky-600">{"\u00b7 " + r.join(", ")}</span><button type="button" className="text-blue-600" onClick={() => onPick(p)}>Add to trade</button></>} />
      )) : <div className="text-slate-400">No buy-low players here right now. Cold streaks need 3 or more recent games to show.</div>}
      {list.length > shown.length && !more ? <button className="text-sm text-blue-600 mt-2" onClick={() => setMore(true)}>Show all {Math.min(20, list.length)}</button> : null}
    </Section>
  );
}
function FaSearch({ s, top, taken, val, onPick }) {
  const [q, setQ] = useState("");
  const [open, setOpen] = useState(false);
  const qq = nrm(q);
  const list = !open ? [] : qq
    ? s.players.filter((p) => p.ft === "fa" && p.prob > 0 && !taken.has(p.id) && nrm(p.n).includes(qq)).sort((a, b) => val(b) - val(a)).slice(0, 8)
    : top.filter((p) => !taken.has(p.id)).slice(0, 6);
  return (
    <div className="relative mt-2">
      <input className={inp + " w-full"} placeholder="Search any free agent by name" value={q}
        onChange={(e) => { setQ(e.target.value); setOpen(true); }} onFocus={() => setOpen(true)} onBlur={() => setTimeout(() => setOpen(false), 150)} />
      {open ? (
        <div className="ms-list">
          {!qq ? <div className="text-xs text-slate-500 px-2 pt-1 pb-1">Best available</div> : null}
          {list.map((p) => (
            <button key={p.id} type="button" className="ms-opt" onMouseDown={(e) => e.preventDefault()} onClick={() => { onPick(p.id); setQ(""); setOpen(false); }}>
              <TeamLogo t={p.t} size={22} />
              <span className="truncate flex-1 text-left">{p.n} <span className="text-xs text-slate-500">{p.p}</span></span>
              <span className="text-xs text-slate-500 whitespace-nowrap">{f1(val(p))}/g</span>
            </button>
          ))}
          {list.length === 0 ? <div className="text-sm text-slate-400 px-2 py-2">No free agent matches.</div> : null}
        </div>
      ) : null}
    </div>
  );
}

'''

R29_ADVICE_NEW = r'''<TradeAdvice s={s} onPick={(p) => { setPartner(p.ft); setGet(p.ft === partner ? [...get.filter((x) => x !== p.id), p.id] : [p.id]); setPick({}); window.scrollTo(0, 0); }} />'''
R29_SEARCH_NEW = r'''<FaSearch s={s} top={fas} taken={new Set(picks.filter(Boolean).map((x) => x.id))} val={pg} onPick={(id) => setPick((x) => ({ ...x, [k]: id }))} />'''


def round29(t):
    t = lit(t, "trades: helpers", ROOT, R29_HELPERS + ROOT, "function TradeAdvice(")
    t = sub_once(t, "trades: trade advice leaves Advice",
                 re.escape('<Section title="Trade advice" sub={`') + r".*?" + re.escape("</Section>"),
                 "{/* round 29: trade advice moved to Trades */}", "round 29: trade advice moved to Trades", re.S)
    t = sub_once(t, "trades: buy-low list replaces trade ideas",
                 re.escape('<Section title="Trade ideas" sub="') + r".*?" + re.escape("</Section>"),
                 R29_ADVICE_NEW, "<TradeAdvice s={s}", re.S)
    t = lit(t, "trades: any free agent can be the pickup", "fas.find((f) => f.id === pick[k]) || null",
            '(pick[k] ? s.players.find((f) => f.ft === "fa" && f.id === pick[k]) : null) || null',
            'f.ft === "fa" && f.id === pick[k]')
    t = sub_once(t, "trades: search box for the pickup",
                 re.escape('<select className={inp + " w-full mt-2"} value={pick[k] || ""}') + r".*?" + re.escape("</select>"),
                 R29_SEARCH_NEW, "<FaSearch s={s}", re.S)
    t = sub_once(t, "trades: two result tiles",
                 re.escape('<Card label="How they see it" ') + r".*?" + re.escape('<Card label="Raw value" ') + r".*?/>",
                 "{/* round 29: two result tiles only */}", "round 29: two result tiles only", re.S)
    t = lit(t, "trades: tiles side by side", '<div className="tb-tiles">', '<div className="tb-grid" data-r29="tiles">', 'data-r29="tiles"')
    for must in ("function TradeAdvice(", "function FaSearch(", "function TradeBuilder(", "function AdvicePanel(", "trades v10",
                 '<Section title="Rosters"', '<Card label="Their lineup"', "const goalieOut ="):
        if must not in t:
            fail("fantasy-gm.html looks damaged after round 29 (" + must + ").")
    return t


_fix_before_r29 = fix


def fix(t):
    return round29(_fix_before_r29(t))

# ---------- round 30: trade builder shows the waiver pickup under "You get" and your league ranks after the trade ----------
R30_HELPERS = r'''// ---------- round 30: league ranks before and after a trade (news_logos.py) ----------
function TradeRanks({ s, partner, give, get, adds, drops }) {
  const addIds = adds.filter(Boolean).map((p) => p.id), dropIds = drops.map((p) => p.id);
  const key = [partner, give.join(), get.join(), addIds.join(), dropIds.join()].join("|");
  const R = useMemo(() => {
    const G = new Set(give), T = new Set(get), A = new Set(addIds), D = new Set(dropIds);
    const players = s.players.map((p) => (G.has(p.id) ? { ...p, ft: partner } : T.has(p.id) || A.has(p.id) ? { ...p, ft: s.me } : D.has(p.id) ? { ...p, ft: "fa" } : p));
    const pos = (t) => { const i = t.rows.findIndex((x) => x.t.id === s.me); return { o: i + 1, st: i >= 0 ? t.rows[i].strength : 0, ...(t.grpRank[s.me] || {}) }; };
    const keep = __LT, after = leagueTable({ ...s, players });
    __LT = keep;
    return { b: pos(leagueTable(s)), a: pos(after) };
  }, [key, s.players, s.wk, s.blend, window.__PMODE]);
  const cell = (lab, b, a) => (
    <span key={lab} className="mr-4 whitespace-nowrap">{lab} <span className="text-slate-500">#{b || "-"}</span>{" \u2192 "}<span className={"font-semibold " + (a < b ? "text-green-700" : a > b ? "text-red-600" : "")}>#{a || "-"}</span></span>
  );
  const up = R.a.st - R.b.st;
  return (
    <div className="text-sm mt-3">
      <div className="text-xs uppercase tracking-wide text-slate-500 mb-1">Your league ranks after this trade</div>
      {cell("Overall", R.b.o, R.a.o)}{cell("Forwards", R.b.F, R.a.F)}{cell("Defence", R.b.D, R.a.D)}{cell("Goalies", R.b.G, R.a.G)}
      <span className="text-xs text-slate-500 whitespace-nowrap">Strength {f1(R.b.st)}{" \u2192 "}<span className={up > 0.05 ? "text-green-700" : up < -0.05 ? "text-red-600" : ""}>{f1(R.a.st)}</span> pts/week</span>
    </div>
  );
}

'''

R30_GET_OLD = r'''{sideBox("You get", Rv, get, setGet)}'''
R30_GET_NEW = r'''{sideBox("You get", Rv, get, setGet, picks.map((f, k) => (f ? <div key={"pk" + k} className="tb-chip"><TeamLogo t={f.t} size={18} /><span className="truncate">{shortN(f.n)}</span><span className="text-xs text-slate-500">{f.p}</span><span className="text-xs text-green-700 whitespace-nowrap">waiver pickup</span><button type="button" className="tb-x" onClick={() => setPick((x) => ({ ...x, [k]: undefined }))}>{"\u00d7"}</button></div> : null)))}'''
R30_TOTAL_OLD = r'''{list.length ? <div className="text-xs text-slate-500 mt-1 pt-1 border-t border-slate-100">'''
R30_RANKS_OLD = r'''{(() => { const a = cnt(res.after), b = cnt(mine); return ('''
R30_RANKS_NEW = r'''<TradeRanks s={s} partner={partner} give={give} get={get} adds={picks} drops={drops} />
            ''' + R30_RANKS_OLD


def round30(t):
    t = lit(t, "trade ranks: side box takes extras", "const sideBox = (lab, list, sel, set) => (",
            "const sideBox = (lab, list, sel, set, extra) => (", "const sideBox = (lab, list, sel, set, extra)")
    t = lit(t, "trade ranks: extras shown in the box", R30_TOTAL_OLD, "{extra || null}" + R30_TOTAL_OLD, "{extra || null}")
    t = lit(t, "trade ranks: pickup under You get", R30_GET_OLD, R30_GET_NEW, "waiver pickup</span>")
    t = lit(t, "trade ranks: ranks after the trade", R30_RANKS_OLD, R30_RANKS_NEW, "<TradeRanks s={s}")
    t = lit(t, "trade ranks: helpers", ROOT, R30_HELPERS + ROOT, "function TradeRanks(")
    for must in ("function TradeRanks(", "function TradeBuilder(", "<TradeAdvice s={s}", "<FaSearch s={s}", 'sideBox("You give", Gv, give, setGive)'):
        if must not in t:
            fail("fantasy-gm.html looks damaged after round 30 (" + must + ").")
    return t


_fix_before_r30 = fix


def fix(t):
    return round30(_fix_before_r30(t))

# ---------- round 31: player pop-up. Past games with box scores, click a line to open that team's lines, calmer Lines page ----------
SYNC31_BLOCK = r'''    # 3e) box-score history for the player pop-up: one small file per finished day (news_logos.py round 31)
    try:
        bdir31_ = os.path.join(HERE, "box")
        os.makedirs(bdir31_, exist_ok=True)
        ipath31_ = os.path.join(bdir31_, "index.json")
        try:
            with open(ipath31_, encoding="utf-8") as f31_:
                idx31_ = json.load(f31_)
        except Exception:
            idx31_ = {}
        have31_, none31_ = set(idx31_.get("dates") or []), set(idx31_.get("none") or [])
        d31_ = min(period_date.values()) if period_date else day1
        todo31_ = []
        while d31_ <= today_et:
            if d31_.isoformat() not in have31_ and d31_.isoformat() not in none31_:
                todo31_.append(d31_.isoformat())
            d31_ += timedelta(days=1)
        new31_ = 0
        for dd31_ in todo31_[:12]:
            try:
                sj31_ = requests.get(f"https://api-web.nhle.com/v1/score/{dd31_}", headers={"User-Agent": "Mozilla/5.0"}, timeout=20).json()
                gms31_ = [g31_ for g31_ in sj31_.get("games", []) if g31_.get("gameType", 2) == 2 and str(g31_.get("gameScheduleState") or "OK") == "OK"]
                if not gms31_:
                    if dd31_ < today_et.isoformat():
                        none31_.add(dd31_)
                    continue
                if not all(str(g31_.get("gameState") or "") in ("FINAL", "OFF") for g31_ in gms31_):
                    continue
                fp31_ = {}
                for tm31_ in (daily.get(dd31_) or {}).values():
                    for pid31_, v31_ in tm31_.items():
                        if v31_ and v31_[0] is not None:
                            fp31_[str(pid31_)] = v31_[0]
                out31_ = {}
                for g31_ in gms31_:
                    bx31_ = requests.get(f"https://api-web.nhle.com/v1/gamecenter/{g31_['id']}/boxscore", headers={"User-Agent": "Mozilla/5.0"}, timeout=20).json()
                    pbg31_ = bx31_.get("playerByGameStats") or {}
                    sc31_ = {s31_: (bx31_.get(s31_) or g31_.get(s31_) or {}) for s31_ in ("homeTeam", "awayTeam")}
                    ab31_ = {}
                    for s31_ in ("homeTeam", "awayTeam"):
                        a31_ = str(sc31_[s31_].get("abbrev") or "").upper()
                        ab31_[s31_] = ALIAS.get(a31_, a31_)
                    for s31_, o31_ in (("homeTeam", "awayTeam"), ("awayTeam", "homeTeam")):
                        grp31_ = pbg31_.get(s31_) or {}
                        base31_ = {"t": ab31_[s31_], "o": ab31_[o31_], "h": 1 if s31_ == "homeTeam" else 0,
                                   "my": sc31_[s31_].get("score"), "op": sc31_[o31_].get("score")}
                        for x31_ in (grp31_.get("forwards") or []) + (grp31_.get("defense") or []) + (grp31_.get("goalies") or []):
                            nm31_ = (x31_.get("name") or {}).get("default") or ""
                            pid31_ = _pidx.get((_nk(nm31_), ab31_[s31_])) or _pidx.get((_nk2(nm31_), ab31_[s31_]))
                            if not pid31_:
                                continue
                            if "saves" in x31_ or "goalsAgainst" in x31_ or "saveShotsAgainst" in x31_:
                                if not x31_.get("toi") or x31_.get("toi") == "00:00":
                                    continue
                                ln31_ = {"sv": x31_.get("saves") or 0, "ga": x31_.get("goalsAgainst") or 0, "dec": x31_.get("decision") or "",
                                         "toi": x31_.get("toi") or "", "sa": x31_.get("shotsAgainst"), "svp": x31_.get("savePctg")}
                            else:
                                ln31_ = {"g": x31_.get("goals") or 0, "a": x31_.get("assists") or 0, "pm": x31_.get("plusMinus") or 0,
                                         "sog": x31_.get("sog") or 0, "pim": x31_.get("pim") or 0, "hit": x31_.get("hits") or 0,
                                         "blk": x31_.get("blockedShots") or 0, "toi": x31_.get("toi") or "", "ppg": x31_.get("powerPlayGoals") or 0,
                                         "fo": x31_.get("faceoffWinningPctg"), "shf": x31_.get("shifts"), "gv": x31_.get("giveaways") or 0, "tk": x31_.get("takeaways") or 0}
                            ln31_.update(base31_)
                            if str(pid31_) in fp31_:
                                ln31_["fp"] = fp31_[str(pid31_)]
                            out31_[str(pid31_)] = ln31_
                with open(os.path.join(bdir31_, dd31_ + ".json"), "w", encoding="utf-8") as f31_:
                    json.dump({"d": dd31_, "p": out31_}, f31_, separators=(",", ":"))
                have31_.add(dd31_)
                new31_ += 1
            except Exception as ex31_:
                print(f"(box) history for {dd31_} failed: {ex31_}")
        with open(ipath31_, "w", encoding="utf-8") as f31_:
            json.dump({"dates": sorted(have31_), "none": sorted(none31_)}, f31_, separators=(",", ":"))
        print(f"(box) history: {new31_} new day(s), {len(have31_)} saved in total")
    except Exception as ex31_:
        print(f"(box) history failed: {ex31_}")
'''

_fix_sync_before_r31 = PY_FIXES[SYNC]


def fix_sync31(t):
    t = _fix_sync_before_r31(t)
    t = lit(t, "sync: box-score history", '    data["pstat"] = pstat\n', '    data["pstat"] = pstat\n' + SYNC31_BLOCK, "# 3e) box-score history")
    py_ok(SYNC, t)
    return t


PY_FIXES[SYNC] = fix_sync31

LT31_ANCHOR = "  // ---------- player detail card (unchanged from the old Lines tab) ----------"
LT31_GAMELOG = r'''  // ---------- game log: past games with box scores (news_logos.py round 31) ----------
  const BOX = (window.__BOX = window.__BOX || { idx: null, at: 0, days: {} });
  const boxIndex = () => {
    if (BOX.idx && Date.now() - BOX.at < 10 * 60 * 1000) return Promise.resolve(BOX.idx);
    return fetch("box/index.json?t=" + Date.now()).then((r) => (r.ok ? r.json() : null))
      .then((j) => { BOX.idx = new Set((j && j.dates) || []); BOX.at = Date.now(); return BOX.idx; })
      .catch(() => { BOX.idx = BOX.idx || new Set(); return BOX.idx; });
  };
  const boxDay = (d) => (BOX.days[d] ? Promise.resolve(BOX.days[d])
    : fetch("box/" + d + ".json").then((r) => (r.ok ? r.json() : null)).then((j) => { if (j && j.p) BOX.days[d] = j.p; return (j && j.p) || {}; }).catch(() => ({})));
  const fpEst = (x, sc) => (x.sv != null
    ? (x.dec === "W" ? (sc.W ?? 5) : 0) + (x.dec === "O" ? (sc.OTL ?? 1) : 0) + (x.sv || 0) * (sc.SV ?? 0.6) + (x.ga || 0) * (sc.GA ?? -3) + (x.dec === "W" && !x.ga ? (sc.SO ?? 5) : 0)
    : (x.g || 0) * (sc.G ?? 6) + (x.a || 0) * (sc.A ?? 4) + (x.pm || 0) * (sc.PM ?? 2) + (x.sog || 0) * (sc.SOG ?? 1) + (x.hit || 0) * (sc.HIT ?? 0.1) + (x.blk || 0) * (sc.BLK ?? 1) + (x.ppg || 0) * (sc.PPP ?? 2));
  const glLine = (x) => (x.sv != null
    ? [x.dec === "W" ? "Win" : x.dec === "L" ? "Loss" : x.dec === "O" ? "OT loss" : null, x.sa != null ? x.sv + " of " + x.sa + " saves" : x.sv + " saves", (x.ga || 0) + " GA", x.toi ? x.toi + " TOI" : null]
    : [(x.g || 0) + " G", (x.a || 0) + " A", (x.pm > 0 ? "+" : "") + (x.pm || 0), (x.sog || 0) + " SOG", (x.hit || 0) + " HIT", (x.blk || 0) + " BLK", x.toi ? x.toi + " TOI" : null]).filter(Boolean).join(", ");
  const glTiles = (x) => (x.sv != null
    ? [["Decision", x.dec || "-"], ["Saves", x.sa != null ? x.sv + "/" + x.sa : x.sv], ["SV%", x.svp != null ? Number(x.svp).toFixed(3).replace(/^0/, "") : "-"], ["GA", x.ga || 0], ["TOI", x.toi || "-"]]
    : [["G", x.g || 0], ["A", x.a || 0], ["PTS", (x.g || 0) + (x.a || 0)], ["+/-", (x.pm > 0 ? "+" : "") + (x.pm || 0)], ["SOG", x.sog || 0], ["PP goals", x.ppg ?? 0], ["PIM", x.pim || 0], ["HIT", x.hit || 0], ["BLK", x.blk || 0],
      ["FO%", x.fo ? Math.round(x.fo * 100) + "%" : "-"], ["Takeaways", x.tk ?? 0], ["Giveaways", x.gv ?? 0], ["Shifts", x.shf ?? "-"], ["TOI", x.toi || "-"]]);
  function GameLog({ p, it, s, H }) {
    const today = H.todayISO(), id = String(p.id).slice(1), sc = s.sc || {};
    const [rows, setRows] = useState(null);
    const [all, setAll] = useState(false);
    const [open, setOpen] = useState(null);
    const past = useMemo(() => (H.SCHED && H.SCHED[it.t] ? [...H.SCHED[it.t]].filter((d) => d <= today).sort().reverse() : []), [it.t, today]);
    useEffect(() => {
      let dead = false;
      setRows(null); setOpen(null);
      const want = all ? past : past.slice(0, 14);
      boxIndex().then((idx) => Promise.all(want.map((d) => {
        const live = H.pStat ? H.pStat(p, d) : null;
        return idx.has(d) ? boxDay(d).then((day) => ({ d, x: day[id] || live || null })) : Promise.resolve({ d, x: live });
      }))).then((list) => { if (!dead) setRows(list.filter((r) => r.x)); });
      return () => { dead = true; };
    }, [p.id, it.t, all]);
    const ptsOf = (r) => { const a = r.x.fp != null ? r.x.fp : realPts(p, r.d); return a != null ? { v: a, est: false } : { v: fpEst(r.x, sc), est: true }; };
    const shown = (rows || []).slice(0, all ? 999 : 10).map((r) => ({ ...r, pt: ptsOf(r) }));
    const avg = shown.length ? shown.reduce((a, r) => a + r.pt.v, 0) / shown.length : 0;
    const anyEst = shown.some((r) => r.pt.est);
    return (
      <div className="mt-4">
        <div className="flex flex-wrap items-baseline gap-2 mb-1">
          <div className="font-medium text-sm">Recent games</div>
          {shown.length ? <span className="text-xs text-slate-500">{H.f1(avg)} fantasy pts a game over the last {shown.length}</span> : null}
        </div>
        {rows === null ? <div className="text-xs text-slate-400">Loading games...</div>
          : !shown.length ? <div className="text-xs text-slate-400">No finished games saved yet. Game history fills in after the next sync.</div>
          : shown.map((r) => {
            const x = r.x, gm = ((((window.GAMES_DATA || {}).games || {})[r.d]) || {})[it.t] || null, live = H.gScore ? H.gScore(it.t, r.d) : null;
            const o = x.o || (gm ? gm.o : ""), h = x.o ? x.h : gm ? gm.h : null;
            const my = x.my != null ? x.my : live ? live.my : null, op = x.op != null ? x.op : live ? live.op : null;
            const res = my != null && op != null ? (my > op ? "W " : my < op ? "L " : "") + my + "-" + op : "";
            return (
              <div key={r.d} className="border-t border-slate-100 py-2 cursor-pointer" onClick={() => setOpen(open === r.d ? null : r.d)}>
                <div className="flex items-baseline gap-3 text-sm">
                  <span className="whitespace-nowrap" style={{ minWidth: 84 }}>{H.dayLabel(r.d)}</span>
                  <span className="text-slate-500 whitespace-nowrap">{o ? (h ? "vs " : "@ ") + o : ""}</span>
                  <span className={"whitespace-nowrap text-xs " + (my > op ? "text-green-700" : my < op ? "text-red-600" : "text-slate-500")}>{res}</span>
                  <span className="ml-auto font-semibold whitespace-nowrap">{(r.pt.est ? "~" : "") + H.f1(r.pt.v)}</span>
                </div>
                <div className="text-xs text-slate-500 mt-0.5">{glLine(x)}</div>
                {open === r.d ? <div className="grid grid-cols-4 md:grid-cols-7 gap-2 mt-2">{glTiles(x).map(([l, v]) => (
                  <div key={l} className="rounded-lg border border-slate-200 px-2 py-1.5 text-center"><div className="text-[10px] uppercase tracking-wide text-slate-500">{l}</div><div className="font-semibold">{v}</div></div>
                ))}</div> : null}
              </div>
            );
          })}
        {!all && past.length > 14 ? <button className="lt-link" onClick={() => setAll(true)}>Show all games</button> : null}
        {shown.length ? <div className="text-xs text-slate-400 mt-1">Tap a game for its full box score.{anyEst ? " ~ means estimated from the box score, without power-play assists or shorthanded points." : ""}</div> : null}
      </div>
    );
  }

'''

LT31_LINE_OLD = r'''{isG ? `Goalie for ${it.t}` : `${LBL[w.es]} for ${it.t}`}'''
LT31_LINE_NEW = r'''<button className="underline" title="Open this team's lines" onClick={() => { if (window.__NAV && window.__NAV.lines) window.__NAV.lines(it.t); }}>{isG ? `Goalie for ${it.t}` : `${LBL[w.es]} for ${it.t}`}</button>'''

LT31_OPEN_NEW = r'''const [open, setOpen] = useState({});
    useEffect(() => {
      // round 31: open one team's lines when a player's line is clicked (news_logos.py)
      const show = (t) => {
        if (!t) return;
        window.__LINES_TEAM = null;
        setOnlyMine(false); setOpen((o) => ({ ...o, [t]: true }));
        setTimeout(() => { const el = document.getElementById("lt-team-" + t); if (el) el.scrollIntoView({ behavior: "smooth", block: "start" }); }, 150);
      };
      show(window.__LINES_TEAM);
      const h = (e) => show(e.detail);
      window.addEventListener("gm-lines-team", h);
      return () => window.removeEventListener("gm-lines-team", h);
    }, []);'''

LT31_ALL_OLD = r'''<label className="flex items-center gap-1 text-xs"><input type="checkbox" checked={onlyMine}'''
LT31_ALL_NEW = r'''<button className="lt-link" style={{ padding: 0 }} onClick={() => setOpen(Object.keys(open).some((k) => open[k]) ? {} : Object.fromEntries(Object.keys(L.teams || {}).map((k) => [k, true])))}>{Object.keys(open).some((k) => open[k]) ? "Close all teams" : "Open all teams"}</button>
          ''' + LT31_ALL_OLD

_fix_lines_before_r31 = JS_FIXES[LINES]


def fix_lines31(t):
    t = _fix_lines_before_r31(t)
    t = lit(t, "lines: game log for the pop-up", LT31_ANCHOR, LT31_GAMELOG + LT31_ANCHOR, "function GameLog(")
    t = lit(t, "lines: recent games in the pop-up", "{games.length > 0 && (",
            "{hasId ? <GameLog p={p} it={it} s={s} H={H} /> : null}\n        {games.length > 0 && (", "<GameLog p={p}")
    t = lit(t, "lines: click a line to open the team", LT31_LINE_OLD, LT31_LINE_NEW, "window.__NAV.lines(it.t)")
    t = lit(t, "lines: open a team when asked", "const [open, setOpen] = useState({});", LT31_OPEN_NEW, "round 31: open one team's lines")
    t = lit(t, "lines: team rows can be scrolled to", '<div key={x.t} className={"lt-team" + (isOpen ? " open" : "")}>',
            '<div key={x.t} id={"lt-team-" + x.t} style={{ scrollMarginTop: 120 }} className={"lt-team" + (isOpen ? " open" : "")}>',
            'id={"lt-team-" + x.t}')
    t = lit(t, "lines: open all teams link", LT31_ALL_OLD, LT31_ALL_NEW, "Open all teams")
    t = lit(t, "lines: changes box starts closed", '<H.Section title="Line & roster changes"', '<H.Section closed title="Line & roster changes"',
            '<H.Section closed title="Line & roster changes"')
    if "lt-legend-wrap" in t:
        print("(news) lines: colour key in a drop-down: already done")
    else:
        t, n31 = re.subn(r'<div className="lt-legend">.*?</div>',
                         lambda m: '<details className="lt-how lt-legend-wrap"><summary>What the colours and marks mean</summary>' + m.group(0) + "</details>",
                         t, flags=re.S)
        if n31 != 1:
            fail(f"'lines: colour key in a drop-down' matched {n31} times (expected 1). Send this log to the AI helper.")
        print("(news) lines: colour key in a drop-down: updated")
    for must in ("function GameLog(", "function PlayerCard(", "function Teams(", "window.PlayerPopup = PlayerPopup;", "game box score v23", "H.TeamLogo t={x.t} size={32}"):
        if must not in t:
            fail("lines-tab.js looks damaged after round 31 (" + must + ").")
    babel_ok(t, LINES)
    return t


JS_FIXES[LINES] = fix_lines31

R31_NAV_OLD = "player: (p) => { if (p) setPlayer(p); } };"
R31_NAV_NEW = ('player: (p) => { if (p) setPlayer(p); }, lines: (t) => { window.__LINES_TEAM = t; go("lines"); '
               'try { window.dispatchEvent(new CustomEvent("gm-lines-team", { detail: t })); } catch (e) {} } };')


def round31(t):
    t = lit(t, "pop-up: schedule for game history", "Card, Pills, inp, todayISO, dayLabel, TL, TeamLogo };",
            "Card, Pills, inp, SCHED, todayISO, dayLabel, TL, TeamLogo };", "Pills, inp, SCHED, todayISO")
    t = lit(t, "pop-up: jump to a team's lines", R31_NAV_OLD, R31_NAV_NEW, 'window.__LINES_TEAM = t; go("lines");')
    for must in ("const LH = { gState, actDay, LiveTag,", "dayLabel, TL, TeamLogo };", "window.__TAB = tab", "LiveTag, pStat, gScore,"):
        if must not in t:
            fail("fantasy-gm.html looks damaged after round 31 (" + must + ").")
    return t


_fix_before_r31 = fix


def fix(t):
    return round31(_fix_before_r31(t))

# ---------- round 32: black and white theme with light mode, new top bar, new Today page ----------
R32_CSS = r'''  /* round 32 theme and Today (news_logos.py) */
  :root { color-scheme: dark; --bg:#0c0d0f; --card:#141518; --card2:#101113; --card3:#1b1c20; --line:#232529; --line2:#34363b; --ink:#f4f5f6; --ink2:#d0d2d6; --mute:#8a8d93; --faint:#5d6066; --accent:#ffffff; --accentSoft:rgba(255,255,255,.08); --good:#5fd08a; --bad:#f06a6a; --warn:#f5c451; --track:#26282c; --hover:rgba(255,255,255,.05); --glass:rgba(12,13,15,.84); --on:#0c0d0f; }
  html[data-theme="light"] { color-scheme: light; --bg:#f5f5f4; --card:#ffffff; --card2:#fafaf9; --card3:#efefed; --line:#e0e0de; --line2:#cfcfcc; --ink:#111214; --ink2:#2c2e33; --mute:#63666b; --faint:#93969b; --accent:#000000; --accentSoft:rgba(0,0,0,.06); --good:#16a34a; --bad:#dc2626; --warn:#b45309; --track:#e4e4e2; --hover:rgba(0,0,0,.04); --glass:rgba(245,245,244,.88); --on:#ffffff; }
  body { color: var(--ink); }
  .bg-slate-800 { background-color: var(--card3) !important; }
  .bg-slate-900 { background-color: var(--glass) !important; }
  .text-slate-600 { color: var(--ink2) !important; }
  .text-slate-300 { color: var(--faint) !important; }
  .border-slate-400, .border-b-slate-400 { border-color: var(--line2) !important; }
  .bg-blue-500, .bg-blue-600 { background-color: var(--ink) !important; color: var(--on) !important; border-color: var(--ink) !important; }
  .bg-red-600 { background-color: var(--bad) !important; color: #ffffff !important; }
  .m-icon, .ms-list { background: var(--card3); }
  .m-slot { background: var(--card2); }
  .tb-p.on .tb-chk { color: var(--on); }
  input[type=date] { color-scheme: inherit; }
  html[data-theme="light"] .text-sky-600 { color: #0369a1 !important; }
  html[data-theme="light"] .text-orange-600 { color: #c2410c !important; }
  .font-semibold.text-base, .font-bold.text-lg { font-family: Inter, ui-sans-serif, system-ui, -apple-system, sans-serif; font-weight: 600 !important; font-size: 1.05rem !important; letter-spacing: -0.01em; }
  button.text-blue-600, a.text-blue-600, button.text-blue-700 { text-decoration: underline; text-decoration-color: var(--line2); text-underline-offset: 3px; }
  .gx-tag { font-size: 12px; color: var(--mute); letter-spacing: .06em; }
  .gx-num { font-variant-numeric: tabular-nums; font-weight: 600; letter-spacing: -.02em; line-height: 1.1; }
  .gx-pn { position: relative; padding: 14px 16px; background: var(--card); }
  .gx-pn > b { position: absolute; width: 10px; height: 10px; border: 0 solid var(--accent); }
  .gx-pn > b:nth-child(1) { top: 0; left: 0; border-top-width: 1.5px; border-left-width: 1.5px; }
  .gx-pn > b:nth-child(2) { top: 0; right: 0; border-top-width: 1.5px; border-right-width: 1.5px; }
  .gx-pn > b:nth-child(3) { bottom: 0; left: 0; border-bottom-width: 1.5px; border-left-width: 1.5px; }
  .gx-pn > b:nth-child(4) { bottom: 0; right: 0; border-bottom-width: 1.5px; border-right-width: 1.5px; }
  .gx-svg text { font-family: Inter, ui-sans-serif, system-ui, -apple-system, sans-serif; font-variant-numeric: tabular-nums; }
  .gx-tab { font-size: 15px; padding: 6px 10px 12px; border-bottom: 2px solid transparent; color: var(--mute); white-space: nowrap; }
  .gx-tab:hover { color: var(--ink); }
  .gx-tab.on { color: var(--ink); font-weight: 600; border-bottom-color: var(--accent); }
  .gx-badge { width: 28px; height: 28px; border-radius: 999px; border: 1.5px solid var(--accent); color: var(--accent); display: inline-flex; align-items: center; justify-content: center; font-weight: 600; font-size: 13px; flex-shrink: 0; margin-bottom: 10px; }
  .gx-menu { position: absolute; right: 0; top: calc(100% + 6px); z-index: 60; min-width: 240px; background: var(--card3); border: 1px solid var(--line2); border-radius: 10px; padding: 6px; }
  .gx-mi { display: block; width: 100%; text-align: left; padding: 8px 10px; border-radius: 6px; font-size: 14px; color: var(--ink); }
  .gx-mi:hover { background: var(--hover); }
'''

R32_HEAD = ('<script>(function(){var k="fantasy-islands-gm-theme";function pref(){try{return localStorage.getItem(k)||"auto"}catch(e){return"auto"}}'
            'function ap(){var v=pref(),d=v==="auto"?(window.matchMedia&&window.matchMedia("(prefers-color-scheme: light)").matches?"light":"dark"):v;'
            'document.documentElement.setAttribute("data-theme",d);var m=document.querySelector(\'meta[name="theme-color"]\');'
            'if(m)m.setAttribute("content",d==="light"?"#f5f5f4":"#0c0d0f");}'
            'window.__themePref=pref;window.__setTheme=function(v){try{localStorage.setItem(k,v)}catch(e){}ap();window.dispatchEvent(new Event("gm-theme"));};ap();'
            'try{window.matchMedia("(prefers-color-scheme: light)").addEventListener("change",function(){ap();window.dispatchEvent(new Event("gm-theme"));});}catch(e){}'
            '})();</script>\n')

R32_HELPERS = r'''// ---------- round 32: theme switch, top bar, Today gauges and week chart (news_logos.py) ----------
const ThemeBtn = ({ cls }) => {
  const v = window.__themePref ? window.__themePref() : "auto";
  const next = v === "auto" ? "light" : v === "light" ? "dark" : "auto";
  return <button type="button" className={cls || "text-xs text-slate-500"} title="Switch between automatic, light and dark" onClick={() => window.__setTheme && window.__setTheme(next)}>{"Theme: " + (v === "auto" ? "automatic" : v)}</button>;
};
const ordN = (n) => n + (n % 100 >= 11 && n % 100 <= 13 ? "th" : ["th", "st", "nd", "rd"][n % 10] || "th");
const lastN = (n) => { const x = String(n || "").split(" "); return x.length > 1 ? x.slice(1).join(" ") : x[0]; };
const GX_TABS = [["today", "Today"], ["matchup", "Matchup"], ["myteam", "Team"], ["moves", "Moves"], ["league", "League"]];
const GX_MORE = [["teams", "Teams"], ["lines", "Lines"], ["news", "News"], ["setup", "Setup"]];
function TopBar({ s, setS, tab, go, ageH }) {
  const [open, setOpen] = useState(false);
  const [rank, setRank] = useState(null);
  useEffect(() => {
    const id = setTimeout(() => { try { const T = leagueTable(s), i = T.rows.findIndex((x) => x.t.id === s.me); setRank(i >= 0 ? [i + 1, T.rows.length] : null); } catch (e) {} }, 400);
    return () => clearTimeout(id);
  }, [s.players, s.wk, s.blend, window.__PMODE]);
  useEffect(() => {
    if (!open) return;
    const h = (e) => { if (!e.target.closest || !e.target.closest(".gx-more")) setOpen(false); };
    document.addEventListener("mousedown", h);
    return () => document.removeEventListener("mousedown", h);
  }, [open]);
  const name = teamName(s, s.me) || "My team";
  const more = GX_MORE.find(([k]) => k === tab);
  const sync = s.lastSync ? toDate(s.lastSync) : null;
  const pick = (k) => { setOpen(false); go(k); };
  return (
    <div className="m-hide max-w-6xl mx-auto px-3 flex items-end gap-1" style={{ paddingTop: 10 }}>
      <span className="gx-badge">{(name[0] || "K").toUpperCase()}</span>
      <span style={{ margin: "0 14px 10px 8px", lineHeight: 1.2, minWidth: 0 }}>
        <span className="block font-semibold truncate" style={{ maxWidth: 180 }}>{name}</span>
        <span className="block text-xs text-slate-500">{rank ? ordN(rank[0]) + " of " + rank[1] : s.league || "\u00a0"}</span>
      </span>
      {GX_TABS.map(([k, l]) => <button key={k} onClick={() => pick(k)} className={"gx-tab" + (tab === k ? " on" : "")}>{l}</button>)}
      <div className="relative gx-more">
        <button onClick={() => setOpen(!open)} className={"gx-tab" + (more || open ? " on" : "")}>{more ? more[1] : "More"}</button>
        {open ? (
          <div className="gx-menu">
            {GX_MORE.map(([k, l]) => <button key={k} className="gx-mi" onClick={() => pick(k)}>{l}</button>)}
            <a className="gx-mi" href="ai-dashboard.html">AI Lab</a>
            <div style={{ borderTop: "1px solid var(--line)", margin: "6px 0" }}></div>
            <div className="px-2 pb-1 text-xs text-slate-500">Week</div>
            <select className={inp + " w-full"} value={s.wk} onChange={(e) => setS({ ...s, wk: +e.target.value })}>
              {s.weeks.map((w, i) => <option key={i} value={i}>{w.label}</option>)}
            </select>
            <div className="px-2 pt-2 pb-1 text-xs text-slate-500">Projections</div>
            <select className={inp + " w-full"} value={window.__PMODE} onChange={(e) => setS({ ...s, pmode: e.target.value, players: [...s.players] })}>
              <option value="espn">ESPN</option>
              <option value="blend" disabled={!window.__MODEL}>Blend</option>
              <option value="model" disabled={!window.__MODEL}>GM model</option>
              <option value="ai" disabled={!window.__MODEL || !window.__AI}>AI (beta)</option>
            </select>
            <div className="pt-2"><ThemeBtn cls="gx-mi" /></div>
          </div>
        ) : null}
      </div>
      <span className="ml-auto text-xs text-slate-500 whitespace-nowrap" style={{ marginBottom: 12 }} title={s.lastSync ? "Synced " + fmtTime(s.lastSync) : ""}>
        <span style={{ display: "inline-block", width: 6, height: 6, borderRadius: 99, marginRight: 6, verticalAlign: 1, background: !s.lastSync ? "var(--faint)" : ageH !== null && ageH > 2 ? "var(--bad)" : "var(--good)" }}></span>
        {sync ? "Synced " + sync.toLocaleTimeString([], { hour: "numeric", minute: "2-digit" }) : "Not synced yet"}
      </span>
    </div>
  );
}
const GxRing = ({ v, big }) => {
  const size = big ? 104 : 64, m = size / 2, r = big ? 36 : 26, w = big ? 6 : 5, c = 2 * Math.PI * r;
  const p = v == null ? 0 : Math.max(0.01, Math.min(0.99, v));
  const col = v == null ? "var(--faint)" : v >= 0.5 ? "var(--good)" : "var(--bad)";
  return (
    <svg viewBox={"0 0 " + size + " " + size} width={size} height={size} className="gx-svg" style={{ flexShrink: 0, display: "block" }} role="img" aria-label={v == null ? "Win chance not available" : wpTxt(v) + " chance to win"}>
      {big ? <circle cx={m} cy={m} r={44} style={{ fill: "none", stroke: "var(--track)", strokeWidth: 1, strokeDasharray: "1 5.9" }} /> : null}
      <circle cx={m} cy={m} r={r} style={{ fill: "none", stroke: "var(--track)", strokeWidth: w }} />
      <circle cx={m} cy={m} r={r} transform={"rotate(-90 " + m + " " + m + ")"} style={{ fill: "none", stroke: col, strokeWidth: w, strokeDasharray: (p * c).toFixed(1) + " " + c.toFixed(1) }} />
      <text x={m} y={big ? m + 3 : m + 5} textAnchor="middle" style={{ fontSize: big ? 21 : 15, fontWeight: 600, fill: big ? col : "var(--ink)" }}>{v == null ? "\u2013" : wpTxt(v)}</text>
      {big ? <text x={m} y={m + 18} textAnchor="middle" style={{ fontSize: 11, fill: "var(--mute)" }}>to win</text> : null}
    </svg>
  );
};
function GxWeek({ wk, A, B, aA, aB }) {
  const dates = wk.dates || [], n = dates.length, today = todayISO();
  if (!n) return null;
  let run = (aA - aB) - (A.act - B.act);
  const rows = dates.map((dt, d) => { const x = A.days[d], y = B.days[d], dv = x.act + x.total - (y.act + y.total); run += dv; return { dt, dv, run, st: dt < today ? "f" : dt === today ? "t" : "p" }; });
  const grid = Math.max(10, Math.ceil(rows.reduce((mx, r) => Math.max(mx, Math.abs(r.dv)), 0) / 10) * 10), sc = 46 / grid;
  const L = 34, colW = (600 - L) / n, cx = (i) => L + colW * (i + 0.5), bw = Math.min(30, colW * 0.42);
  const lo = Math.min.apply(null, rows.map((r) => r.run)), hi = Math.max.apply(null, rows.map((r) => r.run));
  const ry = (v) => (hi === lo ? 167 : 178 - ((v - lo) / (hi - lo)) * 22);
  const ci = rows.findIndex((r) => r.st !== "f"), last = ci < 0 ? n - 1 : ci - 1;
  const pts = (a, b) => rows.slice(a, b + 1).map((r, i) => cx(a + i).toFixed(1) + "," + ry(r.run).toFixed(1)).join(" ");
  const sg = (v) => (v > 0 ? "+" : "") + Math.round(v);
  const col = (v) => (v >= 0 ? "var(--good)" : "var(--bad)");
  const tx = (size, fill, weight) => ({ fontSize: size, fill, fontWeight: weight || 400 });
  const nowLeft = last >= n - 3;
  return (
    <svg viewBox="0 0 620 196" width="100%" className="gx-svg" style={{ display: "block", marginTop: 6 }} role="img" aria-label="Margin each day this week and the running total">
      {rows.map((r, i) => (r.st === "t" ? <rect key={"h" + i} x={cx(i) - colW / 2 + 2} y={4} width={colW - 4} height={136} style={{ fill: "var(--accentSoft)" }} /> : null))}
      <line x1={L} y1={36} x2={600} y2={36} style={{ stroke: "var(--line)", strokeDasharray: "2 4" }} />
      <line x1={L} y1={82} x2={600} y2={82} style={{ stroke: "var(--faint)" }} />
      <line x1={L} y1={128} x2={600} y2={128} style={{ stroke: "var(--line)", strokeDasharray: "2 4" }} />
      <text x={26} y={40} textAnchor="end" style={tx(11, "var(--faint)")}>{"+" + grid}</text>
      <text x={26} y={86} textAnchor="end" style={tx(11, "var(--faint)")}>0</text>
      <text x={26} y={132} textAnchor="end" style={tx(11, "var(--faint)")}>{"-" + grid}</text>
      {rows.map((r, i) => {
        const h = Math.max(1, Math.abs(r.dv) * sc), up = r.dv >= 0, y = up ? 81 - h : 83, flat = Math.abs(r.dv) < 0.05;
        return (
          <g key={r.dt}>
            <text x={cx(i)} y={18} textAnchor="middle" style={tx(12, r.st === "t" ? "var(--accent)" : "var(--mute)", r.st === "t" ? 600 : 400)}>{r.st === "t" ? "Today" : dayLabel(r.dt).split(",")[0]}</text>
            {flat ? null : r.st === "p"
              ? <rect x={cx(i) - bw / 2 + 0.5} y={y + 0.5} width={bw - 1} height={Math.max(1, h - 1)} style={{ fill: "none", stroke: col(r.dv), strokeWidth: 1.5, strokeDasharray: "4 3" }} />
              : <rect x={cx(i) - bw / 2} y={y} width={bw} height={h} style={{ fill: col(r.dv) }} />}
            <text x={cx(i)} y={up && !flat ? 98 : 76} textAnchor="middle" style={tx(12, flat ? "var(--faint)" : col(r.dv))}>{flat ? "0" : sg(r.dv)}</text>
          </g>
        );
      })}
      <line x1={L} y1={152} x2={600} y2={152} style={{ stroke: "var(--line)" }} />
      {last >= 1 ? <polyline points={pts(0, last)} style={{ fill: "none", stroke: "var(--accent)", strokeWidth: 1.5 }} /> : null}
      {last < n - 1 ? <polyline points={pts(Math.max(last, 0), n - 1)} style={{ fill: "none", stroke: "var(--accent)", strokeWidth: 1.5, strokeDasharray: "4 4" }} /> : null}
      {rows.map((r, i) => (i <= last ? <circle key={"c" + i} cx={cx(i)} cy={ry(r.run)} r={i === last ? 3.5 : 2.5} style={i === last ? { fill: "var(--card)", stroke: "var(--accent)", strokeWidth: 1.5 } : { fill: "var(--accent)" }} /> : null))}
      {last >= 0 && ci >= 0 ? <text x={cx(last) + (nowLeft ? -8 : 8)} y={192} textAnchor={nowLeft ? "end" : "start"} style={tx(11, "var(--accent)")}>{sg(aA - aB) + " now"}</text> : null}
      <text x={600} y={192} textAnchor="end" style={tx(11, "var(--mute)")}>{sg(rows[n - 1].run) + (ci < 0 ? " final" : " projected")}</text>
    </svg>
  );
}

'''

# done markers of older rounds that lived inside the old Today page; they are kept as comments so those rounds stay "already done"
R32_KEEP = [
    "old or minor headline", "chance to win</span>", "<WinDelta s={s} add={r.f} drop={r.d} /><span", "<StrategyLine",
    "still projected \u00b7 {f1(fa)} final est.</div>", "still projected \u00b7 {f1(fb)} final est.</div>",
    'PickNote where="today"', '"Best moves for next week" : "Best moves this week"} sub={sameDrop ?',
    '<PlanNote sP={sP} /> : <PickNote where="today" />', "<WinDelta s={sP} add={r.f} drop={r.d} base={pBase} />",
    '<div className="hidden">+ {f1(A.total)} still projected', '<div className="hidden">+ {f1(B.total)} still projected',
    "round 28: advice sentence removed", "L.empty > 0 && !outOfMoves(s)", '"Injuries" + (outNow.length',
    '"News on your players" + (news.length', "Section: SectionShut", "computeMoves(sP, { H: 1, pool: 40 })",
]

R32_TODAY_BODY = r'''  const K = s.blend;
  const opp = oppOf(wk, s.me) || s.opp;
  const mine = s.players.filter((p) => p.ft === s.me), theirs = s.players.filter((p) => p.ft === opp);
  const A = weekLive(mine, wk, K, s.me), B = weekLive(theirs, wk, K, opp);
  const aA = +((wk.act || {})[s.me]) || 0, aB = +((wk.act || {})[opp]) || 0;
  const fa = aA + A.total, fb = aB + B.total, margin = fa - fb, ahead = margin >= 0;
  const dates = wk.dates || [], n = dates.length, today = todayISO(), done = wk.done || 0;
  const over = n > 0 && done >= n;
  const wp = winProb(A, B, aA, aB);
  const sN = useMemo(() => nextWkS(s), [s]);
  const sP = useMemo(() => planS(s), [s]);
  const nOpp = sN ? oppOf(sN.weeks[sN.wk] || {}, s.me) : null;
  const nWin = useMemo(() => (sN && nOpp ? winChance(sN) : null), [sN, nOpp]);
  const best = useMemo(() => {
    const r = computeMoves(sP, { H: 1, pool: 40 }).res.filter((x) => x.gain >= (s.minGain ?? 3))[0];
    if (!r) return null;
    return { r, b: sP === s ? winChance(s) : planBase(s, sP), a: winChance(sP, afterMove(sP, r.f, r.d)) };
  }, [sP]);
  const tag = "Week " + (s.wk + 1) + (!n ? "" : dates[0] > today ? " \u00b7 starts " + dayLabel(dates[0]) : over ? " \u00b7 final" : " \u00b7 day " + Math.min(n, done + 1) + " of " + n);
  const share = aA + aB > 0 ? Math.max(4, Math.min(96, (aA / (aA + aB)) * 100)) : 50;
  const big = { fontSize: "clamp(28px, 7vw, 40px)" };
  return (
    <div className="space-y-3">
      <div>
        <div className="gx-tag">{tag}</div>
        <div style={{ display: "grid", gridTemplateColumns: "minmax(0,1fr) 104px minmax(0,1fr)", alignItems: "center", marginTop: 6 }}>
          <div className="min-w-0">
            <div className="text-sm font-semibold truncate" style={{ color: "var(--accent)" }}>{teamName(s, s.me)}</div>
            <div className="gx-num" style={big}>{f1(aA)}</div>
          </div>
          <button type="button" title="Open the matchup" onClick={() => go("matchup")}><GxRing v={wp} big /></button>
          <div className="min-w-0 text-right">
            <div className="text-sm text-slate-500 truncate"><TL s={s} id={opp} /></div>
            <div className="gx-num" style={{ ...big, color: "var(--ink2)" }}>{f1(aB)}</div>
          </div>
        </div>
        <div style={{ display: "flex", height: 4, gap: 3, marginTop: 10 }}>
          <div style={{ width: share + "%", background: "var(--accent)" }}></div>
          <div style={{ flex: 1, background: "var(--track)" }}></div>
        </div>
        <div className="text-xs text-slate-500" style={{ display: "flex", marginTop: 6 }}>
          <span>{(over ? "Final " : "Projected ") + Math.round(fa)}</span>
          <span style={{ margin: "0 auto", color: ahead ? "var(--good)" : "var(--bad)" }}>{(ahead ? "Ahead by " : "Behind by ") + f1(Math.abs(margin))}</span>
          <span>{Math.round(fb)}</span>
        </div>
      </div>
      <div className="gx-pn"><b></b><b></b><b></b><b></b>
        <div style={{ display: "flex", alignItems: "baseline" }}>
          <span className="gx-tag">This week</span>
          <span className="text-xs text-slate-500" style={{ marginLeft: "auto" }}>Margin each day, and running total</span>
        </div>
        <GxWeek wk={wk} A={A} B={B} aA={aA} aB={aB} />
      </div>
      <div className="gx-pn"><b></b><b></b><b></b><b></b>
        <div style={{ display: "flex", alignItems: "center", gap: 14 }}>
          <GxRing v={nWin} />
          <div className="min-w-0" style={{ flex: 1 }}>
            <div className="gx-tag">Next week{nOpp ? <span> {"\u00b7"} vs <TL s={s} id={nOpp} /></span> : null}</div>
            {best ? (
              <button type="button" className="w-full text-left" style={{ display: "flex", alignItems: "center", gap: 10, marginTop: 8 }} onClick={() => go("moves", "advice")}>
                <span className="min-w-0">
                  <span className="block text-xs text-slate-500">{sP !== s ? "Best move for next week" : "Best move this week"}</span>
                  <span className="block truncate">{lastN(best.r.f.n)} in, {lastN(best.r.d.n)} out</span>
                </span>
                <span className="whitespace-nowrap" style={{ marginLeft: "auto", fontVariantNumeric: "tabular-nums", color: best.a != null && best.b != null && best.a < best.b ? "var(--bad)" : "var(--good)" }}>
                  {best.a != null && best.b != null ? wpTxt(best.b).replace("%", "") + " \u2192 " + wpTxt(best.a) : "+" + f1(best.r.gain)}
                </span>
                <span className="sec-chev shut" style={{ margin: "0 2px 0 4px" }}></span>
              </button>
            ) : <div className="text-sm text-slate-500" style={{ marginTop: 8 }}>No move worth making right now.</div>}
          </div>
        </div>
      </div>
    </div>
  );
}

'''

R32_TODAY = ("function Today({ s, wk, go }) {\n  // today v32: score with win ring, week chart, next week (news_logos.py)\n"
             "  // older done markers kept so earlier rounds stay finished:\n"
             + "".join("  // " + m32 + "\n" for m32 in R32_KEEP) + R32_TODAY_BODY)

R32_BAR_PAT = (re.escape('<div className="m-hide max-w-6xl mx-auto px-3 pt-2 pb-1 flex flex-wrap items-center gap-2">') + r".*?"
               + re.escape("{NAV.map(([k, l]) => (") + r".*?" + re.escape("))}") + r"\s*</div>")
R32_BAR_NEW = ("{/* round 32: new top bar (older marker kept: m-hide max-w-6xl mx-auto px-2) */}\n"
               "        <TopBar s={s} setS={setS} tab={tab} go={go} ageH={ageH} />")


def round32(t):
    t = lit(t, "theme: colours and Today styles", "</style>", R32_CSS + "</style>", "round 32 theme and Today")
    t = lit(t, "theme: light or dark before the page draws", "</head>", R32_HEAD + "</head>", "fantasy-islands-gm-theme")
    t = block(t, "theme: new Today page", "function Today({ s, wk, go }) {", "// ---------- Advice ----------", R32_TODAY, "today v32")
    t = sub_once(t, "theme: new top bar", R32_BAR_PAT, R32_BAR_NEW, "<TopBar s={s}", re.S)
    t = lit(t, "theme: redraw when the theme changes", "const [, tick] = useState(0);",
            'const [, tick] = useState(0);\n  useEffect(() => { const h32 = () => tick((x) => x + 1); window.addEventListener("gm-theme", h32); return () => window.removeEventListener("gm-theme", h32); }, []);',
            'window.addEventListener("gm-theme", h32)')
    t = lit(t, "theme: team logos for light mode", '(NHL_LOGO[t] || t) + "_dark.svg"',
            '(NHL_LOGO[t] || t) + (document.documentElement.getAttribute("data-theme") === "light" ? "_light.svg" : "_dark.svg")',
            '"_light.svg" : "_dark.svg"')
    t = lit(t, "theme: switch on the phone menu", '<a href="ai-dashboard.html" className="text-blue-600 ml-auto">AI Lab</a>',
            '<span className="ml-auto"><ThemeBtn /></span><a href="ai-dashboard.html" className="text-blue-600">AI Lab</a>',
            '<span className="ml-auto"><ThemeBtn /></span>')
    t = lit(t, "theme: lineup grid wording", "Violet = in your lineup", "Bright = in your lineup", "Bright = in your lineup")
    t = lit(t, "theme: helpers", ROOT, R32_HELPERS + ROOT, "function TopBar(")
    for must in R32_KEEP + ["function TopBar(", "function Today(", "function GxWeek(", "<MobileHeader s={s}", "m-hide max-w-6xl mx-auto px-2",
                            "weekLive(mine, wk, K, s.me)", "round 21: live NHL scores", "const planS =", "function TeamLogo("]:
        if must not in t:
            fail("fantasy-gm.html looks damaged after round 32 (" + must + ").")
    return t


_fix_before_r32 = fix


def fix(t):
    return round32(_fix_before_r32(t))


LT32_MAP = [("rgba(139,124,255,.06)", "var(--hover)"), ("rgba(139,124,255,.45)", "var(--line2)"), ("rgba(139,124,255,.1)", "var(--accentSoft)"),
            ("#292929", "var(--line)"), ("#5fd08a", "var(--good)"), ("#f06a6a", "var(--bad)"), ("#8f8f8f", "var(--mute)"), ("#8b7cff", "var(--accent)"),
            ("#161616", "var(--card2)"), ("#4a4a4a", "var(--line2)"), ("#1f1f1f", "var(--card3)"), ("#fafafa", "var(--ink)"), ("#d4d4d4", "var(--ink2)"),
            ("#363636", "var(--line2)"), ("#bdbdbd", "var(--ink2)"), ("#202020", "var(--card3)"), ("#1a1a1a", "var(--card)"), ("#4d4d4d", "var(--faint)")]

_fix_lines_before_r32 = JS_FIXES[LINES]


def fix_lines32(t):
    t = _fix_lines_before_r32(t)
    if "/* round 32 theme */" in t:
        print("(news) lines: theme colours: already done")
    else:
        i32 = t.find("const CSS = `")
        j32 = t.find("`;", i32)
        if i32 < 0 or j32 < 0:
            fail("lines: could not find the style block in lines-tab.js. Send this log to the AI helper.")
        css32 = t[i32:j32]
        for a32, b32 in LT32_MAP:
            css32 = css32.replace(a32, b32)
        css32 = css32.replace("const CSS = `", "const CSS = `\n/* round 32 theme */", 1)
        t = t[:i32] + css32 + t[j32:]
        for a32, b32 in (('"#8b7cff"', '"var(--accent)"'), ('"#5fd08a"', '"var(--good)"'), ('"#4d4d4d"', '"var(--faint)"')):
            t = t.replace(a32, b32)
        print("(news) lines: theme colours: updated")
    for must in ("window.PlayerPopup = PlayerPopup;", "function PlayerCard(", "H.TeamLogo t={x.t} size={32}"):
        if must not in t:
            fail("lines-tab.js looks damaged after round 32 (" + must + ").")
    babel_ok(t, LINES)
    return t


JS_FIXES[LINES] = fix_lines32

# ---------- round 33: home page panels. Next 7 days, around the league, who's carrying you, goalie board, playoff odds ----------
R33_CSS = r'''  /* round 33 home (news_logos.py) */
  .gx-row { display: flex; align-items: center; gap: 8px; padding: 8px 0; border-top: 1px solid var(--line); min-width: 0; }
  .gx-lg { display: grid; grid-template-columns: minmax(0,1fr) 40px 80px 40px minmax(0,1fr); gap: 8px; align-items: center; padding: 9px 0; border-top: 1px solid var(--line); font-variant-numeric: tabular-nums; }
  .gx-n7 { display: grid; grid-template-columns: repeat(7, minmax(0,1fr)); gap: 6px; text-align: center; margin-top: 10px; font-variant-numeric: tabular-nums; }
  .gx-n7 .bars { display: flex; align-items: flex-end; justify-content: center; gap: 4px; height: 44px; }
  .gx-n7 .bars i { width: 10px; display: block; min-height: 1px; }
'''

R33_HELPERS = r'''// ---------- round 33: home page panels (news_logos.py) ----------
const GxPanel = ({ title, right, children }) => (
  <div className="gx-pn" style={{ minWidth: 0 }}><b></b><b></b><b></b><b></b>
    <div style={{ display: "flex", alignItems: "baseline", marginBottom: 6 }}>
      <span className="gx-tag">{title}</span>
      {right ? <span className="text-xs text-slate-500" style={{ marginLeft: "auto" }}>{right}</span> : null}
    </div>
    {children}
  </div>
);
function GxNext7({ s }) {
  const K = s.blend, today = todayISO();
  const rows = useMemo(() => {
    const out = [];
    for (let i = 0; i < 7; i++) {
      const dt = addDays(today, i), wi = s.weeks.findIndex((w) => (w.dates || []).includes(dt));
      if (wi < 0) { out.push({ dt, a: 0, b: 0 }); continue; }
      const dw = deriveWeek(s.weeks[wi], s.autoDone), d = dw.dates.indexOf(dt), opp = oppOf(dw, s.me);
      const cnt = (tid) => (tid ? dayLineup(s.players.filter((p) => p.ft === tid), dw, d, K).start.length : 0);
      out.push({ dt, a: cnt(s.me), b: cnt(opp) });
    }
    return out;
  }, [s.players, s.weeks, K, today, window.__PMODE]);
  const ta = rows.reduce((x, r) => x + r.a, 0), tb = rows.reduce((x, r) => x + r.b, 0);
  const mx = Math.max(1, Math.max.apply(null, rows.map((r) => Math.max(r.a, r.b))));
  return (
    <GxPanel title="Next 7 days" right={"Lineup games \u00b7 you " + ta + ", them " + tb}>
      <div className="gx-n7">
        {rows.map((r, i) => (
          <div key={r.dt}>
            <div className="bars"><i style={{ height: (r.a / mx) * 44, background: "var(--accent)" }}></i><i style={{ height: (r.b / mx) * 44, background: "var(--faint)" }}></i></div>
            <div className="text-xs" style={{ marginTop: 4 }}>{r.a} <span className="text-slate-500">{r.b}</span></div>
            <div className="text-xs text-slate-500">{i === 0 ? "Today" : dayLabel(r.dt).split(",")[0]}</div>
          </div>
        ))}
      </div>
    </GxPanel>
  );
}
function GxLeague({ s, wk }) {
  const K = s.blend, gen = (window.ESPN_DATA || {}).generated;
  const rows = useMemo(() => (wk.pairs || []).filter((p) => p[0] && p[1] && p[0] !== s.me && p[1] !== s.me).map(([a, b]) => {
    const R = (id) => weekLive(s.players.filter((p) => p.ft === id), wk, K, id), act = (id) => +((wk.act || {})[id]) || 0;
    return { a, b, p: winProb(R(a), R(b), act(a), act(b)) };
  }), [s.players, wk, K, gen]);
  return (
    <GxPanel title="Around the league">
      {rows.length ? rows.map(({ a, b, p }, i) => {
        const close = Math.abs(p - 0.5) < 0.1, la = p >= 0.5;
        const bar = (win) => (close ? "var(--mute)" : win ? "var(--good)" : "var(--bad)");
        return (
          <div key={a + "-" + b} className="gx-lg" style={i ? null : { borderTop: 0 }}>
            <span className="truncate"><TL s={s} id={a} /></span>
            <span className="text-right" style={{ color: la || close ? "var(--ink)" : "var(--mute)" }}>{wpTxt(p)}</span>
            <span style={{ display: "flex", height: 4, gap: 2 }}><i style={{ display: "block", width: Math.round(p * 100) + "%", background: bar(la) }}></i><i style={{ display: "block", flex: 1, background: bar(!la) }}></i></span>
            <span style={{ color: !la || close ? "var(--ink)" : "var(--mute)" }}>{wpTxt(1 - p)}</span>
            <span className="truncate text-right"><TL s={s} id={b} /></span>
          </div>
        );
      }) : <div className="text-sm text-slate-500">No other matchups loaded for this week.</div>}
    </GxPanel>
  );
}
function GxCarry({ s, wk }) {
  const K = s.blend, gen = (window.ESPN_DATA || {}).generated;
  const data = useMemo(() => {
    const P = pby(), acc = {};
    (wk.dates || []).forEach((dt) => {
      const AD = actDay(s.me, dt);
      if (!AD) return;
      Object.entries(AD).forEach(([pid, v]) => {
        if (!v || v[0] == null || !ESLOT[v[1]]) return;
        const p = P["e" + pid];
        if (!p || !(SCHED[p.t] && SCHED[p.t].has(dt))) return;
        const st = gState(p.t, dt).s;
        if (st === "P" || (p.p === "G" && !v[0])) return;
        const a = (acc[p.id] = acc[p.id] || { p, pts: 0, g: 0, diff: 0 });
        a.pts += v[0]; a.g++;
        if (st === "F") a.diff += v[0] - effAvg(p, K, dt);
      });
    });
    const list = Object.values(acc), top = [...list].sort((x, y) => y.pts - x.pts).slice(0, 3);
    const low = list.filter((x) => top.indexOf(x) < 0).sort((x, y) => x.diff - y.diff)[0];
    return { top, low: low && low.diff <= -3 ? low : null };
  }, [s.players, wk, K, gen]);
  const row = (x, i, note) => (
    <div key={x.p.id} className="gx-row" style={i === 0 ? { borderTop: 0 } : note ? { borderTop: "1px dashed var(--line2)" } : null}>
      <span className="min-w-0 truncate" style={{ flex: 1 }}><PN p={x.p} className="" /></span>
      {note ? <span className="text-xs whitespace-nowrap" style={{ color: "var(--bad)" }}>{note}</span> : <span className="text-xs text-slate-500 whitespace-nowrap">{x.g} game{x.g === 1 ? "" : "s"}</span>}
      <span className="font-semibold text-right" style={{ minWidth: 40, fontVariantNumeric: "tabular-nums" }}>{f1(x.pts)}</span>
    </div>
  );
  return (
    <GxPanel title="Who's carrying you" right="This matchup, in your lineup">
      {data.top.length ? data.top.map((x, i) => row(x, i, null)) : <div className="text-sm text-slate-500">No games counted yet in this matchup.</div>}
      {data.low ? row(data.low, 9, Math.round(-data.low.diff) + " under projection") : null}
    </GxPanel>
  );
}
function GxGoalies({ s, wk }) {
  const today = todayISO();
  const rows = s.players.filter((p) => p.ft === s.me && p.p === "G" && !p.ir).map((p) => {
    const id = String(p.id).slice(1);
    let st = 0, pts = 0, left = 0;
    (wk.dates || []).forEach((dt, d) => {
      if (!(wk.games[p.t] || []).includes(d)) return;
      if (gState(p.t, dt).s !== "P") {
        const AD = actDay(s.me, dt), v = AD ? AD[id] : null;
        if (v && v[1] === 5 && v[0]) { st++; pts += v[0]; }
      } else if (dt >= today && avail(p, dt) > 0 && gStart(p, dt).v >= 0.5) left++;
    });
    return { p, st, pts, left };
  });
  return (
    <GxPanel title="Goalie board" right={"starts \u00b7 left \u00b7 points"}>
      {rows.length ? rows.map((x, i) => (
        <div key={x.p.id} className="gx-row" style={i ? null : { borderTop: 0 }}>
          <span className="min-w-0 truncate" style={{ flex: 1 }}><PN p={x.p} className="" /></span>
          <span className="text-xs text-slate-500 whitespace-nowrap">{x.st + " \u00b7 " + x.left}</span>
          <span className="font-semibold text-right" style={{ minWidth: 40, fontVariantNumeric: "tabular-nums", color: x.pts > 5 ? "var(--good)" : x.pts < 0 ? "var(--bad)" : "var(--ink)" }}>{f1(x.pts)}</span>
        </div>
      )) : <div className="text-sm text-slate-500">No goalies on your roster.</div>}
    </GxPanel>
  );
}
// chance of a top-6 finish: 2,000 simulated seasons from each team's strength and the real schedule
function playoffSim(s) {
  const ids = s.teams.map((t) => t.id);
  if (ids.length < 2 || ids.indexOf(s.me) < 0) return null;
  const T = leagueTable(s), str = {}, K = s.blend, today = todayISO();
  T.rows.forEach((x) => (str[x.t.id] = x.strength));
  const end = Math.min(s.weeks.length, s.poStart ?? 24), w0 = {}, pf = {}, todo = [];
  ids.forEach((id) => { w0[id] = 0; pf[id] = 0; });
  s.weeks.slice(0, end).forEach((w) => {
    const len = (w.dates || []).length, pairs = (w.pairs || []).filter((p) => p[0] && p[1] && w0[p[0]] != null && w0[p[1]] != null);
    if (!len || !pairs.length) return;
    if (effDone(w, s.autoDone) >= len) {
      pairs.forEach(([a, b]) => {
        const x = +((w.act || {})[a]) || 0, y = +((w.act || {})[b]) || 0;
        if (!x && !y) return;
        pf[a] += x; pf[b] += y;
        if (x > y) w0[a]++; else if (y > x) w0[b]++; else { w0[a] += 0.5; w0[b] += 0.5; }
      });
      return;
    }
    const live = w.dates[0] <= today ? deriveWeek(w, s.autoDone) : null;
    pairs.forEach(([a, b]) => {
      let p;
      if (live) {
        const R = (id) => weekLive(s.players.filter((q) => q.ft === id), live, K, id), act = (id) => +((live.act || {})[id]) || 0;
        p = winProb(R(a), R(b), act(a), act(b));
      } else p = normCdf((((str[a] || 0) - (str[b] || 0)) * (len / 7)) / (80 * Math.sqrt(len / 7)));
      pf[a] += (str[a] || 0) * (len / 7); pf[b] += (str[b] || 0) * (len / 7);
      todo.push([a, b, Math.max(0.02, Math.min(0.98, p))]);
    });
  });
  let seed = 20262027;
  const rnd = () => { seed = (seed + 0x6d2b79f5) | 0; let t = Math.imul(seed ^ (seed >>> 15), 1 | seed); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
  const N = 2000, cut = Math.min(6, ids.length - 1);
  let inN = 0, sum = 0;
  for (let k = 0; k < N; k++) {
    const w = Object.assign({}, w0);
    for (let j = 0; j < todo.length; j++) { const m = todo[j]; if (rnd() < m[2]) w[m[0]]++; else w[m[1]]++; }
    const r = ids.slice().sort((a, b) => w[b] - w[a] || pf[b] - pf[a]).indexOf(s.me) + 1;
    if (r <= cut) inN++;
    sum += r;
  }
  return { odds: inN / N, finish: Math.round(sum / N), cut };
}
function GxPlayoff({ s }) {
  const [res, setRes] = useState(null);
  useEffect(() => {
    const id = setTimeout(() => { try { setRes(playoffSim(s)); } catch (e) { setRes(null); } }, 500);
    return () => clearTimeout(id);
  }, [s.players, s.weeks, s.wk, s.blend, window.__PMODE]);
  useEffect(() => { if (res) uiSet("po:" + s.wk, res.odds); }, [res ? res.odds : null, s.wk]);
  const prev = uiGet()["po:" + (s.wk - 1)];
  const d = res && prev != null ? Math.round(res.odds * 100) - Math.round(prev * 100) : null;
  return (
    <div className="gx-pn"><b></b><b></b><b></b><b></b>
      <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
        <GxRing v={res ? res.odds : null} />
        <div className="min-w-0" style={{ flex: 1 }}>
          <div className="gx-tag">Playoff odds</div>
          <div style={{ marginTop: 6 }}>{res ? "Projected to finish " + ordN(res.finish) : "Working it out..."} <span className="text-slate-500">{"\u00b7 top " + (res ? res.cut : 6) + " make it"}</span></div>
        </div>
        {d != null ? (
          <div className="text-right whitespace-nowrap">
            <div className="text-xs text-slate-500">since last week</div>
            <div style={{ color: d > 0 ? "var(--good)" : d < 0 ? "var(--bad)" : "var(--mute)" }}>{(d > 0 ? "+" : "") + d + "%"}</div>
          </div>
        ) : null}
      </div>
    </div>
  );
}
function GxHome({ s, wk }) {
  return (
    <>
      <div className="grid md:grid-cols-2 gap-3">
        <GxNext7 s={s} />
        <GxLeague s={s} wk={wk} />
        <GxCarry s={s} wk={wk} />
        <GxGoalies s={s} wk={wk} />
      </div>
      <GxPlayoff s={s} />
    </>
  );
}

'''

R33_END_OLD = "No move worth making right now.</div>}"
R33_END_PAT = re.escape(R33_END_OLD) + r"\s*</div>\s*</div>\s*</div>"
R33_END_NEW = R33_END_OLD + "\n          </div>\n        </div>\n      </div>\n      <GxHome s={s} wk={wk} />"


def round33(t):
    t = lit(t, "home: styles", "</style>", R33_CSS + "</style>", "round 33 home")
    t = sub_once(t, "home: five new panels on Today", R33_END_PAT, R33_END_NEW, "<GxHome s={s}")
    t = lit(t, "home: helpers", ROOT, R33_HELPERS + ROOT, "function GxHome(")
    for must in ("function GxHome(", "function playoffSim(", "function GxWeek(", "today v32", "<GxHome s={s}", "const uiGet =", "function TopBar("):
        if must not in t:
            fail("fantasy-gm.html looks damaged after round 33 (" + must + ").")
    return t


_fix_before_r33 = fix


def fix(t):
    return round33(_fix_before_r33(t))

# ---------- round 34: home page tweaks. Games this matchup, full-width league, red and green everywhere, cleaner week chart ----------
R34_CSS = r'''  /* round 34 home tweaks (news_logos.py) */
  .gx-lg { grid-template-columns: minmax(0,1fr) 44px minmax(80px, 2fr) 44px minmax(0,1fr); }
  .gx-gm .bars { height: 64px; gap: 5px; }
  .gx-gm .bars i { width: 14px; }
'''

R34_WEEK = r'''function GxWeek({ wk, A, B, aA, aB }) {
  // week chart v34: drawn at real size so text stays readable, cleaner projection line (news_logos.py)
  const [W, setW] = useState(620);
  const box = React.useRef(null);
  useEffect(() => {
    const el = box.current;
    if (!el) return;
    const fit = () => setW(Math.max(300, Math.round(el.clientWidth)));
    fit();
    if (window.ResizeObserver) { const ro = new ResizeObserver(fit); ro.observe(el); return () => ro.disconnect(); }
    window.addEventListener("resize", fit);
    return () => window.removeEventListener("resize", fit);
  }, []);
  const dates = wk.dates || [], n = dates.length, today = todayISO();
  if (!n) return <div ref={box}></div>;
  let run = (aA - aB) - (A.act - B.act);
  const rows = dates.map((dt, d) => { const x = A.days[d], y = B.days[d], dv = x.act + x.total - (y.act + y.total); run += dv; return { dt, dv, run, st: dt < today ? "f" : dt === today ? "t" : "p" }; });
  const grid = Math.max(10, Math.ceil(rows.reduce((mx, r) => Math.max(mx, Math.abs(r.dv)), 0) / 10) * 10), sc = 46 / grid;
  const L = 34, R = W - 16, colW = (R - L) / n, cx = (i) => L + colW * (i + 0.5), bw = Math.min(40, colW * 0.36);
  const lo = Math.min.apply(null, rows.map((r) => r.run)), hi = Math.max.apply(null, rows.map((r) => r.run));
  const ry = (v) => (hi === lo ? 167 : 178 - ((v - lo) / (hi - lo)) * 22);
  const ci = rows.findIndex((r) => r.st !== "f"), last = ci < 0 ? n - 1 : ci - 1;
  const pts = (a, b) => rows.slice(a, b + 1).map((r, i) => cx(a + i).toFixed(1) + "," + ry(r.run).toFixed(1)).join(" ");
  const sg = (v) => (v > 0 ? "+" : "") + Math.round(v);
  const col = (v) => (v >= 0 ? "var(--good)" : "var(--bad)");
  const tx = (size, fill, weight) => ({ fontSize: size, fill, fontWeight: weight || 400 });
  const nowLeft = last >= n - 3;
  return (
    <div ref={box} style={{ overflow: "hidden" }}>
      <svg viewBox={"0 0 " + W + " 196"} width={W} height={196} className="gx-svg" style={{ display: "block", marginTop: 6 }} role="img" aria-label="Margin each day this week and the running total">
        {rows.map((r, i) => (r.st === "t" ? <rect key={"h" + i} x={cx(i) - colW / 2 + 2} y={4} width={colW - 4} height={136} style={{ fill: "var(--accentSoft)" }} /> : null))}
        <line x1={L} y1={36} x2={R} y2={36} style={{ stroke: "var(--line)", strokeDasharray: "2 4" }} />
        <line x1={L} y1={82} x2={R} y2={82} style={{ stroke: "var(--faint)" }} />
        <line x1={L} y1={128} x2={R} y2={128} style={{ stroke: "var(--line)", strokeDasharray: "2 4" }} />
        <text x={26} y={40} textAnchor="end" style={tx(11, "var(--faint)")}>{"+" + grid}</text>
        <text x={26} y={86} textAnchor="end" style={tx(11, "var(--faint)")}>0</text>
        <text x={26} y={132} textAnchor="end" style={tx(11, "var(--faint)")}>{"-" + grid}</text>
        {rows.map((r, i) => {
          const h = Math.max(1, Math.abs(r.dv) * sc), up = r.dv >= 0, y = up ? 81 - h : 83, flat = Math.abs(r.dv) < 0.05;
          return (
            <g key={r.dt}>
              <text x={cx(i)} y={18} textAnchor="middle" style={tx(12, r.st === "t" ? "var(--accent)" : "var(--mute)", r.st === "t" ? 600 : 400)}>{r.st === "t" ? "Today" : dayLabel(r.dt).split(",")[0]}</text>
              {flat ? null : r.st === "p"
                ? <rect x={cx(i) - bw / 2 + 0.5} y={y + 0.5} width={bw - 1} height={Math.max(1, h - 1)} style={{ fill: "none", stroke: col(r.dv), strokeWidth: 1, strokeDasharray: "3 3" }} />
                : <rect x={cx(i) - bw / 2} y={y} width={bw} height={h} style={{ fill: col(r.dv) }} />}
              <text x={cx(i)} y={up && !flat ? 98 : 76} textAnchor="middle" style={tx(12, flat ? "var(--faint)" : col(r.dv))}>{flat ? "0" : sg(r.dv)}</text>
            </g>
          );
        })}
        <line x1={L} y1={152} x2={R} y2={152} style={{ stroke: "var(--line)" }} />
        {last < n - 1 ? <polyline points={pts(Math.max(last, 0), n - 1)} style={{ fill: "none", stroke: "var(--accent)", strokeWidth: 1, opacity: 0.35 }} /> : null}
        {last >= 1 ? <polyline points={pts(0, last)} style={{ fill: "none", stroke: "var(--accent)", strokeWidth: 1.5 }} /> : null}
        {rows.map((r, i) => (i > last ? <circle key={"p" + i} cx={cx(i)} cy={ry(r.run)} r={2.5} style={{ fill: "var(--card)", stroke: "var(--accent)", strokeWidth: 1, opacity: 0.55 }} /> : null))}
        {rows.map((r, i) => (i <= last ? <circle key={"c" + i} cx={cx(i)} cy={ry(r.run)} r={i === last ? 3.5 : 2.5} style={i === last ? { fill: "var(--card)", stroke: "var(--accent)", strokeWidth: 1.5 } : { fill: "var(--accent)" }} /> : null))}
        {last >= 0 && ci >= 0 ? <text x={cx(last) + (nowLeft ? -8 : 8)} y={192} textAnchor={nowLeft ? "end" : "start"} style={tx(11, "var(--accent)")}>{sg(aA - aB) + " now"}</text> : null}
        <text x={R} y={192} textAnchor="end" style={tx(11, "var(--mute)")}>{sg(rows[n - 1].run) + (ci < 0 ? " final" : " projected")}</text>
      </svg>
    </div>
  );
}

'''

R34_HOME = r'''function GxHome({ s, wk, A, B }) {
  // home v34: games this matchup and the league are full width (news_logos.py)
  return (
    <>
      <GxGames wk={wk} A={A} B={B} />
      <GxLeague s={s} wk={wk} />
      <div className="grid md:grid-cols-2 gap-3">
        <GxCarry s={s} wk={wk} />
        <GxGoalies s={s} wk={wk} />
      </div>
      <GxPlayoff s={s} />
    </>
  );
}

'''

R34_HELPERS = r'''// ---------- round 34: lineup games for each day of this matchup (news_logos.py) ----------
function GxGames({ wk, A, B }) {
  const dates = wk.dates || [], today = todayISO();
  if (!dates.length || !A || !B) return null;
  const rows = dates.map((dt, d) => ({ dt, a: ((A.days[d] || {}).start || []).length, b: ((B.days[d] || {}).start || []).length }));
  const tot = (k, from) => rows.reduce((x, r) => x + (r.dt >= from ? r[k] : 0), 0);
  const mx = Math.max(1, Math.max.apply(null, rows.map((r) => Math.max(r.a, r.b))));
  const open = dates[dates.length - 1] >= today;
  return (
    <GxPanel title="Games this matchup" right={"Lineup games \u00b7 you " + tot("a", "") + ", them " + tot("b", "") + (open ? " \u00b7 from today " + tot("a", today) + " and " + tot("b", today) : "")}>
      <div className="gx-n7 gx-gm" style={{ gridTemplateColumns: "repeat(" + rows.length + ", minmax(0,1fr))" }}>
        {rows.map((r) => {
          const on = r.dt === today, past = r.dt < today;
          return (
            <div key={r.dt} style={{ padding: "6px 0", borderRadius: 6, background: on ? "var(--accentSoft)" : "transparent" }}>
              <div className="bars"><i style={{ height: (r.a / mx) * 64, background: "var(--accent)", opacity: past ? 0.45 : 1 }}></i><i style={{ height: (r.b / mx) * 64, background: "var(--faint)", opacity: past ? 0.45 : 1 }}></i></div>
              <div className="text-sm" style={{ marginTop: 4 }}>{r.a} <span className="text-slate-500">{r.b}</span></div>
              <div className={"text-xs " + (on ? "font-semibold" : "text-slate-500")}>{on ? "Today" : dayLabel(r.dt).split(",")[0]}</div>
            </div>
          );
        })}
      </div>
    </GxPanel>
  );
}

'''


def round34(t):
    t = lit(t, "home 2: styles", "</style>", R34_CSS + "</style>", "round 34 home tweaks")
    t = block(t, "home 2: cleaner week chart", "function GxWeek({ wk, A, B, aA, aB }) {", "// ---------- round 33: home page panels", R34_WEEK, "week chart v34")
    t = lit(t, "home 2: red and green on every matchup", 'const bar = (win) => (close ? "var(--mute)" : win ? "var(--good)" : "var(--bad)");',
            'const bar = (win) => (win ? "var(--good)" : "var(--bad)");', 'const bar = (win) => (win ? "var(--good)" : "var(--bad)");')
    t = block(t, "home 2: full-width panels", "function GxHome({ s, wk }) {", ROOT, R34_HOME, "home v34")
    t = lit(t, "home 2: Today passes both lineups", "<GxHome s={s} wk={wk} />", "<GxHome s={s} wk={wk} A={A} B={B} />", "<GxHome s={s} wk={wk} A={A} B={B} />")
    t = lit(t, "home 2: games this matchup", ROOT, R34_HELPERS + ROOT, "function GxGames(")
    for must in ("function GxGames(", "function GxHome(", "function GxWeek(", "function GxLeague(", "<GxHome s={s}", "today v32", "function playoffSim("):
        if must not in t:
            fail("fantasy-gm.html looks damaged after round 34 (" + must + ").")
    return t


_fix_before_r34 = fix


def fix(t):
    return round34(_fix_before_r34(t))

# ---------- round 35: half dial for win chance everywhere, new Matchup page with swipe between matchups ----------
R35_CSS = r'''  /* round 35 matchup (news_logos.py) */
  .gx-day { border: 1px solid var(--line); border-radius: 8px; padding: 7px 2px; text-align: center; background: var(--card); font-variant-numeric: tabular-nums; }
  .gx-day.on { border-color: var(--accent); box-shadow: inset 0 0 0 0.5px var(--accent); }
  .gx-h2h { display: grid; grid-template-columns: minmax(0,1fr) 48px 28px 48px minmax(0,1fr); align-items: center; gap: 6px; padding: 9px 0; border-top: 1px solid var(--line); font-variant-numeric: tabular-nums; }
  .gx-arw { width: 28px; height: 28px; border-radius: 999px; border: 1px solid var(--line2); color: var(--mute); font-size: 18px; line-height: 1; flex-shrink: 0; }
  .gx-arw:hover { color: var(--ink); border-color: var(--accent); }
'''

R35_DIAL = r'''const GxRing = ({ v, big }) => {
  // dial v35: half dial with a needle in place of the ring (news_logos.py)
  const w = big ? 104 : 88, p = v == null ? 0 : Math.max(0.01, Math.min(0.99, v));
  const col = v == null ? "var(--faint)" : v >= 0.5 ? "var(--good)" : "var(--bad)";
  const th = Math.PI * (1 - p), nx = 50 + 33 * Math.cos(th), ny = 50 - 33 * Math.sin(th);
  return (
    <svg viewBox="0 0 100 68" width={w} height={Math.round(w * 0.68)} className="gx-svg" style={{ display: "block", flexShrink: 0 }} role="img" aria-label={v == null ? "Win chance not available" : wpTxt(v) + " chance to win"}>
      <path d="M10 50 A40 40 0 0 1 90 50" style={{ fill: "none", stroke: "var(--track)", strokeWidth: 7 }} />
      {v == null ? null : <path d="M10 50 A40 40 0 0 1 90 50" style={{ fill: "none", stroke: col, strokeWidth: 7, strokeDasharray: (p * 125.66).toFixed(1) + " 200" }} />}
      {v == null ? null : <line x1={50} y1={50} x2={nx.toFixed(1)} y2={ny.toFixed(1)} style={{ stroke: "var(--ink)", strokeWidth: 2 }} />}
      <circle cx={50} cy={50} r={3.5} style={{ fill: "var(--ink)" }} />
      <text x={50} y={66} textAnchor="middle" style={{ fontSize: 14, fontWeight: 600, fill: col }}>{v == null ? "\u2013" : wpTxt(v) + (big ? " to win" : "")}</text>
    </svg>
  );
};
'''

# done markers of older rounds that lived inside the old Matchup page; kept as comments so those rounds stay "already done"
R35_KEEP = [
    "Day difference", 'data-v="daydiff2"', "day header: running total removed", 'label={"Win chance \u00b7 "', 'data-w="daydiff3"',
    "<H2H x={x}", '<LiveTag st={tag === "LIVE" ? "L" : "F"} />', "round 28: actual-score row removed", "const openDay =",
    "<DayFold key=", "</DayFold>",
]

R35_MATCHUP_BODY = r'''  const K = s.blend, done = wk.done || 0;
  const pairOpp = oppOf(wk, s.me);
  const myPair = [s.me, pairOpp || s.opp];
  const others = (wk.pairs || []).filter((p) => p[0] && p[1] && p[0] !== s.me && p[1] !== s.me);
  const all = [myPair, ...others];
  const [sel, setSel] = useState(0);
  const [day, setDay] = useState(null);
  const touch = React.useRef(null);
  const [a, b] = all[Math.min(sel, all.length - 1)];
  const gen = (window.ESPN_DATA || {}).generated;
  const P = useMemo(() => {
    const o = {};
    [a, b].forEach((id) => { o[id] = { r: weekLive(s.players.filter((p) => p.ft === id), wk, K, id, { detail: true }), act: +((wk.act || {})[id]) || 0 }; });
    return o;
  }, [s.players, wk, K, done, a, b, gen]);
  const A = P[a].r, B = P[b].r, aA = P[a].act, aB = P[b].act;
  const fa = aA + A.total, fb = aB + B.total, margin = fa - fb;
  const dates = wk.dates || [], n = dates.length, today = todayISO();
  const first = dates.findIndex((x) => x >= today);
  const d = Math.max(0, Math.min(n - 1, day != null ? day : first >= 0 ? first : n - 1));
  const over = n > 0 && done >= n;
  const move = (k) => setSel((Math.min(sel, all.length - 1) + k + all.length) % all.length);
  const onStart = (e) => { const t = e.touches[0]; touch.current = [t.clientX, t.clientY]; };
  const onEnd = (e) => {
    const t0 = touch.current, t = e.changedTouches[0];
    touch.current = null;
    if (!t0 || all.length < 2) return;
    const dx = t.clientX - t0[0], dy = t.clientY - t0[1];
    if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy) * 1.5) move(dx < 0 ? 1 : -1);
  };
  const x = A.days[d] || { start: [], bench: [], act: 0, total: 0 }, y = B.days[d] || { start: [], bench: [], act: 0, total: 0 };
  const dvOf = (i) => { const p = A.days[i], q = B.days[i]; return p && q ? p.act + p.total - (q.act + q.total) : 0; };
  const state = x.locked || y.locked ? (x.allDone && y.allDone ? "final" : "live") : dates[d] < today ? "final" : "projected";
  const rows = [];
  ["F", "D", "UTIL", "G"].forEach((sl) => {
    const L = x.start.filter((p) => p.slot === sl), R = y.start.filter((p) => p.slot === sl);
    for (let i = 0; i < Math.max(L.length, R.length); i++) rows.push([sl, L[i] || null, R[i] || null]);
  });
  const val = (p) => (!p ? null : p.st ? (p.a == null ? 0 : p.a) : p.x);
  const cell = (p, right) => {
    if (!p) return <div className={"text-sm text-slate-500" + (right ? " text-right" : "")}>empty</div>;
    const st = p.p === "G" && !p.st ? mStart(p.gs) : "", line = p.st ? statLine(pStat(p, p.dt)) : "";
    return (
      <div className={"min-w-0" + (right ? " text-right" : "")}>
        <div className="truncate"><PN p={p} className="" /></div>
        <div className="text-xs text-slate-500 truncate">{p.st ? <><LiveTag st={p.st} t={p.t} dt={p.dt} />{line ? " " + line : ""}</> : <>{mGame(p)}{st ? " \u00b7 " + st.toLowerCase() : ""}</>}</div>
      </div>
    );
  };
  const num = (p, q, right) => {
    const v = val(p), o = val(q);
    if (v == null) return <div className={"text-slate-500" + (right ? "" : " text-right")}>{"\u2013"}</div>;
    const win = o == null || v - o >= 0.05;
    return <div className={right ? "" : "text-right"} style={win ? { color: "var(--good)", fontWeight: 600 } : null}>{p.st && p.a == null ? "\u2013" : f1(v)}</div>;
  };
  const sit = (l, id) => (l.bench && l.bench.length ? <div className="text-xs text-slate-500" style={{ marginTop: 6 }}>{teamName(s, id)} would sit: {l.bench.map((p) => shortN(p.n)).join(", ")}</div> : null);
  const dayTot = x.act + x.total - (y.act + y.total);
  const mine = a === s.me;
  return (
    <div>
      <div onTouchStart={onStart} onTouchEnd={onEnd} style={{ touchAction: "pan-y" }}>
        <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
          {all.length > 1 ? <button type="button" className="m-hide gx-arw" aria-label="Previous matchup" onClick={() => move(-1)}>{"\u2039"}</button> : null}
          <div className="min-w-0" style={{ flex: 1 }}>
            <div className="text-sm font-semibold truncate" style={mine ? { color: "var(--accent)" } : null}><TL s={s} id={a} /></div>
            <div className="gx-num" style={{ fontSize: 28 }}>{f1(aA)}</div>
          </div>
          <GxRing v={winProb(A, B, aA, aB)} />
          <div className="min-w-0 text-right" style={{ flex: 1 }}>
            <div className="text-sm text-slate-500 truncate"><TL s={s} id={b} /></div>
            <div className="gx-num" style={{ fontSize: 28, color: "var(--ink2)" }}>{f1(aB)}</div>
          </div>
          {all.length > 1 ? <button type="button" className="m-hide gx-arw" aria-label="Next matchup" onClick={() => move(1)}>{"\u203a"}</button> : null}
        </div>
        {all.length > 1 ? (
          <div style={{ display: "flex", justifyContent: "center", gap: 6, marginTop: 8 }}>
            {all.map((pr, i) => <button key={i} type="button" aria-label={"Matchup " + (i + 1)} onClick={() => setSel(i)} style={{ width: 6, height: 6, borderRadius: 99, background: i === Math.min(sel, all.length - 1) ? "var(--accent)" : "var(--line2)" }}></button>)}
          </div>
        ) : null}
        <div className="text-xs text-slate-500" style={{ display: "flex", marginTop: 8 }}>
          <span>{(over ? "Final " : "Projected ") + Math.round(fa)}</span>
          <span style={{ margin: "0 auto", color: margin >= 0 ? "var(--good)" : "var(--bad)" }}>{mine ? (margin >= 0 ? "Ahead by " : "Behind by ") + f1(Math.abs(margin)) : teamName(s, margin >= 0 ? a : b) + " ahead by " + f1(Math.abs(margin))}</span>
          <span>{Math.round(fb)}</span>
        </div>
      </div>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(" + Math.max(1, n) + ", minmax(0,1fr))", gap: 6, marginTop: 14 }}>
        {dates.map((dt, i) => {
          const dv = dvOf(i), flat = Math.abs(dv) < 0.05;
          return (
            <button key={dt} type="button" onClick={() => setDay(i)} className={"gx-day" + (i === d ? " on" : "")}>
              <span className={"block text-xs " + (i === d ? "font-semibold" : "text-slate-500")}>{dt === today ? "Today" : dayLabel(dt).split(",")[0]}</span>
              <span className="block text-sm" style={{ color: flat ? "var(--faint)" : dv > 0 ? "var(--good)" : "var(--bad)" }}>{flat ? "0" : (dv > 0 ? "+" : "") + Math.round(dv)}</span>
            </button>
          );
        })}
      </div>
      <div className="gx-pn" style={{ marginTop: 12 }}><b></b><b></b><b></b><b></b>
        <div style={{ display: "flex", alignItems: "baseline", marginBottom: 6 }}>
          <span className="gx-tag">{(dates[d] === today ? "Today" : dates[d] ? dayLabel(dates[d]) : "") + " \u00b7 " + state}</span>
          <span style={{ marginLeft: "auto", fontVariantNumeric: "tabular-nums" }}>
            <span className="font-semibold">{f1(x.act + x.total)}</span> <span className="text-slate-500">to {f1(y.act + y.total)}</span>
            <span style={{ marginLeft: 8, color: dayTot >= 0 ? "var(--good)" : "var(--bad)" }}>{(dayTot >= 0 ? "+" : "") + f1(dayTot)}</span>
          </span>
        </div>
        {rows.length ? rows.map(([sl, p, q], i) => (
          <div key={i} className="gx-h2h" style={i ? null : { borderTop: 0 }}>
            {cell(p, false)}{num(p, q, false)}
            <div className="text-xs text-center" style={{ color: "var(--faint)" }}>{sl === "UTIL" ? "U" : sl}</div>
            {num(q, p, true)}{cell(q, true)}
          </div>
        )) : <div className="text-sm text-slate-500">No games for either team on this day.</div>}
        {sit(x, a)}{sit(y, b)}
      </div>
      <div className="text-xs text-slate-500" style={{ display: "flex", marginTop: 10 }}>
        <span>{gamesMoves(s, a, wk, A)}</span><span style={{ marginLeft: "auto" }}>{gamesMoves(s, b, wk, B)}</span>
      </div>
    </div>
  );
}

'''

R35_MATCHUP = ("function Matchup({ s, setS, wk, setWk }) {\n"
               "  // matchup v35: one day at a time, head to head, swipe or arrows between matchups (news_logos.py)\n"
               "  // matchup v16: older marker kept, with these done markers from earlier rounds:\n"
               + "".join("  // " + m35 + "\n" for m35 in R35_KEEP) + R35_MATCHUP_BODY)


def round35(t):
    t = lit(t, "matchup: styles", "</style>", R35_CSS + "</style>", "round 35 matchup")
    t = block(t, "matchup: half dial for win chance", "const GxRing = ({ v, big }) => {", "function GxWeek(", R35_DIAL, "dial v35")
    t = block(t, "matchup: new page with swipe", "function Matchup({ s, setS, wk, setWk }) {", "// ---------- Power rankings ----------", R35_MATCHUP, "matchup v35")
    for must in R35_KEEP + ["function Matchup(", "// matchup v16:", "gamesMoves(s, a, wk, A)", "gamesMoves(s, b, wk, B)", "function Side(", "function H2H(",
                            "function GxWeek(", "const GxRing =", "<GxHome s={s}", "<FillSlot", "Projected today"]:
        if must not in t:
            fail("fantasy-gm.html looks damaged after round 35 (" + must + ").")
    return t


_fix_before_r35 = fix


def fix(t):
    return round35(_fix_before_r35(t))

# ---------- round 36: ring back in place of the half dial, team logos on the Matchup rows ----------
R36_RING = r'''const GxRing = ({ v, big }) => {
  // ring v36: the circle is back (older marker kept: dial v35) (news_logos.py)
  const size = big ? 104 : 64, m = size / 2, r = big ? 36 : 26, w = big ? 6 : 5, c = 2 * Math.PI * r;
  const p = v == null ? 0 : Math.max(0.01, Math.min(0.99, v));
  const col = v == null ? "var(--faint)" : v >= 0.5 ? "var(--good)" : "var(--bad)";
  return (
    <svg viewBox={"0 0 " + size + " " + size} width={size} height={size} className="gx-svg" style={{ flexShrink: 0, display: "block" }} role="img" aria-label={v == null ? "Win chance not available" : wpTxt(v) + " chance to win"}>
      {big ? <circle cx={m} cy={m} r={44} style={{ fill: "none", stroke: "var(--track)", strokeWidth: 1, strokeDasharray: "1 5.9" }} /> : null}
      <circle cx={m} cy={m} r={r} style={{ fill: "none", stroke: "var(--track)", strokeWidth: w }} />
      {v == null ? null : <circle cx={m} cy={m} r={r} transform={"rotate(-90 " + m + " " + m + ")"} style={{ fill: "none", stroke: col, strokeWidth: w, strokeDasharray: (p * c).toFixed(1) + " " + c.toFixed(1) }} />}
      <text x={m} y={big ? m + 3 : m + 5} textAnchor="middle" style={{ fontSize: big ? 21 : 15, fontWeight: 600, fill: big ? col : "var(--ink)" }}>{v == null ? "\u2013" : wpTxt(v)}</text>
      {big ? <text x={m} y={m + 18} textAnchor="middle" style={{ fontSize: 11, fill: "var(--mute)" }}>to win</text> : null}
    </svg>
  );
};
'''

R36_CELL_OLD = r'''<div className={"min-w-0" + (right ? " text-right" : "")}>'''
R36_CELL_NEW = (r'''<div className="min-w-0" style={{ display: "flex", alignItems: "center", gap: 10, flexDirection: right ? "row-reverse" : "row" }}>'''
                r'''<TeamLogo t={p.t} size={30} /><div className={"min-w-0" + (right ? " text-right" : "")} style={{ flex: 1 }}>''')
R36_END_OLD = r'''st.toLowerCase() : ""}</>}</div>'''
R36_END_NEW = r'''st.toLowerCase() : ""}</>}</div></div>'''


def round36(t):
    t = block(t, "matchup 2: ring instead of the dial", "const GxRing = ({ v, big }) => {", "function GxWeek(", R36_RING, "ring v36")
    t = lit(t, "matchup 2: team logo beside each player", R36_CELL_OLD, R36_CELL_NEW,
            '<TeamLogo t={p.t} size={30} /><div className={"min-w-0" + (right ? " text-right" : "")} style={{ flex: 1 }}>')
    t = lit(t, "matchup 2: close the logo row", R36_END_OLD, R36_END_NEW, 'st.toLowerCase() : ""}</>}</div></div>')
    for must in ("ring v36", "dial v35", "matchup v35", "function Matchup(", "function GxWeek(", "const GxRing ="):
        if must not in t:
            fail("fantasy-gm.html looks damaged after round 36 (" + must + ").")
    return t


_fix_before_r36 = fix


def fix(t):
    return round36(_fix_before_r36(t))

# ---------- round 37: Moves folds into Team (Roster, Pickups, Plan, Trades, Lines) and a new Roster page ----------
R37_CSS = r'''  /* round 37 team (news_logos.py) */
  .gx-ro { display: grid; grid-template-columns: 28px minmax(0,1fr) 62px 60px 40px 54px 96px 62px 64px; gap: 8px; align-items: center; padding: 8px 0; border-top: 1px solid var(--line); font-variant-numeric: tabular-nums; }
  .gx-ro .n { text-align: right; }
  .gx-roh { font-size: 12px; color: var(--mute); border-top: 0; padding: 0 0 6px; }
  .gx-roh button { color: var(--mute); }
  .gx-roh button.on { color: var(--ink); font-weight: 600; text-decoration: underline; text-underline-offset: 3px; }
  .gx-sp { display: flex; align-items: flex-end; justify-content: flex-end; gap: 2px; height: 22px; }
  .gx-sp i { width: 7px; display: block; }
  @media (max-width: 640px) { .gx-ro { grid-template-columns: 26px minmax(0,1fr) 54px 34px 50px; gap: 6px; } }
'''

R37_MYTEAM = r'''function MyTeam({ s, setS, wk, go }) {
  // team roster v37: one roster list with role, form, schedule and rank (news_logos.py)
  const K = s.blend, today = todayISO(), gen = (window.ESPN_DATA || {}).generated;
  const [sort, setSort] = useState("pg");
  const [hist, setHist] = useState({});
  const roster = s.players.filter((p) => p.ft === s.me);
  const pv = (p) => effAvg(p, K) * (p.p === "G" ? p.prob : 1);
  const T = leagueTable(s), ri = T.rows.findIndex((r) => r.t.id === s.me), meRow = ri >= 0 ? T.rows[ri] : null, g = T.grpRank[s.me] || {};
  const dates = wk.dates || [], done = wk.done || 0;
  const nextW = s.weeks[s.wk + 1] ? deriveWeek(s.weeks[s.wk + 1], s.autoDone) : null;
  const mu = useMemo(() => {
    const P = pby(), o = {};
    dates.forEach((dt) => {
      const AD = actDay(s.me, dt);
      if (!AD) return;
      Object.entries(AD).forEach(([pid, v]) => {
        if (!v || v[0] == null || !ESLOT[v[1]]) return;
        const p = P["e" + pid];
        if (!p || !(SCHED[p.t] && SCHED[p.t].has(dt)) || gState(p.t, dt).s === "P" || (p.p === "G" && !v[0])) return;
        o[p.id] = (o[p.id] || 0) + v[0];
      });
    });
    return o;
  }, [s.players, wk, gen]);
  const total = Object.values(mu).reduce((a, v) => a + Math.max(0, v), 0);
  const rankOf = useMemo(() => {
    const o = {};
    ["F", "D", "G"].forEach((k) => {
      s.players.filter((p) => p.p === k && p.prob > 0 && (p.proj !== false || p.gp > 0)).map((p) => [p.id, pv(p)]).sort((a, b) => b[1] - a[1]).forEach((x, i) => (o[x[0]] = i + 1));
    });
    return o;
  }, [s.players, K, window.__PMODE]);
  const roles = useMemo(() => {
    const L = window.LINES_DATA, o = {};
    if (!L || !L.teams) return o;
    const key = (x) => nrm(x).replace(/[.'\u2019]/g, "").replace(/-/g, " ").replace(/\s+/g, " ").trim();
    roster.forEach((p) => {
      const ln = (L.teams[p.t] || {}).lines;
      if (!ln) return;
      const k = key(p.n), has = (sl) => (ln[sl] || []).some((x) => key(x) === k);
      o[p.id] = { es: ["F1", "F2", "F3", "F4", "D1", "D2", "D3", "G"].find(has), pp: ["PP1", "PP2"].find(has) };
    });
    return o;
  }, [s.players, (window.LINES_DATA || {}).generated]);
  useEffect(() => {
    let dead = false;
    const E = window.ESPN_DATA || {}, sc = s.sc || {}, out = {}, byId = {};
    roster.forEach((p) => (byId[String(p.id).slice(1)] = p));
    Object.entries(E.daily || {}).forEach(([d, Tm]) => Object.values(Tm || {}).forEach((tm) => Object.entries(tm || {}).forEach(([pid, v]) => {
      const p = byId[pid];
      if (!p || !v || v[0] == null || !(SCHED[p.t] && SCHED[p.t].has(d)) || gState(p.t, d).s === "P" || (p.p === "G" && !v[0])) return;
      (out[pid] = out[pid] || {})[d] = v[0];
    })));
    const est = (x) => (x.sv != null
      ? (x.dec === "W" ? (sc.W ?? 5) : 0) + (x.dec === "O" ? (sc.OTL ?? 1) : 0) + (x.sv || 0) * (sc.SV ?? 0.6) + (x.ga || 0) * (sc.GA ?? -3)
      : (x.g || 0) * (sc.G ?? 6) + (x.a || 0) * (sc.A ?? 4) + (x.pm || 0) * (sc.PM ?? 2) + (x.sog || 0) * (sc.SOG ?? 1) + (x.hit || 0) * (sc.HIT ?? 0.1) + (x.blk || 0) * (sc.BLK ?? 1) + (x.ppg || 0) * (sc.PPP ?? 2));
    const finish = () => {
      if (dead) return;
      const h = {};
      Object.keys(out).forEach((pid) => { h[pid] = Object.keys(out[pid]).sort().slice(-5).map((d) => ({ d, v: out[pid][d] })); });
      setHist(h);
    };
    finish();
    gxBoxIdx().then((ds) => Promise.all(ds.slice(-14).map((d) => gxBoxDay(d).then((day) => [d, day])))).then((days) => {
      days.forEach(([d, day]) => {
        if (!day) return;
        Object.keys(byId).forEach((pid) => {
          const x = day[pid];
          if (x) { const o2 = (out[pid] = out[pid] || {}); o2[d] = x.fp != null ? x.fp : o2[d] != null ? o2[d] : est(x); }
          else if (out[pid]) delete out[pid][d];
        });
      });
      finish();
    }).catch(() => {});
    return () => { dead = true; };
  }, [s.players, gen]);
  const RO = { F1: "L1", F2: "L2", F3: "L3", F4: "L4", D1: "D1", D2: "D2", D3: "D3" };
  const roleTxt = (p) => {
    if (p.p === "G") return Math.round(p.prob * 100) + "% of starts";
    const r = roles[p.id];
    if (!r) return "";
    return [r.es ? RO[r.es] : "not in lineup", r.pp].filter(Boolean).join(" \u00b7 ");
  };
  const nextGame = (p) => {
    const S = SCHED[p.t];
    if (!S || p.ir) return "";
    for (let i = 0; i < 10; i++) {
      const dt = addDays(today, i);
      if (S.has(dt) && (i > 0 || gState(p.t, dt).s === "P")) { const gm = gameOf(p.t, dt); return (i === 0 ? "Today" : dayLabel(dt).split(",")[0]) + (gm ? (gm.h ? " vs " : " @ ") + gm.o : ""); }
    }
    return "";
  };
  const left = (p) => (wk.games[p.t] || []).filter((d) => dates[d] >= today && gState(p.t, dates[d]).s === "P").length;
  const nextG = (p) => (nextW ? gms(nextW, p.t) : 0);
  const keyFn = { mu: (p) => mu[p.id] || 0, left, next: nextG, sea: (p) => (p.gp ? p.tot / p.gp : -99), pg: pv, rk: (p) => -(rankOf[p.id] || 9999) }[sort];
  const grp = (k) => roster.filter((p) => !p.ir && p.p === k).sort((a, b) => keyFn(b) - keyFn(a));
  const groups = [["Forwards", grp("F")], ["Defence", grp("D")], ["Goalies", grp("G")], ["Injured reserve", roster.filter((p) => p.ir)]].filter((x) => x[1].length);
  const healthy = roster.filter((p) => !p.ir).sort((a, b) => effAvg(b, K) - effAvg(a, K));
  const prot = new Set([...healthy.slice(0, s.protectTop ?? 8).map((p) => p.id), ...roster.filter((p) => p.keep).map((p) => p.id)]);
  const weak = healthy.filter((p) => !prot.has(p.id)).sort((a, b) => pv(a) - pv(b)).slice(0, 3);
  const HB = (k, l, cls) => <button type="button" className={"n " + (cls || "") + (sort === k ? " on" : "")} onClick={() => setSort(sort === k ? "pg" : k)}>{l}</button>;
  const spark = (p) => {
    const h = hist[String(p.id).slice(1)] || [];
    return (
      <div className="gx-sp m-hide" title="Last five games, oldest to newest">
        {h.length ? h.map((x, i) => <i key={i} style={{ height: Math.max(2, Math.min(22, (Math.max(0, x.v) / 20) * 22)), background: x.v < 0 ? "var(--bad)" : "var(--ink2)" }}></i>) : <span className="text-xs text-slate-500">{"\u2013"}</span>}
      </div>
    );
  };
  const row = (p) => {
    const st = p.ir ? "IR" : p.status && p.status !== "ACTIVE" ? M_ST[p.status] || p.status.replace(/_/g, " ") : "";
    const m = mu[p.id], sea = p.gp ? p.tot / p.gp : null, gap = sea != null && p.avg > 0 ? sea - p.avg : null, rk = rankOf[p.id];
    const sub = [roleTxt(p), nextGame(p)].filter(Boolean).join(" \u00b7 ");
    return (
      <div key={p.id} className="gx-ro">
        <TeamLogo t={p.t} size={26} />
        <div className="min-w-0">
          <div className="truncate"><PN p={p} className="" />{st ? <span className="text-xs" style={{ color: "var(--bad)", marginLeft: 8 }}>{st}</span> : null}</div>
          {sub ? <div className="text-xs text-slate-500 truncate">{sub}</div> : null}
        </div>
        {spark(p)}
        <div className="n">
          <div className="font-semibold" style={p.p === "G" && m != null ? { color: m > 5 ? "var(--good)" : m < 0 ? "var(--bad)" : "var(--ink)" } : null}>{m == null ? "\u2013" : f1(m)}</div>
          {m > 0 && total > 0 ? <div style={{ height: 3, background: "var(--track)", marginTop: 3 }}><div style={{ height: 3, width: Math.min(100, (m / total) * 100) + "%", background: "var(--accent)" }}></div></div> : null}
        </div>
        <div className="n text-slate-500">{p.ir ? "\u2013" : left(p)}</div>
        <div className="n text-slate-500 m-hide">{nextW && !p.ir ? nextG(p) : "\u2013"}</div>
        <div className="n m-hide">{sea == null ? "\u2013" : <>{f1(sea)}{gap != null ? <span className="text-xs" style={{ marginLeft: 6, color: gap >= 0 ? "var(--good)" : "var(--bad)" }}>{(gap >= 0 ? "+" : "") + f1(gap)}</span> : null}</>}</div>
        <div className="n">{f1(effAvg(p, K))}</div>
        <div className="n text-xs text-slate-500 m-hide">{rk ? p.p + " " + ordN(rk) : "\u2013"}</div>
      </div>
    );
  };
  const rkc = (v) => (v >= 8 ? { color: "var(--bad)" } : v && v <= 3 ? { color: "var(--good)" } : null);
  const order = { F: 0, D: 1, G: 2 };
  const sorted = [...roster].sort((a, b) => (a.ir ? 1 : 0) - (b.ir ? 1 : 0) || order[a.p] - order[b.p] || effAvg(b, K) - effAvg(a, K));
  const Ls = wk.days.map((_, d) => (d < done ? null : dayLineup(roster, wk, d, K)));
  const cell = (p, d) => { if (p.ir || !(wk.games[p.t] || []).includes(d)) return "none"; const L = Ls[d]; if (!L) return "past"; if (L.start.some((x) => x.id === p.id)) return "start"; if (L.bench.some((x) => x.id === p.id)) return "sit"; return "out"; };
  const CELL = { start: "bg-green-500", sit: "bg-amber-500", out: "bg-red-500", past: "bg-slate-200" };
  return (
    <div className="space-y-3">
      <div className="text-sm" style={{ display: "flex", flexWrap: "wrap", gap: "6px 18px" }}>
        <span><span className="text-slate-500">Strength</span> {meRow ? f1(meRow.strength) : "\u2013"} a week</span>
        <span><span className="text-slate-500">Forwards</span> <span style={rkc(g.F)}>{g.F ? ordN(g.F) : "\u2013"}</span></span>
        <span><span className="text-slate-500">Defence</span> <span style={rkc(g.D)}>{g.D ? ordN(g.D) : "\u2013"}</span></span>
        <span><span className="text-slate-500">Goalies</span> <span style={rkc(g.G)}>{g.G ? ordN(g.G) : "\u2013"}</span></span>
      </div>
      <div className="gx-pn"><b></b><b></b><b></b><b></b>
        <div className="gx-ro gx-roh">
          <span></span><span>Tap a heading to sort</span>
          <span className="n m-hide">Last 5</span>
          {HB("mu", "Matchup")}{HB("left", "Left")}{HB("next", "Next wk", "m-hide")}{HB("sea", "Season", "m-hide")}{HB("pg", "Per game")}{HB("rk", "Rank", "m-hide")}
        </div>
        {groups.map(([title, list]) => (
          <div key={title} style={{ marginBottom: 10 }}>
            <div className="gx-tag" style={{ padding: "8px 0 4px" }}>{title}</div>
            {list.map(row)}
          </div>
        ))}
      </div>
      <GxPanel title="Weakest spots" right="First to drop or include in a trade">
        {weak.length ? weak.map((p, i) => (
          <div key={p.id} className="gx-row" style={i ? null : { borderTop: 0 }}>
            <TeamLogo t={p.t} size={22} />
            <span className="min-w-0 truncate" style={{ flex: 1 }}><PN p={p} className="" /></span>
            <span className="text-xs text-slate-500 whitespace-nowrap">{rankOf[p.id] ? p.p + " " + ordN(rankOf[p.id]) : p.p}</span>
            <span className="font-semibold text-right" style={{ minWidth: 40, fontVariantNumeric: "tabular-nums" }}>{f1(pv(p))}</span>
          </div>
        )) : <div className="text-sm text-slate-500">Everyone outside your protected players is pulling his weight.</div>}
      </GxPanel>
      <MyForm s={s} />
      <MyInjProt s={s} setS={setS} wk={wk} />
      <Section title="This week, day by day" sub="Bright = in your lineup, amber = plays but would sit, red = out, grey = already played.">
        <div className="overflow-x-auto">
          <table className="text-sm w-full">
            <thead><tr><th className="px-2 py-2 text-left">Player</th>{wk.days.map((d, i) => <th key={i} className="px-1 py-2 text-center">{d.split(",")[0]}</th>)}</tr></thead>
            <tbody>
              {sorted.filter((p) => !p.ir).map((p) => (
                <tr key={p.id} className="border-t border-slate-100">
                  <td className="px-2 py-1 whitespace-nowrap"><PN p={p} className="" /> <span className="text-xs text-slate-400">{p.p}</span></td>
                  {wk.days.map((_, d) => { const c = cell(p, d); return <td key={d} className="px-1 py-1 text-center">{c === "none" ? <span className="text-slate-400">{"\u00b7"}</span> : <span className={"inline-block w-6 h-3 rounded " + CELL[c]}></span>}</td>; })}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Section>
    </div>
  );
}

'''

R37_HELPERS = r'''// ---------- round 37: Team sub-pages and box-score history for the roster (news_logos.py) ----------
const TEAM_SUBS = [["roster", "Roster"], ["pickups", "Pickups"], ["plan", "Plan"], ["trades", "Trades"], ["lines", "Lines"]];
const PICK_SUBS = [["advice", "Advice"], ["adddrop", "Add / Drop"], ["players", "Players"], ["goalies", "Goalie streams"], ["playoffs", "Playoffs"]];
function SubBar({ tab, sub, go, setSubs, nav }) {
  const team = tab === "myteam" || tab === "moves" || tab === "lines";
  if (!team) return nav && nav[2] ? <div className="mb-4"><Pills items={nav[2]} value={sub} onChange={(v) => setSubs((x) => ({ ...x, [tab]: v }))} /></div> : null;
  const inPick = PICK_SUBS.some((x) => x[0] === sub);
  const cur = tab === "myteam" ? "roster" : tab === "lines" ? "lines" : sub === "planner" ? "plan" : sub === "trades" ? "trades" : "pickups";
  const to = (k) => (k === "roster" ? go("myteam") : k === "lines" ? go("lines") : k === "plan" ? go("moves", "planner") : k === "trades" ? go("moves", "trades") : go("moves", inPick ? sub : "advice"));
  return (
    <div className="mb-4">
      <Pills items={TEAM_SUBS} value={cur} onChange={to} />
      {cur === "pickups" ? (
        <div className="flex gap-4 overflow-x-auto navscroll text-sm" style={{ marginTop: 10 }}>
          {PICK_SUBS.map(([k, l]) => <button key={k} type="button" onClick={() => go("moves", k)} className={"whitespace-nowrap " + (sub === k || (k === "advice" && !inPick) ? "font-semibold" : "text-slate-500")}>{l}</button>)}
        </div>
      ) : null}
    </div>
  );
}
const gxBoxIdx = () => fetch("box/index.json?t=" + Date.now()).then((r) => (r.ok ? r.json() : null)).then((j) => (j && j.dates) || []).catch(() => []);
const gxBoxDay = (d) => {
  const B = (window.__BOX = window.__BOX || { idx: null, at: 0, days: {} });
  if (B.days[d]) return Promise.resolve(B.days[d]);
  return fetch("box/" + d + ".json").then((r) => (r.ok ? r.json() : null)).then((j) => { if (j && j.p) B.days[d] = j.p; return (j && j.p) || null; }).catch(() => null);
};

'''

R37_PILLS_OLD = r'''{nav && nav[2] && <div className="mb-4"><Pills items={nav[2]} value={sub} onChange={(v) => setSubs((x) => ({ ...x, [tab]: v }))} /></div>}'''
R37_GROUP = r'''(tab === k || (k === "myteam" && (tab === "moves" || tab === "lines")))'''


def round37(t):
    t = lit(t, "team: styles", "</style>", R37_CSS + "</style>", "round 37 team")
    t = block(t, "team: new Roster page", "function MyTeam({ s, setS, wk, go }) {", "function TeamsTab(", R37_MYTEAM, "team roster v37")
    t = lit(t, "team: sub-buttons under the top bar", R37_PILLS_OLD, "<SubBar tab={tab} sub={sub} go={go} setSubs={setSubs} nav={nav} />", "<SubBar tab={tab}")
    t = lit(t, "team: five top tabs", 'const GX_TABS = [["today", "Today"], ["matchup", "Matchup"], ["myteam", "Team"], ["moves", "Moves"], ["league", "League"]];',
            'const GX_TABS = [["today", "Today"], ["matchup", "Matchup"], ["myteam", "Team"], ["league", "League"]];',
            '["myteam", "Team"], ["league", "League"]];')
    t = lit(t, "team: Setup menu items", 'const GX_MORE = [["teams", "Teams"], ["lines", "Lines"], ["news", "News"], ["setup", "Setup"]];',
            'const GX_MORE = [["setup", "Settings"], ["news", "News"], ["teams", "Teams"]];', 'const GX_MORE = [["setup", "Settings"]')
    t = lit(t, "team: Team tab lights up for its pages",
            '{GX_TABS.map(([k, l]) => <button key={k} onClick={() => pick(k)} className={"gx-tab" + (tab === k ? " on" : "")}>{l}</button>)}',
            '{GX_TABS.map(([k, l]) => <button key={k} onClick={() => pick(k)} className={"gx-tab" + (' + R37_GROUP + ' ? " on" : "")}>{l}</button>)}',
            'className={"gx-tab" + (' + R37_GROUP)
    t = lit(t, "team: last tab is called Setup", '{more ? more[1] : "More"}', '{"Setup"}', '{"Setup"}</button>')
    t = lit(t, "team: phone tabs", 'const M_TABS = [["today", "Today"], ["matchup", "Matchup"], ["myteam", "My Team"], ["moves", "Moves"], ["lines", "Lines"]];',
            'const M_TABS = [["today", "Today"], ["matchup", "Matchup"], ["myteam", "Team"], ["league", "League"]]; // round 37, older marker kept: ["lines", "Lines"]];',
            'round 37, older marker kept: ["lines", "Lines"]];')
    t = lit(t, "team: phone Setup menu", 'const M_MORE = [["teams", "Teams"], ["league", "League"], ["news", "News"], ["setup", "Setup"]];',
            'const M_MORE = [["setup", "Settings"], ["news", "News"], ["teams", "Teams"]]; // round 37, older marker kept: const M_MORE = [["teams", "Teams"], ["league"',
            'round 37, older marker kept: const M_MORE')
    t = lit(t, "team: phone Team tab lights up", "{M_TABS.map(([k, l]) => tabBtn(k, l, tab === k && !menu, () => pick(k)))}",
            "{M_TABS.map(([k, l]) => tabBtn(k, l, " + R37_GROUP + " && !menu, () => pick(k)))}", "tabBtn(k, l, " + R37_GROUP)
    t = lit(t, "team: phone tab row", '<div className="grid grid-cols-6 mt-1">',
            '<div className="grid grid-cols-6 mt-1" style={{ gridTemplateColumns: "repeat(5, minmax(0, 1fr))" }}>', 'gridTemplateColumns: "repeat(5, minmax(0, 1fr))"')
    t = lit(t, "team: phone last tab is Setup", 'tabBtn("more", more ? more[1] : "More",', 'tabBtn("more", more ? more[1] : "Setup",', 'more ? more[1] : "Setup",')
    t = lit(t, "team: helpers", ROOT, R37_HELPERS + ROOT, "function SubBar(")
    for must in ("function SubBar(", "team roster v37", "function MyTeam(", "<MyForm s={s} />", "<MyInjProt s={s}", "Bright = in your lineup", "function TeamsTab(",
                 '["lines", "Lines"]];', 'const M_MORE = [["teams", "Teams"], ["league"', "grid grid-cols-6 mt-1", "function TopBar(", "const GxPanel ="):
        if must not in t:
            fail("fantasy-gm.html looks damaged after round 37 (" + must + ").")
    return t


_fix_before_r37 = fix


def fix(t):
    return round37(_fix_before_r37(t))

# ---------- round 38: Matchup list fits a phone (short names, smaller logos, tighter columns) ----------
R38_CSS = r'''  /* round 38 matchup on phones (news_logos.py) */
  .gx-pc { display: flex; align-items: center; gap: 10px; }
  @media (max-width: 640px) {
    .gx-pn { padding: 12px 10px; }
    .gx-pc { gap: 6px; }
    .gx-h2h { grid-template-columns: minmax(0,1fr) 38px 14px 38px minmax(0,1fr); gap: 4px; padding: 8px 0; }
    .gx-h2h img { width: 20px !important; height: 20px !important; }
    .gx-h2h .gx-nm { font-size: 13px; }
    .gx-h2h .text-xs { font-size: 11px; }
    .gx-h2h .gm-pill { display: none; }
  }
'''

R38_ROW_OLD = r'''<div className="min-w-0" style={{ display: "flex", alignItems: "center", gap: 10, flexDirection: right ? "row-reverse" : "row" }}><TeamLogo t={p.t} size={30} />'''
R38_ROW_NEW = r'''<div className="min-w-0 gx-pc" style={{ flexDirection: right ? "row-reverse" : "row" }}><TeamLogo t={p.t} size={30} />'''
R38_NAME_OLD = r'''<div className="truncate"><PN p={p} className="" /></div>'''
R38_NAME_NEW = (r'''<div className="truncate gx-nm"><button type="button" className="hover:underline text-left" onClick={(e) => { e.stopPropagation(); if (window.__NAV) window.__NAV.player(p); }}>'''
                r'''<span className="m-hide">{p.n}</span><span className="m-inl">{shortN(p.n)}</span></button></div>''')


def round38(t):
    t = lit(t, "matchup phone: styles", "</style>", R38_CSS + "</style>", "round 38 matchup on phones")
    t = lit(t, "matchup phone: tighter logo and name", R38_ROW_OLD, R38_ROW_NEW, 'className="min-w-0 gx-pc"')
    t = lit(t, "matchup phone: short names", R38_NAME_OLD, R38_NAME_NEW, '<div className="truncate gx-nm">')
    for must in ("matchup v35", "ring v36", "function Matchup(",
                 '<TeamLogo t={p.t} size={30} /><div className={"min-w-0" + (right ? " text-right" : "")} style={{ flex: 1 }}>'):
        if must not in t:
            fail("fantasy-gm.html looks damaged after round 38 (" + must + ").")
    return t


_fix_before_r38 = fix


def fix(t):
    return round38(_fix_before_r38(t))

# ---------- round 39: Lines page. Real positions (centre in the middle), rink outline, power play shown, team search ----------
GLINES = "gm_lines.py"
PY_BAK[GLINES] = "gm_lines.backup-news.py"
PY_DONE[GLINES] = "DFPOS = {}"

GL39_DEFS = '''DFPOS = {}


def _df_pos(obj, out):
    # remember each player's position (lw, c, rw, ld, rd, g) for every line group on a Daily Faceoff page (news_logos.py round 39)
    if isinstance(obj, dict):
        nm, pi, gi = obj.get("name"), obj.get("positionIdentifier"), obj.get("groupIdentifier")
        if isinstance(nm, str) and isinstance(pi, str) and isinstance(gi, str):
            out.setdefault(gi.lower(), {})[nm] = pi.lower()
        for v in obj.values():
            _df_pos(v, out)
    elif isinstance(obj, list):
        for v in obj:
            _df_pos(v, out)


def team_pos(t, state, rosters):
    df = DFPOS.get(t) or (state.get("dfpos") or {}).get(t) or {}
    a = {}
    for gi, m in df.items():
        if gi[:1] in ("f", "d", "g"):
            for n, p in m.items():
                a.setdefault(n, p)
    b = {v["n"]: (v.get("pc") or "") + (v.get("sh") or "") for v in (rosters.get(t) or {}).values() if v.get("pc")}
    return {"df": a, "nhl": b}


def read_team(t):'''

GL39_GRAB = '''    try:
        pm39_ = {}
        _df_pos(data, pm39_)
        if pm39_:
            DFPOS[t] = pm39_
    except Exception:
        pass
    out, used = {}, set()
'''


def fix_glines39(t):
    t = lit(t, "lines data: position helpers", "def read_team(t):", GL39_DEFS, "DFPOS = {}")
    t = lit(t, "lines data: read positions from Daily Faceoff", "    out, used = {}, set()\n", GL39_GRAB, "pm39_ = {}")
    t = lit(t, "lines data: NHL position as a backup", 'pl[str(x["id"])] = {"n": n, "p": pos}',
            'pl[str(x["id"])] = {"n": n, "p": pos, "pc": x.get("positionCode") or "", "sh": x.get("shootsCatches") or ""}',
            '"pc": x.get("positionCode")')
    t = lit(t, "lines data: remember positions between reads", '    lines = state.get("lines") or {}\n',
            '    state["dfpos"] = {**(state.get("dfpos") or {}), **DFPOS}\n    lines = state.get("lines") or {}\n', 'state["dfpos"] =')
    t = lit(t, "lines data: positions in the file", '"roster": len(rosters.get(t) or {})}',
            '"roster": len(rosters.get(t) or {}), "pos": team_pos(t, state, rosters)}', '"pos": team_pos(t, state, rosters)')
    py_ok(GLINES, t)
    return t


PY_FIXES[GLINES] = fix_glines39

LT39_CSS = r'''
/* lines v39 */
.lt-rink{border:1px solid var(--line2);border-radius:26px;padding:6px 14px 16px}
.lt-sec{background:none;text-align:left;padding:0;margin:14px 0 8px;font-size:12px;letter-spacing:.06em;text-transform:none;color:var(--mute);font-weight:400}
.lt-pc{border-left-width:1px;border-left-color:var(--line)}
.lt-pc.me{border-color:var(--accent)}
.lt-ps{font-size:11px;color:var(--faint);margin-bottom:1px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.lt-pp5{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:6px}
@media(max-width:640px){.lt-pp5{grid-template-columns:repeat(3,minmax(0,1fr))}.lt-rink{padding:4px 8px 12px;border-radius:18px}}
'''

LT39_TEAMS = r'''  // ---------- player card inside a team (lines v39: real positions, points a game, hot and cold) ----------
  // older done markers kept: round 31: open one team's lines | lt-legend-wrap
  const POS_OK = { lw: 1, c: 1, rw: 1, ld: 1, rd: 1, g: 1 };
  function posMap(T) {
    const P = (T && T.pos) || {}, df = P.df || {}, nhl = {};
    Object.entries(P.nhl || {}).forEach(([n, v]) => { nhl[nk(n)] = v; });
    return (n) => {
      if (df[n] && POS_OK[df[n]]) return df[n];
      const v = nhl[nk(n)] || "";
      return v[0] === "C" ? "c" : v[0] === "L" ? "lw" : v[0] === "R" ? "rw" : v[0] === "D" ? (v[1] === "R" ? "rd" : "ld") : v[0] === "G" ? "g" : "";
    };
  }
  // a forward line in left wing, centre, right wing order; a pair in left, right order
  function arrange(names, pos, fwd, val) {
    if (!fwd) {
      const l = names.filter((n) => pos(n) === "ld"), r = names.filter((n) => pos(n) === "rd"), o = names.filter((n) => pos(n) !== "ld" && pos(n) !== "rd");
      const out = [l[0] || null, r[0] || null];
      [...l.slice(1), ...r.slice(1), ...o].forEach((n) => { const i = out.indexOf(null); if (i >= 0) out[i] = n; else out.push(n); });
      return out;
    }
    const slots = [null, null, null], rest = [], want = { lw: 0, rw: 2 };
    names.filter((n) => pos(n) === "c").sort((x, y) => val(y) - val(x)).forEach((n, i) => { if (i === 0) slots[1] = n; else rest.push(n); });
    names.filter((n) => pos(n) !== "c").forEach((n) => { const i = want[pos(n)]; if (i != null && slots[i] == null) slots[i] = n; else rest.push(n); });
    rest.forEach((n) => { const i = slots[0] == null ? 0 : slots[2] == null ? 2 : slots[1] == null ? 1 : -1; if (i >= 0) slots[i] = n; else slots.push(n); });
    return slots;
  }
  function PCard({ n, t, g, pl, mode, ctx, s, H, onPick }) {
    if (!n) return <div className="lt-pc lt-empty"><div className="lt-nm">{"\u2014"}</div><small>open spot</small></div>;
    const k = nk(n), p = ctx.pOf(k, g), K = s.blend;
    const f = ctx.fpOf(k, g), v = ctx.useThis ? f.cur : f.last, pg = v && v[1] ? v[0] / v[1] : null;
    const rec = p ? H.sigOf(p).rec : null, base = p ? H.effAvg(p, K) : 0, fr = rec && rec.gp >= 3 && base > 0 ? rec.ppg / base : null;
    const tone = fr == null ? "" : fr >= 1.25 ? "lt-up" : fr <= 0.7 ? "lt-dn" : "";
    const w = ctx.where[k + "|" + t] || {}, ch = mode === "pp" ? null : ctx.latestES[k + "|" + t];
    const bits = [];
    if (mode !== "pp" && w.pp) bits.push(w.pp);
    if (ch && ch.type === "line" && ch.from) bits.push((ch.dir === "up" ? "up from " : "down from ") + (SHORT[ch.from] || ch.from));
    if (ch && ch.type === "lineup" && ch.dir === "in") bits.push("new in lineup");
    const hurt = p && p.status && p.status !== "ACTIVE";
    if (hurt) bits.push(INJ[p.status] || pretty(p.status));
    const head = [pl, p && p.ft === s.me ? "yours" : p && p.ft === "fa" ? "free agent" : ""].filter(Boolean).join(" \u00b7 ");
    const parts = n.split(" "), short = parts.length > 1 ? parts[0][0] + ". " + parts.slice(1).join(" ") : n;
    return (
      <button className={"lt-pc" + (p && p.ft === s.me ? " me" : "")} title={n} onClick={() => onPick({ name: n, key: k, t, g: g || (p ? p.p : "F"), p })}>
        {head ? <div className="lt-ps">{head}</div> : null}
        <div className="lt-nm"><span className="lt-full">{n}</span><span className="lt-short">{short}</span></div>
        <small><span className={tone}>{pg == null ? "no games yet" : H.f1(pg)}</span>{bits.map((b, i) => <span key={i}>{" \u00b7 " + b}</span>)}</small>
      </button>
    );
  }

  // ---------- one team, opened: forwards, defence, goalies in a rink, then both power-play units ----------
  function TeamBody({ t, T, chg, ctx, s, H, onPick, onPickChange }) {
    const ln = T.lines || {};
    if (!ln.F1) return <div className="lt-msg">Lines not available yet.</div>;
    const pos = posMap(T);
    const val = (n, g) => { const f = ctx.fpOf(nk(n), g), v = ctx.useThis ? f.cur : f.last; return v ? v[0] : -1; };
    const card = (n, g, pl, mode, key) => <PCard key={key} n={n} t={t} g={g} pl={pl} mode={mode} ctx={ctx} s={s} H={H} onPick={onPick} />;
    const gOf = (n) => { const w = ctx.where[nk(n) + "|" + t]; const g = w && w.es ? grpOf(w.es) : null; if (g) return g; const p = ctx.pOf(nk(n)); return p ? p.p : "F"; };
    const line = (sl, fwd, labels) => {
      const names = ln[sl] || [], known = names.some((n) => pos(n));
      const a = known ? arrange(names, pos, fwd, (n) => val(n, fwd ? "F" : "D")) : names.slice();
      while (a.length < labels.length) a.push(null);
      return a.slice(0, labels.length).map((n, i) => card(n, fwd ? "F" : "D", known ? labels[i] : "", "es", sl + i));
    };
    const goalies = (ln.G || []).slice().sort((a, b) => { const pa = ctx.pOf(nk(a), "G"), pb = ctx.pOf(nk(b), "G"); return (pb ? pb.prob : 0) - (pa ? pa.prob : 0) || val(b, "G") - val(a, "G"); });
    const gLab = (n) => { const p = n ? ctx.pOf(nk(n), "G") : null; return p ? Math.round(p.prob * 100) + "% of starts" : "G"; };
    const unit = (sl) => {
      const arr = ln[sl] || [];
      if (!arr.length) return <div className="lt-msg">Not available.</div>;
      const fw = arr.filter((n) => gOf(n) !== "D").sort((a, b) => val(b, "F") - val(a, "F")), df = arr.filter((n) => gOf(n) === "D").sort((a, b) => val(b, "D") - val(a, "D"));
      return <div className="lt-pp5">{[...fw, ...df].map((n) => card(n, gOf(n), gOf(n) === "D" ? "D" : "F", "pp", sl + n))}</div>;
    };
    return (
      <div>
        <div className="lt-rink">
          <div className="lt-sec">Forwards</div>
          <div className="lt-grid">
            {ES_F.map((sl) => <React.Fragment key={sl}><div className="lt-rl">{SHORT[sl]}</div>{line(sl, true, ["LW", "C", "RW"])}</React.Fragment>)}
          </div>
          <div className="lt-sec">Defence</div>
          <div className="lt-grid d">
            {ES_D.map((sl) => <React.Fragment key={sl}><div className="lt-rl">{SHORT[sl]}</div>{line(sl, false, ["LD", "RD"])}</React.Fragment>)}
          </div>
          <div className="lt-sec">Goalies</div>
          <div className="lt-gg">{[goalies[0] || null, goalies[1] || null].map((n, i) => card(n, "G", gLab(n), "es", "G" + i))}</div>
        </div>
        <div className="lt-sec">Power play 1</div>
        {unit("PP1")}
        <div className="lt-sec">Power play 2</div>
        {unit("PP2")}
        {chg.length ? (
          <details className="lt-how"><summary>{chg.length} recent change{chg.length > 1 ? "s" : ""}</summary>
            {chg.map((x) => <Row key={x.c.id} x={x} s={s} H={H} onPick={onPickChange} dim />)}
          </details>
        ) : null}
      </div>
    );
  }

  // ---------- team list: your teams first, then by standings ----------
  function Teams({ L, ctx, items, s, H, onPick, onPickChange }) {
    const [onlyMine, setOnlyMine] = useState(false);
    const [open, setOpen] = useState({});
    useEffect(() => {
      const show = (t) => {
        if (!t) return;
        window.__LINES_TEAM = null;
        setOnlyMine(false); setOpen((o) => ({ ...o, [t]: true }));
        setTimeout(() => { const el = document.getElementById("lt-team-" + t); if (el) el.scrollIntoView({ behavior: "smooth", block: "start" }); }, 150);
      };
      show(window.__LINES_TEAM);
      const h = (e) => show(e.detail);
      window.addEventListener("gm-lines-team", h);
      return () => window.removeEventListener("gm-lines-team", h);
    }, []);
    const st = (T) => T.st || {};
    const rows = Object.entries(L.teams || {}).map(([t, T]) => ({ t, T }));
    rows.sort((a, b) => (st(b.T).pts || 0) - (st(a.T).pts || 0) || (st(b.T).pct || 0) - (st(a.T).pct || 0));
    const today = H.todayISO();
    rows.forEach((x, i) => {
      x.rank = i + 1;
      x.mine = s.players.filter((p) => p.ft === s.me && p.t === x.t && !p.ir).length;
      x.chg = items.filter((it) => it.c.team === x.t);
      x.next = ((L.sched || {})[x.t] || []).find((g) => g.d >= today);
    });
    const shown = rows.filter((x) => !onlyMine || x.mine).sort((a, b) => (b.mine ? 1 : 0) - (a.mine ? 1 : 0) || a.rank - b.rank);
    const anyOpen = Object.keys(open).some((k) => open[k]);
    return (
      <H.Section title="Teams" sub={`Lines checked ${ago(L.lines_at)}. Numbers are fantasy points a game: green is hot, red is cold.`}>
        <div className="flex flex-wrap gap-4 items-center text-xs" style={{ marginBottom: 10 }}>
          <label className="flex items-center gap-1"><input type="checkbox" checked={onlyMine} onChange={(e) => setOnlyMine(e.target.checked)} /> Only teams with my players</label>
          <button className="lt-link" style={{ padding: 0 }} onClick={() => setOpen(anyOpen ? {} : Object.fromEntries(rows.map((x) => [x.t, true])))}>{anyOpen ? "Close all teams" : "Open all teams"}</button>
        </div>
        {shown.map((x) => {
          const isOpen = !!open[x.t], sd = st(x.T);
          const meta = [sd.gp ? `${sd.w}-${sd.l}-${sd.otl}` : "", x.next ? `next ${H.dayLabel(x.next.d).split(",")[0]} ${x.next.h ? "vs" : "@"} ${x.next.o}` : "", x.mine ? `${x.mine} of yours` : ""].filter(Boolean).join(" \u00b7 ");
          return (
            <div key={x.t} id={"lt-team-" + x.t} style={{ scrollMarginTop: 120 }} className={"lt-team" + (isOpen ? " open" : "")}>
              <div className="lt-tr" onClick={() => setOpen({ ...open, [x.t]: !isOpen })}>
                {H.TeamLogo ? <div style={{ flexShrink: 0 }}><H.TeamLogo t={x.t} size={32} /></div> : null}
                <div className="lt-tmain">
                  <div className="lt-tn">{sd.name || x.t}</div>
                  <div className="lt-meta">{meta}</div>
                </div>
                <div className="lt-chev">{"\u25be"}</div>
              </div>
              {isOpen && <div className="lt-body"><TeamBody t={x.t} T={x.T} chg={x.chg} ctx={ctx} s={s} H={H} onPick={onPick} onPickChange={onPickChange} /></div>}
            </div>
          );
        })}
        {!shown.length && <div className="lt-msg">No teams match.</div>}
      </H.Section>
    );
  }

'''

LT39_TAB = r'''  // ---------- the tab (lines v39: one search box for teams and players) ----------
  function LinesTab({ s, wk, H }) {
    const [, tick] = useState(0);
    const [sel, setSel] = useState(null);
    const [q, setQ] = useState("");
    useEffect(() => {
      const id = setInterval(() => {
        const sc = document.createElement("script");
        sc.src = "lines-data.js?t=" + Date.now();
        sc.onload = () => { sc.remove(); tick((x) => x + 1); };
        sc.onerror = () => sc.remove();
        document.head.appendChild(sc);
      }, 3 * 60 * 1000);
      return () => clearInterval(id);
    }, []);
    const L = window.LINES_DATA;
    const pr = (wk.pairs || []).find((x) => x[0] && x[1] && (x[0] === s.me || x[1] === s.me));
    const opp = pr ? (pr[0] === s.me ? pr[1] : pr[0]) : s.opp;
    const ctx = useMemo(() => build(s, L), [s.players, L && L.generated]);
    const items = useMemo(() => enrich(L, ctx, s, opp), [ctx, opp, L && L.generated]);
    if (!L) return <H.Section title="Lines">No line data yet. It appears after the next sync.</H.Section>;
    const pick = (it) => { setSel(it); window.scrollTo({ top: 0, behavior: "smooth" }); };
    const pickChange = (x) => pick({ name: x.c.name, key: x.c.key, t: x.c.type === "move" && x.c.dir === "in" && x.c.to ? x.c.to : x.c.team, g: x.c.g || (x.p ? x.p.p : "F"), p: x.p || ctx.pOf(x.c.key, x.c.g) });
    const qq = nk(q);
    const teamHits = qq.length < 2 ? [] : Object.entries(L.teams || {}).filter(([t, T]) => nk(t) === qq || nk((T.st || {}).name || "").includes(qq)).slice(0, 4);
    const results = qq.length < 2 ? [] : ctx.items.filter((i) => i.key.includes(qq))
      .sort((a, b) => (b.key.startsWith(qq) - a.key.startsWith(qq)) || ((b.p ? b.p.own : 0) - (a.p ? a.p.own : 0))).slice(0, 8);
    const showTeam = (t) => { setQ(""); setSel(null); window.dispatchEvent(new CustomEvent("gm-lines-team", { detail: t })); };
    return (
      <div className="space-y-4">
        <H.Section title="Find a team or a player">
          <input className={H.inp + " w-full"} placeholder="Team or player, for example Colorado or MacKinnon" value={q} onChange={(e) => setQ(e.target.value)} />
          {teamHits.length + results.length > 0 && <div className="flex flex-wrap gap-2 mt-2">
            {teamHits.map(([t, T]) => (
              <button key={"t" + t} onClick={() => showTeam(t)} className="px-2 py-1 rounded-lg border border-slate-300 text-xs inline-flex items-center gap-1">
                {H.TeamLogo ? <H.TeamLogo t={t} size={16} /> : null}{(T.st || {}).name || t}
              </button>))}
            {results.map((it) => (
              <button key={it.key + it.t} onClick={() => { setSel(it); setQ(""); }} className="px-2 py-1 rounded-lg border border-slate-300 text-xs">
                {it.name} <span className="text-slate-400">{it.g + " \u00b7 " + it.t}</span>
              </button>))}
          </div>}
          {qq.length >= 2 && !results.length && !teamHits.length && <div className="text-xs text-slate-400 mt-2">Nothing matches "{q}".</div>}
          {sel && <PlayerCard it={sel} s={s} wk={wk} H={H} L={L} ctx={ctx} onClose={() => setSel(null)} onPick={pick} />}
        </H.Section>
        <Teams L={L} ctx={ctx} items={items} s={s} H={H} onPick={pick} onPickChange={pickChange} />
        <Feed items={items} s={s} H={H} L={L} onPick={pickChange} />
      </div>
    );
  }

'''

_fix_lines_before_r39 = JS_FIXES[LINES]


def fix_lines39(t):
    t = _fix_lines_before_r39(t)
    if "lines v39" in t:
        print("(news) lines: new Lines page: already done")
    else:
        end_css = '`;\n  if (!document.getElementById("lt2-css"))'
        a = t.find("  // ---------- player card inside a team ----------")
        b = t.find("  // ---------- game log: past games with box scores", a)
        if b < 0:
            b = t.find("  // ---------- player detail card (unchanged from the old Lines tab) ----------", a)
        if a < 0 or b < 0 or t.count(end_css) != 1:
            fail("lines: could not find the team section in lines-tab.js. Send this log to the AI helper.")
        t = t[:a] + LT39_TEAMS + t[b:]
        c = t.find("  // ---------- the tab ----------")
        d = t.find("  // ---------- compact summary for the Today screen ----------", c)
        if c < 0 or d < 0:
            fail("lines: could not find the Lines tab in lines-tab.js. Send this log to the AI helper.")
        t = t[:c] + LT39_TAB + t[d:]
        t = t.replace(end_css, LT39_CSS + end_css, 1)
        print("(news) lines: new Lines page: updated")
    for must in ("function Teams(", "function TeamBody(", "function PCard(", "function LinesTab(", "function PlayerCard(", "window.LinesTab = LinesTab;",
                 "H.TeamLogo t={x.t} size={32}", 'id={"lt-team-" + x.t}', "Open all teams"):
        if must not in t:
            fail("lines-tab.js looks damaged after round 39 (" + must + ").")
    babel_ok(t, LINES)
    return t


JS_FIXES[LINES] = fix_lines39

R39_HEAD_OLD = r'''{HB("sea", "Season", "m-hide")}{HB("pg", "Per game")}'''
R39_HEAD_NEW = r'''{HB("sea", "So far", "m-hide")}{HB("pg", "Expected")}'''


def round39(t):
    t = lit(t, "lines: plainer roster headings", R39_HEAD_OLD, R39_HEAD_NEW, 'HB("pg", "Expected")')
    return t


_fix_before_r39 = fix


def fix(t):
    return round39(_fix_before_r39(t))

# ---------- round 40: Pickups list (replaces Add / Drop and Players), one panel style everywhere, power play as 3 + 2 ----------
R40_CSS = r'''  /* round 40 pickups (news_logos.py) */
  .gx-st { font-weight: 600; font-size: 15px; letter-spacing: -.01em; }
  .gx-pk { display: grid; grid-template-columns: 28px minmax(0,1fr) 52px 46px 66px 58px 56px; gap: 8px; align-items: center; padding: 9px 0; border-top: 1px solid var(--line); font-variant-numeric: tabular-nums; }
  .gx-pk .n { text-align: right; }
  .gx-pk.row { cursor: pointer; }
  .gx-pk.row:hover { background: var(--hover); }
  @media (max-width: 640px) { .gx-pk { grid-template-columns: 26px minmax(0,1fr) 52px 46px; gap: 6px; } }
'''

R40_SECTION = r'''const Section = ({ title, sub, link, children, closed, id }) => {
  // section v40: the same corner-bracket panel as the new pages (news_logos.py)
  const [k] = useState(() => "sec:" + (window.__TAB || "") + ":" + (id || secKey(title)));
  const [open, setOpen] = useState(() => { const v = uiGet()[k]; return v == null ? !(closed || SEC_SHUT.some((x) => k.indexOf("sec:" + x) === 0)) : !!v; });
  const flip = () => { uiSet(k, !open); setOpen(!open); };
  const onKey = (e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); flip(); } };
  return (
    <div className={"gx-pn text-sm" + (open ? "" : " self-start")} style={{ minWidth: 0 }}><b></b><b></b><b></b><b></b>
      <div className={"flex items-start gap-2" + (open ? " mb-2" : "")}>
        <div role="button" tabIndex={0} aria-expanded={open} className="sec-head" onClick={flip} onKeyDown={onKey}>
          <div className="gx-st">{title}</div>{open && sub ? <div className="text-xs text-slate-500" style={{ marginTop: 2 }}>{sub}</div> : null}
        </div>
        {open && link ? <button className="text-xs text-blue-600 whitespace-nowrap" onClick={link[1]}>{link[0] + " \u2192"}</button> : null}
        <button type="button" onClick={flip} aria-label={open ? "Close this box" : "Open this box"} style={{ lineHeight: 0, padding: "2px 0" }}><span className={"sec-chev" + (open ? "" : " shut")}></span></button>
      </div>
      {open ? children : null}
    </div>
  );
};
'''

R40_HELPERS = r'''// ---------- round 40: Pickups list (news_logos.py) ----------
const gxEst = (x, sc) => (x.sv != null
  ? (x.dec === "W" ? (sc.W ?? 5) : 0) + (x.dec === "O" ? (sc.OTL ?? 1) : 0) + (x.sv || 0) * (sc.SV ?? 0.6) + (x.ga || 0) * (sc.GA ?? -3)
  : (x.g || 0) * (sc.G ?? 6) + (x.a || 0) * (sc.A ?? 4) + (x.pm || 0) * (sc.PM ?? 2) + (x.sog || 0) * (sc.SOG ?? 1) + (x.hit || 0) * (sc.HIT ?? 0.1) + (x.blk || 0) * (sc.BLK ?? 1) + (x.ppg || 0) * (sc.PPP ?? 2));
const gxLast5 = (ids, sc) => gxBoxIdx().then((ds) => Promise.all(ds.slice(-14).map((d) => gxBoxDay(d)))).then((days) => {
  const out = {};
  ids.forEach((pid) => { const a = []; days.forEach((day) => { const x = day && day[pid]; if (x) a.push(x.fp != null ? x.fp : gxEst(x, sc)); }); out[pid] = a.slice(-5); });
  return out;
}).catch(() => ({}));
function Pickups({ s, setS, wk }) {
  const K = s.blend;
  const [H, setH] = useState(1);
  const [pos, setPos] = useState("all");
  const [q, setQ] = useState("");
  const [limit, setLimit] = useState(25);
  const [sim, setSim] = useState(null);
  const [hist, setHist] = useState({});
  const sP = useMemo(() => planS(s), [s]);
  const plan = sP !== s;
  const wkP = useMemo(() => (plan ? deriveWeek(sP.weeks[sP.wk], sP.autoDone) : wk), [sP, wk]);
  const M = useMemo(() => computeMoves(sP, { H, pos, q }), [sP, H, pos, q]);
  const base = useMemo(() => planBase(s, sP), [sP]);
  const minGain = s.minGain ?? 3;
  const all = q ? M.res : M.res.filter((r) => r.gain >= minGain);
  const rows = all.slice(0, limit);
  const wins = useMemo(() => {
    const o = {};
    if (base == null) return o;
    rows.forEach((r) => { o[r.f.id] = winChance(sP, afterMove(sP, r.f, r.d)); });
    return o;
  }, [M, limit, base]);
  const ids = rows.map((r) => String(r.f.id).slice(1)).join(",");
  useEffect(() => {
    let dead = false;
    if (!ids) return;
    gxLast5(ids.split(","), s.sc || {}).then((h) => { if (!dead) setHist((x) => Object.assign({}, x, h)); });
    return () => { dead = true; };
  }, [ids]);
  const ml = movesLeft(s, s.me, wk);
  const pw = plan ? sP.weeks[sP.wk] || {} : null, d0 = pw ? (pw.dates || [])[0] : null;
  const qq = nrm(q);
  const others = qq.length >= 2 ? s.players.filter((p) => p.ft !== "fa" && p.ft !== s.me && nrm(p.n).includes(qq)).slice(0, 6) : [];
  const hLabel = plan ? { 1: "next week", 4: "4 weeks from next week", 0: "rest of season" }[H] : { 1: "rest of this week", 4: "next 4 weeks", 0: "rest of season" }[H];
  const spark = (p) => {
    const h = hist[String(p.id).slice(1)] || [];
    return (
      <div className="gx-sp m-hide" title="Last five games, oldest to newest">
        {h.length ? h.map((v, i) => <i key={i} style={{ height: Math.max(2, Math.min(22, (Math.max(0, v) / 20) * 22)), background: v < 0 ? "var(--bad)" : "var(--ink2)" }}></i>) : <span className="text-xs text-slate-500">{"\u2013"}</span>}
      </div>
    );
  };
  return (
    <div className="space-y-3">
      <div className="text-sm">
        <span className="font-semibold">{ml === 0 ? "No moves left this week." : ml == null ? "" : ml + " move" + (ml === 1 ? "" : "s") + " left this week."}</span>
        {plan ? <span className="text-slate-500"> Showing {pw.label || "next week"}.{d0 ? " Moves reset " + dayLabel(d0) + "." : ""}</span> : null}
      </div>
      <div className="flex flex-wrap gap-2 items-center">
        <Pills items={[["all", "All"], ["F", "Forwards"], ["D", "Defence"], ["G", "Goalies"]]} value={pos} onChange={(v) => { setPos(v); setLimit(25); }} />
        <Pills items={[[1, plan ? "Next week" : "This week"], [4, "Next 4 weeks"], [0, "Rest of season"]]} value={H} onChange={(v) => { setH(v); setLimit(25); }} />
      </div>
      <input className={inp + " w-full"} placeholder="Search any player" value={q} onChange={(e) => setQ(e.target.value)} />
      <div className="gx-pn"><b></b><b></b><b></b><b></b>
        <div className="gx-pk text-xs text-slate-500" style={{ borderTop: 0, paddingTop: 0 }}>
          <span></span><span>{base == null ? "Free agents, best first" : "Win chance now " + wpTxt(base)}</span>
          <span className="n m-hide">Last 5</span><span className="n m-hide">Games</span><span className="n m-hide">Expected</span><span className="n">Adds</span><span className="n">Win</span>
        </div>
        {rows.length ? rows.map((r) => {
          const keep = r.gain > 0 && effAvg(r.f, K) - effAvg(r.d, K) >= 0, tg = shortTag(r.f, K), w = wins[r.f.id];
          const st = r.f.status && r.f.status !== "ACTIVE" ? M_ST[r.f.status] || r.f.status.replace(/_/g, " ") : "";
          return (
            <div key={r.f.id} className="gx-pk row" role="button" onClick={() => setSim({ add: r.f.id, drop: r.d.id })}>
              <TeamLogo t={r.f.t} size={26} />
              <div className="min-w-0">
                <div className="truncate"><PN p={r.f} className="" /> <span className="text-xs text-slate-500">{r.f.p}</span>{r.f.wv ? <span className="text-xs" style={{ color: "var(--warn)", marginLeft: 6 }}>on waivers</span> : null}{st ? <span className="text-xs" style={{ color: "var(--bad)", marginLeft: 6 }}>{st}</span> : null}</div>
                <div className="text-xs text-slate-500 truncate">{"Swap for " + r.d.n + " \u00b7 " + (keep ? "keep" : H === 1 ? "one week only" : "short-term") + (tg ? " \u00b7 " + tg.t : "")}</div>
              </div>
              {spark(r.f)}
              <div className="n text-slate-500 m-hide">{M.gamesIn(r.f)}</div>
              <div className="n m-hide">{f1(effAvg(r.f, K))}</div>
              <div className="n font-semibold" style={{ color: r.gain > 0 ? "var(--good)" : "var(--bad)" }}>{(r.gain >= 0 ? "+" : "") + f1(r.gain)}</div>
              <div className="n" style={w != null && base != null ? { color: w > base + 0.004 ? "var(--good)" : w < base - 0.004 ? "var(--bad)" : "var(--ink)" } : null}>{w == null ? "\u2013" : wpTxt(w)}</div>
            </div>
          );
        }) : <div className="text-sm text-slate-500" style={{ padding: "10px 0" }}>{q ? "No free agent matches that name." : "No pickup adds " + minGain + " or more points for this window."}</div>}
        {all.length > rows.length ? <button type="button" className="text-sm text-blue-600" style={{ marginTop: 10 }} onClick={() => setLimit(limit + 25)}>Show {Math.min(25, all.length - rows.length)} more</button> : null}
        {rows.length ? <div className="text-xs text-slate-500" style={{ marginTop: 10 }}>Adds is the extra points in your lineup for {hLabel}. Tap a player to try the swap or change who you drop.</div> : null}
      </div>
      {others.length ? (
        <GxPanel title="On other teams">
          {others.map((p, i) => (
            <div key={p.id} className="gx-row" style={i ? null : { borderTop: 0 }}>
              <TeamLogo t={p.t} size={22} />
              <span className="min-w-0 truncate" style={{ flex: 1 }}><PN p={p} className="" /> <span className="text-xs text-slate-500">{p.p}</span></span>
              <span className="text-xs text-slate-500 truncate"><TL s={s} id={p.ft} /></span>
              <span className="font-semibold text-right" style={{ minWidth: 40, fontVariantNumeric: "tabular-nums" }}>{f1(effAvg(p, K))}</span>
            </div>
          ))}
        </GxPanel>
      ) : null}
      {sim ? <MoveSim s={sP} setS={setS} wk={wkP} M={M} H={H} hLabel={hLabel} init={sim} wBase={base} onClose={() => setSim(null)} /> : null}
    </div>
  );
}

'''


def round40(t):
    t = lit(t, "pickups: styles", "</style>", R40_CSS + "</style>", "round 40 pickups")
    t = block(t, "pickups: one panel style for every box", "const Section = ({ title, sub, link, children, closed, id }) => {", "const SectionShut =", R40_SECTION, "section v40")
    t = lit(t, "pickups: second-row links",
            'const PICK_SUBS = [["advice", "Advice"], ["adddrop", "Add / Drop"], ["players", "Players"], ["goalies", "Goalie streams"], ["playoffs", "Playoffs"]];',
            'const PICK_SUBS = [["adddrop", "Pickups"], ["advice", "Advice"], ["goalies", "Goalies"], ["playoffs", "Playoffs"]];',
            'const PICK_SUBS = [["adddrop", "Pickups"]')
    t = lit(t, "pickups: Pickups button opens the list", ': go("moves", inPick ? sub : "advice"));', ': go("moves", "adddrop"));', ': go("moves", "adddrop"));')
    t = lit(t, "pickups: list is the default page", '(sub === k || (k === "advice" && !inPick) ? "font-semibold" : "text-slate-500")',
            '(sub === k || (k === "adddrop" && !inPick) ? "font-semibold" : "text-slate-500")', 'k === "adddrop" && !inPick')
    t = lit(t, "pickups: new list replaces Add / Drop", 'sub === "adddrop" ? <AddDrop {...P} /> :', 'sub === "adddrop" ? <Pickups {...P} /> :', "<Pickups {...P} />")
    t = lit(t, "pickups: helpers", ROOT, R40_HELPERS + ROOT, "function Pickups(")
    for must in ("function Pickups(", "section v40", "const Section = (", "const SectionShut =", "const SEC_SHUT =", "function SubBar(", "function MoveSim(", "const gxBoxIdx ="):
        if must not in t:
            fail("fantasy-gm.html looks damaged after round 40 (" + must + ").")
    return t


_fix_before_r40 = fix


def fix(t):
    return round40(_fix_before_r40(t))


LT40_PP_OLD = r'''return <div className="lt-pp5">{[...fw, ...df].map((n) => card(n, gOf(n), gOf(n) === "D" ? "D" : "F", "pp", sl + n))}</div>;'''
LT40_PP_NEW = r'''const all5 = [...fw, ...df], ppc = (n) => card(n, gOf(n), gOf(n) === "D" ? "D" : "F", "pp", sl + n);
      return <div><div className="lt-ppu">{all5.slice(0, 3).map(ppc)}</div>{all5.length > 3 ? <div className="lt-ppd">{all5.slice(3).map(ppc)}</div> : null}</div>;'''

_fix_lines_before_r40 = JS_FIXES[LINES]


def fix_lines40(t):
    t = _fix_lines_before_r40(t)
    t = lit(t, "lines: power play as three and two", LT40_PP_OLD, LT40_PP_NEW, "all5.slice(0, 3).map(ppc)")
    babel_ok(t, LINES)
    return t


JS_FIXES[LINES] = fix_lines40

# ---------- round 41: Plan page, "est." label, box scores matched on position so same-name teammates stay separate ----------
R41_CSS = r'''  /* round 41 plan (news_logos.py) */
  .gx-ps { display: grid; grid-template-columns: 54px minmax(0,1fr) 60px 92px; gap: 10px; align-items: center; padding: 11px 0; border-top: 1px solid var(--line); font-variant-numeric: tabular-nums; }
  .gx-dayc { font-size: 12px; border: 1px solid var(--line2); border-radius: 6px; padding: 3px 0; text-align: center; }
  .gx-wk { display: grid; grid-template-columns: minmax(0,1fr) 110px 96px; gap: 10px; align-items: center; padding: 9px 0; border-top: 1px solid var(--line); font-variant-numeric: tabular-nums; }
  .gx-ps .n, .gx-wk .n { text-align: right; }
  @media (max-width: 640px) { .gx-ps { grid-template-columns: 44px minmax(0,1fr) 50px 74px; gap: 6px; } .gx-wk { grid-template-columns: minmax(0,1fr) 84px 64px; } }
'''

R41_HELPERS = r'''// ---------- round 41: Plan page (news_logos.py) ----------
function PlanPage({ s, setS, wk }) {
  const K = s.blend, today = todayISO();
  const sP = useMemo(() => planS(s), [s]);
  const plan = sP !== s;
  const wkP = useMemo(() => (plan ? deriveWeek(sP.weeks[sP.wk], sP.autoDone) : wk), [sP, wk]);
  const dates = wkP.dates || [], ti = dates.indexOf(today);
  const d0 = Math.min(dates.length, Math.max(wkP.done || 0, ti >= 0 ? ti : 0) + (ti >= 0 && lockedToday() ? 1 : 0));
  const ml = movesLeft(sP, sP.me, wkP), left = ml == null ? 3 : ml;
  const [res, setRes] = useState(null);
  const [busy, setBusy] = useState(true);
  const [openW, setOpenW] = useState(-1);
  useEffect(() => {
    let dead = false;
    setBusy(true);
    const id = setTimeout(() => {
      let r = null;
      try {
        if (left > 0 && d0 < dates.length) {
          const p = buildPlan(sP, wkP, d0, left), b = planBase(s, sP);
          r = { p, b, after: p.steps.map((_, i) => (b == null ? null : winChance(sP, planRoster(sP, wkP, p.steps.slice(0, i + 1))))) };
        }
      } catch (e) { r = null; }
      if (!dead) { setRes(r); setBusy(false); }
    }, 60);
    return () => { dead = true; clearTimeout(id); };
  }, [s.players, sP.wk, left, d0, window.__PMODE]);
  const waste = useMemo(() => {
    const mine = s.players.filter((p) => p.ft === s.me), chronic = {};
    const weeks = s.weeks.slice(s.wk, s.wk + 4).map((w, i) => {
      const dw = deriveWeek(w, s.autoDone), from = i === 0 ? dw.done || 0 : 0, sit = {};
      let empty = 0, g = 0, pts = 0;
      dw.days.forEach((dl, d) => {
        if (d < from) return;
        const L = dayLineup(mine, dw, d, K);
        empty += L.empty;
        L.bench.forEach((p) => {
          const x = (sit[p.id] = sit[p.id] || { p, days: [] });
          x.days.push(dl.split(",")[0]); g++; pts += p.x;
          const c = (chronic[p.id] = chronic[p.id] || { p, g: 0 }); c.g++;
        });
      });
      return { dw, from, sit: Object.values(sit), empty, g, pts };
    });
    return { weeks, chronic: Object.values(chronic).filter((c) => c.g >= 2).sort((a, b) => b.g - a.g).slice(0, 3), g: weeks.reduce((a, w) => a + w.g, 0), pts: weeks.reduce((a, w) => a + w.pts, 0) };
  }, [s.players, s.wk, K, window.__PMODE]);
  const fix = useMemo(() => {
    const w = waste.weeks[openW];
    if (!w || !w.sit.length || (openW === 0 && outOfMoves(s))) return null;
    const mine = s.players.filter((p) => p.ft === s.me), mins = { F: s.minF ?? 10, D: s.minD ?? 5, G: s.minGo ?? 2 };
    const healthy = mine.filter((p) => !p.ir).sort((a, b) => effAvg(b, K) - effAvg(a, K));
    const prot = new Set([...healthy.slice(0, s.protectTop ?? 8).map((p) => p.id), ...mine.filter((p) => p.keep).map((p) => p.id)]);
    const cnt = { F: 0, D: 0, G: 0 }; healthy.forEach((p) => { cnt[p.p]++; });
    const drops = w.sit.map((x) => x.p).filter((p) => !p.ir && !prot.has(p.id)).slice(0, 5);
    const weekPts = (p) => (w.dw.games[p.t] || []).filter((d) => d >= w.from).reduce((t, d) => { const dt = w.dw.dates[d]; return t + effAvg(p, K, dt) * (p.p === "G" ? gStart(p, dt).v : p.prob) * avail(p, dt); }, 0);
    const pool = s.players.filter((p) => p.ft === "fa" && p.prob > 0 && (p.proj !== false || p.gp > 0) && !goalieOut(p)).map((p) => ({ p, v: weekPts(p) })).filter((x) => x.v > 0).sort((a, b) => b.v - a.v).slice(0, 25).map((x) => x.p);
    const base = weekProj(mine, w.dw, K, w.from).total;
    let best = null;
    drops.forEach((d) => pool.forEach((f) => {
      if (d.p !== f.p && cnt[d.p] - 1 < mins[d.p]) return;
      const g = weekProj(timedMove(mine, s.me, [{ add: f, drop: d }]), w.dw, K, w.from).total - base;
      if (!best || g > best.g) best = { d, f, g };
    }));
    return best && best.g >= 1 ? best : null;
  }, [openW, waste]);
  const playDays = (p, a) => (wkP.games[p.t] || []).filter((d) => d >= a && (p.p !== "G" || gStart(p, dates[d]).v >= 0.5)).map((d) => wkP.days[d].split(",")[0]).join(", ");
  const steps = res ? res.p.steps : [];
  const lastWin = res && res.after.length ? res.after[res.after.length - 1] : null;
  const wkName = (w) => { const ds = w.dw.dates || []; return ds.length ? mdL(ds[0]) + " to " + mdL(ds[ds.length - 1]) : w.dw.label; };
  return (
    <div className="space-y-3">
      <div className="text-sm">
        <span className="font-semibold">{plan ? "No moves left this week." : left === 0 ? "No moves left this week." : left + " move" + (left === 1 ? "" : "s") + " left this week."}</span>
        {plan ? <span className="text-slate-500"> Planning {wkP.label || "next week"} with {left === 3 ? "all 3 moves" : left + " move" + (left === 1 ? "" : "s")}.</span> : null}
      </div>
      <div className="gx-pn"><b></b><b></b><b></b><b></b>
        <div style={{ display: "flex", alignItems: "baseline" }}>
          <span className="gx-tag">Your plan</span>
          {steps.length ? (
            <span className="text-sm" style={{ marginLeft: "auto" }}>
              <span className="font-semibold" style={{ color: "var(--good)" }}>{"+" + f1(res.p.gain) + " points"}</span>
              {res.b != null && lastWin != null ? <span className="text-slate-500">{" \u00b7 win chance " + wpTxt(res.b) + " to " + wpTxt(lastWin)}</span> : null}
            </span>
          ) : null}
        </div>
        {busy ? <div className="text-sm text-slate-500" style={{ padding: "12px 0 2px" }}>Working it out...</div>
          : steps.length ? steps.map((st, i) => {
            const a = i ? res.after[i - 1] : res.b, b = res.after[i], dy = playDays(st.add, st.day);
            return (
              <div key={i} className="gx-ps" style={i ? null : { marginTop: 6 }}>
                <span className="gx-dayc">{(wkP.days[st.day] || "").split(",")[0]}</span>
                <div className="min-w-0">
                  <div className="truncate"><PN p={st.add} className="" /> in, <PN p={st.drop} className="" /> out</div>
                  <div className="text-xs text-slate-500 truncate">{(st.add.p === "G" ? "Likely starts " : "Plays ") + (dy || "\u2013")}{st.add.wv ? " \u00b7 on waivers" : ""}</div>
                </div>
                <span className="n font-semibold" style={{ color: "var(--good)" }}>{"+" + f1(st.gain)}</span>
                <span className="n text-slate-500">{a != null && b != null ? wpTxt(a).replace("%", "") + " \u2192 " + wpTxt(b) : ""}</span>
              </div>
            );
          }) : <div className="text-sm text-slate-500" style={{ padding: "12px 0 2px" }}>{left === 0 ? "Nothing to plan until your moves reset." : "No move adds " + (s.minGain ?? 3) + " or more points. Save your moves."}</div>}
        {!busy && steps.length ? <div className="text-xs text-slate-500" style={{ paddingTop: 10, borderTop: "1px solid var(--line)" }}>Make each move before that day's first game. The plan updates itself as injuries and starting goalies change.</div> : null}
      </div>
      <div className="gx-pn"><b></b><b></b><b></b><b></b>
        <div style={{ display: "flex", alignItems: "baseline" }}>
          <span className="gx-tag">Games going to waste</span>
          <span className="text-xs text-slate-500" style={{ marginLeft: "auto" }}>{"Next 4 weeks \u00b7 " + waste.g + " game" + (waste.g === 1 ? "" : "s") + (waste.g ? ", about " + Math.round(waste.pts) + " points" : "")}</span>
        </div>
        <div className="gx-wk text-xs text-slate-500" style={{ borderTop: 0, marginTop: 6, paddingBottom: 4 }}><span></span><span className="n">Stuck on bench</span><span className="n">Empty slots</span></div>
        {waste.weeks.map((w, i) => (
          <div key={i}>
            <div className="gx-wk" role="button" style={{ cursor: "pointer" }} onClick={() => setOpenW(openW === i ? -1 : i)}>
              <span>{wkName(w)}</span>
              <span className="n" style={{ color: w.g ? "var(--bad)" : "var(--mute)" }}>{w.g ? w.g + " game" + (w.g === 1 ? "" : "s") : "0"}</span>
              <span className="n text-slate-500">{w.empty}</span>
            </div>
            {openW === i ? (
              <div className="text-xs text-slate-500" style={{ padding: "0 0 10px" }}>
                {w.sit.length ? <div>Sitting: {w.sit.map((x) => x.p.n + " (" + x.days.join(", ") + ")").join("; ")}</div> : <div>Nobody is stuck on your bench this week.</div>}
                {w.sit.length ? (fix ? <div style={{ marginTop: 4, color: "var(--ink)" }}>Swap that fixes it: <PN p={fix.f} className="font-semibold" /> in, <PN p={fix.d} className="font-semibold" /> out <span style={{ color: "var(--good)" }}>{"+" + f1(fix.g)}</span></div>
                  : <div style={{ marginTop: 4 }}>{i === 0 && outOfMoves(s) ? "No moves left this week to fix it." : "No free agent helps more than keeping who you have."}</div>) : null}
              </div>
            ) : null}
          </div>
        ))}
        <div className="text-xs text-slate-500" style={{ paddingTop: 10, borderTop: "1px solid var(--line)" }}>
          {waste.chronic.length ? "Most often stuck: " + waste.chronic.map((c) => c.p.n + " (" + c.g + " games)").join(", ") + ". " : ""}Tap a week to see who sits and the swap that fixes it.
        </div>
      </div>
    </div>
  );
}

'''


def round41(t):
    t = lit(t, "plan: styles", "</style>", R41_CSS + "</style>", "round 41 plan")
    t = lit(t, "plan: new page", 'return <div className="space-y-4"><AcqPlanner {...props} /><BenchFixer {...props} /></div>;',
            "return <PlanPage {...props} />;", "<PlanPage {...props} />")
    t = lit(t, "plan: helpers", ROOT, R41_HELPERS + ROOT, "function PlanPage(")
    for must in ("function PlanPage(", "function buildPlan(", "const planRoster =", "function PlannerAll(", "function AcqPlanner(", "const goalieOut ="):
        if must not in t:
            fail("fantasy-gm.html looks damaged after round 41 (" + must + ").")
    return t


_fix_before_r41 = fix


def fix(t):
    return round41(_fix_before_r41(t))


_fix_lines_before_r41 = JS_FIXES[LINES]


def fix_lines41(t):
    t = _fix_lines_before_r41(t)
    t = lit(t, "lines: est label on scores", '{(r.pt.est ? "~" : "") + H.f1(r.pt.v)}',
            '{H.f1(r.pt.v)}{r.pt.est ? <span className="text-xs text-slate-500" style={{ fontWeight: 400, marginLeft: 4 }}>est.</span> : null}',
            'marginLeft: 4 }}>est.</span>')
    t = lit(t, "lines: est note", '" ~ means estimated from the box score, without power-play assists or shorthanded points."',
            '" est. means worked out from the box score, without power-play assists or shorthanded points."', '" est. means worked out')
    babel_ok(t, LINES)
    return t


JS_FIXES[LINES] = fix_lines41

SYNC41_KEEP = '''                try:
                    with open(os.path.join(bdir31_, dd31_ + ".json"), encoding="utf-8") as f31_:
                        old41_ = (json.load(f31_) or {}).get("p") or {}
                    for k41_, v41_ in out31_.items():
                        if "fp" not in v41_ and "fp" in (old41_.get(k41_) or {}):
                            v41_["fp"] = old41_[k41_]["fp"]
                except Exception:
                    pass
                with open(os.path.join(bdir31_, dd31_ + ".json"), "w", encoding="utf-8") as f31_:
'''

_fix_sync_before_r41 = PY_FIXES[SYNC]


def fix_sync41(t):
    t = _fix_sync_before_r41(t)
    t = lit(t, "sync: name and position index", "    _pidx = {}\n", "    _pidx = {}\n    _pidx3 = {}\n", "_pidx3 = {}")
    t = lit(t, "sync: name and position index (fill)", '_pidx.setdefault((k_, p_["t"]), p_["id"])',
            '_pidx.setdefault((k_, p_["t"]), p_["id"])\n                _pidx3.setdefault((k_, p_["t"], p_["p"]), p_["id"])', '_pidx3.setdefault((k_, p_["t"], p_["p"])')
    t = lit(t, "sync: name match uses position (today)",
            'for x_ in (grp_.get("forwards") or []) + (grp_.get("defense") or []) + (grp_.get("goalies") or []):',
            'for x_, gp_ in [(y_, "F") for y_ in (grp_.get("forwards") or [])] + [(y_, "D") for y_ in (grp_.get("defense") or [])] + [(y_, "G") for y_ in (grp_.get("goalies") or [])]:',
            'for x_, gp_ in [(y_, "F")')
    t = lit(t, "sync: name match uses position (today, lookup)", "pid_ = _pidx.get((_nk(nm_), tab_)) or _pidx.get((_nk2(nm_), tab_))",
            "pid_ = _pidx3.get((_nk(nm_), tab_, gp_)) or _pidx3.get((_nk2(nm_), tab_, gp_))", "_pidx3.get((_nk(nm_), tab_, gp_))")
    t = lit(t, "sync: name match uses position (history)",
            'for x31_ in (grp31_.get("forwards") or []) + (grp31_.get("defense") or []) + (grp31_.get("goalies") or []):',
            'for x31_, gp31_ in [(y31_, "F") for y31_ in (grp31_.get("forwards") or [])] + [(y31_, "D") for y31_ in (grp31_.get("defense") or [])] + [(y31_, "G") for y31_ in (grp31_.get("goalies") or [])]:',
            'for x31_, gp31_ in [(y31_, "F")')
    t = lit(t, "sync: name match uses position (history, lookup)",
            "pid31_ = _pidx.get((_nk(nm31_), ab31_[s31_])) or _pidx.get((_nk2(nm31_), ab31_[s31_]))",
            "pid31_ = _pidx3.get((_nk(nm31_), ab31_[s31_], gp31_)) or _pidx3.get((_nk2(nm31_), ab31_[s31_], gp31_))", "ab31_[s31_], gp31_))")
    if '{"v": 2, "dates": sorted(have31_)' in t:
        print("(news) sync: name fix re-saves stored days: already done")
    else:
        a41 = '        have31_, none31_ = set(idx31_.get("dates") or []), set(idx31_.get("none") or [])\n'
        b41 = '                with open(os.path.join(bdir31_, dd31_ + ".json"), "w", encoding="utf-8") as f31_:\n'
        c41 = 'json.dump({"dates": sorted(have31_), "none": sorted(none31_)}, f31_, separators=(",", ":"))'
        if t.count(a41) != 1 or t.count(b41) != 1 or t.count(c41) != 1:
            fail("sync: could not find the box-score history block (round 31). Send this log to the AI helper.")
        t = t.replace(a41, '        if idx31_.get("v") != 2:\n            idx31_ = {"none": idx31_.get("none") or []}\n' + a41, 1)
        t = t.replace(b41, SYNC41_KEEP, 1)
        t = t.replace(c41, 'json.dump({"v": 2, "dates": sorted(have31_), "none": sorted(none31_)}, f31_, separators=(",", ":"))', 1)
        print("(news) sync: name fix re-saves stored days: updated")
    py_ok(SYNC, t)
    return t


PY_FIXES[SYNC] = fix_sync41

# ---------- round 42: Trades page in the new style. Offer, result with rank and win chance, tap-to-add rosters ----------
R42_CSS = r'''  /* round 42 trades (news_logos.py) */
  .gx-stg { display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: 1px; background: var(--line); margin-top: 12px; }
  .gx-stc { background: var(--bg); padding: 10px 12px; min-width: 0; font-variant-numeric: tabular-nums; }
  .gx-stv { font-size: 20px; font-weight: 600; letter-spacing: -.01em; }
'''

# done markers and must-have strings of rounds 28 to 30 that lived inside the old trade builder; kept as comments
R42_KEEP = [
    '<Section title="Rosters"', '<Card label="Their lineup"', 'sideBox("You give", Gv, give, setGive)', "<TradeRanks s={s}", "{extra || null}",
    "waiver pickup</span>", "const sideBox = (lab, list, sel, set, extra)", "round 29: two result tiles only", 'data-r29="tiles"',
]

R42_BODY = r'''  const K = s.blend, today = todayISO();
  const others = s.teams.filter((t) => t.id !== s.me);
  const [partner, setPartner] = useState(initPartner || (others[0] || {}).id || "");
  const [give, setGive] = useState([]);
  const [get, setGet] = useState([]);
  const [pick, setPick] = useState({});
  const [edit, setEdit] = useState(-1);
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
  const fas = useMemo(() => s.players.filter((p) => p.ft === "fa" && p.prob > 0 && tv[p.id] > 0 && !goalieOut(p)).sort((a, b) => tv[b.id] - tv[a.id]).slice(0, 60), [tv]);
  const rep = useMemo(() => { const o = {}; ["F", "D", "G"].forEach((k) => { const l = s.players.filter((p) => p.ft === "fa" && p.p === k && p.prob > 0 && (p.proj !== false || p.gp > 0)).map(vv).sort((a, b) => b - a).slice(0, 5); o[k] = l.length ? l.reduce((a, b) => a + b, 0) / l.length : 0; }); return o; }, [s.players, K]);
  const pe = (p) => Math.max(0, vv(p) - (rep[p.p] || 0)) * gl(p);
  const Gv = mine.filter((p) => give.includes(p.id)), Rv = theirs.filter((p) => get.includes(p.id));
  const extra = Math.max(0, Gv.length - Rv.length), need = Math.max(0, Rv.length - Gv.length);
  const ready = Gv.length > 0 && Rv.length > 0;
  const myAfter0 = mine.filter((p) => !give.includes(p.id)).concat(Rv.map((p) => ({ ...p, ft: s.me })));
  // free agents for the spots you free: your choice, or the best one available
  const picks = [];
  for (let k = 0; k < extra; k++) {
    if (pick[k] === "none") { picks.push(null); continue; }
    let f = (pick[k] ? s.players.find((f) => f.ft === "fa" && f.id === pick[k]) : null) || null;
    if (!f) {
      const c = cnt(myAfter0.concat(picks.filter(Boolean))), short = ["F", "D", "G"].filter((x) => c[x] < mins[x]);
      f = fas.find((x) => !picks.some((y) => y && y.id === x.id) && (!short.length || short.includes(x.p))) || null;
    }
    picks.push(f);
  }
  const drops = need ? myAfter0.filter((p) => !p.ir && !get.includes(p.id)).sort((a, b) => pg(a) - pg(b)).slice(0, need) : [];
  const key = [partner, give.join(), get.join(), picks.map((f) => (f ? f.id : "-")).join(), drops.map((p) => p.id).join()].join("|");
  const res = useMemo(() => {
    if (!ready) return null;
    const dropIds = new Set(drops.map((p) => p.id)), got = picks.filter(Boolean).map((f) => ({ ...f, ft: s.me }));
    const after = myAfter0.filter((p) => !dropIds.has(p.id)).concat(got);
    const thAfter = theirs.filter((p) => !get.includes(p.id)).concat(Gv.map((p) => ({ ...p, ft: partner })));
    const my = horizonTotal(after, s, nR) - horizonTotal(mine, s, nR), th = horizonTotal(thAfter, s, nR) - horizonTotal(theirs, s, nR);
    const G = new Set(give), T = new Set(get), A = new Set(got.map((f) => f.id));
    const players = s.players.map((p) => (G.has(p.id) ? { ...p, ft: partner } : T.has(p.id) || A.has(p.id) ? { ...p, ft: s.me } : dropIds.has(p.id) ? { ...p, ft: "fa" } : p));
    const pos = (t) => ({ o: t.rows.findIndex((x) => x.t.id === s.me) + 1, ...(t.grpRank[s.me] || {}) });
    const keep = __LT, t2 = leagueTable({ ...s, players });
    __LT = keep;
    const rb = pos(leagueTable(s)), ra = pos(t2);
    const sN = nextWkS(s), hasOpp = sN && oppOf(sN.weeks[sN.wk] || {}, s.me);
    const wb = hasOpp ? winChance(sN) : null, wa = hasOpp ? winChance(sN, after) : null;
    const c = cnt(after);
    return { my, th, rb, ra, wb, wa, short: ["F", "D", "G"].filter((k) => c[k] < mins[k]) };
  }, [key, s.players, s.wk, K, window.__PMODE]);
  const sum = (l, f) => l.reduce((a, p) => a + f(p), 0);
  const peG = sum(Gv, pe), peR = sum(Rv, pe), theyThink = peR > 0 ? (peG - peR) / peR : 0;
  const toggle = (sel, set, id) => { set(sel.includes(id) ? sel.filter((x) => x !== id) : [...sel, id]); setPick({}); setEdit(-1); };
  const vd = !res ? null : res.my <= 0 ? ["Bad for you", "var(--bad)", "Your lineup gets worse."]
    : theyThink >= -0.05 ? ["Good trade", "var(--good)", "You gain, and it should look fair to them."]
    : ["Good for you, hard to sell", "var(--warn)", "You gain, but they would see it as a loss. Expect a counter-offer."];
  const GN = { F: "forwards", D: "defence", G: "goalies" };
  const grp = res ? ["F", "D", "G"].map((k) => [k, (res.rb[k] || 0) - (res.ra[k] || 0)]).sort((a, b) => Math.abs(b[1]) - Math.abs(a[1]))[0] : null;
  const arrow = (b, a, fmt, up) => <><span>{fmt(b)}</span><span className="text-slate-500" style={{ fontSize: 14, margin: "0 6px" }}>{"\u2192"}</span><span style={{ color: up > 0 ? "var(--good)" : up < 0 ? "var(--bad)" : "var(--ink)" }}>{fmt(a)}</span></>;
  const offerRow = (p, i, onX, note) => (
    <div key={p.id} className="gx-row" style={i ? null : { borderTop: 0 }}>
      <TeamLogo t={p.t} size={22} />
      <span className="min-w-0 truncate" style={{ flex: 1 }}><PN p={p} className="" />{note ? <span className="text-xs text-slate-500" style={{ marginLeft: 6 }}>{note}</span> : null}</span>
      <span className="text-slate-500" style={{ fontVariantNumeric: "tabular-nums" }}>{f1(pg(p))}</span>
      <button type="button" aria-label={"Remove " + p.n} className="text-slate-500" style={{ padding: "0 4px", fontSize: 16 }} onClick={onX}>{"\u00d7"}</button>
    </div>
  );
  const rosterRows = (list, sel, set, mySide) => [...list].sort((a, b) => (a.ir ? 1 : 0) - (b.ir ? 1 : 0) || order[a.p] - order[b.p] || pg(b) - pg(a)).map((p) => {
    const on = sel.includes(p.id), fl = tbFlags(p, K).find((f) => (mySide ? f.sell : !f.sell));
    return (
      <div key={p.id} role="button" className="gx-row" style={{ cursor: "pointer", padding: "8px 6px", background: on ? "var(--card3)" : "transparent", opacity: p.ir ? 0.5 : 1 }} onClick={() => toggle(sel, set, p.id)}>
        <TeamLogo t={p.t} size={22} />
        <span className="min-w-0 truncate" style={{ flex: 1 }}>
          <span className="m-hide">{p.n}</span><span className="m-inl">{shortN(p.n)}</span> <span className="text-xs text-slate-500">{p.p + (p.ir ? " \u00b7 IR" : "")}</span>
          {fl ? <span className="text-xs" style={{ marginLeft: 6, color: mySide ? "var(--warn)" : "var(--good)" }}>{mySide ? "sell high" : "buy low"}</span> : null}
        </span>
        <span style={{ fontVariantNumeric: "tabular-nums" }}>{f1(pg(p))}</span>
      </div>
    );
  });
  return (
    <div className="space-y-3">
      <div className="flex items-center gap-2">
        <span className="text-sm text-slate-500 whitespace-nowrap">Trade with</span>
        <select className={inp + " flex-1"} value={partner} onChange={(e) => { setPartner(e.target.value); setGet([]); setPick({}); setEdit(-1); }}>{others.map((t) => <option key={t.id} value={t.id}>{t.name}</option>)}</select>
        {give.length || get.length ? <button className="text-xs text-slate-500 underline whitespace-nowrap" onClick={() => { setGive([]); setGet([]); setPick({}); setEdit(-1); }}>Clear</button> : null}
      </div>
      <div className="tb-grid">
        <div className="gx-pn" style={{ minWidth: 0 }}><b></b><b></b><b></b><b></b>
          <div className="gx-tag" style={{ marginBottom: 4 }}>You give</div>
          {Gv.length ? Gv.map((p, i) => offerRow(p, i, () => toggle(give, setGive, p.id))) : <div className="text-sm text-slate-500">Tap your players below</div>}
        </div>
        <div className="gx-pn" style={{ minWidth: 0 }}><b></b><b></b><b></b><b></b>
          <div className="gx-tag" style={{ marginBottom: 4 }}>You get</div>
          {Rv.length ? Rv.map((p, i) => offerRow(p, i, () => toggle(get, setGet, p.id))) : <div className="text-sm text-slate-500">Tap their players below</div>}
          {picks.map((f, k) => (f ? offerRow(f, 1, () => { setPick((x) => ({ ...x, [k]: "none" })); setEdit(-1); },
            <>free agent <button type="button" className="text-blue-600" style={{ marginLeft: 6 }} onClick={(e) => { e.stopPropagation(); setEdit(edit === k ? -1 : k); }}>change</button></>)
            : ready ? <button key={"add" + k} type="button" className="text-xs text-blue-600" style={{ marginTop: 8 }} onClick={() => setPick((x) => ({ ...x, [k]: undefined }))}>Add a free agent to the open spot</button> : null))}
          {edit >= 0 && edit < extra ? <FaSearch s={s} top={fas} taken={new Set(picks.filter(Boolean).map((x) => x.id))} val={pg} onPick={(id) => { setPick((x) => ({ ...x, [edit]: id })); setEdit(-1); }} /> : null}
        </div>
      </div>
      {res && vd ? (
        <div className="gx-pn"><b></b><b></b><b></b><b></b>
          <div style={{ display: "flex", alignItems: "baseline", gap: 10, flexWrap: "wrap" }}>
            <span className="font-semibold" style={{ color: vd[1] }}>{vd[0]}</span>
            <span className="text-sm text-slate-500">{vd[2]}</span>
          </div>
          <div className="gx-stg">
            <div className="gx-stc"><div className="text-xs text-slate-500">Your lineup</div><div className="gx-stv" style={{ color: res.my >= 0 ? "var(--good)" : "var(--bad)" }}>{(res.my >= 0 ? "+" : "") + Math.round(res.my)}</div><div className="text-xs text-slate-500">points, rest of season</div></div>
            <div className="gx-stc"><div className="text-xs text-slate-500">Their lineup</div><div className="gx-stv" style={{ color: res.th >= 0 ? "var(--good)" : "var(--bad)" }}>{(res.th >= 0 ? "+" : "") + Math.round(res.th)}</div><div className="text-xs text-slate-500">points, rest of season</div></div>
            <div className="gx-stc"><div className="text-xs text-slate-500">Your league rank</div><div className="gx-stv">{arrow(res.rb.o, res.ra.o, ordN, res.rb.o - res.ra.o)}</div><div className="text-xs text-slate-500">{grp && grp[1] ? GN[grp[0]] + " " + ordN(res.rb[grp[0]]) + " \u2192 " + ordN(res.ra[grp[0]]) : "position ranks unchanged"}</div></div>
            {res.wb != null && res.wa != null ? <div className="gx-stc"><div className="text-xs text-slate-500">Next week</div><div className="gx-stv">{arrow(res.wb, res.wa, wpTxt, Math.round(res.wa * 100) - Math.round(res.wb * 100))}</div><div className="text-xs text-slate-500">chance to win</div></div> : null}
          </div>
          {res.short.length ? <div className="text-sm" style={{ marginTop: 10, color: "var(--bad)" }}>This leaves you short at {res.short.map((k) => GN[k]).join(" and ")}.</div> : null}
          {drops.length ? <div className="text-sm" style={{ marginTop: 10, color: "var(--warn)" }}>You would be over 22 players, so this counts {drops.map((p) => p.n).join(" and ")} as dropped.</div> : null}
        </div>
      ) : <div className="text-sm text-slate-500">Pick at least one player on each side to see the result.</div>}
      <div className="gx-pn"><b></b><b></b><b></b><b></b>
        <div style={{ display: "flex", alignItems: "baseline", marginBottom: 6 }}>
          <span className="gx-tag">Rosters</span>
          <span className="text-xs text-slate-500" style={{ marginLeft: "auto" }}>Tap a player to add or remove him</span>
        </div>
        <div className="tb-grid">
          <div className="min-w-0"><div className="text-xs text-slate-500 truncate" style={{ paddingBottom: 2 }}>{teamName(s, s.me)}</div>{rosterRows(mine, give, setGive, true)}</div>
          <div className="min-w-0"><div className="text-xs text-slate-500 truncate" style={{ paddingBottom: 2 }}>{teamName(s, partner)}</div>{rosterRows(theirs, get, setGet, false)}</div>
        </div>
      </div>
      <TradeAdvice s={s} onPick={(p) => { setPartner(p.ft); setGet(p.ft === partner ? [...get.filter((x) => x !== p.id), p.id] : [p.id]); setPick({}); setEdit(-1); window.scrollTo(0, 0); }} />
    </div>
  );
}

'''

R42_TRADE = ("function TradeBuilder({ s, initPartner }) {\n"
             "  // trades v42: offer, result and rosters in the new style (news_logos.py)\n"
             "  // older done markers kept so earlier rounds stay finished:\n"
             + "".join("  // " + m42 + "\n" for m42 in R42_KEEP) + R42_BODY)

R42_ADV_OLD = r'''<Section title="Trade advice" sub={"Your ranks: forwards #" + (g.F || "-") + ", defence #" + (g.D || "-") + ", goalies #" + (g.G || "-") + " of " + T.rows.length + "."}>'''
R42_ADV_NEW = r'''<Section title="Buy low" sub="Good players on other teams who are cold, unlucky or underrated.">'''
R42_PARA_PAT = (re.escape('<div>{weak !== strong && g[weak] > g[strong] ?') + r".*?"
                + re.escape('Sell high: {sell.map((p) => p.n).join(", ")}.</div> : null}'))


def round42(t):
    t = lit(t, "trades 2: styles", "</style>", R42_CSS + "</style>", "round 42 trades")
    t = block(t, "trades 2: new trade page", "function TradeBuilder({ s, initPartner }) {",
              "// ---------- round 14: My Team injuries + protected players", R42_TRADE, "trades v42")
    t = lit(t, "trades 2: buy-low box title", R42_ADV_OLD, R42_ADV_NEW, '<Section title="Buy low"')
    t = sub_once(t, "trades 2: rank paragraph removed", R42_PARA_PAT, "{/* round 42: rank paragraph removed */}", "round 42: rank paragraph removed", re.S)
    t = lit(t, "trades 2: buy-low list heading", '<div className="flex flex-wrap items-center gap-2 mt-4 mb-1">',
            '<div className="flex flex-wrap items-center gap-2 mb-1" data-r42="bl">', 'data-r42="bl"')
    for must in R42_KEEP + ["trades v42", "function TradeBuilder(", "function TradeAdvice(", "function FaSearch(", "function TradeRanks(", "<TradeAdvice s={s}", "<FaSearch s={s}",
                            'f.ft === "fa" && f.id === pick[k]', "tv[p.id] > 0 && !goalieOut(p)", "function MyInjProt("]:
        if must not in t:
            fail("fantasy-gm.html looks damaged after round 42 (" + must + ").")
    return t


_fix_before_r42 = fix


def fix(t):
    return round42(_fix_before_r42(t))

# ---------- round 43: Advice as four plain lists, Goalies with day buttons ----------
R43_CSS = r'''  /* round 43 advice and goalies (news_logos.py) */
  .gx-gl { display: grid; grid-template-columns: 26px minmax(0,1fr) 104px 44px 60px; gap: 8px; align-items: center; padding: 8px 0; border-top: 1px solid var(--line); font-variant-numeric: tabular-nums; }
  .gx-gl .n { text-align: right; }
  @media (max-width: 640px) { .gx-gl { grid-template-columns: 24px minmax(0,1fr) 92px 52px; gap: 6px; } }
'''

R43_HELPERS = r'''// ---------- round 43: Advice page, four plain lists (news_logos.py) ----------
function AdvicePage({ s, setS, wk }) {
  const K = s.blend;
  const [sim, setSim] = useState(null);
  const sP = useMemo(() => planS(s), [s]);
  const wkP = useMemo(() => (sP !== s ? deriveWeek(sP.weeks[sP.wk], sP.autoDone) : wk), [sP, wk]);
  const M = useMemo(() => (sim ? computeMoves(sP, { H: 1, pool: 40 }) : null), [sP, !!sim]);
  const base = useMemo(() => (sim ? planBase(s, sP) : null), [sP, !!sim]);
  const L = useMemo(() => {
    const mb = (p) => { const id = typeof p.id === "string" && p.id[0] === "e" ? p.id.slice(1) : null; return window.__MODEL && id ? (window.__MODEL.base || {})[id] : null; };
    const UP = { F1: "line 1", F2: "line 2", D1: "the top pair", D2: "the second pair" };
    const rise = (p) => {
      const g = sigOf(p), fr = formRatio(p, K), t = g.toi;
      if (g.lines && g.lines.chg === "up") return "Moved up to " + (UP[g.lines.grp] || "a bigger role");
      if (g.ppChg === "added") return "New on the top power play";
      if (t && t.d >= 90) return "More ice time: " + (t.d / 60).toFixed(1) + " more minutes a game";
      if (fr !== null && fr >= 1.25) return "Hot: " + f1(g.rec.ppg) + " a game over two weeks";
      if ((p.chg || 0) >= 5) return "Being picked up fast: +" + f1(p.chg) + "% of leagues";
      return "";
    };
    const under = (p) => {
      const m = mb(p), l = sigOf(p).luck;
      if (m != null && p.proj && p.avg > 0 && m - p.avg >= 1 && m / p.avg >= 1.15) return "Your model rates him " + f1(m - p.avg) + " above ESPN";
      if (l && l.t === "s" && l.d <= -2) return "Unlucky: " + l.g + " goal" + (l.g === 1 ? "" : "s") + " on " + l.sh + " shots";
      if (l && l.t === "g" && l.d <= -4) return "Unlucky: stopping fewer shots than he usually does";
      return "";
    };
    const sell = (p) => {
      const m = mb(p), l = sigOf(p).luck, fr = formRatio(p, K);
      if (m != null && p.proj && p.avg > 0 && p.avg - m >= 1 && m / p.avg <= 0.85) return "ESPN rates him higher than your model";
      if (l && l.t === "s" && l.d >= 2) return "Lucky: " + l.g + " goals on " + l.sh + " shots";
      if (l && l.t === "g" && l.d >= 4) return "Lucky: stopping more shots than he usually does";
      if (fr !== null && fr >= 1.3) return "Hot: " + f1(sigOf(p).rec.ppg) + " a game over two weeks";
      return "";
    };
    const watch = (p) => {
      const g = sigOf(p), fr = formRatio(p, K), t = g.toi;
      if (g.lines && g.lines.chg === "down") return "Moved down the lineup";
      if (g.ppChg === "removed") return "Off the top power play";
      if (t && t.d <= -90) return "Losing ice time: " + (Math.abs(t.d) / 60).toFixed(1) + " minutes less a game";
      if (fr !== null && fr <= 0.7) return "Cold: " + f1(g.rec.ppg) + " a game over two weeks";
      return "";
    };
    const pickL = (list, fn) => list.map((p) => ({ p, why: fn(p) })).filter((x) => x.why).sort((a, b) => effAvg(b.p, K) - effAvg(a.p, K)).slice(0, 6);
    const fa = s.players.filter((p) => p.ft === "fa" && p.prob > 0 && (p.proj !== false || p.gp > 0) && !goalieOut(p)), mine = s.players.filter((p) => p.ft === s.me && !p.ir);
    return { rise: pickL(fa, rise), under: pickL(fa, under), sell: pickL(mine, sell), watch: pickL(mine, watch) };
  }, [s.players, K, window.__PMODE, (window.ESPN_DATA || {}).generated]);
  const open = (p) => { const dr = dropFor(s, p); setSim({ add: p.id, drop: dr ? dr.id : "" }); };
  const list = (title, rows, fa, bad, empty) => (
    <GxPanel title={title}>
      {rows.length ? rows.map((x, i) => (
        <div key={x.p.id} className="gx-row" role={fa ? "button" : undefined} style={{ borderTop: i ? undefined : 0, cursor: fa ? "pointer" : "default" }} onClick={fa ? () => open(x.p) : undefined}>
          <TeamLogo t={x.p.t} size={22} />
          <div className="min-w-0" style={{ flex: 1 }}>
            <div className="truncate">{fa ? x.p.n : <PN p={x.p} className="" />} <span className="text-xs text-slate-500">{x.p.p}</span></div>
            <div className="text-xs truncate" style={{ color: bad ? "var(--bad)" : "var(--mute)" }}>{x.why}</div>
          </div>
          <span style={{ fontVariantNumeric: "tabular-nums" }}>{f1(effAvg(x.p, K))}</span>
        </div>
      )) : <div className="text-sm text-slate-500">{empty}</div>}
    </GxPanel>
  );
  return (
    <div className="space-y-3">
      <div className="grid md:grid-cols-2 gap-3">
        {list("Free agents on the rise", L.rise, true, false, "No free agent is clearly on the way up right now.")}
        {list("Better than they look", L.under, true, false, "Nobody stands out as underrated right now.")}
        {list("Your players to sell high", L.sell, false, false, "None of your players is at a peak right now.")}
        {list("Your players to watch", L.watch, false, true, "None of your players is slipping right now.")}
      </div>
      <div className="text-xs text-slate-500">The number is expected points a game. Tap a free agent to try the swap.</div>
      {sim && M ? <MoveSim s={sP} setS={setS} wk={wkP} M={M} H={1} hLabel={sP !== s ? "next week" : "rest of this week"} init={sim} wBase={base} onClose={() => setSim(null)} /> : null}
    </div>
  );
}

'''

# done markers of rounds 16 to 27 that lived inside the old goalie page; kept as comments
R43_KEEP = [
    "goalie streams v20", "gScore(gm.home.t, dt)", 'avail(p, dt) > 0 && gState(p.t, dt).s === "P" && dt >= pickStart(p)',
    ".slice(0, noMovesWk(s, wk) ? 0 : 3)", 'noMovesWk(s, wk) ? null : head("Free agents to stream")', "(noMovesWk(s, wk) ? null : <div",
    "so no free-agent streams are shown",
]

R43_GOALIE_BODY = r'''  const K = s.blend, today = todayISO(), dates = wk.dates || [];
  const first = dates.findIndex((x) => x >= today);
  const [day, setDay] = useState(null);
  const [all, setAll] = useState(false);
  const d = Math.max(0, Math.min(dates.length - 1, day != null ? day : first >= 0 ? first : dates.length - 1));
  const dt = dates[d];
  const noMv = noMovesWk(s, wk);
  const mineG = s.players.filter((p) => p.ft === s.me && p.p === "G" && !p.ir);
  const plays = (p, i) => (wk.games[p.t] || []).includes(i);
  const stat = (p, x) => {
    const g = gStart(p, x), l = (g.l || "").toLowerCase();
    if (l.includes("confirmed") && !l.includes("un")) return ["Confirmed", "var(--good)", false];
    if (l === "not starting" || l.indexOf("backup") === 0 || l.includes("rests") || g.v < 0.35) return [l.includes("rests") ? "Likely sitting" : "Backup", "var(--mute)", true];
    if (l.includes("likely") || g.v >= 0.8) return ["Likely", "var(--warn)", false];
    return ["Not confirmed", "var(--warn)", false];
  };
  const gameTxt = (p, x) => { const gm = gameOf(p.t, x); return gm ? (gm.h ? "vs " : "@ ") + gm.o + " \u00b7 " + gameTime(gm) : ""; };
  const mineOn = mineG.filter((p) => plays(p, d)), mineOff = mineG.filter((p) => !plays(p, d));
  const fas = !dt || noMv ? [] : s.players
    .filter((p) => p.ft === "fa" && p.p === "G" && plays(p, d) && avail(p, dt) > 0 && gState(p.t, dt).s === "P" && dt >= pickStart(p))
    .map((p) => { const gs = gStart(p, dt); return { p, gs, v: effAvg(p, K, dt) * gs.v }; })
    .filter((x) => x.gs.v >= 0.4).sort((a, b) => b.v - a.v).slice(0, 4);
  const raw = (window.ESPN_DATA || {}).goalies || s.goalies || {}, GD = (window.GAMES_DATA || {}).games || {};
  const games = !dt ? [] : Object.entries(GD[dt] || {}).filter(([, v]) => v.h === 1).map(([home, v]) => {
    const side = (t) => { const e = Object.entries(raw[dt] || {}).find(([, x]) => x && x.team === t); return { t, name: e ? e[0] : null, status: e ? String(e[1].status || "").toLowerCase() : "" }; };
    return { away: side(v.o), home: side(home), st: v.st };
  }).sort((a, b) => String(a.st || "").localeCompare(String(b.st || "")));
  const word = (x) => (!x.name ? "not announced" : x.status.includes("confirm") && !x.status.includes("un") ? "confirmed" : /likely|expected|project/.test(x.status) ? "likely" : "not confirmed");
  const head = (title) => (
    <div className="gx-gl text-xs text-slate-500" style={{ borderTop: 0, paddingTop: 0 }}>
      <span></span><span className="gx-tag">{title}</span><span className="n">Starting</span><span className="n m-hide">Win</span><span className="n">Expected</span>
    </div>
  );
  const line = (p, note) => {
    const live = gState(p.t, dt).s, o = oddsFor(p.t, dt), stt = stat(p, dt);
    const AD = actDay(s.me, dt), v = AD ? AD[String(p.id).slice(1)] : null, pts = live !== "P" && p.ft === s.me && v && v[0] != null ? v[0] : null;
    return (
      <div key={p.id} className="gx-gl">
        <TeamLogo t={p.t} size={24} />
        <div className="min-w-0"><div className="truncate"><PN p={p} className="" /></div><div className="text-xs text-slate-500 truncate">{[gameTxt(p, dt), note].filter(Boolean).join(" \u00b7 ")}</div></div>
        <span className="n text-sm" style={{ color: live !== "P" ? "var(--mute)" : stt[1] }}>{live === "F" ? "Final" : live === "L" ? "Live" : stt[0]}</span>
        <span className="n m-hide">{o ? Math.round(o.win * 100) + "%" : "\u2013"}</span>
        <span className="n" style={pts != null ? { fontWeight: 600, color: pts > 5 ? "var(--good)" : pts < 0 ? "var(--bad)" : "var(--ink)" } : null}>{pts != null ? f1(pts) : live === "P" && stt[2] ? "\u2013" : f1(effAvg(p, K, dt))}</span>
      </div>
    );
  };
  return (
    <div className="space-y-3">
      <div style={{ display: "grid", gridTemplateColumns: "repeat(" + Math.max(1, dates.length) + ", minmax(0,1fr))", gap: 6 }}>
        {dates.map((x, i) => {
          const n = mineG.filter((p) => plays(p, i) && avail(p, x) > 0 && gStart(p, x).v >= 0.5).length;
          return (
            <button key={x} type="button" onClick={() => { setDay(i); setAll(false); }} className={"gx-day" + (i === d ? " on" : "")}>
              <span className={"block text-xs " + (i === d ? "font-semibold" : "text-slate-500")}>{x === today ? "Today" : dayLabel(x).split(",")[0]}</span>
              <span className="block text-xs text-slate-500">{n ? n + " start" + (n === 1 ? "" : "s") : "\u2013"}</span>
            </button>
          );
        })}
      </div>
      <div className="gx-pn"><b></b><b></b><b></b><b></b>
        {head("Your goalies")}
        {mineOn.length ? mineOn.map((p) => line(p, "")) : <div className="text-sm text-slate-500" style={{ padding: "8px 0" }}>None of your goalies has a game on this day.</div>}
        {mineOn.length && mineOff.length ? <div className="text-xs text-slate-500" style={{ paddingTop: 8, borderTop: "1px solid var(--line)" }}>{mineOff.map((p) => p.n).join(" and ") + (mineOff.length === 1 ? " has" : " have") + " no game."}</div> : null}
      </div>
      <div className="gx-pn"><b></b><b></b><b></b><b></b>
        {head("Free agents starting")}
        {noMv ? <div className="text-sm text-slate-500" style={{ padding: "8px 0" }}>No moves left this week, so pickups are hidden.</div>
          : fas.length ? fas.map(({ p }) => { const dr = dropFor(s, p); return line(p, dr ? "swap for " + dr.n : ""); })
          : <div className="text-sm text-slate-500" style={{ padding: "8px 0" }}>{dt && dt < today ? "This day has passed." : "No free-agent goalie is likely to start this day."}</div>}
      </div>
      <div className="gx-pn"><b></b><b></b><b></b><b></b>
        <div role="button" className="flex items-center" style={{ cursor: "pointer" }} onClick={() => setAll(!all)}>
          <span style={{ flex: 1 }}>Every starter {dt === today ? "today" : dt ? "on " + dayLabel(dt).split(",")[0] : ""}</span>
          <span className="text-slate-500 text-sm">{games.length} game{games.length === 1 ? "" : "s"}</span>
          <span className={"sec-chev" + (all ? "" : " shut")} style={{ margin: "0 4px 2px 10px" }}></span>
        </div>
        {all ? (games.length ? games.map((gm, i) => (
          <div key={i} className="gx-row" style={{ marginTop: i ? 0 : 8 }}>
            <TeamLogo t={gm.away.t} size={22} />
            <div className="min-w-0" style={{ flex: 1 }}><div className="truncate">{gm.away.name || gm.away.t}</div><div className="text-xs text-slate-500">{word(gm.away)}</div></div>
            <span className="text-xs text-slate-500 whitespace-nowrap">{gameTime({ st: gm.st })}</span>
            <div className="min-w-0 text-right" style={{ flex: 1 }}><div className="truncate">{gm.home.name || gm.home.t}</div><div className="text-xs text-slate-500">{word(gm.home)}</div></div>
            <TeamLogo t={gm.home.t} size={22} />
          </div>
        )) : <div className="text-sm text-slate-500" style={{ paddingTop: 8 }}>No game times loaded for this day.</div>) : null}
      </div>
    </div>
  );
}

'''

R43_GOALIES = ("function GoalieStreams({ s, wk }) {\n"
               "  // goalies v43: day buttons, your goalies, free agents starting, every starter (news_logos.py)\n"
               "  // older done markers kept so earlier rounds stay finished:\n"
               + "".join("  // " + m43 + "\n" for m43 in R43_KEEP) + R43_GOALIE_BODY)


def round43(t):
    t = lit(t, "advice: styles", "</style>", R43_CSS + "</style>", "round 43 advice and goalies")
    t = lit(t, "advice: page takes the full app state", "function AdviceAll({ s }) {", "function AdviceAll(props) {", "function AdviceAll(props) {")
    t = lit(t, "advice: four plain lists", 'return <div className="space-y-4"><AdvicePanel s={s} /><EdgesPanel s={s} /></div>;',
            "return <AdvicePage {...props} />;", "<AdvicePage {...props} />")
    t = block(t, "advice: new Goalies page", "function GoalieStreams({ s, wk }) {", "// ---------- moves used from ESPN (news_logos.py) ----------", R43_GOALIES, "goalies v43")
    t = lit(t, "advice: helpers", ROOT, R43_HELPERS + ROOT, "function AdvicePage(")
    for must in R43_KEEP + ["goalies v43", "function GoalieStreams(", "function AdvicePage(", "function AdvicePanel(", "function EdgesPanel(", "function movesUsedESPN(",
                            "function MoveSim(", "const dropFor =", "const GxPanel ="]:
        if must not in t:
            fail("fantasy-gm.html looks damaged after round 43 (" + must + ").")
    return t


_fix_before_r43 = fix


def fix(t):
    return round43(_fix_before_r43(t))

# ---------- round 44: League page (one table, this week, playoff schedule) and Setup page; five plain tabs ----------
R44_CSS = r'''  /* round 44 league and setup (news_logos.py) */
  .gx-lt { display: grid; grid-template-columns: 24px minmax(0,1fr) 52px 60px 68px 100px; gap: 8px; align-items: center; padding: 8px 0; border-top: 1px solid var(--line); font-variant-numeric: tabular-nums; }
  .gx-lt .n, .gx-lm .n { text-align: right; }
  .gx-lt.cut { border-top: 1px dashed var(--faint); }
  .gx-lm { display: grid; grid-template-columns: minmax(0,1fr) 54px 40px minmax(50px,1.2fr) 40px 54px minmax(0,1fr); gap: 8px; align-items: center; padding: 9px 0; border-top: 1px solid var(--line); font-variant-numeric: tabular-nums; cursor: pointer; }
  .gx-seg { display: inline-flex; border: 1px solid var(--line2); border-radius: 8px; overflow: hidden; }
  .gx-seg button { padding: 5px 11px; font-size: 13px; color: var(--mute); border-left: 1px solid var(--line2); }
  .gx-seg button:first-child { border-left: 0; }
  .gx-seg button.on { background: var(--ink); color: var(--on); font-weight: 600; }
  .gx-seg button:disabled { opacity: .4; }
  .gx-sr { display: flex; align-items: center; gap: 10px; flex-wrap: wrap; padding: 10px 0; border-top: 1px solid var(--line); }
  .gx-sr > :last-child { margin-left: auto; }
  .gx-lk { display: flex; align-items: center; width: 100%; text-align: left; padding: 11px 0; border-top: 1px solid var(--line); color: var(--ink); }
  @media (max-width: 640px) { .gx-lt { grid-template-columns: 20px minmax(0,1fr) 44px 88px; } .gx-lm { grid-template-columns: minmax(0,1fr) 36px 50px 36px minmax(0,1fr); } }
'''

R44_TOPBAR = r'''function TopBar({ s, setS, tab, go, ageH }) {
  // top bar v44: five plain tabs, Setup is a page (news_logos.py)
  // older done markers kept: className={"gx-tab" + ((tab === k || (k === "myteam" && (tab === "moves" || tab === "lines")))
  // older done markers kept: {"Setup"}</button>
  const [rank, setRank] = useState(null);
  useEffect(() => {
    const id = setTimeout(() => { try { const T = leagueTable(s), i = T.rows.findIndex((x) => x.t.id === s.me); setRank(i >= 0 ? [i + 1, T.rows.length] : null); } catch (e) {} }, 400);
    return () => clearTimeout(id);
  }, [s.players, s.wk, s.blend, window.__PMODE]);
  const name = teamName(s, s.me) || "My team";
  const sync = s.lastSync ? toDate(s.lastSync) : null;
  const TABS = [["today", "Today", ["today"]], ["matchup", "Matchup", ["matchup"]], ["myteam", "Team", ["myteam", "moves", "lines"]], ["league", "League", ["league", "teams"]], ["setup", "Setup", ["setup", "news"]]];
  return (
    <div className="m-hide max-w-6xl mx-auto px-3 flex items-end gap-1" style={{ paddingTop: 10 }}>
      <span className="gx-badge">{(name[0] || "K").toUpperCase()}</span>
      <span style={{ margin: "0 14px 10px 8px", lineHeight: 1.2, minWidth: 0 }}>
        <span className="block font-semibold truncate" style={{ maxWidth: 180 }}>{name}</span>
        <span className="block text-xs text-slate-500">{rank ? ordN(rank[0]) + " of " + rank[1] : s.league || "\u00a0"}</span>
      </span>
      {TABS.map(([k, l, grp]) => <button key={k} onClick={() => go(k, k === "setup" ? "settings" : k === "league" ? "power" : undefined)} className={"gx-tab" + (grp.indexOf(tab) >= 0 ? " on" : "")}>{l}</button>)}
      <span className="ml-auto text-xs text-slate-500 whitespace-nowrap" style={{ marginBottom: 12 }} title={s.lastSync ? "Synced " + fmtTime(s.lastSync) : ""}>
        <span style={{ display: "inline-block", width: 6, height: 6, borderRadius: 99, marginRight: 6, verticalAlign: 1, background: !s.lastSync ? "var(--faint)" : ageH !== null && ageH > 2 ? "var(--bad)" : "var(--good)" }}></span>
        {sync ? "Synced " + sync.toLocaleTimeString([], { hour: "numeric", minute: "2-digit" }) : "Not synced yet"}
      </span>
    </div>
  );
}
'''

R44_HELPERS = r'''// ---------- round 44: League page and Setup page (news_logos.py) ----------
// playoff odds for every team: 2,000 simulated seasons from each team's strength and the real schedule
function leagueSim(s) {
  const ids = s.teams.map((t) => t.id);
  if (ids.length < 2) return null;
  const T = leagueTable(s), str = {}, K = s.blend, today = todayISO();
  T.rows.forEach((x) => (str[x.t.id] = x.strength));
  const end = Math.min(s.weeks.length, s.poStart ?? 24), w0 = {}, pf = {}, todo = [];
  ids.forEach((id) => { w0[id] = 0; pf[id] = 0; });
  s.weeks.slice(0, end).forEach((w) => {
    const len = (w.dates || []).length, pairs = (w.pairs || []).filter((p) => p[0] && p[1] && w0[p[0]] != null && w0[p[1]] != null);
    if (!len || !pairs.length) return;
    if (effDone(w, s.autoDone) >= len) {
      pairs.forEach(([a, b]) => {
        const x = +((w.act || {})[a]) || 0, y = +((w.act || {})[b]) || 0;
        if (!x && !y) return;
        pf[a] += x; pf[b] += y;
        if (x > y) w0[a]++; else if (y > x) w0[b]++; else { w0[a] += 0.5; w0[b] += 0.5; }
      });
      return;
    }
    const live = w.dates[0] <= today ? deriveWeek(w, s.autoDone) : null;
    pairs.forEach(([a, b]) => {
      let p;
      if (live) {
        const R = (id) => weekLive(s.players.filter((q) => q.ft === id), live, K, id), act = (id) => +((live.act || {})[id]) || 0;
        p = winProb(R(a), R(b), act(a), act(b));
      } else p = normCdf((((str[a] || 0) - (str[b] || 0)) * (len / 7)) / (80 * Math.sqrt(len / 7)));
      pf[a] += (str[a] || 0) * (len / 7); pf[b] += (str[b] || 0) * (len / 7);
      todo.push([a, b, Math.max(0.02, Math.min(0.98, p))]);
    });
  });
  let seed = 20262027;
  const rnd = () => { seed = (seed + 0x6d2b79f5) | 0; let t = Math.imul(seed ^ (seed >>> 15), 1 | seed); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
  const N = 2000, cut = Math.min(6, ids.length - 1), inN = {};
  ids.forEach((id) => (inN[id] = 0));
  for (let k = 0; k < N; k++) {
    const w = Object.assign({}, w0);
    for (let j = 0; j < todo.length; j++) { const m = todo[j]; if (rnd() < m[2]) w[m[0]]++; else w[m[1]]++; }
    const order = ids.slice().sort((a, b) => w[b] - w[a] || pf[b] - pf[a]);
    for (let r = 0; r < cut; r++) inN[order[r]]++;
  }
  const out = {};
  ids.forEach((id) => (out[id] = inN[id] / N));
  return { odds: out, cut };
}
function LeaguePage({ s, wk, go }) {
  const K = s.blend, gen = (window.ESPN_DATA || {}).generated;
  const [by, setBy] = useState("st");
  const [sim, setSim] = useState(null);
  const T = leagueTable(s);
  useEffect(() => {
    const id = setTimeout(() => { try { setSim(leagueSim(s)); } catch (e) { setSim(null); } }, 500);
    return () => clearTimeout(id);
  }, [s.players, s.weeks, s.wk, s.blend, window.__PMODE]);
  const wins = (x) => x.rec.w + x.rec.t / 2;
  const stand = [...T.rows].sort((a, b) => wins(b) - wins(a) || b.rec.pf - a.rec.pf || b.strength - a.strength);
  const list = by === "st" ? stand : T.rows;
  const cut = sim ? sim.cut : 6;
  const myOpp = oppOf(wk, s.me);
  const all = [[s.me, myOpp || s.opp]].concat((wk.pairs || []).filter((p) => p[0] && p[1] && p[0] !== s.me && p[1] !== s.me)).filter((p) => p[0] && p[1]);
  const games = useMemo(() => all.map(([a, b]) => {
    const R = (id) => weekLive(s.players.filter((p) => p.ft === id), wk, K, id), act = (id) => +((wk.act || {})[id]) || 0;
    return { a, b, sa: act(a), sb: act(b), p: winProb(R(a), R(b), act(a), act(b)) };
  }), [s.players, wk, K, gen, s.opp]);
  return (
    <div className="space-y-3">
      <div className="gx-pn"><b></b><b></b><b></b><b></b>
        <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 8 }}>
          <span className="gx-tag">League table</span>
          <span className="gx-seg" style={{ marginLeft: "auto" }}>
            <button type="button" className={by === "st" ? "on" : ""} onClick={() => setBy("st")}>Standings</button>
            <button type="button" className={by === "pw" ? "on" : ""} onClick={() => setBy("pw")}>Strength</button>
          </span>
        </div>
        <div className="gx-lt text-xs text-slate-500" style={{ borderTop: 0, paddingTop: 0 }}><span></span><span></span><span className="n">Record</span><span className="n m-hide">Points</span><span className="n m-hide">Strength</span><span className="n">Playoffs</span></div>
        {list.map((x, i) => {
          const me = x.t.id === s.me, od = sim ? sim.odds[x.t.id] : null;
          return (
            <div key={x.t.id} className={"gx-lt" + (by === "st" && i === cut ? " cut" : "") + (me ? " font-semibold" : "")}>
              <span className="text-slate-500" style={{ fontWeight: 400 }}>{i + 1}</span>
              <span className="truncate"><TL s={s} id={x.t.id} /></span>
              <span className="n">{x.rec.n ? x.rec.w + "-" + x.rec.l + (x.rec.t ? "-" + x.rec.t : "") : "\u2013"}</span>
              <span className="n m-hide">{x.rec.n ? Math.round(x.rec.pf) : "\u2013"}</span>
              <span className="n m-hide">{Math.round(x.strength)}</span>
              <span className="n">{od == null ? "\u2026" : <><span style={{ display: "inline-block", width: 38, height: 4, background: "var(--track)", verticalAlign: "middle", marginRight: 6 }}><span style={{ display: "block", height: 4, width: Math.round(od * 100) + "%", background: od >= 0.5 ? "var(--good)" : "var(--bad)" }}></span></span>{wpTxt(od)}</>}</span>
            </div>
          );
        })}
        <div className="text-xs text-slate-500" style={{ paddingTop: 10, borderTop: "1px solid var(--line)" }}>{by === "st" ? "The dashed line is the playoff cut. " : ""}Strength is projected points a week from here on. Tap a team for its roster and how it matches up with yours.</div>
      </div>
      <div className="gx-pn"><b></b><b></b><b></b><b></b>
        <div className="gx-tag" style={{ marginBottom: 4 }}>This week</div>
        {games.length ? games.map((g, i) => {
          const la = g.p >= 0.5;
          return (
            <div key={g.a + "-" + g.b} className="gx-lm" role="button" style={i ? null : { borderTop: 0 }} onClick={() => { window.__MATCH_SEL = i; go("matchup"); }}>
              <span className={"truncate" + (g.a === s.me ? " font-semibold" : "")}>{teamName(s, g.a)}</span>
              <span className="n m-hide">{f1(g.sa)}</span>
              <span className="n" style={{ color: la ? "var(--good)" : "var(--bad)" }}>{wpTxt(g.p)}</span>
              <span style={{ display: "flex", height: 4, gap: 2 }}><i style={{ display: "block", width: Math.round(g.p * 100) + "%", background: la ? "var(--good)" : "var(--bad)" }}></i><i style={{ display: "block", flex: 1, background: la ? "var(--bad)" : "var(--good)" }}></i></span>
              <span style={{ color: la ? "var(--bad)" : "var(--good)" }}>{wpTxt(1 - g.p)}</span>
              <span className="m-hide">{f1(g.sb)}</span>
              <span className="truncate text-right">{teamName(s, g.b)}</span>
            </div>
          );
        }) : <div className="text-sm text-slate-500">No matchups loaded for this week.</div>}
        {games.length ? <div className="text-xs text-slate-500" style={{ paddingTop: 8, borderTop: "1px solid var(--line)" }}>Tap a matchup to open it on the Matchup page.</div> : null}
      </div>
      <button type="button" className="gx-lk" onClick={() => go("league", "playoffs")}>
        <span>Playoff schedule</span><span className="text-sm text-slate-500" style={{ marginLeft: 8 }}>who has the most games in the playoff weeks</span>
        <span className="sec-chev shut" style={{ margin: "0 4px 0 auto" }}></span>
      </button>
    </div>
  );
}
function SetupPage({ s, setS, go }) {
  const E = window.ESPN_DATA, K = s.blend, Sg = E && E.signals;
  const [msg, setMsg] = useState("");
  const theme = window.__themePref ? window.__themePref() : "auto";
  const seg = (items, value, onPick) => <span className="gx-seg">{items.map(([k, l, off]) => <button key={k} type="button" disabled={!!off} className={value === k ? "on" : ""} onClick={() => onPick(k)}>{l}</button>)}</span>;
  const num = (k, v, fb) => setS((st) => ({ ...st, [k]: isNaN(parseFloat(v)) ? fb : parseFloat(v) }));
  const roster = s.players.filter((p) => p.ft === s.me && !p.ir).sort((a, b) => effAvg(b, K) - effAvg(a, K));
  const top = s.protectTop ?? 8, autoIds = new Set(roster.slice(0, top).map((p) => p.id));
  const kept = roster.filter((p) => p.keep && !autoIds.has(p.id)), addable = roster.filter((p) => !p.keep && !autoIds.has(p.id));
  const keep = (id, v) => setS((st) => ({ ...st, players: st.players.map((p) => (p.id === id ? { ...p, keep: v } : p)) }));
  const src = [["ESPN league", !!E], ["GM model", !!(E && E.model)], ["betting lines", !!(E && E.model && E.model.odds && Object.keys(E.model.odds).length)], ["recent form", !!(Sg && Sg.recent)],
    ["power-play units", !!(Sg && Sg.pp1)], ["news", !!(Sg && Sg.news)], ["injuries", !!(Sg && Sg.injuries)], ["starting goalies", !!(E && E.goalies)]];
  const bad = src.filter((x) => !x[1]).map((x) => x[0]);
  const genAt = E && toDate(E.generated), old = genAt ? (Date.now() - genAt.getTime()) / 36e5 > 2 : true;
  const download = () => { const blob = new Blob([JSON.stringify(s)], { type: "application/json" }); const a = document.createElement("a"); a.href = URL.createObjectURL(blob); a.download = "fantasy-gm-backup-" + todayISO() + ".json"; a.click(); setMsg("Backup downloaded."); };
  const upload = (e) => { const f = e.target.files && e.target.files[0]; if (!f) return; const r = new FileReader(); r.onload = () => { try { const v = JSON.parse(r.result); if (v.players && v.weeks) { setS(migrate(v)); setMsg("Backup restored."); } else setMsg("That file isn't a backup."); } catch (ex) { setMsg("Couldn't read that file."); } }; r.readAsText(f); };
  const newsN = s.players.filter((p) => p.ft === s.me && newsOf(p).length).length;
  const link = (label, note, fn) => (
    <button type="button" className="gx-lk" onClick={fn}>
      <span>{label}</span>{note ? <span className="text-sm text-slate-500" style={{ marginLeft: 8 }}>{note}</span> : null}
      <span className="sec-chev shut" style={{ margin: "0 4px 0 auto" }}></span>
    </button>
  );
  const box = inp + " text-sm";
  return (
    <div className="space-y-3">
      <div className="gx-pn"><b></b><b></b><b></b><b></b>
        <div className="gx-tag">Display</div>
        <div className="gx-sr" style={{ borderTop: 0 }}><span>Theme</span>{seg([["auto", "Automatic"], ["light", "Light"], ["dark", "Dark"]], theme, (k) => window.__setTheme && window.__setTheme(k))}</div>
        <div className="gx-sr"><span>Projections</span>{seg([["espn", "ESPN"], ["blend", "Blend", !window.__MODEL], ["model", "GM model", !window.__MODEL], ["ai", "AI", !window.__MODEL || !window.__AI]], window.__PMODE, (k) => setS({ ...s, pmode: k, players: [...s.players] }))}</div>
        <div className="gx-sr"><span>Week on screen</span><select className={box} value={s.wk} onChange={(e) => setS({ ...s, wk: +e.target.value })}>{s.weeks.map((w, i) => <option key={i} value={i}>{w.label}</option>)}</select></div>
      </div>
      <div className="gx-pn"><b></b><b></b><b></b><b></b>
        <div className="gx-tag">Pickup rules</div>
        <div className="gx-sr" style={{ borderTop: 0 }}><span>A move must add at least</span><span><input type="number" step="0.5" className={box + " w-20"} value={s.minGain ?? 3} onChange={(e) => num("minGain", e.target.value, 3)} /> points</span></div>
        <div className="gx-sr"><span>Never suggest dropping my top</span><span><select className={box} value={top} onChange={(e) => setS((st) => ({ ...st, protectTop: +e.target.value }))}>{[...Array(13)].map((_, n) => <option key={n} value={n}>{n}</option>)}</select> players</span></div>
        <div className="gx-sr"><span>Also protect</span>
          <span className="flex flex-wrap gap-2 items-center justify-end">
            {kept.map((p) => <span key={p.id} className="inline-flex items-center gap-1 px-2 py-1 rounded-full border border-slate-300 text-xs">{p.n}<button type="button" aria-label={"Stop protecting " + p.n} className="text-slate-500" style={{ fontSize: 14, lineHeight: 1 }} onClick={() => keep(p.id, false)}>{"\u00d7"}</button></span>)}
            {addable.length ? <select className={box} value="" onChange={(e) => { if (e.target.value) keep(e.target.value, true); }}><option value="">+ add a player</option>{addable.map((p) => <option key={p.id} value={p.id}>{p.n + " (" + p.p + ")"}</option>)}</select> : null}
          </span>
        </div>
        <div className="gx-sr"><span>Always keep at least</span>
          <span className="flex gap-2 items-center">
            <input type="number" className={box + " w-14"} value={s.minF ?? 10} onChange={(e) => num("minF", e.target.value, 10)} /> F
            <input type="number" className={box + " w-14"} value={s.minD ?? 5} onChange={(e) => num("minD", e.target.value, 5)} /> D
            <input type="number" className={box + " w-14"} value={s.minGo ?? 2} onChange={(e) => num("minGo", e.target.value, 2)} /> G
          </span>
        </div>
      </div>
      <div className="gx-pn"><b></b><b></b><b></b><b></b>
        <div className="gx-tag">Data</div>
        <div className="gx-sr" style={{ borderTop: 0 }}>
          <span><span style={{ display: "inline-block", width: 7, height: 7, borderRadius: 99, marginRight: 8, background: !E ? "var(--faint)" : old ? "var(--bad)" : "var(--good)" }}></span>{E ? "Synced " + fmtTime(E.generated) : "No data file found"}</span>
          <span className="text-sm" style={{ color: bad.length ? "var(--bad)" : "var(--mute)" }}>{bad.length ? "Not working: " + bad.join(", ") : "all " + src.length + " sources working"}</span>
        </div>
        <div className="gx-sr"><span>Your settings on this device</span>
          <span className="flex gap-2 items-center">
            <button type="button" className="border border-slate-300 rounded-lg px-3 py-1 text-sm" onClick={download}>Download backup</button>
            <label className="border border-slate-300 rounded-lg px-3 py-1 text-sm cursor-pointer">Restore<input type="file" accept=".json,application/json" className="hidden" onChange={upload} /></label>
          </span>
        </div>
        {msg ? <div className="text-xs" style={{ color: "var(--good)", paddingTop: 6 }}>{msg}</div> : null}
      </div>
      <div>
        {link("News", newsN ? newsN + " on your players" : "", () => go("news"))}
        {link("Betting lines", "", () => go("setup", "odds"))}
        {link("Phone alerts", "what was sent to your phone", () => go("setup", "alerts"))}
        {link("Schedule", "games per NHL team this week", () => go("setup", "sched"))}
        {link("Injury return dates", "", () => go("setup", "inj"))}
        {link("Edit players", "", () => go("setup", "bulk"))}
        {link("Advanced settings", "team names, projection weight, reset", () => go("setup", "adv"))}
        <a className="gx-lk" href="ai-dashboard.html"><span>AI Lab</span><span className="sec-chev shut" style={{ margin: "0 4px 0 auto" }}></span></a>
      </div>
    </div>
  );
}

'''

R44_SUB_OLD = r'''if (!team) return nav && nav[2] ? <div className="mb-4"><Pills items={nav[2]} value={sub} onChange={(v) => setSubs((x) => ({ ...x, [tab]: v }))} /></div> : null;'''
R44_SUB_NEW = r'''if (!team) {
    const back = tab === "news" || (tab === "setup" && sub && sub !== "settings") ? ["Setup", () => go("setup", "settings")] : tab === "league" && sub === "playoffs" ? ["League", () => go("league", "power")] : null;
    return back ? <div className="mb-3"><button type="button" className="text-sm text-blue-600" onClick={back[1]}>{"\u2039 Back to " + back[0]}</button></div> : null;
  }'''
R44_MGRP_OLD = r'''tabBtn(k, l, (tab === k || (k === "myteam" && (tab === "moves" || tab === "lines"))) && !menu, () => pick(k))'''
R44_MGRP_NEW = r'''tabBtn(k, l, (tab === k || (k === "myteam" && (tab === "moves" || tab === "lines"))) && !menu || (k === "league" && tab === "teams"), () => (k === "league" ? (setMenu(false), setOpts(false), go("league", "power")) : pick(k)))'''
R44_MMORE_OLD = r'''{tabBtn("more", more ? more[1] : "Setup", !!more || menu, () => { setMenu(!menu); setOpts(false); })}'''
R44_MMORE_NEW = r'''{tabBtn("setup", "Setup", tab === "setup" || tab === "news", () => { setMenu(false); setOpts(false); go("setup", "settings"); })}{/* older marker kept: more ? more[1] : "Setup", */}'''


def round44(t):
    t = lit(t, "league: styles", "</style>", R44_CSS + "</style>", "round 44 league and setup")
    t = block(t, "league: five plain tabs", "function TopBar({ s, setS, tab, go, ageH }) {", "const GxRing = ({ v, big }) => {", R44_TOPBAR, "top bar v44")
    t = lit(t, "league: phone League tab lights up", R44_MGRP_OLD, R44_MGRP_NEW, '|| (k === "league" && tab === "teams")')
    t = lit(t, "league: phone Setup tab", R44_MMORE_OLD, R44_MMORE_NEW, 'tabBtn("setup", "Setup", tab === "setup"')
    t = lit(t, "league: back links in place of sub-menus", R44_SUB_OLD, R44_SUB_NEW, '"\\u2039 Back to " + back[0]')
    t = lit(t, "league: playoffs leaves Pickups", 'const PICK_SUBS = [["adddrop", "Pickups"], ["advice", "Advice"], ["goalies", "Goalies"], ["playoffs", "Playoffs"]];',
            'const PICK_SUBS = [["adddrop", "Pickups"], ["advice", "Advice"], ["goalies", "Goalies"]];', '["goalies", "Goalies"]];')
    t = lit(t, "league: new League page", 'sub === "odds" ? <OddsBoard s={s} /> : sub === "standings" ? <League {...P} /> : <PowerRankings {...P} />;',
            'sub === "playoffs" ? <PlayoffPlanner {...P} /> : <LeaguePage {...P} />;', "<LeaguePage {...P} />")
    t = lit(t, "league: new Setup page", 'sub === "inj" ? <InjuryPanel {...P} /> : <Settings {...P} />;',
            'sub === "inj" ? <InjuryPanel {...P} /> : sub === "odds" ? <OddsBoard s={s} /> : sub === "alerts" ? <PhoneFeed /> : sub === "adv" ? <Settings {...P} /> : <SetupPage {...P} />;',
            "<SetupPage {...P} />")
    t = lit(t, "league: open a chosen matchup", "const [sel, setSel] = useState(0);",
            "const [sel, setSel] = useState(() => { const v44 = window.__MATCH_SEL || 0; window.__MATCH_SEL = 0; return v44; });", "window.__MATCH_SEL || 0")
    t = lit(t, "league: helpers", ROOT, R44_HELPERS + ROOT, "function LeaguePage(")
    for must in ("top bar v44", "function TopBar(", "const GxRing =", "function LeaguePage(", "function SetupPage(", "function leagueSim(", "function SubBar(", "function Settings(",
                 "function PlayoffPlanner(", 'className={"gx-tab" + ((tab === k || (k === "myteam"', '{"Setup"}</button>', 'more ? more[1] : "Setup",', "matchup v35",
                 '["myteam", "Team"], ["league", "League"]];', 'const GX_MORE = [["setup", "Settings"]'):
        if must not in t:
            fail("fantasy-gm.html looks damaged after round 44 (" + must + ").")
    return t


_fix_before_r44 = fix


def fix(t):
    return round44(_fix_before_r44(t))

# ---------- round 45: phone fit for every page; phone header is just the tabs; Trades stacks on a phone; logos on Today's suggestion ----------
R45_CSS = r'''  /* round 45 phone fit (news_logos.py) */
  button:focus-visible, a:focus-visible, [role="button"]:focus-visible, select:focus-visible, input:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
  @media (prefers-reduced-motion: reduce) { * { transition: none !important; animation: none !important; scroll-behavior: auto !important; } }
  .gx-pl { display: inline-flex; align-items: center; gap: 6px; vertical-align: middle; }
  .m-seg { display: none; }
  @media (max-width: 640px) {
    html, body { overflow-x: hidden; }
    body { font-size: 14px; padding-bottom: 76px; }
    div:has(> .grid.grid-cols-6.mt-1) > div:has(select) { display: none !important; }
    .grid.grid-cols-6.mt-1 { margin-top: 0; }
    .gx-pn { min-width: 0; }
    .gx-hero { gap: 8px; padding: 8px 0 4px; }
    .gx-hero .gx-ring { width: 100px !important; height: 100px !important; }
    .gx-hero .gx-ring > div > div:first-child { font-size: 24px !important; }
    .gx-num { font-size: 24px; }
    .navscroll > button { padding-left: 11px; padding-right: 11px; font-size: 13px; }
    .gx-roh > span { min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
    .gx-ps .truncate, .gx-pk .text-xs.truncate, .gx-gl .text-xs.truncate { white-space: normal; }
    .gx-day { padding-left: 1px; padding-right: 1px; }
    .gx-row button[aria-label] { min-width: 36px; min-height: 40px; }
    .gx-seg button { min-height: 40px; padding: 5px 9px; }
    .gx-lk { min-height: 44px; padding: 12px 0; }
    .gx-sr { gap: 8px; }
    .gx-sr > :last-child { max-width: 100%; }
    .gx-st { font-size: 14px; }
    .gx-stv { font-size: 18px; }
    .tb-grid { grid-template-columns: minmax(0, 1fr); }
    .m-seg { display: inline-flex; max-width: 100%; }
    .m-seg button { max-width: 150px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
    body .lt-rink { padding: 2px 8px 10px; }
    body .lt-ps { font-size: 10px; }
    body .lt-pc { padding: 7px 8px; }
  }
'''

R45_HELPERS = r'''// ---------- round 45: tappable rows work from the keyboard too (news_logos.py) ----------
(function gxA11y() {
  if (window.__gxA11y) return;
  window.__gxA11y = 1;
  const fix = () => document.querySelectorAll('[role="button"]:not([tabindex])').forEach((el) => el.setAttribute("tabindex", "0"));
  let q = 0;
  try {
    new MutationObserver(() => { if (q) return; q = requestAnimationFrame(() => { q = 0; fix(); }); }).observe(document.documentElement, { childList: true, subtree: true });
  } catch (e) {}
  document.addEventListener("keydown", (e) => {
    const el = document.activeElement;
    if (e.defaultPrevented || !(e.key === "Enter" || e.key === " ")) return;
    if (el && el.getAttribute && el.getAttribute("role") === "button" && el.tagName !== "BUTTON") { e.preventDefault(); el.click(); }
  });
})();

'''

R45_OFFER_OLD = r'''<span className="min-w-0 truncate" style={{ flex: 1 }}><PN p={p} className="" />{note ? <span className="text-xs text-slate-500" style={{ marginLeft: 6 }}>{note}</span> : null}</span>'''
R45_OFFER_NEW = r'''<span className="min-w-0" style={{ flex: 1 }}><span className="block truncate"><PN p={p} className="" /></span>{note ? <span className="block text-xs text-slate-500">{note}</span> : null}</span>'''
R45_TAP_OLD = r'''<span className="text-xs text-slate-500" style={{ marginLeft: "auto" }}>Tap a player to add or remove him</span>'''
R45_TAP_NEW = (r'''<span className="text-xs text-slate-500 m-hide" style={{ marginLeft: "auto" }}>Tap a player to add or remove him</span>'''
               r'''<span className="gx-seg m-seg" style={{ marginLeft: "auto" }}><button type="button" className={side === "me" ? "on" : ""} onClick={() => setSide("me")}>{teamName(s, s.me)}</button>'''
               r'''<button type="button" className={side === "them" ? "on" : ""} onClick={() => setSide("them")}>{teamName(s, partner)}</button></span>''')
R45_COL1_OLD = r'''<div className="min-w-0"><div className="text-xs text-slate-500 truncate" style={{ paddingBottom: 2 }}>{teamName(s, s.me)}</div>'''
R45_COL1_NEW = r'''<div className={"min-w-0" + (side === "me" ? "" : " m-hide")}><div className="text-xs text-slate-500 truncate m-hide" style={{ paddingBottom: 2 }}>{teamName(s, s.me)}</div>'''
R45_COL2_OLD = r'''<div className="min-w-0"><div className="text-xs text-slate-500 truncate" style={{ paddingBottom: 2 }}>{teamName(s, partner)}</div>'''
R45_COL2_NEW = r'''<div className={"min-w-0" + (side === "them" ? "" : " m-hide")}><div className="text-xs text-slate-500 truncate m-hide" style={{ paddingBottom: 2 }}>{teamName(s, partner)}</div>'''


def r45_today_logos(t):
    if 'className="gx-pl"' in t:
        print("(news) phone fit: logos on Today's suggestion: already done")
        return t
    m = t.find("today v32")
    a = t.rfind("function Today(", 0, m) if m >= 0 else -1
    ends = [x for x in (t.find("\nfunction ", m), t.find("\nconst ", m)) if x > 0] if m >= 0 else []
    if a < 0 or not ends:
        print("(news) phone fit: logos on Today's suggestion: skipped (Today page not found). Tell the AI helper.")
        return t
    b = min(ends)
    pat = re.compile(r"<PN p=\{([A-Za-z_$][\w$.]*)\}([^<>]*?)/>")
    out, n = [], 0
    for ln in t[a:b].split("\n"):
        if ln.strip().startswith("//") or "/*" in ln or "TeamLogo" in ln:
            out.append(ln)
            continue
        new, k = pat.subn(lambda mm: '<span className="gx-pl"><TeamLogo t={' + mm.group(1) + '.t} size={18} />' + mm.group(0) + "</span>", ln)
        n += k
        out.append(new)
    if not n:
        print("(news) phone fit: logos on Today's suggestion: skipped (no player names found there). Tell the AI helper.")
        return t
    print("(news) phone fit: logos on Today's suggestion: updated (" + str(n) + " names)")
    return t[:a] + "\n".join(out) + t[b:]


def round45(t):
    t = lit(t, "phone fit: styles", "</style>", R45_CSS + "</style>", "round 45 phone fit")
    t = lit(t, "phone fit: keyboard support", ROOT, R45_HELPERS + ROOT, "function gxA11y()")
    t = lit(t, "phone fit: trades roster switch", "  const [edit, setEdit] = useState(-1);\n",
            '  const [edit, setEdit] = useState(-1);\n  const [side, setSide] = useState("me");\n', 'const [side, setSide] = useState("me");')
    t = lit(t, "phone fit: trades offer rows", R45_OFFER_OLD, R45_OFFER_NEW, '<span className="block truncate"><PN p={p} className="" /></span>')
    t = lit(t, "phone fit: trades Change player link", "setEdit(edit === k ? -1 : k); }}>change</button>", "setEdit(edit === k ? -1 : k); }}>Change player</button>", ">Change player</button>")
    t = lit(t, "phone fit: trades team buttons", R45_TAP_OLD, R45_TAP_NEW, 'className="gx-seg m-seg"')
    t = lit(t, "phone fit: trades your roster", R45_COL1_OLD, R45_COL1_NEW, '(side === "me" ? "" : " m-hide")')
    t = lit(t, "phone fit: trades their roster", R45_COL2_OLD, R45_COL2_NEW, '(side === "them" ? "" : " m-hide")')
    t = r45_today_logos(t)
    for must in ("round 45 phone fit", "function gxA11y()", "trades v42", "function TradeBuilder(", "function TopBar(", "function SubBar(", "function GxHome(", "today v32"):
        if must not in t:
            fail("fantasy-gm.html looks damaged after round 45 (" + must + ").")
    return t


_fix_before_r45 = fix


def fix(t):
    return round45(_fix_before_r45(t))

# ---------- round 46: matchup score strip, trades rosters side by side on phones, AI retrain when a week old, AI Lab new look ----------
R46_CSS = r'''  /* round 46 (news_logos.py) */
  .gx-ms { display: flex; gap: 8px; overflow-x: auto; margin-bottom: 12px; scrollbar-width: none; }
  .gx-ms::-webkit-scrollbar { display: none; }
  .gx-ms button { flex: 0 0 auto; border: 1px solid var(--line2); border-radius: 999px; padding: 7px 12px; font-size: 13px; font-variant-numeric: tabular-nums; white-space: nowrap; color: var(--mute); }
  .gx-ms button.on { border-color: var(--accent); color: var(--ink); }
  .gx-ms b { color: var(--ink); font-weight: 600; }
  @media (max-width: 640px) {
    .gx-pn > .tb-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 8px; }
    .gx-pn > .tb-grid > div.m-hide, .gx-pn > .tb-grid > div > div.m-hide { display: block !important; }
    .m-seg { display: none !important; }
  }
'''

R46_HELPERS = r'''// ---------- round 46: every matchup's score in a strip above the Matchup page (news_logos.py) ----------
function MatchStrip({ s, wk }) {
  const [cur, setCur] = useState(window.__matchSel || 0);
  useEffect(() => {
    const h = () => setCur(window.__matchSel || 0);
    window.addEventListener("gm-match", h);
    return () => window.removeEventListener("gm-match", h);
  }, []);
  const myOpp = oppOf(wk, s.me);
  const all = [[s.me, myOpp || s.opp]].concat((wk.pairs || []).filter((p) => p[0] && p[1] && p[0] !== s.me && p[1] !== s.me)).filter((p) => p[0] && p[1]);
  if (all.length < 2) return null;
  const sc = (id) => +((wk.act || {})[id]) || 0;
  const nm = (id) => { const w = (teamName(s, id) || "").split(" ")[0]; return w.length > 10 ? w.slice(0, 9) + "\u2026" : w; };
  return (
    <div className="gx-ms" role="tablist" aria-label="Matchups this week">
      {all.map(([a, b], i) => {
        const x = sc(a), y = sc(b);
        return (
          <button key={a + "-" + b} type="button" role="tab" aria-selected={i === cur} className={i === cur ? "on" : ""}
            onClick={(e) => { if (window.__setMatch) window.__setMatch(i); e.currentTarget.scrollIntoView({ behavior: "smooth", inline: "center", block: "nearest" }); }}>
            {nm(a)} {x >= y ? <b>{f1(x)}</b> : f1(x)} <span style={{ opacity: 0.6 }}>vs</span> {y > x ? <b>{f1(y)}</b> : f1(y)} {nm(b)}
          </button>
        );
      })}
    </div>
  );
}

'''

R46_SEL = "const [sel, setSel] = useState(() => { const v44 = window.__MATCH_SEL || 0; window.__MATCH_SEL = 0; return v44; });"


def round46(t):
    t = lit(t, "round 46: styles", "</style>", R46_CSS + "</style>", "round 46 (news_logos.py)")
    t = lit(t, "round 46: matchup strip helper", ROOT, R46_HELPERS + ROOT, "function MatchStrip(")
    t = lit(t, "round 46: strip follows the open matchup", R46_SEL,
            R46_SEL + '\n  useEffect(() => { window.__matchSel = sel; window.__setMatch = setSel; window.dispatchEvent(new Event("gm-match")); }, [sel]);',
            "window.__setMatch = setSel;")
    t = lit(t, "round 46: strip sits above the Matchup page", "function SubBar({ tab, sub, go, setSubs, nav }) {",
            'function SubBar({ tab, sub, go, setSubs, nav, s, wk }) {\n  if (tab === "matchup") return s && wk ? <MatchStrip s={s} wk={wk} /> : null;', "function SubBar({ tab, sub, go, setSubs, nav, s, wk })")
    t = lit(t, "round 46: strip gets the league data", "<SubBar tab={tab} sub={sub} go={go} setSubs={setSubs} nav={nav} />",
            "<SubBar tab={tab} sub={sub} go={go} setSubs={setSubs} nav={nav} s={s} wk={wk} />", "nav={nav} s={s} wk={wk} />")
    for must in ("function MatchStrip(", "function SubBar(", "<SubBar tab={tab}", "matchup v35", "trades v42"):
        if must not in t:
            fail("fantasy-gm.html looks damaged after round 46 (" + must + ").")
    return t


_fix_before_r46 = fix


def fix(t):
    return round46(_fix_before_r46(t))


# --- AI: retrain whenever the models are a week old, not only on Mondays
AIRES = "ai_research.py"
PY_BAK[AIRES] = "ai_research.backup-news.py"
PY_DONE[AIRES] = "last46_"
AIRES46 = '''    try:
        last46_ = E.parse_utc(reg["last_train"]) if reg.get("last_train") else None
    except Exception:
        last46_ = None
    if last46_ is not None and now - last46_ >= timedelta(days=7):
        print("(research) models are a week old or more - retraining today")
        force = True
    due = (force or reg.get("feature_hash")'''


def fix_aires46(t):
    t = lit(t, "AI retrain when a week old", '    due = (force or reg.get("feature_hash")', AIRES46, "last46_")
    py_ok(AIRES, t)
    return t


PY_FIXES[AIRES] = fix_aires46

# --- AI Lab page: new look, answer first, technical sections folded away
AILAB = "ai-dashboard.html"
PY_BAK[AILAB] = "ai-dashboard.backup-news.html"
PY_DONE[AILAB] = "AI Lab v2"
AL_ROOT_OLD = ':root{--bg:#0b0f17;--card:#111827;--card2:#0f172a;--line:#1f2937;--tx:#e5e7eb;--mu:#9ca3af;--ok:#34d399;--warn:#fbbf24;--bad:#f87171;--acc:#60a5fa}'
AL_ROOT_NEW = (':root{--bg:#0c0d0f;--card:#141518;--card2:#0c0d0f;--line:#232529;--tx:#f4f5f6;--mu:#8a8d93;--ok:#5fd08a;--warn:#f5c451;--bad:#f06a6a;--acc:#f4f5f6}\n'
               'html[data-t="light"]{--bg:#f5f5f4;--card:#ffffff;--card2:#f5f5f4;--line:#e4e4e1;--tx:#111111;--mu:#6b6b68;--ok:#16a34a;--warn:#b45309;--bad:#dc2626;--acc:#111111}')
AL_G = "linear-gradient(var(--tx),var(--tx))"
AL_CSS = ("/* AI Lab v2 (news_logos.py) */\n"
          'section::before{content:"";position:absolute;inset:0;pointer-events:none;background:'
          + ",".join(AL_G + " " + pos + "/" + size + " no-repeat" for pos in ("0 0", "100% 0", "0 100%", "100% 100%") for size in ("10px 1.5px", "1.5px 10px")) + "}\n"
          + r'''.lab{font-size:12px;color:var(--mu);letter-spacing:.06em}
.vd{font-size:17px;font-weight:600;margin:8px 0 10px}
.rk{display:grid;grid-template-columns:86px minmax(0,1fr) 48px;gap:10px;align-items:center;padding:6px 0;font-variant-numeric:tabular-nums}
.rk .bar{height:8px;background:var(--line)}.rk .bar i{display:block;height:8px}.rk b{text-align:right}
.r{display:flex;align-items:baseline;gap:10px;padding:9px 0;border-top:1px solid var(--line);font-variant-numeric:tabular-nums}.r>span:first-child{flex:1}
details.grp{margin-bottom:12px}
details.grp>summary{list-style:none;padding:12px 0;border-top:1px solid var(--line);color:var(--tx);font-size:14px}
details.grp[open]>summary{margin-bottom:12px}
''')
AL_HEADER = '''<header>
  <h1>AI Lab</h1>
  <span style="flex:1"></span>
  <button onclick="location.reload()">Refresh</button>
  <a href="fantasy-gm.html">Back to the app</a>
</header>'''
AL_THEME = '''(function () {
  try {
    var p = localStorage.getItem("fantasy-islands-gm-theme") || "auto";
    var dark = p === "dark" || (p !== "light" && window.matchMedia("(prefers-color-scheme: dark)").matches);
    document.documentElement.setAttribute("data-t", dark ? "dark" : "light");
  } catch (e) {}
})();
'''
AL_FUNCS = r'''// ---- AI Lab v2: the answer first, in plain words
function secVerdict(D) {
  const rep = D.rep || {}, t = (rep.tasks || {}).skater || {}, c = rep.counts || {}, pr = (rep.paired || {}).skater || {};
  let html = `<section id="verdict"><div class="lab">Which projection is most accurate</div>`;
  const rows = M.filter(m => t[m]).map(m => [m, t[m].mae, t[m].n]).sort((a, b) => a[1] - b[1]);
  if (!rows.length) return html + `<div class="empty">No finished games graded yet.</div></section>`;
  const best = rows[0], second = rows[1], last = rows[rows.length - 1];
  const k = second ? (pr[best[0] + "_vs_" + second[0]] || pr[second[0] + "_vs_" + best[0]]) : null;
  const level = !!(k && !/more accurate$/.test(k.verdict));
  let line = level ? `${NAME[best[0]]} and ${NAME[second[0]]} are level.` : `${NAME[best[0]]} is the most accurate so far.`;
  if (rows.length > 2) line += ` ${level ? "Both beat" : "It beats"} ${NAME[last[0]]} by ${f(last[1] - best[1], 1)} points a game.`;
  html += `<p class="vd">${line}</p>`;
  for (const [m, mae] of rows) html += `<div class="rk"><span>${NAME[m]}</span><div class="bar"><i style="width:${Math.round(mae / last[1] * 100)}%;background:${m === best[0] ? "var(--tx)" : m === last[0] ? "var(--bad)" : "var(--mu)"}"></i></div><b>${f(mae)}</b></div>`;
  return html + `<p class="muted small">How many fantasy points each projection is off by per game, on average, for skaters. Shorter is better. ${c.graded_days || 0} game days, ${(best[2] || 0).toLocaleString()} player-games. Goalies need more games before there is a winner.</p></section>`;
}
function secOff(D) {
  const seg = (D.rep || {}).segments || {}, out = [];
  const LAB = {venue: {away: "Players on the road", home: "Players at home"},
    "power play": {"not on PP1": "Players off the top power play", "on PP1": "Players on the top power play"},
    rest: {"back-to-back": "Players on the second night of a back-to-back"},
    line: {D1: "Top-pair defencemen", F1: "First-line forwards", "lower lines": "Lower-line players"}};
  const add = (label, m, s) => { if (s && s.n >= 40 && s.bias_se > 0 && Math.abs(s.bias) >= 0.4 && Math.abs(s.bias) >= 2.4 * s.bias_se) out.push({label, m, b: s.bias}); };
  for (const [key, vals] of Object.entries(LAB)) for (const [v, label] of Object.entries(vals)) for (const m of ["ai", "espn"]) add(label, m, ((seg[key] || {})[v] || {})[m]);
  for (const [tm, ms] of Object.entries(seg.team || {})) add(tm + " skaters", "ai", ms.ai);
  out.sort((a, b) => Math.abs(b.b) - Math.abs(a.b));
  let html = `<section id="off"><div class="lab">Where the projections are off</div>`;
  if (!out.length) return html + `<div class="empty">No pattern is large enough to trust yet.</div></section>`;
  html += out.slice(0, 10).map((x, i) => `<div class="r"${i ? "" : ' style="border-top:0"'}><span>${esc(x.label)}</span><span class="muted small">${NAME[x.m]} projects them</span><b class="${x.b > 0 ? "over" : "under"}" style="min-width:86px;text-align:right">${f(Math.abs(x.b), 1)} too ${x.b > 0 ? "high" : "low"}</b></div>`).join("");
  return html + `<p class="muted small" style="margin-top:8px">Points a game. Only patterns too large to be luck are listed. They are clues, not proven causes.</p></section>`;
}

'''
AL_BOOT = r'''const run = fns => fns.map(fn => { try { return fn(D); } catch (e) { return `<section><div class="empty">This section failed to load: ${esc(e.message)}</div></section>`; } }).join("");
  document.getElementById("app").innerHTML = run([secVerdict, secHealth, secOff, secPlayers])
    + `<details class="grp"><summary>Goalie start chances: did 70% mean 70%</summary>${run([secGoalies])}</details>`
    + `<details class="grp"><summary>Under the hood: accuracy tables, model tests, research log</summary>${run([secLive, secTime, secWhere, secLab, secResearch, secHelp])}</details>`;'''


def fix_ailab46(t):
    if "AI Lab v2" in t:
        print("(news) AI Lab: new look: already done")
        return t

    def rep(old, new):
        nonlocal t
        if t.count(old) != 1:
            fail("AI Lab: could not find this text in ai-dashboard.html: " + old[:60] + " ... Send this log to the AI helper.")
        t = t.replace(old, new, 1)

    def resub(pat, new):
        nonlocal t
        t, n = re.subn(pat, lambda m: new, t, count=1, flags=re.S)
        if n != 1:
            fail("AI Lab: could not find the pattern " + pat[:40] + " in ai-dashboard.html. Send this log to the AI helper.")

    rep(AL_ROOT_OLD, AL_ROOT_NEW)
    rep("background:#0b0f17ee;backdrop-filter:blur(6px);", "background:var(--bg);")
    rep("section{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px 18px;margin-bottom:16px}",
        "section{background:var(--card);padding:16px 18px;margin-bottom:12px;position:relative}")
    rep("tr.best td{background:#064e3b55}", "tr.best td{background:color-mix(in srgb,var(--ok) 14%,transparent)}")
    rep(".chart .grid{stroke:#1f2937}", ".chart .grid{stroke:var(--line)}")
    rep("</style>", AL_CSS + "</style>")
    resub(r"<header>.*?</header>", AL_HEADER)
    rep('const M = ["espn", "gm", "blend", "ai"];', AL_THEME + 'const M = ["espn", "gm", "blend", "ai"];')
    rep('"Mondays 4:20 AM"', '"Whenever they are a week old"')
    rep("(useful days ahead).</p>", "(useful days ahead). The app's rule is graded on its last reading before puck drop, when most starters are already confirmed, so its table says little about how good it is days ahead.</p>")
    resub(r"// -+ boot", AL_FUNCS + "// ------------------------------------------------------------ boot")
    resub(r'document\.getElementById\("app"\)\.innerHTML = \[secHealth.*?\.join\(""\);', AL_BOOT)
    for must in ("function secVerdict(", "function secOff(", "function secHealth(", "function secPlayers(", "function drawPlayer(", "</html>"):
        if must not in t:
            fail("ai-dashboard.html looks damaged after the AI Lab update (" + must + ").")
    print("(news) AI Lab: new look: updated")
    return t


PY_FIXES[AILAB] = fix_ailab46

# ---------- round 47: logos on Today's suggestion, every-starter list open, matchup dots hidden ----------
def r47_region(t, name):
    a = t.find("function " + name + "(")
    if a < 0:
        return -1, -1
    ends = [x for x in (t.find("\nfunction ", a + 10), t.find("\nconst ", a + 10)) if x > 0]
    return a, (min(ends) if ends else len(t))


def r47_today_logos(t):
    if 'className="gx-pl"' in t:
        print("(news) round 47: logos on Today's suggestion: already done")
        return t
    a, b = r47_region(t, "Today")
    if a < 0:
        print("(news) round 47: logos on Today's suggestion: NOT DONE, the Today page was not found. Send this log to the AI helper.")
        return t
    lines = t[a:b].split("\n")
    pats = [(re.compile(r"<PN p=\{([A-Za-z_$][\w$.]*)\}([^<>]*?)/>"),
             lambda m: '<span className="gx-pl"><TeamLogo t={' + m.group(1) + '.t} size={18} />' + m.group(0) + "</span>"),
            (re.compile(r"(?<![=\w$])\{([A-Za-z_$][\w$.]*)\.n\}"),
             lambda m: '<span className="gx-pl"><TeamLogo t={' + m.group(1) + '.t} size={18} />{' + m.group(1) + ".n}</span>")]
    for pat, fn in pats:
        out, n = [], 0
        for ln in lines:
            if ln.strip().startswith("//") or "/*" in ln or "TeamLogo" in ln:
                out.append(ln)
                continue
            new, k = pat.subn(fn, ln)
            n += k
            out.append(new)
        if n:
            print("(news) round 47: logos on Today's suggestion: updated (" + str(n) + " names)")
            return t[:a] + "\n".join(out) + t[b:]
    print("(news) round 47: logos on Today's suggestion: NOT DONE, no player names found. Send these lines to the AI helper:")
    for ln in [x for x in lines if re.search(r"[Mm]ove|[Aa]dd |drop", x)][:8]:
        print("(news)   | " + ln.strip()[:260])
    return t


def r47_dots(t):
    if "round 47 dots" in t:
        print("(news) round 47: matchup dots hidden: already done")
        return t
    a, b = r47_region(t, "Matchup")
    names = sorted(set(re.findall(r'className=\{?"([\w-]*dot[\w-]*)', t[a:b]))) if a >= 0 else []
    if not names:
        print("(news) round 47: matchup dots hidden: NOT DONE, could not tell which element draws them. Send these lines to the AI helper:")
        for ln in [x for x in (t[a:b].split("\n") if a >= 0 else []) if "sel ===" in x or "i === sel" in x][:8]:
            print("(news)   | " + ln.strip()[:260])
        return t
    css = "  /* round 47 dots (news_logos.py) */\n  " + ", ".join("." + n for n in names) + " { display: none !important; }\n"
    print("(news) round 47: matchup dots hidden: updated (" + ", ".join(names) + ")")
    return t.replace("</style>", css + "</style>", 1)


def round47(t):
    t = lit(t, "round 47: every-starter list starts open", "  const [day, setDay] = useState(null);\n  const [all, setAll] = useState(false);",
            "  const [day, setDay] = useState(null);\n  const [all, setAll] = useState(true);", "const [all, setAll] = useState(true);")
    t = lit(t, "round 47: every-starter list stays open", "onClick={() => { setDay(i); setAll(false); }}", "onClick={() => setDay(i)}", 'onClick={() => setDay(i)} className={"gx-day"')
    t = r47_today_logos(t)
    t = r47_dots(t)
    for must in ("goalies v43", "function GoalieStreams(", "function Today(", "function Matchup(", "matchup v35"):
        if must not in t:
            fail("fantasy-gm.html looks damaged after round 47 (" + must + ").")
    return t


_fix_before_r47 = fix


def fix(t):
    return round47(_fix_before_r47(t))

# ---------- round 48: team logos in "Who's carrying you" and "Goalie board"; matchup dots hidden by editing their own line ----------
def r48_region(t, name):
    for head in ("function " + name + "(", "const " + name + " = "):
        a = t.find(head)
        if a >= 0:
            ends = [x for x in (t.find("\nfunction ", a + 10), t.find("\nconst ", a + 10)) if x > 0]
            return a, (min(ends) if ends else len(t))
    return -1, -1


def r48_logos(t):
    pats = [re.compile(r"<PN p=\{([A-Za-z_$][\w$.]*)\}([^<>]*?)/>"), re.compile(r"(?<![=\w$])\{([A-Za-z_$][\w$.]*)\.n\}")]
    wrap = lambda m: '<span className="gx-pl"><TeamLogo t={' + m.group(1) + '.t} size={20} />' + m.group(0) + "</span>"
    for name in ("GxCarry", "GxGoalies", "Today"):
        a, b = r48_region(t, name)
        if a < 0:
            print("(news) round 48: logos in " + name + ": NOT DONE, that box was not found. Send this log to the AI helper.")
            continue
        lines, n = t[a:b].split("\n"), 0
        had = any('className="gx-pl"' in ln for ln in lines)
        for pat in pats:
            out = []
            for ln in lines:
                if ln.strip().startswith("//") or "/*" in ln or "TeamLogo" in ln:
                    out.append(ln)
                    continue
                new, k = pat.subn(wrap, ln)
                n += k
                out.append(new)
            if n:
                t = t[:a] + "\n".join(out) + t[b:]
                break
        if n:
            print("(news) round 48: logos in " + name + ": updated (" + str(n) + " names)")
        elif had:
            print("(news) round 48: logos in " + name + ": already done")
        else:
            print("(news) round 48: logos in " + name + ": no player names found there. If logos are missing in this box, send these lines to the AI helper:")
            for ln in [x for x in lines if ".n" in x or "PN" in x][:6]:
                print("(news)   | " + ln.strip()[:260])
    return t


def r48_dots(t):
    if "r48 dots" in t:
        print("(news) round 48: matchup dots hidden: already done")
        return t
    a, b = r48_region(t, "Matchup")
    if a < 0:
        print("(news) round 48: matchup dots hidden: NOT DONE, the Matchup page was not found. Send this log to the AI helper.")
        return t
    lines, n = t[a:b].split("\n"), 0
    hide = 'display: "none", opacity: 0, pointerEvents: "none", borderRadius'
    for i, ln in enumerate(lines):
        if not re.search(r"\bi === sel\b|\bsel === i\b", ln):
            continue
        if "borderRadius" in ln:
            lines[i] = ln.replace("borderRadius", hide, 1)
            n += 1
        elif "rounded-full" in ln:
            lines[i] = ln.replace("rounded-full", "rounded-full hidden", 1)
            n += 1
    names = sorted(set(re.findall(r'className=\{?"([\w-]*dot[\w-]*)', t[a:b])))
    if not n and not names:
        print("(news) round 48: matchup dots hidden: NOT DONE. Send these lines to the AI helper:")
        for ln in [x for x in lines if re.search(r"\bsel\b", x) and ".map(" in x][:6]:
            print("(news)   | " + ln.strip()[:260])
        return t
    t = t[:a] + "\n".join(lines) + t[b:]
    css = "  /* r48 dots (news_logos.py) */\n" + ("  " + ", ".join("." + x for x in names) + " { display: none !important; }\n" if names else "")
    print("(news) round 48: matchup dots hidden: updated")
    return t.replace("</style>", css + "</style>", 1)


def round48(t):
    t = r48_logos(t)
    t = r48_dots(t)
    for must in ("function Today(", "function Matchup(", "matchup v35", "function GxHome(", "function MatchStrip("):
        if must not in t:
            fail("fantasy-gm.html looks damaged after round 48 (" + must + ").")
    return t


_fix_before_r48 = fix


def fix(t):
    return round48(_fix_before_r48(t))

if __name__ == "__main__":
    main()
