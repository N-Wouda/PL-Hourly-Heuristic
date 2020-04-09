from collections import defaultdict

from numpy.random import RandomState

from heuristic.classes import Problem, Solution
from heuristic.constants import SELF_STUDY_MODULE_ID


def greedy_insert(destroyed: Solution, rnd_state: RandomState) -> Solution:
    """
    Greedily inserts learners into the best, feasible activities. If no
    activity can be found for a learner, (s)he is inserted into self-study
    instead.
    """
    rnd_state.shuffle(destroyed.unassigned)

    problem = Problem()

    activities_by_module = defaultdict(list)

    for activity in destroyed.activities:
        activities_by_module[activity.module.id].append(activity)

    while len(destroyed.unassigned) != 0:
        learner = destroyed.unassigned.pop()

        # Attempts to insert the learner into the most preferred, feasible
        # instruction activity. If no such activities exist the learner is
        # inserted into a self-study activity instead.
        for module in problem.most_preferred[learner.id]:
            if module not in activities_by_module:
                continue

            if _insert(learner, activities_by_module[module]):
                break
        else:
            # Learner could not be inserted into a regular instruction activity,
            # so now we opt for self-study.
            if not _insert(learner, activities_by_module[SELF_STUDY_MODULE_ID]):
                # TODO create new activity for this case. Split an existing
                #  activity to get this done?
                pass

    return destroyed


def _insert(learner, activities):
    for activity in activities:
        if activity.can_insert_learner():
            activity.insert_learner(learner)
            return True

    return False
