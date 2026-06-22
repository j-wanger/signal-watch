#!/usr/bin/env bash
# Vendor aml-casework's RUNTIME into vendor/aml-casework/ so the LIVE investigator workbench's DECIDE
# signed-SAR finale ships from a bare signal-watch clone — no sibling repo required. (Phase 67.)
#
# This is a DISTRIBUTION copy, NOT import-coupling: the companion (serve_workbench.py / serve_chain.py)
# still invokes the vendored casework over the EXISTING subprocess + file-handoff; build.py never imports
# it; the 5 offline ship artifacts are unaffected. aml-casework is local-only (no remote) and mid-feature,
# which is why we vendor a copy rather than use a git submodule.
#
# Re-run any time to REFRESH the vendored copy from the live sibling (records the pin in VENDORED_AT).
# Usage: scripts/vendor_casework.sh [path-to-aml-casework]   (default: ../aml-casework)
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC="${1:-$ROOT/../aml-casework}"
DST="$ROOT/vendor/aml-casework"

[ -d "$SRC/src/aml_casework" ] || { echo "ERROR: aml-casework not found at $SRC (pass its path as arg 1)" >&2; exit 1; }

EXCL=(--exclude '__pycache__' --exclude '*.pyc' --exclude '.venv' --exclude '.pytest_cache'
      --exclude '.mypy_cache' --exclude '.ruff_cache' --exclude '.coverage')

mkdir -p "$DST/src/aml_casework"
# The runtime: the package source + the dependency manifests + the README. NOT tests/.venv/.dev-wiki.
rsync -a --delete "${EXCL[@]}" "$SRC/src/aml_casework/" "$DST/src/aml_casework/"
cp "$SRC/pyproject.toml" "$SRC/uv.lock" "$SRC/README.md" "$DST/"
# casework's corpus_grounding verifier grounds each SAR alert against a PINNED signal-watch corpus
# snapshot that casework vendors under fixtures/corpus/ (its default root). Vendor it too, else EVERY SAR
# fails closed on a corpus_grounding violation and the DECIDE finale can never sign offline.
rsync -a --delete "${EXCL[@]}" "$SRC/fixtures/corpus/" "$DST/fixtures/corpus/"

# Honest pin for the drift we accepted (vendoring a snapshot of a sibling under active development).
COMMIT="$(git -C "$SRC" rev-parse --short HEAD 2>/dev/null || echo unknown)"
BRANCH="$(git -C "$SRC" rev-parse --abbrev-ref HEAD 2>/dev/null || echo unknown)"
DIRTY="$(git -C "$SRC" status --porcelain 2>/dev/null | wc -l | tr -d ' ')"
DATE="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
cat > "$DST/VENDORED_AT" <<EOF
aml-casework vendored into signal-watch — Phase 67 (make the live workbench shippable from a bare clone).

commit:      $COMMIT
branch:      $BRANCH
uncommitted-in-sibling-at-vendor-time: $DIRTY file(s)
vendored-at: $DATE
source:      $SRC  (a sibling repo; local-only / no git remote at vendor time — hence a vendored copy,
                    not a git submodule)

refresh:     scripts/vendor_casework.sh   (re-syncs the runtime copy from the live sibling + rewrites this pin)
boundary:    DISTRIBUTION copy only. The companion subprocesses this over the file-handoff; build.py NEVER
             imports it; the 5 offline ship artifacts (dist/*) are byte-unaffected.
build:       make setup   (builds vendor/aml-casework/.venv from pyproject + uv.lock; needs network once)
EOF

# Build the cross-platform wheel (Phase 67 — Windows/pip-friendly install; py3-none-any, pure Python) so it
# ships committed. `uv build` drops a dist/.gitignore (`*`) that would un-track it — remove it so the wheel
# commits (setup_workbench.py installs from vendor/aml-casework/dist/*.whl).
if command -v uv >/dev/null 2>&1; then
  ( cd "$DST" && uv build --wheel >/dev/null 2>&1 ) && rm -f "$DST/dist/.gitignore" \
    && echo "built wheel: $(cd "$DST" && ls dist/*.whl 2>/dev/null | tail -1)" \
    || echo "WARN: wheel build skipped/failed (uv build) — setup_workbench.py will fall back to a source install"
else
  echo "NOTE: uv not found — skipped the wheel build; setup_workbench.py installs from source"
fi

echo "vendored aml-casework@$COMMIT ($BRANCH, $DIRTY uncommitted) → $DST"
echo "next: python scripts/setup_workbench.py   (then: python scripts/serve_workbench.py)"
