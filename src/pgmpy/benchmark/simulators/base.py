from abc import ABC, abstractmethod
from dataclasses import dataclass
import pandas as pd
import networkx as nx
from typing import Tuple

@dataclass
class GroundTruth:
    dag: nx.DiGraph

class BaseSimulator(ABC):
    @abstractmethod
    def simulate(self, n_samples: int, seed: int) -> Tuple[pd.DataFrame, GroundTruth]:
        pass
