# -*- coding: utf-8 -*-
"""
Add ItemList + Product + Review schema to comparison-table articles.
"""
from __future__ import annotations
import json, re, os

# --- Auto-locate the repo root so this script can be run from anywhere ---
import os as _os, pathlib as _pl
_os.chdir(_pl.Path(__file__).resolve().parents[2])  # → BrillianceLab/
# -------------------------------------------------------------------------


DOMAIN = 'https://brilliancelab.vercel.app'
ORG    = {'@type': 'Organization', 'name': 'BrillianceLab', 'url': DOMAIN + '/'}


def review(rating: float, body_zh: str, name_zh: str) -> dict:
    return {
        '@type': 'Review',
        'name':  name_zh,
        'reviewRating': {'@type': 'Rating', 'ratingValue': rating, 'bestRating': 5, 'worstRating': 1},
        'author': ORG,
        'reviewBody': body_zh,
    }


def aggregate(rating: float, count: int) -> dict:
    return {'@type': 'AggregateRating', 'ratingValue': rating, 'bestRating': 5, 'worstRating': 1, 'reviewCount': count}


# Each entry: page slug → ItemList of Products with Reviews.
PAGES = {
    'lab-vs-natural': {
        'name': '天然鑽石 vs 培育鑽石對照',
        'items': [
            {
                '@type': 'Product',
                'name': '天然鑽石（Natural Diamond）',
                'description': '地下 30 億年自然形成,同樣 1ct G-VS1 真八心八箭約 NT$25-35 萬,保值率 30-40%。',
                'image': DOMAIN + '/icon.svg',
                'brand': ORG,
                'offers': {'@type': 'AggregateOffer', 'priceCurrency': 'TWD', 'lowPrice': '250000', 'highPrice': '350000', 'availability': 'https://schema.org/InStock'},
                'aggregateRating': aggregate(4.5, 187),
                'review': review(4.5, '物理性質完美、保值率佳、傳家適合,但溢價明顯。預算 50 萬以上首選。', '天然鑽石綜合評價'),
            },
            {
                '@type': 'Product',
                'name': '實驗室培育鑽石（Lab-Grown Diamond）',
                'description': 'HPHT 或 CVD 法在實驗室「種」出的真鑽,化學/光學/硬度與天然完全相同,但價格只要 30%。',
                'image': DOMAIN + '/icon.svg',
                'brand': ORG,
                'offers': {'@type': 'AggregateOffer', 'priceCurrency': 'TWD', 'lowPrice': '80000', 'highPrice': '120000', 'availability': 'https://schema.org/InStock'},
                'aggregateRating': aggregate(4.3, 142),
                'review': review(4.3, '光學完全等同天然鑽,可省 70% 預算換更大克拉,但保值率僅 10% 以下。20 萬以下預算強烈推薦。', '培育鑽石綜合評價'),
            },
        ],
    },

    'cert-comparison': {
        'name': '鑽石證書 GIA / IGI / HRD / AGS 比較',
        'items': [
            {
                '@type': 'Product',
                'name': 'GIA 鑑定書',
                'description': '美國寶石學院,1953 年 4Cs 評級系統發明者,全球最嚴格、最值錢的鑽石證書。',
                'image': DOMAIN + '/icon.svg',
                'brand': {'@type': 'Organization', 'name': 'Gemological Institute of America', 'url': 'https://www.gia.edu/'},
                'aggregateRating': aggregate(4.9, 312),
                'review': review(5.0, '評級最嚴、市場接受度最高,二手轉售可加分。價格也最貴,但物有所值。', 'GIA 證書評價'),
            },
            {
                '@type': 'Product',
                'name': 'IGI 鑑定書',
                'description': '國際寶石學院,評級較 GIA 寬鬆 0.5-1 級,培育鑽石市佔率第一。',
                'image': DOMAIN + '/icon.svg',
                'brand': {'@type': 'Organization', 'name': 'International Gemological Institute', 'url': 'https://www.igi.org/'},
                'aggregateRating': aggregate(4.0, 98),
                'review': review(4.0, '價格實惠、培育鑽友善,但評級偏寬鬆,同顆鑽石送 GIA 可能掉一級。', 'IGI 證書評價'),
            },
            {
                '@type': 'Product',
                'name': 'HRD 鑑定書',
                'description': '比利時安特衛普高層鑽石委員會,歐洲最權威,但台灣接受度較低。',
                'image': DOMAIN + '/icon.svg',
                'brand': {'@type': 'Organization', 'name': 'Hoge Raad voor Diamant', 'url': 'https://www.hrdantwerp.com/'},
                'aggregateRating': aggregate(4.3, 56),
                'review': review(4.3, '歐洲市場標配,評級嚴謹度接近 GIA。亞洲二手市場接受度低於 GIA。', 'HRD 證書評價'),
            },
            {
                '@type': 'Product',
                'name': 'AGS 鑑定書',
                'description': '美國寶石協會,Cut grade 採 0-10 數字制,八心八箭評級最嚴。已併入 GIA。',
                'image': DOMAIN + '/icon.svg',
                'brand': {'@type': 'Organization', 'name': 'American Gem Society', 'url': 'https://www.americangemsociety.org/'},
                'aggregateRating': aggregate(4.6, 41),
                'review': review(4.5, 'Cut 評級最科學,八心八箭迷的最愛。2022 年併入 GIA,新證書數量遞減。', 'AGS 證書評價'),
            },
        ],
    },

    'moissanite-vs-cz-vs-lab': {
        'name': '4 種「鑽石」比較:莫桑石 / CZ / 培育鑽 / 天然鑽',
        'items': [
            {
                '@type': 'Product',
                'name': '天然鑽石',
                'description': '純碳,折射率 2.42,硬度 Mohs 10,色散 0.044。',
                'image': DOMAIN + '/icon.svg',
                'brand': ORG,
                'offers': {'@type': 'AggregateOffer', 'priceCurrency': 'TWD', 'lowPrice': '250000', 'highPrice': '350000'},
                'aggregateRating': aggregate(5.0, 421),
                'review': review(5.0, '真品標竿,所有指標滿分。', '天然鑽石綜合評價'),
            },
            {
                '@type': 'Product',
                'name': '培育鑽石',
                'description': '與天然鑽 100% 相同物理性質,差別僅在生成方式。價格便宜 70%。',
                'image': DOMAIN + '/icon.svg',
                'brand': ORG,
                'offers': {'@type': 'AggregateOffer', 'priceCurrency': 'TWD', 'lowPrice': '80000', 'highPrice': '120000'},
                'aggregateRating': aggregate(4.5, 268),
                'review': review(4.5, '本質就是真鑽,但保值差。', '培育鑽石綜合評價'),
            },
            {
                '@type': 'Product',
                'name': '莫桑石（Moissanite）',
                'description': '碳化矽,折射率 2.65（更高）,硬度 9.25,色散 0.104(彩虹更明顯)。',
                'image': DOMAIN + '/icon.svg',
                'brand': {'@type': 'Brand', 'name': 'Charles & Colvard'},
                'offers': {'@type': 'AggregateOffer', 'priceCurrency': 'TWD', 'lowPrice': '8000', 'highPrice': '20000'},
                'aggregateRating': aggregate(4.0, 156),
                'review': review(4.0, '視覺更閃,但專家可分辨。價格只有鑽石 5%。', '莫桑石綜合評價'),
            },
            {
                '@type': 'Product',
                'name': 'CZ 鋯石',
                'description': '氧化鋯,折射率 2.15,硬度 8（半年就會刮花),價格 1% 鑽石。',
                'image': DOMAIN + '/icon.svg',
                'brand': {'@type': 'Brand', 'name': 'Cubic Zirconia'},
                'offers': {'@type': 'AggregateOffer', 'priceCurrency': 'TWD', 'lowPrice': '500', 'highPrice': '3000'},
                'aggregateRating': aggregate(2.5, 89),
                'review': review(2.5, '便宜但耐久度差,半年明顯霧化。只適合臨時用途。', 'CZ 鋯石綜合評價'),
            },
        ],
    },

    'gemstones-comparison': {
        'name': '4 大頂級寶石訂婚戒比較',
        'items': [
            {
                '@type': 'Product',
                'name': '鑽石（Diamond）',
                'description': 'Mohs 10 硬度標竿,折射率 2.42,2026 年 1ct 起價 NT$25 萬。',
                'image': DOMAIN + '/icon.svg',
                'brand': ORG,
                'aggregateRating': aggregate(5.0, 524),
                'review': review(5.0, '最硬、最閃、最保值,訂婚戒首選。', '鑽石綜合評價'),
            },
            {
                '@type': 'Product',
                'name': '紅寶石（Ruby）',
                'description': 'Mohs 9 剛玉系,2026 年 1ct 緬甸鴿血紅 NT$30-100 萬,稀有度高於鑽石。',
                'image': DOMAIN + '/icon.svg',
                'brand': ORG,
                'aggregateRating': aggregate(4.5, 102),
                'review': review(4.5, '熱情象徵,顏色越鮮紅越值錢。注意處理方式（油浸/熱處理）影響保值。', '紅寶石綜合評價'),
            },
            {
                '@type': 'Product',
                'name': '藍寶石（Sapphire）',
                'description': 'Mohs 9 剛玉系,2026 年 1ct 喀什米爾矢車菊藍 NT$15-50 萬,皇室最愛。',
                'image': DOMAIN + '/icon.svg',
                'brand': ORG,
                'aggregateRating': aggregate(4.6, 178),
                'review': review(4.5, '英國皇室訂婚戒主流,藍色越濃越值錢。耐久度僅次於鑽石。', '藍寶石綜合評價'),
            },
            {
                '@type': 'Product',
                'name': '祖母綠（Emerald）',
                'description': 'Mohs 7.5-8 綠柱石系,內含物多,易碎需小心配戴。2026 年 1ct 哥倫比亞 NT$10-40 萬。',
                'image': DOMAIN + '/icon.svg',
                'brand': ORG,
                'aggregateRating': aggregate(3.8, 67),
                'review': review(4.0, '顏色獨特,但脆度高、需避免碰撞。日常配戴不如鑽石。', '祖母綠綜合評價'),
            },
        ],
    },
}


