# -*- coding: utf-8 -*-
"""
SEO content audit for every blog article. Reports:

  - title length        (45-60 chars ideal, 70 max)
  - meta description    (120-158 chars ideal, 160 max)
  - h1 presence + count (must be exactly 1)
  - h1 keyword overlap  (does h1 share words with title? main keyword?)
  - first <p> length    (60-200 chars sweet spot for snippet)
  - first <p> keyword   (does opening sentence contain primary keyword?)
  - h2 count            (should be ≥ 3 for skimmable content)
  - internal link count (≥ 3 to other /blog/ articles is healthy)
  - image alt presence  (currently 0 imgs but checks anyway)
  - canonical present   (delegated to audit_canonicals.py)

Outputs a CSV (audit_seo.csv) for spreadsheet review and a per-page status
to stdout. Exits 0 — this is informational, not a hard fail.
"""
from __future__ import annotations
import re, csv, sys
from pathlib import Path

# --- Auto-locate the repo root so this script can be run from anywhere ---
import os as _os
_os.chdir(Path(__file__).resolve().parents[2])  # → BrillianceLab/
# -------------------------------------------------------------------------

ROOT = Path('.')
TARGETS = sorted(ROOT.glob('blog/*.html'))


def text(html: str) -> str:
    """Strip tags + collapse whitespace."""
    html = re.sub(r'<(script|style|noscript)[\s\S]*?</\1>', '', html, flags=re.I)
    html = re.sub(r'<[^>]+>', ' ', html)
    return re.sub(r'\s+', ' ', html).strip()


def cjk_chars(s: str) -> int:
    return len(re.findall(r'[㐀-䶿一-鿿豈-﫿]', s))


def char_len(s: str) -> int:
    """CJK chars are double-width — count them as 2 for SERP truncation purposes."""
    return cjk_chars(s) * 2 + (len(s) - cjk_chars(s))


def audit_one(p: Path) -> dict:
    src = p.read_text(encoding='utf-8')
    out = {'file': p.name}

    # title
    m_title = re.search(r'<title>([\s\S]+?)</title>', src)
    title = m_title.group(1).strip() if m_title else ''
    out['title']     = title
    out['title_len'] = char_len(title)

    # meta description
    m_desc = re.search(r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']+)["\']', src)
    desc = m_desc.group(1) if m_desc else ''
    out['desc']     = desc[:80] + '…' if len(desc) > 80 else desc
    out['desc_len'] = char_len(desc)

    # h1
    h1s = re.findall(r'<h1\b[^>]*>([\s\S]+?)</h1>', src, re.I)
    h1_clean = [text(h) for h in h1s]
    out['h1_count'] = len(h1s)
    out['h1']       = h1_clean[0] if h1_clean else ''

    # h1 keyword overlap with title — use CJK 2-char n-grams + Latin words so
    # that "鑽石形狀完整指南" in title and "鑽石形狀 完整指南" (split by <br>)
    # in h1 still share tokens. Naive whole-token match misses these.
    def tok(s: str) -> set:
        latin = set(re.findall(r'[A-Za-z]{2,}', s))
        cjk   = re.sub(r'[^㐀-鿿]', '', s)
        bigrams = {cjk[i:i+2] for i in range(len(cjk) - 1)} if len(cjk) >= 2 else set()
        return latin | bigrams
    if h1_clean and title:
        out['h1_overlap'] = len(tok(title) & tok(h1_clean[0]))
    else:
        out['h1_overlap'] = 0

    # h2 count
    h2s = re.findall(r'<h2\b[^>]*>', src, re.I)
    out['h2_count'] = len(h2s)

    # first <p> in the article body. Prefer #proseZh, then .prose-zh, then
    # any <article> element (covers master-guide which uses neither id nor class).
    body = src
    m_zh = re.search(r'(?:id=["\']proseZh["\']|class=["\'][^"\']*\bprose-zh\b[^"\']*["\']|<article\b[^>]*data-pagefind-body)[^>]*>([\s\S]+?)(?=</article>|</section>|<div\s+class=["\'][^"\']*\bprose-en\b)', src, re.I)
    if m_zh:
        body = m_zh.group(1)
    p_match = re.search(r'<p\b[^>]*>([\s\S]+?)</p>', body, re.I)
    first_p_text = text(p_match.group(1)) if p_match else ''
    out['first_p']     = (first_p_text[:60] + '…') if len(first_p_text) > 60 else first_p_text
    out['first_p_len'] = char_len(first_p_text)

    # internal link count to other blog articles
    inter = re.findall(r'href=["\']/blog/([\w-]+)', src)
    distinct = {x for x in inter if x != p.stem}
    out['internal_links'] = len(distinct)

    # image alt audit
    imgs    = re.findall(r'<img\b[^>]*>', src, re.I)
    img_alt = sum(1 for i in imgs if re.search(r'\balt=', i, re.I))
    out['img_count']         = len(imgs)
    out['img_missing_alt']   = len(imgs) - img_alt

    # Verdict
    issues = []
    if out['title_len'] > 70 or out['title_len'] < 30: issues.append('title-len')
    if out['desc_len']  > 160 or out['desc_len']  < 80: issues.append('desc-len')
    if out['h1_count']  != 1:                            issues.append('h1-count')
    if out['h1_overlap'] < 1 and out['h1_count']:        issues.append('h1-keyword')
    if out['h2_count']  < 3:                             issues.append('h2-count')
    if out['first_p_len'] < 60:                          issues.append('first-p-too-short')
    if out['internal_links'] < 3:                        issues.append('few-internal-links')
    if out['img_missing_alt']:                           issues.append('img-no-alt')
    out['issues'] = ' '.join(issues) if issues else 'OK'
    return out


def main():
    rows = [audit_one(p) for p in TARGETS]

    # CSV dump
    csv_path = ROOT / 'audit_seo.csv'
    with open(csv_path, 'w', newline='', encoding='utf-8-sig') as f:
        cols = ['file','title_len','desc_len','h1_count','h1_overlap','h2_count',
                'first_p_len','internal_links','img_count','img_missing_alt','issues',
                'title','desc','h1','first_p']
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in rows: w.writerow(r)
    print(f'wrote {csv_path}\n')

    # Stdout summary — only flag non-OK files
    print(f'{"file":<40} {"title":>5} {"desc":>5} {"h1":>3} {"h2":>3} {"links":>5}  issues')
    print('-' * 100)
    bad = 0
    for r in rows:
        flag = '' if r['issues'] == 'OK' else '  !!'
        if r['issues'] != 'OK':
            print(f"{r['file']:<40} {r['title_len']:>5} {r['desc_len']:>5} {r['h1_count']:>3} {r['h2_count']:>3} {r['internal_links']:>5}  {r['issues']}{flag}")
            bad += 1
    print()
    print(f'Audit summary: {len(rows) - bad}/{len(rows)} pages clean, {bad} flagged for review')
    print(f'Full data: {csv_path.relative_to(ROOT).as_posix()}')


if __name__ == '__main__':
    main()
