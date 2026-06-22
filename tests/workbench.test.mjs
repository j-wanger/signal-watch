#!/usr/bin/env node
// Investigator case-workbench harness — ZERO runtime deps (Node built-in `vm` + a DOM/fetch shim).
// Run: `node tests/workbench.test.mjs`.
//
// workbench.html is NOT a build target (companion-served by scripts/serve_workbench.py). This loads the
// RAW template, shims fetch + a minimal DOM, evaluates the inline <script>, and asserts the three beats:
//   1. CLUTTER  — the population strip (honest counts), the gate-filtered queue, the per-case dense view
//                 (KYC profile, accounts, channel summary, counterparties, the full transaction table).
//   2. SIGNALS  — the master switch toggles `.signals-on`; the grounded risk picture + the precedent read
//                 + the flag→corpus audit walk reveal; the alert-cited transactions highlight.
//   3. DECIDE   — the live finale streams NDJSON stages → signed SAR (the serve_chain ledger pattern).
// Plus: the badge, esc() as the sole escaper (XSS), the backend picker (names only), NO catch-rate /
// precision / lift number anywhere (the detection-lift triple-null), and both motion modes (CSS present).

import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';
import vm from 'node:vm';

const HERE = dirname(fileURLToPath(import.meta.url));
const WB = resolve(HERE, '..', 'workbench.html');

let pass = 0; const fails = [];
function ok(cond, msg){ if (cond){ pass++; console.log(`  ✓ ${msg}`); } else { fails.push(msg); console.log(`  ✗ ${msg}`); } }
function escH(s){return String(s==null?'':s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;').replace(/'/g,'&#39;');}

/* ---------- structural checks on the raw template ---------- */
const html = readFileSync(WB, 'utf8');
ok((html.match(/<!--__WORKBENCH_CONFIG__-->/g)||[]).length === 1, 'raw workbench.html carries exactly one config marker');
ok(/Illustrative data &amp; outputs/.test(html), 'always-on "Illustrative data & outputs" badge present');
ok((html.match(/<script>/g)||[]).length === 1, 'exactly one inline <script>');
ok(/@media\(prefers-reduced-motion:reduce\)/.test(html), 'reduced-motion CSS present (both motion modes)');
ok(/grounded detection \/ illustrative dispositions/.test(html), 'footer states the grounded-detection / illustrative-disposition split');

const open = html.indexOf('<script>'), close = html.lastIndexOf('</script>');
const SCRIPT = html.slice(open + '<script>'.length, close)
  + `\n;globalThis.__T={esc,money,gateClass,gateLabel,channelSummary,counterpartySummary,kycPanel,citedTxnIds,`
  + `toggleSignals,selectCase,pickBackend,applyMessage,runDecision,paintSurface,renderQueue,renderPop,loadQueue,backendLabel,`
  + `liveGate,liveFunnel,setGate,renderGate,loadGate,onKnob,resetGating,doAdjudicate,policyThresholds,`
  + `runGather,applyGather,gatherPanelHTML,gatherResultHTML,gatherGraphHTML,liveGraphLayout,toolLabel,kindLabel,`
  + `setState:(s)=>{ if('META'in s)META=s.META; if('QUEUE'in s)QUEUE=s.QUEUE; if('FILTER'in s)FILTER=s.FILTER; if('SEL'in s)SEL=s.SEL; if('DETAIL'in s)DETAIL=s.DETAIL; if('SIGNALS'in s)SIGNALS=s.SIGNALS; if('RUN'in s)RUN=s.RUN; if('GATE'in s)setGate(s.GATE); if('POLICY'in s)POLICY=s.POLICY; if('ADJ'in s)ADJ=s.ADJ; if('GATHER'in s)GATHER=s.GATHER; },`
  + `getState:()=>({META,QUEUE,FILTER,SEL,DETAIL,SIGNALS,BACKEND,RUN,GATE,POLICY,ADJ,GATHER})};`;

/* ---------- DOM + fetch shim ---------- */
function makeEl(id){
  return {
    id, _html:'', _text:'', _class:'', dataset:{}, onclick:null,
    set innerHTML(v){ this._html = String(v); }, get innerHTML(){ return this._html; },
    set textContent(v){ this._text = String(v); }, get textContent(){ return this._text; },
    set className(v){ this._class = String(v); }, get className(){ return this._class; },
    querySelector(){ return { onclick:null, dataset:{} }; },
    querySelectorAll(sel){
      const attr = /data-backend/.test(sel) ? 'data-backend' : /data-disp/.test(sel) ? 'data-disp'
                 : /data-f"?/.test(sel) ? 'data-f' : 'data-case';
      const out = []; const re = new RegExp(attr + '="([^"]*)"', 'g'); let m;
      while ((m = re.exec(this._html))) out.push({ dataset:{ [attr.replace('data-','')]: m[1] }, onclick:null });
      return out;
    },
  };
}
const ELEMENTS = {};
['badge','draftChip','popStrip','queue','qcount','filters','surf','masterSwitch','decideBtn','picker',
 'gatePanel','knobHigh','knobMed','gateReset','adjud','adjudRead','gatherBtn'].forEach(id => ELEMENTS[id] = makeEl(id));
const documentShim = { getElementById(id){ return ELEMENTS[id] || (ELEMENTS[id] = makeEl(id)); } };

