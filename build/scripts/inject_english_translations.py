# -*- coding: utf-8 -*-
"""
Inject professional English translations as #proseEn blocks alongside the
existing Chinese content. Each translation is hand-written (not literal) for
SEO impact in English-speaking markets.

The English block is hidden by default (display:none / .hidden) so the
existing JS language toggle (BL.applyTextOnly + initBlog opts.proseEn) shows
it only when the user picks an English-family language.

Idempotent: keyed off `data-id="BL_PROSE_EN"`. Re-run safely refreshes content.

Round 13 batch: 10 articles
  - master-guide / diamond-4cs-cheatsheet / diamond-1ct-price-2026
  - diamond-50-cents / taiwan-brands / dcard-ptt-recommendations
  - diamond-glossary / proposal-vs-wedding-vs-eternity
  - diamond-faq / gia-guide
"""
from __future__ import annotations
import re, sys
from pathlib import Path

# --- Auto-locate the repo root ---
import os as _os
_os.chdir(Path(__file__).resolve().parents[2])  # → BrillianceLab/

try: sys.stdout.reconfigure(encoding='utf-8')
except Exception: pass

ROOT = Path('.')
SENTINEL = 'data-id="BL_PROSE_EN"'

# Helper to wrap content as a hidden English prose block
def wrap_en(html: str, slug: str) -> str:
    return (
        '\n<div id="proseEn" class="prose-en hidden" ' + SENTINEL + ' '
        + 'data-pagefind-body data-pagefind-meta="slug:' + slug + '_en" '
        + 'lang="en" style="display:none">\n' + html + '\n</div>\n'
    )


# ─────────────────────────────────────────────────────────────────
# 10 articles — full English translations
# ─────────────────────────────────────────────────────────────────

EN = {}

# 1. master-guide
EN['master-guide'] = '''
<aside style="margin:0 0 22px;padding:16px 20px;background:linear-gradient(180deg,#fffdf7,#fbf3df);border-left:4px solid #c9a45c;border-radius:8px">
  <div style="font-size:10.5px;letter-spacing:.22em;text-transform:uppercase;color:#8a6e30;font-weight:700;margin-bottom:6px">TL;DR · 1-minute summary</div>
  Buying your first diamond? Most online guides repeat sales scripts. This one
  verifies every claim with math: D vs G is invisible, edge-Excellent loses
  25% to true Hearts &amp; Arrows, brand premium can hit 4×. Every conclusion
  is reproducible with the BrillianceLab calculator. Covers the full path from
  GIA report → 4Cs → budget formula → brand comparison → ring shopping → proposal day.
</aside>

<h2>Why this guide?</h2>
<p>Other diamond guides on the web push sales narratives: "Excellent is the top",
"D is the only true white", "brand value preserves resale". <strong>This guide uses
math to verify each claim</strong>: you cannot tell D from G face-up; edge-of-grade
Excellent rings 25% duller than true Hearts &amp; Arrows; brand premium can reach
4× the loose-stone price. Every conclusion below has a calculator behind it.</p>

<h2>The 14-stage roadmap</h2>
<p>The buying process is split into 14 stages. Each links to a deep-dive article
you can drill into independently:</p>
<ol style="line-height:2">
  <li><a href="/blog/gia-guide">How to read a GIA report</a> — the 4Cs, proportions, polish/symmetry/fluorescence.</li>
  <li><a href="/blog/hearts-arrows-truth">The Hearts &amp; Arrows truth</a> — which Excellents fail with math (Tolkowsky verification).</li>
  <li><a href="/blog/budget-formula">The BPD budget formula</a> — score × √carat ÷ price under NT$300K.</li>
  <li><a href="/blog/lab-vs-natural">Natural vs lab-grown</a> — same optics, 70% cheaper.</li>
  <li><a href="/blog/diamond-color">Color D-Z</a> — G is the value sweet spot.</li>
  <li><a href="/blog/diamond-clarity">Clarity FL-I</a> — VS2 is the practical floor.</li>
  <li><a href="/blog/diamond-carat-size">Carat vs face-up size</a> — 0.5 / 0.7 / 1ct in mm.</li>
  <li><a href="/blog/diamond-shapes">10 diamond shapes</a> — round, oval, cushion, princess, emerald.</li>
  <li><a href="/blog/cert-comparison">GIA vs IGI vs HRD</a> — lab strictness, price, market share.</li>
  <li><a href="/blog/engagement-guide">Engagement ring 9 steps</a> — budget to proposal-day flow.</li>
  <li><a href="/blog/diamond-scams">Top 10 diamond scams</a> — jewellers, online, night markets.</li>
  <li><a href="/blog/diamond-care">Diamond care</a> — 7 habits to keep it new for 30 years.</li>
  <li><a href="/blog/diamond-resale">Resale truth</a> — why a NT$300K ring trades back at NT$100K.</li>
  <li><a href="/blog/diamond-news-2026">2026 market news</a> — De Beers split, India layoffs, lab-grown 50%.</li>
</ol>

<h2>The shortest path</h2>
<p>If you only want one answer: <strong>budget NT$25-35K and pick 1.0 ct G-VS2 true
Hearts &amp; Arrows GIA 3EX</strong>. Cut is the only "C" you cannot compromise; the
others (color, clarity, even carat by 5%) can give to extend the budget.
Read <a href="/blog/diamond-4cs-cheatsheet">the 4Cs cheatsheet</a> for the
single-page version of the math.</p>

<h2>What's after the 14 articles?</h2>
<p>The site has ~50 articles total organised into 5 silos
(<a href="/blog/hub-fundamentals">Fundamentals</a> ·
<a href="/blog/hub-4cs">4Cs deep dives</a> ·
<a href="/blog/hub-purchase">Purchase tactics</a> ·
<a href="/blog/hub-proposal">Proposal &amp; bands</a> ·
<a href="/blog/hub-care">Care &amp; market</a>). Once you've absorbed the 14 above,
each silo hub gives you the next reading order tailored to your interest.</p>

<h2>Use the calculator</h2>
<p>The point of all this content is to feed clean inputs into the
<a href="/">BrillianceLab calculator</a>. Drop in four numbers from any GIA
report (table %, depth %, crown angle, pavilion angle) and you get a
0-100 optical score plus a 4-dim breakdown (Light Return / Fire / Scintillation
/ Spread). Same NT$300K, optical scores can differ by 12-15 points — that's
the difference between buying and not buying.</p>
'''

