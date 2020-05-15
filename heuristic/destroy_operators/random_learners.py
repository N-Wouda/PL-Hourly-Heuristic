from copy import deepcopy

from numpy.random import Generator

from heuristic.classes import Solution
from heuristic.functions import learners_to_remove


def random_learners(current: Solution, generator: Generator) -> Solution:
    """
    Randomly removes learners from the solution. The procedure randomly selects
    an activity, and checks if a learner can be removed from that activity. If
    so, a random learner in the activity is selected and removed. If not, a new
    activity is selected. The procedure continues until q learners have been
    removed.
    """
    destroyed = deepcopy(current)

    while len(destroyed.unassigned) < learners_to_remove():
        activity_idx = generator.integers(len(destroyed.activities))
        activity = destroyed.activities[activity_idx]

        if activity.can_remove_learner():
            learner_idx = generator.integers(len(activity.learners))
            learner = activity.learners[learner_idx]

            activity.remove_learner(learner)
            destroyed.unassigned.add(learner)

    return destroyed
