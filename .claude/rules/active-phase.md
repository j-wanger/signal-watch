# Active Phase Context

**Phase 62 — *Grounded probe-history consume (§12); §14 unfreeze STOOD DOWN at the T4 checkpoint*** (signal-watch-local, LITE) — IMPLEMENTED, DELIVERY-READY (direction gate taken 2026-06-20; all_accept:false). Consume aml-substrate's P22 "grounded probe-history" into signal-watch.

## Resolution (T1–T6 done; pending delivery acceptance)

The §12 consume landed cleanly; the §14 unfreeze authorized at the direction gate was **stood down at the T4 pause-checkpoint** — on evidence (the user accepted the boundary). The substrate's label-blind probe-history is the right source for §12 (firing/disposition MEASUREMENT) but the WRONG source for §14 (the triage console needs adjudicable FACT PATTERNS the substrate doesn't emit; its marquee TM-104 pair is C20, no substrate detector). **dist/triage stays BYTE-FROZEN; the only dist change is the launcher pin cascade (dist/index.html, 1 line — Phase-60 Option-A); `--check all` 8/8 throughout.** Delivered: the grounded fixture `data/probe-history/grounded/` (pinned substrate@ae98924), the `capability-tm-map.json` (selftested), `probe_history_stats.py --grounded`/`--selftest` (synthetic path byte-identical), the docs/probe-history.md grounded section + §14 boundary, and the cross-pillar pin re-ground to substrate@ae98924 (verified ZERO tier movement — reachable-now 171). Verified by an adversarial 4-lens pass (all hold). The original planned objective/scope (the unfreeze) is preserved below for context.

## Objective (as planned — the §14 unfreeze did NOT happen, see Resolution)

Substrate P22 projects `monitor/compose.Dossier` into a grounded `alert-history.json` (conformance-validated against a VENDORED copy of signal-watch's OWN `probe_history_stats.py` @58925a8). It REPLACES the SYNTHETIC Phase-48 probe-history fixture as the curate source for BOTH `probe_history_stats.py` (§12) AND `data/triage/scenarios.json` (§14). The alert/entity/cited-evidence side becomes GROUNDED in real substrate detection output; DISPOSITIONS stay label-blind ILLUSTRATIVE (never ground truth) — "grounded detection, illustrative dispositions". Substrate output is synthetic (`meta.synthetic:true`) → "no real data" holds.

## Scope

`data/probe-history/**` · `data/triage/**` · `data/capability-taxonomy.json` (read-only) · `scripts/curate_triage_scenarios.py` · `scripts/probe_history_stats.py` · `scripts/signal_coverage_map.py` + `scripts/e2e_chain_check.py` (pin re-ground only) · `scripts/build.py` (NO substrate import) · `dist/triage/**` (the SANCTIONED unfreeze) · `docs/**` · `.claude/rules/active-phase.md` · `HANDOFF.md` · `CLAUDE.md`.

## Key constraints

- **SANCTIONED ship-artifact UNFREEZE (USER OVERRIDE) — AUTHORIZED at the gate but STOOD DOWN at T4:** the §14 `dist/triage` unfreeze did NOT execute (the §12/§14 source boundary). `dist/triage` stayed BYTE-FROZEN. The ONLY dist that moved is the launcher `dist/index.html` (1 line — the Phase-60 Option-A pin cascade). The OTHER 7 dists byte-frozen.
- **Non-ship vs ship split:** §12 (`probe_history_stats.py`) is non-ship measurement; §14 (the triage curate → `scenarios.json` → `dist/triage`) is the ship side.
- **History-derived strata ONLY:** only fired-signal + below-the-line re-ground; novel + random strata stay AS-AUTHORED (byte-stable).
- **PAUSE-CHECKPOINTS:** T1 — if substrate P22 is uncommitted, PAUSE + ask the user to commit it (do NOT consume an uncommitted projector). T4 — if the grounded history doesn't map cleanly into the §14 strata OR breaks build-boundary validation, PAUSE + report (do NOT redesign the console to force the fit).
- **Honesty split (A3, delivery-checked):** dispositions are label-blind illustrative — never "real disposition rates"; the always-on "Illustrative data & outputs" badge stays; the user checks the framing at the delivery gate.
- **build.py NEVER imports the substrate** — tool-use produces the file (sanctioned, file-contract, NOT lifecycle-driving); build reads committed `data/` only. The C-code→TM-### namespace map is ship-load-bearing (every C-code resolves to a TM id or an explicit honest-null).

## Exit criteria

`build.py --check all` 8/8 at the new frozen state (ONLY `dist/triage` moved; `git diff --stat HEAD -- dist/` = only `dist/triage`); grounded `alert-history.json` committed + deterministic + schema-valid (P22 HEAD pinned); the C-code→TM-### map committed + selftested; `probe_history_stats.py` prints all 6 Role-2 metrics over the grounded file; `scenarios.json` re-curated (history-derived re-grounded, novel+random byte-stable, §14 grammar intact, curate `--selftest` green); `triage-console.test.mjs` green; no substrate import; cross-pillar pins moved to substrate@<P22> with `signal_coverage_map.py --check` byte-identical (reachable-now 171) + `e2e_chain_check.py --selftest` green.

## Abort

Any of the OTHER 7 dists drift / a build.py substrate import → STOP and surface. A C-code resolves to nothing AND the null isn't surfaced → out of bounds. A validator looks like it needs loosening → fix the data/design, never the check.

## Gates

- [x] Direction confirmed by user (assumption positions taken 2026-06-20; all_accept:false — A0 verify-first accept, A1 reject→revised-accept, A3 don't-know→delivery-checkpoint)
- [x] Delivery accepted (post-implementation report 2026-06-21; §12 consume + §14-frozen boundary + P22 pin re-ground; A3 framing accepted; committing + pushing to main)

Plan [[phases/phase-62-grounded-probe-history-consume]]; ledger Phase-62.
