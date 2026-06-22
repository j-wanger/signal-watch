#!/usr/bin/env python3
"""Cross-platform setup for the LIVE investigator workbench (Phase 67 — Windows/macOS/Linux).

Builds the casework venv (`vendor/aml-casework/.venv`) and installs the vendored aml-casework into it, so
the DECIDE signed-SAR finale runs. Uses NO `make`, NO Unix shell — just Python — so it works on Windows
(`python scripts\\setup_workbench.py`) exactly as on POSIX (`python3 scripts/setup_workbench.py`).

Prefers `uv` (the project's tool, cross-platform) and installs the committed WHEEL
(`vendor/aml-casework/dist/aml_casework-*.whl`) for portability; falls back to the stdlib `venv` + `pip`,
and to a source install if no wheel is present. Needs network once (to fetch casework's deps). The FIVE
OFFLINE ship artifacts need NONE of this — open `dist/index.html` in a browser.
"""
from __future__ import annotations

import glob
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VENDOR = ROOT / "vendor" / "aml-casework"
VENV = VENDOR / ".venv"


def venv_python(venv: Path) -> Path:
    """The venv interpreter, cross-platform (Windows: Scripts\\python.exe; POSIX: bin/python)."""
    if os.name == "nt":
        return venv / "Scripts" / "python.exe"
    return venv / "bin" / "python"


def run(cmd: list[str]) -> None:
    print("  $", " ".join(cmd))
    subprocess.run(cmd, check=True)


def main() -> int:
    if not (VENDOR / "src" / "aml_casework").is_dir():
        sys.exit(f"vendor/aml-casework is missing at {VENDOR} — re-vendor it "
                 f"(maintainer: scripts/vendor_casework.sh) or fetch a complete clone.")

    wheels = sorted(glob.glob(str(VENDOR / "dist" / "aml_casework-*.whl")))
    target = wheels[-1] if wheels else str(VENDOR)            # the committed wheel (portable) else source
    using = f"wheel {Path(target).name}" if wheels else "source (no wheel found)"
    have_uv = shutil.which("uv") is not None
    print(f"Setting up the live workbench: installing aml-casework from {using} into {VENV} "
          f"(via {'uv' if have_uv else 'venv+pip'}).")

    if have_uv:
        run(["uv", "venv", "--clear", str(VENV)])             # --clear: idempotent re-setup
        run(["uv", "pip", "install", "--python", str(venv_python(VENV)), target])
    else:
        run([sys.executable, "-m", "venv", "--clear", str(VENV)])
        run([str(venv_python(VENV)), "-m", "pip", "install", target])

    print("\nlive workbench ready:")
    print(f"  {Path(sys.executable).name} scripts/serve_workbench.py   ->  http://localhost:8030")
    print("  DECIDE runs OFFLINE on the deterministic stub. For the neural SAR prose / GATHER, set")
    print("  OPENAI_BASE_URL (a local model) or an Anthropic key SERVER-SIDE before launching — the")
    print("  browser never sees it. Refresh the vendored copy (maintainer): scripts/vendor_casework.sh")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
