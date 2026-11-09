/* Fantasy GM: 3D Lines rink (plain script, needs vendor/gx3d.js first).
   window.gxLn3D.mount(box, opts) -> { focus(id), stop(k), next(d), back(), theme(dark), size(), destroy() }
   opts.players: [{ id, last, no, goalie, row, col, body, trim, num, ring }]  (ring: "" | "me" | "fa")
   opts.rows: row keys in order from the camera back, opts.dark, opts.base (folder of models3d/),
   opts.onPick(id), opts.onStop(id, k), opts.onBack(), opts.logo (url or "") */
(function () {
  "use strict";
  var X = window.GX3D;
  if (!X) return;
  var THREE = X.THREE;
  var STOPS = [-0.38, 1.42, 2.95, 4.62]; // around the player: back, his left side, front, his right side
  var MODELS = { sk: ["brady_low.glb", "brady_hi.glb"], gk: ["gk_low.glb", "gk_hi.glb"] };
  // where the name and number sit on each body, in model metres (x left/right, y up)
  var BACK = { sk: [-0.235, 0.235, 1.02, 1.6], gk: [-0.3, 0.3, 1.06, 1.6] };
  var FRONT = { sk: [-0.15, 0.15, 1.18, 1.46], gk: [-0.17, 0.17, 1.2, 1.48] };
  var cache = {};
  function load(url) {
    if (!cache[url]) cache[url] = new Promise(function (ok, no) { new X.GLTFLoader().load(url, ok, undefined, no); });
    return cache[url];
  }
  function ease(t) { return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; }
  function lin(c) { return new THREE.Color(c || "#888888"); }
  function reduced() { try { return window.matchMedia("(prefers-reduced-motion: reduce)").matches; } catch (e) { return false; } }

  // name and number for the back of the jersey
  function backTex(p, big) {
    var W = big ? 512 : 256, c = document.createElement("canvas"); c.width = W; c.height = W;
    var g = c.getContext("2d"), s = W / 512, nm = String(p.last || "").toUpperCase(), no = p.no == null ? "" : String(p.no);
    g.textAlign = "center"; g.textBaseline = "alphabetic";
    var fs = Math.min(64, 900 / Math.max(6, nm.length)) * s;
    g.font = "900 " + fs + "px 'Arial Black', 'Helvetica Neue', Arial, sans-serif";
    g.lineJoin = "round"; g.lineWidth = 7 * s; g.strokeStyle = p.trim || "#000"; g.fillStyle = p.num || "#fff";
    if (nm) { g.strokeText(nm, W / 2, 96 * s, W * 0.92); g.fillText(nm, W / 2, 96 * s, W * 0.92); }
    if (no) {
      g.font = "900 " + 300 * s + "px 'Arial Black', Impact, 'Helvetica Neue', Arial, sans-serif"; g.lineWidth = 16 * s;
      g.strokeText(no, W / 2, 400 * s, W * 0.86); g.fillText(no, W / 2, 400 * s, W * 0.86);
    }
    var t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 4; return t;
  }
  function frontTex(p, img) {
    var W = 256, c = document.createElement("canvas"); c.width = c.height = W; var g = c.getContext("2d");
    if (img) { try { var r = Math.min(W / img.width, W / img.height) * 0.96; g.drawImage(img, (W - img.width * r) / 2, (W - img.height * r) / 2, img.width * r, img.height * r); } catch (e) {} }
    else if (p.no != null) { g.textAlign = "center"; g.font = "900 120px 'Arial Black', Arial, sans-serif"; g.lineWidth = 8; g.strokeStyle = p.trim; g.fillStyle = p.num; g.strokeText(p.no, W / 2, 170); g.fillText(p.no, W / 2, 170); }
    var t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t;
  }

  // team colours painted over the model's own colours, plus name / number / crest projected on
  function teamMat(src, p, kind, fileM, dec, crest) {
    var m = src.clone();
    m.metalness = 0; if (m.roughness < 0.35) m.roughness = 0.4;
    var U = {
      uBody: { value: lin(p.body) }, uTrim: { value: lin(p.trim) }, uQ: { value: fileM.clone() }, uDim: { value: 1 }, uFade: { value: 1 },
      uDec: { value: dec }, uCrest: { value: crest }, uKind: { value: kind === "gk" ? 1 : 0 },
      uBk: { value: new THREE.Vector4().fromArray(BACK[kind]) }, uFr: { value: new THREE.Vector4().fromArray(FRONT[kind]) }
    };
    m.userData.U = U;
    m.onBeforeCompile = function (sh) {
      Object.keys(U).forEach(function (k) { sh.uniforms[k] = U[k]; });
      sh.vertexShader = sh.vertexShader.replace("#include <common>", "#include <common>\nuniform mat4 uQ; varying vec3 vMP; varying vec3 vMN;")
        .replace("#include <begin_vertex>", "#include <begin_vertex>\nvMP = (uQ * vec4(position, 1.0)).xyz; vMN = normalize(mat3(uQ) * objectNormal);");
      sh.fragmentShader = sh.fragmentShader.replace("#include <common>", [
        "#include <common>",
        "uniform vec3 uBody, uTrim; uniform float uDim, uKind, uFade; uniform sampler2D uDec, uCrest; uniform vec4 uBk, uFr; varying vec3 vMP; varying vec3 vMN;",
        "vec3 gxHsv(vec3 c){ vec4 K = vec4(0., -1./3., 2./3., -1.); vec4 p = mix(vec4(c.bg, K.wz), vec4(c.gb, K.xy), step(c.b, c.g)); vec4 q = mix(vec4(p.xyw, c.r), vec4(c.r, p.yzx), step(p.x, c.r)); float d = q.x - min(q.w, q.y); return vec3(abs(q.z + (q.w - q.y) / (6. * d + 1e-10)), d / (q.x + 1e-10), q.x); }"
      ].join("\n")).replace("#include <color_fragment>", [
        "#include <color_fragment>",
        "if (uFade < 0.999) { vec2 q = floor(mod(gl_FragCoord.xy, 4.)); float b = (q.x * 4. + q.y) / 16.; b = fract(b * 7.31 + q.y * .37); if (b >= uFade) discard; }",
        "{ vec3 lc = diffuseColor.rgb, sc = pow(max(lc, vec3(0.)), vec3(1. / 2.2)), h = gxHsv(sc); float y = vMP.y, ax = abs(vMP.x);",
        "  if (uKind < 0.5) {",
        "    float red = step(0.42, h.y) * (step(h.x, 0.045) + step(0.93, h.x)) * step(0.18, h.z);",
        "    if (red > 0.5) diffuseColor.rgb = uBody * clamp(max(lc.r, max(lc.g, lc.b)) / 0.62, 0.22, 1.35);",
        "    float sock = step(0.24, y) * step(y, 0.62) * step(h.y, 0.22) * step(0.62, h.z);",
        "    if (sock > 0.5) diffuseColor.rgb = uTrim * clamp(h.z / 0.85, 0.5, 1.2);",
        "  } else {",
        "    float wh = step(h.y, 0.2) * step(0.5, h.z);",
        "    float jer = max(step(1.13, y), step(0.97, y) * step(ax, 0.4)) * step(y, 1.63);",
        "    float mask = step(1.6, y) * step(ax, 0.17);",
        "    if (wh * max(jer, mask) > 0.5) diffuseColor.rgb = uBody * clamp(h.z / 0.9, 0.3, 1.15);",
        "    float hem = step(1.0, y) * step(y, 1.06) * step(ax, 0.4) + step(1.2, y) * step(y, 1.26) * step(0.33, ax) * step(ax, 0.56);",
        "    if (wh * hem > 0.5) diffuseColor.rgb = uTrim * clamp(h.z / 0.9, 0.4, 1.15);",
        "  }",
        "  vec2 bu = vec2((uBk.y - vMP.x) / (uBk.y - uBk.x), (vMP.y - uBk.z) / (uBk.w - uBk.z));",
        "  if (vMN.z < -0.3 && vMP.z < 0.08 && bu.x > 0. && bu.x < 1. && bu.y > 0. && bu.y < 1.) { vec4 d = texture2D(uDec, bu); diffuseColor.rgb = mix(diffuseColor.rgb, d.rgb, d.a); }",
        "  vec2 fu = vec2((vMP.x - uFr.x) / (uFr.y - uFr.x), (vMP.y - uFr.z) / (uFr.w - uFr.z));",
        "  if (vMN.z > 0.35 && vMP.z > 0.0 && fu.x > 0. && fu.x < 1. && fu.y > 0. && fu.y < 1.) { vec4 d = texture2D(uCrest, fu); diffuseColor.rgb = mix(diffuseColor.rgb, d.rgb, d.a); }",
        "  diffuseColor.rgb *= uDim; }"
      ].join("\n"));
    };
    m.customProgramCacheKey = function () { return "gxln3d-" + (m.map ? "t" : "v") + (m.normalMap ? "n" : ""); };
    return m;
  }

  // one copy of a model for one player
  function dress(gltf, p, kind, big) {
    var root = gltf.scene, g = new THREE.Group(); root.updateMatrixWorld(true);
    var inv = new THREE.Matrix4().copy(root.matrixWorld).invert();
    var dec = backTex(p, big), crest = frontTex(p, p._logo || null), mats = [];
    root.traverse(function (o) {
      if (!o.isMesh) return;
      var fm = new THREE.Matrix4().multiplyMatrices(inv, o.matrixWorld);
      var part = (o.name || "").toLowerCase(), plain = part.indexOf("stick") >= 0 || part.indexOf("knob") >= 0;
      var mat;
      if (plain) { mat = o.material.clone(); mat.userData.U = { uDim: { value: 1 }, uFade: { value: 1 } }; mat.onBeforeCompile = function (sh) { sh.uniforms.uDim = mat.userData.U.uDim; sh.uniforms.uFade = mat.userData.U.uFade; sh.fragmentShader = sh.fragmentShader.replace("#include <common>", "#include <common>\nuniform float uDim, uFade;").replace("#include <color_fragment>", "#include <color_fragment>\nif (uFade < 0.999) { vec2 q = floor(mod(gl_FragCoord.xy, 4.)); float b = fract((q.x * 4. + q.y) / 16. * 7.31 + q.y * .37); if (b >= uFade) discard; }\ndiffuseColor.rgb *= uDim;"); }; mat.customProgramCacheKey = function () { return "gxln3d-plain" + (mat.map ? "t" : "v"); }; }
      else mat = teamMat(o.material, p, kind, fm, dec, crest);
      var mesh = new THREE.Mesh(o.geometry, mat); mesh.applyMatrix4(fm); mesh.castShadow = true; mesh.receiveShadow = true; mesh.frustumCulled = true;
      g.add(mesh); mats.push(mat);
    });
    g.userData.mats = mats; g.userData.tex = [dec, crest];
    return g;
  }

  function iceTexture(dark) {
    var W = 2048, H = 4096, c = document.createElement("canvas"); c.width = W; c.height = H; var g = c.getContext("2d");
    g.fillStyle = dark ? "#0d1118" : "#eef3f8"; g.fillRect(0, 0, W, H);
    for (var i = 0; i < 14000; i++) { g.fillStyle = dark ? "rgba(255,255,255," + Math.random() * 0.05 + ")" : "rgba(150,170,195," + Math.random() * 0.08 + ")"; g.fillRect(Math.random() * W, Math.random() * H, 4 + Math.random() * 60, 1.5); }
    var px = W / 30; // 30 m wide sheet, 60 m long; z = 0 at H * 0.25
    var Z = function (z) { return H * 0.25 + z * px; }, Xm = function (x) { return W / 2 - x * px; };
    var red = dark ? "rgba(220,40,50,0.85)" : "rgba(200,30,40,0.8)", blue = dark ? "rgba(40,90,230,0.85)" : "rgba(30,70,200,0.75)";
    g.fillStyle = blue; g.fillRect(0, Z(-3.2) - 0.15 * px, W, 0.3 * px); // blue line in front of the first line
    g.fillStyle = red; g.fillRect(0, Z(-9) - 0.15 * px, W, 0.3 * px);
    g.strokeStyle = blue; g.lineWidth = 0.08 * px; g.beginPath(); g.arc(Xm(0), Z(-9), 4.5 * px, 0, Math.PI * 2); g.stroke();
    g.strokeStyle = red; [[-4.8, 7.6], [4.8, 7.6]].forEach(function (q) { g.beginPath(); g.arc(Xm(q[0]), Z(q[1]), 4.5 * px, 0, Math.PI * 2); g.stroke(); g.fillStyle = red; g.beginPath(); g.arc(Xm(q[0]), Z(q[1]), 0.3 * px, 0, Math.PI * 2); g.fill(); });
    g.fillStyle = red; g.fillRect(0, Z(17.3) - 0.03 * px, W, 0.06 * px); // goal line
    g.fillStyle = dark ? "rgba(40,90,230,0.45)" : "rgba(60,120,240,0.35)"; g.beginPath(); g.moveTo(Xm(-1.22), Z(17.3)); g.lineTo(Xm(-1.22), Z(16.1)); g.arc(Xm(0), Z(17.3), 1.83 * px, Math.PI * 1.22, Math.PI * 1.78); g.lineTo(Xm(1.22), Z(17.3)); g.closePath(); g.fill();
    var t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8; return t;
  }
  function glowTex(rgb) {
    var c = document.createElement("canvas"); c.width = c.height = 128; var g = c.getContext("2d"), gr = g.createRadialGradient(64, 64, 4, 64, 64, 64);
    gr.addColorStop(0, "rgba(" + rgb + ",0.75)"); gr.addColorStop(1, "rgba(" + rgb + ",0)"); g.fillStyle = gr; g.fillRect(0, 0, 128, 128); return new THREE.CanvasTexture(c);
  }
  function labelTex(txt, col) {
    var c = document.createElement("canvas"); c.width = 256; c.height = 128; var g = c.getContext("2d");
    g.font = "900 84px 'Arial Black', Arial, sans-serif"; g.textAlign = "center"; g.fillStyle = col; g.fillText(txt, 128, 96);
    var t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t;
  }

  function mount(box, opts) {
    var dark = opts.dark !== false, base = opts.base || "", RM = reduced();
    var W = box.clientWidth || 360, H = box.clientHeight || 600;
    var r = new THREE.WebGLRenderer({ antialias: true, alpha: false, powerPreference: "high-performance" });
    var PR = Math.min(window.devicePixelRatio || 1, 2); r.setPixelRatio(PR); r.setSize(W, H);
    r.toneMapping = THREE.ACESFilmicToneMapping; r.outputColorSpace = THREE.SRGBColorSpace; r.shadowMap.enabled = true; r.shadowMap.type = THREE.PCFSoftShadowMap;
    r.domElement.style.cssText = "display:block;width:100%;height:100%;touch-action:none;outline:none";
    box.appendChild(r.domElement);
    var tags = document.createElement("div"); tags.className = "gx3t"; tags.style.cssText = "position:absolute;inset:0;pointer-events:none;overflow:hidden"; box.appendChild(tags);
    var sc = new THREE.Scene();
    var pm = new THREE.PMREMGenerator(r), env = pm.fromScene(new X.RoomEnvironment(), 0.04).texture; sc.environment = env;
    var cam = new THREE.PerspectiveCamera(46, W / H, 0.05, 120);

    // ice: a mirror under a frosted sheet with the markings
    var mir = new X.Reflector(new THREE.PlaneGeometry(40, 70), { textureWidth: Math.round(W * PR * 0.5), textureHeight: Math.round(H * PR * 0.5), color: 0x8090a4 });
    mir.rotation.x = -Math.PI / 2; mir.position.set(0, -0.003, 12); sc.add(mir);
    var iceM = new THREE.MeshStandardMaterial({ map: iceTexture(dark), transparent: true, opacity: 0.86, roughness: 0.3, metalness: 0 });
    var ice = new THREE.Mesh(new THREE.PlaneGeometry(30, 60), iceM); ice.rotation.x = -Math.PI / 2; ice.position.set(0, 0, 15 - 0.25 * 60 + 15); ice.receiveShadow = true; sc.add(ice);
    // ice plane: texture row 0.25 is z = 0, so its centre sits at z = 15
    ice.position.z = 15;
    // boards, glass edge and crowd lights
    var boards = { material: new THREE.MeshStandardMaterial({ color: 0xe8edf3, roughness: 0.5 }) };
    var stripM = new THREE.MeshBasicMaterial({ color: lin(opts.accent || "#ff3b30") });
    [[0, -15, 0, 30], [0, 45, Math.PI, 30], [-15, 15, Math.PI / 2, 60], [15, 15, -Math.PI / 2, 60]].forEach(function (w) {
      var m = new THREE.Mesh(new THREE.PlaneGeometry(w[3], 1.1), boards.material); m.position.set(w[0], 0.55, w[1]); m.rotation.y = w[2]; sc.add(m);
      var s = new THREE.Mesh(new THREE.PlaneGeometry(w[3], 0.14), stripM); s.position.set(w[0], 1.0, w[1]); s.rotation.y = w[2]; s.position.add(new THREE.Vector3(0, 0, 0.01).applyAxisAngle(new THREE.Vector3(0, 1, 0), w[2])); sc.add(s);
    });
    var bok = document.createElement("canvas"); bok.width = bok.height = 64; (function () { var c = bok.getContext("2d"), gr = c.createRadialGradient(32, 32, 0, 32, 32, 32); gr.addColorStop(0, "rgba(255,255,255,1)"); gr.addColorStop(0.4, "rgba(255,255,255,.35)"); gr.addColorStop(1, "rgba(255,255,255,0)"); c.fillStyle = gr; c.fillRect(0, 0, 64, 64); })();
    var NB = 520, bp = new Float32Array(NB * 3), bc = new Float32Array(NB * 3);
    for (var i = 0; i < NB; i++) { var side = Math.random(), x, z; if (side < 0.5) { x = (Math.random() < 0.5 ? -1 : 1) * (17 + Math.random() * 6); z = -12 + Math.random() * 50; } else { x = -22 + Math.random() * 44; z = 47 + Math.random() * 6; } bp.set([x, 2.5 + Math.random() * 9, z], i * 3); var w = Math.random(), cc = w < 0.14 ? [1, 0.32, 0.25] : w < 0.28 ? [0.4, 0.6, 1] : [1, 0.92, 0.78], k = 0.25 + Math.random() * 0.75; bc.set([cc[0] * k, cc[1] * k, cc[2] * k], i * 3); }
    var bg = new THREE.BufferGeometry(); bg.setAttribute("position", new THREE.BufferAttribute(bp, 3)); bg.setAttribute("color", new THREE.BufferAttribute(bc, 3));
    var crowd = new THREE.Points(bg, new THREE.PointsMaterial({ map: new THREE.CanvasTexture(bok), size: 0.9, vertexColors: true, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, fog: false })); sc.add(crowd);
    // net behind the goalies
    var NET = {};
    (function () {
      var net = new THREE.Group(), red = new THREE.MeshStandardMaterial({ color: 0xd0202a, roughness: 0.35 }), r0 = 0.03;
      var pipe = function (a, b) { var d = new THREE.Vector3().subVectors(b, a), m = new THREE.Mesh(new THREE.CylinderGeometry(r0, r0, d.length(), 10), red); m.position.copy(a).add(b).multiplyScalar(0.5); m.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), d.normalize()); m.castShadow = true; net.add(m); };
      var V = function (x, y, z) { return new THREE.Vector3(x, y, z); };
      pipe(V(-0.915, 0, 0), V(-0.915, 1.22, 0)); pipe(V(0.915, 0, 0), V(0.915, 1.22, 0)); pipe(V(-0.915, 1.22, 0), V(0.915, 1.22, 0));
      pipe(V(-0.915, 1.22, 0), V(-0.6, 1.0, 0.55)); pipe(V(0.915, 1.22, 0), V(0.6, 1.0, 0.55)); pipe(V(-0.6, 1.0, 0.55), V(0.6, 1.0, 0.55));
      var nc = document.createElement("canvas"); nc.width = nc.height = 128; var ng = nc.getContext("2d"); ng.strokeStyle = "rgba(255,255,255,0.75)"; ng.lineWidth = 2; for (var q = 0; q <= 128; q += 12) { ng.beginPath(); ng.moveTo(q, 0); ng.lineTo(q, 128); ng.stroke(); ng.beginPath(); ng.moveTo(0, q); ng.lineTo(128, q); ng.stroke(); }
      var nt = new THREE.CanvasTexture(nc); nt.wrapS = nt.wrapT = THREE.RepeatWrapping; nt.repeat.set(4, 3);
      var mesh = new THREE.Mesh(new THREE.CylinderGeometry(0.8, 0.95, 1.2, 20, 1, true, -Math.PI / 2, Math.PI), new THREE.MeshBasicMaterial({ map: nt, transparent: true, side: THREE.DoubleSide, depthWrite: false }));
      mesh.position.set(0, 0.6, 0.02); mesh.scale.set(1, 1, 0.6); net.add(mesh);
      net.position.set(0, 0, 17.3); sc.add(net); NET.o = net;
    })();

    // lights
    var hemi = new THREE.HemisphereLight(0xdfe8ff, 0x1a1d24, 0.5); sc.add(hemi);
    var sun = new THREE.DirectionalLight(0xffffff, 1.6); sun.position.set(3, 12, -4); sun.target.position.set(0, 0, 8); sun.castShadow = true;
    sun.shadow.mapSize.set(2048, 2048); Object.assign(sun.shadow.camera, { left: -6, right: 6, top: 14, bottom: -14, near: 1, far: 40 }); sun.shadow.bias = -0.0004; sun.shadow.radius = 3; sc.add(sun, sun.target);
    var spot = new THREE.SpotLight(0xffffff, 0, 14, 0.36, 0.65, 1.4); spot.position.set(0.6, 7, 0); spot.castShadow = true; spot.shadow.mapSize.set(1024, 1024); spot.shadow.bias = -0.0003; sc.add(spot, spot.target);
    var rimA = new THREE.SpotLight(0xff3a2a, 0, 12, 0.5, 0.8, 1.2), rimB = new THREE.SpotLight(0x6fa8ff, 0, 12, 0.5, 0.8, 1.2); sc.add(rimA, rimA.target, rimB, rimB.target);
    var fill = new THREE.DirectionalLight(0xdfe8ff, 0.6); fill.position.set(-3, 4, -8); sc.add(fill);
    var ringC = lin(opts.accent || "#ff3b30");
    var ring = new THREE.Mesh(new THREE.RingGeometry(0.6, 0.64, 96), new THREE.MeshBasicMaterial({ color: ringC, transparent: true, opacity: 0, blending: THREE.AdditiveBlending, depthWrite: false })); ring.rotation.x = -Math.PI / 2; ring.position.y = 0.008; sc.add(ring);
    var pool = new THREE.Mesh(new THREE.PlaneGeometry(2.6, 2.6), new THREE.MeshBasicMaterial({ map: glowTex("255,90,70"), transparent: true, opacity: 0, blending: THREE.AdditiveBlending, depthWrite: false })); pool.rotation.x = -Math.PI / 2; pool.position.y = 0.006; sc.add(pool);

    // post effects: soft glow on the brightest bits
    var comp = new X.EffectComposer(r); comp.setPixelRatio(PR); comp.setSize(W, H); comp.addPass(new X.RenderPass(sc, cam));
    var bloom = new X.UnrealBloomPass(new THREE.Vector2(W / 2, H / 2), 0.35, 0.5, 0.96); comp.addPass(bloom); comp.addPass(new X.OutputPass());

    function setTheme(d) {
      dark = d;
      sc.background = new THREE.Color(d ? 0x04060b : 0xdfe6ee); sc.fog = new THREE.FogExp2(d ? 0x04060b : 0xdfe6ee, d ? 0.035 : 0.022);
      r.toneMappingExposure = d ? 0.95 : 1.0; sc.environmentIntensity = d ? 0.35 : 0.8;
      iceM.map = iceTexture(d); iceM.opacity = d ? 0.86 : 0.93; iceM.envMapIntensity = d ? 0.12 : 0.5; iceM.needsUpdate = true;
      boards.material.color.set(d ? 0x3c434e : 0xf4f7fa); hemi.intensity = d ? 0.5 : 1.3; hemi.groundColor.set(d ? 0x1a1d24 : 0xb9c3cf);
      sun.intensity = d ? 1.5 : 2.2; fill.intensity = d ? 0.6 : 0.9; crowd.material.opacity = d ? 1 : 0.35; bloom.strength = d ? 0.35 : 0.12;
      labels.forEach(function (l) { l.material.opacity = d ? 0.55 : 0.7; });
      ask();
    }

    // players
    var rows = opts.rows || [], RZ = {}, zz = 0, P = {}, list = [];
    rows.forEach(function (k, i) { if (i > 0) zz += k[0] === "D" && rows[i - 1][0] !== "D" ? 3.0 : k === "G" ? 2.8 : 2.4; RZ[k] = zz; });
    var labels = [];
    rows.forEach(function (k) {
      var lm = new THREE.Mesh(new THREE.PlaneGeometry(1.2, 0.6), new THREE.MeshBasicMaterial({ map: labelTex(k, dark ? "#ffffff" : "#0b1220"), transparent: true, opacity: 0.55, depthWrite: false }));
      lm.visible = false; lm.rotation.x = -Math.PI / 2; lm.rotation.z = Math.PI; lm.position.set(k === "G" ? 2.9 : 3.0, 0.01, RZ[k] + 0.2); sc.add(lm); labels.push(lm);
    });
    var pickG = new THREE.Group(); sc.add(pickG);
    var pickGeo = new THREE.CylinderGeometry(0.42, 0.42, 2.0, 8), pickMat = new THREE.MeshBasicMaterial({ visible: false });
    (opts.players || []).forEach(function (p) {
      var kind = p.goalie ? "gk" : "sk", n = (opts.players || []).filter(function (q) { return q.row === p.row; }).length;
      var gap = kind === "gk" ? 1.9 : n === 2 ? 1.8 : (W / H < 0.75 ? 1.55 : 1.75), x = (((n - 1) / 2) - p.col) * gap;
      var it = { p: p, kind: kind, x: x, z: RZ[p.row] || 0, low: null, hi: null, grp: new THREE.Group() };
      it.grp.position.set(x, 0, it.z); sc.add(it.grp);
      var pk = new THREE.Mesh(pickGeo, pickMat); pk.position.set(x, 1, it.z); pk.userData.id = p.id; pickG.add(pk);
      var tg = document.createElement("div"); tg.className = "gx3tg" + (p.ring ? " " + p.ring : ""); tg.innerHTML = "<b></b><span></span>";
      tg.firstChild.textContent = p.no != null ? "#" + p.no : ""; tg.lastChild.textContent = p.last || ""; tags.appendChild(tg); it.tag = tg;
      P[p.id] = it; list.push(it);
    });
    var maxZ = zz;
    // logo for the chest (only if the server lets the browser read it)
    var logoImg = null;
    if (opts.logo) { var im = new Image(); im.crossOrigin = "anonymous"; im.onload = function () { logoImg = im; list.forEach(function (it) { [it.low, it.hi].forEach(function (g) { if (g) { var t = frontTex(it.p, im); g.userData.mats.forEach(function (m) { if (m.userData.U.uCrest) m.userData.U.uCrest.value = t; }); } }); }); ask(); }; im.src = opts.logo; }
    load(base + MODELS.sk[0]).then(function (gs) {
      return load(base + MODELS.gk[0]).then(function (gg) {
        list.forEach(function (it) { it.p._logo = logoImg; it.low = dress(it.kind === "gk" ? gg : gs, it.p, it.kind, false); it.grp.add(it.low); });
        ask(); if (opts.onReady) opts.onReady();
      });
    }).catch(function (e) { if (opts.onError) opts.onError(e); });

    // camera: lineup view moves along the rows; focus view circles one player
    var S = { mode: "line", lz: 0, lzv: 0, id: null, k: 0, th: STOPS[0], fly: null, t0: performance.now() };
    function lineCam(z) { var narrow = W / H < 0.75; var back = narrow ? 8.4 : 6.6, up = narrow ? 6.0 : 4.6; return { pos: new THREE.Vector3(0, up, z - back), look: new THREE.Vector3(0, 0.4, z + (narrow ? 3.0 : 3.0)) }; }
    function stopCam(it, th) { var narrow = W / H < 0.75, d = (narrow ? 6.6 : 5.4) * (it.kind === "gk" ? 1.06 : 1), h = 1.55; var c = new THREE.Vector3(it.x, 0, it.z); return { pos: new THREE.Vector3(c.x + Math.sin(th) * d, h, c.z - Math.cos(th) * d), look: new THREE.Vector3(c.x, 0.97, c.z), c: c, th: th, d: d, h: h }; }
    function setCam(pos, look) { cam.position.copy(pos); cam.lookAt(look); }
    var FOV = { line: 46, focus: 30 }; function fov(v) { if (Math.abs(cam.fov - v) > 0.01) { cam.fov = v; cam.updateProjectionMatrix(); } }
    function curLook() { var d = new THREE.Vector3(); cam.getWorldDirection(d); return cam.position.clone().add(d.multiplyScalar(5)); }
    function viewShift(on) { // in focus the player sits in the top half so the stats fit below
      if (on && W / H < 0.75) cam.setViewOffset(W, H, 0, H * 0.17, W, H); else cam.clearViewOffset();
    }
    var L0 = lineCam(0); setCam(L0.pos, L0.look);

    function dimAll(v, keep) { // v 1 = everyone shown, 0 = only the kept player
      list.forEach(function (it) { var me = it.p.id === keep, f = me ? 1 : v; it.grp.visible = f > 0.01;
        [it.low, it.hi].forEach(function (g) { if (g) g.userData.mats.forEach(function (m) { m.userData.U.uFade.value = f; m.userData.U.uDim.value = me ? 1 : 0.55 + 0.45 * f; }); });
        it.grp.traverse(function (o) { if (o.isMesh) o.castShadow = f > 0.5; }); }); }
    function hiFor(it) {
      if (it.hi) return Promise.resolve(it.hi);
      return load(base + MODELS[it.kind][1]).then(function (gl) { it.p._logo = logoImg; it.hi = dress(gl, it.p, it.kind, true); it.hi.visible = false; it.grp.add(it.hi); return it.hi; });
    }
    function show(it, hi) { if (it.low) it.low.visible = !hi || !it.hi; if (it.hi) it.hi.visible = !!hi; }
    function lights(it, on) {
      var c = new THREE.Vector3(it ? it.x : 0, 0, it ? it.z : 0);
      spot.position.set(c.x + 0.6, 7, c.z - 1.5); spot.target.position.set(c.x, 0.9, c.z);
      rimA.position.set(c.x - 2.6, 2.6, c.z + 3); rimA.target.position.set(c.x, 1.1, c.z); rimB.position.set(c.x + 2.8, 2.2, c.z + 2.6); rimB.target.position.set(c.x, 1.1, c.z);
      if (it) { rimA.color.copy(lin(it.p.body)).lerp(new THREE.Color(1, 1, 1), 0.25); ring.material.color.copy(rimA.color); ring.position.x = pool.position.x = c.x; ring.position.z = pool.position.z = c.z; }
    }
    var lt = { on: 0 };
    function anim(from, to, dur, step, done) { var t0 = performance.now(); S.fly = function (now) { var t = Math.min(1, (now - t0) / (RM ? Math.min(dur, 250) : dur)), e = ease(t); step(e, t); if (t >= 1) { S.fly = null; if (done) done(); } }; ask(); }

    function focus(id) {
      var it = P[id]; if (!it) return;
      var prev = S.id && P[S.id], fromPos = cam.position.clone(), fromLook = curLook(), wasLine = S.mode === "line";
      S.mode = "fly"; S.id = id; var th = wasLine ? STOPS[0] : S.th, to = stopCam(it, th);
      hideTags(true); lights(it, true); viewShift(true); if (NET.o) NET.o.visible = false;
      hiFor(it).then(function () { if (S.id === id) { show(it, true); ask(); } });
      var fromOn = lt.on;
      anim(0, 1, wasLine ? 1250 : 950, function (e, t) {
        if (wasLine) { cam.position.lerpVectors(fromPos, to.pos, e); cam.position.y += Math.sin(Math.PI * e) * 0.6; }
        else { var pc = prev ? new THREE.Vector3(prev.x, 0, prev.z) : to.c, c = pc.clone().lerp(to.c, e); cam.position.set(c.x + Math.sin(th) * to.d, to.h + Math.sin(Math.PI * e) * 0.9, c.z - Math.cos(th) * to.d); }
        var lk = fromLook.clone().lerp(to.look, e); cam.lookAt(lk);
        lt.on = fromOn + (1 - fromOn) * e; applyLt(); if (wasLine) fov(FOV.line + (FOV.focus - FOV.line) * e); dimAll(1 - e, id); if (prev && prev !== it) { prev.grp.children.forEach(function () {}); }
      }, function () { S.mode = "focus"; S.th = th; if (prev && prev !== it) show(prev, false); if (opts.onStop) opts.onStop(id, S.k); dimAll(0, id); });
      if (opts.onStop) opts.onStop(id, S.k);
    }
    function applyLt() {
      var d = dark, on = lt.on; spot.intensity = on * (d ? 95 : 70); rimA.intensity = on * (d ? 70 : 30); rimB.intensity = on * (d ? 55 : 25);
      sun.intensity = (d ? 1.5 : 2.2) * (1 - 0.55 * on); ring.material.opacity = 0.9 * on; pool.material.opacity = (d ? 0.9 : 0.5) * on;
    }
    function stop(k) {
      if (!S.id || S.mode === "line") return; var it = P[S.id], n = STOPS.length; k = ((k % n) + n) % n;
      var a0 = S.th, target = STOPS[k]; // move the short way round
      while (target - a0 > Math.PI) target -= Math.PI * 2; while (a0 - target > Math.PI) target += Math.PI * 2;
      S.k = k; S.mode = "fly"; if (opts.onStop) opts.onStop(S.id, k);
      anim(0, 1, 900, function (e) { var th = a0 + (target - a0) * e, c = stopCam(it, th); cam.position.copy(c.pos); cam.position.y += Math.sin(Math.PI * e) * 0.15; cam.lookAt(c.look); }, function () { S.th = target; S.mode = "focus"; });
    }
    function back() {
      if (S.mode === "line" || !S.id) return; var it = P[S.id], fromPos = cam.position.clone(), fromLook = curLook();
      S.lz = Math.max(0, Math.min(maxZ, it.z - 1.2)); var to = lineCam(S.lz); S.mode = "fly"; viewShift(false); var fromOn = lt.on;
      anim(0, 1, 1000, function (e) { cam.position.lerpVectors(fromPos, to.pos, e); cam.position.y += Math.sin(Math.PI * e) * 0.4; cam.lookAt(fromLook.clone().lerp(to.look, e)); lt.on = fromOn * (1 - e); applyLt(); dimAll(e, S.id); fov(FOV.focus + (FOV.line - FOV.focus) * e); },
        function () { if (NET.o) NET.o.visible = true; show(it, false); S.mode = "line"; S.id = null; S.k = 0; hideTags(false); dimAll(1, null); if (opts.onBack) opts.onBack(); });
    }
    function next(d) { if (!S.id) return; var i = list.findIndex(function (x) { return x.p.id === S.id; }), j = i + d; if (j < 0 || j >= list.length) return; focus(list[j].p.id); }
    function jump(row) { if (S.mode !== "line") return; var z0 = S.lz, z1 = Math.max(0, Math.min(maxZ, (RZ[row] || 0) - 1.5)); anim(0, 1, 650, function (e) { S.lz = z0 + (z1 - z0) * e; var c = lineCam(S.lz); setCam(c.pos, c.look); }); }

    // tags follow the players in the lineup view
    var hidden = false;
    function hideTags(h) { hidden = h; tags.style.opacity = h ? "0" : "1"; }
    tags.style.transition = "opacity .25s";
    var v3 = new THREE.Vector3();
    function placeTags() {
      if (hidden) return;
      list.forEach(function (it) { v3.set(it.x, 0, it.z - 0.25).project(cam); var vis = v3.z < 1 && v3.x > -1.2 && v3.x < 1.2 && v3.y > -1.2 && v3.y < 1.2;
        it.tag.style.display = vis ? "" : "none"; if (vis) { var d = cam.position.distanceTo(it.grp.position), s = Math.max(0.6, Math.min(1.15, 9 / d)); it.tag.style.transform = "translate(" + ((v3.x + 1) / 2 * W).toFixed(1) + "px," + ((1 - v3.y) / 2 * H).toFixed(1) + "px) translate(-50%,2px) scale(" + s.toFixed(3) + ")"; it.tag.style.zIndex = String(1000 - Math.round(d * 10)); } });
    }

    // input: drag up / down moves along the lineup, tap picks a player
    var ray = new THREE.Raycaster(), ptr = null;
    function down(e) { ptr = { x: e.clientX, y: e.clientY, z: S.lz, t: performance.now(), moved: false, ly: e.clientY, lt: performance.now() }; S.lzv = 0; try { r.domElement.setPointerCapture(e.pointerId); } catch (x) {} }
    function move(e) {
      if (!ptr) return; var dy = e.clientY - ptr.y, dx = e.clientX - ptr.x; if (Math.abs(dy) > 6 || Math.abs(dx) > 6) ptr.moved = true;
      if (S.mode === "line" && ptr.moved) { var now = performance.now(); S.lz = Math.max(-0.5, Math.min(maxZ + 0.5, ptr.z + dy * 0.028)); S.lzv = (e.clientY - ptr.ly) * 0.028 / Math.max(8, now - ptr.lt) * 16; ptr.ly = e.clientY; ptr.lt = now; var c = lineCam(S.lz); setCam(c.pos, c.look); ask(); }
      if (S.mode === "focus" && ptr.moved && Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy) * 1.4 && !ptr.sw) { ptr.sw = true; stop(S.k + (dx < 0 ? 1 : -1)); }
    }
    function up(e) {
      var p0 = ptr; ptr = null; if (!p0) return;
      if (!p0.moved) {
        var rc = r.domElement.getBoundingClientRect(), m = new THREE.Vector2(((e.clientX - rc.left) / rc.width) * 2 - 1, -((e.clientY - rc.top) / rc.height) * 2 + 1);
        ray.setFromCamera(m, cam); var hit = ray.intersectObjects(pickG.children, false)[0];
        if (S.mode === "line" && hit) { if (opts.onPick) opts.onPick(hit.object.userData.id); focus(hit.object.userData.id); }
        else if (S.mode === "focus" && hit && hit.object.userData.id !== S.id) { if (opts.onPick) opts.onPick(hit.object.userData.id); focus(hit.object.userData.id); }
      }
    }
    r.domElement.addEventListener("pointerdown", down); r.domElement.addEventListener("pointermove", move); r.domElement.addEventListener("pointerup", up); r.domElement.addEventListener("pointercancel", function () { ptr = null; });

    // drawing only when something moves
    var raf = 0, alive = true, lastT = performance.now(), frames = 0;
    function ask() { if (!raf && alive) raf = requestAnimationFrame(frame); }
    function frame(now) {
      raf = 0; if (!alive) return; frames++;
      var dt = Math.min(50, now - lastT); lastT = now; var more = false;
      if (S.fly) { S.fly(now); more = true; }
      else if (S.mode === "line" && !ptr && Math.abs(S.lzv) > 0.002) { S.lz = Math.max(-0.5, Math.min(maxZ + 0.5, S.lz + S.lzv)); S.lzv *= 0.92; var c = lineCam(S.lz); setCam(c.pos, c.look); more = true; }
      else if (S.mode === "line" && !ptr && (S.lz < 0 || S.lz > maxZ)) { S.lz += ((S.lz < 0 ? 0 : maxZ) - S.lz) * 0.2; if (Math.abs(S.lz - Math.max(0, Math.min(maxZ, S.lz))) < 0.01) S.lz = Math.max(0, Math.min(maxZ, S.lz)); var c2 = lineCam(S.lz); setCam(c2.pos, c2.look); more = true; }
      else if (S.mode === "focus" && !RM) { var it = P[S.id], t = (now - S.t0) / 1000, th = S.th + Math.sin(t * 0.35) * 0.07, c3 = stopCam(it, th); cam.position.copy(c3.pos); cam.position.y += Math.sin(t * 0.5) * 0.03; cam.lookAt(c3.look); ring.scale.setScalar(1 + Math.sin(t * 2) * 0.03); more = true; }
      comp.render(); placeTags();
      if (more) ask();
    }
    function size() {
      W = box.clientWidth || W; H = box.clientHeight || H; r.setSize(W, H); comp.setSize(W, H); cam.aspect = W / H; cam.updateProjectionMatrix();
      if (S.mode === "line") { var c = lineCam(S.lz); setCam(c.pos, c.look); viewShift(false); } else viewShift(true);
      ask();
    }
    var ro = window.ResizeObserver ? new ResizeObserver(size) : null; if (ro) ro.observe(box);
    var vis = function () { if (!document.hidden) ask(); }; document.addEventListener("visibilitychange", vis);
    setTheme(dark); applyLt(); ask();
    return {
      focus: focus, stop: function (k) { stop(k); }, next: next, back: back, jump: jump, theme: setTheme, size: size,
      state: function () { return { mode: S.mode, id: S.id, k: S.k, frames: frames }; },
      destroy: function () { alive = false; if (raf) cancelAnimationFrame(raf); if (ro) ro.disconnect(); document.removeEventListener("visibilitychange", vis); r.dispose(); comp.dispose && comp.dispose(); pm.dispose(); if (r.domElement.parentNode) r.domElement.parentNode.removeChild(r.domElement); if (tags.parentNode) tags.parentNode.removeChild(tags); try { r.forceContextLoss(); } catch (e) {} }
    };
  }
  window.gxLn3D = { mount: mount, ok: function () { try { var c = document.createElement("canvas"); return !!(c.getContext("webgl2") || c.getContext("webgl")); } catch (e) { return false; } } };
})();
