# -*- coding: utf-8 -*-
"""
Generate 5 topic-cluster hub pages so internal-link weight concentrates by
silo. Each hub:
  - explains the silo
  - lists every member article with one-line summary
  - has its own Article + ItemList schema
  - is canonical at /blog/hub-<silo>

Run once. Re-run safely overwrites the hub pages without touching anything else.
"""
from __future__ import annotations
import json, os
from pathlib import Path

# --- Auto-locate the repo root so this script can be run from anywhere ---
import os as _os, pathlib as _pl
_os.chdir(_pl.Path(__file__).resolve().parents[2])  # → BrillianceLab/
# -------------------------------------------------------------------------


ROOT   = Path('.')
DOMAIN = 'https://brilliancelab.vercel.app'

HUBS = [
    {
        'slug': 'hub-fundamentals',
        'title': '基礎篇 · 第一次買鑽石必讀',
        'subtitle': '從 GIA 到八心八箭,7 篇文章帶你建立鑽石判讀直覺',
        'desc': '第一次買鑽石必讀 7 篇:GIA 鑑定書、八心八箭、4Cs、培育鑽石、爭議陷阱。從零開始建立完整判讀直覺。',
        'order': [
            ('master-guide',          '購買總教學',         '14 階段入門路線,先讀這篇建立全局觀。'),
            ('gia-guide',             'GIA 鑑定書教學',     '5 分鐘看懂 6 個欄位,學會驗證真偽。'),
            ('hearts-arrows-truth',   '八心八箭真相',       '哪些 GIA Excellent 其實不及格 — Tolkowsky 數學告訴你。'),
            ('cert-comparison',       '證書比較',           'GIA / IGI / HRD / AGS 嚴謹度與市佔率對照。'),
            ('lab-vs-natural',        '天然 vs 培育鑽石',   '一樣是真鑽,差價 70% 的科學原理。'),
            ('diamond-faq',           '50 問 FAQ',          '新手最常問的 50 題,直接給答案不囉嗦。'),
            ('diamond-fun-facts',     '30 個冷知識',        '建立談資 — 鑽石歷史、奇聞、科學趣事。'),
            ('diamond-glossary',      '鑽石術語字典 30 詞', 'GIA / Tolkowsky / Pavé / Halo / 八心八箭 完整定義。'),
        ],
    },
    {
        'slug': 'hub-4cs',
        'title': '4Cs 拆解 · 把每一塊錢花在最划算的等級',
        'subtitle': 'Cut / Color / Clarity / Carat 四篇深度,加上螢光、內含物、形狀的子文',
        'desc': '逐一拆解 4Cs 評級系統 — 哪一級才是 CP 值甜蜜點?克拉與面積關係?螢光該不該避?內含物 8 種怎麼看?',
        'order': [
            ('diamond-color',         '顏色等級 D-Z',       'D 跟 G 真的看得出嗎?23 階完整光譜。'),
            ('diamond-clarity',       '淨度等級 FL-I',      'VS1 跟 VS2 肉眼真的看得出?VS2 為什麼是甜蜜點。'),
            ('diamond-carat-size',    '克拉與視覺尺寸',     '0.5、0.7、1 克拉差幾 mm? 視覺與直徑平方關係。'),
            ('diamond-shapes',        '10 種鑽石形狀',      '圓形、橢圓、墊形、公主方完整對照與光學差異。'),
            ('round-cut-deep-dive',   '圓形明亮車工解析',   '57+1 面的數學起源,Tolkowsky 1919 推導。'),
            ('fancy-cuts-guide',      '花式車工指南',       '橢圓 / 梨形 / 馬眼 / 祖母綠的領結現象與避雷。'),
            ('fluorescence-deep-dive','螢光反應深度解析',   'None / Faint / Medium / Strong 對價格與外觀的影響。'),
            ('inclusions-types-guide','內含物 8 種圖解',    'Plotting 圖看內含物位置,辨別 SI1 跟 VS2 的關鍵。'),
        ],
    },
    {
        'slug': 'hub-purchase',
        'title': '購買實戰 · 預算到下單的完整流程',
        'subtitle': '預算、品牌、分期、二手、詐騙避雷 7 篇',
        'desc': '從決定預算、比較品牌、分期付款利率,到二手鑽戒地雷與詐騙避雷 — 真正下單前必看的 7 篇實戰文。',
        'order': [
            ('budget-formula',        'BPD 預算公式',       '分數 × √克拉 ÷ 價格 = 每元閃光值。'),
            ('engagement-guide',      '結婚鑽戒 9 步驟',    '從決定預算到求婚當天的完整 SOP。'),
            ('taiwan-brands',         '台灣鑽戒品牌完整比較', '12 家 Dcard / PTT 推薦最多的鑽戒品牌對照(點睛品 / ALUXE / I-PRIMO / 銀座白石 等)。'),
            ('diamond-financing',     '分期付款指南',       '0% 利率背後的隱藏成本,5 種方案比較。'),
            ('secondhand-rings',      '二手婚戒指南',       '便宜 30-50% 的祕密,7 個地雷怎麼避。'),
            ('diamond-scams',         '鑽石詐騙 TOP 10',    '銀樓、網購、夜市最常見手法完整避雷。'),
            ('moissanite-vs-cz-vs-lab', '真假鑽辨識',       '莫桑石 / CZ / 培育 / 天然 4 種 6 招辨識。'),
            ('diamond-1ct-price-2026', '一克拉鑽石價格查表', '從培育鑽 NT$7 萬到 Cartier NT$130 萬完整價位帶。'),
            ('dcard-ptt-recommendations', 'Dcard / PTT 推薦排行榜', '30 篇真實心得統計,點睛品 / I-PRIMO / 銀座白石誰被推最多。'),
        ],
    },
    {
        'slug': 'hub-proposal',
        'title': '求婚與婚戒 · 從尺寸到求婚當天',
        'subtitle': '時間軸、求婚詞、戒圍、戒台、男士戒指 7 篇',
        'desc': '12 個月時間軸、50 句求婚詞、7 種偷量戒圍法、5 種戒指類型、6 種金屬、男士戒指、LGBTQ+ — 求婚相關 7 篇文章一站式。',
        'order': [
            ('engagement-timeline',   '12 個月時間軸',      '從訂婚到結婚,每月該完成什麼。'),
            ('proposal-speech',       '求婚詞 50 句',       '5 大主題場景的求婚台詞範本。'),
            ('ring-sizing',           '戒圍完整指南',       '7 種無痕量法,女友不會發現。'),
            ('wedding-bands',         '5 種戒指完整指南',   '訂婚 / 結婚 / 對戒 / 永恆 / 紀念差別。'),
            ('wedding-metals',        '婚戒材質完整指南',   '鉑金、18K、玫瑰金、黃金、鈦的優劣對照。'),
            ('mens-engagement-rings', '男士訂婚戒指南',     '男生也戴訂婚戒嗎?6 種主流款式。'),
            ('lgbtq-rings',           '同志婚戒指南',       'LGBTQ+ 配對戒設計與選擇思路。'),
            ('proposal-vs-wedding-vs-eternity', '4 種戒指完整差別', '求婚戒 / 結婚戒 / 對戒 / 永恆戒 + 日韓 vs 歐美傳統。'),
        ],
    },
    {
        'slug': 'hub-care',
        'title': '保養與市場 · 戴 30 年還像新的',
        'subtitle': '保養、保險、回收、刻字、傳家、市場趨勢 7 篇',
        'desc': '婚戒不是買了就結束 — 保養、失竊處理、轉售真相、市場價格趨勢、傳家鑽石重做、6 種戒台保養差異一站式。',
        'order': [
            ('diamond-care',          '鑽石保養全攻略',     '7 個習慣讓鑽石戴 30 年還像新的。'),
            ('ring-insurance',        '婚戒保險與失竊',     '24 小時 SOP 與 5 大保險公司比較。'),
            ('diamond-resale',        '鑽石回收與保值',     '為什麼 30 萬鑽戒只能換回 10 萬。'),
            ('engraving-personalization', '婚戒刻字指南',   '8 種字體 + 50 句範例文案。'),
            ('heirloom-redesign',     '傳家鑽石重做',       '繼承鑽戒怎麼改設計,避免拆損價值。'),
            ('prong-settings-guide',  '7 種戒台爪鑲',       '六爪、四爪、包邊、Halo、Pavé 保養差異。'),
            ('diamond-price-trends',  '2026-2030 價格趨勢', '培育鑽降價 / De Beers 拆分 / 印度產能。'),
        ],
    },
]


