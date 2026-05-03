"""
Verify blog-shared.js syntax balance with a proper JS state machine.
Tracks single-quote / double-quote / template-literal / line-comment / block-comment
states correctly so quotes and braces inside strings are not miscounted.
Exits non-zero on imbalance.
"""
import sys, pathlib

# --- Auto-locate the repo root so this script can be run from anywhere ---
import os as _os
_os.chdir(pathlib.Path(__file__).resolve().parents[2])  # → BrillianceLab/
# -------------------------------------------------------------------------

PATH = 'blog/blog-shared.js'
src = open(PATH, encoding='utf-8').read()

i, n = 0, len(src)
depth = 0
state = 'code'   # code | sq | dq | bq | lc | bc | re (regex literal)
line, col = 1, 0
errors = []
last_nonws = ''  # previous non-whitespace char in code mode (for regex disambiguation)
# A `/` starts a regex literal (vs division) when the previous non-whitespace
# code char is one of these — covers .match(/.../), arr=[/.../], (/.../), etc.
REGEX_LEADERS = set('(,;=!&|?{}:[+*~^<>%')

while i < n:
    c = src[i]
    nxt = src[i + 1] if i + 1 < n else ''

    if c == '\n':
        line += 1; col = 0
    else:
        col += 1

    if state == 'code':
        if c == '/' and nxt == '/': state = 'lc'; i += 2; continue
        if c == '/' and nxt == '*': state = 'bc'; i += 2; continue
        if c == '/' and (last_nonws == '' or last_nonws in REGEX_LEADERS):
            state = 're'; i += 1; continue
        if c == "'":  state = 'sq'; i += 1; continue
        if c == '"':  state = 'dq'; i += 1; continue
        if c == '`':  state = 'bq'; i += 1; continue
        # We only track '{}' — '()' and '[]' are confused by regex literals like /[abc]/
        if c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
            if depth < 0:
                errors.append(f'extra "}}" at line {line} col {col}')
                break
        if not c.isspace():
            last_nonws = c
        i += 1; continue

    if state == 're':
        if c == '\\' and nxt:
            i += 2; continue
        if c == '[':
            state = 're_class'; i += 1; continue
        if c == '/':
            state = 'code'; i += 1
            # consume regex flags
            while i < n and src[i].isalpha(): i += 1
            last_nonws = ')'   # treat closed regex as expression value
            continue
        if c == '\n':
            # Unterminated regex — bail out gracefully (rare)
            state = 'code'
        i += 1; continue
    if state == 're_class':
        if c == '\\' and nxt:
            i += 2; continue
        if c == ']':
            state = 're'; i += 1; continue
        i += 1; continue

    if state == 'lc':
        if c == '\n': state = 'code'
        i += 1; continue
    if state == 'bc':
        if c == '*' and nxt == '/': state = 'code'; i += 2; continue
        i += 1; continue
    for st, qc in (('sq', "'"), ('dq', '"'), ('bq', '`')):
        if state == st:
            if c == '\\' and nxt:
                i += 2
            elif c == qc:
                state = 'code'; i += 1
            else:
                i += 1
            break
    else:
        i += 1

print(f'depth left: {depth}')
if depth != 0 or errors:
    print('!! FILE UNBALANCED')
    for e in errors: print('   ' + e)
    sys.exit(1)
print('balanced OK')
