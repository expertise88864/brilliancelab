# -*- coding: utf-8 -*-
"""
Auto-tighten <title> to 55-65 SERP characters (CJK counted 2x).

Strategy — applied in order, stop when length reaches sweet spot:
  1. Drop ` | BrillianceLab` brand suffix (saves 17 chars)
  2. Drop ` — <subtitle>` qualifier after em-dash
  3. If still too long, truncate at last 「、」「,」「:」「:」 boundary

Also updates the matching <meta property="og:title">, <meta name="twitter:title">,
JSON-LD `headline` so all signals stay consistent.

Idempotent — only writes when length actually drops below 70.
"""
from __future__ import annotations
import re, sys
from pathlib import Path

# Force UTF-8 stdout so we can safely print Chinese + accented chars on Windows cp950
try: sys.stdout.reconfigure(encoding='utf-8')
except Exception: pass

# --- Auto-locate the repo root so this script can be run from anywhere ---
import os as _os
_os.chdir(Path(__file__).resolve().parents[2])  # → BrillianceLab/
# -------------------------------------------------------------------------

ROOT = Path('.')
TITLE_RE = re.compile(r'<title>([\s\S]+?)</title>')
OG_TITLE_RE  = re.compile(r'(<meta\s+property=["\']og:title["\']\s+content=["\'])([^"\']+)(["\'])', re.I)
TW_TITLE_RE  = re.compile(r'(<meta\s+name=["\']twitter:title["\']\s+content=["\'])([^"\']+)(["\'])', re.I)
HEADLINE_RE  = re.compile(r'("headline"\s*:\s*")([^"]+)(")')

CJK_RE = re.compile(r'[㐀-䶿一-鿿豈-﫿]')

BRAND_SUFFIX_RE = re.compile(r'\s*[|｜]\s*BrillianceLab(?:\s*[··]?\s*鑽石實驗室)?\s*$')
EM_DASH_TAIL_RE = re.compile(r'\s*[—\-–]\s*[^—\-–|]+$')

TARGET = 65   # aim for 55-65 SERP chars; drop when >70


def serp_len(s: str) -> int:
    cjk = len(CJK_RE.findall(s))
    return cjk * 2 + (len(s) - cjk)


def tighten(t: str) -> str:
    if serp_len(t) <= 70:
        return t
    # Step 1: drop brand suffix
    candidate = BRAND_SUFFIX_RE.sub('', t).strip()
    if serp_len(candidate) <= TARGET:
        return candidate
    # Step 2: drop em-dash subtitle (only one pass — usually gets us into range)
    candidate2 = EM_DASH_TAIL_RE.sub('', candidate).strip()
    if serp_len(candidate2) <= TARGET and serp_len(candidate2) >= 30:
        return candidate2
    # Step 3: truncate at last boundary char before SERP-65
    best = candidate
    running = 0; last_break = 0
    for i, c in enumerate(candidate):
        running += 2 if CJK_RE.match(c) else 1
        if running > TARGET:
            break
        if c in '、,:::!?。 ':
            last_break = i + 1
    if last_break > 25:
        return candidate[:last_break].rstrip('  ,、:: ')
    # Step 4: hard cut + ellipsis
    running = 0
    for i, c in enumerate(candidate):
        running += 2 if CJK_RE.match(c) else 1
        if running > TARGET - 2:
            return candidate[:i].rstrip(' ,、') + '…'
    return candidate


def patch(p: Path) -> tuple[bool, int, int, str, str]:
    src = p.read_text(encoding='utf-8')
    m = TITLE_RE.search(src)
    if not m: return False, 0, 0, '', ''
    old = m.group(1).strip()
    if serp_len(old) <= 70:
        return False, serp_len(old), serp_len(old), old, old
    new = tighten(old)
    if new == old or not new:
        return False, serp_len(old), serp_len(old), old, old

    # Update <title>
    new_src = TITLE_RE.sub(lambda _: f'<title>{new}</title>', src, count=1)

    # Update og:title and twitter:title only if their current value matches old
    # (don't blindly overwrite — they may have been hand-tuned).
    for rx in (OG_TITLE_RE, TW_TITLE_RE):
        def repl(mm):
            cur = mm.group(2)
            if cur.strip() == old or cur.strip().startswith(new[:20]):
                return mm.group(1) + new + mm.group(3)
            return mm.group(0)
        new_src = rx.sub(repl, new_src)

    # Update first JSON-LD headline if it equals the old title
    def hl(mm):
        if mm.group(2) == old:
            return mm.group(1) + new + mm.group(3)
        return mm.group(0)
    new_src = HEADLINE_RE.sub(hl, new_src, count=1)

    if new_src != src:
        p.write_text(new_src, encoding='utf-8')
    return True, serp_len(old), serp_len(new), old, new


def main():
    n = 0
    for p in sorted(ROOT.glob('blog/*.html')):
        changed, old_l, new_l, old, new = patch(p)
        if changed:
            n += 1
            print(f'  {p.name:<40} {old_l:>3} → {new_l:>3}')
            print(f'      OLD: {old}')
            print(f'      NEW: {new}')
    print(f'\n{n} title(s) tightened')


if __name__ == '__main__':
    main()
