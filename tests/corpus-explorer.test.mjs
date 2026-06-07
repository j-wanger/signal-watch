#!/usr/bin/env node
// Corpus-explorer arc regression harness — ZERO runtime deps (Node built-in `vm` + a hand-rolled
// DOM shim; no third-party DOM library, no npm install). Run: `node tests/corpus-explorer.test.mjs`.
//
// What it does: loads the COMMITTED dist/corpus/index.html (so it doubles as a build-output smoke
// test — `build.py --check all` already guarantees that file equals a fresh build of corpus.html),
// extracts the single inline <script>, evaluates it under the shim, then drives the 5-screen arc
// (Select → Coverage → Build recs/GATE → Signal → Close the loop) and asserts the Phase-18 invariants
// + the multi-source menu (Phase 20 FinCEN advisories + alerts, Phase 21 OFAC, Phase 22 FINTRAC — 4
// source types, honest doc_type chips; an alert, an OFAC advisory, AND a FINTRAC operational alert each
// walk the full arc; the FINTRAC source panel carries the Crown-copyright basis, not US public domain).
//
// Why a vm + shim instead of a third-party DOM library: the ship artifact is a single file:// offline
// HTML; the project's whole test idiom is dep-free (derive_signals.py --selftest, build.py --check).
// corpus.html's DOM
// surface is tiny (getElementById / querySelectorAll / matchMedia / requestAnimationFrame / setTimeout,
// innerHTML-driven, no layout reads), so a ~120-line shim covers it exactly. The script declares
// everything top-level, so an appended epilogue re-exports `selected`/`ADVISORIES`/the render fns —
// letting us drive the arc AND read/write the gate's real `selected` Set (REDUCED is read once at eval,
// so motion modes are tested in two fresh contexts).

import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';
import vm from 'node:vm';

const HERE = dirname(fileURLToPath(import.meta.url));
const DIST = resolve(HERE, '..', 'dist', 'corpus', 'index.html');

/* ---------- assertion tally ---------- */
let pass = 0;
const fails = [];
function ok(cond, msg) {
  if (cond) { pass++; console.log(`  ✓ ${msg}`); }
  else { fails.push(msg); console.log(`  ✗ ${msg}`); }
}
function eq(actual, expected, msg) {
  ok(actual === expected, `${msg} (expected ${JSON.stringify(expected)}, got ${JSON.stringify(actual)})`);
}

/* ---------- extract the inline script ---------- */
const html = readFileSync(DIST, 'utf8');
const open = html.indexOf('<script>');
const close = html.lastIndexOf('</script>');           // the only script is the last thing before </body>
if (open < 0 || close < 0) { console.error('FATAL: no <script> in', DIST); process.exit(2); }
const SCRIPT = html.slice(open + '<script>'.length, close);

/* ---------- a minimal DOM/window shim ---------- */
// queryAll: find opening tags whose class attr contains ALL the dotted classes in `sel`, returning
// pseudo-elements that carry data-* attributes + a writable onclick + classList/setAttribute/querySelector
// stubs — enough for corpus.html's real event wiring (advcard.live click → pick, brecrow.pickable click →
// toggle `selected`, step click → gotoScreen).
function queryAll(htmlStr, sel) {
  const needed = sel.split('.').filter(Boolean);
  const out = [];
  const tagRe = /<([a-z]+)([^>]*?)>/gi;
  let m;
  while ((m = tagRe.exec(htmlStr))) {
    const attrs = m[2];
    const clsM = /class="([^"]*)"/.exec(attrs);
    const classes = clsM ? clsM[1].split(/\s+/).filter(Boolean) : [];
    if (!needed.every(n => classes.includes(n))) continue;
    const dataset = {};
    let d; const dRe = /data-([a-z0-9-]+)="([^"]*)"/gi;
    while ((d = dRe.exec(attrs))) dataset[d[1].replace(/-([a-z])/g, (_, c) => c.toUpperCase())] = d[2];
    out.push(makePseudo(classes, dataset));
  }
  return out;
}
function makePseudo(classes, dataset) {
  const set = new Set(classes);
  const el = {
    dataset,
    textContent: '',
    onclick: null,
    classList: {
      add: c => set.add(c), remove: c => set.delete(c), contains: c => set.has(c),
      toggle: (c, f) => { const on = f === undefined ? !set.has(c) : f; on ? set.add(c) : set.delete(c); return on; },
    },
    setAttribute() {}, getAttribute() { return null; },
    querySelector() { return { textContent: '' }; },          // e.g. el.querySelector('.cbox')
  };
  return el;
}

