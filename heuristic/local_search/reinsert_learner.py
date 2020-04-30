from collections import defaultdict

from numpy.random import Generator

from heuristic.classes import Problem, Solution
from heapq import heappush, heappop


def reinsert_learner(current: Solution, generator: Generator) -> Solution:
    """
    TODO - explanation, and clean-up of the code (there's too much going on
     here).
    """
    problem = Problem()

    activities_by_module = defaultdict(list)

    for activity in current.activities:
        if activity.is_instruction():
            activities_by_module[activity.module.id].append(activity)

    moves = []

    for from_activity in current.activities:
        if not from_activity.can_remove_learner():
            continue

        for learner in from_activity.learners:
            for module_id in problem.most_preferred[learner.id]:
                module = problem.modules[module_id]

                if from_activity.is_self_study() \
                        and not learner.prefers_over_self_study(module):
                    break

                gain = problem.preferences[learner.id, module_id]
                gain -= problem.preferences[learner.id, from_activity.module.id]

                if gain <= 0:
                    break

                for to_activity in activities_by_module[module_id]:
                    if to_activity.can_insert_learner():
                        item = (-gain, learner, from_activity, to_activity)
                        heappush(moves, item)
                        break

    has_moved = set()

    while len(moves) != 0:
        _, learner, from_activity, to_activity = heappop(moves)

        if from_activity.can_remove_learner() \
                and to_activity.can_insert_learner() \
                and learner not in has_moved:
            from_activity.remove_learner(learner)
            to_activity.insert_learner(learner)
            has_moved.add(learner)

    return current
