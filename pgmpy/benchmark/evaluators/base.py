"""Evaluator interfaces for benchmark metric computation."""

from __future__ import annotations

from abc import ABC, abstractmethod

from ..simulators.base import GroundTruth


class BaseEvaluator(ABC):
    """Abstract evaluator for method predictions against ground truth."""

    metric_keys: tuple[str, ...] = ()

    @abstractmethod
    def evaluate(
        self, predicted: object, ground_truth: GroundTruth
    ) -> dict[str, float]:
        """Return metric dictionary with stable keys for all evaluations."""
