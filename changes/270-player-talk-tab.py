# changes/270-player-talk-tab.py - Player Talk: a Talk tab in every player's screen showing recent Reddit posts and comments about him (collected on Kuvar's Mac by talk_mac.py into talk/raw/), and the blocked GitHub collector switched off

NEW_CSS = r"""  /* change 270 (install.py) */
  .gx-tk270 .hd270 { display: flex; justify-content: space-between; align-items: baseline; gap: 8px; }
  .gx-tk270 .hd270 small { font-size: 12px; font-weight: 500; color: var(--mute); }
  .gx-tk270 .fl270 { display: flex; gap: 6px; margin: 8px 0 4px; overflow-x: auto; }
  .gx-tk270 .fl270 button { flex: 0 0 auto; font-size: 12.5px; padding: 6px 11px; border-radius: 16px; border: 1px solid var(--line); background: var(--card2, transparent); color: var(--mute); }
  .gx-tk270 .fl270 button.on { color: var(--ink); border-color: var(--accent); }
  .gx-tk270 .it270 { display: block; padding: 10px 0; border-bottom: 1px solid var(--line); text-decoration: none; color: inherit; }
  .gx-tk270 .it270 .mt270 { display: flex; gap: 6px; align-items: center; font-size: 11.5px; color: var(--mute); white-space: nowrap; overflow: hidden; }
  .gx-tk270 .it270 .mt270 b { color: var(--ink); font-weight: 700; }
  .gx-tk270 .it270 .mt270 .tg270 { font-size: 10.5px; font-weight: 700; padding: 1px 6px; border-radius: 4px; background: var(--line); color: var(--ink); }
  .gx-tk270 .it270 .mt270 .tg270.d270 { background: #f5a524; color: #121212; }
  .gx-tk270 .it270 .tx270 { font-size: 14px; line-height: 1.4; margin-top: 4px; color: var(--ink); display: -webkit-box; -webkit-line-clamp: 4; -webkit-box-orient: vertical; overflow: hidden; }
  .gx-tk270 .it270 .th270 { font-size: 11.5px; color: var(--mute); margin-top: 3px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .gx-tk270 .em270 { font-size: 13px; color: var(--mute); padding: 12px 0; }
</style>"""

