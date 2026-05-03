# -*- coding: utf-8 -*-
"""
Inject a centralised Person + Organization JSON-LD block (with `sameAs` social
profile slots) into every blog article. Existing Article schemas can then
reference the @id, which gives Google a single canonical author entity to
attribute every post to — boosting E-E-A-T signals.

The placeholder URLs in `SAMEAS_*` are clearly labelled. Edit them once you
have real profiles, then re-run this script — it's idempotent (keyed on
`data-id="BL_AUTHOR_SCHEMA"`).
"""
from __future__ import annotations
import json, re
from pathlib import Path

# --- Auto-locate the repo root so this script can be run from anywhere ---
import os as _os
_os.chdir(Path(__file__).resolve().parents[2])  # → BrillianceLab/
# -------------------------------------------------------------------------

ROOT = Path('.')
DOMAIN = 'https://brilliancelab.vercel.app'

# Replace these once you create the actual profiles. Empty strings are filtered
# out so an unfilled placeholder doesn't break the schema.
SAMEAS_ORG = [
    # 'https://twitter.com/brilliancelab',
    # 'https://github.com/cyc09180/brilliancelab',
    # 'https://www.threads.net/@brilliancelab',
    # 'https://www.linkedin.com/company/brilliancelab',
]
SAMEAS_PERSON = [
    # 'https://twitter.com/brilliancelab_editor',
]

ORG = {
    '@context': 'https://schema.org',
    '@type':    'Organization',
    '@id':      f'{DOMAIN}/#organization',
    'name':     'BrillianceLab',
    'alternateName': ['鑽石實驗室', 'Diamond Math Calculator'],
    'url':      DOMAIN + '/',
    'logo': {
        '@type':  'ImageObject',
        '@id':    f'{DOMAIN}/#logo',
        'url':    f'{DOMAIN}/icon.svg',
        'contentUrl': f'{DOMAIN}/icon.svg',
        'width':  512, 'height': 512,
        'caption':'BrillianceLab',
    },
    'image':       {'@id': f'{DOMAIN}/#logo'},
    'description': '基於 Tolkowsky 黃金比例與 HCA 4 維光學分解的免費鑽石評分工具。',
    'foundingDate': '2025',
    'knowsAbout': [
        'GIA grading','HCA optical scoring','Tolkowsky diamond design',
        'Hearts and Arrows','lab-grown diamonds','engagement rings'
    ],
    'sameAs': [u for u in SAMEAS_ORG if u],
}

PERSON = {
    '@context': 'https://schema.org',
    '@type':    'Person',
    '@id':      f'{DOMAIN}/#editorial-team',
    'name':     'BrillianceLab Editorial',
    'url':      DOMAIN + '/',
    'jobTitle': 'Editorial team',
    'worksFor': {'@id': f'{DOMAIN}/#organization'},
    'image':    {'@id': f'{DOMAIN}/#logo'},
    'knowsAbout': [
        'diamond grading','GIA report interpretation','optical scoring',
        'Hearts and Arrows symmetry','engagement ring purchase','wedding bands'
    ],
    'sameAs': [u for u in SAMEAS_PERSON if u],
}

GRAPH = {
    '@context': 'https://schema.org',
    '@graph': [ORG, PERSON],
}

SENTINEL = 'data-id="BL_AUTHOR_SCHEMA"'
BLOCK = (
    '\n<script type="application/ld+json" ' + SENTINEL + '>\n'
    + json.dumps(GRAPH, ensure_ascii=False, separators=(',', ':'))
    + '\n</script>'
)


def patch(path: Path) -> bool:
    src = path.read_text(encoding='utf-8')
    if SENTINEL in src:
        # Replace existing block in place (idempotent updates)
        new = re.sub(
            r'\n?<script[^>]*' + re.escape(SENTINEL) + r'[^>]*>[\s\S]*?</script>',
            BLOCK, src, count=1)
    else:
        new = src.replace('</head>', BLOCK + '\n</head>', 1)
    if new != src:
        path.write_text(new, encoding='utf-8')
        return True
    return False


def main():
    files = (
        list(ROOT.glob('blog/*.html'))
        + [ROOT / 'index.html', ROOT / 'search.html', ROOT / '404.html']
    )
    n = 0
    for p in files:
        if not p.exists(): continue
        if patch(p):
            n += 1
            print(f'  patched {p.relative_to(ROOT).as_posix()}')
    print(f'\n{n} file(s) updated with Person + Organization schema')
    if not (SAMEAS_ORG or SAMEAS_PERSON):
        print('NOTE: SAMEAS_ORG / SAMEAS_PERSON are empty — fill them in this script and re-run')
        print('      to get sameAs E-E-A-T signals (Twitter / GitHub / LinkedIn etc.).')


if __name__ == '__main__':
    main()
