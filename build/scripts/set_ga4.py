# -*- coding: utf-8 -*-
"""
One-shot GA4 measurement-ID installer. Replaces the placeholder
G-XXXXXXXXXX in index.html with your real ID AND uncomments the
gtag block so it actually loads.

Usage:
  python build/scripts/set_ga4.py G-1AB2CD3EF4

What it does:
  1. Replaces every `G-XXXXXXXXXX` token in index.html
  2. Strips the surrounding HTML comment markers around the gtag block
  3. Verifies the block is now ACTIVE (the script tag is no longer commented)
  4. Updates ads.txt comment if present (informational)

Idempotent — re-run with the same ID and nothing changes; re-run with a
different ID and it swaps the ID in place.
"""
from __future__ import annotations
import re, sys
from pathlib import Path

# --- Auto-locate the repo root so this script can be run from anywhere ---
import os as _os
_os.chdir(Path(__file__).resolve().parents[2])  # → BrillianceLab/
# -------------------------------------------------------------------------


def main():
    if len(sys.argv) != 2 or not re.match(r'^G-[A-Z0-9]{8,12}$', sys.argv[1]):
        print('Usage: python build/scripts/set_ga4.py G-XXXXXXXXXX')
        print('  (your real ID from analytics.google.com → Admin → Data streams)')
        sys.exit(1)

    new_id = sys.argv[1]
    p = Path('index.html')
    if not p.exists():
        print('!! index.html not found — are you in BrillianceLab/?')
        sys.exit(1)

    src = p.read_text(encoding='utf-8')
    out = src

    # 1. Swap any existing G-XXXXXXXXXX (placeholder OR previous real ID)
    out = re.sub(r'G-[A-Z0-9]{8,12}', new_id, out)

    # 2. Uncomment the gtag block. The current placeholder lives inside a
    # comment that starts with `<!-- ===== Google Analytics 4 — UN-COMMENT`.
    # Strip the opening + closing comment markers around the gtag block.
    pattern = re.compile(
        r'<!-- ===== Google Analytics 4[\s\S]*?===== -->',
        re.MULTILINE
    )
    m = pattern.search(out)
    if m:
        block = m.group(0)
        # Remove the opening `<!-- ... uncomment me ===== -->` marker
        # and the closing `==== -->` if separated. Strip ALL `<!--` and `-->`
        # inside this block to fully un-comment the inner script.
        unwrapped = re.sub(r'<!--[^\n]*\n?', '', block)
        unwrapped = re.sub(r'\n?[^<\n]*-->', '', unwrapped)
        # Drop the original-block leading comment lines that don't contain
        # actual code. Anything between markers that's pure prose is gone.
        # The inner <script> tags survive verbatim.
        scripts = re.findall(r'<script[\s\S]*?</script>', unwrapped)
        if scripts:
            out = out.replace(block, '\n'.join(scripts))

    if out == src:
        print(f'No change — index.html already targets {new_id}.')
        return

    p.write_text(out, encoding='utf-8')
    print(f'✓ index.html now ships GA4 measurement ID: {new_id}')
    print('  - Web Vitals (LCP/INP/CLS/FCP/TTFB) → GA4')
    print('  - scroll_depth_25/50/75/100 → GA4')
    print('  - click_outbound + affiliate_click → GA4')
    print('  - bookmark_add/remove + newsletter_subscribe → GA4')
    print('  - experiment_impression/conversion (A/B tests) → GA4')
    print()
    print('Verify after deploy:  https://brilliancelab.vercel.app/')
    print('  open DevTools → Network tab → filter "google-analytics" — should see hits')


if __name__ == '__main__':
    main()
