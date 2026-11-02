# changes/191-game-log-past-seasons.py - Player screen Game log: a season picker (This season, 2025-26, 2024-25 ... back to 2008-09) shows that season's games from ai/history, and an average line under the heading: this season's average and last season's average (fantasy points per game played)

HELPERS = r'''// ---------- change 191: game log for past seasons from ai/history (install.py) ----------
const GXH191 = (window.__GXH191 = window.__GXH191 || { idx: null, seas: {} });
function gxHistIdx191() {
  if (!GXH191.idx) GXH191.idx = fetch("ai/history/index.json").then((r) => (r.ok ? r.json() : {})).catch(() => ({}));
  return GXH191.idx;
}
// the week files are gzip; open them in the browser
function gxGz191(u) {
  return fetch(u).then((r) => (r.ok ? r.arrayBuffer() : null)).then((b) => {
    if (!b) return [];
    const u8 = new Uint8Array(b);
    if (u8[0] === 0x1f && u8[1] === 0x8b) {
      if (typeof DecompressionStream === "undefined") return [];
      return new Response(new Blob([b]).stream().pipeThrough(new DecompressionStream("gzip"))).json();
    }
    try { return JSON.parse(new TextDecoder().decode(u8)); } catch (e) { return []; }
  }).catch(() => []);
}
// one season: regular-season games grouped by name + F/D/G, newest first
function gxSeason191(sea) {
  if (!GXH191.seas[sea]) {
    GXH191.seas[sea] = gxHistIdx191().then((I) => Promise.all(Object.keys(I || {}).filter((k) => k.indexOf(sea + "/") === 0).sort().map((k) => gxGz191("ai/history/" + k + ".json.gz")))).then((parts) => {
      const by = {};
      parts.forEach((L) => (Array.isArray(L) ? L : []).forEach((r) => {
        if (String(r.g).slice(4, 6) !== "02") return;
        const k = nrm(r.n) + "|" + r.pos;
        (by[k] = by[k] || []).push(r);
      }));
      Object.values(by).forEach((L) => L.sort((a, b) => (a.d < b.d ? 1 : a.d > b.d ? -1 : 0)));
      return by;
    }).catch(() => ({}));
  }
  return GXH191.seas[sea];
}
const gxMS191 = (t) => { const v = +t || 0; return Math.floor(v / 60) + ":" + String(Math.round(v % 60)).padStart(2, "0"); };
const gxSeaLbl191 = (k) => String(k).slice(0, 4) + "-" + String(k).slice(6, 8);
// a history row in the same shape as a box score line, with fantasy points from the league scoring
function gxRow191(r, sc) {
  if (r.pos === "G") {
    const x = { sv: r.SV || 0, ga: r.GA || 0, dec: r.W ? "W" : r.OTL ? "O" : r.GS ? "L" : "", svp: r.SA ? (r.SV || 0) / r.SA : null, toi: gxMS191(r.toi), o: r.o, h: r.h };
    return { d: r.d, x, fp: gxEst(x, sc) + (r.SO ? sc.SO ?? 0 : 0), est: false, st: "F", h191: true };
  }
  const x = { g: r.G || 0, a: r.A || 0, pm: r.PM || 0, sog: r.SOG || 0, hit: r.HIT || 0, blk: r.BLK || 0, ppg: r.PPP || 0, pim: "-", toi: gxMS191(r.toi), o: r.o, h: r.h };
  return { d: r.d, x, fp: gxEst(x, sc) + (r.SHP || 0) * (sc.SHP ?? 0), est: false, st: "F", h191: true };
}
const gxAvg191 = (L) => { const q = (L || []).filter((r) => !r.dnp && r.fp != null && r.st !== "L" && r.st !== "P"); return q.length ? [q.reduce((t, r) => t + r.fp, 0) / q.length, q.length] : null; };
'''

