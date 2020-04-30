from numpy.random import Generator

from heuristic.classes import Solution
from .reinsert_learner import reinsert_learner
from .simplify_activities import simplify_activities


def local_search(current: Solution, generator: Generator) -> Solution:
    """
    TODO.
    """
    operators = [
        reinsert_learner,
        simplify_activities,
        # TODO
    ]

    for operator in operators:
        current = operator(current, generator)

    return current
