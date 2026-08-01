# Changelog

## Unreleased - v0.1.0

### Added

- Public `exo.sx` facade and checked application construction
- Sparse-component world with entity IDs
- Explicit material reflectivity and emissive values
- Explicit model transforms
- Explicit CPU-side GLB destruction
- Bounded sub-stepped physics and resting-contact handling
- Reproducible shader and native-shim build scripts
- Separate development, release, test, hello, and snow targets
- Repository validation and CI workflows
- Architecture, build, and GLB support documentation

### Fixed

- Unsafe direct keyboard-state reads for configurable keys
- Uninitialized native runtime, mesh, and audio allocations
- Missing command-buffer abort behavior on frame failures
- GLB chunk, accessor, index, texture, and file-read validation
- GLB mesh-name replacement leak
- GLB textures leaking onto procedural primitives
- Loaded models missing from reflection rendering
- Rendered floor height disagreeing with collision height
- Water clipping when the surface is offset from the origin
- GPU texture uploads ignoring copy-pass and submission failures
- Unbounded audio gain values

### Changed

- Post-processing shaders are named for their actual tone-mapping and bloom behavior rather than FXAA
- Generated `.o` and `.spv` files are no longer source-controlled artifacts
- Legacy alternate entry files moved into maintained examples
- README capability claims now reflect the implemented scope
