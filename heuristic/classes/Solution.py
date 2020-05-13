from __future__ import annotations

from collections import defaultdict
from copy import copy, deepcopy
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

    _used_classrooms: Set[Classroom]
    _used_teachers: Set[Teacher]

    def __init__(self, activities: List[Activity]):
        self.activities = activities
        self.unassigned = []

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
        from .Problem import Problem
        problem = Problem()

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

        # Excess capacity in current self-study assignments; these can be
        # re-used before new activities are required.
        capacity = sum(activity.classroom.capacity - activity.num_learners
                       for activity in self.activities
                       if activity.is_self_study())

        rooms_needed = 0

        for classroom in avail_rooms:
            capacity += classroom.capacity
            rooms_needed += 1

            if capacity >= len(self.unassigned):
                return rooms_needed <= len(avail_teachers)

        return False  # there is insufficient capacity

    def objective(self) -> float:
        # The ALNS algorithm solves a minimisation objective by default, but
        # the problem is actually a maximisation problem, hence the trick with
        # the minus.
        return -sum(map(methodcaller("objective"), self.activities))

    def preferences_by_module(self) \
            -> List[Tuple[float, Module, List[Learner]]]:
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
        return self._used_classrooms

    def used_teachers(self) -> Set[Teacher]:
        return self._used_teachers

    @classmethod
    def from_file(cls, location: str) -> Solution:
        from .Problem import Problem
        problem = Problem()

        with open(location) as file:
            assignments = json.load(file)

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

    def to_file(self, location: str):
        assignments = [[learner.id,
                        activity.module.id,
                        activity.classroom.id,
                        activity.teacher.id]
                       for activity in self.activities
                       for learner in activity.learners]

        with open(location, "w") as file:
            json.dump(assignments, file)
