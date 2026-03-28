from dataclasses import dataclass

import pandas as pd


@dataclass
class ResultRecord:
    method_name: str
    seed: int
    metrics: dict
    runtime_ms: int
    error: str | None


class BenchmarkReport:
    def __init__(self, records: list[ResultRecord]):
        self.records = records

    def to_dataframe(self) -> pd.DataFrame:
        data = []
        for r in self.records:
            row = {
                "Method": r.method_name,
                "Seed": r.seed,
                "Runtime (ms)": r.runtime_ms,
                "Error": r.error,
            }
            row.update(r.metrics)
            data.append(row)
        return pd.DataFrame(data)

    def summary(self):
        df = self.to_dataframe()
        print("\n--- Benchmark Summary ---")
        if df.empty:
            print("No successful runs.")
            return

        metric_cols = [
            c
            for c in df.columns
            if c not in ["Method", "Seed", "Runtime (ms)", "Error"]
        ]

        agg_dict = {m: "mean" for m in metric_cols}
        agg_dict["Runtime (ms)"] = "mean"

        summary_df = df.groupby("Method").agg(agg_dict).reset_index()
        summary_df = summary_df.rename(columns={m: f"Mean {m}" for m in metric_cols})
        summary_df = summary_df.rename(columns={"Runtime (ms)": "Mean Runtime (ms)"})

        print(summary_df.to_string(index=False))
