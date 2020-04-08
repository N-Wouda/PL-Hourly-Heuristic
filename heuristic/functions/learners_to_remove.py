from functools import lru_cache

from heuristic.classes import Problem
from heuristic.constants import DEGREE_OF_DESTRUCTION


@lru_cache(1)
def learners_to_remove() -> int:
    problem = Problem()
    return int(DEGREE_OF_DESTRUCTION * problem.num_learners)
