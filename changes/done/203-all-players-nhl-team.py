# changes/203-all-players-nhl-team.py - Players > All players: second dropdown beside the fantasy team one to pick an NHL team

def change(t):
    t = lit(t, "203: state", '  const [own, setOwn] = useState("all");\n',
            '  const [own, setOwn] = useState("all");\n  const [nhl203, setNhl203] = useState("all");\n', 'const [nhl203, setNhl203]')
    t = lit(t, "203: filter", '(pos === "A" || p.p === pos) && rank[p.id] &&',
            '(pos === "A" || p.p === pos) && rank[p.id] && (nhl203 === "all" || p.t === nhl203) &&', '(nhl203 === "all" || p.t === nhl203)')
    t = lit(t, "203: dropdown",
            '        <input className={inp + " flex-1 min-w-[140px]"} placeholder="Search a player" value={q} onChange={(e) => { setQ(e.target.value); setN(50); }} />',
            '        <select className={inp} value={nhl203} onChange={(e) => { setNhl203(e.target.value); setN(50); }} data-gx="203">\n'
            '          <option value="all">All NHL teams</option>\n'
            '          {[...new Set(s.players.map((p) => p.t).filter((x) => x && x !== "FA"))].sort().map((x) => <option key={x} value={x}>{x}</option>)}\n'
            '        </select>\n'
            '        <input className={inp + " flex-1 min-w-[140px]"} placeholder="Search a player" value={q} onChange={(e) => { setQ(e.target.value); setN(50); }} />',
            'data-gx="203"')
    t = lit(t, "203: rank numbers fit on phone", "</style>",
            "  /* change 203 (install.py) */\n  @media (max-width: 640px) { .gx-sc99.gx-rk106 > .gx-rk > :nth-child(1) { font-size: 12px; padding-left: 2px !important; overflow: hidden; white-space: nowrap; } }\n</style>",
            "change 203 (install.py)")
    return t

edit(APP, change)
