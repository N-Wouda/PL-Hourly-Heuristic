from copy import deepcopy

from numpy.random import RandomState

from heuristic.classes import Solution
from heuristic.functions import learners_to_remove


def random_activities(current: Solution, rnd_state: RandomState) -> Solution:
    """
    Randomly removes whole activities from the solution, until at least q
    learners have been removed.
    """
    destroyed = deepcopy(current)

    while len(destroyed.unassigned) < learners_to_remove():
        idx = rnd_state.randint(len(destroyed.activities))
        learners = destroyed.activities[idx].learners

        destroyed.unassigned.extend(learners)
        del destroyed.activities[idx]

    return destroyed