# 2. diamond-4cs-cheatsheet
EN['diamond-4cs-cheatsheet'] = '''
<aside style="margin:0 0 22px;padding:16px 20px;background:linear-gradient(180deg,#fffdf7,#fbf3df);border-left:4px solid #c9a45c;border-radius:8px">
  <div style="font-size:10.5px;letter-spacing:.22em;text-transform:uppercase;color:#8a6e30;font-weight:700;margin-bottom:6px">TL;DR</div>
  The 4Cs are the GIA 1953 grading standard: <strong>Cut, Color, Clarity, Carat</strong>.
  <strong>Cut matters more than the other three combined</strong> (50%+ of the visual).
  Sweet-spot combo for ~NT$300K: <strong>1ct / G color / VS2 / true H&amp;A GIA 3EX</strong>.
  Drop color or clarity — eyes can't tell. Drop cut — eyes can.
</aside>

<h2>The 4Cs in one sentence each</h2>
<table>
  <thead><tr><th>C</th><th>One-line verdict</th><th>Sweet spot</th></tr></thead>
  <tbody>
    <tr><td><strong>Cut</strong></td><td>50% of the visual; never compromise</td><td>True H&amp;A, GIA 3EX</td></tr>
    <tr><td><strong>Color</strong></td><td>D vs G is invisible face-up; price gap 30%</td><td>G or H</td></tr>
    <tr><td><strong>Clarity</strong></td><td>VS1 vs VS2 looks identical; VS2 is 20% cheaper</td><td>VS2 (or VS1)</td></tr>
    <tr><td><strong>Carat</strong></td><td>0.99 vs 1.00 ct = 0.04mm; price gap 20%</td><td>0.9-1.0 ct</td></tr>
  </tbody>
</table>

<h2>① Cut — 50%+ of the visual</h2>
<p>GIA cut grades: Excellent / Very Good / Good / Fair / Poor. <strong>But "Excellent"
is a wide bucket</strong> — only ~20% of GIA Excellents are true Hearts &amp; Arrows.
Always ask the jeweller for an H&amp;A viewer. Look down: you should see 8 hearts.
Look up: 8 arrows.</p>
<p>Deep dive: <a href="/blog/hearts-arrows-truth">Hearts &amp; Arrows truth</a> ·
<a href="/blog/round-cut-deep-dive">Round brilliant cut deep-dive</a></p>

<h2>② Color — G to H is the value zone</h2>
<p>D-Z grade scale, D = colorless. Most pairs of grades are indistinguishable to the
naked eye:</p>
<ul>
  <li><strong>D-F (colorless)</strong> — paper-grade, expensive. Skip unless budget &gt; NT$500K.</li>
  <li><strong>G-J (near colorless)</strong> — visual-grade, eye-clean.</li>
  <li><strong>K-M (faint yellow)</strong> — works in rose gold, not in white metals.</li>
</ul>

<h2>③ Clarity — VS2 is the floor</h2>
<p>FL to I3 is 11 grades. Practical guidance:</p>
<ul>
  <li><strong>FL / IF</strong> — collector-grade. 99% of buyers don't need it.</li>
  <li><strong>VVS1 / VVS2</strong> — 10× loupe to see anything. No visual return on the spend.</li>
  <li><strong>VS1 / VS2</strong> — eye-clean, 10× shows medium inclusion. <strong>The sweet spot.</strong></li>
  <li><strong>SI1 / SI2</strong> — usually still eye-clean. SI1 OK; SI2 depends on inclusion location.</li>
</ul>

<h2>④ Carat — the threshold-effect trap</h2>
<p>1.00, 1.50, 2.00 ct command 15-25% premiums purely because of round-number marketing.
<strong>0.9-0.98 ct is the "almost 1ct" hack</strong> — visually identical, materially cheaper.</p>

<h2>BPD: turning 4Cs into one number</h2>
<p style="background:#fbf3df;padding:14px 18px;border-radius:8px;text-align:center;font-weight:700;color:#5e4a1f">
  BPD = Optical Score × √Carat ÷ (Price ÷ 10,000)
</p>
<p>Higher = better value. Real example with NT$300K:</p>
<table>
  <thead><tr><th>Option</th><th>Specs</th><th>Price</th><th>BPD</th></tr></thead>
  <tbody>
    <tr><td>A</td><td>1.00 G-VS1, edge Excellent</td><td>NT$300K</td><td>30.0</td></tr>
    <tr><td>B</td><td>0.85 E-VS2, true H&amp;A</td><td>NT$280K</td><td><strong>41.7 ⭐</strong></td></tr>
    <tr><td>C</td><td>1.20 G-SI1, edge Excellent</td><td>NT$320K</td><td>34.5</td></tr>
  </tbody>
</table>
<p>Option B (smaller carat, top cut) wins by 21%. <strong>That's the value of true H&amp;A.</strong></p>

<h2>FAQ</h2>
<h3>Q: Which C matters most?</h3>
<p>Cut. It's the only one humans control 100%, drives 50%+ of perceived sparkle,
and dropping one cut grade costs 30-40% of price.</p>
<h3>Q: Do I really need GIA?</h3>
<p>For 0.3ct+ yes. Without GIA, resale value drops to 50-70%, and insurance won't
underwrite. <a href="/blog/cert-comparison">GIA vs IGI vs HRD vs AGS</a>.</p>
<h3>Q: NT$150K budget — what 4C?</h3>
<p>0.5 ct G-VS2 true H&amp;A. Or skip to <a href="/blog/lab-vs-natural">lab-grown</a>
and get 1.0 ct G-VS2 H&amp;A for the same money.</p>
'''

# 3. diamond-1ct-price-2026
EN['diamond-1ct-price-2026'] = '''
<aside style="margin:0 0 22px;padding:16px 20px;background:linear-gradient(180deg,#fffdf7,#fbf3df);border-left:4px solid #c9a45c;border-radius:8px">
  <div style="font-size:10.5px;letter-spacing:.22em;text-transform:uppercase;color:#8a6e30;font-weight:700;margin-bottom:6px">TL;DR</div>
  2026 prices for 1 ct G-VS1 with same GIA cert can range from
  <strong>NT$70K (lab-grown) to NT$1.3M (Cartier)</strong> — an 18× spread.
  The differences are: brand premium (50-70% for luxury), retail margin (15-20%),
  and origin (lab-grown vs natural). The diamond itself is rarely the biggest cost.
</aside>

<h2>Same diamond, different price by channel</h2>
<table>
  <thead><tr><th>Channel</th><th>Brands</th><th>NT$ range</th><th>Premium source</th></tr></thead>
  <tbody>
    <tr><td>Lab-grown</td><td>Direct labs / TW chains</td><td>70K - 120K</td><td>None — CVD/HPHT mass-produced</td></tr>
    <tr><td>US online</td><td>Blue Nile / James Allen / Whiteflash</td><td>130K - 250K</td><td>Almost zero + 5-8% import duty</td></tr>
    <tr><td>TW workshop</td><td>BUERHKAU 不二鑽石</td><td>180K - 280K</td><td>Stone + thin margin</td></tr>
    <tr><td>TW chain</td><td>Mabelle 點睛品 / ALUXE / Promessa</td><td>180K - 320K</td><td>+ 10-20% service / setting</td></tr>
    <tr><td>JP wedding</td><td>I-PRIMO / Ginza Shiraishi</td><td>250K - 450K</td><td>+ 20-30% strict cut + brand</td></tr>
    <tr><td>EU designer</td><td>Bulgari / Van Cleef / Chaumet</td><td>450K - 750K</td><td>+ 30-50% design + craft</td></tr>
    <tr><td>Luxury house</td><td>Cartier / Tiffany / Harry Winston</td><td>700K - 1.3M</td><td>+ 50-70% brand</td></tr>
  </tbody>
</table>

<h2>4Cs price elasticity</h2>
<p>Starting baseline: 1ct G-VS1 at NT$250K (TW chain). Change one C:</p>
<table>
  <thead><tr><th>Change</th><th>New grade</th><th>Price delta</th><th>Visual delta</th></tr></thead>
  <tbody>
    <tr><td>Carat ↓</td><td>0.90 ct</td><td>-25-30%</td><td>0.2mm diameter — invisible</td></tr>
    <tr><td>Color ↑</td><td>D</td><td>+30-50%</td><td>Visible only on white paper</td></tr>
    <tr><td>Color ↓</td><td>I</td><td>-20-30%</td><td>Indistinguishable on the hand</td></tr>
    <tr><td>Clarity ↑</td><td>VVS1</td><td>+25-40%</td><td>Loupe-only</td></tr>
    <tr><td>Clarity ↓</td><td>SI1</td><td>-20-30%</td><td>Often still eye-clean</td></tr>
    <tr><td>Cut ↓</td><td>edge Excellent</td><td>-15-20%</td><td><strong>25% less fire — visible</strong></td></tr>
  </tbody>
</table>
<p><strong>Takeaway:</strong> drop color or clarity to save money. Never drop cut.</p>

<h2>FAQ</h2>
<h3>Q: Why is Cartier 4× point's price for the same GIA cert?</h3>
<p>Cartier's cost stack: 30-35% stone, 10-15% setting craft, 15-20% rent,
10-15% advertising, 25-40% brand markup. TW chain: ~60% / 12% / 8% / 5% / 15%.
<strong>80% of the price gap is brand and rent</strong>, not the diamond.</p>
<h3>Q: 1.00 vs 0.99 — how much different?</h3>
<p>0.04mm diameter — invisible. Price differs 15-20%. <strong>0.92-0.98 ct is the
"sub-threshold" sweet spot</strong>. See <a href="/blog/diamond-carat-size">carat vs size</a>.</p>
<h3>Q: Are lab-grown really that much cheaper?</h3>
<p>Yes — production cost is ~30% of mining. But resale drops faster (40% after 5
years vs 60% for natural). See <a href="/blog/lab-vs-natural">lab vs natural</a>.</p>
<h3>Q: Best NT$300K play?</h3>
<p>Either: ① TW chain 1.0 ct G-VS1 H&amp;A, or ② I-PRIMO 0.85 ct E-VS2 H&amp;A
(BPD 15% higher), or ③ Blue Nile 1.2 ct G-VS1 (bigger, longer wait).
<strong>Option ② wins on math.</strong></p>
'''

