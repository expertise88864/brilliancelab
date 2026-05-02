# -*- coding: utf-8 -*-
"""
Replace every `data-ad-slot="auto"` (and missing slot attrs) in blog articles
with the per-article slot IDs declared in build/adsense-slots.json.

Usage:
  1. Fill in the slot IDs in build/adsense-slots.json (replace TODO_AD_SLOT_*).
  2. python apply_adsense_slots.py [--dry]

Idempotent. Skips files where every <ins> already has a non-`auto` slot.
"""
from __future__ import annotations
import json, re, argparse
from pathlib import Path

# --- Auto-locate the repo root so this script can be run from anywhere ---
import os as _os, pathlib as _pl
_os.chdir(_pl.Path(__file__).resolve().parents[2])  # → BrillianceLab/
# -------------------------------------------------------------------------


ROOT = Path('.')
CFG  = ROOT / 'build' / 'adsense-slots.json'
INS_RE = re.compile(r'(<ins\s+class="adsbygoogle"\s[^>]*?data-ad-slot=")([^"]*)(")', re.I)


def load_cfg():
    raw = json.loads(CFG.read_text(encoding='utf-8'))
    return raw


def patch(path: Path, slots: list[str], default_top: str, default_bottom: str, dry: bool) -> int:
    src = path.read_text(encoding='utf-8')
    counter = {'i': 0, 'n': 0}

    def pick():
        i = counter['i']
        counter['i'] += 1
        if i < len(slots):    return slots[i]
        if i == 0:            return default_top
        return default_bottom

    def repl(m):
        new_slot = pick()
        if new_slot.startswith('TODO_'):
            return m.group(0)   # leave as-is until user fills config
        if m.group(2) == new_slot:
            return m.group(0)
        counter['n'] += 1
        return m.group(1) + new_slot + m.group(3)

    new = INS_RE.sub(repl, src)
    if not dry and new != src:
        path.write_text(new, encoding='utf-8')
    return counter['n']


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry', action='store_true')
    args = ap.parse_args()

    cfg = load_cfg()
    default_top    = cfg.get('_default_top',    'TODO_AD_SLOT_TOP')
    default_bottom = cfg.get('_default_bottom', 'TODO_AD_SLOT_BOTTOM')

    if default_top.startswith('TODO_') and default_bottom.startswith('TODO_'):
        print('!! All slot values still TODO_*. Edit build/adsense-slots.json first.')
        return

    total = 0
    for p in sorted(ROOT.glob('blog/*.html')):
        slug = p.stem
        slots = cfg.get(slug, [])
        n = patch(p, slots, default_top, default_bottom, args.dry)
        if n:
            total += n
            print(f'  {p.name}: {n} slot(s) updated')
    print(f'\n{total} <ins> slot(s) updated' + (' [dry]' if args.dry else ''))


if __name__ == '__main__':
    main()
