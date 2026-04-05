"""Random DAG simulator scaffold for the benchmarking framework."""

from __future__ import annotations

from typing import Literal

import pandas as pd

from .base import BaseSimulator, GroundTruth


class RandomDAGSimulator(BaseSimulator):
    """Generate synthetic datasets from random causal DAGs.

    Full graph generation and sampling behavior is implemented in Phase 2.
    """

    def __init__(
        self,
        n_nodes: int = 10,
        edge_density: float = 0.3,
        functional_form: Literal[
            "linear_gaussian", "discrete", "additive_noise"
        ] = "linear_gaussian",
        n_samples: int = 1000,
    ) -> None:
        if n_nodes < 2:
            raise ValueError("n_nodes must be >= 2")
        if not 0.0 < edge_density < 1.0:
            raise ValueError("edge_density must be in the open interval (0, 1)")
        if n_samples < 1:
            raise ValueError("n_samples must be >= 1")

        self.n_nodes = n_nodes
        self.edge_density = edge_density
        self.functional_form = functional_form
        self.n_samples = n_samples

    def simulate(self, n_samples: int, seed: int) -> tuple[pd.DataFrame, GroundTruth]:
        """Generate data and complete ground truth for one seeded run.

        Raises:
            NotImplementedError: Until Phase 2 simulator implementation lands.
        """
        _ = (n_samples, seed)
        raise NotImplementedError(
            "RandomDAGSimulator.simulate is scheduled for Phase 2. "
            "Phase 1 defines only the stable public interface."
        )
