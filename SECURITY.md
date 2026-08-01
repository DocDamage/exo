# Security Policy

Exo is pre-alpha software and should not process untrusted assets in a privileged environment.

## Reporting a vulnerability

Report security issues privately to the repository owner rather than opening a public issue. Include:

- Affected commit
- Platform and compiler versions
- Reproduction steps
- The smallest asset or input that triggers the issue
- Expected impact

## High-risk surfaces

The following code requires additional review:

- SDL3 FFI declarations and ABI structure mirrors
- Raw pointer arithmetic
- GPU upload and command-buffer lifecycle
- GLB parsing
- Image decoding
- Audio buffers
- File and shader loading

## Security expectations

- Malformed GLB files must fail without out-of-bounds reads.
- Every allocated CPU or GPU resource must have a defined cleanup path.
- Configuration-derived scancodes must be range checked.
- Generated native objects must be rebuilt for the target platform.
- Third-party source and CI actions should be pinned for release builds.

No stable security-support window is promised before Exo reaches a stable release.
