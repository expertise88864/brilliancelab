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

Round 14 batch: remaining 39 articles (full site coverage)
  4Cs/Shapes:  diamond-color, diamond-clarity, diamond-carat-size, diamond-shapes,
               cert-comparison, hearts-arrows-truth, lab-vs-natural, budget-formula,
               fluorescence-deep-dive, inclusions-types-guide
  Purchase:    engagement-guide, diamond-scams, diamond-resale, diamond-financing,
               diamond-price-trends, diamond-vs-gold, ring-sizing, ring-insurance,
               secondhand-rings, mens-engagement-rings
  Bands/Cer:   wedding-bands, wedding-metals, prong-settings-guide,
               engraving-personalization, heirloom-redesign, proposal-speech,
               engagement-timeline, dating-duration, destination-wedding, lgbtq-rings
  Care/Niche:  diamond-care, diamond-fun-facts, famous-diamonds, fancy-cuts-guide,
               round-cut-deep-dive, moissanite-vs-cz-vs-lab, gemstones-comparison,
               sustainable-diamonds, diamond-photography
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
# Round 14 — 4Cs / Shapes (10)
# ─────────────────────────────────────────────────────────────────

EN['diamond-color'] = '''
<aside style="margin:0 0 22px;padding:16px 20px;background:linear-gradient(180deg,#fffdf7,#fbf3df);border-left:4px solid #c9a45c;border-radius:8px">
  <div style="font-size:10.5px;letter-spacing:.22em;text-transform:uppercase;color:#8a6e30;font-weight:700;margin-bottom:6px">TL;DR</div>
  Diamond color D-Z grades how <em>colorless</em> the stone is. D-F is "colorless",
  G-J "near-colorless", K+ visibly tinted. Face-up you cannot tell D from G.
  G is the value sweet spot — same look as D, ~30% cheaper.
</aside>

<h2>How GIA grades color</h2>
<p>Gemologists view the diamond <strong>table-down</strong> against a white card under
controlled D65 lighting and compare against master stones. The scale runs D
(absolutely colorless) to Z (light yellow). After Z, the diamond enters
<a href="/blog/fancy-cuts-guide">Fancy Color</a> territory and is graded on a
separate scale.</p>

<h2>The face-up truth</h2>
<p>D-G look identical face-up to the naked eye. Below G, a yellow tint becomes
detectable, especially in larger stones (over 1 ct) and in step-cuts (emerald,
asscher) where the open table reveals body color. For brilliant cuts (round,
oval, cushion) you can drop to <strong>H or even I</strong> and still appear white in
warm Asian indoor lighting (3000K).</p>

<h2>Why G is the sweet spot</h2>
<table style="width:100%;border-collapse:collapse;margin:14px 0">
  <thead><tr style="background:#fbf3df"><th style="padding:6px;border:1px solid #d4c08a">Color</th><th style="padding:6px;border:1px solid #d4c08a">Look face-up</th><th style="padding:6px;border:1px solid #d4c08a">Price vs G</th></tr></thead>
  <tbody>
    <tr><td style="padding:6px;border:1px solid #d4c08a">D</td><td style="padding:6px;border:1px solid #d4c08a">Identical</td><td style="padding:6px;border:1px solid #d4c08a">+45%</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">E</td><td style="padding:6px;border:1px solid #d4c08a">Identical</td><td style="padding:6px;border:1px solid #d4c08a">+30%</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">F</td><td style="padding:6px;border:1px solid #d4c08a">Identical</td><td style="padding:6px;border:1px solid #d4c08a">+15%</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a"><strong>G</strong></td><td style="padding:6px;border:1px solid #d4c08a">Reference</td><td style="padding:6px;border:1px solid #d4c08a">0%</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">H</td><td style="padding:6px;border:1px solid #d4c08a">Still white</td><td style="padding:6px;border:1px solid #d4c08a">-10%</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">I</td><td style="padding:6px;border:1px solid #d4c08a">Slight warmth</td><td style="padding:6px;border:1px solid #d4c08a">-20%</td></tr>
  </tbody>
</table>

<h2>Setting metal interaction</h2>
<p>Yellow gold settings <em>mask</em> body color — you can drop to J-K. White gold
or platinum reveals every degree, so don't go below H. Rose gold is forgiving
to I-J. See <a href="/blog/wedding-metals">wedding metal guide</a> for matching.</p>

<p>Read <a href="/blog/diamond-clarity">clarity next</a>, then go to the
<a href="/">calculator</a> to see how color affects your overall optical score.</p>
'''


EN['diamond-clarity'] = '''
<aside style="margin:0 0 22px;padding:16px 20px;background:linear-gradient(180deg,#fffdf7,#fbf3df);border-left:4px solid #c9a45c;border-radius:8px">
  <div style="font-size:10.5px;letter-spacing:.22em;text-transform:uppercase;color:#8a6e30;font-weight:700;margin-bottom:6px">TL;DR</div>
  Clarity grades inclusions under 10× magnification. FL-IF flawless, VVS1-VVS2
  hard to find under loupe, VS1-VS2 invisible to the naked eye, SI1-SI2 sometimes
  visible, I1-I3 visible. <strong>VS2 is the practical floor</strong> — eye-clean and 40-60% cheaper than VVS.
</aside>

<h2>The 11-grade scale</h2>
<p>FL → IF → VVS1 → VVS2 → VS1 → VS2 → SI1 → SI2 → I1 → I2 → I3.
"Eye-clean" means no inclusion visible at 25 cm in normal light. The vast
majority of VS2 and many SI1 stones are eye-clean — but you must check the
GIA plot, not just the grade.</p>

<h2>Inclusion types that matter</h2>
<ul>
  <li><strong>Crystal</strong> — most common, often white/colorless and easy to hide.</li>
  <li><strong>Feather</strong> — small fracture; check it isn't on the girdle (durability risk).</li>
  <li><strong>Cloud</strong> — group of pinpoints; large clouds dim brilliance even at SI grade.</li>
  <li><strong>Cavity / chip</strong> — surface defects; avoid in any grade.</li>
</ul>
<p>See <a href="/blog/inclusions-types-guide">the full inclusion atlas</a> with photos.</p>

<h2>Where on the stone matters</h2>
<p>An inclusion under the table is more visible than one near the girdle (hidden
by the prongs). Ask the seller for a face-up photo at 10× to verify your VS2
or SI1 reads as eye-clean. SI1 with edge-only inclusions can outperform VS2
with a center crystal.</p>

<h2>The economic answer</h2>
<p><strong>VS2 GIA</strong> for safety, <strong>SI1 GIA with eye-clean plot</strong> for value.
Anything VVS+ is paying for the loupe view nobody will ever take. Pair VS2 with
G color for the optimal price-quality knot — see <a href="/blog/diamond-color">color guide</a>
and run the numbers in the <a href="/">calculator</a>.</p>
'''


EN['diamond-carat-size'] = '''
<aside style="margin:0 0 22px;padding:16px 20px;background:linear-gradient(180deg,#fffdf7,#fbf3df);border-left:4px solid #c9a45c;border-radius:8px">
  <div style="font-size:10.5px;letter-spacing:.22em;text-transform:uppercase;color:#8a6e30;font-weight:700;margin-bottom:6px">TL;DR</div>
  Carat is weight, not size. A round 1 ct ≈ 6.5 mm, 0.7 ct ≈ 5.75 mm, 0.5 ct ≈ 5.2 mm.
  Going from 0.7 to 1.0 ct adds only ~13% diameter but ~50% price. Choose carat
  based on <em>face-up diameter</em>, not weight on paper.
</aside>

<h2>Carat-to-mm reference (round brilliant)</h2>
<table style="width:100%;border-collapse:collapse;margin:14px 0">
  <thead><tr style="background:#fbf3df"><th style="padding:6px;border:1px solid #d4c08a">Carat</th><th style="padding:6px;border:1px solid #d4c08a">Diameter</th><th style="padding:6px;border:1px solid #d4c08a">Looks like</th></tr></thead>
  <tbody>
    <tr><td style="padding:6px;border:1px solid #d4c08a">0.30 ct</td><td style="padding:6px;border:1px solid #d4c08a">4.3 mm</td><td style="padding:6px;border:1px solid #d4c08a">delicate, daily wear</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">0.50 ct</td><td style="padding:6px;border:1px solid #d4c08a">5.2 mm</td><td style="padding:6px;border:1px solid #d4c08a">classic petite</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">0.70 ct</td><td style="padding:6px;border:1px solid #d4c08a">5.75 mm</td><td style="padding:6px;border:1px solid #d4c08a">value sweet spot</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a"><strong>1.00 ct</strong></td><td style="padding:6px;border:1px solid #d4c08a"><strong>6.5 mm</strong></td><td style="padding:6px;border:1px solid #d4c08a">milestone, "real" engagement size</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">1.50 ct</td><td style="padding:6px;border:1px solid #d4c08a">7.4 mm</td><td style="padding:6px;border:1px solid #d4c08a">noticeable from across the room</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">2.00 ct</td><td style="padding:6px;border:1px solid #d4c08a">8.1 mm</td><td style="padding:6px;border:1px solid #d4c08a">statement</td></tr>
  </tbody>
</table>

<h2>Magic-number pricing cliffs</h2>
<p>Diamond prices jump at psychological round numbers: 0.50, 0.70, 0.90, 1.00,
1.50, 2.00 ct. A 0.95 ct can be 20-30% cheaper than 1.00 ct with face-up
diameter only 0.1 mm smaller. <strong>Buy "just under"</strong> (0.93, 1.45, 1.95) to
exploit this cliff — see the <a href="/blog/diamond-1ct-price-2026">2026 1-carat
price article</a> for live numbers.</p>

<h2>Spread vs depth</h2>
<p>Two 1.00 ct stones can have different face-up diameters. A "spready" cut
(shallow pavilion) looks 5-7% larger than a deep one — but trades brilliance.
Run candidates through the <a href="/">calculator</a> to verify the deeper one
isn't winning on optics. Read <a href="/blog/hearts-arrows-truth">hearts &amp;
arrows</a> for the cut-quality story.</p>
'''


EN['diamond-shapes'] = '''
<aside style="margin:0 0 22px;padding:16px 20px;background:linear-gradient(180deg,#fffdf7,#fbf3df);border-left:4px solid #c9a45c;border-radius:8px">
  <div style="font-size:10.5px;letter-spacing:.22em;text-transform:uppercase;color:#8a6e30;font-weight:700;margin-bottom:6px">TL;DR</div>
  Round brilliant accounts for ~70% of engagement diamonds for a reason —
  highest brilliance, easiest to certify, deepest market. Fancy shapes (oval,
  cushion, princess, emerald, pear) trade some sparkle for individuality and
  10-25% lower price per carat.
</aside>

<h2>The 10 shapes at a glance</h2>
<table style="width:100%;border-collapse:collapse;margin:14px 0">
  <thead><tr style="background:#fbf3df"><th style="padding:6px;border:1px solid #d4c08a">Shape</th><th style="padding:6px;border:1px solid #d4c08a">Brilliance</th><th style="padding:6px;border:1px solid #d4c08a">Best for</th></tr></thead>
  <tbody>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Round</td><td style="padding:6px;border:1px solid #d4c08a">★★★★★</td><td style="padding:6px;border:1px solid #d4c08a">Maximum sparkle, classic</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Oval</td><td style="padding:6px;border:1px solid #d4c08a">★★★★☆</td><td style="padding:6px;border:1px solid #d4c08a">Elongates fingers, looks 10% larger</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Cushion</td><td style="padding:6px;border:1px solid #d4c08a">★★★★☆</td><td style="padding:6px;border:1px solid #d4c08a">Vintage, soft glow</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Princess</td><td style="padding:6px;border:1px solid #d4c08a">★★★★☆</td><td style="padding:6px;border:1px solid #d4c08a">Modern, square face-up</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Emerald</td><td style="padding:6px;border:1px solid #d4c08a">★★★☆☆</td><td style="padding:6px;border:1px solid #d4c08a">Hall-of-mirrors look, art deco</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Pear</td><td style="padding:6px;border:1px solid #d4c08a">★★★★☆</td><td style="padding:6px;border:1px solid #d4c08a">Unique, slimming finger</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Marquise</td><td style="padding:6px;border:1px solid #d4c08a">★★★★☆</td><td style="padding:6px;border:1px solid #d4c08a">Largest face-up per carat</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Asscher</td><td style="padding:6px;border:1px solid #d4c08a">★★★☆☆</td><td style="padding:6px;border:1px solid #d4c08a">Square emerald, vintage</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Radiant</td><td style="padding:6px;border:1px solid #d4c08a">★★★★☆</td><td style="padding:6px;border:1px solid #d4c08a">Brilliant facets in rectangular outline</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Heart</td><td style="padding:6px;border:1px solid #d4c08a">★★★☆☆</td><td style="padding:6px;border:1px solid #d4c08a">Symbol pieces; 1ct+ recommended</td></tr>
  </tbody>
</table>

<h2>Step-cut vs brilliant-cut</h2>
<p><strong>Brilliant cuts</strong> (round, oval, cushion, pear, marquise, princess, radiant)
have triangular facets that scatter light into many small flashes — high
sparkle, hides inclusions. <strong>Step cuts</strong> (emerald, asscher, baguette) have
parallel rectangular facets producing wide, mirror-like flashes — elegant but
require higher clarity (VS1+).</p>

<h2>Shape-specific buying tips</h2>
<ul>
  <li><strong>Oval &amp; pear</strong> — watch for a "bow-tie" dark shadow across the center.</li>
  <li><strong>Princess</strong> — protect sharp corners with V-prongs.</li>
  <li><strong>Emerald</strong> — buy color G+ and clarity VS1+ (open table reveals everything).</li>
  <li><strong>Marquise</strong> — verify symmetry; lopsided ones look cheap.</li>
</ul>

<p>Round on a budget? Look at <a href="/blog/round-cut-deep-dive">the deep dive</a>.
Want a different shape? Read <a href="/blog/fancy-cuts-guide">the fancy-cuts
guide</a>. Then run your candidate through the <a href="/">calculator</a>.</p>
'''


