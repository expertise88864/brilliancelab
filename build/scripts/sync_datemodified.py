# -*- coding: utf-8 -*-
"""
Set every Article schema's `dateModified` to the file's last git commit date.
This signals content freshness to Google, which weighs recently-updated pages
higher for evergreen queries.

Strategy: for each blog/*.html, read `git log -1 --format=%cs <file>` to get
ISO date of last commit, then update any "dateModified":"YYYY-MM-DD" inside
the file's JSON-LD blocks.

Idempotent: only writes when the date actually changes. Preserves quoting and
spacing inside the JSON literal.
"""
from __future__ import annotations
import re, subprocess
from pathlib import Path

# --- Auto-locate the repo root so this script can be run from anywhere ---
import os as _os
_os.chdir(Path(__file__).resolve().parents[2])  # → BrillianceLab/
# -------------------------------------------------------------------------

ROOT = Path('.')
DM_RE = re.compile(r'("dateModified"\s*:\s*")(\d{4}-\d{2}-\d{2})(")')


def git_mtime(p: Path) -> str | None:
    try:
        r = subprocess.run(
            ['git', 'log', '-1', '--format=%cs', '--', p.as_posix()],
            capture_output=True, text=True, timeout=4)
        date = r.stdout.strip()
        return date if re.match(r'^\d{4}-\d{2}-\d{2}$', date) else None
    except Exception:
        return None


def patch(p: Path) -> tuple[bool, str | None, str | None]:
    src = p.read_text(encoding='utf-8')
    if 'dateModified' not in src:
        return False, None, None
    new_date = git_mtime(p)
    if not new_date:
        return False, None, None
    changed = False
    old_dates = set()
    def repl(m):
        nonlocal changed
        old_dates.add(m.group(2))
        if m.group(2) == new_date:
            return m.group(0)
        changed = True
        return m.group(1) + new_date + m.group(3)
    new_src = DM_RE.sub(repl, src)
    if changed:
        p.write_text(new_src, encoding='utf-8')
    return changed, list(old_dates)[0] if old_dates else None, new_date


def main():
    updated = 0
    for p in sorted(ROOT.glob('blog/*.html')):
        changed, old, new = patch(p)
        if changed:
            updated += 1
            print(f'  {p.name:<40} {old} → {new}')
    print(f'\n{updated} dateModified field(s) refreshed from git log')


if __name__ == '__main__':
    main()
