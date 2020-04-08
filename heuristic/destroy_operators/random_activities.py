from copy import deepcopy

from heuristic.classes import Problem
from heuristic.functions import learners_to_remove


def random_activities(current, rnd_state):
    destroyed = deepcopy(current)
    problem = Problem()

    while len(destroyed.unassigned) < learners_to_remove():
        idx = rnd_state.choice(len(destroyed.activities))
        learners = destroyed.activities[idx].learners

        destroyed.unassigned.extend(learners)
        destroyed.remove_activity(idx)

    return destroyed
