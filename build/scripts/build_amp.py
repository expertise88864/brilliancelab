# -*- coding: utf-8 -*-
"""
Build AMP-lite pages for 5 high-traffic articles.
Each AMP page is a fast, ad-monetised summary that links to the full HTML article.
The shared template mirrors amp/blog/master-guide.html (already in the repo).
"""
from __future__ import annotations
import os, json, datetime

# --- Auto-locate the repo root so this script can be run from anywhere ---
import os as _os, pathlib as _pl
_os.chdir(_pl.Path(__file__).resolve().parents[2])  # → BrillianceLab/
# -------------------------------------------------------------------------


DOMAIN = 'https://brilliancelab.vercel.app'

PAGES = [
    {
        'slug': 'gia-guide',
        'label': '★ AMP 基礎篇 · 第 1 課',
        'title': '如何看懂 GIA 鑑定書',
        'accent': '5 分鐘完整解析',
        'description': '從零開始看懂 GIA 鑽石鑑定書 — 4Cs、比例圖、Polish/Symmetry/Fluorescence、Report Check 真偽驗證,5 分鐘 6 個欄位全部搞懂。AMP 行動加速版。',
        'lead': 'GIA 鑑定書一張看似嚇人,其實只有 6 個欄位真的影響你的判斷。本篇用 5 分鐘把整份報告拆完,還會教你怎麼用線上 Report Check 驗證真偽。',
        'meta': '最後更新:2026 年 5 月 2 日 · 約 1,800 字 · 6 分鐘閱讀 · AMP 行動加速版',
        'word_count': 1800,
        'sections': [
            ('GIA 是什麼', 'GIA(Gemological Institute of America,美國寶石學院)是 1953 年 4Cs 評級系統的發明者,也是全球公認最嚴謹的鑽石實驗室。一張正本 GIA 報告等於是一顆鑽石的「身分證」,沒有它幾乎無法在二級市場流通。'),
            ('看完這 6 欄就夠了', '<ul><li><strong>Carat Weight</strong> — 克拉重量,1 ct = 0.2 g</li><li><strong>Color Grade</strong> — D 最白,Z 最黃,推薦 G-H 甜蜜點</li><li><strong>Clarity Grade</strong> — FL 完美無瑕,推薦 VS1-VS2</li><li><strong>Cut Grade</strong> — Excellent / Very Good / Good。本欄影響閃光最大</li><li><strong>Polish &amp; Symmetry</strong> — 兩者皆 Excellent 才是真頂級</li><li><strong>Fluorescence</strong> — None 最貴,Faint 最 CP 值</li></ul>'),
            ('真 Excellent vs 邊緣 Excellent', 'GIA Excellent 範圍其實很寬,有些 Excellent 鑽石其實是「邊緣值」 — 視覺亮度比真八心八箭差 15-25%。判別方法:看比例圖中的 Crown Angle(34-35°)、Pavilion Angle(40.6-41°)、Table %(54-58%)三項是否落在「Tolkowsky 黃金區間」。'),
            ('Report Check 驗證真偽', '到 https://www.gia.edu/report-check 輸入報告編號(Report No.,7 位數字)+ 克拉數,會回傳完整 4C 與比例圖。如果驗不到 → 假證。'),
        ],
        'cta_text': '想知道你的鑽石屬於「真 Excellent」嗎？把 4C 數據輸入 BrillianceLab,30 秒看到光學評分。',
        'related': [
            ('hearts-arrows-truth', '八心八箭真相'),
            ('cert-comparison', 'GIA / IGI / HRD 證書比較'),
            ('diamond-color',  '顏色等級 D-Z 完整解析'),
            ('diamond-clarity', '淨度等級 FL-I 完整解析'),
        ],
        'prev': ('master-guide',          '購買總教學'),
        'next': ('hearts-arrows-truth',   '八心八箭真相'),
    },

    {
        'slug': 'hearts-arrows-truth',
        'label': '★ AMP 基礎篇 · 第 2 課',
        'title': '八心八箭真相',
        'accent': 'GIA Excellent 也分等級',
        'description': '哪些 GIA Excellent 其實不及格 — 用 Tolkowsky 數學驗證真假八心八箭,告訴你業務話術的盲點與光學差距。AMP 行動加速版。',
        'lead': '所有業務都會說「這顆是 GIA Excellent + 八心八箭」,但 GIA Excellent 範圍寬到讓「邊緣值」也能掛這個名號。本篇用 4 個實際案例 + 數學公式,告訴你怎麼分。',
        'meta': '最後更新:2026 年 5 月 2 日 · 約 2,000 字 · 7 分鐘閱讀 · AMP 行動加速版',
        'word_count': 2000,
        'sections': [
            ('Tolkowsky 黃金比例', '1919 年數學家 Marcel Tolkowsky 推導出鑽石「最完美光學折射」的比例:Table 53-58%、Crown Angle 34.5°、Pavilion Angle 40.75°、Total Depth 59-62.3%。八心八箭只會出現在這個範圍內。'),
            ('GIA Excellent 的盲區', 'GIA Excellent 涵蓋 Table 52-62%、Crown 31-37°、Pavilion 40.2-41.8°,範圍比 Tolkowsky 寬一倍。在 GIA Excellent 內,可能有 30% 的鑽石其實照不出完整八心八箭。'),
            ('4 個案例對比', '<strong>案例 A:</strong>真八心八箭(Table 56% / Crown 34.8°),光學亮度 100%。<br><strong>案例 B:</strong>GIA Excellent 邊緣值(Table 61% / Crown 36.5°),光學亮度 78%。<br><strong>案例 C:</strong>Very Good 但比例佳(Table 57% / Crown 34.5°),光學亮度 92%。<br><strong>案例 D:</strong>偽八心八箭(對稱性差),光學亮度 70%。'),
            ('該怎麼買才對', '不要只看 GIA 那一行 Excellent。看比例圖三項是否都在 Tolkowsky 區間,再加上 Polish &amp; Symmetry 都是 Excellent + Heart &amp; Arrow Scope 實拍。'),
        ],
        'cta_text': '想驗證你的候選鑽石是「真 H&amp;A」嗎？把 Table%、Crown°、Pavilion° 輸入 BrillianceLab,公式直接告訴你光學亮度評分。',
        'related': [
            ('round-cut-deep-dive', '圓形明亮車工深度解析'),
            ('gia-guide',           'GIA 鑑定書教學'),
            ('budget-formula',      'BPD 預算公式'),
            ('fluorescence-deep-dive','螢光反應深度解析'),
        ],
        'prev': ('gia-guide',     'GIA 鑑定書教學'),
        'next': ('budget-formula', 'BPD 預算公式'),
    },

    {
        'slug': 'budget-formula',
        'label': '★ AMP 數學公式 · 第 3 課',
        'title': 'BPD 預算公式',
        'accent': '30 萬以下挑最閃鑽石',
        'description': '用「分數 × √克拉 ÷ 價格」的 BPD 公式,告訴你 30 萬預算內哪一顆鑽石每塊錢買到最強閃光。AMP 行動加速版。',
        'lead': '預算 NT$30 萬要挑哪顆鑽石最閃？答案不是「克拉越大越好」也不是「品牌越貴越好」。用 BrillianceLab 的 BPD(Brilliance Per Dollar)公式,可以把任何鑽石量化成「每元閃光值」直接比較。',
        'meta': '最後更新:2026 年 5 月 2 日 · 約 2,200 字 · 8 分鐘閱讀 · AMP 行動加速版',
        'word_count': 2200,
        'sections': [
            ('BPD 公式長什麼樣', '<strong>BPD = (光學分數 × √克拉) ÷ 價格 × 10,000</strong><br>光學分數來自 4C 加權:Cut 50% + Color 20% + Clarity 20% + 螢光修正 10%。√克拉是因為視覺面積與直徑平方成正比。'),
            ('30 萬實戰對照', '<strong>選項 A:</strong>0.85 ct E VS2 真八心八箭 NT$28 萬 → BPD 39<br><strong>選項 B:</strong>1.00 ct G VS1 邊緣 Excellent NT$30 萬 → BPD 28<br><strong>選項 C:</strong>1.20 ct H SI1 Very Good NT$29 萬 → BPD 25<br>結論:選項 A 比 B 多閃 39%,儘管克拉小 0.15。'),
            ('該砍哪一個 C', '視覺影響排序:<strong>Cut &gt; Color &gt; Clarity &gt; Carat</strong>。砍 Carat 最划算 — 從 1.0 砍到 0.85 省 25% 預算,但視覺只小 5%。砍 Cut 最虧 — 直接損失閃光感受。'),
            ('品牌溢價要不要付', 'Tiffany / Cartier / I-PRIMO 同一顆鑽石價格是裸鑽 1.5-3.5 倍。如果預算 50 萬以下,通常付品牌溢價會讓你多砍 0.2 ct,得不償失。50 萬以上才開始建議考慮品牌。'),
        ],
        'cta_text': '把候選鑽石的 4C 數據輸入 BrillianceLab,自動算出 BPD,3 顆鑽石並排比較哪顆閃。',
        'related': [
            ('hearts-arrows-truth', '八心八箭真相'),
            ('diamond-carat-size',  '克拉與視覺尺寸'),
            ('lab-vs-natural',      '天然 vs 培育鑽石'),
            ('engagement-guide',    '結婚鑽戒 9 步驟'),
        ],
        'prev': ('hearts-arrows-truth', '八心八箭真相'),
        'next': ('lab-vs-natural',      '天然 vs 培育鑽石'),
    },

    {
        'slug': 'lab-vs-natural',
        'label': '★ AMP 基礎篇 · 第 4 課',
        'title': '天然 vs 培育鑽石',
        'accent': '一樣是真鑽,差價 70%',
        'description': '同樣的化學成分、同樣的折射率、同樣的硬度 — 為什麼培育鑽石比天然便宜 70%？2026 年最新市場狀況、保值差異、誰適合誰。AMP 行動加速版。',
        'lead': '培育鑽石(Lab-Grown)不是「假鑽」也不是「合成石」 — 它就是真鑽,只是在實驗室「種」出來的。物理、光學、化學跟天然鑽完全相同,連 GIA 也認證,但價差到 70%。怎麼選？',
        'meta': '最後更新:2026 年 5 月 2 日 · 約 2,100 字 · 7 分鐘閱讀 · AMP 行動加速版',
        'word_count': 2100,
        'sections': [
            ('物理上完全相同', '<strong>化學成分</strong>:純碳 C(兩者一樣)<br><strong>硬度</strong>:Mohs 10(兩者一樣)<br><strong>折射率</strong>:2.42(兩者一樣)<br><strong>色散值</strong>:0.044(兩者一樣)<br>差別只有<strong>形成方式</strong> — 一個地下 30 億年,一個 HPHT/CVD 實驗室 4 週。'),
            ('價格差 70%', '同樣 1ct G VS1 真八心八箭:<br><strong>天然</strong> NT$25-35 萬<br><strong>培育</strong> NT$8-12 萬<br><strong>2026 預測</strong>:培育鑽價格還會再降 20-30%,因為產能持續擴大。'),
            ('保值大不同', '天然鑽石回收率約 30-40%(NT$30 萬鑽戒只能換 10 萬)<br>培育鑽石回收率不到 10%(NT$10 萬鑽戒只能換 1 萬)<br>但問題是 — 兩者「賠掉的金額」其實接近。'),
            ('誰適合誰', '<strong>選天然</strong>:預算 50 萬以上 / 重視傳家 / 想要「稀有感」<br><strong>選培育</strong>:預算 20 萬以下 / 想要更大克拉 / 環保意識強 / 重視 CP 值'),
        ],
        'cta_text': '不確定該選哪種？把預算和需求輸入 BrillianceLab 計算器,自動推薦最適合你的選擇。',
        'related': [
            ('budget-formula',         'BPD 預算公式'),
            ('sustainable-diamonds',   '道德鑽石指南'),
            ('moissanite-vs-cz-vs-lab','真假鑽辨識'),
            ('diamond-resale',         '鑽石回收與保值'),
        ],
        'prev': ('budget-formula',  'BPD 預算公式'),
        'next': ('diamond-color',   '顏色等級 D-Z'),
    },

    {
        'slug': 'diamond-faq',
        'label': '★ AMP 常見問題 · 第 14 課',
        'title': '鑽石購買 50 問 FAQ',
        'accent': '4C、預算、品牌、保養一次解答',
        'description': '鑽石新手最常問的 50 個問題,從 4C、預算、品牌、培育鑽、認證、求婚、保養到轉售一次解答 — 每題直接給答案不囉嗦,AMP 行動加速版。',
        'lead': '不想看 14 篇長文？這裡是 50 個最常被問的問題,直接給你答案。問題越靠前面越熱門 — 想知道某個主題的詳細邏輯,點對應的全文連結即可。',
        'meta': '最後更新:2026 年 5 月 2 日 · 約 2,400 字 · 9 分鐘閱讀 · AMP 行動加速版',
        'word_count': 2400,
        'sections': [
            ('預算與選擇', '<ul><li><strong>30 萬只能買多大？</strong> — 0.85-1.0 ct GVS1 真八心八箭都可</li><li><strong>該不該買培育鑽？</strong> — 預算 20 萬以下強烈建議</li><li><strong>品牌溢價值不值？</strong> — 50 萬以下 No,以上 Maybe</li><li><strong>分期付款可不可以？</strong> — 0% 利率有隱藏成本,看分期手續費</li></ul>'),
            ('4C 等級', '<ul><li><strong>D 跟 G 看得出嗎？</strong> — 在白紙上看得出,正常配戴看不出</li><li><strong>VVS 跟 VS 差很多嗎？</strong> — 肉眼完全看不出</li><li><strong>螢光是壞事嗎？</strong> — Faint/Medium 都 OK,Strong 才扣分</li><li><strong>克拉跟視覺面積關係？</strong> — √克拉成正比</li></ul>'),
            ('證書與真偽', '<ul><li><strong>GIA / IGI / HRD 哪個好？</strong> — GIA 最嚴最值錢</li><li><strong>怎麼驗證 GIA 真偽？</strong> — gia.edu/report-check</li><li><strong>銀樓的證書能信嗎？</strong> — 自家證書很多寬鬆,只認三大實驗室</li></ul>'),
            ('保養與保險', '<ul><li><strong>多久該洗一次？</strong> — 1 個月 1 次溫水中性洗潔劑</li><li><strong>戴著洗手會壞嗎？</strong> — 不會,但會卡污</li><li><strong>該保險嗎？</strong> — NT$20 萬以上的鑽戒值得</li></ul>'),
            ('還有 38 個問題', '本 AMP 版只摘錄 12 題,完整 50 題請看全文版,每題都有展開的詳細解答 + 跨文連結。'),
        ],
        'cta_text': '看完還有問題？用 BrillianceLab 計算器把候選鑽石跑一遍,90% 的疑問會自動消失。',
        'related': [
            ('master-guide',     '購買總教學'),
            ('gia-guide',        'GIA 鑑定書教學'),
            ('budget-formula',   'BPD 預算公式'),
            ('engagement-guide', '結婚鑽戒 9 步驟'),
        ],
        'prev': ('lab-vs-natural', '天然 vs 培育鑽石'),
        'next': ('master-guide',   '回到主幹'),
    },
]


