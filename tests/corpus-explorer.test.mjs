#!/usr/bin/env node
// Corpus-explorer arc regression harness — ZERO runtime deps (Node built-in `vm` + a hand-rolled
// DOM shim; no third-party DOM library, no npm install). Run: `node tests/corpus-explorer.test.mjs`.
//
// What it does: loads the COMMITTED dist/corpus/index.html (so it doubles as a build-output smoke
// test — `build.py --check all` already guarantees that file equals a fresh build of corpus.html),
// extracts the single inline <script>, evaluates it under the shim, then drives the story landing +
// the 6-screen per-doc arc (Select → Read advisory → Coverage → Build recs/GATE → Signal → Combination
// lift → Close) and asserts the Phase-18 invariants + the Phase-25 article-processing screen (the full
// source document with each verbatim red-flag phrase highlighted, then a natural AML red_flag translation
// beside it)
// + the multi-source menu (Phase 20 FinCEN advisories + alerts, Phase 21 OFAC, Phase 22 FINTRAC — 4
// source types, honest doc_type chips; an alert, an OFAC advisory, AND a FINTRAC operational alert each
// walk the full arc; Phase 28 — the FINTRAC source panel no longer renders the Crown-copyright clause
// (the user's compliance call); it never claims US public domain either)
// + the cross-corpus SYNTHESIS view (Phase 24: group by typology, combined coverage across a
// cross-jurisdiction cluster as honest union arithmetic — no similarity/overlap/lift — with drill-through)
// + the Phase-26 register beats: the story LANDING (entry before Select), Select grouped by source /
// newest-first, red-flag section sub-grouping on Coverage, the Act-4 build-log (real build_logic) + the
// Act-5 combination-lift (a GENERIC illustrative template, loudly badged "pending calibration" — never
// per-doc fabricated). Boot auto-enters Select (the landing is the new entry); raw=true stays on the cover.
// + the Phase-28 FULL-MOTION streaming read: the source STREAMS in (caret + scroll-follow), each red-flag
// phrase highlights only as the read reaches it, every translation extracts, then settles (caret removed).
//
// Why a vm + shim instead of a third-party DOM library: the ship artifact is a single file:// offline
// HTML; the project's whole test idiom is dep-free (derive_signals.py --selftest, build.py --check).
// corpus.html's DOM
// surface is tiny (getElementById / querySelectorAll / matchMedia / requestAnimationFrame / setTimeout,
// innerHTML-driven, no layout reads), so a ~120-line shim covers it exactly. The script declares
// everything top-level, so an appended epilogue re-exports `selected`/`ADVISORIES`/the render fns —
// letting us drive the arc AND read/write the gate's real `selected` Set (REDUCED is read once at eval,
// so motion modes are tested in two fresh contexts).

import { readFileSync, readdirSync } from 'node:fs';
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
// mirror corpus.html's esc() so we can assert escaped red_flag text appears in the rendered stage
function escH(s){return String(s==null?'':s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;').replace(/'/g,'&#39;');}

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
    const set = new Set();
    // Phase 28: #doc/#xlate need append + classList + scroll props so the FULL-MOTION streaming read
    // (renderArticle) can run under the shim (the reduced-motion path never touches these). scrollHeight=0
    // keeps the `if(scrollHeight)` scroll-follow a no-op (no layout in the shim).
    return { _html: '', style: {}, textContent: '', scrollTop: 0, scrollHeight: 0,
      get innerHTML() { return this._html; }, set innerHTML(v) { this._html = String(v); },
      insertAdjacentHTML(_pos, h) { this._html += String(h); },
      classList: { add: (...c) => c.forEach(x => set.add(x)), remove: (...c) => c.forEach(x => set.delete(x)), contains: c => set.has(c) } };
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
    reset: chromeEl('reset'), hint: chromeEl('hint'), attribution: chromeEl('attribution') };

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
    __drain: (max = 20000) => { let i = 0; while (timers.length && i++ < max) { const q = timers.splice(0); q.forEach(fn => fn()); } },
  };
  return env;
}

// Run the script in a fresh vm context; the epilogue hands the internals back via __capture.
const EPILOGUE = `;__capture({coverageIndex,buildNows,isLive,curAdv,pick,gotoScreen,toSelect,back,render,renderClose,renderSignal,ADVISORIES,
  clusters,clusterFor,indsForTypology,enterSynthesis,renderSelect,
  capAgg,enterCapability,renderCapability,indsForCap,CAPS,CAP_BY,DS_BY,
  dsAgg,enterDataSource,renderDataSource,indsForDS,DSRC,
  get selected(){return selected}, set selected(v){selected=v},
  get view(){return view}, get screen(){return screen},
  get currentTypology(){return currentTypology}, get fromTypology(){return fromTypology},
  get currentCapability(){return currentCapability}, get fromCapability(){return fromCapability},
  get currentDataSource(){return currentDataSource}, get fromDataSource(){return fromDataSource},
  get selMode(){return selMode}, set selMode(v){selMode=v}});`;
function boot(reduced, raw) {
  const env = makeEnv(reduced);
  vm.createContext(env);
  vm.runInContext(SCRIPT + EPILOGUE, env, { filename: 'corpus-explorer-inline.js' });
  // Phase 26: the story landing is now the ENTRY view. The existing arc/Select assertions expect to begin
  // on Select, so auto-enter the demo unless a test explicitly wants the raw landing (raw=true).
  if (!raw && env.__api && typeof env.__api.toSelect === 'function') env.__api.toSelect();
  return env;
}

function numText(env, id) { return parseInt(String(env.document.getElementById(id).textContent).replace(/[^\d-]/g, ''), 10); }

/* ============================ drive the arc ============================ */
console.log('corpus-explorer arc harness  (source: dist/corpus/index.html)\n');

// ---- (0) the story-driven LANDING is the entry (Phase 26) ----
const envL = boot(true, true);                                // raw — do NOT auto-enter; stay on the cover
const apiL = envL.__api;
eq(apiL.view, 'landing', 'boots into the story landing (the entry before Select)');
ok(/class="scene landing"/.test(envL.__stage._html) && /lhero/.test(envL.__stage._html),
  'landing renders the story hero');
const ltotal = apiL.ADVISORIES.length, lderived = apiL.ADVISORIES.filter(apiL.isLive).length;
ok(envL.__stage._html.includes(`>${ltotal}<`) && envL.__stage._html.includes(`>${lderived}<`),
  `landing stat tiles show HONEST data-derived counts (${ltotal} docs, ${lderived} derived)`);
ok(/id="enter"/.test(envL.__stage._html) && /Enter the corpus/.test(envL.__stage._html), 'landing carries the Enter CTA');
ok(envL.__errors.length === 0, 'landing rendered with no console errors');
apiL.toSelect();                                              // Enter →
ok(apiL.view === 'select' && /class="srcgroup"/.test(envL.__stage._html), 'Enter → the (source-grouped) Select grid');
apiL.back();
eq(apiL.view, 'landing', 'Back from Select returns to the landing cover (re-reachable)');

// ---- reduced-motion context: deterministic single-paint (boot auto-enters Select, Phase 26) ----
const env = boot(true);
const api = env.__api;
ok(api && typeof api.pick === 'function', 'script booted; internals re-exported');

// (1) After entering (boot auto-enters), Select lists every document
eq(api.view, 'select', 'boot auto-enters Select (the story landing is the entry)');
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
const guidanceChips = (env.__stage._html.match(/<span class="chip doc">FINTRAC Guidance<\/span>/g) || []).length;  // Phase 33: 5th source
ok(advisoryChips > 0 && alertChips > 0 && ofacChips > 0 && fintracChips > 0 && guidanceChips > 0,
  `unified menu lists all 5 source types (${advisoryChips} advisories + ${alertChips} alerts + ${ofacChips} OFAC + ${fintracChips} FINTRAC OAs + ${guidanceChips} FINTRAC guidance)`);
eq(advisoryChips + alertChips + ofacChips + fintracChips + guidanceChips, api.ADVISORIES.length,
  'every card carries an honest doc_type chip (Advisory/Alert/OFAC/FINTRAC/FINTRAC Guidance)');
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

// (2) Read-advisory (article-processing) screen — Phase 25: extract (verbatim, highlighted) → translate
api.pick(adv.id);
eq(api.view, 'detail', 'pick() enters detail view');
eq(api.screen, 0, 'pick() starts on Read advisory (screen 0)');
ok(/· Read the source/.test(env.__stage._html) && /Extract → translate/.test(env.__stage._html),
  'Article screen renders (extract → translate)');
