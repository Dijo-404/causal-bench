"""Tests for the simulator layer (Layer 1)."""

from __future__ import annotations

import pandas as pd
import pytest
from causal_bench.simulators import RandomDAGSimulator
from causal_bench.simulators.base import BaseSimulator
from causal_bench.types import GroundTruth


class TestBaseSimulatorContract:
    """Verify the ABC contract prevents direct instantiation."""

    def test_cannot_instantiate_base_directly(self) -> None:
        with pytest.raises(TypeError):
            BaseSimulator()  # type: ignore[abstract]


class TestGroundTruth:
    """Unit tests for the GroundTruth dataclass."""

    def test_adjacency_matrix_shape(self) -> None:
        sim = RandomDAGSimulator(n_nodes=4, edge_density=0.5)
        _, gt = sim.simulate(n_samples=100, seed=0)
        matrix = gt.adjacency_matrix()
        assert matrix.shape == (4, 4), "Adjacency matrix must be (n_nodes x n_nodes)."

    def test_adjacency_matrix_is_binary(self) -> None:
        sim = RandomDAGSimulator(n_nodes=4, edge_density=0.9)
        _, gt = sim.simulate(n_samples=100, seed=0)
        matrix = gt.adjacency_matrix()
        unique_values = set(matrix.values.flatten().tolist())
        assert unique_values <= {0, 1}, "Adjacency matrix must contain only 0 and 1."


class TestRandomDAGSimulatorInit:
    """Parameter validation tests for RandomDAGSimulator.__init__."""

    def test_default_parameters_are_valid(self) -> None:
        sim = RandomDAGSimulator()
        assert sim.n_nodes == 5
        assert sim.edge_density == 0.3
        assert sim.functional_form == "linear"

    def test_invalid_n_nodes_raises(self) -> None:
        with pytest.raises(ValueError, match="n_nodes"):
            RandomDAGSimulator(n_nodes=0)

    def test_invalid_edge_density_zero_raises(self) -> None:
        with pytest.raises(ValueError, match="edge_density"):
            RandomDAGSimulator(edge_density=0.0)

    def test_invalid_edge_density_one_raises(self) -> None:
        with pytest.raises(ValueError, match="edge_density"):
            RandomDAGSimulator(edge_density=1.0)


class TestRandomDAGSimulatorSimulate:
    """Behavioral tests for RandomDAGSimulator.simulate."""

    def test_returns_correct_types(self) -> None:
        sim = RandomDAGSimulator(n_nodes=3)
        data, gt = sim.simulate(n_samples=50, seed=1)
        assert isinstance(data, pd.DataFrame)
        assert isinstance(gt, GroundTruth)

    def test_data_shape(self) -> None:
        n_nodes, n_samples = 6, 200
        sim = RandomDAGSimulator(n_nodes=n_nodes)
        data, _ = sim.simulate(n_samples=n_samples, seed=2)
        assert data.shape == (n_samples, n_nodes), (
            f"Expected ({n_samples}, {n_nodes}), got {data.shape}."
        )

    def test_reproducibility_same_seed(self) -> None:
        sim = RandomDAGSimulator(n_nodes=5)
        data1, gt1 = sim.simulate(n_samples=100, seed=42)
        data2, gt2 = sim.simulate(n_samples=100, seed=42)
        pd.testing.assert_frame_equal(data1, data2)
        assert list(gt1.dag.edges()) == list(gt2.dag.edges())

    def test_different_seeds_produce_different_data(self) -> None:
        sim = RandomDAGSimulator(n_nodes=5)
        data1, _ = sim.simulate(n_samples=100, seed=0)
        data2, _ = sim.simulate(n_samples=100, seed=1)
        assert not data1.equals(data2), "Different seeds should produce different data."

    def test_metadata_recorded(self) -> None:
        sim = RandomDAGSimulator(
            n_nodes=4, edge_density=0.5, functional_form="nonlinear"
        )
        _, gt = sim.simulate(n_samples=50, seed=7)
        assert gt.metadata["n_nodes"] == 4
        assert gt.metadata["edge_density"] == 0.5
        assert gt.metadata["functional_form"] == "nonlinear"
        assert gt.metadata["seed"] == 7

    def test_negative_n_samples_raises(self) -> None:
        sim = RandomDAGSimulator()
        with pytest.raises(ValueError, match="n_samples"):
            sim.simulate(n_samples=0, seed=0)

    def test_negative_seed_raises(self) -> None:
        sim = RandomDAGSimulator()
        with pytest.raises(ValueError, match="seed"):
            sim.simulate(n_samples=10, seed=-1)
