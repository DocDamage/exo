#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET="${1:-dev}"
CC_BIN="${CC:-cc}"

cd "$ROOT"
mkdir -p build/native build/bin

python3 scripts/check_repo.py
"$CC_BIN" -std=c99 -O2 -Isrc -c src/stb_image_shim.c -o build/native/stb_image_shim.o
python3 scripts/compile_shaders.py --clean
spectre build "$TARGET"

printf 'Exo target %s built successfully\n' "$TARGET"
