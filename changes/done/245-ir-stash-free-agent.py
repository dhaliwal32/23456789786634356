# changes/245-ir-stash-free-agent.py - Back from IR card: when nobody on your team can go to IR, suggest good injured free agents to pick up (for the player you drop) and put in the IR spot your returning player leaves

NEW_CSS = r'''  /* change 245 (install.py): stash an injured free agent */
  .gx-ir244 .op .r .fr245 { text-align: right; font-size: 12px; line-height: 1.25; }
  .gx-ir244 .op .r .fr245 small { display: block; font-size: 10.5px; color: var(--mute); }
  .gx-ir244 .op .nt245 { font-size: 12px; color: var(--mute); margin: 2px 0 4px; }
</style>'''

def change(t):
    t = lit(t, "245: styles", "</style>", NEW_CSS, "change 245 (install.py)")
    t = lit(t, "245: injured free agents",
            "        if (!dead) setCalc({ base, irOpts, drops });",
            '''        /* change 245: good injured free agents who could take the IR spot */
        const stash = irOpts.length ? [] : s.players.filter((q) => q.ft === "fa" && ["OUT", "INJURY_RESERVE"].includes(String(q.status || "").toUpperCase()))
          .sort((a, b) => gxPgAvg(b, s.blend) - gxPgAvg(a, s.blend)).slice(0, 4);
        if (!dead) setCalc({ base, irOpts, drops, stash });''',
            "change 245: good injured free agents")
    t = lit(t, "245: show them",
            '''                  {calc.drops.map((o, i) => row(o, o.q.t + " \\u00b7 " + o.q.p, !calc.irOpts.length && i === 0))}\n''',
            '''                  {calc.drops.map((o, i) => row(o, o.q.t + " \\u00b7 " + o.q.p, !calc.irOpts.length && i === 0))}
                  {calc.stash && calc.stash.length && calc.drops.length ? <>{/* change 245 */}
                    <div className="gt">Then stash an injured free agent in IR</div>
                    <div className="nt245">{"Drop " + calc.drops[0].q.n + ", pick up one of these and put him in the IR spot " + p.n.split(" ").slice(-1)[0] + " leaves. He doesn't play now, but you keep him for when he's back."}</div>
                    {calc.stash.map((q, i) => (
                      <div key={q.id} className={"r" + (i === 0 ? " best" : "")}>
                        <GxFace p={q} size={26} />
                        <button type="button" className="nn text-left" onClick={() => openP(q)}><b>{q.n}</b><small>{q.t + " \\u00b7 " + q.p + " \\u00b7 " + (String(q.status || "").toUpperCase() === "OUT" ? "out" : "IR") + (q.back && q.back >= today ? " \\u00b7 back " + dayLabel(q.back) : "")}</small></button>
                        <span className="n">{f1(gxPgAvg(q, s.blend))}<small>pts/g</small></span>
                        <span className="fr245">Add<small>to IR</small></span>
                      </div>
                    ))}
                  </> : null}
''',
            "{/* change 245 */}")
    return t

edit(APP, change)
