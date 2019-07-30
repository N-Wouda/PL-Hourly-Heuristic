from utils import State
from .percentage_self_study import percentage_self_study


def percentage_instruction(state: State) -> float:
    """
    Computes the percentage of learners receiving instruction.
    """
    return 100 - percentage_self_study(state)
