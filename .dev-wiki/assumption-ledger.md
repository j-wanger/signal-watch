# Assumption Ledger

Append-only. One block per phase direction gate (dev-plan Step 13). `revisit-status:` filled at debrief.

## Phase 39 — Live news QOL: streamed extraction progress + one-shot URL acquisition (2026-06-09)

all_accept: false (A1 rejected in round 1 → revised → accepted with condition)

- A1 [HIGH] URL flow shape. Round 1 (preview-then-run): REJECT — user wants one-shot. Round 2 (one-shot /extract {url}, converted text fills textarea as passive recovery): ACCEPT WITH CONDITION — acquisition must go through a multi-method fetch ladder (bot guards expected) + a scripted format STANDARDIZER + VERIFIER before extraction. revisit-status: bit (the accept-with-condition standardizer/verifier turned out LOAD-BEARING — justice.gov answered urllib with a 2.5KB Akamai interstitial converting to 0 chars; a fetch-error-only ladder failed; D5 verifier-advances-the-ladder + D6 interstitial two-step were the fix — the condition validated the design)
- A2 [HIGH] Progress = real stage-level chunked-NDJSON events over POST /extract (fetch+ReadableStream client); token streaming + client-only spinner rejected; job-id+polling is the verified-at-impl fallback if stdlib chunked flush misbehaves. ACCEPT. revisit-status: held (HTTP/1.0 body-until-close per-line write+flush streamed cleanly; the polling fallback was never needed)
- A3 [MED] Verify-latency cause (per-entity second pass, N sequential model calls) stays OUT of scope — feedback this phase, batching stays deferred. ACCEPT. revisit-status: held (latency untouched by design; progress made the 42.7s wait legible, not shorter; batching stays the deferred candidate)
- A4 [MED] Invariants carry forward: all client code in /*LIVE_START*/…/*LIVE_END*/ → offline dist/news byte-identical; markitdown .venv-only lazy import + graceful degrade; build.py never imports the live layer; extract()/call_llm fixture seam preserved (on_progress defaults no-op, no fixture re-capture). ACCEPT. revisit-status: held (replay fixtures green WITHOUT re-capture; dist/news byte-identical; --check all 5/5 zero drift)
