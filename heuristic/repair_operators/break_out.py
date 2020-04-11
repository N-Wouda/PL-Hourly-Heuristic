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

    # Group learners by preference.
    learners = [learner.id for learner in destroyed.unassigned]
    not_assigned = set(problem.modules) - destroyed.used_modules()

    histogram = [(problem.preferences[learners, module.id].sum(), module)
                 for module in not_assigned]

    for _, module in sorted(histogram, reverse=True):
        if module.is_self_study():
            continue

        m_learners = [learner for learner in destroyed.unassigned
                      if problem.preferences[learner.id, module.id] > 0]

        if len(m_learners) < problem.min_batch:
            continue

        try:
            teacher = find_teacher(destroyed, module)
            classroom = find_classroom(destroyed, module)
        except LookupError:
            continue

        # Schedule the class, and continue with another iteration.
        # TODO sort this by best learners (most preferred)
        m_learners = m_learners[:min(problem.max_batch, classroom.capacity)]
        m_set = set(m_learners)

        activity = Activity(m_learners, classroom, teacher, module)

        destroyed.activities.append(activity)
        destroyed.unassigned = [learner for learner in destroyed.unassigned
                                if learner not in m_set]

        return break_out(destroyed, rnd_state)

    # Insert final learners into existing activities, if no new activity
    # can be scheduled.
    return greedy_insert(destroyed, rnd_state)
