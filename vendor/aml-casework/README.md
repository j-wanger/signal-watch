# aml-casework

**Pillar 2** of the AML program: case-investigation → composition → SAR/STR-narrative — the workload
that takes Pillar 1 ([aml-substrate](../aml-substrate)) evidence to a filed-SAR draft a named human
signs off. Built in parallel with Pillar 1, coupled only by the cross-pillar integration contract.

Synthetic data only; real corpus grounding. See `DESIGN.md` for the architecture and
`docs/pillar-integration-contract.md` for the binding.

## Quickstart

```bash
# validate a synthetic evidence bundle against the contract (dependency-free)
python3 src/aml_casework/contract.py fixtures/evidence/case-thin-slice-01.json

# run the deterministic verifiers, dependency-free (or `uv run pytest` for the whole suite)
python3 tests/test_contract_fixture.py      # contract/referential integrity + narrative seam
python3 tests/test_grounding_replay.py      # each cited signal re-derivable over its cited data
python3 tests/test_completeness.py          # STR required elements substantiated; seam honesty
python3 tests/test_citation.py              # every narrative claim resolves to evidence
python3 tests/test_corpus_grounding.py      # every grounding.flag grounds to the real pinned corpus indicator
python3 tests/test_signoff.py               # disposition + sign-off refuses over any violation
python3 tests/test_chain.py                 # SIGNED slice walks all 6 verifiers + sign-off green
python3 tests/test_strata.py                # the disposition strata: conflict / data-gap / both-defensible
python3 tests/test_corpus_drift.py          # advisory: has the live corpus drifted off the vendored pin?
python -m aml_casework.detector_reconciliation  # advisory: have casework's copied screening constants drifted off substrate?
python3 tests/test_ingest.py                # the boundary adapter: reconcile a REAL Pillar-1 txn shape
python3 tests/test_real_ingest_chain.py     # the REAL multi-typology bundle -> signed STR (the chain end-to-end)

# the 6th verifier + the neural generator (widened across the strata) run under the suite (pytest-only):
uv run pytest                               # the full deterministic suite — stub drafters, no network
uv run pytest -m integration                # demos: the real model drafts per stratum behind the gates (needs ANTHROPIC_API_KEY)

# the consume CLI (Phase 7): take a substrate bundle -> a signed STR, choosing the drafter at runtime.
# This is the chain-workbench entrypoint signal-watch's serve_chain.py subprocesses per case. It validates
# FIRST, runs the 6-verifier chain, emits the signed STR, prints a one-line JSON summary, exits 0 iff signed.
python -m aml_casework.ingest fixtures/evidence/real/CASE-P-0010361.json \
  --out fixtures/evidence/real/CASE-P-0010361-signed.json --drafter stub   # reproduces the committed signed STR
# -> {"case_id": "...", "drafter": "stub", "drafter_effective": "stub", "signed": true, "blocking_violations": [], "out": "..."}
#   --drafter claude  uses the live model (server-side ANTHROPIC_API_KEY); fail-soft -> stub on any error,
#                     reporting drafter_effective. The deterministic stub drives CI; claude is one excluded demo.

# consume a REAL Pillar-1 emission and prove the 3-pillar chain CONNECTED (cross-repo, read-only on casework):
python3 ../signal-watch/scripts/e2e_chain_check.py --real \
  --substrate fixtures/evidence/real/CASE-P-0010361.json \
  --casework  fixtures/evidence/real/CASE-P-0010361-signed.json   # prints CONNECTED (exit 0)
```

## Status

Phase 1 — the deterministic chain to a signed STR over the real-grounded thin slice. Five Class-G
verifiers + a sign-off seam, all stdlib-only, each returning `list[str]` violations:

- **Contract/referential** (`contract.validate_bundle`) — reference-by-path integrity, the narrative-seam
  invariant, and `narrative_claims` structure.
- **Grounding-replay** (`grounding_replay.replay_bundle`) — each cited signal re-derivable as a per-capability
  pattern-assertion (C4 structuring, C15 shell); fail-closed on an unregistered capability or missing timestamp.
- **Completeness** (`completeness.verify_completeness` / `is_complete`) — every claimed required element
  substantiated; the narrative seam open-or-filed, never faked.
- **Citation** (`citation.verify_citations`) — every narrative claim resolves to evidence; no dangling cite,
  no uncited claim, and a complete narrative must ground the suspicion (cite a typology signal).
- **Corpus-grounding** (`corpus_grounding.verify_corpus_grounding`) — the audit walk's **last link**: every
  alert's `grounding.flag` grounds (substring under `normalize`) to the REAL committed regulator indicator in
  the FROZEN signal-watch corpus. Makes grounded-to-source *enforced*, not *authored* (see Phase 3 below).
- **Sign-off** (`signoff.record_signoff`) — runs every Class-G verifier and classifies the **disposition**
  (below), snapshotting every result so the named signer is the best-informed person. Never auto-approves.

The narrative here is a **structured set of cited claims** (`narrative_claims`), so citation is a deterministic
resolution check. `case-thin-slice-01-signed.json` is the depth-first end state — a signed STR, deterministic.

Phase 2 — the **disposition model** + a stratified fixture set (DESIGN §14, "never the happy path only").
The system *represents and evidence-validates* dispositions; it **never weighs suspicion strength** —
recommend-to-file is the human's call (RGS is human).

- **Disposition** (`record_signoff`) — the system computes `blocked` (any verifier violation),
  `needs_more_info` (clean but a required element is unsubstantiated — a data gap, distinct from blocked,
  with the missing element named), or `signed` (clean + complete). Over a signable record the human may
  **assign** `file` (validated: a grounded inculpatory suspicion exists), `both_defensible` (validated:
  grounded claims on *both* stances), or `cleared` (validated: a grounded exculpatory mitigation **and** no
  grounded inculpatory predicate — an affirmative documented dismissal, the **mirror of `file`**); an
  unvalidated assignment is refused with a reason. The system **never auto-clears** — `cleared` is only ever
  a validated human claim (system-computing it would move a signable exculpatory-only record `signed → cleared`,
  breaking the additive invariant; an affirmative clear is a suspicion judgment, which stays human).
