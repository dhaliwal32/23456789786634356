# changes/116-trade-grid-chart-lines.py - Trades: team pictures 5 on top and 4 below, both rows centred; Matchup: "Original projection" text removed from the day box; home week chart: original projection is a clear dotted line, real points a bold solid line, with a small key; team pictures: the sync now saves a copy of every team picture into team-logos/ so ESPN can't block them, and the app uses that copy first

NEW_CSS = r'''  /* change 116 (install.py) */
  .gx-tw113.gx-tg114 { display: flex; flex-wrap: wrap; justify-content: center; gap: 10px; max-width: 380px; margin: 0 auto; }
  .gx-tw113.gx-tg114 button { width: calc((100% - 40px) / 5); display: flex; justify-content: center; }
  .gx-tn114 { text-align: center; }
  .gx-key116 { display: flex; flex-wrap: wrap; gap: 4px 14px; font-size: 11px; color: var(--mute); margin-top: 6px; }
  .gx-key116 span { display: inline-flex; align-items: center; gap: 5px; }
  .gx-key116 svg { flex: none; }
</style>'''

KEY = r'''      <div className="gx-key116" data-gx="116k">
        <span><svg width="22" height="6"><line x1="2" x2="20" y1="3" y2="3" style={{ stroke: "var(--ink)", strokeWidth: 2.6, strokeLinecap: "round" }} /></svg>Actual</span>
        <span><svg width="22" height="6"><line x1="2" x2="20" y1="3" y2="3" style={{ stroke: "var(--ink)", strokeWidth: 2.2, strokeDasharray: "0.1 4.5", strokeLinecap: "round" }} /></svg>Original projection</span>
        <span><svg width="22" height="6"><line x1="2" x2="20" y1="3" y2="3" style={{ stroke: "var(--ink)", strokeWidth: 2, strokeDasharray: "5 4" }} /></svg>Projected</span>
      </div>
'''


SYNC_ADD = r"""
# change 116: keep a copy of each team picture here, so the app can always show it
try:
    import hashlib
    _ld = os.path.join(HERE, "team-logos")
    os.makedirs(_ld, exist_ok=True)
    _ext = {"image/png": "png", "image/jpeg": "jpg", "image/jpg": "jpg", "image/gif": "gif", "image/webp": "webp", "image/svg+xml": "svg"}
    for _t in teams:
        _u = _t.get("logo") or ""
        if not _u.startswith("http"):
            continue
        _h = hashlib.md5(_u.encode()).hexdigest()[:8]
        _have = [f for f in os.listdir(_ld) if f.startswith(str(_t["id"]) + "-" + _h + ".")]
        if not _have:
            try:
                _r = session.get(_u, timeout=20, headers={"Referer": "https://fantasy.espn.com/", "Accept": "image/avif,image/webp,image/png,image/svg+xml,image/*,*/*;q=0.8"})
                _ct = (_r.headers.get("Content-Type") or "").split(";")[0].strip().lower()
                _x = _ext.get(_ct) or ("svg" if _u.lower().endswith(".svg") else "png" if _ct.startswith("image/") else "")
                if _r.ok and _x and len(_r.content) > 50:
                    for f in os.listdir(_ld):
                        if f.startswith(str(_t["id"]) + "-"):
                            os.remove(os.path.join(_ld, f))
                    _f = str(_t["id"]) + "-" + _h + "." + _x
                    with open(os.path.join(_ld, _f), "wb") as fh:
                        fh.write(_r.content)
                    _have = [_f]
                else:
                    print("team picture not saved for", _t.get("name"), _r.status_code, _ct)
            except Exception as _e:
                print("team picture not saved for", _t.get("name"), _e)
        if _have:
            _t["pic"] = "team-logos/" + _have[0]
except Exception as _e:
    print("team pictures skipped:", _e)
"""


def change_sync(t):
    anchor = '"logo": str(t.get("logo") or "")} for t in lg.get("teams", [])]  # change 114: team pictures\n'
    return lit(t, "116: sync saves team picture copies", anchor, anchor + SYNC_ADD, "change 116: keep a copy of each team picture")


def change(t):
    t = lit(t, "116: styles", "</style>", NEW_CSS, "change 116 (install.py)")
    # matchup: no "Original projection" line in the day box
    i = t.find('        {state !== "projected" && x.proj != null && y.proj != null ? <div className="text-xs text-slate-500"')
    if i >= 0:
        j = t.find("\n", i) + 1
        if 'data-gx="094"' not in t[i:j]:
            fail("116: original projection line looks different")
        t = t[:i] + t[j:]
        print("(install) 116: matchup original projection text removed: updated")
    # home week chart: clearer original projection (dotted) and actual (solid) lines
    t = lit(t, "116: original projection them",
            '{done >= 2 ? <polyline points={P(EB, 0, done - 1)} style={ln("var(--mute)", "2 4", 1, 0.6)} /> : null}',
            '{done >= 2 ? <polyline points={P(EB, 0, done - 1)} style={ln("var(--mute)", "0.1 4.5", 2.2, 0.85)} /> : null}',
            'ln("var(--mute)", "0.1 4.5", 2.2, 0.85)')
    t = lit(t, "116: original projection you",
            '{done >= 2 ? <polyline points={P(EA, 0, done - 1)} style={ln("var(--accent)", "2 4", 1, 0.45)} /> : null}',
            '{done >= 2 ? <polyline points={P(EA, 0, done - 1)} style={ln("var(--accent)", "0.1 4.5", 2.2, 0.8)} /> : null}',
            'ln("var(--accent)", "0.1 4.5", 2.2, 0.8)')
    t = lit(t, "116: actual them",
            '{done >= 2 ? <polyline points={P(CB, 0, done - 1)} style={ln("var(--mute)")} /> : null}',
            '{done >= 2 ? <polyline points={P(CB, 0, done - 1)} style={ln("var(--mute)", null, 2.6)} /> : null}',
            'P(CB, 0, done - 1)} style={ln("var(--mute)", null, 2.6)}')
    t = lit(t, "116: actual you",
            '{done >= 2 ? <polyline points={P(CA, 0, done - 1)} style={ln("var(--accent)")} /> : null}',
            '{done >= 2 ? <polyline points={P(CA, 0, done - 1)} style={ln("var(--accent)", null, 2.6)} /> : null}',
            'P(CA, 0, done - 1)} style={ln("var(--accent)", null, 2.6)}')
    # small key under the chart
    t = lit(t, "116: chart key", '      <div className="gx-rf" style={{ display: "none" }}>{facts}</div>\n',
            KEY + '      <div className="gx-rf" style={{ display: "none" }}>{facts}</div>\n', 'data-gx="116k"')
    # team pictures: use the saved copy first, then ESPN's link, then the letter
    t = lit(t, "116: team picture copy first",
            '  const [bad, setBad] = useState(false);\n  const z = size || 24, nm = String(T.name || "?");',
            '  const [bad, setBad] = useState(0);\n  const z = size || 24, nm = String(T.name || "?"), srcs = [T.pic, T.logo].filter(Boolean);',
            "srcs = [T.pic, T.logo].filter(Boolean)")
    t = lit(t, "116: team picture fallbacks",
            '  if (T.logo && !bad) return <img className="gx-fp114" src={T.logo} alt="" loading="lazy" style={st} onError={() => setBad(true)} />;',
            '  if (bad < srcs.length) return <img key={bad} className="gx-fp114" src={srcs[bad]} alt="" loading="lazy" style={st} onError={() => setBad(bad + 1)} />;',
            "src={srcs[bad]}")
    return t


edit("espn_sync.py", change_sync)
edit(APP, change)
