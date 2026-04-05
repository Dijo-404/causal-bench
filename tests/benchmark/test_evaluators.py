"""Phase 1 tests for evaluator contracts and registry scaffolding."""

from __future__ import annotations

import pandas as pd
import pytest

from pgmpy.benchmark.evaluators import (
    EVALUATOR_REGISTRY,
    CausalDiscoveryEvaluator,
    CITestEvaluator,
    EffectEstimationEvaluator,
    register_evaluator,
)
from pgmpy.benchmark.evaluators.base import BaseEvaluator
from pgmpy.benchmark.simulators import GroundTruth


@pytest.mark.unit
def test_evaluator_metric_keys_are_stable() -> None:
    assert CausalDiscoveryEvaluator.metric_keys == (
        "shd",
        "f1_directed",
        "precision",
        "recall",
        "fdr",
        "f1_skeleton",
    )
    assert CITestEvaluator.metric_keys == ("power", "fpr", "f1_ci", "calibration_error")
    assert EffectEstimationEvaluator.metric_keys == (
        "ate_abs_error",
        "ate_rel_error",
        "ci_coverage",
        "bias",
        "variance",
    )


@pytest.mark.unit
def test_evaluator_placeholders_raise_not_implemented() -> None:
    gt = GroundTruth(
        dag=object(),
        adjacency_matrix=pd.DataFrame([[0]]),
        d_separations=[],
        ate_values={},
    )

    with pytest.raises(NotImplementedError, match="Phase 4"):
        CausalDiscoveryEvaluator().evaluate(object(), gt)

    with pytest.raises(NotImplementedError, match="Phase 4"):
        CITestEvaluator().evaluate(object(), gt)

    with pytest.raises(NotImplementedError, match="Phase 5"):
        EffectEstimationEvaluator().evaluate(object(), gt)


@pytest.mark.unit
def test_register_evaluator_decorator() -> None:
    name = "phase1_test_custom"
    if name in EVALUATOR_REGISTRY:
        del EVALUATOR_REGISTRY[name]

    @register_evaluator(name)
    class PhaseOneCustomEvaluator(BaseEvaluator):
        metric_keys: tuple[str, ...] = ("custom",)

        def evaluate(
            self, predicted: object, ground_truth: GroundTruth
        ) -> dict[str, float]:
            _ = (predicted, ground_truth)
            return {"custom": 0.0}

    assert EVALUATOR_REGISTRY[name] is PhaseOneCustomEvaluator

    with pytest.raises(ValueError, match="already registered"):

        @register_evaluator(name)
        class DuplicatePhaseOneCustomEvaluator(BaseEvaluator):
            metric_keys: tuple[str, ...] = ("custom",)

            def evaluate(
                self, predicted: object, ground_truth: GroundTruth
            ) -> dict[str, float]:
                _ = (predicted, ground_truth)
                return {"custom": 0.0}

    del EVALUATOR_REGISTRY[name]
