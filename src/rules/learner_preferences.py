from typing import List, Tuple

from src.functions import get_problem


def learner_preferences(solution: List[Tuple]) -> bool:
    """
    Verifies learners are all assigned to modules they are eligible to take,
    that is, hold strictly positive preferences for.
    """
    problem = get_problem()

    return all(problem.preferences[learner, module] > 0
               for learner, module, *_ in solution)
