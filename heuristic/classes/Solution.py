from operator import methodcaller
from typing import List, Set

from alns import State

from .Activity import Activity
from .Classroom import Classroom
from .Learner import Learner
from .Module import Module
from .Teacher import Teacher


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

    def used_classrooms(self) -> Set[Classroom]:
        return {activity.classroom for activity in self.activities}

    def used_teachers(self) -> Set[Teacher]:
        return {activity.teacher for activity in self.activities}

    def used_modules(self) -> Set[Module]:
        return {activity.module for activity in self.activities}
