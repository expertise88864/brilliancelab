/* =============================================================
 * BrillianceLab — server-side scoring (Vercel Function)
 * The full proprietary algorithm lives ONLY here.
 * The browser only knows: send 4 numbers, receive a score.
 * =============================================================
 *
 * Inputs (POST JSON body):
 *   {
 *     table:    Number,   // %
 *     depth:    Number,   // %
 *     crown:    Number,   // °
 *     pavilion: Number,   // °
 *     starLength?: Number,    // %, default 50
 *     lowerGirdle?: Number,   // %, default 80
 *     polish?:       'EX'|'VG'|'G'|'F',
 *     symmetry?:     'EX'|'VG'|'G'|'F',
 *     fluorescence?: 'NONE'|'FAINT'|'MEDIUM'|'STRONG'|'VS'
 *   }
 *
 * Output:
 *   {
 *     score:           Number,   // 0..100 composite
 *     hca: {                     // 4-dimensional Holloway-style breakdown
 *       lightReturn:   Number,   // brilliance, 0..100 higher=better
 *       fire:          Number,
 *       scintillation: Number,
 *       spread:        Number,
 *     },
 *     detail: { [axis]: { value, deviation, tier } },
 *     totalDeduction:  Number,
 *     harmony:         Number,   // crown + 2*pavilion
 *     algorithm:       'BL/3.1'
 *   }
 */

// ---------- Hidden constants (server-only) ----------
// Per-shape sweet spots. Each shape has its own optical optimum derived from
// industry references (Tolkowsky for round; AGS / GIA cushion / oval modifiers
// for the others). Princess uses an entirely different geometry (much smaller
// crown angle, much larger table) so the bounds shift accordingly.
const SHAPES = {
  round: {
    table:    { spot: 55.5, mul: 8,  tiers: [0.5, 1.5], min: 50, max: 62 },
    depth:    { spot: 61.7, mul: 10, tiers: [0.3, 0.8], min: 58, max: 66 },
    crown:    { spot: 34.5, mul: 20, tiers: [0.2, 0.5], min: 30, max: 38 },
    pavilion: { spot: 40.8, mul: 30, tiers: [0.1, 0.2], min: 38, max: 43 },
    harmonyTarget: 116.1, harmonyBand: 1.0,
  },
  oval: {
    table:    { spot: 57.0, mul: 7,  tiers: [1.0, 2.5], min: 53, max: 64 },
    depth:    { spot: 60.5, mul: 8,  tiers: [1.0, 2.0], min: 56, max: 66 },
    crown:    { spot: 35.0, mul: 16, tiers: [0.5, 1.2], min: 30, max: 38 },
    pavilion: { spot: 40.5, mul: 26, tiers: [0.3, 0.6], min: 38, max: 43 },
    harmonyTarget: 115.5, harmonyBand: 1.4,
  },
  cushion: {
    table:    { spot: 60.0, mul: 6,  tiers: [1.5, 3.0], min: 53, max: 70 },
    depth:    { spot: 63.5, mul: 7,  tiers: [1.0, 2.0], min: 58, max: 70 },
    crown:    { spot: 35.0, mul: 14, tiers: [0.7, 1.5], min: 28, max: 40 },
    pavilion: { spot: 40.5, mul: 24, tiers: [0.4, 0.9], min: 38, max: 44 },
    harmonyTarget: 115.5, harmonyBand: 1.6,
  },
  princess: {
    table:    { spot: 70.0, mul: 5,  tiers: [2.0, 4.0], min: 60, max: 80 },
    depth:    { spot: 71.0, mul: 7,  tiers: [1.5, 2.8], min: 65, max: 80 },
    crown:    { spot: 11.0, mul: 14, tiers: [1.0, 2.0], min: 8,  max: 15 },
    pavilion: { spot: 42.0, mul: 22, tiers: [0.6, 1.2], min: 38, max: 48 },
    harmonyTarget:  95.0, harmonyBand: 2.0,    // 11 + 2*42 = 95, very different geometry
  },
  emerald: {
    table:    { spot: 64.0, mul: 5,  tiers: [2.0, 4.0], min: 55, max: 75 },
    depth:    { spot: 67.5, mul: 7,  tiers: [1.5, 3.0], min: 60, max: 75 },
    crown:    { spot: 11.0, mul: 12, tiers: [1.0, 2.5], min: 6,  max: 18 },
    pavilion: { spot: 45.0, mul: 18, tiers: [0.8, 1.6], min: 40, max: 50 },
    harmonyTarget: 101.0, harmonyBand: 2.5,    // step-cut, very different geometry
  },
};

