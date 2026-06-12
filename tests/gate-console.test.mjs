#!/usr/bin/env node
// Gate-console arc regression harness — ZERO runtime deps (Node built-in `vm` + the corpus-explorer
// hand-rolled DOM shim pattern; no third-party DOM library, no npm install).
// Run: `node tests/gate-console.test.mjs`.
//
// What it does: loads console.html (the TEMPLATE — the 4th single-file offline artifact), injects a
// controlled STUB dataset at the single injection placeholder (so the harness owns the XSS strings and
// the FINTRAC-vs-US attribution split), evaluates the inline script under the shim, then drives the
// 5-screen arc (Queue → Evidence → Disposition → Reveal → Ledger) and asserts the Phase-47 invariants:
//   - honest queue counts over the stub cases;
//   - Evidence shows the verbatim grounded flag AND the red_flag translation AND BOTH assessments
//     NEUTRALLY (no "correction" string anywhere pre-disposition — neutrality is load-bearing);
//   - the non-binary graded gate: recording is BLOCKED without grade + rationale (the Class-J
//     rationale-required obligation), records with both;
//   - the Reveal (the historical record) appears ONLY post-disposition, framed as precedent, not a score;
//   - the Ledger accumulates session dispositions; export textarea carries valid JSON; honest empty
//     state; session-only honesty copy;
//   - the always-on badge node; the FINTRAC Crown-copyright footer attribution for a FINTRAC case and
//     an EMPTY footer for a US public-domain case (the Phase-28 relocated-footer rule);
//   - XSS: case fields containing <script> / & render escaped (esc() is the sole escaper);
//   - ←/→/Space/Esc presenter navigation (guarded inside INPUT/TEXTAREA); the reduced-motion branch.

import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';
import vm from 'node:vm';

