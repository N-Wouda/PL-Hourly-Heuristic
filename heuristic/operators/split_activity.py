from numpy.random import RandomState

from heuristic.utils import (find_teacher, find_classroom, HeuristicState,
                             random_activity)

import numpy as np


def split_activity(state: HeuristicState, rnd: RandomState) -> HeuristicState:
    """
    Splits an activity in two, if applicable.
    """
    classroom, teacher, module = random_activity(state, rnd)

    # Check if a split is possible: we should not drop below min_batch
    # assignments to each activity with this module.
    num_learners = np.count_nonzero(state.learner_assignments == module)
    num_activities = 1 + sum(1
                             for _, mod
                             in state.classroom_teacher_assignments.items()
                             if mod == module)

    # A new activity assignment would result in insufficient learners for each
    # classroom activity.
    if state.min_batch * num_activities > num_learners:
        return state

    other_classroom = find_classroom(state, module)
    other_teacher = find_teacher(state, module)

    if other_teacher is not False and other_classroom is not False:
        new_state = state.copy()

        new_assignment = (other_classroom, other_teacher)
        new_state.classroom_teacher_assignments[new_assignment] = module

        return new_state

    return state
