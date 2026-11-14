# Fantasy Islands GM: handoff for a new AI

Written Nov 9, 2026, by Claude. What Kuvar likes, what he rejected and why, ideas already given, and fresh ideas. (Change numbers here are as of Nov 9; see `changes/done/` for the newest.)

## 1. What the app is

- A personal ESPN NHL fantasy hockey helper for one league (10 teams, H2H points, weekly matchups). Kuvar's team is "kanucks".
- A single web page: `fantasy-gm.html` (React 18, about 600 KB), on GitHub Pages: dhaliwal32.github.io/23456789786634356/fantasy-gm.html.
- Data comes from a GitHub Actions sync every 6 to 10 minutes: ESPN league data (scrambled behind a password, `espn-data.enc.js`), NHL lines from Daily Faceoff (`lines-data.js`), box scores (`box/`), an AI projection model (`ai/`). Live scores in the browser come from ESPN's open scoreboard and game summary feeds, every 2 seconds while games are live.
- Kuvar uses it on an iPhone home-screen app and in Firefox on a laptop, always in dark mode.
- Every change is one numbered Python file in `changes/`, run by `install.py`. `build_app.js` then compiles the page to `build/app.js` for phones. Full process in `docs/how-to-make-a-change.md`.
- Never ask Kuvar for ESPN cookies or API keys; they are in GitHub Secrets.

## 2. How Kuvar wants to work

- He is not a programmer. Plain words, short answers, no jargon, no emojis.
- Make the change live right away and show him a picture after. Don't ask for approval first.
- Test every change at phone size (390 wide) and laptop size, in dark mode, before going live.
- Always show him any email and confirm before sending anything.

## 3. What he likes (keep these)

- Live above everything. Scores that update on their own, no refresh, on phone and laptop.
- Everything inside the app. No links out to NHL or ESPN pages; rebuild their look in the app.
- ESPN app look for Matchup, player screen, NHL scores sheet and goal tracker.
- Smooth motion. Anything that moves slides; nothing jumps.
- Tidy and even. Same spacing, same photo sizes, rows lined up, nothing cut off, everything fits on the phone.
- Plain colours on numbers. Scores the same grey as stats, white only while live. Not lots of green and red.
- The Roster page box (230): his scoreboard on top beside a square box you spin by dragging (Day, Win, Games, Players), plus a "best pickup now" card. He wants this to do much more.
- Lines page as a locker room (233 to 237, 246 to 251): jersey backs in stalls with his own stall pictures, team colours, spotlights on players he can pick up, every team's logo at the top.
- His own team as a locker room (238, 239): Roster page Table / My team switch.
- Goal Visualizer, goal video clips, who was on the ice, power-play tags, intermission countdown.

## 4. What he rejected, and why

- 3D player models (Three.js, Meshy). Twisted hands, low detail, choppy. He said "no more 3D models".
- 3D arena, 3D mockups, 3D jumbotron in the Roster box: "looks horrible", removed. Unused files still in the repo (`vendor/gx3d-*.js`, `models3d/`, `proto3d/`).
- The first Roster box: colours and fonts didn't match the app. New parts must use the app's own colours (`--ink`, `--mute`, `--line`, `--accent`, `--good`, `--bad`) and fonts.
- Flat drawn players on a rink for Lines: thin and cheap.
- First jersey drawing: no texture, names cut off, borders.
- Repeated information (win chance shown twice). Each fact once.
- Lesson: he wants premium and polished, not "cool but rough". Simpler and polished beats ambitious and rough.
- Player Talk / Reddit (270 to 274): removed; don't bring back unless he asks.

## 5. Still open

- A Roster box with "full freedom": how his matchup is going, what to do to win, shows everything, looks amazing. The main open request.
- Older ideas he hasn't picked are at the end of `docs/how-to-make-a-change.md`.

## 6. Ideas already given (Nov 9)

Lines: stall flashes when a player scores; tonight's game tag on each stall; hot and cold marks (done as nameplates, 250/251).
Roster: "Do this now" card; player of the night.
Matchup: live momentum tug-of-war bar; goal pop-up banner.
Players: trend chart tab on the player screen; pickup tracker.
League: all-play record.
Roster box: broadcast-style game-night screen with a points ticker; win chance timeline; coach's board with ordered actions; versus fight card; what-if sliders; glowing day tiles; danger alerts with the fix; season story side.

## 7. Fresh ideas for the Roster box

1. One "state of the matchup" sentence at the top, refreshed every few minutes, e.g. "You lead by 12. They have 9 more games left, so you're projected to lose by 4. Add a D with 3 games to flip it."
2. Games-left race: two tracks of game pips (played, live, to come).
3. Tonight panel: every player on both sides playing tonight, by start time, with live points.
4. Swing players: the 3 on each side whose nights matter most.
5. Path to win: points needed per remaining lineup game against what his players average, with the one move that closes the gap.
6. Opponent scouting: their hot players, goalie situation, empty spots, extra-game days.
7. Week replay: scrub across the week and the scoreboard animates.
8. In-app alert banner when win chance moves 5%+, a goalie is confirmed, or a player is scratched.

Keep each one as a side of the box or one tidy card, test on the phone first, match the app's look.