EN['cert-comparison'] = '''
<aside style="margin:0 0 22px;padding:16px 20px;background:linear-gradient(180deg,#fffdf7,#fbf3df);border-left:4px solid #c9a45c;border-radius:8px">
  <div style="font-size:10.5px;letter-spacing:.22em;text-transform:uppercase;color:#8a6e30;font-weight:700;margin-bottom:6px">TL;DR</div>
  GIA is the strictest and most universally trusted. IGI dominates the lab-grown
  market. HRD and AGS are credible alternatives. EGL and "in-house" reports are
  notoriously soft — discount the grade by 1-2 levels.
</aside>

<h2>The big four labs</h2>
<table style="width:100%;border-collapse:collapse;margin:14px 0">
  <thead><tr style="background:#fbf3df"><th style="padding:6px;border:1px solid #d4c08a">Lab</th><th style="padding:6px;border:1px solid #d4c08a">Strictness</th><th style="padding:6px;border:1px solid #d4c08a">Strongest in</th></tr></thead>
  <tbody>
    <tr><td style="padding:6px;border:1px solid #d4c08a"><strong>GIA</strong></td><td style="padding:6px;border:1px solid #d4c08a">Reference</td><td style="padding:6px;border:1px solid #d4c08a">Natural diamonds, global</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">AGS</td><td style="padding:6px;border:1px solid #d4c08a">≥ GIA on cut</td><td style="padding:6px;border:1px solid #d4c08a">Light performance reports (now part of GIA)</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">HRD</td><td style="padding:6px;border:1px solid #d4c08a">≈ GIA</td><td style="padding:6px;border:1px solid #d4c08a">Antwerp / Europe market</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">IGI</td><td style="padding:6px;border:1px solid #d4c08a">~ 0.5 grade looser</td><td style="padding:6px;border:1px solid #d4c08a">Lab-grown, India market</td></tr>
  </tbody>
</table>

<h2>Read GIA before everything</h2>
<p>For natural diamonds, <strong>insist on GIA</strong>. The grade-to-grade discount for
non-GIA paper is real (5-15%) but the resale and trade-in penalty is much worse.
A GIA-graded stone is liquid; a non-GIA stone trades back at 30-50%. Read
<a href="/blog/gia-guide">how to read a GIA report</a> for the format walkthrough.</p>

<h2>For lab-grown: IGI is fine</h2>
<p>IGI dominates lab-grown certification because it built the workflow first.
The grading is consistent within IGI lab-grown reports and the digital format
is QR-verifiable. GIA also grades lab-grown but at a premium price.</p>

<h2>Avoid soft labs</h2>
<p>EGL (especially EGL International) and many "in-house" or jeweller-issued
"appraisals" routinely run 1-2 grades looser. A "EGL F-VS2" is realistically
"GIA H-SI1". Discount the asking price accordingly or refuse.</p>

<p>Verify your report at the lab's official site before purchase. See
<a href="/blog/diamond-scams">the scams article</a> for fake-cert recognition.</p>
'''


EN['hearts-arrows-truth'] = '''
<aside style="margin:0 0 22px;padding:16px 20px;background:linear-gradient(180deg,#fffdf7,#fbf3df);border-left:4px solid #c9a45c;border-radius:8px">
  <div style="font-size:10.5px;letter-spacing:.22em;text-transform:uppercase;color:#8a6e30;font-weight:700;margin-bottom:6px">TL;DR</div>
  "Hearts &amp; Arrows" is a precision benchmark above GIA Excellent — only ~5%
  of round Excellents qualify. The visual pattern (8 hearts under, 8 arrows
  over) is proof of optical symmetry, not marketing.
</aside>

<h2>What is Hearts &amp; Arrows?</h2>
<p>When viewed through an H&amp;A scope from the pavilion side, an ideally cut
round shows 8 perfectly shaped hearts. From the table side, 8 arrows. This
pattern only forms when crown angle, pavilion angle, and facet azimuth are
within ±0.2° of Tolkowsky's ideal. The math is binary: in or out.</p>

<h2>Why GIA Excellent isn't enough</h2>
<p>GIA Excellent allows table 53-58%, depth 60.5-62.5%, crown 31-37°,
pavilion 40.6-41.8°. The <em>edge</em> of Excellent (table 58, crown 37, pavilion
41.8) measurably leaks light — our calculator scores it 25% below the
center-of-Excellent (table 56, crown 34.5, pavilion 41).</p>

<h2>How to verify</h2>
<ol>
  <li>Ask for an <strong>ASET</strong> or <strong>Ideal-Scope</strong> image.</li>
  <li>Look for 8 hearts symmetrical and centered (no split heart bases).</li>
  <li>Confirm proportions: table 55-57%, depth 60.5-62%, crown 34-35°, pavilion 40.6-41°.</li>
  <li>Run the four numbers through the <a href="/">BrillianceLab calculator</a> — true H&amp;A scores 92+.</li>
</ol>

<h2>Is the H&amp;A premium worth it?</h2>
<p>True H&amp;A trades at a 15-25% premium over edge-Excellent. For a 1 ct, that's
roughly NT$30-50K. If your budget allows it, yes — the visible difference is
significant. If not, prioritise center-Excellent proportions over the pattern
itself. Read <a href="/blog/budget-formula">the budget formula</a> for the math.</p>
'''


EN['lab-vs-natural'] = '''
<aside style="margin:0 0 22px;padding:16px 20px;background:linear-gradient(180deg,#fffdf7,#fbf3df);border-left:4px solid #c9a45c;border-radius:8px">
  <div style="font-size:10.5px;letter-spacing:.22em;text-transform:uppercase;color:#8a6e30;font-weight:700;margin-bottom:6px">TL;DR</div>
  Lab-grown diamonds are chemically identical to natural — same C, same lattice,
  same hardness, same optics. Price is now 70-80% lower. The remaining
  arguments are emotional (provenance, resale) — not optical.
</aside>

<h2>Same crystal, different origin</h2>
<p>Both natural and lab-grown diamonds are pure carbon in cubic crystal lattice.
A trained gemologist cannot tell them apart by eye, by loupe, or by fire.
Specialised instruments (DiamondView fluorescence, Raman spectroscopy) detect
the trace nitrogen / Si patterns of growth chambers — but only labs run those
tests. To you and your fiancée, identical.</p>

<h2>The price collapse</h2>
<p>Lab-grown diamond wholesale prices fell ~85% from 2018-2025 as HPHT and
CVD capacity scaled. A 1 ct G-VS2 lab is now ~NT$30-50K vs ~NT$180-250K
natural — same stone, 70% off. See <a href="/blog/diamond-price-trends">price
trends</a> for the full curve.</p>

<h2>The emotional case for natural</h2>
<ul>
  <li><strong>Provenance</strong> — billion-year geological story is real.</li>
  <li><strong>Scarcity</strong> — finite supply (until lab capacity floods).</li>
  <li><strong>Resale</strong> — natural retains 30-40% trade-in; lab is closer to 5-10%.</li>
</ul>

<h2>The case for lab</h2>
<ul>
  <li><strong>3-4× the size</strong> for the same budget.</li>
  <li><strong>No conflict-zone risk</strong> (and natural Kimberley Process has gaps).</li>
  <li><strong>Smaller environmental footprint</strong> (depending on grid mix).</li>
</ul>

<h2>The honest answer</h2>
<p>If you want maximum sparkle for your budget, buy lab. If you want a stone you
can trade or pass down with stable value, buy natural. Both are real diamonds.
Read <a href="/blog/sustainable-diamonds">the sustainability deep-dive</a> and
the <a href="/blog/diamond-faq">FAQ</a> for nuance.</p>
'''


EN['budget-formula'] = '''
<aside style="margin:0 0 22px;padding:16px 20px;background:linear-gradient(180deg,#fffdf7,#fbf3df);border-left:4px solid #c9a45c;border-radius:8px">
  <div style="font-size:10.5px;letter-spacing:.22em;text-transform:uppercase;color:#8a6e30;font-weight:700;margin-bottom:6px">TL;DR</div>
  Forget "3 months' salary" — that was 1947 De Beers ad copy. The real budget
  formula: <strong>BPD = (optical score × √carat) / price</strong>. Maximise BPD
  under your hard cap and you've found the optimal stone.
</aside>

<h2>Why "3 months' salary" is wrong</h2>
<p>The figure was invented by N.W. Ayer for De Beers in the 1940s and bumped to
"2 months" then "3 months" through the 1980s as commission-driven marketing.
There is no relationship between your salary and the optimal stone size.
The optimal stone is the one that maximises perceived sparkle within your
hard budget — measurable, not emotional.</p>

<h2>The BPD formula</h2>
<p><strong>BPD = (Optical Score × √Carat) ÷ Price (NT$1000)</strong></p>
<p>Why √carat? Because face-up area scales with the square of diameter, and
diameter scales with the cube root of weight, so visual impact scales roughly
with √(weight). Optical score (0-100) comes from the
<a href="/">calculator</a> — it captures the 4-dim cut analysis (light return,
fire, scintillation, spread).</p>

<h2>Worked example</h2>
<table style="width:100%;border-collapse:collapse;margin:14px 0">
  <thead><tr style="background:#fbf3df"><th style="padding:6px;border:1px solid #d4c08a">Stone</th><th style="padding:6px;border:1px solid #d4c08a">Score</th><th style="padding:6px;border:1px solid #d4c08a">Carat</th><th style="padding:6px;border:1px solid #d4c08a">Price (k)</th><th style="padding:6px;border:1px solid #d4c08a">BPD</th></tr></thead>
  <tbody>
    <tr><td style="padding:6px;border:1px solid #d4c08a">A: 1ct GIA-EX edge</td><td style="padding:6px;border:1px solid #d4c08a">76</td><td style="padding:6px;border:1px solid #d4c08a">1.00</td><td style="padding:6px;border:1px solid #d4c08a">220</td><td style="padding:6px;border:1px solid #d4c08a">0.345</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">B: 0.95ct H&amp;A</td><td style="padding:6px;border:1px solid #d4c08a">94</td><td style="padding:6px;border:1px solid #d4c08a">0.95</td><td style="padding:6px;border:1px solid #d4c08a">195</td><td style="padding:6px;border:1px solid #d4c08a"><strong>0.470</strong></td></tr>
  </tbody>
</table>
<p>B wins on BPD by 36% despite being 0.05 ct smaller and "only" 6% cheaper —
because the score gap is huge.</p>

<h2>Putting it to work</h2>
<p>Set your hard cap (NT$200K, NT$300K, etc.). Pull 5-10 candidates from
<a href="/blog/taiwan-brands">Taiwan brands</a> in your price range. Compute
BPD for each. Buy the highest. Don't haggle over 5%; haggle over 35% BPD gaps.</p>
'''


EN['fluorescence-deep-dive'] = '''
<aside style="margin:0 0 22px;padding:16px 20px;background:linear-gradient(180deg,#fffdf7,#fbf3df);border-left:4px solid #c9a45c;border-radius:8px">
  <div style="font-size:10.5px;letter-spacing:.22em;text-transform:uppercase;color:#8a6e30;font-weight:700;margin-bottom:6px">TL;DR</div>
  ~30% of diamonds glow blue under UV. For G-J colors, Medium Blue
  fluorescence <em>improves</em> face-up appearance and saves 5-10% on price.
  Avoid only Strong/Very Strong on D-F (potential haziness).
</aside>

<h2>What is fluorescence?</h2>
<p>Trace nitrogen clusters in the diamond lattice absorb UV and re-emit visible
light. Most fluorescence is blue. GIA grades it: None / Faint / Medium /
Strong / Very Strong, and notes color (almost always Blue).</p>

<h2>The myth and the reality</h2>
<p>The trade discounts fluorescent stones because of a 1990s rumor that strong
fluorescence makes diamonds look "milky" or "oily". GIA's own 1997 study
showed: untrained observers <em>preferred</em> fluorescent stones in 99% of
side-by-side comparisons. The "milky" effect is real but rare — limited to
~3% of Strong+ stones.</p>

<h2>Color × fluorescence matrix</h2>
<table style="width:100%;border-collapse:collapse;margin:14px 0">
  <thead><tr style="background:#fbf3df"><th style="padding:6px;border:1px solid #d4c08a">Color</th><th style="padding:6px;border:1px solid #d4c08a">Best fluorescence</th><th style="padding:6px;border:1px solid #d4c08a">Why</th></tr></thead>
  <tbody>
    <tr><td style="padding:6px;border:1px solid #d4c08a">D-F</td><td style="padding:6px;border:1px solid #d4c08a">None / Faint</td><td style="padding:6px;border:1px solid #d4c08a">Already colorless; risk haze</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a"><strong>G-J</strong></td><td style="padding:6px;border:1px solid #d4c08a"><strong>Medium / Strong Blue</strong></td><td style="padding:6px;border:1px solid #d4c08a">Blue cancels yellow tint, looks whiter</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">K+</td><td style="padding:6px;border:1px solid #d4c08a">Strong Blue</td><td style="padding:6px;border:1px solid #d4c08a">Big visual upgrade</td></tr>
  </tbody>
</table>

<h2>The pricing arbitrage</h2>
<p>A G-VS2 with Medium Blue fluorescence trades 5-10% below a non-fluorescent
twin — same paper, same look (or better). On a NT$200K stone, that's NT$10-20K
saved. Always view the stone in person under daylight before buying — the
~3% milky risk is verifiable in 30 seconds.</p>

<p>Read <a href="/blog/diamond-color">the color guide</a> for the matching
strategy and <a href="/blog/gia-guide">how to spot fluorescence</a> on a GIA
report (Page 2, lower-right block).</p>
'''


EN['inclusions-types-guide'] = '''
<aside style="margin:0 0 22px;padding:16px 20px;background:linear-gradient(180deg,#fffdf7,#fbf3df);border-left:4px solid #c9a45c;border-radius:8px">
  <div style="font-size:10.5px;letter-spacing:.22em;text-transform:uppercase;color:#8a6e30;font-weight:700;margin-bottom:6px">TL;DR</div>
  Not all VS2 inclusions are equal. Crystals and feathers near the girdle hide
  under prongs; clouds under the table dim brilliance even at SI grade. Always
  read the GIA plot, not just the letter grade.
</aside>

<h2>The 12 inclusion types</h2>
<ul>
  <li><strong>Crystal</strong> — embedded mineral, most common. Color-grade matters: white crystals hide better than dark.</li>
  <li><strong>Pinpoint</strong> — single tiny crystal, often invisible to eye.</li>
  <li><strong>Cloud</strong> — group of pinpoints. Large clouds look hazy; small clouds invisible.</li>
  <li><strong>Feather</strong> — internal fracture. Safe if small &amp; not on girdle.</li>
  <li><strong>Needle</strong> — long thin crystal. Hard to see face-up.</li>
  <li><strong>Knot</strong> — crystal that reaches the surface. Avoid.</li>
  <li><strong>Cavity</strong> — surface dip. Catches dirt; avoid.</li>
  <li><strong>Chip</strong> — small surface break. Reflects ugly; avoid.</li>
  <li><strong>Indented natural</strong> — original crystal skin recess on girdle. Acceptable.</li>
  <li><strong>Bruise</strong> — impact site, often with feather. Acceptable if small.</li>
  <li><strong>Twinning wisp</strong> — wavy growth ribbons. Often invisible, can dim brilliance if dense.</li>
  <li><strong>Etch channel</strong> — straight tube from natural acid attack. Cosmetic.</li>
</ul>

<h2>Position matters more than count</h2>
<p>An SI1 with one inclusion under the prong can be eye-clean; a VS2 with a
crystal directly under the table can be visible. <strong>Buy by photo, not by
grade.</strong> Ask the seller for a 10× face-up photo and a side-photo before
purchase.</p>

<h2>Avoid these no matter the grade</h2>
<ul>
  <li>Surface-reaching feather on the girdle (durability risk during setting).</li>
  <li>Knot or chip anywhere.</li>
  <li>Dark crystal directly under the table.</li>
  <li>Dense twinning wisps reading as "haze" face-up.</li>
</ul>

<p>See the <a href="/blog/diamond-clarity">clarity guide</a> for the grading
scale and <a href="/blog/gia-guide">GIA plot reading</a> for which symbol is
which on the report.</p>
'''


# ─────────────────────────────────────────────────────────────────
# Round 14 — Purchase / brands / scams (10)
# ─────────────────────────────────────────────────────────────────

