"""
install_ask.py - adds the 💬 Ask button to fantasy-gm.html with 2 small, checked edits.

  python install_ask.py test   -> writes fantasy-gm-ask-test.html (the real app is untouched)
  python install_ask.py live   -> backs up fantasy-gm.html to fantasy-gm.before-ask.html, then edits it
  python install_ask.py undo   -> puts fantasy-gm.before-ask.html back

Nothing is written unless every original line is found exactly once.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.join(HERE, "fantasy-gm.html")
TEST = os.path.join(HERE, "fantasy-gm-ask-test.html")
BACKUP = os.path.join(HERE, "fantasy-gm.before-ask.html")
MARK = "ask-panel.js"

LOADER = ("<script>document.write('<script type=\"text/babel\" data-presets=\"react\" "
          "src=\"ask-panel.js?t=' + Date.now() + '\"><\\/script>');</script>")

MOUNT = ('        {window.AskPanel ? <window.AskPanel {...P} tab={tab} H={{ effAvg, sigOf, tags, avail, effBack, gStart, '
         'teamName, f1, computeMoves, weekProj, oppOf, todayISO }} /> : null}')

EDITS = [
    ('<div id="root"></div>', LOADER + '\n<div id="root"></div>'),
    ('        {content}\n', '        {content}\n' + MOUNT + '\n'),
]


def read(path):
    with open(path, encoding="utf-8", newline="") as f:
        return f.read()


def write(path, text):
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)


def patch(text):
    if MARK in text:
        sys.exit("The Ask button is already installed in fantasy-gm.html - nothing to do.")
    text = text.replace("\r\n", "\n") if "\r\n" in text else text
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
            sys.exit("No backup found (fantasy-gm.before-ask.html) - nothing to undo.")
        shutil.copyfile(BACKUP, APP)
        print("Restored fantasy-gm.html from fantasy-gm.before-ask.html.")
        return
    if not os.path.exists(os.path.join(HERE, "ask-panel.js")):
        sys.exit("ask-panel.js is missing from the repo - add it first. Nothing was changed.")
    new = patch(read(APP))
    if mode == "test":
        write(TEST, new)
        print("Wrote fantasy-gm-ask-test.html - fantasy-gm.html was NOT changed.")
    elif mode == "live":
        shutil.copyfile(APP, BACKUP)
        write(APP, new)
        print("Backed up to fantasy-gm.before-ask.html and installed the Ask button in fantasy-gm.html.")
    else:
        sys.exit("Mode must be test, live or undo.")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "")
