from operator import truediv

from heuristic.classes import Problem
from utils import State


def classroom_utilisation(state: State) -> float:
    """
    Computes the percentage of classrooms in use from the available classroom
    pool.
    """
    problem = Problem()

    return 100 * truediv(len(state.classroom_teacher_assignments),
                         len(problem.classrooms))
