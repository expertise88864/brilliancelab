# -*- coding: utf-8 -*-
"""
Submit URLs to the IndexNow API (Bing, Yandex, Seznam, Naver share the same
endpoint). Fast: typical indexing happens within hours instead of days.

Spec: https://www.indexnow.org/documentation

Usage:

  # Submit every URL listed in sitemap.xml + child sitemaps:
  python ping_indexnow.py --all

  # Submit specific URLs (one per arg):
  python ping_indexnow.py /blog/diamond-news-2026 /blog/master-guide

  # Dry-run (print payload, don't POST):
  python ping_indexnow.py --all --dry

The site's IndexNow key file lives at /<KEY>.txt — Bing fetches it to verify
ownership before accepting submissions. The key + filename are below.
"""
from __future__ import annotations
import argparse, json, sys, urllib.request, urllib.error, re
from pathlib import Path

# --- Auto-locate the repo root so this script can be run from anywhere ---
import os as _os
_os.chdir(Path(__file__).resolve().parents[2])  # → BrillianceLab/
# -------------------------------------------------------------------------

ROOT   = Path('.')
DOMAIN = 'brilliancelab.vercel.app'
HOST   = 'https://' + DOMAIN
KEY    = '0fe6807e04fbf0a30fffa590eb9c1b11'
KEY_FILE = f'{KEY}.txt'   # MUST exist at https://<DOMAIN>/<KEY>.txt
ENDPOINT = 'https://api.indexnow.org/indexnow'


def collect_urls_from_sitemaps() -> list[str]:
    urls = set()
    for fn in ['sitemap-pages.xml', 'sitemap-articles.xml', 'sitemap-amp.xml']:
        p = ROOT / fn
        if not p.exists(): continue
        for m in re.finditer(r'<loc>([^<]+)</loc>', p.read_text(encoding='utf-8')):
            urls.add(m.group(1).strip())
    return sorted(urls)


def submit(urls: list[str], dry: bool = False) -> int:
    if not urls:
        print('no URLs to submit'); return 0
    payload = {
        'host':        DOMAIN,
        'key':         KEY,
        'keyLocation': f'{HOST}/{KEY_FILE}',
        'urlList':     urls,
    }
    body = json.dumps(payload).encode('utf-8')
    print(f'submitting {len(urls)} URL(s) to IndexNow ({ENDPOINT})')
    if dry:
        print('--- dry-run, payload preview ---')
        print(json.dumps(payload, indent=2, ensure_ascii=False)[:1200])
        return 0
    req = urllib.request.Request(
        ENDPOINT, data=body,
        headers={'Content-Type': 'application/json; charset=utf-8'},
        method='POST'
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            print(f'  HTTP {resp.status} {resp.reason}')
            return 0 if 200 <= resp.status < 300 else 1
    except urllib.error.HTTPError as e:
        print(f'  HTTP {e.code} {e.reason}')
        body_text = e.read().decode('utf-8', errors='replace')
        if body_text: print(f'  body: {body_text[:300]}')
        # IndexNow uses 200 (accepted), 202 (queued), 400 (bad request),
        # 403 (key invalid), 422 (URLs not from same host), 429 (too many)
        return e.code if e.code != 200 else 0
    except Exception as e:
        print(f'  error: {e}')
        return 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('paths', nargs='*', help='Specific URL paths or full URLs to submit')
    ap.add_argument('--all', action='store_true', help='Submit every URL in sitemaps')
    ap.add_argument('--dry', action='store_true')
    args = ap.parse_args()

    if args.all:
        urls = collect_urls_from_sitemaps()
    else:
        urls = []
        for p in args.paths:
            if p.startswith('http'): urls.append(p)
            elif p.startswith('/'):  urls.append(HOST + p)
            else:                    urls.append(f'{HOST}/{p}')
    if not urls:
        print('Pass --all or list URLs/paths.'); sys.exit(1)

    # Verify key file is on disk (it should be served at /KEY.txt)
    if not (ROOT / KEY_FILE).exists():
        print(f'!! key file {KEY_FILE} missing from repo root — IndexNow will reject')
        print(f'   run:  echo {KEY} > {KEY_FILE}')
        sys.exit(2)

    sys.exit(submit(urls, dry=args.dry))


if __name__ == '__main__':
    main()
