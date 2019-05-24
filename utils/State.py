from functools import lru_cache
from typing import Optional, Dict, List, Set

from .Data import Data
import numpy as np


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
        assert len(self._learner_assignments) == len(self.learners), \
            "Not all learners have been assigned!"

        modules = self.preferences[np.arange(len(self.preferences)),
                                   self.learner_assignments]

        num_self_study = np.count_nonzero(self.learner_assignments == -1)

        # The total value of the object is the preference for each module
        # assignment, minus the penalty for self study, where applicable.
        return sum(modules) - self.penalty * num_self_study

    @classmethod
    def from_state(cls, state: "State") -> "State":
        return cls(state._data,
                   state.learner_assignments,
                   state.classroom_teacher_assignments)
