# Typology Config Schema

The engine (`index.html`) is generic. All typology-specific content lives in one config
object per typology, `config/typologies/<id>.json`, validated against this contract. Adding
a typology = adding one JSON file + `python3 scripts/build.py <id>`. No engine edits.

> **Build:** `scripts/build.py` inlines the chosen JSON at the `__CONFIG__` injection point
> in `index.html` → `dist/index.html` (single self-contained file, runs from `file://`).
> No `fetch()`, no ES modules in the ship file.

## Conventions

- **HTML allowed in copy fields** (`hook_lead`, `lift_rationale`, advisory `t`, etc.): they
  are injected via `innerHTML`. Use `&lt;` for a literal `<` inside text (as the logic/lift
  strings do) so it doesn't start a tag.
- **Enums:** `status ∈ covered | partial | gap` · `type ∈ entity | relationship | motif` ·
  `cover ∈ covered | partial | gap` · `data ∈ available | partial | insufficient` ·
  `strength ∈ weak | mid | strong`.
- **Buildable candidate** = `cover:"gap" AND data:"available"` (drives the Act 2 "build now"
  flag and Act 3 selectability). Derived — not stored.
- **Target** = the single row to build. Flag exactly one indicator and one candidate with
  `target: true`. The engine derives the Act 4 subject (target candidate) and the Act 6
  now-covered indicator from these flags — do not hardcode ids.
- **Coverage index** (Act 0 gauge, Act 6 before/after) is **derived** from indicator statuses
  (`covered`=1, `partial`=0.5, `gap`=0), not stored — prevents drift.

## Top-level fields

| Field | Req | Type | Notes |
|-------|-----|------|-------|
| `id` | yes | string | kebab id, matches filename stem |
| `label` | yes | string | human label for selectors |
| `steps` | yes | string[7] | stepper rail labels, exactly one per act (act0…act6); RENDER is fixed at 7 acts |
| `next_labels` | yes | string[≥7] | Next-button label per act (+ conventional 8th "Run again"); engine indexes 0–6 |
| `hints` | yes | string[≥7] | control-bar hint per act ("" allowed); engine indexes 0–6 (baseline carries a trailing 8th) |
| `brand` | no | `{title, subtitle}` | header chrome; defaults to "Signal Watch" / "AML Detection · Vision Prototype" |
| `badge` | no | string | always-visible trust badge; default "Illustrative data & outputs" |
| `anchor` | yes | object | see below — typology-specific narrative copy |
| `coverage` | yes | `{indicators: Indicator[]}` | Act 0 map + Act 6 close; before/after derived |
| `advisory_stream` | yes | Segment[] | Act 1 streamed advisory (paraphrased, public-source) |
| `advisory_full` | no | object | Act 1 verbatim source document (public-domain); see below. When present, replaces the paraphrased stream in the SOURCE DOCUMENT panel |
| `candidates` | yes | Candidate[] | Act 1 extraction, Act 2 matrix, Act 3 gate, Act 4 spec |
| `lift` | yes | LiftBar[] | Act 5 combination-lift bars |
| `stats` | yes | `{fire_count, standalone_precision, best_combo_precision}` | Act 5 fire-stat numbers (integers) |

### `anchor`

| Field | Req | Notes |
|-------|-----|-------|
| `hook_eyebrow` | no | Act 0 eyebrow; default generic |
| `hook_title` | yes | Act 0 `<h2>` (HTML ok; italic `<em>` segment allowed) |
| `hook_lead` | yes | Act 0 lead paragraph — **names the typology** (HTML ok) |
| `close_title` | yes | Act 6 `<h2>` (HTML ok) |
| `close_delta` | yes | Act 6 gauge delta line (e.g. "▲ flow-through now covered · courier queued") |
| `coverage_noun` | yes | short noun for the gauge captions ("of known &lt;coverage_noun&gt;" in Act 0, "&lt;coverage_noun&gt;" in Act 6) |
| `lift_rationale` | yes | Act 5 "Why this matters" body — names the composed signals (HTML ok) |
| `source` | yes | footer + Act 1 doc attribution; public advisory, paraphrased |

### `Indicator` (coverage.indicators[])

`{ id, label, status, target?, sub? }` — `status` enum; one row `target:true` (the gap being
built); `sub` optional mono subline.

### `Segment` (advisory_stream[])

`{ t, hl? }` — `t` is a text chunk; `hl:true` highlights it. Whitespace in `t` is significant
(segments are concatenated verbatim during the stream).

### `advisory_full` (optional)

`{ source, text?, text_file?, highlights? }` — a VERBATIM public-source document (e.g. a
FinCEN advisory; U.S. federal works are public domain under 17 U.S.C. §105). Rendered whole and
scrollable in Act 1's SOURCE DOCUMENT panel, with the `source` attribution shown **distinct
from** the always-on "Illustrative data & outputs" badge — the advisory is genuine, not
illustrative. Verbatim reproduction covers US-federal works (FinCEN, OFAC — public domain, 17 U.S.C.
§105) and, since Phase 22, FINTRAC (Canadian Crown copyright, reproduced for non-commercial use with
attribution per FINTRAC's Terms & Conditions — a licence, not public domain); every other non-US /
non-FINTRAC source still paraphrases.

- `source` — required attribution caption (e.g. `FinCEN FIN-2022-A002 · Advisory on Elder Financial Exploitation`).
- `text` — the verbatim body inline; **or**
- `text_file` — a repo-relative path to the markdown corpus file (e.g. `data/fincen/fin-2022-a002.md`).
  The build reads it, strips the leading HTML-comment provenance header, and inlines the body —
  keeping the markdown corpus the single source of truth (no duplication). Provide `text` **or** `text_file`.
- `highlights` — optional `string[]` of EXACT substrings of the verbatim text (the red-flag phrases
  that became signals). The engine wraps each occurrence in `<span class="hl">` and, on reveal,
  scrolls the first highlight into view — tying the source document to the extracted signals. Use
  single-line fragments with no curly quotes/apostrophes so the match is robust.

Act 1 renders this as the "agent reading" beat: it types a capped opening (processing feel), then
reveals the full body with `highlights` applied, then extracts the candidate signals. Body text is
escaped + injected (highlights are the only markup); markdown line structure is preserved via
`white-space: pre-wrap`. Absent or malformed → the panel falls back to the paraphrased
`advisory_stream` (defensive rendering).

### `Candidate` (candidates[])

`{ id, name, type, cover, data, target?, definition? }`. `definition` is required on the
`target:true` candidate (drives the Act 4 spec card), optional/absent otherwise:

`definition = { signal_name, class, features: string[], logic, window, source, route }`
- `signal_name` — proposed signal id shown in the Act 4 spec header (e.g. `S-FLOW-THROUGH-RETAIL`).
- others map 1:1 to the spec rows. `logic` may contain `&lt;`.

### `LiftBar` (lift[])

`{ name, combo, value, strength }` — `value` 0–100 (bar width + animated %); `strength` enum
selects the bar gradient. Order weakest→strongest; first is the new signal alone.

## Validation (defensive rendering)

`validateConfig()` in the engine fills defaults for optional fields and renders a labeled
placeholder for a missing/malformed required section rather than throwing (which would blank
the stage). A config that omits `lift`, for example, still renders the other acts.
