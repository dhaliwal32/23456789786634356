/* sw.js - change 278: shows alerts sent to the home-screen app and opens the right page when one is tapped. It stores nothing and never touches how the app loads. */
self.addEventListener("install", function () { self.skipWaiting(); });
self.addEventListener("activate", function (e) { e.waitUntil(self.clients.claim()); });
self.addEventListener("push", function (e) {
  var d = {};
  try { d = e.data ? e.data.json() : {}; } catch (x) { d = { body: e.data ? e.data.text() : "" }; }
  e.waitUntil(self.registration.showNotification(d.title || "Fantasy GM", { body: d.body || "", icon: "icon.png", data: { url: d.url || "#matchup" } }));
});
self.addEventListener("notificationclick", function (e) {
  e.notification.close();
  var hash = (e.notification.data && e.notification.data.url) || "#matchup";
  e.waitUntil(self.clients.matchAll({ type: "window", includeUncontrolled: true }).then(function (list) {
    for (var i = 0; i < list.length; i++) {
      if (list[i].url.indexOf("fantasy-gm.html") >= 0) { list[i].postMessage({ gxGo278: hash }); return list[i].focus(); }
    }
    return self.clients.openWindow("fantasy-gm.html" + hash);
  }));
});
