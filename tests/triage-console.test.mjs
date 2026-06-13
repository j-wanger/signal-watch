#!/usr/bin/env node
// Triage-console arc regression harness — ZERO runtime deps (the gate-console / corpus-explorer
// hand-rolled DOM shim pattern; no third-party DOM library, no npm install).
// Run: `node tests/triage-console.test.mjs`.
//
// What it does: loads triage.html (the TEMPLATE — the 5th single-file offline artifact), injects a
// controlled STUB dataset at the single injection placeholder (so the harness owns the XSS strings,
// the divergent-disposition pair, and the seeded second-rater fixtures), evaluates the inline script
// under the shim, then drives the 5-screen arc (Queue → Evidence → Disposition → Reveal → Discovery
// ledger) and asserts the Phase-49 invariants:
//   - queue grouped by the 4 §14 strata with honest counts; controls are NOT revealed pre-reveal;
//   - Evidence shows the panel fact pattern + the fired-rule card (or the honest below-the-line /
//     novel / baseline-population cards); novel indicators carry the verbatim flag + translation +
//     the US-federal public-domain licence line;
//   - the §14 graded disposition gate: rationale REQUIRED for every option (empty records NOTHING);
//     need-more-info ADDITIONALLY requires a C/D taxonomy pick; the policy-gap escape records like
//     any grade (rationale required);
//   - the Reveal is LOCKED pre-disposition; history scenarios frame the institution's decision as
//     "decisions, not correctness" (never ground truth); the shared-panel divergent pair surfaces the
//     PROCESS INCONSISTENCY; seeded second raters replay LABELED as synthetic;
//   - the Discovery ledger DERIVES its outputs (signal gaps from fired-rule state, data gaps per
//     D-code, policy gaps, agreement arithmetic with a rendered measurement definition — never a
//     typed-in figure); JSON export; honest empty state; persists nothing;
//   - the always-on badge; XSS-escape (esc() is the sole escaper); ←/→/Space/Esc presenter keys
//     guarded inside TEXTAREA; the reduced-motion branch.

import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';
import vm from 'node:vm';

