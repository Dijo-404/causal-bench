import time

from .report import BenchmarkReport, ResultRecord


class BenchmarkRunner:
    def __init__(self, simulators, methods, evaluators, n_seeds, n_jobs=1):
        self.simulators = simulators
        self.methods = methods
        self.evaluators = evaluators
        self.n_seeds = n_seeds

    def run(self) -> BenchmarkReport:
        records = []
        for sim in self.simulators:
            for seed in range(self.n_seeds):
                try:
                    df, ground_truth = sim.simulate(n_samples=1000, seed=seed)
                except Exception as e:
                    print(f"Simulation failed for seed {seed}: {e}")
                    continue

                for method in self.methods:
                    method_name = method.__class__.__name__
                    for evaluator in self.evaluators:
                        start_time = time.time()
                        metrics = {}
                        error = None
                        try:
                            method.fit(df)

                            predicted_graph = None
                            if hasattr(method, "model_"):
                                predicted_graph = method.model_
                            elif hasattr(method, "dag_"):
                                predicted_graph = method.dag_
                            elif hasattr(method, "predict"):
                                predicted_graph = method.predict(df)
                            elif hasattr(method, "estimate"):
                                predicted_graph = method.estimate()

                            if predicted_graph is None:
                                error = (
                                    "Could not locate predicted graph. "
                                    "Tried .model_, .dag_, .predict(), and .estimate()"
                                )
                            else:
                                metrics = evaluator.evaluate(
                                    predicted_graph, ground_truth
                                )
                        except Exception as e:
                            error = str(e)

                        runtime_ms = int((time.time() - start_time) * 1000)

                        records.append(
                            ResultRecord(
                                method_name=method_name,
                                seed=seed,
                                metrics=metrics,
                                runtime_ms=runtime_ms,
                                error=error,
                            )
                        )
        return BenchmarkReport(records=records)
