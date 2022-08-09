from typing import List, Tuple


def learner_preferences(problem, solution: List[Tuple]) -> bool:
    """
    Verifies learners are all assigned to modules they are eligible to take,
    that is, hold strictly positive preferences for.
    """
    return all(problem.preferences[learner, module] > 0
               for learner, module, *_ in solution)
