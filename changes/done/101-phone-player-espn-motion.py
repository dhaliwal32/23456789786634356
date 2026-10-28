# changes/101-phone-player-espn-motion.py - phone player screen in the ESPN app layout (team colour header, big logo, photo on the right, number box, injury bar, pinned tabs); short game log replaces the news box in Overview; smoother motion (player screen slides up and down, tabs and pages fade in, buttons press in)

NEW_CSS = r'''  /* change 101 (install.py) */
  .gx-pdm, .gx-pdm-inj { display: none; }
  @media (max-width: 640px) {
    .gx-pd-hd, .gx-pd-ac { display: none !important; }
    .gx-pdm { display: block; position: relative; overflow: hidden; padding: 54px 16px 14px; border-bottom: 1px solid var(--line);
      background: linear-gradient(180deg, color-mix(in srgb, var(--tc) 55%, var(--card)) 0%, color-mix(in srgb, var(--tc) 22%, var(--card)) 62%, var(--card) 100%); }
    .gx-pdm .wm { position: absolute; left: 30px; top: 2px; opacity: .16; pointer-events: none; }
    .gx-pdm .top { position: relative; display: flex; align-items: flex-end; min-height: 150px; }
    .gx-pdm .info { position: relative; z-index: 1; flex: 1; min-width: 0; max-width: 66%; padding-bottom: 6px; }
    .gx-pdm .nm { font-size: 22px; line-height: 1.1; font-weight: 800; text-transform: uppercase; letter-spacing: .01em; color: #fff; text-shadow: 0 1px 2px rgba(0,0,0,.35); }
    .gx-pdm .ln { display: flex; align-items: center; gap: 6px; margin-top: 6px; font-size: 14px; color: rgba(255,255,255,.92); }
    .gx-pdm .ln a, .gx-pdm .ln button { color: rgba(255,255,255,.92) !important; }
    .gx-pdm .bt { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 12px; }
    .gx-pdm .bt button { padding: 6px 12px; border-radius: 999px; font-size: 13px; font-weight: 600; background: rgba(0,0,0,.55); color: #fff; border: 1px solid rgba(255,255,255,.25); }
    .gx-pdm .bt button.pr { background: #fff; color: #111; border-color: #fff; }
    .gx-pdm .ph { position: absolute; right: -34px; bottom: -14px; height: 168px; width: auto; z-index: 0; }
    .gx-pdm .strip { position: relative; z-index: 1; display: grid; grid-template-columns: repeat(4, 1fr); margin-top: 14px; border: 1px solid rgba(255,255,255,.18); border-radius: 12px; background: rgba(0,0,0,.35); padding: 10px 4px; text-align: center; }
    .gx-pdm .strip b { display: block; font-size: 20px; font-weight: 800; color: #fff; font-variant-numeric: tabular-nums; }
    .gx-pdm .strip span { display: block; font-size: 10px; letter-spacing: .04em; color: rgba(255,255,255,.75); margin-top: 2px; }
    .gx-pdm-inj { display: flex; justify-content: center; align-items: center; gap: 10px; padding: 10px 12px; background: var(--card); border-bottom: 1px solid var(--line); font-size: 14px; }
    .gx-pdm-inj .pill { background: var(--bad); color: #fff; font-weight: 700; font-size: 12px; letter-spacing: .04em; padding: 4px 10px; border-radius: 6px; }
    .gx-pd-x { color: #fff; z-index: 3; text-shadow: 0 1px 3px rgba(0,0,0,.5); }
    .gx-pd-tb { position: sticky; top: 0; z-index: 4; }
  }
  /* smoother motion */
  @keyframes gx101-fade { from { opacity: 0; } to { opacity: 1; } }
  @keyframes gx101-up { from { opacity: 0; transform: translateY(48px); } to { opacity: 1; transform: none; } }
  @keyframes gx101-pop { from { opacity: 0; transform: translateY(12px) scale(.98); } to { opacity: 1; transform: none; } }
  @keyframes gx101-in { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: none; } }
  .gx-pd-ov { animation: gx101-fade .2s ease-out; transition: opacity .2s ease-in; }
  .gx-pd { animation: gx101-pop .26s cubic-bezier(.2,.8,.2,1); transition: transform .2s ease-in, opacity .2s ease-in; }
  .gx-pd-ov.out { opacity: 0; }
  .gx-pd-ov.out .gx-pd { transform: translateY(24px); opacity: 0; }
  .gx-pd-bd { animation: gx101-in .22s ease-out; }
  .gx-pd-tb button { transition: color .15s, border-color .2s; }
  .gx-pg101 { animation: gx101-in .22s ease-out; }
  button, .gx-pk.row, [role="button"] { transition: transform .12s ease, background-color .15s, color .15s, border-color .15s, opacity .15s; }
  button:active, .gx-pk.row:active, [role="button"]:active { transform: scale(.97); }
  @media (max-width: 640px) {
    .gx-pd { animation: gx101-up .3s cubic-bezier(.2,.8,.2,1); }
    .gx-pd-ov.out .gx-pd { transform: translateY(70px); }
  }
  @media (prefers-reduced-motion: reduce) {
    .gx-pd-ov, .gx-pd, .gx-pd-bd, .gx-pg101 { animation: none !important; transition: none !important; }
    button:active, .gx-pk.row:active, [role="button"]:active { transform: none; }
  }
</style>'''

