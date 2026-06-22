# signal-watch — POSIX convenience targets for the LIVE companion workbench (Phase 67).
#
# ON WINDOWS (where `make` is not native), run the Python scripts DIRECTLY — same effect, cross-platform:
#   python scripts\setup_workbench.py      then      python scripts\serve_workbench.py
#
# These set up the VENDORED aml-casework (vendor/aml-casework/) so the live investigator workbench's DECIDE
# signed-SAR finale runs from a bare clone with NO sibling repo. Live tier only — needs Python >=3.11 + uv
# (or pip). The 5 OFFLINE ship artifacts need NONE of this: open dist/index.html in a browser.
#
# Recipes delegate to cross-platform Python scripts (no Unix-shell builtins), so `make` itself is the only
# POSIX dependency here. Override the interpreter if needed: `make setup PYTHON=python`.

PYTHON ?= python3

.PHONY: setup check vendor-refresh

setup:           ## Build the live-workbench venv (delegates to the cross-platform Python setup script)
	$(PYTHON) scripts/setup_workbench.py

check:           ## Drift guard — the 5 offline ship artifacts stay byte-identical (vendoring must not touch them)
	$(PYTHON) scripts/build.py --check all

vendor-refresh:  ## Re-vendor aml-casework from the local sibling (maintainer; bash/POSIX)
	bash scripts/vendor_casework.sh
