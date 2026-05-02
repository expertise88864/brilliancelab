# -*- coding: utf-8 -*-
"""
Subset Noto Serif TC + Noto Sans TC down to only the characters used on the
site, then emit woff2 ready to be self-hosted at /assets/fonts/.

Usage:

  1. Grab source TTF/OTF files (~7 MB each) once, drop them into
     build/fonts-source/:

         NotoSerifTC-Regular.otf
         NotoSerifTC-Bold.otf
         NotoSansTC-Regular.otf
         NotoSansTC-Bold.otf

     (Available from https://fonts.google.com/noto/specimen/Noto+Serif+TC
     or https://github.com/notofonts/noto-cjk)

  2. Refresh the charset list (in case new CJK chars appeared):

         python build_fonts.py --charset

  3. Subset:

         python build_fonts.py

  4. Subset woff2 files appear in assets/fonts/.
     The charset will typically be 2,000-3,000 chars → ~80-150 KB per weight.

Requires Brotli for woff2 compression — install once:
  pip install fonttools brotli
"""
from __future__ import annotations
import argparse, re, sys
from pathlib import Path

# --- Auto-locate the repo root so this script can be run from anywhere ---
import os as _os
_os.chdir(Path(__file__).resolve().parents[2])  # → BrillianceLab/
# -------------------------------------------------------------------------

ROOT = Path('.')
SRC  = ROOT / 'build' / 'fonts-source'
OUT  = ROOT / 'assets' / 'fonts'

CJK_RE = re.compile(r'[㐀-䶿一-鿿豈-﫿]')

FACES = [
    'NotoSerifTC-Regular',
    'NotoSerifTC-Bold',
    'NotoSansTC-Regular',
    'NotoSansTC-Bold',
]


def collect_charset() -> str:
    chars = set()
    files = (
        list(ROOT.glob('*.html')) +
        list(ROOT.glob('blog/*.html')) +
        list(ROOT.glob('amp/blog/*.html'))
    )
    for p in files:
        src = p.read_text(encoding='utf-8')
        src = re.sub(r'<(script|style|svg|noscript)[\s\S]*?</\1>', '', src, flags=re.I)
        for ch in CJK_RE.findall(src):
            chars.add(ch)
    basics = (
        '，。；：？！「」『』《》〈〉【】（）—…·、 　'
        '0123456789'
        'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
        '.,;:?!()[]{}-_/&%$#@*+=<>"\''
    )
    for ch in basics:
        chars.add(ch)
    return ''.join(sorted(chars))


def write_charset(charset: str):
    out = ROOT / 'build' / 'cjk-charset.txt'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(charset, encoding='utf-8')
    print(f'  charset: {len(charset)} chars → {out}')


def subset_face(face: str, charset: str):
    try:
        from fontTools.subset import Subsetter, Options
        from fontTools.ttLib import TTFont
    except ImportError:
        print('!! fontTools not installed. Run: pip install fonttools brotli')
        sys.exit(1)
    src_otf = SRC / f'{face}.otf'
    src_ttf = SRC / f'{face}.ttf'
    src = src_otf if src_otf.exists() else src_ttf if src_ttf.exists() else None
    if src is None:
        print(f'  SKIP {face} (no source in {SRC})')
        return
    OUT.mkdir(parents=True, exist_ok=True)
    out = OUT / f'{face}.subset.woff2'
    font = TTFont(str(src))
    opts = Options()
    opts.flavor = 'woff2'
    opts.layout_features = ['*']
    opts.no_subset_tables = ['DSIG']
    opts.hinting = False
    opts.ignore_missing_unicodes = True
    sub = Subsetter(options=opts)
    sub.populate(text=charset)
    sub.subset(font)
    font.flavor = 'woff2'
    font.save(str(out))
    size_kb = out.stat().st_size / 1024
    print(f'  wrote {out} ({size_kb:.1f} KB)')


def emit_face_css(charset_size: int):
    """Emit @font-face declarations users can paste into the CSS pipeline."""
    css = '/* Self-hosted CJK fonts (subset of {} glyphs) */\n'.format(charset_size)
    for face in FACES:
        family = 'Noto Serif TC' if 'Serif' in face else 'Noto Sans TC'
        weight = '700' if 'Bold' in face else '400'
        css += (
            f"@font-face{{font-family:'{family}';font-style:normal;font-weight:{weight};"
            f"font-display:swap;src:url('/assets/fonts/{face}.subset.woff2') format('woff2');"
            f"unicode-range:U+4E00-9FFF,U+3400-4DBF,U+F900-FAFF,U+3000-303F,U+FF00-FFEF;}}\n"
        )
    out = ROOT / 'assets' / 'fonts' / 'fonts.css'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(css, encoding='utf-8')
    print(f'  wrote {out}')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--charset', action='store_true', help='only refresh the charset file, do not subset')
    args = ap.parse_args()

    charset = collect_charset()
    write_charset(charset)
    if args.charset:
        return

    print(f'\nSubsetting {len(FACES)} faces against {len(charset)} chars …')
    for face in FACES:
        subset_face(face, charset)
    emit_face_css(len(charset))
    print('\nDone. Inject /assets/fonts/fonts.css alongside /assets/tw.css and remove the')
    print('Google Fonts <link> tags from each HTML page (they download 3 MB unsubset).')


if __name__ == '__main__':
    main()
