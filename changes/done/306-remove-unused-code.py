# changes/306-remove-unused-code.py - takes out 85 old parts of the app that nothing uses any more (old Roster boxes, 3D scoreboard, jerseys, locker room, Talk, old pages); about 159 KB smaller, nothing you see changes
import hashlib

# name, how the part starts, its length, and a fingerprint of the exact text, so only that exact old code is removed
GONE = [
[
"toiOf",
"const toiOf = (p) => sigOf(p).toi || null;",
42,
"1805cc75bbb4a64766610148c6ce9d19"
],
[
"SectionShut",
"const SectionShut = (p) => <Section {...p} closed />;",
53,
"7dbc1127d94164ada708de3b05bc0e22"
],
[
"DayFold",
"const DayFold = ({ id, open0, head, right, children }) => {",
932,
"ff53ec02f47c7f07bc43a51057d09f3b"
],
[
"oddsFor",
"const oddsFor = (t, dt) => { const O = ((window.ESPN_DATA || {}).model || {}).odds || {}; return dt && O[dt] ? O[dt][t] || null : null; };",
138,
"8ac0bb98baab122adbc1b863c8e06ed2"
],
[
"MoveSim",
"function MoveSim({ s, setS, wk, M, H, hLabel, init, wBase, onClose }) {",
11976,
"8a00d8118745f1a75d434a338c07d647"
],
[
"RosterTable",
"function RosterTable({ s, setS, wk, team }) {",
3475,
"78ef2ed8d2653c70153f364695635bd1"
],
[
"WinDelta",
"const WinDelta = ({ s, add, drop, base }) => {",
486,
"631bfdaac72af0be0033fe3dd98edf74"
],
[
"movesUsedESPN",
"function movesUsedESPN(s, w) {",
221,
"a8c98b21045e940d7ddc4ac711ba7d9f"
],
[
"MobileHeader",
"function MobileHeader({ s, setS, tab, go, ageH }) {",
3238,
"e955f99e04f351cdb517976b07026972"
],
[
"Dlt",
"const Dlt = ({ v }) => <span className={\"font-semibold \" + (v >= 0 ? \"text-green-700\" : \"text-red-600\")}>{v >= 0 ? \"+\" : \"\"}{f1(v)}</span>;",
139,
"3908805908f09fb82aee400f9ca04baf"
],
[
"MyInjProt",
"function MyInjProt({ s, setS, wk }) {",
5169,
"b8aac7dcac46a0e2b59eb342afda38f9"
],
[
"PickNote",
"const PickNote = () => { const a = pickStart(null); return a === todayISO() ? null : <div className=\"w-full text-xs text-amber-600 mt-1\">Today's first game has ",
296,
"dacfebc569880439a0a9748514fc30ce"
],
[
"PlanWin",
"const PlanWin = ({ a, b }) => {",
423,
"afc549d7f66d5c1e69a538a72df54a73"
],
[
"planNote",
"const planNote = (sP) => { const w = sP.weeks[sP.wk] || {}, d = (w.dates || [])[0]; return \"No moves left this week. These are for \" + (w.label || \"next week\") ",
226,
"c8cbc035d3e127479c49c184a7026998"
],
[
"PlanNote",
"const PlanNote = ({ sP }) => <div className=\"w-full text-xs text-amber-600 mt-1 mb-1\">{planNote(sP)}</div>;",
107,
"6f2cf0bd7de4dfe1263f8a218a49f4ee"
],
[
"MyForm",
"function MyForm({ s }) {",
1277,
"a58610c6c68261ead5b4f8ea8cee2687"
],
[
"TradeAdvice",
"function TradeAdvice({ s, onPick }) {",
2757,
"efcd8fabbc690480257eccc6fa8a2f26"
],
[
"ThemeBtn",
"const ThemeBtn = ({ cls }) => {",
413,
"7106382292b8b164f10f72451d49e9ea"
],
[
"GxWeek",
"function GxWeek({ wk, A, B, aA, aB }) {",
4951,
"a4403b87b4ea3a790fb8b8d171cb5eec"
],
[
"SubBar",
"function SubBar({ tab, sub, go, setSubs, nav, s, wk }) {",
1935,
"6c7666429fc41088f45e8d9af196c5b6"
],
[
"gxHsKey",
"const gxHsKey = (s) => \"hs83:\" + (((s.weeks || [])[s.wk] || {}).label || s.wk);",
79,
"dde738e03b4f5612b5001c4c52a0e397"
],
[
"gxHsMode",
"const gxHsMode = (s) => { const v = uiGet()[gxHsKey(s)]; return v === \"on\" ? \"on\" : v === \"off\" || v === true ? \"off\" : \"\"; };",
126,
"2cd0c2365dc61561a30091738ed149a6"
],
[
"gxHsAuto",
"const gxHsAuto = (base) => base != null && (base >= GX_HS_SURE || base <= 1 - GX_HS_SURE);",
90,
"43105a5dd115dee7fad7bd389c216059"
],
[
"gxHsOff",
"const gxHsOff = (s) => gxHsMode(s) === \"off\";",
45,
"27e0743c6af034c006989f96f2175d79"
],
[
"gxHsSet",
"const gxHsSet = (s, v) => { uiSet(gxHsKey(s), v); window.dispatchEvent(new Event(\"gx-hs83\")); };",
96,
"23fa6b34bf0117790555c014df2666df"
],
[
"gxHsCan",
"const gxHsCan = (s, base, ml) => !!nextWkS(s) && ml > 0 && base != null;",
72,
"23367658d3e88f99cf39e47ecdef44d2"
],
[
"gxHsOn",
"const gxHsOn = (s, base, ml) => gxHsCan(s, base, ml) && (gxHsMode(s) === \"on\" || (gxHsMode(s) === \"\" && gxHsAuto(base)));",
121,
"073a6b9348a7ebc7f1c1991ea510e59a"
],
[
"gxUseHs",
"function gxUseHs() {",
225,
"4e2ae973bc97b378959aa089d5d1edbb"
],
[
"GxHsLine",
"function GxHsLine({ s, base, ml }) {",
840,
"ed7a7b8477a64783d5643443083422c6"
],
[
"GxHeadStart",
"function GxHeadStart({ s, base, ml }) {",
2745,
"d6beebdc508897d88a3a918df1eb871b"
],
[
"gxIjDays",
"const gxIjDays = (d) => Math.round((fromIso(d) - fromIso(todayISO())) / 864e5);",
79,
"c6b874512b748dd3b5a504d5751407fb"
],
[
"gxIjWhen",
"const gxIjWhen = (d) => { const n = gxIjDays(d); return n < 0 ? \"any day now\" : n === 0 ? \"today\" : n === 1 ? \"tomorrow\" : \"in \" + n + \" days\"; };",
146,
"02baaac10c0eb3e6ab6260defcd1dc2c"
],
[
"gxIjAgo",
"const gxIjAgo = (d) => { const n = -gxIjDays(d); return n <= 0 ? \"today\" : n === 1 ? \"yesterday\" : mdL(d); };",
109,
"da3964f588509007f724d2e77627b8ad"
],
[
"gxIjNote",
"const gxIjNote = (n) => (n && n.length > 15 ? n : \"\");",
54,
"890851f98c2ed71ba75df2a788030e69"
],
[
"GxInjPage",
"function GxInjPage({ s }) {",
6445,
"9a3a84a3289d27d4d71e7250841478a5"
],
[
"GxAutoToday",
"function GxAutoToday({ go }) {",
1407,
"27e4e554d165caedf368d933641703d8"
],
[
"gxApSave",
"const gxApSave = (patch) => {",
1447,
"45118408a9023ae8ba934c68a7bbece3"
],
[
"GxAutoPage2",
"function GxAutoPage2({ s, go }) {",
5247,
"d8e2c2eb3e298c764392d4b6c7d1df84"
],
[
"gxStats99",
"function gxStats99(p) {",
438,
"cea3bec00c6a698628ce277197ac5ae5"
],
[
"gxAgg100",
"function gxAgg100(list, isG, sc) {",
911,
"223d342d995172c448144860e0fb360e"
],
[
"GxSC100",
"function GxSC100({ p, s }) {",
447,
"6fa9396be6a4c6aab9735f4287f2622e"
],
[
"GxSH100",
"function GxSH100() {",
157,
"e14ef538b100fc5a0324fb4026d40b22"
],
[
"GxMuMore103",
"function GxMuMore103({ s, wk }) {",
459,
"fc7b9ab55701d25165cbd940971009d8"
],
[
"GxSC104",
"function GxSC104({ p, s }) {",
635,
"047324150f70bdd74703c789bdc1eeee"
],
[
"GxSH104",
"function GxSH104({ g }) {",
184,
"2c0ccc03672bdc9036764606965fca9f"
],
[
"GxBL104",
"function GxBL104({ s, p, r, onPick }) {",
549,
"82d2b6100bfeabadd701b39d0d88778b"
],
[
"GxRinkLines111",
"function GxRinkLines111({ teamCode }) {",
1220,
"c4c4663805c282daf4b03179f387b19a"
],
[
"GxBox118",
"function GxBox118({ p }) {",
1874,
"a61961f006ba7a63f2dabbbbe706280f"
],
[
"GxNhl131",
"function GxNhl131({ s, opp }) {",
13035,
"36d8e9e99dd7ead4356705a95b0bd705"
],
[
"gxIntFmt159",
"const gxIntFmt159 = (sec) => String(Math.floor(sec / 60)).padStart(2, \"0\") + \":\" + String(sec % 60).padStart(2, \"0\");",
117,
"f39e76ebdeff1e622ea2da05f3030d08"
],
[
"gxRinkBg165",
"function gxRinkBg165() {",
1246,
"72f1f692d6a69fe5f9d404c8517231e9"
],
[
"gxPair169",
"function gxPair169(a, b) {",
510,
"0fd8b95b39d3fad447c610593a19cb3a"
],
[
"gxCol169",
"const gxCol169 = (c, txt) => (txt ? { fill: c.t, fontWeight: 700 } : { fill: c.f, stroke: c.s, strokeWidth: c.f === \"#ffffff\" ? 0.9 : 0.5 });",
141,
"2b2db085b145b11d49c5b4bbb2895a3f"
],
[
"gxLogo184",
"const gxLogo184 = (t) => \"https://assets.nhle.com/logos/nhl/svg/\" + (NHL_LOGO[gxAb131(t)] || gxAb131(t)) + \"_light.svg\";",
120,
"24d4ad22d69dccc29f1b4594664ae7b6"
],
[
"GxSkater224",
"function GxSkater224({ t, name, no, side, goalie, className }) {",
5057,
"6ef630d72767b5a41d0f9b46ad1943eb"
],
[
"GxBox225",
"function GxBox225({ s, wk }) {",
15360,
"a4911d8a2ae03d4c736865aad93fdead"
],
[
"GxBox226",
"function GxBox226({ s, wk }) {",
22798,
"8af1d8c16a6596b33c7dc5d9f4761c1b"
],
[
"gxLoad228",
"function gxLoad228() {",
497,
"4e15ccb129e56b88a36e3f46677fcc2e"
],
[
"GxJumbo228",
"function GxJumbo228({ J, k, setK, onTap, fb }) {",
1305,
"3d79e3c938d880e4c57ee987746e286c"
],
[
"GxJersey231",
"function GxJersey231({ t, name, no, goalie }) {",
2722,
"8418cec43042d2ddd8f80b3067a21ff1"
],
[
"gxLum232",
"function gxLum232(hex) { const h = String(hex || \"#777\").replace(\"#\", \"\"); const v = parseInt(h.length === 3 ? h.split(\"\").map((x) => x + x).join(\"\") : h, 16); ",
242,
"db4b1035ce9b25604499e1785caa883e"
],
[
"GxJersey232",
"function GxJersey232({ t, name, no, goalie }) {",
7448,
"3989fb23d6fbd3422c6d2bde2906eb72"
],
[
"gxRoom236",
"function gxRoom236(t) {",
567,
"9cda8768a5b06815033cf07b7f0ce0f0"
],
[
"GxRoom236",
"function GxRoom236({ t }) {",
390,
"fc59e4d23dafbc1cb881b08869ff3fdf"
],
[
"gxNo238",
"function gxNo238(p) {",
248,
"5b10bd332d5f9b5d4cce4cbc12c26796"
],
[
"gxTn238",
"function gxTn238(p) {",
485,
"196f3a3d7934d563f4df72213630acb8"
],
[
"GxMyRoom238",
"function GxMyRoom238({ s }) {",
2309,
"ad25c282edd9cb8904ebad035f3be31a"
],
[
"GxMore241",
"function GxMore241({ tab, go }) {",
1545,
"370bbe7b9fb1352d2ecc4c8afff3a50f"
],
[
"GxIrBack244",
"function GxIrBack244({ s }) {",
5704,
"fac021832fd805ae2a8ce9513e6f3cdc"
],
[
"gxSt246c",
"const gxSt246c = (t) => (GX_ST246.has(String(t || \"\").toUpperCase()) ? \" st246\" : \"\");",
86,
"93169cc741b88fa7e9bcf56b1c0477c7"
],
[
"gxSt246s",
"const gxSt246s = (t) => { const T = String(t || \"\").toUpperCase(); return GX_ST246.has(T) ? { \"--st\": \"url(stalls/\" + T + \".jpg?v=1)\" } : undefined; };",
151,
"dcbe3842aa89f689168e389369ea3959"
],
[
"gxCup248",
"function gxCup248(x, y, h, k) {",
892,
"04fa774d810b3793a7111a8247c30426"
],
[
"gxWeb248",
"function gxWeb248(cx, cy, r, ang0, k) {",
788,
"479b4ef5f5b15e40edbd810ee7eadef2"
],
[
"gxSpider248",
"function gxSpider248(x, y, top, s, k) {",
902,
"5446edfce68d8ebed1fc26e66ebe2dbf"
],
[
"GxHC248",
"function GxHC248({ k }) {",
894,
"35701be586c23074108a6584d48cf1b5"
],
[
"GxClk265",
"function GxClk265({ id, per, clk }) {",
977,
"395fd1a6256093dd4d3961105c0c1201"
],
[
"gxTkLoad270",
"function gxTkLoad270(name) {",
316,
"07eb9ca27e634731362026483d1a9a1b"
],
[
"gxTkN270",
"const gxTkN270 = (s) => String(s || \"\").normalize(\"NFKD\").replace(/[\\u0300-\\u036f]/g, \"\").toLowerCase().replace(/[^a-z0-9]+/g, \" \").trim();",
139,
"93d3dceb9a6afe65af4edd6b994827ac"
],
[
"gxTkLasts270",
"function gxTkLasts270(s) {",
332,
"6902fc49c8ff51be4a04e4b9a87b7466"
],
[
"gxAgo270",
"const gxAgo270 = (iso) => { const m = Math.max(0, (Date.now() - Date.parse(iso)) / 60e3); return m < 60 ? Math.round(m) + \"m\" : m < 48 * 60 ? Math.round(m / 60)",
199,
"b6cd9945cb869f6ee4e2d8cc22aa5511"
],
[
"GxTalk270",
"function GxTalk270({ p, s }) {",
3093,
"2ff156f8e3cb93d47bfc5e6a3afb3ff6"
],
[
"GxLgLink285",
"function GxLgLink285({ go }) {",
396,
"aad7dead23aa8b40407d29a0f89ebfea"
],
[
"GxPlayers287",
"function GxPlayers287(P) {",
590,
"5684af00917db69c32e916daa1a4cf38"
],
[
"GxGoalCard288",
"function GxGoalCard288(P) {",
1122,
"52a7cccb8ee699530795fa9d80bea404"
],
[
"GxGoal289",
"function GxGoal289(P) {",
1896,
"02291a74a5d923d3aca010b091c6e74e"
]
]


def change(t):
    if GONE[0][1] not in t:
        print("(install) 306: already done")
        return t
    for name, start, size, fp in GONE:
        if t.count(start) != 1:
            fail("306: '" + name + "' found " + str(t.count(start)) + " times (expected 1). Send this log to the AI helper.")
        i = t.index(start)
        part = t[i:i + size]
        if hashlib.md5(part.encode("utf-8")).hexdigest() != fp:
            fail("306: '" + name + "' has changed since this was written. Send this log to the AI helper.")
        j = i + size
        if t[j:j + 1] == "\n":
            j += 1
        t = t[:i] + t[j:]
    print("(install) 306: removed " + str(len(GONE)) + " unused parts")
    return t


edit(APP, change)
