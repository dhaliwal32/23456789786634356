// build_app.js - translates the app once on GitHub so phones can skip that step.
// The Install changes workflow runs it after install.py. If anything goes wrong here,
// the app keeps translating itself in the browser like before.
const fs = require("fs");
const B = require("/tmp/babel/node_modules/@babel/standalone");

const hash = (t) => { let h = 0x811c9dc5; for (let i = 0; i < t.length; i++) { h ^= t.charCodeAt(i); h = Math.imul(h, 0x01000193); } return (h >>> 0).toString(36); };
const OPEN = '<script type="text/babel">';
const META = /[ \t]*<meta name="gx-build"[^>]*>\n?/g;
const log = [];
const say = (x) => { console.log(x); log.push("- " + x.replace(/^\(build\) /, "")); };

const tr = (code, name, presets) => B.transform(code, { filename: name, presets }).code;
// same settings the browser used, so the app behaves exactly as before
function trApp(code, name) {
  try { return tr(code, name, ["react", "es2015"]); }
  catch (e) {
    if (!/preset|es2015/i.test(String(e.message))) throw e;
    say("(build) es2015 setting not available, using react only");
    return tr(code, name, ["react"]);
  }
}
function write(file, text) {
  if (fs.existsSync(file) && fs.readFileSync(file, "utf8") === text) return false;
  fs.writeFileSync(file, text);
  return true;
}

fs.mkdirSync("build", { recursive: true });
const parts = {};
for (const [src, out] of [["lines-tab.js", "build/lines-tab.js"], ["ask-panel.js", "build/ask-panel.js"]]) {
  parts[out] = "/* built from " + src + " - do not edit */\n" + tr(fs.readFileSync(src, "utf8"), src, ["react"]);
  write(out, parts[out]);
}

function buildPage(page, appOut) {
  if (!fs.existsSync(page)) return;
  let html = fs.readFileSync(page, "utf8").replace(/\r\n/g, "\n");
  if (html.indexOf("gx074-loader") < 0) { say("(build) " + page + ": loader not installed yet, skipped"); return; }
  const a = html.indexOf(OPEN);
  if (a < 0) { say("(build) " + page + ": no app code found, skipped"); return; }
  const b = html.indexOf("</script>", a);
  const src = html.slice(a + OPEN.length, b);
  const app = "/* built from " + page + " - do not edit, run Install changes instead */\n" + trApp(src, page);
  const ver = hash(parts["build/lines-tab.js"] + parts["build/ask-panel.js"] + app);
  const tag = '<meta name="gx-build" content="' + hash(src) + "." + ver + '" data-file="' + appOut + '">\n';
  html = html.replace(META, "").replace("</head>", tag + "</head>");
  write(appOut, app);
  const changed = write(page, html);
  say("(build) " + page + " -> " + appOut + (changed ? " (updated)" : " (no change)"));
}

buildPage("fantasy-gm.html", "build/app.js");
buildPage("fantasy-gm-test.html", "build/app-test.js");

if (process.env.GITHUB_STEP_SUMMARY) fs.appendFileSync(process.env.GITHUB_STEP_SUMMARY, "\n### Fast app build\n" + log.join("\n") + "\n");
