from copy import deepcopy

import numpy as np
from numpy.random import Generator

from src.classes import Problem, Solution
from src.functions import learners_to_remove


def most_slack_classrooms(current: Solution,
                          generator: Generator,
                          problem: Problem) -> Solution:
    """
    Removes activities with underutilised classrooms, where we define the
    utilisation as # learners / classroom capacity.
    """
    destroyed = deepcopy(current)

    indices = np.argsort([a.utilisation for a in destroyed.activities])
    activities = [destroyed.activities[idx] for idx in indices]

    for activity in activities:
        # TODO exclude self-study? Add randomness?

        if len(destroyed.unassigned) >= learners_to_remove():
            break

        destroyed.unassigned |= set(activity.learners)
        destroyed.remove_activity(activity)

    return destroyed