ok(/class="doc"/.test(env.__stage._html), 'Article renders the full source-document panel');
ok(/class="hl on"/.test(env.__stage._html), 'at least one verbatim red-flag phrase is highlighted in the source');
const xrows = (env.__stage._html.match(/class="xrow"/g) || []).length;
eq(xrows, adv.indicators.length, 'one extract→translate row per indicator');
ok(adv.indicators.every(i => typeof i.red_flag === 'string' && i.red_flag.trim()),
  'every indicator carries a red_flag (the natural AML translation)');
ok(adv.indicators.every(i => env.__stage._html.includes(escH(i.red_flag))),
  'every red_flag (translation) renders in the extract→translate list');
ok(adv.indicators.every(i => i.red_flag.trim() !== i.flag.trim()),
  'each red_flag is distinct from its verbatim flag (a translation, not a copy)');
ok(env.__errors.length === 0, 'Article screen rendered with no console errors');

// (3) Coverage screen — the red_flag is the label, the verbatim stays as the traceable subline
api.gotoScreen(1);
ok(/· Coverage/.test(env.__stage._html) && /Coverage index/.test(env.__stage._html), 'Coverage screen renders');
ok(env.__stage._html.includes(escH(adv.indicators[0].red_flag)), 'Coverage labels indicators by their red_flag');
const cov = api.coverageIndex(adv.indicators);
eq(numText(env, 'gnum'), cov, 'Coverage gauge lands on coverageIndex(indicators) under reduced motion');

// (4) Build recs = the GATE
api.gotoScreen(2);
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

// (5) Signal reflects the gate
api.gotoScreen(3);
const specCards = (env.__stage._html.match(/PROPOSED ·/g) || []).length;
eq(specCards, buildableIds.length, 'Signal drafts one spec card per selected ∩ buildable BUILD_NOW');
ok(/<span class="sk">Red flag<\/span>/.test(env.__stage._html), 'Signal spec card carries the Red flag (translation) row');
// honest empty state #1 — everything deselected (a choice)
api.selected = new Set();
api.gotoScreen(3);
ok(/No build-now gaps selected/.test(env.__stage._html), 'Signal honest empty state: deselected-all');

// (6) Close the loop — 0-picked flat-hold (no fake rise)
api.gotoScreen(5);
ok(/· Close the loop/.test(env.__stage._html), 'Close-the-loop screen renders');
ok(/coverage holds/.test(env.__stage._html), '0-picked close: honest flat-hold note (no fake rise)');
eq(numText(env, 'gnum'), cov, '0-picked close: gauge holds at the before value');

// (6b) Close the loop — commit all BUILD_NOW, coverage rises by the real recompute, indicators not mutated
api.selected = new Set(buildNowIds);
const pickedSet = new Set(buildNowIds);
const afterInds = adv.indicators.map(i => pickedSet.has(i.id) ? Object.assign({}, i, { status: 'covered' }) : i);
const after = api.coverageIndex(afterInds);
api.gotoScreen(5);
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
api2.gotoScreen(5);
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
eq(apiA.view, 'detail', 'alert: pick() enters detail view (Read advisory)');
apiA.gotoScreen(1);
const covA = apiA.coverageIndex(alert.indicators);
eq(numText(envA, 'gnum'), covA, 'alert: Coverage gauge lands on coverageIndex(indicators)');
apiA.gotoScreen(2);
ok(/Build recommendations · gate/.test(envA.__stage._html), 'alert: Build-recs/GATE screen renders');
eq([...apiA.selected].sort().join(','), apiA.buildNows(alert).map(i => i.id).sort().join(','),
  'alert: gate defaults to ALL BUILD_NOW selected');
apiA.gotoScreen(3);
ok(/PROPOSED ·/.test(envA.__stage._html), 'alert: Signal drafts ≥1 spec card for the picks');
apiA.selected = new Set(apiA.buildNows(alert).map(i => i.id));
const afterA = apiA.coverageIndex(alert.indicators.map(i =>
  apiA.selected.has(i.id) ? Object.assign({}, i, { status: 'covered' }) : i));
apiA.gotoScreen(4);                                           // Combination-lift (Phase 26) — exercise it on the way to Close
apiA.gotoScreen(5);
ok(/· Close the loop/.test(envA.__stage._html), 'alert: Close-the-loop screen renders');
eq(numText(envA, 'gnum'), afterA, 'alert: close gauge lands on the recomputed after-coverage');
ok(envA.__errors.length === 0, 'alert: full 6-screen arc walked with no console errors');

// ---- an OFAC advisory walks the full 5-screen arc (Phase 21 — 3rd source / cross-agency proof) ----
const envO = boot(true);
const apiO = envO.__api;
const ofac = apiO.ADVISORIES.filter(a => a.doc_type === 'OFAC' && apiO.isLive(a))
  .find(a => apiO.buildNows(a).some(i => i.build_logic && typeof i.build_logic === 'object'));
ok(ofac, `found a live OFAC advisory with a buildable BUILD_NOW gap (${ofac && ofac.id})`);
apiO.pick(ofac.id);
eq(apiO.view, 'detail', 'ofac: pick() enters detail view (Read advisory)');
apiO.gotoScreen(1);
const covO = apiO.coverageIndex(ofac.indicators);
eq(numText(envO, 'gnum'), covO, 'ofac: Coverage gauge lands on coverageIndex(indicators)');
apiO.gotoScreen(2);
ok(/Build recommendations · gate/.test(envO.__stage._html), 'ofac: Build-recs/GATE screen renders');
apiO.gotoScreen(3);
ok(/PROPOSED ·/.test(envO.__stage._html), 'ofac: Signal drafts ≥1 spec card for the picks');
apiO.selected = new Set(apiO.buildNows(ofac).map(i => i.id));
const afterO = apiO.coverageIndex(ofac.indicators.map(i =>
  apiO.selected.has(i.id) ? Object.assign({}, i, { status: 'covered' }) : i));
apiO.gotoScreen(4);
apiO.gotoScreen(5);
ok(/· Close the loop/.test(envO.__stage._html), 'ofac: Close-the-loop screen renders');
eq(numText(envO, 'gnum'), afterO, 'ofac: close gauge lands on the recomputed after-coverage');
ok(envO.__errors.length === 0, 'ofac: full 6-screen arc walked with no console errors');

// ---- a FINTRAC operational alert walks the full 5-screen arc (Phase 22 — 4th source / FIRST
//      cross-jurisdiction proof). Phase 28 (user's compliance call): the FINTRAC Crown-copyright
//      reproduction clause is REMOVED from the per-doc Source line — it now shows ONLY the document
//      title, and still NEVER the US "public domain" string. ----
const envF = boot(true);
const apiF = envF.__api;
const fintrac = apiF.ADVISORIES.filter(a => a.doc_type === 'FINTRAC' && apiF.isLive(a))
  .find(a => apiF.buildNows(a).some(i => i.build_logic && typeof i.build_logic === 'object'));
ok(fintrac, `found a live FINTRAC operational alert with a buildable BUILD_NOW gap (${fintrac && fintrac.id})`);
apiF.pick(fintrac.id);
eq(apiF.view, 'detail', 'fintrac: pick() enters detail view (Read advisory)');
// Phase 28 (user's compliance call): the on-screen Source LABEL carries the title only — no "© His Majesty…"
// clause inside #stage, and never the US public-domain line. The full Crown-copyright attribution (© + title
// + source URL) moved to the page FOOTER (#attribution), shown only for the FINTRAC doc being reproduced.
ok(!/His Majesty the King in Right of Canada/.test(envF.__stage._html),
  'fintrac: the on-screen Source label carries no © attribution (it moved to the page footer)');
ok(!/public domain/i.test(envF.__stage._html),
  'fintrac: the FINTRAC source panel does NOT claim US public domain');
ok(/His Majesty the King in Right of Canada/.test(envF.document.getElementById('attribution').innerHTML),
  'fintrac: the page footer carries the full Crown-copyright attribution for the doc on screen');
apiF.gotoScreen(1);
const covF = apiF.coverageIndex(fintrac.indicators);
eq(numText(envF, 'gnum'), covF, 'fintrac: Coverage gauge lands on coverageIndex(indicators)');
apiF.gotoScreen(2);
ok(/Build recommendations · gate/.test(envF.__stage._html), 'fintrac: Build-recs/GATE screen renders');
eq([...apiF.selected].sort().join(','), apiF.buildNows(fintrac).map(i => i.id).sort().join(','),
  'fintrac: gate defaults to ALL BUILD_NOW selected');
apiF.gotoScreen(3);
ok(/PROPOSED ·/.test(envF.__stage._html), 'fintrac: Signal drafts ≥1 spec card for the picks');
apiF.selected = new Set(apiF.buildNows(fintrac).map(i => i.id));
const afterF = apiF.coverageIndex(fintrac.indicators.map(i =>
  apiF.selected.has(i.id) ? Object.assign({}, i, { status: 'covered' }) : i));
