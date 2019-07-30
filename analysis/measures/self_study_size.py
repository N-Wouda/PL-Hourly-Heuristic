import numpy as np

from utils import State


def self_study_size(state: State) -> float:
    """
    Computes the average self-study activity size.
    """
    self_study_module = len(state.modules) - 1

    num_learners = np.count_nonzero(state.learner_assignments
                                    == self_study_module)

    num_classrooms = sum(1 for _, module
                         in state.classroom_teacher_assignments.items()
                         if module == self_study_module)

    if num_learners == 0:
        return 0

    return num_learners / num_classrooms
