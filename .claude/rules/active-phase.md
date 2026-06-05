# Active Phase Context

Phase: 11 - Automated derivation (LLM-drafted signal config) — AUTOMATE — COMPLETE (all 5 tasks [x],
exit criteria MET in working tree; delivery gate pending commit). No next phase planned — run /dev-plan.
Objective: Automate the article→signal derivation proven MANUALLY in Phase 7. Authoring-only
`scripts/derive_signals.py`: DETERMINISTIC layer (`extract_red_flags` + `scaffold_config`, stdlib,
`--selftest`/`--scaffold`, offline) + NEURAL layer (`--draft`, env-keyed) PROPOSING the judgment fields
(status, the one `target:true`, the signal `definition`) via the Anthropic API. LLM proposes a
`.draft.json`; build.py + schema + the two human gates DISPOSE.

Scope: scripts/derive_signals.py (new), scripts/requirements-authoring.txt, .gitignore,
config/typologies/*.draft.json (gitignored scratch), README.md, CLAUDE.md. index.html + build.py UNTOUCHED.

Delivered (verified in working tree):
- `--selftest` extracts 24 EFE red flags (12 behavioral + 12 financial), exit 0, offline, stdlib-only.
- `--scaffold` emits a schema-shaped `<id>.draft.json` SKELETON (indicators line-traced, no target/definition).
- `--draft` (env-keyed; `anthropic` LAZY from the authoring venv) proposes the judgment fields; the
  Anthropic structured-output shape (claude-opus-4-8 + `output_config.format` json_schema) verified
  against the claude-api reference. Live network call unexercised (no key) — recorded-manual-run pattern.
- Boundary holds: build.py REJECTS the bare skeleton naming the 2 judgment gaps; ACCEPTS a filled draft.
- `git diff index.html` empty; `build.py --check all` zero drift; anthropic absent from engine/build imports.
- Documented in docstring + README + CLAUDE. Review gate 9/10 accept (2 MEDIUMs on the `--draft` path).

Open follow-ups (Future candidates): `--draft` live-path hardening (thinking/effort + refusal/max_tokens
handling); run `--draft` end-to-end on a NEW advisory with a real key; elder presentation-values true-up;
fentanyl re-point to fin-2024-a002; manifest `--fetch` cadence.

Gates:
- [x] Direction confirmed by user (AUTOMATE → variant B; user overrode planner's finish-first + deterministic-only recs — 2026-06-05)
- [ ] Delivery accepted (post-implementation report) — flips after the commit verifiably lands (D3)
