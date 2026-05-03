# -*- coding: utf-8 -*-
"""
Inject FAQPage JSON-LD on every article with Q&A structure.

Currently only diamond-faq has FAQPage schema (50 questions). 18 other
articles have a `<h3>Q1: ...</h3><p>answer</p>` convention that maps
1:1 to FAQPage's Question/Answer entities — this script extracts them
and injects the schema in <head>.

Idempotent (sentinel: data-id="BL_FAQPAGE_AUTO"). Re-running refreshes
content.
"""
from __future__ import annotations
import json, re, html as htmllib
from pathlib import Path

# --- Auto-locate the repo root so this script can be run from anywhere ---
import os as _os
_os.chdir(Path(__file__).resolve().parents[2])  # → BrillianceLab/
# -------------------------------------------------------------------------

ROOT = Path('.')
SENTINEL = 'data-id="BL_FAQPAGE_AUTO"'

# Match <h3>Q1: ...</h3> followed by content up to next h2/h3 or end of section
QA_RE = re.compile(
    r'<h3[^>]*>\s*(Q\d+\s*[:：]\s*[^<]+?)\s*</h3>\s*'
    r'([\s\S]+?)'
    r'(?=<h[23]\b|</article>|</section>|<hr\b)',
    re.I
)


def clean_text(t: str) -> str:
    t = re.sub(r'<[^>]+>', '', t)
    t = htmllib.unescape(t)
    return ' '.join(t.split())


def trim_question(q: str) -> str:
    # Strip "Q1：" / "Q1:" prefix
    return re.sub(r'^Q\d+\s*[:：]\s*', '', q).strip()


def extract_qas(html: str) -> list[tuple[str, str]]:
    """Look at the visible Chinese prose block (proseZh / .prose-zh).
    Returns list of (question, answer) pairs."""
    # Narrow to proseZh region if present
    m = re.search(
        r'(?:id=["\']proseZh["\']|class=["\'][^"\']*\bprose-zh\b[^"\']*["\'])'
        r'[^>]*>([\s\S]+?)(?=</article>|<div\s+class=["\'][^"\']*\bprose-en\b)',
        html, re.I)
    body = m.group(1) if m else html
    pairs = []
    for q_raw, body_raw in QA_RE.findall(body):
        question = trim_question(clean_text(q_raw))
        answer   = clean_text(body_raw)
        # Trim absurdly long answers (Google ignores >300 words anyway)
        if len(answer) > 600:
            answer = answer[:597].rstrip() + '…'
        if 4 < len(question) < 200 and 6 < len(answer) < 700:
            pairs.append((question, answer))
    return pairs


def patch(p: Path) -> int:
    src = p.read_text(encoding='utf-8')
    if SENTINEL in src:
        # Idempotent: refresh existing block
        pass
    elif 'FAQPage' in src and 'BL_FAQPAGE' in src:
        # diamond-faq already has its hand-built FAQPage — skip
        return 0
    pairs = extract_qas(src)
    if not pairs:
        return 0

    schema = {
        '@context': 'https://schema.org',
        '@type':    'FAQPage',
        'mainEntity': [
            {
                '@type': 'Question',
                'name':  q,
                'acceptedAnswer': {'@type': 'Answer', 'text': a},
            } for q, a in pairs
        ],
    }
    block = (
        '\n<script type="application/ld+json" ' + SENTINEL + '>\n'
        + json.dumps(schema, ensure_ascii=False, separators=(',', ':'))
        + '\n</script>'
    )
    if SENTINEL in src:
        new = re.sub(
            r'\n?<script[^>]*' + re.escape(SENTINEL) + r'[^>]*>[\s\S]*?</script>',
            block, src, count=1)
    else:
        new = src.replace('</head>', block + '\n</head>', 1)
    if new == src:
        return 0
    p.write_text(new, encoding='utf-8')
    return len(pairs)


def main():
    files = sorted(ROOT.glob('blog/*.html'))
    total_q = 0
    touched = 0
    for p in files:
        n = patch(p)
        if n:
            total_q += n
            touched += 1
            print(f'  {n:>3} Q-A → FAQPage on {p.name}')
    print()
    print(f'{touched} files updated, {total_q} questions total → FAQPage schema')


if __name__ == '__main__':
    main()
