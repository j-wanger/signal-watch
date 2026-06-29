# Signal Watch — AML Vision Demo
## Claude Code Project Handoff & Bootstrap

> ⚠️ **HISTORICAL — a frozen M0-bootstrap handoff (its content was last current ~Phase 54).** This document
> captured the project's *starting point* and early milestone plan; it is **NOT current state**. The repo is
> now at **Phase 66**, with five offline ship artifacts (showcase / corpus / news / console / triage) plus
> the companion investigator workbench and a 3-pillar program — a different shape and run story than the §7
> "How to run" skeleton and §8/§9 milestone/backlog below describe.
> **For current state, read instead:** `README.md` (the run story), `CLAUDE.md` (architecture +
> non-negotiables, self-maintained each phase), `docs/` (per-subsystem detail), `.dev-wiki/` (phase history).
> Keep this only for origin/intent context (the POC 5→1→3 framing, the original "shipped" definition).

> **Purpose of this doc:** bring a fresh Claude Code session up to speed to formally **ship** the interactive vision demo as a maintained project.
> **What you are inheriting:** a single self-contained HTML file (`aml_vision_demo_fentanyl.html`) — a working, fully-scripted, six-act interactive walkthrough of the target AML detection loop.
> **Upstream context (read if available):** `AML_signal_atom_transformation_handoff.md` (the program framework this demo dramatizes) and the transformation blueprint HTML. The demo is the *felt experience* of **POC 5 → POC 1 → POC 3** from that framework. Keep vocabulary consistent with it (atoms, composition, promotion gate, etc.).
> **Status tags used below:** **[SETTLED]** (do not reverse without explicit ask) · **[PLANNED]** · **[OPEN]** (needs a human decision).

---

## 1. What this demo is, and what "shipped" means

### 1.1 What it is
A presenter-driven, browser-based **vision prototype** used to get stakeholder buy-in for an AML signal/atom monitoring transformation. It is **not** a working detection system; it is a scripted, reliable dramatization of the end-to-end loop:

> read a regulatory advisory → extract candidate signals → assess coverage against our library + data → **human selects** what to build → agent drafts a signal definition → **human confirms** → backtest → reveal **combination lift** → coverage closes → loop repeats.

It opens on a "what aren't we watching?" coverage map (the missed-monitoring / TD anxiety made visual), and the two moments designed to win the room are the **two human-in-the-loop gates** (trust) and the **combination-lift reveal** (why atoms beat monolithic scenarios).

### 1.2 Definition of "shipped" (the goal of this project)
A demo that is:
1. **Reliable on stage** — runs offline from a laptop, never fails live, scripted fallback for any optional live call.
2. **Multi-typology** — fentanyl plus at least one more anchor (pig-butchering and/or trade-based), switchable from config, not forked code.
3. **Config-driven & maintainable** — content lives in typology config files; the engine is generic.
4. **Presenter-ready** — keyboard navigation, reset, optional speaker notes; clean on the actual presentation browser.
5. **Compliance-clean** — no real customer/transaction data anywhere; advisory text public-source and paraphrased; figures clearly labelled illustrative.
6. **Documented & handed off** — README with run/present instructions; this project becomes self-sustaining.

**[OPEN] decisions the human (Jake) should confirm early:** (a) ship as a single self-contained file vs a hosted page; (b) for the actual presentation — fully scripted, pre-generated, or live; (c) which typologies; (d) whether to add a closing "what it takes to build this / the ask" slide.

---

## 2. Current state — what you're starting from

