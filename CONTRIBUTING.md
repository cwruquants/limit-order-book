# Contributing

## Environment

Use [uv](https://docs.astral.sh/uv/). It reads `.python-version` and installs the right Python
for you:

```bash
uv sync --extra dev
uv run pytest
uv run ruff check .
uv run ruff format .
```

## Branch naming

`<track>/<short-desc>`, where track is `engine`, `markets`, or `infra`.
Examples: `engine/matching-loop`, `markets/ioc-semantics`, `infra/benchmark-suite`.

## Workflow

1. **Issue**: every change starts from an issue (use the *Task* template).
2. **Branch**: create a branch from `main` using the naming scheme above.
3. **PR**: open a pull request that links the issue (`Closes #N`) and fills in the template.
4. **Review**: 1 approval + green CI is required.
5. **Merge**: squash merge only.

No direct pushes to `main`.

## Interface rule

The signatures in `src/lob/order.py` and `src/lob/book.py` are a contract shared by every
track. Do not change them in a PR without prior agreement: open an issue describing the
proposed change and get tech-lead approval first.

## AI-use policy

- AI assistants are allowed for implementation.
- Humans write the specs and acceptance criteria.
- Every author must be able to explain their PR, line by line, at the weekly check-in.
- Tests are required for every behavior change.
- Matching logic must be covered by [hypothesis](https://hypothesis.readthedocs.io/) property
  tests (e.g. the invariants in `docs/design.md`), not just example-based tests.

## Code style

- Formatting and linting with ruff (`ruff format .`, `ruff check .`); CI enforces both.
- Type hints everywhere, using modern syntax (`X | None`, `list[int]`).
- Docstrings on all public classes and methods.
- Prices are integer ticks. Never use floats for prices.
