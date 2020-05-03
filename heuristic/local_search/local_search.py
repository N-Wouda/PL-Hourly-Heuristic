from numpy.random import Generator

from heuristic.classes import Solution
from .reinsert_learner import reinsert_learner


def local_search(current: Solution, generator: Generator) -> Solution:
    """
    Performs a local search procedure whenever a new best solution is found,
    improving this solution further.
    """
    operators = [
        reinsert_learner,
        # TODO
    ]

    for operator in operators:
        current = operator(current, generator)

    return current
