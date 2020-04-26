from __future__ import annotations

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

        # First we obtain the set of modules for which the unassigned learners
        # hold preferences (i.e., there is at least one learner with positive
        # preference). This saves a lot in meaningless work being done grouping
        # them later.
        module_ids = set()

        for learner in self.unassigned:
            module_ids.update(problem.most_preferred[learner.id, :])

        histogram = []

        for module_id in module_ids:
            module = problem.modules[module_id]

            if module.is_self_study():
                continue

            learners = [learner for learner in self.unassigned
                        if learner.prefers_over_self_study(module)]

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
