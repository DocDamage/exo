#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHADER_ROOT = ROOT / "assets" / "shaders"


def compiler_command(source: Path, output: Path) -> list[str]:
    glslang = shutil.which("glslangValidator")
    if glslang:
        return [glslang, "-V", str(source), "-o", str(output)]
    glslc = shutil.which("glslc")
    if glslc:
        return [glslc, str(source), "-o", str(output)]
    raise RuntimeError("Install glslangValidator or glslc to compile Exo shaders")


def shader_sources() -> list[Path]:
    return sorted(
        path
        for path in SHADER_ROOT.iterdir()
        if path.is_file() and path.suffix in {".vert", ".frag"}
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Compile Exo GLSL shaders to SPIR-V")
    parser.add_argument("--clean", action="store_true", help="remove generated SPIR-V files first")
    parser.add_argument("--check", action="store_true", help="validate sources without keeping output")
    args = parser.parse_args()

    sources = shader_sources()
    if not sources:
        raise RuntimeError(f"No shader sources found under {SHADER_ROOT}")

    if args.clean:
        for generated in SHADER_ROOT.glob("*.spv"):
            generated.unlink()

    generated: list[Path] = []
    try:
        for source in sources:
            output = source.with_name(source.name + ".spv")
            command = compiler_command(source, output)
            print("+", " ".join(command))
            subprocess.run(command, check=True)
            generated.append(output)
    except subprocess.CalledProcessError as exc:
        print(f"shader compilation failed with exit code {exc.returncode}", file=sys.stderr)
        return exc.returncode
    finally:
        if args.check:
            for output in generated:
                output.unlink(missing_ok=True)

    print(f"compiled {len(generated)} shaders")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
