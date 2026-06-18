# Active Phase Context

Phase: 59 — **Consume the substrate Phase 15 build into the coverage map** (re-ground · re-freeze · document the exposure≠reachable-now coupling). signal-watch-local, LITE, NON-ship. The corpus→substrate coverage map (Phase 58) is committed (fc75dd9); aml-substrate Phase 15 (@5875241, DELIVERED) then shipped the SUBSTRATE HALF of Phase 58's brief — a label-blind **PartyView** (exposes D8 KYC + D12 pep) + 4 **SCREENING_DETECTORS** (C7 BusinessActivityAnomaly · C14 KycIntegrity · C8 IncomeMismatch · C26 ScamVulnerable). `substrate-pin.json` was re-grounded in the working tree but `coverage.json` was left un-frozen → `signal_coverage_map.py --check` fails. This phase finishes the consume.

Objective: re-freeze the map at the verified pin + document the honest finding — landing the substrate detectors+views moved **0** signals into reachable-now because reachability is a 3-way AND (substrate-exposed ∧ emission-measurable ∧ casework-asserted); the substrate half satisfied only *exposure*. Measured movement: needs-view-exposure 312→70, needs-behavior 54→296 (the 242 KYC/pep signals are exposed-but-unmeasurable on the txn-only emission — an emission-sample limitation, NOT emergence work); reachable-now stays 93.