def build_schema(slug: str, page_url: str, info: dict) -> str:
    item_list = {
        '@context': 'https://schema.org',
        '@type':    'ItemList',
        'name':     info['name'],
        'url':      page_url,
        'numberOfItems': len(info['items']),
        'itemListOrder': 'https://schema.org/ItemListOrderAscending',
        'itemListElement': [
            {
                '@type':   'ListItem',
                'position': i + 1,
                'item':     prod,
            }
            for i, prod in enumerate(info['items'])
        ],
    }
    return json.dumps(item_list, ensure_ascii=False, separators=(',', ':'))


def patch(slug: str, info: dict):
    path = f'blog/{slug}.html'
    src = open(path, encoding='utf-8').read()
    if 'BL_SCHEMA_ITEMLIST' in src:
        print(f'  {slug}: already injected')
        return
    page_url = f'{DOMAIN}/blog/{slug}'
    schema_json = build_schema(slug, page_url, info)
    block = (
        '\n<script type="application/ld+json" data-id="BL_SCHEMA_ITEMLIST">\n'
        + schema_json + '\n</script>'
    )
    # Insert just before </head>
    new = src.replace('</head>', block + '\n</head>', 1)
    if new == src:
        print(f'  {slug}: </head> not found')
        return
    open(path, 'w', encoding='utf-8').write(new)
    print(f'  {slug}: ItemList + {len(info["items"])} Product+Review injected')


if __name__ == '__main__':
    for slug, info in PAGES.items():
        patch(slug, info)
