from copy import deepcopy

from numpy.random import RandomState

from heuristic.classes import Solution
from heuristic.functions import learners_to_remove


def random_learners(current: Solution, rnd_state: RandomState) -> Solution:
    """
    Randomly removes learners from the solution. The procedure randomly selects
    an activity, and checks if a learner can be removed from that activity. If
    so, a random learner in the activity is selected and removed. If not, a new
    activity is selected. The procedure continues until q learners have been
    removed.
    """
    destroyed = deepcopy(current)

    while len(destroyed.unassigned) < learners_to_remove():
        random_activity = rnd_state.choice(destroyed.activities)

        if random_activity.can_remove_learner():
            learner = rnd_state.choice(random_activity.learners)

            random_activity.remove_learner(learner)
            destroyed.unassigned.append(learner)

    return destroyed
