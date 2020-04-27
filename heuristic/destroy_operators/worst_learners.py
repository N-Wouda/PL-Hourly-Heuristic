from copy import deepcopy

import numpy as np

from heuristic.classes import Problem, Solution
from heuristic.functions import learners_to_remove, random_selection


def worst_learners(current: Solution, rnd_state):
    """
    TODO.
    """
    destroyed = deepcopy(current)

    problem = Problem()
    costs = np.zeros(problem.num_learners)

    # TODO carefully check this method and cost computation. Does this all
    #  work as planned?
    learner2activity = {}

    for activity in destroyed.activities:
        for learner in activity.learners:
            learner2activity[learner.id] = activity

            best_module_id = problem.most_preferred[learner.id, 0]
            curr_module_id = activity.module.id

            costs[learner.id] = problem.preferences[learner.id, best_module_id]
            costs[learner.id] -= problem.preferences[learner.id, curr_module_id]

            if activity.is_self_study():
                costs[learner.id] -= problem.penalty

    learners = np.argsort(costs)
    learners = learners[random_selection(rnd_state)]

    for learner_id in learners:
        activity = learner2activity[learner_id]

        if activity.can_remove_learner():
            learner = problem.learners[learner_id]

            destroyed.unassigned.append(learner)
            activity.remove_learner(learner)
        else:
            continue

        if len(destroyed.unassigned) == learners_to_remove():
            break

    return destroyed
