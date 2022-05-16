from __future__ import annotations

from collections import defaultdict
from copy import copy, deepcopy
from heapq import heapify, heappush
from typing import Dict, List, Set, Tuple

from alns import State

from .Activity import Activity
from .Classroom import Classroom
from .Learner import Learner
from .Module import Module
from .Teacher import Teacher


class Solution(State):
    activities: List[Activity]
    unassigned: Set[Learner]

    _used_classrooms: Set[Classroom]
    _used_teachers: Set[Teacher]

    def __init__(self, activities: List[Activity]):
        self.activities = activities
        self.unassigned = set()

        self._used_classrooms = {activity.classroom for activity in activities}
        self._used_teachers = {activity.teacher for activity in activities}

    def __deepcopy__(self, memo={}):
        # Not every part of a solution needs to be deep-copied - for the cached
        # attributes a shallow copy suffices. For the activities, see also the
        # motivation in Activity.
        sol = Solution([])
        sol.activities = deepcopy(self.activities)
        sol._used_classrooms = copy(self._used_classrooms)
        sol._used_teachers = copy(self._used_teachers)

        return sol

    def add_activity(self, activity: Activity):
        """
        Adds the passed-in activity to the solution.
        """
        self.activities.append(activity)

        self._used_classrooms.add(activity.classroom)
        self._used_teachers.add(activity.teacher)

    def remove_activity(self, idx: int):
        """
        Removes the activity at idx from the solution.
        """
        activity = self.activities[idx]

        self._used_classrooms.remove(activity.classroom)
        self._used_teachers.remove(activity.teacher)

        del self.activities[idx]

    def switch_classrooms(self, from_room: Classroom, to_room: Classroom):
        """
        Updates the solution's cache when a classroom switch is performed.
        """
        self._used_classrooms.remove(from_room)
        self._used_classrooms.add(to_room)

    def find_classroom_for(self, module: Module) -> Classroom:
        """
        Finds a free classroom that can host the passed-in module. If none
        exist, this function raises a LookupError.
        """
        from src.functions import get_problem
        problem = get_problem()

        avail_rooms = set(problem.classrooms_by_module[module])
        avail_rooms -= self.used_classrooms()

        for classroom in avail_rooms:
            if classroom.is_qualified_for(module):
                return classroom

        raise LookupError(f"No qualified, available classrooms for {module}.")

    def find_teacher_for(self, module: Module) -> Teacher:
        """
        Finds a teacher that can teach the passed-in module. If none exist, this
        function raises a LookupError.
        """
        from src.functions import get_problem
        problem = get_problem()

        available_teachers = set(problem.teachers_by_module[module])
        available_teachers -= self.used_teachers()

        # We select the worst qualifying teacher - e.g. for a second degree
        # module, we would first want to exhaust second degree teachers rather
        # than first degree, because those can be used to teach first degree
        # modules as well.
        qualified_teachers = []

        for teacher in available_teachers:
            if teacher.is_qualified_for(module):
                heappush(qualified_teachers,
                         (-teacher.degree, teacher.id, teacher))

        if not qualified_teachers:
            raise LookupError(f"No qualified, available teachers for {module}.")

        return qualified_teachers[0][-1]

    def objective(self) -> float:
        # The ALNS algorithm solves a minimisation objective by default, but
        # the problem is actually a maximisation problem, hence the trick with
        # the minus.
        return -sum(activity.objective() for activity in self.activities)

    def preferences_by_module(self) \
            -> List[Tuple[float, int, List[int]]]:
        """
        Computes the unassigned learners preferences by module. This list
        consists only of modules and learners for which the minimum batch size
        is respected.

        The list forms a heap, ordered by aggregate learner preferences (high
        to low). Use ``heapq`` for modification and access.
        """
        from src.functions import get_problem
        problem = get_problem()

        learners_by_module = defaultdict(list)

        for learner in self.unassigned:
            for module in problem.prefers_over_self_study[learner]:
                learners_by_module[module.id].append(learner.id)

        # Histogram (heap) of (preference, module, learner_ids) tuples.
        histogram = [(-problem.preferences[learners, mod_id].sum(),
                      mod_id,
                      learners)
                     for mod_id, learners in learners_by_module.items()
                     if len(learners) >= problem.min_batch]

        heapify(histogram)
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
        return self._used_classrooms

    def used_teachers(self) -> Set[Teacher]:
        return self._used_teachers

    def get_assignments(self) -> List[List[int]]:
        """
        Returns a list of (learner, module, classroom, teacher) assignments.
        """
        return [[learner.id,
                 activity.module.id,
                 activity.classroom.id,
                 activity.teacher.id]
                for activity in self.activities
                for learner in activity.learners]

    @classmethod
    def from_assignments(cls, assignments: List[List[int]]) -> Solution:
        """
        Reconstructs a Solution object from a list of (learner, module,
        classroom, teacher) assignments.
        """
        from src.functions import get_problem
        problem = get_problem()

        resources = defaultdict(list)

        for learner, module, classroom, teacher in assignments:
            learner = problem.learners[learner]
            resources[classroom, teacher, module].append(learner)

        solution = cls([])

        for (classroom, teacher, module), learners in resources.items():
            classroom = problem.classrooms[classroom]
            teacher = problem.teachers[teacher]
            module = problem.modules[module]

            activity = Activity(learners, classroom, teacher, module)
            solution.add_activity(activity)

        return solution
