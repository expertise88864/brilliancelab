# -*- coding: utf-8 -*-
"""
Inject <link rel="preload"> hints for the LCP-critical assets.

Preloads:
  - /assets/tw.css                                (Tailwind output)
  - /assets/fonts/NotoSerifTC-Regular.subset.woff2 (display headlines)
  - /assets/fonts/NotoSerifTC-Bold.subset.woff2

Idempotent — keyed off a sentinel comment.

Run AFTER build_fonts.py (so the font files exist) and switch_to_static_css.py
(so /assets/tw.css is referenced).
"""
from __future__ import annotations
import re
from pathlib import Path

# --- Auto-locate the repo root so this script can be run from anywhere ---
import os as _os, pathlib as _pl
_os.chdir(_pl.Path(__file__).resolve().parents[2])  # → BrillianceLab/
# -------------------------------------------------------------------------


ROOT = Path('.')
SENTINEL = '<!-- BL_PRELOAD -->'

PRELOAD = SENTINEL + '\n' + '\n'.join([
    '<link rel="preload" as="style" href="/assets/tw.css">',
    '<link rel="preload" as="font" type="font/woff2" href="/assets/fonts/NotoSerifTC-Regular.subset.woff2" crossorigin>',
    '<link rel="preload" as="font" type="font/woff2" href="/assets/fonts/NotoSerifTC-Bold.subset.woff2" crossorigin>',
    '<link rel="preconnect" href="https://pagead2.googlesyndication.com" crossorigin>',
    '<link rel="dns-prefetch" href="https://www.clarity.ms">',
])


def patch(path: Path) -> bool:
    src = path.read_text(encoding='utf-8')
    if SENTINEL in src:
        return False
    # Insert just after <meta charset>
    new = re.sub(r'(<meta\s+charset[^>]*>)\s*', r'\1\n' + PRELOAD + '\n', src, count=1)
    if new == src:
        return False
    path.write_text(new, encoding='utf-8')
    return True


def main():
    n = 0
    for p in sorted(list(ROOT.glob('*.html')) + list(ROOT.glob('blog/*.html'))):
        if patch(p):
            n += 1
            print(f'  preload added → {p}')
    print(f'\n{n} files patched')


if __name__ == '__main__':
    main()
