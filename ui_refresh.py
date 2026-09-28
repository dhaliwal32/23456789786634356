#!/usr/bin/env python3
"""UI refresh installer for fantasy-gm.html.
Removes emojis and makes the home-screen score font match the Matchup tab.
Usage: python ui_refresh.py test | live | undo
"""
import pathlib
import re
import shutil
import sys

SRC = pathlib.Path("fantasy-gm.html")
TEST = pathlib.Path("fantasy-gm-test.html")
BACKUP = pathlib.Path("fantasy-gm.backup-ui.html")
VS = "\ufe0f?"  # optional emoji variation selector
DOT = "\u25cf"  # a small filled circle

# (name, pattern, replacement, text that proves it is already done)
EXACT = [
    ("score font",
     r"^[ \t]*\.text-4xl \{[^\n]*\}[ \t]*$",
     "  .text-4xl { font-weight: 600 !important; font-size: 2.75rem !important; line-height: 1.1; margin-top: .4rem; margin-bottom: .2rem; letter-spacing: -0.03em; font-variant-numeric: tabular-nums; }",
     None),
    ("lineup check icons",
     r'\{ bad: "\u26d4' + VS + r'", warn: "\u26a0' + VS + r'", good: "\u2705' + VS + r'" \}',
     '{ bad: "' + DOT + '", warn: "' + DOT + '", good: "' + DOT + '" }',
     'bad: "' + DOT + '"'),
    ("data source status icons",
     r'\{ok \? "\u2705' + VS + r'" : "\u26aa' + VS + r'"\}',
     '<span className={ok ? "text-green-700" : "text-slate-400"}>' + DOT + "</span>",
     '"text-slate-400"}>' + DOT),
]
ARROWS = [(r"\u2b06" + VS, "\u2191"), (r"\u2b07" + VS, "\u2193")]  # big arrows -> clean arrows
STRIP = ("\U0001F3E0\u2694\U0001F501\U0001F3C6\U0001F3D2\U0001F465\u2699\U0001F9EA"
         "\U0001F4CA\U0001F945\U0001F3B2\U0001F525\u2744\u23F1\U0001F4C8\U0001F4F0"
         "\u26D4\u26A0\u2705\u26AA")


def fail(msg):
    print("STOPPED - nothing was changed: " + msg)
    sys.exit(1)


def transform(text):
    for name, pat, rep, done in EXACT:
        new, n = re.subn(pat, lambda m: rep, text, flags=re.M)
        if n == 1:
            print(f"(ui) {name}: updated")
            text = new
        elif n == 0 and done and done in text:
            print(f"(ui) {name}: already done")
        else:
            fail(f"'{name}' matched {n} times (expected exactly 1). Send this log to the AI helper.")
    for pat, rep in ARROWS:
        text, n = re.subn(pat, rep, text)
        print(f"(ui) arrows {rep}: {n} replaced")
    text, n = re.subn("[" + STRIP + "]\ufe0f? ?", "", text)
    print(f"(ui) emojis removed: {n}")
    left = [c for c in STRIP if c in text]
    if left:
        fail("some emojis are still there: " + " ".join(left))
    if "ReactDOM.createRoot" not in text or "const SR = {" not in text:
        fail("the app code looks damaged after the changes.")
    return text


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "test"
    if mode == "undo":
        if not BACKUP.exists():
            fail("no backup found - live mode has never been run.")
        shutil.copyfile(BACKUP, SRC)
        print("(ui) restored fantasy-gm.html from the backup")
        return
    original = SRC.read_text(encoding="utf-8")
    new = transform(original)
    if mode == "test":
        TEST.write_text(new, encoding="utf-8")
        print("(ui) wrote fantasy-gm-test.html - open it to check before going live")
    elif mode == "live":
        if not BACKUP.exists():
            BACKUP.write_text(original, encoding="utf-8")
            print("(ui) backup saved as fantasy-gm.backup-ui.html")
        SRC.write_text(new, encoding="utf-8")
        print("(ui) fantasy-gm.html updated")
    else:
        fail("mode must be test, live or undo")


if __name__ == "__main__":
    main()
