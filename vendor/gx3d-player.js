// Shared 3D player viewer (used by the test page now, and copied into the app change).
// Needs window.GX3D = { THREE, GLTFLoader, RoomEnvironment, DecalGeometry }.
window.gxPl3D = (function () {
  const cache = {};
  function loadModel(url) {
    if (!cache[url]) cache[url] = new Promise((ok, bad) => new window.GX3D.GLTFLoader().load(url, ok, undefined, bad));
    return cache[url];
  }
  // white parts -> team body colour, grey parts -> trim (pants -> pants colour), skin and black stay
  function teamMat(base, c, THREE) {
    const m = base.clone();
    const u = { uBody: { value: new THREE.Color(c.body) }, uTrim: { value: new THREE.Color(c.trim) }, uPants: { value: new THREE.Color(c.pants) }, uHelm: { value: new THREE.Color(c.helmet) }, uGlove: { value: new THREE.Color(c.glove) } };
    m.onBeforeCompile = (sh) => {
      Object.assign(sh.uniforms, u);
      sh.vertexShader = sh.vertexShader.replace("#include <common>", "#include <common>\nvarying vec3 vLoc;").replace("#include <begin_vertex>", "#include <begin_vertex>\nvLoc = position;");
      sh.fragmentShader = sh.fragmentShader.replace("#include <common>", `#include <common>
varying vec3 vLoc; uniform vec3 uBody, uTrim, uPants, uHelm, uGlove;
vec3 gxTint(vec3 c) {
  float mx = max(c.r, max(c.g, c.b)), mn = min(c.r, min(c.g, c.b)), L = dot(c, vec3(.299, .587, .114)), S = mx > 0.0 ? (mx - mn) / mx : 0.0;
  vec3 p = vLoc;
  if (p.y < -0.72) return c;                                  // skates
  if (S > 0.16 && c.r > c.b * 1.08) return c;                 // skin
  if (L < 0.2) return c;                                      // black: stick, laces, visor edge
  bool head = p.y > 0.66, gloves = (p.y > 0.42 && p.y < 0.70 && p.x < -0.25) || (p.y > -0.12 && p.y < 0.2 && p.x > 0.27);
  bool pants = p.y > -0.30 && p.y < 0.03 && abs(p.x) < 0.27;
  float kw = pow(clamp(L / 0.9, 0.0, 1.0), 1.4), kg = pow(clamp(L / 0.62, 0.0, 1.0), 1.15);
  if (head) return uHelm * kw;
  if (gloves) return (L > 0.66 ? uGlove : uTrim) * (L > 0.66 ? kw : kg);
  if (pants) return uPants * kg;
  return L > 0.66 ? uBody * kw : uTrim * kg;
}`).replace("#include <map_fragment>", "#include <map_fragment>\ndiffuseColor.rgb = gxTint(diffuseColor.rgb);");
    };
    m.customProgramCacheKey = () => "gx225tint";
    return m;
  }
  function backTex(o0, THREE) { const o = Object.assign({}, o0, o0.colors);
    const c = document.createElement("canvas"); c.width = 512; c.height = 512; const g = c.getContext("2d");
    g.textAlign = "center"; g.textBaseline = "middle"; g.lineJoin = "round";
    const st = o.trim.toLowerCase() === o.num.toLowerCase() ? "rgba(0,0,0,.45)" : o.trim;
    g.fillStyle = o.num; g.strokeStyle = st;
    if (o.name) { g.font = "900 64px Arial Black, Arial, sans-serif"; g.lineWidth = 9; g.save(); g.translate(256, 64); const w = g.measureText(o.name).width; if (w > 470) g.scale(470 / w, 1); g.strokeText(o.name, 0, 0); g.fillText(o.name, 0, 0); g.restore(); }
    if (o.no) { g.font = "900 270px Arial Black, Arial, sans-serif"; g.lineWidth = 16; g.strokeText(o.no, 256, 300); g.fillText(o.no, 256, 300); }
    const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 4; return t;
  }
  // mount a viewer in el; returns { dispose }
  function mount(el, o) {
    const G = window.GX3D, THREE = G.THREE, light = o.light;
    const W = el.clientWidth || 300, H = el.clientHeight || 300;
    const r = new THREE.WebGLRenderer({ antialias: true, alpha: true, preserveDrawingBuffer: !!o.keep });
    r.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2)); r.setSize(W, H); r.outputColorSpace = THREE.SRGBColorSpace;
    r.toneMapping = THREE.ACESFilmicToneMapping; r.toneMappingExposure = light ? 1.0 : 0.95;
    el.appendChild(r.domElement); r.domElement.style.touchAction = "pan-y"; r.domElement.style.display = "block";
    const sc = new THREE.Scene(), pm = new THREE.PMREMGenerator(r), envT = pm.fromScene(new G.RoomEnvironment(), 0.04).texture; sc.environment = envT; pm.dispose();
    sc.add(new THREE.HemisphereLight(0xffffff, light ? 0xc0c8d2 : 0x202430, light ? 0.8 : 0.5));
    const key = new THREE.DirectionalLight(0xffffff, light ? 2.0 : 2.3); key.position.set(2.5, 5, 4); sc.add(key);
    const rim = new THREE.DirectionalLight(light ? 0xffffff : 0x9ec3ff, light ? 0.6 : 1.5); rim.position.set(-4, 3, -5); sc.add(rim);
    const cam = new THREE.PerspectiveCamera(28, W / H, 0.05, 50);
    const spin = new THREE.Group(); sc.add(spin);
    let ang = o.start != null ? o.start : Math.PI, vel = 0, raf = 0, dead = false, made = [];
    const draw = () => { spin.rotation.y = ang; r.render(sc, cam); };
    const tick = () => { raf = 0; if (dead) return; if (!drag && Math.abs(vel) > 0.0004) { ang += vel; vel *= 0.92; draw(); raf = requestAnimationFrame(tick); } else draw(); };
    let drag = null;
    const cv = r.domElement;
    const pd = (e) => { e.stopPropagation(); drag = { x: e.clientX, a: ang, t: performance.now(), lx: e.clientX }; vel = 0; try { cv.setPointerCapture(e.pointerId); } catch (x) {} };
    const pmv = (e) => { if (!drag) return; e.stopPropagation(); const now = performance.now(); ang = drag.a + (e.clientX - drag.x) * 0.011; vel = (e.clientX - drag.lx) * 0.011 * Math.min(1, 16 / Math.max(1, now - drag.t)); drag.lx = e.clientX; drag.t = now; if (!raf) raf = requestAnimationFrame(() => { raf = 0; draw(); }); };
    const pu = (e) => { if (!drag) return; drag = null; if (o.reduced) vel = 0; if (!raf) raf = requestAnimationFrame(tick); };
    cv.addEventListener("pointerdown", pd); cv.addEventListener("pointermove", pmv); cv.addEventListener("pointerup", pu); cv.addEventListener("pointercancel", pu);
    const ro = new ResizeObserver(() => { const w = el.clientWidth, h = el.clientHeight; if (!w || !h) return; r.setSize(w, h); cam.aspect = w / h; cam.updateProjectionMatrix(); draw(); }); ro.observe(el);
    const t0 = performance.now();
    const ready = loadModel(o.url).then((gl) => {
      if (dead) return;
      const m = gl.scene.clone(true);
      let mesh = null; m.traverse((x) => { if (x.isMesh) { mesh = x; x.material = teamMat(x.material, o.colors, THREE); made.push(x.material); } });
      const box = new THREE.Box3().setFromObject(m), c = box.getCenter(new THREE.Vector3()), s = box.getSize(new THREE.Vector3());
      spin.rotation.y = 0; m.position.set(-c.x, -box.min.y, -c.z); spin.add(m); spin.updateMatrixWorld(true);
      // name and number on the back, worked out from the surface
      if (mesh && G.DecalGeometry && (o.name || o.no)) {
        const rc = new THREE.Raycaster(new THREE.Vector3(0, s.y * 0.69, -2), new THREE.Vector3(0, 0, 1)), h = rc.intersectObject(mesh, false)[0];
        if (h) {
          const dg = new G.DecalGeometry(mesh, h.point, new THREE.Euler(0, Math.PI, 0), new THREE.Vector3(s.x * 0.5, s.x * 0.5, 0.25));
          const dm = new THREE.MeshStandardMaterial({ map: backTex(o, THREE), transparent: true, depthWrite: false, polygonOffset: true, polygonOffsetFactor: -4, roughness: 0.8 });
          const d = new THREE.Mesh(dg, dm); spin.add(d); made.push(dm, dm.map); dg.userData.own = true; made.push(dg);
          // decal was built in world space; keep it with the model when the group turns
        }
      }
      const fov = cam.fov * Math.PI / 180, dist = (s.y * 0.6) / Math.tan(fov / 2) + s.z;
      cam.position.set(0, s.y * 0.52, dist); cam.lookAt(0, s.y * 0.49, 0); cam.updateProjectionMatrix();
      draw();
      return { ms: Math.round(performance.now() - t0), tris: mesh ? mesh.geometry.index.count / 3 : 0 };
    });
    return {
      ready,
      setAngle: (a) => { ang = a; draw(); },
      dispose: () => {
        dead = true; if (raf) cancelAnimationFrame(raf); ro.disconnect();
        cv.removeEventListener("pointerdown", pd); cv.removeEventListener("pointermove", pmv); cv.removeEventListener("pointerup", pu); cv.removeEventListener("pointercancel", pu);
        made.forEach((x) => x && x.dispose && x.dispose()); envT.dispose(); r.dispose(); try { r.forceContextLoss(); } catch (x) {} cv.remove();
      },
    };
  }
  return { mount, loadModel };
})();