HEAD_TEMPLATE = '''<!doctype html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8" />
<!-- BL_PRELOAD -->
<link rel="preload" as="style" href="/assets/tw.css">
<link rel="preload" as="font" type="font/woff2" href="/assets/fonts/NotoSerifTC-Regular.subset.woff2" crossorigin>
<link rel="preload" as="font" type="font/woff2" href="/assets/fonts/NotoSerifTC-Bold.subset.woff2" crossorigin>
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{title} | BrillianceLab 鑽石實驗室</title>
<meta name="description" content="{desc}" />
<meta name="theme-color" content="#faf8f3" />
<link rel="canonical" href="{canonical}" />
<link rel="alternate" hreflang="x-default" href="{canonical}" />
<link rel="alternate" hreflang="zh-TW"     href="{canonical}" />
<link rel="alternate" type="application/rss+xml" title="BrillianceLab Blog RSS" href="/blog/feed.xml" />
<link rel="icon" type="image/svg+xml" href="/icon.svg" />
<meta property="og:type" content="article" />
<meta property="og:url" content="{canonical}" />
<meta property="og:title" content="{title} | BrillianceLab" />
<meta property="og:description" content="{desc}" />
<meta property="og:image" content="{og_image}" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="{title} | BrillianceLab" />
<meta name="twitter:description" content="{desc}" />
<meta name="twitter:image" content="{og_image}" />

<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-8223268344248663" crossorigin="anonymous"></script>
<meta name="google-adsense-account" content="ca-pub-8223268344248663" />

<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Noto+Serif+TC:wght@500;600;700;800&display=swap" rel="stylesheet" />

<script src="https://cdn.tailwindcss.com"></script>

<style>
  :root{{--bg:#faf8f3;--ink:#1a1d2e;--ink-2:#4a4d5e;--muted:#7e8194;--gold:#c9a45c;--gold-deep:#8a6e30;--gold-soft:#fbf3df;--border:#ebe6dc;--line:#f1ede3}}
  *{{box-sizing:border-box;margin:0;padding:0}}
  html,body{{background:var(--bg);color:var(--ink);font-family:'Inter','Noto Serif TC','Microsoft JhengHei',Georgia,serif}}
  body::before{{content:'';position:fixed;inset:0;pointer-events:none;z-index:-1;background:radial-gradient(800px 500px at 12% -8%,rgba(201,164,92,.16),transparent 60%),linear-gradient(180deg,#faf8f3 0%,#fffdf7 40%,#faf8f3 100%)}}
  .gold-text{{background:linear-gradient(180deg,#c9a45c,#8a6e30);-webkit-background-clip:text;background-clip:text;color:transparent}}
  header.sticky{{position:sticky;top:0;background:rgba(250,248,243,.92);backdrop-filter:blur(10px);border-bottom:1px solid var(--border);z-index:10}}
  .hub-card{{display:block;padding:22px 24px;background:#fff;border:1px solid var(--border);border-radius:16px;text-decoration:none;color:inherit;transition:transform .25s ease,box-shadow .25s ease,border-color .2s}}
  .hub-card:hover{{border-color:rgba(201,164,92,.5);transform:translateY(-3px);box-shadow:0 14px 32px -18px rgba(138,110,48,.4)}}
  .hub-num{{font-family:'Noto Serif TC',Georgia,serif;font-weight:700;font-size:24px;color:#5e4a1f;background:linear-gradient(180deg,#fbf3df,#f5e9d0);width:48px;height:48px;border-radius:12px;display:flex;align-items:center;justify-content:center;border:1px solid rgba(201,164,92,.4);flex-shrink:0}}
  .hub-title{{font-family:'Noto Serif TC',Georgia,serif;font-weight:700;font-size:18px;color:var(--ink);margin-bottom:4px}}
  .hub-body{{font-size:13.5px;color:var(--ink-2);line-height:1.7}}
</style>

<script type="application/ld+json">
{ld_article}
</script>
<script type="application/ld+json">
{ld_itemlist}
</script>
<script type="application/ld+json">
{ld_breadcrumb}
</script>
</head>
<body>

<header class="sticky">
  <div class="max-w-5xl mx-auto px-5 sm:px-8 py-3 flex items-center justify-between">
    <a href="/" class="inline-flex items-center gap-2 text-decoration-none" style="text-decoration:none;color:inherit">
      <svg viewBox="0 0 24 24" width="22" height="22" fill="none"><path d="M3.5 9 12 3l8.5 6-8.5 12L3.5 9Z" stroke="url(#g)" stroke-width="1.4" stroke-linejoin="round"/><defs><linearGradient id="g" x1="0" x2="1" y1="0" y2="1"><stop stop-color="#d4b87a"/><stop offset="1" stop-color="#8a6e30"/></linearGradient></defs></svg>
      <span class="font-display font-bold gold-text">BrillianceLab</span>
    </a>
    <nav class="text-[12px] uppercase tracking-[.18em] text-ink-700 hidden sm:flex gap-5">
      <a href="/" style="color:inherit;text-decoration:none">主頁工具</a>
      <a href="/blog/" style="color:inherit;text-decoration:none">部落格</a>
      <a href="/blog/topics" style="color:inherit;text-decoration:none">主題索引</a>
      <a href="/search" style="color:inherit;text-decoration:none">搜尋</a>
    </nav>
    <div id="langToggle"></div>
  </div>
</header>

<main class="max-w-5xl mx-auto px-5 sm:px-8 py-12">

  <nav class="text-[11px] uppercase tracking-[.22em] text-ink-500 mb-3" aria-label="Breadcrumb">
    <a href="/" style="color:inherit;text-decoration:none">首頁</a> · <a href="/blog/" style="color:inherit;text-decoration:none">部落格</a> · <span style="color:#8a6e30">{title}</span>
  </nav>

  <h1 class="font-display font-bold leading-[1.15] text-[34px] sm:text-[48px]">{title}</h1>
  <p class="mt-5 max-w-2xl text-[15.5px] sm:text-[17px] text-ink-700 leading-[1.85]">{subtitle}</p>

  <article id="proseZh" data-pagefind-body data-pagefind-meta="slug:{slug}" class="mt-10">
    <div style="display:grid;gap:14px;grid-template-columns:repeat(auto-fit,minmax(280px,1fr))">
      {cards}
    </div>
  </article>

  <section class="mt-12 p-6 rounded-2xl border border-[var(--border)] bg-[var(--gold-soft)]/40">
    <h2 class="font-display font-bold text-[20px] mb-3">下一步:動手算分</h2>
    <p class="text-[14.5px] text-ink-700 mb-4">看完 {n} 篇之後,把候選鑽石的 4C 數據輸入 BrillianceLab 計算器,30 秒看到光學評分與 BPD 性價比。</p>
    <a href="/" class="inline-flex items-center gap-2 px-5 py-2.5 rounded-full bg-gradient-to-b from-gold-300 to-gold-600 text-white font-semibold text-[14px]" style="text-decoration:none">🛠 開始計算 →</a>
  </section>

</main>

<footer class="border-t border-[var(--border)] bg-ivory-100/60">
  <div class="max-w-5xl mx-auto px-5 sm:px-8 py-10 text-[12px] text-ink-500 flex flex-wrap items-center justify-between gap-4">
    <div>© <span id="yr"></span> BrillianceLab · 鑽石實驗室</div>
    <div class="flex gap-4 uppercase tracking-[.18em]">
      <a href="/blog/" style="color:inherit;text-decoration:none">部落格</a>
      <a href="/blog/topics" style="color:inherit;text-decoration:none">主題索引</a>
      <a href="/search" style="color:inherit;text-decoration:none">搜尋</a>
    </div>
  </div>
</footer>

<script src="/blog/blog-shared.js" defer></script>
<script defer>document.addEventListener('DOMContentLoaded', () => BL.initBlog({{ slug:'{slug}' }}));</script>

</body>
</html>
'''


