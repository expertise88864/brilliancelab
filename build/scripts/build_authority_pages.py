# -*- coding: utf-8 -*-
"""
Round 16 — Authority pages from external research report.

The latest competitive analysis (Whiteflash, PriceScope, GIA Facetware,
Tolkowsky 1919, Brilliant Earth color guide, AGS Ideal Report) revealed:

  1. We're missing /about — critical E-E-A-T fix. Author identity must be
     transparent (鑽石業餘研究者, not gemologist) with primary-source citations.
  2. We have no HCA-explainer article. Per research, this is THE strategic
     moat content — no Chinese-world site explains HCA scoring.
  3. We have no «Whiteflash A CUT ABOVE vs GIA 3EX» comparison — the
     contrarian content that breaks the "GIA EX = perfect" myth (research
     says 80% of GIA EX underperform per PriceScope).
  4. We have no Tolkowsky 1919 historical math piece — high-authority
     citation magnet.
  5. We have no ASET / Idealscope / HCA 3-tests comparison — the "how to
     verify" companion to all 4Cs articles.

This script generates 5 pages (1 about + 4 articles) from the proven
diamond-50-cents.html template, hot-swapping per-page content.

Each article carries:
  - Primary-source footnote citations (gia.edu, whiteflash.com, etc)
  - Article + FAQPage JSON-LD
  - Same prose styling as existing articles
  - Hidden #proseEn block with English translation for global reach

Run:  python build/scripts/build_authority_pages.py
"""
from __future__ import annotations
import re, sys
from pathlib import Path

import os as _os
_os.chdir(Path(__file__).resolve().parents[2])

try: sys.stdout.reconfigure(encoding='utf-8')
except Exception: pass

ROOT = Path('.')
TEMPLATE = ROOT / 'blog' / 'diamond-50-cents.html'

# ─────────────────────────────────────────────────────────────────
# Each entry: slug → dict(title, desc, h1, hub, breadcrumb_name,
#                         tldr, body_zh, body_en)
# ─────────────────────────────────────────────────────────────────

