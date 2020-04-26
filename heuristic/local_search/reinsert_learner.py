import numpy as np
from numpy.random import RandomState

from heuristic.classes import Solution


# TODO clean up this method, use it?

def reinsert_learner(state: Solution, rnd: RandomState) -> Solution:
    """
    Inserts a learner into a different activity, or self-study.
    """
    pass


def _can_leave(state: Solution, module: int) -> bool:
    # The learner must leave behind a valid activity (min_batch).
    classrooms = sum(1 for ct, mod
                     in state.classroom_teacher_assignments.items()
                     if mod == module)

    fellow_learners = np.count_nonzero(state.learner_assignments == module)

    # If it is strictly larger, it will still be at least equal when one
    # learner leaves.
    return fellow_learners > classrooms * state.min_batch


def _can_attend(state: Solution, module: int) -> bool:
    # The learner must not exceed the maximum learners in the proposed activity
    # (max_batch).
    classrooms = {
        classroom for classroom, teacher in state.classroom_teacher_assignments
        if state.classroom_teacher_assignments[(classroom, teacher)] == module}

    fellow_learners = np.count_nonzero(state.learner_assignments == module)

    if module == len(state.modules) - 1:         # self-study
        # If it is strictly smaller, it will still be at least equal when one
        # learner joins.
        return fellow_learners < sum(state.classrooms[classroom]['capacity']
                                     for classroom in classrooms)

    return fellow_learners < sum(min(state.max_batch,
                                     state.classrooms[classroom]['capacity'])
                                 for classroom in classrooms)