EN['engagement-guide'] = '''
<aside style="margin:0 0 22px;padding:16px 20px;background:linear-gradient(180deg,#fffdf7,#fbf3df);border-left:4px solid #c9a45c;border-radius:8px">
  <div style="font-size:10.5px;letter-spacing:.22em;text-transform:uppercase;color:#8a6e30;font-weight:700;margin-bottom:6px">TL;DR</div>
  9-step engagement ring playbook: budget → ring style → 4Cs → cert lab →
  shortlist 3 stones → in-person view → compute BPD → negotiate → buy.
  Total elapsed time: 2-4 weeks if you start with a clear budget.
</aside>

<h2>The 9 steps</h2>
<ol>
  <li><strong>Set a hard budget cap.</strong> Not "around X", a number. NT$150K, NT$250K, NT$400K.</li>
  <li><strong>Pick a ring style.</strong> Solitaire, halo, three-stone, bezel, vintage. See <a href="/blog/prong-settings-guide">prong settings</a>.</li>
  <li><strong>Get her ring size.</strong> Borrow an existing ring or use the <a href="/blog/ring-sizing">ring sizing guide</a>.</li>
  <li><strong>Decide natural vs lab.</strong> Read <a href="/blog/lab-vs-natural">the comparison</a>; lab is 70% cheaper at the same look.</li>
  <li><strong>Lock the 4Cs.</strong> Default: G color / VS2 clarity / 0.7-1.0 ct / Excellent cut. Adjust per <a href="/blog/budget-formula">BPD formula</a>.</li>
  <li><strong>Insist on GIA.</strong> Or IGI for lab-grown. Read <a href="/blog/cert-comparison">the cert guide</a>.</li>
  <li><strong>Shortlist 3 stones.</strong> From 2-3 vendors. Get GIA numbers; run them through <a href="/">the calculator</a>.</li>
  <li><strong>View in person.</strong> Daylight + indoor. Verify no haze (fluorescence check) and eye-clean.</li>
  <li><strong>Negotiate &amp; buy.</strong> 5-10% off list is normal in Taiwan. Get a written certificate, appraisal, return policy.</li>
</ol>

<h2>Common pitfalls</h2>
<ul>
  <li>Buying brand-name first, stone second — paying 2-4× for a logo. See <a href="/blog/taiwan-brands">brand tier comparison</a>.</li>
  <li>Falling for "GIA Excellent" without checking proportions — read <a href="/blog/hearts-arrows-truth">H&amp;A truth</a>.</li>
  <li>Ignoring resale — see <a href="/blog/diamond-resale">the resale article</a>.</li>
  <li>Forgetting insurance — see <a href="/blog/ring-insurance">ring insurance</a>.</li>
</ul>

<h2>Timeline</h2>
<p>Allow 2-4 weeks for research + viewing + setting (if custom). For a stock
ring you can buy and walk out same day, but custom mounting adds 1-2 weeks.
Time the proposal accordingly. See <a href="/blog/proposal-speech">the
proposal speech guide</a> for what comes next.</p>
'''


EN['diamond-scams'] = '''
<aside style="margin:0 0 22px;padding:16px 20px;background:linear-gradient(180deg,#fffdf7,#fbf3df);border-left:4px solid #c9a45c;border-radius:8px">
  <div style="font-size:10.5px;letter-spacing:.22em;text-transform:uppercase;color:#8a6e30;font-weight:700;margin-bottom:6px">TL;DR</div>
  The 10 most common diamond scams in 2026: switched stones, fake certs, soft
  labs, "investment grade" pitches, lab-as-natural, undisclosed treatments,
  inflated retail "discount", night-market loose stones, fake H&amp;A claims,
  and 4-prong "phantom" weight tricks.
</aside>

<h2>The top 10 scams</h2>
<ol>
  <li><strong>Stone switching</strong> — you bring in a stone for cleaning; you get a CZ back. Always insist on cleaning while watching, or insure first.</li>
  <li><strong>Fake or altered GIA certs</strong> — verify the report number at gia.edu/report-check. The number must match the stone's laser inscription.</li>
  <li><strong>Soft lab certs</strong> — EGL, in-house "appraisals", or "international" labs grading 1-2 levels loose. See <a href="/blog/cert-comparison">cert comparison</a>.</li>
  <li><strong>"Investment grade" pitch</strong> — diamonds are a lousy investment. Resale is 30-40% of retail. See <a href="/blog/diamond-resale">resale truth</a>.</li>
  <li><strong>Lab passed off as natural</strong> — lab-grown stones sold without disclosure. Insist on GIA paper that explicitly states "natural".</li>
  <li><strong>Undisclosed HPHT/laser treatments</strong> — color enhancement or fracture filling not disclosed. GIA reports list treatments; check.</li>
  <li><strong>Fake retail "discount"</strong> — "75% off list price!" Real wholesale is 30-50% under retail; deeper "discounts" usually mean inflated list.</li>
  <li><strong>Night-market loose stones</strong> — moissanite, white sapphire, or CZ sold as "wholesale diamond". Walk away.</li>
  <li><strong>Fake Hearts &amp; Arrows</strong> — H&amp;A claimed without ASET image proof. See <a href="/blog/hearts-arrows-truth">H&amp;A truth</a>.</li>
  <li><strong>Phantom weight</strong> — heavy crowns or extra-deep pavilions raise carat weight without raising face-up size. Check spread vs depth.</li>
</ol>

<h2>How to protect yourself</h2>
<ul>
  <li>Always GIA, always verified at gia.edu.</li>
  <li>Cross-quote with at least 2 vendors (and one online).</li>
  <li>Run proportions through <a href="/">the calculator</a> before paying.</li>
  <li>Pay by credit card (chargeback protection).</li>
  <li>Insist on a written 7-day no-questions return.</li>
  <li>Get an independent appraisal within 48 hours.</li>
</ul>

<p>For brand selection, read <a href="/blog/taiwan-brands">the Taiwan brand
tier guide</a>. For the second-hand market, see <a href="/blog/secondhand-rings">
secondhand rings</a>.</p>
'''


EN['diamond-resale'] = '''
<aside style="margin:0 0 22px;padding:16px 20px;background:linear-gradient(180deg,#fffdf7,#fbf3df);border-left:4px solid #c9a45c;border-radius:8px">
  <div style="font-size:10.5px;letter-spacing:.22em;text-transform:uppercase;color:#8a6e30;font-weight:700;margin-bottom:6px">TL;DR</div>
  A NT$300K diamond ring trades back at NT$80-120K — a 60-75% loss. The "loss"
  is mostly retail markup + setting work + emotion. The stone alone holds 30-40%
  of retail. Buy for love, not investment.
</aside>

<h2>Where the value goes</h2>
<table style="width:100%;border-collapse:collapse;margin:14px 0">
  <thead><tr style="background:#fbf3df"><th style="padding:6px;border:1px solid #d4c08a">Component</th><th style="padding:6px;border:1px solid #d4c08a">% of retail</th><th style="padding:6px;border:1px solid #d4c08a">Resale recovery</th></tr></thead>
  <tbody>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Loose stone</td><td style="padding:6px;border:1px solid #d4c08a">~50%</td><td style="padding:6px;border:1px solid #d4c08a">~70% of stone wholesale = ~25-30% of retail</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Setting (metal + labor)</td><td style="padding:6px;border:1px solid #d4c08a">~10%</td><td style="padding:6px;border:1px solid #d4c08a">Metal scrap value only ~3%</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Brand markup</td><td style="padding:6px;border:1px solid #d4c08a">~25%</td><td style="padding:6px;border:1px solid #d4c08a">~0%</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Retailer margin</td><td style="padding:6px;border:1px solid #d4c08a">~15%</td><td style="padding:6px;border:1px solid #d4c08a">~0%</td></tr>
  </tbody>
</table>

<h2>Channels and recovery rates</h2>
<ul>
  <li><strong>Auction (Christie's/Sotheby's)</strong> — best for 2 ct+ certified stones; 30-50% of original retail after fees.</li>
  <li><strong>Trade-in at original retailer</strong> — usually only against a higher-priced new ring; 40-60% credit, but you spend more.</li>
  <li><strong>Diamond buyback service (e.g. Worthy)</strong> — 25-40% of retail; convenience trade-off.</li>
  <li><strong>Pawn shop</strong> — 10-20%. Avoid.</li>
  <li><strong>Private sale (Carousell/Yahoo)</strong> — 35-50% if you can find a buyer; takes weeks.</li>
</ul>

<h2>Lab-grown resale is much worse</h2>
<p>Lab-grown wholesale is collapsing ~10% per year. A 2024 lab stone bought
for NT$60K trades back for NT$5-10K today. If resale matters, buy natural.</p>

<h2>The honest investment math</h2>
<p>From 1980-2024, natural diamond wholesale grew ~3% annually — below inflation.
A "diamond as investment" pitch ignores the 50% retail markup you can never
recover. Buy for love and lifestyle. For investment, buy gold or stocks. See
<a href="/blog/diamond-vs-gold">the gold comparison</a>.</p>
'''


EN['diamond-financing'] = '''
<aside style="margin:0 0 22px;padding:16px 20px;background:linear-gradient(180deg,#fffdf7,#fbf3df);border-left:4px solid #c9a45c;border-radius:8px">
  <div style="font-size:10.5px;letter-spacing:.22em;text-transform:uppercase;color:#8a6e30;font-weight:700;margin-bottom:6px">TL;DR</div>
  In Taiwan, ring financing usually means 12-24 month installment at 0% APR
  through the jeweller (real cost is hidden in price). Pay cash for negotiating
  power; only finance if the 0% is genuinely free and you have the cash sitting safely.
</aside>

<h2>Taiwan financing options</h2>
<ul>
  <li><strong>Jeweller installment plan</strong> — 6-24 months, advertised 0%. Reality: discount of 5-8% typically goes away if you finance.</li>
  <li><strong>Credit card installment</strong> — 3-24 months. Bank may charge handling fee (1-3% of total). Often passable for cash-back rewards.</li>
  <li><strong>Personal loan</strong> — last resort. Rates 8-15% APR; interest on a depreciating asset is bad math.</li>
</ul>

<h2>The "0%" trick</h2>
<p>Many "0% 24-month" plans embed a 5-10% retailer kickback in the sticker
price. Ask: "what's your cash price?" If the cash price is NT$285K and the
financed price is NT$300K, your "0%" is actually 5.3% over 1 year (~10.6% APR).
Always negotiate <em>both</em> the price and the financing.</p>

<h2>Should you finance an engagement ring?</h2>
<ul>
  <li><strong>If you have the cash and 0% is real</strong> — yes, keep your cash earning interest.</li>
  <li><strong>If you don't have the cash</strong> — buy a smaller ring. Going into debt for a ring is a bad start to a marriage.</li>
  <li><strong>If financing carries any interest</strong> — almost never worth it.</li>
</ul>

<h2>Smarter alternatives</h2>
<ul>
  <li><strong>Buy under-magic numbers</strong> (0.95 vs 1.00 ct) — see <a href="/blog/diamond-1ct-price-2026">1ct price article</a>.</li>
  <li><strong>Choose lab-grown</strong> — 70% cheaper at same look. See <a href="/blog/lab-vs-natural">comparison</a>.</li>
  <li><strong>Buy from value-tier brands</strong> — see <a href="/blog/taiwan-brands">brand tiers</a>.</li>
  <li><strong>Plan an upgrade later</strong> — many jewellers credit 100% of original stone toward future trade-up.</li>
</ul>
'''


EN['diamond-price-trends'] = '''
<aside style="margin:0 0 22px;padding:16px 20px;background:linear-gradient(180deg,#fffdf7,#fbf3df);border-left:4px solid #c9a45c;border-radius:8px">
  <div style="font-size:10.5px;letter-spacing:.22em;text-transform:uppercase;color:#8a6e30;font-weight:700;margin-bottom:6px">TL;DR</div>
  2020-2026 diamond prices: natural 1ct dropped ~28% from peak (2022 H1).
  Lab-grown collapsed ~85% over same period. De Beers split, India layoffs,
  and 50%+ lab market share define the new normal.
</aside>

<h2>The 5-year picture</h2>
<table style="width:100%;border-collapse:collapse;margin:14px 0">
  <thead><tr style="background:#fbf3df"><th style="padding:6px;border:1px solid #d4c08a">Year</th><th style="padding:6px;border:1px solid #d4c08a">Natural 1ct G-VS2 (NT$)</th><th style="padding:6px;border:1px solid #d4c08a">Lab 1ct G-VS2 (NT$)</th></tr></thead>
  <tbody>
    <tr><td style="padding:6px;border:1px solid #d4c08a">2020</td><td style="padding:6px;border:1px solid #d4c08a">200K</td><td style="padding:6px;border:1px solid #d4c08a">120K</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">2022 H1 (peak)</td><td style="padding:6px;border:1px solid #d4c08a">280K</td><td style="padding:6px;border:1px solid #d4c08a">90K</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">2024</td><td style="padding:6px;border:1px solid #d4c08a">220K</td><td style="padding:6px;border:1px solid #d4c08a">50K</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">2026</td><td style="padding:6px;border:1px solid #d4c08a">200K</td><td style="padding:6px;border:1px solid #d4c08a">35K</td></tr>
  </tbody>
</table>

<h2>What's driving the trend</h2>
<ul>
  <li><strong>Lab-grown supply explosion</strong> — Indian CVD capacity grew 8× from 2018-2024.</li>
  <li><strong>De Beers strategic split</strong> — Anglo American spun off De Beers in 2025; rough sales discipline weakening.</li>
  <li><strong>India polishing layoffs</strong> — 200K+ jobs lost in Surat 2023-2024 reflect natural demand softness.</li>
  <li><strong>Lab now ~50% of US engagement market</strong> by units, ~30% by value.</li>
  <li><strong>China demand stagnation</strong> — economic slowdown removed marginal buyers.</li>
</ul>

<h2>Where prices go from here</h2>
<p>Our base case: natural 1 ct G-VS2 holds NT$190-220K through 2027 (some
support from supply discipline). Lab continues falling 8-12% per year toward
the marginal cost of CVD production (~NT$15K for 1 ct by 2028).</p>

<h2>Buy or wait?</h2>
<p>Lab: waiting is rational — you'll pay less in 6 months. Natural: prices
are roughly stable; buy when you need to. See <a href="/blog/diamond-1ct-price-2026">
the 2026 1-carat detail</a> and <a href="/blog/lab-vs-natural">lab vs natural</a>.</p>
'''


