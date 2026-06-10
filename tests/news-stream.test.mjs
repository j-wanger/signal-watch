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
  // Phase 36: the watchlist/disposition (persistence feedback) code is companion-only — none survives the strip
  ok(!html.includes('NEWS._watch') && !html.includes('liveRenderDisposition')
     && !html.includes('/watchlist') && !html.includes('/disposition'),
     'offline dist/news carries NO Phase-36 watchlist/disposition code (screens the static book only)');
  // Phase 38: the watchlist-VIEW + prune is companion-only too — none survives the strip
  ok(!html.includes('watchpanel') && !html.includes('liveRenderWatchlistPanel')
     && !html.includes('livePrune') && !html.includes('/watchlist/prune'),
     'offline dist/news carries NO Phase-38 watchlist-view/prune code (stripped)');
  // …and the SOURCE template DOES carry the companion-only watchlist view + prune
  ok(src.includes('liveRenderWatchlistPanel') && src.includes('livePrune') && src.includes('/watchlist/prune'),
     'news.html SOURCE carries the Phase-38 watchlist view + prune (companion-served)');
  // Phase 39: the extraction-progress stream reader is companion-only — none survives the strip
  ok(!html.includes('liveReadStream') && !html.includes('liveStageLabel') && !html.includes('getReader'),
     'offline dist/news carries NO Phase-39 progress-stream code (stripped)');
  ok(src.includes('liveReadStream') && src.includes('liveStageLabel') && src.includes('Verifying entity '),
     'news.html SOURCE carries the Phase-39 NDJSON progress reader + stage labels (companion-served)');
  // Phase 39: the one-shot URL input is companion-only — none survives the strip
  ok(!html.includes('live-url') && !html.includes('liveApplyConverted'),
     'offline dist/news carries NO Phase-39 URL-input code (stripped)');
  ok(src.includes('live-url') && src.includes('liveApplyConverted'),
     'news.html SOURCE carries the Phase-39 one-shot URL input (companion-served)');
  // Phase 41: the entity-resolution enrichment UI + alias-aware matcher are companion-only — none survives the strip
  ok(!html.includes('live-stype') && !html.includes('liveBestPair') && !html.includes('relpanel')
     && !html.includes('Subject map') && !html.includes('main_subjects'),
     'offline dist/news carries NO Phase-41 enrichment-UI/alias-matcher code (stripped)');
  ok(src.includes('live-stype') && src.includes('liveBestPair') && src.includes('Subject map')
     && src.includes('investigation-note'),
     'news.html SOURCE carries the Phase-41 source-type selector + subject map + alias matcher (companion-served)');
  // Phase 42: the SVG network visualizer + anchor dossier are companion-only — none survives the strip
  ok(!html.includes('liveGraphLayout') && !html.includes('netsvg') && !html.includes('gedge')
     && !html.includes('netpanel') && !html.includes('liveOpenDossier') && !html.includes('dosspanel')
     && !html.includes('/anchor'),
     'offline dist/news carries NO Phase-42 network-visualizer/dossier code (stripped)');
  ok(src.includes('liveGraphLayout') && src.includes('netsvg') && src.includes('gedge')
     && src.includes('liveOpenDossier') && src.includes('dosspanel'),
     'news.html SOURCE carries the Phase-42 SVG network visualizer + anchor dossier (companion-served)');
  // Phase 43: the stage-completion preview + token counter are companion-only — none survives the strip
  ok(!html.includes('livePreviewBody') && !html.includes('live-preview') && !html.includes('pvent')
     && !html.includes('tokens generated'),
     'offline dist/news carries NO Phase-43 progressive-preview/token-counter code (stripped)');
  ok(src.includes('livePreviewBody') && src.includes('live-preview') && src.includes('tokens generated')
     && src.includes("'grounded'") && src.includes("'verified'"),
     'news.html SOURCE carries the Phase-43 staged preview + grounded/verified wiring (companion-served)');
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
  const document = { getElementById: gid, querySelector: () => null, querySelectorAll: qsa,
                     createElement: () => ({ textContent: '', style: {}, appendChild() {}, setAttribute() {} }),
                     head: { appendChild() {} }, addEventListener() {} };
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
// Phase 36: boot the companion-SERVED script (live region present, NEWS.live set) with a fetch stub, to
// behaviorally exercise the client-side overrides that the stripped offline dist never carries.
function bootLive(scriptText, reduced) {
  const env = makeEnv(reduced);
  const fetchStub = () => Promise.resolve({ ok: true, json: () => Promise.resolve({ rows: [] }) });
  const ctx = vm.createContext({ window: env.window, document: env.document, console,
    fetch: fetchStub, setTimeout: env.setTimeout, clearTimeout: env.clearTimeout });
  let threw = null;
  try { vm.runInContext(scriptText + '\n;globalThis.__L={go,state,matchEntities,articleById,NEWS,RENDER,liveRenderWatchlistPanel,livePrune,liveReadStream,liveStageLabel,liveGraphLayout,liveOpenDossier,liveDossierBody,livePreviewBody};', ctx); }
  catch (e) { threw = e; }
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

/* ===================== live mode (companion-served page) — Phase 36 ===================== */
// The offline dist has the live region STRIPPED; here we eval the SERVED page (news.html with a minimal
// live NEWS substituted) under the same shim to behaviorally verify the CLIENT overrides the Python HTTP
// tests can't reach: the Screen step scores against book ∪ watchlist, and the Disposition gate renders
// per-entity escalate controls. (The fetch-driven escalate→persist→refetch loop is covered server-side in
// tests/news_live_test.py; here we set NEWS._watch directly to isolate the client screen/render logic.)
console.log('\n[live mode] companion-served client overrides (book ∪ watchlist screen + escalate gate)');
{
  const SRC = readFileSync(resolve(HERE, '..', 'news.html'), 'utf8');
  const liveNEWS = {
    brand: { title: 'Signal Watch', subtitle: 'Adverse-Media Stream' }, badge: 'Illustrative data & outputs',
    articles: [
      { id: 'live-a', scan_id: 'aaa', title: 'Article A', doc_type: 'News', typology: 'fraud', source_org: 'Live',
        article_text: 'Acme Holdings and Beta Corp moved funds offshore.',
        entities: [{ id: 'E1', name: 'Acme Holdings', type: 'org' }, { id: 'E2', name: 'Beta Corp', type: 'org' }], red_flags: [] },
      { id: 'live-b', scan_id: 'bbb', title: 'Article B', doc_type: 'News', typology: 'fraud', source_org: 'Live',
        article_text: 'Acme Holdings surfaced again in a later filing.',
        entities: [{ id: 'E1', name: 'Acme Holdings', type: 'org' }], red_flags: [] },
      { id: 'live-e', scan_id: 'eee', title: 'Article E', doc_type: 'News', typology: 'fraud', source_org: 'Live',
        article_text: 'Maria Lopez ran Lopez Imports LLC, which was a front for her.',
        entities: [
          { id: 'E1', name: 'Maria Lopez', type: 'person', aliases: ['M. Lopez'],
            properties: [{ kind: 'phone', value: '(212) 555-1234' }, { kind: 'client_number', value: 'C-77812' }] },
          { id: 'E2', name: 'Lopez Imports LLC', type: 'org' },
          // Phase 42 — a hostile store-derived name: the graph + cards must render it ESCAPED (stored-XSS guard)
          { id: 'E3', name: '<img src=x onerror=alert(1)>', type: 'org' }],
        red_flags: [],
        main_subjects: ['Maria Lopez'],
        relationships: [{ from: 'Lopez Imports LLC', to: 'Maria Lopez', label: 'front-for',
                          evidence: 'was a front for her' }] },
    ],
    book: { rows: [{ id: 'bk-1', name: 'Zzz Unrelated Bank', type: 'org', role: 'counterparty', country: 'US', segment: 'Trade' }] },
    match: { threshold: 0.85 },
    live: { extract: '/extract', watchlist: '/watchlist', disposition: '/disposition', prune: '/watchlist/prune', anchor: '/anchor', persist: true, model: 'm', llm_url: 'u' },
  };
  const liveScript = SRC.slice(SRC.indexOf('<script>') + '<script>'.length, SRC.lastIndexOf('</script>'))
    .replace('__NEWS__', JSON.stringify(liveNEWS));
  const { env, ctx, threw } = bootLive(liveScript, true);
  ok(!threw, 'companion-served live page evaluates without throwing' + (threw ? ` (${threw})` : ''));
  await new Promise(r => setImmediate(r));   // flush the init liveRefreshWatchlist() microtask (resolves to [])
  const L = ctx.__L;
  ok(L && L.RENDER && typeof L.RENDER.disposition === 'function', 'liveInit installed the live Disposition gate (RENDER.disposition overridden)');

  // 1) book ∪ watchlist screen — an EMPTY watchlist defers to book-only: Acme does NOT hit (book is unrelated)
  L.NEWS._watch = [];
  const aHit0 = L.matchEntities(L.articleById('live-a')).find(x => x.entity.name === 'Acme Holdings');
  ok(aHit0 && aHit0.hit === false, 'empty watchlist → the override is inert (book-only screen; Acme does not hit)');

  // 2) once escalation populates the watchlist, a LATER article re-mentioning the entity HITS against it
  L.NEWS._watch = [{ name: 'Acme Holdings', type: 'org', kind: 'scanned', role: 'watchlist', country: 'escalated from Article A' }];
  const bHit = L.matchEntities(L.articleById('live-b')).find(x => x.entity.name === 'Acme Holdings');
  ok(bHit && bHit.hit && bHit.row && bHit.row.kind === 'scanned', 'escalated entity on the watchlist → a re-mention HITS (the screen surface compounds)');
  ok(bHit && bHit.score === 1, 'the watchlist re-mention scores 1.000 (exact) against the escalated row');

  // 3) the Disposition gate renders per-entity escalate controls for a live-scanned article (scan_id present)
  L.go('disposition', 'live-b');
  const dh = env.app._html;
  ok(/Disposition — the human gate/.test(dh), 'live Disposition renders');
  ok(/data-e="E1"/.test(dh) && /(＋ WATCHLIST|ESCALATED)/.test(dh), 'Disposition shows a per-entity escalate control (data-e + watchlist label)');
  ok(/the screen surface compounds/.test(dh), 'Disposition explains the escalation → watchlist loop');

  // 4) Phase 38 — the watchlist VIEW renders the escalated surface (name + provenance + a Prune control)
  ok(typeof L.liveRenderWatchlistPanel === 'function' && typeof L.livePrune === 'function',
     'companion page wires the watchlist view (liveRenderWatchlistPanel) + prune (livePrune)');
  env.app._html = '<div id="watchpanel"></div>';
  L.NEWS._watch = [{ name: 'Acme Holdings', type: 'org', kind: 'scanned', role: 'watchlist', country: 'escalated from Article A' }];
  L.liveRenderWatchlistPanel();
  const wp = env.document.getElementById('watchpanel');
  ok(wp && /Acme Holdings/.test(wp.innerHTML) && /escalated from Article A/.test(wp.innerHTML) && /Prune/.test(wp.innerHTML),
     'watchlist view renders the escalated entity with provenance + a Prune control');
  // empty surface → an explicit empty state (not a blank panel)
  L.NEWS._watch = [];
  L.liveRenderWatchlistPanel();
  ok(/No escalated entities yet/.test(env.document.getElementById('watchpanel').innerHTML),
     'watchlist view shows an empty state when nothing is escalated');

  // 4c) Phase 41 — ALIAS-AWARE screening: name ∪ aliases, max pair score, CLASS-AWARE alias rules
  // (multi-token aliases fuzzy like names; single-token aliases + @-handles exact-normalized ONLY).
  L.NEWS._watch = [{ name: 'Zeta Container Line', type: 'org', kind: 'scanned', role: 'watchlist',
                     country: 'escalated from Article A · investigation-note',
                     aliases: ['Krasnov Trading House', 'Smith', '@zetaops'] }];
  const aliasArt = { id: 'live-c', scan_id: 'ccc', title: 'C', article_text: 'x', red_flags: [],
    entities: [
      { id: 'E1', name: 'Krasnov Trading House', type: 'org' },  // exact via a multi-token alias
      { id: 'E2', name: 'Krasnov Trading Huose', type: 'org' },  // near-misspelling, fuzzy via multi-token alias
      { id: 'E3', name: 'Smithe Logistics', type: 'org' },       // must NOT hit via the single-token alias
      { id: 'E4', name: 'Smith', type: 'person' },               // single-token alias DOES hit exact-normalized
      { id: 'E5', name: '@zetaops', type: 'org' },               // handle: exact-normalized only
    ] };
  const am = Object.fromEntries(L.matchEntities(aliasArt).map(x => [x.entity.name, x]));
  ok(am['Krasnov Trading House'].hit && am['Krasnov Trading House'].score === 1 && !!am['Krasnov Trading House'].via,
     'a multi-token watchlist alias matches exactly (via reported for the analyst)');
  ok(am['Krasnov Trading Huose'].hit && am['Krasnov Trading Huose'].kind === 'near',
     'a near-misspelling of a multi-token alias still hits (fuzzy allowed for the open class)');
  ok(!am['Smithe Logistics'].hit,
     'a single-token alias NEVER fuzzy-matches (exact-normalized only — guards the false-positive flood)');
  ok(am['Smith'].hit && am['Smith'].score === 1, 'a single-token alias still matches EXACT-normalized');
  ok(am['@zetaops'].hit && am['@zetaops'].score === 1, 'an @-handle alias matches exact-normalized only');
  L.NEWS._watch = [{ name: 'Acme Holdings', type: 'org', kind: 'scanned', role: 'watchlist',
                     country: 'escalated from Article A', aliases: [] }];
  const am2 = L.matchEntities({ id: 'live-d', red_flags: [], entities: [
    { id: 'E1', name: 'Fresh Shell LLC', type: 'org', aliases: ['Acme Holdings'] }] })[0];
  ok(am2.hit && am2.via && am2.via.entity === 'Acme Holdings',
     'an extracted entity ALIAS matches the watchlist name (the entity-resolution payoff)');

  // 4d) Phase 41/42 — the Disposition gate renders the SUBJECT MAP (now an SVG network) + identity cards
  L.NEWS._watch = [];
  L.go('disposition', 'live-e');
  const eh = env.app._html;
  ok(/Subject map/.test(eh) && /main subject: Maria Lopez/.test(eh),
     'Disposition shows the subject map with the main subject named');
  ok(/<svg[^>]*class="netsvg"/.test(eh) && /class="gnode gmain"/.test(eh) && /class="gedge"/.test(eh),
     'the subject map renders as an SVG network (nodes + edges, main subject highlighted)');
  ok(/front-for/.test(eh), 'a relationship edge renders its vocab label');
  ok(!/was a front for her/.test(eh),
     'the evidence quote is CLOSED until its edge is clicked (graph as navigation, evidence on demand)');
  ok(/a\.k\.a\. M\. Lopez/.test(eh), 'an entity card shows the kept aliases');
  ok(/client_number/.test(eh) && /C-77812/.test(eh) && /\(212\) 555-1234/.test(eh),
     'an entity card shows the grounded identifying properties (incl. client_number)');
  ok(/tag main/.test(eh), 'the main-subject entity card carries the main-subject tag');
  ok(!/<img src=x/.test(eh) && /&lt;img src=x/.test(eh),
     'a hostile store-derived entity name renders ESCAPED everywhere (graph label + card — stored-XSS guard)');
  // clicking the edge (svg or row) reveals the grounded evidence quote
  const edgeEls = env.document.querySelectorAll('.gedge');
  ok(edgeEls.length >= 1, 'the rendered network exposes a clickable edge');
  edgeEls[0]._click();
  ok(/was a front for her/.test(env.app._html),
     'clicking an edge reveals its verbatim grounded evidence quote');

  // 4e) Phase 42 — the layout is a PURE deterministic function (asserted directly, no DOM)
  ok(typeof L.liveGraphLayout === 'function', 'companion page exports liveGraphLayout (pure data→positions)');
  const ents42 = [{ name: 'A Corp' }, { name: 'B Person' }, { name: 'C LLC' }];
  const rels42 = [
    { from: 'B Person', to: 'A Corp', label: 'owner-or-controller-of', evidence: 'B controls A' },
    { from: 'GhostCo', to: 'A Corp', label: 'counterparty', evidence: 'paid GhostCo' },  // endpoint not extracted
    { from: 'A Corp', to: 'A Corp', label: 'counterparty', evidence: 'self' }];          // post-fold artifact
  const lay1 = L.liveGraphLayout(ents42, rels42, ['A Corp']);
  const lay2 = L.liveGraphLayout(ents42, rels42, ['A Corp']);
  ok(JSON.stringify(lay1) === JSON.stringify(lay2), 'layout is deterministic (same input → identical positions)');
  ok(lay1.nodes.length === 4 && lay1.nodes.some(n => n.name === 'GhostCo'),
     'an edge endpoint missing from the entity list is synthesized as a node (the edge is kept)');
  ok(lay1.edges.length === 2 && !lay1.edges.some(e => e.from === e.to), 'a from==to self-edge is skipped defensively');
  const c42 = { x: lay1.w / 2, y: lay1.h / 2 };
  const d42 = n => Math.hypot(n.x - c42.x, n.y - c42.y);
  const main42 = lay1.nodes.find(n => n.name === 'A Corp');
  ok(main42 && main42.main && lay1.nodes.filter(n => n.name !== 'A Corp').every(o => d42(main42) < d42(o)),
     'the main subject sits more central than every other node');
  ok(lay1.nodes.every(n => n.x >= 0 && n.x <= lay1.w && n.y >= 0 && n.y <= lay1.h),
     'every node lands inside the viewBox');
  const lay0 = L.liveGraphLayout([{ name: 'Solo Corp' }], [], []);
  ok(lay0.nodes.length === 1 && lay0.edges.length === 0,
     'a 0-relationship scan lays out as isolated nodes (no edges, no crash)');

  // 4f) Phase 42 — the ANCHOR DOSSIER: node/watchlist click → GET /anchor → the accumulated identity
  ok(typeof L.liveOpenDossier === 'function' && typeof L.liveDossierBody === 'function',
     'companion page wires the anchor dossier (liveOpenDossier + liveDossierBody)');
  const anchorPayload = {
    anchor_id: 'a1', name: 'Maria Lopez', type: 'person', first_source_type: 'gov-enforcement',
    first_ts: '2026-06-10T00:00:00Z',
    scans: [{ scan_id: 's1', title: 'Article E', ts: '2026-06-10T00:00:00Z', source_type: 'gov-enforcement' },
            { scan_id: 's2', title: 'Case note 7', ts: '2026-06-11T00:00:00Z', source_type: 'investigation-note' }],
    properties: [
      { kind: 'alias', value: 'M. Lopez', scan_id: 's1', provenance: { title: 'Article E', ts: '2026-06-10', source_type: 'gov-enforcement' } },
      { kind: 'alias', value: 'M. Lopez', scan_id: 's2', provenance: { title: 'Case note 7', ts: '2026-06-11', source_type: 'investigation-note' } },
      { kind: 'phone', value: '(212) 555-1234', scan_id: 's1', provenance: { title: 'Article E', ts: '2026-06-10', source_type: 'gov-enforcement' } },
      { kind: 'phone', value: '(305) 555-9876', scan_id: 's2', provenance: { title: 'Case note 7', ts: '2026-06-11', source_type: 'investigation-note' } }],
    relationships: [{ from: 'Lopez Imports LLC', to: 'Maria Lopez', label: 'front-for', evidence: 'was a front for her' }],
  };
  const db = L.liveDossierBody(anchorPayload);
  ok(/2 scans/.test(db) && /Article E/.test(db) && /Case note 7/.test(db),
     'dossier lists every scan that touched the anchor');
  ok(/conflicting values — both kept/.test(db) && /\(212\) 555-1234/.test(db) && /\(305\) 555-9876/.test(db),
     'same-kind different values BOTH render with the conflict flag (presentation-only, never resolved)');
  ok(/a\.k\.a\./.test(db) && /M\. Lopez/.test(db), 'accumulated aliases render');
  ok(/investigation-note/.test(db), 'per-row provenance carries the scan source type');
  ok(/front-for/.test(db) && /was a front for her/.test(db), 'the dossier lists relationship edges with evidence');
  const emptyDb = L.liveDossierBody({ anchor_id: 'a2', name: 'Solo', type: 'org', first_source_type: '', first_ts: '',
                                      scans: [{ scan_id: 's1', title: 'One', ts: '', source_type: '' }],
                                      properties: [], relationships: [] });
  ok(/only the name has been seen/.test(emptyDb), 'an anchor with nothing accumulated renders an honest empty state');
  // integration: a graph-node click fetches /anchor and renders the dossier into #dossier
  const fetched = [];
  ctx.fetch = async (url) => { fetched.push(String(url)); return { ok: true, status: 200, json: async () => anchorPayload }; };
  L.go('disposition', 'live-e');
  const nodes42 = env.document.querySelectorAll('.gnode');
  ok(nodes42.length >= 2, 'the rendered network exposes clickable nodes');
  const mlNode = nodes42.filter(n => n.getAttribute('data-n') === 'Maria Lopez')[0];
  ok(!!mlNode, 'the main-subject node is addressable by name');
  mlNode._click();
  await new Promise(r => setImmediate(r));
  ok(fetched.some(u => u.includes('/anchor?name=Maria%20Lopez')), 'a node click fetches GET /anchor?name=<url-encoded>');
  const dEl = env.document.getElementById('dossier');
  ok(dEl && /Anchor dossier — Maria Lopez/.test(dEl.innerHTML) && /conflicting values — both kept/.test(dEl.innerHTML),
     'the dossier panel renders the accumulated identity below the graph');
  // 404 → an honest no-anchor state (never a crash)
  ctx.fetch = async () => ({ ok: false, status: 404, json: async () => ({ error: 'no anchor' }) });
  await L.liveOpenDossier('Ghost Name');
  ok(/No anchor yet for Ghost Name/.test(env.document.getElementById('dossier').innerHTML),
     'an unknown anchor renders an honest 404 state');
  // watchlist rows carry the dossier affordance
  env.app._html = '<div id="watchpanel"></div><div id="dossier"></div>';
  L.NEWS._watch = [{ name: 'Acme Holdings', type: 'org', kind: 'scanned', role: 'watchlist', country: 'escalated from Article A' }];
  L.liveRenderWatchlistPanel();
  ok(/class="wname wdoss"/.test(env.document.getElementById('watchpanel').innerHTML),
     'watchlist rows expose the dossier affordance (name click opens the anchor dossier)');

  // 5) Phase 39 — the client side of the streamed /extract: NDJSON reader + stage labels
  ok(typeof L.liveReadStream === 'function' && typeof L.liveStageLabel === 'function',
     'companion page wires the Phase-39 progress reader + stage labels');
  ok(L.liveStageLabel({ stage: 'verifying', i: 2, n: 9, name: 'Acme' }) === 'Verifying entity 2 of 9 — Acme…',
     'stage label renders verify i/N with the entity name (the wall-time majority made visible)');
  ok(/Fetching \+ converting/.test(L.liveStageLabel({ stage: 'fetching' })),
     'stage label covers the one-shot URL fetching stage');
  const events = [];
  const okStream = { body: null, text: async () =>
    '{"stage":"extracting"}\n{"stage":"grounding"}\n{"done":{"record":{"id":"r"},"dropped":[],"scan_id":null}}\n' };
  const finalEv = await L.liveReadStream(okStream, ev => events.push(ev.stage));
  ok(events.join(',') === 'extracting,grounding' && finalEv.record && finalEv.record.id === 'r',
     'liveReadStream parses NDJSON stage events and returns the final done payload');
  const errEv = await L.liveReadStream(
    { body: null, text: async () => '{"stage":"fetching"}\n{"error":"walled — paste the article text instead"}\n' }, () => {});
  ok(!!errEv.error && /paste the article text/.test(errEv.error),
     'liveReadStream surfaces an in-stream error event (honest verifier/acquisition failure)');

  // 6) Phase 43 — stage-completion progressive rendering (A2': staged reveal, never a token stream)
  ok(typeof L.livePreviewBody === 'function', 'companion page exports livePreviewBody (pure record→HTML)');
  ok(L.liveStageLabel({ stage: 'extracting', tokens: 1280 }).includes('1280 tokens generated'),
     'extracting label carries the token counter when the transport reports progress');
  ok(L.liveStageLabel({ stage: 'grounded', record: { red_flags: [{}, {}], entities: [{}, {}, {}] } })
       === 'Grounded — 2 red flags final; verifying 3 entities…',
     'grounded label names the staged counts (flags FINAL, entities pending verify)');
  ok(L.liveStageLabel({ stage: 'verified', name: 'X', kept: true }) === '',
     'verified events refine chips only — the i/N label keeps the cadence (no 0-of-0 style noise)');
  // sane rendering at n=0 / n=1 / n=large (the spec's three counts) + honest staging labels + XSS escape
  const pv0 = L.livePreviewBody({ red_flags: [], entities: [] });
  ok(pv0.includes('grounded (0)') && (pv0.match(/none grounded/g) || []).length === 2 && !pv0.includes('undefined'),
     'preview at n=0 renders honest empty states (no phantom counts, no 0-of-0)');
  const pv1 = L.livePreviewBody({ red_flags: [{ red_flag: 'Structuring below threshold', category: 'Cash' }],
                                  entities: [{ name: 'Acme Holdings' }] });
  ok(pv1.includes('grounded (1)') && pv1.includes('Structuring below threshold')
     && pv1.includes('final') && pv1.includes('provisional — verifying')
     && pv1.includes('data-pvent="Acme Holdings"'),
     'preview at n=1 renders the grounded flag as FINAL and the entity as PROVISIONAL');
  const many = Array.from({ length: 35 }, (_, i) => ({ name: 'Ent ' + i }));
  const pvN = L.livePreviewBody({ red_flags: [], entities: many });
  ok(pvN.includes('Entities (35)') && (pvN.match(/class="pvent"/g) || []).length === 35,
     'preview at n=35 renders every provisional entity chip (the verify-scale case)');
  const pvX = L.livePreviewBody({ red_flags: [{ red_flag: '<script>x</script>', category: '<b>c</b>' }],
                                  entities: [{ name: '<img onerror=1>' }] });
  ok(!pvX.includes('<script>') && !pvX.includes('<img') && !pvX.includes('<b>c</b>'),
     'preview escapes model-derived text everywhere (esc() is the sole escaper)');
}

console.log(`\n${pass} passed, ${fails.length} failed`);
if (fails.length) { console.error('\nFAILURES:\n  - ' + fails.join('\n  - ')); process.exit(1); }
