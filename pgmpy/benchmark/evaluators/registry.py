"""Evaluator registry for benchmark extension points."""

from __future__ import annotations

from collections.abc import Callable

from .base import BaseEvaluator

EVALUATOR_REGISTRY: dict[str, type[BaseEvaluator]] = {}


def register_evaluator(
    name: str,
) -> Callable[[type[BaseEvaluator]], type[BaseEvaluator]]:
    """Register an evaluator class under a stable name."""

    def decorator(cls: type[BaseEvaluator]) -> type[BaseEvaluator]:
        if name in EVALUATOR_REGISTRY:
            raise ValueError(f"Evaluator '{name}' is already registered")
        EVALUATOR_REGISTRY[name] = cls
        return cls

    return decorator
