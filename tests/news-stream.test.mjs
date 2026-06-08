#!/usr/bin/env node
// Adverse-media / negative-news stream arc harness (Phase 31 M8; Phase 32 real-source + elevation) —
// ZERO runtime deps (Node built-in `vm` + a hand-rolled DOM shim; no npm install). Run:
//   node tests/news-stream.test.mjs
//
// Loads the COMMITTED dist/news/index.html (so it doubles as a build-output smoke test —
// `build.py --check all` guarantees that file equals a fresh build of news.html), extracts the single
// inline <script>, evaluates it under the shim, and drives the screening arc in BOTH motion modes:
//
//   [reduced-motion] the template is the FINAL resting state → assert the static render:
//     Select (4 REAL gov-enforcement articles) · the fuzzy matcher (normalize → token-sort → Jaro-Winkler)
//     scoring the seeded EXACT hit (Siam Expert 1.000), the NEAR-matches an exact-name screen would miss
//     (Pullman suffix 1.000, Zhdanova suffix 0.989, Nikolay translit 0.973, Puzyreva word-order 1.000,
//     Malachi typo 0.962, Ravenell middle-name 0.950), and the common-name FALSE-POSITIVE trap (George
//     Rossi 1.000, a DIFFERENT person) — dismissable at the human gate, dropping the confirmed count ·
//     Read highlights grounded red-flag phrases + tags entities + shows entity cards with the grounded
//     attributes (location/age/profession) + the typology + the real-source attribution (public domain,
//     17 U.S.C. §105) · Screen shows real scores + a threshold + no fabricated % · Close names the atom.
//
//   [full-motion] an ENRICHED shim (insertAdjacentHTML + classList + a drainable setTimeout) drives the
//     streaming "agent reading" Read (every red-flag phrase + entity occurrence streamed, all entity cards
//     + translate rows revealed, the caret removed, both labels counted up to full) and the scan PROCESS
//     (each surfaced hit row swept in, the counter settled) — no thrown errors.

import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';
import vm from 'node:vm';

const HERE = dirname(fileURLToPath(import.meta.url));
const DIST = resolve(HERE, '..', 'dist', 'news', 'index.html');

let pass = 0;
const fails = [];
function ok(cond, msg) { if (cond) { pass++; console.log(`  ✓ ${msg}`); } else { fails.push(msg); console.log(`  ✗ ${msg}`); } }
function approx(a, b, eps, msg) { ok(typeof a === 'number' && Math.abs(a - b) <= eps, `${msg} (expected ~${b}, got ${a})`); }

const html = readFileSync(DIST, 'utf8');
const open = html.indexOf('<script>');
const close = html.lastIndexOf('</script>');
if (open < 0 || close < 0) { console.error('FATAL: no <script> in', DIST); process.exit(2); }
const SCRIPT = html.slice(open + '<script>'.length, close);

// --- Phase 35: the offline ship artifact must carry NO live-mode code (build-time stripped) ---------
// news.html (the SOURCE template) carries the companion-only live region; build.py render_news strips it
// for dist/news, so the offline single file stays self-contained (zero network code); the live branch is
// served only by scripts/serve_news.py.
{
  const src = readFileSync(resolve(HERE, '..', 'news.html'), 'utf8');
  ok(src.includes('/*LIVE_START*/') && src.includes('liveInit') && src.includes('fetch('),
     'news.html SOURCE carries the live-mode region (served by the companion)');
  ok(!html.includes('/*LIVE_START*/') && !html.includes('liveInit') && !html.includes('fetch('),
     'offline dist/news has the live region STRIPPED (zero network code; self-contained)');
}

ok(/class="badge"/.test(html) && /Illustrative data/.test(html), 'always-on illustrative badge present in the ship chrome');