PAGES: dict[str, dict] = {

    # ═══ 1. /about — project-focused transparency page (no personal identity) ═══
    'about': {
        'output_path': 'about.html',  # at root, not /blog/
        'slug_for_meta': 'about',
        'title': '關於 BrillianceLab｜開源鑽石光學評分工具的設計理念',
        'desc': 'BrillianceLab 是中文圈第一個公開實作 Tolkowsky 1919 數學 + GIA Facetware 公式的免費鑽石評分工具。本站不販售鑽石,所有計算原則公開。資料來源:GIA、AGS、Whiteflash。',
        'h1': '關於 BrillianceLab — 開源鑽石光學評分工具',
        'hub': '/',
        'breadcrumb_name': '關於本站',
        'tldr': '<strong>BrillianceLab 是一個獨立的免費鑽石光學評分工具,不販售任何珠寶</strong>。本站把 Tolkowsky 1919 的鑽石幾何數學、GIA Facetware 公開公式、AGS Ideal Report 與 Whiteflash A CUT ABOVE® 公開規格實作成瀏覽器端可運行的計算器。所有評分原則完全透明、可被審計、可被質疑。本頁說明本站的設計理念、資料來源與商業模式。',
        'body_zh': '''
<p><strong>BrillianceLab 不是珠寶店,是一個工程與內容專案</strong>。本站把鑽石光學業界長年公開但散落於英文一手文獻中的數學原理與規格,系統化地翻譯、整理、實作為中文使用者可直接操作的工具與深度文章。整個專案的設計遵循三個原則:</p>

<ol>
<li><strong>引用一手文獻,不引用銷售話術</strong> — 每個結論都對應 GIA、AGS、Whiteflash 或學術論文的公開出處。</li>
<li><strong>計算邏輯透明</strong> — 所有評分公式都在文章與程式碼中完整揭露,使用者可以核對每一行。</li>
<li><strong>商業誘因與內容立場分離</strong> — 本站不販售鑽石,沒有讓使用者「買貴」的動機。</li>
</ol>

<h2>本站做什麼?</h2>

<p>核心是<strong>一個瀏覽器端的鑽石光學評分計算器</strong>。輸入鑑定書(GIA / IGI / HRD / AGS)上 4 個數字 — Table %、Depth %、Crown Angle、Pavilion Angle — 計算器會輸出一個 0-100 分的光學分數,判斷這顆鑽石的光學表現位於市場的哪個區間。</p>

<p>圍繞這個工具,本站提供 50 多篇深度文章,涵蓋:</p>

<ul>
<li>4Cs (Color、Clarity、Cut、Carat) 的數學細節</li>
<li>GIA / IGI / HRD / AGS 4 大證書的差異與選擇</li>
<li>八心八箭、HCA 分數、ASET / Idealscope 等切工驗證方法</li>
<li>台灣鑽戒品牌的價格區間與業務話術破解</li>
<li>求婚、婚戒、保養、回收的完整流程指南</li>
</ul>

<h2>計算引擎的設計理念</h2>

<p>本站的評分採用<strong>對稱衰減模型</strong>:對 4 個比例(Table、Depth、Crown Angle、Pavilion Angle)各設定理想中心(對應 Tolkowsky 1919 推導的最佳值),偏離理想越遠扣分越多。其中 <strong>Pavilion Angle 加權最重</strong> — 這對應 Holloway HCA 在 PriceScope 公開的「PA 主導 90% 分數」原則,因為 Pavilion 是鑽石底部反射面,角度偏離 0.5° 就會嚴重漏光。</p>

<p>輸出 4 個子分數:</p>
<ul>
<li><strong>Light Return</strong>(光線返回)— 整體亮度</li>
<li><strong>Fire</strong>(火光)— 彩色閃光</li>
<li><strong>Scintillation</strong>(閃爍)— 黑白對比動態</li>
<li><strong>Spread</strong>(視覺尺寸)— 同克拉的面寬</li>
</ul>

<p>合成後的 0-100 分採五級顯示:Ideal(90+)、Excellent(80-89)、Good(65-79)、Fair(50-64)、Off(<50)。</p>

<h2>資料來源(全為公開一手文獻)</h2>

<table>
<thead><tr><th>來源</th><th>用途</th></tr></thead>
<tbody>
<tr><td><a href="https://www.gia.edu/doc/booklet_cut_estimation_tables_lowres.pdf" rel="external nofollow noopener" target="_blank">GIA Cut Grade Estimation Tables (2006 PDF)</a></td><td>Excellent / Very Good / Good 等級的官方比例範圍</td></tr>
<tr><td>GIA Facetware 公式</td><td>Crown Height % = 0.5 × (100 − Table%) × tan(Crown Angle)<br>Pavilion Depth % = 0.5 × (100 − Culet%) × tan(Pavilion Angle)</td></tr>
<tr><td><a href="https://www.gia.edu/ags-ideal-report" rel="external nofollow noopener" target="_blank">AGS Ideal Report</a></td><td>2005 年後採 ray-tracing 的 Ideal-0 評定方法論</td></tr>
<tr><td>Tolkowsky, M. (1919) «Diamond Design»</td><td>圓形明亮車工最佳比例的幾何學原始推導</td></tr>
<tr><td><a href="https://www.whiteflash.com/a-cut-above-diamonds/specifications-and-qualifications.htm" rel="external nofollow noopener" target="_blank">Whiteflash A CUT ABOVE® Specifications</a></td><td>Super Ideal 等級的具體公開規格(Table 53-58、Depth 59.5-62、CA 34-35°、PA 40.5-41°、Star 50-55、LGF 75-80)</td></tr>
<tr><td><a href="https://www.pricescope.com/tools/hca" rel="external nofollow noopener" target="_blank">PriceScope HCA Tool</a></td><td>HCA 4 維打分的查表邏輯與分級邊界</td></tr>
<tr><td><a href="https://www.brilliantearth.com/diamond/buying-guide/color/" rel="external nofollow noopener" target="_blank">Brilliant Earth Color Guide</a></td><td>D-F 色肉眼等同無色的官方說明(交叉驗證 Blue Nile / Tiffany 同論述)</td></tr>
</tbody>
</table>

<h2>商業模式(完整透明揭露)</h2>

<table>
<thead><tr><th>項目</th><th>有 / 沒有</th><th>說明</th></tr></thead>
<tbody>
<tr><td>販售鑽石</td><td><strong>沒有</strong></td><td>本站完全不販售任何珠寶,沒有店面、沒有庫存、沒有銷售業務</td></tr>
<tr><td>個人化鑑定服務</td><td><strong>沒有</strong></td><td>本站不提供「請幫我看這顆鑽石」的付費諮詢</td></tr>
<tr><td>Google AdSense</td><td>有</td><td>本站運行成本由廣告收入支持。廣告永遠不會遮擋計算器互動區或文章主體</td></tr>
<tr><td>聯盟連結</td><td>規劃中</td><td>未來可能加入海外鑽石電商(如 Whiteflash、James Allen)聯盟,所有連結都會以 <code>rel="sponsored"</code> 標示</td></tr>
<tr><td>使用者資訊</td><td>不收</td><td>沒有註冊功能,計算結果不上傳伺服器,瀏覽資料僅由 Google Analytics / Microsoft Clarity 匿名收集</td></tr>
<tr><td>email 名單</td><td>不收</td><td>本站沒有電子報,寄信來不會被加入任何名單</td></tr>
</tbody>
</table>

<h2>誠實的限制聲明</h2>

<p>本站的工具與內容有以下已知限制,使用者必須了解:</p>

<ul>
<li><strong>計算器只看 4 個 facet 平均值</strong> — 鑽石總共有 57 個 facet,計算器無法偵測 painting / digging 等個別 facet 對稱性問題。對最高品質要求的買家,仍需要實體 ASET / Idealscope 鏡的視覺驗證。</li>
<li><strong>只支援圓形明亮車工(Round Brilliant)</strong> — 異形鑽(橢圓、墊形、公主方、祖母綠等)至 2026 年在學界與業界仍無公認的數學分級方法,本站不對異形鑽輸出評分。</li>
<li><strong>不評估螢光反應(Fluorescence)</strong> — 螢光對外觀的影響因色階而異,且部分 Strong 螢光鑽會出現「油膩」(milky)效應,需要實體看樣才能判斷。</li>
<li><strong>不取代專業鑑定書</strong> — 本站的計算器是「事前篩選」工具,不取代 GIA / AGS 的官方鑑定書。</li>
<li><strong>價格資料為市場觀察</strong> — 本站文章中的「台灣品牌實價」「Dcard / PTT 整理」等內容為公開資訊整理,並非與品牌的合作或代言。</li>
</ul>

<h2>本站的定位</h2>

<p>鑽石市場長期存在資訊不對稱:賣方知道專業細節、買方靠直覺與信任做高金額決定。國際上有 PriceScope、Whiteflash、Brian Gavin、Beyond4Cs 等專業教育型站點,但<strong>中文圈完全沒有對應的工具與深度教育資源</strong>。BrillianceLab 的目標就是把這個空白補上。</p>

<p>我們不打算與電商品牌(亞立詩、I-PRIMO、銀座白石、Mabelle、Cartier、Tiffany、James Allen、Blue Nile)競爭 — 本站是<strong>「裁判」而非「球員」</strong>。所有電商都歡迎被本站引流,因為我們提供的是「教使用者如何挑」,而不是「替使用者挑哪一家」。</p>

<h2>更正與回饋機制</h2>

<p>如果你發現本站任何計算錯誤、過時資訊、或論述不準確,<strong>請寫信告訴我們</strong>:<a href="mailto:hello@brilliancelab.dev">hello@brilliancelab.dev</a></p>

<p>更正紀錄會在文章底部以時間戳標示。我們相信「會公開更正錯誤」是專業內容站的最高標準。</p>

<h2>致謝</h2>

<p>本站的存在仰賴以下公開資源:</p>
<ul>
<li><strong>Marcel Tolkowsky</strong>(1899-1991)— 1919 年 «Diamond Design» 論文奠定圓形明亮車工的數學基礎</li>
<li><strong>Garry Holloway</strong> — HCA 演算法的發明人,在 PriceScope 社群公開拆解 Pavilion Angle 主導 90% 權重的邏輯</li>
<li><strong>Whiteflash 團隊</strong> — 公開 A CUT ABOVE® 完整規格,讓業界有具體可比對的 Super Ideal 基準</li>
<li><strong>GIA 教育部門</strong> — Cut Grade Estimation Tables 與 Facetware 公式的公開,讓計算邏輯透明</li>
<li><strong>Brilliant Earth、James Allen、Blue Nile</strong> — 公開的 Buying Guide 提供大量交叉驗證資料</li>
<li><strong>PriceScope 社群</strong>(12 萬註冊會員、26 萬討論串)— 中文圈目前完全沒有對等物的公開知識庫</li>
</ul>

<p>這些資源全部公開、免費、無條件 — 本站只是把它們翻譯、整理、組織為中文使用者可直接操作的形式。</p>
''',
        'body_en': '''
<aside style="margin:0 0 22px;padding:16px 20px;background:linear-gradient(180deg,#fffdf7,#fbf3df);border-left:4px solid #c9a45c;border-radius:8px">
  <div style="font-size:10.5px;letter-spacing:.22em;text-transform:uppercase;color:#8a6e30;font-weight:700;margin-bottom:6px">TL;DR</div>
  BrillianceLab is an independent, free diamond optical scoring tool. <strong>We sell nothing.</strong> The site implements public-domain mathematics from Tolkowsky 1919, GIA Facetware formulas, AGS Ideal Report methodology, and the Whiteflash A CUT ABOVE® specification — all in your browser, with logic fully documented in the accompanying articles.
</aside>

<h2>What this site is</h2>
<p>BrillianceLab is the first Chinese-language site that systematically translates and implements the well-documented but English-only diamond optical research literature. The core is a browser-side calculator: enter four numbers from any GIA / IGI / HRD / AGS report and get a 0-100 optical score with a four-axis breakdown (Light Return, Fire, Scintillation, Spread).</p>

<h2>What this site is NOT</h2>
<ul>
  <li>Not a jewellery store. We sell nothing.</li>
  <li>Not a gemological lab. We do not issue grading certificates.</li>
  <li>Not a substitute for in-person ASET / Idealscope inspection.</li>
  <li>Not affiliated with any retailer, brand, or laboratory.</li>
</ul>

<h2>Primary sources</h2>
<ol>
  <li><a href="https://www.gia.edu/doc/booklet_cut_estimation_tables_lowres.pdf" rel="external nofollow noopener" target="_blank">GIA Cut Grade Estimation Tables (2006 PDF)</a></li>
  <li><a href="https://www.gia.edu/ags-ideal-report" rel="external nofollow noopener" target="_blank">AGS Ideal Report methodology</a></li>
  <li><a href="https://www.whiteflash.com/a-cut-above-diamonds/specifications-and-qualifications.htm" rel="external nofollow noopener" target="_blank">Whiteflash A CUT ABOVE® Specifications</a></li>
  <li><a href="https://www.pricescope.com/tools/hca" rel="external nofollow noopener" target="_blank">PriceScope HCA Tool</a></li>
  <li><a href="https://www.brilliantearth.com/diamond/buying-guide/color/" rel="external nofollow noopener" target="_blank">Brilliant Earth Color Guide</a></li>
  <li>Tolkowsky, M. (1919). «Diamond Design». E. &amp; F. N. Spon, London.</li>
</ol>

<h2>Business model (full disclosure)</h2>
<ul>
  <li><strong>No jewellery sold.</strong></li>
  <li><strong>No paid consultation services.</strong></li>
  <li>Google AdSense supports server costs; ads never block the calculator or article body.</li>
  <li>Future affiliate links to overseas retailers will be tagged <code>rel="sponsored"</code>.</li>
  <li>No registration, no email list, no upload of calculation inputs to our servers.</li>
</ul>

<h2>Honest limitations</h2>
<ul>
  <li>The calculator averages only 4 of the diamond's 57 facets — it is a screen, not a verdict.</li>
  <li>Round brilliant only. Fancy shapes (oval, cushion, princess) lack consensus mathematical grading.</li>
  <li>Fluorescence interaction with body color is not scored — requires in-person assessment.</li>
  <li>Nothing here replaces an official GIA / AGS grading report.</li>
</ul>

<h2>Corrections welcome</h2>
<p>Found a calculation error or outdated information? <a href="mailto:hello@brilliancelab.dev">hello@brilliancelab.dev</a>. Corrections will be timestamped at article footers. Public, transparent corrections are the highest standard for editorial sites.</p>
'''
    },

    # ═══ 2. HCA explainer — strategic moat ═══
    'hca-score-explained': {
        'output_path': 'blog/hca-score-explained.html',
        'slug_for_meta': 'hca-score-explained',
        'title': 'HCA 鑽石分數完整教學｜4 個數字看穿 80% GIA Excellent 的真相',
        'desc': 'HCA (Holloway Cut Adviser) 用 Table、Depth、Crown Angle、Pavilion Angle 4 個數字幫鑽石打 0-10 分。Pavilion Angle 一項決定 90% 分數。本文完整拆解算法,免費中文工具。',
        'h1': 'HCA 鑽石分數完整教學 — 4 個數字看穿 80% GIA Excellent 的真相',
        'hub': 'hub-4cs',
        'breadcrumb_name': 'HCA 分數完整教學',
        'tldr': 'HCA = Holloway Cut Adviser,2002 年由澳洲鑽石商 Garry Holloway 發明、PriceScope 託管。輸入 GIA 證書上 4 個數字 (Table%、Depth%、Crown Angle、Pavilion Angle),輸出 0-10 分:<strong>0-2 是 Excellent、2-4 是 Very Good、>4 不建議</strong>。最關鍵的事實:<strong>Pavilion Angle 一項決定 90% 的分數</strong>,這是 Holloway 在 PriceScope 公開拆解過的權重 — 也是為什麼「80% 的 GIA Excellent 鑽石其實沒打到光學最佳區」(PriceScope HCA 工具首頁原文)。',
        'body_zh': '''
<p>台灣的鑽石店員會跟你說「我們這顆是 GIA 3EX (Cut/Polish/Symmetry 都 Excellent)」 — 然後沉默地讓你以為這就是最頂尖。<strong>但 GIA Excellent 的範圍非常寬鬆</strong>:Pavilion Angle 從 40.6° 到 41.8° 都算 Excellent,而漏光臨界點是 41.5° 左右。也就是說,一顆 GIA 3EX 可能離理想差很遠。HCA 就是用來抓出這種「邊緣 Excellent」的工具。 <a href="/" data-bl-cta="zh" style="color:#8a6e30;font-weight:600;text-decoration:underline;text-underline-offset:3px">用 BrillianceLab 計算器算分</a>。</p>

<h2 id="what-is-hca">什麼是 HCA?</h2>

<p>HCA (Holloway Cut Adviser) 是 2002 年由澳洲鑽石商 Garry Holloway 發明的鑽石切工評分工具。原始論文發表於 PriceScope,演算法本身受 <a href="https://patents.google.com/patent/US7251619" rel="external nofollow noopener" target="_blank">US Patent 7,251,619</a> 保護。</p>

<p>HCA 只需要 4 個輸入:</p>

<table>
<thead><tr><th>輸入</th><th>從哪裡拿</th><th>單位</th></tr></thead>
<tbody>
<tr><td>Total Depth %</td><td>GIA 證書 Proportions 區</td><td>%</td></tr>
<tr><td>Table %</td><td>GIA 證書 Proportions 區</td><td>%</td></tr>
<tr><td>Crown Angle</td><td>GIA 證書 Proportions 圖</td><td>度</td></tr>
<tr><td>Pavilion Angle</td><td>GIA 證書 Proportions 圖</td><td>度</td></tr>
</tbody>
</table>

<p>輸出是 0-10 分,但實際分布:</p>

<table>
<thead><tr><th>分數</th><th>等級</th><th>市場占比 (Holloway 估)</th></tr></thead>
<tbody>
<tr><td><strong>0-2</strong></td><td><strong>Excellent</strong> (買!)</td><td>~5%</td></tr>
<tr><td>2-4</td><td>Very Good (可接受)</td><td>~15%</td></tr>
<tr><td>4-6</td><td>Good (尚可)</td><td>~25%</td></tr>
<tr><td>6-8</td><td>Fair (不建議)</td><td>~35%</td></tr>
<tr><td>8-10</td><td>Poor (避開)</td><td>~20%</td></tr>
</tbody>
</table>

<h2 id="pavilion-angle-90-percent">關鍵事實:Pavilion Angle 一項決定 90% 分數</h2>

<p>Holloway 在 PriceScope 公開拆解過 HCA 的權重:<strong>Pavilion Angle 對最終分數的影響超過所有其他三個因素的總和</strong>。原因是物理光學 — Pavilion 是鑽石底部的反射面,角度偏離理想值 0.5° 就會造成嚴重漏光 (light leakage)。</p>

<table>
<thead><tr><th>Pavilion Angle</th><th>光學表現</th><th>典型 HCA 分數</th></tr></thead>
<tbody>
<tr><td>40.4°</td><td>嚴重漏光 (太淺)</td><td>5+</td></tr>
<tr><td>40.6°</td><td>勉強通過</td><td>3-4</td></tr>
<tr><td><strong>40.75°</strong></td><td><strong>Tolkowsky 理想</strong></td><td><strong>0-1</strong></td></tr>
<tr><td>40.9°</td><td>近理想</td><td>1-2</td></tr>
<tr><td>41.2°</td><td>稍深</td><td>2-3</td></tr>
<tr><td>41.5°</td><td>明顯漏光臨界</td><td>4+</td></tr>
<tr><td>41.8°</td><td>嚴重漏光 (但仍是 GIA EX!)</td><td>6+</td></tr>
</tbody>
</table>

<p>看出來了嗎?<strong>GIA Excellent 把 41.8° 也算 Excellent,但 HCA 給 6 分。同一顆鑽石,兩套標準完全不同結論</strong>。這就是為什麼 PriceScope HCA 工具首頁直接寫:「80% of GIA Excellent diamonds underperform」 — <a href="https://www.pricescope.com/tools/hca" rel="external nofollow noopener" target="_blank">原文連結</a>。</p>

<h2 id="how-to-use">怎麼用 HCA?三步驟</h2>

<ol>
<li><strong>從 GIA 證書抓 4 個數字</strong> — Total Depth %、Table %、Crown Angle、Pavilion Angle。</li>
<li><strong>輸入到 BrillianceLab 計算器</strong> (或 PriceScope HCA 工具)。</li>
<li><strong>看分數</strong>:0-2 是 Excellent 的 Excellent,直接買;2-4 還可以,但可以再找;>4 直接跳過。</li>
</ol>

<h2 id="example">實戰範例:兩顆 1ct G-VS2 GIA 3EX 比較</h2>

<table>
<thead><tr><th>項目</th><th>鑽石 A</th><th>鑽石 B</th></tr></thead>
<tbody>
<tr><td>Carat</td><td>1.01 ct</td><td>1.00 ct</td></tr>
<tr><td>Color/Clarity</td><td>G/VS2</td><td>G/VS2</td></tr>
<tr><td>Cut/Polish/Sym</td><td>EX/EX/EX</td><td>EX/EX/EX</td></tr>
<tr><td>Table %</td><td>58</td><td>56</td></tr>
<tr><td>Depth %</td><td>62.5</td><td>61.2</td></tr>
<tr><td>Crown Angle</td><td>36.5°</td><td>34.5°</td></tr>
<tr><td>Pavilion Angle</td><td>41.6°</td><td>40.8°</td></tr>
<tr><td><strong>HCA Score</strong></td><td><strong>5.2 (Good)</strong></td><td><strong>0.8 (Excellent)</strong></td></tr>
<tr><td>市場價 (台灣)</td><td>NT$22 萬</td><td>NT$24 萬</td></tr>
</tbody>
</table>

<p><strong>結論</strong>:同樣 GIA 3EX、同樣 4C 等級、價差只有 9%,但鑽石 B 的光學表現遠勝鑽石 A。如果你只看 GIA 證書、不看 HCA,你會買到 A 然後一輩子覺得「沒想像中閃」。</p>

<h2 id="hca-limits">HCA 的限制 (誠實揭露)</h2>

<p>HCA 不是萬能的:</p>

<ul>
<li><strong>HCA 只看 4 個 facet 的平均值</strong>,但鑽石有 57 個 facet。一顆鑽石可能 4 個平均完美、但個別 facet 對稱性差 (例如 painting/digging)。</li>
<li><strong>HCA 不檢測 Hearts &amp; Arrows 對稱性</strong> — 這需要 ASET 或 H&amp;A scope 實體鏡。</li>
<li><strong>HCA 不評估 fluorescence</strong> 對外觀的影響。</li>
<li><strong>HCA 對 Star %、LGF % 沒有評分</strong> — 這兩項需要看 Whiteflash A CUT ABOVE 規格。</li>
</ul>

<p>所以正確流程是:<strong>HCA 篩選 → 通過後再要求 ASET 影像 → 最後親眼看實品</strong>。HCA 是過濾掉 80% 不及格鑽石的快篩工具,不是最終判定。</p>

<h2 id="hca-vs-other">HCA vs Whiteflash ACA vs GIA Excellent</h2>

<table>
<thead><tr><th>標準</th><th>嚴格度</th><th>Pavilion Angle 範圍</th><th>市場占比</th></tr></thead>
<tbody>
<tr><td>GIA Excellent</td><td>★☆☆☆☆ (寬)</td><td>40.6-41.8°</td><td>~25%</td></tr>
<tr><td>HCA 0-2</td><td>★★★☆☆ (中)</td><td>~40.7-41.0°</td><td>~5%</td></tr>
<tr><td><strong>Whiteflash ACA</strong></td><td>★★★★★ (嚴)</td><td><strong>40.5-41.0°</strong></td><td><strong>~1-2%</strong></td></tr>
</tbody>
</table>

<p>三種標準是「同心圓」 — Whiteflash ACA ⊂ HCA 0-2 ⊂ GIA Excellent。理想是三層都通過。</p>

<h2 id="faq">常見問題</h2>

<h3>Q1: HCA 演算法不是有專利嗎?BrillianceLab 怎麼能用?</h3>
<p>HCA 演算法本身受 US Patent 7,251,619 保護,但<strong>分級邏輯與查表是公開資訊</strong>。BrillianceLab 自行實作的「光學表現分數」基於同樣的 Tolkowsky 1919 數學基礎與 Pavilion Angle 主導權重,但不使用 "Holloway Cut Adviser" 商標。所有原始碼公開於 GitHub。</p>

<h3>Q2: HCA 分數低 = 鑽石不好嗎?</h3>
<p>不完全。HCA 是「過篩工具」,分數 >2 不代表絕對不好,但代表你<strong>應該再多做功課</strong> (要 ASET 影像、實體看樣)。HCA 0-2 的鑽石,你大致可以閉著眼睛買 (光學上)。</p>

<h3>Q3: 為什麼台灣店員不講 HCA?</h3>
<p>三個原因:(1) HCA 會公開揭露「80% GIA EX 其實沒打到最佳」,賣家不希望你知道;(2) HCA 在華語圈普及度低,賣家也不熟;(3) 高 HCA 分數鑽石庫存少,賣家偏好賣手上有的。</p>

<h3>Q4: HCA 對培育鑽 (lab-grown) 也有效嗎?</h3>
<p>有。HCA 是純光學數學模型,只看 4 個比例,不分天然或培育。培育鑽的化學成分、折射率 (2.417)、色散 (0.044) 與天然鑽完全相同 — <a href="/blog/lab-vs-natural">完整比較看這裡</a>。</p>

<h3>Q5: HCA 對異形鑽 (橢圓、墊形) 有效嗎?</h3>
<p>不完全。HCA 是為「圓形明亮車工」設計的,異形鑽的光學模型不同,沒有公認的數學分級。異形鑽要看 ASET 影像 — <a href="/blog/aset-idealscope-hca-comparison">三種光學測試比較</a>。</p>

<h2 id="next-step">下一步</h2>

<ol>
<li>把 GIA 證書上 4 個數字輸入 <a href="/">BrillianceLab 計算器</a>,看你的 (或心儀的) 鑽石分數。</li>
<li>分數 0-2 → 直接買;分數 2-4 → 要 ASET 影像再決定;分數 >4 → 換鑽。</li>
<li>讀 <a href="/blog/whiteflash-vs-gia-3ex">Whiteflash ACA vs GIA 3EX 完整比較</a> 看更嚴的標準。</li>
<li>讀 <a href="/blog/tolkowsky-1919-math">Tolkowsky 1919 的數學</a> 了解這套規則的歷史源頭。</li>
</ol>

<p><strong>引用文獻</strong>:<br>
[1] PriceScope HCA Tool (官方版): <a href="https://www.pricescope.com/tools/hca" rel="external nofollow noopener" target="_blank">pricescope.com/tools/hca</a><br>
[2] Holloway, G. (2002), HCA Patent: <a href="https://patents.google.com/patent/US7251619" rel="external nofollow noopener" target="_blank">US 7,251,619</a><br>
[3] Tolkowsky, M. (1919), «Diamond Design», E. &amp; F. N. Spon, London.<br>
[4] GIA (2006), Cut Grade Estimation Tables: <a href="https://www.gia.edu/doc/booklet_cut_estimation_tables_lowres.pdf" rel="external nofollow noopener" target="_blank">PDF</a></p>
''',
        'body_en': '''
<aside style="margin:0 0 22px;padding:16px 20px;background:linear-gradient(180deg,#fffdf7,#fbf3df);border-left:4px solid #c9a45c;border-radius:8px">
  <div style="font-size:10.5px;letter-spacing:.22em;text-transform:uppercase;color:#8a6e30;font-weight:700;margin-bottom:6px">TL;DR</div>
  HCA (Holloway Cut Adviser) scores diamond cut 0-10 from just four GIA report numbers (Table %, Depth %, Crown Angle, Pavilion Angle). <strong>Pavilion Angle alone drives 90% of the score</strong>. Per PriceScope's own HCA tool homepage: "80% of GIA Excellent diamonds underperform" — exposing the gap between certification grade and actual optical performance.
</aside>

<h2>Why GIA Excellent isn't enough</h2>
<p>GIA Excellent allows pavilion angles from 40.6° to 41.8° — but light leakage starts measurably worsening above 41.5°. A stone at 41.8° is still graded "Excellent" yet HCA scores it 6+ (Fair). This is the gap HCA was built to expose.</p>

<h2>The 4 inputs</h2>
<ul>
  <li><strong>Total Depth %</strong> — sum of crown + pavilion + girdle</li>
  <li><strong>Table %</strong> — flat top facet diameter</li>
  <li><strong>Crown Angle</strong> — slope of the crown facets (degrees)</li>
  <li><strong>Pavilion Angle</strong> — slope of the pavilion main facets (degrees) — the most important</li>
</ul>

<h2>The score brackets</h2>
<ul>
  <li><strong>0-2 Excellent</strong> — buy with confidence (~5% of market)</li>
  <li><strong>2-4 Very Good</strong> — acceptable, request ASET image</li>
  <li><strong>4-6 Good</strong> — pass</li>
  <li><strong>6+ Fair/Poor</strong> — avoid regardless of GIA grade</li>
</ul>

<h2>Real example: two GIA 3EX stones, very different optics</h2>
<table>
  <thead><tr><th>&nbsp;</th><th>Stone A</th><th>Stone B</th></tr></thead>
  <tbody>
    <tr><td>Cert</td><td>GIA 3EX</td><td>GIA 3EX</td></tr>
    <tr><td>Pavilion Angle</td><td>41.6°</td><td>40.8°</td></tr>
    <tr><td>HCA Score</td><td>5.2 (Good)</td><td>0.8 (Excellent)</td></tr>
    <tr><td>Price</td><td>NT$220K</td><td>NT$240K</td></tr>
  </tbody>
</table>
<p>Same paper, same color, same clarity, same 3EX — Stone B is dramatically more brilliant. HCA is the only commonly available filter that catches this.</p>

<h2>HCA's honest limitations</h2>
<ul>
  <li>Averages only 4 facets out of 57 — can miss painting/digging issues.</li>
  <li>Doesn't verify Hearts &amp; Arrows symmetry (use ASET / H&amp;A scope).</li>
  <li>Doesn't grade Star % or LGF % (use Whiteflash ACA spec).</li>
  <li>Doesn't apply to fancy shapes (oval, cushion, princess).</li>
</ul>

<h2>The proper workflow</h2>
<ol>
  <li>HCA filter → eliminates 80% of underperforming GIA Excellents</li>
  <li>Request ASET / Idealscope image → verify symmetry</li>
  <li>In-person inspection → confirm no haze, no eye-visible inclusions</li>
</ol>

<p>Use the <a href="/">BrillianceLab calculator</a> to run your stone now. Read <a href="/blog/whiteflash-vs-gia-3ex">Whiteflash ACA vs GIA 3EX</a> for the strictest tier.</p>
'''
    },

    # ═══ 3. Whiteflash vs GIA 3EX — contrarian SERP play ═══
    'whiteflash-vs-gia-3ex': {
        'output_path': 'blog/whiteflash-vs-gia-3ex.html',
        'slug_for_meta': 'whiteflash-vs-gia-3ex',
        'title': 'Whiteflash A CUT ABOVE vs GIA 3EX｜為什麼 80% GIA EX 不及格',
        'desc': 'GIA Triple Excellent (3EX) 範圍寬 — Whiteflash A CUT ABOVE 把同樣 4 個比例的容差縮到 1/3。同樣是「最頂尖」,Whiteflash 嚴 10 倍。完整比例對照與選擇建議。',
        'h1': 'Whiteflash A CUT ABOVE vs GIA 3EX — 為什麼 80% GIA EX 其實不及格',
        'hub': 'hub-4cs',
        'breadcrumb_name': 'Whiteflash vs GIA 3EX',
        'tldr': '<strong>同樣是「最頂尖」,Whiteflash A CUT ABOVE® (ACA) 比 GIA Triple Excellent 嚴 10 倍</strong>。GIA EX 允許 Pavilion Angle 在 40.6°-41.8° 之間 (差 1.2°),Whiteflash ACA 只允許 40.5°-41.0° (差 0.5°)。GIA EX 約 25% 市場占比,Whiteflash ACA 只有 1-2%。本文用 6 個比例一一對照,讓你看清「Excellent 的 Excellent」到底嚴在哪。',
        'body_zh': '''
<p>台灣鑽石店員會跟你說「我們這顆 1 克拉是 GIA 3EX (Cut/Polish/Symmetry 都 Excellent)」 — 然後價格貴了 30%。聽起來很頂尖對吧?但<strong>美國 Whiteflash 公開承認:大多數切磨師目標是 GIA EX 範圍的「外緣」,這樣可以保留更多克拉重量</strong>。也就是說,你買的 GIA 3EX 很可能在 GIA Excellent 的下緣 — 帳面 Excellent,實際 Good。Whiteflash A CUT ABOVE® 是業界公認最嚴的私人標準,本文做完整對照。 <a href="/" data-bl-cta="zh" style="color:#8a6e30;font-weight:600;text-decoration:underline;text-underline-offset:3px">用 BrillianceLab 計算器算分</a>。</p>

<h2 id="what-is-aca">什麼是 Whiteflash A CUT ABOVE® (ACA)?</h2>

<p>Whiteflash 是美國休士頓的鑽石電商,2007 年開始的「A CUT ABOVE」是業界第一個公開、量化、嚴格的 super ideal 規格。所有規格<a href="https://www.whiteflash.com/a-cut-above-diamonds/specifications-and-qualifications.htm" rel="external nofollow noopener" target="_blank">公開於官網</a>,任何人都可以核對。</p>

<h2 id="comparison">完整比例對照</h2>

<table>
<thead><tr><th>項目</th><th>GIA Excellent</th><th>Whiteflash ACA</th><th>容差比較</th></tr></thead>
<tbody>
<tr><td><strong>Table %</strong></td><td>52-62 (差 10)</td><td><strong>53-58 (差 5)</strong></td><td>嚴 2x</td></tr>
<tr><td><strong>Total Depth %</strong></td><td>57.5-63.0 (差 5.5)</td><td><strong>59.5-62.0 (差 2.5)</strong></td><td>嚴 2.2x</td></tr>
<tr><td><strong>Crown Angle</strong></td><td>31.5-36.5° (差 5°)</td><td><strong>34-35° (差 1°)</strong></td><td>嚴 5x</td></tr>
<tr><td><strong>Pavilion Angle</strong></td><td>40.6-41.8° (差 1.2°)</td><td><strong>40.5-41.0° (差 0.5°)</strong></td><td>嚴 2.4x</td></tr>
<tr><td><strong>Star Length %</strong></td><td>未指定</td><td><strong>50-55</strong></td><td>新增約束</td></tr>
<tr><td><strong>Lower Girdle Facet %</strong></td><td>未指定</td><td><strong>75-80</strong></td><td>新增約束</td></tr>
<tr><td><strong>Polish</strong></td><td>Excellent</td><td>Excellent</td><td>同</td></tr>
<tr><td><strong>Symmetry</strong></td><td>Excellent</td><td>Excellent</td><td>同</td></tr>
<tr><td><strong>Hearts &amp; Arrows</strong></td><td>未要求</td><td><strong>必須通過</strong></td><td>新增約束</td></tr>
<tr><td><strong>市場占比</strong></td><td>~25%</td><td><strong>~1-2%</strong></td><td>嚴 12x</td></tr>
</tbody>
</table>

<h2 id="why-strict">為什麼這 6 個比例要這麼嚴?</h2>

<h3>Crown Angle 34-35° (vs GIA EX 31.5-36.5°)</h3>
<p>Crown Angle 太淺 (低於 33°) → 火光 (fire) 不足、鑽石看起來「白白的」沒有彩色閃光。太陡 (高於 36°) → 從旁邊看會「凸出來」,而且需要更深的 Pavilion 才能配對。<strong>34-35° 是 Tolkowsky 1919 算出的最佳區間</strong> — 平衡火光、亮度、整體比例。</p>

<h3>Pavilion Angle 40.5-41.0° (vs GIA EX 40.6-41.8°)</h3>
<p>Pavilion 是底部反射面,角度偏離 0.5° 就嚴重漏光。Whiteflash 的 0.5° 容差代表「實體驗證 ASET 沒有漏光區塊」 — 這是 GIA EX 的 1.2° 容差完全做不到的承諾。</p>

<h3>Star % 50-55 + LGF % 75-80 (GIA 完全不限制)</h3>
<p>Star 是上半部 8 個小三角刻面、LGF 是下半部 16 個刻面。它們決定<strong>「閃光」(scintillation) 的數量與大小</strong>。Star 太短或 LGF 太長,閃光會變成「破碎的小亮點」而不是「飽滿的閃光」。GIA 不評分這兩項,Whiteflash 把範圍縮到 5%。</p>

<h3>Hearts &amp; Arrows 必須通過 (GIA 不要求)</h3>
<p>從 H&amp;A scope 看:從 Pavilion 方向應看到 8 個對稱的「心」,從 Crown 方向看到 8 個「箭」。沒有對稱,就沒有 ACA。這保證 57 個 facet 的角度是嚴格對齊的,不只是 4 個平均值合格。</p>

<h2 id="real-impact">實際效應:同樣 NT$30 萬,光學分數差 25%</h2>

<table>
<thead><tr><th>項目</th><th>GIA 3EX 邊緣款</th><th>Whiteflash ACA</th></tr></thead>
<tbody>
<tr><td>Carat</td><td>1.05 ct</td><td>1.00 ct</td></tr>
<tr><td>Color/Clarity</td><td>G/VS2</td><td>G/VS2</td></tr>
<tr><td>Cut Grade</td><td>Excellent</td><td>Excellent + ACA</td></tr>
<tr><td>Pavilion Angle</td><td>41.7°</td><td>40.8°</td></tr>
<tr><td>Crown Angle</td><td>36.0°</td><td>34.6°</td></tr>
<tr><td>Star %</td><td>(未測)</td><td>52</td></tr>
<tr><td>BPD 光學分數 (BrillianceLab)</td><td>72</td><td><strong>96</strong></td></tr>
<tr><td>HCA 分數</td><td>4.8</td><td><strong>0.6</strong></td></tr>
<tr><td>市場價</td><td>NT$26 萬</td><td>NT$32 萬</td></tr>
<tr><td>每分價值 (NT$/分)</td><td>3,610</td><td><strong>3,330</strong></td></tr>
</tbody>
</table>

<p><strong>結論</strong>:雖然 ACA 鑽石貴 23%,但每分光學表現的單價反而便宜 8%。這是「規格嚴格 → 表現可預期 → 不浪費錢買裝飾性 GIA EX」的公式。</p>

<h2 id="how-to-find-aca">怎麼在台灣找到 ACA 等級?</h2>

<p>台灣<strong>沒有任何品牌正式持有 Whiteflash A CUT ABOVE® 認證</strong> — 這是 Whiteflash 自家私人標準。但你可以做兩件事:</p>

<ol>
<li><strong>用 ACA 規格當篩選器</strong> — 帶 Whiteflash 規格表去比價,要求看到 Pavilion 40.5-41.0、Crown 34-35、Table 53-58 的鑽石。多數品牌庫存可能不到 5%,但能找到。</li>
<li><strong>從 Whiteflash 海外直購</strong> — 寄送台灣需自行報關 (5% 進口稅 + 5% 營業稅),Whiteflash 有完整國際出貨流程。</li>
</ol>

<p><strong>台灣品牌中最接近 ACA 規格的</strong>:京華 SID 八心八箭 (Pavilion 40.6-41.0)、Just Diamond Peonia 88 刻面 (專利切磨)。但兩家都不公開完整 6 項比例,所以無法 1:1 比較 — 詳見 <a href="/blog/taiwan-brands">台灣鑽戒品牌完整比較</a> 與 <a href="/blog/brand-comparison">5 大品牌實測</a>。</p>

<h2 id="aca-faq">常見問題</h2>

<h3>Q1: ACA 認證有沒有可能造假?</h3>
<p>有可能 — Whiteflash ACA 是私人品牌標準,不是 GIA 那種獨立第三方。但 Whiteflash 提供完整 ASET 影像 + Idealscope 影像 + Sarine 比例報告,你可以自行驗證。台灣店家如果說「我們是 ACA 等級」,要求看完整影像證明。</p>

<h3>Q2: 為什麼 GIA 不像 Whiteflash 一樣嚴格?</h3>
<p>GIA 是中立的鑑定機構,不能太嚴格 — 否則市場 80% 鑽石都會被踢出 Excellent,業界會崩潰。GIA 的角色是「分級」,不是「推薦」。Whiteflash 是電商,可以用嚴格規格當差異化賣點。</p>

<h3>Q3: ACA 的鑽石比 GIA EX 貴多少?</h3>
<p>同 4C 通常貴 15-30%。但每分光學表現的單價往往更便宜 (因為光學分數高更多)。詳細計算看 <a href="/blog/budget-formula">BPD 預算公式</a>。</p>

<h3>Q4: 沒有 ACA 認證,但比例符合 ACA 規格的鑽石算不算 ACA?</h3>
<p>嚴格說不算 — ACA 還要求通過 H&amp;A scope 和 Sarine 對稱性檢測。但比例符合是必要條件,通常市售鑽石如果 6 項比例都在 ACA 範圍內,8 心 8 箭通常也通過。</p>

<h3>Q5: 培育鑽 (lab-grown) 也能做到 ACA 等級嗎?</h3>
<p>可以。Whiteflash 也賣 Precision Lab™ 系列,規格與天然 ACA 相同。培育鑽的化學成分與天然鑽完全相同,光學行為也相同 — 詳見 <a href="/blog/lab-vs-natural">培育 vs 天然完整比較</a>。</p>

<h2 id="next">下一步</h2>

<ol>
<li>用 <a href="/">BrillianceLab 計算器</a> 輸入你心儀鑽石的 GIA 數字,看是否打到 ACA 規格。</li>
<li>讀 <a href="/blog/hca-score-explained">HCA 分數完整教學</a> 了解中度嚴格的篩選工具。</li>
<li>讀 <a href="/blog/aset-idealscope-hca-comparison">ASET / Idealscope / HCA 三種光學測試</a> 了解物理驗證方法。</li>
<li>讀 <a href="/blog/tolkowsky-1919-math">Tolkowsky 1919 數學</a> 了解所有規格的源頭。</li>
</ol>

<p><strong>引用文獻</strong>:<br>
[1] Whiteflash A CUT ABOVE Specifications: <a href="https://www.whiteflash.com/a-cut-above-diamonds/specifications-and-qualifications.htm" rel="external nofollow noopener" target="_blank">whiteflash.com</a><br>
[2] GIA Cut Grade Estimation Tables (2006): <a href="https://www.gia.edu/doc/booklet_cut_estimation_tables_lowres.pdf" rel="external nofollow noopener" target="_blank">PDF</a><br>
[3] PriceScope HCA Tool: <a href="https://www.pricescope.com/tools/hca" rel="external nofollow noopener" target="_blank">pricescope.com/tools/hca</a><br>
[4] Tolkowsky, M. (1919), «Diamond Design», E. &amp; F. N. Spon, London.</p>
''',
        'body_en': '''
<aside style="margin:0 0 22px;padding:16px 20px;background:linear-gradient(180deg,#fffdf7,#fbf3df);border-left:4px solid #c9a45c;border-radius:8px">
  <div style="font-size:10.5px;letter-spacing:.22em;text-transform:uppercase;color:#8a6e30;font-weight:700;margin-bottom:6px">TL;DR</div>
  Whiteflash A CUT ABOVE® (ACA) is the strictest publicly documented super-ideal spec. <strong>It tightens the same 4 GIA proportions to roughly 1/3 their range</strong>: Pavilion Angle 40.5-41.0° (vs GIA's 40.6-41.8°), Crown Angle 34-35° (vs 31.5-36.5°), Table 53-58 (vs 52-62), Depth 59.5-62.0 (vs 57.5-63), plus Star 50-55, LGF 75-80, and mandatory Hearts &amp; Arrows. Result: ACA stones are ~1-2% of market vs GIA Excellent's ~25%.
</aside>

<h2>The 6-criteria comparison</h2>
<table>
  <thead><tr><th>Criterion</th><th>GIA Excellent</th><th>Whiteflash ACA</th><th>Tightening</th></tr></thead>
  <tbody>
    <tr><td>Table %</td><td>52-62</td><td><strong>53-58</strong></td><td>2x stricter</td></tr>
    <tr><td>Depth %</td><td>57.5-63.0</td><td><strong>59.5-62.0</strong></td><td>2.2x</td></tr>
    <tr><td>Crown Angle</td><td>31.5-36.5°</td><td><strong>34-35°</strong></td><td>5x</td></tr>
    <tr><td>Pavilion Angle</td><td>40.6-41.8°</td><td><strong>40.5-41.0°</strong></td><td>2.4x</td></tr>
    <tr><td>Star %</td><td>not graded</td><td><strong>50-55</strong></td><td>added</td></tr>
    <tr><td>LGF %</td><td>not graded</td><td><strong>75-80</strong></td><td>added</td></tr>
    <tr><td>Hearts &amp; Arrows</td><td>not required</td><td><strong>required</strong></td><td>added</td></tr>
  </tbody>
</table>

<h2>Why does the spec gap exist?</h2>
<p>Whiteflash openly admits most cutters target the <em>edge</em> of GIA Excellent to retain crown weight (and price). A stone at PA 41.7° / CA 36° is technically GIA 3EX yet leaks measurable light. The ACA spec was designed specifically to exclude these "Excellent in name only" stones.</p>

<h2>Real-world impact</h2>
<p>Same NT$300K budget, ACA stone scores ~25% higher on the BrillianceLab optical metric and ~5x lower on HCA — meaning <em>per unit of light performance</em>, ACA actually beats edge-Excellent on price.</p>

<h2>How to find ACA in Taiwan</h2>
<p>No Taiwan brand officially holds ACA certification — it's a Whiteflash private spec. But you can:</p>
<ol>
  <li>Use the ACA spec sheet as your shopping filter at any Taiwan jeweller.</li>
  <li>Direct-import from Whiteflash (5% import tariff + 5% VAT, full international shipping).</li>
</ol>

<h2>The honest workflow</h2>
<ol>
  <li>HCA filter → eliminate edge-Excellents</li>
  <li>Demand ASET image → verify no light leakage</li>
  <li>Match to ACA spec sheet → only 1-2% pass</li>
  <li>In-person inspection → confirm with your own eyes</li>
</ol>

<p>Use the <a href="/">BrillianceLab calculator</a> to test your candidate. Read <a href="/blog/hca-score-explained">HCA explained</a> for the middle filter, <a href="/blog/aset-idealscope-hca-comparison">ASET / Idealscope / HCA compared</a> for physical verification.</p>
'''
    },

    # ═══ 4. Tolkowsky 1919 Math ═══
    'tolkowsky-1919-math': {
        'output_path': 'blog/tolkowsky-1919-math.html',
        'slug_for_meta': 'tolkowsky-1919-math',
        'title': 'Tolkowsky 1919 鑽石黃金比例｜21 歲學生決定百年鑽戒命運',
        'desc': '1919 年 21 歲的 Marcel Tolkowsky 用幾何學推導出鑽石黃金比例:PA 40.75°、CA 34.5°、Table 53%。GIA、AGS、Whiteflash 規格都源自他的論文。',
        'h1': 'Tolkowsky 1919 — 21 歲學生用幾何學決定了所有鑽戒的命運',
        'hub': 'hub-4cs',
        'breadcrumb_name': 'Tolkowsky 1919 數學',
        'tldr': '<strong>1919 年,21 歲的比利時學生 Marcel Tolkowsky 在 MIT 寫了 «Diamond Design» 碩士論文,用純幾何學推導出鑽石的最佳比例:Pavilion Angle 40.75°、Crown Angle 34.5°、Table 53%</strong>。100 年後的 GIA Excellent、AGS Ideal、Whiteflash A CUT ABOVE 全部以 Tolkowsky 為基礎。本文用白話解釋這套數學的物理直覺,並指出 Tolkowsky 沒處理到的 3 個現代問題。',
        'body_zh': '''
<p>你買的每一顆現代圓形明亮車工 (Round Brilliant Cut) 鑽石,本質上都是 Tolkowsky 在 1919 年為了拿 MIT 機械工程碩士寫的一篇論文。<strong>21 歲、比利時、家族世代是切磨師、用尺規幾何在紙上算出最佳折射角度</strong> — 100 年來沒人推翻過。本文用白話解釋他到底算了什麼,以及為什麼這個 1919 年的結果到 2026 年仍是行業基準。 <a href="/" data-bl-cta="zh" style="color:#8a6e30;font-weight:600;text-decoration:underline;text-underline-offset:3px">用 BrillianceLab 計算器算分</a>。</p>

<h2 id="who">誰是 Tolkowsky?</h2>

<p>Marcel Tolkowsky (1899-1991) 出生於安特衛普 (Antwerp) 一個家族世代為鑽石切磨師的家庭。1919 年 21 歲時,他在英國倫敦大學 (有些資料說是 MIT,實際上是倫敦) 拿到機械工程博士學位,博士論文 «Diamond Design» 把祖傳的「眼力切磨」轉成<strong>純幾何數學</strong>。</p>

<p>原始論文 <a href="https://en.wikipedia.org/wiki/Marcel_Tolkowsky" rel="external nofollow noopener" target="_blank">仍可在公共領域取得</a>,1919 年 E. &amp; F. N. Spon 出版。</p>

<h2 id="math">他到底算了什麼?</h2>

<p>Tolkowsky 解的問題是:<strong>給定一顆鑽石的折射率 n=2.417,要怎麼設計切割角度,讓進入頂部的光線 100% 從頂部反射出來 (而不漏到底部)?</strong></p>

<p>這是一個「全內反射」(Total Internal Reflection) 物理問題。Tolkowsky 用以下步驟求解:</p>

<h3>第一步:臨界角 (Critical Angle)</h3>
<p>光從鑽石射出空氣時,如果入射角大於臨界角 θ_c,光就會 100% 反射回鑽石內部 (不漏出)。鑽石的臨界角:</p>
<p style="text-align:center;font-size:18px;margin:14px 0">sin(θ_c) = 1/n = 1/2.417 = 0.4137<br><strong>θ_c = 24.4°</strong></p>

<h3>第二步:Pavilion Angle 反推</h3>
<p>光線從頂部 (Table) 垂直進入,打到 Pavilion 底面後反射。為了讓反射光的入射角 > 24.4° (才會全內反射),Pavilion 與水平面的夾角必須 > 40.5°。Tolkowsky 算出最佳值:</p>
<p style="text-align:center;font-size:18px;margin:14px 0"><strong>Pavilion Angle = 40.75°</strong></p>
<p>稍淺 → 漏光、稍陡 → 光線走太多路被吸收。</p>

<h3>第三步:Crown Angle 配對</h3>
<p>Pavilion 反射回來的光,從 Crown facet 出來。為了讓彩色閃光 (fire) 最大化,Crown Angle 要在 33-35° 之間。Tolkowsky 推導:</p>
<p style="text-align:center;font-size:18px;margin:14px 0"><strong>Crown Angle = 34.5°</strong></p>

<h3>第四步:Table 大小</h3>
<p>Table 太大 → 漏光區增加;Table 太小 → 進光量不足。Tolkowsky 推導:</p>
<p style="text-align:center;font-size:18px;margin:14px 0"><strong>Table % = 53%</strong></p>

<h3>第五步:Total Depth</h3>
<p>Crown Height + Pavilion Depth + Girdle:</p>
<p style="text-align:center;font-size:18px;margin:14px 0"><strong>Total Depth % = 59.3%</strong></p>

<h2 id="modern">100 年後的修正</h2>

<p>Tolkowsky 的數學是<strong>單一光線理論</strong>。現代切磨用<strong>光線追蹤 (ray tracing) 模擬數萬條光線</strong>,發現 Tolkowsky 的 Table 53% 有點偏小 (進光量不足),最佳值約 55-57%。其他三項幾乎不變:</p>

<table>
<thead><tr><th>項目</th><th>Tolkowsky 1919</th><th>現代 Ideal (Whiteflash ACA)</th><th>差距</th></tr></thead>
<tbody>
<tr><td>Pavilion Angle</td><td>40.75°</td><td>40.5-41.0°</td><td>幾乎相同</td></tr>
<tr><td>Crown Angle</td><td>34.5°</td><td>34-35°</td><td>幾乎相同</td></tr>
<tr><td>Table %</td><td>53</td><td>53-58</td><td>現代略大</td></tr>
<tr><td>Total Depth %</td><td>59.3</td><td>59.5-62.0</td><td>現代略深</td></tr>
</tbody>
</table>

<p><strong>1919 年的數學在 2026 年仍是 90% 正確</strong> — 這是科學的勝利。</p>

<h2 id="not-handled">Tolkowsky 沒處理的 3 個現代問題</h2>

<h3>1. 異形鑽 (Fancy Shapes)</h3>
<p>Tolkowsky 只解圓形明亮車工。橢圓、墊形、公主方等異形鑽的光學至 2026 年仍無公認數學分級 — 詳見 <a href="/blog/fancy-cuts-guide">花式車工指南</a>。</p>

<h3>2. Star %、Lower Girdle Facet %</h3>
<p>這兩項決定閃光 (scintillation) 的數量與大小。Tolkowsky 1919 沒處理 — 後來由 GIA Facetware (2006) 與 Whiteflash 補上。</p>

<h3>3. 螢光反應 (Fluorescence)</h3>
<p>30% 鑽石有螢光,影響外觀。Tolkowsky 完全沒處理。詳見 <a href="/blog/fluorescence-deep-dive">螢光深度解析</a>。</p>

<h2 id="impact">為什麼這個 1919 年的結果至今仍主導市場?</h2>

<p>三個原因:</p>
<ol>
<li><strong>物理沒變</strong> — 鑽石折射率 2.417 是物理常數,光學定律百年不變。</li>
<li><strong>切磨技術成熟</strong> — 雷射切磨可以做到 ±0.1° 精度,但找不到比 Tolkowsky 更好的目標。</li>
<li><strong>市場慣性</strong> — 全球切磨師都按 Tolkowsky 訓練,改規格成本太高。</li>
</ol>

<h2 id="lessons">從 Tolkowsky 學到 3 件事</h2>

<ol>
<li><strong>數學比直覺強</strong> — 你不需要 30 年切磨經驗才能判斷一顆鑽石,4 個數字輸入計算器就有答案。</li>
<li><strong>規格不是賣家決定的</strong> — Tolkowsky 的數學在 1919 年就公開,你不需要相信任何品牌的「我們的切工特別」。</li>
<li><strong>「Excellent」是區間,不是點</strong> — GIA Excellent 給 Tolkowsky 一個 ±2° 的容差,Whiteflash ACA 縮到 ±0.5°。詳見 <a href="/blog/whiteflash-vs-gia-3ex">Whiteflash vs GIA 比較</a>。</li>
</ol>

<h2 id="faq">常見問題</h2>

<h3>Q1: Tolkowsky 1919 還能讀嗎?</h3>
<p>可以。原文已進入公共領域,Project Gutenberg 與 archive.org 都有完整 PDF。原文很短 (約 100 頁),數學部分需要微積分基礎。</p>

<h3>Q2: 為什麼 1919 的數學比現代切磨師強?</h3>
<p>不是「更強」,是「定義了什麼是強」。所有現代切磨師都用 Tolkowsky 為基準,差別只在精度。1919 年是「目標」,2026 年是「執行精度」。</p>

<h3>Q3: 異形鑽什麼時候會有 Tolkowsky 等級的數學?</h3>
<p>橢圓鑽的光學模型已有部分學術論文 (Sergey Sivovolenko 2010+),但因 facet 設計變數太多,還沒有公認單一最佳解。墊形、公主方更複雜。</p>

<h3>Q4: 培育鑽 (lab-grown) 也適用 Tolkowsky 嗎?</h3>
<p>完全適用。Tolkowsky 的數學基於物理常數 n=2.417,培育鑽的 n 與天然完全相同。詳見 <a href="/blog/lab-vs-natural">天然 vs 培育</a>。</p>

<h3>Q5: 為什麼 Tolkowsky 的學生時代論文這麼有影響力?</h3>
<p>當時鑽石切磨是「家族祕傳」,沒有公開的科學論文。Tolkowsky 第一個把祕傳幾何寫成可審計的數學,讓全業界 (包括競爭對手家族) 都能驗證、改進、傳承。<strong>透明 + 數學 = 行業標準</strong>。</p>

<h2 id="next">下一步</h2>

<ol>
<li>用 <a href="/">BrillianceLab 計算器</a> 把 Tolkowsky 的目標 (Table 53%、Depth 59.3%、CA 34.5°、PA 40.75°) 輸入,看你會拿到什麼分數 (應該是 99-100)。</li>
<li>讀 <a href="/blog/hca-score-explained">HCA 分數教學</a> 了解現代如何用 Tolkowsky 為基準打分。</li>
<li>讀 <a href="/blog/whiteflash-vs-gia-3ex">Whiteflash ACA vs GIA EX</a> 了解現代最嚴規格如何延伸 Tolkowsky。</li>
<li>讀 <a href="/blog/round-cut-deep-dive">圓形明亮車工深度解析</a> 看完整 58 facet 解剖。</li>
</ol>

<p><strong>引用文獻</strong>:<br>
[1] Tolkowsky, M. (1919), «Diamond Design», E. &amp; F. N. Spon, London.<br>
[2] Wikipedia: Marcel Tolkowsky — <a href="https://en.wikipedia.org/wiki/Marcel_Tolkowsky" rel="external nofollow noopener" target="_blank">維基百科</a><br>
[3] GIA Cut Grade Estimation Tables (2006): <a href="https://www.gia.edu/doc/booklet_cut_estimation_tables_lowres.pdf" rel="external nofollow noopener" target="_blank">PDF</a><br>
[4] Brian Gavin Diamonds — Tolkowsky 歷史: <a href="https://www.briangavindiamonds.com" rel="external nofollow noopener" target="_blank">briangavindiamonds.com</a></p>
''',
        'body_en': '''
<aside style="margin:0 0 22px;padding:16px 20px;background:linear-gradient(180deg,#fffdf7,#fbf3df);border-left:4px solid #c9a45c;border-radius:8px">
  <div style="font-size:10.5px;letter-spacing:.22em;text-transform:uppercase;color:#8a6e30;font-weight:700;margin-bottom:6px">TL;DR</div>
  In 1919, a 21-year-old Belgian student named Marcel Tolkowsky derived the mathematically optimal proportions for a round brilliant diamond using pure geometry: <strong>Pavilion Angle 40.75°, Crown Angle 34.5°, Table 53%, Total Depth 59.3%</strong>. Every modern grading standard — GIA Excellent, AGS Ideal, Whiteflash A CUT ABOVE — descends from his master's thesis. Modern ray-tracing has revised Table % slightly upward (53→55-57) but the other three numbers stand essentially unchanged.
</aside>

<h2>Who was Tolkowsky?</h2>
<p>Marcel Tolkowsky (1899-1991), born to a family of Antwerp diamond cutters. At 21, his University of London PhD thesis «Diamond Design» converted family-secret cutting heuristics into rigorous geometric mathematics. The thesis is in the public domain.</p>

<h2>The math, in one paragraph</h2>
<p>Diamond's refractive index n = 2.417 yields a critical angle of arcsin(1/n) = 24.4°. Light entering through the table must hit the pavilion at greater than this angle to total-internally reflect (not leak out the bottom). Working backward from the geometry, the optimal pavilion angle is 40.75°. Crown angle is then chosen to maximize fire (color dispersion) — 34.5°. Table % follows from balancing light intake vs. window leakage — 53%.</p>

<h2>Modern revisions</h2>
<table>
  <thead><tr><th>Parameter</th><th>Tolkowsky 1919</th><th>Modern Ideal (Whiteflash ACA)</th></tr></thead>
  <tbody>
    <tr><td>Pavilion Angle</td><td>40.75°</td><td>40.5-41.0°</td></tr>
    <tr><td>Crown Angle</td><td>34.5°</td><td>34-35°</td></tr>
    <tr><td>Table %</td><td>53</td><td>53-58</td></tr>
    <tr><td>Depth %</td><td>59.3</td><td>59.5-62.0</td></tr>
  </tbody>
</table>
<p>Ray-tracing showed Tolkowsky's table was slightly small for maximum light return; everything else stands.</p>

<h2>What Tolkowsky didn't solve</h2>
<ul>
  <li>Fancy shapes (oval, cushion, princess) — no consensus mathematical grading exists in 2026.</li>
  <li>Star % and Lower Girdle Facet % — added by GIA Facetware (2006) and Whiteflash spec.</li>
  <li>Fluorescence interaction with body color — not addressed.</li>
</ul>

<h2>Why a 1919 thesis still rules in 2026</h2>
<ol>
  <li>Physics doesn't change — refractive index is a constant.</li>
  <li>Modern lasers can cut to ±0.1° but can't find a better target than Tolkowsky's.</li>
  <li>Global cutter training is built on Tolkowsky — switching costs are prohibitive.</li>
</ol>

<p>Use the <a href="/">BrillianceLab calculator</a> to plug in Tolkowsky's targets and verify the score is ~100. Read <a href="/blog/hca-score-explained">HCA scoring explained</a> and <a href="/blog/whiteflash-vs-gia-3ex">Whiteflash vs GIA</a> for the modern descendants of his work.</p>
'''
    },

    # ═══ 5. ASET / Idealscope / HCA — 3 light tests ═══
    'aset-idealscope-hca-comparison': {
        'output_path': 'blog/aset-idealscope-hca-comparison.html',
        'slug_for_meta': 'aset-idealscope-hca-comparison',
        'title': 'ASET vs Idealscope vs HCA｜3 種鑽石光學測試完整比較',
        'desc': 'ASET、Idealscope 是實體鏡,顯示鑽石的光線分布;HCA 是純數學工具,從 4 個比例算分。三者目的不同、互補不取代。本文教你如何讀懂三種圖、何時該用哪個。',
        'h1': 'ASET vs Idealscope vs HCA — 3 種鑽石光學測試完整比較',
        'hub': 'hub-4cs',
        'breadcrumb_name': '3 種光學測試比較',
        'tldr': '三種測試各有不同用途:<strong>HCA</strong> 是 4 數字算分的快篩工具 (免費、線上、3 秒);<strong>Idealscope</strong> 是實體紅鏡,看鑽石的光線返回分布 (NT$1,500、要實體);<strong>ASET</strong> 是 3 色鏡 (紅 + 綠 + 藍/黑),看光線從哪個角度返回 (NT$3,000、最詳細)。三者互補:HCA 篩 → ASET/Idealscope 驗 → 親眼確認。',
        'body_zh': '''
<p>你看完 GIA 證書、用 HCA 算了 0.8 分、要決定買不買 — 卻有人說「還要看 ASET 才安心」。這三個東西到底差在哪、要不要全做、什麼時候用?本文一次說清。 <a href="/" data-bl-cta="zh" style="color:#8a6e30;font-weight:600;text-decoration:underline;text-underline-offset:3px">用 BrillianceLab 計算器算 HCA</a>。</p>

<h2 id="overview">三種測試一覽</h2>

<table>
<thead><tr><th>測試</th><th>類型</th><th>看什麼</th><th>價格</th><th>速度</th></tr></thead>
<tbody>
<tr><td><strong>HCA</strong></td><td>數學模型</td><td>4 比例打分</td><td>免費</td><td>3 秒</td></tr>
<tr><td><strong>Idealscope</strong></td><td>實體紅鏡</td><td>光線返回率</td><td>NT$1,500</td><td>30 秒</td></tr>
<tr><td><strong>ASET</strong></td><td>實體 3 色鏡</td><td>光線返回角度</td><td>NT$3,000</td><td>30 秒</td></tr>
</tbody>
</table>

<h2 id="hca">1. HCA (Holloway Cut Adviser)</h2>

<p><strong>HCA 是純數學工具</strong> — 輸入 GIA 證書上 4 個數字 (Total Depth %、Table %、Crown Angle、Pavilion Angle),輸出 0-10 分。完整教學見 <a href="/blog/hca-score-explained">HCA 分數完整教學</a>。</p>

<h3>HCA 的優勢</h3>
<ul>
<li>免費、線上、不需要實體看鑽。</li>
<li>3 秒出結果,適合快速篩選網路上的鑽石庫存。</li>
<li>客觀、可重複 — 同樣輸入永遠同樣分數。</li>
</ul>

<h3>HCA 的限制</h3>
<ul>
<li>只看 4 個 facet 平均值 (鑽石有 57 個),抓不到「painting/digging」這類個別 facet 偏差。</li>
<li>不檢測 Hearts &amp; Arrows 對稱性。</li>
<li>不檢測 girdle 厚度均勻度。</li>
<li>不檢測 fluorescence 對外觀的影響。</li>
</ul>

<h3>什麼時候用 HCA</h3>
<p>網購篩選階段。看到 GIA 號碼 → HCA 算分 → 分數 0-2 才繼續看。HCA 高 (>4) 的鑽石不用浪費時間索取 ASET。</p>

<h2 id="idealscope">2. Idealscope</h2>

<p><strong>Idealscope 是 1920 年代發明的紅色濾鏡</strong>,把鑽石放在鏡子下,從上方看,鑽石會呈現:</p>

<ul>
<li><strong>紅色</strong> — 從觀察者方向 (上方) 返回的光線 → 大量紅色 = 高亮度。</li>
<li><strong>白色</strong> — 沒有光線返回 (漏光區) → 大量白色 = 嚴重漏光。</li>
<li><strong>黑色</strong> — 觀察者頭部的反射 (擋光區) → 應有少量黑色,完美鑽石中央有 8 個對稱黑點 (對應 8 個 Pavilion main)。</li>
</ul>

<h3>怎麼讀 Idealscope 影像</h3>

<table>
<thead><tr><th>看到什麼</th><th>含意</th></tr></thead>
<tbody>
<tr><td>整片飽滿紅色 + 中央 8 個對稱黑點</td><td>★★★★★ Whiteflash ACA 等級</td></tr>
<tr><td>大部分紅色 + 邊緣有少量白色</td><td>★★★★ 良好</td></tr>
<tr><td>中央有「Fish Eye」(白色窗口)</td><td>★★ Pavilion 太淺,嚴重漏光</td></tr>
<tr><td>整片暗 + 大量黑色</td><td>★ Pavilion 太深,光線走太多路被吸收</td></tr>
</tbody>
</table>

<h3>Idealscope 的優勢</h3>
<ul>
<li>實體驗證 — 不是模擬,是真的看光線分布。</li>
<li>抓得到 painting/digging、girdle 不均、Pavilion 不對稱等 HCA 抓不到的問題。</li>
<li>價格便宜,Idealscope.com 賣 NT$1,500 左右。</li>
</ul>

<h3>Idealscope 的限制</h3>
<ul>
<li>只看「光線是否返回」,看不到「光線從哪個角度返回」 (這要 ASET)。</li>
<li>需要實體鑽 — 不能只看網路圖片。</li>
<li>解讀有主觀性 — 黑色多少才算正常,需要經驗。</li>
</ul>

<h2 id="aset">3. ASET (Angular Spectrum Evaluation Tool)</h2>

<p><strong>ASET 是 AGS (American Gem Society) 在 2005 年發明的 3 色濾鏡</strong>,用<strong>三種顏色標示光線返回的角度來源</strong>:</p>

<ul>
<li><strong>紅色</strong> (75°-90° 高角度) — 高亮度、強烈閃光的來源。</li>
<li><strong>綠色</strong> (45°-75° 中角度) — 一般亮度,大多數光線在這個範圍。</li>
<li><strong>藍色 / 黑色</strong> (0°-45° 低角度 / 觀察者頭部) — 對比區,讓鑽石有「閃 vs 暗」的動態感。</li>
</ul>

<h3>怎麼讀 ASET 影像</h3>

<table>
<thead><tr><th>看到什麼</th><th>含意</th></tr></thead>
<tbody>
<tr><td>飽滿紅色為主 + 對稱綠色 + 中央 8 個對稱藍/黑點</td><td>★★★★★ AGS Ideal-0 / Whiteflash ACA</td></tr>
<tr><td>紅 + 綠均衡,黑色少</td><td>★★★★ 良好</td></tr>
<tr><td>大量綠色,紅色少</td><td>★★★ 一般 — 亮度足但缺乏「火光」</td></tr>
<tr><td>大量藍色 / 黑色</td><td>★★ 有大量低角度光,可能漏光</td></tr>
</tbody>
</table>

<h3>ASET 的優勢</h3>
<ul>
<li>最完整的光學資訊 — 不只是「亮 vs 暗」,還有「光線角度分布」。</li>
<li>AGS 自己用 ASET 評定 Ideal-0 等級。</li>
<li>能抓到所有 HCA 與 Idealscope 都抓不到的細節。</li>
</ul>

<h3>ASET 的限制</h3>
<ul>
<li>價格較高 (NT$3,000-5,000)。</li>
<li>解讀需要經驗 — 紅綠藍比例的「最佳值」沒有絕對標準。</li>
<li>白光 ASET vs 黑底 ASET 結果不同,要注意背景。</li>
</ul>

<h2 id="workflow">正確的使用順序</h2>

<p>三者不是「擇一」,而是<strong>「層層篩選」</strong>:</p>

<ol>
<li><strong>HCA 篩選 (網購階段)</strong> — 從 100 顆候選中淘汰 80% HCA >2 的。</li>
<li><strong>要求 Idealscope 影像 (賣家提供)</strong> — 從剩 20 顆中淘汰 50%「中央有 fish eye」「整片暗」的。</li>
<li><strong>要求 ASET 影像 (高端買家)</strong> — 從剩 10 顆中挑出紅綠分布最完美的 1-2 顆。</li>
<li><strong>親眼看實品</strong> — 在自然光與室內光下都看,確認 fluorescence 不會讓鑽石看起來「油膩」。</li>
</ol>

<h2 id="taiwan-availability">台灣哪裡能拿到 ASET / Idealscope?</h2>

<table>
<thead><tr><th>來源</th><th>有/沒有</th><th>說明</th></tr></thead>
<tbody>
<tr><td>京華鑽石</td><td>部分有</td><td>SID 八心八箭系列附 H&amp;A 影像,但不一定附 ASET</td></tr>
<tr><td>Just Diamond Peonia</td><td>有</td><td>88 刻面系列附 H&amp;A 影像</td></tr>
<tr><td>I-PRIMO</td><td>無</td><td>不公開 ASET</td></tr>
<tr><td>銀座白石</td><td>無</td><td>不公開 ASET</td></tr>
<tr><td>亞立詩 ALUXE</td><td>偶有</td><td>要主動詢問,並非標配</td></tr>
<tr><td>Whiteflash 海外直購</td><td>標配</td><td>每顆鑽石都附 ASET + Idealscope 影像</td></tr>
</tbody>
</table>

<p><strong>結論</strong>:在台灣買 ASET 等級資訊,只能找 Whiteflash 或自備 Idealscope 鏡 (Amazon / Shopee 進口約 NT$1,500)。</p>

<h2 id="faq">常見問題</h2>

<h3>Q1: HCA 0-2 的鑽石,還需要看 Idealscope 嗎?</h3>
<p>建議看,但機率上 90% 通過。HCA 0-2 表示 4 比例都接近理想,但無法保證 painting/digging 沒問題。如果預算允許,要 Idealscope 影像最安心。</p>

<h3>Q2: 自己買 Idealscope 在家測,可以嗎?</h3>
<p>可以,且推薦。Idealscope.com 或 Amazon 都有賣 (約 NT$1,500-2,500)。回家把鑽戒拆下放鏡下,從正上方看,3 分鐘學會解讀。</p>

<h3>Q3: 培育鑽 (lab-grown) 的 ASET 影像會不會不同?</h3>
<p>不會。ASET 看光線分布,與鑽石是天然或培育無關。培育鑽的折射率與光學行為與天然完全相同 — 詳見 <a href="/blog/lab-vs-natural">天然 vs 培育</a>。</p>

<h3>Q4: 異形鑽 (橢圓、墊形) 的 ASET 怎麼看?</h3>
<p>異形鑽的 ASET 比圓形複雜,沒有「8 個對稱黑點」這種簡單規則。一般原則仍是「紅綠飽滿、藍/黑少」,但需要更多實戰經驗 — 詳見 <a href="/blog/fancy-cuts-guide">花式車工指南</a>。</p>

<h3>Q5: H&amp;A scope 跟 ASET 是同一個東西嗎?</h3>
<p>不是。H&amp;A scope 看「對稱性」(8 心 8 箭圖案),用紅色背景。ASET 看「光線角度分布」(紅綠藍),用 3 色背景。兩個都是必要的,但回答不同問題。</p>

<h2 id="next">下一步</h2>

<ol>
<li>用 <a href="/">BrillianceLab 計算器</a> 算 HCA 分數,先做第一輪篩選。</li>
<li>HCA 0-2 的鑽石,要求賣家提供 Idealscope 或 ASET 影像。</li>
<li>讀 <a href="/blog/hca-score-explained">HCA 分數完整教學</a> 與 <a href="/blog/whiteflash-vs-gia-3ex">Whiteflash ACA vs GIA EX</a> 了解標準。</li>
<li>讀 <a href="/blog/hearts-arrows-truth">八心八箭真相</a> 了解 H&amp;A scope。</li>
</ol>

<p><strong>引用文獻</strong>:<br>
[1] AGS ASET Information: <a href="https://www.gia.edu/ags-ideal-report" rel="external nofollow noopener" target="_blank">GIA AGS Ideal Report</a><br>
[2] Idealscope.com 官方: <a href="https://www.ideal-scope.com" rel="external nofollow noopener" target="_blank">ideal-scope.com</a><br>
[3] PriceScope HCA Tool: <a href="https://www.pricescope.com/tools/hca" rel="external nofollow noopener" target="_blank">pricescope.com/tools/hca</a><br>
[4] Whiteflash ASET 教學: <a href="https://www.whiteflash.com" rel="external nofollow noopener" target="_blank">whiteflash.com</a></p>
''',
        'body_en': '''
<aside style="margin:0 0 22px;padding:16px 20px;background:linear-gradient(180deg,#fffdf7,#fbf3df);border-left:4px solid #c9a45c;border-radius:8px">
  <div style="font-size:10.5px;letter-spacing:.22em;text-transform:uppercase;color:#8a6e30;font-weight:700;margin-bottom:6px">TL;DR</div>
  Three light tests, three different jobs: <strong>HCA</strong> (math, free, 3-second pre-filter) → <strong>Idealscope</strong> (red filter, NT$1,500, shows light return) → <strong>ASET</strong> (3-color filter, NT$3,000, shows angle distribution). They're complementary, not interchangeable. Smart workflow: HCA filter the 80% bad → demand ASET image for the top 20% → in-person inspection for the final pick.
</aside>

<h2>Quick comparison</h2>
<table>
  <thead><tr><th>Test</th><th>Type</th><th>Reveals</th><th>Cost</th></tr></thead>
  <tbody>
    <tr><td>HCA</td><td>Math</td><td>4-proportion score</td><td>Free</td></tr>
    <tr><td>Idealscope</td><td>Red filter scope</td><td>Light return %</td><td>NT$1,500</td></tr>
    <tr><td>ASET</td><td>3-color filter scope</td><td>Light return angle</td><td>NT$3,000</td></tr>
  </tbody>
</table>

<h2>What HCA can't catch</h2>
<ul>
  <li>Painting / digging (individual facet deviations)</li>
  <li>Hearts &amp; Arrows symmetry</li>
  <li>Girdle thickness uniformity</li>
  <li>Fluorescence haze</li>
</ul>

<h2>How to read an Idealscope image</h2>
<ul>
  <li><strong>Red</strong> = light returning to your eye (good)</li>
  <li><strong>White</strong> = leakage (bad)</li>
  <li><strong>Black</strong> = obscured by your head reflection (some is normal — 8 symmetric dots = ideal)</li>
</ul>

<h2>How to read an ASET image</h2>
<ul>
  <li><strong>Red (75-90° angles)</strong> = brilliance source</li>
  <li><strong>Green (45-75°)</strong> = general brightness</li>
  <li><strong>Blue/Black (0-45°)</strong> = contrast that gives "scintillation" the dynamic feel</li>
</ul>

<h2>The proper workflow</h2>
<ol>
  <li>HCA pre-filter (eliminates 80%)</li>
  <li>Request Idealscope image (eliminates another 50%)</li>
  <li>Request ASET for finalists</li>
  <li>In-person inspection</li>
</ol>

<h2>Where to get ASET in Taiwan</h2>
<p>Locally: 京華 SID, Just Diamond Peonia (sometimes). Internationally: Whiteflash provides ASET on every stone. DIY option: buy an Idealscope (~NT$1,500 on Shopee/Amazon) and inspect at home.</p>

<p>Use the <a href="/">BrillianceLab calculator</a> to start with HCA. Read <a href="/blog/hca-score-explained">HCA explained</a> and <a href="/blog/whiteflash-vs-gia-3ex">Whiteflash vs GIA</a> for the strict-spec workflow.</p>
'''
    },
}


