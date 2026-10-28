# changes/111-lines-rink.py - new Lines page: search a team and its lineup appears on an ice rink (lines, pairs, goalies; power play and penalty kill tabs), team logo faint in the middle, your players and free agents marked, recent line changes below

NEW_CSS = r'''  /* change 111 (install.py) */
  .gx-ln111 .srch { position: relative; }
  .gx-ln111 .sug { position: absolute; left: 0; right: 0; top: 100%; z-index: 20; margin-top: 4px; background: var(--card); border: 1px solid var(--line2); border-radius: 12px; overflow: hidden; animation: gx101-in .15s ease-out; }
  .gx-ln111 .sug button { display: flex; align-items: center; gap: 10px; width: 100%; padding: 10px 12px; text-align: left; border-top: 1px solid var(--line); }
  .gx-ln111 .sug button:first-child { border-top: 0; }
  .gx-ln111 .rec { display: flex; gap: 8px; flex-wrap: wrap; margin-top: 10px; }
  .gx-ln111 .rec button { display: inline-flex; align-items: center; gap: 6px; padding: 5px 10px 5px 6px; border: 1px solid var(--line2); border-radius: 999px; font-size: 13px; }
  .gx-ln111 .hd { display: flex; align-items: center; gap: 12px; margin: 16px 2px 10px; }
  .gx-ln111 .hd .nm { font-size: 20px; font-weight: 700; line-height: 1.1; }
  .gx-ln111 .hd .rc { font-size: 13px; color: var(--mute); }
  .gx-rk111 { position: relative; border-radius: 44px; border: 2px solid var(--line2); overflow: hidden; padding: 26px 10px 22px; background: color-mix(in srgb, #8fbce6 13%, var(--card)); animation: gx101-in .25s ease-out; }
  .gx-rk111 .ice { position: absolute; inset: 0; pointer-events: none; }
  .gx-rk111 .logo { position: absolute; left: 50%; top: 50%; transform: translate(-50%, -50%); opacity: .09; pointer-events: none; }
  .gx-rk111 .row { position: relative; display: grid; grid-template-columns: 22px repeat(var(--n), minmax(0, 1fr)); gap: 6px; align-items: stretch; margin: 5px 0; }
  .gx-rk111 .row .lb { display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: 700; color: var(--mute); writing-mode: vertical-rl; transform: rotate(180deg); letter-spacing: .06em; }
  .gx-rk111 .sp { height: 14px; }
  .gx-pc111 { display: flex; flex-direction: column; align-items: center; gap: 1px; padding: 6px 3px 5px; border-radius: 14px; background: color-mix(in srgb, var(--card) 88%, transparent); border: 1px solid var(--line); text-align: center; min-width: 0; transition: transform .12s, border-color .15s; }
  .gx-pc111.me { border-color: var(--accent); box-shadow: inset 0 0 0 1px var(--accent); }
  .gx-pc111.fa { border-color: var(--good); }
  .gx-pc111 .n { font-size: 13px; font-weight: 600; max-width: 100%; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; margin-top: 2px; }
  .gx-pc111 .o { font-size: 10px; letter-spacing: .03em; color: var(--mute); max-width: 100%; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .gx-pc111.me .o { color: var(--accent); font-weight: 700; }
  .gx-pc111.fa .o { color: var(--good); font-weight: 700; }
  .gx-pc111 .v { font-size: 12px; font-variant-numeric: tabular-nums; color: var(--ink2); }
  .gx-pc111.empty { opacity: .4; }
  .gx-ln111 .gx-seg103 { margin-bottom: 10px; }
  .gx-ln111 .chg { padding: 9px 0; border-top: 1px solid var(--line); font-size: 13px; }
  .gx-ln111 .chg:first-of-type { border-top: 0; }
  .gx-ln111 .chg small { display: block; color: var(--mute); font-size: 11px; }
  @media (max-width: 640px) { .gx-rk111 { border-radius: 36px; padding: 22px 6px 18px; } .gx-pc111 .n { font-size: 12px; } .gx-rk111 .row { gap: 5px; } }
</style>'''

