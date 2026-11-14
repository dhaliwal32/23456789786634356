# Fantasy Islands GM: how to make a change

Read this first in any new session about Fantasy Islands GM. It covers everything through change 251 (Nov 9, 2026); changes 252 to 274 are described by the first line of each file in `changes/done/` and by `docs/notes/`. It adds to the Oct 11 handoff PDF, which still holds the background: league settings, data files and alert keys.

**Next change number: 285.** Whoever installs a change bumps this number and adds one line to the change log at the bottom.

## 1. Who Kuvar is and how to talk to him

- Kuvar is not a programmer. Give exact GitHub steps: file name, where to click, what to paste. Keep Python indentation exact.
- Use plain words: no jargon, no emojis. Keep the app uncluttered and phone-sized: short lists, one-line summaries, logos beside players.
- **When Kuvar asks for a change, make it go live right away (said Oct 28).** Test it as in section 4, commit it, run live, then show him the pictures and say what changed. He no longer approves a picture before live.
- **Anything that moves up, down, left or right should slide, not jump (said Oct 28).** Use `useSlide105(position)` with a `key` and the `gx-sl105` class, or follow the finger like 106 and 143.
- **Same spacing everywhere (said Oct 29, again Nov 1).** In tables, give every column a fixed width (no `1fr`) and `overflow: hidden` on sticky name cells, or long names push columns out of line (190). Rows side by side must line up no matter how long a name or stat line is: single lines with ellipsis instead of wrapping, fixed column widths, fixed row heights, and an empty placeholder when a line has no text.
- **The page behind a pop-up never scrolls (said Oct 29).** Change 149 does this for every overlay by itself; a new kind of pop-up only needs its class added to `SEL` in the 149 helper if it is not one of the listed classes or `fixed inset-0`.
- **Everything must fit inside its box on the phone (said Oct 29).** No sideways sliding of the whole pop-up, tiles fit the width (exception Kuvar likes: the simulate box Best day to add row slides sideways), tiles in even columns, and choices like More details are big full-width buttons, not small text links.
- **Live is his number one priority (said Oct 31).** Scores must keep changing by themselves on phone and laptop, never needing a refresh.
- **Every pop-up opens and closes with the smooth slide (said Nov 14, "set in stone for every change").** Anything that opens over the page (player, game, sheet, zoomed box) slides or grows in with the `cubic-bezier(.2,.8,.2,1)` motion the player screen and the NHL sheet use, closes by tapping outside it as well as the X, and puts him back exactly where he was (same page, same tab, same scroll). On the phone a pop-up is a sheet with a dark strip on top to tap. Nothing may just appear or jump.
- **Keep everything inside the app (said Nov 1).** No links or embeds that send him to NHL's site or app; rebuild the look in the app instead (184, 185).
- Never ask for ESPN cookies or API keys. They live in GitHub Secrets (ESPN_S2, SWID, NTFY_TOPIC, ODDS_API_KEY).

## 2. What the AI does at the start of a new session

1. **Get the code.** The repo is public: `dhaliwal32/23456789786634356`, branch `main`. In Claude Code you are already in it; run `git fetch && git reset --hard origin/main` first (syncs commit every few minutes).
2. **Check what's installed.** `changes/done/` holds every installed change file (from 070 on they are named just `70.py`, `71.py` and so on; from 091 on they keep their full name, e.g. `093-pickup-projection-pick.py`). The newest number there plus one is the next number; trust that over this doc if they differ.
3. **Quick health check.** Look at the last commit times; "sync ..." commits should come every 6 to 10 minutes. Also check `asof` in `ai/models/ai_proj.json` (should be under 36 hours old).
4. **Read the real code** around whatever you will change before writing anything. Never rewrite `fantasy-gm.html` from memory.

## 3. How a change works

Every app change is one Python file in `changes/`, run by `install.py`.

**Steps:**
1. Commit `changes/NNN-short-name.py` to `main`.
2. That commit starts **Install changes** in test mode. The run's summary links to `fantasy-gm-test.html`.
3. If it looks right: Actions → Install changes → Run workflow → **live**.
4. In the app, tap Refresh in Setup. On the phone, close and reopen.
5. If something is wrong after live: run Install changes with **undo**.

