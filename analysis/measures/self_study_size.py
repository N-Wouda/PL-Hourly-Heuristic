import numpy as np

from heuristic.constants import SELF_STUDY_MODULE_ID
from utils import State


def self_study_size(state: State) -> float:
    """
    Computes the average self-study activity size.
    """
    num_learners = np.count_nonzero(state.learner_assignments
                                    == SELF_STUDY_MODULE_ID)

    num_classrooms = sum(1 for _, module
                         in state.classroom_teacher_assignments.items()
                         if module == SELF_STUDY_MODULE_ID)

    if num_learners == 0:
        return 0

    return num_learners / num_classrooms
