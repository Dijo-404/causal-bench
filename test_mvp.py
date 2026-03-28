import sys
import os

sys.path.insert(0, os.path.abspath('src/pgmpy'))
import benchmark
sys.modules['pgmpy.benchmark'] = benchmark

from pgmpy.benchmark import BenchmarkRunner, RandomDAGSimulator, CausalDiscoveryEvaluator
from pgmpy.estimators import PC as _PC, GES as _GES, MmhcEstimator as _MmhcEstimator

class PC:
    def fit(self, data):
        # pgmpy PC.estimate() will run. Use 'dag' return_type if possible, else default
        self.model_ = _PC(data=data).estimate(return_type='dag', show_progress=False)
        return self

class GES:
    def fit(self, data):
        self.model_ = _GES(data=data).estimate()
        return self

class MmhcEstimator:
    def fit(self, data):
        self.model_ = _MmhcEstimator(data=data).estimate()
        return self

runner = BenchmarkRunner(
    simulators=[RandomDAGSimulator(n_nodes=6, edge_density=0.3)],
    methods=[PC(), GES(), MmhcEstimator()],
    evaluators=[CausalDiscoveryEvaluator()],
    n_seeds=5,
)
report = runner.run()
report.summary()