HELPERS = r'''// ---------- change 101: team colours for the phone player header (install.py) ----------
const GX_TC101 = { ANA: "#F47A38", BOS: "#FFB81C", BUF: "#003087", CGY: "#C8102E", CAR: "#CE1126", CHI: "#CF0A2C", COL: "#6F263D", CBJ: "#002654",
  DAL: "#006847", DET: "#CE1126", EDM: "#FF4C00", FLA: "#C8102E", LA: "#A2AAAD", MIN: "#154734", MTL: "#AF1E2D", NSH: "#FFB81C", NJ: "#CE1126",
  NYI: "#00539B", NYR: "#0038A8", OTT: "#C52032", PHI: "#F74902", PIT: "#FCB514", SJ: "#006D75", SEA: "#355464", STL: "#002F87", TB: "#002868",
  TOR: "#00205B", UTA: "#6CACE4", VAN: "#00205B", VGK: "#B4975A", WSH: "#C8102E", WPG: "#041E42" };
const gxTC101 = (t) => GX_TC101[t] || "#555555";
'''

PHONE_HEAD = r'''<div className="gx-pdm" style={{ "--tc": gxTC101(p.t) }}>
          <span className="wm"><TeamLogo t={p.t} size={260} /></span>
          <div className="top">
            <div className="info">
              <div className="nm">{p.n}</div>
              <div className="ln"><TeamLogo t={p.t} size={20} /><span>{p.t + " · " + posWord + (no != null ? " · #" + no : "")}</span></div>
              <div className="ln">{owner}</div>
              {Q ? (
                <div className="bt">
                  <button type="button" className="pr" onClick={act(Q.swap)}>{Q.mine(p) ? "Find a replacement" : "Find a swap"}</button>
                  {Q.tradeable(p) ? <button type="button" onClick={act(Q.trade)}>Trade</button> : <button type="button" onClick={() => Q.espn(p)}>Add on ESPN</button>}
                </div>
              ) : null}
            </div>
            {eid && img ? <img className="ph" alt="" src={"https://a.espncdn.com/i/headshots/nhl/players/full/" + eid + ".png"} onError={() => setImg(false)} /> : null}
          </div>
          <div className="strip">
            <div><b>{rk || "-"}</b><span>POS RANK</span></div>
            <div><b>{avgSoFar == null ? "-" : f1(avgSoFar)}</b><span>AVG FPTS</span></div>
            <div><b>{f1(p.tot || 0)}</b><span>SEASON FPTS</span></div>
            <div><b>{p.own != null ? (p.own >= 99.5 ? Math.round(p.own) : f1(p.own)) : "-"}</b><span>{"%ROST (" + (p.chg ? (p.chg > 0 ? "+" : "") + f1(p.chg) : "+0") + ")"}</span></div>
          </div>
        </div>
        {hurt ? <div className="gx-pdm-inj"><span className="pill">{stTxt.toUpperCase()}</span>{back.d ? <span>{"Est. return " + dayLabel(back.d)}</span> : null}</div> : null}
        <div className="gx-pd-hd">'''

