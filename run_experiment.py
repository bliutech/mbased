#!/usr/bin/env python

from experiments.experiment import run_experiment

if __name__ == "__main__":
    passes: list[str] = ["sympy_pass"]

    res = run_experiment(passes, 10)

    print("========================================")
    print(res)