apiF.gotoScreen(4);
apiF.gotoScreen(5);
ok(/· Close the loop/.test(envF.__stage._html), 'fintrac: Close-the-loop screen renders');
eq(numText(envF, 'gnum'), afterF, 'fintrac: close gauge lands on the recomputed after-coverage');
ok(envF.__errors.length === 0, 'fintrac: full 6-screen arc walked with no console errors');

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
eq(apiB.view, 'detail', 'fintrac-brief: pick() enters detail view (Read advisory)');
ok(!/His Majesty the King in Right of Canada/.test(envB.__stage._html),
  'fintrac-brief: the on-screen Source label carries no © attribution (it moved to the page footer)');
ok(!/public domain/i.test(envB.__stage._html), 'fintrac-brief: the source panel does NOT claim US public domain');
ok(/His Majesty the King in Right of Canada/.test(envB.document.getElementById('attribution').innerHTML),
  'fintrac-brief: the page footer carries the full Crown-copyright attribution for the doc on screen');

// Phase 28 — the footer licence attribution is PER-DOCUMENT: the full © + complete title + source URL for
// the FINTRAC doc being reproduced, and EMPTY for US public-domain docs (a static © line would misattribute
// US federal works to the Canadian Crown — so it must be conditional on the doc on screen).
const envAt = boot(true);
const apiAt = envAt.__api;
const finAt = apiAt.ADVISORIES.find(a => a.doc_type === 'FINTRAC' && apiAt.isLive(a) && a.url && a.title);
ok(finAt, `found a FINTRAC doc with a title + URL for the footer-attribution check (${finAt && finAt.id})`);
apiAt.pick(finAt.id);
const finAttrib = envAt.document.getElementById('attribution').innerHTML;
ok(finAttrib.includes(finAt.url) && finAttrib.includes(escH(finAt.title)),
  'footer attribution: the FINTRAC attribution is licence-complete (© clause + complete title + source URL)');
const usAt = apiAt.ADVISORIES.find(a => a.jurisdiction === 'US' && apiAt.isLive(a));
apiAt.pick(usAt.id);
eq(envAt.document.getElementById('attribution').innerHTML, '',
  'footer attribution: a US public-domain doc shows NO Crown-copyright attribution (the .attrib slot is empty)');
apiB.gotoScreen(1);
const covB = apiB.coverageIndex(brief.indicators);
eq(numText(envB, 'gnum'), covB, 'fintrac-brief: Coverage gauge lands on coverageIndex(indicators)');
apiB.gotoScreen(2);
ok(/Build recommendations · gate/.test(envB.__stage._html), 'fintrac-brief: Build-recs/GATE screen renders');
eq([...apiB.selected].sort().join(','), apiB.buildNows(brief).map(i => i.id).sort().join(','),
  'fintrac-brief: gate defaults to ALL BUILD_NOW selected');
apiB.gotoScreen(3);
ok(/PROPOSED ·/.test(envB.__stage._html), 'fintrac-brief: Signal drafts ≥1 spec card for the picks');
apiB.selected = new Set(apiB.buildNows(brief).map(i => i.id));
const afterB = apiB.coverageIndex(brief.indicators.map(i =>
  apiB.selected.has(i.id) ? Object.assign({}, i, { status: 'covered' }) : i));
apiB.gotoScreen(4);
apiB.gotoScreen(5);
ok(/· Close the loop/.test(envB.__stage._html), 'fintrac-brief: Close-the-loop screen renders');
eq(numText(envB, 'gnum'), afterB, 'fintrac-brief: close gauge lands on the recomputed after-coverage');
ok(envB.__errors.length === 0, 'fintrac-brief: full 6-screen arc walked with no console errors');

// ---- the CROSS-CORPUS SYNTHESIS view (Phase 24): group documents by typology, show COMBINED coverage
//      across a cross-jurisdiction cluster as honest UNION arithmetic (NO similarity/overlap/lift — the
//      Ph18 precision-lift rejection), with drill-through into each doc's existing per-doc arc and a
//      Back that returns to the origin cluster. ----
const envS = boot(true);
const apiS = envS.__api;

// (S1) the Documents/Typologies toggle + the typology-grouped picker
apiS.selMode = 'typology'; apiS.renderSelect();
const cl = apiS.clusters();
ok(cl.length > 0, `clusters() groups the corpus by typology (${cl.length} typologies)`);
const xj = cl.filter(c => c.xj);
ok(xj.length >= 2, `≥2 typologies are cross-jurisdiction US+Canada (${xj.length}: ${xj.map(c => c.t).join(', ')})`);
const typoCards = (envS.__stage._html.match(/class="advcard live typo"/g) || []).length;
eq(typoCards, cl.length, 'typology mode renders one cluster card per typology');
ok(/cross-jurisdiction/.test(envS.__stage._html), 'typology mode flags cross-jurisdiction clusters');
ok(envS.__errors.length === 0, 'typology-mode picker rendered with no console errors');

// (S2) a cross-jurisdiction cluster's synthesis screen — combined coverage is the honest union
const cluster = xj[0];                                  // clusters() sorts cross-jurisdiction first
apiS.enterSynthesis(cluster.t);
eq(apiS.view, 'synthesis', 'enterSynthesis() enters the synthesis view');
eq(apiS.currentTypology, cluster.t, 'currentTypology is the chosen cluster');
const cdocs = apiS.clusterFor(cluster.t);
const synthrows = (envS.__stage._html.match(/class="covrow synthrow"/g) || []).length;
eq(synthrows, cdocs.length, 'synthesis lists one clickable row per contributing document');
// Phase 37: combined coverage is over the typology's INDICATORS (per-indicator pooling), not docs' full lists
const pool = apiS.indsForTypology(cluster.t).map(r => r.i);
eq(numText(envS, 'gnum'), apiS.coverageIndex(pool),
  'combined coverage = coverageIndex over the typology’s pooled indicators (honest per-indicator set arithmetic)');
ok(/chip jur us/.test(envS.__stage._html) && /chip jur ca/.test(envS.__stage._html),
  'a cross-jurisdiction cluster shows BOTH US and Canada jurisdiction chips');
ok(/No single regulator enumerates all of/.test(envS.__stage._html), 'the cross-jurisdiction headline lands');

// (S2b) HONESTY GATE — no fabricated cross-corpus metric; the de-dup disclaimer is present
ok(/NOT de-duplicated or matched across regulators/.test(envS.__stage._html),
  'honesty note: indicators are NOT de-duplicated/matched across regulators');
ok(!/\d+\s*%\s*(similar|overlap|match)/i.test(envS.__stage._html) && !/\blift\b/i.test(envS.__stage._html),
  'synthesis claims NO similarity/overlap/lift metric');

// (S3) every clustered indicator stays traceable to its source document (data-id on each row)
ok(cdocs.every(d => envS.__stage._html.includes(`data-id="${d.id}"`)),
  'each cluster row is traceable to its source document (data-id)');
ok(envS.__errors.length === 0, 'synthesis screen rendered with no console errors');

// (S4) drill-through into a doc's per-doc arc, and Back returns to the origin cluster (not the picker)
apiS.pick(cdocs[0].id, cluster.t);
eq(apiS.view, 'detail', 'clicking a cluster row drills into the per-doc arc');
eq(apiS.fromTypology, cluster.t, 'the drilled doc remembers its origin cluster');
ok(/· Read the source/.test(envS.__stage._html), 'drill lands on the doc’s own Read-advisory screen');
apiS.back();
eq(apiS.view, 'synthesis', 'Back from the first detail screen returns to the origin cluster (not the picker)');
eq(apiS.currentTypology, cluster.t, 'Back lands on the same cluster');

// (S5) a singleton typology still renders honestly (one document, no fabricated combine)
const single = cl.find(c => c.docs.length === 1);
if (single) {
  apiS.enterSynthesis(single.t);
  ok(/One corpus document covers/.test(envS.__stage._html), `a singleton cluster renders honestly (${single.t})`);
}

// (S6) toSelect() fully resets the synthesis state
apiS.toSelect();
eq(apiS.view, 'select', 'toSelect() returns to the picker');
ok(apiS.currentTypology === null && apiS.fromTypology === null, 'toSelect() clears the synthesis state');
ok(envS.__errors.length === 0, 'the full synthesis flow produced no console errors');

