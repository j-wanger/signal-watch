#!/usr/bin/env node
// Adverse-media / negative-news stream arc harness (Phase 31, M8) — ZERO runtime deps (Node built-in
// `vm` + a hand-rolled DOM shim; no third-party DOM library, no npm install). Run:
//   node tests/news-stream.test.mjs
//
// What it does: loads the COMMITTED dist/news/index.html (so it doubles as a build-output smoke test —
// `build.py --check all` already guarantees that file equals a fresh build of news.html), extracts the
// single inline <script>, evaluates it under the shim in BOTH motion modes, then drives the screening arc
// (Select → Read → Screen → Disposition → Close) and asserts:
//   - the fuzzy matcher (normalize → token-sort → Jaro-Winkler) surfaces the seeded NEAR-matches an
//     exact-name screen would miss (Volkoff ~0.977, Dmitri ~0.921, word-order Van Thanh = 1.0) and the
//     exact matches (Aurelia, Greenfield), at the inlined threshold;
//   - the common-name FALSE-POSITIVE trap (Andrei Petrov, score 1.0, a DIFFERENT person) surfaces but is
//     DISMISSABLE at the human gate, and dismissing it drops the confirmed-exposure count;
//   - the Read screen highlights grounded red-flag phrases + tags entities + shows the red_flag translation;
//   - the always-on illustrative badge is present and no fabricated precision/lift number is claimed
//     (scores are the real computed string-similarity);
//   - reduced-motion settles on the final state (the stream has no animation — both modes render identically,
//     no thrown errors).
//
// Why a vm + shim instead of a third-party DOM library: the ship artifact is a single file:// offline HTML;
// the project's whole test idiom is dep-free. news.html's DOM surface is tiny (getElementById /
// querySelectorAll / matchMedia / addEventListener, innerHTML-driven, no layout reads), so a small shim
// covers it. The script declares everything top-level, so an appended epilogue re-exports the state +
// render fns + the matcher — letting us drive the arc AND read the real fuzzy-match results.

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

// always-on badge lives in the static HTML head (the chrome), not the inlined script
ok(/class="badge"/.test(html) && /Illustrative data/.test(html), 'always-on illustrative badge present in the ship chrome');

/* ---------- a minimal DOM/window shim ---------- */
function makeEnv(reduced) {
  let cache = {}, qcache = {};
  const mkPseudo = (attrs) => {
    const ds = {}; let d; const dRe = /data-([a-z0-9-]+)="([^"]*)"/gi;
    while ((d = dRe.exec(attrs))) ds[d[1].replace(/-([a-z])/g, (_, c) => c.toUpperCase())] = d[2];
    let click = null;
    return {
      dataset: ds, _click() { if (click) click({ preventDefault() {} }); },
      addEventListener(t, f) { if (t === 'click') click = f; },
      getAttribute(n) { const m = new RegExp(n.replace(/-/g, '\\-') + '="([^"]*)"').exec(attrs); return m ? m[1] : null; },
      setAttribute() {}, textContent: '',
    };
  };
  let app;
  const qsa = (sel) => {
    if (qcache[sel]) return qcache[sel];
    const cls = sel.replace(/^\./, ''); const out = []; const h = app._html;
    const tagRe = /<([a-z]+)([^>]*)>/gi; let m;
    while ((m = tagRe.exec(h))) { const c = /class="([^"]*)"/.exec(m[2]); if (c && c[1].split(/\s+/).includes(cls)) out.push(mkPseudo(m[2])); }
    return (qcache[sel] = out);
  };
  const mkChrome = (id) => ({
    id, _html: '', textContent: '',
    get innerHTML() { return this._html; },
    set innerHTML(v) { this._html = String(v); cache = {}; qcache = {}; },
    querySelectorAll: qsa, addEventListener() {}, setAttribute() {}, getAttribute() { return null; },
  });
  const persistent = {}; for (const id of ['app', 'badge', 'brand', 'brandsub', 'foot']) persistent[id] = mkChrome(id);
  app = persistent.app;
  const gid = (id) => {
    if (persistent[id]) return persistent[id];
    if (!(id in cache)) { const re = new RegExp('<([a-z]+)([^>]*\\sid="' + id + '"[^>]*)>', 'i'); const m = re.exec(app._html); cache[id] = m ? mkPseudo(m[2]) : null; }
    return cache[id];
  };
  const document = { getElementById: gid, querySelectorAll: qsa, addEventListener() {} };
  const window = { matchMedia: () => ({ matches: reduced }), scrollTo() {} };
  return { document, window, app };
}

function boot(reduced) {
  const env = makeEnv(reduced);
  const ctx = vm.createContext({ window: env.window, document: env.document, console });
  let threw = null;
  try {
    vm.runInContext(SCRIPT + '\n;globalThis.__t={go,state,matchEntities,articleById,STEP};', ctx);
  } catch (e) { threw = e; }
  return { env, ctx, threw };
}

