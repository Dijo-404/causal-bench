"""Stub for the BenchmarkRunner layer (Layer 2).

This module will orchestrate combinatorial experiments across simulators,
causal discovery methods, and random seeds. Implementation is planned for
the next milestone.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from causal_bench.simulators.base import BaseSimulator


class BenchmarkRunner:
    """Executes experiments across all (simulator, method, seed) combinations.

    Note:
        This class is a **placeholder** stub. The full implementation will
        be delivered in the Layer 2 milestone.
    """

    def __init__(self, simulators: list[BaseSimulator]) -> None:
        """Initialize the runner.

        Args:
            simulators: A list of configured simulator instances whose
                :meth:`~causal_bench.simulators.base.BaseSimulator.simulate`
                methods will be called during the benchmark sweep.
        """
        self.simulators = simulators

    def run(self) -> None:
        """Execute the full combinatorial benchmark sweep.

        Raises:
            NotImplementedError: Until Layer 2 is implemented.
        """
        raise NotImplementedError("BenchmarkRunner is not yet implemented.")