function _shapeOf(input) {
  const k = String(input.shape || 'round').toLowerCase();
  return SHAPES[k] ? k : 'round';
}

const CORE = {
  // Tolkowsky harmony: crown + 2 * pavilion ≈ 116.1°
  harmonyTarget: 116.1,
  harmonyBand:   1.0,
  harmonyWeight: 2.0,
  // Penalty curve & asymmetry
  tailAccel:     1.55,
  pavSkewDeep:   1.25,
  // Hard cap if any axis is off-spec
  capWhenOff:    74,
};

const ADV_PEN = {
  polish:       { EX: 0, VG: 1.5, G: 4,   F: 9  },
  symmetry:     { EX: 0, VG: 2,   G: 6,   F: 11 },
  fluorescence: { NONE: 0, FAINT: 0, MEDIUM: 1.5, STRONG: 4, VS: 7 },
};

// HCA 4-dimensional weighting matrix.
// Each row: how much THIS dimension is hurt by penalty on AXIS X.
const HCA_WEIGHTS = {
  // Brilliance is dominated by pavilion, then depth, then crown.
  lightReturn:   { table: 0.10, depth: 0.45, crown: 0.20, pavilion: 1.00 },
  // Fire is rainbow flashes — crown rules; table/pavilion supporting.
  fire:          { table: 0.30, depth: 0.10, crown: 1.00, pavilion: 0.30 },
  // Scintillation: dynamic flicker — sensitive to facet precision (table/symmetry/star/lg).
  scintillation: { table: 0.45, depth: 0.15, crown: 0.30, pavilion: 0.30 },
  // Spread: face-up apparent size for the carat — depth/table dominate.
  spread:        { table: 0.40, depth: 1.00, crown: 0.05, pavilion: 0.05 },
};

// ---------- Math ----------

function clamp(v, lo, hi) { return Math.max(lo, Math.min(hi, v)); }

function axisPen(SS, key, value) {
  const c = SS[key];
  const dev = value - c.spot;          // signed
  const adev = Math.abs(dev);
  let mul = c.mul;
  if (key === 'pavilion' && dev > 0) mul *= CORE.pavSkewDeep;

  const [tI, tG] = c.tiers;
  if (adev <= tI) return adev * mul * 0.6;                                 // forgiving
  if (adev <= tG) return tI * mul * 0.6 + (adev - tI) * mul * 1.0;          // linear
  const past = adev - tG;
  return tI * mul * 0.6
       + (tG - tI) * mul * 1.0
       + past * mul * CORE.tailAccel
       + Math.pow(past, 1.4) * mul * 0.18;                                  // tail
}

function tierFor(SS, key, value) {
  const c = SS[key];
  const dev = Math.abs(value - c.spot);
  if (dev <= c.tiers[0]) return 'ideal';
  if (dev <= c.tiers[1]) return 'good';
  return 'off';
}

