# causal-bench

A composable benchmarking framework for causal discovery algorithms and
conditional independence tests, built on top of [pgmpy](https://pgmpy.org/).

This project is being developed as part of **Google Summer of Code 2026**.

---

## Architecture

The framework is organized as four composable layers:

| Layer | Class | Responsibility |
|---|---|---|
| 1 | `BaseSimulator` | Generate synthetic data and ground-truth DAGs |
| 2 | `BenchmarkRunner` | Execute combinatorial experiments across simulators, methods, and seeds |
| 3 | `BaseEvaluator` | Compute task-specific metrics (SHD, F1, Power, …) |
| 4 | `BenchmarkReport` | Serialize results to JSON, CSV, and pandas DataFrames |

## Installation

```bash
# Editable install for development
pip install -e ".[dev]"
```

## Quick Start

```python
from causal_bench.simulators import RandomDAGSimulator

sim = RandomDAGSimulator(n_nodes=5, edge_density=0.3, functional_form="linear")
data, ground_truth = sim.simulate(n_samples=500, seed=42)

print(data.head())
print(ground_truth.adjacency_matrix())
```

## Development

```bash
pytest          # run tests
ruff check src  # lint
mypy src        # type-check
```