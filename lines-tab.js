// lines-tab-v2.js - redesigned "Lines" tab for Fantasy Islands GM.
// Same data as before (window.LINES_DATA from lines-data.js) and same app helpers (H).
// New: changes ranked by importance (top few shown, "Show all" for the rest),
// and teams as a ranked list that opens into Daily Faceoff-style lines.
(function () {
  const { useState, useEffect, useMemo } = React;
  const ES_F = ["F1", "F2", "F3", "F4"], ES_D = ["D1", "D2", "D3"];
  const LBL = { F1: "1st line", F2: "2nd line", F3: "3rd line", F4: "4th line", D1: "top pair", D2: "2nd pair", D3: "3rd pair", PP1: "PP1", PP2: "PP2", G: "goalie" };
  const SHORT = { F1: "L1", F2: "L2", F3: "L3", F4: "L4", D1: "D1", D2: "D2", D3: "D3", PP1: "PP1", PP2: "PP2", G: "G" };
  const MODE = { espn: "ESPN", blend: "Blend", model: "GM model", ai: "AI" };
  const INJ = { DAY_TO_DAY: "DTD", OUT: "Out", INJURY_RESERVE: "IR", SUSPENSION: "Susp." };
  const nk = (x) => (x || "").normalize("NFD").replace(/[\u0300-\u036f]/g, "").replace(/[^\x00-\x7f]/g, "").toLowerCase().replace(/\./g, "").replace(/-/g, " ").trim();
  const grpOf = (sl) => (sl === "G" ? "G" : sl && sl[0] !== "P" ? sl[0] : null);
  const pretty = (x) => String(x || "").replace(/_/g, " ").toLowerCase().replace(/\b\w/g, (m) => m.toUpperCase());
  const ago = (iso) => {
    if (!iso) return "never";
    const m = (Date.now() - Date.parse(iso)) / 6e4;
    if (m < 1) return "just now";
    if (m < 60) return Math.round(m) + " min ago";
    if (m < 2880) return Math.round(m / 60) + " h ago";
    return Math.round(m / 1440) + " days ago";
  };

  // real ESPN points for one player on one day (news_logos.py round 19)
  const realPts = (p, d) => {
    const D = (((window.ESPN_DATA || {}).daily) || {})[d] || {}, id = String(p.id || "").replace(/^e/, "");
    for (const tm of Object.values(D)) { const v = (tm || {})[id]; if (v && v[0] != null) return v[0]; }
    return null;
  };

  // ---------- styles (dark, matches the app) ----------
  const CSS = `
.lt-it{display:grid;grid-template-columns:26px 1fr auto;gap:8px;padding:8px 2px;border-top:1px solid #292929;align-items:start;cursor:pointer}
.lt-it:first-child{border-top:none}
.lt-it:hover{background:rgba(139,124,255,.06)}
.lt-low{opacity:.55}
.lt-ic{font-weight:700;font-size:12px;text-align:center;padding-top:2px}
.lt-up{color:#5fd08a}.lt-dn{color:#f06a6a}.lt-mu{color:#8f8f8f}
.lt-tm{font-size:11px;color:#8f8f8f;margin-right:2px}
.lt-why{font-size:12px;color:#8f8f8f;margin-top:1px}
.lt-own{font-size:12px;white-space:nowrap;padding-top:2px;color:#8f8f8f;max-width:130px;overflow:hidden;text-overflow:ellipsis}
.lt-own.me{color:#8b7cff;font-weight:600}.lt-own.fa{color:#5fd08a}
.lt-link{background:none;border:none;color:#8b7cff;cursor:pointer;padding:8px 0 0;font-size:13px}
.lt-bar{display:flex;justify-content:space-between;align-items:center;gap:8px;flex-wrap:wrap;margin-top:10px;padding-top:10px;border-top:1px solid #292929;font-size:12px;color:#8f8f8f}
.lt-grp-h{display:flex;gap:8px;align-items:center;padding:8px 2px;border-top:1px solid #292929;cursor:pointer;font-size:13px}
.lt-grp-b{padding:0 0 6px 16px}
.lt-team{border:1px solid #292929;border-radius:12px;background:#161616;margin-bottom:8px;overflow:hidden}
.lt-team.open{border-color:#4a4a4a}
.lt-tr{display:flex;align-items:center;gap:10px;padding:10px 12px;cursor:pointer}
.lt-tr:hover{background:#1f1f1f}
.lt-rk{font-weight:700;width:34px;color:#8f8f8f;flex-shrink:0}
.lt-tmain{min-width:0;flex:1}
.lt-tn{font-weight:600;color:#fafafa}
.lt-meta{font-size:12px;color:#8f8f8f}
.lt-hint{font-size:12px;margin-top:2px;color:#d4d4d4;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.lt-pills{display:flex;gap:6px;flex-wrap:wrap;justify-content:flex-end}
.lt-pill{font-size:11px;padding:2px 8px;border-radius:999px;border:1px solid #363636;color:#8f8f8f;white-space:nowrap}
.lt-pill.me{color:#8b7cff;border-color:rgba(139,124,255,.45)}
.lt-chev{color:#8f8f8f;transition:transform .2s;flex-shrink:0;display:inline-block}
.lt-team.open .lt-chev{transform:rotate(180deg)}
.lt-body{padding:10px 12px 14px;border-top:1px solid #292929}
.lt-stabs{display:flex;gap:6px;flex-wrap:wrap}
.lt-stab{background:transparent;border:1px solid #363636;color:#d4d4d4;border-radius:999px;padding:4px 11px;font-size:13px;cursor:pointer}
.lt-stab.on{border-color:#8b7cff;color:#8b7cff;background:rgba(139,124,255,.1)}
.lt-sec{font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:#bdbdbd;margin:14px 0 8px;background:#202020;padding:5px 8px;border-radius:6px;text-align:center;font-weight:600}
.lt-grid{display:grid;grid-template-columns:28px repeat(3,minmax(0,1fr));gap:6px}
.lt-grid.d{grid-template-columns:28px repeat(2,minmax(0,1fr));max-width:680px;margin:0 auto}
.lt-rl{font-size:12px;color:#8f8f8f;display:flex;align-items:center}
.lt-pc{display:block;width:100%;background:#1a1a1a;border:1px solid #292929;border-left:3px solid #4d4d4d;border-radius:8px;padding:7px 8px;min-width:0;text-align:left;cursor:pointer;color:#fafafa;font:inherit}
.lt-pc:hover{border-color:#4a4a4a}
.lt-pc.me{border-left-color:#8b7cff}.lt-pc.me .lt-nm{color:#8b7cff}
.lt-pc.fa{border-left-color:#5fd08a}
.lt-nm{font-weight:600;font-size:13px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.lt-pc small{display:block;font-size:11px;color:#8f8f8f;margin-top:2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.lt-pp{color:#8b7cff}
.lt-empty{opacity:.4;text-align:center;cursor:default;border-left-color:#292929}
.lt-short{display:none}
.lt-ppu{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:6px}
.lt-ppd{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:6px;width:66%;margin:6px auto 0}
.lt-gg{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:6px;max-width:680px;margin:0 auto}
.lt-legend{font-size:12px;color:#8f8f8f;display:flex;flex-wrap:wrap;gap:12px;margin:8px 0 10px}
.lt-dot{display:inline-block;width:9px;height:9px;border-radius:2px;margin-right:4px;vertical-align:-1px}
.lt-msg{font-size:13px;color:#8f8f8f;padding:10px 0}
.lt-how{font-size:12px;color:#8f8f8f;margin-top:8px}
.lt-how summary{cursor:pointer;color:#8b7cff}
@media(max-width:640px){.lt-full{display:none}.lt-short{display:inline}.lt-ppd{width:100%}.lt-next{display:none}
.lt-grid{grid-template-columns:22px repeat(3,minmax(0,1fr));gap:4px}.lt-grid.d{grid-template-columns:22px repeat(2,minmax(0,1fr))}
.lt-pc{padding:6px}.lt-tr{padding:10px 8px;gap:8px}}
`;
  if (!document.getElementById("lt2-css")) {
    const el = document.createElement("style"); el.id = "lt2-css"; el.textContent = CSS; document.head.appendChild(el);
  }

  // ---------- lookups ----------
  function build(s, L) {
    const byKey = {}, byName = {}, byId = {};
    s.players.forEach((p) => {
      const k = nk(p.n);
      byKey[k + "|" + p.p] = byKey[k + "|" + p.p] || p;
      byName[k] = byName[k] || p;
      if (typeof p.id === "string" && p.id[0] === "e") byId[p.id.slice(1)] = p;
    });
    const teams = (L && L.teams) || {};
    const where = {};
    Object.entries(teams).forEach(([t, T]) => {
      const ln = T.lines || {};
      [...ES_F, ...ES_D, "G"].forEach((sl) => (ln[sl] || []).forEach((n) => { const id = nk(n) + "|" + t; where[id] = where[id] || { t, name: n }; if (!where[id].es) where[id].es = sl; }));
      ["PP1", "PP2"].forEach((sl) => (ln[sl] || []).forEach((n) => { const id = nk(n) + "|" + t; where[id] = where[id] || { t, name: n }; if (!where[id].pp) where[id].pp = sl; }));
    });
    const fpOf = (k, g) => {
      for (const x of g ? [g] : ["F", "D"]) {
        const a = ((L && L.fp) || {})[k + "|" + x], b = ((L && L.fpl) || {})[k + "|" + x];
        if (a || b) return { cur: a || null, last: b || null };
      }
      return { cur: null, last: null };
    };
    const pOf = (k, g) => (g && byKey[k + "|" + g]) || byName[k] || null;
    const latestES = {}, latestPP = {}, cutoff = Date.now() - 48 * 36e5;
    ((L && L.changes) || []).forEach((c) => {
      if (Date.parse(c.at) < cutoff) return;
      const id = c.key + "|" + c.team;
      if ((c.type === "line" || c.type === "lineup") && !latestES[id]) latestES[id] = c;
      if (c.type === "pp" && !latestPP[id]) latestPP[id] = c;
    });
    const items = [], seen = new Set();
    s.players.forEach((p) => { const k = nk(p.n), id = k + "|" + p.t; if (seen.has(id)) return; seen.add(id); items.push({ name: p.n, key: k, t: p.t, g: p.p, p }); });
    Object.entries(teams).forEach(([t, T]) => Object.entries(T.lines || {}).forEach(([sl, arr]) => (arr || []).forEach((n) => {
      const k = nk(n), id = k + "|" + t; if (seen.has(id)) return; seen.add(id);
      items.push({ name: n, key: k, t, g: grpOf(sl) || "F", p: pOf(k, grpOf(sl)) });
    })));
    return { byId, where, fpOf, pOf, latestES, latestPP, items, useThis: L && L.fp_use === "this" };
  }

  // ---------- importance score ----------
  // role size x who it affects x how recent. Changes scoring TH or more are "worth a look".
  const RW = { F1: 3, D1: 3, PP1: 3, F2: 2, D2: 2, PP2: 1.5, F3: 1, D3: 1, F4: 0.5, G: 2 };
  const BASE = { me: { up: 4, dn: 4, inj: 4 }, fa: { up: 2, dn: 0.4, inj: 0.6 }, other: { up: 0.8, dn: 0.8, inj: 1 }, none: { up: 0.3, dn: 0.2, inj: 0.3 } };
  const TH = 4;
  function roleOf(c, ctx) {
    if (c.type === "line" || c.type === "lineup" || c.type === "pp") return c.dir === "up" || c.dir === "in" ? c.to : c.from;
    const w = ctx.where[c.key + "|" + c.team];
    if (!w) return "NHL";
    return (RW[w.pp] || 0) > (RW[w.es] || 0) ? w.pp : w.es;
  }
  function enrich(L, ctx, s, opp) {
    return ((L && L.changes) || []).map((c) => {
      let p = c.e ? ctx.byId[c.e] : null;
      if (!p) { const q = ctx.pOf(c.key, c.g); if (q && q.t === c.team) p = q; }
      const ok = p ? (p.ft === s.me ? "me" : p.ft === "fa" ? "fa" : "other") : c.who === "mine" ? "me" : c.who === "fa" ? "fa" : "none";
      const dc = c.type === "status" ? "inj" : c.dir === "up" || c.dir === "in" ? "up" : "dn";
      const role = roleOf(c, ctx);
      let mates = [];
      if (ok !== "me" && ["line", "lineup", "pp"].includes(c.type) && dc === "up" && c.to) {
        const arr = ((((L.teams || {})[c.team] || {}).lines || {})[c.to]) || [];
        mates = arr.filter((n) => nk(n) !== c.key).filter((n) => { const q = ctx.pOf(nk(n), grpOf(c.to)); return q && q.ft === s.me && q.t === c.team; });
      }
      const oppHit = !!(p && opp && p.ft === opp);
      const hrs = (Date.now() - Date.parse(c.at)) / 36e5;
      const rec = hrs <= 1 ? 1 : hrs <= 6 ? 0.85 : hrs <= 24 ? 0.75 : hrs <= 48 ? 0.6 : 0.4;
      const w = BASE[ok][dc] + (mates.length ? 1.5 : 0) + (oppHit ? 1 : 0);
      return { c, p, ok, dc, role, mates, oppHit, s: (RW[role] || 0.5) * w * rec };
    }).sort((a, b) => b.s - a.s || Date.parse(b.c.at) - Date.parse(a.c.at));
  }
  function why(x) {
    const R = RW[x.role] || 0.5, c = x.c;
    if (x.ok === "me") return c.type === "status" ? "Your player · injury update" : "Your player";
    if (x.mates.length) {
      const m = x.mates.join(", ").replace(/, ([^,]*)$/, " and $1");
      return c.type === "pp" ? `Joins your ${m} on ${c.to}` : grpOf(c.to) === "D" ? `New partner for your ${m}` : `New linemate for your ${m}`;
    }
    if (x.oppHit) return "Your opponent's player this week";
    if (c.type === "status") return R >= 2 ? "Injury news for a top-role player" : "Injury update";
    if (x.ok === "fa" && x.dc === "up" && R >= 2) return "Free agent moving into a top role";
    if (c.type === "move") return "Roster move";
    if (R <= 1) return "Depth move";
    return x.ok === "fa" ? "Free agent" : x.ok === "other" ? "Rostered in your league" : "Not in your league";
  }
  function txt(c) {
    switch (c.type) {
      case "line": return `${c.dir === "up" ? "up" : "down"}: ${LBL[c.from] || c.from} → ${LBL[c.to] || c.to}`;
      case "lineup": return c.dir === "in" ? `into the lineup on the ${LBL[c.to] || c.to}` : `out of the lineup (was ${LBL[c.from] || c.from}) · scratched, hurt or moved`;
      case "pp": return c.dir === "up" ? `moved onto ${c.to || "PP1"}` : `off ${c.from || "PP1"}`;
      case "move": return c.dir === "in" ? `added to ${c.to}'s NHL roster` : `removed from ${c.from}'s NHL roster`;
      case "status": return `${pretty(c.from)} → ${pretty(c.to)}`;
      default: return c.text || "";
    }
  }
  function iconOf(c) {
    const up = c.dir === "up" || c.dir === "in";
    if (c.type === "line") return [up ? "▲" : "▼", up ? "lt-up" : "lt-dn"];
    if (c.type === "lineup") return [up ? "↪" : "↩", up ? "lt-up" : "lt-dn"];
    if (c.type === "pp") return ["PP", up ? "lt-up" : "lt-dn"];
    if (c.type === "status") return ["✚", c.to === "ACTIVE" ? "lt-up" : "lt-dn"];
    return ["⇄", "lt-mu"];
  }

  function Own({ x, s, H }) {
    if (x.ok === "me") return <span className="lt-own me">yours</span>;
    if (x.ok === "fa") return <span className="lt-own fa">FA</span>;
    return <span className="lt-own">{x.p ? (H.TL ? <H.TL s={s} id={x.p.ft} /> : H.teamName(s, x.p.ft)) : ""}</span>;
  }
  function Row({ x, s, H, onPick, dim }) {
    const c = x.c, [ic, cl] = iconOf(c);
    return (
      <div className={"lt-it" + (dim && x.s < TH ? " lt-low" : "")} onClick={() => onPick(x)}>
        <span className={"lt-ic " + cl}>{ic}</span>
        <div style={{ minWidth: 0 }}>
          <div className="text-sm"><b>{c.name}</b> <span className="lt-tm">{c.team}</span> {txt(c)}</div>
          <div className="lt-why">{why(x)} · {ago(c.at)}</div>
        </div>
        <Own x={x} s={s} H={H} />
      </div>
    );
  }

  // ---------- changes feed ----------
  const FILTERS = [["all", "All"], ["mine", "Mine & linemates"], ["fa", "Free agents"], ["lines", "Lines & PP"], ["moves", "Injuries & roster"]];
  function Feed({ items, s, H, L, onPick }) {
    const [flt, setFlt] = useState("all");
    const [all, setAll] = useState(false);
    const [more, setMore] = useState(false);
    const [openG, setOpenG] = useState({});
    const pass = (x) => flt === "mine" ? x.ok === "me" || x.mates.length > 0 : flt === "fa" ? x.ok === "fa"
      : flt === "lines" ? ["line", "lineup", "pp"].includes(x.c.type) : flt === "moves" ? ["move", "status"].includes(x.c.type) : true;
    const list = items.filter(pass), imp = list.filter((x) => x.s >= TH);
    let body;
    if (!all) {
      const shown = more ? imp : imp.slice(0, 6);
      body = (
        <div>
          {shown.length ? shown.map((x) => <Row key={x.c.id} x={x} s={s} H={H} onPick={onPick} />) : <div className="lt-msg">Nothing important here right now. Tap "Show all" to see every change.</div>}
          {imp.length > 6 && <button className="lt-link" onClick={() => setMore(!more)}>{more ? "Show fewer" : `Show ${imp.length - 6} more worth a look`}</button>}
        </div>
      );
    } else {
      const g = {}; list.forEach((x) => (g[x.c.team] = g[x.c.team] || []).push(x));
      const teams = Object.keys(g).sort((a, b) => g[b][0].s - g[a][0].s);
      body = teams.length ? (
        <div>
          {teams.map((t) => {
            const xs = g[t], up = xs.filter((x) => x.dc === "up").length, dn = xs.filter((x) => x.dc === "dn").length, inj = xs.length - up - dn;
            const isOpen = t in openG ? openG[t] : xs[0].s >= TH;
            const nm = (((L.teams || {})[t] || {}).st || {}).name || t;
            return (
              <div key={t}>
                <div className="lt-grp-h" onClick={() => setOpenG({ ...openG, [t]: !isOpen })}>
                  <span className="lt-chev" style={{ transform: isOpen ? "rotate(180deg)" : "none" }}>▾</span>
                  {H.TeamLogo ? <H.TeamLogo t={t} size={22} /> : null}<b>{nm}</b>
                  <span className="lt-mu" style={{ fontSize: 12 }}>{xs.length} change{xs.length > 1 ? "s" : ""} · <span className="lt-up">▲{up}</span> <span className="lt-dn">▼{dn}</span>{inj ? <span> ✚{inj}</span> : null}</span>
                </div>
                {isOpen && <div className="lt-grp-b">{xs.map((x) => <Row key={x.c.id} x={x} s={s} H={H} onPick={onPick} dim />)}</div>}
              </div>
            );
          })}
        </div>
      ) : <div className="lt-msg">No changes in this filter.</div>;
    }
    return (
      <H.Section title="Line & roster changes" sub={`Checked ${ago(L.lines_at)} · ${imp.length} of ${list.length} changes matter to you. Your phone still gets alerts for your players and for free agents who move into a top role.`}>
        <div className="mb-2"><H.Pills items={FILTERS} value={flt} onChange={(v) => { setFlt(v); setMore(false); }} /></div>
        {body}
        <div className="lt-bar">
          <span>{all ? "Faded rows are low priority (depth moves, scratches, call-ups)." : `${list.length - imp.length} minor changes hidden`}</span>
          <button className="lt-link" style={{ padding: 0 }} onClick={() => setAll(!all)}>{all ? "Back to important only" : `Show all ${list.length} changes`}</button>
        </div>
        <details className="lt-how"><summary>How changes are ranked</summary>
          Each change gets a score from three things: how big the role is (1st line, top pair and PP1 count most; 4th line, 3rd pair and scratches count least), who it affects (your players and their new linemates first, then free agents moving up, then your opponent this week, then everyone else), and how recent it is. Only changes that score high enough show here; everything else is under "Show all".
        </details>
      </H.Section>
    );
  }

  // ---------- player card inside a team ----------
  function PCard({ n, t, g, mode, ctx, s, H, onPick }) {
    if (!n) return <div className="lt-pc lt-empty"><div className="lt-nm">—</div><small>open spot</small></div>;
    const k = nk(n), p = ctx.pOf(k, g);
    const cls = p && p.ft === s.me ? " me" : p && p.ft === "fa" ? " fa" : "";
    const f = ctx.fpOf(k, g), v = ctx.useThis ? f.cur : f.last;
    const w = ctx.where[k + "|" + t] || {};
    const bits = [<span key="v">{v ? H.f1(v[0]) : "no pts yet"}</span>];
    if (mode === "es" && w.pp === "PP1") bits.push(<span key="pp" className="lt-pp">PP1</span>);
    const ch = mode === "pp" ? ctx.latestPP[k + "|" + t] : ctx.latestES[k + "|" + t];
    if (ch) {
      const up = ch.dir === "up" || ch.dir === "in";
      const label = ch.type === "lineup" ? (up ? "new in lineup" : "moved") : ch.type === "pp" ? (up ? "new on " + (ch.to || "PP1") : "off " + (ch.from || "PP1")) : "was " + (SHORT[ch.from] || ch.from);
      bits.push(<span key="c" className={up ? "lt-up" : "lt-dn"}>{up ? "▲ " : "▼ "}{label}</span>);
    }
    const hurt = p && p.status && p.status !== "ACTIVE";
    if (hurt) bits.push(<span key="i" className="lt-dn">{INJ[p.status] || pretty(p.status)}</span>);
    const own = p ? (p.ft === s.me ? "Yours" : p.ft === "fa" ? "Free agent" : "Owned by " + H.teamName(s, p.ft)) : "Not in your league's player list";
    const parts = n.split(" ");
    const short = parts.length > 1 ? parts[0][0] + ". " + parts.slice(1).join(" ") : n;
    return (
      <button className={"lt-pc" + cls} title={`${n} · ${own}`} onClick={() => onPick({ name: n, key: k, t, g: g || (p ? p.p : "F"), p })}>
        <div className="lt-nm"><span className="lt-full">{n}</span><span className="lt-short">{short}</span>{hurt ? <span className="lt-dn" style={{ marginLeft: 3 }}>✚</span> : null}</div>
        <small>{bits.map((b, i) => <React.Fragment key={i}>{i ? " · " : ""}{b}</React.Fragment>)}</small>
      </button>
    );
  }

  // ---------- one team, opened ----------
  function TeamBody({ t, T, tab, setTab, chg, ctx, s, H, onPick, onPickChange }) {
    const ln = T.lines || {};
    const val = (n, g) => { const f = ctx.fpOf(nk(n), g), v = ctx.useThis ? f.cur : f.last; return v ? v[0] : -1; };
    const sorted = (sl, g) => [...(ln[sl] || [])].sort((a, b) => val(b, g) - val(a, g));
    const pad = (a, n) => { const o = a.slice(); while (o.length < n) o.push(null); return o; };
    const card = (n, g, mode, key) => <PCard key={key} n={n} t={t} g={g} mode={mode} ctx={ctx} s={s} H={H} onPick={onPick} />;
    const gOf = (n) => { const w = ctx.where[nk(n) + "|" + t]; const g = w && w.es ? grpOf(w.es) : null; if (g) return g; const p = ctx.pOf(nk(n)); return p ? p.p : "F"; };
    const st = tab || "lines";
    const tabs = (
      <div className="lt-stabs">
        {[["lines", "Lines"], ["pp", "Power play"], ["chg", `Changes (${chg.length})`]].map(([k, l]) => <button key={k} className={"lt-stab" + (st === k ? " on" : "")} onClick={() => setTab(k)}>{l}</button>)}
      </div>
    );
    if (st === "chg") return <div>{tabs}<div style={{ marginTop: 8 }}>{chg.length ? chg.map((x) => <Row key={x.c.id} x={x} s={s} H={H} onPick={onPickChange} dim />) : <div className="lt-msg">No changes for this team right now.</div>}</div></div>;
    if (!ln.F1) return <div>{tabs}<div className="lt-msg">Lines not available yet.</div></div>;
    if (st === "pp") {
      const unit = (sl) => {
        const arr = ln[sl] || [];
        if (!arr.length) return <div className="lt-msg">Not available.</div>;
        const fw = arr.filter((n) => gOf(n) !== "D").sort((a, b) => val(b, "F") - val(a, "F"));
        const df = arr.filter((n) => gOf(n) === "D").sort((a, b) => val(b, "D") - val(a, "D"));
        const all = [...fw, ...df], top = all.slice(0, 3), bot = all.slice(3);
        return (
          <div>
            <div className="lt-ppu">{top.map((n) => card(n, gOf(n), "pp", sl + n))}</div>
            {bot.length > 0 && <div className="lt-ppd">{bot.map((n) => card(n, gOf(n), "pp", sl + n))}</div>}
          </div>
        );
      };
      return <div>{tabs}<div className="lt-sec">1st power-play unit</div>{unit("PP1")}<div className="lt-sec">2nd power-play unit</div>{unit("PP2")}</div>;
    }
    return (
      <div>
        {tabs}
        <div className="lt-sec">Forwards</div>
        <div className="lt-grid">
          {ES_F.map((sl) => <React.Fragment key={sl}><div className="lt-rl">{SHORT[sl]}</div>{pad(sorted(sl, "F"), 3).map((n, i) => card(n, "F", "es", sl + i))}</React.Fragment>)}
        </div>
        <div className="lt-sec">Defence pairs</div>
        <div className="lt-grid d">
          {ES_D.map((sl) => <React.Fragment key={sl}><div className="lt-rl">{SHORT[sl]}</div>{pad(sorted(sl, "D"), 2).map((n, i) => card(n, "D", "es", sl + i))}</React.Fragment>)}
        </div>
        <div className="lt-sec">Goalies</div>
        <div className="lt-gg">{pad(sorted("G", "G"), 2).map((n, i) => card(n, "G", "es", "G" + i))}</div>
      </div>
    );
  }

  // ---------- ranked team list ----------
  function Teams({ L, ctx, items, s, H, onPick, onPickChange }) {
    const [sort, setSort] = useState("standings");
    const [onlyMine, setOnlyMine] = useState(false);
    const [open, setOpen] = useState({});
    const [tabs, setTabs] = useState({});
    const st = (T) => T.st || {};
    const rows = Object.entries(L.teams || {}).map(([t, T]) => ({ t, T }));
    rows.sort((a, b) => (st(b.T).pts || 0) - (st(a.T).pts || 0) || (st(b.T).pct || 0) - (st(a.T).pct || 0)
      || ((st(b.T).gf || 0) - (st(b.T).ga || 0)) - ((st(a.T).gf || 0) - (st(a.T).ga || 0)));
    const today = H.todayISO();
    rows.forEach((x, i) => {
      x.rank = i + 1;
      x.mine = s.players.filter((p) => p.ft === s.me && p.t === x.t && !p.ir);
      x.chg = items.filter((it) => it.c.team === x.t);
      x.best = x.chg.find((it) => it.s >= TH);
      x.next = ((L.sched || {})[x.t] || []).find((g) => g.d >= today);
    });
    const S = {
      standings: (a, b) => a.rank - b.rank,
      fp: (a, b) => (b.T.fp || 0) - (a.T.fp || 0),
      chg: (a, b) => b.chg.length - a.chg.length || a.rank - b.rank,
      mine: (a, b) => b.mine.length - a.mine.length || a.rank - b.rank,
    };
    const shown = rows.filter((x) => !onlyMine || x.mine.length).sort(S[sort]);
    return (
      <H.Section title="Teams" sub={`Daily Faceoff lines, checked ${ago(L.lines_at)}. # = NHL standings (${L.st_src}). Tap a team for its lines, power play and changes; tap a player for full details.`}>
        <div className="flex flex-wrap gap-2 items-center">
          <H.Pills items={[["standings", "NHL standings"], ["fp", "Fantasy points"], ["chg", "Most changes"], ["mine", "My players"]]} value={sort} onChange={setSort} />
          <label className="flex items-center gap-1 text-xs"><input type="checkbox" checked={onlyMine} onChange={(e) => setOnlyMine(e.target.checked)} /> Only teams with my players</label>
        </div>
        <div className="lt-legend">
          <span><span className="lt-dot" style={{ background: "#8b7cff" }}></span>Yours</span>
          <span><span className="lt-dot" style={{ background: "#5fd08a" }}></span>Free agent</span>
          <span><span className="lt-dot" style={{ background: "#4d4d4d" }}></span>Rostered</span>
          <span><span className="lt-up">▲</span>/<span className="lt-dn">▼</span> moved in last 48 h</span>
          <span><span className="lt-dn">✚</span> injured</span>
          <span>Numbers = {L.fp_season} fantasy pts</span>
        </div>
        {shown.map((x) => {
          const isOpen = !!open[x.t], sd = st(x.T);
          let hint = null;
          if (x.best) { const [ic, cl] = iconOf(x.best.c); hint = <div className="lt-hint"><span className={cl}>{ic}</span> {x.best.c.name} {txt(x.best.c)} <span className="lt-mu">· {why(x.best)}</span></div>; }
          return (
            <div key={x.t} className={"lt-team" + (isOpen ? " open" : "")}>
              <div className="lt-tr" onClick={() => setOpen({ ...open, [x.t]: !isOpen })}>
                <div className="lt-rk">#{x.rank}</div>
                {H.TeamLogo ? <div style={{ flexShrink: 0 }}><H.TeamLogo t={x.t} size={32} /></div> : null}<div className="lt-tmain">
                  <div className="lt-tn">{sd.name || x.t}</div>
                  <div className="lt-meta">
                    {sd.gp ? `${sd.w}-${sd.l}-${sd.otl} · ${sd.pts} pts · ` : ""}{Math.round(x.T.fp || 0)} fantasy pts
                    <span className="lt-next">{x.next ? ` · next ${H.dayLabel(x.next.d)} ${x.next.h ? "vs" : "@"} ${x.next.o}` : ""}</span>
                  </div>
                  {hint}
                </div>
                <div className="lt-pills">
                  {x.mine.length ? <span className="lt-pill me">{x.mine.length} yours</span> : null}
                  {x.chg.length ? <span className="lt-pill">{x.chg.length} change{x.chg.length > 1 ? "s" : ""}</span> : null}
                </div>
                <div className="lt-chev">▾</div>
              </div>
              {isOpen && (
                <div className="lt-body">
                  <TeamBody t={x.t} T={x.T} tab={tabs[x.t]} setTab={(k) => setTabs({ ...tabs, [x.t]: k })} chg={x.chg} ctx={ctx} s={s} H={H} onPick={onPick} onPickChange={onPickChange} />
                </div>
              )}
            </div>
          );
        })}
        {!shown.length && <div className="lt-msg">No teams match.</div>}
      </H.Section>
    );
  }

  // ---------- player detail card (unchanged from the old Lines tab) ----------
  function PlayerCard({ it, s, wk, H, L, ctx, onClose, onPick }) {
    const K = s.blend, today = H.todayISO(), p = it.p;
    const hasId = !!(p && typeof p.id === "string" && p.id[0] === "e");
    const isG = it.g === "G";
    const w = ctx.where[it.key + "|" + it.t] || null;
    const ln = ((L.teams || {})[it.t] || {}).lines || {};
    const mates = w && w.es && w.es !== "G" ? (ln[w.es] || []).filter((n) => nk(n) !== it.key) : [];
    const f = ctx.fpOf(it.key, it.g);
    const per = (d) => { if (!hasId) return null; const g = isG ? H.gStart(p, d) : null; return { x: H.effAvg(p, K, d) * (g ? g.v : p.prob) * H.avail(p, d), g }; };
    const games = ((L.sched || {})[it.t] || []).filter((x) => x.d >= today).slice(0, 6);
    const wkIdx = hasId ? (wk.games[p.t] || []).filter((i) => ((wk.dates || [])[i] || "") >= today && !(H.gState && H.gState(p.t, wk.dates[i]).s !== "P")) : [];
    const wkPts = wkIdx.reduce((a, i) => a + ((per(wk.dates[i]) || {}).x || 0), 0);
    const back = hasId ? H.effBack(p) : { d: "" };
    const inj = hasId ? (((window.__SIG || {}).injuries) || {})[p.id.slice(1)] : null;
    const news = hasId ? (H.sigOf(p).news || []) : [];
    const hist = (L.changes || []).filter((c) => c.key === it.key && (c.team === it.t || c.from === it.t || c.to === it.t)).slice(0, 6);
    const fmt = (v) => (v ? `${v[1]} GP · ${H.f1(v[1] ? v[0] / v[1] : 0)}/game` : "no games");
    const hurt = hasId && ((p.status && p.status !== "ACTIVE") || (back.d && back.d > today));
    const LT = H.LiveTag || (() => null), started = (d) => !!(H.gState && H.gState(it.t, d).s !== "P"), tn = hasId && started(today) ? { a: realPts(p, today), st: H.gState(it.t, today).s } : null;
    return (
      <div className="mt-3 border border-slate-200 rounded-xl p-3 bg-slate-50">
        <div className="flex items-start gap-2">
          <div>
            <div className="text-lg font-bold">{it.name}</div>
            <div className="text-xs text-slate-500">
              {isG ? "Goalie" : it.g === "D" ? "Defence" : "Forward"} · {it.t} · {p ? (H.TL ? <H.TL s={s} id={p.ft} /> : H.teamName(s, p.ft)) : "not in your league's ESPN player list"}
              {p && p.own ? ` · ${H.f1(p.own)}% rostered` : ""}{p && p.chg ? ` (${p.chg > 0 ? "+" : ""}${H.f1(p.chg)}%)` : ""}
            </div>
          </div>
          <button className="ml-auto text-xs text-slate-500" onClick={onClose}>✕ close</button>
        </div>
        <div className="mt-2 text-sm">
          {w && w.es ? (
            <span>{isG ? `Goalie for ${it.t}` : `${LBL[w.es]} for ${it.t}`}{mates.length ? " with " : ""}
              {mates.map((n, i) => <span key={n}>{i ? " & " : ""}<button className="underline" onClick={() => onPick({ name: n, key: nk(n), t: it.t, g: grpOf(w.es), p: ctx.pOf(nk(n), grpOf(w.es)) })}>{n}</button></span>)}
            </span>
          ) : <span className="text-amber-600">Not in {it.t}'s current Daily Faceoff lineup (scratched, injured, in the minors, or not read yet)</span>}
          {!isG && <span className="text-slate-500"> · {w && w.pp ? `on ${w.pp}` : "no power-play unit"}</span>}
        </div>
        {hurt && <div className="text-sm text-red-600 mt-1">✚ {String(p.status || "").replace(/_/g, " ")}{back.d ? ` · back around ${H.dayLabel(back.d)} (${back.src})` : ""}{inj && inj.note ? ` — ${inj.note}` : ""}</div>}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-2 mt-3">
          <H.Card label={`${L.season} fantasy pts`} value={hasId ? H.f1(p.tot || 0) : f.cur ? H.f1(f.cur[0]) : "–"} sub={hasId ? <>{p.gp ? `${p.gp} GP · ${H.f1(p.tot / p.gp)}/game` : "no games yet"}{tn ? <> · tonight {tn.a == null ? "–" : H.f1(tn.a)} <LT st={tn.st} /></> : null}</> : fmt(f.cur)} />
          <H.Card label="Last season" value={f.last ? H.f1(f.last[0]) : "–"} sub={fmt(f.last)} />
          <H.Card label="Projection / game" value={hasId ? H.f1(H.effAvg(p, K)) : "–"} sub={hasId ? `${MODE[window.__PMODE] || ""} mode · ESPN ${H.f1(p.avg)}${p.gp ? ` · was ${H.f1(H.effAvg({ ...p, gp: 0, tot: 0 }, K))} before ${p.gp} game${p.gp === 1 ? "" : "s"}` : ""}` : "no projection"} />
          <H.Card label="Rest of this week" value={hasId ? H.f1(wkPts) : "–"} sub={`${wkIdx.length} game${wkIdx.length === 1 ? "" : "s"} left`} />
        </div>
        {games.length > 0 && (
          <div className="mt-3">
            <div className="font-medium text-sm mb-1">Next games</div>
            <table className="w-full text-sm"><tbody>
              {games.map((g) => { const r = per(g.d); return (
                <tr key={g.d} className="border-t border-slate-100">
                  <td className="py-1 pr-2 whitespace-nowrap">{H.dayLabel(g.d)}</td>
                  <td className="py-1 pr-2">{g.h ? "vs" : "@"} {g.o}</td>
                  <td className="py-1 pr-2 text-xs text-slate-500">{r && r.g ? r.g.l || `${Math.round(r.g.v * 100)}% start chance` : ""}</td>
                  <td className="py-1 text-right font-semibold">{hasId && started(g.d) ? <>{realPts(p, g.d) == null ? "–" : H.f1(realPts(p, g.d))} <LT st={H.gState(it.t, g.d).s} /></> : r ? H.f1(r.x) : ""}</td>
                </tr>); })}
            </tbody></table>
          </div>
        )}
        {hasId && <div className="mt-2"><H.Tags p={p} K={K} /></div>}
        {news.length > 0 && <div className="mt-3"><div className="font-medium text-sm mb-1">News</div>
          {news.map((n, i) => <div key={i} className="text-xs"><span className="text-slate-400 mr-2">{n.d}</span><a href={n.u} target="_blank" rel="noreferrer" className={"underline " + (n.tone === "-" ? "text-red-600" : "text-slate-600")}>{n.h}</a></div>)}</div>}
        {hist.length > 0 && <div className="mt-3"><div className="font-medium text-sm mb-1">Recent changes</div>
          {hist.map((c) => <div key={c.id} className="text-xs"><span className="text-slate-400 mr-2">{ago(c.at)}</span>{c.text}</div>)}</div>}
      </div>
    );
  }

  // ---------- the tab ----------
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
    if (!L) return <H.Section title="Lines">No line data yet. It appears after the next sync once gm_lines.py is set up.</H.Section>;
    const pick = (it) => { setSel(it); window.scrollTo({ top: 0, behavior: "smooth" }); };
    const pickChange = (x) => pick({ name: x.c.name, key: x.c.key, t: x.c.type === "move" && x.c.dir === "in" && x.c.to ? x.c.to : x.c.team, g: x.c.g || (x.p ? x.p.p : "F"), p: x.p || ctx.pOf(x.c.key, x.c.g) });
    const qq = nk(q);
    const results = qq.length < 2 ? [] : ctx.items.filter((i) => i.key.includes(qq))
      .sort((a, b) => (b.key.startsWith(qq) - a.key.startsWith(qq)) || ((b.p ? b.p.own : 0) - (a.p ? a.p.own : 0))).slice(0, 8);
    return (
      <div className="space-y-4">
        <H.Section title="Ask about a player" sub="Type any NHL player's name to see his line, power-play unit, season fantasy points, projections, schedule, injury and news in one place.">
          <input className={H.inp + " w-full"} placeholder="Player name, e.g. MacKinnon" value={q} onChange={(e) => setQ(e.target.value)} />
          {results.length > 0 && <div className="flex flex-wrap gap-2 mt-2">{results.map((it) => (
            <button key={it.key + it.t} onClick={() => { setSel(it); setQ(""); }} className="px-2 py-1 rounded-lg border border-slate-300 text-xs">
              {it.name} <span className="text-slate-400">{it.g} · {it.t}{it.p ? " · " + H.teamName(s, it.p.ft) : ""}</span>
            </button>))}</div>}
          {qq.length >= 2 && !results.length && <div className="text-xs text-slate-400 mt-2">No player matches "{q}".</div>}
          {sel && <PlayerCard it={sel} s={s} wk={wk} H={H} L={L} ctx={ctx} onClose={() => setSel(null)} onPick={pick} />}
        </H.Section>
        <Feed items={items} s={s} H={H} L={L} onPick={pickChange} />
        <Teams L={L} ctx={ctx} items={items} s={s} H={H} onPick={pick} onPickChange={pickChange} />
      </div>
    );
  }

  // ---------- compact summary for the Today screen ----------
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

  // ---------- player pop-up used everywhere in the app ----------
  function PlayerPopup({ p, s, wk, H, onClose }) {
    const L = window.LINES_DATA || { teams: {}, changes: [], sched: {}, season: "This season" };
    const ctx = useMemo(() => build(s, L), [s.players, L && L.generated]);
    const [it, setIt] = useState(null);
    useEffect(() => { setIt(null); }, [p && p.id]);
    useEffect(() => { const k = (e) => { if (e.key === "Escape") onClose(); }; window.addEventListener("keydown", k); return () => window.removeEventListener("keydown", k); }, []);
    const real = s.players.find((q) => q.id === p.id) || p;
    const cur = it || { name: real.n, key: nk(real.n), t: real.t, g: real.p, p: real };
    return (
      <div className="fixed inset-0 z-50 overflow-y-auto" style={{ background: "rgba(0,0,0,.65)" }} onClick={onClose}>
        <div className="max-w-2xl mx-auto my-10 px-3" onClick={(e) => e.stopPropagation()}>
          <PlayerCard it={cur} s={s} wk={wk} H={H} L={L} ctx={ctx} onClose={onClose} onPick={setIt} />
        </div>
      </div>
    );
  }

  window.PlayerPopup = PlayerPopup;
  window.LinesSummary = LinesSummary;
  window.LinesTab = LinesTab;
})();
