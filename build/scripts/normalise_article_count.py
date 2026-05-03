# -*- coding: utf-8 -*-
"""
Normalise the article-count references across the site.

The site has accumulated drift: master-guide claims "14 篇" (legacy from the
pre-expansion era), topics says "38 篇", search says "40+ 篇", index says
"43 篇". The actual count is 44 articles + 5 silo hubs + 1 monthly report.

Standard going forward (handles monthly +1):
  Chinese: 「44+ 篇文章」
  English: "44+ articles"

We DON'T touch:
  - master-guide's "14 phases / 14 階段" (intentional structural reference
    to the master guide's own 14-section roadmap)
  - index.html's `ItemList (25 articles ranked)` — bounded data structure
  - Per-hub article counts ("7 篇" / "8 篇" — accurate hub membership)

Idempotent: re-runs are safe (already-correct values are no-ops).
"""
from __future__ import annotations
import re, sys
from pathlib import Path

# --- Auto-locate the repo root so this script can be run from anywhere ---
import os as _os
_os.chdir(Path(__file__).resolve().parents[2])  # → BrillianceLab/
# -------------------------------------------------------------------------

try: sys.stdout.reconfigure(encoding='utf-8')
except Exception: pass

ROOT = Path('.')

# Per-file targeted replacements — keyed by (file, exact_old, new) so we can
# reason about each substitution. "old" must appear verbatim in the source.
REPLACEMENTS = [
    # --- master-guide: keep "14 phases", replace "summary of 14 articles" ---
    ('blog/master-guide.html', 'BrillianceLab 14 篇文章的總整理', 'BrillianceLab 44+ 篇文章的總整理'),
    ('blog/master-guide.html', 'BrillianceLab 14 篇文章的總整理', 'BrillianceLab 44+ 篇文章的總整理'),  # may appear twice
    ('blog/master-guide.html', '這 14 篇文章的「實踐工具」', '這 44+ 篇文章的「實踐工具」'),
    ('blog/master-guide.html', '14 篇文章 + 1 個計算機 = 鑽石購買達人',
     '44+ 篇文章 + 1 個計算機 = 鑽石購買達人'),
    ('blog/master-guide.html', '14 articles + 1 calculator = diamond expert',
     '44+ articles + 1 calculator = diamond expert'),
    ('blog/master-guide.html', '30+ 篇文章的索引主幹', '44+ 篇文章的索引主幹'),
    ('blog/master-guide.html', '35+ 篇文章的總整理', '44+ 篇文章的總整理'),
    ('blog/master-guide.html', '38 篇主題索引', '44+ 篇主題索引'),
    # NOTE: deliberately leave "14 articles into action" / "turns these 14
    # articles" alone — those refer to the 14 stages of the master guide, not
    # the entire blog corpus.

    # --- topics.html: 38 篇 → 44+ 篇 (replace_all is fine here, no ambiguity) ---
    ('blog/topics.html', '38 篇', '44+ 篇'),

    # --- 404.html ---
    ('404.html',         '38 篇',     '44+ 篇'),
    ('404.html',         '38 篇文章',  '44+ 篇文章'),

    # --- search.html ---
    ('search.html',      '40+ 篇',    '44+ 篇'),
    ('search.html',      '38 篇文章 8 個主題',  '44+ 篇文章 9 個主題'),

    # --- index.html: drawer link "🗺 主題索引（43 篇地圖）" ---
    ('index.html',       '43 篇地圖', '44+ 篇地圖'),

    # --- diamond-faq lead ("不想看 14 篇長文") ---
    ('blog/diamond-faq.html', '不想看 14 篇長文', '不想看 44+ 篇長文'),

    # --- blog-shared.js drawer also has the count ---
    ('blog/blog-shared.js', '主題索引（43 篇地圖）', '主題索引（44+ 篇地圖）'),
    ('blog/blog-shared.js', '主題索引(43 篇地圖)', '主題索引(44+ 篇地圖)'),  # half-width paren variant
]


def apply():
    by_file = {}
    for path, old, new in REPLACEMENTS:
        by_file.setdefault(path, []).append((old, new))

    total_files = 0
    total_changes = 0
    for rel, edits in by_file.items():
        p = ROOT / rel
        if not p.exists():
            print(f'  SKIP {rel} (not found)')
            continue
        src = p.read_text(encoding='utf-8')
        new_src = src
        n = 0
        for old, new in edits:
            if old in new_src and new not in new_src:
                # First-occurrence replace — avoid double-substitution if old
                # appears multiple times and we want all of them changed
                count = new_src.count(old)
                new_src = new_src.replace(old, new)
                n += count
        if new_src != src:
            p.write_text(new_src, encoding='utf-8')
            total_files += 1
            total_changes += n
            print(f'  {rel:<32}  {n} replacement(s)')
        else:
            print(f'  {rel:<32}  (already up to date)')
    print(f'\n{total_changes} string(s) updated across {total_files} file(s)')


if __name__ == '__main__':
    apply()
