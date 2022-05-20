from copy import deepcopy

import numpy as np
from numpy.random import Generator

from src.classes import Problem, Solution
from src.functions import learners_to_remove


def worst_learners(current: Solution,
                   generator: Generator,
                   problem: Problem) -> Solution:
    """
    Computes the costs for each learner, as the difference between their best
    and current assignments. Using a skewed distribution, q of the worst cost
    learners are randomly selected and removed from the solution.
    """
    destroyed = deepcopy(current)
    costs = np.zeros(problem.num_learners)

    assigned_activities = {}

    for activity in destroyed.activities:
        for learner in activity.learners:
            assigned_activities[learner.id] = activity

        learner_ids = activity.learner_ids()

        # The cost is the cost of the best possible assignment for this
        # learner, minus the cost of the current assignment (including
        # self-study penalty, if applicable). The larger the cost, the more
        # suboptimal the current assignment.
        best_module_id = problem.most_preferred[learner_ids, 0]
        curr_module_id = activity.module.id

        costs[learner_ids] = problem.preferences[learner_ids, best_module_id]
        costs[learner_ids] -= problem.preferences[learner_ids, curr_module_id]

        if activity.is_self_study():
            # Per the paper:   pref(best) - (pref(curr) - <maybe penalty>)
            #                = pref(best) - pref(curr) + <maybe penalty>.
            costs[learner_ids] += problem.penalty

    learners = np.argsort(costs)
    learners = learners[-_rnd_select(generator, problem)]

    for learner_id in learners:
        activity = assigned_activities[learner_id]

        if activity.num_learners > problem.min_batch:
            learner = problem.learners[learner_id]

            destroyed.unassigned.add(learner)
            activity.remove_learner(learner)

    return destroyed


def _rnd_select(generator: Generator, problem: Problem):
    """
    Implements a random selection mechanism, which selects random indices for
    a certain list of num_learners length (e.g., for a cost computation),
    favouring smaller indices.
    """
    triangle = np.arange(learners_to_remove(), 0, -1)

    probabilities = np.ones(problem.num_learners)
    probabilities[:learners_to_remove()] = triangle
    probabilities = probabilities / np.sum(probabilities)

    return generator.choice(problem.num_learners,
                            learners_to_remove(),
                            replace=False,
                            p=probabilities)
