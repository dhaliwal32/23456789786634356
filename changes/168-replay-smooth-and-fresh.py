# changes/168-replay-smooth-and-fresh.py - goal replay: smooth movement (glides between tracking frames), circles readable in dark and light (blue filled with white numbers, white with dark numbers), and an open page that is older than the newest app reloads itself once so new parts never show without their styling

NEW_EDGE = r'''function GxEdge165({ e, s, x }) {
  /* change 168: smooth glide between frames */
  const F = e.F, fr = F.f || [], n = fr.length, gi = Math.max(0, Math.min(F.gi == null ? n - 1 : F.gi, n - 1));
  const D0 = n > 1 ? fr[n - 1][0] : 0, even = !(D0 > 2000 && D0 < 60000);
  const tOf = (k) => (even ? k * 100 : fr[k][0]);
  const T = n ? tOf(n - 1) : 0;
  const [ms, setMs] = useState(0);
  const [play, setPlay] = useState(true);
  const [run, setRun] = useState(0);
  const [ol166, setOl166] = useState(false);
  useEffect(() => {
    if (!play || n < 2) return undefined;
    let raf = 0;
    const t0 = performance.now() - ms;
    const step = (now) => {
      const m = Math.min(T, now - t0);
      setMs(m);
      if (m >= T) { setPlay(false); return; }
      raf = requestAnimationFrame(step);
    };
    raf = requestAnimationFrame(step);
    return () => cancelAnimationFrame(raf);
  }, [play, run]);
  if (!n) return null;
  let k = 0;
  while (k < n - 1 && tOf(k + 1) <= ms) k++;
  const k2 = Math.min(n - 1, k + 1), span = tOf(k2) - tOf(k), fq = span > 0 ? Math.max(0, Math.min(1, (ms - tOf(k)) / span)) : 0;
  const nx = {};
  ((fr[k2] || [0, []])[1]).forEach((o) => { nx[o[0]] = o; });
  const row = ((fr[k] || [0, []])[1]).map((o) => { const b = nx[o[0]]; return b ? [o[0], o[1], o[2], o[3] + (b[3] - o[3]) * fq, o[4] + (b[4] - o[4]) * fq] : o; });
  const scT = e.v.team || F.team, ro = F.ro || {};
  const gRow = ((fr[gi] || [0, []])[1]).filter((o) => o[0]);
  const code = String(F.sc || e.v.sc || ""), scHome = scT === (F.home || e.v.home);
  const mySk = +(scHome ? code[2] : code[1]), opSk = +(scHome ? code[1] : code[2]);
  const pp = code.length === 4 && mySk > opSk;
  const isG = (o) => ((ro[o[0]] || [])[1] || "") === "G";
  const teams = [scT].concat([...new Set(gRow.map((o) => o[1]))].filter((t) => t !== scT));
  return (
    <div className="gx-ed165" data-gx="168">
      <svg viewBox="-102 -45 204 90" role="img" aria-label="Goal replay with every player on the ice">
        {gxRinkBg165()}
        {row.map((o) => (o[0] ? (
          <g key={"p" + o[0]}><circle cx={o[3]} cy={o[4]} r="3.7" className={o[1] === scT ? "sc" : "ot"} /><text x={o[3]} y={o[4] + 1.25} textAnchor="middle" fontSize="3.4" className={o[1] === scT ? "sc" : "ot"}>{o[2]}</text></g>
        ) : null))}
        {row.filter((o) => !o[0]).map((o, j) => <circle key={"pk" + j} cx={o[3]} cy={o[4]} r="1.5" className="pk" />)}
      </svg>
      <div className="ct">
        <button type="button" onClick={() => { setMs(0); setPlay(true); setRun((r) => r + 1); }} aria-label="Replay">{"↻"}</button>
        <button type="button" onClick={() => { if (ms >= T) setMs(0); setPlay(!play); setRun((r) => r + 1); }}>{play ? "Pause" : "Play"}</button>
        <button type="button" onClick={() => { setPlay(false); setMs(tOf(gi)); }}>Goal moment</button>
        <span className="lg"><i className="sc"></i>{scT}<i className="ot"></i>{teams[1] || ""}</span>
      </div>
      <button type="button" className="dd166" onClick={() => setOl166(!ol166)}>Who was on the ice <i className={ol166 ? "up" : ""}>{"▾"}</i></button>
      <div className="ol" style={ol166 ? null : { display: "none" }}>
        <div className="hd">On the ice at the goal{pp ? " (power play, no plus/minus)" : ""}</div>
        {teams.map((t) => (
          <div key={t} className="tm"><div className="tn">{t + (t === scT ? " (scored)" : "")}</div>
            {gRow.filter((o) => o[1] === t).sort((a, b) => (isG(a) ? 1 : 0) - (isG(b) ? 1 : 0) || a[2] - b[2]).map((o) => {
              const r = ro[o[0]] || [], nm = r[0] || "#" + o[2], p = gxFind131(t, o[2], nm), tag = gxTag131(s, p);
              const pm = isG(o) || pp || code.length !== 4 ? "" : t === scT ? "+1" : "-1";
              return <div key={o[0]} className="pl"><span className="truncate">{"#" + o[2] + " "}{p && window.__NAV ? <button type="button" className="hover:underline" onClick={() => window.__NAV.player(p)}>{shortN(nm)}</button> : shortN(nm)}{isG(o) ? " (G)" : ""}{tag ? <span className="tg">{" (" + tag + ")"}</span> : null}</span><b>{pm}</b></div>;
            })}
          </div>
        ))}
      </div>
    </div>
  );
}
'''

