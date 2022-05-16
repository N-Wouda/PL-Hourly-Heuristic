from __future__ import annotations

from copy import copy
from dataclasses import dataclass
from typing import List, Optional

import numpy as np

from .Classroom import Classroom
from .Learner import Learner
from .Module import Module
from .Teacher import Teacher


@dataclass
class Activity:
    learners: List[Learner]
    classroom: Classroom
    teacher: Teacher
    module: Module
    _objective: Optional[float] = None

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

    def learner_ids(self) -> np.ndarray:
        return np.array([learner.id for learner in self.learners])

    def objective(self):
        if self._objective is None:
            self._objective = self._compute_objective()

        return self._objective

    def is_self_study(self) -> bool:
        return self.module.is_self_study()

    def is_instruction(self) -> bool:
        return not self.is_self_study()

    def can_insert_learner(self, if_self_study: bool = False) -> bool:
        """
        Tests if the passed-in learner can be inserted into this activity.
        The optional argument determines whether the learner could be inserted,
        should this activity be (converted to) self-study.
        """
        if self.is_self_study() or if_self_study:
            return self.num_learners < self.classroom.capacity

        from src.functions import get_problem
        problem = get_problem()

        return self.num_learners < min(problem.max_batch,
                                       self.classroom.capacity)

    def insert_learner(self, learner: Learner):
        self.learners.append(learner)
        self._objective = None

    def remove_learner(self, learner: Learner):
        self.learners.remove(learner)
        self._objective = None

    def remove_learners(self, learners: List[Learner]) -> int:
        """
        Attempts to remove the learners in the passed-in list. Returns the
        actual number removed (from the start of the list).
        """
        from src.functions import get_problem
        problem = get_problem()
        removable = self.num_learners - problem.min_batch

        for learner in learners[:removable]:
            self.remove_learner(learner)

        return min(removable, len(learners))

    def can_split(self) -> bool:
        """
        Tests if this activity can be split, that is, there are sufficient
        learners to break the activity up into two activities.
        """
        from src.functions import get_problem
        problem = get_problem()
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
        from src.functions import get_problem
        problem = get_problem()

        if self.module.is_self_study():
            splitter = min(self.num_learners // 2, classroom.capacity)
        else:
            splitter = min(self.num_learners // 2,
                           classroom.capacity,
                           problem.max_batch)

        learners = self.learners[-splitter:]
        self.learners = self.learners[:-splitter]
        self._objective = None

        return Activity(learners, classroom, teacher, self.module)

    def switch_to_self_study(self):
        from src.functions import get_problem
        problem = get_problem()

        self.module = problem.self_study_module
        self._objective = None

    def _compute_objective(self):
        from src.functions import get_problem
        problem = get_problem()

        return problem.preferences[self.learner_ids(), self.module.id].sum()

    def __str__(self):
        return (f"(#{self.num_learners},"
                f" {self.module},"
                f" {self.classroom},"
                f" {self.teacher})")

    def __repr__(self):
        return "Activity" + str(self)
