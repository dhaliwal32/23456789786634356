# changes/186-replay-zoom-dark.py - Phone goal replay gets a zoom button (magnifier) that glides in to the half of the rink where the goal was scored and back out; the Goal Visualizer and video follow the app's dark mode (dark ice, dark card, dark team logos); the video replay gets a border

OLD_K = r'''  const k = big ? 1.6 : 1;'''
NEW_K = r'''  /* change 186: phone zoom to the goal half */
  const [zm186, setZm186] = useState(false);
  const pk186 = ((fr[gi] || [0, []])[1]).find((o) => !o[0]);
  const side186 = pk186 ? (pk186[3] >= 0 ? 1 : -1) : (+x.cx || 0) >= 0 ? 1 : -1;
  const VB186 = [-106.25, -48.75, 212.5, 97.5], VZ186 = side186 > 0 ? [-3, -45.5, 109.25, 91] : [-106.25, -45.5, 109.25, 91];
  const vbNow186 = React.useRef(VB186);
  useEffect(() => {
    const el = svg.current;
    if (!el) return undefined;
    const from = vbNow186.current.slice(), to = zm186 && big ? VZ186 : VB186, t0 = performance.now(), D = 320;
    let raf = 0;
    const step = (now) => {
      const q = Math.min(1, (now - t0) / D), ez = 1 - Math.pow(1 - q, 3);
      const v = from.map((a, i) => a + (to[i] - a) * ez);
      vbNow186.current = v;
      el.setAttribute("viewBox", v.map((n) => n.toFixed(2)).join(" "));
      if (q < 1) raf = requestAnimationFrame(step);
    };
    raf = requestAnimationFrame(step);
    return () => cancelAnimationFrame(raf);
  }, [zm186, big, side186]);
  const k = big ? (zm186 ? 1.1 : 1.6) : 1;'''

OLD_BTN = r'''<button type="button" className="ib" onClick={() => stopAt(tOf(gi))} aria-label="Goal moment" title="Goal moment">{GX_IC184.gol}</button>'''
NEW_BTN = OLD_BTN + r'''
        {big ? <button type="button" className={"ib" + (zm186 ? " on186" : "")} onClick={() => setZm186(!zm186)} aria-label={zm186 ? "Full rink" : "Zoom in"} title={zm186 ? "Full rink" : "Zoom in"} data-gx="186">{zm186 ? GX_IC186.out : GX_IC186.in}</button> : null}'''

HELPERS = r'''// ---------- change 186: zoom icons for the phone goal replay, dark look (install.py) ----------
const gxDk186 = () => { try { return document.documentElement.getAttribute("data-theme") === "dark"; } catch (e) { return false; } };
const gxLogoT186 = (t) => "https://assets.nhle.com/logos/nhl/svg/" + (NHL_LOGO[gxAb131(t)] || gxAb131(t)) + (gxDk186() ? "_dark.svg" : "_light.svg");
const GX_IC186 = {
  in: <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" aria-hidden="true"><circle cx="7" cy="7" r="4.6" /><path d="M10.4 10.4L14 14M5 7h4M7 5v4" /></svg>,
  out: <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" aria-hidden="true"><circle cx="7" cy="7" r="4.6" /><path d="M10.4 10.4L14 14M5 7h4" /></svg>,
};
'''

