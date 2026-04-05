"""Parametric sweep simulator scaffold."""

from __future__ import annotations

from itertools import product

import pandas as pd

from .base import BaseSimulator, GroundTruth


class ParametricSweepSimulator(BaseSimulator):
    """Generate simulator configurations across a parameter grid."""

    def __init__(
        self,
        base_simulator_cls: type[BaseSimulator],
        param_grid: dict[str, list[object]],
    ) -> None:
        if not param_grid:
            raise ValueError("param_grid must contain at least one parameter")

        self.base_simulator_cls = base_simulator_cls
        self.param_grid = param_grid

    def iter_configs(self) -> list[dict[str, object]]:
        """Return Cartesian-product configurations from the parameter grid."""
        keys = list(self.param_grid.keys())
        value_lists = [self.param_grid[key] for key in keys]
        return [
            dict(zip(keys, values, strict=True))
            for values in product(*value_lists)
        ]

    def simulate(self, n_samples: int, seed: int) -> tuple[pd.DataFrame, GroundTruth]:
        """Produce one sample for the current sweep configuration.

        Raises:
            NotImplementedError: Until Phase 5 sweep execution implementation.
        """
        _ = (n_samples, seed)
        raise NotImplementedError(
            "ParametricSweepSimulator.simulate is scheduled for Phase 5. "
            "Phase 1 defines only the stable public interface."
        )
