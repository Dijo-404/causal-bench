"""Phase 1 tests for simulator API contracts and scaffolding."""

from __future__ import annotations

import pandas as pd
import pytest

from pgmpy.benchmark.simulators import (
    BaseSimulator,
    GroundTruth,
    ParametricSweepSimulator,
    RandomDAGSimulator,
    RealDatasetSimulator,
)


def test_base_simulator_is_abstract() -> None:
    with pytest.raises(TypeError):
        BaseSimulator()  # type: ignore[abstract]


def test_ground_truth_dataclass_fields() -> None:
    matrix = pd.DataFrame([[0, 1], [0, 0]], columns=["A", "B"], index=["A", "B"])
    gt = GroundTruth(
        dag=object(),
        adjacency_matrix=matrix,
        d_separations=[("A", "B", tuple())],
        ate_values={("A", "B"): 1.25},
        partial=False,
    )

    assert gt.adjacency_matrix.shape == (2, 2)
    assert gt.ate_values[("A", "B")] == pytest.approx(1.25)


def test_random_dag_defaults_and_config_round_trip() -> None:
    simulator = RandomDAGSimulator()
    config = simulator.to_config()
    rebuilt = RandomDAGSimulator.from_config(config)

    assert rebuilt.to_config() == config
    assert rebuilt.functional_form == "linear_gaussian"


def test_random_dag_validate_parameters() -> None:
    with pytest.raises(ValueError, match="n_nodes"):
        RandomDAGSimulator(n_nodes=1)

    with pytest.raises(ValueError, match="edge_density"):
        RandomDAGSimulator(edge_density=0.0)

    with pytest.raises(ValueError, match="n_samples"):
        RandomDAGSimulator(n_samples=0)


def test_random_dag_simulate_is_phase_two_placeholder() -> None:
    simulator = RandomDAGSimulator()
    with pytest.raises(NotImplementedError, match="Phase 2"):
        simulator.simulate(n_samples=10, seed=0)


def test_real_dataset_validate_dataset_name() -> None:
    with pytest.raises(ValueError, match="dataset_name"):
        RealDatasetSimulator(dataset_name="")


def test_real_dataset_is_phase_three_placeholder() -> None:
    simulator = RealDatasetSimulator(dataset_name="dummy")
    with pytest.raises(NotImplementedError, match="Phase 3"):
        simulator.simulate(n_samples=10, seed=1)


def test_parametric_sweep_config_generation() -> None:
    simulator = ParametricSweepSimulator(
        base_simulator_cls=RandomDAGSimulator,
        param_grid={"n_nodes": [5, 10], "edge_density": [0.2, 0.3]},
    )
    configs = simulator.iter_configs()
    assert len(configs) == 4
    assert {"n_nodes", "edge_density"}.issubset(configs[0].keys())


def test_parametric_sweep_is_phase_five_placeholder() -> None:
    simulator = ParametricSweepSimulator(
        base_simulator_cls=RandomDAGSimulator,
        param_grid={"n_nodes": [5]},
    )
    with pytest.raises(NotImplementedError, match="Phase 5"):
        simulator.simulate(n_samples=10, seed=1)
