---
applyTo: "**/*.py"
description: "ALWAYS read these when reading or modifying Python files. Covers Ruff linting and Pyright type-checking expectations, scope, and the pre-commit workflow."
---

# Python Files

This repo uses [`ruff`](https://docs.astral.sh/ruff/) for linting and [`pyright`](https://microsoft.github.io/pyright/) for type checking. Config: [`ruff.toml`](../../ruff.toml), [`pyrightconfig.json`](../../pyrightconfig.json).

## Before committing

After editing any `.py` file, run the repository checks:

```bash
pre-commit run --all-files
```

## Expectations

- **Don't introduce new violations.** If either hook reports new errors against files you modified, fix them before committing.
- **Pre-existing violations** in files you didn't touch are out of scope — leave them for whoever next edits that file.
- **Baseline suppressions** in `ruff.toml` and `pyrightconfig.json` represent existing repository debt. Remove them only with the corresponding cleanup.
- **Auto-fixes** (`ruff check --fix`) are safe to apply on files you're already editing when Ruff is installed directly. Review the diff before committing.
- **`# noqa` and `# type: ignore` comments** require a justification comment on the same line (e.g. `# noqa: F401 — re-exported`) and should be used extremely sparingly.

## Tests

- Prefer `pytest` for new Python tests.
- Keep area-specific tests in a `tests/` directory rather than beside executable helper scripts.
- Keep test-only dependencies in `tests/requirements.txt`; include the area's runtime requirements from there when tests import runtime modules. Do not add pytest to runtime requirements solely for tests.
- Run tests explicitly with `python -m pytest <tests-dir>` so the selected interpreter and environment are unambiguous.
- Ruff ignores `S101` in pytest test modules (`test_*.py` and `*_test.py`). Use plain `assert` statements, with a descriptive message, for test expectations. Reserve `pytest.fail(...)` for setup or fixture failures, and use `pytest.raises(...)` for expected exceptions.
- Direct-execution helper directories are not necessarily Python packages. When tests need to import sibling scripts, use a narrow `tests/conftest.py` path setup rather than creating a package API solely for tests.
- If the Pyright CLI is not using the workspace virtual environment, pass it explicitly (for example, `pyright --pythonpath .venv/bin/python <path>`). Do not suppress missing imports that are installed in the configured environment.

## Scope

Both tools scan repository-owned Python source. Generated, vendored, and
imported paths (`base/build`, `base/comps/kernel`, `base/out`, `specs`,
`**/__pycache__`, `**/.venv`, `**/venv`, `**/node_modules`) are excluded.