# 4. diamond-50-cents
EN['diamond-50-cents'] = '''
<aside style="margin:0 0 22px;padding:16px 20px;background:linear-gradient(180deg,#fffdf7,#fbf3df);border-left:4px solid #c9a45c;border-radius:8px">
  <div style="font-size:10.5px;letter-spacing:.22em;text-transform:uppercase;color:#8a6e30;font-weight:700;margin-bottom:6px">TL;DR</div>
  The 0.20-0.50 carat range (20-50 "points") is Taiwan's mainstream engagement
  ring zone — over 50% of sales fall here. <strong>20¢ (NT$80-120K)</strong> for entry,
  <strong>30¢ (NT$120-180K)</strong> is the sales-volume leader, <strong>50¢ (NT$180-250K)</strong>
  is the value sweet spot when budget allows. With small stones, never skimp on cut.
</aside>

<h2>How big are these actually?</h2>
<table>
  <thead><tr><th>Carat</th><th>Grams</th><th>Diameter</th><th>Visual feel</th></tr></thead>
  <tbody>
    <tr><td>0.20 ct (20¢)</td><td>0.04 g</td><td>3.8 mm</td><td>Rice-grain, delicate</td></tr>
    <tr><td>0.30 ct (30¢)</td><td>0.06 g</td><td>4.3 mm</td><td>Rice-to-mungbean, daily-wear sweet spot</td></tr>
    <tr><td>0.50 ct (50¢)</td><td>0.10 g</td><td>5.2 mm</td><td>Mungbean, present on the hand</td></tr>
    <tr><td>0.70 ct</td><td>0.14 g</td><td>5.8 mm</td><td>(reference)</td></tr>
    <tr><td>1.00 ct</td><td>0.20 g</td><td>6.5 mm</td><td>(reference)</td></tr>
  </tbody>
</table>

<h2>Four smart packages</h2>
<h3>① 0.25 ct · G-VS2 · True H&amp;A · NT$80-120K</h3>
<p>20¢ is where retailers cheat on cut most often — small-stone cut differences
are harder to spot. But small stones rely on cut even more to sparkle.
Insist on GIA 3EX + H&amp;A. Color G-H is fine; clarity SI1 acceptable
(at 20¢, SI1 is 100% eye-clean).</p>

<h3>② 0.32 ct · G-VS2 · True H&amp;A · NT$120-180K</h3>
<p>Taiwan's #1 engagement ring spec. Visible without screaming. <strong>Don't pay
the integer premium</strong> — buy 0.32-0.34 ct rather than 0.30 (10-15% cheaper).</p>

<h3>③ 0.52 ct · F-VS2 · True H&amp;A · NT$180-250K</h3>
<p>Half-carat is "obviously a diamond" territory. At this size you can bump
color one grade (G→F) because color shows more. Don't bump clarity beyond
VS2 — zero visual return.</p>

<h3>④ 0.70 ct lab-grown · E-VS1 · True H&amp;A · NT$150-220K</h3>
<p>Same NT$200K budget gets you a 70¢ lab-grown with better color and clarity.
Trade-off: weaker resale. Pick this if buying-to-wear, not buying-to-resell.
See <a href="/blog/lab-vs-natural">lab vs natural</a>.</p>

<h2>Three pitfalls</h2>
<ol>
  <li><strong>Cut downgrade trap</strong> — jewellers push "20¢ D-VVS1 with GIA Very Good"
    to look spec-rich while only delivering 75% fire. Don't compromise on cut.</li>
  <li><strong>Integer premium</strong> — 0.30 / 0.50 ct cost 10-15% more than 0.28 / 0.48.
    See <a href="/blog/diamond-carat-size">half-threshold trick</a>.</li>
  <li><strong>No GIA cert</strong> — under 0.30 ct, jewellers often skip certification.
    But no cert = no resale + no insurance. IGI / HRD acceptable substitutes.</li>
</ol>

<h2>Three settings that visually grow small stones</h2>
<ol>
  <li><strong>Halo</strong> — small-diamond surround makes a 30¢ look like 50¢.</li>
  <li><strong>Thin prongs</strong> — 4-prong covers less of the stone than 6-prong.</li>
  <li><strong>Rose gold + pavé band</strong> — full-band sparkle complements small main.</li>
</ol>

<h2>Brand pricing for 30¢ G-VS2 H&amp;A (May 2026)</h2>
<table>
  <thead><tr><th>Brand</th><th>Price</th><th>Note</th></tr></thead>
  <tbody>
    <tr><td>BUERHKAU 不二鑽石</td><td>NT$100-120K</td><td>TW workshop, cheapest</td></tr>
    <tr><td>Mabelle 點睛品</td><td>NT$120-150K</td><td>Most stores nationwide</td></tr>
    <tr><td>ALUXE 亞立詩</td><td>NT$130-160K</td><td>Customisation</td></tr>
    <tr><td>I-PRIMO</td><td>NT$150-180K</td><td>Strict JP cut standards</td></tr>
    <tr><td>Ginza Shiraishi 銀座白石</td><td>NT$160-200K</td><td>Half-bespoke</td></tr>
    <tr><td>Cartier / Tiffany</td><td>NT$320-450K</td><td>2.5× premium</td></tr>
  </tbody>
</table>
<p>See <a href="/blog/taiwan-brands">Taiwan diamond brand comparison</a>.</p>
'''

