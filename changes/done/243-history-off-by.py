# changes/243-history-off-by.py - AI Lab history, Matchups: how far each projection was off for each team, and a "What was off" list of the players who missed their projection the most

PAGE = "ai-history.html"

CSS = r'''.mo{font-size:12px}
.wo{margin:4px 0 2px}
.wo summary{cursor:pointer;font-size:13px;color:var(--tx);padding:6px 0;list-style:none;text-decoration:underline;text-decoration-color:var(--line2);text-underline-offset:3px}
.wo summary::-webkit-details-marker{display:none}
.wg{display:grid;grid-template-columns:1fr 1fr;gap:18px;padding:4px 0 8px}
.wt{font-size:13px;font-weight:600;margin-bottom:2px;display:flex;justify-content:space-between;gap:8px}
.wr{display:grid;grid-template-columns:minmax(0,1fr) 44px 44px 50px;gap:6px;align-items:center;font-size:12.5px;padding:3px 0;border-top:1px solid var(--line)}
.wr.wh{font-size:11px;color:var(--mu);border-top:0}
.wr>.n{text-align:right}
.wn{font-size:11.5px;color:var(--mu);padding-top:4px}
@media(max-width:640px){.wg{grid-template-columns:1fr;gap:12px}}
</style>'''

CALC_OLD = '''      const byT = {};
      recs.forEach(r => { if (r.ft && !OUTS[r.status]) (byT[r.ft] = byT[r.ft] || []).push(r); });'''
CALC_NEW = '''      const byT = {};
      recs.forEach(r => { if (r.ft && !OUTS[r.status]) (byT[r.ft] = byT[r.ft] || []).push(r); });
      /* change 243: each player's projection (the app's Combined one) against what he scored */
      recs.forEach(r => {
        if (!r.ft || OUTS[r.status]) return;
        const P = (pl[r.ft] = pl[r.ft] || {}), k = r.pid || r.name;
        const x = P[k] = P[k] || {n: r.name, pos: r.pos, t: r.team, p: 0, a: 0, g: 0, s: 0};
        let v = r.combo != null ? r.combo : pred(r);
        if (v != null && r.pos === "G") v *= r.start_p != null ? r.start_p : r.ai_start_p != null ? r.ai_start_p : 0.5;
        x.p += v || 0;
        if (r.played) { x.a += +r.fp || 0; x.g++; } else if (r.pos !== "G") x.s++;
      });'''

def page(t):
    t = lit(t, "243: styles", "</style>", CSS, ".wo summary{cursor:pointer")
    t = lit(t, "243: player list kept", "    const proj = {};\n    MODELS.forEach(([k]) => { proj[k] = {}; });", "    const proj = {}, pl = {};\n    MODELS.forEach(([k]) => { proj[k] = {}; });", "const proj = {}, pl = {};")
    t = lit(t, "243: player sums", CALC_OLD, CALC_NEW, "change 243: each player's projection")
    t = lit(t, "243: returned", "return {pairs: pairs, proj: proj, got: got, n: w.dates.length, done: done};", "return {pairs: pairs, proj: proj, pl: pl, got: got, n: w.dates.length, done: done};", "proj: proj, pl: pl,")
    t = lit(t, "243: off rows and what was off",
            "    return `<div class=\"mt\">${line(m.home, 1, sa)}${line(m.away, -1, sb)}${mark}</div>`;",
            r'''    /* change 243: how far off each projection was, and the players who missed the most */
    const sg = x => (x >= 0 ? "+" : "\u2212") + Math.abs(Math.round(x));
    const off = (id, side, sc) => R.done && R.got ? `<div class="mg mo"><span class="mu ell">${nm(id)} off by</span>`
      + MODELS.map(([k]) => `<span class="n mu">${sg(sc - (side > 0 ? J[k].pa : J[k].pb))}</span>`).join("") + `<span></span></div>` : "";
    const who = id => {
      const L = Object.values((R.pl || {})[id] || {}).map(x => Object.assign({}, x, {d: x.a - x.p})).filter(x => x.p > 0.05 || x.a);
      const tp = L.reduce((a, x) => a + x.p, 0), ta = L.reduce((a, x) => a + x.a, 0);
      const top = L.sort((a, b) => Math.abs(b.d) - Math.abs(a.d)).slice(0, 6);
      return `<div><div class="wt"><span class="ell">${nm(id)}</span><span class="mu">all players ${sg(ta - tp)}</span></div>`
        + `<div class="wr wh"><span>Player</span><span class="n">Scored</span><span class="n">Proj</span><span class="n">Off</span></div>`
        + top.map(x => `<div class="wr"><span class="ell">${esc(x.n)} <span class="mu">${esc(x.pos)} \u00b7 ${esc(x.t)} \u00b7 ${x.g} GP${x.s ? " \u00b7 missed " + x.s : ""}</span></span><span class="n">${f1(x.a)}</span><span class="n mu">${f1(x.p)}</span><span class="n ${x.d >= 0 ? "up" : "dn"}">${(x.d >= 0 ? "+" : "\u2212") + f1(Math.abs(x.d))}</span></div>`).join("")
        + `</div>`;
    };
    const why = R.done && R.got ? `<details class="wo"><summary>What was off</summary><div class="wg">${who(m.home)}${who(m.away)}</div>`
      + `<div class="wn">Players who scored the most above or below their projection this week, using the app's own projection (Combined). \u201cAll players\u201d adds up everyone on the team, bench included, so it can differ from the lineup numbers above. \u201cMissed\u201d is games the projection expected him to play but he didn't.</div></details>` : "";
    return `<div class="mt">${line(m.home, 1, sa)}${line(m.away, -1, sb)}${mark}${off(m.home, 1, sa)}${off(m.away, -1, sb)}${why}</div>`;''',
            "change 243: how far off each projection was")
    return t

edit(PAGE, page)
