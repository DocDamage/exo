# Building Exo

## Supported development environment

The primary validated target is Linux x86-64. Spectre also has macOS and Windows implementations, but Exo's native and shader packaging still requires platform validation on those systems.

## Requirements

- Python 3.10 or newer
- Spectre compiler on `PATH`
- SDL3 development libraries
- A C99 compiler (`clang`, `cc`, or equivalent)
- `glslangValidator` or `glslc`
- Git

## Build targets

```bash
./scripts/build.sh dev
./scripts/build.sh release
./scripts/build.sh test
./scripts/build.sh hello
./scripts/build.sh snow
```

Equivalent Make targets are available:

```bash
make dev
make test
make hello
```

On PowerShell:

```powershell
./scripts/build.ps1 -Target dev
./scripts/build.ps1 -Target test
```

## What the build does

1. Runs `scripts/check_repo.py`.
2. Compiles `src/stb_image_shim.c` into `build/native/stb_image_shim.o`.
3. Compiles GLSL files under `assets/shaders/` into SPIR-V.
4. Runs the selected `spectre build` target from `sx.mod`.

Generated files are placed under `build/` or beside shader sources as ignored `.spv` files. They must not be committed.

## Runtime assets

Run built examples from the repository root unless an explicit asset root is added later. Current default shader and sample-asset paths are repository-relative.

## Troubleshooting

### SDL3 cannot be linked

Confirm SDL3 is discoverable by the system linker. The current Linux configuration expects SDL3 in the normal linker path or `/usr/local/lib`.

### Shader compiler missing

Install either `glslangValidator` or `glslc`. The shader script reports which executable it attempted to use.

### Native object missing

Do not restore `src/stb_image_shim.o`. Run the build script so the object is recreated for the current platform.

### Spectre build target not found

Run `spectre build dev`, `release`, `test`, `hello`, or `snow`. The project uses per-target entries in `sx.mod`.
