from __future__ import annotations

from collections import defaultdict
from heapq import heappush
from operator import attrgetter, methodcaller
from typing import Dict, List, Set, Tuple

import simplejson as json
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

    def find_classroom_for(self, module: Module) -> Classroom:
        """
        Finds a free classroom that can host the passed-in module. If none
        exist, this function raises a LookupError.
        """
        from .Problem import Problem
        problem = Problem()

        available_classrooms = set(problem.classrooms_by_module[module])
        available_classrooms -= self.used_classrooms()

        for classroom in available_classrooms:
            if classroom.is_qualified_for(module):
                return classroom

        raise LookupError(f"No qualified, available classrooms for {module}.")

    def find_teacher_for(self, module: Module) -> Teacher:
        """
        Finds a teacher that can teach the passed-in module. If none exist, this
        function raises a LookupError.
        """
        from .Problem import Problem
        problem = Problem()

        available_teachers = set(problem.teachers_by_module[module])
        available_teachers -= self.used_teachers()

        # We select the worst qualifying teacher - e.g. for a second degree
        # module, we would first want to exhaust second degree teachers rather
        # than first degree, because those can be used to teach first degree
        # modules as well.
        qualified_teachers = []

        for teacher in available_teachers:
            if teacher.is_qualified_for(module):
                qualification = problem.qualifications[teacher.id, module.id]
                heappush(qualified_teachers,
                         (-qualification, teacher.id, teacher))

        if not qualified_teachers:
            raise LookupError(f"No qualified, available teachers for {module}.")

        return qualified_teachers[0][-1]

    def leaves_sufficient_for_self_study(self,
                                         classroom: Classroom,
                                         teacher: Teacher) -> bool:
        """
        Determines if using the passed-in classroom and teacher still leaves
        sufficient unused classrooms and teachers to schedule all unassigned
        learners into self-study. This ensures there always remains a feasible
        repair action.
        """
        from .Problem import Problem
        problem = Problem()

        avail_rooms = set(problem.classrooms) - self.used_classrooms()
        avail_rooms.remove(classroom)

        avail_rooms = filter(methodcaller("is_self_study_allowed"), avail_rooms)
        avail_rooms = sorted(avail_rooms,
                             key=attrgetter("capacity"),
                             reverse=True)

        avail_teachers = set(problem.teachers) - self.used_teachers()
        avail_teachers.remove(teacher)

        capacity = 0
        rooms_needed = 0

        for classroom in avail_rooms:
            capacity += classroom.capacity
            rooms_needed += 1

            if capacity > len(self.unassigned):
                return rooms_needed <= len(avail_teachers)

        return False  # these is insufficient capacity

    def objective(self) -> float:
        # The ALNS algorithm solves a minimisation objective by default, but
        # the problem is actually a maximisation problem, hence the trick with
        # the minus.
        return -sum(map(methodcaller("objective"), self.activities))

    def preferences_by_module(self) \
            -> List[Tuple[float, Module], List[Learner]]:
        """
        Computes the unassigned learners preferences by module. This list
        consists only of modules and learners for which the minimum batch size
        is respected.

        The list forms a heap, ordered by aggregate learner preferences (high
        to low). Use ``heapq`` for modification and access.
        """
        from .Problem import Problem
        problem = Problem()

        learners_by_module = defaultdict(list)

        for learner in self.unassigned:
            for module in problem.prefers_over_self_study[learner]:
                learners_by_module[module].append(learner)

        histogram = []

        for module, learners in learners_by_module.items():
            if len(learners) < problem.min_batch:
                # This cannot be scheduled (except maybe with self-study
                # learners, but that's not considered currently), so there's
                # no point in considering it further.
                continue

            aggregate = sum(problem.preferences[learner.id, module.id]
                            for learner in learners)

            heappush(histogram, (-aggregate, module, learners))

        return histogram

    def activities_by_module(self) -> Dict[Module, List[Activity]]:
        """
        Returns all activities, grouped by module.
        """
        grouped = defaultdict(list)

        for activity in self.activities:
            grouped[activity.module].append(activity)

        return grouped

    def used_classrooms(self) -> Set[Classroom]:
        return {activity.classroom for activity in self.activities}

    def used_teachers(self) -> Set[Teacher]:
        return {activity.teacher for activity in self.activities}

    def used_modules(self) -> Set[Module]:
        return {activity.module for activity in self.activities}

    def to_file(self, experiment: int, instance: int):
        assignments = [[learner.id,
                        activity.module.id,
                        activity.classroom.id,
                        activity.teacher.id]
                       for activity in self.activities
                       for learner in activity.learners]

        location = f"experiments/{experiment}/{instance}-heuristic.json"

        with open(location, "w") as file:
            json.dump(assignments, file)
