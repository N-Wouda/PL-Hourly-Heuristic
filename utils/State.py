from collections import defaultdict
from functools import lru_cache
from typing import Optional, Dict, List, Set, Tuple

import numpy as np

from .Data import Data
from .max_capacity import max_capacity


class State:

    def __init__(self, data: Data,
                 learner_assignments: Optional[np.ndarray] = None,
                 classroom_teacher_assignments: Optional[Dict] = None):
        self._data = data

        self._learner_assignments = np.empty_like(self.learners) \
            if learner_assignments is None \
            else learner_assignments.copy()

        self._classroom_teacher_assignments = {} \
            if classroom_teacher_assignments is None \
            else classroom_teacher_assignments.copy()

    @property
    def learner_assignments(self):
        return self._learner_assignments

    @property
    def classroom_teacher_assignments(self):
        return self._classroom_teacher_assignments

    @property
    def classroom_assignments(self) -> Set[int]:
        classrooms = {classroom for classroom, teacher
                      in self.classroom_teacher_assignments}

        assert len(classrooms) == len(self.classroom_teacher_assignments), \
            "Classrooms are not uniquely assigned!"

        return classrooms

    @property
    def teacher_assignments(self) -> Set[int]:
        teachers = {teacher for classroom, teacher
                    in self.classroom_teacher_assignments}

        assert len(teachers) == len(self.classroom_teacher_assignments), \
            "Teachers are not uniquely assigned!"

        return teachers

    @property
    def module_assignments(self) -> Set[int]:
        return {module for module
                in self.classroom_teacher_assignments.values()}

    @property
    def preferences(self):
        return self._data.preferences

    @property
    def most_preferred(self):
        return self._data.most_preferred

    @property
    def qualifications(self):
        return self._data.qualifications

    @property
    @lru_cache(1)
    def learners(self) -> List:
        return self._data.learners

    @property
    def teachers(self) -> List:
        return self._data.teachers

    @property
    def classrooms(self) -> List:
        return self._data.classrooms

    @property
    def modules(self) -> List:
        return self._data.modules

    @property
    def penalty(self) -> float:
        return self._data.penalty

    @property
    def min_batch(self) -> int:
        return self._data.min_batch

    @property
    def max_batch(self) -> int:
        return self._data.max_batch

    @lru_cache(None)
    def objective(self) -> float:
        """
        Evaluates the current solution, and returns the objective value.
        """
        assert len(self.learner_assignments) == len(self.learners), \
            "Not all learners have been assigned!"

        modules = self.preferences[np.arange(len(self.preferences)),
                                   self.learner_assignments]

        num_self_study = np.count_nonzero(self.learner_assignments
                                          == len(self.modules) - 1)

        # The total value of the object is the preference for each module
        # assignment, minus the penalty for self study, where applicable.
        return sum(modules) - self.penalty * num_self_study

    @classmethod
    def from_state(cls, state: "State") -> "State":
        return cls(state._data,
                   state.learner_assignments,
                   state.classroom_teacher_assignments)

    @classmethod
    def from_assignments(cls, data: Data, solution: List[Tuple]) -> "State":
        """
        Computes a State from a previously serialised solution. To serialise
        the assignments, use the ``to_assignments`` method.
        """
        learner_assignments = np.empty_like(data.learners, dtype=int)
        classroom_module_assignments = {}

        for assignment in solution:
            learner, module, classroom, teacher = assignment

            learner_assignments[learner] = module
            classroom_module_assignments[classroom, teacher] = module

        return cls(data, learner_assignments, classroom_module_assignments)

    def to_assignments(self) -> List[Tuple]:
        """
        Returns the serialised assignments, as a list of (learner, module,
        classroom, teacher)-lists. These may readily be dumped to the file
        system, and can be restored via the ``from_assignments`` class method.
        """
        assignments = []
        counters = defaultdict(lambda: 0)

        for module in range(len(self.modules)):
            # Select learners and activities belonging to each module, such
            # that we can assign them below.
            learners = [learner for learner in range(len(self.learners))
                        if self.learner_assignments[learner] == module]

            activities = [activity for activity, activity_module
                          in self.classroom_teacher_assignments.items()
                          if module == activity_module]

            # Assign at least min_batch number of learners to each activity.
            # This ensures the minimum constraint is met for all activities.
            for classroom, teacher in activities:
                for _ in range(self.min_batch):
                    if not learners:
                        break

                    assignment = (learners.pop(), module, classroom, teacher)
                    assignments.append(list(assignment))

                    counters[classroom] += 1

            # Next we flood-fill these activities with learners, until none
            # remain to be assigned.
            for classroom, teacher in activities:
                capacity = max_capacity(self.classrooms[classroom]['capacity'],
                                        self.max_batch,
                                        module == len(self.modules) - 1)

                while learners:
                    if counters[classroom] == capacity:     # classroom is full
                        break

                    assignment = (learners.pop(), module, classroom, teacher)
                    assignments.append(list(assignment))

                    counters[classroom] += 1

        return assignments
