# -*- coding: utf-8 -*-
"""
Generate per-article 1200×630 PNG OG images and rewrite each page's
og:image / twitter:image to point at it.

Why: SVG og:image (the current /icon.svg) doesn't render in Facebook /
Slack / Discord previews — they need a raster.

Output: og/<slug>.png  (12-25 KB each)
"""
from __future__ import annotations
import re, os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# --- Auto-locate the repo root so this script can be run from anywhere ---
import os as _os, pathlib as _pl
_os.chdir(_pl.Path(__file__).resolve().parents[2])  # → BrillianceLab/
# -------------------------------------------------------------------------


ROOT = Path('.')
OG   = ROOT / 'og'
DOMAIN = 'https://brilliancelab.vercel.app'

W, H = 1200, 630
BG_TOP    = (250, 248, 243)   # ivory
BG_BOTTOM = (252, 247, 232)   # warmer
INK       = (26, 29, 46)
INK_2     = (74, 77, 94)
GOLD      = (201, 164, 92)
GOLD_DEEP = (138, 110, 48)

# Windows CJK fonts (msjh = 微軟正黑體) — will be available on dev machine.
FONT_BOLD = 'C:/Windows/Fonts/msjhbd.ttc'
FONT_REG  = 'C:/Windows/Fonts/msjh.ttc'


def make_gradient(w: int, h: int, top: tuple, bottom: tuple) -> Image.Image:
    img = Image.new('RGB', (w, h), top)
    for y in range(h):
        t = y / (h - 1)
        c = tuple(int(top[i] * (1 - t) + bottom[i] * t) for i in range(3))
        ImageDraw.Draw(img).line([(0, y), (w, y)], fill=c)
    return img


def diamond_silhouette(size: int, color: tuple) -> Image.Image:
    """Stylised diamond glyph (top crown + lower pavilion)."""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    s = size
    pts_top    = [(s * 0.5, s * 0.05), (s * 0.05, s * 0.4), (s * 0.95, s * 0.4)]
    pts_bottom = [(s * 0.05, s * 0.4), (s * 0.95, s * 0.4), (s * 0.5, s * 0.95)]
    d.polygon(pts_top,    fill=color)
    d.polygon(pts_bottom, fill=tuple(int(c * 0.78) for c in color))
    return img


def wrap_cjk(text: str, max_chars: int) -> list[str]:
    """Cheap line-wrap that respects CJK width (1 char ≈ 1 unit)."""
    lines, cur = [], ''
    for ch in text:
        cur += ch
        if len(cur) >= max_chars and ch in '，。、 :;':
            lines.append(cur.strip())
            cur = ''
    if cur:
        lines.append(cur.strip())
    return lines


def render_og(slug: str, title: str, subtitle: str = '', tag: str = 'BrillianceLab · 鑽石實驗室') -> Path:
    img = make_gradient(W, H, BG_TOP, BG_BOTTOM)

    # subtle glow circle behind diamond
    glow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([60, 130, 460, 530], fill=(201, 164, 92, 60))
    glow = glow.filter(ImageFilter.GaussianBlur(40))
    img.paste(glow, (0, 0), glow)

    # diamond silhouette
    diamond = diamond_silhouette(360, GOLD)
    img.paste(diamond, (90, 150), diamond)

    d = ImageDraw.Draw(img)

    # Top tag
    f_tag = ImageFont.truetype(FONT_BOLD, 22)
    d.text((520, 80), tag.upper(), fill=GOLD_DEEP, font=f_tag, spacing=8)

    # Title
    f_title = ImageFont.truetype(FONT_BOLD, 64)
    title_lines = wrap_cjk(title, max_chars=12)
    y = 150
    for line in title_lines[:3]:
        d.text((520, y), line, fill=INK, font=f_title)
        y += 78

    # Subtitle (gold underline)
    if subtitle:
        f_sub = ImageFont.truetype(FONT_REG, 28)
        sub_lines = wrap_cjk(subtitle, max_chars=22)
        y += 24
        d.line([(520, y - 10), (640, y - 10)], fill=GOLD, width=4)
        for line in sub_lines[:2]:
            d.text((520, y), line, fill=INK_2, font=f_sub)
            y += 38

    # Bottom-right footer
    f_foot = ImageFont.truetype(FONT_REG, 22)
    d.text((520, 540), 'brilliancelab.vercel.app', fill=GOLD_DEEP, font=f_foot)

    OG.mkdir(parents=True, exist_ok=True)
    out = OG / f'{slug}.png'
    img.save(out, 'PNG', optimize=True)
    return out


# Per-page metadata. If a slug is missing, the OG generator falls back to
# parsing <title> / <meta name=description> from the HTML.
EXTRA = {
    'master-guide':       {'subtitle': '14 階段 · 數學公式 · 真實案例'},
    'gia-guide':          {'subtitle': '4Cs / 比例圖 / Polish / Symmetry / Fluorescence'},
    'hearts-arrows-truth':{'subtitle': '哪些 GIA Excellent 其實不及格'},
    'budget-formula':     {'subtitle': '分數 × √克拉 ÷ 價格 = BPD'},
    'lab-vs-natural':     {'subtitle': '光學完全相同,差價 70%'},
    'diamond-color':      {'subtitle': 'D-Z 23 階,G 色甜蜜點'},
    'diamond-clarity':    {'subtitle': 'FL-I,VS2 性價比之王'},
    'diamond-shapes':     {'subtitle': '10 種形狀完整對照'},
    'diamond-faq':        {'subtitle': '50 個問題 · 直接給答案'},
    'engagement-guide':   {'subtitle': '預算 → 求婚 9 步驟'},
    'cert-comparison':    {'subtitle': 'GIA / IGI / HRD / AGS'},
    'moissanite-vs-cz-vs-lab': {'subtitle': '4 種「鑽石」完整辨識'},
}


def main():
    pages = sorted(ROOT.glob('blog/*.html'))
    titles_seen = 0
    for p in pages:
        slug = p.stem
        if slug in ('index', 'topics', 'feed'):
            continue
        src = p.read_text(encoding='utf-8')
        m_title = re.search(r'<title>([^|<]+?)(?:\s*[—\-|]\s*[^<]+)?</title>', src)
        title = m_title.group(1).strip() if m_title else slug
        info = EXTRA.get(slug, {})
        sub = info.get('subtitle', '')
        if not sub:
            m_desc = re.search(r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']+)["\']', src)
            if m_desc:
                sub = m_desc.group(1)[:60]
        try:
            out = render_og(slug, title, sub)
            print(f'  wrote {out.relative_to(ROOT)}  ({out.stat().st_size // 1024} KB)')
            titles_seen += 1
        except Exception as e:
            print(f'  ERROR {slug}: {e}')

    # Re-write og:image / twitter:image to point at the new PNG
    print()
    rewritten = 0
    for p in pages:
        slug = p.stem
        if slug in ('index', 'topics', 'feed'):
            continue
        src = p.read_text(encoding='utf-8')
        new = src
        target = f'{DOMAIN}/og/{slug}.png'
        new = re.sub(
            r'(property=["\']og:image["\']\s+content=["\'])[^"\']+(["\'])',
            lambda m: m.group(1) + target + m.group(2), new)
        new = re.sub(
            r'(name=["\']twitter:image["\']\s+content=["\'])[^"\']+(["\'])',
            lambda m: m.group(1) + target + m.group(2), new)
        if new != src:
            p.write_text(new, encoding='utf-8')
            rewritten += 1
    print(f'\n{titles_seen} OG PNG files written, {rewritten} pages rewritten to use them')


if __name__ == '__main__':
    main()
