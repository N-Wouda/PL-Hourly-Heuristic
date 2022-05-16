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
    objective: float
    run_times: List[float]
    lbs: List[float]
    ubs: List[float]

    @cached_property
    def solution(self) -> Solution:
        return Solution.from_assignments(self.assignments)

    @classmethod
    def from_file(cls, loc: str) -> Result:
        with open(loc, "r") as fh:
            data = json.load(fh)

        return cls(data["assignments"],
                   data["objective"],
                   data["run_times"],
                   data["lbs"],
                   data["ubs"])

    def to_file(self, loc: str):
        with open(loc, "w") as fh:
            json.dump(vars(self), fh)

    def measures(self) -> dict[str, ...]:
        return {
            "objective": self.objective(),
            "runtime": sum(self.run_times),
            "instruction (# learners)": self.num_instruction(),
            "self-study (# learners)": self.num_self_study(),
            "activities (#)": self.num_activities(),
            "instruction activity sizes": self.instruction_sizes(),
            "self-study activity sizes": self.self_study_sizes(),
        }

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
        x = np.cumsum(self.run_times)
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
        lb = self.lbs[-1]
        ub = self.ubs[-1]
        run_time = sum(self.run_times)

        lines = ["Solution results",
                 "================",
                 f"      objective: {self.objective:.2f}",
                 f"         bounds: [{lb:.2f}, {ub:.2f}]",
                 f"run-time (wall): {run_time:.2f}s"]

        return "\n".join(lines)
