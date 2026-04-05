"""Conditional independence test evaluator scaffold."""

from __future__ import annotations

from .base import BaseEvaluator


class CITestEvaluator(BaseEvaluator):
    """Evaluate CI-test outputs against d-separation ground truth."""

    metric_keys: tuple[str, ...] = ("power", "fpr", "f1_ci", "calibration_error")

    def evaluate(self, predicted: object, ground_truth: object) -> dict[str, float]:
        """Return CI test metrics.

        Raises:
            NotImplementedError: Until Phase 4 CI metric implementation lands.
        """
        _ = (predicted, ground_truth)
        raise NotImplementedError(
            "CITestEvaluator.evaluate is scheduled for Phase 4. "
            "Phase 1 defines only the stable public interface."
        )
