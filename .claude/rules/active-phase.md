# Active Phase Context

Phase: 12 - FinCEN corpus derivation foundation (deterministic spine all-14 + LLM proof slice) — M7 — COMPLETE
(all 5 tasks [x], exit criteria MET in working tree; delivery gate pending commit). No next phase planned — run /dev-plan.
Objective: Backend for an expanded, singular FinCEN demo (eventual: user picks 1 of 14 advisories, watches the loop
derive coverage → build recommendations → signal). This phase = deterministic spine validated on ALL 14 + LLM-backend
(this session, no key) derivation proven on a 2-advisory slice. Demo expansion (selection UI + build-rec render) = Phase 13.

Scope: scripts/derive_signals.py, .gitignore, data/fincen/*.md (14 committed), data/fincen/derived/*.json (new),
README.md, CLAUDE.md. Engine index.html + build.py + config/schema.md UNTOUCHED (backend-only).

Delivered (verified in working tree):
- 14 corpus md committed; `extract_red_flags` generalized to a section-FINDER (Tier-1 + Tier-2 fallback + filters);
  `--corpus` validates all 14 → 7 CLEAN · 3 LOW · 4 NEEDS (2 NEEDS = FATF jurisdiction advisories = correct).
- Deterministic checks: `build_rec_category` (cover×data matrix) + `check_record` (consistency + traceability + BUILD_NOW⇒logic), in `--selftest`.
- LLM-backend (this session, NO key) derived 2 records: fin-2022-a001 (kleptocracy, 5 ind, 2 BUILD_NOW) + fin-2024-a002 (PRC precursors, 14 ind, 4 BUILD_NOW); both pass `--check-derived`.
- EFE `--selftest` still 12+12; `git diff index.html` empty; `build.py --check all` zero drift; anthropic LAZY.
- DOCUMENTED: the spine ASSISTS but does not AUTOMATE — a complete record still needs LLM-backend authoring (CLAUDE+README).

Open follow-ups (Phase 13 / Future): demo scope expansion (advisory-selection UI + build-rec render = Phase 13);
glued-list splitting for the 2 no-blank-separator NEEDS advisories; exclude the 2 FATF advisories from the derivable
corpus; scale LLM-backend derivation to the remaining 5 CLEAN advisories; residual extraction artifacts (intro-tail).

Gates:
- [x] Direction confirmed by user (backend-only foundation; user chose it over a minimal selectable demo view — 2026-06-05)
- [ ] Delivery accepted (post-implementation report) — flips after the commit verifiably lands (D3)
