from operator import truediv

from utils import State


def classroom_utilisation(state: State) -> float:
    """
    Computes the percentage of classrooms in use from the available classroom
    pool.
    """
    return 100 * truediv(len(state.classroom_teacher_assignments),
                         len(state.classrooms))
