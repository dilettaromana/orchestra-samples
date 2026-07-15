/*!
 * orchestra-sw.js — cache-first service worker per i campioni (uso kiosk/offline).
 *
 * Registrazione (dalla pagina):
 *   if ('serviceWorker' in navigator) {
 *     navigator.serviceWorker.register('sw/orchestra-sw.js', { scope: './' });
 *   }
 *
 * Strategia: i file audio (mp3/ogg/wav/flac) e i manifest vengono serviti dalla
 * cache se presenti, altrimenti scaricati e memorizzati. Cosi' il primo avvio con
 * rete popola la cache e gli avvii successivi funzionano offline.
 */
const CACHE = "orchestra-samples-v1";
const AUDIO_RE = /\.(ogg|mp3|wav|flac)$/i;
const MANIFEST_RE = /manifest(\.[a-z]+)?\.json$/i;

self.addEventListener("install", (e) => { self.skipWaiting(); });

self.addEventListener("activate", (e) => {
  e.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", (e) => {
  const url = e.request.url;
  if (!(AUDIO_RE.test(url) || MANIFEST_RE.test(url))) return; // lascia passare il resto
  e.respondWith(
    caches.open(CACHE).then((cache) =>
      cache.match(e.request).then((hit) => {
        if (hit) return hit;
        return fetch(e.request).then((resp) => {
          // memorizza solo risposte valide (anche opaque per CDN cross-origin)
          if (resp && (resp.ok || resp.type === "opaque")) {
            cache.put(e.request, resp.clone());
          }
          return resp;
        }).catch(() => hit); // offline e non in cache: fallisce come di norma
      })
    )
  );
});
