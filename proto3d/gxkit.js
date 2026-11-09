// gxkit.js - modular hockey character builder (prototype, not in the live app)
// One shared body + one of a few heads + everything else from code: jersey design, colours, name, number, skin, build, shooting side.
// Needs window.GX3D = { THREE, GLTFLoader, RoomEnvironment, DecalGeometry }.
window.GXKit = (function () {
  const G = () => window.GX3D, files = {};
  const load = (url) => (files[url] = files[url] || new Promise((ok, bad) => new (G().GLTFLoader)().load(url, (g) => ok(g), undefined, bad)));
  const meshOf = (g) => { let m = null; g.scene.updateMatrixWorld(true); g.scene.traverse((x) => { if (x.isMesh && !m) m = x; }); return m; };
  // copy of a cached mesh: shares geometry and textures, keeps the file's own placement and scale (needed for compressed files)
  const inst = (src, mat) => { const THREE = G().THREE, m = new THREE.Mesh(src.geometry, mat); m.matrixAutoUpdate = false; m.matrix.copy(src.matrixWorld); return m; };

  // team kits: colours and a jersey design; the design is drawn by code, not by separate models
  const KITS = {
    FLA: { base: "#C8102E", stripe: "#041E42", accent: "#B9975B", pants: "#041E42", helmet: "#C8102E", gloves: "#041E42", socks: "#C8102E", num: "#FFFFFF", numEdge: "#041E42", design: "hem3" },
    EDM: { base: "#041E42", stripe: "#FF4C00", accent: "#FFFFFF", pants: "#041E42", helmet: "#041E42", gloves: "#041E42", socks: "#041E42", num: "#FF4C00", numEdge: "#FFFFFF", design: "yoke" },
    TOR: { base: "#FFFFFF", stripe: "#00205B", accent: "#00205B", pants: "#00205B", helmet: "#00205B", gloves: "#00205B", socks: "#FFFFFF", num: "#00205B", numEdge: "#FFFFFF", design: "plain" },
  };
  // heads: which donor head, and how its helmet is coloured
  const HEADS = { A: { file: "head_A.glb", helmet: "white" }, B: { file: "head_B.glb", helmet: "white" }, C: { file: "head_C.glb", helmet: "dark" }, D: { file: "head_D.glb", helmet: "white" } };
  // body builds: width/depth and height multipliers
  const BUILDS = { lean: [0.94, 1.03], avg: [1, 1], big: [1.08, 1.0] };

  const C3 = (h) => new (G().THREE).Color(h);
  // body shader: the white Meshy body becomes the team jersey, design drawn in model space
  function bodyMat(src, kit) {
    const THREE = G().THREE, m = src.clone();
    const D = { plain: 0, hem3: 1, yoke: 2 }[kit.design] || 0;
    const u = { uBase: { value: C3(kit.base) }, uStripe: { value: C3(kit.stripe) }, uAccent: { value: C3(kit.accent) }, uPants: { value: C3(kit.pants) }, uGloves: { value: C3(kit.gloves) }, uSocks: { value: C3(kit.socks) }, uDesign: { value: D }, uFile: { value: new THREE.Matrix4() } };
    m.userData.u = u;
    m.onBeforeCompile = (sh) => {
      Object.assign(sh.uniforms, u);
      sh.uniforms.uFile = u.uFile; sh.vertexShader = sh.vertexShader.replace("#include <common>", "#include <common>\nvarying vec3 vK; uniform mat4 uFile;").replace("#include <begin_vertex>", "#include <begin_vertex>\nvK = (uFile * vec4(position, 1.0)).xyz;");
      sh.fragmentShader = sh.fragmentShader.replace("#include <common>", `#include <common>
varying vec3 vK; uniform vec3 uBase, uStripe, uAccent, uPants, uGloves, uSocks; uniform float uDesign;
vec3 kitTint(vec3 c) {
  float mx = max(c.r, max(c.g, c.b)), mn = min(c.r, min(c.g, c.b)), L = dot(c, vec3(.299, .587, .114)), S = mx > 0.0 ? (mx - mn) / mx : 0.0;
  vec3 p = vK;                                                        // feet at y = 0, height 1.9, facing +z
  if (p.y < 0.17) return c;                                           // skates
  if (S > 0.16 && c.r > c.b * 1.08) return c;                         // skin
  if (L < 0.2) return c;                                              // stick, laces
  bool white = L > 0.66;
  float kw = pow(clamp(L / 0.9, 0.0, 1.0), 1.4), kg = pow(clamp(L / 0.62, 0.0, 1.0), 1.15);
  bool gloves = (p.y > 1.38 && p.y < 1.66 && p.x < -0.25) || (p.y > 0.82 && p.y < 1.14 && p.x > 0.27);
  if (gloves) return uGloves * (white ? kw : kg);
  bool pants = p.y > 0.66 && p.y < 0.98 && abs(p.x) < 0.27;
  if (pants) return uPants * kg;
  if (p.y < 0.66) return (white ? uSocks : uStripe) * (white ? kw : kg);  // socks with stripes
  // jersey
  vec3 col = white ? uBase : uStripe; float k = white ? kw : kg;
  if (uDesign > 1.5 && p.y > 1.47 && abs(p.x) < 0.33) { col = white ? uStripe : uAccent; }               // yoke over the shoulders
  if (uDesign > 0.5 && uDesign < 1.5 && p.y > 0.985 && p.y < 1.09 && abs(p.x) < 0.33) {                   // three-colour hem stripes
    float b = fract((p.y - 0.985) / 0.035); col = b < 0.33 ? uStripe : b < 0.66 ? uAccent : uStripe; k = kw;
  }
  return col * k;
}`).replace("#include <map_fragment>", "#include <map_fragment>\ndiffuseColor.rgb = kitTint(diffuseColor.rgb);");
    };
    m.customProgramCacheKey = () => "gxkit-body";
    return m;
  }
  // head shader: helmet takes the team colour, skin can be shifted lighter or darker
  function headMat(src, kit, head, skin) {
    const THREE = G().THREE, m = src.clone(); m.metalness = 0; m.metalnessMap = null; m.roughness = 1;
    const u = { uHelm: { value: C3(kit.helmet) }, uSkin: { value: skin || 0 }, uDark: { value: head.helmet === "dark" ? 1 : 0 } };
    m.onBeforeCompile = (sh) => {
      Object.assign(sh.uniforms, u);
      sh.fragmentShader = sh.fragmentShader.replace("#include <common>", `#include <common>
uniform vec3 uHelm; uniform float uSkin, uDark;
vec3 headTint(vec3 c) {
  float mx = max(c.r, max(c.g, c.b)), mn = min(c.r, min(c.g, c.b)), L = dot(c, vec3(.299, .587, .114)), S = mx > 0.0 ? (mx - mn) / mx : 0.0;
  bool skinPx = S > 0.16 && c.r > c.b * 1.08;
  if (skinPx) return uSkin == 0.0 ? c : (uSkin > 0.0 ? mix(c, c * vec3(0.55, 0.42, 0.34), uSkin) : mix(c, min(c * 1.25, vec3(1.0)), -uSkin));
  if (uDark < 0.5 && L > 0.6) return uHelm * pow(clamp(L / 0.9, 0.0, 1.0), 1.3);
  if (uDark > 0.5 && L < 0.25 && S < 0.25) return uHelm * (0.35 + L * 2.0);
  return c;
}`).replace("#include <map_fragment>", "#include <map_fragment>\ndiffuseColor.rgb = headTint(diffuseColor.rgb);");
    };
    m.customProgramCacheKey = () => "gxkit-head";
    return m;
  }
  function backText(p, kit) {
    const THREE = G().THREE, c = document.createElement("canvas"); c.width = 512; c.height = 512; const g = c.getContext("2d");
    g.textAlign = "center"; g.textBaseline = "middle"; g.lineJoin = "round"; g.fillStyle = kit.num; g.strokeStyle = kit.numEdge;
    g.font = "900 62px Arial Black, Arial, sans-serif"; g.lineWidth = 9; if (kit.design === "yoke") { g.fillStyle = kit.base; g.strokeStyle = kit.accent; } g.save(); g.translate(256, 64); const w = g.measureText(p.name).width; if (w > 470) g.scale(470 / w, 1); g.strokeText(p.name, 0, 0); g.fillText(p.name, 0, 0); g.restore();
    g.fillStyle = kit.num; g.strokeStyle = kit.numEdge; g.font = "900 270px Arial Black, Arial, sans-serif"; g.lineWidth = 16; g.strokeText(p.no, 256, 300); g.fillText(p.no, 256, 300);
    const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 4; return t;
  }
  function crestText(kit, code) {
    const THREE = G().THREE, c = document.createElement("canvas"); c.width = 256; c.height = 256; const g = c.getContext("2d");
    g.beginPath(); g.arc(128, 128, 112, 0, Math.PI * 2); g.fillStyle = kit.stripe; g.fill(); g.lineWidth = 10; g.strokeStyle = kit.numEdge === kit.stripe ? kit.num : kit.numEdge; g.stroke();
    g.fillStyle = kit.num === kit.stripe ? kit.base : kit.num; g.font = "900 74px Arial Black, Arial, sans-serif"; g.textAlign = "center"; g.textBaseline = "middle"; g.fillText(code, 128, 134);
    const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t;
  }
  function decal(target, root, at, dir, size, tex) {
    const THREE = G().THREE, rc = new THREE.Raycaster(at, dir), h = rc.intersectObject(target, false)[0]; if (!h) return null;
    const look = dir.clone().negate(), e = new THREE.Euler().setFromQuaternion(new THREE.Quaternion().setFromUnitVectors(new THREE.Vector3(0, 0, 1), look));
    if (Math.abs(look.z + 1) < 1e-3) e.set(0, Math.PI, 0);
    const dg = new (G().DecalGeometry)(target, h.point, e, size);
    const m = new THREE.MeshStandardMaterial({ map: tex, transparent: true, depthWrite: false, polygonOffset: true, polygonOffsetFactor: -4, roughness: 0.8, side: THREE.DoubleSide });
    const d = new THREE.Mesh(dg, m); root.add(d); return d;
  }

  // build one character from player details; base = folder with body/head files; lod = "hi" | "low"
  async function build(p, base, lod) {
    const THREE = G().THREE, kit = KITS[p.team], head = HEADS[p.head] || HEADS.A, meta = await (files[base + "meta"] = files[base + "meta"] || fetch(base + "meta.json").then((r) => r.json()));
    const [gb, gh] = await Promise.all([load(base + (lod === "low" ? "body_standing_low.glb" : "body_standing_hi.glb")), load(base + (lod === "low" ? head.file.replace(".glb", "_low.glb") : head.file))]);
    const root = new THREE.Group(); root.name = p.name;
    const [bw, bh] = BUILDS[p.build] || BUILDS.avg;
    // body: shared geometry and texture, own team material; left shot = mirrored so the stick changes hands
    const bm = meshOf(gb), body = inst(bm, bodyMat(bm.material, kit));
    body.material.userData.u.uFile.value.copy(bm.matrixWorld);
    const bodyG = new THREE.Group(); bodyG.add(body); bodyG.scale.set(bw * (p.shoots === "R" ? -1 : 1), bh, bw); root.add(bodyG); root.updateMatrixWorld(true);
    // head: shared geometry and texture, placed on the neck of this body
    const hm = meshOf(gh), H = meta[p.head].head, A0 = meta.A.head; // the Standing model's own neck is where every head goes
    const hd = new THREE.Group(); hd.add(inst(hm, headMat(hm.material, kit, head, p.skin)));
    const hs = Math.min(1.15, Math.max(0.85, (A0.top - A0.ring.y) / (H.top - H.ring.y)));
    hd.scale.setScalar(hs);
    hd.position.set(-H.ring.x * hs + A0.ring.x * bw * (p.shoots === "R" ? -1 : 1), A0.ring.y * bh - H.ring.y * hs - 0.012, -H.ring.z * hs + A0.ring.z * bw);
    root.add(hd);
    // name and number on the back, crest on the front; numbers on the arms for the inspect view
    root.updateMatrixWorld(true);
    const V = (x, y, z) => new THREE.Vector3(x, y, z);
    decal(body, root, V(0, 1.31 * bh, -2), V(0, 0, 1), V(0.46 * bw, 0.46 * bw, 0.12), backText(p, kit));
    decal(body, root, V(0, 1.25 * bh, 2), V(0, 0, -1), V(0.22 * bw, 0.22 * bw, 0.12), crestText(kit, p.team));
    root.userData.parts = { body, head: hd };
    return root;
  }
  // free per-character materials and decal geometry; shared geometry and textures stay cached
  function dispose(root) { root.traverse((x) => { if (!x.isMesh) return; if (x.material) { if (x.material.map && x.material.map.isCanvasTexture) x.material.map.dispose(); x.material.dispose(); } if (x.geometry && x.geometry.type === "DecalGeometry") x.geometry.dispose(); }); }
  return { KITS, HEADS, BUILDS, build, dispose };
})();
