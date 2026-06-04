# Architecture: AML Signal Engine — Vision Demo

> Last updated: 2026-06-04T19:15:46 by /dev-init

## Directory Layout

signal-watch/
  aml_vision_demo_fentanyl.html   # baseline single-file demo (vanilla HTML/CSS/JS)
  CLAUDE.md                       # always-loaded non-negotiables
  README.md                       # run / present / compliance
  HANDOFF.md                      # full context, content model, milestone plan
  .dev-wiki/                      # lifecycle tracking (this wiki)

Target structure (grows with milestones — HANDOFF §3.3): config/, src/, scripts/,
dist/, data/ (optional), backend/ (optional), tests/.

## Module Responsibilities

| Module | Purpose | Key Entry Points | Inputs | Outputs |
|--------|---------|-----------------|--------|---------|
| aml_vision_demo_fentanyl.html | Six-act scripted walkthrough; state machine + render dispatch + animations, all inline | `goto(0)` (bottom of `<script>`) | Google Fonts (online; degrades) | rendered DOM |

Inside the file: content arrays `STEPS`/`INDICATORS`/`ADVISORY`/`CANDIDATES`/`LIFT`;
state `act`/`selected`/`confirmed`; `goto(i)`, `updateControls()`, `act0()`…`act6()`
dispatched via the `RENDER` array. Theme in `:root` CSS variables.

## Dependencies

| Package | Version | Role |
|---------|---------|------|
| (none) | — | No build, no runtime deps. Google Fonts via `<link>`, degrades to system fonts offline. |

## Data Flow

| Module | Reads (data) | Writes (data) | Env Vars | Notes |
|--------|-------------|---------------|----------|-------|
| demo | inline JS arrays (synthetic, illustrative) | DOM | — | No external/customer data, ever |

## Development Toolchain

| Category | Tool | Config Path | Status |
|----------|------|-------------|--------|
| Build System | none (M1 adds stdlib inline/concat) | — | not detected |
| Dev Server | python3 -m http.server (optional, iteration only) | — | configured (no files) |
| Version Control | git | .git/ | detected |

## Related

- HANDOFF.md (§3 target shape, §5 content model) · CLAUDE.md (non-negotiables)