NEW_CSS = r'''  /* change 186 (install.py) */
  .gx-v184 .ct184 .ib.on186 { background: #8f8f8f; }
  .gx-v184 .vd185 video { border: 1px solid #c9c9c9; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,.18); }
  html[data-theme="dark"] .gx-v184 { background: #141518; color: #ececec; box-shadow: inset 0 0 0 1px #2a2c31; }
  html[data-theme="dark"] .gx-v184 .hd184 b { color: #f2f2f2; }
  html[data-theme="dark"] .gx-v184 .hd184 small, html[data-theme="dark"] .gx-v184 .vd185 small { color: #9a9ca1; }
  html[data-theme="dark"] .gx-v184 .ct184 .ib, html[data-theme="dark"] .gx-v184 .ct184 .oi184 { background: #2c2e33; color: #e6e6e6; }
  html[data-theme="dark"] .gx-v184 .ct184 .ib:hover { background: #3a3c42; }
  html[data-theme="dark"] .gx-v184 .ct184 .ib.on186 { background: #55585f; }
  html[data-theme="dark"] .gx-v184 .cd184 { background: #1c1d21; }
  html[data-theme="dark"] .gx-v184 .nm184 .tx { color: #f2f2f2; }
  html[data-theme="dark"] .gx-v184 .nm184 .tx small, html[data-theme="dark"] .gx-v184 .tl184 small { color: #9a9ca1; }
  html[data-theme="dark"] .gx-v184 .as184 span { color: #c9cacd; }
  html[data-theme="dark"] .gx-v184 .tl184 > div { background: #26282d; }
  html[data-theme="dark"] .gx-v184 .tl184 b { color: #f2f2f2; }
  html[data-theme="dark"] .gx-v184 .ol184 { background: #1c1d21; border-top-color: #2a2c31; }
  html[data-theme="dark"] .gx-v184 .ol184 .ol { color: #e6e6e6; }
  html[data-theme="dark"] .gx-v184 .ol184 .ol .hd, html[data-theme="dark"] .gx-v184 .ol184 .ol .pl .tg { color: #9a9ca1; }
  html[data-theme="dark"] .gx-v184 .sg185 { background: #2c2e33; }
  html[data-theme="dark"] .gx-v184 .sg185 button { color: #a0a2a7; }
  html[data-theme="dark"] .gx-v184 .sg185 button.on { background: #45474d; color: #ffffff; box-shadow: none; }
  html[data-theme="dark"] .gx-v184 .vd185 video { border-color: #3a3c42; box-shadow: 0 2px 14px rgba(0,0,0,.5); }
</style>'''

