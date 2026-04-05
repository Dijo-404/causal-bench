"""Pytest bootstrap for local ``pgmpy.benchmark`` namespace wiring."""

from __future__ import annotations

import sys
import types
from pathlib import Path


def pytest_configure() -> None:
    """Expose local benchmark package as ``pgmpy.benchmark`` for tests."""
    repo_root = Path(__file__).resolve().parents[2]
    local_pgmpy_root = repo_root / "pgmpy"

    if str(local_pgmpy_root) not in sys.path:
        sys.path.insert(0, str(local_pgmpy_root))

    import benchmark as local_benchmark

    try:
        import pgmpy as upstream_pgmpy
    except ModuleNotFoundError:
        upstream_pgmpy = types.ModuleType("pgmpy")
        sys.modules["pgmpy"] = upstream_pgmpy

    sys.modules["pgmpy.benchmark"] = local_benchmark
    setattr(upstream_pgmpy, "benchmark", local_benchmark)
