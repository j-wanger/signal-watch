#!/usr/bin/env node
// Merge-console arc regression harness — ZERO runtime deps (Node built-in `vm` + the corpus-explorer
// hand-rolled DOM shim pattern; no third-party DOM library, no npm install).
// Run: `node tests/merge-console.test.mjs`.
//
// What it does: loads merge.html (the TEMPLATE — the 6th single-file offline artifact), injects a
// controlled STUB dataset at the single injection placeholder (so the harness owns the XSS strings and
// the consensus-vs-scored split), evaluates the inline script under the shim, then drives the 5-screen arc
// (Queue → Evidence → Adjudication → Verdict → Ledger) and asserts the Phase-76 invariants:
//   - the queue groups candidate links BY BASIS (strong-shared-id / weak / name-only); honest split
//     counts (real consensus vs synthetic scored); a "scored · synthetic" chip on synthetic candidates;
//   - Evidence shows BOTH records + the shared signal + the deterministic spine baseline, NEUTRALLY —
//     the latent-truth ORACLE never appears pre-adjudication (the firewall: truth rides the verdict only);
//   - the non-binary graded gate: recording is BLOCKED without grade + rationale (the Class-J obligation),
//     records with both;
//   - the Verdict appears ONLY post-adjudication and SPLITS real-consensus from synthetic-scored:
//       * a REAL case shows "consensus, no ground truth" and carries NO oracle;
//       * a SYNTHETIC case shows the latent truth + a match indicator + the synthetic-only qualifier;
//   - the Ledger accumulates; export is valid JSON; the agreement arithmetic splits consensus from the
//     synthetic-scored set (matched/scored, qualified); session-only honesty copy;
//   - the always-on badge node; NO catch-rate/lift wording;
//   - XSS: case fields containing <script> / & render escaped (esc() is the sole escaper);
//   - ←/→/Space/Esc presenter navigation (guarded inside INPUT/TEXTAREA); the reduced-motion branch.

import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';
import vm from 'node:vm';

