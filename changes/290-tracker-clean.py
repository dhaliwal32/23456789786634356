# changes/290-tracker-clean.py - live tracker: a blocked shot now belongs to the team that shot it (ESPN files it under the blocker, which also made the tracker guess the ends backwards early in a game); the label is off the rink and sits in one clean line under it; plays use a small team dot and plain text instead of heavy colour blocks; plain names (Shot on goal, Blocked shot, Faceoff)

NEW_CSS = r'''  /* change 290 (install.py) */
  .gx-tk264 .st290 { display: flex; align-items: center; justify-content: center; gap: 7px; height: 30px; font-size: 13.5px; font-weight: 600; color: var(--ink); white-space: nowrap; }
  .gx-tk264 .st290 i, .gx-tk264 .tg264 i, .gx-tk264 .ls266 .r266 .tg266 i { width: 8px; height: 8px; border-radius: 99px; flex: none; display: inline-block; background: var(--line2); }
  .gx-tk264 .tg264, .gx-tk264 .ls266 .r266 .tg266 { display: inline-flex; align-items: center; gap: 6px; min-width: 0; padding: 0; border-radius: 0; background: none; color: var(--ink2); font-size: 12.5px; font-weight: 600; text-align: left; }
  .gx-tk264 .ev264 { margin-top: 10px; min-height: 58px; padding: 10px 12px; border-radius: 12px; background: var(--card); gap: 12px; }
  .gx-tk264 .tg264 { min-width: 48px; }
  .gx-tk264 .tx264 b { font-size: 14.5px; font-weight: 600; }
  .gx-tk264 .tx264 span { font-size: 12.5px; height: 18px; }
  .gx-tk264 .ls266 { border-top: 0; }
  .gx-tk264 .ls266 .r266 { grid-template-columns: 44px 50px minmax(0, 1fr); height: 38px; font-size: 13px; }
  .gx-tk264 .ls266 .r266 .tx266 b { font-weight: 600; margin-right: 8px; }
  .gx-tk264 .pb267 { font-weight: 600; }
  .gx-tk264 .hd264 { letter-spacing: 0; font-weight: 600; font-size: 14px; }
  .gx-tk264 .ck264 { font-weight: 600; }
</style>'''

HELPERS = r'''// ---------- change 290: clean live tracker text (install.py) ----------
const GX_TY290 = { "face off": "Faceoff", "blocked": "Blocked shot", "missed": "Missed shot", "shot": "Shot on goal", "failed shot attempt": "Shootout miss", "period start": "Period starts", "period end": "Period ends" };
const gxTy290 = (q) => (!q ? "" : q.goal ? "Goal" : GX_TY290[String(q.ty || "").toLowerCase()] || q.ty || "Play");
// one plain line for what is happening: "CAR shot blocked", "SEA attacking", "Faceoff"
function gxSay290(e, S, A, H) {
  if (!e || e.goal) return { t: "", tx: "" };
  const who = (t) => (t === "h" ? H : t === "a" ? A : ""), ty = String(e.ty || "");
  if (/^blocked/i.test(ty)) return { t: e.t, tx: who(e.t) + " shot blocked" };
  if (/^missed/i.test(ty)) return { t: e.t, tx: who(e.t) + " shot missed" };
  if (/^shot/i.test(ty)) return { t: e.t, tx: who(e.t) + " shot on goal" };
  if (/^(face ?off|stoppage|period|end of|shootout)/i.test(ty)) return { t: "", tx: gxTy290(e) };
  const lab = String((S && S.lab) || ""), t = (S && S.lt) || "";
  if (!lab) return { t: "", tx: "" };
  if (/^attack$/i.test(lab)) return { t, tx: who(t) + " attacking" };
  if (/dangerous/i.test(lab)) return { t, tx: who(t) + " dangerous attack" };
  if (/possession/i.test(lab)) return { t, tx: who(t) + " in possession" };
  return { t: "", tx: gxTy290({ ty: lab }) };
}
'''

