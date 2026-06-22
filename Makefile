# signal-watch — make targets for the LIVE companion workbench (Phase 67).
#
# The 5 OFFLINE ship artifacts need NONE of this: open dist/index.html in a browser (no server, no deps).
# These targets set up the VENDORED aml-casework (vendor/aml-casework/) so the live investigator
# workbench's DECIDE signed-SAR finale runs from a bare clone with NO sibling repo. Live tier only —
# requires Python >=3.11 + uv (the offline artifacts stay zero-dependency).

VENDOR := vendor/aml-casework

.PHONY: setup vendor-refresh check help

help: ## Show these targets
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | awk 'BEGIN{FS=":.*?## "}{printf "  %-16s %s\n", $$1, $$2}'

setup: ## Build the vendored aml-casework venv → enables the live-workbench DECIDE finale (needs network once)
	@test -d $(VENDOR)/src/aml_casework || { echo "vendor/aml-casework missing — run: scripts/vendor_casework.sh"; exit 1; }
	cd $(VENDOR) && uv sync
	@echo ""
	@echo "live workbench ready:  python3 scripts/serve_workbench.py  →  http://localhost:8030"
	@echo "  (DECIDE runs offline on the deterministic stub; for neural SAR/GATHER set OPENAI_BASE_URL"
	@echo "   or an Anthropic key SERVER-SIDE before launching — the browser never sees it.)"

vendor-refresh: ## Re-vendor aml-casework from the local sibling (refresh the copy + rewrite the pin)
	scripts/vendor_casework.sh

check: ## Drift guard — the 5 offline ship artifacts stay byte-identical (vendoring must not touch them)
	python3 scripts/build.py --check all
