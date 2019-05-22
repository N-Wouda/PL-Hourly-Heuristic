from heuristic.Configuration import Configuration


def convex_combination(first: float, second: float) -> float:
    """
    Returns a convex combination of two weights, using the ``OPERATOR_DECAY``
    parameter to combine them.
    """
    return sum([Configuration.OPERATOR_DECAY * first,
                (1 - Configuration.OPERATOR_DECAY) * second])
