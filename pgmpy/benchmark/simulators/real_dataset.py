"""Real dataset simulator scaffold."""

from __future__ import annotations

import pandas as pd

from .base import BaseSimulator, GroundTruth


class RealDatasetSimulator(BaseSimulator):
    """Wrap datasets from ``pgmpy.utils.datasets`` as benchmark simulators."""

    def __init__(self, dataset_name: str, known_dag: object | None = None) -> None:
        if not dataset_name:
            raise ValueError("dataset_name must be a non-empty string")

        self.dataset_name = dataset_name
        self.known_dag = known_dag

    def simulate(self, n_samples: int, seed: int) -> tuple[pd.DataFrame, GroundTruth]:
        """Return dataset samples and partial or complete ground truth.

        Raises:
            NotImplementedError: Until Phase 3 dataset wiring is implemented.
        """
        _ = (n_samples, seed)
        raise NotImplementedError(
            "RealDatasetSimulator.simulate is scheduled for Phase 3. "
            "Phase 1 defines only the stable public interface."
        )
