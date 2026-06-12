# Program Blueprint — The Regulatorily Defensible Agentic AML Program

> **Status: DESIGN.** This document is the engineering blueprint translating the Signal Watch
> vision demo (presented 2026-06-11) into the design of a real AML program. It is a design
> artifact from the vision lab (Phase 47, decision article
> `.dev-wiki/articles/decisions/phase-47-agentic-aml-program-design.md`): nothing in this
> document claims to be built unless it names a committed artifact in this repository.
> Workloads marked **(design-stage)** do not exist; the demo-proven workloads name their
> committed implementations.

## 1. Operating direction

Automate by default; design for judgment. Every workload is built agentic-first, and the human
layer is designed — not residual: humans do only what a verifier cannot do or what a regulator
requires a person to own. (The shorthand "95/5" is a direction, not a measured or target ratio;
see §Honesty in the assembly sections.)

The program optimizes three properties in this order, because each is a precondition of the next:

1. **Defensible** — every output survives the audit walk (§2). An efficient program that cannot
   be examined is a finding, not a program.
2. **Effective** — detection content stays current with the regulatory and typology frontier
   because ingestion is agentic (days, not quarters); human attention concentrates where
   judgment changes outcomes.
3. **Efficient** — the agentic layer absorbs the volume work; efficiency is a *consequence* of
   the first two, never a justification for weakening a gate.

## 2. The universal grounding principle

**Grounding is universal; the substrate varies.** Every agentic output must be traceable to a
grounding substrate, and the gate that disposes it runs a deterministic verifier appropriate to
that substrate. The demo proved the text case: the LLM extracts, the deterministic gate disposes
by checking each quote is a substring of the source (`derive_signals.check_record`,
`news_ground`). The program generalizes the *quote*, not the substring check:

- **Derivation** grounds to advisory/guidance text → *substring verifiers*.
- **Transaction monitoring** grounds to the committed signals plus the transactional and
  non-transactional data supporting them → *referential and lineage verifiers* (an alert cites
  its signal and the data records that satisfy it; the citation is replayable).
- **SAR/STR narratives** ground to guidance, policies, signals, and case data → *citation
  verifiers* (every narrative statement resolves to an evidence item or a policy clause).

Three consequences:

1. **Grounding chains.** A monitoring alert grounds to a signal that was itself grounded to an
   advisory; a SAR narrative grounds to a case that grounds to alerts, screening hits, and data.
   **Defensibility is the audit walk down the chain** — from any output, an examiner reaches the
   regulatory text, the policy, and the data that produced it, in finitely many verified hops.
   This is OSFI E-23's data standard ("documented lineage and provenance," Principle 3.2) made
   structural rather than documentary.
2. **Nothing ungrounded survives a gate.** Grounded-or-dropped is the program-wide contract,
   inherited from the demo's live pipelines. A dropped item is dropped *honestly* (named reason,
   visible count) — silent truncation would pass a gate and is therefore the deeper failure.
3. **Substrate and verifier are NAMED per workload, never assumed.** The substring verifier does
   not transfer to workloads without source text; the principle transfers, the implementation is
   per-substrate design work (§3). Naming the pair is the first act of pipeline
   conceptualization — human charter work (§5).

## 3. Per-workload substrate / verifier table

The six workloads of the target program. *Built* rows name committed implementations in this
repository; *(design-stage)* rows are designs this blueprint proposes, with no implementation
claim. Gate classes are defined in §4.

