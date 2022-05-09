from __future__ import annotations

import json
from dataclasses import dataclass
from typing import List

from .Solution import Solution


@dataclass
class Result:
    assignments: List[List[int, int, int, int]]
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
                   data["run_times"],
                   data["lbs"],
                   data["ubs"])

    def to_file(self, loc: str):
        with open(loc, "w") as fh:
            json.dump(vars(self), fh)
