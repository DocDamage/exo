# Contributing to Exo

## Before opening a pull request

1. Run `python3 scripts/check_repo.py`.
2. Run `./scripts/build.sh test`.
3. Build any affected example target.
4. Do not commit `.o`, `.spv`, generated executables, or cache files.
5. Update documentation when public behavior changes.

## Engineering rules

- Keep unsafe native interop contained and explicitly marked with `trust`.
- Initialize every native resource structure before partial-failure cleanup can inspect it.
- Validate byte ranges before pointer arithmetic.
- Make ownership and destruction responsibilities explicit.
- Keep public compatibility wrappers when moving implementation code.
- Add a test or deterministic validation for every bug fix.
- Prefer focused files below roughly 300 lines. Large ABI or transitional legacy files require a documented reason.

## Commit style

Use concise subsystem prefixes, for example:

```text
render: fix reflection model pass
assets: validate GLB buffer views
build: compile native shim per target
```

## Pull requests

Describe:

- The problem being solved
- The architectural boundary affected
- Validation performed
- Known limitations
- Follow-up work that was intentionally excluded

Large refactors should preserve the existing facade first, then remove obsolete internals in a later change after compatibility tests pass.
