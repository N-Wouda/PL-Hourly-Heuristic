from __future__ import annotations

from collections import defaultdict
from heapq import heappush
from operator import methodcaller
from typing import List, Set, Tuple

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

    def preferences_by_module(self) -> List[Tuple[float, Module]]:
        """
        Computes the unassigned learners preferences by module.
        """
        from .Problem import Problem
        problem = Problem()

        learners_by_module = defaultdict(list)

        for learner in self.unassigned:
            for module_id in problem.most_preferred[learner.id]:
                module = problem.modules[module_id]

                if not learner.prefers_over_self_study(module):
                    # The modules are sorted by preference, so the first time
                    # this happens we can break for this learner (all subsequent
                    # modules will be even worse).
                    break

                learners_by_module[module].append(learner)

        histogram = []

        for module, learners in learners_by_module.items():
            aggregate = sum(problem.preferences[learner.id, module.id]
                            for learner in learners)

            # Negative aggregate, since Python's heap is a min heap but we need
            # to get the largest value first.
            heappush(histogram, (-aggregate, module, learners))

        return histogram

    def used_classrooms(self) -> Set[Classroom]:
        return {activity.classroom for activity in self.activities}

    def used_teachers(self) -> Set[Teacher]:
        return {activity.teacher for activity in self.activities}

    def used_modules(self) -> Set[Module]:
        return {activity.module for activity in self.activities}
