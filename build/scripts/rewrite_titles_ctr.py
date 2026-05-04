# -*- coding: utf-8 -*-
"""
Round 15 — CTR Surgery.

Rewrites <title> and <meta name="description"> on every article using a
formula derived from competitive SERP research:

  TITLE  = [Number/Question/Year hook] + [Primary keyword] + [Emotional sub-hook]
  DESC   = [Number fact, ≤14 chars] + [2nd-person pain point] + [CTA + benefit + year]

Key principles from competitor analysis (I-PRIMO, ALUXE, I-Diamond, Herley,
Tiffany, Artemis, 京華鑽石, 侏羅紀, Dcard threads):

  1. DROP the "| BrillianceLab" brand suffix — we have zero brand recognition
     in TW. Save those 14 chars for emotional hooks.
  2. Add year (2026) to every commercial title — competitor table-stakes.
  3. Use question form ("是什麼？", "怎麼挑？") on educational articles.
  4. Use scare hooks ("踩雷", "別當盤子", "後悔") on buyer-intent articles —
     this niche is owned by Dcard threads only; brand sites refuse to use it.
  5. Front-load NT$ price ranges in price articles.
  6. Mirror "People Also Ask" wording so we win PAA snippets.

Idempotent: re-run safely. The full <title> and <meta description> are
replaced wholesale per slug from the REWRITES dict.

Run:  python build/scripts/rewrite_titles_ctr.py
"""
from __future__ import annotations
import re, sys
from pathlib import Path

# auto-locate repo root
import os as _os
_os.chdir(Path(__file__).resolve().parents[2])

try: sys.stdout.reconfigure(encoding='utf-8')
except Exception: pass

ROOT = Path('.')

# ─────────────────────────────────────────────────────────────────
# Curated rewrites.  Each entry: slug → (NEW_TITLE, NEW_DESC).
#
# Style guide per category:
#   • Price/commercial → year + NT$ range + scare hook
#   • Educational      → question form + 「X分鐘看懂」
#   • Buyer journey    → question + 「避開X大踩雷」
#   • Brand           → 「XXX 評價」+ PTT/Dcard mention
# ─────────────────────────────────────────────────────────────────

