#!/usr/bin/env node
// Chain-workbench harness — ZERO runtime deps (Node built-in `vm` + a hand-rolled DOM/fetch shim).
// Run: `node tests/chain.test.mjs`.
//
// chain.html is NOT a build target (no dist/ — it is companion-served by scripts/serve_chain.py), so
// this loads the RAW template, injects nothing (the client falls back to default endpoints), shims
// fetch to STREAM synthetic NDJSON stages, evaluates the inline <script> under a small DOM shim, and
// asserts: the case library renders, the four-stage ledger reveals progressively (stage rendering — not
// a token stream), the CONNECTED payoff shows the signed SAR + the flag→corpus audit walk, the
// always-on badge, esc() as the sole escaper (XSS), and line-buffered NDJSON consumption (a stage line
// split across two stream chunks).

import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';
import vm from 'node:vm';

const HERE = dirname(fileURLToPath(import.meta.url));
const CHAIN = resolve(HERE, '..', 'chain.html');

let pass = 0; const fails = [];
function ok(cond, msg){ if (cond){ pass++; console.log(`  ✓ ${msg}`); } else { fails.push(msg); console.log(`  ✗ ${msg}`); } }
function escH(s){return String(s==null?'':s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;').replace(/'/g,'&#39;');}

/* ---------- load + structural checks on the raw template ---------- */
const html = readFileSync(CHAIN, 'utf8');
ok(html.includes('<!--__CHAIN_CONFIG__-->'), 'raw chain.html carries exactly the config marker serve_chain replaces');
ok((html.match(/<!--__CHAIN_CONFIG__-->/g)||[]).length === 1, 'exactly one config marker');
ok(/Illustrative data &amp; outputs/.test(html), 'always-on "Illustrative data & outputs" badge present in the markup');
ok((html.match(/<script>/g)||[]).length === 1, 'exactly one inline <script> (the workbench client)');

const open = html.indexOf('<script>'), close = html.lastIndexOf('</script>');
const SCRIPT = html.slice(open + '<script>'.length, close)
  + `\n;globalThis.__T={esc,caseCardHTML,renderCases,selectCase,runCase,applyMessage,paint,`
  + `auditWalkHTML,sarHTML,loadCases,getCASES:()=>CASES,getSTATE:()=>STATE};`;

/* ---------- DOM + fetch shim ---------- */
function makeEl(id){
  return {
    id, _html:'', _text:'', dataset:{}, onclick:null,
    set innerHTML(v){ this._html = String(v); }, get innerHTML(){ return this._html; },
    set textContent(v){ this._text = String(v); }, get textContent(){ return this._text; },
    set className(v){ this._class = String(v); },
    classList:{ add(){}, remove(){}, toggle(){}, contains(){ return false; } },
    querySelector(){ return { onclick:null, classList:{ toggle(){} }, dataset:{} }; },
    querySelectorAll(sel){
      // .ccard lookups in selectCase — return a stub per data-case in this element's html
      const out = []; const re = /data-case="([^"]*)"/g; let m;
      while ((m = re.exec(this._html))) out.push({ dataset:{ case:m[1] }, classList:{ toggle(){} } });
      return out;
    },
  };
}
const ELEMENTS = {};
['caseList','run','badge','draftChip','foot'].forEach(id => ELEMENTS[id] = makeEl(id));
const documentShim = { getElementById(id){ return ELEMENTS[id] || (ELEMENTS[id] = makeEl(id)); } };

// a streaming Response over a list of byte chunks (the fetch ReadableStream contract chain.html reads)
function streamResponse(chunks){
  let i = 0;
  return { ok:true, body:{ getReader(){ return { read(){
    return Promise.resolve(i < chunks.length ? { done:false, value:chunks[i++] } : { done:true, value:undefined });
  } }; } } };
}
const enc = new TextEncoder();
function ndjsonChunks(objs, splitAt){
  // serialize to lines, then optionally split ONE line across two chunks (prove the line buffer)
  const text = objs.map(o => JSON.stringify(o)).join('\n') + '\n';
  if (splitAt == null) return [enc.encode(text)];
  return [enc.encode(text.slice(0, splitAt)), enc.encode(text.slice(splitAt))];
}