const HERE = dirname(fileURLToPath(import.meta.url));
const TEMPLATE = resolve(HERE, '..', 'triage.html');
const PLACEHOLDER = '__TRIAGE__';

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
function escH(s){return String(s==null?'':s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;').replace(/'/g,'&#39;');}
function unesc(s){return s.replace(/&#39;/g,"'").replace(/&quot;/g,'"').replace(/&lt;/g,'<').replace(/&gt;/g,'>').replace(/&amp;/g,'&');}

/* ---------- the stub dataset (the harness owns the edge cases) ---------- */
const STUB = {
  brand: { title: 'Signal Watch', subtitle: 'Triage Console · Vision Prototype' },
  badge: 'Illustrative data & outputs',
  taxonomy: {
    capabilities: [
      { id: 'C4', name: 'Structuring / sub-threshold & reporting-trigger evasion', group: 'Transaction patterns', posture: 'y' },
      { id: 'C24', name: 'Trade-document & goods-flow screening', group: 'Trade', posture: 'n' },
    ],
    data_sources: [
      { id: 'D1', name: 'Core transaction monitoring (deposit/account ledger)', posture: 'y' },
      { id: 'D8', name: 'KYC / CDD & beneficial-ownership data', posture: 'y' },
      { id: 'D15', name: 'Trade documents & shipping data', posture: 'n' },
    ],
  },
  triage: {
    meta: {
      synthetic: true,
      note: 'SYNTHETIC stub for the harness.',
      strata: ['history-signal-fired', 'history-below-the-line', 'synthetic-novel', 'random-population'],
      disposition_grammar: ['confirm-risk', 'confirm-no-risk', 'both-defensible', 'escalate', 'need-more-info', 'no-defensible-option'],
      history_dispositions: ['dismissed', 'escalated', 'sar_filed', 'data_requested'],
      design_params: { note: 'chosen, not measured — stub design parameters', scenario_count: 5, controls: 1, double_assigned: 2 },
    },
    rules: {
      'TM-104': {
        title: 'Unexplained high-risk geography wires',
        logic: 'any wire ≥ $10,000 to or from a high-risk jurisdiction with no documented connection',
        indicator: 'A customer sends or receives international wires involving high-risk jurisdictions with no documented purpose.',
        signal: { red_flag: 'High-risk-geography wire without documented purpose', capability: 'C4', data_source: 'D1', status: 'covered', build_rec: 'COVERED' },
      },
      'TM-101': {
        title: 'Structuring below the reporting threshold',
        logic: 'three or more cash deposits each between $8,000 and $9,999 within 7 days',
        indicator: 'Multiple cash deposits just below the reporting threshold in a short period.',
        signal: { red_flag: 'Sub-threshold cash deposit pattern', capability: 'C4', data_source: 'D1', status: 'covered', build_rec: 'COVERED' },
      },
    },
    panels: {
      'P-PAIR': {
        skeleton: 'TM-104 logic',
        customer: 'Personal account, 6-year tenure. SYNTHETIC. <b>bold-probe</b>',
        activity: ['Outbound wire $14,200 to a high-risk jurisdiction.', 'No documented connection & no prior corridor history.'],
        kyc_note: 'KYC current; occupation: logistics coordinator.',
      },
      'P-BT': {
        skeleton: 'below TM-101 thresholds',
        customer: 'Personal account, 5-year tenure. SYNTHETIC.',
        activity: ['Cash deposits $7,400 / $7,900 / $7,650 across six days — each below the $8,000 floor.'],
        kyc_note: 'Declared low cash volume at onboarding.',
      },
      'P-NV': {
        skeleton: 'novel: stub-doc/IND-09',
        customer: 'Business account — electronics wholesaler. SYNTHETIC.',
        activity: ['Wires to component brokers in two transshipment hubs.'],
        kyc_note: 'No trade history before incorporation.',
      },
      'P-CT': {
        skeleton: 'control: benign retiree',
        customer: 'Personal account, 31-year tenure. SYNTHETIC.',
        activity: ['Monthly pension credits; no cash activity in 5 years.'],
        kyc_note: 'Nothing out of pattern.',
      },
    },
    scenarios: [
      { id: 'S-A', stratum: 'history-signal-fired', panel: 'P-PAIR', fired_rule: 'TM-104', below_rule: null,
        history: { alert_id: 'A-1', disposition: 'dismissed', analyst: 'a1', date: '2023-02-02', entity_id: 'E-1' },
        prior_alerts: 0,
        second_rater: { rater: 'r2', label: 'synthetic second rater (seeded)', disposition: 'escalate',
          rationale: 'No documented connection; unexplained purpose outweighs the in-pattern remainder.' },
        control: null, novel_source: null },
      { id: 'S-B', stratum: 'history-signal-fired', panel: 'P-PAIR', fired_rule: 'TM-104', below_rule: null,
        history: { alert_id: 'A-2', disposition: 'escalated', analyst: 'a2', date: '2023-03-07', entity_id: 'E-2' },
        prior_alerts: 0,
        second_rater: { rater: 'r2', label: 'synthetic second rater (seeded)', disposition: 'escalate',
          rationale: 'Same fact pattern as the dismissed sibling alert.' },
        control: null, novel_source: null },
      { id: 'S-C', stratum: 'history-below-the-line', panel: 'P-BT', fired_rule: null, below_rule: 'TM-101',
        history: null, prior_alerts: 0, second_rater: null, control: null, novel_source: null },
      { id: 'S-D', stratum: 'synthetic-novel', panel: 'P-NV', fired_rule: null, below_rule: null,
        history: null, prior_alerts: 0, second_rater: null, control: null,
        novel_source: { doc_id: 'stub-doc', indicator_id: 'IND-09', source_dir: 'data/fincen',
          flag: 'Importer with no trade history receiving controlled goods <script>alert(1)</script>.',
          red_flag: 'New importer & controlled-goods exposure', capability: 'C24', data_source: 'D15',
          licence: 'US federal — public domain (17 U.S.C. §105)' } },
      { id: 'S-E', stratum: 'random-population', panel: 'P-CT', fired_rule: null, below_rule: null,
        history: null, prior_alerts: 0, second_rater: null,
        control: { known_disposition: 'confirm-no-risk', basis: 'Long-tenure retiree, fully in pattern — seeded clear-benign control.' },
        novel_source: null },
    ],
  },
};

/* ---------- load the template + inject the stub ---------- */
const rawHtml = readFileSync(TEMPLATE, 'utf8');
ok(rawHtml.split(PLACEHOLDER).length === 2, 'triage.html carries exactly ONE injection placeholder');
ok(/id="badge"/.test(rawHtml) && /Illustrative data/.test(rawHtml), 'the always-on "Illustrative data & outputs" badge node is present in the chrome');
ok(/prefers-reduced-motion/.test(rawHtml), 'the reduced-motion CSS branch exists');
ok(!/fetch\(/.test(rawHtml) && !/<script src/.test(rawHtml) && !/type="module"/.test(rawHtml),
  'template is self-contained (no fetch / external script / ES module)');
ok(/decisions, not correctness/.test(rawHtml), 'the template carries the literal "decisions, not correctness" honesty copy');
ok(/chosen, not measured/.test(rawHtml), 'the template carries the literal "chosen, not measured" honesty copy');
ok(!/\b(accuracy|precision|recall)\b/i.test(rawHtml), 'the template never claims accuracy/precision/recall');
ok(!/localStorage|sessionStorage|document\.cookie/.test(rawHtml), 'the template persists nothing (no storage APIs)');

const html = rawHtml.replace(PLACEHOLDER, JSON.stringify(STUB));
const open = html.indexOf('<script>');
const close = html.lastIndexOf('</script>');
if (open < 0 || close < 0) { console.error('FATAL: no <script> in', TEMPLATE); process.exit(2); }
const SCRIPT = html.slice(open + '<script>'.length, close);

/* ---------- a minimal DOM/window shim (the gate-console pattern) ---------- */
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
      onclick: null, oninput: null, onchange: null,
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

  const stage = chromeEl('stage');
  const chrome = { stage, next: chromeEl('next'), back: chromeEl('back'),
    reset: chromeEl('reset'), hint: chromeEl('hint') };

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
    __key: (key, tag = 'DIV') => { const fn = listeners.keydown; if (!fn) return;
      fn({ key, target: { tagName: tag }, preventDefault() {}, metaKey: false, ctrlKey: false, altKey: false }); },
  };
  return env;
}

const EPILOGUE = `;__capture({SCN,GRADES,REDUCED,
  pickScenario,pickGrade,setRationale,setInfo,recordDisposition,advance,back,gotoScreen,toQueue,toLedger,render,
  get view(){return view}, get screen(){return screen},
  get records(){return records}, get draft(){return draft}, get blocked(){return blocked}});`;
function boot(reduced) {
  const env = makeEnv(reduced);
  vm.createContext(env);
  vm.runInContext(SCRIPT + EPILOGUE, env, { filename: 'triage-console-inline.js' });
  return env;
}

/* ============================ drive the arc ============================ */
console.log('triage-console arc harness  (source: triage.html + stub dataset)\n');

const env = boot(true);
const api = env.__api;
ok(api && typeof api.pickScenario === 'function', 'script booted; internals re-exported');

// ---- (1) Queue: the stratified mini-triage queue ----
eq(api.view, 'queue', 'boots into the Queue');
ok((env.__stage._html.match(/class="step /g) || []).length === 5, 'stepper renders the 5 arc steps');
const rows = (env.__stage._html.match(/class="scnrow"/g) || []).length;
eq(rows, STUB.triage.scenarios.length, 'queue lists every scenario as a row');
ok(/history-sourced — signal fired/i.test(env.__stage._html) || /signal fired/i.test(env.__stage._html),
  'queue carries the history-signal-fired stratum group');
ok(/below the line/i.test(env.__stage._html), 'queue carries the below-the-line stratum group');
ok(/novel/i.test(env.__stage._html), 'queue carries the synthetic-novel stratum group');
ok(/population/i.test(env.__stage._html), 'queue carries the random-population stratum group');
ok(!/seeded clear-benign control/.test(env.__stage._html), 'controls are NOT revealed on the queue (the control basis stays hidden pre-reveal)');
ok(/double-assigned/i.test(env.__stage._html), 'double-assigned scenarios carry the sampled-assignment marker');
ok(env.__errors.length === 0, 'queue rendered with no console errors');

// ---- (2) Evidence: the fact-pattern panel + the per-stratum card ----
api.pickScenario('S-A');
eq(api.view, 'case', 'picking a scenario enters the case arc');
eq(api.screen, 0, 'case arc starts on Evidence');
ok(env.__stage._html.includes(escH(STUB.triage.panels['P-PAIR'].customer)), 'Evidence shows the panel customer line (escaped — the <b> probe survives as text)');
ok(env.__stage._html.includes(escH(STUB.triage.panels['P-PAIR'].activity[1])), 'Evidence shows the activity bullets (escaped — & survives as &amp;)');
ok(env.__stage._html.includes(escH(STUB.triage.rules['TM-104'].logic)), 'Evidence shows the fired rule logic verbatim');
ok(env.__stage._html.includes(escH(STUB.triage.rules['TM-104'].signal.red_flag)), 'Evidence shows the derived signal red_flag beside the rule');
ok(!/dismissed/.test(env.__stage._html), 'NEUTRALITY: the historical disposition never leaks on Evidence');
ok(env.__errors.length === 0, 'Evidence rendered with no console errors');

// ---- (3) Disposition: the §14 graded gate, rationale-REQUIRED ----
api.advance();
eq(api.screen, 1, 'advance → Disposition');
eq((env.__stage._html.match(/class="gradebtn/g) || []).length, 6, 'SIX grammar options offered (incl. need-more-info + the policy-gap escape)');
ok(/flag for policy review/i.test(env.__stage._html), 'the policy-gap escape is worded as no-defensible-option → policy review');
api.recordDisposition();
eq(api.screen, 1, 'recording with NEITHER grade nor rationale is blocked');
eq(api.records.length, 0, 'nothing recorded while blocked');
ok(/id="blockmsg"/.test(env.__stage._html), 'an honest blocked message renders');
api.setRationale('Rationale without a grade.');
api.recordDisposition();
ok(api.screen === 1 && api.records.length === 0, 'rationale alone is still blocked (grade required)');
api.setRationale('');
api.pickGrade('confirm-risk');
api.recordDisposition();
ok(api.screen === 1 && api.records.length === 0, 'grade alone is still blocked (rationale required)');
api.pickGrade('need-more-info');
api.setRationale('Need the KYC file before any call.');
api.recordDisposition();
ok(api.screen === 1 && api.records.length === 0, 'need-more-info WITHOUT a C/D pick is blocked (name which information)');
ok(/id="infopick"/.test(env.__stage._html), 'the C/D taxonomy picker renders for need-more-info');
api.setInfo('D8');
api.recordDisposition();
eq(api.records.length, 1, 'need-more-info + rationale + a D-code pick → records');
ok(api.records[0].grade === 'need-more-info' && api.records[0].info_code === 'D8',
  'the record carries the named D-code (the measured data-gap observation)');

// ---- (4) Reveal: decisions-not-correctness; the seeded second rater replays LABELED ----
eq(api.screen, 2, 'recording advances to the Reveal');
ok(/dismissed/.test(env.__stage._html), 'Reveal discloses the institution’s historical disposition');
ok(/decisions, not correctness/.test(env.__stage._html), 'Reveal frames history as decisions, not correctness');
ok(env.__stage._html.includes(escH('synthetic second rater (seeded)')), 'the seeded second rater replays with its synthetic label VERBATIM');
ok(/escalate/i.test(env.__stage._html), 'the seeded second rater’s disposition renders');

// the guard: a FRESH (unrecorded) scenario can never reach the Reveal directly
api.pickScenario('S-C');
api.gotoScreen(2);
ok(api.screen !== 2, 'Reveal is unreachable pre-disposition (gotoScreen(2) on an unrecorded scenario is refused)');

// below-the-line honesty on Evidence + Reveal
ok(/no rule fired/i.test(env.__stage._html) || /below/i.test(env.__stage._html),
  'below-the-line Evidence states honestly that nothing fired');
api.pickGrade('confirm-risk');
api.setRationale('Band-shifted structuring; the rhythm is the signal.');
api.recordDisposition();
eq(api.records.length, 2, 'a below-the-line disposition records');
ok(/no historical decision/i.test(env.__stage._html), 'below-the-line Reveal states honestly that no historical decision exists');

// ---- (5) the process-inconsistency pair (shared panel, divergent history) ----
api.pickScenario('S-B');
api.advance();
api.pickGrade('escalate');
api.setRationale('Same fact pattern as the dismissed sibling; consistency requires the same call.');
api.recordDisposition();
ok(/process inconsistency/i.test(env.__stage._html), 'the shared-panel divergent pair surfaces the PROCESS INCONSISTENCY at the Reveal');
ok(/never auto-resolved/i.test(env.__stage._html) || /surfaced for adjudication/i.test(env.__stage._html),
  'inconsistency copy: surfaced for adjudication, never auto-resolved');

// ---- (6) Discovery ledger: DERIVED outputs + export ----
api.toLedger();
eq(api.view, 'ledger', 'the Discovery ledger renders');
ok(/chosen, not measured/.test(env.__stage._html), 'the design-params box quotes "chosen, not measured"');
ok(/D8/.test(env.__stage._html), 'the data-gap stream aggregates the named D-code');
const expM = /<textarea id="export"[^>]*>([\s\S]*?)<\/textarea>/.exec(env.__stage._html);
ok(!!expM, 'export textarea present');
let exported = null;
try { exported = JSON.parse(unesc(expM ? expM[1] : '')); } catch { /* fails the next assert */ }
ok(exported && Array.isArray(exported.records) && exported.records.length === 3,
  'export textarea contains VALID JSON with all session records');
ok(/persists nothing/i.test(env.__stage._html), 'ledger states honestly that the offline file persists nothing');
ok(env.__errors.length === 0, 'full arc drove with no console errors');

// ---- (7) the novel stratum: verbatim indicator + licence line + XSS-escape ----
api.pickScenario('S-D');
ok(!/<script>alert/.test(env.__stage._html) && env.__stage._html.includes('&lt;script&gt;'),
  'XSS: a novel flag containing <script> renders escaped, never as markup');
ok(/no legacy rule covers/i.test(env.__stage._html), 'novel Evidence states no legacy rule covers the typology');
ok(/17 U\.S\.C\. §105/.test(env.__stage._html), 'novel Evidence carries the US-federal public-domain licence line');
ok(env.__stage._html.includes(escH(STUB.triage.scenarios[3].novel_source.red_flag)),
  'novel Evidence shows the red_flag translation (escaped — & survives as &amp;)');
api.advance();
api.pickGrade('confirm-risk');
api.setRationale('Controlled-goods exposure with no trade history — risk on this evidence.');
api.recordDisposition();
eq(api.records.length, 4, 'a novel-stratum disposition records');
ok(/no historical decision/i.test(env.__stage._html) && /candidate signal gap/i.test(env.__stage._html),
  'novel Reveal: no history exists; confirmed risk is named a candidate signal gap');

// ---- (8) the policy-gap escape + the control reveal ----
api.pickScenario('S-E');
ok(!/seeded clear-benign control/.test(env.__stage._html), 'control basis stays hidden on Evidence too');
api.advance();
api.pickGrade('no-defensible-option');
api.recordDisposition();
ok(api.records.length === 4 && /id="blockmsg"/.test(env.__stage._html),
  'the policy-gap escape still requires a rationale (empty records nothing)');
api.setRationale('Neither risk nor clearance fits a pure baseline draw with no question to answer.');
api.recordDisposition();
eq(api.records.length, 5, 'no-defensible-option + rationale records (the policy-gap observation)');
ok(/Seeded control scenario/i.test(env.__stage._html) && env.__stage._html.includes(escH(STUB.triage.scenarios[4].control.basis)),
  'the control reveals itself ONLY at the Reveal (known disposition + basis)');
ok(/quality control, not a performance score/i.test(env.__stage._html),
  'control copy: a quality control, not a performance score');

// ---- (9) the discovery ledger DERIVES every output (hand-computed fixtures) ----
api.toLedger();
// signal gaps: confirm-risk/escalate where NO rule fired → S-C (confirm-risk, below-the-line) + S-D
// (confirm-risk, novel). S-B escalated but TM-104 FIRED → excluded by construction.
ok(/Signal gaps · 2/.test(env.__stage._html) && /S-C/.test(env.__stage._html) && /S-D/.test(env.__stage._html),
  'signal gaps DERIVE from fired-rule state (S-C + S-D; the escalated-but-fired S-B excluded)');
// agreement: double-assigned worked = S-A + S-B; S-A (need-more-info) diverges from the escalate
// seed, S-B (escalate) matches → 1/2 exactly.
ok(/Agreement · 1\/2/.test(env.__stage._html), 'agreement arithmetic equals the hand-computed fixture (1/2)');
ok(/consensus-class, never a correctness measure/.test(env.__stage._html),
  'the agreement panel renders its measurement-definition string');
ok(/Process inconsistencies · 1/.test(env.__stage._html) && /P-PAIR/.test(env.__stage._html),
  'the worked shared-panel pair lands in the ledger as ONE process inconsistency');
ok(/Policy gaps · 1/.test(env.__stage._html) && /S-E/.test(env.__stage._html),
  'the policy-gap record lands in the ledger');
ok(env.__stage._html.includes(escH(STUB.taxonomy.data_sources[1].name)),
  'data-gap rows carry the taxonomy NAME for the coded gap');
const expM2 = /<textarea id="export"[^>]*>([\s\S]*?)<\/textarea>/.exec(env.__stage._html);
let exported2 = null;
try { exported2 = JSON.parse(unesc(expM2 ? expM2[1] : '')); } catch { /* fails below */ }
ok(exported2 && exported2.records.length === 5, 'export carries all 5 session records');
ok(exported2 && exported2.derived
  && exported2.derived.signal_gaps.join(',') === 'S-C,S-D'
  && exported2.derived.policy_gaps.join(',') === 'S-E'
  && exported2.derived.data_gaps.D8 && exported2.derived.data_gaps.D8.join(',') === 'S-A'
  && exported2.derived.process_inconsistencies.length === 1
  && exported2.derived.agreement.matched === 1 && exported2.derived.agreement.double_assigned_worked === 2
  && /never a correctness measure/.test(exported2.derived.agreement.definition),
  'export.derived carries every §14 discovery output with the hand-computed values + definition');

// ---- (10) revisit + queue marking ----
api.pickScenario('S-A');
ok(/Disposition recorded/i.test(env.__stage._html) || api.screen === 0, 'a disposed scenario reopens (Evidence first)');
api.gotoScreen(2);
eq(api.screen, 2, 'a disposed scenario may revisit its Reveal');
api.toQueue();
eq((env.__stage._html.match(/Recorded ·/g) || []).length, 5, 'queue marks all 5 disposed scenarios');

// ---- (11) honest EMPTY ledger state (fresh context) ----
const envE = boot(true);
envE.__api.toLedger();
ok(/No dispositions/i.test(envE.__stage._html), 'empty ledger shows an honest empty state');

// ---- (12) keyboard navigation (←/→/Space/Esc) + input guards ----
const envK = boot(true);
const apiK = envK.__api;
envK.__key('ArrowRight');
eq(apiK.view, 'queue', 'ArrowRight on the queue stays put (scenarios are picked, not paged)');
apiK.pickScenario('S-A');
envK.__key('ArrowRight');
eq(apiK.screen, 1, '→ advances Evidence → Disposition');
envK.__key('ArrowLeft');
eq(apiK.screen, 0, '← returns Disposition → Evidence');
envK.__key(' ');
eq(apiK.screen, 1, 'Space advances');
envK.__key('ArrowRight', 'TEXTAREA');
eq(apiK.screen, 1, 'arrow keys inside the rationale TEXTAREA never navigate');
envK.__key('ArrowRight', 'SELECT');
eq(apiK.screen, 1, 'arrow keys inside the C/D picker SELECT never navigate');
envK.__key('ArrowRight');
eq(apiK.screen, 1, '→ on an unrecorded Disposition does NOT skip the gate (blocked, not advanced)');
eq(apiK.records.length, 0, 'keyboard advance records nothing without grade + rationale');
envK.__key('Escape');
eq(apiK.view, 'queue', 'Esc returns to the queue');

// ---- (13) queue row click wiring + reduced-motion branch ----
const envC = boot(false);
const apiC = envC.__api;
eq(apiC.REDUCED, false, 'full-motion context: REDUCED is false');
const row = envC.__stage._qs('.scnrow')[0];
ok(row && typeof row.onclick === 'function', 'queue scenario rows are click-wired');
row.onclick();
eq(apiC.view, 'case', 'clicking a queue row opens the scenario');
const envR = boot(true);
eq(envR.__api.REDUCED, true, 'prefers-reduced-motion context: REDUCED branch engages');

/* ---------- verdict ---------- */
console.log(`\n${pass} passed, ${fails.length} failed`);
if (fails.length) { console.log('FAILED:'); fails.forEach(f => console.log('  - ' + f)); process.exit(1); }