TEMPLATE = '''<!doctype html>
<html ⚡ lang="zh-TW">
<head>
<meta charset="utf-8">
<title>{title} · {accent} | BrillianceLab AMP</title>
<link rel="canonical" href="{canonical}">
<link rel="alternate" hreflang="x-default" href="{canonical}">
<meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">
<meta name="description" content="{description}">
<style amp-boilerplate>body{{-webkit-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-moz-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-ms-animation:-amp-start 8s steps(1,end) 0s 1 normal both;animation:-amp-start 8s steps(1,end) 0s 1 normal both}}@-webkit-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-moz-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-ms-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-o-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}</style><noscript><style amp-boilerplate>body{{-webkit-animation:none;-moz-animation:none;-ms-animation:none;animation:none}}</style></noscript>
<script async src="https://cdn.ampproject.org/v0.js"></script>
<script async custom-element="amp-auto-ads" src="https://cdn.ampproject.org/v0/amp-auto-ads-0.1.js"></script>

<style amp-custom>
:root{{--bg:#faf8f3;--ink:#1a1d2e;--ink-2:#4a4d5e;--muted:#7e8194;--gold:#c9a45c;--gold-deep:#8a6e30;--gold-soft:#fbf3df;--border:#ebe6dc}}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{background:var(--bg);color:var(--ink);font-family:"PingFang TC","Microsoft JhengHei",Georgia,serif;line-height:1.85}}
header{{position:sticky;top:0;background:rgba(250,248,243,.92);border-bottom:1px solid var(--border);padding:14px 18px;display:flex;align-items:center;justify-content:space-between;z-index:10;backdrop-filter:blur(10px)}}
.logo{{font-weight:700;font-size:16px;background:linear-gradient(180deg,#c9a45c,#8a6e30);-webkit-background-clip:text;background-clip:text;color:transparent;text-decoration:none}}
.full-link{{font-size:11px;color:var(--gold-deep);text-decoration:underline;letter-spacing:.05em}}
main{{max-width:720px;margin:0 auto;padding:24px 20px 60px}}
.label{{font-size:11px;letter-spacing:.24em;text-transform:uppercase;color:var(--muted);margin-bottom:8px}}
h1{{font-size:30px;font-weight:800;line-height:1.2;letter-spacing:-.01em;margin-bottom:14px}}
h1 .accent{{display:block;background:linear-gradient(180deg,#c9a45c,#8a6e30);-webkit-background-clip:text;background-clip:text;color:transparent;font-size:22px;margin-top:4px}}
.lead{{font-size:15.5px;color:var(--ink-2);line-height:1.85;margin-bottom:20px}}
.meta{{font-size:11.5px;color:var(--muted);padding-bottom:18px;border-bottom:1px dashed var(--border);margin-bottom:24px}}
h2{{font-size:21px;font-weight:700;margin:32px 0 12px;border-left:3px solid var(--gold);padding-left:14px;color:var(--ink)}}
p{{margin:14px 0;color:var(--ink-2);font-size:15.5px}}
strong{{color:var(--ink);font-weight:700}}
em{{font-style:normal;color:var(--gold-deep);font-weight:600}}
a{{color:var(--gold-deep);text-decoration:underline;text-underline-offset:3px}}
ul{{margin:14px 0 14px 22px;color:var(--ink-2)}}
ul li{{margin:6px 0;font-size:15px}}
.cta-box{{background:linear-gradient(180deg,#fffdf7,#fbf3df);border:1px solid rgba(201,164,92,.5);border-radius:14px;padding:18px 20px;margin:28px 0;text-align:center}}
.cta-box h3{{font-size:18px;font-weight:700;margin-bottom:8px}}
.cta-box p{{font-size:13.5px;margin-bottom:12px}}
.cta-btn{{display:inline-block;padding:12px 24px;background:linear-gradient(180deg,#d4b87a,#8a6e30);color:#fff;text-decoration:none;border-radius:9999px;font-size:14px;font-weight:600}}
.related{{margin:32px 0 18px}}
.related h2{{margin-bottom:12px}}
.related a{{display:block;padding:12px 14px;background:#fff;border:1px solid var(--border);border-radius:12px;margin-bottom:8px;text-decoration:none;color:var(--ink);font-size:13.5px;font-weight:600}}
.related a span{{display:block;font-size:10.5px;color:var(--gold-deep);font-weight:700;letter-spacing:.1em;text-transform:uppercase;margin-bottom:3px}}
footer{{padding:24px;text-align:center;font-size:11.5px;color:var(--muted);border-top:1px solid var(--border)}}
footer a{{margin:0 8px;color:var(--gold-deep)}}
.prevnext{{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:32px 0 18px}}
.prevnext a{{display:block;padding:14px;background:#fff;border:1px solid var(--border);border-radius:12px;text-decoration:none;color:var(--ink);font-size:13.5px}}
.prevnext .lab{{font-size:10.5px;color:var(--gold-deep);letter-spacing:.1em;font-weight:700;margin-bottom:3px}}
@media (prefers-color-scheme:dark){{
  :root{{--bg:#15131a;--ink:#f0eadc;--ink-2:#cdc8b8;--muted:#8e8a7d;--border:#3a3530}}
  .related a,.prevnext a{{background:#1f1c20;border-color:#3a3530;color:var(--ink)}}
  .cta-box{{background:linear-gradient(180deg,#3a2f1f,#1f1c20)}}
  header{{background:rgba(21,19,26,.92)}}
}}
</style>

<script type="application/ld+json">
{ld_json}
</script>
</head>
<body>

<amp-auto-ads type="adsense" data-ad-client="ca-pub-8223268344248663"></amp-auto-ads>

<header>
  <a class="logo" href="/">BrillianceLab</a>
  <a class="full-link" href="{canonical}">完整網頁版 →</a>
</header>

<main>
  <div class="label">{label}</div>
  <h1>{title}<span class="accent">{accent}</span></h1>
  <p class="lead">{lead}</p>
  <div class="meta">{meta}</div>

{sections_html}

  <div class="cta-box">
    <h3>動手算分數</h3>
    <p>{cta_text}</p>
    <a class="cta-btn" href="{domain}/">🛠 開始計算 →</a>
  </div>

  <section class="related">
    <h2>繼續閱讀</h2>
{related_html}
  </section>

  <div class="prevnext">
    <a href="{prev_url}"><div class="lab">← 上一篇</div>{prev_title}</a>
    <a href="{next_url}"><div class="lab">下一篇 →</div>{next_title}</a>
  </div>

</main>

<footer>
  <a href="{domain}/">主頁工具</a> ·
  <a href="{domain}/blog/">部落格</a> ·
  <a href="{domain}/search">搜尋</a> ·
  <a href="{domain}/blog/topics">主題索引</a>
  <div style="margin-top:8px">© 2026 BrillianceLab · 鑽石實驗室</div>
</footer>

</body>
</html>
'''


