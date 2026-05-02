# -*- coding: utf-8 -*-
"""
Replace the Tailwind CDN dev runtime + inline tailwind.config with a single
preloaded <link> to ./assets/tw.css. Run AFTER `npm run css:build` succeeds.

Idempotent — safe to re-run. Backs up each file with a `.bak` suffix the first
time it's modified, so you can revert with `mv FILE.bak FILE`.
"""
from __future__ import annotations
import re, shutil
from pathlib import Path

# --- Auto-locate the repo root so this script can be run from anywhere ---
import os as _os, pathlib as _pl
_os.chdir(_pl.Path(__file__).resolve().parents[2])  # → BrillianceLab/
# -------------------------------------------------------------------------


ROOT = Path('.')

# Patterns for the two pieces of Tailwind CDN bootstrap
CDN_TAG_RE = re.compile(r'<script\s+src=["\']https://cdn\.tailwindcss\.com["\'][^>]*></script>\s*', re.I)
TW_CONFIG_RE = re.compile(r'<script>\s*tailwind\.config\s*=[\s\S]*?</script>\s*', re.I)

REPLACEMENT = (
    '<link rel="preload" as="style" href="/assets/tw.css">\n'
    '<link rel="stylesheet" href="/assets/tw.css">\n'
)


def patch(path: Path) -> bool:
    src = path.read_text(encoding='utf-8')
    has_cdn  = bool(CDN_TAG_RE.search(src))
    has_conf = bool(TW_CONFIG_RE.search(src))
    if not has_cdn and not has_conf:
        return False
    if not path.with_suffix(path.suffix + '.bak').exists():
        shutil.copy2(path, path.with_suffix(path.suffix + '.bak'))
    new = src
    if has_cdn:
        new = CDN_TAG_RE.sub(REPLACEMENT, new, count=1)
    if has_conf:
        new = TW_CONFIG_RE.sub('', new, count=1)
    if new != src:
        path.write_text(new, encoding='utf-8')
        return True
    return False


def main():
    n = 0
    for p in sorted(list(ROOT.glob('*.html')) + list(ROOT.rglob('blog/*.html'))):
        if patch(p):
            n += 1
            print(f'  patched {p}')
    print(f'\n{n} file(s) switched to static tw.css')
    if n == 0:
        print('Nothing to do — run `npm run css:build` first, then re-run this.')


if __name__ == '__main__':
    main()