/* ---------- a DOM/window shim — enriched dynamic nodes + drainable timers ---------- */
const DYN = new Set(['doc', 'entities', 'redflags', 'doclabel', 'entlabel', 'flaglabel', 'scanabove', 'scanbelow', 'scanctr', 'screennote']);
function makeEnv(reduced) {
  let cache = {}, qcache = {}, queue = [], app;
  const mkPseudo = (attrs) => {
    let click = null;
    return {
      addEventListener(t, f) { if (t === 'click') click = f; }, _click() { if (click) click({ preventDefault() {} }); },
      getAttribute(n) { const m = new RegExp(n.replace(/-/g, '\\-') + '="([^"]*)"').exec(attrs); return m ? m[1] : null; },
      setAttribute() {}, textContent: '',
    };
  };
  const enriched = () => { const cl = new Set(); return {
    _html: '', textContent: '',
    get innerHTML() { return this._html; }, set innerHTML(v) { this._html = String(v); },
    insertAdjacentHTML(_pos, h) { this._html += String(h); },
    classList: { add: c => cl.add(c), remove: c => cl.delete(c), contains: c => cl.has(c) }, _cl: cl,
    get scrollHeight() { return 1; }, set scrollTop(_v) {}, get scrollTop() { return 0; },
    addEventListener() {}, setAttribute() {}, getAttribute() { return null; },
  }; };
  const qsa = (sel) => {
    if (qcache[sel]) return qcache[sel];
    const cls = sel.replace(/^\./, ''); const out = []; const h = app._html;
    const tagRe = /<([a-z]+)([^>]*)>/gi; let m;
    while ((m = tagRe.exec(h))) { const c = /class="([^"]*)"/.exec(m[2]); if (c && c[1].split(/\s+/).includes(cls)) out.push(mkPseudo(m[2])); }
    return (qcache[sel] = out);
  };
  const mkChrome = (id) => ({
    id, _html: '', textContent: '',
    get innerHTML() { return this._html; }, set innerHTML(v) { this._html = String(v); cache = {}; qcache = {}; },
    querySelectorAll: qsa, addEventListener() {}, setAttribute() {}, getAttribute() { return null; },
  });
  const persistent = {}; for (const id of ['app', 'badge', 'brand', 'brandsub', 'foot']) persistent[id] = mkChrome(id);
  app = persistent.app;
  const gid = (id) => {
    if (persistent[id]) return persistent[id];
    if (!(id in cache)) { const re = new RegExp('<([a-z]+)([^>]*\\sid="' + id + '"[^>]*)>', 'i'); const m = re.exec(app._html); cache[id] = m ? (DYN.has(id) ? enriched() : mkPseudo(m[2])) : null; }
    return cache[id];
  };
  const document = { getElementById: gid, querySelectorAll: qsa, addEventListener() {} };
  const window = { matchMedia: () => ({ matches: reduced }), scrollTo() {} };
  const setTimeout = (fn) => { queue.push(fn); return queue.length; };
  const clearTimeout = () => {};
  const drain = () => { let n = 0; while (queue.length && n < 200000) { (queue.shift())(); n++; } };
  return { document, window, app, setTimeout, clearTimeout, drain };
}
function boot(reduced) {
  const env = makeEnv(reduced);
  const ctx = vm.createContext({ window: env.window, document: env.document, console, setTimeout: env.setTimeout, clearTimeout: env.clearTimeout });
  let threw = null;
  try {
    vm.runInContext(SCRIPT + '\n;globalThis.__t={go,state,matchEntities,articleById,threshold};', ctx);
  } catch (e) { threw = e; }
  return { env, ctx, threw };
}