function compute(input) {
  const shape = _shapeOf(input);
  const SS = SHAPES[shape];

  const v = {
    table:    clampInput(+input.table,    SS.table.spot,    SS.table.min,    SS.table.max),
    depth:    clampInput(+input.depth,    SS.depth.spot,    SS.depth.min,    SS.depth.max),
    crown:    clampInput(+input.crown,    SS.crown.spot,    SS.crown.min,    SS.crown.max),
    pavilion: clampInput(+input.pavilion, SS.pavilion.spot, SS.pavilion.min, SS.pavilion.max),
  };
  const adv = {
    starLength:   clampInput(+input.starLength,  50, 30, 70),
    lowerGirdle:  clampInput(+input.lowerGirdle, 80, 60, 95),
    polish:       (input.polish       in ADV_PEN.polish)       ? input.polish       : 'EX',
    symmetry:     (input.symmetry     in ADV_PEN.symmetry)     ? input.symmetry     : 'EX',
    fluorescence: (input.fluorescence in ADV_PEN.fluorescence) ? input.fluorescence : 'NONE',
  };

  // ---------- Per-axis penalties ----------
  const pen = {
    table:    axisPen(SS, 'table',    v.table),
    depth:    axisPen(SS, 'depth',    v.depth),
    crown:    axisPen(SS, 'crown',    v.crown),
    pavilion: axisPen(SS, 'pavilion', v.pavilion),
  };
  const advStarPen = Math.abs(adv.starLength  - 50) * 0.4;
  const advLgPen   = Math.abs(adv.lowerGirdle - 80) * 0.3;
  const polPen     = ADV_PEN.polish[adv.polish] || 0;
  const symPen     = ADV_PEN.symmetry[adv.symmetry] || 0;
  const fluPen     = ADV_PEN.fluorescence[adv.fluorescence] || 0;

  // ---------- Composite score ----------
  let composite = 100 - (pen.table + pen.depth + pen.crown + pen.pavilion);

  // Tolkowsky cross-axis harmony (shape-specific target & band)
  const harmony  = v.crown + 2 * v.pavilion;
  const hTarget  = SS.harmonyTarget ?? CORE.harmonyTarget;
  const hBand    = SS.harmonyBand   ?? CORE.harmonyBand;
  const hDev = Math.abs(harmony - hTarget);
  if (hDev > hBand) composite -= (hDev - hBand) * CORE.harmonyWeight;

  // Advanced contributions
  composite -= advStarPen + advLgPen + polPen + symPen + fluPen;

  // Per-axis detail
  const detail = {};
  for (const k of ['table','depth','crown','pavilion']) {
    detail[k] = {
      value: v[k],
      deviation: round2(Math.abs(v[k] - SS[k].spot)),
      tier: tierFor(SS, k, v[k]),
    };
  }
  // Hard cap when any axis is off-spec
  const anyOff = Object.values(detail).some((d) => d.tier === 'off');
  if (anyOff) composite = Math.min(composite, CORE.capWhenOff);
  composite = clamp(composite, 0, 100);

  // ---------- HCA 4-dimensional breakdown ----------
  // Each dimension starts at 100 then deducts a *weighted* sum of axis penalties
  // plus dimension-specific finishing penalties. All clamped to [0,100].
  const hcaRaw = {};
  for (const dim of Object.keys(HCA_WEIGHTS)) {
    const w = HCA_WEIGHTS[dim];
    let s = 100
      - pen.table    * w.table
      - pen.depth    * w.depth
      - pen.crown    * w.crown
      - pen.pavilion * w.pavilion;

    if (dim === 'fire') {
      if (hDev > hBand) s -= (hDev - hBand) * 1.4;
      s -= polPen * 0.3;
    } else if (dim === 'lightReturn') {
      if (hDev > hBand) s -= (hDev - hBand) * 1.6;
    } else if (dim === 'scintillation') {
      s -= advStarPen * 1.6;
      s -= advLgPen * 1.6;
      s -= symPen * 1.6;
      s -= polPen * 1.0;
    } else if (dim === 'spread') {
      // Face-up size: deep stones look smaller for same carat. Asymmetric — only deep hurts.
      const depthOver = Math.max(0, v.depth - SS.depth.spot);
      s -= depthOver * 6;
      const deepThreshold = SS.depth.spot + 1.8;
      if (v.depth > deepThreshold) s -= (v.depth - deepThreshold) * 8;
    }

    hcaRaw[dim] = clamp(s, 0, 100);
  }
  // Apply same hard-cap behaviour proportionally if any axis is off
  if (anyOff) {
    for (const dim of Object.keys(hcaRaw)) {
      hcaRaw[dim] = Math.min(hcaRaw[dim], CORE.capWhenOff + 8); // slight headroom
    }
  }

  return {
    shape,
    score:          round2(composite),
    hca: {
      lightReturn:   round1(hcaRaw.lightReturn),
      fire:          round1(hcaRaw.fire),
      scintillation: round1(hcaRaw.scintillation),
      spread:        round1(hcaRaw.spread),
    },
    detail,
    totalDeduction: round2(100 - composite),
    harmony:        round2(harmony),
    algorithm:      'BL/3.2',
  };
}