HELPERS = r"""// ---------- change 270: Player Talk tab (install.py) ----------
// Reddit posts and comments from talk/raw/<subreddit>.json (uploaded by talk_mac.py on Kuvar's Mac every 3 hours);
// the app picks the ones that mention this player: full name anywhere, last name alone only when no other player shares it
const GX_SUB270 = { ANA: "AnaheimDucks", BOS: "BostonBruins", BUF: "sabres", CAR: "canes", CBJ: "BlueJackets", CGY: "CalgaryFlames", CHI: "hawks", COL: "ColoradoAvalanche", DAL: "DallasStars", DET: "DetroitRedWings", EDM: "EdmontonOilers", FLA: "FloridaPanthers", LA: "losangeleskings", MIN: "wildhockey", MTL: "Habs", NJ: "devils", NSH: "Predators", NYI: "NewYorkIslanders", NYR: "rangers", OTT: "OttawaSenators", PHI: "Flyers", PIT: "penguins", SEA: "SeattleKraken", SJ: "SanJoseSharks", STL: "stlouisblues", TB: "TampaBayLightning", TOR: "leafs", UTA: "UtahHockeyClub", UTAH: "UtahHockeyClub", VAN: "canucks", VGK: "goldenknights", WPG: "winnipegjets", WSH: "caps" };
window.__TK270 = window.__TK270 || {};
function gxTkLoad270(name) {
  const c = window.__TK270[name], now = Date.now();
  if (c && now - c.at < 10 * 60e3) return c.p;
  const p = fetch("talk/raw/" + name + ".json?v=" + Math.floor(now / 600e3)).then((r) => (r.ok ? r.json() : null)).catch(() => null);
  window.__TK270[name] = { at: now, p };
  return p;
}
const gxTkN270 = (s) => String(s || "").normalize("NFKD").replace(/[\u0300-\u036f]/g, "").toLowerCase().replace(/[^a-z0-9]+/g, " ").trim();
function gxTkLasts270(s) {
  const k = s.players.length;
  if (window.__TKL270 && window.__TKL270.k === k) return window.__TKL270.m;
  const m = {};
  s.players.forEach((q) => { const l = gxTkN270(String(q.n || "").split(" ").slice(1).join(" ")); if (l) (m[l] = m[l] || []).push(q.t); });
  window.__TKL270 = { k, m };
  return m;
}
const gxAgo270 = (iso) => { const m = Math.max(0, (Date.now() - Date.parse(iso)) / 60e3); return m < 60 ? Math.round(m) + "m" : m < 48 * 60 ? Math.round(m / 60) + "h" : Math.round(m / 1440) + "d"; };
function GxTalk270({ p, s }) {
  const [d, setD] = useState(null), [f, setF] = useState("all");
  const team = GX_SUB270[p.t] || "";
  useEffect(() => {
    let on = true;
    Promise.all([gxTkLoad270("_meta"), gxTkLoad270("fantasyhockey"), gxTkLoad270("hockey"), team ? gxTkLoad270(team) : Promise.resolve(null)]).then(([m, fh, hk, tm]) => {
      if (!on) return;
      const full = " " + gxTkN270(p.n) + " ", last = gxTkN270(String(p.n || "").split(" ").slice(1).join(" ")), L = gxTkLasts270(s)[last] || [];
      const anyOk = last.length > 3 && L.length === 1, teamOk = last.length > 3 && L.filter((t) => t === p.t).length === 1;
      const hit = (it, okLast) => { const x = " " + gxTkN270((it.h || "") + " " + it.x) + " "; return x.indexOf(full) >= 0 || (okLast && x.indexOf(" " + last + " ") >= 0); };
      const out = [], seen = {};
      const take = (src, sub, okLast) => ((src || {}).items || []).forEach((it) => { if (!seen[it.u] && hit(it, okLast)) { seen[it.u] = 1; out.push({ ...it, sub }); } });
      take(tm, team, teamOk); take(fh, "fantasyhockey", anyOk); take(hk, "hockey", anyOk);
      out.sort((a, b) => (a.t < b.t ? 1 : -1));
      setD({ items: out, upd: m && m.upd, none: !m && !fh && !hk });
    });
    return () => { on = false; };
  }, [p.id]);
  if (!d) return <div className="gx-pd-pn gx-tk270" data-gx="270"><div className="gx-pd-h">Talk</div><div className="em270">Loading Reddit...</div></div>;
  const subs = [["all", "All"], ["team", team ? "r/" + team : ""], ["fantasyhockey", "r/fantasyhockey"], ["hockey", "r/hockey"]].filter((x) => x[1]);
  const L = d.items.filter((it) => f === "all" || (f === "team" ? it.sub === team : it.sub === f)).slice(0, 40);
  const stale = d.upd && Date.now() - Date.parse(d.upd) > 8 * 3600e3;
  return (
    <div className="gx-pd-pn gx-tk270" data-gx="270">
      <div className="gx-pd-h hd270"><span>Talk</span><small>{d.upd ? "Reddit, updated " + gxAgo270(d.upd) + " ago" : ""}</small></div>
      {d.none ? <div className="em270">No Reddit posts yet. They come from the script on your Mac every 3 hours.</div> : (<>
        <div className="fl270">{subs.map(([k, l]) => <button key={k} type="button" className={f === k ? "on" : ""} onClick={() => setF(k)}>{l}</button>)}</div>
        {stale ? <div className="em270" style={{ paddingTop: 4 }}>Your Mac hasn't sent new posts for a while (it only runs while the Mac is awake).</div> : null}
        {L.length ? L.map((it) => (
          <a key={it.u} className="it270" href={it.u} target="_blank" rel="noopener" onClick={gxWatchGo211}>
            <div className="mt270"><b>{"r/" + it.sub}</b><span>{gxAgo270(it.t)}</span>{it.d ? <span className="tg270 d270">Daily Discussion</span> : <span className="tg270">{it.k === "c" ? "Comment" : "Post"}</span>}<span>{"u/" + it.w}</span></div>
            <div className="tx270">{it.x}</div>
            {it.h ? <div className="th270">{"in: " + it.h}</div> : null}
          </a>
        )) : <div className="em270">{"Nobody on these subreddits has mentioned " + p.n + " in the last 3 days."}</div>}
      </>)}
    </div>
  );
}
"""

