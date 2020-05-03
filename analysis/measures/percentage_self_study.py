import numpy as np

from heuristic.classes import Problem
from heuristic.constants import SELF_STUDY_MODULE_ID
from utils import State


def percentage_self_study(state: State) -> float:
    """
    Computes the percentage of learners doing self-study.
    """
    problem = Problem()

    self_study_learners = np.count_nonzero(state.learner_assignments
                                           == SELF_STUDY_MODULE_ID)

    return 100 * self_study_learners / len(problem.learners)
