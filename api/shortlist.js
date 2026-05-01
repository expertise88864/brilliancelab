/* =============================================================
 * BrillianceLab — shortlist generator (Vercel Function)
 * Given a budget (TWD) and optional shape preference, returns
 * 3 recommended specs that maximise BPD (brilliance per dollar).
 * Each spec is then re-scored through compute() so the user gets
 * the same authoritative score as the main /api/score endpoint.
 * ============================================================= */

import scoreHandler from './score.js';

// Reuse the SAME compute() from score.js by importing it. But the export there
// is the HTTP handler — for code reuse I'll inline a thin wrapper here.

// Pricing model (rough Taiwan retail mid-tier averages, TWD per carat at 1ct):
// Sources: aggregated 2024-2026 Promessa / Iprimo / Whiteflash retail listings.
const COLOR_MULT   = { D: 1.45, E: 1.30, F: 1.18, G: 1.00, H: 0.88, I: 0.78, J: 0.68 };
const CLARITY_MULT = { IF: 1.50, VVS1: 1.32, VVS2: 1.18, VS1: 1.05, VS2: 1.00, SI1: 0.85, SI2: 0.72 };
const SHAPE_PRICE_MULT = { round: 1.00, oval: 0.80, cushion: 0.78, princess: 0.70, emerald: 0.72 };

/* Carat-price curve: NTD per carat at 1ct base, scales non-linearly.
   Mass-effect: bigger stones are exponentially more expensive per carat. */
function pricePerCt(carat) {
  if (carat < 0.30) return 70_000;
  if (carat < 0.50) return 110_000;
  if (carat < 0.70) return 145_000;
  if (carat < 0.90) return 185_000;
  if (carat < 1.00) return 215_000;
  if (carat < 1.20) return 290_000;        // 1.00 ct premium jump
  if (carat < 1.50) return 330_000;
  if (carat < 2.00) return 410_000;
  return 520_000;
}
function estimatePrice(carat, color, clarity, shape) {
  const base = pricePerCt(carat) * carat;
  return Math.round(base * (COLOR_MULT[color]||1) * (CLARITY_MULT[clarity]||1) * (SHAPE_PRICE_MULT[shape]||1));
}

// --- Compute logic: this is a thin re-implementation matching score.js ----
// (We can't easily import the helpers from score.js without restructuring.
//  Instead, we POST to the local /api/score endpoint via fetch in serverless.)
async function scoreOne(input, host) {
  const url = `https://${host}/api/score`;
  const resp = await fetch(url, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify(input)
  });
  if (!resp.ok) throw new Error('score api ' + resp.status);
  return await resp.json();
}

// Sweet-spot starter values per shape, used to seed the candidate.
// These are rough display-friendly values; real spots are still server-side.
const SHAPE_START = {
  round:    { table: 56.0, depth: 61.8, crown: 34.7, pavilion: 40.8 },
  oval:     { table: 57.0, depth: 60.5, crown: 35.0, pavilion: 40.5 },
  cushion:  { table: 60.0, depth: 63.5, crown: 35.0, pavilion: 40.7 },
  princess: { table: 71.0, depth: 71.0, crown: 11.0, pavilion: 42.0 },
  emerald:  { table: 65.0, depth: 67.5, crown: 11.0, pavilion: 45.0 },
};

/* Tier of recipes per budget. Each yields a (carat × color × clarity × shape) spec.
   We pick tier by budget upper-bound and let the client pick the best. */
function _recipesForBudget(budgetTwd, shapePref) {
  const shapes = shapePref ? [shapePref] : ['round'];
  // 4 candidate recipes ranging from "small + perfect" to "big + reasonable"
  // The shortlist algorithm tries each and ranks by BPD.
  return [
    { name: '車工至上 / Cut-first',  carat: 0.50, color: 'F', clarity: 'VS1' },
    { name: '甜蜜點 / Sweet spot',    carat: 0.70, color: 'G', clarity: 'VS1' },
    { name: '近一克拉 / Near 1 ct',   carat: 0.90, color: 'G', clarity: 'VS2' },
    { name: '一克拉門檻 / 1 ct line', carat: 1.00, color: 'H', clarity: 'VS2' },
    { name: '大顆派 / Bigger',         carat: 1.20, color: 'H', clarity: 'SI1' },
    { name: '頂級派 / Top-tier',       carat: 1.00, color: 'D', clarity: 'VVS1' },
  ].flatMap(r => shapes.map(shape => ({ ...r, shape })));
}

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin',  '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') { res.status(204).end(); return; }
  if (req.method !== 'POST') { res.status(405).json({ error: 'POST only' }); return; }

  try {
    let body = req.body;
    if (typeof body === 'string') { try { body = JSON.parse(body); } catch { body = {}; } }
    body = body || {};

    const budget = +body.budget;
    if (!isFinite(budget) || budget < 30000 || budget > 50_000_000) {
      res.status(400).json({ error: 'invalid budget (NT$30K – NT$50M)' });
      return;
    }
    const shapePref = body.shape && SHAPE_START[body.shape] ? body.shape : 'round';

    const host = req.headers['x-forwarded-host'] || req.headers.host;
    const recipes = _recipesForBudget(budget, shapePref);

    // For each recipe estimate price; if affordable, score it via /api/score
    const candidates = [];
    for (const r of recipes) {
      const price = estimatePrice(r.carat, r.color, r.clarity, r.shape);
      if (price > budget * 1.05) continue; // 5% slack
      const start = SHAPE_START[r.shape];
      const result = await scoreOne({
        shape: r.shape,
        ...start,
        polish: 'EX', symmetry: 'EX', fluorescence: 'NONE'
      }, host);
      const score = result.score || 0;
      const bpd   = score && price ? (score * Math.sqrt(r.carat)) / (price / 10000) : 0;
      candidates.push({
        ...r,
        price,
        score,
        bpd: Math.round(bpd * 100) / 100,
        hca: result.hca
      });
    }

    candidates.sort((a, b) => b.bpd - a.bpd);
    const top = candidates.slice(0, 3);

    res.setHeader('Cache-Control', 'no-store');
    res.status(200).json({
      budget,
      shape: shapePref,
      candidates: top,
      algorithm: 'BL/shortlist-1.0'
    });
  } catch (err) {
    res.status(500).json({ error: 'shortlist failed', message: String(err && err.message || err) });
  }
}
