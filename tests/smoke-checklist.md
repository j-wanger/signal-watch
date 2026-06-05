# Smoke Checklist — stage rehearsal

Run before any presentation, **per typology you intend to present**. Automated checks cover
structure / schema / self-containment (`scripts/build.py` validates the config at the build
boundary and fails loud); this checklist covers what only a human eye can confirm: live visuals,
animation, pacing, keyboard control, and compliance framing.

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