/* ===================== reduced-motion mode (primary drive) ===================== */
console.log('\n[reduced-motion] boot + drive the arc');
{
  const { env, ctx, threw } = boot(true);
  ok(!threw, 'engine evaluates without throwing' + (threw ? ` (${threw})` : ''));
  const app = env.app;
  ok(/Adverse-media exposure stream/.test(app._html), 'boot → Select screen renders');
  ok(/Shell network relabeled/.test(app._html), 'Select lists the marquee article');
  ok(env.document.querySelectorAll('.card').length === 4, 'Select shows 4 article cards');

  // ---- matcher correctness (the new muscle) ----
  const a = ctx.__t.articleById('trade-shell-001');
  const m = ctx.__t.matchEntities(a);
  const by = Object.fromEntries(m.map(x => [x.entity.name, x]));
  approx(by['Volkov Maritime Logistics'].score, 0.977, 0.02, 'Volkoff near-match score');
  ok(by['Volkov Maritime Logistics'].kind === 'near' && by['Volkov Maritime Logistics'].hit, 'Volkoff classified near + surfaces');
  approx(by['Dmitri Karpov'].score, 0.921, 0.03, 'Dmitri Karpov near-match score');
  ok(by['Dmitri Karpov'].kind === 'near', 'Dmitri Karpov classified near');
  ok(by['Aurelia Holdings Ltd'].kind === 'exact' && by['Aurelia Holdings Ltd'].score === 1, 'Aurelia exact match (1.0)');
  ok(by['Andrei Petrov'].score === 1 && by['Andrei Petrov'].hit, 'Andrei Petrov common-name trap surfaces at 1.000');
  ok(by['Eastgate Freight Forwarding'].hit === false, 'Eastgate (no book entry) does NOT surface — discriminates');
  ok(m.filter(x => x.hit).length === 4, 'marquee yields 4 hits (3 true + 1 trap)');
  // a near-match is the wow: a hit that exact-string matching would have missed
  ok(m.some(x => x.hit && !x.exact), 'at least one surfaced hit is a NEAR-match (exact-name screen would miss it)');

  // word-order robustness in a second article
  const m2 = ctx.__t.matchEntities(ctx.__t.articleById('mule-romance-002'));
  const vt = m2.find(x => x.entity.name === 'Nguyen Van Thanh');
  ok(vt && vt.hit && vt.score === 1, 'word-order near-match (Nguyen Van Thanh ↔ Van Thanh Nguyen) = 1.0 via token-sort');

  // ---- drive the arc ----
  ctx.__t.go('read', 'trade-shell-001');
  ok(/class="hl"/.test(app._html), 'Read highlights grounded red-flag phrases');
  ok(/class="ent"/.test(app._html), 'Read tags named entities');
  ok(/Over-invoicing/.test(app._html), 'Read shows a red_flag translation beside the verbatim');
  ok(/300 percent/.test(app._html), 'Read renders the verbatim grounded flag');

  env.document.getElementById('nav-next')._click();
  ok(/Screen against the book/.test(app._html), '→ Screen renders');
  ok(/0\.977/.test(app._html), 'Screen shows the real computed near-match score (0.977)');
  ok(/near-match/.test(app._html), 'Screen notes a near-match an exact-name screen would miss');
  // honesty: no fabricated precision/lift % anywhere in the rendered stream
  ok(!/\b\d{1,3}%/.test(app._html), 'Screen claims no fabricated precision/lift percentage');

  env.document.getElementById('nav-next')._click();
  ok(/Disposition/.test(app._html), '→ Disposition renders (the human gate)');
  let toggles = env.document.querySelectorAll('.hitbtn');
  ok(toggles.length === 4, 'Disposition shows one toggle per surfaced hit (4)');
  ok(/CONFIRMED/.test(app._html), 'hits default to CONFIRMED (agent proposes, human disposes)');
  const trapKey = 'trade-shell-001|' + by['Andrei Petrov'].entity.id;   // dispo keyed per entity
  const trap = toggles.find(t => t.getAttribute('data-k') === trapKey);
  ok(!!trap, 'the common-name trap toggle is present');
  trap._click();
  ok(/DISMISSED/.test(app._html), 'dismissing the trap flips it to DISMISSED');

  env.document.getElementById('nav-next')._click();
  ok(/Exposure/.test(app._html), '→ Close renders');
  const flat = app._html.replace(/\s+/g, '');
  const confTile = /(\d+)<\/div><divclass="l">confirmedexposures/.exec(flat);
  ok(confTile && confTile[1] === '3', 'confirmed exposures = 3 after dismissing the trap');
  const dismTile = /(\d+)<\/div><divclass="l">dismissed/.exec(flat);
  ok(dismTile && dismTile[1] === '1', 'dismissed (false positive) = 1');
  ok(/adverse-media <b>atom<\/b>/.test(app._html), 'Close names the atoms/composition north star');

  // Esc returns to Select
  ok(/Articles/.test(app._html), 'Close keeps the Articles breadcrumb/return path');
}

/* ===================== full-motion mode (parity / no-error) ===================== */
console.log('\n[full-motion] boot + one pass — parity, no errors');
{
  const { env, ctx, threw } = boot(false);
  ok(!threw, 'engine evaluates without throwing (full-motion)' + (threw ? ` (${threw})` : ''));
  const app = env.app;
  ok(/Adverse-media exposure stream/.test(app._html), 'full-motion boot → Select renders identically');
  let threw2 = null;
  try {
    ctx.__t.go('read', 'prof-ml-004');
    env.document.getElementById('nav-next')._click();   // screen
    env.document.getElementById('nav-next')._click();   // disposition
    env.document.getElementById('nav-next')._click();   // close
  } catch (e) { threw2 = e; }
  ok(!threw2, 'full-motion arc drive throws no error' + (threw2 ? ` (${threw2})` : ''));
  ok(/Exposure/.test(app._html), 'full-motion reaches Close');
  // prof-ml-004: Greenfield exact + Marcus Bellwether near = 2 confirmed by default
  const flat = app._html.replace(/\s+/g, '');
  const conf = /(\d+)<\/div><divclass="l">confirmedexposures/.exec(flat);
  ok(conf && conf[1] === '2', 'prof-ml-004 close: 2 confirmed (Greenfield exact + Bellwether near)');
}

console.log(`\n${pass} passed, ${fails.length} failed`);
if (fails.length) { console.error('\nFAILURES:\n  - ' + fails.join('\n  - ')); process.exit(1); }
