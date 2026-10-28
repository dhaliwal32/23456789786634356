# changes/114-team-pictures-matchup-totals.py - ESPN team pictures on Matchup and Trades (sync now saves each fantasy team's logo); Matchup: day and week totals moved to the bottom (projected or final), arrows to the next matchup on phones too; Trades: every team shown at once as a picture, no sideways scrolling

NEW_CSS = r'''  /* change 114 (install.py) */
  .gx-fp114 { display: inline-block; flex: none; object-fit: cover; vertical-align: middle; }
  .gx-fp114.l { display: inline-flex; align-items: center; justify-content: center; background: var(--card3, var(--line)); color: var(--ink); font-weight: 700; }
  .gx-nm114 { display: flex; align-items: center; gap: 6px; min-width: 0; }
  .gx-nm114.r { justify-content: flex-end; }
  .gx-nm114 a, .gx-nm114 > span:not(.gx-fp114) { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; min-width: 0; }
  .gx-ms .gx-fp114 { vertical-align: -4px; margin: 0 5px; }
  .gx-tt114 { font-weight: 700; border-top: 2px solid var(--line2) !important; }
  .gx-tt114 > div:first-child { font-weight: 500; color: var(--mute); font-size: 12px; }
  .gx-wt114 { display: flex; justify-content: space-between; margin-top: 12px; font-variant-numeric: tabular-nums; }
  .gx-wt114 > div { display: flex; flex-direction: column; }
  .gx-wt114 > div.r { align-items: flex-end; }
  .gx-wt114 small { font-size: 12px; color: var(--mute); }
  .gx-wt114 b { font-size: 22px; font-weight: 700; color: var(--ink); line-height: 1.2; }
  .gx-tg114 { display: grid; grid-template-columns: repeat(auto-fill, minmax(56px, 1fr)); gap: 10px; overflow: visible; max-width: 720px; padding: 2px; }
  .gx-tg114 button { padding: 4px; border: 0; border-radius: 14px; justify-content: center; background: transparent; transition: opacity .15s; }
  .gx-tg114 button.on { background: transparent; box-shadow: 0 0 0 2px var(--ink); }
  .gx-tg114 button:not(.on) { opacity: .5; }
  .gx-tn114 { font-size: 13px; color: var(--mute); margin-top: 2px; }
  .gx-tn114 b { color: var(--ink); font-weight: 600; }
</style>'''

HELPERS = r'''// ---------- change 114: fantasy team pictures from ESPN (install.py) ----------
function GxFtPic114({ id, size }) {
  const T = ((window.ESPN_DATA || {}).teams || []).find((t) => String(t.id) === String(id).replace(/^t/, "")) || {};
  const [bad, setBad] = useState(false);
  const z = size || 24, nm = String(T.name || "?");
  const st = { width: z, height: z, borderRadius: Math.round(z * 0.28) };
  if (T.logo && !bad) return <img className="gx-fp114" src={T.logo} alt="" loading="lazy" style={st} onError={() => setBad(true)} />;
  return <span className="gx-fp114 l" style={{ ...st, fontSize: Math.round(z * 0.45) }}>{(nm.replace(/[^A-Za-z0-9 ]/g, "").trim()[0] || "?").toUpperCase()}</span>;
}
'''


def sub_in(t, start, name, old, new, done):
    if done in t:
        print("(install) " + name + ": already done")
        return t
    i = t.find(start)
    if i < 0:
        fail(name + ": start not found")
    j = t.find(old, i)
    if j < 0:
        fail(name + ": not found")
    print("(install) " + name + ": updated")
    return t[:j] + new + t[j + len(old):]


def change_sync(t):
    return lit(t, "114: sync saves team logos",
               '''teams = [{"id": t["id"], "name": (t.get("name") or f"{t.get('location', '')} {t.get('nickname', '')}".strip()
                                  or f"Team {t['id']}")} for t in lg.get("teams", [])]''',
               '''teams = [{"id": t["id"], "name": (t.get("name") or f"{t.get('location', '')} {t.get('nickname', '')}".strip()
                                  or f"Team {t['id']}"), "logo": str(t.get("logo") or "")} for t in lg.get("teams", [])]  # change 114: team pictures''',
               "change 114: team pictures")


