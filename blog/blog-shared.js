/* ============================================================
 * BrillianceLab — shared blog runtime
 * Centralises:
 *   - language detection (cookie > localStorage > navigator > en)
 *   - 10-language dropdown injected over the existing toggle
 *   - reading progress bar + reading-time pill (estimate + remaining)
 *   - scroll-to-top button
 *   - footer year + service worker registration
 *   - Web Vitals (LCP / INP / CLS / FCP / TTFB) → GA4 gtag('event','web_vitals')
 *   - Giscus comments lazy-loader (opt-in via opts.comments)
 *   - Related-articles cross-link injector (43-article topic graph)
 *   - ARIA hardening on injected widgets
 * Each blog page only needs:
 *   <script src="/blog/blog-shared.js" defer></script>
 *   <script>BL.initBlog({ slug:'gia-guide', proseZh:'proseZh', proseEn:'proseEn', comments:true });</script>
 * ============================================================ */
(function () {
  const BL = (window.BL = window.BL || {});

  BL.LANGS = [
    { code: 'zh',    label: '中文(繁體)',  htmlLang: 'zh-TW' },
    { code: 'zh-cn', label: '简体中文',       htmlLang: 'zh-CN' },
    { code: 'en',    label: 'English',         htmlLang: 'en'    },
    { code: 'ja',    label: '日本語',          htmlLang: 'ja'    },
    { code: 'ko',    label: '한국어',          htmlLang: 'ko'    },
    { code: 'th',    label: 'ภาษาไทย',         htmlLang: 'th'    },
    { code: 'vi',    label: 'Tiếng Việt',      htmlLang: 'vi'    },
    { code: 'de',    label: 'Deutsch',         htmlLang: 'de'    },
    { code: 'fr',    label: 'Français',        htmlLang: 'fr'    },
    { code: 'es',    label: 'Español',         htmlLang: 'es'    }
  ];
  BL.LANG_KEY = {
    'zh':'zh', 'zh-cn':'zhcn', 'en':'en', 'ja':'ja', 'ko':'ko',
    'th':'th', 'vi':'vi', 'de':'de', 'fr':'fr', 'es':'es'
  };

  /* ---------- cookie helpers ---------- */
  BL.cookieGet = function (name) {
    const found = document.cookie.split('; ').find(c => c.startsWith(name + '='));
    return found ? decodeURIComponent(found.split('=').slice(1).join('=')) : null;
  };
  BL.cookieSet = function (name, val, days) {
    const exp = new Date(Date.now() + (days || 365) * 86400e3).toUTCString();
    document.cookie = `${name}=${encodeURIComponent(val)}; expires=${exp}; path=/; SameSite=Lax`;
  };

  /* ---------- language detection ---------- */
  BL.detectLang = function () {
    const fromCookie = BL.cookieGet('bl_lang');
    if (fromCookie && BL.LANG_KEY[fromCookie]) return fromCookie;
    const stored = localStorage.getItem('bl_lang');
    if (stored && BL.LANG_KEY[stored]) return stored;
    const nav = (navigator.language || 'en').toLowerCase();
    if (nav.startsWith('zh-cn') || nav.startsWith('zh-hans')) return 'zh-cn';
    if (nav.startsWith('zh')) return 'zh';
    if (nav.startsWith('ja')) return 'ja';
    if (nav.startsWith('ko')) return 'ko';
    if (nav.startsWith('th')) return 'th';
    if (nav.startsWith('vi')) return 'vi';
    if (nav.startsWith('de')) return 'de';
    if (nav.startsWith('fr')) return 'fr';
    if (nav.startsWith('es')) return 'es';
    return 'en';
  };

  BL.setLang = function (code) {
    if (!BL.LANG_KEY[code]) return;
    try { localStorage.setItem('bl_lang', code); } catch (e) { /* private mode */ }
    BL.cookieSet('bl_lang', code);
  };

  /* ---------- per-element translation with fallback ---------- */
  BL.translate = function (el, lang) {
    // For zh / zh-cn, prefer the matching variant first; for everything else,
    // try the exact language → English → Traditional Chinese.
    const order = lang === 'zh-cn' ? ['zhcn', 'zh', 'en']
                : lang === 'zh'    ? ['zh', 'zhcn', 'en']
                : [BL.LANG_KEY[lang], 'en', 'zh'];
    for (const k of order) if (k && el.dataset[k] != null) return el.dataset[k];
    return null;
  };

  BL.applyTextOnly = function (lang) {
    const meta = BL.LANGS.find(l => l.code === lang) || BL.LANGS[2];
    document.documentElement.lang = meta.htmlLang;
    document.querySelectorAll('[data-zh],[data-en]').forEach(el => {
      const txt = BL.translate(el, lang);
      if (txt == null) return;
      if (/[<&]/.test(txt) && /<\/?[a-z]/i.test(txt)) el.innerHTML = txt;
      else el.textContent = txt;
    });
  };

  /* ---------- 10-language dropdown (replaces #langToggle) ---------- */
  BL.injectLangDropdown = function (onChange) {
    const old = document.getElementById('langToggle');
    if (!old) return;
    const wrap = document.createElement('div');
    wrap.className = 'relative';
    wrap.id = 'blLangWrap';
    wrap.innerHTML = `
      <button id="blLangTrigger" type="button"
        class="lang-toggle inline-flex items-center gap-1.5 px-3 py-1.5 text-[12px] font-semibold cursor-pointer hover:border-gold-300"
        aria-haspopup="listbox" aria-expanded="false">
        <svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a13 13 0 0 1 0 18M12 3a13 13 0 0 0 0 18"/></svg>
        <span id="blLangLabel">中文</span>
        <span style="color:#a4a6b6">▾</span>
      </button>
      <div id="blLangMenu" class="hidden absolute right-0 top-full mt-2 card p-1.5 z-50 min-w-[180px] max-h-[60vh] overflow-y-auto" role="listbox"></div>
    `;
    old.parentNode.replaceChild(wrap, old);

    const trig = wrap.querySelector('#blLangTrigger');
    const menu = wrap.querySelector('#blLangMenu');
    const lbl  = wrap.querySelector('#blLangLabel');
    function rebuild(curLang) {
      const meta = BL.LANGS.find(l => l.code === curLang) || BL.LANGS[2];
      lbl.textContent = meta.label;
      menu.innerHTML = '';
      BL.LANGS.forEach(L => {
        const item = document.createElement('button');
        item.type = 'button';
        item.className = 'block w-full text-left px-3 py-1.5 rounded-md text-[12.5px] hover:bg-[var(--gold-soft)]'
                       + (curLang === L.code ? ' text-gold-700 font-semibold bg-[var(--gold-soft)]' : ' text-ink-700');
        item.textContent = L.label;
        item.addEventListener('click', () => {
          BL.setLang(L.code);
          menu.classList.add('hidden');
          rebuild(L.code);
          if (typeof onChange === 'function') onChange(L.code);
        });
        menu.appendChild(item);
      });
    }
    trig.addEventListener('click', () => {
      const open = menu.classList.contains('hidden');
      menu.classList.toggle('hidden');
      trig.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    document.addEventListener('click', (e) => {
      if (!wrap.contains(e.target)) menu.classList.add('hidden');
    });
    rebuild(BL.detectLang());
  };

  /* ---------- reading-progress bar + reading-time pill ---------- */
  BL.addReadingProgress = function () {
    if (document.getElementById('bl-progress')) return;
    const bar = document.createElement('div');
    bar.id = 'bl-progress';
    bar.setAttribute('role', 'progressbar');
    bar.setAttribute('aria-label', '閱讀進度 / Reading progress');
    bar.setAttribute('aria-valuemin', '0');
    bar.setAttribute('aria-valuemax', '100');
    bar.setAttribute('aria-valuenow', '0');
    bar.style.cssText = 'position:fixed;top:0;left:0;height:3px;background:linear-gradient(90deg,#d4b87a,#8a6e30);z-index:60;width:0;transition:width .12s linear;pointer-events:none';
    document.body.appendChild(bar);
    function update() {
      const h = document.documentElement;
      const max = h.scrollHeight - h.clientHeight;
      const pct = max > 0 ? Math.min(100, Math.max(0, (h.scrollTop / max) * 100)) : 0;
      bar.style.width = pct + '%';
      bar.setAttribute('aria-valuenow', String(Math.round(pct)));
      if (BL._readingPill) BL._readingPill.update(pct);
    }
    document.addEventListener('scroll', update, { passive: true });
    update();
  };

  /* ---------- reading-time pill (estimated total + remaining) ---------- */
  BL.addReadingTime = function () {
    if (document.getElementById('bl-rtime')) return;
    // Pick the visible article container — prefer #proseZh / #proseEn, fall back to <article>
    const candidates = ['#proseZh', '#proseEn', 'article', 'main'];
    let root = null;
    for (const sel of candidates) {
      const el = document.querySelector(sel);
      if (el && el.offsetParent !== null) { root = el; break; }
    }
    if (!root) root = document.querySelector('article') || document.body;

    const text = (root.innerText || root.textContent || '').trim();
    // Mixed CJK + Latin: count CJK chars (1 char ≈ 1 word at ~300 cpm) + Latin words (~220 wpm)
    const cjk = (text.match(/[㐀-鿿豈-﫿]/g) || []).length;
    const latin = (text.replace(/[㐀-鿿豈-﫿]/g, ' ').match(/\b[\w'-]+\b/g) || []).length;
    const totalMin = Math.max(1, Math.round(cjk / 350 + latin / 220));

    const pill = document.createElement('div');
    pill.id = 'bl-rtime';
    pill.setAttribute('role', 'status');
    pill.setAttribute('aria-live', 'polite');
    pill.setAttribute('aria-label', '估計閱讀時間');
    pill.style.cssText = 'position:fixed;left:14px;bottom:24px;padding:7px 13px;border-radius:9999px;background:rgba(255,253,247,.92);backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px);border:1px solid rgba(201,164,92,.45);color:#5e4a1f;font-size:11.5px;font-weight:600;letter-spacing:.04em;box-shadow:0 6px 18px -10px rgba(138,110,48,.5);z-index:50;display:flex;align-items:center;gap:6px;font-family:Inter,"Microsoft JhengHei",sans-serif;transition:opacity .25s';
    pill.innerHTML = '<svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg><span id="bl-rtime-text">約 ' + totalMin + ' 分鐘</span>';
    document.body.appendChild(pill);

    const txtEl = pill.querySelector('#bl-rtime-text');
    BL._readingPill = {
      update(pct) {
        if (pct < 1) { txtEl.textContent = '約 ' + totalMin + ' 分鐘'; return; }
        if (pct >= 99) { txtEl.textContent = '✓ 完讀'; pill.style.background = 'rgba(251,243,223,.95)'; return; }
        const remain = Math.max(0, Math.round(totalMin * (1 - pct / 100)));
        txtEl.textContent = remain <= 0 ? '快讀完了' : '剩 ' + remain + ' 分鐘';
      }
    };

    // Hide on small screens when scroll-to-top button overlaps; the pill is on the LEFT, button on RIGHT — no conflict.
    // Auto-hide briefly on tap so it doesn't obscure links on mobile.
    let hideTimer;
    pill.addEventListener('click', () => {
      pill.style.opacity = '.15';
      clearTimeout(hideTimer);
      hideTimer = setTimeout(() => { pill.style.opacity = ''; }, 2500);
    });
  };

  /* ---------- Web Vitals → GA4 ---------- *
   * Sends LCP, INP, CLS, FCP, TTFB as gtag('event','web_vitals',{...}).
   * Uses native PerformanceObserver — no external library, no extra bytes.
   * Safe to call even if gtag is not configured (data is just dropped). */
  BL.initWebVitals = function () {
    if (BL._vitalsArmed) return;
    BL._vitalsArmed = true;
    if (!('PerformanceObserver' in window)) return;

    const send = (name, value, extra) => {
      try {
        const v = Math.round(name === 'CLS' ? value * 1000 : value);
        const payload = Object.assign({
          event_category: 'Web Vitals',
          event_label: location.pathname,
          value: v,
          metric_name: name,
          metric_value: v,
          non_interaction: true
        }, extra || {});
        if (typeof window.gtag === 'function') window.gtag('event', 'web_vitals', payload);
        // Mirror to dataLayer for GTM users
        (window.dataLayer = window.dataLayer || []).push({ event: 'web_vitals', ...payload });
      } catch (e) { /* never break the page for analytics */ }
    };

    // Largest Contentful Paint — keep the latest entry
    let lcpValue = 0;
    try {
      const lcpObs = new PerformanceObserver((list) => {
        const entries = list.getEntries();
        const last = entries[entries.length - 1];
        if (last) lcpValue = last.renderTime || last.loadTime || last.startTime;
      });
      lcpObs.observe({ type: 'largest-contentful-paint', buffered: true });
    } catch (e) {}

    // Cumulative Layout Shift — sum non-input shifts in 1s/5s window
    let clsValue = 0;
    try {
      const clsObs = new PerformanceObserver((list) => {
        for (const entry of list.getEntries()) {
          if (!entry.hadRecentInput) clsValue += entry.value;
        }
      });
      clsObs.observe({ type: 'layout-shift', buffered: true });
    } catch (e) {}

    // First Contentful Paint
    try {
      const fcpObs = new PerformanceObserver((list) => {
        for (const entry of list.getEntries()) {
          if (entry.name === 'first-contentful-paint') {
            send('FCP', entry.startTime);
            fcpObs.disconnect();
          }
        }
      });
      fcpObs.observe({ type: 'paint', buffered: true });
    } catch (e) {}

    // Time To First Byte
    try {
      const nav = performance.getEntriesByType('navigation')[0];
      if (nav && nav.responseStart > 0) send('TTFB', nav.responseStart);
    } catch (e) {}

    // Interaction to Next Paint — track worst event-timing duration
    let inpValue = 0;
    try {
      const inpObs = new PerformanceObserver((list) => {
        for (const entry of list.getEntries()) {
          if (entry.duration > inpValue) inpValue = entry.duration;
        }
      });
      inpObs.observe({ type: 'event', buffered: true, durationThreshold: 16 });
    } catch (e) {}

    // Flush LCP/CLS/INP when the page is hidden or unloaded (most reliable signal)
    const flush = () => {
      if (lcpValue) send('LCP', lcpValue);
      if (clsValue >= 0) send('CLS', clsValue);
      if (inpValue) send('INP', inpValue);
      lcpValue = 0; clsValue = 0; inpValue = 0;
    };
    addEventListener('visibilitychange', () => { if (document.visibilityState === 'hidden') flush(); }, { capture: true });
    addEventListener('pagehide', flush, { capture: true });
  };

  /* ---------- Giscus comments (lazy-loaded when scrolled into view) ---------- *
   * Opts: { repo, repoId, category, categoryId, mapping, theme }
   * Requires the host page to have <div id="bl-comments"></div> at the desired location;
   * if missing, the function injects one before the footer. */
  BL.injectComments = function (cfg) {
    cfg = cfg || {};
    const repo       = cfg.repo       || 'cyc09180/brilliancelab';
    const repoId     = cfg.repoId     || '';   // pass real ID to enable; empty disables
    const category   = cfg.category   || 'Announcements';
    const categoryId = cfg.categoryId || '';
    const mapping    = cfg.mapping    || 'pathname';
    const theme      = cfg.theme      || 'light';

    let mount = document.getElementById('bl-comments');
    if (!mount) {
      mount = document.createElement('section');
      mount.id = 'bl-comments';
      mount.setAttribute('aria-label', '留言區 / Comments');
      mount.style.cssText = 'max-width:780px;margin:48px auto 24px;padding:0 20px';
      mount.innerHTML = '<h2 style="font-size:18px;font-weight:700;color:#1a1d2e;margin-bottom:14px;letter-spacing:-.01em;border-left:3px solid #c9a45c;padding-left:12px"><span data-zh="留言討論" data-en="Comments" data-ja="コメント" data-ko="댓글" data-zhcn="留言讨论">留言討論</span></h2><div id="bl-comments-slot" style="min-height:160px;border:1px dashed #ebe6dc;border-radius:14px;background:#fffdf7;display:flex;align-items:center;justify-content:center;color:#7e8194;font-size:12.5px">向下滾動以載入留言…</div>';
      const footer = document.querySelector('footer');
      if (footer) footer.parentNode.insertBefore(mount, footer);
      else document.body.appendChild(mount);
    }
    if (!repoId || !categoryId) {
      const slot = mount.querySelector('#bl-comments-slot') || mount;
      slot.textContent = '留言系統設定中 — 待 Giscus repo ID 上線後自動啟用。';
      return;
    }

    const load = () => {
      if (mount.dataset.loaded) return;
      mount.dataset.loaded = '1';
      const s = document.createElement('script');
      s.src = 'https://giscus.app/client.js';
      s.async = true; s.crossOrigin = 'anonymous';
      s.setAttribute('data-repo', repo);
      s.setAttribute('data-repo-id', repoId);
      s.setAttribute('data-category', category);
      s.setAttribute('data-category-id', categoryId);
      s.setAttribute('data-mapping', mapping);
      s.setAttribute('data-strict', '0');
      s.setAttribute('data-reactions-enabled', '1');
      s.setAttribute('data-emit-metadata', '0');
      s.setAttribute('data-input-position', 'top');
      s.setAttribute('data-theme', theme);
      s.setAttribute('data-lang', (document.documentElement.lang || 'zh-TW').startsWith('zh') ? 'zh-TW' : 'en');
      s.setAttribute('data-loading', 'lazy');
      const slot = mount.querySelector('#bl-comments-slot') || mount;
      slot.replaceWith(s);
    };
    if ('IntersectionObserver' in window) {
      const io = new IntersectionObserver((es) => {
        if (es.some(e => e.isIntersecting)) { load(); io.disconnect(); }
      }, { rootMargin: '300px 0px' });
      io.observe(mount);
    } else { load(); }
  };

  /* ---------- Related-article cross-link graph ----------
   * Hand-curated topic adjacency for 43 articles. Each slug lists 4 related slugs. */
  BL.RELATED = {
    'master-guide':            ['gia-guide','hearts-arrows-truth','budget-formula','engagement-guide'],
    'gia-guide':               ['cert-comparison','hearts-arrows-truth','diamond-color','diamond-clarity'],
    'hearts-arrows-truth':     ['round-cut-deep-dive','gia-guide','budget-formula','fluorescence-deep-dive'],
    'budget-formula':          ['hearts-arrows-truth','diamond-carat-size','lab-vs-natural','engagement-guide'],
    'lab-vs-natural':          ['budget-formula','sustainable-diamonds','moissanite-vs-cz-vs-lab','diamond-resale'],
    'diamond-color':           ['diamond-clarity','gia-guide','fluorescence-deep-dive','wedding-metals'],
    'diamond-clarity':         ['diamond-color','inclusions-types-guide','gia-guide','cert-comparison'],
    'diamond-carat-size':      ['budget-formula','diamond-shapes','round-cut-deep-dive','engagement-guide'],
    'diamond-shapes':          ['round-cut-deep-dive','fancy-cuts-guide','diamond-carat-size','prong-settings-guide'],
    'cert-comparison':         ['gia-guide','lab-vs-natural','diamond-scams','hearts-arrows-truth'],
    'engagement-guide':        ['proposal-speech','ring-sizing','engagement-timeline','budget-formula'],
    'diamond-scams':           ['cert-comparison','secondhand-rings','moissanite-vs-cz-vs-lab','diamond-resale'],
    'diamond-financing':       ['budget-formula','engagement-guide','diamond-resale','secondhand-rings'],
    'secondhand-rings':        ['diamond-resale','heirloom-redesign','ring-insurance','cert-comparison'],
    'diamond-faq':             ['master-guide','gia-guide','budget-formula','engagement-guide'],
    'proposal-speech':         ['engagement-guide','engagement-timeline','dating-duration','destination-wedding'],
    'ring-sizing':             ['wedding-bands','wedding-metals','prong-settings-guide','engagement-guide'],
    'wedding-bands':           ['wedding-metals','ring-sizing','engraving-personalization','mens-engagement-rings'],
    'wedding-metals':          ['wedding-bands','diamond-color','prong-settings-guide','ring-insurance'],
    'mens-engagement-rings':   ['wedding-bands','prong-settings-guide','engraving-personalization','lgbtq-rings'],
    'diamond-care':            ['ring-insurance','prong-settings-guide','diamond-resale','heirloom-redesign'],
    'ring-insurance':          ['diamond-care','diamond-resale','secondhand-rings','heirloom-redesign'],
    'diamond-resale':          ['lab-vs-natural','secondhand-rings','ring-insurance','diamond-price-trends'],
    'diamond-fun-facts':       ['famous-diamonds','sustainable-diamonds','diamond-news-2026','diamond-price-trends'],
    'round-cut-deep-dive':     ['hearts-arrows-truth','fancy-cuts-guide','diamond-shapes','fluorescence-deep-dive'],
    'fancy-cuts-guide':        ['diamond-shapes','round-cut-deep-dive','prong-settings-guide','diamond-carat-size'],
    'prong-settings-guide':    ['wedding-bands','wedding-metals','ring-sizing','diamond-care'],
    'fluorescence-deep-dive':  ['diamond-color','gia-guide','round-cut-deep-dive','inclusions-types-guide'],
    'inclusions-types-guide':  ['diamond-clarity','gia-guide','fluorescence-deep-dive','diamond-scams'],
    'engraving-personalization':['wedding-bands','mens-engagement-rings','heirloom-redesign','wedding-metals'],
    'moissanite-vs-cz-vs-lab': ['lab-vs-natural','diamond-scams','sustainable-diamonds','cert-comparison'],
    'famous-diamonds':         ['diamond-fun-facts','heirloom-redesign','diamond-price-trends','sustainable-diamonds'],
    'engagement-timeline':     ['engagement-guide','proposal-speech','ring-sizing','dating-duration'],
    'gemstones-comparison':    ['lab-vs-natural','moissanite-vs-cz-vs-lab','diamond-color','sustainable-diamonds'],
    'sustainable-diamonds':    ['lab-vs-natural','diamond-news-2026','famous-diamonds','moissanite-vs-cz-vs-lab'],
    'heirloom-redesign':       ['diamond-care','engraving-personalization','ring-insurance','famous-diamonds'],
    'diamond-vs-gold':         ['diamond-resale','diamond-price-trends','sustainable-diamonds','wedding-metals'],
    'lgbtq-rings':             ['mens-engagement-rings','wedding-bands','engagement-guide','proposal-speech'],
    'diamond-photography':     ['hearts-arrows-truth','round-cut-deep-dive','diamond-fun-facts','engagement-guide'],
    'dating-duration':         ['engagement-timeline','proposal-speech','engagement-guide','destination-wedding'],
    'destination-wedding':     ['engagement-timeline','proposal-speech','dating-duration','engagement-guide'],
    'diamond-price-trends':    ['diamond-news-2026','diamond-resale','lab-vs-natural','sustainable-diamonds'],
    'diamond-news-2026':       ['diamond-price-trends','sustainable-diamonds','lab-vs-natural','master-guide']
  };
  // Title lookup so we don't hard-code titles in every page; fallback = humanise the slug.
  BL.TITLES = {
    'master-guide':           { zh:'鑽石購買總教學', en:'Diamond buying master guide' },
    'gia-guide':              { zh:'如何看懂 GIA 鑑定書', en:'How to read a GIA report' },
    'hearts-arrows-truth':    { zh:'八心八箭真相', en:'Hearts & Arrows truth' },
    'budget-formula':         { zh:'BPD 預算公式', en:'BPD budget formula' },
    'lab-vs-natural':         { zh:'天然 vs 培育鑽石', en:'Lab vs natural diamonds' },
    'diamond-color':          { zh:'鑽石顏色 D-Z', en:'Diamond color D-Z' },
    'diamond-clarity':        { zh:'鑽石淨度 FL-I', en:'Diamond clarity FL-I' },
    'diamond-carat-size':     { zh:'克拉與視覺尺寸', en:'Carat vs face-up size' },
    'diamond-shapes':         { zh:'鑽石形狀指南', en:'Diamond shapes guide' },
    'cert-comparison':        { zh:'證書比較 GIA / IGI', en:'GIA vs IGI cert comparison' },
    'engagement-guide':       { zh:'結婚鑽戒 9 步驟', en:'Engagement ring 9 steps' },
    'diamond-scams':          { zh:'鑽石詐騙 TOP 10', en:'Top 10 diamond scams' },
    'diamond-financing':      { zh:'鑽石分期付款', en:'Diamond financing' },
    'secondhand-rings':       { zh:'二手婚戒指南', en:'Pre-owned ring guide' },
    'diamond-faq':            { zh:'鑽石購買 50 問 FAQ', en:'50 diamond FAQs' },
    'proposal-speech':        { zh:'求婚詞 50 句', en:'50 proposal lines' },
    'ring-sizing':            { zh:'戒指尺寸完整指南', en:'Ring sizing guide' },
    'wedding-bands':          { zh:'婚戒 5 種類完整指南', en:'5 wedding band types' },
    'wedding-metals':         { zh:'婚戒材質完整指南', en:'Wedding metals guide' },
    'mens-engagement-rings':  { zh:'男士訂婚戒指南', en:"Men's engagement rings" },
    'diamond-care':           { zh:'鑽石保養全攻略', en:'Diamond care guide' },
    'ring-insurance':         { zh:'婚戒保險與失竊', en:'Ring insurance & theft' },
    'diamond-resale':         { zh:'鑽石回收與保值', en:'Diamond resale truth' },
    'diamond-fun-facts':      { zh:'鑽石 30 個冷知識', en:'30 diamond fun facts' },
    'round-cut-deep-dive':    { zh:'圓形明亮車工解析', en:'Round brilliant deep dive' },
    'fancy-cuts-guide':       { zh:'花式車工指南', en:'Fancy cuts guide' },
    'prong-settings-guide':   { zh:'鑽戒爪鑲 7 種', en:'7 prong settings' },
    'fluorescence-deep-dive': { zh:'鑽石螢光反應', en:'Fluorescence deep dive' },
    'inclusions-types-guide': { zh:'內含物 8 種', en:'8 inclusion types' },
    'engraving-personalization':{ zh:'婚戒刻字指南', en:'Engraving guide' },
    'moissanite-vs-cz-vs-lab':{ zh:'真假鑽辨識', en:'Moissanite vs CZ vs lab' },
    'famous-diamonds':        { zh:'10 大名鑽傳奇', en:'10 famous diamonds' },
    'engagement-timeline':    { zh:'12 個月時間軸', en:'12-month proposal timeline' },
    'gemstones-comparison':   { zh:'4 大寶石比較', en:'4 gemstones compared' },
    'sustainable-diamonds':   { zh:'道德鑽石指南', en:'Sustainable diamonds' },
    'heirloom-redesign':      { zh:'傳家鑽石重做', en:'Heirloom redesign' },
    'diamond-vs-gold':        { zh:'鑽石 vs 黃金保值', en:'Diamond vs gold as store of value' },
    'lgbtq-rings':            { zh:'同志婚戒指南', en:'LGBTQ+ ring guide' },
    'diamond-photography':    { zh:'鑽石攝影 IG 教學', en:'Diamond photography' },
    'dating-duration':        { zh:'交往多久求婚', en:'When to propose' },
    'destination-wedding':    { zh:'異國婚禮採購', en:'Destination wedding' },
    'diamond-price-trends':   { zh:'2026-2030 鑽石價格趨勢', en:'2026-2030 price trends' },
    'diamond-news-2026':      { zh:'2026 鑽石市場新聞', en:'2026 diamond news' }
  };

  BL.injectRelated = function (slug) {
    if (!slug || document.getElementById('bl-related')) return;
    const list = BL.RELATED[slug];
    if (!list || !list.length) return;
    const sec = document.createElement('section');
    sec.id = 'bl-related';
    sec.setAttribute('aria-label', '相關文章 / Related articles');
    sec.style.cssText = 'max-width:780px;margin:48px auto 0;padding:0 20px';
    let cards = '';
    list.forEach((s, i) => {
      const t = BL.TITLES[s] || { zh: s.replace(/-/g, ' '), en: s.replace(/-/g, ' ') };
      cards += '<a href="/blog/' + s + '" class="bl-rel-card" style="display:block;padding:14px 16px;background:#fff;border:1px solid #ebe6dc;border-radius:14px;text-decoration:none;color:#1a1d2e;transition:all .2s ease"><div style="font-size:10.5px;letter-spacing:.18em;text-transform:uppercase;color:#8a6e30;font-weight:700;margin-bottom:4px">相關 0' + (i + 1) + '</div><div style="font-size:14px;font-weight:600;line-height:1.45" data-zh="' + t.zh + '" data-en="' + t.en + '">' + t.zh + '</div></a>';
    });
    sec.innerHTML = '<h2 style="font-size:18px;font-weight:700;color:#1a1d2e;margin-bottom:14px;letter-spacing:-.01em;border-left:3px solid #c9a45c;padding-left:12px"><span data-zh="繼續閱讀相關主題" data-en="Continue reading" data-ja="関連記事" data-ko="관련 글" data-zhcn="继续阅读相关主题">繼續閱讀相關主題</span></h2><div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px">' + cards + '</div>';
    const footer = document.querySelector('footer');
    if (footer) footer.parentNode.insertBefore(sec, footer);
    else document.body.appendChild(sec);
    // Hover affordance
    sec.querySelectorAll('.bl-rel-card').forEach(c => {
      c.addEventListener('mouseenter', () => { c.style.borderColor = 'rgba(201,164,92,.55)'; c.style.transform = 'translateY(-2px)'; c.style.boxShadow = '0 12px 24px -16px rgba(138,110,48,.4)'; });
      c.addEventListener('mouseleave', () => { c.style.borderColor = '#ebe6dc'; c.style.transform = ''; c.style.boxShadow = ''; });
    });
  };

  /* ---------- TOC: auto-id every H2/H3 inside the article + floating side TOC ----------
   * Targets the visible article container (#proseZh / #proseEn / <article>).
   * For each <h2>/<h3>, derives a stable slug, assigns it as id, and inserts
   * a "¶" anchor link. Then injects a fixed right-side floating TOC that
   * highlights the current section as you scroll. Mobile collapses to a
   * top-anchor list. Skips if fewer than 3 headings — short pages don't need it. */
  BL._slugify = function (s) {
    s = (s || '').trim()
      // Strip trailing pilcrow/anchor symbols if re-running
      .replace(/[¶#§]+$/, '')
      // CJK + ASCII slug: keep CJK, replace runs of non-CJK-non-alnum with `-`
      .replace(/[^\w㐀-䶿一-鿿豈-﫿-]+/g, '-')
      .replace(/-+/g, '-')
      .replace(/^-|-$/g, '');
    return s.toLowerCase();
  };

  BL.injectTOC = function () {
    if (document.getElementById('bl-toc')) return;
    const candidates = ['#proseZh', '#proseEn', 'article', 'main'];
    let root = null;
    for (const sel of candidates) {
      const el = document.querySelector(sel);
      if (el && el.offsetParent !== null) { root = el; break; }
    }
    if (!root) return;

    const heads = root.querySelectorAll('h2, h3');
    if (heads.length < 3) return;

    const used = new Set();
    const items = [];
    heads.forEach((h) => {
      // Derive id if missing
      if (!h.id) {
        let base = BL._slugify(h.textContent) || 'sec';
        let id = base, n = 2;
        while (used.has(id) || document.getElementById(id)) { id = base + '-' + n++; }
        h.id = id;
      }
      used.add(h.id);
      // Add ¶ anchor link (visually hidden until hover)
      if (!h.querySelector('.bl-anchor')) {
        const a = document.createElement('a');
        a.href = '#' + h.id;
        a.className = 'bl-anchor';
        a.setAttribute('aria-label', '直接連結到此節');
        a.textContent = '¶';
        a.style.cssText = 'opacity:0;margin-left:.4em;color:#c9a45c;text-decoration:none;font-weight:400;transition:opacity .15s';
        h.appendChild(a);
        h.addEventListener('mouseenter', () => { a.style.opacity = '.6'; });
        h.addEventListener('mouseleave', () => { a.style.opacity = '0'; });
      }
      items.push({ id: h.id, text: h.textContent.replace(/¶$/, '').trim(), level: h.tagName === 'H3' ? 3 : 2 });
    });

    // Build the floating TOC (desktop ≥ 1280px) — sits right of the article column.
    const toc = document.createElement('aside');
    toc.id = 'bl-toc';
    toc.setAttribute('role', 'navigation');
    toc.setAttribute('aria-label', '本篇章節目錄 / Table of contents');
    toc.style.cssText = 'position:fixed;right:24px;top:96px;width:240px;max-height:calc(100vh - 140px);overflow-y:auto;background:rgba(255,253,247,.92);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);border:1px solid rgba(201,164,92,.4);border-radius:14px;padding:14px 14px 14px 18px;z-index:30;font-family:Inter,"Microsoft JhengHei",sans-serif;font-size:12.5px;line-height:1.6;box-shadow:0 12px 28px -18px rgba(138,110,48,.4);transition:opacity .25s';
    let html = '<div style="font-size:10.5px;letter-spacing:.22em;text-transform:uppercase;color:#8a6e30;font-weight:700;margin-bottom:8px;padding-bottom:8px;border-bottom:1px solid rgba(201,164,92,.25)">本篇導覽</div><ol style="list-style:none;padding:0;margin:0">';
    items.forEach((it, i) => {
      html += `<li style="margin:${it.level === 3 ? '2px 0 2px 14px' : '4px 0'}"><a data-toc-id="${it.id}" href="#${it.id}" style="display:block;padding:4px 8px;border-radius:6px;color:#4a4d5e;text-decoration:none;border-left:2px solid transparent;${it.level === 3 ? 'font-size:11.5px;color:#7e8194;' : ''}">${it.text}</a></li>`;
    });
    html += '</ol>';
    toc.innerHTML = html;

    // Hide on small screens via media query (inject once)
    if (!document.getElementById('bl-toc-style')) {
      const st = document.createElement('style');
      st.id = 'bl-toc-style';
      st.textContent = '@media (max-width:1279px){#bl-toc{display:none!important}}#bl-toc a:hover{background:rgba(251,243,223,.6);color:#5e4a1f}#bl-toc a[data-active="1"]{background:#fbf3df;color:#5e4a1f;border-left-color:#c9a45c!important;font-weight:600}';
      document.head.appendChild(st);
    }
    document.body.appendChild(toc);

    // Active section highlight via IntersectionObserver
    if ('IntersectionObserver' in window) {
      const linkMap = {};
      toc.querySelectorAll('a[data-toc-id]').forEach(a => { linkMap[a.dataset.tocId] = a; });
      let active = null;
      const setActive = (id) => {
        if (active === id) return;
        if (active && linkMap[active]) linkMap[active].removeAttribute('data-active');
        active = id;
        if (id && linkMap[id]) linkMap[id].setAttribute('data-active', '1');
      };
      const io = new IntersectionObserver((entries) => {
        // Pick the topmost intersecting heading
        const visible = entries.filter(e => e.isIntersecting).sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top);
        if (visible[0]) setActive(visible[0].target.id);
      }, { rootMargin: '-20% 0px -65% 0px' });
      heads.forEach(h => io.observe(h));
    }

    // Insert ItemList JSON-LD for the TOC (helps Google's "Jump to" rich result)
    if (items.length >= 4 && !document.getElementById('bl-toc-jsonld')) {
      const url = location.href.split('#')[0];
      const ld = {
        '@context': 'https://schema.org',
        '@type':    'ItemList',
        'name':     'Table of contents',
        'itemListOrder': 'https://schema.org/ItemListOrderAscending',
        'numberOfItems': items.length,
        'itemListElement': items.map((it, i) => ({
          '@type':   'ListItem',
          'position': i + 1,
          'name':     it.text,
          'url':      url + '#' + it.id
        }))
      };
      const s = document.createElement('script');
      s.id = 'bl-toc-jsonld';
      s.type = 'application/ld+json';
      s.textContent = JSON.stringify(ld);
      document.head.appendChild(s);
    }
  };

  /* ---------- scroll-to-top floating button ---------- */
  BL.addScrollToTop = function () {
    if (document.getElementById('bl-totop')) return;
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.id = 'bl-totop';
    btn.setAttribute('aria-label', '回到頂端 / Scroll to top');
    btn.setAttribute('title', '回到頂端 / Scroll to top');
    btn.innerHTML = '<span aria-hidden="true">↑</span>';
    btn.style.cssText = 'position:fixed;right:18px;bottom:24px;width:42px;height:42px;border-radius:50%;background:linear-gradient(180deg,#d4b87a,#8a6e30);color:#fff;border:1px solid rgba(138,110,48,.5);box-shadow:0 8px 20px -8px rgba(138,110,48,.55);cursor:pointer;display:none;align-items:center;justify-content:center;z-index:50;font-size:18px;line-height:1;transition:transform .15s ease';
    btn.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
    btn.addEventListener('mouseenter', () => { btn.style.transform = 'translateY(-2px)'; });
    btn.addEventListener('mouseleave', () => { btn.style.transform = ''; });
    document.body.appendChild(btn);
    document.addEventListener('scroll', () => {
      btn.style.display = window.scrollY > 800 ? 'flex' : 'none';
    }, { passive: true });
  };

  /* ---------- mobile hamburger drawer (auto-injected on every blog page) ---------- */
  BL.injectMobileMenu = function () {
    if (document.getElementById('blMobileMenuBtn')) return;
    // Find the page's <header>; if missing, give up gracefully
    const header = document.querySelector('header.sticky') || document.querySelector('header');
    if (!header) return;
    const headerInner = header.querySelector('div.flex.items-center.justify-between') || header.firstElementChild;
    if (!headerInner) return;
    const right = headerInner.lastElementChild;   // usually the lang-toggle wrapper

    // 1) Hamburger button — inserted before the right cluster
    const btn = document.createElement('button');
    btn.id = 'blMobileMenuBtn';
    btn.type = 'button';
    btn.className = 'sm:hidden inline-flex items-center justify-center w-9 h-9 rounded-lg border border-[var(--border)] bg-white hover:border-gold-300 mr-2';
    btn.setAttribute('aria-label', 'Menu');
    btn.setAttribute('aria-expanded', 'false');
    btn.innerHTML = '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><line x1="4" y1="7" x2="20" y2="7"/><line x1="4" y1="12" x2="20" y2="12"/><line x1="4" y1="17" x2="20" y2="17"/></svg>';
    right.parentNode.insertBefore(btn, right);

    // 2) Drawer — appended INSIDE the header so it inherits sticky positioning
    const drawer = document.createElement('div');
    drawer.id = 'blMobileDrawer';
    drawer.className = 'hidden sm:hidden border-t border-[var(--border)]';
    // max-height + overflow so drawer scrolls when its content is taller than viewport
    drawer.style.cssText = 'background:rgba(250,248,243,.98);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);max-height:calc(100vh - 64px);overflow-y:auto;-webkit-overflow-scrolling:touch;';
    drawer.innerHTML = `
      <nav class="max-w-5xl mx-auto px-5 py-4 flex flex-col gap-1">
        <a href="/"        class="block px-3 py-2.5 rounded-lg hover:bg-[var(--gold-soft)] text-[14px] font-semibold text-gold-700"
           data-zh="🛠 主頁工具(輸入鑽石評分)"   data-en="🛠 Home tool"     data-ja="🛠 ホームツール"  data-ko="🛠 홈 도구"   data-zhcn="🛠 主页工具"></a>
        <div class="mt-2 px-3 pt-2 border-t border-[var(--border)]">
          <div class="text-[10.5px] uppercase tracking-[.22em] text-gold-700 font-semibold mb-2"
               data-zh="部落格文章" data-en="Blog articles" data-ja="ブログ記事" data-ko="블로그 게시물" data-zhcn="博客文章"></div>
          <a href="/blog/"                    class="block py-2 text-[13.5px] text-ink-700 font-semibold"
             data-zh="📖 全部文章索引" data-en="📖 All articles"  data-ja="📖 記事一覧" data-ko="📖 모든 게시물" data-zhcn="📖 全部文章索引"></a>
          <a href="/blog/master-guide"        class="block py-2 text-[13.5px] text-gold-700 font-bold"
             data-zh="★ 鑽石購買總教學(主幹)" data-en="★ Master Guide (pillar)"></a>

          <div class="mt-2 pt-2 border-t border-[var(--line)] text-[10px] uppercase tracking-[.18em] text-ink-500" data-zh="基礎篇" data-en="Fundamentals">基礎篇</div>
          <a href="/blog/gia-guide"           class="block py-1.5 text-[13px] text-ink-700" data-zh="① 如何看懂 GIA 鑑定書" data-en="① GIA report"></a>
          <a href="/blog/hearts-arrows-truth" class="block py-1.5 text-[13px] text-ink-700" data-zh="② 八心八箭真相" data-en="② H&amp;A truth"></a>
          <a href="/blog/budget-formula"      class="block py-1.5 text-[13px] text-ink-700" data-zh="③ 挑最閃公式 BPD" data-en="③ BPD formula"></a>
          <a href="/blog/lab-vs-natural"      class="block py-1.5 text-[13px] text-ink-700" data-zh="④ 天然 vs 實驗室鑽石" data-en="④ Natural vs lab"></a>

          <div class="mt-2 text-[10px] uppercase tracking-[.18em] text-ink-500" data-zh="4C 拆解" data-en="4Cs">4C 拆解</div>
          <a href="/blog/diamond-color"       class="block py-1.5 text-[13px] text-ink-700" data-zh="⑤ 鑽石顏色 D-Z" data-en="⑤ Color D-Z"></a>
          <a href="/blog/diamond-clarity"     class="block py-1.5 text-[13px] text-ink-700" data-zh="⑥ 鑽石淨度 FL-I" data-en="⑥ Clarity FL-I"></a>
          <a href="/blog/diamond-carat-size"  class="block py-1.5 text-[13px] text-ink-700" data-zh="⑦ 克拉與視覺尺寸" data-en="⑦ Carat vs size"></a>
          <a href="/blog/diamond-shapes"      class="block py-1.5 text-[13px] text-ink-700" data-zh="⑧ 鑽石形狀指南" data-en="⑧ Diamond shapes"></a>
          <a href="/blog/cert-comparison"     class="block py-1.5 text-[13px] text-ink-700" data-zh="⑨ 證書比較 GIA / IGI" data-en="⑨ Cert comparison"></a>

          <div class="mt-2 text-[10px] uppercase tracking-[.18em] text-ink-500" data-zh="購買實戰" data-en="Practical">購買實戰</div>
          <a href="/blog/engagement-guide"    class="block py-1.5 text-[13px] text-ink-700" data-zh="⑩ 結婚鑽戒 9 步驟" data-en="⑩ Engagement 9 steps"></a>
          <a href="/blog/diamond-scams"       class="block py-1.5 text-[13px] text-ink-700" data-zh="⑪ 詐騙 TOP 10 避雷" data-en="⑪ Top 10 scams"></a>
          <a href="/blog/diamond-financing"   class="block py-1.5 text-[13px] text-ink-700" data-zh="⑫ 鑽石分期付款指南" data-en="⑫ Financing guide"></a>
          <a href="/blog/secondhand-rings"    class="block py-1.5 text-[13px] text-ink-700" data-zh="⑬ 二手婚戒購買指南" data-en="⑬ Pre-owned guide"></a>
          <a href="/blog/diamond-faq"         class="block py-1.5 text-[13px] text-ink-700" data-zh="⑭ 鑽石購買 50 問 FAQ" data-en="⑭ 50 FAQs"></a>

          <div class="mt-2 text-[10px] uppercase tracking-[.18em] text-ink-500" data-zh="求婚與婚戒" data-en="Proposal &amp; Bands">求婚與婚戒</div>
          <a href="/blog/proposal-speech"     class="block py-1.5 text-[13px] text-ink-700" data-zh="⑮ 求婚詞 50 句" data-en="⑮ 50 proposal lines"></a>
          <a href="/blog/ring-sizing"         class="block py-1.5 text-[13px] text-ink-700" data-zh="⑯ 戒指尺寸完整指南" data-en="⑯ Ring sizing"></a>
          <a href="/blog/wedding-bands"       class="block py-1.5 text-[13px] text-ink-700" data-zh="⑰ 5 種戒指完全指南" data-en="⑰ 5 ring types"></a>
          <a href="/blog/wedding-metals"      class="block py-1.5 text-[13px] text-ink-700" data-zh="⑱ 婚戒材質完整指南" data-en="⑱ Wedding metals"></a>
          <a href="/blog/mens-engagement-rings" class="block py-1.5 text-[13px] text-ink-700" data-zh="⑲ 男士訂婚戒指南" data-en="⑲ Men's rings"></a>

          <div class="mt-2 text-[10px] uppercase tracking-[.18em] text-ink-500" data-zh="保養與市場" data-en="Care &amp; Market">保養與市場</div>
          <a href="/blog/diamond-care"        class="block py-1.5 text-[13px] text-ink-700" data-zh="⑳ 鑽石保養全攻略" data-en="⑳ Diamond care"></a>
          <a href="/blog/ring-insurance"      class="block py-1.5 text-[13px] text-ink-700" data-zh="㉑ 婚戒保險與失竊處理" data-en="㉑ Ring insurance"></a>
          <a href="/blog/diamond-resale"      class="block py-1.5 text-[13px] text-ink-700" data-zh="㉒ 鑽石回收與保值真相" data-en="㉒ Resale truth"></a>
          <a href="/blog/diamond-fun-facts"   class="block py-1.5 text-[13px] text-ink-700" data-zh="㉓ 鑽石 30 個冷知識" data-en="㉓ 30 fun facts"></a>

          <div class="mt-2 text-[10px] uppercase tracking-[.18em] text-gold-700 font-semibold" data-zh="✦ 深度子文" data-en="✦ Deep Dives">✦ 深度子文</div>
          <a href="/blog/round-cut-deep-dive"      class="block py-1.5 text-[13px] text-ink-700" data-zh="◆ 圓形明亮車工" data-en="◆ Round brilliant"></a>
          <a href="/blog/fancy-cuts-guide"         class="block py-1.5 text-[13px] text-ink-700" data-zh="◆ 花式車工指南" data-en="◆ Fancy cuts"></a>
          <a href="/blog/prong-settings-guide"     class="block py-1.5 text-[13px] text-ink-700" data-zh="◆ 鑽戒爪鑲 7 種" data-en="◆ 7 prong settings"></a>
          <a href="/blog/fluorescence-deep-dive"   class="block py-1.5 text-[13px] text-ink-700" data-zh="◆ 鑽石螢光反應" data-en="◆ Fluorescence"></a>
          <a href="/blog/inclusions-types-guide"   class="block py-1.5 text-[13px] text-ink-700" data-zh="◆ 內含物 8 種" data-en="◆ 8 inclusions"></a>
          <a href="/blog/engraving-personalization" class="block py-1.5 text-[13px] text-ink-700" data-zh="◆ 婚戒刻字指南" data-en="◆ Engraving"></a>
          <a href="/blog/moissanite-vs-cz-vs-lab" class="block py-1.5 text-[13px] text-ink-700" data-zh="◆ 真假鑽辨識" data-en="◆ Real vs fake"></a>
          <a href="/blog/famous-diamonds"      class="block py-1.5 text-[13px] text-ink-700" data-zh="◆ 10 大名鑽傳奇" data-en="◆ 10 famous diamonds"></a>
          <a href="/blog/engagement-timeline"  class="block py-1.5 text-[13px] text-ink-700" data-zh="◆ 12 個月時間軸" data-en="◆ 12-month timeline"></a>

          <div class="mt-2 text-[10px] uppercase tracking-[.18em] text-gold-700 font-semibold" data-zh="✦ 進階主題" data-en="✦ Advanced">✦ 進階主題</div>
          <a href="/blog/gemstones-comparison" class="block py-1.5 text-[13px] text-ink-700" data-zh="◆ 4 大寶石比較" data-en="◆ 4 gemstones"></a>
          <a href="/blog/sustainable-diamonds"  class="block py-1.5 text-[13px] text-ink-700" data-zh="◆ 道德鑽石" data-en="◆ Sustainable"></a>
          <a href="/blog/heirloom-redesign"     class="block py-1.5 text-[13px] text-ink-700" data-zh="◆ 傳家鑽石重做" data-en="◆ Heirloom redesign"></a>
          <a href="/blog/diamond-vs-gold"       class="block py-1.5 text-[13px] text-ink-700" data-zh="◆ 鑽石 vs 黃金" data-en="◆ Diamond vs Gold"></a>
          <a href="/blog/lgbtq-rings"           class="block py-1.5 text-[13px] text-ink-700" data-zh="◆ 同志婚戒指南" data-en="◆ LGBTQ+ rings"></a>
          <a href="/blog/diamond-photography"   class="block py-1.5 text-[13px] text-ink-700" data-zh="◆ 鑽石攝影 IG" data-en="◆ Photography"></a>
          <a href="/blog/dating-duration"       class="block py-1.5 text-[13px] text-ink-700" data-zh="◆ 交往多久求婚" data-en="◆ When to propose"></a>
          <a href="/blog/destination-wedding"   class="block py-1.5 text-[13px] text-ink-700" data-zh="◆ 異國婚禮採購" data-en="◆ Destination wedding"></a>
          <a href="/blog/diamond-price-trends"  class="block py-1.5 text-[13px] text-ink-700" data-zh="◆ 2026-2030 趨勢" data-en="◆ Price trends"></a>

          <a href="/blog/topics"               class="block py-2 text-[13.5px] text-gold-700 font-bold" data-zh="🗺 主題索引(43 篇地圖)" data-en="🗺 Topic map"></a>
          <a href="/search"                    class="block py-2 text-[13.5px] text-gold-700 font-bold" data-zh="🔍 站內搜尋" data-en="🔍 Search"></a>

          <a href="/blog/diamond-news-2026"   class="block py-2 text-[13px] text-ink-700 mt-1 pt-2 border-t border-[var(--line)]"
             data-zh="🔔 2026 鑽石市場新聞" data-en="🔔 2026 diamond news"></a>
        </div>
        <a href="/blog/feed.xml" class="mt-2 mx-3 inline-flex items-center justify-center gap-2 py-2.5 rounded-lg border border-[var(--border)] text-[12.5px] font-semibold text-ink-700">
          <svg viewBox="0 0 24 24" width="13" height="13" fill="#c75e00"><circle cx="6" cy="18" r="2.5"/><path d="M3 13a8 8 0 0 1 8 8h-3a5 5 0 0 0-5-5v-3zm0-6a14 14 0 0 1 14 14h-3a11 11 0 0 0-11-11V7z"/></svg>
          <span data-zh="RSS 訂閱" data-en="RSS feed" data-ja="RSS 購読" data-ko="RSS 구독" data-zhcn="RSS 订阅"></span>
        </a>
      </nav>
    `;
    header.appendChild(drawer);

    function open()  { drawer.classList.remove('hidden'); btn.setAttribute('aria-expanded', 'true');  document.body.style.overflow = 'hidden'; }
    function close() { drawer.classList.add('hidden');    btn.setAttribute('aria-expanded', 'false'); document.body.style.overflow = ''; }
    btn.setAttribute('aria-controls', 'blMobileDrawer');
    drawer.setAttribute('role', 'navigation');
    drawer.setAttribute('aria-label', '主選單 / Main menu');
    btn.addEventListener('click', () => drawer.classList.contains('hidden') ? open() : close());
    drawer.querySelectorAll('a').forEach(a => a.addEventListener('click', close));
    window.addEventListener('resize', () => { if (window.innerWidth >= 640) close(); });
  };

  /* ---------- derive slug from path when not explicitly passed ---------- */
  BL.deriveSlug = function () {
    const p = location.pathname.replace(/^\/+|\/+$/g, '').replace(/\.html$/, '');
    const parts = p.split('/');
    return parts[parts.length - 1] || '';
  };

  /* ---------- Affiliate-link decorator ----------
   * Add data-aff to any link to mark it as an affiliate target. This function:
   *   - rewrites href to append ?ref=brilliancelab&utm_source=brilliancelab
   *   - adds rel="sponsored noopener" + target="_blank"
   *   - adds a small "ⓢ Sponsored" badge after the link (CSS ::after)
   *   - logs a 'affiliate_click' event to gtag/dataLayer when clicked
   * Affiliate IDs come from BL.AFF_PARAMS or BL_AFF_PARAMS global. */
  BL.AFF_PARAMS = {
    'bluenile.com':    { ref: 'bl_diamonds',      utm_source: 'brilliancelab', utm_medium: 'affiliate' },
    'jamesallen.com':  { ref: 'bl_diamonds',      utm_source: 'brilliancelab', utm_medium: 'affiliate' },
    'tiffany.com':     { ref: 'bl',                utm_source: 'brilliancelab', utm_medium: 'referral'  },
    'cartier.com':     { ref: 'bl',                utm_source: 'brilliancelab', utm_medium: 'referral'  },
    'gia.edu':         {                            utm_source: 'brilliancelab', utm_medium: 'reference' }
  };
  BL.decorateAffiliates = function () {
    document.querySelectorAll('a[data-aff]').forEach((a) => {
      let url;
      try { url = new URL(a.href, location.href); } catch { return; }
      const host = url.hostname.replace(/^www\./, '');
      const params = (window.BL_AFF_PARAMS && window.BL_AFF_PARAMS[host]) || BL.AFF_PARAMS[host];
      if (params) {
        Object.entries(params).forEach(([k, v]) => { if (!url.searchParams.has(k)) url.searchParams.set(k, v); });
        a.href = url.toString();
      }
      a.rel = (a.rel ? a.rel + ' ' : '') + 'sponsored noopener';
      if (!a.target) a.target = '_blank';
      a.setAttribute('aria-describedby', 'bl-aff-disclosure');
      a.addEventListener('click', () => {
        const payload = { event_category: 'affiliate', event_label: host, link_url: a.href };
        if (typeof window.gtag === 'function') window.gtag('event', 'affiliate_click', payload);
        (window.dataLayer = window.dataLayer || []).push({ event: 'affiliate_click', ...payload });
      });
    });
    if (!document.getElementById('bl-aff-disclosure')) {
      const d = document.createElement('div');
      d.id = 'bl-aff-disclosure';
      d.style.cssText = 'position:absolute;left:-9999px;width:1px;height:1px;overflow:hidden';
      d.textContent = 'Affiliate link — BrillianceLab earns a commission if you purchase through this link.';
      document.body.appendChild(d);
    }
  };

  /* ---------- Sentry browser loader (lazy, ~50 KB) ----------
   * Wires window.onerror + unhandled rejection capture even before the SDK loads;
   * once the SDK is in, captured events are flushed.
   * Set BL.SENTRY_DSN before initBlog() (or pass via opts.sentry) to enable. */
  BL._errorBuffer = [];
  if (!BL._errorHooked) {
    BL._errorHooked = true;
    window.addEventListener('error', (e) => BL._errorBuffer.push({ type: 'error', msg: e.message, src: e.filename, line: e.lineno, col: e.colno }));
    window.addEventListener('unhandledrejection', (e) => BL._errorBuffer.push({ type: 'unhandledrejection', msg: String(e.reason && e.reason.message || e.reason) }));
  }
  BL.initSentry = function (dsn) {
    if (!dsn || BL._sentryArmed) return;
    BL._sentryArmed = true;
    const lazy = () => {
      const s = document.createElement('script');
      s.src = 'https://browser.sentry-cdn.com/8.42.0/bundle.tracing.min.js';
      s.crossOrigin = 'anonymous';
      s.integrity = '';   // pin integrity once you know the sub-resource hash
      s.onload = () => {
        if (!window.Sentry) return;
        Sentry.init({
          dsn: dsn,
          tracesSampleRate: 0.05,
          environment: location.hostname.includes('vercel.app') ? 'production' : 'preview',
          beforeSend: (event) => {
            // Drop AdSense / extension noise
            const f = (event.request && event.request.url) || '';
            if (/googlesyndication|chrome-extension|moz-extension/.test(f)) return null;
            return event;
          }
        });
        BL._errorBuffer.forEach((e) => Sentry.captureMessage(`[buffered] ${e.type}: ${e.msg}`, 'error'));
        BL._errorBuffer.length = 0;
      };
      document.head.appendChild(s);
    };
    // Defer until idle so it never competes with LCP
    if ('requestIdleCallback' in window) requestIdleCallback(lazy, { timeout: 4000 });
    else setTimeout(lazy, 3000);
  };

  /* ---------- one-call init for blog pages ---------- */
  BL.initBlog = function (opts) {
    opts = opts || {};
    const slug = opts.slug || (location.pathname.includes('/blog/') ? BL.deriveSlug() : '');
    let curLang = BL.detectLang();

    function apply(lang) {
      curLang = lang;
      BL.applyTextOnly(lang);
      const isZh = (lang === 'zh' || lang === 'zh-cn');
      const ze = document.getElementById(opts.proseZh || 'proseZh');
      const en = document.getElementById(opts.proseEn || 'proseEn');
      if (ze) ze.style.display = isZh ? '' : 'none';
      if (en) en.style.display = isZh ? 'none' : '';
      if (typeof opts.onChange === 'function') opts.onChange(lang);
    }

    BL.injectMobileMenu();      // run BEFORE injectLangDropdown so the lang trigger ends up to the right of hamburger
    BL.injectLangDropdown(apply);
    apply(curLang);

    // TOC must run BEFORE related/comments so the article hash anchors don't collide.
    if (opts.toc !== false) BL.injectTOC();

    // Related articles + comments injected BEFORE progress/reading-time so they exist in the DOM
    // before the height-based calculations run.
    if (slug && opts.related !== false) BL.injectRelated(slug);
    if (opts.comments) BL.injectComments(typeof opts.comments === 'object' ? opts.comments : {});

    BL.addReadingProgress();
    if (opts.readingTime !== false) BL.addReadingTime();

    // Web Vitals: opt-out via opts.vitals === false.
    if (opts.vitals !== false) BL.initWebVitals();

    // Sentry: opt-in via opts.sentry === '<dsn>' or window.BL_SENTRY_DSN.
    const dsn = opts.sentry || window.BL_SENTRY_DSN || '';
    if (dsn) BL.initSentry(dsn);

    // Affiliate-link decoration (auto runs; no-op when no [data-aff] on page).
    if (opts.affiliates !== false) BL.decorateAffiliates();

    const yr = document.getElementById('yr');
    if (yr) yr.textContent = new Date().getFullYear();

    if ('serviceWorker' in navigator) {
      navigator.serviceWorker.register('/sw.js').catch(() => {});
    }

    // Re-translate newly-injected nodes (related/comments) for the active language
    BL.applyTextOnly(curLang);

    return { applyLang: apply };
  };
})();