def build_one(p):
    canonical = f"{DOMAIN}/blog/{p['slug']}"
    sections_html = '\n\n'.join(
        f'  <h2>{title}</h2>\n  <p>{body}</p>'
        for title, body in p['sections']
    )
    related_html = '\n'.join(
        f'    <a href="{DOMAIN}/blog/{slug}"><span>相關 {i:02d}</span>{title}</a>'
        for i, (slug, title) in enumerate(p['related'], 1)
    )
    today = datetime.date.today().isoformat()
    ld = {
        '@context': 'https://schema.org',
        '@type': 'Article',
        'headline': p['title'],
        'datePublished': '2026-04-30',
        'dateModified':  today,
        'wordCount':     p['word_count'],
        'isAccessibleForFree': True,
        'description':   p['description'],
        'author':    {'@type': 'Person',       'name': 'BrillianceLab Editorial', 'url': DOMAIN + '/'},
        'publisher': {'@type': 'Organization', 'name': 'BrillianceLab',
                      'logo': {'@type': 'ImageObject', 'url': DOMAIN + '/icon.svg'}},
        'image': DOMAIN + '/icon.svg',
        'mainEntityOfPage': canonical,
    }
    return TEMPLATE.format(
        title=p['title'], accent=p['accent'], canonical=canonical,
        description=p['description'], label=p['label'], lead=p['lead'], meta=p['meta'],
        sections_html=sections_html, related_html=related_html,
        cta_text=p['cta_text'], domain=DOMAIN,
        prev_url=f'{DOMAIN}/blog/{p["prev"][0]}', prev_title=p['prev'][1],
        next_url=f'{DOMAIN}/blog/{p["next"][0]}', next_title=p['next'][1],
        ld_json=json.dumps(ld, ensure_ascii=False, separators=(',', ':')),
    )


def main():
    out_dir = 'amp/blog'
    os.makedirs(out_dir, exist_ok=True)
    for p in PAGES:
        path = os.path.join(out_dir, f'{p["slug"]}.html')
        with open(path, 'w', encoding='utf-8', newline='') as f:
            f.write(build_one(p))
        print('wrote', path)


if __name__ == '__main__':
    main()
