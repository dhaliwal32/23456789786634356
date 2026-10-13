/* built from fantasy-gm.html - do not edit, run Install changes instead */
"use strict";

function _typeof(o) { "@babel/helpers - typeof"; return _typeof = "function" == typeof Symbol && "symbol" == typeof Symbol.iterator ? function (o) { return typeof o; } : function (o) { return o && "function" == typeof Symbol && o.constructor === Symbol && o !== Symbol.prototype ? "symbol" : typeof o; }, _typeof(o); }
function _createForOfIteratorHelper(r, e) { var t = "undefined" != typeof Symbol && r[Symbol.iterator] || r["@@iterator"]; if (!t) { if (Array.isArray(r) || (t = _unsupportedIterableToArray(r)) || e && r && "number" == typeof r.length) { t && (r = t); var _n = 0, F = function F() {}; return { s: F, n: function n() { return _n >= r.length ? { done: !0 } : { done: !1, value: r[_n++] }; }, e: function e(r) { throw r; }, f: F }; } throw new TypeError("Invalid attempt to iterate non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); } var o, a = !0, u = !1; return { s: function s() { t = t.call(r); }, n: function n() { var r = t.next(); return a = r.done, r; }, e: function e(r) { u = !0, o = r; }, f: function f() { try { a || null == t.return || t.return(); } finally { if (u) throw o; } } }; }
function _defineProperty(e, r, t) { return (r = _toPropertyKey(r)) in e ? Object.defineProperty(e, r, { value: t, enumerable: !0, configurable: !0, writable: !0 }) : e[r] = t, e; }
function _toPropertyKey(t) { var i = _toPrimitive(t, "string"); return "symbol" == _typeof(i) ? i : i + ""; }
function _toPrimitive(t, e) { if ("object" != _typeof(t) || !t) return t; var r; if ("undefined" != typeof Symbol && void 0 !== (r = t[Symbol.toPrimitive])) { var i = r.call(t, e || "default"); if ("object" != _typeof(i)) return i; throw new TypeError("@@toPrimitive must return a primitive value."); } return ("string" === e ? String : Number)(t); }
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
function _toConsumableArray(r) { return _arrayWithoutHoles(r) || _iterableToArray(r) || _unsupportedIterableToArray(r) || _nonIterableSpread(); }
function _nonIterableSpread() { throw new TypeError("Invalid attempt to spread non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); }
function _iterableToArray(r) { if ("undefined" != typeof Symbol && null != r[Symbol.iterator] || null != r["@@iterator"]) return Array.from(r); }
function _arrayWithoutHoles(r) { if (Array.isArray(r)) return _arrayLikeToArray(r); }
function _slicedToArray(r, e) { return _arrayWithHoles(r) || _iterableToArrayLimit(r, e) || _unsupportedIterableToArray(r, e) || _nonIterableRest(); }
function _nonIterableRest() { throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); }
function _unsupportedIterableToArray(r, a) { if (r) { if ("string" == typeof r) return _arrayLikeToArray(r, a); var t = {}.toString.call(r).slice(8, -1); return "Object" === t && r.constructor && (t = r.constructor.name), "Map" === t || "Set" === t ? Array.from(r) : "Arguments" === t || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(t) ? _arrayLikeToArray(r, a) : void 0; } }
function _arrayLikeToArray(r, a) { (null == a || a > r.length) && (a = r.length); for (var e = 0, n = Array(a); e < a; e++) n[e] = r[e]; return n; }
function _iterableToArrayLimit(r, l) { var t = null == r ? null : "undefined" != typeof Symbol && r[Symbol.iterator] || r["@@iterator"]; if (null != t) { var e, n, i, u, a = [], f = !0, o = !1; try { if (i = (t = t.call(r)).next, 0 === l) { if (Object(t) !== t) return; f = !1; } else for (; !(f = (e = i.call(t)).done) && (a.push(e.value), a.length !== l); f = !0); } catch (r) { o = !0, n = r; } finally { try { if (!f && null != t.return && (u = t.return(), Object(u) !== u)) return; } finally { if (o) throw n; } } return a; } }
function _arrayWithHoles(r) { if (Array.isArray(r)) return r; }
var _React = React,
  useState = _React.useState,
  useEffect = _React.useEffect,
  useMemo = _React.useMemo;
var KEY = "fantasy-islands-gm-v1";
var NHL = ["ANA", "BOS", "BUF", "CGY", "CAR", "CHI", "COL", "CBJ", "DAL", "DET", "EDM", "FLA", "LA", "MIN", "MTL", "NSH", "NJ", "NYI", "NYR", "OTT", "PHI", "PIT", "SJ", "SEA", "STL", "TB", "TOR", "UTA", "VAN", "VGK", "WSH", "WPG"];
var TEAMS0 = [{
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
var R = {
  me: "Nathan MacKinnon|COL|F|15;Brady Tkachuk|FLA|F|10.6|.85;Mikko Rantanen|DAL|F|9.4;Sam Reinhart|FLA|F|9.1;Aleksander Barkov|FLA|F|9.2;Lucas Raymond|DET|F|7.7;Sam Bennett|FLA|F|7.3;Matthew Knies|TOR|F|6;Patrick Kane|CHI|F|8.8;Matt Duchene|DAL|F|7.2|.7;Trevor Zegras|PHI|F|6.6;Tyler Seguin|DAL|F|6.3;Jared McCann|SEA|F|7;Ryan Hartman|MIN|F|6.4;Troy Terry|ANA|F|7.4|0|i;Josh Morrissey|WPG|D|7.6;Shayne Gostisbehere|CAR|D|7.7;Jackson LaCombe|ANA|D|6.6;Victor Hedman|TB|D|8.7;Luke Hughes|NJ|D|5.4;Scott Wedgewood|COL|G|10.8|.55;Lukas Dostal|ANA|G|7.9|.6;Kevin Lankinen|VAN|G|9|.7",
  kap: "Kirill Kaprizov|MIN|F|11;William Nylander|TOR|F|9;Kyle Connor|WPG|F|9;Adrian Kempe|LA|F|8;Alex Ovechkin|WSH|F|8|.75;Mark Stone|VGK|F|7;Ivan Barbashev|VGK|F|6;Pavel Zacha|BOS|F|6;J.T. Miller|NYR|F|8;Nazem Kadri|COL|F|7;Valeri Nichushkin|CBJ|F|6.5;Rickard Rakell|PIT|F|7;Mikael Granlund|ANA|F|6.5;Evan Bouchard|EDM|D|9;Noah Dobson|MTL|D|7.5;Shea Theodore|VGK|D|7;Sean Walker|CAR|D|5.5;Darnell Nurse|SJ|D|6;Dougie Hamilton|NJ|D|7;Mackenzie Blackwood|COL|G|9|.45;Linus Ullmark|OTT|G|9|.65;Darcy Kuemper|LA|G|9|.65",
  fa: "Sergei Murashov|PIT|G|9.9|.65;Joseph Woll|PHI|G|10.3|.5;Stuart Skinner|WPG|G|7.7|.8;Viktor Arvidsson|DET|F|7.3"
};
var SC0 = {
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
var SR = {
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
var MON = {
  S: [2026, 8],
  O: [2026, 9],
  N: [2026, 10],
  D: [2026, 11],
  J: [2027, 0],
  F: [2027, 1],
  M: [2027, 2],
  A: [2027, 3]
};
var iso = function iso(d) {
  return d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0") + "-" + String(d.getDate()).padStart(2, "0");
};
var fromIso = function fromIso(x) {
  return new Date(x + "T12:00:00");
};
var addDays = function addDays(x, n) {
  var d = fromIso(x);
  d.setDate(d.getDate() + n);
  return iso(d);
};
var todayISO = function todayISO() {
  return iso(new Date());
};
var dayLabel = function dayLabel(x) {
  return fromIso(x).toLocaleDateString("en-US", {
    weekday: "short",
    month: "numeric",
    day: "numeric"
  });
};
var mdL = function mdL(x) {
  return fromIso(x).toLocaleDateString("en-US", {
    month: "short",
    day: "numeric"
  });
};
var SCHED = function () {
  var out = {};
  Object.entries(SR).forEach(function (_ref) {
    var _ref2 = _slicedToArray(_ref, 2),
      t = _ref2[0],
      str = _ref2[1];
    var set = new Set();
    str.split(";").forEach(function (part) {
      var _part$split = part.split(":"),
        _part$split2 = _slicedToArray(_part$split, 2),
        m = _part$split2[0],
        ds = _part$split2[1];
      var _MON$m = _slicedToArray(MON[m], 2),
        y = _MON$m[0],
        mo = _MON$m[1];
      ds.split(",").forEach(function (d) {
        return set.add(iso(new Date(y, mo, +d, 12)));
      });
    });
    out[t] = set;
  });
  return out;
}();
var wkGames = function wkGames(dates) {
  var g = {};
  NHL.forEach(function (t) {
    g[t] = [];
    dates.forEach(function (d, i) {
      if (SCHED[t] && SCHED[t].has(d)) g[t].push(i);
    });
  });
  return g;
};
var lab = function lab(i, dates) {
  return "Week ".concat(i + 1, " \xB7 ").concat(mdL(dates[0]), " \u2013 ").concat(mdL(dates[dates.length - 1]));
};
var mkW = function mkW(i, start, len) {
  var dates = _toConsumableArray(Array(len)).map(function (_, k) {
    return addDays(start, k);
  });
  return {
    label: lab(i, dates),
    dates: dates,
    pairs: [],
    done: 0,
    act: {}
  };
};
var defaultWeeks = function defaultWeeks() {
  var w = [mkW(0, "2026-09-29", 6)];
  var st = "2026-10-05";
  for (var i = 1; i < 28; i++) {
    w.push(mkW(i, st, 7));
    st = addDays(st, 7);
  }
  w[0].pairs = [["me", "kap"]];
  return w;
};
var effDone = function effDone(w, auto) {
  return auto && w.dates && w.dates.length ? w.dates.filter(function (d) {
    return d < todayISO();
  }).length : w.done || 0;
};
var deriveWeek = function deriveWeek(w, auto) {
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
  var out = [];
  var i = 0;
  Object.entries(R).forEach(function (_ref3) {
    var _ref4 = _slicedToArray(_ref3, 2),
      ft = _ref4[0],
      str = _ref4[1];
    str.split(";").forEach(function (s) {
      var _s$trim$split = s.trim().split("|"),
        _s$trim$split2 = _slicedToArray(_s$trim$split, 6),
        n = _s$trim$split2[0],
        t = _s$trim$split2[1],
        p = _s$trim$split2[2],
        a = _s$trim$split2[3],
        pr = _s$trim$split2[4],
        f = _s$trim$split2[5];
      out.push({
        id: "p" + i++,
        n: n,
        t: t,
        p: p,
        avg: +a,
        prob: pr === undefined || pr === "" ? 1 : +pr,
        ft: ft,
        ir: f === "i",
        est: !(ft === "me" || ft === "fa"),
        gp: 0,
        tot: 0
      });
    });
  });
  return out;
}
var init = function init() {
  return {
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
  };
};
var migrate = function migrate(v) {
  var weeks;
  if (!v.weeks.some(function (w) {
    return w.dates && w.dates.length;
  })) {
    weeks = defaultWeeks().map(function (w, i) {
      return v.weeks[i] ? {
        ...w,
        pairs: v.weeks[i].pairs || w.pairs,
        act: v.weeks[i].act || {},
        done: v.weeks[i].done || 0
      } : w;
    });
  } else weeks = v.weeks.map(function (w) {
    return {
      pairs: [],
      done: 0,
      act: {},
      ...w
    };
  });
  return {
    ...init(),
    ...v,
    weeks: weeks,
    players: v.players.map(function (p) {
      return {
        gp: 0,
        tot: 0,
        ...p
      };
    }),
    blend: v.blend === undefined ? 10 : v.blend,
    autoDone: v.autoDone === undefined ? true : v.autoDone,
    wk: Math.min(v.wk || 0, weeks.length - 1)
  };
};
var OUTS = ["OUT", "INJURY_RESERVE", "SUSPENSION"];
var DEFAULT_BACK = {
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
  var teams = (E.teams || []).map(function (t) {
    return {
      id: "t" + t.id,
      name: t.name
    };
  });
  if (!teams.length) throw new Error("The ESPN file has no teams in it.");
  var prev = {};
  s.players.forEach(function (p) {
    return prev[p.n.toLowerCase()] = p;
  });
  var players = (E.players || []).filter(function (p) {
    return p.n && NHL.includes(p.t);
  }).map(function (p) {
    var pv = prev[p.n.toLowerCase()];
    var gsAuto = s.autoGoalie !== false && p.p === "G" ? ((E.signals || {}).gstart || {})[p.id] : null;
    var prob = p.p === "G" ? gsAuto ? gsAuto.share : pv && pv.p === "G" && pv.prob > 0 ? pv.prob : 0.5 : p.status === "DAY_TO_DAY" ? 0.8 : 1;
    var avg = p.pavg > 0 ? p.pavg : pv ? pv.avg : p.avg > 0 ? p.avg : p.p === "G" ? 7 : 5;
    var back = pv && pv.back !== undefined ? pv.back : DEFAULT_BACK[p.n] || "";
    return {
      id: "e" + p.id,
      n: p.n,
      t: p.t,
      p: p.p,
      avg: Math.round(avg * 100) / 100,
      prob: prob,
      ft: p.ft ? "t" + p.ft : "fa",
      ir: p.ir !== undefined ? !!p.ir : !!(pv && pv.ir),
      est: !(p.pavg > 0) && !pv,
      gp: p.gp || 0,
      tot: p.tot || 0,
      status: p.status || "",
      back: back,
      proj: p.pavg > 0,
      keep: pv ? pv.keep : false,
      own: p.own || 0,
      chg: p.chg || 0,
      wv: !!p.wv
    };
  });
  var ms = E.matchups || [];
  var pack = function pack(mm) {
    var act = {};
    mm.forEach(function (m) {
      act["t" + m.home] = m.hs;
      act["t" + m.away] = m.as;
    });
    return {
      pairs: mm.map(function (m) {
        return ["t" + m.home, "t" + m.away];
      }),
      act: act
    };
  };
  var okWeeks = function okWeeks(ws) {
    return ws && ws.length >= 20 && ws.length <= 40 && ws.every(function (w) {
      return w.dates && w.dates.length;
    }) && ws.some(function (w) {
      return w.dates.length >= 5;
    });
  };
  var fromEspn = (E.periods || []).filter(function (pp) {
    return pp.dates && pp.dates.length;
  });
  var weeks;
  if (fromEspn.length >= 20 && fromEspn.length <= 40 && fromEspn.some(function (pp) {
    return pp.dates.length >= 5;
  })) {
    weeks = fromEspn.map(function (pp, i) {
      return {
        label: lab(i, pp.dates),
        dates: pp.dates,
        period: pp.id,
        done: 0,
        ...pack(ms.filter(function (m) {
          return m.period === pp.id;
        }))
      };
    });
  } else {
    var base = okWeeks(s.weeks) ? s.weeks : defaultWeeks();
    weeks = base.map(function (w, i) {
      return {
        ...w,
        period: i + 1,
        ...pack(ms.filter(function (m) {
          return m.period === i + 1;
        }))
      };
    });
  }
  var ci = weeks.findIndex(function (w) {
    return w.period === E.currentPeriod;
  });
  var wk = ci >= 0 ? ci : 0;
  var me = "t" + E.myTeamId;
  var opp = teams.some(function (t) {
    return t.id === s.opp;
  }) && s.opp !== me ? s.opp : (teams.find(function (t) {
    return t.id !== me;
  }) || {}).id;
  return {
    ...s,
    teams: teams,
    me: me,
    opp: opp,
    players: players,
    weeks: weeks,
    wk: wk,
    lastSync: E.generated,
    league: E.leagueName || "",
    goalies: E.goalies || s.goalies || {}
  };
}

// ---------- projections ----------
var effAvg0 = function effAvg0(p, K) {
  return p.gp > 0 ? (p.avg * K + p.tot) / (K + p.gp) : p.avg;
};
var effAvg = function effAvg(p, K, dt) {
  var base = effAvg0(p, K);
  var M = window.__MODEL,
    mode = window.__PMODE || "espn";
  {
    var A = window.__AI,
      aid = mode === "ai" && typeof p.id === "string" && p.id[0] === "e" ? p.id.slice(1) : null,
      ap = aid && A ? (A.proj || {})[aid] : null,
      av = ap ? dt && ap[dt] != null ? ap[dt] : (window.__AIAVG || {})[aid] : null;
    if (av != null) return av * (p.gwMul || 1);
  }
  var v = base;
  if (M && mode !== "espn" && typeof p.id === "string" && p.id[0] === "e") {
    var id = p.id.slice(1),
      pr = (M.proj || {})[id];
    var mv = dt && pr && pr[dt] != null ? pr[dt] : (M.base || {})[id];
    if (mv != null) {
      var mb = (M.base || {})[id];
      var ratio = dt && pr && pr[dt] != null && mb > 0 ? Math.max(0.5, Math.min(1.6, pr[dt] / mb)) : 1;
      v = mode === "model" ? mv : (base * ratio + mv) / 2;
    }
  }
  return v * (p.gwMul || 1);
};
var autoInj = function autoInj(p) {
  var S = window.__SIG || {};
  var id = typeof p.id === "string" && p.id[0] === "e" ? p.id.slice(1) : null;
  return id ? (S.injuries || {})[id] || null : null;
};
var effBack = function effBack(p) {
  if (p.back && p.back !== DEFAULT_BACK[p.n]) return {
    d: p.back,
    src: "you"
  };
  var a = autoInj(p);
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
var avail = function avail(p, date) {
  var b = effBack(p).d;
  if (b) {
    if (date && date < b) return 0;
    if (date && date < addDays(b, 7)) return 0.9;
    return 1;
  }
  var a = autoInj(p);
  var st = a && a.status || p.status || "";
  return OUTS.includes(st) || /^out|injured reserve|suspen/i.test(st) ? 0 : 1;
};
var nrm = function nrm(x) {
  return (x || "").normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase().trim();
};
// back-to-backs: starters usually rest the 2nd night, backups usually start it
var b2bAdj = function b2bAdj(p, dt) {
  var S = SCHED[p.t];
  if (!dt || !S || p.p !== "G") return null;
  var pc = function pc(v) {
    return " (".concat(Math.round(v * 100), "%)");
  };
  if (S.has(addDays(dt, -1))) {
    if (p.prob >= 0.55) {
      var v = p.prob * 0.5;
      return {
        v: v,
        l: "B2B 2nd night · likely rests" + pc(v),
        b2b: 2
      };
    }
    if (p.prob <= 0.45) {
      var _v = Math.min(0.8, p.prob + 0.3);
      return {
        v: _v,
        l: "B2B 2nd night · likely starts" + pc(_v),
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
      var _v2 = Math.min(0.95, p.prob + 0.1);
      return {
        v: _v2,
        l: "B2B 1st night · likely starts" + pc(_v2),
        b2b: 1
      };
    }
    if (p.prob <= 0.45) {
      var _v3 = Math.max(0.05, p.prob - 0.1);
      return {
        v: _v3,
        l: "B2B 1st night · likely rests" + pc(_v3),
        b2b: 1
      };
    }
  }
  return null;
};
var gStart = function gStart(p, dt) {
  var aiG = window.__PMODE === "ai" && dt && typeof p.id === "string" && p.id[0] === "e" ? (((window.__AI || {}).gstart || {})[p.id.slice(1)] || {})[dt] : null;
  var fallback = aiG != null ? {
    v: aiG,
    l: "AI start chance (".concat(Math.round(aiG * 100), "%)")
  } : b2bAdj(p, dt) || {
    v: p.prob,
    l: ""
  };
  var day = dt && (window.__GOALIES || {})[dt];
  if (!day) return fallback;
  var me = day[nrm(p.n)];
  if (me) {
    var st = (me.status || "").toLowerCase();
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
  var mate = Object.entries(day).find(function (_ref5) {
    var _ref6 = _slicedToArray(_ref5, 2),
      x = _ref6[1];
    return x.team === p.t;
  });
  if (mate) {
    var _st = (mate[1].status || "").toLowerCase();
    var mv = _st.includes("confirm") && !_st.includes("un") ? 1 : /likely|expected|project/.test(_st) ? 0.85 : 0.5;
    var who = mate[0].replace(/\b\w/g, function (c) {
      return c.toUpperCase();
    });
    return {
      v: 1 - mv,
      l: mv === 1 ? "not starting" : "backup \xB7 ".concat(who, " ").concat(mv === 0.5 ? "unconfirmed" : "likely", " (").concat(Math.round((1 - mv) * 100), "%)")
    };
  }
  return fallback;
};
function dayLineup(roster, wk, d, K, cap) {
  var c = cap || {
    F: 9,
    D: 5,
    U: 1,
    G: 2
  };
  var dt = wk.dates ? wk.dates[d] : null;
  var pl = roster.filter(function (p) {
    return !p.ir && p.prob > 0 && onDay(p, dt) && avail(p, dt) > 0 && (wk.games[p.t] || []).includes(d);
  }).map(function (p) {
    var g = p.p === "G" ? gStart(p, dt) : null;
    return {
      ...p,
      x: effAvg(p, K, dt) * (g ? g.v : p.prob) * avail(p, dt),
      gs: g ? g.l : "",
      dt: dt
    };
  });
  var by = function by(a, b) {
    return b.x - a.x;
  };
  var F = pl.filter(function (p) {
      return p.p === "F";
    }).sort(by),
    D = pl.filter(function (p) {
      return p.p === "D";
    }).sort(by),
    G = pl.filter(function (p) {
      return p.p === "G";
    }).sort(by);
  var fs = F.slice(0, c.F),
    ds = D.slice(0, c.D);
  var rest = [].concat(_toConsumableArray(F.slice(c.F)), _toConsumableArray(D.slice(c.D))).sort(by);
  var u = rest.slice(0, c.U),
    gs = G.slice(0, c.G);
  var bench = [].concat(_toConsumableArray(rest.slice(c.U)), _toConsumableArray(G.slice(c.G)));
  var start = [].concat(_toConsumableArray(fs.map(function (p) {
    return {
      ...p,
      slot: "F"
    };
  })), _toConsumableArray(ds.map(function (p) {
    return {
      ...p,
      slot: "D"
    };
  })), _toConsumableArray(u.map(function (p) {
    return {
      ...p,
      slot: "UTIL"
    };
  })), _toConsumableArray(gs.map(function (p) {
    return {
      ...p,
      slot: "G"
    };
  })));
  return {
    start: start,
    bench: bench,
    total: start.reduce(function (s, p) {
      return s + p.x;
    }, 0),
    empty: c.F - fs.length + (c.D - ds.length) + (c.U - u.length) + (c.G - gs.length),
    sched: pl.length
  };
}
function weekProj(roster, wk, K) {
  var from = arguments.length > 3 && arguments[3] !== undefined ? arguments[3] : 0;
  var days = wk.days.map(function (_, d) {
    return d < from ? null : dayLineup(roster, wk, d, K);
  });
  var live = days.filter(Boolean);
  var sum = function sum(f) {
    return live.reduce(function (s, x) {
      return s + f(x);
    }, 0);
  };
  return {
    days: days,
    total: sum(function (x) {
      return x.total;
    }),
    sched: sum(function (x) {
      return x.sched;
    }),
    used: sum(function (x) {
      return x.start.length;
    }),
    wasted: sum(function (x) {
      return x.bench.length;
    }),
    empty: sum(function (x) {
      return x.empty;
    })
  };
}
var oppOf = function oppOf(wk, me) {
  var pr = (wk.pairs || []).find(function (p) {
    return p[0] && p[1] && (p[0] === me || p[1] === me);
  });
  return pr ? pr[0] === me ? pr[1] : pr[0] : null;
};
var f1 = function f1(x) {
  return (Math.round((+x || 0) * 10) / 10).toFixed(1);
};
var toDate = function toDate(x) {
  if (!x) return null;
  var str = String(x);
  if (!/[zZ]$|[+-]\d\d:?\d\d$/.test(str)) str += "Z";
  var d = new Date(str);
  return isNaN(d) ? null : d;
};
var fmtTime = function fmtTime(x) {
  var d = toDate(x);
  return d ? d.toLocaleString("en-US", {
    weekday: "short",
    month: "short",
    day: "numeric",
    hour: "numeric",
    minute: "2-digit"
  }) : String(x || "");
};
var gms = function gms(wk, t) {
  return (wk.games[t] || []).length;
};

// ---------- signals ----------
var sigOf = function sigOf(p) {
  var S = window.__SIG || {};
  var id = typeof p.id === "string" && p.id[0] === "e" ? p.id.slice(1) : null;
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
var formRatio = function formRatio(p, K) {
  var r = sigOf(p).rec,
    b = effAvg(p, K);
  return r && r.gp >= 3 && b > 0 ? r.ppg / b : null;
};
var LBL = {
  F1: "1st line",
  F2: "2nd line",
  D1: "top pair",
  D2: "2nd pair"
};
var tags = function tags(p, K) {
  var g = sigOf(p),
    out = [],
    fr = formRatio(p, K);
  {
    var M = window.__MODEL,
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
    t: "started ".concat(g.gs.rs, " of last ").concat(g.gs.rg),
    c: g.gs.rs / g.gs.rg > g.gs.prior ? "text-green-700 font-semibold" : "text-red-600 font-semibold"
  });
  if (g.lines && g.lines.chg === "up") out.push({
    t: "\u2191 ".concat(LBL[g.lines.grp] || "promoted"),
    c: "text-green-700 font-semibold"
  });else if (g.lines && g.lines.chg === "down") out.push({
    t: "↓ demoted",
    c: "text-red-600"
  });
  if (g.luck && g.luck.t === "s" && Math.abs(g.luck.d) >= 2) out.push({
    t: g.luck.d > 0 ? "lucky +".concat(f1(g.luck.d), " G") : "unlucky ".concat(f1(g.luck.d), " G"),
    c: g.luck.d > 0 ? "text-amber-600" : "text-sky-600"
  });
  if (g.luck && g.luck.t === "g" && Math.abs(g.luck.d) >= 4) out.push({
    t: g.luck.d > 0 ? "hot SV +".concat(f1(g.luck.d)) : "cold SV ".concat(f1(g.luck.d)),
    c: g.luck.d > 0 ? "text-amber-600" : "text-sky-600"
  });
  if (fr !== null && fr >= 1.25) out.push({
    t: "".concat(f1(g.rec.ppg), "/g last 14d"),
    c: "text-orange-600"
  });else if (fr !== null && fr <= 0.7) out.push({
    t: "".concat(f1(g.rec.ppg), "/g last 14d"),
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
  var t = g.toi;
  if (t && t.d >= 120) out.push({
    t: "".concat(mm(t.d), " TOI"),
    c: "text-green-700 font-semibold"
  });else if (t && t.d <= -120) out.push({
    t: "".concat(mm(t.d), " TOI"),
    c: "text-red-600"
  });
  if (t && t.pd >= 60) out.push({
    t: "PP ".concat(mm(t.pd)),
    c: "text-green-700"
  });else if (t && t.pd <= -60) out.push({
    t: "PP ".concat(mm(t.pd)),
    c: "text-red-600"
  });
  if ((p.chg || 0) >= 5) out.push({
    t: "+".concat(f1(p.chg), "% rostered"),
    c: "text-green-700"
  });
  {
    var nw = newsOf(p)[0];
    if (nw) out.push({
      t: (nw.label ? nw.label + ": " : "") + (nw.h || "").slice(0, 60),
      c: NEWS_CLS[nw.kind] || "text-slate-500",
      u: nw.u
    });
  }
  return out;
};
var Tags = function Tags(_ref7) {
  var p = _ref7.p,
    K = _ref7.K;
  return /*#__PURE__*/React.createElement("span", {
    className: "inline-flex flex-wrap gap-x-2 gap-y-0.5"
  }, tags(p, K).map(function (t, i) {
    return t.u ? /*#__PURE__*/React.createElement("a", {
      key: i,
      href: t.u,
      target: "_blank",
      rel: "noreferrer",
      className: "text-xs underline " + t.c
    }, t.t) : /*#__PURE__*/React.createElement("span", {
      key: i,
      className: "text-xs " + t.c
    }, t.t);
  }));
};
// ice time: seconds -> "+2.5 min"
var mm = function mm(sec) {
  return (sec >= 0 ? "+" : "−") + (Math.abs(sec) / 60).toFixed(1) + " min";
};
var toiOf = function toiOf(p) {
  return sigOf(p).toi || null;
};
// ---------- move engine ----------
function computeMoves(s, o) {
  var K = s.blend,
    gw = s.gw ?? 1.3,
    protectTop = s.protectTop ?? 8;
  var mins = {
    F: s.minF ?? 10,
    D: s.minD ?? 5,
    G: s.minGo ?? 2
  };
  var H = o.H ?? 1,
    pos = o.pos || "all",
    q = (o.q || "").toLowerCase();
  var myR = s.players.filter(function (p) {
    return p.ft === s.me;
  });
  var fas = s.players.filter(function (p) {
    return p.ft === "fa";
  });
  var wt = function wt(p) {
    return p.p === "G" ? {
      ...p,
      gwMul: gw
    } : p;
  };
  var n = H === 0 ? s.weeks.length - s.wk : H;
  var horizon = s.weeks.slice(s.wk, s.wk + n).map(function (w, i) {
    var dw = deriveWeek(w, s.autoDone);
    return {
      wk: dw,
      from: i === 0 ? dw.done : 0
    };
  });
  var lineupAware = H !== 0;
  var total = function total(roster) {
    var r = roster.map(wt);
    return horizon.reduce(function (t, h) {
      return t + weekProj(r, h.wk, K, h.from).total;
    }, 0);
  };
  var gamesIn = function gamesIn(p) {
    var a = pickStart(p);
    var g = 0;
    horizon.forEach(function (h) {
      return (h.wk.games[p.t] || []).forEach(function (d) {
        var dt = h.wk.dates ? h.wk.dates[d] : null;
        if (d >= h.from && (!dt || dt >= a) && !p.ir && avail(p, dt)) g++;
      });
    });
    return g;
  };
  var rawPts = function rawPts(p, ref) {
    var a = pickStart(ref || p);
    var t = 0;
    horizon.forEach(function (h) {
      return (h.wk.games[p.t] || []).forEach(function (d) {
        var dt = h.wk.dates ? h.wk.dates[d] : null;
        if (d >= h.from && (!dt || dt >= a) && !p.ir && avail(p, dt)) t += effAvg(wt(p), K, dt) * p.prob;
      });
    });
    return t;
  };
  var ranked = myR.filter(function (p) {
    return !p.ir;
  }).sort(function (a, b) {
    return effAvg(wt(b), K) - effAvg(wt(a), K);
  });
  var autoProt = new Set(ranked.slice(0, protectTop).map(function (p) {
    return p.id;
  }));
  var protectedIds = new Set([].concat(_toConsumableArray(autoProt), _toConsumableArray(myR.filter(function (p) {
    return p.keep;
  }).map(function (p) {
    return p.id;
  }))));
  var cnt = {
    F: 0,
    D: 0,
    G: 0
  };
  myR.forEach(function (p) {
    if (!p.ir) cnt[p.p]++;
  });
  var keepsMins = function keepsMins(d, f) {
    return d.p === f.p || cnt[d.p] - 1 >= mins[d.p];
  };
  var canDrop = function canDrop(d, f) {
    return !d.ir && !protectedIds.has(d.id) && keepsMins(d, f);
  };
  var inTab = function inTab(f) {
    return pos === "all" || (pos === "pp1" ? !!sigOf(f).pp1 : pos === "sk" ? f.p !== "G" : f.p === pos);
  };
  var base = lineupAware ? total(myR) : 0;
  var pool = fas.filter(function (f) {
    return f.prob > 0 && (f.proj !== false || f.gp > 0) && inTab(f) && f.n.toLowerCase().includes(q) && (!!q || !goalieOut(f));
  }).map(function (f) {
    return {
      f: f,
      raw: rawPts(f)
    };
  }).filter(function (x) {
    return x.raw > 0;
  }).sort(function (a, b) {
    return b.raw - a.raw;
  }).slice(0, lineupAware ? o.pool || 120 : 500);
  var res = [];
  pool.forEach(function (_ref8) {
    var f = _ref8.f,
      raw = _ref8.raw;
    var best = null;
    myR.forEach(function (d) {
      if (!canDrop(d, f)) return;
      var gain = lineupAware ? total(timedMove(myR, s.me, [{
        add: f,
        drop: d
      }])) - base : raw - rawPts(d, f);
      if (!best || gain > best.gain) best = {
        gain: gain,
        d: d
      };
    });
    if (best) res.push({
      f: f,
      ...best
    });
  });
  res.sort(function (a, b) {
    return b.gain - a.gain;
  });
  return {
    res: res,
    total: total,
    gamesIn: gamesIn,
    rawPts: rawPts,
    autoProt: autoProt,
    protectedIds: protectedIds,
    cnt: cnt,
    mins: mins,
    keepsMins: keepsMins,
    lineupAware: lineupAware,
    myR: myR,
    fas: fas,
    K: K,
    gw: gw,
    protectTop: protectTop
  };
}

// ---------- shared UI ----------
var Card = function Card(_ref9) {
  var label = _ref9.label,
    value = _ref9.value,
    sub = _ref9.sub,
    tone = _ref9.tone;
  return /*#__PURE__*/React.createElement("div", {
    className: "rounded-xl p-4 border " + (tone || "bg-white border-slate-200")
  }, /*#__PURE__*/React.createElement("div", {
    className: "text-xs uppercase tracking-wide text-slate-500"
  }, label), /*#__PURE__*/React.createElement("div", {
    className: "text-2xl font-bold"
  }, value), sub && /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500 mt-1"
  }, sub));
};
var inp = "border border-slate-300 rounded-lg px-2 py-1.5 text-sm bg-white";
var box = "bg-white rounded-xl border border-slate-200 p-4 text-sm mb-4";
var Pills = function Pills(_ref0) {
  var items = _ref0.items,
    value = _ref0.value,
    onChange = _ref0.onChange;
  return /*#__PURE__*/React.createElement("div", {
    className: "flex gap-2 overflow-x-auto navscroll pb-1"
  }, items.map(function (_ref1) {
    var _ref10 = _slicedToArray(_ref1, 2),
      k = _ref10[0],
      l = _ref10[1];
    return /*#__PURE__*/React.createElement("button", {
      key: k,
      onClick: function onClick() {
        return onChange(k);
      },
      className: "px-3 py-1.5 rounded-full text-sm border whitespace-nowrap " + (value === k ? "bg-blue-600 text-white border-blue-600" : "bg-white border-slate-300 text-slate-600")
    }, l);
  }));
};
var teamName = function teamName(s, id) {
  return id === "fa" ? "Free agent" : (s.teams.find(function (t) {
    return t.id === id;
  }) || {}).name || "";
};
var PlayerLine = function PlayerLine(_ref11) {
  var s = _ref11.s,
    p = _ref11.p,
    extra = _ref11.extra;
  // player line v15: logo, name, one short note (news_logos.py)
  var tg = shortTag(p, s.blend);
  return /*#__PURE__*/React.createElement("div", {
    className: "flex items-center gap-3 py-2.5 border-t border-slate-100 text-sm"
  }, /*#__PURE__*/React.createElement(TeamLogo, {
    t: p.t,
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
var UIKEY = "fantasy-islands-gm-ui";
var __UI = null;
var uiGet = function uiGet() {
  if (!__UI) {
    try {
      __UI = JSON.parse(localStorage.getItem(UIKEY) || "{}") || {};
    } catch (e) {
      __UI = {};
    }
  }
  return __UI;
};
var uiSet = function uiSet(k, v) {
  var u = uiGet();
  u[k] = v;
  try {
    localStorage.setItem(UIKEY, JSON.stringify(u));
  } catch (e) {}
};
var secKey = function secKey(t) {
  return typeof t === "string" ? t.toLowerCase().replace(/[^a-z ]/g, " ").replace(/\s+/g, " ").trim().slice(0, 40) : "box";
};
// boxes that start closed: "tab:start of the title"
var SEC_SHUT = ["today:your lineup", "today:injuries", "today:news on your players", "myteam:this week day by day", "myteam:player updates", "myteam:injuries", "myteam:protected players", "moves/advice:free agents to watch", "moves/advice:trade advice", "moves/advice:line promotions", "moves/advice:luck", "moves/advice:model vs espn", "moves/planner:week ", "moves/planner:chronic bench players", "moves/trades:trade ideas", "teams:news", "league/power:how to climb the rankings", "league/standings:all teams this week", "news:your opponent", "news:around your league", "news:free agents", "news:phone notifications", "setup/settings:team names"];
var Section = function Section(_ref12) {
  var title = _ref12.title,
    sub = _ref12.sub,
    link = _ref12.link,
    children = _ref12.children,
    closed = _ref12.closed,
    id = _ref12.id;
  // section v40: the same corner-bracket panel as the new pages (news_logos.py)
  var _useState = useState(function () {
      return "sec:" + (window.__TAB || "") + ":" + (id || secKey(title));
    }),
    _useState2 = _slicedToArray(_useState, 1),
    k = _useState2[0];
  var _useState3 = useState(function () {
      var v = uiGet()[k];
      return v == null ? !(closed || SEC_SHUT.some(function (x) {
        return k.indexOf("sec:" + x) === 0;
      })) : !!v;
    }),
    _useState4 = _slicedToArray(_useState3, 2),
    open = _useState4[0],
    setOpen = _useState4[1];
  var flip = function flip() {
    uiSet(k, !open);
    setOpen(!open);
  };
  var onKey = function onKey(e) {
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
var SectionShut = function SectionShut(p) {
  return /*#__PURE__*/React.createElement(Section, _extends({}, p, {
    closed: true
  }));
};
var DayFold = function DayFold(_ref13) {
  var id = _ref13.id,
    open0 = _ref13.open0,
    head = _ref13.head,
    right = _ref13.right,
    children = _ref13.children;
  var k = "day:" + id;
  var _useState5 = useState(function () {
      var v = uiGet()[k];
      return v == null ? !!open0 : !!v;
    }),
    _useState6 = _slicedToArray(_useState5, 2),
    open = _useState6[0],
    setOpen = _useState6[1];
  var flip = function flip() {
    uiSet(k, !open);
    setOpen(!open);
  };
  var onKey = function onKey(e) {
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
var NAV = [["today", "Today", null], ["myteam", "My Team", null], ["matchup", "Matchup", null], ["moves", "Moves", [["advice", "Advice"], ["planner", "Planner"], ["goalies", "Goalie streams"], ["adddrop", "Add / Drop"], ["players", "Players"], ["trades", "Trades"], ["playoffs", "Playoffs"]]], ["teams", "Teams", null], ["lines", "Lines", null], ["league", "League", [["power", "Power rankings"], ["standings", "Standings"], ["odds", "Betting lines"]]], ["news", "News", null], ["setup", "Setup", [["settings", "Settings & backup"], ["sched", "Schedule & weeks"], ["bulk", "Bulk update"], ["inj", "Injury overrides"]]]];
function livePP1(E) {
  var L = window.LINES_DATA;
  if (!L || !L.teams || !E || !E.players || !window.__SIG) return;
  var k = function k(x) {
    return (x || "").normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase().replace(/[.'’]/g, "").replace(/-/g, " ").replace(/\s+/g, " ").trim();
  };
  var byT = {},
    byN = {};
  E.players.forEach(function (p) {
    if (!p.n) return;
    var n = k(p.n);
    byT[n + "|" + p.t] = String(p.id);
    byN[n] = byN[n] === undefined ? String(p.id) : null;
  });
  var idOf = function idOf(n, t) {
    return byT[k(n) + "|" + t] || byN[k(n)] || null;
  };
  var units = {},
    on = {},
    changes = {};
  Object.entries(L.teams).forEach(function (_ref14) {
    var _ref15 = _slicedToArray(_ref14, 2),
      t = _ref15[0],
      x = _ref15[1];
    var u = ((x || {}).lines || {}).PP1 || [];
    units[t] = u;
    u.forEach(function (n) {
      var id = idOf(n, t);
      if (id) on[id] = true;
    });
  });
  var since = Date.now() - 36 * 3600 * 1000;
  _toConsumableArray(L.changes || []).reverse().forEach(function (c) {
    if (c.type !== "pp" || Date.parse(c.at) < since) return;
    var id = idOf(c.name, c.team) || (c.e ? String(c.e) : null);
    if (id) changes[id] = c.dir === "up" ? "added" : "removed";
  });
  Object.keys(changes).forEach(function (id) {
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
      on: on,
      changes: changes,
      units: units
    }
  };
}
function App() {
  var _useState7 = useState(init),
    _useState8 = _slicedToArray(_useState7, 2),
    s = _useState8[0],
    setS = _useState8[1];
  var _useState9 = useState("today"),
    _useState0 = _slicedToArray(_useState9, 2),
    tab = _useState0[0],
    setTab = _useState0[1];
  var _useState1 = useState({
      moves: "advice",
      league: "power",
      setup: "settings"
    }),
    _useState10 = _slicedToArray(_useState1, 2),
    subs = _useState10[0],
    setSubs = _useState10[1];
  var _useState11 = useState(false),
    _useState12 = _slicedToArray(_useState11, 2),
    loaded = _useState12[0],
    setLoaded = _useState12[1];
  var _useState13 = useState(""),
    _useState14 = _slicedToArray(_useState13, 2),
    status = _useState14[0],
    setStatus = _useState14[1];
  var _useState15 = useState(""),
    _useState16 = _slicedToArray(_useState15, 2),
    syncMsg = _useState16[0],
    setSyncMsg = _useState16[1];
  var _useState17 = useState(null),
    _useState18 = _slicedToArray(_useState17, 2),
    teamView = _useState18[0],
    setTeamView = _useState18[1];
  var _useState19 = useState(null),
    _useState20 = _slicedToArray(_useState19, 2),
    prevTab = _useState20[0],
    setPrevTab = _useState20[1];
  var _useState21 = useState(null),
    _useState22 = _slicedToArray(_useState21, 2),
    player = _useState22[0],
    setPlayer = _useState22[1];
  var _useState23 = useState(null),
    _useState24 = _slicedToArray(_useState23, 2),
    tradePartner = _useState24[0],
    setTradePartner = _useState24[1];
  var _useState25 = useState(0),
    _useState26 = _slicedToArray(_useState25, 2),
    tick = _useState26[1];
  useEffect(function () {
    var h32 = function h32() {
      return tick(function (x) {
        return x + 1;
      });
    };
    window.addEventListener("gm-theme", h32);
    return function () {
      return window.removeEventListener("gm-theme", h32);
    };
  }, []);
  useEffect(function () {
    // round 21: live NHL scores straight from the NHL every minute (falls back to the sync's copy if blocked)
    var dead = false;
    var AL = {
      LAK: "LA",
      NJD: "NJ",
      SJS: "SJ",
      TBL: "TB",
      UTAH: "UTA",
      ARI: "UTA"
    };
    var pull = function pull() {
      return fetch("https://api-web.nhle.com/v1/score/now").then(function (r) {
        return r.ok ? r.json() : null;
      }).then(function (js) {
        if (dead || !js || !js.games) return;
        var out = {};
        js.games.forEach(function (g) {
          var d = g.gameDate;
          if (!d) return;
          var st = g.gameState,
            s = st === "FINAL" || st === "OFF" ? "F" : st === "LIVE" || st === "CRIT" ? "L" : "P";
          var pd = g.periodDescriptor || {},
            n = pd.number || 1,
            ck = g.clock || {};
          var rem = ck.secondsRemaining == null ? 1200 : ck.secondsRemaining;
          var f = s === "F" ? 1 : s === "P" ? 0 : Math.min(0.99, ((n - 1) * 1200 + 1200 - rem) / 3600);
          var per = pd.periodType === "OT" ? "OT" : pd.periodType === "SO" ? "SO" : ["", "1st", "2nd", "3rd"][n] || String(n);
          var hs = (g.homeTeam || {}).score,
            as = (g.awayTeam || {}).score;
          out[d] = out[d] || {};
          [[g.homeTeam, hs, as], [g.awayTeam, as, hs]].forEach(function (_ref16) {
            var _ref17 = _slicedToArray(_ref16, 3),
              T = _ref17[0],
              my = _ref17[1],
              op = _ref17[2];
            var a = T && (AL[T.abbrev] || T.abbrev);
            if (a) out[d][a] = {
              s: s,
              f: f,
              my: my,
              op: op,
              per: per,
              clk: ck.timeRemaining || "",
              int: !!ck.inIntermission
            };
          });
        });
        window.__LIVESC = out;
        tick(function (x) {
          return x + 1;
        });
      }).catch(function () {});
    };
    pull();
    var id = setInterval(pull, 60 * 1000);
    return function () {
      dead = true;
      clearInterval(id);
    };
  }, []);
  useEffect(function () {
    var st = init();
    try {
      var v = JSON.parse(localStorage.getItem(KEY) || "null");
      if (v && v.players && v.weeks) st = migrate(v);
    } catch (e) {}
    var E = window.ESPN_DATA;
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
  useEffect(function () {
    if (!loaded) return;
    var id = setInterval(function () {
      var sc = document.createElement("script");
      sc.src = "espn-data.js?t=" + Date.now();
      sc.onload = function () {
        sc.remove();
        var E = window.ESPN_DATA;
        tick(function (x) {
          return x + 1;
        });
        if (!E || !E.generated) return;
        setS(function (st) {
          if (E.generated === st.lastSync) return st;
          try {
            var n = applyESPN(st, E);
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
      sc.onerror = function () {
        return sc.remove();
      };
      document.head.appendChild(sc);
      var ls = document.createElement("script");
      ls.src = "lines-data.js?t=" + Date.now();
      ls.onload = ls.onerror = function () {
        return ls.remove();
      };
      document.head.appendChild(ls);
    }, 2 * 60 * 1000);
    return function () {
      return clearInterval(id);
    };
  }, [loaded]);
  useEffect(function () {
    if (!loaded) return;
    var t = setTimeout(function () {
      try {
        localStorage.setItem(KEY, JSON.stringify(s));
        setStatus("Saved");
      } catch (e) {
        setStatus("Save failed");
      }
    }, 700);
    return function () {
      return clearTimeout(t);
    };
  }, [s, loaded]);
  var E = window.ESPN_DATA;
  window.__MODEL = E && E.model || null;
  window.__SIG = E && E.signals || null;
  livePP1(E);
  window.__PLAYERS = s.players;
  useEffect(function () {
    fetch("ai/models/ai_proj.json?t=" + Date.now()).then(function (r) {
      return r.ok ? r.json() : null;
    }).then(function (A) {
      if (!A || !A.proj || !((Date.now() - Date.parse(A.asof)) / 36e5 < 36)) return;
      var avg = {};
      Object.entries(A.proj).forEach(function (_ref18) {
        var _ref19 = _slicedToArray(_ref18, 2),
          id = _ref19[0],
          m = _ref19[1];
        var v = Object.values(m).filter(function (x) {
          return x != null;
        });
        if (v.length) avg[id] = v.reduce(function (a, b) {
          return a + b;
        }, 0) / v.length;
      });
      window.__AI = A;
      window.__AIAVG = avg;
      setS(function (st) {
        return {
          ...st,
          players: _toConsumableArray(st.players)
        };
      });
    }).catch(function () {});
  }, []);
  // change 072 (gx072-app): keep the address bar in step with the page, and follow Back and Forward
  window.__ROUTE = {
    tab: tab,
    sub: subs[tab],
    team: tab === "teams" ? teamView : null
  };
  var gxWant = React.useRef(null);
  useEffect(function () {
    if (!loaded) return;
    var apply = function apply() {
      var r = gxParseHash(window.location.hash);
      if (!r) return;
      var pl = r.pid ? (window.__PLAYERS || []).find(function (p) {
        return p.id === r.pid;
      }) || null : null;
      var want = gxHash(r.tab, r.sub, r.team, pl ? pl.id : null);
      gxWant.current = want;
      setTimeout(function () {
        if (gxWant.current === want) gxWant.current = null;
      }, 1500);
      setTab(r.tab);
      if (r.sub) setSubs(function (x) {
        return _defineProperty({}, r.tab, r.sub);
      });
      setTeamView(r.tab === "teams" ? r.team : null);
      setPlayer(pl);
    };
    apply();
    window.addEventListener("popstate", apply);
    return function () {
      return window.removeEventListener("popstate", apply);
    };
  }, [loaded]);
  useEffect(function () {
    if (!loaded) return;
    var h = gxHash(tab, subs[tab], tab === "teams" ? teamView : null, player ? player.id : null);
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
  window.__GOALIES = useMemo(function () {
    var o = {};
    Object.entries(s.goalies || {}).forEach(function (_ref21) {
      var _ref22 = _slicedToArray(_ref21, 2),
        d = _ref22[0],
        m = _ref22[1];
      o[d] = {};
      Object.entries(m || {}).forEach(function (_ref23) {
        var _ref24 = _slicedToArray(_ref23, 2),
          n = _ref24[0],
          v = _ref24[1];
        o[d][nrm(n)] = v;
      });
    });
    return o;
  }, [s.goalies]);
  var w0 = s.weeks[s.wk] || s.weeks[0];
  var wk = useMemo(function () {
    return deriveWeek(w0, s.autoDone);
  }, [w0, s.autoDone]);
  var setWk = function setWk(patch) {
    return setS(function (st) {
      return {
        ...st,
        weeks: st.weeks.map(function (w, i) {
          return i === st.wk ? {
            ...w,
            ...(typeof patch === "function" ? patch(w) : patch)
          } : w;
        })
      };
    });
  };
  var go = function go(t, sub, extra) {
    setTab(t);
    setPlayer(null);
    if (sub) setSubs(function (x) {
      return _defineProperty({}, t, sub);
    });
    if (extra && extra.partner) setTradePartner(extra.partner);
    if (t === "teams") setTeamView(null);
    window.scrollTo(0, 0);
  };
  var openTeam = function openTeam(id) {
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
  var backFromTeam = function backFromTeam() {
    setTeamView(null);
    if (prevTab) setTab(prevTab);
    window.scrollTo(0, 0);
  };
  window.__NAV = {
    team: openTeam,
    player: function player(p) {
      if (p) setPlayer(p);
    },
    lines: function lines(t) {
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
  var P = {
    s: s,
    setS: setS,
    wk: wk,
    setWk: setWk,
    go: go
  };
  var LH = {
    gState: gState,
    actDay: actDay,
    LiveTag: LiveTag,
    pStat: pStat,
    gScore: gScore,
    effAvg: effAvg,
    sigOf: sigOf,
    Tags: Tags,
    avail: avail,
    effBack: effBack,
    gStart: gStart,
    teamName: teamName,
    f1: f1,
    Section: Section,
    Card: Card,
    Pills: Pills,
    inp: inp,
    SCHED: SCHED,
    todayISO: todayISO,
    dayLabel: dayLabel,
    TL: TL,
    TeamLogo: TeamLogo
  };
  var genAt = E && toDate(E.generated);
  var ageH = genAt ? (Date.now() - genAt.getTime()) / 36e5 : null;
  var nav = NAV.find(function (n) {
    return n[0] === tab;
  });
  var sub = subs[tab];
  var content = null;
  if (tab === "today") content = /*#__PURE__*/React.createElement(Today, P);else if (tab === "myteam") content = /*#__PURE__*/React.createElement(MyTeam, P);else if (tab === "matchup") content = /*#__PURE__*/React.createElement(Matchup, P);else if (tab === "teams") content = teamView ? /*#__PURE__*/React.createElement(TeamPage, _extends({}, P, {
    id: teamView,
    back: backFromTeam
  })) : /*#__PURE__*/React.createElement(TeamsTab, _extends({}, P, {
    openTeam: openTeam
  }));else if (tab === "lines") content = window.LinesTab ? /*#__PURE__*/React.createElement(window.LinesTab, _extends({}, P, {
    H: LH
  })) : /*#__PURE__*/React.createElement("div", {
    className: "text-slate-400 p-4"
  }, "The Lines tab could not load (lines-tab.js). Refresh the page; if it keeps happening, check that lines-tab.js is in the repo.");else if (tab === "news") content = /*#__PURE__*/React.createElement("div", {
    className: "space-y-4"
  }, /*#__PURE__*/React.createElement(NewsView, {
    s: s,
    wk: wk
  }), /*#__PURE__*/React.createElement(PhoneFeed, null));else if (tab === "moves") content = sub === "planner" ? /*#__PURE__*/React.createElement(PlannerAll, P) : sub === "goalies" ? /*#__PURE__*/React.createElement(GoalieStreams, P) : sub === "adddrop" ? /*#__PURE__*/React.createElement(Pickups, P) : sub === "players" ? /*#__PURE__*/React.createElement(Players, P) : sub === "trades" ? /*#__PURE__*/React.createElement(TradesPanel, _extends({
    key: tradePartner || "none"
  }, P, {
    initPartner: tradePartner
  })) : sub === "playoffs" ? /*#__PURE__*/React.createElement(PlayoffPlanner, P) : /*#__PURE__*/React.createElement(AdviceAll, P);else if (tab === "league") content = sub === "playoffs" ? /*#__PURE__*/React.createElement(PlayoffPlanner, P) : /*#__PURE__*/React.createElement(LeaguePage, P);else if (tab === "setup") content = sub === "sched" ? /*#__PURE__*/React.createElement(Schedule, P) : sub === "bulk" ? /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement(Bulk, {
    s: s,
    setS: setS
  }), /*#__PURE__*/React.createElement(AddOne, P)) : sub === "inj" ? /*#__PURE__*/React.createElement(InjuryPanel, P) : sub === "odds" ? /*#__PURE__*/React.createElement(OddsBoard, {
    s: s
  }) : sub === "alerts" ? /*#__PURE__*/React.createElement(GxAlertsPage, P) : sub === "adv" ? /*#__PURE__*/React.createElement(Settings, P) : /*#__PURE__*/React.createElement(SetupPage, _extends({}, P, {
    sub: sub
  }));
  return /*#__PURE__*/React.createElement("div", {
    className: "min-h-screen bg-slate-100 text-slate-900"
  }, /*#__PURE__*/React.createElement("div", {
    className: "sticky top-0 z-30 bg-slate-900 border-b border-slate-800"
  }, /*#__PURE__*/React.createElement(MobileHeader, {
    s: s,
    setS: setS,
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
  }, /*#__PURE__*/React.createElement(SubBar, {
    tab: tab,
    sub: sub,
    go: go,
    setSubs: setSubs,
    nav: nav,
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
  }), content, window.AskPanel ? /*#__PURE__*/React.createElement(window.AskPanel, _extends({}, P, {
    tab: tab,
    H: {
      effAvg: effAvg,
      sigOf: sigOf,
      tags: tags,
      avail: avail,
      effBack: effBack,
      gStart: gStart,
      teamName: teamName,
      f1: f1,
      computeMoves: computeMoves,
      weekProj: weekProj,
      oppOf: oppOf,
      todayISO: todayISO
    }
  })) : null), player && window.PlayerPopup ? /*#__PURE__*/React.createElement(window.PlayerPopup, {
    p: player,
    s: s,
    wk: wk,
    H: LH,
    onClose: function onClose() {
      return setPlayer(null);
    }
  }) : null);
}

// ---------- Today ----------
function Today(_ref26) {
  var s = _ref26.s,
    wk = _ref26.wk,
    go = _ref26.go;
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
  var K = s.blend;
  var opp = oppOf(wk, s.me) || s.opp;
  var mine = s.players.filter(function (p) {
      return p.ft === s.me;
    }),
    theirs = s.players.filter(function (p) {
      return p.ft === opp;
    });
  var A = weekLive(mine, wk, K, s.me),
    B = weekLive(theirs, wk, K, opp);
  var aA = +(wk.act || {})[s.me] || 0,
    aB = +(wk.act || {})[opp] || 0;
  var fa = aA + A.total,
    fb = aB + B.total,
    margin = fa - fb,
    ahead = margin >= 0;
  var dates = wk.dates || [],
    n = dates.length,
    today = todayISO(),
    done = wk.done || 0;
  var over = n > 0 && done >= n;
  var wp = winProb(A, B, aA, aB);
  var sN = useMemo(function () {
    return nextWkS(s);
  }, [s]);
  var sP = useMemo(function () {
    return planS(s);
  }, [s]);
  // change 071: next week win chance no longer needed on Today

  var tag = "Week " + (s.wk + 1) + (!n ? "" : dates[0] > today ? " \xB7 starts " + dayLabel(dates[0]) : over ? " \xB7 final" : " \xB7 day " + Math.min(n, done + 1) + " of " + n);
  var share = aA + aB > 0 ? Math.max(4, Math.min(96, aA / (aA + aB) * 100)) : 50;
  var big = {
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
    onClick: function onClick() {
      return go("matchup");
    }
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
      margin: "0 auto",
      color: ahead ? "var(--good)" : "var(--bad)"
    }
  }, (ahead ? "Ahead by " : "Behind by ") + f1(Math.abs(margin))), /*#__PURE__*/React.createElement("span", null, Math.round(fb)))), /*#__PURE__*/React.createElement(GxRace, {
    s: s,
    wk: wk
  }), /*#__PURE__*/React.createElement(GxHome, {
    s: s,
    wk: wk,
    A: A,
    B: B
  }));
}
function NewsView(_ref27) {
  var s = _ref27.s,
    wk = _ref27.wk;
  var _useState27 = useState("all"),
    _useState28 = _slicedToArray(_useState27, 2),
    f = _useState28[0],
    setF = _useState28[1];
  var _useState29 = useState({}),
    _useState30 = _slicedToArray(_useState29, 2),
    open = _useState30[0],
    setOpen = _useState30[1];
  var opp = wk ? oppOf(wk, s.me) : null;
  var pass = function pass(n) {
    return f === "all" || (f === "inj" ? NEWS_OUT.has(n.kind) : f === "moves" ? n.kind === "trade" || n.kind === "roster" : n.kind === "hot");
  };
  var rows = s.players.map(function (p) {
    return {
      p: p,
      items: newsOf(p).filter(pass)
    };
  }).filter(function (x) {
    return x.items.length;
  }).sort(function (a, b) {
    return NEWS_RANK[a.items[0].kind] - NEWS_RANK[b.items[0].kind] || a.items[0].age - b.items[0].age;
  });
  var only = function only(list, keep) {
    return list.map(function (x) {
      return {
        ...x,
        items: x.items.filter(keep)
      };
    }).filter(function (x) {
      return x.items.length;
    });
  };
  var groups = [["mine", "Your players", "Regular news shows for a day, hot streaks for 3 days, and injuries, scratches, trades and roster moves for a week.", rows.filter(function (x) {
    return x.p.ft === s.me;
  }), true], ["opp", opp ? "Your opponent · " + teamName(s, opp) : "", "Everything current on the team you play this week.", opp ? rows.filter(function (x) {
    return x.p.ft === opp;
  }) : [], false], ["league", "Around your league", "Other fantasy teams: important news and hot streaks only.", only(rows.filter(function (x) {
    return x.p.ft !== s.me && x.p.ft !== opp && x.p.ft !== "fa";
  }), function (n) {
    return n.kind !== "news";
  }), false], ["fa", "Free agents", "Only important news: injuries, scratches, trades and roster moves.", only(rows.filter(function (x) {
    return x.p.ft === "fa";
  }), function (n) {
    return NEWS_BIG.has(n.kind);
  }), false]];
  return /*#__PURE__*/React.createElement("div", {
    className: "space-y-4"
  }, /*#__PURE__*/React.createElement(Pills, {
    items: [["all", "All"], ["inj", "Injuries & scratches"], ["moves", "Trades & roster moves"], ["hot", "Hot"]],
    value: f,
    onChange: setF
  }), !window.__SIG && /*#__PURE__*/React.createElement("div", {
    className: box + " text-slate-400"
  }, "No news loaded yet."), groups.filter(function (g) {
    return g[4] || g[3].length;
  }).map(function (_ref28) {
    var _ref29 = _slicedToArray(_ref28, 4),
      k = _ref29[0],
      title = _ref29[1],
      sub = _ref29[2],
      list = _ref29[3];
    var shown = open[k] ? list : list.slice(0, 8);
    return /*#__PURE__*/React.createElement(Section, {
      key: k,
      title: title + " (" + list.length + ")",
      sub: sub
    }, shown.length ? shown.map(function (_ref30) {
      var p = _ref30.p,
        items = _ref30.items;
      return /*#__PURE__*/React.createElement("div", {
        key: p.id,
        className: "flex gap-3 py-2.5 border-t border-slate-100"
      }, /*#__PURE__*/React.createElement("div", {
        className: "pt-0.5"
      }, /*#__PURE__*/React.createElement(TeamLogo, {
        t: p.t,
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
      }))), items.slice(0, 2).map(function (n, i) {
        return /*#__PURE__*/React.createElement(NewsItem, {
          key: i,
          n: n
        });
      })));
    }) : /*#__PURE__*/React.createElement("div", {
      className: "text-slate-400 text-xs"
    }, "Nothing current."), list.length > shown.length && /*#__PURE__*/React.createElement("button", {
      className: "text-sm text-blue-600 mt-2",
      onClick: function onClick() {
        return setOpen(_defineProperty({}, k, true));
      }
    }, "Show all ", list.length));
  }));
}

// ---------- Betting lines ----------
var oddsFor = function oddsFor(t, dt) {
  var O = ((window.ESPN_DATA || {}).model || {}).odds || {};
  return dt && O[dt] ? O[dt][t] || null : null;
};
function OddsBoard(_ref31) {
  var s = _ref31.s;
  var O = ((window.ESPN_DATA || {}).model || {}).odds || null;
  var today = todayISO();
  var w = deriveWeek(s.weeks[s.wk] || s.weeks[0], s.autoDone);
  var opp = oppOf(w, s.me);
  var count = function count(tid, team) {
    return s.players.filter(function (p) {
      return p.ft === tid && p.t === team && !p.ir;
    }).length;
  };
  if (!O || !Object.keys(O).length) return /*#__PURE__*/React.createElement("div", {
    className: box + " text-slate-400"
  }, "No betting lines in the data yet \u2014 run the sync.");
  var days = Object.keys(O).filter(function (d) {
    return d >= today;
  }).sort();
  return /*#__PURE__*/React.createElement("div", {
    className: "space-y-4"
  }, /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500"
  }, "Win chance (bookmaker margin removed) and expected goals per team, refreshed every 4 hours. Used by the GM model and shown on the Matchup tab as \"W %\" (goalies) and \"xG\" (skaters). Rows with your players are highlighted."), days.map(function (d) {
    var games = Object.entries(O[d]).filter(function (_ref32) {
      var _ref33 = _slicedToArray(_ref32, 2),
        v = _ref33[1];
      return v.home;
    });
    return /*#__PURE__*/React.createElement("div", {
      key: d,
      className: "bg-white rounded-xl border border-slate-200 overflow-x-auto"
    }, /*#__PURE__*/React.createElement("div", {
      className: "px-4 py-2 border-b border-slate-200 font-semibold text-sm"
    }, dayLabel(d), " \xB7 ", games.length, " games"), /*#__PURE__*/React.createElement("table", {
      className: "w-full text-sm"
    }, /*#__PURE__*/React.createElement("thead", {
      className: "text-left"
    }, /*#__PURE__*/React.createElement("tr", null, ["Game", "Win chance", "Expected goals", "Total", "Yours", opp ? teamName(s, opp) : "Opponent"].map(function (h) {
      return /*#__PURE__*/React.createElement("th", {
        key: h,
        className: "px-3 py-2"
      }, h);
    }))), /*#__PURE__*/React.createElement("tbody", null, games.map(function (_ref34) {
      var _ref35 = _slicedToArray(_ref34, 2),
        home = _ref35[0],
        v = _ref35[1];
      var a = O[d][v.opp] || {};
      var mineN = count(s.me, home) + count(s.me, v.opp),
        oppN = opp ? count(opp, home) + count(opp, v.opp) : 0;
      var fav = v.win >= 0.5 ? home : v.opp;
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
  var K = s.blend,
    nD = wk.days.length;
  var mins = {
    F: s.minF ?? 10,
    D: s.minD ?? 5,
    G: s.minGo ?? 2
  };
  var minGain = s.minGain ?? 3;
  var myR = s.players.filter(function (p) {
    return p.ft === s.me;
  });
  var ranked = myR.filter(function (p) {
    return !p.ir;
  }).sort(function (a, b) {
    return effAvg(b, K) - effAvg(a, K);
  });
  var prot = new Set([].concat(_toConsumableArray(ranked.slice(0, s.protectTop ?? 8).map(function (p) {
    return p.id;
  })), _toConsumableArray(myR.filter(function (p) {
    return p.keep;
  }).map(function (p) {
    return p.id;
  }))));
  var val = function val(p, a) {
    return (wk.games[p.t] || []).filter(function (d) {
      return d >= a;
    }).reduce(function (t, d) {
      var dt = wk.dates[d];
      return t + effAvg(p, K, dt) * (p.p === "G" ? gStart(p, dt).v : p.prob) * avail(p, dt);
    }, 0);
  };
  var dayTotal = function dayTotal(tl, d) {
    return dayLineup(tl.filter(function (x) {
      return x.from <= d && x.to >= d;
    }).map(function (x) {
      return x.p;
    }), wk, d, K).total;
  };
  var tl = myR.map(function (p) {
    return {
      p: p,
      from: 0,
      to: nD - 1,
      orig: true
    };
  });
  var fas = s.players.filter(function (p) {
    return p.ft === "fa" && p.prob > 0 && (p.proj !== false || p.gp > 0) && !goalieOut(p);
  }).map(function (p) {
    return {
      p: p,
      v: val(p, d0)
    };
  }).filter(function (x) {
    return x.v > 0;
  }).sort(function (a, b) {
    return b.v - a.v;
  }).slice(0, 45).map(function (x) {
    return x.p;
  });
  var base0 = 0;
  for (var d = d0; d < nD; d++) base0 += dayTotal(tl, d);
  var steps = [],
    usedFA = new Set();
  var _loop = function _loop() {
    var cur = [];
    for (var _d2 = d0; _d2 < nD; _d2++) cur[_d2] = dayTotal(tl, _d2);
    var suffix = function suffix(a) {
      var t = 0;
      for (var _d3 = a; _d3 < nD; _d3++) t += cur[_d3];
      return t;
    };
    var best = null;
    var _loop2 = function _loop2(_d4) {
      var active = tl.filter(function (x) {
        return x.from <= _d4 && x.to >= _d4;
      });
      var cnt = {
        F: 0,
        D: 0,
        G: 0
      };
      active.forEach(function (x) {
        if (!x.p.ir) cnt[x.p.p]++;
      });
      var drops = active.filter(function (x) {
        return !x.p.ir && x.to === nD - 1 && x.from < _d4 + (x.orig ? 1 : 0) && !(x.orig && prot.has(x.p.id)) && !(!x.orig && x.from >= _d4);
      }).map(function (x) {
        return {
          x: x,
          v: val(x.p, _d4)
        };
      }).sort(function (a, b) {
        return a.v - b.v;
      });
      var cand = [];
      ["F", "D", "G"].forEach(function (ps) {
        return drops.filter(function (y) {
          return y.x.p.p === ps;
        }).slice(0, 4).forEach(function (y) {
          return cand.push(y.x);
        });
      });
      var before = suffix(_d4);
      var _iterator = _createForOfIteratorHelper(fas),
        _step;
      try {
        for (_iterator.s(); !(_step = _iterator.n()).done;) {
          var f = _step.value;
          if (usedFA.has(f.id) || !(wk.games[f.t] || []).includes(_d4) || wk.dates[_d4] < pickStart(f)) continue;
          var _iterator2 = _createForOfIteratorHelper(cand),
            _step2;
          try {
            var _loop3 = function _loop3() {
              var x = _step2.value;
              if (x.p.p !== f.p && cnt[x.p.p] - 1 < mins[x.p.p]) return 1; // continue
              var tl2 = tl.map(function (y) {
                return y === x ? {
                  ...y,
                  to: _d4 - 1
                } : y;
              }).concat([{
                p: {
                  ...f,
                  ft: s.me
                },
                from: _d4,
                to: nD - 1,
                orig: false
              }]);
              var after = 0;
              for (var dd = _d4; dd < nD; dd++) after += dayTotal(tl2, dd);
              var gain = after - before;
              if (!best || gain > best.gain) best = {
                gain: gain,
                d: _d4,
                f: f,
                x: x,
                tl2: tl2
              };
            };
            for (_iterator2.s(); !(_step2 = _iterator2.n()).done;) {
              if (_loop3()) continue;
            }
          } catch (err) {
            _iterator2.e(err);
          } finally {
            _iterator2.f();
          }
        }
      } catch (err) {
        _iterator.e(err);
      } finally {
        _iterator.f();
      }
    };
    for (var _d4 = d0; _d4 < nD; _d4++) {
      _loop2(_d4);
    }
    if (!best || best.gain < minGain) return 1; // break
    steps.push({
      day: best.d,
      add: best.f,
      drop: best.x.p,
      dropWasStream: !best.x.orig,
      gain: best.gain
    });
    usedFA.add(best.f.id);
    tl = best.tl2;
  };
  for (var k = 0; k < M; k++) {
    if (_loop()) break;
  }
  var final = 0;
  for (var _d = d0; _d < nD; _d++) final += dayTotal(tl, _d);
  return {
    steps: steps.sort(function (a, b) {
      return a.day - b.day;
    }),
    gain: final - base0,
    base: base0,
    final: final,
    pool: fas.length,
    d0: d0
  };
}
// ---------- Playoff planner ----------
function PlayoffPlanner(_ref36) {
  var s = _ref36.s,
    setS = _ref36.setS;
  var K = s.blend;
  var st = s.poStart ?? 24,
    nW = s.poWeeks ?? 3;
  var _useState31 = useState("fa"),
    _useState32 = _slicedToArray(_useState31, 2),
    who = _useState32[0],
    setWho = _useState32[1];
  var _useState33 = useState("all"),
    _useState34 = _slicedToArray(_useState33, 2),
    pos = _useState34[0],
    setPos = _useState34[1];
  var _useState35 = useState(""),
    _useState36 = _slicedToArray(_useState35, 2),
    q = _useState36[0],
    setQ = _useState36[1];
  var _useState37 = useState(false),
    _useState38 = _slicedToArray(_useState37, 2),
    showTeams = _useState38[0],
    setShowTeams = _useState38[1];
  var weeks = useMemo(function () {
    return s.weeks.slice(st, st + nW).map(function (w) {
      return deriveWeek(w, false);
    });
  }, [s.weeks, st, nW]);
  var dates = weeks.flatMap(function (w) {
    return w.dates || [];
  });
  var perDay = {};
  dates.forEach(function (d) {
    return perDay[d] = NHL.filter(function (t) {
      return SCHED[t] && SCHED[t].has(d);
    }).length / 2;
  });
  var light = new Set(dates.filter(function (d) {
    return perDay[d] > 0 && perDay[d] <= 5;
  }));
  var teamRows = NHL.map(function (t) {
    var per = weeks.map(function (w) {
      return gms(w, t);
    });
    var tot = per.reduce(function (a, b) {
      return a + b;
    }, 0);
    var off = dates.filter(function (d) {
      return light.has(d) && SCHED[t].has(d);
    }).length;
    return {
      t: t,
      per: per,
      tot: tot,
      off: off
    };
  }).sort(function (a, b) {
    return b.tot - a.tot || b.off - a.off;
  });
  var avgGames = teamRows.reduce(function (a, r) {
    return a + r.tot;
  }, 0) / teamRows.length;
  var tg = {};
  teamRows.forEach(function (r) {
    return tg[r.t] = r;
  });
  var val = function val(p) {
    var v = 0;
    dates.forEach(function (d) {
      if (SCHED[p.t] && SCHED[p.t].has(d)) v += effAvg(p, K, d) * p.prob * avail(p, d);
    });
    return v;
  };
  var rows = useMemo(function () {
    return s.players.filter(function (p) {
      return (who === "all" || (who === "fa" ? p.ft === "fa" : who === "mine" ? p.ft === s.me : p.ft !== "fa" && p.ft !== s.me)) && (pos === "all" || p.p === pos) && p.n.toLowerCase().includes(q.toLowerCase()) && p.prob > 0;
    }).map(function (p) {
      var v = val(p);
      var r = tg[p.t] || {
        tot: 0,
        off: 0,
        per: []
      };
      return {
        p: p,
        v: v,
        g: r.tot,
        off: r.off,
        per: r.per,
        bonus: (r.tot - avgGames) * effAvg(p, K) * p.prob
      };
    }).sort(function (a, b) {
      return b.v - a.v;
    }).slice(0, 100);
  }, [s.players, who, pos, q, st, nW, K]);
  var league = useMemo(function () {
    return s.teams.map(function (t) {
      var r = s.players.filter(function (p) {
        return p.ft === t.id;
      });
      return {
        t: t,
        tot: weeks.reduce(function (a, w) {
          return a + weekProj(r, w, K, 0).total;
        }, 0)
      };
    }).sort(function (a, b) {
      return b.tot - a.tot;
    });
  }, [s.players, weeks, K]);
  var myRank = league.findIndex(function (x) {
    return x.t.id === s.me;
  }) + 1;
  var mine = s.players.filter(function (p) {
    return p.ft === s.me && !p.ir;
  }).map(function (p) {
    return {
      p: p,
      g: (tg[p.t] || {}).tot || 0
    };
  }).sort(function (a, b) {
    return a.g - b.g;
  });
  var weakSched = mine.filter(function (x) {
    return x.g <= avgGames - 1.5;
  });
  var set = function set(k, v) {
    return setS(function (x) {
      return _defineProperty({}, k, v);
    });
  };
  var gCls = function gCls(g, avg) {
    return g >= avg + 1.5 ? "text-green-700 font-semibold" : g <= avg - 1.5 ? "text-red-600" : "";
  };
  var today = todayISO();
  var deadline = "2027-02-26";
  return /*#__PURE__*/React.createElement("div", {
    className: "space-y-4"
  }, /*#__PURE__*/React.createElement(Section, {
    title: "Fantasy playoff planner",
    sub: "".concat(weeks.length ? "".concat(mdL(weeks[0].dates[0]), " \u2013 ").concat(mdL(dates[dates.length - 1])) : "", " \xB7 trade deadline ").concat(mdL(deadline)).concat(today <= deadline ? " (".concat(Math.round((fromIso(deadline) - fromIso(today)) / 864e5), " days away)") : " (passed)")
  }, /*#__PURE__*/React.createElement("div", {
    className: "flex flex-wrap gap-2 items-center"
  }, /*#__PURE__*/React.createElement("label", null, "Playoffs start ", /*#__PURE__*/React.createElement("select", {
    className: inp,
    value: st,
    onChange: function onChange(e) {
      return set("poStart", +e.target.value);
    }
  }, s.weeks.map(function (w, i) {
    return /*#__PURE__*/React.createElement("option", {
      key: i,
      value: i
    }, w.label);
  }))), /*#__PURE__*/React.createElement("label", null, "Weeks ", /*#__PURE__*/React.createElement("select", {
    className: inp,
    value: nW,
    onChange: function onChange(e) {
      return set("poWeeks", +e.target.value);
    }
  }, [1, 2, 3, 4].map(function (n) {
    return /*#__PURE__*/React.createElement("option", {
      key: n,
      value: n
    }, n);
  })))), /*#__PURE__*/React.createElement("div", {
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
  }, league.map(function (x, i) {
    return /*#__PURE__*/React.createElement("div", {
      key: x.t.id,
      className: "flex justify-between py-1 border-t border-slate-100 " + (x.t.id === s.me ? "text-blue-700 font-semibold" : "")
    }, /*#__PURE__*/React.createElement("span", null, i + 1, ". ", x.t.name), /*#__PURE__*/React.createElement("span", null, f1(x.tot)));
  })), /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500 mt-2"
  }, "Lineup-aware totals for all ", nW, " weeks with current rosters and projections.")), /*#__PURE__*/React.createElement(Section, {
    title: "Your players with weak playoff schedules"
  }, weakSched.length ? weakSched.map(function (_ref38) {
    var p = _ref38.p,
      g = _ref38.g;
    return /*#__PURE__*/React.createElement("div", {
      key: p.id,
      className: "flex gap-2 py-1.5 border-t border-slate-100"
    }, /*#__PURE__*/React.createElement("span", {
      className: "font-medium"
    }, p.n), /*#__PURE__*/React.createElement("span", {
      className: "text-xs text-slate-400"
    }, p.p, " \xB7 ", /*#__PURE__*/React.createElement(TeamLogo, {
      t: p.t
    })), /*#__PURE__*/React.createElement("span", {
      className: "ml-auto text-red-600 text-xs"
    }, g, " games (", (g - avgGames).toFixed(1), " vs avg)"));
  }) : /*#__PURE__*/React.createElement("div", {
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
    onChange: function onChange(e) {
      return setPos(e.target.value);
    }
  }, /*#__PURE__*/React.createElement("option", {
    value: "all"
  }, "All positions"), /*#__PURE__*/React.createElement("option", null, "F"), /*#__PURE__*/React.createElement("option", null, "D"), /*#__PURE__*/React.createElement("option", null, "G")), /*#__PURE__*/React.createElement("input", {
    className: inp + " flex-1 min-w-[140px]",
    placeholder: "Search",
    value: q,
    onChange: function onChange(e) {
      return setQ(e.target.value);
    }
  })), /*#__PURE__*/React.createElement("div", {
    className: "overflow-x-auto"
  }, /*#__PURE__*/React.createElement("table", {
    className: "w-full text-sm"
  }, /*#__PURE__*/React.createElement("thead", {
    className: "text-left"
  }, /*#__PURE__*/React.createElement("tr", null, ["Player", "", "Owner"].concat(_toConsumableArray(weeks.map(function (w, i) {
    return "Wk ".concat(st + i + 1);
  })), ["Games", "Light", "Avg", "Playoff pts", "Sched bonus"]).map(function (h, i) {
    return /*#__PURE__*/React.createElement("th", {
      key: i,
      className: "px-2 py-2"
    }, h);
  }))), /*#__PURE__*/React.createElement("tbody", null, rows.map(function (_ref39) {
    var p = _ref39.p,
      v = _ref39.v,
      g = _ref39.g,
      off = _ref39.off,
      per = _ref39.per,
      bonus = _ref39.bonus;
    return /*#__PURE__*/React.createElement("tr", {
      key: p.id,
      className: "border-t border-slate-100 " + (p.ft === s.me ? "bg-blue-50" : "")
    }, /*#__PURE__*/React.createElement("td", {
      className: "px-2 py-2 font-medium whitespace-nowrap"
    }, p.n, p.ir ? /*#__PURE__*/React.createElement("span", {
      className: "text-red-600 text-xs ml-1"
    }, "IR") : ""), /*#__PURE__*/React.createElement("td", {
      className: "px-2 py-2 text-xs text-slate-500 whitespace-nowrap"
    }, p.p, " \xB7 ", /*#__PURE__*/React.createElement(TeamLogo, {
      t: p.t
    })), /*#__PURE__*/React.createElement("td", {
      className: "px-2 py-2 text-xs text-slate-500"
    }, teamName(s, p.ft)), per.map(function (n, i) {
      return /*#__PURE__*/React.createElement("td", {
        key: i,
        className: "px-2 py-2 " + (n >= 4 ? "text-green-700 font-semibold" : n <= 2 ? "text-red-600" : "")
      }, n);
    }), /*#__PURE__*/React.createElement("td", {
      className: "px-2 py-2 " + gCls(g, avgGames)
    }, g), /*#__PURE__*/React.createElement("td", {
      className: "px-2 py-2"
    }, off), /*#__PURE__*/React.createElement("td", {
      className: "px-2 py-2"
    }, f1(effAvg(p, K))), /*#__PURE__*/React.createElement("td", {
      className: "px-2 py-2 font-semibold"
    }, f1(v)), /*#__PURE__*/React.createElement("td", {
      className: "px-2 py-2 " + (bonus >= 0 ? "text-green-700" : "text-red-600")
    }, bonus >= 0 ? "+" : "", f1(bonus)));
  }), rows.length === 0 && /*#__PURE__*/React.createElement("tr", null, /*#__PURE__*/React.createElement("td", {
    className: "px-2 py-3 text-slate-400"
  }, "No players match.")))))), /*#__PURE__*/React.createElement(Section, {
    title: "NHL team schedules in your playoff weeks",
    link: [showTeams ? "Hide" : "Show all 32 teams", function () {
      return setShowTeams(!showTeams);
    }]
  }, /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500 mb-2"
  }, "Best: ", teamRows.slice(0, 5).map(function (r) {
    return "".concat(r.t, " (").concat(r.tot, ")");
  }).join(", "), " \xB7 Worst: ", teamRows.slice(-5).reverse().map(function (r) {
    return "".concat(r.t, " (").concat(r.tot, ")");
  }).join(", ")), showTeams && /*#__PURE__*/React.createElement("div", {
    className: "overflow-x-auto"
  }, /*#__PURE__*/React.createElement("table", {
    className: "w-full text-sm"
  }, /*#__PURE__*/React.createElement("thead", {
    className: "text-left"
  }, /*#__PURE__*/React.createElement("tr", null, ["Team"].concat(_toConsumableArray(weeks.map(function (w, i) {
    return "Wk ".concat(st + i + 1);
  })), ["Total", "Light-night games"]).map(function (h) {
    return /*#__PURE__*/React.createElement("th", {
      key: h,
      className: "px-2 py-2"
    }, h);
  }))), /*#__PURE__*/React.createElement("tbody", null, teamRows.map(function (r) {
    return /*#__PURE__*/React.createElement("tr", {
      key: r.t,
      className: "border-t border-slate-100"
    }, /*#__PURE__*/React.createElement("td", {
      className: "px-2 py-1.5 font-medium whitespace-nowrap"
    }, /*#__PURE__*/React.createElement("span", {
      className: "inline-flex items-center gap-1.5"
    }, /*#__PURE__*/React.createElement(TeamLogo, {
      t: r.t,
      size: 16
    }), r.t)), r.per.map(function (n, i) {
      return /*#__PURE__*/React.createElement("td", {
        key: i,
        className: "px-2 py-1.5 " + (n >= 4 ? "text-green-700 font-semibold" : n <= 2 ? "text-red-600" : "")
      }, n);
    }), /*#__PURE__*/React.createElement("td", {
      className: "px-2 py-1.5 " + gCls(r.tot, avgGames)
    }, r.tot), /*#__PURE__*/React.createElement("td", {
      className: "px-2 py-1.5"
    }, r.off));
  }))))));
}

// ---------- Trade analyzer ----------
var rosRaw = function rosRaw(p, K) {
  if (p.ir && !effBack(p).d) return 0;
  var t = todayISO();
  var v = 0;
  (SCHED[p.t] ? _toConsumableArray(SCHED[p.t]) : []).forEach(function (d) {
    if (d >= t) v += effAvg(p, K, d) * p.prob * avail(p, d);
  });
  return v;
};
var horizonTotal = function horizonTotal(roster, s, n) {
  var t = 0;
  s.weeks.slice(s.wk, s.wk + n).forEach(function (w, i) {
    var dw = deriveWeek(w, s.autoDone);
    t += weekProj(roster, dw, s.blend, i === 0 ? dw.done : 0).total;
  });
  return t;
};
function Matchup(_ref40) {
  var s = _ref40.s,
    setS = _ref40.setS,
    wk = _ref40.wk,
    setWk = _ref40.setWk;
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
  var K = s.blend,
    done = wk.done || 0;
  var pairOpp = oppOf(wk, s.me);
  var myPair = [s.me, pairOpp || s.opp];
  var others = (wk.pairs || []).filter(function (p) {
    return p[0] && p[1] && p[0] !== s.me && p[1] !== s.me;
  });
  var all = [myPair].concat(_toConsumableArray(others));
  var _useState39 = useState(function () {
      var v44 = window.__MATCH_SEL || 0;
      window.__MATCH_SEL = 0;
      return v44;
    }),
    _useState40 = _slicedToArray(_useState39, 2),
    sel = _useState40[0],
    setSel = _useState40[1];
  useEffect(function () {
    window.__matchSel = sel;
    window.__setMatch = setSel;
    window.dispatchEvent(new Event("gm-match"));
  }, [sel]);
  var _useState41 = useState(null),
    _useState42 = _slicedToArray(_useState41, 2),
    day = _useState42[0],
    setDay = _useState42[1];
  var touch = React.useRef(null);
  var _all$Math$min = _slicedToArray(all[Math.min(sel, all.length - 1)], 2),
    a = _all$Math$min[0],
    b = _all$Math$min[1];
  var gen = (window.ESPN_DATA || {}).generated;
  var P = useMemo(function () {
    var o = {};
    [a, b].forEach(function (id) {
      o[id] = {
        r: weekLive(s.players.filter(function (p) {
          return p.ft === id;
        }), wk, K, id, {
          detail: true
        }),
        act: +(wk.act || {})[id] || 0
      };
    });
    return o;
  }, [s.players, wk, K, done, a, b, gen]);
  var A = P[a].r,
    B = P[b].r,
    aA = P[a].act,
    aB = P[b].act;
  var fa = aA + A.total,
    fb = aB + B.total,
    margin = fa - fb;
  var dates = wk.dates || [],
    n = dates.length,
    today = todayISO();
  var first = dates.findIndex(function (x) {
    return x >= today;
  });
  var d = Math.max(0, Math.min(n - 1, day != null ? day : first >= 0 ? first : n - 1));
  var over = n > 0 && done >= n;
  var move = function move(k) {
    return setSel((Math.min(sel, all.length - 1) + k + all.length) % all.length);
  };
  var onStart = function onStart(e) {
    var t = e.touches[0];
    touch.current = [t.clientX, t.clientY];
  };
  var onEnd = function onEnd(e) {
    var t0 = touch.current,
      t = e.changedTouches[0];
    touch.current = null;
    if (!t0 || all.length < 2) return;
    var dx = t.clientX - t0[0],
      dy = t.clientY - t0[1];
    if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy) * 1.5) move(dx < 0 ? 1 : -1);
  };
  var x = A.days[d] || {
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
  var dvOf = function dvOf(i) {
    var p = A.days[i],
      q = B.days[i];
    return p && q ? p.act + p.total - (q.act + q.total) : 0;
  };
  var state = x.locked || y.locked ? x.allDone && y.allDone ? "final" : "live" : dates[d] < today ? "final" : "projected";
  var rows = [];
  ["F", "D", "UTIL", "G"].forEach(function (sl) {
    var L = x.start.filter(function (p) {
        return p.slot === sl;
      }),
      R = y.start.filter(function (p) {
        return p.slot === sl;
      });
    for (var i = 0; i < Math.max(L.length, R.length); i++) rows.push([sl, L[i] || null, R[i] || null]);
  });
  var val = function val(p) {
    return !p ? null : p.st ? p.a == null ? 0 : p.a : p.x;
  };
  var cell = function cell(p, right) {
    if (!p) return /*#__PURE__*/React.createElement("div", {
      className: "text-sm text-slate-500" + (right ? " text-right" : "")
    }, "empty");
    var st = p.p === "G" && !p.st ? mStart(p.gs) : "",
      line = p.st ? statLine(pStat(p, p.dt)) : "";
    return /*#__PURE__*/React.createElement("div", {
      className: "min-w-0 gx-pc",
      style: {
        flexDirection: right ? "row-reverse" : "row"
      }
    }, /*#__PURE__*/React.createElement(TeamLogo, {
      t: p.t,
      size: 30
    }), /*#__PURE__*/React.createElement("div", {
      className: "min-w-0" + (right ? " text-right" : ""),
      style: {
        flex: 1
      }
    }, /*#__PURE__*/React.createElement("div", {
      className: "truncate gx-nm"
    }, /*#__PURE__*/React.createElement("button", {
      type: "button",
      className: "hover:underline text-left",
      onClick: function onClick(e) {
        e.stopPropagation();
        if (window.__NAV) window.__NAV.player(p);
      }
    }, /*#__PURE__*/React.createElement("span", {
      className: "m-hide"
    }, p.n), /*#__PURE__*/React.createElement("span", {
      className: "m-inl"
    }, shortN(p.n)))), /*#__PURE__*/React.createElement("div", {
      className: "text-xs text-slate-500 truncate"
    }, p.st ? /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement(LiveTag, {
      st: p.st,
      t: p.t,
      dt: p.dt
    }), line ? " " + line : "") : /*#__PURE__*/React.createElement(React.Fragment, null, mGame(p), st ? " \xB7 " + st.toLowerCase() : ""))));
  };
  var num = function num(p, q, right) {
    var v = val(p),
      o = val(q);
    if (v == null) return /*#__PURE__*/React.createElement("div", {
      className: "text-slate-500" + (right ? "" : " text-right")
    }, "\u2013");
    var win = o == null || v - o >= 0.05;
    return /*#__PURE__*/React.createElement("div", {
      className: right ? "" : "text-right",
      style: win ? {
        color: "var(--good)",
        fontWeight: 600
      } : null
    }, p.st && p.a == null ? "\u2013" : f1(v));
  };
  var sit = function sit(l, id) {
    return l.bench && l.bench.length ? /*#__PURE__*/React.createElement("div", {
      className: "text-xs text-slate-500",
      style: {
        marginTop: 6
      }
    }, teamName(s, id), " would sit: ", l.bench.map(function (p) {
      return shortN(p.n);
    }).join(", ")) : null;
  };
  var dayTot = x.act + x.total - (y.act + y.total);
  var mine = a === s.me;
  return /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    onTouchStart: onStart,
    onTouchEnd: onEnd,
    style: {
      touchAction: "pan-y"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      alignItems: "center",
      gap: 8
    }
  }, all.length > 1 ? /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: "m-hide gx-arw",
    "aria-label": "Previous matchup",
    onClick: function onClick() {
      return move(-1);
    }
  }, "\u2039") : null, /*#__PURE__*/React.createElement("div", {
    className: "min-w-0",
    style: {
      flex: 1
    }
  }, /*#__PURE__*/React.createElement("div", {
    className: "text-sm font-semibold truncate",
    style: mine ? {
      color: "var(--accent)"
    } : null
  }, /*#__PURE__*/React.createElement(TL, {
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
    className: "text-sm text-slate-500 truncate"
  }, /*#__PURE__*/React.createElement(TL, {
    s: s,
    id: b
  })), /*#__PURE__*/React.createElement("div", {
    className: "gx-num",
    style: {
      fontSize: 28,
      color: "var(--ink2)"
    }
  }, f1(aB))), all.length > 1 ? /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: "m-hide gx-arw",
    "aria-label": "Next matchup",
    onClick: function onClick() {
      return move(1);
    }
  }, "\u203A") : null), all.length > 1 ? /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      justifyContent: "center",
      gap: 6,
      marginTop: 8
    }
  }, all.map(function (pr, i) {
    return /*#__PURE__*/React.createElement("button", {
      key: i,
      type: "button",
      "aria-label": "Matchup " + (i + 1),
      onClick: function onClick() {
        return setSel(i);
      },
      style: {
        width: 6,
        height: 6,
        borderRadius: 99,
        background: i === Math.min(sel, all.length - 1) ? "var(--accent)" : "var(--line2)"
      }
    });
  })) : null, /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500",
    style: {
      display: "flex",
      marginTop: 8
    }
  }, /*#__PURE__*/React.createElement("span", null, (over ? "Final " : "Projected ") + Math.round(fa)), /*#__PURE__*/React.createElement("span", {
    style: {
      margin: "0 auto",
      color: margin >= 0 ? "var(--good)" : "var(--bad)"
    }
  }, mine ? (margin >= 0 ? "Ahead by " : "Behind by ") + f1(Math.abs(margin)) : teamName(s, margin >= 0 ? a : b) + " ahead by " + f1(Math.abs(margin))), /*#__PURE__*/React.createElement("span", null, Math.round(fb)))), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "grid",
      gridTemplateColumns: "repeat(" + Math.max(1, n) + ", minmax(0,1fr))",
      gap: 6,
      marginTop: 14
    }
  }, dates.map(function (dt, i) {
    var dv = dvOf(i),
      flat = Math.abs(dv) < 0.05;
    return /*#__PURE__*/React.createElement("button", {
      key: dt,
      type: "button",
      onClick: function onClick() {
        return setDay(i);
      },
      className: "gx-day" + (i === d ? " on" : "")
    }, /*#__PURE__*/React.createElement("span", {
      className: "block text-xs " + (i === d ? "font-semibold" : "text-slate-500")
    }, dt === today ? "Today" : dayLabel(dt).split(",")[0]), /*#__PURE__*/React.createElement("span", {
      className: "block text-sm",
      style: {
        color: flat ? "var(--faint)" : dv > 0 ? "var(--good)" : "var(--bad)"
      }
    }, flat ? "0" : (dv > 0 ? "+" : "") + Math.round(dv)));
  })), /*#__PURE__*/React.createElement("div", {
    className: "gx-pn",
    style: {
      marginTop: 12
    }
  }, /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      alignItems: "baseline",
      marginBottom: 6
    }
  }, /*#__PURE__*/React.createElement("span", {
    className: "gx-tag"
  }, (dates[d] === today ? "Today" : dates[d] ? dayLabel(dates[d]) : "") + " \xB7 " + state), /*#__PURE__*/React.createElement("span", {
    style: {
      marginLeft: "auto",
      fontVariantNumeric: "tabular-nums"
    }
  }, /*#__PURE__*/React.createElement("span", {
    className: "font-semibold"
  }, f1(x.act + x.total)), " ", /*#__PURE__*/React.createElement("span", {
    className: "text-slate-500"
  }, "to ", f1(y.act + y.total)), /*#__PURE__*/React.createElement("span", {
    style: {
      marginLeft: 8,
      color: dayTot >= 0 ? "var(--good)" : "var(--bad)"
    }
  }, (dayTot >= 0 ? "+" : "") + f1(dayTot)))), rows.length ? rows.map(function (_ref41, i) {
    var _ref42 = _slicedToArray(_ref41, 3),
      sl = _ref42[0],
      p = _ref42[1],
      q = _ref42[2];
    return /*#__PURE__*/React.createElement("div", {
      key: i,
      className: "gx-h2h",
      style: i ? null : {
        borderTop: 0
      }
    }, cell(p, false), num(p, q, false), /*#__PURE__*/React.createElement("div", {
      className: "text-xs text-center",
      style: {
        color: "var(--faint)"
      }
    }, sl === "UTIL" ? "U" : sl), num(q, p, true), cell(q, true));
  }) : /*#__PURE__*/React.createElement("div", {
    className: "text-sm text-slate-500"
  }, "No games for either team on this day."), sit(x, a), sit(y, b)), /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500",
    style: {
      display: "flex",
      marginTop: 10
    }
  }, /*#__PURE__*/React.createElement("span", null, gamesMoves(s, a, wk, A)), /*#__PURE__*/React.createElement("span", {
    style: {
      marginLeft: "auto"
    }
  }, gamesMoves(s, b, wk, B))));
}

// ---------- Add / Drop ----------
var shortTag = function shortTag(p, K) {
  var t = tags(p, K)[0];
  if (!t) return null;
  var x = t.u ? t.t.split(":")[0] : t.t;
  return {
    t: x.length > 20 ? x.slice(0, 19) + "…" : x,
    c: t.c
  };
};
var cntOf = function cntOf(r) {
  var c = {
    F: 0,
    D: 0,
    G: 0
  };
  r.forEach(function (p) {
    if (!p.ir) c[p.p]++;
  });
  return c;
};
function MoveSim(_ref43) {
  var s = _ref43.s,
    setS = _ref43.setS,
    wk = _ref43.wk,
    M = _ref43.M,
    H = _ref43.H,
    hLabel = _ref43.hLabel,
    init = _ref43.init,
    wBase = _ref43.wBase,
    onClose = _ref43.onClose;
  var total = M.total,
    rawPts = M.rawPts,
    gamesIn = M.gamesIn,
    protectedIds = M.protectedIds,
    mins = M.mins,
    lineupAware = M.lineupAware,
    myR = M.myR,
    fas = M.fas,
    K = M.K;
  var left = movesLeft(s, s.me, wk);
  var cap = Math.max(1, left == null ? 3 : left);
  var _useState43 = useState([{
      add: init.add || "",
      drop: init.drop || "",
      sug: init.drop || ""
    }]),
    _useState44 = _slicedToArray(_useState43, 2),
    moves = _useState44[0],
    setMoves = _useState44[1];
  var _useState45 = useState({}),
    _useState46 = _slicedToArray(_useState45, 2),
    qs = _useState46[0],
    setQs = _useState46[1];
  var _useState47 = useState(init.add ? -1 : 0),
    _useState48 = _slicedToArray(_useState47, 2),
    openI = _useState48[0],
    setOpenI = _useState48[1];
  var _useState49 = useState(0),
    _useState50 = _slicedToArray(_useState49, 2),
    focus = _useState50[0],
    setFocus = _useState50[1];
  useEffect(function () {
    var k = function k(e) {
      if (e.key === "Escape") onClose();
    };
    window.addEventListener("keydown", k);
    document.body.style.overflow = "hidden";
    return function () {
      window.removeEventListener("keydown", k);
      document.body.style.overflow = "";
    };
  }, []);
  var byId = function byId(id) {
    return id ? s.players.find(function (p) {
      return p.id === id;
    }) || null : null;
  };
  var rosterBefore = function rosterBefore(i, ms) {
    var r = myR;
    (ms || moves).slice(0, i).forEach(function (m) {
      var a = byId(m.add);
      if (a && r.some(function (x) {
        return x.id === m.drop;
      })) r = r.filter(function (x) {
        return x.id !== m.drop;
      }).concat([{
        ...a,
        ft: s.me
      }]);
    });
    return r;
  };
  var suggestDrop = function suggestDrop(i, f, ms) {
    var r = rosterBefore(i, ms),
      c = cntOf(r);
    var ok = function ok(d) {
      return !d.ir && (d.p === f.p || c[d.p] - 1 >= mins[d.p]);
    };
    var cands = r.filter(function (d) {
      return ok(d) && !protectedIds.has(d.id);
    });
    if (!cands.length) cands = r.filter(ok);
    var b = lineupAware ? total(r) : 0;
    var best = null;
    cands.forEach(function (d) {
      var g = lineupAware ? total(timedMove(r, s.me, [{
        add: f,
        drop: d
      }])) - b : rawPts(f) - rawPts(d, f);
      if (!best || g > best.g) best = {
        d: d,
        g: g
      };
    });
    return best ? best.d.id : "";
  };
  var setAdd = function setAdd(i, id) {
    var f = byId(id);
    setMoves(function (ms) {
      return ms.map(function (m, k) {
        if (k !== i) return m;
        var sug = f ? suggestDrop(i, f, ms) : "";
        return {
          add: id,
          drop: sug,
          sug: sug
        };
      });
    });
    setQs(function (x) {
      return _defineProperty({}, i, "");
    });
    setOpenI(-1);
    setFocus(i);
  };
  var setDrop = function setDrop(i, id) {
    return setMoves(function (ms) {
      return ms.map(function (m, k) {
        return k === i ? {
          ...m,
          drop: id
        } : m;
      });
    });
  };
  var addMove = function addMove() {
    var n = moves.length;
    setMoves(function (ms) {
      return ms.concat([{
        add: "",
        drop: "",
        sug: ""
      }]);
    });
    setOpenI(n);
    setFocus(n);
  };
  var removeMove = function removeMove(i) {
    setMoves(function (ms) {
      return ms.filter(function (_, k) {
        return k !== i;
      });
    });
    setFocus(0);
    setOpenI(-1);
  };
  var matches = function matches(i) {
    var q = nrm(qs[i] || ""),
      used = new Set(moves.filter(function (_, k) {
        return k !== i;
      }).map(function (m) {
        return m.add;
      }));
    if (!q) return M.res.filter(function (r) {
      return !used.has(r.f.id);
    }).slice(0, 6).map(function (r) {
      return r.f;
    });
    return fas.filter(function (p) {
      return p.prob > 0 && !used.has(p.id) && nrm(p.n).includes(q);
    }).sort(function (a, b) {
      return effAvg(b, K) - effAvg(a, K);
    }).slice(0, 8);
  };
  var key = JSON.stringify(moves.map(function (m) {
    return [m.add, m.drop];
  }));
  var R = useMemo(function () {
    var list = moves.map(function (m, i) {
      var a = byId(m.add),
        r = rosterBefore(i);
      var d = r.find(function (x) {
        return x.id === m.drop;
      }) || null;
      return a && d ? {
        a: a,
        d: d
      } : null;
    });
    var ok = list.filter(Boolean);
    if (!ok.length) return {
      list: list,
      ok: ok
    };
    var after = rosterBefore(moves.length);
    var timed = timedMove(myR, s.me, ok.map(function (x) {
      return {
        add: x.a,
        drop: x.d
      };
    }));
    var gain = lineupAware ? total(timed) - total(myR) : ok.reduce(function (t, x) {
      return t + rawPts(x.a) - rawPts(x.d, x.a);
    }, 0);
    var c = cntOf(after);
    return {
      list: list,
      ok: ok,
      after: after,
      gain: gain,
      c: c,
      win: winChance(s, timed),
      short: ["F", "D", "G"].filter(function (k) {
        return c[k] < mins[k];
      })
    };
  }, [key]);
  var addF = byId((moves[focus] || {}).add);
  var alts = useMemo(function () {
    return addF ? computeMoves(s, {
      H: H,
      pos: addF.p,
      pool: 40
    }).res.filter(function (r) {
      return r.f.id !== addF.id && !moves.some(function (m) {
        return m.add === r.f.id;
      });
    }).slice(0, 3) : [];
  }, [addF ? addF.id : "", H]);
  var apply = function apply() {
    var drops = new Set(R.ok.map(function (x) {
        return x.d.id;
      })),
      adds = new Set(R.ok.map(function (x) {
        return x.a.id;
      }));
    setS(function (st) {
      return {
        ...st,
        players: st.players.map(function (p) {
          return drops.has(p.id) ? {
            ...p,
            ft: "fa",
            ir: false
          } : adds.has(p.id) ? {
            ...p,
            ft: st.me
          } : p;
        })
      };
    });
    onClose();
  };
  var before = cntOf(myR);
  var posName = {
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
    onClick: function onClick(e) {
      return e.stopPropagation();
    }
  }, /*#__PURE__*/React.createElement("div", {
    className: "flex items-start gap-3 mb-3"
  }, /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    className: "font-semibold text-base"
  }, "Simulate a move"), /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500"
  }, "Points: ", hLabel, " \xB7 win chance: this week", left != null ? " \xB7 ".concat(left, " move").concat(left === 1 ? "" : "s", " left this week") : "")), /*#__PURE__*/React.createElement("button", {
    className: "ml-auto text-2xl leading-none text-slate-500",
    "aria-label": "Close",
    onClick: onClose
  }, "\xD7")), moves.map(function (m, i) {
    var a = byId(m.add),
      r = rosterBefore(i),
      it = R.list[i];
    var drops = r.filter(function (p) {
      return !p.ir;
    }).sort(function (x, y) {
      return effAvg(x, K) - effAvg(y, K);
    });
    var sd = it ? effAvg(it.a, K) - effAvg(it.d, K) : 0;
    var ml = openI === i ? matches(i) : [];
    return /*#__PURE__*/React.createElement("div", {
      key: i,
      className: "ms-move",
      onClick: function onClick() {
        return setFocus(i);
      }
    }, moves.length > 1 ? /*#__PURE__*/React.createElement("div", {
      className: "flex items-center mb-2"
    }, /*#__PURE__*/React.createElement("span", {
      className: "text-xs uppercase tracking-wide text-slate-500"
    }, "Move ", i + 1), /*#__PURE__*/React.createElement("button", {
      className: "ml-auto text-xs text-slate-500",
      onClick: function onClick(e) {
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
    }, /*#__PURE__*/React.createElement(TeamLogo, {
      t: a.t,
      size: 26
    }), /*#__PURE__*/React.createElement("div", {
      className: "min-w-0 flex-1"
    }, /*#__PURE__*/React.createElement("div", {
      className: "truncate font-medium"
    }, a.n), /*#__PURE__*/React.createElement("div", {
      className: "text-xs text-slate-500"
    }, a.p, " \xB7 ", gamesIn(a), " gms \xB7 ", f1(effAvg(a, K)), "/g")), /*#__PURE__*/React.createElement("button", {
      className: "text-xs text-blue-600",
      onClick: function onClick() {
        return setOpenI(i);
      }
    }, "Change")) : /*#__PURE__*/React.createElement("div", {
      className: "relative"
    }, /*#__PURE__*/React.createElement("input", {
      className: inp + " w-full",
      autoFocus: openI === i,
      placeholder: "Type a free agent's name",
      value: qs[i] || "",
      onChange: function onChange(e) {
        setQs(_defineProperty({}, i, e.target.value));
        setOpenI(i);
      },
      onFocus: function onFocus() {
        return setOpenI(i);
      },
      onBlur: function onBlur() {
        return setTimeout(function () {
          return setOpenI(function (x) {
            return x === i ? -1 : x;
          });
        }, 150);
      }
    }), openI === i ? /*#__PURE__*/React.createElement("div", {
      className: "ms-list"
    }, !(qs[i] || "").trim() ? /*#__PURE__*/React.createElement("div", {
      className: "text-xs text-slate-500 px-2 pt-1 pb-1"
    }, "Top pickups") : null, ml.map(function (p) {
      return /*#__PURE__*/React.createElement("button", {
        key: p.id,
        type: "button",
        className: "ms-opt",
        onMouseDown: function onMouseDown(e) {
          return e.preventDefault();
        },
        onClick: function onClick() {
          return setAdd(i, p.id);
        }
      }, /*#__PURE__*/React.createElement(TeamLogo, {
        t: p.t,
        size: 22
      }), /*#__PURE__*/React.createElement("span", {
        className: "truncate flex-1 text-left"
      }, p.n, " ", /*#__PURE__*/React.createElement("span", {
        className: "text-xs text-slate-500"
      }, p.p)), /*#__PURE__*/React.createElement("span", {
        className: "text-xs text-slate-500 whitespace-nowrap"
      }, gamesIn(p), " gms \xB7 ", f1(effAvg(p, K))));
    }), ml.length === 0 ? /*#__PURE__*/React.createElement("div", {
      className: "text-sm text-slate-400 px-2 py-2"
    }, "No free agent matches.") : null, a ? /*#__PURE__*/React.createElement("button", {
      type: "button",
      className: "text-xs text-slate-500 px-2 py-1",
      onMouseDown: function onMouseDown(e) {
        return e.preventDefault();
      },
      onClick: function onClick() {
        return setOpenI(-1);
      }
    }, "Keep ", a.n) : null) : null)), /*#__PURE__*/React.createElement("div", {
      className: "min-w-0"
    }, /*#__PURE__*/React.createElement("div", {
      className: "text-xs text-slate-500 mb-1"
    }, "Drop", m.drop && m.drop === m.sug ? " · suggested" : ""), /*#__PURE__*/React.createElement("select", {
      className: inp + " w-full",
      value: m.drop,
      onChange: function onChange(e) {
        return setDrop(i, e.target.value);
      }
    }, /*#__PURE__*/React.createElement("option", {
      value: ""
    }, "Choose who to drop"), drops.map(function (p) {
      return /*#__PURE__*/React.createElement("option", {
        key: p.id,
        value: p.id
      }, p.n, " (", p.p, ") \xB7 ", f1(effAvg(p, K)), "/g", protectedIds.has(p.id) ? " · protected" : "");
    })))), it ? /*#__PURE__*/React.createElement("div", {
      className: "text-xs mt-2 " + (sd >= 0 ? "text-green-700" : "text-amber-600")
    }, sd >= 0 ? "Keeper: ".concat(f1(sd), "/game better than ").concat(it.d.n, " long-term") : "Stream only: ".concat(f1(-sd), "/game worse than ").concat(it.d.n, " long-term"), protectedIds.has(it.d.id) ? " \xB7 ".concat(it.d.n, " is protected") : "") : a && m.drop && !r.some(function (x) {
      return x.id === m.drop;
    }) ? /*#__PURE__*/React.createElement("div", {
      className: "text-xs mt-2 text-red-600"
    }, "That player is already dropped in an earlier move. Choose another drop.") : null);
  }), addF && alts.length ? /*#__PURE__*/React.createElement("div", {
    className: "mt-3"
  }, /*#__PURE__*/React.createElement("div", {
    className: "text-xs uppercase tracking-wide text-slate-500 mb-1"
  }, "Other ", posName[addF.p], " to consider"), alts.map(function (r) {
    return /*#__PURE__*/React.createElement("div", {
      key: r.f.id,
      className: "flex items-center gap-2.5 py-2 border-t border-slate-100"
    }, /*#__PURE__*/React.createElement(TeamLogo, {
      t: r.f.t,
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
      onClick: function onClick() {
        return setAdd(focus, r.f.id);
      }
    }, "Use"));
  })) : null, moves.length < cap ? /*#__PURE__*/React.createElement("button", {
    className: "text-sm text-blue-600 mt-3",
    onClick: addMove
  }, "+ Add another move") : /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500 mt-3"
  }, left === 0 ? "No moves left this week on ESPN, so this is only a what-if." : "That's all ".concat(cap, " of your moves left this week.")), /*#__PURE__*/React.createElement("div", {
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
  }, "was F ", before.F, " \xB7 D ", before.D, " \xB7 G ", before.G))), R.short.length ? /*#__PURE__*/React.createElement("div", {
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
function Players(_ref45) {
  var s = _ref45.s,
    wk = _ref45.wk;
  // players v10: no Signals column, phone list (news_logos.py)
  var K = s.blend;
  var _useState51 = useState("all"),
    _useState52 = _slicedToArray(_useState51, 2),
    ft = _useState52[0],
    setFt = _useState52[1];
  var _useState53 = useState("all"),
    _useState54 = _slicedToArray(_useState53, 2),
    pos = _useState54[0],
    setPos = _useState54[1];
  var _useState55 = useState(""),
    _useState56 = _slicedToArray(_useState55, 2),
    q = _useState56[0],
    setQ = _useState56[1];
  var _useState57 = useState("week"),
    _useState58 = _slicedToArray(_useState57, 2),
    sort = _useState58[0],
    setSort = _useState58[1];
  var rows = s.players.filter(function (p) {
    return (ft === "all" || p.ft === ft) && (pos === "all" || p.p === pos) && p.n.toLowerCase().includes(q.toLowerCase());
  }).map(function (p) {
    var g = (wk.games[p.t] || []).filter(function (d) {
      return !p.ir && avail(p, wk.dates ? wk.dates[d] : null);
    }).length;
    var r = sigOf(p).rec;
    return {
      ...p,
      g: g,
      ea: effAvg(p, K),
      wkp: g * effAvg(p, K) * p.prob,
      rp: r ? r.ppg : null,
      rg: r ? r.gp : 0
    };
  }).sort(function (a, b) {
    return sort === "week" ? b.wkp - a.wkp : sort === "avg" ? b.ea - a.ea : sort === "hot" ? (b.rp || 0) - (a.rp || 0) : b.tot - a.tot;
  }).slice(0, 300);
  var stTag = function stTag(p) {
    return p.ir ? "IR" : p.status && p.status !== "ACTIVE" ? M_ST[p.status] || p.status.replace(/_/g, " ") : "";
  };
  return /*#__PURE__*/React.createElement("div", {
    className: "space-y-3"
  }, /*#__PURE__*/React.createElement("div", {
    className: "flex flex-wrap gap-2"
  }, /*#__PURE__*/React.createElement("input", {
    className: inp + " flex-1 min-w-[160px]",
    placeholder: "Search player",
    value: q,
    onChange: function onChange(e) {
      return setQ(e.target.value);
    }
  }), /*#__PURE__*/React.createElement("select", {
    className: inp,
    value: ft,
    onChange: function onChange(e) {
      return setFt(e.target.value);
    }
  }, /*#__PURE__*/React.createElement("option", {
    value: "all"
  }, "All teams"), /*#__PURE__*/React.createElement("option", {
    value: "fa"
  }, "Free agents"), s.teams.map(function (t) {
    return /*#__PURE__*/React.createElement("option", {
      key: t.id,
      value: t.id
    }, t.name);
  })), /*#__PURE__*/React.createElement("select", {
    className: inp,
    value: pos,
    onChange: function onChange(e) {
      return setPos(e.target.value);
    }
  }, /*#__PURE__*/React.createElement("option", {
    value: "all"
  }, "All positions"), /*#__PURE__*/React.createElement("option", null, "F"), /*#__PURE__*/React.createElement("option", null, "D"), /*#__PURE__*/React.createElement("option", null, "G")), /*#__PURE__*/React.createElement("select", {
    className: inp,
    value: sort,
    onChange: function onChange(e) {
      return setSort(e.target.value);
    }
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
  }, /*#__PURE__*/React.createElement("tr", null, ["Player", "", "Team", "Gms", "Avg", "Last 14d", "Season", "Week"].map(function (h, i) {
    return /*#__PURE__*/React.createElement("th", {
      key: i,
      className: "px-3 py-2"
    }, h);
  }))), /*#__PURE__*/React.createElement("tbody", null, rows.map(function (p) {
    return /*#__PURE__*/React.createElement("tr", {
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
    }, p.p, " \xB7 ", /*#__PURE__*/React.createElement(TeamLogo, {
      t: p.t
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
    }, p.rp !== null ? "".concat(f1(p.rp), " (").concat(p.rg, ")") : "–"), /*#__PURE__*/React.createElement("td", {
      className: "px-3 py-2"
    }, p.gp ? "".concat(f1(p.tot), " (").concat(p.gp, ")") : "–"), /*#__PURE__*/React.createElement("td", {
      className: "px-3 py-2 font-semibold"
    }, f1(p.wkp)));
  }))), /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500 p-3"
  }, "Up to 300 shown \u2014 use the filters to narrow down.")), /*#__PURE__*/React.createElement("div", {
    className: "m-only bg-white rounded-xl border border-slate-200 px-3"
  }, /*#__PURE__*/React.createElement("div", {
    className: "m-ghead"
  }, /*#__PURE__*/React.createElement("span", null, "Player"), /*#__PURE__*/React.createElement("span", null, "Gms"), /*#__PURE__*/React.createElement("span", null, "Avg"), /*#__PURE__*/React.createElement("span", null, "Week")), rows.slice(0, 100).map(function (p) {
    var tg = stTag(p);
    return /*#__PURE__*/React.createElement("div", {
      key: p.id,
      className: "m-rrow",
      role: "button",
      onClick: function onClick() {
        return window.__NAV && window.__NAV.player(p);
      }
    }, /*#__PURE__*/React.createElement(TeamLogo, {
      t: p.t,
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
function Bulk(_ref46) {
  var s = _ref46.s,
    setS = _ref46.setS;
  var _useState59 = useState("team"),
    _useState60 = _slicedToArray(_useState59, 2),
    mode = _useState60[0],
    setMode = _useState60[1];
  var _useState61 = useState(""),
    _useState62 = _slicedToArray(_useState61, 2),
    txt = _useState62[0],
    setTxt = _useState62[1];
  var _useState63 = useState(""),
    _useState64 = _slicedToArray(_useState63, 2),
    msg = _useState64[0],
    setMsg = _useState64[1];
  var help = {
    add: "Name | NHL | Pos | ProjAvg | Play% | Fantasy team (or FA)",
    avg: "Name | ProjAvg",
    season: "Name | GP | Season total pts",
    play: "Name | Play% (goalies: start %)   e.g.  Kevin Lankinen | 85",
    team: "Name | Fantasy team (or FA)   e.g.  Colton Parayko | FA"
  };
  var run = function run() {
    var lines = txt.split("\n").map(function (l) {
      return l.trim();
    }).filter(Boolean);
    var players = _toConsumableArray(s.players);
    var upd = 0,
      add = 0;
    var miss = [];
    var find = function find(n) {
      return players.findIndex(function (p) {
        return p.n.toLowerCase() === n.toLowerCase();
      });
    };
    var teamId = function teamId(x) {
      var v = (x || "").trim().toLowerCase();
      if (!v || v === "fa" || v === "free agent") return "fa";
      var t = s.teams.find(function (t) {
        return t.name.toLowerCase() === v || t.id === v;
      });
      return t ? t.id : null;
    };
    lines.forEach(function (l, k) {
      var f = l.split(/\t|\|/).map(function (x) {
        return x.trim();
      });
      if (f.length < 2) {
        miss.push(l);
        return;
      }
      var i = find(f[0]);
      if (mode === "add") {
        var tid = teamId(f[5]);
        var pos = (f[2] || "F").toUpperCase();
        var nhl = (f[1] || "").toUpperCase();
        if (tid === null || !NHL.includes(nhl) || !["F", "D", "G"].includes(pos)) {
          miss.push(l);
          return;
        }
        var rec = {
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
        var _tid = teamId(f[1]);
        if (_tid === null) {
          miss.push(l);
          return;
        }
        players[i] = {
          ...players[i],
          ft: _tid,
          ir: false
        };
      }
      upd++;
    });
    setS({
      ...s,
      players: players
    });
    setMsg("Updated ".concat(upd, ", added ").concat(add, ".") + (miss.length ? " Not matched (".concat(miss.length, "): ").concat(miss.slice(0, 8).join("; ")) : ""));
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
    onChange: function onChange(e) {
      return setMode(e.target.value);
    }
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
    onChange: function onChange(e) {
      return setTxt(e.target.value);
    }
  }), msg && /*#__PURE__*/React.createElement("div", {
    className: "text-sm mt-2"
  }, msg), /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500 mt-2"
  }, "The next ESPN sync replaces manual roster moves with ESPN's real rosters."));
}
function InjuryPanel(_ref47) {
  var s = _ref47.s,
    setS = _ref47.setS;
  var _useState65 = useState(false),
    _useState66 = _slicedToArray(_useState65, 2),
    showFA = _useState66[0],
    setShowFA = _useState66[1];
  var list = s.players.filter(function (p) {
    return p.status && p.status !== "ACTIVE" || p.back || autoInj(p);
  }).filter(function (p) {
    return showFA || p.ft !== "fa";
  }).sort(function (a, b) {
    return (a.ft === s.me ? 0 : 1) - (b.ft === s.me ? 0 : 1) || teamName(s, a.ft).localeCompare(teamName(s, b.ft));
  });
  var upd = function upd(id, back) {
    return setS(function (st) {
      return {
        ...st,
        players: st.players.map(function (p) {
          return p.id === id ? {
            ...p,
            back: back
          } : p;
        })
      };
    });
  };
  var today = todayISO();
  return /*#__PURE__*/React.createElement(Section, {
    title: "Injuries & return dates",
    sub: "Filled automatically from ESPN's injury report. Pick a date to override; Clear to go back to automatic.",
    link: [showFA ? "Hide free agents" : "Include free agents", function () {
      return setShowFA(!showFA);
    }]
  }, /*#__PURE__*/React.createElement("div", {
    className: "overflow-x-auto"
  }, /*#__PURE__*/React.createElement("table", {
    className: "w-full text-sm"
  }, /*#__PURE__*/React.createElement("thead", {
    className: "text-left"
  }, /*#__PURE__*/React.createElement("tr", null, ["Player", "Team", "Status", "Back on", ""].map(function (h) {
    return /*#__PURE__*/React.createElement("th", {
      key: h,
      className: "px-2 py-2"
    }, h);
  }))), /*#__PURE__*/React.createElement("tbody", null, list.map(function (p) {
    var eb = effBack(p),
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
    }, p.p, " \xB7 ", /*#__PURE__*/React.createElement(TeamLogo, {
      t: p.t
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
      onChange: function onChange(e) {
        return upd(p.id, e.target.value);
      }
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
      onClick: function onClick() {
        return upd(p.id, "");
      }
    }, "Clear") : null));
  }), list.length === 0 && /*#__PURE__*/React.createElement("tr", null, /*#__PURE__*/React.createElement("td", {
    className: "px-2 py-3 text-slate-400"
  }, "No injured players."))))));
}
function RosterTable(_ref48) {
  var s = _ref48.s,
    setS = _ref48.setS,
    wk = _ref48.wk,
    team = _ref48.team;
  var _useState67 = useState(""),
    _useState68 = _slicedToArray(_useState67, 2),
    q = _useState68[0],
    setQ = _useState68[1];
  var upd = function upd(id, patch) {
    return setS(function (st) {
      return {
        ...st,
        players: st.players.map(function (p) {
          return p.id === id ? {
            ...p,
            ...patch
          } : p;
        })
      };
    });
  };
  var order = {
    F: 0,
    D: 1,
    G: 2
  };
  var all = s.players.filter(function (p) {
    return p.ft === team;
  });
  var list = all.filter(function (p) {
    return p.n.toLowerCase().includes(q.toLowerCase());
  }).sort(function (a, b) {
    return order[a.p] - order[b.p] || b.avg - a.avg;
  }).slice(0, team === "fa" ? 100 : 999);
  var cnt = {
    F: 0,
    D: 0,
    G: 0
  };
  all.forEach(function (p) {
    if (!p.ir) cnt[p.p]++;
  });
  var active = all.filter(function (p) {
    return !p.ir;
  }).length;
  var mins = {
    F: s.minF ?? 10,
    D: s.minD ?? 5,
    G: s.minGo ?? 2
  };
  var low = team === s.me && (cnt.F < mins.F || cnt.D < mins.D || cnt.G < mins.G);
  return /*#__PURE__*/React.createElement("div", {
    className: "bg-white rounded-xl border border-slate-200 mb-4"
  }, /*#__PURE__*/React.createElement("div", {
    className: "flex flex-wrap items-center gap-3 p-3 border-b border-slate-200"
  }, /*#__PURE__*/React.createElement("div", {
    className: "font-semibold text-base"
  }, teamName(s, team) || "Free agents"), team !== "fa" && /*#__PURE__*/React.createElement("span", {
    className: "text-xs " + (low ? "text-red-600 font-semibold" : "text-slate-500")
  }, active, "/22 active \xB7 F ", cnt.F, " \xB7 D ", cnt.D, " \xB7 G ", cnt.G, all.length - active ? " \xB7 ".concat(all.length - active, " IR") : "", low ? " — below minimums" : ""), /*#__PURE__*/React.createElement("input", {
    className: inp + " ml-auto",
    placeholder: "Search",
    value: q,
    onChange: function onChange(e) {
      return setQ(e.target.value);
    }
  })), /*#__PURE__*/React.createElement("div", {
    className: "overflow-x-auto"
  }, /*#__PURE__*/React.createElement("table", {
    className: "w-full text-sm"
  }, /*#__PURE__*/React.createElement("thead", {
    className: "text-left"
  }, /*#__PURE__*/React.createElement("tr", null, ["Player", "", "Proj avg", "Play %", "IR", "Back on", "Gms", "Fantasy team"].map(function (h, i) {
    return /*#__PURE__*/React.createElement("th", {
      key: i,
      className: "px-2 py-2"
    }, h);
  }))), /*#__PURE__*/React.createElement("tbody", null, list.map(function (p) {
    return /*#__PURE__*/React.createElement("tr", {
      key: p.id,
      className: "border-t border-slate-100"
    }, /*#__PURE__*/React.createElement("td", {
      className: "px-2 py-1.5 font-medium whitespace-nowrap"
    }, p.n, p.status && p.status !== "ACTIVE" ? /*#__PURE__*/React.createElement("span", {
      className: "text-red-600 text-xs ml-1"
    }, p.status.replace(/_/g, " ")) : ""), /*#__PURE__*/React.createElement("td", {
      className: "px-2 py-1.5 text-xs text-slate-500 whitespace-nowrap"
    }, p.p, " \xB7 ", /*#__PURE__*/React.createElement(TeamLogo, {
      t: p.t
    })), /*#__PURE__*/React.createElement("td", {
      className: "px-2 py-1.5"
    }, /*#__PURE__*/React.createElement("input", {
      type: "number",
      step: "0.1",
      className: inp + " w-20",
      value: p.avg,
      onChange: function onChange(e) {
        return upd(p.id, {
          avg: parseFloat(e.target.value) || 0,
          est: false
        });
      }
    })), /*#__PURE__*/React.createElement("td", {
      className: "px-2 py-1.5"
    }, /*#__PURE__*/React.createElement("input", {
      type: "number",
      min: "0",
      max: "100",
      className: inp + " w-16",
      value: Math.round(p.prob * 100),
      onChange: function onChange(e) {
        return upd(p.id, {
          prob: Math.max(0, Math.min(100, parseFloat(e.target.value) || 0)) / 100
        });
      }
    })), /*#__PURE__*/React.createElement("td", {
      className: "px-2 py-1.5"
    }, /*#__PURE__*/React.createElement("input", {
      type: "checkbox",
      checked: !!p.ir,
      onChange: function onChange(e) {
        return upd(p.id, {
          ir: e.target.checked
        });
      }
    })), /*#__PURE__*/React.createElement("td", {
      className: "px-2 py-1.5"
    }, /*#__PURE__*/React.createElement("input", {
      type: "date",
      className: inp,
      value: p.back || "",
      onChange: function onChange(e) {
        return upd(p.id, {
          back: e.target.value
        });
      }
    })), /*#__PURE__*/React.createElement("td", {
      className: "px-2 py-1.5"
    }, gms(wk, p.t)), /*#__PURE__*/React.createElement("td", {
      className: "px-2 py-1.5"
    }, /*#__PURE__*/React.createElement("select", {
      className: inp,
      value: p.ft,
      onChange: function onChange(e) {
        return upd(p.id, {
          ft: e.target.value,
          ir: false
        });
      }
    }, s.teams.map(function (t) {
      return /*#__PURE__*/React.createElement("option", {
        key: t.id,
        value: t.id
      }, t.name);
    }), /*#__PURE__*/React.createElement("option", {
      value: "fa"
    }, "Free agent"))));
  })))), team === "fa" && all.length > 100 && /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500 p-3"
  }, "Showing 100 of ", all.length, " \u2014 use search."));
}
function AddOne(_ref49) {
  var s = _ref49.s,
    setS = _ref49.setS;
  var _useState69 = useState({
      n: "",
      t: "ANA",
      p: "F",
      avg: 6,
      prob: 100,
      ft: s.me
    }),
    _useState70 = _slicedToArray(_useState69, 2),
    nw = _useState70[0],
    setNw = _useState70[1];
  var addP = function addP() {
    if (!nw.n.trim()) return;
    setS(function (st) {
      return {
        ...st,
        players: [].concat(_toConsumableArray(st.players), [{
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
        }])
      };
    });
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
    onChange: function onChange(e) {
      return setNw({
        ...nw,
        n: e.target.value
      });
    }
  }), /*#__PURE__*/React.createElement("select", {
    className: inp,
    value: nw.t,
    onChange: function onChange(e) {
      return setNw({
        ...nw,
        t: e.target.value
      });
    }
  }, NHL.map(function (t) {
    return /*#__PURE__*/React.createElement("option", {
      key: t
    }, t);
  })), /*#__PURE__*/React.createElement("select", {
    className: inp,
    value: nw.p,
    onChange: function onChange(e) {
      return setNw({
        ...nw,
        p: e.target.value
      });
    }
  }, /*#__PURE__*/React.createElement("option", null, "F"), /*#__PURE__*/React.createElement("option", null, "D"), /*#__PURE__*/React.createElement("option", null, "G")), /*#__PURE__*/React.createElement("label", null, "Avg ", /*#__PURE__*/React.createElement("input", {
    type: "number",
    step: "0.1",
    className: inp + " w-20",
    value: nw.avg,
    onChange: function onChange(e) {
      return setNw({
        ...nw,
        avg: e.target.value
      });
    }
  })), /*#__PURE__*/React.createElement("label", null, "Play % ", /*#__PURE__*/React.createElement("input", {
    type: "number",
    className: inp + " w-16",
    value: nw.prob,
    onChange: function onChange(e) {
      return setNw({
        ...nw,
        prob: e.target.value
      });
    }
  })), /*#__PURE__*/React.createElement("select", {
    className: inp,
    value: nw.ft,
    onChange: function onChange(e) {
      return setNw({
        ...nw,
        ft: e.target.value
      });
    }
  }, s.teams.map(function (t) {
    return /*#__PURE__*/React.createElement("option", {
      key: t.id,
      value: t.id
    }, t.name);
  }), /*#__PURE__*/React.createElement("option", {
    value: "fa"
  }, "Free agent")), /*#__PURE__*/React.createElement("button", {
    className: "bg-blue-600 rounded-lg px-3 py-1.5",
    onClick: addP
  }, "Add")));
}
function Schedule(_ref50) {
  var s = _ref50.s,
    setS = _ref50.setS,
    wk = _ref50.wk,
    setWk = _ref50.setWk;
  var _useState71 = useState(""),
    _useState72 = _slicedToArray(_useState71, 2),
    start = _useState72[0],
    setStart = _useState72[1];
  var _useState73 = useState(7),
    _useState74 = _slicedToArray(_useState73, 2),
    len = _useState74[0],
    setLen = _useState74[1];
  useEffect(function () {
    setStart(wk.dates && wk.dates[0] || "");
    setLen(wk.dates && wk.dates.length || 7);
  }, [s.wk]);
  var relabel = function relabel(ws) {
    return ws.map(function (w, i) {
      return w.dates && w.dates.length ? {
        ...w,
        label: lab(i, w.dates)
      } : w;
    });
  };
  var applyDates = function applyDates() {
    if (!start) return;
    var dates = _toConsumableArray(Array(Math.max(1, +len || 1))).map(function (_, k) {
      return addDays(start, k);
    });
    setS(function (st) {
      return {
        ...st,
        weeks: relabel(st.weeks.map(function (w, i) {
          return i === st.wk ? {
            ...w,
            dates: dates
          } : w;
        }))
      };
    });
  };
  var mergeNext = function mergeNext() {
    if (s.wk >= s.weeks.length - 1 || !confirm("Merge this week with the next one?")) return;
    setS(function (st) {
      var ws = _toConsumableArray(st.weeks);
      var a = ws[st.wk],
        b = ws[st.wk + 1];
      ws[st.wk] = {
        ...a,
        dates: [].concat(_toConsumableArray(a.dates || []), _toConsumableArray(b.dates || []))
      };
      ws.splice(st.wk + 1, 1);
      return {
        ...st,
        weeks: relabel(ws)
      };
    });
  };
  var resetWeeks = function resetWeeks() {
    if (confirm("Reset all weeks to Monday–Sunday?")) setS(function (st) {
      return {
        ...st,
        weeks: defaultWeeks(),
        wk: 0
      };
    });
  };
  var perDay = wk.days.map(function (_, d) {
    return NHL.filter(function (t) {
      return (wk.games[t] || []).includes(d);
    }).length / 2;
  });
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
    onChange: function onChange(e) {
      return setStart(e.target.value);
    }
  }), /*#__PURE__*/React.createElement("label", null, "Days ", /*#__PURE__*/React.createElement("input", {
    type: "number",
    min: "1",
    max: "21",
    className: inp + " w-16",
    value: len,
    onChange: function onChange(e) {
      return setLen(e.target.value);
    }
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
  }, "Team"), wk.days.map(function (d, i) {
    return /*#__PURE__*/React.createElement("th", {
      key: i,
      className: "px-2 py-2"
    }, d);
  }), /*#__PURE__*/React.createElement("th", {
    className: "px-2 py-2"
  }, "Gms"))), /*#__PURE__*/React.createElement("tbody", null, NHL.map(function (t) {
    return /*#__PURE__*/React.createElement("tr", {
      key: t,
      className: "border-t border-slate-100"
    }, /*#__PURE__*/React.createElement("td", {
      className: "px-2 py-1 font-medium whitespace-nowrap"
    }, /*#__PURE__*/React.createElement("span", {
      className: "inline-flex items-center gap-1.5"
    }, /*#__PURE__*/React.createElement(TeamLogo, {
      t: t,
      size: 16
    }), t)), wk.days.map(function (_, d) {
      var on = (wk.games[t] || []).includes(d);
      var b2 = on && wk.dates && SCHED[t] && SCHED[t].has(addDays(wk.dates[d], -1));
      return /*#__PURE__*/React.createElement("td", {
        key: d,
        className: "px-1 py-1 text-center"
      }, /*#__PURE__*/React.createElement("span", {
        title: b2 ? "2nd night of a back-to-back — backup goalie likely" : "",
        className: "inline-block w-7 h-4 rounded " + (b2 ? "bg-amber-500" : on ? "bg-blue-600" : "bg-slate-200")
      }));
    }), /*#__PURE__*/React.createElement("td", {
      className: "px-2 py-1 text-center font-semibold " + (gms(wk, t) >= 4 ? "text-green-700" : gms(wk, t) <= 1 ? "text-red-600" : "")
    }, gms(wk, t)));
  }), /*#__PURE__*/React.createElement("tr", {
    className: "border-t-2 border-slate-300"
  }, /*#__PURE__*/React.createElement("td", {
    className: "px-2 py-2 font-semibold"
  }, "Games/day"), perDay.map(function (n, i) {
    return /*#__PURE__*/React.createElement("td", {
      key: i,
      className: "text-center font-semibold " + (n <= 4 ? "text-green-700" : "")
    }, n);
  }), /*#__PURE__*/React.createElement("td", null))))));
}
function Settings(_ref51) {
  var s = _ref51.s,
    setS = _ref51.setS;
  var E = window.ESPN_DATA;
  var _useState75 = useState(""),
    _useState76 = _slicedToArray(_useState75, 2),
    io = _useState76[0],
    setIo = _useState76[1];
  var _useState77 = useState(""),
    _useState78 = _slicedToArray(_useState77, 2),
    msg = _useState78[0],
    setMsg = _useState78[1];
  var Sg = E && E.signals;
  var download = function download() {
    var blob = new Blob([JSON.stringify(s)], {
      type: "application/json"
    });
    var a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = "fantasy-gm-backup-".concat(todayISO(), ".json");
    a.click();
    setMsg("Backup file downloaded — keep it somewhere safe.");
  };
  var upload = function upload(e) {
    var f = e.target.files && e.target.files[0];
    if (!f) return;
    var r = new FileReader();
    r.onload = function () {
      try {
        var v = JSON.parse(r.result);
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
  var row = function row(ok, label, detail) {
    return /*#__PURE__*/React.createElement("div", {
      className: "flex gap-2 py-1 border-t border-slate-100"
    }, /*#__PURE__*/React.createElement("span", null, /*#__PURE__*/React.createElement("span", {
      className: ok ? "text-green-700" : "text-slate-400"
    }, "\u25CF")), /*#__PURE__*/React.createElement("span", {
      className: "font-medium"
    }, label), /*#__PURE__*/React.createElement("span", {
      className: "text-slate-500 text-xs ml-auto text-right"
    }, detail));
  };
  return /*#__PURE__*/React.createElement("div", {
    className: "grid md:grid-cols-2 gap-4"
  }, /*#__PURE__*/React.createElement(Section, {
    title: "Data sources",
    sub: E ? "".concat(E.leagueName || "Your league", " \xB7 synced ").concat(fmtTime(E.generated)) : "No data file found."
  }, row(!!E, "ESPN league", E ? "".concat((E.teams || []).length, " teams \xB7 ").concat((E.players || []).length, " players") : ""), row(!!(E && E.model), "GM model", E && E.model ? "".concat(Object.keys(E.model.base || {}).length, " players") : ""), row(!!(E && E.model && E.model.odds && Object.keys(E.model.odds).length), "Betting lines", E && E.model && E.model.odds ? "".concat(Object.keys(E.model.odds).length, " days") : ""), row(!!(Sg && Sg.recent), "Recent form", Sg && Sg.recent ? "".concat(Object.keys(Sg.recent).length, " players") : ""), row(!!(Sg && Sg.pp1), "PP1 units", Sg && Sg.pp1 ? "checked ".concat(Sg.pp1.asof) : ""), row(!!(Sg && Sg.news), "News", Sg && Sg.news ? "".concat(Object.keys(Sg.news).length, " players") : ""), row(!!(Sg && Sg.injuries), "Injuries", Sg && Sg.injuries ? "".concat(Object.keys(Sg.injuries).length, " players") : ""), row(!!(E && E.goalies), "Starting goalies", E && E.goalies ? "".concat(Object.keys(E.goalies).length, " days") : ""), E && /*#__PURE__*/React.createElement("button", {
    className: "border border-slate-300 rounded-lg px-3 py-1.5 mt-3 text-xs",
    onClick: function onClick() {
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
    onClick: function onClick() {
      return setIo(JSON.stringify(s));
    }
  }, "Export text"), /*#__PURE__*/React.createElement("button", {
    className: "border border-slate-300 rounded px-2 py-1",
    onClick: function onClick() {
      try {
        var v = JSON.parse(io);
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
    onChange: function onChange(e) {
      return setIo(e.target.value);
    }
  })), /*#__PURE__*/React.createElement("button", {
    className: "text-red-600 text-xs mt-3",
    onClick: function onClick() {
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
    onChange: function onChange(e) {
      return setS({
        ...s,
        blend: Math.max(0, parseFloat(e.target.value) || 0)
      });
    }
  })), /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500 mt-1"
  }, "How fast real results replace ESPN's projection (10 = half-and-half after 10 games)."), /*#__PURE__*/React.createElement("label", {
    className: "flex items-center gap-2 mt-3"
  }, /*#__PURE__*/React.createElement("input", {
    type: "checkbox",
    checked: s.autoDone,
    onChange: function onChange(e) {
      return setS({
        ...s,
        autoDone: e.target.checked
      });
    }
  }), " Count completed days automatically"), /*#__PURE__*/React.createElement("label", {
    className: "flex items-center gap-2 mt-2"
  }, /*#__PURE__*/React.createElement("input", {
    type: "checkbox",
    checked: s.autoGoalie !== false,
    onChange: function onChange(e) {
      return setS({
        ...s,
        autoGoalie: e.target.checked
      });
    }
  }), " Set goalie start % automatically from recent starts"), /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500 mt-1"
  }, "Uses who started each team's last ~10 games (blended with last season). Kicks in once a team has played 3 games; applied at every sync. Turn off to keep your own numbers.")), /*#__PURE__*/React.createElement(Section, {
    title: "Team names"
  }, s.teams.map(function (t) {
    return /*#__PURE__*/React.createElement("div", {
      key: t.id,
      className: "flex gap-2 mb-1 items-center"
    }, /*#__PURE__*/React.createElement("input", {
      className: inp + " flex-1",
      value: t.name,
      onChange: function onChange(e) {
        return setS({
          ...s,
          teams: s.teams.map(function (x) {
            return x.id === t.id ? {
              ...x,
              name: e.target.value
            } : x;
          })
        });
      }
    }), t.id === s.me && /*#__PURE__*/React.createElement("span", {
      className: "text-xs text-blue-700"
    }, "you"));
  })));
}

// ---------- Clickable names, team pages, My Team (UI refresh) ----------
var TL = function TL(_ref52) {
  var s = _ref52.s,
    id = _ref52.id,
    className = _ref52.className;
  if (!id) return null;
  var nm = teamName(s, id);
  if (id === "fa") return /*#__PURE__*/React.createElement("span", {
    className: className || ""
  }, nm);
  return /*#__PURE__*/React.createElement("a", {
    href: id === s.me ? "#myteam" : gxHash("teams", null, id),
    className: "hover:underline text-left " + (className || ""),
    onClick: function onClick(e) {
      /* gx072-tl */e.stopPropagation();
      if (gxNewTab(e)) return;
      e.preventDefault();
      if (window.__NAV) window.__NAV.team(id);
    }
  }, nm);
};
var PN = function PN(_ref53) {
  var p = _ref53.p,
    className = _ref53.className;
  return /*#__PURE__*/React.createElement("a", {
    href: gxPHref(p),
    className: "hover:underline text-left " + (className === undefined ? "font-medium" : className),
    onClick: function onClick(e) {
      /* gx072-pn */e.stopPropagation();
      if (gxNewTab(e)) return;
      e.preventDefault();
      if (window.__NAV) window.__NAV.player(p);
    }
  }, p.n);
};
var __LT = null;
function leagueTable(s) {
  var key = [s.players, s.weeks, s.wk, s.blend, s.autoDone, window.__PMODE];
  if (__LT && __LT.key.every(function (v, i) {
    return v === key[i];
  })) return __LT.v;
  var K = s.blend,
    today = todayISO();
  var rows = s.teams.map(function (t) {
    var r = s.players.filter(function (p) {
      return p.ft === t.id;
    });
    var ros = 0,
      n4 = 0,
      days = 0;
    s.weeks.slice(s.wk).forEach(function (w, i) {
      var dw = deriveWeek(w, s.autoDone);
      var from = i === 0 ? dw.done : 0;
      var v = weekProj(r, dw, K, from).total;
      ros += v;
      if (i < 4) n4 += v;
      days += Math.max(0, dw.days.length - from);
    });
    var perGame = function perGame(pos, n) {
      return r.filter(function (p) {
        return p.p === pos && !p.ir && avail(p, today) > 0;
      }).map(function (p) {
        return effAvg(p, K) * (pos === "G" ? p.prob : 1);
      }).sort(function (a, b) {
        return b - a;
      }).slice(0, n).reduce(function (a, b) {
        return a + b;
      }, 0);
    };
    var grp = {
      F: perGame("F", 10),
      D: perGame("D", 5),
      G: perGame("G", 2)
    };
    var out = r.filter(function (p) {
      return p.ir || avail(p, today) === 0;
    }).length;
    return {
      t: t,
      ros: ros,
      n4: n4,
      strength: days ? ros / days * 7 : 0,
      grp: grp,
      out: out
    };
  });
  var rec = {};
  s.teams.forEach(function (t) {
    return rec[t.id] = {
      w: 0,
      l: 0,
      t: 0,
      pf: 0,
      n: 0
    };
  });
  s.weeks.forEach(function (w) {
    var len = (w.dates || []).length;
    if (!len || effDone(w, s.autoDone) < len) return;
    (w.pairs || []).forEach(function (_ref54) {
      var _ref55 = _slicedToArray(_ref54, 2),
        a = _ref55[0],
        b = _ref55[1];
      if (!rec[a] || !rec[b]) return;
      var x = +(w.act || {})[a] || 0,
        y = +(w.act || {})[b] || 0;
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
  rows.forEach(function (x) {
    return x.rec = rec[x.t.id];
  });
  rows.sort(function (a, b) {
    return b.strength - a.strength;
  });
  var grpRank = {};
  ["F", "D", "G"].forEach(function (k) {
    _toConsumableArray(rows).sort(function (a, b) {
      return b.grp[k] - a.grp[k];
    }).forEach(function (x, i) {
      grpRank[x.t.id] = _defineProperty({}, k, i + 1);
    });
  });
  var v = {
    rows: rows,
    grpRank: grpRank
  };
  __LT = {
    key: key,
    v: v
  };
  return v;
}
var recTxt = function recTxt(r) {
  return r && r.n ? "".concat(r.w, "-").concat(r.l).concat(r.t ? "-" + r.t : "") : "–";
};
var RankSpans = function RankSpans(_ref56) {
  var g = _ref56.g;
  return /*#__PURE__*/React.createElement("span", null, ["F", "D", "G"].map(function (k) {
    return /*#__PURE__*/React.createElement("span", {
      key: k,
      className: "mr-2 " + (g[k] <= 3 ? "text-green-700" : g[k] >= 8 ? "text-red-600" : "")
    }, k, " #", g[k]);
  }));
};
function RosterView(_ref57) {
  var s = _ref57.s,
    wk = _ref57.wk,
    team = _ref57.team;
  // roster view v9: no Signals column, phone list by position (news_logos.py)
  var K = s.blend,
    done = wk.done || 0;
  var roster = s.players.filter(function (p) {
    return p.ft === team;
  });
  var order = {
    F: 0,
    D: 1,
    G: 2
  };
  var sorted = _toConsumableArray(roster).sort(function (a, b) {
    return (a.ir ? 1 : 0) - (b.ir ? 1 : 0) || order[a.p] - order[b.p] || effAvg(b, K) - effAvg(a, K);
  });
  var Ls = wk.days.map(function (_, d) {
    return d < done ? null : dayLineup(roster, wk, d, K);
  });
  var wkPts = function wkPts(p) {
    return Ls.reduce(function (a, L) {
      if (!L) return a;
      var x = L.start.find(function (y) {
        return y.id === p.id;
      });
      return a + (x ? x.x : 0);
    }, 0);
  };
  var left = function left(p) {
    return (wk.games[p.t] || []).filter(function (d) {
      return d >= done;
    }).length;
  };
  var stTag = function stTag(p) {
    return p.ir ? "IR" : p.status && p.status !== "ACTIVE" ? M_ST[p.status] || p.status.replace(/_/g, " ") : "";
  };
  var groups = [["Forwards", sorted.filter(function (p) {
    return !p.ir && p.p === "F";
  })], ["Defence", sorted.filter(function (p) {
    return !p.ir && p.p === "D";
  })], ["Goalies", sorted.filter(function (p) {
    return !p.ir && p.p === "G";
  })], ["Injured reserve", sorted.filter(function (p) {
    return p.ir;
  })]].filter(function (g) {
    return g[1].length;
  });
  return /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    className: "m-hide overflow-x-auto"
  }, /*#__PURE__*/React.createElement("table", {
    className: "w-full text-sm"
  }, /*#__PURE__*/React.createElement("thead", {
    className: "text-left"
  }, /*#__PURE__*/React.createElement("tr", null, ["Player", "", "Proj / game", "Games left", "Week pts"].map(function (h, i) {
    return /*#__PURE__*/React.createElement("th", {
      key: i,
      className: "px-2 py-2"
    }, h);
  }))), /*#__PURE__*/React.createElement("tbody", null, sorted.map(function (p) {
    return /*#__PURE__*/React.createElement("tr", {
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
    }, p.p, " \xB7 ", /*#__PURE__*/React.createElement(TeamLogo, {
      t: p.t
    })), /*#__PURE__*/React.createElement("td", {
      className: "px-2 py-2"
    }, f1(effAvg(p, K))), /*#__PURE__*/React.createElement("td", {
      className: "px-2 py-2"
    }, p.ir ? "–" : left(p)), /*#__PURE__*/React.createElement("td", {
      className: "px-2 py-2 font-semibold"
    }, p.ir ? "–" : f1(wkPts(p))));
  })))), /*#__PURE__*/React.createElement("div", {
    className: "m-only"
  }, groups.map(function (_ref58) {
    var _ref59 = _slicedToArray(_ref58, 2),
      title = _ref59[0],
      list = _ref59[1];
    return /*#__PURE__*/React.createElement("div", {
      key: title,
      className: "mb-2"
    }, /*#__PURE__*/React.createElement("div", {
      className: "m-ghead"
    }, /*#__PURE__*/React.createElement("span", null, title), /*#__PURE__*/React.createElement("span", null, "Proj"), /*#__PURE__*/React.createElement("span", null, "Gms"), /*#__PURE__*/React.createElement("span", null, "Week")), list.map(function (p) {
      var tg = stTag(p);
      return /*#__PURE__*/React.createElement("div", {
        key: p.id,
        className: "m-rrow",
        role: "button",
        onClick: function onClick() {
          return window.__NAV && window.__NAV.player(p);
        }
      }, /*#__PURE__*/React.createElement(TeamLogo, {
        t: p.t,
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
    }));
  })));
}
function MyTeam(_ref60) {
  var s = _ref60.s,
    setS = _ref60.setS,
    wk = _ref60.wk,
    go = _ref60.go;
  // team roster v37: one roster list with role, form, schedule and rank (news_logos.py)
  var K = s.blend,
    today = todayISO(),
    gen = (window.ESPN_DATA || {}).generated;
  var _useState79 = useState("pg"),
    _useState80 = _slicedToArray(_useState79, 2),
    sort = _useState80[0],
    setSort = _useState80[1];
  var _useState81 = useState({}),
    _useState82 = _slicedToArray(_useState81, 2),
    hist = _useState82[0],
    setHist = _useState82[1];
  var roster = s.players.filter(function (p) {
    return p.ft === s.me;
  });
  var pv = function pv(p) {
    return effAvg(p, K) * (p.p === "G" ? p.prob : 1);
  };
  var T = leagueTable(s),
    ri = T.rows.findIndex(function (r) {
      return r.t.id === s.me;
    }),
    meRow = ri >= 0 ? T.rows[ri] : null,
    g = T.grpRank[s.me] || {};
  var dates = wk.dates || [],
    done = wk.done || 0;
  var nextW = s.weeks[s.wk + 1] ? deriveWeek(s.weeks[s.wk + 1], s.autoDone) : null;
  var _mu = useMemo(function () {
    var P = pby(),
      o = {};
    dates.forEach(function (dt) {
      var AD = actDay(s.me, dt);
      if (!AD) return;
      Object.entries(AD).forEach(function (_ref61) {
        var _ref62 = _slicedToArray(_ref61, 2),
          pid = _ref62[0],
          v = _ref62[1];
        if (!v || v[0] == null || !ESLOT[v[1]]) return;
        var p = P["e" + pid];
        if (!p || !(SCHED[p.t] && SCHED[p.t].has(dt)) || gState(p.t, dt).s === "P" || p.p === "G" && !v[0]) return;
        o[p.id] = (o[p.id] || 0) + v[0];
      });
    });
    return o;
  }, [s.players, wk, gen]);
  var total = Object.values(_mu).reduce(function (a, v) {
    return a + Math.max(0, v);
  }, 0);
  var rankOf = useMemo(function () {
    var o = {};
    ["F", "D", "G"].forEach(function (k) {
      s.players.filter(function (p) {
        return p.p === k && p.prob > 0 && (p.proj !== false || p.gp > 0);
      }).map(function (p) {
        return [p.id, pv(p)];
      }).sort(function (a, b) {
        return b[1] - a[1];
      }).forEach(function (x, i) {
        return o[x[0]] = i + 1;
      });
    });
    return o;
  }, [s.players, K, window.__PMODE]);
  var roles = useMemo(function () {
    var L = window.LINES_DATA,
      o = {};
    if (!L || !L.teams) return o;
    var key = function key(x) {
      return nrm(x).replace(/[.'\u2019]/g, "").replace(/-/g, " ").replace(/\s+/g, " ").trim();
    };
    roster.forEach(function (p) {
      var ln = (L.teams[p.t] || {}).lines;
      if (!ln) return;
      var k = key(p.n),
        has = function has(sl) {
          return (ln[sl] || []).some(function (x) {
            return key(x) === k;
          });
        };
      o[p.id] = {
        es: ["F1", "F2", "F3", "F4", "D1", "D2", "D3", "G"].find(has),
        pp: ["PP1", "PP2"].find(has)
      };
    });
    return o;
  }, [s.players, (window.LINES_DATA || {}).generated]);
  useEffect(function () {
    var dead = false;
    var E = window.ESPN_DATA || {},
      sc = s.sc || {},
      out = {},
      byId = {};
    roster.forEach(function (p) {
      return byId[String(p.id).slice(1)] = p;
    });
    Object.entries(E.daily || {}).forEach(function (_ref63) {
      var _ref64 = _slicedToArray(_ref63, 2),
        d = _ref64[0],
        Tm = _ref64[1];
      return Object.values(Tm || {}).forEach(function (tm) {
        return Object.entries(tm || {}).forEach(function (_ref65) {
          var _ref66 = _slicedToArray(_ref65, 2),
            pid = _ref66[0],
            v = _ref66[1];
          var p = byId[pid];
          if (!p || !v || v[0] == null || !(SCHED[p.t] && SCHED[p.t].has(d)) || gState(p.t, d).s === "P" || p.p === "G" && !v[0]) return;
          (out[pid] = out[pid] || {})[d] = v[0];
        });
      });
    });
    var est = function est(x) {
      return x.sv != null ? (x.dec === "W" ? sc.W ?? 5 : 0) + (x.dec === "O" ? sc.OTL ?? 1 : 0) + (x.sv || 0) * (sc.SV ?? 0.6) + (x.ga || 0) * (sc.GA ?? -3) : (x.g || 0) * (sc.G ?? 6) + (x.a || 0) * (sc.A ?? 4) + (x.pm || 0) * (sc.PM ?? 2) + (x.sog || 0) * (sc.SOG ?? 1) + (x.hit || 0) * (sc.HIT ?? 0.1) + (x.blk || 0) * (sc.BLK ?? 1) + (x.ppg || 0) * (sc.PPP ?? 2);
    };
    var finish = function finish() {
      if (dead) return;
      var h = {};
      Object.keys(out).forEach(function (pid) {
        h[pid] = Object.keys(out[pid]).sort().slice(-5).map(function (d) {
          return {
            d: d,
            v: out[pid][d]
          };
        });
      });
      setHist(h);
    };
    finish();
    gxBoxIdx().then(function (ds) {
      return Promise.all(ds.slice(-14).map(function (d) {
        return gxBoxDay(d).then(function (day) {
          return [d, day];
        });
      }));
    }).then(function (days) {
      days.forEach(function (_ref67) {
        var _ref68 = _slicedToArray(_ref67, 2),
          d = _ref68[0],
          day = _ref68[1];
        if (!day) return;
        Object.keys(byId).forEach(function (pid) {
          var x = day[pid];
          if (x) {
            var o2 = out[pid] = out[pid] || {};
            o2[d] = x.fp != null ? x.fp : o2[d] != null ? o2[d] : est(x);
          } else if (out[pid]) delete out[pid][d];
        });
      });
      finish();
    }).catch(function () {});
    return function () {
      dead = true;
    };
  }, [s.players, gen]);
  var RO = {
    F1: "L1",
    F2: "L2",
    F3: "L3",
    F4: "L4",
    D1: "D1",
    D2: "D2",
    D3: "D3"
  };
  var roleTxt = function roleTxt(p) {
    if (p.p === "G") return Math.round(p.prob * 100) + "% of starts";
    var r = roles[p.id];
    if (!r) return "";
    return [r.es ? RO[r.es] : "not in lineup", r.pp].filter(Boolean).join(" \xB7 ");
  };
  var nextGame = function nextGame(p) {
    var S = SCHED[p.t];
    if (!S || p.ir) return "";
    for (var i = 0; i < 10; i++) {
      var dt = addDays(today, i);
      if (S.has(dt) && (i > 0 || gState(p.t, dt).s === "P")) {
        var gm = gameOf(p.t, dt);
        return (i === 0 ? "Today" : dayLabel(dt).split(",")[0]) + (gm ? (gm.h ? " vs " : " @ ") + gm.o : "");
      }
    }
    return "";
  };
  var left = function left(p) {
    return (wk.games[p.t] || []).filter(function (d) {
      return dates[d] >= today && gState(p.t, dates[d]).s === "P";
    }).length;
  };
  var nextG = function nextG(p) {
    return nextW ? gms(nextW, p.t) : 0;
  };
  var keyFn = {
    mu: function mu(p) {
      return _mu[p.id] || 0;
    },
    left: left,
    next: nextG,
    sea: function sea(p) {
      return p.gp ? p.tot / p.gp : -99;
    },
    pg: pv,
    rk: function rk(p) {
      return -(rankOf[p.id] || 9999);
    }
  }[sort];
  var grp = function grp(k) {
    return roster.filter(function (p) {
      return !p.ir && p.p === k;
    }).sort(function (a, b) {
      return keyFn(b) - keyFn(a);
    });
  };
  var groups = [["Forwards", grp("F")], ["Defence", grp("D")], ["Goalies", grp("G")], ["Injured reserve", roster.filter(function (p) {
    return p.ir;
  })]].filter(function (x) {
    return x[1].length;
  });
  var healthy = roster.filter(function (p) {
    return !p.ir;
  }).sort(function (a, b) {
    return effAvg(b, K) - effAvg(a, K);
  });
  var prot = new Set([].concat(_toConsumableArray(healthy.slice(0, s.protectTop ?? 8).map(function (p) {
    return p.id;
  })), _toConsumableArray(roster.filter(function (p) {
    return p.keep;
  }).map(function (p) {
    return p.id;
  }))));
  var weak = healthy.filter(function (p) {
    return !prot.has(p.id);
  }).sort(function (a, b) {
    return pv(a) - pv(b);
  }).slice(0, 3);
  var HB = function HB(k, l, cls) {
    return /*#__PURE__*/React.createElement("button", {
      type: "button",
      className: "n " + (cls || "") + (sort === k ? " on" : ""),
      onClick: function onClick() {
        return setSort(sort === k ? "pg" : k);
      }
    }, l);
  };
  var spark = function spark(p) {
    var h = hist[String(p.id).slice(1)] || [];
    return /*#__PURE__*/React.createElement("div", {
      className: "gx-sp m-hide",
      title: "Last five games, oldest to newest"
    }, h.length ? h.map(function (x, i) {
      return /*#__PURE__*/React.createElement("i", {
        key: i,
        style: {
          height: Math.max(2, Math.min(22, Math.max(0, x.v) / 20 * 22)),
          background: x.v < 0 ? "var(--bad)" : "var(--ink2)"
        }
      });
    }) : /*#__PURE__*/React.createElement("span", {
      className: "text-xs text-slate-500"
    }, "\u2013"));
  };
  var row = function row(p) {
    var st = p.ir ? "IR" : p.status && p.status !== "ACTIVE" ? M_ST[p.status] || p.status.replace(/_/g, " ") : "";
    var m = _mu[p.id],
      sea = p.gp ? p.tot / p.gp : null,
      gap = sea != null && p.avg > 0 ? sea - p.avg : null,
      rk = rankOf[p.id];
    var sub = [roleTxt(p), nextGame(p)].filter(Boolean).join(" \xB7 ");
    return /*#__PURE__*/React.createElement("div", {
      key: p.id,
      className: "gx-ro"
    }, /*#__PURE__*/React.createElement(TeamLogo, {
      t: p.t,
      size: 26
    }), /*#__PURE__*/React.createElement("div", {
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
    }, sub) : null), spark(p), /*#__PURE__*/React.createElement("div", {
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
    }, sea == null ? "\u2013" : /*#__PURE__*/React.createElement(React.Fragment, null, f1(sea), gap != null ? /*#__PURE__*/React.createElement("span", {
      className: "text-xs",
      style: {
        marginLeft: 6,
        color: gap >= 0 ? "var(--good)" : "var(--bad)"
      }
    }, (gap >= 0 ? "+" : "") + f1(gap)) : null)), /*#__PURE__*/React.createElement("div", {
      className: "n"
    }, f1(effAvg(p, K))), /*#__PURE__*/React.createElement("div", {
      className: "n text-xs text-slate-500 m-hide"
    }, rk ? p.p + " " + ordN(rk) : "\u2013"));
  };
  var rkc = function rkc(v) {
    return v >= 8 ? {
      color: "var(--bad)"
    } : v && v <= 3 ? {
      color: "var(--good)"
    } : null;
  };
  var order = {
    F: 0,
    D: 1,
    G: 2
  };
  var sorted = _toConsumableArray(roster).sort(function (a, b) {
    return (a.ir ? 1 : 0) - (b.ir ? 1 : 0) || order[a.p] - order[b.p] || effAvg(b, K) - effAvg(a, K);
  });
  var Ls = wk.days.map(function (_, d) {
    return d < done ? null : dayLineup(roster, wk, d, K);
  });
  var cell = function cell(p, d) {
    if (p.ir || !(wk.games[p.t] || []).includes(d)) return "none";
    var L = Ls[d];
    if (!L) return "past";
    if (L.start.some(function (x) {
      return x.id === p.id;
    })) return "start";
    if (L.bench.some(function (x) {
      return x.id === p.id;
    })) return "sit";
    return "out";
  };
  var CELL = {
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
  }, /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("div", {
    className: "gx-ro gx-roh"
  }, /*#__PURE__*/React.createElement("span", null), /*#__PURE__*/React.createElement("span", null, "Tap a heading to sort"), /*#__PURE__*/React.createElement("span", {
    className: "n m-hide"
  }, "Last 5"), HB("mu", "Matchup"), HB("left", "Left"), HB("next", "Next wk", "m-hide"), HB("sea", "So far", "m-hide"), HB("pg", "Expected"), HB("rk", "Rank", "m-hide")), groups.map(function (_ref69) {
    var _ref70 = _slicedToArray(_ref69, 2),
      title = _ref70[0],
      list = _ref70[1];
    return /*#__PURE__*/React.createElement("div", {
      key: title,
      style: {
        marginBottom: 10
      }
    }, /*#__PURE__*/React.createElement("div", {
      className: "gx-tag",
      style: {
        padding: "8px 0 4px"
      }
    }, title), list.map(row));
  })), /*#__PURE__*/React.createElement(GxPanel, {
    title: "Weakest spots",
    right: "First to drop or include in a trade"
  }, weak.length ? weak.map(function (p, i) {
    return /*#__PURE__*/React.createElement("div", {
      key: p.id,
      className: "gx-row",
      style: i ? null : {
        borderTop: 0
      }
    }, /*#__PURE__*/React.createElement(TeamLogo, {
      t: p.t,
      size: 22
    }), /*#__PURE__*/React.createElement("span", {
      className: "min-w-0 truncate",
      style: {
        flex: 1
      }
    }, /*#__PURE__*/React.createElement(PN, {
      p: p,
      className: ""
    })), /*#__PURE__*/React.createElement("span", {
      className: "text-xs text-slate-500 whitespace-nowrap"
    }, rankOf[p.id] ? p.p + " " + ordN(rankOf[p.id]) : p.p), /*#__PURE__*/React.createElement("span", {
      className: "font-semibold text-right",
      style: {
        minWidth: 40,
        fontVariantNumeric: "tabular-nums"
      }
    }, f1(pv(p))));
  }) : /*#__PURE__*/React.createElement("div", {
    className: "text-sm text-slate-500"
  }, "Everyone outside your protected players is pulling his weight.")), /*#__PURE__*/React.createElement(MyForm, {
    s: s
  }), /*#__PURE__*/React.createElement(MyInjProt, {
    s: s,
    setS: setS,
    wk: wk
  }), /*#__PURE__*/React.createElement(Section, {
    title: "This week, day by day",
    sub: "Bright = in your lineup, amber = plays but would sit, red = out, grey = already played."
  }, /*#__PURE__*/React.createElement("div", {
    className: "overflow-x-auto"
  }, /*#__PURE__*/React.createElement("table", {
    className: "text-sm w-full"
  }, /*#__PURE__*/React.createElement("thead", null, /*#__PURE__*/React.createElement("tr", null, /*#__PURE__*/React.createElement("th", {
    className: "px-2 py-2 text-left"
  }, "Player"), wk.days.map(function (d, i) {
    return /*#__PURE__*/React.createElement("th", {
      key: i,
      className: "px-1 py-2 text-center"
    }, d.split(",")[0]);
  }))), /*#__PURE__*/React.createElement("tbody", null, sorted.filter(function (p) {
    return !p.ir;
  }).map(function (p) {
    return /*#__PURE__*/React.createElement("tr", {
      key: p.id,
      className: "border-t border-slate-100"
    }, /*#__PURE__*/React.createElement("td", {
      className: "px-2 py-1 whitespace-nowrap"
    }, /*#__PURE__*/React.createElement(PN, {
      p: p,
      className: ""
    }), " ", /*#__PURE__*/React.createElement("span", {
      className: "text-xs text-slate-400"
    }, p.p)), wk.days.map(function (_, d) {
      var c = cell(p, d);
      return /*#__PURE__*/React.createElement("td", {
        key: d,
        className: "px-1 py-1 text-center"
      }, c === "none" ? /*#__PURE__*/React.createElement("span", {
        className: "text-slate-400"
      }, "\xB7") : /*#__PURE__*/React.createElement("span", {
        className: "inline-block w-6 h-3 rounded " + CELL[c]
      }));
    }));
  }))))));
}
function TeamsTab(_ref71) {
  var s = _ref71.s,
    wk = _ref71.wk,
    openTeam = _ref71.openTeam;
  var T = leagueTable(s);
  return /*#__PURE__*/React.createElement(Section, {
    title: "Teams",
    sub: "Every team in your league, ordered by power ranking. Tap a team to see its roster, its week and how it fits with yours for trades."
  }, /*#__PURE__*/React.createElement("div", {
    className: "grid sm:grid-cols-2 lg:grid-cols-3 gap-3 mt-2"
  }, T.rows.map(function (x, i) {
    var g = T.grpRank[x.t.id] || {};
    var o = oppOf(wk, x.t.id);
    var me = x.t.id === s.me;
    return /*#__PURE__*/React.createElement("div", {
      key: x.t.id,
      role: "button",
      onClick: function onClick() {
        return openTeam(x.t.id);
      },
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
    }, x.rec && x.rec.n ? "".concat(recTxt(x.rec), " \xB7 ").concat(f1(x.rec.pf), " PF \xB7 ") : "", f1(x.strength), " pts/wk projected"), /*#__PURE__*/React.createElement("div", {
      className: "text-xs mt-2"
    }, /*#__PURE__*/React.createElement(RankSpans, {
      g: g
    })), /*#__PURE__*/React.createElement("div", {
      className: "text-xs text-slate-500 mt-2"
    }, o ? "This week vs ".concat(teamName(s, o)) : "No matchup loaded", x.out ? " \xB7 ".concat(x.out, " out") : ""));
  })));
}
function TeamPage(props) {
  // team page v51: new style, with the older detailed view one tap away (news_logos.py)
  var s = props.s,
    wk = props.wk,
    tid = props.id,
    back = props.back;
  var _useState83 = useState(false),
    _useState84 = _slicedToArray(_useState83, 2),
    old = _useState84[0],
    setOld = _useState84[1];
  if (old || !tid || !s || !wk) return /*#__PURE__*/React.createElement(TeamPage0, props);
  var K = s.blend,
    today = todayISO(),
    dates = wk.dates || [];
  var T = leagueTable(s),
    pr = T.rows.findIndex(function (x) {
      return x.t.id === tid;
    }),
    row = pr >= 0 ? T.rows[pr] : null;
  var g = T.grpRank[tid] || {},
    mg = T.grpRank[s.me] || {};
  var roster = s.players.filter(function (p) {
    return p.ft === tid;
  });
  var opp = oppOf(wk, tid),
    sc = function sc(id) {
      return +(wk.act || {})[id] || 0;
    };
  var left = function left(p) {
    return (wk.games[p.t] || []).filter(function (d) {
      return dates[d] >= today && gState(p.t, dates[d]).s === "P";
    }).length;
  };
  var pv = function pv(p) {
    return effAvg(p, K) * (p.p === "G" ? p.prob : 1);
  };
  var grp = function grp(k) {
    return roster.filter(function (p) {
      return !p.ir && p.p === k;
    }).sort(function (a, b) {
      return pv(b) - pv(a);
    });
  };
  var groups = [["Forwards", grp("F")], ["Defence", grp("D")], ["Goalies", grp("G")], ["Injured reserve", roster.filter(function (p) {
    return p.ir;
  })]].filter(function (x) {
    return x[1].length;
  });
  var trade = function trade() {
    window.__TRADE_P = {
      id: null,
      ft: tid
    };
    if (props.go) props.go("moves", "trades");
    setTimeout(function () {
      return window.dispatchEvent(new Event("gm-trade"));
    }, 50);
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
  }, [row && row.rec.n ? row.rec.w + "-" + row.rec.l : "", pr >= 0 ? ordN(pr + 1) + " in strength" : "", row ? Math.round(row.strength) + " a week" : ""].filter(Boolean).join(" \xB7 ")), tid !== s.me ? /*#__PURE__*/React.createElement("button", {
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
  }, [["Forwards", "F"], ["Defence", "D"], ["Goalies", "G"]].map(function (_ref72, i) {
    var _ref73 = _slicedToArray(_ref72, 2),
      lab = _ref73[0],
      k = _ref73[1];
    return /*#__PURE__*/React.createElement("div", {
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
    }, tid === s.me ? "" : "you " + (mg[k] ? ordN(mg[k]) : "\u2013")));
  }))), /*#__PURE__*/React.createElement(GxRosterTable, {
    s: s,
    wk: wk,
    tid: tid
  }), /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: "text-xs text-slate-500 underline",
    onClick: function onClick() {
      return setOld(true);
    }
  }, "Show the older detailed view"));
}
function TeamPage0(_ref74) {
  var s = _ref74.s,
    wk = _ref74.wk,
    id = _ref74.id,
    back = _ref74.back,
    go = _ref74.go;
  var K = s.blend;
  var T = leagueTable(s);
  var x = T.rows.find(function (r) {
    return r.t.id === id;
  });
  if (!x) return /*#__PURE__*/React.createElement(Section, {
    title: "Team not found"
  }, /*#__PURE__*/React.createElement("button", {
    className: "text-blue-600",
    onClick: back
  }, "\u2190 Back"));
  var rank = T.rows.indexOf(x) + 1,
    g = T.grpRank[id] || {},
    mg = T.grpRank[s.me] || {};
  var roster = s.players.filter(function (p) {
    return p.ft === id;
  });
  var done = wk.done || 0,
    o = oppOf(wk, id);
  var act = function act(t) {
    return +(wk.act || {})[t] || 0;
  };
  var mine = weekLive(roster, wk, K, id),
    theirs = o ? weekLive(s.players.filter(function (p) {
      return p.ft === o;
    }), wk, K, o) : null;
  var posName = {
    F: "forwards",
    D: "defence",
    G: "goalies"
  };
  var need = {
    F: 10,
    D: 5,
    G: 2
  };
  var myWeak = ["F", "D", "G"].sort(function (a, b) {
    return (mg[b] || 0) - (mg[a] || 0);
  })[0];
  var theyStrong = ["F", "D", "G"].filter(function (k) {
    return g[k] < mg[k];
  });
  var pv = function pv(p) {
    return effAvg(p, K) * (p.p === "G" ? p.prob : 1);
  };
  var myAt = s.players.filter(function (p) {
    return p.ft === s.me && !p.ir && p.p === myWeak;
  }).map(pv).sort(function (a, b) {
    return b - a;
  });
  var bar = myAt.length ? myAt[Math.min(need[myWeak], myAt.length) - 1] : 0;
  var targets = roster.filter(function (p) {
    return !p.ir && p.p === myWeak && pv(p) > bar;
  }).sort(function (a, b) {
    return pv(b) - pv(a);
  }).slice(0, 4);
  var news = roster.filter(function (p) {
    return newsOf(p).length;
  }).slice(0, 6);
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
    sub: x.rec && x.rec.n ? "".concat(f1(x.rec.pf), " points for") : "no completed weeks yet"
  }), /*#__PURE__*/React.createElement(Card, {
    label: "Strength",
    value: f1(x.strength),
    sub: "projected pts per week"
  }), /*#__PURE__*/React.createElement(Card, {
    label: "Group ranks",
    value: /*#__PURE__*/React.createElement(RankSpans, {
      g: g
    }),
    sub: "among ".concat(T.rows.length, " teams")
  }), /*#__PURE__*/React.createElement(Card, {
    label: "Players out",
    value: x.out,
    sub: "injured or on IR"
  }))), /*#__PURE__*/React.createElement("div", {
    className: "grid md:grid-cols-2 gap-4"
  }, /*#__PURE__*/React.createElement(Section, {
    title: "Their week",
    sub: wk.label,
    link: ["All matchups", function () {
      return go("matchup");
    }]
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
    sub: "Your weakest group: ".concat(posName[myWeak], " (#").concat(mg[myWeak], "). Theirs: F #").concat(g.F, " \xB7 D #").concat(g.D, " \xB7 G #").concat(g.G, ".")
  }, theyStrong.length ? /*#__PURE__*/React.createElement("div", {
    className: "mb-2"
  }, "They're stronger than you at ", /*#__PURE__*/React.createElement("b", null, theyStrong.map(function (k) {
    return posName[k];
  }).join(" and ")), ".") : /*#__PURE__*/React.createElement("div", {
    className: "mb-2 text-slate-500"
  }, "They're not stronger than you anywhere, so trade only for specific players."), /*#__PURE__*/React.createElement("div", {
    className: "font-medium mt-2 mb-1"
  }, "Players who'd upgrade your ", posName[myWeak]), targets.length ? targets.map(function (p) {
    return /*#__PURE__*/React.createElement("div", {
      key: p.id,
      className: "flex gap-2 py-1.5 border-t border-slate-100"
    }, /*#__PURE__*/React.createElement(PN, {
      p: p
    }), /*#__PURE__*/React.createElement("span", {
      className: "text-xs text-slate-400"
    }, p.p, " \xB7 ", /*#__PURE__*/React.createElement(TeamLogo, {
      t: p.t
    })), /*#__PURE__*/React.createElement("span", {
      className: "ml-auto text-xs text-slate-500"
    }, f1(pv(p)), "/game"));
  }) : /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-400"
  }, "None of their ", posName[myWeak], " beat your current starters."), /*#__PURE__*/React.createElement("button", {
    className: "bg-blue-600 rounded-lg px-3 py-1.5 mt-3 text-sm font-semibold",
    onClick: function onClick() {
      return go("moves", "trades", {
        partner: id
      });
    }
  }, "Trade with them"))), /*#__PURE__*/React.createElement(Section, {
    title: "Roster",
    sub: "Lineup order: forwards, defence, goalies, then IR. Tap a player for details."
  }, /*#__PURE__*/React.createElement(RosterView, {
    s: s,
    wk: wk,
    team: id
  })), news.length > 0 && /*#__PURE__*/React.createElement(Section, {
    title: "News"
  }, news.map(function (p) {
    return /*#__PURE__*/React.createElement(PlayerLine, {
      key: p.id,
      s: s,
      p: p
    });
  })));
}
function AdviceAll(props) {
  return /*#__PURE__*/React.createElement(AdvicePage, props);
}
function PlannerAll(props) {
  return /*#__PURE__*/React.createElement(PlanPage, props);
}
function TradesPanel(props) {
  // trades v10: analyzer and 2-for-1 merged into one builder (news_logos.py)
  return /*#__PURE__*/React.createElement(TradeBuilder, props);
}

// ---------- Phone notifications feed (reads notify_outbox.json) ----------
function PhoneFeed() {
  var _useState85 = useState(null),
    _useState86 = _slicedToArray(_useState85, 2),
    box = _useState86[0],
    setBox = _useState86[1];
  var _useState87 = useState(""),
    _useState88 = _slicedToArray(_useState87, 2),
    err = _useState88[0],
    setErr = _useState88[1];
  var _useState89 = useState(5),
    _useState90 = _slicedToArray(_useState89, 2),
    show = _useState90[0],
    setShow = _useState90[1];
  var load = function load() {
    return fetch("notify_outbox.json?t=" + Date.now()).then(function (r) {
      return r.ok ? r.json() : Promise.reject(r.status);
    }).then(function (b) {
      setBox(b);
      setErr("");
    }).catch(function () {
      return setErr("No notification history yet. It appears after the next sync.");
    });
  };
  useEffect(function () {
    load();
    var id = setInterval(load, 2 * 60 * 1000);
    return function () {
      return clearInterval(id);
    };
  }, []);
  var when = function when(iso) {
    var d = toDate(iso);
    return d ? d.toLocaleString("en-US", {
      weekday: "short",
      month: "short",
      day: "numeric",
      hour: "numeric",
      minute: "2-digit"
    }) : "";
  };
  var SEC = {
    lineup: "Lineup",
    mine: "Your players",
    pickup: "Pickup idea",
    other: "Other"
  };
  var items = box && box.items || [];
  var waiting = items.filter(function (i) {
    return !i.sent;
  }).reverse();
  var urgent = items.filter(function (i) {
    return i.sent && (i.via === "urgent" || !i.via && i.urgent);
  }).map(function (i) {
    return {
      at: i.sent_at || i.at,
      kind: "urgent",
      title: i.title,
      body: i.text
    };
  });
  var sent = [].concat(_toConsumableArray(urgent), _toConsumableArray(box && box.log || [])).sort(function (a, b) {
    return a.at < b.at ? 1 : -1;
  });
  var label = {
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
  }, "Waiting for the next summary (", waiting.length, ")"), waiting.length ? waiting.map(function (i) {
    return /*#__PURE__*/React.createElement("div", {
      key: i.k,
      className: "flex flex-wrap items-baseline gap-2 py-2 border-t border-slate-100"
    }, /*#__PURE__*/React.createElement("span", {
      className: "text-xs px-2 py-0.5 rounded " + (i.urgent ? "bg-red-100 text-red-600" : "bg-slate-200 text-slate-500")
    }, i.urgent ? "Urgent (quiet hours)" : SEC[i.section] || "Other"), /*#__PURE__*/React.createElement("span", {
      className: "text-sm text-slate-700 flex-1 min-w-[200px]"
    }, i.text), /*#__PURE__*/React.createElement("span", {
      className: "text-xs text-slate-400"
    }, when(i.at)));
  }) : /*#__PURE__*/React.createElement("div", {
    className: "text-sm text-slate-400"
  }, "Nothing waiting.")), /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    className: "text-xs uppercase tracking-wide text-slate-400 mb-1"
  }, "Sent to your phone"), sent.length ? sent.slice(0, show).map(function (m, i) {
    return /*#__PURE__*/React.createElement("div", {
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
    }, m.body));
  }) : /*#__PURE__*/React.createElement("div", {
    className: "text-sm text-slate-400"
  }, "Nothing sent yet. Your first summary arrives after 8 AM."), sent.length > show && /*#__PURE__*/React.createElement("button", {
    className: "text-sm text-blue-600 mt-2",
    onClick: function onClick() {
      return setShow(show + 12);
    }
  }, "Show older"))));
}
// ---------- team logos, game times and news filter (news_logos.py) ----------
var NHL_LOGO = {
  LA: "LAK",
  NJ: "NJD",
  SJ: "SJS",
  TB: "TBL"
};
function TeamLogo(_ref75) {
  var t = _ref75.t,
    size = _ref75.size;
  var _useState91 = useState(false),
    _useState92 = _slicedToArray(_useState91, 2),
    bad = _useState92[0],
    setBad = _useState92[1];
  if (!t) return null;
  var z = size || 28;
  if (bad) return /*#__PURE__*/React.createElement("span", null, t);
  return /*#__PURE__*/React.createElement("img", {
    src: "https://assets.nhle.com/logos/nhl/svg/" + (NHL_LOGO[t] || t) + (document.documentElement.getAttribute("data-theme") === "light" ? "_light.svg" : "_dark.svg"),
    alt: t,
    title: t,
    loading: "lazy",
    onError: function onError() {
      return setBad(true);
    },
    style: {
      width: z,
      height: z,
      objectFit: "contain",
      display: "inline-block",
      verticalAlign: "middle"
    }
  });
}
var gameOf = function gameOf(t, dt) {
  var G = (window.GAMES_DATA || {}).games || {};
  return dt && G[dt] ? G[dt][t] || null : null;
};
var gameTime = function gameTime(g) {
  var d = g && g.st ? new Date(g.st) : null;
  return d && !isNaN(d) ? d.toLocaleTimeString([], {
    hour: "numeric",
    minute: "2-digit"
  }) : "time TBD";
};
var NEWS_JUNK = /highlights|draft board|rankings|mailbag|podcast|give me a reason|league-winners|sleepers|\bbusts\b|best bets|predictions|betting|\bodds\b|takeaways|\bgrades\b|cheat sheet|start.?sit|waiver wire|what we learned/i;
var NEWS_KINDS = [["trade", "Trade", /\btrade|traded|acquir|deal sends/i], ["scratch", "Scratched", /scratch/i], ["susp", "Suspended", /suspen/i], ["injury", "Injury", /injur|\bIR\b|surgery|day-to-day|week-to-week|month-to-month|out for|out indefinitely|will miss|expected to miss|sidelined|concussion|upper-body|lower-body|leaves game|left the game|ruled out|won't play|will not play|questionable|doubtful/i], ["roster", "Roster move", /waive|claimed|recall|reassign|sent down|assigned to|loaned|signs|signed|extension|contract|released|buyout|activated|returns|back in the lineup|cleared/i], ["hot", "Hot", /streak|hat trick|multi-point|career-high|promot|top line|top-line|first line|pp1|two goals|three points|four points|scores twice|milestone|\brecord\b/i]];
var NEWS_DAYS = {
  trade: 7,
  scratch: 7,
  susp: 7,
  injury: 7,
  roster: 7,
  hot: 3,
  news: 1
};
var NEWS_RANK = {
  injury: 0,
  scratch: 0,
  susp: 0,
  trade: 1,
  roster: 2,
  hot: 3,
  news: 4
};
var NEWS_BIG = new Set(["trade", "scratch", "susp", "injury", "roster"]);
var NEWS_OUT = new Set(["injury", "scratch", "susp"]);
var NEWS_CLS = {
  injury: "text-red-600",
  scratch: "text-red-600",
  susp: "text-red-600",
  trade: "text-blue-600",
  roster: "text-blue-600",
  hot: "text-orange-600"
};
var NEWS_BADGE = {
  injury: "bg-red-100 text-red-600",
  scratch: "bg-red-100 text-red-600",
  susp: "bg-red-100 text-red-600",
  trade: "bg-blue-50 text-blue-600",
  roster: "bg-slate-200 text-slate-600",
  hot: "bg-amber-100 text-orange-600"
};
var newsAge = function newsAge(d) {
  if (!d) return 0;
  var a = Math.round((fromIso(todayISO()) - fromIso(String(d).slice(0, 10))) / 864e5);
  return isNaN(a) ? 0 : Math.max(0, a);
};
var newsOf = function newsOf(p) {
  var last = nrm(p.n).split(" ").pop();
  return (sigOf(p).news || []).map(function (n) {
    var h = n.h || "";
    if (!h || NEWS_JUNK.test(h) || !nrm(h).includes(last)) return null;
    var k = NEWS_KINDS.find(function (x) {
      return x[2].test(h);
    });
    var kind = k ? k[0] : "news",
      age = newsAge(n.d);
    return age < NEWS_DAYS[kind] ? {
      ...n,
      kind: kind,
      label: k ? k[1] : "",
      age: age
    } : null;
  }).filter(Boolean).sort(function (a, b) {
    return NEWS_RANK[a.kind] - NEWS_RANK[b.kind] || a.age - b.age;
  });
};
var NewsItem = function NewsItem(_ref76) {
  var n = _ref76.n;
  return /*#__PURE__*/React.createElement("div", {
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
};

// ---------- win probability (news_logos.py) ----------
var normCdf = function normCdf(z) {
  var t = 1 / (1 + 0.2316419 * Math.abs(z));
  var d = 0.3989423 * Math.exp(-z * z / 2);
  var p = d * t * (0.3193815 + t * (-0.3565638 + t * (1.781478 + t * (-1.821256 + t * 1.330274))));
  return z > 0 ? 1 - p : p;
};
// spread of a team's remaining points: game-to-game swings of every lineup player-game + 10% projection error
var projVar = function projVar(R) {
  var v = (0.1 * R.total) ** 2;
  R.days.forEach(function (L) {
    if (L) L.start.forEach(function (p) {
      var z = p.x0 != null ? p.x0 : p.x,
        sd = p.p === "G" ? 3 + 0.8 * z : 1.5 + 0.6 * z;
      v += sd * sd * (p.vf != null ? p.vf : 1);
    });
  });
  return v;
};
var winProb = function winProb(A, B, aA, aB) {
  var m = aA + A.total - (aB + B.total);
  var sd = Math.sqrt(projVar(A) + projVar(B));
  return sd > 0 ? normCdf(m / sd) : m > 0 ? 1 : m < 0 ? 0 : 0.5;
};
var wpTxt = function wpTxt(v) {
  return Math.round(Math.max(0.01, Math.min(0.99, v)) * 100) + "%";
};
function winChance(s, roster) {
  var w = deriveWeek(s.weeks[s.wk] || s.weeks[0], s.autoDone);
  var opp = oppOf(w, s.me) || s.opp;
  if (!opp) return null;
  var K = s.blend,
    done = w.done || 0;
  var A = weekLive(roster || s.players.filter(function (p) {
    return p.ft === s.me;
  }), w, K, s.me);
  var B = weekLive(s.players.filter(function (p) {
    return p.ft === opp;
  }), w, K, opp);
  return winProb(A, B, +(w.act || {})[s.me] || 0, +(w.act || {})[opp] || 0);
}
var afterMove = function afterMove(s, add, drop) {
  return timedMove(s.players.filter(function (p) {
    return p.ft === s.me;
  }), s.me, [{
    add: add,
    drop: drop
  }]);
};
var WinDelta = function WinDelta(_ref77) {
  var s = _ref77.s,
    add = _ref77.add,
    drop = _ref77.drop,
    base = _ref77.base;
  var b = base === undefined ? winChance(s) : base;
  var n = winChance(s, afterMove(s, add, drop));
  if (b == null || n == null) return null;
  var d = Math.round(n * 100) - Math.round(b * 100);
  return /*#__PURE__*/React.createElement("span", {
    className: "text-xs whitespace-nowrap " + (d > 0 ? "text-green-700" : d < 0 ? "text-red-600" : "text-slate-500"),
    title: "Chance to win this week's matchup, before and after the move"
  }, "win ", wpTxt(b), " \u2192 ", wpTxt(n));
};

// ---------- round 6: moves left, fill slots, ESPN lineup check, goalie streams, strategy (news_logos.py) ----------
var movesLeft = function movesLeft(s, tid, w) {
  var E = window.ESPN_DATA || {};
  if (E.acq && w && w.period != null) {
    var a = E.acq[String(tid).replace(/^t/, "")];
    if (a) return Math.max(0, 3 - (+a[String(w.period)] || 0));
  }
  return tid === s.me ? Math.max(0, 3 - ((s.movesUsed || {})[s.wk] || 0)) : null;
};
var gamesMoves = function gamesMoves(s, tid, w, R) {
  var m = movesLeft(s, tid, w);
  return R.used + " games left" + (m != null ? " · " + m + " move" + (m === 1 ? "" : "s") + " left" : "");
};
var dropFor = function dropFor(s, add) {
  var K = s.blend,
    mine = s.players.filter(function (p) {
      return p.ft === s.me && !p.ir;
    });
  var prot = new Set(_toConsumableArray(mine).sort(function (a, b) {
    return effAvg(b, K) - effAvg(a, K);
  }).slice(0, s.protectTop ?? 8).map(function (p) {
    return p.id;
  }));
  var mins = {
    F: s.minF ?? 10,
    D: s.minD ?? 5,
    G: s.minGo ?? 2
  };
  var cnt = {
    F: 0,
    D: 0,
    G: 0
  };
  mine.forEach(function (p) {
    cnt[p.p]++;
  });
  var pv = function pv(p) {
    return effAvg(p, K) * (p.p === "G" ? p.prob : 1);
  };
  return mine.filter(function (p) {
    return !prot.has(p.id) && !p.keep && (p.p === add.p || cnt[p.p] - 1 >= mins[p.p]);
  }).sort(function (a, b) {
    return pv(a) - pv(b);
  })[0] || null;
};
function GoalieStreams(_ref78) {
  var s = _ref78.s,
    setS = _ref78.setS,
    wk = _ref78.wk;
  // goalies v65: one list of every goalie, any day, yours and free agents marked (news_logos.py)
  var K = s.blend,
    today = todayISO(),
    E = window.ESPN_DATA || {};
  var _useState93 = useState(today),
    _useState94 = _slicedToArray(_useState93, 2),
    day = _useState94[0],
    setDay = _useState94[1];
  var _useState95 = useState({}),
    _useState96 = _slicedToArray(_useState95, 2),
    box = _useState96[0],
    setBox = _useState96[1];
  var _useState97 = useState(null),
    _useState98 = _slicedToArray(_useState97, 2),
    sim = _useState98[0],
    setSim = _useState98[1];
  var touch = React.useRef(null);
  var GD = (window.GAMES_DATA || {}).games || {};
  var minD = ((s.weeks[0] || {}).dates || [])[0] || "2026-09-29";
  var lastG = Object.keys(GD).sort().pop() || addDays(today, 35);
  var maxD = lastG > today ? lastG : today;
  var go = function go(n) {
    var x = addDays(day, n);
    if (x >= minD && x <= maxD) setDay(x);
  };
  useEffect(function () {
    if (day > today || box[day] !== undefined) return;
    var dead = false;
    gxBoxDay(day).then(function (m) {
      if (!dead) setBox(function (b) {
        return _defineProperty({}, day, m || null);
      });
    });
    return function () {
      dead = true;
    };
  }, [day]);
  var played = useMemo(function () {
    var P = pby(),
      out = {};
    var secs = function secs(v) {
      return typeof v === "string" && v.indexOf(":") > 0 ? +v.split(":")[0] * 60 + (+v.split(":")[1] || 0) : +v || 0;
    };
    var add = function add(pid, x, keep) {
      if (!x || x.sv == null) return;
      var p = P["e" + pid] || null,
        t = x.t || p && p.t;
      if (!t || keep && out[t]) return;
      var toi = secs(x.toi);
      if (!out[t] || toi > out[t].toi) out[t] = {
        ...x,
        p: p,
        toi: toi
      };
    };
    Object.entries(box[day] || {}).forEach(function (_ref80) {
      var _ref81 = _slicedToArray(_ref80, 2),
        pid = _ref81[0],
        x = _ref81[1];
      return add(pid, x, false);
    });
    Object.entries((E.pstat || {})[day] || {}).forEach(function (_ref82) {
      var _ref83 = _slicedToArray(_ref82, 2),
        pid = _ref83[0],
        x = _ref83[1];
      return add(pid, x, true);
    });
    return out;
  }, [day, box, E.generated, s.players]);
  var wi = s.weeks.findIndex(function (w) {
    return (w.dates || []).includes(day);
  });
  var sW = wi >= 0 ? {
    ...s,
    wk: wi
  } : s;
  var wkD = useMemo(function () {
    return wi >= 0 ? deriveWeek(s.weeks[wi], s.autoDone) : null;
  }, [wi, s.weeks, s.autoDone]);
  var noMv = !wkD || noMovesWk(s, wkD);
  var M = useMemo(function () {
    return sim ? computeMoves(sW, {
      H: 1,
      pos: "G",
      pool: 40
    }) : null;
  }, [sim, wi]);
  var base = useMemo(function () {
    return sim ? winChance(sW) : null;
  }, [sim, wi]);
  var games = Object.entries(GD[day] || {}).filter(function (_ref84) {
    var _ref85 = _slicedToArray(_ref84, 2),
      v = _ref85[1];
    return v.h === 1;
  }).map(function (_ref86) {
    var _ref87 = _slicedToArray(_ref86, 2),
      home = _ref87[0],
      v = _ref87[1];
    return {
      home: home,
      away: v.o,
      st: v.st || ""
    };
  });
  if (!games.length) {
    var seen = {};
    Object.entries(played).forEach(function (_ref88) {
      var _ref89 = _slicedToArray(_ref88, 2),
        t = _ref89[0],
        x = _ref89[1];
      if (!x.o) return;
      var h = x.h ? t : x.o,
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
  games.sort(function (a, b) {
    return String(a.st).localeCompare(String(b.st)) || a.home.localeCompare(b.home);
  });
  var raw = (E.goalies || s.goalies || {})[day] || {};
  var AIG = (window.__AI || {}).gstart || {};
  var findG = function findG(n) {
    var k = nrm(n);
    return s.players.find(function (p) {
      return p.p === "G" && nrm(p.n) === k;
    }) || null;
  };
  var side = function side(t) {
    var g = gState(t, day),
      x = played[t];
    if (g.s !== "P" && x) {
      var dec = x.dec === "W" ? "W" : x.dec === "L" ? "L" : x.dec === "O" ? "OTL" : g.s === "L" ? "Live" : "";
      var pts = x.fp != null ? x.fp : gxEst(x, s.sc || {});
      return {
        t: t,
        p: x.p,
        name: x.p ? x.p.n : "",
        played: true,
        status: [dec, (x.sv || 0) + " saves", x.ga != null ? x.ga + " GA" : ""].filter(Boolean).join(" \xB7 "),
        col: x.dec === "W" ? "var(--good)" : g.s === "L" ? "var(--warn)" : "var(--mute)",
        val: f1(pts) + (x.fp != null ? " pts" : " pts est.")
      };
    }
    if (g.s !== "P") return {
      t: t,
      p: null,
      name: "",
      status: day < today ? "result not saved" : "in progress",
      col: "var(--mute)",
      val: ""
    };
    var e = Object.entries(raw).find(function (_ref90) {
      var _ref91 = _slicedToArray(_ref90, 2),
        v = _ref91[1];
      return v && v.team === t;
    });
    if (e) {
      var st = String(e[1].status || "").toLowerCase(),
        p = findG(e[0]);
      var w = st.includes("confirm") && !st.includes("un") ? ["confirmed", "var(--good)"] : /likely|expected|project/.test(st) ? ["likely", "var(--warn)"] : ["not confirmed", "var(--warn)"];
      return {
        t: t,
        p: p,
        name: p ? p.n : e[0],
        status: w[0],
        col: w[1],
        val: p ? f1(effAvg(p, K, day)) + " exp" : ""
      };
    }
    var ch = function ch(p) {
      var a = (AIG[String(p.id).slice(1)] || {})[day];
      return a != null ? a : gStart(p, day).v;
    };
    var c = s.players.filter(function (p) {
      return p.p === "G" && p.t === t && !p.ir && avail(p, day) > 0;
    }).map(function (p) {
      return [p, ch(p)];
    }).sort(function (a, b) {
      return b[1] - a[1];
    })[0];
    if (!c) return {
      t: t,
      p: null,
      name: "",
      status: "starter not known",
      col: "var(--mute)",
      val: ""
    };
    return {
      t: t,
      p: c[0],
      name: c[0].n,
      status: Math.round(c[1] * 100) + "% to start",
      col: "var(--mute)",
      val: f1(effAvg(c[0], K, day)) + " exp"
    };
  };
  var rows = games.map(function (gm) {
    return {
      ...gm,
      a: side(gm.away),
      h: side(gm.home)
    };
  });
  var mine = 0,
    fas = 0;
  rows.forEach(function (r) {
    return [r.a, r.h].forEach(function (x) {
      if (x.p) {
        if (x.p.ft === s.me) mine++;else if (x.p.ft === "fa") fas++;
      }
    });
  });
  var mid = function mid(gm) {
    var st = gState(gm.home, day).s;
    if (st === "P") return gm.st ? gameTime({
      st: gm.st
    }) : "";
    var sc = gScore(gm.home, day),
      hx = played[gm.home];
    var hs = sc && sc.my != null ? sc.my : hx && hx.my != null ? hx.my : null;
    var aw = sc && sc.op != null ? sc.op : hx && hx.op != null ? hx.op : null;
    return /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("span", {
      className: "block"
    }, st === "L" ? "Live" : "Final"), hs != null && aw != null ? /*#__PURE__*/React.createElement("span", {
      className: "block",
      style: {
        color: "var(--ink)"
      }
    }, aw + "\u2013" + hs) : null);
  };
  var tag = function tag(p) {
    return !p ? null : p.ft === s.me ? /*#__PURE__*/React.createElement("span", {
      className: "gx-pill me"
    }, "Yours") : p.ft === "fa" ? /*#__PURE__*/React.createElement("span", {
      className: "gx-pill fa"
    }, "Free agent") : /*#__PURE__*/React.createElement("span", {
      className: "text-slate-500"
    }, teamName(s, p.ft));
  };
  var cell = function cell(x, r) {
    var me = !!(x.p && x.p.ft === s.me);
    var dr = x.p && x.p.ft === "fa" && !x.played && !noMv && gState(x.t, day).s === "P" && day >= pickStart(x.p) ? dropFor(s, x.p) : null;
    var nm = x.p ? /*#__PURE__*/React.createElement(PN, {
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
    }, /*#__PURE__*/React.createElement(TeamLogo, {
      t: x.t,
      size: 18
    })), nm, " ", /*#__PURE__*/React.createElement("span", {
      className: "text-xs text-slate-500"
    }, x.t), r ? /*#__PURE__*/React.createElement("span", {
      style: {
        marginLeft: 6
      }
    }, /*#__PURE__*/React.createElement(TeamLogo, {
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
      onClick: function onClick(e) {
        e.stopPropagation();
        setSim({
          add: x.p.id,
          drop: dr.id
        });
      }
    }, "swap for " + lastN(dr.n)) : null));
  };
  var nice = function nice(d) {
    return fromIso(d).toLocaleDateString("en-US", {
      weekday: "short",
      month: "short",
      day: "numeric"
    }).replace(",", "");
  };
  var lbl = day === today ? "Today" : day === addDays(today, 1) ? "Tomorrow" : day === addDays(today, -1) ? "Yesterday" : nice(day);
  var note = [lbl === nice(day) ? "" : nice(day), day < today ? "who started and how they did" : day <= addDays(today, 1) ? "starters from Daily Faceoff" : "projected from recent starts", day >= today && noMv ? "no moves left that week" : ""].filter(Boolean).join(" \xB7 ");
  var nNHL = NHL.filter(function (t) {
    return SCHED[t] && SCHED[t].has(day);
  }).length / 2;
  var onStart = function onStart(e) {
    var t = e.touches[0];
    touch.current = [t.clientX, t.clientY];
  };
  var onEnd = function onEnd(e) {
    var t0 = touch.current,
      t = e.changedTouches[0];
    touch.current = null;
    if (!t0) return;
    var dx = t.clientX - t0[0],
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
    onClick: function onClick() {
      return go(-1);
    }
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
    onClick: function onClick() {
      return setDay(today);
    }
  }, "Back to today") : null), /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: "gx-arw",
    "aria-label": "Later day",
    disabled: day >= maxD,
    onClick: function onClick() {
      return go(1);
    }
  }, "\u203A")), /*#__PURE__*/React.createElement("div", {
    className: "gx-pn",
    "data-r65": "goalies"
  }, /*#__PURE__*/React.createElement("div", {
    className: "gx-tag"
  }, (day < today ? "Who started" : "Every goalie") + " \xB7 " + rows.length + " game" + (rows.length === 1 ? "" : "s")), rows.length ? /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500",
    style: {
      margin: "4px 0 4px"
    }
  }, (mine ? mine + " of yours" : "None of yours") + " \xB7 " + fas + " free agent" + (fas === 1 ? "" : "s")) : null, rows.length ? rows.map(function (gm, i) {
    return /*#__PURE__*/React.createElement("div", {
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
    }, mid(gm)), cell(gm.h, true));
  }) : /*#__PURE__*/React.createElement("div", {
    className: "text-sm text-slate-500",
    style: {
      padding: "10px 0"
    }
  }, nNHL ? day < today ? "Results for this day are not saved." : "Game times for this day are not loaded yet." : "No NHL games this day.")), sim && M && wkD ? /*#__PURE__*/React.createElement(MoveSim, {
    s: sW,
    setS: setS,
    wk: wkD,
    M: M,
    H: 1,
    hLabel: "that week",
    init: sim,
    wBase: base,
    onClose: function onClose() {
      return setSim(null);
    }
  }) : null);
}

// ---------- moves used from ESPN (news_logos.py) ----------
function movesUsedESPN(s, w) {
  var E = window.ESPN_DATA || {};
  if (!E.acq || !w || w.period == null) return null;
  var a = E.acq[String(s.me).replace(/^t/, "")];
  return a ? +a[String(w.period)] || 0 : null;
}

// ---------- round 9: phone layout (news_logos.py) ----------
var M_TABS = [["today", "Today"], ["matchup", "Matchup"], ["myteam", "Team"], ["league", "League"]]; // round 37, older marker kept: ["lines", "Lines"]];
var M_MORE = [["setup", "Settings"], ["news", "News"], ["teams", "Teams"]]; // round 37, older marker kept: const M_MORE = [["teams", "Teams"], ["league"
var M_MODES = [["espn", "ESPN"], ["blend", "Blend"], ["model", "GM model"], ["ai", "AI (beta)"]];
var M_ST = {
  DAY_TO_DAY: "DTD",
  OUT: "Out",
  INJURY_RESERVE: "IR",
  SUSPENSION: "Susp."
};
var shortN = function shortN(n) {
  var x = String(n || "").split(" ");
  return x.length > 1 ? x[0][0] + ". " + x.slice(1).join(" ") : x[0];
};
var mGame = function mGame(p) {
  var g = gameOf(p.t, p.dt);
  return g ? (g.h ? "vs " : "@") + g.o + " " + gameTime(g) : "";
};
var mStart = function mStart(gs) {
  return !gs ? "" : gs.includes("confirmed") && !gs.includes("un") ? "Confirmed" : /not starting|rests|backup/.test(gs) ? "May sit" : /likely/.test(gs) ? "Likely" : "Unconfirmed";
};
function MobileHeader(_ref92) {
  var s = _ref92.s,
    setS = _ref92.setS,
    tab = _ref92.tab,
    go = _ref92.go,
    ageH = _ref92.ageH;
  var _useState99 = useState(false),
    _useState100 = _slicedToArray(_useState99, 2),
    menu = _useState100[0],
    setMenu = _useState100[1];
  var _useState101 = useState(false),
    _useState102 = _slicedToArray(_useState101, 2),
    opts = _useState102[0],
    setOpts = _useState102[1];
  var more = M_MORE.find(function (_ref93) {
    var _ref94 = _slicedToArray(_ref93, 1),
      k = _ref94[0];
    return k === tab;
  });
  var pick = function pick(k) {
    setMenu(false);
    setOpts(false);
    go(k);
  };
  var dot = !s.lastSync ? "var(--faint)" : ageH !== null && ageH > 2 ? "var(--bad)" : "var(--good)";
  var can = function can(k) {
    return k === "espn" || !!window.__MODEL && (k !== "ai" || !!window.__AI);
  };
  var tabBtn = function tabBtn(k, l, on, fn) {
    return /*#__PURE__*/React.createElement("button", {
      key: k,
      onClick: fn,
      className: "m-tab",
      style: {
        color: on ? "var(--ink)" : "var(--mute)",
        borderBottomColor: on ? "var(--accent)" : "transparent"
      }
    }, l);
  };
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
    onChange: function onChange(e) {
      return setS({
        ...s,
        wk: +e.target.value
      });
    }
  }, s.weeks.map(function (w, i) {
    return /*#__PURE__*/React.createElement("option", {
      key: i,
      value: i
    }, (w.label || "").replace(/^Week /, "Wk "));
  })), /*#__PURE__*/React.createElement("button", {
    className: "m-icon",
    "aria-label": "Options",
    onClick: function onClick() {
      setOpts(!opts);
      setMenu(false);
    }
  }, "\u22EF")), opts && /*#__PURE__*/React.createElement("div", {
    className: "px-3 pt-2 pb-1"
  }, /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500 mb-1"
  }, "Projections"), /*#__PURE__*/React.createElement("div", {
    className: "flex gap-2 overflow-x-auto navscroll"
  }, M_MODES.map(function (_ref95) {
    var _ref96 = _slicedToArray(_ref95, 2),
      k = _ref96[0],
      l = _ref96[1];
    return /*#__PURE__*/React.createElement("button", {
      key: k,
      disabled: !can(k),
      onClick: function onClick() {
        return setS({
          ...s,
          pmode: k,
          players: _toConsumableArray(s.players)
        });
      },
      className: "px-3 py-1 rounded-full text-sm border whitespace-nowrap " + (window.__PMODE === k ? "bg-blue-600 border-blue-600" : "border-slate-300 text-slate-600") + (can(k) ? "" : " opacity-40")
    }, l);
  })), /*#__PURE__*/React.createElement("div", {
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
  }, M_TABS.map(function (_ref97) {
    var _ref98 = _slicedToArray(_ref97, 2),
      k = _ref98[0],
      l = _ref98[1];
    return tabBtn(k, l, (tab === k || k === "myteam" && (tab === "moves" || tab === "lines")) && !menu || k === "league" && tab === "teams", function () {
      return k === "league" ? (setMenu(false), setOpts(false), go("league", "power")) : pick(k);
    });
  }), tabBtn("setup", "Setup", tab === "setup" || tab === "news", function () {
    setMenu(false);
    setOpts(false);
    go("setup", "settings");
  })), menu && /*#__PURE__*/React.createElement("div", {
    className: "border-t border-slate-800"
  }, M_MORE.map(function (_ref99) {
    var _ref100 = _slicedToArray(_ref99, 2),
      k = _ref100[0],
      l = _ref100[1];
    return /*#__PURE__*/React.createElement("button", {
      key: k,
      onClick: function onClick() {
        return pick(k);
      },
      className: "block w-full text-left px-4 py-3 border-b border-slate-800",
      style: {
        color: tab === k ? "var(--accent)" : "var(--ink)"
      }
    }, l);
  })));
}
// ---------- round 10: one trade builder (analyzer + 2-for-1 + best waiver pickup) (news_logos.py) ----------
var Dlt = function Dlt(_ref101) {
  var v = _ref101.v;
  return /*#__PURE__*/React.createElement("span", {
    className: "font-semibold " + (v >= 0 ? "text-green-700" : "text-red-600")
  }, v >= 0 ? "+" : "", f1(v));
};
var tbFlags = function tbFlags(p, K) {
  var f = [],
    g = sigOf(p),
    l = g.luck,
    id = typeof p.id === "string" && p.id[0] === "e" ? p.id.slice(1) : null;
  var mb = window.__MODEL && id ? (window.__MODEL.base || {})[id] : null;
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
function TradeBuilder(_ref102) {
  var s = _ref102.s,
    initPartner = _ref102.initPartner;
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
  var K = s.blend,
    today = todayISO();
  var others = s.teams.filter(function (t) {
    return t.id !== s.me;
  });
  var _useState103 = useState(function () {
      var v = window.__TRADE_P || null;
      window.__TRADE_P = null;
      return v;
    }),
    _useState104 = _slicedToArray(_useState103, 1),
    tp0 = _useState104[0];
  var tpThem = tp0 && tp0.ft !== s.me && tp0.ft !== "fa";
  var _useState105 = useState((tpThem ? tp0.ft : null) || initPartner || (others[0] || {}).id || ""),
    _useState106 = _slicedToArray(_useState105, 2),
    partner = _useState106[0],
    setPartner = _useState106[1];
  var _useState107 = useState(tp0 && tp0.ft === s.me && tp0.id ? [tp0.id] : []),
    _useState108 = _slicedToArray(_useState107, 2),
    give = _useState108[0],
    setGive = _useState108[1];
  var _useState109 = useState(tpThem && tp0.id ? [tp0.id] : []),
    _useState110 = _slicedToArray(_useState109, 2),
    get = _useState110[0],
    setGet = _useState110[1];
  useEffect(function () {
    var h = function h() {
      var v = window.__TRADE_P;
      window.__TRADE_P = null;
      if (!v) return;
      if (v.ft === s.me) {
        if (v.id) setGive(function (g) {
          return g.indexOf(v.id) >= 0 ? g : g.concat([v.id]);
        });
      } else if (v.ft !== "fa") {
        setPartner(v.ft);
        setGet(v.id ? [v.id] : []);
      }
    };
    window.addEventListener("gm-trade", h);
    return function () {
      return window.removeEventListener("gm-trade", h);
    };
  }, []);
  var _useState111 = useState({}),
    _useState112 = _slicedToArray(_useState111, 2),
    pick = _useState112[0],
    setPick = _useState112[1];
  var _useState113 = useState(-1),
    _useState114 = _slicedToArray(_useState113, 2),
    edit = _useState114[0],
    setEdit = _useState114[1];
  var _useState115 = useState("me"),
    _useState116 = _slicedToArray(_useState115, 2),
    side = _useState116[0],
    setSide = _useState116[1];
  var _useState117 = useState([]),
    _useState118 = _slicedToArray(_useState117, 2),
    dropSel = _useState118[0],
    setDropSel = _useState118[1];
  var _useState119 = useState(false),
    _useState120 = _slicedToArray(_useState119, 2),
    dropAll = _useState120[0],
    setDropAll = _useState120[1];
  var nR = s.weeks.length - s.wk;
  var mins = {
    F: s.minF ?? 10,
    D: s.minD ?? 5,
    G: s.minGo ?? 2
  };
  var order = {
    F: 0,
    D: 1,
    G: 2
  };
  var mine = s.players.filter(function (p) {
    return p.ft === s.me;
  });
  var theirs = s.players.filter(function (p) {
    return p.ft === partner;
  });
  var pg = function pg(p) {
    return effAvg(p, K) * (p.p === "G" ? p.prob : 1);
  };
  var vv = function vv(p) {
    return effAvg0(p, K) * (p.p === "G" ? p.prob : 1);
  };
  var gl = function gl(p) {
    return _toConsumableArray(SCHED[p.t] || []).filter(function (d) {
      return d >= today && avail(p, d) > 0;
    }).length;
  };
  var cnt = function cnt(r) {
    var c = {
      F: 0,
      D: 0,
      G: 0
    };
    r.forEach(function (p) {
      if (!p.ir) c[p.p]++;
    });
    return c;
  };
  var tv = useMemo(function () {
    var o = {};
    s.players.forEach(function (p) {
      if (p.ft !== "fa" || p.proj !== false || p.gp > 0) o[p.id] = rosRaw(p, K);
    });
    return o;
  }, [s.players, K, window.__PMODE]);
  var fas = useMemo(function () {
    return s.players.filter(function (p) {
      return p.ft === "fa" && p.prob > 0 && tv[p.id] > 0 && !goalieOut(p);
    }).sort(function (a, b) {
      return tv[b.id] - tv[a.id];
    }).slice(0, 60);
  }, [tv]);
  var rep = useMemo(function () {
    var o = {};
    ["F", "D", "G"].forEach(function (k) {
      var l = s.players.filter(function (p) {
        return p.ft === "fa" && p.p === k && p.prob > 0 && (p.proj !== false || p.gp > 0);
      }).map(vv).sort(function (a, b) {
        return b - a;
      }).slice(0, 5);
      o[k] = l.length ? l.reduce(function (a, b) {
        return a + b;
      }, 0) / l.length : 0;
    });
    return o;
  }, [s.players, K]);
  var pe = function pe(p) {
    return Math.max(0, vv(p) - (rep[p.p] || 0)) * gl(p);
  };
  var Gv = mine.filter(function (p) {
      return give.includes(p.id);
    }),
    Rv = theirs.filter(function (p) {
      return get.includes(p.id);
    });
  // round 59: roster spots are counted by active players (22) and one IR spot, a few lines down
  var ready = Gv.length > 0 && Rv.length > 0;
  // round 59: one IR spot each. An injured player who arrives when your IR spot is taken uses an active spot.
  var irOpen59 = Math.max(0, 1 - mine.filter(function (p) {
    return p.ir && !give.includes(p.id);
  }).length);
  var myAfter0 = mine.filter(function (p) {
    return !give.includes(p.id);
  }).concat(Rv.map(function (p) {
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
  var act0 = mine.filter(function (p) {
      return !p.ir;
    }).length,
    act1 = myAfter0.filter(function (p) {
      return !p.ir;
    }).length;
  var need = Math.max(0, act1 - 22),
    extra = Math.max(0, Math.min(act0, 22) - act1);
  var irIn = Rv.filter(function (p) {
    return p.ir && myAfter0.some(function (x) {
      return x.id === p.id && !x.ir;
    });
  });
  var thIrOpen = Math.max(0, 1 - theirs.filter(function (p) {
    return p.ir && !get.includes(p.id);
  }).length);
  var thOver = Math.max(0, theirs.filter(function (p) {
    return !p.ir && !get.includes(p.id);
  }).length + Gv.filter(function (p) {
    return !p.ir;
  }).length + Math.max(0, Gv.filter(function (p) {
    return p.ir;
  }).length - thIrOpen) - 22);
  // free agents for the spots you free: your choice, or the best one available
  var picks = [];
  var _loop4 = function _loop4(k) {
    if (pick[k] === "none") {
      picks.push(null);
      return 1; // continue
    }
    var f = (pick[k] ? s.players.find(function (f) {
      return f.ft === "fa" && f.id === pick[k];
    }) : null) || null;
    if (!f) {
      var c = cnt(myAfter0.concat(picks.filter(Boolean))),
        short = ["F", "D", "G"].filter(function (x) {
          return c[x] < mins[x];
        });
      f = fas.find(function (x) {
        return !picks.some(function (y) {
          return y && y.id === x.id;
        }) && (!short.length || short.includes(x.p));
      }) || null;
    }
    picks.push(f);
  };
  for (var k = 0; k < extra; k++) {
    if (_loop4(k)) continue;
  }
  // round 59: you choose who to drop. The lowest expected players that keep your position minimums are picked to start.
  var dropPool = myAfter0.filter(function (p) {
    return !p.ir && !get.includes(p.id);
  }).sort(function (a, b) {
    return pg(a) - pg(b);
  });
  var drops = [];
  if (need) {
    var c59 = cnt(myAfter0);
    dropSel.forEach(function (id) {
      var p = dropPool.find(function (x) {
        return x.id === id;
      });
      if (p && drops.length < need && drops.indexOf(p) < 0) {
        drops.push(p);
        c59[p.p]--;
      }
    });
    dropPool.forEach(function (p) {
      if (drops.length < need && drops.indexOf(p) < 0 && c59[p.p] - 1 >= mins[p.p]) {
        drops.push(p);
        c59[p.p]--;
      }
    });
    dropPool.forEach(function (p) {
      if (drops.length < need && drops.indexOf(p) < 0) drops.push(p);
    });
  }
  var key = [partner, give.join(), get.join(), picks.map(function (f) {
    return f ? f.id : "-";
  }).join(), drops.map(function (p) {
    return p.id;
  }).join()].join("|");
  var res = useMemo(function () {
    if (!ready) return null;
    var dropIds = new Set(drops.map(function (p) {
        return p.id;
      })),
      got = picks.filter(Boolean).map(function (f) {
        return {
          ...f,
          ft: s.me
        };
      });
    var after = myAfter0.filter(function (p) {
      return !dropIds.has(p.id);
    }).concat(got);
    var thAfter = theirs.filter(function (p) {
      return !get.includes(p.id);
    }).concat(Gv.map(function (p) {
      return {
        ...p,
        ft: partner
      };
    }));
    var live59 = function live59(r) {
      return r.map(function (p) {
        return p.ir ? {
          ...p,
          ir: false
        } : p;
      });
    }; // round 59: injured players count from their return date, for both teams
    var my = horizonTotal(live59(after), s, nR) - horizonTotal(live59(mine), s, nR),
      th = horizonTotal(live59(thAfter), s, nR) - horizonTotal(live59(theirs), s, nR);
    var G = new Set(give),
      T = new Set(get),
      A = new Set(got.map(function (f) {
        return f.id;
      }));
    var players = s.players.map(function (p) {
      return G.has(p.id) ? {
        ...p,
        ft: partner
      } : T.has(p.id) || A.has(p.id) ? {
        ...p,
        ft: s.me
      } : dropIds.has(p.id) ? {
        ...p,
        ft: "fa"
      } : p;
    });
    var pos = function pos(t) {
      return {
        o: t.rows.findIndex(function (x) {
          return x.t.id === s.me;
        }) + 1,
        ...(t.grpRank[s.me] || {})
      };
    };
    var keep = __LT,
      t2 = leagueTable({
        ...s,
        players: players
      });
    __LT = keep;
    var rb = pos(leagueTable(s)),
      ra = pos(t2);
    var sN = nextWkS(s),
      hasOpp = sN && oppOf(sN.weeks[sN.wk] || {}, s.me);
    var wb = hasOpp ? winChance(sN) : null,
      wa = hasOpp ? winChance(sN, after) : null;
    var c = cnt(after);
    return {
      my: my,
      th: th,
      rb: rb,
      ra: ra,
      wb: wb,
      wa: wa,
      short: ["F", "D", "G"].filter(function (k) {
        return c[k] < mins[k];
      })
    };
  }, [key, s.players, s.wk, K, window.__PMODE]);
  var sum = function sum(l, f) {
    return l.reduce(function (a, p) {
      return a + f(p);
    }, 0);
  };
  var peG = sum(Gv, pe),
    peR = sum(Rv, pe),
    theyThink = peR > 0 ? (peG - peR) / peR : 0;
  var toggle = function toggle(sel, set, id) {
    set(sel.includes(id) ? sel.filter(function (x) {
      return x !== id;
    }) : [].concat(_toConsumableArray(sel), [id]));
    setPick({});
    setEdit(-1);
  };
  var vd = !res ? null : res.my <= 0 ? ["Bad for you", "var(--bad)", "Your lineup gets worse."] : theyThink >= -0.05 ? ["Good trade", "var(--good)", "You gain, and it should look fair to them."] : ["Good for you, hard to sell", "var(--warn)", "You gain, but they would see it as a loss. Expect a counter-offer."];
  var GN = {
    F: "forwards",
    D: "defence",
    G: "goalies"
  };
  var grp = res ? ["F", "D", "G"].map(function (k) {
    return [k, (res.rb[k] || 0) - (res.ra[k] || 0)];
  }).sort(function (a, b) {
    return Math.abs(b[1]) - Math.abs(a[1]);
  })[0] : null;
  var arrow = function arrow(b, a, fmt, up) {
    return /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("span", null, fmt(b)), /*#__PURE__*/React.createElement("span", {
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
  };
  var offerRow = function offerRow(p, i, onX, note) {
    return /*#__PURE__*/React.createElement("div", {
      key: p.id,
      className: "gx-row",
      style: i ? null : {
        borderTop: 0
      }
    }, /*#__PURE__*/React.createElement(TeamLogo, {
      t: p.t,
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
    }, "\xD7"));
  };
  var rosterRows = function rosterRows(list, sel, set, mySide) {
    return _toConsumableArray(list).sort(function (a, b) {
      return (a.ir ? 1 : 0) - (b.ir ? 1 : 0) || order[a.p] - order[b.p] || pg(b) - pg(a);
    }).map(function (p) {
      var on = sel.includes(p.id),
        fl = mySide ? null : tbFlags(p, K).find(function (f) {
          return !f.sell;
        }); // round 59: no sell-high tags
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
        onClick: function onClick() {
          return toggle(sel, set, p.id);
        }
      }, /*#__PURE__*/React.createElement(TeamLogo, {
        t: p.t,
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
      }, p.p + (p.ir ? " \xB7 IR" : "")), fl ? /*#__PURE__*/React.createElement("span", {
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
  };
  return /*#__PURE__*/React.createElement("div", {
    className: "space-y-3"
  }, /*#__PURE__*/React.createElement("div", {
    className: "flex items-center gap-2"
  }, /*#__PURE__*/React.createElement("span", {
    className: "text-sm text-slate-500 whitespace-nowrap"
  }, "Trade with"), /*#__PURE__*/React.createElement("select", {
    className: inp + " flex-1",
    value: partner,
    onChange: function onChange(e) {
      setPartner(e.target.value);
      setGet([]);
      setPick({});
      setEdit(-1);
    }
  }, others.map(function (t) {
    return /*#__PURE__*/React.createElement("option", {
      key: t.id,
      value: t.id
    }, t.name);
  })), give.length || get.length ? /*#__PURE__*/React.createElement("button", {
    className: "text-xs text-slate-500 underline whitespace-nowrap",
    onClick: function onClick() {
      setGive([]);
      setGet([]);
      setPick({});
      setEdit(-1);
    }
  }, "Clear") : null), /*#__PURE__*/React.createElement("div", {
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
  }, "You give"), Gv.length ? Gv.map(function (p, i) {
    return offerRow(p, i, function () {
      return toggle(give, setGive, p.id);
    });
  }) : /*#__PURE__*/React.createElement("div", {
    className: "text-sm text-slate-500"
  }, "Tap your players below")), /*#__PURE__*/React.createElement("div", {
    className: "gx-pn",
    style: {
      minWidth: 0
    }
  }, /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("div", {
    className: "gx-tag",
    style: {
      marginBottom: 4
    }
  }, "You get"), Rv.length ? Rv.map(function (p, i) {
    return offerRow(p, i, function () {
      return toggle(get, setGet, p.id);
    });
  }) : /*#__PURE__*/React.createElement("div", {
    className: "text-sm text-slate-500"
  }, "Tap their players below"), picks.map(function (f, k) {
    return f ? offerRow(f, 1, function () {
      setPick(function (x) {
        return _defineProperty({}, k, "none");
      });
      setEdit(-1);
    }, /*#__PURE__*/React.createElement(React.Fragment, null, "free agent ", /*#__PURE__*/React.createElement("button", {
      type: "button",
      className: "text-blue-600",
      style: {
        marginLeft: 6
      },
      onClick: function onClick(e) {
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
      onClick: function onClick() {
        return setPick(function (x) {
          return _defineProperty({}, k, undefined);
        });
      }
    }, "Add a free agent to the open spot") : null;
  }), edit >= 0 && edit < extra ? /*#__PURE__*/React.createElement(FaSearch, {
    s: s,
    top: fas,
    taken: new Set(picks.filter(Boolean).map(function (x) {
      return x.id;
    })),
    val: pg,
    onPick: function onPick(id) {
      setPick(function (x) {
        return _defineProperty({}, edit, id);
      });
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
  }, "This trade leaves you with " + act1 + " active players and the limit is 22." + (Gv.some(function (p) {
    return p.ir;
  }) ? " " + Gv.filter(function (p) {
    return p.ir;
  }).map(function (p) {
    return p.n;
  }).join(" and ") + (Gv.filter(function (p) {
    return p.ir;
  }).length === 1 ? " is on IR, so trading him does not open a spot." : " are on IR, so trading them does not open a spot.") : "")), /*#__PURE__*/React.createElement("div", {
    style: {
      marginTop: 8
    }
  }, dropPool.filter(function (p, i) {
    return dropAll || i < 5 || drops.indexOf(p) >= 0;
  }).map(function (p, i) {
    var on = drops.indexOf(p) >= 0;
    return /*#__PURE__*/React.createElement("div", {
      key: p.id,
      className: "gx-row",
      style: i ? null : {
        borderTop: 0
      }
    }, /*#__PURE__*/React.createElement(TeamLogo, {
      t: p.t,
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
      onClick: function onClick() {
        if (!on) setDropSel(drops.map(function (x) {
          return x.id;
        }).concat([p.id]).slice(-need));
      }
    }, on ? "Dropping" : "Drop"));
  })), dropPool.length > 5 ? /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: "text-xs text-blue-600",
    style: {
      marginTop: 8
    },
    onClick: function onClick() {
      return setDropAll(!dropAll);
    }
  }, dropAll ? "Show fewer" : "Show all my players") : null, /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500",
    style: {
      marginTop: 8
    }
  }, "The result below counts " + drops.map(function (p) {
    return p.n;
  }).join(" and ") + " as dropped. Lowest expected points are listed first.")) : null, res && vd ? /*#__PURE__*/React.createElement("div", {
    className: "gx-pn"
  }, /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("div", {
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
  }, "Your league rank"), /*#__PURE__*/React.createElement("div", {
    className: "gx-stv"
  }, arrow(res.rb.o, res.ra.o, ordN, res.rb.o - res.ra.o)), /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500"
  }, grp && grp[1] ? GN[grp[0]] + " " + ordN(res.rb[grp[0]]) + " \u2192 " + ordN(res.ra[grp[0]]) : "position ranks unchanged")), res.wb != null && res.wa != null ? /*#__PURE__*/React.createElement("div", {
    className: "gx-stc"
  }, /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500"
  }, "Next week"), /*#__PURE__*/React.createElement("div", {
    className: "gx-stv"
  }, arrow(res.wb, res.wa, wpTxt, Math.round(res.wa * 100) - Math.round(res.wb * 100))), /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500"
  }, "chance to win")) : null), res.short.length ? /*#__PURE__*/React.createElement("div", {
    className: "text-sm",
    style: {
      marginTop: 10,
      color: "var(--bad)"
    }
  }, "This leaves you short at ", res.short.map(function (k) {
    return GN[k];
  }).join(" and "), ".") : null, /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500",
    "data-r59": "after",
    style: {
      marginTop: 10
    }
  }, "Your roster after: " + (act1 - drops.length + picks.filter(Boolean).length) + " of 22 active." + (irIn.length ? " Your IR spot is taken, so " + irIn.map(function (p) {
    return p.n;
  }).join(" and ") + " would use an active spot." : "") + (thOver > 0 ? " " + teamName(s, partner) + " would be over 22 and would have to drop " + thOver + " too." : ""))) : /*#__PURE__*/React.createElement("div", {
    className: "text-sm text-slate-500"
  }, "Pick at least one player on each side to see the result."), /*#__PURE__*/React.createElement("div", {
    className: "gx-pn"
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
    onClick: function onClick() {
      return setSide("me");
    }
  }, teamName(s, s.me)), /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: side === "them" ? "on" : "",
    onClick: function onClick() {
      return setSide("them");
    }
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
  }, teamName(s, partner)), rosterRows(theirs, get, setGet, false)))), /*#__PURE__*/React.createElement(TradeAdvice, {
    s: s,
    onPick: function onPick(p) {
      setPartner(p.ft);
      setGet(p.ft === partner ? [].concat(_toConsumableArray(get.filter(function (x) {
        return x !== p.id;
      })), [p.id]) : [p.id]);
      setPick({});
      setEdit(-1);
      window.scrollTo(0, 0);
    }
  }));
}

// ---------- round 14: My Team injuries + protected players (news_logos.py) ----------
function MyInjProt(_ref106) {
  var s = _ref106.s,
    setS = _ref106.setS,
    wk = _ref106.wk;
  var K = s.blend,
    today = todayISO();
  var _useState121 = useState(null),
    _useState122 = _slicedToArray(_useState121, 2),
    edit = _useState122[0],
    setEdit = _useState122[1];
  var _useState123 = useState(false),
    _useState124 = _slicedToArray(_useState123, 2),
    adv = _useState124[0],
    setAdv = _useState124[1];
  var roster = s.players.filter(function (p) {
    return p.ft === s.me;
  });
  var upd = function upd(id, patch) {
    return setS(function (st) {
      return {
        ...st,
        players: st.players.map(function (p) {
          return p.id === id ? {
            ...p,
            ...patch
          } : p;
        })
      };
    });
  };
  var out = roster.filter(function (p) {
    var b = effBack(p).d;
    return p.ir || b && b > today || !b && avail(p, today) === 0 || p.status && p.status !== "ACTIVE";
  }).sort(function (a, b) {
    return (effBack(a).d || "9999") < (effBack(b).d || "9999") ? -1 : 1;
  });
  var top = s.protectTop ?? 8;
  var healthy = roster.filter(function (p) {
    return !p.ir;
  }).sort(function (a, b) {
    return effAvg(b, K) - effAvg(a, K);
  });
  var auto = healthy.slice(0, top),
    autoIds = new Set(auto.map(function (p) {
      return p.id;
    }));
  var mine = healthy.filter(function (p) {
    return p.keep && !autoIds.has(p.id);
  });
  var addable = healthy.filter(function (p) {
    return !autoIds.has(p.id) && !p.keep;
  });
  var ST = {
    DAY_TO_DAY: "Day-to-day",
    OUT: "Out",
    INJURY_RESERVE: "IR",
    SUSPENSION: "Suspended"
  };
  var stTxt = function stTxt(p) {
    return p.ir ? "IR" : ST[p.status] || (p.status || "Out").replace(/_/g, " ");
  };
  var SRC = {
    you: "your date",
    ESPN: "from ESPN",
    news: "from injury news",
    estimate: "estimate"
  };
  var chip = "inline-flex items-center gap-1.5 pl-1.5 pr-2.5 py-1 rounded-full border text-sm ";
  var backTxt = function backTxt(p, b) {
    if (!b) return "No return date yet";
    if (b <= today) return "Available now";
    var n = Math.round((fromIso(b) - fromIso(today)) / 864e5);
    var miss = (wk.dates || []).filter(function (d, i) {
      return d >= today && d < b && (wk.games[p.t] || []).includes(i);
    }).length;
    return "Back " + mdL(b) + " (" + n + " day" + (n === 1 ? "" : "s") + ")" + (miss ? " · misses " + miss + " game" + (miss === 1 ? "" : "s") + " this week" : "");
  };
  return /*#__PURE__*/React.createElement("div", {
    className: "space-y-4"
  }, /*#__PURE__*/React.createElement("div", {
    className: "grid md:grid-cols-2 gap-4 items-start"
  }, /*#__PURE__*/React.createElement(Section, {
    title: "Injuries",
    sub: "Return dates come from ESPN. Change one only if you know better."
  }, out.length ? out.map(function (p) {
    var eb = effBack(p);
    return /*#__PURE__*/React.createElement("div", {
      key: p.id,
      className: "flex items-center gap-3 py-3 border-t border-slate-100"
    }, /*#__PURE__*/React.createElement(TeamLogo, {
      t: p.t,
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
      onClick: function onClick() {
        return upd(p.id, {
          back: DEFAULT_BACK[p.n] || ""
        });
      }
    }, "Reset") : null), edit === p.id ? /*#__PURE__*/React.createElement("div", {
      className: "flex items-center gap-2 mt-2"
    }, /*#__PURE__*/React.createElement("input", {
      type: "date",
      className: inp,
      value: eb.d,
      onChange: function onChange(e) {
        return upd(p.id, {
          back: e.target.value
        });
      }
    }), /*#__PURE__*/React.createElement("button", {
      className: "text-sm text-blue-600",
      onClick: function onClick() {
        return setEdit(null);
      }
    }, "Done")) : null), edit === p.id ? null : /*#__PURE__*/React.createElement("button", {
      className: "text-sm text-blue-600 whitespace-nowrap",
      onClick: function onClick() {
        return setEdit(p.id);
      }
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
    onChange: function onChange(e) {
      return setS(function (st) {
        return {
          ...st,
          protectTop: +e.target.value
        };
      });
    }
  }, _toConsumableArray(Array(13)).map(function (_, n) {
    return /*#__PURE__*/React.createElement("option", {
      key: n,
      value: n
    }, n);
  })), /*#__PURE__*/React.createElement("span", null, "players")), auto.length ? /*#__PURE__*/React.createElement("div", {
    className: "mt-3 flex flex-wrap gap-2"
  }, auto.map(function (p) {
    return /*#__PURE__*/React.createElement("span", {
      key: p.id,
      className: chip + "border-slate-200 text-slate-600"
    }, /*#__PURE__*/React.createElement(TeamLogo, {
      t: p.t,
      size: 18
    }), p.n);
  })) : null, /*#__PURE__*/React.createElement("div", {
    className: "text-xs uppercase tracking-wide text-slate-500 mt-4 mb-2"
  }, "Also protect"), /*#__PURE__*/React.createElement("div", {
    className: "flex flex-wrap gap-2 items-center"
  }, mine.map(function (p) {
    return /*#__PURE__*/React.createElement("span", {
      key: p.id,
      className: chip + "border-green-300 bg-green-50"
    }, /*#__PURE__*/React.createElement(TeamLogo, {
      t: p.t,
      size: 18
    }), p.n, /*#__PURE__*/React.createElement("button", {
      className: "text-slate-500 ml-1 text-base leading-none",
      "aria-label": "Unprotect " + p.n,
      onClick: function onClick() {
        return upd(p.id, {
          keep: false
        });
      }
    }, "\xD7"));
  }), addable.length ? /*#__PURE__*/React.createElement("select", {
    className: inp,
    value: "",
    onChange: function onChange(e) {
      if (e.target.value) upd(e.target.value, {
        keep: true
      });
    }
  }, /*#__PURE__*/React.createElement("option", {
    value: ""
  }, "+ Add a player"), addable.map(function (p) {
    return /*#__PURE__*/React.createElement("option", {
      key: p.id,
      value: p.id
    }, p.n, " (", p.p, ")");
  })) : null))), /*#__PURE__*/React.createElement("div", {
    className: "px-1"
  }, /*#__PURE__*/React.createElement("button", {
    className: "text-sm text-blue-600",
    onClick: function onClick() {
      return setAdv(!adv);
    }
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
var ESLOT = {
  3: "F",
  4: "D",
  6: "UTIL",
  5: "G"
};
var CAPK = {
  F: "F",
  D: "D",
  UTIL: "U",
  G: "G"
};
var __PB = null,
  __NG = null;
var pby = function pby() {
  var L = window.__PLAYERS || [];
  if (!__PB || __PB.k !== L) __PB = {
    k: L,
    m: Object.fromEntries(L.map(function (p) {
      return [p.id, p];
    }))
  };
  return __PB.m;
};
var actDay = function actDay(tid, dt) {
  var D = ((window.ESPN_DATA || {}).daily || {})[dt];
  return D ? D[String(tid).replace(/^t/, "")] || null : null;
};
var gState = function gState(t, dt) {
  var x = ((window.__LIVESC || {})[dt] || {})[t] || (((window.ESPN_DATA || {}).gstate || {})[dt] || {})[t];
  if (x && x.s === "F") return {
    s: "F",
    f: 1
  };
  if (x && x.s === "L") return {
    s: "L",
    f: x.f || 0
  };
  var g = gameOf(t, dt),
    st = g && g.st ? Date.parse(g.st) : NaN;
  if (!isNaN(st)) {
    var el = (Date.now() - st) / 36e5;
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
var gScore = function gScore(t, dt) {
  var L = ((window.__LIVESC || {})[dt] || {})[t];
  return L || (((window.ESPN_DATA || {}).gstate || {})[dt] || {})[t] || null;
};
var LiveTag = function LiveTag(_ref107) {
  var st = _ref107.st,
    t = _ref107.t,
    dt = _ref107.dt;
  // live tag v21: pill + score from the player's team's side (news_logos.py)
  if (st !== "L" && st !== "F") return null;
  var sc = t && dt ? gScore(t, dt) : null;
  var has = !!(sc && sc.my != null && sc.op != null);
  var res = has && st === "F" ? sc.my > sc.op ? "W" : sc.my < sc.op ? "L" : "" : "";
  var tail = !sc ? "" : st === "F" ? sc.per === "OT" || sc.per === "SO" ? " " + sc.per : "" : sc.int ? " · " + sc.per + " int." : sc.per ? " · " + sc.per + (sc.clk ? " " + sc.clk : "") : "";
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
  var E = window.ESPN_DATA || {},
    key = [E.generated, K, window.__PMODE, window.__PLAYERS];
  if (__NG && __NG.k.every(function (v, i) {
    return v === key[i];
  })) return __NG.m;
  var P = pby(),
    acc = {};
  Object.entries(E.daily || {}).forEach(function (_ref108) {
    var _ref109 = _slicedToArray(_ref108, 2),
      dt = _ref109[0],
      T = _ref109[1];
    return Object.values(T || {}).forEach(function (tm) {
      return Object.entries(tm || {}).forEach(function (_ref110) {
        var _ref111 = _slicedToArray(_ref110, 2),
          pid = _ref111[0],
          v = _ref111[1];
        var p = P["e" + pid];
        if (!p || !v || v[0] == null || !(SCHED[p.t] && SCHED[p.t].has(dt)) || gState(p.t, dt).s !== "F") return;
        var a = acc[p.id] = acc[p.id] || {
          s: 0,
          n: 0,
          seen: {}
        };
        if (a.seen[dt]) return;
        a.seen[dt] = 1;
        a.s += v[0] - effAvg(p, K, dt);
        a.n++;
      });
    });
  });
  var m = {};
  Object.entries(acc).forEach(function (_ref112) {
    var _ref113 = _slicedToArray(_ref112, 2),
      id = _ref113[0],
      a = _ref113[1];
    var b = effAvg(P[id], K);
    if (!(b > 0) || !a.n) return;
    var adj = Math.max(-0.15, Math.min(0.15, 0.1 * a.s / a.n / b));
    if (Math.abs(adj) >= 0.005) m[id] = 1 + adj;
  });
  __NG = {
    k: key,
    m: m
  };
  return m;
}
function weekLive(roster, wk, K, tid, opt) {
  // live week v16: real points for games that started (ESPN lineup), projection for everything still to come
  var dates = wk.dates || [],
    ng = liveNudges(K),
    P = pby(),
    today = todayISO();
  var r = roster.map(function (p) {
    return ng[p.id] ? {
      ...p,
      gwMul: (p.gwMul || 1) * ng[p.id]
    } : p;
  });
  var byId = {};
  r.forEach(function (p) {
    return byId[p.id] = p;
  });
  var actSoFar = 0,
    projSoFar = 0;
  var days = wk.days.map(function (_, d) {
    var dt = dates[d];
    var plays = function plays(p) {
      return (wk.games[p.t] || []).includes(d);
    };
    var lk = function lk(p) {
      return !!dt && plays(p) && gState(p.t, dt).s !== "P";
    };
    var full = opt && opt.detail ? dayLineup(roster.filter(function (p) {
      return onEspnDay(dt ? actDay(tid, dt) : null, p);
    }), wk, d, K).total : null;
    var AD = dt ? actDay(tid, dt) : null;
    var adAct = AD ? Object.entries(AD).filter(function (_ref114) {
      var _ref115 = _slicedToArray(_ref114, 2),
        v = _ref115[1];
      return v && ESLOT[v[1]];
    }) : [];
    if (!dt || !r.some(lk) && !adAct.some(function (_ref116) {
      var _ref117 = _slicedToArray(_ref116, 2),
        v = _ref117[1];
      return v[0] != null;
    })) {
      var _L = dayLineup(r.filter(function (p) {
        return onEspnDay(AD, p);
      }), wk, d, K);
      return {
        ..._L,
        act: 0,
        proj: full != null ? full : _L.total,
        locked: 0,
        liveN: 0,
        openN: _L.start.length,
        allDone: !!dt && dt < today,
        benchAct: [],
        empty: dt && dt < today ? 0 : _L.empty
      };
    }
    var cap = {
        F: 9,
        D: 5,
        U: 1,
        G: 2
      },
      rows = [],
      done = new Set();
    var act = 0;
    var take = function take(p, pp, slot, a, assume) {
      var g = gState(p.t, dt),
        gs = p.p === "G" ? gStart(p, dt) : null;
      var base = function base(q) {
        return effAvg(q, K, dt) * (a != null ? 1 : (gs ? gs.v : p.prob) * avail(p, dt));
      };
      var x0 = base(pp),
        playing = assume || a != null || g.s === "L" && g.f < 0.3;
      var vf = g.s === "L" && playing ? 1 - g.f : 0;
      rows.push({
        ...pp,
        slot: slot,
        st: g.s,
        a: a,
        x0: x0,
        x: x0 * vf,
        vf: vf,
        dt: dt,
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
      adAct.forEach(function (_ref118) {
        var _ref119 = _slicedToArray(_ref118, 2),
          pid = _ref119[0],
          v = _ref119[1];
        var p = P["e" + pid];
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
      dayLineup(r, wk, d, K).start.filter(lk).forEach(function (q) {
        var raw = roster.find(function (x) {
          return x.id === q.id;
        }) || q;
        take(raw, byId[q.id] || raw, q.slot, null, true);
      });
    }
    var benchAct = AD ? Object.entries(AD).filter(function (_ref120) {
      var _ref121 = _slicedToArray(_ref120, 2),
        v = _ref121[1];
      return v && v[1] === 7 && v[0];
    }).map(function (_ref122) {
      var _ref123 = _slicedToArray(_ref122, 2),
        pid = _ref123[0],
        v = _ref123[1];
      return {
        p: P["e" + pid],
        a: v[0]
      };
    }).filter(function (x) {
      return x.p && gState(x.p.t, dt).s !== "P";
    }) : [];
    Object.keys(cap).forEach(function (k) {
      return cap[k] = Math.max(0, cap[k]);
    });
    var L = dayLineup(r.filter(function (p) {
      return onEspnDay(AD, p) && !done.has(p.id) && !lk(p);
    }), wk, d, K, cap);
    var liveN = rows.filter(function (x) {
      return x.vf > 0;
    }).length;
    return {
      start: [].concat(rows, _toConsumableArray(L.start)).sort(function (a, b) {
        return ({
          F: 0,
          D: 1,
          UTIL: 2,
          G: 3
        }[a.slot] ?? 4) - ({
          F: 0,
          D: 1,
          UTIL: 2,
          G: 3
        }[b.slot] ?? 4);
      }),
      bench: L.bench,
      total: rows.reduce(function (s2, x) {
        return s2 + x.x;
      }, 0) + L.total,
      act: act,
      proj: full,
      locked: rows.length,
      liveN: liveN,
      openN: L.start.length,
      allDone: !rows.some(function (x) {
        return x.st === "L";
      }) && !L.start.length,
      benchAct: benchAct,
      empty: dt < today ? 0 : L.empty,
      sched: L.sched + liveN
    };
  });
  var sum = function sum(f) {
    return days.reduce(function (a, x) {
      return a + f(x);
    }, 0);
  };
  return {
    days: days,
    total: sum(function (x) {
      return x.total;
    }),
    act: sum(function (x) {
      return x.act;
    }),
    actSoFar: actSoFar,
    projSoFar: projSoFar,
    used: sum(function (x) {
      return x.openN + x.liveN;
    }),
    wasted: sum(function (x) {
      return x.bench.length;
    }),
    empty: sum(function (x) {
      return x.empty;
    }),
    sched: sum(function (x) {
      return x.sched;
    })
  };
}

// ---------- round 22: NHL box-score stat lines (news_logos.py) ----------
var pStat = function pStat(p, dt) {
  var id = String(p && p.id || "").replace(/^e/, "");
  return (((window.ESPN_DATA || {}).pstat || {})[dt] || {})[id] || null;
};
var statLine = function statLine(x) {
  if (!x) return "";
  if (x.sv != null) return [x.dec || null, x.sv + " SV", x.ga + " GA", x.toi ? x.toi + " TOI" : null].filter(Boolean).join(", ");
  var n = function n(v, l) {
    return v ? v > 1 ? v + " " + l : l : null;
  };
  return [n(x.g, "G"), n(x.a, "A"), (x.pm > 0 ? "+" : "") + (x.pm || 0), n(x.sog, "SOG"), n(x.pim, "PIM"), n(x.hit, "HIT"), n(x.blk, "BLK"), x.toi ? x.toi + " TOI" : null].filter(Boolean).join(", ");
};

// ---------- round 24: a player counts on a day only if ESPN has him on that day's roster (news_logos.py) ----------
var onEspnDay = function onEspnDay(AD, p) {
  return !AD || !Object.keys(AD).length || AD[String(p.id).replace(/^e/, "")] != null;
};

// ---------- round 25: pickups start after the daily lock (news_logos.py) ----------
// ESPN locks the whole day at the first puck drop, so anyone added after that plays from tomorrow.
// Players on waivers (1-day waivers) can play from tomorrow at the earliest.
var __LK = null;
var lockedToday = function lockedToday() {
  var today = todayISO(),
    k = today + ":" + Math.floor(Date.now() / 30000);
  if (__LK && __LK.k === k) return __LK.v;
  var G = ((window.GAMES_DATA || {}).games || {})[today] || {};
  var first = Object.values(G).reduce(function (m, g) {
    var t = g && g.st ? Date.parse(g.st) : NaN;
    return isNaN(t) ? m : Math.min(m, t);
  }, Infinity);
  var live = Object.values((window.__LIVESC || {})[today] || {}).some(function (x) {
    return x && x.s && x.s !== "P";
  });
  var espn = Object.values(((window.ESPN_DATA || {}).gstate || {})[today] || {}).some(function (x) {
    return x && x.s && x.s !== "P";
  });
  var v = live || espn || first <= Date.now();
  __LK = {
    k: k,
    v: v
  };
  return v;
};
var pickStart = function pickStart(p) {
  return p && p.wv || lockedToday() ? addDays(todayISO(), 1) : todayISO();
};
var onDay = function onDay(p, dt) {
  return !dt || (!p.fromD || dt >= p.fromD) && (!p.untilD || dt < p.untilD);
};
var timedMove = function timedMove(roster, me, moves) {
  var r = roster;
  moves.forEach(function (_ref124) {
    var add = _ref124.add,
      drop = _ref124.drop;
    var a = pickStart(add);
    r = r.map(function (p) {
      return drop && p.id === drop.id ? {
        ...p,
        untilD: a
      } : p;
    }).concat([{
      ...add,
      ft: me,
      fromD: a
    }]);
  });
  return r;
};
var PickNote = function PickNote() {
  var a = pickStart(null);
  return a === todayISO() ? null : /*#__PURE__*/React.createElement("div", {
    className: "w-full text-xs text-amber-600 mt-1"
  }, "Today's first game has started, so anyone you add now plays from ", dayLabel(a), ". Players on waivers show a Waivers tag and can't play before tomorrow.");
};

// ---------- round 26: planner win chance (news_logos.py) ----------
var planRoster = function planRoster(s, wk, steps) {
  var r = s.players.filter(function (p) {
    return p.ft === s.me;
  });
  steps.forEach(function (st) {
    var a = wk.dates[st.day];
    r = r.map(function (p) {
      return p.id === st.drop.id ? {
        ...p,
        untilD: a
      } : p;
    }).concat([{
      ...st.add,
      ft: s.me,
      fromD: a
    }]);
  });
  return r;
};
var PlanWin = function PlanWin(_ref125) {
  var a = _ref125.a,
    b = _ref125.b;
  if (a == null || b == null) return null;
  var d = Math.round(b * 100) - Math.round(a * 100);
  return /*#__PURE__*/React.createElement("span", {
    className: "text-sm whitespace-nowrap " + (d > 0 ? "text-green-700" : d < 0 ? "text-red-600" : "text-slate-500"),
    title: "Your chance to win this week before and after this move"
  }, "win ", wpTxt(a), " \u2192 ", wpTxt(b), " ", /*#__PURE__*/React.createElement("span", {
    className: "font-semibold"
  }, d > 0 ? "+" : "", d, "%"));
};

// ---------- round 27: no moves left this week, so plan next week instead (news_logos.py) ----------
var noMovesWk = function noMovesWk(s, w) {
  return !!w && movesLeft(s, s.me, w) === 0;
};
var outOfMoves = function outOfMoves(s) {
  return noMovesWk(s, s.weeks[s.wk]);
};
var nextWkS = function nextWkS(s) {
  return s.wk + 1 < s.weeks.length ? {
    ...s,
    wk: s.wk + 1
  } : null;
};
var planS = function planS(s) {
  return outOfMoves(s) && nextWkS(s) || s;
};
var planBase = function planBase(s, sP) {
  return sP !== s && !oppOf(sP.weeks[sP.wk] || {}, sP.me) ? null : winChance(sP);
};
var planNote = function planNote(sP) {
  var w = sP.weeks[sP.wk] || {},
    d = (w.dates || [])[0];
  return "No moves left this week. These are for " + (w.label || "next week") + (d ? ", once your moves reset on " + dayLabel(d) : "") + ".";
};
var PlanNote = function PlanNote(_ref126) {
  var sP = _ref126.sP;
  return /*#__PURE__*/React.createElement("div", {
    className: "w-full text-xs text-amber-600 mt-1 mb-1"
  }, planNote(sP));
};

// ---------- round 28: goalies must be playing, player updates for My Team (news_logos.py) ----------
// a goalie is "not playing" if he started fewer than 2 of his team's last 5 games, or is out right now
var gxGoalieOut0 = function gxGoalieOut0(p) {
  /* gx075-g */
  if (!p || p.p !== "G") return false;
  var today = todayISO();
  if (avail(p, today) === 0) return true;
  var g = sigOf(p).gs;
  if (g && g.rg >= 3) return g.rs * 5 < g.rg * 2;
  var played = _toConsumableArray(SCHED[p.t] || []).filter(function (d) {
    return d < today;
  }).length;
  return played >= 4 && !(p.gp > 0);
};
function MyForm(_ref127) {
  var s = _ref127.s;
  var K = s.blend;
  var rows = s.players.filter(function (p) {
    return p.ft === s.me && !p.ir;
  }).map(function (p) {
    var fr = formRatio(p, K),
      t = toiOf(p),
      rec = sigOf(p).rec;
    if (fr !== null && fr >= 1.3) return {
      p: p,
      n: "Hot: " + f1(rec.ppg) + "/g lately. Start him every game.",
      c: "text-orange-600"
    };
    if (fr !== null && fr <= 0.7) return {
      p: p,
      n: "Cold: " + f1(rec.ppg) + "/g lately. Check his role before dropping.",
      c: "text-sky-600"
    };
    if (t && (t.d <= -90 || t.pd <= -45)) return {
      p: p,
      n: "Losing minutes (" + (t.d <= -90 ? mm(t.d) + " a game" : "power play " + mm(t.pd)) + "). Watch closely.",
      c: "text-red-600"
    };
    if (t && (t.d >= 90 || t.pd >= 45)) return {
      p: p,
      n: "Bigger role (" + (t.d >= 90 ? mm(t.d) + " a game" : "power play " + mm(t.pd)) + ").",
      c: "text-green-700"
    };
    return null;
  }).filter(Boolean);
  return /*#__PURE__*/React.createElement(Section, {
    title: "Player updates" + (rows.length ? " (" + rows.length + ")" : ""),
    sub: "Hot and cold streaks and ice-time changes, compared with each player's projection."
  }, rows.length ? rows.map(function (_ref128) {
    var p = _ref128.p,
      n = _ref128.n,
      c = _ref128.c;
    return /*#__PURE__*/React.createElement(PlayerLine, {
      key: p.id,
      s: s,
      p: p,
      extra: /*#__PURE__*/React.createElement("span", {
        className: c
      }, "\xB7 " + n)
    });
  }) : /*#__PURE__*/React.createElement("div", {
    className: "text-slate-400"
  }, "Everyone is playing close to projection."));
}

// ---------- round 29: trade advice with buy-low list, free-agent search (news_logos.py) ----------
function TradeAdvice(_ref129) {
  var s = _ref129.s,
    onPick = _ref129.onPick;
  var K = s.blend;
  var _useState125 = useState("all"),
    _useState126 = _slicedToArray(_useState125, 2),
    team = _useState126[0],
    setTeam = _useState126[1];
  var _useState127 = useState(false),
    _useState128 = _slicedToArray(_useState127, 2),
    more = _useState128[0],
    setMore = _useState128[1];
  var T = leagueTable(s),
    g = T.grpRank[s.me] || {};
  var posName = {
      F: "forwards",
      D: "defence",
      G: "goalies"
    },
    need = {
      F: 10,
      D: 5,
      G: 2
    };
  var by = ["F", "D", "G"].sort(function (a, b) {
      return (g[b] || 0) - (g[a] || 0);
    }),
    weak = by[0],
    strong = by[2];
  var pg = function pg(p) {
    return effAvg(p, K) * (p.p === "G" ? p.prob : 1);
  };
  var mine = s.players.filter(function (p) {
    return p.ft === s.me && !p.ir;
  });
  var spare = mine.filter(function (p) {
    return p.p === strong;
  }).sort(function (a, b) {
    return pg(b) - pg(a);
  }).slice(need[strong]);
  var sell = mine.filter(function (p) {
    return tbFlags(p, K).some(function (f) {
      return f.sell;
    });
  }).sort(function (a, b) {
    return pg(b) - pg(a);
  }).slice(0, 6);
  var all = useMemo(function () {
    var why = function why(p) {
      var r = [],
        fr = formRatio(p, K),
        sg = sigOf(p),
        rec = sg.rec,
        l = sg.luck;
      var id = typeof p.id === "string" && p.id[0] === "e" ? p.id.slice(1) : null;
      var mb = window.__MODEL && id ? (window.__MODEL.base || {})[id] : null;
      if (fr !== null && fr <= 0.75 && rec) r.push("cold: " + f1(rec.ppg) + "/g last 14 days");
      if (mb != null && p.proj && p.avg > 0 && mb / p.avg >= 1.15 && mb - p.avg >= 1) r.push("model " + f1(mb) + " vs ESPN " + f1(p.avg));
      if (l && (l.t === "s" && l.d <= -2 || l.t === "g" && l.d <= -4)) r.push("unlucky");
      return r;
    };
    return s.players.filter(function (p) {
      return p.ft !== s.me && p.ft !== "fa" && !p.ir && pg(p) >= 6 && !goalieOut(p);
    }).map(function (p) {
      return {
        p: p,
        r: why(p)
      };
    }).filter(function (x) {
      return x.r.length;
    }).sort(function (a, b) {
      return pg(b.p) - pg(a.p);
    });
  }, [s.players, K, window.__PMODE]);
  var list = all.filter(function (x) {
    return team === "all" || x.p.ft === team;
  });
  var shown = list.slice(0, more ? 20 : 8);
  return /*#__PURE__*/React.createElement(Section, {
    title: "Buy low",
    sub: "Good players on other teams who are cold, unlucky or underrated."
  }, /*#__PURE__*/React.createElement("div", {
    className: "flex flex-wrap items-center gap-2 mb-1",
    "data-r42": "bl"
  }, /*#__PURE__*/React.createElement("div", {
    className: "text-xs uppercase tracking-wide text-slate-500"
  }, "Buy low (", list.length, "): good players who are cold, unlucky or underrated"), /*#__PURE__*/React.createElement("select", {
    className: inp + " ml-auto",
    value: team,
    onChange: function onChange(e) {
      setTeam(e.target.value);
      setMore(false);
    }
  }, /*#__PURE__*/React.createElement("option", {
    value: "all"
  }, "All teams"), s.teams.filter(function (t) {
    return t.id !== s.me;
  }).map(function (t) {
    return /*#__PURE__*/React.createElement("option", {
      key: t.id,
      value: t.id
    }, t.name);
  }))), shown.length ? shown.map(function (_ref130) {
    var p = _ref130.p,
      r = _ref130.r;
    return /*#__PURE__*/React.createElement(PlayerLine, {
      key: p.id,
      s: s,
      p: p,
      extra: /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("span", {
        className: "text-sky-600"
      }, "\xB7 " + r.join(", ")), /*#__PURE__*/React.createElement("button", {
        type: "button",
        className: "text-blue-600",
        onClick: function onClick() {
          return onPick(p);
        }
      }, "Add to trade"))
    });
  }) : /*#__PURE__*/React.createElement("div", {
    className: "text-slate-400"
  }, "No buy-low players here right now. Cold streaks need 3 or more recent games to show."), list.length > shown.length && !more ? /*#__PURE__*/React.createElement("button", {
    className: "text-sm text-blue-600 mt-2",
    onClick: function onClick() {
      return setMore(true);
    }
  }, "Show all ", Math.min(20, list.length)) : null);
}
function FaSearch(_ref131) {
  var s = _ref131.s,
    top = _ref131.top,
    taken = _ref131.taken,
    val = _ref131.val,
    onPick = _ref131.onPick;
  var _useState129 = useState(""),
    _useState130 = _slicedToArray(_useState129, 2),
    q = _useState130[0],
    setQ = _useState130[1];
  var _useState131 = useState(false),
    _useState132 = _slicedToArray(_useState131, 2),
    open = _useState132[0],
    setOpen = _useState132[1];
  var qq = nrm(q);
  var list = !open ? [] : qq ? s.players.filter(function (p) {
    return p.ft === "fa" && p.prob > 0 && !taken.has(p.id) && nrm(p.n).includes(qq);
  }).sort(function (a, b) {
    return val(b) - val(a);
  }).slice(0, 8) : top.filter(function (p) {
    return !taken.has(p.id);
  }).slice(0, 6);
  return /*#__PURE__*/React.createElement("div", {
    className: "relative mt-2"
  }, /*#__PURE__*/React.createElement("input", {
    className: inp + " w-full",
    placeholder: "Search any free agent by name",
    value: q,
    onChange: function onChange(e) {
      setQ(e.target.value);
      setOpen(true);
    },
    onFocus: function onFocus() {
      return setOpen(true);
    },
    onBlur: function onBlur() {
      return setTimeout(function () {
        return setOpen(false);
      }, 150);
    }
  }), open ? /*#__PURE__*/React.createElement("div", {
    className: "ms-list"
  }, !qq ? /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500 px-2 pt-1 pb-1"
  }, "Best available") : null, list.map(function (p) {
    return /*#__PURE__*/React.createElement("button", {
      key: p.id,
      type: "button",
      className: "ms-opt",
      onMouseDown: function onMouseDown(e) {
        return e.preventDefault();
      },
      onClick: function onClick() {
        onPick(p.id);
        setQ("");
        setOpen(false);
      }
    }, /*#__PURE__*/React.createElement(TeamLogo, {
      t: p.t,
      size: 22
    }), /*#__PURE__*/React.createElement("span", {
      className: "truncate flex-1 text-left"
    }, p.n, " ", /*#__PURE__*/React.createElement("span", {
      className: "text-xs text-slate-500"
    }, p.p)), /*#__PURE__*/React.createElement("span", {
      className: "text-xs text-slate-500 whitespace-nowrap"
    }, f1(val(p)), "/g"));
  }), list.length === 0 ? /*#__PURE__*/React.createElement("div", {
    className: "text-sm text-slate-400 px-2 py-2"
  }, "No free agent matches.") : null) : null);
}

// ---------- round 32: theme switch, top bar, Today gauges and week chart (news_logos.py) ----------
var ThemeBtn = function ThemeBtn(_ref132) {
  var cls = _ref132.cls;
  var v = window.__themePref ? window.__themePref() : "auto";
  var next = v === "auto" ? "light" : v === "light" ? "dark" : "auto";
  return /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: cls || "text-xs text-slate-500",
    title: "Switch between automatic, light and dark",
    onClick: function onClick() {
      return window.__setTheme && window.__setTheme(next);
    }
  }, "Theme: " + (v === "auto" ? "automatic" : v));
};
var ordN = function ordN(n) {
  return n + (n % 100 >= 11 && n % 100 <= 13 ? "th" : ["th", "st", "nd", "rd"][n % 10] || "th");
};
var lastN = function lastN(n) {
  var x = String(n || "").split(" ");
  return x.length > 1 ? x.slice(1).join(" ") : x[0];
};
var GX_TABS = [["today", "Today"], ["matchup", "Matchup"], ["myteam", "Team"], ["league", "League"]];
var GX_MORE = [["setup", "Settings"], ["news", "News"], ["teams", "Teams"]];
function TopBar(_ref133) {
  var s = _ref133.s,
    setS = _ref133.setS,
    tab = _ref133.tab,
    go = _ref133.go,
    ageH = _ref133.ageH;
  // top bar v44: five plain tabs, Setup is a page (news_logos.py)
  // older done markers kept: className={"gx-tab" + ((tab === k || (k === "myteam" && (tab === "moves" || tab === "lines")))
  // older done markers kept: {"Setup"}</button>
  var _useState133 = useState(null),
    _useState134 = _slicedToArray(_useState133, 2),
    rank = _useState134[0],
    setRank = _useState134[1];
  useEffect(function () {
    var id = setTimeout(function () {
      try {
        var T = leagueTable(s),
          i = T.rows.findIndex(function (x) {
            return x.t.id === s.me;
          });
        setRank(i >= 0 ? [i + 1, T.rows.length] : null);
      } catch (e) {}
    }, 400);
    return function () {
      return clearTimeout(id);
    };
  }, [s.players, s.wk, s.blend, window.__PMODE]);
  var name = teamName(s, s.me) || "My team";
  var sync = s.lastSync ? toDate(s.lastSync) : null;
  var TABS = [["today", "Today", ["today"]], ["matchup", "Matchup", ["matchup"]], ["myteam", "Team", ["myteam", "moves", "lines"]], ["league", "League", ["league", "teams"]], ["setup", "Setup", ["setup", "news"]]];
  var W = gxWarn(s);
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
  }, rank ? ordN(rank[0]) + " of " + rank[1] : s.league || "\xA0")), TABS.map(function (_ref134) {
    var _ref135 = _slicedToArray(_ref134, 3),
      k = _ref135[0],
      l = _ref135[1],
      grp = _ref135[2];
    return /*#__PURE__*/React.createElement("a", {
      key: k,
      href: gxHash(k),
      onClick: function onClick(e) {
        /* gx072-top */if (gxNewTab(e)) return;
        e.preventDefault();
        go(k, k === "setup" ? "settings" : k === "league" ? "power" : undefined);
      },
      className: "gx-tab" + (grp.indexOf(tab) >= 0 ? " on" : "")
    }, l, W[k] ? /*#__PURE__*/React.createElement("i", {
      className: "gx-wd",
      title: "Needs a look"
    }) : null);
  }), /*#__PURE__*/React.createElement("a", {
    className: "gx-tab",
    href: "ai-dashboard.html",
    target: "_blank",
    rel: "noopener",
    "data-r63": "ailab"
  }, "AI Lab"), /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: "ml-auto gx-tab",
    onClick: function onClick() {
      return window.dispatchEvent(new Event("gm-search"));
    }
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
var GxRing = function GxRing(_ref136) {
  var v = _ref136.v,
    big = _ref136.big;
  // ring v36: the circle is back (older marker kept: dial v35) (news_logos.py)
  var size = big ? 104 : 64,
    m = size / 2,
    r = big ? 36 : 26,
    w = big ? 6 : 5,
    c = 2 * Math.PI * r;
  var p = v == null ? 0 : Math.max(0.01, Math.min(0.99, v));
  var col = v == null ? "var(--faint)" : v >= 0.5 ? "var(--good)" : "var(--bad)";
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
function GxWeek(_ref137) {
  var wk = _ref137.wk,
    A = _ref137.A,
    B = _ref137.B,
    aA = _ref137.aA,
    aB = _ref137.aB;
  // week chart v34: drawn at real size so text stays readable, cleaner projection line (news_logos.py)
  var _useState135 = useState(620),
    _useState136 = _slicedToArray(_useState135, 2),
    W = _useState136[0],
    setW = _useState136[1];
  var box = React.useRef(null);
  useEffect(function () {
    var el = box.current;
    if (!el) return;
    var fit = function fit() {
      return setW(Math.max(300, Math.round(el.clientWidth)));
    };
    fit();
    if (window.ResizeObserver) {
      var ro = new ResizeObserver(fit);
      ro.observe(el);
      return function () {
        return ro.disconnect();
      };
    }
    window.addEventListener("resize", fit);
    return function () {
      return window.removeEventListener("resize", fit);
    };
  }, []);
  var dates = wk.dates || [],
    n = dates.length,
    today = todayISO();
  if (!n) return /*#__PURE__*/React.createElement("div", {
    ref: box
  });
  var run = aA - aB - (A.act - B.act);
  var rows = dates.map(function (dt, d) {
    var x = A.days[d],
      y = B.days[d],
      dv = x.act + x.total - (y.act + y.total);
    run += dv;
    return {
      dt: dt,
      dv: dv,
      run: run,
      st: dt < today ? "f" : dt === today ? "t" : "p"
    };
  });
  var grid = Math.max(10, Math.ceil(rows.reduce(function (mx, r) {
      return Math.max(mx, Math.abs(r.dv));
    }, 0) / 10) * 10),
    sc = 46 / grid;
  var L = 34,
    R = W - 16,
    colW = (R - L) / n,
    cx = function cx(i) {
      return L + colW * (i + 0.5);
    },
    bw = Math.min(40, colW * 0.36);
  var lo = Math.min.apply(null, rows.map(function (r) {
      return r.run;
    })),
    hi = Math.max.apply(null, rows.map(function (r) {
      return r.run;
    }));
  var ry = function ry(v) {
    return hi === lo ? 167 : 178 - (v - lo) / (hi - lo) * 22;
  };
  var ci = rows.findIndex(function (r) {
      return r.st !== "f";
    }),
    last = ci < 0 ? n - 1 : ci - 1;
  var pts = function pts(a, b) {
    return rows.slice(a, b + 1).map(function (r, i) {
      return cx(a + i).toFixed(1) + "," + ry(r.run).toFixed(1);
    }).join(" ");
  };
  var sg = function sg(v) {
    return (v > 0 ? "+" : "") + Math.round(v);
  };
  var col = function col(v) {
    return v >= 0 ? "var(--good)" : "var(--bad)";
  };
  var tx = function tx(size, fill, weight) {
    return {
      fontSize: size,
      fill: fill,
      fontWeight: weight || 400
    };
  };
  var nowLeft = last >= n - 3;
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
  }, rows.map(function (r, i) {
    return r.st === "t" ? /*#__PURE__*/React.createElement("rect", {
      key: "h" + i,
      x: cx(i) - colW / 2 + 2,
      y: 4,
      width: colW - 4,
      height: 136,
      style: {
        fill: "var(--accentSoft)"
      }
    }) : null;
  }), /*#__PURE__*/React.createElement("line", {
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
  }, "-" + grid), rows.map(function (r, i) {
    var h = Math.max(1, Math.abs(r.dv) * sc),
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
  }) : null, rows.map(function (r, i) {
    return i > last ? /*#__PURE__*/React.createElement("circle", {
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
    }) : null;
  }), rows.map(function (r, i) {
    return i <= last ? /*#__PURE__*/React.createElement("circle", {
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
    }) : null;
  }), last >= 0 && ci >= 0 ? /*#__PURE__*/React.createElement("text", {
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
var GxPanel = function GxPanel(_ref138) {
  var title = _ref138.title,
    right = _ref138.right,
    children = _ref138.children;
  return /*#__PURE__*/React.createElement("div", {
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
};
function GxCarry(_ref139) {
  var s = _ref139.s,
    wk = _ref139.wk;
  var K = s.blend,
    gen = (window.ESPN_DATA || {}).generated;
  var data = useMemo(function () {
    var P = pby(),
      acc = {};
    (wk.dates || []).forEach(function (dt) {
      var AD = actDay(s.me, dt);
      if (!AD) return;
      Object.entries(AD).forEach(function (_ref140) {
        var _ref141 = _slicedToArray(_ref140, 2),
          pid = _ref141[0],
          v = _ref141[1];
        if (!v || v[0] == null || !ESLOT[v[1]]) return;
        var p = P["e" + pid];
        if (!p || !(SCHED[p.t] && SCHED[p.t].has(dt))) return;
        var st = gState(p.t, dt).s;
        if (st === "P" || p.p === "G" && !v[0]) return;
        var a = acc[p.id] = acc[p.id] || {
          p: p,
          pts: 0,
          g: 0,
          diff: 0
        };
        a.pts += v[0];
        a.g++;
        if (st === "F") a.diff += v[0] - effAvg(p, K, dt);
      });
    });
    var list = Object.values(acc),
      top = [].concat(list).sort(function (x, y) {
        return y.pts - x.pts;
      }).slice(0, 3);
    var low = list.filter(function (x) {
      return top.indexOf(x) < 0;
    }).sort(function (x, y) {
      return x.diff - y.diff;
    })[0];
    return {
      top: top,
      low: low && low.diff <= -3 ? low : null
    };
  }, [s.players, wk, K, gen]);
  var row = function row(x, i, note) {
    return /*#__PURE__*/React.createElement("div", {
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
    }, /*#__PURE__*/React.createElement(TeamLogo, {
      t: x.p.t,
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
  };
  return /*#__PURE__*/React.createElement(GxPanel, {
    title: "Who's carrying you",
    right: "This matchup, in your lineup"
  }, data.top.length ? data.top.map(function (x, i) {
    return row(x, i, null);
  }) : /*#__PURE__*/React.createElement("div", {
    className: "text-sm text-slate-500"
  }, "No games counted yet in this matchup."), data.low ? row(data.low, 9, Math.round(-data.low.diff) + " under projection") : null);
}
function GxGoalies(_ref142) {
  var s = _ref142.s,
    wk = _ref142.wk;
  var today = todayISO();
  var rows = s.players.filter(function (p) {
    return p.ft === s.me && p.p === "G" && !p.ir;
  }).map(function (p) {
    var id = String(p.id).slice(1);
    var st = 0,
      pts = 0,
      left = 0;
    (wk.dates || []).forEach(function (dt, d) {
      if (!(wk.games[p.t] || []).includes(d)) return;
      if (gState(p.t, dt).s !== "P") {
        var AD = actDay(s.me, dt),
          v = AD ? AD[id] : null;
        if (v && v[1] === 5 && v[0]) {
          st++;
          pts += v[0];
        }
      } else if (dt >= today && avail(p, dt) > 0 && gStart(p, dt).v >= 0.5) left++;
    });
    return {
      p: p,
      st: st,
      pts: pts,
      left: left
    };
  });
  return /*#__PURE__*/React.createElement(GxPanel, {
    title: "Goalie board",
    right: "starts \xB7 left \xB7 points"
  }, rows.length ? rows.map(function (x, i) {
    return /*#__PURE__*/React.createElement("div", {
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
    }, /*#__PURE__*/React.createElement(TeamLogo, {
      t: x.p.t,
      size: 20
    }), /*#__PURE__*/React.createElement(PN, {
      p: x.p,
      className: ""
    }))), /*#__PURE__*/React.createElement("span", {
      className: "text-xs text-slate-500 whitespace-nowrap"
    }, x.st + " \xB7 " + x.left), /*#__PURE__*/React.createElement("span", {
      className: "font-semibold text-right",
      style: {
        minWidth: 40,
        fontVariantNumeric: "tabular-nums",
        color: x.pts > 5 ? "var(--good)" : x.pts < 0 ? "var(--bad)" : "var(--ink)"
      }
    }, f1(x.pts)));
  }) : /*#__PURE__*/React.createElement("div", {
    className: "text-sm text-slate-500"
  }, "No goalies on your roster."));
}
// chance of a top-6 finish: 2,000 simulated seasons from each team's strength and the real schedule
function playoffSim(s) {
  var ids = s.teams.map(function (t) {
    return t.id;
  });
  if (ids.length < 2 || ids.indexOf(s.me) < 0) return null;
  var T = leagueTable(s),
    str = {},
    K = s.blend,
    today = todayISO();
  T.rows.forEach(function (x) {
    return str[x.t.id] = x.strength;
  });
  var end = Math.min(s.weeks.length, s.poStart ?? 24),
    w0 = {},
    pf = {},
    todo = [];
  ids.forEach(function (id) {
    w0[id] = 0;
    pf[id] = 0;
  });
  s.weeks.slice(0, end).forEach(function (w) {
    var len = (w.dates || []).length,
      pairs = (w.pairs || []).filter(function (p) {
        return p[0] && p[1] && w0[p[0]] != null && w0[p[1]] != null;
      });
    if (!len || !pairs.length) return;
    if (effDone(w, s.autoDone) >= len) {
      pairs.forEach(function (_ref143) {
        var _ref144 = _slicedToArray(_ref143, 2),
          a = _ref144[0],
          b = _ref144[1];
        var x = +(w.act || {})[a] || 0,
          y = +(w.act || {})[b] || 0;
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
    var live = w.dates[0] <= today ? deriveWeek(w, s.autoDone) : null;
    pairs.forEach(function (_ref145) {
      var _ref146 = _slicedToArray(_ref145, 2),
        a = _ref146[0],
        b = _ref146[1];
      var p;
      if (live) {
        var _R = function _R(id) {
            return weekLive(s.players.filter(function (q) {
              return q.ft === id;
            }), live, K, id);
          },
          act = function act(id) {
            return +(live.act || {})[id] || 0;
          };
        p = winProb(_R(a), _R(b), act(a), act(b));
      } else p = normCdf(((str[a] || 0) - (str[b] || 0)) * (len / 7) / (80 * Math.sqrt(len / 7)));
      pf[a] += (str[a] || 0) * (len / 7);
      pf[b] += (str[b] || 0) * (len / 7);
      todo.push([a, b, Math.max(0.02, Math.min(0.98, p))]);
    });
  });
  var seed = 20262027;
  var rnd = function rnd() {
    seed = seed + 0x6d2b79f5 | 0;
    var t = Math.imul(seed ^ seed >>> 15, 1 | seed);
    t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
    return ((t ^ t >>> 14) >>> 0) / 4294967296;
  };
  var N = 2000,
    cut = Math.min(6, ids.length - 1);
  var inN = 0,
    sum = 0;
  var _loop5 = function _loop5() {
    var w = Object.assign({}, w0);
    for (var j = 0; j < todo.length; j++) {
      var m = todo[j];
      if (rnd() < m[2]) w[m[0]]++;else w[m[1]]++;
    }
    var r = ids.slice().sort(function (a, b) {
      return w[b] - w[a] || pf[b] - pf[a];
    }).indexOf(s.me) + 1;
    if (r <= cut) inN++;
    sum += r;
  };
  for (var k = 0; k < N; k++) {
    _loop5();
  }
  return {
    odds: inN / N,
    finish: Math.round(sum / N),
    cut: cut
  };
}
function GxPlayoff(_ref147) {
  var s = _ref147.s;
  var _useState137 = useState(null),
    _useState138 = _slicedToArray(_useState137, 2),
    res = _useState138[0],
    setRes = _useState138[1];
  useEffect(function () {
    var id = setTimeout(function () {
      try {
        setRes(playoffSim(s));
      } catch (e) {
        setRes(null);
      }
    }, 500);
    return function () {
      return clearTimeout(id);
    };
  }, [s.players, s.weeks, s.wk, s.blend, window.__PMODE]);
  useEffect(function () {
    if (res) uiSet("po:" + s.wk, res.odds);
  }, [res ? res.odds : null, s.wk]);
  var prev = uiGet()["po:" + (s.wk - 1)];
  var d = res && prev != null ? Math.round(res.odds * 100) - Math.round(prev * 100) : null;
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
  }, "\xB7 top " + (res ? res.cut : 6) + " make it"))), d != null ? /*#__PURE__*/React.createElement("div", {
    className: "text-right whitespace-nowrap"
  }, /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500"
  }, "since last week"), /*#__PURE__*/React.createElement("div", {
    style: {
      color: d > 0 ? "var(--good)" : d < 0 ? "var(--bad)" : "var(--mute)"
    }
  }, (d > 0 ? "+" : "") + d + "%")) : null));
}
function GxHome(_ref148) {
  var s = _ref148.s,
    wk = _ref148.wk,
    A = _ref148.A,
    B = _ref148.B;
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
var TEAM_SUBS = [["roster", "Roster"], ["pickups", "Pickups"], ["plan", "Plan"], ["trades", "Trades"], ["lines", "Lines"]];
var PICK_SUBS = [["adddrop", "Pickups"], ["advice", "Advice"], ["goalies", "Goalies"]];
function SubBar(_ref149) {
  var tab = _ref149.tab,
    sub = _ref149.sub,
    go = _ref149.go,
    setSubs = _ref149.setSubs,
    nav = _ref149.nav,
    s = _ref149.s,
    wk = _ref149.wk;
  if (tab === "matchup") return s && wk ? /*#__PURE__*/React.createElement(MatchStrip, {
    s: s,
    wk: wk
  }) : null;
  var team = tab === "myteam" || tab === "moves" || tab === "lines";
  if (!team) {
    var back = tab === "news" || tab === "setup" && sub && sub !== "settings" ? ["Setup", function () {
      return go("setup", "settings");
    }] : tab === "league" && sub === "playoffs" ? ["League", function () {
      return go("league", "power");
    }] : null;
    return back ? /*#__PURE__*/React.createElement("div", {
      className: "mb-3"
    }, /*#__PURE__*/React.createElement("button", {
      type: "button",
      className: "text-sm text-blue-600",
      onClick: back[1]
    }, "\u2039 Back to " + back[0])) : null;
  }
  var inPick = PICK_SUBS.some(function (x) {
    return x[0] === sub;
  });
  var cur = tab === "myteam" ? "roster" : tab === "lines" ? "lines" : sub === "planner" ? "plan" : sub === "trades" ? "trades" : "pickups";
  var to = function to(k) {
    return k === "roster" ? go("myteam") : k === "lines" ? go("lines") : k === "plan" ? go("moves", "planner") : k === "trades" ? go("moves", "trades") : go("moves", "adddrop");
  };
  return /*#__PURE__*/React.createElement("div", {
    className: "mb-4"
  }, /*#__PURE__*/React.createElement("div", {
    className: "flex gap-2 overflow-x-auto navscroll pb-1"
  }, TEAM_SUBS.map(function (_ref150) {
    var _ref151 = _slicedToArray(_ref150, 2),
      k = _ref151[0],
      l = _ref151[1];
    return /*#__PURE__*/React.createElement("a", {
      key: k,
      href: GX_TEAM_HREF[k],
      onClick: function onClick(e) {
        if (gxNewTab(e)) return;
        e.preventDefault();
        to(k);
      },
      className: "px-3 py-1.5 rounded-full text-sm border whitespace-nowrap " + (cur === k ? "bg-blue-600 text-white border-blue-600" : "bg-white border-slate-300 text-slate-600")
    }, l);
  })), cur === "pickups" ? /*#__PURE__*/React.createElement("div", {
    className: "flex gap-4 overflow-x-auto navscroll text-sm",
    style: {
      marginTop: 10
    }
  }, PICK_SUBS.map(function (_ref152) {
    var _ref153 = _slicedToArray(_ref152, 2),
      k = _ref153[0],
      l = _ref153[1];
    return /*#__PURE__*/React.createElement("a", {
      key: k,
      href: gxHash("moves", k),
      onClick: function onClick(e) {
        /* gx072-pick */if (gxNewTab(e)) return;
        e.preventDefault();
        go("moves", k);
      },
      className: "whitespace-nowrap " + (sub === k || k === "adddrop" && !inPick ? "font-semibold" : "text-slate-500")
    }, l);
  })) : null);
}
var gxBoxIdx = function gxBoxIdx() {
  return fetch("box/index.json?t=" + Date.now()).then(function (r) {
    return r.ok ? r.json() : null;
  }).then(function (j) {
    return j && j.dates || [];
  }).catch(function () {
    return [];
  });
};
var gxBoxDay = function gxBoxDay(d) {
  var B = window.__BOX = window.__BOX || {
    idx: null,
    at: 0,
    days: {}
  };
  if (B.days[d]) return Promise.resolve(B.days[d]);
  return fetch("box/" + d + ".json").then(function (r) {
    return r.ok ? r.json() : null;
  }).then(function (j) {
    if (j && j.p) B.days[d] = j.p;
    return j && j.p || null;
  }).catch(function () {
    return null;
  });
};

// ---------- round 40: Pickups list (news_logos.py) ----------
var gxEst = function gxEst(x, sc) {
  return x.sv != null ? (x.dec === "W" ? sc.W ?? 5 : 0) + (x.dec === "O" ? sc.OTL ?? 1 : 0) + (x.sv || 0) * (sc.SV ?? 0.6) + (x.ga || 0) * (sc.GA ?? -3) : (x.g || 0) * (sc.G ?? 6) + (x.a || 0) * (sc.A ?? 4) + (x.pm || 0) * (sc.PM ?? 2) + (x.sog || 0) * (sc.SOG ?? 1) + (x.hit || 0) * (sc.HIT ?? 0.1) + (x.blk || 0) * (sc.BLK ?? 1) + (x.ppg || 0) * (sc.PPP ?? 2);
};
var gxLast5 = function gxLast5(ids, sc) {
  return gxBoxIdx().then(function (ds) {
    return Promise.all(ds.slice(-14).map(function (d) {
      return gxBoxDay(d);
    }));
  }).then(function (days) {
    var out = {};
    ids.forEach(function (pid) {
      var a = [];
      days.forEach(function (day) {
        var x = day && day[pid];
        if (x) a.push(x.fp != null ? x.fp : gxEst(x, sc));
      });
      out[pid] = a.slice(-5);
    });
    return out;
  }).catch(function () {
    return {};
  });
};
function Pickups(_ref154) {
  var s = _ref154.s,
    setS = _ref154.setS,
    wk = _ref154.wk;
  var K = s.blend;
  var _useState139 = useState(1),
    _useState140 = _slicedToArray(_useState139, 2),
    H = _useState140[0],
    setH = _useState140[1];
  var _useState141 = useState(function () {
      var v = window.__PICK_POS || "all";
      window.__PICK_POS = "";
      return v;
    }),
    _useState142 = _slicedToArray(_useState141, 2),
    pos = _useState142[0],
    setPos = _useState142[1];
  var _useState143 = useState(function () {
      var v = window.__PICK_Q || "";
      window.__PICK_Q = "";
      return v;
    }),
    _useState144 = _slicedToArray(_useState143, 2),
    q = _useState144[0],
    setQ = _useState144[1];
  var _useState145 = useState(25),
    _useState146 = _slicedToArray(_useState145, 2),
    limit = _useState146[0],
    setLimit = _useState146[1];
  useEffect(function () {
    var h = function h() {
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
    return function () {
      return window.removeEventListener("gm-pick", h);
    };
  }, []);
  var _useState147 = useState(null),
    _useState148 = _slicedToArray(_useState147, 2),
    sim = _useState148[0],
    setSim = _useState148[1];
  var _useState149 = useState({}),
    _useState150 = _slicedToArray(_useState149, 2),
    hist = _useState150[0],
    setHist = _useState150[1];
  var sP = useMemo(function () {
    return planS(s);
  }, [s]);
  var plan = sP !== s;
  var wkP = useMemo(function () {
    return plan ? deriveWeek(sP.weeks[sP.wk], sP.autoDone) : wk;
  }, [sP, wk]);
  var gxHideV = gxUseHide(); /* gx075-m */
  var M = useMemo(function () {
    return computeMoves(sP, {
      H: H,
      pos: pos,
      q: q
    });
  }, [sP, H, pos, q, gxHideV]);
  var base = useMemo(function () {
    return planBase(s, sP);
  }, [sP]);
  var minGain = s.minGain ?? 3;
  var all = q ? M.res : M.res.filter(function (r) {
    return r.gain >= minGain;
  });
  var rows = all.slice(0, limit);
  var wins = useMemo(function () {
    var o = {};
    if (base == null) return o;
    rows.forEach(function (r) {
      o[r.f.id] = winChance(sP, afterMove(sP, r.f, r.d));
    });
    return o;
  }, [M, limit, base]);
  var ids = rows.map(function (r) {
    return String(r.f.id).slice(1);
  }).join(",");
  useEffect(function () {
    var dead = false;
    if (!ids) return;
    gxLast5(ids.split(","), s.sc || {}).then(function (h) {
      if (!dead) setHist(function (x) {
        return Object.assign({}, x, h);
      });
    });
    return function () {
      dead = true;
    };
  }, [ids]);
  var ml = movesLeft(s, s.me, wk);
  var pw = plan ? sP.weeks[sP.wk] || {} : null,
    d0 = pw ? (pw.dates || [])[0] : null;
  var qq = nrm(q);
  var others = qq.length >= 2 ? s.players.filter(function (p) {
    return p.ft !== "fa" && p.ft !== s.me && nrm(p.n).includes(qq);
  }).slice(0, 6) : [];
  var hLabel = plan ? {
    1: "next week",
    4: "4 weeks from next week",
    0: "rest of season"
  }[H] : {
    1: "rest of this week",
    4: "next 4 weeks",
    0: "rest of season"
  }[H];
  var spark = function spark(p) {
    var h = hist[String(p.id).slice(1)] || [];
    return /*#__PURE__*/React.createElement("div", {
      className: "gx-sp m-hide",
      title: "Last five games, oldest to newest"
    }, h.length ? h.map(function (v, i) {
      return /*#__PURE__*/React.createElement("i", {
        key: i,
        style: {
          height: Math.max(2, Math.min(22, Math.max(0, v) / 20 * 22)),
          background: v < 0 ? "var(--bad)" : "var(--ink2)"
        }
      });
    }) : /*#__PURE__*/React.createElement("span", {
      className: "text-xs text-slate-500"
    }, "\u2013"));
  };
  return /*#__PURE__*/React.createElement("div", {
    className: "space-y-3"
  }, /*#__PURE__*/React.createElement("div", {
    className: "text-sm"
  }, /*#__PURE__*/React.createElement("span", {
    className: "font-semibold"
  }, ml === 0 ? "No moves left this week." : ml == null ? "" : ml + " move" + (ml === 1 ? "" : "s") + " left this week."), plan ? /*#__PURE__*/React.createElement("span", {
    className: "text-slate-500"
  }, " Showing ", pw.label || "next week", ".", d0 ? " Moves reset " + dayLabel(d0) + "." : "") : null), /*#__PURE__*/React.createElement("div", {
    className: "flex flex-wrap gap-2 items-center"
  }, /*#__PURE__*/React.createElement(Pills, {
    items: [["all", "All"], ["F", "Forwards"], ["D", "Defence"], ["G", "Goalies"]],
    value: pos,
    onChange: function onChange(v) {
      setPos(v);
      setLimit(25);
    }
  }), /*#__PURE__*/React.createElement(Pills, {
    items: [[1, plan ? "Next week" : "This week"], [4, "Next 4 weeks"], [0, "Rest of season"]],
    value: H,
    onChange: function onChange(v) {
      setH(v);
      setLimit(25);
    }
  })), /*#__PURE__*/React.createElement(GxWatchPanel, {
    s: s
  }), /*#__PURE__*/React.createElement(GxHiddenPanel, {
    s: s
  }), /*#__PURE__*/React.createElement("input", {
    className: inp + " w-full",
    placeholder: "Search any player",
    value: q,
    onChange: function onChange(e) {
      return setQ(e.target.value);
    }
  }), /*#__PURE__*/React.createElement("div", {
    className: "gx-pn"
  }, /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("div", {
    className: "gx-pk text-xs text-slate-500",
    style: {
      borderTop: 0,
      paddingTop: 0
    }
  }, /*#__PURE__*/React.createElement("span", null), /*#__PURE__*/React.createElement("span", null, base == null ? "Free agents, best first" : "Win chance now " + wpTxt(base)), /*#__PURE__*/React.createElement("span", {
    className: "n m-hide"
  }, "Last 5"), /*#__PURE__*/React.createElement("span", {
    className: "n m-hide"
  }, "Games"), /*#__PURE__*/React.createElement("span", {
    className: "n m-hide"
  }, "Expected"), /*#__PURE__*/React.createElement("span", {
    className: "n"
  }, "Adds"), /*#__PURE__*/React.createElement("span", {
    className: "n"
  }, "Win")), rows.length ? rows.map(function (r) {
    var keep = r.gain > 0 && effAvg(r.f, K) - effAvg(r.d, K) >= 0,
      tg = shortTag(r.f, K),
      w = wins[r.f.id];
    var st = r.f.status && r.f.status !== "ACTIVE" ? M_ST[r.f.status] || r.f.status.replace(/_/g, " ") : "";
    return /*#__PURE__*/React.createElement("div", {
      key: r.f.id,
      className: "gx-pk row",
      role: "button",
      onClick: function onClick() {
        return setSim({
          add: r.f.id,
          drop: r.d.id
        });
      }
    }, /*#__PURE__*/React.createElement(TeamLogo, {
      t: r.f.t,
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
    }, "on waivers") : null, st ? /*#__PURE__*/React.createElement("span", {
      className: "text-xs",
      style: {
        color: "var(--bad)",
        marginLeft: 6
      }
    }, st) : null), /*#__PURE__*/React.createElement("div", {
      className: "text-xs text-slate-500 truncate"
    }, "Swap for " + r.d.n + " \xB7 " + (keep ? "keep" : H === 1 ? "one week only" : "short-term") + (tg ? " \xB7 " + tg.t : ""), " \xB7 ", /*#__PURE__*/React.createElement("button", {
      type: "button",
      className: "text-blue-600",
      onClick: function onClick(e) {
        e.stopPropagation();
        if (window.__QA) window.__QA.espn(r.f);
      }
    }, "Add on ESPN"), " \xB7 ", /*#__PURE__*/React.createElement("button", {
      type: "button",
      className: "text-blue-600",
      onClick: function onClick(e) {
        e.stopPropagation();
        gxHide.toggle(r.f.id);
      }
    }, gxHideSet().has(r.f.id) ? "Show again" : "Hide" /* gx075-row */), gxScratch(r.f) ? /*#__PURE__*/React.createElement("span", {
      style: {
        color: "var(--warn)"
      }
    }, " \xB7 not in lineup") : null)), spark(r.f), /*#__PURE__*/React.createElement("div", {
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
    }, w == null ? "\u2013" : wpTxt(w)));
  }) : /*#__PURE__*/React.createElement("div", {
    className: "text-sm text-slate-500",
    style: {
      padding: "10px 0"
    }
  }, q ? "No free agent matches that name." : "No pickup adds " + minGain + " or more points for this window."), all.length > rows.length ? /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: "text-sm text-blue-600",
    style: {
      marginTop: 10
    },
    onClick: function onClick() {
      return setLimit(limit + 25);
    }
  }, "Show ", Math.min(25, all.length - rows.length), " more") : null, rows.length ? /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500",
    style: {
      marginTop: 10
    }
  }, "Adds is the extra points in your lineup for ", hLabel, ". Tap a player to try the swap or change who you drop.") : null), others.length ? /*#__PURE__*/React.createElement(GxPanel, {
    title: "On other teams"
  }, others.map(function (p, i) {
    return /*#__PURE__*/React.createElement("div", {
      key: p.id,
      className: "gx-row",
      style: i ? null : {
        borderTop: 0
      }
    }, /*#__PURE__*/React.createElement(TeamLogo, {
      t: p.t,
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
    }, f1(effAvg(p, K))));
  })) : null, sim ? /*#__PURE__*/React.createElement(MoveSim, {
    s: sP,
    setS: setS,
    wk: wkP,
    M: M,
    H: H,
    hLabel: hLabel,
    init: sim,
    wBase: base,
    onClose: function onClose() {
      return setSim(null);
    }
  }) : null);
}

// ---------- round 41: Plan page (news_logos.py) ----------
function PlanPage(_ref155) {
  var s = _ref155.s,
    setS = _ref155.setS,
    wk = _ref155.wk;
  var K = s.blend,
    today = todayISO();
  var sP = useMemo(function () {
    return planS(s);
  }, [s]);
  var plan = sP !== s;
  var wkP = useMemo(function () {
    return plan ? deriveWeek(sP.weeks[sP.wk], sP.autoDone) : wk;
  }, [sP, wk]);
  var dates = wkP.dates || [],
    ti = dates.indexOf(today);
  var d0 = Math.min(dates.length, Math.max(wkP.done || 0, ti >= 0 ? ti : 0) + (ti >= 0 && lockedToday() ? 1 : 0));
  var ml = movesLeft(sP, sP.me, wkP),
    left = ml == null ? 3 : ml;
  var _useState151 = useState(null),
    _useState152 = _slicedToArray(_useState151, 2),
    res = _useState152[0],
    setRes = _useState152[1];
  var _useState153 = useState(true),
    _useState154 = _slicedToArray(_useState153, 2),
    busy = _useState154[0],
    setBusy = _useState154[1];
  var _useState155 = useState(-1),
    _useState156 = _slicedToArray(_useState155, 2),
    openW = _useState156[0],
    setOpenW = _useState156[1];
  useEffect(function () {
    var dead = false;
    setBusy(true);
    var id = setTimeout(function () {
      var r = null;
      try {
        if (left > 0 && d0 < dates.length) {
          var p = buildPlan(sP, wkP, d0, left),
            b = planBase(s, sP);
          r = {
            p: p,
            b: b,
            after: p.steps.map(function (_, i) {
              return b == null ? null : winChance(sP, planRoster(sP, wkP, p.steps.slice(0, i + 1)));
            })
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
    return function () {
      dead = true;
      clearTimeout(id);
    };
  }, [s.players, sP.wk, left, d0, window.__PMODE]);
  var waste = useMemo(function () {
    var mine = s.players.filter(function (p) {
        return p.ft === s.me;
      }),
      chronic = {};
    var weeks = s.weeks.slice(s.wk, s.wk + 4).map(function (w, i) {
      var dw = deriveWeek(w, s.autoDone),
        from = i === 0 ? dw.done || 0 : 0,
        sit = {};
      var empty = 0,
        g = 0,
        pts = 0;
      dw.days.forEach(function (dl, d) {
        if (d < from) return;
        var L = dayLineup(mine, dw, d, K);
        empty += L.empty;
        L.bench.forEach(function (p) {
          var x = sit[p.id] = sit[p.id] || {
            p: p,
            days: []
          };
          x.days.push(dl.split(",")[0]);
          g++;
          pts += p.x;
          var c = chronic[p.id] = chronic[p.id] || {
            p: p,
            g: 0
          };
          c.g++;
        });
      });
      return {
        dw: dw,
        from: from,
        sit: Object.values(sit),
        empty: empty,
        g: g,
        pts: pts
      };
    });
    return {
      weeks: weeks,
      chronic: Object.values(chronic).filter(function (c) {
        return c.g >= 2;
      }).sort(function (a, b) {
        return b.g - a.g;
      }).slice(0, 3),
      g: weeks.reduce(function (a, w) {
        return a + w.g;
      }, 0),
      pts: weeks.reduce(function (a, w) {
        return a + w.pts;
      }, 0)
    };
  }, [s.players, s.wk, K, window.__PMODE]);
  var fix = useMemo(function () {
    var w = waste.weeks[openW];
    if (!w || !w.sit.length || openW === 0 && outOfMoves(s)) return null;
    var mine = s.players.filter(function (p) {
        return p.ft === s.me;
      }),
      mins = {
        F: s.minF ?? 10,
        D: s.minD ?? 5,
        G: s.minGo ?? 2
      };
    var healthy = mine.filter(function (p) {
      return !p.ir;
    }).sort(function (a, b) {
      return effAvg(b, K) - effAvg(a, K);
    });
    var prot = new Set([].concat(_toConsumableArray(healthy.slice(0, s.protectTop ?? 8).map(function (p) {
      return p.id;
    })), _toConsumableArray(mine.filter(function (p) {
      return p.keep;
    }).map(function (p) {
      return p.id;
    }))));
    var cnt = {
      F: 0,
      D: 0,
      G: 0
    };
    healthy.forEach(function (p) {
      cnt[p.p]++;
    });
    var drops = w.sit.map(function (x) {
      return x.p;
    }).filter(function (p) {
      return !p.ir && !prot.has(p.id);
    }).slice(0, 5);
    var weekPts = function weekPts(p) {
      return (w.dw.games[p.t] || []).filter(function (d) {
        return d >= w.from;
      }).reduce(function (t, d) {
        var dt = w.dw.dates[d];
        return t + effAvg(p, K, dt) * (p.p === "G" ? gStart(p, dt).v : p.prob) * avail(p, dt);
      }, 0);
    };
    var pool = s.players.filter(function (p) {
      return p.ft === "fa" && p.prob > 0 && (p.proj !== false || p.gp > 0) && !goalieOut(p);
    }).map(function (p) {
      return {
        p: p,
        v: weekPts(p)
      };
    }).filter(function (x) {
      return x.v > 0;
    }).sort(function (a, b) {
      return b.v - a.v;
    }).slice(0, 25).map(function (x) {
      return x.p;
    });
    var base = weekProj(mine, w.dw, K, w.from).total;
    var best = null;
    drops.forEach(function (d) {
      return pool.forEach(function (f) {
        if (d.p !== f.p && cnt[d.p] - 1 < mins[d.p]) return;
        var g = weekProj(timedMove(mine, s.me, [{
          add: f,
          drop: d
        }]), w.dw, K, w.from).total - base;
        if (!best || g > best.g) best = {
          d: d,
          f: f,
          g: g
        };
      });
    });
    return best && best.g >= 1 ? best : null;
  }, [openW, waste]);
  var playDays = function playDays(p, a) {
    return (wkP.games[p.t] || []).filter(function (d) {
      return d >= a && (p.p !== "G" || gStart(p, dates[d]).v >= 0.5);
    }).map(function (d) {
      return wkP.days[d].split(",")[0];
    }).join(", ");
  };
  var steps = res ? res.p.steps : [];
  var lastWin = res && res.after.length ? res.after[res.after.length - 1] : null;
  var wkName = function wkName(w) {
    var ds = w.dw.dates || [];
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
  }, " \xB7 win chance " + wpTxt(res.b) + " to " + wpTxt(lastWin)) : null) : null), busy ? /*#__PURE__*/React.createElement("div", {
    className: "text-sm text-slate-500",
    style: {
      padding: "12px 0 2px"
    }
  }, "Working it out...") : steps.length ? steps.map(function (st, i) {
    var a = i ? res.after[i - 1] : res.b,
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
    }, (st.add.p === "G" ? "Likely starts " : "Plays ") + (dy || "\u2013"), st.add.wv ? " \xB7 on waivers" : "", " \xB7 ", /*#__PURE__*/React.createElement("button", {
      type: "button",
      className: "text-blue-600",
      onClick: function onClick() {
        return window.__QA && window.__QA.espn(st.add);
      }
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
  }, "Next 4 weeks \xB7 " + waste.g + " game" + (waste.g === 1 ? "" : "s") + (waste.g ? ", about " + Math.round(waste.pts) + " points" : ""))), /*#__PURE__*/React.createElement("div", {
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
  }, "Empty slots")), waste.weeks.map(function (w, i) {
    return /*#__PURE__*/React.createElement("div", {
      key: i
    }, /*#__PURE__*/React.createElement("div", {
      className: "gx-wk",
      role: "button",
      style: {
        cursor: "pointer"
      },
      onClick: function onClick() {
        return setOpenW(openW === i ? -1 : i);
      }
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
    }, w.sit.length ? /*#__PURE__*/React.createElement("div", null, "Sitting: ", w.sit.map(function (x) {
      return x.p.n + " (" + x.days.join(", ") + ")";
    }).join("; ")) : /*#__PURE__*/React.createElement("div", null, "Nobody is stuck on your bench this week."), w.sit.length ? fix ? /*#__PURE__*/React.createElement("div", {
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
    }, i === 0 && outOfMoves(s) ? "No moves left this week to fix it." : "No free agent helps more than keeping who you have.") : null) : null);
  }), /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500",
    style: {
      paddingTop: 10,
      borderTop: "1px solid var(--line)"
    }
  }, waste.chronic.length ? "Most often stuck: " + waste.chronic.map(function (c) {
    return c.p.n + " (" + c.g + " games)";
  }).join(", ") + ". " : "", "Tap a week to see who sits and the swap that fixes it.")));
}

// ---------- round 43: Advice page, four plain lists (news_logos.py) ----------
function AdvicePage(_ref156) {
  var s = _ref156.s,
    setS = _ref156.setS,
    wk = _ref156.wk;
  var K = s.blend;
  var _useState157 = useState(null),
    _useState158 = _slicedToArray(_useState157, 2),
    sim = _useState158[0],
    setSim = _useState158[1];
  var sP = useMemo(function () {
    return planS(s);
  }, [s]);
  var wkP = useMemo(function () {
    return sP !== s ? deriveWeek(sP.weeks[sP.wk], sP.autoDone) : wk;
  }, [sP, wk]);
  var M = useMemo(function () {
    return sim ? computeMoves(sP, {
      H: 1,
      pool: 40
    }) : null;
  }, [sP, !!sim]);
  var base = useMemo(function () {
    return sim ? planBase(s, sP) : null;
  }, [sP, !!sim]);
  var L = useMemo(function () {
    var mb = function mb(p) {
      var id = typeof p.id === "string" && p.id[0] === "e" ? p.id.slice(1) : null;
      return window.__MODEL && id ? (window.__MODEL.base || {})[id] : null;
    };
    var UP = {
      F1: "line 1",
      F2: "line 2",
      D1: "the top pair",
      D2: "the second pair"
    };
    var rise = function rise(p) {
      var g = sigOf(p),
        fr = formRatio(p, K),
        t = g.toi;
      if (g.lines && g.lines.chg === "up") return "Moved up to " + (UP[g.lines.grp] || "a bigger role");
      if (g.ppChg === "added") return "New on the top power play";
      if (t && t.d >= 90) return "More ice time: " + (t.d / 60).toFixed(1) + " more minutes a game";
      if (fr !== null && fr >= 1.25) return "Hot: " + f1(g.rec.ppg) + " a game over two weeks";
      if ((p.chg || 0) >= 5) return "Being picked up fast: +" + f1(p.chg) + "% of leagues";
      return "";
    };
    var under = function under(p) {
      var m = mb(p),
        l = sigOf(p).luck;
      if (m != null && p.proj && p.avg > 0 && m - p.avg >= 1 && m / p.avg >= 1.15) return "Your model rates him " + f1(m - p.avg) + " above ESPN";
      if (l && l.t === "s" && l.d <= -2) return "Unlucky: " + l.g + " goal" + (l.g === 1 ? "" : "s") + " on " + l.sh + " shots";
      if (l && l.t === "g" && l.d <= -4) return "Unlucky: stopping fewer shots than he usually does";
      return "";
    };
    var sell = function sell(p) {
      var m = mb(p),
        l = sigOf(p).luck,
        fr = formRatio(p, K);
      if (m != null && p.proj && p.avg > 0 && p.avg - m >= 1 && m / p.avg <= 0.85) return "ESPN rates him higher than your model";
      if (l && l.t === "s" && l.d >= 2) return "Lucky: " + l.g + " goals on " + l.sh + " shots";
      if (l && l.t === "g" && l.d >= 4) return "Lucky: stopping more shots than he usually does";
      if (fr !== null && fr >= 1.3) return "Hot: " + f1(sigOf(p).rec.ppg) + " a game over two weeks";
      return "";
    };
    var watch = function watch(p) {
      var g = sigOf(p),
        fr = formRatio(p, K),
        t = g.toi;
      if (g.lines && g.lines.chg === "down") return "Moved down the lineup";
      if (g.ppChg === "removed") return "Off the top power play";
      if (t && t.d <= -90) return "Losing ice time: " + (Math.abs(t.d) / 60).toFixed(1) + " minutes less a game";
      if (fr !== null && fr <= 0.7) return "Cold: " + f1(g.rec.ppg) + " a game over two weeks";
      return "";
    };
    var pickL = function pickL(list, fn) {
      return list.map(function (p) {
        return {
          p: p,
          why: fn(p)
        };
      }).filter(function (x) {
        return x.why;
      }).sort(function (a, b) {
        return effAvg(b.p, K) - effAvg(a.p, K);
      }).slice(0, 6);
    };
    var fa = s.players.filter(function (p) {
        return p.ft === "fa" && p.prob > 0 && (p.proj !== false || p.gp > 0) && !goalieOut(p);
      }),
      mine = s.players.filter(function (p) {
        return p.ft === s.me && !p.ir;
      });
    return {
      rise: pickL(fa, rise),
      under: pickL(fa, under),
      sell: pickL(mine, sell),
      watch: pickL(mine, watch)
    };
  }, [s.players, K, window.__PMODE, (window.ESPN_DATA || {}).generated]);
  var open = function open(p) {
    var dr = dropFor(s, p);
    setSim({
      add: p.id,
      drop: dr ? dr.id : ""
    });
  };
  var list = function list(title, rows, fa, bad, empty) {
    return /*#__PURE__*/React.createElement(GxPanel, {
      title: title
    }, rows.length ? rows.map(function (x, i) {
      return /*#__PURE__*/React.createElement("div", {
        key: x.p.id,
        className: "gx-row",
        role: fa ? "button" : undefined,
        style: {
          borderTop: i ? undefined : 0,
          cursor: fa ? "pointer" : "default"
        },
        onClick: fa ? function () {
          return open(x.p);
        } : undefined
      }, /*#__PURE__*/React.createElement(TeamLogo, {
        t: x.p.t,
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
      }, f1(effAvg(x.p, K))));
    }) : /*#__PURE__*/React.createElement("div", {
      className: "text-sm text-slate-500"
    }, empty));
  };
  return /*#__PURE__*/React.createElement("div", {
    className: "space-y-3"
  }, /*#__PURE__*/React.createElement("div", {
    className: "grid md:grid-cols-2 gap-3"
  }, list("Free agents on the rise", L.rise, true, false, "No free agent is clearly on the way up right now."), list("Better than they look", L.under, true, false, "Nobody stands out as underrated right now."), list("Your players to sell high", L.sell, false, false, "None of your players is at a peak right now."), list("Your players to watch", L.watch, false, true, "None of your players is slipping right now.")), /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500"
  }, "The number is expected points a game. Tap a free agent to try the swap."), sim && M ? /*#__PURE__*/React.createElement(MoveSim, {
    s: sP,
    setS: setS,
    wk: wkP,
    M: M,
    H: 1,
    hLabel: sP !== s ? "next week" : "rest of this week",
    init: sim,
    wBase: base,
    onClose: function onClose() {
      return setSim(null);
    }
  }) : null);
}

// ---------- round 44: League page and Setup page (news_logos.py) ----------
// playoff odds for every team: 2,000 simulated seasons from each team's strength and the real schedule
function leagueSim(s) {
  var ids = s.teams.map(function (t) {
    return t.id;
  });
  if (ids.length < 2) return null;
  var T = leagueTable(s),
    str = {},
    K = s.blend,
    today = todayISO();
  T.rows.forEach(function (x) {
    return str[x.t.id] = x.strength;
  });
  var end = Math.min(s.weeks.length, s.poStart ?? 24),
    w0 = {},
    pf = {},
    todo = [];
  ids.forEach(function (id) {
    w0[id] = 0;
    pf[id] = 0;
  });
  s.weeks.slice(0, end).forEach(function (w) {
    var len = (w.dates || []).length,
      pairs = (w.pairs || []).filter(function (p) {
        return p[0] && p[1] && w0[p[0]] != null && w0[p[1]] != null;
      });
    if (!len || !pairs.length) return;
    if (effDone(w, s.autoDone) >= len) {
      pairs.forEach(function (_ref157) {
        var _ref158 = _slicedToArray(_ref157, 2),
          a = _ref158[0],
          b = _ref158[1];
        var x = +(w.act || {})[a] || 0,
          y = +(w.act || {})[b] || 0;
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
    var live = w.dates[0] <= today ? deriveWeek(w, s.autoDone) : null;
    pairs.forEach(function (_ref159) {
      var _ref160 = _slicedToArray(_ref159, 2),
        a = _ref160[0],
        b = _ref160[1];
      var p;
      if (live) {
        var _R2 = function _R2(id) {
            return weekLive(s.players.filter(function (q) {
              return q.ft === id;
            }), live, K, id);
          },
          act = function act(id) {
            return +(live.act || {})[id] || 0;
          };
        p = winProb(_R2(a), _R2(b), act(a), act(b));
      } else p = normCdf(((str[a] || 0) - (str[b] || 0)) * (len / 7) / (80 * Math.sqrt(len / 7)));
      pf[a] += (str[a] || 0) * (len / 7);
      pf[b] += (str[b] || 0) * (len / 7);
      todo.push([a, b, Math.max(0.02, Math.min(0.98, p))]);
    });
  });
  var seed = 20262027;
  var rnd = function rnd() {
    seed = seed + 0x6d2b79f5 | 0;
    var t = Math.imul(seed ^ seed >>> 15, 1 | seed);
    t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
    return ((t ^ t >>> 14) >>> 0) / 4294967296;
  };
  var N = 2000,
    cut = Math.min(6, ids.length - 1),
    inN = {};
  ids.forEach(function (id) {
    return inN[id] = 0;
  });
  var _loop6 = function _loop6() {
    var w = Object.assign({}, w0);
    for (var j = 0; j < todo.length; j++) {
      var m = todo[j];
      if (rnd() < m[2]) w[m[0]]++;else w[m[1]]++;
    }
    var order = ids.slice().sort(function (a, b) {
      return w[b] - w[a] || pf[b] - pf[a];
    });
    for (var r = 0; r < cut; r++) inN[order[r]]++;
  };
  for (var k = 0; k < N; k++) {
    _loop6();
  }
  var out = {};
  ids.forEach(function (id) {
    return out[id] = inN[id] / N;
  });
  return {
    odds: out,
    cut: cut
  };
}
function LeaguePage(_ref161) {
  var s = _ref161.s,
    wk = _ref161.wk,
    go = _ref161.go;
  var K = s.blend,
    gen = (window.ESPN_DATA || {}).generated;
  var _useState159 = useState("st"),
    _useState160 = _slicedToArray(_useState159, 2),
    by = _useState160[0],
    setBy = _useState160[1];
  var _useState161 = useState(null),
    _useState162 = _slicedToArray(_useState161, 2),
    sim = _useState162[0],
    setSim = _useState162[1];
  var T = leagueTable(s);
  useEffect(function () {
    var id = setTimeout(function () {
      try {
        setSim(leagueSim(s));
      } catch (e) {
        setSim(null);
      }
    }, 500);
    return function () {
      return clearTimeout(id);
    };
  }, [s.players, s.weeks, s.wk, s.blend, window.__PMODE]);
  var wins = function wins(x) {
    return x.rec.w + x.rec.t / 2;
  };
  var stand = _toConsumableArray(T.rows).sort(function (a, b) {
    return wins(b) - wins(a) || b.rec.pf - a.rec.pf || b.strength - a.strength;
  });
  var list = by === "st" ? stand : T.rows;
  var cut = sim ? sim.cut : 6;
  var myOpp = oppOf(wk, s.me);
  var all = [[s.me, myOpp || s.opp]].concat((wk.pairs || []).filter(function (p) {
    return p[0] && p[1] && p[0] !== s.me && p[1] !== s.me;
  })).filter(function (p) {
    return p[0] && p[1];
  });
  var games = useMemo(function () {
    return all.map(function (_ref162) {
      var _ref163 = _slicedToArray(_ref162, 2),
        a = _ref163[0],
        b = _ref163[1];
      var R = function R(id) {
          return weekLive(s.players.filter(function (p) {
            return p.ft === id;
          }), wk, K, id);
        },
        act = function act(id) {
          return +(wk.act || {})[id] || 0;
        };
      return {
        a: a,
        b: b,
        sa: act(a),
        sb: act(b),
        p: winProb(R(a), R(b), act(a), act(b))
      };
    });
  }, [s.players, wk, K, gen, s.opp]);
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
    onClick: function onClick() {
      return setBy("st");
    }
  }, "Standings"), /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: by === "pw" ? "on" : "",
    onClick: function onClick() {
      return setBy("pw");
    }
  }, "Strength"))), /*#__PURE__*/React.createElement("div", {
    className: "gx-lt text-xs text-slate-500",
    style: {
      borderTop: 0,
      paddingTop: 0
    }
  }, /*#__PURE__*/React.createElement("span", null), /*#__PURE__*/React.createElement("span", null), /*#__PURE__*/React.createElement("span", {
    className: "n"
  }, "Record"), /*#__PURE__*/React.createElement("span", {
    className: "n m-hide"
  }, "Points"), /*#__PURE__*/React.createElement("span", {
    className: "n m-hide"
  }, "Strength"), /*#__PURE__*/React.createElement("span", {
    className: "n"
  }, "Playoffs")), list.map(function (x, i) {
    var me = x.t.id === s.me,
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
  }, "This week"), games.length ? games.map(function (g, i) {
    var la = g.p >= 0.5;
    return /*#__PURE__*/React.createElement("div", {
      key: g.a + "-" + g.b,
      className: "gx-lm",
      role: "button",
      style: i ? null : {
        borderTop: 0
      },
      onClick: function onClick() {
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
    onClick: function onClick() {
      return go("league", "playoffs");
    }
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
function SetupPage(_ref164) {
  var s = _ref164.s,
    setS = _ref164.setS,
    go = _ref164.go,
    sub = _ref164.sub;
  // setup v67: a short list with summaries, each row opens its own page (news_logos.py)
  // older done markers kept: ["best", "Best" + (s.pbest | <GxAlertPrefs /> | href="ai-history.html"
  var E = window.ESPN_DATA,
    Sg = E && E.signals;
  var _useState163 = useState(""),
    _useState164 = _slicedToArray(_useState163, 2),
    msg = _useState164[0],
    setMsg = _useState164[1];
  var _useState165 = useState(null),
    _useState166 = _slicedToArray(_useState165, 2),
    al = _useState166[0],
    setAl = _useState166[1];
  useEffect(function () {
    var dead = false;
    gxAlLoad().then(function (x) {
      if (!dead) setAl(x);
    });
    return function () {
      dead = true;
    };
  }, []);
  var K = s.blend,
    theme = window.__themePref ? window.__themePref() : "auto";
  var seg = function seg(items, value, onPick) {
    return /*#__PURE__*/React.createElement("span", {
      className: "gx-seg"
    }, items.map(function (_ref165) {
      var _ref166 = _slicedToArray(_ref165, 3),
        k = _ref166[0],
        l = _ref166[1],
        off = _ref166[2];
      return /*#__PURE__*/React.createElement("button", {
        key: k,
        type: "button",
        disabled: !!off,
        className: value === k ? "on" : "",
        onClick: function onClick() {
          return onPick(k);
        }
      }, l);
    }));
  };
  var num = function num(k, v, fb) {
    return setS(function (x) {
      return _defineProperty({}, k, isNaN(parseFloat(v)) ? fb : parseFloat(v));
    });
  };
  var roster = s.players.filter(function (p) {
    return p.ft === s.me && !p.ir;
  }).sort(function (a, b) {
    return effAvg(b, K) - effAvg(a, K);
  });
  var top = s.protectTop ?? 8,
    autoIds = new Set(roster.slice(0, top).map(function (p) {
      return p.id;
    }));
  var kept = roster.filter(function (p) {
      return p.keep && !autoIds.has(p.id);
    }),
    addable = roster.filter(function (p) {
      return !p.keep && !autoIds.has(p.id);
    });
  var keep = function keep(id, v) {
    return setS(function (x) {
      return {
        ...x,
        players: x.players.map(function (p) {
          return p.id === id ? {
            ...p,
            keep: v
          } : p;
        })
      };
    });
  };
  var src = [["ESPN league", !!E], ["GM model", !!(E && E.model)], ["betting lines", !!(E && E.model && E.model.odds && Object.keys(E.model.odds).length)], ["recent form", !!(Sg && Sg.recent)], ["power-play units", !!(Sg && Sg.pp1)], ["news", !!(Sg && Sg.news)], ["injuries", !!(Sg && Sg.injuries)], ["starting goalies", !!(E && E.goalies)]];
  var bad = src.filter(function (x) {
    return !x[1];
  }).map(function (x) {
    return x[0];
  });
  var genAt = E && toDate(E.generated),
    old = genAt ? (Date.now() - genAt.getTime()) / 36e5 > 2 : true;
  var download = function download() {
    var blob = new Blob([JSON.stringify(s)], {
      type: "application/json"
    });
    var a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = "fantasy-gm-backup-" + todayISO() + ".json";
    a.click();
    setMsg("Backup downloaded.");
  };
  var upload = function upload(e) {
    var f = e.target.files && e.target.files[0];
    if (!f) return;
    var r = new FileReader();
    r.onload = function () {
      try {
        var v = JSON.parse(r.result);
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
  var newsN = s.players.filter(function (p) {
    return p.ft === s.me && newsOf(p).length;
  }).length;
  var box = inp + " text-sm";
  var PM = {
    espn: "ESPN",
    blend: "Blend",
    model: "GM model",
    ai: "AI"
  };
  var projTxt = s.pbest ? "Best projection (" + (PM[window.__PMODE] || "ESPN") + ")" : (PM[window.__PMODE] || "ESPN") + " projections";
  var themeTxt = theme === "auto" ? "Automatic theme" : theme === "light" ? "Light theme" : "Dark theme";
  var ast = al ? gxAlertState(al.p) : null,
    alog = al ? gxAlertLog(al.b) : [];
  var lastSent = alog.find(function (m) {
    return !m.held && !m.wait;
  });
  var alertTxt = !ast ? "Checking..." : ast.filter(function (x) {
    return x.on;
  }).length + " on \xB7 " + ast.filter(function (x) {
    return !x.on;
  }).length + " off" + (lastSent ? " \xB7 last sent " + gxWhen(lastSent.at) : "");
  var outN = s.players.filter(function (p) {
    return p.ft === s.me && (p.ir || p.status && p.status !== "ACTIVE");
  }).length;
  var syncTxt = E ? "Synced " + (genAt ? genAt.toLocaleTimeString([], {
    hour: "numeric",
    minute: "2-digit"
  }) : "") : "No data file found";
  var refresh = function refresh() {
    window.location.href = window.location.pathname + "?v=" + Date.now();
  };
  var btn = "border border-slate-300 rounded-lg px-3 py-1 text-sm";
  var row = function row(k, title, sumTxt, fn, i) {
    /* gx072-row */
    var ext = k === "ailab" ? "ai-dashboard.html" : k === "history" ? "ai-history.html" : "";
    var href = ext || (k === "news" ? "#news" : gxHash("setup", k));
    return /*#__PURE__*/React.createElement("a", {
      key: k,
      href: href,
      target: ext ? "_blank" : undefined,
      rel: ext ? "noopener" : undefined,
      className: "gx-lk",
      style: i ? null : {
        borderTop: 0
      },
      onClick: function onClick(e) {
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
  var page = function page(title, kids) {
    return /*#__PURE__*/React.createElement("div", {
      className: "space-y-3"
    }, /*#__PURE__*/React.createElement("div", {
      className: "font-semibold",
      style: {
        fontSize: 17
      }
    }, title), /*#__PURE__*/React.createElement("div", {
      className: "gx-pn"
    }, kids));
  };
  if (sub === "display") return page("Display", /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("div", {
    className: "gx-sr",
    style: {
      borderTop: 0
    }
  }, /*#__PURE__*/React.createElement("span", null, "Theme"), seg([["auto", "Automatic"], ["light", "Light"], ["dark", "Dark"]], theme, function (k) {
    return window.__setTheme && window.__setTheme(k);
  })), /*#__PURE__*/React.createElement("div", {
    className: "gx-sr"
  }, /*#__PURE__*/React.createElement("span", null, "Projections"), seg([["best", "Best" + (s.pbest ? " (" + ({
    espn: "ESPN",
    blend: "Blend",
    model: "GM model",
    ai: "AI"
  }[window.__PMODE] || "") + ")" : ""), !window.__MODEL], ["espn", "ESPN"], ["blend", "Blend", !window.__MODEL], ["model", "GM model", !window.__MODEL], ["ai", "AI", !window.__MODEL || !window.__AI]], s.pbest ? "best" : window.__PMODE, function (k) {
    return k === "best" ? setS({
      ...s,
      pbest: true
    }) : setS({
      ...s,
      pbest: false,
      pmode: k,
      players: _toConsumableArray(s.players)
    });
  })), /*#__PURE__*/React.createElement("div", {
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
    onChange: function onChange(e) {
      return num("minGain", e.target.value, 3);
    }
  }), " points")), /*#__PURE__*/React.createElement("div", {
    className: "gx-sr"
  }, /*#__PURE__*/React.createElement("span", null, "Never suggest dropping my top"), /*#__PURE__*/React.createElement("span", null, /*#__PURE__*/React.createElement("select", {
    className: box,
    value: top,
    onChange: function onChange(e) {
      return setS(function (x) {
        return {
          ...x,
          protectTop: +e.target.value
        };
      });
    }
  }, _toConsumableArray(Array(13)).map(function (_, n) {
    return /*#__PURE__*/React.createElement("option", {
      key: n,
      value: n
    }, n);
  })), " players")), /*#__PURE__*/React.createElement("div", {
    className: "gx-sr"
  }, /*#__PURE__*/React.createElement("span", null, "Also protect"), /*#__PURE__*/React.createElement("span", {
    className: "flex flex-wrap gap-2 items-center justify-end"
  }, kept.map(function (p) {
    return /*#__PURE__*/React.createElement("span", {
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
      onClick: function onClick() {
        return keep(p.id, false);
      }
    }, "\xD7"));
  }), addable.length ? /*#__PURE__*/React.createElement("select", {
    className: box,
    value: "",
    onChange: function onChange(e) {
      if (e.target.value) keep(e.target.value, true);
    }
  }, /*#__PURE__*/React.createElement("option", {
    value: ""
  }, "+ add a player"), addable.map(function (p) {
    return /*#__PURE__*/React.createElement("option", {
      key: p.id,
      value: p.id
    }, p.n + " (" + p.p + ")");
  })) : null)), /*#__PURE__*/React.createElement("div", {
    className: "gx-sr"
  }, /*#__PURE__*/React.createElement("span", null, "Always keep at least"), /*#__PURE__*/React.createElement("span", {
    className: "flex gap-2 items-center"
  }, /*#__PURE__*/React.createElement("input", {
    type: "number",
    className: box + " w-14",
    value: s.minF ?? 10,
    onChange: function onChange(e) {
      return num("minF", e.target.value, 10);
    }
  }), " F", /*#__PURE__*/React.createElement("input", {
    type: "number",
    className: box + " w-14",
    value: s.minD ?? 5,
    onChange: function onChange(e) {
      return num("minD", e.target.value, 5);
    }
  }), " D", /*#__PURE__*/React.createElement("input", {
    type: "number",
    className: box + " w-14",
    value: s.minGo ?? 2,
    onChange: function onChange(e) {
      return num("minGo", e.target.value, 2);
    }
  }), " G"))));
  if (sub === "players") return page("Players and injuries", /*#__PURE__*/React.createElement(React.Fragment, null, row("inj", "Injury return dates", outN ? outN + " of your players hurt or on IR" : "Everyone on your team is healthy", function () {
    return go("setup", "inj");
  }, 0), row("bulk", "Edit players", "Projections, play %, fantasy team", function () {
    return go("setup", "bulk");
  }, 1)));
  if (sub === "league") return page("League info", /*#__PURE__*/React.createElement(React.Fragment, null, row("news", "News", newsN ? newsN + " of your players in the news" : "Nothing new on your players", function () {
    return go("news");
  }, 0), row("odds", "Betting lines", "Win chances and expected goals for each game", function () {
    return go("setup", "odds");
  }, 1), row("sched", "Schedule", "Games per NHL team this week", function () {
    return go("setup", "sched");
  }, 2)));
  if (sub === "data") return page("Data and backup", /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("div", {
    className: "gx-sr",
    style: {
      borderTop: 0
    }
  }, /*#__PURE__*/React.createElement("span", null, syncTxt), /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: btn,
    onClick: refresh
  }, "Refresh")), bad.length ? bad.map(function (l) {
    return /*#__PURE__*/React.createElement("div", {
      key: l,
      className: "gx-sr"
    }, /*#__PURE__*/React.createElement("span", null, l.charAt(0).toUpperCase() + l.slice(1)), /*#__PURE__*/React.createElement("span", {
      className: "text-sm",
      style: {
        color: "var(--bad)"
      }
    }, "Not working"));
  }) : /*#__PURE__*/React.createElement("div", {
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
    onChange: function onChange(e) {
      return setS({
        ...s,
        wk: +e.target.value
      });
    }
  }, s.weeks.map(function (w, i) {
    return /*#__PURE__*/React.createElement("option", {
      key: i,
      value: i
    }, w.label);
  }))), row("adv", "Advanced settings", "Team names, projection weight, reset", function () {
    return go("setup", "adv");
  }, 1)));
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
  }, syncTxt + " \xB7 " + (!E ? "check GitHub Actions" : bad.length ? bad.length + " data source" + (bad.length === 1 ? "" : "s") + " not working" : old ? "data is over 2 hours old" : "everything working")), /*#__PURE__*/React.createElement("button", {
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
  }, row("display", "Display", themeTxt + " \xB7 " + projTxt, function () {
    return go("setup", "display");
  }, 0), row("rules", "Pickup rules", "Moves must add " + (s.minGain ?? 3) + "+ points \xB7 top " + top + " protected" + (kept.length ? " plus " + kept.length + " more" : ""), function () {
    return go("setup", "rules");
  }, 1), row("alerts", "Phone alerts", alertTxt, function () {
    return go("setup", "alerts");
  }, 2), row("players", "Players and injuries", "Injury return dates \xB7 edit players", function () {
    return go("setup", "players");
  }, 3), row("league", "League info", "News \xB7 betting lines \xB7 NHL schedule", function () {
    return go("setup", "league");
  }, 4), row("data", "Data and backup", (bad.length ? "Not working: " + bad.join(", ") : "All " + src.length + " data sources working") + " \xB7 backup \xB7 advanced", function () {
    return go("setup", "data");
  }, 5), row("ailab", "AI Lab", "How each projection is doing", function () {
    return window.open("ai-dashboard.html", "_blank");
  }, 6), row("history", "Prediction history", "Every projection and what happened", function () {
    return window.open("ai-history.html", "_blank");
  }, 7)));
}

// ---------- round 45: tappable rows work from the keyboard too (news_logos.py) ----------
(function gxA11y() {
  if (window.__gxA11y) return;
  window.__gxA11y = 1;
  var fix = function fix() {
    return document.querySelectorAll('[role="button"]:not([tabindex])').forEach(function (el) {
      return el.setAttribute("tabindex", "0");
    });
  };
  var q = 0;
  try {
    new MutationObserver(function () {
      if (q) return;
      q = requestAnimationFrame(function () {
        q = 0;
        fix();
      });
    }).observe(document.documentElement, {
      childList: true,
      subtree: true
    });
  } catch (e) {}
  document.addEventListener("keydown", function (e) {
    var el = document.activeElement;
    if (e.defaultPrevented || !(e.key === "Enter" || e.key === " ")) return;
    if (el && el.getAttribute && el.getAttribute("role") === "button" && el.tagName !== "BUTTON") {
      e.preventDefault();
      el.click();
    }
  });
})();

// ---------- round 46: every matchup's score in a strip above the Matchup page (news_logos.py) ----------
function MatchStrip(_ref168) {
  var s = _ref168.s,
    wk = _ref168.wk;
  var _useState167 = useState(window.__matchSel || 0),
    _useState168 = _slicedToArray(_useState167, 2),
    cur = _useState168[0],
    setCur = _useState168[1];
  useEffect(function () {
    var h = function h() {
      return setCur(window.__matchSel || 0);
    };
    window.addEventListener("gm-match", h);
    return function () {
      return window.removeEventListener("gm-match", h);
    };
  }, []);
  var myOpp = oppOf(wk, s.me);
  var all = [[s.me, myOpp || s.opp]].concat((wk.pairs || []).filter(function (p) {
    return p[0] && p[1] && p[0] !== s.me && p[1] !== s.me;
  })).filter(function (p) {
    return p[0] && p[1];
  });
  if (all.length < 2) return null;
  var sc = function sc(id) {
    return +(wk.act || {})[id] || 0;
  };
  var nm = function nm(id) {
    var w = (teamName(s, id) || "").split(" ")[0];
    return w.length > 10 ? w.slice(0, 9) + "\u2026" : w;
  };
  return /*#__PURE__*/React.createElement("div", {
    className: "gx-ms",
    role: "tablist",
    "aria-label": "Matchups this week"
  }, all.map(function (_ref169, i) {
    var _ref170 = _slicedToArray(_ref169, 2),
      a = _ref170[0],
      b = _ref170[1];
    var x = sc(a),
      y = sc(b);
    return /*#__PURE__*/React.createElement("button", {
      key: a + "-" + b,
      type: "button",
      role: "tab",
      "aria-selected": i === cur,
      className: i === cur ? "on" : "",
      onClick: function onClick(e) {
        if (window.__setMatch) window.__setMatch(i);
        e.currentTarget.scrollIntoView({
          behavior: "smooth",
          inline: "center",
          block: "nearest"
        });
      }
    }, nm(a), " ", x >= y ? /*#__PURE__*/React.createElement("b", null, f1(x)) : f1(x), " ", /*#__PURE__*/React.createElement("span", {
      style: {
        opacity: 0.6
      }
    }, "vs"), " ", y > x ? /*#__PURE__*/React.createElement("b", null, f1(y)) : f1(y), " ", nm(b));
  }));
}

// ---------- round 50: warning dots, search, bottom tabs, swipe days, home-screen icon (news_logos.py) ----------
function gxWarn(s) {
  var o = {
    myteam: false,
    matchup: false
  };
  try {
    var today = todayISO(),
      wk = deriveWeek(s.weeks[s.wk], s.autoDone),
      mine = s.players.filter(function (p) {
        return p.ft === s.me && !p.ir;
      });
    var open = function open(p) {
      var g = gStart(p, today),
        l = (g.l || "").toLowerCase();
      return g.v >= 0.5 && !(l.includes("confirmed") && !l.includes("un"));
    };
    o.myteam = false && mine.some(function (p) {
      return p.status && /OUT|INJURY_RESERVE|SUSPENSION/.test(p.status);
    }) || mine.some(function (p) {
      return p.p === "G" && SCHED[p.t] && SCHED[p.t].has(today) && gState(p.t, today).s === "P" && open(p);
    });
    var opp = oppOf(wk, s.me) || s.opp,
      a = +(wk.act || {})[s.me] || 0,
      b = +(wk.act || {})[opp] || 0,
      sign = String(a === b ? 0 : a > b ? 1 : -1);
    var key = "gm-lead-" + s.wk,
      seen = localStorage.getItem(key);
    window.__leadNow = [key, sign];
    if (seen == null) localStorage.setItem(key, sign);else o.matchup = sign !== "0" && seen !== sign;
  } catch (e) {}
  return o;
}
var GX_ICON = {
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
function GxExtras(_ref171) {
  var s = _ref171.s,
    tab = _ref171.tab,
    go = _ref171.go;
  var _useState169 = useState(false),
    _useState170 = _slicedToArray(_useState169, 2),
    open = _useState170[0],
    setOpen = _useState170[1];
  var _useState171 = useState(""),
    _useState172 = _slicedToArray(_useState171, 2),
    q = _useState172[0],
    setQ = _useState172[1];
  var K = s.blend,
    W = gxWarn(s);
  useEffect(function () {
    var show = function show() {
      setQ("");
      setOpen(true);
    };
    var key = function key(e) {
      var el = document.activeElement,
        typing = el && /INPUT|TEXTAREA|SELECT/.test(el.tagName);
      if (e.key === "/" && !typing) {
        e.preventDefault();
        show();
      }
      if (e.key === "Escape") setOpen(false);
    };
    window.addEventListener("gm-search", show);
    document.addEventListener("keydown", key);
    return function () {
      window.removeEventListener("gm-search", show);
      document.removeEventListener("keydown", key);
    };
  }, []);
  useEffect(function () {
    if (tab === "matchup" && window.__leadNow) {
      try {
        localStorage.setItem(window.__leadNow[0], window.__leadNow[1]);
      } catch (e) {}
    }
  }, [tab, s.lastSync]);
  useEffect(function () {
    // lift the floating Ask button above the bottom tabs on phones
    var fix = function fix() {
      if (window.innerWidth > 640) return;
      Array.prototype.forEach.call(document.querySelectorAll("button, a"), function (b) {
        if ((b.textContent || "").trim() === "Ask" && getComputedStyle(b).position === "fixed") b.style.bottom = "calc(74px + env(safe-area-inset-bottom))";
      });
    };
    fix();
    var id = setInterval(fix, 2000);
    return function () {
      return clearInterval(id);
    };
  }, []);
  var TABS = [["today", "Today", ["today"]], ["matchup", "Matchup", ["matchup"]], ["myteam", "Team", ["myteam", "moves", "lines"]], ["league", "League", ["league", "teams"]], ["setup", "Setup", ["setup", "news"]]];
  var qq = nrm(q);
  var teams = qq.length < 2 ? [] : s.teams.filter(function (t) {
    return nrm(t.name || "").includes(qq);
  }).slice(0, 4);
  var players = qq.length < 2 ? [] : s.players.filter(function (p) {
    return nrm(p.n).includes(qq);
  }).sort(function (a, b) {
    return (nrm(b.n).indexOf(qq) === 0) - (nrm(a.n).indexOf(qq) === 0) || (b.own || 0) - (a.own || 0);
  }).slice(0, 10);
  var svg = function svg(k) {
    return /*#__PURE__*/React.createElement("svg", {
      viewBox: "0 0 24 24",
      fill: "none",
      stroke: "currentColor",
      strokeWidth: "1.6",
      strokeLinecap: "round",
      strokeLinejoin: "round",
      "aria-hidden": "true"
    }, GX_ICON[k]);
  };
  return /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("nav", {
    className: "gx-bb",
    "aria-label": "Main"
  }, TABS.map(function (_ref172) {
    var _ref173 = _slicedToArray(_ref172, 3),
      k = _ref173[0],
      l = _ref173[1],
      grp = _ref173[2];
    return /*#__PURE__*/React.createElement("button", {
      key: k,
      type: "button",
      className: grp.indexOf(tab) >= 0 ? "on" : "",
      onClick: function onClick() {
        return go(k, k === "setup" ? "settings" : k === "league" ? "power" : undefined);
      }
    }, svg(k), l, W[k] ? /*#__PURE__*/React.createElement("i", {
      className: "gx-wd"
    }) : null);
  }), /*#__PURE__*/React.createElement("button", {
    type: "button",
    onClick: function onClick() {
      setQ("");
      setOpen(true);
    }
  }, svg("search"), "Search")), open ? /*#__PURE__*/React.createElement("div", {
    className: "gx-so",
    role: "dialog",
    "aria-label": "Search",
    onClick: function onClick() {
      return setOpen(false);
    }
  }, /*#__PURE__*/React.createElement("div", {
    className: "gx-sbx",
    onClick: function onClick(e) {
      return e.stopPropagation();
    }
  }, /*#__PURE__*/React.createElement("input", {
    autoFocus: true,
    className: inp + " w-full",
    placeholder: "Search a player or a team",
    value: q,
    onChange: function onChange(e) {
      return setQ(e.target.value);
    }
  }), teams.map(function (t) {
    return /*#__PURE__*/React.createElement("div", {
      key: t.id,
      role: "button",
      className: "gx-row",
      style: {
        cursor: "pointer"
      },
      onClick: function onClick() {
        setOpen(false);
        if (window.__NAV && window.__NAV.team) window.__NAV.team(t.id);
      }
    }, /*#__PURE__*/React.createElement("span", {
      style: {
        flex: 1
      }
    }, t.name), /*#__PURE__*/React.createElement("span", {
      className: "text-xs text-slate-500"
    }, "fantasy team"));
  }), players.map(function (p) {
    return /*#__PURE__*/React.createElement("div", {
      key: p.id,
      role: "button",
      className: "gx-row",
      style: {
        cursor: "pointer"
      },
      onClick: function onClick() {
        setOpen(false);
        if (window.__NAV) window.__NAV.player(p);
      }
    }, /*#__PURE__*/React.createElement(TeamLogo, {
      t: p.t,
      size: 22
    }), /*#__PURE__*/React.createElement("span", {
      className: "min-w-0 truncate",
      style: {
        flex: 1
      }
    }, p.n, " ", /*#__PURE__*/React.createElement("span", {
      className: "text-xs text-slate-500"
    }, p.p + " \xB7 " + (p.ft === "fa" ? "free agent" : teamName(s, p.ft)))), /*#__PURE__*/React.createElement("span", {
      style: {
        fontVariantNumeric: "tabular-nums"
      }
    }, f1(effAvg(p, K))));
  }), qq.length >= 2 && !teams.length && !players.length ? /*#__PURE__*/React.createElement("div", {
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
  var x0 = 0,
    y0 = 0,
    ok = false;
  document.addEventListener("touchstart", function (e) {
    var t = e.touches[0];
    x0 = t.clientX;
    y0 = t.clientY;
    ok = !(e.target.closest && e.target.closest(".gx-ms, .navscroll, .overflow-x-auto, .gx-so, .gx-bb, input, select"));
  }, {
    capture: true,
    passive: true
  });
  document.addEventListener("touchend", function (e) {
    if (!ok || window.innerWidth > 640) return;
    var t = e.changedTouches[0],
      dx = t.clientX - x0,
      dy = t.clientY - y0;
    if (Math.abs(dx) < 70 || Math.abs(dy) > 50) return;
    var cur = document.querySelector(".gx-day.on");
    if (!cur) return;
    e.stopPropagation();
    var nxt = dx < 0 ? cur.nextElementSibling : cur.previousElementSibling;
    if (nxt && nxt.classList.contains("gx-day")) nxt.click();
  }, {
    capture: true
  });
  try {
    var c = document.createElement("canvas");
    c.width = c.height = 180;
    var g = c.getContext("2d");
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
    var l = document.createElement("link");
    l.rel = "apple-touch-icon";
    l.href = c.toDataURL("image/png");
    document.head.appendChild(l);
  } catch (e) {}
})();

// ---------- round 51: watchlist and quick actions (news_logos.py) ----------
var gxWatch = {
  list: function list() {
    try {
      return JSON.parse(localStorage.getItem("gm-watch") || "[]");
    } catch (e) {
      return [];
    }
  },
  has: function has(id) {
    return gxWatch.list().indexOf(id) >= 0;
  },
  toggle: function toggle(id) {
    var l = gxWatch.list(),
      i = l.indexOf(id);
    if (i >= 0) l.splice(i, 1);else l.push(id);
    try {
      localStorage.setItem("gm-watch", JSON.stringify(l));
    } catch (e) {}
    window.dispatchEvent(new Event("gm-watch"));
  }
};
function GxWatchPanel(_ref174) {
  var s = _ref174.s;
  var _useState173 = useState(0),
    _useState174 = _slicedToArray(_useState173, 2),
    tick = _useState174[1];
  useEffect(function () {
    var h = function h() {
      return tick(function (x) {
        return x + 1;
      });
    };
    window.addEventListener("gm-watch", h);
    return function () {
      return window.removeEventListener("gm-watch", h);
    };
  }, []);
  var K = s.blend,
    list = gxWatch.list().map(function (id) {
      return s.players.find(function (p) {
        return p.id === id;
      });
    }).filter(Boolean);
  if (!list.length) return null;
  var note = function note(p) {
    if (p.ft !== "fa") return "now on " + teamName(s, p.ft);
    var g = sigOf(p),
      fr = formRatio(p, K);
    return g.lines && g.lines.chg === "up" ? "moved up a line" : g.ppChg === "added" ? "new on the top power play" : g.lines && g.lines.chg === "down" ? "moved down a line" : fr !== null && fr >= 1.25 ? "hot" : fr !== null && fr <= 0.7 ? "cold" : "";
  };
  return /*#__PURE__*/React.createElement(GxPanel, {
    title: "Watchlist"
  }, list.map(function (p, i) {
    return /*#__PURE__*/React.createElement("div", {
      key: p.id,
      className: "gx-row",
      style: i ? null : {
        borderTop: 0
      }
    }, /*#__PURE__*/React.createElement(TeamLogo, {
      t: p.t,
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
      onClick: function onClick() {
        return gxWatch.toggle(p.id);
      }
    }, "\xD7"));
  }));
}
function GxQA(_ref175) {
  var s = _ref175.s,
    go = _ref175.go;
  var lid = (window.ESPN_DATA || {}).leagueId || 1363781006,
    num = function num(x) {
      return String(x).replace(/\D/g, "");
    };
  window.__QA = {
    mine: function mine(p) {
      return p.ft === s.me;
    },
    fa: function fa(p) {
      return p.ft === "fa";
    },
    tradeable: function tradeable(p) {
      return p.ft !== "fa";
    },
    swap: function swap(p) {
      if (p.ft === "fa") window.__PICK_Q = p.n;else window.__PICK_POS = p.p;
      go("moves", "adddrop");
      setTimeout(function () {
        return window.dispatchEvent(new Event("gm-pick"));
      }, 50);
    },
    trade: function trade(p) {
      window.__TRADE_P = {
        id: p.id,
        ft: p.ft
      };
      go("moves", "trades");
      setTimeout(function () {
        return window.dispatchEvent(new Event("gm-trade"));
      }, 50);
    },
    lines: function lines(p) {
      if (window.__NAV && window.__NAV.lines) window.__NAV.lines(p.t);else go("lines");
    },
    espn: function espn(p) {
      try {
        if (navigator.clipboard) navigator.clipboard.writeText(p.n);
      } catch (e) {}
      window.open(p.ft === "fa" ? "https://fantasy.espn.com/hockey/players/add?leagueId=" + lid + "&teamId=" + num(s.me) : "https://fantasy.espn.com/hockey/team?leagueId=" + lid + "&teamId=" + num(p.ft), "_blank");
    },
    star: function star(p) {
      return gxWatch.toggle(p.id);
    },
    starred: function starred(p) {
      return gxWatch.has(p.id);
    }
  };
  return null;
}

// ---------- round 52: keep the floating Ask button clear of the bottom tabs (news_logos.py) ----------
(function gxAsk() {
  if (window.__gxAsk) return;
  window.__gxAsk = 1;
  var box = null;
  var lift = function lift(el) {
    var n = el;
    while (n && n !== document.body && n !== document.documentElement) {
      if (getComputedStyle(n).position === "fixed") {
        n.style.setProperty("bottom", "calc(72px + env(safe-area-inset-bottom))", "important");
        return n;
      }
      n = n.parentElement;
    }
    return null;
  };
  var run = function run() {
    var root = document.documentElement;
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
    var all = document.querySelectorAll("button, a, div, span");
    for (var i = 0; i < all.length && !box; i++) {
      var el = all[i],
        leaf = el.tagName === "BUTTON" || el.tagName === "A" || !el.childElementCount;
      if (!leaf || el.closest && el.closest(".gx-bb, .gx-so")) continue;
      if ((el.textContent || "").trim() === "Ask") box = lift(el);
    }
    root.classList.toggle("gx-noask", !box);
  };
  setTimeout(run, 300);
  setInterval(run, 1500);
  window.addEventListener("resize", run);
})();

// ---------- round 56: the Roster table for any fantasy team (news_logos.py) ----------
function GxRosterTable(_ref176) {
  var s = _ref176.s,
    wk = _ref176.wk,
    tid = _ref176.tid;
  var K = s.blend,
    today = todayISO(),
    gen = (window.ESPN_DATA || {}).generated;
  var _useState175 = useState("pg"),
    _useState176 = _slicedToArray(_useState175, 2),
    sort = _useState176[0],
    setSort = _useState176[1];
  var _useState177 = useState({}),
    _useState178 = _slicedToArray(_useState177, 2),
    hist = _useState178[0],
    setHist = _useState178[1];
  var roster = s.players.filter(function (p) {
    return p.ft === tid;
  });
  var pv = function pv(p) {
    return effAvg(p, K) * (p.p === "G" ? p.prob : 1);
  };
  var dates = wk.dates || [];
  var nextW = s.weeks[s.wk + 1] ? deriveWeek(s.weeks[s.wk + 1], s.autoDone) : null;
  var _mu2 = useMemo(function () {
    var P = pby(),
      o = {};
    dates.forEach(function (dt) {
      var AD = actDay(tid, dt);
      if (!AD) return;
      Object.entries(AD).forEach(function (_ref177) {
        var _ref178 = _slicedToArray(_ref177, 2),
          pid = _ref178[0],
          v = _ref178[1];
        if (!v || v[0] == null || !ESLOT[v[1]]) return;
        var p = P["e" + pid];
        if (!p || !(SCHED[p.t] && SCHED[p.t].has(dt)) || gState(p.t, dt).s === "P" || p.p === "G" && !v[0]) return;
        o[p.id] = (o[p.id] || 0) + v[0];
      });
    });
    return o;
  }, [s.players, wk, gen, tid]);
  var total = Object.values(_mu2).reduce(function (a, v) {
    return a + Math.max(0, v);
  }, 0);
  var rankOf = useMemo(function () {
    var o = {};
    ["F", "D", "G"].forEach(function (k) {
      s.players.filter(function (p) {
        return p.p === k && p.prob > 0 && (p.proj !== false || p.gp > 0);
      }).map(function (p) {
        return [p.id, pv(p)];
      }).sort(function (a, b) {
        return b[1] - a[1];
      }).forEach(function (x, i) {
        return o[x[0]] = i + 1;
      });
    });
    return o;
  }, [s.players, K, window.__PMODE]);
  var roles = useMemo(function () {
    var L = window.LINES_DATA,
      o = {};
    if (!L || !L.teams) return o;
    var key = function key(x) {
      return nrm(x).replace(/[.'\u2019]/g, "").replace(/-/g, " ").replace(/\s+/g, " ").trim();
    };
    roster.forEach(function (p) {
      var ln = (L.teams[p.t] || {}).lines;
      if (!ln) return;
      var k = key(p.n),
        has = function has(sl) {
          return (ln[sl] || []).some(function (x) {
            return key(x) === k;
          });
        };
      o[p.id] = {
        es: ["F1", "F2", "F3", "F4", "D1", "D2", "D3", "G"].find(has),
        pp: ["PP1", "PP2"].find(has)
      };
    });
    return o;
  }, [s.players, tid, (window.LINES_DATA || {}).generated]);
  useEffect(function () {
    var dead = false;
    var E = window.ESPN_DATA || {},
      out = {},
      byId = {};
    roster.forEach(function (p) {
      return byId[String(p.id).slice(1)] = p;
    });
    Object.entries(E.daily || {}).forEach(function (_ref179) {
      var _ref180 = _slicedToArray(_ref179, 2),
        d = _ref180[0],
        Tm = _ref180[1];
      return Object.values(Tm || {}).forEach(function (tm) {
        return Object.entries(tm || {}).forEach(function (_ref181) {
          var _ref182 = _slicedToArray(_ref181, 2),
            pid = _ref182[0],
            v = _ref182[1];
          var p = byId[pid];
          if (!p || !v || v[0] == null || !(SCHED[p.t] && SCHED[p.t].has(d)) || gState(p.t, d).s === "P" || p.p === "G" && !v[0]) return;
          (out[pid] = out[pid] || {})[d] = v[0];
        });
      });
    });
    var finish = function finish() {
      if (dead) return;
      var h = {};
      Object.keys(out).forEach(function (pid) {
        h[pid] = Object.keys(out[pid]).sort().slice(-5).map(function (d) {
          return out[pid][d];
        });
      });
      setHist(h);
    };
    finish();
    gxBoxIdx().then(function (ds) {
      return Promise.all(ds.slice(-14).map(function (d) {
        return gxBoxDay(d).then(function (day) {
          return [d, day];
        });
      }));
    }).then(function (days) {
      days.forEach(function (_ref183) {
        var _ref184 = _slicedToArray(_ref183, 2),
          d = _ref184[0],
          day = _ref184[1];
        if (!day) return;
        Object.keys(byId).forEach(function (pid) {
          var x = day[pid];
          if (x) {
            var o2 = out[pid] = out[pid] || {};
            o2[d] = x.fp != null ? x.fp : o2[d] != null ? o2[d] : gxEst(x, s.sc || {});
          } else if (out[pid]) delete out[pid][d];
        });
      });
      finish();
    }).catch(function () {});
    return function () {
      dead = true;
    };
  }, [s.players, gen, tid]);
  var RO = {
    F1: "L1",
    F2: "L2",
    F3: "L3",
    F4: "L4",
    D1: "D1",
    D2: "D2",
    D3: "D3"
  };
  var roleTxt = function roleTxt(p) {
    if (p.p === "G") return Math.round(p.prob * 100) + "% of starts";
    var r = roles[p.id];
    return r ? [r.es ? RO[r.es] : "not in lineup", r.pp].filter(Boolean).join(" \xB7 ") : "";
  };
  var nextGame = function nextGame(p) {
    var S = SCHED[p.t];
    if (!S || p.ir) return "";
    for (var i = 0; i < 10; i++) {
      var dt = addDays(today, i);
      if (S.has(dt) && (i > 0 || gState(p.t, dt).s === "P")) {
        var gm = gameOf(p.t, dt);
        return (i === 0 ? "Today" : dayLabel(dt).split(",")[0]) + (gm ? (gm.h ? " vs " : " @ ") + gm.o : "");
      }
    }
    return "";
  };
  var left = function left(p) {
    return (wk.games[p.t] || []).filter(function (d) {
      return dates[d] >= today && gState(p.t, dates[d]).s === "P";
    }).length;
  };
  var nextG = function nextG(p) {
    return nextW ? gms(nextW, p.t) : 0;
  };
  var keyFn = {
    mu: function mu(p) {
      return _mu2[p.id] || 0;
    },
    left: left,
    next: nextG,
    sea: function sea(p) {
      return p.gp ? p.tot / p.gp : -99;
    },
    pg: pv,
    rk: function rk(p) {
      return -(rankOf[p.id] || 9999);
    }
  }[sort];
  var grp = function grp(k) {
    return roster.filter(function (p) {
      return !p.ir && p.p === k;
    }).sort(function (a, b) {
      return keyFn(b) - keyFn(a);
    });
  };
  var groups = [["Forwards", grp("F")], ["Defence", grp("D")], ["Goalies", grp("G")], ["Injured reserve", roster.filter(function (p) {
    return p.ir;
  })]].filter(function (x) {
    return x[1].length;
  });
  var HB = function HB(k, l, cls) {
    return /*#__PURE__*/React.createElement("button", {
      type: "button",
      className: "n " + (cls || "") + (sort === k ? " on" : ""),
      onClick: function onClick() {
        return setSort(sort === k ? "pg" : k);
      }
    }, l);
  };
  var row = function row(p) {
    var st = p.ir ? "IR" : p.status && p.status !== "ACTIVE" ? M_ST[p.status] || p.status.replace(/_/g, " ") : "";
    var m = _mu2[p.id],
      sea = p.gp ? p.tot / p.gp : null,
      gap = sea != null && p.avg > 0 ? sea - p.avg : null,
      rk = rankOf[p.id];
    var sub = [roleTxt(p), nextGame(p)].filter(Boolean).join(" \xB7 "),
      h = hist[String(p.id).slice(1)] || [];
    return /*#__PURE__*/React.createElement("div", {
      key: p.id,
      className: "gx-ro"
    }, /*#__PURE__*/React.createElement(TeamLogo, {
      t: p.t,
      size: 26
    }), /*#__PURE__*/React.createElement("div", {
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
    }, sub) : null), /*#__PURE__*/React.createElement("div", {
      className: "gx-sp m-hide",
      title: "Last five games, oldest to newest"
    }, h.length ? h.map(function (v, i) {
      return /*#__PURE__*/React.createElement("i", {
        key: i,
        style: {
          height: Math.max(2, Math.min(22, Math.max(0, v) / 20 * 22)),
          background: v < 0 ? "var(--bad)" : "var(--ink2)"
        }
      });
    }) : /*#__PURE__*/React.createElement("span", {
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
    }, sea == null ? "\u2013" : /*#__PURE__*/React.createElement(React.Fragment, null, f1(sea), gap != null ? /*#__PURE__*/React.createElement("span", {
      className: "text-xs",
      style: {
        marginLeft: 6,
        color: gap >= 0 ? "var(--good)" : "var(--bad)"
      }
    }, (gap >= 0 ? "+" : "") + f1(gap)) : null)), /*#__PURE__*/React.createElement("div", {
      className: "n"
    }, f1(effAvg(p, K))), /*#__PURE__*/React.createElement("div", {
      className: "n text-xs text-slate-500 m-hide"
    }, rk ? p.p + " " + ordN(rk) : "\u2013"));
  };
  return /*#__PURE__*/React.createElement("div", {
    className: "gx-pn"
  }, /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("b", null), /*#__PURE__*/React.createElement("div", {
    className: "gx-ro gx-roh"
  }, /*#__PURE__*/React.createElement("span", null), /*#__PURE__*/React.createElement("span", null, "Tap a heading to sort"), /*#__PURE__*/React.createElement("span", {
    className: "n m-hide"
  }, "Last 5"), HB("mu", "Matchup"), HB("left", "Left"), HB("next", "Next wk", "m-hide"), HB("sea", "So far", "m-hide"), HB("pg", "Expected"), HB("rk", "Rank", "m-hide")), groups.map(function (_ref185) {
    var _ref186 = _slicedToArray(_ref185, 2),
      title = _ref186[0],
      list = _ref186[1];
    return /*#__PURE__*/React.createElement("div", {
      key: title,
      style: {
        marginBottom: 10
      }
    }, /*#__PURE__*/React.createElement("div", {
      className: "gx-tag",
      style: {
        padding: "8px 0 4px"
      }
    }, title), list.map(row));
  }));
}

// ---------- round 58: Best projection and phone alert switches (news_logos.py) ----------
function GxBest(_ref187) {
  var s = _ref187.s,
    setS = _ref187.setS;
  useEffect(function () {
    if (!s.pbest) return;
    var dead = false;
    var MAP = {
      espn: "espn",
      gm: "model",
      blend: "blend",
      ai: "ai"
    };
    var use = function use(m) {
      var k = MAP[m] || "ai";
      if (k === "ai" && !window.__AI || k !== "espn" && !window.__MODEL) k = window.__MODEL ? "model" : "espn";
      if (!dead) setS(function (st) {
        return st.pmode === k ? st : {
          ...st,
          pmode: k,
          players: _toConsumableArray(st.players)
        };
      });
    };
    var c = null;
    try {
      c = JSON.parse(localStorage.getItem("gm-best") || "null");
    } catch (e) {}
    if (c && c.d === todayISO() && c.m) {
      use(c.m);
      return;
    }
    fetch("ai/report.json?t=" + Date.now()).then(function (r) {
      return r.ok ? r.json() : null;
    }).then(function (j) {
      var m = j && j.best && j.best.skater && j.best.skater.model;
      if (!m) return;
      try {
        localStorage.setItem("gm-best", JSON.stringify({
          d: todayISO(),
          m: m
        }));
      } catch (e) {}
      use(m);
    }).catch(function () {});
    return function () {
      dead = true;
    };
  }, [s.pbest]);
  return null;
}
// ---------- round 61: any week on two Today boxes (news_logos.py) ----------
var gxSpan61 = function gxSpan61(ds) {
  if (!ds || !ds.length) return "";
  var a = ds[0],
    b = ds[ds.length - 1];
  return mdL(a) + " to " + (fromIso(a).getMonth() === fromIso(b).getMonth() ? fromIso(b).getDate() : mdL(b));
};
var gxWkName61 = function gxWkName61(s, k) {
  return k === s.wk ? "This week" : k === s.wk + 1 ? "Next week" : "Week " + (k + 1);
};
var gxWkAt61 = function gxWkAt61(s, pick) {
  return pick == null ? s.wk : Math.max(0, Math.min(s.weeks.length - 1, pick));
};
var gxSwipe61 = function gxSwipe61(ref, i, go) {
  return {
    onTouchStart: function onTouchStart(e) {
      var t = e.touches[0];
      ref.current = [t.clientX, t.clientY];
    },
    onTouchEnd: function onTouchEnd(e) {
      var t0 = ref.current,
        t = e.changedTouches[0];
      ref.current = null;
      if (!t0 || e.target.closest && e.target.closest("select, button")) return;
      var dx = t.clientX - t0[0],
        dy = t.clientY - t0[1];
      if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy) * 1.5) go(i + (dx < 0 ? 1 : -1));
    }
  };
};
var GxWkPick = function GxWkPick(_ref188) {
  var s = _ref188.s,
    i = _ref188.i,
    go = _ref188.go;
  return /*#__PURE__*/React.createElement("span", {
    className: "gx-wpk"
  }, /*#__PURE__*/React.createElement("button", {
    type: "button",
    "aria-label": "Earlier week",
    disabled: i <= 0,
    onClick: function onClick() {
      return go(i - 1);
    }
  }, "\u2039"), /*#__PURE__*/React.createElement("select", {
    "aria-label": "Choose a week",
    value: i,
    onChange: function onChange(e) {
      return go(+e.target.value);
    }
  }, s.weeks.map(function (w, k) {
    return /*#__PURE__*/React.createElement("option", {
      key: k,
      value: k
    }, gxWkName61(s, k));
  })), /*#__PURE__*/React.createElement("button", {
    type: "button",
    "aria-label": "Later week",
    disabled: i >= s.weeks.length - 1,
    onClick: function onClick() {
      return go(i + 1);
    }
  }, "\u203A"));
};
function GxGamesAny(_ref189) {
  var s = _ref189.s,
    wk = _ref189.wk,
    A = _ref189.A,
    B = _ref189.B;
  var K = s.blend,
    today = todayISO();
  var _useState179 = useState(null),
    _useState180 = _slicedToArray(_useState179, 2),
    pick = _useState180[0],
    setPick = _useState180[1];
  var touch = React.useRef(null);
  var i = gxWkAt61(s, pick),
    cur = i === s.wk;
  var go = function go(k) {
    return setPick(Math.max(0, Math.min(s.weeks.length - 1, k)));
  };
  var w = useMemo(function () {
    return cur ? wk : deriveWeek(s.weeks[i], s.autoDone);
  }, [cur, wk, s.weeks, i, s.autoDone]);
  var dates = w.dates || [],
    opp = oppOf(w, s.me) || (cur ? s.opp : null);
  var fin = !cur && dates.length > 0 && dates[dates.length - 1] < today;
  var N = useMemo(function () {
    if (cur || fin || !opp || !dates.length) return null;
    var R = function R(id) {
      return weekLive(s.players.filter(function (p) {
        return p.ft === id;
      }), w, K, id);
    };
    return [R(s.me), R(opp)];
  }, [cur, fin, opp, w, s.players, K, window.__PMODE]);
  var X = cur ? A : N ? N[0] : null,
    Y = cur ? B : N ? N[1] : null;
  var rows = X && Y ? dates.map(function (dt, d) {
    return {
      dt: dt,
      a: ((X.days[d] || {}).start || []).length,
      b: ((Y.days[d] || {}).start || []).length
    };
  }) : [];
  var tot = function tot(k, from) {
    return rows.reduce(function (x, r) {
      return x + (r.dt >= from ? r[k] : 0);
    }, 0);
  };
  var mx = Math.max(1, Math.max.apply(null, rows.map(function (r) {
    return Math.max(r.a, r.b);
  })));
  var live = dates.length > 0 && dates[0] <= today && dates[dates.length - 1] >= today;
  var sa = +(w.act || {})[s.me] || 0,
    sb = opp ? +(w.act || {})[opp] || 0 : 0;
  var sub = [opp ? "vs " + teamName(s, opp) : "", gxSpan61(dates), fin ? "final" : rows.length ? "lineup games: you " + tot("a", "") + ", them " + tot("b", "") : "", !fin && live && rows.length ? "from today " + tot("a", today) + " and " + tot("b", today) : ""].filter(Boolean).join(" \xB7 ");
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
  }, rows.map(function (r) {
    var now = r.dt === today,
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
function GxLeagueAny(_ref190) {
  var s = _ref190.s,
    wk = _ref190.wk;
  var K = s.blend,
    gen = (window.ESPN_DATA || {}).generated,
    today = todayISO();
  var _useState181 = useState(null),
    _useState182 = _slicedToArray(_useState181, 2),
    pick = _useState182[0],
    setPick = _useState182[1];
  var touch = React.useRef(null);
  var i = gxWkAt61(s, pick),
    cur = i === s.wk;
  var go = function go(k) {
    return setPick(Math.max(0, Math.min(s.weeks.length - 1, k)));
  };
  var w = useMemo(function () {
    return cur ? wk : deriveWeek(s.weeks[i], s.autoDone);
  }, [cur, wk, s.weeks, i, s.autoDone]);
  var dates = w.dates || [];
  var fin = !cur && dates.length > 0 && dates[dates.length - 1] < today;
  var rows = useMemo(function () {
    return (w.pairs || []).filter(function (p) {
      return p[0] && p[1] && p[0] !== s.me && p[1] !== s.me;
    }).map(function (_ref191) {
      var _ref192 = _slicedToArray(_ref191, 2),
        a = _ref192[0],
        b = _ref192[1];
      var act = function act(id) {
        return +(w.act || {})[id] || 0;
      };
      if (fin) return {
        a: a,
        b: b,
        sa: act(a),
        sb: act(b)
      };
      var R = function R(id) {
        return weekLive(s.players.filter(function (p) {
          return p.ft === id;
        }), w, K, id);
      };
      return {
        a: a,
        b: b,
        p: winProb(R(a), R(b), act(a), act(b))
      };
    });
  }, [s.players, w, fin, K, gen, window.__PMODE]);
  var sub = cur ? "Win chance right now" : [gxSpan61(dates), fin ? "final scores" : "projected win chance from today's rosters"].filter(Boolean).join(" \xB7 ");
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
  }, sub), rows.length ? rows.map(function (r, k) {
    var p = fin ? r.sa + r.sb > 0 ? r.sa / (r.sa + r.sb) : 0.5 : r.p;
    var la = fin ? r.sa >= r.sb : p >= 0.5,
      close = !fin && Math.abs(p - 0.5) < 0.1;
    var bar = function bar(win) {
      return win ? "var(--good)" : "var(--bad)";
    };
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
var GX_AL = [["Lineup warnings", "starter_is_out", "Starter is out", "An injured player is in your lineup with a game today", "injuries"], ["Lineup warnings", "possible_scratch", "Possible scratch", "A starter is missing from tonight's lineup, within 3 hours of the game", "injuries"], ["Lineup warnings", "goalie_not_starting", "Goalie not starting", "Your goalie is not tonight's starter", "goalies"], ["Lineup warnings", "goalie_not_confirmed", "Goalie not confirmed", "75 minutes before the game and still not confirmed", "goalies"], ["Lineup warnings", "bench_player_has_a_game", "Bench player has a game", "A bench player plays while a starter does not", ""], ["Your players", "your_player_line_change", "Line change", "Moved up or down a line", "lines"], ["Your players", "your_player_lineup_change", "In or out of the lineup", "Added to or missing from his team's lineup", "lines"], ["Your players", "your_player_power_play_change", "Power-play change", "On or off a power-play unit", "lines"], ["Your players", "your_player_roster_move", "Roster move", "Traded, called up or sent down", "lines"], ["Your players", "your_player_injury_update", "Injury update", "ESPN injury status changed", "injuries"], ["Your players", "your_player_losing_ice_time", "Losing ice time", "Down 3 or more minutes a game lately", "lines"], ["Your players", "more_line_changes", "Extra line changes", "Several changes at once, sent as one message", "lines"], ["Pickup ideas", "pickup_bigger_role", "Bigger role", "A free agent moved to a top-six line or the top pair", "pickups"], ["Pickup ideas", "pickup_new_pp1", "New on the top power play", "A free agent just moved onto PP1", "pickups"], ["Pickup ideas", "pickup_ice_time_jump", "Ice time jump", "A free agent's minutes went up a lot", "pickups"], ["Pickup ideas", "pickup_trending", "Trending free agent", "Other managers are adding him fast", "pickups"], ["Summaries", "morning_summary", "Morning summary", "8 a.m., everything that waited overnight", ""], ["Summaries", "pregame_summary", "Before puck drop", "An hour before your first game, only if something new came in", ""]];
var GX_AL_MASTER = [["injuries", "Injuries"], ["lines", "Line and power-play changes"], ["goalies", "Goalie starts"], ["pickups", "Pickup ideas"]];
var GX_AL_TITLES = [["Lineup: starter is OUT", "starter_is_out"], ["Possible scratch tonight", "possible_scratch"], ["Your player: injury update", "your_player_injury_update"], ["Lineup: bench player has a game", "bench_player_has_a_game"], ["Goalie not starting tonight", "goalie_not_starting"], ["Goalie not confirmed yet", "goalie_not_confirmed"], ["Your player's line changed", "your_player_line_change"], ["Your player: lineup change", "your_player_lineup_change"], ["Your player: power-play change", "your_player_power_play_change"], ["Your player: roster move", "your_player_roster_move"], ["Your player is losing ice time", "your_player_losing_ice_time"], ["Pickup: new PP1 free agent", "pickup_new_pp1"], ["Pickup: ice time jump", "pickup_ice_time_jump"], ["Pickup: trending free agent", "pickup_trending"], ["Pickup idea: bigger role", "pickup_bigger_role"], ["Morning summary", "morning_summary"], ["Before puck drop", "pregame_summary"]];
var GX_PREFS_URL = "https://github.com/dhaliwal32/23456789786634356/edit/main/alert_prefs.json";
var gxAlKind = function gxAlKind(title) {
  var t = String(title || "");
  if (t.indexOf("roster/line changes") >= 0) return "more_line_changes";
  var m = GX_AL_TITLES.find(function (x) {
    return t.indexOf(x[0]) === 0;
  });
  return m ? m[1] : null;
};
var gxAlertState = function gxAlertState(p) {
  return GX_AL.map(function (_ref193) {
    var _ref194 = _slicedToArray(_ref193, 5),
      sec = _ref194[0],
      k = _ref194[1],
      label = _ref194[2],
      desc = _ref194[3],
      g = _ref194[4];
    var own = p && p[k] != null ? p[k] : k !== "bench_player_has_a_game";
    var gOff = !!(g && p && p[g] === false);
    var gl = (GX_AL_MASTER.find(function (x) {
      return x[0] === g;
    }) || [])[1];
    return {
      sec: sec,
      k: k,
      label: label,
      desc: desc,
      on: own !== false && !gOff,
      why: own === false ? "" : gOff ? "off by the " + gl + " master switch" : ""
    };
  });
};
var gxAlertLog = function gxAlertLog(b) {
  var out = [],
    LBL = {
      urgent: "Sent right away",
      morning: "Morning summary",
      pregame: "Before puck drop"
    };
  (b && b.log || []).forEach(function (m) {
    return out.push({
      at: m.at,
      title: m.title,
      body: m.body,
      status: LBL[m.kind] || m.kind || "Sent",
      held: /^Not sent/.test(m.kind || "")
    });
  });
  (b && b.items || []).forEach(function (i) {
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
  return out.sort(function (a, c) {
    return String(a.at || "") < String(c.at || "") ? 1 : -1;
  });
};
var gxWhen = function gxWhen(iso) {
  var d = toDate(iso);
  if (!d) return "";
  var t = d.toLocaleTimeString([], {
    hour: "numeric",
    minute: "2-digit"
  });
  var k = function k(x) {
      return x.toDateString();
    },
    now = new Date(),
    y = new Date(Date.now() - 864e5);
  return (k(d) === k(now) ? "Today " : k(d) === k(y) ? "Yesterday " : d.toLocaleDateString("en-US", {
    weekday: "short",
    month: "short",
    day: "numeric"
  }).replace(",", "") + " ") + t;
};
var gxAlLoad = function gxAlLoad() {
  return Promise.all([fetch("alert_prefs.json?t=" + Date.now()).then(function (r) {
    return r.ok ? r.json() : null;
  }).catch(function () {
    return null;
  }), fetch("notify_outbox.json?t=" + Date.now()).then(function (r) {
    return r.ok ? r.json() : null;
  }).catch(function () {
    return null;
  })]).then(function (_ref195) {
    var _ref196 = _slicedToArray(_ref195, 2),
      p = _ref196[0],
      b = _ref196[1];
    return {
      p: p,
      b: b
    };
  });
};
function GxAlertsPage() {
  // alerts page v67 (news_logos.py)
  var _useState183 = useState(null),
    _useState184 = _slicedToArray(_useState183, 2),
    d = _useState184[0],
    setD = _useState184[1];
  var _useState185 = useState("all"),
    _useState186 = _slicedToArray(_useState185, 2),
    f = _useState186[0],
    setF = _useState186[1];
  var _useState187 = useState(30),
    _useState188 = _slicedToArray(_useState187, 2),
    lim = _useState188[0],
    setLim = _useState188[1];
  useEffect(function () {
    var dead = false;
    var load = function load() {
      return gxAlLoad().then(function (x) {
        if (!dead) setD(x);
      });
    };
    load();
    var id = setInterval(load, 2 * 60 * 1000);
    return function () {
      dead = true;
      clearInterval(id);
    };
  }, []);
  if (!d) return /*#__PURE__*/React.createElement("div", {
    className: "text-sm text-slate-500"
  }, "Loading your phone alerts...");
  var st = gxAlertState(d.p),
    log = gxAlertLog(d.b);
  var cut = new Date(Date.now() - 7 * 864e5).toISOString().slice(0, 19) + "Z";
  var cnt = {};
  log.forEach(function (m) {
    if (m.held || m.wait || String(m.at || "") < cut) return;
    var k = gxAlKind(m.title);
    if (k) cnt[k] = (cnt[k] || 0) + 1;
  });
  var shown = log.filter(function (m) {
    return f === "all" ? true : f === "held" ? m.held : f === "wait" ? m.wait : !m.held && !m.wait;
  });
  var onN = st.filter(function (x) {
    return x.on;
  }).length;
  var chip = function chip(m) {
    var c = m.held ? "var(--mute)" : m.wait ? "var(--warn)" : "var(--good)";
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
  }, "Switches \xB7 " + onN + " on, " + (st.length - onN) + " off"), /*#__PURE__*/React.createElement("a", {
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
  }, "Change opens the settings file on GitHub. Set a line to false to switch it off, then commit. It applies at the next sync, within 30 minutes. Nothing is sent from 11 p.m. to 7 a.m."), ["Lineup warnings", "Your players", "Pickup ideas", "Summaries"].map(function (sec) {
    return /*#__PURE__*/React.createElement("div", {
      key: sec
    }, /*#__PURE__*/React.createElement("div", {
      className: "text-xs text-slate-500",
      style: {
        margin: "12px 0 2px",
        letterSpacing: ".04em"
      }
    }, sec), st.filter(function (x) {
      return x.sec === sec;
    }).map(function (x, i) {
      return /*#__PURE__*/React.createElement("div", {
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
      }, x.desc + " \xB7 " + (cnt[x.k] || 0) + " in the last 7 days" + (x.why ? " \xB7 " + x.why : ""))), /*#__PURE__*/React.createElement("span", {
        className: "text-sm",
        style: {
          color: x.on ? "var(--good)" : "var(--mute)"
        }
      }, x.on ? "On" : "Off"));
    }));
  }), /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500",
    style: {
      margin: "12px 0 2px",
      letterSpacing: ".04em"
    }
  }, "Master switches"), GX_AL_MASTER.map(function (_ref197, i) {
    var _ref198 = _slicedToArray(_ref197, 2),
      k = _ref198[0],
      l = _ref198[1];
    var on = !(d.p && d.p[k] === false);
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
    }, " \xB7 turns its whole group on or off")), /*#__PURE__*/React.createElement("span", {
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
  }, [["all", "All"], ["sent", "Sent"], ["held", "Held back"], ["wait", "Waiting"]].map(function (_ref199) {
    var _ref200 = _slicedToArray(_ref199, 2),
      k = _ref200[0],
      l = _ref200[1];
    return /*#__PURE__*/React.createElement("button", {
      key: k,
      type: "button",
      className: f === k ? "on" : "",
      onClick: function onClick() {
        setF(k);
        setLim(30);
      }
    }, l);
  }))), shown.length ? shown.slice(0, lim).map(function (m, i) {
    var k = gxAlKind(m.title);
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
    }, gxWhen(m.at), k ? /*#__PURE__*/React.createElement(React.Fragment, null, " \xB7 ", /*#__PURE__*/React.createElement("a", {
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
    onClick: function onClick() {
      return setLim(lim + 30);
    }
  }, "Show more") : null));
}

// change 069: old unused pages removed
// ---------- change 070: This week box as a score race, any week (install.py) ----------
function GxRace(_ref201) {
  var s = _ref201.s,
    wk = _ref201.wk;
  var K = s.blend,
    today = todayISO(),
    gen = (window.ESPN_DATA || {}).generated;
  var _useState189 = useState(null),
    _useState190 = _slicedToArray(_useState189, 2),
    pick = _useState190[0],
    setPick = _useState190[1];
  var _useState191 = useState(null),
    _useState192 = _slicedToArray(_useState191, 2),
    sel = _useState192[0],
    setSel = _useState192[1];
  var _useState193 = useState(620),
    _useState194 = _slicedToArray(_useState193, 2),
    W = _useState194[0],
    setW = _useState194[1];
  var box = React.useRef(null);
  var touch = React.useRef(null);
  useEffect(function () {
    var el = box.current;
    if (!el) return;
    var fit = function fit() {
      return setW(Math.max(290, Math.round(el.clientWidth - 28)));
    };
    fit();
    if (window.ResizeObserver) {
      var ro = new ResizeObserver(fit);
      ro.observe(el);
      return function () {
        return ro.disconnect();
      };
    }
    window.addEventListener("resize", fit);
    return function () {
      return window.removeEventListener("resize", fit);
    };
  }, []);
  useEffect(function () {
    var h = function h() {
      setPick(Math.min(s.weeks.length - 1, s.wk + 1));
      setSel(null);
      if (box.current) box.current.scrollIntoView({
        behavior: "smooth",
        block: "start"
      });
    };
    window.addEventListener("gx-race-next", h);
    return function () {
      return window.removeEventListener("gx-race-next", h);
    };
  }, [s.wk, s.weeks.length]);
  var i = gxWkAt61(s, pick),
    cur = i === s.wk;
  var go = function go(k) {
    setPick(Math.max(0, Math.min(s.weeks.length - 1, k)));
    setSel(null);
  };
  var w = useMemo(function () {
    return cur ? wk : deriveWeek(s.weeks[i], s.autoDone);
  }, [cur, wk, s.weeks, i, s.autoDone]);
  var dates = w.dates || [],
    n = dates.length;
  var opp = oppOf(w, s.me) || (cur ? s.opp : null);
  var up = !(n > 0 && dates[0] <= today),
    fin = !cur && n > 0 && dates[n - 1] < today;
  var R = useMemo(function () {
    if (!opp || !n || fin) return null;
    var run = function run(id) {
      return weekLive(s.players.filter(function (p) {
        return p.ft === id;
      }), w, K, id, {
        detail: true
      });
    };
    return [run(s.me), run(opp)];
  }, [w, opp, fin, s.players, K, gen, window.__PMODE]);
  var mv = useMemo(function () {
    if (!up || !opp || !R) return null;
    try {
      var sW = {
        ...s,
        wk: i
      };
      var r = computeMoves(sW, {
        H: 1,
        pool: 40
      }).res.filter(function (x) {
        return x.gain >= (s.minGain ?? 3);
      })[0];
      if (!r) return {
        none: true
      };
      return {
        r: r,
        b: winChance(sW),
        a: winChance(sW, afterMove(sW, r.f, r.d))
      };
    } catch (e) {
      return null;
    }
  }, [up, i, opp, R]);
  var act = function act(id) {
    return +(w.act || {})[id] || 0;
  };
  var sa = up ? 0 : act(s.me),
    sb = up || !opp ? 0 : act(opp);
  var nm0 = opp ? (teamName(s, opp) || "").split(" ")[0] : "",
    nm = nm0.length > 10 ? nm0.slice(0, 9) + "\u2026" : nm0;
  var title = cur ? "This week" : up && i === s.wk + 1 ? "Next week" : "Week " + (i + 1);
  var head = /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      alignItems: "center",
      gap: 8,
      flexWrap: "wrap"
    }
  }, /*#__PURE__*/React.createElement("span", {
    className: "gx-tag"
  }, title, opp ? " \xB7 vs " + teamName(s, opp) : ""), /*#__PURE__*/React.createElement(GxWkPick, {
    s: s,
    i: i,
    go: go
  }));
  var wrapP = {
    className: "gx-pn",
    ref: box,
    style: {
      minWidth: 0,
      touchAction: "pan-y"
    },
    ...gxSwipe61(touch, i, go)
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
  var X = R[0],
    Y = R[1];
  var st = function st(d) {
    return dates[d] < today ? "f" : dates[d] === today ? "t" : "p";
  };
  var pts = function pts(L, d) {
    var x = L.days[d] || {},
      k = st(d);
    return k === "f" ? x.act || 0 : k === "t" ? (x.act || 0) + (x.total || 0) : x.total || 0;
  };
  var exp = function exp(L, d) {
    var x = L.days[d] || {};
    return x.proj != null ? x.proj : x.total || 0;
  };
  var me = dates.map(function (_, d) {
      return pts(X, d);
    }),
    th = dates.map(function (_, d) {
      return pts(Y, d);
    });
  var cum = function cum(a) {
    var t = 0;
    return a.map(function (v) {
      return t += v;
    });
  };
  var CA = cum(me),
    CB = cum(th);
  var fdays = dates.map(function (_, d) {
      return d;
    }).filter(function (d) {
      return st(d) === "f";
    }),
    done = fdays.length;
  var EA = cum(dates.map(function (_, d) {
      return exp(X, d);
    })),
    EB = cum(dates.map(function (_, d) {
      return exp(Y, d);
    }));
  var wp = winProb(X, Y, sa, sb),
    fa = sa + X.total,
    fb = sb + Y.total;
  var ti = dates.indexOf(today),
    d0 = sel != null && sel < n ? sel : ti >= 0 ? ti : up ? 0 : n - 1;
  var narrow = W < 480,
    gut = narrow ? 80 : 108,
    L0 = 4,
    R0 = W - gut,
    cw = (R0 - L0) / n,
    cx = function cx(d) {
      return L0 + cw * (d + 0.5);
    };
  var topV = Math.max(CA[n - 1], CB[n - 1], done ? Math.max(EA[done - 1], EB[done - 1]) : 0, 1) * 1.06;
  var base = 172,
    yy = function yy(v) {
      return base - v / topV * 158;
    },
    Hh = narrow ? 230 : 214;
  var P = function P(a, from, to) {
    return a.slice(from, to + 1).map(function (v, k) {
      return cx(from + k).toFixed(1) + "," + yy(v).toFixed(1);
    }).join(" ");
  };
  var ln = function ln(col, dash, wdt, op) {
    return {
      fill: "none",
      stroke: col,
      strokeWidth: wdt || 2,
      strokeDasharray: dash || "none",
      strokeLinejoin: "round",
      strokeLinecap: "round",
      opacity: op || 1
    };
  };
  var segs = [];
  for (var k = 0; k < n - 1; k++) {
    var ah = CA[k + 1] >= CB[k + 1];
    segs.push(/*#__PURE__*/React.createElement("polygon", {
      key: "g" + k,
      points: [cx(k) + "," + yy(CA[k]), cx(k + 1) + "," + yy(CA[k + 1]), cx(k + 1) + "," + yy(CB[k + 1]), cx(k) + "," + yy(CB[k])].join(" "),
      style: {
        fill: ah ? "var(--good)" : "var(--bad)",
        opacity: 0.1
      }
    }));
  }
  var ya = yy(CA[n - 1]) + 4,
    yb = yy(CB[n - 1]) + 4;
  if (Math.abs(ya - yb) < 15) {
    var m = (ya + yb) / 2,
      sg1 = ya <= yb ? -1 : 1;
    ya = m + sg1 * 7.5;
    yb = m - sg1 * 7.5;
  }
  ya = Math.max(12, ya);
  yb = Math.max(12, yb);
  var lx = cx(n - 1) + 12,
    fs = narrow ? 11 : 12;
  var sg = function sg(v) {
    return (v >= 0 ? "+" : "\u2212") + Math.round(Math.abs(v));
  };
  var DN = function DN(d) {
    return dates[d] === today ? "Today" : dayLabel(dates[d]).split(",")[0];
  };
  var rng = up || !done ? dates.map(function (_, d) {
    return d;
  }) : fdays;
  var won = rng.filter(function (d) {
    return me[d] > th[d];
  }).length;
  var bD = rng.reduce(function (b, d) {
    return b == null || me[d] - th[d] > me[b] - th[b] ? d : b;
  }, null);
  var bestTxt = bD != null && me[bD] > th[bD] ? "best " + DN(bD) + " " + sg(me[bD] - th[bD]) : "";
  var vsA = fdays.reduce(function (t, d) {
      return t + me[d] - exp(X, d);
    }, 0),
    vsB = fdays.reduce(function (t, d) {
      return t + th[d] - exp(Y, d);
    }, 0);
  var gms = function gms(L, d) {
    return ((L.days[d] || {}).start || []).length;
  };
  var totG = function totG(L) {
    return dates.reduce(function (t, _, d) {
      return t + gms(L, d);
    }, 0);
  };
  var topOf = function topOf(L) {
    var t = ((L || {}).start || []).filter(function (p) {
      return p.x > 0;
    }).sort(function (a, b) {
      return b.x - a.x;
    })[0];
    return t ? shortN(t.n) + " " + f1(t.x) : "\u2013";
  };
  var fact = function fact(key, label, big, sub, col) {
    return /*#__PURE__*/React.createElement("div", {
      key: key
    }, /*#__PURE__*/React.createElement("small", null, label), /*#__PURE__*/React.createElement("b", {
      style: col ? {
        color: col
      } : null
    }, big), sub ? /*#__PURE__*/React.createElement("span", {
      className: "text-sm text-slate-500"
    }, " " + sub) : null);
  };
  var facts = up ? [fact("g", "Lineup games", totG(X), "them " + totG(Y)), fact("d", "Days favoured", won + " of " + n, bestTxt), fact("m", "Best move", mv ? mv.none ? "None worth it" : lastN(mv.r.f.n) + " in" : "\u2026", mv && !mv.none ? lastN(mv.r.d.n) + " out" + (mv.a != null && mv.b != null ? " \xB7 " + wpTxt(mv.b).replace("%", "") + " \u2192 " + wpTxt(mv.a) : "") : "")] : [done ? fact("v", "Against projection", sg(vsA), "them " + sg(vsB), vsA >= 0 ? "var(--good)" : "var(--bad)") : fact("g", "Lineup games", totG(X), "them " + totG(Y)), fact("l", "Lineup games left", X.used, "them " + Y.used), done ? fact("w", "Days won", won + " of " + done, bestTxt) : fact("d", "Days favoured", won + " of " + n, bestTxt)];
  var k0 = st(d0),
    m0 = me[d0] - th[d0],
    x0 = X.days[d0] || {},
    y0 = Y.days[d0] || {};
  var mc = function mc(v) {
    return {
      color: v >= 0 ? "var(--good)" : "var(--bad)"
    };
  };
  return /*#__PURE__*/React.createElement("div", wrapP, head, /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500",
    style: {
      marginTop: 4
    }
  }, (done >= n ? "Final " : "Projected ") + Math.round(fa) + " \u2013 " + Math.round(fb) + " \xB7 ", /*#__PURE__*/React.createElement("span", {
    style: {
      color: wp >= 0.5 ? "var(--good)" : "var(--bad)"
    }
  }, wpTxt(wp) + " to win")), /*#__PURE__*/React.createElement("svg", {
    viewBox: "0 0 " + W + " " + Hh,
    width: "100%",
    className: "gx-svg",
    style: {
      display: "block",
      marginTop: 8
    },
    role: "img",
    "aria-label": "Running total for both teams through the week"
  }, /*#__PURE__*/React.createElement("rect", {
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
  }), segs, done >= 2 ? /*#__PURE__*/React.createElement("polyline", {
    points: P(EB, 0, done - 1),
    style: ln("var(--mute)", "2 4", 1, 0.6)
  }) : null, done >= 2 ? /*#__PURE__*/React.createElement("polyline", {
    points: P(EA, 0, done - 1),
    style: ln("var(--accent)", "2 4", 1, 0.45)
  }) : null, done < n ? /*#__PURE__*/React.createElement("polyline", {
    points: P(CB, Math.max(0, done - 1), n - 1),
    style: ln("var(--mute)", "5 4")
  }) : null, done < n ? /*#__PURE__*/React.createElement("polyline", {
    points: P(CA, Math.max(0, done - 1), n - 1),
    style: ln("var(--accent)", "5 4")
  }) : null, done >= 2 ? /*#__PURE__*/React.createElement("polyline", {
    points: P(CB, 0, done - 1),
    style: ln("var(--mute)")
  }) : null, done >= 2 ? /*#__PURE__*/React.createElement("polyline", {
    points: P(CA, 0, done - 1),
    style: ln("var(--accent)")
  }) : null, fdays.map(function (d) {
    return /*#__PURE__*/React.createElement("g", {
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
    }));
  }), /*#__PURE__*/React.createElement("circle", {
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
  }, nm + " " + Math.round(CB[n - 1])), dates.map(function (dt, d) {
    var on = d === d0,
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
    }, Math.round(th[d])) : null, /*#__PURE__*/React.createElement("rect", {
      x: cx(d) - cw / 2,
      y: 0,
      width: cw,
      height: Hh,
      style: {
        fill: "transparent",
        cursor: "pointer"
      },
      onClick: function onClick() {
        return setSel(d);
      }
    }));
  })), /*#__PURE__*/React.createElement("div", {
    className: "gx-rf"
  }, facts), /*#__PURE__*/React.createElement("div", {
    className: "gx-rt"
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
  }, "Vs expected"), /*#__PURE__*/React.createElement("span", {
    style: mc(me[d0] - exp(X, d0))
  }, sg(me[d0] - exp(X, d0))), /*#__PURE__*/React.createElement("span", {
    style: mc(th[d0] - exp(Y, d0))
  }, sg(th[d0] - exp(Y, d0)))) : null, k0 === "t" ? /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("span", {
    className: "l"
  }, "So far"), /*#__PURE__*/React.createElement("span", null, f1(x0.act || 0)), /*#__PURE__*/React.createElement("span", null, f1(y0.act || 0)), /*#__PURE__*/React.createElement("span", {
    className: "l"
  }, "Projected"), /*#__PURE__*/React.createElement("span", null, f1(me[d0]) + " ", /*#__PURE__*/React.createElement("span", {
    style: mc(m0)
  }, (m0 >= 0 ? "ahead by " : "behind by ") + f1(Math.abs(m0)))), /*#__PURE__*/React.createElement("span", null, f1(th[d0]))) : null, k0 === "p" ? /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("span", {
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
var GX_RT = ["today", "matchup", "myteam", "moves", "lines", "league", "teams", "news", "setup"];
var GX_RDEF = {
  moves: "adddrop",
  league: "power",
  setup: "settings"
};
var GX_TEAM_HREF = {
  roster: "#myteam",
  pickups: "#moves",
  plan: "#moves/planner",
  trades: "#moves/trades",
  lines: "#lines"
};
var gxHash = function gxHash(tab, sub, team, pid) {
  var t = GX_RT.indexOf(tab) >= 0 ? tab : "today";
  var h = "#" + t;
  if (GX_RDEF[t] && sub && sub !== GX_RDEF[t]) h += "/" + sub;
  if (t === "teams" && team) h += "/" + team;
  if (pid) h += "&p=" + encodeURIComponent(pid);
  return h;
};
var gxParseHash = function gxParseHash(h) {
  var m = String(h || "").replace(/^#\/?/, "").split("&p=");
  var parts = m[0].split("/").filter(Boolean),
    tab = parts[0];
  if (!tab || GX_RT.indexOf(tab) < 0) return null;
  var r = {
    tab: tab,
    sub: null,
    team: null,
    pid: m[1] ? decodeURIComponent(m[1]) : null
  };
  if (tab === "teams") r.team = parts[1] || null;else if (GX_RDEF[tab]) r.sub = parts[1] || GX_RDEF[tab];
  return r;
};
var gxNewTab = function gxNewTab(e) {
  return !!(e && (e.metaKey || e.ctrlKey || e.shiftKey || e.button === 1));
};
var gxPHref = function gxPHref(p) {
  var R = window.__ROUTE || {};
  return gxHash(R.tab, R.sub, R.team, p && p.id);
};

// ---------- change 073: settings sync between devices (install.py) ----------
var GX_SYNC_K = "gm-sync-key",
  GX_SYNC_AT = "gm-sync-at";
var GX_SYNC_API = "https://api.github.com/repos/dhaliwal32/23456789786634356/contents/settings.json";
var GX_SYNC_SET = ["pmode", "pbest", "minGain", "protectTop", "minF", "minD", "minGo", "blend", "autoDone", "autoGoalie", "gw", "poStart", "poWeeks"];
var gxSyncKey = function gxSyncKey() {
  try {
    return localStorage.getItem(GX_SYNC_K) || "";
  } catch (e) {
    return "";
  }
};
var gxSyncNote = function gxSyncNote(t) {
  window.__SYNC_ST = t;
  window.dispatchEvent(new Event("gx-sync"));
};
var gxSyncPick = function gxSyncPick(s) {
  var set = {},
    keep = [],
    back = {};
  GX_SYNC_SET.forEach(function (k) {
    if (s[k] !== undefined) set[k] = s[k];
  });
  if (s.pbest) delete set.pmode;
  (s.players || []).forEach(function (p) {
    if (p.keep) keep.push(p.id);
    if (p.back && p.back !== (DEFAULT_BACK[p.n] || "")) back[p.id] = p.back;
  });
  var watch = [];
  try {
    watch = JSON.parse(localStorage.getItem("gm-watch") || "[]") || [];
  } catch (e) {}
  return {
    set: set,
    keep: keep,
    back: back,
    watch: watch,
    hide: gxHide.list() /* gx075-s1 */,
    theme: window.__themePref ? window.__themePref() : "auto"
  };
};
var gxSyncSig = function gxSyncSig(P) {
  var srt = function srt(o) {
    var x = {};
    Object.keys(o || {}).sort().forEach(function (k) {
      return x[k] = o[k];
    });
    return x;
  };
  return JSON.stringify([srt(P.set), (P.keep || []).slice().sort(), srt(P.back), (P.watch || []).slice().sort(), (P.hide || []).slice().sort() /* gx075-s2 */, P.theme || "auto"]);
};
var gxSyncApply = function gxSyncApply(st, R) {
  var next = {
      ...st
    },
    keep = new Set(R.keep || []),
    back = R.back || {};
  GX_SYNC_SET.forEach(function (k) {
    if (R.set && R.set[k] !== undefined) next[k] = R.set[k];
  });
  next.players = (st.players || []).map(function (p) {
    var def = DEFAULT_BACK[p.n] || "";
    var b = back[p.id] != null ? back[p.id] : p.back && p.back !== def ? def : p.back;
    var k = keep.has(p.id);
    return !!p.keep === k && b === p.back ? p : {
      ...p,
      keep: k,
      back: b
    };
  });
  return next;
};
var gxB64 = function gxB64(str) {
  return btoa(unescape(encodeURIComponent(str)));
};
var gxUnB64 = function gxUnB64(b) {
  return decodeURIComponent(escape(atob(String(b || "").replace(/\s/g, ""))));
};
function GxSync(_ref202) {
  var s = _ref202.s,
    setS = _ref202.setS;
  var _useState195 = useState(0),
    _useState196 = _slicedToArray(_useState195, 2),
    tick = _useState196[1];
  var sha = React.useRef(null),
    last = React.useRef(null),
    timer = React.useRef(null),
    ready = React.useRef(false),
    sRef = React.useRef(s);
  sRef.current = s;
  useEffect(function () {
    var h = function h() {
      return tick(function (x) {
        return x + 1;
      });
    };
    window.addEventListener("gm-watch", h);
    window.addEventListener("gm-theme", h);
    window.addEventListener("gm-hide", h); /* gx075-s4 */
    return function () {
      window.removeEventListener("gm-watch", h);
      window.removeEventListener("gm-theme", h);
    };
  }, []);
  var hdr = function hdr(key) {
    return {
      Authorization: "Bearer " + key,
      Accept: "application/vnd.github+json"
    };
  };
  var pull = function pull() {
    var key = gxSyncKey();
    var req = key ? fetch(GX_SYNC_API + "?ref=main&t=" + Date.now(), {
      headers: hdr(key),
      cache: "no-store"
    }).then(function (r) {
      if (r.status === 404) {
        sha.current = null;
        return null;
      }
      if (r.status === 401 || r.status === 403) throw new Error("key");
      if (!r.ok) throw new Error("net");
      return r.json().then(function (j) {
        sha.current = j.sha;
        return JSON.parse(gxUnB64(j.content));
      });
    }) : fetch("settings.json?t=" + Date.now(), {
      cache: "no-store"
    }).then(function (r) {
      return r.ok ? r.json() : null;
    });
    return req.then(function (R) {
      if (!R || !R.at) {
        if (key) gxSyncNote("On \xB7 nothing saved yet");
        return false;
      }
      var seen = "";
      try {
        seen = localStorage.getItem(GX_SYNC_AT) || "";
      } catch (e) {}
      last.current = gxSyncSig(R);
      if (key) gxSyncNote("On \xB7 last change " + gxWhen(R.at));
      if (R.at <= seen) return false;
      try {
        localStorage.setItem(GX_SYNC_AT, R.at);
      } catch (e) {}
      setS(function (st) {
        return gxSyncApply(st, R);
      });
      if (Array.isArray(R.hide)) gxHide.set(R.hide); /* gx075-s3 */
      if (Array.isArray(R.watch)) {
        try {
          localStorage.setItem("gm-watch", JSON.stringify(R.watch));
        } catch (e) {}
        window.dispatchEvent(new Event("gm-watch"));
      }
      if (R.theme && window.__themePref && window.__setTheme && window.__themePref() !== R.theme) window.__setTheme(R.theme);
      return true;
    }).catch(function (e) {
      if (key) gxSyncNote(e && e.message === "key" ? "GitHub refused the key. It needs Contents: Read and write on this repo." : "Could not reach GitHub. Trying again in 2 minutes.");
      return true;
    });
  };
  var push = function push() {
    var key = gxSyncKey();
    if (!key || !ready.current) return;
    var P = gxSyncPick(sRef.current),
      sig = gxSyncSig(P);
    if (sig === last.current) return;
    var body = {
      ...P,
      at: new Date().toISOString()
    };
    var _put = function put(again) {
      return fetch(GX_SYNC_API, {
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
      }).then(function (r) {
        if ((r.status === 409 || r.status === 422) && again) {
          return fetch(GX_SYNC_API + "?ref=main&t=" + Date.now(), {
            headers: hdr(key),
            cache: "no-store"
          }).then(function (g) {
            return g.ok ? g.json() : null;
          }).then(function (j) {
            sha.current = j ? j.sha : null;
            return _put(false);
          });
        }
        if (!r.ok) {
          gxSyncNote(r.status === 401 || r.status === 403 ? "GitHub refused the key. It needs Contents: Read and write on this repo." : "Saving failed (" + r.status + "). Trying again in 2 minutes.");
          return;
        }
        return r.json().then(function (j) {
          sha.current = j && j.content ? j.content.sha : null;
          last.current = sig;
          try {
            localStorage.setItem(GX_SYNC_AT, body.at);
          } catch (e) {}
          gxSyncNote("On \xB7 saved " + gxWhen(body.at));
        });
      });
    };
    return _put(true).catch(function () {
      return gxSyncNote("Could not reach GitHub. Trying again in 2 minutes.");
    });
  };
  useEffect(function () {
    var busy = false;
    var cycle = function cycle() {
      if (busy) return;
      busy = true;
      pull().then(function (applied) {
        ready.current = true;
        busy = false;
        if (!applied) push();
      });
    };
    cycle();
    var id = setInterval(cycle, 2 * 60 * 1000);
    var vis = function vis() {
      if (document.visibilityState === "visible") cycle();
    };
    document.addEventListener("visibilitychange", vis);
    window.addEventListener("gx-sync-now", cycle);
    return function () {
      clearInterval(id);
      document.removeEventListener("visibilitychange", vis);
      window.removeEventListener("gx-sync-now", cycle);
    };
  }, []);
  var sig = gxSyncSig(gxSyncPick(s));
  useEffect(function () {
    if (!ready.current || !gxSyncKey() || sig === last.current) return;
    clearTimeout(timer.current);
    timer.current = setTimeout(push, 4000);
    return function () {
      return clearTimeout(timer.current);
    };
  }, [sig]);
  return null;
}
function GxSyncRow() {
  var _useState197 = useState(0),
    _useState198 = _slicedToArray(_useState197, 2),
    tick = _useState198[1];
  var _useState199 = useState(""),
    _useState200 = _slicedToArray(_useState199, 2),
    key = _useState200[0],
    setKey = _useState200[1];
  var _useState201 = useState(false),
    _useState202 = _slicedToArray(_useState201, 2),
    edit = _useState202[0],
    setEdit = _useState202[1];
  useEffect(function () {
    var h = function h() {
      return tick(function (x) {
        return x + 1;
      });
    };
    window.addEventListener("gx-sync", h);
    return function () {
      return window.removeEventListener("gx-sync", h);
    };
  }, []);
  var has = !!gxSyncKey(),
    st = window.__SYNC_ST || "";
  var btn = "border border-slate-300 rounded-lg px-3 py-1 text-sm";
  var save = function save() {
    var v = key.trim();
    if (!v) return;
    try {
      localStorage.setItem(GX_SYNC_K, v);
    } catch (e) {}
    setKey("");
    setEdit(false);
    gxSyncNote("Key saved. Syncing...");
    window.dispatchEvent(new Event("gx-sync-now"));
  };
  var off = function off() {
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
    onChange: function onChange(e) {
      return setKey(e.target.value);
    }
  }), /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: btn,
    onClick: save
  }, "Save")) : /*#__PURE__*/React.createElement("span", {
    className: "flex gap-2 items-center"
  }, has ? /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: btn,
    onClick: function onClick() {
      return window.dispatchEvent(new Event("gx-sync-now"));
    }
  }, "Sync now") : null, /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: btn,
    onClick: function onClick() {
      return has ? off() : setEdit(true);
    }
  }, has ? "Turn off" : "Turn on")));
}

// ---------- change 075: hide players from pickup suggestions (install.py) ----------
var __GXH = {
  raw: null,
  set: new Set()
};
var gxHideSet = function gxHideSet() {
  var raw = "[]";
  try {
    raw = localStorage.getItem("gm-hide") || "[]";
  } catch (e) {}
  if (raw !== __GXH.raw) {
    var a = [];
    try {
      a = JSON.parse(raw) || [];
    } catch (e) {}
    __GXH = {
      raw: raw,
      set: new Set(a)
    };
  }
  return __GXH.set;
};
var gxHide = {
  list: function list() {
    return _toConsumableArray(gxHideSet());
  },
  set: function set(l) {
    var raw = JSON.stringify((l || []).slice().sort());
    var old = "[]";
    try {
      old = localStorage.getItem("gm-hide") || "[]";
    } catch (e) {}
    if (raw === old) return;
    try {
      localStorage.setItem("gm-hide", raw);
    } catch (e) {}
    window.dispatchEvent(new Event("gm-hide"));
  },
  toggle: function toggle(id) {
    var l = gxHide.list(),
      i = l.indexOf(id);
    if (i >= 0) l.splice(i, 1);else l.push(id);
    gxHide.set(l);
  }
};
function gxUseHide() {
  var _useState203 = useState(0),
    _useState204 = _slicedToArray(_useState203, 2),
    v = _useState204[0],
    setV = _useState204[1];
  useEffect(function () {
    var h = function h() {
      return setV(function (x) {
        return x + 1;
      });
    };
    window.addEventListener("gm-hide", h);
    return function () {
      return window.removeEventListener("gm-hide", h);
    };
  }, []);
  return v;
}
// skaters who are healthy but not in their team's current lineup (Daily Faceoff), only when the full lineup is known
var gxLK = function gxLK(x) {
  return nrm(x).replace(/[.'\u2019]/g, "").replace(/-/g, " ").replace(/\s+/g, " ").trim();
};
var __GXL = {
  L: null,
  m: null
};
var gxLineupSets = function gxLineupSets() {
  var L = window.LINES_DATA;
  if (!L || !L.teams) return null;
  if (__GXL.L === L && __GXL.m) return __GXL.m;
  var m = {};
  Object.entries(L.teams).forEach(function (_ref203) {
    var _ref204 = _slicedToArray(_ref203, 2),
      t = _ref204[0],
      x = _ref204[1];
    var ln = (x || {}).lines || {},
      names = [];
    ["F1", "F2", "F3", "F4", "D1", "D2", "D3"].forEach(function (sl) {
      return (ln[sl] || []).forEach(function (n) {
        return names.push(gxLK(n));
      });
    });
    if (names.length >= 15) m[t] = new Set(names);
  });
  __GXL = {
    L: L,
    m: m
  };
  return m;
};
var gxScratch = function gxScratch(p) {
  if (!p || p.p === "G" || p.ir) return false;
  var m = gxLineupSets(),
    set = m && m[p.t];
  if (!set) return false;
  if (avail(p, todayISO()) === 0) return false;
  return !set.has(gxLK(p.n));
};
var goalieOut = function goalieOut(p) {
  return gxGoalieOut0(p) || !!p && (gxHideSet().has(p.id) || gxScratch(p));
};
function GxHiddenPanel(_ref205) {
  var s = _ref205.s;
  gxUseHide();
  var _useState205 = useState(false),
    _useState206 = _slicedToArray(_useState205, 2),
    open = _useState206[0],
    setOpen = _useState206[1];
  var K = s.blend;
  var list = gxHide.list().map(function (id) {
    return s.players.find(function (p) {
      return p.id === id;
    });
  }).filter(Boolean);
  if (!list.length) return null;
  return /*#__PURE__*/React.createElement("div", {
    className: "gx-pn"
  }, /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: "text-sm text-slate-500",
    onClick: function onClick() {
      return setOpen(!open);
    }
  }, list.length + " player" + (list.length === 1 ? "" : "s") + " hidden from suggestions \xB7 ", /*#__PURE__*/React.createElement("span", {
    className: "text-blue-600"
  }, open ? "Close" : "Show")), open ? list.map(function (p) {
    return /*#__PURE__*/React.createElement("div", {
      key: p.id,
      className: "gx-row"
    }, /*#__PURE__*/React.createElement(TeamLogo, {
      t: p.t,
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
    }, p.p + (p.ft !== "fa" ? " \xB7 " + teamName(s, p.ft) : ""))), /*#__PURE__*/React.createElement("span", {
      style: {
        fontVariantNumeric: "tabular-nums"
      }
    }, f1(effAvg(p, K))), /*#__PURE__*/React.createElement("button", {
      type: "button",
      className: "text-sm text-blue-600",
      style: {
        marginLeft: 8
      },
      onClick: function onClick() {
        return gxHide.toggle(p.id);
      }
    }, "Show again"));
  }) : null, open ? /*#__PURE__*/React.createElement("div", {
    className: "text-xs text-slate-500",
    style: {
      marginTop: 8
    }
  }, "Hidden players also stay out of the Plan, Advice and trade ideas. Searching a name still finds them.") : null);
}
ReactDOM.createRoot(document.getElementById("root")).render(/*#__PURE__*/React.createElement(App, null));