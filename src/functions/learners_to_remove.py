from functools import lru_cache

from src.classes import Problem
from src.constants import DEGREE_OF_DESTRUCTION


@lru_cache(1)
def learners_to_remove() -> int:
    problem = Problem()
    return int(DEGREE_OF_DESTRUCTION * problem.num_learners)
