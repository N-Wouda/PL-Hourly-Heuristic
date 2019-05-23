from functools import lru_cache
from typing import Optional, Dict, List, Set

from .Data import Data


class State:

    def __init__(self, data: Data,
                 learner_assignments: Optional[Dict] = None,
                 classroom_teacher_assignments: Optional[Dict] = None):
        self._data = data

        self._learner_assignments = {} \
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
        return {classroom for classroom, teacher
                in self.classroom_teacher_assignments}

    @property
    def teacher_assignments(self) -> Set[int]:
        return {teacher for classroom, teacher
                in self.classroom_teacher_assignments}

    @property
    @lru_cache(1)
    def preferences(self):
        return self._data.preferences

    @property
    @lru_cache(1)
    def qualifications(self):
        return self._data.qualifications

    @property
    @lru_cache(1)
    def learners(self) -> List:
        return self._data.learners

    @property
    @lru_cache(1)
    def teachers(self) -> List:
        return self._data.teachers

    @property
    @lru_cache(1)
    def classrooms(self) -> List:
        return self._data.classrooms

    @property
    @lru_cache(1)
    def modules(self) -> List:
        return self._data.modules

    @property
    @lru_cache(1)
    def penalty(self) -> float:
        return self._data.penalty

    @property
    @lru_cache(1)
    def min_batch(self) -> int:
        return self._data.min_batch

    @property
    @lru_cache(1)
    def max_batch(self) -> int:
        return self._data.max_batch

    @lru_cache(1)
    def evaluate(self) -> float:
        """
        Evaluates the current solution, and returns the objective value.
        """
        assert len(self._learner_assignments) == len(self.learners), \
            "Not all learners have been assigned!"

        modules = sum(self.preferences[learner, module]
                      for learner, module
                      in self._learner_assignments.items())

        penalty = sum(self.penalty for learner, module
                      in self._learner_assignments.items()
                      if module == self.modules[-1]['id'])

        # The total value of the object is the preference for each module
        # assignment, minus the penalty for self study, where applicable.
        return modules - penalty

    @classmethod
    def from_state(cls, state: "State") -> "State":
        return cls(state._data,
                   state.learner_assignments,
                   state.classroom_teacher_assignments)

    def __str__(self):
        return str(self.learner_assignments) \
            + str(self.classroom_teacher_assignments)
