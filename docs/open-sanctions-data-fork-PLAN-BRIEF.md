# PLAN-BRIEF — open sanctions datasets: the ship-compliance license matrix + the non-commercial boundary

> **Authored Phase 81 (2026-06-28).** The user's directive: *"plan for open sanctions datasets — we will
> not use for commercial purposes."* This brief is the SIGNAL-WATCH **ship-compliance** companion to the
> substrate-side [`substrate-open-reference-data-fork-PLAN-BRIEF.md`](substrate-open-reference-data-fork-PLAN-BRIEF.md)
> (which covers anchoring substrate's *synthetic* universe to open reference data — the data-GENERATION side).
> The distinct question here: **which sanctions sources may enter a signal-watch SHIP or COMPANION artifact**,
> given the demo's purpose, and where the non-commercial boundary actually bites. **Not legal advice — a
> compliance MAP to take to counsel.** No rate, score, or multiplier is claimed anywhere.

## The boundary that decides everything: is the demo "commercial"?

signal-watch is a **vision prototype for stakeholder buy-in** — shown to prospective bank customers to win the
program. That PURPOSE is plausibly **commercial / business use** even when the *intent* is "not for production
screening." So a non-commercial-only licence (CC-BY-NC) is **risky to ship in the demo artifact**, regardless of
the non-commercial intent — the use is downstream-commercial by purpose. This is the load-bearing call:

- **The compliance-clean path is the underlying PUBLIC-DOMAIN / OPEN-GOVERNMENT source lists** — NOT a
  value-added non-commercial *consolidation*. You do not need OpenSanctions' CC-BY-NC consolidation to get
  real sanctions-name realism; the government source lists are openly licensed and ship clean.
- **OpenSanctions (the consolidated graph) stays PLAN-ONLY / no-ship** for this artifact — companion-or-plan,
  never in a `dist/`. (substrate may license it internally for *its own* anchoring if it ever needs the FtM
  graph — that is the other brief's Stage-3 decision, internal-only, re-examined on redistribution.)

## The per-source license matrix (ship-compliance, signal-watch artifacts)

| Source | Licence | Ship in an offline demo artifact? | Notes |
|---|---|---|---|
| **OFAC SDN / Consolidated** (US Treasury) | **US-federal public domain — 17 USC §105** | **SHIP — clean, verbatim OK** | The existing CLAUDE.md exception explicitly covers OFAC (US Treasury). What signal-watch already uses (via substrate's `watchlist_ofac.csv` reference, label-blind false-positive trap). |
| **FinCEN advisories** (US Treasury) | US-federal public domain — 17 USC §105 | SHIP — verbatim OK | Already corpus source #1 (the US-federal exception). |
| **UK HMT / OFSI / FCDO UK Sanctions List** | **Open Government Licence v3.0 (Crown copyright)** | **SHIP — with OGL attribution** | Attribution string required (© Crown copyright, OGL v3.0 link). NOTE: the OFSI *Consolidated List* CLOSED 28 Jan 2026 → the **UK Sanctions List** is now the single source (the matrix must track source moves). Mirrors the FINTRAC OGL-with-attribution pattern signal-watch already ships. |
| **Consolidated Canadian Autonomous Sanctions List** | Canada OGL-equivalent (free, attribution) | SHIP — with attribution | The Canadian-bank audience's home jurisdiction; attribution like the FINTRAC Crown-copyright footer. |
| **EU Consolidated Financial Sanctions List** | **© European Union — conditional** (Commission reuse decision + attribution; liability disclaimer) | **CONDITIONAL — verify with counsel before ship** | Free to download, reuse permitted with attribution under the EU reuse framework, but NOT public domain. Treat as ship-able-with-care, counsel-confirmed; otherwise paraphrase / reference. |
| **UN Security Council Consolidated List** | **UN — conditional** (no open licence surfaced; permission/attribution via the UN Secretariat) | **CONDITIONAL — verify; default paraphrase** | No clear open reuse licence. Default to reference/paraphrase unless the UN terms are confirmed. |
| **OpenSanctions** (consolidated FtM graph / PEPs) | **CC-BY-NC 4.0** ("any business purposes requires a licensing agreement") | **NO-SHIP** (no CC-BY-NC bytes in any signal-watch repo/dist/companion) | The demo's buy-in purpose is plausibly commercial → CC-BY-NC bites. Use the government SOURCE lists above instead; OpenSanctions only if the *consolidated graph itself* is ever specifically needed, internal-only, licensed. |

**The honesty caveat (carried from CLAUDE.md's non-negotiables):** the always-on "Illustrative data & outputs"
badge stays; any real sanctions NAME shipped is framed STRICTLY as the **false-positive-trap** entity-resolution
illustration (a synthetic party's name *collides* with a listed name — the synthetic party is NEVER the listed
entity; never "we caught a sanctioned party"). This is the Phase-80/81 framing and it is the SHIP rule for any
real listed name.

## What this changes for signal-watch (the plan)

1. **No new sanctions dataset is integrated this phase** (the user's "plan for" — plan, not integrate). signal-watch
   already ships real OFAC NAMES (via substrate's PD `watchlist_ofac.csv`, the Phase-80 person merge class + the
   Phase-81 measurements) — the PD path is already exercised and compliance-clean.
2. **If a future phase broadens cross-jurisdiction sanctions realism**, the ship-safe order is: OFAC PD (have it) →
   UK Sanctions List OGL (+ attribution) → Canadian Consolidated List (+ attribution) → THEN counsel-gated EU/UN.
   **OpenSanctions stays out of the ship/companion path.**
3. **The substrate side** (anchoring synthetic entities to real listed names so a screen genuinely hits) is the
   other brief's **Stage-2** seam-5 — already partially landed (substrate uses the PD OFAC SDN as a label-blind
   collision reference). The cross-jurisdiction extension (UK/Canada/FATF anchors) is substrate-side work, governed
   by the SAME per-source matrix, internal-only (substrate emits synthetic data; no real list ships from substrate
   either).

## Boundary + out of scope

- **No CC-BY-NC bytes enter any signal-watch repo, dist, or companion** (the Phase-81 abort rule).
- **Counsel-gated:** the EU/UN "conditional" rows + the "is the buy-in demo commercial" question are **legal calls**,
  not engineering calls — this brief maps them, it does not decide them. Verify before any EU/UN list or any
  CC-BY-NC source touches a shippable surface.
- **Out of scope:** integrating any real cross-jurisdiction dataset (plan-only this phase); the substrate-side
  anchoring (the other brief); a sanctions DETECTION claim (substrate's `sanctions_flag` is label-blind, corr≈0 —
  the Phase-81 finding; a sanctions hit is a screening/false-positive illustration, never a detection claim).