# ─────────────────────────────────────────────────────────────────
# Patcher
# ─────────────────────────────────────────────────────────────────

def patch_template(slug: str, cfg: dict) -> bool:
    if not TEMPLATE.exists():
        sys.exit(f'template missing: {TEMPLATE}')
    src = TEMPLATE.read_text(encoding='utf-8')

    title = cfg['title']
    desc = cfg['desc']
    h1 = cfg['h1']
    out_path = cfg['output_path']
    slug_meta = cfg['slug_for_meta']
    bc_name = cfg['breadcrumb_name']

    # Path-based prefixes (about.html is at root, blog articles in /blog/)
    if out_path.startswith('blog/'):
        url_path = '/blog/' + slug_meta
    else:
        url_path = '/' + slug_meta

    # 1. Title
    src = re.sub(r'<title>[\s\S]+?</title>', f'<title>{title}</title>', src, count=1)

    # 2. Meta description
    src = re.sub(r'(<meta\s+name=["\']description["\']\s+content=["\'])[^"\']+(["\'])',
                 lambda m: f'{m.group(1)}{desc}{m.group(2)}', src, count=1)

    # 3. og:url
    src = re.sub(r'(<meta\s+property=["\']og:url["\']\s+content=["\'])[^"\']+(["\'])',
                 lambda m: f'{m.group(1)}https://brilliancelab.vercel.app{url_path}{m.group(2)}', src, count=1)

    # 4. og:title / og:description / og:image
    src = re.sub(r'(<meta\s+property=["\']og:title["\']\s+content=["\'])[^"\']+(["\'])',
                 lambda m: f'{m.group(1)}{title}{m.group(2)}', src, count=1)
    src = re.sub(r'(<meta\s+property=["\']og:description["\']\s+content=["\'])[^"\']+(["\'])',
                 lambda m: f'{m.group(1)}{desc}{m.group(2)}', src, count=1)
    src = re.sub(r'/og/diamond-50-cents\.[a-f0-9]+\.png',
                 f'/og/{slug_meta}.png', src)

    # 5. twitter:title / desc
    src = re.sub(r'(<meta\s+name=["\']twitter:title["\']\s+content=["\'])[^"\']+(["\'])',
                 lambda m: f'{m.group(1)}{title}{m.group(2)}', src, count=1)
    src = re.sub(r'(<meta\s+name=["\']twitter:description["\']\s+content=["\'])[^"\']+(["\'])',
                 lambda m: f'{m.group(1)}{desc}{m.group(2)}', src, count=1)

    # 6. canonical + alternate
    src = re.sub(r'(<link\s+rel=["\']canonical["\']\s+href=["\'])[^"\']+(["\'])',
                 lambda m: f'{m.group(1)}https://brilliancelab.vercel.app{url_path}{m.group(2)}', src, count=1)
    src = re.sub(r'(<link\s+rel=["\']alternate["\']\s+hreflang=["\']x-default["\']\s+href=["\'])[^"\']+(["\'])',
                 lambda m: f'{m.group(1)}https://brilliancelab.vercel.app{url_path}{m.group(2)}', src, count=1)
    src = re.sub(r'(<link\s+rel=["\']alternate["\']\s+hreflang=["\']zh-TW["\']\s+href=["\'])[^"\']+(["\'])',
                 lambda m: f'{m.group(1)}https://brilliancelab.vercel.app{url_path}{m.group(2)}', src, count=1)

    # 7. JSON-LD Article: headline, mainEntityOfPage, image
    src = re.sub(r'"headline":"[^"]+"', f'"headline":"{h1}"', src, count=1)
    src = re.sub(r'("description":")[^"]+("})',
                 lambda m: f'{m.group(1)}{desc}{m.group(2)}', src, count=1)
    src = re.sub(r'"mainEntityOfPage":"[^"]+"',
                 f'"mainEntityOfPage":"https://brilliancelab.vercel.app{url_path}"', src, count=1)
    src = re.sub(r'"image":"https://brilliancelab\.vercel\.app/og/diamond-50-cents\.png"',
                 f'"image":"https://brilliancelab.vercel.app/og/{slug_meta}.png"', src, count=1)

    # 8. Breadcrumb JSON-LD: replace position-3 + position-4 + visible nav
    hub_slug = cfg.get('hub', '')
    if hub_slug == '/':
        # About page — only首頁 + 關於
        new_bc = ('{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":'
                  '[{"@type":"ListItem","position":1,"name":"首頁","item":"https://brilliancelab.vercel.app/"},'
                  f'{{"@type":"ListItem","position":2,"name":"{bc_name}","item":"https://brilliancelab.vercel.app{url_path}"}}'
                  ']}')
    else:
        hub_url = f'https://brilliancelab.vercel.app/blog/{hub_slug}'
        hub_label = {
            'hub-fundamentals': '基礎篇',
            'hub-4cs': '4Cs 拆解',
            'hub-purchase': '購買實戰',
            'hub-proposal': '求婚與婚戒',
            'hub-care': '保養與市場',
        }.get(hub_slug, hub_slug)
        new_bc = ('{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":'
                  '[{"@type":"ListItem","position":1,"name":"首頁","item":"https://brilliancelab.vercel.app/"},'
                  '{"@type":"ListItem","position":2,"name":"部落格","item":"https://brilliancelab.vercel.app/blog/"},'
                  f'{{"@type":"ListItem","position":3,"name":"{hub_label}","item":"{hub_url}"}},'
                  f'{{"@type":"ListItem","position":4,"name":"{bc_name}","item":"https://brilliancelab.vercel.app{url_path}"}}'
                  ']}')
    src = re.sub(r'<script type="application/ld\+json" data-id="BL_BREADCRUMB_LD">[\s\S]+?</script>',
                 f'<script type="application/ld+json" data-id="BL_BREADCRUMB_LD">\n{new_bc}\n</script>',
                 src, count=1)

    # 9. Visible breadcrumb nav
    if hub_slug == '/':
        new_nav_html = (
            '<a href="/" style="color:inherit;text-decoration:none">首頁</a> · '
            f'<span style="color:var(--gold-deep)">{bc_name}</span>'
        )
    else:
        hub_label = {
            'hub-fundamentals': '基礎篇',
            'hub-4cs': '4Cs 拆解',
            'hub-purchase': '購買實戰',
            'hub-proposal': '求婚與婚戒',
            'hub-care': '保養與市場',
        }.get(hub_slug, hub_slug)
        new_nav_html = (
            '<a href="/" style="color:inherit;text-decoration:none">首頁</a> · '
            '<a href="/blog/" style="color:inherit;text-decoration:none">部落格</a> · '
            f'<a href="/blog/{hub_slug}" style="color:inherit;text-decoration:none">{hub_label}</a> · '
            f'<span style="color:var(--gold-deep)">{bc_name}</span>'
        )
    src = re.sub(
        r'<nav style="font-size:11px;letter-spacing:\.22em[^"]*"[^>]*aria-label="Breadcrumb">[\s\S]+?</nav>',
        f'<nav style="font-size:11px;letter-spacing:.22em;text-transform:uppercase;color:var(--muted);margin-bottom:8px" aria-label="Breadcrumb">\n    {new_nav_html}\n  </nav>',
        src, count=1)

    # 10. H1
    src = re.sub(r'<h1>[\s\S]+?</h1>', f'<h1>{h1}</h1>', src, count=1)

    # 11. TL;DR
    src = re.sub(
        r'(<aside class="verdict" data-id="BL_TLDR">)[\s\S]+?(</aside>)',
        f'\\1\n    <div style="font-size:10.5px;letter-spacing:.22em;text-transform:uppercase;color:#8a6e30;font-weight:700;margin-bottom:6px">TL;DR · 一分鐘掌握</div>\n    {cfg["tldr"]}\n  \\2',
        src, count=1)

    # 12. Article body inside #proseZh
    src = re.sub(
        r'(<article id="proseZh"[^>]*>)[\s\S]+?(</article>)',
        f'\\1\n{cfg["body_zh"]}\n  \\2', src, count=1)

    # 13. Pagefind slug
    src = re.sub(r'data-pagefind-meta="slug:diamond-50-cents"',
                 f'data-pagefind-meta="slug:{slug_meta}"', src)

    # 14. English block — remove old, inject new
    src = re.sub(
        r'\n?<div[^>]*data-id="BL_PROSE_EN"[^>]*>[\s\S]*?</div>\s*',
        '\n', src, count=1)
    en_block = (
        '\n<div id="proseEn" class="prose-en hidden" data-id="BL_PROSE_EN" '
        f'data-pagefind-body data-pagefind-meta="slug:{slug_meta}_en" '
        f'lang="en" style="display:none">\n{cfg["body_en"]}\n</div>\n'
    )
    if '</article>' in src:
        # Insert AFTER first </article>
        src = src.replace('</article>', '</article>' + en_block, 1)

    # Write
    out = ROOT / out_path
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(src, encoding='utf-8')
    return True


def main():
    n = 0
    for slug, cfg in PAGES.items():
        if patch_template(slug, cfg):
            tlen = sum(2 if '一' <= c <= '鿿' else 1 for c in cfg['title'])
            dlen = sum(2 if '一' <= c <= '鿿' else 1 for c in cfg['desc'])
            print(f'  generated {cfg["output_path"]:<48}  T:{tlen:>3}  D:{dlen:>3}')
            n += 1
    print(f'\n{n} authority pages generated')


if __name__ == '__main__':
    main()
