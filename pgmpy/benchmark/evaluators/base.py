from abc import ABC, abstractmethod

import networkx as nx

from ..simulators.base import GroundTruth


class BaseEvaluator(ABC):
    @abstractmethod
    def evaluate(
        self, predicted: nx.DiGraph, ground_truth: GroundTruth
    ) -> dict[str, float]:
        pass
