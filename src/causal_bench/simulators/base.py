"""Abstract base class for all causal-bench simulators."""

from __future__ import annotations

from abc import ABC, abstractmethod

import pandas as pd

from causal_bench.types import GroundTruth

SimulationResult = tuple[pd.DataFrame, GroundTruth]


class BaseSimulator(ABC):
    """Abstract interface for data-generating processes in causal-bench.

    Every concrete simulator must implement :meth:`simulate`, which returns
    a synthetic dataset alongside the corresponding ground-truth causal
    structure. The contract guarantees that:

    * Running :meth:`simulate` with the same ``seed`` always produces
      identical output (reproducibility).
    * The returned :class:`~causal_bench.types.GroundTruth` fully describes
      the true causal structure so that evaluators can compute metrics without
      any knowledge of the simulator internals.

    Example:
        Define a minimal concrete simulator::

            class MySimulator(BaseSimulator):
                def simulate(
                    self, n_samples: int, seed: int
                ) -> SimulationResult:
                    rng = np.random.default_rng(seed)
                    data = pd.DataFrame({"X": rng.normal(size=n_samples)})
                    dag = nx.DiGraph()
                    dag.add_node("X")
                    return data, GroundTruth(dag=dag)
    """

    @abstractmethod
    def simulate(self, n_samples: int, seed: int) -> SimulationResult:
        """Generate a synthetic dataset and its ground-truth causal structure.

        Args:
            n_samples: Number of i.i.d. observations to generate.
            seed: Random seed for full reproducibility.

        Returns:
            A two-element tuple ``(data, ground_truth)`` where ``data`` is a
            :class:`pandas.DataFrame` with one column per variable and
            ``ground_truth`` is a :class:`~causal_bench.types.GroundTruth`
            containing the true DAG and optional structural parameters.

        Raises:
            ValueError: If ``n_samples`` or ``seed`` are negative.
        """
        ...
