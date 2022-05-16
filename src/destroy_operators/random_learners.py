from copy import deepcopy

from numpy.random import Generator

from src.classes import Problem, Solution
from src.functions import learners_to_remove


def random_learners(current: Solution,
                    generator: Generator,
                    problem: Problem) -> Solution:
    """
    Randomly removes learners from the solution. The procedure randomly selects
    an activity, and checks if a learner can be removed from that activity. If
    so, a random learner in the activity is selected and removed. If not, a new
    activity is selected. The procedure continues until q learners have been
    removed.
    """
    destroyed = deepcopy(current)

    activities = [activity for activity in destroyed.activities
                  if activity.num_learners > problem.min_batch]

    while len(destroyed.unassigned) < learners_to_remove():
        a_frac, l_frac = generator.random(size=2)

        activity_idx = int(a_frac * len(activities))
        activity = activities[activity_idx]

        learner_idx = int(l_frac * len(activity.learners))
        learner = activity.learners[learner_idx]

        activity.remove_learner(learner)
        destroyed.unassigned.add(learner)

        if activity.num_learners == problem.min_batch:
            activities.remove(activity)

    return destroyed
