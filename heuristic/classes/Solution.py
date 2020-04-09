from operator import methodcaller
from typing import List

from alns import State

from .Activity import Activity
from .Learner import Learner


class Solution(State):
    activities: List[Activity]
    unassigned: List[Learner]

    def __init__(self, activities: List[Activity]):
        self.activities = activities
        self.unassigned = []

    def objective(self) -> float:
        # The ALNS algorithm solves a minimisation objective by default, but
        # the problem is actually a maximisation problem, hence the trick with
        # the minus.
        return -sum(map(methodcaller("objective"), self.activities))