let CASES_RESPONSE = { badge:'Illustrative data & outputs', cases:[] };
let RUN_CHUNKS = [];
function fetchShim(url, opts){
  if (String(url).includes('/cases')) return Promise.resolve({ ok:true, json:()=>Promise.resolve(CASES_RESPONSE) });
  if (String(url).includes('/run'))   return Promise.resolve(streamResponse(RUN_CHUNKS));
  return Promise.reject(new Error('unexpected url '+url));
}

const sandbox = { document:documentShim, window:{}, fetch:fetchShim,
  TextDecoder, TextEncoder, Uint8Array, JSON, Promise, setTimeout, console };
sandbox.globalThis = sandbox;
vm.createContext(sandbox);
vm.runInContext(SCRIPT, sandbox);
const T = sandbox.__T;

/* ---------- esc() is the sole escaper ---------- */
ok(T.esc('<b>&"\'') === '&lt;b&gt;&amp;&quot;&#39;', 'esc() encodes <,>,&,",\' (the one escaper)');

/* ---------- case library renders + escapes (XSS) ---------- */
const CASES = [
  { case_id:'CASE-P-0010361', title:'Multi-typology mule', summary:'one account, five composed signals',
    alert_count:5, txn_count:71,
    capabilities:[{capability:'C4'},{capability:'C3'},{capability:'C2'},{capability:'C5'},{capability:'C15'}],
    provenance:{ substrate_repo:'aml-substrate', substrate_head:'df23bba' } },
  { case_id:'CASE-XSS', title:'<img src=x onerror=alert(1)>', summary:'<script>steal()</script>',
    alert_count:0, txn_count:0, capabilities:[{capability:'<b>C9</b>'}], provenance:{} },
];
T.renderCases(CASES);
const listHTML = ELEMENTS.caseList._html;
ok(/Multi-typology mule/.test(listHTML), 'case library renders a case card title');
ok(/data-case="CASE-P-0010361"/.test(listHTML), 'case card carries its data-case id');
ok(/aml-substrate@df23bba/.test(listHTML), 'provenance pin (substrate@HEAD) renders on the card');
ok(!/<img src=x onerror/.test(listHTML) && listHTML.includes(escH('<img src=x onerror=alert(1)>')),
   'XSS: a malicious case title is esc()-escaped, not injected');
ok(!/<script>steal/.test(listHTML), 'XSS: a malicious summary is escaped');

