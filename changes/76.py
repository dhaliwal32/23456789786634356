# changes/076-fix-fast-build.py - fixes the fast phone build: keeps {...x, [k]: v} intact and stays safe with Babel 8

OLD_TR = 'const tr = (code, name, presets) => B.transform(code, { filename: name, presets }).code;'
NEW_TR = '''// change 076: classic React output (Babel 8 would otherwise add imports a browser cannot load),
// and stop before writing anything if the output still needs imports, so the app keeps working.
const tr = (code, name, presets) => {
  const out = B.transform(code, { filename: name, presets: presets.map((p) => (p === "react" ? ["react", { runtime: "classic" }] : p)) }).code;
  if (/^\\s*import\\s|require\\(["']react/m.test(out)) throw new Error(name + ": the build would need imports, so the old build was kept");
  return out;
};'''

OLD_APP = '  try { return tr(code, name, ["react", "es2015"]); }'
NEW_APP = '  try { return tr(code, name, ["react"]); } // change 076: es2015 removed, it was dropping {...x, [k]: v}'


def change(t):
    t = lit(t, "076: classic React build with safety stop", OLD_TR, NEW_TR, "change 076: classic React output")
    t = lit(t, "076: drop the es2015 setting", OLD_APP, NEW_APP, "change 076: es2015 removed")
    return t


edit("build_app.js", change)