function streamResponse(chunks){
  let i = 0;
  return { ok:true, body:{ getReader(){ return { read(){
    return Promise.resolve(i < chunks.length ? { done:false, value:chunks[i++] } : { done:true, value:undefined });
  } }; } } };
}
const enc = new TextEncoder();
function ndjsonChunks(objs, splitAt){
  const text = objs.map(o => JSON.stringify(o)).join('\n') + '\n';
  if (splitAt == null) return [enc.encode(text)];
  return [enc.encode(text.slice(0, splitAt)), enc.encode(text.slice(splitAt))];
}

let CASES_RESPONSE = { badge:'Illustrative data & outputs', meta:{}, cases:[] };
let CASE_RESPONSE = {};
let RUN_CHUNKS = [];
let LAST_RUN_BODY = null;
let GATE_RESPONSE = null, ADJ_RESPONSE = null;     // the gating-engine stubs (set per gating test)
let LAST_GATE_URL = null, LAST_ADJ_BODY = null;
let GATHER_CHUNKS = [], LAST_GATHER_BODY = null;    // the gather-beat stream stub (Phase 65)
function fetchShim(url, opts){
  const u = String(url);
  if (u.includes('/gather')){ try { LAST_GATHER_BODY = JSON.parse((opts&&opts.body)||'{}'); } catch(e){ LAST_GATHER_BODY = null; }
    return Promise.resolve(streamResponse(GATHER_CHUNKS)); }
  if (u.includes('/cases')) return Promise.resolve({ ok:true, json:()=>Promise.resolve(CASES_RESPONSE) });
  if (u.includes('/case/')) return Promise.resolve({ ok:true, json:()=>Promise.resolve(CASE_RESPONSE) });
  if (u.includes('/gate')){ LAST_GATE_URL = u;
    return Promise.resolve({ ok:true, json:()=>Promise.resolve(GATE_RESPONSE||{error:'no gate stub'}) }); }
  if (u.includes('/adjudicate')){ try { LAST_ADJ_BODY = JSON.parse((opts&&opts.body)||'{}'); } catch(e){ LAST_ADJ_BODY = null; }
    return Promise.resolve({ ok:true, json:()=>Promise.resolve(ADJ_RESPONSE||{ok:true}) }); }
  if (u.includes('/run')){ try { LAST_RUN_BODY = JSON.parse((opts&&opts.body)||'{}'); } catch(e){ LAST_RUN_BODY = null; }
    return Promise.resolve(streamResponse(RUN_CHUNKS)); }
  return Promise.reject(new Error('unexpected url '+url));
}

const WB_CFG = { cases:'/cases', case:'/case', gate:'/gate', adjudicate:'/adjudicate', run:'/run',
  health:'/health', badge:'Illustrative data & outputs',
  policy:{ thresholds:{high:500, medium:50}, gate_of_level:{high:'auto-clear', medium:'review', low:'human-gate'} },
  drafter:{ default:'stub', available:['stub','claude','openai'],
            backends:[{name:'stub',available:true},{name:'claude',available:true},
                      {name:'openai',available:true},{name:'opencode',available:false}] } };

const sandbox = { document:documentShim, window:{ __WORKBENCH_CONFIG__: WB_CFG }, fetch:fetchShim,
  TextDecoder, TextEncoder, Uint8Array, JSON, Promise, setTimeout, console, encodeURIComponent };
sandbox.globalThis = sandbox;
vm.createContext(sandbox);
vm.runInContext(SCRIPT, sandbox);
const T = sandbox.__T;

/* ---------- esc() + money formatting ---------- */
ok(T.esc('<b>&"\'') === '&lt;b&gt;&amp;&quot;&#39;', 'esc() encodes <,>,&,",\' (the sole escaper)');
ok(T.money(1234567) === '$12,345.67', 'money() formats cents → CAD dollars');

/* ---------- synthetic population (a gate spread + an XSS case) ---------- */
const META = {
  slice_total:4, substrate_head:'f90bd39',
  coverage:{ groundable:4, total:4, basis:'casework-asserted capabilities' },
  gate_funnel:{ 'auto-clear':2, 'review':1, 'human-gate':1 },
  exemplars:{ mule:'CASE-P-MULE', fp_trap:'CASE-P-FP', thin:'CASE-P-THIN', ambiguous:'CASE-O-AMB' },
};
const QUEUE = [
  { case_id:'CASE-P-MULE', display:{kind:'person',name:'Zane Zhao',synthetic_label:true}, capabilities:['C15','C2','C3','C4','C5'],
    n_alerts:5, n_txns:391, advisories:['fin-2020-alert001'], exemplar:'mule', grounds_e2e:false,
    e2e_note:'casework refused — independent replay couldn\'t reproduce C15, C3 from the cited evidence',
    kyc:{ is_person:true, risk_rating:'HIGH', cdd_level:'EDD', pep_tier:'DPEP', sanctions_flag:false, adverse_media_flag:true,
      occupation:'consultant', source_of_funds:'business income', nationality:'CA', residency_status:'resident',
      expected_monthly_volume_cents:500000, expected_monthly_txn_count:20 },
    confidence:{ combo:'C15+C2+C3+C4+C5', n_precedent:4, level:'low', gate:'human-gate',
      disposition_illustrative:{cleared_pct:28,escalated_pct:72}, disposition_basis:'ILLUSTRATIVE — chosen, not measured' } },
  { case_id:'CASE-O-AMB', display:{kind:'org',name:'General Trading Co.',synthetic_label:true}, capabilities:['C15','C2','C3','C5'],
    n_alerts:4, n_txns:190, advisories:['fin-2020-alert001'], exemplar:'ambiguous', grounds_e2e:false, e2e_note:'casework refused',
    confidence:{ combo:'C15+C2+C3+C5', n_precedent:58, level:'medium', gate:'review',
      disposition_illustrative:{cleared_pct:62,escalated_pct:38}, disposition_basis:'ILLUSTRATIVE — chosen, not measured' } },
  { case_id:'CASE-P-FP', display:{kind:'person',name:'Liam Jain',synthetic_label:true}, capabilities:['C2','C3'],
    n_alerts:2, n_txns:201, advisories:['fin-2020-alert001'], exemplar:'fp_trap', grounds_e2e:false, e2e_note:'casework refused',
    confidence:{ combo:'C2+C3', n_precedent:16856, level:'high', gate:'auto-clear',
      disposition_illustrative:{cleared_pct:88,escalated_pct:12}, disposition_basis:'ILLUSTRATIVE — chosen, not measured' } },
  { case_id:'CASE-XSS', display:{kind:'person',name:'<img src=x onerror=alert(1)>',synthetic_label:true}, capabilities:['<b>C9</b>'],
    n_alerts:1, n_txns:24, advisories:[], exemplar:null, grounds_e2e:true, e2e_note:'signed end-to-end',
    confidence:{ combo:'C2', n_precedent:1031, level:'high', gate:'auto-clear',
      disposition_illustrative:{cleared_pct:88,escalated_pct:12}, disposition_basis:'ILLUSTRATIVE — chosen, not measured' } },
];

