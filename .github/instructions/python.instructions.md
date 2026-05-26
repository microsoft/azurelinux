---
applyTo: "**/*.py"
description: "ALWAYS read these when reading or modifying Python files. Covers ruff lint/format and pyright type-checking expectations, scope, and the pre-commit workflow."
---

# Python Files

This repo uses [`ruff`](https://docs.astral.sh/ruff/) for linting/formatting and [`pyright`](https://microsoft.github.io/pyright/) for type checking. Config: [`ruff.toml`](../../ruff.toml), [`pyrightconfig.json`](../../pyrightconfig.json).

## Before committing

After editing any `.py` file, run both checks on the files you touched:

```bash
ruff check <file>            # add --fix to auto-apply safe fixes
ruff format <file>            # formatting
pyright <file>                # type checking
```

Or check everything at once:

```bash
ruff check
pyright
```

## Expectations

- **Don't introduce new violations.** If `ruff check` or `pyright` reports new errors against files you modified, fix them before committing.
- **Pre-existing violations** in files you didn't touch are out of scope — leave them for whoever next edits that file.
- **Auto-fixes** (`ruff check --fix`) are safe to apply on files you're already editing. Review the diff before committing.
- **`# noqa` and `# type: ignore` comments** require a justification comment on the same line (e.g. `# noqa: F401 — re-exported`) and should be used extremely sparingly.

## Scope

Both tools currently scan: `.github/`, `base/`, `scripts/`. Generated/vendored paths (`base/build`, `base/out`, `specs`, `**/__pycache__`, `**/.venv`, `**/venv`, `**/node_modules`) are excluded.