# 5. taiwan-brands
EN['taiwan-brands'] = '''
<aside style="margin:0 0 22px;padding:16px 20px;background:linear-gradient(180deg,#fffdf7,#fbf3df);border-left:4px solid #c9a45c;border-radius:8px">
  <div style="font-size:10.5px;letter-spacing:.22em;text-transform:uppercase;color:#8a6e30;font-weight:700;margin-bottom:6px">TL;DR</div>
  Taiwan diamond rings split into 4 price tiers: <strong>international luxury</strong>
  Cartier/Tiffany NT$700K-1.3M (50-70% brand premium); <strong>EU designer</strong>
  Bulgari/Van Cleef NT$450K-750K; <strong>Japanese wedding line</strong>
  I-PRIMO/Ginza Shiraishi NT$250K-450K (best cut standards);
  <strong>Taiwan chain</strong> Mabelle/ALUXE/Promessa/JustDiamond NT$180K-320K
  (highest CP, most Dcard / PTT recommendations). Pick by which tier matches
  your budget and brand-vs-stone preference.
</aside>

<h2>Five price tiers at a glance</h2>
<table>
  <thead><tr><th>Tier</th><th>Brands</th><th>1 ct G-VS1</th><th>Premium</th></tr></thead>
  <tbody>
    <tr><td><strong>① Luxury house</strong></td><td>Cartier · Tiffany · Harry Winston</td><td>NT$700K-1.3M</td><td>Brand 50-70%</td></tr>
    <tr><td><strong>② EU designer</strong></td><td>Bulgari · Van Cleef · Chaumet</td><td>NT$450K-750K</td><td>Design + craft 30-50%</td></tr>
    <tr><td><strong>③ JP wedding</strong></td><td>I-PRIMO · Ginza Shiraishi · Mikimoto</td><td>NT$250K-450K</td><td>Cut + service 20-30%</td></tr>
    <tr><td><strong>④ TW chain</strong></td><td>Mabelle · ALUXE · Promessa · Just Diamond · BUERHKAU</td><td>NT$180K-320K</td><td>Lowest 10-20%</td></tr>
    <tr><td><strong>⑤ Online direct</strong></td><td>Blue Nile · James Allen · Whiteflash</td><td>NT$130K-250K</td><td>Near zero</td></tr>
  </tbody>
</table>

<h2>Taiwan chain (Tier 4) deep-dive</h2>
<h3>Mabelle 點睛品</h3>
<p>Owned by <strong>Chow Sang Sang</strong> (HK, 80+ years). 20+ years in Taiwan, "craft +
quality" positioning. GIA standard, loose-stone purchase available.
<strong>Most-recommended brand on Dcard 婚版 in 2024</strong>. Largest physical-store
network — best for "see before you decide" buyers.</p>

<h3>ALUXE 亞立詩</h3>
<p>Founded 2005 in Taiwan. Specialises in <strong>customised GIA diamond engagement
rings</strong>. Strong on customisation flexibility and consultation; weaker on
brand strength and resale value vs Mabelle.</p>

<h3>Promessa 瑞鎂</h3>
<p>"European-design Taiwan-made". Modern light-luxe style. GIA standard, settings
favour European geometry. Suits buyers preferring clean modernist designs.</p>

<h3>Just Diamond 鎮金店 / Peonia Diamond</h3>
<p>Two product lines: classic (Just Diamond) and patented (Peonia). The
<strong>Peonia 88-facet cut</strong> (DE/JP/TW patents) creates more fire than the
standard 57-facet round brilliant — one of the few Taiwan brands with a
genuine optical differentiation. Top-3 on Dcard / PTT.</p>

<h3>BUERHKAU 不二鑽石</h3>
<p>Northern-Taiwan workshop-style brand. <strong>No advertising budget = lowest
price</strong>. GIA standard, Taipei stores only. Best for cost-conscious buyers
who don't care about brand packaging.</p>

<h2>Japanese line (Tier 3)</h2>
<h3>I-PRIMO</h3>
<p>Japan's #1 wedding-ring specialist, ~150 designs. <strong>Strongest on consultation
process and cut standards</strong> — H&amp;A is the floor, not a feature. 12 stores
in Taiwan. Best fit: NT$250-400K budget, prefer Japanese refinement.</p>

<h3>Ginza Diamond Shiraishi 銀座白石</h3>
<p>Founded 1994. Pioneer of "half-bespoke" wedding rings and "set ring" concept.
28 years, 64 stores worldwide, served 850K+ couples. <strong>Cut + service tier
above I-PRIMO</strong>; price slightly higher.</p>

<h3>Mikimoto</h3>
<p>1893 pearl royalty; diamond rings are an extension. Best when buyer wants
both diamonds and pearl pieces. Limited ring designs, classic 6-prong focus.</p>

<h2>Three buying scenarios</h2>
<h3>Scenario A: NT$200-300K, brand visibility matters</h3>
<p><strong>Pick Mabelle or Just Diamond Peonia.</strong> Mabelle for store coverage and
service guarantee; Peonia for the patented optical differentiation.</p>

<h3>Scenario B: NT$300-450K, cut and service matter</h3>
<p><strong>Pick I-PRIMO or Ginza Shiraishi.</strong> JP cut standards are noticeably
stricter than TW chain. The 90-min consultation is part of the value.</p>

<h3>Scenario C: NT$150-220K, maximum CP</h3>
<p><strong>Pick BUERHKAU (in-store) or Blue Nile / James Allen (online).</strong>
No brand-marketing tax means more of your money buys actual diamond.
Verify the return policy.</p>

<h2>Three traps that hit every brand</h2>
<ol>
  <li><strong>"In-house certificate" doesn't count</strong> — must be GIA / IGI / HRD.
    See <a href="/blog/cert-comparison">cert comparison</a>.</li>
  <li><strong>"Excellent" is not "true H&amp;A"</strong> — only 20% of GIA Excellents pass.
    See <a href="/blog/hearts-arrows-truth">H&amp;A truth</a>.</li>
  <li><strong>"0% interest financing" hides 5-8% discount</strong>.
    See <a href="/blog/diamond-financing">financing guide</a>.</li>
</ol>

<h2>Verify with math</h2>
<p>Picked a brand? <strong>Get the GIA report photo from the staff</strong> and put the
four proportions into the <a href="/">BrillianceLab calculator</a>. Same NT$300K,
optical scores can differ 10-15 points between brands — that's the difference
no brand reputation can hide.</p>
'''

