"""Shared type definitions used across the causal-bench framework."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import networkx as nx
import pandas as pd


@dataclass(frozen=True)
class GroundTruth:
    """Immutable ground-truth information produced by a simulator.

    Attributes:
        dag: The directed acyclic graph representing the true causal structure.
            Nodes are variable names; edges encode direct causal relationships.
        cpds: A mapping from node name to its conditional probability
            distribution or structural equation parameters. The exact schema
            depends on the functional form used by the simulator.
        metadata: Optional free-form metadata about the simulation (e.g.,
            functional form, noise type, edge density).
    """

    dag: nx.DiGraph
    cpds: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    def adjacency_matrix(self) -> pd.DataFrame:
        """Return the adjacency matrix of the true DAG as a DataFrame.

        Returns:
            A binary DataFrame where entry (i, j) is 1 if there is a directed
            edge from node i to node j, and 0 otherwise.
        """
        nodes = list(self.dag.nodes())
        matrix = nx.to_pandas_adjacency(self.dag, nodelist=nodes, dtype=int)
        return matrix