EN['diamond-vs-gold'] = '''
<aside style="margin:0 0 22px;padding:16px 20px;background:linear-gradient(180deg,#fffdf7,#fbf3df);border-left:4px solid #c9a45c;border-radius:8px">
  <div style="font-size:10.5px;letter-spacing:.22em;text-transform:uppercase;color:#8a6e30;font-weight:700;margin-bottom:6px">TL;DR</div>
  Gold is liquid, fungible, and tracks inflation. Diamonds are illiquid, unique,
  and lose 60-70% on resale. As an investment, gold wins. As an emotional
  symbol, diamonds win. Don't confuse the two.
</aside>

<h2>Side-by-side</h2>
<table style="width:100%;border-collapse:collapse;margin:14px 0">
  <thead><tr style="background:#fbf3df"><th style="padding:6px;border:1px solid #d4c08a">Dimension</th><th style="padding:6px;border:1px solid #d4c08a">Gold</th><th style="padding:6px;border:1px solid #d4c08a">Diamond</th></tr></thead>
  <tbody>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Liquidity</td><td style="padding:6px;border:1px solid #d4c08a">Daily quotes; cash-out in 24h</td><td style="padding:6px;border:1px solid #d4c08a">Weeks-months to sell</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Resale recovery</td><td style="padding:6px;border:1px solid #d4c08a">95-98% of spot</td><td style="padding:6px;border:1px solid #d4c08a">25-40% of retail</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">15-yr CAGR</td><td style="padding:6px;border:1px solid #d4c08a">~7%</td><td style="padding:6px;border:1px solid #d4c08a">~3% (natural); negative (lab)</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Inflation hedge</td><td style="padding:6px;border:1px solid #d4c08a">Strong</td><td style="padding:6px;border:1px solid #d4c08a">Weak</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Wearability</td><td style="padding:6px;border:1px solid #d4c08a">High; jewellery + bullion</td><td style="padding:6px;border:1px solid #d4c08a">High; emotional</td></tr>
  </tbody>
</table>

<h2>Taiwan context</h2>
<p>Taiwanese savers historically buy gold as a wealth store — bank gold passbooks,
gold bars, gold jewellery. Diamond ownership is for milestone events
(engagement, anniversary). The two serve different mental accounts.</p>

<h2>If you must choose only one wedding metal</h2>
<p>For engagement: a 1 ct natural diamond + plain platinum band beats any
"all-gold" alternative on emotional impact. For wealth-storage anniversary
gifts: 24K gold pendants beat colored stones. See <a href="/blog/wedding-metals">
the metal guide</a>.</p>

<p>Investment-minded? Read <a href="/blog/diamond-resale">the resale article</a> —
the math is brutal.</p>
'''


EN['ring-sizing'] = '''
<aside style="margin:0 0 22px;padding:16px 20px;background:linear-gradient(180deg,#fffdf7,#fbf3df);border-left:4px solid #c9a45c;border-radius:8px">
  <div style="font-size:10.5px;letter-spacing:.22em;text-transform:uppercase;color:#8a6e30;font-weight:700;margin-bottom:6px">TL;DR</div>
  Ring size in Taiwan uses Hong Kong (HK) numbering 1-30. Average bride: HK 10-13.
  Measure 3 times across the day (size changes ±1 with temperature). Buy 0.5
  size larger if proposing as a surprise — easier to size down than up.
</aside>

<h2>Three ways to measure</h2>
<ol>
  <li><strong>Borrow an existing ring</strong> — take it to any jeweller; they'll size it free in 30 seconds. Most accurate.</li>
  <li><strong>Wrap a string</strong> around her finger at the base, mark the overlap, measure mm. Divide by π (3.14) for diameter, look up HK size.</li>
  <li><strong>Print a sizing chart</strong> — many jeweller sites offer PDF templates. Accuracy ±1 size.</li>
</ol>

<h2>Quick reference (HK ↔ mm)</h2>
<table style="width:100%;border-collapse:collapse;margin:14px 0">
  <thead><tr style="background:#fbf3df"><th style="padding:6px;border:1px solid #d4c08a">HK</th><th style="padding:6px;border:1px solid #d4c08a">Inner diameter</th><th style="padding:6px;border:1px solid #d4c08a">US</th><th style="padding:6px;border:1px solid #d4c08a">EU</th></tr></thead>
  <tbody>
    <tr><td style="padding:6px;border:1px solid #d4c08a">8</td><td style="padding:6px;border:1px solid #d4c08a">15.7 mm</td><td style="padding:6px;border:1px solid #d4c08a">5</td><td style="padding:6px;border:1px solid #d4c08a">49</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">10</td><td style="padding:6px;border:1px solid #d4c08a">16.5 mm</td><td style="padding:6px;border:1px solid #d4c08a">6</td><td style="padding:6px;border:1px solid #d4c08a">52</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a"><strong>12</strong></td><td style="padding:6px;border:1px solid #d4c08a"><strong>17.3 mm</strong></td><td style="padding:6px;border:1px solid #d4c08a">7</td><td style="padding:6px;border:1px solid #d4c08a">54</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">14</td><td style="padding:6px;border:1px solid #d4c08a">18.2 mm</td><td style="padding:6px;border:1px solid #d4c08a">8</td><td style="padding:6px;border:1px solid #d4c08a">57</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">16</td><td style="padding:6px;border:1px solid #d4c08a">19.0 mm</td><td style="padding:6px;border:1px solid #d4c08a">9</td><td style="padding:6px;border:1px solid #d4c08a">60</td></tr>
  </tbody>
</table>

<h2>Tips</h2>
<ul>
  <li>Fingers are largest in the afternoon, smallest in the morning and after exercise. Measure mid-day for the daily-life size.</li>
  <li>Wide bands (4mm+) feel tighter than thin bands at the same nominal size. Go +0.5.</li>
  <li>If proposing as a surprise: pick HK 12 (Taiwanese bridal average). Size adjustments ±2 are usually free in the first 6 months.</li>
  <li>Knuckle larger than the base? Use a sizing bead added to the inner band.</li>
</ul>

<p>Once sized, see <a href="/blog/wedding-bands">wedding bands</a> for the
matching band style and <a href="/blog/engagement-guide">engagement playbook</a>
for the full purchase flow.</p>
'''


EN['ring-insurance'] = '''
<aside style="margin:0 0 22px;padding:16px 20px;background:linear-gradient(180deg,#fffdf7,#fbf3df);border-left:4px solid #c9a45c;border-radius:8px">
  <div style="font-size:10.5px;letter-spacing:.22em;text-transform:uppercase;color:#8a6e30;font-weight:700;margin-bottom:6px">TL;DR</div>
  In Taiwan, jewellery insurance runs ~1-2% of appraised value annually.
  For a NT$300K ring that's NT$3-6K/year — cheap insurance against loss
  or theft. Get a fresh appraisal every 3-5 years.
</aside>

<h2>Coverage options in Taiwan</h2>
<ul>
  <li><strong>Home contents rider</strong> (Cathay, Fubon, Shin Kong) — adds jewellery to your home insurance, covers theft &amp; damage at home. Cheapest.</li>
  <li><strong>Standalone jewellery policy</strong> — covers loss anywhere worldwide including drain, accidental damage. ~1.5-2% of appraised value annually.</li>
  <li><strong>Travel insurance valuables rider</strong> — for trips only; useful for honeymoon photography sessions.</li>
</ul>

<h2>What's covered, what's not</h2>
<table style="width:100%;border-collapse:collapse;margin:14px 0">
  <thead><tr style="background:#fbf3df"><th style="padding:6px;border:1px solid #d4c08a">Event</th><th style="padding:6px;border:1px solid #d4c08a">Home rider</th><th style="padding:6px;border:1px solid #d4c08a">Standalone</th></tr></thead>
  <tbody>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Theft from home</td><td style="padding:6px;border:1px solid #d4c08a">✓</td><td style="padding:6px;border:1px solid #d4c08a">✓</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Theft from car/hotel</td><td style="padding:6px;border:1px solid #d4c08a">Often ✗</td><td style="padding:6px;border:1px solid #d4c08a">✓</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Loss (fell off, drain)</td><td style="padding:6px;border:1px solid #d4c08a">✗</td><td style="padding:6px;border:1px solid #d4c08a">✓</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Stone lost from prong</td><td style="padding:6px;border:1px solid #d4c08a">✗</td><td style="padding:6px;border:1px solid #d4c08a">✓ if mysteriously disappeared</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Wear &amp; tear</td><td style="padding:6px;border:1px solid #d4c08a">✗</td><td style="padding:6px;border:1px solid #d4c08a">✗</td></tr>
  </tbody>
</table>

<h2>Documentation checklist</h2>
<ul>
  <li>Original GIA report.</li>
  <li>Independent appraisal from licensed gemologist (insurer usually requires).</li>
  <li>Receipt &amp; certificate of authenticity.</li>
  <li>High-resolution photos of stone (face-up + side) and any unique inscription.</li>
  <li>Refresh appraisal every 3-5 years to reflect current replacement cost.</li>
</ul>

<h2>Daily prevention beats insurance</h2>
<p>Take it off when: showering (soap film), swimming (chlorine + cold-shrink),
gym (impact), gardening, kitchen prep. Most claims are preventable. See
<a href="/blog/diamond-care">diamond care</a> for daily habits.</p>
'''


EN['secondhand-rings'] = '''
<aside style="margin:0 0 22px;padding:16px 20px;background:linear-gradient(180deg,#fffdf7,#fbf3df);border-left:4px solid #c9a45c;border-radius:8px">
  <div style="font-size:10.5px;letter-spacing:.22em;text-transform:uppercase;color:#8a6e30;font-weight:700;margin-bottom:6px">TL;DR</div>
  Pre-owned rings sell at 40-60% of original retail — same diamond, same
  certification, with a story. The risk is provenance and authenticity. Buy
  only with verified GIA paper, in-person inspection, and a return window.
</aside>

<h2>Where to look in Taiwan</h2>
<ul>
  <li><strong>Auction houses</strong> — Sotheby's HK, Christie's HK, Ravenel; safest, well-vetted.</li>
  <li><strong>Estate-jewellery dealers</strong> — small shops in Taipei (e.g., Yongkang St area); negotiable.</li>
  <li><strong>Carousell / Yahoo</strong> — cheapest but highest risk; insist on viewing in person at a neutral jeweller.</li>
  <li><strong>Pawn auctions</strong> — typhoon-priced occasionally; verify GIA before bidding.</li>
</ul>

<h2>The verification protocol</h2>
<ol>
  <li><strong>Match laser inscription to GIA cert.</strong> No inscription, no deal — fake risk too high.</li>
  <li><strong>Check the GIA report at gia.edu.</strong> Confirm the report number is real and current.</li>
  <li><strong>Take to an independent gemologist</strong> for in-person verification (NT$1-3K, well worth it).</li>
  <li><strong>Inspect the prongs &amp; setting</strong> — old rings often need re-tipping (NT$2-5K) or new shank (NT$8-15K).</li>
  <li><strong>Insist on 7-day return</strong> from any reputable seller.</li>
</ol>

<h2>Pricing benchmarks</h2>
<table style="width:100%;border-collapse:collapse;margin:14px 0">
  <thead><tr style="background:#fbf3df"><th style="padding:6px;border:1px solid #d4c08a">Source</th><th style="padding:6px;border:1px solid #d4c08a">Typical % of original retail</th></tr></thead>
  <tbody>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Auction (vintage, brand-name)</td><td style="padding:6px;border:1px solid #d4c08a">50-80%</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Estate dealer</td><td style="padding:6px;border:1px solid #d4c08a">45-60%</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Private (Carousell)</td><td style="padding:6px;border:1px solid #d4c08a">35-50%</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Pawn shop</td><td style="padding:6px;border:1px solid #d4c08a">30-45%</td></tr>
  </tbody>
</table>

<h2>Cultural note</h2>
<p>Some Taiwanese families consider second-hand engagement rings inauspicious.
Worth asking before going down this road. If it matters, you can buy a
secondhand stone and have it reset in a new ring — no one will know.</p>

<p>See <a href="/blog/heirloom-redesign">heirloom redesign</a> for the
re-mounting workflow.</p>
'''


EN['mens-engagement-rings'] = '''
<aside style="margin:0 0 22px;padding:16px 20px;background:linear-gradient(180deg,#fffdf7,#fbf3df);border-left:4px solid #c9a45c;border-radius:8px">
  <div style="font-size:10.5px;letter-spacing:.22em;text-transform:uppercase;color:#8a6e30;font-weight:700;margin-bottom:6px">TL;DR</div>
  Men's engagement rings are now ~25% of the market. Common styles: plain
  band, bezel-set diamond, black diamond, salt-and-pepper, signet. Budget
  NT$30-80K for solid value.
</aside>

<h2>Five style directions</h2>
<ul>
  <li><strong>Plain platinum / 18K white gold band</strong> — minimal, can double as wedding band.</li>
  <li><strong>Bezel-set diamond (0.3-0.7 ct)</strong> — flush, snag-free, professional.</li>
  <li><strong>Black diamond solitaire</strong> — strong contrast against finger; opaque so cut grade matters less.</li>
  <li><strong>Salt-and-pepper diamond</strong> — included natural diamonds with character; affordable.</li>
  <li><strong>Signet with engraving</strong> — heirloom-style; surface for monogram.</li>
</ul>

<h2>Metal choices</h2>
<table style="width:100%;border-collapse:collapse;margin:14px 0">
  <thead><tr style="background:#fbf3df"><th style="padding:6px;border:1px solid #d4c08a">Metal</th><th style="padding:6px;border:1px solid #d4c08a">Look</th><th style="padding:6px;border:1px solid #d4c08a">Daily wear</th></tr></thead>
  <tbody>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Platinum</td><td style="padding:6px;border:1px solid #d4c08a">Cool white, weighty</td><td style="padding:6px;border:1px solid #d4c08a">Hardest, most durable</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">18K white gold</td><td style="padding:6px;border:1px solid #d4c08a">Bright white</td><td style="padding:6px;border:1px solid #d4c08a">Re-rhodium every 2-3 yrs</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Titanium</td><td style="padding:6px;border:1px solid #d4c08a">Dark grey, tactical</td><td style="padding:6px;border:1px solid #d4c08a">Cannot be resized</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Tantalum</td><td style="padding:6px;border:1px solid #d4c08a">Inky grey</td><td style="padding:6px;border:1px solid #d4c08a">Hypoallergenic</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Tungsten</td><td style="padding:6px;border:1px solid #d4c08a">Heavy, dark</td><td style="padding:6px;border:1px solid #d4c08a">Brittle; chips on impact</td></tr>
  </tbody>
</table>

<h2>Sizing for active hands</h2>
<p>If he works with hands (surgeon, mechanic, athlete), pick:
low-profile bezel or flush set, ≤4mm wide, comfort-fit interior, and a
metal that re-sizes easily (gold/platinum, not titanium/tungsten). See
<a href="/blog/ring-sizing">ring sizing</a>.</p>

<p>For LGBTQ couples planning matched-style sets, see
<a href="/blog/lgbtq-rings">LGBTQ rings</a>.</p>
'''


# ─────────────────────────────────────────────────────────────────
# Round 14 — Bands / ceremony / lifestyle (10)
# ─────────────────────────────────────────────────────────────────