function makeEnv(reduced) {
  let now = 0;
  const timers = [];
  const errors = [];
  let dynCache = {};                                          // dynamic getElementById results, reset on stage repaint

  function dynEl() {
    return { _html: '', style: {}, textContent: '',
      get innerHTML() { return this._html; }, set innerHTML(v) { this._html = String(v); } };
  }
  function chromeEl(id) {
    const lastQS = {};
    const e = {
      id, _html: '', style: {}, textContent: '', onclick: null,
      get innerHTML() { return this._html; },
      set innerHTML(v) { this._html = String(v); if (id === 'stage') dynCache = {}; },   // repaint clears dyn lookups
      querySelectorAll(sel) { const r = queryAll(this._html, sel); lastQS[sel] = r; return r; },
      querySelector(sel) { return queryAll(this._html, sel)[0] || null; },
      _qs(sel) { return lastQS[sel] || []; },                  // harness peeks the wired elements the script got
    };
    return e;
  }

  const stage = chromeEl('stage'), stepper = chromeEl('stepper');
  const chrome = { stage, stepper, next: chromeEl('next'), back: chromeEl('back'),
    reset: chromeEl('reset'), hint: chromeEl('hint') };

  const document = {
    getElementById(id) {
      if (chrome[id]) return chrome[id];
      if (dynCache[id]) return dynCache[id];
      if (new RegExp(`id="${id}"`).test(stage._html)) { return (dynCache[id] = dynEl()); }
      return dynEl();                                          // badge/brandTitle/brandSub etc. — never NPE
    },
    addEventListener() {},
    querySelectorAll(sel) { return queryAll(stage._html, sel); },
  };
  const window = {
    matchMedia: q => ({ matches: reduced, media: q, addListener() {}, removeListener() {}, addEventListener() {}, removeEventListener() {} }),
    scrollTo() {},
  };
  const env = {
    document, window,
    console: { error: (...a) => errors.push(a.join(' ')), log() {}, warn() {} },
    performance: { now: () => now },
    requestAnimationFrame: cb => { now += 1e6; cb(now); return 0; },   // advance past any duration → lands final in one call
    cancelAnimationFrame() {},
    setTimeout: (fn) => { timers.push(fn); return timers.length; },
    clearTimeout() {},
    __capture: api => { env.__api = api; },
    __errors: errors,
    __stage: stage,
    __flush: () => { const q = timers.splice(0); q.forEach(fn => fn()); },
  };
  return env;
}

// Run the script in a fresh vm context; the epilogue hands the internals back via __capture.
const EPILOGUE = `;__capture({coverageIndex,buildNows,isLive,curAdv,pick,gotoScreen,toSelect,render,renderClose,renderSignal,ADVISORIES,
  get selected(){return selected}, set selected(v){selected=v},
  get view(){return view}, get screen(){return screen}});`;
function boot(reduced) {
  const env = makeEnv(reduced);
  vm.createContext(env);
  vm.runInContext(SCRIPT + EPILOGUE, env, { filename: 'corpus-explorer-inline.js' });
  return env;
}

function numText(env, id) { return parseInt(String(env.document.getElementById(id).textContent).replace(/[^\d-]/g, ''), 10); }

/* ============================ drive the arc ============================ */
console.log('corpus-explorer arc harness  (source: dist/corpus/index.html)\n');

// ---- reduced-motion context: deterministic single-paint ----
const env = boot(true);
const api = env.__api;
ok(api && typeof api.pick === 'function', 'script booted; internals re-exported');

