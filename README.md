# AML Signal Engine — Vision Demo

A presenter-driven, offline, browser-based **vision prototype** for AML stakeholder
buy-in. It is a scripted, reliable dramatization of a signal/atom monitoring loop —
**not** a working detection system. Every figure shown is illustrative and labelled
as such.

The walkthrough, in six acts:

> read a regulatory advisory → extract candidate signals → assess coverage against
> our library + data → **human selects** what to build → agent drafts a signal
> definition → **human confirms** → backtest → reveal **combination lift** →
> coverage closes → loop repeats.

The persuasion lives in two human-in-the-loop gates (trust) and the combination-lift
reveal (why composed atoms beat monolithic scenarios).

## Run it

No build, no server, no dependencies (except a Google Fonts `<link>` when online).

```
open aml_vision_demo_fentanyl.html      # macOS — or just double-click it
```

It runs offline from `file://`. Fonts fall back to system serif/sans/mono if offline.

## Present it

- Open the file in the presentation browser, fullscreen.
- Drive it with the on-screen **Back / Next** buttons; the stepper rail at the top is
  clickable to jump to any act already reached.
- **Act 3** (Human review) requires you to select at least one candidate before Next
  enables — this is the first human gate. **Act 4** (Agent builds) waits on your
  confirm — the second gate. Don't skip these; they are the point.
- The final act loops back to the start (**Run again**) for a clean reset between runs.

Keyboard navigation, reset, and speaker-notes are planned for M3 (see HANDOFF.md §8).

## Compliance

- No real customer, account, or transaction data — anywhere. Coverage, population, and
  precision numbers are synthetic and illustrative.
- The only real-world content is **public advisory material, paraphrased**: the FINTRAC
  Operational Alert on illicit synthetic opioids (Jan 2025) and FinCEN FIN-2019-A006 /
  FIN-2024-A002.
- The "Illustrative data & outputs" badge stays visible at all times — it is a trust
  device for a compliance audience, not a disclaimer to hide.

## Project docs

- `HANDOFF.md` — full context, constraints, content model, milestone plan, decision log.
- `CLAUDE.md` — always-loaded project memory / non-negotiables for the agent.

## Status

**M0 — bootstrap.** Baseline demo imported and runs from the repo. Next: M1, the
config-driven refactor (extract typology content to JSON, add the single-file build).
