# -*- coding: utf-8 -*-
"""
Audit every HTML file's <link rel="canonical"> against its actual on-disk path.
Self-references that don't match break the canonical signal — Google may pick
the wrong URL (or none) for the search result.

Reports:
  OK     canonical matches expected URL
  WRONG  canonical points elsewhere — investigate
  MULTI  multiple <link rel="canonical"> tags (must be one)
  MISS   no <link rel="canonical"> tag

Exits non-zero if any WRONG/MULTI/MISS.
"""
from __future__ import annotations
import re, sys
from pathlib import Path

# --- Auto-locate the repo root so this script can be run from anywhere ---
import os as _os
_os.chdir(Path(__file__).resolve().parents[2])  # → BrillianceLab/
# -------------------------------------------------------------------------

ROOT = Path('.')
DOMAIN = 'https://brilliancelab.vercel.app'

CANON_RE = re.compile(r'<link\s+[^>]*rel=["\']canonical["\'][^>]*>', re.I)
HREF_RE  = re.compile(r'href=["\']([^"\']+)["\']', re.I)


def expected_url(p: Path) -> str:
    """Map a file path to its public URL (no .html extension, trailing slash on dirs).

    AMP pages MUST canonical to the non-AMP version (per AMP spec):
        amp/blog/foo.html  →  /blog/foo  (NOT /amp/blog/foo)
    """
    rel = p.as_posix()
    if rel.endswith('blog/index.html'):
        return f'{DOMAIN}/blog/'
    if rel == 'index.html':
        return f'{DOMAIN}/'
    if rel == '404.html':
        return f'{DOMAIN}/404'
    if rel == 'search.html':
        return f'{DOMAIN}/search'
    # AMP rule: amp/blog/foo.html → /blog/foo
    if rel.startswith('amp/'):
        rel = rel[len('amp/'):]
    return f'{DOMAIN}/{rel.replace(".html", "")}'


def audit(p: Path) -> tuple[str, str]:
    src = p.read_text(encoding='utf-8')
    tags = CANON_RE.findall(src)
    if not tags:
        return ('MISS', 'no canonical tag')
    if len(tags) > 1:
        return ('MULTI', f'{len(tags)} canonical tags found')
    href_m = HREF_RE.search(tags[0])
    if not href_m:
        return ('WRONG', 'canonical tag has no href')
    actual = href_m.group(1).strip()
    expected = expected_url(p)
    if actual == expected:
        return ('OK', actual)
    return ('WRONG', f'has {actual!r} | expected {expected!r}')


def main():
    files = (
        list(ROOT.glob('*.html'))
        + list(ROOT.glob('blog/*.html'))
        + list(ROOT.glob('amp/blog/*.html'))
    )
    bad = 0
    counts = {'OK': 0, 'WRONG': 0, 'MISS': 0, 'MULTI': 0}
    rows = []
    for p in sorted(files):
        status, msg = audit(p)
        counts[status] += 1
        rows.append((status, p.as_posix(), msg))
        if status != 'OK':
            bad += 1

    # Print per-file: only show non-OK, plus a summary
    for status, path, msg in rows:
        if status != 'OK':
            print(f'  {status:<5} {path}  →  {msg}')
    print()
    print(f'Summary: OK {counts["OK"]} · WRONG {counts["WRONG"]} · MISS {counts["MISS"]} · MULTI {counts["MULTI"]}')
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