TALK_MAC = r'''#!/usr/bin/env python3
"""
talk_mac.py - Fantasy Islands GM, Player Talk collector that runs on Kuvar's Mac (change 270).

Reddit refuses GitHub's servers, so this runs on the Mac every 3 hours (launchd) from home internet.
It reads Reddit's public RSS feeds (newest comments and posts of all 32 team subreddits, r/fantasyhockey with the
Daily Discussion thread, and r/hockey), keeps the last 3 days, and uploads talk/raw/<subreddit>.json to the repo
in one commit through the GitHub API. It needs no roster: the app picks out the posts about each player itself.

The GitHub key is read from the Mac Keychain (service "fantasy-gm-talk", account "talk"); it is never in a file.
Only Python's own modules are used, so nothing has to be installed.
Run by hand:  python3 ~/FantasyTalk/talk_mac.py
"""
import base64
import hashlib
import html
import json
import os
import re
import subprocess
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone

REPO = "dhaliwal32/23456789786634356"
BRANCH = "main"
HOME = os.path.join(os.path.expanduser("~"), "FantasyTalk")
DATA = os.path.join(HOME, "data")
UA = "FantasyIslandsGM/1.0 (personal fantasy hockey app; macOS; github.com/dhaliwal32)"
KEEP_DAYS = 3
MAX_ITEMS = 400
GAP_S = 1.5
NS = {"a": "http://www.w3.org/2005/Atom"}
TEAM_SUBS = ["AnaheimDucks", "BostonBruins", "sabres", "canes", "BlueJackets", "CalgaryFlames", "hawks", "ColoradoAvalanche",
             "DallasStars", "DetroitRedWings", "EdmontonOilers", "FloridaPanthers", "losangeleskings", "wildhockey", "Habs",
             "devils", "Predators", "NewYorkIslanders", "rangers", "OttawaSenators", "Flyers", "penguins", "SeattleKraken",
             "SanJoseSharks", "stlouisblues", "TampaBayLightning", "leafs", "UtahHockeyClub", "canucks", "goldenknights",
             "winnipegjets", "caps"]
BOTS = {"automoderator", "sportsbot", "nhl_bot", "[deleted]", "gdt_bot", "nhl_gdt"}
BAD = re.compile(r"\b(retard\w*|f[a@]gg?\w*|n[i1]gg\w*|kys)\b", re.I)


def log(m):
    print(datetime.now().strftime("%Y-%m-%d %H:%M"), m, flush=True)


def plain(s):
    s = re.sub(r"<[^>]+>", " ", html.unescape(s or ""))
    s = html.unescape(s)
    s = re.sub(r"submitted by\s+/u/\S+.*$", "", s, flags=re.S)
    s = re.sub(r"\[link\]|\[comments\]", "", s)
    return re.sub(r"\s+", " ", s).strip()


def cut(s, n=300):
    if len(s) <= n:
        return s
    return s[:n].rsplit(" ", 1)[0].rstrip(",.;:-") + "..."


FAILS = [0]


def feed(url):
    if FAILS[0] >= 6:
        return None
    for attempt in (1, 2):
        time.sleep(GAP_S if attempt == 1 else 12)
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=20) as r:
                root = ET.fromstring(r.read())
            FAILS[0] = 0
            break
        except urllib.error.HTTPError as ex:
            if ex.code == 429 and attempt == 1:
                continue
            FAILS[0] += 1
            log(f"{ex.code} {url}")
            return None
        except Exception as ex:
            FAILS[0] += 1
            log(f"failed {url}: {ex}")
            return None
    out = []
    for e in root.findall("a:entry", NS):
        g = lambda k: (e.findtext("a:" + k, default="", namespaces=NS) or "").strip()
        ln = e.find("a:link", NS)
        au = e.find("a:author/a:name", NS)
        who = (au.text or "").replace("/u/", "").strip() if au is not None else ""
        url_ = ln.get("href") if ln is not None else ""
        if not url_ or who.lower() in BOTS:
            continue
        title = plain(g("title"))
        body = plain(g("content"))
        is_c = re.search(r"/comments/\w+/[^/]*/\w+/?$", url_) is not None
        if is_c:
            text, head = body, re.sub(r"^/?u/\S+ on ", "", title)
        else:
            text, head = title + (". " + body if body and body != title else ""), ""
        if len(text) < 20 or BAD.search(text) or (text.upper() == text and len(text) > 30):
            continue
        out.append({"u": url_, "t": g("updated") or g("published"), "w": who, "k": "c" if is_c else "p", "h": cut(head, 120), "x": cut(text)})
    return out


def collect():
    got = {}
    def add(sub, items):
        if items is not None:
            got.setdefault(sub, []).extend(items)
    for s in ["fantasyhockey", "hockey"] + TEAM_SUBS:
        add(s, feed(f"https://www.reddit.com/r/{s}/comments/.rss?limit=100"))
        add(s, feed(f"https://www.reddit.com/r/{s}/new/.rss?limit={50 if s in ('fantasyhockey', 'hockey') else 25}"))
    # newest Daily Discussion thread in r/fantasyhockey: its comments too
    q = urllib.parse.quote('title:"Daily Discussion"')
    th = feed(f"https://www.reddit.com/r/fantasyhockey/search.rss?q={q}&restrict_sr=on&sort=new&t=week") or []
    if th:
        dd = feed(th[0]["u"].rstrip("/") + "/.rss?limit=100&sort=new")
        if dd:
            for it in dd:
                it["d"] = 1
            add("fantasyhockey", dd)
    return got


def merge(sub, new):
    path = os.path.join(DATA, sub + ".json")
    try:
        old = json.load(open(path)).get("items", [])
    except Exception:
        old = []
    cutoff = datetime.now(timezone.utc) - timedelta(days=KEEP_DAYS)
    seen, items = set(), []
    for it in new + old:
        key = it["u"]
        if key in seen:
            continue
        try:
            if datetime.fromisoformat(it["t"].replace("Z", "+00:00")) < cutoff:
                continue
        except Exception:
            continue
        seen.add(key)
        items.append(it)
    items.sort(key=lambda x: x["t"], reverse=True)
    body = {"sub": sub, "upd": datetime.now(timezone.utc).isoformat(timespec="seconds"), "items": items[:MAX_ITEMS]}
    json.dump(body, open(path, "w"), ensure_ascii=False, separators=(",", ":"))
    return body


def token():
    try:
        return subprocess.run(["security", "find-generic-password", "-s", "fantasy-gm-talk", "-a", "talk", "-w"],
                              capture_output=True, text=True, check=True).stdout.strip()
    except Exception:
        log("no GitHub key in the Keychain (service fantasy-gm-talk); see the setup steps")
        return ""


def gh(tok, method, path, body=None):
    req = urllib.request.Request("https://api.github.com/repos/" + REPO + path, method=method,
                                 data=json.dumps(body).encode() if body is not None else None,
                                 headers={"Authorization": "Bearer " + tok, "Accept": "application/vnd.github+json",
                                          "User-Agent": UA, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read() or b"{}")


def upload(files):
    tok = token()
    if not tok or not files:
        return False
    for attempt in range(4):
        try:
            head = gh(tok, "GET", f"/git/ref/heads/{BRANCH}")["object"]["sha"]
            base = gh(tok, "GET", f"/git/commits/{head}")["tree"]["sha"]
            tree = gh(tok, "POST", "/git/trees", {"base_tree": base, "tree": [
                {"path": p, "mode": "100644", "type": "blob", "content": c} for p, c in files.items()]})["sha"]
            com = gh(tok, "POST", "/git/commits", {"message": "talk " + datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ"),
                                                    "tree": tree, "parents": [head]})["sha"]
            gh(tok, "PATCH", f"/git/refs/heads/{BRANCH}", {"sha": com})
            return True
        except urllib.error.HTTPError as ex:
            log(f"GitHub upload try {attempt + 1}: {ex.code} {ex.read()[:200]!r}")
            if ex.code in (401, 403, 404):
                return False
            time.sleep(5)
        except Exception as ex:
            log(f"GitHub upload try {attempt + 1}: {ex}")
            time.sleep(5)
    return False


def main():
    os.makedirs(DATA, exist_ok=True)
    t0 = time.time()
    got = collect()
    if not got:
        log("Reddit gave nothing this time; nothing uploaded")
        return
    sent = {}
    try:
        sent = json.load(open(os.path.join(HOME, "sent.json")))
    except Exception:
        pass
    files, meta = {}, {}
    for sub, new in got.items():
        body = merge(sub, new)
        txt = json.dumps(body, ensure_ascii=False, separators=(",", ":"))
        h = hashlib.sha1(json.dumps(body["items"]).encode()).hexdigest()
        meta[sub] = {"n": len(body["items"]), "upd": body["upd"]}
        if sent.get(sub) != h:
            files["talk/raw/" + sub + ".json"] = txt
            sent[sub] = h
    files["talk/raw/_meta.json"] = json.dumps({"upd": datetime.now(timezone.utc).isoformat(timespec="seconds"), "from": "mac", "subs": meta}, separators=(",", ":"))
    ok = upload(files)
    if ok:
        json.dump(sent, open(os.path.join(HOME, "sent.json"), "w"))
    log(f"{len(got)} subreddits, {sum(len(v) for v in got.values())} new items, {len(files)} files {'uploaded' if ok else 'NOT uploaded'}, {int(time.time() - t0)} s")


if __name__ == "__main__":
    main()
'''

