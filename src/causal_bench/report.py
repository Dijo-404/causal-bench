"""Stub for the BenchmarkReport layer (Layer 4).

BenchmarkReport will serialize raw run results into structured JSON, CSV,
and pandas DataFrames for downstream analysis and visualization.
"""

from __future__ import annotations


class BenchmarkReport:
    """Packages benchmark results into structured, serializable formats.

    Note:
        This class is a **placeholder** stub. The full implementation will
        be delivered in the Layer 4 milestone.
    """

    def to_dataframe(self) -> None:
        """Convert results to a pandas DataFrame.

        Raises:
            NotImplementedError: Until Layer 4 is implemented.
        """
        raise NotImplementedError("BenchmarkReport is not yet implemented.")

    def to_json(self, path: str) -> None:
        """Write results to a JSON file.

        Args:
            path: Filesystem path for the output JSON file.

        Raises:
            NotImplementedError: Until Layer 4 is implemented.
        """
        raise NotImplementedError("BenchmarkReport is not yet implemented.")

    def to_csv(self, path: str) -> None:
        """Write results to a CSV file.

        Args:
            path: Filesystem path for the output CSV file.

        Raises:
            NotImplementedError: Until Layer 4 is implemented.
        """
        raise NotImplementedError("BenchmarkReport is not yet implemented.")
