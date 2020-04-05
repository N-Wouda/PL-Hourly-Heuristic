import numpy as np
from numpy.random import RandomState

from heuristic.utils import random_activity, HeuristicState
from heuristic.utils.simplify_activity import simplify_activity


def fold_in(current: HeuristicState, rnd_state: RandomState) -> HeuristicState:
    """
    Folds-in an activity into self-study, if applicable.
    """
    classroom, teacher, module = random_activity(current, rnd_state)

    # No need to fold-in self-study assignments, as those are already
    # simplified via another operator
    if module == len(current.modules) - 1:
        return current

    # Total learners assigned to the module associated with this activity
    total_learners = np.count_nonzero(current.learner_assignments == module)

    # All classrooms assigned to this module, excluding the currently selected
    # classroom
    classrooms = {
        classroom for classroom, teacher in current.classroom_teacher_assignments
        if current.classroom_teacher_assignments[(classroom, teacher)] == module}
    classrooms.discard(classroom)

    new_state = current.copy()

    total_capacity = sum(min(current.classrooms[room]['capacity'],
                             current.max_batch)
                         for room in classrooms)

    # This implies we can freely remove an activity, as there is sufficient
    # capacity in the remaining activities.
    if total_capacity >= total_learners:
        del new_state.classroom_teacher_assignments[(classroom, teacher)]

    # We have some excess learners in this case. Let us try to move those back
    # into self-study.
    if current.classrooms[classroom]['self_study_allowed'] \
            and module != len(current.modules) - 1:
        excess = total_learners - total_capacity

        module_learners = (current.learner_assignments == module)
        excess_learners = module_learners.nonzero()[0][:excess]

        new_state.learner_assignments[excess_learners] = len(current.modules) - 1
        new_state.classroom_teacher_assignments[(classroom, teacher)] \
            = len(current.modules) - 1

    return simplify_activity(new_state, module)
