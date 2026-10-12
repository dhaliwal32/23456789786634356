#!/usr/bin/env python3
"""
install.py - puts changes into Fantasy Islands GM.

How a change works:
  1. A change is one small file in the changes folder, for example changes/068-goalie-colours.py.
     Make it on GitHub with Add file -> Create new file, paste, commit.
  2. Committing it starts the Install changes workflow in test mode by itself. It checks the change and writes
     fantasy-gm-test.html (and a -test copy of any new page). The run's summary has a link to the test page.
  3. When the test page looks right, run Install changes with "live". The change goes into the real files
     and its file moves to changes/done.
  4. "undo" puts the files back as they were before the last live run and moves that run's change files
     to changes/undone.

Inside a change file you can use: APP, ROOT, lit, block, sub_once, fail, py_ok, babel_ok,
edit(file name, function) and new_file(file name, full text).
Every edit must find its text exactly once, or the whole run stops and nothing changes.
Changes made before October 12, 2026 (rounds 1 to 67) are already part of the files.

Commands: python install.py test | live | undo
"""
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import time

APP, APP_TEST = "fantasy-gm.html", "fantasy-gm-test.html"
CHANGES = pathlib.Path("changes")
DONE, UNDONE = CHANGES / "done", CHANGES / "undone"
UNDO = pathlib.Path(".undo")
BABEL = "/tmp/babel/node_modules/@babel/standalone"
ROOT = 'ReactDOM.createRoot(document.getElementById("root")).render(<App />);'
SITE = "https://dhaliwal32.github.io/23456789786634356/"
EDITS, NEW, CUR = [], {}, [""]


# ---------- tools for change files ----------
def fail(msg):
    print("STOPPED - nothing was changed: " + msg)
    summary(["### Stopped - nothing was changed", msg])
    sys.exit(1)


def sub_once(text, name, pat, rep, done=None, flags=0, count=1):
    if done and done in text:
        print(f"(install) {name}: already done")
        return text
    new, n = re.subn(pat, lambda m: rep, text, flags=flags)
    if n != count:
        fail(f"'{name}' matched {n} times (expected {count}). Send this log to the AI helper.")
    print(f"(install) {name}: updated")
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
        print(f"(install) {name}: syntax check skipped (checker not installed)")
        return
    pathlib.Path("/tmp/check.jsx").write_text(code, encoding="utf-8")
    js = ("const B=require(%r);const fs=require('fs');try{B.transform(fs.readFileSync('/tmp/check.jsx','utf8'),"
          "{presets:['react']});console.log('ok')}catch(e){console.log(e.message);process.exit(1)}") % BABEL
    r = subprocess.run(["node", "-e", js], capture_output=True, text=True)
    if r.returncode:
        fail(f"{name} would have a syntax error: " + (r.stdout or r.stderr)[:600])
    print(f"(install) {name}: syntax check ok")


def edit(file, fn):
    EDITS.append((file, fn, CUR[0]))


def new_file(name, text):
    NEW[name] = text


# ---------- installer ----------
def summary(lines):
    p = os.environ.get("GITHUB_STEP_SUMMARY")
    if p:
        with open(p, "a", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")


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


def load():
    files = sorted(CHANGES.glob("*.py")) if CHANGES.is_dir() else []
    for f in files:
        CUR[0] = f.name
        ns = {"APP": APP, "ROOT": ROOT, "lit": lit, "block": block, "sub_once": sub_once, "fail": fail,
              "py_ok": py_ok, "babel_ok": babel_ok, "edit": edit, "new_file": new_file,
              "re": re, "json": json, "pathlib": pathlib}
        try:
            exec(compile(f.read_text(encoding="utf-8"), str(f), "exec"), ns)
        except SystemExit:
            raise
        except Exception as ex:
            fail(f"{f.name} has a mistake in it: {type(ex).__name__}: {ex}")
        print(f"(install) read {f.name}")
    return files


def run(mode):
    files = load()
    if not files:
        print("(install) no changes waiting in the changes folder")
    names = [APP]
    for f in [e[0] for e in EDITS] + list(NEW):
        if f not in names:
            names.append(f)
    out = {}
    for f in names:
        p = pathlib.Path(f)
        before = p.read_text(encoding="utf-8") if p.exists() else None
        if f in NEW:
            after = NEW[f]
        elif before is None:
            fail(f"{f} is missing from the repo")
        else:
            after = before
        for g, fn, src in EDITS:
            if g != f:
                continue
            try:
                after = fn(after)
            except SystemExit:
                raise
            except Exception as ex:
                fail(f"{src} has a mistake in it: {type(ex).__name__}: {ex}")
        check(f, after)
        out[f] = (before, after)
    waiting = ", ".join(x.name for x in files) or "none"
    if mode == "test":
        stamp, links = int(time.time()), []
        for f, (b, a) in out.items():
            if f == APP or f in NEW:
                pathlib.Path(test_name(f)).write_text(a, encoding="utf-8")
                links.append(f"- Open [{test_name(f)}]({SITE}{test_name(f)}?v={stamp}) about a minute after this run finishes")
            elif a != b:
                print(f"(install) {f}: changes checked - they are applied in live mode")
        print("(install) test finished - nothing live was changed")
        summary(["### Test finished - nothing live was changed", f"Changes checked: {waiting}", ""] + links
                + ["", "If it looks right, run **Install changes** again with **live**."])
        return
    changed = {f: v for f, v in out.items() if v[1] != v[0]}
    if not changed and not files:
        print("(install) live: nothing waiting")
        summary(["### Nothing waiting", "There are no change files in the changes folder."])
        return
    shutil.rmtree(UNDO, ignore_errors=True)
    UNDO.mkdir()
    saved = {}
    for f, (b, a) in changed.items():
        saved[f] = b is not None
        if b is not None:
            (UNDO / f.replace("/", "__")).write_text(b, encoding="utf-8")
        pathlib.Path(f).write_text(a, encoding="utf-8")
        print(f"(install) {f} updated")
    DONE.mkdir(parents=True, exist_ok=True)
    for x in files:
        x.rename(DONE / x.name)
    (UNDO / "files.json").write_text(json.dumps({"files": saved, "changes": [x.name for x in files]}, indent=1), encoding="utf-8")
    print(f"(install) live finished - {len(changed)} file(s) changed")
    summary(["### Live - the app is updated", f"Changes put in: {waiting}", f"Files changed: {', '.join(changed) or 'none'}",
             "", "Tap Refresh in the app's Setup. If something is wrong, run **Install changes** with **undo**."])


def undo():
    man = UNDO / "files.json"
    if not man.exists():
        fail("nothing to undo - no live run has saved an undo copy yet.")
    data = json.loads(man.read_text(encoding="utf-8"))
    for f, existed in data.get("files", {}).items():
        if existed:
            pathlib.Path(f).write_text((UNDO / f.replace("/", "__")).read_text(encoding="utf-8"), encoding="utf-8")
            print(f"(install) undo: put back {f}")
        else:
            pathlib.Path(f).unlink(missing_ok=True)
            print(f"(install) undo: removed {f} (it was new in the last live run)")
    UNDONE.mkdir(parents=True, exist_ok=True)
    for n in data.get("changes", []):
        if (DONE / n).exists():
            (DONE / n).rename(UNDONE / n)
    shutil.rmtree(UNDO, ignore_errors=True)
    print("(install) undo finished")
    summary(["### Undone", "The files are back to how they were before the last live run.",
             "That run's change files are in changes/undone."])


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "test"
    if mode == "undo":
        undo()
    elif mode in ("test", "live"):
        run(mode)
    else:
        fail("mode must be test, live or undo")
