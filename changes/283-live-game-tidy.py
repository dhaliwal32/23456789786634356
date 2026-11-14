# changes/283-live-game-tidy.py - live game view tidied: only the rink stays pinned while you scroll (pressure bar and the current play scroll with the page), the rink is not oversized on the laptop, and live and finished games get a Team stats card (shots, faceoffs, hits, blocks, takeaways, giveaways, power play, penalty minutes) with the better side in bold

NEW_CSS = r'''  /* change 283 (install.py) */
  .gx-tk264 .un283 { padding: 0 16px; }
  @media (min-width: 641px) { .gx-tk264 .rw264 { max-width: 560px; margin: 0 auto; } }
  .gx-pv279.gs283 { padding-top: 0; }
</style>'''

PIN_OLD = r'''        </svg>
      </div>
      <div className="pb267" data-gx="267b">'''
PIN_NEW = r'''        </svg>
      </div>
      </div>{/* change 283: only the rink stays pinned */}
      <div className="un283">
      <div className="pb267" data-gx="267b">'''

HELPERS = r'''// ---------- change 283: team stats card for live and finished games (install.py) ----------
const GX_GS283 = [["shotsTotal", "Shots", 1], ["faceoffPercent", "Faceoff %", 1], ["hits", "Hits", 1], ["blockedShots", "Blocked shots", 1], ["takeaways", "Takeaways", 1], ["giveaways", "Giveaways", -1], ["pp", "Power play", 1], ["penaltyMinutes", "Penalty minutes", -1]];
function GxGmStats283({ id, g, live }) {
  const [sm, setSm] = useState(null);
  useEffect(() => {
    let dead = false;
    const load = () => gxSum132(id).then((js) => { if (!dead && js) setSm(js); });
    setSm(null); load();
    const t = live ? setInterval(load, 10000) : null;
    return () => { dead = true; if (t) clearInterval(t); };
  }, [id, live]);
  if (!sm) return null;
  const aw = gxAb131((g.awayTeam || {}).abbrev), hm = gxAb131((g.homeTeam || {}).abbrev);
  const tm = (ab) => ((((sm.boxscore || {}).teams) || []).find((x) => gxAb131(((x || {}).team || {}).abbreviation) === ab) || {}).statistics || [];
  const raw = (ab, nm) => { const x = tm(ab).find((q) => q.name === nm); return x ? x.displayValue : null; };
  const val = (ab, nm) => (nm === "pp" ? (raw(ab, "powerPlayOpportunities") == null ? null : (raw(ab, "powerPlayGoals") || "0") + " for " + raw(ab, "powerPlayOpportunities")) : raw(ab, nm));
  const rows = GX_GS283.map(([k, l, dir]) => { const a = val(aw, k), b = val(hm, k); if (a == null && b == null) return null; const x = parseFloat(a), y = parseFloat(b), tie = isNaN(x) || isNaN(y) || x === y, aw2 = dir > 0 ? x > y : x < y; return { k, l, a, b, wa: !tie && aw2, wb: !tie && !aw2 }; }).filter(Boolean);
  if (!rows.length) return null;
  return (
    <div className="gx-pv279 gs283" data-gx="283">
      <div className="h"><span>TEAM STATS</span><small>{live ? "so far, better side in bold" : "better side in bold"}</small></div>
      <div className="cd">
        <div className="c3 tm"><span><TeamLogo t={aw} size={22} />{aw}</span><span></span><span style={{ justifyContent: "flex-end" }}>{hm}<TeamLogo t={hm} size={22} /></span></div>
        {rows.map((r) => <div key={r.k} className="c3">{r.wa ? <b>{r.a}</b> : <span className={r.wb ? "lo" : ""}>{r.a}</span>}<span>{r.l}</span>{r.wb ? <b>{r.b}</b> : <span className={r.wa ? "lo" : ""}>{r.b}</span>}</div>)}
      </div>
    </div>
  );
}
'''

END_OLD = r''': <div className="em" style={{ padding: 16, color: "var(--mute)" }}>{pre(g) ? "Not started yet." : "No goals yet."}</div>}</>;'''
END_NEW = r''': <div className="em" style={{ padding: 16, color: "var(--mute)" }}>{pre(g) ? "Not started yet." : "No goals yet."}</div>}<GxGmStats283 id={gid} g={g} live={live(g)} /></>;'''


def change(t):
    t = lit(t, "283: styles", "</style>", NEW_CSS, "change 283 (install.py)")
    t = lit(t, "283: pin only the rink", PIN_OLD, PIN_NEW, "change 283: only the rink stays pinned")
    t = lit(t, "283: helpers", ROOT, HELPERS + ROOT, "change 283: team stats card")
    t = lit(t, "283: show the stats", END_OLD, END_NEW, "<GxGmStats283 id={gid}")
    return t

edit(APP, change)
