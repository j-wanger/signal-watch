# Working Knowledge

- [uses: 1] FinCEN advisory structure is a reusable template: typology overview → enumerated red-flag indicators (split behavioral vs financial) → SAR filing instructions with a designated key term + SAR field references. The enumerated red-flag list is the derivation surface for a detection signal.
  source: [[wiki:money-laundering-red-flags]] | activated: 2026-06-04
- [uses: 1] Red-flag→signal derivation pattern (project-local, applies to every typology): advisory red flag → coverage.indicator (status covered/partial/gap, exactly one target:true) → buildable candidate (cover:"gap" AND data:"available") → target candidate.definition {signal_name, class, features[], logic, window, source, route}.
  source: config/schema.md (project) | activated: 2026-06-04 | tier: 3
