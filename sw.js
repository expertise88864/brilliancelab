/* BrillianceLab service worker — offline-first for static, network-first for HTML */
const CACHE = 'bl-v13';
const PRECACHE = [
  '/',
  '/index.html',
  '/icon.svg',
  '/manifest.json',
  '/blog/',
  '/blog/feed.xml',
  '/blog/blog-shared.js',
  '/blog/master-guide',
  '/blog/gia-guide',
  '/blog/hearts-arrows-truth',
  '/blog/budget-formula',
  '/blog/lab-vs-natural',
  '/blog/engagement-guide',
  '/blog/diamond-news-2026',
  '/blog/cert-comparison',
  '/blog/diamond-scams',
  '/blog/diamond-shapes',
  '/blog/diamond-care',
  '/blog/diamond-resale',
  '/blog/diamond-color',
  '/blog/diamond-clarity',
  '/blog/diamond-carat-size',
  '/blog/mens-engagement-rings',
  '/blog/proposal-speech',
  '/blog/wedding-bands',
  '/blog/wedding-metals',
  '/blog/ring-sizing',
  '/blog/diamond-fun-facts',
  '/blog/diamond-financing',
  '/blog/secondhand-rings',
  '/blog/ring-insurance',
  '/blog/diamond-faq',
  '/blog/round-cut-deep-dive',
  '/blog/fancy-cuts-guide',
  '/blog/prong-settings-guide',
  '/blog/fluorescence-deep-dive',
  '/blog/inclusions-types-guide',
  '/blog/engraving-personalization',
  '/blog/moissanite-vs-cz-vs-lab',
  '/blog/famous-diamonds',
  '/blog/engagement-timeline',
  '/blog/topics',
  '/blog/gemstones-comparison',
  '/blog/sustainable-diamonds',
  '/blog/heirloom-redesign',
  '/blog/diamond-vs-gold',
  '/blog/lgbtq-rings',
  '/search'
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

  // STALE-WHILE-REVALIDATE for HTML pages: serve cache immediately, update in background.
  // User gets instant page; next visit gets fresh content. Best of both worlds.
  if (req.mode === 'navigate' || req.headers.get('accept')?.includes('text/html')) {
    e.respondWith(
      caches.match(req).then((cached) => {
        const fetchPromise = fetch(req).then((resp) => {
          if (resp && resp.status === 200) {
            const copy = resp.clone();
            caches.open(CACHE).then((c) => c.put(req, copy));
          }
          return resp;
        }).catch(() => cached || caches.match('/'));
        // Return cached immediately if present, otherwise wait for network.
        return cached || fetchPromise;
      })
    );
    return;
  }

  // STALE-WHILE-REVALIDATE for static assets too — serve cache, refresh in background.
  e.respondWith(
    caches.match(req).then((cached) => {
      const fetchPromise = fetch(req).then((resp) => {
        if (resp && resp.status === 200) {
          const copy = resp.clone();
          caches.open(CACHE).then((c) => c.put(req, copy));
        }
        return resp;
      }).catch(() => cached);
      return cached || fetchPromise;
    })
  );
});
