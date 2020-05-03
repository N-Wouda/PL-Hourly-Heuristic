from operator import truediv

from heuristic.classes import Problem
from utils import State


def teacher_utilisation(state: State) -> float:
    """
    Computes the percentage of teachers in use from the available teacher pool.
    """
    problem = Problem()

    return 100 * truediv(len(state.classroom_teacher_assignments),
                         len(problem.teachers))
