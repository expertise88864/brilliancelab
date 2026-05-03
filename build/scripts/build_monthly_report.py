# -*- coding: utf-8 -*-
"""
Generate a monthly diamond-market roundup HTML page from Google News RSS.

Pulls the latest 30 days of headlines for 6 curated queries (鑽石市場, GIA,
培育鑽石, De Beers, lab grown diamond, Tiffany Cartier earnings), groups them
into 4 sections, and scaffolds /blog/diamond-news-YYYY-MM.html with full
template (head, schema, hub-link, ads, etc.). The headline + link + 1-line
summary is auto-extracted; commentary blocks are left as TODO for you to fill.

Run:
  python build/scripts/build_monthly_report.py             # current month
  python build/scripts/build_monthly_report.py --month 2026-06  # specific
  python build/scripts/build_monthly_report.py --dry       # preview only

Requires only stdlib (no requests). Network call goes to news.google.com RSS.
"""
from __future__ import annotations
import argparse, datetime as dt, html, json, re, sys, urllib.parse, urllib.request
from pathlib import Path
from xml.etree import ElementTree as ET

# --- Auto-locate the repo root so this script can be run from anywhere ---
import os as _os
_os.chdir(Path(__file__).resolve().parents[2])  # → BrillianceLab/
# -------------------------------------------------------------------------

try: sys.stdout.reconfigure(encoding='utf-8')
except Exception: pass

ROOT   = Path('.')
DOMAIN = 'https://brilliancelab.vercel.app'

# 4 sections × 1-2 query each. Add/remove as taste dictates.
SECTIONS = [
    {
        'id': 'market',
        'title': '市場 · 價格與景氣',
        'queries': ['鑽石價格 OR 鑽石市場', 'diamond market 2026'],
    },
    {
        'id': 'lab-grown',
        'title': '培育鑽石 · 技術與滲透率',
        'queries': ['培育鑽石 OR lab grown diamond', 'CVD diamond OR HPHT diamond'],
    },
    {
        'id': 'industry',
        'title': '產業 · 品牌與供應鏈',
        'queries': ['De Beers earnings', 'Tiffany OR Cartier 鑽石'],
    },
    {
        'id': 'policy',
        'title': '政策 · 監管與證書',
        'queries': ['GIA 證書 OR Kimberley Process', 'EU diamond regulation'],
    },
]


def fetch_rss(query: str, max_n: int = 8) -> list[dict]:
    """Pull Google News RSS — returns list of {title, link, pubDate, source}."""
    encoded = urllib.parse.quote(query)
    url = f'https://news.google.com/rss/search?q={encoded}+when:30d&hl=zh-TW&gl=TW&ceid=TW:zh-Hant'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (BrillianceLab/build)'})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            xml = r.read()
    except Exception as e:
        print(f'  WARN  fetch failed for {query!r}: {e}')
        return []

    items = []
    try:
        root = ET.fromstring(xml)
        for item in root.findall('.//item')[:max_n]:
            title = (item.findtext('title') or '').strip()
            link  = (item.findtext('link')  or '').strip()
            date  = (item.findtext('pubDate') or '').strip()
            source = item.find('source')
            src_name = source.text if source is not None else ''
            # Strip trailing source from title (Google News appends "- Reuters")
            title = re.sub(r'\s*-\s*[^\-]+$', '', title).strip()
            items.append({'title': title, 'link': link, 'pubDate': date, 'source': src_name})
    except ET.ParseError as e:
        print(f'  WARN  parse error for {query!r}: {e}')
    return items


def dedupe(items: list[dict]) -> list[dict]:
    seen_titles = set()
    out = []
    for it in items:
        # Use first 18 chars as dedup key (titles often vary by source suffix)
        key = it['title'][:18]
        if key in seen_titles: continue
        seen_titles.add(key)
        out.append(it)
    return out


def render_section(sec: dict, items: list[dict]) -> str:
    if not items:
        return f'''  <h2 id="sec-{sec['id']}">{html.escape(sec['title'])}</h2>
  <p style="color:#7e8194;font-style:italic">本月暫無重大新聞。</p>'''
    rows = []
    for i, it in enumerate(items[:6], 1):
        title = html.escape(it['title'])
        link  = html.escape(it['link'])
        src   = html.escape(it['source'])
        rows.append(
            f'  <li class="news-item">'
            f'<a href="{link}" target="_blank" rel="noopener nofollow"><strong>{title}</strong></a>'
            f' <span class="news-src">— {src}</span>'
            f'</li>'
        )
    return f'''  <h2 id="sec-{sec['id']}">{html.escape(sec['title'])}</h2>
  <ul class="news-list">
{chr(10).join(rows)}
  </ul>
  <p class="commentary"><em>編輯觀點(請補):</em> TODO — 用 2-3 句話總結這個月這條 silo 的趨勢和對買鑽人的實際影響。</p>'''


