# Changes 270 to 274 (all live Nov 14, 2026)

These rows are not yet in the change log of `docs/how-to-make-a-change.md`. Merge them in, set "Next change number" to 275, then delete this file. Changes 252 to 269 are also missing from that log; each one's first line in `changes/done/` says what it did.

| 270 | Player Talk tab (Kuvar, Nov 14: Reddit is "the main thing"; no paid AI). Reddit refuses GitHub's servers (403/429) and sends no CORS header, but answers his Mac. So `talk_mac.py` (repo root, Python standard library only) runs on his Mac every 3 hours via launchd (`~/Library/LaunchAgents/com.fantasyislands.talk.plist`, folder `~/FantasyTalk`, log `~/FantasyTalk/log.txt`), reading team subreddits, r/fantasyhockey, r/hockey and the Daily Discussion, and uploads `talk/raw/<sub>.json` plus `talk/raw/_meta.json` in one commit via the Git Data API with a fine-grained GitHub key from the Mac Keychain (service `fantasy-gm-talk`, account `talk`). App: `GxTalk270({ p, s })` = Talk tab in the player screen. gm_notify.py no longer runs gm_talk.py. Install note: `new_file` can't make a new folder; keep new files at the repo root or in an existing folder |
| 271 | talk_mac.py slower after 429s: 7 s between requests (`GAP_S`), retries on 429, gives up after 4 failures in a row; team subreddits comments only |
| 272 | talk_mac.py fetches Reddit with macOS `curl` (Reddit blocked Python's urllib with 429 even when slow, but curl got 200) |
| 273 | talk_mac.py asks Reddit the plain way: User-Agent `FantasyIslandsGM/1.0`, no `limit=`, no Accept header; timer every hour |
| 274 | Talk tab removed (Kuvar, Nov 14: "no more talk"). Reddit allowed only a trickle without an app key, and new Reddit app keys need review. Player screen tabs back to Overview, Game log, News, Lines (`/* 274: Talk tab removed */`); `GxTalk270` and other 270 helpers stay in the file unused; gm_talk.py and talk_mac.py stay in the repo unused. Kuvar was given Terminal steps to stop the Mac timer and remove the Keychain key and ~/FantasyTalk |

Don't bring Player Talk / Reddit back unless Kuvar asks. If he does, the only reliable route is an approved Reddit app key (OAuth), not RSS.