OLD_STATE = r'''  const [nLog, setNLog] = useState(100000); /* gx118: full log */'''
NEW_STATE = r'''  const [nLog, setNLog] = useState(100000); /* gx118: full log */
  /* change 191: past seasons */
  const [sea191, setSea191] = useState("cur");
  const [seas191, setSeas191] = useState([]);
  const [hist191, setHist191] = useState(null);
  const [prev191, setPrev191] = useState(null);
  const key191 = nrm(p.n) + "|" + (p.p === "G" ? "G" : p.p === "D" ? "D" : "F");
  useEffect(() => {
    let dead = false;
    setSea191("cur"); setPrev191(null);
    gxHistIdx191().then((I) => {
      const L = [...new Set(Object.keys(I || {}).map((k) => k.split("/")[0]))].sort().reverse().slice(1);
      if (dead) return;
      setSeas191(L);
      if (L[0]) gxSeason191(L[0]).then((by) => { if (!dead) setPrev191(((by || {})[key191] || []).map((r) => gxRow191(r, sc))); });
      else setPrev191([]);
    });
    return () => { dead = true; };
  }, [p.id]);
  useEffect(() => {
    let dead = false;
    if (sea191 === "cur") return undefined;
    setHist191(null);
    gxSeason191(sea191).then((by) => { if (!dead) setHist191(((by || {})[key191] || []).map((r) => gxRow191(r, sc))); });
    return () => { dead = true; };
  }, [sea191, p.id]);'''

OLD_TAB = '''          {tab === "log" ? (
            <div className="gx-pd-pn">
              <div className="gx-pd-h">Game log<span className="r">{log && log.length ? log.length + " games" : ""}</span></div>'''
NEW_TAB = '''          {tab === "log" ? ((log) => (
            <div className="gx-pd-pn">
              <div className="gx-pd-h gx-gh191">Game log<select className={inp + " sl191"} value={sea191} onChange={(e) => setSea191(e.target.value)} aria-label="Season"><option value="cur">This season</option>{seas191.map((k) => <option key={k} value={k}>{gxSeaLbl191(k)}</option>)}</select></div>
              <div className="gx-av191">{(() => { const a = gxAvg191(log), b = gxAvg191(prev191), cur = sea191 === "cur"; return <>
                <span>{log === null ? "" : a ? <><b>{f1(a[0])}</b>{" avg \\u00b7 " + a[1] + " GP"}</> : "No games"}</span>
                {cur && seas191[0] ? <span>{gxSeaLbl191(seas191[0]) + ": "}{prev191 === null ? "..." : b ? <><b>{f1(b[0])}</b>{" avg \\u00b7 " + b[1] + " GP"}</> : "no games"}</span> : null}
              </>; })()}</div>'''

OLD_END = '''                {log.some((r) => r.est) ? <div className="text-xs text-slate-500" style={{ marginTop: 8 }}>* worked out from the box score, without power-play or shorthanded points.</div> : null}
              </>)}
            </div>
          ) : null}'''
NEW_END = '''                {log.some((r) => r.est) ? <div className="text-xs text-slate-500" style={{ marginTop: 8 }}>* worked out from the box score, without power-play or shorthanded points.</div> : null}
                {log.some((r) => r.h191) ? <div className="text-xs text-slate-500" style={{ marginTop: 8 }}>Past seasons: points worked out from each game's stats with your league's scoring (PIM not saved).</div> : null}
              </>)}
            </div>
          ))(sea191 === "cur" ? log : hist191) : null}'''

NEW_CSS = r'''  /* change 191 (install.py) */
  .gx-gh191 { display: flex; align-items: center; gap: 10px; }
  .gx-gh191 .sl191 { margin-left: auto; width: auto; max-width: 150px; height: 32px; padding: 0 28px 0 10px; font-size: 13px; text-transform: none; letter-spacing: 0; font-weight: 400; }
  .gx-av191 { display: flex; gap: 18px; align-items: center; height: 22px; margin: -2px 0 8px; font-size: 13px; color: var(--mute); white-space: nowrap; overflow: hidden; }
  .gx-av191 > span { min-width: 0; overflow: hidden; text-overflow: ellipsis; }
  .gx-av191 b { color: var(--ink); font-weight: 600; }
</style>'''


def change(t):
    t = lit(t, "191: styles", "</style>", NEW_CSS, "change 191 (install.py)")
    t = lit(t, "191: helpers", ROOT, HELPERS + ROOT, "change 191: game log for past seasons")
    t = lit(t, "191: season state", OLD_STATE, NEW_STATE, "change 191: past seasons")
    t = lit(t, "191: season picker and averages", OLD_TAB, NEW_TAB, "gx-pd-h gx-gh191")
    t = lit(t, "191: past season rows", OLD_END, NEW_END, "))(sea191 === \"cur\" ? log : hist191)")
    return t


edit(APP, change)