OLD_NEWS = '''{news.length ? (
              <div className="gx-pd-pn">
                <div className="gx-pd-h">Latest news<button type="button" className="r text-blue-600" onClick={() => setTab("news")}>All news</button></div>
                <GxPdNews items={news.slice(0, 1)} />
              </div>
            ) : null}
          </>) : null}'''

NEW_LOG = '''{log && log.length ? (
              <div className="gx-pd-pn" data-gx="101log">
                <div className="gx-pd-h">Game log</div>
                <table className="gx-pd-t">
                  <thead><tr><th>Date</th><th>Opp</th><th>FPTS</th>{isG ? <><th>Dec</th><th>SV</th><th>GA</th></> : <><th>TOI</th><th>G</th><th>A</th><th>+/-</th></>}</tr></thead>
                  <tbody>{log.slice(0, 6).map((r) => { const x = r.x, gm = ((((window.GAMES_DATA || {}).games || {})[r.d]) || {})[p.t] || null, o = x.o || (gm ? gm.o : ""), h = x.o ? x.h : gm ? gm.h : null; return (
                    <tr key={r.d}><td>{r.d.slice(5).replace("-", "/")}</td><td>{o ? (h ? "" : "@") + o : ""}</td><td className="b">{f1(r.fp)}</td>
                      {isG ? <><td>{x.dec === "O" ? "OTL" : x.dec || "-"}</td><td>{x.sv || 0}</td><td>{x.ga || 0}</td></> : <><td>{x.toi || "-"}</td><td>{x.g || 0}</td><td>{x.a || 0}</td><td>{gxPdSigned(x.pm)}</td></>}</tr>); })}</tbody>
                </table>
                <button type="button" className="gx-pd-more" onClick={() => setTab("log")}>See full game log</button>
              </div>
            ) : null}
          </>) : null}'''


def change(t):
    t = lit(t, "101: styles", "</style>", NEW_CSS, "change 101 (install.py)")
    t = lit(t, "101: helpers", ROOT, HELPERS + ROOT, "change 101: team colours")
    t = lit(t, "101: phone header", '<div className="gx-pd-hd">', PHONE_HEAD, '<div className="gx-pdm" style=')
    t = lit(t, "101: game log instead of news in Overview", OLD_NEWS, NEW_LOG, 'data-gx="101log"')
    # close with a slide-down instead of vanishing
    t = lit(t, "101: closing state", "  const [img, setImg] = useState(true);\n",
            "  const [img, setImg] = useState(true);\n  const [out101, setOut101] = useState(false);\n  const close101 = () => { if (out101) return; setOut101(true); setTimeout(onClose, 190); };\n",
            "const close101 = () =>")
    t = lit(t, "101: overlay close", '<div className="gx-pd-ov" onClick={onClose}>', '<div className={"gx-pd-ov" + (out101 ? " out" : "")} onClick={close101}>', '(out101 ? " out" : "")')
    t = lit(t, "101: x close", 'onClick={onClose}>{String.fromCharCode(215)}</button>', 'onClick={close101}>{String.fromCharCode(215)}</button>', 'onClick={close101}>{String.fromCharCode(215)}')
    # each tab fades in when you switch to it
    t = lit(t, "101: tab fade", '<div className="gx-pd-bd">', '<div className="gx-pd-bd" key={tab}>', '<div className="gx-pd-bd" key={tab}>')
    # each app page fades in when you switch to it
    t = lit(t, "101: page fade", "        {content}\n", '        <div key={tab + "/" + (sub || "")} className="gx-pg101">{content}</div>\n', 'className="gx-pg101">{content}</div>')
    t = lit(t, "101: no repeated injury note on phone",
            '{hurt && tab === "ov" ? (\n            <div className="gx-pd-pn" style={{ color: "var(--bad)", fontSize: 14 }}>',
            '{hurt && tab === "ov" ? (\n            <div className="gx-pd-pn m-hide" style={{ color: "var(--bad)", fontSize: 14 }}>',
            '<div className="gx-pd-pn m-hide" style={{ color: "var(--bad)"')
    return t


edit(APP, change)