HELPERS = r'''// ---------- change 111: Lines on an ice rink (install.py) ----------
const GX_ORD111 = { lw: 0, l: 0, c: 1, rw: 2, r: 2, ld: 3, rd: 4, d: 3, g: 5 };
function GxRinkLines111({ teamCode }) {
  const t = teamCode;
  return (
    <svg className="ice" viewBox="0 0 100 200" preserveAspectRatio="none" aria-hidden="true">
      <line x1="0" y1="12" x2="100" y2="12" style={{ stroke: "rgba(220,38,38,.35)", strokeWidth: 0.6 }} vectorEffect="non-scaling-stroke" />
      <line x1="0" y1="66" x2="100" y2="66" style={{ stroke: "rgba(37,99,235,.45)", strokeWidth: 1.6 }} vectorEffect="non-scaling-stroke" />
      <line x1="0" y1="100" x2="100" y2="100" style={{ stroke: "rgba(220,38,38,.45)", strokeWidth: 1.6 }} vectorEffect="non-scaling-stroke" />
      <line x1="0" y1="134" x2="100" y2="134" style={{ stroke: "rgba(37,99,235,.45)", strokeWidth: 1.6 }} vectorEffect="non-scaling-stroke" />
      <line x1="0" y1="188" x2="100" y2="188" style={{ stroke: "rgba(220,38,38,.35)", strokeWidth: 0.6 }} vectorEffect="non-scaling-stroke" />
      <ellipse cx="50" cy="100" rx="16" ry="8" style={{ fill: "none", stroke: "rgba(37,99,235,.3)", strokeWidth: 0.8 }} vectorEffect="non-scaling-stroke" />
      <path d="M42 188 A8 4 0 0 1 58 188" style={{ fill: "rgba(37,99,235,.10)", stroke: "rgba(220,38,38,.35)", strokeWidth: 0.6 }} vectorEffect="non-scaling-stroke" />
    </svg>
  );
}
function GxLines111({ s }) {
  const L = window.LINES_DATA || { teams: {}, changes: [] };
  const teams = Object.keys(L.teams || {}).filter((t) => ((L.teams[t] || {}).lines || {}).F1).sort();
  const [t, setT] = useState(() => window.__LINES_TEAM || uiGet().ln111 || "");
  const [q, setQ] = useState("");
  const [open, setOpen] = useState(false);
  const [mode, setMode] = useState("es");
  const [recent, setRecent] = useState(() => uiGet().ln111r || []);
  useEffect(() => {
    const h = (e) => { if (e && e.detail) pick(e.detail); };
    window.addEventListener("gm-lines-team", h);
    return () => window.removeEventListener("gm-lines-team", h);
  }, []);
  const pick = (code) => {
    setT(code); setQ(""); setOpen(false); uiSet("ln111", code); window.__LINES_TEAM = "";
    setRecent((r) => { const n = [code, ...r.filter((x) => x !== code)].slice(0, 6); uiSet("ln111r", n); return n; });
  };
  const nameOf = (c) => (((L.teams[c] || {}).st || {}).name) || c;
  const qq = nrm(q);
  const hits = qq.length < 1 ? [] : teams.filter((c) => nrm(c).startsWith(qq) || nrm(nameOf(c)).split(" ").some((w) => w.startsWith(qq)) || nrm(nameOf(c)).includes(qq)).slice(0, 6);
  const T = L.teams[t] || null, ln = (T && T.lines) || {}, df = ((T && T.pos) || {}).df || {};
  const byName = useMemo(() => { const o = {}; s.players.forEach((p) => { const k = nrm(p.n); if (!o[k] || p.t === t) o[k] = p; }); return o; }, [s.players, t]);
  const ord = (arr) => [...(arr || [])].sort((a, b) => (GX_ORD111[df[a]] ?? 9) - (GX_ORD111[df[b]] ?? 9));
  const chip = (n, i) => {
    if (!n) return <div key={"e" + i} className="gx-pc111 empty"><span className="n">{"-"}</span></div>;
    const p = byName[nrm(n)], mine = p && p.ft === s.me, fa = p && p.ft === "fa";
    const last = n.split(" ").slice(1).join(" ") || n;
    const tn = (teamName(s, p ? p.ft : "") || "").replace(/[^A-Za-z0-9' ]/g, " ").trim().split(/\s+/)[0] || "";
    const own = !p ? "" : mine ? "YOURS" : fa ? (p.wv ? "WAIVERS" : "FA") : tn;
    return (
      <button key={n + i} type="button" className={"gx-pc111" + (mine ? " me" : fa ? " fa" : "")} onClick={() => { if (p && window.__NAV) window.__NAV.player(p); }}>
        {p ? <GxFace p={p} size={22} /> : <span style={{ height: 29 }}></span>}
        <span className="n">{last}</span>
        <span className="o">{own}</span>
        {p ? <span className="v">{f1(gxPgAvg(p, s.blend))}</span> : null}
      </button>
    );
  };
  const row = (lb, arr, n) => {
    const a = ord(arr);
    while (a.length < n) a.push("");
    return <div key={lb} className="row" style={{ "--n": n }}><span className="lb">{lb}</span>{a.slice(0, n).map(chip)}</div>;
  };
  const rows = mode === "pp" ? [row("PP1", ln.PP1, 5), <div key="s1" className="sp"></div>, row("PP2", ln.PP2, 5)]
    : mode === "pk" ? [row("PK1", ln.PK1, 4), <div key="s1" className="sp"></div>, row("PK2", ln.PK2, 4)]
    : [row("L1", ln.F1, 3), row("L2", ln.F2, 3), row("L3", ln.F3, 3), row("L4", ln.F4, 3), <div key="s1" className="sp"></div>,
       row("D1", ln.D1, 2), row("D2", ln.D2, 2), row("D3", ln.D3, 2), <div key="s2" className="sp"></div>, row("G", ln.G, 2)];
  const chg = t ? (L.changes || []).filter((c) => c.team === t || c.from === t || c.to === t).slice(0, 6) : [];
  const st = (T && T.st) || {};
  return (
    <div className="gx-ln111">
      <div className="srch">
        <input className={inp + " w-full"} placeholder="Search a team" value={q} onFocus={() => setOpen(true)} onBlur={() => setTimeout(() => setOpen(false), 150)} onChange={(e) => { setQ(e.target.value); setOpen(true); }} />
        {open && hits.length ? (
          <div className="sug">{hits.map((c) => <button key={c} type="button" onMouseDown={(e) => e.preventDefault()} onClick={() => pick(c)}><TeamLogo t={c} size={24} /><span>{nameOf(c)}</span><span className="text-xs text-slate-500" style={{ marginLeft: "auto" }}>{c}</span></button>)}</div>
        ) : null}
      </div>
      {recent.length ? <div className="rec">{recent.map((c) => <button key={c} type="button" onClick={() => pick(c)}><TeamLogo t={c} size={18} />{c}</button>)}</div> : null}
      {T ? (
        <>
          <div className="hd">
            <TeamLogo t={t} size={40} />
            <div className="min-w-0"><div className="nm truncate">{nameOf(t)}</div>{st.w != null ? <div className="rc">{st.w + "-" + st.l + "-" + st.otl + (st.streak ? " · " + st.streak : "")}</div> : null}</div>
          </div>
          <div className="gx-seg103">{[["es", "Even strength"], ["pp", "Power play"], ["pk", "Penalty kill"]].map(([k, l]) => <button key={k} type="button" className={mode === k ? "on" : ""} onClick={() => setMode(k)}>{l}</button>)}</div>
          <div key={t + mode} className="gx-rk111">
            <GxRinkLines111 teamCode={t} />
            <span className="logo"><TeamLogo t={t} size={220} /></span>
            {rows}
          </div>
          {chg.length ? (
            <div className="gx-pn" style={{ marginTop: 12 }}>
              <div className="gx-tag" style={{ marginBottom: 4 }}>Recent changes</div>
              {chg.map((c) => <div key={c.id} className="chg">{c.text}<small>{dayLabel(String(c.at || "").slice(0, 10))}</small></div>)}
            </div>
          ) : null}
        </>
      ) : <div className="text-sm text-slate-500" style={{ marginTop: 14 }}>Search a team to see its lines.</div>}
    </div>
  );
}
'''


def change(t):
    t = lit(t, "111: styles", "</style>", NEW_CSS, "change 111 (install.py)")
    t = lit(t, "111: helpers", ROOT, HELPERS + ROOT, "change 111: Lines on an ice rink")
    t = lit(t, "111: lines page", 'else if (tab === "lines") content = window.LinesTab ?', 'else if (tab === "lines") content = true ? <GxLines111 {...P} /> : window.LinesTab ?', "<GxLines111 {...P} />")
    return t


edit(APP, change)
