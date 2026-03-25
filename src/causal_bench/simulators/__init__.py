"""Simulator sub-package for causal-bench.

Exports the main simulator classes for convenience::

    from causal_bench.simulators import BaseSimulator, RandomDAGSimulator
"""

from causal_bench.simulators.base import BaseSimulator, SimulationResult
from causal_bench.simulators.random_dag import RandomDAGSimulator

__all__ = ["BaseSimulator", "SimulationResult", "RandomDAGSimulator"]
