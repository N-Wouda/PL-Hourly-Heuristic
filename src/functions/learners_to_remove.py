from functools import lru_cache

from src.constants import DEGREE_OF_DESTRUCTION
from .problem import get_problem


@lru_cache(1)
def learners_to_remove() -> int:
    problem = get_problem()
    return int(DEGREE_OF_DESTRUCTION * problem.num_learners)
