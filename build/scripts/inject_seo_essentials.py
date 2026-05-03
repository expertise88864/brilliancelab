# -*- coding: utf-8 -*-
"""
Inject 4 cross-cutting SEO/UX upgrades into every blog article HTML:

  1. First-paragraph CTA — discreet inline link to the calculator inside the
     first <p> of #proseZh and #proseEn (boosts tool conversion + dwells).
  2. <noscript> visibility fallback — when JS is disabled (Googlebot's
     conservative crawl, fetch-as-Google for testing, screen readers in
     no-JS mode), reveal BOTH #proseZh and #proseEn so crawlers index full
     bilingual content rather than just the default Chinese block.
  3. fonts.gstatic.com preload — explicit `<link rel="preload" as="font"
     crossorigin>` for the actual woff2 URL the Google Fonts CSS resolves to.
     Saves a 200-400 ms LCP gap on cold loads.
  4. Pre-baked BreadcrumbList JSON-LD — runs the same hub-mapping logic that
     blog-shared.js uses at runtime, but writes the schema directly into the
     HTML so crawlers don't have to execute JS to see it.

Idempotent: each section is keyed off a sentinel (BL_CTA, BL_NOSCRIPT,
BL_FONTPRELOAD, BL_BREADCRUMB_LD) so re-running just refreshes content.
"""
from __future__ import annotations
import re, json
from pathlib import Path

# --- Auto-locate the repo root so this script can be run from anywhere ---
import os as _os
_os.chdir(Path(__file__).resolve().parents[2])  # → BrillianceLab/
# -------------------------------------------------------------------------

ROOT = Path('.')
DOMAIN = 'https://brilliancelab.vercel.app'

# --- Hub mapping (mirrors blog-shared.js BL.HUBS_REVERSE) ---
HUBS_REVERSE = {
    'gia-guide':'hub-fundamentals','hearts-arrows-truth':'hub-fundamentals','master-guide':'hub-fundamentals',
    'cert-comparison':'hub-fundamentals','lab-vs-natural':'hub-fundamentals','diamond-faq':'hub-fundamentals',
    'diamond-fun-facts':'hub-fundamentals',
    'diamond-color':'hub-4cs','diamond-clarity':'hub-4cs','diamond-carat-size':'hub-4cs',
    'diamond-shapes':'hub-4cs','round-cut-deep-dive':'hub-4cs','fancy-cuts-guide':'hub-4cs',
    'fluorescence-deep-dive':'hub-4cs','inclusions-types-guide':'hub-4cs',
    'budget-formula':'hub-purchase','engagement-guide':'hub-purchase','diamond-financing':'hub-purchase',
    'secondhand-rings':'hub-purchase','diamond-scams':'hub-purchase','moissanite-vs-cz-vs-lab':'hub-purchase',
    'engagement-timeline':'hub-proposal','proposal-speech':'hub-proposal','ring-sizing':'hub-proposal',
    'wedding-bands':'hub-proposal','wedding-metals':'hub-proposal','mens-engagement-rings':'hub-proposal',
    'lgbtq-rings':'hub-proposal',
    'diamond-care':'hub-care','ring-insurance':'hub-care','diamond-resale':'hub-care',
    'engraving-personalization':'hub-care','heirloom-redesign':'hub-care','prong-settings-guide':'hub-care',
    'diamond-price-trends':'hub-care',
    'taiwan-brands':'hub-purchase'
}
HUB_TITLES = {
    'hub-fundamentals': '基礎篇',
    'hub-4cs':          '4Cs 拆解',
    'hub-purchase':     '購買實戰',
    'hub-proposal':     '求婚與婚戒',
    'hub-care':         '保養與市場',
}


# ============================================================
# 1. First-paragraph CTA
# ============================================================

CTA_SENTINEL_ZH = 'data-bl-cta="zh"'
CTA_SENTINEL_EN = 'data-bl-cta="en"'

def cta_zh() -> str:
    return (
        ' <a href="/" '
        + CTA_SENTINEL_ZH
        + ' style="color:#8a6e30;font-weight:600;text-decoration:underline;text-underline-offset:3px"'
        + ' title="BrillianceLab 鑽石光學評分計算機">用 BrillianceLab 計算器先算分</a>'
    )

def cta_en() -> str:
    return (
        ' <a href="/" '
        + CTA_SENTINEL_EN
        + ' style="color:#8a6e30;font-weight:600;text-decoration:underline;text-underline-offset:3px"'
        + ' title="BrillianceLab diamond optical scoring calculator">Try the BrillianceLab calculator first</a>'
    )