TEAM_OLD = r'''t: tid && tid === H.id ? "h" : tid && tid === A.id ? "a" : "",'''
TEAM_NEW = r'''t: ((t0) => (/^blocked/i.test(String((e.type || {}).text || "")) ? (t0 === "h" ? "a" : t0 === "a" ? "h" : "") : t0))(tid && tid === H.id ? "h" : tid && tid === A.id ? "a" : ""), /* change 290: a blocked shot belongs to the shooter's team */'''

LAB_START = r'''          {S267.lab && !(e && e.goal) ? <g className="lb267" data-gx="267l" pointerEvents="none">'''
LAB_END = r'''</text></g> : null}
'''
LAB_NEW = r'''          {/* change 290: the label moved off the rink */}
'''

PB_OLD = r'''      <div className="pb267" data-gx="267b">'''
PB_NEW = r'''      {(() => { const y = gxSay290(e, S267, A, H), c = col(y.t); return <div className="st290" data-gx="290">{y.tx ? <><i style={c ? { background: c.f } : null}></i>{y.tx}</> : null}</div>; })()}
      <div className="pb267" data-gx="267b">'''

T1_OLD = r'''{e ? <span className="tg264" style={{ background: ec ? ec.f : "var(--line)", color: ec ? ec.t : "var(--ink)" }}>{e.t === "h" ? H : e.t === "a" ? A : "NHL"}</span> : null}'''
T1_NEW = r'''{e ? <span className="tg264"><i style={ec ? { background: ec.f } : null}></i>{e.t === "h" ? H : e.t === "a" ? A : "NHL"}</span> : null}'''
B1_OLD = r'''<b>{e ? (e.goal ? "GOAL" : e.ty || "Play") : "Waiting for the first play"}</b>'''
B1_NEW = r'''<b>{e ? gxTy290(e) : "Waiting for the first play"}</b>'''

T2_OLD = r'''<span className="tg266" style={{ background: c ? c.f : "var(--line)", color: c ? c.t : "var(--ink)" }}>{q.t === "h" ? H : q.t === "a" ? A : "NHL"}</span>'''
T2_NEW = r'''<span className="tg266"><i style={c ? { background: c.f } : null}></i>{q.t === "h" ? H : q.t === "a" ? A : "NHL"}</span>'''
B2_OLD = r'''<span className="tx266"><b>{q.goal ? "GOAL" : q.ty || "Play"}</b>{q.tx}</span>'''
B2_NEW = r'''<span className="tx266"><b>{gxTy290(q)}</b>{q.tx}</span>'''


def cut(t, name, start, end, new, done):
    if done in t:
        print(f"(install) {name}: already done")
        return t
    if t.count(start) != 1:
        fail(f"'{name}' start matched {t.count(start)} times")
    a = t.find(start)
    b = t.find(end, a)
    if b < 0:
        fail(f"'{name}' end not found")
    print(f"(install) {name}: updated")
    return t[:a] + new + t[b + len(end):]


def change(t):
    t = lit(t, "290: styles", "</style>", NEW_CSS, "change 290 (install.py)")
    t = lit(t, "290: helpers", ROOT, HELPERS + ROOT, "change 290: clean live tracker text")
    t = lit(t, "290: blocked shot team", TEAM_OLD, TEAM_NEW, "change 290: a blocked shot belongs", 2)
    t = cut(t, "290: label off the rink", LAB_START, LAB_END, LAB_NEW, "change 290: the label moved off the rink")
    t = lit(t, "290: status line", PB_OLD, PB_NEW, 'className="st290"')
    t = lit(t, "290: play tag", T1_OLD, T1_NEW, '<span className="tg264"><i')
    t = lit(t, "290: play name", B1_OLD, B1_NEW, "gxTy290(e) :")
    t = lit(t, "290: list tag", T2_OLD, T2_NEW, '<span className="tg266"><i')
    t = lit(t, "290: list name", B2_OLD, B2_NEW, "<b>{gxTy290(q)}</b>")
    return t

edit(APP, change)