function clampInput(v, fallback, lo, hi) {
  if (!Number.isFinite(v)) return fallback;
  return clamp(v, lo, hi);
}
function round1(v) { return Math.round(v * 10) / 10; }
function round2(v) { return Math.round(v * 100) / 100; }

// ---------- Per-IP rate limiter (in-memory, per Vercel container) ----------
// Two windows: short burst guard (60 / minute) and longer ceiling (600 / hour).
// State is per-region/per-instance so it resets on cold start; that's intentional —
// for tighter limits, layer Upstash Redis or Vercel KV on top.
const _rl = new Map();   // ip -> { m: [count, windowStart], h: [count, windowStart] }
const _RL_LIMITS = { perMin: 60, perHour: 600 };

function _clientIp(req) {
  const xf = req.headers['x-forwarded-for'];
  if (xf) return String(xf).split(',')[0].trim();
  return (req.headers['x-real-ip'] || req.socket?.remoteAddress || 'anon');
}

function _checkRate(ip) {
  const now = Date.now();
  let s = _rl.get(ip);
  if (!s) { s = { m: [0, now], h: [0, now] }; _rl.set(ip, s); }
  // GC: prune the map if it gets large
  if (_rl.size > 5000) {
    for (const [k, v] of _rl) {
      if (now - v.h[1] > 3600_000) _rl.delete(k);
      if (_rl.size < 4000) break;
    }
  }
  if (now - s.m[1] > 60_000)   { s.m = [0, now]; }
  if (now - s.h[1] > 3600_000) { s.h = [0, now]; }
  s.m[0]++; s.h[0]++;
  if (s.m[0] > _RL_LIMITS.perMin)  return { ok: false, retry: 60_000   - (now - s.m[1]), kind: 'minute' };
  if (s.h[0] > _RL_LIMITS.perHour) return { ok: false, retry: 3600_000 - (now - s.h[1]), kind: 'hour'   };
  return { ok: true, remaining: _RL_LIMITS.perMin - s.m[0] };
}

// ---------- Vercel handler ----------
export default function handler(req, res) {
  // Permissive CORS (for the same-origin call from /).
  res.setHeader('Access-Control-Allow-Origin',  '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') { res.status(204).end(); return; }
  if (req.method !== 'POST') {
    res.status(405).json({ error: 'POST only' });
    return;
  }

  // ---- Rate limit ----
  const ip = _clientIp(req);
  const rl = _checkRate(ip);
  res.setHeader('X-RateLimit-Limit',     String(_RL_LIMITS.perMin));
  res.setHeader('X-RateLimit-Remaining', String(Math.max(0, rl.remaining ?? 0)));
  if (!rl.ok) {
    res.setHeader('Retry-After', String(Math.max(1, Math.ceil(rl.retry / 1000))));
    res.status(429).json({
      error: 'Too many requests',
      kind:  rl.kind,
      retryAfterSeconds: Math.max(1, Math.ceil(rl.retry / 1000))
    });
    return;
  }

  try {
    // Vercel auto-parses JSON when content-type is application/json
    let body = req.body;
    if (typeof body === 'string') {
      try { body = JSON.parse(body); } catch { body = {}; }
    }
    if (!body || typeof body !== 'object') body = {};
    const result = compute(body);

    res.setHeader('Cache-Control', 'no-store');
    res.setHeader('X-Algorithm',   'BL/3.2');
    res.status(200).json(result);
  } catch (err) {
    res.status(500).json({ error: 'Scoring failed', message: String(err && err.message || err) });
  }
}
