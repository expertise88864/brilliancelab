/* BrillianceLab service worker — offline-first for static, network-first for HTML */
const CACHE = 'bl-v17';
// All entries MUST be canonical URLs (no trailing slashes on dirs because
// vercel.json sets trailingSlash:false — caching the slashed form would store
// the 308 redirect itself and break navigation).
const PRECACHE = [
  '/',
  '/index.html',
  '/icon.svg',
  '/manifest.json',
  '/blog',
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
  '/search',
  '/blog/diamond-photography',
  '/blog/dating-duration',
  '/blog/destination-wedding',
  '/blog/diamond-price-trends',
  '/blog/hub-fundamentals',
  '/blog/hub-4cs',
  '/blog/hub-purchase',
  '/blog/hub-proposal',
  '/blog/hub-care',
  '/amp/blog/master-guide',
  '/amp/blog/gia-guide',
  '/amp/blog/hearts-arrows-truth',
  '/amp/blog/budget-formula',
  '/amp/blog/lab-vs-natural',
  '/amp/blog/diamond-faq'
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
    e.respondWith((async () => {
      let cached = await caches.match(req);
      // Defensive: drop a cached opaque-redirect entry (left over from older SW
      // versions that stored the 308 produced by trailingSlash:false). Symptom
      // was ERR_FAILED on /blog/. Force a fresh network fetch instead.
      if (cached && (cached.type === 'opaqueredirect' || cached.redirected || cached.status === 0)) {
        try { const c = await caches.open(CACHE); await c.delete(req); } catch (_) {}
        cached = null;
      }
      const fetchPromise = fetch(req).then((resp) => {
        if (resp && resp.status === 200 && !resp.redirected) {
          const copy = resp.clone();
          caches.open(CACHE).then((c) => c.put(req, copy));
        }
        return resp;
      }).catch(() => cached || caches.match('/') || new Response('Offline', { status: 503 }));
      return cached || fetchPromise;
    })());
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
