from ..State import State
import numpy as np


def insert_learner(state: State) -> State:
    """
    Inserts a learner into a different activity, or self-study.
    """
    learner = np.random.choice(state.learners)['id']

    # We include the self-study module, as the learner could also be inserted
    # into a self-study assignment.
    preferences = [*state.most_preferred[learner, :], -1]

    for module in preferences:
        # This is the currently assigned module - it is unlikely a new
        # assignment will result in better performance.
        if module == state.learner_assignments[learner]:
            return state

        # The selected learner holds a preference for this module, *and* we
        # have an activity for this module.
        if module not in state.module_assignments:
            continue

        if _can_leave(state, learner) and _can_attend(state, module):
            new_state = State.from_state(state)
            new_state.learner_assignments[learner] = module

            return new_state

    return state


def _can_leave(state: State, learner: int) -> bool:
    # The learner must leave behind a valid activity (min_batch).
    current = state.learner_assignments[learner]
    classrooms = sum(1 for ct, mod
                     in state.classroom_teacher_assignments.items()
                     if mod == current)

    fellow_learners = np.count_nonzero(state.learner_assignments == current)

    # If it is strictly larger, it will still be at least equal when one
    # learner leaves.
    return fellow_learners > classrooms * state.min_batch


def _can_attend(state: State, module: int) -> bool:
    # The learner must not exceed the maximum learners in the proposed activity
    # (max_batch).
    classrooms = {
        classroom for classroom, teacher in state.classroom_teacher_assignments
        if state.classroom_teacher_assignments[(classroom, teacher)] == module}

    fellow_learners = np.count_nonzero(state.learner_assignments == module)

    if module == -1:    # only capacity is of relevance for self-study modules
        # If it is strictly smaller, it will still be at least equal when one
        # learner joins.
        return fellow_learners < sum(state.classrooms[classroom]['capacity']
                                     for classroom in classrooms)

    return fellow_learners < sum(min(state.max_batch,
                                     state.classrooms[classroom]['capacity'])
                                 for classroom in classrooms)