| Workload | Grounding substrate | Verifier mechanism | Gate classes | Human role |
|---|---|---|---|---|
| Corpus derivation (built) | Regulator advisory/guidance text — the committed source `md` (FinCEN, OFAC, FINTRAC) | Substring quote-grounding under `normalize()` within `rf_region` (`derive_signals.check_record`); cover×data matrix derives coverage deterministically from C/D codes | G (grounding) + M (C/D tag inter-rater agreement — the unguarded neural dimension) + J (divergence adjudication) + A (committing a derived record = a human-reviewed act under licence rules) | Adjudicate measured C/D divergences; decide promotion of derived records to committed data; conceive new sources/anchors |
| Adverse-media screening (built) | Article body text + the book/watchlist records + the closed vocab (`news_ground.PROPERTY_KINDS`/`RELATION_LABELS`) | Grounded-or-stripped evidence checks with wrap-tolerant exact-byte requote (`locate_span`); referential vocab checks; quality-regression harness vs committed baseline | G (grounding + referential) + M (alias ownership measured-not-gated; `news_quality_harness --check`) + J (Disposition gate: escalate/dismiss) | Disposition decisions (escalate→watchlist, dismiss the common-name trap); match adjudication on near-hits; re-baseline only consciously (`--freeze`) |
| Transaction monitoring (design-stage) | The committed signal definitions (themselves grounded to advisories — the chain) + the transactional and non-transactional data records the signal logic reads | Referential/lineage verification: every alert cites its signal id + the data records satisfying its logic; deterministic replay of the cited signal over the cited data reproduces the alert (alert reproducibility check) | G (referential/lineage) + M (alert-quality baselines; above/below-threshold sampling agreement) + J (graded alert disposition) | Graded alert/case dispositions with captured rationale; tuning and threshold judgment as risk-appetite calls; conceive new signals from covered indicators |
| Case investigation (design-stage) | The case evidence set: alerts, signals, screening hits, KYC/account data, investigation notes, entity anchors (the Phase-41 anchor model) | Citation verification: every factual claim in the case assessment resolves to an evidence item; dangling-reference and entity-anchor resolution checks; conflicting values surfaced both-kept, never auto-resolved | G (citation/referential) + M (blind second-rater agreement on sampled cases — consensus, never ground truth) + J (the investigative conclusion itself: intent, story coherence, escalate/close) | The investigation judgment — graded, rationale-captured; the narrative of intent is human; agents assemble and verify the evidence walk |
| SAR/STR narrative (design-stage) | Filing guidance (FinCEN SAR instructions, FINTRAC STR requirements) + institutional policy + the case's signals, evidence, and data | Citation verification of every narrative statement against case evidence; deterministic completeness checklist vs the filing guidance's required elements; format/vocabulary checks | G (citation + completeness) + M (narrative-quality sampling) + J (file/don't-file judgment) + A (filer sign-off — compulsory, non-delegable) | The filing decision and the sign-off: a named person owns the SAR; drafting is agentic, accountability is not |
| Entity/event risk decisioning — the LFCM assist layer (design-stage, §13) | The fired signals with their full grounding chains + entity anchors and properties (the live layer's anchor model) + the institution's coverage posture | Referential replay: every signal contributing to a dossier is cited and independently re-derivable over its cited data; the no-unmeasured-number rule — no aggregate score without a named, owned calibration measurement | G (referential replay) + M (composition-quality sampling; elicited-judgment agreement, §14) + J (the risk call over the assembled dossier) | The risk judgment over the dossier; composition adjudication; risk-appetite thresholds — calls about the institution's posture, never delegated to an optimizer |

Reading the table column-wise is the design argument: the substrate column is the grounding
chain top to bottom (text → signals+data → evidence → guidance+case → fired-signals+chains+
anchors); the verifier column is
"the same principle, six implementations"; the human-role column **is** the 5% — and no row's
human role contains transcription, rote review, or any work a verifier in its own row could do.

## 4. The gate taxonomy

Four gate classes. A workload composes several; no class substitutes for another — the Phase-34
lesson generalized: *a grounding gate ≠ a completeness gate ≠ a correctness gate*.

- **Class G — deterministic verifiers (binary).** Grounding, referential, lineage, citation,
  completeness and schema/vocab checks. Properties: replayable, regression-gated (the frozen
  core + anchored-extension discipline of `rf_region`), cheap enough to run on every output.
  Binary by design — this is what makes the layer examinable. G gates are where the demo's
  "agent proposes, gate disposes" inversion lives.
- **Class M — measured dimensions (continuous, baselined).** Neural judgments no deterministic
  check can verify (C/D tag correctness, alias ownership, narrative quality). Controls: blind
  inter-rater agreement reported as *consensus, never ground truth*; committed regression
  baselines where re-baselining is a conscious human act (`--check` / `--freeze`). Rule
  inherited from the news-lift finding: **every scored dimension is surfaced in the gate
  report** — an agent optimizes only what it sees, and an unsurfaced dimension silently
  regresses.
- **Class J — human-judgment gates (non-binary, graded).** Dispositions are graded, not
  approve/reject: e.g. *confirm / confirm-with-conditions / both-defensible / escalate /
  reject*, each with captured rationale. The gates below assemble the evidence; the human
  judges. Two design obligations: (i) the rationale record is itself lifecycle evidence — under
  E-23 the model definition explicitly includes "judgmental assumptions," so the judgment layer
  is in scope of model-risk governance, and the captured rationale is what makes art-like
  judgment defensible; (ii) dispositions accumulate as queryable precedent (provenance rows),
  so judgment compounds instead of evaporating.
- **Class A — mandated accountability (compulsory).** Human acts a regulator requires of a named
  person regardless of judgment-need: SAR sign-off, model approval (E-23's lifecycle has an
  explicit *Approval* component; SR 11-7 Pillar 3 governance), periodic attestations,
  three-lines-of-defense roles. Class A work cannot be automated *by definition* — the design
  goal is that it arrives evidence-complete (the G/M/J layers below have already assembled and
  verified everything the accountable person needs).

## 5. The human-work charter

The human layer — the 5% in the operating direction — has two designed streams. Both are
first-class; a charter containing only the interesting work would under-count the human layer
and leave an examiner-visible hole.

**The judgment stream** (Class J work, plus conceptualization):

- **Pipeline conceptualization** — naming a new workload's substrate and verifier (§2.3),
  designing new signals from covered indicators, deciding what the next gate measures. This is
  the work this very blueprint instantiates.
- **Graded gate dispositions** — the non-binary calls over gate-assembled evidence: alert and
  case dispositions, divergence adjudications, match decisions. Non-binary with rationale is
  what makes the call *art-like and defensible at once*: the grade carries the nuance, the
  rationale carries the audit.
- **Risk-appetite and threshold judgment** — tuning decisions, above/below-threshold review,
  what to escalate. These are judgments about the institution's posture, not about any single
  output — exactly the calls that should never be delegated to an optimizer.
- **Adjudication of measured divergences** — where Class M reports disagreement (rater A vs
  rater B, model vs baseline), a human resolves the cluster and the resolution feeds back as
  precedent.

**The accountability stream** (Class A work):

- Model approval at lifecycle gates (E-23 *Approval*), SAR/STR sign-off, periodic attestations,
  model-inventory ownership, three-lines-of-defense responsibilities. Designed-for, never
  designed-away: the system's job is to make the accountable person the *best-informed person
  in the room*, not to absorb their accountability.

**Charter invariants:**

1. No human performs work a Class-G verifier can do (no transcription, no rote re-checking).
2. Every human touch is evidence-fed: the gates assemble, verify, and surface everything the
   judgment needs before it is asked for.
3. Every judgment is rationale-captured and becomes precedent — human work compounds.
4. The volume knob never points at a human: scale is absorbed by the agentic layer or surfaced
   honestly as a capacity decision, never amortized into shallower review.

## 6. The agentification criterion

What earns an agent loop, program-wide — the adoption-probe rule (captured from the Phase-46
corpus probe and the news-side lift evaluation; *n=1 per workload class, so the rule is the
PROBE, not a settled verdict*):

1. **A/B probe first.** A component is agentified (iterating loop, harness, multi-step agent)
   only where a direct deterministic or single-shot baseline *measurably leaves recoveries on
   the table* on the same material through the same gate. Where the baseline matches the loop,
   the simpler system wins (the corpus probe: identical output, 3.1× cheaper).
2. **Fold the idea in.** When a loop does lift, prefer extracting its one effective mechanism
   into the deterministic pipeline (the news finding: most of a 5.5× evidence recovery was a
   deterministic requote pass) before adopting the loop itself.
3. **Caps are mandatory.** Every adopted loop carries a max-iteration cap; the news loop never
   self-terminated — quality plateaued while the loop ran on.
4. **Gates surface all scored dimensions** (§4-M). The news loop silently regressed the one
   dimension its gate report did not show. A loop's gate report is its objective function:
   incomplete report, corrupted optimization.
5. **Tag-class neural judgments stay measured** (Class M) regardless of harness — no loop makes
   a correctness gate out of a grounding gate.

## 7. Control mapping — SR 11-7 pillars × OSFI E-23 lifecycle

The program's regulatory anchor is layered: **SR 11-7** (with the 2021 interagency statement
pulling AI monitoring/screening under model-risk governance) supplies the structural backbone;
**OSFI E-23** (effective 2027-05-01; the audience jurisdiction's regulator — see the aml-wiki
article `osfi-e-23-model-risk-management` for the per-stage mapping table) supplies the
lifecycle; **FINTRAC** obligations remain the content-domain layer. E-23 contains no
AML-specific text — compliance models are in scope generically, which is exactly why the
mapping below must be made by design rather than read off the guideline.

| E-23 lifecycle component | SR 11-7 pillar | Program control (built ones name committed artifacts) |
|---|---|---|
| Design — rationale | P1 development + P2 conceptual soundness | Decision articles + spec contracts per pipeline; the substrate/verifier pair NAMED before build (§2.3) |
| Design — data | P1 data/documentation | The grounding chain as structural lineage (committed source `md` → derived records → signals); provenance-per-row (anchor store pattern) |
| Design — development | P1 development | Authoring pipelines separated from ship/serve layers (build.py never imports authoring; the inverted extraction boundary) |
| Review | P2 validation (conceptual soundness + outcomes analysis) | Independent re-gate of every derived output (`--check-derived`); blind inter-rater measurement on neural dimensions; adversarial review agents at phase gates |
| Approval | P3 governance | Class-A human gates: committing a derived record is a human-reviewed act; model/pipeline approval before deployment |
| Deployment | P1 implementation | Build-boundary fail-loud validation (schema, closed vocab, referential integrity); drift guard (`build.py --check`, byte-identity) |
| Monitoring | P2 ongoing monitoring | Committed quality-regression baselines (`news_quality_harness --check`); conscious re-baseline (`--freeze`); surfaced-dimension completeness (§4-M) |
| Decommission | P3 governance (inventory/lifecycle policy) | Honest retirement: frozen archive + the record of WHY (the demo's archive/ + journal discipline, formalized) |

Opacity is treated as model risk: every decision-time output carries its explanation artifact
*cached with the record* (the grounded verbatim evidence beside the neural translation; the
disposition rationale beside the judgment) — generated when the decision is made, never
reconstructed for the examiner afterward.

## 8. Validation story — the no-ground-truth problem

AML has no ground truth: "all laundering that occurred" is unobservable, class imbalance is
extreme, and a confirmed-outcome label arrives years late if ever. Regulators acknowledge this
(OCC explicitly endorses alternative validation approaches for BSA/AML models). The program's
validation is therefore *alternative by design*, and each control is dispositioned honestly:

**Designed now** (the apparatus exists in this repository, demo-scale):

- Deterministic replay: every Class-G gate is re-runnable by an independent party on the
  committed artifacts (`derive_signals --check-derived`, the news replay fixtures, build-boundary
  validation) — conceptual-soundness evidence that does not depend on outcome labels.
- Regression-vs-baseline: committed quality baselines with `--check` failing loud and `--freeze`
  as a conscious, attributable re-baseline act — the embryo of E-23's *Monitoring* component.
- Blind inter-rater agreement on neural dimensions, reported as consensus and never as accuracy
  (the Phase-34/38 doctrine); divergences routed to human adjudication (Class J).

**Deferred — with owner** (cannot be built in a vision lab; owned by the model-risk function of
the adopting institution at program implementation, tracked as roadmap items in §11):

- Outcome-feedback loops (SAR acceptance/quality feedback, law-enforcement response, confirmed
  cases) folded into outcomes analysis — *the forward loop is deferred: requires real filings;
  an adopter's historical filing corpus is available at adoption as biased Class-M evidence
  (§12, Role 3).*
- Population-level drift monitoring on live data and model versions (input drift, score drift,
  alert-mix drift) — *deferred: requires production volumes; the baseline mechanism above is its
  designed seam*.
- Above/below-threshold sampling programs for monitoring effectiveness — *deferred for live
  operation: requires a live transaction population and a risk-appetite owner; the historical
  alert population enables below-the-line replay at adoption (§12, Role 2).*

The boundary is itself the honesty rule: nothing in the deferred list is claimed as mitigated by
the designed-now list.

## 9. Honesty dispositions — survive vs transform

The demo's honesty constraints, dispositioned for the program (none silently dropped):

| Demo constraint | Disposition | Program form |
|---|---|---|
| No fabricated numbers (no lift/precision claims) | **SURVIVES verbatim** | No unmeasured performance claim, ever; measured numbers carry their measurement definition |
| "Illustrative data & outputs" badge, always visible | **TRANSFORMS** | Output-status labeling: illustrative vs live-unreviewed vs human-confirmed, always visible per record (the corpus live mode's "UNREVIEWED" group is the precedent); plus the §8 outcomes-analysis obligation once outputs are real |
| NO real customer/transaction data, ever | **TRANSFORMS** | Privacy-by-construction generalized: governed data boundaries, local/in-perimeter inference (the 127.0.0.1 + gitignored-store pattern at institutional scale), licence/allowlist gates on what may persist |
| Verbatim only US-federal + FINTRAC-licensed; all else paraphrased | **SURVIVES** | Licence basis named per source in the registry; new jurisdictions enter only with a named reproduction basis |
| Live mode optional/isolated, scripted fallback | **TRANSFORMS** | Graceful degradation as a deployment requirement: every agentic component has a deterministic fallback or an honest outage state — never a silent quality cliff |
| Single-file offline ship artifact | **TRANSFORMS** | A demo-era constraint, not a program one; what survives is the property it enforced: deterministic, dependency-pinned, replayable builds with drift guards |

## 10. The 95/5 framing — direction, not ratio

"95% agentic / 5% human" is the program's *direction*: automate by default, design the human
layer deliberately (§5). It is not a measured quantity and not a target, and this blueprint
states no percentage as either. If the share of work is ever reported, the measurement is
defined first — e.g. decision-volume share per gate class (G/M/J/A) over a stated period — and
reported as measured. A target ratio is refused on design grounds, not just honesty grounds: a
ratio target inverts the charter by pressuring judgment work below the line to hit a number,
which is precisely the failure mode the charter invariants (§5) exist to prevent.

## 11. Capability roadmap — the deferred list, re-sequenced

The dev-wiki DEFERRED candidates, re-sequenced as program capabilities (each carries its open
sub-questions with it; demo-track residue stays in the dev-wiki, not here):

1. **Detection-content coverage** (corpus derivation, built): the FINTRAC `/intel/` frontier as
   committed corpus extension; a third jurisdiction (AUSTRAC CC-BY / UK OGL — a third licence
   basis is a compliance call per §9); internal history as the sixth source class (§12, Role 1).
   The content capability feeds every chain below it — its terminal state is the LFCM signal
   library (§13), built out source class by source class through the same gate discipline.
2. **Screening recovery** (adverse-media, built): the news REQUOTE-RETRY pass — the worked
   example of agentification-criterion rule 2 (fold the loop's one idea into the deterministic
   pipeline); then bulk-scan capacity with honest wall-time budgeting.
3. **Entity resolution** (the live layer's growth path): fuzzy-merge adjudication with
   identifier-layered matching over the anchor/properties model — reversible merge edges, human
   adjudication as a Class-J console (the gate console's natural sibling).
4. **Monitoring / investigation / SAR designs** (design-stage, §3): each begins as
   conceptualization work — substrate + verifier named, probe before agentifying — and each is a
   candidate future engagement, not a vision-lab build (assumption A2).

The **gate console** (Phase 47 T5, this phase) dramatizes the Class-J layer over real committed
divergence data — the vision-lab artifact for exactly the human work §5 charters.

## 12. Brownfield substrate — utilizing institutional history

The sections above read, as first drafted, like a program starting from nothing. No real
institution does: an adopter arrives with years of transaction-monitoring alert history,
investigation history, and SAR/STR filing history. These are not documentation — they are
substrates, and the program names a role and a verifier for each per §2.3. History plays THREE
distinct roles; conflating them is itself a failure mode, and one doctrine governs all three:
**history is evidence, never ground truth.** Historical dispositions encode the legacy program's
thresholds, policies, staffing, and blind spots; historical decisioning is a replayable fact
about *decisions* — what the institution decided — never a label of correctness (the consensus
doctrine of §4-M, extended backward).

**Role 1 — derivation substrate (decomposition).** The legacy assets decompose through the same
inverted extraction boundary the corpus proved (the agent extracts, a deterministic gate
disposes, a human adjudicates):

- *The legacy TM rulebook* → each rule's logic, thresholds, and intent extract into the signal
  model, verified referentially against the rule's committed definition; every legacy rule lands
  in the C/D coverage model — an honest map of what the legacy program covered and what it never
  did. The mechanism is probe-proven on synthetic material (`docs/probe-history.md`): a 12-rule
  synthetic rulebook derived 12/12 gate-green through the UNCHANGED frozen gate, coverage
  derived deterministically from the committed interview posture — with the stated shape caveat
  (the rulebook was authored advisory-shaped; real rulebooks may need the regression-gated
  anchor-extension path).
- *Investigation narratives and filed SAR/STRs* → entity, relationship, and typology extraction
  from unstructured case text — where the bulk of investigative intelligence sits — quote-grounded
  against the source narrative: the institution's OWN typologies, entering the corpus as the
  sixth source class beside the five regulators.
- Caveat carried on every history-derived item: decomposition extends coverage of the KNOWN.
  Deriving from history cannot escape legacy myopia — the regulatory/typology ingestion chain
  (§11.1) remains the frontier feed.

**Role 2 — probe baseline.** §6 requires an A/B probe before anything is agentified; for the
monitoring workload the legacy TM system IS the baseline, and the alert history with its
dispositions is the comparator corpus: candidate signals replay over the historical population,
above- and below-the-line, before any live cutover. Without history, §6 is unexecutable for
monitoring. The leverage is documented industry practice — recurring alerts on previously
cleared customers dominate rule-based queues (at one documented institution ~70% of alerts
re-reviewed behavior analysts had already discounted) — making the adjudication-history feedback
fold the highest-leverage known false-positive control.

**Role 3 — outcome-feedback embryo.** Filed SAR/STRs are the closest thing AML has to outcome
labels, and they are biased evidence: defensive filing skews the positives, filed ≠ confirmed
crime, and FIUs return almost no per-filing feedback. They enter as Class-M material — blind
inter-rater discipline, consensus never accuracy — seeding the §8 outcomes-analysis obligation
from day one of an adoption instead of years after the first filing.

The split this section forces on §8: for the vision lab, the deferred rows stay deferred — no
real customer or transaction data ever enters this repository. For an adopter, the historical
half of each row is **available at adoption** with the caveats above; what genuinely remains
deferred is only the forward loop (new filings, live drift, production volumes).

## 13. LFCM — the Large Financial Crime Model as the target architecture

The program's detection content converges on the **LFCM**: thousands to tens of thousands of
signals covering different grounds, every one grounded to evidence, assisting the judgment and
decisioning of financial-crime risk for any event or entity. The name describes the *program
capability*; the architecture beneath it is deliberately NOT one large model:

**Library, not monolith.** The LFCM is a governed **library of small grounded models** — each
signal individually derived, quote- or referentially-grounded, replayable, and carrying its own
lifecycle (design → review → approval → deployment → monitoring → decommission, the §7 mapping
applied per signal, with the Class-G evidence automatable at scale) — plus a small **composition
layer** that assembles fired signals into dossiers and is itself a separately validatable model.
The library IS the model inventory; tiering (per SR 11-7 inventory practice) sets validation
depth per signal class. A single Tier-1 mega-model as the unit of validation is refused on
defensibility grounds: conceptual-soundness review of a 10^4-signal monolith is intractable,
and opacity at that scale is unmitigable model risk. (Signal-library-scale governance has no
documented prior art — an open design question this blueprint names rather than settles.) The
five-source corpus — 2,251 grounded indicators, 56 derived signals, every quote gate-verified —
is the library's committed embryo; §12's decomposition adds internal history as the sixth
source class, and the §11.1 chain is the build-out path.

**Decisioning form: dossier now, score deferred — with owner.** For any entity or event, the
LFCM's designed-now output is **evidence assembly**: which signals fire, each carrying its full
grounding walk (§2), over the entity's anchors and properties — a dossier a human judges (the
§3 decisioning row). A calibrated unified risk *score* is explicitly deferred-with-owner: a
score requires calibration against outcomes, AML's no-ground-truth problem (§8) is at its
maximum for an "any event/entity" claim, and an uncalibrated aggregate presented as a score is
the fabricated-figure class (§9, row 1). The named embryos for eventual calibration: the
adopter's filing history (§12, Role 3 — biased, Class-M) and the elicited-judgment stream
(§14). Until a calibration measurement is defined, owned, and run, the LFCM states no number.

**Named failure modes** (design constraints, not afterthoughts):

1. **Correlated double-counting.** At library scale the signals are massively redundant across
   regulators and history (the corpus already refuses cross-regulator dedup on honesty grounds).
   Naive aggregation inflates risk for any entity touching a popular typology — the composition
   layer must model redundancy explicitly or refuse to aggregate.
2. **Volume inversion.** Thousands of signals firing per entity either get strangled by
   thresholds (the legacy TM failure, rebuilt) or bury the judgment layer — charter invariant 4.
   The design answer is **composition before escalation**: humans see composed dossiers, never
   raw signal-alerts.
3. **Coverage illusion.** 10^4 signals reads as "everything is covered"; count is not coverage.
   Coverage stays honest union arithmetic over *named grounds* (the lens discipline, scaled);
   the miss that hurts is the typology in no advisory and no history.
4. **The monolith trap.** Letting "LFCM" become the validation unit (see above) — the name stays
   at program level; the inventory stays per-signal.
5. **Drift at scale.** Signals ground to advisories that get superseded and history that goes
   stale; at 10^4 the refresh/decommission half of the lifecycle (§7, last row) must itself be
   agentic with sampled human oversight — an annual review cycle cannot arithmetically cover
   the library.

## 14. The continuous adjudication loop — eliciting judgment at a designed cadence

The program does not wait for the world to label events. Confirmed-event history at a single
institution is too thin to align a statistical model against (the documented reason in-house
AML ML underperforms); the loop instead **elicits expert judgment on curated mini-triage
scenarios at a designed cadence** — analysts work a short daily queue, each scenario judged
with a graded disposition and a captured rationale. The gate console (Phase 47) is this loop's
committed embryo: same arc (evidence → graded disposition → required rationale → precedent),
pointed at a continuous scenario stream instead of a one-off divergence set.

**Scenario source — the binding design condition.** Scenarios are sourced from the
institution's REAL history: past alerts, cases, and filings replayed as mini-triage scenarios
(§12). Historical decisioning is a replayable fact about *decisions* — the analyst's call can
be compared to what the institution actually decided — never a label of correctness. Sampling
is stratified against selection bias, because whoever curates the scenarios determines what
statistics accumulate: *history-sourced signal-fired* / *history-sourced below-the-line* /
*synthetic-novel* (typologies from the ingestion frontier not yet in any historical alert) /
*random-population*. Sampling only what already fires would calibrate the known and never
measure the unknown — the §13 coverage illusion in miniature.

**The disposition grammar.** Graded options per §4-J — confirm-risk / confirm-no-risk /
both-defensible / escalate — plus the load-bearing one: **"I need more information (naming
which)"**, e.g. a KYC attribute, a counterparty record, a screening source. That option wires
the loop into the coverage model: every need-more-info disposition is a *measured data-gap
observation* against the C/D taxonomy — the coverage interview made continuous and grounded in
real judgment moments instead of a one-time posture survey.

**Discovery outputs** (the value floor — these accrue even if consensus never converges):
signal gaps (risk judged present, no signal fired), data gaps (the need-more-info stream, per
D-code), **process inconsistencies** (the same fact pattern carrying divergent historical
dispositions — surfaced for adjudication, never auto-resolved), and **policy gaps** (scenarios
where the disposition grammar itself has no defensible option). Calibration statistics —
judgment distributions per signal and per stratum — are the compounding *upside*, always
consensus-class (§4-M), never accuracy.

**Self-instrumentation.** Agreement is a first-class measured dimension: scenarios are
double-blind-assigned at a sampled rate, divergence routes to cluster adjudication (the console
pattern), and the loop's own failure modes are named: *elicited-consensus drift* (analysts
converging on each other rather than on risk — a Class-M dimension watched against the
interleaved controls) and *click-through fatigue* (known-disposition control scenarios
interleaved; per-analyst agreement monitored — a quality control, not a performance score).

**Regulatory framing.** OCC explicitly endorses alternative validation for BSA/AML models, and
structured expert judgment is a recognized alternative-validation form; under E-23 the model
definition includes judgmental assumptions, so the rationale records double as lifecycle
evidence (§7, Review and Monitoring rows). One activity, three audit artifacts: calibration
material, ongoing-monitoring evidence, and documented analyst capability.

**Design parameters** — every figure in this section is **chosen, not measured**: the cadence
(~30 minutes per analyst per day — chosen to sit below fatigue, not derived from data), the
strata and their mix, the double-assignment rate, the agreement thresholds. Each becomes a
measured quantity only when the loop runs and the measurement is defined and owned (§10
discipline). FIU per-filing feedback is assumed near-absent (the documented norm); if an FIU
feedback channel exists at adoption, it enters Role 3 (§12), not this loop.

## 15. Relationship to the demo charter

HANDOFF's working agreement — "do not over-engineer; this project ships a demo, not a system" —
is **transcended for design artifacts only**, under user override at the Phase-47 direction gate
(2026-06-12): this blueprint designs the system; the repository still ships demos. The four
ship artifacts remain demo-class, byte-frozen through design phases, and nothing in this
document changes a non-negotiable.
