"""Simulator interfaces and shared data structures for benchmarks."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import TypeVar

import pandas as pd


@dataclass(slots=True)
class GroundTruth:
    """Ground-truth artifacts emitted by a simulator.

    Attributes:
        dag: Ground-truth causal graph object.
        adjacency_matrix: Binary adjacency matrix of the ground-truth graph.
        d_separations: Triples of known d-separation statements.
        ate_values: Ground-truth average treatment effects keyed by variable pair.
        partial: Whether the ground truth is incomplete.
        metadata: Extra run metadata for traceability.
    """

    dag: object
    adjacency_matrix: pd.DataFrame
    d_separations: list[tuple]
    ate_values: dict[tuple[str, str], float]
    partial: bool = False
    metadata: dict[str, object] = field(default_factory=dict)


TBaseSimulator = TypeVar("TBaseSimulator", bound="BaseSimulator")


class BaseSimulator(ABC):
    """Abstract simulator contract for generating benchmark datasets."""

    config: dict[str, object]

    @abstractmethod
    def simulate(self, n_samples: int, seed: int) -> tuple[pd.DataFrame, GroundTruth]:
        """Return dataset and ground truth for a deterministic seed."""

    def to_config(self) -> dict[str, object]:
        """Serialize simulator configuration for reproducibility records."""
        return {k: v for k, v in vars(self).items() if not k.startswith("_")}

    @classmethod
    def from_config(
        cls: type[TBaseSimulator], config: dict[str, object]
    ) -> TBaseSimulator:
        """Reconstruct a simulator instance from JSON-compatible configuration."""
        return cls(**config)  # type: ignore[arg-type]
