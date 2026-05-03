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

## Schema / E-E-A-T

| Script | When to run | What it does |
|---|---|---|
| `inject_author_schema.py` | After updating SAMEAS_* social URLs in the script | Injects centralised Person + Organization JSON-LD (with `sameAs`) into every page. |
| `inject_faqpage_multi.py` | After adding any `<h3>Q1: ...</h3><p>` blocks | Auto-extracts Q&A pairs and emits FAQPage schema. Idempotent. |
| `tighten_meta_desc.py`    | When `audit_seo.py` flags `desc-len` issues | Tightens meta descriptions to 100-158 SERP chars (CJK counted 2x). |
| `tighten_titles.py`       | When `audit_seo.py` flags `title-len` issues | Drops `\| BrillianceLab` brand suffix and em-dash subtitle to bring `<title>` into 55-65 SERP chars. Also updates `og:title` / `twitter:title` / JSON-LD `headline`. |
| `sync_datemodified.py`    | Pre-deploy or in CI | Updates every Article schema's `dateModified` to file's last `git log` date — content-freshness signal for Google. |
| `build_monthly_report.py` | Monthly (e.g. cron 1st of month) | Pulls Google News RSS for 4 silos (market / lab-grown / industry / policy), generates `/blog/diamond-news-YYYY-MM.html` with full template + Article schema. Editor fills "TODO commentary" blocks. |

## Sitemap / search hygiene

| Script | When to run | What it does |
|---|---|---|
| `build_sitemap_split.py` | After adding articles or hubs | Splits monolithic sitemap into `sitemap-pages.xml` / `sitemap-articles.xml` / `sitemap-amp.xml` + `sitemap.xml` (index). Search Console reports per-sitemap so you can see hubs vs articles indexing rates separately. |
| `build_image_sitemap.py` | After `build_og_images.py` | Builds `/og-sitemap.xml` listing every OG PNG for Google Image Search. Skips legacy `<slug>.png` when a hashed `<slug>.<hash>.png` exists. |
| `ping_indexnow.py` | After every deploy | POSTs URL list to IndexNow API (Bing/Yandex/Seznam/Naver) — typical indexing within hours. `--all` submits everything in sitemaps; pass paths to submit specific URLs. |
| `audit_seo.py` | Anytime | CSV audit of title length, meta desc length, h1 keyword overlap, first-paragraph length, h2 count, internal-link count, image alt. Outputs `audit_seo.csv` + flags issues to stdout. |
| `audit_canonicals.py` | Before deploy / in CI | Verifies every `<link rel="canonical">` matches the file's URL (handles AMP self-canonical-to-HTML rule). Exits non-zero on failure. |
| `inject_seo_essentials.py` | When adding articles | One-shot injects 4 SEO essentials per article: first-paragraph CTA to calculator, `<noscript>` visibility fallback, `fonts.gstatic.com` crossorigin preload, pre-baked BreadcrumbList JSON-LD. Idempotent. |

## PWA

| Script | When to run | What it does |
|---|---|---|
| `build_pwa_icons.py` | When the brand logo changes | Renders 192/512/maskable PNGs + apple-touch-icon (180); patches `manifest.json` and `<link rel="apple-touch-icon">`. |

## Sanity

| Script | When to run | What it does |
|---|---|---|
| `check_js.py` | Anytime | Proper JS state-machine brace balance on `blog/blog-shared.js`. Handles strings, templates, comments, regex literals. Exits non-zero on imbalance. |

## Pre-commit hook

One-time install of the pre-commit hook (runs JSON-LD parse + canonical
audit + JS brace check on every commit, blocks bad commits):

```bash
sh build/git-hooks/install.sh         # macOS / Linux / Git Bash
build\git-hooks\install.bat           # Windows cmd
```

Bypass once with `git commit --no-verify`.

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
