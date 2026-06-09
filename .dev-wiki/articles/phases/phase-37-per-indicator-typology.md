---
title: "Phase 37: Per-indicator typology (corpus Typologies lens)"
aliases: []
category: phases
tags: [corpus, typology, typologies-lens, fintrac, sector-guidance, overlay, neural-assignment, measure-first, cross-corpus-synthesis]
parents: []
created: 2026-06-08
updated: 2026-06-08
source: plan
status: active
scope: [".dev-wiki/tmp/**", "data/indicator-typology-map.json", "scripts/build.py", "corpus.html", "data/typology-map.json", "dist/corpus/index.html", "tests/corpus-explorer.test.mjs", "docs/**", "tests/smoke-checklist.md", "CLAUDE.md", ".claude/rules/active-phase.md"]
entry_criteria: "Phase 36 DELIVERED + accepted + committed (e96f31d + 71e0989, pushed to main). The corpus is the primary demo; its Typologies lens groups each DOC by one money-laundering typology (data/typology-map.json, 27-term closed vocab). All 10 derived FINTRAC sector-guidance pages render; 7 collapse into a catch-all typology fintrac-sector-baselines."
exit_criteria: "The Typologies lens groups by INDICATOR typology; the 7 FINTRAC sector pages distribute across real typology clusters; fintrac-sector-baselines retired; per-indicator typology lives in a NEW overlay so all 56 derived records + derive_signals.py stay byte-frozen; combined coverage stays honest union arithmetic (no lift/dedup; badge intact); --check all 5/5 zero drift; node corpus + news harnesses + derive --selftest green; the agreement rate reported as consensus (not a new demo number); NO non-negotiable change."
---

# Phase 37: Per-indicator typology (corpus Typologies lens)

## Objective

Make the corpus Typologies lens honestly represent FINTRAC's sector guidance. Today the lens groups
each DOCUMENT by ONE money-laundering typology (`data/typology-map.json`, a doc→typology closed-vocab
overlay — a Phase-24 honesty constraint). That model breaks on the FINTRAC per-sector indicator pages:
a sector page (e.g. *Financial entities*) enumerates indicators across MANY typologies (bribery/
corruption, TF, structuring-below-threshold, wire transfers, non-Canadian jurisdictions), so 7 of the
10 derived sector pages couldn't take a single real typology and were bucketed into a catch-all
`fintrac-sector-baselines`. The user (eyeballing the BUILT demo) asked why only "7 documents" show
under the FINTRAC guidance typology. The fix: tag typology PER INDICATOR so a sector page's indicators
distribute across the real typology clusters and the catch-all retires.

## Investigation (this session — the gap, sized honestly)

- **All 10 derived sector pages RENDER** in `dist/corpus`. The "7" is the `fintrac-sector-baselines`
  cluster; the other 3 are filed under their own typology (casinos→`casino-gaming`,
  real-estate→`real-estate`, virtual-currency→`virtual-currency`), and all 10 appear together in the
  **Documents** lens under "FINTRAC sector guidance (ML/TF indicators)". Nothing is lost — the catch-all
  just presents FINTRAC's richest contribution as a lump in the PRIMARY cross-corpus view.
- **The FINTRAC source side is COMPLETE.** FINTRAC publishes exactly 11 per-sector
  `indicators-indicateurs/<sector>_mltf-eng` pages; we have all 11 (10 derived, crown-agents honestly
  skipped). Within-page extraction is complete (derived count ≥ source bullets on every page). The
  STR-reporting (`str-dod`) + sanctions-evasion guidance pages enumerate NO indicators (process
  guidance, honestly non-derivable, like the 4 existing skips).
- **The remaining derivable FINTRAC frontier** is in the /intel/ special-bulletin family (OA001
  tax-evasion-real-estate + sanctions-evasion SB + Russia-linked-ML SB + dual-use advisory) — OFFERED
  and DEFERRED in favour of the representation fix.

## Scope

Files and modules affected:
- `data/indicator-typology-map.json` (NEW overlay) — indicator-id→typology; carries the typology so
  the 56 derived records stay byte-frozen.
- `scripts/build.py` — load + validate the overlay at the build boundary (closed vocab + referential
  integrity); resolve each indicator's typology (overlay ELSE doc-inheritance); inject into `__CORPUS__`.
