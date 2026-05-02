# -*- coding: utf-8 -*-
"""
Add loading="lazy" + decoding="async" to every <img> across the site.
The FIRST <img> per page (assumed to be the LCP candidate) gets
fetchpriority="high" + loading="eager" instead.

Re-run any time after adding new images. Idempotent.
"""
from __future__ import annotations
import re
from pathlib import Path

# --- Auto-locate the repo root so this script can be run from anywhere ---
import os as _os, pathlib as _pl
_os.chdir(_pl.Path(__file__).resolve().parents[2])  # → BrillianceLab/
# -------------------------------------------------------------------------


ROOT = Path('.')
IMG_RE = re.compile(r'<img\b([^>]*?)(/?)>', re.I | re.S)


def patch_img(attr_str: str, is_first: bool) -> str:
    a = attr_str
    has_loading       = re.search(r'\bloading\s*=', a, re.I)
    has_decoding      = re.search(r'\bdecoding\s*=', a, re.I)
    has_fetchpriority = re.search(r'\bfetchpriority\s*=', a, re.I)

    additions = ''
    if not has_decoding:
        additions += ' decoding="async"'
    if is_first:
        if not has_loading:        additions += ' loading="eager"'
        if not has_fetchpriority:  additions += ' fetchpriority="high"'
    else:
        if not has_loading:        additions += ' loading="lazy"'
    return a + additions


def process(path: Path) -> int:
    src = path.read_text(encoding='utf-8')
    counter = {'n': 0, 'first_done': False}

    def repl(m):
        attrs, slash = m.group(1), m.group(2)
        is_first = not counter['first_done']
        new_attrs = patch_img(attrs, is_first)
        counter['first_done'] = True
        counter['n'] += 1
        return f'<img{new_attrs}{slash}>'

    new = IMG_RE.sub(repl, src)
    if new != src:
        path.write_text(new, encoding='utf-8')
    return counter['n']


def main():
    total_files = 0
    total_imgs = 0
    for p in sorted(ROOT.rglob('*.html')):
        n = process(p)
        if n:
            total_imgs += n
            total_files += 1
            print(f'  hardened {n:>2} <img> in {p}')
    print(f'\n{total_imgs} <img> across {total_files} file(s)')


if __name__ == '__main__':
    main()
