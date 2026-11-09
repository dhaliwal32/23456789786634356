# changes/216-ready-made-styles.py - the app's look is built once on GitHub (build/tw.css) instead of on the phone every time it opens

OLD_TAG = '<script src="https://cdn.tailwindcss.com"></script>'
NEW_TAG = r'''<script>/* gx216-tw: use the styles built on GitHub; if they are missing, build them in the browser like before */(function () {
  var m = document.querySelector('meta[name="gx-tw"]'), v = m && m.getAttribute("content");
  if (!v || /[?&]tw\b/.test(location.search)) { document.write('<script src="https://cdn.tailwindcss.com"><\/script>'); return; }
  window.__gxTwFail216 = function () { if (window.__gxTw216) return; window.__gxTw216 = 1; var s = document.createElement("script"); s.src = "https://cdn.tailwindcss.com"; document.head.appendChild(s); };
  document.write('<link rel="stylesheet" href="build/tw.css?v=' + v + '" onerror="__gxTwFail216()">');
})();</script>'''

OLD_END = 'if (process.env.GITHUB_STEP_SUMMARY) fs.appendFileSync(process.env.GITHUB_STEP_SUMMARY, "\\n### Fast app build\\n" + log.join("\\n") + "\\n");'
NEW_END = r'''// change 216: build the Tailwind styles once here, so phones don't build them on every open.
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

if (process.env.GITHUB_STEP_SUMMARY) fs.appendFileSync(process.env.GITHUB_STEP_SUMMARY, "\n### Fast app build\n" + log.join("\n") + "\n");'''

def change(t):
    t = lit(t, "216: style tag", OLD_TAG, NEW_TAG, "gx216-tw: use the styles built on GitHub")
    return t

def change_build(t):
    t = lit(t, "216: build styles", OLD_END, NEW_END, "change 216: build the Tailwind styles once here")
    return t

edit(APP, change)
edit("build_app.js", change_build)
