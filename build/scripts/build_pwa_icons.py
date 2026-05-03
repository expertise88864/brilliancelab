# -*- coding: utf-8 -*-
"""
Generate PWA-quality raster icons + Apple touch icons + maskable variants from
the existing SVG diamond glyph, and update manifest.json to reference them.

Outputs (under assets/icons/):
  icon-192.png        — Android home screen (any)
  icon-512.png        — Android splash + larger displays (any)
  icon-maskable-192.png  — same artwork on a generous gold-soft safe-area pad
  icon-maskable-512.png
  apple-touch-icon.png   180×180 — iOS home screen

Why we don't keep just the SVG: Lighthouse PWA audit + iOS/Android stores still
reach for raster icons. Maskable PNGs are required for Android adaptive icons.
"""
from __future__ import annotations
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import json

# --- Auto-locate the repo root so this script can be run from anywhere ---
import os as _os
_os.chdir(Path(__file__).resolve().parents[2])  # → BrillianceLab/
# -------------------------------------------------------------------------

ROOT  = Path('.')
OUT   = ROOT / 'assets' / 'icons'

# Brand colours (mirror tailwind.config.js)
BG_SOFT  = (251, 243, 223)
GOLD     = (201, 164, 92)
GOLD_DEEP= (138, 110, 48)
INK      = (26, 29, 46)
INK_DEEP = (10, 12, 22)


def diamond(size: int, fill: tuple, shadow: tuple, padding_ratio: float = 0.0) -> Image.Image:
    """Render a stylised diamond on a transparent canvas. padding_ratio shrinks
    the glyph so a maskable icon's safe area survives Android's 80% mask."""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    p = padding_ratio * size
    s = size - 2 * p
    cx = size / 2
    # Crown (upper triangle)
    crown = [
        (cx,            p + s * 0.05),
        (p + s * 0.05,  p + s * 0.40),
        (p + s * 0.95,  p + s * 0.40),
    ]
    # Pavilion (lower triangle)
    pav = [
        (p + s * 0.05,  p + s * 0.40),
        (p + s * 0.95,  p + s * 0.40),
        (cx,            p + s * 0.95),
    ]
    d.polygon(crown, fill=fill)
    d.polygon(pav,   fill=shadow)
    # Facet hint — vertical line down the middle of the pavilion
    d.line([(cx, p + s * 0.40), (cx, p + s * 0.95)], fill=tuple(int(c * 0.55) for c in shadow), width=max(1, size // 200))
    # Outline
    d.polygon([crown[0], crown[1], pav[2], crown[2]], outline=tuple(int(c * 0.45) for c in fill), width=max(1, size // 350))
    return img


def render(size: int, maskable: bool = False) -> Image.Image:
    bg = Image.new('RGB', (size, size), BG_SOFT if maskable else (255, 255, 255))
    # Soft background glow
    glow = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([size * 0.1, size * 0.15, size * 0.9, size * 0.95], fill=(201, 164, 92, 50))
    glow = glow.filter(ImageFilter.GaussianBlur(size // 16))
    bg.paste(glow, (0, 0), glow)
    # Diamond — maskable needs ~20% safe padding so Android's mask doesn't crop it
    pad = 0.16 if maskable else 0.06
    glyph = diamond(size, GOLD, GOLD_DEEP, padding_ratio=pad)
    bg.paste(glyph, (0, 0), glyph)
    return bg


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    targets = [
        ('icon-192.png',          192, False),
        ('icon-512.png',          512, False),
        ('icon-maskable-192.png', 192, True),
        ('icon-maskable-512.png', 512, True),
        ('apple-touch-icon.png',  180, False),
    ]
    for name, size, maskable in targets:
        p = OUT / name
        render(size, maskable=maskable).save(p, 'PNG', optimize=True)
        print(f'  wrote {p.relative_to(ROOT).as_posix()}  ({p.stat().st_size // 1024} KB)')

    # Patch manifest.json
    mf = ROOT / 'manifest.json'
    data = json.loads(mf.read_text(encoding='utf-8'))
    data['icons'] = [
        {'src': '/assets/icons/icon-192.png',          'sizes': '192x192', 'type': 'image/png', 'purpose': 'any'},
        {'src': '/assets/icons/icon-512.png',          'sizes': '512x512', 'type': 'image/png', 'purpose': 'any'},
        {'src': '/assets/icons/icon-maskable-192.png', 'sizes': '192x192', 'type': 'image/png', 'purpose': 'maskable'},
        {'src': '/assets/icons/icon-maskable-512.png', 'sizes': '512x512', 'type': 'image/png', 'purpose': 'maskable'},
        {'src': '/icon.svg',                            'sizes': 'any',     'type': 'image/svg+xml', 'purpose': 'any'},
    ]
    mf.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'\n  patched manifest.json with 5 icon entries')

    # Patch index.html / blog header — add apple-touch-icon link if missing
    apple_link = '<link rel="apple-touch-icon" sizes="180x180" href="/assets/icons/apple-touch-icon.png">'
    for p in [ROOT / 'index.html', ROOT / 'blog' / 'index.html']:
        if not p.exists(): continue
        src = p.read_text(encoding='utf-8')
        if 'apple-touch-icon' in src and 'apple-touch-icon.png' in src:
            continue
        # Replace existing apple-touch-icon (SVG) or insert before </head>
        import re
        new = re.sub(
            r'<link\s+rel=["\']apple-touch-icon["\'][^>]*>\s*',
            apple_link + '\n', src)
        if new == src:
            new = src.replace('</head>', '  ' + apple_link + '\n</head>', 1)
        if new != src:
            p.write_text(new, encoding='utf-8')
            print(f'  patched {p.relative_to(ROOT).as_posix()} apple-touch-icon link')


if __name__ == '__main__':
    main()
