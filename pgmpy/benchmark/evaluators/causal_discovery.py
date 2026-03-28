import networkx as nx

from ..simulators.base import GroundTruth
from .base import BaseEvaluator


class CausalDiscoveryEvaluator(BaseEvaluator):
    def evaluate(
        self, predicted: nx.DiGraph, ground_truth: GroundTruth
    ) -> dict[str, float]:
        true_dag = ground_truth.dag

        true_edges = set(true_dag.edges())
        try:
            pred_edges = set(predicted.edges())
        except Exception:
            pred_edges = set()

        missing = 0
        extra = 0
        reversed_edges = 0

        for e in true_edges:
            if e not in pred_edges:
                if (e[1], e[0]) in pred_edges:
                    reversed_edges += 1
                else:
                    missing += 1

        for e in pred_edges:
            if e not in true_edges and (e[1], e[0]) not in true_edges:
                extra += 1

        shd = missing + extra + reversed_edges

        tp = len(pred_edges.intersection(true_edges))
        fp = len(pred_edges - true_edges)
        fn = len(true_edges - pred_edges)

        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = (
            2 * (precision * recall) / (precision + recall)
            if (precision + recall) > 0
            else 0.0
        )

        return {"SHD": float(shd), "F1": float(f1)}