# 6. dcard-ptt-recommendations
EN['dcard-ptt-recommendations'] = '''
<aside style="margin:0 0 22px;padding:16px 20px;background:linear-gradient(180deg,#fffdf7,#fbf3df);border-left:4px solid #c9a45c;border-radius:8px">
  <div style="font-size:10.5px;letter-spacing:.22em;text-transform:uppercase;color:#8a6e30;font-weight:700;margin-bottom:6px">TL;DR</div>
  Manual count of 30 real-purchase posts on <strong>Dcard 婚版 + PTT marriage</strong>
  (Jan 2024 - Apr 2026). Top 5: ① Mabelle 點睛品 (8 mentions),
  ② I-PRIMO (7), ③ Ginza Shiraishi 銀座白石 (5), ④ Just Diamond Peonia (4),
  ⑤ ALUXE 亞立詩 (3). Common praise: physical service + after-sales.
  Common complaint: brand premium too high.
</aside>

<h2>Full ranking</h2>
<p>Counted across <strong>30 real-purchase posts</strong> on Dcard 婚版 (≥ 10 likes) and
PTT marriage board (high推/like) between Jan 2024 and Apr 2026. Brand mentions
in the body of recommendation posts only — not ads.</p>

<table>
  <thead><tr><th>Rank</th><th>Brand</th><th>Dcard</th><th>PTT</th><th>Total</th></tr></thead>
  <tbody>
    <tr><td><strong>01</strong></td><td>Mabelle 點睛品</td><td>5</td><td>3</td><td>8</td></tr>
    <tr><td><strong>02</strong></td><td>I-PRIMO</td><td>4</td><td>3</td><td>7</td></tr>
    <tr><td><strong>03</strong></td><td>Ginza Shiraishi 銀座白石</td><td>3</td><td>2</td><td>5</td></tr>
    <tr><td><strong>04</strong></td><td>Just Diamond Peonia 鎮金店</td><td>3</td><td>1</td><td>4</td></tr>
    <tr><td><strong>05</strong></td><td>ALUXE 亞立詩</td><td>2</td><td>1</td><td>3</td></tr>
    <tr><td>06</td><td>Cartier</td><td>0</td><td>2</td><td>2</td></tr>
  </tbody>
</table>

<h2>Five common positives</h2>
<ol>
  <li><strong>In-store H&amp;A viewers</strong> — buyers can verify Hearts &amp; Arrows on the spot.
    All JP-line brands and Mabelle offer this. See <a href="/blog/hearts-arrows-truth">H&amp;A truth</a>.</li>
  <li><strong>GIA is the floor</strong> — 28 of 30 posts insist on GIA. No GIA = no buy.
    See <a href="/blog/gia-guide">GIA guide</a>.</li>
  <li><strong>Free ring-size adjustment</strong> — most brands offer 1-2 size adjustments for life.</li>
  <li><strong>Annual polish included</strong> — most chains offer one free polish per year.</li>
  <li><strong>7-30 day returns</strong> — Mabelle 30 days, I-PRIMO 14 days, Cartier 14 days.</li>
</ol>

<h2>Three common pitfalls</h2>
<ol>
  <li><strong>"Store certificates" trap</strong> — local jewellers' own certificates have no
    international standing; insurance won't accept them. Always insist on GIA / IGI / HRD.</li>
  <li><strong>"0% interest financing" hides discount</strong> — typically equivalent to giving
    up 5-8% off-list discount. See <a href="/blog/diamond-financing">financing guide</a>.</li>
  <li><strong>Online no-return</strong> — verify return windows for domestic; calculate 5-8%
    import duty for Blue Nile / James Allen.</li>
</ol>

<h2>How to use this ranking</h2>
<p>"Many people picked X" doesn't equal "right for you". Suggested process:</p>
<ol>
  <li>Use <a href="/blog/budget-formula">BPD formula</a> to find your budget's best 4Cs.</li>
  <li>Pick 3 brands at that price tier (e.g., NT$250K → Mabelle + ALUXE + I-PRIMO).</li>
  <li>Visit each store, view one same-spec stone, run all three through the
    <a href="/">BrillianceLab calculator</a>.</li>
  <li>Buy the highest BPD.</li>
</ol>
'''

# 7. diamond-glossary
EN['diamond-glossary'] = '''
<aside style="margin:0 0 22px;padding:16px 20px;background:linear-gradient(180deg,#fffdf7,#fbf3df);border-left:4px solid #c9a45c;border-radius:8px">
  <div style="font-size:10.5px;letter-spacing:.22em;text-transform:uppercase;color:#8a6e30;font-weight:700;margin-bottom:6px">TL;DR</div>
  30 essential diamond-buying terms across 4 categories: <strong>certs &amp; grades</strong>
  (GIA, IGI, HRD, 4Cs, Plotting), <strong>cut geometry</strong> (Tolkowsky, Crown Angle,
  Pavilion, Table %, Hearts &amp; Arrows), <strong>settings</strong> (Pavé, Halo, Bezel,
  Solitaire, prongs), <strong>optics &amp; market</strong> (BPD, HCA, Light Return, Fire,
  Scintillation, Lab-grown).
</aside>

<h2>Certs &amp; grades (8 terms)</h2>
<p><strong>GIA</strong> — Gemological Institute of America, founded 1931, the most authoritative
diamond grading lab. <a href="/blog/gia-guide">→ GIA report guide</a></p>
<p><strong>IGI</strong> — International Gemological Institute, India-based, standards 1-2 grades
looser than GIA; dominant in lab-grown.</p>
<p><strong>HRD</strong> — Hoge Raad voor Diamant (Belgium), most authoritative European cert.</p>
<p><strong>AGS</strong> — American Gem Society, 0-10 scale (0 = best). Acquired by GIA but
certs still circulate.</p>
<p><strong>4Cs</strong> — Cut, Color, Clarity, Carat. The grading framework GIA standardised in 1953.</p>
<p><strong>Plotting</strong> — the inclusion-distribution diagram on a GIA report. Functions like
the diamond's fingerprint. <a href="/blog/inclusions-types-guide">→ inclusion types</a></p>
<p><strong>Laser inscription</strong> — GIA-laser-engraved cert number on the diamond's girdle,
visible at 10× magnification. Used for authentication.</p>
<p><strong>Report Check</strong> — GIA's online verification tool (gia.edu/report-check).
Enter cert number + carat to get full diamond data.</p>

<h2>Cut geometry (8 terms)</h2>
<p><strong>Tolkowsky proportions</strong> — Marcel Tolkowsky's 1919 PhD-derived "optically perfect"
proportions: Table 53%, Crown 34.5°, Pavilion 40.75°. <a href="/blog/round-cut-deep-dive">→ round brilliant</a></p>
<p><strong>Crown Angle</strong> — slope of the upper half. Tolkowsky standard 34.5°; GIA Excellent
range 31.5-36.5°.</p>
<p><strong>Pavilion Angle</strong> — slope of the lower half. Tolkowsky 40.75°. Off by 0.4° hurts
light return.</p>
<p><strong>Table %</strong> — top flat width ÷ total width. Ideal 53-58%; too wide = "glassy".</p>
<p><strong>Depth %</strong> — total height ÷ total width. Ideal 59-62.5%; too deep leaks light.</p>
<p><strong>Hearts &amp; Arrows (H&amp;A)</strong> — viewed through an H&amp;A scope: 8 arrows from
top, 8 hearts from bottom. The mark of perfect 8-fold symmetry.
<a href="/blog/hearts-arrows-truth">→ H&amp;A truth</a></p>
<p><strong>Polish</strong> — finishing-quality grade (Excellent / Very Good / Good).
Excellent is the floor.</p>
<p><strong>Symmetry</strong> — facet-alignment grade. Excellent is required for Hearts &amp; Arrows.</p>

<h2>Settings (8 terms)</h2>
<p><strong>Solitaire</strong> — single-stone classic, usually 6- or 4-prong.</p>
<p><strong>Halo</strong> — small-diamond ring around the main stone, visually enlarges by 30-40%.
<a href="/blog/prong-settings-guide">→ 7 settings</a></p>
<p><strong>Pavé</strong> — densely set tiny diamonds on the band, paving-stone effect.</p>
<p><strong>Bezel</strong> — full metal rim around the main stone. Most secure, makes stone look smaller.</p>
<p><strong>Trilogy / 3-stone</strong> — central main + two side stones (typically 30% smaller),
symbolising past / present / future.</p>
<p><strong>6-prong / 4-prong</strong> — number of metal claws holding the main stone. 6 = secure
but covers more; 4 = more light, slight stone-loss risk.</p>
<p><strong>Eternity</strong> — full-circle pavé band, often anniversary gift.</p>
<p><strong>Toi et Moi</strong> — "you and me", two main stones of different shapes side-by-side
(often pear + oval). Trending 2024-2026.</p>

<h2>Optics &amp; market (6 terms)</h2>
<p><strong>Brilliance</strong> — white light returned to the eye. Main component of Light Return.</p>
<p><strong>Fire</strong> — degree to which white light disperses into spectral colors.
Crown Angle is the key driver.</p>
<p><strong>Scintillation</strong> — bright/dark contrast as the diamond moves. Drives "dynamic" appeal.</p>
<p><strong>HCA</strong> — Holloway Cut Adviser, 4-dimensional optical scoring (Light Return / Fire /
Scintillation / Spread), each 0-2 points.</p>
<p><strong>BPD</strong> — Brilliance per Dollar = optical-score × √carat ÷ (price ÷ 10K).
BrillianceLab's metric for "sparkle per dollar". <a href="/blog/budget-formula">→ BPD formula</a></p>
<p><strong>Lab-grown</strong> — CVD- or HPHT-grown diamonds, chemically identical to natural,
70% cheaper. <a href="/blog/lab-vs-natural">→ lab vs natural</a></p>
'''

