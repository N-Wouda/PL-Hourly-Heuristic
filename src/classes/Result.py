from __future__ import annotations

import json
from dataclasses import dataclass
from functools import cached_property
from typing import List

import matplotlib.pyplot as plt
import numpy as np

from .Solution import Solution


@dataclass
class Result:
    assignments: List[List[int]]
    runtimes: List[float]
    lbs: List[float]
    ubs: List[float]
    objective: float

    @cached_property
    def solution(self) -> Solution:
        return Solution.from_assignments(self.assignments)

    @classmethod
    def from_file(cls, loc: str) -> Result:
        with open(loc, "r") as fh:
            data = json.load(fh)

        runtimes = data["runtimes"] if "runtimes" in data else data["run_times"]

        return cls(data["assignments"],
                   runtimes,
                   data["lbs"],
                   data["ubs"],
                   data["objective"])

    def to_file(self, loc: str):
        with open(loc, "w") as fh:
            json.dump(vars(self), fh)

    def measures(self) -> dict[str, ...]:
        return {
            "objective": self.objective,
            "bounds": [self.lbs[-1], self.ubs[-1]],
            "iterations": self.iterations(),
            "run-time (wall)": sum(self.runtimes),
            "instruction (# learners)": self.num_instruction(),
            "self-study (# learners)": self.num_self_study(),
            "activities (#)": self.num_activities(),
            "instruction activity sizes": self.instruction_sizes(),
            "self-study activity sizes": self.self_study_sizes(),
        }

    def iterations(self):
        return len(self.runtimes)

    def objective(self):
        return self.objective

    def num_activities(self):
        return len(self.solution.activities)

    def num_self_study(self):
        return sum(a.num_learners for a in self.solution.activities
                   if a.is_self_study())

    def num_instruction(self):
        return sum(a.num_learners for a in self.solution.activities
                   if a.is_instruction())

    def instruction_sizes(self):
        return [a.num_learners for a in self.solution.activities
                if a.is_instruction()]

    def self_study_sizes(self):
        return [a.num_learners for a in self.solution.activities
                if a.is_self_study()]

    def plot_convergence(self):
        x = np.cumsum(self.runtimes)
        lbs = np.array(self.lbs)
        ubs = np.array(self.ubs)

        _, ax = plt.subplots(figsize=(12, 8))

        ax.plot(x[lbs > 0], lbs[lbs > 0], label="Lower bound")
        ax.plot(x[lbs > 0], ubs[lbs > 0], label="Upper bound")
        ax.plot(x[-1], self.objective, 'r*', markersize=18, label="Optimal")

        ax.set_xlabel("Run-time (s)")
        ax.set_ylabel("Objective")
        ax.set_title("Convergence plot")
        ax.legend(frameon=False)

        plt.tight_layout()
        plt.show()

    def __str__(self):
        measures = self.measures()

        lb, ub = measures["bounds"]
        runtime = measures["run-time (wall)"]
        instruction = measures["instruction (# learners)"]
        self_study = measures["self-study (# learners)"]

        lines = ["Solution results",
                 "================",
                 f"      objective: {self.objective:.2f}",
                 f"         bounds: [{lb:.2f}, {ub:.2f}]",
                 f"run-time (wall): {runtime:.2f}s",
                 f"    instruction: {instruction} learners",
                 f"     self-study: {self_study} learners"]

        return "\n".join(lines)