TEMPLATE = '''<!doctype html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8" />
<!-- BL_PRELOAD -->
<link rel="preload" as="style" href="/assets/tw.css">
<link rel="preload" as="font" type="font/woff2" href="/assets/fonts/NotoSerifTC-Regular.subset.woff2" crossorigin>
<link rel="preload" as="font" type="font/woff2" href="/assets/fonts/NotoSerifTC-Bold.subset.woff2" crossorigin>
<link rel="preconnect" href="https://pagead2.googlesyndication.com" crossorigin>
<link rel="dns-prefetch" href="https://www.clarity.ms">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover" />
<title>{title}</title>
<meta name="description" content="{description}" />
<meta name="theme-color" content="#faf8f3" />
<link rel="canonical" href="{canonical}" />
<link rel="alternate" hreflang="x-default" href="{canonical}" />
<link rel="alternate" hreflang="zh-TW" href="{canonical}" />
<link rel="alternate" type="application/rss+xml" title="BrillianceLab Blog RSS" href="/blog/feed.xml" />
<link rel="icon" type="image/svg+xml" href="/icon.svg" />

<meta property="og:type" content="article" />
<meta property="og:url" content="{canonical}" />
<meta property="og:title" content="{title}" />
<meta property="og:description" content="{description}" />
<meta property="og:image" content="{og_image}" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="{title}" />
<meta name="twitter:description" content="{description}" />
<meta name="twitter:image" content="{og_image}" />

<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-8223268344248663" crossorigin="anonymous"></script>
<meta name="google-adsense-account" content="ca-pub-8223268344248663" />
<script src="https://cdn.tailwindcss.com"></script>
<style>
  :root{{--bg:#faf8f3;--ink:#1a1d2e;--ink-2:#4a4d5e;--muted:#7e8194;--gold:#c9a45c;--gold-deep:#8a6e30;--gold-soft:#fbf3df;--border:#ebe6dc;}}
  *{{box-sizing:border-box;margin:0;padding:0;}}
  html,body{{background:var(--bg);color:var(--ink);font-family:Inter,'Noto Serif TC','Microsoft JhengHei',Georgia,serif;line-height:1.85;}}
  body::before{{content:'';position:fixed;inset:0;pointer-events:none;z-index:-1;background:radial-gradient(800px 500px at 12% -8%,rgba(201,164,92,.16),transparent 60%),linear-gradient(180deg,#faf8f3 0%,#fffdf7 40%,#faf8f3 100%);}}
  .gold-text{{background:linear-gradient(180deg,#c9a45c,#8a6e30);-webkit-background-clip:text;background-clip:text;color:transparent;}}
  header.sticky{{position:sticky;top:0;background:rgba(250,248,243,.92);backdrop-filter:blur(10px);border-bottom:1px solid var(--border);z-index:10;padding:14px 24px;display:flex;align-items:center;justify-content:space-between;}}
  main{{max-width:780px;margin:0 auto;padding:32px 24px 80px;}}
  h1{{font-family:'Noto Serif TC',Georgia,serif;font-size:clamp(28px,4.5vw,42px);font-weight:800;line-height:1.2;margin-bottom:14px;}}
  h2{{font-family:'Noto Serif TC',Georgia,serif;font-size:22px;font-weight:700;border-left:3px solid var(--gold);padding-left:12px;margin:36px 0 14px;}}
  .lead{{font-size:16px;color:var(--ink-2);margin-bottom:20px;}}
  .meta{{font-size:12.5px;color:var(--muted);padding-bottom:16px;border-bottom:1px dashed var(--border);margin-bottom:24px;}}
  .news-list{{list-style:none;padding:0;display:flex;flex-direction:column;gap:10px;}}
  .news-item{{padding:12px 14px;background:#fff;border:1px solid var(--border);border-radius:10px;transition:border-color .2s;}}
  .news-item:hover{{border-color:rgba(201,164,92,.55);}}
  .news-item a{{color:var(--ink);text-decoration:none;}}
  .news-item a:hover strong{{color:var(--gold-deep);}}
  .news-src{{font-size:12px;color:var(--muted);}}
  .commentary{{margin-top:14px;padding:14px;background:var(--gold-soft);border-radius:8px;font-size:14px;color:var(--ink-2);line-height:1.7;}}
</style>

<script type="application/ld+json">
{schema}
</script>
</head>
<body>

<header class="sticky">
  <a href="/" style="text-decoration:none;color:inherit;display:inline-flex;align-items:center;gap:8px">
    <svg viewBox="0 0 24 24" width="22" height="22" fill="none"><path d="M3.5 9 12 3l8.5 6-8.5 12L3.5 9Z" stroke="url(#g)" stroke-width="1.4" stroke-linejoin="round"/><defs><linearGradient id="g" x1="0" x2="1" y1="0" y2="1"><stop stop-color="#d4b87a"/><stop offset="1" stop-color="#8a6e30"/></linearGradient></defs></svg>
    <span class="gold-text" style="font-weight:700">BrillianceLab</span>
  </a>
  <nav style="font-size:12px;letter-spacing:.18em;text-transform:uppercase;color:var(--ink-2)">
    <a href="/blog/" style="color:inherit;text-decoration:none;margin:0 10px">部落格</a>
    <a href="/blog/topics" style="color:inherit;text-decoration:none;margin:0 10px">主題</a>
  </nav>
</header>

<main>
  <nav style="font-size:11px;letter-spacing:.22em;text-transform:uppercase;color:var(--muted);margin-bottom:8px" aria-label="Breadcrumb">
    <a href="/" style="color:inherit;text-decoration:none">首頁</a> · <a href="/blog/" style="color:inherit;text-decoration:none">部落格</a> · <span style="color:var(--gold-deep)">{ym} 鑽石市場月報</span>
  </nav>
  <h1>{title}</h1>
  <p class="lead">本月鑽石市場 4 大主題自動彙整 — 共 {n_items} 條精選新聞,加上編輯觀點與對買鑽消費者的實際影響。</p>
  <div class="meta">最後更新:{today} · 自動匯整自 Google News · TODO 將每段「編輯觀點」補上</div>

  <article id="proseZh" data-pagefind-body data-pagefind-meta="slug:diamond-news-{ym}" class="prose-zh">
{sections}
  </article>
</main>

<script src="/blog/blog-shared.js" defer></script>
<script defer>document.addEventListener('DOMContentLoaded', () => BL.initBlog({{ slug:'diamond-news-{ym}' }}));</script>
</body>
</html>
'''


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--month', help='YYYY-MM (default: current)')
    ap.add_argument('--dry', action='store_true', help='preview, do not write')
    args = ap.parse_args()

    today = dt.date.today()
    if args.month:
        ym = args.month
        y, m = map(int, ym.split('-'))
    else:
        y, m = today.year, today.month
        ym = f'{y:04d}-{m:02d}'

    print(f'building monthly report for {ym} …')
    sections_html = []
    total_items = 0
    for sec in SECTIONS:
        items = []
        for q in sec['queries']:
            items.extend(fetch_rss(q, max_n=6))
        items = dedupe(items)[:6]
        print(f'  [{sec["id"]:>10}]  {len(items)} items')
        total_items += len(items)
        sections_html.append(render_section(sec, items))

    slug = f'diamond-news-{ym}'
    title = f'{ym} 鑽石市場月報 — 培育鑽 · GIA · De Beers'
    description = f'{ym} 鑽石市場 30 天精選 — 培育鑽滲透率、價格動向、品牌新聞、政策更新,共 {total_items} 則新聞 + 編輯解讀。'
    canonical = f'{DOMAIN}/blog/{slug}'
    og_image = f'{DOMAIN}/og/{slug}.png'

    schema = json.dumps({
        '@context': 'https://schema.org',
        '@type':    'Article',
        'headline': title,
        'description': description,
        'datePublished': str(today),
        'dateModified':  str(today),
        'author':    {'@id': f'{DOMAIN}/#editorial-team'},
        'publisher': {'@id': f'{DOMAIN}/#organization'},
        'image':     og_image,
        'mainEntityOfPage': canonical,
        'inLanguage': 'zh-TW',
        'isAccessibleForFree': True,
    }, ensure_ascii=False, separators=(',', ':'))

    out = TEMPLATE.format(
        title=title, description=description, canonical=canonical, og_image=og_image,
        schema=schema, sections='\n\n'.join(sections_html),
        ym=ym, today=str(today), n_items=total_items,
    )

    target = ROOT / 'blog' / f'{slug}.html'
    if args.dry:
        print(f'\n--- DRY-RUN ({len(out)} chars to {target}) ---\n')
        print(out[:1500])
        return
    target.write_text(out, encoding='utf-8')
    print(f'\nwrote {target.relative_to(ROOT).as_posix()}')
    print(f'next steps:')
    print(f'  1. fill in TODO commentary blocks')
    print(f'  2. python build/scripts/build_og_images.py        # generate OG image')
    print(f'  3. python build/scripts/build_sitemap_split.py    # add to sitemap')
    print(f'  4. python build/scripts/ping_indexnow.py /blog/{slug}')


if __name__ == '__main__':
    main()
