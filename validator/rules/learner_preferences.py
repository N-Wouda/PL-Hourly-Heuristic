from typing import List, Tuple

from utils import Data


def learner_preferences(data: Data, solution: List[Tuple]) -> bool:
    """
    Verifies learners are all assigned to modules they are eligible to take,
    that is, hold strictly positive preferences for.
    """
    return all(data.preferences[learner, module] > 0
               for learner, module, *_ in solution)
