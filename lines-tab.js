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
/* round 32 theme */
.lt-it{display:grid;grid-template-columns:26px 1fr auto;gap:8px;padding:8px 2px;border-top:1px solid var(--line);align-items:start;cursor:pointer}
.lt-it:first-child{border-top:none}
.lt-it:hover{background:var(--hover)}
.lt-low{opacity:.55}
.lt-ic{font-weight:700;font-size:12px;text-align:center;padding-top:2px}
.lt-up{color:var(--good)}.lt-dn{color:var(--bad)}.lt-mu{color:var(--mute)}
.lt-tm{font-size:11px;color:var(--mute);margin-right:2px}
.lt-why{font-size:12px;color:var(--mute);margin-top:1px}
.lt-own{font-size:12px;white-space:nowrap;padding-top:2px;color:var(--mute);max-width:130px;overflow:hidden;text-overflow:ellipsis}
.lt-own.me{color:var(--accent);font-weight:600}.lt-own.fa{color:var(--good)}
.lt-link{background:none;border:none;color:var(--accent);cursor:pointer;padding:8px 0 0;font-size:13px}
.lt-bar{display:flex;justify-content:space-between;align-items:center;gap:8px;flex-wrap:wrap;margin-top:10px;padding-top:10px;border-top:1px solid var(--line);font-size:12px;color:var(--mute)}
.lt-grp-h{display:flex;gap:8px;align-items:center;padding:8px 2px;border-top:1px solid var(--line);cursor:pointer;font-size:13px}
.lt-grp-b{padding:0 0 6px 16px}
.lt-team{border:1px solid var(--line);border-radius:12px;background:var(--card2);margin-bottom:8px;overflow:hidden}
.lt-team.open{border-color:var(--line2)}
.lt-tr{display:flex;align-items:center;gap:10px;padding:10px 12px;cursor:pointer}
.lt-tr:hover{background:var(--card3)}
.lt-rk{font-weight:700;width:34px;color:var(--mute);flex-shrink:0}
.lt-tmain{min-width:0;flex:1}
.lt-tn{font-weight:600;color:var(--ink)}
.lt-meta{font-size:12px;color:var(--mute)}
.lt-hint{font-size:12px;margin-top:2px;color:var(--ink2);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.lt-pills{display:flex;gap:6px;flex-wrap:wrap;justify-content:flex-end}
.lt-pill{font-size:11px;padding:2px 8px;border-radius:999px;border:1px solid var(--line2);color:var(--mute);white-space:nowrap}
.lt-pill.me{color:var(--accent);border-color:var(--line2)}
.lt-chev{color:var(--mute);transition:transform .2s;flex-shrink:0;display:inline-block}
.lt-team.open .lt-chev{transform:rotate(180deg)}
.lt-body{padding:10px 12px 14px;border-top:1px solid var(--line)}
.lt-stabs{display:flex;gap:6px;flex-wrap:wrap}
.lt-stab{background:transparent;border:1px solid var(--line2);color:var(--ink2);border-radius:999px;padding:4px 11px;font-size:13px;cursor:pointer}
.lt-stab.on{border-color:var(--accent);color:var(--accent);background:var(--accentSoft)}
.lt-sec{font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:var(--ink2);margin:14px 0 8px;background:var(--card3);padding:5px 8px;border-radius:6px;text-align:center;font-weight:600}
.lt-grid{display:grid;grid-template-columns:28px repeat(3,minmax(0,1fr));gap:6px}
.lt-grid.d{grid-template-columns:28px repeat(2,minmax(0,1fr));max-width:680px;margin:0 auto}
.lt-rl{font-size:12px;color:var(--mute);display:flex;align-items:center}
.lt-pc{display:block;width:100%;background:var(--card);border:1px solid var(--line);border-left:3px solid var(--faint);border-radius:8px;padding:7px 8px;min-width:0;text-align:left;cursor:pointer;color:var(--ink);font:inherit}
.lt-pc:hover{border-color:var(--line2)}
.lt-pc.me{border-left-color:var(--accent)}.lt-pc.me .lt-nm{color:var(--accent)}
.lt-pc.fa{border-left-color:var(--good)}
.lt-nm{font-weight:600;font-size:13px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.lt-pc small{display:block;font-size:11px;color:var(--mute);margin-top:2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.lt-pp{color:var(--accent)}
.lt-empty{opacity:.4;text-align:center;cursor:default;border-left-color:var(--line)}
.lt-short{display:none}
.lt-ppu{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:6px}
.lt-ppd{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:6px;width:66%;margin:6px auto 0}
.lt-gg{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:6px;max-width:680px;margin:0 auto}
.lt-legend{font-size:12px;color:var(--mute);display:flex;flex-wrap:wrap;gap:12px;margin:8px 0 10px}
.lt-dot{display:inline-block;width:9px;height:9px;border-radius:2px;margin-right:4px;vertical-align:-1px}
.lt-msg{font-size:13px;color:var(--mute);padding:10px 0}
.lt-how{font-size:12px;color:var(--mute);margin-top:8px}
.lt-how summary{cursor:pointer;color:var(--accent)}
@media(max-width:640px){.lt-full{display:none}.lt-short{display:inline}.lt-ppd{width:100%}.lt-next{display:none}
.lt-grid{grid-template-columns:22px repeat(3,minmax(0,1fr));gap:4px}.lt-grid.d{grid-template-columns:22px repeat(2,minmax(0,1fr))}
.lt-pc{padding:6px}.lt-tr{padding:10px 8px;gap:8px}}

/* lines v39 */
.lt-rink{border:1px solid var(--line2);border-radius:26px;padding:6px 14px 16px}
.lt-sec{background:none;text-align:left;padding:0;margin:14px 0 8px;font-size:12px;letter-spacing:.06em;text-transform:none;color:var(--mute);font-weight:400}
.lt-pc{border-left-width:1px;border-left-color:var(--line)}
.lt-pc.me{border-color:var(--accent)}
.lt-ps{font-size:11px;color:var(--faint);margin-bottom:1px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.lt-pp5{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:6px}
@media(max-width:640px){.lt-pp5{grid-template-columns:repeat(3,minmax(0,1fr))}.lt-rink{padding:4px 8px 12px;border-radius:18px}}
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
      <H.Section closed title="Line & roster changes" sub={`Checked ${ago(L.lines_at)} · ${imp.length} of ${list.length} changes matter to you. Your phone still gets alerts for your players and for free agents who move into a top role.`}>
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

  // ---------- player card inside a team (lines v39: real positions, points a game, hot and cold) ----------
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

  // ---------- game log: past games with box scores (news_logos.py round 31) ----------
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
            <span><button className="underline" title="Open this team's lines" onClick={() => { if (window.__NAV && window.__NAV.lines) window.__NAV.lines(it.t); }}>{isG ? `Goalie for ${it.t}` : `${LBL[w.es]} for ${it.t}`}</button>{mates.length ? " with " : ""}
              {mates.map((n, i) => <span key={n}>{i ? " & " : ""}<button className="underline" onClick={() => onPick({ name: n, key: nk(n), t: it.t, g: grpOf(w.es), p: ctx.pOf(nk(n), grpOf(w.es)) })}>{n}</button></span>)}
            </span>
          ) : <span className="text-amber-600">Not in {it.t}'s current Daily Faceoff lineup (scratched, injured, in the minors, or not read yet)</span>}
          {!isG && <span className="text-slate-500"> · {w && w.pp ? `on ${w.pp}` : "no power-play unit"}</span>}
        </div>
        {hurt && <div className="text-sm text-red-600 mt-1">✚ {String(p.status || "").replace(/_/g, " ")}{back.d ? ` · back around ${H.dayLabel(back.d)} (${back.src})` : ""}{inj && inj.note ? ` — ${inj.note}` : ""}</div>}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-2 mt-3">
          <H.Card label={`${L.season} fantasy pts`} value={hasId ? H.f1(p.tot || 0) : f.cur ? H.f1(f.cur[0]) : "–"} sub={hasId ? <>{p.gp ? `${p.gp} GP · ${H.f1(p.tot / p.gp)}/game` : "no games yet"}{tn ? <> · tonight {tn.a == null ? "–" : H.f1(tn.a)} <LT st={tn.st} t={it.t} dt={today} /></> : null}</> : fmt(f.cur)} />
          <H.Card label="Last season" value={f.last ? H.f1(f.last[0]) : "–"} sub={fmt(f.last)} />
          <H.Card label="Projection / game" value={hasId ? H.f1(H.effAvg(p, K)) : "–"} sub={hasId ? `${MODE[window.__PMODE] || ""} mode · ESPN ${H.f1(p.avg)}${p.gp ? ` · was ${H.f1(H.effAvg({ ...p, gp: 0, tot: 0 }, K))} before ${p.gp} game${p.gp === 1 ? "" : "s"}` : ""}` : "no projection"} />
          <H.Card label="Rest of this week" value={hasId ? H.f1(wkPts) : "–"} sub={`${wkIdx.length} game${wkIdx.length === 1 ? "" : "s"} left`} />
        </div>
        {(() => {
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
        {hasId ? <GameLog p={p} it={it} s={s} H={H} /> : null}
        {games.length > 0 && (
          <div className="mt-3">
            <div className="font-medium text-sm mb-1">Next games</div>
            <table className="w-full text-sm"><tbody>
              {games.map((g) => { const r = per(g.d); return (
                <tr key={g.d} className="border-t border-slate-100">
                  <td className="py-1 pr-2 whitespace-nowrap">{H.dayLabel(g.d)}</td>
                  <td className="py-1 pr-2">{g.h ? "vs" : "@"} {g.o}</td>
                  <td className="py-1 pr-2 text-xs text-slate-500">{r && r.g ? r.g.l || `${Math.round(r.g.v * 100)}% start chance` : ""}</td>
                  <td className="py-1 text-right font-semibold">{hasId && started(g.d) ? <>{realPts(p, g.d) == null ? "–" : H.f1(realPts(p, g.d))} <LT st={H.gState(it.t, g.d).s} t={it.t} dt={g.d} /></> : r ? H.f1(r.x) : ""}</td>
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

  // ---------- the tab (lines v39: one search box for teams and players) ----------
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
    const cur = it || { name: real.n, key: nk(real.n), t: real.t, g: real.p, p: real, gd: p.dt };
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