- **Stance + conflict-both-kept** — each `narrative_claim` carries a `stance` (`inculpatory` | `exculpatory`
  | `neutral`, default inculpatory); a transaction may be marked `exculpatory: true` (documented
  counter-evidence). A `neutral` claim is *mechanism-acknowledgment* — it cites the alert that fired without
  asserting suspicion either way, so it grounds NEITHER stance (the seam a `cleared` case rides: the
  narrative acknowledges the mechanism, satisfying the citation verifier's indicator→suspicion completeness
  connection, without grounding inculpatory). The *conflict-both-kept* check requires the narrative to RETAIN
  each exculpatory data row (an exculpatory-stance claim must cite it). The system keeps both sides; it never
  adjudicates the conflict.

The five stratified fixtures isolate the dispositions the thin slice never touched:
`case-conflicting-02` (file, both sides retained), `case-data-gap-03` (needs_more_info),
`case-both-defensible-04` (human-assigned both_defensible), `case-cleared-05` (human-assigned `cleared` —
a registered cash business whose structuring alert is affirmatively explained), plus the signed thin slice (file).

The `cleared` disposition is the casework half of signal-watch's **CW-4** (cross-pillar Round 1): the live
cleared-by-mitigation verdict, casework's affirmative dismissal. signal-watch's leg-based clear is
*re-expressed* onto casework's stance model (it is not ported unchanged); casework authors its **own**
synthetic exculpatory bundle (`case-cleared-05`) because signal-watch's Lakeshore casefile is its own format,
not a casework contract bundle — the Lakeshore narrative is the semantic template only.

Phase 3 — **enforce grounded-to-source.** The other verifiers prove a cited flag resolves to an *in-bundle*
id; none opened the corpus, so "this flag IS the real regulator text" was *authored*-real — a human copied it
and asserted so. The corpus-grounding verifier closes that last link: it reads the FROZEN signal-watch corpus
as DATA and grounds each `grounding.flag` (substring under `normalize`) to the real committed indicator. A
paraphrased or drifted flag is now a loud `blocked`, not a silent pass — the program's most defensible claim
is true *by construction*.

- **Vendored pinned corpus** — CI checks out only this repo, so the corpus is committed as a read-only,
  pinned snapshot under `fixtures/corpus/` (`signal-watch@a75a136`); the enforcement gate fails the build with
  no sibling checkout. `SIGNAL_WATCH_CORPUS` can point the verifier at a live corpus instead. **Read-only on
  signal-watch** — the verifier opens `derived/*.json` for reading only; the 3-line `normalize` is a deliberate
  *copy* of signal-watch's own (never an engine import). The vendored snapshot is never edited to make a
  fixture pass — a non-grounding flag is a surfaced violation, the corpus is the oracle.
- **Drift check** (`corpus_grounding.check_corpus_drift`) — advisory, not a gate: surfaces (as a warning) when
  the live sibling has moved off the vendored pin, so an upstream re-baseline is *visible* rather than silently
  changing what the verifier enforces against. Skips honestly when no sibling is present.

Phase 4 — **the neural narrative generator**, the one neural step, fenced by the gates. Composition leaves
the narrative seam open; the generator fills it, and a **sixth** Class-G verifier closes the hole the others
left open — making this the only non-deterministic component in a deliberately all-deterministic system.

- **Narrative-grounding** (`narrative_grounding.verify_narrative_grounding`) — no other verifier reads the
  free-text `str_record.narrative` a human signs and files; the citation verifier checks the structured
  `narrative_claims`, not the prose. This sixth verifier ATOM-GROUNDS the prose: every monetary amount, date,
  account/txn/signal id, and named party in it must resolve to the cited evidence (∪ a documented regulatory
  constant such as the $10,000 CTR threshold), under the same copied `normalize`. Deterministic (regex +
  membership), never an NLP judge. Wired into `record_signoff` as the sixth verifier — an ungrounded figure or
  an invented counterparty is a loud `blocked`. (It immediately caught a real mixed-unit slip in the
  hand-authored signed-slice prose: a wire stated as "$1.84M" while the cited transaction was $18,400.)
- **Generator + bounded loop** (`narrative_generator.generate_narrative(bundle, drafter)`) — fills the three
  seam fields over an injected `Drafter`, wrapped in a bounded regenerate-against-verifier-feedback loop: draft
  → run the six verifiers → feed the violations back → regenerate up to `MAX_DRAFT_ATTEMPTS`, else fail-closed
  (the seam is left open, never a filed STR). The "judge" is the deterministic chain, not a neural one. The
  function is pure (deepcopy, no I/O beyond logging), so CI injects deterministic stub drafters and the
  verifier suite stays reproducible — **the gate, not the model, is the oracle** (temperature is gone on Opus
  4.8 anyway; you cannot pin the model, so the gate is the only determinism mechanism).
- **Real adapter** (`drafter_claude.ClaudeDrafter`) — a thin `anthropic` SDK boundary (`claude-opus-4-8`,
  structured output via `messages.parse`, no temperature), the project's FIRST runtime dependency, kept in its
  own module so the generator core stays import-light. Demo-only: the end-to-end test is
  `@pytest.mark.integration` and excluded from the default suite (`uv run pytest -m integration`, needs
  `ANTHROPIC_API_KEY`). The model is now an SR 11-7-governed artifact — model id pinned, every draft attempt
  logged (the attempt trail is the audit record).

Phase 5 — **widen generation to the stratified set.** Phase 4 drove the generator only on the thin slice;
this proves it generalizes to the three disposition strata — and, more to the point, that it cannot
manufacture a defensible record the evidence does not support. The generator needed **no change** (it was
built disposition-blind and loops only on verifier violations); the work is the proof, plus shaping the real
adapter for stance retention.