NEW_CSS = r'''  /* change 168 (install.py) */
  .gx-ed165 circle.sc { fill: #2563eb !important; stroke: #ffffff !important; stroke-width: .5 !important; }
  .gx-ed165 text.sc { fill: #ffffff !important; }
  .gx-ed165 circle.ot { fill: #ffffff !important; stroke: #111111 !important; stroke-width: .6 !important; }
  .gx-ed165 text.ot { fill: #111111 !important; }
  .gx-ed165 circle.pk { fill: #111111 !important; stroke: #ffffff !important; stroke-width: .5 !important; }
  .gx-ed165 .ct .lg i.sc { background: #2563eb !important; box-shadow: none !important; }
  .gx-ed165 .ct .lg i.ot { background: #ffffff !important; box-shadow: inset 0 0 0 1.5px #111111 !important; }
</style>'''


def cut(t, label, start, end, new, done):
    if done in t:
        print("(install) " + label + ": already done")
        return t
    a = t.find(start)
    if a < 0 or t.count(start) != 1:
        fail(label + ": start text not found exactly once")
    b = t.find(end, a)
    if b < 0:
        fail(label + ": end text not found")
    print("(install) " + label + ": updated")
    return t[:a] + new + t[b + len(end):]


def app(t):
    t = lit(t, "168: styles", "</style>", NEW_CSS, "change 168 (install.py)")
    t = cut(t, "168: smooth replay", "function GxEdge165({ e, s, x }) {\n", "\n  );\n}\n", NEW_EDGE, "change 168: smooth glide between frames")
    t = lit(t, "168: page id for the build check", "    window.__GX_FAST = c[1];", "    window.__GX_FAST = c[1]; window.__GX_PAGE = c[0]; /* gx168 */", "window.__GX_PAGE = c[0]; /* gx168 */")
    return t


def build(t):
    return lit(t, "168: build checks the page",
               '  const app = "/* built from " + page + " - do not edit, run Install changes instead */\\n" + trApp(src, page);',
               '  const app = "/* built from " + page + " - do not edit, run Install changes instead */\\n" + GUARD168(hash(src)) + trApp(src, page);',
               "GUARD168(hash(src))")


def build2(t):
    return lit(t, "168: guard helper",
               "const OPEN = '<script type=\"text/babel\">';",
               "const OPEN = '<script type=\"text/babel\">';\n"
               "// change 168: a page older than this build reloads itself once (GitHub serves the newest build to every page)\n"
               "const GUARD168 = (h) => '(function(){var p=window.__GX_PAGE;if(!p||p===\"' + h + '\")return;var k=\"gx168-reload\";var s=\"\";try{s=sessionStorage.getItem(k)||\"\";}catch(e){}if(s===p)return;try{sessionStorage.setItem(k,p);}catch(e){}location.replace(location.pathname+\"?v=\"+Date.now()+location.hash);throw new Error(\"gx168: reloading a newer page\");})();\\n';",
               "const GUARD168 = (h) =>")


edit(APP, app)
edit("build_app.js", build2)
edit("build_app.js", build)
