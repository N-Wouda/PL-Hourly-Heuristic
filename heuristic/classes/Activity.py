from __future__ import annotations

from copy import copy
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
    _objective: float

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

        self._objective = self._compute_objective()

    def __contains__(self, learner: Learner) -> bool:
        return learner in self._learners_set

    def __deepcopy__(self, memo={}) -> Activity:
        # This is not an *actual* deepcopy, but that's also not necessary
        # - the objects themselves don't change, only their composition, and
        # a shallow copy can account for that.
        return Activity(copy(self.learners),
                        self.classroom,
                        self.teacher,
                        self.module)

    @property
    def num_learners(self) -> int:
        return len(self.learners)

    @property
    def learners(self) -> List[Learner]:
        return self._learners

    @property
    def classroom(self) -> Classroom:
        return self._classroom

    @classroom.setter
    def classroom(self, classroom: Classroom):
        self._classroom = classroom

    @property
    def teacher(self) -> Teacher:
        return self._teacher

    @teacher.setter
    def teacher(self, teacher: Teacher):
        self._teacher = teacher

    @property
    def module(self) -> Module:
        return self._module

    def objective(self):
        return self._objective

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

            if not self.teacher.is_qualified_for(self.module):
                return False

        if not self.classroom.is_qualified_for(self.module):
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

        problem = Problem()

        if self.is_self_study():
            module_id = problem.most_preferred[learner.id, 0]

            objective = problem.preferences[learner.id, module_id]
            objective -= problem.penalty

            self._objective += objective
        else:
            self._objective += problem.preferences[learner.id, self.module.id]

    def can_remove_learner(self) -> bool:
        problem = Problem()
        return self.num_learners > problem.min_batch

    def remove_learner(self, learner: Learner):
        self.learners.remove(learner)
        self._learners_set.remove(learner)

        problem = Problem()

        if self.is_self_study():
            module_id = problem.most_preferred[learner.id, 0]

            objective = problem.preferences[learner.id, module_id]
            objective -= problem.penalty

            self._objective -= objective
        else:
            self._objective -= problem.preferences[learner.id, self.module.id]

    def remove_learners(self, learners: List[Learner]) -> int:
        """
        Attempts to remove the learners in the passed-in list. Returns the
        actual number removed (from the start of the list).
        """
        problem = Problem()
        removable = self.num_learners - problem.min_batch

        for learner in learners[:removable]:
            self.remove_learner(learner)

        return min(removable, len(learners))

    def can_split(self) -> bool:
        """
        Tests if this activity can be split, that is, there are sufficient
        learners to break the activity up into two activities.
        """
        problem = Problem()

        return self.num_learners >= 2 * problem.min_batch

    def split_with(self, classroom: Classroom, teacher: Teacher) -> Activity:
        """
        Splits this activity into two activities, using the passed-in classroom
        and teacher resources. The learners are halved, with each receiving
        half the current activity's learners - or less, according to batching
        requirements.

        Does not check whether whether the passed-in classroom and teacher are
        qualified for the activity's module.
        """
        problem = Problem()

        if self.module.is_self_study():
            splitter = min(self.num_learners // 2, classroom.capacity)
        else:
            splitter = min(self.num_learners // 2,
                           classroom.capacity,
                           problem.max_batch)

        learners = self.learners[-splitter:]
        self._learners = self.learners[:-splitter]

        activity = Activity(learners, classroom, teacher, self.module)

        # Since we split the learners, we should update our objective value
        # by subtracting the difference.
        self._objective -= activity.objective()

        return activity

    def switch_to_self_study(self):
        problem = Problem()

        self._module = problem.self_study_module
        self._objective -= problem.penalty * self.num_learners

    def _compute_objective(self):
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

    def __str__(self):
        return (f"(#{self.num_learners},"
                f" {self.module},"
                f" {self.classroom},"
                f" {self.teacher})")

    def __repr__(self):
        return "Activity" + str(self)
