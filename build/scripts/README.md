# build/scripts/

Repeatable maintenance & build scripts. Each one auto-locates the repo root via
`Path(__file__).resolve().parents[2]` so it can be invoked from anywhere — but
**all path arguments and outputs are relative to `BrillianceLab/`**, since that
is the cwd the script chdirs into.

## Daily / per-article

| Script | When to run | What it does |
|---|---|---|
| `punct_fullwidth.py blog` | After authoring a new article | Converts half-width `,.;:?!()` to full-width inside Chinese text contexts (skips code/script/style/attrs). Always do `--dry` first to preview. |
| `harden_images.py` | After adding any `<img>` | Adds `loading="lazy" decoding="async"` to every image; first `<img>` per page gets `fetchpriority="high"`. |
| `build_og_images.py` | After adding/renaming an article | Renders 1200×630 OG PNGs (PIL + Windows CJK font) and rewrites every `og:image` / `twitter:image`. |
| `inject_preload.py` | Per new HTML | Adds `<link rel="preload">` for tw.css + Noto Serif Regular/Bold + AdSense preconnect + Clarity dns-prefetch. |

## Less frequent

| Script | When to run | What it does |
|---|---|---|
| `build_amp.py` | When the source article is rewritten | Regenerates 5 AMP pages (gia-guide, hearts-arrows-truth, budget-formula, lab-vs-natural, diamond-faq) from the inline PAGES dict. Edit the dict in the script first. |
| `build_hubs.py` | When silos restructure | Regenerates 5 hub pages (fundamentals/4Cs/purchase/proposal/care). Edit the inline HUBS list to change membership. |
| `inject_schema.py` | One-time (already applied) | Adds ItemList + Product + Review schema to 4 comparison articles. Idempotent. |

## After Tailwind/Pagefind/Fonts builds

| Script | When to run | What it does |
|---|---|---|
| `switch_to_static_css.py` | **Only AFTER `npm run css:build` succeeds.** | Replaces `<script src="cdn.tailwindcss.com">` + inline tailwind.config with `<link rel="stylesheet" href="/assets/tw.css">`. Backs up to `*.bak`. |
| `build_fonts.py` | After dropping Noto OTFs in `build/fonts-source/` | Subsets Noto Serif TC + Noto Sans TC against the 2,445-char charset and emits self-hosted woff2 + fonts.css. |
| `apply_adsense_slots.py` | After filling slot IDs in `build/adsense-slots.json` | Replaces every `data-ad-slot="auto"` with a per-article slot ID. |

## Sanity

| Script | When to run | What it does |
|---|---|---|
| `check_js.py` | Anytime | Brace/paren/bracket balance check on `blog/blog-shared.js`. Quick smoke test. |

## Order of operations for a fresh deploy

```bash
# 1. Build CSS, fonts, search index
cd BrillianceLab
npm install
npm run css:build
python build/scripts/build_fonts.py     # if fonts-source/ has the OTFs
npm run search:build

# 2. Apply HTML transforms that only make sense after build
python build/scripts/switch_to_static_css.py
python build/scripts/apply_adsense_slots.py     # only if you've filled slot IDs

# 3. Commit + push
./deploy.bat
```
