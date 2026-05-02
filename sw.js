/* BrillianceLab service worker — offline-first for static, network-first for HTML */
const CACHE = 'bl-v6';
const PRECACHE = [
  '/',
  '/index.html',
  '/icon.svg',
  '/manifest.json',
  '/blog/',
  '/blog/feed.xml',
  '/blog/blog-shared.js',
  '/blog/gia-guide',
  '/blog/hearts-arrows-truth',
  '/blog/budget-formula',
  '/blog/lab-vs-natural',
  '/blog/engagement-guide',
  '/blog/diamond-news-2026'
];

self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(CACHE)
      .then((c) => Promise.allSettled(PRECACHE.map((u) => c.add(u))))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (e) => {
  const req = e.request;
  if (req.method !== 'GET') return;

  const url = new URL(req.url);
  // Bypass cross-origin (Tailwind CDN, Google Fonts, AdSense, Clarity, jsPDF, html2canvas, etc.)
  if (url.origin !== location.origin) return;
  // Bypass server-side function endpoints
  if (url.pathname.startsWith('/api/')) return;

  // Network-first for navigation requests (HTML pages)
  if (req.mode === 'navigate' || req.headers.get('accept')?.includes('text/html')) {
    e.respondWith(
      fetch(req)
        .then((resp) => {
          const copy = resp.clone();
          caches.open(CACHE).then((c) => c.put(req, copy));
          return resp;
        })
        .catch(() => caches.match(req).then((r) => r || caches.match('/')))
    );
    return;
  }

  // Cache-first for static assets
  e.respondWith(
    caches.match(req).then((cached) => {
      if (cached) return cached;
      return fetch(req).then((resp) => {
        if (resp && resp.status === 200) {
          const copy = resp.clone();
          caches.open(CACHE).then((c) => c.put(req, copy));
        }
        return resp;
      }).catch(() => cached);
    })
  );
});
