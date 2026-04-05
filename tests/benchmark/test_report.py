"""Phase 1 tests for BenchmarkReport serialization and tabulation."""

from __future__ import annotations

import json

import pandas as pd
import pytest

from pgmpy.benchmark.report import BenchmarkReport, ResultRecord


@pytest.fixture
def sample_records() -> list[ResultRecord]:
    return [
        ResultRecord(
            method_name="PC",
            simulator_config={"type": "RandomDAGSimulator", "n_nodes": 5},
            seed=0,
            metrics={"shd": 2.0, "f1_directed": 0.8},
            runtime_ms=120,
            pgmpy_version="0.1.26",
            python_version="3.12.0",
            error=None,
        ),
        ResultRecord(
            method_name="PC",
            simulator_config={"type": "RandomDAGSimulator", "n_nodes": 5},
            seed=1,
            metrics={"shd": 3.0, "f1_directed": 0.7},
            runtime_ms=110,
            pgmpy_version="0.1.26",
            python_version="3.12.0",
            error=None,
        ),
    ]


@pytest.mark.unit
def test_report_to_dataframe(sample_records: list[ResultRecord]) -> None:
    report = BenchmarkReport(records=sample_records)
    df = report.to_dataframe()

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    assert "method_name" in df.columns
    assert "shd" in df.columns


@pytest.mark.unit
def test_report_json_round_trip(
    tmp_path, sample_records: list[ResultRecord]
) -> None:
    report = BenchmarkReport(records=sample_records)
    path = tmp_path / "report.json"

    json_string = report.to_json(str(path))
    payload = json.loads(json_string)
    assert "records" in payload

    loaded = BenchmarkReport.from_json(str(path))
    assert len(loaded.records) == 2
    assert loaded.records[0].method_name == "PC"


@pytest.mark.unit
def test_report_summary_and_latex(sample_records: list[ResultRecord]) -> None:
    report = BenchmarkReport(records=sample_records)

    summary_df = report.summary()
    assert "method_name" in summary_df.columns
    assert "shd_mean" in summary_df.columns

    latex = report.latex_table()
    assert "tabular" in latex
