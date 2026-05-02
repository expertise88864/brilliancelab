# Build pipeline

Required tooling (install once on dev machine):

```bash
npm install
```

## Tailwind CSS — replace 350 KB CDN dev runtime with ~15 KB pre-built CSS

```bash
npm run css:build       # one-shot, minified
npm run css:watch       # rebuild on save
```

Outputs `assets/tw.css`. Then in HTML, swap:

```html
<!-- BEFORE -->
<script src="https://cdn.tailwindcss.com"></script>
<script>tailwind.config = { ... }</script>

<!-- AFTER -->
<link rel="preload" as="style" href="/assets/tw.css">
<link rel="stylesheet" href="/assets/tw.css">
```

Run `python ../../switch_to_static_css.py` from the project root to do this swap
across all 50+ pages automatically (only after `npm run css:build` succeeds).

## Pagefind — static site search index (replaces Fuse.js)

```bash
npm run css:build       # build CSS first so search.html renders correctly
npm run search:build    # crawls ./, writes ./_pagefind/
```

The Pagefind UI is wired into `search.html` via `<link rel="stylesheet" href="/_pagefind/pagefind-ui.css">`
and `<script src="/_pagefind/pagefind-ui.js">`.

## Lighthouse CI — performance budgets in CI

```bash
npm run lhci            # locally
```

Configured in `lighthouserc.json` (project root).
GitHub Action: `.github/workflows/lighthouse.yml` runs on every push.
