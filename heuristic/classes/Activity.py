from __future__ import annotations

from copy import copy
from typing import List, Optional

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
    _objective: float
    _excess_capacity: int  # num learners that can be added to this activity

    def __init__(self,
                 learners: List[Learner],
                 classroom: Classroom,
                 teacher: Teacher,
                 module: Module,
                 objective: Optional[float] = None):
        self._learners = learners
        self._learners_set = set(learners)

        self._classroom = classroom
        self._teacher = teacher
        self._module = module

        if objective is None:
            self._objective = self._compute_objective()
        else:
            self._objective = objective

        problem = Problem()

        if self.is_instruction():
            self._excess_capacity = min(classroom.capacity, problem.max_batch)
        else:
            self._excess_capacity = classroom.capacity

        self._excess_capacity -= self.num_learners

    def __contains__(self, learner: Learner) -> bool:
        return learner in self._learners_set

    def __deepcopy__(self, memo={}) -> Activity:
        # This is not an *actual* deepcopy, but that's also not necessary
        # - the objects themselves don't change, only their composition, and
        # a shallow copy can account for that.
        return Activity(copy(self.learners),
                        self.classroom,
                        self.teacher,
                        self.module,
                        self._objective)

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

    def learner_ids(self) -> np.ndarray:
        return np.array([learner.id for learner in self.learners])

    def objective(self):
        return self._objective

    def is_self_study(self) -> bool:
        return self.module.is_self_study()

    def is_instruction(self) -> bool:
        return not self.is_self_study()

    def can_insert_learner(self) -> bool:
        return self._excess_capacity > 0

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

        self._excess_capacity -= 1

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

        self._excess_capacity += 1

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
        return self.num_learners >= 2 * Problem().min_batch

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

        self._objective -= activity.objective()  # book-keeping on cached vars.
        self._excess_capacity += len(learners)

        return activity

    def switch_to_self_study(self):
        problem = Problem()

        self._module = problem.self_study_module
        self._objective -= problem.penalty * self.num_learners

    def _compute_objective(self):
        problem = Problem()
        learner_ids = self.learner_ids()

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
