/* built from fantasy-gm.html - do not edit, run Install changes instead */
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
const {
  useState,
  useEffect,
  useMemo
} = React;
const KEY = "fantasy-islands-gm-v1";
const NHL = ["ANA", "BOS", "BUF", "CGY", "CAR", "CHI", "COL", "CBJ", "DAL", "DET", "EDM", "FLA", "LA", "MIN", "MTL", "NSH", "NJ", "NYI", "NYR", "OTT", "PHI", "PIT", "SJ", "SEA", "STL", "TB", "TOR", "UTA", "VAN", "VGK", "WSH", "WPG"];
const TEAMS0 = [{
  id: "me",
  name: "My Team (MacKinnon)"
}, {
  id: "kap",
  name: "Team Kaprizov"
}, {
  id: "kuc",
  name: "Team Kucherov"
}, {
  id: "dra",
  name: "Team Draisaitl"
}, {
  id: "mcd",
  name: "Team McDavid"
}, {
  id: "mak",
  name: "Team Makar"
}, {
  id: "mat",
  name: "Team Matthews"
}, {
  id: "pas",
  name: "Team Pastrnak"
}, {
  id: "cel",
  name: "Team Celebrini"
}, {
  id: "rob",
  name: "Team Robertson"
}];
const R = {
  me: "Nathan MacKinnon|COL|F|15;Brady Tkachuk|FLA|F|10.6|.85;Mikko Rantanen|DAL|F|9.4;Sam Reinhart|FLA|F|9.1;Aleksander Barkov|FLA|F|9.2;Lucas Raymond|DET|F|7.7;Sam Bennett|FLA|F|7.3;Matthew Knies|TOR|F|6;Patrick Kane|CHI|F|8.8;Matt Duchene|DAL|F|7.2|.7;Trevor Zegras|PHI|F|6.6;Tyler Seguin|DAL|F|6.3;Jared McCann|SEA|F|7;Ryan Hartman|MIN|F|6.4;Troy Terry|ANA|F|7.4|0|i;Josh Morrissey|WPG|D|7.6;Shayne Gostisbehere|CAR|D|7.7;Jackson LaCombe|ANA|D|6.6;Victor Hedman|TB|D|8.7;Luke Hughes|NJ|D|5.4;Scott Wedgewood|COL|G|10.8|.55;Lukas Dostal|ANA|G|7.9|.6;Kevin Lankinen|VAN|G|9|.7",
  kap: "Kirill Kaprizov|MIN|F|11;William Nylander|TOR|F|9;Kyle Connor|WPG|F|9;Adrian Kempe|LA|F|8;Alex Ovechkin|WSH|F|8|.75;Mark Stone|VGK|F|7;Ivan Barbashev|VGK|F|6;Pavel Zacha|BOS|F|6;J.T. Miller|NYR|F|8;Nazem Kadri|COL|F|7;Valeri Nichushkin|CBJ|F|6.5;Rickard Rakell|PIT|F|7;Mikael Granlund|ANA|F|6.5;Evan Bouchard|EDM|D|9;Noah Dobson|MTL|D|7.5;Shea Theodore|VGK|D|7;Sean Walker|CAR|D|5.5;Darnell Nurse|SJ|D|6;Dougie Hamilton|NJ|D|7;Mackenzie Blackwood|COL|G|9|.45;Linus Ullmark|OTT|G|9|.65;Darcy Kuemper|LA|G|9|.65",
  fa: "Sergei Murashov|PIT|G|9.9|.65;Joseph Woll|PHI|G|10.3|.5;Stuart Skinner|WPG|G|7.7|.8;Viktor Arvidsson|DET|F|7.3"
};
const SC0 = {
  G: 6,
  A: 4,
  PM: 2,
  PPP: 2,
  SHP: 3,
  SOG: 1,
  HIT: 0.1,
  BLK: 1,
  W: 5,
  GA: -3,
  SV: 0.6,
  SO: 5,
  OTL: 1
};

// Full 2026-27 NHL schedule. Month letters: S=Sep O=Oct N=Nov D=Dec J=Jan F=Feb M=Mar A=Apr
const SR = {
  ANA: "O:2,4,7,9,10,13,16,19,20,22,24,27,29;N:1,3,5,6,8,11,14,15,17,19,21,23,25,27,28;D:1,4,6,8,10,12,13,16,18,20,22,27,29;J:1,3,5,8,10,12,14,16,19,21,23,24,26,28,30;F:9,11,13,15,16,18,20,24,26,27;M:1,5,7,10,13,14,16,18,20,22,24,25,27,30;A:1,3,6,10",
  BOS: "S:29;O:2,3,5,8,10,13,16,17,20,22,24,27,29,31;N:2,5,8,12,14,17,18,21,25,27,29;D:1,5,8,10,12,13,15,17,19,20,22,26,27,30;J:1,2,5,6,9,12,14,16,18,20,22,23,26,28,30;F:10,13,15,17,19,21,22,25,27;M:3,4,6,8,10,11,13,15,18,20,23,25,26,30;A:1,3,5,7,9,10",
  BUF: "O:1,3,6,8,10,12,13,15,17,21,24,27,29,31;N:4,6,8,11,12,14,17,19,21,22,25,27;D:1,3,4,6,10,12,14,15,18,20,22,26,28,30;J:2,4,5,8,9,12,14,16,18,20,21,24,27,28,30;F:3,13,15,18,20,21,24,26,27;M:2,4,6,7,9,12,14,15,18,20,21,23,25,28,30;A:1,3,5,7,10",
  CGY: "O:1,3,4,8,10,13,15,18,22,24,26,28,30,31;N:2,4,6,8,11,14,15,17,19,21,23,25,27,28;D:1,3,5,8,10,11,15,17,19,22,26,29,31;J:2,3,5,7,9,12,14,16,18,21,23,26,28,30;F:1,3,12,13,15,17,19,21,24,27;M:3,5,7,9,12,13,15,17,19,21,23,25,27,30;A:1,3,5,8,10",
  CAR: "S:29;O:2,3,6,8,10,11,13,17,18,20,22,24,27,29;N:1,3,5,7,12,14,19,21,22,25,28,30;D:3,5,8,11,13,15,17,18,21,26,28,29,31;J:2,5,7,9,12,14,15,17,21,23,25,26,28,30;F:9,11,13,16,18,19,21,23,25,27;M:1,3,5,7,9,12,13,16,18,20,23,25,27,29,30;A:2,3,5,7,10",
  CHI: "S:29;O:1,3,6,8,10,13,15,17,23,25,27,29,31;N:2,4,5,7,12,14,17,19,21,22,25,27,29,30;D:3,4,6,8,10,12,18,20,27,29;J:1,2,4,7,9,10,12,14,16,18,20,22,24,26,28,30;F:10,11,13,17,20,21,23,26,28;M:1,3,5,6,8,10,13,14,16,19,21,23,25,26,28,30;A:1,3,6,8,10",
  COL: "S:30;O:3,7,8,10,13,14,16,19,20,23,25,28,31;N:2,3,5,7,10,12,14,18,19,25,27,28;D:1,3,5,7,8,12,14,16,18,20,27,29,31;J:2,4,6,8,10,12,14,16,18,20,22,24,26,28,30;F:9,12,13,15,17,20,22,25,27,28;M:2,5,7,9,11,13,15,17,19,21,23,25,27,29,30;A:2,4,6,8,10",
  CBJ: "O:1,3,9,10,13,17,18,20,24,27,29,31;N:3,5,6,10,12,14,17,19,21,23,25,27,30;D:3,5,7,10,12,13,15,17,19,21,22,26,27,29,31;J:2,3,5,7,8,12,15,16,18,21,23,24,26,28,30;F:8,9,11,13,15,17,18,20,22,26,27;M:1,3,5,7,11,13,16,18,20,22,25,27,30;A:1,3,6,8,10",
  DAL: "O:2,3,5,8,10,13,14,17,20,22,25,27,29,31;N:3,5,7,12,14,15,17,19,22,25,27,28;D:1,3,5,9,12,15,17,19,20,22,27,29,31;J:2,4,6,8,9,12,14,15,17,19,20,22,24,26,28,30;F:8,12,13,16,18,20,23,25,27,28;M:3,5,6,8,10,13,15,17,20,23,25,27,30;A:2,3,5,7,9,10",
  DET: "O:2,4,6,9,10,13,15,17,20,22,24,26,29,31;N:2,3,5,7,10,12,14,18,21,25,27,28;D:1,3,5,9,11,12,15,17,18,20,22,26,28,29,31;J:2,4,7,9,13,16,17,19,21,23,25,27,29,30;F:9,11,13,15,18,19,21,23,25,27;M:1,4,6,9,12,14,16,18,20,23,24,27,28,30;A:2,4,6,9,10",
  EDM: "S:29;O:1,3,7,10,13,15,17,20,22,24,26,28,31;N:1,3,5,7,9,11,14,15,17,19,21,22,24,27,28;D:1,3,6,8,10,12,14,17,19,20,27,28,30;J:2,3,5,7,9,11,13,15,17,20,21,23,26,28,30;F:3,12,13,17,19,22,25,27;M:1,3,6,9,11,13,15,18,20,21,23,25,27,31;A:2,3,5,7,10",
  FLA: "S:29;O:1,4,6,10,12,13,15,17,21,22,25,27,30;N:2,4,7,8,10,12,14,15,17,21,25,27,28;D:1,3,5,8,10,12,14,15,19,21,26,28,30;J:1,2,5,7,9,12,14,16,18,21,24,26,27,29;F:1,3,12,13,16,18,20,21,24,26,27;M:2,4,6,9,12,15,16,18,20,23,25,27,30;A:1,3,4,6,9,10",
  LA: "S:30;O:3,6,10,13,17,20,22,24,26,27,29,31;N:4,7,10,12,14,17,19,21,23,27,28;D:1,3,5,9,11,12,15,17,19,20,22,26,28,30;J:2,4,6,9,11,13,15,16,19,21,23,24,26,28,30;F:8,9,11,13,15,17,18,20,24,26,27;M:1,3,5,7,9,11,13,16,18,21,23,25,27,29,31;A:2,3,6,8,10",
  MIN: "O:1,3,6,8,10,12,13,15,18,20,22,24,25,27,29;N:1,3,6,7,10,12,14,17,19,21,23,25,27,29;D:1,3,5,8,10,12,15,18,19,22,26,28;J:1,2,5,7,9,14,16,17,19,21,23,25,26,28,30;F:11,13,15,16,18,20,23,27,28;M:3,6,7,9,11,14,17,19,21,23,25,27,29,31;A:2,4,6,8,10",
  MTL: "S:29;O:3,6,8,10,13,14,17,20,23,25,27,29,31;N:3,5,7,10,12,14,16,18,19,21,23,25,28,30;D:2,5,6,8,10,12,14,18,19,22,26,27,29,31;J:2,4,6,9,13,14,16,18,19,21,23,26,28,30;F:1,3,13,14,18,20,22,24,27;M:1,4,6,9,10,13,16,18,20,22,24,27,28,30;A:1,4,6,8,10",
  NSH: "O:1,3,6,8,10,13,15,17,22,24,25,27,29,31;N:3,5,7,10,11,13,15,17,21,25,27,28,30;D:3,5,6,8,10,12,15,18,20,22,26,28,29;J:1,2,5,7,9,10,12,14,16,18,20,21,23,26,28,30,31;F:2,13,16,18,20,21,23,25,27;M:2,4,6,9,11,13,15,17,20,23,26,27,30;A:1,3,6,8,10",
  NJ: "O:1,3,6,10,12,13,15,17,20,22,24,27,28,30;N:3,5,7,8,10,12,14,18,21,23,25,27,28;D:1,3,5,7,9,12,15,17,19,20,22,26,27,29;J:1,2,4,7,9,12,13,16,19,21,23,24,26,28,30,31;F:3,13,16,18,20,21,23,26,28;M:2,4,5,9,11,13,18,20,23,25,27,29,31;A:3,4,6,8,10",
  NYI: "S:30;O:3,6,8,10,13,15,17,20,22,25,27,29,31;N:5,7,9,12,14,17,19,21,23,25,27,28;D:1,3,4,7,10,11,15,16,18,20,22,26,27,30;J:2,5,7,9,13,15,16,18,20,22,23,26,28,30;F:1,3,12,13,15,18,20,22,23,26,27;M:1,4,7,9,12,13,15,17,20,21,25,27,30;A:1,2,4,6,8,10",
  NYR: "S:29;O:1,2,4,6,9,11,13,15,17,19,22,24,26;N:1,3,5,7,9,11,13,16,22,25,27,28,30;D:3,5,7,8,11,13,15,16,18,20,22,27,29,31;J:3,5,7,9,11,12,16,17,19,21,23,25,27,29,30;F:3,12,14,15,18,20,21,23,26,28;M:3,6,7,9,11,13,16,18,20,21,23,25,27,29;A:1,3,6,10",
  OTT: "O:3,5,6,8,10,12,13,15,17,21,22,24,27,29,31;N:1,4,7,10,12,14,17,19,21,23,25,27,28,30;D:3,5,6,8,10,12,14,18,20,27,29,31;J:2,5,6,8,12,14,16,18,20,23,25,28,30;F:9,11,13,15,17,18,21,22,25,26;M:2,4,6,7,9,11,13,14,16,18,20,24,25,27,30;A:2,4,7,8,10",
  PHI: "S:30;O:1,3,5,8,10,11,13,15,17,19,21,24,27,28;N:1,3,5,8,9,11,14,15,17,19,21,25,27,28,30;D:3,5,8,11,14,16,18,20,21,27,29;J:1,3,4,7,9,10,12,15,16,19,21,23,26,28,30,31;F:3,13,15,18,20,22,24,26,27;M:2,5,7,9,11,13,16,18,20,23,25,27,30;A:1,3,5,8,10",
  PIT: "S:30;O:3,5,7,9,10,13,16,17,19,22,24,29,31;N:3,5,7,8,11,14,19,21,22,25,27,28,30;D:2,5,6,8,10,12,15,17,18,22,26,29,31;J:1,3,7,9,12,13,16,18,21,23,25,26,29,31;F:2,13,15,16,19,21,23,25,28;M:2,4,6,7,9,11,13,14,16,18,20,22,25,27,30;A:1,3,4,6,9,10",
  SJ: "O:1,3,5,8,10,13,15,17,19,20,22,24,27,29,31;N:2,4,6,7,9,11,14,15,17,21,23,25,27,28;D:1,3,4,6,8,9,11,14,16,19,22,26,28,29;J:1,2,4,6,8,9,13,14,16,18,23,28,30;F:10,13,15,19,21,23,25,27;M:1,3,5,6,9,11,13,15,16,18,20,22,24,26,29,31;A:3,4,8,10",
  SEA: "O:1,3,4,6,9,11,13,15,17,20,22,24,28,30;N:4,7,12,14,19,21,23,25,27,28;D:1,3,4,6,8,10,12,15,17,18,20,22,29,30;J:2,3,5,8,9,12,14,16,18,19,21,23,25,26,28,31;F:3,13,15,17,19,20,22,24,27;M:1,3,4,6,8,11,13,15,17,19,21,23,25,27,28,30;A:3,5,6,8,10",
  STL: "O:2,3,6,8,10,13,15,17,20,22,24,27,29,31;N:3,5,7,10,12,14,17,19,21,22,25,27,28;D:2,4,6,8,10,12,13,15,17,19,21,22,27,29,31;J:2,3,5,8,13,14,16,18,21,23,26,28,30;F:9,12,13,15,17,19,21,25,27,28;M:4,7,9,11,13,15,18,20,21,23,25,27,28;A:1,3,4,6,8,10",
  TB: "O:1,3,5,8,10,13,15,17,20,23,24,29,31;N:3,5,7,8,11,12,14,17,19,22,25,27,28;D:2,5,7,10,12,13,15,17,19,20,22,26,28,29,31;J:2,5,7,9,11,14,16,18,21,23,26,30;F:2,3,12,13,16,18,20,23,25,27,28;M:3,5,6,8,11,13,15,17,18,20,23,25,27,30;A:1,3,5,6,8,10",
  TOR: "S:29,30;O:3,6,8,10,13,15,17,19,20,22,24,26,28,31;N:3,7,8,10,12,14,17,19,21,23,27,28,30;D:3,5,9,12,13,15,17,19,21,22,26,29,30;J:2,4,7,9,11,14,16,18,20,23,26,27,30;F:8,10,13,16,18,20,23,25,27;M:1,3,5,6,8,11,13,15,17,18,20,22,25,27,28,30;A:1,3,5,10",
  UTA: "O:1,3,4,6,8,10,13,15,17,19,22,24,27,29;N:1,3,5,7,11,12,14,16,18,21,23,25,27,28,30;D:2,3,5,10,12,14,15,17,19,21,26,29,31;J:2,5,7,9,12,13,15,18,23,25,27,29,31;F:2,3,12,14,15,17,19,21,24,26,28;M:2,4,7,9,13,15,18,19,21,23,26,30;A:1,3,5,7,9,10",
  VAN: "S:29;O:1,3,4,8,10,11,13,15,17,20,22,25,27,29,31;N:3,5,7,9,13,15,16,19,21,22,25,27,29;D:1,4,5,7,10,12,14,16,19,21,26,28,30;J:2,3,5,7,9,14,16,18,20,22,23,26,28,30;F:1,3,13,16,18,20,21,23,25,27;M:3,6,9,11,13,14,17,20,21,23,25,27,29,31;A:3,6,9,10",
  VGK: "S:29;O:2,4,6,8,10,12,13,15,17,20,22,24,27,30;N:2,3,5,8,11,13,15,17,19,21,24,27,28;D:1,3,5,8,10,12,16,18,21,22,26,28,29,31;J:2,4,7,9,12,14,16,17,20,22,24,26,28,30;F:1,3,13,15,18,20,22,24,26;M:2,4,5,7,9,11,13,15,17,20,23,25,27,31;A:2,3,6,8,10",
  WSH: "O:2,3,7,9,11,13,14,17,20,24,28,29;N:1,3,7,10,12,14,17,19,21,25,27,28;D:1,3,5,7,10,12,15,17,19,21,26,28,30,31;J:2,4,6,8,10,12,14,16,18,19,22,24,29,30;F:2,3,13,14,16,19,21,23,25,26;M:1,3,5,7,9,10,13,15,17,18,21,23,24,26,28,30;A:1,3,4,6,8,10",
  WPG: "O:2,4,5,7,9,13,15,17,20,22,25,27,29,30;N:1,3,5,8,10,12,14,17,19,21,23,25,27,28,30;D:2,5,6,8,10,12,15,19,20,22,26,28,31;J:2,4,7,9,11,14,16,17,19,21,24,28,30;F:2,3,13,15,17,19,21,23,25,27;M:1,5,7,9,11,13,15,16,18,20,23,25,27,31;A:3,5,7,9,10"
};
const MON = {
  S: [2026, 8],
  O: [2026, 9],
  N: [2026, 10],
  D: [2026, 11],
  J: [2027, 0],
  F: [2027, 1],
  M: [2027, 2],
  A: [2027, 3]
};
const iso = d => d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0") + "-" + String(d.getDate()).padStart(2, "0");
const fromIso = x => new Date(x + "T12:00:00");
const addDays = (x, n) => {
  const d = fromIso(x);
  d.setDate(d.getDate() + n);
  return iso(d);
};
const todayISO = () => iso(new Date());
const dayLabel = x => fromIso(x).toLocaleDateString("en-US", {
  weekday: "short",
  month: "numeric",
  day: "numeric"
});
const mdL = x => fromIso(x).toLocaleDateString("en-US", {
  month: "short",
  day: "numeric"
});
const SCHED = (() => {
  const out = {};
  Object.entries(SR).forEach(([t, str]) => {
    const set = new Set();
    str.split(";").forEach(part => {
      const [m, ds] = part.split(":");
      const [y, mo] = MON[m];
      ds.split(",").forEach(d => set.add(iso(new Date(y, mo, +d, 12))));
    });
    out[t] = set;
  });
  return out;
})();
const wkGames = dates => {
  const g = {};
  NHL.forEach(t => {
    g[t] = [];
    dates.forEach((d, i) => {
      if (SCHED[t] && SCHED[t].has(d)) g[t].push(i);
    });
  });
  return g;
};
const lab = (i, dates) => `Week ${i + 1} · ${mdL(dates[0])} – ${mdL(dates[dates.length - 1])}`;
const mkW = (i, start, len) => {
  const dates = [...Array(len)].map((_, k) => addDays(start, k));
  return {
    label: lab(i, dates),
    dates,
    pairs: [],
    done: 0,
    act: {}
  };
};
const defaultWeeks = () => {
  const w = [mkW(0, "2026-09-29", 6)];
  let st = "2026-10-05";
  for (let i = 1; i < 28; i++) {
    w.push(mkW(i, st, 7));
    st = addDays(st, 7);
  }
  w[0].pairs = [["me", "kap"]];
  return w;
};
const effDone = (w, auto) => auto && w.dates && w.dates.length ? w.dates.filter(d => d < todayISO()).length : w.done || 0;
const deriveWeek = (w, auto) => {
  if (!w.dates || !w.dates.length) return {
    ...w,
    days: w.days || [],
    games: w.games || {},
    done: w.done || 0
  };
  return {
    ...w,
    days: w.dates.map(dayLabel),
    games: wkGames(w.dates),
    done: effDone(w, auto)
  };
};
function parsePlayers() {
  const out = [];
  let i = 0;
  Object.entries(R).forEach(([ft, str]) => {
    str.split(";").forEach(s => {
      const [n, t, p, a, pr, f] = s.trim().split("|");
      out.push({
        id: "p" + i++,
        n,
        t,
        p,
        avg: +a,
        prob: pr === undefined || pr === "" ? 1 : +pr,
        ft,
        ir: f === "i",
        est: !(ft === "me" || ft === "fa"),
        gp: 0,
        tot: 0
      });
    });
  });
  return out;
}
const init = () => ({
  teams: TEAMS0,
  me: "me",
  opp: "kap",
  players: parsePlayers(),
  weeks: defaultWeeks(),
  wk: 0,
  sc: SC0,
  blend: 10,
  autoDone: true,
  lastSync: null
});
const migrate = v => {
  let weeks;
  if (!v.weeks.some(w => w.dates && w.dates.length)) {
    weeks = defaultWeeks().map((w, i) => v.weeks[i] ? {
      ...w,
      pairs: v.weeks[i].pairs || w.pairs,
      act: v.weeks[i].act || {},
      done: v.weeks[i].done || 0
    } : w);
  } else weeks = v.weeks.map(w => ({
    pairs: [],
    done: 0,
    act: {},
    ...w
  }));
  return {
    ...init(),
    ...v,
    weeks,
    players: v.players.map(p => ({
      gp: 0,
      tot: 0,
      ...p
    })),
    blend: v.blend === undefined ? 10 : v.blend,
    autoDone: v.autoDone === undefined ? true : v.autoDone,
    wk: Math.min(v.wk || 0, weeks.length - 1)
  };
};
const OUTS = ["OUT", "INJURY_RESERVE", "SUSPENSION"];
const DEFAULT_BACK = {
  "Brady Tkachuk": "2026-09-29",
  "Matt Duchene": "2026-10-02",
  "Alex Ovechkin": "2026-10-02",
  "Jake Oettinger": "2026-10-02",
  "Mathew Barzal": "2026-09-30",
  "Dylan Larkin": "2026-10-02",
  "Seth Jarvis": "2026-10-24",
  "Charlie McAvoy": "2026-10-13",
  "Filip Gustavsson": "2026-11-01",
  "Brad Marchand": "2026-11-02",
  "Connor Bedard": "2026-11-07",
  "Troy Terry": "2026-11-21",
  "Dan Vladar": "2026-09-30",
  "Brock Faber": "2026-10-01",
  "Mattias Samuelsson": "2026-10-01",
  "Jake Sanderson": "2026-09-29",
  "Elvis Merzlikins": "2026-11-30",
  "Thatcher Demko": "2026-10-03",
  "Alex Lyon": "2026-10-01",
  "Artem Zub": "2026-10-05",
  "Kaiden Guhle": "2026-10-23",
  "Max Domi": "2026-11-07",
  "Jiri Kulich": "2026-10-01",
  "Jason Zucker": "2026-10-15",
  "Ivan Demidov": "2026-09-29",
  "Jonathan Huberdeau": "2026-10-08",
  "Filip Chytil": "2026-10-08",
  "Shane Pinto": "2026-09-29"
};
function applyESPN(s, E) {
  const teams = (E.teams || []).map(t => ({
    id: "t" + t.id,
    name: t.name
  }));
  if (!teams.length) throw new Error("The ESPN file has no teams in it.");
  const prev = {};
  s.players.forEach(p => prev[p.n.toLowerCase()] = p);
  const players = (E.players || []).filter(p => p.n && NHL.includes(p.t)).map(p => {
    const pv = prev[p.n.toLowerCase()];
    const gsAuto = s.autoGoalie !== false && p.p === "G" ? ((E.signals || {}).gstart || {})[p.id] : null;
    const prob = p.p === "G" ? gsAuto ? gsAuto.share : pv && pv.p === "G" && pv.prob > 0 ? pv.prob : 0.5 : p.status === "DAY_TO_DAY" ? 0.8 : 1;
    const avg = p.pavg > 0 ? p.pavg : pv ? pv.avg : p.avg > 0 ? p.avg : p.p === "G" ? 7 : 5;
    const back = pv && pv.back !== undefined ? pv.back : DEFAULT_BACK[p.n] || "";
    return {
      id: "e" + p.id,
      n: p.n,
      t: p.t,
      p: p.p,
      avg: Math.round(avg * 100) / 100,
      prob,
      ft: p.ft ? "t" + p.ft : "fa",
      ir: p.ir !== undefined ? !!p.ir : !!(pv && pv.ir),
      est: !(p.pavg > 0) && !pv,
      gp: p.gp || 0,
      tot: p.tot || 0,
      status: p.status || "",
      back,
      proj: p.pavg > 0,
      keep: pv ? pv.keep : false,
      own: p.own || 0,
      chg: p.chg || 0,
      wv: !!p.wv
    };
  });
  const ms = E.matchups || [];
  const pack = mm => {
    const act = {};
    mm.forEach(m => {
      act["t" + m.home] = m.hs;
      act["t" + m.away] = m.as;
    });
    return {
      pairs: mm.map(m => ["t" + m.home, "t" + m.away]),
      act
    };
  };
  const okWeeks = ws => ws && ws.length >= 20 && ws.length <= 40 && ws.every(w => w.dates && w.dates.length) && ws.some(w => w.dates.length >= 5);
  const fromEspn = (E.periods || []).filter(pp => pp.dates && pp.dates.length);
  let weeks;
  if (fromEspn.length >= 20 && fromEspn.length <= 40 && fromEspn.some(pp => pp.dates.length >= 5)) {
    weeks = fromEspn.map((pp, i) => ({
      label: lab(i, pp.dates),
      dates: pp.dates,
      period: pp.id,
      done: 0,
      ...pack(ms.filter(m => m.period === pp.id))
    }));
  } else {
    const base = okWeeks(s.weeks) ? s.weeks : defaultWeeks();
    weeks = base.map((w, i) => ({
      ...w,
      period: i + 1,
      ...pack(ms.filter(m => m.period === i + 1))
    }));
  }
  const ci = weeks.findIndex(w => w.period === E.currentPeriod);
  const wk = ci >= 0 ? ci : 0;
  const me = "t" + E.myTeamId;
  const opp = teams.some(t => t.id === s.opp) && s.opp !== me ? s.opp : (teams.find(t => t.id !== me) || {}).id;
  return {
    ...s,
    teams,
    me,
    opp,
    players: gxSimPlayers(players),
    weeks,
    wk,
    lastSync: E.generated,
    league: E.leagueName || "",
    goalies: E.goalies || s.goalies || {}
  };
}

// ---------- projections ----------
const effAvg0 = (p, K) => p.gp > 0 ? (p.avg * K + p.tot) / (K + p.gp) : p.avg;
const effAvg = (p, K, dt) => {
  const base = effAvg0(p, K);
  const M = window.__MODEL,
    mode = window.__PMODE || "espn";
  {
    const A = window.__AI,
      aid = mode === "ai" && typeof p.id === "string" && p.id[0] === "e" ? p.id.slice(1) : null,
      ap = aid && A ? (A.proj || {})[aid] : null,
      av = ap ? dt && ap[dt] != null ? ap[dt] : (window.__AIAVG || {})[aid] : null;
    if (av != null) return av * (p.gwMul || 1);
  }
  let v = base;
  if (M && mode !== "espn" && typeof p.id === "string" && p.id[0] === "e") {
    const id = p.id.slice(1),
      pr = (M.proj || {})[id];
    const mv = dt && pr && pr[dt] != null ? pr[dt] : (M.base || {})[id];
    if (mv != null) {
      const mb = (M.base || {})[id];
      const ratio = dt && pr && pr[dt] != null && mb > 0 ? Math.max(0.5, Math.min(1.6, pr[dt] / mb)) : 1;
      v = mode === "model" ? mv : (base * ratio + mv) / 2;
    }
  }
  return v * (p.gwMul || 1);
};
const autoInj = p => {
  const S = window.__SIG || {};
  const id = typeof p.id === "string" && p.id[0] === "e" ? p.id.slice(1) : null;
  return id ? (S.injuries || {})[id] || null : null;
};
const effBack = p => {
  if (p.back && p.back !== DEFAULT_BACK[p.n]) return {
    d: p.back,
    src: "you"
  };
  const a = autoInj(p);
  if (a && a.back) return {
    d: a.back,
    src: a.src === "parsed" ? "news" : "ESPN"
  };
  if (p.back) return {
    d: p.back,
    src: "estimate"
  };
  return {
    d: "",
    src: ""
  };
};
const avail = (p, date) => {
  const b = effBack(p).d;
  if (b) {
    if (date && date < b) return 0;
    if (date && date < addDays(b, 7)) return 0.9;
    return 1;
  }
  const a = autoInj(p);
  const st = a && a.status || p.status || "";
  return OUTS.includes(st) || /^out|injured reserve|suspen/i.test(st) ? 0 : 1;
};
const nrm = x => (x || "").normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase().trim();
// back-to-backs: starters usually rest the 2nd night, backups usually start it
const b2bAdj = (p, dt) => {
  const S = SCHED[p.t];
  if (!dt || !S || p.p !== "G") return null;
  const pc = v => ` (${Math.round(v * 100)}%)`;
  if (S.has(addDays(dt, -1))) {
    if (p.prob >= 0.55) {
      const v = p.prob * 0.5;
      return {
        v,
        l: "B2B 2nd night · likely rests" + pc(v),
        b2b: 2
      };
    }
    if (p.prob <= 0.45) {
      const v = Math.min(0.8, p.prob + 0.3);
      return {
        v,
        l: "B2B 2nd night · likely starts" + pc(v),
        b2b: 2
      };
    }
    return {
      v: p.prob,
      l: "B2B 2nd night · split" + pc(p.prob),
      b2b: 2
    };
  }
  if (S.has(addDays(dt, 1))) {
    if (p.prob >= 0.55) {
      const v = Math.min(0.95, p.prob + 0.1);
      return {
        v,
        l: "B2B 1st night · likely starts" + pc(v),
        b2b: 1
      };
    }
    if (p.prob <= 0.45) {
      const v = Math.max(0.05, p.prob - 0.1);
      return {
        v,
        l: "B2B 1st night · likely rests" + pc(v),
        b2b: 1
      };
    }
  }
  return null;
};
const gStart = (p, dt) => {
  const aiG = window.__PMODE === "ai" && dt && typeof p.id === "string" && p.id[0] === "e" ? (((window.__AI || {}).gstart || {})[p.id.slice(1)] || {})[dt] : null;
  const fallback = aiG != null ? {
    v: aiG,
    l: `AI start chance (${Math.round(aiG * 100)}%)`
  } : b2bAdj(p, dt) || {
    v: p.prob,
    l: ""
  };
  const day = dt && (window.__GOALIES || {})[dt];
  if (!day) return fallback;
  const me = day[nrm(p.n)];
  if (me) {
    const st = (me.status || "").toLowerCase();
    if (st.includes("confirm") && !st.includes("un")) return {
      v: 1,
      l: "✓ confirmed"
    };
    if (/likely|expected|project/.test(st)) return {
      v: 0.85,
      l: "likely"
    };
    return {
      v: 0.5,
      l: "unconfirmed"
    };
  }
  const mate = Object.entries(day).find(([, x]) => x.team === p.t);
  if (mate) {
    const st = (mate[1].status || "").toLowerCase();
    const mv = st.includes("confirm") && !st.includes("un") ? 1 : /likely|expected|project/.test(st) ? 0.85 : 0.5;
    const who = mate[0].replace(/\b\w/g, c => c.toUpperCase());
    return {
      v: 1 - mv,
      l: mv === 1 ? "not starting" : `backup · ${who} ${mv === 0.5 ? "unconfirmed" : "likely"} (${Math.round((1 - mv) * 100)}%)`
    };
  }
  return fallback;
};
function dayLineup(roster, wk, d, K, cap) {
  const c = cap || {
    F: 9,
    D: 5,
    U: 1,
    G: 2
  };
  const dt = wk.dates ? wk.dates[d] : null;
  const pl = roster.filter(p => !p.ir && p.prob > 0 && onDay(p, dt) && avail(p, dt) > 0 && (wk.games[p.t] || []).includes(d)).map(p => {
    const g = p.p === "G" ? gStart(p, dt) : null;
    return {
      ...p,
      x: effAvg(p, K, dt) * (g ? g.v : p.prob) * avail(p, dt),
      gs: g ? g.l : "",
      dt
    };
  });
  const by = (a, b) => b.x - a.x;
  const F = pl.filter(p => p.p === "F").sort(by),
    D = pl.filter(p => p.p === "D").sort(by),
    G = pl.filter(p => p.p === "G").sort(by);
  const fs = F.slice(0, c.F),
    ds = D.slice(0, c.D);
  const rest = [...F.slice(c.F), ...D.slice(c.D)].sort(by);
  const u = rest.slice(0, c.U),
    gs = G.slice(0, c.G);
  const bench = [...rest.slice(c.U), ...G.slice(c.G)];
  const start = [...fs.map(p => ({
    ...p,
    slot: "F"
  })), ...ds.map(p => ({
    ...p,
    slot: "D"
  })), ...u.map(p => ({
    ...p,
    slot: "UTIL"
  })), ...gs.map(p => ({
    ...p,
    slot: "G"
  }))];
  return {
    start,
    bench,
    total: start.reduce((s, p) => s + p.x, 0),
    empty: c.F - fs.length + (c.D - ds.length) + (c.U - u.length) + (c.G - gs.length),
    sched: pl.length
  };
}
function weekProj(roster, wk, K, from = 0) {
  const days = wk.days.map((_, d) => d < from ? null : dayLineup(roster, wk, d, K));
  const live = days.filter(Boolean);
  const sum = f => live.reduce((s, x) => s + f(x), 0);
  return {
    days,
    total: sum(x => x.total),
    sched: sum(x => x.sched),
    used: sum(x => x.start.filter(gxGPlays).length),
    wasted: sum(x => x.bench.length),
    empty: sum(x => x.empty)
  };
}
const oppOf = (wk, me) => {
  const pr = (wk.pairs || []).find(p => p[0] && p[1] && (p[0] === me || p[1] === me));
  return pr ? pr[0] === me ? pr[1] : pr[0] : null;
};
const f1 = x => (Math.round((+x || 0) * 10) / 10).toFixed(1);
const toDate = x => {
  if (!x) return null;
  let str = String(x);
  if (!/[zZ]$|[+-]\d\d:?\d\d$/.test(str)) str += "Z";
  const d = new Date(str);
  return isNaN(d) ? null : d;
};
const fmtTime = x => {
  const d = toDate(x);
  return d ? d.toLocaleString("en-US", {
    weekday: "short",
    month: "short",
    day: "numeric",
    hour: "numeric",
    minute: "2-digit"
  }) : String(x || "");
};
const gms = (wk, t) => (wk.games[t] || []).length;

// ---------- signals ----------
const sigOf = p => {
  const S = window.__SIG || {};
  const id = typeof p.id === "string" && p.id[0] === "e" ? p.id.slice(1) : null;
  if (!id) return {};
  return {
    rec: (S.recent || {})[id],
    pp1: ((S.pp1 || {}).on || {})[id],
    ppChg: ((S.pp1 || {}).changes || {})[id],
    news: (S.news || {})[id],
    toi: (S.toi || {})[id],
    lines: {
      grp: ((S.lines || {}).top || {})[id],
      chg: ((S.lines || {}).changes || {})[id]
    },
    luck: (S.luck || {})[id],
    gs: (S.gstart || {})[id]
  };
};
const formRatio = (p, K) => {
  const r = sigOf(p).rec,
    b = effAvg(p, K);
  return r && r.gp >= 3 && b > 0 ? r.ppg / b : null;
};
const LBL = {
  F1: "1st line",
  F2: "2nd line",
  D1: "top pair",
  D2: "2nd pair"
};
const tags = (p, K) => {
  const g = sigOf(p),
    out = [],
    fr = formRatio(p, K);
  {
    const M = window.__MODEL,
      pid = typeof p.id === "string" && p.id[0] === "e" ? p.id.slice(1) : null,
      mb = M && pid ? (M.base || {})[pid] : null;
    if (mb != null && p.proj && p.avg > 0 && window.__PMODE !== "espn") {
      if (mb - p.avg >= 1 && mb / p.avg >= 1.15) out.push({
        t: "underrated",
        c: "text-green-700"
      });else if (p.avg - mb >= 1 && mb / p.avg <= 0.85) out.push({
        t: "overrated",
        c: "text-amber-600"
      });
    }
  }
  if (g.gs && g.gs.flag) out.push({
    t: `started ${g.gs.rs} of last ${g.gs.rg}`,
    c: g.gs.rs / g.gs.rg > g.gs.prior ? "text-green-700 font-semibold" : "text-red-600 font-semibold"
  });
  if (g.lines && g.lines.chg === "up") out.push({
    t: `↑ ${LBL[g.lines.grp] || "promoted"}`,
    c: "text-green-700 font-semibold"
  });else if (g.lines && g.lines.chg === "down") out.push({
    t: "↓ demoted",
    c: "text-red-600"
  });
  if (g.luck && g.luck.t === "s" && Math.abs(g.luck.d) >= 2) out.push({
    t: g.luck.d > 0 ? `lucky +${f1(g.luck.d)} G` : `unlucky ${f1(g.luck.d)} G`,
    c: g.luck.d > 0 ? "text-amber-600" : "text-sky-600"
  });
  if (g.luck && g.luck.t === "g" && Math.abs(g.luck.d) >= 4) out.push({
    t: g.luck.d > 0 ? `hot SV +${f1(g.luck.d)}` : `cold SV ${f1(g.luck.d)}`,
    c: g.luck.d > 0 ? "text-amber-600" : "text-sky-600"
  });
  if (fr !== null && fr >= 1.25) out.push({
    t: `${f1(g.rec.ppg)}/g last 14d`,
    c: "text-orange-600"
  });else if (fr !== null && fr <= 0.7) out.push({
    t: `${f1(g.rec.ppg)}/g last 14d`,
    c: "text-sky-600"
  });
  if (g.ppChg === "added") out.push({
    t: "↑ new on PP1",
    c: "text-green-700 font-semibold"
  });else if (g.ppChg === "removed") out.push({
    t: "↓ off PP1",
    c: "text-red-600 font-semibold"
  });else if (g.pp1) out.push({
    t: "PP1",
    c: "text-slate-500"
  });
  const t = g.toi;
  if (t && t.d >= 120) out.push({
    t: `${mm(t.d)} TOI`,
    c: "text-green-700 font-semibold"
  });else if (t && t.d <= -120) out.push({
    t: `${mm(t.d)} TOI`,
    c: "text-red-600"
  });
  if (t && t.pd >= 60) out.push({
    t: `PP ${mm(t.pd)}`,
    c: "text-green-700"
  });else if (t && t.pd <= -60) out.push({
    t: `PP ${mm(t.pd)}`,
    c: "text-red-600"
  });
  if ((p.chg || 0) >= 5) out.push({
    t: `+${f1(p.chg)}% rostered`,
    c: "text-green-700"
  });
  {
    const nw = newsOf(p)[0];
    if (nw) out.push({
      t: (nw.label ? nw.label + ": " : "") + (nw.h || "").slice(0, 60),
      c: NEWS_CLS[nw.kind] || "text-slate-500",
      u: nw.u
    });
  }
  return out;
};
const Tags = ({
  p,
  K
}) => /*#__PURE__*/React.createElement("span", {
  className: "inline-flex flex-wrap gap-x-2 gap-y-0.5"
}, tags(p, K).map((t, i) => t.u ? /*#__PURE__*/React.createElement("a", {
  key: i,
  href: t.u,
  target: "_blank",
  rel: "noreferrer",
  className: "text-xs underline " + t.c
}, t.t) : /*#__PURE__*/React.createElement("span", {
  key: i,
  className: "text-xs " + t.c
}, t.t)));
// ice time: seconds -> "+2.5 min"
const mm = sec => (sec >= 0 ? "+" : "−") + (Math.abs(sec) / 60).toFixed(1) + " min";
const toiOf = p => sigOf(p).toi || null;
// ---------- move engine ----------
function computeMoves(s, o) {
  const K = s.blend,
    gw = s.gw ?? 1.3,
    protectTop = s.protectTop ?? 8;
  const mins = {
    F: s.minF ?? 10,
    D: s.minD ?? 5,
    G: s.minGo ?? 2
  };
  const H = o.H ?? 1,
    pos = o.pos || "all",
    q = (o.q || "").toLowerCase();
  const myR = s.players.filter(p => p.ft === s.me);
  const fas = s.players.filter(p => p.ft === "fa");
  const wt = p => p.p === "G" ? {
    ...p,
    gwMul: gw
  } : p;
  const n = H === 0 ? s.weeks.length - s.wk : H;
  const horizon = s.weeks.slice(s.wk, s.wk + n).map((w, i) => {
    const dw = deriveWeek(w, s.autoDone);
    return {
      wk: dw,
      from: i === 0 ? dw.done : 0
    };
  });
  const lineupAware = H !== 0;
  const total = roster => {
    const r = roster.map(wt);
    return horizon.reduce((t, h) => t + weekProj(r, h.wk, K, h.from).total, 0);
  };
  const gamesIn = p => {
    const a = pickStart(p);
    let g = 0;
    horizon.forEach(h => (h.wk.games[p.t] || []).forEach(d => {
      const dt = h.wk.dates ? h.wk.dates[d] : null;
      if (d >= h.from && (!dt || dt >= a) && !p.ir && avail(p, dt)) g++;
    }));
    return g;
  };
  const rawPts = (p, ref) => {
    const a = pickStart(ref || p);
    let t = 0;
    horizon.forEach(h => (h.wk.games[p.t] || []).forEach(d => {
      const dt = h.wk.dates ? h.wk.dates[d] : null;
      if (d >= h.from && (!dt || dt >= a) && !p.ir && avail(p, dt)) t += effAvg(wt(p), K, dt) * p.prob;
    }));
    return t;
  };
  const ranked = myR.filter(p => !p.ir).sort((a, b) => gxPgAvg(wt(b), K) - gxPgAvg(wt(a), K)); /* gx088 */
  const autoProt = new Set(ranked.slice(0, protectTop).map(p => p.id));
  const protectedIds = new Set([...autoProt, ...myR.filter(p => p.keep).map(p => p.id)]);
  const cnt = {
    F: 0,
    D: 0,
    G: 0
  };
  myR.forEach(p => {
    if (!p.ir) cnt[p.p]++;
  });
  const keepsMins = (d, f) => d.p === f.p || cnt[d.p] - 1 >= mins[d.p];
  const canDrop = (d, f) => !d.ir && !protectedIds.has(d.id) && keepsMins(d, f);
  const inTab = f => pos === "all" || (pos === "pp1" ? !!sigOf(f).pp1 : pos === "sk" ? f.p !== "G" : f.p === pos);
  const base = lineupAware ? total(myR) : 0;
  const pool = fas.filter(f => f.prob > 0 && (f.proj !== false || f.gp > 0) && inTab(f) && f.n.toLowerCase().includes(q) && (!!q || !goalieOut(f))).map(f => ({
    f,
    raw: rawPts(f)
  })).filter(x => x.raw > 0).sort((a, b) => b.raw - a.raw).slice(0, lineupAware ? o.pool || 120 : 500);
  const res = [];
  pool.forEach(({
    f,
    raw
  }) => {
    let best = null;
    myR.forEach(d => {
      if (!canDrop(d, f)) return;
      const gain = lineupAware ? total(timedMove(myR, s.me, [{
        add: f,
        drop: d
      }])) - base : raw - rawPts(d, f);
      if (!best || gain > best.gain) best = {
        gain,
        d
      };
    });
    if (best) res.push({
      f,
      ...best
    });
  });
  res.sort((a, b) => b.gain - a.gain);
  return {
    res,
    total,
    gamesIn,
    rawPts,
    autoProt,
    protectedIds,
    cnt,
    mins,
    keepsMins,
    lineupAware,
    myR,
    fas,
    K,
    gw,
    protectTop
  };
}

// ---------- shared UI ----------
const Card = ({
  label,
  value,
  sub,
  tone
}) => /*#__PURE__*/React.createElement("div", {
  className: "rounded-xl p-4 border " + (tone || "bg-white border-slate-200")
}, /*#__PURE__*/React.createElement("div", {
  className: "text-xs uppercase tracking-wide text-slate-500"
}, label), /*#__PURE__*/React.createElement("div", {
  className: "text-2xl font-bold"
}, value), sub && /*#__PURE__*/React.createElement("div", {
  className: "text-xs text-slate-500 mt-1"
}, sub));
const inp = "border border-slate-300 rounded-lg px-2 py-1.5 text-sm bg-white";
const box = "bg-white rounded-xl border border-slate-200 p-4 text-sm mb-4";
const Pills = ({
  items,
  value,
  onChange
}) => /*#__PURE__*/React.createElement("div", {
  className: "flex gap-2 overflow-x-auto navscroll pb-1"
}, items.map(([k, l]) => /*#__PURE__*/React.createElement("button", {
  key: k,
  onClick: () => onChange(k),
  className: "px-3 py-1.5 rounded-full text-sm border whitespace-nowrap " + (value === k ? "bg-blue-600 text-white border-blue-600" : "bg-white border-slate-300 text-slate-600")
}, l)));
const teamName = (s, id) => id === "fa" ? "Free agent" : (s.teams.find(t => t.id === id) || {}).name || "";
const PlayerLine = ({
  s,
  p,
  extra
}) => {
  // player line v15: logo, name, one short note (news_logos.py)
  const tg = shortTag(p, s.blend);
  return /*#__PURE__*/React.createElement("div", {
    className: "flex items-center gap-3 py-2.5 border-t border-slate-100 text-sm"
  }, /*#__PURE__*/React.createElement(GxFace, {
    p: p,
    size: 26
  }), /*#__PURE__*/React.createElement("div", {
    className: "min-w-0 flex-1"
  }, /*#__PURE__*/React.createElement("div", {
    className: "flex items-center gap-2 min-w-0"
  }, /*#__PURE__*/React.createElement(PN, {
    p: p,
    className: "truncate font-medium"
  }), /*#__PURE__*/React.createElement("span", {
    className: "text-xs text-slate-500"
  }, p.p), tg ? /*#__PURE__*/React.createElement("span", {
    className: "text-xs truncate " + tg.c
  }, tg.t) : null), /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500 flex flex-wrap items-baseline gap-x-2 mt-0.5"
  }, /*#__PURE__*/React.createElement(TL, {
    s: s,
    id: p.ft
  }), extra)), /*#__PURE__*/React.createElement("div", {
    className: "text-right whitespace-nowrap"
  }, /*#__PURE__*/React.createElement("div", {
    className: "font-semibold"
  }, f1(effAvg(p, s.blend))), /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500"
  }, "pts/g")));
};
// round 28: every box opens and closes; the choice is remembered on this device (news_logos.py)
const UIKEY = "fantasy-islands-gm-ui";
let __UI = null;
const uiGet = () => {
  if (!__UI) {
    try {
      __UI = JSON.parse(localStorage.getItem(UIKEY) || "{}") || {};
    } catch (e) {
      __UI = {};
    }
  }
  return __UI;
};
const uiSet = (k, v) => {
  const u = uiGet();
  u[k] = v;
  try {
    localStorage.setItem(UIKEY, JSON.stringify(u));
  } catch (e) {}
};
const secKey = t => typeof t === "string" ? t.toLowerCase().replace(/[^a-z ]/g, " ").replace(/\s+/g, " ").trim().slice(0, 40) : "box";
// boxes that start closed: "tab:start of the title"
const SEC_SHUT = ["today:your lineup", "today:injuries", "today:news on your players", "myteam:this week day by day", "myteam:player updates", "myteam:injuries", "myteam:protected players", "moves/advice:free agents to watch", "moves/advice:trade advice", "moves/advice:line promotions", "moves/advice:luck", "moves/advice:model vs espn", "moves/planner:week ", "moves/planner:chronic bench players", "moves/trades:trade ideas", "teams:news", "league/power:how to climb the rankings", "league/standings:all teams this week", "news:your opponent", "news:around your league", "news:free agents", "news:phone notifications", "setup/settings:team names"];
const Section = ({
  title,
  sub,
  link,
  children,
  closed,
  id
}) => {
  // section v40: the same corner-bracket panel as the new pages (news_logos.py)
  const [k] = useState(() => "sec:" + (window.__TAB || "") + ":" + (id || secKey(title)));
  const [open, setOpen] = useState(() => {
    const v = uiGet()[k];
    return v == null ? !(closed || SEC_SHUT.some(x => k.indexOf("sec:" + x) === 0)) : !!v;
  });
  const flip = () => {
    uiSet(k, !open);
    setOpen(!open);
  };
  const onKey = e => {
    if (e.key === "Enter" || e.key === " ") {
      e.preventDefault();
      flip();
    }
  };
  return /*#__PURE__*/React.createElement("div", {
    className: "gx-pn text-sm" + (open ? "" : " self-start"),
    style: {
      minWidth: 0
    }
  }, /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("div", {
    className: "flex items-start gap-2" + (open ? " mb-2" : "")
  }, /*#__PURE__*/React.createElement("div", {
    role: "button",
    tabIndex: 0,
    "aria-expanded": open,
    className: "sec-head",
    onClick: flip,
    onKeyDown: onKey
  }, /*#__PURE__*/React.createElement("div", {
    className: "gx-st"
  }, title), open && sub ? /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500",
    style: {
      marginTop: 2
    }
  }, sub) : null), open && link ? /*#__PURE__*/React.createElement("button", {
    className: "text-xs text-blue-600 whitespace-nowrap",
    onClick: link[1]
  }, link[0] + " \u2192") : null, /*#__PURE__*/React.createElement("button", {
    type: "button",
    onClick: flip,
    "aria-label": open ? "Close this box" : "Open this box",
    style: {
      lineHeight: 0,
      padding: "2px 0"
    }
  }, /*#__PURE__*/React.createElement("span", {
    className: "sec-chev" + (open ? "" : " shut")
  }))), open ? children : null);
};
const SectionShut = p => /*#__PURE__*/React.createElement(Section, _extends({}, p, {
  closed: true
}));
const DayFold = ({
  id,
  open0,
  head,
  right,
  children
}) => {
  const k = "day:" + id;
  const [open, setOpen] = useState(() => {
    const v = uiGet()[k];
    return v == null ? !!open0 : !!v;
  });
  const flip = () => {
    uiSet(k, !open);
    setOpen(!open);
  };
  const onKey = e => {
    if (e.key === "Enter" || e.key === " ") {
      e.preventDefault();
      flip();
    }
  };
  return /*#__PURE__*/React.createElement("div", {
    className: "bg-white rounded-xl border border-slate-200 mb-3"
  }, /*#__PURE__*/React.createElement("div", {
    role: "button",
    tabIndex: 0,
    "aria-expanded": open,
    onClick: flip,
    onKeyDown: onKey,
    className: "flex items-center gap-3 px-3 py-2 text-sm cursor-pointer" + (open ? " border-b border-slate-200" : "")
  }, /*#__PURE__*/React.createElement("span", {
    className: "font-semibold"
  }, head), /*#__PURE__*/React.createElement("span", {
    className: "ml-auto flex items-center gap-3"
  }, right), /*#__PURE__*/React.createElement("span", {
    className: "sec-chev" + (open ? "" : " shut"),
    style: {
      margin: "0 4px 2px 2px"
    }
  })), open ? children : null);
};

// ---------- App ----------
const NAV = [["today", "Today", null], ["myteam", "My Team", null], ["matchup", "Matchup", null], ["moves", "Moves", [["advice", "Advice"], ["planner", "Planner"], ["goalies", "Goalie streams"], ["adddrop", "Add / Drop"], ["players", "Players"], ["trades", "Trades"], ["playoffs", "Playoffs"]]], ["teams", "Teams", null], ["lines", "Lines", null], ["league", "League", [["power", "Power rankings"], ["standings", "Standings"], ["odds", "Betting lines"]]], ["news", "News", null], ["setup", "Setup", [["settings", "Settings & backup"], ["sched", "Schedule & weeks"], ["bulk", "Bulk update"], ["inj", "Injury overrides"]]]];
function livePP1(E) {
  const L = window.LINES_DATA;
  if (!L || !L.teams || !E || !E.players || !window.__SIG) return;
  const k = x => (x || "").normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase().replace(/[.'’]/g, "").replace(/-/g, " ").replace(/\s+/g, " ").trim();
  const byT = {},
    byN = {};
  E.players.forEach(p => {
    if (!p.n) return;
    const n = k(p.n);
    byT[n + "|" + p.t] = String(p.id);
    byN[n] = byN[n] === undefined ? String(p.id) : null;
  });
  const idOf = (n, t) => byT[k(n) + "|" + t] || byN[k(n)] || null;
  const units = {},
    on = {},
    changes = {};
  Object.entries(L.teams).forEach(([t, x]) => {
    const u = ((x || {}).lines || {}).PP1 || [];
    units[t] = u;
    u.forEach(n => {
      const id = idOf(n, t);
      if (id) on[id] = true;
    });
  });
  const since = Date.now() - 36 * 3600 * 1000;
  [...(L.changes || [])].reverse().forEach(c => {
    if (c.type !== "pp" || Date.parse(c.at) < since) return;
    const id = idOf(c.name, c.team) || (c.e ? String(c.e) : null);
    if (id) changes[id] = c.dir === "up" ? "added" : "removed";
  });
  Object.keys(changes).forEach(id => {
    if (changes[id] === "removed" === !!on[id]) delete changes[id];
  });
  window.__SIG = {
    ...window.__SIG,
    pp1: {
      asof: new Date(L.lines_at || L.generated).toLocaleString([], {
        month: "short",
        day: "numeric",
        hour: "numeric",
        minute: "2-digit"
      }),
      on,
      changes,
      units
    }
  };
}
function App() {
  const [s, setS] = useState(init);
  const [tab, setTab] = useState("myteam");
  const [subs, setSubs] = useState({
    moves: "advice",
    league: "power",
    setup: "settings"
  });
  const [loaded, setLoaded] = useState(false);
  const [status, setStatus] = useState("");
  const [syncMsg, setSyncMsg] = useState("");
  const [teamView, setTeamView] = useState(null);
  const [prevTab, setPrevTab] = useState(null);
  const [player, setPlayer] = useState(null);
  const [tradePartner, setTradePartner] = useState(null);
  const [, tick] = useState(0);
  useEffect(() => {
    const h32 = () => tick(x => x + 1);
    window.addEventListener("gm-theme", h32);
    return () => window.removeEventListener("gm-theme", h32);
  }, []);
  useEffect(() => {
    // round 21: live NHL scores straight from the NHL every minute (falls back to the sync's copy if blocked)
    let dead = false;
    const AL = {
      LAK: "LA",
      NJD: "NJ",
      SJS: "SJ",
      TBL: "TB",
      UTAH: "UTA",
      ARI: "UTA"
    };
    const pull = () => fetch("https://api-web.nhle.com/v1/score/now").then(r => r.ok ? r.json() : null).then(js => {
      if (dead || !js || !js.games) return;
      const out = {};
      js.games.forEach(g => {
        const d = g.gameDate;
        if (!d) return;
        const st = g.gameState,
          s = st === "FINAL" || st === "OFF" ? "F" : st === "LIVE" || st === "CRIT" ? "L" : "P";
        const pd = g.periodDescriptor || {},
          n = pd.number || 1,
          ck = g.clock || {};
        const rem = ck.secondsRemaining == null ? 1200 : ck.secondsRemaining;
        const f = s === "F" ? 1 : s === "P" ? 0 : Math.min(0.99, ((n - 1) * 1200 + 1200 - rem) / 3600);
        const per = pd.periodType === "OT" ? "OT" : pd.periodType === "SO" ? "SO" : ["", "1st", "2nd", "3rd"][n] || String(n);
        const hs = (g.homeTeam || {}).score,
          as = (g.awayTeam || {}).score;
        out[d] = out[d] || {};
        [[g.homeTeam, hs, as], [g.awayTeam, as, hs]].forEach(([T, my, op]) => {
          const a = T && (AL[T.abbrev] || T.abbrev);
          if (a) out[d][a] = {
            s,
            f,
            my,
            op,
            per,
            clk: ck.timeRemaining || "",
            int: !!ck.inIntermission
          };
        });
      });
      window.__LP120 = Date.now();
      window.__LIVEANY120 = js.games.some(g => g.gameState === "LIVE" || g.gameState === "CRIT" || (g.gameState === "FUT" || g.gameState === "PRE") && g.startTimeUTC && Date.parse(g.startTimeUTC) - Date.now() < 15 * 60e3);
      const sg120 = JSON.stringify(out);
      window.__LIVESC = out;
      if (sg120 !== window.__LSG120) {
        window.__LSG120 = sg120;
        tick(x => x + 1);
      }
      if (window.gxLive120) window.gxLive120(js, () => tick(x => x + 1));
    }).catch(() => {});
    pull();
    const id = setInterval(() => {
      if (document.hidden) return;
      if (window.__LIVEANY120 || Date.now() - (window.__LP120 || 0) > 59000) pull();
    }, 15 * 1000); /* gx120 */
    return () => {
      dead = true;
      clearInterval(id);
    };
  }, []);
  useEffect(() => {
    let st = init();
    try {
      const v = JSON.parse(localStorage.getItem(KEY) || "null");
      if (v && v.players && v.weeks) st = migrate(v);
    } catch (e) {}
    const E = window.ESPN_DATA;
    if (E && E.generated && E.generated !== st.lastSync) {
      try {
        st = applyESPN(st, E);
        setSyncMsg("Updated");
      } catch (e) {
        setSyncMsg("ESPN file problem: " + e.message);
      }
    }
    setS(st);
    setLoaded(true);
  }, []);
  useEffect(() => {
    if (!loaded) return;
    const id = setInterval(() => {
      const sc = document.createElement("script");
      sc.src = "espn-data.js?t=" + Date.now();
      sc.onload = () => {
        sc.remove();
        const E = window.ESPN_DATA;
        if (!E || !E.generated || E.generated === window.__GX102G) return;
        window.__GX102G = E.generated;
        tick(x => x + 1);
        setS(st => {
          if (E.generated === st.lastSync) return st;
          try {
            const n = applyESPN(st, E);
            setSyncMsg("Auto-updated " + new Date().toLocaleTimeString([], {
              hour: "numeric",
              minute: "2-digit"
            }));
            return n;
          } catch (e) {
            return st;
          }
        });
      };
      sc.onerror = () => sc.remove();
      document.head.appendChild(sc);
      const ls = document.createElement("script");
      ls.src = "lines-data.js?t=" + Date.now();
      ls.onload = ls.onerror = () => ls.remove();
      document.head.appendChild(ls);
    }, 2 * 60 * 1000);
    return () => clearInterval(id);
  }, [loaded]);
  useEffect(() => {
    if (!loaded) return;
    const t = setTimeout(() => {
      try {
        localStorage.setItem(KEY, JSON.stringify(s));
        setStatus("Saved");
      } catch (e) {
        setStatus("Save failed");
      }
    }, 700);
    return () => clearTimeout(t);
  }, [s, loaded]);
  const E = window.ESPN_DATA;
  window.__MODEL = E && E.model || null;
  window.__SIG = E && E.signals || null;
  livePP1(E);
  window.__PLAYERS = s.players;
  useEffect(() => {
    fetch("ai/models/ai_proj.json?t=" + Date.now()).then(r => r.ok ? r.json() : null).then(A => {
      if (!A || !A.proj || !((Date.now() - Date.parse(A.asof)) / 36e5 < 36)) return;
      const avg = {};
      Object.entries(A.proj).forEach(([id, m]) => {
        const v = Object.values(m).filter(x => x != null);
        if (v.length) avg[id] = v.reduce((a, b) => a + b, 0) / v.length;
      });
      window.__AI = A;
      window.__AIAVG = avg;
      setS(st => ({
        ...st,
        players: [...st.players]
      }));
    }).catch(() => {});
  }, []);
  // change 072 (gx072-app): keep the address bar in step with the page, and follow Back and Forward
  window.__ROUTE = {
    tab,
    sub: subs[tab],
    team: tab === "teams" ? teamView : null
  };
  const gxWant = React.useRef(null);
  useEffect(() => {
    if (!loaded) return;
    const apply = () => {
      const r = gxParseHash(window.location.hash);
      if (!r) return;
      const pl = r.pid ? (window.__PLAYERS || []).find(p => p.id === r.pid) || null : null;
      const want = gxHash(r.tab, r.sub, r.team, pl ? pl.id : null);
      gxWant.current = want;
      setTimeout(() => {
        if (gxWant.current === want) gxWant.current = null;
      }, 1500);
      setTab(r.tab);
      if (r.sub) setSubs(x => ({
        ...x,
        [r.tab]: r.sub
      }));
      setTeamView(r.tab === "teams" ? r.team : null);
      setPlayer(pl);
    };
    apply();
    window.addEventListener("popstate", apply);
    return () => window.removeEventListener("popstate", apply);
  }, [loaded]);
  useEffect(() => {
    if (!loaded) return;
    const h = gxHash(tab, subs[tab], tab === "teams" ? teamView : null, player ? player.id : null);
    if (gxWant.current) {
      if (h === gxWant.current) gxWant.current = null;
      return;
    }
    if (window.location.hash === h) return;
    try {
      if (!window.location.hash) window.history.replaceState(null, "", h);else window.history.pushState(null, "", h);
    } catch (e) {}
  }, [loaded, tab, subs[tab], teamView, player ? player.id : null]);
  window.__PMODE = window.__MODEL ? s.pmode || "blend" : "espn";
  window.__GOALIES = useMemo(() => {
    const o = {};
    Object.entries(s.goalies || {}).forEach(([d, m]) => {
      o[d] = {};
      Object.entries(m || {}).forEach(([n, v]) => {
        o[d][nrm(n)] = v;
      });
    });
    return o;
  }, [s.goalies]);
  const w0 = s.weeks[s.wk] || s.weeks[0];
  const wk = useMemo(() => deriveWeek(w0, s.autoDone), [w0, s.autoDone]);
  const setWk = patch => setS(st => ({
    ...st,
    weeks: st.weeks.map((w, i) => i === st.wk ? {
      ...w,
      ...(typeof patch === "function" ? patch(w) : patch)
    } : w)
  }));
  const go = (t, sub, extra) => {
    setTab(t);
    setPlayer(null);
    if (sub) setSubs(x => ({
      ...x,
      [t]: sub
    }));
    if (extra && extra.partner) setTradePartner(extra.partner);
    if (t === "teams") setTeamView(null);
    window.scrollTo(0, 0);
  };
  const openTeam = id => {
    setPlayer(null);
    if (!id || id === "fa") {
      go("moves", "adddrop");
      return;
    }
    if (id === s.me) {
      go("myteam");
      return;
    }
    setPrevTab(tab === "teams" ? null : tab);
    setTeamView(id);
    setTab("teams");
    window.scrollTo(0, 0);
  };
  const backFromTeam = () => {
    setTeamView(null);
    if (prevTab) setTab(prevTab);
    window.scrollTo(0, 0);
  };
  window.__NAV = {
    team: openTeam,
    player: p => {
      if (p) setPlayer(p);
    },
    lines: t => {
      window.__LINES_TEAM = t;
      go("lines");
      try {
        window.dispatchEvent(new CustomEvent("gm-lines-team", {
          detail: t
        }));
      } catch (e) {}
    }
  };
  window.__TAB = tab + (subs[tab] ? "/" + subs[tab] : "");
  if (!loaded) return /*#__PURE__*/React.createElement("div", {
    className: "p-8 text-slate-500"
  }, "Loading your league\u2026");
  window.__SC120 = s.sc;
  const P = {
    s,
    setS,
    wk,
    setWk,
    go
  };
  const LH = {
    gState,
    actDay,
    LiveTag,
    pStat,
    gScore,
    effAvg,
    sigOf,
    Tags,
    avail,
    effBack,
    gStart,
    teamName,
    f1,
    Section,
    Card,
    Pills,
    inp,
    SCHED,
    todayISO,
    dayLabel,
    TL,
    TeamLogo
  };
  const genAt = E && toDate(E.generated);
  const ageH = genAt ? (Date.now() - genAt.getTime()) / 36e5 : null;
  const nav = NAV.find(n => n[0] === tab);
  const sub = subs[tab];
  let content = null;
  if (tab === "today" || tab === "myteam") content = /*#__PURE__*/React.createElement("div", {
    className: "space-y-4"
  }, /*#__PURE__*/React.createElement(Today, _extends({}, P, {
    top103: true
  })), /*#__PURE__*/React.createElement(MyTeam, P));else if (tab === "myteam") content = /*#__PURE__*/React.createElement(MyTeam, P);else if (tab === "matchup") content = /*#__PURE__*/React.createElement("div", {
    className: "space-y-4"
  }, /*#__PURE__*/React.createElement(Matchup, P));else if (tab === "teams") content = teamView ? /*#__PURE__*/React.createElement(TeamPage, _extends({}, P, {
    id: teamView,
    back: backFromTeam
  })) : /*#__PURE__*/React.createElement(TeamsTab, _extends({}, P, {
    openTeam: openTeam
  }));else if (tab === "lines") content = true ? /*#__PURE__*/React.createElement(GxLines111, P) : window.LinesTab ? /*#__PURE__*/React.createElement(window.LinesTab, _extends({}, P, {
    H: LH
  })) : /*#__PURE__*/React.createElement("div", {
    className: "text-slate-400 p-4"
  }, "The Lines tab could not load (lines-tab.js). Refresh the page; if it keeps happening, check that lines-tab.js is in the repo.");else if (tab === "news") content = /*#__PURE__*/React.createElement("div", {
    className: "space-y-4"
  }, /*#__PURE__*/React.createElement(NewsView, {
    s: s,
    wk: wk
  }), /*#__PURE__*/React.createElement(PhoneFeed, null));else if (tab === "moves") content = sub === "allp" ? /*#__PURE__*/React.createElement("div", {
    className: "space-y-3"
  }, /*#__PURE__*/React.createElement(GxFaToggle105, {
    cur: "allp",
    go: go
  }), /*#__PURE__*/React.createElement(GxRankings, P)) : sub === "planner" ? /*#__PURE__*/React.createElement(PlannerAll, P) : sub === "goalies" ? /*#__PURE__*/React.createElement(GoalieStreams, P) : sub === "injuries" ? /*#__PURE__*/React.createElement(GxInj109, P) : sub === "adddrop" ? /*#__PURE__*/React.createElement(Pickups, P) : sub === "players" ? /*#__PURE__*/React.createElement(Players, P) : sub === "trades" ? /*#__PURE__*/React.createElement(TradesPanel, _extends({
    key: tradePartner || "none"
  }, P, {
    initPartner: tradePartner
  })) : sub === "playoffs" ? /*#__PURE__*/React.createElement(PlayoffPlanner, P) : /*#__PURE__*/React.createElement(AdviceAll, P);else if (tab === "league") content = sub === "playoffs" ? /*#__PURE__*/React.createElement(PlayoffPlanner, P) : sub === "players" ? /*#__PURE__*/React.createElement(GxRankings, P) : /*#__PURE__*/React.createElement("div", {
    className: "space-y-4"
  }, /*#__PURE__*/React.createElement(LeaguePage, P), /*#__PURE__*/React.createElement(GxPlayoff, {
    s: s
  }));else if (tab === "setup") content = sub === "sched" ? /*#__PURE__*/React.createElement(Schedule, P) : sub === "bulk" ? /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement(Bulk, {
    s: s,
    setS: setS
  }), /*#__PURE__*/React.createElement(AddOne, P)) : sub === "inj" ? /*#__PURE__*/React.createElement(InjuryPanel, P) : sub === "odds" ? /*#__PURE__*/React.createElement(OddsBoard, {
    s: s
  }) : sub === "alerts" ? /*#__PURE__*/React.createElement(GxAlertsPage, P) : sub === "autopilot" ? /*#__PURE__*/React.createElement(GxAutoPage, P) : /* gx091 */sub === "adv" ? /*#__PURE__*/React.createElement(Settings, P) : /*#__PURE__*/React.createElement(SetupPage, _extends({}, P, {
    sub: sub
  }));
  return /*#__PURE__*/React.createElement("div", {
    className: "min-h-screen bg-slate-100 text-slate-900"
  }, /*#__PURE__*/React.createElement("div", {
    className: "sticky top-0 z-30 bg-slate-900 border-b border-slate-800"
  }, /*#__PURE__*/React.createElement(GxTopM103, {
    s: s,
    tab: tab,
    go: go,
    ageH: ageH
  }), /*#__PURE__*/React.createElement(TopBar, {
    s: s,
    setS: setS,
    tab: tab,
    go: go,
    ageH: ageH
  })), ageH !== null && ageH > 2 && /*#__PURE__*/React.createElement("div", {
    className: "bg-red-600 text-white text-sm px-4 py-2 text-center"
  }, "Data is ", Math.round(ageH), " hours old \u2014 the automatic sync may have stopped. Check GitHub \u2192 Actions for a red \u2715."), /*#__PURE__*/React.createElement("div", {
    className: "max-w-6xl mx-auto px-3 py-4"
  }, /*#__PURE__*/React.createElement(GxSimBar, {
    s: s,
    setS: setS,
    go: go
  }), /*#__PURE__*/React.createElement(GxSubBar103, {
    tab: tab,
    sub: sub,
    go: go,
    s: s,
    wk: wk
  }), /*#__PURE__*/React.createElement(GxExtras, {
    s: s,
    tab: tab,
    go: go
  }), /*#__PURE__*/React.createElement(GxQA, {
    s: s,
    go: go
  }), /*#__PURE__*/React.createElement(GxBest, {
    s: s,
    setS: setS
  }), /*#__PURE__*/React.createElement(GxSync, {
    s: s,
    setS: setS
  }), /*#__PURE__*/React.createElement("div", {
    key: tab + "/" + (sub || ""),
    className: "gx-pg101"
  }, content), false && window.AskPanel ? /*#__PURE__*/React.createElement(window.AskPanel, _extends({}, P, {
    tab: tab,
    H: {
      effAvg,
      sigOf,
      tags,
      avail,
      effBack,
      gStart,
      teamName,
      f1,
      computeMoves,
      weekProj,
      oppOf,
      todayISO
    }
  })) : null), player ? /*#__PURE__*/React.createElement(GxPdSafe, {
    key: player.id,
    p: player,
    s: s,
    wk: wk,
    H: LH,
    onClose: () => setPlayer(null)
  }) : null);
}

// ---------- Today ----------
function Today({
  s,
  wk,
  go,
  top103
}) {
  // today v32: score with win ring, week chart, next week (news_logos.py)
  // older done markers kept so earlier rounds stay finished:
  // old or minor headline
  // chance to win</span>
  // <WinDelta s={s} add={r.f} drop={r.d} /><span
  // <StrategyLine
  // still projected · {f1(fa)} final est.</div>
  // still projected · {f1(fb)} final est.</div>
  // PickNote where="today"
  // "Best moves for next week" : "Best moves this week"} sub={sameDrop ?
  // <PlanNote sP={sP} /> : <PickNote where="today" />
  // <WinDelta s={sP} add={r.f} drop={r.d} base={pBase} />
  // <div className="hidden">+ {f1(A.total)} still projected
  // <div className="hidden">+ {f1(B.total)} still projected
  // round 28: advice sentence removed
  // L.empty > 0 && !outOfMoves(s)
  // "Injuries" + (outNow.length
  // "News on your players" + (news.length
  // Section: SectionShut
  // computeMoves(sP, { H: 1, pool: 40 })
  const K = s.blend;
  const opp = oppOf(wk, s.me) || s.opp;
  const mine = s.players.filter(p => p.ft === s.me),
    theirs = s.players.filter(p => p.ft === opp);
  const A = weekLive(mine, wk, K, s.me),
    B = weekLive(theirs, wk, K, opp);
  const aA = +gxAct120(wk)[s.me] || 0,
    aB = +gxAct120(wk)[opp] || 0;
  const fa = aA + A.total,
    fb = aB + B.total,
    margin = fa - fb,
    ahead = margin >= 0;
  const dates = wk.dates || [],
    n = dates.length,
    today = todayISO(),
    done = wk.done || 0;
  const over = n > 0 && done >= n;
  const wp = winProb(A, B, aA, aB);
  const sN = useMemo(() => nextWkS(s), [s]);
  const sP = useMemo(() => planS(s), [s]);
  // change 071: next week win chance no longer needed on Today

  const tag = "Week " + (s.wk + 1) + (!n ? "" : dates[0] > today ? " \u00b7 starts " + dayLabel(dates[0]) : over ? " \u00b7 final" : " \u00b7 day " + Math.min(n, done + 1) + " of " + n);
  const share = aA + aB > 0 ? Math.max(4, Math.min(96, aA / (aA + aB) * 100)) : 50;
  const big = {
    fontSize: "clamp(28px, 7vw, 40px)"
  };
  return /*#__PURE__*/React.createElement("div", {
    className: "space-y-3"
  }, /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    className: "gx-tag"
  }, tag), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "grid",
      gridTemplateColumns: "minmax(0,1fr) 104px minmax(0,1fr)",
      alignItems: "center",
      marginTop: 6
    }
  }, /*#__PURE__*/React.createElement("div", {
    className: "min-w-0"
  }, /*#__PURE__*/React.createElement("div", {
    className: "text-sm font-semibold truncate",
    style: {
      color: "var(--accent)"
    }
  }, teamName(s, s.me)), /*#__PURE__*/React.createElement("div", {
    className: "gx-num",
    style: big
  }, f1(aA))), /*#__PURE__*/React.createElement("button", {
    type: "button",
    title: "Open the matchup",
    onClick: () => go("matchup")
  }, /*#__PURE__*/React.createElement(GxRing, {
    v: wp,
    big: true
  })), /*#__PURE__*/React.createElement("div", {
    className: "min-w-0 text-right"
  }, /*#__PURE__*/React.createElement("div", {
    className: "text-sm text-slate-500 truncate"
  }, /*#__PURE__*/React.createElement(TL, {
    s: s,
    id: opp
  })), /*#__PURE__*/React.createElement("div", {
    className: "gx-num",
    style: {
      ...big,
      color: "var(--ink2)"
    }
  }, f1(aB)))), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      height: 4,
      gap: 3,
      marginTop: 10
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      width: share + "%",
      background: "var(--accent)"
    }
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      flex: 1,
      background: "var(--track)"
    }
  })), /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500",
    style: {
      display: "flex",
      marginTop: 6
    }
  }, /*#__PURE__*/React.createElement("span", null, (over ? "Final " : "Projected ") + Math.round(fa)), /*#__PURE__*/React.createElement("span", {
    style: {
      margin: "0 auto"
    }
  }), /*#__PURE__*/React.createElement("span", null, Math.round(fb)))), /*#__PURE__*/React.createElement(GxAutoToday2, {
    go: go
  }), /*#__PURE__*/React.createElement(GxRace, {
    s: s,
    wk: wk
  }), top103 ? null : /*#__PURE__*/React.createElement(GxHome, {
    s: s,
    wk: wk,
    A: A,
    B: B
  }));
}
function NewsView({
  s,
  wk
}) {
  const [f, setF] = useState("all");
  const [open, setOpen] = useState({});
  const opp = wk ? oppOf(wk, s.me) : null;
  const pass = n => f === "all" || (f === "inj" ? NEWS_OUT.has(n.kind) : f === "moves" ? n.kind === "trade" || n.kind === "roster" : n.kind === "hot");
  const rows = s.players.map(p => ({
    p,
    items: newsOf(p).filter(pass)
  })).filter(x => x.items.length).sort((a, b) => NEWS_RANK[a.items[0].kind] - NEWS_RANK[b.items[0].kind] || a.items[0].age - b.items[0].age);
  const only = (list, keep) => list.map(x => ({
    ...x,
    items: x.items.filter(keep)
  })).filter(x => x.items.length);
  const groups = [["mine", "Your players", "Regular news shows for a day, hot streaks for 3 days, and injuries, scratches, trades and roster moves for a week.", rows.filter(x => x.p.ft === s.me), true], ["opp", opp ? "Your opponent · " + teamName(s, opp) : "", "Everything current on the team you play this week.", opp ? rows.filter(x => x.p.ft === opp) : [], false], ["league", "Around your league", "Other fantasy teams: important news and hot streaks only.", only(rows.filter(x => x.p.ft !== s.me && x.p.ft !== opp && x.p.ft !== "fa"), n => n.kind !== "news"), false], ["fa", "Free agents", "Only important news: injuries, scratches, trades and roster moves.", only(rows.filter(x => x.p.ft === "fa"), n => NEWS_BIG.has(n.kind)), false]];
  return /*#__PURE__*/React.createElement("div", {
    className: "space-y-4"
  }, /*#__PURE__*/React.createElement(Pills, {
    items: [["all", "All"], ["inj", "Injuries & scratches"], ["moves", "Trades & roster moves"], ["hot", "Hot"]],
    value: f,
    onChange: setF
  }), !window.__SIG && /*#__PURE__*/React.createElement("div", {
    className: box + " text-slate-400"
  }, "No news loaded yet."), groups.filter(g => g[4] || g[3].length).map(([k, title, sub, list]) => {
    const shown = open[k] ? list : list.slice(0, 8);
    return /*#__PURE__*/React.createElement(Section, {
      key: k,
      title: title + " (" + list.length + ")",
      sub: sub
    }, shown.length ? shown.map(({
      p,
      items
    }) => /*#__PURE__*/React.createElement("div", {
      key: p.id,
      className: "flex gap-3 py-2.5 border-t border-slate-100"
    }, /*#__PURE__*/React.createElement("div", {
      className: "pt-0.5"
    }, /*#__PURE__*/React.createElement(GxFace, {
      p: p,
      size: 36
    })), /*#__PURE__*/React.createElement("div", {
      className: "min-w-0 flex-1"
    }, /*#__PURE__*/React.createElement("div", {
      className: "flex flex-wrap items-baseline gap-2"
    }, /*#__PURE__*/React.createElement(PN, {
      p: p
    }), /*#__PURE__*/React.createElement("span", {
      className: "text-xs text-slate-400"
    }, p.p, " \xB7 ", /*#__PURE__*/React.createElement(TL, {
      s: s,
      id: p.ft
    }))), items.slice(0, 2).map((n, i) => /*#__PURE__*/React.createElement(NewsItem, {
      key: i,
      n: n
    }))))) : /*#__PURE__*/React.createElement("div", {
      className: "text-slate-400 text-xs"
    }, "Nothing current."), list.length > shown.length && /*#__PURE__*/React.createElement("button", {
      className: "text-sm text-blue-600 mt-2",
      onClick: () => setOpen({
        ...open,
        [k]: true
      })
    }, "Show all ", list.length));
  }));
}

// ---------- Betting lines ----------
const oddsFor = (t, dt) => {
  const O = ((window.ESPN_DATA || {}).model || {}).odds || {};
  return dt && O[dt] ? O[dt][t] || null : null;
};
function OddsBoard({
  s
}) {
  const O = ((window.ESPN_DATA || {}).model || {}).odds || null;
  const today = todayISO();
  const w = deriveWeek(s.weeks[s.wk] || s.weeks[0], s.autoDone);
  const opp = oppOf(w, s.me);
  const count = (tid, team) => s.players.filter(p => p.ft === tid && p.t === team && !p.ir).length;
  if (!O || !Object.keys(O).length) return /*#__PURE__*/React.createElement("div", {
    className: box + " text-slate-400"
  }, "No betting lines in the data yet \u2014 run the sync.");
  const days = Object.keys(O).filter(d => d >= today).sort();
  return /*#__PURE__*/React.createElement("div", {
    className: "space-y-4"
  }, /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500"
  }, "Win chance (bookmaker margin removed) and expected goals per team, refreshed every 4 hours. Used by the GM model and shown on the Matchup tab as \"W %\" (goalies) and \"xG\" (skaters). Rows with your players are highlighted."), days.map(d => {
    const games = Object.entries(O[d]).filter(([, v]) => v.home);
    return /*#__PURE__*/React.createElement("div", {
      key: d,
      className: "bg-white rounded-xl border border-slate-200 overflow-x-auto"
    }, /*#__PURE__*/React.createElement("div", {
      className: "px-4 py-2 border-b border-slate-200 font-semibold text-sm"
    }, dayLabel(d), " \xB7 ", games.length, " games"), /*#__PURE__*/React.createElement("table", {
      className: "w-full text-sm"
    }, /*#__PURE__*/React.createElement("thead", {
      className: "text-left"
    }, /*#__PURE__*/React.createElement("tr", null, ["Game", "Win chance", "Expected goals", "Total", "Yours", opp ? teamName(s, opp) : "Opponent"].map(h => /*#__PURE__*/React.createElement("th", {
      key: h,
      className: "px-3 py-2"
    }, h)))), /*#__PURE__*/React.createElement("tbody", null, games.map(([home, v]) => {
      const a = O[d][v.opp] || {};
      const mineN = count(s.me, home) + count(s.me, v.opp),
        oppN = opp ? count(opp, home) + count(opp, v.opp) : 0;
      const fav = v.win >= 0.5 ? home : v.opp;
      return /*#__PURE__*/React.createElement("tr", {
        key: home,
        className: "border-t border-slate-100 " + (mineN ? "bg-blue-50" : "")
      }, /*#__PURE__*/React.createElement("td", {
        className: "px-3 py-2 font-medium whitespace-nowrap"
      }, /*#__PURE__*/React.createElement("span", {
        className: "inline-flex items-center gap-1.5"
      }, /*#__PURE__*/React.createElement(TeamLogo, {
        t: v.opp,
        size: 18
      }), v.opp, " @ ", /*#__PURE__*/React.createElement(TeamLogo, {
        t: home,
        size: 18
      }), home)), /*#__PURE__*/React.createElement("td", {
        className: "px-3 py-2 whitespace-nowrap"
      }, /*#__PURE__*/React.createElement("span", {
        className: fav === v.opp ? "font-semibold text-green-700" : ""
      }, v.opp, " ", Math.round((a.win ?? 1 - v.win) * 100), "%"), " \xB7 ", /*#__PURE__*/React.createElement("span", {
        className: fav === home ? "font-semibold text-green-700" : ""
      }, home, " ", Math.round(v.win * 100), "%")), /*#__PURE__*/React.createElement("td", {
        className: "px-3 py-2 whitespace-nowrap"
      }, v.opp, " ", (a.gf ?? v.ga).toFixed(1), " \xB7 ", home, " ", v.gf.toFixed(1)), /*#__PURE__*/React.createElement("td", {
        className: "px-3 py-2"
      }, (v.gf + v.ga).toFixed(1)), /*#__PURE__*/React.createElement("td", {
        className: "px-3 py-2"
      }, mineN ? /*#__PURE__*/React.createElement("span", {
        className: "text-blue-700 font-semibold"
      }, mineN) : "–"), /*#__PURE__*/React.createElement("td", {
        className: "px-3 py-2"
      }, oppN || "–"));
    }))));
  }));
}

// ---------- Weekly acquisition planner ----------
function buildPlan(s, wk, d0, M) {
  const K = s.blend,
    nD = wk.days.length;
  const mins = {
    F: s.minF ?? 10,
    D: s.minD ?? 5,
    G: s.minGo ?? 2
  };
  const minGain = s.minGain ?? 3;
  const myR = s.players.filter(p => p.ft === s.me);
  const ranked = myR.filter(p => !p.ir).sort((a, b) => gxPgAvg(b, K) - gxPgAvg(a, K)); /* gx088-a */
  const prot = new Set([...ranked.slice(0, s.protectTop ?? 8).map(p => p.id), ...myR.filter(p => p.keep).map(p => p.id)]);
  const val = (p, a) => (wk.games[p.t] || []).filter(d => d >= a).reduce((t, d) => {
    const dt = wk.dates[d];
    return t + effAvg(p, K, dt) * (p.p === "G" ? gStart(p, dt).v : p.prob) * avail(p, dt);
  }, 0);
  const dayTotal = (tl, d) => dayLineup(tl.filter(x => x.from <= d && x.to >= d).map(x => x.p), wk, d, K).total;
  let tl = myR.map(p => ({
    p,
    from: 0,
    to: nD - 1,
    orig: true
  }));
  const fas = s.players.filter(p => p.ft === "fa" && p.prob > 0 && (p.proj !== false || p.gp > 0) && !goalieOut(p)).map(p => ({
    p,
    v: val(p, d0)
  })).filter(x => x.v > 0).sort((a, b) => b.v - a.v).slice(0, 45).map(x => x.p);
  let base0 = 0;
  for (let d = d0; d < nD; d++) base0 += dayTotal(tl, d);
  const steps = [],
    usedFA = new Set();
  for (let k = 0; k < M; k++) {
    const cur = [];
    for (let d = d0; d < nD; d++) cur[d] = dayTotal(tl, d);
    const suffix = a => {
      let t = 0;
      for (let d = a; d < nD; d++) t += cur[d];
      return t;
    };
    let best = null;
    for (let d = d0; d < nD; d++) {
      const active = tl.filter(x => x.from <= d && x.to >= d);
      const cnt = {
        F: 0,
        D: 0,
        G: 0
      };
      active.forEach(x => {
        if (!x.p.ir) cnt[x.p.p]++;
      });
      const drops = active.filter(x => !x.p.ir && x.to === nD - 1 && x.from < d + (x.orig ? 1 : 0) && !(x.orig && prot.has(x.p.id)) && !(!x.orig && x.from >= d)).map(x => ({
        x,
        v: val(x.p, d)
      })).sort((a, b) => a.v - b.v);
      const cand = [];
      ["F", "D", "G"].forEach(ps => drops.filter(y => y.x.p.p === ps).slice(0, 4).forEach(y => cand.push(y.x)));
      const before = suffix(d);
      for (const f of fas) {
        if (usedFA.has(f.id) || !(wk.games[f.t] || []).includes(d) || wk.dates[d] < pickStart(f)) continue;
        for (const x of cand) {
          if (x.p.p !== f.p && cnt[x.p.p] - 1 < mins[x.p.p]) continue;
          const tl2 = tl.map(y => y === x ? {
            ...y,
            to: d - 1
          } : y).concat([{
            p: {
              ...f,
              ft: s.me
            },
            from: d,
            to: nD - 1,
            orig: false
          }]);
          let after = 0;
          for (let dd = d; dd < nD; dd++) after += dayTotal(tl2, dd);
          const gain = after - before;
          if (!best || gain > best.gain) best = {
            gain,
            d,
            f,
            x,
            tl2
          };
        }
      }
    }
    if (!best || best.gain < minGain) break;
    steps.push({
      day: best.d,
      add: best.f,
      drop: best.x.p,
      dropWasStream: !best.x.orig,
      gain: best.gain
    });
    usedFA.add(best.f.id);
    tl = best.tl2;
  }
  let final = 0;
  for (let d = d0; d < nD; d++) final += dayTotal(tl, d);
  return {
    steps: steps.sort((a, b) => a.day - b.day),
    gain: final - base0,
    base: base0,
    final,
    pool: fas.length,
    d0
  };
}
// ---------- Playoff planner ----------
function PlayoffPlanner({
  s,
  setS
}) {
  const K = s.blend;
  const st = s.poStart ?? 24,
    nW = s.poWeeks ?? 3;
  const [who, setWho] = useState("fa");
  const [pos, setPos] = useState("all");
  const [q, setQ] = useState("");
  const [showTeams, setShowTeams] = useState(false);
  const weeks = useMemo(() => s.weeks.slice(st, st + nW).map(w => deriveWeek(w, false)), [s.weeks, st, nW]);
  const dates = weeks.flatMap(w => w.dates || []);
  const perDay = {};
  dates.forEach(d => perDay[d] = NHL.filter(t => SCHED[t] && SCHED[t].has(d)).length / 2);
  const light = new Set(dates.filter(d => perDay[d] > 0 && perDay[d] <= 5));
  const teamRows = NHL.map(t => {
    const per = weeks.map(w => gms(w, t));
    const tot = per.reduce((a, b) => a + b, 0);
    const off = dates.filter(d => light.has(d) && SCHED[t].has(d)).length;
    return {
      t,
      per,
      tot,
      off
    };
  }).sort((a, b) => b.tot - a.tot || b.off - a.off);
  const avgGames = teamRows.reduce((a, r) => a + r.tot, 0) / teamRows.length;
  const tg = {};
  teamRows.forEach(r => tg[r.t] = r);
  const val = p => {
    let v = 0;
    dates.forEach(d => {
      if (SCHED[p.t] && SCHED[p.t].has(d)) v += effAvg(p, K, d) * p.prob * avail(p, d);
    });
    return v;
  };
  const [sp79, setSp79] = useState("v"); // change 079: tap a heading to sort
  const pk79 = x => sp79[0] === "w" ? x.per[+sp79.slice(1)] || 0 : sp79 === "avg" ? effAvg(x.p, K) : x[sp79] || 0;
  const rows = useMemo(() => s.players.filter(p => (who === "all" || (who === "fa" ? p.ft === "fa" : who === "mine" ? p.ft === s.me : p.ft !== "fa" && p.ft !== s.me)) && (pos === "all" || p.p === pos) && p.n.toLowerCase().includes(q.toLowerCase()) && p.prob > 0).map(p => {
    const v = val(p);
    const r = tg[p.t] || {
      tot: 0,
      off: 0,
      per: []
    };
    return {
      p,
      v,
      g: r.tot,
      off: r.off,
      per: r.per,
      bonus: (r.tot - avgGames) * effAvg(p, K) * p.prob
    };
  }).sort((a, b) => pk79(b) - pk79(a) || b.v - a.v).slice(0, 100), [s.players, who, pos, q, st, nW, K, sp79]);
  const league = useMemo(() => s.teams.map(t => {
    const r = s.players.filter(p => p.ft === t.id);
    return {
      t,
      tot: weeks.reduce((a, w) => a + weekProj(r, w, K, 0).total, 0)
    };
  }).sort((a, b) => b.tot - a.tot), [s.players, weeks, K]);
  const myRank = league.findIndex(x => x.t.id === s.me) + 1;
  const mine = s.players.filter(p => p.ft === s.me && !p.ir).map(p => ({
    p,
    g: (tg[p.t] || {}).tot || 0
  })).sort((a, b) => a.g - b.g);
  const weakSched = mine.filter(x => x.g <= avgGames - 1.5);
  const set = (k, v) => setS(x => ({
    ...x,
    [k]: v
  }));
  const gCls = (g, avg) => g >= avg + 1.5 ? "text-green-700 font-semibold" : g <= avg - 1.5 ? "text-red-600" : "";
  const today = todayISO();
  const deadline = "2027-02-26";
  return /*#__PURE__*/React.createElement("div", {
    className: "space-y-4"
  }, /*#__PURE__*/React.createElement(Section, {
    title: "Fantasy playoff planner",
    sub: `${weeks.length ? `${mdL(weeks[0].dates[0])} – ${mdL(dates[dates.length - 1])}` : ""} · trade deadline ${mdL(deadline)}${today <= deadline ? ` (${Math.round((fromIso(deadline) - fromIso(today)) / 864e5)} days away)` : " (passed)"}`
  }, /*#__PURE__*/React.createElement("div", {
    className: "flex flex-wrap gap-2 items-center"
  }, /*#__PURE__*/React.createElement("label", null, "Playoffs start ", /*#__PURE__*/React.createElement("select", {
    className: inp,
    value: st,
    onChange: e => set("poStart", +e.target.value)
  }, s.weeks.map((w, i) => /*#__PURE__*/React.createElement("option", {
    key: i,
    value: i
  }, w.label)))), /*#__PURE__*/React.createElement("label", null, "Weeks ", /*#__PURE__*/React.createElement("select", {
    className: inp,
    value: nW,
    onChange: e => set("poWeeks", +e.target.value)
  }, [1, 2, 3, 4].map(n => /*#__PURE__*/React.createElement("option", {
    key: n,
    value: n
  }, n))))), /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500 mt-2"
  }, "Players are valued on ", /*#__PURE__*/React.createElement("b", null, "games in your playoff weeks \xD7 projection"), ". Average team plays ", avgGames.toFixed(1), " games in this window. \"Light nights\" = 5 or fewer NHL games \u2014 easier to fit everyone into your lineup.")), /*#__PURE__*/React.createElement("div", {
    className: "grid md:grid-cols-2 gap-4"
  }, /*#__PURE__*/React.createElement(Section, {
    title: "Your playoff outlook"
  }, /*#__PURE__*/React.createElement("div", {
    className: "text-2xl font-bold"
  }, "#", myRank, " ", /*#__PURE__*/React.createElement("span", {
    className: "text-sm font-normal text-slate-500"
  }, "of ", league.length, " in projected playoff-week points")), /*#__PURE__*/React.createElement("div", {
    className: "mt-2"
  }, league.map((x, i) => /*#__PURE__*/React.createElement("div", {
    key: x.t.id,
    className: "flex justify-between py-1 border-t border-slate-100 " + (x.t.id === s.me ? "text-blue-700 font-semibold" : "")
  }, /*#__PURE__*/React.createElement("span", null, i + 1, ". ", x.t.name), /*#__PURE__*/React.createElement("span", null, f1(x.tot))))), /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500 mt-2"
  }, "Lineup-aware totals for all ", nW, " weeks with current rosters and projections.")), /*#__PURE__*/React.createElement(Section, {
    title: "Your players with weak playoff schedules"
  }, weakSched.length ? weakSched.map(({
    p,
    g
  }) => /*#__PURE__*/React.createElement("div", {
    key: p.id,
    className: "flex gap-2 py-1.5 border-t border-slate-100"
  }, /*#__PURE__*/React.createElement("span", {
    className: "font-medium"
  }, p.n), /*#__PURE__*/React.createElement("span", {
    className: "text-xs text-slate-400"
  }, p.p, " \xB7 ", /*#__PURE__*/React.createElement(GxFace, {
    p: p
  })), /*#__PURE__*/React.createElement("span", {
    className: "ml-auto text-red-600 text-xs"
  }, g, " games (", (g - avgGames).toFixed(1), " vs avg)"))) : /*#__PURE__*/React.createElement("div", {
    className: "text-green-700"
  }, "None of your players have a clearly light playoff schedule."), /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500 mt-2"
  }, "Trade candidates before the deadline \u2014 swap them for similar players with more games."))), /*#__PURE__*/React.createElement(Section, {
    title: "Playoff targets",
    sub: "Ranked by projected points in your playoff weeks. Schedule bonus = extra points from games above the average."
  }, /*#__PURE__*/React.createElement("div", {
    className: "flex flex-wrap gap-2 mb-3"
  }, /*#__PURE__*/React.createElement(Pills, {
    items: [["fa", "Free agents (stash)"], ["other", "Other teams (trade)"], ["mine", "My team"], ["all", "Everyone"]],
    value: who,
    onChange: setWho
  }), /*#__PURE__*/React.createElement("select", {
    className: inp,
    value: pos,
    onChange: e => setPos(e.target.value)
  }, /*#__PURE__*/React.createElement("option", {
    value: "all"
  }, "All positions"), /*#__PURE__*/React.createElement("option", null, "F"), /*#__PURE__*/React.createElement("option", null, "D"), /*#__PURE__*/React.createElement("option", null, "G")), /*#__PURE__*/React.createElement("input", {
    className: inp + " flex-1 min-w-[140px]",
    placeholder: "Search",
    value: q,
    onChange: e => setQ(e.target.value)
  })), /*#__PURE__*/React.createElement("div", {
    className: "overflow-x-auto"
  }, /*#__PURE__*/React.createElement("table", {
    className: "w-full text-sm"
  }, /*#__PURE__*/React.createElement("thead", {
    className: "text-left"
  }, /*#__PURE__*/React.createElement("tr", null, ["Player", "", "Owner", ...weeks.map((w, i) => `Wk ${st + i + 1}`), "Games", "Light", "Avg", "Playoff pts", "Sched bonus"].map((h, i) => {
    const k = i < 3 ? null : i < 3 + weeks.length ? "w" + (i - 3) : ["g", "off", "avg", "v", "bonus"][i - 3 - weeks.length];
    return /*#__PURE__*/React.createElement("th", {
      key: i,
      className: "px-2 py-2"
    }, k ? /*#__PURE__*/React.createElement(GxSH, {
      k: k,
      cur: sp79,
      set: setSp79,
      def: "v"
    }, h) : h);
  }))), /*#__PURE__*/React.createElement("tbody", null, rows.map(({
    p,
    v,
    g,
    off,
    per,
    bonus
  }) => /*#__PURE__*/React.createElement("tr", {
    key: p.id,
    className: "border-t border-slate-100 " + (p.ft === s.me ? "bg-blue-50" : "")
  }, /*#__PURE__*/React.createElement("td", {
    className: "px-2 py-2 font-medium whitespace-nowrap"
  }, p.n, p.ir ? /*#__PURE__*/React.createElement("span", {
    className: "text-red-600 text-xs ml-1"
  }, "IR") : ""), /*#__PURE__*/React.createElement("td", {
    className: "px-2 py-2 text-xs text-slate-500 whitespace-nowrap"
  }, p.p, " \xB7 ", /*#__PURE__*/React.createElement(GxFace, {
    p: p
  })), /*#__PURE__*/React.createElement("td", {
    className: "px-2 py-2 text-xs text-slate-500"
  }, teamName(s, p.ft)), per.map((n, i) => /*#__PURE__*/React.createElement("td", {
    key: i,
    className: "px-2 py-2 " + (n >= 4 ? "text-green-700 font-semibold" : n <= 2 ? "text-red-600" : "")
  }, n)), /*#__PURE__*/React.createElement("td", {
    className: "px-2 py-2 " + gCls(g, avgGames)
  }, g), /*#__PURE__*/React.createElement("td", {
    className: "px-2 py-2"
  }, off), /*#__PURE__*/React.createElement("td", {
    className: "px-2 py-2"
  }, f1(effAvg(p, K))), /*#__PURE__*/React.createElement("td", {
    className: "px-2 py-2 font-semibold"
  }, f1(v)), /*#__PURE__*/React.createElement("td", {
    className: "px-2 py-2 " + (bonus >= 0 ? "text-green-700" : "text-red-600")
  }, bonus >= 0 ? "+" : "", f1(bonus)))), rows.length === 0 && /*#__PURE__*/React.createElement("tr", null, /*#__PURE__*/React.createElement("td", {
    className: "px-2 py-3 text-slate-400"
  }, "No players match.")))))), /*#__PURE__*/React.createElement(Section, {
    title: "NHL team schedules in your playoff weeks",
    link: [showTeams ? "Hide" : "Show all 32 teams", () => setShowTeams(!showTeams)]
  }, /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500 mb-2"
  }, "Best: ", teamRows.slice(0, 5).map(r => `${r.t} (${r.tot})`).join(", "), " \xB7 Worst: ", teamRows.slice(-5).reverse().map(r => `${r.t} (${r.tot})`).join(", ")), showTeams && /*#__PURE__*/React.createElement("div", {
    className: "overflow-x-auto"
  }, /*#__PURE__*/React.createElement("table", {
    className: "w-full text-sm"
  }, /*#__PURE__*/React.createElement("thead", {
    className: "text-left"
  }, /*#__PURE__*/React.createElement("tr", null, ["Team", ...weeks.map((w, i) => `Wk ${st + i + 1}`), "Total", "Light-night games"].map(h => /*#__PURE__*/React.createElement("th", {
    key: h,
    className: "px-2 py-2"
  }, h)))), /*#__PURE__*/React.createElement("tbody", null, teamRows.map(r => /*#__PURE__*/React.createElement("tr", {
    key: r.t,
    className: "border-t border-slate-100"
  }, /*#__PURE__*/React.createElement("td", {
    className: "px-2 py-1.5 font-medium whitespace-nowrap"
  }, /*#__PURE__*/React.createElement("span", {
    className: "inline-flex items-center gap-1.5"
  }, /*#__PURE__*/React.createElement(TeamLogo, {
    t: r.t,
    size: 16
  }), r.t)), r.per.map((n, i) => /*#__PURE__*/React.createElement("td", {
    key: i,
    className: "px-2 py-1.5 " + (n >= 4 ? "text-green-700 font-semibold" : n <= 2 ? "text-red-600" : "")
  }, n)), /*#__PURE__*/React.createElement("td", {
    className: "px-2 py-1.5 " + gCls(r.tot, avgGames)
  }, r.tot), /*#__PURE__*/React.createElement("td", {
    className: "px-2 py-1.5"
  }, r.off))))))));
}

// ---------- Trade analyzer ----------
const rosRaw = (p, K) => {
  if (p.ir && !effBack(p).d) return 0;
  const t = todayISO();
  let v = 0;
  (SCHED[p.t] ? [...SCHED[p.t]] : []).forEach(d => {
    if (d >= t) v += effAvg(p, K, d) * p.prob * avail(p, d);
  });
  return v;
};
const horizonTotal = (roster, s, n) => {
  let t = 0;
  s.weeks.slice(s.wk, s.wk + n).forEach((w, i) => {
    const dw = deriveWeek(w, s.autoDone);
    t += weekProj(roster, dw, s.blend, i === 0 ? dw.done : 0).total;
  });
  return t;
};
function Matchup({
  s,
  setS,
  wk,
  setWk
}) {
  // matchup v35: one day at a time, head to head, swipe or arrows between matchups (news_logos.py)
  // matchup v16: older marker kept, with these done markers from earlier rounds:
  // Day difference
  // data-v="daydiff2"
  // day header: running total removed
  // label={"Win chance · "
  // data-w="daydiff3"
  // <H2H x={x}
  // <LiveTag st={tag === "LIVE" ? "L" : "F"} />
  // round 28: actual-score row removed
  // const openDay =
  // <DayFold key=
  // </DayFold>
  const K = s.blend,
    done = wk.done || 0;
  const pairOpp = oppOf(wk, s.me);
  const myPair = [s.me, pairOpp || s.opp];
  const others = (wk.pairs || []).filter(p => p[0] && p[1] && p[0] !== s.me && p[1] !== s.me);
  const all = [myPair, ...others];
  const [sel, setSel] = useState(() => {
    const v44 = window.__MATCH_SEL || 0;
    window.__MATCH_SEL = 0;
    return v44;
  });
  useEffect(() => {
    window.__matchSel = sel;
    window.__setMatch = setSel;
    window.dispatchEvent(new Event("gm-match"));
  }, [sel]);
  const [day, setDay] = useState(null);
  const touch = React.useRef(null);
  const [a, b] = all[Math.min(sel, all.length - 1)];
  const gen = (window.ESPN_DATA || {}).generated;
  const P = useMemo(() => {
    const o = {};
    [a, b].forEach(id => {
      o[id] = {
        r: weekLive(s.players.filter(p => p.ft === id), wk, K, id, {
          detail: true
        }),
        act: +gxAct120(wk)[id] || 0
      };
    });
    return o;
  }, [s.players, wk, K, done, a, b, gen, window.__LIVEV120]);
  const A = P[a].r,
    B = P[b].r,
    aA = P[a].act,
    aB = P[b].act;
  const fa = aA + A.total,
    fb = aB + B.total,
    margin = fa - fb;
  const dates = wk.dates || [],
    n = dates.length,
    today = todayISO();
  const first = dates.findIndex(x => x >= today);
  const d = Math.max(0, Math.min(n - 1, day != null ? day : first >= 0 ? first : n - 1));
  const sl105a = useSlide105(sel),
    sl105b = useSlide105(sel * 100 + d);
  const [bx118, setBx118] = useState("");
  const [dr106, dh106] = useDrag106(d > 0 ? () => setDay(d - 1) : null, d < n - 1 ? () => setDay(d + 1) : null);
  const over = n > 0 && done >= n;
  const move = k => setSel((Math.min(sel, all.length - 1) + k + all.length) % all.length);
  const onStart = e => {
    const t = e.touches[0];
    touch.current = [t.clientX, t.clientY];
  };
  const onEnd = e => {
    const t0 = touch.current,
      t = e.changedTouches[0];
    touch.current = null;
    if (!t0 || all.length < 2) return;
    const dx = t.clientX - t0[0],
      dy = t.clientY - t0[1];
    if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy) * 1.5) move(dx < 0 ? 1 : -1);
  };
  const x = A.days[d] || {
      start: [],
      bench: [],
      act: 0,
      total: 0
    },
    y = B.days[d] || {
      start: [],
      bench: [],
      act: 0,
      total: 0
    };
  const dvOf = i => {
    const p = A.days[i],
      q = B.days[i];
    return p && q ? p.act + p.total - (q.act + q.total) : 0;
  };
  const state = x.locked || y.locked ? x.allDone && y.allDone ? "final" : "live" : dates[d] < today ? "final" : "projected";
  const rows = [];
  ["F", "D", "UTIL", "G"].forEach(sl => {
    const L = x.start.filter(p => p.slot === sl),
      R = y.start.filter(p => p.slot === sl);
    for (let i = 0; i < Math.max(L.length, R.length); i++) rows.push([sl, L[i] || null, R[i] || null]);
  });
  const val = p => !p ? null : p.st ? p.a == null ? 0 : p.a : p.x;
  const cell = (p, right) => {
    if (!p) return /*#__PURE__*/React.createElement("div", {
      className: "text-sm text-slate-500" + (right ? " text-right" : "")
    }, "empty");
    const st = p.p === "G" && !p.st ? mStart(p.gs) : "",
      line = p.st ? statLine(pStat(p, p.dt)) : "";
    return /*#__PURE__*/React.createElement("div", {
      className: "min-w-0 gx-pc" + (p.st === "F" ? " gx-fin" : ""),
      style: {
        flexDirection: right ? "row-reverse" : "row"
      },
      onClick: () => setBx118(bx118 === p.id + "|" + p.dt ? "" : p.id + "|" + p.dt)
    }, /*#__PURE__*/React.createElement("span", {
      className: "gx-fw",
      style: {
        display: "inline-flex"
      }
    }, /*#__PURE__*/React.createElement(GxFace, {
      p: p,
      size: 30
    })), /*#__PURE__*/React.createElement("div", {
      className: "min-w-0" + (right ? " text-right" : ""),
      style: {
        flex: 1
      }
    }, /*#__PURE__*/React.createElement("div", {
      className: "truncate gx-nm"
    }, /*#__PURE__*/React.createElement("button", {
      type: "button",
      className: "hover:underline text-left",
      onClick: e => {
        e.stopPropagation();
        if (window.__NAV) window.__NAV.player(p);
      }
    }, /*#__PURE__*/React.createElement("span", {
      className: "m-hide"
    }, p.n), /*#__PURE__*/React.createElement("span", {
      className: "m-inl"
    }, shortN(p.n))), /*#__PURE__*/React.createElement("span", {
      className: "gx-tl98"
    }, /*#__PURE__*/React.createElement(TeamLogo, {
      t: p.t,
      size: 15
    }))), /*#__PURE__*/React.createElement("div", {
      className: "text-xs text-slate-500 truncate"
    }, p.st ? /*#__PURE__*/React.createElement(React.Fragment, null, gxOpp98(p), /*#__PURE__*/React.createElement(LiveTag, {
      st: p.st,
      t: p.t,
      dt: p.dt
    }), p.st === "F" ? /*#__PURE__*/React.createElement("span", {
      className: "m-inl"
    }, " Final") : null, /*#__PURE__*/React.createElement("span", {
      className: "gx-st98"
    }, line ? " " + line : "")) : /*#__PURE__*/React.createElement(React.Fragment, null, mGame(p), st ? " \u00b7 " + st.toLowerCase() : "")), p.st && line ? /*#__PURE__*/React.createElement("div", {
      className: "gx-sl98"
    }, line) : null));
  };
  const num = (p, q, right) => {
    const v = val(p),
      o = val(q);
    if (v == null) return /*#__PURE__*/React.createElement("div", {
      className: "text-slate-500" + (right ? "" : " text-right")
    }, "\u2013");
    const win = o == null || v - o >= 0.05;
    return /*#__PURE__*/React.createElement("div", {
      className: right ? "" : "text-right",
      style: win ? {
        color: "var(--good)",
        fontWeight: 600
      } : p.st && p.x0 != null && v < p.x0 - 0.05 ? {
        color: "var(--bad)"
      } : null
    }, p.st && p.a == null ? "\u2013" : f1(v), p.st && p.x0 != null ? /*#__PURE__*/React.createElement("div", {
      className: "text-xs",
      style: {
        color: "var(--faint)",
        fontWeight: 400
      },
      "data-gx": "094p"
    }, /*#__PURE__*/React.createElement("span", {
      className: "m-hide"
    }, "proj "), f1(p.x0)) : null);
  };
  const sit = (l, id) => l.bench && l.bench.length ? /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500",
    style: {
      marginTop: 6
    }
  }, teamName(s, id), " would sit: ", l.bench.map(p => shortN(p.n)).join(", ")) : null;
  const dayTot = x.act + x.total - (y.act + y.total);
  const mine = a === s.me;
  return /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    key: "m105-" + sel,
    className: "gx-sl105 " + sl105a,
    style: {
      display: "flex",
      alignItems: "center",
      gap: 8
    }
  }, all.length > 1 ? /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: "gx-arw",
    "aria-label": "Previous matchup",
    onClick: () => move(-1)
  }, "\u2039") : null, /*#__PURE__*/React.createElement("div", {
    className: "min-w-0",
    style: {
      flex: 1
    }
  }, /*#__PURE__*/React.createElement("div", {
    className: "text-sm font-semibold gx-nm114",
    style: mine ? {
      color: "var(--accent)"
    } : null
  }, /*#__PURE__*/React.createElement(GxFtPic114, {
    id: a,
    size: 22
  }), /*#__PURE__*/React.createElement(TL, {
    s: s,
    id: a
  })), /*#__PURE__*/React.createElement("div", {
    className: "gx-num",
    style: {
      fontSize: 28
    }
  }, f1(aA))), /*#__PURE__*/React.createElement(GxRing, {
    v: winProb(A, B, aA, aB)
  }), /*#__PURE__*/React.createElement("div", {
    className: "min-w-0 text-right",
    style: {
      flex: 1
    }
  }, /*#__PURE__*/React.createElement("div", {
    className: "text-sm text-slate-500 gx-nm114 r"
  }, /*#__PURE__*/React.createElement(TL, {
    s: s,
    id: b
  }), /*#__PURE__*/React.createElement(GxFtPic114, {
    id: b,
    size: 22
  })), /*#__PURE__*/React.createElement("div", {
    className: "gx-num",
    style: {
      fontSize: 28,
      color: "var(--ink2)"
    }
  }, f1(aB))), all.length > 1 ? /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: "gx-arw",
    "aria-label": "Next matchup",
    onClick: () => move(1)
  }, "\u203a") : null), all.length > 1 ? /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      justifyContent: "center",
      gap: 6,
      marginTop: 8
    }
  }, all.map((pr, i) => /*#__PURE__*/React.createElement("button", {
    key: i,
    type: "button",
    "aria-label": "Matchup " + (i + 1),
    onClick: () => setSel(i),
    style: {
      width: 6,
      height: 6,
      borderRadius: 99,
      background: i === Math.min(sel, all.length - 1) ? "var(--accent)" : "var(--line2)"
    }
  }))) : null, /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500",
    style: {
      display: "flex",
      marginTop: 8
    }
  }, /*#__PURE__*/React.createElement("span", {
    "data-gx": "114w",
    style: {
      margin: "0 auto",
      color: margin >= 0 ? "var(--good)" : "var(--bad)"
    }
  }, mine ? (margin >= 0 ? "Ahead by " : "Behind by ") + f1(Math.abs(margin)) : teamName(s, margin >= 0 ? a : b) + " ahead by " + f1(Math.abs(margin))))), /*#__PURE__*/React.createElement("div", {
    className: "gx-dn108"
  }, /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: "gx-arw",
    "aria-label": "Earlier day",
    disabled: d <= 0,
    onClick: () => setDay(d - 1)
  }, "\u2039"), /*#__PURE__*/React.createElement("div", {
    className: "dt"
  }, dates[d] === today ? "Today" : dates[d] ? dayLabel(dates[d]) : "", /*#__PURE__*/React.createElement("small", {
    style: {
      color: Math.abs(dvOf(d)) < 0.05 ? "var(--mute)" : dvOf(d) > 0 ? "var(--good)" : "var(--bad)"
    }
  }, (dvOf(d) > 0 ? "+" : "") + f1(dvOf(d)))), /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: "gx-arw",
    "aria-label": "Later day",
    disabled: d >= n - 1,
    onClick: () => setDay(d + 1)
  }, "\u203a")), /*#__PURE__*/React.createElement("div", _extends({
    key: "d105-" + sel + "-" + d,
    ref: dr106
  }, dh106, {
    className: "gx-pn gx-dr106 gx-sl105 " + sl105b,
    style: {
      marginTop: 12
    }
  }), /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      alignItems: "baseline",
      marginBottom: 6
    }
  }, /*#__PURE__*/React.createElement("span", {
    className: "gx-tag"
  }, (dates[d] === today ? "Today" : dates[d] ? dayLabel(dates[d]) : "") + " \u00b7 " + state)), rows.length ? rows.map(([sl, p, q], i) => /*#__PURE__*/React.createElement(React.Fragment, {
    key: i
  }, /*#__PURE__*/React.createElement("div", {
    className: "gx-h2h",
    style: i ? null : {
      borderTop: 0
    }
  }, cell(p, false), num(p, q, false), /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-center",
    style: {
      color: "var(--faint)"
    }
  }, sl === "UTIL" ? "U" : sl), num(q, p, true), cell(q, true)))) : /*#__PURE__*/React.createElement("div", {
    className: "text-sm text-slate-500"
  }, "No games for either team on this day."), rows.length ? /*#__PURE__*/React.createElement("div", {
    className: "gx-h2h gx-tt114"
  }, /*#__PURE__*/React.createElement("div", null, state === "final" ? "Final" : state === "live" ? "Live" : "Projected"), /*#__PURE__*/React.createElement("div", {
    className: "text-right"
  }, f1(x.act + x.total)), /*#__PURE__*/React.createElement("div", null), /*#__PURE__*/React.createElement("div", null, f1(y.act + y.total)), /*#__PURE__*/React.createElement("div", {
    className: "text-right",
    style: {
      color: Math.abs(dayTot) < 0.05 ? "var(--mute)" : dayTot > 0 ? "var(--good)" : "var(--bad)"
    }
  }, (dayTot > 0 ? "+" : "") + f1(dayTot))) : null, sit(x, a), sit(y, b), (() => {
    /* gx119-popup */const z = bx118 ? rows.map(r => [r[1], r[2]]).flat().find(v => v && v.id + "|" + v.dt === bx118) : null;
    return z ? /*#__PURE__*/React.createElement(GxBox119, {
      s: s,
      p: z,
      onClose: () => setBx118("")
    }) : null;
  })()), /*#__PURE__*/React.createElement("div", {
    className: "gx-wt114"
  }, /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("small", null, over ? "Week final" : "Week projected"), /*#__PURE__*/React.createElement("b", null, Math.round(fa))), /*#__PURE__*/React.createElement("div", {
    className: "r"
  }, /*#__PURE__*/React.createElement("small", null, over ? "Week final" : "Week projected"), /*#__PURE__*/React.createElement("b", null, Math.round(fb)))), /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500",
    style: {
      display: "flex",
      marginTop: 6
    }
  }, /*#__PURE__*/React.createElement("span", null, gamesMoves(s, a, wk, A)), /*#__PURE__*/React.createElement("span", {
    style: {
      marginLeft: "auto"
    }
  }, gamesMoves(s, b, wk, B))));
}

// ---------- Add / Drop ----------
const shortTag = (p, K) => {
  const t = tags(p, K)[0];
  if (!t) return null;
  const x = t.u ? t.t.split(":")[0] : t.t;
  return {
    t: x.length > 20 ? x.slice(0, 19) + "…" : x,
    c: t.c
  };
};
const cntOf = r => {
  const c = {
    F: 0,
    D: 0,
    G: 0
  };
  r.forEach(p => {
    if (!p.ir) c[p.p]++;
  });
  return c;
};
function MoveSim({
  s,
  setS,
  wk,
  M,
  H,
  hLabel,
  init,
  wBase,
  onClose
}) {
  const effAvg = gxPgAvg; /* gx088-sim */
  const {
    total,
    rawPts,
    gamesIn,
    protectedIds,
    mins,
    lineupAware,
    myR,
    fas,
    K
  } = M;
  const left = movesLeft(s, s.me, wk);
  const cap = Math.max(1, left == null ? 3 : left);
  const [moves, setMoves] = useState([{
    add: init.add || "",
    drop: init.drop || "",
    sug: init.drop || ""
  }]);
  const [qs, setQs] = useState({});
  const [openI, setOpenI] = useState(init.add ? -1 : 0);
  const [focus, setFocus] = useState(0);
  useEffect(() => {
    const k = e => {
      if (e.key === "Escape") onClose();
    };
    window.addEventListener("keydown", k);
    document.body.style.overflow = "hidden";
    return () => {
      window.removeEventListener("keydown", k);
      document.body.style.overflow = "";
    };
  }, []);
  const byId = id => id ? s.players.find(p => p.id === id) || null : null;
  const rosterBefore = (i, ms) => {
    let r = myR;
    (ms || moves).slice(0, i).forEach(m => {
      const a = byId(m.add);
      if (a && r.some(x => x.id === m.drop)) r = r.filter(x => x.id !== m.drop).concat([{
        ...a,
        ft: s.me
      }]);
    });
    return r;
  };
  const suggestDrop = (i, f, ms) => {
    const r = rosterBefore(i, ms),
      c = cntOf(r);
    const ok = d => !d.ir && (d.p === f.p || c[d.p] - 1 >= mins[d.p]);
    let cands = r.filter(d => ok(d) && !protectedIds.has(d.id));
    if (!cands.length) cands = r.filter(ok);
    const b = lineupAware ? total(r) : 0;
    let best = null;
    cands.forEach(d => {
      const g = lineupAware ? total(timedMove(r, s.me, [{
        add: f,
        drop: d
      }])) - b : rawPts(f) - rawPts(d, f);
      if (!best || g > best.g) best = {
        d,
        g
      };
    });
    return best ? best.d.id : "";
  };
  const setAdd = (i, id) => {
    const f = byId(id);
    setMoves(ms => ms.map((m, k) => {
      if (k !== i) return m;
      const sug = f ? suggestDrop(i, f, ms) : "";
      return {
        add: id,
        drop: sug,
        sug
      };
    }));
    setQs(x => ({
      ...x,
      [i]: ""
    }));
    setOpenI(-1);
    setFocus(i);
  };
  const setDrop = (i, id) => setMoves(ms => ms.map((m, k) => k === i ? {
    ...m,
    drop: id
  } : m));
  const addMove = () => {
    const n = moves.length;
    setMoves(ms => ms.concat([{
      add: "",
      drop: "",
      sug: ""
    }]));
    setOpenI(n);
    setFocus(n);
  };
  const removeMove = i => {
    setMoves(ms => ms.filter((_, k) => k !== i));
    setFocus(0);
    setOpenI(-1);
  };
  const matches = i => {
    const q = nrm(qs[i] || ""),
      used = new Set(moves.filter((_, k) => k !== i).map(m => m.add));
    if (!q) return M.res.filter(r => !used.has(r.f.id)).slice(0, 6).map(r => r.f);
    return fas.filter(p => p.prob > 0 && !used.has(p.id) && nrm(p.n).includes(q)).sort((a, b) => effAvg(b, K) - effAvg(a, K)).slice(0, 8);
  };
  const key = JSON.stringify(moves.map(m => [m.add, m.drop]));
  const R = useMemo(() => {
    const list = moves.map((m, i) => {
      const a = byId(m.add),
        r = rosterBefore(i);
      const d = r.find(x => x.id === m.drop) || null;
      return a && d ? {
        a,
        d
      } : null;
    });
    const ok = list.filter(Boolean);
    if (!ok.length) return {
      list,
      ok
    };
    const after = rosterBefore(moves.length);
    const timed = timedMove(myR, s.me, ok.map(x => ({
      add: x.a,
      drop: x.d
    })));
    const gain = lineupAware ? total(timed) - total(myR) : ok.reduce((t, x) => t + rawPts(x.a) - rawPts(x.d, x.a), 0);
    const c = cntOf(after);
    return {
      list,
      ok,
      after,
      gain,
      c,
      win: winChance(s, timed),
      short: ["F", "D", "G"].filter(k => c[k] < mins[k])
    };
  }, [key]);
  const addF = byId((moves[focus] || {}).add);
  const alts = useMemo(() => addF ? computeMoves(s, {
    H,
    pos: addF.p,
    pool: 40
  }).res.filter(r => r.f.id !== addF.id && !moves.some(m => m.add === r.f.id)).slice(0, 3) : [], [addF ? addF.id : "", H]);
  const apply = () => {
    const drops = new Set(R.ok.map(x => x.d.id)),
      adds = new Set(R.ok.map(x => x.a.id));
    setS(st => ({
      ...st,
      players: st.players.map(p => drops.has(p.id) ? {
        ...p,
        ft: "fa",
        ir: false
      } : adds.has(p.id) ? {
        ...p,
        ft: st.me
      } : p)
    }));
    onClose();
  };
  const before = cntOf(myR);
  const posName = {
    F: "forwards",
    D: "defencemen",
    G: "goalies"
  };
  return /*#__PURE__*/React.createElement("div", {
    className: "fixed inset-0 z-50 flex items-start justify-center p-3 sm:p-6 overflow-y-auto",
    style: {
      background: "rgba(0,0,0,.65)"
    },
    onClick: onClose
  }, /*#__PURE__*/React.createElement("div", {
    className: "ms-card",
    onClick: e => e.stopPropagation()
  }, /*#__PURE__*/React.createElement("div", {
    className: "flex items-start gap-3 mb-3"
  }, /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    className: "font-semibold text-base"
  }, "Simulate a move"), /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500"
  }, "Points: ", hLabel, " \xB7 win chance: this week", left != null ? ` · ${left} move${left === 1 ? "" : "s"} left this week` : "")), /*#__PURE__*/React.createElement("button", {
    className: "ml-auto text-2xl leading-none text-slate-500",
    "aria-label": "Close",
    onClick: onClose
  }, "\xD7")), moves.map((m, i) => {
    const a = byId(m.add),
      r = rosterBefore(i),
      it = R.list[i];
    const drops = r.filter(p => !p.ir).sort((x, y) => effAvg(x, K) - effAvg(y, K));
    const sd = it ? effAvg(it.a, K) - effAvg(it.d, K) : 0;
    const ml = openI === i ? matches(i) : [];
    return /*#__PURE__*/React.createElement("div", {
      key: i,
      className: "ms-move",
      onClick: () => setFocus(i)
    }, moves.length > 1 ? /*#__PURE__*/React.createElement("div", {
      className: "flex items-center mb-2"
    }, /*#__PURE__*/React.createElement("span", {
      className: "text-xs uppercase tracking-wide text-slate-500"
    }, "Move ", i + 1), /*#__PURE__*/React.createElement("button", {
      className: "ml-auto text-xs text-slate-500",
      onClick: e => {
        e.stopPropagation();
        removeMove(i);
      }
    }, "Remove")) : null, /*#__PURE__*/React.createElement("div", {
      className: "tb-grid"
    }, /*#__PURE__*/React.createElement("div", {
      className: "min-w-0"
    }, /*#__PURE__*/React.createElement("div", {
      className: "text-xs text-slate-500 mb-1"
    }, "Add"), a && openI !== i ? /*#__PURE__*/React.createElement("div", {
      className: "ms-pick"
    }, /*#__PURE__*/React.createElement(GxFace, {
      p: a,
      size: 26
    }), /*#__PURE__*/React.createElement("div", {
      className: "min-w-0 flex-1"
    }, /*#__PURE__*/React.createElement("div", {
      className: "truncate font-medium"
    }, a.n), /*#__PURE__*/React.createElement("div", {
      className: "text-xs text-slate-500"
    }, a.p, " \xB7 ", gamesIn(a), " gms \xB7 ", f1(effAvg(a, K)), "/g")), /*#__PURE__*/React.createElement("button", {
      className: "text-xs text-blue-600",
      onClick: () => setOpenI(i)
    }, "Change")) : /*#__PURE__*/React.createElement("div", {
      className: "relative"
    }, /*#__PURE__*/React.createElement("input", {
      className: inp + " w-full",
      autoFocus: openI === i,
      placeholder: "Type a free agent's name",
      value: qs[i] || "",
      onChange: e => {
        setQs({
          ...qs,
          [i]: e.target.value
        });
        setOpenI(i);
      },
      onFocus: () => setOpenI(i),
      onBlur: () => setTimeout(() => setOpenI(x => x === i ? -1 : x), 150)
    }), openI === i ? /*#__PURE__*/React.createElement("div", {
      className: "ms-list"
    }, !(qs[i] || "").trim() ? /*#__PURE__*/React.createElement("div", {
      className: "text-xs text-slate-500 px-2 pt-1 pb-1"
    }, "Top pickups") : null, ml.map(p => /*#__PURE__*/React.createElement("button", {
      key: p.id,
      type: "button",
      className: "ms-opt",
      onMouseDown: e => e.preventDefault(),
      onClick: () => setAdd(i, p.id)
    }, /*#__PURE__*/React.createElement(GxFace, {
      p: p,
      size: 22
    }), /*#__PURE__*/React.createElement("span", {
      className: "truncate flex-1 text-left"
    }, p.n, " ", /*#__PURE__*/React.createElement("span", {
      className: "text-xs text-slate-500"
    }, p.p)), /*#__PURE__*/React.createElement("span", {
      className: "text-xs text-slate-500 whitespace-nowrap"
    }, gamesIn(p), " gms \xB7 ", f1(effAvg(p, K))))), ml.length === 0 ? /*#__PURE__*/React.createElement("div", {
      className: "text-sm text-slate-400 px-2 py-2"
    }, "No free agent matches.") : null, a ? /*#__PURE__*/React.createElement("button", {
      type: "button",
      className: "text-xs text-slate-500 px-2 py-1",
      onMouseDown: e => e.preventDefault(),
      onClick: () => setOpenI(-1)
    }, "Keep ", a.n) : null) : null)), /*#__PURE__*/React.createElement("div", {
      className: "min-w-0"
    }, /*#__PURE__*/React.createElement("div", {
      className: "text-xs text-slate-500 mb-1"
    }, "Drop", m.drop && m.drop === m.sug ? " · suggested" : ""), /*#__PURE__*/React.createElement("select", {
      className: inp + " w-full",
      value: m.drop,
      onChange: e => setDrop(i, e.target.value)
    }, /*#__PURE__*/React.createElement("option", {
      value: ""
    }, "Choose who to drop"), drops.map(p => /*#__PURE__*/React.createElement("option", {
      key: p.id,
      value: p.id
    }, p.n, " (", p.p, ") \xB7 ", f1(effAvg(p, K)), "/g", p.p === "G" ? " · starts " + Math.round((p.prob || 0) * 100) + "%" : "", protectedIds.has(p.id) ? " · protected" : ""))))), it ? /*#__PURE__*/React.createElement("div", {
      className: "text-xs mt-2 " + (sd >= 0 ? "text-green-700" : "text-amber-600")
    }, sd >= 0 ? `Keeper: ${f1(sd)}/game better than ${it.d.n} long-term` : `Stream only: ${f1(-sd)}/game worse than ${it.d.n} long-term`, protectedIds.has(it.d.id) ? ` · ${it.d.n} is protected` : "") : a && m.drop && !r.some(x => x.id === m.drop) ? /*#__PURE__*/React.createElement("div", {
      className: "text-xs mt-2 text-red-600"
    }, "That player is already dropped in an earlier move. Choose another drop.") : null);
  }), addF && alts.length ? /*#__PURE__*/React.createElement("div", {
    className: "mt-3"
  }, /*#__PURE__*/React.createElement("div", {
    className: "text-xs uppercase tracking-wide text-slate-500 mb-1"
  }, "Other ", posName[addF.p], " to consider"), alts.map(r => /*#__PURE__*/React.createElement("div", {
    key: r.f.id,
    className: "flex items-center gap-2.5 py-2 border-t border-slate-100"
  }, /*#__PURE__*/React.createElement(GxFace, {
    p: r.f,
    size: 22
  }), /*#__PURE__*/React.createElement("div", {
    className: "min-w-0 flex-1"
  }, /*#__PURE__*/React.createElement("div", {
    className: "truncate"
  }, r.f.n), /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500"
  }, gamesIn(r.f), " gms \xB7 ", f1(effAvg(r.f, K)), "/g \xB7 drop ", r.d.n)), /*#__PURE__*/React.createElement("span", {
    className: "text-green-700 font-semibold text-sm"
  }, "+", f1(r.gain)), /*#__PURE__*/React.createElement("button", {
    className: "text-xs text-blue-600",
    onClick: () => setAdd(focus, r.f.id)
  }, "Use")))) : null, moves.length < cap ? /*#__PURE__*/React.createElement("button", {
    className: "text-sm text-blue-600 mt-3",
    onClick: addMove
  }, "+ Add another move") : /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500 mt-3"
  }, left === 0 ? "No moves left this week on ESPN, so this is only a what-if." : `That's all ${cap} of your moves left this week.`), /*#__PURE__*/React.createElement("div", {
    className: "ms-res"
  }, R.ok.length ? /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    className: "grid grid-cols-3 gap-2 text-center"
  }, /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500"
  }, "Points"), /*#__PURE__*/React.createElement("div", {
    className: "text-xl"
  }, /*#__PURE__*/React.createElement(Dlt, {
    v: R.gain
  })), /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500"
  }, hLabel)), /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500"
  }, "Win this week"), /*#__PURE__*/React.createElement("div", {
    className: "text-xl font-semibold " + (R.win != null && wBase != null ? R.win > wBase ? "text-green-700" : R.win < wBase ? "text-red-600" : "" : "")
  }, R.win == null ? "–" : wpTxt(R.win)), /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500"
  }, "now ", wBase == null ? "–" : wpTxt(wBase))), /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500"
  }, "Roster after"), /*#__PURE__*/React.createElement("div", {
    className: "text-sm font-semibold mt-1"
  }, "F ", R.c.F, " \xB7 D ", R.c.D, " \xB7 G ", R.c.G), /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500"
  }, "was F ", before.F, " \xB7 D ", before.D, " \xB7 G ", before.G))), /*#__PURE__*/React.createElement(GxPickRes92, {
    s: s,
    myR: myR,
    ok: R.ok
  }), R.short.length ? /*#__PURE__*/React.createElement("div", {
    className: "text-sm text-red-600 mt-2"
  }, "Below your minimum at ", R.short.join(", "), ". Pick a different drop.") : null, /*#__PURE__*/React.createElement("div", {
    className: "flex flex-wrap items-center gap-3 mt-3"
  }, /*#__PURE__*/React.createElement("button", {
    className: "bg-blue-600 rounded-lg px-4 py-1.5 font-semibold",
    onClick: apply
  }, "Apply here"), /*#__PURE__*/React.createElement("span", {
    className: "text-xs text-slate-500"
  }, "Updates this app only. Make the real move on ESPN; the next sync confirms it."))) : /*#__PURE__*/React.createElement("div", {
    className: "text-sm text-slate-400"
  }, "Pick a player to add and one to drop to see the result."))));
}

// ---------- Players ----------
function Players({
  s,
  wk
}) {
  // players v10: no Signals column, phone list (news_logos.py)
  const K = s.blend;
  const [ft, setFt] = useState("all");
  const [pos, setPos] = useState("all");
  const [q, setQ] = useState("");
  const [sort, setSort] = useState("week");
  const rows = s.players.filter(p => (ft === "all" || p.ft === ft) && (pos === "all" || p.p === pos) && p.n.toLowerCase().includes(q.toLowerCase())).map(p => {
    const g = (wk.games[p.t] || []).filter(d => !p.ir && avail(p, wk.dates ? wk.dates[d] : null)).length;
    const r = sigOf(p).rec;
    return {
      ...p,
      g,
      ea: effAvg(p, K),
      wkp: g * effAvg(p, K) * p.prob,
      rp: r ? r.ppg : null,
      rg: r ? r.gp : 0
    };
  }).sort((a, b) => sort === "week" ? b.wkp - a.wkp : sort === "avg" ? b.ea - a.ea : sort === "hot" ? (b.rp || 0) - (a.rp || 0) : b.tot - a.tot).slice(0, 300);
  const stTag = p => p.ir ? "IR" : p.status && p.status !== "ACTIVE" ? M_ST[p.status] || p.status.replace(/_/g, " ") : "";
  return /*#__PURE__*/React.createElement("div", {
    className: "space-y-3"
  }, /*#__PURE__*/React.createElement("div", {
    className: "flex flex-wrap gap-2"
  }, /*#__PURE__*/React.createElement("input", {
    className: inp + " flex-1 min-w-[160px]",
    placeholder: "Search player",
    value: q,
    onChange: e => setQ(e.target.value)
  }), /*#__PURE__*/React.createElement("select", {
    className: inp,
    value: ft,
    onChange: e => setFt(e.target.value)
  }, /*#__PURE__*/React.createElement("option", {
    value: "all"
  }, "All teams"), /*#__PURE__*/React.createElement("option", {
    value: "fa"
  }, "Free agents"), s.teams.map(t => /*#__PURE__*/React.createElement("option", {
    key: t.id,
    value: t.id
  }, t.name))), /*#__PURE__*/React.createElement("select", {
    className: inp,
    value: pos,
    onChange: e => setPos(e.target.value)
  }, /*#__PURE__*/React.createElement("option", {
    value: "all"
  }, "All positions"), /*#__PURE__*/React.createElement("option", null, "F"), /*#__PURE__*/React.createElement("option", null, "D"), /*#__PURE__*/React.createElement("option", null, "G")), /*#__PURE__*/React.createElement("select", {
    className: inp,
    value: sort,
    onChange: e => setSort(e.target.value)
  }, /*#__PURE__*/React.createElement("option", {
    value: "week"
  }, "Sort: this week"), /*#__PURE__*/React.createElement("option", {
    value: "avg"
  }, "Sort: projected avg"), /*#__PURE__*/React.createElement("option", {
    value: "hot"
  }, "Sort: last 14 days"), /*#__PURE__*/React.createElement("option", {
    value: "tot"
  }, "Sort: season total"))), /*#__PURE__*/React.createElement("div", {
    className: "m-hide bg-white rounded-xl border border-slate-200 overflow-x-auto"
  }, /*#__PURE__*/React.createElement("table", {
    className: "w-full text-sm"
  }, /*#__PURE__*/React.createElement("thead", {
    className: "text-left"
  }, /*#__PURE__*/React.createElement("tr", null, ["Player", "", "Team", "Gms", "Avg", "Last 14d", "Season", "Week"].map((h, i) => /*#__PURE__*/React.createElement("th", {
    key: i,
    className: "px-3 py-2"
  }, h)))), /*#__PURE__*/React.createElement("tbody", null, rows.map(p => /*#__PURE__*/React.createElement("tr", {
    key: p.id,
    className: "border-t border-slate-100 " + (p.ft === s.me ? "bg-blue-50" : "")
  }, /*#__PURE__*/React.createElement("td", {
    className: "px-3 py-2"
  }, /*#__PURE__*/React.createElement(PN, {
    p: p
  }), stTag(p) ? /*#__PURE__*/React.createElement("span", {
    className: "text-red-600 text-xs ml-1"
  }, stTag(p)) : null), /*#__PURE__*/React.createElement("td", {
    className: "px-3 py-2 text-xs text-slate-500 whitespace-nowrap"
  }, p.p, " \xB7 ", /*#__PURE__*/React.createElement(GxFace, {
    p: p
  })), /*#__PURE__*/React.createElement("td", {
    className: "px-3 py-2 text-xs text-slate-500"
  }, /*#__PURE__*/React.createElement(TL, {
    s: s,
    id: p.ft
  })), /*#__PURE__*/React.createElement("td", {
    className: "px-3 py-2"
  }, p.g), /*#__PURE__*/React.createElement("td", {
    className: "px-3 py-2 font-semibold"
  }, f1(p.ea)), /*#__PURE__*/React.createElement("td", {
    className: "px-3 py-2"
  }, p.rp !== null ? `${f1(p.rp)} (${p.rg})` : "–"), /*#__PURE__*/React.createElement("td", {
    className: "px-3 py-2"
  }, p.gp ? `${f1(p.tot)} (${p.gp})` : "–"), /*#__PURE__*/React.createElement("td", {
    className: "px-3 py-2 font-semibold"
  }, f1(p.wkp)))))), /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500 p-3"
  }, "Up to 300 shown \u2014 use the filters to narrow down.")), /*#__PURE__*/React.createElement("div", {
    className: "m-only bg-white rounded-xl border border-slate-200 px-3"
  }, /*#__PURE__*/React.createElement("div", {
    className: "m-ghead"
  }, /*#__PURE__*/React.createElement("span", null, "Player"), /*#__PURE__*/React.createElement("span", null, "Gms"), /*#__PURE__*/React.createElement("span", null, "Avg"), /*#__PURE__*/React.createElement("span", null, "Week")), rows.slice(0, 100).map(p => {
    const tg = stTag(p);
    return /*#__PURE__*/React.createElement("div", {
      key: p.id,
      className: "m-rrow",
      role: "button",
      onClick: () => window.__NAV && window.__NAV.player(p)
    }, /*#__PURE__*/React.createElement(GxFace, {
      p: p,
      size: 26
    }), /*#__PURE__*/React.createElement("div", {
      className: "min-w-0"
    }, /*#__PURE__*/React.createElement("div", {
      className: "truncate font-medium" + (p.ft === s.me ? " text-blue-600" : "")
    }, p.n), /*#__PURE__*/React.createElement("div", {
      className: "text-xs text-slate-500 truncate"
    }, p.p, " \xB7 ", teamName(s, p.ft), tg ? /*#__PURE__*/React.createElement("span", {
      className: "text-red-600"
    }, " \xB7 ", tg) : null)), /*#__PURE__*/React.createElement("span", {
      className: "m-num"
    }, p.g), /*#__PURE__*/React.createElement("span", {
      className: "m-num"
    }, f1(p.ea)), /*#__PURE__*/React.createElement("span", {
      className: "m-num font-semibold"
    }, f1(p.wkp)));
  }), /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500 py-3"
  }, "Up to 100 shown \u2014 use the filters to narrow down.")));
}

// ---------- Setup ----------
function Bulk({
  s,
  setS
}) {
  const [mode, setMode] = useState("team");
  const [txt, setTxt] = useState("");
  const [msg, setMsg] = useState("");
  const help = {
    add: "Name | NHL | Pos | ProjAvg | Play% | Fantasy team (or FA)",
    avg: "Name | ProjAvg",
    season: "Name | GP | Season total pts",
    play: "Name | Play% (goalies: start %)   e.g.  Kevin Lankinen | 85",
    team: "Name | Fantasy team (or FA)   e.g.  Colton Parayko | FA"
  };
  const run = () => {
    const lines = txt.split("\n").map(l => l.trim()).filter(Boolean);
    let players = [...s.players];
    let upd = 0,
      add = 0;
    const miss = [];
    const find = n => players.findIndex(p => p.n.toLowerCase() === n.toLowerCase());
    const teamId = x => {
      const v = (x || "").trim().toLowerCase();
      if (!v || v === "fa" || v === "free agent") return "fa";
      const t = s.teams.find(t => t.name.toLowerCase() === v || t.id === v);
      return t ? t.id : null;
    };
    lines.forEach((l, k) => {
      const f = l.split(/\t|\|/).map(x => x.trim());
      if (f.length < 2) {
        miss.push(l);
        return;
      }
      const i = find(f[0]);
      if (mode === "add") {
        const tid = teamId(f[5]);
        const pos = (f[2] || "F").toUpperCase();
        const nhl = (f[1] || "").toUpperCase();
        if (tid === null || !NHL.includes(nhl) || !["F", "D", "G"].includes(pos)) {
          miss.push(l);
          return;
        }
        const rec = {
          n: f[0],
          t: nhl,
          p: pos,
          avg: parseFloat(f[3]) || 0,
          prob: f[4] === undefined || f[4] === "" ? 1 : (parseFloat(f[4]) || 0) / 100,
          ft: tid,
          est: false
        };
        if (i >= 0) {
          players[i] = {
            ...players[i],
            ...rec
          };
          upd++;
        } else {
          players.push({
            id: "p" + Date.now() + "_" + k,
            ir: false,
            gp: 0,
            tot: 0,
            ...rec
          });
          add++;
        }
        return;
      }
      if (i < 0) {
        miss.push(f[0]);
        return;
      }
      if (mode === "avg") players[i] = {
        ...players[i],
        avg: parseFloat(f[1]) || 0,
        est: false
      };
      if (mode === "season") players[i] = {
        ...players[i],
        gp: parseInt(f[1]) || 0,
        tot: parseFloat(f[2]) || 0
      };
      if (mode === "play") players[i] = {
        ...players[i],
        prob: Math.max(0, Math.min(100, parseFloat(f[1]) || 0)) / 100
      };
      if (mode === "team") {
        const tid = teamId(f[1]);
        if (tid === null) {
          miss.push(l);
          return;
        }
        players[i] = {
          ...players[i],
          ft: tid,
          ir: false
        };
      }
      upd++;
    });
    setS({
      ...s,
      players
    });
    setMsg(`Updated ${upd}, added ${add}.` + (miss.length ? ` Not matched (${miss.length}): ${miss.slice(0, 8).join("; ")}` : ""));
  };
  return /*#__PURE__*/React.createElement("div", {
    className: box
  }, /*#__PURE__*/React.createElement("div", {
    className: "font-semibold text-base mb-2"
  }, "Bulk update"), /*#__PURE__*/React.createElement("div", {
    className: "flex flex-wrap gap-2 items-center mb-2"
  }, /*#__PURE__*/React.createElement("select", {
    className: inp,
    value: mode,
    onChange: e => setMode(e.target.value)
  }, /*#__PURE__*/React.createElement("option", {
    value: "team"
  }, "Move players (adds, drops, trades)"), /*#__PURE__*/React.createElement("option", {
    value: "play"
  }, "Injuries / goalie start %"), /*#__PURE__*/React.createElement("option", {
    value: "season"
  }, "Season GP & total"), /*#__PURE__*/React.createElement("option", {
    value: "avg"
  }, "Projected averages"), /*#__PURE__*/React.createElement("option", {
    value: "add"
  }, "Add or replace players")), /*#__PURE__*/React.createElement("button", {
    className: "bg-blue-600 rounded-lg px-3 py-1.5",
    onClick: run
  }, "Apply")), /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500 mb-2"
  }, "One per line: ", help[mode]), /*#__PURE__*/React.createElement("textarea", {
    className: inp + " w-full h-32 font-mono text-xs",
    value: txt,
    onChange: e => setTxt(e.target.value)
  }), msg && /*#__PURE__*/React.createElement("div", {
    className: "text-sm mt-2"
  }, msg), /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500 mt-2"
  }, "The next ESPN sync replaces manual roster moves with ESPN's real rosters."));
}
function InjuryPanel({
  s,
  setS
}) {
  const [showFA, setShowFA] = useState(false);
  const list = s.players.filter(p => p.status && p.status !== "ACTIVE" || p.back || autoInj(p)).filter(p => showFA || p.ft !== "fa").sort((a, b) => (a.ft === s.me ? 0 : 1) - (b.ft === s.me ? 0 : 1) || teamName(s, a.ft).localeCompare(teamName(s, b.ft)));
  const upd = (id, back) => setS(st => ({
    ...st,
    players: st.players.map(p => p.id === id ? {
      ...p,
      back
    } : p)
  }));
  const today = todayISO();
  return /*#__PURE__*/React.createElement(Section, {
    title: "Injuries & return dates",
    sub: "Filled automatically from ESPN's injury report. Pick a date to override; Clear to go back to automatic.",
    link: [showFA ? "Hide free agents" : "Include free agents", () => setShowFA(!showFA)]
  }, /*#__PURE__*/React.createElement("div", {
    className: "overflow-x-auto"
  }, /*#__PURE__*/React.createElement("table", {
    className: "w-full text-sm"
  }, /*#__PURE__*/React.createElement("thead", {
    className: "text-left"
  }, /*#__PURE__*/React.createElement("tr", null, ["Player", "Team", "Status", "Back on", ""].map(h => /*#__PURE__*/React.createElement("th", {
    key: h,
    className: "px-2 py-2"
  }, h)))), /*#__PURE__*/React.createElement("tbody", null, list.map(p => {
    const eb = effBack(p),
      a = autoInj(p);
    return /*#__PURE__*/React.createElement("tr", {
      key: p.id,
      className: "border-t border-slate-100 align-top " + (p.ft === s.me ? "bg-blue-50" : "")
    }, /*#__PURE__*/React.createElement("td", {
      className: "px-2 py-2"
    }, /*#__PURE__*/React.createElement("div", {
      className: "font-medium"
    }, p.n), /*#__PURE__*/React.createElement("div", {
      className: "text-xs text-slate-400"
    }, p.p, " \xB7 ", /*#__PURE__*/React.createElement(GxFace, {
      p: p
    }))), /*#__PURE__*/React.createElement("td", {
      className: "px-2 py-2 text-xs text-slate-500"
    }, teamName(s, p.ft)), /*#__PURE__*/React.createElement("td", {
      className: "px-2 py-2 text-red-600 text-xs"
    }, (a && a.status || p.status || "").replace(/_/g, " ")), /*#__PURE__*/React.createElement("td", {
      className: "px-2 py-2"
    }, /*#__PURE__*/React.createElement("input", {
      type: "date",
      className: inp,
      value: eb.d,
      onChange: e => upd(p.id, e.target.value)
    }), eb.src ? /*#__PURE__*/React.createElement("span", {
      className: "text-xs ml-2 " + (eb.src === "you" ? "text-blue-700 font-semibold" : "text-slate-500")
    }, eb.src === "you" ? "set by you" : "auto: " + eb.src) : null, eb.d && eb.d <= today ? /*#__PURE__*/React.createElement("span", {
      className: "text-green-700 text-xs ml-2"
    }, today < addDays(eb.d, 7) ? "back (90% first week)" : "available") : null, a && a.note ? /*#__PURE__*/React.createElement("div", {
      className: "text-xs text-slate-500 mt-1 max-w-md"
    }, a.type ? a.type + " — " : "", a.note) : null), /*#__PURE__*/React.createElement("td", {
      className: "px-2 py-2"
    }, p.back ? /*#__PURE__*/React.createElement("button", {
      className: "text-xs text-red-600",
      onClick: () => upd(p.id, "")
    }, "Clear") : null));
  }), list.length === 0 && /*#__PURE__*/React.createElement("tr", null, /*#__PURE__*/React.createElement("td", {
    className: "px-2 py-3 text-slate-400"
  }, "No injured players."))))));
}
function RosterTable({
  s,
  setS,
  wk,
  team
}) {
  const [q, setQ] = useState("");
  const upd = (id, patch) => setS(st => ({
    ...st,
    players: st.players.map(p => p.id === id ? {
      ...p,
      ...patch
    } : p)
  }));
  const order = {
    F: 0,
    D: 1,
    G: 2
  };
  const all = s.players.filter(p => p.ft === team);
  const list = all.filter(p => p.n.toLowerCase().includes(q.toLowerCase())).sort((a, b) => order[a.p] - order[b.p] || b.avg - a.avg).slice(0, team === "fa" ? 100 : 999);
  const cnt = {
    F: 0,
    D: 0,
    G: 0
  };
  all.forEach(p => {
    if (!p.ir) cnt[p.p]++;
  });
  const active = all.filter(p => !p.ir).length;
  const mins = {
    F: s.minF ?? 10,
    D: s.minD ?? 5,
    G: s.minGo ?? 2
  };
  const low = team === s.me && (cnt.F < mins.F || cnt.D < mins.D || cnt.G < mins.G);
  return /*#__PURE__*/React.createElement("div", {
    className: "bg-white rounded-xl border border-slate-200 mb-4"
  }, /*#__PURE__*/React.createElement("div", {
    className: "flex flex-wrap items-center gap-3 p-3 border-b border-slate-200"
  }, /*#__PURE__*/React.createElement("div", {
    className: "font-semibold text-base"
  }, teamName(s, team) || "Free agents"), team !== "fa" && /*#__PURE__*/React.createElement("span", {
    className: "text-xs " + (low ? "text-red-600 font-semibold" : "text-slate-500")
  }, active, "/22 active \xB7 F ", cnt.F, " \xB7 D ", cnt.D, " \xB7 G ", cnt.G, all.length - active ? ` · ${all.length - active} IR` : "", low ? " — below minimums" : ""), /*#__PURE__*/React.createElement("input", {
    className: inp + " ml-auto",
    placeholder: "Search",
    value: q,
    onChange: e => setQ(e.target.value)
  })), /*#__PURE__*/React.createElement("div", {
    className: "overflow-x-auto"
  }, /*#__PURE__*/React.createElement("table", {
    className: "w-full text-sm"
  }, /*#__PURE__*/React.createElement("thead", {
    className: "text-left"
  }, /*#__PURE__*/React.createElement("tr", null, ["Player", "", "Proj avg", "Play %", "IR", "Back on", "Gms", "Fantasy team"].map((h, i) => /*#__PURE__*/React.createElement("th", {
    key: i,
    className: "px-2 py-2"
  }, h)))), /*#__PURE__*/React.createElement("tbody", null, list.map(p => /*#__PURE__*/React.createElement("tr", {
    key: p.id,
    className: "border-t border-slate-100"
  }, /*#__PURE__*/React.createElement("td", {
    className: "px-2 py-1.5 font-medium whitespace-nowrap"
  }, p.n, p.status && p.status !== "ACTIVE" ? /*#__PURE__*/React.createElement("span", {
    className: "text-red-600 text-xs ml-1"
  }, p.status.replace(/_/g, " ")) : ""), /*#__PURE__*/React.createElement("td", {
    className: "px-2 py-1.5 text-xs text-slate-500 whitespace-nowrap"
  }, p.p, " \xB7 ", /*#__PURE__*/React.createElement(GxFace, {
    p: p
  })), /*#__PURE__*/React.createElement("td", {
    className: "px-2 py-1.5"
  }, /*#__PURE__*/React.createElement("input", {
    type: "number",
    step: "0.1",
    className: inp + " w-20",
    value: p.avg,
    onChange: e => upd(p.id, {
      avg: parseFloat(e.target.value) || 0,
      est: false
    })
  })), /*#__PURE__*/React.createElement("td", {
    className: "px-2 py-1.5"
  }, /*#__PURE__*/React.createElement("input", {
    type: "number",
    min: "0",
    max: "100",
    className: inp + " w-16",
    value: Math.round(p.prob * 100),
    onChange: e => upd(p.id, {
      prob: Math.max(0, Math.min(100, parseFloat(e.target.value) || 0)) / 100
    })
  })), /*#__PURE__*/React.createElement("td", {
    className: "px-2 py-1.5"
  }, /*#__PURE__*/React.createElement("input", {
    type: "checkbox",
    checked: !!p.ir,
    onChange: e => upd(p.id, {
      ir: e.target.checked
    })
  })), /*#__PURE__*/React.createElement("td", {
    className: "px-2 py-1.5"
  }, /*#__PURE__*/React.createElement("input", {
    type: "date",
    className: inp,
    value: p.back || "",
    onChange: e => upd(p.id, {
      back: e.target.value
    })
  })), /*#__PURE__*/React.createElement("td", {
    className: "px-2 py-1.5"
  }, gms(wk, p.t)), /*#__PURE__*/React.createElement("td", {
    className: "px-2 py-1.5"
  }, /*#__PURE__*/React.createElement("select", {
    className: inp,
    value: p.ft,
    onChange: e => upd(p.id, {
      ft: e.target.value,
      ir: false
    })
  }, s.teams.map(t => /*#__PURE__*/React.createElement("option", {
    key: t.id,
    value: t.id
  }, t.name)), /*#__PURE__*/React.createElement("option", {
    value: "fa"
  }, "Free agent")))))))), team === "fa" && all.length > 100 && /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500 p-3"
  }, "Showing 100 of ", all.length, " \u2014 use search."));
}
function AddOne({
  s,
  setS
}) {
  const [nw, setNw] = useState({
    n: "",
    t: "ANA",
    p: "F",
    avg: 6,
    prob: 100,
    ft: s.me
  });
  const addP = () => {
    if (!nw.n.trim()) return;
    setS(st => ({
      ...st,
      players: [...st.players, {
        id: "p" + Date.now(),
        n: nw.n.trim(),
        t: nw.t,
        p: nw.p,
        avg: +nw.avg,
        prob: +nw.prob / 100,
        ft: nw.ft,
        ir: false,
        est: false,
        gp: 0,
        tot: 0
      }]
    }));
    setNw({
      ...nw,
      n: ""
    });
  };
  return /*#__PURE__*/React.createElement("div", {
    className: box
  }, /*#__PURE__*/React.createElement("div", {
    className: "font-semibold text-base mb-2"
  }, "Add one player"), /*#__PURE__*/React.createElement("div", {
    className: "flex flex-wrap gap-2 items-center"
  }, /*#__PURE__*/React.createElement("input", {
    className: inp,
    placeholder: "Name",
    value: nw.n,
    onChange: e => setNw({
      ...nw,
      n: e.target.value
    })
  }), /*#__PURE__*/React.createElement("select", {
    className: inp,
    value: nw.t,
    onChange: e => setNw({
      ...nw,
      t: e.target.value
    })
  }, NHL.map(t => /*#__PURE__*/React.createElement("option", {
    key: t
  }, t))), /*#__PURE__*/React.createElement("select", {
    className: inp,
    value: nw.p,
    onChange: e => setNw({
      ...nw,
      p: e.target.value
    })
  }, /*#__PURE__*/React.createElement("option", null, "F"), /*#__PURE__*/React.createElement("option", null, "D"), /*#__PURE__*/React.createElement("option", null, "G")), /*#__PURE__*/React.createElement("label", null, "Avg ", /*#__PURE__*/React.createElement("input", {
    type: "number",
    step: "0.1",
    className: inp + " w-20",
    value: nw.avg,
    onChange: e => setNw({
      ...nw,
      avg: e.target.value
    })
  })), /*#__PURE__*/React.createElement("label", null, "Play % ", /*#__PURE__*/React.createElement("input", {
    type: "number",
    className: inp + " w-16",
    value: nw.prob,
    onChange: e => setNw({
      ...nw,
      prob: e.target.value
    })
  })), /*#__PURE__*/React.createElement("select", {
    className: inp,
    value: nw.ft,
    onChange: e => setNw({
      ...nw,
      ft: e.target.value
    })
  }, s.teams.map(t => /*#__PURE__*/React.createElement("option", {
    key: t.id,
    value: t.id
  }, t.name)), /*#__PURE__*/React.createElement("option", {
    value: "fa"
  }, "Free agent")), /*#__PURE__*/React.createElement("button", {
    className: "bg-blue-600 rounded-lg px-3 py-1.5",
    onClick: addP
  }, "Add")));
}
function Schedule({
  s,
  setS,
  wk,
  setWk
}) {
  const [start, setStart] = useState("");
  const [len, setLen] = useState(7);
  useEffect(() => {
    setStart(wk.dates && wk.dates[0] || "");
    setLen(wk.dates && wk.dates.length || 7);
  }, [s.wk]);
  const relabel = ws => ws.map((w, i) => w.dates && w.dates.length ? {
    ...w,
    label: lab(i, w.dates)
  } : w);
  const applyDates = () => {
    if (!start) return;
    const dates = [...Array(Math.max(1, +len || 1))].map((_, k) => addDays(start, k));
    setS(st => ({
      ...st,
      weeks: relabel(st.weeks.map((w, i) => i === st.wk ? {
        ...w,
        dates
      } : w))
    }));
  };
  const mergeNext = () => {
    if (s.wk >= s.weeks.length - 1 || !confirm("Merge this week with the next one?")) return;
    setS(st => {
      const ws = [...st.weeks];
      const a = ws[st.wk],
        b = ws[st.wk + 1];
      ws[st.wk] = {
        ...a,
        dates: [...(a.dates || []), ...(b.dates || [])]
      };
      ws.splice(st.wk + 1, 1);
      return {
        ...st,
        weeks: relabel(ws)
      };
    });
  };
  const resetWeeks = () => {
    if (confirm("Reset all weeks to Monday–Sunday?")) setS(st => ({
      ...st,
      weeks: defaultWeeks(),
      wk: 0
    }));
  };
  const perDay = wk.days.map((_, d) => NHL.filter(t => (wk.games[t] || []).includes(d)).length / 2);
  return /*#__PURE__*/React.createElement("div", {
    className: "space-y-4"
  }, /*#__PURE__*/React.createElement(Section, {
    title: wk.label,
    sub: "The full NHL schedule is built in; matchups come from ESPN."
  }, /*#__PURE__*/React.createElement("div", {
    className: "flex flex-wrap gap-2 items-center"
  }, /*#__PURE__*/React.createElement("input", {
    type: "date",
    className: inp,
    value: start,
    onChange: e => setStart(e.target.value)
  }), /*#__PURE__*/React.createElement("label", null, "Days ", /*#__PURE__*/React.createElement("input", {
    type: "number",
    min: "1",
    max: "21",
    className: inp + " w-16",
    value: len,
    onChange: e => setLen(e.target.value)
  })), /*#__PURE__*/React.createElement("button", {
    className: "bg-blue-600 rounded-lg px-3 py-1.5",
    onClick: applyDates
  }, "Update dates"), /*#__PURE__*/React.createElement("button", {
    className: "border border-slate-300 rounded-lg px-3 py-1.5",
    onClick: mergeNext
  }, "Merge with next week"), /*#__PURE__*/React.createElement("button", {
    className: "text-red-600 ml-auto text-xs",
    onClick: resetWeeks
  }, "Reset all weeks"))), /*#__PURE__*/React.createElement("div", {
    className: "bg-white rounded-xl border border-slate-200 overflow-x-auto"
  }, /*#__PURE__*/React.createElement("table", {
    className: "text-sm w-full"
  }, /*#__PURE__*/React.createElement("thead", null, /*#__PURE__*/React.createElement("tr", null, /*#__PURE__*/React.createElement("th", {
    className: "px-2 py-2 text-left"
  }, "Team"), wk.days.map((d, i) => /*#__PURE__*/React.createElement("th", {
    key: i,
    className: "px-2 py-2"
  }, d)), /*#__PURE__*/React.createElement("th", {
    className: "px-2 py-2"
  }, "Gms"))), /*#__PURE__*/React.createElement("tbody", null, NHL.map(t => /*#__PURE__*/React.createElement("tr", {
    key: t,
    className: "border-t border-slate-100"
  }, /*#__PURE__*/React.createElement("td", {
    className: "px-2 py-1 font-medium whitespace-nowrap"
  }, /*#__PURE__*/React.createElement("span", {
    className: "inline-flex items-center gap-1.5"
  }, /*#__PURE__*/React.createElement(TeamLogo, {
    t: t,
    size: 16
  }), t)), wk.days.map((_, d) => {
    const on = (wk.games[t] || []).includes(d);
    const b2 = on && wk.dates && SCHED[t] && SCHED[t].has(addDays(wk.dates[d], -1));
    return /*#__PURE__*/React.createElement("td", {
      key: d,
      className: "px-1 py-1 text-center"
    }, /*#__PURE__*/React.createElement("span", {
      title: b2 ? "2nd night of a back-to-back — backup goalie likely" : "",
      className: "inline-block w-7 h-4 rounded " + (b2 ? "bg-amber-500" : on ? "bg-blue-600" : "bg-slate-200")
    }));
  }), /*#__PURE__*/React.createElement("td", {
    className: "px-2 py-1 text-center font-semibold " + (gms(wk, t) >= 4 ? "text-green-700" : gms(wk, t) <= 1 ? "text-red-600" : "")
  }, gms(wk, t)))), /*#__PURE__*/React.createElement("tr", {
    className: "border-t-2 border-slate-300"
  }, /*#__PURE__*/React.createElement("td", {
    className: "px-2 py-2 font-semibold"
  }, "Games/day"), perDay.map((n, i) => /*#__PURE__*/React.createElement("td", {
    key: i,
    className: "text-center font-semibold " + (n <= 4 ? "text-green-700" : "")
  }, n)), /*#__PURE__*/React.createElement("td", null))))));
}
function Settings({
  s,
  setS
}) {
  const E = window.ESPN_DATA;
  const [io, setIo] = useState("");
  const [msg, setMsg] = useState("");
  const Sg = E && E.signals;
  const download = () => {
    const blob = new Blob([JSON.stringify(s)], {
      type: "application/json"
    });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = `fantasy-gm-backup-${todayISO()}.json`;
    a.click();
    setMsg("Backup file downloaded — keep it somewhere safe.");
  };
  const upload = e => {
    const f = e.target.files && e.target.files[0];
    if (!f) return;
    const r = new FileReader();
    r.onload = () => {
      try {
        const v = JSON.parse(r.result);
        if (v.players && v.weeks) {
          setS(migrate(v));
          setMsg("Backup restored.");
        } else setMsg("That file isn't a backup.");
      } catch (ex) {
        setMsg("Couldn't read that file.");
      }
    };
    r.readAsText(f);
  };
  const row = (ok, label, detail) => /*#__PURE__*/React.createElement("div", {
    className: "flex gap-2 py-1 border-t border-slate-100"
  }, /*#__PURE__*/React.createElement("span", null, /*#__PURE__*/React.createElement("span", {
    className: ok ? "text-green-700" : "text-slate-400"
  }, "\u25CF")), /*#__PURE__*/React.createElement("span", {
    className: "font-medium"
  }, label), /*#__PURE__*/React.createElement("span", {
    className: "text-slate-500 text-xs ml-auto text-right"
  }, detail));
  return /*#__PURE__*/React.createElement("div", {
    className: "grid md:grid-cols-2 gap-4"
  }, /*#__PURE__*/React.createElement(Section, {
    title: "Data sources",
    sub: E ? `${E.leagueName || "Your league"} · synced ${fmtTime(E.generated)}` : "No data file found."
  }, row(!!E, "ESPN league", E ? `${(E.teams || []).length} teams · ${(E.players || []).length} players` : ""), row(!!(E && E.model), "GM model", E && E.model ? `${Object.keys(E.model.base || {}).length} players` : ""), row(!!(E && E.model && E.model.odds && Object.keys(E.model.odds).length), "Betting lines", E && E.model && E.model.odds ? `${Object.keys(E.model.odds).length} days` : ""), row(!!(Sg && Sg.recent), "Recent form", Sg && Sg.recent ? `${Object.keys(Sg.recent).length} players` : ""), row(!!(Sg && Sg.pp1), "PP1 units", Sg && Sg.pp1 ? `checked ${Sg.pp1.asof}` : ""), row(!!(Sg && Sg.news), "News", Sg && Sg.news ? `${Object.keys(Sg.news).length} players` : ""), row(!!(Sg && Sg.injuries), "Injuries", Sg && Sg.injuries ? `${Object.keys(Sg.injuries).length} players` : ""), row(!!(E && E.goalies), "Starting goalies", E && E.goalies ? `${Object.keys(E.goalies).length} days` : ""), E && /*#__PURE__*/React.createElement("button", {
    className: "border border-slate-300 rounded-lg px-3 py-1.5 mt-3 text-xs",
    onClick: () => {
      try {
        setS(applyESPN(s, E));
        setMsg("ESPN data re-applied.");
      } catch (e) {
        setMsg(e.message);
      }
    }
  }, "Re-apply ESPN data")), /*#__PURE__*/React.createElement(Section, {
    title: "Backup & restore",
    sub: "Your settings (goalie start %, return dates, protected players, minimums) live in this browser. Back them up."
  }, /*#__PURE__*/React.createElement("div", {
    className: "flex flex-wrap gap-2"
  }, /*#__PURE__*/React.createElement("button", {
    className: "bg-blue-600 rounded-lg px-3 py-1.5",
    onClick: download
  }, "\u2193 Download backup file"), /*#__PURE__*/React.createElement("label", {
    className: "border border-slate-300 rounded-lg px-3 py-1.5 cursor-pointer"
  }, "\u2191 Restore from file", /*#__PURE__*/React.createElement("input", {
    type: "file",
    accept: ".json,application/json",
    className: "hidden",
    onChange: upload
  }))), msg && /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-green-700 mt-2"
  }, msg), /*#__PURE__*/React.createElement("details", {
    className: "mt-3 text-xs text-slate-500"
  }, /*#__PURE__*/React.createElement("summary", {
    className: "cursor-pointer"
  }, "Copy / paste instead"), /*#__PURE__*/React.createElement("div", {
    className: "flex gap-2 my-2"
  }, /*#__PURE__*/React.createElement("button", {
    className: "border border-slate-300 rounded px-2 py-1",
    onClick: () => setIo(JSON.stringify(s))
  }, "Export text"), /*#__PURE__*/React.createElement("button", {
    className: "border border-slate-300 rounded px-2 py-1",
    onClick: () => {
      try {
        const v = JSON.parse(io);
        if (v.players && v.weeks) {
          setS(migrate(v));
          setMsg("Imported.");
        }
      } catch (e) {
        setMsg("Invalid data");
      }
    }
  }, "Import text")), /*#__PURE__*/React.createElement("textarea", {
    className: inp + " w-full h-24 font-mono text-xs",
    value: io,
    onChange: e => setIo(e.target.value)
  })), /*#__PURE__*/React.createElement("button", {
    className: "text-red-600 text-xs mt-3",
    onClick: () => {
      if (confirm("Reset everything? Download a backup first!")) setS(init());
    }
  }, "Reset all")), /*#__PURE__*/React.createElement(Section, {
    title: "Projection settings"
  }, /*#__PURE__*/React.createElement("label", {
    className: "flex items-center gap-2"
  }, "ESPN projection weight (games) ", /*#__PURE__*/React.createElement("input", {
    type: "number",
    min: "0",
    className: inp + " w-20",
    value: s.blend,
    onChange: e => setS({
      ...s,
      blend: Math.max(0, parseFloat(e.target.value) || 0)
    })
  })), /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500 mt-1"
  }, "How fast real results replace ESPN's projection (10 = half-and-half after 10 games)."), /*#__PURE__*/React.createElement("label", {
    className: "flex items-center gap-2 mt-3"
  }, /*#__PURE__*/React.createElement("input", {
    type: "checkbox",
    checked: s.autoDone,
    onChange: e => setS({
      ...s,
      autoDone: e.target.checked
    })
  }), " Count completed days automatically"), /*#__PURE__*/React.createElement("label", {
    className: "flex items-center gap-2 mt-2"
  }, /*#__PURE__*/React.createElement("input", {
    type: "checkbox",
    checked: s.autoGoalie !== false,
    onChange: e => setS({
      ...s,
      autoGoalie: e.target.checked
    })
  }), " Set goalie start % automatically from recent starts"), /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500 mt-1"
  }, "Uses who started each team's last ~10 games (blended with last season). Kicks in once a team has played 3 games; applied at every sync. Turn off to keep your own numbers.")), /*#__PURE__*/React.createElement(Section, {
    title: "Team names"
  }, s.teams.map(t => /*#__PURE__*/React.createElement("div", {
    key: t.id,
    className: "flex gap-2 mb-1 items-center"
  }, /*#__PURE__*/React.createElement("input", {
    className: inp + " flex-1",
    value: t.name,
    onChange: e => setS({
      ...s,
      teams: s.teams.map(x => x.id === t.id ? {
        ...x,
        name: e.target.value
      } : x)
    })
  }), t.id === s.me && /*#__PURE__*/React.createElement("span", {
    className: "text-xs text-blue-700"
  }, "you")))));
}

// ---------- Clickable names, team pages, My Team (UI refresh) ----------
const TL = ({
  s,
  id,
  className
}) => {
  if (!id) return null;
  const nm = teamName(s, id);
  if (id === "fa") return /*#__PURE__*/React.createElement("span", {
    className: className || ""
  }, nm);
  return /*#__PURE__*/React.createElement("a", {
    href: id === s.me ? "#myteam" : gxHash("teams", null, id),
    className: "hover:underline text-left " + (className || ""),
    onClick: e => {
      /* gx072-tl */e.stopPropagation();
      if (gxNewTab(e)) return;
      e.preventDefault();
      if (window.__NAV) window.__NAV.team(id);
    }
  }, nm);
};
const PN = ({
  p,
  className
}) => /*#__PURE__*/React.createElement("a", {
  href: gxPHref(p),
  className: "hover:underline text-left " + (className === undefined ? "font-medium" : className),
  onClick: e => {
    /* gx072-pn */e.stopPropagation();
    if (gxNewTab(e)) return;
    e.preventDefault();
    if (window.__NAV) window.__NAV.player(p);
  }
}, p.n);
let __LT = null;
function leagueTable(s) {
  const key = [s.players, s.weeks, s.wk, s.blend, s.autoDone, window.__PMODE];
  if (__LT && __LT.key.every((v, i) => v === key[i])) return __LT.v;
  const K = s.blend,
    today = todayISO();
  const rows = s.teams.map(t => {
    const r = s.players.filter(p => p.ft === t.id);
    let ros = 0,
      n4 = 0,
      days = 0;
    s.weeks.slice(s.wk).forEach((w, i) => {
      const dw = deriveWeek(w, s.autoDone);
      const from = i === 0 ? dw.done : 0;
      const v = weekProj(r, dw, K, from).total;
      ros += v;
      if (i < 4) n4 += v;
      days += Math.max(0, dw.days.length - from);
    });
    const perGame = (pos, n) => r.filter(p => p.p === pos && !p.ir && avail(p, today) > 0).map(p => effAvg(p, K) * (pos === "G" ? p.prob : 1)).sort((a, b) => b - a).slice(0, n).reduce((a, b) => a + b, 0);
    const grp = {
      F: perGame("F", 10),
      D: perGame("D", 5),
      G: perGame("G", 2)
    };
    const out = r.filter(p => p.ir || avail(p, today) === 0).length;
    return {
      t,
      ros,
      n4,
      strength: days ? ros / days * 7 : 0,
      grp,
      out
    };
  });
  const rec = {};
  s.teams.forEach(t => rec[t.id] = {
    w: 0,
    l: 0,
    t: 0,
    pf: 0,
    n: 0
  });
  s.weeks.forEach(w => {
    const len = (w.dates || []).length;
    if (!len || effDone(w, s.autoDone) < len) return;
    (w.pairs || []).forEach(([a, b]) => {
      if (!rec[a] || !rec[b]) return;
      const x = +gxAct120(w)[a] || 0,
        y = +gxAct120(w)[b] || 0;
      if (!x && !y) return;
      rec[a].pf += x;
      rec[b].pf += y;
      rec[a].n++;
      rec[b].n++;
      if (x > y) {
        rec[a].w++;
        rec[b].l++;
      } else if (y > x) {
        rec[b].w++;
        rec[a].l++;
      } else {
        rec[a].t++;
        rec[b].t++;
      }
    });
  });
  rows.forEach(x => x.rec = rec[x.t.id]);
  rows.sort((a, b) => b.strength - a.strength);
  const grpRank = {};
  ["F", "D", "G"].forEach(k => {
    [...rows].sort((a, b) => b.grp[k] - a.grp[k]).forEach((x, i) => {
      grpRank[x.t.id] = {
        ...(grpRank[x.t.id] || {}),
        [k]: i + 1
      };
    });
  });
  const v = {
    rows,
    grpRank
  };
  __LT = {
    key,
    v
  };
  return v;
}
const recTxt = r => r && r.n ? `${r.w}-${r.l}${r.t ? "-" + r.t : ""}` : "–";
const RankSpans = ({
  g
}) => /*#__PURE__*/React.createElement("span", null, ["F", "D", "G"].map(k => /*#__PURE__*/React.createElement("span", {
  key: k,
  className: "mr-2 " + (g[k] <= 3 ? "text-green-700" : g[k] >= 8 ? "text-red-600" : "")
}, k, " #", g[k])));
function RosterView({
  s,
  wk,
  team
}) {
  // roster view v9: no Signals column, phone list by position (news_logos.py)
  const K = s.blend,
    done = wk.done || 0;
  const roster = s.players.filter(p => p.ft === team);
  const order = {
    F: 0,
    D: 1,
    G: 2
  };
  const sorted = [...roster].sort((a, b) => (a.ir ? 1 : 0) - (b.ir ? 1 : 0) || order[a.p] - order[b.p] || effAvg(b, K) - effAvg(a, K));
  const Ls = wk.days.map((_, d) => d < done ? null : dayLineup(roster, wk, d, K));
  const wkPts = p => Ls.reduce((a, L) => {
    if (!L) return a;
    const x = L.start.find(y => y.id === p.id);
    return a + (x ? x.x : 0);
  }, 0);
  const left = p => (wk.games[p.t] || []).filter(d => d >= done).length;
  const stTag = p => p.ir ? "IR" : p.status && p.status !== "ACTIVE" ? M_ST[p.status] || p.status.replace(/_/g, " ") : "";
  const groups = [["Forwards", sorted.filter(p => !p.ir && p.p === "F")], ["Defence", sorted.filter(p => !p.ir && p.p === "D")], ["Goalies", sorted.filter(p => !p.ir && p.p === "G")], ["Injured reserve", sorted.filter(p => p.ir)]].filter(g => g[1].length);
  return /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    className: "m-hide overflow-x-auto"
  }, /*#__PURE__*/React.createElement("table", {
    className: "w-full text-sm"
  }, /*#__PURE__*/React.createElement("thead", {
    className: "text-left"
  }, /*#__PURE__*/React.createElement("tr", null, ["Player", "", "Proj / game", "Games left", "Week pts"].map((h, i) => /*#__PURE__*/React.createElement("th", {
    key: i,
    className: "px-2 py-2"
  }, h)))), /*#__PURE__*/React.createElement("tbody", null, sorted.map(p => /*#__PURE__*/React.createElement("tr", {
    key: p.id,
    className: "border-t border-slate-100 align-top"
  }, /*#__PURE__*/React.createElement("td", {
    className: "px-2 py-2 whitespace-nowrap"
  }, /*#__PURE__*/React.createElement(PN, {
    p: p
  }), p.ir ? /*#__PURE__*/React.createElement("span", {
    className: "text-red-600 text-xs ml-1"
  }, "IR") : p.status && p.status !== "ACTIVE" ? /*#__PURE__*/React.createElement("span", {
    className: "text-red-600 text-xs ml-1"
  }, p.status.replace(/_/g, " ")) : null), /*#__PURE__*/React.createElement("td", {
    className: "px-2 py-2 text-xs text-slate-500 whitespace-nowrap"
  }, p.p, " \xB7 ", /*#__PURE__*/React.createElement(GxFace, {
    p: p
  })), /*#__PURE__*/React.createElement("td", {
    className: "px-2 py-2"
  }, f1(effAvg(p, K))), /*#__PURE__*/React.createElement("td", {
    className: "px-2 py-2"
  }, p.ir ? "–" : left(p)), /*#__PURE__*/React.createElement("td", {
    className: "px-2 py-2 font-semibold"
  }, p.ir ? "–" : f1(wkPts(p)))))))), /*#__PURE__*/React.createElement("div", {
    className: "m-only"
  }, groups.map(([title, list]) => /*#__PURE__*/React.createElement("div", {
    key: title,
    className: "mb-2"
  }, /*#__PURE__*/React.createElement("div", {
    className: "m-ghead"
  }, /*#__PURE__*/React.createElement("span", null, title), /*#__PURE__*/React.createElement("span", null, "Proj"), /*#__PURE__*/React.createElement("span", null, "Gms"), /*#__PURE__*/React.createElement("span", null, "Week")), list.map(p => {
    const tg = stTag(p);
    return /*#__PURE__*/React.createElement("div", {
      key: p.id,
      className: "m-rrow",
      role: "button",
      onClick: () => window.__NAV && window.__NAV.player(p)
    }, /*#__PURE__*/React.createElement(GxFace, {
      p: p,
      size: 26
    }), /*#__PURE__*/React.createElement("div", {
      className: "min-w-0"
    }, /*#__PURE__*/React.createElement("div", {
      className: "truncate font-medium"
    }, p.n), /*#__PURE__*/React.createElement("div", {
      className: "text-xs text-slate-500"
    }, p.p, tg ? /*#__PURE__*/React.createElement("span", {
      className: "text-red-600"
    }, " \xB7 ", tg) : null)), /*#__PURE__*/React.createElement("span", {
      className: "m-num"
    }, f1(effAvg(p, K))), /*#__PURE__*/React.createElement("span", {
      className: "m-num"
    }, p.ir ? "–" : left(p)), /*#__PURE__*/React.createElement("span", {
      className: "m-num font-semibold"
    }, p.ir ? "–" : f1(wkPts(p))));
  })))));
}
function MyTeam({
  s,
  setS,
  wk,
  go
}) {
  gxUseSort108(); /* gx109 */
  // team roster v37: one roster list with role, form, schedule and rank (news_logos.py)
  const K = s.blend,
    today = todayISO(),
    gen = (window.ESPN_DATA || {}).generated;
  const [sort, setSort] = useState("pg");
  const [hist, setHist] = useState({});
  const roster = s.players.filter(p => p.ft === s.me);
  const pv = p => effAvg(p, K) * (p.p === "G" ? p.prob : 1);
  const T = leagueTable(s),
    ri = T.rows.findIndex(r => r.t.id === s.me),
    meRow = ri >= 0 ? T.rows[ri] : null,
    g = T.grpRank[s.me] || {};
  const dates = wk.dates || [],
    done = wk.done || 0;
  const nextW = s.weeks[s.wk + 1] ? deriveWeek(s.weeks[s.wk + 1], s.autoDone) : null;
  const mu = useMemo(() => {
    const P = pby(),
      o = {};
    dates.forEach(dt => {
      const AD = actDay(s.me, dt);
      if (!AD) return;
      Object.entries(AD).forEach(([pid, v]) => {
        if (!v || v[0] == null || !ESLOT[v[1]]) return;
        const p = P["e" + pid];
        if (!p || !(SCHED[p.t] && SCHED[p.t].has(dt)) || gState(p.t, dt).s === "P" || p.p === "G" && !v[0]) return;
        o[p.id] = (o[p.id] || 0) + v[0];
      });
    });
    return o;
  }, [s.players, wk, gen]);
  const total = Object.values(mu).reduce((a, v) => a + Math.max(0, v), 0);
  const rankOf = useMemo(() => {
    const o = {};
    ["F", "D", "G"].forEach(k => {
      s.players.filter(p => p.p === k && p.prob > 0 && (p.proj !== false || p.gp > 0)).map(p => [p.id, pv(p)]).sort((a, b) => b[1] - a[1]).forEach((x, i) => o[x[0]] = i + 1);
    });
    return o;
  }, [s.players, K, window.__PMODE]);
  const roles = useMemo(() => {
    const L = window.LINES_DATA,
      o = {};
    if (!L || !L.teams) return o;
    const key = x => nrm(x).replace(/[.'\u2019]/g, "").replace(/-/g, " ").replace(/\s+/g, " ").trim();
    roster.forEach(p => {
      const ln = (L.teams[p.t] || {}).lines;
      if (!ln) return;
      const k = key(p.n),
        has = sl => (ln[sl] || []).some(x => key(x) === k);
      o[p.id] = {
        es: ["F1", "F2", "F3", "F4", "D1", "D2", "D3", "G"].find(has),
        pp: ["PP1", "PP2"].find(has)
      };
    });
    return o;
  }, [s.players, (window.LINES_DATA || {}).generated]);
  useEffect(() => {
    let dead = false;
    const E = window.ESPN_DATA || {},
      sc = s.sc || {},
      out = {},
      byId = {};
    roster.forEach(p => byId[String(p.id).slice(1)] = p);
    Object.entries(E.daily || {}).forEach(([d, Tm]) => Object.values(Tm || {}).forEach(tm => Object.entries(tm || {}).forEach(([pid, v]) => {
      const p = byId[pid];
      if (!p || !v || v[0] == null || !(SCHED[p.t] && SCHED[p.t].has(d)) || gState(p.t, d).s === "P" || p.p === "G" && !v[0]) return;
      (out[pid] = out[pid] || {})[d] = v[0];
    })));
    const est = x => x.sv != null ? (x.dec === "W" ? sc.W ?? 5 : 0) + (x.dec === "O" ? sc.OTL ?? 1 : 0) + (x.sv || 0) * (sc.SV ?? 0.6) + (x.ga || 0) * (sc.GA ?? -3) : (x.g || 0) * (sc.G ?? 6) + (x.a || 0) * (sc.A ?? 4) + (x.pm || 0) * (sc.PM ?? 2) + (x.sog || 0) * (sc.SOG ?? 1) + (x.hit || 0) * (sc.HIT ?? 0.1) + (x.blk || 0) * (sc.BLK ?? 1) + (x.ppg || 0) * (sc.PPP ?? 2);
    const finish = () => {
      if (dead) return;
      const h = {};
      Object.keys(out).forEach(pid => {
        h[pid] = Object.keys(out[pid]).sort().slice(-5).map(d => ({
          d,
          v: out[pid][d]
        }));
      });
      setHist(h);
    };
    finish();
    gxBoxIdx().then(ds => Promise.all(ds.slice(-14).map(d => gxBoxDay(d).then(day => [d, day])))).then(days => {
      days.forEach(([d, day]) => {
        if (!day) return;
        Object.keys(byId).forEach(pid => {
          const x = day[pid];
          if (x) {
            const o2 = out[pid] = out[pid] || {};
            o2[d] = x.fp != null ? x.fp : o2[d] != null ? o2[d] : est(x);
          } else if (out[pid]) delete out[pid][d];
        });
      });
      finish();
    }).catch(() => {});
    return () => {
      dead = true;
    };
  }, [s.players, gen]);
  const RO = {
    F1: "L1",
    F2: "L2",
    F3: "L3",
    F4: "L4",
    D1: "D1",
    D2: "D2",
    D3: "D3"
  };
  const roleTxt = p => {
    if (p.p === "G") return gxGsTxt106(p);
    const r = roles[p.id];
    if (!r) return "";
    return [r.es ? RO[r.es] : "not in lineup", r.pp].filter(Boolean).join(" \u00b7 ");
  };
  const nextGame = p => {
    const S = SCHED[p.t];
    if (!S || p.ir) return "";
    for (let i = 0; i < 10; i++) {
      const dt = addDays(today, i);
      if (S.has(dt) && (i > 0 || gState(p.t, dt).s === "P")) {
        const gm = gameOf(p.t, dt);
        return (i === 0 ? "Today" : dayLabel(dt).split(",")[0]) + (gm ? (gm.h ? " vs " : " @ ") + gm.o : "");
      }
    }
    return "";
  };
  const left = p => (wk.games[p.t] || []).filter(d => dates[d] >= today && gState(p.t, dates[d]).s === "P").length;
  const nextG = p => nextW ? gms(nextW, p.t) : 0;
  const keyFn = {
    mu: p => mu[p.id] || 0,
    left,
    next: nextG,
    sea: p => p.gp ? p.tot / p.gp : -99,
    pg: pv,
    rk: p => -(rankOf[p.id] || 9999),
    l5: p => gxL5v(hist[String(p.id).slice(1)])
  }[sort]; // change 079: Last 5 sorts too
  const grp = k => roster.filter(p => !p.ir && p.p === k).sort((a, b) => keyFn(b) - keyFn(a));
  const groups = [["Forwards", grp("F")], ["Defence", grp("D")], ["Goalies", grp("G")], ["Injured reserve", roster.filter(p => p.ir)]].filter(x => x[1].length);
  const healthy = roster.filter(p => !p.ir).sort((a, b) => gxPgAvg(b, K) - gxPgAvg(a, K)); /* gx088-r */
  const prot = new Set([...healthy.slice(0, s.protectTop ?? 8).map(p => p.id), ...roster.filter(p => p.keep).map(p => p.id)]);
  const weak = healthy.filter(p => !prot.has(p.id)).sort((a, b) => pv(a) - pv(b)).slice(0, 3);
  const HB = (k, l, cls) => /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: "n " + (cls || "") + (sort === k ? " on" : ""),
    onClick: () => setSort(sort === k ? "pg" : k)
  }, l);
  const spark = p => {
    const h = hist[String(p.id).slice(1)] || [];
    return /*#__PURE__*/React.createElement("div", {
      className: "gx-sp m-hide",
      title: "Last five games, oldest to newest"
    }, h.length ? h.map((x, i) => /*#__PURE__*/React.createElement("i", {
      key: i,
      style: {
        height: Math.max(2, Math.min(22, Math.max(0, x.v) / 20 * 22)),
        background: x.v < 0 ? "var(--bad)" : "var(--ink2)"
      }
    })) : /*#__PURE__*/React.createElement("span", {
      className: "text-xs text-slate-500"
    }, "\u2013"));
  };
  const row = p => {
    const st = p.ir ? "IR" : p.status && p.status !== "ACTIVE" ? M_ST[p.status] || p.status.replace(/_/g, " ") : "";
    const m = mu[p.id],
      sea = p.gp ? p.tot / p.gp : null,
      gap = sea != null && p.avg > 0 ? sea - p.avg : null,
      rk = rankOf[p.id];
    const sub = [roleTxt(p), nextGame(p)].filter(Boolean).join(" \u00b7 ");
    return /*#__PURE__*/React.createElement("div", {
      key: p.id,
      className: "gx-ro"
    }, /*#__PURE__*/React.createElement("div", {
      className: "gx-fc99"
    }, /*#__PURE__*/React.createElement(GxFace, {
      p: p,
      size: 26
    })), /*#__PURE__*/React.createElement("div", {
      className: "min-w-0"
    }, /*#__PURE__*/React.createElement("div", {
      className: "truncate"
    }, /*#__PURE__*/React.createElement(PN, {
      p: p,
      className: ""
    }), st ? /*#__PURE__*/React.createElement("span", {
      className: "text-xs",
      style: {
        color: "var(--bad)",
        marginLeft: 8
      }
    }, st) : null), sub ? /*#__PURE__*/React.createElement("div", {
      className: "text-xs text-slate-500 truncate"
    }, sub) : null), gxToday99(p), spark(p), /*#__PURE__*/React.createElement("div", {
      className: "n"
    }, /*#__PURE__*/React.createElement("div", {
      className: "font-semibold",
      style: p.p === "G" && m != null ? {
        color: m > 5 ? "var(--good)" : m < 0 ? "var(--bad)" : "var(--ink)"
      } : null
    }, m == null ? "\u2013" : f1(m)), m > 0 && total > 0 ? /*#__PURE__*/React.createElement("div", {
      style: {
        height: 3,
        background: "var(--track)",
        marginTop: 3
      }
    }, /*#__PURE__*/React.createElement("div", {
      style: {
        height: 3,
        width: Math.min(100, m / total * 100) + "%",
        background: "var(--accent)"
      }
    })) : null), /*#__PURE__*/React.createElement("div", {
      className: "n text-slate-500"
    }, p.ir ? "\u2013" : left(p)), /*#__PURE__*/React.createElement("div", {
      className: "n text-slate-500 m-hide"
    }, nextW && !p.ir ? nextG(p) : "\u2013"), /*#__PURE__*/React.createElement("div", {
      className: "n m-hide"
    }, sea == null ? "\u2013" : f1(sea), p.p === "G" && gxGS106(p) ? /*#__PURE__*/React.createElement("span", {
      className: "gx-gs106"
    }, gxGS106(p).pct) : null), /*#__PURE__*/React.createElement("div", {
      className: "n"
    }, f1(effAvg(p, K))), /*#__PURE__*/React.createElement("div", {
      className: "n text-xs text-slate-500 m-hide"
    }, rk ? p.p + " " + ordN(rk) : "\u2013"), /*#__PURE__*/React.createElement(GxSC106, {
      p: p,
      s: s,
      mode: "full"
    }));
  };
  const rkc = v => v >= 8 ? {
    color: "var(--bad)"
  } : v && v <= 3 ? {
    color: "var(--good)"
  } : null;
  const order = {
    F: 0,
    D: 1,
    G: 2
  };
  const sorted = [...roster].sort((a, b) => (a.ir ? 1 : 0) - (b.ir ? 1 : 0) || order[a.p] - order[b.p] || effAvg(b, K) - effAvg(a, K));
  const Ls = wk.days.map((_, d) => d < done ? null : dayLineup(roster, wk, d, K));
  const cell = (p, d) => {
    if (p.ir || !(wk.games[p.t] || []).includes(d)) return "none";
    const L = Ls[d];
    if (!L) return "past";
    if (L.start.some(x => x.id === p.id)) return "start";
    if (L.bench.some(x => x.id === p.id)) return "sit";
    return "out";
  };
  const CELL = {
    start: "bg-green-500",
    sit: "bg-amber-500",
    out: "bg-red-500",
    past: "bg-slate-200"
  };
  return /*#__PURE__*/React.createElement("div", {
    className: "space-y-3"
  }, /*#__PURE__*/React.createElement("div", {
    className: "text-sm",
    style: {
      display: "flex",
      flexWrap: "wrap",
      gap: "6px 18px"
    }
  }, /*#__PURE__*/React.createElement("span", null, /*#__PURE__*/React.createElement("span", {
    className: "text-slate-500"
  }, "Strength"), " ", meRow ? f1(meRow.strength) : "\u2013", " a week"), /*#__PURE__*/React.createElement("span", null, /*#__PURE__*/React.createElement("span", {
    className: "text-slate-500"
  }, "Forwards"), " ", /*#__PURE__*/React.createElement("span", {
    style: rkc(g.F)
  }, g.F ? ordN(g.F) : "\u2013")), /*#__PURE__*/React.createElement("span", null, /*#__PURE__*/React.createElement("span", {
    className: "text-slate-500"
  }, "Defence"), " ", /*#__PURE__*/React.createElement("span", {
    style: rkc(g.D)
  }, g.D ? ordN(g.D) : "\u2013")), /*#__PURE__*/React.createElement("span", null, /*#__PURE__*/React.createElement("span", {
    className: "text-slate-500"
  }, "Goalies"), " ", /*#__PURE__*/React.createElement("span", {
    style: rkc(g.G)
  }, g.G ? ordN(g.G) : "\u2013"))), /*#__PURE__*/React.createElement("div", {
    className: "gx-pn"
  }, /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement(GxRngSel100, null), /*#__PURE__*/React.createElement("div", {
    className: "gx-sc99"
  }, /*#__PURE__*/React.createElement("div", {
    className: "gx-ro gx-roh"
  }, /*#__PURE__*/React.createElement("span", null), /*#__PURE__*/React.createElement("span", null, "Player"), /*#__PURE__*/React.createElement("span", null, "Today"), /*#__PURE__*/React.createElement("span", {
    className: "n"
  }, "Pts"), HB("l5", "Last 5", "m-hide"), HB("mu", "Matchup"), HB("left", "Left"), HB("next", "Next wk", "m-hide"), /*#__PURE__*/React.createElement(GxHB108, {
    k: "Avg"
  }), /*#__PURE__*/React.createElement(GxHB108, {
    k: "Exp",
    l: "Expected"
  }), /*#__PURE__*/React.createElement(GxHB108, {
    k: "Rank"
  }), /*#__PURE__*/React.createElement(GxSH106, {
    mode: "sk"
  })), groups.map(([title, list]) => /*#__PURE__*/React.createElement("div", {
    key: title,
    style: {
      marginBottom: 10
    }
  }, /*#__PURE__*/React.createElement("div", {
    className: "gx-tag",
    style: {
      padding: "8px 0 4px"
    }
  }, title), title === "Goalies" ? /*#__PURE__*/React.createElement(GxGH104, null) : null, gxSort108(list, s).map(row))))));
}
function TeamsTab({
  s,
  wk,
  openTeam
}) {
  const T = leagueTable(s);
  return /*#__PURE__*/React.createElement(Section, {
    title: "Teams",
    sub: "Every team in your league, ordered by power ranking. Tap a team to see its roster, its week and how it fits with yours for trades."
  }, /*#__PURE__*/React.createElement("div", {
    className: "grid sm:grid-cols-2 lg:grid-cols-3 gap-3 mt-2"
  }, T.rows.map((x, i) => {
    const g = T.grpRank[x.t.id] || {};
    const o = oppOf(wk, x.t.id);
    const me = x.t.id === s.me;
    return /*#__PURE__*/React.createElement("div", {
      key: x.t.id,
      role: "button",
      onClick: () => openTeam(x.t.id),
      className: "rounded-xl border p-4 cursor-pointer hover:border-slate-400 " + (me ? "border-blue-500 bg-blue-50" : "border-slate-200 bg-slate-50")
    }, /*#__PURE__*/React.createElement("div", {
      className: "flex items-baseline gap-2"
    }, /*#__PURE__*/React.createElement("span", {
      className: "text-slate-400 text-sm"
    }, "#", i + 1), /*#__PURE__*/React.createElement("span", {
      className: "font-semibold truncate"
    }, x.t.name), me && /*#__PURE__*/React.createElement("span", {
      className: "text-xs text-blue-600 ml-auto"
    }, "You")), /*#__PURE__*/React.createElement("div", {
      className: "text-xs text-slate-500 mt-1"
    }, x.rec && x.rec.n ? `${recTxt(x.rec)} · ${f1(x.rec.pf)} PF · ` : "", f1(x.strength), " pts/wk projected"), /*#__PURE__*/React.createElement("div", {
      className: "text-xs mt-2"
    }, /*#__PURE__*/React.createElement(RankSpans, {
      g: g
    })), /*#__PURE__*/React.createElement("div", {
      className: "text-xs text-slate-500 mt-2"
    }, o ? `This week vs ${teamName(s, o)}` : "No matchup loaded", x.out ? ` · ${x.out} out` : ""));
  })));
}
function TeamPage(props) {
  // team page v51: new style, with the older detailed view one tap away (news_logos.py)
  const {
      s,
      wk
    } = props,
    tid = props.id,
    back = props.back;
  const [old, setOld] = useState(false);
  if (old || !tid || !s || !wk) return /*#__PURE__*/React.createElement(TeamPage0, props);
  const K = s.blend,
    today = todayISO(),
    dates = wk.dates || [];
  const T = leagueTable(s),
    pr = T.rows.findIndex(x => x.t.id === tid),
    row = pr >= 0 ? T.rows[pr] : null;
  const g = T.grpRank[tid] || {},
    mg = T.grpRank[s.me] || {};
  const roster = s.players.filter(p => p.ft === tid);
  const opp = oppOf(wk, tid),
    sc = id => +gxAct120(wk)[id] || 0;
  const left = p => (wk.games[p.t] || []).filter(d => dates[d] >= today && gState(p.t, dates[d]).s === "P").length;
  const pv = p => effAvg(p, K) * (p.p === "G" ? p.prob : 1);
  const grp = k => roster.filter(p => !p.ir && p.p === k).sort((a, b) => pv(b) - pv(a));
  const groups = [["Forwards", grp("F")], ["Defence", grp("D")], ["Goalies", grp("G")], ["Injured reserve", roster.filter(p => p.ir)]].filter(x => x[1].length);
  const trade = () => {
    window.__TRADE_P = {
      id: null,
      ft: tid
    };
    if (props.go) props.go("moves", "trades");
    setTimeout(() => window.dispatchEvent(new Event("gm-trade")), 50);
  };
  return /*#__PURE__*/React.createElement("div", {
    className: "space-y-3"
  }, /*#__PURE__*/React.createElement("div", {
    className: "flex items-center gap-3 flex-wrap"
  }, back ? /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: "text-sm text-blue-600",
    onClick: back
  }, "\u2039 Back") : null, /*#__PURE__*/React.createElement("span", {
    className: "font-semibold",
    style: {
      fontSize: 18
    }
  }, teamName(s, tid)), /*#__PURE__*/React.createElement("span", {
    className: "text-sm text-slate-500"
  }, [row && row.rec.n ? row.rec.w + "-" + row.rec.l : "", pr >= 0 ? ordN(pr + 1) + " in strength" : "", row ? Math.round(row.strength) + " a week" : ""].filter(Boolean).join(" \u00b7 ")), tid !== s.me ? /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: "border border-slate-300 rounded-lg px-3 py-1 text-sm",
    style: {
      marginLeft: "auto"
    },
    onClick: trade
  }, "Trade with them") : null), /*#__PURE__*/React.createElement("div", {
    className: "grid md:grid-cols-2 gap-3"
  }, /*#__PURE__*/React.createElement(GxPanel, {
    title: "This week"
  }, opp ? /*#__PURE__*/React.createElement("div", {
    className: "flex items-baseline gap-3"
  }, /*#__PURE__*/React.createElement("span", {
    className: "gx-stv"
  }, f1(sc(tid))), /*#__PURE__*/React.createElement("span", {
    className: "text-slate-500"
  }, "to"), /*#__PURE__*/React.createElement("span", {
    className: "gx-stv",
    style: {
      color: "var(--ink2)"
    }
  }, f1(sc(opp))), /*#__PURE__*/React.createElement("span", {
    className: "text-sm text-slate-500 truncate"
  }, "vs ", teamName(s, opp))) : /*#__PURE__*/React.createElement("div", {
    className: "text-sm text-slate-500"
  }, "No matchup this week.")), /*#__PURE__*/React.createElement(GxPanel, {
    title: "Against you",
    right: "league rank by position"
  }, [["Forwards", "F"], ["Defence", "D"], ["Goalies", "G"]].map(([lab, k], i) => /*#__PURE__*/React.createElement("div", {
    key: k,
    className: "gx-row",
    style: i ? null : {
      borderTop: 0
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      flex: 1
    }
  }, lab), /*#__PURE__*/React.createElement("span", {
    style: {
      color: g[k] && mg[k] && g[k] < mg[k] ? "var(--good)" : "var(--ink)"
    }
  }, g[k] ? ordN(g[k]) : "\u2013"), /*#__PURE__*/React.createElement("span", {
    className: "text-xs text-slate-500",
    style: {
      minWidth: 76,
      textAlign: "right"
    }
  }, tid === s.me ? "" : "you " + (mg[k] ? ordN(mg[k]) : "\u2013")))))), /*#__PURE__*/React.createElement(GxRosterTable, {
    s: s,
    wk: wk,
    tid: tid
  }), /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: "text-xs text-slate-500 underline",
    onClick: () => setOld(true)
  }, "Show the older detailed view"));
}
function TeamPage0({
  s,
  wk,
  id,
  back,
  go
}) {
  const K = s.blend;
  const T = leagueTable(s);
  const x = T.rows.find(r => r.t.id === id);
  if (!x) return /*#__PURE__*/React.createElement(Section, {
    title: "Team not found"
  }, /*#__PURE__*/React.createElement("button", {
    className: "text-blue-600",
    onClick: back
  }, "\u2190 Back"));
  const rank = T.rows.indexOf(x) + 1,
    g = T.grpRank[id] || {},
    mg = T.grpRank[s.me] || {};
  const roster = s.players.filter(p => p.ft === id);
  const done = wk.done || 0,
    o = oppOf(wk, id);
  const act = t => +gxAct120(wk)[t] || 0;
  const mine = weekLive(roster, wk, K, id),
    theirs = o ? weekLive(s.players.filter(p => p.ft === o), wk, K, o) : null;
  const posName = {
    F: "forwards",
    D: "defence",
    G: "goalies"
  };
  const need = {
    F: 10,
    D: 5,
    G: 2
  };
  const myWeak = ["F", "D", "G"].sort((a, b) => (mg[b] || 0) - (mg[a] || 0))[0];
  const theyStrong = ["F", "D", "G"].filter(k => g[k] < mg[k]);
  const pv = p => effAvg(p, K) * (p.p === "G" ? p.prob : 1);
  const myAt = s.players.filter(p => p.ft === s.me && !p.ir && p.p === myWeak).map(pv).sort((a, b) => b - a);
  const bar = myAt.length ? myAt[Math.min(need[myWeak], myAt.length) - 1] : 0;
  const targets = roster.filter(p => !p.ir && p.p === myWeak && pv(p) > bar).sort((a, b) => pv(b) - pv(a)).slice(0, 4);
  const news = roster.filter(p => newsOf(p).length).slice(0, 6);
  return /*#__PURE__*/React.createElement("div", {
    className: "space-y-4"
  }, /*#__PURE__*/React.createElement("button", {
    className: "text-sm text-blue-600",
    onClick: back
  }, "\u2190 Back"), /*#__PURE__*/React.createElement("div", {
    className: "bg-white rounded-xl border border-slate-200 p-4"
  }, /*#__PURE__*/React.createElement("div", {
    className: "text-xs uppercase tracking-wide text-slate-500"
  }, "Power rank #", rank, " of ", T.rows.length), /*#__PURE__*/React.createElement("div", {
    className: "text-2xl font-bold mt-1"
  }, x.t.name), /*#__PURE__*/React.createElement("div", {
    className: "grid grid-cols-2 md:grid-cols-4 gap-3 mt-4"
  }, /*#__PURE__*/React.createElement(Card, {
    label: "Record",
    value: recTxt(x.rec),
    sub: x.rec && x.rec.n ? `${f1(x.rec.pf)} points for` : "no completed weeks yet"
  }), /*#__PURE__*/React.createElement(Card, {
    label: "Strength",
    value: f1(x.strength),
    sub: "projected pts per week"
  }), /*#__PURE__*/React.createElement(Card, {
    label: "Group ranks",
    value: /*#__PURE__*/React.createElement(RankSpans, {
      g: g
    }),
    sub: `among ${T.rows.length} teams`
  }), /*#__PURE__*/React.createElement(Card, {
    label: "Players out",
    value: x.out,
    sub: "injured or on IR"
  }))), /*#__PURE__*/React.createElement("div", {
    className: "grid md:grid-cols-2 gap-4"
  }, /*#__PURE__*/React.createElement(Section, {
    title: "Their week",
    sub: wk.label,
    link: ["All matchups", () => go("matchup")]
  }, o ? /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    className: "flex justify-between py-2"
  }, /*#__PURE__*/React.createElement("span", {
    className: "font-medium"
  }, x.t.name), /*#__PURE__*/React.createElement("span", {
    className: "font-semibold"
  }, f1(act(id) + mine.total))), /*#__PURE__*/React.createElement("div", {
    className: "flex justify-between py-2 border-t border-slate-100"
  }, /*#__PURE__*/React.createElement(TL, {
    s: s,
    id: o
  }), /*#__PURE__*/React.createElement("span", {
    className: "font-semibold"
  }, f1(act(o) + theirs.total))), /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500 mt-1"
  }, mine.used, " lineup games left \xB7 ", mine.wasted, " would sit \xB7 ", mine.empty, " empty slots")) : /*#__PURE__*/React.createElement("div", {
    className: "text-slate-400"
  }, "No matchup loaded for this week.")), /*#__PURE__*/React.createElement(Section, {
    title: "Trade fit with you",
    sub: `Your weakest group: ${posName[myWeak]} (#${mg[myWeak]}). Theirs: F #${g.F} · D #${g.D} · G #${g.G}.`
  }, theyStrong.length ? /*#__PURE__*/React.createElement("div", {
    className: "mb-2"
  }, "They're stronger than you at ", /*#__PURE__*/React.createElement("b", null, theyStrong.map(k => posName[k]).join(" and ")), ".") : /*#__PURE__*/React.createElement("div", {
    className: "mb-2 text-slate-500"
  }, "They're not stronger than you anywhere, so trade only for specific players."), /*#__PURE__*/React.createElement("div", {
    className: "font-medium mt-2 mb-1"
  }, "Players who'd upgrade your ", posName[myWeak]), targets.length ? targets.map(p => /*#__PURE__*/React.createElement("div", {
    key: p.id,
    className: "flex gap-2 py-1.5 border-t border-slate-100"
  }, /*#__PURE__*/React.createElement(PN, {
    p: p
  }), /*#__PURE__*/React.createElement("span", {
    className: "text-xs text-slate-400"
  }, p.p, " \xB7 ", /*#__PURE__*/React.createElement(GxFace, {
    p: p
  })), /*#__PURE__*/React.createElement("span", {
    className: "ml-auto text-xs text-slate-500"
  }, f1(pv(p)), "/game"))) : /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-400"
  }, "None of their ", posName[myWeak], " beat your current starters."), /*#__PURE__*/React.createElement("button", {
    className: "bg-blue-600 rounded-lg px-3 py-1.5 mt-3 text-sm font-semibold",
    onClick: () => go("moves", "trades", {
      partner: id
    })
  }, "Trade with them"))), /*#__PURE__*/React.createElement(Section, {
    title: "Roster",
    sub: "Lineup order: forwards, defence, goalies, then IR. Tap a player for details."
  }, /*#__PURE__*/React.createElement(RosterView, {
    s: s,
    wk: wk,
    team: id
  })), news.length > 0 && /*#__PURE__*/React.createElement(Section, {
    title: "News"
  }, news.map(p => /*#__PURE__*/React.createElement(PlayerLine, {
    key: p.id,
    s: s,
    p: p
  }))));
}
function AdviceAll(props) {
  return /*#__PURE__*/React.createElement(AdvicePage, props);
}
function PlannerAll(props) {
  return /*#__PURE__*/React.createElement(PlanPage, props);
}
function TradesPanel(props) {
  // trades v10: analyzer and 2-for-1 merged into one builder (news_logos.py)
  // change 078: build a trade from any team's side, not only yours
  const s = props.s;
  const [side, setSide] = useState(s.me);
  const [from113, setFrom113] = useState(false);
  window.__TB_REAL = s.me;
  const a = s.teams.some(t => t.id === side) ? side : s.me;
  const s2 = a === s.me ? s : {
    ...s,
    me: a,
    opp: null
  };
  const ip = props.initPartner && props.initPartner !== a ? props.initPartner : null;
  return /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    className: "gx-th113",
    "data-c78": "side"
  }, a === s.me ? "Trading as you" : "Trading as " + teamName(s, a), /*#__PURE__*/React.createElement("button", {
    type: "button",
    onClick: () => setFrom113(!from113)
  }, from113 ? "Done" : "Change"), a !== s.me ? /*#__PURE__*/React.createElement("button", {
    type: "button",
    onClick: () => setSide(s.me)
  }, "Back to mine") : null), from113 ? /*#__PURE__*/React.createElement("select", {
    className: inp + " w-full",
    style: {
      marginBottom: 12
    },
    value: a,
    onChange: e => {
      setSide(e.target.value);
      setFrom113(false);
    }
  }, s.teams.map(t => /*#__PURE__*/React.createElement("option", {
    key: t.id,
    value: t.id
  }, t.name, t.id === s.me ? " (you)" : ""))) : null, a !== s.me ? /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500",
    style: {
      margin: "-4px 0 12px"
    }
  }, "Showing the trade from " + teamName(s, a).trim() + "'s side. Pick who they trade with below.") : null, /*#__PURE__*/React.createElement(TradeBuilder, _extends({
    key: a
  }, props, {
    s: s2,
    initPartner: ip
  })));
}

// ---------- Phone notifications feed (reads notify_outbox.json) ----------
function PhoneFeed() {
  const [box, setBox] = useState(null);
  const [err, setErr] = useState("");
  const [show, setShow] = useState(5);
  const load = () => fetch("notify_outbox.json?t=" + Date.now()).then(r => r.ok ? r.json() : Promise.reject(r.status)).then(b => {
    setBox(b);
    setErr("");
  }).catch(() => setErr("No notification history yet. It appears after the next sync."));
  useEffect(() => {
    load();
    const id = setInterval(load, 2 * 60 * 1000);
    return () => clearInterval(id);
  }, []);
  const when = iso => {
    const d = toDate(iso);
    return d ? d.toLocaleString("en-US", {
      weekday: "short",
      month: "short",
      day: "numeric",
      hour: "numeric",
      minute: "2-digit"
    }) : "";
  };
  const SEC = {
    lineup: "Lineup",
    mine: "Your players",
    pickup: "Pickup idea",
    other: "Other"
  };
  const items = box && box.items || [];
  const waiting = items.filter(i => !i.sent).reverse();
  const urgent = items.filter(i => i.sent && (i.via === "urgent" || !i.via && i.urgent)).map(i => ({
    at: i.sent_at || i.at,
    kind: "urgent",
    title: i.title,
    body: i.text
  }));
  const sent = [...urgent, ...(box && box.log || [])].sort((a, b) => a.at < b.at ? 1 : -1);
  const label = {
    urgent: "Sent right away",
    morning: "Morning summary",
    pregame: "Pre-game summary"
  };
  return /*#__PURE__*/React.createElement(Section, {
    title: "Phone notifications",
    sub: "Everything your phone gets from ntfy, newest first. Checks for new ones every 2 minutes."
  }, err ? /*#__PURE__*/React.createElement("div", {
    className: "text-slate-400"
  }, err) : !box ? /*#__PURE__*/React.createElement("div", {
    className: "text-slate-400"
  }, "Loading\u2026") : /*#__PURE__*/React.createElement("div", {
    className: "space-y-5 mt-2"
  }, /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    className: "text-xs uppercase tracking-wide text-slate-400 mb-1"
  }, "Waiting for the next summary (", waiting.length, ")"), waiting.length ? waiting.map(i => /*#__PURE__*/React.createElement("div", {
    key: i.k,
    className: "flex flex-wrap items-baseline gap-2 py-2 border-t border-slate-100"
  }, /*#__PURE__*/React.createElement("span", {
    className: "text-xs px-2 py-0.5 rounded " + (i.urgent ? "bg-red-100 text-red-600" : "bg-slate-200 text-slate-500")
  }, i.urgent ? "Urgent (quiet hours)" : SEC[i.section] || "Other"), /*#__PURE__*/React.createElement("span", {
    className: "text-sm text-slate-700 flex-1 min-w-[200px]"
  }, i.text), /*#__PURE__*/React.createElement("span", {
    className: "text-xs text-slate-400"
  }, when(i.at)))) : /*#__PURE__*/React.createElement("div", {
    className: "text-sm text-slate-400"
  }, "Nothing waiting.")), /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    className: "text-xs uppercase tracking-wide text-slate-400 mb-1"
  }, "Sent to your phone"), sent.length ? sent.slice(0, show).map((m, i) => /*#__PURE__*/React.createElement("div", {
    key: i,
    className: "py-3 border-t border-slate-100"
  }, /*#__PURE__*/React.createElement("div", {
    className: "flex flex-wrap items-baseline gap-2"
  }, /*#__PURE__*/React.createElement("span", {
    className: "text-xs px-2 py-0.5 rounded " + (m.kind === "urgent" ? "bg-red-100 text-red-600" : "bg-blue-50 text-blue-600")
  }, label[m.kind] || m.kind), /*#__PURE__*/React.createElement("span", {
    className: "font-medium"
  }, m.title), /*#__PURE__*/React.createElement("span", {
    className: "text-xs text-slate-400 ml-auto"
  }, when(m.at))), /*#__PURE__*/React.createElement("div", {
    className: "text-sm text-slate-600 mt-1 whitespace-pre-wrap"
  }, m.body))) : /*#__PURE__*/React.createElement("div", {
    className: "text-sm text-slate-400"
  }, "Nothing sent yet. Your first summary arrives after 8 AM."), sent.length > show && /*#__PURE__*/React.createElement("button", {
    className: "text-sm text-blue-600 mt-2",
    onClick: () => setShow(show + 12)
  }, "Show older"))));
}
// ---------- team logos, game times and news filter (news_logos.py) ----------
const NHL_LOGO = {
  LA: "LAK",
  NJ: "NJD",
  SJ: "SJS",
  TB: "TBL"
};
function TeamLogo({
  t,
  size
}) {
  const [bad, setBad] = useState(false);
  if (!t) return null;
  const z = size || 28;
  if (bad) return /*#__PURE__*/React.createElement("span", null, t);
  return /*#__PURE__*/React.createElement("img", {
    src: "https://assets.nhle.com/logos/nhl/svg/" + (NHL_LOGO[t] || t) + (document.documentElement.getAttribute("data-theme") === "light" ? "_light.svg" : "_dark.svg"),
    alt: t,
    title: t,
    loading: "lazy",
    onError: () => setBad(true),
    style: {
      width: z,
      height: z,
      objectFit: "contain",
      display: "inline-block",
      verticalAlign: "middle"
    }
  });
}
const gameOf = (t, dt) => {
  const G = (window.GAMES_DATA || {}).games || {};
  return dt && G[dt] ? G[dt][t] || null : null;
};
const gameTime = g => {
  const d = g && g.st ? new Date(g.st) : null;
  return d && !isNaN(d) ? d.toLocaleTimeString([], {
    hour: "numeric",
    minute: "2-digit"
  }) : "time TBD";
};
const NEWS_JUNK = /highlights|draft board|rankings|mailbag|podcast|give me a reason|league-winners|sleepers|\bbusts\b|best bets|predictions|betting|\bodds\b|takeaways|\bgrades\b|cheat sheet|start.?sit|waiver wire|what we learned/i;
const NEWS_KINDS = [["trade", "Trade", /\btrade|traded|acquir|deal sends/i], ["scratch", "Scratched", /scratch/i], ["susp", "Suspended", /suspen/i], ["injury", "Injury", /injur|\bIR\b|surgery|day-to-day|week-to-week|month-to-month|out for|out indefinitely|will miss|expected to miss|sidelined|concussion|upper-body|lower-body|leaves game|left the game|ruled out|won't play|will not play|questionable|doubtful/i], ["roster", "Roster move", /waive|claimed|recall|reassign|sent down|assigned to|loaned|signs|signed|extension|contract|released|buyout|activated|returns|back in the lineup|cleared/i], ["hot", "Hot", /streak|hat trick|multi-point|career-high|promot|top line|top-line|first line|pp1|two goals|three points|four points|scores twice|milestone|\brecord\b/i]];
const NEWS_DAYS = {
  trade: 7,
  scratch: 7,
  susp: 7,
  injury: 7,
  roster: 7,
  hot: 3,
  news: 1
};
const NEWS_RANK = {
  injury: 0,
  scratch: 0,
  susp: 0,
  trade: 1,
  roster: 2,
  hot: 3,
  news: 4
};
const NEWS_BIG = new Set(["trade", "scratch", "susp", "injury", "roster"]);
const NEWS_OUT = new Set(["injury", "scratch", "susp"]);
const NEWS_CLS = {
  injury: "text-red-600",
  scratch: "text-red-600",
  susp: "text-red-600",
  trade: "text-blue-600",
  roster: "text-blue-600",
  hot: "text-orange-600"
};
const NEWS_BADGE = {
  injury: "bg-red-100 text-red-600",
  scratch: "bg-red-100 text-red-600",
  susp: "bg-red-100 text-red-600",
  trade: "bg-blue-50 text-blue-600",
  roster: "bg-slate-200 text-slate-600",
  hot: "bg-amber-100 text-orange-600"
};
const newsAge = d => {
  if (!d) return 0;
  const a = Math.round((fromIso(todayISO()) - fromIso(String(d).slice(0, 10))) / 864e5);
  return isNaN(a) ? 0 : Math.max(0, a);
};
const newsOf = p => {
  const last = nrm(p.n).split(" ").pop();
  return (sigOf(p).news || []).map(n => {
    const h = n.h || "";
    if (!h || NEWS_JUNK.test(h) || !nrm(h).includes(last)) return null;
    const k = NEWS_KINDS.find(x => x[2].test(h));
    const kind = k ? k[0] : "news",
      age = newsAge(n.d);
    return age < NEWS_DAYS[kind] ? {
      ...n,
      kind,
      label: k ? k[1] : "",
      age
    } : null;
  }).filter(Boolean).sort((a, b) => NEWS_RANK[a.kind] - NEWS_RANK[b.kind] || a.age - b.age);
};
const NewsItem = ({
  n
}) => /*#__PURE__*/React.createElement("div", {
  className: "flex flex-wrap items-baseline gap-x-2 mt-1 text-sm"
}, n.label ? /*#__PURE__*/React.createElement("span", {
  className: "text-xs px-1.5 py-0.5 rounded " + (NEWS_BADGE[n.kind] || "")
}, n.label) : null, /*#__PURE__*/React.createElement("a", {
  href: n.u,
  target: "_blank",
  rel: "noreferrer",
  className: "hover:underline text-slate-700"
}, n.h), /*#__PURE__*/React.createElement("span", {
  className: "text-xs text-slate-400"
}, n.age <= 0 ? "today" : n.age === 1 ? "yesterday" : n.age + " days ago"));

// ---------- win probability (news_logos.py) ----------
const normCdf = z => {
  const t = 1 / (1 + 0.2316419 * Math.abs(z));
  const d = 0.3989423 * Math.exp(-z * z / 2);
  const p = d * t * (0.3193815 + t * (-0.3565638 + t * (1.781478 + t * (-1.821256 + t * 1.330274))));
  return z > 0 ? 1 - p : p;
};
// spread of a team's remaining points: game-to-game swings of every lineup player-game + 10% projection error
const projVar = R => {
  let v = (0.1 * R.total) ** 2;
  R.days.forEach(L => {
    if (L) L.start.forEach(p => {
      const z = p.x0 != null ? p.x0 : p.x,
        sd = p.p === "G" ? 3 + 0.8 * z : 1.5 + 0.6 * z;
      v += sd * sd * (p.vf != null ? p.vf : 1);
    });
  });
  return v;
};
const winProb = (A, B, aA, aB) => {
  const m = aA + A.total - (aB + B.total);
  const sd = Math.sqrt(projVar(A) + projVar(B));
  return sd > 0 ? normCdf(m / sd) : m > 0 ? 1 : m < 0 ? 0 : 0.5;
};
const wpTxt = v => Math.round(Math.max(0.01, Math.min(0.99, v)) * 100) + "%";
function winChance(s, roster) {
  const w = deriveWeek(s.weeks[s.wk] || s.weeks[0], s.autoDone);
  const opp = oppOf(w, s.me) || s.opp;
  if (!opp) return null;
  const K = s.blend,
    done = w.done || 0;
  const A = weekLive(roster || s.players.filter(p => p.ft === s.me), w, K, s.me);
  const B = weekLive(s.players.filter(p => p.ft === opp), w, K, opp);
  return winProb(A, B, +gxAct120(w)[s.me] || 0, +gxAct120(w)[opp] || 0);
}
const afterMove = (s, add, drop) => timedMove(s.players.filter(p => p.ft === s.me), s.me, [{
  add,
  drop
}]);
const WinDelta = ({
  s,
  add,
  drop,
  base
}) => {
  const b = base === undefined ? winChance(s) : base;
  const n = winChance(s, afterMove(s, add, drop));
  if (b == null || n == null) return null;
  const d = Math.round(n * 100) - Math.round(b * 100);
  return /*#__PURE__*/React.createElement("span", {
    className: "text-xs whitespace-nowrap " + (d > 0 ? "text-green-700" : d < 0 ? "text-red-600" : "text-slate-500"),
    title: "Chance to win this week's matchup, before and after the move"
  }, "win ", wpTxt(b), " \u2192 ", wpTxt(n));
};

// ---------- round 6: moves left, fill slots, ESPN lineup check, goalie streams, strategy (news_logos.py) ----------
const movesLeft = (s, tid, w) => {
  const E = window.ESPN_DATA || {};
  if (E.acq && w && w.period != null) {
    const a = E.acq[String(tid).replace(/^t/, "")];
    if (a) return Math.max(0, 3 - (+a[String(w.period)] || 0));
  }
  return tid === s.me ? Math.max(0, 3 - ((s.movesUsed || {})[s.wk] || 0)) : null;
};
const gamesMoves = (s, tid, w, R) => {
  const m = movesLeft(s, tid, w);
  return R.used + " games left" + (m != null ? " · " + m + " move" + (m === 1 ? "" : "s") + " left" : "");
};
const dropFor = (s, add) => {
  const K = s.blend,
    mine = s.players.filter(p => p.ft === s.me && !p.ir);
  const prot = new Set([...mine].sort((a, b) => effAvg(b, K) - effAvg(a, K)).slice(0, s.protectTop ?? 8).map(p => p.id));
  const mins = {
    F: s.minF ?? 10,
    D: s.minD ?? 5,
    G: s.minGo ?? 2
  };
  const cnt = {
    F: 0,
    D: 0,
    G: 0
  };
  mine.forEach(p => {
    cnt[p.p]++;
  });
  const pv = p => effAvg(p, K) * (p.p === "G" ? p.prob : 1);
  return mine.filter(p => !prot.has(p.id) && !p.keep && (p.p === add.p || cnt[p.p] - 1 >= mins[p.p])).sort((a, b) => pv(a) - pv(b))[0] || null;
};
function GoalieStreams({
  s,
  setS,
  wk
}) {
  // goalies v65: one list of every goalie, any day, yours and free agents marked (news_logos.py)
  const K = s.blend,
    today = todayISO(),
    E = window.ESPN_DATA || {};
  const [day, setDay] = useState(today);
  const [box, setBox] = useState({});
  const [sim, setSim] = useState(null);
  const touch = React.useRef(null);
  const GD = (window.GAMES_DATA || {}).games || {};
  const minD = ((s.weeks[0] || {}).dates || [])[0] || "2026-09-29";
  const lastG = Object.keys(GD).sort().pop() || addDays(today, 35);
  const maxD = lastG > today ? lastG : today;
  const go = n => {
    const x = addDays(day, n);
    if (x >= minD && x <= maxD) setDay(x);
  };
  useEffect(() => {
    if (day > today || box[day] !== undefined) return;
    let dead = false;
    gxBoxDay(day).then(m => {
      if (!dead) setBox(b => ({
        ...b,
        [day]: m || null
      }));
    });
    return () => {
      dead = true;
    };
  }, [day]);
  const played = useMemo(() => {
    const P = pby(),
      out = {};
    const secs = v => typeof v === "string" && v.indexOf(":") > 0 ? +v.split(":")[0] * 60 + (+v.split(":")[1] || 0) : +v || 0;
    const add = (pid, x, keep) => {
      if (!x || x.sv == null) return;
      const p = P["e" + pid] || null,
        t = x.t || p && p.t;
      if (!t || keep && out[t]) return;
      const toi = secs(x.toi);
      if (!out[t] || toi > out[t].toi) out[t] = {
        ...x,
        p,
        toi
      };
    };
    Object.entries(box[day] || {}).forEach(([pid, x]) => add(pid, x, false));
    Object.entries((E.pstat || {})[day] || {}).forEach(([pid, x]) => add(pid, x, true));
    return out;
  }, [day, box, E.generated, s.players]);
  const wi = s.weeks.findIndex(w => (w.dates || []).includes(day));
  const sW = wi >= 0 ? {
    ...s,
    wk: wi
  } : s;
  const wkD = useMemo(() => wi >= 0 ? deriveWeek(s.weeks[wi], s.autoDone) : null, [wi, s.weeks, s.autoDone]);
  const noMv = !wkD || noMovesWk(s, wkD);
  const M = useMemo(() => sim ? computeMoves(sW, {
    H: 1,
    pos: "G",
    pool: 40
  }) : null, [sim, wi]);
  const base = useMemo(() => sim ? winChance(sW) : null, [sim, wi]);
  let games = Object.entries(GD[day] || {}).filter(([, v]) => v.h === 1).map(([home, v]) => ({
    home,
    away: v.o,
    st: v.st || ""
  }));
  if (!games.length) {
    const seen = {};
    Object.entries(played).forEach(([t, x]) => {
      if (!x.o) return;
      const h = x.h ? t : x.o,
        a = x.h ? x.o : t;
      if (!seen[h]) {
        seen[h] = 1;
        games.push({
          home: h,
          away: a,
          st: ""
        });
      }
    });
  }
  games.sort((a, b) => String(a.st).localeCompare(String(b.st)) || a.home.localeCompare(b.home));
  const raw = (E.goalies || s.goalies || {})[day] || {};
  const AIG = (window.__AI || {}).gstart || {};
  const findG = n => {
    const k = nrm(n);
    return s.players.find(p => p.p === "G" && nrm(p.n) === k) || null;
  };
  const side = t => {
    const g = gState(t, day),
      x = played[t];
    if (g.s !== "P" && x) {
      const dec = x.dec === "W" ? "W" : x.dec === "L" ? "L" : x.dec === "O" ? "OTL" : g.s === "L" ? "Live" : "";
      const pts = x.fp != null ? x.fp : gxEst(x, s.sc || {});
      return {
        t,
        p: x.p,
        name: x.p ? x.p.n : "",
        played: true,
        status: [dec, (x.sv || 0) + " saves", x.ga != null ? x.ga + " GA" : ""].filter(Boolean).join(" \u00b7 "),
        col: x.dec === "W" ? "var(--good)" : g.s === "L" ? "var(--warn)" : "var(--mute)",
        val: f1(pts) + (x.fp != null ? " pts" : " pts est.")
      };
    }
    if (g.s !== "P") return {
      t,
      p: null,
      name: "",
      status: day < today ? "result not saved" : "in progress",
      col: "var(--mute)",
      val: ""
    };
    const e = Object.entries(raw).find(([, v]) => v && v.team === t);
    if (e) {
      const st = String(e[1].status || "").toLowerCase(),
        p = findG(e[0]);
      const w = st.includes("confirm") && !st.includes("un") ? ["confirmed", "var(--good)"] : /likely|expected|project/.test(st) ? ["likely", "var(--warn)"] : ["not confirmed", "var(--warn)"];
      return {
        t,
        p,
        name: p ? p.n : e[0],
        status: w[0],
        col: w[1],
        val: p ? f1(effAvg(p, K, day)) + " exp" : ""
      };
    }
    const ch = p => {
      const a = (AIG[String(p.id).slice(1)] || {})[day];
      return a != null ? a : gStart(p, day).v;
    };
    const c = s.players.filter(p => p.p === "G" && p.t === t && !p.ir && avail(p, day) > 0).map(p => [p, ch(p)]).sort((a, b) => b[1] - a[1])[0];
    if (!c) return {
      t,
      p: null,
      name: "",
      status: "starter not known",
      col: "var(--mute)",
      val: ""
    };
    return {
      t,
      p: c[0],
      name: c[0].n,
      status: Math.round(c[1] * 100) + "% to start",
      col: "var(--mute)",
      val: f1(effAvg(c[0], K, day)) + " exp"
    };
  };
  const rows = games.map(gm => ({
    ...gm,
    a: side(gm.away),
    h: side(gm.home)
  }));
  let mine = 0,
    fas = 0;
  rows.forEach(r => [r.a, r.h].forEach(x => {
    if (x.p) {
      if (x.p.ft === s.me) mine++;else if (x.p.ft === "fa") fas++;
    }
  }));
  const mid = gm => {
    const st = gState(gm.home, day).s;
    if (st === "P") return gm.st ? gameTime({
      st: gm.st
    }) : "";
    const sc = gScore(gm.home, day),
      hx = played[gm.home];
    const hs = sc && sc.my != null ? sc.my : hx && hx.my != null ? hx.my : null;
    const aw = sc && sc.op != null ? sc.op : hx && hx.op != null ? hx.op : null;
    return /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("span", {
      className: "block"
    }, st === "L" ? "Live" : "Final"), hs != null && aw != null ? /*#__PURE__*/React.createElement("span", {
      className: "block",
      style: {
        color: "var(--ink)"
      }
    }, aw + "\u2013" + hs) : null);
  };
  const tag = p => !p ? null : p.ft === s.me ? /*#__PURE__*/React.createElement("span", {
    className: "gx-pill me"
  }, "Yours") : p.ft === "fa" ? /*#__PURE__*/React.createElement("span", {
    className: "gx-pill fa"
  }, "Free agent") : /*#__PURE__*/React.createElement("span", {
    className: "text-slate-500"
  }, teamName(s, p.ft));
  const cell = (x, r) => {
    const me = !!(x.p && x.p.ft === s.me);
    const dr = x.p && x.p.ft === "fa" && !x.played && !noMv && gState(x.t, day).s === "P" && day >= pickStart(x.p) ? dropFor(s, x.p) : null;
    const nm = x.p ? /*#__PURE__*/React.createElement(PN, {
      p: x.p,
      className: ""
    }) : x.name ? /*#__PURE__*/React.createElement("span", null, x.name) : /*#__PURE__*/React.createElement("span", {
      className: "text-slate-500"
    }, "\u2013");
    return /*#__PURE__*/React.createElement("div", {
      className: "gx-gs" + (r ? " r" : "") + (me ? " me" : "")
    }, /*#__PURE__*/React.createElement("div", {
      className: "truncate",
      style: {
        fontWeight: me ? 600 : 400
      }
    }, r ? null : /*#__PURE__*/React.createElement("span", {
      style: {
        marginRight: 6
      }
    }, /*#__PURE__*/React.createElement(GxFace, {
      p: x.p,
      t: x.t,
      size: 18
    })), nm, " ", /*#__PURE__*/React.createElement("span", {
      className: "text-xs text-slate-500"
    }, x.t), r ? /*#__PURE__*/React.createElement("span", {
      style: {
        marginLeft: 6
      }
    }, /*#__PURE__*/React.createElement(GxFace, {
      p: x.p,
      t: x.t,
      size: 18
    })) : null), /*#__PURE__*/React.createElement("div", {
      className: "gx-gl2"
    }, /*#__PURE__*/React.createElement("span", {
      style: {
        color: x.col
      }
    }, x.status), tag(x.p), x.val ? /*#__PURE__*/React.createElement("span", {
      className: "text-slate-500"
    }, x.val) : null, dr ? /*#__PURE__*/React.createElement("button", {
      type: "button",
      className: "text-blue-600",
      onClick: e => {
        e.stopPropagation();
        setSim({
          add: x.p.id,
          drop: dr.id
        });
      }
    }, "swap for " + lastN(dr.n)) : null));
  };
  const nice = d => fromIso(d).toLocaleDateString("en-US", {
    weekday: "short",
    month: "short",
    day: "numeric"
  }).replace(",", "");
  const lbl = day === today ? "Today" : day === addDays(today, 1) ? "Tomorrow" : day === addDays(today, -1) ? "Yesterday" : nice(day);
  const note = [lbl === nice(day) ? "" : nice(day), day < today ? "who started and how they did" : day <= addDays(today, 1) ? "starters from Daily Faceoff" : "projected from recent starts", day >= today && noMv ? "no moves left that week" : ""].filter(Boolean).join(" \u00b7 ");
  const nNHL = NHL.filter(t => SCHED[t] && SCHED[t].has(day)).length / 2;
  const onStart = e => {
    const t = e.touches[0];
    touch.current = [t.clientX, t.clientY];
  };
  const onEnd = e => {
    const t0 = touch.current,
      t = e.changedTouches[0];
    touch.current = null;
    if (!t0) return;
    const dx = t.clientX - t0[0],
      dy = t.clientY - t0[1];
    if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy) * 1.5) go(dx < 0 ? 1 : -1);
  };
  return /*#__PURE__*/React.createElement("div", {
    className: "space-y-3",
    onTouchStart: onStart,
    onTouchEnd: onEnd,
    style: {
      touchAction: "pan-y"
    }
  }, /*#__PURE__*/React.createElement("div", {
    className: "gx-dnav"
  }, /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: "gx-arw",
    "aria-label": "Earlier day",
    disabled: day <= minD,
    onClick: () => go(-1)
  }, "\u2039"), /*#__PURE__*/React.createElement("div", {
    className: "text-center",
    style: {
      minWidth: 200
    }
  }, /*#__PURE__*/React.createElement("div", {
    className: "font-semibold",
    style: {
      fontSize: 17
    }
  }, lbl), /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500"
  }, note), day !== today ? /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: "text-xs text-blue-600",
    onClick: () => setDay(today)
  }, "Back to today") : null), /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: "gx-arw",
    "aria-label": "Later day",
    disabled: day >= maxD,
    onClick: () => go(1)
  }, "\u203a")), /*#__PURE__*/React.createElement(GxGoSl105, {
    day: day
  }, /*#__PURE__*/React.createElement("div", {
    className: "gx-pn",
    "data-r65": "goalies"
  }, /*#__PURE__*/React.createElement("div", {
    className: "gx-tag"
  }, (day < today ? "Who started" : "Every goalie") + " \u00b7 " + rows.length + " game" + (rows.length === 1 ? "" : "s")), rows.length ? /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500",
    style: {
      margin: "4px 0 4px"
    }
  }, (mine ? mine + " of yours" : "None of yours") + " \u00b7 " + fas + " free agent" + (fas === 1 ? "" : "s")) : null, rows.length ? rows.map((gm, i) => /*#__PURE__*/React.createElement("div", {
    key: gm.home + i,
    className: "gx-gm2",
    style: i ? null : {
      borderTop: 0
    }
  }, cell(gm.a, false), /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500 text-center",
    style: {
      alignSelf: "center"
    }
  }, mid(gm)), cell(gm.h, true))) : /*#__PURE__*/React.createElement("div", {
    className: "text-sm text-slate-500",
    style: {
      padding: "10px 0"
    }
  }, nNHL ? day < today ? "Results for this day are not saved." : "Game times for this day are not loaded yet." : "No NHL games this day."))), sim && M && wkD ? /*#__PURE__*/React.createElement(GxSim107, {
    s: sW,
    setS: setS,
    wk: wkD,
    M: M,
    H: 1,
    hLabel: "that week",
    init: sim,
    wBase: base,
    onClose: () => setSim(null)
  }) : null);
}

// ---------- moves used from ESPN (news_logos.py) ----------
function movesUsedESPN(s, w) {
  const E = window.ESPN_DATA || {};
  if (!E.acq || !w || w.period == null) return null;
  const a = E.acq[String(s.me).replace(/^t/, "")];
  return a ? +a[String(w.period)] || 0 : null;
}

// ---------- round 9: phone layout (news_logos.py) ----------
const M_TABS = [["today", "Today"], ["matchup", "Matchup"], ["myteam", "Team"], ["league", "League"]]; // round 37, older marker kept: ["lines", "Lines"]];
const M_MORE = [["setup", "Settings"], ["news", "News"], ["teams", "Teams"]]; // round 37, older marker kept: const M_MORE = [["teams", "Teams"], ["league"
const M_MODES = [["espn", "ESPN"], ["blend", "Blend"], ["model", "GM model"], ["ai", "AI (beta)"]];
const M_ST = {
  DAY_TO_DAY: "DTD",
  OUT: "Out",
  INJURY_RESERVE: "IR",
  SUSPENSION: "Susp."
};
const shortN = n => {
  const x = String(n || "").split(" ");
  return x.length > 1 ? x[0][0] + ". " + x.slice(1).join(" ") : x[0];
};
const mGame = p => {
  const g = gameOf(p.t, p.dt);
  return g ? (g.h ? "vs " : "@") + g.o + " " + gameTime(g) : "";
};
const mStart = gs => !gs ? "" : gs.includes("confirmed") && !gs.includes("un") ? "Confirmed" : /not starting|rests|backup/.test(gs) ? "May sit" : /likely/.test(gs) ? "Likely" : "Unconfirmed";
function MobileHeader({
  s,
  setS,
  tab,
  go,
  ageH
}) {
  const [menu, setMenu] = useState(false);
  const [opts, setOpts] = useState(false);
  const more = M_MORE.find(([k]) => k === tab);
  const pick = k => {
    setMenu(false);
    setOpts(false);
    go(k);
  };
  const dot = !s.lastSync ? "var(--faint)" : ageH !== null && ageH > 2 ? "var(--bad)" : "var(--good)";
  const can = k => k === "espn" || !!window.__MODEL && (k !== "ai" || !!window.__AI);
  const tabBtn = (k, l, on, fn) => /*#__PURE__*/React.createElement("button", {
    key: k,
    onClick: fn,
    className: "m-tab",
    style: {
      color: on ? "var(--ink)" : "var(--mute)",
      borderBottomColor: on ? "var(--accent)" : "transparent"
    }
  }, l);
  return /*#__PURE__*/React.createElement("div", {
    className: "m-only"
  }, /*#__PURE__*/React.createElement("div", {
    className: "flex items-center gap-2 px-3 pt-2"
  }, /*#__PURE__*/React.createElement("span", {
    className: "font-semibold text-white truncate",
    style: {
      fontSize: 18
    }
  }, teamName(s, s.me) || "Islands GM"), /*#__PURE__*/React.createElement("span", {
    title: s.lastSync ? "Synced " + fmtTime(s.lastSync) : "Not synced yet",
    style: {
      width: 7,
      height: 7,
      borderRadius: 99,
      background: dot,
      flexShrink: 0
    }
  }), /*#__PURE__*/React.createElement("select", {
    className: "m-wk ml-auto",
    value: s.wk,
    onChange: e => setS({
      ...s,
      wk: +e.target.value
    })
  }, s.weeks.map((w, i) => /*#__PURE__*/React.createElement("option", {
    key: i,
    value: i
  }, (w.label || "").replace(/^Week /, "Wk ")))), /*#__PURE__*/React.createElement("button", {
    className: "m-icon",
    "aria-label": "Options",
    onClick: () => {
      setOpts(!opts);
      setMenu(false);
    }
  }, "\u22EF")), opts && /*#__PURE__*/React.createElement("div", {
    className: "px-3 pt-2 pb-1"
  }, /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500 mb-1"
  }, "Projections"), /*#__PURE__*/React.createElement("div", {
    className: "flex gap-2 overflow-x-auto navscroll"
  }, M_MODES.map(([k, l]) => /*#__PURE__*/React.createElement("button", {
    key: k,
    disabled: !can(k),
    onClick: () => setS({
      ...s,
      pmode: k,
      players: [...s.players]
    }),
    className: "px-3 py-1 rounded-full text-sm border whitespace-nowrap " + (window.__PMODE === k ? "bg-blue-600 border-blue-600" : "border-slate-300 text-slate-600") + (can(k) ? "" : " opacity-40")
  }, l))), /*#__PURE__*/React.createElement("div", {
    className: "flex items-center gap-3 text-xs text-slate-500 mt-2"
  }, /*#__PURE__*/React.createElement("span", null, s.lastSync ? "Synced " + fmtTime(s.lastSync) : "Not synced yet"), /*#__PURE__*/React.createElement("span", {
    className: "ml-auto"
  }, /*#__PURE__*/React.createElement(ThemeBtn, null)), /*#__PURE__*/React.createElement("a", {
    href: "ai-dashboard.html",
    className: "text-blue-600"
  }, "AI Lab"))), /*#__PURE__*/React.createElement("div", {
    className: "grid grid-cols-6 mt-1",
    style: {
      gridTemplateColumns: "repeat(5, minmax(0, 1fr))"
    }
  }, M_TABS.map(([k, l]) => tabBtn(k, l, (tab === k || k === "myteam" && (tab === "moves" || tab === "lines")) && !menu || k === "league" && tab === "teams", () => k === "league" ? (setMenu(false), setOpts(false), go("league", "power")) : pick(k))), tabBtn("setup", "Setup", tab === "setup" || tab === "news", () => {
    setMenu(false);
    setOpts(false);
    go("setup", "settings");
  })), menu && /*#__PURE__*/React.createElement("div", {
    className: "border-t border-slate-800"
  }, M_MORE.map(([k, l]) => /*#__PURE__*/React.createElement("button", {
    key: k,
    onClick: () => pick(k),
    className: "block w-full text-left px-4 py-3 border-b border-slate-800",
    style: {
      color: tab === k ? "var(--accent)" : "var(--ink)"
    }
  }, l))));
}
// ---------- round 10: one trade builder (analyzer + 2-for-1 + best waiver pickup) (news_logos.py) ----------
const Dlt = ({
  v
}) => /*#__PURE__*/React.createElement("span", {
  className: "font-semibold " + (v >= 0 ? "text-green-700" : "text-red-600")
}, v >= 0 ? "+" : "", f1(v));
const tbFlags = (p, K) => {
  const f = [],
    g = sigOf(p),
    l = g.luck,
    id = typeof p.id === "string" && p.id[0] === "e" ? p.id.slice(1) : null;
  const mb = window.__MODEL && id ? (window.__MODEL.base || {})[id] : null;
  if (mb != null && p.proj && p.avg > 0) {
    if (mb / p.avg <= 0.85 && p.avg - mb >= 1) f.push({
      t: "ESPN overrates",
      sell: true
    });else if (mb / p.avg >= 1.15 && mb - p.avg >= 1) f.push({
      t: "underrated",
      sell: false
    });
  }
  if (l && (l.t === "s" && l.d >= 2 || l.t === "g" && l.d >= 4)) f.push({
    t: "lucky",
    sell: true
  });
  if (l && (l.t === "s" && l.d <= -2 || l.t === "g" && l.d <= -4)) f.push({
    t: "unlucky",
    sell: false
  });
  if ((formRatio(p, K) || 0) >= 1.25) f.push({
    t: "hot",
    sell: true
  });
  return f;
};
function TradeBuilder({
  s,
  initPartner,
  setS
}) {
  const [det110, setDet110] = useState(() => window.innerWidth > 640);
  const [pk113, setPk113] = useState(null);
  // trades v42: offer, result and rosters in the new style (news_logos.py)
  // older done markers kept so earlier rounds stay finished:
  // <Section title="Rosters"
  // <Card label="Their lineup"
  // sideBox("You give", Gv, give, setGive)
  // <TradeRanks s={s}
  // {extra || null}
  // waiver pickup</span>
  // const sideBox = (lab, list, sel, set, extra)
  // round 29: two result tiles only
  // data-r29="tiles"
  const K = s.blend,
    today = todayISO();
  const others = s.teams.filter(t => t.id !== s.me);
  const [tp0] = useState(() => {
    const v = window.__TRADE_P || null;
    window.__TRADE_P = null;
    return v;
  });
  const tpThem = tp0 && tp0.ft !== s.me && tp0.ft !== "fa";
  const [partner, setPartner] = useState((tpThem ? tp0.ft : null) || initPartner || (others[0] || {}).id || "");
  const [give, setGive] = useState(tp0 && tp0.ft === s.me && tp0.id ? [tp0.id] : []);
  const [get, setGet] = useState(tpThem && tp0.id ? [tp0.id] : []);
  useEffect(() => {
    const h = () => {
      const v = window.__TRADE_P;
      window.__TRADE_P = null;
      if (!v) return;
      if (v.ft === s.me) {
        if (v.id) setGive(g => g.indexOf(v.id) >= 0 ? g : g.concat([v.id]));
      } else if (v.ft !== "fa") {
        setPartner(v.ft);
        setGet(v.id ? [v.id] : []);
      }
    };
    window.addEventListener("gm-trade", h);
    return () => window.removeEventListener("gm-trade", h);
  }, []);
  const [pick, setPick] = useState({});
  const [edit, setEdit] = useState(-1);
  const [side, setSide] = useState("me");
  const [dropSel, setDropSel] = useState([]);
  const [dropAll, setDropAll] = useState(false);
  const [tm82, setTm82] = useState(null); // change 082: projection for this page only
  const nR = s.weeks.length - s.wk;
  const mins = {
    F: s.minF ?? 10,
    D: s.minD ?? 5,
    G: s.minGo ?? 2
  };
  const order = {
    F: 0,
    D: 1,
    G: 2
  };
  const mine = s.players.filter(p => p.ft === s.me);
  const theirs = s.players.filter(p => p.ft === partner);
  const pg = p => effAvg(p, K) * (p.p === "G" ? p.prob : 1);
  const vv = p => effAvg0(p, K) * (p.p === "G" ? p.prob : 1);
  const gl = p => [...(SCHED[p.t] || [])].filter(d => d >= today && avail(p, d) > 0).length;
  const cnt = r => {
    const c = {
      F: 0,
      D: 0,
      G: 0
    };
    r.forEach(p => {
      if (!p.ir) c[p.p]++;
    });
    return c;
  };
  const tv = useMemo(() => {
    const o = {};
    s.players.forEach(p => {
      if (p.ft !== "fa" || p.proj !== false || p.gp > 0) o[p.id] = rosRaw(p, K);
    });
    return o;
  }, [s.players, K, window.__PMODE]);
  const fas = useMemo(() => s.players.filter(p => p.ft === "fa" && p.prob > 0 && tv[p.id] > 0 && !goalieOut(p)).sort((a, b) => tv[b.id] - tv[a.id]).slice(0, 60), [tv]);
  const rep = useMemo(() => {
    const o = {};
    ["F", "D", "G"].forEach(k => {
      const l = s.players.filter(p => p.ft === "fa" && p.p === k && p.prob > 0 && (p.proj !== false || p.gp > 0)).map(vv).sort((a, b) => b - a).slice(0, 5);
      o[k] = l.length ? l.reduce((a, b) => a + b, 0) / l.length : 0;
    });
    return o;
  }, [s.players, K]);
  const pe = p => Math.max(0, vv(p) - (rep[p.p] || 0)) * gl(p);
  const Gv = mine.filter(p => give.includes(p.id)),
    Rv = theirs.filter(p => get.includes(p.id));
  // round 59: roster spots are counted by active players (22) and one IR spot, a few lines down
  const ready = Gv.length > 0 && Rv.length > 0;
  // round 59: one IR spot each. An injured player who arrives when your IR spot is taken uses an active spot.
  let irOpen59 = Math.max(0, 1 - mine.filter(p => p.ir && !give.includes(p.id)).length);
  const myAfter0 = mine.filter(p => !give.includes(p.id)).concat(Rv.map(p => {
    if (p.ir && irOpen59 > 0) {
      irOpen59--;
      return {
        ...p,
        ft: s.me
      };
    }
    return {
      ...p,
      ft: s.me,
      ir: false
    };
  }));
  const act0 = mine.filter(p => !p.ir).length,
    act1 = myAfter0.filter(p => !p.ir).length;
  const need = Math.max(0, act1 - 22),
    extra = Math.max(0, Math.min(act0, 22) - act1);
  const irIn = Rv.filter(p => p.ir && myAfter0.some(x => x.id === p.id && !x.ir));
  const thIrOpen = Math.max(0, 1 - theirs.filter(p => p.ir && !get.includes(p.id)).length);
  const thOver = Math.max(0, theirs.filter(p => !p.ir && !get.includes(p.id)).length + Gv.filter(p => !p.ir).length + Math.max(0, Gv.filter(p => p.ir).length - thIrOpen) - 22);
  // free agents for the spots you free: your choice, or the best one available
  const picks = [];
  for (let k = 0; k < extra; k++) {
    if (pick[k] === "none") {
      picks.push(null);
      continue;
    }
    let f = (pick[k] ? s.players.find(f => f.ft === "fa" && f.id === pick[k]) : null) || null;
    if (!f) {
      const c = cnt(myAfter0.concat(picks.filter(Boolean))),
        short = ["F", "D", "G"].filter(x => c[x] < mins[x]);
      f = fas.find(x => !picks.some(y => y && y.id === x.id) && (!short.length || short.includes(x.p))) || null;
    }
    picks.push(f);
  }
  // round 59: you choose who to drop. The lowest expected players that keep your position minimums are picked to start.
  const dropPool = myAfter0.filter(p => !p.ir && !get.includes(p.id)).sort((a, b) => pg(a) - pg(b));
  const drops = [];
  if (need) {
    const c59 = cnt(myAfter0);
    dropSel.forEach(id => {
      const p = dropPool.find(x => x.id === id);
      if (p && drops.length < need && drops.indexOf(p) < 0) {
        drops.push(p);
        c59[p.p]--;
      }
    });
    dropPool.forEach(p => {
      if (drops.length < need && drops.indexOf(p) < 0 && c59[p.p] - 1 >= mins[p.p]) {
        drops.push(p);
        c59[p.p]--;
      }
    });
    dropPool.forEach(p => {
      if (drops.length < need && drops.indexOf(p) < 0) drops.push(p);
    });
  }
  const key = [partner, give.join(), get.join(), picks.map(f => f ? f.id : "-").join(), drops.map(p => p.id).join()].join("|");
  const res = useMemo(() => gxWithMode82(tm82, () => {
    // change 082
    if (!ready) return null;
    const dropIds = new Set(drops.map(p => p.id)),
      got = picks.filter(Boolean).map(f => ({
        ...f,
        ft: s.me
      }));
    const after = myAfter0.filter(p => !dropIds.has(p.id)).concat(got);
    const thAfter = theirs.filter(p => !get.includes(p.id)).concat(Gv.map(p => ({
      ...p,
      ft: partner
    })));
    const live59 = r => r.map(p => p.ir ? {
      ...p,
      ir: false
    } : p); // round 59: injured players count from their return date, for both teams
    const tD81 = gxTradeDay(),
      myT = gxTimed(mine, after, tD81),
      thT = gxTimed(theirs, thAfter, tD81); // change 081
    const my = horizonTotal(live59(myT), s, nR) - horizonTotal(live59(mine), s, nR),
      th = horizonTotal(live59(thT), s, nR) - horizonTotal(live59(theirs), s, nR);
    const G = new Set(give),
      T = new Set(get),
      A = new Set(got.map(f => f.id));
    const players = s.players.map(p => G.has(p.id) ? {
      ...p,
      ft: partner
    } : T.has(p.id) || A.has(p.id) ? {
      ...p,
      ft: s.me
    } : dropIds.has(p.id) ? {
      ...p,
      ft: "fa"
    } : p);
    const pos = t => ({
      o: t.rows.findIndex(x => x.t.id === s.me) + 1,
      ...(t.grpRank[s.me] || {})
    });
    const keep = __LT,
      t2 = leagueTable({
        ...s,
        players
      });
    __LT = keep;
    const rb = pos(leagueTable(s)),
      ra = pos(t2);
    const sN = nextWkS(s),
      hasOpp = sN && oppOf(sN.weeks[sN.wk] || {}, s.me);
    const wb = hasOpp ? winChance(sN) : null,
      wa = hasOpp ? winChance(sN, myT) : null; /* change 081 */
    // change 077: this week's win chance too, while the week still has days to play
    const w77 = deriveWeek(s.weeks[s.wk] || s.weeks[0], s.autoDone),
      on77 = oppOf(w77, s.me) && (w77.done || 0) < (w77.dates || []).length;
    const tb = on77 ? winChance(s) : null,
      ta = on77 ? winChance(s, myT) : null; /* change 081 */
    // change 082: the same numbers under every projection
    const q82 = () => {
      const sN2 = nextWkS(s),
        ho = sN2 && oppOf(sN2.weeks[sN2.wk] || {}, s.me);
      return {
        my: horizonTotal(live59(myT), s, nR) - horizonTotal(live59(mine), s, nR),
        th: horizonTotal(live59(thT), s, nR) - horizonTotal(live59(theirs), s, nR),
        tb: on77 ? winChance(s) : null,
        ta: on77 ? winChance(s, myT) : null,
        wb: ho ? winChance(sN2) : null,
        wa: ho ? winChance(sN2, myT) : null
      };
    };
    const mode82 = window.__PMODE;
    const c = cnt(after);
    return {
      myL: live59(myT),
      meL: live59(mine),
      my,
      th,
      rb,
      ra,
      wb,
      wa,
      tb,
      ta,
      q82,
      mode82,
      short: ["F", "D", "G"].filter(k => c[k] < mins[k])
    };
  }), [key, s.players, s.wk, K, window.__PMODE, tm82]);
  const [cmp82, setCmp82] = useState(null); // change 082: every projection, filled in a moment after the main result
  useEffect(() => {
    setCmp82(null);
    if (!res || !res.q82) return;
    const id = setTimeout(() => setCmp82(GX_PM82.filter(([k]) => gxCanMode82(k)).map(([k, l]) => ({
      k,
      l,
      ...(k === res.mode82 ? {
        my: res.my,
        th: res.th,
        tb: res.tb,
        ta: res.ta,
        wb: res.wb,
        wa: res.wa
      } : gxWithMode82(k, res.q82))
    }))), 60);
    return () => clearTimeout(id);
  }, [res]);
  const sum = (l, f) => l.reduce((a, p) => a + f(p), 0);
  const peG = sum(Gv, pe),
    peR = sum(Rv, pe),
    theyThink = peR > 0 ? (peG - peR) / peR : 0;
  const toggle = (sel, set, id) => {
    set(sel.includes(id) ? sel.filter(x => x !== id) : [...sel, id]);
    setPick({});
    setEdit(-1);
  };
  const vd = !res ? null : res.my <= 0 ? ["Bad for you", "var(--bad)", "Your lineup gets worse."] : theyThink >= -0.05 ? ["Good trade", "var(--good)", "You gain, and it should look fair to them."] : ["Good for you, hard to sell", "var(--warn)", "You gain, but they would see it as a loss. Expect a counter-offer."];
  const GN = {
    F: "forwards",
    D: "defence",
    G: "goalies"
  };
  const grp = res ? ["F", "D", "G"].map(k => [k, (res.rb[k] || 0) - (res.ra[k] || 0)]).sort((a, b) => Math.abs(b[1]) - Math.abs(a[1]))[0] : null;
  const arrow = (b, a, fmt, up) => /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("span", null, fmt(b)), /*#__PURE__*/React.createElement("span", {
    className: "text-slate-500",
    style: {
      fontSize: 14,
      margin: "0 6px"
    }
  }, "\u2192"), /*#__PURE__*/React.createElement("span", {
    style: {
      color: up > 0 ? "var(--good)" : up < 0 ? "var(--bad)" : "var(--ink)"
    }
  }, fmt(a)));
  const offerRow = (p, i, onX, note) => /*#__PURE__*/React.createElement("div", {
    key: p.id,
    className: "gx-row",
    style: i ? null : {
      borderTop: 0
    }
  }, /*#__PURE__*/React.createElement(GxFace, {
    p: p,
    size: 22
  }), /*#__PURE__*/React.createElement("span", {
    className: "min-w-0",
    style: {
      flex: 1
    }
  }, /*#__PURE__*/React.createElement("span", {
    className: "block truncate"
  }, /*#__PURE__*/React.createElement(PN, {
    p: p,
    className: ""
  })), note ? /*#__PURE__*/React.createElement("span", {
    className: "block text-xs text-slate-500"
  }, note) : null), /*#__PURE__*/React.createElement("span", {
    className: "text-slate-500",
    style: {
      fontVariantNumeric: "tabular-nums"
    }
  }, f1(pg(p))), /*#__PURE__*/React.createElement("button", {
    type: "button",
    "aria-label": "Remove " + p.n,
    className: "text-slate-500",
    style: {
      padding: "0 4px",
      fontSize: 16
    },
    onClick: onX
  }, "\u00d7"));
  const rosterRows = (list, sel, set, mySide) => [...list].sort((a, b) => (a.ir ? 1 : 0) - (b.ir ? 1 : 0) || order[a.p] - order[b.p] || pg(b) - pg(a)).map(p => {
    const on = sel.includes(p.id),
      fl = mySide ? null : tbFlags(p, K).find(f => !f.sell); // round 59: no sell-high tags
    return /*#__PURE__*/React.createElement("div", {
      key: p.id,
      role: "button",
      className: "gx-row",
      style: {
        cursor: "pointer",
        padding: "8px 6px",
        background: on ? "var(--card3)" : "transparent"
      },
      "data-r59": "ir",
      onClick: () => toggle(sel, set, p.id)
    }, /*#__PURE__*/React.createElement(GxFace, {
      p: p,
      size: 22
    }), /*#__PURE__*/React.createElement("span", {
      className: "min-w-0 truncate",
      style: {
        flex: 1
      }
    }, /*#__PURE__*/React.createElement("span", {
      className: "m-hide"
    }, p.n), /*#__PURE__*/React.createElement("span", {
      className: "m-inl"
    }, shortN(p.n)), " ", /*#__PURE__*/React.createElement("span", {
      className: "text-xs text-slate-500"
    }, p.p + (p.ir ? " \u00b7 IR" : "")), fl ? /*#__PURE__*/React.createElement("span", {
      className: "text-xs",
      style: {
        marginLeft: 6,
        color: mySide ? "var(--warn)" : "var(--good)"
      }
    }, mySide ? "sell high" : "buy low") : null), /*#__PURE__*/React.createElement("span", {
      style: {
        fontVariantNumeric: "tabular-nums"
      }
    }, f1(pg(p))));
  });
  return /*#__PURE__*/React.createElement("div", {
    className: "space-y-3"
  }, /*#__PURE__*/React.createElement("div", {
    className: "gx-tw113 gx-tg114"
  }, others.map(t => /*#__PURE__*/React.createElement("button", {
    key: t.id,
    type: "button",
    title: t.name,
    "aria-label": t.name,
    className: partner === t.id ? "on" : "",
    onClick: () => {
      setPartner(t.id);
      setGet([]);
      setPick({});
      setEdit(-1);
    }
  }, /*#__PURE__*/React.createElement(GxFtPic114, {
    id: t.id,
    size: 44
  })))), partner ? /*#__PURE__*/React.createElement("div", {
    className: "gx-tn114"
  }, "Trading with ", /*#__PURE__*/React.createElement("b", null, teamName(s, partner))) : null, give.length || get.length ? /*#__PURE__*/React.createElement("div", {
    style: {
      textAlign: "right"
    }
  }, /*#__PURE__*/React.createElement("button", {
    className: "text-xs text-slate-500 underline",
    onClick: () => {
      setGive([]);
      setGet([]);
      setPick({});
      setEdit(-1);
    }
  }, "Clear")) : null, /*#__PURE__*/React.createElement("div", {
    className: "tb-grid"
  }, /*#__PURE__*/React.createElement("div", {
    className: "gx-pn",
    style: {
      minWidth: 0
    }
  }, /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("div", {
    className: "gx-tag",
    style: {
      marginBottom: 4
    }
  }, gxYou(s, "You give", teamName(s, s.me) + " gives")), Gv.map((p, i) => offerRow(p, i, () => toggle(give, setGive, p.id))), /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: "gx-add113",
    onClick: () => setPk113("give")
  }, "+ Add players")), /*#__PURE__*/React.createElement("div", {
    className: "gx-pn",
    style: {
      minWidth: 0
    }
  }, /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("div", {
    className: "gx-tag",
    style: {
      marginBottom: 4
    }
  }, gxYou(s, "You get", teamName(s, s.me) + " gets")), Rv.map((p, i) => offerRow(p, i, () => toggle(get, setGet, p.id))), /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: "gx-add113",
    onClick: () => setPk113("get")
  }, "+ Add players"), picks.map((f, k) => f ? offerRow(f, 1, () => {
    setPick(x => ({
      ...x,
      [k]: "none"
    }));
    setEdit(-1);
  }, /*#__PURE__*/React.createElement(React.Fragment, null, "free agent ", /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: "text-blue-600",
    style: {
      marginLeft: 6
    },
    onClick: e => {
      e.stopPropagation();
      setEdit(edit === k ? -1 : k);
    }
  }, "Change player"))) : ready ? /*#__PURE__*/React.createElement("button", {
    key: "add" + k,
    type: "button",
    className: "text-xs text-blue-600",
    style: {
      marginTop: 8
    },
    onClick: () => setPick(x => ({
      ...x,
      [k]: undefined
    }))
  }, "Add a free agent to the open spot") : null), edit >= 0 && edit < extra ? /*#__PURE__*/React.createElement(FaSearch, {
    s: s,
    top: fas,
    taken: new Set(picks.filter(Boolean).map(x => x.id)),
    val: pg,
    onPick: id => {
      setPick(x => ({
        ...x,
        [edit]: id
      }));
      setEdit(-1);
    }
  }) : null)), ready && need > 0 ? /*#__PURE__*/React.createElement("div", {
    className: "gx-pn",
    "data-r59": "drop",
    style: {
      borderLeft: "3px solid var(--bad)"
    }
  }, /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("div", {
    className: "font-semibold",
    style: {
      color: "var(--bad)"
    }
  }, "You must drop " + need + " player" + (need === 1 ? "" : "s") + " to make room"), /*#__PURE__*/React.createElement("div", {
    className: "text-sm text-slate-500",
    style: {
      marginTop: 2
    }
  }, "This trade leaves you with " + act1 + " active players and the limit is 22." + (Gv.some(p => p.ir) ? " " + Gv.filter(p => p.ir).map(p => p.n).join(" and ") + (Gv.filter(p => p.ir).length === 1 ? " is on IR, so trading him does not open a spot." : " are on IR, so trading them does not open a spot.") : "")), /*#__PURE__*/React.createElement("div", {
    style: {
      marginTop: 8
    }
  }, dropPool.filter((p, i) => dropAll || i < 5 || drops.indexOf(p) >= 0).map((p, i) => {
    const on = drops.indexOf(p) >= 0;
    return /*#__PURE__*/React.createElement("div", {
      key: p.id,
      className: "gx-row",
      style: i ? null : {
        borderTop: 0
      }
    }, /*#__PURE__*/React.createElement(GxFace, {
      p: p,
      size: 22
    }), /*#__PURE__*/React.createElement("span", {
      className: "min-w-0 truncate",
      style: {
        flex: 1
      }
    }, /*#__PURE__*/React.createElement("span", {
      className: "m-hide"
    }, p.n), /*#__PURE__*/React.createElement("span", {
      className: "m-inl"
    }, shortN(p.n)), " ", /*#__PURE__*/React.createElement("span", {
      className: "text-xs text-slate-500"
    }, p.p)), /*#__PURE__*/React.createElement("span", {
      className: "text-slate-500",
      style: {
        fontVariantNumeric: "tabular-nums"
      }
    }, f1(pg(p))), /*#__PURE__*/React.createElement("button", {
      type: "button",
      className: "rounded-lg text-sm",
      style: {
        minWidth: 82,
        padding: "4px 10px",
        border: "1px solid var(--bad)",
        background: on ? "var(--bad)" : "transparent",
        color: on ? "#ffffff" : "var(--bad)"
      },
      onClick: () => {
        if (!on) setDropSel(drops.map(x => x.id).concat([p.id]).slice(-need));
      }
    }, on ? "Dropping" : "Drop"));
  })), dropPool.length > 5 ? /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: "text-xs text-blue-600",
    style: {
      marginTop: 8
    },
    onClick: () => setDropAll(!dropAll)
  }, dropAll ? "Show fewer" : "Show all my players") : null, /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500",
    style: {
      marginTop: 8
    }
  }, "The result below counts " + drops.map(p => p.n).join(" and ") + " as dropped. Lowest expected points are listed first.")) : null, res && vd ? /*#__PURE__*/React.createElement("div", {
    className: "gx-pn gx-tp110" + (det110 ? " open" : "")
  }, /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      alignItems: "baseline",
      gap: 10,
      flexWrap: "wrap"
    }
  }, /*#__PURE__*/React.createElement("span", {
    className: "gx-vd110",
    style: {
      background: vd[1]
    }
  }, vd[0])), det110 && res.mode82 ? /*#__PURE__*/React.createElement(GxTradeModes82, {
    part: "pick",
    res: res,
    tm: tm82,
    setTm: setTm82
  }) : null, /*#__PURE__*/React.createElement("div", {
    className: "gx-stg" + (det110 ? "" : " gx-tr110")
  }, /*#__PURE__*/React.createElement("div", {
    className: "gx-stc"
  }, /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500 truncate"
  }, gxYou(s, "Your lineup", teamName(s, s.me))), /*#__PURE__*/React.createElement("div", {
    className: "gx-stv",
    style: {
      color: res.my >= 0 ? "var(--good)" : "var(--bad)"
    }
  }, (res.my >= 0 ? "+" : "") + Math.round(res.my)), /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500"
  }, "points, rest of season")), /*#__PURE__*/React.createElement("div", {
    className: "gx-stc"
  }, /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500"
  }, "Their lineup"), /*#__PURE__*/React.createElement("div", {
    className: "gx-stv",
    style: {
      color: res.th >= 0 ? "var(--good)" : "var(--bad)"
    }
  }, (res.th >= 0 ? "+" : "") + Math.round(res.th)), /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500"
  }, "points, rest of season")), /*#__PURE__*/React.createElement("div", {
    className: "gx-stc"
  }, /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500"
  }, gxYou(s, "Your league rank", "League rank")), /*#__PURE__*/React.createElement("div", {
    className: "gx-stv"
  }, arrow(res.rb.o, res.ra.o, ordN, res.rb.o - res.ra.o)), /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500"
  }, "by team strength")), /*#__PURE__*/React.createElement("div", {
    className: "gx-stc",
    "data-c77": "pos"
  }, /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500"
  }, "Position ranks"), ["F", "D", "G"].map(k => {
    const b = res.rb[k],
      a = res.ra[k],
      f = v => v ? ordN(v) : "\u2013";
    return /*#__PURE__*/React.createElement("div", {
      key: k,
      style: {
        display: "flex",
        alignItems: "baseline",
        gap: 6,
        fontSize: 15,
        fontWeight: 600,
        fontVariantNumeric: "tabular-nums",
        marginTop: 2
      }
    }, /*#__PURE__*/React.createElement("span", {
      className: "text-xs text-slate-500",
      style: {
        width: 74,
        flexShrink: 0,
        fontWeight: 400
      }
    }, GN[k][0].toUpperCase() + GN[k].slice(1)), b === a ? /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("span", null, f(b)), /*#__PURE__*/React.createElement("span", {
      className: "text-xs text-slate-500",
      style: {
        fontWeight: 400
      }
    }, "same")) : /*#__PURE__*/React.createElement("span", null, arrow(b, a, f, (b || 0) - (a || 0))));
  })), res.tb != null && res.ta != null ? /*#__PURE__*/React.createElement("div", {
    className: "gx-stc",
    "data-c77": "week"
  }, /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500"
  }, "This week"), /*#__PURE__*/React.createElement("div", {
    className: "gx-stv"
  }, arrow(res.tb, res.ta, wpTxt, Math.round(res.ta * 100) - Math.round(res.tb * 100))), /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500"
  }, "chance to win")) : null, res.wb != null && res.wa != null ? /*#__PURE__*/React.createElement("div", {
    className: "gx-stc"
  }, /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500"
  }, "Next week"), /*#__PURE__*/React.createElement("div", {
    className: "gx-stv"
  }, arrow(res.wb, res.wa, wpTxt, Math.round(res.wa * 100) - Math.round(res.wb * 100))), /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500"
  }, "chance to win")) : null), det110 && res.mode82 ? /*#__PURE__*/React.createElement(GxTradeModes82, {
    res: res,
    cmp: cmp82,
    tm: tm82,
    setTm: setTm82
  }) : null, res.short.length ? /*#__PURE__*/React.createElement("div", {
    className: "text-sm",
    style: {
      marginTop: 10,
      color: "var(--bad)"
    }
  }, gxYou(s, "This leaves you", "This leaves " + teamName(s, s.me).trim()), " short at ", res.short.map(k => GN[k]).join(" and "), ".") : null, /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500",
    "data-r59": "after",
    style: {
      marginTop: 10
    }
  }, gxYou(s, "Your roster after: ", teamName(s, s.me) + " after: ") + (act1 - drops.length + picks.filter(Boolean).length) + " of 22 active. Trades take " + GX_TRADE_DAYS + " days, so it goes through " + dayLabel(gxTradeDay()) + "; until then both teams keep their players, and the numbers above count that." + (irIn.length ? " Your IR spot is taken, so " + irIn.map(p => p.n).join(" and ") + " would use an active spot." : "") + (thOver > 0 ? " " + teamName(s, partner) + " would be over 22 and would have to drop " + thOver + " too." : "")), /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: "gx-mr110",
    onClick: () => setDet110(!det110)
  }, det110 ? "Hide details" : "More details"), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      flexWrap: "wrap",
      alignItems: "center",
      gap: 12,
      marginTop: 12
    }
  }, /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: "bg-blue-600 rounded-lg px-4 py-1.5 font-semibold",
    onClick: () => {
      gxSimAdd({
        a: s.me,
        b: partner,
        give: Gv.map(p => p.id),
        get: Rv.map(p => p.id),
        add: picks.filter(Boolean).map(p => p.id),
        drop: drops.map(p => p.id)
      }, setS);
      setGive([]);
      setGet([]);
      setPick({});
      setEdit(-1);
      setDropSel([]);
      window.scrollTo(0, 0);
    }
  }, "Apply here"))) : /*#__PURE__*/React.createElement("div", {
    className: "text-sm text-slate-500"
  }, "Pick at least one player on each side to see the result."), res && vd ? /*#__PURE__*/React.createElement(GxTradeLab113, {
    s: s,
    res: res,
    Gv: Gv,
    Rv: Rv,
    pg: pg,
    gl: gl
  }) : null, pk113 ? /*#__PURE__*/React.createElement(GxPick113, {
    title: pk113 === "give" ? gxYou(s, "You give", teamName(s, s.me) + " gives") : teamName(s, partner),
    list: pk113 === "give" ? mine : theirs,
    sel: pk113 === "give" ? give : get,
    pg: pg,
    onToggle: id => pk113 === "give" ? toggle(give, setGive, id) : toggle(get, setGet, id),
    onClose: () => setPk113(null)
  }) : null, /*#__PURE__*/React.createElement("div", {
    className: "gx-pn",
    style: {
      display: "none"
    }
  }, /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      alignItems: "baseline",
      marginBottom: 6
    }
  }, /*#__PURE__*/React.createElement("span", {
    className: "gx-tag"
  }, "Rosters"), /*#__PURE__*/React.createElement("span", {
    className: "text-xs text-slate-500 m-hide",
    style: {
      marginLeft: "auto"
    }
  }, "Tap a player to add or remove him"), /*#__PURE__*/React.createElement("span", {
    className: "gx-seg m-seg",
    style: {
      marginLeft: "auto"
    }
  }, /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: side === "me" ? "on" : "",
    onClick: () => setSide("me")
  }, teamName(s, s.me)), /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: side === "them" ? "on" : "",
    onClick: () => setSide("them")
  }, teamName(s, partner)))), /*#__PURE__*/React.createElement("div", {
    className: "tb-grid"
  }, /*#__PURE__*/React.createElement("div", {
    className: "min-w-0" + (side === "me" ? "" : " m-hide")
  }, /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500 truncate m-hide",
    style: {
      paddingBottom: 2
    }
  }, teamName(s, s.me)), rosterRows(mine, give, setGive, true)), /*#__PURE__*/React.createElement("div", {
    className: "min-w-0" + (side === "them" ? "" : " m-hide")
  }, /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500 truncate m-hide",
    style: {
      paddingBottom: 2
    }
  }, teamName(s, partner)), rosterRows(theirs, get, setGet, false)))));
}

// ---------- round 14: My Team injuries + protected players (news_logos.py) ----------
function MyInjProt({
  s,
  setS,
  wk
}) {
  const K = s.blend,
    today = todayISO();
  const [edit, setEdit] = useState(null);
  const [adv, setAdv] = useState(false);
  const roster = s.players.filter(p => p.ft === s.me);
  const upd = (id, patch) => setS(st => ({
    ...st,
    players: st.players.map(p => p.id === id ? {
      ...p,
      ...patch
    } : p)
  }));
  const out = roster.filter(p => {
    const b = effBack(p).d;
    return p.ir || b && b > today || !b && avail(p, today) === 0 || p.status && p.status !== "ACTIVE";
  }).sort((a, b) => (effBack(a).d || "9999") < (effBack(b).d || "9999") ? -1 : 1);
  const top = s.protectTop ?? 8;
  const healthy = roster.filter(p => !p.ir).sort((a, b) => gxPgAvg(b, K) - gxPgAvg(a, K)); /* gx088-r */
  const auto = healthy.slice(0, top),
    autoIds = new Set(auto.map(p => p.id));
  const mine = healthy.filter(p => p.keep && !autoIds.has(p.id));
  const addable = healthy.filter(p => !autoIds.has(p.id) && !p.keep);
  const ST = {
    DAY_TO_DAY: "Day-to-day",
    OUT: "Out",
    INJURY_RESERVE: "IR",
    SUSPENSION: "Suspended"
  };
  const stTxt = p => p.ir ? "IR" : ST[p.status] || (p.status || "Out").replace(/_/g, " ");
  const SRC = {
    you: "your date",
    ESPN: "from ESPN",
    news: "from injury news",
    estimate: "estimate"
  };
  const chip = "inline-flex items-center gap-1.5 pl-1.5 pr-2.5 py-1 rounded-full border text-sm ";
  const backTxt = (p, b) => {
    if (!b) return "No return date yet";
    if (b <= today) return "Available now";
    const n = Math.round((fromIso(b) - fromIso(today)) / 864e5);
    const miss = (wk.dates || []).filter((d, i) => d >= today && d < b && (wk.games[p.t] || []).includes(i)).length;
    return "Back " + mdL(b) + " (" + n + " day" + (n === 1 ? "" : "s") + ")" + (miss ? " · misses " + miss + " game" + (miss === 1 ? "" : "s") + " this week" : "");
  };
  return /*#__PURE__*/React.createElement("div", {
    className: "space-y-4"
  }, /*#__PURE__*/React.createElement("div", {
    className: "grid md:grid-cols-2 gap-4 items-start"
  }, /*#__PURE__*/React.createElement(Section, {
    title: "Injuries",
    sub: "Return dates come from ESPN. Change one only if you know better."
  }, out.length ? out.map(p => {
    const eb = effBack(p);
    return /*#__PURE__*/React.createElement("div", {
      key: p.id,
      className: "flex items-center gap-3 py-3 border-t border-slate-100"
    }, /*#__PURE__*/React.createElement(GxFace, {
      p: p,
      size: 30
    }), /*#__PURE__*/React.createElement("div", {
      className: "min-w-0 flex-1"
    }, /*#__PURE__*/React.createElement("div", {
      className: "flex items-center gap-2"
    }, /*#__PURE__*/React.createElement(PN, {
      p: p
    }), /*#__PURE__*/React.createElement("span", {
      className: "text-xs text-slate-500"
    }, p.p), /*#__PURE__*/React.createElement("span", {
      className: "text-xs px-1.5 py-0.5 rounded bg-red-100 text-red-600"
    }, stTxt(p))), /*#__PURE__*/React.createElement("div", {
      className: "text-xs text-slate-500 mt-0.5"
    }, backTxt(p, eb.d), eb.d && eb.src ? " · " + SRC[eb.src] : "", eb.src === "you" ? /*#__PURE__*/React.createElement("button", {
      className: "text-blue-600 ml-2",
      onClick: () => upd(p.id, {
        back: DEFAULT_BACK[p.n] || ""
      })
    }, "Reset") : null), edit === p.id ? /*#__PURE__*/React.createElement("div", {
      className: "flex items-center gap-2 mt-2"
    }, /*#__PURE__*/React.createElement("input", {
      type: "date",
      className: inp,
      value: eb.d,
      onChange: e => upd(p.id, {
        back: e.target.value
      })
    }), /*#__PURE__*/React.createElement("button", {
      className: "text-sm text-blue-600",
      onClick: () => setEdit(null)
    }, "Done")) : null), edit === p.id ? null : /*#__PURE__*/React.createElement("button", {
      className: "text-sm text-blue-600 whitespace-nowrap",
      onClick: () => setEdit(p.id)
    }, "Change"));
  }) : /*#__PURE__*/React.createElement("div", {
    className: "text-green-700"
  }, "Everyone is healthy.")), /*#__PURE__*/React.createElement(Section, {
    title: "Protected players",
    sub: "Never suggested as drops anywhere in the app. Players on IR are never dropped."
  }, /*#__PURE__*/React.createElement("label", {
    className: "flex flex-wrap items-center gap-2 text-sm"
  }, /*#__PURE__*/React.createElement("span", null, "Always protect my top"), /*#__PURE__*/React.createElement("select", {
    className: inp,
    value: top,
    onChange: e => setS(st => ({
      ...st,
      protectTop: +e.target.value
    }))
  }, [...Array(13)].map((_, n) => /*#__PURE__*/React.createElement("option", {
    key: n,
    value: n
  }, n))), /*#__PURE__*/React.createElement("span", null, "players")), auto.length ? /*#__PURE__*/React.createElement("div", {
    className: "mt-3 flex flex-wrap gap-2"
  }, auto.map(p => /*#__PURE__*/React.createElement("span", {
    key: p.id,
    className: chip + "border-slate-200 text-slate-600"
  }, /*#__PURE__*/React.createElement(GxFace, {
    p: p,
    size: 18
  }), p.n))) : null, /*#__PURE__*/React.createElement("div", {
    className: "text-xs uppercase tracking-wide text-slate-500 mt-4 mb-2"
  }, "Also protect"), /*#__PURE__*/React.createElement("div", {
    className: "flex flex-wrap gap-2 items-center"
  }, mine.map(p => /*#__PURE__*/React.createElement("span", {
    key: p.id,
    className: chip + "border-green-300 bg-green-50"
  }, /*#__PURE__*/React.createElement(GxFace, {
    p: p,
    size: 18
  }), p.n, /*#__PURE__*/React.createElement("button", {
    className: "text-slate-500 ml-1 text-base leading-none",
    "aria-label": "Unprotect " + p.n,
    onClick: () => upd(p.id, {
      keep: false
    })
  }, "\xD7"))), addable.length ? /*#__PURE__*/React.createElement("select", {
    className: inp,
    value: "",
    onChange: e => {
      if (e.target.value) upd(e.target.value, {
        keep: true
      });
    }
  }, /*#__PURE__*/React.createElement("option", {
    value: ""
  }, "+ Add a player"), addable.map(p => /*#__PURE__*/React.createElement("option", {
    key: p.id,
    value: p.id
  }, p.n, " (", p.p, ")"))) : null))), /*#__PURE__*/React.createElement("div", {
    className: "px-1"
  }, /*#__PURE__*/React.createElement("button", {
    className: "text-sm text-blue-600",
    onClick: () => setAdv(!adv)
  }, adv ? "Hide the full editor" : "Edit every player: projections, play %, IR"), adv ? /*#__PURE__*/React.createElement("div", {
    className: "mt-3"
  }, /*#__PURE__*/React.createElement(RosterTable, {
    s: s,
    setS: setS,
    wk: wk,
    team: s.me
  })) : null));
}

// ---------- round 16: live and final points from ESPN (news_logos.py) ----------
const ESLOT = {
  3: "F",
  4: "D",
  6: "UTIL",
  5: "G"
};
const CAPK = {
  F: "F",
  D: "D",
  UTIL: "U",
  G: "G"
};
let __PB = null,
  __NG = null;
const pby = () => {
  const L = window.__PLAYERS || [];
  if (!__PB || __PB.k !== L) __PB = {
    k: L,
    m: Object.fromEntries(L.map(p => [p.id, p]))
  };
  return __PB.m;
};
const actDay = (tid, dt) => {
  const D = ((window.ESPN_DATA || {}).daily || {})[dt];
  return D ? D[String(tid).replace(/^t/, "")] || null : null;
};
const gState = (t, dt) => {
  const x = ((window.__LIVESC || {})[dt] || {})[t] || (((window.ESPN_DATA || {}).gstate || {})[dt] || {})[t];
  if (x && x.s === "F") return {
    s: "F",
    f: 1
  };
  if (x && x.s === "L") return {
    s: "L",
    f: x.f || 0
  };
  const g = gameOf(t, dt),
    st = g && g.st ? Date.parse(g.st) : NaN;
  if (!isNaN(st)) {
    const el = (Date.now() - st) / 36e5;
    return el < 0 ? {
      s: "P",
      f: 0
    } : el > 3.5 ? {
      s: "F",
      f: 1
    } : {
      s: "L",
      f: Math.min(0.95, el / 2.6)
    };
  }
  return dt && dt < todayISO() ? {
    s: "F",
    f: 1
  } : {
    s: "P",
    f: 0
  };
};
const gScore = (t, dt) => {
  const L = ((window.__LIVESC || {})[dt] || {})[t];
  return L || (((window.ESPN_DATA || {}).gstate || {})[dt] || {})[t] || null;
};
const LiveTag = ({
  st,
  t,
  dt
}) => {
  // live tag v21: pill + score from the player's team's side (news_logos.py)
  if (st !== "L" && st !== "F") return null;
  const sc = t && dt ? gScore(t, dt) : null;
  const has = !!(sc && sc.my != null && sc.op != null);
  const res = has && st === "F" ? sc.my > sc.op ? "W" : sc.my < sc.op ? "L" : "" : "";
  const tail = !sc ? "" : st === "F" ? sc.per === "OT" || sc.per === "SO" ? " " + sc.per : "" : sc.int ? " · " + sc.per + " int." : sc.per ? " · " + sc.per + (sc.clk ? " " + sc.clk : "") : "";
  return /*#__PURE__*/React.createElement("span", {
    className: "inline-flex items-center gap-1.5 whitespace-nowrap align-middle"
  }, st === "L" ? /*#__PURE__*/React.createElement("span", {
    className: "gm-pill inline-flex items-center gap-1 bg-red-100 text-red-600"
  }, /*#__PURE__*/React.createElement("span", {
    className: "gm-dot"
  }), "LIVE") : /*#__PURE__*/React.createElement("span", {
    className: "gm-pill bg-slate-200 text-slate-500"
  }, "FINAL"), has ? /*#__PURE__*/React.createElement("span", {
    className: "text-xs font-semibold " + (res === "W" ? "text-green-700" : res === "L" ? "text-red-600" : "text-slate-700")
  }, res ? res + " " : "", sc.my, "\u2013", sc.op, /*#__PURE__*/React.createElement("span", {
    className: "font-normal text-slate-500"
  }, tail)) : null);
};
// players who beat or missed their projection get 10% of the average miss per game, capped at 15%
function liveNudges(K) {
  const E = window.ESPN_DATA || {},
    key = [E.generated, K, window.__PMODE, window.__PLAYERS];
  if (__NG && __NG.k.every((v, i) => v === key[i])) return __NG.m;
  const P = pby(),
    acc = {};
  Object.entries(E.daily || {}).forEach(([dt, T]) => Object.values(T || {}).forEach(tm => Object.entries(tm || {}).forEach(([pid, v]) => {
    const p = P["e" + pid];
    if (!p || !v || v[0] == null || !(SCHED[p.t] && SCHED[p.t].has(dt)) || gState(p.t, dt).s !== "F") return;
    const a = acc[p.id] = acc[p.id] || {
      s: 0,
      n: 0,
      seen: {}
    };
    if (a.seen[dt]) return;
    a.seen[dt] = 1;
    a.s += v[0] - effAvg(p, K, dt);
    a.n++;
  })));
  const m = {};
  Object.entries(acc).forEach(([id, a]) => {
    const b = effAvg(P[id], K);
    if (!(b > 0) || !a.n) return;
    const adj = Math.max(-0.15, Math.min(0.15, 0.1 * a.s / a.n / b));
    if (Math.abs(adj) >= 0.005) m[id] = 1 + adj;
  });
  __NG = {
    k: key,
    m
  };
  return m;
}
function weekLive(roster, wk, K, tid, opt) {
  // live week v16: real points for games that started (ESPN lineup), projection for everything still to come
  const dates = wk.dates || [],
    ng = liveNudges(K),
    P = pby(),
    today = todayISO();
  const r = roster.map(p => ng[p.id] ? {
    ...p,
    gwMul: (p.gwMul || 1) * ng[p.id]
  } : p);
  const byId = {};
  r.forEach(p => byId[p.id] = p);
  let actSoFar = 0,
    projSoFar = 0;
  const days = wk.days.map((_, d) => {
    const dt = dates[d];
    const plays = p => (wk.games[p.t] || []).includes(d);
    const lk = p => !!dt && plays(p) && gState(p.t, dt).s !== "P";
    const full = opt && opt.detail ? dayLineup(roster.filter(p => onEspnDay(dt ? actDay(tid, dt) : null, p)), wk, d, K).total : null;
    const AD = dt ? actDay(tid, dt) : null;
    const adAct = AD ? Object.entries(AD).filter(([, v]) => v && ESLOT[v[1]]) : [];
    if (!dt || !r.some(lk) && !adAct.some(([, v]) => v[0] != null)) {
      const L = dayLineup(r.filter(p => onEspnDay(AD, p)), wk, d, K);
      return {
        ...L,
        act: 0,
        proj: full != null ? full : L.total,
        locked: 0,
        liveN: 0,
        openN: L.start.length,
        allDone: !!dt && dt < today,
        benchAct: [],
        empty: dt && dt < today ? 0 : L.empty
      };
    }
    const cap = {
        F: 9,
        D: 5,
        U: 1,
        G: 2
      },
      rows = [],
      done = new Set();
    let act = 0;
    const take = (p, pp, slot, a, assume) => {
      a = gxLiveA120(p, dt, a); /* gx120 */
      const g = gState(p.t, dt),
        gs = p.p === "G" ? gStart(p, dt) : null;
      const base = q => effAvg(q, K, dt) * (a != null ? 1 : (gs ? gs.v : p.prob) * avail(p, dt));
      const x0 = base(pp),
        playing = assume || a != null || g.s === "L" && g.f < 0.3;
      const vf = g.s === "L" && playing ? 1 - g.f : 0;
      rows.push({
        ...pp,
        slot,
        st: g.s,
        a,
        x0,
        x: x0 * vf,
        vf,
        dt,
        gs: gs ? gs.l : ""
      });
      if (a != null) {
        act += a;
        actSoFar += a;
        projSoFar += base(p) * (g.s === "F" ? 1 : g.f);
      }
      done.add(p.id);
      if (CAPK[slot]) cap[CAPK[slot]]--;
    };
    if (AD) {
      adAct.forEach(([pid, v]) => {
        const p = P["e" + pid];
        if (!p) {
          if (v[0] != null) {
            act += v[0];
            actSoFar += v[0];
          }
          return;
        }
        if (plays(p) ? gState(p.t, dt).s === "P" : !v[0]) return;
        take(p, byId[p.id] || p, ESLOT[v[1]], v[0], false);
      });
    } else {
      dayLineup(r, wk, d, K).start.filter(lk).forEach(q => {
        const raw = roster.find(x => x.id === q.id) || q;
        take(raw, byId[q.id] || raw, q.slot, null, true);
      });
    }
    const benchAct = AD ? Object.entries(AD).filter(([, v]) => v && v[1] === 7 && v[0]).map(([pid, v]) => ({
      p: P["e" + pid],
      a: v[0]
    })).filter(x => x.p && gState(x.p.t, dt).s !== "P") : [];
    Object.keys(cap).forEach(k => cap[k] = Math.max(0, cap[k]));
    const L = dayLineup(r.filter(p => onEspnDay(AD, p) && !done.has(p.id) && !lk(p)), wk, d, K, cap);
    const liveN = rows.filter(x => x.vf > 0).length;
    return {
      start: [...rows, ...L.start].sort((a, b) => ({
        F: 0,
        D: 1,
        UTIL: 2,
        G: 3
      }[a.slot] ?? 4) - ({
        F: 0,
        D: 1,
        UTIL: 2,
        G: 3
      }[b.slot] ?? 4)),
      bench: L.bench,
      total: rows.reduce((s2, x) => s2 + x.x, 0) + L.total,
      act,
      proj: full,
      locked: rows.length,
      liveN,
      openN: L.start.length,
      allDone: !rows.some(x => x.st === "L") && !L.start.length,
      benchAct,
      empty: dt < today ? 0 : L.empty,
      sched: L.sched + liveN
    };
  });
  const sum = f => days.reduce((a, x) => a + f(x), 0);
  return {
    days,
    total: sum(x => x.total),
    act: sum(x => x.act),
    actSoFar,
    projSoFar,
    used: gxGmLeft(days) /* gx087 */,
    wasted: sum(x => x.bench.length),
    empty: sum(x => x.empty),
    sched: sum(x => x.sched)
  };
}

// ---------- round 22: NHL box-score stat lines (news_logos.py) ----------
const pStat = (p, dt) => {
  const id = String(p && p.id || "").replace(/^e/, "");
  const E0 = (((window.ESPN_DATA || {}).pstat || {})[dt] || {})[id] || null;
  const L = p && dt && typeof gxUseLive120 === "function" ? gxUseLive120(p, dt, gxPdReal(p, dt)) : null;
  return L || E0; /* gx120 */
};
const statLine = x => {
  if (!x) return "";
  if (x.sv != null) return [x.dec || null, x.sv + " SV", x.ga + " GA", x.toi ? x.toi + " TOI" : null].filter(Boolean).join(", ");
  const n = (v, l) => v ? v > 1 ? v + " " + l : l : null;
  return [n(x.g, "G"), n(x.a, "A"), (x.pm > 0 ? "+" : "") + (x.pm || 0), n(x.sog, "SOG"), n(x.pim, "PIM"), n(x.hit, "HIT"), n(x.blk, "BLK"), x.toi ? x.toi + " TOI" : null].filter(Boolean).join(", ");
};

// ---------- round 24: a player counts on a day only if ESPN has him on that day's roster (news_logos.py) ----------
const onEspnDay = (AD, p) => !AD || !Object.keys(AD).length || AD[String(p.id).replace(/^e/, "")] != null;

// ---------- round 25: pickups start after the daily lock (news_logos.py) ----------
// ESPN locks the whole day at the first puck drop, so anyone added after that plays from tomorrow.
// Players on waivers (1-day waivers) can play from tomorrow at the earliest.
let __LK = null;
const lockedToday = () => {
  const today = todayISO(),
    k = today + ":" + Math.floor(Date.now() / 30000);
  if (__LK && __LK.k === k) return __LK.v;
  const G = ((window.GAMES_DATA || {}).games || {})[today] || {};
  const first = Object.values(G).reduce((m, g) => {
    const t = g && g.st ? Date.parse(g.st) : NaN;
    return isNaN(t) ? m : Math.min(m, t);
  }, Infinity);
  const live = Object.values((window.__LIVESC || {})[today] || {}).some(x => x && x.s && x.s !== "P");
  const espn = Object.values(((window.ESPN_DATA || {}).gstate || {})[today] || {}).some(x => x && x.s && x.s !== "P");
  const v = live || espn || first <= Date.now();
  __LK = {
    k,
    v
  };
  return v;
};
const pickStart = p => p && p.wv || lockedToday() ? addDays(todayISO(), 1) : todayISO();
const onDay = (p, dt) => !dt || (!p.fromD || dt >= p.fromD) && (!p.untilD || dt < p.untilD);
const timedMove = (roster, me, moves) => {
  let r = roster;
  moves.forEach(({
    add,
    drop
  }) => {
    const a = pickStart(add);
    r = r.map(p => drop && p.id === drop.id ? {
      ...p,
      untilD: a
    } : p).concat([{
      ...add,
      ft: me,
      fromD: a
    }]);
  });
  return r;
};
const PickNote = () => {
  const a = pickStart(null);
  return a === todayISO() ? null : /*#__PURE__*/React.createElement("div", {
    className: "w-full text-xs text-amber-600 mt-1"
  }, "Today's first game has started, so anyone you add now plays from ", dayLabel(a), ". Players on waivers show a Waivers tag and can't play before tomorrow.");
};

// ---------- round 26: planner win chance (news_logos.py) ----------
const planRoster = (s, wk, steps) => {
  let r = s.players.filter(p => p.ft === s.me);
  steps.forEach(st => {
    const a = wk.dates[st.day];
    r = r.map(p => p.id === st.drop.id ? {
      ...p,
      untilD: a
    } : p).concat([{
      ...st.add,
      ft: s.me,
      fromD: a
    }]);
  });
  return r;
};
const PlanWin = ({
  a,
  b
}) => {
  if (a == null || b == null) return null;
  const d = Math.round(b * 100) - Math.round(a * 100);
  return /*#__PURE__*/React.createElement("span", {
    className: "text-sm whitespace-nowrap " + (d > 0 ? "text-green-700" : d < 0 ? "text-red-600" : "text-slate-500"),
    title: "Your chance to win this week before and after this move"
  }, "win ", wpTxt(a), " \u2192 ", wpTxt(b), " ", /*#__PURE__*/React.createElement("span", {
    className: "font-semibold"
  }, d > 0 ? "+" : "", d, "%"));
};

// ---------- round 27: no moves left this week, so plan next week instead (news_logos.py) ----------
const noMovesWk = (s, w) => !!w && movesLeft(s, s.me, w) === 0;
const outOfMoves = s => noMovesWk(s, s.weeks[s.wk]);
const nextWkS = s => s.wk + 1 < s.weeks.length ? {
  ...s,
  wk: s.wk + 1
} : null;
const planS = s => outOfMoves(s) && nextWkS(s) || s;
const planBase = (s, sP) => sP !== s && !oppOf(sP.weeks[sP.wk] || {}, sP.me) ? null : winChance(sP);
const planNote = sP => {
  const w = sP.weeks[sP.wk] || {},
    d = (w.dates || [])[0];
  return "No moves left this week. These are for " + (w.label || "next week") + (d ? ", once your moves reset on " + dayLabel(d) : "") + ".";
};
const PlanNote = ({
  sP
}) => /*#__PURE__*/React.createElement("div", {
  className: "w-full text-xs text-amber-600 mt-1 mb-1"
}, planNote(sP));

// ---------- round 28: goalies must be playing, player updates for My Team (news_logos.py) ----------
// a goalie is "not playing" if he started fewer than 2 of his team's last 5 games, or is out right now
const gxGoalieOut0 = p => {
  /* gx075-g */
  if (!p || p.p !== "G") return false;
  const today = todayISO();
  if (avail(p, today) === 0) return true;
  const g = sigOf(p).gs;
  if (g && g.rg >= 3) return g.rs * 5 < g.rg * 2;
  const played = [...(SCHED[p.t] || [])].filter(d => d < today).length;
  return played >= 4 && !(p.gp > 0);
};
function MyForm({
  s
}) {
  const K = s.blend;
  const rows = s.players.filter(p => p.ft === s.me && !p.ir).map(p => {
    const fr = formRatio(p, K),
      t = toiOf(p),
      rec = sigOf(p).rec;
    if (fr !== null && fr >= 1.3) return {
      p,
      n: "Hot: " + f1(rec.ppg) + "/g lately. Start him every game.",
      c: "text-orange-600"
    };
    if (fr !== null && fr <= 0.7) return {
      p,
      n: "Cold: " + f1(rec.ppg) + "/g lately. Check his role before dropping.",
      c: "text-sky-600"
    };
    if (t && (t.d <= -90 || t.pd <= -45)) return {
      p,
      n: "Losing minutes (" + (t.d <= -90 ? mm(t.d) + " a game" : "power play " + mm(t.pd)) + "). Watch closely.",
      c: "text-red-600"
    };
    if (t && (t.d >= 90 || t.pd >= 45)) return {
      p,
      n: "Bigger role (" + (t.d >= 90 ? mm(t.d) + " a game" : "power play " + mm(t.pd)) + ").",
      c: "text-green-700"
    };
    return null;
  }).filter(Boolean);
  return /*#__PURE__*/React.createElement(Section, {
    title: "Player updates" + (rows.length ? " (" + rows.length + ")" : ""),
    sub: "Hot and cold streaks and ice-time changes, compared with each player's projection."
  }, rows.length ? rows.map(({
    p,
    n,
    c
  }) => /*#__PURE__*/React.createElement(PlayerLine, {
    key: p.id,
    s: s,
    p: p,
    extra: /*#__PURE__*/React.createElement("span", {
      className: c
    }, "\u00b7 " + n)
  })) : /*#__PURE__*/React.createElement("div", {
    className: "text-slate-400"
  }, "Everyone is playing close to projection."));
}

// ---------- round 29: trade advice with buy-low list, free-agent search (news_logos.py) ----------
function TradeAdvice({
  s,
  onPick
}) {
  const K = s.blend;
  const [team, setTeam] = useState("all");
  const [more, setMore] = useState(false);
  const T = leagueTable(s),
    g = T.grpRank[s.me] || {};
  const posName = {
      F: "forwards",
      D: "defence",
      G: "goalies"
    },
    need = {
      F: 10,
      D: 5,
      G: 2
    };
  const by = ["F", "D", "G"].sort((a, b) => (g[b] || 0) - (g[a] || 0)),
    weak = by[0],
    strong = by[2];
  const pg = p => effAvg(p, K) * (p.p === "G" ? p.prob : 1);
  const mine = s.players.filter(p => p.ft === s.me && !p.ir);
  const spare = mine.filter(p => p.p === strong).sort((a, b) => pg(b) - pg(a)).slice(need[strong]);
  const sell = mine.filter(p => tbFlags(p, K).some(f => f.sell)).sort((a, b) => pg(b) - pg(a)).slice(0, 6);
  const all = useMemo(() => {
    const why = p => {
      const r = [],
        fr = formRatio(p, K),
        sg = sigOf(p),
        rec = sg.rec,
        l = sg.luck;
      const id = typeof p.id === "string" && p.id[0] === "e" ? p.id.slice(1) : null;
      const mb = window.__MODEL && id ? (window.__MODEL.base || {})[id] : null;
      if (fr !== null && fr <= 0.75 && rec) r.push("cold: " + f1(rec.ppg) + "/g last 14 days");
      if (mb != null && p.proj && p.avg > 0 && mb / p.avg >= 1.15 && mb - p.avg >= 1) r.push("model " + f1(mb) + " vs ESPN " + f1(p.avg));
      if (l && (l.t === "s" && l.d <= -2 || l.t === "g" && l.d <= -4)) r.push("unlucky");
      return r;
    };
    return s.players.filter(p => p.ft !== s.me && p.ft !== "fa" && !p.ir && pg(p) >= 6 && !goalieOut(p)).map(p => ({
      p,
      r: why(p)
    })).filter(x => x.r.length).sort((a, b) => pg(b.p) - pg(a.p));
  }, [s.players, K, window.__PMODE]);
  const list = all.filter(x => team === "all" || x.p.ft === team);
  const shown = list.slice(0, more ? 20 : 8);
  return /*#__PURE__*/React.createElement(Section, {
    title: "Buy low"
  }, /*#__PURE__*/React.createElement("div", {
    className: "flex flex-wrap items-center gap-2 mb-1",
    "data-r42": "bl"
  }, /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500"
  }, list.length + " players"), /*#__PURE__*/React.createElement("select", {
    className: inp + " ml-auto",
    value: team,
    onChange: e => {
      setTeam(e.target.value);
      setMore(false);
    }
  }, /*#__PURE__*/React.createElement("option", {
    value: "all"
  }, "All teams"), s.teams.filter(t => t.id !== s.me).map(t => /*#__PURE__*/React.createElement("option", {
    key: t.id,
    value: t.id
  }, t.name)))), shown.length ? shown.map(({
    p,
    r
  }) => /*#__PURE__*/React.createElement(GxBL104, {
    key: p.id,
    s: s,
    p: p,
    r: r,
    onPick: onPick
  })) : /*#__PURE__*/React.createElement("div", {
    className: "text-slate-400"
  }, "No buy-low players here right now. Cold streaks need 3 or more recent games to show."), list.length > shown.length && !more ? /*#__PURE__*/React.createElement("button", {
    className: "text-sm text-blue-600 mt-2",
    onClick: () => setMore(true)
  }, "Show all ", Math.min(20, list.length)) : null);
}
function FaSearch({
  s,
  top,
  taken,
  val,
  onPick
}) {
  const [q, setQ] = useState("");
  const [open, setOpen] = useState(false);
  const qq = nrm(q);
  const list = !open ? [] : qq ? s.players.filter(p => p.ft === "fa" && p.prob > 0 && !taken.has(p.id) && nrm(p.n).includes(qq)).sort((a, b) => val(b) - val(a)).slice(0, 8) : top.filter(p => !taken.has(p.id)).slice(0, 6);
  return /*#__PURE__*/React.createElement("div", {
    className: "relative mt-2"
  }, /*#__PURE__*/React.createElement("input", {
    className: inp + " w-full",
    placeholder: "Search any free agent by name",
    value: q,
    onChange: e => {
      setQ(e.target.value);
      setOpen(true);
    },
    onFocus: () => setOpen(true),
    onBlur: () => setTimeout(() => setOpen(false), 150)
  }), open ? /*#__PURE__*/React.createElement("div", {
    className: "ms-list"
  }, !qq ? /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500 px-2 pt-1 pb-1"
  }, "Best available") : null, list.map(p => /*#__PURE__*/React.createElement("button", {
    key: p.id,
    type: "button",
    className: "ms-opt",
    onMouseDown: e => e.preventDefault(),
    onClick: () => {
      onPick(p.id);
      setQ("");
      setOpen(false);
    }
  }, /*#__PURE__*/React.createElement(GxFace, {
    p: p,
    size: 22
  }), /*#__PURE__*/React.createElement("span", {
    className: "truncate flex-1 text-left"
  }, p.n, " ", /*#__PURE__*/React.createElement("span", {
    className: "text-xs text-slate-500"
  }, p.p)), /*#__PURE__*/React.createElement("span", {
    className: "text-xs text-slate-500 whitespace-nowrap"
  }, f1(val(p)), "/g"))), list.length === 0 ? /*#__PURE__*/React.createElement("div", {
    className: "text-sm text-slate-400 px-2 py-2"
  }, "No free agent matches.") : null) : null);
}

// ---------- round 32: theme switch, top bar, Today gauges and week chart (news_logos.py) ----------
const ThemeBtn = ({
  cls
}) => {
  const v = window.__themePref ? window.__themePref() : "auto";
  const next = v === "auto" ? "light" : v === "light" ? "dark" : "auto";
  return /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: cls || "text-xs text-slate-500",
    title: "Switch between automatic, light and dark",
    onClick: () => window.__setTheme && window.__setTheme(next)
  }, "Theme: " + (v === "auto" ? "automatic" : v));
};
const ordN = n => n + (n % 100 >= 11 && n % 100 <= 13 ? "th" : ["th", "st", "nd", "rd"][n % 10] || "th");
const lastN = n => {
  const x = String(n || "").split(" ");
  return x.length > 1 ? x.slice(1).join(" ") : x[0];
};
const GX_TABS = [["today", "Today"], ["matchup", "Matchup"], ["myteam", "Team"], ["league", "League"]];
const GX_MORE = [["setup", "Settings"], ["news", "News"], ["teams", "Teams"]];
function TopBar({
  s,
  setS,
  tab,
  go,
  ageH
}) {
  // top bar v44: five plain tabs, Setup is a page (news_logos.py)
  // older done markers kept: className={"gx-tab" + ((tab === k || (k === "myteam" && (tab === "moves" || tab === "lines")))
  // older done markers kept: {"Setup"}</button>
  const [rank, setRank] = useState(null);
  useEffect(() => {
    const id = setTimeout(() => {
      try {
        const T = leagueTable(s),
          i = T.rows.findIndex(x => x.t.id === s.me);
        setRank(i >= 0 ? [i + 1, T.rows.length] : null);
      } catch (e) {}
    }, 400);
    return () => clearTimeout(id);
  }, [s.players, s.wk, s.blend, window.__PMODE]);
  const name = teamName(s, s.me) || "My team";
  const sync = s.lastSync ? toDate(s.lastSync) : null;
  const TABS = [["today", "Today", ["today"]], ["matchup", "Matchup", ["matchup"]], ["myteam", "Team", ["myteam", "moves", "lines"]], ["league", "League", ["league", "teams"]], ["setup", "Setup", ["setup", "news"]]];
  const W = gxWarn(s);
  return /*#__PURE__*/React.createElement("div", {
    className: "m-hide max-w-6xl mx-auto px-3 flex items-end gap-1",
    style: {
      paddingTop: 10
    }
  }, /*#__PURE__*/React.createElement("span", {
    className: "gx-badge"
  }, (name[0] || "K").toUpperCase()), /*#__PURE__*/React.createElement("span", {
    style: {
      margin: "0 14px 10px 8px",
      lineHeight: 1.2,
      minWidth: 0
    }
  }, /*#__PURE__*/React.createElement("span", {
    className: "block font-semibold truncate",
    style: {
      maxWidth: 180
    }
  }, name), /*#__PURE__*/React.createElement("span", {
    className: "block text-xs text-slate-500"
  }, rank ? ordN(rank[0]) + " of " + rank[1] : s.league || "\u00a0")), GX_TABS103.map(([k, l, t, sb]) => /*#__PURE__*/React.createElement("a", {
    key: k,
    href: gxHash(t, sb || undefined),
    onClick: e => {
      if (gxNewTab(e)) return;
      e.preventDefault();
      go(t, sb || undefined);
    },
    className: "gx-tab" + (gxTabOn103(k, tab) ? " on" : "")
  }, l)), /*#__PURE__*/React.createElement("a", {
    className: "gx-tab",
    href: "ai-dashboard.html",
    target: "_blank",
    rel: "noopener",
    "data-r63": "ailab"
  }, "AI Lab"), /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: "ml-auto gx-tab",
    onClick: () => window.dispatchEvent(new Event("gm-search"))
  }, "Search"), /*#__PURE__*/React.createElement("span", {
    className: "text-xs text-slate-500 whitespace-nowrap",
    style: {
      marginBottom: 12,
      marginLeft: 12
    },
    title: s.lastSync ? "Synced " + fmtTime(s.lastSync) : ""
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      display: "inline-block",
      width: 6,
      height: 6,
      borderRadius: 99,
      marginRight: 6,
      verticalAlign: 1,
      background: !s.lastSync ? "var(--faint)" : ageH !== null && ageH > 2 ? "var(--bad)" : "var(--good)"
    }
  }), sync ? "Synced " + sync.toLocaleTimeString([], {
    hour: "numeric",
    minute: "2-digit"
  }) : "Not synced yet"));
}
const GxRing = ({
  v,
  big
}) => {
  // ring v36: the circle is back (older marker kept: dial v35) (news_logos.py)
  const size = big ? 104 : 64,
    m = size / 2,
    r = big ? 36 : 26,
    w = big ? 6 : 5,
    c = 2 * Math.PI * r;
  const p = v == null ? 0 : Math.max(0.01, Math.min(0.99, v));
  const col = v == null ? "var(--faint)" : v >= 0.5 ? "var(--good)" : "var(--bad)";
  return /*#__PURE__*/React.createElement("svg", {
    viewBox: "0 0 " + size + " " + size,
    width: size,
    height: size,
    className: "gx-svg",
    style: {
      flexShrink: 0,
      display: "block"
    },
    role: "img",
    "aria-label": v == null ? "Win chance not available" : wpTxt(v) + " chance to win"
  }, big ? /*#__PURE__*/React.createElement("circle", {
    cx: m,
    cy: m,
    r: 44,
    style: {
      fill: "none",
      stroke: "var(--track)",
      strokeWidth: 1,
      strokeDasharray: "1 5.9"
    }
  }) : null, /*#__PURE__*/React.createElement("circle", {
    cx: m,
    cy: m,
    r: r,
    style: {
      fill: "none",
      stroke: "var(--track)",
      strokeWidth: w
    }
  }), v == null ? null : /*#__PURE__*/React.createElement("circle", {
    cx: m,
    cy: m,
    r: r,
    transform: "rotate(-90 " + m + " " + m + ")",
    style: {
      fill: "none",
      stroke: col,
      strokeWidth: w,
      strokeDasharray: (p * c).toFixed(1) + " " + c.toFixed(1)
    }
  }), /*#__PURE__*/React.createElement("text", {
    x: m,
    y: big ? m + 3 : m + 5,
    textAnchor: "middle",
    style: {
      fontSize: big ? 21 : 15,
      fontWeight: 600,
      fill: big ? col : "var(--ink)"
    }
  }, v == null ? "\u2013" : wpTxt(v)), big ? /*#__PURE__*/React.createElement("text", {
    x: m,
    y: m + 18,
    textAnchor: "middle",
    style: {
      fontSize: 11,
      fill: "var(--mute)"
    }
  }, "to win") : null);
};
function GxWeek({
  wk,
  A,
  B,
  aA,
  aB
}) {
  // week chart v34: drawn at real size so text stays readable, cleaner projection line (news_logos.py)
  const [W, setW] = useState(620);
  const box = React.useRef(null);
  useEffect(() => {
    const el = box.current;
    if (!el) return;
    const fit = () => setW(Math.max(300, Math.round(el.clientWidth)));
    fit();
    if (window.ResizeObserver) {
      const ro = new ResizeObserver(fit);
      ro.observe(el);
      return () => ro.disconnect();
    }
    window.addEventListener("resize", fit);
    return () => window.removeEventListener("resize", fit);
  }, []);
  const dates = wk.dates || [],
    n = dates.length,
    today = todayISO();
  if (!n) return /*#__PURE__*/React.createElement("div", {
    ref: box
  });
  let run = aA - aB - (A.act - B.act);
  const rows = dates.map((dt, d) => {
    const x = A.days[d],
      y = B.days[d],
      dv = x.act + x.total - (y.act + y.total);
    run += dv;
    return {
      dt,
      dv,
      run,
      st: dt < today ? "f" : dt === today ? "t" : "p"
    };
  });
  const grid = Math.max(10, Math.ceil(rows.reduce((mx, r) => Math.max(mx, Math.abs(r.dv)), 0) / 10) * 10),
    sc = 46 / grid;
  const L = 34,
    R = W - 16,
    colW = (R - L) / n,
    cx = i => L + colW * (i + 0.5),
    bw = Math.min(40, colW * 0.36);
  const lo = Math.min.apply(null, rows.map(r => r.run)),
    hi = Math.max.apply(null, rows.map(r => r.run));
  const ry = v => hi === lo ? 167 : 178 - (v - lo) / (hi - lo) * 22;
  const ci = rows.findIndex(r => r.st !== "f"),
    last = ci < 0 ? n - 1 : ci - 1;
  const pts = (a, b) => rows.slice(a, b + 1).map((r, i) => cx(a + i).toFixed(1) + "," + ry(r.run).toFixed(1)).join(" ");
  const sg = v => (v > 0 ? "+" : "") + Math.round(v);
  const col = v => v >= 0 ? "var(--good)" : "var(--bad)";
  const tx = (size, fill, weight) => ({
    fontSize: size,
    fill,
    fontWeight: weight || 400
  });
  const nowLeft = last >= n - 3;
  return /*#__PURE__*/React.createElement("div", {
    ref: box,
    style: {
      overflow: "hidden"
    }
  }, /*#__PURE__*/React.createElement("svg", {
    viewBox: "0 0 " + W + " 196",
    width: W,
    height: 196,
    className: "gx-svg",
    style: {
      display: "block",
      marginTop: 6
    },
    role: "img",
    "aria-label": "Margin each day this week and the running total"
  }, rows.map((r, i) => r.st === "t" ? /*#__PURE__*/React.createElement("rect", {
    key: "h" + i,
    x: cx(i) - colW / 2 + 2,
    y: 4,
    width: colW - 4,
    height: 136,
    style: {
      fill: "var(--accentSoft)"
    }
  }) : null), /*#__PURE__*/React.createElement("line", {
    x1: L,
    y1: 36,
    x2: R,
    y2: 36,
    style: {
      stroke: "var(--line)",
      strokeDasharray: "2 4"
    }
  }), /*#__PURE__*/React.createElement("line", {
    x1: L,
    y1: 82,
    x2: R,
    y2: 82,
    style: {
      stroke: "var(--faint)"
    }
  }), /*#__PURE__*/React.createElement("line", {
    x1: L,
    y1: 128,
    x2: R,
    y2: 128,
    style: {
      stroke: "var(--line)",
      strokeDasharray: "2 4"
    }
  }), /*#__PURE__*/React.createElement("text", {
    x: 26,
    y: 40,
    textAnchor: "end",
    style: tx(11, "var(--faint)")
  }, "+" + grid), /*#__PURE__*/React.createElement("text", {
    x: 26,
    y: 86,
    textAnchor: "end",
    style: tx(11, "var(--faint)")
  }, "0"), /*#__PURE__*/React.createElement("text", {
    x: 26,
    y: 132,
    textAnchor: "end",
    style: tx(11, "var(--faint)")
  }, "-" + grid), rows.map((r, i) => {
    const h = Math.max(1, Math.abs(r.dv) * sc),
      up = r.dv >= 0,
      y = up ? 81 - h : 83,
      flat = Math.abs(r.dv) < 0.05;
    return /*#__PURE__*/React.createElement("g", {
      key: r.dt
    }, /*#__PURE__*/React.createElement("text", {
      x: cx(i),
      y: 18,
      textAnchor: "middle",
      style: tx(12, r.st === "t" ? "var(--accent)" : "var(--mute)", r.st === "t" ? 600 : 400)
    }, r.st === "t" ? "Today" : dayLabel(r.dt).split(",")[0]), flat ? null : r.st === "p" ? /*#__PURE__*/React.createElement("rect", {
      x: cx(i) - bw / 2 + 0.5,
      y: y + 0.5,
      width: bw - 1,
      height: Math.max(1, h - 1),
      style: {
        fill: "none",
        stroke: col(r.dv),
        strokeWidth: 1,
        strokeDasharray: "3 3"
      }
    }) : /*#__PURE__*/React.createElement("rect", {
      x: cx(i) - bw / 2,
      y: y,
      width: bw,
      height: h,
      style: {
        fill: col(r.dv)
      }
    }), /*#__PURE__*/React.createElement("text", {
      x: cx(i),
      y: up && !flat ? 98 : 76,
      textAnchor: "middle",
      style: tx(12, flat ? "var(--faint)" : col(r.dv))
    }, flat ? "0" : sg(r.dv)));
  }), /*#__PURE__*/React.createElement("line", {
    x1: L,
    y1: 152,
    x2: R,
    y2: 152,
    style: {
      stroke: "var(--line)"
    }
  }), last < n - 1 ? /*#__PURE__*/React.createElement("polyline", {
    points: pts(Math.max(last, 0), n - 1),
    style: {
      fill: "none",
      stroke: "var(--accent)",
      strokeWidth: 1,
      opacity: 0.35
    }
  }) : null, last >= 1 ? /*#__PURE__*/React.createElement("polyline", {
    points: pts(0, last),
    style: {
      fill: "none",
      stroke: "var(--accent)",
      strokeWidth: 1.5
    }
  }) : null, rows.map((r, i) => i > last ? /*#__PURE__*/React.createElement("circle", {
    key: "p" + i,
    cx: cx(i),
    cy: ry(r.run),
    r: 2.5,
    style: {
      fill: "var(--card)",
      stroke: "var(--accent)",
      strokeWidth: 1,
      opacity: 0.55
    }
  }) : null), rows.map((r, i) => i <= last ? /*#__PURE__*/React.createElement("circle", {
    key: "c" + i,
    cx: cx(i),
    cy: ry(r.run),
    r: i === last ? 3.5 : 2.5,
    style: i === last ? {
      fill: "var(--card)",
      stroke: "var(--accent)",
      strokeWidth: 1.5
    } : {
      fill: "var(--accent)"
    }
  }) : null), last >= 0 && ci >= 0 ? /*#__PURE__*/React.createElement("text", {
    x: cx(last) + (nowLeft ? -8 : 8),
    y: 192,
    textAnchor: nowLeft ? "end" : "start",
    style: tx(11, "var(--accent)")
  }, sg(aA - aB) + " now") : null, /*#__PURE__*/React.createElement("text", {
    x: R,
    y: 192,
    textAnchor: "end",
    style: tx(11, "var(--mute)")
  }, sg(rows[n - 1].run) + (ci < 0 ? " final" : " projected"))));
}

// ---------- round 33: home page panels (news_logos.py) ----------
const GxPanel = ({
  title,
  right,
  children
}) => /*#__PURE__*/React.createElement("div", {
  className: "gx-pn",
  style: {
    minWidth: 0
  }
}, /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("div", {
  style: {
    display: "flex",
    alignItems: "baseline",
    marginBottom: 6
  }
}, /*#__PURE__*/React.createElement("span", {
  className: "gx-tag"
}, title), right ? /*#__PURE__*/React.createElement("span", {
  className: "text-xs text-slate-500",
  style: {
    marginLeft: "auto"
  }
}, right) : null), children);
function GxCarry({
  s,
  wk
}) {
  const K = s.blend,
    gen = (window.ESPN_DATA || {}).generated;
  const data = useMemo(() => {
    const P = pby(),
      acc = {};
    (wk.dates || []).forEach(dt => {
      const AD = actDay(s.me, dt);
      if (!AD) return;
      Object.entries(AD).forEach(([pid, v]) => {
        if (!v || v[0] == null || !ESLOT[v[1]]) return;
        const p = P["e" + pid];
        if (!p || !(SCHED[p.t] && SCHED[p.t].has(dt))) return;
        const st = gState(p.t, dt).s;
        if (st === "P" || p.p === "G" && !v[0]) return;
        const a = acc[p.id] = acc[p.id] || {
          p,
          pts: 0,
          g: 0,
          diff: 0
        };
        a.pts += v[0];
        a.g++;
        if (st === "F") a.diff += v[0] - effAvg(p, K, dt);
      });
    });
    const list = Object.values(acc),
      top = [...list].sort((x, y) => y.pts - x.pts).slice(0, 3);
    const low = list.filter(x => top.indexOf(x) < 0).sort((x, y) => x.diff - y.diff)[0];
    return {
      top,
      low: low && low.diff <= -3 ? low : null
    };
  }, [s.players, wk, K, gen]);
  const row = (x, i, note) => /*#__PURE__*/React.createElement("div", {
    key: x.p.id,
    className: "gx-row",
    style: i === 0 ? {
      borderTop: 0
    } : note ? {
      borderTop: "1px dashed var(--line2)"
    } : null
  }, /*#__PURE__*/React.createElement("span", {
    className: "min-w-0 truncate",
    style: {
      flex: 1
    }
  }, /*#__PURE__*/React.createElement("span", {
    className: "gx-pl"
  }, /*#__PURE__*/React.createElement(GxFace, {
    p: x.p,
    size: 20
  }), /*#__PURE__*/React.createElement(PN, {
    p: x.p,
    className: ""
  }))), note ? /*#__PURE__*/React.createElement("span", {
    className: "text-xs whitespace-nowrap",
    style: {
      color: "var(--bad)"
    }
  }, note) : /*#__PURE__*/React.createElement("span", {
    className: "text-xs text-slate-500 whitespace-nowrap"
  }, x.g, " game", x.g === 1 ? "" : "s"), /*#__PURE__*/React.createElement("span", {
    className: "font-semibold text-right",
    style: {
      minWidth: 40,
      fontVariantNumeric: "tabular-nums"
    }
  }, f1(x.pts)));
  return /*#__PURE__*/React.createElement(GxPanel, {
    title: "Who's carrying you",
    right: "This matchup, in your lineup"
  }, data.top.length ? data.top.map((x, i) => row(x, i, null)) : /*#__PURE__*/React.createElement("div", {
    className: "text-sm text-slate-500"
  }, "No games counted yet in this matchup."), data.low ? row(data.low, 9, Math.round(-data.low.diff) + " under projection") : null);
}
function GxGoalies({
  s,
  wk
}) {
  const today = todayISO();
  const rows = s.players.filter(p => p.ft === s.me && p.p === "G" && !p.ir).map(p => {
    const id = String(p.id).slice(1);
    let st = 0,
      pts = 0,
      left = 0;
    (wk.dates || []).forEach((dt, d) => {
      if (!(wk.games[p.t] || []).includes(d)) return;
      if (gState(p.t, dt).s !== "P") {
        const AD = actDay(s.me, dt),
          v = AD ? AD[id] : null;
        if (v && v[1] === 5 && v[0]) {
          st++;
          pts += v[0];
        }
      } else if (dt >= today && avail(p, dt) > 0 && gStart(p, dt).v >= 0.5) left++;
    });
    return {
      p,
      st,
      pts,
      left
    };
  });
  return /*#__PURE__*/React.createElement(GxPanel, {
    title: "Goalie board",
    right: "starts \u00b7 left \u00b7 points"
  }, rows.length ? rows.map((x, i) => /*#__PURE__*/React.createElement("div", {
    key: x.p.id,
    className: "gx-row",
    style: i ? null : {
      borderTop: 0
    }
  }, /*#__PURE__*/React.createElement("span", {
    className: "min-w-0 truncate",
    style: {
      flex: 1
    }
  }, /*#__PURE__*/React.createElement("span", {
    className: "gx-pl"
  }, /*#__PURE__*/React.createElement(GxFace, {
    p: x.p,
    size: 20
  }), /*#__PURE__*/React.createElement(PN, {
    p: x.p,
    className: ""
  }))), /*#__PURE__*/React.createElement("span", {
    className: "text-xs text-slate-500 whitespace-nowrap"
  }, x.st + " \u00b7 " + x.left), /*#__PURE__*/React.createElement("span", {
    className: "font-semibold text-right",
    style: {
      minWidth: 40,
      fontVariantNumeric: "tabular-nums",
      color: x.pts > 5 ? "var(--good)" : x.pts < 0 ? "var(--bad)" : "var(--ink)"
    }
  }, f1(x.pts)))) : /*#__PURE__*/React.createElement("div", {
    className: "text-sm text-slate-500"
  }, "No goalies on your roster."));
}
// chance of a top-6 finish: 2,000 simulated seasons from each team's strength and the real schedule
function playoffSim(s) {
  const ids = s.teams.map(t => t.id);
  if (ids.length < 2 || ids.indexOf(s.me) < 0) return null;
  const T = leagueTable(s),
    str = {},
    K = s.blend,
    today = todayISO();
  T.rows.forEach(x => str[x.t.id] = x.strength);
  const end = Math.min(s.weeks.length, s.poStart ?? 24),
    w0 = {},
    pf = {},
    todo = [];
  ids.forEach(id => {
    w0[id] = 0;
    pf[id] = 0;
  });
  s.weeks.slice(0, end).forEach(w => {
    const len = (w.dates || []).length,
      pairs = (w.pairs || []).filter(p => p[0] && p[1] && w0[p[0]] != null && w0[p[1]] != null);
    if (!len || !pairs.length) return;
    if (effDone(w, s.autoDone) >= len) {
      pairs.forEach(([a, b]) => {
        const x = +gxAct120(w)[a] || 0,
          y = +gxAct120(w)[b] || 0;
        if (!x && !y) return;
        pf[a] += x;
        pf[b] += y;
        if (x > y) w0[a]++;else if (y > x) w0[b]++;else {
          w0[a] += 0.5;
          w0[b] += 0.5;
        }
      });
      return;
    }
    const live = w.dates[0] <= today ? deriveWeek(w, s.autoDone) : null;
    pairs.forEach(([a, b]) => {
      let p;
      if (live) {
        const R = id => weekLive(s.players.filter(q => q.ft === id), live, K, id),
          act = id => +gxAct120(live)[id] || 0;
        p = winProb(R(a), R(b), act(a), act(b));
      } else p = normCdf(((str[a] || 0) - (str[b] || 0)) * (len / 7) / (80 * Math.sqrt(len / 7)));
      pf[a] += (str[a] || 0) * (len / 7);
      pf[b] += (str[b] || 0) * (len / 7);
      todo.push([a, b, Math.max(0.02, Math.min(0.98, p))]);
    });
  });
  let seed = 20262027;
  const rnd = () => {
    seed = seed + 0x6d2b79f5 | 0;
    let t = Math.imul(seed ^ seed >>> 15, 1 | seed);
    t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
    return ((t ^ t >>> 14) >>> 0) / 4294967296;
  };
  const N = 2000,
    cut = Math.min(6, ids.length - 1);
  let inN = 0,
    sum = 0;
  for (let k = 0; k < N; k++) {
    const w = Object.assign({}, w0);
    for (let j = 0; j < todo.length; j++) {
      const m = todo[j];
      if (rnd() < m[2]) w[m[0]]++;else w[m[1]]++;
    }
    const r = ids.slice().sort((a, b) => w[b] - w[a] || pf[b] - pf[a]).indexOf(s.me) + 1;
    if (r <= cut) inN++;
    sum += r;
  }
  return {
    odds: inN / N,
    finish: Math.round(sum / N),
    cut
  };
}
function GxPlayoff({
  s
}) {
  const [res, setRes] = useState(null);
  useEffect(() => {
    const id = setTimeout(() => {
      try {
        setRes(playoffSim(s));
      } catch (e) {
        setRes(null);
      }
    }, 500);
    return () => clearTimeout(id);
  }, [s.players, s.weeks, s.wk, s.blend, window.__PMODE]);
  useEffect(() => {
    if (res) uiSet("po:" + s.wk, res.odds);
  }, [res ? res.odds : null, s.wk]);
  const prev = uiGet()["po:" + (s.wk - 1)];
  const d = res && prev != null ? Math.round(res.odds * 100) - Math.round(prev * 100) : null;
  return /*#__PURE__*/React.createElement("div", {
    className: "gx-pn"
  }, /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      alignItems: "center",
      gap: 16
    }
  }, /*#__PURE__*/React.createElement(GxRing, {
    v: res ? res.odds : null
  }), /*#__PURE__*/React.createElement("div", {
    className: "min-w-0",
    style: {
      flex: 1
    }
  }, /*#__PURE__*/React.createElement("div", {
    className: "gx-tag"
  }, "Playoff odds"), /*#__PURE__*/React.createElement("div", {
    style: {
      marginTop: 6
    }
  }, res ? "Projected to finish " + ordN(res.finish) : "Working it out...", " ", /*#__PURE__*/React.createElement("span", {
    className: "text-slate-500"
  }, "\u00b7 top " + (res ? res.cut : 6) + " make it"))), d != null ? /*#__PURE__*/React.createElement("div", {
    className: "text-right whitespace-nowrap"
  }, /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500"
  }, "since last week"), /*#__PURE__*/React.createElement("div", {
    style: {
      color: d > 0 ? "var(--good)" : d < 0 ? "var(--bad)" : "var(--mute)"
    }
  }, (d > 0 ? "+" : "") + d + "%")) : null));
}
function GxHome({
  s,
  wk,
  A,
  B
}) {
  // home v34: games this matchup and the league are full width (news_logos.py)
  return /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement(GxGamesAny, {
    s: s,
    wk: wk,
    A: A,
    B: B
  }), /*#__PURE__*/React.createElement(GxLeagueAny, {
    s: s,
    wk: wk
  }), /*#__PURE__*/React.createElement("div", {
    className: "grid md:grid-cols-2 gap-3"
  }, /*#__PURE__*/React.createElement(GxCarry, {
    s: s,
    wk: wk
  }), /*#__PURE__*/React.createElement(GxGoalies, {
    s: s,
    wk: wk
  })), /*#__PURE__*/React.createElement(GxPlayoff, {
    s: s
  }));
}

// ---------- round 37: Team sub-pages and box-score history for the roster (news_logos.py) ----------
const TEAM_SUBS = [["roster", "Roster"], ["pickups", "Pickups"], ["plan", "Plan"], ["trades", "Trades"], ["lines", "Lines"]];
const PICK_SUBS = [["adddrop", "Pickups"], ["advice", "Advice"], ["goalies", "Goalies"], ["injuries", "Injuries"]];
function SubBar({
  tab,
  sub,
  go,
  setSubs,
  nav,
  s,
  wk
}) {
  if (tab === "matchup") return s && wk ? /*#__PURE__*/React.createElement(MatchStrip, {
    s: s,
    wk: wk
  }) : null;
  const team = tab === "myteam" || tab === "moves" || tab === "lines";
  if (!team) {
    const back = tab === "news" || tab === "setup" && sub && sub !== "settings" ? ["Setup", () => go("setup", "settings")] : tab === "league" && (sub === "playoffs" || sub === "players") ? ["League", () => go("league", "power")] : null;
    return back ? /*#__PURE__*/React.createElement("div", {
      className: "mb-3"
    }, /*#__PURE__*/React.createElement("button", {
      type: "button",
      className: "text-sm text-blue-600",
      onClick: back[1]
    }, "\u2039 Back to " + back[0])) : null;
  }
  const inPick = PICK_SUBS.some(x => x[0] === sub);
  const cur = tab === "myteam" ? "roster" : tab === "lines" ? "lines" : sub === "planner" ? "plan" : sub === "trades" ? "trades" : "pickups";
  const to = k => k === "roster" ? go("myteam") : k === "lines" ? go("lines") : k === "plan" ? go("moves", "planner") : k === "trades" ? go("moves", "trades") : go("moves", "adddrop");
  return /*#__PURE__*/React.createElement("div", {
    className: "mb-4"
  }, /*#__PURE__*/React.createElement("div", {
    className: "flex gap-2 overflow-x-auto navscroll pb-1"
  }, TEAM_SUBS.map(([k, l]) => /*#__PURE__*/React.createElement("a", {
    key: k,
    href: GX_TEAM_HREF[k],
    onClick: e => {
      if (gxNewTab(e)) return;
      e.preventDefault();
      to(k);
    },
    className: "px-3 py-1.5 rounded-full text-sm border whitespace-nowrap " + (cur === k ? "bg-blue-600 text-white border-blue-600" : "bg-white border-slate-300 text-slate-600")
  }, l))), cur === "pickups" ? /*#__PURE__*/React.createElement("div", {
    className: "flex gap-4 overflow-x-auto navscroll text-sm",
    style: {
      marginTop: 10
    }
  }, PICK_SUBS.map(([k, l]) => /*#__PURE__*/React.createElement("a", {
    key: k,
    href: gxHash("moves", k),
    onClick: e => {
      /* gx072-pick */if (gxNewTab(e)) return;
      e.preventDefault();
      go("moves", k);
    },
    className: "whitespace-nowrap " + (sub === k || k === "adddrop" && !inPick ? "font-semibold" : "text-slate-500")
  }, l))) : null);
}
const gxBoxIdx = () => fetch("box/index.json?t=" + Date.now()).then(r => r.ok ? r.json() : null).then(j => j && j.dates || []).catch(() => []);
const gxBoxDay = d => {
  const B = window.__BOX = window.__BOX || {
    idx: null,
    at: 0,
    days: {}
  };
  if (B.days[d]) return Promise.resolve(B.days[d]);
  return fetch("box/" + d + ".json").then(r => r.ok ? r.json() : null).then(j => {
    if (j && j.p) B.days[d] = j.p;
    return j && j.p || null;
  }).catch(() => null);
};

// ---------- round 40: Pickups list (news_logos.py) ----------
const gxEst = (x, sc) => x.sv != null ? (x.dec === "W" ? sc.W ?? 5 : 0) + (x.dec === "O" ? sc.OTL ?? 1 : 0) + (x.sv || 0) * (sc.SV ?? 0.6) + (x.ga || 0) * (sc.GA ?? -3) : (x.g || 0) * (sc.G ?? 6) + (x.a || 0) * (sc.A ?? 4) + (x.pm || 0) * (sc.PM ?? 2) + (x.sog || 0) * (sc.SOG ?? 1) + (x.hit || 0) * (sc.HIT ?? 0.1) + (x.blk || 0) * (sc.BLK ?? 1) + (x.ppg || 0) * (sc.PPP ?? 2);
const gxLast5 = (ids, sc) => gxBoxIdx().then(ds => Promise.all(ds.slice(-14).map(d => gxBoxDay(d)))).then(days => {
  const out = {};
  ids.forEach(pid => {
    const a = [];
    days.forEach(day => {
      const x = day && day[pid];
      if (x) a.push(x.fp != null ? x.fp : gxEst(x, sc));
    });
    out[pid] = a.slice(-5);
  });
  return out;
}).catch(() => ({}));
function Pickups({
  s,
  setS,
  wk
}) {
  gxUseSort108(); /* gx109 */
  const effAvg = gxPgAvg; /* gx088-pk */
  const K = s.blend;
  const [H, setH] = useState(1);
  const [pos, setPos] = useState(() => {
    const v = window.__PICK_POS || "all";
    window.__PICK_POS = "";
    return v;
  });
  const [q, setQ] = useState(() => {
    const v = window.__PICK_Q || "";
    window.__PICK_Q = "";
    return v;
  });
  const [limit, setLimit] = useState(100000); /* gx118: show all */
  useEffect(() => {
    const h = () => {
      if (window.__PICK_Q) {
        setQ(window.__PICK_Q);
        window.__PICK_Q = "";
      }
      if (window.__PICK_POS) {
        setPos(window.__PICK_POS);
        window.__PICK_POS = "";
      }
    };
    window.addEventListener("gm-pick", h);
    return () => window.removeEventListener("gm-pick", h);
  }, []);
  const [sim, setSim] = useState(null);
  const [hist, setHist] = useState({});
  const sP = useMemo(() => planS(s), [s]);
  const plan = sP !== s;
  const wkP = useMemo(() => plan ? deriveWeek(sP.weeks[sP.wk], sP.autoDone) : wk, [sP, wk]);
  const gxHideV = gxUseHide(); /* gx075-m */
  const M = useMemo(() => gxMoves102(s, sP, {
    H,
    pos,
    q
  }), [sP, H, pos, q, gxHideV]);
  const base = useMemo(() => planBase(s, sP), [sP]);
  const minGain = s.minGain ?? 3;
  const all = q ? M.res : M.res.filter(r => r.gain >= minGain);
  // change 079: sort the whole list by any heading before it is cut to the first rows
  const [srt79, setSrt79] = useState("add");
  const wAll79 = useMemo(() => {
    const o = {};
    if (srt79 !== "win" || base == null) return o;
    all.slice(0, 150).forEach(r => {
      o[r.f.id] = winChance(sP, afterMove(sP, r.f, r.d));
    });
    return o;
  }, [M, srt79, base]);
  const key79 = {
    l5: r => gxL5v(hist[String(r.f.id).slice(1)]),
    g: r => M.gamesIn(r.f),
    x: r => effAvg(r.f, K),
    win: r => wAll79[r.f.id] != null ? wAll79[r.f.id] : -1
  }[srt79];
  const rows = (key79 ? [...all].sort((a, b) => key79(b) - key79(a) || b.gain - a.gain) : all).slice(0, limit);
  const wins = useMemo(() => {
    const o = {};
    if (base == null) return o;
    rows.forEach(r => {
      o[r.f.id] = winChance(sP, afterMove(sP, r.f, r.d));
    });
    return o;
  }, [M, limit, base, srt79, wAll79]);
  const ids = (srt79 === "l5" ? all.slice(0, 150) : rows).map(r => String(r.f.id).slice(1)).join(",");
  useEffect(() => {
    let dead = false;
    if (!ids) return;
    gxLast5(ids.split(","), s.sc || {}).then(h => {
      if (!dead) setHist(x => Object.assign({}, x, h));
    });
    return () => {
      dead = true;
    };
  }, [ids]);
  const ml = movesLeft(s, s.me, wk);
  const pw = plan ? sP.weeks[sP.wk] || {} : null,
    d0 = pw ? (pw.dates || [])[0] : null;
  const qq = nrm(q);
  const others = qq.length >= 2 ? s.players.filter(p => p.ft !== "fa" && p.ft !== s.me && nrm(p.n).includes(qq)).slice(0, 6) : [];
  const hLabel = plan ? {
    1: "next week",
    4: "4 weeks from next week",
    0: "rest of season"
  }[H] : {
    1: "rest of this week",
    4: "next 4 weeks",
    0: "rest of season"
  }[H];
  const spark = p => {
    const h = hist[String(p.id).slice(1)] || [];
    return /*#__PURE__*/React.createElement("div", {
      className: "gx-sp m-hide",
      title: "Last five games, oldest to newest"
    }, h.length ? h.map((v, i) => /*#__PURE__*/React.createElement("i", {
      key: i,
      style: {
        height: Math.max(2, Math.min(22, Math.max(0, v) / 20 * 22)),
        background: v < 0 ? "var(--bad)" : "var(--ink2)"
      }
    })) : /*#__PURE__*/React.createElement("span", {
      className: "text-xs text-slate-500"
    }, "\u2013"));
  };
  return /*#__PURE__*/React.createElement("div", {
    className: "space-y-3"
  }, /*#__PURE__*/React.createElement(GxFaToggle105, {
    cur: "adddrop",
    go: (t, k) => {
      window.location.hash = gxHash(t, k);
    }
  }), /*#__PURE__*/React.createElement("div", {
    className: "text-sm"
  }, /*#__PURE__*/React.createElement("span", {
    className: "font-semibold"
  }, ml === 0 ? "No moves left" : ml == null ? "" : ml + " move" + (ml === 1 ? "" : "s") + " left"), !plan ? /*#__PURE__*/React.createElement(GxHsLine, {
    s: s,
    base: base,
    ml: ml
  }) : null, plan ? /*#__PURE__*/React.createElement("span", {
    className: "text-slate-500"
  }, " \u00b7 showing next week") : null), /*#__PURE__*/React.createElement(GxFlt108, {
    label: {
      all: "All",
      F: "Forwards",
      D: "Defence",
      G: "Goalies"
    }[pos] + " \u00b7 " + {
      1: plan ? "Next week" : "This week",
      4: "Next 4 weeks",
      0: "Rest of season"
    }[H] + " \u00b7 " + gxRngLbl108()
  }, /*#__PURE__*/React.createElement("div", {
    className: "flex flex-wrap gap-2 items-center"
  }, /*#__PURE__*/React.createElement(Pills, {
    items: [["all", "All"], ["F", "Forwards"], ["D", "Defence"], ["G", "Goalies"]],
    value: pos,
    onChange: v => {
      setPos(v);
      setLimit(100000);
    }
  }), /*#__PURE__*/React.createElement(Pills, {
    items: [[1, plan ? "Next week" : "This week"], [4, "Next 4 weeks"], [0, "Rest of season"]],
    value: H,
    onChange: v => {
      setH(v);
      setLimit(100000);
    }
  })), /*#__PURE__*/React.createElement(GxRngSel100, null)), !plan ? /*#__PURE__*/React.createElement(GxHeadStart, {
    s: s,
    base: base,
    ml: ml
  }) : null, /*#__PURE__*/React.createElement(GxWatchPanel, {
    s: s
  }), /*#__PURE__*/React.createElement(GxHiddenPanel, {
    s: s
  }), /*#__PURE__*/React.createElement("input", {
    className: inp + " w-full",
    placeholder: "Search any player",
    value: q,
    onChange: e => setQ(e.target.value)
  }), /*#__PURE__*/React.createElement("div", {
    className: "gx-pn"
  }, /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("div", {
    className: "gx-sc99"
  }, /*#__PURE__*/React.createElement("div", {
    className: "gx-pk text-xs text-slate-500 " + gxPkMode106(pos),
    style: {
      borderTop: 0,
      paddingTop: 0
    }
  }, /*#__PURE__*/React.createElement("span", null), /*#__PURE__*/React.createElement("span", null, "Player"), /*#__PURE__*/React.createElement(GxSH, {
    k: "l5",
    cur: srt79,
    set: v => {
      setSrt79(v);
      setLimit(100000);
    },
    def: "add",
    cls: "m-hide"
  }, "Last 5"), /*#__PURE__*/React.createElement(GxSH, {
    k: "g",
    cur: srt79,
    set: v => {
      setSrt79(v);
      setLimit(100000);
    },
    def: "add",
    cls: "m-hide"
  }, "Games"), /*#__PURE__*/React.createElement(GxSH, {
    k: "x",
    cur: srt79,
    set: v => {
      setSrt79(v);
      setLimit(100000);
    },
    def: "add",
    cls: "m-hide"
  }, "Expected"), /*#__PURE__*/React.createElement(GxSH, {
    k: "add",
    cur: srt79,
    set: v => {
      setSrt79(v);
      setLimit(100000);
    },
    def: "add"
  }, "Adds"), /*#__PURE__*/React.createElement(GxSH, {
    k: "win",
    cur: srt79,
    set: v => {
      setSrt79(v);
      setLimit(100000);
    },
    def: "add"
  }, "Win"), /*#__PURE__*/React.createElement("span", {
    className: "n"
  }, "Avg"), /*#__PURE__*/React.createElement("span", {
    className: "n"
  }, "Rost"), /*#__PURE__*/React.createElement(GxSH106, {
    mode: pos === "G" ? "go" : "sk"
  })), rows.length ? gxSort108(rows, s, r => r.f).map(r => {
    const keep = r.gain > 0 && effAvg(r.f, K) - effAvg(r.d, K) >= 0,
      tg = shortTag(r.f, K),
      w = wins[r.f.id];
    const st = r.f.status && r.f.status !== "ACTIVE" ? M_ST[r.f.status] || r.f.status.replace(/_/g, " ") : "";
    return /*#__PURE__*/React.createElement("div", {
      key: r.f.id,
      className: "gx-pk row " + gxPkMode106(pos),
      role: "button",
      onClick: () => setSim({
        add: r.f.id,
        drop: r.d.id
      })
    }, /*#__PURE__*/React.createElement("div", {
      className: "gx-fc99"
    }, /*#__PURE__*/React.createElement(GxFace, {
      p: r.f,
      size: 26
    })), /*#__PURE__*/React.createElement("div", {
      className: "min-w-0"
    }, /*#__PURE__*/React.createElement("div", {
      className: "truncate"
    }, /*#__PURE__*/React.createElement(PN, {
      p: r.f,
      className: ""
    }), " ", /*#__PURE__*/React.createElement("span", {
      className: "text-xs text-slate-500"
    }, r.f.p), r.f.wv ? /*#__PURE__*/React.createElement("span", {
      className: "text-xs",
      style: {
        color: "var(--warn)",
        marginLeft: 6
      }
    }, "on waivers") : null, st ? /*#__PURE__*/React.createElement("span", {
      className: "text-xs",
      style: {
        color: "var(--bad)",
        marginLeft: 6
      }
    }, st) : null)), spark(r.f), /*#__PURE__*/React.createElement("div", {
      className: "n text-slate-500 m-hide"
    }, M.gamesIn(r.f)), /*#__PURE__*/React.createElement("div", {
      className: "n m-hide"
    }, f1(effAvg(r.f, K))), /*#__PURE__*/React.createElement("div", {
      className: "n font-semibold",
      style: {
        color: r.gain > 0 ? "var(--good)" : "var(--bad)"
      }
    }, (r.gain >= 0 ? "+" : "") + f1(r.gain)), /*#__PURE__*/React.createElement("div", {
      className: "n",
      style: w != null && base != null ? {
        color: w > base + 0.004 ? "var(--good)" : w < base - 0.004 ? "var(--bad)" : "var(--ink)"
      } : null
    }, w == null ? "\u2013" : wpTxt(w)), /*#__PURE__*/React.createElement("div", {
      className: "n text-slate-500"
    }, r.f.gp ? f1(r.f.tot / r.f.gp) : "-"), /*#__PURE__*/React.createElement("div", {
      className: "n text-slate-500"
    }, r.f.own != null ? Math.round(r.f.own) + "%" : "-"), /*#__PURE__*/React.createElement(GxSC106, {
      p: r.f,
      s: s,
      mode: pos === "G" ? "full" : "mx"
    }));
  }) : /*#__PURE__*/React.createElement("div", {
    className: "text-sm text-slate-500",
    style: {
      padding: "10px 0"
    }
  }, q ? "No free agent matches that name." : "No pickup adds " + minGain + " or more points for this window.")), all.length > rows.length ? /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: "text-sm text-blue-600",
    style: {
      marginTop: 10
    },
    onClick: () => setLimit(limit + 25)
  }, "Show ", Math.min(25, all.length - rows.length), " more") : null), others.length ? /*#__PURE__*/React.createElement(GxPanel, {
    title: "On other teams"
  }, others.map((p, i) => /*#__PURE__*/React.createElement("div", {
    key: p.id,
    className: "gx-row",
    style: i ? null : {
      borderTop: 0
    }
  }, /*#__PURE__*/React.createElement(GxFace, {
    p: p,
    size: 22
  }), /*#__PURE__*/React.createElement("span", {
    className: "min-w-0 truncate",
    style: {
      flex: 1
    }
  }, /*#__PURE__*/React.createElement(PN, {
    p: p,
    className: ""
  }), " ", /*#__PURE__*/React.createElement("span", {
    className: "text-xs text-slate-500"
  }, p.p)), /*#__PURE__*/React.createElement("span", {
    className: "text-xs text-slate-500 truncate"
  }, /*#__PURE__*/React.createElement(TL, {
    s: s,
    id: p.ft
  })), /*#__PURE__*/React.createElement("span", {
    className: "font-semibold text-right",
    style: {
      minWidth: 40,
      fontVariantNumeric: "tabular-nums"
    }
  }, f1(effAvg(p, K)))))) : null, sim ? /*#__PURE__*/React.createElement(GxSim107, {
    s: sP,
    setS: setS,
    wk: wkP,
    M: M,
    H: H,
    hLabel: hLabel,
    init: sim,
    wBase: base,
    onClose: () => setSim(null)
  }) : null);
}

// ---------- round 41: Plan page (news_logos.py) ----------
function PlanPage({
  s,
  setS,
  wk
}) {
  const K = s.blend,
    today = todayISO();
  const sP = useMemo(() => planS(s), [s]);
  const plan = sP !== s;
  const wkP = useMemo(() => plan ? deriveWeek(sP.weeks[sP.wk], sP.autoDone) : wk, [sP, wk]);
  const dates = wkP.dates || [],
    ti = dates.indexOf(today);
  const d0 = Math.min(dates.length, Math.max(wkP.done || 0, ti >= 0 ? ti : 0) + (ti >= 0 && lockedToday() ? 1 : 0));
  const ml = movesLeft(sP, sP.me, wkP),
    left = ml == null ? 3 : ml;
  const [res, setRes] = useState(null);
  const [busy, setBusy] = useState(true);
  const [openW, setOpenW] = useState(-1);
  useEffect(() => {
    let dead = false;
    setBusy(true);
    const id = setTimeout(() => {
      let r = null;
      try {
        if (left > 0 && d0 < dates.length) {
          const p = buildPlan(sP, wkP, d0, left),
            b = planBase(s, sP);
          r = {
            p,
            b,
            after: p.steps.map((_, i) => b == null ? null : winChance(sP, planRoster(sP, wkP, p.steps.slice(0, i + 1))))
          };
        }
      } catch (e) {
        r = null;
      }
      if (!dead) {
        setRes(r);
        setBusy(false);
      }
    }, 60);
    return () => {
      dead = true;
      clearTimeout(id);
    };
  }, [s.players, sP.wk, left, d0, window.__PMODE]);
  const waste = useMemo(() => {
    const mine = s.players.filter(p => p.ft === s.me),
      chronic = {};
    const weeks = s.weeks.slice(s.wk, s.wk + 4).map((w, i) => {
      const dw = deriveWeek(w, s.autoDone),
        from = i === 0 ? dw.done || 0 : 0,
        sit = {};
      let empty = 0,
        g = 0,
        pts = 0;
      dw.days.forEach((dl, d) => {
        if (d < from) return;
        const L = dayLineup(mine, dw, d, K);
        empty += L.empty;
        L.bench.forEach(p => {
          const x = sit[p.id] = sit[p.id] || {
            p,
            days: []
          };
          x.days.push(dl.split(",")[0]);
          g++;
          pts += p.x;
          const c = chronic[p.id] = chronic[p.id] || {
            p,
            g: 0
          };
          c.g++;
        });
      });
      return {
        dw,
        from,
        sit: Object.values(sit),
        empty,
        g,
        pts
      };
    });
    return {
      weeks,
      chronic: Object.values(chronic).filter(c => c.g >= 2).sort((a, b) => b.g - a.g).slice(0, 3),
      g: weeks.reduce((a, w) => a + w.g, 0),
      pts: weeks.reduce((a, w) => a + w.pts, 0)
    };
  }, [s.players, s.wk, K, window.__PMODE]);
  const fix = useMemo(() => {
    const w = waste.weeks[openW];
    if (!w || !w.sit.length || openW === 0 && outOfMoves(s)) return null;
    const mine = s.players.filter(p => p.ft === s.me),
      mins = {
        F: s.minF ?? 10,
        D: s.minD ?? 5,
        G: s.minGo ?? 2
      };
    const healthy = mine.filter(p => !p.ir).sort((a, b) => effAvg(b, K) - effAvg(a, K));
    const prot = new Set([...healthy.slice(0, s.protectTop ?? 8).map(p => p.id), ...mine.filter(p => p.keep).map(p => p.id)]);
    const cnt = {
      F: 0,
      D: 0,
      G: 0
    };
    healthy.forEach(p => {
      cnt[p.p]++;
    });
    const drops = w.sit.map(x => x.p).filter(p => !p.ir && !prot.has(p.id)).slice(0, 5);
    const weekPts = p => (w.dw.games[p.t] || []).filter(d => d >= w.from).reduce((t, d) => {
      const dt = w.dw.dates[d];
      return t + effAvg(p, K, dt) * (p.p === "G" ? gStart(p, dt).v : p.prob) * avail(p, dt);
    }, 0);
    const pool = s.players.filter(p => p.ft === "fa" && p.prob > 0 && (p.proj !== false || p.gp > 0) && !goalieOut(p)).map(p => ({
      p,
      v: weekPts(p)
    })).filter(x => x.v > 0).sort((a, b) => b.v - a.v).slice(0, 25).map(x => x.p);
    const base = weekProj(mine, w.dw, K, w.from).total;
    let best = null;
    drops.forEach(d => pool.forEach(f => {
      if (d.p !== f.p && cnt[d.p] - 1 < mins[d.p]) return;
      const g = weekProj(timedMove(mine, s.me, [{
        add: f,
        drop: d
      }]), w.dw, K, w.from).total - base;
      if (!best || g > best.g) best = {
        d,
        f,
        g
      };
    }));
    return best && best.g >= 1 ? best : null;
  }, [openW, waste]);
  const playDays = (p, a) => (wkP.games[p.t] || []).filter(d => d >= a && (p.p !== "G" || gStart(p, dates[d]).v >= 0.5)).map(d => wkP.days[d].split(",")[0]).join(", ");
  const steps = res ? res.p.steps : [];
  const lastWin = res && res.after.length ? res.after[res.after.length - 1] : null;
  const wkName = w => {
    const ds = w.dw.dates || [];
    return ds.length ? mdL(ds[0]) + " to " + mdL(ds[ds.length - 1]) : w.dw.label;
  };
  return /*#__PURE__*/React.createElement("div", {
    className: "space-y-3"
  }, /*#__PURE__*/React.createElement("div", {
    className: "text-sm"
  }, /*#__PURE__*/React.createElement("span", {
    className: "font-semibold"
  }, plan ? "No moves left this week." : left === 0 ? "No moves left this week." : left + " move" + (left === 1 ? "" : "s") + " left this week."), plan ? /*#__PURE__*/React.createElement("span", {
    className: "text-slate-500"
  }, " Planning ", wkP.label || "next week", " with ", left === 3 ? "all 3 moves" : left + " move" + (left === 1 ? "" : "s"), ".") : null), /*#__PURE__*/React.createElement("div", {
    className: "gx-pn"
  }, /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      alignItems: "baseline"
    }
  }, /*#__PURE__*/React.createElement("span", {
    className: "gx-tag"
  }, "Your plan"), steps.length ? /*#__PURE__*/React.createElement("span", {
    className: "text-sm",
    style: {
      marginLeft: "auto"
    }
  }, /*#__PURE__*/React.createElement("span", {
    className: "font-semibold",
    style: {
      color: "var(--good)"
    }
  }, "+" + f1(res.p.gain) + " points"), res.b != null && lastWin != null ? /*#__PURE__*/React.createElement("span", {
    className: "text-slate-500"
  }, " \u00b7 win chance " + wpTxt(res.b) + " to " + wpTxt(lastWin)) : null) : null), busy ? /*#__PURE__*/React.createElement("div", {
    className: "text-sm text-slate-500",
    style: {
      padding: "12px 0 2px"
    }
  }, "Working it out...") : steps.length ? steps.map((st, i) => {
    const a = i ? res.after[i - 1] : res.b,
      b = res.after[i],
      dy = playDays(st.add, st.day);
    return /*#__PURE__*/React.createElement("div", {
      key: i,
      className: "gx-ps",
      style: i ? null : {
        marginTop: 6
      }
    }, /*#__PURE__*/React.createElement("span", {
      className: "gx-dayc"
    }, (wkP.days[st.day] || "").split(",")[0]), /*#__PURE__*/React.createElement("div", {
      className: "min-w-0"
    }, /*#__PURE__*/React.createElement("div", {
      className: "truncate"
    }, /*#__PURE__*/React.createElement(PN, {
      p: st.add,
      className: ""
    }), " in, ", /*#__PURE__*/React.createElement(PN, {
      p: st.drop,
      className: ""
    }), " out"), /*#__PURE__*/React.createElement("div", {
      className: "text-xs text-slate-500 truncate"
    }, (st.add.p === "G" ? "Likely starts " : "Plays ") + (dy || "\u2013"), st.add.wv ? " \u00b7 on waivers" : "", " \u00b7 ", /*#__PURE__*/React.createElement("button", {
      type: "button",
      className: "text-blue-600",
      onClick: () => window.__QA && window.__QA.espn(st.add)
    }, "Add on ESPN"))), /*#__PURE__*/React.createElement("span", {
      className: "n font-semibold",
      style: {
        color: "var(--good)"
      }
    }, "+" + f1(st.gain)), /*#__PURE__*/React.createElement("span", {
      className: "n text-slate-500"
    }, a != null && b != null ? wpTxt(a).replace("%", "") + " \u2192 " + wpTxt(b) : ""));
  }) : /*#__PURE__*/React.createElement("div", {
    className: "text-sm text-slate-500",
    style: {
      padding: "12px 0 2px"
    }
  }, left === 0 ? "Nothing to plan until your moves reset." : "No move adds " + (s.minGain ?? 3) + " or more points. Save your moves."), !busy && steps.length ? /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500",
    style: {
      paddingTop: 10,
      borderTop: "1px solid var(--line)"
    }
  }, "Make each move before that day's first game. The plan updates itself as injuries and starting goalies change.") : null), /*#__PURE__*/React.createElement("div", {
    className: "gx-pn"
  }, /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      alignItems: "baseline"
    }
  }, /*#__PURE__*/React.createElement("span", {
    className: "gx-tag"
  }, "Games going to waste"), /*#__PURE__*/React.createElement("span", {
    className: "text-xs text-slate-500",
    style: {
      marginLeft: "auto"
    }
  }, "Next 4 weeks \u00b7 " + waste.g + " game" + (waste.g === 1 ? "" : "s") + (waste.g ? ", about " + Math.round(waste.pts) + " points" : ""))), /*#__PURE__*/React.createElement("div", {
    className: "gx-wk text-xs text-slate-500",
    style: {
      borderTop: 0,
      marginTop: 6,
      paddingBottom: 4
    }
  }, /*#__PURE__*/React.createElement("span", null), /*#__PURE__*/React.createElement("span", {
    className: "n"
  }, "Stuck on bench"), /*#__PURE__*/React.createElement("span", {
    className: "n"
  }, "Empty slots")), waste.weeks.map((w, i) => /*#__PURE__*/React.createElement("div", {
    key: i
  }, /*#__PURE__*/React.createElement("div", {
    className: "gx-wk",
    role: "button",
    style: {
      cursor: "pointer"
    },
    onClick: () => setOpenW(openW === i ? -1 : i)
  }, /*#__PURE__*/React.createElement("span", null, wkName(w)), /*#__PURE__*/React.createElement("span", {
    className: "n",
    style: {
      color: w.g ? "var(--bad)" : "var(--mute)"
    }
  }, w.g ? w.g + " game" + (w.g === 1 ? "" : "s") : "0"), /*#__PURE__*/React.createElement("span", {
    className: "n text-slate-500"
  }, w.empty)), openW === i ? /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500",
    style: {
      padding: "0 0 10px"
    }
  }, w.sit.length ? /*#__PURE__*/React.createElement("div", null, "Sitting: ", w.sit.map(x => x.p.n + " (" + x.days.join(", ") + ")").join("; ")) : /*#__PURE__*/React.createElement("div", null, "Nobody is stuck on your bench this week."), w.sit.length ? fix ? /*#__PURE__*/React.createElement("div", {
    style: {
      marginTop: 4,
      color: "var(--ink)"
    }
  }, "Swap that fixes it: ", /*#__PURE__*/React.createElement(PN, {
    p: fix.f,
    className: "font-semibold"
  }), " in, ", /*#__PURE__*/React.createElement(PN, {
    p: fix.d,
    className: "font-semibold"
  }), " out ", /*#__PURE__*/React.createElement("span", {
    style: {
      color: "var(--good)"
    }
  }, "+" + f1(fix.g))) : /*#__PURE__*/React.createElement("div", {
    style: {
      marginTop: 4
    }
  }, i === 0 && outOfMoves(s) ? "No moves left this week to fix it." : "No free agent helps more than keeping who you have.") : null) : null)), /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500",
    style: {
      paddingTop: 10,
      borderTop: "1px solid var(--line)"
    }
  }, waste.chronic.length ? "Most often stuck: " + waste.chronic.map(c => c.p.n + " (" + c.g + " games)").join(", ") + ". " : "", "Tap a week to see who sits and the swap that fixes it.")));
}

// ---------- round 43: Advice page, four plain lists (news_logos.py) ----------
function AdvicePage({
  s,
  setS,
  wk
}) {
  const K = s.blend;
  const [sim, setSim] = useState(null);
  const sP = useMemo(() => planS(s), [s]);
  const wkP = useMemo(() => sP !== s ? deriveWeek(sP.weeks[sP.wk], sP.autoDone) : wk, [sP, wk]);
  const M = useMemo(() => sim ? computeMoves(sP, {
    H: 1,
    pool: 40
  }) : null, [sP, !!sim]);
  const base = useMemo(() => sim ? planBase(s, sP) : null, [sP, !!sim]);
  const L = useMemo(() => {
    const mb = p => {
      const id = typeof p.id === "string" && p.id[0] === "e" ? p.id.slice(1) : null;
      return window.__MODEL && id ? (window.__MODEL.base || {})[id] : null;
    };
    const UP = {
      F1: "line 1",
      F2: "line 2",
      D1: "the top pair",
      D2: "the second pair"
    };
    const rise = p => {
      const g = sigOf(p),
        fr = formRatio(p, K),
        t = g.toi;
      if (g.lines && g.lines.chg === "up") return "Moved up to " + (UP[g.lines.grp] || "a bigger role");
      if (g.ppChg === "added") return "New on the top power play";
      if (t && t.d >= 90) return "More ice time: " + (t.d / 60).toFixed(1) + " more minutes a game";
      if (fr !== null && fr >= 1.25) return "Hot: " + f1(g.rec.ppg) + " a game over two weeks";
      if ((p.chg || 0) >= 5) return "Being picked up fast: +" + f1(p.chg) + "% of leagues";
      return "";
    };
    const under = p => {
      const m = mb(p),
        l = sigOf(p).luck;
      if (m != null && p.proj && p.avg > 0 && m - p.avg >= 1 && m / p.avg >= 1.15) return "Your model rates him " + f1(m - p.avg) + " above ESPN";
      if (l && l.t === "s" && l.d <= -2) return "Unlucky: " + l.g + " goal" + (l.g === 1 ? "" : "s") + " on " + l.sh + " shots";
      if (l && l.t === "g" && l.d <= -4) return "Unlucky: stopping fewer shots than he usually does";
      return "";
    };
    const sell = p => {
      const m = mb(p),
        l = sigOf(p).luck,
        fr = formRatio(p, K);
      if (m != null && p.proj && p.avg > 0 && p.avg - m >= 1 && m / p.avg <= 0.85) return "ESPN rates him higher than your model";
      if (l && l.t === "s" && l.d >= 2) return "Lucky: " + l.g + " goals on " + l.sh + " shots";
      if (l && l.t === "g" && l.d >= 4) return "Lucky: stopping more shots than he usually does";
      if (fr !== null && fr >= 1.3) return "Hot: " + f1(sigOf(p).rec.ppg) + " a game over two weeks";
      return "";
    };
    const watch = p => {
      const g = sigOf(p),
        fr = formRatio(p, K),
        t = g.toi;
      if (g.lines && g.lines.chg === "down") return "Moved down the lineup";
      if (g.ppChg === "removed") return "Off the top power play";
      if (t && t.d <= -90) return "Losing ice time: " + (Math.abs(t.d) / 60).toFixed(1) + " minutes less a game";
      if (fr !== null && fr <= 0.7) return "Cold: " + f1(g.rec.ppg) + " a game over two weeks";
      return "";
    };
    const pickL = (list, fn) => list.map(p => ({
      p,
      why: fn(p)
    })).filter(x => x.why).sort((a, b) => effAvg(b.p, K) - effAvg(a.p, K)).slice(0, 6);
    const fa = s.players.filter(p => p.ft === "fa" && p.prob > 0 && (p.proj !== false || p.gp > 0) && !goalieOut(p)),
      mine = s.players.filter(p => p.ft === s.me && !p.ir);
    return {
      rise: pickL(fa, rise),
      under: pickL(fa, under),
      sell: pickL(mine, sell),
      watch: pickL(mine, watch)
    };
  }, [s.players, K, window.__PMODE, (window.ESPN_DATA || {}).generated]);
  const open = p => {
    const dr = dropFor(s, p);
    setSim({
      add: p.id,
      drop: dr ? dr.id : ""
    });
  };
  const list = (title, rows, fa, bad, empty) => /*#__PURE__*/React.createElement(GxPanel, {
    title: title
  }, rows.length ? rows.map((x, i) => /*#__PURE__*/React.createElement("div", {
    key: x.p.id,
    className: "gx-row",
    role: fa ? "button" : undefined,
    style: {
      borderTop: i ? undefined : 0,
      cursor: fa ? "pointer" : "default"
    },
    onClick: fa ? () => open(x.p) : undefined
  }, /*#__PURE__*/React.createElement(GxFace, {
    p: x.p,
    size: 22
  }), /*#__PURE__*/React.createElement("div", {
    className: "min-w-0",
    style: {
      flex: 1
    }
  }, /*#__PURE__*/React.createElement("div", {
    className: "truncate"
  }, fa ? x.p.n : /*#__PURE__*/React.createElement(PN, {
    p: x.p,
    className: ""
  }), " ", /*#__PURE__*/React.createElement("span", {
    className: "text-xs text-slate-500"
  }, x.p.p)), /*#__PURE__*/React.createElement("div", {
    className: "text-xs truncate",
    style: {
      color: bad ? "var(--bad)" : "var(--mute)"
    }
  }, x.why)), /*#__PURE__*/React.createElement("span", {
    style: {
      fontVariantNumeric: "tabular-nums"
    }
  }, f1(effAvg(x.p, K))))) : /*#__PURE__*/React.createElement("div", {
    className: "text-sm text-slate-500"
  }, empty));
  return /*#__PURE__*/React.createElement("div", {
    className: "space-y-3"
  }, /*#__PURE__*/React.createElement("div", {
    className: "grid md:grid-cols-2 gap-3"
  }, list("Free agents on the rise", L.rise, true, false, "No free agent is clearly on the way up right now."), list("Better than they look", L.under, true, false, "Nobody stands out as underrated right now."), list("Your players to sell high", L.sell, false, false, "None of your players is at a peak right now."), list("Your players to watch", L.watch, false, true, "None of your players is slipping right now.")), /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500"
  }, "The number is expected points a game. Tap a free agent to try the swap."), sim && M ? /*#__PURE__*/React.createElement(GxSim107, {
    s: sP,
    setS: setS,
    wk: wkP,
    M: M,
    H: 1,
    hLabel: sP !== s ? "next week" : "rest of this week",
    init: sim,
    wBase: base,
    onClose: () => setSim(null)
  }) : null);
}

// ---------- round 44: League page and Setup page (news_logos.py) ----------
// playoff odds for every team: 2,000 simulated seasons from each team's strength and the real schedule
function leagueSim(s) {
  const ids = s.teams.map(t => t.id);
  if (ids.length < 2) return null;
  const T = leagueTable(s),
    str = {},
    K = s.blend,
    today = todayISO();
  T.rows.forEach(x => str[x.t.id] = x.strength);
  const end = Math.min(s.weeks.length, s.poStart ?? 24),
    w0 = {},
    pf = {},
    todo = [];
  ids.forEach(id => {
    w0[id] = 0;
    pf[id] = 0;
  });
  s.weeks.slice(0, end).forEach(w => {
    const len = (w.dates || []).length,
      pairs = (w.pairs || []).filter(p => p[0] && p[1] && w0[p[0]] != null && w0[p[1]] != null);
    if (!len || !pairs.length) return;
    if (effDone(w, s.autoDone) >= len) {
      pairs.forEach(([a, b]) => {
        const x = +gxAct120(w)[a] || 0,
          y = +gxAct120(w)[b] || 0;
        if (!x && !y) return;
        pf[a] += x;
        pf[b] += y;
        if (x > y) w0[a]++;else if (y > x) w0[b]++;else {
          w0[a] += 0.5;
          w0[b] += 0.5;
        }
      });
      return;
    }
    const live = w.dates[0] <= today ? deriveWeek(w, s.autoDone) : null;
    pairs.forEach(([a, b]) => {
      let p;
      if (live) {
        const R = id => weekLive(s.players.filter(q => q.ft === id), live, K, id),
          act = id => +gxAct120(live)[id] || 0;
        p = winProb(R(a), R(b), act(a), act(b));
      } else p = normCdf(((str[a] || 0) - (str[b] || 0)) * (len / 7) / (80 * Math.sqrt(len / 7)));
      pf[a] += (str[a] || 0) * (len / 7);
      pf[b] += (str[b] || 0) * (len / 7);
      todo.push([a, b, Math.max(0.02, Math.min(0.98, p))]);
    });
  });
  let seed = 20262027;
  const rnd = () => {
    seed = seed + 0x6d2b79f5 | 0;
    let t = Math.imul(seed ^ seed >>> 15, 1 | seed);
    t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
    return ((t ^ t >>> 14) >>> 0) / 4294967296;
  };
  const N = 2000,
    cut = Math.min(6, ids.length - 1),
    inN = {};
  ids.forEach(id => inN[id] = 0);
  for (let k = 0; k < N; k++) {
    const w = Object.assign({}, w0);
    for (let j = 0; j < todo.length; j++) {
      const m = todo[j];
      if (rnd() < m[2]) w[m[0]]++;else w[m[1]]++;
    }
    const order = ids.slice().sort((a, b) => w[b] - w[a] || pf[b] - pf[a]);
    for (let r = 0; r < cut; r++) inN[order[r]]++;
  }
  const out = {};
  ids.forEach(id => out[id] = inN[id] / N);
  return {
    odds: out,
    cut
  };
}
function LeaguePage({
  s,
  wk,
  go
}) {
  const K = s.blend,
    gen = (window.ESPN_DATA || {}).generated;
  const [by, setBy] = useState("st");
  const [sim, setSim] = useState(null);
  const T = leagueTable(s);
  useEffect(() => {
    const id = setTimeout(() => {
      try {
        setSim(leagueSim(s));
      } catch (e) {
        setSim(null);
      }
    }, 500);
    return () => clearTimeout(id);
  }, [s.players, s.weeks, s.wk, s.blend, window.__PMODE]);
  const wins = x => x.rec.w + x.rec.t / 2;
  const stand = [...T.rows].sort((a, b) => wins(b) - wins(a) || b.rec.pf - a.rec.pf || b.strength - a.strength);
  // change 079: Points and Playoffs headings sort too
  const list = by === "st" ? stand : by === "pf" ? [...T.rows].sort((a, b) => b.rec.pf - a.rec.pf || b.strength - a.strength) : by === "po" ? [...T.rows].sort((a, b) => (sim && sim.odds[b.t.id] || 0) - (sim && sim.odds[a.t.id] || 0) || b.strength - a.strength) : T.rows;
  const cut = sim ? sim.cut : 6;
  const myOpp = oppOf(wk, s.me);
  const all = [[s.me, myOpp || s.opp]].concat((wk.pairs || []).filter(p => p[0] && p[1] && p[0] !== s.me && p[1] !== s.me)).filter(p => p[0] && p[1]);
  const games = useMemo(() => all.map(([a, b]) => {
    const R = id => weekLive(s.players.filter(p => p.ft === id), wk, K, id),
      act = id => +gxAct120(wk)[id] || 0;
    return {
      a,
      b,
      sa: act(a),
      sb: act(b),
      p: winProb(R(a), R(b), act(a), act(b))
    };
  }), [s.players, wk, K, gen, s.opp, window.__LIVEV120]);
  return /*#__PURE__*/React.createElement("div", {
    className: "space-y-3"
  }, /*#__PURE__*/React.createElement("div", {
    className: "gx-pn"
  }, /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      alignItems: "center",
      gap: 8,
      marginBottom: 8
    }
  }, /*#__PURE__*/React.createElement("span", {
    className: "gx-tag"
  }, "League table"), /*#__PURE__*/React.createElement("span", {
    className: "gx-seg",
    style: {
      marginLeft: "auto"
    }
  }, /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: by === "st" ? "on" : "",
    onClick: () => setBy("st")
  }, "Standings"), /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: by === "pw" ? "on" : "",
    onClick: () => setBy("pw")
  }, "Strength"))), /*#__PURE__*/React.createElement("div", {
    className: "gx-lt text-xs text-slate-500",
    style: {
      borderTop: 0,
      paddingTop: 0
    }
  }, /*#__PURE__*/React.createElement("span", null), /*#__PURE__*/React.createElement("span", null), /*#__PURE__*/React.createElement(GxSH, {
    k: "st",
    cur: by,
    set: setBy,
    def: "st"
  }, "Record"), /*#__PURE__*/React.createElement(GxSH, {
    k: "pf",
    cur: by,
    set: setBy,
    def: "st",
    cls: "m-hide"
  }, "Points"), /*#__PURE__*/React.createElement(GxSH, {
    k: "pw",
    cur: by,
    set: setBy,
    def: "st",
    cls: "m-hide"
  }, "Strength"), /*#__PURE__*/React.createElement(GxSH, {
    k: "po",
    cur: by,
    set: setBy,
    def: "st"
  }, "Playoffs")), list.map((x, i) => {
    const me = x.t.id === s.me,
      od = sim ? sim.odds[x.t.id] : null;
    return /*#__PURE__*/React.createElement("div", {
      key: x.t.id,
      className: "gx-lt" + (by === "st" && i === cut ? " cut" : "") + (me ? " font-semibold" : "")
    }, /*#__PURE__*/React.createElement("span", {
      className: "text-slate-500",
      style: {
        fontWeight: 400
      }
    }, i + 1), /*#__PURE__*/React.createElement("span", {
      className: "truncate"
    }, /*#__PURE__*/React.createElement(TL, {
      s: s,
      id: x.t.id
    })), /*#__PURE__*/React.createElement("span", {
      className: "n"
    }, x.rec.n ? x.rec.w + "-" + x.rec.l + (x.rec.t ? "-" + x.rec.t : "") : "\u2013"), /*#__PURE__*/React.createElement("span", {
      className: "n m-hide"
    }, x.rec.n ? Math.round(x.rec.pf) : "\u2013"), /*#__PURE__*/React.createElement("span", {
      className: "n m-hide"
    }, Math.round(x.strength)), /*#__PURE__*/React.createElement("span", {
      className: "n"
    }, od == null ? "\u2026" : /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("span", {
      style: {
        display: "inline-block",
        width: 38,
        height: 4,
        background: "var(--track)",
        verticalAlign: "middle",
        marginRight: 6
      }
    }, /*#__PURE__*/React.createElement("span", {
      style: {
        display: "block",
        height: 4,
        width: Math.round(od * 100) + "%",
        background: od >= 0.5 ? "var(--good)" : "var(--bad)"
      }
    })), wpTxt(od))));
  }), /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500",
    style: {
      paddingTop: 10,
      borderTop: "1px solid var(--line)"
    }
  }, by === "st" ? "The dashed line is the playoff cut. " : "", "Strength is projected points a week from here on. Tap a team for its roster and how it matches up with yours.")), /*#__PURE__*/React.createElement("div", {
    className: "gx-pn"
  }, /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("div", {
    className: "gx-tag",
    style: {
      marginBottom: 4
    }
  }, "This week"), games.length ? games.map((g, i) => {
    const la = g.p >= 0.5;
    return /*#__PURE__*/React.createElement("div", {
      key: g.a + "-" + g.b,
      className: "gx-lm",
      role: "button",
      style: i ? null : {
        borderTop: 0
      },
      onClick: () => {
        window.__MATCH_SEL = i;
        go("matchup");
      }
    }, /*#__PURE__*/React.createElement("span", {
      className: "truncate" + (g.a === s.me ? " font-semibold" : "")
    }, teamName(s, g.a)), /*#__PURE__*/React.createElement("span", {
      className: "n m-hide"
    }, f1(g.sa)), /*#__PURE__*/React.createElement("span", {
      className: "n",
      style: {
        color: la ? "var(--good)" : "var(--bad)"
      }
    }, wpTxt(g.p)), /*#__PURE__*/React.createElement("span", {
      style: {
        display: "flex",
        height: 4,
        gap: 2
      }
    }, /*#__PURE__*/React.createElement("i", {
      style: {
        display: "block",
        width: Math.round(g.p * 100) + "%",
        background: la ? "var(--good)" : "var(--bad)"
      }
    }), /*#__PURE__*/React.createElement("i", {
      style: {
        display: "block",
        flex: 1,
        background: la ? "var(--bad)" : "var(--good)"
      }
    })), /*#__PURE__*/React.createElement("span", {
      style: {
        color: la ? "var(--bad)" : "var(--good)"
      }
    }, wpTxt(1 - g.p)), /*#__PURE__*/React.createElement("span", {
      className: "m-hide"
    }, f1(g.sb)), /*#__PURE__*/React.createElement("span", {
      className: "truncate text-right"
    }, teamName(s, g.b)));
  }) : /*#__PURE__*/React.createElement("div", {
    className: "text-sm text-slate-500"
  }, "No matchups loaded for this week."), games.length ? /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500",
    style: {
      paddingTop: 8,
      borderTop: "1px solid var(--line)"
    }
  }, "Tap a matchup to open it on the Matchup page.") : null), /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: "gx-lk",
    onClick: () => go("league", "playoffs")
  }, /*#__PURE__*/React.createElement("span", null, "Playoff schedule"), /*#__PURE__*/React.createElement("span", {
    className: "text-sm text-slate-500",
    style: {
      marginLeft: 8
    }
  }, "who has the most games in the playoff weeks"), /*#__PURE__*/React.createElement("span", {
    className: "sec-chev shut",
    style: {
      margin: "0 4px 0 auto"
    }
  })));
}
function SetupPage({
  s,
  setS,
  go,
  sub
}) {
  // setup v67: a short list with summaries, each row opens its own page (news_logos.py)
  // older done markers kept: ["best", "Best" + (s.pbest | <GxAlertPrefs /> | href="ai-history.html"
  const E = window.ESPN_DATA,
    Sg = E && E.signals;
  const [msg, setMsg] = useState("");
  const [al, setAl] = useState(null);
  useEffect(() => {
    let dead = false;
    gxAlLoad().then(x => {
      if (!dead) setAl(x);
    });
    return () => {
      dead = true;
    };
  }, []);
  const K = s.blend,
    theme = window.__themePref ? window.__themePref() : "auto";
  const seg = (items, value, onPick) => /*#__PURE__*/React.createElement("span", {
    className: "gx-seg"
  }, items.map(([k, l, off]) => /*#__PURE__*/React.createElement("button", {
    key: k,
    type: "button",
    disabled: !!off,
    className: value === k ? "on" : "",
    onClick: () => onPick(k)
  }, l)));
  const num = (k, v, fb) => setS(x => ({
    ...x,
    [k]: isNaN(parseFloat(v)) ? fb : parseFloat(v)
  }));
  const roster = s.players.filter(p => p.ft === s.me && !p.ir).sort((a, b) => effAvg(b, K) - effAvg(a, K));
  const top = s.protectTop ?? 8,
    autoIds = new Set(roster.slice(0, top).map(p => p.id));
  const kept = roster.filter(p => p.keep && !autoIds.has(p.id)),
    addable = roster.filter(p => !p.keep && !autoIds.has(p.id));
  const keep = (id, v) => setS(x => ({
    ...x,
    players: x.players.map(p => p.id === id ? {
      ...p,
      keep: v
    } : p)
  }));
  const src = [["ESPN league", !!E], ["GM model", !!(E && E.model)], ["betting lines", !!(E && E.model && E.model.odds && Object.keys(E.model.odds).length)], ["recent form", !!(Sg && Sg.recent)], ["power-play units", !!(Sg && Sg.pp1)], ["news", !!(Sg && Sg.news)], ["injuries", !!(Sg && Sg.injuries)], ["starting goalies", !!(E && E.goalies)]];
  const bad = src.filter(x => !x[1]).map(x => x[0]);
  const genAt = E && toDate(E.generated),
    old = genAt ? (Date.now() - genAt.getTime()) / 36e5 > 2 : true;
  const download = () => {
    const blob = new Blob([JSON.stringify(s)], {
      type: "application/json"
    });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = "fantasy-gm-backup-" + todayISO() + ".json";
    a.click();
    setMsg("Backup downloaded.");
  };
  const upload = e => {
    const f = e.target.files && e.target.files[0];
    if (!f) return;
    const r = new FileReader();
    r.onload = () => {
      try {
        const v = JSON.parse(r.result);
        if (v.players && v.weeks) {
          setS(migrate(v));
          setMsg("Backup restored.");
        } else setMsg("That file isn't a backup.");
      } catch (ex) {
        setMsg("Couldn't read that file.");
      }
    };
    r.readAsText(f);
  };
  const newsN = s.players.filter(p => p.ft === s.me && newsOf(p).length).length;
  const box = inp + " text-sm";
  const PM = {
    espn: "ESPN",
    blend: "Blend",
    model: "GM model",
    ai: "AI"
  };
  const projTxt = s.pbest ? "Best projection (" + (PM[window.__PMODE] || "ESPN") + ")" : (PM[window.__PMODE] || "ESPN") + " projections";
  const themeTxt = theme === "auto" ? "Automatic theme" : theme === "light" ? "Light theme" : "Dark theme";
  const ast = al ? gxAlertState(al.p) : null,
    alog = al ? gxAlertLog(al.b) : [];
  const lastSent = alog.find(m => !m.held && !m.wait);
  const alertTxt = !ast ? "Checking..." : ast.filter(x => x.on).length + " on \u00b7 " + ast.filter(x => !x.on).length + " off" + (lastSent ? " \u00b7 last sent " + gxWhen(lastSent.at) : "");
  const outN = s.players.filter(p => p.ft === s.me && (p.ir || p.status && p.status !== "ACTIVE")).length;
  const syncTxt = E ? "Synced " + (genAt ? genAt.toLocaleTimeString([], {
    hour: "numeric",
    minute: "2-digit"
  }) : "") : "No data file found";
  const refresh = () => {
    window.location.href = window.location.pathname + "?v=" + Date.now();
  };
  const btn = "border border-slate-300 rounded-lg px-3 py-1 text-sm";
  const row = (k, title, sumTxt, fn, i) => {
    /* gx072-row */
    const ext = k === "ailab" ? "ai-dashboard.html" : k === "history" ? "ai-history.html" : "";
    const href = ext || (k === "news" ? "#news" : gxHash("setup", k));
    return /*#__PURE__*/React.createElement("a", {
      key: k,
      href: href,
      target: ext ? "_blank" : undefined,
      rel: ext ? "noopener" : undefined,
      className: "gx-lk",
      style: i ? null : {
        borderTop: 0
      },
      onClick: e => {
        if (ext || gxNewTab(e)) return;
        e.preventDefault();
        fn(e);
      }
    }, /*#__PURE__*/React.createElement("span", {
      className: "min-w-0",
      style: {
        flex: 1
      }
    }, /*#__PURE__*/React.createElement("span", {
      className: "block"
    }, title), sumTxt ? /*#__PURE__*/React.createElement("span", {
      className: "block text-xs text-slate-500 truncate"
    }, sumTxt) : null), /*#__PURE__*/React.createElement("span", {
      className: "sec-chev shut",
      style: {
        margin: "0 4px 0 12px"
      }
    }));
  };
  const page = (title, kids) => /*#__PURE__*/React.createElement("div", {
    className: "space-y-3"
  }, /*#__PURE__*/React.createElement("div", {
    className: "font-semibold",
    style: {
      fontSize: 17
    }
  }, title), /*#__PURE__*/React.createElement("div", {
    className: "gx-pn"
  }, kids));
  if (sub === "display") return page("Display", /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("div", {
    className: "gx-sr",
    style: {
      borderTop: 0
    }
  }, /*#__PURE__*/React.createElement("span", null, "Theme"), seg([["auto", "Automatic"], ["light", "Light"], ["dark", "Dark"]], theme, k => window.__setTheme && window.__setTheme(k))), /*#__PURE__*/React.createElement("div", {
    className: "gx-sr"
  }, /*#__PURE__*/React.createElement("span", null, "Projections"), seg([["best", "Best" + (s.pbest ? " (" + ({
    espn: "ESPN",
    blend: "Blend",
    model: "GM model",
    ai: "AI"
  }[window.__PMODE] || "") + ")" : ""), !window.__MODEL], ["espn", "ESPN"], ["blend", "Blend", !window.__MODEL], ["model", "GM model", !window.__MODEL], ["ai", "AI", !window.__MODEL || !window.__AI]], s.pbest ? "best" : window.__PMODE, k => k === "best" ? setS({
    ...s,
    pbest: true
  }) : setS({
    ...s,
    pbest: false,
    pmode: k,
    players: [...s.players]
  }))), /*#__PURE__*/React.createElement("div", {
    className: "gx-sr"
  }, /*#__PURE__*/React.createElement("span", null, "Favourite team (Lines)"), /*#__PURE__*/React.createElement(GxFavSel112, null)), /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500",
    style: {
      paddingTop: 8
    }
  }, "Best switches each day to whichever projection has been most accurate in the AI Lab.")));
  if (sub === "rules") return page("Pickup rules", /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("div", {
    className: "gx-sr",
    style: {
      borderTop: 0
    }
  }, /*#__PURE__*/React.createElement("span", null, "A move must add at least"), /*#__PURE__*/React.createElement("span", null, /*#__PURE__*/React.createElement("input", {
    type: "number",
    step: "0.5",
    className: box + " w-20",
    value: s.minGain ?? 3,
    onChange: e => num("minGain", e.target.value, 3)
  }), " points")), /*#__PURE__*/React.createElement("div", {
    className: "gx-sr"
  }, /*#__PURE__*/React.createElement("span", null, "Never suggest dropping my top"), /*#__PURE__*/React.createElement("span", null, /*#__PURE__*/React.createElement("select", {
    className: box,
    value: top,
    onChange: e => setS(x => ({
      ...x,
      protectTop: +e.target.value
    }))
  }, [...Array(13)].map((_, n) => /*#__PURE__*/React.createElement("option", {
    key: n,
    value: n
  }, n))), " players")), /*#__PURE__*/React.createElement("div", {
    className: "gx-sr"
  }, /*#__PURE__*/React.createElement("span", null, "Also protect"), /*#__PURE__*/React.createElement("span", {
    className: "flex flex-wrap gap-2 items-center justify-end"
  }, kept.map(p => /*#__PURE__*/React.createElement("span", {
    key: p.id,
    className: "inline-flex items-center gap-1 px-2 py-1 rounded-full border border-slate-300 text-xs"
  }, p.n, /*#__PURE__*/React.createElement("button", {
    type: "button",
    "aria-label": "Stop protecting " + p.n,
    className: "text-slate-500",
    style: {
      fontSize: 14,
      lineHeight: 1
    },
    onClick: () => keep(p.id, false)
  }, "\u00d7"))), addable.length ? /*#__PURE__*/React.createElement("select", {
    className: box,
    value: "",
    onChange: e => {
      if (e.target.value) keep(e.target.value, true);
    }
  }, /*#__PURE__*/React.createElement("option", {
    value: ""
  }, "+ add a player"), addable.map(p => /*#__PURE__*/React.createElement("option", {
    key: p.id,
    value: p.id
  }, p.n + " (" + p.p + ")"))) : null)), /*#__PURE__*/React.createElement("div", {
    className: "gx-sr"
  }, /*#__PURE__*/React.createElement("span", null, "Always keep at least"), /*#__PURE__*/React.createElement("span", {
    className: "flex gap-2 items-center"
  }, /*#__PURE__*/React.createElement("input", {
    type: "number",
    className: box + " w-14",
    value: s.minF ?? 10,
    onChange: e => num("minF", e.target.value, 10)
  }), " F", /*#__PURE__*/React.createElement("input", {
    type: "number",
    className: box + " w-14",
    value: s.minD ?? 5,
    onChange: e => num("minD", e.target.value, 5)
  }), " D", /*#__PURE__*/React.createElement("input", {
    type: "number",
    className: box + " w-14",
    value: s.minGo ?? 2,
    onChange: e => num("minGo", e.target.value, 2)
  }), " G"))));
  if (sub === "players") return page("Players and injuries", /*#__PURE__*/React.createElement(React.Fragment, null, row("inj", "Injury return dates", outN ? outN + " of your players hurt or on IR" : "Everyone on your team is healthy", () => go("setup", "inj"), 0), row("bulk", "Edit players", "Projections, play %, fantasy team", () => go("setup", "bulk"), 1)));
  if (sub === "league") return page("League info", /*#__PURE__*/React.createElement(React.Fragment, null, row("news", "News", newsN ? newsN + " of your players in the news" : "Nothing new on your players", () => go("news"), 0), row("odds", "Betting lines", "Win chances and expected goals for each game", () => go("setup", "odds"), 1), row("sched", "Schedule", "Games per NHL team this week", () => go("setup", "sched"), 2)));
  if (sub === "data") return page("Data and backup", /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("div", {
    className: "gx-sr",
    style: {
      borderTop: 0
    }
  }, /*#__PURE__*/React.createElement("span", null, syncTxt), /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: btn,
    onClick: refresh
  }, "Refresh")), bad.length ? bad.map(l => /*#__PURE__*/React.createElement("div", {
    key: l,
    className: "gx-sr"
  }, /*#__PURE__*/React.createElement("span", null, l.charAt(0).toUpperCase() + l.slice(1)), /*#__PURE__*/React.createElement("span", {
    className: "text-sm",
    style: {
      color: "var(--bad)"
    }
  }, "Not working"))) : /*#__PURE__*/React.createElement("div", {
    className: "gx-sr"
  }, /*#__PURE__*/React.createElement("span", null, "All " + src.length + " data sources"), /*#__PURE__*/React.createElement("span", {
    className: "text-sm",
    style: {
      color: "var(--good)"
    }
  }, "Working")), /*#__PURE__*/React.createElement("div", {
    className: "gx-sr"
  }, /*#__PURE__*/React.createElement("span", null, "Your settings on this device"), /*#__PURE__*/React.createElement("span", {
    className: "flex gap-2 items-center"
  }, /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: btn,
    onClick: download
  }, "Download backup"), /*#__PURE__*/React.createElement("label", {
    className: btn + " cursor-pointer"
  }, "Restore", /*#__PURE__*/React.createElement("input", {
    type: "file",
    accept: ".json,application/json",
    className: "hidden",
    onChange: upload
  })))), msg ? /*#__PURE__*/React.createElement("div", {
    className: "text-xs",
    style: {
      color: "var(--good)",
      paddingTop: 6
    }
  }, msg) : null, /*#__PURE__*/React.createElement(GxSyncRow, null), /*#__PURE__*/React.createElement("div", {
    className: "gx-sr"
  }, /*#__PURE__*/React.createElement("span", null, "Week on screen"), /*#__PURE__*/React.createElement("select", {
    className: box,
    value: s.wk,
    onChange: e => setS({
      ...s,
      wk: +e.target.value
    })
  }, s.weeks.map((w, i) => /*#__PURE__*/React.createElement("option", {
    key: i,
    value: i
  }, w.label)))), row("adv", "Advanced settings", "Team names, projection weight, reset", () => go("setup", "adv"), 1)));
  return /*#__PURE__*/React.createElement("div", {
    className: "space-y-3"
  }, /*#__PURE__*/React.createElement("div", {
    className: "gx-pn",
    style: {
      display: "flex",
      alignItems: "center",
      gap: 10
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      width: 8,
      height: 8,
      borderRadius: 99,
      flexShrink: 0,
      background: !E ? "var(--faint)" : old || bad.length ? "var(--bad)" : "var(--good)"
    }
  }), /*#__PURE__*/React.createElement("span", {
    className: "text-sm min-w-0"
  }, syncTxt + " \u00b7 " + (!E ? "check GitHub Actions" : bad.length ? bad.length + " data source" + (bad.length === 1 ? "" : "s") + " not working" : old ? "data is over 2 hours old" : "everything working")), /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: btn,
    style: {
      marginLeft: "auto"
    },
    onClick: refresh
  }, "Refresh")), /*#__PURE__*/React.createElement("div", {
    className: "gx-pn",
    style: {
      paddingTop: 2,
      paddingBottom: 2
    }
  }, row("display", "Display", themeTxt + " \u00b7 " + projTxt, () => go("setup", "display"), 0), row("rules", "Pickup rules", "Moves must add " + (s.minGain ?? 3) + "+ points \u00b7 top " + top + " protected" + (kept.length ? " plus " + kept.length + " more" : ""), () => go("setup", "rules"), 1), row("alerts", "Phone alerts", alertTxt, () => go("setup", "alerts"), 2), /*#__PURE__*/React.createElement(GxAutoRow, {
    row: row,
    go: go
  }), row("players", "Players and injuries", "Injury return dates \u00b7 edit players", () => go("setup", "players"), 3), row("league", "League info", "News \u00b7 betting lines \u00b7 NHL schedule", () => go("setup", "league"), 4), row("data", "Data and backup", (bad.length ? "Not working: " + bad.join(", ") : "All " + src.length + " data sources working") + " \u00b7 backup \u00b7 advanced", () => go("setup", "data"), 5), row("ailab", "AI Lab", "How each projection is doing", () => window.open("ai-dashboard.html", "_blank"), 6), row("history", "Prediction history", "Every projection and what happened", () => window.open("ai-history.html", "_blank"), 7)));
}

// ---------- round 45: tappable rows work from the keyboard too (news_logos.py) ----------
(function gxA11y() {
  if (window.__gxA11y) return;
  window.__gxA11y = 1;
  const fix = () => document.querySelectorAll('[role="button"]:not([tabindex])').forEach(el => el.setAttribute("tabindex", "0"));
  let q = 0;
  try {
    new MutationObserver(() => {
      if (q) return;
      q = requestAnimationFrame(() => {
        q = 0;
        fix();
      });
    }).observe(document.documentElement, {
      childList: true,
      subtree: true
    });
  } catch (e) {}
  document.addEventListener("keydown", e => {
    const el = document.activeElement;
    if (e.defaultPrevented || !(e.key === "Enter" || e.key === " ")) return;
    if (el && el.getAttribute && el.getAttribute("role") === "button" && el.tagName !== "BUTTON") {
      e.preventDefault();
      el.click();
    }
  });
})();

// ---------- round 46: every matchup's score in a strip above the Matchup page (news_logos.py) ----------
function MatchStrip({
  s,
  wk
}) {
  const [cur, setCur] = useState(window.__matchSel || 0);
  useEffect(() => {
    const h = () => setCur(window.__matchSel || 0);
    window.addEventListener("gm-match", h);
    return () => window.removeEventListener("gm-match", h);
  }, []);
  const myOpp = oppOf(wk, s.me);
  const all = [[s.me, myOpp || s.opp]].concat((wk.pairs || []).filter(p => p[0] && p[1] && p[0] !== s.me && p[1] !== s.me)).filter(p => p[0] && p[1]);
  if (all.length < 2) return null;
  const sc = id => +gxAct120(wk)[id] || 0;
  const nm = id => {
    const w = (teamName(s, id) || "").split(" ")[0];
    return w.length > 10 ? w.slice(0, 9) + "\u2026" : w;
  };
  return /*#__PURE__*/React.createElement("div", {
    className: "gx-ms",
    role: "tablist",
    "aria-label": "Matchups this week"
  }, all.map(([a, b], i) => {
    const x = sc(a),
      y = sc(b);
    return /*#__PURE__*/React.createElement("button", {
      key: a + "-" + b,
      type: "button",
      role: "tab",
      "aria-selected": i === cur,
      className: i === cur ? "on" : "",
      onClick: e => {
        if (window.__setMatch) window.__setMatch(i);
        e.currentTarget.scrollIntoView({
          behavior: "smooth",
          inline: "center",
          block: "nearest"
        });
      }
    }, /*#__PURE__*/React.createElement(GxFtPic114, {
      id: a,
      size: 18
    }), nm(a), " ", x >= y ? /*#__PURE__*/React.createElement("b", null, f1(x)) : f1(x), " ", /*#__PURE__*/React.createElement("span", {
      style: {
        opacity: 0.6
      }
    }, "vs"), " ", y > x ? /*#__PURE__*/React.createElement("b", null, f1(y)) : f1(y), " ", nm(b), /*#__PURE__*/React.createElement(GxFtPic114, {
      id: b,
      size: 18
    }));
  }));
}

// ---------- round 50: warning dots, search, bottom tabs, swipe days, home-screen icon (news_logos.py) ----------
function gxWarn(s) {
  const o = {
    myteam: false,
    matchup: false
  };
  try {
    const today = todayISO(),
      wk = deriveWeek(s.weeks[s.wk], s.autoDone),
      mine = s.players.filter(p => p.ft === s.me && !p.ir);
    const open = p => {
      const g = gStart(p, today),
        l = (g.l || "").toLowerCase();
      return g.v >= 0.5 && !(l.includes("confirmed") && !l.includes("un"));
    };
    o.myteam = false && mine.some(p => p.status && /OUT|INJURY_RESERVE|SUSPENSION/.test(p.status)) || mine.some(p => p.p === "G" && SCHED[p.t] && SCHED[p.t].has(today) && gState(p.t, today).s === "P" && open(p));
    const opp = oppOf(wk, s.me) || s.opp,
      a = +gxAct120(wk)[s.me] || 0,
      b = +gxAct120(wk)[opp] || 0,
      sign = String(a === b ? 0 : a > b ? 1 : -1);
    const key = "gm-lead-" + s.wk,
      seen = localStorage.getItem(key);
    window.__leadNow = [key, sign];
    if (seen == null) localStorage.setItem(key, sign);else o.matchup = sign !== "0" && seen !== sign;
  } catch (e) {}
  return o;
}
const GX_ICON = {
  today: /*#__PURE__*/React.createElement("path", {
    d: "M4 11l8-7 8 7v9H4z"
  }),
  matchup: /*#__PURE__*/React.createElement("path", {
    d: "M4 8h13l-3-3M20 16H7l3 3"
  }),
  myteam: /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("circle", {
    cx: "12",
    cy: "8",
    r: "3.5"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M5 20c0-4 3-6 7-6s7 2 7 6"
  })),
  league: /*#__PURE__*/React.createElement("path", {
    d: "M5 6h14M5 12h14M5 18h14"
  }),
  setup: /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("circle", {
    cx: "12",
    cy: "12",
    r: "3"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M12 3v3M12 18v3M3 12h3M18 12h3M5.6 5.6l2.1 2.1M16.3 16.3l2.1 2.1M5.6 18.4l2.1-2.1M16.3 7.7l2.1-2.1"
  })),
  search: /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("circle", {
    cx: "11",
    cy: "11",
    r: "6"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M16 16l4 4"
  }))
};
function GxExtras({
  s,
  tab,
  go
}) {
  const [open, setOpen] = useState(false);
  const [q, setQ] = useState("");
  const K = s.blend,
    W = gxWarn(s);
  useEffect(() => {
    const show = () => {
      setQ("");
      setOpen(true);
    };
    const key = e => {
      const el = document.activeElement,
        typing = el && /INPUT|TEXTAREA|SELECT/.test(el.tagName);
      if (e.key === "/" && !typing) {
        e.preventDefault();
        show();
      }
      if (e.key === "Escape") setOpen(false);
    };
    window.addEventListener("gm-search", show);
    document.addEventListener("keydown", key);
    return () => {
      window.removeEventListener("gm-search", show);
      document.removeEventListener("keydown", key);
    };
  }, []);
  useEffect(() => {
    if (tab === "matchup" && window.__leadNow) {
      try {
        localStorage.setItem(window.__leadNow[0], window.__leadNow[1]);
      } catch (e) {}
    }
  }, [tab, s.lastSync]);
  useEffect(() => {
    // lift the floating Ask button above the bottom tabs on phones
    const fix = () => {
      if (window.innerWidth > 640) return;
      Array.prototype.forEach.call(document.querySelectorAll("button, a"), b => {
        if ((b.textContent || "").trim() === "Ask" && getComputedStyle(b).position === "fixed") b.style.bottom = "calc(74px + env(safe-area-inset-bottom))";
      });
    };
    const id = 0; /* gx102: no repeating scan */
    return () => clearInterval(id);
  }, []);
  const TABS = [["today", "Today", ["today"]], ["matchup", "Matchup", ["matchup"]], ["myteam", "Team", ["myteam", "moves", "lines"]], ["league", "League", ["league", "teams"]], ["setup", "Setup", ["setup", "news"]]];
  const qq = nrm(q);
  const teams = qq.length < 2 ? [] : s.teams.filter(t => nrm(t.name || "").includes(qq)).slice(0, 4);
  const players = qq.length < 2 ? [] : s.players.filter(p => nrm(p.n).includes(qq)).sort((a, b) => (nrm(b.n).indexOf(qq) === 0) - (nrm(a.n).indexOf(qq) === 0) || (b.own || 0) - (a.own || 0)).slice(0, 10);
  const svg = k => /*#__PURE__*/React.createElement("svg", {
    viewBox: "0 0 24 24",
    fill: "none",
    stroke: "currentColor",
    strokeWidth: "1.6",
    strokeLinecap: "round",
    strokeLinejoin: "round",
    "aria-hidden": "true"
  }, GX_ICON[k]);
  return /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("nav", {
    className: "gx-bb",
    "aria-label": "Main"
  }, TABS.map(([k, l, grp]) => /*#__PURE__*/React.createElement("button", {
    key: k,
    type: "button",
    className: grp.indexOf(tab) >= 0 ? "on" : "",
    onClick: () => go(k, k === "setup" ? "settings" : k === "league" ? "power" : undefined)
  }, svg(k), l, W[k] ? /*#__PURE__*/React.createElement("i", {
    className: "gx-wd"
  }) : null)), /*#__PURE__*/React.createElement("button", {
    type: "button",
    onClick: () => {
      setQ("");
      setOpen(true);
    }
  }, svg("search"), "Search")), open ? /*#__PURE__*/React.createElement("div", {
    className: "gx-so",
    role: "dialog",
    "aria-label": "Search",
    onClick: () => setOpen(false)
  }, /*#__PURE__*/React.createElement("div", {
    className: "gx-sbx",
    onClick: e => e.stopPropagation()
  }, /*#__PURE__*/React.createElement("input", {
    autoFocus: true,
    className: inp + " w-full",
    placeholder: "Search a player or a team",
    value: q,
    onChange: e => setQ(e.target.value)
  }), teams.map(t => /*#__PURE__*/React.createElement("div", {
    key: t.id,
    role: "button",
    className: "gx-row",
    style: {
      cursor: "pointer"
    },
    onClick: () => {
      setOpen(false);
      if (window.__NAV && window.__NAV.team) window.__NAV.team(t.id);
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      flex: 1
    }
  }, t.name), /*#__PURE__*/React.createElement("span", {
    className: "text-xs text-slate-500"
  }, "fantasy team"))), players.map(p => /*#__PURE__*/React.createElement("div", {
    key: p.id,
    role: "button",
    className: "gx-row",
    style: {
      cursor: "pointer"
    },
    onClick: () => {
      setOpen(false);
      if (window.__NAV) window.__NAV.player(p);
    }
  }, /*#__PURE__*/React.createElement(GxFace, {
    p: p,
    size: 22
  }), /*#__PURE__*/React.createElement("span", {
    className: "min-w-0 truncate",
    style: {
      flex: 1
    }
  }, p.n, " ", /*#__PURE__*/React.createElement("span", {
    className: "text-xs text-slate-500"
  }, p.p + " \u00b7 " + (p.ft === "fa" ? "free agent" : teamName(s, p.ft)))), /*#__PURE__*/React.createElement("span", {
    style: {
      fontVariantNumeric: "tabular-nums"
    }
  }, f1(effAvg(p, K))))), qq.length >= 2 && !teams.length && !players.length ? /*#__PURE__*/React.createElement("div", {
    className: "text-sm text-slate-500",
    style: {
      paddingTop: 10
    }
  }, "Nothing matches that.") : null, qq.length < 2 ? /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500",
    style: {
      paddingTop: 10
    }
  }, "Type at least two letters.") : null)) : null);
}
(function gxSwipeAndIcon() {
  if (window.__gx50) return;
  window.__gx50 = 1;
  let x0 = 0,
    y0 = 0,
    ok = false;
  document.addEventListener("touchstart", e => {
    const t = e.touches[0];
    x0 = t.clientX;
    y0 = t.clientY;
    ok = false; /* gx106: swipes are handled where they happen */
  }, {
    capture: true,
    passive: true
  });
  document.addEventListener("touchend", e => {
    if (!ok || window.innerWidth > 640) return;
    const t = e.changedTouches[0],
      dx = t.clientX - x0,
      dy = t.clientY - y0;
    if (Math.abs(dx) < 70 || Math.abs(dy) > 50) return;
    const cur = document.querySelector(".gx-day.on");
    if (!cur) return;
    e.stopPropagation();
    const nxt = dx < 0 ? cur.nextElementSibling : cur.previousElementSibling;
    if (nxt && nxt.classList.contains("gx-day")) nxt.click();
  }, {
    capture: true
  });
  try {
    const c = document.createElement("canvas");
    c.width = c.height = 180;
    const g = c.getContext("2d");
    g.fillStyle = "#0c0d0f";
    g.fillRect(0, 0, 180, 180);
    g.strokeStyle = "#ffffff";
    g.lineWidth = 8;
    g.beginPath();
    g.arc(90, 90, 58, 0, Math.PI * 2);
    g.stroke();
    g.fillStyle = "#ffffff";
    g.font = "600 72px Inter, -apple-system, sans-serif";
    g.textAlign = "center";
    g.textBaseline = "middle";
    g.fillText("K", 90, 95);
    const l = document.createElement("link");
    l.rel = "apple-touch-icon";
    l.href = c.toDataURL("image/png");
    document.head.appendChild(l);
  } catch (e) {}
})();

// ---------- round 51: watchlist and quick actions (news_logos.py) ----------
const gxWatch = {
  list: () => {
    try {
      return JSON.parse(localStorage.getItem("gm-watch") || "[]");
    } catch (e) {
      return [];
    }
  },
  has: id => gxWatch.list().indexOf(id) >= 0,
  toggle: id => {
    const l = gxWatch.list(),
      i = l.indexOf(id);
    if (i >= 0) l.splice(i, 1);else l.push(id);
    try {
      localStorage.setItem("gm-watch", JSON.stringify(l));
    } catch (e) {}
    window.dispatchEvent(new Event("gm-watch"));
  }
};
function GxWatchPanel({
  s
}) {
  const effAvg = gxPgAvg; /* gx088-w */
  const [, tick] = useState(0);
  useEffect(() => {
    const h = () => tick(x => x + 1);
    window.addEventListener("gm-watch", h);
    return () => window.removeEventListener("gm-watch", h);
  }, []);
  const K = s.blend,
    list = gxWatch.list().map(id => s.players.find(p => p.id === id)).filter(Boolean);
  if (!list.length) return null;
  const note = p => {
    if (p.ft !== "fa") return "now on " + teamName(s, p.ft);
    const g = sigOf(p),
      fr = formRatio(p, K);
    return g.lines && g.lines.chg === "up" ? "moved up a line" : g.ppChg === "added" ? "new on the top power play" : g.lines && g.lines.chg === "down" ? "moved down a line" : fr !== null && fr >= 1.25 ? "hot" : fr !== null && fr <= 0.7 ? "cold" : "";
  };
  return /*#__PURE__*/React.createElement(GxPanel, {
    title: "Watchlist"
  }, list.map((p, i) => /*#__PURE__*/React.createElement("div", {
    key: p.id,
    className: "gx-row",
    style: i ? null : {
      borderTop: 0
    }
  }, /*#__PURE__*/React.createElement(GxFace, {
    p: p,
    size: 22
  }), /*#__PURE__*/React.createElement("span", {
    className: "min-w-0 truncate",
    style: {
      flex: 1
    }
  }, /*#__PURE__*/React.createElement(PN, {
    p: p,
    className: ""
  }), " ", /*#__PURE__*/React.createElement("span", {
    className: "text-xs text-slate-500"
  }, p.p), note(p) ? /*#__PURE__*/React.createElement("span", {
    className: "text-xs text-slate-500",
    style: {
      marginLeft: 8
    }
  }, note(p)) : null), /*#__PURE__*/React.createElement("span", {
    style: {
      fontVariantNumeric: "tabular-nums"
    }
  }, f1(effAvg(p, K))), /*#__PURE__*/React.createElement("button", {
    type: "button",
    "aria-label": "Stop watching " + p.n,
    className: "text-slate-500",
    style: {
      padding: "0 4px",
      fontSize: 16
    },
    onClick: () => gxWatch.toggle(p.id)
  }, "\u00d7"))));
}
function GxQA({
  s,
  go
}) {
  useEffect(() => {
    const id = setTimeout(() => gxPrewarm102(s), 2500);
    return () => clearTimeout(id);
  }, [s]);
  const lid = (window.ESPN_DATA || {}).leagueId || 1363781006,
    num = x => String(x).replace(/\D/g, "");
  window.__QA = {
    mine: p => p.ft === s.me,
    fa: p => p.ft === "fa",
    tradeable: p => p.ft !== "fa",
    swap: p => {
      if (p.ft === "fa") window.__PICK_Q = p.n;else window.__PICK_POS = p.p;
      go("moves", "adddrop");
      setTimeout(() => window.dispatchEvent(new Event("gm-pick")), 50);
    },
    trade: p => {
      window.__TRADE_P = {
        id: p.id,
        ft: p.ft
      };
      go("moves", "trades");
      setTimeout(() => window.dispatchEvent(new Event("gm-trade")), 50);
    },
    lines: p => {
      if (window.__NAV && window.__NAV.lines) window.__NAV.lines(p.t);else go("lines");
    },
    espn: p => {
      try {
        if (navigator.clipboard) navigator.clipboard.writeText(p.n);
      } catch (e) {}
      window.open(p.ft === "fa" ? "https://fantasy.espn.com/hockey/players/add?leagueId=" + lid + "&teamId=" + num(s.me) : "https://fantasy.espn.com/hockey/team?leagueId=" + lid + "&teamId=" + num(p.ft), "_blank");
    },
    star: p => gxWatch.toggle(p.id),
    starred: p => gxWatch.has(p.id)
  };
  return null;
}

// ---------- round 52: keep the floating Ask button clear of the bottom tabs (news_logos.py) ----------
(function gxAsk() {
  if (window.__gxAsk) return;
  window.__gxAsk = 1;
  let box = null;
  const lift = el => {
    let n = el;
    while (n && n !== document.body && n !== document.documentElement) {
      if (getComputedStyle(n).position === "fixed") {
        n.style.setProperty("bottom", "calc(72px + env(safe-area-inset-bottom))", "important");
        return n;
      }
      n = n.parentElement;
    }
    return null;
  };
  const run = () => {
    const root = document.documentElement;
    if (window.innerWidth > 640) {
      root.classList.remove("gx-noask");
      return;
    }
    if (box && box.isConnected) {
      lift(box);
      root.classList.remove("gx-noask");
      return;
    }
    box = null;
    const all = document.querySelectorAll("button, a, div, span");
    for (let i = 0; i < all.length && !box; i++) {
      const el = all[i],
        leaf = el.tagName === "BUTTON" || el.tagName === "A" || !el.childElementCount;
      if (!leaf || el.closest && el.closest(".gx-bb, .gx-so")) continue;
      if ((el.textContent || "").trim() === "Ask") box = lift(el);
    }
    root.classList.toggle("gx-noask", !box);
  };
  /* gx102: the Ask button is placed by CSS now */
})();

// ---------- round 56: the Roster table for any fantasy team (news_logos.py) ----------
function GxRosterTable({
  s,
  wk,
  tid
}) {
  gxUseSort108(); /* gx109 */
  const K = s.blend,
    today = todayISO(),
    gen = (window.ESPN_DATA || {}).generated;
  const [sort, setSort] = useState("pg");
  const [hist, setHist] = useState({});
  const roster = s.players.filter(p => p.ft === tid);
  const pv = p => effAvg(p, K) * (p.p === "G" ? p.prob : 1);
  const dates = wk.dates || [];
  const nextW = s.weeks[s.wk + 1] ? deriveWeek(s.weeks[s.wk + 1], s.autoDone) : null;
  const mu = useMemo(() => {
    const P = pby(),
      o = {};
    dates.forEach(dt => {
      const AD = actDay(tid, dt);
      if (!AD) return;
      Object.entries(AD).forEach(([pid, v]) => {
        if (!v || v[0] == null || !ESLOT[v[1]]) return;
        const p = P["e" + pid];
        if (!p || !(SCHED[p.t] && SCHED[p.t].has(dt)) || gState(p.t, dt).s === "P" || p.p === "G" && !v[0]) return;
        o[p.id] = (o[p.id] || 0) + v[0];
      });
    });
    return o;
  }, [s.players, wk, gen, tid]);
  const total = Object.values(mu).reduce((a, v) => a + Math.max(0, v), 0);
  const rankOf = useMemo(() => {
    const o = {};
    ["F", "D", "G"].forEach(k => {
      s.players.filter(p => p.p === k && p.prob > 0 && (p.proj !== false || p.gp > 0)).map(p => [p.id, pv(p)]).sort((a, b) => b[1] - a[1]).forEach((x, i) => o[x[0]] = i + 1);
    });
    return o;
  }, [s.players, K, window.__PMODE]);
  const roles = useMemo(() => {
    const L = window.LINES_DATA,
      o = {};
    if (!L || !L.teams) return o;
    const key = x => nrm(x).replace(/[.'\u2019]/g, "").replace(/-/g, " ").replace(/\s+/g, " ").trim();
    roster.forEach(p => {
      const ln = (L.teams[p.t] || {}).lines;
      if (!ln) return;
      const k = key(p.n),
        has = sl => (ln[sl] || []).some(x => key(x) === k);
      o[p.id] = {
        es: ["F1", "F2", "F3", "F4", "D1", "D2", "D3", "G"].find(has),
        pp: ["PP1", "PP2"].find(has)
      };
    });
    return o;
  }, [s.players, tid, (window.LINES_DATA || {}).generated]);
  useEffect(() => {
    let dead = false;
    const E = window.ESPN_DATA || {},
      out = {},
      byId = {};
    roster.forEach(p => byId[String(p.id).slice(1)] = p);
    Object.entries(E.daily || {}).forEach(([d, Tm]) => Object.values(Tm || {}).forEach(tm => Object.entries(tm || {}).forEach(([pid, v]) => {
      const p = byId[pid];
      if (!p || !v || v[0] == null || !(SCHED[p.t] && SCHED[p.t].has(d)) || gState(p.t, d).s === "P" || p.p === "G" && !v[0]) return;
      (out[pid] = out[pid] || {})[d] = v[0];
    })));
    const finish = () => {
      if (dead) return;
      const h = {};
      Object.keys(out).forEach(pid => {
        h[pid] = Object.keys(out[pid]).sort().slice(-5).map(d => out[pid][d]);
      });
      setHist(h);
    };
    finish();
    gxBoxIdx().then(ds => Promise.all(ds.slice(-14).map(d => gxBoxDay(d).then(day => [d, day])))).then(days => {
      days.forEach(([d, day]) => {
        if (!day) return;
        Object.keys(byId).forEach(pid => {
          const x = day[pid];
          if (x) {
            const o2 = out[pid] = out[pid] || {};
            o2[d] = x.fp != null ? x.fp : o2[d] != null ? o2[d] : gxEst(x, s.sc || {});
          } else if (out[pid]) delete out[pid][d];
        });
      });
      finish();
    }).catch(() => {});
    return () => {
      dead = true;
    };
  }, [s.players, gen, tid]);
  const RO = {
    F1: "L1",
    F2: "L2",
    F3: "L3",
    F4: "L4",
    D1: "D1",
    D2: "D2",
    D3: "D3"
  };
  const roleTxt = p => {
    if (p.p === "G") return gxGsTxt106(p);
    const r = roles[p.id];
    return r ? [r.es ? RO[r.es] : "not in lineup", r.pp].filter(Boolean).join(" \u00b7 ") : "";
  };
  const nextGame = p => {
    const S = SCHED[p.t];
    if (!S || p.ir) return "";
    for (let i = 0; i < 10; i++) {
      const dt = addDays(today, i);
      if (S.has(dt) && (i > 0 || gState(p.t, dt).s === "P")) {
        const gm = gameOf(p.t, dt);
        return (i === 0 ? "Today" : dayLabel(dt).split(",")[0]) + (gm ? (gm.h ? " vs " : " @ ") + gm.o : "");
      }
    }
    return "";
  };
  const left = p => (wk.games[p.t] || []).filter(d => dates[d] >= today && gState(p.t, dates[d]).s === "P").length;
  const nextG = p => nextW ? gms(nextW, p.t) : 0;
  const keyFn = {
    mu: p => mu[p.id] || 0,
    left,
    next: nextG,
    sea: p => p.gp ? p.tot / p.gp : -99,
    pg: pv,
    rk: p => -(rankOf[p.id] || 9999),
    l5: p => gxL5v(hist[String(p.id).slice(1)])
  }[sort]; // change 079: Last 5 sorts too
  const grp = k => roster.filter(p => !p.ir && p.p === k).sort((a, b) => keyFn(b) - keyFn(a));
  const groups = [["Forwards", grp("F")], ["Defence", grp("D")], ["Goalies", grp("G")], ["Injured reserve", roster.filter(p => p.ir)]].filter(x => x[1].length);
  const HB = (k, l, cls) => /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: "n " + (cls || "") + (sort === k ? " on" : ""),
    onClick: () => setSort(sort === k ? "pg" : k)
  }, l);
  const row = p => {
    const st = p.ir ? "IR" : p.status && p.status !== "ACTIVE" ? M_ST[p.status] || p.status.replace(/_/g, " ") : "";
    const m = mu[p.id],
      sea = p.gp ? p.tot / p.gp : null,
      gap = sea != null && p.avg > 0 ? sea - p.avg : null,
      rk = rankOf[p.id];
    const sub = [roleTxt(p), nextGame(p)].filter(Boolean).join(" \u00b7 "),
      h = hist[String(p.id).slice(1)] || [];
    return /*#__PURE__*/React.createElement("div", {
      key: p.id,
      className: "gx-ro"
    }, /*#__PURE__*/React.createElement("div", {
      className: "gx-fc99"
    }, /*#__PURE__*/React.createElement(GxFace, {
      p: p,
      size: 26
    })), /*#__PURE__*/React.createElement("div", {
      className: "min-w-0"
    }, /*#__PURE__*/React.createElement("div", {
      className: "truncate"
    }, /*#__PURE__*/React.createElement(PN, {
      p: p,
      className: ""
    }), st ? /*#__PURE__*/React.createElement("span", {
      className: "text-xs",
      style: {
        color: "var(--bad)",
        marginLeft: 8
      }
    }, st) : null), sub ? /*#__PURE__*/React.createElement("div", {
      className: "text-xs text-slate-500 truncate"
    }, sub) : null), gxToday99(p), /*#__PURE__*/React.createElement("div", {
      className: "gx-sp m-hide",
      title: "Last five games, oldest to newest"
    }, h.length ? h.map((v, i) => /*#__PURE__*/React.createElement("i", {
      key: i,
      style: {
        height: Math.max(2, Math.min(22, Math.max(0, v) / 20 * 22)),
        background: v < 0 ? "var(--bad)" : "var(--ink2)"
      }
    })) : /*#__PURE__*/React.createElement("span", {
      className: "text-xs text-slate-500"
    }, "\u2013")), /*#__PURE__*/React.createElement("div", {
      className: "n"
    }, /*#__PURE__*/React.createElement("div", {
      className: "font-semibold",
      style: p.p === "G" && m != null ? {
        color: m > 5 ? "var(--good)" : m < 0 ? "var(--bad)" : "var(--ink)"
      } : null
    }, m == null ? "\u2013" : f1(m)), m > 0 && total > 0 ? /*#__PURE__*/React.createElement("div", {
      style: {
        height: 3,
        background: "var(--track)",
        marginTop: 3
      }
    }, /*#__PURE__*/React.createElement("div", {
      style: {
        height: 3,
        width: Math.min(100, m / total * 100) + "%",
        background: "var(--accent)"
      }
    })) : null), /*#__PURE__*/React.createElement("div", {
      className: "n text-slate-500"
    }, p.ir ? "\u2013" : left(p)), /*#__PURE__*/React.createElement("div", {
      className: "n text-slate-500 m-hide"
    }, nextW && !p.ir ? nextG(p) : "\u2013"), /*#__PURE__*/React.createElement("div", {
      className: "n m-hide"
    }, sea == null ? "\u2013" : f1(sea), p.p === "G" && gxGS106(p) ? /*#__PURE__*/React.createElement("span", {
      className: "gx-gs106"
    }, gxGS106(p).pct) : null), /*#__PURE__*/React.createElement("div", {
      className: "n"
    }, f1(effAvg(p, K))), /*#__PURE__*/React.createElement("div", {
      className: "n text-xs text-slate-500 m-hide"
    }, rk ? p.p + " " + ordN(rk) : "\u2013"), /*#__PURE__*/React.createElement(GxSC106, {
      p: p,
      s: s,
      mode: "full"
    }));
  };
  return /*#__PURE__*/React.createElement("div", {
    className: "gx-pn"
  }, /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement(GxRngSel100, null), /*#__PURE__*/React.createElement("div", {
    className: "gx-sc99"
  }, /*#__PURE__*/React.createElement("div", {
    className: "gx-ro gx-roh"
  }, /*#__PURE__*/React.createElement("span", null), /*#__PURE__*/React.createElement("span", null, "Player"), /*#__PURE__*/React.createElement("span", null, "Today"), /*#__PURE__*/React.createElement("span", {
    className: "n"
  }, "Pts"), HB("l5", "Last 5", "m-hide"), HB("mu", "Matchup"), HB("left", "Left"), HB("next", "Next wk", "m-hide"), /*#__PURE__*/React.createElement(GxHB108, {
    k: "Avg"
  }), /*#__PURE__*/React.createElement(GxHB108, {
    k: "Exp",
    l: "Expected"
  }), /*#__PURE__*/React.createElement(GxHB108, {
    k: "Rank"
  }), /*#__PURE__*/React.createElement(GxSH106, {
    mode: "sk"
  })), groups.map(([title, list]) => /*#__PURE__*/React.createElement("div", {
    key: title,
    style: {
      marginBottom: 10
    }
  }, /*#__PURE__*/React.createElement("div", {
    className: "gx-tag",
    style: {
      padding: "8px 0 4px"
    }
  }, title), title === "Goalies" ? /*#__PURE__*/React.createElement(GxGH104, null) : null, gxSort108(list, s).map(row)))));
}

// ---------- round 58: Best projection and phone alert switches (news_logos.py) ----------
function GxBest({
  s,
  setS
}) {
  useEffect(() => {
    if (!s.pbest) return;
    let dead = false;
    const MAP = {
      espn: "espn",
      gm: "model",
      blend: "blend",
      ai: "ai"
    };
    const use = m => {
      let k = MAP[m] || "ai";
      if (k === "ai" && !window.__AI || k !== "espn" && !window.__MODEL) k = window.__MODEL ? "model" : "espn";
      if (!dead) setS(st => st.pmode === k ? st : {
        ...st,
        pmode: k,
        players: [...st.players]
      });
    };
    let c = null;
    try {
      c = JSON.parse(localStorage.getItem("gm-best") || "null");
    } catch (e) {}
    if (c && c.d === todayISO() && c.m) {
      use(c.m);
      return;
    }
    fetch("ai/report.json?t=" + Date.now()).then(r => r.ok ? r.json() : null).then(j => {
      const m = j && j.best && j.best.skater && j.best.skater.model;
      if (!m) return;
      try {
        localStorage.setItem("gm-best", JSON.stringify({
          d: todayISO(),
          m
        }));
      } catch (e) {}
      use(m);
    }).catch(() => {});
    return () => {
      dead = true;
    };
  }, [s.pbest]);
  return null;
}
// ---------- round 61: any week on two Today boxes (news_logos.py) ----------
const gxSpan61 = ds => {
  if (!ds || !ds.length) return "";
  const a = ds[0],
    b = ds[ds.length - 1];
  return mdL(a) + " to " + (fromIso(a).getMonth() === fromIso(b).getMonth() ? fromIso(b).getDate() : mdL(b));
};
const gxWkName61 = (s, k) => k === s.wk ? "This week" : k === s.wk + 1 ? "Next week" : "Week " + (k + 1);
const gxWkAt61 = (s, pick) => pick == null ? s.wk : Math.max(0, Math.min(s.weeks.length - 1, pick));
const gxSwipe61 = (ref, i, go) => ({
  onTouchStart: e => {
    const t = e.touches[0];
    ref.current = [t.clientX, t.clientY];
  },
  onTouchEnd: e => {
    const t0 = ref.current,
      t = e.changedTouches[0];
    ref.current = null;
    if (!t0 || e.target.closest && e.target.closest("select, button")) return;
    const dx = t.clientX - t0[0],
      dy = t.clientY - t0[1];
    if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy) * 1.5) go(i + (dx < 0 ? 1 : -1));
  }
});
const GxWkPick = ({
  s,
  i,
  go
}) => /*#__PURE__*/React.createElement("span", {
  className: "gx-wpk"
}, /*#__PURE__*/React.createElement("button", {
  type: "button",
  "aria-label": "Earlier week",
  disabled: i <= 0,
  onClick: () => go(i - 1)
}, "\u2039"), /*#__PURE__*/React.createElement("select", {
  "aria-label": "Choose a week",
  value: i,
  onChange: e => go(+e.target.value)
}, s.weeks.map((w, k) => /*#__PURE__*/React.createElement("option", {
  key: k,
  value: k
}, gxWkName61(s, k)))), /*#__PURE__*/React.createElement("button", {
  type: "button",
  "aria-label": "Later week",
  disabled: i >= s.weeks.length - 1,
  onClick: () => go(i + 1)
}, "\u203a"));
function GxGamesAny({
  s,
  wk,
  A,
  B
}) {
  const K = s.blend,
    today = todayISO();
  const [pick, setPick] = useState(null);
  const touch = React.useRef(null);
  const i = gxWkAt61(s, pick),
    cur = i === s.wk;
  const go = k => setPick(Math.max(0, Math.min(s.weeks.length - 1, k)));
  const w = useMemo(() => cur ? wk : deriveWeek(s.weeks[i], s.autoDone), [cur, wk, s.weeks, i, s.autoDone]);
  const dates = w.dates || [],
    opp = oppOf(w, s.me) || (cur ? s.opp : null);
  const fin = !cur && dates.length > 0 && dates[dates.length - 1] < today;
  const N = useMemo(() => {
    if (cur || fin || !opp || !dates.length) return null;
    const R = id => weekLive(s.players.filter(p => p.ft === id), w, K, id);
    return [R(s.me), R(opp)];
  }, [cur, fin, opp, w, s.players, K, window.__PMODE, window.__LIVEV120]);
  const X = cur ? A : N ? N[0] : null,
    Y = cur ? B : N ? N[1] : null;
  const rows = X && Y ? dates.map((dt, d) => ({
    dt,
    a: gxGmN(X.days[d]),
    b: gxGmN(Y.days[d])
  })) : [];
  const tot = (k, from) => rows.reduce((x, r) => x + (r.dt >= from ? r[k] : 0), 0);
  const mx = Math.max(1, Math.max.apply(null, rows.map(r => Math.max(r.a, r.b))));
  const live = dates.length > 0 && dates[0] <= today && dates[dates.length - 1] >= today;
  const sa = +gxAct120(w)[s.me] || 0,
    sb = opp ? +gxAct120(w)[opp] || 0 : 0;
  const sub = [opp ? "vs " + teamName(s, opp) : "", gxSpan61(dates), fin ? "final" : rows.length ? "lineup games: you " + tot("a", "") + ", them " + tot("b", "") : "", !fin && live && rows.length ? "from today " + tot("a", today) + " and " + tot("b", today) : ""].filter(Boolean).join(" \u00b7 ");
  return /*#__PURE__*/React.createElement("div", _extends({
    className: "gx-pn",
    style: {
      minWidth: 0,
      touchAction: "pan-y"
    }
  }, gxSwipe61(touch, i, go)), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      alignItems: "center",
      gap: 8,
      flexWrap: "wrap"
    }
  }, /*#__PURE__*/React.createElement("span", {
    className: "gx-tag"
  }, cur ? "Games this matchup" : "Games in " + (i === s.wk + 1 ? "next week" : "week " + (i + 1))), /*#__PURE__*/React.createElement(GxWkPick, {
    s: s,
    i: i,
    go: go
  })), /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500",
    style: {
      marginTop: 4
    }
  }, sub), rows.length ? /*#__PURE__*/React.createElement("div", {
    className: "gx-n7 gx-gm",
    style: {
      gridTemplateColumns: "repeat(" + rows.length + ", minmax(0,1fr))"
    }
  }, rows.map(r => {
    const now = r.dt === today,
      past = r.dt < today;
    return /*#__PURE__*/React.createElement("div", {
      key: r.dt,
      style: {
        padding: "6px 0",
        borderRadius: 6,
        background: now ? "var(--accentSoft)" : "transparent"
      }
    }, /*#__PURE__*/React.createElement("div", {
      className: "bars"
    }, /*#__PURE__*/React.createElement("i", {
      style: {
        height: r.a / mx * 64,
        background: "var(--accent)",
        opacity: past ? 0.45 : 1
      }
    }), /*#__PURE__*/React.createElement("i", {
      style: {
        height: r.b / mx * 64,
        background: "var(--faint)",
        opacity: past ? 0.45 : 1
      }
    })), /*#__PURE__*/React.createElement("div", {
      className: "text-sm",
      style: {
        marginTop: 4
      }
    }, r.a, " ", /*#__PURE__*/React.createElement("span", {
      className: "text-slate-500"
    }, r.b)), /*#__PURE__*/React.createElement("div", {
      className: "text-xs " + (now ? "font-semibold" : "text-slate-500")
    }, now ? "Today" : dayLabel(r.dt).split(",")[0]));
  })) : fin && opp && (sa || sb) ? /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      alignItems: "baseline",
      gap: 10,
      paddingTop: 10,
      fontVariantNumeric: "tabular-nums"
    }
  }, /*#__PURE__*/React.createElement("span", {
    className: "gx-stv"
  }, f1(sa)), /*#__PURE__*/React.createElement("span", {
    className: "text-slate-500"
  }, "to ", f1(sb)), /*#__PURE__*/React.createElement("span", {
    style: {
      color: sa > sb ? "var(--good)" : sa < sb ? "var(--bad)" : "var(--mute)"
    }
  }, sa > sb ? "Won by " + f1(sa - sb) : sa < sb ? "Lost by " + f1(sb - sa) : "Tied")), /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500",
    style: {
      marginTop: 6
    }
  }, "Day by day games are only kept for the current week.")) : /*#__PURE__*/React.createElement("div", {
    className: "text-sm text-slate-500",
    style: {
      paddingTop: 10
    }
  }, fin ? "No result saved for this week." : opp ? "No games loaded for this week." : "The matchup for this week is not set yet."));
}
function GxLeagueAny({
  s,
  wk
}) {
  const K = s.blend,
    gen = (window.ESPN_DATA || {}).generated,
    today = todayISO();
  const [pick, setPick] = useState(null);
  const touch = React.useRef(null);
  const i = gxWkAt61(s, pick),
    cur = i === s.wk;
  const go = k => setPick(Math.max(0, Math.min(s.weeks.length - 1, k)));
  const w = useMemo(() => cur ? wk : deriveWeek(s.weeks[i], s.autoDone), [cur, wk, s.weeks, i, s.autoDone]);
  const dates = w.dates || [];
  const fin = !cur && dates.length > 0 && dates[dates.length - 1] < today;
  const rows = useMemo(() => (w.pairs || []).filter(p => p[0] && p[1] && p[0] !== s.me && p[1] !== s.me).map(([a, b]) => {
    const act = id => +gxAct120(w)[id] || 0;
    if (fin) return {
      a,
      b,
      sa: act(a),
      sb: act(b)
    };
    const R = id => weekLive(s.players.filter(p => p.ft === id), w, K, id);
    return {
      a,
      b,
      p: winProb(R(a), R(b), act(a), act(b))
    };
  }), [s.players, w, fin, K, gen, window.__PMODE, window.__LIVEV120]);
  const sub = cur ? "Win chance right now" : [gxSpan61(dates), fin ? "final scores" : "projected win chance from today's rosters"].filter(Boolean).join(" \u00b7 ");
  return /*#__PURE__*/React.createElement("div", _extends({
    className: "gx-pn",
    style: {
      minWidth: 0,
      touchAction: "pan-y"
    }
  }, gxSwipe61(touch, i, go)), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      alignItems: "center",
      gap: 8,
      flexWrap: "wrap"
    }
  }, /*#__PURE__*/React.createElement("span", {
    className: "gx-tag"
  }, "Around the league"), /*#__PURE__*/React.createElement(GxWkPick, {
    s: s,
    i: i,
    go: go
  })), /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500",
    style: {
      margin: "4px 0"
    }
  }, sub), rows.length ? rows.map((r, k) => {
    const p = fin ? r.sa + r.sb > 0 ? r.sa / (r.sa + r.sb) : 0.5 : r.p;
    const la = fin ? r.sa >= r.sb : p >= 0.5,
      close = !fin && Math.abs(p - 0.5) < 0.1;
    const bar = win => win ? "var(--good)" : "var(--bad)";
    return /*#__PURE__*/React.createElement("div", {
      key: r.a + "-" + r.b,
      className: "gx-lg",
      style: k ? null : {
        borderTop: 0
      }
    }, /*#__PURE__*/React.createElement("span", {
      className: "truncate"
    }, /*#__PURE__*/React.createElement(TL, {
      s: s,
      id: r.a
    })), /*#__PURE__*/React.createElement("span", {
      className: "text-right",
      style: {
        color: la || close ? "var(--ink)" : "var(--mute)"
      }
    }, fin ? Math.round(r.sa) : wpTxt(p)), /*#__PURE__*/React.createElement("span", {
      style: {
        display: "flex",
        height: 4,
        gap: 2
      }
    }, /*#__PURE__*/React.createElement("i", {
      style: {
        display: "block",
        width: Math.round(p * 100) + "%",
        background: bar(la)
      }
    }), /*#__PURE__*/React.createElement("i", {
      style: {
        display: "block",
        flex: 1,
        background: bar(!la)
      }
    })), /*#__PURE__*/React.createElement("span", {
      style: {
        color: !la || close ? "var(--ink)" : "var(--mute)"
      }
    }, fin ? Math.round(r.sb) : wpTxt(1 - p)), /*#__PURE__*/React.createElement("span", {
      className: "truncate text-right"
    }, /*#__PURE__*/React.createElement(TL, {
      s: s,
      id: r.b
    })));
  }) : /*#__PURE__*/React.createElement("div", {
    className: "text-sm text-slate-500",
    style: {
      paddingTop: 6
    }
  }, cur ? "No other matchups loaded for this week." : "No other matchups are set for this week yet."));
}

// ---------- round 67: phone alerts page and helpers (news_logos.py) ----------
const GX_AL = [["Lineup warnings", "starter_is_out", "Starter is out", "An injured player is in your lineup with a game today", "injuries"], ["Lineup warnings", "possible_scratch", "Possible scratch", "A starter is missing from tonight's lineup, within 3 hours of the game", "injuries"], ["Lineup warnings", "goalie_not_starting", "Goalie not starting", "Your goalie is not tonight's starter", "goalies"], ["Lineup warnings", "goalie_not_confirmed", "Goalie not confirmed", "75 minutes before the game and still not confirmed", "goalies"], ["Lineup warnings", "bench_player_has_a_game", "Bench player has a game", "A bench player plays while a starter does not", ""], ["Your players", "your_player_line_change", "Line change", "Moved up or down a line", "lines"], ["Your players", "your_player_lineup_change", "In or out of the lineup", "Added to or missing from his team's lineup", "lines"], ["Your players", "your_player_power_play_change", "Power-play change", "On or off a power-play unit", "lines"], ["Your players", "your_player_roster_move", "Roster move", "Traded, called up or sent down", "lines"], ["Your players", "your_player_injury_update", "Injury update", "ESPN injury status changed", "injuries"], ["Your players", "your_player_losing_ice_time", "Losing ice time", "Down 3 or more minutes a game lately", "lines"], ["Your players", "more_line_changes", "Extra line changes", "Several changes at once, sent as one message", "lines"], ["Pickup ideas", "pickup_bigger_role", "Bigger role", "A free agent moved to a top-six line or the top pair", "pickups"], ["Pickup ideas", "pickup_new_pp1", "New on the top power play", "A free agent just moved onto PP1", "pickups"], ["Pickup ideas", "pickup_ice_time_jump", "Ice time jump", "A free agent's minutes went up a lot", "pickups"], ["Pickup ideas", "pickup_trending", "Trending free agent", "Other managers are adding him fast", "pickups"], ["Summaries", "morning_summary", "Morning summary", "8 a.m., everything that waited overnight", ""], ["Summaries", "pregame_summary", "Before puck drop", "An hour before your first game, only if something new came in", ""]];
const GX_AL_MASTER = [["injuries", "Injuries"], ["lines", "Line and power-play changes"], ["goalies", "Goalie starts"], ["pickups", "Pickup ideas"]];
const GX_AL_TITLES = [["Lineup: starter is OUT", "starter_is_out"], ["Possible scratch tonight", "possible_scratch"], ["Your player: injury update", "your_player_injury_update"], ["Lineup: bench player has a game", "bench_player_has_a_game"], ["Goalie not starting tonight", "goalie_not_starting"], ["Goalie not confirmed yet", "goalie_not_confirmed"], ["Your player's line changed", "your_player_line_change"], ["Your player: lineup change", "your_player_lineup_change"], ["Your player: power-play change", "your_player_power_play_change"], ["Your player: roster move", "your_player_roster_move"], ["Your player is losing ice time", "your_player_losing_ice_time"], ["Pickup: new PP1 free agent", "pickup_new_pp1"], ["Pickup: ice time jump", "pickup_ice_time_jump"], ["Pickup: trending free agent", "pickup_trending"], ["Pickup idea: bigger role", "pickup_bigger_role"], ["Morning summary", "morning_summary"], ["Before puck drop", "pregame_summary"]];
const GX_PREFS_URL = "https://github.com/dhaliwal32/23456789786634356/edit/main/alert_prefs.json";
const gxAlKind = title => {
  const t = String(title || "");
  if (t.indexOf("roster/line changes") >= 0) return "more_line_changes";
  const m = GX_AL_TITLES.find(x => t.indexOf(x[0]) === 0);
  return m ? m[1] : null;
};
const gxAlertState = p => GX_AL.map(([sec, k, label, desc, g]) => {
  const own = p && p[k] != null ? p[k] : k !== "bench_player_has_a_game";
  const gOff = !!(g && p && p[g] === false);
  const gl = (GX_AL_MASTER.find(x => x[0] === g) || [])[1];
  return {
    sec,
    k,
    label,
    desc,
    on: own !== false && !gOff,
    why: own === false ? "" : gOff ? "off by the " + gl + " master switch" : ""
  };
});
const gxAlertLog = b => {
  const out = [],
    LBL = {
      urgent: "Sent right away",
      morning: "Morning summary",
      pregame: "Before puck drop"
    };
  (b && b.log || []).forEach(m => out.push({
    at: m.at,
    title: m.title,
    body: m.body,
    status: LBL[m.kind] || m.kind || "Sent",
    held: /^Not sent/.test(m.kind || "")
  }));
  (b && b.items || []).forEach(i => {
    if (i.sent && (i.via === "urgent" || !i.via && i.urgent)) out.push({
      at: i.sent_at || i.at,
      title: i.title,
      body: i.text,
      status: "Sent right away",
      held: false
    });else if (!i.sent) out.push({
      at: i.at,
      title: i.title,
      body: i.text,
      status: "Waiting for the next summary",
      held: false,
      wait: true
    });
  });
  return out.sort((a, c) => String(a.at || "") < String(c.at || "") ? 1 : -1);
};
const gxWhen = iso => {
  const d = toDate(iso);
  if (!d) return "";
  const t = d.toLocaleTimeString([], {
    hour: "numeric",
    minute: "2-digit"
  });
  const k = x => x.toDateString(),
    now = new Date(),
    y = new Date(Date.now() - 864e5);
  return (k(d) === k(now) ? "Today " : k(d) === k(y) ? "Yesterday " : d.toLocaleDateString("en-US", {
    weekday: "short",
    month: "short",
    day: "numeric"
  }).replace(",", "") + " ") + t;
};
const gxAlLoad = () => Promise.all([fetch("alert_prefs.json?t=" + Date.now()).then(r => r.ok ? r.json() : null).catch(() => null), fetch("notify_outbox.json?t=" + Date.now()).then(r => r.ok ? r.json() : null).catch(() => null)]).then(([p, b]) => ({
  p: p,
  b: b
}));
function GxAlertsPage() {
  // alerts page v67 (news_logos.py)
  const [d, setD] = useState(null);
  const [f, setF] = useState("all");
  const [lim, setLim] = useState(30);
  useEffect(() => {
    let dead = false;
    const load = () => gxAlLoad().then(x => {
      if (!dead) setD(x);
    });
    load();
    const id = setInterval(load, 2 * 60 * 1000);
    return () => {
      dead = true;
      clearInterval(id);
    };
  }, []);
  if (!d) return /*#__PURE__*/React.createElement("div", {
    className: "text-sm text-slate-500"
  }, "Loading your phone alerts...");
  const st = gxAlertState(d.p),
    log = gxAlertLog(d.b);
  const cut = new Date(Date.now() - 7 * 864e5).toISOString().slice(0, 19) + "Z";
  const cnt = {};
  log.forEach(m => {
    if (m.held || m.wait || String(m.at || "") < cut) return;
    const k = gxAlKind(m.title);
    if (k) cnt[k] = (cnt[k] || 0) + 1;
  });
  const shown = log.filter(m => f === "all" ? true : f === "held" ? m.held : f === "wait" ? m.wait : !m.held && !m.wait);
  const onN = st.filter(x => x.on).length;
  const chip = m => {
    const c = m.held ? "var(--mute)" : m.wait ? "var(--warn)" : "var(--good)";
    return /*#__PURE__*/React.createElement("span", {
      className: "gx-chip",
      style: {
        color: c,
        borderColor: c
      }
    }, m.status);
  };
  return /*#__PURE__*/React.createElement("div", {
    className: "space-y-3"
  }, /*#__PURE__*/React.createElement("div", {
    className: "font-semibold",
    style: {
      fontSize: 17
    }
  }, "Phone alerts"), /*#__PURE__*/React.createElement("div", {
    className: "gx-pn"
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      alignItems: "baseline",
      gap: 8
    }
  }, /*#__PURE__*/React.createElement("span", {
    className: "gx-tag"
  }, "Switches \u00b7 " + onN + " on, " + (st.length - onN) + " off"), /*#__PURE__*/React.createElement("a", {
    className: "text-sm text-blue-600",
    style: {
      marginLeft: "auto"
    },
    href: GX_PREFS_URL,
    target: "_blank",
    rel: "noopener"
  }, "Change")), /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500",
    style: {
      marginTop: 2
    }
  }, "Change opens the settings file on GitHub. Set a line to false to switch it off, then commit. It applies at the next sync, within 30 minutes. Nothing is sent from 11 p.m. to 7 a.m."), ["Lineup warnings", "Your players", "Pickup ideas", "Summaries"].map(sec => /*#__PURE__*/React.createElement("div", {
    key: sec
  }, /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500",
    style: {
      margin: "12px 0 2px",
      letterSpacing: ".04em"
    }
  }, sec), st.filter(x => x.sec === sec).map((x, i) => /*#__PURE__*/React.createElement("div", {
    key: x.k,
    className: "gx-row",
    style: i ? null : {
      borderTop: 0
    }
  }, /*#__PURE__*/React.createElement("div", {
    className: "min-w-0",
    style: {
      flex: 1
    }
  }, /*#__PURE__*/React.createElement("div", null, x.label), /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500"
  }, x.desc + " \u00b7 " + (cnt[x.k] || 0) + " in the last 7 days" + (x.why ? " \u00b7 " + x.why : ""))), /*#__PURE__*/React.createElement("span", {
    className: "text-sm",
    style: {
      color: x.on ? "var(--good)" : "var(--mute)"
    }
  }, x.on ? "On" : "Off"))))), /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500",
    style: {
      margin: "12px 0 2px",
      letterSpacing: ".04em"
    }
  }, "Master switches"), GX_AL_MASTER.map(([k, l], i) => {
    const on = !(d.p && d.p[k] === false);
    return /*#__PURE__*/React.createElement("div", {
      key: k,
      className: "gx-row",
      style: i ? null : {
        borderTop: 0
      }
    }, /*#__PURE__*/React.createElement("span", {
      className: "min-w-0",
      style: {
        flex: 1
      }
    }, l, /*#__PURE__*/React.createElement("span", {
      className: "text-xs text-slate-500"
    }, " \u00b7 turns its whole group on or off")), /*#__PURE__*/React.createElement("span", {
      className: "text-sm",
      style: {
        color: on ? "var(--good)" : "var(--mute)"
      }
    }, on ? "On" : "Off"));
  })), /*#__PURE__*/React.createElement("div", {
    className: "gx-pn"
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      alignItems: "center",
      gap: 8,
      flexWrap: "wrap"
    }
  }, /*#__PURE__*/React.createElement("span", {
    className: "gx-tag"
  }, "Sent to your phone"), /*#__PURE__*/React.createElement("span", {
    className: "gx-seg",
    style: {
      marginLeft: "auto"
    }
  }, [["all", "All"], ["sent", "Sent"], ["held", "Held back"], ["wait", "Waiting"]].map(([k, l]) => /*#__PURE__*/React.createElement("button", {
    key: k,
    type: "button",
    className: f === k ? "on" : "",
    onClick: () => {
      setF(k);
      setLim(30);
    }
  }, l)))), shown.length ? shown.slice(0, lim).map((m, i) => {
    const k = gxAlKind(m.title);
    return /*#__PURE__*/React.createElement("div", {
      key: i,
      className: "gx-row",
      style: i ? {
        alignItems: "flex-start"
      } : {
        alignItems: "flex-start",
        borderTop: 0,
        marginTop: 6
      }
    }, /*#__PURE__*/React.createElement("div", {
      className: "min-w-0",
      style: {
        flex: 1
      }
    }, /*#__PURE__*/React.createElement("div", null, m.title), m.body ? /*#__PURE__*/React.createElement("div", {
      className: "text-xs text-slate-500",
      style: {
        whiteSpace: "pre-wrap",
        marginTop: 2
      }
    }, m.body) : null, /*#__PURE__*/React.createElement("div", {
      className: "text-xs text-slate-500",
      style: {
        marginTop: 3
      }
    }, gxWhen(m.at), k ? /*#__PURE__*/React.createElement(React.Fragment, null, " \u00b7 ", /*#__PURE__*/React.createElement("a", {
      className: "text-blue-600",
      href: GX_PREFS_URL,
      target: "_blank",
      rel: "noopener"
    }, "Change this switch")) : null)), chip(m));
  }) : /*#__PURE__*/React.createElement("div", {
    className: "text-sm text-slate-500",
    style: {
      paddingTop: 8
    }
  }, "Nothing here yet."), shown.length > lim ? /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: "text-sm text-blue-600",
    style: {
      marginTop: 10
    },
    onClick: () => setLim(lim + 30)
  }, "Show more") : null));
}

// change 069: old unused pages removed
// ---------- change 070: This week box as a score race, any week (install.py) ----------
function GxRace({
  s,
  wk
}) {
  const K = s.blend,
    today = todayISO(),
    gen = (window.ESPN_DATA || {}).generated;
  const [pick, setPick] = useState(null);
  const [sel, setSel] = useState(null);
  const [W, setW] = useState(620);
  const box = React.useRef(null);
  const touch = React.useRef(null);
  useEffect(() => {
    const el = box.current;
    if (!el) return;
    const fit = () => setW(Math.max(290, Math.round(el.clientWidth - 28)));
    fit();
    if (window.ResizeObserver) {
      const ro = new ResizeObserver(fit);
      ro.observe(el);
      return () => ro.disconnect();
    }
    window.addEventListener("resize", fit);
    return () => window.removeEventListener("resize", fit);
  }, []);
  useEffect(() => {
    const h = () => {
      setPick(Math.min(s.weeks.length - 1, s.wk + 1));
      setSel(null);
      if (box.current) box.current.scrollIntoView({
        behavior: "smooth",
        block: "start"
      });
    };
    window.addEventListener("gx-race-next", h);
    return () => window.removeEventListener("gx-race-next", h);
  }, [s.wk, s.weeks.length]);
  const i = gxWkAt61(s, pick),
    cur = i === s.wk;
  const go = k => {
    setPick(Math.max(0, Math.min(s.weeks.length - 1, k)));
    setSel(null);
  };
  const w = useMemo(() => cur ? wk : deriveWeek(s.weeks[i], s.autoDone), [cur, wk, s.weeks, i, s.autoDone]);
  const dates = w.dates || [],
    n = dates.length;
  const opp = oppOf(w, s.me) || (cur ? s.opp : null);
  const up = !(n > 0 && dates[0] <= today),
    fin = !cur && n > 0 && dates[n - 1] < today;
  const R = useMemo(() => {
    if (!opp || !n || fin) return null;
    const run = id => weekLive(s.players.filter(p => p.ft === id), w, K, id, {
      detail: true
    });
    return [run(s.me), run(opp)];
  }, [w, opp, fin, s.players, K, gen, window.__PMODE, window.__LIVEV120]);
  const mv = useMemo(() => {
    if (!up || !opp || !R) return null;
    try {
      const sW = {
        ...s,
        wk: i
      };
      const r = computeMoves(sW, {
        H: 1,
        pool: 40
      }).res.filter(x => x.gain >= (s.minGain ?? 3))[0];
      if (!r) return {
        none: true
      };
      return {
        r,
        b: winChance(sW),
        a: winChance(sW, afterMove(sW, r.f, r.d))
      };
    } catch (e) {
      return null;
    }
  }, [up, i, opp, R]);
  const sl105 = useSlide105(i);
  const [dr106, dh106] = useDrag106(i > 0 ? () => go(i - 1) : null, i < s.weeks.length - 1 ? () => go(i + 1) : null);
  const act = id => +gxAct120(w)[id] || 0;
  const sa = up ? 0 : act(s.me),
    sb = up || !opp ? 0 : act(opp);
  const nm0 = opp ? (teamName(s, opp) || "").split(" ")[0] : "",
    nm = nm0.length > 10 ? nm0.slice(0, 9) + "\u2026" : nm0;
  const title = cur ? "This week" : up && i === s.wk + 1 ? "Next week" : "Week " + (i + 1);
  const head = /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      alignItems: "center",
      gap: 8,
      flexWrap: "wrap"
    }
  }, /*#__PURE__*/React.createElement("span", {
    className: "gx-tag"
  }, title, opp ? " \u00b7 vs " + teamName(s, opp) : ""), /*#__PURE__*/React.createElement(GxWkPick, {
    s: s,
    i: i,
    go: go
  }));
  const wrapP = {
    className: "gx-pn",
    ref: box,
    style: {
      minWidth: 0,
      touchAction: "pan-y"
    }
  };
  if (fin || !R) {
    return /*#__PURE__*/React.createElement("div", wrapP, head, fin && opp && (sa || sb) ? /*#__PURE__*/React.createElement("div", {
      style: {
        display: "flex",
        alignItems: "baseline",
        gap: 10,
        paddingTop: 10,
        fontVariantNumeric: "tabular-nums"
      }
    }, /*#__PURE__*/React.createElement("span", {
      className: "gx-stv"
    }, f1(sa)), /*#__PURE__*/React.createElement("span", {
      className: "text-slate-500"
    }, "to ", f1(sb)), /*#__PURE__*/React.createElement("span", {
      style: {
        color: sa > sb ? "var(--good)" : sa < sb ? "var(--bad)" : "var(--mute)"
      }
    }, sa > sb ? "Won by " + f1(sa - sb) : sa < sb ? "Lost by " + f1(sb - sa) : "Tied")) : /*#__PURE__*/React.createElement("div", {
      className: "text-sm text-slate-500",
      style: {
        paddingTop: 10
      }
    }, fin ? "No result saved for this week." : "The matchup for this week is not set yet."), fin ? /*#__PURE__*/React.createElement("div", {
      className: "text-xs text-slate-500",
      style: {
        marginTop: 6
      }
    }, "Day by day scores are only kept for the current week.") : null);
  }
  const X = R[0],
    Y = R[1];
  const st = d => dates[d] < today ? "f" : dates[d] === today ? "t" : "p";
  const pts = (L, d) => {
    const x = L.days[d] || {},
      k = st(d);
    return k === "f" ? x.act || 0 : k === "t" ? (x.act || 0) + (x.total || 0) : x.total || 0;
  };
  const exp = (L, d) => {
    const x = L.days[d] || {};
    return x.proj != null ? x.proj : x.total || 0;
  };
  const me = dates.map((_, d) => pts(X, d)),
    th = dates.map((_, d) => pts(Y, d));
  const cum = a => {
    let t = 0;
    return a.map(v => t += v);
  };
  const CA = cum(me),
    CB = cum(th);
  const fdays = dates.map((_, d) => d).filter(d => st(d) === "f"),
    done = fdays.length;
  const EA = cum(dates.map((_, d) => exp(X, d))),
    EB = cum(dates.map((_, d) => exp(Y, d)));
  const wp = winProb(X, Y, sa, sb),
    fa = sa + X.total,
    fb = sb + Y.total;
  const ti = dates.indexOf(today),
    d0 = sel != null && sel < n ? sel : ti >= 0 ? ti : up ? 0 : n - 1;
  const narrow = W < 480,
    gut = narrow ? 80 : 108,
    L0 = 4,
    R0 = W - gut,
    cw = (R0 - L0) / n,
    cx = d => L0 + cw * (d + 0.5);
  const topV = Math.max(CA[n - 1], CB[n - 1], done ? Math.max(EA[done - 1], EB[done - 1]) : 0, 1) * 1.06;
  const base = 172,
    yy = v => base - v / topV * 158,
    Hh = (narrow ? 230 : 214) + (gxGopt105() === "text" ? 18 : 0);
  const P = (a, from, to) => a.slice(from, to + 1).map((v, k) => cx(from + k).toFixed(1) + "," + yy(v).toFixed(1)).join(" ");
  const ln = (col, dash, wdt, op) => ({
    fill: "none",
    stroke: col,
    strokeWidth: wdt || 2,
    strokeDasharray: dash || "none",
    strokeLinejoin: "round",
    strokeLinecap: "round",
    opacity: op || 1
  });
  const segs = [];
  for (let k = 0; k < n - 1; k++) {
    const ah = CA[k + 1] >= CB[k + 1];
    segs.push(/*#__PURE__*/React.createElement("polygon", {
      key: "g" + k,
      points: [cx(k) + "," + yy(CA[k]), cx(k + 1) + "," + yy(CA[k + 1]), cx(k + 1) + "," + yy(CB[k + 1]), cx(k) + "," + yy(CB[k])].join(" "),
      style: {
        fill: ah ? "var(--good)" : "var(--bad)",
        opacity: 0.1
      }
    }));
  }
  let ya = yy(CA[n - 1]) + 4,
    yb = yy(CB[n - 1]) + 4;
  if (Math.abs(ya - yb) < 15) {
    const m = (ya + yb) / 2,
      sg1 = ya <= yb ? -1 : 1;
    ya = m + sg1 * 7.5;
    yb = m - sg1 * 7.5;
  }
  ya = Math.max(12, ya);
  yb = Math.max(12, yb);
  const lx = cx(n - 1) + 12,
    fs = narrow ? 11 : 12;
  const sg = v => (v >= 0 ? "+" : "\u2212") + Math.round(Math.abs(v));
  const DN = d => dates[d] === today ? "Today" : dayLabel(dates[d]).split(",")[0];
  const rng = up || !done ? dates.map((_, d) => d) : fdays;
  const won = rng.filter(d => me[d] > th[d]).length;
  const bD = rng.reduce((b, d) => b == null || me[d] - th[d] > me[b] - th[b] ? d : b, null);
  const bestTxt = bD != null && me[bD] > th[bD] ? "best " + DN(bD) + " " + sg(me[bD] - th[bD]) : "";
  const vsA = fdays.reduce((t, d) => t + me[d] - exp(X, d), 0),
    vsB = fdays.reduce((t, d) => t + th[d] - exp(Y, d), 0);
  const gms = (L, d) => gxGmN(L.days[d]);
  const totG = L => dates.reduce((t, _, d) => t + gms(L, d), 0);
  const topOf = L => {
    const t = ((L || {}).start || []).filter(p => p.x > 0).sort((a, b) => b.x - a.x)[0];
    return t ? shortN(t.n) + " " + f1(t.x) : "\u2013";
  };
  const fact = (key, label, big, sub, col) => /*#__PURE__*/React.createElement("div", {
    key: key
  }, /*#__PURE__*/React.createElement("small", null, label), /*#__PURE__*/React.createElement("b", {
    style: col ? {
      color: col
    } : null
  }, big), sub ? /*#__PURE__*/React.createElement("span", {
    className: "text-sm text-slate-500"
  }, " " + sub) : null);
  const facts = up ? [fact("g", "Lineup games", totG(X), "them " + totG(Y)), fact("d", "Days favoured", won + " of " + n, bestTxt), fact("m", "Best move", mv ? mv.none ? "None worth it" : lastN(mv.r.f.n) + " in" : "\u2026", mv && !mv.none ? lastN(mv.r.d.n) + " out" + (mv.a != null && mv.b != null ? " \u00b7 " + wpTxt(mv.b).replace("%", "") + " \u2192 " + wpTxt(mv.a) : "") : "")] : [done ? fact("v", "Against projection", sg(vsA), "them " + sg(vsB), vsA >= 0 ? "var(--good)" : "var(--bad)") : fact("g", "Lineup games", totG(X), "them " + totG(Y)), fact("l", "Lineup games left", X.used, "them " + Y.used), done ? fact("w", "Days won", won + " of " + done, bestTxt) : fact("d", "Days favoured", won + " of " + n, bestTxt)];
  const k0 = st(d0),
    m0 = me[d0] - th[d0],
    x0 = X.days[d0] || {},
    y0 = Y.days[d0] || {};
  const mc = v => ({
    color: v >= 0 ? "var(--good)" : "var(--bad)"
  });
  return /*#__PURE__*/React.createElement("div", wrapP, head, /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500",
    style: {
      display: "none"
    }
  }, (done >= n ? "Final " : "Projected ") + Math.round(fa) + " \u2013 " + Math.round(fb) + " \u00b7 ", /*#__PURE__*/React.createElement("span", {
    style: {
      color: wp >= 0.5 ? "var(--good)" : "var(--bad)"
    }
  }, wpTxt(wp) + " to win")), /*#__PURE__*/React.createElement("svg", _extends({
    key: "w105-" + i,
    ref: dr106
  }, dh106, {
    viewBox: "0 0 " + W + " " + Hh,
    width: "100%",
    className: "gx-svg gx-dr106 gx-sl105 " + sl105,
    style: {
      display: "block",
      marginTop: 8
    },
    role: "img",
    "aria-label": "Running total for both teams through the week"
  }), /*#__PURE__*/React.createElement("rect", {
    x: cx(d0) - cw / 2 + 2,
    y: 4,
    width: cw - 4,
    height: Hh - 6,
    rx: 6,
    style: {
      fill: "var(--accentSoft)"
    }
  }), /*#__PURE__*/React.createElement("line", {
    x1: L0,
    x2: R0,
    y1: base,
    y2: base,
    style: {
      stroke: "var(--line)"
    }
  }), segs, gxGopt105() === "bars" ? dates.map((_, d) => {
    const ga = gms(X, d),
      gb = gms(Y, d);
    return /*#__PURE__*/React.createElement("g", {
      key: "gb" + d
    }, /*#__PURE__*/React.createElement("rect", {
      x: cx(d) - 9,
      y: base - ga * 4,
      width: 7,
      height: ga * 4,
      rx: 1.5,
      style: {
        fill: "var(--accent)",
        opacity: 0.3
      }
    }), /*#__PURE__*/React.createElement("rect", {
      x: cx(d) + 2,
      y: base - gb * 4,
      width: 7,
      height: gb * 4,
      rx: 1.5,
      style: {
        fill: "var(--mute)",
        opacity: 0.3
      }
    }));
  }) : null, done >= 2 ? /*#__PURE__*/React.createElement("polyline", {
    points: P(EB, 0, done - 1),
    style: ln("var(--mute)", "0.1 4.5", 2.2, 0.85)
  }) : null, done >= 2 ? /*#__PURE__*/React.createElement("polyline", {
    points: P(EA, 0, done - 1),
    style: ln("var(--accent)", "0.1 4.5", 2.2, 0.8)
  }) : null, done < n ? /*#__PURE__*/React.createElement("polyline", {
    points: P(CB, Math.max(0, done - 1), n - 1),
    style: ln("var(--mute)", "5 4")
  }) : null, done < n ? /*#__PURE__*/React.createElement("polyline", {
    points: P(CA, Math.max(0, done - 1), n - 1),
    style: ln("var(--accent)", "5 4")
  }) : null, done >= 2 ? /*#__PURE__*/React.createElement("polyline", {
    points: P(CB, 0, done - 1),
    style: ln("var(--mute)", null, 2.6)
  }) : null, done >= 2 ? /*#__PURE__*/React.createElement("polyline", {
    points: P(CA, 0, done - 1),
    style: ln("var(--accent)", null, 2.6)
  }) : null, fdays.map(d => /*#__PURE__*/React.createElement("g", {
    key: "f" + d
  }, /*#__PURE__*/React.createElement("circle", {
    cx: cx(d),
    cy: yy(CB[d]),
    r: 2.5,
    style: {
      fill: "var(--mute)"
    }
  }), /*#__PURE__*/React.createElement("circle", {
    cx: cx(d),
    cy: yy(CA[d]),
    r: 2.5,
    style: {
      fill: "var(--accent)"
    }
  }))), /*#__PURE__*/React.createElement("circle", {
    cx: cx(d0),
    cy: yy(CB[d0]),
    r: 4.5,
    style: k0 === "f" ? {
      fill: "var(--mute)",
      stroke: "var(--card)",
      strokeWidth: 2
    } : {
      fill: "var(--card)",
      stroke: "var(--mute)",
      strokeWidth: 2
    }
  }), /*#__PURE__*/React.createElement("circle", {
    cx: cx(d0),
    cy: yy(CA[d0]),
    r: 4.5,
    style: k0 === "f" ? {
      fill: "var(--accent)",
      stroke: "var(--card)",
      strokeWidth: 2
    } : {
      fill: "var(--card)",
      stroke: "var(--accent)",
      strokeWidth: 2
    }
  }), /*#__PURE__*/React.createElement("text", {
    x: lx,
    y: ya,
    style: {
      fontSize: fs,
      fill: "var(--accent)",
      fontWeight: 600
    }
  }, "You " + Math.round(CA[n - 1])), /*#__PURE__*/React.createElement("text", {
    x: lx,
    y: yb,
    style: {
      fontSize: fs,
      fill: "var(--mute)"
    }
  }, nm + " " + Math.round(CB[n - 1])), (() => {
    const sy = Math.max(ya, yb) + 26,
      gx = lx + (W - lx) / 2 - 4,
      lab = {
        fontSize: fs - 1,
        fill: "var(--mute)"
      },
      val = {
        fontSize: fs,
        fill: "var(--ink)",
        fontWeight: 600
      };
    return /*#__PURE__*/React.createElement("g", null, sy + 50 < base ? /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("text", {
      x: lx,
      y: sy,
      style: lab
    }, up ? "Games" : "Games left"), /*#__PURE__*/React.createElement("text", {
      x: lx,
      y: sy + 15,
      style: val
    }, (up ? totG(X) : X.used) + "–" + (up ? totG(Y) : Y.used)), /*#__PURE__*/React.createElement("text", {
      x: lx,
      y: sy + 36,
      style: lab
    }, done ? "Days won" : "Days ahead"), /*#__PURE__*/React.createElement("text", {
      x: lx,
      y: sy + 51,
      style: val
    }, won + " of " + (done || n))) : null, /*#__PURE__*/React.createElement("text", {
      x: gx,
      y: 192,
      textAnchor: "middle",
      style: {
        fontSize: fs,
        fill: "var(--ink)",
        fontWeight: 600
      }
    }, "Week"), narrow ? /*#__PURE__*/React.createElement("text", {
      x: gx,
      y: 208,
      textAnchor: "middle",
      style: {
        fontSize: fs,
        fill: CA[n - 1] > CB[n - 1] ? "var(--good)" : "var(--ink2)",
        fontWeight: 600
      }
    }, Math.round(CA[n - 1])) : /*#__PURE__*/React.createElement("text", {
      x: gx,
      y: 209,
      textAnchor: "middle",
      style: {
        fontSize: fs,
        fill: CA[n - 1] > CB[n - 1] ? "var(--good)" : "var(--ink2)",
        fontWeight: 600
      }
    }, Math.round(CA[n - 1]) + "–" + Math.round(CB[n - 1])), narrow ? /*#__PURE__*/React.createElement("text", {
      x: gx,
      y: 223,
      textAnchor: "middle",
      style: {
        fontSize: fs,
        fill: "var(--mute)",
        fontWeight: 600
      }
    }, Math.round(CB[n - 1])) : null, gxGopt105() === "text" ? /*#__PURE__*/React.createElement("text", {
      x: gx,
      y: Hh - 4,
      textAnchor: "middle",
      style: {
        fontSize: fs - 1,
        fill: "var(--mute)"
      }
    }, totG(X) + "–" + totG(Y)) : null);
  })(), dates.map((dt, d) => {
    const on = d === d0,
      win = me[d] > th[d] + 0.05;
    return /*#__PURE__*/React.createElement("g", {
      key: dt
    }, /*#__PURE__*/React.createElement("text", {
      x: cx(d),
      y: 192,
      textAnchor: "middle",
      style: {
        fontSize: fs,
        fill: on ? "var(--ink)" : "var(--mute)",
        fontWeight: on ? 600 : 400
      }
    }, DN(d)), narrow ? /*#__PURE__*/React.createElement("text", {
      x: cx(d),
      y: 208,
      textAnchor: "middle",
      style: {
        fontSize: fs,
        fill: win ? "var(--good)" : "var(--ink2)"
      }
    }, Math.round(me[d])) : /*#__PURE__*/React.createElement("text", {
      x: cx(d),
      y: 209,
      textAnchor: "middle",
      style: {
        fontSize: fs,
        fill: win ? "var(--good)" : "var(--ink2)"
      }
    }, Math.round(me[d]) + "\u2013" + Math.round(th[d])), narrow ? /*#__PURE__*/React.createElement("text", {
      x: cx(d),
      y: 223,
      textAnchor: "middle",
      style: {
        fontSize: fs,
        fill: "var(--mute)"
      }
    }, Math.round(th[d])) : null, gxGopt105() === "text" ? /*#__PURE__*/React.createElement("text", {
      x: cx(d),
      y: Hh - 4,
      textAnchor: "middle",
      style: {
        fontSize: fs - 1,
        fill: "var(--mute)"
      }
    }, gms(X, d) + "\u2013" + gms(Y, d)) : null, /*#__PURE__*/React.createElement("rect", {
      x: cx(d) - cw / 2,
      y: 0,
      width: cw,
      height: Hh,
      style: {
        fill: "transparent",
        cursor: "pointer"
      },
      onClick: () => setSel(d)
    }));
  })), /*#__PURE__*/React.createElement("div", {
    className: "gx-rf",
    style: {
      display: "none"
    }
  }, facts), /*#__PURE__*/React.createElement("div", {
    className: "gx-rt",
    style: {
      display: "none"
    }
  }, /*#__PURE__*/React.createElement("span", {
    className: "l"
  }, dayLabel(dates[d0])), /*#__PURE__*/React.createElement("span", {
    style: {
      color: "var(--accent)",
      fontWeight: 600
    }
  }, "You"), /*#__PURE__*/React.createElement("span", {
    className: "text-slate-500 truncate"
  }, teamName(s, opp)), k0 === "f" ? /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("span", {
    className: "l"
  }, "Points"), /*#__PURE__*/React.createElement("span", null, f1(me[d0]) + " ", /*#__PURE__*/React.createElement("span", {
    style: mc(m0)
  }, (m0 >= 0 ? "won by " : "lost by ") + f1(Math.abs(m0)))), /*#__PURE__*/React.createElement("span", null, f1(th[d0])), /*#__PURE__*/React.createElement("span", {
    className: "l"
  }, "Original"), /*#__PURE__*/React.createElement("span", null, f1(exp(X, d0))), /*#__PURE__*/React.createElement("span", null, f1(exp(Y, d0))), /*#__PURE__*/React.createElement("span", {
    className: "l"
  }, "Vs expected"), /*#__PURE__*/React.createElement("span", {
    style: mc(me[d0] - exp(X, d0))
  }, sg(me[d0] - exp(X, d0))), /*#__PURE__*/React.createElement("span", {
    style: mc(th[d0] - exp(Y, d0))
  }, sg(th[d0] - exp(Y, d0)))) : null, k0 === "t" ? /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("span", {
    className: "l"
  }, "So far"), /*#__PURE__*/React.createElement("span", null, f1(x0.act || 0)), /*#__PURE__*/React.createElement("span", null, f1(y0.act || 0)), /*#__PURE__*/React.createElement("span", {
    className: "l"
  }, "Projected now"), /*#__PURE__*/React.createElement("span", null, f1(me[d0]) + " ", /*#__PURE__*/React.createElement("span", {
    style: mc(m0)
  }, (m0 >= 0 ? "ahead by " : "behind by ") + f1(Math.abs(m0)))), /*#__PURE__*/React.createElement("span", null, f1(th[d0])), /*#__PURE__*/React.createElement("span", {
    className: "l"
  }, "Original"), /*#__PURE__*/React.createElement("span", null, f1(exp(X, d0)) + " ", /*#__PURE__*/React.createElement("span", {
    style: mc(exp(X, d0) - exp(Y, d0))
  }, (exp(X, d0) - exp(Y, d0) >= 0 ? "ahead by " : "behind by ") + f1(Math.abs(exp(X, d0) - exp(Y, d0))))), /*#__PURE__*/React.createElement("span", null, f1(exp(Y, d0)))) : null /* gx094 */, k0 === "p" ? /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("span", {
    className: "l"
  }, "Projected"), /*#__PURE__*/React.createElement("span", null, f1(me[d0]) + " ", /*#__PURE__*/React.createElement("span", {
    style: mc(m0)
  }, (m0 >= 0 ? "ahead by " : "behind by ") + f1(Math.abs(m0)))), /*#__PURE__*/React.createElement("span", null, f1(th[d0]))) : null, /*#__PURE__*/React.createElement("span", {
    className: "l"
  }, "Lineup games"), /*#__PURE__*/React.createElement("span", null, gms(X, d0)), /*#__PURE__*/React.createElement("span", null, gms(Y, d0)), k0 === "p" ? /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("span", {
    className: "l"
  }, "Top pick"), /*#__PURE__*/React.createElement("span", {
    className: "truncate"
  }, topOf(x0)), /*#__PURE__*/React.createElement("span", {
    className: "truncate"
  }, topOf(y0))) : null));
}

// ---------- change 072: page addresses and links that open in a new tab (install.py) ----------
const GX_RT = ["today", "matchup", "myteam", "moves", "lines", "league", "teams", "news", "setup"];
const GX_RDEF = {
  moves: "adddrop",
  league: "power",
  setup: "settings"
};
const GX_TEAM_HREF = {
  roster: "#myteam",
  pickups: "#moves",
  plan: "#moves/planner",
  trades: "#moves/trades",
  lines: "#lines"
};
const gxHash = (tab, sub, team, pid) => {
  const t = GX_RT.indexOf(tab) >= 0 ? tab : "today";
  let h = "#" + t;
  if (GX_RDEF[t] && sub && sub !== GX_RDEF[t]) h += "/" + sub;
  if (t === "teams" && team) h += "/" + team;
  if (pid) h += "&p=" + encodeURIComponent(pid);
  return h;
};
const gxParseHash = h => {
  const m = String(h || "").replace(/^#\/?/, "").split("&p=");
  const parts = m[0].split("/").filter(Boolean),
    tab = parts[0];
  if (!tab || GX_RT.indexOf(tab) < 0) return null;
  const r = {
    tab,
    sub: null,
    team: null,
    pid: m[1] ? decodeURIComponent(m[1]) : null
  };
  if (tab === "teams") r.team = parts[1] || null;else if (GX_RDEF[tab]) r.sub = parts[1] || GX_RDEF[tab];
  return r;
};
const gxNewTab = e => !!(e && (e.metaKey || e.ctrlKey || e.shiftKey || e.button === 1));
const gxPHref = p => {
  const R = window.__ROUTE || {};
  return gxHash(R.tab, R.sub, R.team, p && p.id);
};

// ---------- change 073: settings sync between devices (install.py) ----------
const GX_SYNC_K = "gm-sync-key",
  GX_SYNC_AT = "gm-sync-at";
const GX_SYNC_API = "https://api.github.com/repos/dhaliwal32/23456789786634356/contents/settings.json";
const GX_SYNC_SET = ["pmode", "pbest", "minGain", "protectTop", "minF", "minD", "minGo", "blend", "autoDone", "autoGoalie", "gw", "poStart", "poWeeks"];
const gxSyncKey = () => {
  try {
    return localStorage.getItem(GX_SYNC_K) || "";
  } catch (e) {
    return "";
  }
};
const gxSyncNote = t => {
  window.__SYNC_ST = t;
  window.dispatchEvent(new Event("gx-sync"));
};
const gxSyncPick = s => {
  const set = {},
    keep = [],
    back = {};
  GX_SYNC_SET.forEach(k => {
    if (s[k] !== undefined) set[k] = s[k];
  });
  if (s.pbest) delete set.pmode;
  (s.players || []).forEach(p => {
    if (p.keep) keep.push(p.id);
    if (p.back && p.back !== (DEFAULT_BACK[p.n] || "")) back[p.id] = p.back;
  });
  let watch = [];
  try {
    watch = JSON.parse(localStorage.getItem("gm-watch") || "[]") || [];
  } catch (e) {}
  return {
    set,
    keep,
    back,
    watch,
    hide: gxHide.list() /* gx075-s1 */,
    theme: window.__themePref ? window.__themePref() : "auto"
  };
};
const gxSyncSig = P => {
  const srt = o => {
    const x = {};
    Object.keys(o || {}).sort().forEach(k => x[k] = o[k]);
    return x;
  };
  return JSON.stringify([srt(P.set), (P.keep || []).slice().sort(), srt(P.back), (P.watch || []).slice().sort(), (P.hide || []).slice().sort() /* gx075-s2 */, P.theme || "auto"]);
};
const gxSyncApply = (st, R) => {
  const next = {
      ...st
    },
    keep = new Set(R.keep || []),
    back = R.back || {};
  GX_SYNC_SET.forEach(k => {
    if (R.set && R.set[k] !== undefined) next[k] = R.set[k];
  });
  next.players = (st.players || []).map(p => {
    const def = DEFAULT_BACK[p.n] || "";
    const b = back[p.id] != null ? back[p.id] : p.back && p.back !== def ? def : p.back;
    const k = keep.has(p.id);
    return !!p.keep === k && b === p.back ? p : {
      ...p,
      keep: k,
      back: b
    };
  });
  return next;
};
const gxB64 = str => btoa(unescape(encodeURIComponent(str)));
const gxUnB64 = b => decodeURIComponent(escape(atob(String(b || "").replace(/\s/g, ""))));
function GxSync({
  s,
  setS
}) {
  const [, tick] = useState(0);
  const sha = React.useRef(null),
    last = React.useRef(null),
    timer = React.useRef(null),
    ready = React.useRef(false),
    sRef = React.useRef(s);
  sRef.current = s;
  useEffect(() => {
    const h = () => tick(x => x + 1);
    window.addEventListener("gm-watch", h);
    window.addEventListener("gm-theme", h);
    window.addEventListener("gm-hide", h); /* gx075-s4 */
    return () => {
      window.removeEventListener("gm-watch", h);
      window.removeEventListener("gm-theme", h);
    };
  }, []);
  const hdr = key => ({
    Authorization: "Bearer " + key,
    Accept: "application/vnd.github+json"
  });
  const pull = () => {
    const key = gxSyncKey();
    const req = key ? fetch(GX_SYNC_API + "?ref=main&t=" + Date.now(), {
      headers: hdr(key),
      cache: "no-store"
    }).then(r => {
      if (r.status === 404) {
        sha.current = null;
        return null;
      }
      if (r.status === 401 || r.status === 403) throw new Error("key");
      if (!r.ok) throw new Error("net");
      return r.json().then(j => {
        sha.current = j.sha;
        return JSON.parse(gxUnB64(j.content));
      });
    }) : fetch("settings.json?t=" + Date.now(), {
      cache: "no-store"
    }).then(r => r.ok ? r.json() : null);
    return req.then(R => {
      if (!R || !R.at) {
        if (key) gxSyncNote("On \u00b7 nothing saved yet");
        return false;
      }
      let seen = "";
      try {
        seen = localStorage.getItem(GX_SYNC_AT) || "";
      } catch (e) {}
      last.current = gxSyncSig(R);
      if (key) gxSyncNote("On \u00b7 last change " + gxWhen(R.at));
      if (R.at <= seen) return false;
      try {
        localStorage.setItem(GX_SYNC_AT, R.at);
      } catch (e) {}
      setS(st => gxSyncApply(st, R));
      if (Array.isArray(R.hide)) gxHide.set(R.hide); /* gx075-s3 */
      if (Array.isArray(R.watch)) {
        try {
          localStorage.setItem("gm-watch", JSON.stringify(R.watch));
        } catch (e) {}
        window.dispatchEvent(new Event("gm-watch"));
      }
      if (R.theme && window.__themePref && window.__setTheme && window.__themePref() !== R.theme) window.__setTheme(R.theme);
      return true;
    }).catch(e => {
      if (key) gxSyncNote(e && e.message === "key" ? "GitHub refused the key. It needs Contents: Read and write on this repo." : "Could not reach GitHub. Trying again in 2 minutes.");
      return true;
    });
  };
  const push = () => {
    const key = gxSyncKey();
    if (!key || !ready.current) return;
    const P = gxSyncPick(sRef.current),
      sig = gxSyncSig(P);
    if (sig === last.current) return;
    const body = {
      ...P,
      at: new Date().toISOString()
    };
    const put = again => fetch(GX_SYNC_API, {
      method: "PUT",
      headers: {
        ...hdr(key),
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        message: "Settings saved from the app",
        content: gxB64(JSON.stringify(body, null, 1) + "\n"),
        branch: "main",
        ...(sha.current ? {
          sha: sha.current
        } : {})
      })
    }).then(r => {
      if ((r.status === 409 || r.status === 422) && again) {
        return fetch(GX_SYNC_API + "?ref=main&t=" + Date.now(), {
          headers: hdr(key),
          cache: "no-store"
        }).then(g => g.ok ? g.json() : null).then(j => {
          sha.current = j ? j.sha : null;
          return put(false);
        });
      }
      if (!r.ok) {
        gxSyncNote(r.status === 401 || r.status === 403 ? "GitHub refused the key. It needs Contents: Read and write on this repo." : "Saving failed (" + r.status + "). Trying again in 2 minutes.");
        return;
      }
      return r.json().then(j => {
        sha.current = j && j.content ? j.content.sha : null;
        last.current = sig;
        try {
          localStorage.setItem(GX_SYNC_AT, body.at);
        } catch (e) {}
        gxSyncNote("On \u00b7 saved " + gxWhen(body.at));
      });
    });
    return put(true).catch(() => gxSyncNote("Could not reach GitHub. Trying again in 2 minutes."));
  };
  useEffect(() => {
    let busy = false;
    const cycle = () => {
      if (busy) return;
      busy = true;
      pull().then(applied => {
        ready.current = true;
        busy = false;
        if (!applied) push();
      });
    };
    cycle();
    const id = setInterval(cycle, 2 * 60 * 1000);
    const vis = () => {
      if (document.visibilityState === "visible") cycle();
    };
    document.addEventListener("visibilitychange", vis);
    window.addEventListener("gx-sync-now", cycle);
    return () => {
      clearInterval(id);
      document.removeEventListener("visibilitychange", vis);
      window.removeEventListener("gx-sync-now", cycle);
    };
  }, []);
  const sig = gxSyncSig(gxSyncPick(s));
  useEffect(() => {
    if (!ready.current || !gxSyncKey() || sig === last.current) return;
    clearTimeout(timer.current);
    timer.current = setTimeout(push, 4000);
    return () => clearTimeout(timer.current);
  }, [sig]);
  return null;
}
function GxSyncRow() {
  const [, tick] = useState(0);
  const [key, setKey] = useState("");
  const [edit, setEdit] = useState(false);
  useEffect(() => {
    const h = () => tick(x => x + 1);
    window.addEventListener("gx-sync", h);
    return () => window.removeEventListener("gx-sync", h);
  }, []);
  const has = !!gxSyncKey(),
    st = window.__SYNC_ST || "";
  const btn = "border border-slate-300 rounded-lg px-3 py-1 text-sm";
  const save = () => {
    const v = key.trim();
    if (!v) return;
    try {
      localStorage.setItem(GX_SYNC_K, v);
    } catch (e) {}
    setKey("");
    setEdit(false);
    gxSyncNote("Key saved. Syncing...");
    window.dispatchEvent(new Event("gx-sync-now"));
  };
  const off = () => {
    try {
      localStorage.removeItem(GX_SYNC_K);
    } catch (e) {}
    gxSyncNote("");
  };
  return /*#__PURE__*/React.createElement("div", {
    className: "gx-sr"
  }, /*#__PURE__*/React.createElement("span", {
    className: "min-w-0"
  }, /*#__PURE__*/React.createElement("span", {
    className: "block"
  }, "Sync between devices"), /*#__PURE__*/React.createElement("span", {
    className: "block text-xs text-slate-500"
  }, has ? st || "On" : "Off on this device. Turn on and paste your GitHub key.")), edit ? /*#__PURE__*/React.createElement("span", {
    className: "flex gap-2 items-center"
  }, /*#__PURE__*/React.createElement("input", {
    type: "password",
    autoComplete: "off",
    className: inp + " text-sm",
    style: {
      width: 170
    },
    placeholder: "Paste the key",
    value: key,
    onChange: e => setKey(e.target.value)
  }), /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: btn,
    onClick: save
  }, "Save")) : /*#__PURE__*/React.createElement("span", {
    className: "flex gap-2 items-center"
  }, has ? /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: btn,
    onClick: () => window.dispatchEvent(new Event("gx-sync-now"))
  }, "Sync now") : null, /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: btn,
    onClick: () => has ? off() : setEdit(true)
  }, has ? "Turn off" : "Turn on")));
}

// ---------- change 075: hide players from pickup suggestions (install.py) ----------
let __GXH = {
  raw: null,
  set: new Set()
};
const gxHideSet = () => {
  let raw = "[]";
  try {
    raw = localStorage.getItem("gm-hide") || "[]";
  } catch (e) {}
  if (raw !== __GXH.raw) {
    let a = [];
    try {
      a = JSON.parse(raw) || [];
    } catch (e) {}
    __GXH = {
      raw,
      set: new Set(a)
    };
  }
  return __GXH.set;
};
const gxHide = {
  list: () => [...gxHideSet()],
  set: l => {
    const raw = JSON.stringify((l || []).slice().sort());
    let old = "[]";
    try {
      old = localStorage.getItem("gm-hide") || "[]";
    } catch (e) {}
    if (raw === old) return;
    try {
      localStorage.setItem("gm-hide", raw);
    } catch (e) {}
    window.dispatchEvent(new Event("gm-hide"));
  },
  toggle: id => {
    const l = gxHide.list(),
      i = l.indexOf(id);
    if (i >= 0) l.splice(i, 1);else l.push(id);
    gxHide.set(l);
  }
};
function gxUseHide() {
  const [v, setV] = useState(0);
  useEffect(() => {
    const h = () => setV(x => x + 1);
    window.addEventListener("gm-hide", h);
    return () => window.removeEventListener("gm-hide", h);
  }, []);
  return v;
}
// skaters who are healthy but not in their team's current lineup (Daily Faceoff), only when the full lineup is known
const gxLK = x => nrm(x).replace(/[.'\u2019]/g, "").replace(/-/g, " ").replace(/\s+/g, " ").trim();
let __GXL = {
  L: null,
  m: null
};
const gxLineupSets = () => {
  const L = window.LINES_DATA;
  if (!L || !L.teams) return null;
  if (__GXL.L === L && __GXL.m) return __GXL.m;
  const m = {};
  Object.entries(L.teams).forEach(([t, x]) => {
    const ln = (x || {}).lines || {},
      names = [];
    ["F1", "F2", "F3", "F4", "D1", "D2", "D3"].forEach(sl => (ln[sl] || []).forEach(n => names.push(gxLK(n))));
    if (names.length >= 15) m[t] = new Set(names);
  });
  __GXL = {
    L,
    m
  };
  return m;
};
const gxScratch = p => {
  if (!p || p.p === "G" || p.ir) return false;
  const m = gxLineupSets(),
    set = m && m[p.t];
  if (!set) return false;
  if (avail(p, todayISO()) === 0) return false;
  return !set.has(gxLK(p.n));
};
const goalieOut = p => gxGoalieOut0(p) || !!p && (gxHideSet().has(p.id) || gxScratch(p));
function GxHiddenPanel({
  s
}) {
  gxUseHide();
  const [open, setOpen] = useState(false);
  const K = s.blend;
  const list = gxHide.list().map(id => s.players.find(p => p.id === id)).filter(Boolean);
  if (!list.length) return null;
  return /*#__PURE__*/React.createElement("div", {
    className: "gx-pn"
  }, /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: "text-sm text-slate-500",
    onClick: () => setOpen(!open)
  }, list.length + " player" + (list.length === 1 ? "" : "s") + " hidden from suggestions \u00b7 ", /*#__PURE__*/React.createElement("span", {
    className: "text-blue-600"
  }, open ? "Close" : "Show")), open ? list.map(p => /*#__PURE__*/React.createElement("div", {
    key: p.id,
    className: "gx-row"
  }, /*#__PURE__*/React.createElement(GxFace, {
    p: p,
    size: 22
  }), /*#__PURE__*/React.createElement("span", {
    className: "min-w-0 truncate",
    style: {
      flex: 1
    }
  }, /*#__PURE__*/React.createElement(PN, {
    p: p,
    className: ""
  }), " ", /*#__PURE__*/React.createElement("span", {
    className: "text-xs text-slate-500"
  }, p.p + (p.ft !== "fa" ? " \u00b7 " + teamName(s, p.ft) : ""))), /*#__PURE__*/React.createElement("span", {
    style: {
      fontVariantNumeric: "tabular-nums"
    }
  }, f1(effAvg(p, K))), /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: "text-sm text-blue-600",
    style: {
      marginLeft: 8
    },
    onClick: () => gxHide.toggle(p.id)
  }, "Show again"))) : null, open ? /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500",
    style: {
      marginTop: 8
    }
  }, "Hidden players also stay out of the Plan, Advice and trade ideas. Searching a name still finds them.") : null);
}

// ---------- change 078: player rankings for the whole league, and trades between any two teams (install.py) ----------
const gxYou = (s, you, other) => !window.__TB_REAL || s.me === window.__TB_REAL ? you : other;
function GxRankings({
  s
}) {
  gxUseSort108(); /* gx109 */
  const K = s.blend;
  const [pos, setPos] = useState("F");
  const [own, setOwn] = useState("all");
  const [q, setQ] = useState("");
  const [sort, setSort] = useState("exp");
  const [n, setN] = useState(50);
  const pv = p => effAvg(p, K) * (p.p === "G" ? p.prob : 1);
  const rank = useMemo(() => {
    const o = {};
    ["F", "D", "G"].forEach(k => {
      s.players.filter(p => p.p === k && p.prob > 0 && (p.proj !== false || p.gp > 0)).map(p => [p.id, pv(p)]).sort((a, b) => b[1] - a[1]).forEach((x, i) => o[x[0]] = i + 1);
    });
    return o;
  }, [s.players, K, window.__PMODE]);
  const qq = nrm(q);
  const rows = s.players.filter(p => p.p === pos && rank[p.id] && (own === "all" || (own === "rost" ? p.ft !== "fa" : own === "fa" ? p.ft === "fa" : p.ft === own)) && (!qq || nrm(p.n).includes(qq))).map(p => ({
    p,
    rk: rank[p.id],
    e: pv(p),
    sf: p.gp ? p.tot / p.gp : null
  })).sort((a, b) => sort === "exp" ? a.rk - b.rk : sort === "gp" ? (b.p.gp || 0) - (a.p.gp || 0) || a.rk - b.rk : sort === "sf" ? (b.sf == null ? -99 : b.sf) - (a.sf == null ? -99 : a.sf) : (b.p.tot || 0) - (a.p.tot || 0));
  const shown = gxSort108(rows, s, x => x.p).slice(0, n);
  const stTag = p => p.ir ? "IR" : p.status && p.status !== "ACTIVE" ? M_ST[p.status] || p.status.replace(/_/g, " ") : "";
  const owner = p => p.ft === "fa" ? /*#__PURE__*/React.createElement("span", {
    className: "text-slate-500"
  }, p.wv ? "Waivers" : "Free agent") : /*#__PURE__*/React.createElement(TL, {
    s: s,
    id: p.ft,
    className: p.ft === s.me ? "font-semibold" : ""
  });
  const HB = (k, l, cls) => /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: "n " + (cls || "") + (sort === k ? " on" : ""),
    onClick: () => {
      setSort(k);
      setN(50);
    }
  }, l);
  const PN78 = {
    F: "forwards",
    D: "defencemen",
    G: "goalies"
  };
  return /*#__PURE__*/React.createElement("div", {
    className: "space-y-3",
    "data-c78": "rank"
  }, /*#__PURE__*/React.createElement("div", {
    className: "flex flex-wrap items-center gap-2"
  }, /*#__PURE__*/React.createElement("span", {
    className: "gx-seg"
  }, [["F", "Forwards"], ["D", "Defence"], ["G", "Goalies"]].map(([k, l]) => /*#__PURE__*/React.createElement("button", {
    key: k,
    type: "button",
    className: pos === k ? "on" : "",
    onClick: () => {
      setPos(k);
      setN(50);
    }
  }, l))), /*#__PURE__*/React.createElement("select", {
    className: inp,
    value: own,
    onChange: e => {
      setOwn(e.target.value);
      setN(50);
    }
  }, /*#__PURE__*/React.createElement("option", {
    value: "all"
  }, "Every player"), /*#__PURE__*/React.createElement("option", {
    value: "rost"
  }, "On a fantasy team"), /*#__PURE__*/React.createElement("option", {
    value: "fa"
  }, "Free agents"), s.teams.map(t => /*#__PURE__*/React.createElement("option", {
    key: t.id,
    value: t.id
  }, t.name, t.id === s.me ? " (you)" : ""))), /*#__PURE__*/React.createElement("input", {
    className: inp + " flex-1 min-w-[140px]",
    placeholder: "Search a player",
    value: q,
    onChange: e => {
      setQ(e.target.value);
      setN(50);
    }
  })), /*#__PURE__*/React.createElement("div", {
    className: "gx-pn"
  }, /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement(GxRngSel100, null), /*#__PURE__*/React.createElement("div", {
    className: "gx-sc99 gx-rk106"
  }, /*#__PURE__*/React.createElement("div", {
    className: "gx-rk gx-rkh"
  }, /*#__PURE__*/React.createElement("span", null, "#"), /*#__PURE__*/React.createElement("span", null), /*#__PURE__*/React.createElement("span", null, "Player"), /*#__PURE__*/React.createElement("span", {
    className: "m-hide"
  }, "Fantasy team"), HB("gp", "GP", "m-hide"), HB("sf", "Avg"), HB("exp", "Expected"), /*#__PURE__*/React.createElement(GxSH106, {
    mode: pos === "G" ? "go" : "sk"
  })), shown.map(({
    p,
    rk,
    e,
    sf
  }) => {
    const me = p.ft === s.me,
      st = stTag(p);
    return /*#__PURE__*/React.createElement("div", {
      key: p.id,
      className: "gx-rk" + (me ? " me" : "")
    }, /*#__PURE__*/React.createElement("span", {
      className: "text-slate-500",
      style: {
        paddingLeft: 4
      }
    }, rk), /*#__PURE__*/React.createElement(GxFace, {
      p: p,
      size: 22
    }), /*#__PURE__*/React.createElement("div", {
      className: "min-w-0"
    }, /*#__PURE__*/React.createElement("div", {
      className: "truncate"
    }, /*#__PURE__*/React.createElement(PN, {
      p: p,
      className: me ? "font-semibold" : ""
    }), st ? /*#__PURE__*/React.createElement("span", {
      className: "text-xs",
      style: {
        color: "var(--bad)",
        marginLeft: 8
      }
    }, st) : null), /*#__PURE__*/React.createElement("div", {
      className: "text-xs text-slate-500 truncate"
    }, /*#__PURE__*/React.createElement("span", {
      className: "m-inl"
    }, owner(p), " · "), p.t, sort === "tot" ? " · " + f1(p.tot) + " pts" : "")), /*#__PURE__*/React.createElement("span", {
      className: "truncate text-sm m-hide"
    }, owner(p)), /*#__PURE__*/React.createElement("span", {
      className: "n text-slate-500 m-hide"
    }, p.gp || "–"), /*#__PURE__*/React.createElement("span", {
      className: "n"
    }, sf == null ? "–" : f1(sf)), /*#__PURE__*/React.createElement("span", {
      className: "n font-semibold"
    }, f1(e)), /*#__PURE__*/React.createElement(GxSC106, {
      p: p,
      s: s,
      mode: "full"
    }));
  }), !shown.length ? /*#__PURE__*/React.createElement("div", {
    className: "text-sm text-slate-500",
    style: {
      padding: "10px 0"
    }
  }, "No ", PN78[pos], " match.") : null), rows.length > shown.length ? /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: "text-sm text-blue-600",
    style: {
      marginTop: 10
    },
    onClick: () => setN(n + 50)
  }, "Show 50 more (" + (rows.length - shown.length) + " left)") : null, /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500",
    style: {
      display: "none"
    }
  }, "Rank is each player's place among all ", PN78[pos], " by expected points a game", pos === "G" ? ", weighted by how often he starts" : "", ", the same rank shown on team pages. So far is his average this season. ", /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: "text-blue-600",
    onClick: () => {
      setSort(sort === "tot" ? "exp" : "tot");
      setN(50);
    }
  }, sort === "tot" ? "Back to rank order" : "Sort by season total"))));
}
// ---------- change 079: tap a heading to sort (install.py) ----------
// first tap: highest first; tap the same heading again: back to the normal order
const GxSH = ({
  k,
  cur,
  set,
  def,
  cls,
  children
}) => /*#__PURE__*/React.createElement("button", {
  type: "button",
  className: "n gx-sh " + (cls || "") + (cur === k ? " on" : ""),
  title: "Tap to sort, highest first",
  onClick: e => {
    e.stopPropagation();
    set(cur === k ? def : k);
  }
}, children);
const gxL5v = h => {
  const a = (h || []).map(x => typeof x === "number" ? x : x && x.v).filter(x => x != null);
  return a.length ? a.reduce((s, x) => s + x, 0) / a.length : -99;
};
// ---------- change 081: trades take 3 days to go through (install.py) ----------
const GX_TRADE_DAYS = 3;
const gxTradeDay = () => addDays(todayISO(), GX_TRADE_DAYS);
// a roster that keeps its old players until the trade day and has the new ones from that day on
const gxTimed = (before, after, day) => {
  const was = new Set(before.map(p => p.id)),
    now = new Set(after.map(p => p.id));
  return before.filter(p => !now.has(p.id)).map(p => ({
    ...p,
    untilD: day
  })).concat(after.map(p => was.has(p.id) ? p : {
    ...p,
    fromD: day
  }));
};
// ---------- change 082: trade result under each projection (install.py) ----------
const GX_PM82 = [["espn", "ESPN"], ["model", "GM model"], ["blend", "Blend"], ["ai", "AI"]];
const gxCanMode82 = k => k === "espn" || !!window.__MODEL && (k !== "ai" || !!window.__AI);
// run fn with a different projection, then put the app's projection back
const gxWithMode82 = (m, fn) => {
  const prev = window.__PMODE;
  if (!m || m === prev || !gxCanMode82(m)) return fn();
  window.__PMODE = m;
  try {
    return fn();
  } finally {
    window.__PMODE = prev;
  }
};
const gxPct82 = (b, a) => {
  if (b == null || a == null) return "–";
  const d = Math.round(a * 100) - Math.round(b * 100);
  return (d > 0 ? "+" : "") + d + "%";
};
function GxTradeModes82({
  res,
  cmp,
  tm,
  setTm,
  part
}) {
  const app = window.__PMODE,
    cur = res.mode82,
    lbl = k => (GX_PM82.find(x => x[0] === k) || [k, k])[1];
  const sg = v => (v >= 0 ? "+" : "") + Math.round(v);
  if (part === "pick") return /*#__PURE__*/React.createElement("div", {
    className: "gx-pmh82"
  }, /*#__PURE__*/React.createElement("span", {
    className: "text-xs text-slate-500"
  }, "Projection"), /*#__PURE__*/React.createElement("span", {
    className: "gx-seg"
  }, GX_PM82.map(([k, l]) => /*#__PURE__*/React.createElement("button", {
    key: k,
    type: "button",
    disabled: !gxCanMode82(k),
    className: cur === k ? "on" : "",
    onClick: () => setTm(k === app ? null : k)
  }, l))), tm && tm !== app ? /*#__PURE__*/React.createElement("span", {
    className: "text-xs text-slate-500"
  }, "Trades only. The rest of the app still uses ", lbl(app), ".") : null);
  return /*#__PURE__*/React.createElement("div", {
    style: {
      marginTop: 12
    }
  }, /*#__PURE__*/React.createElement("div", {
    className: "gx-tag",
    style: {
      marginBottom: 4
    }
  }, "Every projection"), /*#__PURE__*/React.createElement("div", {
    className: "gx-pm82 h"
  }, /*#__PURE__*/React.createElement("span", null, "Projection"), /*#__PURE__*/React.createElement("span", null, "You"), /*#__PURE__*/React.createElement("span", {
    className: "m-hide"
  }, "Them"), /*#__PURE__*/React.createElement("span", {
    className: "m-hide"
  }, "This week"), /*#__PURE__*/React.createElement("span", null, "Next week"), /*#__PURE__*/React.createElement("span", null, "Result")), !cmp ? /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500",
    style: {
      padding: "8px 6px"
    }
  }, "Working out every projection...") : cmp.map(x => /*#__PURE__*/React.createElement("div", {
    key: x.k,
    className: "gx-pm82 r" + (x.k === cur ? " on" : ""),
    onClick: () => setTm(x.k === app ? null : x.k),
    title: "Show the trade with this projection"
  }, /*#__PURE__*/React.createElement("span", null, x.l, x.k === app ? /*#__PURE__*/React.createElement("span", {
    className: "text-xs text-slate-500"
  }, " (app)") : null), /*#__PURE__*/React.createElement("span", {
    style: {
      color: x.my >= 0 ? "var(--good)" : "var(--bad)"
    }
  }, sg(x.my)), /*#__PURE__*/React.createElement("span", {
    className: "m-hide",
    style: {
      color: x.th >= 0 ? "var(--good)" : "var(--bad)"
    }
  }, sg(x.th)), /*#__PURE__*/React.createElement("span", {
    className: "m-hide"
  }, gxPct82(x.tb, x.ta)), /*#__PURE__*/React.createElement("span", null, gxPct82(x.wb, x.wa)), /*#__PURE__*/React.createElement("span", {
    className: x.my > 0 ? "w" : "l"
  }, x.my > 0 ? "Win" : "Lose"))), /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500",
    style: {
      marginTop: 6
    }
  }, "Points are for the rest of the season. The weeks show the change in your chance to win. Win means your lineup gains points."));
}
// ---------- change 083: head start on next week when this week is decided (install.py) ----------
const GX_HS_SURE = 0.80;
const gxHsKey = s => "hs83:" + (((s.weeks || [])[s.wk] || {}).label || s.wk);
const gxHsMode = s => {
  const v = uiGet()[gxHsKey(s)];
  return v === "on" ? "on" : v === "off" || v === true ? "off" : "";
}; /* change 084 */
const gxHsAuto = base => base != null && (base >= GX_HS_SURE || base <= 1 - GX_HS_SURE);
const gxHsOff = s => gxHsMode(s) === "off";
const gxHsSet = (s, v) => {
  uiSet(gxHsKey(s), v);
  window.dispatchEvent(new Event("gx-hs83"));
};
const gxHsCan = (s, base, ml) => !!nextWkS(s) && ml > 0 && base != null;
const gxHsOn = (s, base, ml) => gxHsCan(s, base, ml) && (gxHsMode(s) === "on" || gxHsMode(s) === "" && gxHsAuto(base));
function gxUseHs() {
  const [n, setN] = useState(0);
  useEffect(() => {
    const h = () => setN(x => x + 1);
    window.addEventListener("gx-hs83", h);
    return () => window.removeEventListener("gx-hs83", h);
  }, []);
  return n;
}
function GxHsLine({
  s,
  base,
  ml
}) {
  gxUseHs();
  if (!gxHsCan(s, base, ml)) return null;
  const btn = {
    marginLeft: 6
  };
  if (!gxHsOn(s, base, ml)) return /*#__PURE__*/React.createElement("span", null, " ", /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: "text-blue-600 text-sm",
    style: btn,
    onClick: () => gxHsSet(s, "on")
  }, "Use them for next week instead"));
  const why084 = base >= GX_HS_SURE ? "You're " + wpTxt(base) + " to win this week, so they're aimed at next week." : base <= 1 - GX_HS_SURE ? "This week looks lost (" + wpTxt(base) + "), so they're aimed at next week." : "Aimed at next week by you (" + wpTxt(base) + " to win this week).";
  return /*#__PURE__*/React.createElement("span", {
    className: "text-slate-500"
  }, " " + why084, /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: "text-blue-600 text-sm",
    style: btn,
    onClick: () => gxHsSet(s, "off")
  }, "Keep them for this week"));
}
function GxHeadStart({
  s,
  base,
  ml
}) {
  const hsV = gxUseHs();
  const gxHideV = gxUseHide();
  const sN = nextWkS(s);
  const on = gxHsOn(s, base, ml);
  const baseN = useMemo(() => on ? winChance(sN) : null, [on, s]);
  const rows = useMemo(() => {
    if (!on || baseN == null) return [];
    const M = computeMoves(s, {
      H: 2,
      pos: "all",
      pool: 60
    });
    const out = [];
    M.res.slice(0, 30).forEach(r => {
      if (gxHideSet().has(r.f.id) || gxScratch(r.f)) return;
      const R = afterMove(s, r.f, r.d),
        now = winChance(s, R),
        nx = winChance(sN, R);
      if (now == null || nx == null || nx <= baseN + 0.004) return;
      if (base >= 0.5 && now < (gxHsAuto(base) ? Math.min(base, GX_HS_SURE) : base) - 0.03) return;
      out.push({
        ...r,
        now,
        nx
      });
    });
    return out.sort((a, b) => b.nx - a.nx || b.gain - a.gain).slice(0, 5);
  }, [on, s, baseN, gxHideV, hsV]);
  if (!on || baseN == null) return null;
  const wN = deriveWeek(sN.weeks[sN.wk], sN.autoDone),
    opp = oppOf(wN, s.me);
  return /*#__PURE__*/React.createElement("div", {
    className: "gx-pn"
  }, /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("div", {
    className: "gx-st"
  }, "Pickups for next week"), /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500",
    style: {
      marginTop: 2,
      marginBottom: 6
    }
  }, "Best adds for next week" + (opp ? " against " + teamName(s, opp) : "") + " (" + wpTxt(baseN) + " now). You still get 3 new moves next week."), rows.length ? /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    className: "gx-hs83 hd"
  }, /*#__PURE__*/React.createElement("span", null), /*#__PURE__*/React.createElement("span", null), /*#__PURE__*/React.createElement("span", {
    className: "n"
  }, "This wk"), /*#__PURE__*/React.createElement("span", {
    className: "n"
  }, "Next wk")), rows.map(r => /*#__PURE__*/React.createElement("div", {
    key: r.f.id,
    className: "gx-hs83"
  }, /*#__PURE__*/React.createElement(GxFace, {
    p: r.f,
    size: 26
  }), /*#__PURE__*/React.createElement("div", {
    className: "min-w-0"
  }, /*#__PURE__*/React.createElement("div", {
    className: "truncate"
  }, /*#__PURE__*/React.createElement(PN, {
    p: r.f,
    className: ""
  }), " ", /*#__PURE__*/React.createElement("span", {
    className: "text-xs text-slate-500"
  }, r.f.p), r.f.wv ? /*#__PURE__*/React.createElement("span", {
    className: "text-xs",
    style: {
      color: "var(--warn)",
      marginLeft: 6
    }
  }, "on waivers") : null), /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500"
  }, "Swap for " + r.d.n + " · ", /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: "text-blue-600",
    onClick: e => {
      e.stopPropagation();
      if (window.__QA) window.__QA.espn(r.f);
    }
  }, "Add on ESPN"), " · ", /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: "text-blue-600",
    onClick: e => {
      e.stopPropagation();
      gxHide.toggle(r.f.id);
    }
  }, "Hide"))), /*#__PURE__*/React.createElement("div", {
    className: "n",
    style: {
      color: r.now < base - 0.004 ? "var(--bad)" : "var(--ink)"
    }
  }, wpTxt(r.now)), /*#__PURE__*/React.createElement("div", {
    className: "n font-semibold",
    style: {
      color: "var(--good)"
    }
  }, wpTxt(r.nx))))) : /*#__PURE__*/React.createElement("div", {
    className: "text-sm text-slate-500",
    style: {
      padding: "6px 0"
    }
  }, "No free agent raises next week's win chance right now."));
}
// ---------- change 085: Injuries page under Team > Pickups (install.py) ----------
const gxIjDays = d => Math.round((fromIso(d) - fromIso(todayISO())) / 864e5);
const gxIjWhen = d => {
  const n = gxIjDays(d);
  return n < 0 ? "any day now" : n === 0 ? "today" : n === 1 ? "tomorrow" : "in " + n + " days";
};
const gxIjAgo = d => {
  const n = -gxIjDays(d);
  return n <= 0 ? "today" : n === 1 ? "yesterday" : mdL(d);
};
const gxIjLast = e => e.nd && e.nd > e.d ? e.nd : e.d;
const gxIjNote = n => n && n.length > 15 ? n : "";
function GxInjPage({
  s
}) {
  const effAvg = gxPgAvg; /* gx088-i */
  const [, tick] = useState(0);
  useEffect(() => {
    const h = () => tick(x => x + 1);
    window.addEventListener("gm-watch", h);
    return () => window.removeEventListener("gm-watch", h);
  }, []);
  const [who, setWho] = useState(() => uiGet()["ij85:who"] || "fa");
  const [pos, setPos] = useState("all");
  const [allP, setAllP] = useState(false);
  const [moreU, setMoreU] = useState(false);
  const [moreL, setMoreL] = useState(false);
  const [openN, setOpenN] = useState({});
  const K = s.blend;
  const pick = v => {
    setWho(v);
    uiSet("ij85:who", v);
  };
  const D = useMemo(() => {
    const S = window.__SIG || {},
      EV = S.injmoves || {};
    const val = p => effAvg(p, K); /* gx088-iv */
    const mine = s.players.filter(p => p.ft === s.me && !p.ir);
    const bar = {};
    ["F", "D", "G"].forEach(g => {
      const v = mine.filter(p => p.p === g).map(val);
      bar[g] = v.length ? Math.min(...v) : 0;
    });
    const list = [],
      ups = [];
    s.players.forEach(p => {
      const id = typeof p.id === "string" && p.id[0] === "e" ? p.id.slice(1) : null;
      const inj = autoInj(p),
        e = id ? EV[id] : null;
      if (!inj && !(e && e.k === "back")) return;
      const v = val(p),
        good = v > 0 && v >= bar[p.p];
      const r = {
        p,
        v,
        good,
        inj,
        e,
        back: inj ? effBack(p).d : ""
      };
      if (inj) list.push(r);
      if (e) ups.push(r);
    });
    return {
      list,
      ups
    };
  }, [s]);
  const inWho = r => who === "fa" ? r.p.ft === "fa" : who === "mine" ? r.p.ft === s.me : true;
  const keep = r => inWho(r) && (pos === "all" || r.p.p === pos) && (allP || who === "mine" || r.good);
  const ups = D.ups.filter(keep).sort((a, b) => gxIjLast(b.e).localeCompare(gxIjLast(a.e)) || b.v - a.v);
  const list = D.list.filter(keep).sort((a, b) => (a.back || "9").localeCompare(b.back || "9") || b.v - a.v);
  const groups = [["Back within a week", list.filter(r => r.back && gxIjDays(r.back) <= 7)], ["Back in 1 to 4 weeks", list.filter(r => r.back && gxIjDays(r.back) > 7 && gxIjDays(r.back) <= 30)], ["Out longer", list.filter(r => r.back && gxIjDays(r.back) > 30)], ["No return date", list.filter(r => !r.back)]];
  const evTxt = e => {
    if (e.k === "back") return /*#__PURE__*/React.createElement("span", {
      className: "up"
    }, "Off the injury list");
    if (e.k === "sooner") return /*#__PURE__*/React.createElement("span", {
      className: "up"
    }, "Back sooner: was " + mdL(e.was) + ", now " + mdL(e.now));
    if (e.k === "dtd") return /*#__PURE__*/React.createElement("span", {
      className: "up"
    }, "Now day-to-day (was " + (e.was || "out").replace("Injured Reserve", "IR") + ")");
    if (e.k === "later") return /*#__PURE__*/React.createElement("span", {
      className: "wn"
    }, "Pushed back: was " + mdL(e.was) + ", now " + mdL(e.now));
    if (e.k === "new") return /*#__PURE__*/React.createElement("span", {
      className: "dn"
    }, "Newly injured" + (e.now ? ", back about " + mdL(e.now) : ""));
    return /*#__PURE__*/React.createElement("span", null, "New injury news");
  };
  const owner = p => p.ft === "fa" ? "Free agent" : p.ft === s.me ? "Your team" : teamName(s, p.ft);
  const row = (r, i, upd) => {
    const st = r.inj ? (r.inj.status || "Out").replace("Injured Reserve", "IR") + (r.inj.type ? " · " + r.inj.type : "") + (r.back ? " · back " + mdL(r.back) + " (" + gxIjWhen(r.back) + ")" : "") : "Healthy now";
    const note = r.inj ? gxIjNote(r.inj.note) : "",
      nk = (upd ? "u" : "l") + r.p.id;
    return /*#__PURE__*/React.createElement("div", {
      key: nk,
      className: "gx-ij85" + (i ? "" : " first")
    }, /*#__PURE__*/React.createElement(GxFace, {
      p: r.p,
      size: 26
    }), /*#__PURE__*/React.createElement("div", {
      className: "min-w-0"
    }, /*#__PURE__*/React.createElement("div", {
      className: "truncate"
    }, /*#__PURE__*/React.createElement(PN, {
      p: r.p,
      className: ""
    }), " ", /*#__PURE__*/React.createElement("span", {
      className: "text-xs text-slate-500"
    }, r.p.p), r.good && allP && who !== "mine" ? /*#__PURE__*/React.createElement("span", {
      className: "good"
    }, "Good") : null, r.p.wv ? /*#__PURE__*/React.createElement("span", {
      className: "text-xs",
      style: {
        color: "var(--warn)",
        marginLeft: 6
      }
    }, "on waivers") : null), /*#__PURE__*/React.createElement("div", {
      className: "text-xs text-slate-500"
    }, (who === "fa" ? "" : owner(r.p) + " · ") + st), upd && r.e ? /*#__PURE__*/React.createElement("div", {
      className: "text-xs"
    }, evTxt(r.e), /*#__PURE__*/React.createElement("span", {
      className: "text-slate-500"
    }, " · " + gxIjAgo(gxIjLast(r.e)))) : !upd && r.e && r.e.k !== "news" ? /*#__PURE__*/React.createElement("div", {
      className: "text-xs"
    }, evTxt(r.e)) : null, /*#__PURE__*/React.createElement("div", {
      className: "text-xs text-slate-500"
    })), /*#__PURE__*/React.createElement("div", {
      className: "n"
    }, /*#__PURE__*/React.createElement("div", {
      className: "font-semibold"
    }, f1(effAvg(r.p, K))), /*#__PURE__*/React.createElement("div", {
      className: "text-xs text-slate-500"
    }, "pts/g")));
  };
  const upsShown = moreU ? ups : ups.slice(0, 5);
  return /*#__PURE__*/React.createElement("div", {
    className: "space-y-3"
  }, /*#__PURE__*/React.createElement("div", {
    className: "flex flex-wrap gap-2 items-center"
  }, /*#__PURE__*/React.createElement(Pills, {
    items: [["fa", "Free agents"], ["mine", "My team"], ["all", "All teams"]],
    value: who,
    onChange: pick
  }), /*#__PURE__*/React.createElement(Pills, {
    items: [["all", "All"], ["F", "Forwards"], ["D", "Defence"], ["G", "Goalies"]],
    value: pos,
    onChange: setPos
  })), who !== "mine" ? /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500"
  }, allP ? "Every injured player \u00b7 " : "Good players only \u00b7 ", /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: "text-blue-600",
    onClick: () => setAllP(!allP)
  }, allP ? "Good players only" : "Show everyone")) : null, /*#__PURE__*/React.createElement(GxPanel, {
    title: "Updates",
    right: "last 7 days"
  }, ups.length ? upsShown.map((r, i) => row(r, i, true)) : /*#__PURE__*/React.createElement("div", {
    className: "text-sm text-slate-500",
    style: {
      padding: "4px 0"
    }
  }, "No injury updates in the last 7 days", who === "fa" ? " for these free agents" : "", ". New return dates, day-to-day moves and fresh news show up here."), ups.length > 5 ? /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: "text-sm text-blue-600",
    style: {
      marginTop: 8
    },
    onClick: () => setMoreU(!moreU)
  }, moreU ? "Show fewer" : "Show all " + ups.length + " updates") : null), groups.map(([title, g]) => {
    if (!g.length) return null;
    const longer = title === "Out longer" || title === "No return date";
    const shown = longer && !moreL ? g.slice(0, 3) : g;
    return /*#__PURE__*/React.createElement(GxPanel, {
      key: title,
      title: title,
      right: g.length + (g.length === 1 ? " player" : " players")
    }, shown.map((r, i) => row(r, i, false)), shown.length < g.length ? /*#__PURE__*/React.createElement("button", {
      type: "button",
      className: "text-sm text-blue-600",
      style: {
        marginTop: 8
      },
      onClick: () => setMoreL(true)
    }, "Show " + (g.length - shown.length) + " more") : null);
  }), !list.length ? /*#__PURE__*/React.createElement("div", {
    className: "text-sm text-slate-500"
  }, "No injured players match.") : null);
}
// ---------- change 086: simulated trades that stay on until you undo them (install.py) ----------
const GX_SIM_K = "gm-simtrade";
const gxSimList = () => {
  try {
    const v = JSON.parse(localStorage.getItem(GX_SIM_K) || "[]");
    return Array.isArray(v) ? v : [];
  } catch (e) {
    return [];
  }
};
const gxSimSave = l => {
  try {
    localStorage.setItem(GX_SIM_K, JSON.stringify(l));
  } catch (e) {}
  window.dispatchEvent(new Event("gx-sim86"));
};
// apply each saved trade in order; a player only moves if he is still where the trade expects him
const gxSimPlayers = players => {
  const L = gxSimList();
  if (!L.length) return players;
  let P = players,
    keep = [];
  L.forEach(t => {
    const at = {};
    P.forEach(p => {
      at[p.id] = p.ft;
    });
    const real = t.give.every(id => at[id] === t.b) && t.get.every(id => at[id] === t.a);
    if (real) return; // the real trade went through on ESPN, so the what-if is no longer needed
    const mv = {};
    t.give.forEach(id => {
      if (at[id] === t.a) mv[id] = t.b;
    });
    t.get.forEach(id => {
      if (at[id] === t.b) mv[id] = t.a;
    });
    (t.add || []).forEach(id => {
      if (at[id] === "fa") mv[id] = t.a;
    });
    (t.drop || []).forEach(id => {
      if (at[id] === t.a) mv[id] = "fa";
    });
    if (!Object.keys(mv).length) return;
    keep.push(t);
    P = P.map(p => mv[p.id] ? {
      ...p,
      ft: mv[p.id],
      ir: false
    } : p);
  });
  if (keep.length !== L.length) {
    try {
      localStorage.setItem(GX_SIM_K, JSON.stringify(keep));
    } catch (e) {}
  }
  return P;
};
const gxSimReload = setS => {
  const E = window.ESPN_DATA;
  setS(st => {
    if (E) {
      try {
        return applyESPN(st, E);
      } catch (e) {}
    }
    return {
      ...st,
      players: gxSimPlayers(st.players)
    };
  });
};
const gxSimAdd = (t, setS) => {
  gxSimSave(gxSimList().concat([t]));
  gxSimReload(setS);
};
const gxSimDrop = (i, setS) => {
  gxSimSave(gxSimList().filter((_, k) => k !== i));
  gxSimReload(setS);
};
function GxSimBar({
  s,
  setS,
  go
}) {
  const [, tick] = useState(0);
  useEffect(() => {
    const h = () => tick(x => x + 1);
    window.addEventListener("gx-sim86", h);
    return () => window.removeEventListener("gx-sim86", h);
  }, []);
  const L = gxSimList();
  if (!L.length || !s || !s.players) return null;
  const real = window.__TB_REAL || s.me;
  const nm = ids => ids.map(id => {
    const p = s.players.find(x => x.id === id);
    return p ? p.n : null;
  }).filter(Boolean).join(", ");
  const who = id => id === real ? "You" : teamName(s, id).trim();
  const line = t => {
    const g = t.get.concat(t.add || []);
    return who(t.a) + (t.a === real ? " get " : " gets ") + nm(g) + "; " + (t.b === real ? "you get " : teamName(s, t.b).trim() + " gets ") + nm(t.give) + ((t.drop || []).length ? "; " + (t.a === real ? "you drop " : who(t.a) + " drops ") + nm(t.drop) : "") + ".";
  };
  return /*#__PURE__*/React.createElement("div", {
    className: "gx-pn gx-sim86"
  }, /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("div", {
    className: "text-sm",
    style: {
      display: "flex",
      alignItems: "baseline",
      gap: 10,
      flexWrap: "wrap"
    }
  }, /*#__PURE__*/React.createElement("span", {
    className: "font-semibold",
    style: {
      color: "var(--warn)"
    }
  }, L.length === 1 ? "What-if trade is on" : L.length + " what-if trades are on"), /*#__PURE__*/React.createElement("span", {
    className: "text-xs text-slate-500"
  }, "Every page shows it. Nothing changed on ESPN."), /*#__PURE__*/React.createElement("span", {
    style: {
      marginLeft: "auto"
    }
  }, L.length > 1 ? /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: "text-sm text-blue-600",
    onClick: () => {
      gxSimSave([]);
      gxSimReload(setS);
    }
  }, "Undo all") : null)), L.map((t, i) => /*#__PURE__*/React.createElement("div", {
    key: i,
    className: "ln"
  }, /*#__PURE__*/React.createElement("span", {
    className: "min-w-0",
    style: {
      flex: 1
    }
  }, line(t)), /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: "text-sm text-blue-600 whitespace-nowrap",
    onClick: () => gxSimDrop(i, setS)
  }, "Undo"))));
}
// ---------- change 087: a goalie only counts as a lineup game if he starts (install.py) ----------
const gxGPlays = p => {
  if (!p || p.p !== "G") return true;
  if (p.a != null) return p.a !== 0; // game played: real points tell us he was in net
  const g = p.dt ? gStart(p, p.dt) : null;
  return (g ? g.v : p.prob || 0) >= 0.5; // still to come: count him if he is more likely than not to start
};
const gxGmN = L => ((L || {}).start || []).filter(gxGPlays).length;
const gxGmLeft = days => {
  const today = todayISO();
  return (days || []).reduce((t, x) => t + (x ? (x.start || []).filter(p => (!p.dt || p.dt >= today) && (!p.st || p.st === "L" && p.vf > 0) && gxGPlays(p)).length : 0), 0);
};
// ---------- change 088: goalies per team game, like Trades (install.py) ----------
const gxPgAvg = (p, K, dt) => effAvg(p, K, dt) * (p && p.p === "G" ? p.prob != null ? p.prob : 0.5 : 1);
// ---------- change 089: lineup autopilot status (install.py) ----------
const GX_AP_EDIT = "https://github.com/dhaliwal32/23456789786634356/edit/main/autopilot.json";
let __gxAP = null;
const gxApLoad = () => {
  const k = (window.ESPN_DATA || {}).generated || "";
  if (__gxAP && __gxAP.k === k) return __gxAP.p;
  const j = f => fetch(f + "?t=" + Date.now()).then(r => r.ok ? r.json() : null).catch(() => null);
  const p = Promise.all([j("autopilot.json"), j("autopilot_log.json")]).then(([c, b]) => ({
    c,
    b: b || {
      entries: []
    }
  }));
  __gxAP = {
    k,
    p
  };
  return p;
};
function gxUseAp() {
  const [v, setV] = useState(null);
  useEffect(() => {
    let dead = false;
    gxApLoad().then(x => {
      if (!dead) setV(x);
    });
    return () => {
      dead = true;
    };
  }, [(window.ESPN_DATA || {}).generated]);
  return v;
}
const GX_AP_MODE = {
  on: ["On", "var(--good)", "Changes your ESPN lineup by itself and sends you a note each time."],
  test: ["Test", "var(--warn)", "Works out the best lineup and sends you a note, but changes nothing on ESPN."],
  off: ["Off", "var(--mute)", "Does nothing."]
};
const gxApMode = v => v && v.c ? String(v.c.mode || "test").toLowerCase() : null;
const gxApTime = iso => {
  try {
    return new Date(iso).toLocaleTimeString([], {
      hour: "numeric",
      minute: "2-digit"
    });
  } catch (e) {
    return "";
  }
};
const gxApDay = iso => {
  try {
    return new Date(iso).toLocaleDateString([], {
      weekday: "short",
      month: "short",
      day: "numeric"
    });
  } catch (e) {
    return "";
  }
};
function GxAutoToday({
  go
}) {
  const v = gxUseAp();
  if (!v || !v.b) return null;
  const today = todayISO();
  const e = [...(v.b.entries || [])].reverse().find(x => String(x.at || "").slice(0, 10) === today);
  if (!e) return null;
  const fail = String(e.result || "").indexOf("failed") === 0,
    test = e.mode !== "on";
  return /*#__PURE__*/React.createElement("div", {
    className: "gx-pn",
    style: {
      borderLeft: "3px solid " + (fail ? "var(--bad)" : test ? "var(--warn)" : "var(--good)"),
      padding: "10px 14px"
    }
  }, /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("div", {
    className: "text-sm"
  }, /*#__PURE__*/React.createElement("span", {
    className: "font-semibold",
    style: {
      color: fail ? "var(--bad)" : test ? "var(--warn)" : "var(--good)"
    }
  }, fail ? "Autopilot could not change your lineup" : test ? "Autopilot test" : "Autopilot set your lineup"), /*#__PURE__*/React.createElement("span", {
    className: "text-slate-500"
  }, " · " + gxApTime(e.at))), /*#__PURE__*/React.createElement("div", {
    className: "text-sm",
    style: {
      marginTop: 2
    }
  }, (e.day && e.day !== todayISO() ? "For " + gxApDayName(e.day) + ": " : "") + (test && !fail ? "Would: " : "") + e.text + (e.gain ? " +" + e.gain + " points." : "")), /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500",
    style: {
      marginTop: 4
    }
  }, fail ? "Set it by hand on ESPN today. " : test ? "Nothing was changed on ESPN. " : "", /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: "text-blue-600",
    onClick: () => go("setup", "autopilot")
  }, "Autopilot details")));
}
function GxAutoPage({
  s,
  go
}) {
  const v = gxUseAp();
  const m = gxApMode(v),
    M = GX_AP_MODE[m] || null;
  const list = v && v.b ? [...(v.b.entries || [])].reverse().slice(0, 25) : [];
  return /*#__PURE__*/React.createElement("div", {
    className: "space-y-3"
  }, /*#__PURE__*/React.createElement("div", {
    className: "font-semibold",
    style: {
      fontSize: 17
    }
  }, "Lineup autopilot"), /*#__PURE__*/React.createElement("div", {
    className: "gx-pn"
  }, /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("div", {
    className: "gx-sr",
    style: {
      borderTop: 0
    }
  }, /*#__PURE__*/React.createElement("span", null, "Mode"), /*#__PURE__*/React.createElement("span", {
    className: "font-semibold",
    style: {
      color: M ? M[1] : "var(--mute)"
    }
  }, !v ? "Checking…" : M ? M[0] : "Starts after the next sync")), M ? /*#__PURE__*/React.createElement("div", {
    className: "text-sm text-slate-500",
    style: {
      padding: "2px 0 8px"
    }
  }, M[2]) : null, /*#__PURE__*/React.createElement("div", {
    className: "gx-sr"
  }, /*#__PURE__*/React.createElement("span", null, "Change the mode"), /*#__PURE__*/React.createElement("a", {
    className: "text-sm text-blue-600",
    href: GX_AP_EDIT,
    target: "_blank",
    rel: "noopener"
  }, "Open on GitHub")), /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500",
    style: {
      paddingTop: 6
    }
  }, "On GitHub, tap the pencil, change the word after \"mode\" to on, test or off (keep the quote marks), then Commit changes. It takes effect at the next sync. To set lineups ahead, change the number after \"days_ahead\": 0 is today only, 3 is the next 3 days too, 7 is a week. Days after today are set once, then only changed again on the day itself.")), /*#__PURE__*/React.createElement("div", {
    className: "gx-pn"
  }, /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("div", {
    className: "gx-tag",
    style: {
      marginBottom: 6
    }
  }, "What it does"), /*#__PURE__*/React.createElement("div", {
    className: "text-sm",
    style: {
      lineHeight: 1.6
    }
  }, /*#__PURE__*/React.createElement("div", null, "• Every sync (every 6 to 30 minutes) it works out today's best lineup from your projections."), /*#__PURE__*/React.createElement("div", null, "• Starts players who have a game, benches players who don't, and swaps in the goalie who is actually starting."), /*#__PURE__*/React.createElement("div", null, "• Never moves a player once his game has started, never touches IR, and only changes things when it adds at least " + (v && v.c && v.c.min_gain || 0.5) + " points."), /*#__PURE__*/React.createElement("div", null, "• Sends a phone note every time, and shows it on Today."))), /*#__PURE__*/React.createElement(GxPanel, {
    title: "History",
    right: list.length ? "newest first" : ""
  }, list.length ? list.map((e, i) => {
    const fail = String(e.result || "").indexOf("failed") === 0,
      test = e.mode !== "on";
    return /*#__PURE__*/React.createElement("div", {
      key: i,
      className: "gx-row",
      style: {
        display: "block",
        ...(i ? {} : {
          borderTop: 0
        })
      }
    }, /*#__PURE__*/React.createElement("div", {
      className: "text-xs text-slate-500"
    }, gxApDay(e.at) + " · " + gxApTime(e.at) + " · ", /*#__PURE__*/React.createElement("span", {
      style: {
        color: fail ? "var(--bad)" : test ? "var(--warn)" : "var(--good)"
      }
    }, fail ? "ESPN refused" : test ? "test only" : "done"), e.gain ? " · +" + e.gain + " pts" : ""), /*#__PURE__*/React.createElement("div", {
      className: "text-sm"
    }, e.text), fail ? /*#__PURE__*/React.createElement("div", {
      className: "text-xs",
      style: {
        color: "var(--bad)"
      }
    }, String(e.result).replace(/^failed: /, "")) : null);
  }) : /*#__PURE__*/React.createElement("div", {
    className: "text-sm text-slate-500"
  }, "Nothing yet. The first suggestion shows up here when your lineup can be improved.")));
}
function GxAutoRow({
  row,
  go
}) {
  const v = gxUseAp();
  const m = gxApMode(v),
    M = GX_AP_MODE[m];
  const last = v && v.b && (v.b.entries || []).length ? v.b.entries[v.b.entries.length - 1] : null;
  const txt = !v ? "Checking…" : !M ? "Starts after the next sync" : M[0] + " mode" + (last ? " · last: " + gxApDay(last.at) + " " + gxApTime(last.at) : " · nothing to fix yet");
  return row("autopilot", "Lineup autopilot", txt, () => go("setup", "autopilot"), 3);
}
// ---------- change 090: autopilot controls in the app, lineups set days ahead (install.py) ----------
const GX_AP_API = "https://api.github.com/repos/dhaliwal32/23456789786634356/contents/autopilot.json";
const GX_AP_RUN = "https://api.github.com/repos/dhaliwal32/23456789786634356/actions/workflows/sync.yml/dispatches";
const gxApSave = patch => {
  const key = gxSyncKey();
  if (!key) return Promise.reject(new Error("nokey"));
  const hdr = {
    Authorization: "Bearer " + key,
    Accept: "application/vnd.github+json"
  };
  const once = again => fetch(GX_AP_API + "?ref=main&t=" + Date.now(), {
    headers: hdr,
    cache: "no-store"
  }).then(r => {
    if (r.status === 401 || r.status === 403) throw new Error("key");
    if (!r.ok) throw new Error("read " + r.status);
    return r.json();
  }).then(j => {
    let cur = {};
    try {
      cur = JSON.parse(decodeURIComponent(escape(atob(String(j.content || "").replace(/\n/g, "")))));
    } catch (e) {}
    const next = {
      ...cur,
      ...patch
    };
    return fetch(GX_AP_API, {
      method: "PUT",
      headers: {
        ...hdr,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        message: "Autopilot settings from the app",
        content: gxB64(JSON.stringify(next, null, 2) + "\n"),
        branch: "main",
        sha: j.sha
      })
    }).then(r => {
      if ((r.status === 409 || r.status === 422) && again) return once(false);
      if (!r.ok) throw new Error(r.status === 401 || r.status === 403 ? "key" : "save " + r.status);
      return next;
    });
  });
  return once(true).then(next => fetch(GX_AP_RUN, {
    method: "POST",
    headers: {
      ...hdr,
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      ref: "main"
    })
  }).then(r => ({
    next,
    ran: r.status === 204
  })).catch(() => ({
    next,
    ran: false
  })));
};
const GX_AP_AHEAD = [["0", "Today only"], ["1", "+1 day"], ["3", "+3 days"], ["week", "Rest of week"], ["7", "+7 days"]];
const gxApDayName = d => {
  try {
    return d === todayISO() ? "today" : fromIso(d).toLocaleDateString([], {
      weekday: "short",
      month: "short",
      day: "numeric"
    });
  } catch (e) {
    return d || "";
  }
};
function GxAutoPage2({
  s,
  go
}) {
  const v = gxUseAp();
  const [cfg, setCfg] = useState(null);
  const [busy, setBusy] = useState(false);
  const [msg, setMsg] = useState("");
  const c = cfg || v && v.c || null;
  const m = c ? String(c.mode || "test").toLowerCase() : null,
    M = GX_AP_MODE[m] || null;
  const ahead = c ? String(c.days_ahead == null ? 0 : c.days_ahead) : "0";
  const has = !!gxSyncKey();
  const list = v && v.b ? [...(v.b.entries || [])].reverse().slice(0, 25) : [];
  const save = (patch, done) => {
    if (busy) return;
    setBusy(true);
    setMsg("Saving…");
    gxApSave(patch).then(({
      next,
      ran
    }) => {
      setCfg(next);
      __gxAP = null;
      setMsg((done || "Saved.") + (ran ? " Running now; give it about 2 minutes." : " It takes effect at the next sync (every 6 to 30 minutes)."));
    }).catch(e => setMsg(e && e.message === "key" ? "GitHub refused the key. It needs Contents: Read and write on this repo." : e && e.message === "nokey" ? "Turn on Sync between devices first." : "Could not reach GitHub. Try again.")).finally(() => setBusy(false));
  };
  const seg = (items, val, pick) => /*#__PURE__*/React.createElement("span", {
    className: "gx-seg"
  }, items.map(([k, l]) => /*#__PURE__*/React.createElement("button", {
    key: k,
    type: "button",
    disabled: busy || !has,
    className: val === k ? "on" : "",
    onClick: () => pick(k)
  }, l)));
  const pickMode = k => {
    if (k === m) return;
    if (k === "on" && !window.confirm("Let the app change your real ESPN lineup by itself?")) return;
    save({
      mode: k
    }, "Mode set to " + GX_AP_MODE[k][0] + ".");
  };
  return /*#__PURE__*/React.createElement("div", {
    className: "space-y-3"
  }, /*#__PURE__*/React.createElement("div", {
    className: "font-semibold",
    style: {
      fontSize: 17
    }
  }, "Lineup autopilot"), /*#__PURE__*/React.createElement("div", {
    className: "gx-pn"
  }, /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("div", {
    className: "gx-sr",
    style: {
      borderTop: 0
    }
  }, /*#__PURE__*/React.createElement("span", null, "Mode"), c ? seg([["off", "Off"], ["test", "Test"], ["on", "On"]], m, pickMode) : /*#__PURE__*/React.createElement("span", {
    className: "text-sm text-slate-500"
  }, v ? "Starts after the next sync" : "Checking…")), M ? /*#__PURE__*/React.createElement("div", {
    className: "text-sm text-slate-500",
    style: {
      padding: "2px 0 8px"
    }
  }, M[2]) : null, /*#__PURE__*/React.createElement("div", {
    className: "gx-sr"
  }, /*#__PURE__*/React.createElement("span", null, "Set lineups"), seg(GX_AP_AHEAD, ahead, k => save({
    days_ahead: k === "week" ? "week" : +k
  }, "Lineups will be set " + ({
    "0": "for today only.",
    "1": "for today and tomorrow.",
    "3": "for today and the next 3 days.",
    week: "through Sunday.",
    "7": "for today and the next 7 days."
  }[k] || ".")))), /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500",
    style: {
      paddingTop: 6
    }
  }, "Days after today are set once. After that they only change on the day itself, when starting goalies are confirmed, or when you tap Redo."), /*#__PURE__*/React.createElement("div", {
    className: "gx-sr"
  }, /*#__PURE__*/React.createElement("span", null, "Upcoming days"), /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: "border border-slate-300 rounded-lg px-3 py-1 text-sm",
    disabled: busy || !has || ahead === "0",
    onClick: () => save({
      redo_at: new Date().toISOString()
    }, "Upcoming days will be set again.")
  }, "Redo upcoming days")), msg ? /*#__PURE__*/React.createElement("div", {
    className: "text-xs",
    style: {
      paddingTop: 6,
      color: /refused|Could not|first/.test(msg) ? "var(--bad)" : "var(--good)"
    }
  }, msg) : null, !has ? /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500",
    style: {
      paddingTop: 8
    }
  }, "To change these here, turn on Sync between devices in Setup, Data and backup. Or ", /*#__PURE__*/React.createElement("a", {
    className: "text-blue-600",
    href: GX_AP_EDIT,
    target: "_blank",
    rel: "noopener"
  }, "edit autopilot.json on GitHub"), ".") : null), /*#__PURE__*/React.createElement("div", {
    className: "gx-pn"
  }, /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("div", {
    className: "gx-tag",
    style: {
      marginBottom: 6
    }
  }, "What it does"), /*#__PURE__*/React.createElement("div", {
    className: "text-sm",
    style: {
      lineHeight: 1.6
    }
  }, /*#__PURE__*/React.createElement("div", null, "• Every sync it works out the best lineup for today and for the days you chose."), /*#__PURE__*/React.createElement("div", null, "• Starts players who have a game, benches players who don't, and swaps in the goalie who is actually starting."), /*#__PURE__*/React.createElement("div", null, "• Never moves a player once his game has started, never touches IR, and only changes things when it adds at least " + (c && c.min_gain || 0.5) + " points."), /*#__PURE__*/React.createElement("div", null, "• Sends a phone note every time, and shows it on Today."))), /*#__PURE__*/React.createElement(GxPanel, {
    title: "History",
    right: list.length ? "newest first" : ""
  }, list.length ? list.map((e, i) => {
    const fail = String(e.result || "").indexOf("failed") === 0,
      test = e.mode !== "on";
    return /*#__PURE__*/React.createElement("div", {
      key: i,
      className: "gx-row",
      style: {
        display: "block",
        ...(i ? {} : {
          borderTop: 0
        })
      }
    }, /*#__PURE__*/React.createElement("div", {
      className: "text-xs text-slate-500"
    }, "For " + gxApDayName(e.day) + " · " + gxApDay(e.at) + " " + gxApTime(e.at) + " · ", /*#__PURE__*/React.createElement("span", {
      style: {
        color: fail ? "var(--bad)" : test ? "var(--warn)" : "var(--good)"
      }
    }, fail ? "ESPN refused" : test ? "test only" : "done"), e.gain ? " · +" + e.gain + " pts" : ""), /*#__PURE__*/React.createElement("div", {
      className: "text-sm"
    }, e.text), fail ? /*#__PURE__*/React.createElement("div", {
      className: "text-xs",
      style: {
        color: "var(--bad)"
      }
    }, String(e.result).replace(/^failed: /, "")) : null);
  }) : /*#__PURE__*/React.createElement("div", {
    className: "text-sm text-slate-500"
  }, "Nothing yet. The first suggestion shows up here when a lineup can be improved.")));
}
// ---------- change 092: full result for a pickup, like Trades (install.py) ----------
function GxPickRes92({
  s,
  myR,
  ok
}) {
  const key = ok.map(x => x.a.id + ">" + x.d.id).join(",");
  const calc = () => {
    const nR = s.weeks.length - s.wk;
    const timed = timedMove(myR, s.me, ok.map(x => ({
      add: x.a,
      drop: x.d
    })));
    const my = horizonTotal(timed, s, nR) - horizonTotal(myR, s, nR);
    const w = deriveWeek(s.weeks[s.wk] || s.weeks[0], s.autoDone),
      on = oppOf(w, s.me) && (w.done || 0) < (w.dates || []).length;
    const tb = on ? winChance(s) : null,
      ta = on ? winChance(s, timed) : null;
    const sN = nextWkS(s),
      ho = sN && oppOf(sN.weeks[sN.wk] || {}, s.me);
    const wb = ho ? winChance(sN) : null,
      wa = ho ? winChance(sN, timed) : null;
    return {
      my,
      tb,
      ta,
      wb,
      wa
    };
  };
  const [tm93, setTm93] = useState(null); // change 093: projection for this box only
  const res = useMemo(() => gxWithMode82(tm93, () => {
    const base = calc();
    const A = new Set(ok.map(x => x.a.id)),
      D = new Set(ok.map(x => x.d.id));
    const players = s.players.map(p => A.has(p.id) ? {
      ...p,
      ft: s.me
    } : D.has(p.id) ? {
      ...p,
      ft: "fa",
      ir: false
    } : p);
    const pos = t => ({
      o: t.rows.findIndex(x => x.t.id === s.me) + 1,
      ...(t.grpRank[s.me] || {})
    });
    const keep = __LT,
      t2 = leagueTable({
        ...s,
        players
      });
    __LT = keep;
    return {
      ...base,
      rb: pos(leagueTable(s)),
      ra: pos(t2),
      mode: window.__PMODE
    };
  }), [key, s.players, s.wk, window.__PMODE, tm93]);
  const [cmp, setCmp] = useState(null);
  useEffect(() => {
    setCmp(null);
    const id = setTimeout(() => setCmp(GX_PM82.filter(([k]) => gxCanMode82(k)).map(([k, l]) => ({
      k,
      l,
      ...(k === res.mode ? res : gxWithMode82(k, calc))
    }))), 60);
    return () => clearTimeout(id);
  }, [res]);
  const GN = {
    F: "Forwards",
    D: "Defence",
    G: "Goalies"
  };
  const sg = v => (v >= 0 ? "+" : "") + Math.round(v);
  const arrow = (b, a, fmt, up) => /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("span", null, fmt(b)), /*#__PURE__*/React.createElement("span", {
    className: "text-slate-500",
    style: {
      fontSize: 14,
      margin: "0 6px"
    }
  }, "→"), /*#__PURE__*/React.createElement("span", {
    style: {
      color: up > 0 ? "var(--good)" : up < 0 ? "var(--bad)" : "var(--ink)"
    }
  }, fmt(a)));
  const wkUp = res.ta != null && res.tb != null ? Math.round(res.ta * 100) - Math.round(res.tb * 100) : 0;
  const vd = res.my > 0.5 ? ["Good pickup", "var(--good)", "Your lineup gains points for the rest of the season."] : wkUp > 0 ? ["Stream only", "var(--warn)", "Helps this week, but costs you points over the season. Fine if you swap him back later."] : ["Bad for you", "var(--bad)", "Your lineup gets worse."];
  return /*#__PURE__*/React.createElement("div", {
    style: {
      marginTop: 14
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      alignItems: "baseline",
      gap: 10,
      flexWrap: "wrap"
    }
  }, /*#__PURE__*/React.createElement("span", {
    className: "font-semibold",
    style: {
      color: vd[1]
    }
  }, vd[0]), /*#__PURE__*/React.createElement("span", {
    className: "text-sm text-slate-500"
  }, vd[2])), /*#__PURE__*/React.createElement("div", {
    className: "gx-pmh82"
  }, /*#__PURE__*/React.createElement("span", {
    className: "text-xs text-slate-500"
  }, "Projection"), /*#__PURE__*/React.createElement("span", {
    className: "gx-seg"
  }, GX_PM82.map(([k, l]) => /*#__PURE__*/React.createElement("button", {
    key: k,
    type: "button",
    disabled: !gxCanMode82(k),
    className: res.mode === k ? "on" : "",
    onClick: () => setTm93(k === window.__PMODE ? null : k)
  }, l))), tm93 && tm93 !== window.__PMODE ? /*#__PURE__*/React.createElement("span", {
    className: "text-xs text-slate-500"
  }, "This box only. The rest of the app still uses " + (GX_PM82.find(x => x[0] === window.__PMODE) || [0, "Best"])[1] + ".") : null), /*#__PURE__*/React.createElement("div", {
    className: "gx-stg"
  }, /*#__PURE__*/React.createElement("div", {
    className: "gx-stc"
  }, /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500"
  }, "Your lineup"), /*#__PURE__*/React.createElement("div", {
    className: "gx-stv",
    style: {
      color: res.my >= 0 ? "var(--good)" : "var(--bad)"
    }
  }, sg(res.my)), /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500"
  }, "points, rest of season")), /*#__PURE__*/React.createElement("div", {
    className: "gx-stc"
  }, /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500"
  }, "Your league rank"), /*#__PURE__*/React.createElement("div", {
    className: "gx-stv"
  }, arrow(res.rb.o, res.ra.o, ordN, res.rb.o - res.ra.o)), /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500"
  }, "by team strength")), /*#__PURE__*/React.createElement("div", {
    className: "gx-stc"
  }, /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500"
  }, "Position ranks"), ["F", "D", "G"].map(k => {
    const b = res.rb[k],
      a = res.ra[k],
      f = v => v ? ordN(v) : "–";
    return /*#__PURE__*/React.createElement("div", {
      key: k,
      style: {
        display: "flex",
        alignItems: "baseline",
        gap: 6,
        fontSize: 15,
        fontWeight: 600,
        fontVariantNumeric: "tabular-nums",
        marginTop: 2
      }
    }, /*#__PURE__*/React.createElement("span", {
      className: "text-xs text-slate-500",
      style: {
        width: 74,
        flexShrink: 0,
        fontWeight: 400
      }
    }, GN[k]), b === a ? /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("span", null, f(b)), /*#__PURE__*/React.createElement("span", {
      className: "text-xs text-slate-500",
      style: {
        fontWeight: 400
      }
    }, "same")) : /*#__PURE__*/React.createElement("span", null, arrow(b, a, f, (b || 0) - (a || 0))));
  })), res.tb != null && res.ta != null ? /*#__PURE__*/React.createElement("div", {
    className: "gx-stc"
  }, /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500"
  }, "This week"), /*#__PURE__*/React.createElement("div", {
    className: "gx-stv"
  }, arrow(res.tb, res.ta, wpTxt, wkUp)), /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500"
  }, "chance to win")) : null, res.wb != null && res.wa != null ? /*#__PURE__*/React.createElement("div", {
    className: "gx-stc"
  }, /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500"
  }, "Next week"), /*#__PURE__*/React.createElement("div", {
    className: "gx-stv"
  }, arrow(res.wb, res.wa, wpTxt, Math.round(res.wa * 100) - Math.round(res.wb * 100))), /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500"
  }, "chance to win")) : null), /*#__PURE__*/React.createElement("div", {
    style: {
      marginTop: 12
    }
  }, /*#__PURE__*/React.createElement("div", {
    className: "gx-tag",
    style: {
      marginBottom: 4
    }
  }, "Every projection"), /*#__PURE__*/React.createElement("div", {
    className: "gx-pm92 h"
  }, /*#__PURE__*/React.createElement("span", null, "Projection"), /*#__PURE__*/React.createElement("span", null, "Season"), /*#__PURE__*/React.createElement("span", {
    className: "m-hide"
  }, "This week"), /*#__PURE__*/React.createElement("span", null, "Next week"), /*#__PURE__*/React.createElement("span", null, "Result")), !cmp ? /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500",
    style: {
      padding: "8px 6px"
    }
  }, "Working out every projection...") : cmp.map(x => /*#__PURE__*/React.createElement("div", {
    key: x.k,
    className: "gx-pm92 r" + (x.k === res.mode ? " on" : ""),
    role: "button",
    onClick: () => setTm93(x.k === window.__PMODE ? null : x.k),
    title: "Show the pickup with this projection"
  }, /*#__PURE__*/React.createElement("span", null, x.l, x.k === window.__PMODE ? /*#__PURE__*/React.createElement("span", {
    className: "text-xs text-slate-500"
  }, " (app)") : null), /*#__PURE__*/React.createElement("span", {
    style: {
      color: x.my >= 0 ? "var(--good)" : "var(--bad)"
    }
  }, sg(x.my)), /*#__PURE__*/React.createElement("span", {
    className: "m-hide"
  }, gxPct82(x.tb, x.ta)), /*#__PURE__*/React.createElement("span", null, gxPct82(x.wb, x.wa)), /*#__PURE__*/React.createElement("span", {
    className: x.my > 0 ? "w" : "l"
  }, x.my > 0 ? "Win" : "Lose"))), /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500",
    style: {
      marginTop: 6
    }
  }, "Tap a projection to see the result with it. Season is points for the rest of the season. The weeks show the change in your chance to win. Win means your lineup gains points.")));
}
// ---------- change 092: autopilot note on Today is one short line (install.py) ----------
function GxAutoToday2({
  go
}) {
  const v = gxUseAp();
  if (!v || !v.b) return null;
  const today = todayISO();
  const e = [...(v.b.entries || [])].reverse().find(x => String(x.at || "").slice(0, 10) === today);
  if (!e) return null;
  const fail = String(e.result || "").indexOf("failed") === 0,
    test = e.mode !== "on";
  const col = fail ? "var(--bad)" : test ? "var(--warn)" : "var(--good)";
  const day = e.day && e.day !== today ? gxApDayName(e.day) + "'s" : "today's";
  const txt = fail ? "Autopilot could not set your lineup. Set it on ESPN." : (test ? "Autopilot test: would change " : "Autopilot set ") + day + " lineup" + (e.gain ? " (+" + e.gain + ")" : "");
  return /*#__PURE__*/React.createElement("div", {
    className: "gx-pn gx-ap92",
    role: "button",
    onClick: () => go("setup", "autopilot"),
    title: e.text
  }, /*#__PURE__*/React.createElement("span", {
    className: "dot",
    style: {
      background: col
    }
  }), /*#__PURE__*/React.createElement("span", {
    className: "truncate",
    style: {
      flex: 1,
      minWidth: 0
    }
  }, txt), /*#__PURE__*/React.createElement("span", {
    className: "text-xs text-slate-500",
    style: {
      flexShrink: 0
    }
  }, gxApTime(e.at)));
}
// ---------- change 095: ESPN-style player screen (install.py) ----------
const GXPD_DOT = " " + String.fromCharCode(183) + " ";
const gxPdSec = t => {
  const m = String(t || "").split(":");
  return m.length === 2 ? +m[0] * 60 + +m[1] : null;
};
const gxPdMS = v => {
  if (v == null) return "-";
  const r = Math.round(v);
  return Math.floor(r / 60) + ":" + String(r % 60).padStart(2, "0");
};
const gxPdReal = (p, d) => {
  const D = ((window.ESPN_DATA || {}).daily || {})[d] || {},
    id = String(p.id || "").replace(/^e/, "");
  for (const tm of Object.values(D)) {
    const v = (tm || {})[id];
    if (v && v[0] != null) return v[0];
  }
  return null;
};
const gxPdTeam = t => ((window.LINES_DATA || {}).teams || {})[t] || {};
// jersey number from the NHL roster (saved by gm_lines.py from change 095 on)
const gxPdNo = p => {
  const m = gxPdTeam(p.t).no;
  if (!m) return null;
  const k = nrm(p.n);
  for (const n in m) if (nrm(n) === k) return m[n];
  return null;
};
// NHL position code and shoots (C, LW, RW, D; L or R)
const gxPdNhlPos = p => {
  const m = (gxPdTeam(p.t).pos || {}).nhl || {},
    k = nrm(p.n);
  for (const n in m) if (nrm(n) === k) return m[n];
  return "";
};
const gxPdSigned = v => v > 0 ? "+" + v : String(v || 0);
// one row of totals for a set of games
const gxPdSum = (rows, isG) => {
  const n = rows.length,
    sum = f => rows.reduce((a, r) => a + (f(r) || 0), 0);
  if (isG) {
    const sv = sum(r => r.x.sv),
      sa = sum(r => r.x.sa != null ? r.x.sa : (r.x.sv || 0) + (r.x.ga || 0));
    return {
      gp: n,
      w: rows.filter(r => r.x.dec === "W").length,
      l: rows.filter(r => r.x.dec === "L" || r.x.dec === "O").length,
      ga: sum(r => r.x.ga),
      sv,
      svp: sa ? sv / sa : null,
      fp: sum(r => r.fp)
    };
  }
  const ts = rows.map(r => gxPdSec(r.x.toi)).filter(v => v != null);
  return {
    gp: n,
    toi: ts.length ? ts.reduce((a, v) => a + v, 0) / ts.length : null,
    g: sum(r => r.x.g),
    a: sum(r => r.x.a),
    pm: sum(r => r.x.pm),
    pim: sum(r => r.x.pim),
    sog: sum(r => r.x.sog),
    fp: sum(r => r.fp)
  };
};
const GX_PD_SLOT = {
  F1: "1st line",
  F2: "2nd line",
  F3: "3rd line",
  F4: "4th line",
  D1: "Top pair",
  D2: "2nd pair",
  D3: "3rd pair",
  PP1: "Power play 1",
  PP2: "Power play 2",
  PK1: "Penalty kill 1",
  PK2: "Penalty kill 2",
  G: "Goalies"
};
function GxPlayerDetail({
  p: p0,
  s,
  wk,
  onClose
}) {
  const K = s.blend,
    today = todayISO(),
    sc = s.sc || {};
  const p = s.players.find(q => q.id === p0.id) || p0;
  const eid = typeof p.id === "string" && p.id[0] === "e" ? p.id.slice(1) : null;
  const isG = p.p === "G";
  const [tab, setTab] = useState("ov");
  const [log, setLog] = useState(null);
  const [nLog, setNLog] = useState(100000); /* gx118: full log */
  const [img, setImg] = useState(true);
  const [out101, setOut101] = useState(false);
  const close101 = () => {
    if (out101) return;
    setOut101(true);
    setTimeout(onClose, 190);
  };
  const rank = useMemo(() => {
    const o = {},
      pv = q => effAvg(q, K) * (q.p === "G" ? q.prob : 1);
    ["F", "D", "G"].forEach(k => {
      s.players.filter(q => q.p === k && q.prob > 0 && (q.proj !== false || q.gp > 0)).map(q => [q.id, pv(q)]).sort((a, b) => b[1] - a[1]).forEach((x, i) => o[x[0]] = i + 1);
    });
    return o;
  }, [s.players, K, window.__PMODE]);
  useEffect(() => {
    setTab("ov");
    setNLog(100000);
    setImg(true);
  }, [p.id]);
  useEffect(() => {
    const k = e => {
      if (e.key === "Escape") onClose();
    };
    window.addEventListener("keydown", k);
    return () => window.removeEventListener("keydown", k);
  }, []);
  useEffect(() => {
    let dead = false;
    setLog(null);
    if (!eid) {
      setLog([]);
      return;
    }
    const past = [...(SCHED && SCHED[p.t] || [])].filter(d => d <= today).sort().reverse();
    gxBoxIdx().then(idx => {
      const has = new Set(idx || []);
      return Promise.all(past.map(d => {
        const live = pStat(p, d);
        return has.has(d) ? gxBoxDay(d).then(day => ({
          d,
          x: day && day[eid] || live,
          day
        })) : Promise.resolve({
          d,
          x: live
        });
      }));
    }).then(list => {
      if (dead) return;
      setLog(list.filter(r => r.x || !(r.d === today && gState(p.t, r.d).s === "P")).map(r => {
        if (!r.x) {
          const tm = r.day ? Object.values(r.day).find(v => v && v.t === p.t) : null;
          return {
            ...r,
            x: tm ? {
              ...GX_DNP105,
              o: tm.o,
              h: tm.h
            } : GX_DNP105,
            dnp: true,
            fp: null,
            est: false,
            st: "F"
          };
        }
        const a = r.x.fp != null ? r.x.fp : gxPdReal(p, r.d);
        return {
          ...r,
          fp: a != null ? a : gxEst(r.x, sc),
          est: a == null,
          st: gState(p.t, r.d).s
        };
      }));
    }).catch(() => {
      if (!dead) setLog([]);
    });
    return () => {
      dead = true;
    };
  }, [p.id]);

  // header facts
  const sp = String(p.n || "").indexOf(" "),
    first = sp > 0 ? p.n.slice(0, sp) : "",
    last = sp > 0 ? p.n.slice(sp + 1) : p.n;
  const no = gxPdNo(p),
    nhlPos = gxPdNhlPos(p);
  const T = gxPdTeam(p.t),
    tName = (T.st || {}).name || p.t;
  const back = eid ? effBack(p) : {
    d: ""
  };
  const hurt = !!(p.ir || p.status && p.status !== "ACTIVE" || back.d && back.d > today);
  const stTxt = !hurt ? "Healthy" : p.ir ? "Injured reserve" : p.status === "DAY_TO_DAY" ? "Day to day" : p.status === "OUT" ? "Out" : p.status === "SUSPENSION" ? "Suspended" : p.status === "INJURY_RESERVE" ? "Injured reserve" : "Not playing";
  const stCol = !hurt ? "var(--good)" : p.status === "DAY_TO_DAY" ? "var(--warn)" : "var(--bad)";
  const posWord = isG ? "G" : p.p === "D" ? "D" : "F";
  const elig = posWord + (nhlPos && nhlPos[0] !== posWord ? " (" + nhlPos.replace(/[LR]$/, "") + ")" : "");
  const rk = rank[p.id];
  const avgSoFar = p.gp ? p.tot / p.gp : null;
  const proj = eid ? effAvg(p, K) : null;
  const inj = eid ? ((window.__SIG || {}).injuries || {})[eid] : null;
  const news = eid ? sigOf(p).news || [] : [];

  // this week and next games
  const per = d => {
    if (!eid) return null;
    const g = isG ? gStart(p, d) : null;
    return {
      x: effAvg(p, K, d) * (g ? g.v : p.prob != null ? p.prob : 1) * avail(p, d),
      g
    };
  };
  const wkIdx = eid && wk && wk.games ? (wk.games[p.t] || []).filter(i => ((wk.dates || [])[i] || "") >= today && gState(p.t, wk.dates[i]).s === "P") : [];
  const wkPts = wkIdx.reduce((a, i) => a + ((per(wk.dates[i]) || {}).x || 0), 0);
  const L = window.LINES_DATA || {};
  const nextG = ((L.sched || {})[p.t] || []).filter(x => x.d >= today).slice(0, 5);

  // stats rows
  const rows = log || [];
  const done = rows.filter(r => !r.dnp);
  const since = n => done.filter(r => r.d >= addDays(today, -(n - 1)));
  const statRows = [["Season", gxPdSum(done, isG)], ["Last 7 days", gxPdSum(since(7), isG)], ["Last 15 days", gxPdSum(since(15), isG)]];
  const SH = isG ? ["GP", "W", "L", "GA", "SV", "SV%", "FPTS"] : ["GP", "ATOI", "G", "A", "+/-", "PIM", "SOG", "FPTS"];
  const svp = v => v == null ? "-" : v.toFixed(3).replace(/^0/, "");
  const statCells = r => isG ? [r.gp, r.w, r.l, r.ga, r.sv, svp(r.svp), f1(r.fp)] : [r.gp, gxPdMS(r.toi), r.g, r.a, gxPdSigned(r.pm), r.pim, r.sog, f1(r.fp)];

  // lines
  const ln = T.lines || {},
    me = nrm(p.n);
  const slots = Object.keys(ln).filter(k => (ln[k] || []).some(n => nrm(n) === me));
  const mateP = n => s.players.find(q => nrm(q.n) === nrm(n) && q.t === p.t) || s.players.find(q => nrm(q.n) === nrm(n));
  const chg = (L.changes || []).filter(c => nrm(c.name) === me && (c.team === p.t || c.from === p.t || c.to === p.t)).slice(0, 6);
  const Q = window.__QA;
  const act = fn => () => {
    onClose();
    fn(p);
  };
  const owner = p.ft === "fa" ? p.wv ? "Waivers" : "Free agent" : /*#__PURE__*/React.createElement(TL, {
    s: s,
    id: p.ft
  });
  const tabs = [["ov", "Overview"], ["log", "Game log"], ["news", "News" + (news.length ? " (" + news.length + ")" : "")], ["lines", "Lines"]];
  return /*#__PURE__*/React.createElement("div", {
    className: "gx-pd-ov" + (out101 ? " out" : ""),
    onClick: close101
  }, /*#__PURE__*/React.createElement("div", {
    className: "gx-pd",
    "data-gx": "095",
    onClick: e => e.stopPropagation()
  }, /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: "gx-pd-x",
    "aria-label": "Close",
    onClick: close101
  }, String.fromCharCode(215)), /*#__PURE__*/React.createElement("div", {
    className: "gx-pdm",
    style: {
      "--tc": gxTC101(p.t)
    }
  }, /*#__PURE__*/React.createElement("span", {
    className: "wm"
  }, /*#__PURE__*/React.createElement(TeamLogo, {
    t: p.t,
    size: 260
  })), /*#__PURE__*/React.createElement("div", {
    className: "top"
  }, /*#__PURE__*/React.createElement("div", {
    className: "info"
  }, /*#__PURE__*/React.createElement("div", {
    className: "nm"
  }, p.n), /*#__PURE__*/React.createElement("div", {
    className: "ln"
  }, /*#__PURE__*/React.createElement(TeamLogo, {
    t: p.t,
    size: 20
  }), /*#__PURE__*/React.createElement("span", null, p.t + " · " + posWord + (no != null ? " · #" + no : "") + (gxGS106(p) ? " · starts " + gxGS106(p).pct : ""))), /*#__PURE__*/React.createElement("div", {
    className: "ln"
  }, owner), Q ? /*#__PURE__*/React.createElement("div", {
    className: "bt"
  }, /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: "pr",
    onClick: act(Q.swap)
  }, Q.mine(p) ? "Find a replacement" : "Find a swap"), Q.tradeable(p) ? /*#__PURE__*/React.createElement("button", {
    type: "button",
    onClick: act(Q.trade)
  }, "Trade") : /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("button", {
    type: "button",
    onClick: () => Q.espn(p)
  }, "Add on ESPN"), /*#__PURE__*/React.createElement("button", {
    type: "button",
    onClick: () => {
      gxHide.toggle(p.id);
      close101();
    }
  }, gxHideSet().has(p.id) ? "Show" : "Hide"))) : null), eid && img ? /*#__PURE__*/React.createElement("img", {
    className: "ph",
    alt: "",
    src: "https://a.espncdn.com/i/headshots/nhl/players/full/" + eid + ".png",
    onError: () => setImg(false)
  }) : null), /*#__PURE__*/React.createElement("div", {
    className: "strip"
  }, /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("b", null, rk || "-"), /*#__PURE__*/React.createElement("span", null, "POS RANK")), /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("b", null, avgSoFar == null ? "-" : f1(avgSoFar)), /*#__PURE__*/React.createElement("span", null, "AVG FPTS")), /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("b", null, f1(p.tot || 0)), /*#__PURE__*/React.createElement("span", null, "SEASON FPTS")), /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("b", null, p.own != null ? p.own >= 99.5 ? Math.round(p.own) : f1(p.own) : "-"), /*#__PURE__*/React.createElement("span", null, "%ROST (" + (p.chg ? (p.chg > 0 ? "+" : "") + f1(p.chg) : "+0") + ")")))), hurt ? /*#__PURE__*/React.createElement("div", {
    className: "gx-pdm-inj"
  }, /*#__PURE__*/React.createElement("span", {
    className: "pill"
  }, stTxt.toUpperCase()), back.d ? /*#__PURE__*/React.createElement("span", null, "Est. return " + dayLabel(back.d)) : null) : null, /*#__PURE__*/React.createElement("div", {
    className: "gx-pd-hd"
  }, /*#__PURE__*/React.createElement("div", {
    className: "gx-pd-ph"
  }, /*#__PURE__*/React.createElement("span", {
    className: "lg"
  }, /*#__PURE__*/React.createElement(TeamLogo, {
    t: p.t,
    size: 44
  })), eid && img ? /*#__PURE__*/React.createElement("img", {
    alt: p.n,
    src: "https://a.espncdn.com/i/headshots/nhl/players/full/" + eid + ".png",
    onError: () => setImg(false)
  }) : /*#__PURE__*/React.createElement("span", {
    className: "ini"
  }, (first[0] || "") + (last[0] || ""))), /*#__PURE__*/React.createElement("div", {
    className: "min-w-0"
  }, /*#__PURE__*/React.createElement("div", {
    className: "gx-pd-nm"
  }, no != null ? /*#__PURE__*/React.createElement("span", {
    className: "gx-pd-no"
  }, "#" + no) : null, /*#__PURE__*/React.createElement("div", {
    className: "min-w-0"
  }, /*#__PURE__*/React.createElement("div", {
    className: "f truncate"
  }, first), /*#__PURE__*/React.createElement("div", {
    className: "l truncate"
  }, last))), /*#__PURE__*/React.createElement("div", {
    className: "gx-pd-tm truncate"
  }, tName, gxGS106(p) ? " \u00b7 " + gxGsTxt106(p) + " (" + gxGS106(p).pct + ")" : ""), /*#__PURE__*/React.createElement("div", {
    className: "gx-pd-kv"
  }, /*#__PURE__*/React.createElement("span", {
    className: "k"
  }, "Elig"), /*#__PURE__*/React.createElement("span", null, elig), /*#__PURE__*/React.createElement("span", {
    className: "k"
  }, "Manager"), /*#__PURE__*/React.createElement("span", {
    className: "truncate"
  }, owner), /*#__PURE__*/React.createElement("span", {
    className: "k"
  }, "Status"), /*#__PURE__*/React.createElement("span", null, stTxt, /*#__PURE__*/React.createElement("span", {
    className: "gx-pd-dot",
    style: {
      background: stCol
    }
  })))), /*#__PURE__*/React.createElement("div", {
    className: "gx-pd-st"
  }, /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    className: "k"
  }, "Position rank"), /*#__PURE__*/React.createElement("div", {
    className: "v"
  }, rk || "-", /*#__PURE__*/React.createElement("small", null, rk ? posWord : ""))), /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    className: "k"
  }, "Average points"), /*#__PURE__*/React.createElement("div", {
    className: "v"
  }, avgSoFar == null ? "-" : f1(avgSoFar))), /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    className: "k"
  }, "Projected"), /*#__PURE__*/React.createElement("div", {
    className: "v"
  }, proj == null ? "-" : f1(proj))), /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    className: "k"
  }, "% rostered"), /*#__PURE__*/React.createElement("div", {
    className: "v"
  }, p.own != null ? f1(p.own) : "-", /*#__PURE__*/React.createElement("small", null, p.chg ? "(" + (p.chg > 0 ? "+" : "") + f1(p.chg) + ")" : "(+0)"))))), Q ? /*#__PURE__*/React.createElement("div", {
    className: "gx-pd-ac"
  }, /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: "pr",
    onClick: act(Q.swap)
  }, Q.mine(p) ? "Find a replacement" : "Find a swap"), Q.tradeable(p) ? /*#__PURE__*/React.createElement("button", {
    type: "button",
    onClick: act(Q.trade)
  }, "Add to a trade") : null, /*#__PURE__*/React.createElement("button", {
    type: "button",
    onClick: () => Q.espn(p)
  }, Q.fa(p) ? "Add on ESPN" : "Open on ESPN"), Q.fa(p) ? /*#__PURE__*/React.createElement(GxPdWatch, {
    p: p,
    Q: Q
  }) : null, Q.fa(p) ? /*#__PURE__*/React.createElement("button", {
    type: "button",
    onClick: () => {
      gxHide.toggle(p.id);
      onClose();
    }
  }, gxHideSet().has(p.id) ? "Show in pickups" : "Hide from pickups") : null) : null, /*#__PURE__*/React.createElement("div", {
    className: "gx-pd-tb"
  }, tabs.map(([k, l]) => /*#__PURE__*/React.createElement("button", {
    key: k,
    type: "button",
    className: tab === k ? "on" : "",
    onClick: () => setTab(k)
  }, l))), /*#__PURE__*/React.createElement("div", {
    className: "gx-pd-bd",
    key: tab
  }, hurt && tab === "ov" ? /*#__PURE__*/React.createElement("div", {
    className: "gx-pd-pn m-hide",
    style: {
      color: "var(--bad)",
      fontSize: 14
    }
  }, stTxt, back.d ? GXPD_DOT + "back around " + dayLabel(back.d) : "", inj && inj.note ? GXPD_DOT + inj.note : "") : null, tab === "ov" ? /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("div", {
    className: "gx-pd-pn"
  }, /*#__PURE__*/React.createElement("div", {
    className: "gx-pd-h"
  }, "Stats", /*#__PURE__*/React.createElement("span", {
    className: "r"
  }, "fantasy points (FPTS) by your league's scoring")), log === null ? /*#__PURE__*/React.createElement("div", {
    className: "text-sm text-slate-500"
  }, "Loading games...") : /*#__PURE__*/React.createElement("table", {
    className: "gx-pd-t"
  }, /*#__PURE__*/React.createElement("thead", null, /*#__PURE__*/React.createElement("tr", null, /*#__PURE__*/React.createElement("th", null), SH.map(h => /*#__PURE__*/React.createElement("th", {
    key: h
  }, h)))), /*#__PURE__*/React.createElement("tbody", null, statRows.map(([l, r]) => /*#__PURE__*/React.createElement("tr", {
    key: l
  }, /*#__PURE__*/React.createElement("td", null, l), statCells(r).map((v, i) => /*#__PURE__*/React.createElement("td", {
    key: i,
    className: i === SH.length - 1 ? "b" : ""
  }, r.gp ? v : i ? "-" : 0))))))), /*#__PURE__*/React.createElement("div", {
    className: "gx-pd-pn"
  }, /*#__PURE__*/React.createElement("div", {
    className: "gx-pd-h"
  }, "This week"), /*#__PURE__*/React.createElement("div", {
    className: "gx-pd-tl"
  }, /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    className: "k"
  }, "Per game"), /*#__PURE__*/React.createElement("div", {
    className: "v"
  }, proj == null ? "-" : f1(proj)), /*#__PURE__*/React.createElement("div", {
    className: "s"
  }, isG ? gxGS106(p) ? "starts " + gxGS106(p).pct : "" : "ESPN " + f1(p.avg || 0))), /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    className: "k"
  }, "Rest of this week"), /*#__PURE__*/React.createElement("div", {
    className: "v"
  }, eid ? f1(wkPts) : "-"), /*#__PURE__*/React.createElement("div", {
    className: "s"
  }, wkIdx.length + " game" + (wkIdx.length === 1 ? "" : "s") + " left")), /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    className: "k"
  }, "Season points"), /*#__PURE__*/React.createElement("div", {
    className: "v"
  }, f1(p.tot || 0)), /*#__PURE__*/React.createElement("div", {
    className: "s"
  }, (p.gp || 0) + " GP"))), nextG.length ? /*#__PURE__*/React.createElement("table", {
    className: "gx-pd-t",
    style: {
      marginTop: 10
    }
  }, /*#__PURE__*/React.createElement("thead", null, /*#__PURE__*/React.createElement("tr", null, /*#__PURE__*/React.createElement("th", null, "Next games"), /*#__PURE__*/React.createElement("th", null, "Opp"), /*#__PURE__*/React.createElement("th", null, "Proj"))), /*#__PURE__*/React.createElement("tbody", null, nextG.map(g => {
    const r = per(g.d),
      lv = gState(p.t, g.d).s !== "P",
      a = lv ? gxPdReal(p, g.d) : null;
    return /*#__PURE__*/React.createElement("tr", {
      key: g.d,
      className: lv ? "lv" : ""
    }, /*#__PURE__*/React.createElement("td", null, dayLabel(g.d)), /*#__PURE__*/React.createElement("td", null, /*#__PURE__*/React.createElement("span", {
      className: "inline-flex items-center gap-1 justify-end"
    }, g.h ? "vs" : "@", " ", /*#__PURE__*/React.createElement(TeamLogo, {
      t: g.o,
      size: 16
    }), " ", g.o)), /*#__PURE__*/React.createElement("td", {
      className: "b"
    }, lv ? /*#__PURE__*/React.createElement(React.Fragment, null, a == null ? "-" : f1(a), " ", /*#__PURE__*/React.createElement(LiveTag, {
      st: gState(p.t, g.d).s,
      t: p.t,
      dt: g.d
    })) : r ? f1(r.x) : ""));
  }))) : null, eid ? /*#__PURE__*/React.createElement("div", {
    style: {
      marginTop: 8
    }
  }, /*#__PURE__*/React.createElement(Tags, {
    p: p,
    K: K
  })) : null), log && log.length ? /*#__PURE__*/React.createElement("div", {
    className: "gx-pd-pn",
    "data-gx": "101log"
  }, /*#__PURE__*/React.createElement("div", {
    className: "gx-pd-h"
  }, "Game log"), /*#__PURE__*/React.createElement("table", {
    className: "gx-pd-t"
  }, /*#__PURE__*/React.createElement("thead", null, /*#__PURE__*/React.createElement("tr", null, /*#__PURE__*/React.createElement("th", null, "Date"), /*#__PURE__*/React.createElement("th", null, "Opp"), /*#__PURE__*/React.createElement("th", null, "FPTS"), isG ? /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("th", null, "Dec"), /*#__PURE__*/React.createElement("th", null, "SV"), /*#__PURE__*/React.createElement("th", null, "GA")) : /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("th", null, "TOI"), /*#__PURE__*/React.createElement("th", null, "G"), /*#__PURE__*/React.createElement("th", null, "A"), /*#__PURE__*/React.createElement("th", null, "+/-")))), /*#__PURE__*/React.createElement("tbody", null, log.slice(0, 6).map(r => {
    const x = r.x,
      gm = (((window.GAMES_DATA || {}).games || {})[r.d] || {})[p.t] || null,
      o = x.o || (gm ? gm.o : ""),
      h = x.o ? x.h : gm ? gm.h : null;
    return /*#__PURE__*/React.createElement("tr", {
      key: r.d
    }, /*#__PURE__*/React.createElement("td", null, r.d.slice(5).replace("-", "/")), /*#__PURE__*/React.createElement("td", null, o ? (h ? "" : "@") + o : ""), /*#__PURE__*/React.createElement("td", {
      className: "b"
    }, r.dnp ? "-" : f1(r.fp)), isG ? /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("td", null, x.dec === "O" ? "OTL" : x.dec || "-"), /*#__PURE__*/React.createElement("td", null, x.sv || 0), /*#__PURE__*/React.createElement("td", null, x.ga || 0)) : /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("td", null, x.toi || "-"), /*#__PURE__*/React.createElement("td", null, x.g || 0), /*#__PURE__*/React.createElement("td", null, x.a || 0), /*#__PURE__*/React.createElement("td", null, gxPdSigned(x.pm))));
  }))), /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: "gx-pd-more",
    onClick: () => setTab("log")
  }, "See full game log")) : null) : null, tab === "log" ? /*#__PURE__*/React.createElement("div", {
    className: "gx-pd-pn"
  }, /*#__PURE__*/React.createElement("div", {
    className: "gx-pd-h"
  }, "Game log", /*#__PURE__*/React.createElement("span", {
    className: "r"
  }, log && log.length ? log.length + " games" : "")), log === null ? /*#__PURE__*/React.createElement("div", {
    className: "text-sm text-slate-500"
  }, "Loading games...") : !log.length ? /*#__PURE__*/React.createElement("div", {
    className: "text-sm text-slate-500"
  }, "No games saved yet.") : /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("table", {
    className: "gx-pd-t"
  }, /*#__PURE__*/React.createElement("thead", null, /*#__PURE__*/React.createElement("tr", null, /*#__PURE__*/React.createElement("th", null, "Date"), /*#__PURE__*/React.createElement("th", null, "Opp"), isG ? /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("th", null, "Dec"), /*#__PURE__*/React.createElement("th", null, "SV"), /*#__PURE__*/React.createElement("th", null, "GA"), /*#__PURE__*/React.createElement("th", {
    className: "m-hide"
  }, "SV%")) : /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("th", {
    className: "m-hide"
  }, "TOI"), /*#__PURE__*/React.createElement("th", null, "G"), /*#__PURE__*/React.createElement("th", null, "A"), /*#__PURE__*/React.createElement("th", null, "+/-"), /*#__PURE__*/React.createElement("th", {
    className: "m-hide"
  }, "PIM"), /*#__PURE__*/React.createElement("th", null, "SOG")), /*#__PURE__*/React.createElement("th", null, "FPTS"))), /*#__PURE__*/React.createElement("tbody", null, log.slice(0, nLog).map(r => {
    const x = r.x,
      gm = (((window.GAMES_DATA || {}).games || {})[r.d] || {})[p.t] || null,
      o = x.o || (gm ? gm.o : ""),
      h = x.o ? x.h : gm ? gm.h : null;
    return /*#__PURE__*/React.createElement("tr", {
      key: r.d,
      className: r.st === "L" ? "lv" : ""
    }, /*#__PURE__*/React.createElement("td", null, r.d.slice(5).replace("-", "/")), /*#__PURE__*/React.createElement("td", null, o ? (h ? "" : "@") + o : ""), isG ? /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("td", null, x.dec === "O" ? "OTL" : x.dec || "-"), /*#__PURE__*/React.createElement("td", null, x.sv || 0), /*#__PURE__*/React.createElement("td", null, x.ga || 0), /*#__PURE__*/React.createElement("td", {
      className: "m-hide"
    }, x.svp != null ? svp(Number(x.svp)) : "-")) : /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("td", {
      className: "m-hide"
    }, x.toi || "-"), /*#__PURE__*/React.createElement("td", null, x.g || 0), /*#__PURE__*/React.createElement("td", null, x.a || 0), /*#__PURE__*/React.createElement("td", null, gxPdSigned(x.pm)), /*#__PURE__*/React.createElement("td", {
      className: "m-hide"
    }, x.pim || 0), /*#__PURE__*/React.createElement("td", null, x.sog || 0)), /*#__PURE__*/React.createElement("td", {
      className: "b"
    }, r.dnp ? "-" : f1(r.fp), r.est ? "*" : ""));
  }))), log.length > nLog ? /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: "gx-pd-more",
    onClick: () => setNLog(nLog + 20)
  }, "Show more") : null, log.some(r => r.est) ? /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500",
    style: {
      marginTop: 8
    }
  }, "* worked out from the box score, without power-play or shorthanded points.") : null)) : null, tab === "news" ? /*#__PURE__*/React.createElement("div", {
    className: "gx-pd-pn"
  }, /*#__PURE__*/React.createElement("div", {
    className: "gx-pd-h"
  }, "Recent news"), inj && inj.note ? /*#__PURE__*/React.createElement("div", {
    className: "gx-pd-nw"
  }, /*#__PURE__*/React.createElement("div", {
    className: "d"
  }, "Injury"), /*#__PURE__*/React.createElement("div", {
    style: {
      color: "var(--bad)"
    }
  }, inj.note)) : null, news.length ? /*#__PURE__*/React.createElement(GxPdNews, {
    items: news
  }) : !(inj && inj.note) ? /*#__PURE__*/React.createElement("div", {
    className: "text-sm text-slate-500"
  }, "No news for him in the last few days.") : null) : null, tab === "lines" ? /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("div", {
    className: "gx-pd-pn"
  }, /*#__PURE__*/React.createElement("div", {
    className: "gx-pd-h"
  }, "Where he plays for " + p.t, /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: "r text-blue-600",
    onClick: act(() => window.__NAV && window.__NAV.lines(p.t))
  }, "All team lines")), !slots.length ? /*#__PURE__*/React.createElement("div", {
    className: "text-sm",
    style: {
      color: "var(--warn)"
    }
  }, "Not in " + p.t + "'s current Daily Faceoff lineup (scratched, injured, in the minors, or not read yet).") : slots.sort().map(k => /*#__PURE__*/React.createElement("div", {
    key: k,
    className: "gx-pd-nw"
  }, /*#__PURE__*/React.createElement("div", {
    className: "d"
  }, GX_PD_SLOT[k] || k), /*#__PURE__*/React.createElement("div", null, (ln[k] || []).filter(n => nrm(n) !== me).map(n => {
    const q = mateP(n);
    return q ? /*#__PURE__*/React.createElement("button", {
      key: n,
      type: "button",
      className: "gx-pd-mt",
      onClick: () => window.__NAV && window.__NAV.player(q)
    }, n) : /*#__PURE__*/React.createElement("span", {
      key: n,
      className: "gx-pd-mt text-slate-500"
    }, n);
  })))), !isG && slots.length && !slots.some(k => k[0] === "P") ? /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500",
    style: {
      marginTop: 6
    }
  }, "Not on a power-play or penalty-kill unit.") : null), chg.length ? /*#__PURE__*/React.createElement("div", {
    className: "gx-pd-pn"
  }, /*#__PURE__*/React.createElement("div", {
    className: "gx-pd-h"
  }, "Recent changes"), chg.map(c => /*#__PURE__*/React.createElement("div", {
    key: c.id,
    className: "gx-pd-nw"
  }, /*#__PURE__*/React.createElement("div", {
    className: "d"
  }, dayLabel(String(c.at || "").slice(0, 10))), /*#__PURE__*/React.createElement("div", null, c.text)))) : null) : null)));
}
function GxPdNews({
  items
}) {
  return items.map((n, i) => /*#__PURE__*/React.createElement("div", {
    key: i,
    className: "gx-pd-nw"
  }, /*#__PURE__*/React.createElement("div", {
    className: "d"
  }, n.d), /*#__PURE__*/React.createElement("a", {
    href: n.u,
    target: "_blank",
    rel: "noreferrer",
    style: {
      color: n.tone === "-" ? "var(--bad)" : "var(--ink)"
    }
  }, n.h)));
}
function GxPdWatch({
  p,
  Q
}) {
  const [, tick] = useState(0);
  return /*#__PURE__*/React.createElement("button", {
    type: "button",
    onClick: () => {
      Q.star(p);
      tick(x => x + 1);
    }
  }, Q.starred(p) ? "Watching" : "Watch");
}
// if the new screen ever breaks, fall back to the old pop-up
class GxPdSafe extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      bad: false
    };
  }
  static getDerivedStateFromError() {
    return {
      bad: true
    };
  }
  componentDidCatch(e) {
    try {
      console.error("player screen (095)", e);
    } catch (x) {}
  }
  render() {
    const P = this.props;
    if (this.state.bad) return window.PlayerPopup ? /*#__PURE__*/React.createElement(window.PlayerPopup, {
      p: P.p,
      s: P.s,
      wk: P.wk,
      H: P.H,
      onClose: P.onClose
    }) : null;
    return /*#__PURE__*/React.createElement(GxPlayerDetail, {
      p: P.p,
      s: P.s,
      wk: P.wk,
      onClose: P.onClose
    });
  }
}
// ---------- change 096: player faces beside names (install.py) ----------
// a round ESPN headshot with a small team logo badge; the plain team logo if there is no photo
function GxFace({
  p,
  t,
  size
}) {
  const [bad, setBad] = useState(false);
  const tm = p && p.t || t,
    z = size || 28;
  const eid = p && typeof p.id === "string" && p.id[0] === "e" ? p.id.slice(1) : null;
  if (!eid || bad) return /*#__PURE__*/React.createElement(TeamLogo, {
    t: tm,
    size: size
  });
  const b = Math.max(11, Math.round(z * 0.5));
  return /*#__PURE__*/React.createElement("span", {
    className: "gx-face",
    style: {
      width: "calc(" + z + "px * var(--gx-fs, 1))",
      height: "calc(" + z + "px * var(--gx-fs, 1))"
    },
    title: (p.n || "") + " (" + tm + ")"
  }, /*#__PURE__*/React.createElement("span", {
    className: "c"
  }, /*#__PURE__*/React.createElement("img", {
    src: "https://a.espncdn.com/i/headshots/nhl/players/full/" + eid + ".png",
    alt: "",
    loading: "lazy",
    onError: () => setBad(true)
  })), /*#__PURE__*/React.createElement("span", {
    className: "bd",
    style: {
      width: b,
      height: b
    }
  }, /*#__PURE__*/React.createElement(TeamLogo, {
    t: tm,
    size: b - 2
  })));
}
// ---------- change 098: phone Matchup in ESPN's layout (install.py) ----------
// opponent before the score on the phone, e.g. "@WPG"
function gxOpp98(p) {
  const g = gameOf(p.t, p.dt);
  return g ? /*#__PURE__*/React.createElement("span", {
    className: "m-inl"
  }, (g.h ? "" : "@") + g.o + " ") : null;
}
// ---------- change 099: today's game and stat line columns for rosters (install.py) ----------
const GX_ST99 = ["G", "A", "+/-", "SOG", "HIT", "BLK", "SV", "GA", "TOI"];
function gxToday99(p) {
  const td = todayISO(),
    g = p.ir ? null : gameOf(p.t, td),
    st = g ? gState(p.t, td).s : null,
    sc = g && st !== "P" ? gScore(p.t, td) : null;
  let opp = "-",
    res = "";
  if (g) {
    opp = (g.h ? "" : "@") + g.o;
    res = st === "P" ? gameTime(g) : sc && sc.my != null ? sc.my + "-" + sc.op + (st === "F" ? " Final" : sc.per ? " " + sc.per : "") : st === "F" ? "Final" : "Live";
  }
  const a = st && st !== "P" ? gxPdReal(p, td) : null;
  return [/*#__PURE__*/React.createElement("div", {
    key: "t99a",
    className: "gx-op99"
  }, /*#__PURE__*/React.createElement("div", null, opp), res ? /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500"
  }, res) : null), /*#__PURE__*/React.createElement("div", {
    key: "t99b",
    className: "n font-semibold"
  }, a == null ? "-" : f1(a))];
}
function gxStats99(p) {
  const td = todayISO(),
    x = gState(p.t, td).s !== "P" ? pStat(p, td) : null,
    d = "-";
  const v = !x ? GX_ST99.map(() => d) : p.p === "G" ? [d, d, d, d, d, d, x.sv != null ? x.sv : d, x.ga != null ? x.ga : d, x.toi || d] : [x.g || 0, x.a || 0, gxPdSigned(x.pm), x.sog || 0, x.hit || 0, x.blk || 0, d, d, x.toi || d];
  return v.map((c, i) => /*#__PURE__*/React.createElement("div", {
    key: "s99" + i,
    className: "n text-slate-500"
  }, c));
}
// ---------- change 100: stats range picker for rosters (install.py) ----------
const GX_RNG100 = [["today", "Today"], ["l7", "Last 7 days"], ["l15", "Last 15 days"], ["l30", "Last 30 days"], ["sea", "Season"], ["n7", "Next 7 days (projected)"], ["n30", "Next 30 days (projected)"], ["ros", "Rest of season (projected)"]];
const GX_C100 = ["GP", "G", "A", "+/-", "PIM", "SOG", "HIT", "BLK", "TOI", "W", "SV", "GA", "SV%", "FPTS", "Avg"];
const gxRng100 = () => {
  const v = uiGet().gxRng100;
  return GX_RNG100.some(r => r[0] === v) ? v : "sea";
};
const gxProjR100 = r => r === "n7" || r === "n30" || r === "ros";
const GX100 = window.__GX100 = window.__GX100 || {
  data: {},
  busy: {}
};
// past ranges: every saved box score day in the range (plus today's and yesterday's live lines)
function gxLoad100(rng) {
  if (gxProjR100(rng) || GX100.data[rng] || GX100.busy[rng]) return;
  GX100.busy[rng] = true;
  const td = todayISO(),
    from = rng === "today" ? td : rng === "sea" ? "0000" : addDays(td, -{
      l7: 6,
      l15: 14,
      l30: 29
    }[rng]);
  const P = (window.ESPN_DATA || {}).pstat || {};
  gxBoxIdx().then(idx => {
    const ds = (idx || []).filter(d => d >= from && d <= td);
    return Promise.all(ds.map(d => gxBoxDay(d).then(day => [d, day || {}]))).then(list => {
      const have = new Set(ds);
      Object.keys(P).forEach(d => {
        if (d >= from && d <= td && !have.has(d)) list.push([d, P[d] || {}]);
      });
      return list;
    });
  }).then(list => {
    const o = {};
    list.forEach(([d, day]) => Object.keys(day).forEach(id => {
      if (day[id]) (o[id] = o[id] || []).push(day[id]);
    }));
    GX100.data[rng] = o;
  }).catch(() => {
    GX100.data[rng] = {};
  }).then(() => {
    GX100.busy[rng] = false;
    window.dispatchEvent(new Event("gx-rng100"));
  });
}
function gxAgg100(list, isG, sc) {
  if (!list || !list.length) return GX_C100.map((h, i) => i === 0 ? 0 : "-");
  const n = list.length,
    S = f => list.reduce((a, x) => a + (+f(x) || 0), 0);
  const fp = S(x => x.fp != null ? x.fp : gxEst(x, sc));
  const ts = list.map(x => gxPdSec(x.toi)).filter(v => v != null);
  const toi = ts.length ? gxPdMS(ts.reduce((a, v) => a + v, 0) / ts.length) : "-";
  if (isG) {
    const sv = S(x => x.sv),
      sa = S(x => x.sa != null ? x.sa : (x.sv || 0) + (x.ga || 0));
    return [n, "-", "-", "-", "-", "-", "-", "-", toi, list.filter(x => x.dec === "W").length, sv, S(x => x.ga), sa ? (sv / sa).toFixed(3).replace(/^0/, "") : "-", f1(fp), f1(fp / n)];
  }
  return [n, S(x => x.g), S(x => x.a), gxPdSigned(S(x => x.pm)), S(x => x.pim), S(x => x.sog), Math.round(S(x => x.hit)), S(x => x.blk), toi, "-", "-", "-", "-", f1(fp), f1(fp / n)];
}
// projected ranges: games left and projected fantasy points (the app does not project goals or shots)
function gxProj100(p, s, rng) {
  const td = todayISO(),
    K = s.blend,
    S = SCHED[p.t];
  if (!S || p.ir) return GX_C100.map((h, i) => i === 0 ? 0 : "-");
  const end = rng === "n7" ? addDays(td, 6) : rng === "n30" ? addDays(td, 29) : "9999";
  let n = 0,
    x = 0;
  [...S].sort().forEach(d => {
    if (d < td || d > end || d === td && gState(p.t, d).s !== "P") return;
    const av = avail(p, d);
    if (!(av > 0)) return;
    const g = p.p === "G" ? gStart(p, d) : null;
    n += 1;
    x += effAvg(p, K, d) * (g ? g.v : 1) * av;
  });
  return [n, "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", f1(x), n ? f1(x / n) : "-"];
}
const gxUse100 = () => {
  const [, tick] = useState(0);
  useEffect(() => {
    const f = () => tick(x => x + 1);
    window.addEventListener("gx-rng100", f);
    return () => window.removeEventListener("gx-rng100", f);
  }, []);
  return gxRng100();
};
function GxSC100({
  p,
  s
}) {
  const rng = gxUse100();
  useEffect(() => {
    gxLoad100(rng);
  });
  const eid = String(p.id || "").replace(/^e/, "");
  let v;
  if (gxProjR100(rng)) v = gxProj100(p, s, rng);else {
    const D = GX100.data[rng];
    v = D ? gxAgg100(D[eid], p.p === "G", s.sc || {}) : GX_C100.map(() => "...");
  }
  return v.map((c, i) => /*#__PURE__*/React.createElement("div", {
    key: "c100" + i,
    className: "n " + (i >= 13 ? "font-semibold" : "text-slate-500")
  }, c));
}
function GxSH100() {
  const rng = gxUse100();
  return GX_C100.map((h, i) => /*#__PURE__*/React.createElement("span", {
    key: h,
    className: "n"
  }, gxProjR100(rng) && i === 0 ? "Gms" : h));
}
function GxRngSel100() {
  const rng = gxUse100();
  return /*#__PURE__*/React.createElement("div", {
    className: "gx-rs100"
  }, /*#__PURE__*/React.createElement("span", {
    className: "text-xs text-slate-500"
  }, "Stats"), /*#__PURE__*/React.createElement("select", {
    className: inp,
    value: rng,
    onChange: e => {
      uiSet("gxRng100", e.target.value);
      window.dispatchEvent(new Event("gx-rng100"));
    }
  }, GX_RNG100.map(([k, l]) => /*#__PURE__*/React.createElement("option", {
    key: k,
    value: k
  }, l))));
}
// ---------- change 101: team colours for the phone player header (install.py) ----------
const GX_TC101 = {
  ANA: "#F47A38",
  BOS: "#FFB81C",
  BUF: "#003087",
  CGY: "#C8102E",
  CAR: "#CE1126",
  CHI: "#CF0A2C",
  COL: "#6F263D",
  CBJ: "#002654",
  DAL: "#006847",
  DET: "#CE1126",
  EDM: "#FF4C00",
  FLA: "#C8102E",
  LA: "#A2AAAD",
  MIN: "#154734",
  MTL: "#AF1E2D",
  NSH: "#FFB81C",
  NJ: "#CE1126",
  NYI: "#00539B",
  NYR: "#0038A8",
  OTT: "#C52032",
  PHI: "#F74902",
  PIT: "#FCB514",
  SJ: "#006D75",
  SEA: "#355464",
  STL: "#002F87",
  TB: "#002868",
  TOR: "#00205B",
  UTA: "#6CACE4",
  VAN: "#00205B",
  VGK: "#B4975A",
  WSH: "#C8102E",
  WPG: "#041E42"
};
const gxTC101 = t => GX_TC101[t] || "#555555";
// ---------- change 102: Pickups list remembered until the next sync (install.py) ----------
const GX102 = new WeakMap();
function gxMoves102(s, sP, o) {
  let m = GX102.get(s);
  if (!m) {
    m = new Map();
    GX102.set(s, m);
  }
  const key = [o.H, o.pos, o.q, window.__PMODE, [...gxHideSet()].sort().join(",")].join("|");
  if (!m.has(key)) m.set(key, computeMoves(sP, o));
  return m.get(key);
}
// work out the default Pickups list quietly after the app has loaded, so the first visit is quick
function gxPrewarm102(s) {
  const run = () => {
    try {
      gxMoves102(s, planS(s), {
        H: 1,
        pos: "all",
        q: ""
      });
    } catch (e) {}
  };
  if (window.requestIdleCallback) window.requestIdleCallback(run, {
    timeout: 4000
  });else setTimeout(run, 1500);
}
// ---------- change 103: new layout, tabs at the top (install.py) ----------
const GX_TABS103 = [["roster", "Roster", "myteam", null], ["matchup", "Matchup", "matchup", null], ["players", "Players", "moves", "adddrop"], ["lines", "Lines", "lines", null], ["trades", "Trades", "moves", "trades"], ["league", "League", "league", "power"], ["setup", "Setup", "setup", "settings"]];
const gxTabOn103 = (k, tab) => {
  const sub = (window.__ROUTE || {}).sub;
  return k === "roster" ? tab === "myteam" || tab === "today" : k === "matchup" ? tab === "matchup" : k === "players" ? tab === "moves" && sub !== "trades" : k === "trades" ? tab === "moves" && sub === "trades" : k === "lines" ? tab === "lines" : k === "league" ? tab === "league" || tab === "teams" : tab === "setup" || tab === "news";
};
function GxTopM103({
  s,
  tab,
  go,
  ageH
}) {
  const ref = React.useRef(null);
  const sub = (window.__ROUTE || {}).sub;
  useEffect(() => {
    const n = ref.current,
      el = n && n.querySelector(".on");
    if (el) {
      try {
        n.scrollTo({
          left: el.offsetLeft - n.clientWidth / 2 + el.clientWidth / 2,
          behavior: "smooth"
        });
      } catch (e) {}
    }
  }, [tab, sub]);
  const dot = !s.lastSync ? "var(--faint)" : ageH !== null && ageH > 2 ? "var(--bad)" : "var(--good)";
  const name = teamName(s, s.me) || "Islands GM";
  return /*#__PURE__*/React.createElement("div", {
    className: "m-only gx-tm103"
  }, /*#__PURE__*/React.createElement("div", {
    className: "hd"
  }, /*#__PURE__*/React.createElement("span", {
    className: "gx-badge"
  }, (name[0] || "K").toUpperCase()), /*#__PURE__*/React.createElement("span", {
    className: "nm"
  }, name), /*#__PURE__*/React.createElement("span", {
    className: "dt",
    style: {
      background: dot
    },
    title: s.lastSync ? "Synced " + fmtTime(s.lastSync) : "Not synced yet"
  }), /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: "sr",
    "aria-label": "Search",
    onClick: () => window.dispatchEvent(new Event("gm-search"))
  }, /*#__PURE__*/React.createElement("svg", {
    viewBox: "0 0 24 24",
    fill: "none",
    stroke: "currentColor",
    strokeWidth: "2",
    strokeLinecap: "round"
  }, /*#__PURE__*/React.createElement("circle", {
    cx: "11",
    cy: "11",
    r: "7"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M20 20l-3.5-3.5"
  })))), /*#__PURE__*/React.createElement("nav", {
    className: "tb",
    ref: ref,
    "aria-label": "Main"
  }, GX_TABS103.map(([k, l, t, sb]) => /*#__PURE__*/React.createElement("a", {
    key: k,
    href: gxHash(t, sb || undefined),
    className: gxTabOn103(k, tab) ? "on" : "",
    onClick: e => {
      if (gxNewTab(e)) return;
      e.preventDefault();
      go(t, sb || undefined);
    }
  }, l))));
}
const GX_PL103 = [["adddrop", "Free agents"], ["goalies", "Goalies"], ["injuries", "Injuries"]];
function GxSubBar103({
  tab,
  sub,
  go,
  s,
  wk
}) {
  if (tab === "matchup") return s && wk ? /*#__PURE__*/React.createElement(MatchStrip, {
    s: s,
    wk: wk
  }) : null;
  if (tab === "moves" && sub !== "trades") {
    if (sub === "planner" || sub === "advice" || sub === "players") return /*#__PURE__*/React.createElement("div", {
      className: "mb-3"
    }, /*#__PURE__*/React.createElement("button", {
      type: "button",
      className: "text-sm text-blue-600",
      onClick: () => go("moves", "adddrop")
    }, "\u2039 Back to Free agents"));
    const cur = GX_PL103.some(x => x[0] === sub) ? sub : "adddrop";
    return /*#__PURE__*/React.createElement("div", {
      className: "gx-seg103 mb-3"
    }, GX_PL103.map(([k, l]) => /*#__PURE__*/React.createElement("button", {
      key: k,
      type: "button",
      className: cur === k ? "on" : "",
      onClick: () => go("moves", k)
    }, l)));
  }
  const back = tab === "news" || tab === "setup" && sub && sub !== "settings" ? ["Setup", () => go("setup", "settings")] : tab === "league" && (sub === "playoffs" || sub === "players") ? ["League", () => go("league", "power")] : null;
  return back ? /*#__PURE__*/React.createElement("div", {
    className: "mb-3"
  }, /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: "text-sm text-blue-600",
    onClick: back[1]
  }, "\u2039 Back to " + back[0])) : null;
}
// the boxes that used to sit lower on Today, now under the Matchup
function GxMuMore103({
  s,
  wk
}) {
  const K = s.blend,
    opp = oppOf(wk, s.me) || s.opp;
  const A = useMemo(() => weekLive(s.players.filter(p => p.ft === s.me), wk, K, s.me), [s.players, wk, K, window.__LIVEV120]);
  const B = useMemo(() => weekLive(s.players.filter(p => p.ft === opp), wk, K, opp), [s.players, wk, K, opp, window.__LIVEV120]);
  return /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement(GxGamesAny, {
    s: s,
    wk: wk,
    A: A,
    B: B
  }), /*#__PURE__*/React.createElement(GxLeagueAny, {
    s: s,
    wk: wk
  }), /*#__PURE__*/React.createElement(GxCarry, {
    s: s,
    wk: wk
  }));
}
// ---------- change 104: separate skater and goalie stat columns (install.py) ----------
const GX_SK104 = ["GP", "G", "A", "PTS", "+/-", "PIM", "SOG", "HIT", "BLK", "TOI", "FPTS", "Avg"];
const GX_GO104 = ["GP", "W", "L", "OTL", "GA", "SV", "SV%", "GAA", "SO", "TOI", "FPTS", "GS%"];
function gxAgg104(list, isG, sc) {
  const C = isG ? GX_GO104 : GX_SK104;
  if (!list || !list.length) return C.map((h, i) => i === 0 ? 0 : "-");
  const n = list.length,
    S = f => list.reduce((a, x) => a + (+f(x) || 0), 0);
  const fp = S(x => x.fp != null ? x.fp : gxEst(x, sc));
  const ts = list.map(x => gxPdSec(x.toi)).filter(v => v != null),
    tot = ts.reduce((a, v) => a + v, 0);
  const toi = ts.length ? gxPdMS(tot / ts.length) : "-";
  if (isG) {
    const sv = S(x => x.sv),
      ga = S(x => x.ga),
      sa = S(x => x.sa != null ? x.sa : (x.sv || 0) + (x.ga || 0));
    return [n, list.filter(x => x.dec === "W").length, list.filter(x => x.dec === "L").length, list.filter(x => x.dec === "O").length, ga, sv, sa ? (sv / sa).toFixed(3).replace(/^0/, "") : "-", tot ? (ga * 3600 / tot).toFixed(2) : "-", list.filter(x => x.dec === "W" && !x.ga).length, toi, f1(fp), f1(fp / n)];
  }
  const g = S(x => x.g),
    a = S(x => x.a);
  return [n, g, a, g + a, gxPdSigned(S(x => x.pm)), S(x => x.pim), S(x => x.sog), Math.round(S(x => x.hit)), S(x => x.blk), toi, f1(fp), f1(fp / n)];
}
function GxSC104({
  p,
  s
}) {
  const rng = gxUse100();
  useEffect(() => {
    gxLoad100(rng);
  });
  const eid = String(p.id || "").replace(/^e/, ""),
    isG = p.p === "G";
  let v;
  if (gxProjR100(rng)) {
    const pr = gxProj100(p, s, rng);
    v = [pr[0], "-", "-", "-", "-", "-", "-", "-", "-", "-", pr[13], pr[14]];
  } else {
    const D = GX100.data[rng];
    v = D ? gxAgg104(D[eid], isG, s.sc || {}) : GX_SK104.map(() => "...");
  }
  if (isG) v = [...v.slice(0, 11), p.prob != null ? Math.round(p.prob * 100) + "%" : "-"];
  return v.map((c, i) => /*#__PURE__*/React.createElement("div", {
    key: "c104" + i,
    className: "n " + (i >= 10 ? "font-semibold" : "text-slate-500")
  }, c));
}
function GxSH104({
  g
}) {
  const rng = gxUse100();
  return (g ? GX_GO104 : GX_SK104).map((h, i) => /*#__PURE__*/React.createElement("span", {
    key: h + i,
    className: "n"
  }, gxProjR100(rng) && i === 0 ? "Gms" : h));
}
// heading row for the goalie group (11 blank cells under the roster columns, then the goalie stats)
function GxGH104() {
  return /*#__PURE__*/React.createElement("div", {
    className: "gx-ro gx-roh gx-gh104"
  }, Array.from({
    length: 11
  }, (_, i) => /*#__PURE__*/React.createElement("span", {
    key: i
  })), /*#__PURE__*/React.createElement(GxSH106, {
    mode: "go"
  }));
}
// ---------- change 104: tidy Buy low row ----------
function GxBL104({
  s,
  p,
  r,
  onPick
}) {
  return /*#__PURE__*/React.createElement("div", {
    className: "gx-bl104"
  }, /*#__PURE__*/React.createElement(GxFace, {
    p: p,
    size: 26
  }), /*#__PURE__*/React.createElement("div", {
    className: "min-w-0"
  }, /*#__PURE__*/React.createElement("div", {
    className: "truncate"
  }, /*#__PURE__*/React.createElement(PN, {
    p: p,
    className: "font-medium"
  }), " ", /*#__PURE__*/React.createElement("span", {
    className: "text-xs text-slate-500"
  }, p.p)), /*#__PURE__*/React.createElement("div", {
    className: "why"
  }, /*#__PURE__*/React.createElement(TL, {
    s: s,
    id: p.ft
  }), " · " + r.join(", "))), /*#__PURE__*/React.createElement("div", {
    className: "pg"
  }, f1(effAvg(p, s.blend)), /*#__PURE__*/React.createElement("span", null, "pts/g")), /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: "tr",
    onClick: () => onPick(p)
  }, "+ Trade"));
}
// ---------- change 105: slide on swipe, all players, chart games (install.py) ----------
// returns "r" or "l" when the key moves forward or back, so the new content slides in from that side
function useSlide105(k) {
  const r = React.useRef({
    k,
    c: ""
  });
  if (r.current.k !== k) r.current = {
    k,
    c: k > r.current.k ? "r" : "l"
  };
  return r.current.c;
}
// lineup games in the week chart: "text" (under each day) or "bars" (behind each day)
const gxGopt105 = () => {
  const v = uiGet().gxGopt105;
  return v === "bars" ? "bars" : "text";
};
const GX_DNP105 = {
  dec: "-",
  sv: "-",
  ga: "-",
  svp: null,
  toi: "-",
  g: "-",
  a: "-",
  pm: "-",
  pim: "-",
  sog: "-"
};
function GxFaToggle105({
  cur,
  go
}) {
  return /*#__PURE__*/React.createElement("div", {
    className: "gx-seg gx-fa105"
  }, /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: cur !== "allp" ? "on" : "",
    onClick: () => go("moves", "adddrop")
  }, "Free agents"), /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: cur === "allp" ? "on" : "",
    onClick: () => go("moves", "allp")
  }, "All players"));
}
// ---------- change 105: goalie days slide ----------
function GxGoSl105({
  day,
  children
}) {
  const c = useSlide105(day);
  return /*#__PURE__*/React.createElement("div", {
    key: "g105-" + day,
    className: "gx-sl105 " + c
  }, children);
}
// ---------- change 106: drag to swipe, stats everywhere, goalie start share (install.py) ----------
// follow the finger; past about a quarter of the width it moves on, otherwise it springs back
function useDrag106(prev, next) {
  const ref = React.useRef(null),
    st = React.useRef(null);
  const set = (el, tr, x, op) => {
    el.style.transition = tr;
    el.style.transform = x;
    el.style.opacity = op;
  };
  const h = {
    onTouchStart: e => {
      const t = e.touches[0];
      st.current = {
        x: t.clientX,
        y: t.clientY,
        dx: 0,
        lock: null
      };
    },
    onTouchMove: e => {
      const s = st.current,
        el = ref.current;
      if (!s || !el) return;
      const t = e.touches[0],
        dx = t.clientX - s.x,
        dy = t.clientY - s.y;
      if (s.lock == null) {
        if (Math.abs(dx) < 8 && Math.abs(dy) < 8) return;
        s.lock = Math.abs(dx) > Math.abs(dy) ? "x" : "y";
      }
      if (s.lock !== "x") return;
      const can = dx < 0 ? !!next : !!prev;
      s.dx = can ? dx : dx / 4;
      set(el, "none", "translateX(" + s.dx + "px)", String(1 - Math.min(0.5, Math.abs(s.dx) / 700)));
    },
    onTouchEnd: () => {
      const s = st.current,
        el = ref.current;
      st.current = null;
      if (!s || !el || s.lock !== "x") return;
      const w = el.offsetWidth || 320,
        fn = Math.abs(s.dx) > w * 0.22 ? s.dx < 0 ? next : prev : null;
      if (fn) {
        set(el, "transform .15s ease-in, opacity .15s", "translateX(" + (s.dx < 0 ? -w : w) * 0.6 + "px)", "0");
        setTimeout(() => {
          set(el, "none", "", "");
          fn();
        }, 140);
      } else set(el, "transform .22s cubic-bezier(.2,.8,.2,1), opacity .22s", "", "");
    }
  };
  h.onTouchCancel = h.onTouchEnd;
  return [ref, h];
}
// how often a goalie has started: games played out of his team's games so far
function gxGS106(p) {
  const S = SCHED[p.t],
    td = todayISO();
  if (!S || p.p !== "G") return null;
  let tg = 0;
  S.forEach(d => {
    if (d < td || d === td && gState(p.t, d).s === "F") tg += 1;
  });
  if (!tg) return null;
  const n = Math.min(p.gp || 0, tg);
  return {
    n,
    tg,
    pct: Math.round(n / tg * 100) + "%"
  };
}
const gxGsTxt106 = p => {
  const g = gxGS106(p);
  return g ? "started " + g.n + " of " + g.tg : "";
};
// stat values in display order: FPTS first, no average at the end
const GX_SK106 = ["FPTS", "GP", "G", "A", "PTS", "+/-", "PIM", "SOG", "HIT", "BLK", "TOI"];
const GX_GO106 = ["FPTS", "GP", "W", "L", "OTL", "GA", "SV", "SV%", "GAA", "SO", "TOI"];
const GX_CM106 = ["FPTS"];
function gxVals106(p, s, rng) {
  const eid = String(p.id || "").replace(/^e/, ""),
    isG = p.p === "G";
  let v;
  if (gxProjR100(rng)) {
    const pr = gxProj100(p, s, rng);
    v = [pr[0], "-", "-", "-", "-", "-", "-", "-", "-", "-", pr[13], pr[14]];
  } else {
    const D = GX100.data[rng];
    v = D ? gxAgg104(D[eid], isG, s.sc || {}) : GX_SK104.map(() => "...");
  }
  return [v[10], ...v.slice(0, 10)];
}
function GxSC106({
  p,
  s,
  mode
}) {
  const rng = gxUse100();
  useEffect(() => {
    gxLoad100(rng);
  });
  const v0 = gxVals106(p, s, rng),
    v = mode === "mx" && p.p === "G" ? [v0[0], v0[1], "-", "-", "-", "-", "-", "-", "-", "-", v0[10]] : v0,
    out = mode === "cm" ? v.slice(0, 1) : v;
  return out.map((c, i) => /*#__PURE__*/React.createElement("div", {
    key: "c106" + i,
    className: "n " + (i === 0 ? "font-semibold" : "text-slate-500")
  }, c));
}
function GxSH106({
  mode
}) {
  const rng = gxUse100();
  const H = mode === "go" ? GX_GO106 : mode === "cm" ? GX_CM106 : GX_SK106;
  const S = gxUseSort108();
  return H.map((h, i) => /*#__PURE__*/React.createElement("button", {
    type: "button",
    key: h + i,
    className: "n gx-sh108" + (S.k === h ? " on" : ""),
    onClick: () => gxSet108(h)
  }, gxProjR100(rng) && h === "GP" ? "Gms" : h, S.k === h ? /*#__PURE__*/React.createElement("i", null, S.dir > 0 ? "\u25bc" : "\u25b2") : null));
}
const gxPkMode106 = pos => pos === "G" ? "full go" : "full sk";
// ---------- change 107: Simulate a pickup, cleaned up (install.py) ----------
function GxSim107({
  s,
  setS,
  wk,
  M,
  H,
  hLabel,
  init,
  wBase,
  onClose
}) {
  const ea = gxPgAvg,
    K = M.K,
    myR = M.myR,
    today = todayISO();
  const byId = id => id ? s.players.find(p => p.id === id) || null : null;
  const [addId, setAddId] = useState(init.add || "");
  const [chg, setChg] = useState(!init.add);
  const [q, setQ] = useState("");
  const [dropId, setDropId] = useState(init.drop || "");
  const [day, setDay] = useState(null);
  const [allD, setAllD] = useState(false);
  const [det, setDet] = useState(false);
  const [out, setOut] = useState(false);
  const close = () => {
    if (out) return;
    setOut(true);
    setTimeout(onClose, 170);
  };
  useEffect(() => {
    const k = e => {
      if (e.key === "Escape") close();
    };
    window.addEventListener("keydown", k);
    document.body.style.overflow = "hidden";
    return () => {
      window.removeEventListener("keydown", k);
      document.body.style.overflow = "";
    };
  }, []);
  const a = byId(addId),
    d = byId(dropId);
  const left = movesLeft(s, s.me, wk);
  const dates = wk.dates || [],
    from = wk.done || 0;
  const a0 = a ? pickStart(a) : today;
  const cands = useMemo(() => myR.filter(p => !p.ir).sort((x, y) => ea(x, K) - ea(y, K)), [myR, K]);
  const weak = cands.filter(p => !M.protectedIds.has(p.id)).slice(0, 6);
  const sug = useMemo(() => {
    if (!a) return "";
    const c = cntOf(myR),
      ok = x => x.p === a.p || c[x.p] - 1 >= M.mins[x.p],
      b = M.total(myR);
    let best = null;
    (weak.length ? weak : cands).filter(ok).forEach(x => {
      const g = M.total(timedMove(myR, s.me, [{
        add: a,
        drop: x
      }])) - b;
      if (!best || g > best.g) best = {
        x,
        g
      };
    });
    return best ? best.x.id : "";
  }, [addId]);
  useEffect(() => {
    if (sug && (!dropId || !init.drop)) setDropId(sug);
  }, [sug]);
  const rosterOn = dt => myR.map(p => d && p.id === d.id ? {
    ...p,
    untilD: dt
  } : p).concat(a ? [{
    ...a,
    ft: s.me,
    fromD: dt
  }] : []);
  const dayG = useMemo(() => {
    if (!a || !d) return [];
    const b = weekProj(myR, wk, K, from).total;
    return dates.map((dt, i) => ({
      dt,
      i
    })).filter(x => x.i >= from && x.dt >= a0).map(x => ({
      ...x,
      g: weekProj(rosterOn(x.dt), wk, K, from).total - b
    }));
  }, [addId, dropId, wk]);
  const best = dayG.reduce((b, x) => !b || x.g > b.g + 0.05 ? x : b, null);
  const pick = day != null && dayG.some(x => x.dt === day) ? day : best ? best.dt : null;
  const R = useMemo(() => {
    if (!a || !d || !pick) return null;
    const r = rosterOn(pick);
    const dg = dayG.find(x => x.dt === pick);
    return {
      gain: H === 1 && dg ? dg.g : M.total(r) - M.total(myR),
      win: winChance(s, r)
    };
  }, [addId, dropId, pick]);
  const qq = nrm(q);
  const opts = !chg ? [] : qq ? M.fas.filter(p => p.prob > 0 && nrm(p.n).includes(qq)).sort((x, y) => ea(y, K) - ea(x, K)).slice(0, 8) : M.res.slice(0, 8).map(r => r.f);
  const apply = () => {
    if (!a || !d) return;
    setS(st => ({
      ...st,
      players: st.players.map(p => p.id === d.id ? {
        ...p,
        ft: "fa",
        ir: false
      } : p.id === a.id ? {
        ...p,
        ft: st.me
      } : p)
    }));
    close();
  };
  const DN = dt => dt === today ? "Today" : dayLabel(dt).split(",")[0];
  const sg = v => (v >= 0 ? "+" : "") + f1(v);
  return /*#__PURE__*/React.createElement("div", {
    className: "gx-so107" + (out ? " out" : ""),
    onClick: close
  }, /*#__PURE__*/React.createElement("div", {
    className: "gx-sim107",
    onClick: e => e.stopPropagation()
  }, /*#__PURE__*/React.createElement("div", {
    className: "hd"
  }, /*#__PURE__*/React.createElement("span", {
    className: "t"
  }, "Simulate a pickup"), left != null ? /*#__PURE__*/React.createElement("span", {
    className: "m"
  }, left + " move" + (left === 1 ? "" : "s") + " left") : null, /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: "x",
    "aria-label": "Close",
    onClick: close
  }, "×")), a && !chg ? /*#__PURE__*/React.createElement("div", {
    className: "pl"
  }, /*#__PURE__*/React.createElement(GxFace, {
    p: a,
    size: 44
  }), /*#__PURE__*/React.createElement("div", {
    className: "min-w-0",
    style: {
      flex: 1
    }
  }, /*#__PURE__*/React.createElement("div", {
    className: "nm truncate"
  }, a.n), /*#__PURE__*/React.createElement("div", {
    className: "sb"
  }, a.p + " · " + a.t + " · " + f1(ea(a, K)) + "/g · " + M.gamesIn(a) + " games")), /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: "lk",
    onClick: () => {
      setChg(true);
      setQ("");
    }
  }, "Change")) : /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("input", {
    className: inp + " sr",
    autoFocus: true,
    placeholder: "Search a free agent",
    value: q,
    onChange: e => setQ(e.target.value)
  }), opts.map(p => /*#__PURE__*/React.createElement("button", {
    key: p.id,
    type: "button",
    className: "opt",
    onClick: () => {
      setAddId(p.id);
      setDropId("");
      setDay(null);
      setChg(false);
    }
  }, /*#__PURE__*/React.createElement(GxFace, {
    p: p,
    size: 26
  }), /*#__PURE__*/React.createElement("span", {
    className: "truncate"
  }, p.n, " ", /*#__PURE__*/React.createElement("span", {
    className: "text-xs text-slate-500"
  }, p.p)), /*#__PURE__*/React.createElement("span", {
    className: "v"
  }, f1(ea(p, K)))))), a && !chg ? /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("div", {
    className: "sec"
  }, "Drop"), /*#__PURE__*/React.createElement("div", {
    className: "chips"
  }, (allD ? cands : weak).map(p => /*#__PURE__*/React.createElement("button", {
    key: p.id,
    type: "button",
    className: "dc" + (p.id === dropId ? " on" : ""),
    onClick: () => {
      setDropId(p.id);
      setDay(null);
    }
  }, /*#__PURE__*/React.createElement(GxFace, {
    p: p,
    size: 28
  }), /*#__PURE__*/React.createElement("span", {
    className: "min-w-0"
  }, /*#__PURE__*/React.createElement("span", {
    className: "n"
  }, shortN(p.n)), /*#__PURE__*/React.createElement("span", {
    className: "v"
  }, p.p + " · " + f1(ea(p, K)))), p.id === sug ? /*#__PURE__*/React.createElement("i", null, "BEST") : null))), /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: "lk",
    style: {
      marginTop: 8
    },
    onClick: () => setAllD(!allD)
  }, allD ? "Weakest only" : "Whole roster"), dayG.length ? /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("div", {
    className: "sec"
  }, "Best day to add"), /*#__PURE__*/React.createElement("div", {
    className: "days"
  }, dayG.map(x => /*#__PURE__*/React.createElement("button", {
    key: x.dt,
    type: "button",
    className: "dy" + (x.dt === pick ? " on" : "") + (best && x.dt === best.dt && dayG.length > 1 ? " best" : ""),
    onClick: () => setDay(x.dt)
  }, /*#__PURE__*/React.createElement("span", null, DN(x.dt)), /*#__PURE__*/React.createElement("b", {
    style: {
      color: x.g >= 0 ? "var(--good)" : "var(--bad)"
    }
  }, sg(x.g)))))) : null, R ? /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("div", {
    className: "res"
  }, /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("small", null, "Points, " + hLabel), /*#__PURE__*/React.createElement("b", {
    style: {
      color: R.gain >= 0 ? "var(--good)" : "var(--bad)"
    }
  }, sg(R.gain))), /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("small", null, "Win " + (String(hLabel).indexOf("next week") === 0 ? "next week" : "this week")), /*#__PURE__*/React.createElement("b", null, (wBase != null ? wpTxt(wBase) + " → " : "") + (R.win == null ? "-" : wpTxt(R.win))))), /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: "lk",
    style: {
      marginTop: 10
    },
    onClick: () => setDet(!det)
  }, det ? "Hide details" : "More details"), det ? /*#__PURE__*/React.createElement(GxPickRes92, {
    s: s,
    myR: myR,
    ok: [{
      a,
      d
    }]
  }) : null, /*#__PURE__*/React.createElement("div", {
    className: "act"
  }, /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: "pr",
    onClick: () => {
      if (window.__QA) window.__QA.espn(a);
    }
  }, "Add on ESPN"), /*#__PURE__*/React.createElement("button", {
    type: "button",
    onClick: apply
  }, "Try it here"))) : null) : null));
}
// ---------- change 108: tap a stat heading to sort, pickup filters (install.py) ----------
// one sort for every stat table: key = heading, dir 1 = best first, -1 = worst first
const GX108 = window.__GX108 = window.__GX108 || {
  k: null,
  dir: 1
};
const GX_LOW108 = {
  GA: 1,
  GAA: 1,
  L: 1,
  OTL: 1
};
function gxSet108(k) {
  if (GX108.k === k) GX108.dir = -GX108.dir;else {
    GX108.k = k;
    GX108.dir = 1;
  }
  window.dispatchEvent(new Event("gx-sort108"));
}
const gxUseSort108 = () => {
  const [, t] = useState(0);
  useEffect(() => {
    const f = () => t(x => x + 1);
    window.addEventListener("gx-sort108", f);
    return () => window.removeEventListener("gx-sort108", f);
  }, []);
  return GX108;
};
const gxNum108 = v => {
  if (v == null) return -Infinity;
  const x = String(v);
  if (/^\d+:\d\d$/.test(x)) return gxPdSec(x);
  const n = parseFloat(x.replace("%", "").replace("+", ""));
  return isNaN(n) ? -Infinity : x.indexOf("%") > 0 && n > 1 ? n / 100 : n;
};
function gxSort108(list, s, get) {
  const k = GX108.k;
  if (!k) return list;
  const rng = gxRng100(),
    g = get || (x => x),
    K = s.blend;
  const val = p => {
    if (k === "Avg") return p.gp ? p.tot / p.gp : -Infinity;
    if (k === "Exp" || k === "Rank") return gxPgAvg(p, K);
    const H = p.p === "G" ? GX_GO106 : GX_SK106,
      i = H.indexOf(k);
    if (i < 0) return -Infinity;
    const v = gxNum108(gxVals106(p, s, rng)[i]);
    return GX_LOW108[k] && v !== -Infinity ? -v : v;
  };
  return [...list].map(x => [x, val(g(x))]).sort((a, b) => (b[1] - a[1]) * GX108.dir).map(x => x[0]);
}
function GxHB108({
  k,
  l
}) {
  const S = gxUseSort108();
  return /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: "n gx-sh108" + (S.k === k ? " on" : ""),
    onClick: () => gxSet108(k)
  }, l || k, S.k === k ? /*#__PURE__*/React.createElement("i", null, S.dir > 0 ? "\u25bc" : "\u25b2") : null);
}
function GxFlt108({
  label,
  children
}) {
  const [open, setOpen] = useState(false);
  return /*#__PURE__*/React.createElement("div", {
    className: "gx-ft108" + (open ? " open" : "")
  }, /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: "tg",
    onClick: () => setOpen(!open)
  }, "Filters ", /*#__PURE__*/React.createElement("span", null, label), /*#__PURE__*/React.createElement("b", null, "\u25be")), open ? /*#__PURE__*/React.createElement("div", {
    className: "pnl"
  }, children) : null);
}
const gxRngLbl108 = () => (GX_RNG100.find(r => r[0] === gxRng100()) || [0, "Season"])[1].replace(" (projected)", " proj.");
// ---------- change 109: clean Injuries page (install.py) ----------
function GxInj109({
  s
}) {
  const ea = gxPgAvg,
    K = s.blend;
  const [who, setWho] = useState(() => uiGet()["ij85:who"] || "fa");
  const [pos, setPos] = useState("all");
  const [by, setBy] = useState(() => uiGet().ij109by || "best");
  const [nU, setNU] = useState(5);
  const [nL, setNL] = useState(15);
  const D = useMemo(() => {
    const EV = (window.__SIG || {}).injmoves || {},
      list = [],
      ups = [];
    s.players.forEach(p => {
      const id = typeof p.id === "string" && p.id[0] === "e" ? p.id.slice(1) : null;
      const inj = autoInj(p),
        e = id ? EV[id] : null;
      if (!inj && !(e && e.k === "back")) return;
      const r = {
        p,
        v: ea(p, K),
        inj,
        e,
        back: inj ? effBack(p).d : ""
      };
      if (inj) list.push(r);
      if (e) ups.push(r);
    });
    return {
      list,
      ups
    };
  }, [s]);
  const keep = r => (who === "fa" ? r.p.ft === "fa" : who === "mine" ? r.p.ft === s.me : true) && (pos === "all" || r.p.p === pos);
  const best = (a, b) => b.v - a.v;
  const ups = D.ups.filter(keep).sort(by === "best" ? best : (a, b) => gxIjLast(b.e).localeCompare(gxIjLast(a.e)) || best(a, b));
  const list = D.list.filter(keep).sort(by === "best" ? best : (a, b) => (a.back || "9").localeCompare(b.back || "9") || best(a, b));
  const ev = e => e.k === "back" ? ["up", "Off the injury list"] : e.k === "sooner" ? ["up", "Back sooner, now " + mdL(e.now)] : e.k === "dtd" ? ["up", "Now day-to-day"] : e.k === "later" ? ["wn", "Pushed back to " + mdL(e.now)] : e.k === "new" ? ["dn", "New injury" + (e.now ? ", back " + mdL(e.now) : "")] : ["", "New news"];
  const own = p => p.ft === "fa" ? "" : p.ft === s.me ? "Yours · " : teamName(s, p.ft) + " · ";
  const row = (r, upd) => {
    const st = r.inj ? (r.inj.status || "Out").replace("Injured Reserve", "IR") + (r.back ? " · back " + mdL(r.back) : "") : "Healthy";
    const x = upd && r.e ? ev(r.e) : null;
    return /*#__PURE__*/React.createElement("div", {
      key: (upd ? "u" : "l") + r.p.id,
      className: "gx-ij109"
    }, /*#__PURE__*/React.createElement(GxFace, {
      p: r.p,
      size: 28
    }), /*#__PURE__*/React.createElement("div", {
      className: "min-w-0"
    }, /*#__PURE__*/React.createElement("div", {
      className: "truncate"
    }, /*#__PURE__*/React.createElement(PN, {
      p: r.p,
      className: ""
    }), " ", /*#__PURE__*/React.createElement("span", {
      className: "text-xs text-slate-500"
    }, r.p.p)), /*#__PURE__*/React.createElement("div", {
      className: "l2"
    }, (who === "fa" ? "" : own(r.p)) + st), x ? /*#__PURE__*/React.createElement("div", {
      className: "ev " + x[0]
    }, x[1]) : null), /*#__PURE__*/React.createElement("div", {
      className: "v"
    }, f1(r.v), /*#__PURE__*/React.createElement("small", null, "pts/g")));
  };
  const lbl = {
    fa: "Free agents",
    mine: "My team",
    all: "All teams"
  }[who] + " · " + {
    all: "All",
    F: "Forwards",
    D: "Defence",
    G: "Goalies"
  }[pos] + " · " + (by === "best" ? "Best first" : "By date");
  return /*#__PURE__*/React.createElement("div", {
    className: "space-y-3"
  }, /*#__PURE__*/React.createElement(GxFlt108, {
    label: lbl
  }, /*#__PURE__*/React.createElement(Pills, {
    items: [["fa", "Free agents"], ["mine", "My team"], ["all", "All teams"]],
    value: who,
    onChange: v => {
      setWho(v);
      uiSet("ij85:who", v);
    }
  }), /*#__PURE__*/React.createElement(Pills, {
    items: [["all", "All"], ["F", "Forwards"], ["D", "Defence"], ["G", "Goalies"]],
    value: pos,
    onChange: setPos
  }), /*#__PURE__*/React.createElement(Pills, {
    items: [["best", "Best first"], ["date", "By date"]],
    value: by,
    onChange: v => {
      setBy(v);
      uiSet("ij109by", v);
    }
  })), ups.length ? /*#__PURE__*/React.createElement(GxPanel, {
    title: "Updates",
    right: "last 7 days"
  }, ups.slice(0, nU).map(r => row(r, true)), ups.length > nU ? /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: "text-sm text-blue-600",
    style: {
      marginTop: 8
    },
    onClick: () => setNU(nU + 10)
  }, "Show more") : null) : null, /*#__PURE__*/React.createElement(GxPanel, {
    title: "Injured",
    right: list.length + ""
  }, list.length ? list.slice(0, nL).map(r => row(r, false)) : /*#__PURE__*/React.createElement("div", {
    className: "text-sm text-slate-500"
  }, "None"), list.length > nL ? /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: "text-sm text-blue-600",
    style: {
      marginTop: 8
    },
    onClick: () => setNL(nL + 20)
  }, "Show more") : null));
}
// ---------- change 111: Lines on an ice rink (install.py) ----------
const GX_ORD111 = {
  lw: 0,
  l: 0,
  c: 1,
  rw: 2,
  r: 2,
  ld: 3,
  rd: 4,
  d: 3,
  g: 5
};
function GxRinkLines111({
  teamCode
}) {
  const t = teamCode;
  return /*#__PURE__*/React.createElement("svg", {
    className: "ice",
    viewBox: "0 0 100 200",
    preserveAspectRatio: "none",
    "aria-hidden": "true"
  }, /*#__PURE__*/React.createElement("line", {
    x1: "0",
    y1: "12",
    x2: "100",
    y2: "12",
    style: {
      stroke: "rgba(220,38,38,.35)",
      strokeWidth: 0.6
    },
    vectorEffect: "non-scaling-stroke"
  }), /*#__PURE__*/React.createElement("line", {
    x1: "0",
    y1: "66",
    x2: "100",
    y2: "66",
    style: {
      stroke: "rgba(37,99,235,.45)",
      strokeWidth: 1.6
    },
    vectorEffect: "non-scaling-stroke"
  }), /*#__PURE__*/React.createElement("line", {
    x1: "0",
    y1: "100",
    x2: "100",
    y2: "100",
    style: {
      stroke: "rgba(220,38,38,.45)",
      strokeWidth: 1.6
    },
    vectorEffect: "non-scaling-stroke"
  }), /*#__PURE__*/React.createElement("line", {
    x1: "0",
    y1: "134",
    x2: "100",
    y2: "134",
    style: {
      stroke: "rgba(37,99,235,.45)",
      strokeWidth: 1.6
    },
    vectorEffect: "non-scaling-stroke"
  }), /*#__PURE__*/React.createElement("line", {
    x1: "0",
    y1: "188",
    x2: "100",
    y2: "188",
    style: {
      stroke: "rgba(220,38,38,.35)",
      strokeWidth: 0.6
    },
    vectorEffect: "non-scaling-stroke"
  }), /*#__PURE__*/React.createElement("ellipse", {
    cx: "50",
    cy: "100",
    rx: "16",
    ry: "8",
    style: {
      fill: "none",
      stroke: "rgba(37,99,235,.3)",
      strokeWidth: 0.8
    },
    vectorEffect: "non-scaling-stroke"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M42 188 A8 4 0 0 1 58 188",
    style: {
      fill: "rgba(37,99,235,.10)",
      stroke: "rgba(220,38,38,.35)",
      strokeWidth: 0.6
    },
    vectorEffect: "non-scaling-stroke"
  }));
}
function GxLines111({
  s
}) {
  const L = window.LINES_DATA || {
    teams: {},
    changes: []
  };
  const teams = Object.keys(L.teams || {}).filter(t => ((L.teams[t] || {}).lines || {}).F1).sort();
  const [t, setT] = useState(() => window.__LINES_TEAM || uiGet().ln111fav || uiGet().ln111 || "");
  const [fav112, setFav112] = useState(() => uiGet().ln111fav || "");
  const [q, setQ] = useState("");
  const [open, setOpen] = useState(false);
  const [mode, setMode] = useState("es");
  const [recent, setRecent] = useState(() => uiGet().ln111r || []);
  useEffect(() => {
    const h = e => {
      if (e && e.detail) pick(e.detail);
    };
    window.addEventListener("gm-lines-team", h);
    return () => window.removeEventListener("gm-lines-team", h);
  }, []);
  const pick = code => {
    setT(code);
    setQ("");
    setOpen(false);
    uiSet("ln111", code);
    window.__LINES_TEAM = "";
    setRecent(r => {
      const n = [code, ...r.filter(x => x !== code)].slice(0, 6);
      uiSet("ln111r", n);
      return n;
    });
  };
  const nameOf = c => ((L.teams[c] || {}).st || {}).name || c;
  const qq = nrm(q);
  const hits = qq.length < 1 ? [] : teams.filter(c => nrm(c).startsWith(qq) || nrm(nameOf(c)).split(" ").some(w => w.startsWith(qq)) || nrm(nameOf(c)).includes(qq)).slice(0, 6);
  const T = L.teams[t] || null,
    ln = T && T.lines || {},
    df = (T && T.pos || {}).df || {};
  const byName = useMemo(() => {
    const o = {};
    s.players.forEach(p => {
      const k = nrm(p.n);
      if (!o[k] || p.t === t) o[k] = p;
    });
    return o;
  }, [s.players, t]);
  const ord = arr => [...(arr || [])].sort((a, b) => (GX_ORD111[df[a]] ?? 9) - (GX_ORD111[df[b]] ?? 9));
  const chip = (n, i) => {
    if (!n) return /*#__PURE__*/React.createElement("div", {
      key: "e" + i,
      className: "gx-pc111 empty"
    }, /*#__PURE__*/React.createElement("span", {
      className: "n"
    }, "-"));
    const p = byName[nrm(n)],
      mine = p && p.ft === s.me,
      fa = p && p.ft === "fa";
    const last = n.split(" ").slice(1).join(" ") || n;
    const tn = (teamName(s, p ? p.ft : "") || "").replace(/[^A-Za-z0-9' ]/g, " ").trim().split(/\s+/)[0] || "";
    const own = !p ? "" : mine ? "YOURS" : fa ? p.wv ? "WAIVERS" : "FA" : tn;
    return /*#__PURE__*/React.createElement("button", {
      key: n + i,
      type: "button",
      className: "gx-pc111" + (mine ? " me" : fa ? " fa" : ""),
      onClick: () => {
        if (p && window.__NAV) window.__NAV.player(p);
      }
    }, p ? /*#__PURE__*/React.createElement(GxFace, {
      p: p,
      size: 22
    }) : /*#__PURE__*/React.createElement("span", {
      style: {
        height: 29
      }
    }), /*#__PURE__*/React.createElement("span", {
      className: "n"
    }, last), /*#__PURE__*/React.createElement("span", {
      className: "o"
    }, own), p ? /*#__PURE__*/React.createElement("span", {
      className: "v"
    }, f1(gxPgAvg(p, s.blend))) : null);
  };
  const row = (lb, arr, n) => {
    const a = ord(arr);
    while (a.length < n) a.push("");
    return /*#__PURE__*/React.createElement("div", {
      key: lb,
      className: "row",
      style: {
        "--n": n
      }
    }, /*#__PURE__*/React.createElement("span", {
      className: "lb"
    }, lb), a.slice(0, n).map(chip));
  };
  const unit112 = (lb, arr, a, b) => {
    const o = ord(arr),
      r = (k, l, xs, n, c) => {
        const z = [...xs];
        while (z.length < n) z.push("");
        return /*#__PURE__*/React.createElement("div", {
          key: k,
          className: "row" + (c ? " c112" : ""),
          style: {
            "--n": n
          }
        }, /*#__PURE__*/React.createElement("span", {
          className: "lb"
        }, l), z.slice(0, n).map(chip));
      };
    return [r(lb + "a", lb, o.slice(0, a), a, a < 3), r(lb + "b", "", o.slice(a), b, true)];
  };
  const pair112 = (lb, arr) => {
    const o = ord(arr);
    while (o.length < 2) o.push("");
    return /*#__PURE__*/React.createElement("div", {
      key: lb,
      className: "row c112",
      style: {
        "--n": 2
      }
    }, /*#__PURE__*/React.createElement("span", {
      className: "lb"
    }, lb), o.slice(0, 2).map(chip));
  };
  const rows = mode === "pp" ? [...unit112("PP1", ln.PP1, 3, 2), /*#__PURE__*/React.createElement("div", {
    key: "s1",
    className: "sp"
  }), ...unit112("PP2", ln.PP2, 3, 2)] : mode === "pk" ? [...unit112("PK1", ln.PK1, 2, 2), /*#__PURE__*/React.createElement("div", {
    key: "s1",
    className: "sp"
  }), ...unit112("PK2", ln.PK2, 2, 2)] : [row("L1", ln.F1, 3), row("L2", ln.F2, 3), row("L3", ln.F3, 3), row("L4", ln.F4, 3), /*#__PURE__*/React.createElement("div", {
    key: "s1",
    className: "sp"
  }), pair112("D1", ln.D1), pair112("D2", ln.D2), pair112("D3", ln.D3), /*#__PURE__*/React.createElement("div", {
    key: "s2",
    className: "sp"
  }), pair112("G", ln.G)];
  const chg = t ? (L.changes || []).filter(c => c.team === t || c.from === t || c.to === t).slice(0, 6) : [];
  const st = T && T.st || {};
  return /*#__PURE__*/React.createElement("div", {
    className: "gx-ln111"
  }, /*#__PURE__*/React.createElement("div", {
    className: "srch"
  }, /*#__PURE__*/React.createElement("input", {
    className: inp + " w-full",
    placeholder: "Search a team",
    value: q,
    onFocus: () => setOpen(true),
    onBlur: () => setTimeout(() => setOpen(false), 150),
    onChange: e => {
      setQ(e.target.value);
      setOpen(true);
    }
  }), open && hits.length ? /*#__PURE__*/React.createElement("div", {
    className: "sug"
  }, hits.map(c => /*#__PURE__*/React.createElement("button", {
    key: c,
    type: "button",
    onMouseDown: e => e.preventDefault(),
    onClick: () => pick(c)
  }, /*#__PURE__*/React.createElement(TeamLogo, {
    t: c,
    size: 24
  }), /*#__PURE__*/React.createElement("span", null, nameOf(c)), /*#__PURE__*/React.createElement("span", {
    className: "text-xs text-slate-500",
    style: {
      marginLeft: "auto"
    }
  }, c)))) : null), recent.length ? /*#__PURE__*/React.createElement("div", {
    className: "rec"
  }, recent.map(c => /*#__PURE__*/React.createElement("button", {
    key: c,
    type: "button",
    onClick: () => pick(c)
  }, /*#__PURE__*/React.createElement(TeamLogo, {
    t: c,
    size: 18
  }), c))) : null, T ? /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("div", {
    className: "hd"
  }, /*#__PURE__*/React.createElement(TeamLogo, {
    t: t,
    size: 40
  }), /*#__PURE__*/React.createElement("div", {
    className: "min-w-0"
  }, /*#__PURE__*/React.createElement("div", {
    className: "nm truncate"
  }, nameOf(t)), st.w != null ? /*#__PURE__*/React.createElement("div", {
    className: "rc"
  }, st.w + "-" + st.l + "-" + st.otl + (st.streak ? " · " + st.streak : "")) : null)), /*#__PURE__*/React.createElement("div", {
    className: "gx-seg103"
  }, [["es", "Even strength"], ["pp", "Power play"], ["pk", "Penalty kill"]].map(([k, l]) => /*#__PURE__*/React.createElement("button", {
    key: k,
    type: "button",
    className: mode === k ? "on" : "",
    onClick: () => setMode(k)
  }, l))), /*#__PURE__*/React.createElement("div", {
    key: t + mode,
    className: "gx-rk111"
  }, /*#__PURE__*/React.createElement(GxRinkLines111, {
    teamCode: t
  }), /*#__PURE__*/React.createElement("span", {
    className: "logo"
  }, /*#__PURE__*/React.createElement(TeamLogo, {
    t: t,
    size: 220
  })), rows), chg.length ? /*#__PURE__*/React.createElement("div", {
    className: "gx-pn",
    style: {
      marginTop: 12
    }
  }, /*#__PURE__*/React.createElement("div", {
    className: "gx-tag",
    style: {
      marginBottom: 4
    }
  }, "Recent changes"), chg.map(c => /*#__PURE__*/React.createElement("div", {
    key: c.id,
    className: "chg"
  }, c.text, /*#__PURE__*/React.createElement("small", null, dayLabel(String(c.at || "").slice(0, 10)))))) : null) : null, !fav112 ? /*#__PURE__*/React.createElement(GxFavPick112, {
    onPick: c => {
      uiSet("ln111fav", c);
      setFav112(c);
      pick(c);
    }
  }) : null);
}
// ---------- change 112: favourite team for Lines (install.py) ----------
function GxFavPick112({
  onPick
}) {
  const L = window.LINES_DATA || {
    teams: {}
  };
  const teams = Object.keys(L.teams || {}).filter(t => ((L.teams[t] || {}).lines || {}).F1).sort();
  return /*#__PURE__*/React.createElement("div", {
    className: "gx-pn gx-fav112"
  }, /*#__PURE__*/React.createElement("div", {
    className: "font-semibold"
  }, "Pick your favourite team"), /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500"
  }, "It opens here every time. Change it in Setup, Display."), /*#__PURE__*/React.createElement("div", {
    className: "g"
  }, teams.map(c => /*#__PURE__*/React.createElement("button", {
    key: c,
    type: "button",
    onClick: () => onPick(c)
  }, /*#__PURE__*/React.createElement(TeamLogo, {
    t: c,
    size: 30
  }), c))));
}
function GxFavSel112() {
  const L = window.LINES_DATA || {
    teams: {}
  };
  const teams = Object.keys(L.teams || {}).filter(t => ((L.teams[t] || {}).lines || {}).F1).sort();
  const [v, setV] = useState(uiGet().ln111fav || "");
  return /*#__PURE__*/React.createElement("select", {
    className: inp,
    value: v,
    onChange: e => {
      setV(e.target.value);
      uiSet("ln111fav", e.target.value);
      uiSet("ln111", e.target.value);
    }
  }, /*#__PURE__*/React.createElement("option", {
    value: ""
  }, "None"), teams.map(c => /*#__PURE__*/React.createElement("option", {
    key: c,
    value: c
  }, ((L.teams[c] || {}).st || {}).name || c)));
}
// ---------- change 113: Trades rebuilt (install.py) ----------
function GxPick113({
  title,
  list,
  sel,
  onToggle,
  onClose,
  pg
}) {
  const [q, setQ] = useState("");
  const [out, setOut] = useState(false);
  const close = () => {
    if (out) return;
    setOut(true);
    setTimeout(onClose, 160);
  };
  const qq = nrm(q),
    ord = {
      F: 0,
      D: 1,
      G: 2
    };
  const rows = list.filter(p => !qq || nrm(p.n).includes(qq)).sort((a, b) => (a.ir ? 1 : 0) - (b.ir ? 1 : 0) || ord[a.p] - ord[b.p] || pg(b) - pg(a));
  return /*#__PURE__*/React.createElement("div", {
    className: "gx-so107" + (out ? " out" : ""),
    onClick: close
  }, /*#__PURE__*/React.createElement("div", {
    className: "gx-sim107 gx-pk113",
    onClick: e => e.stopPropagation()
  }, /*#__PURE__*/React.createElement("div", {
    className: "hd"
  }, /*#__PURE__*/React.createElement("span", {
    className: "t"
  }, title), /*#__PURE__*/React.createElement("span", {
    className: "m"
  }, sel.length ? sel.length + " picked" : ""), /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: "x",
    "aria-label": "Close",
    onClick: close
  }, "×")), /*#__PURE__*/React.createElement("input", {
    className: inp + " sr",
    placeholder: "Search",
    value: q,
    onChange: e => setQ(e.target.value)
  }), /*#__PURE__*/React.createElement("div", {
    className: "lst"
  }, rows.map(p => {
    const on = sel.includes(p.id);
    return /*#__PURE__*/React.createElement("button", {
      key: p.id,
      type: "button",
      className: "it" + (on ? " on" : ""),
      onClick: () => onToggle(p.id)
    }, /*#__PURE__*/React.createElement(GxFace, {
      p: p,
      size: 26
    }), /*#__PURE__*/React.createElement("span", {
      className: "min-w-0"
    }, /*#__PURE__*/React.createElement("span", {
      className: "block truncate"
    }, p.n), /*#__PURE__*/React.createElement("span", {
      className: "text-xs text-slate-500"
    }, p.p + " · " + p.t + (p.ir ? " · IR" : ""))), /*#__PURE__*/React.createElement("span", {
      className: "v",
      style: {
        marginLeft: "auto"
      }
    }, f1(pg(p))), /*#__PURE__*/React.createElement("span", {
      className: "ck",
      style: {
        marginLeft: 10
      }
    }, on ? "✓" : ""));
  })), /*#__PURE__*/React.createElement("div", {
    className: "act"
  }, /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: "pr",
    onClick: close
  }, "Done"))));
}
// laptop only: week-by-week chart and player comparison
function GxTradeLab113({
  s,
  res,
  Gv,
  Rv,
  pg,
  gl
}) {
  const K = s.blend;
  const rng = gxUse100();
  useEffect(() => {
    gxLoad100("sea");
    gxLoad100("l15");
  }, []);
  const W = useMemo(() => {
    if (!res || !res.myL || !res.meL) return [];
    const out = [];
    for (let i = s.wk; i < s.weeks.length; i++) {
      const dw = deriveWeek(s.weeks[i], s.autoDone),
        from = i === s.wk ? dw.done || 0 : 0;
      out.push({
        i,
        b: weekProj(res.meL, dw, K, from).total,
        a: weekProj(res.myL, dw, K, from).total
      });
    }
    return out;
  }, [res]);
  const n = W.length,
    w = 640,
    h = 180,
    pad = 30;
  const mx = Math.max(1, ...W.map(x => Math.max(x.a, x.b))) * 1.08;
  const X = k => pad + (n <= 1 ? 0 : k * (w - pad - 10) / (n - 1)),
    Y = v => h - 22 - v / mx * (h - 34);
  const line = key => W.map((x, k) => X(k).toFixed(1) + "," + Y(x[key]).toFixed(1)).join(" ");
  const tot = W.reduce((t, x) => t + x.a - x.b, 0);
  const st = (p, r) => {
    const v = gxVals106(p, s, r);
    const gp = gxNum108(v[1]);
    return gp > 0 ? f1(gxNum108(v[0]) / gp) : "-";
  };
  const row = (p, side) => {
    const v = gxVals106(p, s, "sea");
    return /*#__PURE__*/React.createElement("tr", {
      key: side + p.id
    }, /*#__PURE__*/React.createElement("td", null, /*#__PURE__*/React.createElement("span", {
      className: "inline-flex items-center gap-2"
    }, /*#__PURE__*/React.createElement(GxFace, {
      p: p,
      size: 20
    }), p.n)), /*#__PURE__*/React.createElement("td", null, side === "g" ? "Give" : "Get"), /*#__PURE__*/React.createElement("td", null, p.p), /*#__PURE__*/React.createElement("td", null, p.t), /*#__PURE__*/React.createElement("td", null, v[1]), /*#__PURE__*/React.createElement("td", null, v[0]), /*#__PURE__*/React.createElement("td", null, st(p, "sea")), /*#__PURE__*/React.createElement("td", null, st(p, "l15")), /*#__PURE__*/React.createElement("td", {
      className: "b"
    }, f1(pg(p))), /*#__PURE__*/React.createElement("td", null, gl(p)));
  };
  return /*#__PURE__*/React.createElement("div", {
    className: "gx-lab113 m-hide space-y-3"
  }, /*#__PURE__*/React.createElement("div", {
    className: "gx-pn"
  }, /*#__PURE__*/React.createElement("div", {
    className: "gx-pd-h"
  }, "Week by week", /*#__PURE__*/React.createElement("span", {
    className: "r"
  }, "Your projected points, rest of season · " + (tot >= 0 ? "+" : "") + Math.round(tot))), n > 1 ? /*#__PURE__*/React.createElement("svg", {
    viewBox: "0 0 " + w + " " + h,
    width: "100%",
    style: {
      display: "block"
    }
  }, /*#__PURE__*/React.createElement("line", {
    x1: pad,
    x2: w - 10,
    y1: h - 22,
    y2: h - 22,
    style: {
      stroke: "var(--line)"
    }
  }), /*#__PURE__*/React.createElement("polyline", {
    points: line("b"),
    style: {
      fill: "none",
      stroke: "var(--mute)",
      strokeWidth: 2,
      strokeDasharray: "4 4"
    }
  }), /*#__PURE__*/React.createElement("polyline", {
    points: line("a"),
    style: {
      fill: "none",
      stroke: "var(--accent)",
      strokeWidth: 2.5
    }
  }), W.map((x, k) => k % Math.max(1, Math.ceil(n / 12)) === 0 ? /*#__PURE__*/React.createElement("text", {
    key: k,
    x: X(k),
    y: h - 6,
    textAnchor: "middle",
    style: {
      fontSize: 11,
      fill: "var(--mute)"
    }
  }, "W" + (x.i + 1)) : null)) : /*#__PURE__*/React.createElement("div", {
    className: "text-sm text-slate-500"
  }, "Not enough weeks left."), /*#__PURE__*/React.createElement("div", {
    className: "lg"
  }, /*#__PURE__*/React.createElement("span", null, /*#__PURE__*/React.createElement("i", {
    style: {
      background: "var(--accent)"
    }
  }), "After the trade"), /*#__PURE__*/React.createElement("span", null, /*#__PURE__*/React.createElement("i", {
    style: {
      background: "var(--mute)"
    }
  }), "Now"))), /*#__PURE__*/React.createElement("div", {
    className: "gx-pn"
  }, /*#__PURE__*/React.createElement("div", {
    className: "gx-pd-h"
  }, "Player comparison"), /*#__PURE__*/React.createElement("table", {
    className: "gx-pd-t"
  }, /*#__PURE__*/React.createElement("thead", null, /*#__PURE__*/React.createElement("tr", null, /*#__PURE__*/React.createElement("th", null, "Player"), /*#__PURE__*/React.createElement("th", null, "Side"), /*#__PURE__*/React.createElement("th", null, "Pos"), /*#__PURE__*/React.createElement("th", null, "Team"), /*#__PURE__*/React.createElement("th", null, "GP"), /*#__PURE__*/React.createElement("th", null, "FPTS"), /*#__PURE__*/React.createElement("th", null, "Avg"), /*#__PURE__*/React.createElement("th", null, "Last 15"), /*#__PURE__*/React.createElement("th", null, "Proj/g"), /*#__PURE__*/React.createElement("th", null, "Games left"))), /*#__PURE__*/React.createElement("tbody", null, Gv.map(p => row(p, "g")), Rv.map(p => row(p, "r"))))));
}
// ---------- change 114: fantasy team pictures from ESPN (install.py) ----------
function GxFtPic114({
  id,
  size
}) {
  const T = ((window.ESPN_DATA || {}).teams || []).find(t => String(t.id) === String(id).replace(/^t/, "")) || {};
  const [bad, setBad] = useState(0);
  const z = size || 24,
    nm = String(T.name || "?"),
    srcs = [T.pic, T.logo].filter(Boolean);
  const st = {
    width: z,
    height: z,
    borderRadius: Math.round(z * 0.28)
  };
  if (bad < srcs.length) return /*#__PURE__*/React.createElement("img", {
    key: bad,
    className: "gx-fp114",
    src: srcs[bad],
    alt: "",
    loading: "lazy",
    style: st,
    onError: () => setBad(bad + 1)
  });
  return /*#__PURE__*/React.createElement("span", {
    className: "gx-fp114 l",
    style: {
      ...st,
      fontSize: Math.round(z * 0.45)
    }
  }, (nm.replace(/[^A-Za-z0-9 ]/g, "").trim()[0] || "?").toUpperCase());
}
// ---------- change 118: one player's box score for one day, opened from Matchup (install.py) ----------
function GxBox118({
  p
}) {
  const x = typeof pStat === "function" ? pStat(p, p.dt) : null;
  const pts = p.st ? p.a == null ? 0 : p.a : p.x;
  const opp = p.st && typeof gxOpp98 === "function" ? gxOpp98(p) : mGame(p);
  const t = (k, l, v, f) => /*#__PURE__*/React.createElement("div", {
    key: k,
    className: f ? "f" : ""
  }, /*#__PURE__*/React.createElement("small", null, l), /*#__PURE__*/React.createElement("b", null, v));
  let cells = [];
  if (x && x.sv != null) {
    cells = [t("f", "FPTS", f1(pts || 0), 1), t("dec", "Result", {
      W: "Win",
      L: "Loss",
      O: "OT loss"
    }[x.dec] || "–"), t("sv", "Saves", x.sv), t("ga", "Goals against", x.ga), t("sa", "Shots", x.sa != null ? x.sa : x.sv + x.ga), t("svp", "Save %", x.sv + x.ga ? (x.sv / (x.sv + x.ga)).toFixed(3).replace(/^0/, "") : "–"), t("so", "Shutout", x.ga === 0 && x.dec === "W" ? "Yes" : "No"), t("toi", "TOI", x.toi || "–")];
  } else if (x) {
    const pm = x.pm || 0;
    cells = [t("f", "FPTS", f1(pts || 0), 1), t("g", "G", x.g || 0), t("a", "A", x.a || 0), t("pts", "PTS", (x.g || 0) + (x.a || 0)), t("pm", "+/-", (pm > 0 ? "+" : "") + pm), t("sog", "SOG", x.sog || 0), t("ppg", "PPG", x.ppg || 0), t("pim", "PIM", x.pim || 0), t("hit", "HIT", x.hit || 0), t("blk", "BLK", x.blk || 0), t("tk", "TK", x.tk || 0), t("gv", "GV", x.gv || 0), x.fo ? t("fo", "FO%", Math.round(x.fo * 100) + "%") : null, t("shf", "Shifts", x.shf || 0), t("toi", "TOI", x.toi || "–")].filter(Boolean);
  }
  return /*#__PURE__*/React.createElement("div", {
    className: "gx-bx118"
  }, /*#__PURE__*/React.createElement("div", {
    className: "hd"
  }, /*#__PURE__*/React.createElement("span", {
    className: "n"
  }, p.n), /*#__PURE__*/React.createElement("span", {
    className: "o"
  }, opp), /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: "x",
    onClick: e => {
      e.stopPropagation();
      if (window.__NAV) window.__NAV.player(p);
    }
  }, "Profile")), cells.length ? /*#__PURE__*/React.createElement("div", {
    className: "g"
  }, cells) : /*#__PURE__*/React.createElement("div", {
    className: "e"
  }, p.st ? "No stats yet for this game." : "Has not played yet. Projected " + f1(p.x || 0) + " FPTS."));
}
// ---------- change 119: box score pop-up for one player on one day (install.py) ----------
const GX_NICK119 = {
  ANA: "Ducks",
  BOS: "Bruins",
  BUF: "Sabres",
  CAR: "Hurricanes",
  CBJ: "Blue Jackets",
  CGY: "Flames",
  CHI: "Blackhawks",
  COL: "Avalanche",
  DAL: "Stars",
  DET: "Red Wings",
  EDM: "Oilers",
  FLA: "Panthers",
  LA: "Kings",
  LAK: "Kings",
  MIN: "Wild",
  MTL: "Canadiens",
  NJ: "Devils",
  NJD: "Devils",
  NSH: "Predators",
  NYI: "Islanders",
  NYR: "Rangers",
  OTT: "Senators",
  PHI: "Flyers",
  PIT: "Penguins",
  SEA: "Kraken",
  SJ: "Sharks",
  SJS: "Sharks",
  STL: "Blues",
  TB: "Lightning",
  TBL: "Lightning",
  TOR: "Maple Leafs",
  UTA: "Mammoth",
  VAN: "Canucks",
  VGK: "Golden Knights",
  WPG: "Jets",
  WSH: "Capitals"
};
function GxBox119({
  s,
  p,
  onClose
}) {
  useEffect(() => {
    const k = e => {
      if (e.key === "Escape") onClose();
    };
    window.addEventListener("keydown", k);
    return () => window.removeEventListener("keydown", k);
  }, []);
  const sc = Object.assign({}, typeof SC0 === "object" ? SC0 : {}, s && s.sc || {});
  const x = typeof pStat === "function" ? pStat(p, p.dt) : null;
  const g = gameOf(p.t, p.dt);
  const sub = dayLabel(p.dt).replace(",", "") + (g ? (g.h ? " vs. " : " @ ") + (GX_NICK119[g.o] || g.o) : "");
  const rows = [];
  const add = (l, w, n) => {
    if (n && w) rows.push([l, w, n, n * w]);
  };
  let est = 0;
  if (x && x.sv != null) {
    const w = x.dec === "W" ? 1 : 0,
      o = x.dec === "O" ? 1 : 0,
      so = w && x.ga === 0 ? 1 : 0;
    add("Wins", sc.W, w);
    add("Overtime losses", sc.OTL, o);
    add("Saves", sc.SV, x.sv || 0);
    add("Goals against", sc.GA, x.ga || 0);
    add("Shutouts", sc.SO, so);
  } else if (x) {
    add("Goals", sc.G, x.g || 0);
    add("Assists", sc.A, x.a || 0);
    add("Plus/minus", sc.PM, x.pm || 0);
    add("Shots on goal", sc.SOG, x.sog || 0);
    add("Hits", sc.HIT, x.hit || 0);
    add("Blocked shots", sc.BLK, x.blk || 0);
  }
  rows.forEach(r => {
    est += r[3];
  });
  const real = p.st && p.a != null ? p.a : null;
  if (x && x.sv == null) {
    // ESPN counts power play points; the box score only has power play goals, so the rest comes from ESPN's total
    let left = real != null ? real - est : (x.ppg || 0) * (sc.PPP || 0),
      ppp = x.ppg || 0;
    if (real != null && sc.PPP) {
      const k = Math.round(left / sc.PPP);
      if (k > 0 && Math.abs(left - k * sc.PPP) < 0.05) {
        ppp = k;
      }
    }
    if (ppp && sc.PPP) {
      add("Power Play Points", sc.PPP, ppp);
      est += ppp * sc.PPP;
      left = real != null ? real - est : 0;
    }
    if (real != null && Math.abs(real - est) >= 0.05) rows.push(["Other", null, null, real - est]);
  } else if (x && real != null && Math.abs(real - est) >= 0.05) rows.push(["Other", null, null, real - est]);
  const total = real != null ? real : x ? est : null;
  const num = v => (Math.round(v * 10) / 10).toString();
  const box = /*#__PURE__*/React.createElement("div", {
    className: "gx-bm119",
    onClick: onClose,
    role: "dialog",
    "aria-label": p.n + " box score"
  }, /*#__PURE__*/React.createElement("div", {
    className: "cd",
    onClick: e => e.stopPropagation()
  }, /*#__PURE__*/React.createElement("div", {
    className: "fc"
  }, /*#__PURE__*/React.createElement(GxFace, {
    p: p,
    size: 100
  })), /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: "xx",
    "aria-label": "Close",
    onClick: onClose
  }, "×"), /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: "nm hover:underline",
    onClick: () => {
      onClose();
      if (window.__NAV) window.__NAV.player(p);
    }
  }, p.n), /*#__PURE__*/React.createElement("div", {
    className: "sb"
  }, sub), p.st && x ? /*#__PURE__*/React.createElement("div", {
    className: "tb"
  }, /*#__PURE__*/React.createElement("div", {
    className: "h"
  }, "Scoring category"), /*#__PURE__*/React.createElement("div", {
    className: "h"
  }, "Pts per"), /*#__PURE__*/React.createElement("div", {
    className: "h"
  }, "#"), /*#__PURE__*/React.createElement("div", {
    className: "h"
  }, "Score"), rows.map((r, i) => /*#__PURE__*/React.createElement(React.Fragment, {
    key: i
  }, /*#__PURE__*/React.createElement("div", null, r[0]), /*#__PURE__*/React.createElement("div", null, r[1] == null ? "" : num(r[1])), /*#__PURE__*/React.createElement("div", null, r[2] == null ? "" : r[2]), /*#__PURE__*/React.createElement("div", null, f1(r[3])))), !rows.length ? /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("div", {
    style: {
      color: "var(--mute)"
    }
  }, "No points this game"), /*#__PURE__*/React.createElement("div", null), /*#__PURE__*/React.createElement("div", null), /*#__PURE__*/React.createElement("div", null)) : null, /*#__PURE__*/React.createElement("div", {
    className: "t"
  }, p.st === "F" ? "Total" : "Total so far"), /*#__PURE__*/React.createElement("div", {
    className: "t"
  }), /*#__PURE__*/React.createElement("div", {
    className: "t"
  }), /*#__PURE__*/React.createElement("div", {
    className: "t"
  }, f1(total || 0))) : /*#__PURE__*/React.createElement("div", {
    className: "em"
  }, p.st ? "No stats yet for this game." : "Has not played yet.", /*#__PURE__*/React.createElement("div", {
    style: {
      marginTop: 6,
      color: "var(--ink)",
      fontWeight: 600
    }
  }, "Projected " + f1(p.x || 0) + " FPTS"))));
  return ReactDOM.createPortal(box, document.body);
}
// ---------- change 120: live fantasy points from the NHL's box scores (install.py) ----------
const G120 = {
  box: {},
  pp: {},
  goals: {},
  fin: {},
  busy: false
};
const GX_AL120 = {
  LAK: "LA",
  NJD: "NJ",
  SJS: "SJ",
  TBL: "TB",
  UTAH: "UTA",
  ARI: "UTA"
};
const gxSc120 = () => Object.assign({}, typeof SC0 === "object" ? SC0 : {}, window.__SC120 || {});
function gxPP120(pb) {
  const hid = (pb.homeTeam || {}).id,
    out = {};
  (pb.plays || []).forEach(e => {
    if (e.typeDescKey !== "goal") return;
    const d = e.details || {},
      c = String(e.situationCode || "");
    if (c.length !== 4) return;
    const ag = +c[0],
      as = +c[1],
      hs = +c[2],
      hg = +c[3],
      home = d.eventOwnerTeamId === hid;
    const my = home ? hs : as,
      op = home ? as : hs,
      myG = home ? hg : ag,
      opG = home ? ag : hg;
    const pp = my > op && (myG === 1 || my - op >= 2),
      sh = my < op && (opG === 1 || op - my >= 2);
    if (!pp && !sh) return;
    [d.scoringPlayerId, d.assist1PlayerId, d.assist2PlayerId].forEach(id => {
      if (!id) return;
      const o = out[id] = out[id] || {
        ppp: 0,
        shp: 0
      };
      if (pp) o.ppp++;else o.shp++;
    });
  });
  return out;
}
function gxFp120(x) {
  const sc = gxSc120(),
    w = k => +sc[k] || 0;
  if (x.sv != null) return (x.dec === "W" ? w("W") : 0) + (x.dec === "O" ? w("OTL") : 0) + x.sv * w("SV") + x.ga * w("GA") + (x.dec === "W" && x.ga === 0 ? w("SO") : 0);
  return x.g * w("G") + x.a * w("A") + x.pm * w("PM") + x.sog * w("SOG") + x.hit * w("HIT") + x.blk * w("BLK") + x.ppp * w("PPP") + x.shp * w("SHP") + x.pim * w("PIM");
}
function gxRebuild120() {
  const out = {};
  Object.entries(G120.box).forEach(([gid, B]) => {
    const bx = B.bx || {},
      pbg = bx.playerByGameStats || {},
      pp = G120.pp[gid] || {},
      D = out[B.d] = out[B.d] || {};
    ["awayTeam", "homeTeam"].forEach(k => {
      const T = bx[k] || {},
        ab = GX_AL120[T.abbrev] || T.abbrev,
        P = pbg[k] || {};
      const put = (pl, x) => {
        x.fp = Math.round(gxFp120(x) * 100) / 100;
        x.fin = B.fin || 0;
        x.gs = B.start || "";
        if (pl.sweaterNumber != null) D[ab + "#" + pl.sweaterNumber] = x;
        const nm = String((pl.name || {}).default || ""),
          i = nm.indexOf(". "),
          ln = nrm(i > 0 ? nm.slice(i + 2) : nm.split(" ").slice(1).join(" "));
        if (ln) D[ab + ":" + nrm(nm).charAt(0) + ":" + ln] = x;
      };
      [...(P.forwards || []), ...(P.defense || [])].forEach(pl => {
        const q = pp[pl.playerId] || {};
        put(pl, {
          g: pl.goals || 0,
          a: pl.assists || 0,
          pm: pl.plusMinus || 0,
          sog: (pl.sog != null ? pl.sog : pl.shots) || 0,
          pim: pl.pim || 0,
          hit: pl.hits || 0,
          blk: (pl.blockedShots != null ? pl.blockedShots : pl.blocked) || 0,
          ppg: pl.powerPlayGoals || 0,
          ppp: q.ppp || 0,
          shp: q.shp || 0,
          toi: pl.toi || "",
          fo: pl.faceoffWinningPctg || 0,
          shf: pl.shifts || 0,
          gv: pl.giveaways || 0,
          tk: pl.takeaways || 0
        });
      });
      (P.goalies || []).forEach(pl => {
        if (!pl.toi || pl.toi === "00:00") return;
        let sv = pl.saves,
          sa = pl.shotsAgainst;
        if (sv == null && pl.saveShotsAgainst) {
          const m = String(pl.saveShotsAgainst).split("/");
          sv = +m[0];
          sa = +m[1];
        }
        put(pl, {
          sv: sv || 0,
          ga: pl.goalsAgainst || 0,
          sa: sa || 0,
          dec: pl.decision || "",
          toi: pl.toi
        });
      });
    });
  });
  const sg = JSON.stringify(out);
  if (sg === window.__LPSG120) return false;
  window.__LPSG120 = sg;
  window.__LIVEPTS = out;
  window.__LIVEV120 = (window.__LIVEV120 || 0) + 1;
  return true;
}
window.gxLive120 = (js, done) => {
  if (G120.busy || !js || !js.games) return;
  const isF = g => g.gameState === "FINAL" || g.gameState === "OFF";
  const games = js.games.filter(g => g.id && (g.gameState === "LIVE" || g.gameState === "CRIT" || isF(g) && !G120.fin[g.id]));
  if (!games.length) return;
  G120.busy = true;
  const U = "https://api-web.nhle.com/v1/gamecenter/";
  Promise.all(games.map(g => fetch(U + g.id + "/boxscore").then(r => r.ok ? r.json() : null).catch(() => null).then(bx => {
    if (!bx) return null;
    const goals = ((g.homeTeam || {}).score || 0) + ((g.awayTeam || {}).score || 0),
      needP = goals > 0 && G120.goals[g.id] !== goals;
    return (needP ? fetch(U + g.id + "/play-by-play").then(r => r.ok ? r.json() : null).catch(() => null) : Promise.resolve(null)).then(pb => {
      if (pb) {
        G120.pp[g.id] = gxPP120(pb);
        G120.goals[g.id] = goals;
      }
      const old = G120.box[g.id];
      G120.box[g.id] = {
        bx,
        d: g.gameDate,
        start: g.startTimeUTC || "",
        fin: isF(g) ? old && old.fin || (old ? Date.now() : (Date.parse(g.startTimeUTC || "") || 0) + 3 * 36e5) : 0
      };
      if (isF(g) && (!needP || pb)) G120.fin[g.id] = 1;
      return null;
    });
  }))).then(() => {
    G120.busy = false;
    if (gxRebuild120() && done) done();
  }, () => {
    G120.busy = false;
  });
};
// the live box score line for one player on one day (from the NHL), or null
function gxLiveStat120(p, dt) {
  const D = (window.__LIVEPTS || {})[dt];
  if (!D || !p) return null;
  const no = typeof gxPdNo === "function" ? gxPdNo(p) : null;
  let x = no != null ? D[p.t + "#" + no] : null;
  if (!x) {
    const ln = nrm(String(p.n || "").split(" ").slice(1).join(" "));
    x = ln ? D[p.t + ":" + nrm(p.n).charAt(0) + ":" + ln] : null;
  }
  return x || null;
}
// live numbers count while the game is on, and after it ends until an ESPN sync from after the final confirms them
function gxUseLive120(p, dt, a) {
  const L = gxLiveStat120(p, dt);
  if (!L) return null;
  const g = gState(p.t, dt);
  if (g.s === "L") return L;
  if (g.s !== "F") return null;
  if (a == null) return L;
  const gen = Date.parse(String((window.ESPN_DATA || {}).generated || "") + "Z"),
    fin = L.fin || (L.gs ? Date.parse(L.gs) + 3 * 36e5 : 0);
  return !isNaN(gen) && fin && gen > fin + 5 * 60e3 ? null : L;
}
const gxLiveA120 = (p, dt, a) => {
  const L = p && dt ? gxUseLive120(p, dt, a) : null;
  return L ? L.fp : a;
};
// team scores with today's live points in place of the last sync's
const W120 = new WeakMap();
function gxAct120(w) {
  const A = w && w.act || {},
    today = todayISO();
  if (!w || !window.__LIVEPTS || !(w.dates || []).includes(today)) return A;
  const c = W120.get(w),
    k = (window.__LIVEV120 || 0) + "|" + ((window.ESPN_DATA || {}).generated || "");
  if (c && c.k === k && c.A === A) return c.v;
  const v = {
      ...A
    },
    P = pby();
  Object.keys(A).forEach(tid => {
    const AD = actDay(tid, today);
    if (!AD) return;
    let d = 0;
    Object.entries(AD).forEach(([pid, x]) => {
      if (!x || !ESLOT[x[1]]) return;
      const p = P["e" + pid];
      if (!p) return;
      const a2 = gxLiveA120(p, today, x[0]);
      if (a2 != null) d += a2 - (x[0] || 0);
    });
    v[tid] = (+A[tid] || 0) + d;
  });
  W120.set(w, {
    k,
    A,
    v
  });
  return v;
}
ReactDOM.createRoot(document.getElementById("root")).render(/*#__PURE__*/React.createElement(App, null));