from ..State import State
import numpy as np
from heuristic.utils import random_activity


def fold_in(state: State) -> State:
    """
    Folds-in an activity into self-study, if applicable.
    """
    classroom, teacher, module = random_activity(state)

    # Total learners assigned to the module associated with this activity
    total_learners = np.count_nonzero(state.learner_assignments == module)

    # All classrooms assigned to this module, excluding the currently selected
    # classroom
    classrooms = {
        classroom for classroom, teacher in state.classroom_teacher_assignments
        if state.classroom_teacher_assignments[(classroom, teacher)] == module}
    classrooms.discard(classroom)

    if module == -1:    # only capacity is of relevance for self-study modules
        total_capacity = sum(state.classrooms[room]['capacity']
                             for room in classrooms)
    else:
        total_capacity = sum(min(state.classrooms[room]['capacity'],
                                 state.max_batch)
                             for room in classrooms)

    if total_capacity >= total_learners:
        new_state = State.from_state(state)
        del new_state.classroom_teacher_assignments[(classroom, teacher)]

        return new_state

    return state
