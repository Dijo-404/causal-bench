"""Phase 1 tests for benchmark runner API scaffolding."""

from __future__ import annotations

import pytest

from pgmpy.benchmark.evaluators import CausalDiscoveryEvaluator
from pgmpy.benchmark.runner import BenchmarkRunner
from pgmpy.benchmark.simulators import RandomDAGSimulator


@pytest.mark.unit
def test_runner_validates_constructor_inputs() -> None:
    simulator = RandomDAGSimulator()
    evaluator = CausalDiscoveryEvaluator()

    with pytest.raises(ValueError, match="n_seeds"):
        BenchmarkRunner(
            simulators=[simulator],
            methods=[object()],
            evaluators=[evaluator],
            n_seeds=0,
        )

    with pytest.raises(ValueError, match="n_jobs"):
        BenchmarkRunner(
            simulators=[simulator],
            methods=[object()],
            evaluators=[evaluator],
            n_jobs=0,
        )

    with pytest.raises(ValueError, match="timeout_seconds"):
        BenchmarkRunner(
            simulators=[simulator],
            methods=[object()],
            evaluators=[evaluator],
            timeout_seconds=0,
        )


@pytest.mark.unit
def test_runner_is_phase_three_placeholder() -> None:
    runner = BenchmarkRunner(
        simulators=[RandomDAGSimulator()],
        methods=[object()],
        evaluators=[CausalDiscoveryEvaluator()],
    )

    with pytest.raises(NotImplementedError, match="Phase 3"):
        runner.run()
