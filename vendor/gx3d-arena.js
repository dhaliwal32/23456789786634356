/* Fantasy GM: 3D matchup arena for the Roster page (plain script, needs vendor/gx3d.js first).
   window.gxArena3D.mount(box, opts) -> { set(data), theme(dark), size(), focus(side, id), board(), back(), destroy(), state() }
   data = { A: side, B: side, days: [{ lab, a, b, on, fut }], jumbo: { ... } }
   side = { ab, col, pl: [{ id, last, pos: "F"|"D"|"G", v, txt, body, trim, dim }] }
   Built to stay light on phones: two instanced player meshes, one instanced pillar mesh, one label mesh,
   no mirror, no glow pass, shadows drawn only when the layout changes, frames drawn only while something moves. */
(function () {
  "use strict";
  var X = window.GX3D;
  if (!X) return;
  var THREE = X.THREE;
  var cache = {};
  function load(url) { if (!cache[url]) cache[url] = new Promise(function (ok, no) { new X.GLTFLoader().load(url, ok, undefined, no); }); return cache[url]; }
  function firstGeo(g) { // plain numbers first: squeezed (quantized) files can't hold values above 1
    var geo = null; g.scene.updateMatrixWorld(true);
    g.scene.traverse(function (o) { if (!o.isMesh || geo) return; var src = o.geometry; geo = new THREE.BufferGeometry();
      Object.keys(src.attributes).forEach(function (k) { var a = src.attributes[k], n = a.count, s = a.itemSize, f = new Float32Array(n * s);
        for (var i = 0; i < n; i++) { f[i * s] = a.getX(i); if (s > 1) f[i * s + 1] = a.getY(i); if (s > 2) f[i * s + 2] = a.getZ(i); if (s > 3) f[i * s + 3] = a.getW(i); }
        geo.setAttribute(k, new THREE.BufferAttribute(f, s)); });
      if (src.index) geo.setIndex(new THREE.BufferAttribute(new Uint32Array(src.index.array), 1)); geo.applyMatrix4(o.matrixWorld); });
    return geo; }
  function ease(t) { return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; }
  function reduced() { try { return window.matchMedia("(prefers-reduced-motion: reduce)").matches; } catch (e) { return false; } }
  var COL = function (c) { return new THREE.Color(c || "#888"); };

  // team colours on the shared bodies, per instance
  function playerMat(kind) {
    var m = new THREE.MeshStandardMaterial({ vertexColors: true, roughness: 0.62, metalness: 0 });
    m.onBeforeCompile = function (sh) {
      sh.vertexShader = sh.vertexShader.replace("#include <common>", "#include <common>\nattribute vec3 iBody; attribute vec3 iTrim; attribute float iDim; varying vec3 vB; varying vec3 vT; varying float vD; varying vec3 vP;")
        .replace("#include <begin_vertex>", "#include <begin_vertex>\nvB = iBody; vT = iTrim; vD = iDim; vP = position;");
      sh.fragmentShader = sh.fragmentShader.replace("#include <common>", [
        "#include <common>", "varying vec3 vB; varying vec3 vT; varying float vD; varying vec3 vP;",
        "vec3 gxHsv(vec3 c){ vec4 K = vec4(0., -1./3., 2./3., -1.); vec4 p = mix(vec4(c.bg, K.wz), vec4(c.gb, K.xy), step(c.b, c.g)); vec4 q = mix(vec4(p.xyw, c.r), vec4(c.r, p.yzx), step(p.x, c.r)); float d = q.x - min(q.w, q.y); return vec3(abs(q.z + (q.w - q.y) / (6. * d + 1e-10)), d / (q.x + 1e-10), q.x); }"].join("\n"))
        .replace("#include <color_fragment>", [
          "#include <color_fragment>",
          "{ vec3 lc = diffuseColor.rgb, h = gxHsv(pow(max(lc, vec3(0.)), vec3(1. / 2.2))); float y = vP.y, ax = abs(vP.x);",
          kind === "gk"
            ? "  float wh = step(h.y, 0.22) * step(0.5, h.z); float jer = step(0.66, y) * step(y, 1.24) * (1. - step(0.36, ax) * step(y, 0.98)); float mask = step(1.2, y) * step(ax, 0.17);\n  if (wh * max(jer, mask) > 0.5) diffuseColor.rgb = vB * clamp(h.z / 0.9, 0.3, 1.15);\n  float navy = step(0.55, h.x) * step(h.x, 0.72) * step(0.3, h.y) * step(h.z, 0.45); if (navy > 0.5) diffuseColor.rgb = vT * clamp(h.z / 0.3, 0.4, 1.2);"
            : "  float red = step(0.42, h.y) * (step(h.x, 0.045) + step(0.93, h.x)) * step(0.18, h.z); if (red > 0.5) diffuseColor.rgb = vB * clamp(max(lc.r, max(lc.g, lc.b)) / 0.62, 0.22, 1.35);\n  float sock = step(0.24, y) * step(y, 0.62) * step(h.y, 0.22) * step(0.62, h.z); if (sock > 0.5) diffuseColor.rgb = vT * clamp(h.z / 0.85, 0.5, 1.2);",
          "  diffuseColor.rgb *= vD; }"].join("\n"));
    };
    m.customProgramCacheKey = function () { return "gxar-" + kind; };
    return m;
  }

  // name + value labels: one texture, one draw call, always facing the camera
  function labelMat(tex) {
    return new THREE.ShaderMaterial({
      uniforms: { map: { value: tex }, uOp: { value: 1 } }, transparent: true, depthWrite: false,
      vertexShader: "attribute vec4 iUV; attribute float iA; varying vec2 vU; varying float vA; void main(){ vec4 c = modelViewMatrix * instanceMatrix * vec4(0.,0.,0.,1.); float s = length(instanceMatrix[0].xyz) * clamp(-c.z * 0.042, 0.55, 1.7); c.xy += position.xy * vec2(1.6, 0.5) * s; vU = iUV.xy + uv * iUV.zw; vA = iA; gl_Position = projectionMatrix * c; }",
      fragmentShader: "uniform sampler2D map; uniform float uOp; varying vec2 vU; varying float vA; void main(){ vec4 t = texture2D(map, vU); gl_FragColor = vec4(t.rgb, t.a * uOp * vA);\n#include <colorspace_fragment>\n}"
    });
  }

  function iceTex(dark, A, B) {
    var W = 1024, H = 2048, c = document.createElement("canvas"); c.width = W; c.height = H; var g = c.getContext("2d");
    var px = W / 15; // 15 m by 30 m
    var a = COL(A.col).getStyle(), b = COL(B.col).getStyle();
    g.fillStyle = dark ? "#0b0f16" : "#f3f6fa"; g.fillRect(0, 0, W, H);
    var ga = g.createLinearGradient(0, H, 0, H / 2); ga.addColorStop(0, hexA(A.col, dark ? 0.32 : 0.16)); ga.addColorStop(1, hexA(A.col, dark ? 0.06 : 0.03)); g.fillStyle = ga; g.fillRect(0, H / 2, W, H / 2);
    var gb = g.createLinearGradient(0, 0, 0, H / 2); gb.addColorStop(0, hexA(B.col, dark ? 0.32 : 0.16)); gb.addColorStop(1, hexA(B.col, dark ? 0.06 : 0.03)); g.fillStyle = gb; g.fillRect(0, 0, W, H / 2);
    for (var i = 0; i < 5000; i++) { g.fillStyle = dark ? "rgba(255,255,255," + Math.random() * 0.05 + ")" : "rgba(140,160,190," + Math.random() * 0.07 + ")"; g.fillRect(Math.random() * W, Math.random() * H, 3 + Math.random() * 40, 1.2); }
    g.fillStyle = dark ? "rgba(225,45,55,.9)" : "rgba(205,30,40,.85)"; g.fillRect(0, H / 2 - 0.15 * px, W, 0.3 * px);
    g.fillStyle = dark ? "rgba(45,95,235,.9)" : "rgba(30,70,200,.8)"; g.fillRect(0, H / 2 - 7.6 * px, W, 0.3 * px); g.fillRect(0, H / 2 + 7.3 * px, W, 0.3 * px);
    g.strokeStyle = dark ? "rgba(45,95,235,.9)" : "rgba(30,70,200,.8)"; g.lineWidth = 0.08 * px; g.beginPath(); g.arc(W / 2, H / 2, 2.6 * px, 0, Math.PI * 2); g.stroke();
    g.textAlign = "center"; g.font = "900 " + 2.4 * px + "px 'Arial Black', Arial, sans-serif";
    g.save(); g.translate(W / 2, H * 0.78); g.fillStyle = hexA(A.col, dark ? 0.35 : 0.25); g.fillText(A.ab || "", 0, 0); g.restore();
    g.save(); g.translate(W / 2, H * 0.22); g.rotate(Math.PI); g.fillStyle = hexA(B.col, dark ? 0.35 : 0.25); g.fillText(B.ab || "", 0, 0); g.restore();
    var t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 4; return t;
  }
  function hexA(c, a) { var k = COL(c); k.convertLinearToSRGB(); return "rgba(" + Math.round(k.r * 255) + "," + Math.round(k.g * 255) + "," + Math.round(k.b * 255) + "," + a + ")"; }

  function mount(box, opts) {
    var dark = opts.dark !== false, base = opts.base || "", RM = reduced(), card = !!opts.card;
    var W = box.clientWidth || 360, H = box.clientHeight || 300;
    var r = new THREE.WebGLRenderer({ antialias: true, powerPreference: "high-performance" });
    var PR = Math.min(window.devicePixelRatio || 1, opts.maxPR || 1.5); r.setPixelRatio(PR); r.setSize(W, H);
    r.toneMapping = THREE.ACESFilmicToneMapping; r.outputColorSpace = THREE.SRGBColorSpace;
    r.shadowMap.enabled = true; r.shadowMap.type = THREE.PCFSoftShadowMap; r.shadowMap.autoUpdate = false;
    r.domElement.style.cssText = "display:block;width:100%;height:100%;touch-action:none;outline:none";
    box.appendChild(r.domElement);
    var sc = new THREE.Scene(), pm = new THREE.PMREMGenerator(r); sc.environment = pm.fromScene(new X.RoomEnvironment(), 0.04).texture;
    var cam = new THREE.PerspectiveCamera(40, W / H, 0.1, 160);

    // rink, boards, crowd
    var iceM = new THREE.MeshStandardMaterial({ roughness: 0.32, metalness: 0, envMapIntensity: 0.25 });
    var ice = new THREE.Mesh(new THREE.PlaneGeometry(15, 30), iceM); ice.rotation.x = -Math.PI / 2; ice.receiveShadow = true; sc.add(ice);
    var boardM = new THREE.MeshStandardMaterial({ color: 0xe8edf3, roughness: 0.5 }), capM = new THREE.MeshBasicMaterial({ color: 0xffffff });
    var stripA = new THREE.MeshBasicMaterial({ color: 0x2f7bff }), stripB = new THREE.MeshBasicMaterial({ color: 0xff7a1a });
    [[0, -15, 0, 15, stripA], [0, 15, Math.PI, 15, stripB], [-7.5, -7.5, Math.PI / 2, 15, stripA], [-7.5, 7.5, Math.PI / 2, 15, stripB], [7.5, -7.5, -Math.PI / 2, 15, stripA], [7.5, 7.5, -Math.PI / 2, 15, stripB]].forEach(function (w) {
      var m = new THREE.Mesh(new THREE.PlaneGeometry(w[3], 1.1), boardM); m.position.set(w[0], 0.55, w[1]); m.rotation.y = w[2]; sc.add(m);
      var s = new THREE.Mesh(new THREE.PlaneGeometry(w[3], 0.16), w[4]); s.position.set(w[0], 0.95, w[1]); s.rotation.y = w[2]; s.translateZ(0.01); sc.add(s);
    });
    var bok = document.createElement("canvas"); bok.width = bok.height = 32; (function () { var c = bok.getContext("2d"), gr = c.createRadialGradient(16, 16, 0, 16, 16, 16); gr.addColorStop(0, "rgba(255,255,255,1)"); gr.addColorStop(0.45, "rgba(255,255,255,.3)"); gr.addColorStop(1, "rgba(255,255,255,0)"); c.fillStyle = gr; c.fillRect(0, 0, 32, 32); })();
    var NB = 700, bp = new Float32Array(NB * 3), bc = new Float32Array(NB * 3);
    for (var i = 0; i < NB; i++) { var a = Math.random() * Math.PI * 2, rx = 12 + Math.random() * 7, rz = 20 + Math.random() * 7; bp.set([Math.cos(a) * rx, 2 + Math.random() * 10, Math.sin(a) * rz], i * 3); var w = Math.random(), cc = w < 0.15 ? [0.3, 0.55, 1] : w < 0.3 ? [1, 0.55, 0.2] : [1, 0.92, 0.8], k = 0.25 + Math.random() * 0.75; bc.set([cc[0] * k, cc[1] * k, cc[2] * k], i * 3); }
    var bg = new THREE.BufferGeometry(); bg.setAttribute("position", new THREE.BufferAttribute(bp, 3)); bg.setAttribute("color", new THREE.BufferAttribute(bc, 3));
    var crowd = new THREE.Points(bg, new THREE.PointsMaterial({ map: new THREE.CanvasTexture(bok), size: 0.8, vertexColors: true, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, fog: false })); sc.add(crowd);

    // lights: shadows drawn once per layout change
    var hemi = new THREE.HemisphereLight(0xdfe8ff, 0x1a1d24, 0.6); sc.add(hemi);
    var sun = new THREE.DirectionalLight(0xffffff, 1.6); sun.position.set(4, 16, -6); sun.castShadow = true; sun.shadow.mapSize.set(1024, 2048);
    Object.assign(sun.shadow.camera, { left: -9, right: 9, top: 17, bottom: -17, near: 2, far: 40 }); sun.shadow.bias = -0.0006; sun.shadow.radius = 3; sc.add(sun);
    var lA = new THREE.PointLight(0x2f7bff, 30, 18, 1.6), lB = new THREE.PointLight(0xff7a1a, 30, 18, 1.6); lA.position.set(0, 5, -9); lB.position.set(0, 5, 9); sc.add(lA, lB);

    // jumbotron: four screens and a ring of day boards under it
    var JY = 12.5, JW = 4.2, JH = 2.4, faces = [], fTex = [];
    var jumbo = new THREE.Group(); jumbo.position.y = JY; sc.add(jumbo);
    var frameM = new THREE.MeshStandardMaterial({ color: 0x14171d, roughness: 0.6, metalness: 0.2 });
    jumbo.add(new THREE.Mesh(new THREE.BoxGeometry(JW + 0.25, JH + 1.5, JW + 0.25), frameM));
    var dayTex = [];
    for (var f = 0; f < 4; f++) {
      var cv = document.createElement("canvas"); cv.width = 1024; cv.height = 576; var t = new THREE.CanvasTexture(cv); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 4; fTex.push(t);
      var sm = new THREE.Mesh(new THREE.PlaneGeometry(JW, JH), new THREE.MeshBasicMaterial({ map: t, toneMapped: false }));
      var ang = f * Math.PI / 2 + Math.PI; sm.position.set(Math.sin(ang) * (JW / 2 + 0.14), 0.4, Math.cos(ang) * (JW / 2 + 0.14)); sm.rotation.y = ang; sm.userData.face = f; jumbo.add(sm); faces.push(sm);
      var dc = document.createElement("canvas"); dc.width = 1024; dc.height = 160; var dt = new THREE.CanvasTexture(dc); dt.colorSpace = THREE.SRGBColorSpace; dayTex.push(dt);
      var dm = new THREE.Mesh(new THREE.PlaneGeometry(JW, JW * 160 / 1024), new THREE.MeshBasicMaterial({ map: dt, toneMapped: false }));
      dm.position.set(Math.sin(ang) * (JW / 2 + 0.14), -JH / 2 - 0.32, Math.cos(ang) * (JW / 2 + 0.14)); dm.rotation.y = ang; dm.userData.days = f; jumbo.add(dm); faces.push(dm);
    }
    var cable = new THREE.Mesh(new THREE.CylinderGeometry(0.04, 0.04, 20, 6), frameM); cable.position.y = JY + 11.5; sc.add(cable);

    // players, pillars, labels
    var geoSk = null, geoGk = null, matSk = playerMat("sk"), matGk = playerMat("gk");
    var MAXN = 40, pillarGeo = new THREE.CylinderGeometry(0.44, 0.5, 1, 28, 1); pillarGeo.translate(0, 0.5, 0);
    var pillarM = new THREE.MeshStandardMaterial({ roughness: 0.35, metalness: 0.15 });
    var pillars = new THREE.InstancedMesh(pillarGeo, pillarM, MAXN * 2); pillars.castShadow = true; pillars.receiveShadow = true; pillars.count = 0; sc.add(pillars);
    var capGeo = new THREE.TorusGeometry(0.47, 0.035, 8, 40); capGeo.rotateX(Math.PI / 2);
    var caps = new THREE.InstancedMesh(capGeo, new THREE.MeshBasicMaterial({ toneMapped: false }), MAXN * 2); caps.count = 0; sc.add(caps);
    var sk = null, gk = null;
    var LCV = document.createElement("canvas"); LCV.width = 1024; LCV.height = 2048; var LT = new THREE.CanvasTexture(LCV); LT.colorSpace = THREE.SRGBColorSpace; LT.anisotropy = 4;
    var labels = new THREE.InstancedMesh(new THREE.PlaneGeometry(1, 1), labelMat(LT), MAXN * 2); labels.count = 0; labels.renderOrder = 5; labels.frustumCulled = false;
    labels.geometry.setAttribute("iUV", new THREE.InstancedBufferAttribute(new Float32Array(MAXN * 2 * 4), 4)); labels.geometry.setAttribute("iA", new THREE.InstancedBufferAttribute(new Float32Array(MAXN * 2).fill(1), 1)); sc.add(labels);
    var items = [], data = null, anims = [];

    function instAttrs(mesh, n) { var g = mesh.geometry; g.setAttribute("iBody", new THREE.InstancedBufferAttribute(new Float32Array(n * 3), 3)); g.setAttribute("iTrim", new THREE.InstancedBufferAttribute(new Float32Array(n * 3), 3)); g.setAttribute("iDim", new THREE.InstancedBufferAttribute(new Float32Array(n).fill(1), 1)); }
    function ready() { return geoSk && geoGk; }
    Promise.all([load(base + "sk_xs.glb"), load(base + "gk_xs.glb")]).then(function (L) {
      geoSk = firstGeo(L[0]); geoGk = firstGeo(L[1]);
      sk = new THREE.InstancedMesh(geoSk.clone(), matSk, MAXN * 2); gk = new THREE.InstancedMesh(geoGk.clone(), matGk, 12);
      [sk, gk].forEach(function (m) { instAttrs(m, m.instanceMatrix.count); m.castShadow = true; m.count = 0; m.frustumCulled = false; sc.add(m); });
      if (data) layout(true); if (opts.onReady) opts.onReady();
    }).catch(function (e) { if (opts.onError) opts.onError(e); });

    // where each player stands: rows by position on each half, best in the middle
    function spots(pl, side) {
      var rows = { F: [], D: [], G: [] }; pl.forEach(function (p) { (rows[p.pos] || rows.F).push(p); });
      var out = [], sgn = side === "A" ? -1 : 1;
      var put = function (list, z0, per, gap) {
        var srt = list.slice().sort(function (a, b) { return b.v - a.v; }), lines = [];
        for (var i = 0; i < srt.length; i += per) lines.push(srt.slice(i, i + per));
        lines.forEach(function (ln, li) {
          var ord = []; ln.forEach(function (p, k) { if (k % 2 === 0) ord.push(p); else ord.unshift(p); });
          ord.forEach(function (p, k) { out.push({ p: p, x: (k - (ord.length - 1) / 2) * gap * (side === "A" ? 1 : -1), z: sgn * (z0 + li * 2.0) }); });
        });
        return z0 + lines.length * 2.0;
      };
      var z = put(rows.F, 2.6, 6, 1.85); z = put(rows.D, z + 0.4, 5, 1.95); put(rows.G, z + 0.6, 3, 2.3);
      return out;
    }
    var maxV = 1;
    function hOf(v) { return 0.12 + 2.6 * Math.max(0, v) / maxV; }
    function tH(s) { return C.sel && C.sel !== s && !(C.sel.side === s.side && C.sel.p.id === s.p.id) ? 0.03 : hOf(s.p.v); }
    function tS(s) { var me = C.sel && C.sel.side === s.side && C.sel.p.id === s.p.id; return C.sel && (!me || hero.on) ? 0.001 : 1; }
    // a sharper copy of the picked player, in his colours
    var hero = { mesh: null, on: false };
    function heroFor(it) {
      var kind = it.p.pos === "G" ? "gk" : "sk";
      return load(base + kind + "_md.glb").then(function (gl) {
        if (C.sel !== it) return;
        var g = firstGeo(gl), n = g.attributes.position.count, bo = COL(it.p.body), tr = COL(it.p.trim);
        var fill = function (c) { var a = new Float32Array(n * 3); for (var i = 0; i < n; i++) { a[i * 3] = c.r; a[i * 3 + 1] = c.g; a[i * 3 + 2] = c.b; } return new THREE.BufferAttribute(a, 3); };
        g.setAttribute("iBody", fill(bo)); g.setAttribute("iTrim", fill(tr)); g.setAttribute("iDim", new THREE.BufferAttribute(new Float32Array(n).fill(1), 1));
        if (hero.mesh) { sc.remove(hero.mesh); hero.mesh.geometry.dispose(); }
        var m = new THREE.Mesh(g, kind === "gk" ? matGk : matSk); m.castShadow = true; m.position.set(it.x, it.h1, it.z); m.rotation.y = it.side === "A" ? 0 : Math.PI;
        sc.add(m); hero.mesh = m; hero.on = true; it.sc = 0.001; place(); r.shadowMap.needsUpdate = true; ask();
      });
    }
    function heroOff() { if (hero.mesh) { sc.remove(hero.mesh); hero.mesh.geometry.dispose(); hero.mesh = null; } hero.on = false; }
    function rankLabels() { ["A", "B"].forEach(function (sd) { items.filter(function (i) { return i.side === sd; }).sort(function (a, b) { return b.p.v - a.p.v; }).forEach(function (it, k) { it.top = k < 6; }); }); }
    var lblNear = null;
    function labelVis() { var near = C.dist < 20 || C.mode !== "arena"; if (near === lblNear && !C.sel) return; lblNear = near; if (!items.length) return; var a = labels.geometry.attributes.iA; items.forEach(function (it, i) { var v = C.sel ? 0 : (near || it.top ? (it.p.dim ? 0.35 : 1) : 0); a.setX(i, v); }); a.needsUpdate = true; }
    function reshape(dur) { items.forEach(function (it) { it.h0 = it.h; it.h1 = tH(it); it.s0 = it.sc; it.s1 = tS(it); }); var t0 = performance.now(); anims.push(function (now) { var t = Math.min(1, (now - t0) / (RM ? 1 : dur)), e = ease(t); items.forEach(function (it) { it.h = it.h0 + (it.h1 - it.h0) * e; it.sc = it.s0 + (it.s1 - it.s0) * e; }); place(); if (t >= 1) { r.shadowMap.needsUpdate = true; return false; } return true; }); lblNear = null; labelVis(); ask(); }
    var M4 = new THREE.Matrix4(), Q4 = new THREE.Quaternion(), S3 = new THREE.Vector3(1, 1, 1), P3 = new THREE.Vector3(), UP = new THREE.Vector3(0, 1, 0);
    function layout(first) {
      if (!data) return;
      var A = data.A, B = data.B, all = [];
      maxV = 1; [A, B].forEach(function (s) { s.pl.forEach(function (p) { if (p.v > maxV) maxV = p.v; }); });
      spots(A.pl, "A").forEach(function (s) { all.push(Object.assign(s, { side: "A" })); });
      spots(B.pl, "B").forEach(function (s) { all.push(Object.assign(s, { side: "B" })); });
      var old = {}; items.forEach(function (it) { old[it.side + it.p.id] = it; });
      items = all.map(function (s) { var o = old[s.side + s.p.id]; s.h0 = o ? o.h : 0.05; s.x0 = o ? o.x : s.x; s.z0 = o ? o.z : s.z; s.h1 = tH(s); s.h = s.h0; s.s0 = o ? o.sc : 1; s.sc = s.s0; s.s1 = tS(s); return s; });
      rankLabels();
      drawLabels(); paintIce(); paintJumbo(); lblNear = null; labelVis();
      var t0 = performance.now(), dur = first || RM ? 1 : 650;
      anims.push(function (now) { var t = Math.min(1, (now - t0) / dur), e = ease(t); items.forEach(function (it) { it.h = it.h0 + (it.h1 - it.h0) * e; it.sc = it.s0 + (it.s1 - it.s0) * e; it.cx = it.x0 + (it.x - it.x0) * e; it.cz = it.z0 + (it.z - it.z0) * e; }); place(); if (t >= 1) { r.shadowMap.needsUpdate = true; return false; } return true; });
      ask();
    }
    function place() {
      if (!ready()) return;
      var ni = 0, ns = 0, ng = 0;
      items.forEach(function (it, i) {
        var x = it.cx == null ? it.x : it.cx, z = it.cz == null ? it.z : it.cz, side = data[it.side], dim = it.p.dim ? 0.32 : 1;
        M4.compose(P3.set(x, 0, z), Q4.identity(), S3.set(1, it.h, 1)); pillars.setMatrixAt(ni, M4);
        var pc = COL(side.col); pc.multiplyScalar(it.p.dim ? 0.18 : 0.42); pillars.setColorAt(ni, pc);
        M4.compose(P3.set(x, it.h + 0.01, z), Q4.identity(), S3.set(1, 1, 1)); caps.setMatrixAt(ni, M4); var cc = COL(side.col); if (it.p.dim) cc.multiplyScalar(0.25); caps.setColorAt(ni, cc);
        var face = it.side === "A" ? 0 : Math.PI, mesh = it.p.pos === "G" ? gk : sk, k = it.p.pos === "G" ? ng++ : ns++;
        var ss = it.sc == null ? 1 : it.sc; M4.compose(P3.set(x, it.h, z), Q4.setFromAxisAngle(UP, face), S3.set(ss, ss, ss)); mesh.setMatrixAt(k, M4);
        var bo = COL(it.p.body), tr = COL(it.p.trim);
        mesh.geometry.attributes.iBody.setXYZ(k, bo.r, bo.g, bo.b); mesh.geometry.attributes.iTrim.setXYZ(k, tr.r, tr.g, tr.b); mesh.geometry.attributes.iDim.setX(k, dim);
        it.k = k; it.mesh = mesh; it.wy = it.h + (it.p.pos === "G" ? 1.45 : 1.87);
        M4.compose(P3.set(x, it.wy + 0.42, z), Q4.identity(), S3.set(1, 1, 1)); labels.setMatrixAt(ni, M4); 
        ni++;
      });
      pillars.count = caps.count = labels.count = ni; sk.count = ns; gk.count = ng;
      [pillars, caps, labels, sk, gk].forEach(function (m) { m.instanceMatrix.needsUpdate = true; if (m.instanceColor) m.instanceColor.needsUpdate = true; });
      [sk, gk].forEach(function (m) { ["iBody", "iTrim", "iDim"].forEach(function (a) { m.geometry.attributes[a].needsUpdate = true; }); });
      labels.geometry.attributes.iA.needsUpdate = true; pillars.computeBoundingSphere(); sk.computeBoundingSphere(); gk.computeBoundingSphere();
    }
    function drawLabels() {
      var g = LCV.getContext("2d"), cw = 256, ch = 80, cols = 4; g.clearRect(0, 0, LCV.width, LCV.height);
      var uv = labels.geometry.attributes.iUV;
      items.forEach(function (it, i) {
        var cx = (i % cols) * cw, cy = Math.floor(i / cols) * ch, side = data[it.side];
        g.fillStyle = dark ? "rgba(8,11,18,.86)" : "rgba(255,255,255,.92)"; rr(g, cx + 6, cy + 6, cw - 12, ch - 12, 16); g.fill();
        g.fillStyle = hexA(side.col, 1); rr(g, cx + 6, cy + 6, 8, ch - 12, 4); g.fill();
        g.textAlign = "left"; g.fillStyle = dark ? "#f3f5f8" : "#0b1220"; g.font = "800 27px -apple-system, 'Segoe UI', Roboto, Arial, sans-serif";
        g.fillText(fit(g, String(it.p.last || "").toUpperCase(), 150), cx + 24, cy + 51);
        g.textAlign = "right"; g.font = "900 30px -apple-system, 'Segoe UI', Roboto, Arial, sans-serif"; g.fillStyle = hexA(side.col, 1); if (!dark) g.fillStyle = hexA(side.col, 1);
        g.fillText(it.p.txt == null ? "" : String(it.p.txt), cx + cw - 20, cy + 52);
        uv.setXYZW(i, cx / LCV.width, 1 - (cy + ch) / LCV.height, cw / LCV.width, ch / LCV.height);
      });
      uv.needsUpdate = true; LT.needsUpdate = true;
    }
    function rr(g, x, y, w, h, q) { g.beginPath(); g.moveTo(x + q, y); g.arcTo(x + w, y, x + w, y + h, q); g.arcTo(x + w, y + h, x, y + h, q); g.arcTo(x, y + h, x, y, q); g.arcTo(x, y, x + w, y, q); g.closePath(); }
    function fit(g, s, w) { if (g.measureText(s).width <= w) return s; while (s.length > 2 && g.measureText(s + ".").width > w) s = s.slice(0, -1); return s + "."; }
    function paintIce() { if (iceM.map) iceM.map.dispose(); iceM.map = iceTex(dark, data.A, data.B); iceM.needsUpdate = true; stripA.color.copy(COL(data.A.col)); stripB.color.copy(COL(data.B.col)); lA.color.copy(COL(data.A.col)); lB.color.copy(COL(data.B.col)); }
    // the four screens: each one shows a different view of the matchup
    function paintJumbo() {
      var J = data.jumbo || {}, A = data.A, B = data.B;
      fTex.forEach(function (t, f) {
        var cv = t.image, g = cv.getContext("2d"), w = cv.width, h = cv.height;
        var bgd = g.createLinearGradient(0, 0, 0, h); bgd.addColorStop(0, "#0a0d14"); bgd.addColorStop(1, "#05070b"); g.fillStyle = bgd; g.fillRect(0, 0, w, h);
        g.fillStyle = hexA(A.col, 0.9); g.fillRect(0, 0, w / 2, 10); g.fillStyle = hexA(B.col, 0.9); g.fillRect(w / 2, 0, w / 2, 10);
        var title = (J.titles || ["SCORE", "WIN CHANCE", "GAMES", "TOP PLAYERS"])[f];
        g.fillStyle = "#8f9bb0"; g.font = "800 30px -apple-system, 'Segoe UI', Roboto, Arial, sans-serif"; g.textAlign = "center"; g.fillText(title, w / 2, 58);
        g.fillStyle = "#fff";
        if (f === 0) {
          g.font = "900 54px -apple-system, Arial, sans-serif"; g.fillStyle = hexA(A.col, 1); g.fillText(A.ab, w * 0.25, 150); g.fillStyle = hexA(B.col, 1); g.fillText(B.ab, w * 0.75, 150);
          g.fillStyle = "#fff"; g.font = "900 140px -apple-system, Arial, sans-serif"; g.fillText(J.a || "0", w * 0.25, 300); g.fillText(J.b || "0", w * 0.75, 300);
          g.font = "700 34px -apple-system, Arial, sans-serif"; g.fillStyle = "#8f9bb0"; g.fillText("PROJ " + (J.pa || "-"), w * 0.25, 360); g.fillText("PROJ " + (J.pb || "-"), w * 0.75, 360);
          g.fillStyle = "#cfd6e2"; g.font = "800 40px -apple-system, Arial, sans-serif"; g.fillText(J.line || "", w / 2, 470);
        } else if (f === 1) {
          var p = Math.max(0, Math.min(1, J.win == null ? 0.5 : J.win));
          g.font = "900 170px -apple-system, Arial, sans-serif"; g.fillStyle = hexA(p >= 0.5 ? A.col : B.col, 1); g.fillText(Math.round((p >= 0.5 ? p : 1 - p) * 100) + "%", w / 2, 270);
          g.font = "800 38px -apple-system, Arial, sans-serif"; g.fillStyle = "#cfd6e2"; g.fillText((p >= 0.5 ? A.ab : B.ab) + " TO WIN", w / 2, 330);
          g.fillStyle = "#1c2230"; rr(g, 90, 390, w - 180, 34, 17); g.fill(); g.fillStyle = hexA(A.col, 1); rr(g, 90, 390, (w - 180) * p, 34, 17); g.fill(); g.fillStyle = hexA(B.col, 1); rr(g, 90 + (w - 180) * p, 390, (w - 180) * (1 - p), 34, 17); g.fill();
          g.font = "700 30px -apple-system, Arial, sans-serif"; g.fillStyle = "#8f9bb0"; g.textAlign = "left"; g.fillText(A.ab, 90, 470); g.textAlign = "right"; g.fillText(B.ab, w - 90, 470);
        } else if (f === 2) {
          var rowG = function (y, lab, a, b) { g.textAlign = "left"; g.fillStyle = "#8f9bb0"; g.font = "800 32px -apple-system, Arial, sans-serif"; g.fillText(lab, 80, y); g.textAlign = "center"; g.font = "900 64px -apple-system, Arial, sans-serif"; g.fillStyle = hexA(A.col, 1); g.fillText(a, w * 0.6, y + 8); g.fillStyle = hexA(B.col, 1); g.fillText(b, w * 0.84, y + 8); };
          g.font = "800 34px -apple-system, Arial, sans-serif"; g.fillStyle = hexA(A.col, 1); g.fillText(A.ab, w * 0.6, 120); g.fillStyle = hexA(B.col, 1); g.fillText(B.ab, w * 0.84, 120);
          rowG(220, "GAMES PLAYED", String(J.ua == null ? "-" : J.ua), String(J.ub == null ? "-" : J.ub)); rowG(330, "GAMES LEFT", String(J.la == null ? "-" : J.la), String(J.lb == null ? "-" : J.lb)); rowG(440, "TODAY", String(J.ta == null ? "-" : J.ta), String(J.tb == null ? "-" : J.tb));
        } else {
          var ka = J.ka || [], kb = J.kb || [];
          g.font = "800 34px -apple-system, Arial, sans-serif"; g.fillStyle = hexA(A.col, 1); g.fillText(A.ab, w * 0.25, 120); g.fillStyle = hexA(B.col, 1); g.fillText(B.ab, w * 0.75, 120);
          for (var i = 0; i < 3; i++) {
            [[ka[i], 0.25, A], [kb[i], 0.75, B]].forEach(function (q) { if (!q[0]) return; g.textAlign = "center"; g.fillStyle = "#fff"; g.font = "800 36px -apple-system, Arial, sans-serif"; g.fillText(fit(g, q[0][0].toUpperCase(), w * 0.42), w * q[1], 200 + i * 110); g.fillStyle = hexA(q[2].col, 1); g.font = "900 40px -apple-system, Arial, sans-serif"; g.fillText(q[0][1], w * q[1], 245 + i * 110); });
          }
        }
        t.needsUpdate = true;
      });
      var D = data.days || [];
      dayTex.forEach(function (t) {
        var cv = t.image, g = cv.getContext("2d"), w = cv.width, h = cv.height, n = Math.max(1, D.length), bw = w / n; g.fillStyle = "#05070b"; g.fillRect(0, 0, w, h);
        D.forEach(function (d, i) {
          var x = i * bw; g.fillStyle = d.on ? "rgba(255,255,255,.14)" : (i % 2 ? "rgba(255,255,255,.03)" : "rgba(255,255,255,0)"); g.fillRect(x + 2, 2, bw - 4, h - 4);
          if (d.on) { g.strokeStyle = "#ffffff"; g.lineWidth = 4; g.strokeRect(x + 4, 4, bw - 8, h - 8); }
          g.textAlign = "center"; g.fillStyle = d.today ? "#ffd166" : "#8f9bb0"; g.font = "800 26px -apple-system, Arial, sans-serif"; g.fillText(d.lab, x + bw / 2, 38);
          var aw = d.a != null && d.b != null && d.a !== d.b ? (d.a > d.b ? "a" : "b") : "";
          g.font = "900 40px -apple-system, Arial, sans-serif"; g.fillStyle = aw === "a" ? hexA(A.col, 1) : d.fut ? "#5d6779" : "#e6ebf2"; g.fillText(d.a == null ? "-" : d.a, x + bw / 2, 88);
          g.fillStyle = aw === "b" ? hexA(B.col, 1) : d.fut ? "#5d6779" : "#e6ebf2"; g.fillText(d.b == null ? "-" : d.b, x + bw / 2, 138);
        });
        t.needsUpdate = true;
      });
    }

    function setTheme(d) {
      dark = d;
      sc.background = new THREE.Color(d ? 0x04060b : 0xdde4ec); sc.fog = new THREE.Fog(d ? 0x04060b : 0xdde4ec, 30, 70);
      r.toneMappingExposure = d ? 1.0 : 1.05; sc.environmentIntensity = d ? 0.35 : 0.8;
      boardM.color.set(d ? 0x2c323c : 0xf6f8fb); hemi.intensity = d ? 0.6 : 1.35; hemi.groundColor.set(d ? 0x1a1d24 : 0xbcc6d2); sun.intensity = d ? 1.6 : 2.1;
      lA.intensity = lB.intensity = d ? 30 : 8; crowd.material.opacity = d ? 1 : 0.3;
      if (data) { paintIce(); drawLabels(); } r.shadowMap.needsUpdate = true; ask();
    }

    // camera: circle the arena by dragging, pinch to zoom, fly to a player or the big screen
    var C = { yaw: 0, pitch: card ? 0.78 : 0.92, dist: 0, tgt: new THREE.Vector3(0, 1.4, 0.6), vy: 0, vp: 0, mode: "arena", sel: null };
    function homeDist() { var a = W / H; return card ? (a < 1.2 ? 26 : 22) : a < 0.75 ? 31 : a < 1.2 ? 26 : 22; }
    C.dist = homeDist();
    function camPlace() { labelVis(); var cp = Math.cos(C.pitch); cam.position.set(C.tgt.x + Math.sin(C.yaw) * cp * C.dist, C.tgt.y + Math.sin(C.pitch) * C.dist, C.tgt.z - Math.cos(C.yaw) * cp * C.dist); cam.lookAt(C.tgt); }
    function flyTo(to, dur, done) {
      var f = { yaw: C.yaw, pitch: C.pitch, dist: C.dist, tgt: C.tgt.clone() }, t0 = performance.now();
      while (to.yaw - f.yaw > Math.PI) to.yaw -= Math.PI * 2; while (f.yaw - to.yaw > Math.PI) to.yaw += Math.PI * 2;
      anims.push(function (now) { var t = Math.min(1, (now - t0) / (RM ? 1 : dur)), e = ease(t); C.yaw = f.yaw + (to.yaw - f.yaw) * e; C.pitch = f.pitch + (to.pitch - f.pitch) * e; C.dist = f.dist + (to.dist - f.dist) * e; C.tgt.lerpVectors(f.tgt, to.tgt, e); camPlace(); if (t >= 1) { if (done) done(); return false; } return true; });
      ask();
    }
    function focus(side, id) {
      var it = items.find(function (x) { return x.side === side && x.p.id === id; }); if (!it) return;
      heroOff(); C.mode = "player"; C.sel = it; reshape(700); heroFor(it);
      var yaw = side === "A" ? Math.PI + 0.3 : 0.3, hh = hOf(it.p.v); // the others sink into the ice; look at his front
      shift(true); flyTo({ yaw: yaw, pitch: 0.12, dist: W / H < 0.75 ? 6.2 : 5, tgt: new THREE.Vector3(it.x, hh + (it.p.pos === "G" ? 0.6 : 0.85), it.z) }, 1000);
      if (opts.onPick) opts.onPick(side, id);
    }
    function board(face) {
      if (C.sel) { C.sel = null; heroOff(); reshape(500); } shift(true); C.mode = "board"; var f = face == null ? Math.round(((C.yaw % (Math.PI * 2)) + Math.PI * 2) % (Math.PI * 2) / (Math.PI / 2)) % 4 : face;
      flyTo({ yaw: f * Math.PI / 2, pitch: -0.02, dist: W / H < 0.75 ? 12.5 : 9, tgt: new THREE.Vector3(0, JY + 0.1, 0) }, 1000);
      if (opts.onBoard) opts.onBoard(f);
    }
    function shift(on) { if (on && W / H < 0.9) cam.setViewOffset(W, H, 0, H * 0.17, W, H); else cam.clearViewOffset(); }
    function back() { var had = !!C.sel; C.mode = "arena"; C.sel = null; heroOff(); shift(false); if (had) reshape(700); flyTo({ yaw: 0, pitch: card ? 0.78 : 0.92, dist: homeDist(), tgt: new THREE.Vector3(0, 1.4, 0.6) }, 900); if (opts.onBack) opts.onBack(); }
    camPlace();

    // input
    var ray = new THREE.Raycaster(), pts = {}, drag = null;
    function rayAt(x, y) { var rc = r.domElement.getBoundingClientRect(); ray.setFromCamera(new THREE.Vector2(((x - rc.left) / rc.width) * 2 - 1, -((y - rc.top) / rc.height) * 2 + 1), cam); }
    function down(e) { pts[e.pointerId] = { x: e.clientX, y: e.clientY }; try { r.domElement.setPointerCapture(e.pointerId); } catch (x) {} var k = Object.keys(pts); drag = { x: e.clientX, y: e.clientY, sx: e.clientX, sy: e.clientY, moved: false, n: k.length, d0: k.length === 2 ? dist2() : 0, dd: C.dist, t: performance.now() }; C.vy = C.vp = 0; }
    function dist2() { var k = Object.keys(pts); if (k.length < 2) return 0; var a = pts[k[0]], b = pts[k[1]]; return Math.hypot(a.x - b.x, a.y - b.y); }
    function move(e) {
      if (!pts[e.pointerId] || !drag) return; pts[e.pointerId] = { x: e.clientX, y: e.clientY };
      if (card) return;
      if (Object.keys(pts).length === 2) { var d = dist2(); if (drag.d0 > 0) { C.dist = Math.max(6, Math.min(44, drag.dd * drag.d0 / d)); camPlace(); ask(); drag.moved = true; } return; }
      var dx = e.clientX - drag.x, dy = e.clientY - drag.y; if (Math.hypot(e.clientX - drag.sx, e.clientY - drag.sy) > 7) drag.moved = true; if (!drag.moved) return;
      drag.x = e.clientX; drag.y = e.clientY; C.yaw -= dx * 0.008; C.pitch = Math.max(-0.05, Math.min(1.25, C.pitch + dy * 0.005)); C.vy = -dx * 0.008; C.vp = dy * 0.005; camPlace(); ask();
    }
    function up(e) {
      delete pts[e.pointerId]; var d = drag; if (Object.keys(pts).length) return; drag = null; if (!d) return;
      if (!d.moved) { if (card) { if (opts.onOpen) opts.onOpen(); return; } tap(e.clientX, e.clientY); return; }
      if (Math.abs(C.vy) + Math.abs(C.vp) > 0.002 && !RM) anims.push(function () { C.yaw += C.vy; C.pitch = Math.max(-0.05, Math.min(1.25, C.pitch + C.vp)); C.vy *= 0.9; C.vp *= 0.9; camPlace(); return Math.abs(C.vy) + Math.abs(C.vp) > 0.0005; });
      ask();
    }
    function wheel(e) { if (card) return; e.preventDefault(); C.dist = Math.max(6, Math.min(44, C.dist * (1 + e.deltaY * 0.001))); camPlace(); ask(); }
    function tap(x, y) {
      rayAt(x, y);
      var hits = ray.intersectObjects([pillars, sk, gk, hero.mesh].concat(faces).filter(Boolean), false);
      if (!hits.length) { if (C.mode !== "arena") back(); return; }
      var h = hits[0], o = h.object;
      if (o.userData.days != null) { var D = data.days || [], i = Math.floor(h.uv.x * D.length); if (opts.onDay && D[i]) opts.onDay(i); return; }
      if (o.userData.face != null) { board(o.userData.face); return; }
      var it = null;
      if (o === hero.mesh) return;
      if (o === pillars) it = items[h.instanceId];
      else it = items.find(function (x) { return x.mesh === o && x.k === h.instanceId; });
      if (it) focus(it.side, it.p.id);
    }
    var el = r.domElement;
    el.addEventListener("pointerdown", down); el.addEventListener("pointermove", move); el.addEventListener("pointerup", up); el.addEventListener("pointercancel", function (e) { delete pts[e.pointerId]; drag = null; }); el.addEventListener("wheel", wheel, { passive: false });

    // drawing: only while something moves, and not while the box is off screen
    var raf = 0, alive = true, onScreen = true, frames = 0;
    function ask() { if (!raf && alive && onScreen && !document.hidden) raf = requestAnimationFrame(frame); }
    function frame(now) {
      raf = 0; if (!alive) return; frames++;
      anims = anims.filter(function (f) { return f(now) !== false; });
      r.render(sc, cam);
      if (anims.length) ask();
    }
    var io = window.IntersectionObserver ? new IntersectionObserver(function (es) { onScreen = es[0].isIntersecting; if (onScreen) ask(); }) : null; if (io) io.observe(box);
    function size() { var w = box.clientWidth, h = box.clientHeight; if (!w || !h) return; W = w; H = h; r.setSize(W, H); cam.aspect = W / H; cam.updateProjectionMatrix(); if (C.mode === "arena") { C.dist = homeDist(); camPlace(); } ask(); }
    var ro = window.ResizeObserver ? new ResizeObserver(size) : null; if (ro) ro.observe(box);
    var vis = function () { if (!document.hidden) ask(); }; document.addEventListener("visibilitychange", vis);
    setTheme(dark);
    return {
      set: function (d) { data = d; layout(!items.length); }, theme: setTheme, size: size, focus: focus, board: board, back: back,
      card: function (v) { card = !!v; C.pitch = card ? 0.78 : 0.92; if (C.mode === "arena") camPlace(); ask(); },
      state: function () { var hb = hero.mesh ? new THREE.Box3().setFromObject(hero.mesh) : null; if (hero.mesh) hero.mesh.geometry.computeBoundingBox(); return { pos: hero.mesh ? hero.mesh.position.toArray() : null, gb: hero.mesh ? [hero.mesh.geometry.boundingBox.min.toArray(), hero.mesh.geometry.boundingBox.max.toArray()] : null, sel1: C.sel ? [C.sel.h, C.sel.h1, C.sel.x, C.sel.z] : null, mode: C.mode, frames: frames, sel: C.sel ? C.sel.p.id : null, cam: cam.position.toArray().map(function (x) { return +x.toFixed(2); }), hero: hb ? [hb.min.toArray(), hb.max.toArray()] : null, near: cam.near, far: cam.far }; },
      destroy: function () { alive = false; if (raf) cancelAnimationFrame(raf); if (io) io.disconnect(); if (ro) ro.disconnect(); document.removeEventListener("visibilitychange", vis); r.dispose(); pm.dispose(); if (el.parentNode) el.parentNode.removeChild(el); try { r.forceContextLoss(); } catch (e) {} }
    };
  }
  window.gxArena3D = { mount: mount };
})();