EN['wedding-bands'] = '''
<aside style="margin:0 0 22px;padding:16px 20px;background:linear-gradient(180deg,#fffdf7,#fbf3df);border-left:4px solid #c9a45c;border-radius:8px">
  <div style="font-size:10.5px;letter-spacing:.22em;text-transform:uppercase;color:#8a6e30;font-weight:700;margin-bottom:6px">TL;DR</div>
  The wedding band sits next to the engagement ring on the same finger.
  Match metal, profile, and width. Plain bands age best; pavé and eternity
  bands are higher-maintenance but more visible.
</aside>

<h2>The four band families</h2>
<ul>
  <li><strong>Plain</strong> — solid metal, no stones. Flat, comfort-fit, or knife-edge profile. Cheapest, longest-lasting.</li>
  <li><strong>Pavé / micro-pavé</strong> — tiny diamonds (0.005-0.02 ct) covering the top. Sparkly but small stones can pop out.</li>
  <li><strong>Channel-set</strong> — small diamonds inset between two metal walls. More secure than pavé.</li>
  <li><strong>Eternity</strong> — diamonds all the way around. Most expensive; cannot be resized.</li>
</ul>

<h2>Matching to the engagement ring</h2>
<table style="width:100%;border-collapse:collapse;margin:14px 0">
  <thead><tr style="background:#fbf3df"><th style="padding:6px;border:1px solid #d4c08a">Engagement ring</th><th style="padding:6px;border:1px solid #d4c08a">Band that pairs well</th></tr></thead>
  <tbody>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Solitaire 4-prong</td><td style="padding:6px;border:1px solid #d4c08a">Plain or contour band</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Halo</td><td style="padding:6px;border:1px solid #d4c08a">Plain (halo provides the sparkle)</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Pavé shank</td><td style="padding:6px;border:1px solid #d4c08a">Matching pavé band</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Three-stone</td><td style="padding:6px;border:1px solid #d4c08a">Plain narrow band</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Vintage / filigree</td><td style="padding:6px;border:1px solid #d4c08a">Milgrain band, similar era</td></tr>
  </tbody>
</table>

<h2>Width and profile</h2>
<p>Bridal band width 1.5-3 mm; men's 4-6 mm. Comfort-fit (rounded inside)
slips on easier and feels lighter. Keep widths within 1 mm of each other
between the two rings to avoid awkward stacking.</p>

<h2>Metal matching</h2>
<p>Always match the metal of the engagement ring exactly. A platinum solitaire
with an 18K white-gold band will visibly mismatch over time as gold yellows
slightly. Read <a href="/blog/wedding-metals">the wedding metals guide</a>.</p>

<p>For the proposal-vs-wedding-vs-eternity ring distinction, see the
<a href="/blog/proposal-vs-wedding-vs-eternity">three-ring article</a>.</p>
'''


EN['wedding-metals'] = '''
<aside style="margin:0 0 22px;padding:16px 20px;background:linear-gradient(180deg,#fffdf7,#fbf3df);border-left:4px solid #c9a45c;border-radius:8px">
  <div style="font-size:10.5px;letter-spacing:.22em;text-transform:uppercase;color:#8a6e30;font-weight:700;margin-bottom:6px">TL;DR</div>
  Five metals dominate wedding rings: platinum (king), 18K white gold (most
  popular), 18K yellow gold (warm), 18K rose gold (trendy), and palladium
  (rare). Match to skin tone and lifestyle.
</aside>

<h2>The big five</h2>
<table style="width:100%;border-collapse:collapse;margin:14px 0">
  <thead><tr style="background:#fbf3df"><th style="padding:6px;border:1px solid #d4c08a">Metal</th><th style="padding:6px;border:1px solid #d4c08a">Color</th><th style="padding:6px;border:1px solid #d4c08a">Pros</th><th style="padding:6px;border:1px solid #d4c08a">Cons</th></tr></thead>
  <tbody>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Platinum (Pt950)</td><td style="padding:6px;border:1px solid #d4c08a">Cool white</td><td style="padding:6px;border:1px solid #d4c08a">Densest, hypoallergenic, no fade</td><td style="padding:6px;border:1px solid #d4c08a">~30% pricier; develops patina</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">18K white gold</td><td style="padding:6px;border:1px solid #d4c08a">Bright white</td><td style="padding:6px;border:1px solid #d4c08a">Cheapest white option, hard</td><td style="padding:6px;border:1px solid #d4c08a">Re-rhodium every 2-3 yrs (~NT$1-2K)</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">18K yellow gold</td><td style="padding:6px;border:1px solid #d4c08a">Warm yellow</td><td style="padding:6px;border:1px solid #d4c08a">Classic, masks low color stones</td><td style="padding:6px;border:1px solid #d4c08a">Less popular in young Taiwan</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">18K rose gold</td><td style="padding:6px;border:1px solid #d4c08a">Pink-copper</td><td style="padding:6px;border:1px solid #d4c08a">Romantic, distinctive</td><td style="padding:6px;border:1px solid #d4c08a">Color drifts with patina</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Palladium</td><td style="padding:6px;border:1px solid #d4c08a">Cool grey-white</td><td style="padding:6px;border:1px solid #d4c08a">Light, hypoallergenic</td><td style="padding:6px;border:1px solid #d4c08a">Hard to find in Taiwan</td></tr>
  </tbody>
</table>

<h2>Skin tone matching</h2>
<ul>
  <li><strong>Cool undertones (blue veins)</strong> — platinum, white gold.</li>
  <li><strong>Warm undertones (green veins)</strong> — yellow gold, rose gold.</li>
  <li><strong>Neutral</strong> — anything works; default to platinum or white gold.</li>
</ul>

<h2>Daily wear durability</h2>
<p>Platinum scratches but doesn't lose mass — patina builds, looks vintage.
White gold loses its rhodium plating revealing a yellower base color; needs
re-plating. 18K is harder than 14K (Taiwan default is 18K); avoid 9K which
tarnishes. See <a href="/blog/diamond-care">care guide</a>.</p>

<p>Buying for an active spouse? See <a href="/blog/mens-engagement-rings">men's
ring guide</a> for harder alternatives like titanium and tantalum.</p>
'''


EN['prong-settings-guide'] = '''
<aside style="margin:0 0 22px;padding:16px 20px;background:linear-gradient(180deg,#fffdf7,#fbf3df);border-left:4px solid #c9a45c;border-radius:8px">
  <div style="font-size:10.5px;letter-spacing:.22em;text-transform:uppercase;color:#8a6e30;font-weight:700;margin-bottom:6px">TL;DR</div>
  Prong settings hold the diamond. 4-prong shows more stone; 6-prong is more
  secure. Bezel is safest for active wear; halo amplifies the look. Choose
  based on the wearer's lifestyle.
</aside>

<h2>The 6 main settings</h2>
<ul>
  <li><strong>4-prong solitaire</strong> — Tiffany classic. Maximum stone exposure, slightly less secure.</li>
  <li><strong>6-prong solitaire</strong> — More fingers gripping, slightly less stone visible.</li>
  <li><strong>Bezel</strong> — Metal rim around the entire stone. Safest for active hands, snag-free.</li>
  <li><strong>Halo</strong> — Small diamonds surround the center, making it look 30-50% larger.</li>
  <li><strong>Three-stone</strong> — Center + two side stones (past, present, future).</li>
  <li><strong>Tension</strong> — Stone held by inward metal pressure. Modern look, hardest to resize.</li>
</ul>

<h2>4 vs 6 prong — the real difference</h2>
<table style="width:100%;border-collapse:collapse;margin:14px 0">
  <thead><tr style="background:#fbf3df"><th style="padding:6px;border:1px solid #d4c08a">Aspect</th><th style="padding:6px;border:1px solid #d4c08a">4-prong</th><th style="padding:6px;border:1px solid #d4c08a">6-prong</th></tr></thead>
  <tbody>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Stone visibility</td><td style="padding:6px;border:1px solid #d4c08a">~92% face-up exposed</td><td style="padding:6px;border:1px solid #d4c08a">~88%</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Snag risk</td><td style="padding:6px;border:1px solid #d4c08a">Slightly higher</td><td style="padding:6px;border:1px solid #d4c08a">Lower</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">If one prong fails</td><td style="padding:6px;border:1px solid #d4c08a">Stone at risk</td><td style="padding:6px;border:1px solid #d4c08a">5 still hold</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Look</td><td style="padding:6px;border:1px solid #d4c08a">Modern, square outline</td><td style="padding:6px;border:1px solid #d4c08a">Round, traditional</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Best for stone shape</td><td style="padding:6px;border:1px solid #d4c08a">Princess, cushion, emerald</td><td style="padding:6px;border:1px solid #d4c08a">Round brilliant</td></tr>
  </tbody>
</table>

<h2>Maintenance schedule</h2>
<ul>
  <li>Inspect prongs annually — bring it in, ask the jeweller to check tightness with tweezers.</li>
  <li>Re-tip every 5-10 years (NT$2-5K). Worn prongs are the #1 cause of stone loss.</li>
  <li>Avoid catching on hair, fabric, gym equipment — see <a href="/blog/diamond-care">care guide</a>.</li>
</ul>

<p>For unusual stone shapes (princess corners, marquise points), V-prongs
specifically protect the vulnerable tips. See <a href="/blog/diamond-shapes">
shape guide</a> for which corners need protection.</p>
'''


EN['engraving-personalization'] = '''
<aside style="margin:0 0 22px;padding:16px 20px;background:linear-gradient(180deg,#fffdf7,#fbf3df);border-left:4px solid #c9a45c;border-radius:8px">
  <div style="font-size:10.5px;letter-spacing:.22em;text-transform:uppercase;color:#8a6e30;font-weight:700;margin-bottom:6px">TL;DR</div>
  Inside-band engraving costs NT$500-2,000 and adds permanent meaning.
  Keep it short (15-25 characters), use serif or italic for elegance, and
  laser-engrave (hand-engraved is harder to redo if you resize).
</aside>

<h2>What to engrave</h2>
<ul>
  <li><strong>Wedding date</strong> — "2026.10.10" or "10·10·26".</li>
  <li><strong>Initials + date</strong> — "A &amp; B / 10.10.26".</li>
  <li><strong>Short phrase</strong> — "Forever yours", "我的妳", "永遠 ∞".</li>
  <li><strong>Coordinates</strong> — proposal location lat/long for the romantically inclined.</li>
  <li><strong>Sound wave</strong> — laser-etched waveform of "I do". Trendy.</li>
</ul>

<h2>Engraving methods</h2>
<table style="width:100%;border-collapse:collapse;margin:14px 0">
  <thead><tr style="background:#fbf3df"><th style="padding:6px;border:1px solid #d4c08a">Method</th><th style="padding:6px;border:1px solid #d4c08a">Cost</th><th style="padding:6px;border:1px solid #d4c08a">Notes</th></tr></thead>
  <tbody>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Laser</td><td style="padding:6px;border:1px solid #d4c08a">NT$500-1,500</td><td style="padding:6px;border:1px solid #d4c08a">Precise, fits any font, redo-able if resized</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Hand</td><td style="padding:6px;border:1px solid #d4c08a">NT$2,000-5,000</td><td style="padding:6px;border:1px solid #d4c08a">Artisanal, deeper, not redo-able</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Machine</td><td style="padding:6px;border:1px solid #d4c08a">NT$300-800</td><td style="padding:6px;border:1px solid #d4c08a">Mass-jeweller default; limited fonts</td></tr>
  </tbody>
</table>

<h2>Practical guidelines</h2>
<ul>
  <li><strong>Length</strong> — interior of a 4 mm band fits ~30 characters; 2 mm band only ~15.</li>
  <li><strong>Font</strong> — serif/italic for romance; sans-serif for modern; avoid script (illegible at small size).</li>
  <li><strong>Resize impact</strong> — laser engraving can be re-done after resizing; hand-engraving usually cannot.</li>
  <li><strong>Languages</strong> — Chinese characters work but require deeper engraving; allow more space per character.</li>
</ul>

<h2>Beyond text — true personalization</h2>
<ul>
  <li>Birthstone accents in the band shoulders.</li>
  <li>Family heirloom diamond reset into a new mounting (see <a href="/blog/heirloom-redesign">heirloom redesign</a>).</li>
  <li>Custom milgrain pattern matching grandmother's ring.</li>
  <li>Hidden inset stone visible only when removed.</li>
</ul>

<p>For full-custom design timelines, see <a href="/blog/engagement-guide">
the engagement playbook</a>.</p>
'''


EN['heirloom-redesign'] = '''
<aside style="margin:0 0 22px;padding:16px 20px;background:linear-gradient(180deg,#fffdf7,#fbf3df);border-left:4px solid #c9a45c;border-radius:8px">
  <div style="font-size:10.5px;letter-spacing:.22em;text-transform:uppercase;color:#8a6e30;font-weight:700;margin-bottom:6px">TL;DR</div>
  Inheriting Grandma's ring? You can keep the stone and modernize the setting.
  Cost: NT$15-40K for a new mounting + stone re-grading + setting work. The
  diamond becomes "yours" without erasing the lineage.
</aside>

<h2>The redesign workflow</h2>
<ol>
  <li><strong>Have the stone certified.</strong> Old family stones often have no GIA paper; spend NT$3-8K to get one. You may discover it's a much better stone than the family thought.</li>
  <li><strong>Decide what to keep.</strong> The stone? The metal (often re-melted)? The setting style as a reference?</li>
  <li><strong>Choose new design.</strong> Solitaire to halo, princess to cushion, etc. See <a href="/blog/prong-settings-guide">settings guide</a>.</li>
  <li><strong>Find a custom jeweller.</strong> Established shops in Taipei (e.g., Just Diamond, BUERHKAU custom department) handle this routinely.</li>
  <li><strong>Approve CAD render</strong> before metal is cut. Insist on 3 angles + a wax model.</li>
  <li><strong>Photograph the original ring</strong> before destruction — for sentimental record.</li>
</ol>

<h2>Cost breakdown</h2>
<table style="width:100%;border-collapse:collapse;margin:14px 0">
  <thead><tr style="background:#fbf3df"><th style="padding:6px;border:1px solid #d4c08a">Service</th><th style="padding:6px;border:1px solid #d4c08a">Cost (NT$)</th></tr></thead>
  <tbody>
    <tr><td style="padding:6px;border:1px solid #d4c08a">GIA recertification (loose)</td><td style="padding:6px;border:1px solid #d4c08a">3,000-8,000</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Custom CAD design</td><td style="padding:6px;border:1px solid #d4c08a">3,000-10,000</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Mounting (Pt950 solitaire)</td><td style="padding:6px;border:1px solid #d4c08a">15,000-30,000</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Setting + finish</td><td style="padding:6px;border:1px solid #d4c08a">5,000-12,000</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a"><strong>Total</strong></td><td style="padding:6px;border:1px solid #d4c08a"><strong>~25,000-50,000</strong></td></tr>
  </tbody>
</table>

<h2>Common modernizations</h2>
<ul>
  <li>Old European cut → re-cut to modern brilliant (loses 5-10% weight, gains 30% sparkle). Controversial — many prefer to preserve original cut.</li>
  <li>Yellow gold → platinum or white gold (suits modern aesthetics).</li>
  <li>Ornate filigree → minimalist solitaire.</li>
  <li>Add a halo around small inherited stone for size.</li>
</ul>

<h2>Cultural & emotional</h2>
<p>Discuss with the family. Some prefer the original ring be preserved as-is.
Compromise: have the original ring photographed and cast in resin display,
keep the stone, redesign the rest. See <a href="/blog/secondhand-rings">
secondhand rings</a> for related provenance discussion.</p>
'''


