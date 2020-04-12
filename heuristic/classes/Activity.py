from __future__ import annotations

from typing import List

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
        self._learners_set = set(learners)

        self._classroom = classroom
        self._teacher = teacher
        self._module = module

    def __contains__(self, learner: Learner) -> bool:
        return learner in self._learners_set

    @property
    def num_learners(self) -> int:
        return len(self.learners)

    @property
    def learners(self) -> List[Learner]:
        return self._learners

    @property
    def classroom(self) -> Classroom:
        return self._classroom

    @property
    def teacher(self) -> Teacher:
        return self._teacher

    @property
    def module(self) -> Module:
        return self._module

    def objective(self):
        # TODO this can probably be cached.

        problem = Problem()
        learner_ids = [learner.id for learner in self.learners]

        if self.is_self_study():
            # In self-study, everyone works on their most-preferred module,
            # but at the cost of a controlled penalty.
            modules = problem.most_preferred[learner_ids, 0]

            objective = problem.preferences[learner_ids, modules].sum()
            objective -= len(self.learners) * problem.penalty

            return objective

        return problem.preferences[learner_ids, self.module.id].sum()

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

            if self.classroom.room_type != self.module.room_type:
                return False

            if not self.teacher.is_qualified_for(self.module):
                return False

        if self.is_self_study():
            if not self.classroom.is_self_study_allowed():
                return False

        if self.num_learners > self.classroom.capacity:
            return False

        if not all(problem.preferences[learner.id, self.module.id] > 0
                   for learner in self.learners):
            return False

        return True

    def is_self_study(self) -> bool:
        return self.module.is_self_study()

    def is_instruction(self) -> bool:
        return not self.is_self_study()

    def can_insert_learner(self) -> bool:
        if self.is_self_study():
            return self.num_learners < self.classroom.capacity

        problem = Problem()
        return self.num_learners < min(problem.max_batch,
                                       self.classroom.capacity)

    def insert_learner(self, learner: Learner):
        self.learners.append(learner)
        self._learners_set.add(learner)

    def can_remove_learner(self) -> bool:
        problem = Problem()
        return self.num_learners > problem.min_batch

    def remove_learner(self, learner: Learner):
        self.learners.remove(learner)
        self._learners_set.remove(learner)

    def split_with(self, classroom: Classroom, teacher: Teacher) -> Activity:
        """
        Splits this activity into two activities, using the passed-in classroom
        and teacher resources. The learners are halved, with each receiving
        half the current activity's learners.

        Does not check whether splitting is feasible, nor whether the passed-in
        classroom and teacher are qualified for the activity's module.
        """
        splitter = self.num_learners // 2

        learners = self.learners[splitter:]
        self._learners = self.learners[:splitter]

        return Activity(learners, classroom, teacher, self.module)