/* ---------- BEAT 1: population strip + queue ---------- */
T.setState({ META, QUEUE, FILTER:'all', SIGNALS:false });
T.renderPop(); T.renderQueue();
const pop = ELEMENTS.popStrip._html;
ok(/4<\/span>/.test(pop) || /4</.test(pop), 'population strip shows the case count');
ok(/4\/4/.test(pop), 'population strip shows the coverage statistic (groundable/total)');
ok(/1<\/b> human gate/.test(pop) && /1<\/b> review/.test(pop) && /2<\/b> auto-clear/.test(pop),
   'population strip shows the honest gate funnel');
ok(/id="masterSwitch"/.test(pop), 'the signals master switch renders');

const q = ELEMENTS.queue._html;
ok(/Zane Zhao/.test(q) && /General Trading Co\./.test(q), 'queue renders case display names');
ok((q.match(/class="qcard/g)||[]).length === 4, 'queue renders one card per case');
ok(/gdot human/.test(q) && /gdot review/.test(q) && /gdot auto/.test(q), 'queue cards carry a gate dot per gate level');
ok(/class="xtag">mule</.test(q), 'an exemplar case is tagged in the queue');
ok(/✓ grounds/.test(q) && /won.{0,2}t sign/.test(q), 'queue cards show the grounds-end-to-end indicator (signs vs fails-closed)');
ok(!/<img src=x onerror/.test(q) && q.includes(escH('<img src=x onerror=alert(1)>')), 'XSS: a malicious display name is esc()-escaped');

/* gate filter narrows the queue */
T.setState({ FILTER:'human-gate' }); T.renderQueue();
const qh = ELEMENTS.queue._html;
ok(/Zane Zhao/.test(qh) && !/Liam Jain/.test(qh), 'the human-gate filter shows only human-gate cases');
T.setState({ FILTER:'all' }); T.renderQueue();

/* ---------- per-case clutter view (signals OFF) ---------- */
const MULE_DETAIL = {
  case: QUEUE[0],
  bundle: {
    subject:{ customer_id:'P-0002174', account_ids:['A-1','A-2'] },
    parties:[{ is_person:true, risk_rating:'HIGH', cdd_level:'EDD', pep_tier:'DPEP', sanctions_flag:false,
      adverse_media_flag:true, occupation:'consultant', source_of_funds:'business income',
      nationality:'CA', residency_status:'resident', expected_monthly_volume_cents:500000, expected_monthly_txn_count:20 }],
    alerts:[{ capability:'C4', detector:'structuring', txn_ids:['T-1','T-3'],
              grounding:{ advisory_id:'fin-2020-alert001', indicator_id:'IND-05', signal_id:'fin-2020-alert001:IND-05',
                          flag:'sub-$10,000 structured cash deposits' } }],
    transactions:[
      { txn_id:'T-1', timestamp:'2024-01-01T08:00:00', channel:'CASH', direction:'CREDIT', amount_cents:900000, counterparty_ref:'CP-1' },
      { txn_id:'T-2', timestamp:'2024-01-02T09:00:00', channel:'EMT', direction:'DEBIT', amount_cents:120000, counterparty_ref:'CP-2' },
      { txn_id:'T-3', timestamp:'2024-01-03T10:00:00', channel:'CASH', direction:'CREDIT', amount_cents:880000, counterparty_ref:'CP-1' },
    ],
  },
  signals: [
    { capability:'C4', detector:'structuring', signal_id:'fin-2020-alert001:IND-05', source:'fincen',
      corpus_flag:'multiple cash transactions for under $10,000 <not a tag>', red_flag:'CTR-trigger evasion', grounded:true },
  ],
};
T.setState({ SEL:'CASE-P-MULE', DETAIL:MULE_DETAIL, SIGNALS:false }); T.paintSurface();
let s = ELEMENTS.surf._html;
ok(/Zane Zhao/.test(s), 'case view headlines the subject');
ok(/synthetic display identity over real KYC/.test(s), 'the synthetic-identity-over-real-KYC note is shown');
ok(/risk rating/.test(s) && /HIGH/.test(s) && /EDD/.test(s) && /DPEP/.test(s), 'KYC panel renders the real profile fields');
ok(/A-1/.test(s) && /A-2/.test(s), 'accounts panel lists the subject accounts');
ok(/CASH · 2 ·/.test(s), 'channel summary aggregates by channel (count + total)');
ok(/class="tx"/.test(s) && (s.match(/data-tx=/g)||[]).length === 3, 'transaction table renders every transaction (the clutter)');
ok(!/signals-on/.test(ELEMENTS.surf._class), 'with signals OFF the surface is NOT in signals-on mode');

/* ---------- BEAT 2: turn signals ON ---------- */
T.toggleSignals(); s = ELEMENTS.surf._html;
ok(/signals-on/.test(ELEMENTS.surf._class), 'the master switch puts the surface into signals-on mode (clutter→clarity)');
ok(/Grounded risk picture/.test(s), 'signals-on reveals the grounded risk picture');
ok(/C15.*C2.*C3.*C4.*C5/s.test(s) || /5 grounded signals compose/.test(s), 'risk picture names the composed signals');
ok(/gatebadge human/.test(s) && /Human gate/.test(s), 'the gate badge reflects the case gate (human-gate)');
ok(/<b>4<\/b> similar prior firings/.test(s), 'the precedent read shows the REAL sample size');
ok(/Disposition history illustrative/.test(s), 'the disposition is explicitly labeled illustrative');
ok(/Audit walk/.test(s), 'the flag→corpus audit walk reveals');
ok((s.match(/class="wrow"/g)||[]).length === 1 && /✓ grounded/.test(s), 'the audit walk renders a grounded signal row');
ok(/under \$10,000/.test(s), 'the audit walk quotes the verbatim corpus flag');
ok(s.includes(escH('<not a tag>')), 'XSS: a corpus flag is esc()-escaped');
ok((s.match(/class="cited"/g)||[]).length === 2, 'signals-on highlights the 2 alert-cited transactions (T-1, T-3)');

/* ---------- HONESTY: no catch-rate / precision / lift / detection-% anywhere ---------- */
const allRendered = ELEMENTS.popStrip._html + ELEMENTS.queue._html + ELEMENTS.surf._html;
ok(!/\b(lift|precision|recall|catch[\s-]?rate|f1|auroc)\b/i.test(allRendered),
   'NO catch-rate/precision/lift/recall vocabulary in any rendered surface (the detection-lift null)');
ok(!/\d+(\.\d+)?\s*%/.test(allRendered) && !/\d+(\.\d+)?x\b/.test(allRendered),
   'NO performance percentage or "Nx" lift figure rendered (counts only: precedent sample, coverage ratio)');

/* ---------- BEAT 3: the live finale (decide) ---------- */
T.setState({ SEL:'CASE-P-MULE', DETAIL:MULE_DETAIL, SIGNALS:true, RUN:null });
const DONE = {
  case:{ case_id:'CASE-P-MULE', confidence:QUEUE[0].confidence },
  consume:{ drafter_effective:'stub', signed:true, blocking_violations:[] },
  signed_sar:{ str_record:{ narrative:'Subject exhibits a multi-typology pattern. <not a tag>',
    narrative_claims:[{ text:'Sub-$10k cash deposits indicate structuring.', cites:['fin-2020-alert001:IND-05'] }] } },
  audit_walk:[{ capability:'C4', grounded:true }], connected:true,
};
const RUN_MSGS = [
  { stage:'evidence', case_id:'CASE-P-MULE', alert_count:5, txn_count:391, capabilities:['C4'], subject:{} },
  { stage:'consume', status:'running', drafter:'stub' },
  { stage:'consume', status:'done', drafter:'stub', drafter_effective:'stub', signed:true, blocking_violations:[],
    completeness:{ reporting_entity:true, transaction_details:true, account_information:true,
      subject_information:true, typology_grounds:true, grounds_for_suspicion_narrative:true } },
  { stage:'verify', status:'done', connected:true, exit:0 },
  { stage:'connected', connected:true },
  { done: DONE },
];
RUN_CHUNKS = ndjsonChunks(RUN_MSGS, 35);   // split the first line across chunks → the line buffer
await T.runDecision();
const f = ELEMENTS.surf._html;
ok((f.match(/class="node /g)||[]).length === 4, 'the decision ledger has the four canonical stage nodes');
ok(/class="node connected"/.test(f), 'the streamed finale reaches the CONNECTED node');
ok((f.match(/class="vchk"/g)||[]).length === 6, 'the consume stage lists the six completeness elements (the verifier gate)');
ok(/Signed STR/.test(f) && /multi-typology pattern/.test(f), 'the signed-STR narrative renders');
ok(f.includes(escH('<not a tag>')), 'XSS: the model narrative is esc()-escaped');
const st = T.getState();
ok(st.RUN && st.RUN.done && st.RUN.running === false, 'the decision settles (done payload, not running)');

/* the picked backend NAME is POSTed to /run (never a cred) */
ok(LAST_RUN_BODY && LAST_RUN_BODY.case === 'CASE-P-MULE', 'runDecision POSTs the case to /run');

/* a NEURAL backend the server didn't actually run → a LOUD "server unavailable, ran the stub" banner
   (the "all enabled, say unavailable" UX), distinguishing not-configured from a configured-but-failed draft.
   (a) UNCONFIGURED (opencode is available:false here) → "not configured" + the env NAME (never a value, §4.5) */
T.pickBackend('opencode');
T.setState({ SEL:'CASE-P-MULE', DETAIL:MULE_DETAIL, RUN:null });
RUN_CHUNKS = ndjsonChunks(RUN_MSGS, 35);   // consume settles drafter_effective:'stub' → it fell back
await T.runDecision();
const banner = (ELEMENTS.surf._html.match(/<div class="srvna">[\s\S]*?<\/div>/)||[''])[0];
ok(banner && /not configured/.test(banner), 'an UNCONFIGURED backend that ran the stub shows the prominent "server unavailable" banner (no silent stub-as-neural)');
ok(/OPENCODE_SERVE_URL/.test(banner) && !/sk-[A-Za-z0-9]{6,}/.test(banner), 'the banner names the env var to set — a NAME, never a credential value (§4.5)');
/* (b) a CONFIGURED backend (claude available:true) that still fell back → "live draft failed", NOT "not configured" */
T.pickBackend('claude');
T.setState({ SEL:'CASE-P-MULE', DETAIL:MULE_DETAIL, RUN:null });
RUN_CHUNKS = ndjsonChunks(RUN_MSGS, 35);
await T.runDecision();
const banner2 = (ELEMENTS.surf._html.match(/<div class="srvna">[\s\S]*?<\/div>/)||[''])[0];
ok(banner2 && /live draft failed/.test(banner2) && !/not configured/.test(banner2), 'a CONFIGURED backend that fell back says the live draft failed — the honest distinction, not "not configured"');
T.pickBackend('stub');  // reset

/* ---------- BEAT 3 (fail-closed): the defensibility climax — casework REFUSES a composed mule ---------- */
const VIOLS = ['grounding_replay: alerts[AL-x].replay(C3): only 0 cited outflow(s); the fan-out pattern needs >=5',
               'grounding_replay: alerts[AL-y].replay(C15): no shell pattern in the cited evidence'];
const FC_DONE = { case:{ case_id:'CASE-P-MULE', confidence:QUEUE[0].confidence },
  consume:{ drafter_effective:'stub', signed:false, blocking_violations:VIOLS },
  signed_sar:{ str_record:{ narrative:null } }, audit_walk:[{capability:'C3',grounded:true}],
  connected:false, disposition:'escalate', fail_closed:true };
const FC_MSGS = [
  { stage:'evidence', case_id:'CASE-P-MULE', alert_count:5, txn_count:391, capabilities:['C3'], subject:{} },
  { stage:'consume', status:'running', drafter:'stub' },
  { stage:'consume', status:'done', drafter:'stub', drafter_effective:'stub', signed:false, blocking_violations:VIOLS, completeness:{} },
  { stage:'verify', status:'skipped', connected:false, note:'casework did not sign — escalating to a human' },
  { stage:'connected', connected:false, fail_closed:true, disposition:'escalate', blocking_violations:VIOLS },
  { done: FC_DONE },
];
T.setState({ SEL:'CASE-P-MULE', DETAIL:MULE_DETAIL, RUN:null });
RUN_CHUNKS = ndjsonChunks(FC_MSGS, 30);
await T.runDecision();
const fc = ELEMENTS.surf._html;
ok(/✗ refused/.test(fc), 'fail-closed: the consume stage shows casework REFUSED (not a crash)');
ok(/escalate to a human/.test(fc) && /That refusal is the defensibility/.test(fc),
   'fail-closed: the escalate-disposition panel is the defensibility climax');
ok(/replay\(C3\)/.test(fc) && /replay\(C15\)/.test(fc), 'fail-closed: the disposition panel lists the blocking violations (the honest reason)');
ok(/⊘ skipped/.test(fc), 'fail-closed: the verify stage renders as skipped (the join is moot), not failed');
ok(!/class="err"/.test(fc), 'fail-closed is a DISPOSITION, not an error banner (no crash framing)');
ok(!/Signed STR/.test(fc), 'fail-closed renders NO signed-STR card');
const fcst = T.getState();
ok(fcst.RUN && fcst.RUN.done && fcst.RUN.done.fail_closed === true && fcst.RUN.running === false,
   'the fail-closed decision settles (fail_closed payload, not running, not errored)');

/* error / gated path (a genuine CRASH — distinct from fail-closed) */
T.setState({ SEL:'CASE-P-MULE', DETAIL:MULE_DETAIL, RUN:null });
RUN_CHUNKS = ndjsonChunks([{ error:'casework consume crashed (no SAR written)' }]);
await T.runDecision();
ok(/Decision gated \/ failed/.test(ELEMENTS.surf._html) && /crashed/.test(ELEMENTS.surf._html),
   'a genuine crash renders the named gated/failed banner (distinct from a fail-closed disposition)');

/* ---------- backend picker (names only; default + unavailable) ---------- */
ok(T.backendLabel('stub')==='deterministic stub' && /claude/.test(T.backendLabel('claude')), 'backendLabel maps backends to display names');
T.setState({ SEL:'CASE-P-MULE', DETAIL:MULE_DETAIL, RUN:null }); T.paintSurface();
const pk = ELEMENTS.surf._html;
ok(/data-backend="stub"/.test(pk) && /data-backend="claude"/.test(pk), 'the picker renders a button per backend');
const ocBtn = (pk.match(/data-backend="opencode"[^>]*>/)||[''])[0];
ok(!/disabled/.test(ocBtn) && /server n\/a/.test(pk), 'an unavailable backend is shown ENABLED (selectable) + marked "server n/a" — not greyed/disabled');
ok(T.getState().BACKEND === 'stub', 'default backend is the config default (stub)');
T.pickBackend('openai'); ok(T.getState().BACKEND === 'openai', 'pickBackend selects an available backend');
T.pickBackend('opencode'); ok(T.getState().BACKEND === 'opencode', 'pickBackend now selects an UNAVAILABLE backend too (it will run the stub + say so)');
T.pickBackend('stub');  // reset for the run tests below

/* ---------- loadQueue via the shimmed /cases endpoint ---------- */
CASES_RESPONSE = { badge:'Illustrative data & outputs', meta:META, cases:QUEUE };
await T.loadQueue();
ok(/Zane Zhao/.test(ELEMENTS.queue._html), 'loadQueue() fetches /cases and renders the population');

/* ---------- selectCase via the shimmed /case endpoint (the real async path) ---------- */
CASE_RESPONSE = MULE_DETAIL;
await T.selectCase('CASE-P-MULE');
ok(/risk rating/.test(ELEMENTS.surf._html) && /HIGH/.test(ELEMENTS.surf._html), 'selectCase() fetches /case/<id> and renders the clutter');

/* ===================== PHASE 64: the gating engine + the elicitation loop ===================== */
/* the LIVE /gate response: per-case routing + funnel under the default policy (reproduces the baked funnel) */
const GATE_DEFAULT = {
  badge:'Illustrative data & outputs',
  policy:{ thresholds:{high:500, medium:50} },
  funnel:{ 'auto-clear':2, 'review':1, 'human-gate':1 },
  cases:[
    { case_id:'CASE-P-MULE', combo:'C15+C2+C3+C4+C5', n_precedent:4,     baked_n:4,     gate:'human-gate', level:'low' },
    { case_id:'CASE-O-AMB',  combo:'C15+C2+C3+C5',    n_precedent:58,    baked_n:58,    gate:'review',     level:'medium' },
    { case_id:'CASE-P-FP',   combo:'C2+C3',           n_precedent:16856, baked_n:16856, gate:'auto-clear', level:'high' },
    { case_id:'CASE-XSS',    combo:'C2',              n_precedent:1031,  baked_n:1031,  gate:'auto-clear', level:'high' },
  ],
};
/* --- the gating panel renders from the live engine --- */
GATE_RESPONSE = GATE_DEFAULT;
T.setState({ META, QUEUE, FILTER:'all', SIGNALS:false, SEL:null, GATE:null, POLICY:WB_CFG.policy, ADJ:null });
await T.loadGate();
const gp = ELEMENTS.gatePanel._html;
ok(/Gating control/.test(gp), 'the gating control panel renders');
ok(/id="knobHigh"/.test(gp) && /id="knobMed"/.test(gp), 'the policy KNOBS render (auto-clear + review thresholds)');
ok(/Auto-clear at ≥/.test(gp) && /Review at ≥/.test(gp) && /prior firings/.test(gp), 'the knobs are framed as sample-size counts (prior firings)');
ok(/chosen, not measured/.test(gp), 'the panel states the thresholds are chosen, not measured');
ok(/real/.test(gp) && /illustrative/.test(gp), 'the panel states the §12 (real routing) / §14 (illustrative disposition) seam');
ok(/<b>2<\/b> auto-clear/.test(gp) && /<b>1<\/b> review/.test(gp) && /<b>1<\/b> human gate/.test(gp), 'the gating panel shows the live funnel (reproduces the baked funnel under the default policy)');
ok(/high=500/.test(LAST_GATE_URL) && /medium=50/.test(LAST_GATE_URL), '/gate is queried with the policy thresholds');

/* --- the knobs are live: dragging the review threshold re-derives the funnel --- */
GATE_RESPONSE = { ...GATE_DEFAULT, funnel:{ 'auto-clear':2, 'review':2, 'human-gate':0 },
  cases: GATE_DEFAULT.cases.map(c => c.case_id==='CASE-P-MULE' ? { ...c, gate:'review', level:'medium' } : c) };
await T.onKnob('medium', 3);
ok(T.getState().POLICY.thresholds.medium === 3, 'dragging the review knob updates the live policy');
ok(/medium=3\b/.test(LAST_GATE_URL), 'the knob change re-queries /gate with the new threshold');
ok(/<b>0<\/b> human gate/.test(ELEMENTS.gatePanel._html), 'lowering the review threshold folds the rare case out of human-gate (the funnel re-derives live)');
const qLive = ELEMENTS.queue._html;
ok(!/gdot human/.test(qLive), 'the queue re-routes live too — no human-gate dot remains after loosening');

/* --- the ELICITATION LOOP: adjudicate a gated case → grow precedent → re-route live --- */
T.setState({ SEL:'CASE-P-MULE', DETAIL:MULE_DETAIL, SIGNALS:true, GATE:GATE_DEFAULT, POLICY:WB_CFG.policy, ADJ:null, RUN:null });
T.paintSurface();
const sAdj = ELEMENTS.surf._html;
ok(/Adjudicate \(grows precedent\)/.test(sAdj), 'the signals-on surface offers the adjudication control');
ok(/data-disp="cleared"/.test(sAdj) && /data-disp="escalated"/.test(sAdj) && /data-disp="needs_more_info"/.test(sAdj),
   'the adjudication control offers the disposition vocabulary');
ok(/<b>4<\/b> prior firings → Human gate/.test(sAdj), 'before adjudication the case reads its real precedent + the human-gate routing');
/* the server returns the re-route (precedent 4 → 50 crosses the review threshold) */
ADJ_RESPONSE = { badge:'Illustrative data & outputs', case_id:'CASE-P-MULE', combo:'C15+C2+C3+C4+C5',
  before:{ gate:'human-gate', level:'low' }, after:{ gate:'review', level:'medium' }, rerouted:true,
  n_precedent:50, combo_adjudications:1, funnel:{ 'auto-clear':2, 'review':2, 'human-gate':0 },
  cases: GATE_DEFAULT.cases.map(c => c.case_id==='CASE-P-MULE' ? { ...c, n_precedent:50, gate:'review', level:'medium' } : c) };
await T.doAdjudicate('cleared');
const sLoop = ELEMENTS.surf._html;
ok(LAST_ADJ_BODY && LAST_ADJ_BODY.case==='CASE-P-MULE' && LAST_ADJ_BODY.disposition==='cleared',
   'doAdjudicate POSTs the case + disposition to /adjudicate (a NAME, never a cred)');
ok(/re-routed Human gate → Review/.test(sLoop), 'the loop re-routes the case live: human gate → review (precedent crossed the threshold)');
ok(/now <b>50<\/b> prior firings → Review/.test(sLoop), 'the precedent read reflects the grown session sample size');
ok(/<b>1<\/b> recorded this session/.test(sLoop), 'the session adjudication count is shown');
ok(/<b>0<\/b> human gate/.test(ELEMENTS.gatePanel._html), 'the loop shrinks the human-gate funnel as precedent accumulates (judgment concentrates)');

/* --- an unknown/refused adjudication is surfaced, not a crash; nothing claims correctness --- */
ADJ_RESPONSE = { error:"unknown disposition 'definitely-guilty'" };
await T.doAdjudicate('definitely-guilty');
ok(T.getState().ADJ && T.getState().ADJ.error, 'a refused adjudication is captured as an error, not a crash');

/* --- HONESTY re-check over the gating surfaces: still counts-only, no % / lift / correctness claim --- */
const gateRendered = ELEMENTS.gatePanel._html + ELEMENTS.surf._html;
ok(!/\d+(\.\d+)?\s*%/.test(gateRendered) && !/\d+(\.\d+)?x\b/.test(gateRendered),
   'the gating panel + loop render counts only — NO percentage or "Nx" figure');
ok(!/\b(lift|precision|recall|catch[\s-]?rate|f1|auroc)\b/i.test(gateRendered),
   'the gating surfaces carry NO detection-performance vocabulary (routing concentrates judgment, it does not score)');

/* ===================== PHASE 65: the GATHER beat (agentic evidence-gathering loop) ===================== */
/* the panel is always present (the synthetic-provenance string must show BEFORE any gather runs) */
T.setState({ SEL:'CASE-P-MULE', DETAIL:MULE_DETAIL, SIGNALS:true, GATHER:null, RUN:null }); T.paintSurface();
const gp0 = ELEMENTS.surf._html;
ok(/Gather evidence \(synthetic OSINT corpus\)/.test(gp0), 'the GATHER button names the SYNTHETIC corpus substrate (not "external evidence")');
ok(/Synthetic corpus\./.test(gp0) && /NOT a live web search or a real OFAC list/.test(gp0),
   'the GATHER beat shows the always-visible synthetic-provenance string (the ambient badge is not sufficient)');

/* the live gather stream: per-tool stages → grounded findings + a gate rejection + the network */
const GATHER_DONE = {
  badge:'Illustrative data & outputs', subject:'Zane Zhao',
  synthetic_note:'Gathered over a COMMITTED SYNTHETIC OSINT corpus — fictional records, NOT a live web search or a real OFAC list.',
  backend:{ requested:'stub', effective:'stub', note:null },
  grounded:[
    { source_kind:'registry', record_id:'rg-zz-01', entity:'Crescent Dunes Trading FZE',
      quote:'Zane Zhao is recorded as the sole beneficial owner of Crescent Dunes Trading FZE',
      synthesis:'Registry declares an ownership/control tie.', link:'Zane Zhao',
      rel_label:'BENEFICIAL_OWNER', ownership_pct:100, jurisdiction:'AE-RAK (Ras Al Khaimah free zone)' },
    { source_kind:'sanctions', record_id:'sx-cd-01', entity:'Crescent Dunes Trading FZE',
      quote:'Crescent Dunes Trading FZE appears on the OFAC Specially Designated Nationals list',
      synthesis:'An affiliated entity matches a sanctions listing.', link:null },
    { source_kind:'adverse_media', record_id:'am-zz-01', entity:'Zane Zhao <not a tag>',
      quote:'A regional trade outlet named Zane Zhao', synthesis:'Adverse media names the subject.', link:null },
  ],
  dropped:[{ source_kind:'registry', record_id:'rg-zz-01', quote:'this exact phrase is not present',
    reason:'quote did not ground as a real single-sentence substring of the cited record' }],
  graph:{ entities:[{name:'Zane Zhao'},{name:'Crescent Dunes Trading FZE'}],
    relationships:[
      { from:'Zane Zhao', to:'Crescent Dunes Trading FZE', label:'beneficial owner', evidence:'sole beneficial owner of Crescent Dunes Trading FZE', ownership_pct:100 },
      { from:'Zane Zhao', to:'Crescent Dunes Trading FZE', label:'sanctions screen', evidence:'appears on the OFAC Specially Designated Nationals list' }],
    mains:['Zane Zhao'] },
  tools_called:[{tool:'lookup_registry',query:'Zane Zhao',n_records:1},
    {tool:'screen_sanctions',query:'Crescent Dunes Trading FZE',n_records:1},
    {tool:'screen_adverse_media',query:'Zane Zhao',n_records:1}],
  counts:{ grounded:3, dropped:1, tools:3 },
};
const GATHER_MSGS = [
  { stage:'backend', requested:'stub', effective:'stub', note:null },
  { stage:'plan', subject:'Zane Zhao', tools:['screen_sanctions','screen_adverse_media','lookup_registry'] },
  { stage:'tool', tool:'lookup_registry', query:'Zane Zhao', n_records:1 },
  { stage:'findings', tool:'lookup_registry', grounded:1, dropped:1 },
  { stage:'tool', tool:'screen_sanctions', query:'Crescent Dunes Trading FZE', n_records:1 },
  { stage:'findings', tool:'screen_sanctions', grounded:1, dropped:0 },
  { stage:'tool', tool:'screen_adverse_media', query:'Zane Zhao', n_records:1 },
  { stage:'findings', tool:'screen_adverse_media', grounded:1, dropped:0 },
  { done: GATHER_DONE },
];
GATHER_CHUNKS = ndjsonChunks(GATHER_MSGS, 45);
await T.runGather();
const gg = ELEMENTS.surf._html;
ok(LAST_GATHER_BODY && LAST_GATHER_BODY.case === 'CASE-P-MULE', 'runGather POSTs the case to /gather (a NAME, never a cred)');
ok(/registry lookup · 1 record\b/.test(gg) && /sanctions screen · 1 record/.test(gg),
   'the gather stages reveal per-tool completion (stage-completion, not a token stream)');
ok((gg.match(/class="gfind"/g)||[]).length === 3, 'three grounded findings render');
ok(/Evidence · verbatim from a synthetic record/.test(gg), 'each grounded finding labels its quote as verbatim EVIDENCE');
ok(/Crescent Dunes Trading FZE appears on the OFAC/.test(gg), 'the chained sanctions finding renders its grounded quote (the registry→sanctions chain)');
ok(/illustrative reading — not verified/.test(gg), 'the synthesis is labeled an illustrative, unverified reading (subordinate to the grounded quote)');
ok(/rejected by the gate/.test(gg) && /did not ground/.test(gg), 'the ungrounded finding renders WITH its rejection reason (the gate firing is legible)');
ok(/authored over synthetic records, not discovered/.test(gg), 'the network is labeled authored-not-discovered (the chain is not framed as a real discovery)');
ok(/class="gnsvg"/.test(gg) && (gg.match(/class="gge"/g)||[]).length >= 1, 'the network graph renders as a deterministic SVG with grounded edges');
/* Phase 66 — the ownership mirror: the RelationshipEdge label + ownership_pct render (as "N pct", never "N%") */
ok(/class="grel"/.test(gg) && /beneficial owner/.test(gg) && /100 pct/.test(gg),
   'an ownership finding renders the RelationshipEdge label + ownership_pct as "N pct" (mirrors the substrate BO graph)');
ok(/class="gjur"/.test(gg) && /AE-RAK/.test(gg), 'the ownership finding shows its jurisdiction chip');
ok(/beneficial owner · 100 pct/.test(gg), 'the network edge is labeled by the ownership relationship + the pct');
ok(!/Zane Zhao <not a tag>/.test(gg) && gg.includes('&lt;not a tag&gt;'), 'XSS: a malicious gathered entity is esc()-escaped');

/* HONESTY re-check over the gather surface — counts only, NO % / lift / detection vocabulary */
ok(!/\d+(\.\d+)?\s*%/.test(gg) && !/\d+(\.\d+)?x\b/.test(gg), 'the gather surface renders no % / "Nx" figure');
ok(!/\b(lift|precision|recall|catch[\s-]?rate|f1|auroc)\b/i.test(gg),
   'the gather surface carries NO detection-performance vocabulary (gather-and-ground, it does not score)');

/* clicking a network edge reveals its grounded evidence quote */
const stG = T.getState(); stG.GATHER.gsel = 0; T.setState({ GATHER: stG.GATHER }); T.paintSurface();
ok(/class="gerow open"/.test(ELEMENTS.surf._html) && /class="gev"/.test(ELEMENTS.surf._html),
   'selecting a network edge reveals its grounded evidence quote');

/* the false-positive-trap honest negative: a gather that grounds NOTHING reads "no external findings" */
const EMPTY_DONE = { ...GATHER_DONE, subject:'Liam Jain', grounded:[], dropped:[],
  graph:{ entities:[{name:'Liam Jain'}], relationships:[], mains:['Liam Jain'] }, counts:{grounded:0,dropped:0,tools:3} };
T.setState({ GATHER:{ caseId:'CASE-P-MULE', stages:[], done:EMPTY_DONE, error:null, running:false, gsel:null } }); T.paintSurface();
ok(/No external findings grounded/.test(ELEMENTS.surf._html), 'an honest empty result reads "no external findings" (the false-positive-trap payoff)');

/* a gather transport failure renders a NAMED error, not a crash */
T.setState({ GATHER:{ caseId:'CASE-P-MULE', stages:[], done:null, error:'could not reach the workbench companion', running:false } }); T.paintSurface();
ok(/Gather failed/.test(ELEMENTS.surf._html) && !/class="gfind"/.test(ELEMENTS.surf._html),
   'a gather transport failure renders the named error banner (no findings, not a crash)');

/* ---------- summary ---------- */
console.log(`\n${pass} passed, ${fails.length} failed`);
if (fails.length){ console.error('FAILURES:\n  - ' + fails.join('\n  - ')); process.exit(1); }
