from numpy.random import RandomState

from heuristic.classes import Solution
from .greedy_insert import greedy_insert


def break_out(destroyed: Solution, rnd_state: RandomState) -> Solution:
    """
    TODO.
    """
    return greedy_insert(destroyed, rnd_state)
