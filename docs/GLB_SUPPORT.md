# GLB Support

Exo currently supports a deliberately constrained GLB 2.0 subset.

## Supported

- Binary GLB 2.0 container
- One JSON chunk followed by one BIN chunk
- First mesh
- First primitive
- `POSITION` as tightly packed float32 `VEC3`
- Optional `NORMAL` as tightly packed float32 `VEC3`
- Optional `TEXCOORD_0` as tightly packed float32 `VEC2`
- Unindexed primitives
- Unsigned 16-bit or unsigned 32-bit indices
- One image embedded through a buffer view
- PNG decoding through `stb_image`
- CPU-side bounds calculation

## Not yet supported

- Multiple nodes, meshes, or primitives
- Node hierarchy and node transforms
- Multiple materials or textures
- External buffers or images
- Data URIs
- Accessor `byteStride`
- Sparse accessors
- Quantized or normalized vertex formats
- Unsigned 8-bit indices
- Morph targets
- Skinning and animation
- Cameras and lights from the GLB
- KTX, WebP, or JPEG decoding in the current image shim

## Safety rules

The loader rejects files when:

- The GLB magic or version is invalid.
- Declared total length exceeds the supplied buffer.
- JSON or BIN chunks exceed the declared container.
- Accessor counts, offsets, or element ranges exceed the BIN chunk.
- Embedded image ranges exceed the BIN chunk.
- A file read is incomplete.

Parsed models own their copied byte buffer and mesh-name allocation. Call `engine.destroy_glb_model` directly or use `asset_ownership.release_scene_model(s)` after the engine is finished with them.

## Roadmap

The next asset milestones are:

1. Dedicated parser data structures instead of reparsing JSON during upload.
2. Buffer-view stride and component-type validation.
3. Multiple primitives and materials.
4. Node transforms and scene hierarchy.
5. Asset handles and centralized reference-counted ownership.
6. Fuzz testing with malformed and truncated GLB inputs.