REWRITES: dict[str, tuple[str, str]] = {
    # ═══ Price / commercial queries (highest CTR sensitivity) ═══

    'diamond-1ct-price-2026': (
        '1克拉鑽石價格 2026｜7萬到130萬，差 18 倍的真相',
        '一克拉鑽石市價落在 NT$7-130 萬，差距高達 18 倍。教你用 4C 拆解價格、避開「品牌溢價陷阱」，'
        '2026 年最新行情 + 線上免費試算。看完不再被當盤子。'
    ),
    'diamond-50-cents': (
        '20-50分鑽戒推薦 2026｜NT$8-25萬，避開4個品牌溢價陷阱',
        '20 分、30 分、50 分鑽戒到底差多少？台灣主流婚戒落在 0.2-0.5 克拉，售價 NT$8-25 萬。'
        '視覺尺寸對照、4C 最佳組合、踩雷品牌實名點名，2026 完整選購攻略。'
    ),
    'diamond-4cs-cheatsheet': (
        '鑽石 4C 是什麼？5 分鐘看懂顏色淨度切工克拉｜2026',
        '鑽石 4C = Color、Clarity、Cut、Carat。哪一 C 不能省？哪一 C 是賣家溢價陷阱？'
        '5 分鐘一篇看懂，附完整等級對照表 + 線上免費試算。'
    ),
    'diamond-color': (
        '鑽石顏色等級 D-Z 怎麼選？D 跟 G 真的看得出差別嗎',
        'GIA 鑽石顏色從 D（無色）到 Z（淺黃）共 23 級。D 與 G 肉眼真的有差？'
        '哪個等級才是 CP 值甜蜜點？D-VVS1 與 G-VVS1 價差實測。'
    ),
    'diamond-clarity': (
        '鑽石淨度等級 FL-I 怎麼看？VVS1 跟 VS1 肉眼有差嗎',
        'GIA 鑽石淨度從 FL（完全無瑕）到 I3（明顯瑕疵）共 11 級。VVS 比 VS 真的有差？'
        'SI1 還能買嗎？VS1-SI1 哪個才是 CP 值甜蜜點。'
    ),
    'diamond-carat-size': (
        '鑽石克拉視覺尺寸對照｜0.5、0.7、1克拉差多少 mm？',
        '鑽石「克拉」是重量，不是尺寸。0.5 克拉與 1 克拉的視覺直徑只差 1.3 mm，但價格差 5 倍。'
        '完整尺寸對照圖、戴在手上大小比較、不同形狀的克拉換算。'
    ),
    'diamond-shapes': (
        '10種鑽石形狀完整解析｜哪一款最顯大？選錯後悔10年',
        '圓形、橢圓、墊形、公主方、祖母綠… 10 種鑽石形狀完整圖解 + 顯大排行 + 領結效應與崩角風險。'
        '台灣最熱門 5 形狀比較。2026 完整指南。'
    ),

    # ═══ Buying journey (high-intent commercial) ═══

    'engagement-guide': (
        '求婚鑽戒怎麼挑 2026｜避開3大踩雷、9步驟完整流程',
        '從預算到求婚的 9 步驟完整 SOP — 台灣品牌實價、4C 最佳組合、求婚當天注意事項。'
        '避開 3 大常見踩雷：品牌溢價、假八心八箭、不肖證書。'
    ),
    'budget-formula': (
        '30萬以下挑最閃鑽石的數學公式｜NT$ 預算最佳化',
        '同樣 NT$30 萬，買對和買錯的鑽石光學分數差 25%。用 4Cs 拆數學算出 Tolkowsky 標準切磨，'
        '告訴你每一塊錢應該花在哪一 C。線上免費試算。'
    ),
    'master-guide': (
        '鑽石購買完整教學 2026｜從零到下單，1 篇看懂全部',
        '台灣鑽石市場最完整的 1 篇 — 4C、品牌、預算、GIA、求婚、保養全收錄。'
        '附 BPD 試算、Dcard/PTT 心得整理、台灣 14 大品牌實價對照。看完不再被當盤子。'
    ),
    'diamond-faq': (
        '鑽石購買 50 問 FAQ 2026｜4C、預算、品牌一次解答',
        '鑽石新手最常問的 50 個問題，從 4C、預算、品牌、培育鑽、認證、求婚、保養全部一次解答。'
        '每題都有完整答案不囉嗦，看完馬上動手。'
    ),
    'diamond-glossary': (
        '鑽石術語 30 個｜不懂這些就被當盤子｜2026 字典',
        '鑽石店員愛用的 30 個術語：Tolkowsky、八心八箭、螢光、領結效應、底尖… '
        '看了就懂、用了就會議價、不再被話術唬。線上免費試算搭配使用。'
    ),

    # ═══ Brand / scare-hook (where Dcard owns the SERP) ═══

    'taiwan-brands': (
        '台灣鑽戒品牌推薦 2026｜亞立詩 ALUXE、I-PRIMO 一次比',
        '台灣 14 大鑽戒品牌實價比較 — 亞立詩 ALUXE、I-PRIMO、銀座白石、Mabelle 點睛品、Just Diamond。'
        '哪家有品牌溢價？哪家 CP 值最高？2026 完整 PTT/Dcard 心得整理。'
    ),
    'dcard-ptt-recommendations': (
        '2026 Dcard PTT 鑽戒推薦排行榜｜30 篇真實心得整理',
        '整理 Dcard 與 PTT 婚戒板過去 1 年 30 篇真實心得 — 哪些品牌被罵翻？哪些網友推爆？'
        '亞立詩、I-PRIMO、Cartier、Just Diamond、銀座白石全部點評。'
    ),
    'diamond-scams': (
        '鑽石詐騙 TOP 10 避雷指南｜銀樓、網購、夜市黑名單',
        '台灣最常見 10 種鑽石詐騙手法 — 換石頭、假 GIA、改證書、夜市鋯石… '
        '附完整防騙 SOP、買前查證 5 步驟、被騙後 24 小時行動清單。'
    ),
    'diamond-resale': (
        '鑽石回收價真相｜為什麼 30 萬鑽戒只能換回 10 萬？',
        '鑽石零售價有 60-70% 是品牌溢價、店租、業務獎金。回收只值毛重，台灣 5 大回收通路實價對照、'
        '保值最差/最佳品牌、培育鑽幾乎無回收價的真相。'
    ),
    'diamond-financing': (
        '鑽戒分期付款指南｜0% 利率背後的隱藏成本拆解',
        '0 利率分期真的不用利息嗎？台灣銀行卡、店家分期、信用貸款、典當借款 5 種方案完整比較。'
        '附隱藏手續費換算、實質年利率試算。'
    ),
    'diamond-price-trends': (
        '鑽石價格趨勢 2026-2030 預測｜培育鑽崩盤、天然鑽分化',
        '2026-2030 鑽石市場 5 種情境分析 — De Beers 解體、印度切磨業裁員、培育鑽佔率突破 50%。'
        '現在買還是等？結婚預算什麼時候動最划算？'
    ),

    # ═══ Authority/educational ═══

    'gia-guide': (
        'GIA 鑑定書怎麼看？7 個必查欄位 + 線上驗證教學',
        'GIA 鑑定書到底要看哪幾欄才不會被騙？7 個必查欄位逐項解說、線上驗證連結、'
        '常見偽造手法 4 種辨識方法。5 分鐘成為證書達人。'
    ),
    'cert-comparison': (
        'GIA vs IGI vs HRD vs AGS｜哪一張證書最值得信？',
        '4 大鑽石證書實驗室嚴格度、價格、市佔率完整比較。培育鑽選 IGI、天然鑽選 GIA？'
        'AGS 跟 GIA 差在哪？哪些證書千萬別買。'
    ),
    'hearts-arrows-truth': (
        '八心八箭真相｜哪些 GIA Excellent 其實不及格？',
        '不是每顆 GIA 3EX 都是真八心八箭。Tolkowsky 1919 數學告訴你 Excellent 邊緣的鑽石漏光 25%。'
        '附 4 個關鍵比例 + 線上免費試算 + 八心八箭辨識教學。'
    ),
    'lab-vs-natural': (
        '培育鑽 vs 天然鑽 2026｜便宜 70% 的代價是什麼？',
        '培育鑽（Lab-grown）化學上 100% 是鑽石，價格只有天然鑽 30%。為什麼？'
        '光學差別、保值真相、台灣品牌、5 年後價格走勢、適合誰買的完整比較。'
    ),
    'fluorescence-deep-dive': (
        '鑽石螢光反應深度解析｜Strong 螢光便宜 15% 卻可能更白',
        '30% 鑽石有螢光反應，業界卻多數打折。GIA 1997 研究：99% 觀察者偏好螢光鑽。'
        '哪些顏色等級配 Medium 螢光最划算？避開的 3% 油膩風險。'
    ),
    'inclusions-types-guide': (
        '鑽石內含物 12 種完整圖解｜哪些可買、哪些一定避開',
        '不是每個 VS2 等級都一樣。檯面下的雲狀物比邊緣晶體更傷亮度。'
        '12 種內含物完整圖解、安全與危險的位置、買前必看 GIA 內含物圖。'
    ),
    'round-cut-deep-dive': (
        '圓形明亮車工深度解析｜為什麼 75% 鑽石都選這個',
        '58 個刻面、Tolkowsky 1919 黃金比例、AGS Ideal 規範詳解。'
        '為什麼圓形是鑽石的最大宗？4 個必查比例 + 線上免費試算。'
    ),
    'fancy-cuts-guide': (
        '花式車工完整指南｜橢圓、梨形、馬眼的領結效應與崩角風險',
        '橢圓、墊形、公主方、祖母綠、梨形、馬眼、雷地恩、阿斯切、心形 9 種完整對照。'
        '為什麼花式比圓形便宜 10-25%？哪些形狀崩角風險高？2026 完整指南。'
    ),

    # ═══ Care / market / niche ═══

    'diamond-care': (
        '鑽石保養 7 個習慣｜戴 30 年還像新的｜2026 教學',
        '鑽石不是無敵 — 衝擊會缺角、油垢會立刻暗 50%。沐浴、運動、煮飯前必脫的原因。'
        '7 個日常習慣、4 個禁忌、年度保養 4 件事。30 年保新攻略。'
    ),
    'diamond-fun-facts': (
        '鑽石 30 個冷知識｜從太空墜落到 9.99 億年的歷史',
        '鑽石會燃燒、土星會下鑽石雨、八心八箭來自 1919 MIT 論文、「鑽石恆久遠」是 1947 廣告詞。'
        '30 個你不知道的鑽石冷知識，閒聊話題滿滿。'
    ),
    'famous-diamonds': (
        '世界 10 大名鑽傳奇｜庫利南、霍普、Pink Star 完整百科',
        '從庫利南 3,106 克拉粗鑽到霍普藍鑽詛咒、Pink Star 71 億拍賣紀錄。'
        '10 大名鑽完整故事、現藏地點、估值。每位寶石學家都會背的歷史。'
    ),
    'gemstones-comparison': (
        '鑽石 vs 紅寶石 vs 藍寶石 vs 祖母綠｜4 大寶石訂婚戒比較',
        '寶石硬度、價格、適用場合完整對照。藍寶石（凱特王妃同款）只要鑽石 1/3 價、'
        '紅寶石比鑽石更貴的真相、祖母綠為什麼不適合日常配戴。'
    ),
    'sustainable-diamonds': (
        '道德鑽石完整指南｜血鑽石、Kimberley 流程、環保培育鑽',
        'Kimberley 流程真的能阻止血鑽石嗎？培育鑽真的環保嗎？4 種道德選項對比。'
        '加拿大鑽、回收鑽、培育鑽、Fairmined 黃金 5 個必問問題。'
    ),
    'diamond-photography': (
        '鑽石攝影完整指南｜手機拍出 IG 大放閃的 7 個技巧',
        '為什麼手機隨拍鑽石永遠暗一片？關鍵在「微距 + 點光源 + 暗背景 + 微傾錄影」。'
        '5 個拍攝設定 + 4 個後製禁忌，從此 IG 限動讓朋友以為你買了 5 克拉。'
    ),
    'moissanite-vs-cz-vs-lab': (
        '真假鑽辨識完整指南｜莫桑石、CZ、培育鑽、天然鑽 4 比',
        '硬度、火光、色散、價格、辨識方法 4 種寶石完整對照表。'
        '莫桑石為什麼比鑽石更閃？CZ 為什麼 2 年就霧化？培育鑽 = 鑽石的真相。'
    ),

    # ═══ Bands / ceremony / lifestyle ═══

    'wedding-bands': (
        '對戒挑選完整指南 2026｜訂婚戒 vs 結婚戒 vs 永恆戒怎麼分',
        '4 種戒指完整差別 — 哪一只戴左手？哪一只可以重設？永恆戒值不值得？'
        '台灣熱門品牌對戒款式 + 預算建議 + 寬度與材質配對。'
    ),
    'wedding-metals': (
        '婚戒材質完整比較｜白金 vs 18K 黃金 vs 玫瑰金 vs 鈀金',
        '5 種主流婚戒金屬完整對照 — 鉑金 (Pt950) 比 18K 白金貴 30% 值不值得？'
        '玫瑰金會褪色嗎？膚色配對、日常磨耗、長期維護成本一次解答。'
    ),
    'prong-settings-guide': (
        '鑽戒爪鑲完整指南｜6 爪、4 爪、包邊、暈鑲 7 種比較',
        '4 爪比 6 爪好看？包邊比較安全？爪型怎麼選最不易脫落？'
        '7 種戒台優缺點、適合的鑽石形狀、年度保養必做的 1 件事。'
    ),
    'engraving-personalization': (
        '婚戒刻字完整指南｜8 種字體、5 種文案、不褪色的 4 秘訣',
        '婚戒內側刻字花費 NT$500-2,000，是最低成本的個人化。'
        '中英文字體、字數限制、雷射 vs 手工差別、改尺寸後刻字會消失嗎？'
    ),
    'heirloom-redesign': (
        '傳家鑽石重新設計指南｜老一輩戒指如何升級成現代款',
        '繼承奶奶的鑽戒可以重新設計，保留鑽石換新戒台。'
        '完整流程：GIA 重檢、CAD 設計、爪鑲改造、預算 NT$15-40K。家族傳承 + 現代美感的解法。'
    ),
    'proposal-speech': (
        '求婚詞範本 50 句｜5 種風格 × 真情實感寫法',
        '60-90 秒的求婚詞分 3 段：為什麼是她、為什麼是現在、提問。'
        '50 句範本 + 5 種風格 + 3 個常見地雷 + 緊張時的 10 秒備案。'
    ),
    'engagement-timeline': (
        '訂婚到結婚 12 個月時間軸｜求婚到婚禮完整里程碑',
        '台灣平均訂婚到結婚 6-12 個月。場地 12 個月前訂、婚紗 5 個月前選、'
        '喜帖 3 個月前發。月份 × 任務完整時間軸 + 壓縮版（懷孕急婚）3 個月清單。'
    ),
    'dating-duration': (
        '交往多久可以求婚？12 國數據 + 6 個信號 + 3 個警訊',
        'Emory 大學研究：交往 3 年以上離婚率比交往 1 年低 50%。'
        '台灣 PTT/Dcard 平均 2-4 年。6 個求婚信號、3 個過早警訊、無關時間長短的 5 個紅燈。'
    ),
    'destination-wedding': (
        '異國婚禮鑽石採購｜峇里、京都、紐約、巴黎省 30%',
        '海外婚禮 = 蜜月 + 婚禮一起辦。NT$30-150 萬辦 20-50 人。'
        '6 大目的地實價、12-18 個月籌備清單、隱藏成本 5 種、台灣補請流程。'
    ),
    'lgbtq-rings': (
        '同志婚戒完整指南｜LGBTQ+ 訂婚戒選擇與求婚實戰',
        '台灣 2019 同婚合法後，LGBTQ+ 婚戒選購完全主流化。'
        '配對戒、不對稱戒、彩虹戒、彩色寶石 4 種風格 + 台灣友善品牌名單。'
    ),
    'mens-engagement-rings': (
        '男士求婚戒完整指南｜5 種風格、預算配方、配戴建議',
        '男戒已佔市場 25%。素環、包鑲、黑鑽、鹽胡椒鑽、印戒 5 種主流。'
        '鉑金 vs 鈦金 vs 鎢金 vs 鈦鎢比較、活躍工作者選戒指南。'
    ),
    'ring-sizing': (
        '戒指尺寸完整指南｜7 種無痕量法 + 台美日歐換算表',
        '台灣婚戒尺寸用港圍 1-30。新娘平均港圍 10-13。'
        '3 種家用量法、戴一天的尺寸變化、求婚驚喜該選哪號、寬戒要 +0.5 的原因。'
    ),
    'ring-insurance': (
        '婚戒保險與失竊處理｜4 種保險方案 + 24小時行動清單',
        'NT$30 萬婚戒年保費僅 NT$3-6K。家產保險附加 vs 獨立珠寶保險差在哪？'
        '掉入水溝、車裡被偷、手指縮水滑落 3 種理賠真實案例。'
    ),
    'secondhand-rings': (
        '二手婚戒購買指南｜省 50% 但別踩這 7 個雷',
        '二手鑽戒只要新品 40-60% — 同顆鑽、同證書、不同故事。'
        '5 步驟驗證 SOP、台灣 4 大購買通路實價、傳統忌諱與化解、文化敏感點解說。'
    ),

    # ═══ News / monthly reports (auto-generated, just polish title) ═══

    'diamond-news-2026': (
        '2026 鑽石市場新聞速報｜De Beers 大裁、培育鑽搶市',
        '2026 鑽石市場 5 大新聞 — De Beers 從 Anglo American 分割、印度切磨業萬人裁員、'
        '培育鑽佔美國訂婚市場 50%、中國買氣下滑、中東買家興起。'
    ),
    'diamond-news-2026-05': (
        '2026 年 5 月鑽石市場月報｜培育鑽、GIA、De Beers',
        '5 月 Google News 整理 — 培育鑽價格再跌 8%、GIA 新增認證類別、'
        'De Beers 庫存策略轉向、印度 Surat 切磨產能調整。'
    ),
    'diamond-vs-gold': (
        '鑽石 vs 黃金保值大比較｜30 年投報率與 5 個替代方案',
        '黃金 15 年年化報酬 ~7%、鑽石 ~3%。為什麼台灣人傳統買黃金存錢？'
        '保值、流動性、抗通膨完整對照 + 5 種其他選項（白銀、白金、鉑金、巴麗石）。'
    ),

    # ═══ Hubs (silo navigation) ═══

    'hub-fundamentals': (
        '鑽石基礎篇｜第一次買鑽石必讀 12 篇精選教學',
        '鑽石新手第一次必讀的 12 篇文章 — 4C、預算、品牌、認證、形狀、克拉、保養全收錄。'
        '從零到下單的完整教學序列。'
    ),
    'hub-4cs': (
        '鑽石 4Cs 完整拆解｜把每一塊錢花在最划算的等級',
        'Color、Clarity、Cut、Carat 4 大維度深度拆解。哪一 C 不能省？'
        '哪一 C 是業務溢價陷阱？10 篇深度文章一次看完。'
    ),
    'hub-purchase': (
        '鑽石購買實戰｜預算到下單的完整流程教學',
        '從預算規劃、品牌比較、Dcard PTT 心得、求婚 9 步驟、分期、保險到回收的完整實戰路徑。'
        '12 篇必看，避開所有踩雷。'
    ),
    'hub-proposal': (
        '求婚與婚戒指南｜從尺寸到求婚當天的 12 步',
        '求婚詞、婚戒尺寸、訂婚戒、結婚戒、永恆戒、對戒材質、刻字、傳家戒重設 12 篇完整指南。'
        '從計畫到求婚當天每一步。'
    ),
    'hub-care': (
        '鑽石保養與市場｜戴 30 年還像新的完整教學',
        '鑽石保養、攝影、保險、回收、保值、市場趨勢、培育鑽、道德採購 10 篇深度文章。'
        '婚後 30 年的鑽石生活完整指南。'
    ),
    'topics': (
        '鑽石主題索引｜44+ 篇文章 × 8 個主題完整地圖',
        '所有鑽石文章的主題式索引 — 4C、品牌、價格、求婚、保養、培育鑽、道德採購、市場趨勢 8 個分類。'
        '快速找到你要的那一篇。'
    ),
    'index': (
        '鑽石購買指南部落格｜44+ 篇實測教學完整目錄',
        'BrillianceLab 鑽石部落格 — 44+ 篇從 4C 到品牌的完整教學。'
        '台灣鑽戒實價、Dcard/PTT 心得、求婚攻略、線上免費試算。'
    ),
}


