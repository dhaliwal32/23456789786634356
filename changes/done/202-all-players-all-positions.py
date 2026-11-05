# changes/202-all-players-all-positions.py - Players > All players: new "All" button (first, opens by default) lists forwards, defence and goalies together

def change(t):
    t = lit(t, "202: All opens first", 'const [pos, setPos] = useState("F");',
            'const [pos, setPos] = useState("A"); /* gx202 */', 'useState("A"); /* gx202 */')
    t = lit(t, "202: overall rank",
            '  }, [s.players, K, window.__PMODE]);\n  const qq = nrm(q);',
            '  }, [s.players, K, window.__PMODE]);\n'
            '  const rankA202 = useMemo(() => { const o = {}; s.players.filter((p) => rank[p.id]).map((p) => [p.id, pv(p)]).sort((a, b) => b[1] - a[1]).forEach((x, i) => (o[x[0]] = i + 1)); return o; }, [rank]);\n'
            '  const qq = nrm(q);', 'const rankA202 = useMemo')
    t = lit(t, "202: filter", '.filter((p) => p.p === pos && rank[p.id] &&',
            '.filter((p) => (pos === "A" || p.p === pos) && rank[p.id] &&', '(pos === "A" || p.p === pos)')
    t = lit(t, "202: rank shown", '.map((p) => ({ p, rk: rank[p.id], e: pv(p)',
            '.map((p) => ({ p, rk: pos === "A" ? rankA202[p.id] : rank[p.id], e: pv(p)', 'pos === "A" ? rankA202[p.id]')
    t = lit(t, "202: words", 'const PN78 = { F: "forwards", D: "defencemen", G: "goalies" };',
            'const PN78 = { A: "players", F: "forwards", D: "defencemen", G: "goalies" };', 'A: "players", F: "forwards"')
    t = lit(t, "202: button", '{[["F", "Forwards"], ["D", "Defence"], ["G", "Goalies"]].map(([k, l]) => <button key={k} type="button" className={pos === k ? "on" : ""} onClick={() => { setPos(k); setN(50); }}>',
            '{[["A", "All"], ["F", "Forwards"], ["D", "Defence"], ["G", "Goalies"]].map(([k, l]) => <button key={k} type="button" className={pos === k ? "on" : ""} onClick={() => { setPos(k); setN(50); }}>', '[["A", "All"], ["F", "Forwards"]')
    t = lit(t, "202: goalie stats in All", '<span className="n font-semibold">{f1(e)}</span><GxSC106 p={p} s={s} mode="full" />',
            '<span className="n font-semibold">{f1(e)}</span><GxSC106 p={p} s={s} mode={pos === "A" ? "mx" : "full"} />', 'mode={pos === "A" ? "mx" : "full"}')
    t = lit(t, "202: position in sub line", '{p.t}{sort === "tot" ?',
            '{p.t}{pos === "A" ? " · " + p.p : ""}{sort === "tot" ?', '{pos === "A" ? " · " + p.p : ""}')
    return t

edit(APP, change)
