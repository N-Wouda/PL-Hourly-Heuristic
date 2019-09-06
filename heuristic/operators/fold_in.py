import numpy as np
from numpy.random import RandomState

from heuristic.utils import random_activity, HeuristicState
from .simplify_activity import simplify_activity


def fold_in(state: HeuristicState, rnd: RandomState) -> HeuristicState:
    """
    Folds-in an activity into self-study, if applicable.
    """
    classroom, teacher, module = random_activity(state, rnd)

    # No need to fold-in self-study assignments, as those are already
    # simplified via another operator
    if module == len(state.modules) - 1:
        return state

    # Total learners assigned to the module associated with this activity
    total_learners = np.count_nonzero(state.learner_assignments == module)

    # All classrooms assigned to this module, excluding the currently selected
    # classroom
    classrooms = {
        classroom for classroom, teacher in state.classroom_teacher_assignments
        if state.classroom_teacher_assignments[(classroom, teacher)] == module}
    classrooms.discard(classroom)

    new_state = state.copy()

    total_capacity = sum(min(state.classrooms[room]['capacity'],
                             state.max_batch)
                         for room in classrooms)

    # This implies we can freely remove an activity, as there is sufficient
    # capacity in the remaining activities.
    if total_capacity >= total_learners:
        del new_state.classroom_teacher_assignments[(classroom, teacher)]

    # We have some excess learners in this case. Let us try to move those back
    # into self-study.
    if state.classrooms[classroom]['self_study_allowed'] \
            and module != len(state.modules) - 1:
        excess = total_learners - total_capacity

        module_learners = (state.learner_assignments == module)
        excess_learners = module_learners.nonzero()[0][:excess]

        new_state.learner_assignments[excess_learners] = len(state.modules) - 1
        new_state.classroom_teacher_assignments[(classroom, teacher)] \
            = len(state.modules) - 1

    return simplify_activity(new_state, module)
