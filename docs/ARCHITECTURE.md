# Exo Architecture

Exo is a pre-alpha 3D engine built in Spectre on top of SDL3's GPU, input, windowing, and audio APIs.

## Design goals

- Keep the public application API small and predictable.
- Keep unsafe native interop behind explicit boundaries.
- Make CPU and GPU resource ownership visible.
- Preserve a lightweight scene API while growing a real component world.
- Rebuild every generated artifact from source.

## Layers

### Public facade

`src/exo.sx` is the preferred application entry point. It exposes application construction and execution without requiring callers to depend directly on every renderer implementation detail.

`src/app_validation.sx` provides strict and safe-default construction paths.

### World and scene

`src/world.sx` provides entity identifiers and sparse stores for transforms, velocity, and renderable components. It converts a world snapshot into the current renderer-facing `Scene3D` representation.

`src/ecs.sx` retains the renderer-facing scene model and compatibility constructors such as `make_cube` and `make_sphere`. These functions are prefab-style helpers, not the component storage implementation.

### Runtime and rendering

`src/engine.sx` currently contains the legacy SDL3 runtime, GPU bindings, render passes, GLB upload logic, input loop, and audio runtime. The public facade isolates users from this file while it is progressively decomposed.

The render sequence is:

1. Acquire a GPU command buffer and swapchain texture.
2. Recreate size-dependent render targets when necessary.
3. Render a mirrored reflection scene.
4. Render the main scene into an off-screen target.
5. Apply tone mapping, compact bloom, and gamma correction.
6. Submit the command buffer.

Frame failures call an explicit abort path that ends active passes and cancels unsubmitted command buffers.

### Physics

`src/physics.sx` implements bounded sub-stepped gravity integration and floor contacts. It is intentionally small. It is not a general rigid-body solver.

### Assets

`src/asset_ownership.sx` defines CPU-side GLB destruction. GPU meshes and textures are owned by the runtime and destroyed during scene changes or shutdown.

The current GLB loader supports a constrained subset documented in `GLB_SUPPORT.md`. All offsets and byte ranges must be validated before raw memory access.

### Native shim

`src/stb_image_shim.c` contains the `stb_image` implementation. Its object file is compiled into `build/native/`; precompiled objects are not source artifacts.

### Shaders

GLSL lives in `assets/shaders/`. `scripts/compile_shaders.py` compiles each shader to SPIR-V during the build. Generated `.spv` files are ignored.

## Compatibility strategy

The existing `engine.sx`, `rendering.sx`, `ecs.sx`, and builder functions remain available while implementation ownership moves behind the facade. New game code should prefer `exo.sx` and `world.sx`.

## Next decomposition boundaries

The remaining large legacy runtime should be split without changing the public API:

- SDL3 ABI declarations and native helpers
- GPU device and resource lifecycle
- render-pass orchestration
- input and camera
- audio mixer
- GLB parsing and upload
- math primitives

Each extraction should land with behavior tests before the old implementation is removed.
