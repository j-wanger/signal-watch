# Smoke Checklist — stage rehearsal

Run before any presentation. Automated checks cover structure/equivalence/self-containment
(`scripts/build.py` + the node checks in the M1 verification); this checklist covers what only
a human eye can confirm: live visuals, animation, and pacing.

## Build & open
- [ ] `python3 scripts/build.py` prints `fentanyl -> dist/index.html`
- [ ] Open `dist/index.html` by **double-clicking the file** (true `file://`, no server)
- [ ] Header shows **Signal Engine** / AML Detection · Vision Prototype
- [ ] The amber **"Illustrative data & outputs"** badge is visible (top-right) on every act

## Walk the six-act arc (Next / Back)
- [ ] **Act 0 — Blind spot:** coverage map renders; gauge animates to **45%**; red rows visible
- [ ] **Act 1 — Read advisory:** advisory text streams with highlighted phrases; candidate signals appear staggered, count climbs
- [ ] **Act 2 — Assess coverage:** matrix renders; "build now" flags on the gap+available rows
- [ ] **Act 3 — Human review (GATE 1):** Next is **disabled with zero selected**; selecting a candidate enables it; label reads "Build selected (N) ›"
- [ ] **Act 4 — Agent builds (GATE 2):** spec card shows `PROPOSED · S-FLOW-THROUGH-RETAIL`; build log auto-advances to "Await human confirmation"; **Next confirms** → "Building…" → advances
- [ ] **Act 5 — Combination lift:** fire-stats animate (**1,240 / 18% / 83%**); three lift bars grow (weak→mid→strong)
- [ ] **Act 6 — Loop closes:** gauge animates **45% → 55%**; "▲ flow-through now covered" delta; recap chips

## Reset & loop
- [ ] On Act 6, Next reads "Run again ↺" and returns cleanly to Act 0 with selection reset
- [ ] Stepper rail: clicking a reached step jumps to it

## Offline / reliability
- [ ] Disconnect network, reload `dist/index.html` from `file://` — still runs; fonts fall back to system serif/sans/mono (no layout break)
- [ ] No console errors during a full run

## Compliance
- [ ] Every figure is illustrative; nothing reads as a real customer/transaction number
- [ ] Footer attributes the public FINTRAC / FinCEN advisories (paraphrased)

## Deferred to M3 (presenter polish — not yet implemented)
- [ ] Keyboard nav (←/→ / Esc-reset)
- [ ] `prefers-reduced-motion` honored
- [ ] Cross-browser pass on the actual presentation browser