/* ===================== Phase 29 — the CAPABILITY LENS ===================== */
// re-project the corpus by DETECTION CAPABILITY: a third Select mode → per-capability DEMAND (honest
// count) + the institution's interview POSTURE + the covered/partial/gap split, gap-priority sorted →
// drill into a capability → its indicators grouped by source document → drill into a doc's per-doc arc →
// Back returns to the capability. Honest counts only (NO similarity/overlap/lift); the derived records
// already carry the capability/data_source codes — this re-projects them, it does not re-derive.
console.log('\n— Phase 29: the capability lens —');
const envC = boot(true);
const apiC = envC.__api;

// (C1) the taxonomy is present + well-shaped (referential integrity is gated upstream in build.py)
ok(Array.isArray(apiC.CAPS) && apiC.CAPS.length === 28, `taxonomy carries 28 capabilities (got ${apiC.CAPS && apiC.CAPS.length})`);
ok(apiC.CAPS.every(c => c.id && c.name && ['y', 'n', 'partial'].includes(c.posture)),
  'every capability has an id + name + a posture ∈ {y,n,partial}');

// (C2) the Capabilities Select mode renders one card per demanded capability, gap-priority sorted
apiC.selMode = 'capability'; apiC.renderSelect();
const ag = apiC.capAgg();
ok(ag.length > 0 && ag.every(x => x.demand > 0), `capAgg() returns only demanded capabilities (${ag.length})`);
const capCards = (envC.__stage._html.match(/class="advcard live cap"/g) || []).length;
eq(capCards, ag.length, 'capability mode renders one card per demanded capability');
ok(/Capabilities<\/button>/.test(envC.__stage._html), 'the Documents/Typologies/Capabilities toggle shows the third mode');
const prank = { n: 0, partial: 1, y: 2 };
ok(ag.every((x, i) => i === 0 || prank[ag[i - 1].c.posture] <= prank[x.c.posture]),
  'capabilities are sorted gap-priority (not-yet first, then partial, then in-place)');
ok(envC.__errors.length === 0, 'capability-mode picker rendered with no console errors');

// (C2b) HONESTY — demand/coverage are honest counts; no fabricated cross-capability metric in the picker
ok(!/\blift\b/i.test(envC.__stage._html) && !/\d+\s*%\s*(similar|overlap|match)/i.test(envC.__stage._html),
  'capability picker claims NO similarity/overlap/lift metric');
// the per-capability demand on each card is the honest count from capAgg (not a fabricated figure)
ok(ag.every(x => envC.__stage._html.includes(`${x.demand} indicator${x.demand === 1 ? '' : 's'} · ${x.docs} doc`)),
  'each capability card shows its honest demand + document count');

// (C3) drill into the highest-exposure capability — its pool = every live indicator carrying that code
const topCap = ag[0];
apiC.enterCapability(topCap.c.id);
eq(apiC.view, 'capability', 'enterCapability() enters the capability view');
eq(apiC.currentCapability, topCap.c.id, 'currentCapability is the chosen capability');
const poolC = apiC.indsForCap(topCap.c.id).map(r => r.i);
eq(poolC.length, topCap.demand, 'the capability view pools exactly the indicators carrying that capability code');
eq(numText(envC, 'gnum'), apiC.coverageIndex(poolC),
  'capability coverage = coverageIndex over the indicators that depend on it (honest set arithmetic)');
ok(/Capability coverage/.test(envC.__stage._html), 'the capability gauge labels honestly');
ok(/NOT de-duplicated or matched across sources/.test(envC.__stage._html),
  'honesty note: indicators are NOT de-duplicated/matched across sources');
ok(envC.__errors.length === 0, 'capability drill rendered with no console errors');

// (C3b) one clickable drill row per contributing document, each traceable by id
const docsC = [...new Set(apiC.indsForCap(topCap.c.id).map(r => r.a.id))];
const capRows = (envC.__stage._html.match(/class="covrow synthrow"/g) || []).length;
eq(capRows, docsC.length, 'the capability view lists one clickable row per contributing document');
ok(docsC.every(id => envC.__stage._html.includes(`data-id="${id}"`)),
  'each capability document row is traceable to its source (data-id)');

// (C4) drill into a doc's per-doc arc; Back returns to the origin capability (not the picker)
apiC.pick(docsC[0], null, topCap.c.id);
eq(apiC.view, 'detail', 'clicking a capability document row drills into the per-doc arc');
eq(apiC.fromCapability, topCap.c.id, 'the drilled doc remembers its origin capability');
apiC.back();
eq(apiC.view, 'capability', 'Back from the first detail screen returns to the origin capability (not the picker)');
eq(apiC.currentCapability, topCap.c.id, 'Back lands on the same capability');

// (C5) toSelect() fully resets the capability state
apiC.toSelect();
eq(apiC.view, 'select', 'toSelect() returns to the picker');
ok(apiC.currentCapability === null && apiC.fromCapability === null, 'toSelect() clears the capability state');
ok(envC.__errors.length === 0, 'the full capability-lens flow produced no console errors');

/* ===================== Phase 30 — the DATA-SOURCE LENS ===================== */
// the symmetric counterpart to the capability lens on the D1–D20 data axis: a FOURTH Select mode →
// per-data-source DEMAND (honest count) + the institution's access POSTURE + the covered/partial/gap
// split, gap-priority sorted → drill into a data source → its indicators grouped by source document
// (+ the capabilities they implement, the inverse panel) → drill into a doc's per-doc arc → Back returns
// to the data source. Honest counts only (NO similarity/overlap/lift); build.py + the taxonomy + the 42
// records were already inlined/validated in Phase 29 — this is a pure UI re-projection of the data_source codes.
console.log('\n— Phase 30: the data-source lens —');
const envD = boot(true);
const apiD = envD.__api;

// (D1) the data-source taxonomy is present + well-shaped (referential integrity gated upstream in build.py)
ok(Array.isArray(apiD.DSRC) && apiD.DSRC.length === 20, `taxonomy carries 20 data sources (got ${apiD.DSRC && apiD.DSRC.length})`);
ok(apiD.DSRC.every(d => d.id && d.name && ['y', 'n', 'partial'].includes(d.posture)),
  'every data source has an id + name + a posture ∈ {y,n,partial}');

// (D2) the Data-sources Select mode renders one card per demanded data source, gap-priority sorted
apiD.selMode = 'datasource'; apiD.renderSelect();
const dag = apiD.dsAgg();
ok(dag.length > 0 && dag.every(x => x.demand > 0), `dsAgg() returns only demanded data sources (${dag.length})`);
const dsCards = (envD.__stage._html.match(/class="advcard live ds"/g) || []).length;
eq(dsCards, dag.length, 'data-source mode renders one card per demanded data source');
ok(/Data sources<\/button>/.test(envD.__stage._html), 'the Documents/Typologies/Capabilities/Data sources toggle shows the fourth mode');
const drank = { n: 0, partial: 1, y: 2 };
ok(dag.every((x, i) => i === 0 || drank[dag[i - 1].d.posture] <= drank[x.d.posture]),
  'data sources are sorted gap-priority (not-yet first, then partial, then in-place)');
ok(envD.__errors.length === 0, 'data-source-mode picker rendered with no console errors');

// (D2b) HONESTY — demand/coverage are honest counts; no fabricated cross-source metric in the picker
ok(!/\blift\b/i.test(envD.__stage._html) && !/\d+\s*%\s*(similar|overlap|match)/i.test(envD.__stage._html),
  'data-source picker claims NO similarity/overlap/lift metric');
ok(dag.every(x => envD.__stage._html.includes(`${x.demand} indicator${x.demand === 1 ? '' : 's'} · ${x.docs} doc`)),
  'each data-source card shows its honest demand + document count');

// (D2c) the lens is genuinely DISTINCT from the capability lens — at least one feed is "not yet" available
// (the SOURCE_DATA / data-access exposure the capability lens can't surface)
ok(dag.some(x => x.d.posture === 'n'), 'at least one demanded data source is "not yet" available (the data-access exposure)');

// (D3) drill into the highest-exposure data source — its pool = every live indicator carrying that code
const topDS = dag[0];
apiD.enterDataSource(topDS.d.id);
eq(apiD.view, 'datasource', 'enterDataSource() enters the data-source view');
eq(apiD.currentDataSource, topDS.d.id, 'currentDataSource is the chosen data source');
const poolD = apiD.indsForDS(topDS.d.id).map(r => r.i);
eq(poolD.length, topDS.demand, 'the data-source view pools exactly the indicators carrying that data_source code');
eq(numText(envD, 'gnum'), apiD.coverageIndex(poolD),
  'data-source coverage = coverageIndex over the indicators that depend on it (honest set arithmetic)');
