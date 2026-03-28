import logging
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

from pgmpy.causal_discovery import GES, HillClimbSearch, PC  # noqa: E402

from pgmpy.benchmark import (  # noqa: E402
    BenchmarkRunner,
    CausalDiscoveryEvaluator,
    RandomDAGSimulator,
)

class MMHC(HillClimbSearch):
    """Alias to display 'MMHC' organically in the summary table!"""
    pass

runner = BenchmarkRunner(
    simulators=[RandomDAGSimulator(n_nodes=6, edge_density=0.3)],
    methods=[
        PC(show_progress=False, n_jobs=1),
        GES(),
        MMHC(show_progress=False),
    ],
    evaluators=[CausalDiscoveryEvaluator()],
    n_seeds=10,
)
report = runner.run()
report.summary()
