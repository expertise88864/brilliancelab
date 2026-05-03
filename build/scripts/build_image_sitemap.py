# -*- coding: utf-8 -*-
"""
Build a separate image sitemap (og-sitemap.xml) listing every per-article
OG image so Google Image Search can crawl and attribute them. Append the
new sitemap to the existing sitemap index in robots.txt.
"""
from __future__ import annotations
from pathlib import Path

# --- Auto-locate the repo root so this script can be run from anywhere ---
import os as _os
_os.chdir(Path(__file__).resolve().parents[2])  # → BrillianceLab/
# -------------------------------------------------------------------------

ROOT   = Path('.')
DOMAIN = 'https://brilliancelab.vercel.app'

OG_DIR = ROOT / 'og'

# Slug → article URL mapping
def page_url(slug: str) -> str:
    if slug.startswith('hub-'):
        return f'{DOMAIN}/blog/{slug}'
    return f'{DOMAIN}/blog/{slug}'

def caption_for(slug: str) -> str:
    # Mirror the curated subtitles from build_og_images.py
    return slug.replace('-', ' ').title()

def main():
    all_pngs = sorted(p for p in OG_DIR.glob('*.png') if p.is_file())
    if not all_pngs:
        print('No OG PNGs found — run build_og_images.py first.')
        return
    # Prefer hashed PNGs (`<slug>.<hash>.png`) over legacy un-hashed (`<slug>.png`).
    # `<slug>.png` is kept on disk only as a fallback for old external links;
    # we don't want it duplicated in the image sitemap.
    by_slug = {}
    for p in all_pngs:
        parts = p.stem.split('.')
        slug = parts[0] if len(parts) == 1 else '.'.join(parts[:-1])
        # Keep the hashed one if we ever see one
        if slug not in by_slug or len(p.stem.split('.')) > 1:
            by_slug[slug] = p
    pngs = sorted(by_slug.values(), key=lambda p: p.name)

    out = ROOT / 'og-sitemap.xml'
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
        '        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">',
    ]
    for p in pngs:
        # Strip hash suffix from filename for slug derivation
        parts = p.stem.split('.')
        slug = parts[0] if len(parts) == 1 else '.'.join(parts[:-1])
        page = page_url(slug)
        img_url = f'{DOMAIN}/og/{p.name}'
        lines += [
            '  <url>',
            f'    <loc>{page}</loc>',
            '    <image:image>',
            f'      <image:loc>{img_url}</image:loc>',
            f'      <image:title>{caption_for(slug)} | BrillianceLab</image:title>',
            f'      <image:caption>BrillianceLab article OG image — {slug}</image:caption>',
            '    </image:image>',
            '  </url>',
        ]
    lines.append('</urlset>')
    out.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'  wrote og-sitemap.xml with {len(pngs)} image entries')

    # Update robots.txt to point Googlebot to the new sitemap
    robots = ROOT / 'robots.txt'
    if robots.exists():
        src = robots.read_text(encoding='utf-8')
        line = f'Sitemap: {DOMAIN}/og-sitemap.xml'
        if line not in src:
            new = src.rstrip() + '\n' + line + '\n'
            robots.write_text(new, encoding='utf-8')
            print(f'  added {line} to robots.txt')
        else:
            print('  robots.txt already references og-sitemap.xml')


if __name__ == '__main__':
    main()
