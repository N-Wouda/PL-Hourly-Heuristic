from heuristic.classes import Solution
from .percentage_self_study import percentage_self_study


def percentage_instruction(solution: Solution) -> float:
    """
    Computes the percentage of learners receiving instruction.
    """
    return 100 - percentage_self_study(solution)