EN['proposal-speech'] = '''
<aside style="margin:0 0 22px;padding:16px 20px;background:linear-gradient(180deg,#fffdf7,#fbf3df);border-left:4px solid #c9a45c;border-radius:8px">
  <div style="font-size:10.5px;letter-spacing:.22em;text-transform:uppercase;color:#8a6e30;font-weight:700;margin-bottom:6px">TL;DR</div>
  A proposal speech doesn't need to be Shakespeare. 60-90 seconds, three beats:
  (1) why her, (2) why now, (3) the question. Memorize the question; you'll
  forget everything else.
</aside>

<h2>The 3-beat structure</h2>
<ol>
  <li><strong>Why her</strong> (30s) — one specific moment that captures her essence. Not "you're amazing" (generic) — "the way you stayed up making soup when I had food poisoning at 3am" (specific).</li>
  <li><strong>Why now</strong> (20s) — what changed in you that made marriage feel right. "I used to think marriage was just paperwork. The last year showed me what it actually is."</li>
  <li><strong>The question</strong> (10s) — kneel, ring out, breathe, ask. "Will you marry me?" — clear and direct.</li>
</ol>

<h2>Three drafts to write</h2>
<ul>
  <li><strong>Long version (90s)</strong> — practice this one. Shows you took it seriously.</li>
  <li><strong>Medium version (45s)</strong> — for if you start crying and need to compress.</li>
  <li><strong>Emergency version (10s)</strong> — just the question. If everything goes sideways, you have a fallback.</li>
</ul>

<h2>Common mistakes</h2>
<ul>
  <li><strong>Reading from your phone.</strong> Memorize. Phone-reading kills the moment.</li>
  <li><strong>Jokes that bomb.</strong> Save humor for the wedding speech.</li>
  <li><strong>Listing her flaws cutely.</strong> Don't.</li>
  <li><strong>Forgetting to actually ask the question.</strong> Surprisingly common.</li>
  <li><strong>Mentioning exes.</strong> Just don't.</li>
</ul>

<h2>Setting the scene</h2>
<p>Choose a location that means something — first date spot, vacation place,
home. Public proposals can pressure her into yes; consider private. Bring a
photographer (friend, hidden) so she has the photos. See
<a href="/blog/engagement-guide">engagement playbook</a> for the rest of the
purchase flow leading up to this moment.</p>
'''


EN['engagement-timeline'] = '''
<aside style="margin:0 0 22px;padding:16px 20px;background:linear-gradient(180deg,#fffdf7,#fbf3df);border-left:4px solid #c9a45c;border-radius:8px">
  <div style="font-size:10.5px;letter-spacing:.22em;text-transform:uppercase;color:#8a6e30;font-weight:700;margin-bottom:6px">TL;DR</div>
  Average Taiwanese couple: 2-4 years dating before engagement, 6-12 months
  engagement before wedding. Compress for visa/family/financial reasons,
  extend if you want spread costs and finalize career plans.
</aside>

<h2>Common timelines in Taiwan</h2>
<table style="width:100%;border-collapse:collapse;margin:14px 0">
  <thead><tr style="background:#fbf3df"><th style="padding:6px;border:1px solid #d4c08a">Stage</th><th style="padding:6px;border:1px solid #d4c08a">Typical duration</th></tr></thead>
  <tbody>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Dating before living together</td><td style="padding:6px;border:1px solid #d4c08a">1-3 years</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Living together before engagement</td><td style="padding:6px;border:1px solid #d4c08a">0-2 years</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a"><strong>Engagement to wedding</strong></td><td style="padding:6px;border:1px solid #d4c08a"><strong>6-12 months</strong></td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Wedding to first child</td><td style="padding:6px;border:1px solid #d4c08a">1-3 years (declining)</td></tr>
  </tbody>
</table>

<h2>What needs to happen in the engagement window</h2>
<ol>
  <li><strong>Month 1-2</strong> — both families meet, set wedding budget split.</li>
  <li><strong>Month 2-3</strong> — book venue, photographer, banquet hall (Taipei prime dates 12+ months out).</li>
  <li><strong>Month 3-5</strong> — wedding gowns &amp; tuxedos selection, photo prewedding.</li>
  <li><strong>Month 5-8</strong> — guest list, invitations, registry, accommodation logistics.</li>
  <li><strong>Month 8-10</strong> — finalize vows, ceremony order, music, transportation.</li>
  <li><strong>Month 10-12</strong> — dress rehearsal, marriage registration, honeymoon booking.</li>
</ol>

<h2>When to compress</h2>
<ul>
  <li>Pregnancy timing.</li>
  <li>Visa requirements (foreign spouse).</li>
  <li>Job relocation.</li>
  <li>Family member's health window.</li>
</ul>
<p>Compressed timelines are normal — 3-month engagements happen often. Just
expect higher venue costs (less negotiating leverage) and limited photographer
choice.</p>

<h2>When to extend</h2>
<ul>
  <li>Saving up to avoid debt.</li>
  <li>Awaiting graduation, professional qualification.</li>
  <li>Wanting a destination wedding (12-18 months prep).</li>
</ul>

<p>For dating duration norms, see <a href="/blog/dating-duration">dating duration
article</a>. For overseas weddings, see <a href="/blog/destination-wedding">
destination wedding</a>.</p>
'''


EN['dating-duration'] = '''
<aside style="margin:0 0 22px;padding:16px 20px;background:linear-gradient(180deg,#fffdf7,#fbf3df);border-left:4px solid #c9a45c;border-radius:8px">
  <div style="font-size:10.5px;letter-spacing:.22em;text-transform:uppercase;color:#8a6e30;font-weight:700;margin-bottom:6px">TL;DR</div>
  Studies show couples who dated 2+ years before engagement have lower divorce
  rates than those at 1 year or less. But duration matters less than what's
  in those years — cohabitation, conflict resolution, financial alignment.
</aside>

<h2>What the data says</h2>
<p>Emory University's 2014 study (3,000+ US couples) found:</p>
<ul>
  <li>Dated &lt;1 year before engagement → 20% higher divorce risk vs 1-2 years.</li>
  <li>Dated 3+ years → ~50% lower risk vs &lt;1 year.</li>
  <li>Lived together first → small positive correlation with stability (in modern cohorts).</li>
</ul>
<p>Taiwan-specific data is sparser; PTT/Dcard surveys suggest modern Taiwanese
couples date 2-4 years before engagement on average — slightly longer than
US.</p>

<h2>The "right" duration depends on what you're testing</h2>
<table style="width:100%;border-collapse:collapse;margin:14px 0">
  <thead><tr style="background:#fbf3df"><th style="padding:6px;border:1px solid #d4c08a">Test</th><th style="padding:6px;border:1px solid #d4c08a">Months needed</th></tr></thead>
  <tbody>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Sexual chemistry beyond honeymoon</td><td style="padding:6px;border:1px solid #d4c08a">6-12</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">First major fight + recovery</td><td style="padding:6px;border:1px solid #d4c08a">6-18</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Meet both extended families</td><td style="padding:6px;border:1px solid #d4c08a">12-18</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Cohabitation conflict patterns surface</td><td style="padding:6px;border:1px solid #d4c08a">12-24 living together</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Financial habits visible</td><td style="padding:6px;border:1px solid #d4c08a">18-24</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Kids/career/city alignment confirmed</td><td style="padding:6px;border:1px solid #d4c08a">18-36</td></tr>
  </tbody>
</table>

<h2>Red flags that no duration fixes</h2>
<ul>
  <li>Refusing to discuss money openly.</li>
  <li>Different positions on having children.</li>
  <li>Refusing to meet the other's family after 12+ months.</li>
  <li>Repeating same conflict with no learning.</li>
  <li>Hiding financial debt.</li>
</ul>

<p>For the engagement-to-wedding flow, see <a href="/blog/engagement-timeline">
the engagement timeline</a>.</p>
'''


EN['destination-wedding'] = '''
<aside style="margin:0 0 22px;padding:16px 20px;background:linear-gradient(180deg,#fffdf7,#fbf3df);border-left:4px solid #c9a45c;border-radius:8px">
  <div style="font-size:10.5px;letter-spacing:.22em;text-transform:uppercase;color:#8a6e30;font-weight:700;margin-bottom:6px">TL;DR</div>
  Destination weddings (Bali, Okinawa, Hawaii, Maldives) cost NT$300K-1.5M
  for 20-50 guests. Smaller, more intimate, doubles as honeymoon. Plan
  12-18 months ahead for visa, accommodation, vendor coordination.
</aside>

<h2>Top destinations for Taiwanese couples</h2>
<table style="width:100%;border-collapse:collapse;margin:14px 0">
  <thead><tr style="background:#fbf3df"><th style="padding:6px;border:1px solid #d4c08a">Location</th><th style="padding:6px;border:1px solid #d4c08a">Vibe</th><th style="padding:6px;border:1px solid #d4c08a">Cost (50 guests)</th></tr></thead>
  <tbody>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Okinawa</td><td style="padding:6px;border:1px solid #d4c08a">Beach chapel, easy flight</td><td style="padding:6px;border:1px solid #d4c08a">NT$500K-800K</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Bali</td><td style="padding:6px;border:1px solid #d4c08a">Cliff resort, sunset</td><td style="padding:6px;border:1px solid #d4c08a">NT$400K-700K</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Hawaii</td><td style="padding:6px;border:1px solid #d4c08a">Beach + iconic</td><td style="padding:6px;border:1px solid #d4c08a">NT$1.0M-1.8M</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Maldives</td><td style="padding:6px;border:1px solid #d4c08a">Overwater bungalow</td><td style="padding:6px;border:1px solid #d4c08a">NT$1.2M-2.0M</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Kenting / Hualien</td><td style="padding:6px;border:1px solid #d4c08a">Domestic; budget-friendly</td><td style="padding:6px;border:1px solid #d4c08a">NT$200K-400K</td></tr>
  </tbody>
</table>

<h2>Logistics checklist</h2>
<ol>
  <li><strong>12-18 months before</strong> — pick destination, book chapel/venue, save dates to guests.</li>
  <li><strong>9 months</strong> — block hotel rooms (group rates), hire local planner.</li>
  <li><strong>6 months</strong> — invitations with detailed travel info, flight booking deadline.</li>
  <li><strong>3 months</strong> — confirm vendor list (florist, photographer, makeup, transport).</li>
  <li><strong>1 month</strong> — final headcount, dietary needs, emergency contacts.</li>
  <li><strong>Week before</strong> — fly out 3 days early for jet lag + setup.</li>
</ol>

<h2>Hidden costs</h2>
<ul>
  <li>Guest accommodation subsidy (often 30-50% of total).</li>
  <li>Welcome dinner the night before.</li>
  <li>Local marriage license requirements (legal recognition usually back home).</li>
  <li>Translator if vendor doesn't speak Mandarin/English.</li>
  <li>Shipping wedding attire (separate luggage; chapel may have storage).</li>
</ul>

<h2>Pros &amp; cons</h2>
<p><strong>Pros:</strong> intimate (smaller guest list cuts naturally), built-in honeymoon,
photogenic. <strong>Cons:</strong> guests bear travel cost (some can't attend), weather
risk, less family-side flexibility. Many couples pair it with a Taiwan-side
banquet for older relatives 1-2 months later.</p>
'''


EN['lgbtq-rings'] = '''
<aside style="margin:0 0 22px;padding:16px 20px;background:linear-gradient(180deg,#fffdf7,#fbf3df);border-left:4px solid #c9a45c;border-radius:8px">
  <div style="font-size:10.5px;letter-spacing:.22em;text-transform:uppercase;color:#8a6e30;font-weight:700;margin-bottom:6px">TL;DR</div>
  Taiwan legalized same-sex marriage in 2019. LGBTQ engagement and wedding
  ring shopping has become mainstream. Common patterns: matched-style sets,
  asymmetric pairs, alternative gemstones (sapphire, emerald), and
  rainbow-band designs.
</aside>

<h2>Style approaches</h2>
<ul>
  <li><strong>Matched set</strong> — both partners wear identical rings (or mirrored versions, e.g. left-curved and right-curved). Symbol of equality.</li>
  <li><strong>Coordinated pair</strong> — same metal and theme, different sizes/widths reflecting personal style.</li>
  <li><strong>Asymmetric</strong> — completely different rings, united by a hidden detail (matching engraving, same stone origin).</li>
  <li><strong>His &amp; hers / theirs &amp; theirs</strong> — traditional engagement-and-band combinations, mixed and matched.</li>
</ul>

<h2>Stone choices beyond diamond</h2>
<table style="width:100%;border-collapse:collapse;margin:14px 0">
  <thead><tr style="background:#fbf3df"><th style="padding:6px;border:1px solid #d4c08a">Stone</th><th style="padding:6px;border:1px solid #d4c08a">Hardness (Mohs)</th><th style="padding:6px;border:1px solid #d4c08a">Notes</th></tr></thead>
  <tbody>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Diamond</td><td style="padding:6px;border:1px solid #d4c08a">10</td><td style="padding:6px;border:1px solid #d4c08a">Hardest; safest daily wear</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Sapphire</td><td style="padding:6px;border:1px solid #d4c08a">9</td><td style="padding:6px;border:1px solid #d4c08a">All colors except red; durable</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Ruby</td><td style="padding:6px;border:1px solid #d4c08a">9</td><td style="padding:6px;border:1px solid #d4c08a">Red corundum; passion symbol</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Emerald</td><td style="padding:6px;border:1px solid #d4c08a">7.5-8</td><td style="padding:6px;border:1px solid #d4c08a">Beautiful but inclusion-prone</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Moissanite</td><td style="padding:6px;border:1px solid #d4c08a">9.25</td><td style="padding:6px;border:1px solid #d4c08a">Diamond alternative; high fire</td></tr>
  </tbody>
</table>

<h2>Rainbow / pride elements</h2>
<ul>
  <li>Rainbow band — channel-set sapphires in spectral order (red ruby + pink + yellow + green tsavorite + blue + purple amethyst).</li>
  <li>Hidden rainbow — single colored stones inside the band (only the wearer sees).</li>
  <li>Custom enamel inlay in pride colors.</li>
  <li>Two metals fused (rose + white gold) representing union.</li>
</ul>

<h2>Taiwan vendors LGBTQ-friendly</h2>
<p>Major chains (ALUXE, Mabelle, Just Diamond) all serve LGBTQ couples without
issue. Independent designers in Taipei (e.g., Sangmun, Ai-Yu) often have
specific portfolios for same-sex couples. See <a href="/blog/taiwan-brands">
brand tier guide</a> and <a href="/blog/wedding-bands">wedding bands</a>.</p>
'''


# ─────────────────────────────────────────────────────────────────
# Round 14 — Care / niche / fancy (9)
# ─────────────────────────────────────────────────────────────────