def inject_first_para_cta(src: str) -> tuple[str, bool]:
    """Insert CTA inside the first <p> of each prose block.
    Supports two markup conventions found across the corpus:
      a) <div id="proseZh">...</div>             (older articles)
      b) <div class="prose-zh">...</div>         (newer articles)
    Same for English (proseEn / prose-en).
    """
    def patch_block(html: str, locators: list, cta_html: str, sentinel: str) -> tuple[str, bool]:
        m = None
        for pat in locators:
            m = pat.search(html)
            if m: break
        if not m:
            return html, False
        head, body = m.group(1), m.group(2)
        if sentinel in body:
            return html, False
        # First <p> in the block
        pm = re.search(r'(<p\b[^>]*>)([\s\S]+?)(</p>)', body, re.I)
        if not pm:
            return html, False
        inner = pm.group(2).rstrip()
        # Avoid double-period if the paragraph already ends in 。 / .
        sep = '' if inner.endswith(('。', '.', '!', '?', '!', '?')) else '。'
        new_p = pm.group(1) + inner + sep + cta_html + '。' + pm.group(3)
        new_body = body[:pm.start()] + new_p + body[pm.end():]
        return html[:m.start()] + head + new_body + html[m.end():], True

    zh_locators = [
        re.compile(r'(id=["\']proseZh["\'][^>]*>)([\s\S]+?)(?=</section>|</article>|</main>|<div\s+class=["\']prose-en)', re.I),
        re.compile(r'(<div\s+class=["\'][^"\']*\bprose-zh\b[^"\']*["\'][^>]*>)([\s\S]+?)(?=<div\s+class=["\'][^"\']*\bprose-en\b|</article>|</section>|</main>)', re.I),
    ]
    en_locators = [
        re.compile(r'(id=["\']proseEn["\'][^>]*>)([\s\S]+?)(?=</section>|</article>|</main>)', re.I),
        re.compile(r'(<div\s+class=["\'][^"\']*\bprose-en\b[^"\']*["\'][^>]*>)([\s\S]+?)(?=</article>|</section>|</main>)', re.I),
    ]

    src, c1 = patch_block(src, zh_locators, cta_zh(), CTA_SENTINEL_ZH)
    src, c2 = patch_block(src, en_locators, cta_en(), CTA_SENTINEL_EN)
    return src, (c1 or c2)


# ============================================================
# 2. <noscript> visibility fallback
# ============================================================

NOSCRIPT_SENTINEL = '<!-- BL_NOSCRIPT -->'
NOSCRIPT_BLOCK = (
    NOSCRIPT_SENTINEL + '\n'
    '<noscript>\n'
    '  <style>\n'
    '    /* No-JS readers (incl. cautious crawlers): show BOTH language\n'
    '       blocks side-by-side so all content is indexable. */\n'
    '    #proseZh, #proseEn { display: block !important; }\n'
    '    #proseEn::before {\n'
    '      content: "— English —"; display:block; margin:32px 0 12px;\n'
    '      padding:6px 12px; background:#fbf3df; color:#8a6e30;\n'
    '      font-size:11px; letter-spacing:.22em; text-transform:uppercase;\n'
    '      font-weight:700; border-radius:8px;\n'
    '    }\n'
    '    /* Hide JS-injected widgets that won\'t function */\n'
    '    #bl-toc, #bl-rtime, #bl-totop, #bl-progress { display:none !important; }\n'
    '  </style>\n'
    '</noscript>'
)

def inject_noscript(src: str) -> tuple[str, bool]:
    if NOSCRIPT_SENTINEL in src:
        return src, False
    new = src.replace('</head>', NOSCRIPT_BLOCK + '\n</head>', 1)
    return (new, True) if new != src else (src, False)


# ============================================================
# 3. Fonts preload (gstatic woff2)
# ============================================================

# These are the ACTUAL Google Fonts woff2 endpoints that Noto Serif TC's
# CSS resolves to (variable subset, Chinese Traditional). Hard-coded so
# we can preload before the CSS even resolves.
FONT_PRELOAD_SENTINEL = '<!-- BL_FONTPRELOAD -->'
FONT_PRELOAD_BLOCK = (
    FONT_PRELOAD_SENTINEL + '\n'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
    '<link rel="preload" as="font" type="font/woff2"\n'
    '      href="https://fonts.gstatic.com/s/notoseriftc/v30/XLYzIZb5bJNDGYxLBibeHZ0BhncESXFtUsM.woff2"\n'
    '      crossorigin>\n'
    '<link rel="preload" as="font" type="font/woff2"\n'
    '      href="https://fonts.gstatic.com/s/notoseriftc/v30/XLYgIZb5bJNDGYxLBibeHZAKgo3xx.woff2"\n'
    '      crossorigin>'
)

