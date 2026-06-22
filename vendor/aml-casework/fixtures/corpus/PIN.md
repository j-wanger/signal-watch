# Vendored corpus snapshot — pinned

**Pin:** `signal-watch@a75a136`
**Source:** `signal-watch:data/fincen-alerts/derived/`
**Vendored via:** `git show a75a136:<path>` (the pinned blob, not a working-tree copy)

These are read-only, pinned copies of the FROZEN signal-watch corpus indicators that the casework
fixtures ground against. The corpus-grounding verifier (`src/aml_casework/corpus_grounding.py`)
reads them as DATA — it never imports signal-watch engine code, and it never writes signal-watch.

## Contract

- **Do NOT hand-edit these records.** The oracle is upstream (`signal-watch@a75a136`). A casework
  fixture whose `grounding.flag` fails to ground here is a SURFACED violation — never a license to
  edit the snapshot to make it pass.
- **Re-vendor only deliberately.** If signal-watch re-baselines and we choose to move the pin, copy
  the new pinned content with `git show <new-ref>:<path>`, update the pin above and `CORPUS_PIN`,
  and re-run the suite. The drift check (`check_corpus_drift`) surfaces when the live sibling has
  moved off this snapshot so a re-baseline is visible, not silent.

## Vendored records

- `fincen-alerts/derived/fin-2026-alert001.json` — carries `IND-11` (capability C4, data_source D2)
- `fincen-alerts/derived/fin-2023-alert006.json` — carries `IND-04` (capability C15, data_source D8)
- `fincen-alerts/derived/fin-2020-alert001.json` — carries `IND-05` (capability C3 funnel/fan) — added Phase 6
- `fincen-alerts/derived/fin-2023-alert001.json` — carries `IND-03` (capability C2 pass-through) — added Phase 6
- `fincen-alerts/derived/fin-2022-alert002.json` — carries `IND-08` (capability C5 cash-placement) — added Phase 6

The Phase-6 trio grounds the C2/C3/C5 alerts of the first REAL consumed bundle (CASE-P-0010361, a
5-typology mule). Each record's indicator flag was confirmed at vendor time to CONTAIN the bundle's
verbatim `grounding.flag` under `normalize()` (the corpus-grounding contract).