const HERE = dirname(fileURLToPath(import.meta.url));
const TEMPLATE = resolve(HERE, '..', 'console.html');
const PLACEHOLDER = '__CONSOLE__';

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
// mirror console.html's esc() so we can assert escaped text appears in the rendered stage
function escH(s){return String(s==null?'':s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;').replace(/'/g,'&#39;');}
// undo esc() on extracted textarea content (entity order matters: &amp; LAST)
function unesc(s){return s.replace(/&#39;/g,"'").replace(/&quot;/g,'"').replace(/&lt;/g,'<').replace(/&gt;/g,'>').replace(/&amp;/g,'&');}

/* ---------- the stub dataset (the harness owns the edge cases) ---------- */
const STUB = {
  brand: { title: 'Signal Watch', subtitle: 'Gate Console · Vision Prototype' },
  badge: 'Illustrative data & outputs',
  cases: [
    { // FINTRAC case (Crown-copyright attribution) — changed axis D
      id: 'fintrac-guid-accountants/IND-08', doc_id: 'fintrac-guid-accountants', indicator_id: 'IND-08',
      source_dir: 'data/fintrac-guidance',
      flag: 'Client alters the transaction after being asked for identity documents & refuses to proceed.',
      red_flag: 'Transaction altered when ID requested',
      rater_a: { capability: 'C4', capability_name: 'Structuring / sub-threshold & reporting-trigger evasion',
                 data_source: 'D8', data_source_name: 'KYC / CDD & beneficial-ownership data' },
      rater_b: { capability: 'C4', capability_name: 'Structuring / sub-threshold & reporting-trigger evasion',
                 data_source: 'D1', data_source_name: 'Core transaction monitoring (deposit/account ledger)' },
      changed: 'D',
      attribution: { title: 'Money laundering and terrorist financing indicators – Accountants',
                     url: 'https://fintrac-canafe.canada.ca/guidance-directives/transaction-operation/indicators-indicateurs/accts_mltf-eng' } },
    { // US public-domain case (NO attribution — footer must stay empty) — changed axis C
      id: 'fin-2019-a006/IND-13', doc_id: 'fin-2019-a006', indicator_id: 'IND-13',
      source_dir: 'data/fincen',
      flag: 'The source of funds cannot be corroborated.',
      red_flag: 'Unverifiable source of funds',
      rater_a: { capability: 'C8', capability_name: 'Income / occupation-vs-activity profile-inconsistency detection',
                 data_source: 'D8', data_source_name: 'KYC / CDD & beneficial-ownership data' },
      rater_b: { capability: 'C14', capability_name: 'KYC integrity & customer-cooperation screening',
                 data_source: 'D8', data_source_name: 'KYC / CDD & beneficial-ownership data' },
      changed: 'C',
      attribution: null },
    { // XSS probe case — hostile strings in the data fields; esc() must neutralize — changed axis both
      id: 'fintrac-guid-casinos/IND-02', doc_id: 'fintrac-guid-casinos', indicator_id: 'IND-02',
      source_dir: 'data/fintrac-guidance',
      flag: 'Chips bought & cashed with minimal play <b>at multiple casinos</b>.',
      red_flag: '<script>alert(1)</script> minimal-play chip cashing',
      rater_a: { capability: 'C4', capability_name: 'Structuring / sub-threshold & reporting-trigger evasion',
                 data_source: 'D1', data_source_name: 'Core transaction monitoring (deposit/account ledger)' },
      rater_b: { capability: 'C8', capability_name: 'Income / occupation-vs-activity profile-inconsistency detection',
                 data_source: 'D8', data_source_name: 'KYC / CDD & beneficial-ownership data' },
      changed: 'both',
      attribution: { title: 'ML/TF indicators – Casinos <test&title>',
                     url: 'https://fintrac-canafe.canada.ca/guidance-directives/transaction-operation/indicators-indicateurs/casinos_mltf-eng' } },
  ],
  taxonomy: {
    capabilities: [
      { id: 'C4', name: 'Structuring / sub-threshold & reporting-trigger evasion', group: 'Transaction patterns', posture: 'y' },
      { id: 'C8', name: 'Income / occupation-vs-activity profile-inconsistency detection', group: 'Entity, KYC & screening', posture: 'partial' },
      { id: 'C14', name: 'KYC integrity & customer-cooperation screening', group: 'Entity, KYC & screening', posture: 'partial' },
    ],
    data_sources: [
      { id: 'D1', name: 'Core transaction monitoring (deposit/account ledger)', posture: 'y' },
      { id: 'D8', name: 'KYC / CDD & beneficial-ownership data', posture: 'y' },
    ],
  },
  docs: {
    'fintrac-guid-accountants': { title: 'Money laundering and terrorist financing indicators – Accountants', doc_type: 'FINTRAC Guidance', jurisdiction: 'Canada' },
    'fin-2019-a006': { title: 'Advisory on the FATF-Identified Jurisdictions', doc_type: 'Advisory', jurisdiction: 'US' },
    'fintrac-guid-casinos': { title: 'ML/TF indicators – Casinos <test&title>', doc_type: 'FINTRAC Guidance', jurisdiction: 'Canada' },
  },
};

/* ---------- load the template + inject the stub ---------- */
const rawHtml = readFileSync(TEMPLATE, 'utf8');
ok(rawHtml.split(PLACEHOLDER).length === 2, 'console.html carries exactly ONE injection placeholder');
ok(/id="badge"/.test(rawHtml) && /Illustrative data/.test(rawHtml), 'the always-on "Illustrative data & outputs" badge node is present in the chrome');
ok(/id="attribution"/.test(rawHtml), 'the page-footer attribution node is present (Phase-28 relocated-footer mechanism)');
ok(/prefers-reduced-motion/.test(rawHtml), 'the reduced-motion CSS branch exists');
ok(!/fetch\(/.test(rawHtml) && !/<script src/.test(rawHtml) && !/type="module"/.test(rawHtml),
  'template is self-contained (no fetch / external script / ES module)');

const html = rawHtml.replace(PLACEHOLDER, JSON.stringify(STUB));
const open = html.indexOf('<script>');
const close = html.lastIndexOf('</script>');
if (open < 0 || close < 0) { console.error('FATAL: no <script> in', TEMPLATE); process.exit(2); }
const SCRIPT = html.slice(open + '<script>'.length, close);

/* ---------- a minimal DOM/window shim (the corpus-explorer pattern) ---------- */
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
  return {
    dataset, textContent: '', onclick: null,
    classList: {
      add: c => set.add(c), remove: c => set.delete(c), contains: c => set.has(c),
      toggle: (c, f) => { const on = f === undefined ? !set.has(c) : f; on ? set.add(c) : set.delete(c); return on; },
    },
    setAttribute() {}, getAttribute() { return null; },
    querySelector() { return { textContent: '' }; },
  };
}

function makeEnv(reduced) {
  let now = 0;
  const timers = [];
  const errors = [];
  const listeners = {};
  let dynCache = {};

  function dynEl() {
    const set = new Set();
    return { _html: '', style: {}, textContent: '', value: '', scrollTop: 0, scrollHeight: 0,
      onclick: null, oninput: null,
      get innerHTML() { return this._html; }, set innerHTML(v) { this._html = String(v); },
      insertAdjacentHTML(_pos, h) { this._html += String(h); },
      select() {}, focus() {},
      classList: { add: (...c) => c.forEach(x => set.add(x)), remove: (...c) => c.forEach(x => set.delete(x)), contains: c => set.has(c) } };
  }
  function chromeEl(id) {
    const lastQS = {};
    return {
      id, _html: '', style: {}, textContent: '', onclick: null,
      get innerHTML() { return this._html; },
      set innerHTML(v) { this._html = String(v); if (id === 'stage') dynCache = {}; },
      querySelectorAll(sel) { const r = queryAll(this._html, sel); lastQS[sel] = r; return r; },
      querySelector(sel) { return queryAll(this._html, sel)[0] || null; },
      _qs(sel) { return lastQS[sel] || []; },
    };
  }

  const stage = chromeEl('stage'), stepper = chromeEl('stepper');
  const chrome = { stage, stepper, next: chromeEl('next'), back: chromeEl('back'),
    reset: chromeEl('reset'), hint: chromeEl('hint'), attribution: chromeEl('attribution') };

  const document = {
    getElementById(id) {
      if (chrome[id]) return chrome[id];
      if (dynCache[id]) return dynCache[id];
      if (new RegExp(`id="${id}"`).test(stage._html)) { return (dynCache[id] = dynEl()); }
      return dynEl();
    },
    addEventListener(type, fn) { listeners[type] = fn; },
    querySelectorAll(sel) { return queryAll(stage._html, sel); },
    execCommand() { return true; },
  };
  const window = {
    matchMedia: q => ({ matches: reduced, media: q, addListener() {}, removeListener() {}, addEventListener() {}, removeEventListener() {} }),
    scrollTo() {},
  };
  const env = {
    document, window,
    console: { error: (...a) => errors.push(a.join(' ')), log() {}, warn() {} },
    performance: { now: () => now },
    requestAnimationFrame: cb => { now += 1e6; cb(now); return 0; },
    cancelAnimationFrame() {},
    setTimeout: (fn) => { timers.push(fn); return timers.length; },
    clearTimeout() {},
    __capture: api => { env.__api = api; },
    __errors: errors,
    __stage: stage,
    __attr: chrome.attribution,
    __key: (key, tag = 'DIV') => { const fn = listeners.keydown; if (!fn) return;
      fn({ key, target: { tagName: tag }, preventDefault() {}, metaKey: false, ctrlKey: false, altKey: false }); },
  };
  return env;
}

const EPILOGUE = `;__capture({CASES,GRADES,REDUCED,
  pickCase,pickGrade,setRationale,recordDisposition,advance,back,gotoScreen,toQueue,toLedger,render,
  get view(){return view}, get screen(){return screen},
  get dispositions(){return dispositions}, get draft(){return draft}, get blocked(){return blocked}});`;
function boot(reduced) {
  const env = makeEnv(reduced);
  vm.createContext(env);
  vm.runInContext(SCRIPT + EPILOGUE, env, { filename: 'gate-console-inline.js' });
  return env;
}

/* ============================ drive the arc ============================ */
console.log('gate-console arc harness  (source: console.html + stub dataset)\n');

const env = boot(true);
const api = env.__api;
ok(api && typeof api.pickCase === 'function', 'script booted; internals re-exported');

// ---- (1) Queue: the adjudication queue with honest counts ----
eq(api.view, 'queue', 'boots into the Queue (the adjudication queue is the entry)');
ok((env.__stage._html.match(/class="step /g) || []).length === 5, 'stepper renders the 5 arc steps');
const rows = (env.__stage._html.match(/class="caserow"/g) || []).length;
eq(rows, STUB.cases.length, 'queue lists every case as a row');
ok(env.__stage._html.includes(`>${STUB.cases.length}<`), 'queue shows the honest total case count');
ok(/Capability differs/.test(env.__stage._html) && /Data source differs/.test(env.__stage._html)
  && /Both differ/.test(env.__stage._html), 'queue groups by the changed axis (C / D / both)');
ok(env.__stage._html.includes(escH(STUB.cases[1].red_flag)), 'queue rows show the case red_flag (escaped)');
ok(!/correction/i.test(env.__stage._html), 'NEUTRALITY: no "correction" string on the queue');
ok(env.__errors.length === 0, 'queue rendered with no console errors');

// ---- (2) Evidence: show-both + the two assessments, neutrally ----
const c0 = STUB.cases[0];
api.pickCase(c0.id);
eq(api.view, 'case', 'picking a case enters the case arc');
eq(api.screen, 0, 'case arc starts on Evidence');
ok(env.__stage._html.includes(escH(c0.flag)), 'Evidence shows the verbatim grounded flag (escaped — & survives as &amp;)');
ok(env.__stage._html.includes(escH(c0.red_flag)), 'Evidence shows the red_flag translation beside it');
ok(/Assessment A/.test(env.__stage._html) && /Assessment B/.test(env.__stage._html),
  'both competing assignments are presented as Assessment A / Assessment B');
ok(env.__stage._html.includes(escH(c0.rater_a.data_source_name)) && env.__stage._html.includes(escH(c0.rater_b.data_source_name)),
  'both raters’ taxonomy names render');
ok(env.__stage._html.includes(escH('Transaction patterns')), 'capability taxonomy GROUP renders (from the inlined taxonomy)');
ok(!/correction/i.test(env.__stage._html) && !/pre-adjudication/i.test(env.__stage._html) && !/upheld/i.test(env.__stage._html),
  'NEUTRALITY: Evidence never labels which assessment is the historical correction');
ok(/© His Majesty/.test(env.__attr._html) && env.__attr._html.includes(escH(c0.attribution.title))
  && env.__attr._html.includes(escH(c0.attribution.url)),
  'footer carries the FINTRAC Crown-copyright attribution (© clause + complete title + URL) for a FINTRAC case');
ok(env.__errors.length === 0, 'Evidence rendered with no console errors');

// ---- (3) Disposition: the non-binary graded gate, rationale-REQUIRED ----
api.advance();
eq(api.screen, 1, 'advance → Disposition');
eq((env.__stage._html.match(/class="gradebtn/g) || []).length, 4, 'FOUR grades offered (uphold A / uphold B / both defensible / escalate)');
ok(/id="rationale"/.test(env.__stage._html), 'free-text rationale field present');
ok(!/correction/i.test(env.__stage._html), 'NEUTRALITY: no "correction" string on Disposition');
api.recordDisposition();
eq(api.screen, 1, 'recording with NEITHER grade nor rationale is blocked (stays on Disposition)');
eq(api.dispositions.length, 0, 'nothing recorded while blocked');
ok(/id="blockmsg"/.test(env.__stage._html), 'an honest blocked message renders');
api.setRationale('Rationale without a grade.');
api.recordDisposition();
ok(api.screen === 1 && api.dispositions.length === 0, 'rationale alone is still blocked (grade required)');
api.setRationale('');
api.pickGrade('uphold_b');
api.recordDisposition();
ok(api.screen === 1 && api.dispositions.length === 0, 'grade alone is still blocked (rationale required — the Class-J obligation)');
const RAT = 'D1 is right: the alteration is observable in the transaction ledger, not in the KYC file. <&test>';
api.setRationale(RAT);
api.recordDisposition();
eq(api.dispositions.length, 1, 'grade + rationale → the disposition records');
ok(api.dispositions[0].grade === 'uphold_b' && api.dispositions[0].rationale === RAT
  && api.dispositions[0].case_id === c0.id, 'the recorded disposition carries case + grade + rationale');

// ---- (4) Reveal: ONLY post-disposition; precedent, never a score ----
eq(api.screen, 2, 'recording advances to the Reveal');
ok(/pre-adjudication/.test(env.__stage._html) && /upheld/.test(env.__stage._html),
  'Reveal now discloses the historical record (A = pre-adjudication, B = the recorded adjudication)');
ok(env.__stage._html.includes(escH(RAT)), 'Reveal shows the presenter’s own rationale (escaped)');
ok(/Uphold B/.test(env.__stage._html), 'Reveal shows the presenter’s own grade beside the history');
ok(/not a score/i.test(env.__stage._html), 'Reveal copy frames the comparison as precedent, NOT a score');
ok(/© His Majesty/.test(env.__attr._html), 'FINTRAC footer attribution persists across the case screens');

// the guard: a FRESH (unrecorded) case can never reach the Reveal directly
api.pickCase(STUB.cases[1].id);
api.gotoScreen(2);
ok(api.screen !== 2, 'Reveal is unreachable pre-disposition (gotoScreen(2) on an unrecorded case is refused)');
eq(env.__attr._html, '', 'footer attribution is EMPTY for a US public-domain case');

// ---- (5) Ledger: session accumulation + JSON export + honesty ----
api.toQueue();
ok(/recorded/i.test(env.__stage._html), 'queue marks the already-disposed case');
api.pickCase(STUB.cases[2].id);                       // the XSS probe case
ok(!/<script>alert/.test(env.__stage._html) && env.__stage._html.includes('&lt;script&gt;'),
  'XSS: a red_flag containing <script> renders escaped, never as markup');
ok(env.__stage._html.includes(escH(STUB.cases[2].flag)), 'XSS: a flag containing & + <b> renders escaped');
ok(!/<script>alert/.test(env.__attr._html) && !/<test&title>/.test(env.__attr._html),
  'XSS: the attribution title renders escaped in the footer');
api.advance();
api.pickGrade('escalate');
api.setRationale('Neither assignment holds; the indicator is behavioural, not transactional.');
api.recordDisposition();
api.advance();
eq(api.view, 'ledger', 'advance from the Reveal reaches the session Ledger');
eq((env.__stage._html.match(/class="ledrow"/g) || []).length, 2, 'ledger accumulates both session dispositions');
ok(/Escalate/.test(env.__stage._html) && /Uphold B/.test(env.__stage._html), 'ledger rows carry the grades');
const expM = /<textarea id="export"[^>]*>([\s\S]*?)<\/textarea>/.exec(env.__stage._html);
ok(!!expM, 'export textarea present');
let exported = null;
try { exported = JSON.parse(unesc(expM ? expM[1] : '')); } catch { /* fails the next assert */ }
ok(exported && Array.isArray(exported.dispositions) && exported.dispositions.length === 2,
  'export textarea contains VALID JSON with both dispositions');
ok(exported && exported.dispositions[0].rationale === RAT && exported.dispositions[0].order === 1
  && exported.dispositions[1].order === 2, 'exported dispositions keep the order index + raw rationale');
ok(/session/i.test(env.__stage._html) && /persists nothing/i.test(env.__stage._html),
  'ledger states honestly that the offline file persists nothing (session-only)');
ok(env.__errors.length === 0, 'full arc drove with no console errors');

// ---- (6) honest EMPTY ledger state (fresh context) ----
const envE = boot(true);
envE.__api.toLedger();
ok(/No dispositions/i.test(envE.__stage._html), 'empty ledger shows an honest empty state');

// ---- (7) keyboard navigation (←/→/Space/Esc) + input guard ----
const envK = boot(true);
const apiK = envK.__api;
envK.__key('ArrowRight');
eq(apiK.view, 'queue', 'ArrowRight on the queue stays put (cases are picked, not paged)');
apiK.pickCase(STUB.cases[0].id);
envK.__key('ArrowRight');
eq(apiK.screen, 1, '→ advances Evidence → Disposition');
envK.__key('ArrowLeft');
eq(apiK.screen, 0, '← returns Disposition → Evidence');
envK.__key(' ');
eq(apiK.screen, 1, 'Space advances');
envK.__key('ArrowRight', 'TEXTAREA');
eq(apiK.screen, 1, 'arrow keys inside the rationale TEXTAREA never navigate');
envK.__key('ArrowRight');
eq(apiK.screen, 1, '→ on an unrecorded Disposition does NOT skip the gate (blocked, not advanced)');
eq(apiK.dispositions.length, 0, 'keyboard advance records nothing without grade + rationale');
envK.__key('Escape');
eq(apiK.view, 'queue', 'Esc returns to the queue');

// ---- (8) queue row click wiring + reduced-motion branch ----
const envC = boot(false);
const apiC = envC.__api;
eq(apiC.REDUCED, false, 'full-motion context: REDUCED is false');
const row = envC.__stage._qs('.caserow')[0];
ok(row && typeof row.onclick === 'function', 'queue case rows are click-wired');
row.onclick();
eq(apiC.view, 'case', 'clicking a queue row opens the case');
const envR = boot(true);
eq(envR.__api.REDUCED, true, 'prefers-reduced-motion context: REDUCED branch engages');

/* ---------- verdict ---------- */
console.log(`\n${pass} passed, ${fails.length} failed`);
if (fails.length) { console.log('FAILED:'); fails.forEach(f => console.log('  - ' + f)); process.exit(1); }