// (1) Boot lands on Select and lists every document
eq(api.view, 'select', 'boot view = select');
ok(/Pick a document/.test(env.__stage._html), 'Select screen renders ("Pick a document")');
const advCards = (env.__stage._html.match(/class="advcard /g) || []).length;
eq(advCards, api.ADVISORIES.length, 'Select lists every document as a card');
const liveCount = api.ADVISORIES.filter(api.isLive).length;
const liveCards = (env.__stage._html.match(/class="advcard live"/g) || []).length;
eq(liveCards, liveCount, 'only live (derived) documents are clickable cards');
ok(env.__errors.length === 0, 'Select rendered with no console errors');

// (1b) MULTI-SOURCE menu (Phase 20): both FinCEN publication types present, each card honestly typed
const advisoryChips = (env.__stage._html.match(/<span class="chip doc">Advisory<\/span>/g) || []).length;
const alertChips = (env.__stage._html.match(/<span class="chip doc">Alert<\/span>/g) || []).length;
const ofacChips = (env.__stage._html.match(/<span class="chip doc">OFAC<\/span>/g) || []).length;
const fintracChips = (env.__stage._html.match(/<span class="chip doc">FINTRAC<\/span>/g) || []).length;
ok(advisoryChips > 0 && alertChips > 0 && ofacChips > 0 && fintracChips > 0,
  `unified menu lists all 4 source types (${advisoryChips} advisories + ${alertChips} alerts + ${ofacChips} OFAC + ${fintracChips} FINTRAC)`);
eq(advisoryChips + alertChips + ofacChips + fintracChips, api.ADVISORIES.length,
  'every card carries an honest doc_type chip (Advisory/Alert/OFAC/FINTRAC)');
const liveAlerts = api.ADVISORIES.filter(a => a.doc_type === 'Alert' && api.isLive(a));
ok(liveAlerts.length > 0, `at least one FinCEN Alert is derived/live (${liveAlerts.length})`);
const liveOfac = api.ADVISORIES.filter(a => a.doc_type === 'OFAC' && api.isLive(a));
ok(liveOfac.length > 0, `at least one OFAC advisory is derived/live (${liveOfac.length})`);
const liveFintrac = api.ADVISORIES.filter(a => a.doc_type === 'FINTRAC' && api.isLive(a));
ok(liveFintrac.length > 0, `at least one FINTRAC operational alert is derived/live (${liveFintrac.length})`);

// choose a live advisory that has at least one buildable (BUILD_NOW + build_logic) gap
const adv = api.ADVISORIES.filter(api.isLive)
  .find(a => api.buildNows(a).some(i => i.build_logic && typeof i.build_logic === 'object'));
ok(adv, `found a live advisory with a buildable BUILD_NOW gap (${adv && adv.id})`);
const buildNowIds = api.buildNows(adv).map(i => i.id);
const buildableIds = api.buildNows(adv).filter(i => i.build_logic && typeof i.build_logic === 'object').map(i => i.id);

// (2) Coverage screen
api.pick(adv.id);
eq(api.view, 'detail', 'pick() enters detail view');
eq(api.screen, 0, 'pick() starts on Coverage (screen 0)');
ok(/· Coverage/.test(env.__stage._html) && /Coverage index/.test(env.__stage._html), 'Coverage screen renders');
const cov = api.coverageIndex(adv.indicators);
eq(numText(env, 'gnum'), cov, 'Coverage gauge lands on coverageIndex(indicators) under reduced motion');

// (3) Build recs = the GATE
api.gotoScreen(1);
ok(/Build recommendations · gate/.test(env.__stage._html), 'Build-recs/GATE screen renders');
eq([...api.selected].sort().join(','), [...buildNowIds].sort().join(','), 'gate defaults to ALL BUILD_NOW selected');
const pickable = env.__stage._qs('.brecrow.pickable');
eq(pickable.length, buildNowIds.length, 'exactly the BUILD_NOW rows are pickable (non-BUILD_NOW read-only)');

// (3b) the div-toggle gate really flips `selected` via the wired onclick (keyboard-safe, no <input>)
const before = api.selected.size;
const togId = pickable[0].dataset.id;
pickable[0].onclick();
ok(!api.selected.has(togId) && api.selected.size === before - 1, 'div-toggle onclick DESELECTS a BUILD_NOW row');
pickable[0].onclick();
ok(api.selected.has(togId) && api.selected.size === before, 'div-toggle onclick RE-SELECTS it');

// (4) Signal reflects the gate
api.gotoScreen(2);
const specCards = (env.__stage._html.match(/PROPOSED ·/g) || []).length;
eq(specCards, buildableIds.length, 'Signal drafts one spec card per selected ∩ buildable BUILD_NOW');
// honest empty state #1 — everything deselected (a choice)
api.selected = new Set();
api.gotoScreen(2);
ok(/No build-now gaps selected/.test(env.__stage._html), 'Signal honest empty state: deselected-all');

// (5) Close the loop — 0-picked flat-hold (no fake rise)
api.gotoScreen(3);
ok(/· Close the loop/.test(env.__stage._html), 'Close-the-loop screen renders');
ok(/coverage holds/.test(env.__stage._html), '0-picked close: honest flat-hold note (no fake rise)');
eq(numText(env, 'gnum'), cov, '0-picked close: gauge holds at the before value');

// (5b) Close the loop — commit all BUILD_NOW, coverage rises by the real recompute, indicators not mutated
api.selected = new Set(buildNowIds);
const pickedSet = new Set(buildNowIds);
const afterInds = adv.indicators.map(i => pickedSet.has(i.id) ? Object.assign({}, i, { status: 'covered' }) : i);
const after = api.coverageIndex(afterInds);
api.gotoScreen(3);
ok(after > cov, `committing the gaps raises coverage (${cov}% → ${after}%)`);
eq(numText(env, 'gnum'), after, 'close gauge lands on the recomputed after-coverage (reduced motion)');
ok(new RegExp(`\\+${after - cov} pts`).test(env.__stage._html), 'close shows the +Δpts chip from the picks');
eq(api.coverageIndex(adv.indicators), cov, 'a.indicators is NOT mutated by the close screen (Object.assign copy)');

// ---- animated (non-reduced) context: the close path lands final after a flush (closes a Ph18 soft-obs) ----
const env2 = boot(false);
const api2 = env2.__api;
const adv2 = api2.ADVISORIES.find(a => a.id === adv.id);
api2.pick(adv2.id);
api2.selected = new Set(api2.buildNows(adv2).map(i => i.id));
const after2 = api2.coverageIndex(adv2.indicators.map(i =>
  api2.selected.has(i.id) ? Object.assign({}, i, { status: 'covered' }) : i));
api2.gotoScreen(3);
ok(numText(env2, 'gnum') !== after2 || after2 === api2.coverageIndex(adv2.indicators),
  'animated close: gauge starts at the before value (not yet animated)');
env2.__flush();                                              // run the deferred T() → animVal → rAF chain
eq(numText(env2, 'gnum'), after2, 'animated close: gauge reaches the after value after the rAF/timer flush');
ok(env2.__errors.length === 0, 'animated run produced no console errors');

// ---- a FinCEN ALERT walks the full 5-screen arc (Phase 20 multi-source proof) ----
const envA = boot(true);
const apiA = envA.__api;
const alert = apiA.ADVISORIES.filter(a => a.doc_type === 'Alert' && apiA.isLive(a))
  .find(a => apiA.buildNows(a).some(i => i.build_logic && typeof i.build_logic === 'object'));
ok(alert, `found a live FinCEN Alert with a buildable BUILD_NOW gap (${alert && alert.id})`);
apiA.pick(alert.id);
eq(apiA.view, 'detail', 'alert: pick() enters detail view');
const covA = apiA.coverageIndex(alert.indicators);
eq(numText(envA, 'gnum'), covA, 'alert: Coverage gauge lands on coverageIndex(indicators)');
apiA.gotoScreen(1);
ok(/Build recommendations · gate/.test(envA.__stage._html), 'alert: Build-recs/GATE screen renders');
eq([...apiA.selected].sort().join(','), apiA.buildNows(alert).map(i => i.id).sort().join(','),
  'alert: gate defaults to ALL BUILD_NOW selected');
apiA.gotoScreen(2);
ok(/PROPOSED ·/.test(envA.__stage._html), 'alert: Signal drafts ≥1 spec card for the picks');
apiA.selected = new Set(apiA.buildNows(alert).map(i => i.id));
const afterA = apiA.coverageIndex(alert.indicators.map(i =>
  apiA.selected.has(i.id) ? Object.assign({}, i, { status: 'covered' }) : i));
apiA.gotoScreen(3);
ok(/· Close the loop/.test(envA.__stage._html), 'alert: Close-the-loop screen renders');
eq(numText(envA, 'gnum'), afterA, 'alert: close gauge lands on the recomputed after-coverage');
ok(envA.__errors.length === 0, 'alert: full 5-screen arc walked with no console errors');

// ---- an OFAC advisory walks the full 5-screen arc (Phase 21 — 3rd source / cross-agency proof) ----
const envO = boot(true);
const apiO = envO.__api;
const ofac = apiO.ADVISORIES.filter(a => a.doc_type === 'OFAC' && apiO.isLive(a))
  .find(a => apiO.buildNows(a).some(i => i.build_logic && typeof i.build_logic === 'object'));
ok(ofac, `found a live OFAC advisory with a buildable BUILD_NOW gap (${ofac && ofac.id})`);
apiO.pick(ofac.id);
eq(apiO.view, 'detail', 'ofac: pick() enters detail view');
const covO = apiO.coverageIndex(ofac.indicators);
eq(numText(envO, 'gnum'), covO, 'ofac: Coverage gauge lands on coverageIndex(indicators)');
apiO.gotoScreen(1);
ok(/Build recommendations · gate/.test(envO.__stage._html), 'ofac: Build-recs/GATE screen renders');
apiO.gotoScreen(2);
ok(/PROPOSED ·/.test(envO.__stage._html), 'ofac: Signal drafts ≥1 spec card for the picks');
apiO.selected = new Set(apiO.buildNows(ofac).map(i => i.id));
const afterO = apiO.coverageIndex(ofac.indicators.map(i =>
  apiO.selected.has(i.id) ? Object.assign({}, i, { status: 'covered' }) : i));
apiO.gotoScreen(3);
ok(/· Close the loop/.test(envO.__stage._html), 'ofac: Close-the-loop screen renders');
eq(numText(envO, 'gnum'), afterO, 'ofac: close gauge lands on the recomputed after-coverage');
ok(envO.__errors.length === 0, 'ofac: full 5-screen arc walked with no console errors');

// ---- a FINTRAC operational alert walks the full 5-screen arc (Phase 22 — 4th source / FIRST
//      cross-jurisdiction proof) + the source attribution is the FINTRAC Crown-copyright basis,
//      NOT the US "public domain" string (compliance: FINTRAC is reproduced under a non-commercial
//      licence, distinct from the US-federal 17 U.S.C. 105 sources). ----
const envF = boot(true);
const apiF = envF.__api;
const fintrac = apiF.ADVISORIES.filter(a => a.doc_type === 'FINTRAC' && apiF.isLive(a))
  .find(a => apiF.buildNows(a).some(i => i.build_logic && typeof i.build_logic === 'object'));
ok(fintrac, `found a live FINTRAC operational alert with a buildable BUILD_NOW gap (${fintrac && fintrac.id})`);
apiF.pick(fintrac.id);
eq(apiF.view, 'detail', 'fintrac: pick() enters detail view');
// the source panel (srcCap) on the Coverage screen carries the FINTRAC Crown-copyright attribution,
// and NEVER the US public-domain line (the footer's mixed-basis note is outside #stage).
ok(/His Majesty the King in Right of Canada/.test(envF.__stage._html),
  'fintrac: source panel renders the FINTRAC Crown-copyright attribution (© His Majesty…)');
ok(!/public domain/i.test(envF.__stage._html),
  'fintrac: the FINTRAC source panel does NOT claim US public domain');
const covF = apiF.coverageIndex(fintrac.indicators);
eq(numText(envF, 'gnum'), covF, 'fintrac: Coverage gauge lands on coverageIndex(indicators)');
apiF.gotoScreen(1);
ok(/Build recommendations · gate/.test(envF.__stage._html), 'fintrac: Build-recs/GATE screen renders');
eq([...apiF.selected].sort().join(','), apiF.buildNows(fintrac).map(i => i.id).sort().join(','),
  'fintrac: gate defaults to ALL BUILD_NOW selected');
apiF.gotoScreen(2);
ok(/PROPOSED ·/.test(envF.__stage._html), 'fintrac: Signal drafts ≥1 spec card for the picks');
apiF.selected = new Set(apiF.buildNows(fintrac).map(i => i.id));
const afterF = apiF.coverageIndex(fintrac.indicators.map(i =>
  apiF.selected.has(i.id) ? Object.assign({}, i, { status: 'covered' }) : i));
apiF.gotoScreen(3);
ok(/· Close the loop/.test(envF.__stage._html), 'fintrac: Close-the-loop screen renders');
eq(numText(envF, 'gnum'), afterF, 'fintrac: close gauge lands on the recomputed after-coverage');
ok(envF.__errors.length === 0, 'fintrac: full 5-screen arc walked with no console errors');

// ---- the FINTRAC real-estate OPERATIONAL BRIEF walks the full 5-screen arc (Phase 23 — FINTRAC
//      depth: the Brief is the doc that required the NEW inverted "Indicators of <X>" rf_region anchor,
//      and is a different FINTRAC product subtype (Operational Brief, FINTRAC-2016-OB001) than the OAs.
//      Snow-washing / real-estate ML is the marquee Canadian typology for the demo's audience. ----
const envB = boot(true);
const apiB = envB.__api;
const brief = apiB.ADVISORIES.find(a => a.id === 'fintrac-real-estate');
ok(brief && apiB.isLive(brief), 'fintrac-brief: the real-estate Operational Brief is derived/live');
ok(/Operational Brief/.test(brief.title || ''), 'fintrac-brief: doc is the FINTRAC Operational Brief subtype');
ok(apiB.buildNows(brief).some(i => i.build_logic && typeof i.build_logic === 'object'),
  'fintrac-brief: the Brief carries a buildable BUILD_NOW gap (inverted-anchor derivation produced real signals)');
apiB.pick(brief.id);
eq(apiB.view, 'detail', 'fintrac-brief: pick() enters detail view');
ok(/His Majesty the King in Right of Canada/.test(envB.__stage._html),
  'fintrac-brief: source panel renders the FINTRAC Crown-copyright attribution');
ok(!/public domain/i.test(envB.__stage._html), 'fintrac-brief: the source panel does NOT claim US public domain');
const covB = apiB.coverageIndex(brief.indicators);
eq(numText(envB, 'gnum'), covB, 'fintrac-brief: Coverage gauge lands on coverageIndex(indicators)');
apiB.gotoScreen(1);
ok(/Build recommendations · gate/.test(envB.__stage._html), 'fintrac-brief: Build-recs/GATE screen renders');
eq([...apiB.selected].sort().join(','), apiB.buildNows(brief).map(i => i.id).sort().join(','),
  'fintrac-brief: gate defaults to ALL BUILD_NOW selected');
apiB.gotoScreen(2);
ok(/PROPOSED ·/.test(envB.__stage._html), 'fintrac-brief: Signal drafts ≥1 spec card for the picks');
apiB.selected = new Set(apiB.buildNows(brief).map(i => i.id));
const afterB = apiB.coverageIndex(brief.indicators.map(i =>
  apiB.selected.has(i.id) ? Object.assign({}, i, { status: 'covered' }) : i));
apiB.gotoScreen(3);
ok(/· Close the loop/.test(envB.__stage._html), 'fintrac-brief: Close-the-loop screen renders');
eq(numText(envB, 'gnum'), afterB, 'fintrac-brief: close gauge lands on the recomputed after-coverage');
ok(envB.__errors.length === 0, 'fintrac-brief: full 5-screen arc walked with no console errors');

/* ============================ report ============================ */
console.log(`\n${pass} passed, ${fails.length} failed`);
if (fails.length) { console.log('FAILURES:\n  - ' + fails.join('\n  - ')); process.exit(1); }
console.log('OK — corpus-explorer arc invariants hold against the committed dist.');
