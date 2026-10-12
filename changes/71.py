# changes/071-remove-next-week.py - removes the "Next week · vs ..." card from Today

OLD_CARD = r'''      <div className="gx-pn"><b></b><b></b><b></b><b></b>
        <div style={{ display: "flex", alignItems: "center", gap: 14 }}>
          <GxRing v={nWin} />
          <div className="min-w-0" style={{ flex: 1 }}>
            <div className="gx-tag">Next week{nOpp ? <span> {"\u00b7"} vs <TL s={s} id={nOpp} /></span> : null}</div>
            <button type="button" className="text-sm text-blue-600" style={{ marginTop: 8 }} onClick={() => window.dispatchEvent(new Event("gx-race-next"))}>See next week's forecast</button>
          </div>
        </div>
      </div>
'''

NEW_CARD = r'''      {/* change 071: next week card removed */}
'''

OLD_CALC = r'''  const nOpp = sN ? oppOf(sN.weeks[sN.wk] || {}, s.me) : null;
  const nWin = useMemo(() => (sN && nOpp ? winChance(sN) : null), [sN, nOpp]);
'''

NEW_CALC = r'''  // change 071: next week win chance no longer needed on Today
'''


def change(t):
    t = lit(t, "071: remove next week card", OLD_CARD, NEW_CARD, "change 071: next week card removed")
    t = lit(t, "071: remove next week win chance", OLD_CALC, NEW_CALC, "change 071: next week win chance")
    for must in ("function Today(", "<GxRace s={s} wk={wk} />", "<GxHome s={s} wk={wk} A={A} B={B} />"):
        if must not in t:
            fail("fantasy-gm.html looks damaged after change 071 (" + must + ").")
    for gone in ("nWin", "nOpp"):
        if gone in t:
            fail("change 071 left " + gone + " behind in fantasy-gm.html.")
    return t


edit(APP, change)