ok(/Data-source coverage/.test(envD.__stage._html), 'the data-source gauge labels honestly');
ok(/Implements capabilities/.test(envD.__stage._html), 'the data-source view shows the capabilities its indicators implement (the inverse panel)');
ok(/NOT de-duplicated or matched across sources/.test(envD.__stage._html),
  'honesty note: indicators are NOT de-duplicated/matched across sources');
ok(envD.__errors.length === 0, 'data-source drill rendered with no console errors');

// (D3b) one clickable drill row per contributing document, each traceable by id
const docsD = [...new Set(apiD.indsForDS(topDS.d.id).map(r => r.a.id))];
const dsRows = (envD.__stage._html.match(/class="covrow synthrow"/g) || []).length;
eq(dsRows, docsD.length, 'the data-source view lists one clickable row per contributing document');
ok(docsD.every(id => envD.__stage._html.includes(`data-id="${id}"`)),
  'each data-source document row is traceable to its source (data-id)');

// (D4) drill into a doc's per-doc arc; Back returns to the origin data source (not the picker)
apiD.pick(docsD[0], null, null, topDS.d.id);
eq(apiD.view, 'detail', 'clicking a data-source document row drills into the per-doc arc');
eq(apiD.fromDataSource, topDS.d.id, 'the drilled doc remembers its origin data source');
apiD.back();
eq(apiD.view, 'datasource', 'Back from the first detail screen returns to the origin data source (not the picker)');
eq(apiD.currentDataSource, topDS.d.id, 'Back lands on the same data source');

// (D5) toSelect() fully resets the data-source state
apiD.toSelect();
eq(apiD.view, 'select', 'toSelect() returns to the picker');
ok(apiD.currentDataSource === null && apiD.fromDataSource === null, 'toSelect() clears the data-source state');
ok(envD.__errors.length === 0, 'the full data-source-lens flow produced no console errors');

/* ===== Phase 26 — register beats: source grouping/sort, section grouping, build-log, combination-lift ===== */
const env26 = boot(true);
const api26 = env26.__api;
const s26 = env26.__stage._html;

// (P26-1) Select grouped by SOURCE, newest-first within each group
eq((s26.match(/class="srcgroup"/g) || []).length, 5,
  'Select groups documents into 5 source sections (Advisories / Alerts / OFAC / FINTRAC OAs / FINTRAC guidance)');
['FinCEN Advisories', 'FinCEN Alerts', 'OFAC Advisories', 'FINTRAC Operational Alerts &amp; Briefs', 'FINTRAC Sector Guidance'].forEach(l =>
  ok(s26.includes(l), `source-group header present: "${l}"`));   // labels render through esc() — & is &amp;
