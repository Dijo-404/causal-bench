"""Phase 1 smoke tests for package exports and module structure."""

from __future__ import annotations

import pgmpy.benchmark as benchmark


def test_public_exports_present() -> None:
    required_exports = {
        "BaseSimulator",
        "GroundTruth",
        "RandomDAGSimulator",
        "RealDatasetSimulator",
        "ParametricSweepSimulator",
        "BaseEvaluator",
        "CausalDiscoveryEvaluator",
        "CITestEvaluator",
        "EffectEstimationEvaluator",
        "register_evaluator",
        "BenchmarkRunner",
        "BenchmarkReport",
        "ResultRecord",
    }

    assert required_exports.issubset(set(benchmark.__all__))
