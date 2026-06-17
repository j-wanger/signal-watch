#!/usr/bin/env node
// Launcher arc regression harness — ZERO runtime deps (Node built-in `vm` + a minimal DOM shim;
// no third-party DOM library, no npm install). Run: `node tests/launcher.test.mjs`.
//
// What it does: loads launcher.html (the TEMPLATE — the 8th single-file offline artifact, the front
// door), asserts it is self-contained (no fetch / external script / ES module), carries the always-on
// badge and relative links to all 5 existing artifacts (7 dist entry points), then injects a controlled
// STUB cross-pillar status at __STATUS__ (so the harness owns the XSS strings + the state words),
// evaluates the inline script under the shim, and asserts:
//   - renderStatus() renders the three bridge states (pending/done/failed) with the right CSS class;
//   - esc() is the sole escaper — a <script> / & / < in a status detail renders ESCAPED, never raw;
//   - metaLine() surfaces the spine state + both grounding HEADs;
//   - the prefers-reduced-motion CSS branch is present.

import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';
import vm from 'node:vm';

const HERE = dirname(fileURLToPath(import.meta.url));
const TEMPLATE = resolve(HERE, '..', 'launcher.html');
const PLACEHOLDER = '__STATUS__';

let pass = 0;
const fails = [];
function ok(cond, msg) {
  if (cond) { pass++; console.log(`  ✓ ${msg}`); }
  else { fails.push(msg); console.log(`  ✗ ${msg}`); }
}

const raw = readFileSync(TEMPLATE, 'utf8');

/* ---------- static (source) assertions ---------- */
ok(!/fetch\(/.test(raw) && !/<script src/.test(raw) && !/type="module"/.test(raw),
  'template is self-contained (no fetch / external script / ES module)');
ok(/Illustrative data &amp; outputs/.test(raw), 'always-on Illustrative badge present');
const links = [...raw.matchAll(/href="([a-z-]+\/index\.html)"/g)].map(m => m[1]);
for (const a of ['fentanyl', 'trade-based', 'elder-financial-exploitation', 'corpus', 'news', 'console', 'triage']) {
  ok(links.includes(`${a}/index.html`), `links the ${a} artifact (relative, file:// safe)`);
}
ok(/prefers-reduced-motion/.test(raw), 'prefers-reduced-motion CSS branch present');
ok(raw.split(PLACEHOLDER).length - 1 === 1, `exactly one ${PLACEHOLDER} injection placeholder`);

/* ---------- the controlled stub (the harness owns the edge cases) ---------- */
const STUB = {
  illustrative: true, phase: '55',
  grounding_heads: { aml_substrate: 'bafc67d', aml_casework: '0316580' },
  spine: { state: 'proven', detail: 'selftest green on the synthetic C4 fixture' },
  bridges: {
    bridge_1_persist: { state: 'pending', detail: '<script>alert(1)</script> persist & emit' },
    bridge_2_consume: { state: 'done', detail: 'consumed a real bundle' },
    e2e_real: { state: 'failed', detail: 'x & y < z' },
  },
};

/* ---------- evaluate the inline script under a minimal DOM shim ---------- */
const scriptSrc = raw.match(/<script>([\s\S]*?)<\/script>/)[1].replace(PLACEHOLDER, JSON.stringify(STUB));
const nodes = {};
function fakeNode() { return { _html: '', textContent: '', get innerHTML() { return this._html; }, set innerHTML(v) { this._html = String(v); } }; }
let api = null;
const sandbox = {
  document: { getElementById: (id) => (nodes[id] = nodes[id] || fakeNode()) },
  window: { __capture: (a) => { api = a; } },
};
vm.createContext(sandbox);
vm.runInContext(scriptSrc, sandbox);

ok(api && typeof api.renderStatus === 'function', 'inline script exposes renderStatus via __capture');

const html = api.renderStatus(STUB);
ok(/pending/.test(html) && /done/.test(html) && /failed/.test(html), 'renders all three bridge state words');
ok(/class="bridge ok"/.test(html), 'done -> .ok class');
ok(/class="bridge bad"/.test(html), 'failed -> .bad class');
ok(/class="bridge pending"/.test(html), 'pending -> .pending class');
ok(/Substrate persists/.test(html) && /Casework consumes/i.test(html), 'renders the bridge labels');

// XSS: the sole escaper neutralizes hostile status text — raw markup must NOT survive
ok(!/<script>alert\(1\)<\/script>/.test(html), 'raw <script> from status detail does NOT survive (esc neutralizes)');
ok(/&lt;script&gt;alert\(1\)&lt;\/script&gt;/.test(html), 'the script tag renders ESCAPED');
ok(/x &amp; y &lt; z/.test(html), 'ampersand + angle-bracket in a detail render escaped');
ok(api.esc("<b>&'\"") === '&lt;b&gt;&amp;&#39;&quot;', 'esc() escapes < > & \' "');

// the bridges container actually received the rendered html (the IIFE wired it)
ok(nodes.bridges && /class="bridge/.test(nodes.bridges.innerHTML), 'IIFE injects renderStatus output into #bridges');

const meta = api.metaLine(STUB);
ok(/proven/.test(meta) && /bafc67d/.test(meta) && /0316580/.test(meta), 'metaLine surfaces spine state + both grounding HEADs');

/* ---------- tally ---------- */
console.log(`\n${pass} passed, ${fails.length} failed`);
if (fails.length) { for (const f of fails) console.error(`FAIL: ${f}`); process.exit(1); }