Direction gate (2026-06-18, all_accept: true): direction **A** (re-freeze + document the coupling, tiers unchanged) over re-tiering with a `blocked_on` field (C) / hold-and-revert (B). The user chose **"verify first, then re-confirm"** → A0 (pin ↔ substrate@5875241) + A1 (the 242→needs-behavior / 62-C7→needs-detector tiering is intended classifier semantics) were CODE-VERIFIED before any freeze, both HELD, the user re-confirmed proceed. A2 (reachable-now can't move on the substrate half alone) / A3 (non-ship) held by evidence. Ledger: Phase-59 block. Grounded against aml-substrate@5875241 + aml-casework@4ac9523 + corpus@472b44e.

Scope: `data/coverage-map/**` (the re-grounded pin + the re-frozen coverage.json) · `docs/corpus-substrate-coverage.md` · `docs/pillar-integration-contract.md` (§8) · `aml-substrate/docs/corpus-coverage-build-PLAN-BRIEF.md` + `aml-casework/docs/capability-assertions-PLAN-BRIEF.md` (sibling, re-grounded). NOT touched: the 8 build targets / offline dists; the committed corpus records + overlays (read-only); `build.py` never imports `signal_coverage_map.py`; no sibling import.

Key constraints:
- The tier NAMES are now stale/composite for the touched signals — needs-behavior=296 = ~242 exposed-but-unmeasurable-on-the-txn-emission + ~54 genuine emergence gaps; needs-detector=62 (all C7) = detector-EXISTS-blocked-on-the-casework-assertion. The per-signal `data_source_class` + `behavior_confirmed:false` carry the real reason; the prose makes it explicit so the count isn't misread as "242 need emergence work."
- reachable-now rises only when BOTH sibling halves land: a party-bearing emission bundle (aml-substrate) + the 4 paired grounding_replay assertions C7/C8/C14/C26 (aml-casework). Both are sibling-rooted (the briefs hand them off).
- Re-ground before commit: any cross-pillar artifact re-grounded against the sibling current HEAD, HEADs pinned inline (2026-06-16 process rule).

Exit criteria:
1. `signal_coverage_map.py --check` byte-identical (coverage.json re-frozen at 5875241) · `--selftest` green · `! grep import aml_substrate|aml_casework` · build.py never imports it.
2. `docs/corpus-substrate-coverage.md` + contract §8: the measured movement + the 3-way-AND finding + the stale-label/composite-needs-behavior caveat; HEADs re-pinned (substrate@5875241, casework@4ac9523).
3. Both sibling briefs re-grounded: substrate detector/view half DONE → next = a party-bearing emission; casework → the 4 paired assertions; shared acceptance = reachable-now rises only when both land; doctrine constraint (no behavior/label stamping).
4. `python3 scripts/build.py --check all` → 8/8, the 8 ship dists byte-identical; ZERO ship artifacts in the change set.

Abort: any of the 8 offline dists drift / a ship artifact touched → STOP and surface (never re-baseline). A brief that stamps behavior or labels → out of bounds (emergence doctrine). The companion importing sibling code → out of bounds (vendored-pin / file-contract only). A validator/selftest looks like it needs loosening → fix the data/design, never the check.

Gates:
- [x] Direction confirmed by user (assumption positions taken; A0/A1 verify-first → verified HELD → re-confirmed; A2/A3 held; no unresolved reject/don't-know)
- [x] Delivery accepted (post-implementation report — user "continue", 2026-06-18)

Plan [[phases/phase-59-consume-substrate-phase-15]]; ledger Phase-59.

---

## Standing program context (durable — not a changelog)

**Program structure (Phase 50, parallel-pillar):** signal-watch is the program-ARCHITECTURE home (the blueprint `docs/program-blueprint.md` + this lifecycle record only). The real build lives one repo per pillar:
- Pillar 1 = data substrate → **`/Users/jwang/aml-substrate`** (current HEAD **5875241**, Phase 15 — corpus detectors + PartyView; the persist seam `--emit-evidence` is built; the measured TRIPLE-NULL stands [composition never required to detect laundering]; composition detection-lift RETIRED).
- Pillar 2 = case-investigation → composition → SAR/STR narrative → **`/Users/jwang/aml-casework`** (current HEAD **4ac9523**, Phase 9 — 6 Class-G verifiers + the real neural narrator + pluggable drafter backends openai/opencode; corpus_grounding ENFORCED-real against the vendored frozen-corpus pin).
- signal-watch owns the cross-pillar **integration contract** `docs/pillar-integration-contract.md` + the e2e harness `scripts/e2e_chain_check.py` + the coverage map `scripts/signal_coverage_map.py`.

**Doctrine (aml-substrate):** data-first/emergent (typologies EMERGE from modeled behavior, NEVER injected/stamped); deterministically SCRIPTED generation, no runtime LLM; grounded in researched REAL schemas + distributions; everything SYNTHETIC, no real customer data, ever. The corpus may drive DETECTOR + observable-exposure design TOP-DOWN; data generation + labels stay BOTTOM-UP. The coverage map MEASURES behavioral gaps, never stamps them (Phase 58 A0 / Phase 59 A1).

**FROZEN (signal-watch, no further demo work unless re-opened):** the 5 ship artifacts + dists byte-identical (index.html + config + 3 typology dists; corpus.html + dist/corpus; news.html + dist/news; console.html + dist/console; triage.html + dist/triage) + the launcher dist/index.html (8th target); derive_signals.py; the news pipeline; ALL committed derived data + the 3 overlays; docs/program-blueprint.md + blueprint-report.html. `--check all` → 8/8.

**Process rules:** (1) any cross-pillar artifact MUST be re-grounded against the sibling repo's CURRENT measured HEAD before commit/consume, HEADs pinned inline. (2) This file + _CURRENT_STATE drift between cross-pillar reviews — trust each sibling repo's CURRENT HEAD for its live state. (3) signal-watch-rooted sessions CANNOT drive the siblings' dev-* lifecycle (their hooks bind there).

**Prior signal-watch-local phases (detail in `_CURRENT_STATE.md` + the journal):** the measure-first workstream (51 corpus redundancy · 52/53/54 C/D-tag reliability→control) · the cross-pillar bridge (55 e2e · 56 chain workbench · 57 neural drafter backends) · 58 the corpus→substrate coverage map (this phase consumes its sibling follow-on).
