# Smoke Checklist — stage rehearsal

Run before any presentation, **per typology you intend to present**. Automated checks cover
structure / schema / self-containment (`scripts/build.py --check` validates the config at the build
boundary and fails loud) and the corpus explorer's 5-screen arc behavior
(`node tests/corpus-explorer.test.mjs` — see the corpus-explorer note below); this checklist covers
what only a human eye can confirm: live visuals, animation, pacing, keyboard control, and compliance
framing.

Engine chrome (header, badge, the six-act arc, both human gates, the gate labels) is **identical
across typologies** — it lives in the generic engine, not the config. Only the six values in the
**per-typology table** below change. Walk the arc once per typology, reading expected values from
that table.

## Per-typology expected values

| Act / element | `fentanyl` | `trade-based` |
|---|---|---|
| Act 0 — Coverage index gauge | **45%** | **35%** |
| Act 4 — Spec card signal name | `S-FLOW-THROUGH-RETAIL` | `S-PRICE-ANOMALY-TRADE` |
| Act 5 — Fire-stats (count / standalone / best-combo) | **1,240 / 18% / 83%** | **1,860 / 22% / 81%** |
| Act 5 — Lift bars (weak → mid → strong) | **18 → 64 → 83** | **22 → 58 → 81** |
| Act 6 — Gauge animates | **45% → 55%** | **35% → 45%** |
| Act 6 — Delta chip | ▲ flow-through now covered · courier queued | ▲ price-anomaly now covered · phantom-shipment queued |

> Source of truth: `config/typologies/<id>.json` (gauge % is derived by the engine as
> `round((covered·1 + partial·0.5) / N · 100)`; the rest are config fields). If you add a typology,
> add a column.

