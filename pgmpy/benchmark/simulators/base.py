from abc import ABC, abstractmethod
from dataclasses import dataclass

import networkx as nx
import pandas as pd


@dataclass
class GroundTruth:
    dag: nx.DiGraph


class BaseSimulator(ABC):
    @abstractmethod
    def simulate(self, n_samples: int, seed: int) -> tuple[pd.DataFrame, GroundTruth]:
        pass
