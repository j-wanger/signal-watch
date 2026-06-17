# End-to-End Walkthrough — presenting the connected 3-pillar demo (Phase 55)

> **Illustrative data & outputs.** This is the presenter script for the cross-pillar demo. Two things
> are "end to end" and they're different: **(A)** the 5 signal-watch ship artifacts as one presentation,
> and **(B)** the full program chain across the 3 pillars. (A) is presentable today; (B) connects in
> **two beats** — the signal-watch spine (now, fixture-proven) and the real chain (gated on the two
> sibling sessions). Acceptance contract: `docs/e2e-acceptance.md`. Serialization contract:
> `docs/pillar-integration-contract.md` §2.

## The single front door

`python3 scripts/build.py launcher` → open **`dist/index.html`** offline (`file://`, no server). It is
the one entry point:
- **The demo artifacts** (arc order): Showcase ×3 (fentanyl / trade-based / elder) → Corpus explorer →
  News stream → Gate console → Triage console. Each link opens the existing self-contained artifact.
- **The 3-pillar program chain** panel: `Pillar 1 · substrate → persist → Pillar 2 · casework → signed
  SAR → human gate`, with the three bridge states rendered live from `data/pillar-status.json` — *a
  measured check, not a claim.* Today all three read **pending** (honest: the spine is built, the real
  chain is gated).

## (A) The 5 artifacts — presentable today

Open the launcher, walk the five in arc order. The narrated thread: *one grounded signal* (showcase) →
*the signal library at regulator scale* (corpus) → *a second atom stream* (news) → *the human gates that
adjudicate what the machine proposes* (console + triage). Frame console = Class-J adjudication of C/D-tag
divergences; triage = the §14 continuous mini-triage loop. All offline, badge always on, no network.

## (B) The full chain — two beats

### Beat 1 — the signal-watch SPINE (now, fixture-proven)

In signal-watch:
```
python3 scripts/e2e_chain_check.py --selftest      # proves the JOIN logic on a synthetic C4 fixture
python3 scripts/build.py launcher && open dist/index.html
```
- `--selftest` PASSES: a synthetic C4-structuring bundle + a signed-SAR fixture satisfy every check in
  `docs/e2e-acceptance.md` (A substrate-grounding · B SAR-verified · C cross-pillar identity), and a
  deliberately-broken fixture is caught. This proves the harness; it does **not** claim the real chain is
  connected (the fixtures are LABELED synthetic, never real substrate output).
- The launcher's chain panel shows the three bridges **pending** — the honest current state.

### Beat 2 — the REAL chain (the delivery gate; gated on the sibling sessions)

1. **aml-substrate session** — run `aml-substrate/docs/persist-evidence-seam-PLAN-BRIEF.md` (bridge #1):
   emit a real C4 case to `evidence/<run_id>/<case_id>.json` (the §2 bundle, minted ids).
2. **aml-casework session** — run `aml-casework/docs/consume-real-bundle-PLAN-BRIEF.md` (bridge #2):
   ingest that bundle, run the 6 Class-G verifiers + draft + sign → emit the signed SAR json.
3. **signal-watch** — verify the join on the real outputs:
   ```
   python3 scripts/e2e_chain_check.py --real --substrate <evidence bundle> --casework <signed SAR>
   ```
   Prints **CONNECTED** (exit 0) when A∧B∧C pass. Then `python3 scripts/build.py launcher` → the chain
   panel flips to **done** (green). Until both sibling outputs exist, `--real` prints an honest
   `GATED: sibling output absent` and exits non-zero — the bridges stay pending.

## How the harness proves each join (the audit walk)

`e2e_chain_check.py` reads only committed/regenerated sibling **outputs** (json) — **no sibling code is
imported** (the one-repo-per-pillar boundary; the only import is signal-watch's own
`derive_signals.normalize`, the grounding core). The checks (full list in `docs/e2e-acceptance.md`):
- **A — substrate side:** bundle shape · per-alert grounding chain · the deterministic §2 id-mint ·
  every alert's `flag` grounds to the FROZEN corpus (`fin-2026-alert001:IND-11` for the C4 slice) under
  `normalize()`.
- **B — casework side:** the SAR seam flipped · completeness · every narrative-claim citation resolves to
  a grounded signal/txn · signed with no blocking violations.
- **C — cross-pillar:** same `case_id`; the SAR cited what the bundle grounded — the audit walk is
  continuous from the signed narrative down to the regulator advisory.

A green `--real` is the deterministic proof that a synthetic-substrate-detected C4 case became a
verified, signed SAR whose every statement walks back to the frozen corpus.

## Honesty framing (say this out loud)

The chain is wired by a **file contract**, not by code coupling: each pillar is its own repo; signal-watch
verifies the seam by reading their outputs. The synthetic fixtures are labeled synthetic and never shown
as real. The chain-state panel is a re-runnable check, not a performance number. Nothing here claims a
detection rate — the substrate's published triple-null stands: composition is evidence-assembly, not
detection-lift.
