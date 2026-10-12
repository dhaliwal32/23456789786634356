#!/usr/bin/env python3
"""
news_logos.py (version 2, October 2026) - installs app changes and refreshes game times for Fantasy Islands GM.

The News and logos workflow runs these:
  python news_logos.py games   refresh games-data.js (every 6 hours)
  python news_logos.py test    try every round: writes fantasy-gm-test.html and checks other files; nothing live changes
  python news_logos.py live    apply every round to the real files (saves an undo copy in .undo first)
  python news_logos.py undo    put the files back exactly as they were before the last live run

Rounds 1 to 67 (September and October 2026) are already part of the files. The old installer that held
their code is in this repo's history if it is ever needed.

Adding a change: write a function that takes a file's text and returns the new text, then register it
below it with  ROUNDS.append((APP, round68))  (or another file name). Paste new rounds just above the
line  if __name__ == "__main__":  at the bottom. Each edit uses lit, block or sub_once, which stop the
whole run (and change nothing) if the text is not found exactly once.
"""
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import urllib.request
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

APP, APP_TEST = "fantasy-gm.html", "fantasy-gm-test.html"
GAMES = "games-data.js"
UNDO = ".undo"
BABEL = "/tmp/babel/node_modules/@babel/standalone"
ALIAS = {"LAK": "LA", "NJD": "NJ", "SJS": "SJ", "TBL": "TB", "ARI": "UTA", "UTAH": "UTA"}
ROOT = 'ReactDOM.createRoot(document.getElementById("root")).render(<App />);'
ROUNDS = []      # (file name, function that takes the file text and returns the new text)
NEW_FILES = {}   # file name -> full text, for whole new pages


# ---------- tools ----------
def fail(msg):
    print("STOPPED - nothing was changed: " + msg)
    sys.exit(1)


def sub_once(text, name, pat, rep, done=None, flags=0, count=1):
    if done and done in text:
        print(f"(news) {name}: already done")
        return text
    new, n = re.subn(pat, lambda m: rep, text, flags=flags)
    if n != count:
        fail(f"'{name}' matched {n} times (expected {count}). Send this log to the AI helper.")
    print(f"(news) {name}: updated")
    return new


def lit(text, name, old, new, done=None, count=1):
    return sub_once(text, name, re.escape(old), new, done, 0, count)


def block(text, name, start, end, rep, done):
    pat = re.escape(start) + r"\r?\n.*?(?=" + re.escape(end) + ")"
    return sub_once(text, name, pat, rep, done, re.S)


def py_ok(name, src):
    try:
        compile(src, name, "exec")
    except SyntaxError as ex:
        fail(f"{name} would have a Python error after the change (line {ex.lineno}): {ex.msg}")


def babel_ok(code, name):
    if not shutil.which("node") or not os.path.exists(BABEL):
        print(f"(news) {name}: syntax check skipped (checker not installed)")
        return
    pathlib.Path("/tmp/check.jsx").write_text(code, encoding="utf-8")
    js = ("const B=require(%r);const fs=require('fs');try{B.transform(fs.readFileSync('/tmp/check.jsx','utf8'),"
          "{presets:['react']});console.log('ok')}catch(e){console.log(e.message);process.exit(1)}") % BABEL
    r = subprocess.run(["node", "-e", js], capture_output=True, text=True)
    if r.returncode:
        fail(f"{name} would have a syntax error: " + (r.stdout or r.stderr)[:600])
    print(f"(news) {name}: syntax check ok")


def check(name, text):
    if name.endswith(".py"):
        py_ok(name, text)
    elif name.endswith(".js"):
        babel_ok(text, name)
    elif name == APP:
        m = re.search(r'<script type="text/babel">(.*?)</script>', text, re.S)
        if not m:
            fail("could not find the app code in fantasy-gm.html")
        for must in (ROOT, "function App(", "function Today(", "function SetupPage("):
            if must not in text:
                fail("fantasy-gm.html looks damaged (" + must + ").")
        babel_ok(m.group(1), APP)
    elif name.endswith(".html"):
        code = "\n;\n".join(re.findall(r"<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>", text, re.S))
        if code.strip():
            babel_ok(code, name)


def test_name(f):
    p = pathlib.Path(f)
    return APP_TEST if f == APP else str(p.with_name(p.stem + "-test" + p.suffix))


# ---------- game times ----------
def ab(x):
    x = (x or "").upper()
    return ALIAS.get(x, x)