# 8. proposal-vs-wedding-vs-eternity
EN['proposal-vs-wedding-vs-eternity'] = '''
<aside style="margin:0 0 22px;padding:16px 20px;background:linear-gradient(180deg,#fffdf7,#fbf3df);border-left:4px solid #c9a45c;border-radius:8px">
  <div style="font-size:10.5px;letter-spacing:.22em;text-transform:uppercase;color:#8a6e30;font-weight:700;margin-bottom:6px">TL;DR</div>
  Four ring types: <strong>engagement ring</strong> (main diamond, given at proposal),
  <strong>wedding ring</strong> (exchanged at ceremony, usually no main stone),
  <strong>wedding band</strong> (couple-paired same design), <strong>eternity ring</strong>
  (full-circle diamonds, anniversary gift). JP/KR culture uses "one-ring" model;
  Western uses "two-ring"; Greater China sometimes adds a third anniversary ring.
</aside>

<h2>Quick comparison</h2>
<table>
  <thead><tr><th>Ring</th><th>When</th><th>Main stone?</th><th>Worn on</th><th>NT$</th></tr></thead>
  <tbody>
    <tr><td><strong>Engagement ring</strong></td><td>Proposal moment</td><td>Yes (0.5-2 ct)</td><td>Left ring finger</td><td>150K-1M</td></tr>
    <tr><td><strong>Wedding ring</strong></td><td>Ceremony exchange</td><td>None / micro-pavé</td><td>Same finger</td><td>30-150K / pair</td></tr>
    <tr><td><strong>Wedding band</strong></td><td>Daily wear</td><td>None / micro-pavé</td><td>Both partners</td><td>50-250K / pair</td></tr>
    <tr><td><strong>Eternity ring</strong></td><td>Anniversary / milestone</td><td>Full-circle small stones</td><td>Right finger / stacked</td><td>100-500K</td></tr>
  </tbody>
</table>

<h2>Each ring in detail</h2>
<h3>① Engagement ring (proposal ring)</h3>
<p><strong>Prepared by one partner for the proposal moment</strong>; main stone is the focus
(0.5-2 ct, solitaire or halo). Traditionally a "surprise" given to the future
spouse, so size has to be measured covertly.
See <a href="/blog/ring-sizing">7 stealth ring-sizing methods</a>. Western tradition
centres the engagement ring; JP/KR often skips the wedding band entirely.</p>

<h3>② Wedding ring (wedding band)</h3>
<p>Exchanged during the marriage ceremony. <strong>Typically a clean metal band with
no or micro-pavé diamonds</strong> (platinum, 18K white gold, rose gold are most common).
Symbolises "no beginning, no end". NT$30-150K per pair. When stacked with the
engagement ring, match the metal color to avoid wear marks.</p>

<h3>③ Wedding band (couple rings)</h3>
<p><strong>Same-design for both partners</strong>, different widths (men wider). Usually
plain metal. <strong>Most popular in Taiwan</strong> — clean, durable, reasonably priced
(NT$50-250K per pair). Japanese brands (I-PRIMO, Ginza Shiraishi) excel here.</p>

<h3>④ Eternity ring</h3>
<p><strong>Small diamonds set around the full circumference</strong>. Often gifted on
anniversaries (10th, 25th), childbirth, milestones. Stacks with the wedding band
forming a "three-ring set". NT$100-500K, typically uses 0.05-0.10 ct × 20-30 stones.</p>

<h2>Three traditions</h2>
<h3>JP/KR "one-ring" model</h3>
<p>Engagement ring IS the wedding ring. Same ring is exchanged at the ceremony.
Best fit: NT$300-500K all-in budget, one ring serves both purposes.</p>

<h3>Western "two-ring" model</h3>
<p>Engagement (large) + wedding band (plain metal), worn stacked daily.
Best fit: NT$450-800K, wants formal exchange-of-rings ceremony, and may add
an eternity ring later for the three-ring set.</p>

<h3>Greater China "three-ring" model</h3>
<p>Engagement + wedding + eternity rings rotated through life stages.
Best fit: NT$600K-1.5M, uses rings to mark life chapters.</p>

<h2>FAQ</h2>
<h3>Q: Budget NT$200K — can I just buy 1 ring?</h3>
<p>Yes — go JP/KR style. One 0.5 ct G-VS2 true H&amp;A (NT$180-220K) serves
as both engagement and wedding ring. Groom places it during the ceremony;
no second ring needed. See <a href="/blog/wedding-bands">5-rings guide</a>.</p>
<h3>Q: Do men need a ring?</h3>
<p>Cultural choice. Western + Greater China usually yes; JP less so. If
yes, choose plain or micro-pavé band, 4-6mm width, work-friendly.
See <a href="/blog/mens-engagement-rings">men's engagement ring guide</a>.</p>
<h3>Q: Can three rings stack?</h3>
<p>Yes — match metal colour. Order from base outward: wedding band → engagement
→ eternity. Three-ring stacking has been Western-trending for ~5 years.</p>
<h3>Q: Are wedding band and wedding ring different?</h3>
<p>Wedding ring = any ring exchanged at the ceremony (matching pair or not);
wedding band = specifically the matching pair. Taiwan's "結婚對戒" is both —
matching pair exchanged at ceremony.</p>
'''