**The test page and build changes:** the test page only shows edits to `fantasy-gm.html`. Changes to other files, such as `build_app.js`, Python files or `lines-tab.js`, are checked in test but only applied in live.

### Change file template

```python
# changes/112-example.py - one line saying what this change does

NEW_CSS = r'''  /* change 112 (install.py) */
  .gx-example { color: var(--good); }
</style>'''

HELPERS = r'''// ---------- change 112: what this adds (install.py) ----------
function GxExample({ s }) {
  return <div className="gx-pn">...</div>;
}
'''

def change(t):
    t = lit(t, "112: styles", "</style>", NEW_CSS, "change 112 (install.py)")
    t = lit(t, "112: helpers", ROOT, HELPERS + ROOT, "change 112: what this adds")
    t = lit(t, "112: show it", "<exact old text>", "<exact new text>", "<a unique piece of the new text>")
    return t

edit(APP, change)
```

**Tools available inside a change file:**
- `lit(text, label, old, new, done_marker)`: replace exact text once.
- `block(text, label, start, end, new, done_marker)`: replace from the start line up to the end anchor.
- `sub_once`: the regex version of `lit`.
- `fail`: stop the run with a message.
- `py_ok`, `babel_ok`: syntax checks.
- `edit(file, fn)`: register edits to a file.
- `new_file(name, text)`: add a whole new page (can't make a new folder; keep new files at the repo root or in an existing folder).
- `APP` (= `fantasy-gm.html`) and `ROOT` (the `ReactDOM.createRoot(...)` line).
- `re`, `json`, `pathlib`.

**Rules:**
- Every `old` text must appear exactly once in the current file. Check with `grep -c -F '<text>' fantasy-gm.html`. If any edit misses, the whole run stops and nothing changes.
- The done marker must be a piece of the new text, so a re-run says "already done" instead of failing.
- There is exactly one `</style>`. New CSS goes before it; new helper code goes just before `ROOT`.
- New components and helpers get a `Gx` / `gx` prefix and a name that doesn't exist yet. Check with grep before using a name.
- Every React hook must run before any early return.
- Wrap rather than rewrite when you don't know a function's insides.
- Other files work the same way: `edit("gm_notify.py", fn)`, and so on. Python files are compiled before anything is written.
- The app's code has escapes like `"–"` written as six plain characters. A file-writing tool can turn these into a real dash when it saves a change file, so the anchor then misses. Keep anchors clear of them, or check the saved file for non-ASCII characters. Inside a plain (not `r'''`) Python string, write `\\u00b7` so the app gets the six characters. (177, 184, 201 all hit this; grep the saved file for non-ASCII before installing.)
- To replace a large stretch of code, a small helper in the change file can cut from an exact start text to an exact end text (138 and 184 use `cut`); `block` passes the new text through regex replacement, so backslashes in it get eaten.
- **Don't edit a change file after pushing it (199).** Once a change file is pushed, the live run may already have installed the first version and moved it to `changes/done/`; a second push of the same file then fails the test run. Make a new numbered change instead.
- A removal edit must run before an edit that adds the same done marker (244).
- Before choosing a number, `git fetch` and check `changes/` and `changes/done/` again; two sessions once both used 232 in the same minute.

## 4. Test before going live

1. **Install it on a copy:** copy the repo, put the change in `changes/`, run `python3 install.py live`. It must print "finished", not "STOPPED". Install Babel first (step 2) or the syntax check is skipped.
2. **Build the fast phone app:** install Babel 7 (`npm install --prefix <dir> @babel/standalone@7`), link it at `/tmp/babel/node_modules/@babel/standalone`, then run `node build_app.js`.
3. **Check the build:**
   - `grep -c '_defineProperty({}, ' build/app.js` must be 0.
   - There must be no `import` or `require("react` lines.
   - All three files in `build/` must parse with `new Function(...)`.
4. **Look at it** (render locally with Playwright):
   - Serve the copy with `python3 -m http.server`.
   - Answer the unpkg React requests with local `react@18.3.1` / `react-dom@18.3.1` UMD files.
   - Styles: serve the repo's own `build/tw.css` (216). If needed, answer `cdn.tailwindcss.com` with CSS built by `npx tailwindcss@3 --content build/*.js,fantasy-gm.html`, injected with `json.dumps` (not Python's `%r`).
   - Answer image requests with a plain stand-in picture (otherwise team codes show twice beside logos), and block everything else.
   - ESPN: for the NHL scores panel (131 on), answer `site.api.espn.com/.../scoreboard` and `summary?event=ID` with made-up games in ESPN's shape (events / competitions / competitors / status; summary header + plays with scoringPlay, participants scorer/assister) and tell Kuvar the games are made up.
   - For live points, the summary needs `boxscore.players[]` (team id, statistics groups forwards/defenses/goalies with `keys` such as goals, assists, plusMinus, shotsTotal, blockedShots, hits, penaltyMinutes, timeOnIce, and athletes with `shortName` like "P. Kane"). Make the numbers grow with each request and use `page.clock.install(time=...)` to set the day; read the Matchup score before and after a 45 s wait to prove it updates without a refresh (152).
   - Set the browser time zone to `America/Vancouver`.
   - Don't use `wait_for_function` to wait for the app; a plain 10-second wait works.
   - Screenshot at phone size (390 wide) and laptop size (1200 wide).
   - Navigate with hashes, e.g. `#league/players`, `#moves/trades`, `#myteam`, `#moves/goalies`. To open one team on Lines, run `window.__NAV.lines("COL")`. To open a player, run `window.__NAV.player({ id: "e5436" })`.
   - The Pickups simulate box opens from the player screen's Simulate button (151).
   - Watch for page errors and `console.error` lines: the player screen (095) catches its own errors and quietly shows the old pop-up instead.
   - If a feature only shows under certain conditions, make a picture-only copy with the condition loosened and tell Kuvar so.
   - Kuvar uses dark mode: run `window.__setTheme("dark")` after the page loads (176).
   - Don't stop the local server with `pkill -f "http.server"` (it kills the shell running the command). Start a second server on another port instead.
   - Goal Visualizer pictures (184, 185): use a real goal that has a file in `edge/` and a made-up ESPN summary with that goal's play. Phone: click `.gx-fb140`, the "Goal Tracker" tab, then `.gx-sh141 .gv163`; laptop: `.gx-sd141 .gv167`.
   - Goal button pictures (208): made-up goals must match real `edge/index.json` entries for the clock's day (team, period, time); add `videos[]` to the summary for the Video cases.
   - Player screen game card (201): the made-up scoreboard needs a game with the player's team (Josi e5436 is NSH); click `.gx-tg201`.
   - Matchup day picker and Summary (209): click `.gx-dp209 > .bt`, then the first `.gx-dp209 .rw`.
   - Tapping tabs (213): `locator.click()` scrolls the page, which hides scroll bugs. Put the tab in view inside the tab bar and tap with `page.mouse.click` at its centre.
   - Smoothness measurements: never use `page.clock.install` for frame timing (it fakes requestAnimationFrame and performance.now); fake only `Date`. Slow the processor 3x with CDP `Emulation.setCPUThrottlingRate`, measure freezes with a `longtask` PerformanceObserver.
   - Small code-only changes with nothing new to see can be checked by running the function in node.
5. **Password-locked data (156):** for local pictures, take plain data from git history (`git fetch --shallow-since=2026-10-31T09:00:00Z`, then `git show 00215b1:espn-data.js`), and answer the `gx-lock.js` request with `document.write('<script src="espn-data.js"><\/script>')` with the old espn-data.js in the served folder. Oct 31 2026 4 PM Pacific is epoch 1793487600. Never ask Kuvar for his password.

## 5. Going live from Claude Code

- `git fetch && git reset --hard origin/main` right before committing (the new change file is untracked, so it survives).
- Commit only the change file to `main` and push. That starts the test run.
- Start live: `gh workflow run install.yml -f mode=live`, or `gh api -X POST repos/dhaliwal32/23456789786634356/actions/workflows/install.yml/dispatches -f ref=main -f 'inputs[mode]=live'`.
- Check: `gh api "repos/dhaliwal32/23456789786634356/actions/workflows/install.yml/runs?per_page=1"` (list under `workflow_runs`). A sync commit can land between push and live, so check the marker in the file on origin.
- Workflows under `.github/workflows/` can't be edited by the install bot; commit those directly.
- After pushing a change to gm_live.py, cancel the running Live lead alerts run and start it again, or it keeps the old code until games end (206).

## 6. Things learned the hard way

- **Fast phone build (074, fixed in 076).** `build_app.js` compiles the app once on GitHub into `build/app.js`; phones load that, not Babel. Never add the `es2015` preset back (it broke `{ ...x, [k]: v }`). The build uses React "classic" output and refuses to write a build that needs `import` (Babel 8 safety). If the fast build fails, the page compiles in the browser. JSX comments are stripped from `build/app.js`; grep a function name to confirm a change reached the build. The build drops spaces (`SJ:"sj"`).
- **The syntax check is not a render test.** Always render it.
- **Weeks:** ESPN's `periods` are days, not weeks. Use the app's weeks (`s.weeks`, `deriveWeek`).
- **`SCHED[team]` is a Set of dates.** Spread it first: `[...SCHED[t]]`.
- **ESPN's player order is lost in the browser (152).** Use `E.dorder[date][team]` for anything shown "like ESPN".
- **Started means puck drop (152).** `gState` returns P while the live feed says pregame or 1st period 20:00 at 0-0.
- **Overscroll (152).** `overscroll-behavior: contain` only on the element that actually scrolls.
- **Ranks:** a player's rank is his place within his position by `effAvg(p, K) * (goalie ? start chance : 1)`. Team position ranks (`leagueTable(s).grpRank`) use the top 10 F, 5 D and 2 G healthy today.
- **Goalie numbers:** `effAvg` for a goalie is points if he starts. Trades and Pickups show points per team game, `gxPgAvg` = `effAvg` x `p.prob`.
- **Day projections (094):** `weekLive(..., { detail: true })` gives each day `proj` (original) while `act + total` is the updated one; started rows have `x0`.
- **Player screen (095):** `GxPdSafe` around `GxPlayerDetail`; old `lines-tab.js` pop-up is the fallback. Photos `a.espncdn.com/i/headshots/nhl/players/full/<ESPN id>.png`. Jersey numbers from `lines-data.js` `teams[T].no`. Stats summed from `box/` files.
- **Player faces (096, 097):** `GxFace({ p, t, size })`, square ESPN photo, size x `--gx-fs`. New player lists use `<GxFace p={p} size={22} />`. Don't put a face inside a text line that truncates; give it its own grid column.
- **Pickup rules (settings.json):** protect top N is 0, 16 players on "also protect", goalie minimum 3. Moves left from ESPN (`E.acq`), 3 per matchup.
- **Trades:** timed rosters (`myT`, `thT`) from `gxTimed` (081); other teams' trades run with `{ ...s, me: thatTeam, opp: null }` (078).
- **One projection (124):** `window.__PMODE` is always "combo"; `effAvg` calls `gxCombo124`; weights from `ai/combo.json`.
- **Live NHL scores:** the browser can't fetch the NHL API (no CORS). Since 132 every `api-web.nhle.com/v1/` call is answered from ESPN's open feed. Feed calls time out at 12 s (`__GXF152`); `G120.busy` clears after 20 s.
- **Stray change files:** a leftover file in `changes/` runs on every install. Keep only the one numbered file there.
- **Password lock (156):** only `espn-data.enc.js` is published. Other repo files (box/, ai/, lines-data.js, settings.json) are readable.
- **Inside the NHL scores panel (`GxNhl131`/`GxNhl141`)**, `.tm`, `.st`, `.gm`, `.hd`, `.nm`, `.pl`, `.tn` already have rules; new pieces need their own class names. Inside the Simulate box don't name a class `.pl`.
- **Applied moves:** Pickups' Apply here only changes `ft` in app state; the next sync resets it.
- **The app can't write to the repo**, except the settings sync (073).
- **Line data:** `gm_lines.py` reads Daily Faceoff; lines re-read every 2 hours (hourly 2 to 7 PM Pacific).
- **NHL pages can't be embedded (184)** (`frame-ancestors`). The cloud can't reach www.nhl.com.
- **Opening a game from anywhere (201):** use `gxOpen201(gameId)`.
- **Tabs (213):** `go` switches inside `React.startTransition`; code after a switch should not assume it is instant. Don't put `overflow-x: hidden` back on html or body (breaks the sticky phone tab bar).
- **Styles (216):** Tailwind is pre-built into `build/tw.css`. A class made by joining strings at run time would be missing; write class names out in full.
- **Speed caches:** `dayLabel`, `mdL`, `wkGames` cache (212); pickup win chances cached 2 min (`gxWinC215`); player screen waits 260 ms (`rd214`).
- **Outside links from the home screen app (211):** use `gxWatchGo211` as onClick so they open in real Safari.

## 7. Where things are in the app

Routing is `go(tab, sub)`, and the address bar mirrors it, e.g. `#moves/trades`.

| Tab | Route | What's there |
|---|---|---|
| Roster (first page) | `myteam` (`today` too) | Roster box (`GxBox230`: scoreboard, day strip, facts, spinning box Day / Win / Games / Players, best pickup), Back from IR card, Table / My team switch (239) |
| Matchup | `matchup` | Matchups strip, score, day picker (Summary or any day, 209), head to head, week totals, games left, NHL scores at the bottom |
| Players | `moves/adddrop`, `moves/allp`, `moves/goalies`, `moves/injuries` | Free agents / All players / Goalies / Injuries (219), Simulate box (107) |
| Trades | `moves/trades` | Trade builder, result tiles, More details (195) |
| Lines | `lines` | `GxLines111` locker room (233 to 251) |
| League | `league` | League table, matchups, playoff odds, Draft (197), Player rankings `league/players` |
| Setup | `setup` | Display (Favourite team, Watch link, My team view-as), Pickup rules, Phone alerts, AI Lab, Prediction history |
| Player screen | tap a name | `GxPlayerDetail` (095): Overview, Game log, News, Lines |

On the phone, Trades / League / Setup sit under a More button (241).

**Useful building blocks:**
- Players and teams: `s.players`, `s.me`, `p.ft` (team id or `"fa"`), `PN`, `TL`, `TeamLogo`, `teamName`, `GxFtPic114`.
- Projections and weeks: `effAvg`, `gStart`, `avail`, `weekLive`, `winProb`, `winChance(s, roster)`, `leagueTable(s)`, `deriveWeek`, `oppOf`, `nextWkS(s)`.
- Moves: `computeMoves(s, { H, pos })`, `afterMove(s, add, drop)`, `movesLeft`, `planS`.
- Box scores: `gxBoxIdx()`, `gxBoxDay(date)`, `gxEst(line, scoring)`, `pStat(p, date)`.
- Today's NHL games: `window.__NHLNOW.games`, `gxGame201(team)`, `gxOpen201(id)`.
- Week points per player: `gxSum209(s, teamId, weekLive result)`.
- Formatting: `f1`, `ordN`, `wpTxt`, `nrm`, `M_ST`.
- Saved on the device: `uiGet()` / `uiSet(key, value)`.
- CSS: `gx-pn` (panel), `gx-tag`, `gx-row`, `gx-lk`, `gx-seg`, `gx-stg` / `gx-stc` / `gx-stv`, `gx-pd-*`, `m-hide` / `m-only` / `m-inl`.
- Colours: `--ink`, `--mute`, `--line`, `--accent`, `--good`, `--bad`, `--warn`.

## 8. Change log

The full row-by-row log for 068 to 251 (with every helper name and marker) is in Kuvar's claude.ai Fantasy GM project doc of the same name, and each installed change file in `changes/done/` starts with a one-line summary and contains the exact code. For any past change, read its file in `changes/done/`.

Recent rows (add new ones here):

| # | What |
|---|---|
| 270 to 274 | Player Talk (Reddit) tab added then removed; see `docs/notes/changes-270-to-274.md` |
| 275 | Setup cleaned up (Kuvar, Nov 14: "a lot of information in there, most isn't being used"). Main Setup page is now short: App (My team, Favourite team, Watch link inline), Alerts and lineup (Phone alerts, Lineup autopilot, Protected players = the old Pickup rules page), AI (AI Lab, Prediction history), then one More row. `#setup/more` holds Theme, Injury return dates, Edit players, News, Betting lines, Schedule, Data and backup. Nothing was deleted; old `#setup/display`, `players`, `league` pages still open by hash. Class `gx-st275` |
| 276 | Roster box: Game plan card above Best pickup (`GxPlan276`, worker `gxPlan276(s, w, today)`). One sentence on where the matchup stands, then for today (or the next day with games once today's have started) who starts over who when more players have a game than there are spots: each player who sits is paired with the weakest starter he could replace. Yellow dot = ESPN's lineup has them the other way round (`actDay` slots; 7 = bench). Also lists goalies not confirmed. Uses `liveNudges` so its numbers match the Day side. Classes `gp276`, `dd276` (don't use `.dy` inside the box, it is taken) |
| 277 | Cleaner look (Kuvar, Nov 14: wants it smooth like Apple's apps). CSS only: every `.gx-pn` card has rounded corners (16px, 14px on the phone, none when `.full`), `.gx-seg` and `.gx-seg103` switches are soft grey sliders (`--seg277`), tap highlight off |
| 278 | Alerts from the app itself (web push), next to ntfy, which still runs. App: `GxPush278` card at the top of Setup > Phone alerts (Turn on, Send a test, Turn off); `sw.js` shows the alert and tells the open app which page to show (`gxGo278` message, `#myteam` for lineup alerts, `#matchup` for lead changes); `manifest.webmanifest` linked in the head. Devices are saved in `push_subs.json` through the GitHub key from Sync between devices (so that must be on for the device). Server: `gm_push.py` (only needs `cryptography`; pywebpush would not install) encrypts per RFC 8291 and signs with a key worked out from the SWID and NTFY_TOPIC secrets, so no new secret; the public half is `push_key.json`, written by gm_notify.py on every sync. Hooks in gm_notify.py (first `push`) and gm_live.py. `push-test.yml` sends a test (the Send a test button starts it). Not yet proven on Kuvar's iPhone: the test browser cannot receive real pushes, so only the sending maths, the switch and tap-to-open were tested. If the iPhone says alerts are not possible, the home screen icon has to be deleted and added again so it picks up the manifest |
| 279 | Tap a game before it starts: full preview instead of "Not started yet" (Kuvar, Nov 14, wanted what ESPN's game page shows). `GxPre279` on the GAME tab reads ESPN's summary (`gxSum132`, refreshed each minute): records, goalies (app's own `__GOALIES`), line, total, where, TV, season series, scoring leaders, team stats side by side with the better side in bold, injuries with return dates, last 5. `GxPreTab279` on FANTASY (your and their players in the game with projections, best 6 free agents) and on the team tabs (every player's GP, FPTS, AVG, tonight's projection, owner tag). ESPN athlete id = app id without the "e" (`pby()["e" + id]`). Real pregame summary keys: boxscore.teams[].statistics, leaders, injuries, lastFiveGames, seasonseries, pickcenter, gameInfo.venue, broadcasts, standings, goalies |
| 280 | Game plan moved inside the Win side of the Roster box (Kuvar, Nov 14), under the win numbers; the card on the left is gone. `GxPlan276` takes `inWin` (class `in280`): no card border and no sentence, because the Win side already says it. The Win side scrolls inside the box when the list is long |
| 281 | Tapping a player inside the NHL game sheet opens him on top of the game instead of closing it (Kuvar, Nov 14: closing him must put you back where you were). `go` in `GxNhl141` no longer calls `close`; it adds `gx-pt281` to `<html>`, which lifts `.gx-pd-ov` to z-index 80 (the sheet is 75); a `gx-game201` event takes the class off again so a game opened from the player screen still comes out on top. App alerts: proven on Kuvar's iPhone on Nov 14 (Apple accepted the test). His GitHub key may save files but not start jobs (403), so Send a test now saves `push_test.json` (`gxPushPing281`) and `push-test.yml` runs on that push |
| 282 | Phone alerts: every alert has a real switch (`GxSw282`) tapped in the app; the GitHub link and the Master switches block are gone. `gxAlSave282(patch)` saves `alert_prefs.json` through the device's GitHub key; `gxAlPatch282` also turns a switched-off group back on while keeping its other alerts off. Taps show at once (`ov282`) and flip back with a message if saving fails. Phone buttons get a forced min-height, so small controls need `min-height ... !important` |
| 283 | Live game view tidied (Kuvar, Nov 14, before any game had started): only the rink stays pinned while scrolling (pressure bar and current play moved into `.un283`), rink max 560px wide on the laptop, and `GxGmStats283` adds a Team stats card (shots, faceoff %, hits, blocks, takeaways, giveaways, power play, PIM) under Scoring for live and finished games. Tested by replaying a real finished game (NSH at VGK, Nov 13) as live: `live.js` in the session scratchpad cut ESPN's summary to the first N plays, set the status to in progress and grew N on each request. Not yet seen on a truly live game |
| 284 | Three things. (1) Roster box sides would not scroll with a finger on the iPhone: WebKit does not scroll inside a 3D-turned element, so once the box stops turning the facing side lies flat (`.pr.rs284`, front face `.fr284`, other faces hidden) and a sideways drag or a turn stands it up again from `el.__rest284` (animation checked frame by frame against the old one). Every side but Graph scrolls. Could only be tested in Chromium; needs Kuvar's word that it scrolls on the phone. (2) Phone player screen is a sheet: 52px dark strip on top, grab bar, tap the strip to close. (3) ntfy is off (Kuvar confirmed the app alert arrived): `NTFY_ON = False` in gm_notify.py, an early `return` in gm_live.py `push`, sync-watch.yml sends through gm_push. The NTFY_TOPIC secret must stay: the app alert key is worked out from it |
| (no number) | `.github/workflows/sync-watch.yml`: every 30 minutes, one ntfy alert when the newest "sync" commit is 50 to 80 minutes old, and again at 6 hours |

## 9. Open ideas Kuvar has not chosen yet

- A "Do this now" card on Roster: the single best move right now, or "Lineup is set".
- A phone alert when the sync breaks or ESPN refuses access.
- A lineup check that warns when a bench player is projected above a starter tonight.
- A move tracker: points a pickup scored compared with the player dropped.
- An all-play record on League.
- A player trend chart in the player screen.
- Stop the page loading the uncompiled `lines-tab.js` and `ask-panel.js` copies when the fast build is in use.
- Alerts `injuries` and `starter_is_out` are off in `alert_prefs.json`; he may want them back.
- Autopilot is ON since Oct 21. Later: auto pickups once lineup mode proves itself.
- AI accuracy list (Oct 28): already tested and no help: expected goals, schedule extras, PP/line labels, starting goalie quality, model mixes, bigger AI, scratch prediction, one season of odds. Claude's picks to try: power play time trend, re-project after morning skate lines, opponent penalties, weekly win chance with teammates scoring together, live projection for time left in a game.
- Cloud sessions: the `fantasy-gm` environment allows `site.api.espn.com`, so real ESPN feeds can be fetched with curl for tests (the test browser still needs them handed to it with `route.fulfill`).
- Lock screen live scores (iPhone Live Activity) need a real iPhone app; Kuvar said not now.
- Watch link codes (`GX_NHL175`): LA la, NJ nj, SJ sj, TB tb, UTAH uta.
- 201 follow-up: past games in the game log don't open a game view yet.
- 209 follow-up: Summary could add a week stat line (G, A, SOG).
- 211 follow-up: if Watch still opens inside the home screen app, his iPhone may be older than iOS 17.
- Don't bring back Player Talk / Reddit or 3D models unless he asks.
