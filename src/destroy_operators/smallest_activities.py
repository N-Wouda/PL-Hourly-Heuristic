from copy import deepcopy

import numpy as np
from numpy.random import Generator

from src.classes import Problem, Solution
from src.functions import learners_to_remove


def smallest_activities(current: Solution,
                        generator: Generator,
                        problem: Problem) -> Solution:
    """
    Removes activities that consist of the smallest number of learners.
    """
    destroyed = deepcopy(current)

    indices = np.argsort([a.num_learners for a in destroyed.activities])
    activities = [destroyed.activities[idx] for idx in indices]

    for activity in activities:
        # TODO add randomness?

        if len(destroyed.unassigned) >= learners_to_remove():
            break

        destroyed.unassigned |= set(activity.learners)
        destroyed.remove_activity(activity)

    return destroyed