const advBlock = s26.slice(s26.indexOf('FinCEN Advisories'), s26.indexOf('FinCEN Alerts'));
const renderedAdvIds = [...advBlock.matchAll(/class="advcard [^"]*" data-id="([^"]+)"/g)].map(m => m[1]);
const expectedAdvIds = api26.ADVISORIES.filter(a => (a.doc_type || 'Advisory') === 'Advisory').slice()
  .sort((x, y) => String(y.date || '').localeCompare(String(x.date || '')) || String(x.id).localeCompare(String(y.id)))
  .map(a => a.id);
eq(renderedAdvIds.join(','), expectedAdvIds.join(','), 'Advisories group is sorted newest-first (date desc)');

// (P26-2) red-flag grouping by SECTION on Coverage — multi-section doc shows sub-headers; single-section is flat
const multi = api26.ADVISORIES.find(a => api26.isLive(a) &&
  new Set(a.indicators.map(i => i.section || '')).size > 1 && a.indicators.every(i => i.section));
ok(multi, `found a multi-section doc for section grouping (${multi && multi.id})`);
api26.pick(multi.id); api26.gotoScreen(1);
ok(/class="secthead"/.test(env26.__stage._html), 'Coverage of a multi-section doc renders section sub-headers');
// a single-section doc renders flat (no sub-headers). The complete re-extraction (Phase 28) gave EFE two
// sections (Behavioral/Financial Red Flags), so pick a genuinely single-section live doc dynamically.
const flat = api26.ADVISORIES.find(a => api26.isLive(a) &&
  (new Set(a.indicators.map(i => i.section || '')).size <= 1 || !a.indicators.every(i => i.section)));
ok(flat, `found a single-section doc for the flat-render check (${flat && flat.id})`);
api26.pick(flat.id); api26.gotoScreen(1);
ok(!/class="secthead"/.test(env26.__stage._html), `Coverage of a single-section doc (${flat && flat.id}) renders flat — no section noise`);
const efe = api26.ADVISORIES.find(a => a.id === 'fin-2022-a002');     // EFE — for the progressive-render settle check

// (P26-3) progressive article render SETTLES to the final state (reduced motion = the resting paint)
api26.pick(efe.id);
ok(/phrase.? extracted/.test(env26.__stage._html) && !/reading…/.test(env26.__stage._html),
  'Read-advisory settles to the final "phrases extracted" state (progressive render resting paint)');

// (P26-4) build-log on Signal (Act-4 port) — structural, reads the real build_logic, NO numbers
const adv26 = api26.ADVISORIES.filter(api26.isLive)
  .find(a => api26.buildNows(a).some(i => i.build_logic && typeof i.build_logic === 'object'));
api26.pick(adv26.id); api26.gotoScreen(3);
ok(/class="buildlog"/.test(env26.__stage._html) && /Agent build log/.test(env26.__stage._html),
  'Signal renders the agent build-log (Act-4 port)');
eq((env26.__stage._html.match(/class="blstep/g) || []).length, 6, 'build-log has 6 structural steps');
ok(/PROPOSED ·/.test(env26.__stage._html), 'Signal still drafts the spec card(s) below the build-log');

// (P45-T2) combination-lift — the R2 REAL composition search space (Phase 45 replaced the Phase-26
// generic illustrative template). The expected counts are recomputed INDEPENDENTLY from the COMMITTED
// DATA FILES (data/*/derived/*.json + the two typology overlays) — never from __CORPUS__ or the DOM —
// so a wrong on-screen count (NaN→0, double-count) can never pin itself as truth.
const DATA45 = resolve(HERE, '..', 'data');
const SRCS45 = [['fincen','Advisory'],['fincen-alerts','Alert'],['ofac','OFAC'],['fintrac','FINTRAC'],['fintrac-guidance','FINTRAC Guidance']];
const REG45 = {'Advisory':'FinCEN','Alert':'FinCEN','OFAC':'OFAC','FINTRAC':'FINTRAC','FINTRAC Guidance':'FINTRAC'};
const tv45 = v => (typeof v === 'string') ? v : (v && v.typology) || null;
const dmap45r = JSON.parse(readFileSync(resolve(DATA45, 'typology-map.json'), 'utf8'));
const dmap45 = dmap45r.map || dmap45r;
const imap45r = JSON.parse(readFileSync(resolve(DATA45, 'indicator-typology-map.json'), 'utf8'));
const imap45 = imap45r.map || imap45r;
const recs45 = [];
for (const [dir, dt] of SRCS45)
  for (const f of readdirSync(resolve(DATA45, dir, 'derived')).filter(f => f.endsWith('.json')))
    recs45.push({ rec: JSON.parse(readFileSync(resolve(DATA45, dir, 'derived', f), 'utf8')), dt, fid: f.replace(/\.json$/, '') });
const covByTyp45 = new Map(); let covAll45 = 0; const regsAll45 = new Set();
for (const { rec, dt, fid } of recs45) {
  const did = rec.id || fid;
  for (const i of rec.indicators || []) {
    if (i.status !== 'covered') continue;
    const typ = tv45(imap45[`${did}/${i.id}`]) || tv45(dmap45[did]);   // overlay keys are doc-qualified
    if (!covByTyp45.has(typ)) covByTyp45.set(typ, { n: 0, regs: new Set() });
    const e = covByTyp45.get(typ); e.n++; e.regs.add(REG45[dt]);
    covAll45++; regsAll45.add(REG45[dt]);
  }
}
function expected45(docId) {                 // mirrors renderLift's derivation RULE, from data files only
  const r = recs45.find(x => (x.rec.id || x.fid) === docId);
  const first = (r.rec.indicators || []).filter(i => i.build_rec === 'BUILD_NOW')
    .find(i => i.build_logic && typeof i.build_logic === 'object');
  const typ = first ? (tv45(imap45[`${docId}/${first.id}`]) || tv45(dmap45[docId])) : null;
  const e = typ && covByTyp45.get(typ);
  return (e && e.n) ? { n: e.n, regs: e.regs.size } : { n: covAll45, regs: regsAll45.size };
}
api26.gotoScreen(4);
const lift45 = env26.__stage._html;
const exp45 = expected45(adv26.id);
ok(/· Combination lift/.test(lift45), 'screen 4 is the Combination-lift beat');
ok(/candidate composition partner/.test(lift45), 'R2: the real composition search space renders (stable marker)');
eq(numText(env26, 'lfn'), exp45.n, `R2 partner count equals the INDEPENDENTLY recomputed covered inventory (${exp45.n})`);
ok(new RegExp(`<span class="lfn">${exp45.regs}</span>`).test(lift45),
  `R2 regulator count equals the independent recomputation (${exp45.regs})`);
ok(!/\d+\s*%/.test(lift45), 'NO percentage anywhere on the lift screen — inventory facts only, no performance claim');
ok(!/liftbar|pending calibration|class="illus"/.test(lift45),
  'the fake 18→64→83 bars and the "pending calibration" disclaimer are GONE (nothing left to disclaim)');
ok(/promotion gate/.test(lift45), 'the promotion gate closes the beat');
ok(/NOT de-duplicated or matched across regulators/.test(lift45), 'the honest-union disclosure stays on the framenote');
ok(env26.__errors.length === 0, 'grouping + build-log + lift rendered with no console errors');

// (P26-6) combination-lift honest empty state when nothing is committed at the gate
api26.selected = new Set(); api26.gotoScreen(4);
ok(/class="empty"/.test(env26.__stage._html) && /No signal committed/.test(env26.__stage._html),
  'combination-lift shows an honest empty state when nothing is committed');

// (P45-T2b) animated (non-reduced) — the partner count counts up to the REAL inventory value
const env26b = boot(false);
const api26b = env26b.__api;
const adv26b = api26b.ADVISORIES.find(a => a.id === adv26.id);
api26b.pick(adv26b.id);
api26b.selected = new Set(api26b.buildNows(adv26b).map(i => i.id));
api26b.gotoScreen(4);
env26b.__flush();                                            // run the deferred T() → animVal → rAF chain
eq(numText(env26b, 'lfn'), exp45.n, 'animated: the partner count-up reaches the real inventory value after the timer flush');
ok(env26b.__errors.length === 0, 'animated combination-lift produced no console errors');

/* ===================== Phase 27 — presentation fixes (T2 cleaner / T3 highlight / T4 build-beat) ===================== */
const env27 = boot(true);
const api27 = env27.__api;
// (P27-1) T2: the displayed source is markitdown-CLEANED — a header-dirty FinCEN advisory's doc panel
// carries no running header / letter-spaced header / tab-soup. (T3) normalize-both-sides highlighting
// lands on ~every grounded flag — not the old best-effort literal match.
const dirty27 = api27.ADVISORIES.find(a => a.id === 'FIN-2020-A008' && api27.isLive(a))
  || api27.ADVISORIES.filter(api27.isLive).find(a => typeof a.article_text === 'string' && /FINCEN ADVISORY/.test(a.article_text));
ok(dirty27, `found a header-dirty live advisory for the T2 cleaner check (${dirty27 && dirty27.id})`);
api27.pick(dirty27.id);
const doc27 = (env27.__stage._html.match(/<div class="doc"[^>]*>([\s\S]*?)<\/div>/) || [])[1] || '';
ok(doc27.length > 100 && !/FINCEN ADVISORY|FINCEN ALERT|F I N C E N/.test(doc27) && !doc27.includes('\t'),
  'T2: cleaned article panel carries no running-header / letter-spaced / tab-soup markitdown artifacts');
const hl27 = (env27.__stage._html.match(/class="hl on"/g) || []).length;
ok(hl27 >= Math.ceil(dirty27.indicators.length * 0.8),
  `T3: normalize-both-sides highlighting lands on ≥80% of grounded flags (${hl27}/${dirty27.indicators.length})`);
ok(env27.__errors.length === 0, 'T2/T3: cleaned + highlighted article rendered with no console errors');
// (P27-2) T4: the build-log renders in a proposal grid (spec | buildside) with the 6-step sequence; the
// Combination-lift carries the lift-side rationale panel and OMITS firestat (no fabricated stats).
const buildable27 = api27.ADVISORIES.filter(api27.isLive)
  .find(a => api27.buildNows(a).some(i => i.build_logic && typeof i.build_logic === 'object'));
api27.pick(buildable27.id);
api27.selected = new Set(api27.buildNows(buildable27).map(i => i.id));
api27.gotoScreen(3);
ok(/class="proposal"/.test(env27.__stage._html) && /class="buildside"/.test(env27.__stage._html),
  'T4: Signal renders the build-log in a proposal grid (spec | buildside)');
eq((env27.__stage._html.match(/class="blstep/g) || []).length, 6,
  'T4: the build-log carries the 6-step agent-build sequence');
api27.gotoScreen(4);
ok(/class="liftwrap"/.test(env27.__stage._html) && /class="liftside"/.test(env27.__stage._html),
  'T4: Combination-lift renders the lift-side rationale panel (liftwrap grid)');
ok(!/firestat/.test(env27.__stage._html),
  'T4: lift OMITS firestat (no fabricated fire-count / precision stats — only the badged illustrative template)');
ok(env27.__errors.length === 0, 'T4: Signal build-log + lift rendered with no console errors');

/* ===================== Phase 28 — display polish (de-piped tables) + the streaming read ===================== */
// markitdown renders figures/tables as markdown PIPE GRIDS (`| --- |` rule rows + `| CELL | CELL |`); the
// cleaner de-pipes them to readable text (display only — normalize() drops `|`/spaces, so grounding +
// highlighting are unchanged). The worst offender (fin-2021-a004's ransomware-flow figure) must render no grid.
const envTbl = boot(true);
const apiTbl = envTbl.__api;
const tableDoc = (apiTbl.ADVISORIES.find(a => a.id === 'fin-2021-a004' && apiTbl.isLive(a))
  || apiTbl.ADVISORIES.filter(apiTbl.isLive).find(a => typeof a.article_text === 'string' && /\n\s*\|.*\|/.test(a.article_text)));
ok(tableDoc, `found a doc whose markitdown source had pipe-grid tables (${tableDoc && tableDoc.id})`);
apiTbl.pick(tableDoc.id);
const docTbl = (envTbl.__stage._html.match(/<div class="doc"[^>]*>([\s\S]*?)<\/div>/) || [])[1] || '';
ok(docTbl.length > 100 && !/\|[^|\n]*\|[^|\n]*\|/.test(docTbl),
  'display polish: the source panel carries no markdown pipe-grid rows (de-piped to readable prose)');

/* ===================== Phase 28 — the streaming "agent reading" read (renderArticle redo) ===================== */
// The reduced-motion settle test (P26-3) only covers the resting paint; the bug it MISSED was that the
// full-motion read was "staged" (whole text placed at once, ~48s of highlight-popping). This drives the
// FULL-MOTION path the reduced shim skips: under motion the source STREAMS in (the panel fills, the
// `reading` caret trails), each red-flag phrase highlights ONLY as the read reaches it, every translation
// extracts, and it settles to all-highlighted with the caret removed. (dynEl now backs append/classList;
// __drain runs the whole nested T(read) chain — the shim ignores delays, so this is timeline-agnostic.)
const env28 = boot(false);
const api28 = env28.__api;
const small28 = api28.ADVISORIES.filter(api28.isLive)
  .find(a => typeof a.article_text === 'string' && a.article_text.length > 0
    && a.indicators.length >= 3 && a.indicators.length <= 12);
ok(small28, `found a small live doc for the full-motion streaming read (${small28 && small28.id})`);
api28.pick(small28.id);
const doc28 = () => env28.document.getElementById('doc');
const xlabel28 = () => env28.document.getElementById('xlabel');
ok(doc28().classList.contains('reading') && doc28()._html === '',
  'streaming read: the panel starts EMPTY with the reading caret (progressive, not staged)');
ok(/·\s*0 red flag/.test(xlabel28().textContent),
  'streaming read: the translate count starts at 0 and counts up — NOT the full count shown up-front (staged tell)');
env28.__drain();                                                // run the entire T(read) streaming chain
const streamed28 = doc28()._html;
const hl28 = (streamed28.match(/class="hl on"/g) || []).length;
ok(streamed28.length > 200, 'streaming read: the source streamed into the panel (text present after the read)');
ok(hl28 >= Math.ceil(small28.indicators.length * 0.8),
  `streaming read: each reached phrase highlighted as the read passed it (${hl28}/${small28.indicators.length})`);
eq((env28.document.getElementById('xlate')._html.match(/class="xrow"/g) || []).length, small28.indicators.length,
  'streaming read: every indicator extracted a translation row by the end');
ok(new RegExp(`· ${small28.indicators.length} red flag`).test(xlabel28().textContent),
  'streaming read: the translate count finishes at the full count once the read completes');
ok(!doc28().classList.contains('reading'), 'streaming read: the caret is removed once the read completes (settled)');
ok(env28.__errors.length === 0, 'streaming read: full-motion streaming produced no console errors');

/* ===== Phase 33 — corpus completeness (FINTRAC sector-guidance source #5) + typology re-segmentation ===== */
const env33 = boot(true);
const api33 = env33.__api;
// (P33-1) the 5th source — FINTRAC per-sector ML/TF indicator guidance — is live and dense
const guid33 = api33.ADVISORIES.filter(a => a.doc_type === 'FINTRAC Guidance' && api33.isLive(a));
ok(guid33.length >= 10, `FINTRAC sector-guidance source present and derived (${guid33.length} live sector pages)`);
const fe33 = api33.ADVISORIES.find(a => a.id === 'fintrac-guid-financial-entities');
ok(fe33 && api33.isLive(fe33) && fe33.indicators.length > 100,
  `financial-entities guidance is dense (${fe33 && fe33.indicators.length} indicators)`);
// (P33-2) corpus scale — +5 FinCEN advisories + 11 FINTRAC guidance docs; indicators more than doubled
eq(api33.ADVISORIES.length, 62, 'corpus has 62 publications (Phase 33: +5 FinCEN + 11 FINTRAC guidance)');
eq(api33.ADVISORIES.filter(a => api33.isLive(a)).length, 56, 'corpus has 56 derived documents');
const totalInd33 = api33.ADVISORIES.filter(a => api33.isLive(a)).reduce((s, a) => s + a.indicators.length, 0);
ok(totalInd33 > 2000, `corpus indicators more than doubled (${totalInd33}, was 875)`);
// (P33-3) a FINTRAC guidance doc walks the full per-doc arc — Crown-copyright held, no US public-domain claim
api33.pick(fe33.id);
eq(api33.view, 'detail', 'guidance: pick() enters detail view');
ok(!/public domain/i.test(env33.__stage._html), 'guidance: source panel does NOT claim US public domain');
ok(/His Majesty the King in Right of Canada/.test(env33.document.getElementById('attribution').innerHTML),
  'guidance: page footer carries the Crown-copyright attribution for the doc on screen');
// (P33-3b) the FINTRAC-guidance HTML→markitdown glossary links are DISPLAY-stripped — the rendered Read
// panel (article + verbatim flag quotes) carries no "[text](/url)" residue, and the de-linked flags still
// highlight in the de-linked article (the strip is applied consistently at article + flag + matcher).
const readHtml33 = env33.__stage._html;
ok(!/\]\((\/|#)/.test(readHtml33),
  'guidance: rendered Read panel strips markitdown glossary-link syntax (no "](/" or "](#" residue)');
ok((readHtml33.match(/class="hl on"/g) || []).length > 0,
  'guidance: de-linked flags still highlight in the de-linked dense article');
for (let s = 1; s <= 5; s++) api33.gotoScreen(s);
ok(/· Close the loop/.test(env33.__stage._html), 'guidance: Close-the-loop screen renders');
ok(env33.__errors.length === 0, 'guidance: full per-doc arc walked with no console errors');
// (P33-4) typology re-segmentation — TBML is now its own typology; the sector baselines + new crime typologies
const env33t = boot(true);
const api33t = env33t.__api;
api33t.selMode = 'typology'; api33t.renderSelect();
const typset33 = new Set(api33t.clusters().map(c => c.t));
ok(typset33.has('trade-based-money-laundering'), 'TBML is now its own typology (ofac-sham-transactions re-segmented)');
ok(typset33.has('virtual-currency') && typset33.has('unlawful-employment') && typset33.has('casino-gaming'),
  'new crime typologies present: virtual-currency, unlawful-employment, casino-gaming');
const tbml33 = api33t.clusterFor('trade-based-money-laundering');
ok(tbml33.some(d => d.id === 'ofac-sham-transactions'),
  'TBML cluster contains the re-segmented ofac-sham-transactions doc');
ok(env33t.__errors.length === 0, 'typology re-segmentation view rendered with no console errors');

// (P37) per-indicator typology — the FINTRAC sector pages distribute across real typology clusters; the catch-all retires
ok(!typset33.has('fintrac-sector-baselines'), 'the fintrac-sector-baselines catch-all is RETIRED (no such cluster)');
ok(typset33.has('cross-cutting-indicators'), 'the honest cross-cutting-indicators bucket holds the generic sector indicators');
ok(typset33.has('corruption') && typset33.has('terrorist-financing'),
  'corruption + terrorist-financing clusters exist (the sector pages distribute into them)');
const feTypos = new Set((api33t.ADVISORIES.find(a => a.id === 'fintrac-guid-financial-entities').indicators).map(i => i.typology));
ok(feTypos.has('corruption') && feTypos.has('terrorist-financing') && feTypos.has('cross-cutting-indicators') && feTypos.size >= 3,
  `a FINTRAC sector page distributes across ≥3 typologies incl. corruption + TF (${[...feTypos].sort().join(', ')})`);
const corrDocs = new Set(api33t.clusterFor('corruption').map(d => d.id));
ok(corrDocs.has('fintrac-guid-financial-entities') && corrDocs.has('fintrac-guid-msb'),
  'the corruption cluster now draws indicators from multiple FINTRAC sector pages');

/* ===================== Phase 45 — presentation polish (pre-presentation day) ===================== */
// (P45-T1a) build-rec row stagger is CAPPED — the 119–173-row FINTRAC guidance docs must not blank-wait ~15s.
const env45 = boot(false);                                   // full motion: the delays are real
const api45 = env45.__api;
const big45 = api45.ADVISORIES.filter(api45.isLive).slice().sort((x, y) => y.indicators.length - x.indicators.length)[0];
ok(big45.indicators.length > 30, `largest doc is big enough for the cap to bind (${big45.id}: ${big45.indicators.length} rows)`);
api45.pick(big45.id); api45.gotoScreen(2);
const delays45 = [...env45.__stage._html.matchAll(/animation-delay:(\d+)ms/g)].map(m => +m[1]);
ok(delays45.length >= big45.indicators.length, `every build-rec row carries a stagger delay (${delays45.length})`);
ok(Math.max(...delays45) <= 1500, `stagger capped at 1500ms (max ${Math.max(...delays45)}ms) — last row visible ≤2s, reduced-motion instant`);
// (P45-T1b) the human gate reads PROPOSED, not pre-decided — the agent proposes, the presenter disposes.
ok(/proposed all/.test(env45.__stage._html) && /Deselect any to dispose/.test(env45.__stage._html),
  'human gate copy: agent has PROPOSED all N, deselect to dispose (not pre-decided)');
// (P45-T1c) a zero-build-now doc never dead-ends with impossible advice on the lift screen.
const env45z = boot(true);
const api45z = env45z.__api;
const zero45 = api45z.ADVISORIES.find(a => api45z.isLive(a) &&
  api45z.buildNows(a).filter(i => i.build_logic && typeof i.build_logic === 'object').length === 0);
ok(zero45, `found a zero-build-now doc for the dead-end check (${zero45 && zero45.id})`);
api45z.pick(zero45.id); api45z.gotoScreen(4);
ok(/No immediately-buildable signal/.test(env45z.__stage._html) && !/pick at least one build-now gap/.test(env45z.__stage._html),
  'zero-build-now doc: lift empty state never advises the impossible (no "go back and pick")');
// (P45-T1d) the build-log QUEUES the backtest — no ✓ for a backtest that never ran.
const advQ45 = api45.ADVISORIES.filter(api45.isLive).find(a => api45.buildNows(a).some(i => i.build_logic && typeof i.build_logic === 'object'));
api45.pick(advQ45.id); api45.gotoScreen(3);
ok(/Queue backtest on population/.test(env45.__stage._html),
  'build-log step 4 reads "Queue backtest on population" — a handoff, not a false claim');
ok(env45.__errors.length === 0 && env45z.__errors.length === 0, 'Phase-45 T1 screens rendered with no console errors');

// (P45-T3) FINTRAC licence attribution on the QUOTING lens views — the capability/data-source drills
// reproduce each indicator's verbatim flag text, so the footer must attribute EVERY contributing
// FINTRAC doc (© clause + complete title + source URL — per reproduced work), and stay EMPTY where
// nothing Crown-copyrighted is quoted. The synthesis (Typologies) drill shows titles/counts only
// (no reproduced text) and stays footer-silent.
const env45a = boot(true);
const api45a = env45a.__api;
const capCodes45 = Object.keys(api45a.CAP_BY);
const capWith45 = capCodes45.find(c => api45a.indsForCap(c).some(r => r.a.attribution));
ok(capWith45, `found a FINTRAC-bearing capability for the attribution check (${capWith45})`);
api45a.enterCapability(capWith45);
const attC45 = env45a.document.getElementById('attribution').innerHTML;
const nFC45 = new Set(api45a.indsForCap(capWith45).filter(r => r.a.attribution).map(r => r.a.id)).size;
ok(/His Majesty the King in Right of Canada/.test(attC45), 'capability drill: footer carries the Crown-copyright clause');
eq((attC45.match(/a copy of the version available at/g) || []).length, nFC45,
  `capability drill: attribution lists EVERY contributing FINTRAC doc with its source URL (${nFC45})`);
ok((attC45.match(/“/g) || []).length >= nFC45, 'capability drill: each listed attribution carries the complete document title');
const dsCodes45 = Object.keys(api45a.DS_BY);
const dsWith45 = dsCodes45.find(c => api45a.indsForDS(c).some(r => r.a.attribution));
ok(dsWith45, `found a FINTRAC-bearing data source for the attribution check (${dsWith45})`);
api45a.enterDataSource(dsWith45);
ok(/His Majesty the King in Right of Canada/.test(env45a.document.getElementById('attribution').innerHTML),
  'data-source drill: footer carries the Crown-copyright attribution');
// the EMPTY side: a US-only lens slice (no FINTRAC quote on screen) shows NO attribution — over-attribution
// would misstate the US docs' public-domain basis. Fall back across cap → DS for whichever US-only slice exists.
const usCap45 = capCodes45.find(c => { const rs = api45a.indsForCap(c); return rs.length && rs.every(r => !r.a.attribution); });
const usDS45 = usCap45 ? null : dsCodes45.find(c => { const rs = api45a.indsForDS(c); return rs.length && rs.every(r => !r.a.attribution); });
if (usCap45) {
  api45a.enterCapability(usCap45);
  eq(env45a.document.getElementById('attribution').innerHTML, '', `US-only capability drill (${usCap45}): footer attribution EMPTY`);
} else if (usDS45) {
  api45a.enterDataSource(usDS45);
  eq(env45a.document.getElementById('attribution').innerHTML, '', `US-only data-source drill (${usDS45}): footer attribution EMPTY`);
} else {
  ok(true, 'no US-only lens slice exists in the current corpus (every capability/data source draws ≥1 FINTRAC doc) — empty side covered by synthesis below');
}
// synthesis (titles only, no reproduced text) stays footer-silent
const typ45 = api45a.clusters()[0];
api45a.enterSynthesis(typ45.t);
eq(env45a.document.getElementById('attribution').innerHTML, '', 'synthesis drill (titles/counts only): footer attribution stays EMPTY');
ok(env45a.__errors.length === 0, 'Phase-45 T3 attribution views rendered with no console errors');

// (P45-T4) copy coherence — the story reads as ONE story from landing to close.
const envL45 = boot(true, true);                              // raw=true stays on the landing cover
const landing45 = envL45.__stage._html;
ok(/per-sector ML\/TF indicator guidance/.test(landing45), 'landing names ALL 5 source families (incl. FINTRAC sector guidance)');
ok(/detection <b>atoms<\/b>/.test(landing45), 'landing SEEDS the atom vocabulary — the lift beat lands as a callback, not jargon');
ok(/source families · 3 regulators/.test(landing45), 'landing tile: honest "5 source families · 3 regulators" split');
// FINTRAC invented reference slugs are humanized at display (FinCEN/OFAC real refs pass through)
const envR45 = boot(true);
const apiR45 = envR45.__api;
const ftDoc45 = apiR45.ADVISORIES.find(a => apiR45.isLive(a) && /^FINTRAC-/.test(a.advisory || '') && !/\d/.test(a.advisory || ''));
ok(ftDoc45, `found a FINTRAC doc with an invented ref slug (${ftDoc45 && ftDoc45.advisory})`);
apiR45.pick(ftDoc45.id);
ok(!new RegExp(ftDoc45.advisory).test(envR45.__stage._html) && /FINTRAC( Guidance)? · /.test(envR45.__stage._html),
  'FINTRAC eyebrow wears a humanized source label, never the invented ALL-CAPS slug');
const efeR45 = apiR45.ADVISORIES.find(a => a.id === 'fin-2022-a002');
apiR45.pick(efeR45.id);
ok(/FIN-2022-A002/.test(envR45.__stage._html), 'FinCEN real reference numbers still pass through untouched');
// the close-screen pill speaks the UI vocabulary, not the internal token
apiR45.pick(advQ45.id); apiR45.gotoScreen(5);
ok(/not covered → covered/.test(envR45.__stage._html) && !/>gap → covered</.test(envR45.__stage._html),
  'close-screen pill reads "not covered → covered" (the internal token stays internal)');
// typology cluster labels are human-readable
const envT45 = boot(true);
const apiT45 = envT45.__api;
apiT45.selMode = 'typology'; apiT45.renderSelect();
ok(/Cross-cutting indicators/.test(envT45.__stage._html), 'the cross-cutting cluster label is title-cased + hyphenated');
ok(!/cross cutting indicators/.test(envT45.__stage._html), 'no de-hyphenated lowercase slug remains on the Typologies lens');
ok(envL45.__errors.length === 0 && envR45.__errors.length === 0 && envT45.__errors.length === 0,
  'Phase-45 T4 copy surfaces rendered with no console errors');

// (P45-T5) walkthrough feedback — (a) the landing hooks on an effective, regulatorily defensible
// financial-crime program; (b) NO mojibake / PDF-symbol tofu reaches any rendered surface (the load-time
// display repair fixes the authored coverage fields' broken encoding + the article bullets; committed
// records/md stay byte-frozen).
ok(/regulatorily defensible/.test(boot(true, true).__stage._html),
  'landing hooks on the effective + regulatorily defensible financial-crime program');
const MOJI45 = /\u00e2[\u0080-\u009f\u0086]|\u00c2[\u00b7\u00a7\u00a0\u00ae]|[\uf000-\uf0ff]|\ufeff/;
const envM45 = boot(true);
const apiM45 = envM45.__api;
// FULL-CONTENT sweep: EVERY live doc × all six screens renders mojibake/tofu-free (the fincen-alerts
// records carried Â·/â-mojibake in their authored coverage fields — repaired at load, records byte-frozen).
let clean45 = true; const dirty45 = [];
const live45 = apiM45.ADVISORIES.filter(apiM45.isLive);
for (const d of live45) {
  apiM45.pick(d.id);
  for (let sN = 0; sN <= 5; sN++) {
    apiM45.gotoScreen(sN);
    if (MOJI45.test(envM45.__stage._html)) { clean45 = false; dirty45.push(`${d.id}#${sN}`); }
  }
}
ok(clean45, `ALL ${live45.length} live docs × 6 screens render mojibake/tofu-free${dirty45.length ? ' — DIRTY: ' + dirty45.slice(0, 5).join(', ') : ''}`);
// and every lens drill surface
let cleanLens45 = true;
for (const c of Object.keys(apiM45.CAP_BY)) { if (apiM45.indsForCap(c).length) { apiM45.enterCapability(c); if (MOJI45.test(envM45.__stage._html)) cleanLens45 = false; } }
for (const c of Object.keys(apiM45.DS_BY)) { if (apiM45.indsForDS(c).length) { apiM45.enterDataSource(c); if (MOJI45.test(envM45.__stage._html)) cleanLens45 = false; } }
for (const cl of apiM45.clusters()) { apiM45.enterSynthesis(cl.t); if (MOJI45.test(envM45.__stage._html)) cleanLens45 = false; }
ok(cleanLens45, 'ALL capability / data-source / typology drill surfaces render mojibake/tofu-free');
const puaDoc45 = apiM45.ADVISORIES.find(a => a.id === 'fintrac-cannabis');     // article md carries PDF symbol-font bullets
ok(puaDoc45 && apiM45.isLive(puaDoc45), 'the PDF-bullet FINTRAC doc is live for the cleanliness walk');
apiM45.pick(puaDoc45.id);
ok(!/[\uf000-\uf0ff]/.test(envM45.__stage._html) && /\u2022/.test(envM45.__stage._html),
  'fintrac-cannabis: PDF symbol-font bullets render as • (no tofu boxes in the article)');
ok(envM45.__errors.length === 0, 'Phase-45 T5 cleanliness walks rendered with no console errors');

/* ============================ report ============================ */
console.log(`\n${pass} passed, ${fails.length} failed`);
if (fails.length) { console.log('FAILURES:\n  - ' + fails.join('\n  - ')); process.exit(1); }
console.log('OK — corpus-explorer arc invariants hold against the committed dist.');
