import os
import sys

# Remove script directory to prevent namespace shadowing of real pgmpy
script_dir = os.path.abspath(os.path.dirname(__file__))
if sys.path[0] in ('', script_dir):
    sys.path.pop(0)

import pgmpy

sys.path.insert(0, os.path.join(script_dir, "pgmpy"))
import benchmark

sys.modules["pgmpy.benchmark"] = benchmark
pgmpy.benchmark = benchmark

sys.path.insert(0, script_dir)

sys.modules["pgmpy.benchmark"] = benchmark
pgmpy.benchmark = benchmark

from pgmpy.estimators import GES as _GES  # noqa: E402
from pgmpy.estimators import PC as _PC  # noqa: E402
from pgmpy.estimators import MmhcEstimator as _MmhcEstimator  # noqa: E402

from pgmpy.benchmark import (  # noqa: E402
    BenchmarkRunner,
    CausalDiscoveryEvaluator,
    RandomDAGSimulator,
)


class PC:
    def fit(self, data):
        self.model_ = _PC(data=data).estimate(return_type="dag", show_progress=False)
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