def build(hub: dict) -> str:
    canonical = f'{DOMAIN}/blog/{hub["slug"]}'
    cards = []
    for i, (slug, title, summary) in enumerate(hub['order'], 1):
        cards.append(
            f'<a class="hub-card" href="/blog/{slug}">'
            f'<div style="display:flex;gap:14px;align-items:start">'
            f'<div class="hub-num">{i:02d}</div>'
            f'<div><div class="hub-title">{title}</div>'
            f'<div class="hub-body">{summary}</div></div></div></a>'
        )
    article_ld = {
        '@context':'https://schema.org',
        '@type':'Article',
        'headline': hub['title'],
        'description': hub['desc'],
        'datePublished': '2026-05-03',
        'dateModified':  '2026-05-03',
        'mainEntityOfPage': canonical,
        'image': f'{DOMAIN}/og/{hub["slug"]}.png',
        'author':    {'@type':'Organization','name':'BrillianceLab','url':DOMAIN+'/'},
        'publisher': {'@type':'Organization','name':'BrillianceLab','logo':{'@type':'ImageObject','url':DOMAIN+'/icon.svg'}},
    }
    itemlist_ld = {
        '@context':'https://schema.org',
        '@type':'ItemList',
        'name':  hub['title'],
        'numberOfItems': len(hub['order']),
        'itemListOrder': 'https://schema.org/ItemListOrderAscending',
        'itemListElement': [
            {'@type':'ListItem','position':i+1,'name':t,'url':f'{DOMAIN}/blog/{s}'}
            for i,(s,t,_) in enumerate(hub['order'])
        ],
    }
    breadcrumb_ld = {
        '@context':'https://schema.org','@type':'BreadcrumbList',
        'itemListElement':[
            {'@type':'ListItem','position':1,'name':'首頁','item':DOMAIN+'/'},
            {'@type':'ListItem','position':2,'name':'部落格','item':DOMAIN+'/blog/'},
            {'@type':'ListItem','position':3,'name':hub['title'],'item':canonical},
        ]
    }
    return HEAD_TEMPLATE.format(
        title=hub['title'], desc=hub['desc'], subtitle=hub['subtitle'],
        canonical=canonical, og_image=f'{DOMAIN}/og/{hub["slug"]}.png',
        slug=hub['slug'], n=len(hub['order']),
        cards='\n      '.join(cards),
        ld_article=json.dumps(article_ld, ensure_ascii=False, separators=(',',':')),
        ld_itemlist=json.dumps(itemlist_ld, ensure_ascii=False, separators=(',',':')),
        ld_breadcrumb=json.dumps(breadcrumb_ld, ensure_ascii=False, separators=(',',':')),
    )


def main():
    out_dir = ROOT / 'blog'
    for hub in HUBS:
        path = out_dir / f'{hub["slug"]}.html'
        path.write_text(build(hub), encoding='utf-8')
        print(f'  wrote {path.relative_to(ROOT)}  ({len(hub["order"])} articles)')


if __name__ == '__main__':
    main()
