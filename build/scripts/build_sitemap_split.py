# -*- coding: utf-8 -*-
"""
Split the monolithic sitemap.xml into 4 child sitemaps + a sitemap-index:

  /sitemap.xml           — sitemap index (lists all child sitemaps)
  /sitemap-pages.xml     — top-level pages (/, /search, hubs)
  /sitemap-articles.xml  — every regular blog article
  /sitemap-amp.xml       — AMP variants
  /og-sitemap.xml        — image sitemap (already built by build_image_sitemap.py)

Why split: Search Console reports indexing status PER sitemap. Splitting lets
you see at a glance "20/35 articles indexed but only 1/5 hubs" — much faster
diagnosis than one giant 53-URL sitemap.

Each child sitemap retains the xhtml:link hreflang block per URL.
"""
from __future__ import annotations
from pathlib import Path

# --- Auto-locate the repo root so this script can be run from anywhere ---
import os as _os
_os.chdir(Path(__file__).resolve().parents[2])  # → BrillianceLab/
# -------------------------------------------------------------------------

ROOT   = Path('.')
DOMAIN = 'https://brilliancelab.vercel.app'
LANGS  = ['x-default','zh-Hant','zh-TW','zh-Hans','zh-CN','en','ja','ko','th','vi','de','fr','es']
LASTMOD = '2026-05-03'


def url_block(loc: str, changefreq: str, priority: str) -> str:
    lines = ['  <url>', f'    <loc>{loc}</loc>',
             f'    <lastmod>{LASTMOD}</lastmod>',
             f'    <changefreq>{changefreq}</changefreq>',
             f'    <priority>{priority}</priority>']
    for L in LANGS:
        lines.append(f'    <xhtml:link rel="alternate" hreflang="{L}" href="{loc}" />')
    lines.append('  </url>')
    return '\n'.join(lines)


def write_sitemap(path: Path, urls: list[tuple[str,str,str]]):
    body = ['<?xml version="1.0" encoding="UTF-8"?>',
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
            '        xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for loc, freq, prio in urls:
        body.append(url_block(loc, freq, prio))
    body.append('</urlset>')
    path.write_text('\n'.join(body) + '\n', encoding='utf-8')


def main():
    # --- pages: top-level ---
    pages_urls = [
        (f'{DOMAIN}/',                  'weekly',  '1.0'),
        (f'{DOMAIN}/blog/',             'weekly',  '0.95'),
        (f'{DOMAIN}/search',            'monthly', '0.7'),
        (f'{DOMAIN}/blog/topics',       'weekly',  '0.85'),
        (f'{DOMAIN}/blog/hub-fundamentals', 'weekly', '0.95'),
        (f'{DOMAIN}/blog/hub-4cs',          'weekly', '0.95'),
        (f'{DOMAIN}/blog/hub-purchase',     'weekly', '0.95'),
        (f'{DOMAIN}/blog/hub-proposal',     'weekly', '0.95'),
        (f'{DOMAIN}/blog/hub-care',         'weekly', '0.95'),
    ]

    # --- articles: scan blog/ excluding index/topics/hubs/feed ---
    excluded = {'index', 'topics', 'feed'}
    article_urls = []
    for p in sorted(ROOT.glob('blog/*.html')):
        slug = p.stem
        if slug in excluded or slug.startswith('hub-'):
            continue
        prio = '0.95' if slug == 'master-guide' else '0.9'
        article_urls.append((f'{DOMAIN}/blog/{slug}', 'monthly', prio))

    # --- AMP ---
    amp_urls = []
    for p in sorted(ROOT.glob('amp/blog/*.html')):
        amp_urls.append((f'{DOMAIN}/amp/blog/{p.stem}', 'monthly', '0.7'))

    write_sitemap(ROOT / 'sitemap-pages.xml',    pages_urls)
    write_sitemap(ROOT / 'sitemap-articles.xml', article_urls)
    write_sitemap(ROOT / 'sitemap-amp.xml',      amp_urls)

    # --- sitemap index ---
    idx_lines = ['<?xml version="1.0" encoding="UTF-8"?>',
                 '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for fn in ['sitemap-pages.xml', 'sitemap-articles.xml', 'sitemap-amp.xml', 'og-sitemap.xml']:
        if (ROOT / fn).exists():
            idx_lines += [f'  <sitemap>',
                          f'    <loc>{DOMAIN}/{fn}</loc>',
                          f'    <lastmod>{LASTMOD}</lastmod>',
                          '  </sitemap>']
    idx_lines.append('</sitemapindex>')
    (ROOT / 'sitemap.xml').write_text('\n'.join(idx_lines) + '\n', encoding='utf-8')

    print(f'  sitemap-pages.xml:     {len(pages_urls)} URLs')
    print(f'  sitemap-articles.xml:  {len(article_urls)} URLs')
    print(f'  sitemap-amp.xml:       {len(amp_urls)} URLs')
    print(f'  sitemap.xml (index):   {sum((ROOT / fn).exists() for fn in ["sitemap-pages.xml","sitemap-articles.xml","sitemap-amp.xml","og-sitemap.xml"])} child sitemaps')

    # robots.txt should now point to the index, not individual sitemaps
    robots = ROOT / 'robots.txt'
    if robots.exists():
        src = robots.read_text(encoding='utf-8')
        # Strip all existing Sitemap: lines, then add the canonical index
        new = '\n'.join(line for line in src.split('\n') if not line.startswith('Sitemap:'))
        new = new.rstrip() + f'\n\nSitemap: {DOMAIN}/sitemap.xml\n'
        robots.write_text(new, encoding='utf-8')
        print(f'  robots.txt: now references sitemap index only')


if __name__ == '__main__':
    main()
