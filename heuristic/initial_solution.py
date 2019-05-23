from itertools import zip_longest

import numpy as np

from .Data import Data
from .State import State


def initial_solution(data: Data) -> State:
    state = State(data)

    # 1. Assign all learners to self-study.
    state = State(data, np.full_like(state.learners, -1, dtype=int))

    # 2. Construct (classroom, teacher) pairs for them.

    # Not all classrooms can host self-study, so we only select those that
    # can.
    classrooms = [classroom for classroom in state.classrooms
                  if classroom['self_study_allowed']]

    # In contrast, all teachers can supervise a self-study assignment.
    teachers = state.teachers

    # Assign learners until we have none left to assign
    learners_to_assign = len(state.learners)

    for classroom, teacher in zip_longest(classrooms, teachers):
        assert classroom is not None, "Classroom is None!"
        assert teacher is not None, "Teacher is None!"

        assignment = (classroom['id'], teacher['id'])

        state.classroom_teacher_assignments[assignment] = -1

        learners_to_assign -= min(learners_to_assign, classroom['capacity'])

        if learners_to_assign == 0:
            break

    return state
