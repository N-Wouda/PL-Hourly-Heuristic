from __future__ import annotations

import json
from dataclasses import dataclass
from typing import List

from .Solution import Solution


@dataclass
class Result:
    assignments: List[List[int]]
    objective: float
    run_times: List[float]
    lbs: List[float]
    ubs: List[float]

    @property
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
