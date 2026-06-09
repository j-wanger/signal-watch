# Active Phase Context

Phase: 39 — Live news QOL: streamed extraction progress + one-shot URL acquisition. DELIVERED 2026-06-09 — all 5 lite tasks T1–T5 [x]; exit criteria MET; awaiting the delivery gate (present report → accept → commit + push to main → flip gate post-commit). Direction was approved via the assumption gate 2026-06-09 (A1 reject→revised→accept-with-condition; revisit: A1 BIT — the verifier/standardizer condition proved load-bearing on the justice.gov Akamai interstitial; A2–A4 held). Lite ceremony.

Objective: make the LIVE news companion legible + one-shot. DELIVERED: (1) `/extract` is ALWAYS an NDJSON stage stream (received → [fetching → converting] → extracting → grounding → verifying i/N → done; HTTP/1.0 body-until-close per-line flush — NO chunked framing, polling fallback unused; `extract(on_progress=None)` kept the Phase-38 replay fixtures green WITHOUT re-capture); (2) NEW companion-only `scripts/news_fetch.py` — fetch ladder urllib→curl→markitdown + deterministic standardizer + article-shape VERIFIER (D5: a rung wins ONLY by passing the verifier; D6: cookie + one same-host meta-refresh beats the Akamai interstitial); `/extract` accepts {url} OR {text} (text wins, D8); news.html live-region URL input + progress UI.

Scope (UNFREEZE was): scripts/serve_news.py · scripts/news_fetch.py (NEW) · news.html (live region only) · dist/news/index.html (BYTE-IDENTICAL via the strip) · tests/news_live_test.py · tests/news-stream.test.mjs · tests/fixtures/news-fetch/** (NEW) · docs/news-live.md · tests/smoke-checklist.md · CLAUDE.md (in-place) · this file.

Key constraints (held): offline `dist/news` byte-identical (all client code inside /*LIVE_START*/…/*LIVE_END*/); build.py NEVER imports the live layer (news_fetch companion-only; markitdown lazy/.venv-only); replay fixtures green without re-capture; a fetch that can't pass the verifier is an HONEST failure → paste fallback (never loosen the verifier); the always-on badge stays; NO non-negotiable change.

Exit criteria: MET — news-stream 81→90 + corpus green; `--check all` 5/5 ZERO DRIFT; news_live_test PASS (system + .venv + --live real-Qwen smoke); news_fetch/news_ground/serve_news/news_store/derive_signals --selftest PASS; measured live 42.7s end-to-end, 16 entities + 8 flags grounded, 0 dropped (treasury.gov jy2735).

Abort rule: (closed) blocked >3 attempts → mark [blocked: …] + ask the user: skip or abort.

Gates:
- [x] Direction confirmed by user (assumption-approval gate 2026-06-09: A1 accept-with-condition, A2–A4 accept)
- [ ] Delivery accepted
