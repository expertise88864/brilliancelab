/* ============================================================
 * BrillianceLab — shared blog runtime
 * Centralises:
 *   - language detection (cookie > localStorage > navigator > en)
 *   - language preference persistence (cookie + localStorage)
 *   - 10-language dropdown injected over the existing toggle
 *   - reading progress bar
 *   - scroll-to-top button
 *   - footer year + service worker registration
 * Each blog page only needs:
 *   <script src="/blog/blog-shared.js" defer></script>
 *   <script>BL.initBlog({ proseZh:'proseZh', proseEn:'proseEn' });</script>
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

  /* ---------- reading-progress bar ---------- */
  BL.addReadingProgress = function () {
    if (document.getElementById('bl-progress')) return;
    const bar = document.createElement('div');
    bar.id = 'bl-progress';
    bar.style.cssText = 'position:fixed;top:0;left:0;height:3px;background:linear-gradient(90deg,#d4b87a,#8a6e30);z-index:60;width:0;transition:width .12s linear;pointer-events:none';
    document.body.appendChild(bar);
    function update() {
      const h = document.documentElement;
      const max = h.scrollHeight - h.clientHeight;
      bar.style.width = (max > 0 ? (h.scrollTop / max) * 100 : 0) + '%';
    }
    document.addEventListener('scroll', update, { passive: true });
    update();
  };

  /* ---------- scroll-to-top floating button ---------- */
  BL.addScrollToTop = function () {
    if (document.getElementById('bl-totop')) return;
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.id = 'bl-totop';
    btn.setAttribute('aria-label', 'Scroll to top');
    btn.innerHTML = '↑';
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
    drawer.style.cssText = 'background:rgba(250,248,243,.98);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px)';
    drawer.innerHTML = `
      <nav class="max-w-5xl mx-auto px-5 py-4 flex flex-col gap-1">
        <a href="/"        class="block px-3 py-2.5 rounded-lg hover:bg-[var(--gold-soft)] text-[14px] font-semibold text-gold-700"
           data-zh="🛠 主頁工具(輸入鑽石評分)"   data-en="🛠 Home tool"     data-ja="🛠 ホームツール"  data-ko="🛠 홈 도구"   data-zhcn="🛠 主页工具"></a>
        <div class="mt-2 px-3 pt-2 border-t border-[var(--border)]">
          <div class="text-[10.5px] uppercase tracking-[.22em] text-gold-700 font-semibold mb-2"
               data-zh="部落格文章" data-en="Blog articles" data-ja="ブログ記事" data-ko="블로그 게시물" data-zhcn="博客文章"></div>
          <a href="/blog/"                    class="block py-2 text-[13.5px] text-ink-700 font-semibold"
             data-zh="📖 全部文章索引" data-en="📖 All articles"  data-ja="📖 記事一覧" data-ko="📖 모든 게시물" data-zhcn="📖 全部文章索引"></a>
          <a href="/blog/gia-guide"           class="block py-2 text-[13px] text-ink-700"
             data-zh="① 如何看懂 GIA 鑑定書"           data-en="① How to read a GIA report"></a>
          <a href="/blog/hearts-arrows-truth" class="block py-2 text-[13px] text-ink-700"
             data-zh="② 八心八箭真相"                 data-en="② Hearts &amp; Arrows truth"></a>
          <a href="/blog/budget-formula"      class="block py-2 text-[13px] text-ink-700"
             data-zh="③ 30 萬以下挑最閃鑽石的數學公式" data-en="③ Math formula under NT$300K"></a>
          <a href="/blog/lab-vs-natural"      class="block py-2 text-[13px] text-ink-700"
             data-zh="④ 天然 vs 實驗室鑽石"           data-en="④ Natural vs lab-grown"></a>
          <a href="/blog/engagement-guide"    class="block py-2 text-[13px] text-ink-700"
             data-zh="⑤ 結婚鑽戒 9 步驟"             data-en="⑤ Engagement ring 9 steps"></a>
          <a href="/blog/cert-comparison"     class="block py-2 text-[13px] text-ink-700"
             data-zh="⑦ 鑽石證書比較"               data-en="⑦ Cert comparison"></a>
          <a href="/blog/diamond-scams"       class="block py-2 text-[13px] text-ink-700"
             data-zh="⑧ 鑽石詐騙 TOP 10"           data-en="⑧ Top 10 diamond scams"></a>
          <a href="/blog/diamond-shapes"      class="block py-2 text-[13px] text-ink-700"
             data-zh="⑨ 鑽石形狀完整指南"           data-en="⑨ Diamond shapes guide"></a>
          <a href="/blog/diamond-care"        class="block py-2 text-[13px] text-ink-700"
             data-zh="⑩ 鑽石保養全攻略"             data-en="⑩ Diamond care"></a>
          <a href="/blog/diamond-resale"      class="block py-2 text-[13px] text-ink-700"
             data-zh="⑪ 鑽石回收與保值真相"         data-en="⑪ Diamond resale truth"></a>
          <a href="/blog/diamond-color"       class="block py-2 text-[13px] text-ink-700"
             data-zh="⑫ 鑽石顏色等級 D-Z"           data-en="⑫ Diamond color D-Z"></a>
          <a href="/blog/diamond-clarity"     class="block py-2 text-[13px] text-ink-700"
             data-zh="⑬ 鑽石淨度等級 FL-I"          data-en="⑬ Diamond clarity FL-I"></a>
          <a href="/blog/diamond-carat-size"  class="block py-2 text-[13px] text-ink-700"
             data-zh="⑭ 鑽石克拉與視覺尺寸對照"       data-en="⑭ Carat vs face-up size"></a>
          <a href="/blog/diamond-news-2026"   class="block py-2 text-[13px] text-ink-700 mt-1 pt-2 border-t border-[var(--line)]"
             data-zh="🔔 2026 鑽石市場新聞(滾動更新)" data-en="🔔 2026 diamond news (rolling)"></a>
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
    btn.addEventListener('click', () => drawer.classList.contains('hidden') ? open() : close());
    drawer.querySelectorAll('a').forEach(a => a.addEventListener('click', close));
    window.addEventListener('resize', () => { if (window.innerWidth >= 640) close(); });
  };

  /* ---------- one-call init for blog pages ---------- */
  BL.initBlog = function (opts) {
    opts = opts || {};
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
    BL.addReadingProgress();
    BL.addScrollToTop();

    const yr = document.getElementById('yr');
    if (yr) yr.textContent = new Date().getFullYear();

    if ('serviceWorker' in navigator) {
      navigator.serviceWorker.register('/sw.js').catch(() => {});
    }

    return { applyLang: apply };
  };
})();
