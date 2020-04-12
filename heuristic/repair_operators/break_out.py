import numpy as np
from numpy.random import RandomState

from heuristic.classes import Activity, Problem, Solution
from heuristic.utils import find_classroom, find_teacher
from .greedy_insert import greedy_insert


def break_out(destroyed: Solution, rnd_state: RandomState) -> Solution:
    """
    TODO.
    """
    problem = Problem()

    histogram = []

    for module in problem.modules:
        if module.is_self_study():
            continue

        aggregate = sum(problem.preferences[learner.id, module.id]
                        for learner in destroyed.unassigned
                        if _is_better_than_self_study(learner, module))

        histogram.append((aggregate, module))

    for _, module in sorted(histogram, reverse=True):
        # We collect all unassigned learner that can be assigned to this module,
        # and snoop off any self-study learner we can as well.
        to_assign = [learner for learner in destroyed.unassigned
                     if _is_better_than_self_study(learner, module)]

        if len(to_assign) < problem.min_batch:
            # TODO we can probably also grab a few from self-study for the
            #   comparison.
            continue

        try:
            classroom = find_classroom(destroyed, module)
            teacher = find_teacher(destroyed, module)
        except LookupError:
            continue

        max_size = min(classroom.capacity, problem.max_batch)

        for activity in destroyed.activities:
            if activity.is_self_study():
                # TODO sort by best?
                learners = [learner for learner in activity.learners
                            if _is_better_than_self_study(learner, module)]

                while activity.can_remove_learner() \
                        and len(to_assign) < max_size \
                        and len(learners) != 0:
                    learner = learners.pop()
                    activity.remove_learner(learner)
                    to_assign.append(learner)

        if len(to_assign) > max_size:
            # TODO sort by best?
            to_assign = to_assign[:max_size]

        activity = Activity(to_assign, classroom, teacher, module)

        destroyed.activities.append(activity)
        destroyed.unassigned = [learner for learner in destroyed.unassigned
                                if learner not in activity]

        return break_out(destroyed, rnd_state)

    # Insert final learners into existing activities, if no new activity
    # can be scheduled.
    return greedy_insert(destroyed, rnd_state)


def _is_better_than_self_study(learner, module) -> bool:
    preferences = Problem().preferences
    return preferences[learner.id, module.id] > learner.self_study_objective()
