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

## Tests

- Prefer `pytest` for new Python tests.
- Keep area-specific tests in a `tests/` directory rather than beside executable helper scripts.
- Keep test-only dependencies in `tests/requirements.txt`; include the area's runtime requirements from there when tests import runtime modules. Do not add pytest to runtime requirements solely for tests.
- Run tests explicitly with `python -m pytest <tests-dir>` so the selected interpreter and environment are unambiguous.
- Ruff currently enforces `S101` in tests. Use `pytest.fail(...)` for explicit value checks and `pytest.raises(...)` for exceptions rather than bare `assert` statements.
- Direct-execution helper directories are not necessarily Python packages. When tests need to import sibling scripts, use a narrow `tests/conftest.py` path setup rather than creating a package API solely for tests.
- If the Pyright CLI is not using the workspace virtual environment, pass it explicitly (for example, `pyright --pythonpath .venv/bin/python <path>`). Do not suppress missing imports that are installed in the configured environment.

## Scope

Both tools currently scan: `.github/`, `base/`, `scripts/`. Generated/vendored paths (`base/build`, `base/out`, `specs`, `**/__pycache__`, `**/.venv`, `**/venv`, `**/node_modules`) are excluded.
