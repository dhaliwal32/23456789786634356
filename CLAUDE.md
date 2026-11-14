# Fantasy Islands GM: instructions for Claude Code

This repo is Kuvar's Fantasy Islands GM app: a personal ESPN NHL fantasy helper (10-team H2H points league, his team is "kanucks").
Live site: https://dhaliwal32.github.io/23456789786634356/fantasy-gm.html

## Read first, every session
1. `docs/how-to-make-a-change.md` (the full rulebook: change files, helpers, testing, lessons learned, change log, open ideas).
2. `docs/handoff.md` (what Kuvar likes, what he rejected and why, open requests).
3. `docs/notes/` (notes for changes not yet merged into the change log).
4. The rulebook's change log stops at 251. For 252 and later, the first line of each file in `changes/done/` says what it did.

If `docs/how-to-make-a-change.md` is missing, tell Kuvar to add it (copy from his claude.ai Fantasy GM project doc "Fantasy GM - how to make a change") before making any change.

If anything here and those docs disagree, the docs win, except where this file talks about how Claude Code works.

## Talking to Kuvar
- He is not a programmer. Plain words, short answers, no jargon, no emojis.
- When he asks for a change, make it go live right away, then show him phone and laptop pictures and say in one or two lines what changed. Do not ask for approval first.
- Never ask for ESPN cookies or API keys. They are GitHub Secrets (ESPN_S2, SWID, NTFY_TOPIC, ODDS_API_KEY).
- Never put the app password in the repo or in a message.
- Always show any email and confirm before sending anything.
- Every pop-up slides in smoothly, closes by tapping outside it, and returns him exactly where he was. He called this "set in stone for every change" (Nov 14). Details in the rulebook, section 1.
- Phone alerts come from the app itself (gm_push.py, change 278). ntfy is switched off; do not bring it back unless he asks.

## How a change works (short version; full version in the doc)
- Every change to the app is ONE Python file in `changes/`, named with the next number, e.g. `changes/275-short-name.py`. It is run by `install.py`.
- Next number: run `git fetch && git reset --hard origin/main`, then look at `changes/done/` and `changes/`. Highest number + 1. Another chat may have used a number minutes ago, so check again right before pushing.
- Never rewrite `fantasy-gm.html` by hand or from memory. Read the real code around the spot first (grep), then write exact `lit(...)` replacements. Every old text must appear exactly once (`grep -c -F '<text>' fantasy-gm.html`).
- New CSS goes before the one `</style>`; new helpers go just before `ROOT`. New names get a `Gx`/`gx` prefix plus the change number.
- Never edit a change file after pushing it. Make a new numbered change instead.
- After writing a change file, grep it for non-ASCII characters (escapes like `–` must stay six plain characters).
- Files under `.github/workflows/` cannot be edited by the install bot; commit those directly.

## Test before going live
1. In a scratch copy of the repo: put the change in `changes/`, run `python3 install.py live`. Must print "finished", not "STOPPED".
2. `npm install --prefix /tmp/babel @babel/standalone@7`, then `node build_app.js`. Check: `grep -c '_defineProperty({}, ' build/app.js` is 0, no `import`/`require("react` lines, all files in `build/` parse.
3. Look at it with Playwright at 390 wide (phone) and 1200 wide (laptop), dark mode (`window.__setTheme("dark")`), time zone America/Vancouver. Section 4 of the doc lists every trick (serving React locally, made-up ESPN games, password-locked data, where to click).
4. Watch for page errors and `console.error`.

## Going live
1. `git fetch && git reset --hard origin/main` (syncs commit every few minutes).
2. Commit only the change file to `main` and push. That starts the Install changes test run.
3. Start live: `gh workflow run install.yml -f mode=live` (if that fails, use `gh api -X POST repos/dhaliwal32/23456789786634356/actions/workflows/install.yml/dispatches -f ref=main -f 'inputs[mode]=live'`).
4. Check the run: `gh run list --workflow install.yml --limit 1`.
5. If something breaks after live: run the same workflow with mode `undo`.
6. Tell Kuvar to tap Refresh in Setup (or close and reopen on the phone).

## After every live change
- Add one row to the change log in `docs/how-to-make-a-change.md` and bump "Next change number" at the top. Commit that with the next sync-safe push.

## Health check (when asked "is it working?")
- Recent "sync ..." commits every 6 to 10 minutes.
- `ai/models/ai_proj.json` `asof` under 36 hours old.
- Latest Actions runs green: `gh run list --limit 10`.
