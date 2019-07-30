from utils import State


def teacher_utilisation(state: State) -> float:
    """
    Computes the percentage of teachers in use from the available teacher pool.
    """
    return 100 * len(state.classroom_teacher_assignments) / len(state.teachers)