def change(t):
    t = lit(t, "270: styles", "</style>", NEW_CSS, "change 270 (install.py)")
    t = lit(t, "270: helpers", ROOT, HELPERS + ROOT, "change 270: Player Talk tab")
    t = lit(t, "270: Talk tab button",
            'const tabs = [["ov", "Overview"], ["log", "Game log"], ["news", "News" + (news.length ? " (" + news.length + ")" : "")], ["lines", "Lines"]];',
            'const tabs = [["ov", "Overview"], ["log", "Game log"], ["news", "News" + (news.length ? " (" + news.length + ")" : "")], ["talk", "Talk"], ["lines", "Lines"]];',
            '["talk", "Talk"]')
    t = lit(t, "270: Talk tab body", '          {tab === "lines" ? (<>',
            '          {tab === "talk" ? <GxTalk270 p={p} s={s} /> : null}\n          {tab === "lines" ? (<>', "<GxTalk270 p={p} s={s} />")
    return t

def unhook(t):
    return lit(t, "270: GitHub collector off (Reddit blocks GitHub)",
               "        try:  # change 268: player talk from Reddit\n            import gm_talk\n            gm_talk.run()\n        except Exception as ex:\n            print(f\"(talk) WARNING: {ex}\")\n",
               "        # change 270: gm_talk.py off - Reddit refuses GitHub's servers; talk_mac.py on Kuvar's Mac collects instead\n",
               "change 270: gm_talk.py off")

edit(APP, change)
edit("gm_notify.py", unhook)
new_file("talk_mac.py", TALK_MAC)
