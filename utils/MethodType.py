from enum import Enum, unique


@unique
class MethodType(Enum):
    """
    The type of method used to arrive at a result.
    """
    ILP = 'ilp'
    HEURISTIC = 'heuristic'