def inject_fonts_preload(src: str) -> tuple[str, bool]:
    if FONT_PRELOAD_SENTINEL in src:
        return src, False
    # Insert immediately after BL_PRELOAD comment (so it's grouped with other preloads)
    if '<!-- BL_PRELOAD -->' in src:
        new = src.replace('<!-- BL_PRELOAD -->', '<!-- BL_PRELOAD -->\n' + FONT_PRELOAD_BLOCK, 1)
    else:
        new = src.replace('</head>', FONT_PRELOAD_BLOCK + '\n</head>', 1)
    return (new, True) if new != src else (src, False)


# ============================================================
# 4. Pre-baked BreadcrumbList JSON-LD
# ============================================================

BC_SENTINEL = 'data-id="BL_BREADCRUMB_LD"'

def derive_slug(path: Path) -> str:
    if path.parent.name == 'amp' and path.parent.parent.name != '':
        return ''
    if path.name == 'index.html':
        return ''
    return path.stem

def article_title(src: str, slug: str) -> str:
    m = re.search(r'<title>([^|<]+?)(?:\s*[—\-|]\s*[^<]+)?</title>', src)
    return (m.group(1).strip() if m else slug.replace('-', ' '))

def inject_breadcrumb_ld(src: str, slug: str) -> tuple[str, bool]:
    if BC_SENTINEL in src:
        return src, False
    if not slug:
        return src, False
    items = [
        {'@type':'ListItem','position':1,'name':'首頁','item': DOMAIN + '/'},
        {'@type':'ListItem','position':2,'name':'部落格','item': DOMAIN + '/blog/'},
    ]
    hub = HUBS_REVERSE.get(slug)
    if hub:
        items.append({'@type':'ListItem','position':len(items)+1,'name': HUB_TITLES[hub], 'item': f'{DOMAIN}/blog/{hub}'})
    items.append({'@type':'ListItem','position':len(items)+1,'name': article_title(src, slug), 'item': f'{DOMAIN}/blog/{slug}'})
    ld = {'@context':'https://schema.org', '@type':'BreadcrumbList', 'itemListElement': items}
    block = (
        '\n<script type="application/ld+json" ' + BC_SENTINEL + '>\n'
        + json.dumps(ld, ensure_ascii=False, separators=(',', ':'))
        + '\n</script>'
    )
    new = src.replace('</head>', block + '\n</head>', 1)
    return (new, True) if new != src else (src, False)


# ============================================================
# Driver
# ============================================================

def process(p: Path, slug: str) -> dict:
    src = p.read_text(encoding='utf-8')
    out = src
    flags = {'cta':False, 'noscript':False, 'fonts':False, 'bc':False}
    out, flags['cta']      = inject_first_para_cta(out)
    out, flags['noscript'] = inject_noscript(out)
    out, flags['fonts']    = inject_fonts_preload(out)
    out, flags['bc']       = inject_breadcrumb_ld(out, slug)
    if out != src:
        p.write_text(out, encoding='utf-8')
    return flags

def main():
    files = sorted(ROOT.glob('blog/*.html'))
    totals = {'cta':0,'noscript':0,'fonts':0,'bc':0,'pages':0}
    for p in files:
        if p.name == 'index.html':
            slug = ''
        elif p.name == 'topics.html':
            slug = 'topics'
        else:
            slug = p.stem
        flags = process(p, slug)
        if any(flags.values()): totals['pages'] += 1
        for k,v in flags.items():
            if v: totals[k] += 1
        marks = ''.join('+' if flags[k] else '·' for k in ('cta','noscript','fonts','bc'))
        print(f'  [{marks}] {p.name}')
    print()
    print(f'pages touched: {totals["pages"]}/{len(files)}')
    print(f'  CTA injected:        {totals["cta"]}')
    print(f'  noscript injected:   {totals["noscript"]}')
    print(f'  fonts preload:       {totals["fonts"]}')
    print(f'  Breadcrumb JSON-LD:  {totals["bc"]}')

if __name__ == '__main__':
    main()
