# changes/069-remove-old-pages.py - removes old pages and helpers the app no longer shows
MARK = "// change 069: old unused pages removed"
APP_END = 'ReactDOM.createRoot(document.getElementById("root")).render(<App />);'

CUTS = [
    ("old ice-time movers", "function ToiMovers({ s }) {", "// ---------- move engine ----------"),
    ("old Advice page", "// ---------- Advice ----------", "function NewsView({ s, wk }) {"),
    ("old PP1 pages", "// ---------- PP1 ----------", "// ---------- Betting lines ----------"),
    ("old Planner, Edges and Bench fixer", "function AcqPlanner({ s: s0, setS, wk: wk0 }) {", "// ---------- Playoff planner ----------"),
    ("old 2-for-1 builder", "// ---------- 2-for-1 builder ----------", "// ---------- Trade analyzer ----------"),
    ("old Trade analyzer and matchup cards", "function TradeAnalyzer({ s, initPartner }) {", "function Matchup({ s, setS, wk, setWk }) {"),
    ("old Power rankings and League page", "// ---------- Power rankings ----------", "// ---------- Add / Drop ----------"),
    ("old Add / Drop page", "const WinCell = ({ s, add, drop, base }) => {", "function MoveSim("),
    ("old other-team rosters", "function OppRosters(props) {", "function RosterTable({ s, setS, wk, team }) {"),
    ("old strategy and lineup helpers", "const strategy = (p) =>", "function GoalieStreams({ s, setS, wk }) {"),
    ("old phone matchup layout", "function MSide({ p, right }) {", "// ---------- round 10: one trade builder"),
    ("old trade rank box", "// ---------- round 30: league ranks before and after a trade", "// ---------- round 32: theme switch"),
    ("old Next 7 days and league boxes", "function GxNext7({ s }) {", "function GxCarry({ s, wk }) {"),
    ("old games box", "// ---------- round 34: lineup games for each day of this matchup", "// ---------- round 37: Team sub-pages"),
    ("old alert box and week arrows", "function GxAlertPrefs() {", "// ---------- round 61: any week on two Today boxes"),
]

GONE = ["ToiMovers", "verdict", "advDot", "KeepLegend", "AdvMove", "AdvicePanel", "ppKey", "ppData",
        "rankCls", "AvailPP", "PPView", "AcqPlanner", "EdgesPanel", "BenchFixer", "TwoForOne",
        "TradeAnalyzer", "LiveBar", "Side", "MatchCard", "PowerRankings", "ClimbPanel", "League",
        "WinCell", "AddDrop", "OppRosters", "strategy", "StrategyLine", "FillSlot", "espnLineupChecks",
        "startTag", "MSide", "H2H", "TradeRanks", "GxNext7", "GxLeague", "GxGames", "GxAlertPrefs",
        "gxSpan60", "gxNextWk60", "gxWkTouch", "GxWkSw", "GxGamesWk", "GxLeagueWk"]


def cut(t, label, start, end):
    if t.count(start) != 1:
        fail("069: the start of '" + label + "' was found " + str(t.count(start)) + " times, expected once.")
    if t.count(end) != 1:
        fail("069: the end of '" + label + "' was found " + str(t.count(end)) + " times, expected once.")
    a = t.index(start)
    b = t.index(end)
    if b <= a:
        fail("069: the end of '" + label + "' comes before its start.")
    print("069: removing " + label + " (" + str(b - a) + " characters)")
    return t[:a] + t[b:]


def code_only(t):
    t = re.sub(r"/\*.*?\*/", "", t, flags=re.S)
    return re.sub(r"(?<![:\\])//[^\n]*", "", t)


def change(t):
    if MARK in t:
        print("069: already done")
        return t
    n0 = len(t)
    for label, start, end in CUTS:
        t = cut(t, label, start, end)
    code = code_only(t)
    for name in GONE:
        for pat in (r"<" + name + r"[\s/>]", r"(?<![\w$.])" + name + r"\s*\("):
            if re.search(pat, code):
                fail("069: '" + name + "' is still used somewhere, so nothing was changed.")
    if t.count(APP_END) != 1:
        fail("069: could not find the last line of the app.")
    t = t.replace(APP_END, MARK + "\n" + APP_END, 1)
    for must in ("function Today(", "function App(", "function SetupPage(", "function Pickups(", "function TradeBuilder(", "function PlanPage("):
        if must not in t:
            fail("fantasy-gm.html looks damaged after change 069 (" + must + ").")
    print("069: removed " + str(n0 - len(t)) + " characters in total, file is now " + str(len(t)) + " characters")
    return t


edit(APP, change)