const HERE = dirname(fileURLToPath(import.meta.url));
const TEMPLATE = resolve(HERE, '..', 'merge.html');
const PLACEHOLDER = '__MERGE__';
const QUAL = 'measured on synthetic clusters; production has no ground truth';

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
// mirror merge.html's esc() so we can assert escaped text appears in the rendered stage
function escH(s){return String(s==null?'':s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;').replace(/'/g,'&#39;');}
// undo esc() on extracted textarea content (entity order matters: &amp; LAST)
function unesc(s){return s.replace(/&#39;/g,"'").replace(/&quot;/g,'"').replace(/&lt;/g,'<').replace(/&gt;/g,'>').replace(/&amp;/g,'&');}

/* ---------- the stub dataset (the harness owns the edge cases) ---------- */
const STUB = {
  brand: { title: 'Signal Watch', subtitle: 'Merge Console · Vision Prototype' },
  badge: 'Illustrative data & outputs',
  adjudication_grades: [
    { id: 'uphold_merge', label: 'Uphold the merge', desc: 'These records are the same entity.' },
    { id: 'reject_as_shares', label: 'Reject — keep distinct (a SHARES edge)', desc: 'Distinct entities that share an identifier.' },
    { id: 'both_defensible', label: 'Both defensible', desc: 'The evidence underdetermines it.' },
    { id: 'escalate', label: 'Neither — escalate', desc: 'Insufficient to call either way.' },
  ],
  bases: [
    { id: 'strong', label: 'Strong shared identifier', desc: 'share an exact email / phone / account number' },
    { id: 'weak', label: 'Weak corroboration', desc: 'share only an address' },
    { id: 'name', label: 'Name-only', desc: 'share only a name' },
  ],
  provenance: { substrate_head: 'fc98b09', slice_cases: 376, n_real_consensus: 1, n_synthetic_scored: 3,
                synthetic_qualifier: QUAL },
  cases: [
    { // REAL consensus — strong shared email, two distinct names, NO oracle
      id: 'real-P-0001-P-0002', source: 'substrate-v0.5-slice', scored: false, basis: 'strong',
      shared: { kind: 'email', value: 'user383771@example.test' }, cross_institution: true,
      spine_verdict: 'kept_distinct', substrate_claim: 'resolved',
      a: { ref: 'P-0001', name: 'Owen Patel', kind: 'person', role: 'BENEFICIAL_OWNER',
           attrs: { risk: 'LOW', pep: 'NONE', sanctions: false, adverse_media: false } },
      b: { ref: 'P-0002', name: 'Emma Thompson', kind: 'person', role: 'BENEFICIAL_OWNER',
           attrs: { risk: 'MEDIUM', pep: 'NONE', sanctions: false, adverse_media: false } } },
    { // SYNTHETIC scored — over-merge trap (resolver MERGED; truth DISTINCT → reject is correct)
      id: 'syn-o9-o10', source: 'synthetic-oracle', scored: true, basis: 'strong',
      shared: { kind: 'phone', value: '15550140' }, spine_verdict: 'merged',
      a: { ref: 'o9', name: 'Marcus Webb', kind: 'person', role: 'related_party',
           identifiers: [{ kind: 'phone', value: '+1-555-0140' }] },
      b: { ref: 'o10', name: 'Tanya Webb', kind: 'person', role: 'counterparty',
           identifiers: [{ kind: 'phone', value: '+1-555-0140' }] },
      oracle: { same_entity: false, klass: 'over-merge-trap', correct_adjudication: 'reject_as_shares', qualifier: QUAL } },
    { // SYNTHETIC scored — fragmentation gap, NAME-only basis (resolver kept distinct; truth SAME → uphold)
      id: 'syn-o7-o8', source: 'synthetic-oracle', scored: true, basis: 'name',
      shared: null, spine_verdict: 'kept_distinct',
      a: { ref: 'o7', name: 'Sam Okafor', kind: 'person', role: 'counterparty',
           identifiers: [{ kind: 'phone', value: '+1-555-0173' }] },
      b: { ref: 'o8', name: 'Sam Okafor', kind: 'person', role: 'counterparty', identifiers: [] },
      oracle: { same_entity: true, klass: 'fragmentation-gap', correct_adjudication: 'uphold_merge', qualifier: QUAL } },
    { // XSS probe — hostile strings in name fields + a WEAK (address) basis; esc() must neutralize
      id: 'syn-xss', source: 'synthetic-oracle', scored: true, basis: 'weak',
      shared: { kind: 'address', value: '88 Maple Ave <test>' }, spine_verdict: 'kept_distinct',
      a: { ref: 'oX', name: '<script>alert(1)</script> Reyes', kind: 'person', role: 'counterparty',
           identifiers: [{ kind: 'address', value: '88 Maple Ave' }] },
      b: { ref: 'oY', name: 'Nadia & Haddad', kind: 'person', role: 'counterparty',
           identifiers: [{ kind: 'address', value: '88 Maple Ave' }] },
      oracle: { same_entity: false, klass: 'correct-rejection', correct_adjudication: 'reject_as_shares', qualifier: QUAL } },
  ],
};

/* ---------- load the template + inject the stub ---------- */
const rawHtml = readFileSync(TEMPLATE, 'utf8');
ok(rawHtml.split(PLACEHOLDER).length === 2, 'merge.html carries exactly ONE injection placeholder');
ok(/id="badge"/.test(rawHtml) && /Illustrative data/.test(rawHtml), 'the always-on "Illustrative data & outputs" badge node is present in the chrome');
ok(/prefers-reduced-motion/.test(rawHtml), 'the reduced-motion CSS branch exists');
ok(!/fetch\(/.test(rawHtml) && !/<script src/.test(rawHtml) && !/type="module"/.test(rawHtml),
  'template is self-contained (no fetch / external script / ES module)');
ok(!/catch[- ]rate/i.test(rawHtml) && !/\blift\b/i.test(rawHtml) && !/precision/i.test(rawHtml),
  'NO catch-rate / lift / precision wording anywhere in the template (the honesty governor)');

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

const EPILOGUE = `;__capture({CASES,GRADES,REDUCED,
  pickCase,pickGrade,setRationale,recordDisposition,advance,back,gotoScreen,toQueue,toLedger,render,
  get view(){return view}, get screen(){return screen},
  get dispositions(){return dispositions}, get draft(){return draft}, get blocked(){return blocked}});`;
function boot(reduced) {
  const env = makeEnv(reduced);
  vm.createContext(env);
  vm.runInContext(SCRIPT + EPILOGUE, env, { filename: 'merge-console-inline.js' });
  return env;
}

/* ============================ drive the arc ============================ */
console.log('merge-console arc harness  (source: merge.html + stub dataset)\n');

const env = boot(true);
const api = env.__api;
ok(api && typeof api.pickCase === 'function', 'script booted; internals re-exported');

// ---- (1) Queue: candidate links grouped by basis, honest split counts ----
eq(api.view, 'queue', 'boots into the Queue (the candidate-SHARES queue is the entry)');
ok((env.__stage._html.match(/class="step /g) || []).length === 5, 'stepper renders the 5 arc steps');
const rows = (env.__stage._html.match(/class="caserow"/g) || []).length;
eq(rows, STUB.cases.length, 'queue lists every candidate as a row');
ok(/Strong shared identifier/.test(env.__stage._html) && /Weak corroboration/.test(env.__stage._html)
  && /Name-only/.test(env.__stage._html), 'queue groups candidates by basis (strong / weak / name)');
eq((env.__stage._html.match(/Scored · synthetic/g) || []).length, 3, 'each synthetic candidate carries a "scored · synthetic" chip');
ok(/Consensus/.test(env.__stage._html), 'the real candidate carries a "consensus" chip');
ok(env.__stage._html.includes('Owen Patel') && env.__stage._html.includes('Emma Thompson'),
  'queue rows show the two record names of each candidate pair');
// NEUTRALITY: the latent truth never appears before the verdict
ok(!/Latent truth/.test(env.__stage._html) && !/Synthetic ground truth/.test(env.__stage._html)
  && !/Defensible call/.test(env.__stage._html), 'NEUTRALITY: the queue never reveals a case oracle truth');
ok(env.__errors.length === 0, 'queue rendered with no console errors');

// ---- (2) Evidence: both records + the shared signal + the deterministic baseline, NEUTRALLY ----
const cReal = STUB.cases[0];
api.pickCase(cReal.id);
eq(api.view, 'case', 'picking a candidate enters the case arc');
eq(api.screen, 0, 'case arc starts on Evidence');
ok(env.__stage._html.includes('Owen Patel') && env.__stage._html.includes('Emma Thompson'),
  'Evidence shows BOTH record names');
ok(env.__stage._html.includes(escH(cReal.shared.value)), 'Evidence shows the shared identifier value');
ok(/kept distinct/.test(env.__stage._html), 'Evidence shows the deterministic spine baseline (kept distinct)');
ok(/same entity/i.test(env.__stage._html), 'Evidence shows the upstream resolver claim for the real case');
ok(/Risk rating/.test(env.__stage._html), 'Evidence shows the real record KYC attributes');
// the firewall in the render: the oracle truth is NOT in the pre-adjudication evidence
ok(!/Latent truth/.test(env.__stage._html) && !/Synthetic ground truth/.test(env.__stage._html)
  && !/Defensible call/.test(env.__stage._html), 'FIREWALL: Evidence never reveals the latent-truth oracle');
ok(env.__errors.length === 0, 'Evidence rendered with no console errors');

// ---- (3) Adjudication: the non-binary graded gate, rationale-REQUIRED ----
api.advance();
eq(api.screen, 1, 'advance → Adjudication');
eq((env.__stage._html.match(/class="gradebtn/g) || []).length, 4, 'FOUR grades offered (uphold / reject-as-SHARES / both / escalate)');
ok(/id="rationale"/.test(env.__stage._html), 'free-text rationale field present');
api.recordDisposition();
eq(api.screen, 1, 'recording with NEITHER grade nor rationale is blocked (stays on Adjudication)');
eq(api.dispositions.length, 0, 'nothing recorded while blocked');
ok(/id="blockmsg"/.test(env.__stage._html), 'an honest blocked message renders');
api.pickGrade('reject_as_shares');
api.recordDisposition();
ok(api.screen === 1 && api.dispositions.length === 0, 'grade alone is still blocked (rationale required — the Class-J obligation)');
const RAT_REAL = 'Distinct beneficial owners sharing a noise-floor email; no ground truth — record as a SHARES edge. <&test>';
api.setRationale(RAT_REAL);
api.recordDisposition();
eq(api.dispositions.length, 1, 'grade + rationale → the adjudication records');
ok(api.dispositions[0].grade === 'reject_as_shares' && api.dispositions[0].rationale === RAT_REAL
  && api.dispositions[0].scored === false, 'the recorded real disposition carries grade + rationale + scored=false');

// ---- (4) Verdict for a REAL case: consensus, NO oracle ----
eq(api.screen, 2, 'recording advances to the Verdict');
ok(/consensus/i.test(env.__stage._html) && /no ground truth/i.test(env.__stage._html),
  'the REAL verdict frames the call as consensus, no ground truth');
ok(!/Synthetic ground truth/.test(env.__stage._html) && !/Latent truth/.test(env.__stage._html),
  'the REAL verdict carries NO oracle (no fabricated ground truth on real data)');
ok(env.__stage._html.includes(escH(RAT_REAL)), 'the REAL verdict shows the presenter rationale (escaped)');

// the guard: a FRESH (unrecorded) candidate can never reach the Verdict directly
api.pickCase(STUB.cases[1].id);
api.gotoScreen(2);
ok(api.screen !== 2, 'Verdict is unreachable pre-adjudication (gotoScreen(2) on an unrecorded candidate is refused)');

// ---- (5) Verdict for a SYNTHETIC scored case: the latent truth + a match indicator + the qualifier ----
const cOver = STUB.cases[1];   // over-merge trap: truth DISTINCT, correct call reject_as_shares
api.pickCase(cOver.id);
api.advance();                  // Evidence → Adjudication
// neutrality on the synthetic evidence too (re-pick lands on Evidence first)
api.gotoScreen(0);
ok(!/Synthetic ground truth/.test(env.__stage._html) && !/Latent truth/.test(env.__stage._html),
  'FIREWALL: a synthetic case Evidence screen also hides the oracle');
api.gotoScreen(1);
api.pickGrade('reject_as_shares');                 // the correct call
api.setRationale('A shared landline is household, not identity — keep distinct.');
api.recordDisposition();
eq(api.screen, 2, 'synthetic adjudication advances to the Verdict');
ok(/Synthetic ground truth/.test(env.__stage._html), 'the SYNTHETIC verdict shows the latent-truth oracle card');
ok(/DISTINCT entities/.test(env.__stage._html), 'the oracle shows the latent truth (distinct entities)');
ok(/matched the synthetic truth/i.test(env.__stage._html), 'a correct call is shown as matching the synthetic truth');
ok(env.__stage._html.includes(QUAL), 'the synthetic verdict carries the synthetic-only qualifier');

// a WRONG call on a synthetic case shows the mismatch
const cFrag = STUB.cases[2];   // fragmentation gap: truth SAME, correct call uphold_merge
api.pickCase(cFrag.id);
api.advance();
api.pickGrade('reject_as_shares');                 // the WRONG call (truth is SAME)
api.setRationale('Different identifiers — I keep them apart.');
api.recordDisposition();
ok(/the SAME entity/.test(env.__stage._html), 'the fragmentation oracle shows the latent truth (same entity)');
ok(/differs from the synthetic truth/i.test(env.__stage._html), 'a wrong call is shown as differing from the synthetic truth');

// ---- (6) Ledger: accumulation + the consensus/scored split + JSON export ----
api.advance();
eq(api.view, 'ledger', 'advance from the Verdict reaches the session Ledger');
eq((env.__stage._html.match(/class="ledrow"/g) || []).length, 3, 'ledger accumulates all session adjudications');
ok(/1<\/b> real/.test(env.__stage._html) || /1 real/.test(env.__stage._html), 'ledger reports the consensus (real) count');
ok(env.__stage._html.includes(QUAL), 'the ledger agreement arithmetic carries the synthetic-only qualifier');
ok(/persists nothing/i.test(env.__stage._html), 'ledger states honestly that the offline file persists nothing');
const expM = /<textarea id="export"[^>]*>([\s\S]*?)<\/textarea>/.exec(env.__stage._html);
ok(!!expM, 'export textarea present');
let exported = null;
try { exported = JSON.parse(unesc(expM ? expM[1] : '')); } catch { /* fails the next assert */ }
ok(exported && Array.isArray(exported.dispositions) && exported.dispositions.length === 3,
  'export textarea contains VALID JSON with all three adjudications');
ok(exported && exported.scored_agreement && exported.scored_agreement.matched === 1
  && exported.scored_agreement.scored_adjudicated === 2,
  'exported scored_agreement counts only synthetic cases (1 of 2 matched the oracle)');
ok(exported && exported.consensus_adjudicated === 1, 'exported consensus_adjudicated counts only the real case');
ok(exported && exported.scored_agreement.qualifier === QUAL, 'the exported scored agreement is qualified synthetic-only');
ok(env.__errors.length === 0, 'full arc drove with no console errors');

// ---- (7) XSS: hostile fields render escaped ----
const envX = boot(true);
const apiX = envX.__api;
apiX.pickCase('syn-xss');
ok(!/<script>alert/.test(envX.__stage._html) && envX.__stage._html.includes('&lt;script&gt;'),
  'XSS: a record name containing <script> renders escaped, never as markup');
ok(envX.__stage._html.includes('Nadia &amp; Haddad'), 'XSS: a name containing & renders escaped');
ok(envX.__stage._html.includes(escH('88 Maple Ave <test>')), 'XSS: a shared identifier value with <…> renders escaped');

// ---- (8) honest EMPTY ledger state (fresh context) ----
const envE = boot(true);
envE.__api.toLedger();
ok(/No adjudications recorded/i.test(envE.__stage._html), 'empty ledger shows an honest empty state');

// ---- (9) keyboard navigation (←/→/Space/Esc) + input guard ----
const envK = boot(true);
const apiK = envK.__api;
envK.__key('ArrowRight');
eq(apiK.view, 'queue', 'ArrowRight on the queue stays put (candidates are picked, not paged)');
apiK.pickCase(STUB.cases[0].id);
envK.__key('ArrowRight');
eq(apiK.screen, 1, '→ advances Evidence → Adjudication');
envK.__key('ArrowLeft');
eq(apiK.screen, 0, '← returns Adjudication → Evidence');
envK.__key(' ');
eq(apiK.screen, 1, 'Space advances');
envK.__key('ArrowRight', 'TEXTAREA');
eq(apiK.screen, 1, 'arrow keys inside the rationale TEXTAREA never navigate');
envK.__key('ArrowRight');
eq(apiK.screen, 1, '→ on an unrecorded Adjudication does NOT skip the gate (blocked, not advanced)');
eq(apiK.dispositions.length, 0, 'keyboard advance records nothing without grade + rationale');
envK.__key('Escape');
eq(apiK.view, 'queue', 'Esc returns to the queue');

// ---- (10) queue row click wiring + reduced-motion branch ----
const envC = boot(false);
const apiC = envC.__api;
eq(apiC.REDUCED, false, 'full-motion context: REDUCED is false');
const row = envC.__stage._qs('.caserow')[0];
ok(row && typeof row.onclick === 'function', 'queue candidate rows are click-wired');
row.onclick();
eq(apiC.view, 'case', 'clicking a queue row opens the candidate');
const envR = boot(true);
eq(envR.__api.REDUCED, true, 'prefers-reduced-motion context: REDUCED branch engages');

/* ---------- verdict ---------- */
console.log(`\n${pass} passed, ${fails.length} failed`);
if (fails.length) { console.log('FAILED:'); fails.forEach(f => console.log('  - ' + f)); process.exit(1); }
