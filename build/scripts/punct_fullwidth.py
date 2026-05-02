# -*- coding: utf-8 -*-
"""
Convert half-width ASCII punctuation to full-width Chinese punctuation
INSIDE Chinese text contexts only — never inside <script>/<style>/<pre>/<code>/<svg>/<noscript>,
never inside HTML attribute values except `data-zh`/`data-zhcn`/`title`,
and never inside numbers/code-like tokens.

Usage:
    python punct_fullwidth.py [--dry] FILE_OR_DIR ...
"""
from __future__ import annotations
import re, sys, os, argparse, difflib

# --- Auto-locate the repo root so this script can be run from anywhere ---
import os as _os, pathlib as _pl
_os.chdir(_pl.Path(__file__).resolve().parents[2])  # → BrillianceLab/
# -------------------------------------------------------------------------


CJK = r'[㐀-䶿一-鿿豈-﫿]'
CJK = r"[㐀-䶿一-鿿豈-﫿]"
CJK_CTX = r'[㐀-䶿一-鿿豈-﫿①-⓿❶-➿　-〿＀-￯]'

# Tags whose text content must NOT be touched.
SKIP_TAGS = {'script', 'style', 'pre', 'code', 'svg', 'noscript', 'textarea'}


# Full-width replacements as explicit unicode escapes so source-encoding can never
# silently downgrade them.
FW_COMMA  = '，'   # ，
FW_PERIOD = '。'   # 。
FW_COLON  = '：'   # :
FW_SEMI   = '；'   # ;
FW_Q      = '？'   # ?
FW_EX     = '！'   # !
FW_LPAREN = '（'   # (
FW_RPAREN = '）'   # )


def cn_punct(text: str) -> str:
    """Apply punctuation conversion to a stretch of (already-decoded) Chinese-context text."""
    if not text:
        return text
    C  = CJK
    CC = CJK_CTX   # lookahead/behind: include circled numbers, fullwidth, CJK punct
    # 1. Comma — surrounded by CJK / CJK-context.
    text = re.sub(rf'({C})\s*,\s*(?={CC})',   rf'\1{FW_COMMA}', text)
    text = re.sub(rf'({C})\s*,\s*(?=$|<|\n)', rf'\1{FW_COMMA}', text)
    # 2. Period — protect decimal numbers (digit.digit) and abbreviations.
    text = re.sub(rf'({C})\s*\.\s*(?={CC})',   rf'\1{FW_PERIOD}', text)
    text = re.sub(rf'({C})\s*\.\s*(?=$|<|\n)', rf'\1{FW_PERIOD}', text)
    # 3. Colon
    text = re.sub(rf'({C})\s*:\s*(?={CC})', rf'\1{FW_COLON}', text)
    text = re.sub(rf'({C}):(?=\s)',          rf'\1{FW_COLON}', text)
    # 4. Semicolon
    text = re.sub(rf'({C})\s*;\s*(?={CC})', rf'\1{FW_SEMI}', text)
    text = re.sub(rf'({C});(?=\s)',          rf'\1{FW_SEMI}', text)
    # 4b. CJK-then-HTML-tag for : ; , .
    text = re.sub(rf'({C})\s*:\s*(?=<)', rf'\1{FW_COLON}',  text)
    text = re.sub(rf'({C})\s*;\s*(?=<)', rf'\1{FW_SEMI}',   text)
    text = re.sub(rf'({C})\s*,\s*(?=<)', rf'\1{FW_COMMA}',  text)
    text = re.sub(rf'({C})\s*\.\s*(?=<)', rf'\1{FW_PERIOD}', text)
    # 5. Question mark
    text = re.sub(rf'({C})\?',  rf'\1{FW_Q}',  text)
    # 6. Exclamation
    text = re.sub(rf'({C})!',   rf'\1{FW_EX}', text)
    # 7. Leading punctuation at the START of a text node, when followed by CJK context.
    #    These appear when the preceding inline tag (e.g. <a>) closes and Chinese resumes.
    text = re.sub(rf'^\s*,\s*(?={CC})',  rf'{FW_COMMA}',  text)
    text = re.sub(rf'^\s*\.\s*(?={CC})', rf'{FW_PERIOD}', text)
    text = re.sub(rf'^\s*:\s*(?={CC})',  rf'{FW_COLON}',  text)
    text = re.sub(rf'^\s*;\s*(?={CC})',  rf'{FW_SEMI}',   text)
    text = re.sub(rf'^\s*\?\s*(?={CC})', rf'{FW_Q}',      text)
    text = re.sub(rf'^\s*!\s*(?={CC})',  rf'{FW_EX}',     text)
    # 7. Parens around CJK content (skip if inside parens we already see existing fw or contains URL chars).
    def paren_repl(m):
        inner = m.group(1)
        if not re.search(C, inner):
            return m.group(0)
        if re.search(r'[/\\@#=&?]', inner):
            return m.group(0)
        return f'{FW_LPAREN}{inner}{FW_RPAREN}'
    text = re.sub(r'\(([^()]{1,80})\)', paren_repl, text)
    return text


