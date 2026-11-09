/* Fantasy GM: the 3D scoreboard in the Roster box (plain script, needs vendor/gx3d.js first).
   window.gxJumbo.mount(box, { base, onFace(k), onTap(id) }) -> { set(J), turn(k), size(), destroy() }
   J: { nmA, nmB, today, win, games, players } (see the draw functions). The four screens are drawn on canvases. */
(function () {
  "use strict";
  var X = window.GX3D;
  if (!X) return;
  var THREE = X.THREE;
  // screen spot on each side of the model, in the model's own units (measured from jumbo.glb)
  var SX = 0.515, SY0 = -0.505, SY1 = 0.125, SZ = 0.626, CW = 1024, CH = Math.round(1024 * (SY1 - SY0) / (2 * SX));
  var FONT = "-apple-system, 'SF Pro Text', 'Segoe UI', Roboto, Arial, sans-serif";
  var C = { bg: "#06080c", ink: "#f4f5f6", ink2: "#d0d2d6", mute: "#8a8d93", faint: "#4d5157", line: "rgba(255,255,255,.09)", good: "#5fd08a", bad: "#f06a6a" };
  function f1(v) { return v == null || isNaN(v) ? "–" : (Math.round(v * 10) / 10).toFixed(1); }
  function fit(g, s, w) { s = String(s == null ? "" : s); if (g.measureText(s).width <= w) return s; while (s.length > 1 && g.measureText(s + "…").width > w) s = s.slice(0, -1); return s + "…"; }
  function txt(g, s, x, y, o) { o = o || {}; g.font = (o.w || 500) + " " + (o.s || 26) + "px " + FONT; g.fillStyle = o.c || C.ink; g.textAlign = o.a || "left"; g.fillText(o.max ? fit(g, s, o.max) : s, x, y); }
  function frame(g, title, right) {
    g.fillStyle = C.bg; g.fillRect(0, 0, CW, CH);
    var gr = g.createLinearGradient(0, 0, 0, CH); gr.addColorStop(0, "rgba(255,255,255,.05)"); gr.addColorStop(0.4, "rgba(255,255,255,0)"); g.fillStyle = gr; g.fillRect(0, 0, CW, CH);
    txt(g, title.toUpperCase(), 40, 56, { s: 24, w: 600, c: C.mute });
    if (right) txt(g, right, CW - 40, 56, { s: 24, c: C.mute, a: "right" });
  }
  function cells(g, list, y, cols) {
    var w = (CW - 80) / cols;
    g.fillStyle = C.line; g.fillRect(40, y - 34, CW - 80, 2);
    list.forEach(function (c, i) { var x = 40 + (i % cols) * w, yy = y + Math.floor(i / cols) * 74; txt(g, c[0], x, yy, { s: 20, c: C.mute, max: w - 12 }); txt(g, c[1], x, yy + 34, { s: 28, w: 600, max: w - 12 }); });
  }
  // each side: draws itself and returns tap areas [x, y, w, h, id]
  function drawToday(g, J) {
    var T = J.today || {}, hits = [];
    frame(g, "Today", T.right || "");
    if (T.none) { txt(g, T.none, 40, 130, { s: 28, c: C.mute }); return hits; }
    var colW = (CW - 80 - 40) / 2;
    [[T.a || [], J.nmA, T.ta, T.pa, 40, false], [T.b || [], J.nmB, T.tb, T.pb, 40 + colW + 40, true]].forEach(function (q) {
      var x = q[4], rows = q[0];
      txt(g, q[1], x, 104, { s: 26, w: 600, c: q[5] ? C.ink2 : C.ink, max: colW - 190 });
      txt(g, f1(q[2]), x + colW - 92, 104, { s: 30, w: 600, a: "right" }); txt(g, "/ " + f1(q[3]), x + colW, 104, { s: 22, c: C.mute, a: "right" });
      var rh = Math.min(40, (CH - 150) / Math.max(8, Math.min(rows.length, 10)));
      rows.slice(0, 10).forEach(function (r, k) {
        var y = 146 + k * rh;
        g.fillStyle = C.line; g.fillRect(x, y + 12, colW, 1.5);
        txt(g, r.n, x, y, { s: 23, max: colW - 190 });
        txt(g, r.st, x + colW - 92, y, { s: 19, c: r.live ? C.good : C.mute, a: "right" });
        txt(g, f1(r.v), x + colW, y, { s: 24, w: r.real ? 600 : 400, c: r.real ? C.ink : C.faint, a: "right" });
        if (r.id) hits.push([x, y - rh + 12, colW, rh, r.id]);
      });
      if (rows.length > 10) txt(g, "+" + (rows.length - 10) + " more", x, 146 + 10 * rh, { s: 20, c: C.mute });
      if (!rows.length) txt(g, "No games today", x, 150, { s: 22, c: C.mute });
    });
    return hits;
  }
  function drawWin(g, J) {
    var W = J.win || {};
    frame(g, "Win", W.right || "");
    txt(g, W.line || "", 40, 112, { s: 38, w: 600, max: CW - 80 });
    txt(g, W.sub || "", 40, 152, { s: 22, c: C.mute, max: CW - 80 });
    var h = W.hist || [], x0 = 60, x1 = CW - 60, y0 = 190, y1 = 330, py = function (v) { return y1 - v * (y1 - y0); };
    g.setLineDash([6, 8]); g.strokeStyle = "rgba(255,255,255,.18)"; g.lineWidth = 2; g.beginPath(); g.moveTo(40, py(0.5)); g.lineTo(CW - 40, py(0.5)); g.stroke(); g.setLineDash([]);
    if (h.length) {
      var px = function (j) { return h.length > 1 ? x0 + (x1 - x0) * j / (h.length - 1) : (x0 + x1) / 2; };
      g.strokeStyle = C.ink; g.lineWidth = 4; g.lineJoin = "round"; g.beginPath(); h.forEach(function (p, j) { if (j) g.lineTo(px(j), py(p.v)); else g.moveTo(px(j), py(p.v)); }); g.stroke();
      h.forEach(function (p, j) { g.fillStyle = C.ink; g.beginPath(); g.arc(px(j), py(p.v), 7, 0, Math.PI * 2); g.fill(); txt(g, Math.round(p.v * 100), px(j), py(p.v) - 16, { s: 20, c: C.ink2, a: "center" }); txt(g, p.d, px(j), y1 + 34, { s: 18, c: C.mute, a: "center" }); });
    } else txt(g, "Win chance after each day shows once the first day is over.", 40, 260, { s: 22, c: C.mute });
    cells(g, W.cells || [], 420, 3);
    return [];
  }
  function drawGames(g, J) {
    var G = J.games || {}, n = (G.days || []).length || 7;
    frame(g, "Lineup games", G.right || "");
    var lx = 40, lw = 150, rw = 80, cw = (CW - 80 - lw - rw) / n;
    (G.days || []).forEach(function (d, i) { txt(g, d, lx + lw + cw * i + cw / 2, 104, { s: 19, c: G.ti === i ? C.ink : C.mute, w: G.ti === i ? 600 : 400, a: "center" }); });
    txt(g, G.leftLab || "Left", CW - 40, 104, { s: 19, c: C.mute, a: "right" });
    var mx = Math.max.apply(null, [1].concat(G.a || [], G.b || []));
    [[G.a || [], J.nmA, G.la, 0], [G.b || [], J.nmB, G.lb, 1]].forEach(function (q, r) {
      var y = 128 + r * 70;
      txt(g, q[1], lx, y + 38, { s: 22, w: 600, c: r ? C.ink2 : C.ink, max: lw - 12 });
      q[0].forEach(function (v, i) {
        var x = lx + lw + cw * i + 4, fut = (G.fut || [])[i];
        if (fut) { g.strokeStyle = "rgba(255,255,255,.14)"; g.setLineDash([5, 5]); g.lineWidth = 2; g.strokeRect(x, y, cw - 8, 56); g.setLineDash([]); }
        else { g.fillStyle = "rgba(255,255,255," + (0.06 + (r ? 0.14 : 0.24) * v / mx) + ")"; g.fillRect(x, y, cw - 8, 56); }
        txt(g, v, x + (cw - 8) / 2, y + 38, { s: 26, w: 600, c: fut ? C.faint : r ? C.ink2 : C.ink, a: "center" });
      });
      txt(g, q[2], CW - 40, y + 38, { s: 30, w: 600, a: "right", c: r ? C.ink2 : C.ink });
    });
    cells(g, G.cells || [], 330, 3);
    return [];
  }
  function drawPlayers(g, J) {
    var P = J.players || {}, hits = [], colW = (CW - 80 - 40) / 2;
    frame(g, "Players", "Points this week");
    [[P.a || [], P.la || [], J.nmA, 40, false], [P.b || [], P.lb || [], J.nmB, 40 + colW + 40, true]].forEach(function (q) {
      var x = q[3];
      txt(g, q[2], x, 100, { s: 24, w: 600, c: q[4] ? C.ink2 : C.ink, max: colW });
      q[0].slice(0, 5).forEach(function (r, k) {
        var y = 140 + k * 50;
        g.fillStyle = C.line; g.fillRect(x, y + 16, colW, 1.5);
        txt(g, r.n, x, y, { s: 24, w: 600, max: colW - 110 });
        txt(g, r.sub, x + colW - 110, y, { s: 17, c: C.mute, a: "right", max: 130 });
        txt(g, f1(r.v), x + colW, y, { s: 26, w: 600, a: "right", c: q[4] ? C.ink2 : C.ink });
        if (r.id) hits.push([x, y - 34, colW, 50, r.id]);
      });
      txt(g, "MOST LEFT TO GIVE", x, 420, { s: 18, w: 600, c: C.mute });
      q[1].slice(0, 3).forEach(function (r, k) { var y = 456 + k * 40; txt(g, r.n, x, y, { s: 21, max: colW - 100 }); txt(g, r.v, x + colW, y, { s: 22, w: 600, a: "right" }); if (r.id) hits.push([x, y - 28, colW, 40, r.id]); });
      if (!q[1].length) txt(g, "No games left", x, 456, { s: 20, c: C.mute });
    });
    return hits;
  }
  var DRAW = [drawToday, drawWin, drawGames, drawPlayers];
  var cache = {};
  function load(url) { if (!cache[url]) cache[url] = new Promise(function (ok, no) { new X.GLTFLoader().load(url, ok, undefined, no); }); return cache[url]; }
  function ease(t) { return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; }

  function mount(box, opts) {
    var W = box.clientWidth || 340, H = box.clientHeight || 340, alive = true;
    var r = new THREE.WebGLRenderer({ antialias: true, alpha: true, powerPreference: "high-performance" });
    var PR = Math.min(window.devicePixelRatio || 1, 2); r.setPixelRatio(PR); r.setSize(W, H); r.setClearColor(0x000000, 0);
    r.toneMapping = THREE.ACESFilmicToneMapping; r.toneMappingExposure = 0.95; r.outputColorSpace = THREE.SRGBColorSpace;
    r.domElement.style.cssText = "display:block;width:100%;height:100%;touch-action:pan-y;outline:none";
    box.appendChild(r.domElement);
    var sc = new THREE.Scene(), pm = new THREE.PMREMGenerator(r); sc.environment = pm.fromScene(new X.RoomEnvironment(), 0.04).texture; sc.environmentIntensity = 0.22;
    var key = new THREE.DirectionalLight(0xffffff, 1.1); key.position.set(2, 3, 4); sc.add(key, new THREE.HemisphereLight(0xffffff, 0x202226, 0.5));
    var cam = new THREE.PerspectiveCamera(30, W / H, 0.05, 40);
    var rig = new THREE.Group(); sc.add(rig);
    var screens = [], tex = [], hits = [[], [], [], []];
    for (var f = 0; f < 4; f++) {
      var cv = document.createElement("canvas"); cv.width = CW; cv.height = CH;
      var t = new THREE.CanvasTexture(cv); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = r.capabilities.getMaxAnisotropy(); tex.push(t);
      var m = new THREE.Mesh(new THREE.PlaneGeometry(2 * SX, SY1 - SY0), new THREE.MeshBasicMaterial({ map: t, toneMapped: false }));
      var a = f * Math.PI / 2; m.position.set(Math.sin(a) * SZ, (SY0 + SY1) / 2, Math.cos(a) * SZ); m.rotation.y = a; m.userData.f = f; rig.add(m); screens.push(m);
    }
    var model = null;
    load(opts.base + "jumbo.glb").then(function (gl) { if (!alive) return; model = gl.scene; rig.add(model); ask(); if (opts.onReady) opts.onReady(); }).catch(function (e) { if (opts.onError) opts.onError(e); });
    function place() {
      var d = 1.12 / (2 * Math.tan(THREE.MathUtils.degToRad(cam.fov / 2)) * Math.min(1, W / H));
      cam.position.set(0, -0.15, d + 0.62); cam.lookAt(0, -0.2, 0); cam.aspect = W / H; cam.updateProjectionMatrix();
    }
    place();
    var J = null;
    function paint() { if (!J) return; tex.forEach(function (t, f) { var g = t.image.getContext("2d"); g.textBaseline = "alphabetic"; hits[f] = DRAW[f](g, J) || []; t.needsUpdate = true; }); ask(); }
    // turning: drag sideways, or turn(k) from the buttons
    var ang = 0, anim = null, face = 0;
    function setAng(a) { ang = a; rig.rotation.y = -a; ask(); }
    function turn(k, quick) {
      var a0 = ang, t1 = Math.round(a0 / (Math.PI * 2)) * Math.PI * 2 + k * Math.PI / 2;
      while (t1 - a0 > Math.PI) t1 -= Math.PI * 2; while (a0 - t1 > Math.PI) t1 += Math.PI * 2;
      face = ((k % 4) + 4) % 4; if (opts.onFace) opts.onFace(face);
      var t0 = performance.now(), dur = quick ? 1 : 620;
      anim = function (now) { var p = Math.min(1, (now - t0) / dur); setAng(a0 + (t1 - a0) * ease(p)); if (p >= 1) anim = null; };
      ask();
    }
    var drag = null, ray = new THREE.Raycaster();
    var el = r.domElement;
    el.addEventListener("pointerdown", function (e) { drag = { x: e.clientX, y: e.clientY, a: ang, on: false }; anim = null; });
    el.addEventListener("pointermove", function (e) {
      if (!drag) return; var dx = e.clientX - drag.x, dy = e.clientY - drag.y;
      if (!drag.on) { if (Math.abs(dx) > 8 && Math.abs(dx) > Math.abs(dy)) { drag.on = true; try { el.setPointerCapture(e.pointerId); } catch (x) {} } else return; }
      setAng(drag.a - dx * 0.0075);
    });
    function up(e) {
      var d = drag; drag = null; if (!d) return;
      if (d.on) { var moved = ang - d.a, k = Math.round(d.a / (Math.PI / 2)) + (Math.abs(moved) > 0.3 ? Math.sign(moved) : 0); turn(k); return; }
      if (e && e.type === "pointerup") {
        var rc = el.getBoundingClientRect(); ray.setFromCamera(new THREE.Vector2(((e.clientX - rc.left) / rc.width) * 2 - 1, -((e.clientY - rc.top) / rc.height) * 2 + 1), cam);
        var h = ray.intersectObjects(screens, false)[0]; if (!h || !h.uv) return;
        var fx = h.uv.x * CW, fy = (1 - h.uv.y) * CH, f = h.object.userData.f;
        var hit = (hits[f] || []).find(function (q) { return fx >= q[0] && fx <= q[0] + q[2] && fy >= q[1] && fy <= q[1] + q[3]; });
        if (hit && opts.onTap) opts.onTap(hit[4]); else if (f !== face) turn(Math.round(ang / (Math.PI / 2)) + ((f - face + 4) % 4 === 1 ? 1 : -1));
      }
    }
    el.addEventListener("pointerup", up); el.addEventListener("pointercancel", function () { drag = null; });
    var raf = 0, onScreen = true;
    function ask() { if (!raf && alive && onScreen) raf = requestAnimationFrame(frameFn); }
    function frameFn(now) { raf = 0; if (!alive) return; if (anim) anim(now); r.render(sc, cam); if (anim) ask(); }
    var io = window.IntersectionObserver ? new IntersectionObserver(function (es) { onScreen = es[0].isIntersecting; if (onScreen) ask(); }) : null; if (io) io.observe(box);
    function size() { var w = box.clientWidth, h = box.clientHeight; if (!w || !h) return; W = w; H = h; r.setSize(W, H); place(); ask(); }
    var ro = window.ResizeObserver ? new ResizeObserver(size) : null; if (ro) ro.observe(box);
    return {
      set: function (j) { J = j; paint(); }, turn: function (k) { turn(k); }, size: size,
      destroy: function () { alive = false; if (raf) cancelAnimationFrame(raf); if (io) io.disconnect(); if (ro) ro.disconnect(); r.dispose(); pm.dispose(); tex.forEach(function (t) { t.dispose(); }); if (el.parentNode) el.parentNode.removeChild(el); try { r.forceContextLoss(); } catch (x) {} }
    };
  }
  window.gxJumbo = { mount: mount, ok: function () { try { var c = document.createElement("canvas"); return !!(c.getContext("webgl2") || c.getContext("webgl")); } catch (e) { return false; } } };
})();