def change(t):
    t = lit(t, "114: styles", "</style>", NEW_CSS, "change 114 (install.py)")
    t = lit(t, "114: helpers", ROOT, HELPERS + ROOT, "change 114: fantasy team pictures")
    M = "// matchup v35:"
    # matchup: team pictures by the names
    t = lit(t, "114: matchup left name",
            '<div className="text-sm font-semibold truncate" style={mine ? { color: "var(--accent)" } : null}><TL s={s} id={a} /></div>',
            '<div className="text-sm font-semibold gx-nm114" style={mine ? { color: "var(--accent)" } : null}><GxFtPic114 id={a} size={22} /><TL s={s} id={a} /></div>',
            "<GxFtPic114 id={a} size={22} />")
    t = lit(t, "114: matchup right name",
            '<div className="text-sm text-slate-500 truncate"><TL s={s} id={b} /></div>',
            '<div className="text-sm text-slate-500 gx-nm114 r"><TL s={s} id={b} /><GxFtPic114 id={b} size={22} /></div>',
            "<GxFtPic114 id={b} size={22} />")
    # matchup: arrows to the next matchup on phones too
    t = lit(t, "114: previous matchup arrow", 'className="m-hide gx-arw" aria-label="Previous matchup"', 'className="gx-arw" aria-label="Previous matchup"', 'className="gx-arw" aria-label="Previous matchup"')
    t = lit(t, "114: next matchup arrow", 'className="m-hide gx-arw" aria-label="Next matchup"', 'className="gx-arw" aria-label="Next matchup"', 'className="gx-arw" aria-label="Next matchup"')
    # matchup: week totals off the top (only who is ahead stays)
    t = sub_in(t, M, "114: week totals off the top",
               """          <span>{(over ? "Final " : "Projected ") + Math.round(fa)}</span>
          <span style={{ margin: "0 auto", color: margin >= 0 ? "var(--good)" : "var(--bad)" }}>{mine ? (margin >= 0 ? "Ahead by " : "Behind by ") + f1(Math.abs(margin)) : teamName(s, margin >= 0 ? a : b) + " ahead by " + f1(Math.abs(margin))}</span>
          <span>{Math.round(fb)}</span>""",
               """          <span data-gx="114w" style={{ margin: "0 auto", color: margin >= 0 ? "var(--good)" : "var(--bad)" }}>{mine ? (margin >= 0 ? "Ahead by " : "Behind by ") + f1(Math.abs(margin)) : teamName(s, margin >= 0 ? a : b) + " ahead by " + f1(Math.abs(margin))}</span>""",
               'data-gx="114w"')
    # matchup: day totals off the top of the day box
    t = sub_in(t, M, "114: day totals off the top",
               '''          <span style={{ marginLeft: "auto", fontVariantNumeric: "tabular-nums" }}>
            <span className="font-semibold">{f1(x.act + x.total)}</span> <span className="text-slate-500">to {f1(y.act + y.total)}</span>
            <span style={{ marginLeft: 8, color: dayTot >= 0 ? "var(--good)" : "var(--bad)" }}>{(dayTot >= 0 ? "+" : "") + f1(dayTot)}</span>
          </span>
''', "", 'className="gx-h2h gx-tt114"')
    # matchup: day totals at the bottom of the day box
    t = sub_in(t, M, "114: day totals at the bottom",
               ''')) : <div className="text-sm text-slate-500">No games for either team on this day.</div>}''',
               ''')) : <div className="text-sm text-slate-500">No games for either team on this day.</div>}
        {rows.length ? <div className="gx-h2h gx-tt114"><div>{state === "final" ? "Final" : state === "live" ? "Live" : "Projected"}</div><div className="text-right">{f1(x.act + x.total)}</div><div></div><div>{f1(y.act + y.total)}</div><div className="text-right" style={{ color: Math.abs(dayTot) < 0.05 ? "var(--mute)" : dayTot > 0 ? "var(--good)" : "var(--bad)" }}>{(dayTot > 0 ? "+" : "") + f1(dayTot)}</div></div> : null}''',
               'className="gx-h2h gx-tt114"')
    # matchup: week totals at the bottom of the page
    t = sub_in(t, M, "114: week totals at the bottom",
               '''      <div className="text-xs text-slate-500" style={{ display: "flex", marginTop: 10 }}>
        <span>{gamesMoves(s, a, wk, A)}</span>''',
               '''      <div className="gx-wt114"><div><small>{over ? "Week final" : "Week projected"}</small><b>{Math.round(fa)}</b></div><div className="r"><small>{over ? "Week final" : "Week projected"}</small><b>{Math.round(fb)}</b></div></div>
      <div className="text-xs text-slate-500" style={{ display: "flex", marginTop: 6 }}>
        <span>{gamesMoves(s, a, wk, A)}</span>''',
               "gx-wt114\"><div><small>")
    # matchup chips at the top: small team pictures
    t = lit(t, "114: matchup chips pictures",
            '{nm(a)} {x >= y ? <b>{f1(x)}</b> : f1(x)} <span style={{ opacity: 0.6 }}>vs</span> {y > x ? <b>{f1(y)}</b> : f1(y)} {nm(b)}',
            '<GxFtPic114 id={a} size={18} />{nm(a)} {x >= y ? <b>{f1(x)}</b> : f1(x)} <span style={{ opacity: 0.6 }}>vs</span> {y > x ? <b>{f1(y)}</b> : f1(y)} {nm(b)}<GxFtPic114 id={b} size={18} />',
            "<GxFtPic114 id={a} size={18} />")
    # trades: every team at once, pictures only
    t = lit(t, "114: trades team pictures",
            '''      <div className="gx-tw113">
        {others.map((t) => <button key={t.id} type="button" className={partner === t.id ? "on" : ""} onClick={() => { setPartner(t.id); setGet([]); setPick({}); setEdit(-1); }}><span className="b">{(String(t.name || "?").replace(/[^A-Za-z0-9 ]/g, "").trim()[0] || "?").toUpperCase()}</span>{t.name}</button>)}
      </div>''',
            '''      <div className="gx-tw113 gx-tg114">
        {others.map((t) => <button key={t.id} type="button" title={t.name} aria-label={t.name} className={partner === t.id ? "on" : ""} onClick={() => { setPartner(t.id); setGet([]); setPick({}); setEdit(-1); }}><GxFtPic114 id={t.id} size={44} /></button>)}
      </div>
      {partner ? <div className="gx-tn114">Trading with <b>{teamName(s, partner)}</b></div> : null}''',
            "gx-tw113 gx-tg114")
    return t


edit("espn_sync.py", change_sync)
edit(APP, change)