- **Generation across the strata** (`tests/test_strata_generation.py`) — for each open stratum a stub drafter
  fills the seam and the gate + disposition model reach the documented outcome: `case-conflicting-02` → `file`
  (both sides retained), `case-data-gap-03` → `needs_more_info`, `case-both-defensible-04` → `both_defensible`.
  The open forms are derived in-test from the filled fixtures (`open_seam`), which stay the single source of
  truth — no separate `-open` fixtures to drift.
- **No-fabricate-to-fill-a-gap** (the thesis) — a drafter that invents an ungrounded named party writes a
  span `narrative_grounding` cannot resolve, so the bounded loop fails closed and leaves the seam open →
  `needs_more_info`, never a fraudulent `signed`. The existing gate enforces this; Phase 5 only proves it (no
  new verifier logic). (The data-gap stratum's gap was relocated in Phase 6 — see below.)
- **Conflict-both-kept under generation** — a generated draft that omits the exculpatory-stance claim trips
  conflict-both-kept; the violation is fed back and the loop recovers, or it fails closed. The generator
  cannot file a one-sided narrative over conflicting / both-defensible evidence.
- **Adapter stance-shaping** (`drafter_claude.build_user_prompt`) — surfaces the exculpatory transactions
  (with their memos) and an explicit retain-both / never-adjudicate instruction, so the real model can satisfy
  conflict-both-kept; the gate enforces it regardless. Per-stratum end-to-end demos are
  `@pytest.mark.integration` and excluded from CI — stub drafters drive the whole gate.

Phase 6 — **consume a REAL substrate bundle → signed STR** (the substrate→casework seam; bridge #2 of the
cross-pillar end-to-end demo). The chain had only ever run on hand-authored fixtures; pointing it at the
real Pillar-1 emission (`CASE-P-0010361`, a 5-typology mule: C4 structuring · C3 funnel/fan · C2
pass-through · C5 cash-placement · C15 shell) surfaced — exactly as a first real ingest should — that the
replay layer had been grounded against *invented fixture semantics*, and reconciled it.

- **Ingest boundary adapter** (`ingest.canonicalize_transactions` / `load_real_bundle`) — the real txn row
  carries `{channel, direction, timestamp, counterparty_ref}`; the verifiers read fixture-invented
  `{kind, ts, counterparty_name}`. `validate_bundle` passed (the txn-row contract is just
  `{txn_id, account_id, …}`), so the drift lived *below* it, in the replay layer. The adapter reconciles the
  shapes at the boundary — idempotent (fixtures already carry the internal fields pass through untouched),
  deriving only the kinds the assertions need — **never by loosening the validator**.
- **Replay reconciliation** (`grounding_replay`) — the assertions now re-derive real detector behaviour:
  **C4** broadened from an over-narrow `(9000,10000)` band to canonical structuring (sub-$10k cash deposits
  *aggregating* to ≥$10k — the real deposits are ~$7–8k); **C15** gained a throughput / ~0-net-retention
  sub-signal *alongside* the grounded generic-"trading company" name match (the real shell conduit carries
  no names); and **C2 / C3 / C5** were registered. C3 is **count-based** fan-out (≥N outflows) with a
  documented limitation — the bundle omits counterparty refs, so "distinct counterparties" is not
  re-derivable (a Pillar-1 follow-up).
- **No-PII completeness** (`completeness._has_subject_information`) — the first real ingest also showed the
  subject is identified by `customer_id` only: the substrate emits **no personal name** by design ("no real
  customer data, ever"). The completeness check required a `name` the fixtures had invented, so it was
  reconciled to substantiate on `customer_id`. The data-gap stratum's gap (formerly the missing name) was
  relocated to the uncompiled transaction-detail schedule.
- **Vendored real bundle + corpus pin** — the real emission (`aml-substrate@df23bba`) and the three corpus
  records the new typologies ground to (`fin-2020-alert001`, `fin-2023-alert001`, `fin-2022-alert002` @
  `signal-watch@a75a136`) are vendored read-only under `fixtures/` (the Phase-3 pin precedent); CI runs
  deterministically without the sibling trees.
- **End-to-end → CONNECTED** — `generate_narrative` (a deterministic stub in CI; `ClaudeDrafter` in the
  `@pytest.mark.integration` demo) fills the seam, `record_signoff` reaches `file`, and the signed STR
  (`fixtures/evidence/real/CASE-P-0010361-signed.json`) is emitted. signal-watch's
  `e2e_chain_check.py --real` then prints **CONNECTED**: a synthetic-substrate-detected case became a
  verified, signed STR whose every statement walks back through the evidence to the frozen regulator corpus.

Deferred: migrating the Phase 1–5 fixtures to the canonical real txn shape + tightening the contract §2 txn
row (the ingest adapter isolates the drift for now); enriching the bundle with counterparty refs so C3 can
re-derive distinct-counterparty fan-out; and tightening `completeness`'s reporting-entity proxy to a real
field — all Pillar-1 / cross-pillar-contract follow-ups.

## Phase 7 — the consume CLI (`python -m aml_casework.ingest`)

The substrate→signed-SAR chain was real and green at Phase 6, but lived only as a test function. Phase 7
ships a stable command-line entrypoint so signal-watch's chain workbench can invoke it **per case, as a
subprocess** — the boundary stays subprocess + file-handoff, neither pillar imports the other.

- **The CLI** (`ingest.main`) — `python -m aml_casework.ingest <bundle> --out <signed> [--drafter stub|claude]
  [--signer …] [--ts …] [--disposition file]`. It runs `validate_bundle` **first** (a schema-drifted bundle
  fails loud + nonzero, no SAR written — never loosen the validator), reconciles the txn shape, runs the
  6-verifier chain with the chosen drafter, emits the signed STR, and prints a one-line JSON summary
  (`case_id`, `drafter`, `drafter_effective`, `signed`, `blocking_violations`, `out`) so the caller
  stage-streams without re-parsing the file. Exit 0 iff signed with no blocking violations.
- **The deterministic drafter** (`drafter_stub.DeterministicDrafter`) — the **first production drafter in
  `src/`** (prior drafters were test-only or demo-only). It builds a minimally-grounded draft mechanically:
  one inculpatory claim per cited signal + prose naming only the subject `account_id` and lowercase typology
  phrases — no amount, date, or named party the gate cannot ground. So it grounds for **any inculpatory-only
  library case** without per-case authoring; the committed signed STR is regenerated from it (single source
  of truth — `python -m aml_casework.ingest … --drafter stub` reproduces it byte-for-byte). **Scope
  (documented):** inculpatory-only — an exculpatory bundle would trip conflict-both-kept and fail *closed* to
  `needs_more_info`, visibly; the documented fallback there is a per-case committed-draft replay, never a
  loosened verifier. The affirmative-exculpatory / `cleared` path is realized as a **hand-authored** stratum
  (`case-cleared-05`, the both_defensible pattern — a neutral mechanism claim + a grounded exculpatory
  mitigation), closing the long-deferred "widen to an exculpatory case" item; the mechanical stub stays
  inculpatory-only by design.
- **`--drafter claude` is fail-soft** — a missing key / absent SDK / network error degrades to the
  deterministic stub, reporting `drafter_effective: "stub"` + a note (a live hiccup becomes a
  connected-but-stubbed result, never a broken chain). `ANTHROPIC_API_KEY` is read by the SDK from the
  server-side environment only. The stub drives CI; the live model is one `@pytest.mark.integration` demo.

## Phase 8 — running the neural draft on the Claude subscription (OAuth)

The `@integration` `ClaudeDrafter` demo can authenticate with a Claude Pro/Max **subscription via OAuth**
instead of a paid `ANTHROPIC_API_KEY`. The CI/API-key path is unchanged; the OAuth path is exercised only by
the network-marked probe. Run recipe:

```bash
claude setup-token                    # mint a subscription OAuth token (a CLAUDE_CODE_OAUTH_TOKEN)
export ANTHROPIC_AUTH_TOKEN=<that token>   # the SDK reads it natively → Authorization: Bearer
unset ANTHROPIC_API_KEY                # if BOTH are set the SDK sends both and the API rejects
uv run pytest -m integration tests/test_oauth_probe.py   # the two-stage OAuth probe
```

- **The env-gate** (`drafter_claude._build_client`) adds the `anthropic-beta: oauth-2025-04-20` header
  **only** when `ANTHROPIC_AUTH_TOKEN` is set and `ANTHROPIC_API_KEY` is not — `/v1/messages` 401s on an
  OAuth token without that beta header. With no token set (CI) the client is bare and byte-unchanged. Use the
  `claude setup-token` token (long-lived, programmatic), **not** the interactive `~/.claude/.credentials.json`
  accessToken. The token is read from the environment at runtime — never committed or logged.
- **The two-stage probe** isolates the two ways subscription OAuth can reject the call: stage 1
  (`test_oauth_bare_system_prompt_accepted`) tests whether OAuth accepts casework's **custom system prompt**
  (subscription OAuth has historically expected a Claude-Code identity); stage 2
  (`test_oauth_structured_output_draft`) tests the **structured-output** `messages.parse`/`output_format`.
  **Documented contingencies (built only if the probe names one):** a structured-output rejection →
  `messages.create` + a manual `json.loads` (the six verifiers stay the oracle either way); a
  system-prompt-identity rejection → a follow-up (a Claude-Code identity prefix, or accept the limit) — note
  dropping structured output does **not** fix that mode. Never loosen a verifier.
- **Operational note:** the env-var OAuth token does **not** auto-refresh, so a long-running
  `serve_chain` process would need it re-minted before expiry. signal-watch needs **no** change — it passes
  the environment through to the casework subprocess.

## Phase 9 — pluggable drafter backends (local model via `--drafter openai` / `--drafter opencode`)

The neural draft is now multi-backend behind the **same** `Drafter` seam — no verifier, contract, or
grounding change; the six Class-G verifiers stay the oracle on whatever any backend produces. Two new thin
adapters let a **local model** write the SAR/STR narrative, and the shared grounding-aware prompt +
structured-output schema were extracted to `drafter_prompts` (anthropic-free) so neither new adapter pulls in
the anthropic SDK. Both use stdlib `urllib` only — **zero new dependencies** — and a **tolerant parse**: a
malformed/missing draft → `None` (fail-closed refuse → `needs_more_info`), with no dependency on strict
json_schema enforcement.

- **`drafter_openai.OpenAIDrafter`** (`--drafter openai`) — a thin OpenAI-standard `/v1/chat/completions`
  adapter: one non-streaming POST, best-effort `response_format` json_schema, tolerant parse. Works against
  any OpenAI-compatible server (a local llama-server, LM Studio, Ollama, vLLM).

  ```bash
  export OPENAI_BASE_URL=http://localhost:8080/v1   # your local server's /v1 endpoint
  export OPENAI_MODEL=local-model                   # optional (server default otherwise)
  # export OPENAI_API_KEY=...                        # optional — a local model needs none
  python -m aml_casework.ingest <bundle> --out <signed> --drafter openai
  ```

- **`drafter_opencode.OpencodeDrafter`** (`--drafter opencode`) — drives drafting **through** a running
  `opencode serve` agent loop (which wires the local model via an `@ai-sdk/openai-compatible` provider). Use
  `opencode serve`, **never** bare `opencode run` (a known headless-permission bug). The adapter creates a
  session, sends the shaped prompt (instructing the agent that its final message be ONLY the structured Draft
  JSON), and **polls** for the assistant's final message under a turn/time bound; an exceeded bound or an
  unparseable reply → `None` (fail-closed). Run recipe:

  ```bash
  # 1. serve a local model for agent loops (tool-calling needs --jinja; ctx >= 16384, 64K+ for real loops):
  llama-server -m <model.gguf> --alias my-local --jinja --ctx-size 65536
  # 2. wire it into opencode via an @ai-sdk/openai-compatible provider whose model key == the --alias
  #    ("my-local"), then start the server:
  opencode serve                         # exposes an OpenAPI 3.1 API (schema at /doc) — NOT `opencode run`
  export OPENCODE_SERVE_URL=http://localhost:4096
  export OPENCODE_MODEL=my-local         # optional; must match the llama-server --alias
  python -m aml_casework.ingest <bundle> --out <signed> --drafter opencode
  ```

- **Per-route fail-soft** — `ingest._generate_with_drafter` resolves the drafter from a `{name → (drafter,
  fault-tuple)}` spec and runs it inside a fail-soft envelope: a missing SDK, an unreachable endpoint, or a
  garbage response degrades to the deterministic stub with a named note (`drafter_effective: "stub"`), so a
  missing local server never breaks the chain. The fault tuple is deliberately **narrow** (`URLError`,
  `TimeoutError` — each adapter normalizes its transport/parse faults to `URLError`) so a downstream verifier
  error is never masked as a drafter fault. A drafter that *refuses* (returns `None`) still fails **closed**
  (the seam stays open → `needs_more_info`), distinct from the fail-soft.

- **Measurement-task half (CI tests the gate, not the model):** the offline suite stubs both backends'
  clients — no network — and is the gate. The real local-model **CONNECTED** runs (`serve_chain.py --drafter
  openai|opencode` → `e2e_chain_check --real`) are operator-run `@integration` demos, excluded from CI with an
  honest skip when `OPENAI_BASE_URL` / `OPENCODE_SERVE_URL` is unset (the agent holds no local server). The
  `opencode serve` wire shape in the default client is the one part exercised only in that run — verify it
  against the live OpenAPI at `{OPENCODE_SERVE_URL}/doc`. signal-watch needs **no** change — its chain
  workbench already resolves both backends server-side and passes `--drafter <name>` + the env to this CLI.

## Phase 10 — the screening-grounded class (`grounding_replay` for non-replayable capabilities)

Pillar 1 splits its detectors in two: per-account **transaction-monitoring** detectors (C2–C6, C15),
whose alerts are Class-G replay-reproducible from the records they cite, and **screening** detectors
(C7 peer/business-activity anomaly, C14 KYC-integrity, C8 income, C26 scam), which read the *whole
population* — a peer/cohort comparison or a static KYC state — and are, by Pillar 1's own design, **not**
reproducible from one account's cited records (its replay gate `monitor/verify.py` runs the
transaction-monitoring detectors only). casework's `grounding_replay` now mirrors that split:

- **`_ASSERTIONS`** — the replay-reproducible signals (C2–C5, C15): a per-capability **pattern
  re-derivation** over the cited evidence (unchanged).
- **`_SCREENING`** (new) — a context-relative signal (**C7**) that has no replay core.
  `_screen_c7_peer_anomaly` grounds what the cited evidence *can* re-derive — the detector's **absolute
  $25k inflow floor** (`_PEER_ANOMALY_MIN_INFLOW_CENTS`, copied from the substrate's `MIN_INFLOW_CENTS`,
  no sibling import) — while the **peer-cohort outlier core is NAMED as screening-lineage**: recorded in
  `alert.rule` and corpus-resolved by `verify_corpus_grounding`, never faked as a replay.
- **Dispatch stays fail-closed** — `_ASSERTIONS` → `_SCREENING` → violation. Screening-grounded is **not**
  a loosening of grounded-or-dropped: an alert whose cited inflow is below the floor, whose capability is
  unregistered, or whose flag doesn't resolve to the corpus still fails closed and blocks sign-off. A
  synthetic C7 alert (`fixtures/evidence/case-c7-screening-01.json`) reaches a **signed STR** through all
  six verifiers; a below-floor mutation blocks it (`test_chain.py` / `test_signoff.py`).

No contract or §2 schema change — the alert already carries `rule`. The entity/KYC screening siblings
(**C14 / C8 / C26**, all Pillar-1 `ScreeningDetector`s) stay fail-closed until the substrate's PartyView
emits them — casework does not register an assertion for a capability the substrate cannot yet emit. The
**real-substrate-C7 acceptance** (a live C7 emission passes the chain; signal-watch's
`signal_coverage_map.py --check` `reachable-now` count rises) is an operator-run `@integration` step — CI
proves the capability offline on the synthetic fixture (the Phase 6/8/9 measurement-half pattern).

## Phase 11 — party-grounded screening: C8 income-mismatch (consuming the v0.2 `parties` block)

The substrate's Phase-17 contract amendment (**CONTRACT_VERSION 0.2**) adds an optional, additive
`parties` block — a label-stripped **PartyView** (the 16-field KYC/CDD allow-list, never raw
Person/Organization). casework consumes it to register the first **party-grounded** screening capability,
**C8 income/activity mismatch**.

- **Contract (additive).** `validate_bundle` now accepts `contract_version` ∈ `KNOWN_CONTRACT_VERSIONS`
  (`0.1`, `0.2`) — an unvalidated version is a violation, not a silent pass — and validates the optional
  `parties` block for **shape**: every row carries the 16 `PARTY_VIEW_FIELDS` keys. casework **trusts the
  projection** as the leak firewall (the substrate serializes `PartyView` only) — it validates the known
  keys are present and tolerates unknown extras (validate-known-present, never re-implementing the
  firewall). No change to the alert `txn_ids` leaf rule.
- **Party-aware dispatch.** `_SCREENING` assertions now carry a wider signature —
  `ScreeningAssertion = (alert, cited_txns, party)` — mirroring Pillar 1's
  `ScreeningDetector(txns, accounts, parties)`. `replay_bundle` resolves each alert's PartyView via
  `_party_by_account` (the observable FK **`customer_id` IS `party_id`**) and threads it to screening
  assertions only; the five `_ASSERTIONS` (C2–C5, C15) keep the narrow txn-only signature, byte-unchanged.
  C7 migrates onto the wider signature and ignores `party`.
- **`_screen_c8_income_mismatch`.** Grounds on a **re-derivable ratio**: `sum(cited CREDIT inflow) >=
  max($25k floor, 12 × party.expected_monthly_volume_cents)`. The declared baseline is screening-state
  **read from the recorded `parties` block** (named in `alert.rule`), the inflow is re-derived from the
  cited transactions — neither is faked. Constants are copied from the substrate's `income_mismatch.py`
  (no sibling import). Fail-closed: no resolved party, no positive declared volume, or inflow below the
  ratio/floor is a violation that blocks sign-off — screening-grounded is **not** a loosening. A synthetic
  C8 alert (`fixtures/evidence/case-c8-screening-01.json`) reaches a **signed STR** through all six
  verifiers; raising the declared volume so inflow falls below 12× blocks it (`test_chain.py` /
  `test_signoff.py`).

**Deferred (their own follow-on phase):** **C14** KYC-integrity is a *txn-less* screen — its substrate
detector cites `txn_ids=()` (its lineage is the KYC record), which the contract's reference-by-path
invariant (`an alert must cite txn_ids`) rejects today; admitting it is a grounding-leaf *doctrine
extension*, not an additive change. **C26** scam is transaction-behavioral and hits the same
`counterparty_ref` honesty gap as C3. Both stay fail-closed.

**Cross-pillar seam (real demo, pending).** The substrate fires C8/C14 in volume but does **not yet
compose screening detections into evidence bundles** (`emit_evidence_bundles` carries only the
transaction-monitoring alerts + the `parties` block). The **real-substrate-C8 acceptance** — a real
composed C8 bundle through the chain → signed STR, with casework's copied re-derivation reconciled against
the real detector, and `reachable-now` rising off 93 — is therefore gated on a **substrate Phase 18**
(compose C8 screening detections into bundles, an aml-substrate-repo phase). casework's contract amendment
+ `_screen_c8` + the synthetic fixture **specify** what that emission must look like.

## Phase 12 — C14 KYC-integrity on a *party leaf* (the reference-by-path extension)

C14 KYC-integrity is a **txn-less** screen: the substrate's `KycIntegrityDetector` fires on a defective
**static KYC state** and emits `txn_ids=()` by design (its lineage is the KYC record, not a transaction).
casework's grounding-LEAF doctrine required every alert to cite a non-empty `txn_ids`, so C14 could not
ride the additive path C8 took. Phase 12 **widens the leaf doctrine** from *txn-leaf only* to *txn-leaf
**XOR** party-leaf* — the **reference-by-path** extension.

- **Leaf-XOR contract rule** (`contract.py`). An alert grounds on **EXACTLY ONE** leaf: a non-empty
  `txn_ids` **XOR** a `party_ref` that resolves to a `parties[].party_id`. Neither leaf, or both leaves,
  is a violation (no ungrounded alert, no double-cite); a `party_ref` that resolves to no party row
  **fails closed** (an unresolvable reference is ungroundable, never a silent pass).
- **`_screen_c14_kyc_integrity`** (`grounding_replay.py`). A txn-less party-leaf alert resolves its party
  via `party_ref` (`_party_by_ref`, reference-by-path) and re-derives the screened **KYC defect** over
  the recorded `PartyView` state — EDD-classified with no documented `source_of_funds`, a HIGH
  `risk_rating` not escalated to EDD, or a sanctions/adverse-media flag without EDD (**copied** from
  substrate `kyc_integrity._kyc_defect`, no sibling import). The KYC state is grounded as
  **screening-lineage, not a transaction replay**. Fail-closed: no resolving party / missing `cdd_level`
  pivot / a clean KYC state is a violation.
- **Txn-less path through all six verifiers.** The build-and-test (Phase-11/A0 bet made good): tracing a
  txn-less party-leaf alert through the chain, only `completeness` assumed cited transactions —
  `transaction_details` is now substantiated by the **resolving party leaf** when a case cites no txns
  (still fail-closed: no cited txns *and* no resolving party leaf is unsubstantiated; whether the leaf
  actually grounds stays grounding-replay's job). citation / corpus-grounding / narrative-grounding /
  sign-off needed no change. A synthetic txn-less C14 alert
  (`fixtures/evidence/case-c14-screening-01.json`) reaches a **signed STR** through all six verifiers; an
  unresolved-party or unscreened-KYC-state mutation **blocks** (`test_chain.py`, `test_signoff.py`).

**C26 stays UNREGISTERED — the honest NULL.** C26 (scam) is transaction-behavioral and the substrate
designates no scam-**victim** role; it carries `behavior_emergence=absent`. An **ungroundable** capability
is a violation (fail-closed, grounded-or-dropped), so casework ships **zero code** for it — a documented
non-registration. Registering C26 to chase a coverage number would be exactly the dishonest-thin move the
gate chain exists to prevent.

**No `reachable-now` claim.** Phase 12 is a **groundability / honesty refinement** (admitting a legitimate
txn-less grounding shape), **not** a coverage gain — the scoreboard move was C7 (`reachable-now` +78 at
Phase 10). C14 carries `behavior_emergence=absent`, so no reachable-now is claimed.

**Cross-pillar sequence (casework LEADS).** casework ships the party-leaf **doctrine first**; the synthetic
fixture **defines** the shape (framing A: `txn_ids=()` + a `party_ref`). The substrate screening-emission
brief (Increment 3) then emits a **real composed C14 bundle to match**. That real bundle — through the
chain to a signed STR — is the shared **cross-pillar acceptance gate** (it lands after casework ships).

## Phase 14 — reconcile copied detectors against the live source + vendor the real C8 bundle

casework grounds screening capabilities by **re-deriving the detector's screened condition** over the cited
evidence — **copied from the substrate detector with provenance, never imported** (the no-sibling-import
doctrine). A copy **drifts** when the substrate detector changes; a self-authored synthetic fixture (where
casework writes *both* the emission and its grounding) cannot expose that drift — only reconciliation against
the live source / a real emission can (the Phase-6 lesson). Phase 14 reconciles on two threads:

- **C14 `_kyc_defect` drift fix.** The substrate **re-keyed** `kyc_integrity._kyc_defect` (Phase 25): its
  primary defect branch moved off the old **EDD-only tautology** (`cdd_level == EDD and not source_of_funds`,
  which fired on every EDD party and *missed every elevated-non-EDD subject*) onto the broader
  **elevated-obligation** rule — `elevated_obligation and source_of_funds is None`, where *elevated* =
  `risk_rating != LOW` **or** EDD **or** a PEP **or** sanctions/adverse-flagged. casework had copied the OLD
  rule (Phase 12), so it would **false-block** a real C14 alert on an elevated-non-EDD subject (a MEDIUM-risk
  or PEP customer with no documented source of funds). The fix broadens the copied branch to match
  (`grounding_replay.py`, provenance-stamped to `aml-substrate@01ddeaf`) and switches `not source_of_funds` →
  `source_of_funds is None` to mirror substrate exactly. Over the substrate data domain (`source_of_funds` is a
  documented string or `None`, never empty) it is a **strict superset** of the old branch — every party the old
  rule grounded still grounds, so it only *reduces* false-blocks. The
  behavioral reconciliation against a **real C14 emission** stays **deferred** (the substrate emits no C14
  yet — an open item, not a coverage claim).

- **Vendor the real C8 bundle + reconcile.** `CASE-P-0000251` (the substrate's real `income_mismatch`
  emission, **contract v0.3**) is vendored under `fixtures/evidence/real/` and reaches a **signed STR**
  through all six verifiers — closing the long-deferred *real composed C8 demo* (Phase 11's deferred T4),
  now over a **real emission** rather than a synthetic fixture. The party resolves via the account join
  (`party_ref` is null → `subject.customer_id == party_id`). The **C8 reconciliation** then *establishes*
  (does not assume) that casework's `_screen_c8` re-derivation **agrees** with the substrate detector's
  firing: casework sums the **cited** credits while the detector sums **all account** credits, and a guard
  test pins that the alert cites the account's *full* credit set (`cited == account == the inflow the
  detector recorded in `alert.rule``). A future emission that cited a credit *subset* would make casework
  under-count and is surfaced by the guard for a fail-closed fix — **never** a loosened floor.

**Contract v0.3 (`related_parties[]`).** The vendored bundle carries the additive v0.3 `related_parties[]`
beneficial-ownership graph block; casework **validates it to the v0.2 bar** (its determination/network consume
is signal-watch-side) — vendoring the v0.3 bundle incidentally proves that acceptance end-to-end.

## Phase 15 — detector-drift reconciliation harness (kill the copied-formula *silent*-drift class)

Copied-formula drift has bitten twice (C4/C15 in Phase 6, C14 in Phase 14). The structural fix is **not** to
stop copying — the re-derivation is what gives screening grounding its *specificity* — but to stop the copies
drifting **silently**. (The alternative, re-grounding screening on `alert.rule` + corpus lineage *only* like
C7, was rejected: it would collapse C8 into C7 and let a C14 claim ground against a *clean* party — weaker
grounding, a false-PASS hole.) `detector_reconciliation.py` is the tripwire — a **standalone, sibling-gated**
check (the 6-verifier chain is byte-unchanged; it is *not* a per-bundle verifier), mirroring
`corpus_grounding.check_corpus_drift`:

- **Constant drift-check** (`check_detector_drift`) — reads the live substrate detector **source** (`ast`, no
  import) and reconciles casework's copied screening **constants** against it: the C7 peer-anomaly floor
  (`business_activity.MIN_INFLOW_CENTS`) and the C8 income-mismatch floor + multiple
  (`income_mismatch.MIN_INFLOW_CENTS` / `MISMATCH_MONTHLY_MULTIPLE`). A divergence (or a vanished symbol) is a
  **warning** naming both values; **honest-skip** when the substrate sibling is absent. Run it:
  `python -m aml_casework.detector_reconciliation`.
- **Behavioral C14 reconciliation** (`tests/test_c14_behavioral_reconciliation.py`) — the C14 `_kyc_defect`
  *predicate* is branch logic a literal-diff can't catch, so it is reconciled **behaviorally**: a synthetic
  KYC-state battery runs through both casework's copied `_screen_c14` and substrate's **real** `_kyc_defect`
  (in substrate's own env, via subprocess), and the two must agree **verdict-for-verdict**. A default-suite
  pin (`labeled_c14_battery`) guards the copy against an *independent* reading of the spec; the live
  equivalence sweep is `@integration` (excluded from the default suite, honest-skip when the sibling is absent).

**Warn, never a build break.** A substrate re-key is a *human* signal (review + re-pin the copy), not a CI
failure — so detector-logic drift is **surfaced**, not gated: the check returns warnings and
`check_detector_drift` never raises (the corpus-drift posture).

**This closes Phase-14 A0's correctness leg.** That gate was deferred to "a real C14 emission," but behavioral
*equivalence* needs only a **runnable predicate** (which the substrate has), not a real emission — correctness
≠ coverage. Only a real C14 *emission* (for coverage) stays substrate-gated.

**Scope boundary (named, not silent).** The harness covers only the screening copies with a named
substrate-symbol provenance (C7/C8 constants, the C14 predicate). The replay assertions (C2–C5, C15) were
Phase-6 *reconciled-to-semantics* — no 1:1 substrate constant to diff — so they are **out of scope** here; the
broader semantic reconciliation for them is **Phase 16** (below).

## Phase 16 — replay-assertion semantic reconciliation (C2–C5/C15)

The replay assertions C2–C5/C15 are copied re-derivations of substrate's
`passthrough`/`funnel`/`structuring`/`cash_placement`/`shell` detectors, living in the **signed** chain
(`replay_bundle`, verifier #2). They carry the same copied-formula drift risk as the screening copies — but a
constant-diff can't catch them, because there is no 1:1 constant. **The crux:** substrate fires over the *full*
transaction stream, while casework re-derives over the *cited subset* of an already-fired alert, so the
constants *legitimately* differ (casework is deliberately looser). A strict verdict-equality would cry wolf on
every deliberate-looseness case; a constant-diff has nothing to diff.

So the reconciliation invariant is **directional**:

> **substrate-fires ⇒ casework-grounds over the detector's emitted `txn_ids`.**

The dangerous failure is casework being *stricter* than substrate → a **false-block of a real alert** (the
C14/Phase-14 bug). Two legs, extending the Phase-15 C14 precedent (`tests/_reconciliation.py` +
`tests/test_replay_reconciliation.py`):

- **Pinned default-CI battery** (`labeled_replay_battery`) — per-cap synthetic `(alert, cited-txns)` cases with
  expected verdicts reasoned *independently* from the substrate spec; runs without a substrate checkout. The
  deliberate-looseness cases ground (casework looser/equal over the firing set); the three analyzed latent
  false-blocks (C3 fan-in, C15 retention band, C4 non-cash channel) are pinned to their reasoned ungrounded
  verdict.
- **`@integration` live equivalence** (`test_casework_replay_grounds_substrate_firing_sets`) — subprocesses
  substrate's **real** detectors over synthetic firing batteries, takes each `Detection`'s emitted `txn_ids` as
  the cited set, maps them to casework's cited shape via the **production ingest adapter**
  (`canonicalize_transactions` — the same boundary a real bundle takes, so the mapping is anchored to reality,
  not invented; cross-checked against a real fixture's `txn_ids` in the default suite), and asserts the
  directional verdict. Honest-skip when the sibling is absent.

**Safe deliberate divergences** (casework looser → grounds the firing set, never false-blocks): C2 drops the
detector's credit-before-debit ordering and the $1k floor; C4's 7-day window ⊇ substrate's 24h and it accepts any
sub-$10k amount (no $7k band); C5 needs ≥3 cited cash deposits vs substrate's ≥5; C3 uses a count proxy.

**Findings (the gap register).** The harness surfaces three latent false-blocks — cases where the substrate
detector fires but casework re-derives the firing evidence as *ungrounded* (casework stricter):

| Finding | Substrate fires | casework re-derivation | Logic-reachable? | Data-reachable today? | Triage |
|---------|-----------------|------------------------|------------------|-----------------------|--------|
| **C15 retention band** | shell throughput up to ≤10% net retention | grounds throughput only ≤5% (+ a generic-name fallback) | **Yes** (confirmed @ substrate `fc98b09`) | **No** — the real conduit (`CASE-P-0010361`) retains **3.57%**, grounded via throughput | **Document** |
| **C3 fan-in** | fan-IN (≥5 distinct CREDIT sources) *and* fan-out | re-derives fan-**out** only → counts 0 cited outflows | **Yes** (confirmed @ substrate `fc98b09`) | **No** — the real C3 (`CASE-P-0010361`) is fan-**out**, grounded by the count proxy | **Document** |
| **C4 non-cash channel** | structuring on sub-$10k CREDIT of **any** channel (no channel filter) | grounds only CASH `cash_deposit` → a non-cash structuring alert counts 0 deposits | **Yes** (confirmed @ substrate `fc98b09`: fires on EMT in-band credits) | **No** — the real C4 (`CASE-P-0010361`) cites CASH deposits; substrate's non-cash sub-$10k stream sits below the $7k band | **Document** |

**Triage outcome (triage-per-finding, by reachability).** All three gaps are *logic*-reachable (substrate's real
detectors fire on them and casework false-blocks — the `@integration` leg confirms it) but **not**
*data*-reachable against current substrate emission. So they are **documented as latent, not fixed** — the
6-verifier chain stays **byte-unchanged**. The directional battery + the `@integration` regression are the
durable **loud** signal: if substrate's emission ever shifts into a gap (a C15 alert at 5–10% retention, a C3
fan-in, or a non-cash C4 structuring), the live-equivalence test goes red — surfacing the drift instead of
false-blocking a real SAR silently. (Were a gap to become data-reachable, the fix is a source-faithful
re-derivation update to `grounding_replay` — e.g. tracking substrate's 10% retention tolerance, or grounding C4
on sub-$10k CREDIT of any channel — with a verify-first regression.)

**Named structural gaps** (reconciled only at the transaction-observable level, not faked): C3's
distinct-counterparty count is not re-derivable without `counterparty_ref` on the cited outflows (a cross-pillar
follow-up); C15's ownership-graph features (circular ownership, shared-address/director overlap) need a
relationship graph casework does not carry.

## Phase 17 — the reconciliation lane (operationalize the drift tripwires)

Phase 15 + 16 built four sibling-gated drift tripwires — the copied-constant check
(`detector_reconciliation.check_detector_drift`), the vendored-corpus check (`corpus_grounding.check_corpus_drift`),
and the two behavioral `@integration` equivalences (C14 `_kyc_defect`, the replay assertions). They only ever fired
in a manual `pytest -m integration` run with the substrate sibling present. Phase 17 makes them fire as **one
advisory lane**.

- **The local runner — fires today** (`python -m aml_casework.reconcile`): consolidates the two `DriftReport` checks
  into one report and exits non-zero **only** on `drift` (the loud signal). It honest-skips when the sibling is
  absent and **never raises** — a drift is a human *re-pin signal*, not a build break. This is the command to run
  when you bump the substrate pin.
- **The `reconciliation` marker** (`pytest -m reconciliation`): selects the three substrate-gated tripwires apart
  from the credential/network drafter demos that share the overloaded `integration` marker. The three keep
  `@pytest.mark.integration`, so the **default suite is unchanged** (they stay excluded) — the marker only adds a
  group selector for the lane.
- **The hosted lane** (`.github/workflows/reconciliation.yml`): an **advisory, non-required** workflow (nightly
  schedule + manual `workflow_dispatch`) that checks out the substrate sibling when reachable and runs the runner +
  `pytest -m reconciliation` under `continue-on-error`. It is **dormant** until both repos are hosted with cross-repo
  access (today neither has a git remote) and degrades to honest-skip when the sibling is unavailable. The required
  gate (`ci.yml`: lint / typecheck / test / security) stays **substrate-independent** — drift surfaces out-of-band,
  it never blocks a merge.

The first live run already earned its keep: it surfaced a real `corpus-drift` — a vendored advisory with no
counterpart in the live signal-watch corpus — exactly the re-pin signal the lane exists to make loud.

See `.dev-wiki/` for phase/task state and `DESIGN.md` for full doctrine.
