"""Simulator that samples random DAGs and generates synthetic observational data."""

from __future__ import annotations

from typing import Literal

import networkx as nx
import numpy as np
import pandas as pd

from causal_bench.simulators.base import BaseSimulator, SimulationResult
from causal_bench.types import GroundTruth

FunctionalForm = Literal["linear", "nonlinear"]


class RandomDAGSimulator(BaseSimulator):
    """Generates synthetic data from a randomly sampled DAG.

    The simulator follows a two-phase procedure:

    1. **Structure phase** — sample a random DAG with ``n_nodes`` nodes and
       approximately ``edge_density`` expected edge probability per node pair.
    2. **Data phase** — draw ``n_samples`` observations from the joint
       distribution implied by the DAG using the specified ``functional_form``.

    Both phases are seeded deterministically from the ``seed`` argument passed
    to :meth:`simulate`, so all results are fully reproducible.

    Note:
        Data generation is currently **mocked** (returns Gaussian noise with
        zero causal signal). The full structural-equation model will be wired
        up in a subsequent implementation pass.

    Attributes:
        n_nodes: Number of variables (nodes) in the sampled DAG.
        edge_density: Probability of including each candidate directed edge
            in the Erdos-Renyi-style DAG sampling procedure. Must be in
            ``(0, 1)``.
        functional_form: Structural equation type — either ``"linear"`` for
            linear additive noise models or ``"nonlinear"`` for GP-based
            nonlinear mechanisms.

    Example:
        ::

            sim = RandomDAGSimulator(n_nodes=5, edge_density=0.4)
            data, gt = sim.simulate(n_samples=1000, seed=0)
            print(gt.adjacency_matrix())
    """

    def __init__(
        self,
        n_nodes: int = 5,
        edge_density: float = 0.3,
        functional_form: FunctionalForm = "linear",
    ) -> None:
        """Initialize the simulator with structural hyper-parameters.

        Args:
            n_nodes: Number of nodes in the randomly sampled DAG.
                Must be a positive integer.
            edge_density: Expected edge probability per ordered node pair.
                Must satisfy ``0 < edge_density < 1``.
            functional_form: Structural equation type used during data
                generation. One of ``"linear"`` or ``"nonlinear"``.

        Raises:
            ValueError: If ``n_nodes < 1`` or ``edge_density`` is outside
                the open interval ``(0, 1)``.
        """
        if n_nodes < 1:
            raise ValueError(f"n_nodes must be >= 1, got {n_nodes}.")
        if not (0.0 < edge_density < 1.0):
            raise ValueError(
                f"edge_density must be in (0, 1), got {edge_density}."
            )

        self.n_nodes = n_nodes
        self.edge_density = edge_density
        self.functional_form: FunctionalForm = functional_form

    def _sample_dag(self, rng: np.random.Generator) -> nx.DiGraph:
        """Sample a random DAG using an upper-triangular Bernoulli mask.

        Nodes are topologically fixed as integers ``0 … n_nodes-1``.  For
        each ordered pair ``(i, j)`` with ``i < j``, an edge is included with
        probability :attr:`edge_density`.

        Args:
            rng: A seeded :class:`numpy.random.Generator` instance.

        Returns:
            A directed acyclic graph whose nodes are named ``"X0" … "Xk"``.
        """
        node_names = [f"X{i}" for i in range(self.n_nodes)]
        dag = nx.DiGraph()
        dag.add_nodes_from(node_names)

        for i in range(self.n_nodes):
            for j in range(i + 1, self.n_nodes):
                if rng.random() < self.edge_density:
                    dag.add_edge(node_names[i], node_names[j])

        return dag

    def _generate_data(
        self,
        dag: nx.DiGraph,
        n_samples: int,
        rng: np.random.Generator,
    ) -> pd.DataFrame:
        """Generate observational data from the sampled DAG.

        Note:
            This is a **mock** implementation that returns independent
            Gaussian noise for each node, ignoring causal structure.
            The full structural-equation model implementation is planned for
            a later milestone.

        Args:
            dag: The ground-truth DAG defining the causal structure.
            n_samples: Number of i.i.d. observations to draw.
            rng: A seeded :class:`numpy.random.Generator` instance.

        Returns:
            A :class:`pandas.DataFrame` with one column per node and
            ``n_samples`` rows.
        """
        data: dict[str, np.ndarray] = {}
        for node in nx.topological_sort(dag):
            data[node] = rng.standard_normal(n_samples)
        return pd.DataFrame(data)

    def simulate(self, n_samples: int, seed: int) -> SimulationResult:
        """Generate a random DAG and sample observational data from it.

        Args:
            n_samples: Number of i.i.d. observations to generate.
                Must be a positive integer.
            seed: Integer seed that fully determines the random DAG structure
                and the sampled observations.

        Returns:
            A tuple ``(data, ground_truth)`` where ``data`` is a
            :class:`pandas.DataFrame` of shape ``(n_samples, n_nodes)`` and
            ``ground_truth`` is a :class:`~causal_bench.types.GroundTruth`
            containing the true DAG and simulation metadata.

        Raises:
            ValueError: If ``n_samples < 1`` or ``seed < 0``.
        """
        if n_samples < 1:
            raise ValueError(f"n_samples must be >= 1, got {n_samples}.")
        if seed < 0:
            raise ValueError(f"seed must be >= 0, got {seed}.")

        rng = np.random.default_rng(seed)

        dag = self._sample_dag(rng)
        data = self._generate_data(dag, n_samples, rng)

        ground_truth = GroundTruth(
            dag=dag,
            metadata={
                "n_nodes": self.n_nodes,
                "edge_density": self.edge_density,
                "functional_form": self.functional_form,
                "seed": seed,
            },
        )

        return data, ground_truth