EN['diamond-care'] = '''
<aside style="margin:0 0 22px;padding:16px 20px;background:linear-gradient(180deg,#fffdf7,#fbf3df);border-left:4px solid #c9a45c;border-radius:8px">
  <div style="font-size:10.5px;letter-spacing:.22em;text-transform:uppercase;color:#8a6e30;font-weight:700;margin-bottom:6px">TL;DR</div>
  Diamond is hardest mineral but not invincible — it can chip on impact and
  loose oil dramatically dims sparkle. 7 daily habits keep your ring looking
  new for 30+ years.
</aside>

<h2>The 7 habits</h2>
<ol>
  <li><strong>Take it off for showers.</strong> Soap film coats the pavilion and dims brilliance immediately.</li>
  <li><strong>Take it off for swimming.</strong> Chlorine erodes prongs over time; cold water shrinks fingers and ring slips.</li>
  <li><strong>Take it off at the gym.</strong> Impact + sweat + barbells = chipped stones, bent prongs.</li>
  <li><strong>Take it off in the kitchen.</strong> Oil, garlic juice, raw meat handling — bacteria love prong crevices.</li>
  <li><strong>Clean weekly.</strong> Warm water + 1 drop dish soap + soft toothbrush, 2 min. Rinse, pat dry.</li>
  <li><strong>Inspect prongs monthly.</strong> Run thumbnail along each prong; if it catches, see jeweller.</li>
  <li><strong>Annual professional check.</strong> Most jewellers offer free inspection + ultrasonic cleaning.</li>
</ol>

<h2>What NOT to do</h2>
<ul>
  <li><strong>Don't use toothpaste</strong> — abrasives scratch metal (not the diamond, but the setting).</li>
  <li><strong>Don't use bleach</strong> — corrodes alloys in white gold.</li>
  <li><strong>Don't store loose with other jewellery</strong> — diamond scratches everything else.</li>
  <li><strong>Don't sleep with it on</strong> — prongs catch on hair and sheets.</li>
  <li><strong>Don't ultrasonic clean if there's a fracture-filled or heavily included stone</strong> — vibrations expand inclusions.</li>
</ul>

<h2>Long-term maintenance</h2>
<table style="width:100%;border-collapse:collapse;margin:14px 0">
  <thead><tr style="background:#fbf3df"><th style="padding:6px;border:1px solid #d4c08a">Service</th><th style="padding:6px;border:1px solid #d4c08a">Frequency</th><th style="padding:6px;border:1px solid #d4c08a">Cost</th></tr></thead>
  <tbody>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Professional clean + inspect</td><td style="padding:6px;border:1px solid #d4c08a">Annual</td><td style="padding:6px;border:1px solid #d4c08a">Free at original retailer</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Re-rhodium plating (white gold)</td><td style="padding:6px;border:1px solid #d4c08a">2-3 years</td><td style="padding:6px;border:1px solid #d4c08a">NT$1,000-2,000</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Re-tip prongs</td><td style="padding:6px;border:1px solid #d4c08a">5-10 years</td><td style="padding:6px;border:1px solid #d4c08a">NT$2,000-5,000</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Resize</td><td style="padding:6px;border:1px solid #d4c08a">As needed</td><td style="padding:6px;border:1px solid #d4c08a">NT$1,500-4,000</td></tr>
  </tbody>
</table>

<p>Pair with <a href="/blog/ring-insurance">ring insurance</a> for full
protection.</p>
'''


EN['diamond-fun-facts'] = '''
<aside style="margin:0 0 22px;padding:16px 20px;background:linear-gradient(180deg,#fffdf7,#fbf3df);border-left:4px solid #c9a45c;border-radius:8px">
  <div style="font-size:10.5px;letter-spacing:.22em;text-transform:uppercase;color:#8a6e30;font-weight:700;margin-bottom:6px">TL;DR</div>
  Diamonds are weirder than you think — they can be rendered into graphite,
  burn at 763°C, transmit X-rays, and form on Saturn from lightning storms.
  Plus the marketing history is wilder than the geology.
</aside>

<h2>10 strange-but-true facts</h2>
<ol>
  <li><strong>Diamonds burn.</strong> Heat to 763°C in air and they oxidize into CO₂. Watch a candle vs a propane torch.</li>
  <li><strong>Saturn rains diamonds.</strong> Lightning in Saturn's methane atmosphere converts CH₄ to carbon, falls 1500 km, compresses into diamond rain. Same on Neptune.</li>
  <li><strong>"Brilliant" is a math invention.</strong> Marcel Tolkowsky (1919) proved the optimal facet angles in his MIT thesis. Every modern round brilliant traces back.</li>
  <li><strong>"A diamond is forever" was 1947.</strong> N.W. Ayer copywriter Frances Gerety wrote it for De Beers. AdAge ranked it #1 slogan of the 20th century.</li>
  <li><strong>Diamonds are old.</strong> Most are 1-3 billion years old, formed 150-200 km below the surface.</li>
  <li><strong>Earth has no monopoly.</strong> Meteorite impacts create "lonsdaleite" diamonds (hexagonal lattice, harder than regular).</li>
  <li><strong>Diamonds glow.</strong> ~30% fluoresce blue under UV — see <a href="/blog/fluorescence-deep-dive">fluorescence deep-dive</a>.</li>
  <li><strong>"Conflict diamonds" is &lt;1% of supply.</strong> Kimberley Process (since 2003) has gaps but the &lt;1% figure is industry consensus.</li>
  <li><strong>The Cullinan was 3,106 ct rough.</strong> Cut into 9 major + 96 minor stones; the largest, "Cullinan I" (530 ct), is in the British Sovereign's Sceptre.</li>
  <li><strong>Lab-grown is now ~50% of US engagement market by units.</strong> Five years ago: ~5%.</li>
</ol>

<h2>Cultural curiosities</h2>
<ul>
  <li>Romans believed diamonds were splinters of fallen stars.</li>
  <li>Indian kings wore them to ward off enemies in battle.</li>
  <li>Victorian Britain popularized the diamond engagement ring after Prince Albert proposed to Queen Victoria with one.</li>
  <li>The "Hope Diamond" carries a curse story largely invented by jeweller Pierre Cartier as marketing.</li>
</ul>

<p>For real history of the trade, see <a href="/blog/famous-diamonds">famous
diamonds</a>. For modern market dynamics, see <a href="/blog/diamond-price-trends">
price trends</a>.</p>
'''


EN['famous-diamonds'] = '''
<aside style="margin:0 0 22px;padding:16px 20px;background:linear-gradient(180deg,#fffdf7,#fbf3df);border-left:4px solid #c9a45c;border-radius:8px">
  <div style="font-size:10.5px;letter-spacing:.22em;text-transform:uppercase;color:#8a6e30;font-weight:700;margin-bottom:6px">TL;DR</div>
  The 10 most famous diamonds in history each tell a story of empire, theft,
  craft, and obsession. Cullinan, Hope, Koh-i-Noor, Tiffany Yellow, Centenary —
  these are the stones every gemologist memorizes.
</aside>

<h2>The 10 you should know</h2>
<ol>
  <li><strong>Cullinan (3,106 ct rough)</strong> — found 1905, South Africa. Cut into 9 major stones; Cullinan I (530.4 ct) is the largest faceted clear diamond on earth, set in the British Sovereign's Sceptre.</li>
  <li><strong>Hope Diamond (45.52 ct, blue)</strong> — Smithsonian, Washington DC. Famed "curse" mostly invented by Pierre Cartier as marketing. Worth ~US$250M.</li>
  <li><strong>Koh-i-Noor (105.6 ct)</strong> — currently in the British Crown Jewels (Queen Mother's crown). India, Pakistan, Iran, and Afghanistan all formally claim it.</li>
  <li><strong>Tiffany Yellow (128.54 ct, fancy yellow)</strong> — discovered 1877, Kimberley. Cut by Tiffany &amp; Co.; only 4 women have worn it (most recently Beyoncé in 2021).</li>
  <li><strong>Centenary (273.85 ct, D-Flawless)</strong> — De Beers' 100th anniversary stone (1988). Largest D-Flawless modern brilliant.</li>
  <li><strong>Pink Star (59.6 ct, vivid pink)</strong> — sold US$71.2M in 2017, second-highest auction price ever for a gem.</li>
  <li><strong>Oppenheimer Blue (14.62 ct, fancy vivid blue)</strong> — sold US$57.5M in 2016; among rarest natural blues.</li>
  <li><strong>Sancy (55.23 ct, pale yellow)</strong> — Louvre. Passed through Henry IV, James I, Cardinal Mazarin, Louis XIV — quintessential European royal stone.</li>
  <li><strong>Regent (140.64 ct)</strong> — Louvre. Once owned by Napoleon (set in his sword pommel). Found 1698 in India.</li>
  <li><strong>Excelsior (995.2 ct rough)</strong> — found 1893 by an African worker who turned it in for a horse + £150. Cut into 21 stones, several lost to history.</li>
</ol>

<h2>What we learn from them</h2>
<p>Every famous diamond's story includes empire, conflict, and someone who got
the short end. The aesthetic legacy is real, but so is the colonial chain of
custody. Modern ethical jewellery (Kimberley Process certification, lab-grown,
verifiable provenance) addresses these issues — though imperfectly.</p>

<p>For the modern trade structure, see <a href="/blog/diamond-price-trends">
price trends</a> and <a href="/blog/sustainable-diamonds">sustainable
diamonds</a>.</p>
'''


EN['fancy-cuts-guide'] = '''
<aside style="margin:0 0 22px;padding:16px 20px;background:linear-gradient(180deg,#fffdf7,#fbf3df);border-left:4px solid #c9a45c;border-radius:8px">
  <div style="font-size:10.5px;letter-spacing:.22em;text-transform:uppercase;color:#8a6e30;font-weight:700;margin-bottom:6px">TL;DR</div>
  "Fancy cut" means any non-round shape: oval, cushion, princess, emerald,
  pear, marquise, asscher, radiant, heart. They cost 10-25% less per carat
  than rounds and offer distinctive style.
</aside>

<h2>The 9 fancy cuts</h2>
<table style="width:100%;border-collapse:collapse;margin:14px 0">
  <thead><tr style="background:#fbf3df"><th style="padding:6px;border:1px solid #d4c08a">Cut</th><th style="padding:6px;border:1px solid #d4c08a">Origin</th><th style="padding:6px;border:1px solid #d4c08a">Best feature</th></tr></thead>
  <tbody>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Oval</td><td style="padding:6px;border:1px solid #d4c08a">1957 (Lazare Kaplan)</td><td style="padding:6px;border:1px solid #d4c08a">Looks ~10% larger than round, elongates fingers</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Cushion</td><td style="padding:6px;border:1px solid #d4c08a">1700s</td><td style="padding:6px;border:1px solid #d4c08a">Vintage glow, softer flashes</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Princess</td><td style="padding:6px;border:1px solid #d4c08a">1960s (Israel)</td><td style="padding:6px;border:1px solid #d4c08a">Modern square; high brilliance</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Emerald</td><td style="padding:6px;border:1px solid #d4c08a">1500s (originally for emerald gems)</td><td style="padding:6px;border:1px solid #d4c08a">Hall-of-mirrors look; art deco</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Pear</td><td style="padding:6px;border:1px solid #d4c08a">1458 (Lodewyk van Bercken)</td><td style="padding:6px;border:1px solid #d4c08a">Unique; slimming finger</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Marquise</td><td style="padding:6px;border:1px solid #d4c08a">1745 (commissioned by Louis XV)</td><td style="padding:6px;border:1px solid #d4c08a">Largest face-up per carat</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Asscher</td><td style="padding:6px;border:1px solid #d4c08a">1902 (Asscher Brothers)</td><td style="padding:6px;border:1px solid #d4c08a">Square step-cut; vintage</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Radiant</td><td style="padding:6px;border:1px solid #d4c08a">1977 (Henry Grossbard)</td><td style="padding:6px;border:1px solid #d4c08a">Brilliant facets in rectangular outline</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Heart</td><td style="padding:6px;border:1px solid #d4c08a">1400s</td><td style="padding:6px;border:1px solid #d4c08a">Romantic symbol; needs 1ct+ to read clearly</td></tr>
  </tbody>
</table>

<h2>Why fancy cuts cost less</h2>
<p>Diamond rough most often crystallizes in shapes more suited to round
brilliant cutting. Fancy cuts often "use" rough that wasn't ideal for round —
yielding 10-25% per-carat savings. They also retain more weight from rough
than round (round wastes ~50%; cushion wastes ~35%).</p>

<h2>Risks per shape</h2>
<ul>
  <li><strong>Oval &amp; pear</strong> — bow-tie shadow across center. Demand to see in person.</li>
  <li><strong>Princess</strong> — sharp corners chip; insist on V-prongs.</li>
  <li><strong>Emerald &amp; asscher</strong> — open table reveals every flaw; need VS1+ clarity, G+ color.</li>
  <li><strong>Marquise &amp; pear</strong> — pointed tips most fragile; protect with V-prongs.</li>
  <li><strong>Heart</strong> — under 1 ct, the "lobes" don't read clearly. Buy 1.0+ ct.</li>
</ul>

<h2>Fancy color</h2>
<p>Beyond shape, "fancy color" diamonds (yellow, pink, blue, green) are graded
on a separate scale (Fancy Light → Fancy → Fancy Intense → Fancy Vivid).
Vivid pinks and blues set auction records — see
<a href="/blog/famous-diamonds">famous diamonds</a>.</p>

<p>For round buyers, see <a href="/blog/round-cut-deep-dive">round cut deep
dive</a>.</p>
'''


EN['round-cut-deep-dive'] = '''
<aside style="margin:0 0 22px;padding:16px 20px;background:linear-gradient(180deg,#fffdf7,#fbf3df);border-left:4px solid #c9a45c;border-radius:8px">
  <div style="font-size:10.5px;letter-spacing:.22em;text-transform:uppercase;color:#8a6e30;font-weight:700;margin-bottom:6px">TL;DR</div>
  Round brilliant accounts for ~70% of engagement diamonds. Tolkowsky's 1919
  math defined the optimal proportions; modern AGS Ideal extends them.
  Round = maximum brilliance per facet, the safest first-time choice.
</aside>

<h2>The 58-facet anatomy</h2>
<p>A modern round brilliant has 58 facets: 33 above the girdle (1 table + 8 stars
+ 8 bezels + 16 upper halves), 24 below (8 pavilion mains + 16 lower halves),
and 1 culet (often pointed = no culet in modern stones).</p>

<h2>The Tolkowsky proportions</h2>
<table style="width:100%;border-collapse:collapse;margin:14px 0">
  <thead><tr style="background:#fbf3df"><th style="padding:6px;border:1px solid #d4c08a">Parameter</th><th style="padding:6px;border:1px solid #d4c08a">Tolkowsky 1919</th><th style="padding:6px;border:1px solid #d4c08a">Modern Ideal</th><th style="padding:6px;border:1px solid #d4c08a">GIA Excellent range</th></tr></thead>
  <tbody>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Table %</td><td style="padding:6px;border:1px solid #d4c08a">53.0</td><td style="padding:6px;border:1px solid #d4c08a">55-57</td><td style="padding:6px;border:1px solid #d4c08a">53-58</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Crown angle</td><td style="padding:6px;border:1px solid #d4c08a">34.5°</td><td style="padding:6px;border:1px solid #d4c08a">34-35°</td><td style="padding:6px;border:1px solid #d4c08a">31-37°</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Pavilion angle</td><td style="padding:6px;border:1px solid #d4c08a">40.75°</td><td style="padding:6px;border:1px solid #d4c08a">40.6-41.0°</td><td style="padding:6px;border:1px solid #d4c08a">40.6-41.8°</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Total depth %</td><td style="padding:6px;border:1px solid #d4c08a">59.3</td><td style="padding:6px;border:1px solid #d4c08a">60.5-62.0</td><td style="padding:6px;border:1px solid #d4c08a">60.5-62.5</td></tr>
  </tbody>
</table>

<h2>Why the Tolkowsky math wins</h2>
<p>At pavilion 40.75° + crown 34.5°, all light entering the table reflects off
the pavilion at angles greater than the critical angle (24.4° from normal),
total-internal-reflects across the diamond, and exits the crown facets — that's
brilliance. Steeper or shallower angles "leak" light through the pavilion,
which is why edge-of-Excellent stones look duller. See <a href="/blog/hearts-arrows-truth">
the H&amp;A truth article</a>.</p>

<h2>Buying recommendations</h2>
<ul>
  <li>Insist on table 55-57%, crown 34-35°, pavilion 40.6-41.0°.</li>
  <li>Total depth 60.5-62.0%.</li>
  <li>Polish &amp; symmetry: Excellent.</li>
  <li>Verify with the <a href="/">BrillianceLab calculator</a> — score 90+ is true ideal.</li>
</ul>

<p>For other shapes, see <a href="/blog/fancy-cuts-guide">fancy cuts guide</a>
and <a href="/blog/diamond-shapes">all 10 shapes</a>.</p>
'''


