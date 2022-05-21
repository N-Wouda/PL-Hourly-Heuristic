from copy import deepcopy

from numpy.random import Generator

from src.classes import Problem, Solution
from src.functions import learners_to_remove


def random_activities(current: Solution,
                      generator: Generator,
                      problem: Problem) -> Solution:
    """
    Randomly removes whole activities from the solution, until at least q
    learners have been removed.
    """
    destroyed = deepcopy(current)

    while len(destroyed.unassigned) < learners_to_remove():
        idx = generator.integers(len(destroyed.activities))
        activity = destroyed.activities[idx]

        destroyed.unassigned |= set(activity.learners)
        destroyed.remove_activity(activity)

    return destroyed
