from typing import List, Tuple

from heuristic.classes import Problem


def learner_preferences(solution: List[Tuple]) -> bool:
    """
    Verifies learners are all assigned to modules they are eligible to take,
    that is, hold strictly positive preferences for.
    """
    problem = Problem()

    return all(problem.preferences[learner, module] > 0
               for learner, module, *_ in solution)
