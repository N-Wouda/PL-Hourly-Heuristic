from copy import deepcopy

from numpy.random import Generator

from src.classes import Problem, Solution


def most_mobile_teachers(current: Solution,
                         generator: Generator,
                         problem: Problem) -> Solution:
    """
    Removes activities with teachers that can be used to teach the most
    demanded activities that are not currently scheduled (or not scheduled
    enough). This should improve the solution by making the appropriate
    resources available for a better schedule.
    """
    destroyed = deepcopy(current)

    # 1. Determine the most demanded modules in general
    learner_ids = [learner.id for learner in problem.learners]
    all_prefs = problem.preferences_by_module(learner_ids)

    # 2. Determine which of those are not yet scheduled because no teachers
    #  are available to teach them.
    pass

    # 3. Determine if a teacher can be made available to teach the most demanded
    #    modules that are not currently scheduled.
    pass

    # 4. If a teacher can be made available, make them available.
    pass

    return destroyed