- **One file**, `aml_vision_demo_fentanyl.html`. Vanilla HTML/CSS/JS, **no build step, no dependencies** except a Google Fonts `<link>` (Newsreader / Archivo / JetBrains Mono).
- **Already data-driven.** Content lives in JS arrays at the top of the `<script>`; render functions read from them. This is the single most important property to preserve — it's what makes config-driven multi-typology cheap.
- **Architecture inside the file:**
  - Content arrays: `STEPS`, `INDICATORS`, `ADVISORY`, `CANDIDATES`, `LIFT`, plus label/hint arrays.
  - A small **state machine**: `act`, `selected`, `confirmed`; functions `goto(i)`, `updateControls()`, and `act0()`…`act6()` render functions dispatched via a `RENDER` array.
  - Theme entirely in `:root` CSS variables (dark "dossier" aesthetic; `--signal` amber accent).
  - The two gates are real interactions: Act 3 selection (Next disabled with zero selected), Act 4 confirm (drives a build animation then advances).
- **Known good behaviours to preserve:** streamed advisory text with highlighted phrases; staggered signal extraction; animated coverage gauge; animated lift bars; the persistent **"Illustrative data & outputs"** badge.

---

## 3. Target project shape

### 3.1 Guiding principle — do **not** over-engineer
This is a demo, not a product. Resist frameworks, bundlers, and SPA machinery unless a milestone genuinely needs them. The bar: **the shippable artifact must always run by opening one file, offline, with no server.** Optimize for stage reliability over engineering elegance.

### 3.2 The file:// trap — read before you refactor **[SETTLED constraint]**
If you split the engine into ES modules (`import`/`export`) or load config via `fetch()`, the page **will break when opened directly from `file://`** (module CORS + fetch-from-file restrictions). That kills the "present off a USB stick / downloaded file" story, which is the whole reliability argument.

**Resolution:** develop in a structured repo if you like, but the **ship target is a single self-contained HTML file** produced by a trivial inline/concat step. Either (a) keep the engine in one file and inline each typology config as a JS object, or (b) keep a small build script that inlines `config/*.json` + `src/*.js` + `src/*.css` into `dist/index.html`. Do **not** ship something that depends on a running server for the core walkthrough. A dev-time static server (`python -m http.server`) is fine for iteration; it must not be required to present.

### 3.3 Recommended repo structure
```
aml-signal-demo/
  CLAUDE.md                  # always-loaded project memory (skeleton in §7)
  README.md                  # run + present instructions
  HANDOFF.md                 # this document
  index.html                 # dev entry (may load src/ + config/ via server)
  dist/
    index.html               # SHIP TARGET — single self-contained file
  src/
    engine.js                # state machine, render dispatch, controls, animations
    acts.js                  # the six act renderers (generic, read from active config)
    theme.css                # :root tokens + base
    components.css           # act-specific styles
  config/
    schema.md                # the typology content-model spec (§5)
    typologies/
      fentanyl.json
      pig-butchering.json    # [PLANNED]
      trade-based.json       # [PLANNED]
  data/
    signals_fentanyl.json    # OPTIONAL pre-generated candidate signals (§6)
  backend/                   # OPTIONAL live mode — off by default (§6)
    relay.py                 # FastAPI relay → local llama.cpp / approved gateway
    README.md
  scripts/
    build.(py|js)            # inline src+config → dist/index.html
    pregenerate.md           # OpenCode/Copilot prompt-spec to produce data/signals_*.json
  tests/
    smoke-checklist.md       # manual stage-rehearsal checklist
    walkthrough.spec.(js)    # OPTIONAL Playwright click-through
```

If a structured repo feels heavier than the demo warrants, a perfectly acceptable minimal version is: `index.html` (the single file) + `config/typologies/*.json` inlined at build time + `CLAUDE.md` + `README.md`. Scale up only as milestones require.

---

## 4. Constraints carried over (the "why it's shaped this way")

These come from the conversation that produced the demo and the enterprise environment. Treat as **[SETTLED]** unless the human says otherwise.

