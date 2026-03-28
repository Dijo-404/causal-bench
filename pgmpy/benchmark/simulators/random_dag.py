import networkx as nx
import numpy as np
import pandas as pd
from pgmpy.factors.discrete import TabularCPD
from pgmpy.models import DiscreteBayesianNetwork

from .base import BaseSimulator, GroundTruth


class RandomDAGSimulator(BaseSimulator):
    def __init__(self, n_nodes: int, edge_density: float):
        self.n_nodes = n_nodes
        self.edge_density = edge_density

    def simulate(self, n_samples: int, seed: int) -> tuple[pd.DataFrame, GroundTruth]:
        np.random.seed(seed)

        graph = nx.fast_gnp_random_graph(
            self.n_nodes, self.edge_density, seed=seed, directed=True
        )
        dag = nx.DiGraph()
        dag.add_nodes_from([str(n) for n in graph.nodes()])
        for u, v in graph.edges():
            if u < v:
                dag.add_edge(str(u), str(v))
            elif u > v:
                dag.add_edge(str(v), str(u))

        model = DiscreteBayesianNetwork(list(dag.edges()))
        model.add_nodes_from(dag.nodes())

        for node in model.nodes():
            parents = model.get_parents(node)
            n_parents = len(parents)

            probabilities = np.random.rand(2, 2**n_parents)
            probabilities = probabilities / probabilities.sum(axis=0)

            cpd = TabularCPD(
                variable=node,
                variable_card=2,
                values=probabilities,
                evidence=parents if parents else None,
                evidence_card=[2] * n_parents if parents else None,
            )
            model.add_cpds(cpd)

        df = model.simulate(n_samples=n_samples, show_progress=False)
        return df, GroundTruth(dag=dag)
