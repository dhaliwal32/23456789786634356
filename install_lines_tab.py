"""
install_lines_tab.py - adds the Lines tab to fantasy-gm.html with 3 small, checked edits.

  python install_lines_tab.py test   -> writes fantasy-gm-lines-test.html (the real app is untouched)
  python install_lines_tab.py live   -> backs up fantasy-gm.html to fantasy-gm.before-lines.html, then edits it
  python install_lines_tab.py undo   -> puts fantasy-gm.before-lines.html back

Nothing is written unless every original line is found exactly once.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.join(HERE, "fantasy-gm.html")
TEST = os.path.join(HERE, "fantasy-gm-lines-test.html")
BACKUP = os.path.join(HERE, "fantasy-gm.before-lines.html")
MARK = "lines-tab.js"

LOADER = ("<script>window.LINES_DATA = null; "
          "document.write('<script src=\"lines-data.js?t=' + Date.now() + '\"><\\/script>'); "
          "document.write('<script type=\"text/babel\" data-presets=\"react\" src=\"lines-tab.js?t=' + Date.now() + '\"><\\/script>');</script>")

ROUTE = ('  else if (tab === "lines") content = window.LinesTab ? <window.LinesTab {...P} H={{ effAvg, sigOf, Tags, avail, effBack, '
         'gStart, teamName, f1, Section, Card, Pills, inp, todayISO, dayLabel }} /> : <div className="text-slate-400 p-4">'
         'The Lines tab could not load (lines-tab.js). Refresh the page; if it keeps happening, check that lines-tab.js is in the repo.</div>;')

EDITS = [
    ('<div id="root"></div>', LOADER + '\n<div id="root"></div>'),
    ('  ["players", "', '  ["lines", "🏒 Lines", null],\n  ["players", "'),
    ('  else if (tab === "players") content = <Players {...P} />;',
     '  else if (tab === "players") content = <Players {...P} />;\n' + ROUTE),
]


def read(path):
    with open(path, encoding="utf-8", newline="") as f:
        return f.read()


def write(path, text):
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)


def patch(text):
    if MARK in text:
        sys.exit("The Lines tab is already installed in fantasy-gm.html - nothing to do.")
    for i, (old, _) in enumerate(EDITS, 1):
        n = text.count(old)
        if n != 1:
            sys.exit(f"Edit {i}: expected the original line exactly once but found it {n} times - NOTHING was changed.")
    for old, new in EDITS:
        text = text.replace(old, new, 1)
    return text


def main(mode):
    if mode == "undo":
        if not os.path.exists(BACKUP):
            sys.exit("No backup found (fantasy-gm.before-lines.html) - nothing to undo.")
        shutil.copyfile(BACKUP, APP)
        print("Restored fantasy-gm.html from fantasy-gm.before-lines.html.")
        return
    if not os.path.exists(os.path.join(HERE, "lines-tab.js")):
        sys.exit("lines-tab.js is missing from the repo - add it first. Nothing was changed.")
    if not os.path.exists(os.path.join(HERE, "lines-data.js")):
        print("NOTE: lines-data.js doesn't exist yet - run 'Fantasy sync' once so the tab has data.")
    new = patch(read(APP))
    if mode == "test":
        write(TEST, new)
        print("Wrote fantasy-gm-lines-test.html - fantasy-gm.html was NOT changed.")
    elif mode == "live":
        shutil.copyfile(APP, BACKUP)
        write(APP, new)
        print("Backed up to fantasy-gm.before-lines.html and installed the Lines tab in fantasy-gm.html.")
    else:
        sys.exit("Mode must be test, live or undo.")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "")