1. **Scripted-first for reliability.** Live agentic pipelines fail in front of audiences. The default presentation path is fully scripted. Any live element must have a scripted fallback that triggers automatically on error/timeout.
2. **Two wow beats are load-bearing.** The two human gates (selection + confirm) and the combination-lift reveal are the persuasion. Do not redesign the six-act narrative or remove these without an explicit ask.
3. **"Illustrative data & outputs" badge stays, always visible.** Never present synthetic figures as real. This *increases* trust with a compliance audience; it's a feature, not a disclaimer to hide.
4. **No real data, ever.** No customer, account, or transaction data in the repo or the demo — coverage/population/precision numbers are synthetic. The only real-world content is **public advisory text**. Default rule: **paraphrase** it (copyright) — e.g. the FINTRAC Jan-2025 Operational Alert on illicit synthetic opioids behind the fentanyl SHOWCASE is paraphrased. **Two verbatim exceptions**, each kept visually separate from the always-on "Illustrative data & outputs" badge: **(1)** US **federal government** advisories are **public domain (17 USC §105 — works of the US government carry no copyright)** and may be reproduced **verbatim with attribution** (Act 1's SOURCE DOCUMENT panel renders EFE FIN-2022-A002 this way). This US-federal exception covers **FinCEN and OFAC** (both US Treasury — Phase 21 added OFAC as corpus source #3) and other US federal agencies. **(2)** **FINTRAC** (Phase 22, corpus source #4 — the **first cross-jurisdiction source**) is **Canadian Crown copyright — NOT public domain** — but its publications **may be reproduced verbatim for NON-COMMERCIAL use WITH FINTRAC's required attribution** (© His Majesty the King in Right of Canada + complete title + "a copy of the version available at &lt;URL&gt;"), per **FINTRAC's Terms & Conditions**: a reproduction **licence**, distinct from the US 17 USC §105 no-copyright basis. **Not** commercial redistribution (needs FINTRAC's written permission). The verbatim relaxation is **US-federal + FINTRAC only** — every **other** non-US / non-FINTRAC / non-government source still paraphrases (the fentanyl showcase still paraphrases its FINTRAC OA). _Phase 28 (the owner's compliance call):_ in the corpus explorer the per-doc Source **label** carries the document title only; the FINTRAC Crown-copyright attribution (© His Majesty… + complete title + source URL) renders in the **page footer** for the FINTRAC document on screen (empty for US public-domain docs) — verbatim-with-attribution **held**, the attribution **relocated, not removed**.
5. **Live backend reality on the enterprise machine** (if a live mode is ever built):
   - **GitHub Copilot cannot be a web backend** — no entitled general chat API; the editor endpoint is off-limits on an enterprise machine and the CLI is disabled in this subscription.
   - **Legitimate live option:** a thin **FastAPI relay → local `llama.cpp` OpenAI-compatible endpoint** (offline, no key, no egress) or the bank's **approved LLM gateway**. JupyterHub-hosted models are reachable only via sanctioned paths (`jupyter-server-proxy` + a Hub API token) and ideally called server-side, not from the laptop browser.
   - **Copilot-in-the-loop, the safe way:** use **OpenCode (Copilot provider) to pre-generate** `data/signals_*.json` ahead of time — genuine model output, reproducible, zero live-failure risk. Prefer this over a live call for the actual presentation.
   - **Never put API keys/tokens in the frontend or commit them.** The browser never holds a credential.
6. **Offline-first ship target.** See §3.2. The core walkthrough never depends on network or server.

---

## 5. The content model (refactor target)

The current arrays map cleanly onto a per-typology config object. Define this schema (`config/schema.md`) and make the engine generic against it; `fentanyl.json` is just the first instance.

```jsonc
{
  "id": "fentanyl",
  "label": "Illicit synthetic opioids (fentanyl)",
  "anchor": {
    "advisory_name": "Laundering the Proceeds of Illicit Synthetic Opioids",
    "source": "FINTRAC Operational Alert, Jan 2025",
    "hook_title": "What aren't we watching?",
    "close_title": "The blind spot closes — and stays closed"
  },
  "coverage": {
    "before_index": 45,
    "after_index": 55,
    "indicators": [
      { "id": "IND-02", "label": "Rapid pass-through / flow-through account",
        "status": "gap", "target": true, "sub": "funds in → out within days, little balance retained" }
      // status ∈ "covered" | "partial" | "gap"; one row flagged target:true is the build subject
    ]
  },
  "advisory_stream": [
    { "t": "Plain advisory text, PARAPHRASED…", "hl": false },
    { "t": "e-transfer fan-in into flow-through accounts", "hl": true }
  ],
  "candidates": [
    { "id": "C2", "name": "Rapid pass-through / flow-through", "type": "entity",
      "cover": "gap", "data": "available", "target": true,
      "definition": {
        "class": "entity · account-level · stateful",
        "features": ["inbound_credit_count_7d","outbound_debit_count_7d","retained_balance_ratio","distinct_sender_count_7d"],
        "logic": "inflows ≈ outflows within a short window AND retained balance ratio < 0.1",
        "window": "rolling 7 days",
        "source": "EMT transaction features (Gold)",
        "route": "Tier-1 alert → gate candidate"
      }
    }
    // type ∈ entity|relationship|motif; cover ∈ covered|partial|gap; data ∈ available|partial|insufficient
    // buildable = cover:"gap" AND data:"available"
  ],
  "lift": [
    { "name": "S-FLOW-THROUGH alone", "combo": "new signal in isolation", "value": 18, "strength": "weak" },
    { "name": "+ E-transfer fan-in (existing)", "combo": "S-FLOW × S-FANIN", "value": 64, "strength": "mid" },
    { "name": "+ Account age < 90 days (existing)", "combo": "S-FLOW × S-FANIN × S-NEWACCT", "value": 83, "strength": "strong" }
  ],
  "stats": { "fire_count": 1240, "standalone_precision": 18, "best_combo_precision": 83 }
}
```

**Engine contract:** given any valid config, all six acts render and the arc holds. Adding a typology = adding one JSON file (+ a selector entry). No engine edits.

---

## 6. Optional live / pre-generated mode (isolated, off by default)

Keep this entirely separate from the scripted core; the demo must run with this absent.

- **Act to make live:** only **Act 1** (advisory → candidate signals). Coverage and lift depend on data you don't have — keep them scripted/deterministic.
- **Pre-generated (preferred for stage):** `scripts/pregenerate.md` holds the OpenCode/Copilot prompt-spec that, given a paraphrased advisory, emits `data/signals_<typology>.json` matching the `candidates` schema. The engine loads it if present (when served), else falls back to the inline config. Genuine model output, no live risk.
- **Live (optional):** `backend/relay.py` = FastAPI, holds no key, forwards to `http://localhost:8080/v1/chat/completions` (llama.cpp) or the approved gateway; serves the HTML from the same app to avoid CORS; forces JSON-schema output; the frontend `extractSignals()` does `try fetch(/extract-signals) … catch → scripted CANDIDATES`. Never the default path.

---

## 7. `CLAUDE.md` skeleton (paste into the new project)

See `CLAUDE.md` in this repo — adapted from the skeleton below to reflect current (M0) state.

```markdown
# Signal Watch — AML Vision Demo

## What this project is
A presenter-driven, offline, browser-based VISION PROTOTYPE for AML stakeholder buy-in.
Not a real detection system — a scripted dramatization of the signal/atom loop.
See HANDOFF.md for full context; it dramatizes POC 5 → POC 1 → POC 3 of the
AML transformation framework.

## Non-negotiables (do not violate)
- The shippable artifact in dist/ MUST run by opening one file, offline, no server.
- Do NOT split into ES modules / fetch()-loaded config in the ship target (file:// breaks).
  Develop modular if useful; build inlines everything into dist/index.html.
- Content is config-driven (config/typologies/*.json against config/schema.md).
  The engine is generic — no hardcoded typology copy in engine code.
- Keep the six-act arc and the two wow beats (two human gates + combination-lift reveal)
  unless explicitly asked to change them.
- Keep the "Illustrative data & outputs" badge always visible. Never present synthetic
  numbers as real.
- NO real customer/transaction data, ever. Advisory text must be public-source and PARAPHRASED.
- Live mode is optional, lives in backend/, off by default, always has a scripted fallback.
  Never put keys/tokens in the frontend. Copilot is NOT a web backend (see HANDOFF §4).

## How to run
- Present: open dist/index.html (no server).
- Develop: `python -m http.server` then open index.html.
- Build ship file: `python scripts/build.py` → dist/index.html.

## Aesthetic
Dark "dossier" theme, amber --signal accent; fonts Newsreader / Archivo / JetBrains Mono.
Refined, not flashy. Match the existing look.

## Definition of done
Reliable offline · multi-typology from config · presenter controls · compliance-clean ·
README written. See HANDOFF.md §1.2.
```

---

## 8. Milestone plan

**M0 · Bootstrap.** Init repo + git; add `CLAUDE.md`, `README.md`, this `HANDOFF.md`; import `aml_vision_demo_fentanyl.html` as the baseline; confirm it runs. *Done when:* the current demo runs from the repo and is committed.

**M1 · Config-driven refactor.** Define `config/schema.md`; extract fentanyl content into `config/typologies/fentanyl.json`; make the engine generic against the schema; add the build step that inlines config → `dist/index.html`. *Done when:* the fentanyl demo is byte-for-byte equivalent in behaviour but driven by config, and `dist/index.html` runs from `file://`.

**M2 · Multi-typology.** Author at least one more typology (pig-butchering and/or trade-based) as config; add a typology selector or build-time switch; verify the six-act arc and both wow beats hold for each. *Done when:* ≥2 typologies present and switchable with no engine edits.

**M3 · Presenter polish.** Keyboard nav (←/→/Esc-reset), reset control, optional speaker-notes / teleprompter mode, `prefers-reduced-motion`, cross-browser pass on the presentation browser, timing/pacing review. *Done when:* a presenter can run it end-to-end on the target laptop with keys only.

**M4 · (Optional) Live / pre-gen mode.** `scripts/pregenerate.md` + loader for `data/signals_*.json` with fallback; optionally `backend/relay.py` for live llama.cpp. *Done when:* pre-generated path works and absence of it changes nothing.

**M5 · Ship.** README run/present instructions; compliance self-check (no real data, advisories paraphrased/public, badge present); single-file `dist/index.html` verified offline; human sign-off. *Done when:* §1.2 is fully satisfied.

*(M6 — Signal Watch ingestion pipeline; M7 — corpus-backed demo, multi-source. Both complete; see `CLAUDE.md` for the per-phase detail. Phase 33 closed the corpus SOURCE SET + re-segmented the typology axis: +5 FinCEN advisories and a NEW 5th source — all 11 FINTRAC `/guidance-directives/` per-sector ML/TF indicator pages — taking the corpus to **2,251 indicators across 56 derived / 62 publications / 5 sources**, with TBML and 4 other typologies added; workflow-driven, the showcase + entire news stream byte-frozen, no non-negotiable change. Phase 34 then verified the one neural step of Phase 33 — the 1,376 new indicators' capability/data-source codes, inherited and gated only for vocab validity, never correctness: a deterministic consistency audit (419/1,376 = 30.5% in same-text-different-code contradictions), a blind re-assignment over the 589 unique texts measuring inter-rater agreement (C 74.4% / D 77.9%, honest consensus not ground truth), user cluster-level adjudication (adverse-media ≠ KYC, cash ≠ PEP), and a byte-surgical apply correcting 213 indicators (flag/red_flag byte-frozen) → consistency 30.5% → 2.0%; a data-correctness phase, no UI/source/non-negotiable change.)*

**M8 · Adverse-media / negative-news stream (in progress).** A **second atom stream** as a third single-file artifact `dist/news/index.html` (built from `news.html`, mirroring how `dist/corpus` was added): unstructured news → grounded entity + red-flag extraction → a client-side **fuzzy match** (normalize → token-sort → Jaro-Winkler) against a **synthetic** client/counterparty book → potential exposure → a **human disposition gate**. The thesis is unchanged — an adverse-media hit is an **atom** that composes with a counterparty's transaction signals (the compose-with-the-signal payoff is the M8 north star, scoped beyond the walking skeleton). Compliance-clean by construction: the **client/counterparty book is synthetic** (no real customer data, ever) and — as of *Phase 32* — the **source articles are real US-federal public-domain enforcement records** (DOJ + OFAC, verbatim under 17 U.S.C. §105), both under the always-on illustrative badge; fuzzy scores are **real** computed similarity, never fabricated; entities + red-flag phrases are **quote-grounded** in their source article at the build boundary (`validate_news_data`), the runtime is pure client-side JS (no LLM/fetch), and `build.py` gained only an additive `news` target — the showcase + the entire corpus + the grounding core stay byte-frozen. *Phase 31* shipped the walking skeleton; *Phase 32* switched the source articles synthetic→**real US-federal gov-enforcement records** (DOJ + OFAC, verbatim under 17 U.S.C. §105 — the corpus's existing basis applied to news; the book stays synthetic) and raised the presentation to the corpus's bar (a streaming "agent reading" Read with grounded entity cards [name/location/age/profession] + the typology, a visible **scan process** on Screen [the real per-row Jaro-Winkler sweep, a threshold line, near-matches surfaced, the common-name trap flagged], the full dossier theme, and per-doc source attribution); acquisition is build-time only, the runtime still never fetches. **No non-negotiable changed.**

**M9 · Program design (Phase 47, 2026-06-12).** The "do not over-engineer — ships a demo, not a system" working agreement is **transcended for DESIGN artifacts only**, under user override at the Phase-47 direction gate: `docs/program-blueprint.md` designs the real regulatorily defensible agentic program (universal grounding principle, per-workload gate taxonomy, human-work charter); the repository still ships demos, the three ship artifacts stay demo-class and byte-frozen, no non-negotiable changed. *Phase 48* extended the blueprint brownfield + LFCM (§12 institutional-history utilization under "history is evidence, never ground truth" · §13 the LFCM target architecture — a grounded signal LIBRARY + composition layer, dossier-now/score-deferred · §14 the continuous adjudication loop, history-sourced mini-triage at a designed cadence), proved history-as-derivation-surface with a fully SYNTHETIC probe through the UNCHANGED gate (12/12 gate-green; `data/probe-history/` + `docs/probe-history.md`, outside every build path), and added the self-contained offline NON-ship report `docs/blueprint-report.html` (system-flow + grounding-chain SVG centerpieces); all 4 ship dists byte-identical, no non-negotiable changed. *Phase 49* made §14's continuous adjudication loop demo-able as the FIFTH ship artifact, `dist/triage/` (the gate console's sibling — console byte-frozen): 20 fully SYNTHETIC mini-triage scenarios across the 4 §14 strata (16 + 4 hidden controls), deterministically curated from the Phase-48 probe history into committed `data/triage/scenarios.json` (rule text embedded — build.py never reads `data/probe-history`; the synthetic-novel stratum quotes US-federal public-domain indicators ONLY, drift-checked against the current committed records); the §14 disposition grammar incl. need-more-info→C/D picker (the measured data-gap observation) + the policy-gap escape, rationale required; the reveal frames history as "decisions, not correctness" with labeled synthetic second-rater replay + process-inconsistency surfacing (evidence panels shared BY REFERENCE across divergent-disposition pairs — fact-pattern identity is structural, build-validated); the discovery ledger DERIVES every output at render with its measurement definition (params "chosen, not measured"); the 4 prior dists stayed byte-identical, no non-negotiable changed. *Phases 51–54* are NON-ship measure-first analyses over the FROZEN corpus (no ship artifact touched; `--check all` 7/7 throughout): 51 quantified cross-regulator redundancy (co-occurrence ≤32.5%, genuine equivalence ~1.4% — the corpus's no-dedup stance vindicated); 52/53 measured + decomposed the **unguarded C/D-tag** reliability (the one dimension the grounding gate never checks — self-consistency 0.677, κ≈0.65, disagreements sharp-not-scatter, committed-error bounded but context-confounded); and *Phase 54* turned those measurements into the blueprint §4–§5 **measured-not-gated control** for the C/D tag — `docs/cd-tag-control.md` (SR-11-7 Pillar-2 + OSFI E-23 grounded) + an executable `cd_correctness.py --control-check`/`--control-freeze` harness (PASS on the frozen corpus, BREACH on injected drift) — and EXECUTED the deferred independent effectiveness challenge once (a context-matched cross-family local-Qwen rater → C 0.604 / D 0.646, Krippendorff α ≈0.62, statistically indistinguishable from same-family self-consistency → the dimension's reliability is genuine, ~0.6/axis, never validated-correct), closing the Phase-47 T2/T3 control-story gap; no non-negotiable changed. *Phase 83* turned the agentification roadmap's **Stage 1** live — the **merge adjudicator** (`docs/agentification-roadmap.md`, `docs/merge-live.md`): an agent proposes each merge call from the evidence ONLY (the oracle firewall), MEASURED against the merge gate's correctness oracle (counts only, synthetic — the agent matched 54 of 66 vs the deterministic spine baseline's 33, recovering 21 of the 33 the resolver got wrong), surfaced as the 5th companion LIVE loop (`scripts/serve_merge.py` + a build-stripped overlay in `merge.html`); all 9 ship dists byte-frozen, `evidence_requirements.py`/build firewall untouched, no non-negotiable changed.

---

## 9. Backlog (concrete tasks)
- [ ] `config/schema.md` written and validated against the existing fentanyl content.
- [ ] Engine reads active typology from a single source (e.g. `?typology=fentanyl` query param with default, resolved at build for the ship file).
- [ ] Build script inlines src + css + active config(s) into `dist/index.html`; verify `file://`.
- [ ] Defensive rendering: a malformed/partial config should degrade gracefully, not blank the stage.
- [ ] Second typology authored from public advisory material (paraphrased).
- [ ] Keyboard navigation + reset + reduced-motion.
- [ ] Optional: speaker-notes overlay (toggle), per-act presenter timing.
- [ ] Optional: closing "what it takes to build this / the ask" act, pulling phase/cost framing from the transformation blueprint.
- [ ] `tests/smoke-checklist.md`; optional Playwright click-through that asserts each act renders and both gates work.
- [ ] README: run, present, add-a-typology, (optional) live mode.

---

## 10. Decision log (carried from the design conversation)
- **[SETTLED]** Scripted-first; live elements always have scripted fallback.
- **[SETTLED]** Six-act arc; two wow beats = two human gates + combination-lift.
- **[SETTLED]** Data-driven content model; engine generic.
- **[SETTLED]** "Illustrative" badge as a trust device, always visible.
- **[SETTLED]** Fentanyl / Project-Guardian as first anchor (Canadian resonance).
- **[SETTLED]** Single-file, offline-first ship target; no server for the core.
- **[SETTLED]** Live mode optional + isolated; llama.cpp/approved gateway only; **never** Copilot-as-web-API; keys never in frontend.
- **[PLANNED]** pig-butchering and/or trade-based typologies.
- **[OPEN]** ship as single file vs hosted; presentation mode (scripted/pre-gen/live); closing "ask" slide; project/product name.

---

## 11. Working agreements for the agent
1. Respect the non-negotiables in `CLAUDE.md` / §4; surface disagreement explicitly rather than silently building the alternative.
2. Preserve the data-driven design and the narrative arc; content changes go in config, not engine code.
3. Keep it offline-first and dependency-light; justify any new tooling against stage reliability.
4. Treat compliance as a hard constraint: no real data, advisories paraphrased + public-source, badge present, no secrets in the repo.
5. After each milestone, update `CLAUDE.md` / this doc's status tags and the backlog.
6. When unsure about an **[OPEN]** item, ask the human rather than guessing — these are presentation/branding calls, not engineering ones.

---

*This project ships a demo, not a system. Every decision optimizes for one thing: that it runs flawlessly in the room and makes the vision feel inevitable.*
