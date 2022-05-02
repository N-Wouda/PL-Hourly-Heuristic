from __future__ import annotations

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
        pass  # TODO

    def to_file(self, loc: str):
        pass  # TODO
