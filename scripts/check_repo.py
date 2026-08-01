#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = (
    "LICENSE",
    "README.md",
    "sx.mod",
    "src/engine.sx",
    "src/exo.sx",
    "src/world.sx",
    "src/asset_ownership.sx",
    "src/app_validation.sx",
    "scripts/build.sh",
    "scripts/build.ps1",
    "scripts/compile_shaders.py",
    "docs/ARCHITECTURE.md",
    "docs/BUILDING.md",
    "docs/GLB_SUPPORT.md",
)


def tracked_files() -> list[str]:
    result = subprocess.run(
        ["git", "ls-files"], cwd=ROOT, check=True, capture_output=True, text=True
    )
    return [line for line in result.stdout.splitlines() if line]


def main() -> int:
    errors: list[str] = []
    for relative in REQUIRED:
        if not (ROOT / relative).is_file():
            errors.append(f"missing required file: {relative}")

    tracked = tracked_files()
    for relative in tracked:
        if relative.endswith((".o", ".spv", ".pyc")):
            errors.append(f"generated artifact is tracked: {relative}")

    engine_path = ROOT / "src" / "engine.sx"
    if engine_path.is_file():
        engine = engine_path.read_text(encoding="utf-8")
        required_markers = (
            "// EXO_HARDENING_V1",
            "fn exo_sdl3_abort_frame",
            "pub fn destroy_glb_model",
            "use_albedo_texture: bool",
            "scene_reflection_plane",
            "model_position",
            "postprocess.vert.spv",
        )
        for marker in required_markers:
            if marker not in engine:
                errors.append(f"engine hardening marker missing: {marker}")
        forbidden = (
            'link "./src/stb_image_shim.o"',
            "@load8(@ptradd(keys, app.input.quit_key",
            "@load8(@ptradd(keys, app.next_scene_key",
            "@load8(@ptradd(keys, app.audio.trigger_key",
            "val floor_y: f32 = -0.18 as f32",
        )
        for marker in forbidden:
            if marker in engine:
                errors.append(f"unsafe legacy engine pattern remains: {marker}")

    water = (ROOT / "assets" / "shaders" / "water.frag").read_text(encoding="utf-8")
    if "uWaterCenter" not in water or "vWorldPos.xz - uWaterCenter.xz" not in water:
        errors.append("water shader does not calculate its mask in local water space")

    if errors:
        print("repository validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"repository validation passed ({len(tracked)} tracked files)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
