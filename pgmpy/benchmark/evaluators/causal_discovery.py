from .base import BaseEvaluator


class CausalDiscoveryEvaluator(BaseEvaluator):
    """Evaluate discovered graph structure against ground truth DAG."""

    metric_keys: tuple[str, ...] = (
        "shd",
        "f1_directed",
        "precision",
        "recall",
        "fdr",
        "f1_skeleton",
    )

    def evaluate(self, predicted: object, ground_truth: object) -> dict[str, float]:
        """Return causal discovery metrics.

        Raises:
            NotImplementedError: Until Phase 4 metric implementation is complete.
        """
        _ = (predicted, ground_truth)
        raise NotImplementedError(
            "CausalDiscoveryEvaluator.evaluate is scheduled for Phase 4. "
            "Phase 1 defines only the stable public interface."
        )