/* ===================== reduced-motion mode (final-state drive) ===================== */
console.log('\n[reduced-motion] boot + drive the arc (template = final resting state)');
{
  const { env, ctx, threw } = boot(true);
  ok(!threw, 'engine evaluates without throwing' + (threw ? ` (${threw})` : ''));
  const A = env.app;
  ok(/What aren’t we watching/.test(A._html), 'boot → Select hero renders');
  ok(env.document.querySelectorAll('.card').length === 4, 'Select shows 4 article cards');
  ok(/Baltimore Defense Attorney/.test(A._html), 'Select lists the Ravenell (professional-ML) article');
  ok(/Canadian National Sentenced/.test(A._html), 'Select lists the Goltsev (export-control) article');
  ok(/Treasury Targets Russian Illicit Finance/.test(A._html), 'Select lists the OFAC TGR (sanctions-evasion) article');
  ok(/class="chip sig">DOJ/.test(A._html) && /class="chip sig">OFAC/.test(A._html), 'Select shows honest source chips (DOJ / OFAC)');

  // ---- matcher correctness (the new muscle), on the OFAC TGR article ----
  const tgr = ctx.__t.articleById('ofac-tgr-group');
  const m = ctx.__t.matchEntities(tgr);
  const by = Object.fromEntries(m.map(x => [x.entity.name, x]));
  ok(by['Siam Expert Trading Company Limited'].exact && by['Siam Expert Trading Company Limited'].score === 1, 'Siam Expert = EXACT 1.000 (counterparty IS a designated entity)');
  approx(by['Pullman Global Solutions LLC'].score, 1.0, 0.001, 'Pullman near-match (suffix-drop) score');
  ok(by['Pullman Global Solutions LLC'].kind === 'near' && by['Pullman Global Solutions LLC'].hit, 'Pullman classified NEAR (exact-name screen would miss the dropped "LLC")');
  approx(by['Ekaterina Zhdanova'].score, 0.989, 0.01, 'Zhdanova near-match (suffix) score');
  ok(by['Ekaterina Zhdanova'].kind === 'near', 'Zhdanova classified near');
  ok(by['George Rossi'].score === 1 && by['George Rossi'].hit && by['George Rossi'].exact, 'George Rossi common-name TRAP surfaces at 1.000 (exact score)');
  ok(by['Elena Chirkinyan'].hit === false, 'Chirkinyan (no near book row) does NOT surface — the matcher discriminates');
  ok(m.filter(x => x.hit).length === 4, 'TGR yields 4 surfaced hits (Siam exact + Pullman/Zhdanova near + Rossi trap)');
  ok(m.some(x => x.hit && !x.exact), 'at least one surfaced hit is a NEAR-match an exact-name screen would miss');

  // transliteration + word-order in the Goltsev article; typo in Mullings; middle-name in Ravenell
  const gm = Object.fromEntries(ctx.__t.matchEntities(ctx.__t.articleById('doj-goltsev-export-control')).map(x => [x.entity.name, x]));
  approx(gm['Nikolay Goltsev'].score, 0.973, 0.02, 'Nikolay→Nikolai transliteration near-match');
  ok(gm['Kristina Puzyreva'].score === 1 && gm['Kristina Puzyreva'].kind === 'near', 'word-order near-match (Kristina Puzyreva ↔ Puzyreva Kristina) = 1.000 via token-sort, classified near');
  const mu = Object.fromEntries(ctx.__t.matchEntities(ctx.__t.articleById('doj-mullings-romance-mule')).map(x => [x.entity.name, x]));
  approx(mu['Malachi Mullings'].score, 0.962, 0.02, 'Malachi→Malaki typo near-match');
  const rv = Object.fromEntries(ctx.__t.matchEntities(ctx.__t.articleById('doj-ravenell-attorney-ml')).map(x => [x.entity.name, x]));
  approx(rv['Kenneth Wendell Ravenell'].score, 0.950, 0.03, 'Ravenell middle-name near-match');

  // ---- Read screen ----
  ctx.__t.go('read', 'ofac-tgr-group');
  ok(/class="rail"/.test(A._html), 'Read shows the step rail (the arc is legible)');
  ok(/class="hl on"/.test(A._html), 'Read highlights grounded red-flag phrases');
  ok(/class="ent"/.test(A._html), 'Read tags named entities');
  ok(/class="ecard/.test(A._html), 'Read renders entity cards');
  ok(/Ukrainian national/.test(A._html), 'entity card shows the grounded location attribute');
  ok(/founder of TGR Partners/.test(A._html), 'entity card shows the grounded profession attribute');
  ok(/Launder client funds via stablecoins/.test(A._html), 'Read shows a red_flag translation beside the verbatim');
  ok(/Tether \(USDT\)/.test(A._html), 'Read renders the verbatim grounded flag');
  ok(/typology<\/span>/.test(A._html) && /sanctions-evasion/.test(A._html), 'Read shows the typology');
  ok(/Office of Foreign Assets Control/.test(A._html) && /17 U\.S\.C/.test(A._html), 'Read shows the real-source attribution (OFAC, public domain 17 U.S.C. §105)');

  ctx.__t.go('read', 'doj-goltsev-export-control');
  ok(/Montreal, Canada/.test(A._html), 'Goltsev entity card shows the grounded location (Montreal, Canada)');
  ok(/<b>Age<\/b>38/.test(A._html.replace(/\s+/g, '')), 'Goltsev entity card shows the grounded age (38)');

  // ---- Screen (scan) ----
  ctx.__t.go('screen', 'ofac-tgr-group');
  ok(/Screen against the book/.test(A._html), '→ Screen renders');
  ok(/1\.000/.test(A._html), 'Screen shows the real exact score (1.000)');
  ok(/0\.989/.test(A._html), 'Screen shows a real near-match score (0.989)');
  ok(/potential exposure/.test(A._html) && /no exposure/.test(A._html), 'Screen draws the threshold line (above / below)');
  ok(/near-match/.test(A._html), 'Screen notes a near-match an exact-name screen would miss');
  ok(!/\b\d{1,3}%/.test(A._html), 'Screen claims no fabricated precision/lift percentage');

  // ---- Disposition (human gate) ----
  ctx.__t.go('disposition', 'ofac-tgr-group');
  ok(/Disposition — the human gate/.test(A._html), '→ Disposition renders');
  let toggles = env.document.querySelectorAll('.hitbtn');
  ok(toggles.length === 4, 'Disposition shows one toggle per surfaced hit (4)');
  ok(/CONFIRMED/.test(A._html), 'hits default to CONFIRMED (agent proposes, human disposes)');
  ok(/no link to the sanctioned individual/.test(A._html), 'the common-name trap carries its dismiss note');
  const trapKey = 'ofac-tgr-group|' + by['George Rossi'].entity.id;
  const trap = toggles.find(t => t.getAttribute('data-k') === trapKey);
  ok(!!trap, 'the George Rossi trap toggle is present');
  trap._click();
  ok(/DISMISSED/.test(A._html), 'dismissing the trap flips it to DISMISSED');

  // ---- Close (exposure) ----
  ctx.__t.go('close', 'ofac-tgr-group');
  ok(/Exposure/.test(A._html), '→ Close renders');
  const flat = A._html.replace(/\s+/g, '');
  const conf = /(\d+)<\/div><divclass="l">confirmedexposures/.exec(flat);
  ok(conf && conf[1] === '3', 'confirmed exposures = 3 after dismissing the trap');
  const dism = /(\d+)<\/div><divclass="l">dismissed/.exec(flat);
  ok(dism && dism[1] === '1', 'dismissed (false positive) = 1');
  ok(/adverse-media <b>atom<\/b>/.test(A._html), 'Close names the atom / composition north star');
  ok(/Articles/.test(A._html), 'Close keeps the Articles return path');
}

/* ===================== full-motion mode (streaming + scan drive) ===================== */
console.log('\n[full-motion] enriched shim drives the streaming Read + scan PROCESS');
{
  const { env, ctx, threw } = boot(false);
  ok(!threw, 'engine evaluates without throwing (full-motion)' + (threw ? ` (${threw})` : ''));
  let threw2 = null;
  try { ctx.__t.go('read', 'ofac-tgr-group'); env.drain(); } catch (e) { threw2 = e; }
  ok(!threw2, 'full-motion streaming Read drives without error' + (threw2 ? ` (${threw2})` : ''));
  const doc = env.document.getElementById('doc'), ents = env.document.getElementById('entities'),
        rf = env.document.getElementById('redflags'), dl = env.document.getElementById('doclabel'),
        el = env.document.getElementById('entlabel'), fl = env.document.getElementById('flaglabel');
  ok((doc._html.match(/class="hl on"/g) || []).length === 8, 'streamed source reveals all 8 red-flag phrases');
  ok((doc._html.match(/class="ent"/g) || []).length >= 6, 'streamed source tags the entity occurrences');
  ok((ents._html.match(/class="ecard/g) || []).length === 6, 'all 6 entity cards streamed in');
  ok((rf._html.match(/class="xrow/g) || []).length === 8, 'all 8 red-flag translate rows streamed in');
  ok(!doc.classList.contains('reading'), 'the reading caret (.reading) is removed when the read completes');
  ok(/Named entities · 6/.test(el.textContent), 'the entities label counts up to 6');
  ok(/8/.test(fl.textContent), 'the red-flags label counts up to 8');
  ok(/6 entit/.test(dl.textContent), 'the doc label settles at the full entity count');

  let threw3 = null;
  try { ctx.__t.go('screen', 'ofac-tgr-group'); env.drain(); } catch (e) { threw3 = e; }
  ok(!threw3, 'full-motion scan PROCESS drives without error' + (threw3 ? ` (${threw3})` : ''));
  const above = env.document.getElementById('scanabove'), ctr = env.document.getElementById('scanctr');
  ok((above._html.match(/class="row hit/g) || []).length === 4, 'scan sweeps in all 4 surfaced hit rows');
  ok(/scanned/.test(ctr.textContent), 'the scan counter settles');

  // a clean drive of a different article through to Close throws nothing
  let threw4 = null;
  try {
    ctx.__t.go('read', 'doj-mullings-romance-mule'); env.drain();
    ctx.__t.go('screen', 'doj-mullings-romance-mule'); env.drain();
    ctx.__t.go('disposition', 'doj-mullings-romance-mule');
    ctx.__t.go('close', 'doj-mullings-romance-mule');
  } catch (e) { threw4 = e; }
  ok(!threw4, 'full-motion full arc on a second article throws no error' + (threw4 ? ` (${threw4})` : ''));
  ok(/Exposure/.test(env.app._html), 'full-motion reaches Close on the second article');
}

console.log(`\n${pass} passed, ${fails.length} failed`);
if (fails.length) { console.error('\nFAILURES:\n  - ' + fails.join('\n  - ')); process.exit(1); }