DARK = [
    ("186: dark ice texture 1", 'function gxIce184() {', 'function gxIce184(dk) {\n  const K186 = dk ? "d" : "l"; window.__GXICE186 = window.__GXICE186 || {}; /* change 186: dark ice */\n  if (window.__GXICE186[K186] != null) return window.__GXICE186[K186];', 'change 186: dark ice'),
    ("186: dark ice texture 2", '  if (GX_ICE184 !== null) return GX_ICE184;\n', '', None),
    ("186: dark ice texture 3", 'x.fillStyle = "#fbfbfb"; x.fillRect(0, 0, 1000, 425);', 'x.fillStyle = dk ? "#1b1d21" : "#fbfbfb"; x.fillRect(0, 0, 1000, 425);', 'x.fillStyle = dk ? "#1b1d21"'),
    ("186: dark ice texture 4", 'x.strokeStyle = "rgba(120,130,140," +', 'x.strokeStyle = (dk ? "rgba(210,220,230," : "rgba(120,130,140,") +', 'dk ? "rgba(210,220,230,"'),
    ("186: dark ice texture 5", '    GX_ICE184 = c.toDataURL("image/jpeg", 0.8);\n  } catch (e) { GX_ICE184 = ""; }\n  return GX_ICE184;', '    window.__GXICE186[K186] = c.toDataURL("image/jpeg", 0.8);\n  } catch (e) { window.__GXICE186[K186] = ""; }\n  return window.__GXICE186[K186];', 'catch (e) { window.__GXICE186[K186] = ""; }'),
    ("186: dark rink colours", 'const red = GX_RED184, blue = GX_BLUE184, cp = "gxb184" + id, ice = gxIce184(), out = [];', 'const dk = gxDk186(), red = dk ? "#e05a5a" : GX_RED184, blue = dk ? "#5b8ff0" : GX_BLUE184, cp = "gxb184" + id + (dk ? "d" : ""), ice = gxIce184(dk), out = []; /* change 186: dark rink */', 'change 186: dark rink'),
    ("186: dark ice", 'width="200" height="85" rx="28" ry="28" fill="#fbfbfb" />);', 'width="200" height="85" rx="28" ry="28" fill={dk ? "#1b1d21" : "#fbfbfb"} />);', 'fill={dk ? "#1b1d21" : "#fbfbfb"}'),
    ("186: dark nets", 'fill="#ffffff" stroke={red} strokeWidth="0.35" />);', 'fill={dk ? "#2a2c31" : "#ffffff"} stroke={red} strokeWidth="0.35" />);', 'fill={dk ? "#2a2c31" : "#ffffff"} stroke={red}'),
    ("186: dark centre line gaps", 'width="0.4" height="1.5" fill="#ffffff" />);', 'width="0.4" height="1.5" fill={dk ? "#1b1d21" : "#ffffff"} />);', 'height="1.5" fill={dk ?'),
    ("186: dark end code L", 'fill="#121212">{L}</text>', 'fill={dk ? "#e8e8e8" : "#121212"}>{L}</text>', '"#121212"}>{L}'),
    ("186: dark end code R", 'fill="#121212">{R}</text>', 'fill={dk ? "#e8e8e8" : "#121212"}>{R}</text>', '"#121212"}>{R}'),
    ("186: dark boards", 'stroke="#c5c5c7" strokeWidth="0.3" />);', 'stroke={dk ? "#4a4c52" : "#c5c5c7"} strokeWidth="0.3" />);', 'stroke={dk ? "#4a4c52"'),
    ("186: dark centre logo", '<image key="lg" href={gxLogo184(H)}', '<image key="lg" href={gxLogoT186(H)}', 'href={gxLogoT186(H)}'),
    ("186: light puck on dark ice", '<circle r={1 * k} fill="#121212" stroke="#121212" strokeWidth="0.25" />', '<circle r={1 * k} fill={gxDk186() ? "#f2f2f2" : "#121212"} stroke={gxDk186() ? "#f2f2f2" : "#121212"} strokeWidth="0.25" />', 'fill={gxDk186() ? "#f2f2f2"'),
    ("186: dark card logo", '<img src={gxLogo184(tm)} alt={gxAb131(tm)} loading="lazy" />', '<img src={gxLogoT186(tm)} alt={gxAb131(tm)} loading="lazy" />', 'src={gxLogoT186(tm)}'),
    ("186: still rink puck path", '<line x1={px} y1={py} x2={nx} y2="0" stroke="#121212" strokeWidth="0.35" strokeDasharray="1.2 1" />', '<line x1={px} y1={py} x2={nx} y2="0" stroke={gxDk186() ? "#e8e8e8" : "#121212"} strokeWidth="0.35" strokeDasharray="1.2 1" />', 'stroke={gxDk186() ? "#e8e8e8"'),
    ("186: still rink puck", '<circle cx={nx} cy="0" r="1" fill="#121212" />', '<circle cx={nx} cy="0" r="1" fill={gxDk186() ? "#e8e8e8" : "#121212"} />', 'r="1" fill={gxDk186()'),
]


def change(t):
    t = lit(t, "186: styles", "</style>", NEW_CSS, "change 186 (install.py)")
    t = lit(t, "186: icons", ROOT, HELPERS + ROOT, "change 186: zoom icons")
    t = lit(t, "186: zoom state and glide", OLD_K, NEW_K, "change 186: phone zoom to the goal half")
    t = lit(t, "186: zoom button", OLD_BTN, NEW_BTN, 'data-gx="186"')
    for lab, old, new, done in DARK:
        if done is None:
            if old in t:
                t = lit(t, lab, old, new)
            else:
                print("(install) " + lab + ": already done")
        else:
            t = lit(t, lab, old, new, done)
    return t


edit(APP, change)
