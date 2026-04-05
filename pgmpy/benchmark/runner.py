"""Benchmark execution runner scaffold."""

from __future__ import annotations

from .evaluators.base import BaseEvaluator
from .report import BenchmarkReport
from .simulators.base import BaseSimulator


class BenchmarkRunner:
    """Coordinate simulator, method, and evaluator execution across seeds."""

    def __init__(
        self,
        simulators: list[BaseSimulator],
        methods: list[object],
        evaluators: list[BaseEvaluator],
        n_seeds: int = 10,
        n_jobs: int = 1,
        timeout_seconds: int = 300,
    ) -> None:
        if n_seeds < 1:
            raise ValueError("n_seeds must be >= 1")
        if n_jobs < 1:
            raise ValueError("n_jobs must be >= 1")
        if timeout_seconds < 1:
            raise ValueError("timeout_seconds must be >= 1")

        self.simulators = simulators
        self.methods = methods
        self.evaluators = evaluators
        self.n_seeds = n_seeds
        self.n_jobs = n_jobs
        self.timeout_seconds = timeout_seconds

    def run(self) -> BenchmarkReport:
        """Execute all simulator-method-seed combinations.

        Raises:
            NotImplementedError: Until Phase 3 execution engine implementation.
        """
        raise NotImplementedError(
            "BenchmarkRunner.run is scheduled for Phase 3. "
            "Phase 1 defines only the stable public interface."
        )
