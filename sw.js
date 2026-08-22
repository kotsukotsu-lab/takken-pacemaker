/* オフラインで開けるようにするだけの最小構成。
   questions.js（手元専用）はキャッシュしない。 */
const CACHE = "takken-pacemaker-v3";
const ASSETS = ["./", "./index.html", "./data.js", "./manifest.webmanifest",
                "./icon-192.png", "./icon-512.png", "./icon-maskable-512.png",
                "./apple-touch-icon.png", "./favicon-32.png"];

self.addEventListener("install", e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(ASSETS)).then(() => self.skipWaiting()));
});

self.addEventListener("activate", e => {
  e.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", e => {
  const req = e.request;
  if (req.method !== "GET") return;
  if (req.url.includes("questions.js")) return;
  // まずネットワーク。落ちていたらキャッシュ（＝地下鉄でも開く）。
  e.respondWith(
    fetch(req)
      .then(res => {
        const copy = res.clone();
        caches.open(CACHE).then(c => c.put(req, copy)).catch(() => {});
        return res;
      })
      .catch(() => caches.match(req).then(r => r || caches.match("./index.html")))
  );
});
