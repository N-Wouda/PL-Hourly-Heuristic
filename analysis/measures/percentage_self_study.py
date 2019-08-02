from utils import State
import numpy as np


def percentage_self_study(state: State) -> float:
    """
    Computes the percentage of learners doing self-study.
    """
    self_study_module = len(state.modules) - 1

    self_study_learners = np.count_nonzero(state.learner_assignments
                                           == self_study_module)

    return 100 * self_study_learners / len(state.learners)