- `corpus.html` — the Typologies lens + cross-corpus synthesis group by INDICATOR typology.
- `data/typology-map.json` — the 7 catch-all doc entries repurposed to a doc HEADLINE or retired.
- `dist/corpus/index.html` — rebuilt (the new frozen corpus baseline).
- `tests/corpus-explorer.test.mjs` — a no-catch-all + distribution assertion.
- `.dev-wiki/tmp/**` — the T1 probe + the T2 assignment/agreement artifacts (intermediate, non-ship).
- `docs/**`, `tests/smoke-checklist.md`, `CLAUDE.md` (in-place `## Current state` edit),
  `.claude/rules/active-phase.md`.

## Exit Criteria

- [ ] The Typologies lens groups by INDICATOR typology; the 7 FINTRAC sector pages' indicators appear
      under ≥2 distinct real typologies; `fintrac-sector-baselines` retired (0 clusters)
- [ ] Per-indicator typology lives in `data/indicator-typology-map.json`; all 56 derived records +
      `derive_signals.py` BYTE-FROZEN (`git diff` clean)
- [ ] build.py validates the overlay at the build boundary (fail-loud on out-of-vocab / dangling key)
      and resolves every live indicator's typology (overlay ELSE doc-inheritance)
- [ ] Combined coverage stays honest union arithmetic over per-indicator statuses — NO lift/similarity/
      cross-regulator dedup; the always-on badge intact
- [ ] `--check all` 5/5 zero drift; node corpus + news harnesses + derive `--selftest` green; the
      frozen set byte-clean; the agreement rate reported as consensus (NOT a new demo number); NO
      non-negotiable change

## Constraints

- MEASURE-FIRST: no tagging before the T1 probe + the user's model checkpoint. The T0 risk is real —
  many indicators are genuinely CROSS-CUTTING (structuring serves drug-trafficking AND fraud AND TF),
  so per-indicator-ONE-typology may merely RELOCATE the catch-all to indicator level.
- OVERLAY, not record edits: the typology lives in `data/indicator-typology-map.json` so all 56
  derived records + `derive_signals.py` (the grounding core) stay BYTE-FROZEN.
- Assign per UNIQUE indicator text (the Phase-34 method, ~589 unique of ~1,020) — same text → same
  typology by construction; kills cross-page inconsistency.
- HONESTY: verify as an INTER-RATER AGREEMENT rate (consensus, NEVER "proven correct"); the user
  adjudicates ambiguous CLUSTERS (the accepted truth source). Combined coverage = honest union
  arithmetic; no lift/dedup; the always-on "Illustrative data & outputs" badge stays. The agreement
  rate is a journal/quality artifact, not a new demo number.
- The ~1,231 single-typology indicators INHERIT their doc's typology at build time (free,
  deterministic); only the ~1,020 sector-page indicators need the neural assignment.

## Checkpoints

- After T1 (the probe): CHECKPOINT to the user — the MODEL (single primary typology / multi-label set /
  honest indicator-level "sector-general" bucket), the deterministic[section-heading]/neural split, and
  whether the 3 specific sector pages (casinos/real-estate/VC) fold in for consistency. No tagging until
  this lands.
- If the overlay can't keep the 56 derived records byte-frozen → STOP + re-confirm store-as-overlay vs
  Phase-34-style record edits.
- If T4 (the lens rewire) exceeds an M → STOP + split the synthesis sub-task.

## Assumptions

- The unique-text spine holds (~589 unique of ~1,020 in the 7 pages, per Phase 34's analysis). If
  false: the assignment surface is larger but the method is unchanged.
- Each live indicator carries a stable `id` (the grounding gate enforces indicator-id uniqueness) — the
  overlay keys on it. If false: key on doc-id + normalized-flag.
- The existing 27-term typology vocab mostly covers the sector-page indicators; a grounded extension is
  added only where a real typology is missing.

## Notes

- The T2 assign/verify is a strong Workflow candidate (the Phase 33/34 fan-out: assign per unique text →
  blind re-assignment → agreement → cluster adjudication). The user opts in at implementation.
- A doc may now contribute indicators to MULTIPLE typology clusters (a financial-entities page shows up
  under `corruption`, `terrorist-financing`, `structuring`…). The cross-corpus synthesis math changes
  from clustering whole DOCS to clustering INDICATORS by typology — but the combined-coverage union
  arithmetic already operates per-indicator, so the honesty invariant is preserved.
- `data/typology-map.json` stays for the doc HEADLINE chip; its 7 catch-all entries are repurposed to
  the doc's dominant indicator typology (deterministic) or retired. The Typologies CLUSTERS come from
  the per-indicator overlay, so `fintrac-sector-baselines` disappears as a cluster either way.
- KNOWLEDGE GAPS to verify at impl: the exact unique-text count + section-heading inventory across the
  7 pages (the T1 probe produces these); whether section→typology is deterministic enough to bound the
  neural surface.