# --------------------------------------------------------------------------
# HTML walker — split into (tag, text) segments and convert text in non-skip scopes.
# --------------------------------------------------------------------------

# Properly handles `>` inside quoted attribute values (the outer attr quote rules).
TAG_RE = re.compile(
    r'<!--[\s\S]*?-->'                                     # comments
    r'|<![A-Za-z][^>]*>'                                    # DOCTYPE / declarations
    r'|<\?[\s\S]*?\?>'                                      # processing instructions
    r'|</?[a-zA-Z][a-zA-Z0-9]*'                             # opening / closing tag start
    r'(?:\s+[^\s/>"\'=]+(?:\s*=\s*(?:"[^"]*"|\'[^\']*\'|[^\s"\'=<>`]+))?)*'  # attributes
    r'\s*/?>',
    re.DOTALL,
)


def convert_html(src: str) -> str:
    out = []
    pos = 0
    skip_depth = 0          # > 0 means inside a SKIP_TAGS block
    skip_stack = []         # names of nested skip tags
    for m in TAG_RE.finditer(src):
        # text segment
        text = src[pos:m.start()]
        if text:
            if skip_depth == 0:
                out.append(cn_punct(text))
            else:
                out.append(text)
        tag_src = m.group(0)
        # Comments / DOCTYPE / processing instructions — copy verbatim
        if tag_src.startswith('<!') or tag_src.startswith('<?'):
            out.append(tag_src)
            pos = m.end()
            continue
        # Identify tag name and open/close
        name_match = re.match(r'<\s*(/?)([a-zA-Z][a-zA-Z0-9]*)', tag_src)
        if not name_match:
            out.append(tag_src)
            pos = m.end()
            continue
        is_close = name_match.group(1) == '/'
        name = name_match.group(2).lower()
        self_closing = tag_src.endswith('/>')

        # Convert Chinese inside specific attribute values
        if not is_close:
            tag_src = _rewrite_attrs(tag_src)

        # Skip tag depth tracking
        if name in SKIP_TAGS:
            if is_close:
                if skip_stack and skip_stack[-1] == name:
                    skip_stack.pop()
                    skip_depth = len(skip_stack)
            elif not self_closing:
                skip_stack.append(name)
                skip_depth = len(skip_stack)
        out.append(tag_src)
        pos = m.end()
    # tail text
    text = src[pos:]
    if text:
        if skip_depth == 0:
            out.append(cn_punct(text))
        else:
            out.append(text)
    return ''.join(out)


ATTR_RE = re.compile(
    r'(\s)(data-zh|data-zhcn|title|alt|aria-label|content|placeholder|summary)\s*=\s*'
    r'(?:"([^"]*)"|\'([^\']*)\')',
    re.IGNORECASE,
)


def _rewrite_attrs(tag: str) -> str:
    def repl(m):
        ws, name, q1, q2 = m.group(1), m.group(2), m.group(3), m.group(4)
        val = q1 if q1 is not None else q2
        # Only convert if value contains CJK (else it's English/code).
        if not re.search(CJK, val):
            return m.group(0)
        new_val = cn_punct(val)
        if new_val == val:
            return m.group(0)
        quote = '"' if q1 is not None else "'"
        return f'{ws}{name}={quote}{new_val}{quote}'
    return ATTR_RE.sub(repl, tag)


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def process_file(path: str, dry: bool) -> tuple[int, int]:
    with open(path, 'r', encoding='utf-8') as f:
        src = f.read()
    out = convert_html(src)
    if out == src:
        return (0, 0)
    diff_lines = sum(1 for _ in difflib.unified_diff(src.splitlines(), out.splitlines(), n=0))
    if not dry:
        with open(path, 'w', encoding='utf-8', newline='') as f:
            f.write(out)
    return (1, diff_lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('paths', nargs='+')
    ap.add_argument('--dry', action='store_true', help='print diff stats only, do not write')
    ap.add_argument('--show', action='store_true', help='show first 30 diff lines')
    args = ap.parse_args()

    files: list[str] = []
    for p in args.paths:
        if os.path.isdir(p):
            for root, _, fns in os.walk(p):
                for fn in fns:
                    if fn.endswith('.html'):
                        files.append(os.path.join(root, fn))
        else:
            files.append(p)

    total_changed = 0
    for f in sorted(files):
        before = open(f, 'r', encoding='utf-8').read()
        after = convert_html(before)
        if before == after:
            print(f'  ok   {f}')
            continue
        total_changed += 1
        n = sum(1 for _ in difflib.unified_diff(before.splitlines(), after.splitlines(), n=0))
        print(f'  EDIT {f}   ({n} diff lines)')
        if args.show:
            for line in list(difflib.unified_diff(before.splitlines(), after.splitlines(), n=1))[:30]:
                print('       ' + line)
        if not args.dry:
            with open(f, 'w', encoding='utf-8', newline='') as out:
                out.write(after)
    print(f'\n{total_changed}/{len(files)} file(s) modified' + (' [dry-run]' if args.dry else ''))


if __name__ == '__main__':
    main()
