from heapq import heappop, heappush

from numpy.random import Generator

from src.classes import Problem, Solution


def reinsert_learner(current: Solution,
                     generator: Generator,
                     problem: Problem) -> Solution:
    """
    Computes the best reinsertion moves for each learner, stores these in order,
    and executes them. This improves the solution further by moving learners
    into strictly improving assignments, if possible.
    """
    # Get all instruction activities, grouped by module. We only consider
    # moves out of self-study (self-study could be better as well, but the
    # structure of the repair operators makes it unlikely it is preferred over
    # the current learner assignment).
    activities_by_module = current.activities_by_module()
    del activities_by_module[problem.self_study_module]

    moves = []

    for from_activity in current.activities:
        if from_activity.num_learners <= problem.min_batch:
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
                    # This module does not result in any gain. Since we go
                    # through the modules in order of preference, any later
                    # modules are not better than this one. So we can stop
                    # here.
                    break

                for to_activity in activities_by_module[module_id]:
                    if to_activity.can_insert_learner():
                        # Random value only to ensure this orders well -
                        # learners and activities cannot be used to compare
                        # the tuples, and gain is the same for many values.
                        item = (-gain, generator.random(),
                                learner, from_activity, to_activity)
                        heappush(moves, item)

    if not moves:
        return current

    has_moved = set()  # tracks whether we've already moved a learner.

    while len(moves) != 0:
        *_, learner, from_activity, to_activity = heappop(moves)

        if learner not in has_moved \
                and from_activity.num_learners > problem.min_batch \
                and to_activity.can_insert_learner():
            from_activity.remove_learner(learner)
            to_activity.insert_learner(learner)
            has_moved.add(learner)

    return reinsert_learner(current, generator, problem)
