// build_app.js - translates the app once on GitHub so phones can skip that step.
// The Install changes workflow runs it after install.py. If anything goes wrong here,
// the app keeps translating itself in the browser like before.
const fs = require("fs");
const B = require("/tmp/babel/node_modules/@babel/standalone");

const hash = (t) => { let h = 0x811c9dc5; for (let i = 0; i < t.length; i++) { h ^= t.charCodeAt(i); h = Math.imul(h, 0x01000193); } return (h >>> 0).toString(36); };
const OPEN = '<script type="text/babel">';
// change 168: a page older than this build reloads itself once (GitHub serves the newest build to every page)
const GUARD168 = (h) => '(function(){var p=window.__GX_PAGE;if(!p||p==="' + h + '")return;var k="gx168-reload";var s="";try{s=sessionStorage.getItem(k)||"";}catch(e){}if(s===p)return;try{sessionStorage.setItem(k,p);}catch(e){}location.replace(location.pathname+"?v="+Date.now()+location.hash);throw new Error("gx168: reloading a newer page");})();\n';
const META = /[ \t]*<meta name="gx-build"[^>]*>\n?/g;
const log = [];
const say = (x) => { console.log(x); log.push("- " + x.replace(/^\(build\) /, "")); };

// change 076: classic React output (Babel 8 would otherwise add imports a browser cannot load),
// and stop before writing anything if the output still needs imports, so the app keeps working.
const tr = (code, name, presets) => {
  const out = B.transform(code, { filename: name, presets: presets.map((p) => (p === "react" ? ["react", { runtime: "classic" }] : p)) }).code;
  if (/^\s*import\s|require\(["']react/m.test(out)) throw new Error(name + ": the build would need imports, so the old build was kept");
  return out;
};
// same settings the browser used, so the app behaves exactly as before
function trApp(code, name) {
  try { return tr(code, name, ["react"]); } // change 076: es2015 removed, it was dropping {...x, [k]: v}
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
  const app = "/* built from " + page + " - do not edit, run Install changes instead */\n" + GUARD168(hash(src)) + trApp(src, page);
  const ver = hash(parts["build/lines-tab.js"] + parts["build/ask-panel.js"] + app);
  const tag = '<meta name="gx-build" content="' + hash(src) + "." + ver + '" data-file="' + appOut + '">\n';
  html = html.replace(META, "").replace("</head>", tag + "</head>");
  write(appOut, app);
  const changed = write(page, html);
  say("(build) " + page + " -> " + appOut + (changed ? " (updated)" : " (no change)"));
}

buildPage("fantasy-gm.html", "build/app.js");
buildPage("fantasy-gm-test.html", "build/app-test.js");

// change 216: build the Tailwind styles once here, so phones don't build them on every open.
// If this fails, build/tw.css is removed and the page builds the styles itself like before.
const TWM216 = /[ \t]*<meta name="gx-tw"[^>]*>\n?/g;
function twPage216(page, h) {
  if (!fs.existsSync(page)) return;
  let html = fs.readFileSync(page, "utf8").replace(/\r\n/g, "\n").replace(TWM216, "");
  const at = html.indexOf("<script>/* gx216-tw");
  if (at < 0) return;
  if (h) html = html.slice(0, at) + '<meta name="gx-tw" content="' + h + '">\n' + html.slice(at);
  write(page, html);
}
let tw216 = "";
try {
  const files = ["fantasy-gm.html", "fantasy-gm-test.html", "build/app.js", "build/app-test.js", "build/lines-tab.js", "build/ask-panel.js"].filter((f) => fs.existsSync(f));
  require("child_process").execSync('npx --yes tailwindcss@3 --content "' + files.join(",") + '" -o build/tw-new.css --minify', { stdio: "pipe", timeout: 240000 });
  const css = fs.readFileSync("build/tw-new.css", "utf8");
  fs.unlinkSync("build/tw-new.css");
  if (css.length < 5000 || css.indexOf(".flex{") < 0) throw new Error("the styles came out incomplete");
  write("build/tw.css", css);
  tw216 = hash(css);
  say("(build) styles -> build/tw.css (" + Math.round(css.length / 1024) + " KB)");
} catch (e) {
  say("(build) styles not built, the page will build them itself: " + String((e && e.message) || e).slice(0, 200));
  try { fs.unlinkSync("build/tw.css"); } catch (x) {}
  try { fs.unlinkSync("build/tw-new.css"); } catch (x) {}
}
twPage216("fantasy-gm.html", tw216);
twPage216("fantasy-gm-test.html", tw216);

if (process.env.GITHUB_STEP_SUMMARY) fs.appendFileSync(process.env.GITHUB_STEP_SUMMARY, "\n### Fast app build\n" + log.join("\n") + "\n");
