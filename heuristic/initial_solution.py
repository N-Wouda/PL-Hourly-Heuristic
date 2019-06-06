from itertools import zip_longest

import numpy as np

from utils import Data, State


def initial_solution(data: Data) -> State:
    """
    Constructs an initial solution, where all learners are in self-study,
    and sufficient classroom-teacher pairs have been assigned to supervise
    the activities.
    """
    state = State(data)

    # Assign all learners to self-study.
    state = State(data, np.full_like(state.learners, -1, dtype=int))

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

        # Since the maximum activity size does not come into play for
        # self-study assignments.
        learners_to_assign -= min(learners_to_assign, classroom['capacity'])

        if learners_to_assign == 0:
            break

    assert learners_to_assign == 0, "There are still some learners unassigned!"

    return state