EN['moissanite-vs-cz-vs-lab'] = '''
<aside style="margin:0 0 22px;padding:16px 20px;background:linear-gradient(180deg,#fffdf7,#fbf3df);border-left:4px solid #c9a45c;border-radius:8px">
  <div style="font-size:10.5px;letter-spacing:.22em;text-transform:uppercase;color:#8a6e30;font-weight:700;margin-bottom:6px">TL;DR</div>
  Lab diamond = chemically diamond. Moissanite = silicon carbide, more fire
  than diamond, very durable. CZ = cubic zirconia, soft and dulls within
  2-3 years. Lab and moissanite are both legitimate; CZ is for costume.
</aside>

<h2>Side-by-side</h2>
<table style="width:100%;border-collapse:collapse;margin:14px 0">
  <thead><tr style="background:#fbf3df"><th style="padding:6px;border:1px solid #d4c08a">Property</th><th style="padding:6px;border:1px solid #d4c08a">Diamond (lab or natural)</th><th style="padding:6px;border:1px solid #d4c08a">Moissanite</th><th style="padding:6px;border:1px solid #d4c08a">CZ</th></tr></thead>
  <tbody>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Composition</td><td style="padding:6px;border:1px solid #d4c08a">Pure carbon</td><td style="padding:6px;border:1px solid #d4c08a">Silicon carbide (SiC)</td><td style="padding:6px;border:1px solid #d4c08a">Zirconium dioxide (ZrO₂)</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Mohs hardness</td><td style="padding:6px;border:1px solid #d4c08a">10</td><td style="padding:6px;border:1px solid #d4c08a">9.25</td><td style="padding:6px;border:1px solid #d4c08a">8.5</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Refractive index</td><td style="padding:6px;border:1px solid #d4c08a">2.42</td><td style="padding:6px;border:1px solid #d4c08a">2.65 (more fire)</td><td style="padding:6px;border:1px solid #d4c08a">2.16 (less fire)</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Dispersion (fire)</td><td style="padding:6px;border:1px solid #d4c08a">0.044</td><td style="padding:6px;border:1px solid #d4c08a">0.104 (rainbow flash)</td><td style="padding:6px;border:1px solid #d4c08a">0.060</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Price (1ct equivalent)</td><td style="padding:6px;border:1px solid #d4c08a">NT$35K (lab) / NT$200K (natural)</td><td style="padding:6px;border:1px solid #d4c08a">NT$5-10K</td><td style="padding:6px;border:1px solid #d4c08a">NT$300-1K</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Lifespan looking new</td><td style="padding:6px;border:1px solid #d4c08a">Forever</td><td style="padding:6px;border:1px solid #d4c08a">Forever</td><td style="padding:6px;border:1px solid #d4c08a">2-3 years (clouds, scratches)</td></tr>
  </tbody>
</table>

<h2>How to tell them apart</h2>
<ul>
  <li><strong>Diamond test pen</strong> (thermal) — diamond passes, moissanite usually passes too (high thermal conductivity), CZ fails.</li>
  <li><strong>Moissanite tester</strong> (electrical) — distinguishes moissanite from diamond.</li>
  <li><strong>Loupe</strong> — moissanite shows "doubling" of facet edges (it's birefringent); diamond doesn't.</li>
  <li><strong>Fire</strong> — moissanite throws more rainbow flash than diamond. Some find this "showy".</li>
  <li><strong>Weight</strong> — moissanite is ~15% lighter than diamond at same dimensions.</li>
</ul>

<h2>When to choose each</h2>
<ul>
  <li><strong>Lab diamond</strong> — best balance of price, optics, status. The default modern choice.</li>
  <li><strong>Moissanite</strong> — maximum dollar/sparkle ratio; great for travel rings, second sets.</li>
  <li><strong>CZ</strong> — costume only; do not use for engagement rings.</li>
</ul>

<p>For natural vs lab depth, see <a href="/blog/lab-vs-natural">lab vs natural</a>.
For other gemstones, see <a href="/blog/gemstones-comparison">gemstones
comparison</a>.</p>
'''


EN['gemstones-comparison'] = '''
<aside style="margin:0 0 22px;padding:16px 20px;background:linear-gradient(180deg,#fffdf7,#fbf3df);border-left:4px solid #c9a45c;border-radius:8px">
  <div style="font-size:10.5px;letter-spacing:.22em;text-transform:uppercase;color:#8a6e30;font-weight:700;margin-bottom:6px">TL;DR</div>
  Diamond, sapphire, ruby, emerald — the "big four" precious gems. Sapphire
  and ruby (both corundum, Mohs 9) are durable engagement alternatives;
  emerald is fragile. Each has a different price-per-carat curve.
</aside>

<h2>The big four</h2>
<table style="width:100%;border-collapse:collapse;margin:14px 0">
  <thead><tr style="background:#fbf3df"><th style="padding:6px;border:1px solid #d4c08a">Stone</th><th style="padding:6px;border:1px solid #d4c08a">Mohs</th><th style="padding:6px;border:1px solid #d4c08a">Engagement-suitable?</th><th style="padding:6px;border:1px solid #d4c08a">1ct fine quality</th></tr></thead>
  <tbody>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Diamond</td><td style="padding:6px;border:1px solid #d4c08a">10</td><td style="padding:6px;border:1px solid #d4c08a">★★★★★</td><td style="padding:6px;border:1px solid #d4c08a">NT$200K (natural)</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Sapphire (blue)</td><td style="padding:6px;border:1px solid #d4c08a">9</td><td style="padding:6px;border:1px solid #d4c08a">★★★★★</td><td style="padding:6px;border:1px solid #d4c08a">NT$30-150K</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Ruby</td><td style="padding:6px;border:1px solid #d4c08a">9</td><td style="padding:6px;border:1px solid #d4c08a">★★★★☆</td><td style="padding:6px;border:1px solid #d4c08a">NT$80-500K (varies)</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Emerald</td><td style="padding:6px;border:1px solid #d4c08a">7.5-8</td><td style="padding:6px;border:1px solid #d4c08a">★★★☆☆ (fragile)</td><td style="padding:6px;border:1px solid #d4c08a">NT$100-400K (Colombian)</td></tr>
  </tbody>
</table>

<h2>The "next tier"</h2>
<ul>
  <li><strong>Tanzanite</strong> — found only in Tanzania; bluish-violet; Mohs 6.5-7 (avoid daily wear).</li>
  <li><strong>Spinel</strong> — historic confusion with ruby (the "Black Prince's Ruby" is actually spinel). Mohs 8.</li>
  <li><strong>Aquamarine</strong> — pale blue beryl; Mohs 7.5-8.</li>
  <li><strong>Tourmaline</strong> — many colors; Mohs 7-7.5.</li>
  <li><strong>Garnet</strong> — beyond burgundy: tsavorite (green), spessartine (orange). Mohs 6.5-7.5.</li>
  <li><strong>Topaz</strong> — imperial topaz (peach) is the prized variety; Mohs 8.</li>
</ul>

<h2>Treatments to know</h2>
<ul>
  <li><strong>Sapphire heat treatment</strong> — universal for blue sapphire; "unheated" commands 2-5× premium.</li>
  <li><strong>Ruby glass-filling</strong> — common for cheap rubies; durability is poor. Avoid.</li>
  <li><strong>Emerald oiling</strong> — universal; "no oil" or "minor oil" commands premium.</li>
  <li><strong>Diamond HPHT/laser</strong> — must be disclosed on GIA report.</li>
</ul>

<h2>For an alternative engagement stone</h2>
<p>Best non-diamond pick: <strong>blue sapphire</strong> (Princess Diana / Kate Middleton ring).
Mohs 9, vivid color, no chip risk, ~70% cheaper than diamond per carat.
Second choice: <strong>ruby</strong> for the symbolism. Avoid emerald for daily-wear rings —
oil dries out, fractures grow. See <a href="/blog/lgbtq-rings">LGBTQ rings</a>
for color stone trends in modern engagement.</p>
'''


EN['sustainable-diamonds'] = '''
<aside style="margin:0 0 22px;padding:16px 20px;background:linear-gradient(180deg,#fffdf7,#fbf3df);border-left:4px solid #c9a45c;border-radius:8px">
  <div style="font-size:10.5px;letter-spacing:.22em;text-transform:uppercase;color:#8a6e30;font-weight:700;margin-bottom:6px">TL;DR</div>
  "Ethical diamonds" usually means: lab-grown (no mining footprint), Canadian
  natural (verifiable supply chain), or recycled (re-cut antique stones).
  Kimberley Process exists but has known gaps. Lab is currently the most
  defensible choice on environmental + provenance grounds.
</aside>

<h2>The four sustainability paths</h2>
<ol>
  <li><strong>Lab-grown</strong> — zero mining; energy footprint depends on grid. Indian CVD on coal grid is high; US lab on solar/hydro is very low.</li>
  <li><strong>Canadian natural</strong> — fully traceable from mine to retail (Maple Leaf, CanadaMark certifications). Higher labor + environmental standards than typical mines.</li>
  <li><strong>Recycled / antique</strong> — re-cut from estate jewellery; no new extraction. Some loss in cutting (~10-30% mass).</li>
  <li><strong>Fairmined / Fairtrade Gold setting</strong> — paired with any of the above; addresses gold mining's mercury &amp; child-labor issues.</li>
</ol>

<h2>The Kimberley Process — what it does and doesn't cover</h2>
<p>Founded 2003, KP certifies that rough diamonds are not from rebel-controlled
zones funding armed conflict. It does <em>not</em> cover:</p>
<ul>
  <li>Government-perpetrated human rights abuses (Zimbabwe Marange).</li>
  <li>Worker safety, child labor, or fair wages.</li>
  <li>Environmental damage.</li>
  <li>Smuggling that bypasses the certification chain.</li>
</ul>
<p>Industry consensus: KP catches the worst (financing rebel groups) but is not
a guarantee of "ethical".</p>

<h2>Carbon footprint — the messy comparison</h2>
<table style="width:100%;border-collapse:collapse;margin:14px 0">
  <thead><tr style="background:#fbf3df"><th style="padding:6px;border:1px solid #d4c08a">Source</th><th style="padding:6px;border:1px solid #d4c08a">kg CO₂ per ct (estimate)</th></tr></thead>
  <tbody>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Natural mining (Botswana avg.)</td><td style="padding:6px;border:1px solid #d4c08a">~160</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Lab CVD (India coal grid)</td><td style="padding:6px;border:1px solid #d4c08a">~510</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Lab CVD (renewable grid)</td><td style="padding:6px;border:1px solid #d4c08a">~50</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Recycled / vintage</td><td style="padding:6px;border:1px solid #d4c08a">~10 (re-cut energy only)</td></tr>
  </tbody>
</table>
<p>Numbers vary widely by source; the takeaway: "lab is greener" is conditional
on the grid mix.</p>

<h2>What to ask your jeweller</h2>
<ul>
  <li>"Where was the rough mined? Can you trace it?"</li>
  <li>"Is the gold setting Fairmined or recycled?"</li>
  <li>"For lab — which production facility? What's their energy source?"</li>
  <li>"Do you offer a verified provenance report?"</li>
</ul>

<p>For natural-vs-lab depth, see <a href="/blog/lab-vs-natural">lab vs
natural</a>. For market trends shaping this, see <a href="/blog/diamond-price-trends">
price trends</a>.</p>
'''


EN['diamond-photography'] = '''
<aside style="margin:0 0 22px;padding:16px 20px;background:linear-gradient(180deg,#fffdf7,#fbf3df);border-left:4px solid #c9a45c;border-radius:8px">
  <div style="font-size:10.5px;letter-spacing:.22em;text-transform:uppercase;color:#8a6e30;font-weight:700;margin-bottom:6px">TL;DR</div>
  Phone-camera diamond photos disappoint because diamond brilliance is dynamic
  motion-light. Solution: macro lens, point light source, slight tilt during
  capture, dark background. 5 setup tricks transform results.
</aside>

<h2>Why phone shots look dead</h2>
<p>Diamonds throw color (fire), white sparkle (scintillation), and brilliance
through facet motion. A static photo at 4-meter focus distance compresses all
of that into one frozen reflection — usually a single white blob. The eye-
beating dynamic range gets clipped into a JPEG.</p>

<h2>5 setup tricks</h2>
<ol>
  <li><strong>Macro lens (clip-on or smartphone macro)</strong> — get the camera 4-8 cm from the diamond. Suddenly individual facets fire.</li>
  <li><strong>Single point light source</strong> — a desk lamp at 30° angle, or even one phone flashlight, beats overhead fluorescent.</li>
  <li><strong>Dark background</strong> — black velvet or matte black card. Removes reflections of clutter.</li>
  <li><strong>Slight tilt motion during burst capture</strong> — record a 1-second video, scrub for the frame with most fire. Diamond brilliance is in the motion.</li>
  <li><strong>Clean the stone first</strong> — finger oil dims sparkle dramatically. Dish-soap clean + lint-free polish.</li>
</ol>

<h2>For online sellers / social media</h2>
<table style="width:100%;border-collapse:collapse;margin:14px 0">
  <thead><tr style="background:#fbf3df"><th style="padding:6px;border:1px solid #d4c08a">Shot</th><th style="padding:6px;border:1px solid #d4c08a">Setup</th></tr></thead>
  <tbody>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Face-up sparkle</td><td style="padding:6px;border:1px solid #d4c08a">Macro + single LED + dark bg + 30° camera tilt</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Side profile (proportions)</td><td style="padding:6px;border:1px solid #d4c08a">Diffused even light, white background, perpendicular angle</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">On-finger lifestyle</td><td style="padding:6px;border:1px solid #d4c08a">Soft window light + skin-tone-matched fabric drape</td></tr>
    <tr><td style="padding:6px;border:1px solid #d4c08a">Hearts &amp; Arrows view</td><td style="padding:6px;border:1px solid #d4c08a">H&amp;A scope (NT$300 on Shopee) + macro phone</td></tr>
  </tbody>
</table>

<h2>Editing principles</h2>
<ul>
  <li>Don't crush blacks — you'll lose facet structure.</li>
  <li>Don't oversaturate — fancy color stones look fake when boosted.</li>
  <li>Sharpen mildly; over-sharpening creates halos around facet edges.</li>
  <li>Disclose any editing on for-sale listings (legal in some jurisdictions).</li>
</ul>

<p>For a thoughtful proposal photoshoot, see <a href="/blog/proposal-speech">
proposal speech</a> for setting context.</p>
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