# ─────────────────────────────────────────────────────────────────
# Patcher
# ─────────────────────────────────────────────────────────────────

TITLE_RE = re.compile(r'<title>([\s\S]+?)</title>', re.I)
DESC_RE  = re.compile(r'(<meta\s+name=["\']description["\']\s+content=["\'])([^"\']+)(["\'])', re.I)
OGTITLE_RE = re.compile(r'(<meta\s+property=["\']og:title["\']\s+content=["\'])([^"\']+)(["\'])', re.I)
OGDESC_RE  = re.compile(r'(<meta\s+property=["\']og:description["\']\s+content=["\'])([^"\']+)(["\'])', re.I)
TWTITLE_RE = re.compile(r'(<meta\s+name=["\']twitter:title["\']\s+content=["\'])([^"\']+)(["\'])', re.I)
TWDESC_RE  = re.compile(r'(<meta\s+name=["\']twitter:description["\']\s+content=["\'])([^"\']+)(["\'])', re.I)

def patch(slug: str, new_title: str, new_desc: str) -> bool:
    p = ROOT / 'blog' / f'{slug}.html'
    if not p.exists():
        print(f'  miss: {slug}')
        return False
    src = p.read_text(encoding='utf-8')
    orig = src

    # 1. <title>
    src = TITLE_RE.sub(lambda m: f'<title>{new_title}</title>', src, count=1)

    # 2. meta description
    src = DESC_RE.sub(lambda m: f'{m.group(1)}{new_desc}{m.group(3)}', src, count=1)

    # 3. og:title — sync to new title
    src = OGTITLE_RE.sub(lambda m: f'{m.group(1)}{new_title}{m.group(3)}', src, count=1)

    # 4. og:description — sync to new description
    src = OGDESC_RE.sub(lambda m: f'{m.group(1)}{new_desc}{m.group(3)}', src, count=1)

    # 5. twitter:title — sync
    src = TWTITLE_RE.sub(lambda m: f'{m.group(1)}{new_title}{m.group(3)}', src, count=1)

    # 6. twitter:description — sync
    src = TWDESC_RE.sub(lambda m: f'{m.group(1)}{new_desc}{m.group(3)}', src, count=1)

    if src == orig:
        return False
    p.write_text(src, encoding='utf-8')
    return True


def main():
    n = 0
    skipped = 0
    for slug, (t, d) in REWRITES.items():
        if not t or 'skip' in slug:
            skipped += 1
            continue
        if patch(slug, t, d):
            tlen = sum(2 if '一' <= c <= '鿿' else 1 for c in t)
            dlen = sum(2 if '一' <= c <= '鿿' else 1 for c in d)
            mark = ''
            if tlen > 70: mark += ' !!T'
            if dlen > 160: mark += ' !!D'
            print(f'  rewrote {slug:<38}  T:{tlen:>3}  D:{dlen:>3}{mark}')
            n += 1
    print(f'\n{n} articles re-titled, {skipped} skipped')


if __name__ == '__main__':
    main()
