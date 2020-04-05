from typing import List

from utils import State
from .Activity import Activity


class Solution(State):
    activities: List[Activity]

    def objective(self) -> float:
        # The ALNS algorithm solves a minimisation objective by default, but
        # the problem is actually a maximisation problem, hence this trick.
        return -super().objective()
