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
