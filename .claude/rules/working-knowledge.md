# Working Knowledge

- [uses: 2] FinCEN advisory structure is a reusable template: typology overview → enumerated red-flag indicators (split behavioral vs financial) → SAR filing instructions with a designated key term + SAR field references. The enumerated red-flag list is the derivation surface for a detection signal. (Phase 11: this is the surface `extract_red_flags(md)` deterministically parses — Behavioral/Financial section anchors.)
  source: [[wiki:money-laundering-red-flags]] | activated: 2026-06-05
- [uses: 2] Red-flag→signal derivation pattern (project-local, applies to every typology): advisory red flag → coverage.indicator (status covered/partial/gap, exactly one target:true) → buildable candidate (cover:"gap" AND data:"available") → target candidate.definition {signal_name, class, features[], logic, window, source, route}. (Phase 11: scaffold_config emits the indicators deterministically; the LLM --draft proposes status + the one target + the definition; build.py disposes.)
  source: config/schema.md (project) | activated: 2026-06-05 | tier: 3
