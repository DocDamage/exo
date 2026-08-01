#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys

from tools.refactor import patch_assets, patch_gpu, patch_render, patch_runtime

ROOT = Path(__file__).resolve().parents[2]
ENGINE = ROOT / "src" / "engine.sx"
MARKER = "// EXO_HARDENING_V1"


def main() -> int:
    text = ENGINE.read_text(encoding="utf-8")
    if MARKER in text:
        print("engine hardening already applied")
        return 0
    for patch in (patch_gpu, patch_runtime, patch_assets, patch_render):
        text = patch.apply(text)
    ENGINE.write_text(text, encoding="utf-8")
    print("applied Exo engine hardening")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"engine hardening failed: {exc}", file=sys.stderr)
        raise
