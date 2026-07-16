"""Packaging sanity gate: every ``.py`` file in the source tree must compile.

This is the cross-cutting acceptance gate referenced by Requirement 13.1 of
the ``dfm-analyzer-cr-analyzer-fixes`` spec. The repository has no dedicated
CI gate script (no ``Makefile``, ``tox.ini``, ``noxfile.py``, ``pyproject.toml``,
or ``.github/workflows/`` entries), so this test takes the role of the gate:
it walks the source tree and runs :mod:`py_compile` against every Python
module, mirroring ``python -m py_compile $(git ls-files '*.py')``.

If any tracked Python file fails to byte-compile, BEARS and any
``py_compile``-driven gate will fail; this test fails the build first so the
regression is caught locally before it reaches the CR analyzers.
"""

from __future__ import annotations

import os
import py_compile
from pathlib import Path

import pytest

# Walk relative to the repo root (one level above the ``tests/`` directory).
REPO_ROOT = Path(__file__).resolve().parent.parent

# Generated, cached, vendored, or virtual-env directories that should never be
# byte-compiled as part of the package source tree.
SKIP_DIRS = frozenset(
    {
        "__pycache__",
        ".venv",
        "venv",
        "env",
        ".env",
        ".git",
        ".kiro",
        ".hypothesis",
        ".pytest_cache",
        ".mypy_cache",
        ".ruff_cache",
        ".tox",
        ".nox",
        "build",
        "dist",
        "node_modules",
        "site-packages",
        ".idea",
        ".vscode",
        "extracted_specs",
        "extracted_specs_new",
    }
)


def _iter_py_files(root: Path):
    """Yield every ``.py`` file under *root*, pruning :data:`SKIP_DIRS`."""

    for dirpath, dirnames, filenames in os.walk(root):
        # Mutate ``dirnames`` in-place so :func:`os.walk` does not descend
        # into pruned directories.
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            if name.endswith(".py"):
                yield Path(dirpath) / name


def test_all_python_modules_byte_compile() -> None:
    """Every ``.py`` file under the repo must byte-compile cleanly.

    Validates Requirement 13.1.
    """

    failures: list[tuple[Path, str]] = []
    compiled = 0
    for py_file in _iter_py_files(REPO_ROOT):
        compiled += 1
        try:
            py_compile.compile(str(py_file), doraise=True)
        except py_compile.PyCompileError as exc:  # pragma: no cover - failure path
            failures.append((py_file, str(exc)))

    assert compiled > 0, "no Python files were discovered under the repo root"

    if failures:
        rendered = "\n".join(
            f"  {path.relative_to(REPO_ROOT)}: {err}" for path, err in failures
        )
        pytest.fail(
            f"py_compile failed for {len(failures)} of {compiled} file(s):\n"
            f"{rendered}"
        )
