# -*- coding: utf-8 -*-
"""
Inject a 30-70-word TL;DR box right after the article H1.

Why: Google's featured snippet (Position 0) usually picks paragraphs in the
30-80 word range and prefers content near the page top. Voice search reads
the snippet as the answer. Owning the snippet for our top queries means
direct traffic + AI Overview citations.

Source TL;DR text comes from BUILD_TLDR_DATA below — hand-curated for the
20 highest-priority articles. Falls back to "auto-extract first sentence"
for the long tail.

Idempotent (sentinel: data-id="BL_TLDR").
"""
from __future__ import annotations
import re, sys
from pathlib import Path

# --- Auto-locate the repo root so this script can be run from anywhere ---
import os as _os
_os.chdir(Path(__file__).resolve().parents[2])  # → BrillianceLab/
# -------------------------------------------------------------------------

try: sys.stdout.reconfigure(encoding='utf-8')
except Exception: pass

ROOT = Path('.')
SENTINEL = 'data-id="BL_TLDR"'

# Hand-curated TL;DRs — these are the answers Google should quote. Each one is
# 50-70 Chinese characters (≈ 30-50 English words equivalent), the sweet spot
# for paragraph snippets.
TLDR = {
    'master-guide':
      '第一次買鑽石,先學 4Cs 中最關鍵的「車工」(占視覺 50% 以上),選 GIA Excellent 真八心八箭、'
      'G 色、VS2 淨度,搭配 BPD 公式(分數×√克拉÷價格)在預算內挑出最閃的一顆。本文用 14 階段帶你從決定預算走到求婚當天。',
    'gia-guide':
      'GIA 鑑定書 6 個欄位:4Cs(車工/顏色/淨度/克拉)、比例圖、Polish/Symmetry、Fluorescence、'
      '雷射編號、Plotting 內含物圖。Cut + Polish + Symmetry 全 Excellent + 真八心八箭才算「真 3EX」,光學差距可達 25%。',
    'hearts-arrows-truth':
      'GIA Excellent 涵蓋的比例範圍很廣 — 真八心八箭只占 Excellent 的 20%。用 Tolkowsky 1919 標準'
      '(亭角 40.8°、冠角 34.5°、桌面 55.5%)驗算,可篩出真正的 H&A,光學表現比邊緣 Excellent 強 25%。',
    'budget-formula':
      'BPD(Brilliance per Dollar)= 光學分數 × √克拉 ÷ (價格÷10K),數字越大越划算。30 萬預算下,'
      '0.85 克拉 E-VS2 真八心八箭的 BPD 比 1 克拉 G-VS1 邊緣 Excellent 高 39%,是更聰明的選擇。',
    'lab-vs-natural':
      '培育鑽石跟天然鑽石化學成分 100% 相同,GIA 用同一套 4C 標準鑑定。同等級下,培育鑽便宜約 70%'
      '(1 克拉 G-VS1 從 NT$30 萬降到 NT$8-10 萬)。但轉售價值較低,適合「買來戴」而非「買來保值」。',
    'diamond-color':
      '鑽石顏色 D-Z 共 23 階,D 最白、Z 最黃。實務上 D 跟 G 肉眼幾乎分不出,但價差 30-50%。'
      'G-H 是 CP 值甜蜜點:既看起來夠白,又省下大筆預算用來升級車工或克拉。',
    'diamond-clarity':
      '鑽石淨度 FL-I 共 11 階。VVS1 跟 VS1 肉眼絕對看不出差異,但價差 25-40%。VS2 是性價比甜蜜點 — '
      '10 倍放大才看得到內含物,日常配戴肉眼完全 clean,卻比 VVS 便宜近半。',
    'diamond-shapes':
      '圓形明亮車工最閃(57+1 面)且最保值,公主方第二閃,墊形溫柔復古,橢圓拉長手指顯瘦。'
      '第一次選建議圓形 — 光學表現可量化驗證,5 種主流形狀價差可達 25%。',
    'cert-comparison':
      '4 大實驗室嚴謹度:GIA(美,最嚴格,溢價 10-20%)> AGS(美,光學評分 0-10) > HRD(比利時,歐洲標準)> IGI(印度為主,寬鬆 1-2 級)。'
      '0.3 克拉以上強烈建議 GIA,小鑽 IGI 可接受。',
    'engagement-guide':
      '結婚鑽戒 9 步驟:① 決定預算(月薪 2-3 個月為常見區段) ② 偷量戒圍 ③ 選天然 vs 培育 ④ 4Cs 順序(切工>顏色>淨度>克拉) '
      '⑤ 看 GIA 證書 ⑥ 用 BrillianceLab 算分 ⑦ 選戒台 ⑧ 確認尺寸 ⑨ 求婚當天細節。',
    'diamond-faq':
      '50 個鑽石購買新手最常問的問題,涵蓋 4C、預算、品牌、培育鑽、求婚、保養、轉售 7 大主題。'
      '每題直接給答案,不囉嗦。看完就能直接下單,不用再 google。',
    'diamond-scams':
      '鑽石詐騙 TOP 10:① 假 GIA 證書 ② 莫桑石冒充 ③ 銀樓「自家保證書」 ④ 雷射編號不對 ⑤ Excellent 邊緣值 ⑥ 螢光隱瞞 '
      '⑦ 二手翻新 ⑧ 夜市超低價 ⑨ 海外免稅店 ⑩ 網購無退換。9 步驗鑽流程完整避雷。',
    'moissanite-vs-cz-vs-lab':
      '4 種「鑽石」辨識:天然鑽 = CP 值低保值高;培育鑽 = 光學一樣便宜 70%;莫桑石 = 折射率更高更閃但易刮;CZ = 玻璃替代品 1 年就霧。'
      '哈氣測試 + 折射筆 + 證書 3 招辨真假。',
    'diamond-care':
      '鑽石保養 7 個習慣:洗碗、運動、塗防曬前先取下;每月用稀釋洗碗精+牙刷清潔;每年送專業檢查爪鑲;'
      '存放分隔絨布盒避免互刮;游泳前必脫;氯與汗水損鉑金。戴 30 年還像新的關鍵。',
    'ring-insurance':
      '婚戒保險 4 種方案:① 居家保險附加(便宜但理賠麻煩) ② 珠寶專案(理賠快保額足) '
      '③ 國際保險(出國旅遊) ④ 自購保管箱(省保費)。失竊 24h SOP:報警→保險公司→GIA 雷射編號掛失。',
    'diamond-resale':
      '30 萬鑽戒只能換回 10 萬?品牌溢價、零售毛利、市場流動性是 3 大殺價因素。GIA 認證鑽石 7 折回購;'
      '無證書只剩 3-5 折;品牌戒台幾乎歸零(只剩鑽石本身)。培育鑽轉售更慘。',
    'wedding-bands':
      '5 種戒指完整指南:訂婚戒(主鑽)、結婚對戒(對應彼此)、永恆戒(滿圈鑽)、紀念戒(週年送)、堆疊戒(混搭多枚)。'
      '日韓多採一戒制,歐美多採訂婚+結婚雙戒。',
    'wedding-metals':
      '6 種婚戒材質:鉑金(最保值但軟)、18K 白金(實用但需要重鍍)、玫瑰金(溫柔顯白)、'
      '黃金(亞洲市場最保值)、鈀金(輕便)、鈦/鎢鋼(便宜但無法調尺寸)。鉑金與 18K 是主流。',
    'ring-sizing':
      '7 種偷量戒圍法:① 借她現有戒指描內圈 ② 線繞中指(中指比無名指大 0.5 號) ③ 印手照 ④ 問閨蜜 ⑤ 假裝逛逛試戴 '
      '⑥ 預設台灣女生平均 11.5 號 ⑦ 線上 PDF 量尺。15 分鐘搞定。',
    'proposal-speech':
      '50 句求婚詞範本,涵蓋 5 大場景:浪漫海邊、家中驚喜、餐廳告白、復古信件、影片回顧。每句字數適中(20-40 字),'
      '具體說出「為什麼是她」3 個理由比通用情話打動人 10 倍。',
}


