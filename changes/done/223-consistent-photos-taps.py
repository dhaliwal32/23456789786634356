# changes/223-consistent-photos-taps.py - same photo size in every phone list, bigger tap areas for small buttons and names, big Show more buttons

NEW_CSS = r'''  /* change 223 (install.py): one photo size in every phone list, bigger tap areas */
  @media (max-width: 640px) {
    .gx-face[style*="calc(22px"], .gx-face[style*="calc(24px"], .gx-face[style*="calc(26px"], .gx-face[style*="calc(28px"], .gx-face[style*="calc(30px"], .gx-face[style*="calc(36px"] { width: 34px !important; height: 34px !important; }
    select { min-height: 36px; }
  }
  .gx-arw { width: 36px; height: 36px; }
  .gx-sh108, .gx-sh, .gx-tp187, button[aria-label^="Matchup "], .gx-th113 button { position: relative; }
  .gx-sh108::after, .gx-sh::after { content: ""; position: absolute; left: -2px; right: -2px; top: -12px; bottom: -12px; }
  .gx-tp187::after, .gx-pd-x::after, .gx-th113 button::after { content: ""; position: absolute; inset: -10px; }
  button[aria-label^="Matchup "]::after { content: ""; position: absolute; left: -5px; right: -5px; top: -14px; bottom: -14px; }
  .gx-more223 { display: block; width: 100%; margin-top: 10px; padding: 10px 12px; border: 1px solid var(--line2); border-radius: 10px; font-size: 14px; color: var(--ink); text-align: center; }
</style>'''

M1 = '<button type="button" className="text-sm text-blue-600" style={{ marginTop: 10 }} onClick={() => setLim(lim + 30)}>Show more</button>'
M2 = '<button type="button" className="text-sm text-blue-600" style={{ marginTop: 8 }} onClick={() => setNU(nU + 10)}>Show more</button>'
M3 = '<button type="button" className="text-sm text-blue-600" style={{ marginTop: 8 }} onClick={() => setNL(nL + 20)}>Show more</button>'

def change(t):
    t = lit(t, "223: styles", "</style>", NEW_CSS, "change 223 (install.py)")
    t = lit(t, "223: show more 1", M1, '<button type="button" className="gx-more223" onClick={() => setLim(lim + 30)}>Show more</button>', 'className="gx-more223" onClick={() => setLim(lim + 30)}')
    t = lit(t, "223: show more 2", M2, '<button type="button" className="gx-more223" onClick={() => setNU(nU + 10)}>Show more</button>', 'className="gx-more223" onClick={() => setNU(nU + 10)}')
    t = lit(t, "223: show more 3", M3, '<button type="button" className="gx-more223" onClick={() => setNL(nL + 20)}>Show more</button>', 'className="gx-more223" onClick={() => setNL(nL + 20)}')
    return t

edit(APP, change)
