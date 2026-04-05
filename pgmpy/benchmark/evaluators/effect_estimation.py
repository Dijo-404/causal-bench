"""Causal effect estimation evaluator scaffold."""

from __future__ import annotations

from .base import BaseEvaluator


class EffectEstimationEvaluator(BaseEvaluator):
    """Evaluate estimated treatment effects against known ATE values."""

    metric_keys: tuple[str, ...] = (
        "ate_abs_error",
        "ate_rel_error",
        "ci_coverage",
        "bias",
        "variance",
    )

    def evaluate(self, predicted: object, ground_truth: object) -> dict[str, float]:
        """Return effect estimation metrics.

        Raises:
            NotImplementedError: Until Phase 5 effect evaluator implementation.
        """
        _ = (predicted, ground_truth)
        raise NotImplementedError(
            "EffectEstimationEvaluator.evaluate is scheduled for Phase 5. "
            "Phase 1 defines only the stable public interface."
        )
