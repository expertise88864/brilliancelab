# -*- coding: utf-8 -*-
"""
Auto-tighten meta descriptions to the 120-158 character SERP sweet spot,
preserving sentence boundaries.

Rules:
  - If desc length > 160 chars (CJK counted 2x for SERP truncation):
    truncate at the last 「。」「,」「、」「:」「;」 before char-160; ellipsis
    if cut mid-sentence.
  - If desc length < 80 chars: append the first sentence of the article's
    first <p> until reaching ≥ 100 chars.
  - Always preserve quotes and existing punctuation.

Idempotent: only rewrites when content actually changes.
"""
from __future__ import annotations
import re
from pathlib import Path

# --- Auto-locate the repo root so this script can be run from anywhere ---
import os as _os
_os.chdir(Path(__file__).resolve().parents[2])  # → BrillianceLab/
# -------------------------------------------------------------------------

ROOT = Path('.')

CJK_RE = re.compile(r'[㐀-䶿一-鿿豈-﫿]')
DESC_RE = re.compile(r'(<meta\s+name=["\']description["\']\s+content=["\'])([^"\']+)(["\']\s*/?>)', re.I)

def serp_len(s: str) -> int:
    """CJK chars count as 2 (double-wide in SERP)."""
    cjk = len(CJK_RE.findall(s))
    return cjk * 2 + (len(s) - cjk)


def tighten(desc: str, page_text: str = '') -> str:
    sl = serp_len(desc)
    if 100 <= sl <= 160:
        return desc

    # Too long — truncate at last sentence boundary before ~160 SERP chars
    if sl > 160:
        # Walk character by character, track SERP length, remember last
        # punctuation index that's ≤ 156 (leave 4 for ellipsis)
        target_serp = 156
        running = 0
        last_punct = 0
        for i, c in enumerate(desc):
            running += 2 if CJK_RE.match(c) else 1
            if running > target_serp:
                break
            if c in '。、,!?;:':
                last_punct = i + 1
        if last_punct > 30:
            return desc[:last_punct]
        # No good break — hard cut + ellipsis
        running = 0
        for i, c in enumerate(desc):
            running += 2 if CJK_RE.match(c) else 1
            if running > target_serp - 2:
                return desc[:i].rstrip(' ,、') + '…'

    # Too short — pull from first paragraph
    if sl < 100 and page_text:
        # Take sentences from page_text until the combined length is in range
        sentences = re.findall(r'[^。!?]+[。!?]', page_text)
        addition = ''
        for s in sentences:
            candidate = (desc + ' ' + addition + s).strip()
            if 100 <= serp_len(candidate) <= 158:
                return candidate
            if serp_len(candidate) > 158:
                break
            addition += s
        if addition:
            return (desc + ' ' + addition).strip()
    return desc


def first_para_text(html: str) -> str:
    m = re.search(r'(?:id=["\']proseZh["\']|class=["\'][^"\']*\bprose-zh\b[^"\']*["\'])'
                  r'[^>]*>[\s\S]+?<p\b[^>]*>([\s\S]+?)</p>', html, re.I)
    if not m: return ''
    txt = re.sub(r'<[^>]+>', '', m.group(1))
    return ' '.join(txt.split())


def patch(path: Path) -> tuple[bool, int, int]:
    src = path.read_text(encoding='utf-8')
    m = DESC_RE.search(src)
    if not m: return False, 0, 0
    old = m.group(2)
    page_txt = first_para_text(src)
    new = tighten(old, page_txt)
    if new == old: return False, serp_len(old), serp_len(old)
    new_tag = m.group(1) + new + m.group(3)
    new_src = src[:m.start()] + new_tag + src[m.end():]
    path.write_text(new_src, encoding='utf-8')
    return True, serp_len(old), serp_len(new)


def main():
    n = 0
    for p in sorted(ROOT.glob('blog/*.html')):
        changed, old_len, new_len = patch(p)
        if changed:
            print(f'  {p.name}  {old_len:>3} → {new_len:>3}')
            n += 1
    print(f'\n{n} meta description(s) tightened')


if __name__ == '__main__':
    main()
