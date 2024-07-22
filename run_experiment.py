#!/usr/bin/env python
from experiments.experiment import run_experiment
import argparse
import matplotlib.pyplot as plt
import numpy as np


def generate_plot(res) -> None:
    orig_op_counts: list[int] = []
    obf_op_counts: list[int] = []
    simplified_op_counts: list[int] = []

    orig_var_counts: list[int] = []
    obf_var_counts: list[int] = []
    simplified_var_counts: list[int] = []

    labels: list[str] = []

    for experiment in res:
        orig_op_counts.append(experiment[2])
        obf_op_counts.append(experiment[5])
        simplified_op_counts.append(experiment[8])

        orig_var_counts.append(experiment[3])
        obf_var_counts.append(experiment[6])
        simplified_var_counts.append(experiment[9])

        labels.append(f"N={experiment[0]}")

    op_formatted_experiments: dict[str, list[int]] = {
        # "Original": orig_op_counts,
        "Obfuscated": obf_op_counts,
        "Simplified": simplified_op_counts,
    }

    var_formatted_experiments: dict[str, list[int]] = {
        # "Original": orig_var_counts,
        "Obfuscated": obf_var_counts,
        "Simplified": simplified_var_counts,
    }

    x: np.ndarray = np.arange(len(labels))
    width: float = 0.25
    multiplier: int = 0

    fig, axes = plt.subplots(2, 2, layout="constrained")
    ax1: plt.Axes = axes[0, 0]
    ax2: plt.Axes = axes[1, 0]
    ax3: plt.Axes = axes[0, 1]
    ax4: plt.Axes = axes[1, 1]

    for attribute, measurement in op_formatted_experiments.items():
        offset = width * multiplier
        rects = ax1.bar(x + offset, measurement, width, label=attribute)
        ax1.bar_label(rects, padding=3)
        multiplier += 1

    ax1.set_title("Number Operations", y=1.02)
    ax1.set_xticks(x + width, labels)
    ax1.legend(loc="upper left", ncols=3)
    ax1.tick_params(axis="both", which="major", labelsize=4, rotation=70)

    multiplier: int = 0

    for attribute, measurement in var_formatted_experiments.items():
        offset = width * multiplier
        rects = ax2.bar(x + offset, measurement, width, label=attribute)
        ax2.bar_label(rects, padding=3)
        multiplier += 1

    ax2.set_title("Number Variables", y=1.02)
    ax2.set_xticks(x + width, labels)
    ax2.legend(loc="upper left", ncols=3)
    ax2.tick_params(axis="both", which="major", labelsize=4, rotation=70)

    experiment_range: np.array = np.arange(len(res))

    for attribute, measurement in op_formatted_experiments.items():
        ax3.plot(experiment_range, measurement, label=attribute)

    ax3.legend(loc="upper left", ncols=3)

    ax3.set_title("Number Operations", y=1.02)
    ax3.set_xticks(x + width, labels)
    ax3.legend(loc="upper left", ncols=3)
    ax3.tick_params(axis="both", which="major", labelsize=4, rotation=70)

    for attribute, measurement in var_formatted_experiments.items():
        ax4.plot(experiment_range, measurement, label=attribute)

    ax4.legend(loc="upper left", ncols=3)

    ax4.set_title("Number Variables", y=1.02)
    ax4.set_xticks(x + width, labels)
    ax4.legend(loc="upper left", ncols=3)
    ax4.tick_params(axis="both", which="major", labelsize=4, rotation=70)

    plt.show()


if __name__ == "__main__":
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Runs MBA simplification experiment"
    )
    parser.add_argument(
        "--plot", action="store_true", help="Display plots of the data."
    )

    args: argparse.Namespace = parser.parse_args()

    passes: list[str] = ["sympy_pass"]

    res = run_experiment(passes, 100)

    print("========================================")
    print(res)

    if args.plot:
        generate_plot(res)