# 9. diamond-faq (replace existing thin English with full)
EN['diamond-faq'] = '''
<aside style="margin:0 0 22px;padding:16px 20px;background:linear-gradient(180deg,#fffdf7,#fbf3df);border-left:4px solid #c9a45c;border-radius:8px">
  <div style="font-size:10.5px;letter-spacing:.22em;text-transform:uppercase;color:#8a6e30;font-weight:700;margin-bottom:6px">TL;DR</div>
  50 of the most common questions Taiwanese first-time diamond buyers ask,
  organised into 7 themes: 4C basics, budget &amp; value, certs, lab-grown,
  brands &amp; channels, proposal &amp; rings, care &amp; resale.
  Direct answers, no fluff.
</aside>

<h2>About 4Cs (8 questions)</h2>
<details><summary>What are the 4Cs?</summary><p>Cut, Color, Clarity, Carat.
<strong>Cut matters most</strong> — the only one humans control 100%. See
<a href="/blog/diamond-4cs-cheatsheet">4Cs cheatsheet</a>.</p></details>
<details><summary>Which C matters most?</summary><p>Cut. Same carat / color /
clarity, dropping cut one grade costs 30-40% of price.</p></details>
<details><summary>Can I tell D from H face-up?</summary><p>On white paper yes, in
normal wear barely. <strong>G-H is the value sweet spot</strong> — 30% cheaper than D-F
with no visible difference.</p></details>
<details><summary>What clarity is enough?</summary><p>VS2. Eye-clean for sure;
VVS / IF spend doesn't show.</p></details>
<details><summary>How big is 1 carat?</summary><p>0.2g, ~6.5mm round diameter.
0.5 ct ≈ 5mm, 2 ct ≈ 8mm.</p></details>
<details><summary>Excellent vs Very Good cut?</summary><p>One GIA grade apart,
~5-10% optical difference. Tight budget: VG cut + bumped color/clarity may
out-perform Excellent + lower others.</p></details>
<details><summary>Is fluorescence good or bad?</summary><p>Medium fluor on D-H
is neutral or slightly whitening; on I-K it can occasionally cause haze.
Strong/Very Strong fluor diamonds are 10-15% cheaper.</p></details>
<details><summary>How to pick a shape?</summary><p>Round = brightest + most resale.
Princess = second-brightest. Pear = elongates fingers. Oval = warm.
Emerald = elegant. <strong>First-timers should pick round.</strong></p></details>

<h2>Budget &amp; value (8 questions)</h2>
<details><summary>Reasonable budget?</summary><p>No "should" amount. Common
ranges in Taiwan: NT$150-250K for 0.5-0.7ct, NT$300-500K for 1ct.
2-3 months' salary is common. <strong>Doesn't strain quality of life</strong> = reasonable.</p></details>
<details><summary>Where did "3 months' salary" come from?</summary><p>1947 De Beers
ad campaign — pure marketing.</p></details>
<details><summary>0.99 vs 1.00 carat?</summary><p>Visually identical (0.04mm
diameter), price differs 15-20%. <strong>0.92-0.98 is the smart half-threshold.</strong></p></details>
<details><summary>How to compute value?</summary><p>Use BPD = (optical × √carat)
÷ (price ÷ 10K). Higher = better. <a href="/">BrillianceLab calculator</a> auto-calculates.</p></details>
<details><summary>Can I haggle?</summary><p>Yes. Chain brands typically 5-10%,
independent workshops 10-20%, second-hand 15-30%.</p></details>
<details><summary>Engagement and wedding ring same?</summary><p>JP/KR yes,
Western no. See <a href="/blog/proposal-vs-wedding-vs-eternity">4 ring types</a>.</p></details>
<details><summary>Is financing worth it?</summary><p>"0% interest" usually = giving
up 5-8% off-list discount. See <a href="/blog/diamond-financing">financing guide</a>.</p></details>
<details><summary>Online vs in-store savings?</summary><p>Online beats in-store
by 15-30% (no brand markup, no rent, no salesperson commission). Verify
return policy.</p></details>

<h2>Certs &amp; grading (6 questions)</h2>
<details><summary>GIA, IGI, HRD — which is best?</summary><p>GIA most authoritative,
HRD second, IGI third (looser standards). <strong>0.3 ct+ insist on one of them.</strong>
See <a href="/blog/cert-comparison">full comparison</a>.</p></details>
<details><summary>Can I buy without GIA?</summary><p>Under 0.3 ct OK; 0.3 ct+
strongly recommended for resale and insurance.</p></details>
<details><summary>Is a copy of the cert OK?</summary><p>No — demand the original
and verify the laser inscription on the diamond's girdle (10× loupe).</p></details>
<details><summary>How to verify a GIA cert?</summary><p>Visit gia.edu/report-check,
enter cert number + carat. Real cert shows full data + PDF.</p></details>
<details><summary>"Store guarantee certificates" valid?</summary><p>No. They lack
international recognition; insurers won't honor them.</p></details>
<details><summary>How much is GIA re-grading?</summary><p>NT$4-10K depending on
carat; takes 4-8 weeks.</p></details>

<h2>Lab-grown (6 questions)</h2>
<details><summary>What are lab-grown diamonds?</summary><p>Diamonds grown via
CVD or HPHT in labs. <strong>Chemically 100% identical to natural diamonds.</strong></p></details>
<details><summary>Are they "fake"?</summary><p>No. They're real diamonds. GIA grades
them with the same 4Cs. Fakes are moissanite or CZ — different materials.</p></details>
<details><summary>How much cheaper?</summary><p>~70% less for the same grade.
1ct G-VS1 natural NT$300K → lab-grown NT$80-100K.
See <a href="/blog/lab-vs-natural">lab vs natural</a>.</p></details>
<details><summary>OK for engagement?</summary><p>Yes. 40% of Western under-30
proposers choose lab-grown. Discuss first — some partners value the natural origin.</p></details>
<details><summary>Will they lose value?</summary><p>Lower resale due to falling
production prices. Buy lab-grown for wearing, not investing.</p></details>
<details><summary>How to tell lab from natural?</summary><p>Visually impossible.
GIA / IGI certs explicitly mark "Laboratory-Grown".</p></details>

<h2>Brands &amp; channels (7 questions)</h2>
<details><summary>Tiffany / Cartier worth it?</summary><p>For brand story and
unboxing experience yes; for diamond value, the 30-50% brand premium buys
no extra optical performance. Same-grade stone at independent workshop
is 40% cheaper.</p></details>
<details><summary>Can I trust Taiwan local brands?</summary><p>Mid-size chains
(Mabelle, Ginza Shiraishi TW, ALUXE) are reliable with international certs.
Independent workshops vary — check reputation.
See <a href="/blog/taiwan-brands">Taiwan brands</a>.</p></details>
<details><summary>Pre-owned worth considering?</summary><p>30-50% cheaper than
retail, but check 7 traps. See <a href="/blog/secondhand-rings">pre-owned guide</a>.</p></details>
<details><summary>Best Dcard / PTT-recommended brand?</summary><p>Mabelle 點睛品.
See <a href="/blog/dcard-ptt-recommendations">full ranking</a>.</p></details>
<details><summary>Is online safe?</summary><p>For Blue Nile / James Allen yes (US
established, returns honored). Avoid private sellers without escrow.</p></details>
<details><summary>How much can I haggle off list?</summary><p>Chain brands 5-10%
discount common; aggressive negotiation can hit 15% if buying multiple pieces.</p></details>
<details><summary>Best month to buy?</summary><p>Aug (post-Anniversary clearance)
or after Chinese New Year (slow season). 5-10% extra discount common.</p></details>

<h2>Proposal &amp; rings (8 questions) · Care &amp; resale (7 questions)</h2>
<p>For these full sections see the Chinese version above. The questions cover:
ring sizing, proposal-day logistics, mens' rings, materials, daily care,
insurance, and resale realities. Direct deep-dives:
<a href="/blog/engagement-guide">9-step engagement</a> ·
<a href="/blog/ring-sizing">ring sizing</a> ·
<a href="/blog/wedding-bands">5 ring types</a> ·
<a href="/blog/wedding-metals">6 metals</a> ·
<a href="/blog/diamond-care">care guide</a> ·
<a href="/blog/ring-insurance">insurance</a> ·
<a href="/blog/diamond-resale">resale truth</a>.</p>
'''

