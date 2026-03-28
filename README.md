# causal-bench

A composable benchmarking framework for causal discovery algorithms and conditional independence tests, built on top of [pgmpy](https://pgmpy.org/).

This project is being developed as part of **Google Summer of Code 2026**.

---

## Mission Statement

Build **causal-bench** — a standalone prototype repository that develops and validates `pgmpy.benchmark`, a composable, reproducible benchmarking module. The code is developed here and contributed upstream to pgmpy as a final PR. A full benchmark must be expressible in 10 lines of Python or less.

## Architecture

The framework is organized as four composable layers. Swapping any layer requires implementing exactly one method.

```mermaid
flowchart TD
    In([INPUT\nKnown models · Real datasets · External CSVs]):::input

    In --> L1

    subgraph L1 ["Layer 1 — Simulator"]
        direction TB
        S_API(["BaseSimulator.simulate"]):::api
        S1[RandomDAGSimulator]:::impl
        S2[RealDatasetSimulator]:::impl
        S3[ParametricSweepSimulator]:::impl
        S_API --> S1 & S2 & S3
    end

    L1 --> L2

    subgraph L2 ["Layer 2 — Benchmark Runner"]
        direction TB
        R_API(["BenchmarkRunner"]):::api
        R_Desc["Executes simulator × method × seed triples"]:::note
        R_API --> R_Desc
    end

    L2 --> L3

    subgraph L3 ["Layer 3 — Evaluator"]
        direction TB
        E_API(["BaseEvaluator.evaluate"]):::api
        E1[CausalDiscoveryEvaluator]:::impl
        E2[CITestEvaluator]:::impl
        E3[EffectEstimationEvaluator]:::impl
        E_API --> E1 & E2 & E3
    end

    L3 --> L4

    subgraph L4 ["Layer 4 — Benchmark Report"]
        direction TB
        Rep_API(["BenchmarkReport"]):::api
        Rep_Out["JSON · CSV · DataFrame · LaTeX · Summary"]:::note
        Rep_API --> Rep_Out
    end

    classDef input  fill:#4a4a8a,stroke:#7a7acc,color:#fff
    classDef api    fill:#2d6a4f,stroke:#52b788,color:#fff
    classDef impl   fill:#1e3a5f,stroke:#4a90d9,color:#fff
    classDef note   fill:#3a3a3a,stroke:#888,color:#ccc,font-style:italic
```

## Module Structure

The code is developed within this standalone repository and contributed upstream to `pgmpy` as a final PR.

```text
causal-bench/
├── pgmpy/
│   └── benchmark/
│       ├── __init__.py               # Public API exports
│       ├── simulators/
│       │   ├── __init__.py
│       │   ├── base.py               # BaseSimulator ABC + GroundTruth dataclass
│       │   ├── random_dag.py         # RandomDAGSimulator
│       │   ├── real_dataset.py       # RealDatasetSimulator
│       │   └── parametric_sweep.py   # ParametricSweepSimulator
│       ├── runner.py                 # BenchmarkRunner + ResultRecord
│       ├── evaluators/
│       │   ├── __init__.py
│       │   ├── base.py               # BaseEvaluator ABC
│       │   ├── causal_discovery.py   # CausalDiscoveryEvaluator
│       │   ├── ci_test.py            # CITestEvaluator
│       │   ├── effect_estimation.py  # EffectEstimationEvaluator
│       │   └── registry.py           # @register_evaluator decorator
│       └── report.py                 # BenchmarkReport
├── notebooks/
│   ├── 01_causal_discovery_comparison.ipynb
│   ├── 02_ci_test_power_analysis.ipynb
│   └── 03_effect_estimation_census.ipynb
├── docs/
│   └── benchmark/
│       ├── index.rst
│       ├── simulators.rst
│       ├── runner.rst
│       ├── evaluators.rst
│       └── report.rst
├── tests/
│   └── benchmark/
│       ├── test_simulators.py
│       ├── test_runner.py
│       ├── test_evaluators.py
│       ├── test_report.py
│       └── conftest.py
├── .github/
│   └── workflows/
│       └── ci.yml                   # GitHub Actions tests
├── pyproject.toml                   # Package metadata + dev dependencies
├── README.md
└── plan.md                          # Implementation plan
```

## Supported Tasks and Methods

| Task | Target Methods | Evaluator |
|---|---|---|
| Causal Discovery | PC, GES, MMHC, ExactSearch | `CausalDiscoveryEvaluator` |
| CI Testing | Chi-Square, G-Test, Fisher Z, KCI | `CITestEvaluator` |
| Effect Estimation | CausalInference | `EffectEstimationEvaluator` |

## Key Features

- **Combinatorial Execution Engine:** Executes every combination of simulator, method, and seed with error handling and wall-clock timing.
- **Parallelism:** Executes tasks concurrently via joblib (loky backend) to bypass pickling issues and race conditions.
- **Graceful Error Handling:** Full tracebacks are recorded without failing the entire run if a method times out or fails to converge.
- **Reproducible Exports:** Output full reproducible experiment records to JSON, summarizing seed, runtime, system info, and component configurations.

## Installation

```bash
# Editable install for development
pip install -e ".[dev]"
```

## Quick Start

```python
from pgmpy.benchmark import BenchmarkRunner, RandomDAGSimulator, CausalDiscoveryEvaluator
from pgmpy.estimators import PC, GES, MMHC

# 1. Setup
runner = BenchmarkRunner(
    simulators=[RandomDAGSimulator(n_nodes=10, edge_density=0.3)],
    methods=[PC(), GES(), MMHC()],
    evaluators=[CausalDiscoveryEvaluator()],
    n_seeds=20,
    n_jobs=4,
)

# 2. Run
report = runner.run()

# 3. Analyze
report.summary()                      # method x SHD/F1 table (mean +/- std)
report.to_json("results.json")        # reproducible record
df = report.to_dataframe()            # flat pandas DataFrame for plotting
```

## Development

```bash
pytest          # run tests
ruff check .    # lint
mypy pgmpy      # type-check
```