## Build & open
- [ ] `python3 scripts/build.py <id>` prints `<id> -> dist/<id>/index.html` (or `all` to build every typology)
- [ ] **Drift guard:** `python3 scripts/build.py --check all` reports **zero drift** — every committed `dist/<id>/index.html` still equals a fresh build of its config (guards all 3 shipped typologies; non-mutating). Catches a stale-dist commit before it reaches the stage. Belt-and-suspenders: `git status --porcelain dist/` is also clean (flags a stray/untracked dist file that `--check` won't)
- [ ] Open `dist/<id>/index.html` by **double-clicking the file** (true `file://`, no server)
- [ ] Header shows **Signal Watch** / AML Detection · Vision Prototype *(shared chrome)*
- [ ] The amber **"Illustrative data & outputs"** badge is visible (top-right) on **every** act *(shared chrome)*

## Corpus explorer (`dist/corpus/`) — automated arc check + human walk
- [ ] **Automated arc (structural pre-present check):** `node tests/corpus-explorer.test.mjs` exits **0** —
  drives the committed `dist/corpus/index.html` through the 5-screen arc under a dep-free DOM shim and
  asserts the invariants (the human gate's div-toggle selection, the two honest Signal empty states, the
  close-the-loop coverage math + no indicator mutation, reduced-motion single-paint, 0-picked flat-hold).
  Run it after any `corpus.html` edit + rebuild; it doubles as a build-output smoke test for the corpus dist.
- [ ] Open `dist/corpus/index.html` (`file://`): pick a **derived** advisory → walk **Select → Coverage →
  Build recs (gate) → Signal → Close the loop**; deselect a build-now row and confirm the Signal cards +
  the closing coverage rise both shrink to match (the automated check pins this, but eyeball it on the
  presentation browser).
- [ ] **Capabilities mode (Phase 29):** on Select, click the **Capabilities** toggle (third button, after
  Documents / Typologies). Confirm: one card per detection capability, each with a posture chip
  (**in place / partial / not yet**), an honest indicator-demand count + a covered/partial/gap micro-bar;
  the list is **gap-priority** sorted (not-yet capabilities lead). Click a capability → its indicators
  appear grouped by source document with a coverage gauge + a "Depends on data" row; click a document row
  to **drill into that doc's per-doc arc**, then **Back** returns to the capability (not the picker). No
  fabricated number — only honest counts + the always-on "Illustrative data & outputs" badge.
- [ ] **Data sources mode (Phase 30):** on Select, click the **Data sources** toggle (fourth button, after
  Documents / Typologies / Capabilities). Confirm: one card per data source, each with a data-access posture
  chip (**available / partial / not yet**), an honest indicator-demand count + a covered/partial/gap micro-bar;
  the list is **gap-priority** sorted (not-yet feeds lead — the data-access exposure). Click a data source →
  its indicators appear grouped by source document with a coverage gauge + an **"Implements capabilities"** row
  (the inverse of the capability view); click a document row to **drill into that doc's per-doc arc**, then
  **Back** returns to the data source (not the picker). No fabricated number — only honest counts + the
  always-on badge. (Sanity: the lens is genuinely distinct — at least one feed reads **"not yet"**.)

## Adverse-media / negative-news stream (`dist/news/`) — M8, Phase 31 + Phase 32
- [ ] **Automated arc:** `node tests/news-stream.test.mjs` exits **0** — drives the committed
  `dist/news/index.html` through the screening arc (Select → Read → Screen → Disposition → Exposure) +
  the fuzzy matcher under a dep-free DOM shim, both motion modes (**65 assertions** — reduced-motion final
  state + a full-motion enriched-shim drive of the stream + scan). Run after any `news.html` edit + rebuild
  (`python3 scripts/build.py news`); it doubles as a build-output smoke test.
- [ ] Open `dist/news/index.html` (`file://`): the **"Illustrative data & outputs"** badge is visible; the
  Select screen lists the **real enforcement articles** with an honest source chip (DOJ / OFAC) and stat
  tiles. A **step rail** (Select › Read › Screen › Disposition › Exposure) shows where you are. Pick the
  **OFAC TGR Group** article.
- [ ] **Read (streaming):** under full motion the source **streams in** (a blinking caret trails the read);
  each red-flag phrase **highlights** (amber) as the read reaches it and each named entity is **tagged**
  (green); **entity cards** reveal alongside with grounded **location / age / profession**, the **typology**
  is shown, a natural-AML `red_flag` translation sits beside each verbatim quote, and the **source
  attribution** (public domain, 17 U.S.C. §105) is shown. Reduced-motion shows the same final state at once.
- [ ] **Screen (scan process):** the book is **swept** — each entity scored against every row, ranked across a
  **threshold line**. **Siam Expert Trading Company Limited = 1.000 (EXACT)** — a counterparty *is* a
  designated entity; near-matches an exact-name screen would miss surface too (**Pullman ≈ 1.000** suffix,
  **Ekaterina Zhdanova ≈ 0.989**). No percentage / precision figure is shown.
- [ ] **Disposition (the human gate):** hits default to **CONFIRMED**; the common-name collision
  **George Rossi (1.000)** is present with its dismiss note — click it to **DISMISS** it (a different person;
  high score ≠ confirmation). Toggles respond to click and to Space/Enter when focused; ←/→ still navigate.
- [ ] **Exposure:** after dismissing the trap, **confirmed = 3, dismissed = 1**; the confirmed hits are
  framed as adverse-media **atoms** (the compose-with-the-transaction-signal north star is named).
- [ ] Keyboard: **→ next · ← back · Esc** returns to the article list. No console errors (both motion modes).
- [ ] Compliance: the source **articles are real US-federal public-domain enforcement records** (DOJ + OFAC,
  verbatim under 17 U.S.C. §105); the client/counterparty **book is synthetic** (no real customer data);
  scores are real computed similarity; nothing reads as a real detection/precision rate.

## Walk the six-act arc (Next / Back) — read values from the table
- [ ] **Act 0 — Blind spot:** coverage map renders; gauge animates to the **table value**; red (not-covered) rows visible
- [ ] **Act 1 — Read advisory:** advisory text streams with highlighted phrases; candidate signals appear staggered, count climbs
- [ ] **Act 2 — Assess coverage:** matrix renders; "build now" flags on the gap+data-available rows
- [ ] **Act 3 — Human review (GATE 1):** Next is **disabled with zero selected**; selecting a candidate enables it; label reads "Build selected (N) ›" *(shared)*
- [ ] **Act 4 — Agent builds (GATE 2):** spec card shows `PROPOSED · <table signal name>`; build log auto-advances to "Await human confirmation"; **Next confirms** → "Building…" → advances
- [ ] **Act 5 — Combination lift:** fire-stats animate to the **table values**; three lift bars grow weak→mid→strong to the **table values**
- [ ] **Act 6 — Loop closes:** gauge animates the **table delta**; the **table delta chip** shows; recap chips render

## Presenter controls (M3 — keyboard nav, reset)
- [ ] **→ / Space** advances; **←** goes back — but **both gates still hold** (→ does nothing on Act 3 with zero selected, or on Act 4 before confirm)
- [ ] **Esc** resets to a clean Act 0 (selection cleared, gauge back to the base table value)
- [ ] On-screen **↺ Reset** control does the same as Esc; the key legend is visible
- [ ] Stepper rail: clicking a reached step jumps to it
- [ ] On Act 6, Next reads "Run again ↺" and returns cleanly to Act 0 with selection reset

## Reduced motion (M3 — `prefers-reduced-motion`)
- [ ] With OS "Reduce motion" **on** (macOS: System Settings → Accessibility → Display), reload from `file://`
- [ ] Every act lands in its **final state in one paint** — no animation, gauge/stats/bars show final table values immediately; no pending timers left running

## Offline / reliability
- [ ] Disconnect network, reload `dist/<id>/index.html` from `file://` — still runs; fonts fall back to system serif/sans/mono (no layout break)
- [ ] No console errors during a full run (check with reduced-motion **on** and **off**)
- [ ] Cross-browser: confirm on the **actual presentation browser** (target: Chrome / macOS)

## Compliance (hard gate — see T3 / HANDOFF §4)
- [ ] Every figure is illustrative; nothing reads as a real customer/transaction number
- [ ] Advisory text is **paraphrased + public-source**, and the footer/source line attributes it:
  - `fentanyl`: FINTRAC Operational Alert on illicit synthetic opioids (Jan 2025)
  - `trade-based`: FinCEN Alert on fentanyl-linked trade-based laundering (Apr 2025) · FATF TBML trends & developments (2024)
- [ ] No secrets/keys anywhere in the shipped file

---

## M5 ship — compliance self-check record (automated, 2026-06-04)

Deterministic gate run against both shipped `dist/<id>/index.html`. **Result: PASS.**

- ✅ Zero drift — now an automated guard (see **Build & open** above): `build.py --check all` confirms every committed `dist/<id>/index.html` equals a fresh build; `git status --porcelain dist/` clean (shipped = source = HEAD).
- ✅ Badge `Illustrative data & outputs` present in both (persistent header chrome → on every act).
- ✅ Self-contained for `file://`: no `<script src>`, no `fetch()`, no unresolved `__CONFIG__`; `const CONFIG` inlined; boot `goto(0)` present. Only external ref is the Google Fonts `<link>` (degrades to system fonts offline).
- ✅ Advisories paraphrased + public-source, attributed in both (fentanyl: FINTRAC Jan-2025 · trade-based: FinCEN Apr-2025 / FATF TBML 2024).
- ✅ No secrets/keys; no real-data/PII (no emails, no ≥9-digit runs, no card/SSN patterns). All figures are config-sourced illustrative numbers.
- ↪ Runtime render (Act 0, no console errors) was verified on real Chrome 149 × both motion modes at **M3**; these dist bytes are unchanged since (zero drift), so that pass carries. Re-run the live walk above before any presentation.
