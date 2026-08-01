# Exo

Exo is a **pre-alpha 3D engine and renderer** written in the Spectre programming language. It uses SDL3 for GPU rendering, windows, input, and audio.

The project is usable as an experimental engine foundation. It is not yet a production-ready replacement for Godot, Unity, Unreal, or established lower-level frameworks.

## Current capabilities

- SDL3 GPU render backend
- Scene, reflection, water, glow, and post-processing passes
- Point lighting and material color, reflectivity, and emissive controls
- Procedural cubes and spheres
- A sparse-component world with entity IDs, transforms, velocity, and renderables
- Bounded sub-stepped gravity and floor collision
- Keyboard and relative-mouse camera controls
- WAV playback through SDL3
- Constrained GLB 2.0 loading with embedded PNG textures
- CPU-side model bounds
- Multi-scene applications
- Application builder and checked public facade

## Important limits

- The component world is intentionally small and uses linear sparse stores.
- Physics currently covers gravity and floor contacts, not general rigid-body simulation.
- GLB support is limited to the subset in [`docs/GLB_SUPPORT.md`](docs/GLB_SUPPORT.md).
- The primary build target is currently Linux x86-64.
- Shader and native object files are generated during the build and are not committed.

## Requirements

- Python 3.10+
- Spectre compiler
- SDL3 development libraries
- A C99 compiler
- `glslangValidator` or `glslc`

## Build

```bash
./scripts/build.sh dev
./scripts/build.sh test
./scripts/build.sh hello
./scripts/build.sh snow
```

PowerShell:

```powershell
./scripts/build.ps1 -Target dev
```

See [`docs/BUILDING.md`](docs/BUILDING.md) for complete setup and troubleshooting.

## Minimal example

```spectre
val ecs    = use("../../src/ecs.sx")
val engine = use("../../src/engine.sx")
val exo    = use("../../src/exo.sx")
val world  = use("../../src/world.sx")

pub fn main() i32 = {
    val state: mut world.World = world.new_world()
    val entity = world.create_entity(state)

    world.set_transform(state, entity, world.make_transform(
        ecs.make_vec3(0.0 as f32, 0.0 as f32, -2.5 as f32),
        1.0 as f32
    ))
    world.set_renderable(state, entity, world.cube_renderable(
        ecs.default_cube_material(ecs.make_vec3(0.25 as f32, 0.72 as f32, 1.0 as f32)),
        1.0 as f32
    ))

    val scenes: mut list[ecs.Scene3D] = []
    @append(scenes, world.to_scene(state))

    val builder: mut engine.ExoAppBuilder = exo.new_app()
    engine.with_title(builder, "Hello Exo")
    engine.with_scene_list(builder, scenes)
    engine.with_default_camera(builder)

    return trust exo.run(exo.build_app(builder))
}
```

The complete example is under [`examples/hello_world/`](examples/hello_world/).

## Default controls

| Action | Input |
|---|---|
| Move | W, A, S, D |
| Turn/look | Mouse or arrow keys |
| Cycle scene | X |
| Play configured WAV | Y |
| Quit | Escape |

All configurable scancodes are validated before keyboard-state access.

## Repository map

```text
src/exo.sx                 public facade
src/app_validation.sx      checked construction
src/world.sx               sparse component world
src/ecs.sx                 renderer-facing scene types
src/physics.sx             bounded gravity/floor physics
src/asset_ownership.sx     CPU asset destruction
src/engine.sx              legacy SDL3/GPU runtime
assets/shaders/            GLSL shader sources
examples/                  maintained application examples
scripts/                   build and validation tooling
docs/                      architecture and format documentation
```

Read [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) before making structural changes.

## Development status

Exo uses semantic versions beginning at `v0.1.0`. Until a stable release, APIs and internal formats may change. Changes that affect existing examples should include migration notes and tests.

## License

GPL-3.0-only. See [`LICENSE`](LICENSE).
