"""Benchmark result records and report utilities."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

import pandas as pd


@dataclass(slots=True)
class ResultRecord:
    """One benchmark trial record."""

    method_name: str
    simulator_config: dict[str, object]
    seed: int
    metrics: dict[str, float]
    runtime_ms: int
    pgmpy_version: str
    python_version: str
    error: str | None = None

    @classmethod
    def from_dict(cls, payload: dict[str, object]) -> ResultRecord:
        """Create a typed record from JSON-compatible payload data."""
        metrics_raw = payload.get("metrics", {})
        if not isinstance(metrics_raw, dict):
            raise TypeError("metrics must be a dictionary")
        metrics = {str(k): float(v) for k, v in metrics_raw.items()}

        simulator_config = payload.get("simulator_config", {})
        if not isinstance(simulator_config, dict):
            raise TypeError("simulator_config must be a dictionary")

        return cls(
            method_name=str(payload.get("method_name", "")),
            simulator_config=dict(simulator_config),
            seed=int(payload.get("seed", 0)),
            metrics=metrics,
            runtime_ms=int(payload.get("runtime_ms", 0)),
            pgmpy_version=str(payload.get("pgmpy_version", "unknown")),
            python_version=str(payload.get("python_version", "unknown")),
            error=(
                str(payload["error"])
                if payload.get("error") is not None
                else None
            ),
        )


class BenchmarkReport:
    """Container with export and aggregation utilities for benchmark records."""

    def __init__(self, records: list[ResultRecord]) -> None:
        self.records = records

    def to_json(self, path: str | None = None) -> str:
        """Serialize all records to JSON, optionally writing to disk."""
        payload = {"records": [asdict(record) for record in self.records]}
        json_str = json.dumps(payload, indent=2, sort_keys=True)

        if path is not None:
            Path(path).write_text(json_str, encoding="utf-8")

        return json_str

    @classmethod
    def from_json(cls, path: str) -> BenchmarkReport:
        """Load a report from a JSON file."""
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
        records_payload = payload.get("records", [])
        if not isinstance(records_payload, list):
            raise ValueError("Invalid report JSON: 'records' must be a list")

        records = [ResultRecord.from_dict(item) for item in records_payload]
        return cls(records=records)

    def to_dataframe(self) -> pd.DataFrame:
        """Return a flat DataFrame with one row per trial."""
        rows: list[dict[str, object]] = []
        for record in self.records:
            row: dict[str, object] = {
                "method_name": record.method_name,
                "simulator_config": json.dumps(
                    record.simulator_config, sort_keys=True
                ),
                "seed": record.seed,
                "runtime_ms": record.runtime_ms,
                "pgmpy_version": record.pgmpy_version,
                "python_version": record.python_version,
                "error": record.error,
            }
            row.update(record.metrics)
            rows.append(row)

        return pd.DataFrame(rows)

    def to_csv(self, path: str) -> None:
        """Export report data as CSV."""
        self.to_dataframe().to_csv(path, index=False)

    def summary(self) -> pd.DataFrame:
        """Compute mean and std for all metric columns grouped by method."""
        df = self.to_dataframe()
        if df.empty:
            return pd.DataFrame()

        excluded_columns = {
            "method_name",
            "simulator_config",
            "seed",
            "runtime_ms",
            "pgmpy_version",
            "python_version",
            "error",
        }
        metric_columns = [c for c in df.columns if c not in excluded_columns]

        if not metric_columns:
            return df[["method_name"]].drop_duplicates().reset_index(drop=True)

        summary_df = df.groupby("method_name", dropna=False)[metric_columns].agg(
            ["mean", "std"]
        )
        summary_df.columns = [
            f"{metric}_{stat}" for metric, stat in summary_df.columns.to_flat_index()
        ]
        return summary_df.reset_index()

    def latex_table(self) -> str:
        """Render the summary table as LaTeX (booktabs-style)."""
        summary_df = self.summary()
        if summary_df.empty:
            return ""

        columns = summary_df.columns.tolist()
        column_spec = "l" + "r" * (len(columns) - 1)
        lines = [
            rf"\begin{{tabular}}{{{column_spec}}}",
            r"\toprule",
            " & ".join(columns) + r" \\",
            r"\midrule",
        ]

        for _, row in summary_df.iterrows():
            cells: list[str] = []
            for column in columns:
                value = row[column]
                if isinstance(value, float):
                    cells.append("nan" if pd.isna(value) else f"{value:.4f}")
                else:
                    cells.append(str(value))

            lines.append(" & ".join(cells) + r" \\")

        lines.extend([r"\bottomrule", r"\end{tabular}"])
        return "\n".join(lines)
