from abc import ABC, abstractmethod
import networkx as nx
from typing import Dict
from ..simulators.base import GroundTruth

class BaseEvaluator(ABC):
    @abstractmethod
    def evaluate(self, predicted: nx.DiGraph, ground_truth: GroundTruth) -> Dict[str, float]:
        pass
