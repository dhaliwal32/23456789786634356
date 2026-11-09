# changes/239-roster-table-or-team.py - Roster page: choose Table or My team (locker room); the choice is remembered on the device

NEW_CSS = r'''  /* change 239 (install.py): Table / My team choice on Roster */
  .gx-rv239 > .gx-seg103 { margin-bottom: 10px; }
</style>'''

HELPERS = r'''// ---------- change 239: Table or My team on Roster, remembered (install.py) ----------
function GxRosterView239({ P }) {
  const [v, setV] = useState(() => (uiGet().rv239 === "team" ? "team" : "table"));
  const pick = (k) => { setV(k); uiSet("rv239", k); };
  return (
    <div className="gx-rv239" data-gx="239">
      <div className="gx-seg103">{[["table", "Table"], ["team", "My team"]].map(([k, l]) => <button key={k} type="button" className={v === k ? "on" : ""} onClick={() => pick(k)}>{l}</button>)}</div>
      {v === "team" ? <GxMyRoom238 s={P.s} /> : <MyTeam {...P} />}
    </div>
  );
}
'''

def change(t):
    t = lit(t, "239: styles", "</style>", NEW_CSS, "change 239 (install.py)")
    t = lit(t, "239: helpers", ROOT, HELPERS + ROOT, "change 239: Table or My team")
    t = lit(t, "239: switch on Roster",
            '<MyTeam {...P} /><GxMyRoom238 s={s} /></div>',
            '<GxRosterView239 P={P} /></div>',
            '<GxRosterView239 P={P} />')
    return t

edit(APP, change)