# 10. gia-guide (extend the existing thin English)
EN['gia-guide'] = '''
<aside style="margin:0 0 22px;padding:16px 20px;background:linear-gradient(180deg,#fffdf7,#fbf3df);border-left:4px solid #c9a45c;border-radius:8px">
  <div style="font-size:10.5px;letter-spacing:.22em;text-transform:uppercase;color:#8a6e30;font-weight:700;margin-bottom:6px">TL;DR</div>
  A GIA report has 6 sections: <strong>4Cs · proportions diagram · Polish/Symmetry/
  Fluorescence · laser inscription · plotting (inclusion map) · Report Check QR</strong>.
  Cut + Polish + Symmetry all Excellent + true Hearts &amp; Arrows = "true 3EX".
  Optical performance gap between true 3EX and edge-Excellent is ~25%.
</aside>

<h2>What's on a GIA report</h2>
<p>The GIA Diamond Grading Report has 6 functional zones:</p>
<ol>
  <li><strong>4Cs panel</strong> — Cut grade, Color (D-Z), Clarity (FL-I3), Carat (e.g. 1.05 ct)</li>
  <li><strong>Proportions diagram</strong> — table %, depth %, crown angle, pavilion angle, girdle, culet</li>
  <li><strong>Polish &amp; Symmetry</strong> — finishing-quality grades (Excellent / Very Good / Good)</li>
  <li><strong>Fluorescence</strong> — None / Faint / Medium / Strong / Very Strong (UV reaction)</li>
  <li><strong>Laser inscription</strong> — cert number engraved on girdle (10× loupe)</li>
  <li><strong>Plotting</strong> — inclusion type, position, severity diagram</li>
</ol>

<h2>"True 3EX" — what it actually means</h2>
<p>The industry shorthand "3EX" stands for: Cut Excellent + Polish Excellent +
Symmetry Excellent. <strong>But "Cut Excellent" is a wide bucket</strong> — only ~20% of
GIA Excellents pass true Hearts &amp; Arrows verification (8-fold optical
symmetry). Always ask the jeweller for an H&amp;A scope. The visual gap
between true 3EX and edge-of-Excellent is <strong>25%</strong> in fire and brilliance.
<a href="/blog/hearts-arrows-truth">→ H&amp;A truth</a></p>

<h2>Verifying authenticity</h2>
<p>Three checks any buyer should do:</p>
<ol>
  <li><strong>Online verification</strong> — visit gia.edu/report-check, enter the
    cert number + carat. Real cert shows full data + downloadable PDF.</li>
  <li><strong>Laser inscription match</strong> — under 10× loupe, the diamond's girdle
    should show "GIA + 8 digits" matching the report.</li>
  <li><strong>Plotting cross-check</strong> — internal inclusions on the report should
    appear in the same positions when viewed under loupe.</li>
</ol>

<h2>How to read the proportions diagram</h2>
<p>The diamond cross-section shows your stone's geometry. Compare against
Tolkowsky 1919 standards:</p>
<ul>
  <li>Table %: ideal 53-58%</li>
  <li>Depth %: ideal 59-62.5%</li>
  <li>Crown angle: ideal 33.7-35.0°</li>
  <li>Pavilion angle: ideal 40.6-41.0°</li>
  <li>Girdle: thin to slightly thick (avoid extremely thin / extremely thick)</li>
  <li>Culet: none to small (large culet = visible dot from top, hurts brilliance)</li>
</ul>
<p>Plug these four numbers into the <a href="/">BrillianceLab calculator</a>
for an objective optical score and 4-dim breakdown
(Light Return / Fire / Scintillation / Spread).</p>

<h2>Fluorescence — overlooked variable</h2>
<p>Fluorescence is the diamond's reaction under UV light:</p>
<ul>
  <li><strong>None</strong> — neutral, ~5% premium in some markets</li>
  <li><strong>Faint / Medium</strong> — usually neutral on D-H color; can slightly
    whiten the appearance of I-K stones</li>
  <li><strong>Strong / Very Strong</strong> — occasionally causes "haze" on high-color
    diamonds; 10-15% price discount</li>
</ul>
<p>Fluorescence is a personal preference + a value play.
<a href="/blog/fluorescence-deep-dive">→ deep dive</a></p>

<h2>Common GIA-report misreadings</h2>
<ol>
  <li><strong>"Excellent" is the floor, not the goal</strong> — many GIA Excellents are
    average; H&amp;A is the actual top.</li>
  <li><strong>Color and clarity grades aren't the price drivers</strong> — cut is.
    Don't over-pay for D-VVS combos.</li>
  <li><strong>The plotting map matters even when SI</strong> — SI1 with a
    table-edge inclusion is a real problem; SI1 with a side inclusion is invisible.</li>
</ol>

<h2>Next step</h2>
<p>You can read a GIA report? Now run your candidate's four proportion numbers
through the <a href="/">BrillianceLab calculator</a> and see where it scores.
Same NT$300K, two GIA-Excellent stones can score 30 points apart on optics —
that's the difference between buying and not buying.</p>
'''


# ─────────────────────────────────────────────────────────────────
# Driver
# ─────────────────────────────────────────────────────────────────

def patch(slug: str, en_html: str) -> bool:
    p = ROOT / 'blog' / f'{slug}.html'
    if not p.exists():
        print(f'  miss: {slug}')
        return False
    src = p.read_text(encoding='utf-8')
    block = wrap_en(en_html, slug)
    if SENTINEL in src:
        # Replace existing block in place
        new = re.sub(
            r'\n?<div[^>]*' + re.escape(SENTINEL) + r'[^>]*>[\s\S]*?</div>\s*',
            block, src, count=1)
    else:
        # Insert immediately after the article body close OR before footer/script
        # Strategy: find closing </article> (most reliable); fall back to before </main>.
        if '</article>' in src:
            new = src.replace('</article>', '</article>' + block, 1)
        elif '</main>' in src:
            new = src.replace('</main>', block + '</main>', 1)
        else:
            print(f'  no article/main close: {slug}')
            return False
    if new == src:
        return False
    p.write_text(new, encoding='utf-8')
    return True


def main():
    n = 0
    for slug, html in EN.items():
        if patch(slug, html):
            n += 1
            wc = len(re.findall(r'\b[a-zA-Z]{2,}\b', html))
            print(f'  injected en ({wc:>4} words): {slug}')
    print(f'\n{n} articles received English translations')


if __name__ == '__main__':
    main()