def serp_chars(s: str) -> int:
    """CJK chars count as 2 in Google snippet width."""
    cjk = len(re.findall(r'[㐀-鿿]', s))
    return cjk * 2 + (len(s) - cjk)


def render_box(text: str) -> str:
    return (
        '\n  <aside ' + SENTINEL + ' class="bl-tldr"'
        ' style="margin:0 0 22px;padding:16px 20px;background:linear-gradient(180deg,#fffdf7,#fbf3df);'
        'border-left:4px solid #c9a45c;border-radius:8px;font-size:14.5px;line-height:1.85;color:#1a1d2e">'
        '<div style="font-size:10.5px;letter-spacing:.22em;text-transform:uppercase;color:#8a6e30;'
        'font-weight:700;margin-bottom:6px">TL;DR · 一分鐘掌握</div>'
        + text +
        '</aside>'
    )


def patch(p: Path, slug: str) -> bool:
    src = p.read_text(encoding='utf-8')
    if SENTINEL in src:
        return False
    text = TLDR.get(slug)
    if not text:
        # Fallback: auto-extract first sentence of the article
        m = re.search(
            r'(?:id=["\']proseZh["\']|class=["\'][^"\']*\bprose-zh\b[^"\']*["\'])'
            r'[^>]*>[\s\S]+?<p\b[^>]*>([\s\S]+?)</p>', src, re.I)
        if not m: return False
        clean = re.sub(r'<[^>]+>', '', m.group(1)).strip()
        # Take 1-2 sentences, trim to ~60 chars
        sents = re.split(r'(?<=[。!?])', clean)
        text = ''
        for s in sents:
            if serp_chars(text + s) > 130: break
            text += s
        if not text: return False
    if serp_chars(text) > 160:
        # Truncate at last 「。」 before 150 chars
        running = 0; cut = 0
        for i, c in enumerate(text):
            running += 2 if re.match(r'[㐀-鿿]', c) else 1
            if running > 150: break
            if c == '。': cut = i + 1
        if cut > 50: text = text[:cut]

    box = render_box(text)
    # Insert AFTER the first </h1>
    new = re.sub(r'(</h1>)', r'\1' + box, src, count=1)
    if new == src: return False
    p.write_text(new, encoding='utf-8')
    return True


def main():
    n_curated = 0; n_auto = 0
    for p in sorted(ROOT.glob('blog/*.html')):
        slug = p.stem
        if slug in ('index', 'topics', 'feed'): continue
        if slug.startswith('hub-'): continue
        before = SENTINEL in p.read_text(encoding='utf-8')
        if patch(p, slug):
            if slug in TLDR: n_curated += 1
            else: n_auto += 1
            print(f'  TL;DR → {p.name}  ({"curated" if slug in TLDR else "auto"})')
    print(f'\n{n_curated} curated + {n_auto} auto-extracted = {n_curated + n_auto} TL;DR boxes injected')


if __name__ == '__main__':
    main()
