from collections import defaultdict
from functools import lru_cache
from typing import Dict, List, Optional, Tuple

import numpy as np
from alns import State as ALNSState

from heuristic.classes import Problem
from heuristic.constants import SELF_STUDY_MODULE_ID


# TODO remove in favour of heuristic.classes.Solution

class State(ALNSState):

    def __init__(self,
                 learner_assignments: Optional[np.ndarray] = None,
                 classroom_teacher_assignments: Optional[Dict] = None):
        problem = Problem()

        self._learner_assignments = np.empty_like(problem.learners)

        if learner_assignments is not None:
            self._learner_assignments = learner_assignments

        self._classroom_teacher_assignments = {}

        if classroom_teacher_assignments is not None:
            self._classroom_teacher_assignments = classroom_teacher_assignments

    @property
    def learner_assignments(self):
        return self._learner_assignments

    @property
    def classroom_teacher_assignments(self):
        return self._classroom_teacher_assignments

    @lru_cache(None)
    def objective(self) -> float:
        """
        Evaluates the current solution, and returns the objective value.
        """
        problem = Problem()

        assert len(self.learner_assignments) == len(problem.learners), \
            "Not all learners have been assigned!"

        modules = problem.preferences[np.arange(len(problem.preferences)),
                                      self.learner_assignments]

        num_self_study = np.count_nonzero(self.learner_assignments
                                          == SELF_STUDY_MODULE_ID)

        # The total value of the object is the preference for each module
        # assignment, minus the penalty for self study, where applicable.
        return sum(modules) - problem.penalty * num_self_study

    @classmethod
    def from_assignments(cls, solution: List[Tuple]) -> "State":
        """
        Computes a State from a previously serialised solution. To serialise
        the assignments, use the ``to_assignments`` method.
        """
        problem = Problem()

        learner_assignments = np.empty_like(problem.learners, dtype=int)
        classroom_module_assignments = {}

        for assignment in solution:
            learner, module, classroom, teacher = assignment

            learner_assignments[learner] = module
            classroom_module_assignments[classroom, teacher] = module

        return cls(learner_assignments, classroom_module_assignments)

    def to_assignments(self) -> List[Tuple]:
        """
        Returns the serialised assignments, as a list of (learner, module,
        classroom, teacher)-lists. These may readily be dumped to the file
        system, and can be restored via the ``from_assignments`` class method.
        """
        problem = Problem()

        assignments = []
        counters = defaultdict(lambda: 0)

        for module in range(len(problem.modules)):
            # Select learners and activities belonging to each module, such
            # that we can assign them below.
            learners = [learner for learner in range(len(problem.learners))
                        if self.learner_assignments[learner] == module]

            activities = [activity for activity, activity_module
                          in self.classroom_teacher_assignments.items()
                          if module == activity_module]

            # Assign at least min_batch number of learners to each activity.
            # This ensures the minimum constraint is met for all activities.
            for classroom, teacher in activities:
                for _ in range(problem.min_batch):
                    if not learners:
                        break

                    assignment = (learners.pop(), module, classroom, teacher)
                    assignments.append(list(assignment))

                    counters[classroom] += 1

            # Next we flood-fill these activities with learners, until none
            # remain to be assigned.
            for classroom, teacher in activities:
                capacity = problem.classrooms[classroom].capacity

                if module != SELF_STUDY_MODULE_ID:
                    capacity = min(self.max_batch, capacity)

                while learners:
                    if counters[classroom] == capacity:  # classroom is full
                        break

                    assignment = (learners.pop(), module, classroom, teacher)
                    assignments.append(list(assignment))

                    counters[classroom] += 1

        return assignments
