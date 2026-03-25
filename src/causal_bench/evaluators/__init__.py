"""Stub for the evaluators sub-package (Layer 3).

Evaluators will compute task-specific metrics (SHD, F1, Power, FDR, …)
from a predicted graph and a GroundTruth object.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from causal_bench.types import GroundTruth


class BaseEvaluator(ABC):
    """Abstract base for all metric evaluators.

    Note:
        This class is a **placeholder** stub. The full implementation will
        be delivered in the Layer 3 milestone.
    """

    @abstractmethod
    def evaluate(self, predicted: Any, ground_truth: GroundTruth) -> dict[str, float]:
        """Compute metrics comparing a predicted graph to the ground truth.

        Args:
            predicted: The predicted causal graph in whatever format the
                concrete evaluator expects.
            ground_truth: The true causal structure from the simulator.

        Returns:
            A dictionary mapping metric names to scalar float values.

        Raises:
            NotImplementedError: Until Layer 3 is implemented.
        """
        ...


__all__ = ["BaseEvaluator"]
