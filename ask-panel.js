// ask-panel.js - the 💬 Ask button for Fantasy Islands GM (loaded by fantasy-gm.html).
// Answers any question with Google Gemini, using your league data from the app.
// Your Gemini key is saved only in this browser (localStorage) - never in the GitHub repo.
(function () {
  const { useState, useEffect, useRef } = React;
  const KEYSTORE = "fantasy-islands-gemini-key";
  const MODELSTORE = "fantasy-islands-gemini-model";
  const MODELS = ["gemini-flash-latest", "gemini-3-flash-preview", "gemini-2.5-flash", "gemini-flash-lite-latest"];
  const SYSTEM = `You are the personal GM assistant for Kuvar's ESPN fantasy hockey team "kanucks" in the league Fantasy Islands.
League: 10 teams, head-to-head POINTS. Scoring - skaters: G 6, A 4, +/- 2, PPP 2, SHP 3, SOG 1, HIT 0.1, BLK 1. Goalies: W 5, GA -3, SV 0.6, SO 5, OTL 1.
Daily lineup: 9 F, 5 D, 1 UTIL, 2 G (bench 5, 1 IR). 3 acquisitions per weekly matchup, 1-day waivers. Trade deadline Feb 26, 2027. Top 6 make playoffs.
Rules for answering:
- Base your answer on the LEAGUE DATA provided (projections, lines, PP units, schedule, injuries, goalie start chances, free agents, rosters). Quote the numbers you use.
- Give a clear recommendation first (e.g. "Start X", "Add Y, drop Z", "Decline the trade"), then 2-5 short reasons.
- In a points league games played matters: more games = more points, but only if the player fits in the daily lineup.
- If the data doesn't cover something, say so briefly instead of guessing. Never invent stats, injuries or news.
- Keep it short and plain - the user is not a hockey analytics expert. Use short bullet points.`;
  const SUGGEST = ["Who should I start tonight?", "Best pickup for this week?", "Am I going to win my matchup? What should I do?", "Which of my goalies should I start?", "Who on my team should I try to trade?"];
  const nk = (x) => (x || "").normalize("NFD").replace(/[\u0300-\u036f]/g, "").replace(/[^\x00-\x7f]/g, "").toLowerCase().replace(/\./g, "").replace(/-/g, " ").trim();
  const ls = {
    get: (k) => { try { return localStorage.getItem(k) || ""; } catch (e) { return ""; } },
    set: (k, v) => { try { if (v) localStorage.setItem(k, v); else localStorage.removeItem(k); } catch (e) {} },
  };

  function buildContext(q, props) {
    const { s, wk, H } = props;
    const K = s.blend, today = H.todayISO(), f1 = H.f1, L = window.LINES_DATA || {};
    const out = [];
    const MODE = { espn: "ESPN", blend: "Blend (ESPN + GM model)", model: "GM model", ai: "AI model" };
    out.push(`Today: ${today}. Matchup: ${wk.label}. Projection mode: ${MODE[window.__PMODE] || "ESPN"}. Last data sync: ${s.lastSync || "unknown"} (UTC).`);
    const where = {};
    Object.entries(L.teams || {}).forEach(([t, T]) => Object.entries(T.lines || {}).forEach(([sl, arr]) => (arr || []).forEach((n) => {
      const k = nk(n) + "|" + t; where[k] = where[k] || {};
      if (sl.startsWith("PP")) where[k].pp = where[k].pp || sl; else where[k].es = where[k].es || sl;
    })));
    const ROLE = { F1: "1st line", F2: "2nd line", F3: "3rd line", F4: "4th line", D1: "top pair", D2: "2nd pair", D3: "3rd pair" };
    const dates = wk.dates || [];
    const left = (p) => (wk.games[p.t] || []).filter((i) => (dates[i] || "") >= today);
    const fpTxt = (p) => {
      const a = (L.fp || {})[nk(p.n) + "|" + p.p], b = (L.fpl || {})[nk(p.n) + "|" + p.p];
      return a && a[1] ? `${f1(a[0])} fantasy pts in ${a[1]} GP this season` : b ? `${f1(b[0])} fantasy pts in ${b[1]} GP last season` : "";
    };
    const line = (p) => {
      const w = where[nk(p.n) + "|" + p.t] || {}, back = H.effBack(p), gl = left(p);
      const bits = [`${p.n} (${p.p}, ${p.t})`];
      if (p.status && p.status !== "ACTIVE") bits.push(`STATUS ${p.status}${back.d ? ", expected back " + back.d : ""}`);
      if (p.ir) bits.push("in IR slot");
      bits.push(`proj ${f1(H.effAvg(p, K))} pts/game`);
      bits.push(`${gl.length} games left this week${gl.length ? " (" + gl.map((i) => dates[i].slice(5)).join(", ") + ")" : ""}`);
      if (w.es && ROLE[w.es]) bits.push(ROLE[w.es]);
      if (w.pp) bits.push(w.pp);
      const f = fpTxt(p); if (f) bits.push(f);
      const tg = (H.tags(p, K) || []).map((x) => x.t).filter((t) => t && !t.startsWith("📰")).join("; ");
      if (tg) bits.push(tg);
      return bits.join(" | ");
    };
    const mine = s.players.filter((p) => p.ft === s.me);
    const opp = H.oppOf(wk, s.me) || s.opp;
    const theirs = s.players.filter((p) => p.ft === opp);
    try {
      const A = H.weekProj(mine, wk, K, wk.done || 0), B = H.weekProj(theirs, wk, K, wk.done || 0);
      const aA = +((wk.act || {})[s.me]) || 0, aB = +((wk.act || {})[opp]) || 0;
      out.push(`\nMATCHUP: ${H.teamName(s, s.me)} (me) ${f1(aA)} actual + ${f1(A.total)} projected = ${f1(aA + A.total)} vs ${H.teamName(s, opp)} ${f1(aB)} + ${f1(B.total)} = ${f1(aB + B.total)}. My games that would sit on the bench: ${A.wasted}. My empty lineup slots: ${A.empty}.`);
    } catch (e) {}
    out.push("\nMY ROSTER:");
    mine.forEach((p) => out.push("- " + line(p)));
    const gl = mine.filter((p) => p.p === "G" && !p.ir);
    if (gl.length) {
      out.push("\nMY GOALIES - start chance for upcoming games:");
      gl.forEach((p) => out.push(`- ${p.n}: ` + (left(p).slice(0, 4).map((i) => { const g = H.gStart(p, dates[i]); return `${dates[i].slice(5)} ${Math.round(g.v * 100)}%${g.l ? " (" + g.l + ")" : ""}`; }).join("; ") || "no games left this week")));
    }
    out.push(`\nTHIS WEEK'S OPPONENT (${H.teamName(s, opp)}) ROSTER:`);
    theirs.forEach((p) => out.push(`- ${p.n} (${p.p}, ${p.t}) proj ${f1(H.effAvg(p, K))}/game, ${left(p).length} games left${p.status && p.status !== "ACTIVE" ? ", " + p.status : ""}`));
    const weekPts = (p) => left(p).reduce((a, i) => { const d = dates[i]; const g = p.p === "G" ? H.gStart(p, d).v : p.prob; return a + H.effAvg(p, K, d) * g * H.avail(p, d); }, 0);
    const fas = s.players.filter((p) => p.ft === "fa" && p.prob > 0);
    const byWeek = fas.map((p) => ({ p, v: weekPts(p) })).sort((a, b) => b.v - a.v).slice(0, 25);
    out.push("\nBEST FREE AGENTS (by projected points for the rest of this week):");
    byWeek.forEach(({ p, v }) => out.push(`- ${line(p)} | ${f1(v)} pts rest of week | ${f1(p.own)}% rostered`));
    const byAvg = [...fas].sort((a, b) => H.effAvg(b, K) - H.effAvg(a, K)).filter((p) => !byWeek.some((x) => x.p === p)).slice(0, 15);
    if (byAvg.length) { out.push("\nMORE FREE AGENTS (best points per game, long term):"); byAvg.forEach((p) => out.push(`- ${line(p)} | ${f1(p.own)}% rostered`)); }
    try {
      const res = H.computeMoves(s, { H: 1, pool: 40 }).res.filter((r) => r.gain > 0).slice(0, 5);
      if (res.length) { out.push("\nAPP'S TOP SUGGESTED PICKUPS THIS WEEK (lineup-aware):"); res.forEach((r) => out.push(`- Add ${r.f.n} (${r.f.p}, ${r.f.t}), drop ${r.d.n}: +${f1(r.gain)} pts this week`)); }
    } catch (e) {}
    out.push("\nOTHER FANTASY TEAMS (for trade questions; name position/team projected pts per game):");
    s.teams.filter((t) => t.id !== s.me).forEach((t) => {
      const r = s.players.filter((p) => p.ft === t.id).sort((a, b) => H.effAvg(b, K) - H.effAvg(a, K));
      out.push(`${t.name}: ` + r.map((p) => `${p.n} ${p.p}/${p.t} ${f1(H.effAvg(p, K))}${p.status && p.status !== "ACTIVE" ? " " + p.status : ""}`).join("; "));
    });
    const qn = " " + nk(q).replace(/[^a-z ]/g, " ") + " ";
    const full = s.players.filter((p) => qn.includes(" " + nk(p.n) + " "));
    const lastOnly = s.players.filter((p) => { const last = nk(p.n).split(" ").pop(); return !full.includes(p) && last.length >= 4 && qn.includes(" " + last + " "); });
    const hits = [...full, ...lastOnly].slice(0, 8);
    if (hits.length) {
      out.push("\nPLAYERS NAMED IN THE QUESTION (details):");
      const S = window.__SIG || {};
      hits.forEach((p) => {
        const id = typeof p.id === "string" ? p.id.slice(1) : "";
        out.push("- " + line(p));
        out.push(`  Owner: ${H.teamName(s, p.ft)} | ${f1(p.own)}% rostered (${p.chg > 0 ? "+" : ""}${f1(p.chg)}% this week) | ESPN projection ${f1(p.pavg)}/game`);
        const inj = (S.injuries || {})[id]; if (inj && inj.note) out.push(`  Injury: ${inj.status} - ${inj.note}`);
        ((S.news || {})[id] || []).forEach((n) => out.push(`  News ${n.d}: ${n.h}`));
        const games = ((L.sched || {})[p.t] || []).filter((g) => g.d >= today).slice(0, 5);
        if (games.length) out.push("  Next games: " + games.map((g) => { const gs = p.p === "G" ? H.gStart(p, g.d) : null; return `${g.d.slice(5)} ${g.h ? "vs" : "@"} ${g.o} ${f1(H.effAvg(p, K, g.d) * (gs ? gs.v : 1))} pts${gs ? " (" + Math.round(gs.v * 100) + "% start)" : ""}`; }).join("; "));
      });
    }
    const ch = (L.changes || []).slice(0, 25);
    if (ch.length) { out.push("\nRECENT NHL LINE / ROSTER / INJURY CHANGES:"); ch.forEach((c) => out.push(`- ${c.at.slice(0, 10)} ${c.text}`)); }
    return out.join("\n");
  }

  async function callGemini(key, q, ctx, hist) {
    const contents = [];
    hist.forEach((h) => { contents.push({ role: "user", parts: [{ text: h.q }] }); contents.push({ role: "model", parts: [{ text: h.a }] }); });
    contents.push({ role: "user", parts: [{ text: "LEAGUE DATA (from my app):\n" + ctx + "\n\nMY QUESTION: " + q }] });
    const body = JSON.stringify({ systemInstruction: { parts: [{ text: SYSTEM }] }, contents, generationConfig: { temperature: 0.4, maxOutputTokens: 4096 } });
    const saved = ls.get(MODELSTORE);
    const models = saved ? [saved, ...MODELS.filter((m) => m !== saved)] : MODELS;
    let last = "";
    for (const m of models) {
      try {
        const r = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/${m}:generateContent?key=${encodeURIComponent(key)}`, { method: "POST", headers: { "Content-Type": "application/json" }, body });
        const d = await r.json().catch(() => ({}));
        if (r.ok) {
          const parts = (((d.candidates || [])[0] || {}).content || {}).parts || [];
          const text = parts.map((p) => p.text || "").join("").trim();
          if (text) { ls.set(MODELSTORE, m); return { a: text, model: m }; }
          last = m + ": empty answer"; continue;
        }
        const msg = String((d.error && d.error.message) || r.status);
        if (/api key/i.test(msg)) return { err: "Google says the key isn't valid. Click 🔑 Key and paste it again." };
        if (r.status === 403) return { err: "Google refused the key: " + msg };
        last = `${m}: ${msg}`;
      } catch (e) { last = "network error: " + e.message; }
    }
    return { err: "The AI couldn't answer right now (maybe the free daily limit). Details: " + last };
  }

  function Md({ text }) {
    return (
      <div className="space-y-1">
        {text.split("\n").map((ln, i) => {
          const t = ln.trim(); if (!t) return null;
          const bullet = /^[-*•]\s+/.test(t), head = /^#+\s+/.test(t);
          const body = t.replace(/^[-*•]\s+/, "").replace(/^#+\s+/, "");
          const parts = body.split(/(\*\*[^*]+\*\*)/g).map((x, j) => (x.startsWith("**") && x.endsWith("**") && x.length > 4 ? <b key={j}>{x.slice(2, -2)}</b> : <span key={j}>{x}</span>));
          return <div key={i} className={bullet ? "pl-4 relative" : head ? "font-semibold mt-1" : ""}>{bullet ? <span className="absolute left-1">•</span> : null}{parts}</div>;
        })}
      </div>
    );
  }

  function AskPanel(props) {
    const [open, setOpen] = useState(false);
    const [key, setKey] = useState(() => ls.get(KEYSTORE));
    const [keyInput, setKeyInput] = useState("");
    const [showKey, setShowKey] = useState(false);
    const [draft, setDraft] = useState("");
    const [msgs, setMsgs] = useState([]);
    const [busy, setBusy] = useState(false);
    const endRef = useRef(null);
    useEffect(() => { if (endRef.current) endRef.current.scrollIntoView({ behavior: "smooth" }); }, [msgs, busy, open]);
    const saveKey = () => { const k = keyInput.trim(); if (!k) return; ls.set(KEYSTORE, k); setKey(k); setKeyInput(""); setShowKey(false); };
    const ask = async (text) => {
      const q = (text || draft).trim();
      if (!q || busy || !key) return;
      setDraft(""); setBusy(true);
      const hist = msgs.filter((m) => m.a).slice(-4);
      setMsgs((m) => [...m, { q }]);
      let ctx = "";
      try { ctx = buildContext(q, props); } catch (e) { ctx = "(the app could not collect its data: " + e.message + ")"; }
      const res = await callGemini(key, q, ctx, hist);
      setMsgs((m) => m.map((x, i) => (i === m.length - 1 ? { ...x, ...res } : x)));
      setBusy(false);
    };
    if (!open) {
      return <button onClick={() => setOpen(true)} className="fixed bottom-5 right-5 z-40 bg-blue-600 rounded-full px-5 py-3 shadow-lg font-semibold text-sm">💬 Ask</button>;
    }
    const needKey = !key || showKey;
    return (
      <div className="fixed bottom-0 right-0 sm:bottom-5 sm:right-5 z-50 w-full sm:w-[440px] h-[85vh] sm:h-[640px] bg-white border border-slate-200 rounded-t-xl sm:rounded-xl shadow-2xl flex flex-col text-sm">
        <div className="flex items-center gap-2 px-3 py-2 border-b border-slate-200">
          <span className="font-semibold">💬 Ask your GM</span>
          <span className="text-xs text-slate-400">Gemini · uses your league data</span>
          <button className="ml-auto text-xs text-slate-500" onClick={() => setShowKey(!showKey)}>🔑 Key</button>
          {msgs.length > 0 && <button className="text-xs text-slate-500" onClick={() => setMsgs([])}>Clear</button>}
          <button className="text-slate-500 px-1" onClick={() => setOpen(false)}>✕</button>
        </div>
        {needKey && (
          <div className="p-3 border-b border-slate-200 bg-slate-50">
            <div className="text-xs text-slate-600 mb-2">Paste your Gemini API key (starts with <b>AIza</b>). It's saved only in this browser on this device, not on GitHub. Get it at aistudio.google.com → 🔑 key icon.</div>
            <div className="flex gap-2">
              <input type="password" className="border border-slate-300 rounded-lg px-2 py-1.5 text-sm flex-1" placeholder="AIza..." value={keyInput} onChange={(e) => setKeyInput(e.target.value)} onKeyDown={(e) => e.key === "Enter" && saveKey()} />
              <button className="bg-blue-600 rounded-lg px-3 py-1.5" onClick={saveKey}>Save</button>
            </div>
            {key && <button className="text-xs text-red-600 mt-2" onClick={() => { ls.set(KEYSTORE, ""); setKey(""); }}>Remove saved key from this device</button>}
          </div>
        )}
        <div className="flex-1 overflow-y-auto p-3 space-y-3">
          {!msgs.length && (
            <div>
              <div className="text-xs text-slate-500 mb-2">Ask anything about your team, matchup, pickups, goalies or trades. Name players and I'll pull their full details.</div>
              <div className="flex flex-wrap gap-2">{SUGGEST.map((q) => <button key={q} disabled={!key} onClick={() => ask(q)} className="text-xs border border-slate-300 rounded-full px-3 py-1 text-left">{q}</button>)}</div>
            </div>
          )}
          {msgs.map((m, i) => (
            <div key={i} className="space-y-2">
              <div className="flex justify-end"><div className="bg-blue-600 rounded-xl px-3 py-2 max-w-[85%] whitespace-pre-wrap">{m.q}</div></div>
              {m.a ? <div className="bg-slate-50 border border-slate-200 rounded-xl px-3 py-2"><Md text={m.a} /><div className="text-xs text-slate-400 mt-1">{m.model}</div></div>
                : m.err ? <div className="text-red-600 text-xs">{m.err}</div>
                : <div className="text-slate-400 text-xs">Thinking… (reading your roster, matchup and free agents)</div>}
            </div>
          ))}
          <div ref={endRef} />
        </div>
        <div className="p-2 border-t border-slate-200 flex gap-2">
          <textarea rows={2} className="border border-slate-300 rounded-lg px-2 py-1.5 text-sm flex-1 resize-none" placeholder={key ? "Ask a question… (Enter to send)" : "Save your key above first"} value={draft}
            onChange={(e) => setDraft(e.target.value)} onKeyDown={(e) => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); ask(); } }} disabled={!key} />
          <button className="bg-blue-600 rounded-lg px-4 font-semibold" disabled={busy || !key || !draft.trim()} onClick={() => ask()}>{busy ? "…" : "Send"}</button>
        </div>
      </div>
    );
  }

  window.AskPanel = AskPanel;
})();