def games():
    start = datetime.now(ZoneInfo("America/New_York")).date() - timedelta(days=3)
    out, ok = {}, 0
    for k in range(6):
        d = (start + timedelta(days=7 * k)).isoformat()
        try:
            req = urllib.request.Request(f"https://api-web.nhle.com/v1/schedule/{d}", headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=30) as r:
                js = json.load(r)
            ok += 1
        except Exception as ex:
            print(f"(games) week of {d} failed: {type(ex).__name__}: {ex}")
            continue
        for day in js.get("gameWeek", []):
            for g in day.get("games", []):
                if g.get("gameType") != 2:
                    continue
                h, a = ab(g["homeTeam"]["abbrev"]), ab(g["awayTeam"]["abbrev"])
                st = g.get("startTimeUTC") or ""
                dd = out.setdefault(day["date"], {})
                dd[h] = {"o": a, "h": 1, "st": st}
                dd[a] = {"o": h, "h": 0, "st": st}
    n = sum(len(v) for v in out.values()) // 2
    if not n:
        fail(f"no games downloaded ({ok}/6 weeks reached the NHL). The old games-data.js is kept.")
    p = pathlib.Path(GAMES)
    if p.exists():
        try:
            old = json.loads(p.read_text(encoding="utf-8").split("=", 1)[1].strip().rstrip(";"))
            if old.get("games") == out:
                print(f"(games) {n} games, no changes since last time")
                return
        except Exception:
            pass
    data = {"generated": datetime.now(timezone.utc).isoformat(timespec="seconds"), "games": out}
    p.write_text("window.GAMES_DATA = " + json.dumps(data, separators=(",", ":")) + ";\n", encoding="utf-8")
    print(f"(games) wrote {GAMES}: {n} games over {len(out)} days")


# ---------- undo ----------
def undo():
    man = pathlib.Path(UNDO) / "files.json"
    if not man.exists():
        fail("nothing to undo - no live run has saved an undo copy yet.")
    files = json.loads(man.read_text(encoding="utf-8"))
    for f, existed in files.items():
        if existed:
            pathlib.Path(f).write_text((pathlib.Path(UNDO) / f.replace("/", "__")).read_text(encoding="utf-8"), encoding="utf-8")
            print(f"(news) undo: put back {f}")
        else:
            pathlib.Path(f).unlink(missing_ok=True)
            print(f"(news) undo: removed {f} (it was new in the last live run)")
    shutil.rmtree(UNDO, ignore_errors=True)
    print("(news) undo finished - the files are as they were before the last live run")


# ---------- test and live ----------
def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "test"
    if mode == "games":
        games()
        return
    if mode == "undo":
        undo()
        return
    if mode not in ("test", "live"):
        fail("mode must be test, live, undo or games")
    names = [APP]
    for f in [f for f, _ in ROUNDS] + list(NEW_FILES):
        if f not in names:
            names.append(f)
    out = {}
    for f in names:
        p = pathlib.Path(f)
        before = p.read_text(encoding="utf-8") if p.exists() else None
        if f in NEW_FILES:
            after = NEW_FILES[f]
        elif before is None:
            fail(f"{f} is missing from the repo")
        else:
            after = before
        for g, fn in ROUNDS:
            if g == f:
                after = fn(after)
        check(f, after)
        out[f] = (before, after)
    if mode == "test":
        for f, (b, a) in out.items():
            if f == APP or f in NEW_FILES:
                pathlib.Path(test_name(f)).write_text(a, encoding="utf-8")
                print(f"(news) test copy written - open {test_name(f)} to check")
            elif a != b:
                print(f"(news) {f}: changes checked - they are applied in live mode")
        print("(news) test finished - nothing live was changed")
        return
    changed = {f: v for f, v in out.items() if v[1] != v[0]}
    if not changed:
        print("(news) live: nothing to change - every round is already in the files")
        return
    u = pathlib.Path(UNDO)
    shutil.rmtree(u, ignore_errors=True)
    u.mkdir()
    files = {}
    for f, (b, a) in changed.items():
        files[f] = b is not None
        if b is not None:
            (u / f.replace("/", "__")).write_text(b, encoding="utf-8")
        pathlib.Path(f).write_text(a, encoding="utf-8")
        print(f"(news) {f} updated")
    (u / "files.json").write_text(json.dumps(files, indent=1), encoding="utf-8")
    print(f"(news) live finished - {len(changed)} file(s) changed; 'undo' puts them back")


# ---------- rounds (newest at the bottom, above the last line) ----------


if __name__ == "__main__":
    main()