/* ---------- stage-rendering contract: progressive reveal via applyMessage ---------- */
T.selectCase('CASE-P-0010361');
ok(/Run the chain/.test(ELEMENTS.run._html), 'selecting a case shows the Run control + the (pending) ledger');
ok((ELEMENTS.run._html.match(/class="node /g)||[]).length === 4, 'the ledger has the four canonical stage nodes');

T.applyMessage({ stage:'evidence', case_id:'CASE-P-0010361', alert_count:5, txn_count:71,
  capabilities:['C4','C3','C2','C5','C15'], subject:{ account_id:'A-00038593' } });
ok(/5<\/b> alerts/.test(ELEMENTS.run._html) && /71<\/b> transactions/.test(ELEMENTS.run._html),
   'evidence stage renders the bundle shape (alerts + txns)');
ok(/A-00038593/.test(ELEMENTS.run._html), 'evidence stage names the subject account');

T.applyMessage({ stage:'consume', drafter:'stub', status:'running' });
ok(/node active/.test(ELEMENTS.run._html.split('Consume')[0].split('node').slice(-1)[0]) ||
   /class="node active"/.test(ELEMENTS.run._html), 'a running stage marks its node active');

T.applyMessage({ stage:'consume', status:'done', drafter:'stub', drafter_effective:'stub', signed:true,
  blocking_violations:[], narrative_present:true,
  completeness:{ reporting_entity:true, transaction_details:true, account_information:true,
    subject_information:true, typology_grounds:true, grounds_for_suspicion_narrative:true } });
ok(/deterministic stub/.test(ELEMENTS.run._html), 'consume stage shows the drafter (stub) used');
ok(/✓ signed/.test(ELEMENTS.run._html) && /0 blocking/.test(ELEMENTS.run._html),
   'consume stage shows signed + zero blocking violations (the six-verifier gate)');
ok((ELEMENTS.run._html.match(/class="vchk"/g)||[]).length === 6, 'consume stage lists the six completeness elements');

T.applyMessage({ stage:'verify', status:'done', connected:true, exit:0 });
ok(/join verified/.test(ELEMENTS.run._html), 'verify stage renders the cross-pillar result');

T.applyMessage({ stage:'connected', connected:true });
ok(/class="node connected"/.test(ELEMENTS.run._html), 'the connected node lights on CONNECTED');

/* ---------- full NDJSON stream consumption (line split across chunks) + CONNECTED payoff ---------- */
const SUBJ = 'A-00038593';
const DONE = {
  case:{ case_id:'CASE-P-0010361', title:'Multi-typology mule', summary:'…' },
  signed_sar:{ str_record:{
    narrative:'Account A-00038593 exhibits a multi-typology laundering pattern. <not a tag>',
    narrative_claims:[{ text:'Sub-$10,000 cash deposits indicate structuring.', cites:['fin-2026-alert001:IND-11'] }] } },
  audit_walk:[
    { capability:'C4', detector:'structuring', signal_id:'fin-2026-alert001:IND-11', source:'fincen-alerts',
      corpus_flag:'engages in structuring with multiple cash transactions for under $10,000',
      red_flag:'CTR-trigger evasion: sub-$10K cash structuring', grounded:true },
    { capability:'C15', detector:'shell_nominee', signal_id:'fin-2023-alert006:IND-04', source:'fincen-alerts',
      corpus_flag:'entities that are shell corporations', red_flag:'Shell/nominee throughput', grounded:true },
  ],
  connected:true,
};
const RUN_MSGS = [
  { stage:'evidence', case_id:'CASE-P-0010361', alert_count:5, txn_count:71, capabilities:['C4'], subject:{ account_id:SUBJ } },
  { stage:'consume', status:'running', drafter:'stub' },
  { stage:'consume', status:'done', drafter:'stub', drafter_effective:'stub', signed:true, blocking_violations:[],
    narrative_present:true, completeness:{ reporting_entity:true, transaction_details:true, account_information:true,
      subject_information:true, typology_grounds:true, grounds_for_suspicion_narrative:true } },
  { stage:'verify', status:'done', connected:true, exit:0 },
  { stage:'connected', connected:true },
  { done: DONE },
];
T.selectCase('CASE-P-0010361');
RUN_CHUNKS = ndjsonChunks(RUN_MSGS, 40);   // split the first line mid-way → exercises the line buffer
await T.runCase();
const finalHTML = ELEMENTS.run._html;
ok(/class="node connected"/.test(finalHTML), 'streamed run reaches the CONNECTED node');
ok(/Signed SAR/.test(finalHTML) && /multi-typology laundering pattern/.test(finalHTML),
   'CONNECTED payoff renders the signed-SAR narrative');
ok(finalHTML.includes(escH('<not a tag>')), 'XSS: the model narrative is esc()-escaped');
ok(/Audit walk/.test(finalHTML), 'the flag→corpus audit walk renders');
ok((finalHTML.match(/class="wrow"/g)||[]).length === 2, 'audit walk renders one row per grounded alert');
ok(/fin-2026-alert001:IND-11/.test(finalHTML) && /fincen-alerts/.test(finalHTML),
   'audit walk shows the signal_id and its source regulator');
ok(/under \$10,000/.test(finalHTML), 'audit walk quotes the verbatim corpus flag');
ok((finalHTML.match(/✓ grounded/g)||[]).length >= 2, 'every walked alert shows a grounded check');
const st = T.getSTATE();
ok(st && st.done && st.connected !== false && st.running === false, 'run settles: state has the done payload, not running');

/* ---------- error / gated path ---------- */
T.selectCase('CASE-P-0010361');
RUN_CHUNKS = ndjsonChunks([{ error:'casework consume failed (bridge gated)' }]);
await T.runCase();
ok(/Run gated \/ failed/.test(ELEMENTS.run._html) && /bridge gated/.test(ELEMENTS.run._html),
   'an in-stream error renders the named gated/failed banner');

/* ---------- loadCases via the shimmed /cases endpoint ---------- */
CASES_RESPONSE = { badge:'Illustrative data & outputs', cases:[CASES[0]] };
await T.loadCases();
ok(/Multi-typology mule/.test(ELEMENTS.caseList._html), 'loadCases() fetches /cases and renders the library');

/* ---------- summary ---------- */
console.log(`\n${pass} passed, ${fails.length} failed`);
if (fails.length){ console.error('FAILURES:\n  - ' + fails.join('\n  - ')); process.exit(1); }
