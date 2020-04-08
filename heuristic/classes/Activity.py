from typing import List

import numpy as np

from .Classroom import Classroom
from .Learner import Learner
from .Module import Module
from .Problem import Problem
from .Teacher import Teacher


class Activity:
    _learners: List[Learner]
    _classroom: Classroom
    _teacher: Teacher
    _module: Module

    def __init__(self,
                 learners: List[Learner],
                 classroom: Classroom,
                 teacher: Teacher,
                 module: Module):
        self._learners = learners
        self._classroom = classroom
        self._teacher = teacher
        self._module = module

    @property
    def num_learners(self) -> int:
        return len(self._learners)

    def objective(self):
        problem = Problem()
        learner_ids = [learner.id for learner in self._learners]

        if self.is_self_study():
            # Preferences minus self-study penalty.
            objective = np.sum(problem.most_preferred[learner_ids, 0])
            objective -= len(self._learners) * problem.penalty

            return objective

        return np.sum(problem.preferences[learner_ids, self._module.id])

    def is_feasible(self) -> bool:
        """
        Tests if this activity is feasible. There are several constraints that
        must be satisfied, and this method tests if that is the case.
        """
        problem = Problem()

        if self.num_learners < problem.min_batch:
            return False

        if self.is_instruction():
            if self.num_learners > problem.max_batch:
                return False

            if self._classroom.room_type != self._module.room_type:
                return False

            if not self._teacher.is_qualified_for(self._module):
                return False

        if self.is_self_study():
            if not self._classroom.is_self_study_allowed():
                return False

        if self.num_learners > self._classroom.capacity:
            return False

        if not all(problem.preferences[learner.id, self._module.id] > 0
                   for learner in self._learners):
            return False

        return True

    def is_self_study(self) -> bool:
        return self._module.is_self_study()

    def is_instruction(self) -> bool:
        return not self.is_self_study()
